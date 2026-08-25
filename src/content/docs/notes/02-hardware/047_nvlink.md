---
sidebar:
  order: 47
  label: "047. NVLink 고속 인터커넥트 (NVLink)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 47
extra:
  question_no: "047"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "다중 GPU 분산 통신과 메모리 풀링의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NVLink**: NVIDIA가 개발한 GPU-GPU 및 CPU-GPU 간 전용 초고대역폭 직렬 인터커넥트로, 하드웨어 캐시 일관성 및 직접 메모리 공유(P2P)를 제공하는 독자 버스 인터페이스.
- **피어 투 피어 전송(Peer-to-Peer Transfer, P2P 전송)**: 호스트 CPU와 시스템 메인 메모리를 경유하지 않고 GPU 간 전용 고속 링크를 통해 VRAM 데이터를 직접 고속 송수신하는 기술.

</details>

- 정의/개념: 호스트 CPU 경유 없이 GPU 간 초고대역폭 직접 메모리 접근(P2P)과 하드웨어 캐시 일관성을 제공하는 **NVIDIA NVLink 고속 인터커넥트 아키텍처**
- 배경/필요성: 기존 표준 PCIe 버스의 대역폭 한계(Gen5 x16: 64GB/s)로 인한 **초대형 LLM 모델 병렬화 시 그래디언트 동기화 및 텐서 교환 통신 병목 극복**

#### 한줄 요약
- NVLink는 호스트 CPU를 거치지 않고 GPU 간 초당 수 테라바이트급 초고대역폭 직접 통신(P2P)을 가능하게 하는 스케일업 인터커넥트 기술이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NVSwitch**: 단일 노드 내 다수 GPU의 NVLink 포트를 크로스바 스위치 구조로 연결하여 전 대역폭 완전 연결(Full Mesh)을 지원하는 전용 패브릭 스위치 칩.
- **집단 통신(Collective Communication)**: 분산 딥러닝 환경에서 다수 GPU 간 그래디언트 및 텐서 데이터를 동기화하는 다대다 통신 패턴(All-Reduce, All-Gather 등).

</details>

- 초고대역폭 통신: 다중 링크 집성(Link Aggregation)을 통해 **PCIe 대비 7~14배 이상의 초고대역폭(양방향 최대 1.8TB/s)** 제공
- CPU 개입 없는 직접 메모리 접근: **P2P(Peer-to-Peer)** 직접 로드/스토어를 지원하여 시스템 DRAM 복사 오버헤드 원천 제거
- 노드 내 완전 풀메시 연결: **NVSwitch** 칩을 통해 단일 서버 내 8~72개 GPU 간 비차단(Non-Blocking) 완전 연결망 구축

#### 한줄 요약
- NVSwitch와 결합하여 노드 내 모든 GPU 간 비차단 풀메시 대역폭을 제공함으로써 대규모 모델 병렬화의 통신 지연을 극소화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 칩 내부의 병렬 데이터를 초고속 차동 직렬 신호(100Gbps+ PAM4)로 변환하여 물리 링크로 송수신하는 고속 물리 계층 회로.
- **NCCL(NVIDIA Collective Communications Library)**: 하드웨어 NVLink/NVSwitch 토폴로지를 자동 감지하여 최적화된 링·트리 집단 통신 연산을 실행하는 멀티 GPU 라이브러리.

</details>

