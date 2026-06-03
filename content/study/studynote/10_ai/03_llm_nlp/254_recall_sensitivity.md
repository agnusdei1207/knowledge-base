+++
weight = 254
title = "254. 재현율 (Recall) / 민감도"
date = "2026-05-09"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[092_recall_sensitivity_hit_rate|재현율]](Recall)은 실제 Positive 중 모델이 올바르게 Positive로 예측한 비율 — FN(False Negative)을 최소화하는 지표.
> 2. **가치**: 암 진단·사기 탐지처럼 "놓치면 안 되는" 상황에서 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]보다 [[092_recall_sensitivity_hit_rate|재현율]]을 우선시해야 한다.
> 3. **판단 포인트**: 임계값(Threshold)을 낮추면 [[092_recall_sensitivity_hit_rate|재현율]]이 오르지만 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 떨어지는 트레이드오프를 반드시 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

[[092_recall_sensitivity_hit_rate|재현율]](Recall)은 **실제 Positive 샘플 중 모델이 Positive로 맞게 예측한 비율**을 측정하는 평가 지표다. 의학 통계에서는 동일한 개념을 **민감도(Sensitivity)**라고 부른다.

$$\text{Recall} = \frac{TP}{TP + FN}$$

- **TP(True Positive)**: 실제 Positive이고, 모델도 Positive로 예측한 경우
- **FN(False Negative)**: 실제 Positive이지만, 모델이 Negative로 잘못 예측한 경우

[[092_recall_sensitivity_hit_rate|재현율]]이 중요한 대표 사례:

| [[064_relation_domain|도메인]] | 문제 | 놓쳤을 때 결과 |
|:---|:---|:---|
| 암 진단 | 암 환자를 정상으로 [[104_classification_analysis|분류]] | 치료 기회 상실 (생명 위협) |
| 금융 사기 탐지 | 사기 거래를 정상으로 [[104_classification_analysis|분류]] | 금전 피해 발생 |
| [[589_virus|바이러스]] 검역 | 감염자를 미검출 | 전파 위험 증가 |
| 자율주행 | 보행자를 미탐지 | 사고 위험 |

이처럼 **FN 비용이 [[293_fp_function_point|FP]] 비용보다 압도적으로 큰 경우** [[092_recall_sensitivity_hit_rate|재현율]]을 최우선 지표로 삼는다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[092_recall_sensitivity_hit_rate|재현율]]은 "그물로 고기를 얼마나 많이 건졌나"다. 그물 구멍이 커서 고기를 놓치면(FN) 큰일 나는 상황에서 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] ([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]])과 [[092_recall_sensitivity_hit_rate|재현율]] 위치

```
              ┌────────────────────────────────────────────────┐
              │           예측값 (Predicted)                   │
              │       Positive         Negative                │
 ┌────────────┼───────────────────────┬────────────────────────┤
 │ 실  Pos    │  TP (True Positive)   │  FN (False Negative)   │
 │ 제         │  ← 재현율 분자        │  ← 재현율 분모에 포함  │
 │ 값 ────────┼───────────────────────┼────────────────────────┤
 │ (A Neg    │  FP (False Positive)  │  TN (True Negative)    │
 │  ct)       │                       │                        │
 └────────────┴───────────────────────┴────────────────────────┘

  Recall(재현율) = TP / (TP + FN)     ← 행 기준 (실제 Pos 행)
  Precision(정밀도) = TP / (TP + FP)  ← 열 기준 (예측 Pos 열)
  Specificity(특이도) = TN / (TN + FP) ← 실제 Neg 행
```

### 특이도(Specificity)와 비교

**특이도(Specificity)**는 실제 Negative 중 모델이 올바르게 Negative로 예측한 비율이다.

$$\text{Specificity} = \frac{TN}{TN + [[293_fp_function_point|FP]]}$$

| 지표 | 분모 | 목적 |
|:---|:---|:---|
| [[092_recall_sensitivity_hit_rate|재현율]] / 민감도 (Sensitivity) | 실제 Positive 전체 | FN 최소화 |
| 특이도 (Specificity) | 실제 Negative 전체 | [[293_fp_function_point|FP]] 최소화 |
| [[233_precision_recall_f1_roc_auc_threshold|정밀도]] ([[233_precision_recall_f1_roc_auc_threshold|Precision]]) | 예측 Positive 전체 | [[293_fp_function_point|FP]] 최소화 |
| 정확도 (Accuracy) | 전체 샘플 | 전반적 [[282_performance_tactics|성능]] |

