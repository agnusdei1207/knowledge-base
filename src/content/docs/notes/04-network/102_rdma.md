---
sidebar:
  order: 102
  label: "102. RDMA 원격 직접 메모리 접근"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초저지연 고대역폭 메모리 전송 : RDMA (Remote Direct Memory Access)"
date: "2026-08-26T14:10:47+09:00"
tags:
  - "notes-network"
weight: 102
extra:
  question_no: "102"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "커널 우회(Kernel Bypass), 제로 카피(Zero-Copy), CPU 오프로드, 큐 페어(QP) 및 메모리 키(rkey/lkey)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RDMA (Remote Direct Memory Access)**: OS 커널과 CPU 개입 없이 RNIC가 원격 호스트의 등록된 물리 메모리로 직접 DMA 읽기/쓰기를 수행하는 기술.
- **Kernel Bypass & Zero-Copy**: OS 시스템 콜과 컨텍스트 스위칭을 제거하고 소켓 버퍼 복사 없이 사용자 버퍼에서 직접 송수신하는 메커니즘.

</details>

- 정의/개념: RNIC가 **커널 우회·제로 카피**로 원격 메모리에 직접 전송
- 배경/필요성: TCP/IP의 시스템 호출·복사로 **CPU·분산 학습 병목** 발생

#### 한줄 요약
- 커널 우회, 제로 카피, CPU 오프로드를 통해 마이크로초 미만의 초저지연 메모리 전송을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CPU Offload**: 패킷 조립, 체크섬, 흐름 제어, 재전송 로직을 호스트 CPU 대신 RNIC 하드웨어 ASIC 엔진에서 전담 처리하는 기능.
- **Memory Key (lkey / rkey)**: 등록된 메모리 영역(MR)에 대해 로컬 접근 권한(lkey)과 원격 읽기/쓰기 권한(rkey)을 부여하는 보안 암호 키.

</details>

- **커널 우회**: 시스템 호출 없이 RNIC 큐에 WQE 등록
- **제로 카피**: 사용자 버퍼에서 RNIC로 직접 DMA
- **CPU 오프로드**: 캡슐화·재전송을 RNIC가 처리

#### 한줄 요약
- 커널 우회, 제로 카피, CPU 오프로드를 통해 초저지연과 고대역폭을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **QP (Queue Pair) & CQ (Completion Queue)**: 송신 큐(SQ)와 수신 큐(RQ)로 구성된 통신 채널(QP)과 작업 완료 이벤트를 수신하는 완료 큐(CQ).

</details>

```text
[RDMA 정적 구성]
|-- RNIC
|-- 보호 도메인
|-- 메모리 영역
|-- 큐 페어
`-- 완료 큐
```

선의 의미: 양 호스트의 애플리케이션이 커널을 거치지 않고 User Space에서 직접 RNIC를 제어하여 원격 메모리로 DMA 전송을 수행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| RNIC | **주소 변환·DMA 전송** | Hardware Offload |
| 보호 도메인 | **QP·MR 접근 격리** | Protection Domain |
| 메모리 영역 | **Page Pinning·lkey/rkey** | Memory Region |
| 큐 페어 | **WQE·수신 버퍼 관리** | SQ + RQ |
| 완료 큐 | **완료 이벤트 반환** | CQ Polling |

#### 한줄 요약
- RNIC, 보호 도메인(PD), 메모리 영역(MR), 큐 페어(QP), 완료 큐(CQ)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Page Pinning (페이지 고정)**: RDMA 전송 도중 OS가 물리 메모리 페이지를 디스크로 스왑 아웃하지 못하도록 주소 매핑을 물리 RAM에 고정하는 절차.

</details>

```text
애플리케이션 요청
    |
1. 메모리 고정·등록
    |
2. 주소·rkey 교환
    |
3. WQE 포스팅
    |
4. RNIC DMA 전송
    |
5. 원격 메모리 기록
    |
완료 통지
```

- 1. 메모리 고정·등록
- 2. 주소·rkey 교환
- 3. WQE 포스팅
- 4. RNIC DMA 전송
- 5. 원격 메모리 기록

#### 한줄 요약
- 메모리 등록 → rkey 교환 → SQ 작업 포스팅 → RNIC 간 전송 → 원격 메모리 직접 DMA 기록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **InfiniBand vs RoCEv2 vs iWARP**: 전용 하드웨어 패브릭, 무손실 이더넷 UDP 캡슐화, 일반 TCP/IP 지원.

</details>

| 비교 항목 | 인피니밴드 (InfiniBand) | RoCEv2 (RDMA over Converged Ethernet) | iWARP (Internet Wide Area RDMA) |
|:---|:---|:---|:---|
| 물리 전송 매체 | **전용 패브릭** | **무손실 이더넷** | **일반 이더넷** |
| 전송 계층 프로토콜 | **InfiniBand** | **UDP/IP** | **TCP/IP** |
| 지연 시간 | **0.6μs 이하** | **1~2μs** | 5~10μs |
| 네트워크 요건 | 전용 인프라 | **PFC·ECN** | 손실망 지원 |
| 주요 적용 영역 | **HPC·AI 클러스터** | **AI 데이터센터** | WAN 스토리지 |

#### 한줄 요약
- InfiniBand는 최고 성능 전용망, RoCEv2는 이더넷 기반 AI 데이터센터 표준, iWARP는 WAN 호환성에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Completion Polling Loop**: 송신 측이 인터럽트 컨텍스트 스위칭 지연을 피하기 위해 CQ를 무한 루프로 폴링하여 전송 완료를 마이크로초 단위로 감지하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 완료 전 버퍼 덮어쓰기로 데이터 손상 | **CQ 폴링·버퍼 수명주기 동기화** | 데이터 무결성 확보 |
| rkey 유출로 원격 메모리 변조 | **PD·Memory Window** | 비인가 접근 차단 |
| RoCEv2 손실로 재전송 폭주 | **PFC·DCQCN** | 무손실·혼잡 제어 |
| MTT 캐시 미스로 연결 병목 | **SRQ·ODP** | QP 확장성 확보 |

#### 한줄 요약
- CQ 폴링으로 데이터 손상을 방지하고, 보호 도메인으로 메모리를 격리하며, PFC/ECN으로 패킷 손실을 차단한다.

## Ⅶ. 결론

- 최고 성능 전용망은 **InfiniBand**, 이더넷 활용은 **RoCEv2·PFC** 선택

#### 한줄 요약
- **커널 우회·제로 카피**로 CPU 병목 제거
