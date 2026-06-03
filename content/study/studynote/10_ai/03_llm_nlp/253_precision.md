---
title: 253. 정밀도 (Precision)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]])는 모델이 Positive라고 예측한 것들 중 실제로 Positive인 비율로, **[[293_fp_function_point|FP]](False Positive, 거짓 양성)를 얼마나 [[656_ir_containment|억제]]했는지**를 측정한다.
> 2. **가치**: 스팸 필터, 광고 타기팅, 법적 판단 등 **잘못된 양성 판정의 비용이 큰 [[064_relation_domain|도메인]]**에서 [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])보다 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 우선시해야 한다.
> 3. **판단 포인트**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]은 트레이드오프([[233_precision_recall_f1_roc_auc_threshold|Precision]]-[[254_recall_sensitivity|Recall]] Tradeoff) [[083_relationship_in_er_model|관계]]이므로, 임계값(Threshold) 조정 또는 F1-Score로 균형을 찾아야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]의 정의와 직관

```
정밀도(Precision) = TP / (TP + FP)

            실제로 Positive인 것
= ─────────────────────────────────────────
  내가 Positive라고 예측한 것(TP + FP) 전체
```

**직관적 해석**: "내가 맞다고 말한 것 중에서 실제로 맞은 비율"
- [[233_precision_recall_f1_roc_auc_threshold|정밀도]] = 1.0: Positive 예측이 모두 정확, FP가 0
- [[233_precision_recall_f1_roc_auc_threshold|정밀도]] = 0.5: Positive 예측의 절반만 실제 Positive

### 1.2 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 중요한 이유

[[293_fp_function_point|FP]](False Positive)의 실제 비용:

| [[064_relation_domain|도메인]] | FP의 의미 | [[293_fp_function_point|FP]] 발생 비용 |
|:---|:---|:---|
| 스팸 필터 | 정상 메일을 스팸으로 차단 | 중요 업무 이메일 분실 |
| 광고 타기팅 | 관심 없는 사용자에게 광고 | 광고 예산 낭비 |
| 법원 판결 [[190_ai_llm_requirements_specification|AI]] | 무고한 사람을 유죄 판정 | 억울한 처벌 |
| 금융 대출 심사 | 신용 양호자 대출 거절 | 고객 이탈, 기회 손실 |
| 뉴스 팩트체크 | 진실 정보를 가짜뉴스로 [[104_classification_analysis|분류]] | 정보 왜곡 |

- **📢 섹션 요약 비유**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 낚시꾼의 정확도다. 그물을 100번 던져서 물고기만 잡히면([[293_fp_function_point|FP]]=0) [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 100%, 절반이 쓰레기([[293_fp_function_point|FP]])면 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 50%. 쓸데없이 그물을 많이 던져 정상 메일까지 잡으면 안 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]-[[092_recall_sensitivity_hit_rate|재현율]] 트레이드오프 도식

```
┌──────────────────────────────────────────────────────────┐
│         정밀도(Precision) - 재현율(Recall) 트레이드오프     │
│                                                          │
│  정밀도                                                   │
│  (Precision)                                             │
│  ↑                                                       │
│  1.0 │╲                                                  │
│      │ ╲   이상적 곡선 (정밀도·재현율 모두 최대)             │
│  0.8 │  ╲                                                │
│      │   ╲    ← PR 곡선 (Precision-Recall Curve)         │
│  0.6 │    ╲                                              │
│      │     ╲                                             │
│  0.4 │      ╲                                            │
│      │       ╲                                           │
│  0.2 │        ╲                                          │
│      └──────────────────────────────────────→ 재현율     │
│       0.0   0.2   0.4   0.6   0.8   1.0    (Recall)     │
│                                                          │
│  임계값(Threshold)↑ → 정밀도↑, 재현율↓                    │
│  임계값(Threshold)↓ → 정밀도↓, 재현율↑                    │
└──────────────────────────────────────────────────────────┘
```

### 2.2 임계값 (Threshold) 조정 원리

[[104_classification_analysis|분류]] 모델은 보통 [[130_probability|확률]]값(0~1)을 출력하고, 임계값을 기준으로 Positive/Negative 판정:

| 임계값 | 효과 | [[233_precision_recall_f1_roc_auc_threshold|정밀도]] | [[092_recall_sensitivity_hit_rate|재현율]] |
|:---:|:---|:---:|:---:|
| 0.9 (높음) | 매우 확실할 때만 Positive | ↑↑ | ↓↓ |
| 0.5 (기본) | 표준 판정 | 중간 | 중간 |
| 0.1 (낮음) | 조금만 Positive 같아도 판정 | ↓↓ | ↑↑ |

**구체적 예시:**
```
샘플별 스팸 확률: [0.92, 0.85, 0.73, 0.55, 0.41, 0.29, 0.12]

임계값=0.5 → [Spam, Spam, Spam, Spam, Normal, Normal, Normal]
임계값=0.8 → [Spam, Spam, Normal, Normal, Normal, Normal, Normal]
임계값=0.3 → [Spam, Spam, Spam, Spam, Spam, Normal, Normal]
```

