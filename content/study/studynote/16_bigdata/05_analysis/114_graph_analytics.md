+++
weight = 114
title = "111. 그래프 분석 (Graph Analytics) — PageRank/커뮤니티 탐지/최단 경로"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[070_graph_datastructure|그래프]] 분석 ([[104_graph|Graph]] Analytics)은 노드 (Node)와 엣지 (Edge)로 구성된 [[070_graph_datastructure|그래프]] 구조 [[001_dikw_pyramid|데이터]]에서 PageRank·커뮤니티 탐지·최단 경로·삼각형 수 (Triangle Count) 등의 [[001_algorithm_definition|알고리즘]]을 적용하여 구조적 패턴과 영향력을 분석하는 기법이다.
> 2. **가치**: [[160_knowledge_graph_graphrag_integration|지식 그래프]] ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]]), 소셜 네트워크, [[520_supply_chain_attack_and_ci_cd_security|공급망]], 사기 탐지 네트워크, [[211_recommendation_system|추천 시스템]] 등 [[083_relationship_in_er_model|관계]]가 본질인 모든 [[001_dikw_pyramid|데이터]]에서 일반 테이블 기반 분석이 놓치는 구조적 인사이트를 제공한다.
> 3. **판단 포인트**: 소규모 [[070_graph_datastructure|그래프]]는 NetworkX, 대규모 [[136_variance|분산]] 처리는 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX·[[215_flink_native_stream_watermark_window_time|Apache Flink]] Gelly, 실시간 [[070_graph_datastructure|그래프]] [[298_qkv_attention|쿼리]]는 TigerGraph·Amazon Neptune을 선택하며, [[082_attribute_types_er_model|속성]] [[070_graph_datastructure|그래프]] (Property [[104_graph|Graph]]) vs RDF (Resource Description Framework) 모델 선택이 아키텍처의 핵심이다.

---

## Ⅰ. 개요 및 필요성

구글 검색의 핵심인 PageRank, 페이스북의 친구 추천, 넷플릭스의 영화 추천, 금융 사기 탐지—이 모두는 [[001_dikw_pyramid|데이터]]를 [[070_graph_datastructure|그래프]]로 보는 관점에서 태어났다. 테이블에 저장된 [[001_dikw_pyramid|데이터]]는 "각 행의 [[082_attribute_types_er_model|속성]]"을 잘 표현하지만, "행들 간의 [[083_relationship_in_er_model|관계]]"는 조인을 거듭해도 한계가 있다.

[[070_graph_datastructure|그래프]] 분석은 "[[083_relationship_in_er_model|관계]] 자체가 [[001_dikw_pyramid|데이터]]"라는 인식의 전환에서 비롯된다. 노드가 수십억 개이고 엣지가 수천억 개인 소셜 [[070_graph_datastructure|그래프]]나 [[160_knowledge_graph_graphrag_integration|지식 그래프]]에서 의미 있는 패턴을 찾으려면 [[070_graph_datastructure|그래프]] 전용 처리 엔진이 필수다.

- **📢 섹션 요약 비유**: [[070_graph_datastructure|그래프]] 분석은 사람들이 서로 어떻게 연결돼 있는지 보여주는 지도다. 테이블이 이름표를 모은 서랍장이라면, [[070_graph_datastructure|그래프]]는 사람들이 실제로 걸어 다니는 도시 지도다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]] [[104_classification_analysis|분류]]

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    핵심 그래프 알고리즘                               │
├─────────────────────┬──────────────────────┬─────────────────────────┤
│  중심성 알고리즘    │  커뮤니티 탐지        │  경로 알고리즘          │
├─────────────────────┼──────────────────────┼─────────────────────────┤
│  PageRank           │  Louvain             │  BFS (너비 우선 탐색)   │
│  (연결 권위도)      │  (모듈러리티 최적화) │  (최단 홉 수)           │
│                     │                      │                         │
│  Betweenness        │  Label Propagation   │  Dijkstra               │
│  (매개 중심성)      │  (레이블 전파)       │  (가중 최단 경로)       │
│                     │                      │                         │
│  Eigenvector        │  Girvan-Newman       │  A* (휴리스틱)          │
│  (고유벡터 중심성)  │  (엣지 제거)         │  (GPS 내비게이션)       │
├─────────────────────┴──────────────────────┴─────────────────────────┤
│  삼각형 수 (Triangle Count): 군집 계수 → 사기 탐지, 커뮤니티 밀도   │
│  WCC (Weakly Connected Component): 연결 요소 탐지 → 고립 클러스터   │
└──────────────────────────────────────────────────────────────────────┘
```

### PageRank 원리

```text
PR(u) = (1-d)/N + d × Σ [PR(v) / OutDegree(v)]
        (for all v pointing to u)

