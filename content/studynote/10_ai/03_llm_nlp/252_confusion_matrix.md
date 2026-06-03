---
title: 252. 혼동 행렬 (Confusion Matrix)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]], 오차 행렬)은 [[104_classification_analysis|분류]] 모델의 예측 결과를 **실제 정답과 비교하여 4가지 경우(TP, TN, [[293_fp_function_point|FP]], FN)로 세분화**한 [[282_performance_tactics|성능]] 분석 도구다.
> 2. **가치**: 단순 정확도(Accuracy)만으로는 클래스 불균형 문제를 감출 수 있으나, [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]은 어떤 유형의 오류가 발생하는지 정밀하게 드러내어 [[064_relation_domain|도메인]]에 맞는 평가 지표 선택을 가능하게 한다.
> 3. **판단 포인트**: [[293_fp_function_point|FP]](False Positive, 1종 오류)와 FN(False Negative, 2종 오류) 중 어느 것이 더 치명적인지에 따라 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]) 또는 [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])을 최우선 지표로 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정확도(Accuracy)만으로 부족한 이유

**극단적 클래스 불균형 예시:**
```
암 환자 진단 데이터: 양성(암) 1%, 음성(정상) 99%

"항상 음성으로 예측"하는 모델:
  정확도(Accuracy) = 99% ← 높아 보이지만!
  암 환자를 한 명도 찾지 못하는 쓸모없는 모델
```

→ 이런 상황에서 정확도는 오해를 유발. **[[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 기반 세부 지표 필수**

### 1.2 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]의 4가지 셀

| 구분 | 예측: Positive | 예측: Negative |
|:---|:---:|:---:|
| **실제: Positive** | TP (True Positive) | FN (False Negative) |
| **실제: Negative** | [[293_fp_function_point|FP]] (False Positive) | TN (True Negative) |

- **TP (True Positive)**: 실제 양성 → 양성으로 정확히 예측 ✅
- **TN (True Negative)**: 실제 음성 → 음성으로 정확히 예측 ✅
- **[[293_fp_function_point|FP]] (False Positive, 1종 오류)**: 실제 음성 → 양성으로 잘못 예측 ❌
- **FN (False Negative, 2종 오류)**: 실제 양성 → 음성으로 잘못 예측 ❌

- **📢 섹션 요약 비유**: [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]은 의사의 진단 성적표와 같다. 환자를 환자라고 맞힌 것(TP), 건강한 사람을 건강하다고 맞힌 것(TN), 건강한 사람을 환자라고 오진한 것([[293_fp_function_point|FP]]), 환자를 건강하다고 놓친 것(FN) — 이 네 가지가 의사의 실력을 정확히 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 전체 구조

```
┌──────────────────────────────────────────────────────────┐
│                   혼동 행렬 (Confusion Matrix)             │
│                                                          │
│              │  예측: Positive  │  예측: Negative  │      │
│  ────────────┼──────────────────┼──────────────────┤      │
│  실제: Pos.  │   TP (진양성)    │   FN (위음성)    │      │
│              │  (올바른 양성)   │ (2종 오류, 미검출)│      │
│  ────────────┼──────────────────┼──────────────────┤      │
│  실제: Neg.  │   FP (위양성)   │   TN (진음성)    │      │
│              │ (1종 오류, 과경보)│  (올바른 음성)   │      │
│  ────────────┴──────────────────┴──────────────────┘      │
│                                                          │
│  오류 유형:                                               │
│  FP = 1종 오류 (Type I Error) — 없는 것을 있다고 함       │
│  FN = 2종 오류 (Type II Error) — 있는 것을 없다고 함      │
└──────────────────────────────────────────────────────────┘
```

### 2.2 핵심 [[282_performance_tactics|성능]] 지표 계산

| 지표 | 수식 | 의미 |
|:---|:---|:---|
| **정확도(Accuracy)** | (TP+TN) / (TP+TN+[[293_fp_function_point|FP]]+FN) | 전체 중 올바른 예측 비율 |
| **[[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]])** | TP / (TP+[[293_fp_function_point|FP]]) | Positive 예측 중 실제 Positive 비율 |
| **[[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])** | TP / (TP+FN) | 실제 Positive 중 맞게 예측한 비율 |
| **[[255_f1_score|F1-Score]]** | 2 × (P×R)/(P+R) | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]의 조화평균 |
| **특이도(Specificity)** | TN / (TN+[[293_fp_function_point|FP]]) | 실제 Negative 중 맞게 예측한 비율 |

