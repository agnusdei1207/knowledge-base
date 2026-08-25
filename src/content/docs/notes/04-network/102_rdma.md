---
sidebar:
  order: 102
  label: "102. RDMA 원격 직접 메모리 접근"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초저지연 고대역폭 메모리 전송 : RDMA (Remote Direct Memory Access)"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: 호스트 CPU와 커널의 개입을 배제하고 **RNIC 간에 제로 카피와 커널 우회를 통해 원격 메모리에 직접 DMA 전송을 수행하는 초저지연 통신 기술**
- 배경/필요성: 전통적 TCP/IP 소켓 스택의 잦은 시스템 콜 및 메모리 복사로 인한 **CPU 부하 폭증, 마이크로초 단위 지연 누적 및 AI 분산 학습 통신 병목**

#### 한줄 요약
- 커널 우회, 제로 카피, CPU 오프로드를 통해 마이크로초 미만의 초저지연 메모리 전송을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CPU Offload**: 패킷 조립, 체크섬, 흐름 제어, 재전송 로직을 호스트 CPU 대신 RNIC 하드웨어 ASIC 엔진에서 전담 처리하는 기능.
- **Memory Key (lkey / rkey)**: 등록된 메모리 영역(MR)에 대해 로컬 접근 권한(lkey)과 원격 읽기/쓰기 권한(rkey)을 부여하는 보안 암호 키.

</details>

- **커널 우회(Kernel Bypass)**: 유저 공간 애플리케이션이 **OS 시스템 콜 없이 RNIC 하드웨어 큐에 직접 작업 요청(WQE)**
- **제로 카피(Zero-Copy) 전송**: OS 소켓 버퍼를 거치지 않고 **사용자 메모리 버퍼에서 네트워크 하드웨어로 직접 DMA 전송**
- **호스트 CPU 오프로드(Offload)**: 패킷 캡슐화, 재전송, 혼잡 제어를 **RNIC 하드웨어 엔진이 전담하여 CPU 점유율 0% 유지**

#### 한줄 요약
- 커널 우회, 제로 카피, CPU 오프로드를 통해 초저지연과 고대역폭을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **QP (Queue Pair) & CQ (Completion Queue)**: 송신 큐(SQ)와 수신 큐(RQ)로 구성된 통신 채널(QP)과 작업 완료 이벤트를 수신하는 완료 큐(CQ).

</details>

```text
[RDMA 커널 우회 및 메모리 전송 아키텍처]
|-- Host A User Space (송신단: Registered Memory, Queue Pair[SQ/RQ], Completion Queue[CQ])
|   `-- Direct Hardware Ringing (커널 개입 없이 libibverbs 라이브러리로 직접 호출)
`-- Host A RNIC (RDMA-enabled NIC: 가상-물리 주소 변환 MPT, 하드웨어 DMA 컨트롤러)
`-- Network Fabric (InfiniBand Dedicated Fabric / RoCEv2 Lossless Ethernet: RTT $\le 1\mu\text{s}$)
`-- Host B RNIC (수신단: rkey 검증 및 원격 메모리 직접 DMA 쓰기 집행)
`-- Host B User Space (수신단: Registered Memory, CQ 완료 이벤트 폴링)
```

선의 의미: 양 호스트의 애플리케이션이 커널을 거치지 않고 User Space에서 직접 RNIC를 제어하여 원격 메모리로 DMA 전송을 수행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **RNIC (RDMA NIC)** | RDMA 프로토콜 하드웨어 엔진, **가상-물리 주소 변환(MPT) 및 DMA 전송 집행** | Hardware Offload |
| **보호 도메인 (PD)** | 특정 큐 페어(QP)가 접근할 수 있는 **등록 메모리 영역(MR)의 격리 경계 정의** | Protection Domain |
| **메모리 영역 (MR)** | 물리 메모리를 락(Page Pinning)하고 **접근 키(lkey/rkey)를 발급받은 버퍼** | Memory Region |
| **큐 페어 (Queue Pair)**| **송신 작업 요청(WQE)과 수신 버퍼 큐를 관리하는 인터페이스 엔티티** | SQ + RQ |
| **완료 큐 (CQ)** | 전송 완료 이벤트(Work Completion)를 **폴링 또는 인터럽트로 애플리케이션에 반환**| CQ Polling |

#### 한줄 요약
- RNIC, 보호 도메인(PD), 메모리 영역(MR), 큐 페어(QP), 완료 큐(CQ)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Page Pinning (페이지 고정)**: RDMA 전송 도중 OS가 물리 메모리 페이지를 디스크로 스왑 아웃하지 못하도록 주소 매핑을 물리 RAM에 고정하는 절차.

</details>

```text
RDMA 메모리 등록, rkey 교환 및 원격 직접 쓰기 파이프라인
        │
   1. [메모리 고정 및 등록] 송/수신 앱이 통신용 버퍼를 OS에 락(Page Pinning)하고 lkey/rkey 획득
        │
   2. [Out-of-Band 키 교환] TCP 소켓을 통해 수신 측 버퍼의 가상 주소(VA)와 rkey를 송신단에 사전 전달
        │
   3. [Send Queue 작업 포스팅] 송신 앱이 원격 VA, rkey, 크기를 담은 WQE를 Send Queue에 직접 포스팅
        │
   4. [하드웨어 DMA 전송] 송신 RNIC가 DMA로 로컬 메모리를 읽어 캡슐화 후 네트워크 전송
        │
   ▼
