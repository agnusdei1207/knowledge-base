+++
title = "358. 계층적 군집화 (Hierarchical Clustering)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)(Hierarchical [Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트들을 단계적으로 병합(Agglomerative, 상향식) 또는 분할(Divisive, 하향식)하여 트리 형태의 덴드로그램(Dendrogram)을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 이를 특정 높이에서 자르면 원하는 군집 수를 얻는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 군집 수 K를 사전에 정하지 않아도 되고, 덴드로그램으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 전체 계층 구조를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하여 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문가가 적절한 군집 수를 사후에 결정할 수 있다.
> 3. **판단 포인트**: 연결 기준(Linkage)으로 단순 연결(Single, 연쇄 효과), 완전 연결(Complete, 컴팩트), 평균 연결(Average, 균형), [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 연결(Ward, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최소화)이 있으며 Ward가 실무 기본값이다.

---

## Ⅰ. 개요 및 필요성

유전체 발현 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 유사한 발현 패턴을 가진 유전자 그룹을 찾거나, 회사 조직도처럼 계층적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)할 때 K-Means 같은 평면적 방법은 계층 구조를 표현하지 못한다. 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 가장 유사한 두 포인트를 묶고, 다시 가장 가까운 두 군집을 묶는 과정을 반복하여 최종적으로 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잇는 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)(덴드로그램)를 만든다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 "족보 만들기"다. 가장 비슷한 두 사람을 먼저 같은 가족으로 묶고, 가족들 중 가장 비슷한 두 가족을 씨족으로 묶고, 씨족들을 부족으로 묶는 과정을 반복해 전체 인류의 족보(덴드로그램)가 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------+
|  병합적 계층 군집화 (Agglomerative Hierarchical Clustering) |
+------------------------------------------------------------+
|  데이터: {A, B, C, D, E}                                   |
|                                                            |
|  Step 1: 거리 행렬 계산 후 가장 가까운 쌍 병합             |
|          {A,B} 병합 -> 새 군집 AB                          |
|  Step 2: AB와 다른 군집 거리 재계산 (Linkage 적용)        |
|          {C,D} 병합                                        |
|  Step 3: {AB,CD} 병합                                     |
|  Step 4: {ABCD, E} 병합                                   |
|                                                            |
|  덴드로그램 (Dendrogram):                                  |
|      E ----------------------+                            |
|      A --+                   |                            |
|      B --+------+            |                            |
|      C --+      +------------+                            |
|      D --+------+                                         |
|  높이(거리)+-------------------------                     |
|  자르면 K개의 군집 선택 가능!                              |
+------------------------------------------------------------+
```

| 연결 기준 | 군집 간 거리 정의 | 특성 | 문제점 |
|:---|:---|:---|:---|
| 단순 연결 (Single) | 최소 거리 | 비구형 탐지 가능 | 연쇄 효과([Chaining](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/)) |
| 완전 연결 (Complete) | 최대 거리 | 컴팩트 구형 군집 | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 영향 큼 |
| 평균 연결 (Average) | 평균 거리 | 균형 잡힌 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | - |
| [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 연결 (Ward) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 증가 최소화 | 구형, 균일 크기 | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 민감 |

- **📢 섹션 요약 비유**: 연결 기준은 "두 도시 간 거리 측정 방식"이다. 단순 연결은 두 도시 중 가장 가까운 두 변두리 간 거리, 완전 연결은 가장 먼 두 끝점 간 거리, [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 합쳐지면 내부 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 얼마나 늘어나는지로 결정한다.

---

## Ⅲ. 비교 및 연결

코팬틱 상관 계수(Cophenetic Correlation Coefficient): 덴드로그램에서 각 쌍의 병합 높이와 실제 거리 행렬의 상관관계로 덴드로그램의 질을 평가(1에 가까울수록 좋음). 코팬틱 계수 > 0.75면 좋은 덴드로그램으로 간주한다. UPGMA(Unweighted Pair Group Method with Arithmetic Mean)는 평균 연결(Average Linkage)의 진화 생물학 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 계통수(Phylogenetic Tree) 구성에 사용된다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) (Hierarchical [Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: 코팬틱 상관은 "지도의 정확도 점수"다. 실제 땅 거리(원래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))와 지도에 그려진 거리(덴드로그램)가 얼마나 잘 맞는지 점수로 평가한다. 1점 만점에 0.75 이상이면 믿을만한 지도다.

---

## Ⅳ. 실무 적용 및 기술사 판단

계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)의 치명적 단점은 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) O(n^ log n)~O(n³)다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개를 넘으면 계산이 불가능해진다. 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서는 Mini-batch K-Means로 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 군집을 만든 뒤, 군집 중심(centroid)에 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)를 적용하는 하이브리드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 사용한다. scipy의 linkage/dendrogram 함수와 scikit-learn의 AgglomerativeClustering으로 구현 가능하다.

- **📢 섹션 요약 비유**: 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)를 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 직접 쓰는 것은 "[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0만 명의 족보를 손으로 그리는 것"이다. 대신 먼저 K-Means로 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0개 가문(군집)을 만든 뒤, 100개 가문 간 족보(계층 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))를 그리는 2단계 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 현실적이다.

---

## Ⅴ. 기대효과 및 결론

계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 내재적 계층 구조를 시각적으로 탐색하는 데 탁월하다. 유전체학, 문서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 마케팅 고객 세분화에서 K개를 몰라도 전체 구조를 파악한 후 적절한 수준에서 자를 수 있다는 유연성이 핵심 강점이다. 기술사 시험에서 4가지 연결 기준의 수식과 장단점, 코팬틱 상관으로 품질 평가하는 방법을 함께 서술하면 완성도 높은 답안이 된다.

- **📢 섹션 요약 비유**: 덴드로그램은 AI의 "진화 계통수"다. 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 조상부터 개별 후손까지 전체 연결 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 한 눈에 보인다. 어느 높이에서 자르느냐에 따라 "과(科)" 수준의 큰 그룹이 될 수도, "종(種)" 수준의 세밀한 그룹이 될 수도 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 덴드로그램 (Dendrogram) | 트리 구조 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) / 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)의 핵심 출력 |
| [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 연결 (Ward Linkage) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최소화 / 실무 기본 연결 기준 |
| K-Means | 평면 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) / 계층 구조 표현 불가, 대비 비교 |
| 코팬틱 상관 | 덴드로그램 품질 / 군집 구조 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 평가 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [계층적 군집화 (Hierarchical Clustering)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 계층적 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 "세상에서 가장 비슷한 친구 두 명을 먼저 짝지어주는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"예요.
2. 짝들을 계속 더 큰 그룹으로 묶어나가면 전체 연결 트리(덴드로그램)가 완성돼요.
3. 이 트리를 원하는 높이에서 자르면 "3개 그룹", "5개 그룹"처럼 원하는 만큼 군집을 만들 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 358 / 420

<- **이전**: [357. DBSCAN (Density-Based Spatial Clustering)](/knowledge-base/studynote/10_ai/05_data_science_ml/357_dbscan/)
**다음**: [359. 코사인 유사도 (Cosine Similarity)](/knowledge-base/studynote/10_ai/05_data_science_ml/359_cosine_similarity_math/) ->

---
