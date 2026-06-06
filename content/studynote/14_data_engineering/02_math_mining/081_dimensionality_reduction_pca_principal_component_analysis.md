---
title: "081. Dimensionality Reduction Pca Principal Component Analysis"
date: "2026-04-12"
tags:
  - "studynote-data-engineering"
---

# 81. 차원 축소 ([Dimensionality Reduction](/studynote/12_it_management/02_itsm_itil/863_dimensionality_reduction/)) 및 [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([주성분 분석](/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 차원 축소([Dimensionality Reduction](/studynote/12_it_management/02_itsm_itil/863_dimensionality_reduction/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 수많은 변수(Feature, 차원)들 중에서 불필요한 노이즈를 제거하고 핵심적인 정보량([분산](/studynote/08_algorithm_stats/08_stats/136_variance/), [Variance](/studynote/08_algorithm_stats/08_stats/136_variance/))만을 남겨 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 복잡도를 획기적으로 줄이는 [비지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) 전처리 기법이다.
> 2. **PCA의 원리**: [주성분 분석](/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/)([PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [Principal Component Analysis](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))은 변수들 간의 상관관계를 분석하여, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 가장 최대로 보존하는 새로운 직교 축(Principal [Component](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))을 수학적([고유값 분해](/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/))으로 찾아내 투영(Projection)하는 대표적인 선형 차원 축소 알고리즘이다.
> 3. **가치**: 이를 통해 '차원의 저주([Curse of Dimensionality](/studynote/12_it_management/02_itsm_itil/864_curse_of_dimensionality/))'를 피하고, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델의 학습 속도 향상, 메모리 절약, 그리고 고차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 2차원이나 3차원으로 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)(Visualization)하여 직관적인 분석을 가능하게 한다.

---

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
빅데이터 시대에는 한 사람을 분석하기 위해 나이, 성별, 키, 몸무게, 소득, 소비 패턴 등 수백, 수천 개의 컬럼(차원)이 수집됩니다. 차원이 늘어날수록 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 설명하는 변수가 많아지지만, 일정 수준을 넘어서면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간의 부피가 기하급수적으로 커져 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 희소해지는 <strong>차원의 저주(<a href="/studynote/12_it_management/02_itsm_itil/864_curse_of_dimensionality/">Curse of Dimensionality</a>)</strong>가 발생합니다. 이로 인해 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 알고리즘은 과적합([Overfitting](/studynote/10_ai/03_llm_nlp/245_overfitting_variance/))에 빠지기 쉽고 계산 비용은 천문학적으로 증가합니다. 이를 해결하기 위해 원래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 가진 고유한 정보([분산](/studynote/08_algorithm_stats/08_stats/136_variance/))는 최대한 유지하면서 변수의 개수를 줄이는 마법 같은 수학적 기법이 바로 <strong>차원 축소</strong>이며, 그중 가장 널리 쓰이는 것이 <strong><a href="/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a>(<a href="/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/">주성분 분석</a>)</strong>입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

