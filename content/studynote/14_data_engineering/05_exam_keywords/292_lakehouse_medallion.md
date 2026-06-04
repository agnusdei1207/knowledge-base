+++
title = "292. 데이터 레이크하우스 메달리온 아키텍처 (Data Lakehouse Medallion Architecture)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 레이크하우스의 메달리온 아키텍처는 원시 데이터(Bronze) -> 정제·통합 데이터(Silver) -> 비즈니스 집계·모델링 데이터(Gold)로 점진적 정제(Progressive Refinement)를 수행하는 **다층 데이터 조직화 패턴**이며, Delta Lake/Iceberg/Hudi 기반의 **ACID 트랜잭션, 스키마 진화, 타임 트래블(Time Travel)** 을 통해 레이크의 유연성과 웨어하우스의 신뢰성을 동시 확보한다.
> 2. **가치**: 단일 스토리지(예: S3/ADLS/GCS)에 모든 데이터 등급을 보관함으로써 **스토리지 비용 60~80% 절감**, 데이터 중복 제거 및 단일 진실 공급원(SSOT) 확립, **데이터 리니지 자동 추적**, 배치·스트리밍·ML 워크로드의 통합 처리, 분석 인사이트 도출 시간(TTI) 단축.
> 3. **판단 포인트**: Bronze의 원본 보존 기간 vs 스토리지 비용, Silver의 **Late-arriving Data(지연 도착 데이터) 처리 전략**(Type 1/2 SCD), Gold의 **서빙 계층(Star Schema vs Data Mart vs Feature Store) 분기**, 컴퓨션 엔진 선택(Spark vs Photon vs Trino), 그리고 **증분 처리(Incremental Processing)** vs 전체 재처리(Full Reprocessing) 트레이드오프.

---

## Ⅰ. 개요 및 필요성

기존의 데이터 플랫폼 패러다임은 **데이터 웨어하우스(DW)** 와 **데이터 레이크(DL)** 의 이분법으로 갈려 있었습니다. DW(예: Teradata, Oracle Exadata, Snowflake)는 고품질의 정형 데이터에 대해 강력한 ACID 트랜잭션과 SQL 성능을 제공했지만, 스키마-on-Write의 경직성과 페타바이트급 비정형 데이터 처리 한계, 그리고 비싼 스토리지 비용이 발목이었습니다. 반면 DL(예: Hadoop HDFS, AWS S3 + EMR)은 정형·비정형·반정형 데이터를 schema-on-read로 자유롭게 적재할 수 있었지만, **파일 단위의 원자성 부재(Partial File Writes)**, 트랜잭션 미지원, 작은 파일(Small Files) 문제, 그리고 동시성 제어 부재로 인해 신뢰성 있는 분석 워크로드에 활용하기 어려웠습니다.

메달리온 아키텍처(Medallion Architecture)는 Databricks가 2019~2020년경 Delta Lake 기반의 Lakehouse 비전과 함께 공식화한 **데이터 정제 단계화 패턴**입니다. 이는 **Bronze(원시) -> Silver(정제) -> Gold(집계/서빙)** 의 3단계(필요 시 4단계 이상 확장)로 데이터를 점진적으로 변환·품질 향상시켜, **단일 스토리지에 다층 데이터 등급**을 공존시키는 것이 핵심입니다. ETL이 아닌 ELT 패러다임을 표방하며, 각 레이어는 **물리적·논리적 격리(Physical/Logical Isolation)** 를 통해 독립적 거버넌스와 액세스 제어가 가능합니다.

