---
title: "모델 프루닝 (Model Pruning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 75
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 프루닝을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 모델에서 중요도가 낮은 가중치·채널·헤드·레이어를 제거해 연산량과 크기를 줄이는 압축 기법
- **왜 필요한가**: 모든 파라미터가 동일하게 중요한 것은 아니며, 일부 연결은 정확도 기여가 작아 배포 비용만 늘림.
- **핵심 직관**: 나무의 죽은 가지를 잘라 햇빛과 영양분을 중요한 가지에 집중시키는 작업임.

## 깊이 이해
- **배경·문제의식**: 딥러닝 모델은 over-parameterized되어 중복 표현을 포함함. Pruning은 중요도가 낮은 요소를 제거해 FLOPs, memory, latency를 줄임.
- **작동 원리**: magnitude, gradient, Hessian, attention head importance 등 기준으로 제거 대상을 정함. 제거 후 fine-tuning으로 정확도 회복을 수행함.
- **비유**: 답안에서 채점에 영향 없는 문장을 삭제하고 핵심 표·수식만 남겨 같은 점수를 더 짧게 쓰는 것과 같음.
- **구체 예시**: CNN은 channel pruning, Transformer는 attention head·FFN neuron pruning, LLM은 structured sparsity와 layer dropping을 적용함.
- **흔한 오해·주의점**: unstructured pruning은 희소성은 높지만 일반 하드웨어에서 속도가 바로 줄지 않을 수 있음. 하드웨어 친화적 structured pruning이 실무에 유리함.

## 연결 개념
- Model Compression — pruning의 상위 개념
- Sparse Model — pruning 결과 구조
- Fine-Tuning — pruning 후 정확도 회복 단계

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Pruning은 중요도 낮은 파라미터·구조를 제거해 모델 연산량과 메모리를 줄이는 압축 기법임.
> 2. **가치**: 배포 지연·전력·저장 비용을 낮추고 엣지·온디바이스 실행 가능성을 높임.
> 3. **판단 포인트**: unstructured/structured 방식, 중요도 기준, fine-tuning, 하드웨어 가속 효과를 검증해야 함.

## Ⅰ. 개요 및 필요성

모델 프루닝은 불필요한 모델 요소를 제거하는 압축 기법임. 대형 모델의 배포 비용과 지연을 낮추기 위해 정확도 기여가 낮은 가중치·채널·헤드·레이어를 제거함.

## Ⅱ. 구조 및 구성요소

```text
Trained Model -> Importance Scoring -> Pruning Mask/Removal
      -> Fine-tuning -> Sparse/Compact Model -> Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Importance Metric | 제거 대상 산정 | magnitude, gradient |
| Pruning Unit | weight/channel/head/layer | structured 권장 |
| Fine-tuning | 정확도 회복 | small LR, few epochs |
| Sparse Runtime | 희소 연산 실행 | HW 지원 필요 |

> 요약: Pruning은 중요도 평가, 제거 단위 선택, 재학습, 런타임 검증을 거쳐 실제 배포 효과를 확인함.

## Ⅲ. 동작원리 및 흐름도

```text
기준 모델 평가 -> 중요도 계산 -> 하위 요소 제거
    -> 미세조정 -> 정확도·FLOPs·지연 평가 -> 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | baseline 정확도·latency 측정 | 기준 성능 |
| 2 | pruning ratio와 단위 결정 | 10~50% 제거율 |
| 3 | 제거 후 fine-tuning 수행 | 정확도 회복 |
| 4 | 실제 하드웨어 지연 측정 | FLOPs vs latency gap |

> 요약: Pruning은 제거율을 높이는 작업이 아니라, 하드웨어에서 지연이 줄고 정확도가 유지되는 지점을 찾는 과정임.

## Ⅳ. 특징

| 구분 | Unstructured Pruning | Structured Pruning | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 제거 단위 | 개별 weight | channel/head/layer | HW 친화성 |
| 압축률 | 높음 | 중간 | sparsity 50~90% 가능 |
| 속도 개선 | sparse kernel 필요 | 일반 kernel 효과 | latency 실측 필수 |
| 정확도 | 회복 가능 | 제거 단위 영향 큼 | fine-tuning 필요 |

> 요약: 실무에서는 압축률보다 실제 하드웨어 지연 개선이 중요하므로 structured pruning이 우선 검토됨.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. CNN 비전 모델은 channel pruning 30% 적용 후 mAP 하락 2%p 이내, FPS 30 이상 기준으로 배포
2. Transformer는 attention head importance를 측정해 하위 20% head 제거 후 MMLU·사내셋 회귀 검증
3. LLM은 pruning 단독보다 quantization·distillation과 결합해 메모리·지연·정확도 균형을 맞춤

**결론 (2줄):**
- 기술사 판단: 범용 하드웨어 배포는 structured pruning, 전용 sparse accelerator 보유 시 unstructured pruning을 선택함.
- 향후 방향: Pruning은 NAS·quantization-aware training과 결합해 배포 자동 최적화 파이프라인으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 중요도 평가·제거·재학습 흐름 | pruning 방식 비교 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | 병목별 pruning ratio·검증 절차 | 정확도·FLOPs·latency 기준 |

> 요약: 설명형은 pruning 원리, 방안형은 실제 하드웨어 지연과 정확도 회귀 기준으로 목차를 전환함.
