---
sidebar:
  order: 106
  label: "106. 집합 통신 All-Reduce (All-Reduce Collective Communication)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 딥러닝 텐서 동기화 : 집합 통신 All-Reduce (Collective Communication)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 106
extra:
  question_no: "106"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "Ring All-Reduce (Reduce-Scatter + All-Gather), Tree All-Reduce, 계층형 All-Reduce 및 NCCL 가속"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **올리듀스(All-Reduce)**: 분산 딥러닝(Distributed Deep Learning) 환경에서 $N$개의 GPU/노드가 보유한 로컬 그래디언트(Gradient) 또는 가중치 텐서를 특정 연산자(Sum, Min, Max, Prod)로 집계(Reduce)한 후, 그 최종 집계 결과를 참여한 모든 $N$개의 GPU에 동일하게 복제·배포(Broadcast/Gather)하는 집합 통신(Collective Communication) 프리미티브.
- **파라미터 서버(Parameter Server) 병목**: 단일 중앙 마스터 서버로 모든 워커 GPU가 기울기를 업로드하고 다운로드할 때 중앙 서버의 네트워크 대역폭이 포화되어 확장성이 붕괴되는 전통적 구조의 한계.

</details>

- 정의/개념: 중앙 집중형 파라미터 서버 없이 워커 GPU 간에 분산 토폴로지(Ring, Tree, Mesh)를 형성하여, **Reduce-Scatter(축소 분산)** 와 **All-Gather(전체 수집)** 2단계 파이프라인으로 전송 통신량을 $2\times \frac{N-1}{N} \times M$으로 최소화하는 **탈중앙화 집합 통신 아키텍처**
- 배경/필요성: 수천억 파라미터 LLM의 데이터 병렬(Data Parallelism) 및 파이프라인 병렬 학습 시, 매 배치(Step)마다 발생하는 대규모 그래디언트 동기화 시간을 최소화하여 GPU 연산 유휴(Compute Idle) 시간을 제거할 요구

#### 한줄 요약
- Reduce-Scatter와 All-Gather를 통해 중앙 병목 없이 모든 GPU의 텐서를 완전 분산 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Reduce-Scatter(축소 분산)**: 크기 $M$의 텐서를 $N$개 청크로 분할하여 이웃 노드로 순환 전송하며 합산함으로써, 각 GPU가 최종 집계된 텐서의 서로 다른 $\frac{1}{N}$ 조각만을 보유하게 만드는 1단계 연산.
- **All-Gather(전체 수집)**: 각 GPU가 보유한 완성된 $\frac{1}{N}$ 조각을 이웃 노드로 순환 브로드캐스트하여, 모든 GPU가 크기 $M$의 완전한 집계 텐서를 복원하게 만드는 2단계 연산.

</details>

- **노드 수($N$) 무관한 대역폭 최적화 (Ring All-Reduce)**: 각 GPU의 총 송수신 데이터량이 $2M$ ($N \rightarrow \infty$ 시)으로 수렴하여 노드 수가 증가해도 통신 시간 불변
- **하이브리드 계층형 토폴로지 (Hierarchical All-Reduce)**: 노드 내부는 초고속 NVLink로 1차 집계하고, 노드 간에는 InfiniBand/RoCEv2로 2차 교환하여 WAN/클러스터 트래픽 최소화
- **스트래글러(Straggler) 민감성**: 동기식(Synchronous) All-Reduce 특성상 가장 느린 단 1개의 저속 노드(Straggler) 속도에 맞춰 전체 클러스터 동기화가 지연되는 강한 동기화 종속성

#### 한줄 요약
- Ring 기반 $2M$ 통신량 최소화, 계층형 하이브리드 가속, 스트래글러 동기화 종속성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **텐서 버킷(Tensor Fusion / Bucket)**: 수천 개의 작은 텐서를 매번 개별 All-Reduce 호출하면 발생하는 커널 런치 오버헤드를 방지하기 위해, 일정한 크기(예: 25MB)의 단일 버킷으로 합쳐서(Fusing) 전송하는 최적화 기법.

</details>

