+++
title = "035. NoSQL 데이터베이스"
date = 2026-03-03

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

> **핵심 인사이트**
> 1. NoSQL ([Not Only SQL](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/274_nosql/))은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 고정 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)와 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 일부 포기하는 대신, 수평 확장([Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))·고가용성·대용량 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리에 최적화된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 패러다임이다.
> 2. NoSQL은 단일 기술이 아니라 문서([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/)), 키-값(Key-Value), 열(Column-Family), [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) 등 4가지 주요 모델로 구성되며, 각 모델은 특정 워크로드에 최적화된다.
> 3. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)-Availability-Partition Tolerance)에 따라 NoSQL은 대부분 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용)를 선택하며, [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))을 제공한다.

---

## I. RDBMS vs NoSQL 비교

```
RDBMS                    NoSQL
+-- 고정 스키마           +-- 유연한 스키마
+-- ACID 트랜잭션         +-- BASE (결과적 일관성)
+-- 수직 확장 (Scale-Up) +-- 수평 확장 (Scale-Out)
+-- SQL 표준             +-- 각 DB별 고유 API
+-- 관계 모델            +-- 문서/키값/그래프 등
```

| 항목          | RDBMS          | NoSQL             |
|-------------|----------------|-------------------|
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)        | 고정            | 유연 (Schema-less)|
| 확장         | 수직            | 수평              |
| [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)      | ACID            | BASE / [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)|
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어     | SQL             | DB별 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)          |
| 조인         | 복잡한 조인 가능 | 조인 어려움 / 비정규화|
| 적합 워크로드 | 정형 + [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)     | 대용량, 비정형, 빠른 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)|

> 📢 **섹션 요약 비유**: RDBMS는 엄격한 서식이 있는 서류함, NoSQL은 각 서류를 자유 형식으로 담는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 폴더 — 유연하지만 색인 방법이 다르다.

---

## II. NoSQL 4대 모델

```
1. 키-값 (Key-Value)
   key: "user:1001"
   value: { name: "홍길동", age: 30 }
   예시: Redis, DynamoDB, Memcached
   장점: 단순, 초고속 읽기/쓰기

2. 문서 (Document)
   {
     "_id": "order_001",
     "items": [{"sku": "A1", "qty": 2}],
     "total": 5000
   }
   예시: MongoDB, Firestore, CouchDB
   장점: JSON 유사 구조, 계층적 데이터

3. 열 (Column-Family)
   RowKey: "user#001"
   CF:info -> { name, email, signup_date }
   CF:activity -> { last_login, page_views }
   예시: Cassandra, HBase, BigTable
   장점: 시계열, 대용량 쓰기

4. 그래프 (Graph)
   (홍길동)-[:FOLLOWS]->(김철수)
   예시: Neo4j, Amazon Neptune
   장점: 관계 탐색 (SNS, 추천, 사기 탐지)
```

> 📢 **섹션 요약 비유**: 4가지 선반 구조 — 키-값은 열쇠고리(빠른 접근), 문서는 서랍(계층적), 열은 스프레드시트(시계열), [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 지도([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색).

---

## III. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리와 NoSQL 선택

```
CAP 정리:
분산 시스템에서 Consistency, Availability,
Partition Tolerance 중 최대 2개만 보장 가능

        C (일관성)
       / \
      /   \
CA    /     \ CP
    /         \
   /     AP    \
  A (가용성) -- P (분단 허용)

NoSQL 대부분: AP 선택 (가용성 + 분단 허용)
  -> 결과적 일관성 (Eventually Consistent)
```

| DB        | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 선택 | 특성                     |
|----------|---------|--------------------------|
| [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/)   | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)/[AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)   | 설정에 따라 선택 가능     |
| [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)      | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/), 고가용성   |
| [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)     | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)      | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)    |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)     | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)      | 메모리, 단일 노드 강함    |
| [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/)  | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)      | 글로벌 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)|

> 📢 **섹션 요약 비유**: CAP은 항공사 딜레마 — 정시 출발([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))·취소 없음([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))·네트워크 장애 시 비행(분단 허용) 중 2개만 선택.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). BASE vs ACID

```
ACID (RDBMS):
  Atomicity  - 트랜잭션 원자성 (All or Nothing)
  Consistency - 무결성 제약 항상 유지
  Isolation  - 트랜잭션 간 격리
  Durability - 커밋된 데이터 영구 보존

BASE (NoSQL):
  Basically Available  - 기본 가용성 보장
  Soft State           - 상태가 변할 수 있음
  Eventually Consistent - 결과적으로 일관성 수렴
```

> 📢 **섹션 요약 비유**: ACID는 은행 통장(정확한 잔액 보장), BASE는 소셜 미디어 좋아요 수(잠깐 다를 수 있지만 결국 같아진다).

---

## V. 실무 시나리오 — 이커머스 아키텍처

| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형    | 저장소         | 이유                        |
|-------------|--------------|------------------------------|
| 상품 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)  | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/)      | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 구조, 유연한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)      |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)/장바구니  | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)        | 빠른 키-값, [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 지원         |
| 주문 이력     | MySQL/PostgreSQL | ACID, 재무 정합성 필요      |
| [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)   | Neo4j        | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색 (구매 패턴)  |
| 클릭스트림    | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)    | 시계열 대용량 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)           |

> 📢 **섹션 요약 비유**: 하나의 창고보다 여러 종류의 선반 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성에 맞는 저장소를 골라야 성능과 비용이 최적화된다.

---

## 📌 관련 개념 맵

```
NoSQL
+-- 4대 모델
|   +-- 키-값: Redis, DynamoDB
|   +-- 문서: MongoDB, Firestore
|   +-- 열: Cassandra, HBase
|   +-- 그래프: Neo4j, Neptune
+-- 이론
|   +-- CAP 정리 (CP/AP/CA)
|   +-- BASE (vs ACID)
|   +-- 수평 확장 (Sharding)
+-- 적용 패턴
    +-- 세션 저장 (Redis)
    +-- 이벤트 소싱 (Cassandra)
    +-- 콘텐츠 관리 (MongoDB)
    +-- 사기 탐지 (Neo4j)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[RDBMS 독주 시대 (1970s~2000s)]
관계형 모델, SQL 표준, ACID
      |
      v
[웹 2.0 스케일 문제 (2003~2008)]
Google Bigtable (2006), Amazon Dynamo (2007)
대용량 수평 확장 필요성
      |
      v
[NoSQL 붐 (2009~2012)]
MongoDB, Cassandra, Redis 등장
"NoSQL" 용어 확산
      |
      v
[NewSQL 등장 (2012~)]
Google Spanner, CockroachDB
ACID + 수평 확장 동시 달성
      |
      v
[현재: 다중 모델 DB]
한 DB가 여러 모델 지원
CosmosDB, ArangoDB, YugabyteDB
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. NoSQL은 엑셀 표처럼 딱딱하게 정해진 칸이 아니라, 자유롭게 내용을 담을 수 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 폴더예요.
2. 친구 목록처럼 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 저장하거나, 지도처럼 위치 정보를 담기에 훨씬 유리해요.
3. 대신 "이 금액이 정확히 맞다"는 보장이 약해서, 은행 같은 데는 여전히 SQL을 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 35 / 258

<- **이전**: [ELT (Extract, Load, Transform) 현대 데이터 스택](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/)
**다음**: [036. 키-값 저장소 (Key-Value Store)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/) ->

---
