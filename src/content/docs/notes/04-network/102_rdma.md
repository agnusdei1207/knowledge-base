---
sidebar:
  order: 102
  label: "102. RDMA 원격 직접 메모리 접근 (RDMA)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초저지연 고대역폭 메모리 전송 : RDMA (Remote Direct Memory Access)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
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

- **원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: 원격 호스트의 운영체제(커널)와 CPU 개입 없이, 로컬 네트워크 카드(RNIC)가 원격 호스트의 등록된 물리 메모리 주소 공간으로 직접 데이터를 읽거나(Read) 쓰는(Write) 하드웨어 가속 전송 기술.
- **커널 우회(Kernel Bypass) 및 제로 카피(Zero-Copy)**: 데이터 송수신 시 운영체제 시스템 호출(System Call)과 컨텍스트 스위칭을 제거하고(Kernel Bypass), 사용자 메모리에서 소켓 버퍼를 거치지 않고 NIC 하드웨어 버퍼로 DMA 직결 전송하는 방식(Zero-Copy).

</details>

- 정의/개념: 호스트 CPU와 운영체제 커널의 개입을 배제하고 **RNIC(RDMA-enabled NIC)** 간에 **제로 카피(Zero-Copy)** 및 **커널 우회(Kernel Bypass)** 를 통해 마이크로초($\mu\text{s}$) 미만의 초저지연과 테라비트급 고대역폭 메모리 전송을 실현하는 **고성능 분산 컴퓨팅 통신 아키텍처**
- 배경/필요성: 대규모 분산 AI LLM 학습(All-Reduce) 및 HPC 클러스터에서 전통적인 TCP/IP 스택의 반복적 메모리 복사($\text{User} \leftrightarrow \text{Kernel}$)와 과도한 CPU 점유율(CPU Overhead) 병목을 해소할 요구

#### 한줄 요약
- 커널 우회와 제로 카피를 통해 원격 호스트 메모리에 직접 데이터를 읽고 쓰는 초저지연 전송 기술이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **원격 메모리 키(Remote Key, rkey)**: 송신 측 RNIC가 원격 호스트의 특정 가상 메모리 영역에 접근할 수 있는 물리 주소 매핑 및 읽기/쓰기 인가 권한을 증명하는 암호학적 토큰.
- **단방향 동작(One-Sided Operations)**: 원격 CPU의 수신 인터럽트나 애플리케이션 호출 없이 송신 측이 직접 원격 메모리를 수정하는 RDMA Read / RDMA Write 연산.

</details>

- **CPU 오프로드(CPU Offloading)**: 패킷 생성, 세그멘테이션, 확인 응답, 흐름 제어 로직을 전적으로 RNIC 하드웨어가 전담 처리하여 호스트 CPU 사용률 0%에 근접
- **초저지연 결정론적 전송**: 소켓 계층 버퍼링 지연을 제거하여 노드 간 왕복 지연 시간(RTT)을 $1\sim 2\mu\text{s}$ 수준으로 극소화
- **단방향(One-Sided) 및 양방향(Two-Sided) 통신 지원**: 원격 CPU를 전혀 깨우지 않는 단방향(Read/Write)과 메시지 동기화용 양방향(Send/Receive) 선택 제공

#### 한줄 요약
- 제로 카피, 커널 우회, CPU 오프로드, 단방향 원격 메모리 직접 읽기/쓰기를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **큐 페어(Queue Pair, QP)**: 애플리케이션이 RNIC에 전송 명령을 하달하는 송신 큐(Send Queue, SQ)와 수신 버퍼를 등록하는 수신 큐(Receive Queue, RQ)의 쌍.
- **완료 큐(Completion Queue, CQ)**: RNIC가 전송 또는 수신 작업을 완료했을 때 작업 완료 요소(Work Completion, WC)를 적재하여 애플리케이션에 통지하는 큐.

</details>

