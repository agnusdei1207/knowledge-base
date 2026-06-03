---
title: 231. SMOTE (Synthetic Minority Over-sampling Technique) 불균형 데이터 증강
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SMOTE(Synthetic Minority Over-[[056_표본화_Sampling|sampling]] Technique)는 소수 클래스 샘플 간 [[352_knn_distance_metrics|k-NN]](k-Nearest Neighbor) 보간([[187_time_series_interpolation_rollup_dashboard|Interpolation]])으로 합성 [[001_dikw_pyramid|데이터]]를 [[087_process_state_transition|생성]]해 클래스 불균형(Class Imbalance)을 해소한다.
> 2. **가치**: 사기 탐지·의료 진단처럼 소수 클래스가 핵심인 [[064_relation_domain|도메인]]에서 모델이 다수 클래스에 편향되는 문제를 근본적으로 차단하고 [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])을 극적으로 개선한다.
> 3. **판단 포인트**: 불균형 비율·[[247_feature_label_variables|피처]] 공간 특성·과적합 위험에 따라 SMOTE 변형 선택 및 언더샘플링(UnderSampling) 조합 여부를 결정하며, [[001_dikw_pyramid|Data]] Leakage 방지를 위해 반드시 훈련 [[001_dikw_pyramid|데이터]]에만 적용한다.

## Ⅰ. 개요 및 필요성

### 클래스 불균형 (Class Imbalance) 문제

실세계 [[001_dikw_pyramid|데이터]]는 대부분 클래스 비율이 심각하게 불균형하다.

| [[064_relation_domain|도메인]] | 다수 클래스 비율 | 소수 클래스 비율 |
|:---|:---:|:---:|
| 신용카드 사기 탐지 | 99.8% (정상 거래) | 0.2% (사기 거래) |
| 암 진단 | 95% (음성) | 5% (양성) |
| 네트워크 침입 탐지 | 99% (정상 트래픽) | 1% (공격 트래픽) |
| 제조 불량 검출 | 98% (양품) | 2% (불량품) |

이러한 불균형 [[001_dikw_pyramid|데이터]]를 그대로 학습하면 모델이 다수 클래스만 예측해도 높은 정확도(Accuracy)를 달성한다. 사기 탐지에서 무조건 "정상"이라 예측해도 99.8% 정확도가 나오지만, 소수 클래스(사기)를 전혀 탐지하지 못해 비즈니스적으로는 완전히 무용한 모델이 된다.

### [[356_imbalanced_data_sampling|불균형 데이터 처리]] [[268_strategy_pattern|전략]] [[104_classification_analysis|분류]]

```
불균형 데이터 처리 전략
├── 데이터 수준 (Data-Level)
│   ├── 오버샘플링 (OverSampling)  ← 소수 클래스 증가
│   │   ├── 무작위 오버샘플링 (Random OverSampling)
│   │   └── SMOTE / ADASYN / BorderlineSMOTE
│   └── 언더샘플링 (UnderSampling) ← 다수 클래스 감소
│       ├── 무작위 언더샘플링 (Random UnderSampling)
│       └── Tomek Links / ENN (Edited Nearest Neighbour)
├── 알고리즘 수준 (Algorithm-Level)
│   ├── 비용 민감 학습 (Cost-Sensitive Learning)
│   └── 앙상블 (Ensemble): BalancedBagging, EasyEnsemble
└── 평가 수준 (Evaluation-Level)
    └── Accuracy 대신 F1 · AUC · G-Mean 사용
```

📢 **섹션 요약 비유**: 클래스 불균형은 마치 100명의 반 학생 중 1명만 빨간 옷을 입은 상황이다. 선생님이 "모두 파란 옷"이라 해도 99%가 맞아 보이지만, 빨간 옷을 찾는 임무는 완전히 실패한다.

## Ⅱ. 아키텍처 및 핵심 원리

### SMOTE 합성 샘플 [[087_process_state_transition|생성]] 원리

SMOTE는 소수 클래스 샘플 간 [[038_knn|k-최근접 이웃]]([[352_knn_distance_metrics|k-NN]], k-Nearest Neighbor)을 이용해 보간([[187_time_series_interpolation_rollup_dashboard|Interpolation]]) 방식으로 새로운 합성 샘플을 만든다.

