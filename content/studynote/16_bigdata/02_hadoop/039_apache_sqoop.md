---
title: 17. 아파치 스쿱 (Apache Sqoop) - RDBMS ↔ 하둡 데이터 전송
date: '2026-03-04'
tags:
- hadoop
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- 아파치 스쿱(Apache Sqoop)은 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]](RDBMS)와 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[013_hdfs|HDFS]], [[544_hive|Hive]], [[543_hbase|HBase]]) 간에 대용량 [[001_dikw_pyramid|데이터]]를 효율적으로 주고받는 '[[001_dikw_pyramid|데이터]] 이관 전용' 도구임.
- SQL-to-Hadoop의 약자로, 커넥터를 통해 [[430_index_fast_full_scan|병렬]]로 [[001_dikw_pyramid|데이터]]를 추출(Import)하거나 적재(Export)하여 [[208_data_lake_schema_on_read|데이터 레이크]]의 [[459_quic_fec_forward_error_correction|초기]] [[001_dikw_pyramid|데이터]]를 채우는 가교 역할을 수행함.
- [[018_mapreduce|맵리듀스]]([[018_mapreduce|MapReduce]])를 기반으로 동작하여 [[136_variance|분산]] [[430_index_fast_full_scan|병렬]] 전송이 가능하며, 증분 업데이트(Incremental Update) 기능을 통해 변경된 [[001_dikw_pyramid|데이터]]만 선별적으로 가져올 수 있음.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
기업의 핵심 [[001_dikw_pyramid|데이터]](고객 정보, 거래 이력 등)는 대부분 오라클, MySQL 같은 RDBMS에 들어있다. 빅데이터 분석을 위해 이 [[001_dikw_pyramid|데이터]]를 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]으로 옮겨야 하는데, 단순한 덤프(Dump) [[501_file_definition_logical_record|파일]] 전송은 시간이 너무 오래 걸리고 관리도 어렵다. 스쿱은 RDBMS의 테이블 구조를 그대로 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]으로 가져오거나 반대로 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]에서 분석된 결과를 운영 DB로 다시 밀어 넣어주는 표준화된 자동화 도구로 개발되었다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스쿱은 사용자의 명령을 [[018_mapreduce|맵리듀스]] 잡으로 변환하여 RDBMS와 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 사이의 [[430_index_fast_full_scan|병렬]] [[001_dikw_pyramid|데이터]] 통로를 [[087_process_state_transition|생성]]한다.

```text
[ Apache Sqoop Architecture ]

 +-------------+        +--------------------------+        +-------------+
 |    RDBMS    |        |       Sqoop Client       |        |    Hadoop   |
 | (Oracle,    | <----> | (Map-Only MapReduce Job) | <----> | (HDFS, Hive,|
 |  MySQL, etc)|        |      [Parallel I/O]      |        |  HBase)     |
 +-------------+        +------------+-------------+        +-------------+
                                     |
                      +--------------v-------------+
                      |    JDBC Drivers / Connectors|
                      +----------------------------+

[ Bilingual Comparison ]
- Import (임포트): RDBMS에서 하둡으로 데이터를 가져오는 과정.
- Export (익스포트): 하둡에서 RDBMS로 결과 데이터를 내보내는 과정.
- Boundary Query (경계 쿼리): 데이터를 병렬로 쪼개기 위해 Primary Key 범위를 확인하는 쿼리.
- Map-Only Job: 리듀스 단계 없이 매퍼(Mapper)들이 각자 DB에 붙어 데이터를 긁어오는 방식.
```

