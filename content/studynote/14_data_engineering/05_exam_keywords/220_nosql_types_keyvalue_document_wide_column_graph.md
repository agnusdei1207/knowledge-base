+++
title = "220. NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL은 "[Not Only SQL](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/274_nosql/)"로, RDBMS의 엄격한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)와 ACID 제약을 완화하고 **수평 확장([Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))**을 통해 빅데이터 규모의 다양한 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)을 처리하기 위해 등장했다.
> 2. **가치**: 키-값([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value)·도큐먼트([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/))·와이드 컬럼(Wide-Column)·[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) 4가지 유형은 각각 캐시·컨텐츠·시계열·[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 분석 등 특정 사용 사례에 최적화되어 있다.
> 3. **판단 포인트**: [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) DB 선택은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조(정형/비정형), 접근 패턴(단순 조회/복잡 조인/[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색), [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 요건(강한/결과적), 규모(단일 서버/수백 노드)를 종합 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

### [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 등장 배경

2000년대 후반 Google(Bigtable, 2006), Amazon(Dynamo, 2007), Facebook([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), 2008)이 기존 RDBMS로는 처리 불가능한 규모의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 위해 자체 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) DB를 개발·공개하면서 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 생태계가 폭발적으로 성장했다.

**RDBMS의 한계:**
- 수평 확장([Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 어려움 → 수직 확장([Scale-Up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 비용 폭증
- 엄격한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) → [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리 불가
- ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 오버헤드 → [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 처리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하
- [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 연산 비용 → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 네트워크 병목

### [NoSQL BASE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/218_nosql_base_eventual_consistency_sharding/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)

| RDBMS ACID | [NoSQL BASE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/218_nosql_base_eventual_consistency_sharding/) | 설명 |
|:---|:---|:---|
| [Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) | Basically Available | 일부 노드 장애에도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지속 |
| [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | Soft-state | 일시적 불일치 허용 |
| [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) | Eventually Consistent | 시간이 지나면 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 달성 |
| [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) | - | 내구성은 유지 |

📢 **섹션 요약 비유**: RDBMS는 **엄격한 은행 창구**고, NoSQL은 **편의점 계산대**다. 편의점은 영수증이 가끔 느리게 나와도 되지만, 은행은 모든 거래가 정확해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 4대 유형 비교

```
NoSQL 유형별 데이터 모델
┌──────────────┬──────────────────────────────────────────┐
│ 키-값        │  "user:1234" → { name, age, email }     │
│ (Key-Value)  │  단순 해시맵, 빠른 단일 조회             │
├──────────────┼──────────────────────────────────────────┤
│ 도큐먼트     │  { _id: 1, name: "홍길동",              │
│ (Document)   │    orders: [{...}, {...}] }             │
│              │  JSON/BSON 중첩 구조, 유연한 스키마      │
├──────────────┼──────────────────────────────────────────┤
│ 와이드 컬럼  │  Row Key │ CF:col1 │ CF:col2 │ ...      │
│ (Wide-Column)│  희소 행렬, 컬럼 패밀리 단위 저장        │
├──────────────┼──────────────────────────────────────────┤
│ 그래프       │  (노드A) -[관계:FRIENDS]-> (노드B)       │
│ (Graph)      │  노드·엣지·속성, 관계 탐색 최적화        │
└──────────────┴──────────────────────────────────────────┘
```

### 세부 비교 표

| 항목 | 키-값 | 도큐먼트 | 와이드 컬럼 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
|:---|:---|:---|:---|:---|
| **대표 제품** | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), Couchbase | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) | Neo4j, Amazon Neptune |
| **[데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)** | 단순 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)→Value | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON 도큐먼트 | 컬럼 패밀리 | 노드·엣지 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 방식** | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 기반 단순 조회 | 필드 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | Row [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), 범위 스캔 | Cypher, Gremlin |
| **확장성** | 매우 높음 | 높음 | 매우 높음 | 수평 확장 어려움 |
| **[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | 결과적/조정 가능 | 도큐먼트 단위 ACID | 결과적/조정 가능 | ACID (Neo4j) |
| **주 사용 사례** | 캐시, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 리더보드 | 컨텐츠 관리, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | 시계열, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | SNS [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 추천, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) |
| **[JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 지원** | 없음 | 제한적 ($lookup) | 없음 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 순회 |

📢 **섹션 요약 비유**: 키-값은 **사물함(번호→물건)**, 도큐먼트는 **서류 봉투(내용물 자유)**, 와이드 컬럼은 **엑셀 시트(행·열 희소)**, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 **[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 지도(사람 간 연결)**다.

---

## Ⅲ. 비교 및 연결

### 유형별 심화 특성

**키-값 ([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value):**
- [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/): 인메모리 + RDB/AOF [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/), 자료 구조(Hash·List·Sorted Set) 지원
- [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/): [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), 자동 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)(Auto [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/)), DAX 캐시 계층

**도큐먼트 ([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/)):**
- [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/): BSON 저장, Aggregation [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/), Atlas Search(전문 검색)
- [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성 → 마이크로서비스의 독립 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화에 적합

**와이드 컬럼 (Wide-Column):**
- [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/): 일관적 해시([Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)) + 가십 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)(Gossip [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화(LSM Tree)
- [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/): [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/[HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위에 동작, 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) → [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 분석 연계

**[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)):**
- Neo4j: Property [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) 모델, Cypher [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어, 임베디드/클러스터 모드
- 사용 사례: 부정 탐지(Fraud [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)), 추천 엔진, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/), SNS

### [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) vs [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/)

| 항목 | [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) | [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/) |
|:---|:---|:---|
| **목표** | 확장성·유연성 | 확장성 + ACID 보장 |
| **대표 제품** | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | Spanner, [CockroachDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/292_etl_process/), [TiDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/) |
| **SQL 지원** | 제한적 | 완전 SQL |
| **[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |

📢 **섹션 요약 비유**: [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) vs NewSQL은 **리어카(가볍고 빠름) vs 소형 트럭(무겁지만 규칙 준수)**의 차이다. NewSQL은 RDBMS의 규칙을 지키면서 트럭을 여러 대 이어 붙인 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 사용 사례별 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 선택 매트릭스

| 사용 사례 | 권장 유형 | 이유 |
|:---|:---|:---|
| 웹 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 캐시 | 키-값 ([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)) | 빠른 만료([TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)) 관리, 인메모리 |
| 사용자 프로필 | 도큐먼트 ([MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/)) | 유연한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/), 중첩 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 시계열 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 와이드 컬럼 ([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중, 시간 범위 스캔 |
| SNS 친구 추천 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Neo4j) | 다단계 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색 |
| 쇼핑몰 상품 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | 도큐먼트 ([MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/)) | 다양한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/), 전문 검색 |
| 실시간 순위표 | 키-값 ([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sorted Set) | O(log n) 순위 갱신 |

### 기술사 판단 포인트

1. **복합 사용 패턴**: 하나의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 여러 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 혼용 ([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))
2. **RDBMS와 공존**: RDBMS는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 핵심, NoSQL은 캐시·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·분석 보조
3. **운영 복잡성**: [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 도입 시 관리 오버헤드 증가 → 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(AWS [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), Atlas) 활용

📢 **섹션 요약 비유**: [폴리글랏 퍼시스턴스](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))는 **요리마다 다른 조리 기구**를 쓰는 것이다. 밥은 솥, 고기는 그릴, 국은 냄비. 모두 밥솥으로만 하려면 불편하다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 도입으로 DB 부하 70~90% 감소 |
| [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 증가 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 클러스터 확장으로 초당 수십만 건 처리 |
| 개발 민첩성 | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 없는 도큐먼트 DB로 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 마이그레이션 없이 기능 추가 |
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 분석 속도 | 6단계 친구 찾기: RDBMS 수십 초 → Neo4j 수십 밀리초 |

### 결론

NoSQL은 RDBMS를 대체하는 것이 아니라 **상호 보완적으로 공존**한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조, 접근 패턴, 규모, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 요건을 기반으로 적절한 저장소를 선택하는 **[폴리글랏 퍼시스턴스](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))** [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍처의 표준이 되었다.

📢 **섹션 요약 비유**: 최적의 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 선택은 **운동 종목에 맞는 신발 선택**이다. 등산화, 러닝화, 수영장 슬리퍼 모두 좋은 신발이지만, 상황에 따라 맞는 것이 다르다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 키-값 ([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/)) | 단순 해시맵, 캐시·[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 최적 |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 도큐먼트 ([MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), Couchbase) | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON, 유연한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 와이드 컬럼 ([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)) | 시계열·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화 |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Neo4j, Neptune) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색, SNS·추천 |
| 이론 기반 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) vs [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 선택 근거 |
| [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | BASE | NoSQL의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 완화 모델 |
| 진화 | [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/) ([CockroachDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/292_etl_process/), [TiDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/)) | 확장성 + ACID 결합 |
| 설계 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [폴리글랏 퍼시스턴스](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/) | 목적별 다수 DB 혼용 |

### 👶 어린이를 위한 3줄 비유 설명

1. 키-값은 **사물함**이야. 번호(키)를 알면 바로 내 물건(값)을 꺼낼 수 있어. 엄청 빠르지!

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS (관계형, 정형 데이터)
    │
    ▼
NoSQL 4대 유형
    ├─► Key-Value: Redis · DynamoDB (캐시 · 세션)
    ├─► Document: MongoDB · CouchDB (유연 스키마)
    ├─► Wide-Column: Cassandra · HBase (대규모 쓰기)
    └─► Graph: Neo4j · Amazon Neptune (관계 탐색)
    │
    ▼
Multi-Model DB: 여러 데이터 모델 통합 지원
```
2. 도큐먼트는 **서류 봉투**야. 봉투 안에 사진도 넣고 편지도 넣고 뭐든 넣을 수 있어. 내용이 다 달라도 괜찮아.
3. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 **친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도**야. 나→내 친구→내 친구의 친구를 따라가면서 "우리 학교에서 몇 다리 건너 연결됐지?" 같은 걸 빠르게 찾을 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 220 / 258

← **이전**: [219. CAP 정리 (CAP Theorem)와 PACELC 정리 분산 트레이드오프](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)
**다음**: [221. LSM 트리 (Log-Structured Merge-Tree) 멤테이블 순차 플러시 콤팩션](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/) →

---