**[[087_process_state_transition|생성]] 공식:**
```
x_new = x_i + λ × (x_nn - x_i)

여기서:
  x_i   = 소수 클래스 임의 샘플
  x_nn  = x_i의 k-NN 중 무작위 선택된 이웃
  λ     = [0, 1] 범위의 난수 (균등 분포)
```

### SMOTE 샘플 [[087_process_state_transition|생성]] 과정 ([[103_ascii|ASCII]] 다이어그램)

```
피처 공간 (Feature Space)

  F2
   │
 5 │    ○         ○
   │       ○
 4 │    ●            ○
   │       ★
 3 │          ●
   │       ★
 2 │    ○      ●
   │
 1 │    ○         ○
   └────────────────── F1
        1    2    3

  ● = 소수 클래스 원본 (3개)
  ★ = SMOTE 합성 샘플 (보간점, 2개)
  ○ = 다수 클래스 원본

  x_new = ● + λ × (인접● - ●)
  → 두 ● 사이 선분 위의 임의 점을 새 샘플로 생성
```

### SMOTE 변형 [[001_algorithm_definition|알고리즘]] 비교

| [[001_algorithm_definition|알고리즘]] | 핵심 아이디어 | 장점 | 단점 |
|:---|:---|:---|:---|
| **SMOTE** | [[352_knn_distance_metrics|k-NN]] 이웃 간 선형 보간 | 단순·검증됨 | 경계선 근처 노이즈 샘플 [[087_process_state_transition|생성]] 가능 |
| **ADASYN** (Adaptive Synthetic [[056_표본화_Sampling|Sampling]]) | [[104_classification_analysis|분류]] 어려운 샘플에 더 많이 [[087_process_state_transition|생성]] | 어려운 경계 집중 학습 | 과도한 노이즈 증폭 위험 |
| **Borderline-SMOTE** | 경계선 근처 소수 샘플만 선택 | 결정 경계 강화 | 경계 샘플 부족 시 효과 ↓ |
| **[[238_svm_margin_kernel_trick_naive_bayes|SVM]]-SMOTE** | [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 서포트 벡터 주변 샘플 [[087_process_state_transition|생성]] | 고차원 효과적 | 계산 비용 높음 |
| **SMOTENC** | 범주형+수치형 혼합 [[001_dikw_pyramid|데이터]] 처리 | 실무 [[001_dikw_pyramid|데이터]] 적합 | 인코딩 [[009_config|설정]] 복잡 |

### 언더샘플링 (UnderSampling) vs 오버샘플링 ([[096_oversampling_smote|OverSampling]])

```
┌─────────────────────────────────────────────────────────────┐
│              데이터 불균형 해소 전략 비교                       │
├──────────────────┬───────────────────┬─────────────────────┤
│   구분           │   언더샘플링       │    오버샘플링        │
├──────────────────┼───────────────────┼─────────────────────┤
│ 방향             │ 다수 클래스 ↓      │ 소수 클래스 ↑       │
│ 데이터 크기      │ 감소 (학습 빠름)   │ 증가 (학습 느림)    │
│ 정보 손실        │ 있음 (위험)        │ 없음                │
│ 과적합 위험      │ 낮음              │ 높음 (단순 복제 시) │
│ 권장 상황        │ 데이터 충분        │ 데이터 희귀         │
│ 대표 기법        │ Tomek Links, ENN  │ SMOTE, ADASYN       │
└──────────────────┴───────────────────┴─────────────────────┘
```

📢 **섹션 요약 비유**: SMOTE는 두 점 사이에 점을 찍는 것이다. 빨간 공 두 개 사이에 새 빨간 공을 놓아 "비슷하지만 완전히 같지 않은" 새 예시를 만드는 것과 같다.

## Ⅲ. 비교 및 연결

### 평가 지표 선택 주의사항

불균형 [[001_dikw_pyramid|데이터]]에서 Accuracy는 사용하면 안 된다. 올바른 지표 선택이 핵심이다.

| 지표 | 공식 | 불균형 적합성 | 비고 |
|:---|:---|:---:|:---|
| Accuracy (정확도) | (TP+TN) / 전체 | ❌ 부적합 | 다수 클래스 편향 |
| [[233_precision_recall_f1_roc_auc_threshold|Precision]] ([[233_precision_recall_f1_roc_auc_threshold|정밀도]]) | TP / (TP+[[293_fp_function_point|FP]]) | ✅ | 오탐([[293_fp_function_point|FP]]) 비용 높을 때 |
| [[254_recall_sensitivity|Recall]] ([[092_recall_sensitivity_hit_rate|재현율]]) | TP / (TP+FN) | ✅ | 미탐(FN) 비용 높을 때 |
| [[255_f1_score|F1 Score]] | 2×P×R / (P+R) | ✅ | P·R 균형 필요 시 |
| ROC-AUC | ROC 곡선 아래 면적 | ✅ | 전체 임계값 [[282_performance_tactics|성능]] |
| G-Mean | √(Recall_pos × Recall_neg) | ✅✅ | 심각한 불균형 시 최선 |
| [[067_pull_request_pr_merge_request_code_review|PR]]-AUC | [[067_pull_request_pr_merge_request_code_review|PR]] 곡선 아래 면적 | ✅✅ | 소수 클래스 [[282_performance_tactics|성능]] 집중 |

### SMOTE 적용 시 [[001_dikw_pyramid|Data]] Leakage 방지

```
❌ 잘못된 적용 (Data Leakage 발생):
   전체 데이터 → SMOTE → 훈련/테스트 분할
   (테스트 데이터에 합성 샘플 유입 → 평가 결과 부풀려짐)

✅ 올바른 적용:
   전체 데이터 → 훈련/테스트 분할 → 훈련 데이터에만 SMOTE
   (테스트 데이터는 반드시 원본 유지 → 공정한 평가)

✅ 파이프라인 적용 (sklearn Pipeline):
   Pipeline([
     ('smote', SMOTE()),
     ('model', XGBClassifier())
   ])
   → cross_val_score로 CV 수행 시 각 폴드 내에서만 SMOTE 적용
```

📢 **섹션 요약 비유**: 시험 문제를 미리 알고 공부(테스트에 SMOTE 적용)하면 점수가 높아 보이지만 실력이 아니다. 공부할 때(훈련 [[001_dikw_pyramid|데이터]])만 연습 문제를 늘려야 진짜 실력이 오른다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 불균형 처리 파이프라인

```
┌───────────────────────────────────────────────────────────────┐
│                  불균형 데이터 처리 파이프라인                    │
│                                                               │
│  원시 데이터     EDA          전처리       SMOTE    모델 학습   │
│  [Raw Data] → [불균형    → [결측치    → [합성   → [학습]      │
│               비율 분석]    처리·정규화]   샘플생성]            │
│                  ↓                          ↓                 │
│              불균형비율                 훈련 데이터만           │
│              측정 (1%?)               (테스트 제외)            │
│                                                               │
│  평가: F1 · AUC · PR-AUC 중심 (Accuracy 배제)                 │
└───────────────────────────────────────────────────────────────┘
```

### 기술사 판단 포인트

1. **비율 [[489_raid_10_hybrid|10]]:1 이하**: 단순 클래스 [[267_weight_bias_activation|가중치]](class_weight='balanced') 조정으로 충분
2. **비율 100:1 이상**: SMOTE + 언더샘플링 조합(SMOTEENN, SMOTETomek) 권장
3. **고차원 [[001_dikw_pyramid|데이터]]**: SMOTE 직전 [[163_pca|PCA]]([[163_pca|Principal Component Analysis]]) [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 권장
4. **범주형 [[247_feature_label_variables|피처]] 혼합**: SMOTENC 또는 인코딩 후 표준 SMOTE 적용
5. **실시간 추론 시스템**: 학습 시만 SMOTE, 추론 파이프라인에는 미적용

📢 **섹션 요약 비유**: 요리 연습(훈련)할 때는 재료를 다양하게 써도 되지만, 실제 손님 음식(테스트)에는 정해진 레시피대로만 만들어야 진짜 실력을 알 수 있다.

## Ⅴ. 기대효과 및 결론

### 기법별 [[282_performance_tactics|성능]] 비교 (불균형비율 100:1 기준, 소수 클래스 기준)

| 접근 방식 | [[254_recall_sensitivity|Recall]] (소수) | [[233_precision_recall_f1_roc_auc_threshold|Precision]] (소수) | [[255_f1_score|F1 Score]] |
|:---|:---:|:---:|:---:|
| 불균형 그대로 학습 | 0.05 | 0.90 | 0.09 |
| 무작위 오버샘플링 | 0.65 | 0.52 | 0.58 |
| SMOTE 단독 적용 | 0.78 | 0.71 | 0.74 |
| SMOTE + ENN 조합 | 0.82 | 0.76 | 0.79 |
| ADASYN 적용 | 0.80 | 0.68 | 0.74 |

### 결론

SMOTE는 클래스 불균형 문제 해결의 사실상 표준 기법이지만 만능이 아니다. [[247_feature_label_variables|피처]] 공간 특성, 불균형 비율, 과적합 위험을 종합 고려해 적합한 변형 [[001_algorithm_definition|알고리즘]]과 언더샘플링 조합을 선택해야 한다. 무엇보다 Accuracy가 아닌 F1·AUC·[[067_pull_request_pr_merge_request_code_review|PR]]-AUC 기반 평가가 필수이며, [[001_dikw_pyramid|Data]] Leakage 방지를 위해 학습/평가 분리 파이프라인 설계가 선행되어야 한다.

📢 **섹션 요약 비유**: SMOTE는 시험 공부할 때 핵심 유형 문제를 더 많이 만들어 연습하는 것이다. 단, 실제 시험([[444_test_data_management|테스트 데이터]])에는 그 연습 문제가 들어가면 안 된다—그건 답 알려주는 것과 같으니까.

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 문제 원인 | 클래스 불균형 (Class Imbalance) | 소수 클래스가 과소 대표되는 현상 |
| 핵심 해법 | SMOTE | 소수 클래스 [[352_knn_distance_metrics|k-NN]] 보간 합성 샘플 [[087_process_state_transition|생성]] |
| 변형 [[001_algorithm_definition|알고리즘]] | ADASYN | 어려운 경계 근처 집중 [[087_process_state_transition|생성]] |
| 변형 [[001_algorithm_definition|알고리즘]] | Borderline-SMOTE | 결정 경계 강화 [[288_version_ihl_tos_total_length|버전]] |
| 반대 방향 해법 | 언더샘플링 (UnderSampling) | 다수 클래스 제거로 균형 달성 |
| 조합 기법 | SMOTEENN / SMOTETomek | 오버+언더샘플링 하이브리드 |
| 평가 지표 | [[067_pull_request_pr_merge_request_code_review|PR]]-AUC / F1 / G-Mean | 불균형 [[001_dikw_pyramid|데이터]] 핵심 지표 |
| 주의사항 | [[001_dikw_pyramid|Data]] Leakage | [[444_test_data_management|테스트 데이터]]에 SMOTE 적용 금지 |

### 👶 어린이를 위한 3줄 비유 설명

1. 반에 100명 중 파란 옷 99명, 빨간 옷 1명이 있는데, AI가 "모두 파란 옷"이라 해도 99%가 맞아 보이지만 빨간 옷을 찾는 임무는 완전히 실패한다.

### 📈 관련 키워드 및 발전 흐름도

```text
클래스 불균형 데이터 (소수 클래스 탐지 실패)
    │
    ▼
오버샘플링: SMOTE · ADASYN · BorderlineSMOTE
언더샘플링: RandomUnder · NearMiss · Tomek Links
    │
    ▼
비용 민감 학습 · 임계값 조정 · Focal Loss
    │
    ▼
데이터 증강 (이미지: Augmentation · 텍스트: Back Translation)
```
2. SMOTE는 빨간 옷 아이 두 명 사이에 "비슷하게 생긴 새 빨간 옷 아이"를 만들어줘서 AI가 빨간 옷의 특징을 더 잘 배우게 해준다.
3. 단, 시험 볼 때(테스트)는 진짜 빨간 옷 아이만 써야 한다—연습용 가짜 아이를 시험에 쓰면 점수가 부풀려지는 속임수가 된다.