```text
[ 송신 호스트 (Host A User Space) ]                      [ 수신 호스트 (Host B User Space) ]
 ├─ 사용자 버퍼 (Registered Memory)                       ├─ 사용자 버퍼 (Registered Memory)
 ├─ 큐 페어 (QP: Send Queue / Receive Queue)               ├─ 큐 페어 (QP: SQ / RQ)
 └─ 완료 큐 (Completion Queue: CQ)                        └─ 완료 큐 (Completion Queue: CQ)
         │ (커널 우회: User Space에서 직접 접근)                   │ (커널 우회)
         ▼                                                         ▼
┌────────────────────────────────┐                        ┌────────────────────────────────┐
│ [ 송신 측 RNIC (RDMA NIC) ]    │ ══════════════════════ │ [ 수신 측 RNIC (RDMA NIC) ]    │
│  ├─ 메모리 변환 엔진 (VA ➔ PA) │   (InfiniBand / RoCE)   │  ├─ rkey / lkey 권한 검증      │
│  └─ 하드웨어 DMA 컨트롤러      │ ══════════════════════ │  └─ 원격 메모리 직접 DMA 기록  │
└────────────────────────────────┘                        └────────────────────────────────┘
```

선의 의미: 양 호스트의 애플리케이션이 커널을 거치지 않고 User Space에서 직접 RNIC를 제어하여 원격 메모리로 DMA 전송을 수행하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **RNIC (RDMA NIC)** | RDMA 프로토콜 하드웨어 엔진, 가상-물리 주소 변환(MPT) 및 DMA 전송 집행 | Hardware Offload |
| **보호 도메인 (PD)** | 특정 큐 페어(QP)가 접근할 수 있는 등록 메모리 영역(MR)의 격리 경계 정의 | Protection Domain |
| **메모리 영역 (MR)** | 물리 메모리를 락(Page Pinning)하고 접근 키(lkey/rkey)를 발급받은 버퍼 | Memory Region |
| **큐 페어 (Queue Pair)** | 송신 작업 요청(WQE)과 수신 버퍼 큐를 관리하는 인터페이스 엔티티 | SQ + RQ |
| **완료 큐 (CQ)** | 전송 완료 이벤트(Work Completion)를 폴링 또는 인터럽트로 애플리케이션에 반환 | CQ Polling |

#### 한줄 요약
- RNIC, 보호 도메인(PD), 메모리 영역(MR), 큐 페어(QP), 완료 큐(CQ)가 결합하여 커널 우회 전송을 수행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **페이지 고정(Page Pinning)**: RDMA 전송 중 OS가 해당 물리 메모리 페이지를 디스크로 스왑 아웃(Paging)하지 못하도록 가상-물리 주소 매핑을 메모리에 영구 고정하는 작업.

</details>

```text
1. 송/수신 애플리케이션이 통신용 버퍼를 OS에 등록(Page Pinning)하고 lkey 및 rkey 획득
            │
            ▼
2. 대역 외(Out-of-Band) TCP/IP 소켓을 통해 수신 측 버퍼의 가상 주소(VA)와 rkey를 송신 측으로 사전 교환
            │
            ▼
3. 송신 애플리케이션이 원격 VA, rkey, 데이터 크기를 지정한 WQE(작업 요청)를 Send Queue에 직접 포스팅
            │
            ▼
4. 송신 RNIC가 DMA로 로컬 메모리를 읽어 패킷 캡슐화 후 네트워크 전송 ➔ 수신 RNIC 수신
            │
            ▼
5. 수신 RNIC가 rkey 유효성을 하드웨어 검증하고 원격 CPU 개입 없이 대상 물리 메모리에 직접 DMA 기록
            │
            ▼
6. 송신/수신 RNIC가 각각의 완료 큐(CQ)에 Work Completion 이벤트를 인입하여 작업 종료 통지
```

**동작 원리**

1. **메모리 등록(MR)**: 사용자 버퍼를 물리 메모리에 고정하고 RNIC 주소 변환 테이블(MTT)에 등록
2. **연결 및 키 교환**: QP 번호와 rkey를 상호 교환하여 보안 채널(RC: Reliable Connected) 수립
3. **작업 요청(WQE)**: 커널 시스템 호출 없이 유저 레벨 라이브러리(libibverbs)로 하드웨어 큐 직접 호출
4. **직접 DMA 전송**: RNIC가 패킷 전송 및 흐름 제어(Go-Back-N / Selective ACK)를 자체 처리
5. **원격 직접 쓰기**: 수신 호스트 CPU의 컨텍스트 스위칭 없이 타겟 물리 주소에 바이트 단위 복사