### 임계값과 [[092_recall_sensitivity_hit_rate|재현율]]의 [[083_relationship_in_er_model|관계]]

이진 [[104_classification_analysis|분류]]기는 내부적으로 [[130_probability|확률]]값을 출력하고, 임계값(Threshold)에 따라 Positive/Negative를 결정한다.

```
 임계값 낮춤  ──────────────────────────►  임계값 높임

 재현율 ↑  ◄────────── Threshold ──────────► 재현율 ↓
 정밀도 ↓  ◄────────── 조정 효과 ──────────► 정밀도 ↑
```

- 임계값을 0.3으로 낮추면: 더 많은 샘플을 Positive로 예측 → FN 감소 → Recall 상승
- 임계값을 0.7로 높이면: Positive 예측이 신중해짐 → [[293_fp_function_point|FP]] 감소 → [[233_precision_recall_f1_roc_auc_threshold|Precision]] 상승

- **📢 섹션 요약 비유**: 공항 보안 검색대에서 "조금이라도 의심되면 검사"하면 [[092_recall_sensitivity_hit_rate|재현율]]이 높아지지만 멀쩡한 여행자도 많이 잡아내게([[293_fp_function_point|FP]]) 된다.

---

## Ⅲ. 비교 및 연결

### [[233_precision_recall_f1_roc_auc_threshold|정밀도]]-[[092_recall_sensitivity_hit_rate|재현율]] 트레이드오프 ([[233_precision_recall_f1_roc_auc_threshold|Precision]]-Recall Tradeoff)

[[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]])와 [[092_recall_sensitivity_hit_rate|재현율]](Recall)은 반비례 [[083_relationship_in_er_model|관계]]에 있다. 이를 동시에 높이는 것은 불가능하며, 업무 목적에 따라 균형점을 결정해야 한다.

```
  Precision
     1.0 ┤ ●
         │  ╲
     0.8 ┤   ╲
         │    ╲
     0.6 ┤     ╲  (이상적 PR 곡선은
         │      ╲  오른쪽 위로 볼록)
     0.4 ┤       ╲
         │        ●
     0.0 ┼────────────── Recall
         0.0  0.5  1.0
```

| 상황 | 우선 지표 | 이유 |
|:---|:---|:---|
| 암 진단 스크리닝 | Recall ↑ | FN 비용이 치명적 |
| 스팸 필터 | [[233_precision_recall_f1_roc_auc_threshold|Precision]] ↑ | [[293_fp_function_point|FP]](정상 메일 차단)가 불편 |
| 신용카드 사기 | Recall ↑ | 사기 놓치는 것이 더 위험 |
| 콘텐츠 추천 | [[233_precision_recall_f1_roc_auc_threshold|Precision]] ↑ | 관련 없는 추천이 신뢰 저하 |

### F1 스코어와의 연결

F1 스코어는 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]의 **조화 평균(Harmonic Mean)**으로 두 지표를 동시에 고려한다.

$$F1 = \frac{2 \times \text{[[233_precision_recall_f1_roc_auc_threshold|Precision]]} \times \text{Recall}}{\text{[[233_precision_recall_f1_roc_auc_threshold|Precision]]} + \text{Recall}}$$

- **📢 섹션 요약 비유**: [[233_precision_recall_f1_roc_auc_threshold|정밀도]]는 "쐈을 때 얼마나 명중하는가", [[092_recall_sensitivity_hit_rate|재현율]]은 "과녁을 얼마나 빠짐없이 맞히는가"다. 좋은 저격수는 둘 다 높아야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 임상 진단 시스템 설계 사례

암 검진 AI를 설계할 때 모델 임계값 결정 [[268_strategy_pattern|전략]]:

1. **1차 스크리닝**: Recall을 최대한 높여 잠재 환자를 모두 탐지 (임계값 ↓)
2. **2차 확진**: 1차 통과자 중 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]가 높은 모델로 재검사 (임계값 ↑)

이 2단계 접근으로 전체적인 FN과 FP를 동시에 관리한다.

### 기술사 답안 포인트