```text
[NVIDIA DGX 단일 노드 스케일업 아키텍처]
 ┌─────────────────────────────────────────────────────────────┐
 │ [NVSwitch 스위치 패브릭 (초고속 크로스바 교환망)]            │
 └──────┬──────────────┬──────────────┬──────────────┬─────────┘
        │ NVLink 포트  │ NVLink       │ NVLink       │ NVLink
 ┌──────▼──────┐┌──────▼──────┐┌──────▼──────┐┌──────▼──────┐
 │ GPU 코어 0  ││ GPU 코어 1  ││ GPU 코어 2  ││ GPU 코어 7  │
 │ ├─ HBM3 VRAM││ ├─ HBM3 VRAM││ ├─ HBM3 VRAM││ ├─ HBM3 VRAM│
 │ └─ SerDes PHY││ └─ SerDes PHY││ └─ SerDes PHY││ └─ SerDes PHY│
 └──────┬──────┘└──────┬──────┘└──────┬──────┘└──────┬──────┘
        │ PCIe         │ PCIe         │ PCIe         │ PCIe
 ┌──────▼──────────────▼──────────────▼──────────────▼─────────┐
 │ 호스트 CPU & 시스템 메모리 (PCIe 컨트롤러 / 부팅 / 스토리지) │
 └─────────────────────────────────────────────────────────────┘
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 포함 관계; GPU 간 대용량 연산 트래픽은 NVSwitch 상단 경로로 처리되고, 제어 명령만 하단 PCIe로 처리됨

| 구성요소 | 소속 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| **GPU 엔드포인트** | 가속기 다이 | 대규모 텐서 연산 수행 및 NVLink P2P 패킷 송수신 | HBM3 메모리 직결 |
| **SerDes 물리 계층** | 칩 경계 PHY | 100Gbps+ PAM4 고속 차동 신호 변환 및 물리 전송 | 초저에너지(pJ/bit) |
| **NVSwitch 칩** | 서버 백플레인 기판 | 8~72개 GPU 간 비차단 풀메시 크로스바 라우팅 | 초당 수십 TB/s 스위칭 |
| **NCCL 라이브러리** | 통신 소프트웨어 계층 | 물리 토폴로지 자동 탐색 및 **All-Reduce / All-to-All 알고리즘 최적화** | 링/트리 집단 통신 |
| **호스트 CPU / PCIe** | 시스템 제어 계층 | OS 부팅, 드라이버 초기화 및 스토리지 데이터 로딩 | 제어 플레인 담당 |

#### 한줄 요약
- NVLink 시스템은 GPU 엔드포인트(SerDes), NVSwitch 크로스바 패브릭, NCCL 통신 라이브러리 및 호스트 제어 계층으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **All-Reduce**: 각 GPU가 계산한 그래디언트를 합산(Reduce)한 뒤, 최종 결과를 모든 참여 GPU에 동일하게 복제 분배(Broadcast)하는 집단 통신 연산.

</details>

```text
1. 역전파(Backpropagation) 연산 완료 ➔ GPU별 그래디언트 텐서 도출
                      │
                      ▼
2. NCCL 통신 라이브러리: 물리 인터커넥트 토폴로지 감지
   ┌──────────────────┴──────────────────┐
[ 노드 내부 GPU 간 통신 (Intra-Node) ]  [ 노드 간 분산 통신 (Inter-Node) ]
   │                                     │
   ▼                                     ▼
3. NVLink P2P 직접 패킷 발행             3. InfiniBand RDMA 네트워크로 우회 전송
   │                                     │ (NIC 경유로 지연시간 및 대역폭 제약 발생)
   ▼                                     │
4. NVSwitch 크로스바를 통해 목적지       │
   GPU VRAM으로 제로 카피 직결 라우팅    │
   │                                     │
   └──────────────────┬──────────────────┘
                      │
                      ▼
