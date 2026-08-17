---
sidebar:
  order: 48
  label: "048. InfiniBand (InfiniBand)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "InfiniBand (InfiniBand)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 48
extra:
  question_no: "048"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "RDMA•집단 통신의 단일 기출 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **InfiniBand**: HPC 및 AI 데이터센터에서 서버 간 초고대역폭(수백 Gbps)과 마이크로초(Sub-$\mu$s) 미만의 초저지연을 제공하는 무손실 패브릭 통신 규격.
- **RDMA(Remote Direct Memory Access)**: CPU와 OS 개입 없이 로컬 호스트 메모리에서 원격 호스트 메모리로 데이터를 직접 읽고 쓰는 기술.
- **Kernel Bypass(커널 우회)**: 네트워크 I/O 시 OS 커널의 TCP/IP 스택을 거치지 않고 사용자 공간 앱이 직접 HCA 하드웨어와 통신하는 기법.

</details>

- 정의/개념: HCA(Host Channel Adapter), 전용 스위치 패브릭 및 RDMA 기술을 결합하여, CPU 및 OS 커널 개입 없이 마이크로초(Sub-$\mu$s) 단위 초저지연과 무손실(Lossless) 전송을 보장하는 고성능 컴퓨팅(HPC) 및 AI 클러스터 전용 고속 네트워킹 아키텍처
- 배경/필요성: 기존 소켓 기반 TCP/IP 네트워크의 과도한 메모리 복사(Copy Overhead), 커널 문맥 전환 지연 및 **CPU 점유율 급증을 해소하고 수만 개 GPU 간 초대용량 텐서 동기화 지원**

#### 한줄 요약

- **RDMA와 커널 우회(Kernel Bypass)**로 CPU 부하 없는 초저지연 무손실 패브릭 실현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Memory Registration**: RDMA 통신에 사용할 메모리 페이지를 물리 메모리에 잠금(Pinning)하고 가상-물리 주소 변환 키(L_Key, R_Key)를 생성하는 절차.
- **Credit-Based Flow Control**: 수신 버퍼 여유 공간(크레딧)을 송신 측에 미리 통지하여 패킷 드롭(Drop)과 재전송을 원천 방지하는 링크 계층 무손실 제어.

</details>

- 사용자 공간에서 OS 커널을 거치지 않고 직접 HCA를 제어하는 **커널 우회(Kernel Bypass)** 및 **Zero-Copy** 전송
- 수신 버퍼 오버플로우로 인한 패킷 폐기를 원천 차단하는 하드웨어 **크레딧 기반 무손실 흐름 제어(Credit-based Flow Control)**
- HPC 및 대규모 AI 분산 학습의 병목인 All-Reduce 집단 통신을 지원하는 **SHARP 인네트워크 연산** 통합

#### 한줄 요약

- **Memory Registration 기반 Zero-Copy·Credit 기반 무손실 흐름 제어·HPC/AI 집단 통신 가속**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Queue Pair(QP)**: 송신 큐(Send Queue, SQ)와 수신 큐(Receive Queue, RQ)로 구성된 RDMA 기본 통신 엔드포인트.
- **Completion Queue(CQ)**: 전송 작업 완료 이벤트(Work Completion)를 비동기로 수신하는 큐.
- **Subnet Manager(SM)**: 인피니밴드 패브릭 전체의 토폴로지를 탐색하고 노드에 LID(Local Identifier) 주소 및 라우팅 경로를 할당하는 관리 엔티티.

</details>

```text
[ InfiniBand 무손실 패브릭 및 RDMA 아키텍처 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ 노드 1 (User Space App)      │        │ 노드 2 (User Space App)      │
│  ├─ 등록 메모리 (Pinned)     │        │  ├─ 등록 메모리 (Pinned)     │
│  └─ QP (Send/Receive Queue)  │        │  └─ QP (Send/Receive Queue)  │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │ (Kernel Bypass)                       │ (Kernel Bypass)
┌──────────────┴───────────────┐        ┌──────────────┴───────────────┐
│ HCA (Host Channel Adapter)   │        │ HCA (Host Channel Adapter)   │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │ (InfiniBand Link)                     │ (InfiniBand Link)
═══════════════╧═══════════════════════════════════════╧════════════════ (무손실 스위치 패브릭)
               │
┌──────────────┴───────────────┐
│ 서브넷 관리자 (Subnet Manager)│
└──────────────────────────────┘
```

