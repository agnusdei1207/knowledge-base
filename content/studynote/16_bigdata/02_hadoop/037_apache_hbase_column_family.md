---
title: 'Apache HBase: 하둡 기반의 고성능 분산 NoSQL 데이터베이스'
date: '2026-03-04'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- 구글의 빅테이블(Bigtable)을 [[219_benchmarking_best_practice|벤치마킹]]하여 개발된, [[013_hdfs|HDFS]] 위에서 동작하는 열 지향(Column-Oriented) [[035_nosql|NoSQL]] [[002_database_definition|데이터베이스]]임.
- 수십억 개의 행과 수백만 개의 열을 가진 대규모 [[001_dikw_pyramid|데이터]]셋에 대해 밀리초(ms) 단위의 랜덤 읽기/[[289_cqrs_db|쓰기]](Random R/W) [[282_performance_tactics|성능]]을 보장함.
- 주키퍼([[798_distributed_lock_zookeeper_consensus|ZooKeeper]])를 통한 [[136_variance|분산]] 코디네이션과 리전 서버(Region Server) 기반의 수평 확장을 통해 높은 [[452_availability|가용성]]을 확보함.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
[[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 HDFS는 한 번 저장하면 수정이 어려운 불변([[298_immutable|Immutable]]) [[501_file_definition_logical_record|파일]] 시스템이며, [[001_dikw_pyramid|데이터]] 조회도 전체 스캔(Full Scan) 방식이다. 정보통신기술사 관점에서 Apache HBase는 이러한 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 한계를 극복하고, HDFS를 '저장소'로 활용하면서도 실시간으로 특정 [[001_dikw_pyramid|데이터]]를 콕 집어 조회(Point Lookup)하거나 수정할 수 있는 능력을 부여한 핵심 DB이다. 주로 페이스북의 [[389_mesh_topology|메시]]징 [[090_service_kubernetes_network_load_balancing|서비스]], 주식 거래 로깅, 시계열 [[001_dikw_pyramid|데이터]] 저장 등 '[[289_cqrs_db|쓰기]] 부하가 크고 실시간 조회가 필요한' 영역에서 활용된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
HBase는 [[001_dikw_pyramid|데이터]]를 행 키(Row [[067_db_key_uniqueness_minimality|Key]]) 순으로 정렬하여 여러 대의 리전 서버에 [[136_variance|분산]] 저장한다.

```text
[ Apache HBase Architecture ]

     [ Client / App ] <--- ( ZooKeeper / Meta Table Lookup )
            |
    +-------V-------+       +-----------------------+
    |   HMaster     | <---> |   ZooKeeper Quorum    |
    | (Coordination)|       | (Status / Leader)     |
    +-------+-------+       +-----------------------+
            |
    +-------V-------+       +-------V-------+
    | Region Server |       | Region Server | (Worker)
    | [MemStore]    |       | [MemStore]    | (LSM Tree)
    | [HFile/WAL]   |       | [HFile/WAL]   |
    +-------+-------+       +-------+-------+
            |               |
    [       HDFS Distributed Storage Layers       ]

[ Bilingual Storage Logic ]
- Row Key (행 키): 데이터의 유일한 식별자. 정렬되어 인덱스 역할.
- Column Family (컬럼 패밀리): 연관된 컬럼들의 논리적 그룹. 물리적 저장 단위.
- MemStore (멤스토어): 쓰기 시 먼저 저장되는 인메모리 버퍼. (LSM-Tree 구조)
- HFile (에이치파일): MemStore가 꽉 차면 HDFS로 플러시되는 최종 파일.
```

HBase는 [[377_lsm_tree_storage_engine|LSM-Tree]] 구조를 채택하여, [[289_cqrs_db|쓰기]] 요청을 일단 메모리(MemStore)에 순차적으로 기록한 뒤 나중에 덩어리로 디스크(HFile)에 내려보낸다. 덕분에 디스크 랜덤 I/O를 피하고 압도적인 [[289_cqrs_db|쓰기]] 속도를 낸다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[083_relationship_in_er_model|관계]]형 DB (RDBMS) | Apache [[543_hbase|HBase]] ([[035_nosql|NoSQL]]) |
| :--- | :--- | :--- |
| **확장 방식** | 수직 확장 ([[621_scale_up_system_bus|Scale-up]]) | **수평 확장 ([[202_scale_out_distributed_horizontal_expansion|Scale-out]] / [[280_sharding|샤딩]])** |
| **저장 방식** | 로우 기반 (Row-oriented) | **컬럼 패밀리 기반 (Columnar Family)** |
| **[[005_schema|스키마]] 유연성** | 고정 [[005_schema|스키마]] (엄격함) | **가변 [[005_schema|스키마]] (Sparse [[001_dikw_pyramid|Data]] 지원)** |
| **[[014_data_model_components|데이터 모델]]** | 테이블 조인([[521_join|Join]]) 중심 | **비정규화 (Denormalized) 중심** |
| **주요 용도** | 결제, 회계 등 [[191_transaction_concept_states|트랜잭션]] | **대용량 [[568_logs_distributed_logging_elk_fluentd|로그]], 타임라인, 추천 엔진** |
| **기술사적 판단** | "강력한 [[194_consistency_database_integrity|일관성]](ACID) 우선" | **"대용량 확장성 및 [[452_availability|가용성]] 우선"** |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **(행 키 설계 - Row [[067_db_key_uniqueness_minimality|Key]] Design)** 특정 날짜에 [[001_dikw_pyramid|데이터]]가 몰리는 'Hotspotting'을 방지하기 위해, Row [[067_db_key_uniqueness_minimality|Key]] 앞에 해시(Hash)나 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])를 붙여 트래픽을 [[136_variance|분산]] 노드에 골고루 뿌리는 설계가 필수적이다.
- **(컬럼 패밀리 수 제한)** 컬럼 패밀리 수가 너무 많으면 [[013_hdfs|HDFS]] [[501_file_definition_logical_record|파일]] 수가 급격히 늘어나 [[014_namenode|네임노드]]에 부하를 주므로, 가급적 1~2개 이내로 유지해야 한다.
- **([[378_lsm_compaction_tombstone|콤팩션]] 튜닝 - [[347_compaction|Compaction]])** 작은 HFile들을 병합하는 [[347_compaction|Compaction]] 과정에서 디스크 I/O가 폭증할 수 있으므로, [[090_service_kubernetes_network_load_balancing|서비스]] 사용량이 적은 야간 시간대에 Major Compaction이 일어나도록 [[208_schedule_history_transaction_execution_order|스케줄]]링해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
HBase는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 생태계에서 '실시간 읽기/[[289_cqrs_db|쓰기]]'라는 퍼즐 조각을 맞춘 기술이다. 최근에는 [[299_data_lake|카산드라]]([[541_cassandra|Cassandra]])나 클라우드 기반 [[035_nosql|NoSQL]]([[545_dynamodb|DynamoDB]] 등)에 시장 점유율을 내주고 있지만, [[211_hadoop_ecosystem_mapreduce|하둡 에코시스템]]과의 강력한 결합성([[544_hive|Hive]] 연동 등) 덕분에 여전히 거대 엔터프라이즈 환경의 중추를 담당한다. 기술사는 비즈니스 [[001_dikw_pyramid|데이터]]의 '[[289_cqrs_db|쓰기]]/읽기 패턴'을 면밀히 분석하여 HBase의 열 기반 저장 구조가 주는 이점을 극대화해야 한다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[013_hdfs|HDFS]]**: HBase의 [[001_dikw_pyramid|데이터]]가 물리적으로 저장되는 장부
- **[[798_distributed_lock_zookeeper_consensus|ZooKeeper]]**: 클러스터 노드들의 출석부
- **[[377_lsm_tree_storage_engine|LSM-Tree]]**: HBase의 고속 [[289_cqrs_db|쓰기]] 수리 모델
- **[[543_hbase|HBase]] [[044_shell|Shell]] / Thrift**: HBase에 접속하는 인터페이스


