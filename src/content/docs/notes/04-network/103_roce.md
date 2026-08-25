---
sidebar:
  order: 103
  label: "103. RoCE — RDMA over Converged Ethernet"
  badge:
    text: "미출 · 50%"
    variant: note
title: "이더넷 기반 무손실 고속 전송 : RoCE 및 RoCEv2"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 103
extra:
  question_no: "103"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "RoCEv1(L2) vs RoCEv2(L3 UDP 4791), 무손실 이더넷(PFC/IEEE 802.1Qbb), ECN/DCQCN 혼잡 제어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RoCE (RDMA over Converged Ethernet)**: 범용 이더넷 상에서 InfiniBand 전송 계층 패킷을 캡슐화하여 RDMA를 제공하는 기술 (IBTA 표준).
- **RoCEv2 (Routable RoCE)**: IP 및 UDP 헤더(포트 4791)로 패킷을 캡슐화하여 대규모 L3 패브릭 라우팅을 지원하는 차세대 표준.

</details>

- 정의/개념: 범용 이더넷 상에서 **InfiniBand 패킷을 UDP/IP(포트 4791)로 캡슐화하고 무손실 패브릭(PFC/ECN)과 결합하여 L3 라우팅을 지원하는 RDMA 기술**
- 배경/필요성: 전용 InfiniBand 인프라의 **천문학적 구축 비용 발생, 기존 데이터센터 이더넷 스위치와의 비호환성 및 대규모 L3 확장 한계**

#### 한줄 요약
- 범용 이더넷 상에서 무손실 흐름 제어와 UDP 캡슐화를 통해 L3 확장형 초저지연 RDMA를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lossless Ethernet (무손실 이더넷)**: 패킷 드롭이 발생하면 성능이 급락하는 RDMA를 위해 L2 PFC와 L3 ECN으로 버퍼 오버플로우를 원천 방지하는 네트워크.
- **DCQCN (Data Center QCN)**: 스위치의 ECN 마킹과 수신단의 CNP 알림을 기반으로 송신단 전송률을 동적 조절하는 혼잡 제어 알고리즘.

</details>

- **L3 라우팅 지원(RoCEv2)**: UDP 목적지 포트 4791 캡슐화를 통해 **데이터센터 리프-스파인 L3 패브릭 완벽 수용**
- **무손실 패브릭(Lossless Fabric) 보장**: IEEE 802.1Qbb PFC를 통해 **스위치 버퍼 고갈 시 패킷 드롭 제로 달성**
- **하드웨어 가속 혼잡 제어(DCQCN)**: ECN 마킹과 CNP 역방향 알림을 통해 **스위치 큐 버퍼 폭발을 선제적으로 완화**

#### 한줄 요약
- L3 라우팅 지원, PFC 무손실 보장, DCQCN 하드웨어 혼잡 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **PFC vs ECN**: 버퍼 고갈 시 L2 PAUSE 프레임으로 송신을 일시 중단시키는 하드웨어 차단(PFC)과 버퍼 임계치 초과 시 IP 헤더 비트를 마킹하는 선제 제어(ECN).

</details>

```text
[RoCEv2 무손실 이더넷 및 DCQCN 제어 토폴로지]
|-- Host A (GPU/RNIC: RoCEv2 UDP 4791 패킷 라인레이트 송출)
`-- Leaf-Spine Lossless Ethernet Fabric
|   |-- L2: PFC (IEEE 802.1Qbb: 버퍼 위험 시 상류 포트로 PAUSE 송출)
|   |-- L3: WRED / ECN (RFC 3168: 버퍼 경고 임계치 도달 시 ECN 비트 '11' 마킹)
|   `-- ECMP: UDP Source Port 엔트로피 해시 기반 다중 스파인 부하 분산
`-- Host B (GPU/RNIC: ECN 감지 시 50us 주기로 CNP 역방향 피드백 송출)
`-- Host A DCQCN Rate Controller (CNP 수신 시 전송 속도 즉각 감속 및 점진 회복)
```

선의 의미: RoCEv2 데이터 패킷이 스위치 패브릭에서 ECN 마킹을 거쳐 수신단에 도착하고 수신 RNIC가 생성한 CNP 피드백을 통해 송신단이 레이트를 조절하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **RoCEv2 RNIC** | UDP 4791 캡슐화, **DMA 메모리 읽기/쓰기, DCQCN 레이트 제어기 구동** | Mellanox ConnectX |
| **PFC 제어기 (L2)** | 스위치 입력 버퍼 고갈 시 **송신 포트에 802.1Qbb PAUSE를 전송하여 드롭 방지** | Lossless Queue |
| **ECN 마킹 엔진 (L3)**| 출력 큐 임계치 초과 시 **패킷 폐기 대신 IP 헤더 ECN 비트('11') 마킹** | RFC 3168 ECN |
| **CNP 생성기** | 수신 패킷의 ECN 마킹을 감지하여 **발신지로 $50\mu\text{s}$ 주기 CNP 패킷 회신** | Congestion Signal |
| **ECMP 패브릭** | UDP 출발지 포트 엔트로피 해시를 기반으로 **다중 스파인 경로 균등 분산** | Load Balancing |

#### 한줄 요약
- RoCEv2 RNIC, PFC 무손실 큐, ECN 스위치 마킹, CNP 피드백 루프, ECMP 분산 패브릭이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CNP (Congestion Notification Packet)**: 수신 호스트 RNIC가 ECN 마킹을 감지했을 때 송신 호스트를 향해 전송 속도를 줄이라고 역방향으로 보내는 경보 패킷.