선의 의미: 분산 노드의 QP/CQ 큐잉, HCA 어댑터, InfiniBand 스위치 패브릭 및 서브넷 관리자(SM) 간의 패브릭 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 채널 어댑터 및 큐 쌍, 완료 큐 종단점 | 응용 프로그램의 **원격 직접 메모리 접근** 명령을 가로채어, 하드웨어 전용 칩으로 직접 펌핑 전송하고 **완료 큐**에 영수증을 꽂아주는 말단 노가다 반장 |
| 인피니밴드 거대 스위치 패브릭 망 | 패킷이 바닥에 떨어지지 않는 100% 무손실 핑퐁을 보장하는 **크레딧 기반 흐름 제어** 및 수천 개 포트의 미친 크로스바 스위칭 책임 |
| 소프트웨어 서브넷 관리자 | 얽히고설킨 수만 가닥의 광케이블 망 지형을 파악하고, 각 노드에 논리적 주소(LID)를 할당하며 차단 없는 최적의 경로를 뚫는 교통경찰 |

#### 한줄 요약

- **HCA 어댑터·Queue Pair(QP) & CQ·InfiniBand 스위치 패브릭·Subnet Manager(SM)**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RDMA Write**: 송신 측이 원격 노드의 가상 메모리 주소와 R_Key를 명시하여 원격 CPU의 개입 없이 원격 메모리에 데이터를 직접 기록하는 원격 단방향 연산.

</details>

```text
[ InfiniBand RDMA Write 전송 시퀀스 ]
                         │
                         ▼
   [ 1. 앱이 송신 SQ에 RDMA Write 작업 요청(WR) 등록 ]
                         │
                         ▼
   [ 2. 송신 HCA가 로컬 DMA로 등록 버퍼 데이터 직접 인출 ]
                         │
                         ▼
   [ 3. 크레딧 검증 후 InfiniBand 패브릭으로 패킷 전송 ]
                         │
                         ▼
   [ 4. 수신 HCA가 R_Key 권한 검증 및 원격 메모리에 직접 쓰기 ]
                         │
                         ▼
   [ 5. 양측 CQ(Completion Queue)에 완료 통지 및 세션 종료 ]
```

**동작 원리**

1. **WR 제출**: 사용자 애플리케이션이 원격 가상 주소와 R_Key가 포함된 Work Request를 SQ에 푸시
2. **로컬 DMA**: 송신 HCA가 CPU 개입 없이 로컬 등록 메모리에서 DMA로 페이로드 인출
3. **패브릭 전송**: 수신 측 크레딧을 확인하고 무손실 스위치 패브릭을 통해 패킷 전송
4. **원격 메모리 쓰기**: 수신 HCA가 R_Key 유효성을 검증하고 수신 측 등록 메모리에 DMA 직접 쓰기
5. **완료 통보**: 전송 완료 이벤트를 CQ에 기록하여 애플리케이션에 비동기 완료 알림

#### 한줄 요약

- Work Request $\to$ **송신 HCA 로컬 DMA 인출 $\to$ rkey 보안 검증 $\to$ 원격 메모리 직접 쓰기 $\to$ CQ 영수증 통보**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **InfiniBand vs RoCEv2 vs TCP/IP**:
  - InfiniBand: 네이티브 하드웨어 패브릭, 완전 무손실 크레딧 제어, 최고 성능 (HPC/AI)
  - RoCEv2: 이더넷 UDP/IP 캡슐화, PFC/ECN 기반 무손실 구현, 가성비
  - TCP/IP: 표준 소켓 스택, 커널 복사 및 문맥 전환 오버헤드, 범용 웹/DB

</details>

