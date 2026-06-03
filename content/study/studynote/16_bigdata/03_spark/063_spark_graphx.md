+++
weight = 63
title = "스파크 그래프엑스 (Spark GraphX) - 분산 그래프 분석"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **스파크 [[070_graph_datastructure|그래프]]엑스 (Spark GraphX)**는 [[070_graph_datastructure|그래프]]([[104_graph|Graph]]) [[001_dikw_pyramid|데이터]]와 컬렉션(Collection) [[001_dikw_pyramid|데이터]]를 통합하여 처리하는 스파크의 [[136_variance|분산]] [[070_graph_datastructure|그래프]] 처리 엔진이다.
2. 정점(Vertex)과 간선(Edge) 정보를 [[430_index_fast_full_scan|병렬]]로 처리하는 **'프로퍼티 [[070_graph_datastructure|그래프]](Property [[104_graph|Graph]])'** 모델을 사용하며, 대규모 소셜 네트워크나 [[160_knowledge_graph_graphrag_integration|지식 그래프]] 분석에 최적화되어 있다.
3. 구글의 **Pregel** 아키텍처를 스파크 상에 구현하여, 복잡한 [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]]을 반복적(Iterative)으로 수행할 때 높은 [[282_performance_tactics|성능]]을 제공한다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **정의**: [[001_dikw_pyramid|데이터]] 간의 복잡한 [[083_relationship_in_er_model|관계]]를 노드(Node)와 링크(Link)로 표현하고, 이를 [[136_variance|분산]] 환경에서 효율적으로 연산하기 위한 스파크 [[336_library_vs_framework|라이브러리]]이다.
- **배경**: 전통적인 표 형식(Table) [[001_dikw_pyramid|데이터]] 처리 방식으로는 수십억 개의 [[083_relationship_in_er_model|관계]]를 가진 [[001_dikw_pyramid|데이터]]의 연결성(Connectivity) 분석에 한계가 있어 이를 보완하기 위해 탄생했다.
- **주요 활용**: 페이스북/링크드인의 친구 추천, 구글의 [[286_page_frame|페이지]]랭크(PageRank) 순위 결정, 사기 결제망 탐지, 단백질 구조 분석 등 초연결 [[001_dikw_pyramid|데이터]] 분석에 필수적이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 프로퍼티 [[070_graph_datastructure|그래프]](Property [[104_graph|Graph]]) 모델
```text
( Vertex A ) --[ Edge ]--> ( Vertex B )
     |                         |
  [Property]                [Property]
 (Name: John)              (Name: Bob)
 (Age: 30)                 (Age: 25)

[ GraphX Object ] = { VertexRDD, EdgeRDD }
```

