---
sidebar:
  order: 103
  label: "103. RoCE — RDMA over Converged Ethernet (RoCE)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "이더넷 기반 무손실 고속 전송 : RoCE 및 RoCEv2 (RDMA over Converged Ethernet)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
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

- **RoCE(RDMA over Converged Ethernet)**: 값비싼 InfiniBand 전용 케이블과 스위치 대신, 범용 데이터센터 이더넷(Ethernet) 인프라 상에서 InfiniBand 전송 계층 패킷을 캡슐화하여 RDMA 서비스를 제공하는 표준 기술 (IBTA 표준).
- **RoCEv2(Routable RoCE / InfiniBand over UDP)**: L2 브로드캐스트 도메인에 국한되던 RoCEv1의 한계를 극복하기 위해, IP 및 UDP 헤더(목적지 포트 4791)로 InfiniBand 패킷을 캡슐화하여 L3 라우팅을 지원하는 차세대 표준.

</details>

- 정의/개념: 이더넷 인프라 상에서 **무손실 패브릭(Lossless Fabric: PFC, ECN)** 과 **UDP/IP 캡슐화(RoCEv2)** 를 결합하여, 커널 우회 및 제로 카피 기반의 초저지연·고대역폭 전송을 L3 라우팅 규모로 확장한 **데이터센터 AI 네트워크 아키텍처**
- 배경/필요성: 수만 개의 GPU가 참여하는 대규모 분산 AI 모델 학습 환경에서 InfiniBand의 높은 구축 비용 및 벤더 종속성을 탈피하고, 표준 이더넷 생태계의 가성비와 확장성을 활용할 요구

#### 한줄 요약
- 범용 이더넷 상에서 UDP 캡슐화와 무손실 제어(PFC/ECN)를 통해 L3 라우팅 가능한 고성능 RDMA를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PFC(Priority-based Flow Control, IEEE 802.1Qbb)**: 이더넷 링크 전체를 일시 정지시키는 레거시 PAUSE(802.3x)와 달리, 8개의 CoS 우선순위 큐 중 특정 큐(통상 Queue 3/4)에만 PAUSE 프레임을 전송하여 무손실(Lossless) 전송을 보장하는 L2 흐름 제어 기술.
- **DCQCN(Data Center Quantized Congestion Notification)**: 스위치 버퍼가 차오르면 ECN 마킹(IP ToS/DSCP)을 수행하고, 수신 RNIC가 송신 RNIC로 CNP(혼잡 알림 패킷)를 회신하여 송신 속도를 정밀 감속하는 L3 엔드투엔드 혼잡 제어 알고리즘.

</details>

- **L3 라우팅 확장성 (RoCEv2 UDP 4791)**: 표준 IP 라우팅 및 ECMP(Equal-Cost Multi-Path) 해싱을 완벽 지원하여 대규모 데이터센터 리프-스파인(Leaf-Spine) 패브릭에 유연하게 배포
- **무손실 이더넷(Lossless Ethernet) 기반 패킷 드롭 방지**: L2 PFC 하드웨어 버퍼 제어와 L3 ECN/DCQCN 선제적 감속을 결합하여 제로 패킷 손실 보장
- **기존 이더넷 생태계 호환성**: 100G/200G/400G/800G 상용 스위치 및 광모듈을 그대로 활용하여 인프라 구축 비용(CapEx) 대폭 절감

#### 한줄 요약
- L3 IP/UDP 라우팅 지원, PFC/DCQCN 기반 무손실 전송, 상용 이더넷 하드웨어 호환성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CNP(Congestion Notification Packet)**: ECN(CE 비트)이 마킹된 패킷을 수신한 목적지 RNIC가 발신지 RNIC로 즉시 전송하여 전송 레이트(Rate)를 낮추도록 지시하는 전용 제어 패킷 (RoCEv2 Opcode 0x81).

</details>

