+++
title = "82. 선형 판별 분석 (LDA: Linear Discriminant Analysis)"
date = 2026-04-13

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선형 판별 분석(LDA)은 PCA와 같은 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 기법이지만, 정답 라벨(Y)을 활용하여 "클래스(집단)를 가장 잘 구별할 수 있는 축"을 찾아내는 **[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/))** 기반의 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 및 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 알고리즘이다.
> 2. **수학적 목표**: LDA의 목적 함수는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 투영되었을 때, 서로 다른 클래스 간의 중심 거리(Between-class [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))는 **최대화**하고, 동일한 클래스 내의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 퍼짐(Within-class [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))은 **최소화**하는 최적의 직교 축을 찾는 것이다.
> 3. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 군집이 확실하게 분리되도록 차원을 압축하기 때문에, 이후에 적용되는 로지스틱 회귀나 [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 같은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델의 예측 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 비약적으로 끌어올리는 강력한 전처리 도구로 활용된다.

---

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
빅데이터 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서 변수의 수가 너무 많아지면 모델이 학습 방향을 잃어버리는 '차원의 저주'가 발생합니다. 앞서 다룬 [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전체의 퍼짐([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))만을 고려하기 때문에, 정작 "사과와 바나나를 구별하는 데 핵심적인 정보"는 지워버리고 쓸데없는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 남길 위험이 존재합니다. 이러한 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 한계를 극복하기 위해 제안된 것이 바로 **LDA(Linear Discriminant Analysis)**입니다. LDA는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 속한 범주(Class) 정보를 적극적으로 활용하여, 집단 간의 차이를 가장 극명하게 보여주는 선형 축을 찾아 투영시킵니다. 즉, [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)와 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델링을 동시에 수행할 수 있는 스마트한 알고리즘입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

LDA의 최적화 메커니즘은 두 가지 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 행렬(Scatter Matrix)을 정의하고 이들의 비율(Ratio)을 최대화하는 고유값(Eigenvalue) 문제를 푸는 것입니다.
1. **$S_B$ (Between-class Scatter Matrix)**: 서로 다른 클래스 중심(Mean)들 간의 거리. (이 값은 클수록 좋다)
2. **$S_W$ (Within-class Scatter Matrix)**: 동일 클래스 내에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들이 뭉쳐있는 정도. (이 값은 작을수록 좋다)
3. **목적 함수**: $J(W) = \frac{W^T S_B W}{W^T S_W W}$ 를 최대화하는 투영 행렬 $W$를 구합니다.

```text
+---------------------------------------------------------------+
|         LDA (Linear Discriminant Analysis) Mechanism          |
+---------------------------------------------------------------+
|  [Bad Projection (Like PCA)]    [Good Projection (LDA)]       |
|                                                               |
|        Class A      Class B        Class A          Class B   |
|         ooo          xxx             ooo              xxx     |
|          ooo        xxx               ooo            xxx      |
|           ooo      xxx                 ooo          xxx       |
|                                                               |
|  --+---------+---------+-->    --+----------+----------+-->   |
|   Mixed Projection Axis        Discriminant Axis (LDA)        |
|  (Hard to separate A & B)      (A & B are clearly separated)  |
|                                                               |
| [Mathematical Pipeline]                                       |
|  1. Compute d-dimensional mean vectors for different classes. |
|  2. Compute Within-class Scatter Matrix (S_W).                |
|  3. Compute Between-class Scatter Matrix (S_B).               |
|  4. Compute Eigenvectors & Eigenvalues for (S_W^-1 * S_B).    |
|  5. Sort Eigenvectors by decreasing Eigenvalues.              |
|  6. Choose Top-K Eigenvectors to form transformation matrix W.|
|  7. Project samples onto the new subspace: Y = X * W          |
+---------------------------------------------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/)) | LDA (선형 판별 분석) |
| :--- | :--- | :--- |
| **목적** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최대화** (정보량 보존) | 클래스 간 **분리도 최대화** ([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화) |
| **학습 방법** | **[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)** (Unsupervised) | **[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)** (Supervised) |
| **라벨(Y) 유무** | 필요 없음 (X 변수들만 사용) | **반드시 필요함** (클래스 소속 정보 필수) |
| **축소 가능한 최대 차원** | 변수의 개수 (D) | **클래스 개수 - 1** (C - 1) |
| **취약점** | 클래스 구분에 중요한 정보가 손실될 수 있음 | 정규분포 가정을 위배하거나, $S_W$ 행렬의 역행렬을 구할 수 없는 경우(소규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 취약함 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

현업 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 파이프라인에서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 과제를 수행할 때, LDA는 단순한 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)를 넘어 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기(Classifier) 자체로도 훌륭한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 발휘합니다.
1. **차원 제약 조건의 인식**: LDA가 생성할 수 있는 새로운 축(차원)의 최대 개수는 `(클래스 개수 - 1)`입니다. 즉, 개와 고양이를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 2진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(Binary [Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 문제에서는 수백 개의 변수가 단 **1개**의 차원(1D 축)으로 극단적으로 압축됩니다. 이는 강력한 압축률을 자랑하지만, 복잡한 비선형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 담아내기에는 한계가 있음을 인지해야 합니다.
2. **[다중 공선성](/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)과 PCA와의 융합**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변수들 간에 [다중 공선성](/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)([Multicollinearity](/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/))이 너무 심하면 LDA 내부에서 역행렬 연산 시 오류(Singular Matrix)가 발생할 수 있습니다. 기술사적 최적화 전략으로는 **먼저 PCA를 적용하여 [다중 공선성](/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)을 제거한 뒤, 그 결과물에 LDA를 적용하는 하이브리드 파이프라인([PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) -> LDA)**을 구축하여 수학적 안정성과 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 취하는 방식을 권장합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

LDA는 통계학과 패턴 인식 분야에서 가장 역사 깊고 견고한 선형 판별 알고리즘입니다. 딥러닝(Deep [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 시대가 도래하면서 신경망 자체가 은닉층(Hidden Layer)을 통해 더 강력한 비선형 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)와 판별을 수행하게 되었지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 양이 적거나 완벽한 화이트박스(White-box) 모델 해석력이 요구되는 의료 진단, 금융 신용 평가 도메인에서는 여전히 LDA가 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 모델로 강력하게 군림하고 있습니다. LDA의 "클래스 내부는 뭉치고, 클래스 간은 멀게 한다"는 우아한 수학적 철학은 현대의 대조 학습(Contrastive [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))이나 샴 네트워크(Siamese Network)의 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/)) 설계 철학으로 고스란히 계승되어 그 명맥을 이어가고 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* **상위 개념**: [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)), [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/))
* **핵심 수학**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 행렬(Scatter Matrix), [고유값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/)(Eigen Decomposition)
* **비교/응용 기법**: [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/)), QDA(이차 판별 분석), 대조 학습(Contrastive [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))

---

### 👶 어린이를 위한 3줄 비유 설명
1. 체육 시간에 "빨간 팀"과 "파란 팀"을 나누려고 하는데, 운동장이 너무 넓어서 애들이 마구 섞여 있어요.
2. 똑똑한 체육 선생님(LDA)이 나타나서, "빨간 팀은 왼쪽으로 뭉치고, 파란 팀은 오른쪽으로 뭉쳐! 그리고 두 팀 사이는 최대한 멀리 떨어져!"라고 선을 그어줬어요.
3. 이제 선 하나만 딱 봐도, 누가 빨간 팀이고 파란 팀인지 한눈에 100% 알아맞힐 수 있게 되었답니다! (분리도 최대화)

### 📈 관련 키워드 및 발전 흐름도

```text
피셔 판별 분석 (Fisher's LDA, 1936)
    │
    ▼
LDA: 클래스 간 분산 최대화 + 클래스 내 분산 최소화
    │
    ├─► 차원 축소: 최대 (C-1)개 축으로 압축
    └─► 분류기: 가우시안 사후 확률로 직접 분류
    │
    ▼
PCA → LDA 하이브리드 파이프라인 (실무 표준)
    │
    ▼
비선형 확장
    ├─► QDA (이차 판별 분석) — 클래스별 공분산 허용
    ├─► Kernel LDA — 커널 트릭 적용
    └─► 대조 학습 (Contrastive Learning) — LDA 철학의 딥러닝 계승
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 82 / 258

← **이전**: [81. 차원 축소 (Dimensionality Reduction) 및 PCA](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)
**다음**: [83. 연관 규칙 탐색 (Association Rule) - Apriori 알고리즘](/knowledge-base/studynote/14_data_engineering/02_math_mining/083_association_rule_apriori_market_basket/) →

---
