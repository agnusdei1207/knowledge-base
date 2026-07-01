---
title: "Tensor Parallelism 텐서 병렬 (Tensor Parallelism)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 259
---

# 📖 【암기용】 개념 완전 이해

> 목적: 텐서 병렬을 Transformer layer 내부의 큰 행렬 연산을 여러 GPU에 나누는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 하나의 layer 안에서 weight tensor와 activation 연산을 여러 GPU에 분할하는 모델 병렬 방식
- **왜 필요한가**: Attention과 MLP의 weight matrix가 커지면 단일 GPU memory와 연산 시간이 병목이 되므로 layer 내부를 나눠야 한다.
- **핵심 직관**: 큰 표 계산을 행 또는 열 단위로 여러 사람이 나눠 계산하고, 마지막에 필요한 부분만 모아 결과표를 만드는 방식이다.

## 깊이 이해
- **배경·문제의식**: Pipeline Parallelism은 layer 묶음을 나누지만, 개별 layer 자체가 크면 한 stage 내부 GPU memory와 compute가 부족하다.
- **작동 원리**: Column parallel 또는 row parallel 방식으로 weight matrix를 나누고, forward/backward 중 all-reduce, all-gather, reduce-scatter로 부분 결과를 결합한다.
- **비유**: 거대한 행렬 곱을 한 사람이 다 하지 않고, 열 묶음 또는 행 묶음으로 분담한 뒤 합산이 필요한 위치에서 결과를 맞추는 방식이다.
- **구체 예시**: Transformer MLP의 첫 linear layer는 column-wise로 나누고, 두 번째 linear layer는 row-wise로 나누어 GPU group이 하나의 layer처럼 동작하게 할 수 있다.
- **흔한 오해·주의점**: Tensor Parallelism은 통신이 적은 기법이 아니다. Layer마다 collective가 발생하므로 NVLink 같은 intra-node fabric과 rank 배치가 step time을 좌우한다.

## 연결 개념
- Model Parallelism — Tensor Parallelism의 상위 개념
- All-Reduce — row parallel 결과 결합에 사용
- NVLink — tensor parallel group 내부 통신에 적합한 GPU fabric

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Tensor Parallelism은 layer 내부 weight shard, collective 위치, GPU topology를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Tensor Parallelism은 Transformer layer의 큰 tensor 연산을 GPU group에 분할해 실행하는 모델 병렬 방식임.
> 2. **가치**: 단일 layer의 parameter와 activation memory를 나누고, 큰 matrix multiplication을 device group이 함께 처리하게 함.
> 3. **판단 포인트**: Collective가 layer마다 발생하므로 tensor parallel group은 고대역폭 intra-node fabric에 배치해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분할 단위 확인 | layer 내부 weight tensor shard | pipeline parallel과 혼동 |
| 통신 위치 확인 | all-reduce, all-gather, reduce-scatter | 통신 없는 memory 절감으로 설명 |
| 적용 판단 확인 | TP size, GPU topology, kernel granularity | TP size 증가가 항상 유리하다고 단정 |

> 요약: 이 문제는 tensor를 어떻게 나누고 어떤 collective로 다시 맞추는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: layer 내부 tensor 분할
- 배경: 대형 Transformer의 attention과 MLP weight가 커지면 개별 layer가 단일 GPU memory와 compute 한계를 초과함.
- 필요성: Weight matrix와 activation을 GPU group에 나누고 collective 위치를 최적화해 layer 단위 실행을 유지해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Transformer Layer -> Column Parallel Linear / Row Parallel Linear
-> Tensor Parallel Group -> Collective Runtime -> Combined Layer Output
                         +-> NVLink / High-Bandwidth Fabric
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TP Group | layer 내부 shard를 담당하는 GPU 집합 | 보통 node 내부 배치 |
| Column Shard | output feature 방향 분할 | concat/all-gather 필요 가능 |
| Row Shard | input feature 방향 분할 | partial sum all-reduce 필요 |
| Collective Runtime | shard 결과 결합 | NCCL 등 사용 |

