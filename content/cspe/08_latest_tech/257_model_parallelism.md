---
title: "Model Parallelism 모델 병렬 (Model Parallelism)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 257
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 병렬을 하나의 모델을 여러 device에 나누어 올리는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 모델 parameter, layer, tensor, expert를 여러 device에 분할 배치해 학습·추론하는 병렬화 방식
- **왜 필요한가**: LLM은 parameter와 activation이 단일 GPU memory를 초과하므로, 데이터를 나누는 것만으로는 모델을 실행할 수 없다.
- **핵심 직관**: 책 한 권이 너무 커서 한 책상에 놓을 수 없을 때, 장별 또는 페이지별로 여러 책상에 나눠 놓고 순서대로 읽는 방식이다.

## 깊이 이해
- **배경·문제의식**: Data Parallelism은 모델을 GPU마다 복제하므로 모델 하나가 GPU memory에 들어가야 한다. 초대형 모델은 parameter, optimizer state, activation 합계가 device memory를 초과한다.
- **작동 원리**: 모델을 layer 단위로 나누면 pipeline parallelism, tensor 연산 내부를 나누면 tensor parallelism, expert 단위로 나누면 expert parallelism이 된다.
- **비유**: 한 공장에서 모든 공정을 처리할 수 없어 절단, 조립, 검사 공장을 나누고 중간 산출물을 이동시키는 구조다.
- **구체 예시**: Transformer block의 attention/MLP weight를 GPU group에 나눠 저장하고, forward 중 필요한 activation을 all-gather 또는 all-reduce로 교환한다.
- **흔한 오해·주의점**: 모델 병렬은 memory 문제를 풀지만 통신이 사라지지 않는다. activation, tensor shard, pipeline boundary 통신이 새 병목이 된다.

## 연결 개념
- Tensor Parallelism — layer 내부 tensor를 나누는 모델 병렬
- Pipeline Parallelism — layer 묶음을 stage로 나누는 모델 병렬
- ZeRO — data parallel replica의 state 중복을 줄이는 보완 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Model Parallelism은 memory 수용성, 분할 단위, activation 통신, bubble/collective 비용을 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Parallelism은 하나의 모델을 여러 GPU에 분할 배치해 단일 device memory 한계를 넘는 병렬화 방식임.
> 2. **가치**: 초대형 LLM의 parameter, activation, optimizer state를 device group에 분산해 학습과 추론 실행을 가능하게 함.
> 3. **판단 포인트**: tensor, pipeline, expert 분할 중 어떤 통신 패턴이 workload와 topology에 맞는지 선택해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 병렬화 목적 구분 확인 | memory 초과 해결, 모델 분할 | Data Parallel과 혼동 |
| 분할 방식 이해 확인 | tensor, pipeline, expert parallel | 모델을 단순 복제한다고 설명 |
| 통신 리스크 확인 | activation, collective, pipeline bubble | memory 절감만 강조 |

> 요약: 이 문제는 모델을 어떻게 나누고 그 결과 어떤 통신이 생기는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 모델 분할 병렬 실행
- 배경: 대규모 LLM은 parameter와 activation이 단일 GPU memory를 초과해 model replica 기반 학습만으로 실행 불가함.
- 필요성: 모델 구조를 tensor, layer, expert 단위로 나누고 device 간 통신 비용을 topology에 맞춰 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Model Graph -> Partition Planner -> Tensor / Layer / Expert Shard
-> Device Group Mapping -> Runtime Communication -> Forward / Backward Execution
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Partition Planner | 분할 단위와 device group 결정 | memory와 communication 동시 고려 |
| Tensor Shard | weight matrix 일부 저장 | intra-layer collective 필요 |
| Pipeline Stage | layer 묶음 저장 | micro-batch schedule 필요 |
| Runtime Communication | activation, gradient, shard 교환 | NVLink/IB topology 영향 |

