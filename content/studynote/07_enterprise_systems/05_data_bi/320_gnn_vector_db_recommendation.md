---
title: 320. GNN + 벡터 DB (Milvus) 기반 추천 시스템
date: '2026-05-09'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]], [[306_graph_neural_network_gnn|그래프 신경망]])은 사용자-아이템 상호작용 [[070_graph_datastructure|그래프]]에서 고차원 [[083_relationship_in_er_model|관계]] 패턴을 학습하여 [[345_collaborative_filtering|협업 필터링]]의 한계를 극복하고, 벡터 DB ([[223_vector_database_embedding|Vector Database]], Milvus 등)는 [[087_process_state_transition|생성]]된 [[278_instruction_tuning|임베딩]] 벡터를 고속 [[348_similarity_search|유사도 검색]] ([[350_ann|ANN]], [[351_hnsw|Approximate Nearest Neighbor]])으로 실시간 추천을 제공한다.
> 2. **가치**: [[159_gnn_graph_neural_network_message_passing|GNN]] 기반 추천은 사용자와 아이템의 다단계 연결 정보(사용자 A가 구매한 상품의 구매자 B가 본 상품)를 [[070_graph_datastructure|그래프]] 구조로 포착하여, MF ([[348_matrix_factorization|Matrix Factorization]], 행렬 인수분해) 기반 [[345_collaborative_filtering|협업 필터링]]보다 풍부한 [[033_context|컨텍스트]] [[278_instruction_tuning|임베딩]]을 [[087_process_state_transition|생성]]한다.
> 3. **판단 포인트**: 벡터 DB의 [[350_ann|ANN]] ([[351_hnsw|Approximate Nearest Neighbor]], 근사 최근접 이웃) 검색은 정확한 최근접 이웃 검색보다 빠르지만 약간의 정확도 손실이 있으며, [[351_hnsw|HNSW]] ([[352_rag|Hierarchical Navigable Small World]]) [[070_graph_datastructure|그래프]] [[154_database_index_b_tree_search_optimization|인덱스]]로 속도-정확도 트레이드오프를 조정한다.

---

## Ⅰ. 개요 및 필요성

[[211_recommendation_system|추천 시스템]]은 이커머스, 스트리밍, 소셜 미디어의 핵심 가치 엔진이다. 전통적 [[345_collaborative_filtering|협업 필터링]] ([[186_graph_db_recommendation_collaborative_filtering_cold_start|Collaborative Filtering]])은 사용자-아이템 상호작용 행렬의 희소성(Sparsity) 문제와 [[347_cold_start_problem|Cold Start]] (신규 사용자/아이템) 문제가 있었다. MF(행렬 인수분해)로 이를 완화했지만, 2홉 이상의 간접 [[083_relationship_in_er_model|관계]]는 포착하지 못했다.

GNN은 [[070_graph_datastructure|그래프]] 구조에서 여러 홉(hop)의 이웃 정보를 집계([[222_aggregate_ddd_transaction_consistency|Aggregate]])하여 풍부한 [[278_instruction_tuning|임베딩]]을 [[087_process_state_transition|생성]]한다. LightGCN, PinSage 등의 [[159_gnn_graph_neural_network_message_passing|GNN]] 추천 모델이 기존 MF 모델을 크게 뛰어넘는 [[282_performance_tactics|성능]]을 보였다. [[087_process_state_transition|생성]]된 고차원 [[278_instruction_tuning|임베딩]] 벡터를 실시간으로 검색하기 위해 벡터 DB가 필수 인프라로 부상했다.