### 2.3 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]의 수식 비교

| 지표 | 수식 | 분모 의미 | 초점 |
|:---|:---|:---|:---|
| **[[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]])** | TP / (TP+[[293_fp_function_point|FP]]) | 내가 Positive라 예측한 전체 | [[293_fp_function_point|FP]] [[656_ir_containment|억제]] |
| **[[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])** | TP / (TP+FN) | 실제 Positive 전체 | FN [[656_ir_containment|억제]] |
| **정확도(Accuracy)** | (TP+TN) / 전체 | 전체 샘플 | 전체 오류 |
| **[[255_f1_score|F1-Score]]** | 2PR/(P+R) | — | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]·[[092_recall_sensitivity_hit_rate|재현율]] 균형 |

- **📢 섹션 요약 비유**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 "말하면 반드시 맞는" 입이 무거운 사람이다. 확실하지 않으면 말을 안 한다([[092_recall_sensitivity_hit_rate|재현율]] 희생). 반면 [[092_recall_sensitivity_hit_rate|재현율]]을 중시하면 확실하지 않아도 일단 말한다([[233_precision_recall_f1_roc_auc_threshold|정밀도]] 희생). 두 성격이 서로 반대인 것이 트레이드오프다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] vs [[092_recall_sensitivity_hit_rate|재현율]]: [[064_relation_domain|도메인]]별 우선순위

| [[064_relation_domain|도메인]] | 우선 지표 | 이유 | 감수할 수 있는 오류 |
|:---|:---|:---|:---|
| 암 진단 | [[092_recall_sensitivity_hit_rate|재현율]]↑ | FN(미검출) 치명적 | [[293_fp_function_point|FP]](과잉 검사)는 추가 검사로 해결 |
| 스팸 필터 | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]↑ | [[293_fp_function_point|FP]](정상 차단) 치명적 | FN(일부 스팸 허용)은 수용 가능 |
| 사기 탐지 | [[092_recall_sensitivity_hit_rate|재현율]]↑ | FN(사기 미탐지) 치명적 | [[293_fp_function_point|FP]](의심 거래 차단)는 해결 가능 |
| 법률 [[190_ai_llm_requirements_specification|AI]] | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]↑ | [[293_fp_function_point|FP]](무죄인 유죄 판정) 치명적 | FN은 다른 수단으로 탐지 |
| 유해 콘텐츠 필터 | [[092_recall_sensitivity_hit_rate|재현율]]↑ | FN(유해 콘텐츠 통과) 치명적 | [[293_fp_function_point|FP]](일부 정상 콘텐츠 차단) 수용 |

### 3.2 Average [[233_precision_recall_f1_roc_auc_threshold|Precision]] ([[572_ap_access_point_ds_distribution_system|AP]])와 AUPRC

- **[[067_pull_request_pr_merge_request_code_review|PR]] 곡선 아래 면적(AUPRC, Area Under [[233_precision_recall_f1_roc_auc_threshold|Precision]]-[[254_recall_sensitivity|Recall]] Curve)**: 다양한 임계값에서의 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]·[[092_recall_sensitivity_hit_rate|재현율]] [[282_performance_tactics|성능]]을 종합 평가
- 클래스 불균형 [[001_dikw_pyramid|데이터]]에서 **AUROC보다 더 민감한 지표**로 선호됨
- **[[572_ap_access_point_ds_distribution_system|AP]](Average [[233_precision_recall_f1_roc_auc_threshold|Precision]])**: [[067_pull_request_pr_merge_request_code_review|PR]] 곡선의 가중 평균, [[288_object_detection_yolo_rcnn|객체 탐지]]([[288_object_detection_yolo_rcnn|Object Detection]])에서 mAP(mean [[572_ap_access_point_ds_distribution_system|AP]])로 활용

### 3.3 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 관련된 α·β 오류

| 통계학 용어 | ML 용어 | 의미 |
|:---|:---|:---|
| 1종 오류(Type I Error) | [[293_fp_function_point|FP]] (False Positive) | 실제 음성을 양성으로 잘못 판정 |
| 2종 오류(Type II Error) | FN (False Negative) | 실제 양성을 음성으로 잘못 판정 |
| [[233_precision_recall_f1_roc_auc_threshold|정밀도]] | 1 - FDR (False Discovery Rate) | FP를 줄이는 것이 목표 |

- **📢 섹션 요약 비유**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 검사의 기소율이다. 기소한 피의자 중 실제 유죄 비율이 높아야([[233_precision_recall_f1_roc_auc_threshold|정밀도]]↑) 억울한 사람이 없다. 하지만 기소를 너무 신중히 하면 진짜 범인을 놓칠 수 있다([[092_recall_sensitivity_hit_rate|재현율]]↓) — 이것이 트레이드오프다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 최적화를 위한 임계값 탐색