5. [원격 메모리 직접 DMA 기록] 수신 RNIC가 rkey 검증 후 원격 CPU 개입 없이 물리 메모리에 직접 쓰기 완료
```

#### 한줄 요약
- 메모리 등록 → rkey 교환 → SQ 작업 포스팅 → RNIC 간 전송 → 원격 메모리 직접 DMA 기록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **InfiniBand vs RoCEv2 vs iWARP**: 전용 하드웨어 패브릭, 무손실 이더넷 UDP 캡슐화, 일반 TCP/IP 지원.

</details>

| 비교 항목 | 인피니밴드 (InfiniBand) | RoCEv2 (RDMA over Converged Ethernet) | iWARP (Internet Wide Area RDMA) |
|:---|:---|:---|:---|
| **물리 전송 매체** | **전용 InfiniBand 케이블 및 스위치** | **표준 이더넷 (Lossless Ethernet 필수)** | **표준 이더넷 (일반 TCP/IP 네트워크)** |
| **전송 계층 프로토콜**| **InfiniBand Native Transport Layer** | **UDP / IP (포트 4791 캡슐화)** | **TCP / IP (RFC 5040 / 5041)** |
| **지연 시간 (RTT)** | **초저지연 ($\le 0.6\mu\text{s}$ 최고 성능)** | **초저지연 ($1\sim 2\mu\text{s}$ 고성능)** | 중간 ($5\sim 10\mu\text{s}$ TCP 오버헤드)|
| **네트워크 요건** | 전용 인프라 구축 필수 (고비용) | **PFC / ECN 기반 무손실 이더넷 필수** | 손실 네트워크에서도 구동 가능 |
| **주요 적용 영역** | **슈퍼컴퓨터, 초대규모 AI 클러스터** | **하이퍼스케일 AI 데이터센터, RoCE 백본**| 광역 WAN 분산 스토리지 연동 |

#### 한줄 요약
- InfiniBand는 최고 성능 전용망, RoCEv2는 이더넷 기반 AI 데이터센터 표준, iWARP는 WAN 호환성에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Completion Polling Loop**: 송신 측이 인터럽트 컨텍스트 스위칭 지연을 피하기 위해 CQ를 무한 루프로 폴링하여 전송 완료를 마이크로초 단위로 감지하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전송 완료(CQE) 확인 전 애플리케이션의 메모리 조기 덮어쓰기로 인한 데이터 손상 | **`CQ (Completion Queue) 폴링 루프 기반 버퍼 수명주기 동기화`** | 메모리 경합 방지 및 전송 데이터 무결성 100% 보장 |
| 유출된 rkey를 악용한 비인가 노드의 원격 호스트 메모리 무단 변조 위협 | **`보호 도메인(PD) 격리 및 단기 동적 메모리 윈도우(Memory Window)`** | 비인가 메모리 침범 원천 차단 및 멀티 테넌트 보안 달성 |
| RoCEv2 환경에서 네트워크 패킷 손실 시 대규모 Go-Back-N 재전송 폭풍 발생 | 스위치 전 포트에 **`PFC (우선순위 흐름 제어) 및 DCQCN 혼잡 제어`** 구성 | 무손실 패킷 포워딩 보장 및 대규모 AI 학습 시 처리율 95% 유지 |
| 대규모 노드 확장 시 RNIC 온칩 캐시 초과로 인한 MTT 캐시 미스 병목 | **`SRQ (Shared Receive Queue) 및 온디맨드 페이징(ODP)`** 적용 | RNIC 메모리 사용량 절감 및 수만 개 QP 연결 확장 수용 |

#### 한줄 요약
- CQ 폴링으로 데이터 손상을 방지하고, 보호 도메인으로 메모리를 격리하며, PFC/ECN으로 패킷 손실을 차단한다.

## Ⅶ. 결론

- 대규모 LLM 인공지능 분산 학습 및 초고속 분산 스토리지(NVMe-oF)의 통신 병목을 제거하기 위해 **RDMA 아키텍처를 차세대 데이터센터 네트워킹 표준으로 채택**하되, 실무 구축 시 **RoCEv2 및 InfiniBand 패브릭 최적화, PFC/ECN 기반 무손실 네트워크 환경 보장, 정밀한 메모리 키(rkey) 수명주기 관리**를 통합 구현하여 테라비트급 고효율 데이터 전송 완성

#### 한줄 요약
- RDMA는 커널 우회와 제로 카피 및 CPU 오프로드를 통해 AI 데이터센터의 초저지연 고대역폭 메모리 전송을 실현하는 핵심 통신 기술이다.