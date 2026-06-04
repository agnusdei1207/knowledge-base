+++
title = "320. GNN + 벡터 DB (Milvus) 기반 추천 시스템"
date = 2026-05-09

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) ([Graph Neural Network](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/), [그래프 신경망](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/306_graph_neural_network_gnn/))은 사용자-아이템 상호작용 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 고차원 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 패턴을 학습하여 [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)의 한계를 극복하고, 벡터 DB ([Vector Database](/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/), Milvus 등)는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터를 고속 [유사도 검색](/knowledge-base/studynote/05_database/06_dw_olap_trends/348_similarity_search/) ([ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/), [Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/))으로 실시간 추천을 제공한다.
> 2. **가치**: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 기반 추천은 사용자와 아이템의 다단계 연결 정보(사용자 A가 구매한 상품의 구매자 B가 본 상품)를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조로 포착하여, MF ([Matrix Factorization](/knowledge-base/studynote/06_ict_convergence/05_data_science/348_matrix_factorization/), 행렬 인수분해) 기반 [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)보다 풍부한 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.
> 3. **판단 포인트**: 벡터 DB의 [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) ([Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/), 근사 최근접 이웃) 검색은 정확한 최근접 이웃 검색보다 빠르지만 약간의 정확도 손실이 있으며, [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/) ([Hierarchical Navigable Small World](/knowledge-base/studynote/05_database/06_dw_olap_trends/352_rag/)) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 속도-정확도 트레이드오프를 조정한다.

---

## Ⅰ. 개요 및 필요성

[추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)은 이커머스, 스트리밍, 소셜 미디어의 핵심 가치 엔진이다. 전통적 [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) ([Collaborative Filtering](/knowledge-base/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/))은 사용자-아이템 상호작용 행렬의 희소성(Sparsity) 문제와 [Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/) (신규 사용자/아이템) 문제가 있었다. MF(행렬 인수분해)로 이를 완화했지만, 2홉 이상의 간접 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 포착하지 못했다.