### 📈 관련 키워드 및 발전 흐름도

```text
[RDBMS (관계형 DB) — 행 기반 스키마, ACID 트랜잭션, 수직 확장 한계]
    │
    ▼
[HBase — HDFS 위의 컬럼 패밀리 기반 분산 NoSQL, 수억 행 수평 확장]
    │
    ▼
[컬럼 패밀리 (Column Family) — 연관 컬럼 묶음을 동일 HFile에 배치, I/O 최적화]
    │
    ▼
[LSM-Tree (Log-Structured Merge Tree) — MemStore→HFile 계단식 병합으로 고속 쓰기]
    │
    ▼
[Apache Phoenix — HBase 위에 SQL 레이어를 추가, 기업 데이터 웨어하우스 확장]
```

이 흐름은 행 기반 RDBMS의 수직 확장 한계를 극복하기 위해 [[543_hbase|HBase]] 컬럼 패밀리 구조가 등장하고, [[377_lsm_tree_storage_engine|LSM-Tree]] 기반 고속 [[289_cqrs_db|쓰기]]를 확보한 뒤, Phoenix SQL 레이어로 기업 분석 환경에 통합되는 컬럼형 [[136_variance|분산]] NoSQL의 발전 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 아주아주 큰 도서관에 매일 수만 권의 책이 새로 들어온다고 해보자.
- HBase는 책을 하나하나 예쁘게 꽂는 대신, 일단 상자에 담아두고(메모리) 나중에 한꺼번에 서가에 정리해(디스크).
- 덕분에 책을 아주 빨리 받을 수 있고, 나중에 "그 책 어디 있어?"라고 물어봐도 금방 찾아줄 수 있단다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 37 / 262

← **이전**: [[036_apache_hive_sql_interface|Apache Hive: 하둡 기반의 SQL 온 하둡(SQL-on-Hadoop) 데이터 웨어하우스]]
**다음**: [[038_apache_pig|16. 아파치 피그 (Apache Pig) - 하둡 데이터 흐름 스크립팅]] →

---