### 2.3 F1-Score의 의미

[[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]] 중 하나만 높여도 점수가 오르는 산술평균과 달리, 조화평균은 **둘 다 균형 있게 높아야** 높은 [[255_f1_score|F1-Score]] 달성:

```
정밀도=1.0, 재현율=0.0:
  산술평균 = 0.5      ← 높아 보임
  F1-Score = 0.0     ← 실제론 쓸모없음

정밀도=0.8, 재현율=0.8:
  산술평균 = 0.8
  F1-Score = 0.8     ← 균형잡힌 성능
```

- **📢 섹션 요약 비유**: F1-Score는 양 팔 힘이 다 좋아야 높은 점수를 받는 철봉 체력검사와 같다. 왼팔만 강하고 오른팔이 0이면 총점은 0에 가깝다 — 양쪽이 균형 있어야 진짜 강한 것이다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[293_fp_function_point|FP]] vs FN: 어떤 오류가 더 치명적인가?

| [[064_relation_domain|도메인]] | 더 치명적인 오류 | 최우선 지표 | 이유 |
|:---|:---|:---|:---|
| 암 진단 | FN (암 미검출) | [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]) ↑ | 환자를 놓치면 치명적 |
| 스팸 필터 | [[293_fp_function_point|FP]] (정상 메일을 스팸) | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]) ↑ | 중요 메일 차단 방지 |
| 사기 탐지 | FN (사기 미탐지) | [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]) ↑ | 사기를 놓치면 손실 |
| 광고 타기팅 | [[293_fp_function_point|FP]] (관심 없는 사용자) | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]) ↑ | 광고 비용 낭비 |
| 자율주행 장애물 | FN (장애물 미탐지) | [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]) ↑ | 충돌 사고 방지 |

### 3.2 클래스 불균형에서의 지표 선택

| 상황 | 문제 | 해결 |
|:---|:---|:---|
| 클래스 비율 95:5 | Accuracy 95%인 쓸모없는 모델 | [[255_f1_score|F1-Score]], AUROC 사용 |
| 양성 클래스 중요 | [[254_recall_sensitivity|Recall]] 극대화 | 임계값(Threshold) 낮춤 |
| 음성 오판 치명적 | [[233_precision_recall_f1_roc_auc_threshold|Precision]] 극대화 | 임계값(Threshold) 높임 |

### 3.3 ROC 곡선 (Receiver Operating Characteristic Curve)

임계값(Threshold)을 0~1로 변화시키며 FPR(False Positive Rate) vs TPR(True Positive Rate, [[092_recall_sensitivity_hit_rate|재현율]]) [[070_graph_datastructure|그래프]] 표시:
- **AUROC (Area Under [[256_roc_auc|ROC Curve]])**: 면적이 1에 가까울수록 우수한 [[104_classification_analysis|분류]]기
- 클래스 불균형에서도 안정적인 종합 평가 지표

- **📢 섹션 요약 비유**: 암 진단에서 FN(암 미검출)과 [[293_fp_function_point|FP]](정상인 오진) 중 FN이 훨씬 치명적이다. "놓친 암 환자"는 치료 기회를 잃지만, "과잉 검사"는 추가 검사로 해결할 수 있다. 따라서 암 진단 AI는 [[092_recall_sensitivity_hit_rate|재현율]]을 최우선 지표로 삼는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 실제 예시

**스팸 필터 (1000개 이메일 중 스팸 100개)**

| 구분 | 예측: 스팸 | 예측: 정상 | 합계 |
|:---|:---:|:---:|:---:|
| 실제: 스팸 | TP=85 | FN=15 | 100 |
| 실제: 정상 | [[293_fp_function_point|FP]]=[[489_raid_10_hybrid|10]] | TN=890 | 900 |
| 합계 | 95 | 905 | 1000 |

```
정확도 = (85+890)/1000 = 97.5%
정밀도 = 85/(85+10) = 89.5%
재현율 = 85/(85+15) = 85.0%
F1    = 2×(0.895×0.85)/(0.895+0.85) = 87.2%
```

### 4.2 임계값 (Threshold) 조정 효과