</details>

```text
RoCEv2 전송, ECN 마킹, CNP 피드백 및 DCQCN 감속 파이프라인
        │
   1. [RoCEv2 패킷 송출] 송신 호스트가 GPU 데이터를 UDP 4791로 캡슐화하여 패브릭으로 송출
        │
   2. [스위치 ECN 선제 마킹] 스위치 버퍼가 경고 임계치에 도달 시 IP 헤더 ECN 필드를 '11'(CE)로 마킹
        │
   3. [수신단 CNP 역전송] 수신 호스트 RNIC가 CE 마킹을 감지하고 송신단으로 CNP 패킷 즉시 회신
        │
   4. [DCQCN 전송률 감속] 송신 RNIC가 CNP를 수신하여 해당 QP의 전송 속도를 즉각 감속
        │
   ▼
5. [PFC 최후 방어선] 버퍼가 위험 임계치에 도달할 경우 L2 PFC PAUSE가 발동하여 0ms 무손실 방어
```

#### 한줄 요약
- RoCEv2 송출 → ECN 스위치 마킹 → CNP 역방향 통지 → DCQCN 감속 → PFC 무손실 방어 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RoCEv1 (L2)** vs **RoCEv2 (L3 UDP/IP)** vs **Native InfiniBand**.

</details>

| 비교 항목 | RoCEv1 (IB over L2 Ethernet) | RoCEv2 (IB over UDP/IP) | 네이티브 인피니밴드 (InfiniBand) |
|:---|:---|:---|:---|
| **캡슐화 계층** | **L2 이더넷 (EtherType: 0x8915)** | **L3/L4 UDP/IP (UDP Port: 4791)** | **InfiniBand Native Frame** |
| **L3 라우팅 지원** | **불가 (단일 L2 서브넷에 국한)** | **완벽 지원 (IP 기반 L3 패브릭 라우팅)**| InfiniBand 서브넷 라우터 필요 |
| **혼잡 제어 방식** | PFC (L2 Flow Control) 단독 의존 | **ECN + CNP + DCQCN + PFC 결합** | **신용 기반 흐름 제어 (Credit-Based)**|
| **초기 구축 비용** | 저렴 (표준 L2 스위치) | **저렴 (표준 L3 데이터센터 스위치)** | **매우 높음 (전용 케이블 및 스위치)** |
| **주요 적용 영역** | 소규모 클러스터, 단일 랙 스토리지 | **초대규모 AI 데이터센터 (GPU 백본)** | 국가 슈퍼컴퓨터, 초고성능 HPC |

#### 한줄 요약
- RoCEv1은 소규모 L2 단일 랙용, RoCEv2는 초대규모 AI 클러스터 표준, InfiniBand는 최고 성능 전용망이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PFC Deadlock**: 링 토폴로지나 버퍼 순환 구조에서 스위치들이 서로를 향해 PAUSE 프레임을 영구 전송하여 트래픽이 완전 마비되는 교착 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스위치 간 PFC PAUSE 전파로 인한 패브릭 전체의 **PFC 데드락 및 HoL 블로킹** | **`PFC 데드락 워치독(Deadlock Watchdog)` 및 ECN 임계치 사전 튜닝** | PFC 발동 빈도 90% 감소 및 데드락 시 큐 드레인 복구 |
| 다중 GPU의 동시 전송 시 버퍼 폭발로 인한 **인캐스트(Incast) 패킷 손실** | **`스위치 WRED ECN 조기 마킹 및 송신단 DCQCN 정밀 튜닝`** | 버퍼 오버플로우 방지 및 무손실 처리율 98% 유지 |
| ECMP 라우팅 시 동일 플로우가 특정 링크로 쏠려 발생하는 **핫스팟(Hotspot)** | RoCEv2 UDP Source Port에 **`5-Tuple 엔트로피 해싱(Entropy Hashing)`** | 리프-스파인 다중 경로 간 완벽한 로드밸런싱 달성 |
| 네트워크 패킷 1개 손실 시 Go-Back-N 재전송으로 인한 대역폭 급감 | **`선택적 재전송(Selective Repeat / Out-of-Order)` 지원 RNIC** 도입 | 패킷 손실 시 재전송 오버헤드 극소화 |

#### 한줄 요약
- ECN/PFC 튜닝으로 데드락을 방지하고, DCQCN으로 인캐스트를 해소하며, 엔트로피 해싱으로 ECMP 부하를 분산한다.

## Ⅶ. 결론

- 하이퍼스케일 AI 데이터센터에서 GPU 간 통신 병목을 해소하고 비용 효율적인 고성능 네트워크를 구축하기 위해 **RoCEv2 기반의 무손실 이더넷 아키텍처를 핵심 표준으로 도입**하되, 인프라의 안정성을 극대화하기 위해 **PFC/ECN 듀얼 혼잡 제어 파라미터 최적화, PFC 데드락 워치독, 엔트로피 해시 기반 ECMP 로드밸런싱**을 통합 적용하여 고성능 AI 패브릭 완성

#### 한줄 요약
- RoCEv2는 범용 이더넷 상에서 무손실 흐름 제어와 L3 라우팅을 지원하여 대규모 AI 분산 학습의 통신 병목을 해소하는 핵심 기술이다.