> 요약: Model Parallelism은 model graph를 분할하고 device group에 배치한 뒤 runtime이 필요한 중간 데이터를 교환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
모델 memory 산정 -> 분할 전략 선택 -> GPU group mapping
-> Forward activation 교환 -> Backward gradient 교환 -> Optimizer state 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | parameter, activation, optimizer memory 산정 | peak memory |
| 2 | tensor/pipeline/expert 분할 전략 선택 | communication plan |
| 3 | device topology에 shard 배치 | rank mapping |
| 4 | forward/backward 중 shard와 activation 교환 | step time, correctness |

> 요약: Model Parallelism은 memory 계산에서 시작해 분할·배치·통신·검증의 순서로 설계한다.

---

## Ⅳ. 특징

| 구분 | Data Parallelism | Model Parallelism | 판단 기준 |
|:---|:---|:---|:---|
| 배치 방식 | 모델 복제, 데이터 분할 | 모델 분할, 데이터 일부 공유 | model memory |
| 통신 대상 | gradient all-reduce | activation, tensor shard, boundary | 통신 패턴 |
| 적용 목적 | throughput 확대 | memory 한계 극복 | 단일 GPU 적재 가능 여부 |
| 구현 난이도 | framework 지원 폭 큼 | partition과 schedule 필요 | 운영 역량 |

> 요약: Model Parallelism은 단일 GPU memory를 넘는 모델에 필요하지만, 분할 단위에 따른 통신 설계가 추가된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Tensor Parallel | Pipeline Parallel | layer 내부 통신 vs stage boundary 통신 |
| 비용/성능 | 단일 전략 | 3D parallel 조합 | memory와 step time 균형 |
| 운영/위험 | 자동 분할 도구 의존 | 수동 partition tuning | profiler 기반 조정 |

> 요약: 모델 병렬은 tensor와 pipeline을 단독으로 쓰기보다 data parallel까지 포함한 3D 조합으로 적용하는 경우가 많다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 통신 과다 | 분할 경계가 빈번한 tensor 교환 유발 | layer grouping, topology-aware mapping | communication/compute ratio |
| memory 불균형 | stage별 parameter와 activation 편차 | stage rebalancing | peak memory per rank |
| 디버깅 난이도 | shard별 tensor shape 불일치 | shape assertion, checkpoint validation | runtime error rate |

> 요약: Model Parallelism 리스크는 통신, memory 불균형, 검증 난이도이며 profiler와 shape 검증이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| memory | 모든 rank peak memory 한도 이내 | framework memory stats |
| step time | 통신 시간이 compute를 과도하게 잠식하지 않음 | profiler |
| 정확성 | 단일 모델 기준 loss와 일치 범위 확인 | small-scale parity test |

> 요약: Model Parallelism은 memory 수용성과 학습 정확성을 먼저 확인하고, 이후 step time을 줄이는 순서로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 모델 parameter, activation, optimizer state를 산정해 단일 GPU 적재 가능 여부를 먼저 판단함.
2. Tensor parallel group은 NVLink domain 내부에 배치하고, pipeline stage는 activation boundary와 memory 균형을 기준으로 나눔.
3. Small model parity test로 loss와 gradient shape를 검증한 뒤 full-scale job에 적용함.

**결론 (2줄):**
- 기술사 판단: 모델이 단일 GPU memory를 초과하면 Model Parallelism을 적용하고, 통신량이 커지면 ZeRO와 Data Parallelism을 조합함.
- 향후 방향: Model Parallelism은 tensor, pipeline, expert, sequence parallel을 조합하는 multi-dimensional parallelism으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "모델 병렬을 설명하시오" | partition, mapping, communication 흐름 | Data Parallel 대비 차이 |
| 요구사항 명시형 | "초대형 모델 학습 방안을 제시하시오" | memory 산정과 분할 전략 선택 | tensor/pipeline 조합과 리스크 |

> 요약: 설명형은 모델 분할 원리를, 방안형은 memory 계산과 통신 배치 기준을 중심으로 작성한다.
