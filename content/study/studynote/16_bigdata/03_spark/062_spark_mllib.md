+++
weight = 62
title = "스파크 엠엘립 (Spark MLlib) - 분산 머신러닝 라이브러리"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **스파크 MLlib (Machine [[240_switch_learning_forwarding_flooding|Learning]] [[336_library_vs_framework|Library]])**는 대규모 [[136_variance|분산]] 환경에서 동작하는 고성능 [[241_machine_learning_basics|머신러닝]] [[001_algorithm_definition|알고리즘]] 및 유틸리티를 제공하는 스파크의 핵심 [[603_component_independent_deployment_unit|컴포넌트]]이다.
2. Spark SQL의 DataFrame API를 기반으로 하는 **'ML [[123_pipe|파이프]]라인(ML Pipelines)'** 아키텍처를 도입하여, [[001_dikw_pyramid|데이터]] 변환부터 모델 학습/평가까지의 과정을 표준화한다.
3. 반복적(Iterative) 연산이 많은 [[241_machine_learning_basics|머신러닝]] 특성에 맞춰 **인메모리 연산**을 수행하므로, 기존 [[018_mapreduce|MapReduce]] 기반 도구보다 최대 100배 빠른 [[282_performance_tactics|성능]]을 제공한다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **정의**: 스파크 [[031_에코_반향|에코]]시스템 내에서 [[136_variance|분산]] [[104_classification_analysis|분류]], 회귀, 군집, [[211_recommendation_system|추천 시스템]] 및 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] [[001_algorithm_definition|알고리즘]]을 수행하기 위한 [[336_library_vs_framework|라이브러리]]이다.
- **배경**: 단일 노드 [[241_machine_learning_basics|머신러닝]] [[336_library_vs_framework|라이브러리]](scikit-learn 등)로는 처리 불가능한 '테라바이트(TB) 급 대용량 [[001_dikw_pyramid|데이터]]'를 [[136_variance|분산]] [[430_index_fast_full_scan|병렬]] 학습하기 위해 고안되었다.
- **주요 활용**: 대규모 사용자 대상의 상품 [[211_recommendation_system|추천 시스템]], 실시간 [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 사기 탐지([[267_gnn_fraud_detection_knowledge_graph|FDS]]), 대규모 텍스트 [[001_dikw_pyramid|데이터]]의 [[116_topic_modeling|토픽 모델링]] 등 빅데이터 분석의 최전선에서 활용된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ML [[123_pipe|파이프]]라인([[082_pipeline|Pipeline]]) 구조
```text
[ Raw Data (DataFrame) ]
      |
      V [ Transformer ] (e.g., Tokenizer, Scaler) --> [ Transformed Data ]
      |
      V [ Estimator ] (e.g., Logistic Regression) --> [ Model (Transformer) ]
      |
      V [ Evaluator ] (e.g., BinaryClassificationEvaluator) --> [ Performance Metric ]
```

#### 2. 핵심 [[001_algorithm_definition|알고리즘]] 카테고리
- **[[107_classification|Classification]] & Regression**: [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]], [[353_random_forest|랜덤 포레스트]], GBT(Gradient Boosted Trees), [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 등
- **[[186_graph_db_recommendation_collaborative_filtering_cold_start|Collaborative Filtering]]**: ALS([[349_svd_als_recommendation|Alternating Least Squares]]) 기반의 대규모 [[045_recommendation_system_algorithms|추천 시스템 알고리즘]]
- **[[105_clustering_analysis|Clustering]]**: K-means, Gaussian Mixture, LDA(Latent Dirichlet Allocation) 등
- **[[079_dimensionality_reduction|Dimensionality Reduction]]**: [[163_pca|PCA]]([[338_pca_principal_component_analysis|주성분 분석]]), [[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]]([[342_svd|특이값 분해]])

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Scikit-learn (Python) | Spark MLlib |
| :--- | :--- | :--- |
| **처리 [[001_dikw_pyramid|데이터]] 규모** | 단일 노드 메모리 한계 (GB 수준) | 클러스터 [[136_variance|분산]] 메모리 (TB/PB 수준) |
| **학습 방식** | 단일 CPU/[[418_gpu|GPU]] 위주 학습 | 수백 개의 워커 노드 [[430_index_fast_full_scan|병렬]] 학습 |
| **[[014_api_posix|API]] 편의성** | 매우 높음, [[336_library_vs_framework|라이브러리]] 풍부 | ML [[082_pipeline|Pipeline]] 도입 후 매우 개선됨 |
| **병목 지점** | 연산 속도 및 메모리 부족 | 네트워크 셔플링(Shuffle) 발생 |
| **사용 사례** | 모델 연구 및 중소형 [[001_dikw_pyramid|데이터]] | 대규모 [[067_service_operation|서비스 운영]] 및 배치 학습 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **[[001_dikw_pyramid|데이터]] 엔지니어링의 중요성**: MLlib [[282_performance_tactics|성능]]의 80%는 학습 [[001_algorithm_definition|알고리즘]]보다 앞단의 [[001_dikw_pyramid|데이터]] 전처리(`VectorAssembler` 등)와 [[247_feature_label_variables|피처]] 엔지니어링 효율화에서 결정된다.
- **[[041_bagging_boosting|하이퍼파라미터 튜닝]] 최적화**: `CrossValidator`를 사용한 대규모 [[430_index_fast_full_scan|병렬]] 튜닝 시 클러스터 자원이 급격히 소모될 수 있으므로, [[251_grid_search_random_search|그리드 서치]]([[251_grid_search_random_search|Grid Search]]) 범위를 신중히 [[009_config|설정]]해야 한다.
- **모델 서빙(Serving) [[268_strategy_pattern|전략]]**: 학습된 MLlib 모델을 실시간 추론에 사용할 경우, Spark 클러스터 오버헤드를 피하기 위해 PMML이나 MLeap 같은 표준 포맷으로 익스포트하여 경량 서버에서 서빙하는 방식이 선호된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: [[001_dikw_pyramid|데이터]] 분석가가 복잡한 [[136_variance|분산]] 프로그래밍 지식 없이도 고성능 대규모 [[241_machine_learning_basics|머신러닝]] 시스템을 직접 구축하고 배포할 수 있게 한다.
- **결론**: MLlib은 빅데이터 플랫폼으로서의 스파크의 가치를 완성하는 조각이다. 향후 딥러닝 프레임워크와의 연동(Spark deep [[240_switch_learning_forwarding_flooding|learning]] pipelines) 및 [[136_variance|분산]] 학습 표준화를 통해 [[001_dikw_pyramid|데이터]] 과학의 대중화를 이끌 핵심 기술로 남을 것이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
1. **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]**: [[001_dikw_pyramid|데이터]]를 다른 [[001_dikw_pyramid|데이터]]로 변환하는 [[001_algorithm_definition|알고리즘]] (추론 포함)
2. **Estimator**: [[001_dikw_pyramid|데이터]]를 학습하여 모델([[246_transformer_self_attention_parallel_positional_encoding|Transformer]])을 [[087_process_state_transition|생성]]하는 [[001_algorithm_definition|알고리즘]]
3. **ALS ([[349_svd_als_recommendation|Alternating Least Squares]])**: [[161_matrix_decomposition|행렬 분해]] 기반의 [[211_recommendation_system|추천 시스템]] 핵심 [[001_algorithm_definition|알고리즘]]

