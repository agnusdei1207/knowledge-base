---
title: "Data Parallelism 데이터 병렬 (Data Parallelism)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 256
---

# 📖 【암기용】 개념 완전 이해

> 목적: 데이터 병렬을 같은 모델을 여러 GPU에 복제하고 서로 다른 데이터를 처리한 뒤 gradient를 맞추는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 동일 model replica를 여러 device에 두고 mini-batch를 나눠 학습하는 병렬화 방식
- **왜 필요한가**: 모델 하나가 GPU memory에 들어가지만 데이터와 학습 시간이 크면, 여러 GPU가 각자 다른 batch를 처리해 step 처리량을 늘려야 한다.
- **핵심 직관**: 같은 문제집을 여러 사람이 나눠 풀고, 채점 결과를 모아 하나의 공통 답안지를 갱신하는 구조다.

## 깊이 이해
- **배경·문제의식**: 단일 GPU 학습은 batch 처리량과 학습 시간이 제한된다. 모델이 device memory에 들어가는 경우에는 모델을 나누기보다 데이터를 나누는 방식이 구현과 디버깅 측면에서 단순하다.
- **작동 원리**: 각 GPU는 동일 parameter로 forward/backward를 수행하고, backward 후 gradient를 All-Reduce로 평균 내며, 모든 replica가 같은 optimizer step을 적용한다.
- **비유**: 같은 교재를 가진 학생들이 서로 다른 문제를 풀고, 풀이에서 나온 오답 경향을 모아 다음 공부 방향을 동일하게 수정하는 방식이다.
- **구체 예시**: 8 GPU에서 local batch 4, gradient accumulation 2이면 global batch는 8 x 4 x 2 = 64가 된다.
- **흔한 오해·주의점**: GPU 수를 늘리면 항상 학습 결과가 같아지는 것은 아니다. global batch 증가에 맞춰 learning rate, warmup, gradient clipping을 조정해야 한다.

## 연결 개념
- All-Reduce — replica gradient 동기화에 사용
- DistributedDataParallel — PyTorch의 대표 data parallel 구현
- ZeRO — data parallel redundancy를 줄이는 메모리 최적화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Data Parallelism은 model replica, batch shard, gradient synchronization, global batch 조정을 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Data Parallelism은 동일 모델을 각 GPU에 복제하고 mini-batch를 나누어 학습하는 병렬화 방식임.
> 2. **가치**: 모델이 단일 GPU에 들어갈 때 구현 복잡도를 낮게 유지하면서 학습 throughput을 rank 수에 맞춰 늘릴 수 있음.
> 3. **판단 포인트**: gradient all-reduce 비용과 global batch 증가에 따른 수렴 특성을 함께 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 병렬 학습 기본 구조 확인 | model replica, data shard, gradient sync | 데이터를 복제한다고 오해 |
| 통신 병목 이해 확인 | All-Reduce, bucket, step time | GPU 수 증가만 강조 |
| 학습 품질 판단 확인 | global batch, learning rate scaling | batch 증가에 따른 수렴 영향 누락 |

> 요약: 이 문제는 데이터 분할과 gradient 동기화를 하나의 학습 step으로 설명하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 모델 복제·데이터 분할 학습
- 배경: 단일 GPU는 batch 처리량과 학습 시간이 제한되지만, 모델 크기가 device memory 내라면 모델 분할은 불필요할 수 있음.
- 필요성: 동일 parameter를 유지하면서 여러 GPU가 서로 다른 mini-batch를 처리하고 gradient를 동기화해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Dataset -> Sampler -> Mini-batch Shard per Rank -> Model Replica per GPU
-> Local Forward/Backward -> Gradient All-Reduce -> Same Optimizer Step
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Distributed Sampler | rank별 data shard 제공 | epoch별 shuffle seed 관리 |
| Model Replica | 각 GPU에 동일 parameter 보유 | memory 중복 발생 |
| Gradient Bucket | gradient를 묶어 collective 호출 | overlap 조정 가능 |
| All-Reduce | rank 간 gradient 평균 | network 병목 가능 |