```text
+------------------------------------------------------------------------+
|                    데이터 소스(Source Systems)                            |
|  +---------+  +---------+  +----------+  +---------+  +------------+  |
|  | RDBMS   |  | Kafka   |  | API/SaaS |  | IoT/Log |  | Files/CSV  |  |
|  |(MySQL)  |  |(Stream) |  |(Salesfoce)| |(Sensor) |  |(SFTP/FTP) |  |
|  +----+----+  +----+----+  +-----+----+  +----+----+  +-----+------+  |
|       |            |             |             |             |          |
|       +------------+-------------+-------------+-------------+          |
|                                | CDC/Streaming/CDC Connector            |
|                                v                                        |
|  +-----------------------------------------------------------------+   |
|  |                  🥉 BRONZE (Raw / Landing)                      |   |
|  |  - Append-Only, 원본 그대로 보존 (Parquet/Delta/Avro/JSON)     |   |
|  |  - Source Schema as-Is, 메타데이터 컬럼 추가 (_ingest_ts, _src) |   |
|  |  - Schema-on-Read 가능, Schema Enforcement로 안전망             |   |
|  +-----------------------------+-----------------------------------+   |
|                                | ① Deduplication (batch_id 기준)         |
|                                | ② Type Casting & Schema Conformance     |
|                                | ③ PII Masking / Tokenization            |
|                                v                                        |
|  +-----------------------------------------------------------------+   |
|  |                  🥈 SILVER (Cleansed / Conformed)               |   |
|  |  - 비즈니스 엔터티 정규화 (Customer, Product, Order 통합)      |   |
|  |  - Slowly Changing Dimensions (SCD Type 1/2) 적용              |   |
|  |  - Data Quality 검증 (Great Expectations, DQX, Soda)            |   |
|  |  - Late-arriving data 처리, 완전 데이터 모델(3NF)               |   |
|  +-----------------------------+-----------------------------------+   |
|                                | ① 비즈니스 집계 (Daily/Monthly KPI)     |
|                                | ② Star Schema (Fact/Dim) 모델링         |
|                                | ③ Feature Engineering (ML용)            |
|                                v                                        |
|  +-----------------------------------------------------------------+   |
|  |                  🥇 GOLD (Curated / Business-Ready)             |   |
|  |  - BI 대시보드용 Star Schema (예: dwh.fact_sales_dd)            |   |
|  |  - ML Feature Store (예: features.user_churn_30d)               |   |
|  |  - 보고·규제 준수(Regulatory) 데이터 마트                       |   |
|  |  - Reverse ETL -> 운영 시스템 피드백                            |   |
|  +-----------------------------------------------------------------+   |
|                                                                        |
|  +-----------------------------------------------------------------+   |
|  |     🗄️  Storage: S3 / ADLS Gen2 / GCS / MinIO / HDFS          |   |
|  |     🔧  Table Format: Delta Lake / Apache Iceberg / Apache Hudi |   |
|  |     ⚙️  Engine: Spark / Photon / Trino / Dremio / Snowflake     |   |
|  +-----------------------------------------------------------------+   |
+------------------------------------------------------------------------+
```

기존 ELT의 약점은 **단일 변환 레이어에서 모든 비즈니스 로직을 처리**하려 들었다는 점입니다. 이는 디버깅을 어렵게 하고, 재처리(Reprocessing) 시 전체 파이프라인을 중단시키며, 데이터 계보(Lineage) 추적의 복잡성을 기하급수적으로 증가시켰습니다. 메달리온 아키텍처는 **관심사 분리(Separation of Concerns)** 원칙을 데이터 영역에 적용한 것으로, **3~5명의 엔지니어가 병렬로 협업 가능한 도메인별 팀 운영**을 가능하게 합니다.

- **📢 섹션 요약 비유**: 광산에서 채굴한 원석(Bronze) -> 보석세공소의 정제·연마(Silver) -> 백화점 진열장의 완제품(Gold)으로 가는 **보석 가공 파이프라인**과 같습니다. 원석은 절대 폐기하지 않고(재처리 대비), 각 단계에서 품질 검사를 거쳐 점진적으로 가치가 상승합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

메달리온 아키텍처는 단순한 폴더 명명 규칙이 아니라, **테이블 포맷(Table Format) + 트랜잭션 로그(Transaction Log) + 데이터 카탈로그(Data Catalog) + 컴퓨션 엔진**이 유기적으로 결합한 **Lakehouse Storage Layer** 위에서 동작합니다. 핵심 메커니즘은 오픈 테이블 포맷(Delta Lake, Apache Iceberg, Apache Hudi)이 제공하는 **로그 기반의 ACID 보장**입니다.

