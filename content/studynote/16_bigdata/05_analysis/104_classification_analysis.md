+++
title = "분류 (Classification) 분석"
date = 2024-03-20

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **범주 예측:** 입력된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특징(Feature)을 기반으로 해당 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 속할 미리 정의된 집단(Class/Label)을 판별하는 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)의 핵심.
- **결정 경계 (Decision Boundary):** 서로 다른 클래스를 가장 잘 구분하는 최적의 경계면을 수학적 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 찾아냄.
- <strong>불균형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 대응:</strong> 암 진단이나 사기 탐지처럼 정답 비율이 극히 낮은 경우엔 단순 정확도보다 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))과 F1-Score가 더 중요함.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의:** 이산적인 결과값(Yes/No, A/B/C)을 예측하는 기법으로, 비즈니스 영역에서 가장 광범위하게 쓰이는 분석 기퍼임.
- **활용 사례:** 스팸 메일 분류, 질병 유무 판독, 이탈 고객 예측, 이미지 객체 인식 등 무수히 많은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 적용됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **프로세스:** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 -> 전처리 -> 모델 선택 -> 학습(Fit) -> 평가(Score) -> 튜닝.
- <strong>Bilingual <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/">ASCII</a> Diagram:</strong>
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
- **평가 지표:** [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)) 기반의 [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/), [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/), AUC-ROC.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) (Logistic) | 결정 트리 (Tree) | [서포트 벡터 머신](/knowledge-base/studynote/14_data_engineering/02_math_mining/104_svm_support_vector_machine/) ([SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/)) |
| :--- | :--- | :--- | :--- |
| **모델 구조** | 선형 결합 (Linear) | 계층적 분기 (Hierarchy) | 마진 최대화 (Margin) |
| **장점 (Pros)** | 결과 해석 용이 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리 불필요 | 복잡한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 강점 |
| **단점 (Cons)** | 선형 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)만 해석 가능 | 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) 취약 | 학습 시간 및 자원 소모 |
| **비유 (Analogy)** | 찬성/반대 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 투표 | 스무고개 질문 | 안전 지대 확보하기 |
| **비고 (Note)** | 분류의 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) | [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)의 기본 단위 | 비선형 [커널 트릭](/knowledge-base/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/) 활용 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 불균형(Imbalance) 처리:</strong> 실제 현업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 대개 편향되어 있으므로 <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/">SMOTE</a></strong>나 <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/096_oversampling_smote/">Oversampling</a></strong> 기법을 적용하여 모델이 소수 클래스를 학습하지 못하는 '정확도의 함정'을 피해야 함.
- <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">앙상블</a>(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">Ensemble</a>) <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>:</strong> 단일 모델보다는 <strong>XGBoost</strong>나 **LightGBM** 같은 [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) 모델을 사용하는 것이 실질적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(Score) 확보에 유리함.
- <strong>설명 가능성(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/">XAI</a>):</strong> 딥러닝 기반 분류 시 판단 근거를 알기 어려우므로, <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/">SHAP</a></strong>이나 <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/326_lime/">LIME</a></strong> 기표를 통해 변수 중요도를 역추적하는 것이 기술사적 필수 소양임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **자동화 의사결정:** 인간의 수동 판단 영역을 기계가 대체하여 비용 절감과 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 향상을 달성함.
- **실시간 탐지:** 스트리밍 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 결합하여 초단위로 발생하는 이상 결제나 공격 시도를 즉각 차단할 수 있음.
- **표준화된 평가:** 정량적인 평가 지표(F1, AUC)의 확립은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언스 프로젝트의 성공 여부를 판단하는 글로벌 표준이 됨.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/), Machine [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)
- **하위 개념:** [Ensemble](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/), Neural Networks, [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)
- **연관 기술:** [Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/), [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/), [Hyperparameter Tuning](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_hyperparameter_tuning/), [XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)

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

이 흐름도는 [Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) ([지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/))에서 출발해 [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) (불균형 처리)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **과일 분류 비유:** 사과와 오렌지의 색깔과 모양을 보고, "이건 사과야!"라고 이름표를 붙여주는 거예요.
2. **우편물 비유:** 편지 주소를 보고 "이건 서울로 가야 해!" 하고 바구니에 나누어 담는 우체부 아저씨와 같아요.
3. **거름망 비유:** 구멍이 숭숭 뚫린 체로 크고 작은 콩을 걸러내는 것처럼, 특징에 따라 방을 나누는 마법의 방 배정 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 104 / 262

← **이전**: [회귀 분석 (Regression Analysis)](/knowledge-base/studynote/16_bigdata/05_analysis/103_regression_analysis/)
**다음**: [군집화 (Clustering) 분석](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) →

---