> 요약: Data Parallelism은 sampler가 데이터를 나누고, replica가 local gradient를 만든 뒤 All-Reduce로 parameter 갱신을 맞춘다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Global Batch 분할 -> 각 GPU Forward -> 각 GPU Backward
-> Gradient Bucket 생성 -> All-Reduce 평균 -> Optimizer Step -> Parameter 동기 상태 유지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | rank별 mini-batch shard 로딩 | data overlap 없음 |
| 2 | 동일 model replica로 forward/backward 수행 | loss 계산 |
| 3 | gradient bucket별 All-Reduce 수행 | gradient checksum |
| 4 | 모든 rank가 동일 optimizer step 적용 | parameter checksum |

> 요약: Data Parallelism은 각 GPU의 local 계산 후 gradient 평균을 맞추어 모든 replica가 같은 parameter 상태로 다음 step을 시작한다.

---

## Ⅳ. 특징

| 구분 | 단일 GPU 학습 | Data Parallelism | 판단 기준 |
|:---|:---|:---|:---|
| 모델 배치 | GPU 1개에 1개 모델 | GPU마다 replica | 모델 memory 크기 |
| 데이터 처리 | batch 단일 처리 | mini-batch shard 병렬 처리 | dataset 처리량 |
| 통신 | 없음 | gradient All-Reduce | gradient 크기 |
| 학습 설정 | local batch 기준 | global batch 조정 필요 | 수렴 curve |

> 요약: Data Parallelism은 구현 구조가 단순하지만 gradient 통신과 global batch 조정이 핵심 관리 포인트다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Model Parallelism | Data Parallelism | 모델이 단일 GPU memory에 들어가는지 |
| 비용/성능 | 통신 적은 단일 GPU | All-Reduce 비용 추가, 처리량 증가 | communication/compute ratio |
| 운영/위험 | 단순 재현성 | rank seed, sampler, checkpoint 관리 | reproducibility |

> 요약: 모델이 device memory에 들어가고 gradient 통신이 감당 가능하면 Data Parallelism을 첫 선택지로 둔다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 수렴 변화 | global batch 증가 | learning rate scaling, warmup | validation loss |
| 통신 병목 | 큰 gradient와 많은 rank | bucketing, overlap, NVLink/IB 사용 | all-reduce time |
| 데이터 중복 | sampler seed 오류 | DistributedSampler 검증 | sample id overlap |

> 요약: Data Parallelism 리스크는 수렴, 통신, 데이터 샤딩이며 학습 로그와 sampler 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| scaling | GPU 수 증가 대비 step throughput 증가 | samples/sec |
| 동기화 | rank 간 parameter 차이 없음 | checksum |
| 품질 | baseline 대비 validation metric 유지 | evaluation set |

> 요약: Data Parallelism 효과는 처리량, parameter 동기화, validation 품질을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. PyTorch DistributedDataParallel 또는 framework 기본 DDP를 적용하고 DistributedSampler 중복 여부를 검증함.
2. Global batch = local batch x rank 수 x accumulation step으로 계산하고 learning rate와 warmup을 함께 조정함.
3. Profiler에서 all-reduce time과 compute time overlap을 확인해 bucket size와 rank placement를 조정함.

**결론 (2줄):**
- 기술사 판단: 모델이 단일 GPU에 적재되면 Data Parallelism을 우선 적용하고, memory 초과 시 ZeRO 또는 Model Parallelism을 결합함.
- 향후 방향: Data Parallelism은 ZeRO, tensor parallel, pipeline parallel과 조합되어 3D parallel training의 기본 축으로 남음.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "데이터 병렬을 설명하시오" | mini-batch shard와 gradient all-reduce 흐름 | 단일 GPU 대비 차이 |
| 요구사항 명시형 | "대규모 학습 확장 방안을 제시하시오" | global batch, sampler, bucket 조정 | 수렴 변화와 통신 병목 |

> 요약: 설명형은 구조와 동기화 원리를, 방안형은 batch·통신·품질 지표를 중심으로 작성한다.