> 요약: Tensor Parallelism은 layer의 weight를 방향별로 나누고 collective runtime으로 부분 결과를 결합한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Weight Matrix 분할 -> 각 GPU Partial GEMM 수행
-> 필요한 Collective 수행 -> Activation 전달 -> Backward에서 Gradient Shard 계산 -> Optimizer 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | layer weight를 column 또는 row 방향으로 shard | shard shape |
| 2 | 각 GPU가 partial matrix multiplication 수행 | kernel time |
| 3 | all-reduce/all-gather로 layer output 구성 | output parity |
| 4 | backward에서 shard gradient와 optimizer state 갱신 | gradient checksum |

> 요약: Tensor Parallelism은 partial GEMM과 collective 결합을 layer마다 반복해 하나의 큰 layer처럼 동작한다.

---

## Ⅳ. 특징

| 구분 | Pipeline Parallelism | Tensor Parallelism | 판단 기준 |
|:---|:---|:---|:---|
| 분할 위치 | layer 묶음 사이 | layer 내부 tensor | layer 크기 |
| 통신 빈도 | stage boundary | layer별 collective | fabric bandwidth |
| 유휴 문제 | bubble 발생 | bubble보다 collective 지배 | TP group size |
| 배치 | stage 간 순차 | 같은 layer 동시 실행 | intra-node topology |

> 요약: Tensor Parallelism은 layer 내부 병렬 처리에 적합하지만 collective가 빈번해 GPU 간 fabric 품질에 민감하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 GPU layer 실행 | TP group partial layer 실행 | layer memory 초과 여부 |
| 비용/성능 | 통신 없음, memory 한계 | collective 비용 추가, memory 분산 | compute/communication ratio |
| 운영/위험 | 단순 checkpoint | sharded checkpoint 필요 | checkpoint 변환 도구 |

> 요약: Tensor Parallelism은 큰 layer를 실행 가능하게 하지만, TP size가 커질수록 kernel granularity와 collective overhead를 확인해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| collective 병목 | layer마다 all-reduce 발생 | TP group을 NVLink domain 내부 배치 | collective time |
| kernel 분할 손실 | shard가 작아져 GPU 점유율 감소 | TP size 제한, fused kernel 적용 | SM occupancy |
| checkpoint 복잡도 | weight shard 저장 | conversion script와 metadata 관리 | load failure rate |

> 요약: Tensor Parallelism 리스크는 collective, kernel granularity, checkpoint이며 TP size와 topology 선택으로 step time과 복구 실패를 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| memory | rank별 layer memory 한도 이내 | GPU memory stats |
| 통신 | collective time 허용 비율 이내 | profiler, NCCL trace |
| 정확성 | 단일 layer 결과와 parity 확인 | unit test |

> 요약: Tensor Parallelism은 memory 감소와 layer output parity를 먼저 검증하고, collective time을 줄이는 순서로 조정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Attention head 수와 MLP hidden size가 TP size로 나누어지는지 확인해 shard shape 오류를 방지함.
2. Tensor parallel group을 같은 NVLink/NVSwitch domain에 배치하고 node 간 TP group 구성을 피함.
3. Sharded checkpoint metadata를 관리해 training, inference, fine-tuning 간 weight 변환 절차를 표준화함.

**결론 (2줄):**
- 기술사 판단: 개별 layer가 크면 Tensor Parallelism을 적용하고, 모델 depth가 병목이면 Pipeline Parallelism을 함께 적용함.
- 향후 방향: Tensor Parallelism은 sequence parallel, expert parallel과 결합되어 Transformer 내부 분할의 기본 기술로 유지됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "텐서 병렬을 설명하시오" | partial GEMM과 collective 결합 흐름 | pipeline parallel 대비 차이 |
| 요구사항 명시형 | "LLM layer 병렬화 방안을 제시하시오" | TP size, shard shape, topology 절차 | collective 병목과 checkpoint 리스크 |

> 요약: 설명형은 layer 내부 분할 원리를, 방안형은 TP group 배치와 검증 기준을 중심으로 작성한다.