```
목표: 정밀도 ≥ 0.95 조건에서 재현율 최대화

방법:
1. 모델 출력 확률값 수집
2. 임계값 0.0 ~ 1.0 구간에서 탐색
3. 각 임계값에서 정밀도, 재현율 계산
4. 정밀도 ≥ 0.95 조건 만족하는 가장 낮은 임계값 선택
   (가장 낮은 임계값 = 재현율 최대)
```

### 4.2 클래스 불균형에서 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 해석

**예시: 사기 탐지 (사기 0.1%, 정상 99.9%)**

```
모델 A: 정밀도=0.50, 재현율=0.80
→ 사기라고 예측한 것 중 50%만 실제 사기
→ 정상 거래 차단이 절반 → 고객 불만

모델 B: 정밀도=0.85, 재현율=0.50
→ 사기라고 예측한 것의 85% 실제 사기
→ 일부 사기는 놓치지만 정상 거래 차단 최소화
```

### 4.3 기술사 핵심 판단 포인트
- **[[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 중요한 이유를 [[064_relation_domain|도메인]] 맥락으로 설명**할 것
- [[233_precision_recall_f1_roc_auc_threshold|정밀도]]·[[092_recall_sensitivity_hit_rate|재현율]] 트레이드오프 → **임계값 조정**으로 해결
- F1-Score는 균형이 필요할 때, **[[064_relation_domain|도메인]] 특성에 따라 가중 F-Score(Fβ)**로 조정 가능
- `Fβ = (1+β²) × (P×R) / (β²×P + R)` — β>1이면 [[092_recall_sensitivity_hit_rate|재현율]] 중시, β<1이면 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 중시

- **📢 섹션 요약 비유**: 광고 타기팅 AI의 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 30%라면, 광고를 보여준 10명 중 7명이 전혀 관심 없는 사람이라는 뜻이다. 광고주는 광고비를 70% 낭비하는 것 — [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 높이면 예산 효율이 극적으로 개선된다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 향상의 기대효과
- **스팸 필터**: 중요 이메일 차단율 감소 → 사용자 [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상
- **광고 시스템**: 클릭률([[090_ctr_mode|CTR]], Click-Through Rate) 향상 → [[012_roi_return_on_investment|ROI]] 개선
- **의료 [[190_ai_llm_requirements_specification|AI]] 보조 진단**: 의사 추가 검토 부담 감소 → 업무 효율 향상
- **자동화 품질 검사**: 정상 제품 폐기 비용 절감

### 5.2 결론
[[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 "정확하게 예측했을 때만 발언하라"는 원칙을 수치화한 지표다. [[293_fp_function_point|FP]](False Positive)를 최소화해야 하는 [[064_relation_domain|도메인]]에서 핵심 지표이며, [[233_precision_recall_f1_roc_auc_threshold|정밀도]]-[[092_recall_sensitivity_hit_rate|재현율]] 트레이드오프를 이해하고 임계값 조정과 Fβ-Score를 통해 실무 요구사항에 맞게 균형을 조율하는 능력이 [[190_ai_llm_requirements_specification|AI]] 엔지니어의 핵심 역량이다.

- **📢 섹션 요약 비유**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 바둑 기사의 수 선택과 같다. 확실히 좋은 수만 두는 기사([[233_precision_recall_f1_roc_auc_threshold|정밀도]]↑)는 실수는 없지만 빠른 대응을 못 할 수 있다. 빠르게 많은 수를 두는 기사([[092_recall_sensitivity_hit_rate|재현율]]↑)는 공격적이지만 실수도 많다 — 최고의 기사는 이 둘의 균형을 잡는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]) | TP/(TP+[[293_fp_function_point|FP]]), [[293_fp_function_point|FP]] [[656_ir_containment|억제]] / [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 기반 [[282_performance_tactics|성능]] 지표 |
| [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]) | TP/(TP+FN), FN [[656_ir_containment|억제]] / [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 트레이드오프 [[083_relationship_in_er_model|관계]] |
| 임계값(Threshold) | [[130_probability|확률]] 판정 기준, 조정 / [[233_precision_recall_f1_roc_auc_threshold|정밀도]]-[[092_recall_sensitivity_hit_rate|재현율]] 균형 조절 |
| [[255_f1_score|F1-Score]] | 조화평균, 균형 지표 / [[233_precision_recall_f1_roc_auc_threshold|정밀도]]·[[092_recall_sensitivity_hit_rate|재현율]] 통합 |
| Fβ-Score | β값으로 중요도 가중 / [[064_relation_domain|도메인]] 맞춤 평가 |
| AUPRC | [[067_pull_request_pr_merge_request_code_review|PR]] 곡선 면적 / 불균형 [[001_dikw_pyramid|데이터]] 종합 평가 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [정밀도 (Precision)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 **"내가 맞다고 한 것 중 실제로 맞은 비율"**이에요.
2. "이 사람이 나쁜 사람이야!"라고 100번 말했는데 85번만 맞았으면 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 85%예요.
3. [[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 낮으면 억울한 사람이 많아지니까, 특히 법이나 의료처럼 중요한 곳에서는 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 꼭 높여야 해요!