---

### 📈 관련 키워드 및 발전 흐름도

```text
[원시 피처 데이터 (Raw Feature Data) — DataFrame·RDD로 메모리 로딩]
    │
    ▼
[피처 엔지니어링 (Feature Engineering) — MLlib Pipeline으로 전처리·변환]
    │
    ▼
[모델 학습 (Model Training) — 분산 클러스터 병렬 알고리즘 수행]
    │
    ▼
[모델 평가 (Model Evaluation) — CrossValidator·TrainValidationSplit]
    │
    ▼
[모델 배포 (Model Serving) — MLflow·Spark Structured Streaming 연동]
```

이 흐름은 Spark MLlib가 [[247_feature_label_variables|피처]] 전처리부터 [[136_variance|분산]] 학습·평가·서빙까지 [[241_machine_learning_basics|머신러닝]] [[123_pipe|파이프]]라인을 일원화하는 과정을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. "전교생 수만 명의 키와 몸무게 [[001_dikw_pyramid|데이터]]를 보고, 어떤 아이가 운동을 잘할지 한꺼번에 알아맞히는 똑똑한 로봇 선생님이에요."
2. "혼자서 공부하는 게 아니라, 친구 로봇 수백 명과 함께 문제를 나눠서 풀기 때문에 아주 빠르게 정답을 찾아요."
3. "이게 바로 커다란 [[001_dikw_pyramid|데이터]]를 공부해서 미래를 예측하는 '엠엘립'이라는 기술이랍니다!"
