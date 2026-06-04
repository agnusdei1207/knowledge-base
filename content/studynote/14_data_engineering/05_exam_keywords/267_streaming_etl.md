+++
title = "267. 스트리밍 ETL 실시간 파이프라인 설계 (Streaming ETL Real-time Pipeline Design)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스트리밍 ETL은 Kafka/Kinesis 등 로그 기반 메시지 브로커를 Source of Truth로 두고, Flink/Spark Structured Streaming 같은 분산 스트림 프로세서가 Change Data Capture(CDC)로 추출한 변경 이벤트를 Event Time 기준 Watermark·Checkpoint·Exactly-Once Semantics(EOS) 하에서 변환·적재하여 수 초~수 분 내 Downstream 가용성을 보장하는 **Low-Latency Continuous Dataflow**이다.
> 2. **가치**: 기존 야간 배치 대비 데이터 신선도(Freshness)를 T+24h에서 P50 1~5초·P99 30초 수준으로 단축하여, 실시간 사기 탐지·동적 가격 책정·이상 거래 알림 등 Time-Critical 의사결정의 비즈니스 ROI를 직접 창출하며, 동일 데이터 사본을 통해 Batch/AI Serving을 중복 적재 없이 재사용할 수 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **Stateful 처리 비용 vs. Stateless 단순성**, ② **End-to-End EOS를 위한 2PC vs. Sink 측 Idempotent Upsert(MERGE)**, ③ **Lambda(배치+스트림 이원화) vs. Kappa(단일 스트림)**, ④ **Watermark 허용 지연(latency tolerance)에 따른 정확도/지연 균형**, ⑤ **Event Time vs. Processing Time**의 의미론적 차이를 비즈니스 SLA와 데이터 정확성 요구수준으로 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 야간/시간 단위 Batch ETL은 데이터 웨어하우스(DW)·데이터 레이크를 구축하는 데 충분했지만, 디지털 트랜잭션이 마이크로초 단위로 발생하고 고객 행동이 실시간화되는 환경에서는 한계가 명확해졌다. 금융사 사기 탐지(FDS)의 경우 1시간 지연은 이미 막대한 손실을 의미하고, 이커머스 추천 엔진은 5분 전 클릭 이력만으로 CTR이 18~30% 하락한다. 또한 동일 원천 데이터를 분석용 DW, ML Feature Store, 운영용 RDBMS에 중복 적재하며 발생하는 스토리지 비용·정합성 문제(다중 진실 문제)는 배치 시대의 가장 큰 아키텍처 부채였다.

스트리밍 ETL은 RDBMS의 WAL(Write-Ahead Log) 또는 Binlog를 Debezium/Oracle GoldenGate 등으로 추출해 Kafka의 **불변 로그(Immutable Log)** 에 적재하고, 이를 Flink Job이 CDC 이벤트 단위로 변환해 Iceberg·Delta Lake·ClickHouse·DynamoDB 등에 MERGE/INSERT하는 파이프라인이다. 핵심은 원천 DB에 부하를 주지 않으면서(Log-based CDC는 Asynchronous로 동작) 트랜잭션 정합성을 보존하는 것이며, 이를 위해 Debezium은 `read_committed` Snapshot 모드와 `tombstone` 이벤트 처리를 제공한다.

```text
+-------------------------------------------------------------------------+
|         기존 Batch ETL (T+24h, 야간 윈도우) -> Streaming ETL (초 단위)     |
+-------------------------------------------------------------------------+

[Source DB]                  [Stream ETL]                       [Sink]
+----------+    CDC       +------------+   Flink   +--------------------+
| MySQL    |--Binlog------>| Kafka      |--Job------>| Iceberg +          |
| Postgres |              |  - topic A |           |   ClickHouse       |
| Oracle   |              |  - topic B |   CDC     |   + DynamoDB       |
+----------+  Debezium    |  - topic C |  --->      |   + Feature Store  |
                         | (immutable)|  Kafka     |                    |
                         |   KRaft    |  Connect   |  • OLAP Query      |
                         |  cluster   |  (S3 Sink) |  • ML Training     |
                         +------------+            |  • API Serving     |
                                ^                  +--------------------+
                                |
                          +-----+-----+
                          | Schema    |  Avro/Protobuf with
                          | Registry  |  backward-compatible evolution
                          +-----------+

   [Time]
   -----+
   T+0  |  ● 트랜잭션 발생  --->  Kafka  --->  Flink Window  --->  Sink
        |        (ms)            (ms)        (1~30s)
        |
        |
   T+24h|  Batch   ---------------------------->  DW (야간 누락)
        |  ETL     (참고용 Snapshot)            (불필요해짐)
        v
```