```text
[ 4개 GPU 간 Ring All-Reduce 구조: N=4 ]

  ┌───────────────┐                  ┌───────────────┐
  │ GPU 0 (Rank 0)│ ── (청크 전송) ─▶ │ GPU 1 (Rank 1)│
  └───────┬───────┘                  └───────┬───────┘
          ▲                                  │
          │ (Ring 통신 루프)                  │ (Reduce-Scatter ➔ All-Gather)
          │                                  ▼
  ┌───────┴───────┐                  ┌───────────────┐
  │ GPU 3 (Rank 3)│ ◀── (청크 전송) ─ │ GPU 2 (Rank 2)│
  └───────────────┘                  └───────────────┘

[ 통신 2단계 파이프라인 ]
1단계 Reduce-Scatter: 3회 ($N-1$) 전송 ➔ 각 GPU가 1/4 크기의 최종 합산 조각 보유
2단계 All-Gather:     3회 ($N-1$) 전송 ➔ 모든 GPU가 완전한 전체 합산 텐서 보유
```

선의 의미: 4개의 GPU가 원형 링(Ring)으로 연결되어 이웃 GPU로만 데이터를 전달하며 합산과 배포를 완수하는 탈중앙화 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **통신 랭크 (Rank)** | All-Reduce 통신 그룹(Communicator) 내에서 각 GPU에 부여된 고유 식별자 (0 ~ N-1) | MPI / NCCL Rank |
| **텐서 버킷 퓨전기** | 역전파(Backprop) 중 계산된 미세 그래디언트들을 25~50MB 단위로 병합 | Bucket Engine |
| **NCCL 엔진** | 텐서 크기 및 인터커넥트에 따라 Ring, Tree, CollNet 알고리즘 자동 선택·실행 | NCCL Primitive |
| **Reduce-Scatter 모듈** | 텐서를 $N$분할하여 링/트리 경로로 순환 전달하며 로컬 버퍼 누적 합산 | 1st Phase |
| **All-Gather 모듈** | 합산 완료된 청크들을 전 GPU로 순환 전송하여 최종 텐서 완성 복원 | 2nd Phase |

#### 한줄 요약
- 통신 랭크, 텐서 버킷 퓨전기, NCCL 엔진, Reduce-Scatter 모듈, All-Gather 모듈이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인패브릭 리덕션(In-Network Reduction, SHARP)**: All-Reduce 합산 연산을 GPU 코어가 아닌 Mellanox Quantum 인피니밴드 스위치 내부 연산 ASIC에서 직접 수행하여 네트워크 트래픽을 50% 절감하는 기술.

</details>

```text
1. 딥러닝 역전파(Backward Pass) 진행 중 GPU별 로컬 그래디언트 텐서 버킷 생성
            │
            ▼
2. NCCL이 통신 계약(자료형: FP16/BF16, 텐서 형상, Sum 연산자) 일치 검증
            │
            ▼
3. [1단계: Reduce-Scatter 실행] ➔ 각 노드가 자신의 청크를 이웃 노드로 $(N-1)$회 전송하며 누적 합산
            │ (각 노드가 고유한 1/N 완성 청크 획득 완료)
            ▼
4. [2단계: All-Gather 실행] ➔ 완성된 1/N 청크를 이웃 노드로 $(N-1)$회 순환 전송하여 전역 복제
            │
            ▼
5. 전 GPU가 완벽히 동일한 집계 그래디언트 획득 ➔ 옵티마이저(AdamW) 가중치 업데이트 즉각 착수
```

**동작 원리**

1. **계산-통신 오버랩**: 역전파 계산이 완료된 레이어부터 즉시 비동기(Asynchronous) All-Reduce 트리거
2. **청크 분할 전송**: 전체 텐서 크기 $M$을 $N$개 블록으로 쪼개어 파이프라인 스트리밍
3. **링 축소(Reduce-Scatter)**: 노드 $i$가 노드 $i+1$로 데이터를 쏘고 수신 노드는 자신의 데이터와 하드웨어 덧셈
4. **링 수집(All-Gather)**: 누적 합산이 완료된 청크를 링을 따라 한 바퀴 돌려 전원 공유
5. **동기화 완료**: 링을 2바퀴 ($2(N-1)$ 스텝) 도는 동안 네트워크 링크는 100% 포화 상태로 가동

