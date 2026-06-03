---
title: 분류 (Classification) 분석
date: '2024-03-20'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **범주 예측:** 입력된 [[001_dikw_pyramid|데이터]]의 특징(Feature)을 기반으로 해당 [[001_dikw_pyramid|데이터]]가 속할 미리 정의된 집단(Class/Label)을 판별하는 [[121_supervised_learning|지도 학습]]의 핵심.
- **결정 경계 (Decision Boundary):** 서로 다른 클래스를 가장 잘 구분하는 최적의 경계면을 수학적 [[001_algorithm_definition|알고리즘]]으로 찾아냄.
- **불균형 [[001_dikw_pyramid|데이터]] 대응:** 암 진단이나 사기 탐지처럼 정답 비율이 극히 낮은 경우엔 단순 정확도보다 [[092_recall_sensitivity_hit_rate|재현율]]([[254_recall_sensitivity|Recall]])과 F1-Score가 더 중요함.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **정의:** 이산적인 결과값(Yes/No, A/B/C)을 예측하는 기법으로, 비즈니스 영역에서 가장 광범위하게 쓰이는 분석 기퍼임.
- **활용 사례:** 스팸 메일 분류, 질병 유무 판독, 이탈 고객 예측, 이미지 객체 인식 등 무수히 많은 [[064_relation_domain|도메인]]에 적용됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **프로세스:** [[001_dikw_pyramid|데이터]] 수집 -> 전처리 -> 모델 선택 -> 학습(Fit) -> 평가(Score) -> 튜닝.
- **Bilingual [[103_ascii|ASCII]] Diagram:**
```text
[Classification Logic & Decision Boundary / 분류 로직 및 결정 경계]

   Feature Y (x2)
      ^
      |   Class A (O)    |    Class B (X)
      |         O   O    |    X     X
      |      O     O     |      X     X
      |   ---------------|----------------  <-- Optimal Boundary
      |          O   O   |   X     X
      |       O          |      X
      +---------------------------------------> Feature X (x1)

[Major Algorithms / 주요 알고리즘]
1. Logistic Regression: Probability-based (Sigmoid)
2. Decision Tree: Rule-based branching (If-Then)
3. SVM: Maximum Margin Hyperplane
4. Random Forest/Boosting: Ensemble of weak learners
```
- **평가 지표:** [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]]([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]]) 기반의 [[233_precision_recall_f1_roc_auc_threshold|Precision]], [[254_recall_sensitivity|Recall]], AUC-ROC.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] (Logistic) | 결정 트리 (Tree) | [[104_svm_support_vector_machine|서포트 벡터 머신]] ([[238_svm_margin_kernel_trick_naive_bayes|SVM]]) |
| :--- | :--- | :--- | :--- |
| **모델 구조** | 선형 결합 (Linear) | 계층적 분기 (Hierarchy) | 마진 최대화 (Margin) |
| **장점 (Pros)** | 결과 해석 용이 | [[001_dikw_pyramid|데이터]] 전처리 불필요 | 복잡한 [[001_dikw_pyramid|데이터]] 처리 강점 |
| **단점 (Cons)** | 선형 [[083_relationship_in_er_model|관계]]만 해석 가능 | 과적합([[245_overfitting_variance|Overfitting]]) 취약 | 학습 시간 및 자원 소모 |
| **비유 (Analogy)** | 찬성/반대 [[130_probability|확률]] 투표 | 스무고개 질문 | 안전 지대 확보하기 |
| **비고 (Note)** | 분류의 [[159_baseline_requirements_configuration_management|베이스라인]] | [[257_ensemble_learning|앙상블]]의 기본 단위 | 비선형 [[059_kernel_trick_rbf_polynomial|커널 트릭]] 활용 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **[[001_dikw_pyramid|데이터]] 불균형(Imbalance) 처리:** 실제 현업 [[001_dikw_pyramid|데이터]]는 대개 편향되어 있으므로 **[[231_smote_oversampling_class_imbalance_augmentation|SMOTE]]**나 **[[096_oversampling_smote|Oversampling]]** 기법을 적용하여 모델이 소수 클래스를 학습하지 못하는 '정확도의 함정'을 피해야 함.
- **[[257_ensemble_learning|앙상블]]([[257_ensemble_learning|Ensemble]]) [[268_strategy_pattern|전략]]:** 단일 모델보다는 **XGBoost**나 **LightGBM** 같은 [[127_boosting|부스팅]] 모델을 사용하는 것이 실질적인 [[282_performance_tactics|성능]](Score) 확보에 유리함.
- **설명 가능성([[227_xai_explainable_ai_lime_shap|XAI]]):** 딥러닝 기반 분류 시 판단 근거를 알기 어려우므로, **[[327_shap|SHAP]]**이나 **[[326_lime|LIME]]** 기표를 통해 변수 중요도를 역추적하는 것이 기술사적 필수 소양임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **자동화 의사결정:** 인간의 수동 판단 영역을 기계가 대체하여 비용 절감과 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 향상을 달성함.
- **실시간 탐지:** 스트리밍 [[001_dikw_pyramid|데이터]]와 결합하여 초단위로 발생하는 이상 결제나 공격 시도를 즉각 차단할 수 있음.
- **표준화된 평가:** 정량적인 평가 지표(F1, AUC)의 확립은 [[001_dikw_pyramid|데이터]] 사이언스 프로젝트의 성공 여부를 판단하는 글로벌 표준이 됨.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념:** [[121_supervised_learning|Supervised Learning]], Machine [[240_switch_learning_forwarding_flooding|Learning]]
- **하위 개념:** [[257_ensemble_learning|Ensemble]], Neural Networks, [[270_softmax|Softmax]]
- **연관 기술:** [[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]], [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]], [[085_hyperparameter_tuning|Hyperparameter Tuning]], [[227_xai_explainable_ai_lime_shap|XAI]]

### 📈 관련 키워드 및 발전 흐름도

```text
[Supervised Learning (지도 학습)]
    │
    ▼
[Ensemble (앙상블)]
    │
    ▼
[Neural Networks (신경망)]
    │
    ▼
[Confusion Matrix (혼동 행렬)]
    │
    ▼
[SMOTE (불균형 처리)]
```

이 흐름도는 [[121_supervised_learning|Supervised Learning]] ([[121_supervised_learning|지도 학습]])에서 출발해 [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] (불균형 처리)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **과일 분류 비유:** 사과와 오렌지의 색깔과 모양을 보고, "이건 사과야!"라고 이름표를 붙여주는 거예요.
2. **우편물 비유:** 편지 주소를 보고 "이건 서울로 가야 해!" 하고 바구니에 나누어 담는 우체부 아저씨와 같아요.
3. **거름망 비유:** 구멍이 숭숭 뚫린 체로 크고 작은 콩을 걸러내는 것처럼, 특징에 따라 방을 나누는 마법의 방 배정 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 104 / 262

← **이전**: [[103_regression_analysis|회귀 분석 (Regression Analysis)]]
**다음**: [[105_clustering_analysis|군집화 (Clustering) 분석]] →

---