```text
[ 송신 호스트 (Host A: GPU/RNIC) ]                   [ 수신 호스트 (Host B: GPU/RNIC) ]
 ├─ RDMA User Buffer (Pinned)                         ├─ RDMA User Buffer (Pinned)
 └─ DCQCN 송신 레이트 제어기                            └─ CNP 생성 엔진
         │                                                    ▲
         ▼ (1. RoCEv2 패킷 송출: UDP Dst Port 4791)          │
┌─────────────────────────────────────────────────────────────┼───────────────────────────────────┐
│ [ 리프-스파인 무손실 이더넷 패브릭 (Leaf-Spine Network) ]    │                                   │
│  ├─ L2 계층: PFC (IEEE 802.1Qbb) ── (버퍼 임계치 도달 시 상류 스위치로 PAUSE 전송: 무손실 보장) │
│  └─ L3 계층: WRED / ECN (RFC 3168) ── (스위치 큐 점유 시 IP 헤더 ECN 비트를 '11'로 마킹)         │
└─────────────────────────────────────────────────────────────┼───────────────────────────────────┘
         ▲                                                    │ (2. ECN 마킹 패킷 수신)
         └──────────────── (3. CNP 패킷 역방향 전송) ─────────┘
```

선의 의미: RoCEv2 데이터 패킷이 스위치 패브릭에서 ECN 마킹을 거쳐 수신단에 도착하고, 수신 RNIC가 생성한 CNP 피드백을 통해 송신단이 레이트를 조절하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **RoCEv2 RNIC** | UDP 4791 캡슐화/역캡슐화, DMA 메모리 읽기/쓰기, DCQCN 레이트 제어기 구동 | Mellanox ConnectX |
| **PFC 제어기 (L2)** | 스위치 입력 버퍼 고갈 시 송신 포트에 802.1Qbb PAUSE 프레임을 전송하여 드롭 방지 | Lossless Queue |
| **ECN 마킹 엔진 (L3)** | 스위치 출력 큐의 WRED 임계치 초과 시 패킷 폐기 대신 IP 헤더 ECN 비트 마킹 | RFC 3168 ECN |
| **CNP 생성기** | 수신된 패킷의 ECN 마킹을 감지하여 발신지로 50$\mu\text{s}$ 주기 CNP 패킷 회신 | Congestion Signal |
| **ECMP 패브릭** | UDP 출발지 포트 번호(엔트로피 해시)를 기반으로 다중 스파인 경로에 트래픽 균등 분산 | Load Balancing |

#### 한줄 요약
- RoCEv2 RNIC, PFC 무손실 큐, ECN 스위치 마킹, CNP 피드백 루프, ECMP 분산 패브릭이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PFC 데드락(PFC Deadlock)**: 링(Ring) 또는 복합 토폴로지에서 스위치 간 버퍼가 서로 상대를 향해 영구적으로 PAUSE 프레임을 전송하여 트래픽 흐름이 완전히 마비되는 교착 상태.

</details>

```text
1. 송신 호스트가 GPU 메모리의 텐서 데이터를 RoCEv2(UDP 4791)로 캡슐화하여 패브릭으로 라인 레이트 송출
            │
            ▼
2. 스위치 버퍼가 경고 임계치(ECN Threshold)에 도달 ➔ 스위치가 패킷 IP 헤더의 ECN 필드를 '11'(CE)로 마킹
            │
            ▼
3. 수신 호스트 RNIC가 CE 마킹을 감지 ➔ 송신 호스트를 목적지로 하는 CNP(혼잡 알림 패킷)를 즉시 송출
            │
            ▼
4. 송신 RNIC의 DCQCN 엔진이 CNP를 수신하여 해당 큐 페어(QP)의 전송 속도를 즉각 감속(Rate Throttling)
            │
            ▼
5. 순간 폭주로 스위치 버퍼가 위험 임계치에 도달할 경우 ➔ L2 PFC PAUSE가 발동하여 0ms 무손실 방어
```

**동작 원리**

1. **UDP 캡슐화 전송**: InfiniBand BTH(기본 전송 헤더) 앞에 IP 및 UDP 헤더를 부착하여 전송
2. **ECN 선제 마킹**: 스위치 큐가 넘치기 전에 패킷을 폐기하지 않고 비트만 수정하여 하류로 전달
3. **CNP 신속 피드백**: 수신단이 혼잡 상태를 인지하고 고우선순위 CNP를 역방향으로 전송
4. **DCQCN 전송률 조절**: 송신단이 $\alpha$ 가중치에 따라 속도를 줄이고, 혼잡 해소 시 타이머 기반으로 속도 점진 회복
5. **PFC 최후 방어선**: DCQCN 반응 시간 이전에 버퍼가 가득 찰 경우에만 PFC가 일시 정지하여 패킷 드롭 원천 방지

