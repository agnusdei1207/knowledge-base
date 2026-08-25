---
sidebar:
  order: 106
  label: "106. 집합 통신 All-Reduce"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 딥러닝 텐서 동기화 : 집합 통신 All-Reduce"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
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

- **All-Reduce**: $N$개 GPU의 로컬 텐서를 합산(Reduce)한 후 최종 결과를 모든 노드에 동일하게 배포(Gather)하는 집합 통신 프리미티브.
- **Parameter Server (PS) 병목**: 중앙 서버로 모든 그래디언트를 업로드/다운로드할 때 발생하는 대역폭 병목과 선형적 지연 폭증 한계.

</details>

- 정의/개념: 중앙 서버 없이 분산 GPU 간에 **Reduce-Scatter와 All-Gather 2단계를 통해 총 전송량을 GPU 수와 무관하게 고정하는 집합 통신 프리미티브**
- 배경/필요성: 파라미터 서버(PS) 방식의 중앙 대역폭 포화 한계로 인한 **GPU 수 증가 시 통신 시간 급증 및 분산 딥러닝 확장성 붕괴**

#### 한줄 요약
- Reduce-Scatter와 All-Gather를 통해 노드 수와 무관한 일정한 통신량으로 그래디언트를 전역 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Communication-Computation Overlap**: 딥러닝 역전파가 진행되는 동안 하위 레이어의 그래디언트 계산과 상위 레이어의 All-Reduce 통신을 비동기로 동시 병렬 수행하는 기법.

</details>

- **GPU 수($N$)와 무관한 전송량 고정($2 \times \frac{N-1}{N} M \approx 2M$)**: 노드가 수천 개로 확장되어도 **각 GPU당 송수신 데이터양은 텐서 크기 2배로 수렴**
- **완전 탈중앙화(Decentralized) 구조**: 중앙 병목 마스터 없이 **모든 GPU가 동일한 대역폭과 연산 부하를 공평 분담**
- **역전파 연산-통신 오버랩(Overlap)**: 이전 레이어 그래디언트 계산과 **다음 레이어 All-Reduce 통신을 백그라운드 병렬 처리**

#### 한줄 요약
- 노드 수 무관 전송량 고정, 완전 탈중앙화 부하 분담, 연산-통신 비동기 오버랩을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Tensor Fusion (버킷팅)**: 작은 크기의 수천 개 텐서를 개별 통신하지 않고 25~50MB 단위 버킷으로 합쳐서 전송하는 최적화 기법.

</details>

```text
[4개 GPU 간 Ring All-Reduce 토폴로지 및 2단계 파이프라인]
|-- GPU 0 (Rank 0: Chunk 0 송출 -> Rank 1 전달)
`-- GPU 1 (Rank 1: Chunk 1 송출 -> Rank 2 전달)
`-- GPU 2 (Rank 2: Chunk 2 송출 -> Rank 3 전달)
`-- GPU 3 (Rank 3: Chunk 3 송출 -> Rank 0 전달)
    |-- 1단계: Reduce-Scatter (N-1 = 3회 전송 -> 각 노드가 1/4 크기의 최종 합산 조각 보유)
    `-- 2단계: All-Gather (N-1 = 3회 전송 -> 모든 노드가 완전한 전체 합산 텐서 획득)
```

선의 의미: 4개의 GPU가 원형 링(Ring)으로 연결되어 이웃 GPU로만 데이터를 전달하며 합산과 배포를 완수하는 탈중앙화 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **통신 랭크 (Rank)** | All-Reduce 통신 그룹 내에서 **각 GPU에 부여된 고유 식별자 (0 ~ N-1)** | MPI / NCCL Rank |
| **텐서 버킷 퓨전기** | 역전파 중 계산된 미세 그래디언트들을 **25~50MB 단위로 병합** | Bucket Engine |
| **NCCL 엔진** | 텐서 크기 및 인터커넥트에 따라 **Ring, Tree, CollNet 알고리즘 자동 선택·실행** | NCCL Primitive |
| **Reduce-Scatter 모듈**| 텐서를 $N$분할하여 **순환 전달하며 로컬 버퍼 누적 합산** | 1st Phase |
| **All-Gather 모듈** | 합산 완료된 청크들을 **전 GPU로 순환 전송하여 최종 텐서 완성 복원** | 2nd Phase |

