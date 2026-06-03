+++
weight = 102
title = "탐색적 데이터 분석 (EDA, Exploratory Data Analysis)"
date = "2025-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- **[[064_eda|EDA]] ([[105_exploratory_data_analysis|Exploratory Data Analysis]])**: 수집된 [[001_dikw_pyramid|데이터]]를 편견 없이 들여다보며 [[001_dikw_pyramid|데이터]]의 구조, 특징, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 및 변수 간 [[083_relationship_in_er_model|관계]]를 시각적으로 탐색하는 [[001_dikw_pyramid|데이터]] 분석의 첫 단계.
- **가설 [[087_process_state_transition|생성]]의 장**: 엄격한 [[145_hypothesis_testing|가설 검정]]([[101_inferential_statistics|추론 통계]])에 앞서, [[001_dikw_pyramid|데이터]]가 가진 잠재적 패턴을 직관적으로 발견하고 [[001_dikw_pyramid|데이터]]에 대한 통찰(Insight)을 얻는 과정.
- **품질 진단**: 결측치 처리, [[001_dikw_pyramid|데이터]] 분포의 왜곡 [[396_validation|확인]], 변수 변환(Log, Scale) 필요성 등 기계학습 모델링을 위한 [[268_strategy_pattern|전략]]적 의사결정의 근거를 제공함.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
빅데이터 분석에서 가장 위험한 것은 성급한 결론입니다. EDA는 존 튜키(John Tukey)가 제안한 방법론으로, 단순히 요약 통계량(평균 등)에만 의존하지 않고 [[003_resistance|저항]]성(Resistancy)과 잔차(Residual) 분석 등을 통해 [[001_dikw_pyramid|데이터]]의 '속살'을 파악합니다. 이는 분석의 정확도를 높이고 불필요한 시행착오를 줄이는 핵심 절차입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
EDA의 4대 핵심 원칙과 분석 워크플로우 아키텍처입니다.

```text
[ EDA Iteration Loop & 4 Core Principles ]

  [ Raw Data ] --> [ Data Cleaning ] --> [ Visualization & Summary ]
                         ^                          |
                         | (Discovery)              v
                  [ Model Design ] <--- [ Insights / Hypothesis ]

[ 4 Principles of EDA ]
1. Resistance (저항성): 이상치(Outlier)에 영향을 덜 받는 척도 사용.
2. Residual (잔차): 관찰값과 예측값의 차이를 분석하여 숨은 패턴 탐색.
3. Re-expression (재표현): 로그 변환 등으로 데이터 구조를 단순화/정규화.
4. Revelation (현시성): 그래프를 통한 시각화로 데이터를 한눈에 보여줌.
```

**핵심 원리:**
1. **일변량 분석 (Univariate)**: 변수 하나의 분포(히스토그램, 박스플롯)와 중심 경향성 [[396_validation|확인]].
2. **이변량 분석 (Bivariate)**: 두 변수 간의 상관관계(산점도, 상관계수) 및 인과 [[083_relationship_in_er_model|관계]]의 실마리 탐색.
3. **다변량 분석 (Multivariate)**: 3개 이상의 변수 조합을 통해 복합적인 영향도 파악 (히트맵, [[163_pca|PCA]] 등).
4. **[[003_bigdata_7v|시각화]]의 힘**: '안스콤의 4분할(Anscombe's Quartet)' 예시처럼 요약 통계가 같아도 [[070_graph_datastructure|그래프]]는 완전히 다를 수 있음을 명심해야 함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 탐색적 분석 ([[064_eda|EDA]]) | 확증적 분석 (CDA, Confirmatory) |
| :--- | :--- | :--- |
| **목적** | 패턴 발견, 가설 수립 | 가설 [[395_verification_process_review|검증]], 유의성 확정 |
| **자세** | 개방적, 유연함, 탐정(Detective) | 보수적, 엄격함, 판사(Judge) |
| **주요 도구** | [[070_graph_datastructure|그래프]], 산점도, 상자 수염 그림 | [[337_p_value_significance|p-value]], 신뢰구간, [[070_t_test_independent_paired_mean_difference|t-test]], [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] |
| **수행 시점** | 분석의 시작 (Pre-processing) | 분석의 결론 ([[395_verification_process_review|Verification]]) |
| **상호 작용** | EDA에서 발견한 패턴을 CDA에서 [[395_verification_process_review|검증]]하는 상호보완 [[083_relationship_in_er_model|관계]] |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
* **적용 [[268_strategy_pattern|전략]] (Implementation [[268_strategy_pattern|Strategy]])**:
  * **[[283_data_visualization_dashboard_report|데이터 시각화]] 도구 활용**: Python의 Seaborn, Plotly 등을 활용하여 동적 [[003_bigdata_7v|시각화]]를 수행하고, [[001_dikw_pyramid|데이터]]의 층(Layer)별 특징 파악.
  * **반복적 프로세스**: 한 번의 EDA로 끝나지 않고, [[247_feature_label_variables|피처]] 엔지니어링([[081_feature_engineering|Feature Engineering]]) 후에 다시 EDA를 수행하여 [[001_dikw_pyramid|데이터]]의 변화를 지속적으로 관찰.