5. 텐서 합산 및 전체 GPU 재분배 (All-Reduce 완료) ➔ 다음 학습 스텝 개시
```

분기 결과: **노드 내부 GPU 간 통신은** NVLink와 NVSwitch를 통해 초당 테라바이트급으로 완료되나, **노드 간 통신은** InfiniBand RDMA를 거치게 됨

#### 한줄 요약
- 역전파 ➔ NCCL 토폴로지 판정 ➔ NVLink P2P 발행 ➔ NVSwitch 크로스바 라우팅 ➔ All-Reduce 완료의 5단계로 동작한다.

## Ⅴ. 종류 및 비교

| 인터커넥트 기술 | NVIDIA NVLink (v4 / v5) | PCIe Gen5 / Gen6 | CXL.mem | InfiniBand (RDMA) |
|:---|:---|:---|:---|:---|
| 연결 범위 | **단일 노드 내 다중 GPU (스케일업)** | 단일 노드 내 범용 장치 | 단일 노드/랙 내 메모리 풀링 | **노드 간 대규모 클러스터 (스케일아웃)** |
| 양방향 대역폭 | **초고대역폭 (GPU당 900GB/s ~ 1.8TB/s)** | 보통 (x16 기준 64GB/s ~ 128GB/s) | 고속 (x16 기준 64GB/s+) | 초고속 (400Gbps ~ 800Gbps) |
| 지연시간 (Latency)| **초저지연 (수십 ns 수준)** | 보통 (수백 ns) | 저지연 (150~200ns) | 마이크로초 ($\sim 1\mu\text{s}$) |
| 캐시 일관성 / P2P | **하드웨어 GPU P2P 완벽 지원** | 제한적 P2P (일관성 없음) | **하드웨어 캐시 일관성 지원** | 메모리 직접 접근(RDMA) |
| 생태계 및 표준화 | **NVIDIA 독점 규격 (GPU 최적화)** | PCI-SIG 개방형 범용 표준 | CXL 컨소시엄 개방형 표준 | IBTA 개방형 고성능 표준 |

#### 한줄 요약
- 단일 노드 내 초고속 GPU 스케일업에는 NVLink가 독보적이며, 노드 간 대규모 클러스터 스케일아웃 네트워킹에는 InfiniBand가 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **통신-연산 오버랩(Communication-Computation Overlap)**: 후속 레이어 역전파 연산을 수행하는 동안 선행 레이어의 그래디언트를 NVLink로 비동기 전송하는 파이프라이닝 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 All-Reduce 통신 대기로 인한 GPU 연산 파이프라인 유휴 | **통신-연산 오버랩(Overlap) 및 텐서 버킷팅(Bucket Size 최적화)** | 통신 지연시간 100% 은닉 및 학습 처리량 30% 향상 |
| 단일 서버 내 8개 GPU 집적으로 인한 극심한 발열(수 kW) | **다이렉트 칩 수랭 냉각(Direct-to-Chip Liquid Cooling) 설계** | 열 스로틀링 방지 및 100% 지속 부스트 클록 유지 |
| 멀티 노드 확장 시 노드 간 InfiniBand와의 대역폭 불균형 | **노드 내 텐서 병렬화(TP) + 노드 간 파이프라인/데이터 병렬화(PP/DP)** | 통신 집중 계층 분리로 클러스터 확장 효율 90% 사수 |

#### 한줄 요약
- 실무에서는 통신-연산 오버랩으로 지연을 은닉하고, 수랭 냉각으로 발열을 제어하며, 하이브리드 병렬화로 노드 간 병목을 극복한다.

## Ⅶ. 결론

- 초대형 생성형 AI 모델의 분산 학습 및 고성능 추론 병목을 제거하기 위해 **단일 노드 내부에 NVLink와 NVSwitch 기반의 풀메시 스케일업 아키텍처를 표준 구축**하고, 통신 지연을 은닉하기 위해 **NCCL 기반의 통신-연산 오버랩 파이프라이닝**을 적용하며, 멀티 노드 확장 시에는 **InfiniBand RDMA와 하이브리드 병렬화(TP+PP+DP) 기술**을 융합하는 고성능 AI 슈퍼컴퓨팅 인프라 설계 확립

#### 한줄 요약
- NVLink는 GPU 간 초고대역폭 직접 통신을 실현하는 AI 스케일업의 핵심이며, NVSwitch 및 NCCL과의 결합으로 초거대 모델 병렬화를 완성한다.