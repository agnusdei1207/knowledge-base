+++
title = "247. 독립 변수 (피처) / 종속 변수 (라벨)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 독립 변수(Independent Variable) 또는 피처(Feature)는 모델의 입력이고, 종속 변수(Dependent Variable) 또는 라벨(Label)/타깃(Target)은 예측해야 할 출력이다.
> 2. **가치**: 피처의 품질이 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정하며, 피처 공학([Feature 엔진ering](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/))은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식을 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델에 주입하는 핵심 프로세스다.
> 3. **판단 포인트**: [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))는 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/863_dimensionality_reduction/))를 통해 불필요한 특성을 제거하면서 정보 손실을 최소화하는 대표적 피처 처리 기법이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 기본 개념 정의
[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델은 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(피처)를 받아 출력(라벨)을 예측한다. 이 두 변수 유형은 통계학, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)에 걸쳐 다양한 명칭으로 불린다.

| ML 용어 | 통계학 용어 | 수학 표기 | 역할 |
|:---|:---|:---|:---|
| 피처(Feature) | 독립 변수(Independent Variable) | X | 모델 입력 |
| 라벨(Label) / 타깃(Target) | 종속 변수(Dependent Variable) | y | 모델 출력 (예측 대상) |
| 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 표본(Sample) | (X, y) | 학습에 사용되는 쌍 |

### 1.2 피처와 라벨의 실제 예시

| 문제 | 피처 (X) | 라벨 (y) |
|:---|:---|:---|
| 주택 가격 예측 | 면적, 방 수, 위치, 층수 | 가격(만원) |
| 이메일 스팸 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 단어 빈도, 발신자, 링크 수 | 스팸 여부 (0/1) |
| 의료 진단 | 혈압, 혈당, 나이, BMI | 질병 여부 |
| 영화 평점 예측 | 장르, 감독, 배우, 개봉연도 | 평점 (1~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)) |

### 1.3 입력 공간 (Input Space)
피처 벡터 X = (x₁, x₂, ..., xₙ)가 존재하는 n차원 공간을 **입력 공간(Input Space)** 또는 <strong>특성 공간(Feature Space)</strong>이라 한다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 피처는 집을 설명하는 "스펙표"(방 수, 층수, 위치)이고, 라벨은 그 집의 "실제 매매가"다. 좋은 스펙표(피처)일수록 실제 가격(라벨)을 더 정확히 예측할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 피처 처리 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인

```
+---------------------------------------------------------+
|                피처 처리 파이프라인                        |
|                                                         |
|  원시 데이터        피처 공학         모델 입력             |
|  (Raw Data)    (Feature Eng.)    (Input Space)          |
|                                                         |
|  +----------+   +--------------+   +--------------+    |
|  |나이: 25   |   |나이 정규화    |   |[0.3, 1, 0, 0,|    |
|  |직업: 학생 |--->|직업: 원-핫   |--->| 0.7, 50000]  |    |
|  |수입: 50만 |   |수입: 로그변환 |   +--------------+    |
|  +----------+   +--------------+        X 벡터          |
|                                                         |
|         v 모델 학습/예측 v                               |
|                                                         |
|         ŷ = f(X) -> 라벨 예측                            |
+---------------------------------------------------------+
```

### 2.2 피처 공학 ([Feature 엔진ering](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/)) 유형

| 유형 | 기법 | 예시 |
|:---|:---|:---|
| <strong>특성 선택(Feature <a href="/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/">Selection</a>)</strong> | 불필요한 피처 제거 | 상관관계 분석, RFE |
| **특성 추출(Feature Extraction)** | 기존 피처에서 새 피처 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), t-SNE, [오토인코더](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) |
| **특성 변환(Feature Transformation)** | [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), 인코딩 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) |
| **파생 특성(Derived Feature)** | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 기반 신규 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 나이/수입 비율, BMI 계산 |

### 2.3 [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))

```
      고차원 특성 공간         ->        저차원 주성분 공간
  x₁ --+                           PC1 (분산 최대 방향)
  x₂ --+  PCA 변환   --------->     PC2 (PC1에 직교)
  x₃ --+  (선형 투영)               PC3 ...
  xₙ --+
  n차원                             k차원 (k < n)
```

PCA는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 최대가 되는 방향(주성분)으로 투영하여 차원을 줄이는 기법이다. 공분산 행렬(Covariance Matrix)의 고유벡터(Eigenvector)가 주성분이 된다.

### 2.4 레이블 인코딩 (Label Encoding) vs [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) ([One-Hot Encoding](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/))

| 구분 | 레이블 인코딩 | [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) |
|:---|:---|:---|
| 방법 | 범주에 정수 부여 | 범주별 이진 열 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 예시 | 빨강=0, 초록=1, 파랑=2 | [1,0,0], [0,1,0], [0,0,1] |
| 장점 | 차원 유지, 단순 | 순서 가정 없음 |
| 단점 | 순서 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 오해 가능 | 고차원화 |
| 적합 모델 | 트리 기반 모델 | 선형 모델, 신경망 |

- **📢 섹션 요약 비유**: PCA는 사진 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하는 것과 같다. 눈에 중요한 정보([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 큰 방향)는 남기고, 거의 안 보이는 세부 내용([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 작은 방향)은 버려서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기를 줄이지만 사진의 핵심은 유지한다.

---

## Ⅲ. 비교 및 연결

### 3.1 피처 선택 vs 피처 추출

| 구분 | 피처 선택(Feature [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/)) | 피처 추출(Feature Extraction) |
|:---|:---|:---|
| 원리 | 기존 피처 중 중요한 것만 선택 | 기존 피처를 변환하여 새 피처 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 해석 가능성 | 높음 (원본 피처 유지) | 낮음 (변환된 피처는 추상적) |
| 방법 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 임계값, 상관관계, RFE | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), t-SNE, [오토인코더](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) |
| [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) | 불필요한 피처 제거 | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)된 표현으로 재구성 |