| 비교 항목 | InfiniBand (네이티브 패브릭) | RoCEv2 (이더넷 위 RDMA) | TCP/IP (표준 이더넷) |
|:---|:---|:---|:---|
| 네트워크 계층 및 전송 | 네이티브 하드웨어 패브릭 (무손실 크레딧 제어) | Converged 이더넷 (UDP/IP 캡슐화 + PFC/ECN) | 표준 이더넷 (TCP 소켓 + 커널 스택) |
| 지연시간 및 CPU 부하 | 마이크로초 미만(Sub-$\mu$s), CPU 부하 0% (Zero-Copy) | 초저지연(수 $\mu$s), CPU 부하 0% (Zero-Copy) | 밀리초 단위(수십 $\mu$s~ms), 높은 CPU 부하 |
| 한계 및 구축 비용 | 전용 HCA/스위치 고비용, NVIDIA 단일 벤더 종속 | 스위치 PFC/ECN 복잡한 튜닝 및 Pause Frame 혼잡 | 대규모 분산 AI 학습 시 심각한 통신 병목 |

#### 한줄 요약

- 최고 성능 HPC/AI는 **InfiniBand**, 기존 이더넷 활용은 **RoCEv2**, 범용 통신은 **TCP/IP**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **GPUDirect RDMA**: 시스템 메인 메모리(Host RAM)를 거치지 않고 PCIe 버스를 통해 GPU VRAM에서 HCA로 데이터를 직접 고속 전송하는 기술.
- **Adaptive Routing(적응형 라우팅)**: 고정된 단일 경로 대신 실시간 패브릭 혼잡도를 감지하여 유휴 링크로 패킷을 동적 분산 전송하는 스위칭 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 허공에 노출된 낡은 **등록 키**를 악용한 해커의 원격 서버 램 무단 침범 및 인공지능 텐서 데이터 탈취 보안 참사 위험 | RDMA 전송 작업 완료 직후 얄짤없는 즉각적 **키 폐기** 및 할당된 메모리 영역 강제 락업(Pinning) 해제 조치 시스템화 | 승인되지 않은 비인가 메모리 경계 오염 및 세그먼트 오류(Segfault) 크래시 원천 방지 및 데이터 보안망 구축 |
| 광케이블 순간 패킷 에러 또는 스위치 재부팅에 의한 **큐 쌍 오류 상태** 강제 전환 및 클러스터 전체 통신 세션 연쇄 마비 현상 | 하드웨어 수준의 에러 복구 핸들러 펌웨어 구축 및 인공지능 학습이 멈추지 않게 자동 큐 쌍 리셋 재연결 알고리즘 떡칠 탑재 | 찰나의 네트워크 단절이나 펄스 에러에도 학습 훈련 세션이 날아가지 않는 시스템 가용성 100% 방어 확보 |
| 특정 스위치 링크로 트래픽이 미친 듯이 쏠려 패킷이 버려지고 클러스터 전체가 버벅대는 극심한 네트워크 병목 혼잡 붕괴 | 트래픽 핫스폿을 요리조리 피하는 스위치 하드웨어 적응형 라우팅 및 런타임 동적 다중 경로 부하 분산 강제 적용 | 특정 노드 연결선의 혼잡 붕괴(Congestion Collapse) 현상 원천 방지 및 전체 초거대 클러스터 대역폭 균등화 수호 |
| 가속기(GPU) 데이터가 굳이 호스트 시스템 메모리(RAM)를 거쳐가야 하는 굴욕적인 데이터 핑퐁 복사 지연 오버헤드 병목 | **지피유 직접 원격 메모리 접근** 기술을 켜서 중앙 처리 장치를 기절시키고 그래픽 램과 네트워크 랜카드 직결 펌핑 야바위 구현 | 중앙 처리 장치 낭비를 막고, 서버 간 그래픽 카드 칩 간 통신 지연시간(Latency)을 마이크로초 단위의 0에 가깝게 극한 최소화 달성 |

#### 한줄 요약

- **Key Revocation 보안 관리·QP 에러 핸들러 자동 재연결·적응형 라우팅·GPUDirect RDMA**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **InfiniBand XDR (800Gbps)**: 차세대 슈퍼컴퓨팅 패브릭으로, 포트당 800Gbps 대역폭과 액체 냉각(Direct Liquid Cooling)을 결합하여 초대규모 LLM 클러스터 지원.

</details>

- 초대규모 AI 슈퍼컴퓨터 및 LLM 클러스터에서 **InfiniBand NDR(400Gbps) / XDR(800Gbps) 패브릭 및 GPUDirect RDMA 표준 채택**

#### 한줄 요약

- **초저지연 무손실 보장(InfiniBand)과 기존 인프라 가성비(RoCEv2)** 간의 인프라 전략 선정