- **기존 vs 신규 패러다임**
  - **기존**: RDBMS -> Sqoop/Airflow(1h) -> Hive/Snowflake(15h) -> BI. 총 지연 16h+, 재처리 시 HDFS 전체 재적재.
  - **신규**: RDBMS -> Debezium(ms) -> Kafka(ms) -> Flink(1~30s) -> Lakehouse(s). 재처리는 Consumer Group Offset 리셋 + Kafka Log Replay로 **코드 변경 없이 임의 시점 재생** 가능.

- **📢 섹션 요약 비유**: 야간에 신문을 받아 읽는 것(배치 ETL)에서, 중요한 뉴스는 푸시 알림으로 즉시 받는 알림 서비스(스트리밍 ETL)로 옮겨온 것과 같다. 알림이 오지 않아도 나중에 신문으로 전체 흐름을 다시 확인할 수 있다(Replayability).

---

## Ⅱ. 아키텍처 및 핵심 원리

스트리밍 ETL의 표준 아키텍처는 **Source -> Ingest -> Process -> Sink**의 4단 계층으로 구성되며, 각 계층은 Loose Coupling을 위해 메시지 브로커(Kafka·Pulsar·Kinesis)를 중심에 둔다. End-to-End 정확성을 보장하기 위해 **Source Connector(Fetch/Offset Commit) ↔ Kafka(Broker Replication + Log Compaction) ↔ Flink(Checkpoint + 2PC Sink) ↔ Sink Connector(Exactly-Once Sink Function)**의 4개 경계에서 EOS를 중첩 적용한다.