* **기술사적 판단 (Architectural Judgment)**:
  * 빅데이터 환경에서 모든 행을 [[003_bigdata_7v|시각화]]하는 것은 불가능함. 따라서 신뢰할 수 있는 무작위 샘플링([[056_표본화_Sampling|Sampling]])을 통해 EDA를 수행하거나, [[208_data_lake_schema_on_read|데이터 레이크]]의 [[012_metadata|메타데이터]]를 활용한 '[[613_profiling_gprof|프로파일링]]([[613_profiling_gprof|Profiling]])' 자동화 시스템 구축이 필수적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
EDA는 분석 모델의 품질(Garbage In, Garbage Out 방지)을 결정짓는 가장 중요한 공정입니다. 향후에는 AI가 자동으로 [[001_dikw_pyramid|데이터]]의 특징을 파악하여 가장 적합한 [[003_bigdata_7v|시각화]]와 이상 징후 보고서를 [[087_process_state_transition|생성]]해 주는 'Auto-[[064_eda|EDA]]' 도구들이 [[052_data_governance_framework|데이터 거버넌스]] 시스템의 표준 기능으로 통합될 것입니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
* **[[003_bigdata_7v|시각화]] 기술**: Histogram, Box Plot, Scatter Matrix, Heatmap
* **[[266_data_cleansing|데이터 정제]]**: [[397_outlier_mahalanobis|Outlier Detection]], [[367_missing_value_imputation_mice|Imputation]], Scaling
* **분석 기구**: [[325_correlation_analysis_pearson_spearman|Correlation Analysis]], [[355_random_forest_feature_importance|Feature Importance]], Anscombe's Quartet

### 📈 관련 키워드 및 발전 흐름도

```text
[시각화 기술: Histogram, Box Plot, Scatter Matrix, Heatmap]
    │
    ▼
[데이터 정제: Outlier Detection, Imputation, Scaling]
    │
    ▼
[분석 기구: Correlation Analysis, Feature Importance, Anscombe's Quartet]
```

이 흐름도는 [[003_bigdata_7v|시각화]] 기술: Histogram, Box Plot, Scatter Matrix, Heatmap에서 출발해 분석 기구: [[325_correlation_analysis_pearson_spearman|Correlation Analysis]], [[355_random_forest_feature_importance|Feature Importance]], Anscombe's Quartet까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 낯선 곳으로 여행(분석)을 가기 전에, 지도를 펼쳐보고 어디에 산이 있고 바다가 있는지 훑어보는 것과 같아요.
2. 돋보기를 들고 [[001_dikw_pyramid|데이터]] 속에 숨겨진 보물(패턴)이나 함정([[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]])을 찾는 탐정 놀이와 같답니다.
3. 본격적으로 요리를 시작하기 전에, 재료들이 신선한지 상한 곳은 없는지 꼼꼼히 살펴보는 과정이에요.
