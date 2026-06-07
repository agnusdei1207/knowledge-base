---
title: "Regression Analysis"
date: "2024-03-20"
tags:
  - "studynote-bigdata"
weight: 103
---
## 핵심 인사이트 (3줄 요약)
- <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 모델링:</strong> 하나 이상의 독립변수($X$)와 종속변수($Y$) 사이의 상관관계를 함수로 공식화하여 미래의 수치 값을 예측함.
- **최소제곱법 (OLS):** 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트와 회귀선 사이의 거리의 제곱합(Error)을 최소화하는 최적의 직선([Best Fit](/studynote/02_operating_system/06_memory_management/345_best_fit/) Line)을 도출함.
- **설명력 확보:** 단순한 수치 예측을 넘어, 어떤 변수가 결과에 유의미한 영향을 주는지 통계적으로 입증 가능함.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **통계학의 근간:** '평균으로의 회귀(Regression to the Mean)' 현상에서 유래하였으며, 오늘날 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 [지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) 중 '수치 예측' 영역의 핵심 기술임.
- **비즈니스 가치:** 매출액 예측, 부동산 가격 산정, 고객 평생 가치([LTV](/studynote/07_enterprise_systems/02_erp_systems/108_ltv_life_time_value/)) 추정 등 연속형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루는 모든 의사결정 모델링에 필수적임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **수학적 기본 모델:** $Y = \beta_0 + \beta_1 X_1 + \dots + \beta_n X_n + \epsilon$
- <strong>Bilingual <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/">ASCII</a> Diagram:</strong>
```text
[Linear Regression Concepts / 선형 회귀 핵심 개념]

    Dependent (Y)
      ^
      |           *  Actual Data Point (y)
      |          /
      |         |  Residual/Error (e = y - y_hat)
      |         v
      |       /------* Regression Line (y_hat = b0 + b1x)
      |     /   *
      |   /  *
      | /_________________ Independent (X)

[Key Assumptions / 핵심 가정]
1. Linearity (선형성): X와 Y는 직선 관계
2. Independence (독립성): 잔차 간의 상관관계 없음
3. Homoscedasticity (등분산성): 잔차의 분산이 일정
4. Normality (정규성): 잔차 항은 정규 분포를 따름
```
- **주요 유형:**
  - **단순 회귀:** 독립변수 1개.
  - **다중 회귀:** 독립변수 2개 이상 ([다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/) 주의).
  - **다항 회귀:** 변수 간 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 곡선일 때 차수를 높임.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 선형 회귀 (Linear) | 라쏘 ([Lasso](/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/) / L1) | 릿지 (Ridge / L2) |
| :--- | :--- | :--- | :--- |
| **목적 (Goal)** | 오차 최소화 | 변수 선택 + 과적합 방지 | 과적합 방지 (계수 축소) |
| **페널티 (Penalty)** | 없음 | 계수의 절대값 합 추가 | 계수의 제곱합 추가 |
| **특징 (Feature)** | 해석이 쉬움 | 중요하지 않은 변수 계수 0화 | 모든 변수를 유지하며 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감소 |
| **모델 복잡도** | 높음 | 낮음 (Sparse) | 중간 |
| **비유 (Analogy)** | 있는 그대로의 직선 | 깐깐한 거름망 | 부드러운 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>적 전처리:</strong> [회귀 분석](/studynote/08_algorithm_stats/08_stats/149_regression_analysis/) 전 <strong><a href="/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/">다중 공선성</a>(<a href="/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/">Multicollinearity</a>)</strong> [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 필수적임. VIF 지수가 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이상인 변수는 제거하거나 PCA로 차원을 축소해야 모델의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 확보함.
- <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 지표:</strong> 단순 정확도보다는 **[결정 계수](/studynote/14_data_engineering/02_math_mining/098_coefficient_of_determination_r_squared/)($R^2$)**를 통해 모델의 설명력을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)/RMSE를 통해 오차의 크기를 평가함.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 엔지니어링 연계:</strong> 대규모 빅데이터 환경에서는 Spark의 MLlib LinearRegression을 사용하여 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서의 연산 가속을 꾀함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **예측 가능성 증대:** 불확실한 미래 수치를 정교한 수식 기반으로 예측하여 비즈니스 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 낮춤.
- **AI의 기초:** 복잡한 신경망(Deep [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))도 결국 수많은 [로지스틱 회귀](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)와 선형 회귀 층의 결합체이므로, [회귀 분석](/studynote/08_algorithm_stats/08_stats/149_regression_analysis/)에 대한 깊은 이해는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 전문가의 기본 소양임.
- **표준 확립:** 설명 가능한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)) 트렌드에서 회귀 계수는 모델의 판단 근거를 제시하는 강력한 표준 지표로 활용됨.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [Predictive Analytics](/studynote/16_bigdata/02_hadoop/046_predictive_analytics/), [Supervised Learning](/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)
- **하위 개념:** OLS, [Regularization](/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/) (L1, L2), [Logistic Regression](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)
- **연관 기술:** [Pearson Correlation](/studynote/14_data_engineering/05_exam_keywords/226_pearson_correlation_regression_r2_vif_multicollinearity/), VIF, R-Squared, [Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/)

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: Predictive Analytics, Supervised Learning]
    |
    v
[하위 개념: OLS, Regularization (L1, L2), Logistic Regression]
    |
    v
[연관 기술: Pearson Correlation, VIF, R-Squared, Gradient Descent]
```

이 흐름도는 상위 개념: [Predictive Analytics](/studynote/16_bigdata/02_hadoop/046_predictive_analytics/), Supervised Learning에서 출발해 연관 기술: [Pearson Correlation](/studynote/14_data_engineering/05_exam_keywords/226_pearson_correlation_regression_r2_vif_multicollinearity/), VIF, R-Squared, Gradient Descent까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **키 크기 비유:** 부모님의 키를 보고 내 키가 얼마나 클지 예상하는 마법의 자와 같아요.
2. **성적 비유:** 공부한 시간과 시험 점수 사이의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 찾아내서, "몇 시간 공부하면 몇 점 받을까?"를 맞히는 게임이에요.
3. **길찾기 비유:** 점들이 흩어져 있는 운동장에 선을 하나 그어서, 점들이 최대한 그 선 근처에 모이게 만드는 놀이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 103 / 262

<- **이전**: [탐색적 데이터 분석 (EDA, Exploratory Data Analysis)](/studynote/16_bigdata/05_analysis/102_eda_exploratory_data_analysis/)
**다음**: [분류 (Classification) 분석](/studynote/16_bigdata/05_analysis/104_classification_analysis/) ->

---
