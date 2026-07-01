---
title: "Pipeline Parallelism 파이프라인 병렬 (Pipeline Parallelism)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 258
---

# 📖 【암기용】 개념 완전 이해

> 목적: 파이프라인 병렬을 모델의 layer를 여러 stage로 나누고 micro-batch를 흘려보내는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 모델 layer를 순서대로 여러 GPU stage에 배치하고 micro-batch를 pipeline으로 실행하는 병렬화 방식
- **왜 필요한가**: 모델 layer 전체가 단일 GPU memory에 들어가지 않을 때 layer 묶음을 여러 GPU에 나눠 저장해야 한다.
- **핵심 직관**: 긴 생산 라인을 여러 작업대에 나누고, 작은 묶음의 제품을 연속 투입해 작업대가 차례로 일하게 하는 구조다.

## 깊이 이해
- **배경·문제의식**: Layer를 GPU별로 나누면 한 micro-batch는 stage를 순차 통과해야 하므로 모든 GPU가 동시에 일하지 못하는 bubble이 생긴다.
- **작동 원리**: Global batch를 여러 micro-batch로 나누고, 각 stage가 forward와 backward를 일정한 schedule로 실행해 pipeline bubble을 줄인다.
- **비유**: 식당 코스요리에서 전채, 메인, 디저트 담당이 따로 있고 손님 여러 팀을 시간차로 받아 각 담당자가 계속 일하게 만드는 방식이다.
- **구체 예시**: 4개 pipeline stage에 16 micro-batch를 흘리면 초기 채우기와 마지막 비우기 구간의 bubble 비율이 줄어든다.
- **흔한 오해·주의점**: stage 수를 늘리면 memory는 줄지만 bubble, activation 전송, schedule 복잡도가 증가한다. stage별 계산량 균형이 필요하다.

## 연결 개념
- Model Parallelism — Pipeline Parallelism의 상위 개념
- Micro-batching — pipeline bubble을 줄이는 batch 분할
- Tensor Parallelism — stage 내부 layer를 다시 나누는 병렬화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Pipeline Parallelism은 layer partition, micro-batch schedule, bubble, activation memory를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pipeline Parallelism은 모델 layer를 stage로 나누고 micro-batch를 순차적으로 흘려 실행하는 모델 병렬 방식임.
> 2. **가치**: layer를 GPU별로 나눠 저장해 단일 GPU memory 한계를 넘고, micro-batch로 stage 유휴 시간을 줄임.
> 3. **판단 포인트**: stage 균형, micro-batch 수, bubble ratio, activation 전송량이 적용 성패를 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| layer 분할 이해 확인 | pipeline stage, micro-batch | 데이터 병렬과 혼동 |
| schedule 이해 확인 | forward/backward, bubble | stage 수 증가만 강조 |
| 적용 판단 확인 | memory 절감 vs bubble/activation 통신 | stage imbalance 누락 |

> 요약: 이 문제는 layer를 나누는 것보다 stage가 계속 일하도록 micro-batch를 스케줄링하는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: layer stage 병렬 실행
- 배경: 초대형 모델은 layer 전체 parameter와 activation이 단일 GPU memory를 초과해 layer 단위 분할이 필요함.
- 필요성: Micro-batch schedule로 stage 유휴 구간을 줄이고 stage별 memory와 계산량을 균형화해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Model Layers -> Stage 0 / Stage 1 / Stage 2 / Stage 3
Micro-batch 0..M -> Forward Pipeline -> Backward Pipeline -> Gradient Sync
                   +-> Schedule / Activation Buffer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Pipeline Stage | layer 묶음을 GPU에 배치 | 계산량 균형 필요 |
| Micro-batch | batch를 작은 단위로 분할 | bubble 감소와 overhead 균형 |
| Schedule | forward/backward 실행 순서 제어 | 1F1B 등 사용 |
| Activation Buffer | stage 간 중간값 저장·전송 | memory와 통신량 영향 |