d = 감쇠 계수 (Damping Factor) ≈ 0.85
N = 전체 노드 수
→ "권위 있는 노드(높은 PR)로부터 연결받을수록 PR이 높아진다"
```

### [[070_graph_datastructure|그래프]] [[014_data_model_components|데이터 모델]] 비교

| 모델 | 구조 | 특징 | 적합 사용처 |
|:---|:---|:---|:---|
| **[[082_attribute_types_er_model|속성]] [[070_graph_datastructure|그래프]] (Property [[104_graph|Graph]])** | 노드/엣지 + [[082_attribute_types_er_model|속성]]([[067_db_key_uniqueness_minimality|key]]-value) | 직관적, [[484_elt_extract_load_transform|성능 우수]] | 소셜 네트워크, 추천 |
| **RDF (Resource Description Framework)** | 주어-술어-목적어 트리플 | [[003_semantic_web|시맨틱 웹]], 표준화 | [[160_knowledge_graph_graphrag_integration|지식 그래프]], 온톨로지 |
| **하이퍼그래프 (Hypergraph)** | 하나의 엣지가 다수 노드 연결 | 복잡한 다자 [[083_relationship_in_er_model|관계]] | 협업 네트워크 |

- **📢 섹션 요약 비유**: PageRank는 학문 논문 인용 [[083_relationship_in_er_model|관계]]에서 영감을 얻었다. 많이 인용되는 논문이 중요한 것처럼, 권위 있는 사이트에서 링크를 받는 [[286_page_frame|페이지]]가 중요하다는 [[369_logic_bomb|논리]]다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[070_graph_datastructure|그래프]] DB (Neo4j/Neptune) | RDBMS | [[070_graph_datastructure|그래프]] 처리 엔진 (GraphX/Gelly) |
|:---|:---|:---|:---|
| **최적화 대상** | [[083_relationship_in_er_model|관계]] 탐색 [[298_qkv_attention|쿼리]] | 집계·[[191_transaction_concept_states|트랜잭션]] | 대규모 [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]] |
| **[[298_qkv_attention|쿼리]] 언어** | Cypher / Gremlin / SPARQL | SQL | [[014_api_posix|API]] (GraphX/Pregel) |
| **확장성** | 수십억 노드까지 (수직 확장) | 테이블 조인 한계 | 수천억 노드 (수평 [[136_variance|분산]]) |
| **실시간 처리** | 밀리초 수준 | 조인 증가시 느려짐 | 배치 중심 (실시간은 Flink) |
| **사용 사례** | 추천, 사기 탐지, KG | [[081_erp_enterprise_resource_planning|ERP]], [[107_crm_customer_relationship_management|CRM]] | 소셜 [[070_graph_datastructure|그래프]] 분석, PageRank |

[[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]])과 [[070_graph_datastructure|그래프]] 분석의 결합이 최신 트렌드다. GNN은 노드의 [[247_feature_label_variables|피처]]와 [[070_graph_datastructure|그래프]] 구조를 동시에 학습하여 링크 예측 (Link Prediction), 노드 [[104_classification_analysis|분류]] (Node [[107_classification|Classification]]), [[070_graph_datastructure|그래프]] [[104_classification_analysis|분류]]에서 우수한 [[282_performance_tactics|성능]]을 보인다.

- **📢 섹션 요약 비유**: [[070_graph_datastructure|그래프]] DB는 빠른 [[083_relationship_in_er_model|관계]] 탐색에 특화된 지도 앱이고, [[070_graph_datastructure|그래프]] 처리 엔진은 수십억 명의 이동 패턴을 통계로 분석하는 빅데이터 시스템이다. 목적이 다르면 도구도 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. **[[160_knowledge_graph_graphrag_integration|지식 그래프]] ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])**: 엔티티와 [[083_relationship_in_er_model|관계]]를 RDF/[[082_attribute_types_er_model|속성]] [[070_graph_datastructure|그래프]]로 구축 → 검색 엔진 강화, 추천 연계
2. **금융 사기 공모 탐지**: 계좌-거래 [[070_graph_datastructure|그래프]]에서 밀집 커뮤니티 = 공모 그룹 자동 탐지
3. **[[520_supply_chain_attack_and_ci_cd_security|공급망]] [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 분석**: 공급업체-부품 의존성 [[070_graph_datastructure|그래프]] → 단일 공급업체 의존 취약점 [[003_bigdata_7v|시각화]]
4. **[[211_recommendation_system|추천 시스템]]**: 사용자-상품 이분 [[070_graph_datastructure|그래프]] (Bipartite [[104_graph|Graph]]) + PageRank → 개인화 추천

### [[136_variance|분산]] 처리 플랫폼

| 플랫폼 | 특징 | 규모 |
|:---|:---|:---|
| **[[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX** | Pregel [[014_api_posix|API]], [[310_audit|RDD]] 기반, Scala/Python | 수십억 노드 |
| **[[215_flink_native_stream_watermark_window_time|Apache Flink]] Gelly** | 스트리밍 [[070_graph_datastructure|그래프]] 처리, 이터레이티브 | 실시간 수십억 |
| **TigerGraph** | 실시간 [[070_graph_datastructure|그래프]] [[298_qkv_attention|쿼리]] DB, GSQL | 실시간 수천억 |
| **Amazon Neptune** | 관리형 [[070_graph_datastructure|그래프]] DB, Property + RDF | 클라우드 완전관리형 |
| **NetworkX** | Python [[336_library_vs_framework|라이브러리]], 단일 머신 | 수백만 노드 |

- **📢 섹션 요약 비유**: [[070_graph_datastructure|그래프]] 분석 플랫폼 선택은 용도에 따라 달라진다. 프로토타이핑은 NetworkX, 대규모 배치 분석은 GraphX, 실시간 [[298_qkv_attention|쿼리]]는 TigerGraph, 완전 관리형 클라우드는 Amazon Neptune이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 숨겨진 [[083_relationship_in_er_model|관계]] 발굴 | 테이블 분석으로는 보이지 않는 N단계 간접 연결 탐지 |
| 사기 탐지 정확도 | 공모 패턴의 구조적 특징 자동 인식으로 미탐 감소 |
| 추천 품질 향상 | [[345_collaborative_filtering|협업 필터링]] + [[070_graph_datastructure|그래프]] 구조 결합으로 다양성 개선 |
| [[008_knowledge_base_inference_engine|지식 베이스]] 구축 | [[160_knowledge_graph_graphrag_integration|지식 그래프]]로 조직 내 [[136_variance|분산]] 지식을 통합 |
| [[520_supply_chain_attack_and_ci_cd_security|공급망]] 가시성 | N차 공급업체까지 의존성 추적으로 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 사전 파악 |

[[070_graph_datastructure|그래프]] 분석은 "모든 것은 연결돼 있다"는 인식의 수학적 구현이다. 기존 테이블 기반 [[001_dikw_pyramid|데이터]] 분석 패러다임으로는 접근할 수 없던 [[083_relationship_in_er_model|관계]] 구조 문제에 대한 체계적 해법을 제공한다. GNN의 부상으로 전통 [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]]과 딥러닝의 경계가 사라지고 있으며, 이 둘의 결합이 [[160_knowledge_graph_graphrag_integration|지식 그래프]]·[[211_recommendation_system|추천 시스템]]·생명공학 연구의 미래를 열고 있다.

- **📢 섹션 요약 비유**: [[070_graph_datastructure|그래프]] 분석은 세상의 복잡한 연결망을 이해하는 현미경이다. 사람들이 어떻게 연결돼 있는지, 정보가 어떻게 흐르는지, 위험이 어디서 전파되는지를 한눈에 볼 수 있게 해준다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| PageRank | 구글 검색의 핵심, 연결 권위도 측정 |
| Louvain [[001_algorithm_definition|알고리즘]] | 대규모 커뮤니티 탐지 표준 [[001_algorithm_definition|알고리즘]] |
| [[036_dijkstra|Dijkstra]] [[001_algorithm_definition|알고리즘]] | 가중 [[070_graph_datastructure|그래프]] 최단 경로 탐색 |
| [[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]]) | [[070_graph_datastructure|그래프]] 구조 + 딥러닝의 결합 |
| [[160_knowledge_graph_graphrag_integration|지식 그래프]] ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]]) | 엔티티-[[083_relationship_in_er_model|관계]] 구조로 [[007_knowledge_representation|지식 표현]] |
| [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX | [[136_variance|분산]] 환경 대규모 [[070_graph_datastructure|그래프]] 처리 |
| RDF (Resource Description Framework) | [[003_semantic_web|시맨틱 웹]] 표준 [[070_graph_datastructure|그래프]] [[014_data_model_components|데이터 모델]] |


### 📈 관련 키워드 및 발전 흐름도

```text
[그래프 이론 (Graph Theory) — 정점(Vertex)·간선(Edge)으로 관계를 수학적 표현]
    │
    ▼