```text
   +--------------------------------------------------------------------+
   |                  Streaming ETL End-to-End Architecture              |
   +--------------------------------------------------------------------+

   [1. Source]                 [2. Ingest]            [3. Process]
   +----------+                +----------+           +--------------+
   | RDBMS    |                | Kafka    |           | Flink Job    |
   | -------- |   CDC Events   | -------- |   consume | ------------ |
   | MySQL    | --Binlog------->| topic    | ---------->| Source       |
   |  Master  |   (ROW image)  |  orders  |           |   v          |
   |          |                |          |           | Watermark    |
   | Postgres | --WAL---------> | topic    | ---------->|   v          |
   |          |                |  users   |           | Process       |
   | MongoDB  | --Oplog-------> | topic    | ---------->|  • enrich    |
   +----------+                |          |           |  • join       |
        ^                      | -------- |           |  • aggregate |
        |                      | Partition|           |   v          |
   +----+-----+                |  0..N    |           |  Windowing   |
   | Debezium |                |          |           |   v          |
   | Connect  |                |  Schema  |           |  State(Rocks)|
   | Server   |                |  Registry|           |   v          |
   | (Kafka   |                |  (Avro)  |           |  Checkpoint  |
   |  Connect)|                |          |           |   v          |
   +----------+                |  KRaft   |           |  2PC Sink    |
                               |  Controller           +------+-------+
                               +----------+                  |
                                                              v
                              [4. Sink]              +------------------+
                              +----------+           | Lakehouse        |
                              | Iceberg  | <----------|  • S3 + Athena   |
                              | Delta    |           |  • Snowflake     |
                              | Hudi     |           |  • BigQuery      |
                              |          |           |  • ClickHouse    |
                              | Key-Value|           |  • DynamoDB      |
                              | Redis    |           |  • Postgres      |
                              |          |           |  • ElasticSearch |
                              +----------+           +------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Source Connector (Debezium/Kafka Connect)** | RDBMS Binlog/WAL의 변경 이벤트를 Kafka 토픽으로 비동기 발행. Source DB의 Transaction Log Reader로 동작하여 Lock 없이 일관된 스냅샷 제공 | Debezium은 MySQL의 `binlog_reader=binlog_client_v4`, Postgres의 `pgoutput`/`wal2json` 플러그인을 사용. `snapshot.mode=initial`(전체 스냅샷 후 증분 전환) 또는 `schema_only`. `tombstone`은 Soft Delete의 전파를 위해 `__deleted` 컬럼과 null value로 발행 |
| **Message Broker (Kafka KRaft)** | 모든 CDC 이벤트의 불변 로그(Immutable, Append-only) 저장. Consumer Group별 Offset으로 재생·재처리 지원. Log Compaction으로 Key별 최종 상태만 유지 | KRaft 모드(ZooKeeper 제거, Raft 합의)로 메타데이터 관리 단순화. `min.insync.replicas=2`, `acks=all`, `enable.idempotence=true`로 Leader Epoch 기반 중복 방지. `cleanup.policy=compact`로 Changelog 토픽 운영 |
| **Schema Registry (Confluent/Apicurio)** | Avro/Protobuf 스키마 버전 관리. Producer/Consumer 간 Contract 보장 및 Backward/Forward/Full 호환성 검증 | Schema ID는 Wire Format에 인라인 임베드(Magic Byte + Schema ID). `compatibility=BACKWARD`로 신규 필드 default 추가만 허용, 필드 삭제는 불가. CI 단계에서 Compatibility Check 필수 |
| **Stream Processor (Flink/Spark Structured Streaming)** | Stateful 변환(Join, Aggregate, Enrichment), Window 연산, Watermark 기반 Event Time 처리, Exactly-Once Checkpoint | Flink는 Chandy-Lamport 분산 스냅샷을 주기적(보통 10~60s)으로 RocksDB State Backend에 저장. Barrier Alignment로 병렬 Subtask 간 일관성 보존. 두 번의 Checkpoint 완료로 멱등성 보장. Watermark는 `(event_time - max_out_of_orderness)`로 설정 |
| **Sink (Lakehouse/OLAP/KV)** | 변환 결과를 영구 저장. MERGE(UPSERT) 지원 여부가 EOS 구현 가능 여부를 결정 | Iceberg의 `V2` Hidden Partition + MOR(Merge-on-Read) Delete File로 Row-level Update 지원. ClickHouse는 `ReplacingMergeTree` + `FINAL` 또는 `Lightweight Update`. DynamoDB는 Conditional Write로 멱등성 보장 |
| **Orchestration & Observability** | 파이프라인 배포·모니터링·장애 대응. Flink Job은 Savepoint로 버전 업그레이드 시 상태 보존 | Kubernetes(Operator 패턴: Strimzi, Flink Kubernetes Operator), Prometheus + Grafana, OpenLineage(Marquez)로 Lineage 추적, PagerDuty 연동 Alert |

### 핵심 메커니즘 심층 분석

**1. Exactly-Once Semantics(EOS) — "데이터는 한 번도 빠짐없이, 한 번뿐이 아니라 정확히 한 번만 반영되어야 한다"**

EOS는 다음 4가지가 동시 만족되어야 달성된다.
- **Idempotent Source**: Kafka 자체가 동일 Offset을 재처리해도 동일 Record를 반환(아직 Offset Commit 전이면).
- **Deterministic Processing**: Flink는 동일 입력 + 동일 상태 -> 동일 출력 보장. 단, `currentTimestamp()`·Random·UUID 같은 비결정적 함수 사용 시 깨짐.
- **Atomic Checkpoint**: Flink의 Barrier가 모든 Parallel Instance를 통과해야 Checkpoint 성공. 실패 시 State와 Kafka Offset을 함께 롤백.
- **Idempotent/Transactional Sink**:
  - **2PC Sink** (Kafka -> JDBC/Exactly-Once Sink Function): Sink가 `beginTransaction` -> `invoke` -> `preCommit` -> `commit` 4단계로 JDBC에 2PC 적용. 단, Sink DB가 XA Transaction을 지원해야 함(Postgres·MySQL은 제한적).
  - **Idempotent Sink** (Lakehouse MERGE): `UPSERT WHERE _op = 'd' DELETE` 형태로 Key 기준 멱등. 실전에서 가장 많이 사용.

**2. Watermark & Event Time**

`Watermark(t) = max(event_time) - max_out_of_orderness`로 정의하며, `t` 이후의 이벤트는 더 이상 도착하지 않을 것이라고 **낙관적으로 가정**하는 메커니즘.

$$W(t) = \max_{seen}(\text{event\_time}) - \text{idle\_timeout}$$

- `Bounded Out-of-Orderness`: 5분 허용 시 `W(t) = max_event_time - 5min`. 너무 작으면 Late Event가 Drop, 너무 크면 Latency 증가.
- `Punctuated Watermark`: Source 레코드 일부에 Watermark 정보 임베드.
- `Idle Source Detection`: Kafka Partition이 데이터를 일시적으로 안 보내면 Watermark 진행 정지 -> TM(TaskManager)이 자동 감지.

**3. Stateful Stream Processing**

Flink의 `Keyed State`는 RocksDB에 LSM-Tree로 저장되며, Checkpoint 시 `sst` 파일을 Streaming으로 S3/HDFS에 업로드. TB 단위 상태도 처리 가능하나, State Size가 크면 Checkpoint 시간과 Recovery 시간이 선형 증가. **State Schema Evolution** 시 `AvroSerializer`와 `State Schema Registry`를 함께 사용해야 Job 재시작 시 역직렬화 실패를 방지한다.

**4. Kafka의 KRaft 모드**

기존 ZooKeeper 의존을 제거한 Raft 합의 기반 컨트롤러. 단일 Controller(Scalability 한계) 문제를 해결하기 위해 KRaft 2.0+에서는 Multi-Controller(Quorum of Controllers) 지원. Producer는 `acks=all` + `enable.idempotence=true`로 Leader Epoch 기반 중복 제거 수행.

- **📢 섹션 요약 비유**: 스트리밍 ETL은 택배의 실시간 배송 추적 시스템과 같다. 상점에서 주문이 들어오면(Database Transaction), 분류 센터(Kafka)가 각 배송 차량별로 분류하고, 배송 기사(Flink)가 주소 변경·시간대별 재배분(Enrichment)을 거쳐 고객에게 전달(Sink)한다. 중간에 문제가 생기면 출고 시점부터 다시 분류를 시작(Replay)할 수 있다.

---

## Ⅲ. 비교 및 연결

스트리밍 ETL은 여러 유사 개념과 명확히 구분되어야 한다. 가장 자주 혼동되는 것은 **Batch ETL**, **Lambda Architecture**, **ELT**이며, 의사결정 시 핵심 차이를 정확히 파악해야 한다.

| 구분 | Batch ETL (전통) | Lambda Architecture | Kappa Architecture (스트리밍 ETL) | ELT (Modern DW) |
| :--- | :--- | :--- | :--- | :--- |
| **지연 시간 (Latency)** | T+12h ~ T+24h | 실시간(Layer) + 배치(보정) | P50 1~5초, P99 30초 | T+1h ~ T+24h (dbt 기반) |
| **코드 중복** | 없음 (단일 파이프라인) | 있음 (Batch Layer + Speed Layer 동일 로직 2벌) | 없음 (단일 스트림 코드) | 없음 (SQL 변환) |
| **재처리 방식** | 전체 재적재(Full Reload) | Batch Layer가 Raw 데이터로 재계산 | Kafka Log Replay (Offset Reset) | 테이블 전체 REPLACE |
| **State 관리** | 단순 (DB 테이블 JOIN) | 복잡 (2개 Layer 동기화) | 중간 (Flink State) | 없음 (DW 엔진이 처리) |
| **적합 Use Case** | 일간 리포팅, 정합성 최우선 | 추천
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 267 / 300

<- **이전**: [266. 데이터 사일로 해소 통합 전략 (Data Silo Breaking Integration Strategy)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/266_data_silo_integration/)
**다음**: [268. 벡터 데이터베이스 임베딩 유사도 검색 (Vector Database Embedding Similarity Search)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/268_vector_database/) ->

---