> 요약: Pipeline Parallelism은 stage, micro-batch, schedule, activation buffer가 결합되어 layer 분할 모델을 실행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Layer Partition -> Micro-batch 생성 -> Stage별 Forward 전파
-> Loss 계산 -> Stage별 Backward 역전파 -> Gradient 누적 -> Optimizer Step
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | layer를 stage별로 분할 | stage compute balance |
| 2 | batch를 micro-batch로 분할 | micro-batch count |
| 3 | forward activation을 다음 stage로 전달 | activation transfer time |
| 4 | backward gradient를 이전 stage로 전달 | bubble ratio |

> 요약: Pipeline Parallelism은 micro-batch가 forward와 backward 방향으로 stage를 통과하며 gradient를 계산한다.

---

## Ⅳ. 특징

| 구분 | Tensor Parallelism | Pipeline Parallelism | 판단 기준 |
|:---|:---|:---|:---|
| 분할 단위 | layer 내부 tensor | layer 묶음 stage | 모델 구조 |
| 통신 시점 | layer마다 collective | stage 경계 activation | 통신 빈도 |
| 병목 | intra-layer bandwidth | bubble과 stage imbalance | micro-batch 수 |
| 적용 범위 | GPU group 내부 | 여러 stage로 깊은 모델 분할 | layer depth |

> 요약: Pipeline Parallelism은 깊은 모델의 layer memory를 나누는 데 적합하지만 bubble과 stage 균형이 성능 한계가 된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단순 layer split | micro-batch pipeline | stage 유휴 시간 |
| 비용/성능 | memory 절감만 고려 | bubble, activation memory 동시 고려 | bubble ratio |
| 운영/위험 | 수동 stage 지정 | profiler 기반 repartition | stage time skew |

> 요약: Pipeline Parallelism은 memory를 줄이는 기법이면서 schedule 문제이므로 bubble과 stage skew를 같이 봐야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| pipeline bubble | micro-batch 수 부족 | micro-batch 증가, 1F1B schedule | bubble ratio |
| stage imbalance | layer별 계산량 편차 | stage repartition | stage latency |
| activation memory 증가 | micro-batch 누적 저장 | activation checkpointing | peak activation memory |

> 요약: 주요 리스크는 bubble, stage imbalance, activation memory이며 schedule과 repartition으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| bubble | stage idle time 허용 범위 이내 | pipeline profiler |
| memory | stage별 peak memory 한도 이내 | GPU memory stats |
| 처리량 | micro-batch 조정 후 samples/sec 확인 | training log |

> 요약: Pipeline Parallelism 효과는 bubble, stage memory, 처리량 지표를 동시에 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Layer별 parameter와 FLOPs를 산정해 stage별 계산량과 memory가 균형을 이루도록 partition함.
2. Micro-batch 수를 stage 수보다 충분히 크게 설정하고 profiler로 bubble ratio를 확인함.
3. Activation checkpointing과 1F1B schedule을 적용해 activation memory와 stage idle time을 함께 줄임.

**결론 (2줄):**
- 기술사 판단: 모델 depth가 크고 layer memory가 병목이면 Pipeline Parallelism을 적용하되, stage imbalance가 크면 tensor parallel과 재분할을 병행함.
- 향후 방향: Pipeline Parallelism은 interleaved schedule과 3D parallel training 조합으로 대규모 LLM 학습의 기본 구성요소가 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "파이프라인 병렬을 설명하시오" | micro-batch forward/backward 흐름 | tensor parallel 대비 차이 |
| 요구사항 명시형 | "LLM 학습 병렬화 방안을 제시하시오" | stage partition과 bubble 측정 절차 | activation memory와 stage imbalance |

> 요약: 설명형은 pipeline 실행 원리를, 방안형은 stage 균형과 micro-batch 조정을 중심으로 작성한다.