GNN은 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조에서 여러 홉(hop)의 이웃 정보를 집계([Aggregate](/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/))하여 풍부한 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. LightGCN, PinSage 등의 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 추천 모델이 기존 MF 모델을 크게 뛰어넘는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보였다. [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 고차원 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터를 실시간으로 검색하기 위해 벡터 DB가 필수 인프라로 부상했다.

- **📢 섹션 요약 비유**: [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 "나와 비슷한 사람이 구매한 것" 추천, GNN은 "나와 비슷한 사람이 구매한 것을 함께 구매한 사람이 또 구매한 것"까지 포착하는 심층 연결 분석이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|          GNN + 벡터 DB 기반 추천 시스템 아키텍처                    |
+------------------------------------------------------------------+
|  오프라인 학습 파이프라인 (배치)                                     |
|  사용자-아이템 그래프 구성 (클릭, 구매, 평점 -> 엣지)                 |
|    |                                                              |
|    v                                                              |
|  GNN 학습 (LightGCN, GraphSAGE)                                  |
|  +- 각 노드(사용자·아이템)에 대해 이웃 임베딩 집계                   |
|    |                                                              |
|    v                                                              |
|  임베딩 벡터 생성 (사용자: 128d, 아이템: 128d)                      |
|    |                                                              |
|    v                                                              |
|  벡터 DB 저장 (Milvus/Pinecone: HNSW 인덱스 구축)                  |
|                                                                  |
|  온라인 서빙 파이프라인 (실시간)                                     |
|  사용자 요청 -> 사용자 임베딩 조회 -> ANN 검색 -> Top-K 아이템 반환    |
|  응답: 수백ms -> 재랭킹 (Business Rule 필터) -> 최종 추천 리스트      |
+------------------------------------------------------------------+
```

| [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 모델          | 특성                              | 추천 적합성                   |
|:---------------|:----------------------------------|:-----------------------------|
| LightGCN       | 간단한 선형 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 컨볼루션           | [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)에 최적화           |
| GraphSAGE      | 샘플링 기반 이웃 집계               | 대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), 귀납적 학습     |
| PinSage        | Pinterest의 웹-스케일 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/)          | 이미지 특성 통합, 콘텐츠 추천 |
| NGCF           | [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)에 상호작용 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 통합          | 명시적 협업 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 포착          |

- **📢 섹션 요약 비유**: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)은 사람의 "취향 DNA"를 숫자 벡터로 표현하는 것이다. 비슷한 취향의 사람은 비슷한 벡터를 가진다.

---

## Ⅲ. 비교 및 연결

벡터 DB의 핵심 기술은 [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) ([Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)다. 정확한 최근접 이웃 탐색은 O(n)이지만, [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/) ([Hierarchical Navigable Small World](/knowledge-base/studynote/05_database/06_dw_olap_trends/352_rag/)) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 기반 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 O(log n)에 근사한다.

| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유형   | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)              | 검색 속도  | 정확도  | 메모리   |
|:----------|:--------------------|:---------|:-------|:--------|
| [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)      | 계층적 탐색 가능 소세계 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | 매우 빠름  | 높음   | 높음     |
| IVF-[PQ](/knowledge-base/studynote/03_network/07_network_layer_routing/391_qos_queuing_pq_cq_wfq_cbwfq_llq/)    | 역파일 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) + 곱 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)  | 빠름       | 중간    | 낮음     |
| Flat      | 완전 [선형 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)          | 느림       | 완벽    | 없음 추가|

**Milvus vs Pinecone vs Weaviate**:
- Milvus: [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)/클라우드, 다양한 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 지원
- Pinecone: 완전 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 운영 부담 없음
- Weaviate: 시맨틱 검색 + 벡터 DB 통합, [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) 지원

- **📢 섹션 요약 비유**: HNSW는 지하철 환승 노선처럼 계층적으로 이동하여 목적지(가장 유사한 벡터)를 빠르게 찾는다. 직접 걷는(Flat) 것보다 환승을 활용하는 것이 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/">추천 시스템</a> 설계 단계</strong>:
1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집: 사용자 행동 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) (클릭, 구매, 체류 시간) -> 이분 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구성
2. [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 학습: LightGCN으로 사용자·아이템 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) (주기적 배치 재학습)
3. [벡터 인덱싱](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/300_ann_approximate_nearest_neighbor_vector_index/): Milvus에 아이템 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구축
4. 온라인 서빙: 사용자 요청 -> 사용자 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 조회 -> [Top-K](/knowledge-base/studynote/06_ict_convergence/05_data_science/414_llm_decoder_top_k_temperature/) [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) 검색 -> 비즈니스 필터
5. A/B 테스트: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) vs 기존 MF 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 ([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), CVR 지표)

<strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> 최신성 유지 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>:
- 신규 아이템 ([Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/)): 사이드 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) ([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), 이미지) 기반 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- 온라인 업데이트: 새 상호작용 발생 시 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 점진적 업데이트 (Online [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 연구 분야)
- 주기적 재학습: 일·주 단위 전체 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 재학습 + 벡터 DB 업데이트

- **📢 섹션 요약 비유**: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 최신성은 지도 업데이트와 같다. 너무 오래된 지도([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))는 신규 건물(아이템)이 없어서 길을 잘못 안내한다.

---

## Ⅴ. 기대효과 및 결론

[GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) + 벡터 DB 기반 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)은 MF 기반 대비 클릭률 ([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), Click-Through Rate) 15~30% 향상, 전환율 (CVR, Conversion Rate) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20% 향상을 보고한 사례가 있다. 특히 롱테일 아이템(비인기 상품) 추천 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선 효과가 크다.

한계는 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구축과 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 학습의 계산 복잡도다. 수억 사용자·아이템 규모의 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 학습은 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 클러스터가 필요하며, 실시간 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 업데이트는 여전히 어렵다. 배치 학습 + 실시간 [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) 서빙의 하이브리드 접근이 현실적 해결책이다.

- **📢 섹션 요약 비유**: [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) + 벡터 DB 추천은 최고의 서점 직원이다. 고객의 독서 이력뿐만 아니라 비슷한 취향의 독자들이 함께 읽은 책까지 파악하여 최적의 책을 추천한다.

---

### 📌 관련 개념 맵

| 개념                          | 연결 포인트                              |
|:-----------------------------|:----------------------------------------|
| LightGCN                      | 추천 특화 경량 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 모델                  |
| [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/) ([Hierarchical Navigable Small World](/knowledge-base/studynote/05_database/06_dw_olap_trends/352_rag/)) | 벡터 DB [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) 검색 핵심 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)  |
| [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/) ([Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)) | 벡터 유사도 근사 검색 기법         |
| [Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/)                    | 신규 사용자·아이템의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 문제     |
| [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) ([Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))             | 고차원 의미 정보를 저차원 벡터로 표현     |

### 📈 관련 키워드 및 발전 흐름도

```
협업 필터링 (User-Item 행렬)
    |
    v
행렬 인수분해 (MF, SVD) -> 임베딩 학습
    |
    v
딥러닝 추천 (NCF, DeepFM)
    |
    v
GNN 추천 (LightGCN, PinSage, NGCF)
    |
    v
벡터 DB (Milvus, Pinecone) + ANN 실시간 서빙
    |
    v
LLM + 벡터 DB: RAG (Retrieval-Augmented Generation) 추천
```

### 👶 어린이를 위한 3줄 비유 설명

1. [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) 추천은 "내 친구의 친구가 좋아하는 책"까지 파악해서 나에게 맞는 책을 추천해주는 거예요.
2. 벡터 DB는 수백만 권의 책을 "취향 지도"에 배치해두고, 내 취향과 가장 가까운 책을 순식간에 찾아주는 시스템이에요.
3. AI가 계속 학습해서 내 취향 지도를 업데이트하면, 추천이 점점 정확해져요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 320 / 482

<- **이전**: [319. Apache Airflow DAG 파이프라인 오케스트레이션](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/319_airflow_dag_pipeline/)
**다음**: [321. ISP AS-IS TO-BE 분석 방법론 (ISP Information Strategy Planning)](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/321_isp_as_is_to_be/) ->

---