#### 한줄 요약
- 텐서 버킷화, 통신 계약 검증, Reduce-Scatter 축소, All-Gather 수집, 옵티마이저 갱신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Ring vs Tree vs 계층형(Hierarchical) All-Reduce**: 대역폭 우선 링 알고리즘, 소형 메시지 저지연 트리 알고리즘, 노드 내/간 인터커넥트 분리 계층형 알고리즘의 비교.

</details>

| 알고리즘 종류 | 링 All-Reduce (Ring All-Reduce) | 트리 All-Reduce (Tree All-Reduce) | 계층형 All-Reduce (Hierarchical) |
|:---|:---|:---|:---|
| **통신 메커니즘** | **원형 링 순환 (2(N-1) 스텝)** | **이진/바이너리 트리 집계 및 배포** | **노드 내 NVLink 집계 + 노드 간 IB 집계**|
| **최적 데이터 크기** | **대형 텐서 (대역폭 집약적 워크로드)**| **소형 텐서 (지연 시간 집약적 워크로드)**| **초대규모 멀티 노드 GPU 클러스터** |
| **소요 지연 시간** | $O(N)$ 홉 수 비례 지연 시간 발생 | **$O(\log N)$ 초저지연 트리 수렴** | 노드 간 저속 인터커넥트 트래픽 최소화 |
| **인터커넥트 활용** | 모든 링크가 동일 대역폭일 때 최적 | 루트 노드 링크 포화 위험 존재 | **NVLink와 InfiniBand 성능 격차 완벽 극복**|
| **주요 적용 영역** | 표준 멀티 GPU 데이터 병렬화 | 파이프라인/텐서 병렬화 중간 동기화 | **수만 개 GPU 하이퍼스케일 AI 클러스터** |

#### 한줄 요약
- 대형 텐서는 링(대역폭 최적), 소형 텐서는 트리(지연 최적), 대규모 클러스터는 계층형(링크 격차 해소)을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스트래글러 노드(Straggler Node)**: GPU 클럭 저하, 열 쓰로틀링, 광케이블 패킷 재전송 등으로 인해 타 노드보다 연산/통신 완료가 뒤처져 전체 클러스터의 All-Reduce 완료를 지연시키는 지연 노드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단 1개의 저속 노드로 인해 전체 수천 개 GPU의 All-Reduce 대기 시간 폭증 (스트래글러 문제) | **NCCL 타임아웃 감시 및 Straggler 감지 시 클러스터 슬로우 노드 자동 격리/대체** | 동기화 지연(Tail Latency) 80% 단축 및 전체 학습 효율 복원 |
| 작은 텐서 수천 개의 빈번한 개별 All-Reduce 호출로 인한 **커널 런치 오버헤드 폭증** | 프레임워크 레벨의 **텐서 버킷 퓨전(Tensor Fusion: 25MB~50MB 단위 병합)** 강제 | 네트워크 페이로드 효율 극대화 및 통신 개시 오버헤드 90% 제거 |
| GPU 랭크 간 All-Reduce 호출 순서 불일치로 인한 **영구 집합 통신 데드락(Deadlock)** | **NCCL 통신 계약(호출 순서, 텐서 형상, 데이터 타입) 정적 컴파일 검증** | 랭크 간 실행 순서 역전 차단 및 훈련 중단 무한 대기 원천 방지 |

#### 한줄 요약
- 슬로우 노드 격리로 스트래글러를 방지하고, 텐서 퓨전으로 오버헤드를 줄이며, 계약 검증으로 데드락을 차단한다.

## Ⅶ. 결론

- 대규모 언어 모델(LLM) 및 생성형 AI의 분산 학습 확장성을 결정짓는 핵심 병목은 집합 통신에 있으며, 이를 극복하기 위해 **Ring 및 계층형 All-Reduce 아키텍처**를 기반으로 **노드 내 NVLink 초고속 집계**, **노드 간 InfiniBand/RoCEv2 무손실 전송**, **NVIDIA SHARP 인패브릭 연산 하드웨어 가속**을 통합 구현하여 선형적(Linear) 분산 학습 확장성을 완성

#### 한줄 요약
- Reduce-Scatter와 All-Gather 및 계층형 NVLink/RDMA 패브릭을 결합하여 고효율 대규모 AI 분산 훈련을 실현한다.
