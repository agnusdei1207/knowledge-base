+++
title = "239. 그래프 데이터베이스 (Neo4j, AWS Neptune)"
date = 2026-05-05

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)([Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/))는 테이블(표) 형태를 버리고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>노드(Node, 점)</strong>와 그들 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 나타내는 <strong>엣지(Edge, 선)</strong>라는 1급 객체(First-class citizen)로 물리적 저장소에 직결시키는 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 아키텍처다.
> 2. **가치**: [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB(RDBMS)에서 수천만 건의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 4~5번씩 조인([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))하다가 서버가 터져버리는 '초연결 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색(예: 친구의 친구의 친구 찾기)' 연산을, 포인터 추적(Index-free [Adjacency](/knowledge-base/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/))을 통해 O(1) 수준의 광속으로 해결한다.
> 3. **판단 포인트**: SNS [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/), 금융 사기([FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/)) 돈세탁 경로 추적 등 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체'보다 <strong>'<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 간의 연결 고리(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">Relationship</a>)'가 비즈니스의 핵심 가치일 때</strong> 압도적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 내지만, 단순 통계나 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에는 최악의 선택이다.

---

## Ⅰ. 개요 및 필요성

페이스북(Facebook)이 처음 등장했을 때, 10억 명의 유저 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 "내 친구의 친구들 중에서, 넷플릭스를 좋아하는 사람을 추천해 줘"라는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 RDBMS(MySQL)로 돌리자 서버가 그대로 녹아내렸다.

[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB는 외래키(Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 이용해 테이블과 테이블의 집합을 수학적으로 곱하고 쪼개는([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 무거운 쇳덩어리다. [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)([Relationship](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))를 찾기 위해 거대한 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) B-Tree를 머리부터 발끝까지 뒤져야 했다. 아키텍트들은 깨달았다. "애초에 하드디스크에 저장할 때부터 A와 B가 친구라는 선(Edge)을 메모리 포인터로 다이렉트로 연결해 두면 안 될까?" 수학의 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 이론([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) Theory)을 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 스토리지 엔진에 때려 박은 것, 그것이 바로 Neo4j와 AWS Neptune으로 대변되는 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB의 탄생이다.

- **📢 섹션 요약 비유**: RDBMS의 조인([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산은 '전화번호부를 뒤져가며 친구 찾기'다. 내 친구 이름을 찾고, 그 친구 페이지로 가서 또 다른 친구 번호를 검색하는 걸 반복(수십 초 소요)한다. 반면 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 '사람들이 손에 손을 잡고 서 있는 광장'이다. 내 손을 잡고 있는 사람, 그 사람이 잡고 있는 사람을 그냥 물리적으로 1초 만에 쭉쭉 당겨오면 끝난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 프리 인접성 (Index-free [Adjacency](/knowledge-base/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/))
[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 미친 속도를 내는 가장 핵심적인 하드웨어적/논리적 아키텍처다.

```text
+--------------------------------------------------------+
|           그래프 DB의 스토리지 포인터 연결(Index-free Adjacency) |
+--------------------------------------------------------+
|   [ 노드(Node): 사람 ]              [ 엣지(Edge): 관계 ]         |
|                                                        |
|   (Node: "Alice") -------------> (Edge: "KNOWS")        |
|       |                                |               |
|   물리적 포인터(메모리 주소) 다이렉트 점프 |               |
|       v                                v               |
|   (Node: "Bob") <------------- (Edge: "LIKES")          |
|       |                                                |
|       v                                                |
|   (Node: "Sushi")                                      |
|                                                        |
| * 핵심 논리: Alice가 아는 사람을 찾기 위해 전체 DB 인덱스를      |
|   검색(O(log N))할 필요가 없다. Alice 노드 껍데기에 붙어있는     |
|   엣지 포인터를 따라 메모리 주소만 점프(O(1))하면 끝난다!        |
+--------------------------------------------------------+
```

RDBMS는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많아질수록(N이 커질수록) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 트리가 깊어져 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 속도가 기하급수적으로 느려진다. 하지만 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 프리 인접성을 갖춘 진정한 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB(Native [Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/))는 이웃 노드로 넘어가는 시간이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 총량(N)과 무관하게 항상 일정(O(1))하다. 100만 명 중 친구를 찾든, 10억 명 중 친구를 찾든 탐색 속도가 똑같다는 기적의 아키텍처다.

- **📢 섹션 요약 비유**: RDBMS는 아파트 호수를 찾기 위해 1층 관리실([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))의 명부를 계속 뒤적여야 하는 택배 기사다. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 이웃집 벽에 다음 집으로 통하는 비밀문(포인터)이 뚫려 있어서, 관리실에 내려갈 필요 없이 방 안에서 문만 열면 계속 옆집으로 넘어갈 수 있는 도둑(광속 탐색)이다.

---

## Ⅲ. 비교 및 연결

### [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB (RDBMS) vs [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB ([Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/))
이름에 '[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)(Relational)'가 들어간 RDBMS가 정작 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 처리에 가장 취약하다는 것은 IT 역사상 최고의 아이러니다.

| 비교 항목 | RDBMS (MySQL, [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB (Neo4j, Neptune) |
|:---|:---|:---|
| **저장 구조** | 엄격한 2차원 테이블(행과 열) | 노드(점), 엣지(선), 프로퍼티([속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 처리 방식</strong> | <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> 연산 (<a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 검색 필요, 느림)</strong> | **메모리 포인터 직결 (Index-free, 광속)** |
| **강점** | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 정합성(ACID), 집계(SUM/AVG) 연산 | 깊은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색 (Pathfinding), [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) |
| **질의어 (Query)** | SQL (선언적, 구조적) | **Cypher, Gremlin, SPARQL** (패턴 매칭 중심) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 병목</strong> | [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 뎁스(Depth)가 3~4번 넘어가면 사망 | 노드가 너무 많은 밀집 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(슈퍼노드)의 폭발 |

"테이블 A와 테이블 B가 엮여 있다"는 논리적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 RDBMS에서는 조인이라는 연산 비용(CPU/Memory)을 지불하며 런타임에 억지로 짜 맞춰야 한다. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 디스크에 저장(Write)되는 순간부터 엣지라는 물리적 선으로 묶여버리므로, 읽기(Read) 시점에는 연산 없이 선만 따라가면 되는 극단적인 구조적 우위를 점한다.

- **📢 섹션 요약 비유**: RDBMS는 '레고 블록 상자'다. 설명서([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 조건)를 보고 그때그때 블록을 찾아 조립해야 모양이 나온다. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 이미 접착제로 '완성된 레고 성'이다. 필요한 부분을 그냥 통째로 들어 올리면 조립할 시간(연산) 없이 바로 모양이 잡혀 올라온다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong>금융권 자금세탁방지(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/">FDS</a>) 및 사기 탐지 체계</strong>: 대포통장을 통한 자금 세탁은 A 계좌 ➔ B ➔ C ➔ D를 거쳐 쪼개졌다가 다시 E 계좌로 뭉치는 복잡한 네트워크 구조를 띤다. RDBMS로 이 5단계 돈의 흐름을 쫓으려면 자기 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) JOIN을 5번 걸어야 해서 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 며칠 동안 돌아간다([타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)). 아키텍트는 Neo4j를 도입해 계좌를 노드로, 이체 내역을 엣지로 박아버린다. `(A)-[:TRANSFER]->(B)-[:TRANSFER]->(C)`라는 직관적인 Cypher [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 한 줄로 0.1초 만에 사기 링(Fraud Ring)을 실시간으로 적발해 낸다.
2. <strong>이커머스 실시간 초개인화 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/">추천 시스템</a></strong>: "아이폰을 산 고객이, 친구들이 샀던 에어팟 케이스 중 평점 4점 이상인 제품을 보여줘." 아마존 클라우드의 AWS Neptune은 이 복잡한 다차원 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)(고객-구매-상품-친구)를 탐색하며 밀리초(ms) 단위로 추천 목록을 뽑아내 웹 화면에 렌더링한다. 일반 DB였다면 배치(Batch)로 새벽에나 돌렸을 연산을 실시간(Real-time) 비즈니스로 격상시킨다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>단순 집계(Aggregation) 업무에 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a> DB 오남용</strong>: "우리 회사도 최신 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 쓰자!"라며, 전체 사용자의 평균 나이를 구하거나 일일 총매출액(SUM)을 계산하는 장부에 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB를 쑤셔 넣는 만행. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 점과 선을 따라가는 데 최적화되어 있지, 테이블 전체의 값을 위에서 아래로 싹 쓸어 담아([Table Full Scan](/knowledge-base/studynote/05_database/07_exam_summary/428_table_full_scan/)) 더하는 연산에는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 없어 RDBMS보다 훨씬 멍청하고 느리다. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 중심일 때만 칼을 뽑아야 한다.

- **📢 섹션 요약 비유**: 매출 평균 구하는 데 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB를 쓰는 것은, 거미줄처럼 이어진 '지하철 노선도'를 펼쳐놓고 "이 지도에 적힌 역 이름 글자 수가 총 몇 개야?"라고 세고 있는 멍청한 짓이다. 그냥 엑셀 표(RDBMS)에 세로로 역 이름을 적어놓고 함수를 돌리는 게 천 배 빠르다.

---

## Ⅴ. 기대효과 및 결론

[그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)([Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/))는 인류가 현실 세계를 2차원 표(Table)에 억지로 구겨 넣으면서 상실했던 '[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)성(Connectedness)'의 본질을 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 아키텍처로 부활시킨 혁명이다.

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언스의 중심이 개별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))에서, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들이 어떻게 연결되어 상호작용하는지(Network)로 이동하면서 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB의 가치는 폭발하고 있다. 페이스북의 소셜 네트워크, 구글의 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)), 테슬라의 자율주행 도로망 모델링에 이르기까지, 복잡계(Complex System)를 실시간으로 해석하고 추론해야 하는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대의 가장 밑바닥 인프라에는 결코 끊어지지 않는 쇳덩어리 엣지(Edge)로 무장한 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 굳건히 자리 잡고 있다.

- **📢 섹션 요약 비유**: [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 '범죄 수사반의 사건 연결 보드판'이다. 용의자 사진(노드)을 벽에 붙여놓고 그들 사이의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 빨간 실(엣지)로 연결해 두면, 형사([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))는 두꺼운 수사 기록철(RDBMS)을 뒤질 필요 없이 빨간 실만 눈으로 따라가 배후의 보스를 1초 만에 찾아낼 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Cypher / Gremlin** | SQL이 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 언어라면, Cypher는 그림을 그리듯 `(User)-[:KNOWS]->(User)` 형태의 화살표로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 날리는 Neo4j의 전용 패턴 매칭 언어 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/">NoSQL</a> (<a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/274_nosql/">Not Only SQL</a>)</strong> | RDBMS의 테이블 구조적 한계를 깨부수고 등장한 비정형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 진영. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 [Document DB](/knowledge-base/studynote/16_bigdata/06_nosql/129_document_db/), [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value DB와 함께 이 진영의 가장 이질적인 천재다. |
| <strong>프로퍼티 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a> (Property <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/">Graph</a>)</strong> | 점(Node)과 선(Edge) 자체에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Property, 예: '친구 맺은 날짜')를 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value 형태로 주렁주렁 매달아 놓을 수 있는 현대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB의 표준 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) |

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS의 JOIN 연산 폭발로 인한 복잡한 관계 탐색 한계 (성능 병목)
    |
    v
소셜 네트워크(SNS)의 등장 및 초연결 데이터(Highly Connected Data) 폭증
    |
    v
수학적 그래프 이론(Graph Theory)의 스토리지 엔진 도입 (Neo4j 등장)
    |
    v
인덱스 프리 인접성(Index-free Adjacency) 하드웨어 로직 구현 (O(1) 탐색 속도 달성)
    |
    v
클라우드 융합(AWS Neptune) 및 사기 탐지(FDS), 지식 그래프(Knowledge Graph)의 핵심 AI 인프라로 안착
```

이 흐름도는 "[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델의 조인([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 한계 직면 -> [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 최우선([Relationship](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)-first) 철학의 설계 -> 포인터 기반 탐색 엔진 개발 -> 현대 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)/[추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)의 인프라 정착"으로 이어지는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 구조의 패러다임 전환을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 네모난 '표'에 가두지 않고, 도화지 위에 점(노드)을 찍고 선(엣지)으로 연결해서 그리는 마법의 그림판이에요.
2. 예전 DB(RDBMS)는 내 친구의 친구를 찾으려면 두꺼운 주소록 책을 5번이나 넘기며 고생해야 했어요.
3. 하지만 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 친구들끼리 이미 손(엣지)을 꽉 잡고 있어서, 내 손을 잡은 친구의 팔만 쭉쭉 따라가면 눈 깜짝할 새에 수백 명의 친구를 다 찾아낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 238 / 371

<- **이전**: [238. 와이드 컬럼 저장소 (Wide-Column Store) - Cassandra / HBase](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/238_wide_column_cassandra_hbase_lsm/)
**다음**: [240. 시계열 데이터베이스 (TSDB: InfluxDB, Prometheus)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/240_time_series_database_influxdb_prometheus/) ->

---