#### 한줄 요약
- RoCEv2 송출, ECN 스위치 마킹, CNP 역방향 통지, DCQCN 감속, PFC 무손실 방어 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RoCEv1 vs RoCEv2 vs InfiniBand**: L2 전용 무손실 이더넷, L3 라우팅 지원 UDP/IP 이더넷, 네이티브 전용 패브릭의 비교.

</details>

| 비교 항목 | RoCEv1 (IB over L2 Ethernet) | RoCEv2 (IB over UDP/IP) | 네이티브 인피니밴드 (InfiniBand) |
|:---|:---|:---|:---|
| **캡슐화 계층** | **L2 이더넷 (EtherType: 0x8915)** | **L3/L4 UDP/IP (UDP Port: 4791)** | **InfiniBand Native Frame** |
| **L3 라우팅 가능 여부**| **불가 (단일 L2 서브넷에 국한)** | **완벽 지원 (IP 기반 L3 패브릭 라우팅)**| InfiniBand 서브넷 라우터 필요 |
| **혼잡 제어 메커니즘**| PFC (L2 Flow Control) 단독 의존 | **ECN + CNP + DCQCN + PFC 결합** | **신용 기반 흐름 제어 (Credit-Based)** |
| **인프라 비용 (CapEx)**| 저렴 (표준 L2 스위치) | **저렴 (표준 L3 데이터센터 스위치)** | **매우 높음 (전용 케이블 및 스위치)** |
| **주요 적용 영역** | 소규모 클러스터, 단일 랙 스토리지 | **초대규모 AI 데이터센터 (GPU 백본)** | 국가 슈퍼컴퓨터, 초고성능 HPC |

#### 한줄 요약
- RoCEv1은 소규모 L2 단일 랙용, RoCEv2는 초대규모 AI 클러스터 표준, InfiniBand는 최고 성능 전용망이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **헤드 오브 라인 블로킹(Head-of-Line Blocking, HoL)**: 특정 큐의 PFC 정지로 인해 해당 큐를 공유하는 다른 무관한 정상 트래픽까지 스위치 포트에서 전송이 가로막히는 전파 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스위치 간 PFC PAUSE 전파로 인한 패브릭 전체의 **PFC 데드락(Deadlock) 및 HoL 블로킹** | **PFC 데드락 워치독(Deadlock Watchdog)** 활성화 및 ECN 임계치를 PFC보다 낮게 사전 튜닝 | PFC 발동 빈도 90% 감소 및 데드락 발생 시 강제 큐 드레인으로 복구 |
| 다중 GPU가 단일 목적지로 동시 전송 시 버퍼 폭발로 인한 **인캐스트(Incast) 패킷 손실** | **스위치 WRED ECN 조기 마킹 및 송신단 DCQCN 정밀 튜닝** (Fast Recovery 적용) | 버퍼 오버플로우 방지 및 무손실 상태에서 처리율 98% 유지 |
| ECMP 라우팅 시 동일 플로우가 특정 링크로 쏠려 발생하는 **패브릭 불균형 및 핫스팟(Hotspot)** | RoCEv2 UDP Source Port에 **5-Tuple 엔트로피 해시 무작위화(Entropy Hashing)** 적용 | 리프-스파인 다중 경로 간 완벽한 트래픽 로드밸런싱 달성 |

#### 한줄 요약
- ECN/PFC 튜닝으로 데드락을 방지하고, DCQCN으로 인캐스트를 해소하며, 엔트로피 해싱으로 ECMP 부하를 분산한다.

## Ⅶ. 결론

- 하이퍼스케일 AI 데이터센터에서 GPU 간 통신 병목을 해소하고 비용 효율적인 고성능 네트워크를 구축하기 위해 **RoCEv2 기반의 무손실 이더넷 아키텍처**가 핵심 표준으로 채택되고 있으며, 인프라의 안정성을 극대화하기 위해 **PFC/ECN 듀얼 혼잡 제어 파라미터 최적화**, **PFC 데드락 워치독**, **엔트로피 해시 기반 ECMP 로드밸런싱**을 통합 적용하여 고성능 AI 패브릭을 완성

#### 한줄 요약
- RoCEv2와 무손실 이더넷(PFC/ECN) 및 DCQCN을 결합하여 고효율 AI 분산 학습 네트워크를 실현한다.