[그래프 분석 (Graph Analytics) — PageRank·커뮤니티 탐지·최단 경로 등 관계 패턴 발굴]
    │
    ▼
[Apache Spark GraphX / Pregel — 대규모 그래프의 분산 병렬 처리 프레임워크]
    │
    ▼
[지식 그래프 (Knowledge Graph) — RDF/OWL 기반 엔티티-관계 구조화, 의미 추론]
    │
    ▼
[GNN (Graph Neural Network) — 그래프 구조 + 딥러닝, 분자설계·사기탐지·추천시스템 적용]
```

이 흐름은 [[070_graph_datastructure|그래프]] 이론의 수학적 기반에서 출발해 [[136_variance|분산]] 처리 프레임워크로 대규모 분석을 가능케 하고, [[160_knowledge_graph_graphrag_integration|지식 그래프]]의 의미 추론과 GNN의 딥러닝 결합으로 진화하는 [[070_graph_datastructure|그래프]] [[001_dikw_pyramid|데이터]] 활용 기술의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- [[070_graph_datastructure|그래프]] 분석은 사람들 사이의 친구 [[083_relationship_in_er_model|관계]]를 선으로 그려서 누가 제일 인기 있고, 어떤 그룹이 있는지 찾는 거예요.
- PageRank는 "유명한 친구가 많은 사람이 더 유명하다"는 원리로 웹페이지의 중요도를 계산해요.
- 구글 검색, 페이스북 친구 추천, 배달 앱 최단 경로가 모두 이 기술을 사용해요!
