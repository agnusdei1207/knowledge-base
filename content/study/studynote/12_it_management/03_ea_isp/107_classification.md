+++
weight = 107
title = "107. 소셜 네트워크 분석 (SNA) — 중심성 / 커뮤니티 탐지 / 영향력"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[104_classification_analysis|분류]] (Classification)는 과거의 [[001_dikw_pyramid|데이터]] 패턴(입력 X)과 정답 레이블(출력 Y)의 관계를 학습하여, 새롭게 주어지는 미지의 [[001_dikw_pyramid|데이터]]가 어떤 범주에 속하는지 예측하는 기계 학습(Machine [[240_switch_learning_forwarding_flooding|Learning]]) [[001_algorithm_definition|알고리즘]]이다.
> 2. **가치**: 스팸 메일 필터링, 신용카드 사기 탐지, 고객 이탈 예측 등 비즈니스에서 발생하는 "예/아니오" 또는 "다중 선택"의 의사결정을 인간의 개입 없이 빠르고 정확하게 자동화할 수 있다.
> 3. **판단 포인트**: 실무에서는 단일 [[001_algorithm_definition|알고리즘]]([[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]], 의사결정 나무 등)보다 예측 [[282_performance_tactics|성능]]이 압도적인 [[257_ensemble_learning|앙상블]] 모델인 XGBoost (Extreme [[034_gradient_boosting|Gradient Boosting]]) 등을 기본으로 채택하되, 클래스 불균형 문제를 반드시 보정해야 한다.

---

## Ⅰ. 개요 및 필요성

[[104_classification_analysis|분류]] (Classification)는 [[231_ai_turing_test|인공지능]] 분야의 [[121_supervised_learning|지도 학습]]([[121_supervised_learning|Supervised Learning]]) 중 가장 대표적인 문제 해결 방식이다. 연속적인 수치를 예측하는 회귀(Regression)와 달리, [[104_classification_analysis|분류]]는 [[001_dikw_pyramid|데이터]]를 미리 정의된 불연속적인 범주(클래스)로 나누는 것이 목적이다. 

현대의 비즈니스 환경에서는 매일 수백만 건의 텍스트, 이미지, 거래 [[001_dikw_pyramid|데이터]]가 [[087_process_state_transition|생성]]된다. 사람이 일일이 이 [[001_dikw_pyramid|데이터]]가 정상인지 사기인지, 스팸인지 아닌지 판별하는 것은 물리적으로 불가능하다. 따라서 기계가 과거의 정답 [[001_dikw_pyramid|데이터]]를 바탕으로 복잡한 비선형적 패턴을 학습하여 스스로 범주를 할당하는 [[104_classification_analysis|분류]] [[001_algorithm_definition|알고리즘]]의 도입이 필수적이다.

- **📢 섹션 요약 비유**: [[104_classification_analysis|분류]]는 베테랑 우체국 직원이 편지봉투의 특징(우편번호, 글씨체)만 보고도 수천 통의 편지를 각 동네 바구니(범주)로 1초 만에 휙휙 던져넣는 자동 [[104_classification_analysis|분류]] 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[104_classification_analysis|분류]] [[001_algorithm_definition|알고리즘]]은 [[001_dikw_pyramid|데이터]]를 나누는 결정 경계(Decision Boundary)를 어떻게 형성하느냐에 따라 다양한 원리가 존재한다.

1. **[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]])**:
   [[001_dikw_pyramid|데이터]]의 선형 결합 결과를 [[268_sigmoid_vanishing_gradient|시그모이드]]([[268_sigmoid_vanishing_gradient|Sigmoid]]) 함수에 통과시켜 0과 1 사이의 확률값으로 변환한다. 확률이 0.5 이상이면 클래스 1로 [[104_classification_analysis|분류]]한다.
2. **결정 트리 ([[124_decision_tree|Decision Tree]])**:
   특성(Feature) 값에 따라 스무고개 하듯 if-else 규칙 분기를 만든다. 노드를 나눌 때는 정보 이득(Information Gain)이 최대화되는 기준을 선택한다.
3. **[[238_svm_margin_kernel_trick_naive_bayes|SVM]] ([[238_svm_margin_kernel_trick_naive_bayes|Support Vector Machine]])**:
   [[001_dikw_pyramid|데이터]]를 범주로 나누는 가장 여백(Margin)이 넓은 최적의 초평면을 그린다. [[059_kernel_trick_rbf_polynomial|커널 트릭]]([[059_kernel_trick_rbf_polynomial|Kernel Trick]])을 사용해 비선형 [[001_dikw_pyramid|데이터]]도 [[104_classification_analysis|분류]]할 수 있다.