PCA는 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 <strong>공분산 행렬(Covariance Matrix)</strong>을 구한 뒤, 이를 <strong><a href="/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/">고유값 분해</a>(<a href="/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/">Eigenvalue Decomposition</a>)</strong>하여 고유벡터(Eigenvector)와 고유값(Eigenvalue)을 도출하는 선형 대수학의 결정체입니다.
1. **고유벡터(Eigenvector)**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 가장 넓게 퍼져 있는([분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 가장 큰) 방향의 새로운 축(주성분)입니다.
2. **고유값(Eigenvalue)**: 해당 고유벡터 축이 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 얼마나 많이 설명하는지를 나타내는 크기입니다.

```text
+---------------------------------------------------------------+
|         PCA (Principal Component Analysis) Mechanism          |
+---------------------------------------------------------------+
|  [2D Original Data]            [Transformed to 1D via PCA]    |
|   y ^                        ^ PC2 (Orthogonal, 2nd variance) |
|     |     . .                |                                |
|     |    . . .               |         Original Data points   |
|     |   . . .                |            projected onto PC1  |
|     |  . . .                 |  .                             |
|     | . .                    |  .                             |
|     +----------------> x     +--.----------------------> PC1  |
|                                 .     (Direction of Maximum   |
|                                 .      Variance = 1st PC)     |
|                                                               |
| [Mathematical Pipeline]                                       |
|  1. Standardization (Mean=0, Var=1)                           |
|  2. Covariance Matrix Computation                             |
|  3. Eigen Decomposition (Extract Eigenvectors & Eigenvalues)  |
|  4. Sort descending by Eigenvalues                            |
|  5. Select Top-K Components & Project Data (Matrix Multiply)  |
+---------------------------------------------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)) | LDA (Linear Discriminant Analysis) | t-SNE / UMAP |
| :--- | :--- | :--- | :--- |
| **학습 유형** | <strong><a href="/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a></strong> (정답 라벨 Y가 없음) | <strong><a href="/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/">지도 학습</a></strong> (정답 라벨 Y를 사용) | <strong><a href="/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a></strong> (비선형 매핑) |
| **최적화 목표** | 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a>) 최대화</strong> | 클래스 간 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 최대, 클래스 내 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 최소화 | 고차원의 <strong>지역적 거리(Local Structure)</strong>를 저차원에 보존 |
| **주 사용 목적** | [데이터 압축](/studynote/08_algorithm_stats/09_info_theory/159_compression/), 노이즈 제거, 다중공선성 해결 | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/studynote/12_it_management/03_ea_isp/107_classification/)) 모델의 전처리 및 차원 축소 | [데이터 시각화](/studynote/07_enterprise_systems/05_data_bi/283_data_visualization_dashboard_report/) (2D/3D 군집 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)) |
| **선형/비선형** | 선형 변환 (Linear) | 선형 변환 (Linear) | 비선형 변환 (Non-linear) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파이프라인에서 차원 축소는 필수적인 방어 기제입니다. 실무에서 PCA를 적용할 때 기술사로서 반드시 고려해야 할 사항은 다음과 같습니다.
1. <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a>(Scaling) 필수</strong>: PCA는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 '[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)'을 기준으로 작동하므로, 변수 간의 단위(Scale) 차이에 극도로 민감합니다. 예를 들어 '키(cm)'와 '연봉(원)'이 섞여 있다면 연봉의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 압도적으로 커 [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 축이 왜곡됩니다. 따라서 [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 적용 전 반드시 <strong>표준화(Standardization, Z-Score)</strong>를 수행해야 합니다.
2. <strong>설명력 보존율(Explained <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a> Ratio)의 타협</strong>: 주성분을 몇 개(K) 남길 것인가가 핵심입니다. 통상적으로 누적 설명 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 비율이 **80% ~ 90%** 이상이 되는 지점(Elbow Point)에서 주성분의 개수를 결정하여, 약간의 정보 손실을 감수하고 연산의 효율성을 극대화하는 엔지니어링적 타협(Trade-off)이 필요합니다.
3. **해석력의 상실**: 차원을 축소하여 만든 PC1, PC2는 원본 변수들의 선형 결합(짬뽕)이므로, "PC1이 도대체 무슨 의미인가?"를 현업에 설명하기가 매우 어렵습니다. 설명력이 중요한 비즈니스 의사결정에서는 PCA보다 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 선택(Feature [Selection](/studynote/10_ai/01_ai_basics/022_mcts_four_stages/))이 더 나은 전략일 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

차원 축소를 적재적소에 활용하면 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 파이프라인의 훈련 속도를 수십 배 이상 끌어올릴 수 있으며, 동시에 과적합을 방지하여 실서비스 환경에서의 일반화 성능을 높입니다. 특히, 이미지나 텍스트 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 같은 초고차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루는 딥러닝 영역에서, PCA는 무거운 텐서(Tensor)의 핵심 뼈대만 남겨 경량화하는 데 기여합니다. 더 나아가 비선형 차원 축소 기법인 t-SNE나 [오토인코더](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)([AutoEncoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/))와 결합하여, 방대한 빅데이터의 숨겨진 잠재 공간(Latent Space)을 탐험하는 핵심 항해 기술로 영구히 활용될 것입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* **상위 개념**: [비지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리(Preprocessing)
* **핵심 수학**: 공분산 행렬(Covariance Matrix), [고유값 분해](/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/)(Eigen Decomposition)
* **유사/발전 기법**: [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)([특이값 분해](/studynote/10_ai/05_data_science_ml/342_svd/)), LDA([선형 판별 분석](/studynote/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification/)), t-SNE, [AutoEncoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)

---

### 👶 어린이를 위한 3줄 비유 설명
1. 둥이의 장난감 상자에 장난감이 1,000개나 있어서 방이 너무 지저분하고 꽉 차버렸어요. (차원의 저주)
2. 그래서 똑똑한 정리 로봇([PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))이 와서, "자동차 종류는 빨간 박스에, 로봇 종류는 파란 박스에 합쳐서 넣자!" 하고 특징이 비슷한 것들끼리 뭉쳐버렸어요. ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 최대화 축 투영)
3. 장난감 개수는 1,000개에서 큰 박스 10개로 확 줄어들었지만, 둥이는 자기가 무슨 장난감을 가지고 있는지 여전히 다 기억할 수 있답니다! (정보량 보존)

### 📈 관련 키워드 및 발전 흐름도

```text
고차원 데이터 -> 차원의 저주 (과적합 · 계산 폭발)
    |
    v
선형 차원 축소
    +-► PCA: 분산 최대화 직교 축 투영 (비지도)
    +-► LDA: 클래스 간 분리 최대화 (지도)
    |
    v
비선형 차원 축소
    +-► t-SNE: 지역 구조 보존 (시각화 특화)
    +-► UMAP: 전역+지역 구조 보존 (t-SNE보다 빠름)
    +-► AutoEncoder: 신경망 기반 잠재 공간 학습
    |
    v
딥러닝 임베딩 -> VAE / Diffusion -> 잠재 공간 표현 학습
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 258

<- **이전**: [80. 다중 공선성 (Multicollinearity) 및 VIF 지수](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)
**다음**: [82. 선형 판별 분석 (LDA: Linear Discriminant Analysis)](/studynote/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification/) ->

---
