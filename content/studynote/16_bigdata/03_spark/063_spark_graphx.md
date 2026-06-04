+++
title = "스파크 그래프엑스 (Spark GraphX) - 분산 그래프 분석"
date = 2026-04-05

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. <strong>스파크 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>엑스 (Spark GraphX)</strong>는 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 컬렉션(Collection) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통합하여 처리하는 스파크의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 엔진이다.
2. 정점(Vertex)과 간선(Edge) 정보를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 처리하는 <strong>'프로퍼티 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>(Property <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/">Graph</a>)'</strong> 모델을 사용하며, 대규모 소셜 네트워크나 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) 분석에 최적화되어 있다.
3. 구글의 **Pregel** 아키텍처를 스파크 상에 구현하여, 복잡한 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 반복적(Iterative)으로 수행할 때 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공한다.

---

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 노드(Node)와 링크(Link)로 표현하고, 이를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 효율적으로 연산하기 위한 스파크 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)이다.
- **배경**: 전통적인 표 형식(Table) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 방식으로는 수십억 개의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 가진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 연결성(Connectivity) 분석에 한계가 있어 이를 보완하기 위해 탄생했다.
- **주요 활용**: 페이스북/링크드인의 친구 추천, 구글의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)랭크(PageRank) 순위 결정, 사기 결제망 탐지, 단백질 구조 분석 등 초연결 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석에 필수적이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 프로퍼티 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(Property [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) 모델
```text
( Vertex A ) --[ Edge ]--> ( Vertex B )
     |                         |
  [Property]                [Property]
 (Name: John)              (Name: Bob)
 (Age: 30)                 (Age: 25)

[ GraphX Object ] = { VertexRDD, EdgeRDD }
```

#### 2. 핵심 연산 및 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- <strong>Triplet <a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a></strong>: 정점-간선-정점을 하나의 단위로 묶어 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 기반 연산을 수행한다.
- **PageRank**: 특정 노드의 중요도를 측정하여 순위를 매긴다 (검색 엔진의 핵심).
- **Connected Components**: 서로 연결된 정점들의 그룹(클러스터)을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한다.
- **Triangle Counting**: [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망 내의 삼각형 구조 개수를 세어 커뮤니티의 밀집도를 측정한다.
- <strong>Pregel <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong>: [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) 방식을 통해 정점들이 상태를 주고받으며 전역 해를 찾아가는 반복적 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 프레임워크를 제공한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전용 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB (Neo4j) | Spark GraphX |
| :--- | :--- | :--- |
| **목적** | 실시간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 및 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | 대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 배치 분석 및 학습 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 규모</strong> | 단일 노드 중심 (클러스터 확장성 제한) | TB/PB급 초대형 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 |
| **유연성** | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 전용 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(Cypher) 중심 | SQL 및 DataFrame과의 강력한 결합 |
| **속도** | 소수 정점 간의 탐색(Traversing) 우세 | 전체 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 대상 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(PageRank) 우세 |
| <strong>실무 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 엔드포인트 저장소로 활용 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 및 통찰 도출용으로 활용 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 통합(Unified)의 강점</strong>: GraphX의 최대 장점은 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 결과물(DataFrame)을 즉시 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 변환하고, 분석 결과를 다시 SQL로 조회할 수 있다는 점이다.
- <strong>셔플링과 <a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a></strong>: [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 연결성 때문에 노드 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동(Shuffle)이 매우 잦다. `PartitionStrategy`를 적절히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 네트워크 비용을 최소화하는 것이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝의 핵심이다.
- **GraphFrames로의 진화**: 최근에는 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 기반의 GraphX보다 DataFrame 기반의 `GraphFrames` [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 더 널리 쓰이며, Spark SQL과의 연동성이 더 뛰어나므로 프로젝트 시작 시 고려해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 개별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)뿐 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이의 '[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)'에서 숨겨진 가치를 찾아냄으로써 비즈니스 통찰의 차원을 한 단계 높인다.
- **결론**: GraphX는 대규모 [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) 분야의 강력한 표준이다. 향후 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))와 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)형 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))의 결합이 중요해짐에 따라, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 기반의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 처리하는 GraphX의 역할은 더욱 증대될 것이다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
1. **VertexRDD / EdgeRDD**: GraphX를 구성하는 두 가지 핵심 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입
2. **PageRank**: 노드 간의 링크 구조를 분석하여 중요도를 수치화하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
3. **Pregel**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 연산을 위한 '정점 중심(Vertex-centric)' 프로그래밍 모델

---

### 📈 관련 키워드 및 발전 흐름도

```text
[그래프 이론 (Graph Theory) — 정점/엣지 모델]
    |
    v
[스파크 GraphX (Apache Spark GraphX) — 분산 그래프 처리]
    |
    v
[Pregel API (Pregel Computation Model) — 정점 중심 반복]
    |
    v
[PageRank / 연결 요소 (PageRank / Connected Components) — 대표 알고리즘]
    |
    v
[그래프프레임즈 (GraphFrames) — 데이터프레임 기반 확장]
```

이 흐름은 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 이론을 Spark 위에 올려 GraphX와 Pregel로 반복 계산을 수행하고, PageRank와 GraphFrames로 분석 범위를 넓히는 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. "수많은 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 얽힌 학교 지도를 그리는 기술이에요. 누가 가장 인기가 많은지 찾아낼 수 있죠."
2. "점과 선으로 이루어진 복잡한 그물을 아주 커다란 컴퓨터 수백 대가 나눠서 분석하는 거예요."
3. "이게 바로 사람과 물건 사이의 연결 고리를 찾아내는 '[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)엑스'라는 대단한 방법이랍니다!"

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 63 / 262

<- **이전**: [스파크 엠엘립 (Spark MLlib) - 분산 머신러닝 라이브러리](/knowledge-base/studynote/16_bigdata/03_spark/062_spark_mllib/)
**다음**: [스파크 배포 모드 (Spark Deployment Modes)](/knowledge-base/studynote/16_bigdata/03_spark/064_spark_deployment_modes/) ->

---