#### 한줄 요약
- 메모리 등록, rkey 교환, SQ 작업 포스팅, RNIC 간 전송, 원격 메모리 직접 DMA 기록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전송 계층 구현체 비교**: 전용 하드웨어 패브릭을 사용하는 InfiniBand, 이더넷 상에서 UDP 캡슐화를 사용하는 RoCEv2, 표준 TCP/IP 상에서 구동되는 iWARP의 비교.

</details>

| 비교 항목 | 인피니밴드 (InfiniBand) | RoCEv2 (RDMA over Converged Ethernet) | iWARP (Internet Wide Area RDMA) |
|:---|:---|:---|:---|
| **물리 전송 매체** | **전용 InfiniBand 케이블 및 스위치** | **표준 이더넷 (Lossless Ethernet 필수)** | **표준 이더넷 (일반 TCP/IP 네트워크)** |
| **전송 계층 프로토콜**| **InfiniBand Native Transport Layer** | **UDP / IP (포트 4791 캡슐화)** | **TCP / IP (RFC 5040 / 5041)** |
| **지연 시간 (RTT)** | **초저지연 ($\le 0.6\mu\text{s}$ 최고 성능)** | **초저지연 ($1\sim 2\mu\text{s}$ 고성능)** | 중간 ($5\sim 10\mu\text{s}$ TCP 오버헤드)|
| **네트워크 요건** | 전용 인프라 구축 필수 (고비용) | **PFC / ECN 기반 무손실 이더넷 필수** | 손실 네트워크에서도 구동 가능 |
| **주요 적용 영역** | 슈퍼컴퓨터, AI 초대규모 클러스터 | **하이퍼스케일 AI 데이터센터, RoCE 백본**| 광역 WAN 분산 스토리지 연동 |

#### 한줄 요약
- InfiniBand는 최고 성능 전용망, RoCEv2는 이더넷 기반 AI 데이터센터 표준, iWARP는 WAN 호환성에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **조기 버퍼 재사용(Premature Buffer Reuse)**: 송신 애플리케이션이 RNIC의 전송 완료(CQ 확인)를 기다리지 않고 버퍼 데이터를 덮어써서 전송 데이터가 훼손되는 동기화 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전송 완료(CQE) 확인 전 애플리케이션의 메모리 조기 덮어쓰기로 인한 데이터 손상 | **CQ(Completion Queue) 폴링 루프 기반 버퍼 수명주기 동기화** 강제 | 메모리 경합 방지 및 전송 데이터 무결성 100% 보장 |
| 유출된 rkey를 악용한 비인가 노드의 원격 호스트 메모리 무단 변조 위협 | **보호 도메인(PD) 기반 메모리 격리 및 작업별 단기 동적 키(Memory Window)** 적용 | 비인가 메모리 침범 원천 차단 및 멀티 테넌트 보안 격리 달성 |
| RoCEv2 환경에서 네트워크 패킷 손실 시 대규모 Go-Back-N 재전송 폭풍 발생 | 스위치 전 포트에 **PFC(우선순위 흐름 제어) 및 DCQCN(혼잡 제어)** 구성 | 무손실 패킷 포워딩 보장 및 대규모 AI 학습 시 통신 처리율 95% 유지 |

#### 한줄 요약
- CQ 폴링으로 데이터 손상을 방지하고, 보호 도메인으로 메모리를 격리하며, PFC/ECN으로 패킷 손실을 차단한다.

## Ⅶ. 결론

- 대규모 LLM 인공지능 분산 학습 및 초고속 분산 스토리지(NVMe-oF)의 통신 병목을 제거하기 위해 **RDMA 아키텍처**는 데이터센터 네트워킹의 핵심 기반 기술로 확립되었으며, 실무 구축 시 **RoCEv2 및 InfiniBand 패브릭 최적화**, **PFC/ECN 기반 무손실 네트워크 환경 보장**, **정밀한 메모리 키(rkey) 수명주기 관리**를 통합 구현하여 테라비트급 고효율 데이터 전송을 완성

#### 한줄 요약
- RDMA의 커널 우회와 제로 카피를 무손실 이더넷 및 InfiniBand와 결합하여 고성능 AI 분산 통신을 실현한다.