- **문제가 "[[092_recall_sensitivity_hit_rate|재현율]] 개선 방법"을 물을 때**: ① 임계값 하향 ② 오버샘플링([[231_smote_oversampling_class_imbalance_augmentation|SMOTE]])으로 소수 클래스 강화 ③ 클래스 [[267_weight_bias_activation|가중치]](Class [[267_weight_bias_activation|Weight]]) 조정 ④ [[257_ensemble_learning|앙상블]] 강화
- **"민감도와 특이도의 [[083_relationship_in_er_model|관계]]"를 물을 때**: ROC 곡선이 (FPR, TPR) 평면에 그려지는 원리와 연결
- **불균형 [[001_dikw_pyramid|데이터]]셋**: 클래스 불균형 시 정확도(Accuracy)는 무의미—[[092_recall_sensitivity_hit_rate|재현율]]과 F1으로 평가

- **📢 섹션 요약 비유**: [[092_recall_sensitivity_hit_rate|재현율]] 개선은 "체를 더 촘촘하게 만드는 것"이다. 더 많이 걸러낼수록 잡동사니([[293_fp_function_point|FP]])도 많이 걸리지만, 놓치는 것(FN)은 줄어든다.

---

## Ⅴ. 기대효과 및 결론

[[092_recall_sensitivity_hit_rate|재현율]](Recall / Sensitivity)을 올바르게 이해하고 활용하면:

1. **[[064_relation_domain|도메인]] 적합 모델 평가**: FN 비용이 높은 의료·보안 분야에서 적절한 지표 선택
2. **임계값 최적화**: 비즈니스 요구사항에 맞는 Threshold 조정으로 실질적 가치 창출
3. **트레이드오프 명시**: [[092_recall_sensitivity_hit_rate|재현율]]과 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 중 어느 쪽을 희생하는지 [[173_stakeholder_identification_impact_matrix|이해관계자]]와 투명하게 소통
4. **다중 지표 체계**: Recall, [[233_precision_recall_f1_roc_auc_threshold|Precision]], F1, AUC를 조합한 종합 평가 체계 구축

기술사 시험에서 [[092_recall_sensitivity_hit_rate|재현율]]은 반드시 **[[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] → 수식 → 트레이드오프 → [[064_relation_domain|도메인]]별 우선순위** 순서로 설명하는 것이 고득점 [[268_strategy_pattern|전략]]이다.

- **📢 섹션 요약 비유**: [[092_recall_sensitivity_hit_rate|재현율]]은 의사가 "의심 증상이 있으면 일단 검사부터"라고 판단하는 것과 같다. 놓치는 환자가 없도록 그물을 촘촘히 치되, 과잉 진단 비용과의 균형을 항상 고려해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[092_recall_sensitivity_hit_rate|재현율]] (Recall) | TP, FN, 민감도(Sensitivity) / 실제 Pos 탐지율 |
| [[233_precision_recall_f1_roc_auc_threshold|정밀도]] ([[233_precision_recall_f1_roc_auc_threshold|Precision]]) | TP, [[293_fp_function_point|FP]] / 예측 Pos [[002_bigdata_5v|정확성]] |
| 특이도 (Specificity) | TN, [[293_fp_function_point|FP]] / 실제 Neg 탐지율 |
| F1 스코어 ([[255_f1_score|F1-Score]]) | 조화 평균(Harmonic Mean) / [[233_precision_recall_f1_roc_auc_threshold|Precision]]·Recall 균형 |
| ROC 곡선 ([[256_roc_auc|ROC Curve]]) | TPR, FPR, AUC / 임계값별 [[282_performance_tactics|성능]] [[003_bigdata_7v|시각화]] |
| 임계값 (Threshold) | 이진 [[104_classification_analysis|분류]], [[130_probability|확률]] 출력 / Recall/[[233_precision_recall_f1_roc_auc_threshold|Precision]] 조정 레버 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [재현율 (Recall) / 민감도] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 선생님이 반에서 감기 걸린 아이를 찾는다고 해보자. [[092_recall_sensitivity_hit_rate|재현율]]은 감기 걸린 아이 중 실제로 찾아낸 비율이다.
2. 아이를 너무 조심스럽게 찾으면(높은 임계값) 몇 명을 놓치는데, 그게 FN이다.
3. 중요한 것을 놓치면 안 될 때는 좀 더 넓게 의심해서 다 잡아내는 [[268_strategy_pattern|전략]]이 바로 [[092_recall_sensitivity_hit_rate|재현율]]을 높이는 것!