스쿱은 [[001_dikw_pyramid|데이터]] 전송 시 '리듀스(Reduce)' 단계가 필요 없는 Map-Only 방식으로 동작한다. 이는 [[001_dikw_pyramid|데이터]]를 가공하는 것이 아니라 '운반'하는 것이 목적이기 때문이며, 이 덕분에 매우 빠른 전송 속도를 보장한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 아파치 스쿱 (Apache Sqoop) | [[040_apache_flume|아파치 플룸]] ([[040_apache_flume|Apache Flume]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 원천** | **[[002_structured_data|정형 데이터]] (RDBMS, [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]])** | [[004_unstructured_data|비정형 데이터]] (Log, SNS, Sensor) |
| **전송 방식** | 배치(Batch) 방식, 벌크 이관 | 실시간(Real-time) 스트리밍 수집 |
| **동작 기반** | [[018_mapreduce|맵리듀스]] 잡 실행 | 에이전트(Source/Channel/Sink) 기반 |
| **주요 용도** | **기존 DB의 과거 [[001_dikw_pyramid|데이터]] 전량 이관** | 서버 [[568_logs_distributed_logging_elk_fluentd|로그]] 실시간 수집 |
| **기술사적 판단** | 정적 [[001_dikw_pyramid|데이터]]의 [[212_synchronization_mechanisms|동기화]]에 최적 | 동적 [[001_dikw_pyramid|데이터]]의 흐름 처리에 최적 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **([[430_index_fast_full_scan|병렬]] 처리 최적화)** `--num-mappers` 옵션을 통해 [[430_index_fast_full_scan|병렬]]도를 조절한다. 너무 높이면 운영 DB에 과부하를 주고, 너무 낮으면 전송이 느려진다. 통상 DB 서버의 [[282_performance_tactics|성능]]과 네트워크 [[140_bandwidth|대역폭]]을 고려하여 4~8개 사이에서 시작한다.
- **(증분 임포트 [[268_strategy_pattern|전략]])** 매번 전체 [[001_dikw_pyramid|데이터]]를 가져오는 것은 낭비다. `--incremental append`나 `--check-column` 옵션을 사용하여 마지막으로 가져온 이후에 추가된 [[001_dikw_pyramid|데이터]](신규 ID 등)만 긁어오는 것이 실무의 정석이다.
- **(커넥터 최적화)** 일반 JDBC 대신 오라클 전용 커넥터(OraOop) 등을 사용하면 특정 DB의 내부 메커니즘을 활용해 훨씬 더 빠른 전송 속도를 낼 수 있다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
아파치 스쿱은 [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])를 구축하기 위한 첫 번째 단추인 '[[001_dikw_pyramid|데이터]] 이관'을 표준화한 기술이다. 최근에는 실시간 [[217_cdc_binlog_change_capture_debezium|CDC]]([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) 기술에 밀려 배치성 작업으로 국한되는 경향이 있으나, 대량의 이력을 한 번에 옮기는 벌크 이관에는 여전히 스쿱만한 도구가 없다. 기술사는 스쿱을 통해 운영계와 분석계 사이의 [[001_dikw_pyramid|데이터]] 이동 [[268_strategy_pattern|전략]]을 수립할 수 있어야 한다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **JDBC (Java [[501_database|Database]] Connectivity)**: 스쿱이 DB에 접속하는 표준 방식
- **Map-Only Job**: 스쿱의 [[430_index_fast_full_scan|병렬]] 전송 엔진
- **[[215_etl_vs_elt_pipeline|ETL]]**: 추출(E)과 적재(L)의 핵심 도구
- **[[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]])**: 스쿱의 배치 방식을 대체하는 실시간 기술

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 ETL 스크립트 — JDBC 기반 수동 데이터 추출·적재, 유지보수 부담]
    │
    ▼
[Apache Sqoop — RDBMS ↔ 하둡 MapReduce 병렬 대용량 데이터 전송 자동화]
    │
    ▼
[Apache Flume — 로그·스트림 실시간 수집, HDFS·HBase 적재 파이프라인]
    │
    ▼
[Apache Kafka Connect — 분산 커넥터 프레임워크, RDBMS·클라우드 소스 실시간 CDC]
    │
    ▼
[CDC (Change Data Capture) — Debezium 기반 변경분만 스트리밍 추출·전달]
    │
    ▼
[데이터 레이크하우스 Ingestion — Apache Iceberg·Delta Lake 직접 ACID 적재]
```
이 흐름은 수동 JDBC 스크립트에서 Sqoop [[430_index_fast_full_scan|병렬]] 배치 전송으로 자동화된 뒤, 실시간 CDC와 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 직접 적재로 진화하는 [[001_dikw_pyramid|데이터]] 수집 [[123_pipe|파이프]]라인 기술의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 아파트 이사를 갈 때 짐을 하나씩 옮기면 너무 힘들겠지?
- 스쿱은 이삿짐 트럭 여러 대를 동시에 불러서, 집 안의 가구들을 한꺼번에 새집으로 옮겨주는 이삿짐센터 아저씨야.
- "어디에 있는 짐을 어디로 옮겨주세요"라고 말만 하면, 아주 빠르고 안전하게 짐을 옮겨준단다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 39 / 262

← **이전**: [[038_apache_pig|16. 아파치 피그 (Apache Pig) - 하둡 데이터 흐름 스크립팅]]
**다음**: [[040_apache_flume|18. 아파치 플룸 (Apache Flume) - 대규모 로그 수집 및 전송]] →

---