#### 2. 핵심 연산 및 [[001_algorithm_definition|알고리즘]]
- **Triplet [[151_sql_view_virtual_table|View]]**: 정점-간선-정점을 하나의 단위로 묶어 [[083_relationship_in_er_model|관계]] 기반 연산을 수행한다.
- **PageRank**: 특정 노드의 중요도를 측정하여 순위를 매긴다 (검색 엔진의 핵심).
- **Connected Components**: 서로 연결된 정점들의 그룹(클러스터)을 [[655_ir_detection_analysis|식별]]한다.
- **Triangle Counting**: [[083_relationship_in_er_model|관계]]망 내의 삼각형 구조 개수를 세어 커뮤니티의 밀집도를 측정한다.
- **Pregel [[014_api_posix|API]]**: [[119_message_passing|메시지 전달]] 방식을 통해 정점들이 상태를 주고받으며 전역 해를 찾아가는 반복적 [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]] 프레임워크를 제공한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전용 [[070_graph_datastructure|그래프]] DB (Neo4j) | Spark GraphX |
| :--- | :--- | :--- |
| **목적** | 실시간 [[083_relationship_in_er_model|관계]] [[298_qkv_attention|쿼리]] 및 [[191_transaction_concept_states|트랜잭션]] | 대규모 [[070_graph_datastructure|그래프]] 배치 분석 및 학습 |
| **[[001_dikw_pyramid|데이터]] 규모** | 단일 노드 중심 (클러스터 확장성 제한) | TB/PB급 초대형 [[070_graph_datastructure|그래프]] [[136_variance|분산]] 처리 |
| **유연성** | [[070_graph_datastructure|그래프]] 전용 [[298_qkv_attention|쿼리]](Cypher) 중심 | SQL 및 DataFrame과의 강력한 결합 |
| **속도** | 소수 정점 간의 탐색(Traversing) 우세 | 전체 [[070_graph_datastructure|그래프]] 대상 [[001_algorithm_definition|알고리즘]](PageRank) 우세 |
| **실무 [[268_strategy_pattern|전략]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트 저장소로 활용 | [[001_dikw_pyramid|데이터]] 분석 및 통찰 도출용으로 활용 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **[[001_dikw_pyramid|데이터]] 통합(Unified)의 강점**: GraphX의 최대 장점은 [[215_etl_vs_elt_pipeline|ETL]] 결과물(DataFrame)을 즉시 [[070_graph_datastructure|그래프]]로 변환하고, 분석 결과를 다시 SQL로 조회할 수 있다는 점이다.
- **셔플링과 [[179_table_partitioning_concept|파티셔닝]]**: [[070_graph_datastructure|그래프]] [[001_dikw_pyramid|데이터]]는 연결성 때문에 노드 간 [[001_dikw_pyramid|데이터]] 이동(Shuffle)이 매우 잦다. `PartitionStrategy`를 적절히 [[009_config|설정]]하여 네트워크 비용을 최소화하는 것이 [[282_performance_tactics|성능]] 튜닝의 핵심이다.
- **GraphFrames로의 진화**: 최근에는 [[310_audit|RDD]] 기반의 GraphX보다 DataFrame 기반의 `GraphFrames` [[336_library_vs_framework|라이브러리]]가 더 널리 쓰이며, Spark SQL과의 연동성이 더 뛰어나므로 프로젝트 시작 시 고려해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 개별 [[001_dikw_pyramid|데이터]]의 [[082_attribute_types_er_model|속성]]뿐 아니라 [[001_dikw_pyramid|데이터]] 사이의 '[[083_relationship_in_er_model|관계]]'에서 숨겨진 가치를 찾아냄으로써 비즈니스 통찰의 차원을 한 단계 높인다.
- **결론**: GraphX는 대규모 [[114_graph_analytics|그래프 분석]] 분야의 강력한 표준이다. 향후 [[160_knowledge_graph_graphrag_integration|지식 그래프]]([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])와 [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]]([[263_llm_large_language_model|LLM]])의 결합이 중요해짐에 따라, [[083_relationship_in_er_model|관계]] 기반의 [[001_dikw_pyramid|데이터]] 구조를 처리하는 GraphX의 역할은 더욱 증대될 것이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
1. **VertexRDD / EdgeRDD**: GraphX를 구성하는 두 가지 핵심 [[310_audit|RDD]] [[001_dikw_pyramid|데이터]] 타입
2. **PageRank**: 노드 간의 링크 구조를 분석하여 중요도를 수치화하는 [[001_algorithm_definition|알고리즘]]
3. **Pregel**: [[136_variance|분산]] [[070_graph_datastructure|그래프]] 연산을 위한 '정점 중심(Vertex-centric)' 프로그래밍 모델

---

### 📈 관련 키워드 및 발전 흐름도

```text
[그래프 이론 (Graph Theory) — 정점/엣지 모델]
    │
    ▼
[스파크 GraphX (Apache Spark GraphX) — 분산 그래프 처리]
    │
    ▼
[Pregel API (Pregel Computation Model) — 정점 중심 반복]
    │
    ▼
[PageRank / 연결 요소 (PageRank / Connected Components) — 대표 알고리즘]
    │
    ▼
[그래프프레임즈 (GraphFrames) — 데이터프레임 기반 확장]
```

이 흐름은 [[070_graph_datastructure|그래프]] 이론을 Spark 위에 올려 GraphX와 Pregel로 반복 계산을 수행하고, PageRank와 GraphFrames로 분석 범위를 넓히는 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. "수많은 친구 [[083_relationship_in_er_model|관계]]가 얽힌 학교 지도를 그리는 기술이에요. 누가 가장 인기가 많은지 찾아낼 수 있죠."
2. "점과 선으로 이루어진 복잡한 그물을 아주 커다란 컴퓨터 수백 대가 나눠서 분석하는 거예요."
3. "이게 바로 사람과 물건 사이의 연결 고리를 찾아내는 '[[070_graph_datastructure|그래프]]엑스'라는 대단한 방법이랍니다!"
