---
title: "087. Loss Function"
date: "2026-04-05"
tags:
  - "it_management"
  - "studynote-it-management"
weight: 87
---
## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) (Loss Function)는 예측값과 정답 사이의 차이를 수치화해 학습 방향을 제공하는 목적 함수의 핵심 요소다.
    > 2. **가치**: [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)), MAE (Mean Absolute Error), cross-entropy는 문제 유형과 오차 민감도에 따라 다른 학습 성향을 만든다.
    > 3. **판단 포인트**: 평가 지표와 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 혼동하면 모델은 최적화되지만 업무 목표에는 맞지 않는 결과를 낼 수 있다.

    ---

    ## Ⅰ. 개요 및 필요성

    [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) (Loss Function)는 모델이 얼마나 틀렸는지 알려 주는 숫자다. [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) ([Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))은 이 값을 줄이는 방향으로 파라미터를 갱신하므로, [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 단순한 점수가 아니라 학습의 지도다.

회귀와 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 손실 선택이 다르다. 회귀는 연속값의 거리와 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 민감도를, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석과 클래스 불균형을 함께 고려해야 하므로, 같은 모델이라도 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)에 따라 학습 성격이 크게 달라진다.

    - **📢 섹션 요약 비유**: 시험에서 채점 기준이 있어야 어디를 고칠지 알 수 있는 것과 같다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    손실은 보통 `L(y, ŷ)` 형태로 표현된다. MSE는 큰 오차를 제곱해 강하게 벌주고, MAE는 오차를 선형으로 다뤄 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에 덜 민감하며, cross-entropy는 정답 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 높이는 방향으로 학습한다.

| [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) | 주 용도 | 특징 |
| :-- | :-- | :-- |
| [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)) | 회귀 | 큰 오차에 민감, 매끄러운 미분 |
| MAE (Mean Absolute Error) | 회귀 | [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에 강함, 기울기 일정 |
| Binary [cross-entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) | 이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석이 자연스러움 |
| Categorical [cross-entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) | 다중 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 정답 클래스 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 강화 |
| Hinge loss | 마진 기반 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 경계 여유를 강조 |
| Focal loss | 불균형 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 어려운 샘플에 집중 |

```text
입력 x -► 모델 -► 예측 ŷ -► 손실 L(y, ŷ) -► 기울기 -► 파라미터 업데이트
```

[손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 "틀림의 크기"를 만드는 동시에 "어떻게 고칠지"를 함께 결정한다. 그래서 학습 곡선이 좋은지는 모델 구조뿐 아니라 손실 설계에 달려 있다.

    - **📢 섹션 요약 비유**: 점수판마다 다른 룰이 있듯, 회귀와 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 서로 다른 손실을 써야 한다.

    ---

    ## Ⅲ. 비교 및 연결

    [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/), 평가 지표, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 항은 역할이 다르다. [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 학습용이고, 평가 지표는 사업 성과를 읽는 눈이며, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 항은 과적합을 막는 제약이다.

| 구분 | 역할 | 예시 |
| :-- | :-- | :-- |
| Loss | 학습 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/), [cross-entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) |
| [Metric](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 최종 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 측정 | Accuracy, [F1-score](/studynote/10_ai/03_llm_nlp/255_f1_score/) |
| Regularizer | 복잡도 제어 | L1, L2 |

[확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 관점에서도 연결된다. MSE는 보통 Gaussian 가정과, MAE는 Laplace 가정과 잘 맞고, cross-entropy는 Bernoulli나 multinomial 분포 해석과 연결된다. 즉 손실 선택은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포에 대한 가정이기도 하다.

    - **📢 섹션 요약 비유**: 성적표와 훈련 점수를 같은 것으로 보면, 연습 방향이 헷갈린다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 문제 유형보다 오차 비용 구조를 먼저 봐야 한다. 값의 크기가 중요하면 [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/), [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 많으면 MAE, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이 중요하면 cross-entropy를 우선 검토한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)가 실제 비즈니스 비용과 맞는가?
2. 클래스 불균형이나 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 특성을 반영했는가?
3. 손실과 평가 지표가 서로 충돌하지 않는가?
4. 커스텀 손실이 미분 가능하고 수치적으로 안정한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- accuracy만 보고 손실은 대충 고르는 것
- 불균형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 기본 cross-entropy만 쓰는 것
- 커스텀 손실을 만들고 gradient 안정성을 검증하지 않는 것

    - **📢 섹션 요약 비유**: 똑같이 틀려도 어떤 오답은 크게, 어떤 오답은 작게 보는 채점자가 있다.

    ---

    ## Ⅴ. 기대효과 및 결론

    [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 모델 학습의 성격을 정하는 설계 변수다. 같은 네트워크라도 어떤 손실을 쓰느냐에 따라 민감도, 안정성, 수렴 속도가 모두 달라진다.

따라서 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 구현 디테일이 아니라, 업무 목표를 최적화 문제로 번역하는 계약으로 기억하는 것이 가장 정확하다.

    - **📢 섹션 요약 비유**: 무엇을 잘했는지보다 무엇을 줄여야 하는지가 학습을 움직인다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| Loss Function | 학습 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| [MSE](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)) | 회귀의 기본 손실 |
| [Cross-Entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 기반 손실 |
| [Metric](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 최종 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| Regularizer | 과적합 제어 항 |

    ### 📈 관련 키워드 및 발전 흐름도

    예측값 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
    |
    v
손실 계산
    |
    v
[역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/) / 경사 하강
    |
    v
모델 파라미터 갱신

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 숙제를 틀렸을 때 어디가 틀렸는지 알려 주는 점수표예요.
    2. 회귀는 얼마나 틀렸는지, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 맞혔는지에 따라 다른 점수표를 써요.
    3. 그래서 컴퓨터도 문제에 맞는 점수 규칙이 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 587

<- **이전**: [86. OLA (Operational Level Agreement)](/studynote/12_it_management/02_itsm_itil/870_ola/)
**다음**: [87. UC (Underpinning Contract)](/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) ->

---