```
확률 출력 모델: P(스팸) = 0.65

임계값 = 0.5 → Positive 판정 (P > 0.5)
  → 더 많이 양성 판정 → 재현율↑, 정밀도↓

임계값 = 0.8 → Negative 판정 (P < 0.8)
  → 더 적게 양성 판정 → 정밀도↑, 재현율↓
```

### 4.3 기술사 핵심 판단 포인트
- **클래스 불균형 [[001_dikw_pyramid|데이터]]에서 정확도(Accuracy)만 보고하는 것은 오류**
- [[293_fp_function_point|FP]]/FN 오류 비용이 비대칭일 때 비용 민감 학습(Cost-Sensitive [[240_switch_learning_forwarding_flooding|Learning]]) 적용
- **다중 클래스 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]**: n×n 행렬로 확장, Macro/Micro/Weighted F1 사용

- **📢 섹션 요약 비유**: 임계값 조정은 보안 게이트의 민감도를 조절하는 것이다. 민감도를 높이면(임계값 낮춤) 수상한 사람을 더 많이 잡지만([[092_recall_sensitivity_hit_rate|재현율]]↑) 정상인도 자주 검사받고([[233_precision_recall_f1_roc_auc_threshold|정밀도]]↓), 민감도를 낮추면 반대가 된다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 활용 기대효과
- 오류 패턴 세밀 분석으로 모델 개선 방향 도출
- [[064_relation_domain|도메인]] 특성에 맞는 [[282_performance_tactics|성능]] 지표 선택
- 임계값 최적화를 통한 [[293_fp_function_point|FP]]/FN 균형 조절

### 5.2 결론
[[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]은 [[104_classification_analysis|분류]] 모델 [[282_performance_tactics|성능]]을 다각도로 분석하는 핵심 도구다. TP, TN, [[293_fp_function_point|FP]], FN의 4가지 경우를 이해하고, [[064_relation_domain|도메인]]의 오류 비용에 따라 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]·[[092_recall_sensitivity_hit_rate|재현율]]·[[255_f1_score|F1-Score]]·AUROC 중 적절한 지표를 선택하는 것이 실무와 기술사 시험 모두에서 핵심이다.

- **📢 섹션 요약 비유**: [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]은 야구 타자의 성적표다. 단순 타율(정확도)만 보면 안 되고 — 홈런(TP), 삼진(FN), 볼넷([[293_fp_function_point|FP]]), 아웃(TN) — 상황별 성적을 다 봐야 진짜 타자를 평가할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] | TP, TN, [[293_fp_function_point|FP]], FN / [[104_classification_analysis|분류]] [[282_performance_tactics|성능]] 분석 기반 도구 |
| [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]) | [[293_fp_function_point|FP]] 최소화, 스팸/광고 / TP/(TP+[[293_fp_function_point|FP]]) |
| [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]) | FN 최소화, 암 진단 / TP/(TP+FN) |
| [[255_f1_score|F1-Score]] | 조화평균, 균형 지표 / [[233_precision_recall_f1_roc_auc_threshold|Precision]]×[[254_recall_sensitivity|Recall]] 결합 |
| AUROC | ROC 곡선 면적, 임계값 독립 / 종합 [[104_classification_analysis|분류]] [[282_performance_tactics|성능]] 지표 |
| 임계값(Threshold) | [[233_precision_recall_f1_roc_auc_threshold|정밀도]]-[[092_recall_sensitivity_hit_rate|재현율]] 트레이드오프 / [[293_fp_function_point|FP]]/FN 균형 조절 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [혼동 행렬 (Confusion Matrix)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]은 **받아쓰기 성적표**예요 — 맞힌 것(TP, TN)과 틀린 것([[293_fp_function_point|FP]], FN)을 4가지로 나눠요.
2. 암 진단처럼 "환자를 놓치면 안 되는" 경우에는 FN이 없어야 하고, 스팸 필터처럼 "멀쩡한 메일을 차단하면 안 되는" 경우에는 FP가 없어야 해요.
3. F1-Score는 이 두 가지 실수를 균형 있게 잘하는지 알려주는 종합 성적표예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 252 / 420

← **이전**: [[251_grid_search_random_search|251. 그리드 서치 (Grid Search) / 랜덤 서치 (Random Search)]]
**다음**: [[253_precision|253. 정밀도 (Precision)]] →

---