#### 한줄 요약
- 통신 랭크, 텐서 버킷 퓨전기, NCCL 엔진, Reduce-Scatter 모듈, All-Gather 모듈이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **In-Network Reduction (SHARP)**: All-Reduce 집계 연산을 GPU 코어가 아닌 인피니밴드 스위치 ASIC에서 직접 수행하여 트래픽을 50% 절감하는 기술.

</details>

```text
All-Reduce 텐서 버킷화, Reduce-Scatter 및 All-Gather 파이프라인
        │
   1. [텐서 버킷 생성] 역전파 진행 중 GPU별 로컬 그래디언트를 25MB 단위 버킷으로 융합
        │
   2. [통신 계약 검증] NCCL이 자료형(FP16/BF16), 텐서 형상, Sum 연산자 일치성 확인
        │
   3. [1단계: Reduce-Scatter] 각 노드가 청크를 이웃 노드로 $(N-1)$회 전송하며 누적 합산
        │ (각 노드가 고유한 1/N 완성 청크 획득 완료)
        ▼
   4. [2단계: All-Gather] 완성된 1/N 청크를 이웃 노드로 $(N-1)$회 순환 전송하여 전역 복제
        │
   ▼
5. [가중치 갱신] 전 GPU가 동일한 그래디언트를 획득하여 옵티마이저(AdamW) 가중치 업데이트
```

#### 한줄 요약
- 텐서 버킷화 → 통신 계약 검증 → Reduce-Scatter 축소 → All-Gather 수집 → 옵티마이저 갱신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Ring (대역폭 최적)** vs **Tree (지연시간 최적)** vs **Hierarchical (노드 내외 분리)**.

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

- **Straggler Node (스트래글러 노드)**: 열 쓰로틀링이나 패킷 손실로 인해 연산/통신 속도가 뒤처져 전체 클러스터의 동기화를 지연시키는 노드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단 1개의 저속 노드로 인해 전체 수천 개 GPU의 All-Reduce 대기 시간 폭증 | **NCCL 타임아웃 감시 및 `Straggler 노드 자동 감지/대체`** | 동기화 지연(Tail Latency) 80% 단축 및 전체 학습 효율 복원 |
| 작은 텐서 수천 개의 빈번한 개별 All-Reduce 호출로 인한 **커널 런치 오버헤드** | 프레임워크 레벨의 **`텐서 버킷 퓨전(Tensor Fusion: 25~50MB)`** 강제 | 네트워크 페이로드 효율 극대화 및 통신 오버헤드 90% 제거 |
| GPU 랭크 간 호출 순서 불일치로 인한 **영구 집합 통신 데드락(Deadlock)** | **NCCL 통신 계약(호출 순서, 텐서 형상) 정적 컴파일 검증** | 랭크 간 실행 순서 역전 차단 및 무한 대기 원천 방지 |
| 광역 분산 학습 시 노드 간 WAN 지연으로 인한 All-Reduce 정체 | **`勾배 압축(FP8/INT8 양자화)` 및 비동기 파이프라인** 적용 | 노드 간 통신 페이로드 50% 이상 감축 |

#### 한줄 요약
- 슬로우 노드 격리로 스트래글러를 방지하고, 텐서 퓨전으로 오버헤드를 줄이며, 계약 검증으로 데드락을 차단한다.

## Ⅶ. 결론

- 대규모 언어 모델(LLM) 및 생성형 AI의 분산 학습 확장성을 결정짓는 핵심 병목은 집합 통신에 있으며, 이를 극복하기 위해 **Ring 및 계층형 All-Reduce 아키텍처를 기반으로 노드 내 NVLink 초고속 집계, 노드 간 InfiniBand/RoCEv2 무손실 전송, NVIDIA SHARP 인패브릭 연산 가속**을 통합 구현하여 선형적(Linear) 분산 학습 확장성 완성

#### 한줄 요약
- All-Reduce는 Reduce-Scatter와 All-Gather 및 계층형 NVLink/RDMA 패브릭을 결합하여 대규모 AI 분산 훈련을 실현하는 핵심 통신 프리미티브다.