- **📢 섹션 요약 비유**: [[345_collaborative_filtering|협업 필터링]]은 "나와 비슷한 사람이 구매한 것" 추천, GNN은 "나와 비슷한 사람이 구매한 것을 함께 구매한 사람이 또 구매한 것"까지 포착하는 심층 연결 분석이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│          GNN + 벡터 DB 기반 추천 시스템 아키텍처                    │
├──────────────────────────────────────────────────────────────────┤
│  오프라인 학습 파이프라인 (배치)                                     │
│  사용자-아이템 그래프 구성 (클릭, 구매, 평점 → 엣지)                 │
│    │                                                              │
│    ▼                                                              │
│  GNN 학습 (LightGCN, GraphSAGE)                                  │
│  └─ 각 노드(사용자·아이템)에 대해 이웃 임베딩 집계                   │
│    │                                                              │
│    ▼                                                              │
│  임베딩 벡터 생성 (사용자: 128d, 아이템: 128d)                      │
│    │                                                              │
│    ▼                                                              │
│  벡터 DB 저장 (Milvus/Pinecone: HNSW 인덱스 구축)                  │
│                                                                  │
│  온라인 서빙 파이프라인 (실시간)                                     │
│  사용자 요청 → 사용자 임베딩 조회 → ANN 검색 → Top-K 아이템 반환    │
│  응답: 수백ms → 재랭킹 (Business Rule 필터) → 최종 추천 리스트      │
└──────────────────────────────────────────────────────────────────┘
```

| [[159_gnn_graph_neural_network_message_passing|GNN]] 모델          | 특성                              | 추천 적합성                   |
|:---------------|:----------------------------------|:-----------------------------|
| LightGCN       | 간단한 선형 [[070_graph_datastructure|그래프]] 컨볼루션           | [[345_collaborative_filtering|협업 필터링]]에 최적화           |
| GraphSAGE      | 샘플링 기반 이웃 집계               | 대규모 [[070_graph_datastructure|그래프]], 귀납적 학습     |
| PinSage        | Pinterest의 웹-스케일 [[159_gnn_graph_neural_network_message_passing|GNN]]          | 이미지 특성 통합, 콘텐츠 추천 |
| NGCF           | [[278_instruction_tuning|임베딩]]에 상호작용 [[130_signal|신호]] 통합          | 명시적 협업 [[083_relationship_in_er_model|관계]] 포착          |

- **📢 섹션 요약 비유**: [[159_gnn_graph_neural_network_message_passing|GNN]] [[278_instruction_tuning|임베딩]]은 사람의 "취향 DNA"를 숫자 벡터로 표현하는 것이다. 비슷한 취향의 사람은 비슷한 벡터를 가진다.

---

## Ⅲ. 비교 및 연결

벡터 DB의 핵심 기술은 [[350_ann|ANN]] ([[351_hnsw|Approximate Nearest Neighbor]]) [[154_database_index_b_tree_search_optimization|인덱스]]다. 정확한 최근접 이웃 탐색은 O(n)이지만, [[351_hnsw|HNSW]] ([[352_rag|Hierarchical Navigable Small World]]) [[070_graph_datastructure|그래프]] 기반 [[154_database_index_b_tree_search_optimization|인덱스]]는 O(log n)에 근사한다.

| [[154_database_index_b_tree_search_optimization|인덱스]] 유형   | [[001_algorithm_definition|알고리즘]]              | 검색 속도  | 정확도  | 메모리   |
|:----------|:--------------------|:---------|:-------|:--------|
| [[351_hnsw|HNSW]]      | 계층적 탐색 가능 소세계 [[070_graph_datastructure|그래프]] | 매우 빠름  | 높음   | 높음     |
| IVF-[[391_qos_queuing_pq_cq_wfq_cbwfq_llq|PQ]]    | 역파일 [[154_database_index_b_tree_search_optimization|인덱스]] + 곱 [[434_quantization|양자화]]  | 빠름       | 중간    | 낮음     |
| Flat      | 완전 [[030_linear_search|선형 탐색]]          | 느림       | 완벽    | 없음 추가|

**Milvus vs Pinecone vs Weaviate**:
- Milvus: [[191_oss_license_compliance|오픈소스]], [[061_on_premise_legacy_infrastructure|온프레미스]]/클라우드, 다양한 [[154_database_index_b_tree_search_optimization|인덱스]] 지원
- Pinecone: 완전 관리형 [[090_service_kubernetes_network_load_balancing|서비스]], 운영 부담 없음
- Weaviate: 시맨틱 검색 + 벡터 DB 통합, [[158_multimodal_clip_vision_audio_encoding|멀티모달]] 지원

- **📢 섹션 요약 비유**: HNSW는 지하철 환승 노선처럼 계층적으로 이동하여 목적지(가장 유사한 벡터)를 빠르게 찾는다. 직접 걷는(Flat) 것보다 환승을 활용하는 것이 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[211_recommendation_system|추천 시스템]] 설계 단계**:
1. [[001_dikw_pyramid|데이터]] 수집: 사용자 행동 [[568_logs_distributed_logging_elk_fluentd|로그]] (클릭, 구매, 체류 시간) → 이분 [[070_graph_datastructure|그래프]] 구성
2. [[159_gnn_graph_neural_network_message_passing|GNN]] 학습: LightGCN으로 사용자·아이템 [[278_instruction_tuning|임베딩]] [[087_process_state_transition|생성]] (주기적 배치 재학습)
3. [[300_ann_approximate_nearest_neighbor_vector_index|벡터 인덱싱]]: Milvus에 아이템 [[278_instruction_tuning|임베딩]] [[351_hnsw|HNSW]] [[154_database_index_b_tree_search_optimization|인덱스]] 구축
4. 온라인 서빙: 사용자 요청 → 사용자 [[278_instruction_tuning|임베딩]] 조회 → [[414_llm_decoder_top_k_temperature|Top-K]] [[350_ann|ANN]] 검색 → 비즈니스 필터
5. A/B 테스트: [[159_gnn_graph_neural_network_message_passing|GNN]] vs 기존 MF 모델 [[282_performance_tactics|성능]] 비교 ([[090_ctr_mode|CTR]], CVR 지표)

**[[278_instruction_tuning|임베딩]] 최신성 유지 [[268_strategy_pattern|전략]]**:
- 신규 아이템 ([[347_cold_start_problem|Cold Start]]): 사이드 [[247_feature_label_variables|피처]] ([[012_metadata|메타데이터]], 이미지) 기반 [[459_quic_fec_forward_error_correction|초기]] [[278_instruction_tuning|임베딩]] [[087_process_state_transition|생성]]
- 온라인 업데이트: 새 상호작용 발생 시 [[278_instruction_tuning|임베딩]] 점진적 업데이트 (Online [[159_gnn_graph_neural_network_message_passing|GNN]] 연구 분야)
- 주기적 재학습: 일·주 단위 전체 [[159_gnn_graph_neural_network_message_passing|GNN]] 재학습 + 벡터 DB 업데이트

- **📢 섹션 요약 비유**: [[159_gnn_graph_neural_network_message_passing|GNN]] [[278_instruction_tuning|임베딩]] 최신성은 지도 업데이트와 같다. 너무 오래된 지도([[278_instruction_tuning|임베딩]])는 신규 건물(아이템)이 없어서 길을 잘못 안내한다.

---

## Ⅴ. 기대효과 및 결론

[[159_gnn_graph_neural_network_message_passing|GNN]] + 벡터 DB 기반 [[211_recommendation_system|추천 시스템]]은 MF 기반 대비 클릭률 ([[090_ctr_mode|CTR]], Click-Through Rate) 15~30% 향상, 전환율 (CVR, Conversion Rate) [[489_raid_10_hybrid|10]]~20% 향상을 보고한 사례가 있다. 특히 롱테일 아이템(비인기 상품) 추천 [[282_performance_tactics|성능]] 개선 효과가 크다.

한계는 [[070_graph_datastructure|그래프]] 구축과 [[159_gnn_graph_neural_network_message_passing|GNN]] 학습의 계산 복잡도다. 수억 사용자·아이템 규모의 [[070_graph_datastructure|그래프]] 학습은 [[418_gpu|GPU]] 클러스터가 필요하며, 실시간 [[278_instruction_tuning|임베딩]] 업데이트는 여전히 어렵다. 배치 학습 + 실시간 [[350_ann|ANN]] 서빙의 하이브리드 접근이 현실적 해결책이다.

- **📢 섹션 요약 비유**: [[159_gnn_graph_neural_network_message_passing|GNN]] + 벡터 DB 추천은 최고의 서점 직원이다. 고객의 독서 이력뿐만 아니라 비슷한 취향의 독자들이 함께 읽은 책까지 파악하여 최적의 책을 추천한다.

---

### 📌 관련 개념 맵

| 개념                          | 연결 포인트                              |
|:-----------------------------|:----------------------------------------|
| LightGCN                      | 추천 특화 경량 [[159_gnn_graph_neural_network_message_passing|GNN]] 모델                  |
| [[351_hnsw|HNSW]] ([[352_rag|Hierarchical Navigable Small World]]) | 벡터 DB [[350_ann|ANN]] 검색 핵심 [[154_database_index_b_tree_search_optimization|인덱스]]  |
| [[350_ann|ANN]] ([[351_hnsw|Approximate Nearest Neighbor]]) | 벡터 유사도 근사 검색 기법         |
| [[347_cold_start_problem|Cold Start]]                    | 신규 사용자·아이템의 [[459_quic_fec_forward_error_correction|초기]] [[278_instruction_tuning|임베딩]] 문제     |
| [[278_instruction_tuning|임베딩]] ([[278_instruction_tuning|Embedding]])             | 고차원 의미 정보를 저차원 벡터로 표현     |

### 📈 관련 키워드 및 발전 흐름도

```
협업 필터링 (User-Item 행렬)
    │
    ▼
행렬 인수분해 (MF, SVD) → 임베딩 학습
    │
    ▼
딥러닝 추천 (NCF, DeepFM)
    │
    ▼
GNN 추천 (LightGCN, PinSage, NGCF)
    │
    ▼
벡터 DB (Milvus, Pinecone) + ANN 실시간 서빙
    │
    ▼
LLM + 벡터 DB: RAG (Retrieval-Augmented Generation) 추천
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[159_gnn_graph_neural_network_message_passing|GNN]] 추천은 "내 친구의 친구가 좋아하는 책"까지 파악해서 나에게 맞는 책을 추천해주는 거예요.
2. 벡터 DB는 수백만 권의 책을 "취향 지도"에 배치해두고, 내 취향과 가장 가까운 책을 순식간에 찾아주는 시스템이에요.
3. AI가 계속 학습해서 내 취향 지도를 업데이트하면, 추천이 점점 정확해져요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 320 / 482

← **이전**: [[319_airflow_dag_pipeline|319. Apache Airflow DAG 파이프라인 오케스트레이션]]
**다음**: [[321_isp_as_is_to_be|321. ISP AS-IS TO-BE 분석 방법론 (ISP Information Strategy Planning)]] →

---