4. **[[257_ensemble_learning|앙상블]] ([[257_ensemble_learning|Ensemble]])**:
   여러 개의 약한 [[104_classification_analysis|분류]]기를 결합하여 강력한 [[104_classification_analysis|분류]]기를 만드는 기법이다. 트리를 병렬로 만드는 [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]])나 순차적으로 오차를 보완하는 LightGBM (Light [[034_gradient_boosting|Gradient Boosting]] Machine)이 대표적이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                 [ 주요 분류 알고리즘의 결정 경계 ]          │
├─────────────────────────────────────────────────────────────┤
│ 1. Logistic Regression      2. Decision Tree                │
│       │   ●   ●             │ ┌───────┐ ┌───────┐         │
│     ● │ ●   ●               │ │   ●   │ │ ●   ● │         │
│  ─────┼──────── (선형)      │ └───────┘ └───────┘ (계단형)│
│   ▲   │   ▲                 │   ▲   ┌───────┐             │
│   ▲ ▲│                     │   ▲ ▲│   ▲   │             │
│                                                             │
│ 3. SVM (Kernel Trick)       4. Ensemble (Random Forest)     │
│       │     ●               │    복수의 결정 트리가 다수결로  │
│    ●  (  ●    )  (비선형)   │    투표하여 가장 안정적이고   │
│   ▲ ▲  \   ●               │    복잡한 비선형 경계를 형성  │
│   ▲   │   ▲                 │                               │
└─────────────────────────────────────────────────────────────┘
```

[[001_algorithm_definition|알고리즘]]이 모델을 학습한 후에는 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]])을 통해 예측값과 실제 정답을 교차 검증하여 [[282_performance_tactics|성능]]을 평가한다.

- **📢 섹션 요약 비유**: [[104_classification_analysis|분류]] [[001_algorithm_definition|알고리즘]]은 면접관과 같다. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 엑셀 점수만 보는 딱딱한 면접관, 결정 트리는 꼬리에 꼬리를 무는 질문을 던지는 면접관, [[257_ensemble_learning|앙상블]]은 100명의 면접관이 각자 점수를 매긴 뒤 다수결로 최종 합격을 결정하는 공정한 위원회다.

---

## Ⅲ. 비교 및 연결

[[104_classification_analysis|분류]] 문제를 다룰 때는 단일 모델과 [[257_ensemble_learning|앙상블]] 모델의 명확한 트레이드오프를 비교해야 하며, 평가지표의 특성을 이해하는 것이 중요하다.

| 비교 항목 | [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] / 의사결정 나무 | [[257_ensemble_learning|앙상블]] (XGBoost, LightGBM) |
| :--- | :--- | :--- |
| **설명력 (해석 가능성)** | 우수 (가중치와 분기 규칙을 사람에게 설명 가능) | 낮음 (블랙박스화되어 결과 도출 과정 설명이 어려움) |
| **[[282_performance_tactics|성능]] 및 복잡도** | 상대적으로 낮음 / 과적합 위험 높음 | 매우 높음 / 대용량 [[001_dikw_pyramid|데이터]]에서 압도적인 정확도 |
| **적용 [[064_relation_domain|도메인]]** | 금융/의료 등 설명 책임이 규제로 강제되는 분야 | 이미지, 텍스트 [[104_classification_analysis|분류]] 및 예측 정확도가 최우선인 분야 |

[[104_classification_analysis|분류]] [[282_performance_tactics|성능]]을 평가할 때 정확도(Accuracy)만을 신뢰해선 안 된다. 전체의 99%가 정상 거래인 **클래스 불균형** 상황에서는 "모두 정상"으로만 찍어도 정확도가 99%가 나오기 때문이다. 이때는 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]([[233_precision_recall_f1_roc_auc_threshold|Precision]]), [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]]), [[255_f1_score|F1 Score]], 그리고 AUC-ROC (Area Under the Curve - Receiver Operating Characteristic) 지표를 함께 비교해야 한다.

- **📢 섹션 요약 비유**: [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 이유를 명확하게 설명해주는 친절한 동네 의사라면, XGBoost는 이유는 설명 못 해도 병을 정확히 짚어내는 로봇 명의다. 병의 원인을 아는 게 중요하면 전자를, 당장 수술 여부를 맞추는 게 중요하면 후자를 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 현장에서 [[104_classification_analysis|분류]] 모델을 설계하고 배포할 때 기술사로서 판단해야 할 핵심 요소는 다음과 같다.

1. **클래스 불균형 (Class Imbalance) 보정**:
   - 사기 탐지처럼 소수 클래스를 맞추는 것이 핵심일 경우, 합성 소수 표본 [[087_process_state_transition|생성]] 기법인 [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] (Synthetic Minority Over-sampling Technique)를 쓰거나 [[001_algorithm_definition|알고리즘]] 내부에서 소수 클래스에 가중치를 주어야 한다.
2. **임계값 (Threshold) 튜닝**:
   - [[104_classification_analysis|분류]]기가 반환하는 확률의 기본 기준점은 0.5다. 하지만 암 환자를 놓치는 FN (False Negative)이 오진을 하는 [[293_fp_function_point|FP]] (False Positive)보다 훨씬 치명적이라면, 이 기준점을 0.3으로 낮춰 의심되면 바로 환자로 [[104_classification_analysis|분류]]하도록 전략적 조정을 해야 한다.
3. **설명 가능한 [[231_ai_turing_test|인공지능]] 도입**:
   - [[257_ensemble_learning|앙상블]] 모델을 신용 심사에 쓸 경우 [[227_xai_explainable_ai_lime_shap|XAI]] (eXplainable [[001_artificial_intelligence|Artificial Intelligence]]) 기법이 필요하다. [[327_shap|SHAP]] ([[327_shap|SHapley Additive exPlanations]])이나 [[326_lime|LIME]] (Local Interpretable Model-agnostic Explanations)을 결합하여 왜 [[104_classification_analysis|분류]]되었는지 설명할 수 있어야 한다.

- **📢 섹션 요약 비유**: 화재경보기를 설치할 때, 알람이 안 울려 집이 타는 것이 무서우면 담배 연기만 나도 울리게 임계값을 예민하게 맞춰야 하고, 자꾸 울려서 잠을 깨는 것이 싫다면 진짜 불꽃이 보일 때만 울리도록 세팅해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[104_classification_analysis|분류]] 모델의 도입은 단순한 업무 자동화를 넘어 비즈니스의 선제적 방어 체계와 공격적 마케팅을 가능하게 한다.

하지만 [[001_dikw_pyramid|데이터]] 분포가 시간에 따라 변하는 [[163_data_drift_statistical_distribution_shift|데이터 드리프트]]([[163_data_drift_statistical_distribution_shift|Data Drift]]) 현상이 발생하면 [[282_performance_tactics|성능]]은 급격히 하락한다. 결론적으로 훌륭한 [[104_classification_analysis|분류]] 시스템은 한 번 만들고 끝나는 것이 아니라, 최신 [[001_dikw_pyramid|데이터]]를 지속적으로 수집하고 모델을 재학습시키는 [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) 파이프라인과 함께 구축되어야 생명력을 얻는다.

- **📢 섹션 요약 비유**: [[104_classification_analysis|분류]] 시스템은 네비게이션과 같다. 처음엔 가장 빠른 길을 잘 [[104_classification_analysis|분류]]해 알려주지만, 실시간으로 바뀌는 도로 통제 상황(새로운 [[001_dikw_pyramid|데이터]])을 업데이트하지 않으면 결국 막히는 옛날 길로 운전자를 안내하게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[121_supervised_learning|지도 학습]] ([[121_supervised_learning|Supervised Learning]])** | [[104_classification_analysis|분류]] [[001_algorithm_definition|알고리즘]]이 성립하기 위해 반드시 정답 레이블이 존재하는 [[001_dikw_pyramid|데이터]]셋 |
| **의사결정 나무 ([[124_decision_tree|Decision Tree]])** | [[104_classification_analysis|분류]]를 위해 스무고개 형태의 규칙을 [[087_process_state_transition|생성]]하는 직관적인 화이트박스 모델 |
| **[[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] ([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]])** | TP, TN, [[293_fp_function_point|FP]], FN을 통해 [[104_classification_analysis|분류]] 모델이 어떤 종류의 에러를 냈는지 분석하는 표 |
| **[[163_data_drift_statistical_distribution_shift|데이터 드리프트]] ([[163_data_drift_statistical_distribution_shift|Data Drift]])** | 시간이 지나면서 입력 [[001_dikw_pyramid|데이터]]의 통계적 특성이 변해 [[104_classification_analysis|분류]] [[282_performance_tactics|성능]]이 떨어지는 현상 |

### 📈 관련 키워드 및 발전 흐름도

```text
분류 (Classification) 방법론의 진화
    │
    ▼
규칙 기반 분류 (인간이 직접 if-else 하드코딩)
    │
    ▼
통계/수학적 기계 학습 (Logistic Regression, SVM, Decision Tree)
    │
    ▼
앙상블 학습 (Random Forest, XGBoost, LightGBM - 다수결로 성능 극대화)
    │
    ▼
딥러닝 기반 분류 & XAI (신경망 도입 및 SHAP을 통한 결과 설명력 확보)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[104_classification_analysis|분류]]는 수많은 레고 블록을 보고 "빨간색 바구니"와 "파란색 바구니"로 나누어 담는 놀이예요.
2. 기계에게 "이게 빨간색이야"라고 정답을 여러 번 가르쳐주면, 나중에는 기계가 스스로 척척 바구니에 잘 넣게 된답니다.
3. 여러 명의 친구들([[257_ensemble_learning|앙상블]])이 모여서 "이건 빨간색이 맞아!"라고 다수결로 정하면 틀릴 확률이 훨씬 줄어들어요!