### 3.2 피처 중요도 ([Feature Importance](/knowledge-base/studynote/10_ai/05_data_science_ml/355_random_forest_feature_importance/)) 측정

| 방법 | 원리 | 모델 의존성 |
|:---|:---|:---|
| [피어슨 상관](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/226_pearson_correlation_regression_r2_vif_multicollinearity/)계수 | 선형 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 강도 측정 | 모델 독립 |
| [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) 중요도 | 불순도 감소 기여도 | 트리 기반 |
| [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) (SHapley Additive exPlanation) | 게임 이론 기반 기여도 | 모델 독립 |
| 퍼뮤테이션 중요도 | 피처 섞었을 때 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 변화 | 모델 독립 |

### 3.3 차원의 저주 ([Curse of Dimensionality](/knowledge-base/studynote/12_it_management/02_itsm_itil/864_curse_of_dimensionality/))
피처 수가 너무 많아지면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간이 희소(Sparse)해져 모델 학습이 어려워지는 현상. [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 등)로 완화한다.

- **📢 섹션 요약 비유**: 피처가 너무 많으면 큰 창고에 물건이 너무 드문드문 흩어져 있어 패턴을 찾기 어려운 것과 같다. PCA는 창고를 작게 만들되 핵심 물건은 모아두는 창고 재배치 작업이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 피처 엔지니어링 실무 워크플로우
1. <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis/">탐색적 데이터 분석</a>(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/">EDA</a>)</strong>: 분포, 결측치, [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
2. **상관관계 분석**: 피처 간 다중공선성([Multicollinearity](/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)) 점검
3. **인코딩**: 범주형 변수 수치화 (레이블/원-핫 선택)
4. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong>: 수치형 변수 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)/표준화
5. <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/">차원 축소</a></strong>: [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 또는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 기반 피처 선택
6. <strong>파생 특성 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: 비즈니스 인사이트 반영

### 4.2 기술사 핵심 판단 포인트
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 누수(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Leakage)</strong>: 라벨 정보가 피처에 포함되지 않도록 주의
- **피처 중요도 해석**: 모델 설명 가능성([XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/), [Explainable AI](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/)) 요구 시 [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) 활용
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a> 적용 시기</strong>: 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(100차원 이상), [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 필요 시, 다중공선성 제거 시
- **인코딩 선택 기준**: 트리 모델 -> 레이블 인코딩 가능, 선형/신경망 -> 원-핫 필요

### 4.3 실무 예시: 고객 이탈 예측

| 피처 유형 | 피처 예시 | 전처리 |
|:---|:---|:---|
| 수치형 | 가입 기간, 월 사용료 | 표준화 (Z-Score) |
| 범주형 | 요금제 유형 (A/B/C) | [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) |
| 순서형 | 만족도 (1~5) | 레이블 인코딩 |
| 파생형 | 월 사용료 / 가입 기간 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 반영 |

- **📢 섹션 요약 비유**: 피처 공학은 재료 손질이다. 아무리 좋은 셰프(모델)도 씻지 않고 썰지 않은 재료(원시 피처)로는 맛있는 요리를 못 만든다. 재료를 어떻게 다듬느냐(인코딩, [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))가 최종 맛([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))을 좌우한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 품질 좋은 피처의 효과
- 모델 학습 속도 향상
- 예측 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선 (단순한 모델로도 높은 정확도)
- 모델 해석 가능성 향상
- 과대적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) 위험 감소

### 5.2 결론
피처(독립 변수)와 라벨(종속 변수)의 명확한 구분은 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 프로젝트의 출발점이다. 피처 공학은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식과 통계적 방법을 결합하여 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화하는 핵심 기술이며, PCA를 포함한 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 기법은 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 정보를 효율적으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)한다. 기술사 시험에서는 피처-라벨 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 원리, 인코딩 기법 선택 기준을 명확히 서술할 수 있어야 한다.

- **📢 섹션 요약 비유**: 독립 변수와 종속 변수의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 원인과 결과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. 피처 공학은 그 원인들을 가장 명확하게 드러내도록 정제하는 작업이고, PCA는 수많은 원인을 몇 가지 핵심 원인으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하는 지혜다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 피처(Feature) | 독립 변수, 입력 공간 / 모델의 학습 재료 |
| 라벨(Label) | 종속 변수, 타깃, 정답 / 모델의 예측 목표 |
| [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | 주성분, 고유값, [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) / 피처 추출 기법 |
| 레이블 인코딩 | 정수 매핑, 순서 가정 / 범주형 -> 수치형 변환 |
| [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) | 이진 벡터, 다중공선성 / 범주형 -> 이진 행렬 |
| 피처 중요도 | [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/), RFE, 상관계수 / 피처 선택 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [독립 변수 (피처) / 종속 변수 (라벨)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 피처는 사람을 설명하는 **키, 몸무게, 나이** 같은 정보들이에요.
2. 라벨은 그 사람이 <strong>농구 선수인지 아닌지</strong>처럼 우리가 맞혀야 하는 정답이에요.
3. PCA는 수백 가지 정보를 "가장 중요한 몇 가지"로 줄여서 컴퓨터가 더 빨리 배울 수 있게 도와주는 마법이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 247 / 420

<- **이전**: [246. 과소 적합 (Underfitting)](/knowledge-base/studynote/10_ai/03_llm_nlp/246_underfitting_bias/)
**다음**: [248. 원-핫 인코딩 (One-Hot Encoding)](/knowledge-base/studynote/10_ai/03_llm_nlp/248_one_hot_encoding/) ->

---
