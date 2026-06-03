+++
title = "군집화 (Clustering) 분석"
date = 2024-03-20

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a>(Unsupervised):</strong> 정답(Label)이 없는 상태에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 유사성(Similarity/Distance)만을 기준으로 그룹을 나누는 탐색적 기법.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/">응집도</a>와 분리도:</strong> 같은 군집 내의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 가깝게(Intra-cluster), 서로 다른 군집 간의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 멀게(Inter-cluster) 배치하는 것이 핵심 목표임.
- <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 통찰:</strong> 고객 세분화나 [이미지 분할](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/289_image_segmentation/)처럼 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내에 숨겨진 구조와 패턴을 발견하는 데 탁월함.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의:** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트들 간의 거리를 계산하여 유사한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 가진 개체들을 하나의 집단(Cluster)으로 묶는 분석 방법론임.
- **활용 동기:** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특징이 너무 많거나 정답이 명확하지 않을 때, 우선적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 성질을 파악하기 위한 전처리 단계로 활용됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **거리 측정 방식:** Euclidean, Manhattan, [Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) 등.
- <strong>Bilingual <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/">ASCII</a> Diagram:</strong>
```text
[Clustering Process & Results / 군집화 프로세스 및 결과]

   Before Clustering             After Clustering (K-Means)
   (Unlabeled Data)              (Segmented Groups)
   ----------------              ------------------
     .  .   .  .                  ( G1 )      ( G3 )
   .  .   .  .  .                  .  .        .  .
     .  .   .                     .  .          .
   .  .  .  .  .                  ( G2 )
                                   .  .  .

[Major Algorithms / 주요 알고리즘]
1. K-Means: Partitioning based on Centroids (K clusters)
2. Hierarchical: Tree-based grouping (Dendrogram)
3. DBSCAN: Density-based (High density vs Noise)
4. Gaussian Mixture (GMM): Probability-based (Normal Dist.)
```
- **최적의 K 찾기:** Elbow Method ([SSE](/knowledge-base/studynote/03_network/09_application_layer_web_email/481_sse_server_sent_events/) 감소폭), [Silhouette Score](/knowledge-base/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/) ([응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)/분리도 지수).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | K-Means 군집화 | [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) (밀도 기반) | [계층적 군집화](/knowledge-base/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/) |
| :--- | :--- | :--- | :--- |
| **군집 형성 방식** | 중심점(Centroid) 기준 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 밀도 기준 | 계층적 트리 구조 |
| **장점 (Pros)** | 연산이 매우 빠름 | 비정형 모양(Crescent) 가능 | 군집 수를 미리 정할 필요 없음 |
| **단점 (Cons)** | K값을 미리 정해야 함 | 파라미터(eps) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 민감 | 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시 연산 부하 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a>(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">Outlier</a>) 처리</strong> | 취약 (평균 왜곡) | 강함 (Noise로 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)) | 중간 |
| **비유 (Analogy)** | 반장 선거하기 | 사람들 모여있는 곳 찾기 | 가족 족보 그리기 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong>군집 타당성(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>) 평가:</strong> [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)과 달리 정답이 없으므로 <strong>실루엣 계수</strong>가 0.5 이상인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 각 군집의 비즈니스적 의미(예: VIP 고객, 이탈 위험군)를 해석하는 과정이 필수적임.
- <strong>차원의 저주(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/080_curse_of_dimensionality/">Curse of Dimensionality</a>):</strong> 변수가 너무 많으면 거리 계산의 의미가 사라지므로, 군집화 전 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a></strong>나 <strong>t-SNE</strong>를 통한 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 전처리가 기술사적 권고 사항임.
- <strong>하이브리드 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>:</strong> 군집화 결과를 새로운 변수(Label)로 사용하여 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) 모델에 입력값으로 넣는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인(Stacking) 구성도 효과적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- <strong>초개인화 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>:</strong> 타겟 마케팅이나 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)의 기초가 되어 고객 만족도를 극대화함.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 향상:</strong> [이상치 탐지](/knowledge-base/studynote/10_ai/05_data_science_ml/397_outlier_mahalanobis/)를 통해 [데이터 정제](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/)(Cleaning)의 정확도를 높임.
- **결론:** 군집화는 빅데이터 분석의 출발점이며, 최근에는 딥러닝 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터와 결합하여 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(이미지, 텍스트)의 고차원 군집화로 발전하고 있음.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/), [Data Mining](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/284_data_mining_association_classification_clustering_crisp_dm/)
- **하위 개념:** K-Means++, Dendrogram, [Silhouette Score](/knowledge-base/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/)
- **연관 기술:** [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/)), [Mahalanobis Distance](/knowledge-base/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/), [Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) [Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비지도 학습 (Unsupervised Learning)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">클러스터링 (Clustering)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">K-평균 (K-Means)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">실루엣 계수 (Silhouette Score)</div></div>
</div>
</div>



이 흐름도는 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)에서 클러스터링과 K-평균, 실루엣 계수로 평가가 이어지는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. **장난감 정리 비유:** 뒤섞인 블록들을 색깔별로 모으거나, 크기가 비슷한 인형끼리 모아서 정리 상자에 담는 거예요.
2. **운동장 비유:** 운동장에 모인 학생들 중에서 친한 친구들끼리 동그랗게 모여 보라고 하는 것과 같아요.
3. **옷 정리 비유:** 계절에 맞춰 여름 옷은 여름 옷끼리, 겨울 옷은 겨울 옷끼리 옷장에 따로 넣어두는 마법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 105 / 262

← **이전**: [분류 (Classification) 분석](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)
**다음**: [103. 연관 규칙 (Association Rules) — Apriori/FP-Growth 장바구니 분석](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/) →

---