```text
+--------------------------------------------------------------------------+
|                  Medallion Architecture: Deep Technical View             |
+--------------------------------------------------------------------------+

  +--------------- BRONZE LAYER -----------------------------------------+
  |                                                                      |
  |  +----------------+    +---------------------------------------+   |
  |  | Kafka Topic    |---->| Auto Loader (Spark Structured         |   |
  |  | orders.v1.raw  |    | Streaming) -> cloudFiles               |   |
  |  +----------------+    |   • Trigger: 30s/1000 files           |   |
  |                        |   • Schema Location: bronze_schema     |   |
  |                        +--------------+-------------------------+   |
  |                                       |                              |
  |                                       v                              |
  |  +--------------------------------------------------------------+   |
  |  | Table: bronze.orders_raw  (Delta/Iceberg)                    |   |
  |  | -----------------------------------------                    |   |
  |  | Partition: _ingest_date (yyyy-MM-dd)                          |   |
  |  | Columns:  order_id, user_id, raw_payload JSON, _ingest_ts,    |   |
  |  |           _src_system, _batch_id, _kafka_offset              |   |
  |  | Properties:                                                   |   |
  |  |   delta.enableChangeDataFeed = true                           |   |
  |  |   delta.autoOptimize.optimizeWrite = true                     |   |
  |  |   delta.autoOptimize.autoCompact = true                       |   |
  |  | Retention: 90 days (Bronze TTL, VACUUM)                       |   |
  |  +--------------------------------------------------------------+   |
  +---------------------------------------------------------------------+
                                    |  Spark Structured Streaming
                                    |  MERGE INTO (CDC upsert)
                                    |  watermark: 7 days
                                    v
  +--------------- SILVER LAYER -----------------------------------------+
  |                                                                      |
  |  +--------------------------------------------------------------+   |
  |  | Transformation Logic (PySpark / SQL / dbt-on-Spark)          |   |
  |  | -------------------------------------------------            |   |
  |  | 1. bronze.orders_raw.parse_json(payload)                      |   |
  |  | 2. .withColumn("email_norm", lower(trim(col("email"))))      |   |
  |  | 3. .dropDuplicates(["order_id", "user_id"])                  |   |
  |  | 4. .join(silver.dim_customer, "user_id", "left")             |   |
  |  | 5. SCD Type 2: valid_from, valid_to, is_current              |   |
  |  | 6. Data Quality Checks:                                      |   |
  |  |    ✓ NOT NULL on order_id, amount                            |   |
  |  |    ✓ amount BETWEEN 0 AND 10000000                            |   |
  |  |    ✓ email MATCHES regex '^[A-Za-z0-9._%+-]+@…$'            |   |
  |  +--------------------------------------------------------------+   |
  |                                                                      |
  |  +--------------------------------------------------------------+   |
  |  | Table: silver.orders_cleansed                                |   |
  |  | Columns: order_id, user_id, order_dt, amount, currency,     |   |
  |  |          status, normalized_email, customer_sk, _loaded_at   |   |
  |  | Liquid Clustering (Delta 3.0+): CLUSTER BY (user_id, order_dt)|  |
  |  | Z-Order (legacy): ZORDER BY (user_id, order_dt)               |  |
  |  +--------------------------------------------------------------+   |
  +---------------------------------------------------------------------+
                                    |  dbt incremental model
                                    |  OR Spark batch aggregation
                                    v
  +--------------- GOLD LAYER -------------------------------------------+
  |                                                                      |
  |  +--------------------+  +--------------------+  +--------------+  |
  |  | gold.fact_sales_dd |  | gold.dim_customer  |  | gold.mart_   |  |
  |  | (Star Schema,      |  | (Conformed Dim)    |  |    kpi_daily |  |
  |  |  daily grain)      |  |                    |  |  (Aggregate) |  |
  |  +--------------------+  +--------------------+  +--------------+  |
  |                                                                      |
  |  +--------------------------------------------------------------+   |
  |  | Materialization Strategy:                                    |   |
  |  |   • BI/Dashboard: Dynamic Table / Materialized View (Snowflake)| |
  |  |   • ML: Delta Table -> Feast/Tecton Feature Store            |   |
  |  |   • Reverse ETL: Hightouch / Airbyte -> Salesforce, HubSpot  |   |
  |  +--------------------------------------------------------------+   |
  +---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Bronze Layer (Raw Zone)** | 원본 데이터의 불변(Immutable) 보존, 데이터 사일로 해체 | Delta Lake의 `MERGE INTO` + Change Data Feed, `cloudFiles`(Auto Loader)로 증분 처리. 메타데이터 컬럼(`_ingest_ts`, `_src_system`, `_batch_id`)을 자동 주입하여 **데이터 카디널리티 보존** 및 리니지 추적 기반 마련. |
| **Silver Layer (Conformed/Refined)** | 데이터 정제, 중복 제거, 비즈니스 규칙 적용, 엔터티 정규화 | **Slowly Changing Dimensions (SCD Type 1/2)** 적용으로 Slowly Changing 비즈니스 키의 이력 관리. Great Expectations, Soda Core, Databricks DQX로 데이터 품질 계약(Data Quality Contract) 시행. **Time Travel**(`VERSION AS OF`, `TIMESTAMP AS OF`)으로 과거 시점 디버깅. |
| **Gold Layer (Curated/Serving)** | 도메인별 집계, KPI 산출, ML 피처, BI 마트 | **Star Schema(Kimball)** 또는 **Data Vault 2.0** 모델링. Photon, Snowflake Dynamic Table, Materialize, Apache Pinot으로 서빙 계층 구성. dbt의 `incremental_strategy='merge'`로 효율적 갱신. |
| **Storage & Table Format** | ACID 트랜잭션, 스키마 진화, 타임 트래블, 벡터 검색 통합 | **Delta Lake** (transaction log `_delta_log/`), **Apache Iceberg** (metadata.json, manifest list), **Apache Hudi** (timeline 기반). 모두 객체 스토리지(S3/ADLS/GCS) 위에서 작동. |

**핵심 메커니즘 - Delta Lake Transaction Log 상세**:
Delta Lake의 `_delta_log/` 폴더에는 JSON/Checkpoint 파일이 저장됩니다. 각 트랜잭션마다 `add`, `remove`, `metaData`, `protocol`, `txn` 액션이 추가되며, **Optimistic Concurrency Control(OCC)** 방식으로 동시성 충돌을 해결합니다. `MERGE INTO` 시 Bronze 테이블에 신규 도착한 레코드는 `_commit_version` 단위로 식별되어 Silver에 CDC 방식으로 반영됩니다. 이를 통해 **Exactly-Once Semantics(정확히 한 번 의미론)** 가 보장됩니다.

**Z-Ordering vs Liquid Clustering vs Partitioning**:
- **Partition**: `_ingest_date=2024-01-15/` 형태로 디렉토리 분할. 카디널리티가 낮은 컬럼에 적합.
- **Z-Order**: 다차원 클러스터링. Delta Lake의 `OPTIMIZE table ZORDER BY (col1, col2)`. 데이터 파일 내에서 정렬되어 데이터 스킵(Data Skipping) 효율 극대화.
- **Liquid Clustering** (Delta 3.0+): Z-Order의 후속 기술. 데이터 크기 변화에 따라 자동 클러스터링 키 조정. `CLUSTER BY (user_id, order_dt)`.

- **📢 섹션 요약 비유**: 메달리온은 **뉴스 편집국의 3단계 검수 시스템**과 같습니다. 1차(통신사로부터 받은 원고=Bronze) -> 2차(사실 확인·교정·표준 용어 통일=Silver) -> 3차(독자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 292 / 300

<- **이전**: [291. 아이스버그 후디 델타 레이크 테이블 형식 (Iceberg Hudi Delta Lake Table Format)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/291_iceberg_hudi_delta/)
**다음**: [293. 데이터 관측 가능성 이상 탐지 SLO (Data Observability Anomaly Detection SLO)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/293_data_observability/) ->

---
