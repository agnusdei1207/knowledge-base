---
title: "NoSQL Architecture"
tags:
  - "bigdata"
---

## 핵심 인사이트 (3줄 요약)
1. <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리 기반의 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 아키텍처</strong>: [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), 분할 내성([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 중 시스템 목적에 맞춰 두 가지를 선택하는 트레이드오프 설계.
2. <strong><a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>리스(Schemaless)와 유연성</strong>: 고정된 테이블 구조를 탈피하여 비정형/[반정형 데이터](/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)의 빠른 수용 및 [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 개발을 지원함.
3. <strong><a href="/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">스케일 아웃</a>(<a href="/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">Scale-out</a>) 최적화</strong>: 수평적 확장이 용이한 아키텍처([Sharding](/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/)/[Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))를 통해 대용량 트래픽과 페타바이트급 빅데이터 처리에 특화됨.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의**: '[Not Only SQL](/studynote/05_database/05_distributed_nosql_newsql/274_nosql/)'의 약자로, 전통적인 RDBMS의 한계([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 경직성, 수직적 확장성의 한계)를 극복하기 위해 등장한 비관계형 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 총칭.
- **등장 배경**: Web 2.0 시대의 도래로 폭증하는 소셜 미디어, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등 대용량 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 실시간으로 처리할 시스템 요구.
- **적용 분야**: 실시간 추천 엔진, 사용자 프로필 저장소, 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)), 대용량 [세션 관리](/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/) 등.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)([Sharding](/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))를 통해 고가용성과 확장성을 달성합니다.

```text
+-------------------------------------------------------------+
|                NoSQL 분산 클러스터 아키텍처 (NoSQL Cluster Arch)   |
+-------------------------------------------------------------+
|                                                             |
|                    [Client Applications]                    |
|                              |                              |
|                 +-------------------------+                 |
|                 | Load Balancer / Router  |                 |
|                 +-------------------------+                 |
|                       /      |      \                       |
|          +-----------+  +-----------+  +-----------+        |
|          | Node 1    |  | Node 2    |  | Node 3    |        |
|          | (Shard A) |  | (Shard B) |  | (Shard C) |        |
|          | --------- |  | --------- |  | --------- |        |
|          | Replica C'|  | Replica A'|  | Replica B'|        |
|          +-----------+  +-----------+  +-----------+        |
|                |              |              |              |
|                +--------------+--------------+              |
|                 (Gossip Protocol / Ring Topology)           |
|                                                             |
| * 핵심 메커니즘:                                             |
|  - Sharding: Consistent Hashing을 통한 데이터 수평 분할         |
|  - Replication: 데이터 복제본 유지로 고가용성 보장 (Masterless)    |
|  - Eventual Consistency: 결과적 일관성 동기화                  |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 핵심 특징 | 대표 솔루션 | 주요 Use Case |
|---|---|---|---|
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/036_key_value/">Key-Value Store</a></strong> | [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) Read/Write, 단순 구조 | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/), Memcached | [세션 관리](/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/), 인메모리 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), 장바구니 |
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/037_document/">Document Store</a></strong> | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON 형태 저장, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성 | [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/), Couchbase | CMS, 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/), 실시간 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| **Column-Family** | 대량 [데이터 압축](/studynote/08_algorithm_stats/09_info_theory/159_compression/), 넓은 열(Wide-column) | [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [HBase](/studynote/05_database/04_transactions_concurrency/543_hbase/) | 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)), 넷플릭스 유저 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/039_graph_db/">Graph DB</a></strong> | 노드와 엣지 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)로 복잡한 네트워크 모델링 | Neo4j, Amazon Neptune | [소셜 네트워크 분석](/studynote/12_it_management/03_ea_isp/107_classification/), 사기 탐지, 추천 망 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/">Polyglot Persistence</a> 아키텍처</strong>: 단일 DB에 모든 것을 담지 않고, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(RDBMS), [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)), [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)([MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/)) 등 목적에 맞게 DB를 조합하여 구성.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>링 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Normalization](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))와 반대로, NoSQL은 '애플리케이션의 읽기 패턴(Query Pattern)'에 맞춰 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비정규화([Denormalization](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/))하여 저장해야 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 극대화됨.
- <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 수준 튜닝</strong>: 비즈니스 중요도에 따라 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(Strong [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))과 [결과적 일관성](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 사이의 Read/Write Quorum 파라미터 튜닝 필수.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- <strong>무중단 <a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증가와 트래픽 폭주 시 노드 추가만으로 선형적인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상을 얻어 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에 완벽 부합.
- **Time-to-Market 단축**: [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경을 위한 마이그레이션 작업 없이 유연하게 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 변경하며 빠른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 런칭 가능.
- **표준화 트렌드**: 최근에는 NoSQL에서도 ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 일부를 지원하고, RDBMS가 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 타입을 수용하는 등 뉴-스퀄([NewSQL](/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/))로의 수렴 현상 가속화.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템(Distributed Systems), [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 시스템([DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/))
- **하위 개념**: [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리, BASE 원칙, [Sharding](/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/), [Consistent Hashing](/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)
- **연관 기술**: RDBMS, [NewSQL](/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/), 클라우드 스토리지, 빅데이터 플랫폼([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/), Spark)

### 📈 관련 키워드 및 발전 흐름도

```text
[Key-Value]
    |
    v
[Document]
    |
    v
[Column-Family]
    |
    v
[Graph]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>전통적 DB(RDBMS)가 칸막이가 쳐진 꼼꼼한 서류철이라면, NoSQL은 물건을 모양 상관없이 쑥쑥 넣을 수 있는 마법의 상자</strong>예요.
2. 손님이 너무 많이 올 때, <strong>계산대를 하나만 크고 좋게 만드는 게 아니라(<a href="/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/">Scale-up</a>), 작은 계산대 여러 개를 넓게 쫙 깔아놓는 방식(<a href="/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">Scale-out</a>)</strong>이랍니다.
3. 복잡한 표를 그리지 않아도 <strong>사진, 메모장, 동영상 정보를 그냥 하나의 상자(<a href="/studynote/14_data_engineering/01_infrastructure/037_document/">Document</a>)에 담아 보관</strong>할 수 있어서 아주 빠르고 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 262

<- **이전**: [26. 인과 추론 (Causal Inference) — 상관관계를 넘어 인과관계 규명](/studynote/16_bigdata/05_analysis/122_causal_inference/)
**다음**: [BASE 원칙 (Basically Available, Soft State, Eventual Consistency)](/studynote/16_bigdata/06_nosql/124_base_principles_nosql/) ->

---
