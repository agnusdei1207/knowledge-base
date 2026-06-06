---
title: "Data Engineering PE Master Architecture Map"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 엔지니어링 종합 아키텍처는 **Source -> Ingestion -> Storage(Lake/Lakehouse) -> Processing(Batch/Stream) -> Serving -> Consumption**의 6계층 파이프라인에 **거버넌스(Metadata/Catalog/Lineage), 보안(AuthN/AuthZ/Masking), 오케스트레이션(Airflow/Dagster), 옵저버빌리티(OpenTelemetry/Datadog)**를 횡단 관심사로 직조한 End-to-End 청사진이며, Lambda·Kappa·Lakehouse·Data Mesh 패턴이 이를 구현하는 핵심 토대입니다.
> 2. **가치**: 단일 데이터 카탈로그 기반 **데이터 발견성(Discoverability) 70% 향상**, **Time-to-Insight 50% 단축**, **ETL 중복 개발 60% 절감**, **GDPR/개인정보보호법 컴플라이언스 자동화**를 통한 법적 리스크 제거, 그리고 **도메인별 Self-service Analytics** 실현으로 전사 데이터 자산의 ROI 극대화.
> 3. **판단 포인트**: **배치 vs 스트리밍**(지연시간 허용치 SLO 기준), **단일 클러스터 vs 분리 컴퓨트 스토리지**(Snowflake/BigQuery vs Spark+HDFS), **중앙집중형 모놀리스 vs 도메인 자율형 Data Mesh**(조직 규모와 데이터 성숙도), **Pull-based CDC(Debezium) vs Push-based Streaming(Kafka)**, **강한 스키마(Avro/Protobuf) vs 약한 스키마(JSON)** — 이 5대 결정이 전체 TCO와 운영 복잡도를 좌우합니다.

---

## Ⅰ. 개요 및 필요성

데이터 엔지니어링은 2010년 Hadoop 기반 배치 ETL에서 시작해, 2015년 Kafka·Spark Streaming의 등장으로 실시간 처리가 가능해졌고, 2020년 Delta Lake·Iceberg·Hudi로 대표되는 **Lakehouse** 패러다임이 출현하면서 데이터 레이크의 유연성과 데이터 웨어하우스의 ACID 트랜잭션을 동시에 확보했습니다. 2023년 이후에는 **Data Mesh**(도메인 자율성 + Federated Governance)와 **DataOps**(CI/CD for Data), **AI/MLOps 통합**으로 진화하며, 더 이상 단일 기술 스택이 아닌 **다층 하이브리드 아키텍처**의 시대가 도래했습니다.

기술사 시험 관점에서, 데이터 엔지니어링은 **"데이터가 태어나는 순간부터 가치를 창출하는 순간까지의 전 과정을 어떻게 설계·구축·운영할 것인가"**에 대한 통합적 답안이며, 다음 4가지 배경 도전에 대응하기 위해 종합 아키텍처 청사진이 필수적입니다.

- **데이터 볼륨·속도·다양성의 폭발**: 단일 시스템으로는 100TB+ 일일 처리, 초당 수백만 이벤트, 100+ 소스 포맷(CDC, 로그, IoT, API) 처리 불가
- **사일로화(Silo) 문제**: 부서별·프로젝트별 독립 파이프라인으로 인한 **중복 개발 40~60%**, **데이터 정합성 결함**, **메타데이터 단절**
- **실시간 비즈니스 요구**: 전통적 야간 배치(D+1)는 리테일 추천, 이상거래 탐지, 동적 가격 결정에 부적합
- **규제·컴플라이언스 강화**: GDPR, 개인정보보호법, 데이터3법, AI기본법으로 **데이터 계보(Lineage) 추적**, **PII 마스킹**, **접근통제**의 자동화 요구

```text
[End-to-End Data Engineering Master Architecture Map]

+------------------------------------------------------------------------------+
|  CONSUMPTION LAYER (데이터 소비)                                              |
|  +------------+  +------------+  +------------+  +------------+              |
|  | BI/Dashboard|  | ML/AI/MLOps|  | Reverse ETL |  | API/Apps   |              |
|  | Tableau/Looker|  |SageMaker/  |  |Hightouch/  |  |GraphQL/REST|              |
|  | Power BI    |  |Vertex AI   |  | Census     |  |            |              |
|  +------+------+  +------+------+  +------+------+  +------+------+              |
|---------+----------------+----------------+----------------+------------------|
|         v                v                v                v                  |
|  SERVING LAYER (데이터 서빙)                                                  |
|  +------------+  +------------+  +------------+  +------------+              |
|  | Star Schema |  | Wide Column |  | Search/Vec |  | OLAP Cube  |              |
|  | Snowflake/  |  | ClickHouse/ |  | Elasticsearch| | Druid/    |              |
|  | BigQuery/   |  | Doris/      |  | OpenSearch/ |  | Pinot/     |              |
|  | Redshift    |  | StarRocks   |  | Milvus/Pinecone| Apache Kylin|            |
|  +------^------+  +------^------+  +------^------+  +------^------+              |
|---------+----------------+----------------+----------------+------------------|
|         | Gold/Serving   |                |                |                  |
|  PROCESSING LAYER (데이터 처리)              |                |                  |
|  +--------------------------+  +--------------------------+                  |
|  | BATCH (배치)               |  | STREAM (스트리밍)          |                  |
|  | Spark/Databricks/EMR/    |  | Flink/Kafka Streams/     |                  |
|  | Trino/Hive/Batch ETL     |  | Spark Structured Stream  |                  |
|  | dbt (in-warehouse)        |  | Materialize/Decodable    |                  |
|  +--------------+-----------+  +--------------+-----------+                  |
|-----------------+------------------------------+------------------------------|
|                 |   +--------------------------+------------+                 |
|                 v   v                                       |                 |
|  STORAGE LAYER (저장소 - Lakehouse)                          |                 |
|  +----------------------------------------------------+    |                 |
|  |  Bronze (Raw) -> Silver (Cleansed) -> Gold (Conformed)|   |                 |
|  |  +----------+  +----------+  +----------+         |    |                 |
|  |  | Delta Lake|  | Iceberg  |  | Apache Hudi|        |    |                 |
|  |  | (Open)   |  | (Open)   |  | (Open)    |         |    |                 |
|  |  | + Parquet|  | + Parquet|  | + Parquet |         |    |                 |
|  |  +----------+  +----------+  +----------+         |    |                 |
|  |  Object Store: S3 / ADLS / GCS / MinIO / HDFS     |    |                 |
|  |  Table Format: ACID, Schema Evolution, Time Travel |    |                 |
|  +----------------------------------------------------+    |                 |
|------------------------------------------------------------|-----------------|
|  INGESTION LAYER (수집)                                   |                 |
|  +------------+  +------------+  +------------+  +------------+              |
|  | CDC        |  | Event Stream|  | Batch/ETL  |  | API/SDK    |              |
|  | Debezium   |  | Kafka/      |  | Airbyte/   |  | Custom     |              |
|  | Maxwell/   |  | Pulsar/     |  | Fivetran/  |  | Ingest     |              |
|  | Oracle     |  | Kinesis/    |  | Sqoop/     |  | Service    |              |
|  | GoldenGate |  | EventHubs   |  | NiFi       |  |            |              |
|  +------+------+  +------+------+  +------+------+  +------+------+              |
|---------+----------------+----------------+----------------+------------------|
|         v                v                v                v                  |
|  SOURCE LAYER (데이터 소스)                                                   |
|  RDBMS | NoSQL | SaaS APIs | IoT/MQTT | Logs | Files | Social/3rd-party       |
+------------------------------------------------------------------------------+

+------------------------------------------------------------------------------+
|  CROSS-CUTTING CONCERNS (횡단 관심사 - 모든 계층에 적용)                      |
|  +------------------------------------------------------------------------+  |
|  | ORCHESTRATION: Airflow / Dagster / Prefect / Temporal / Argo Workflows |  |
|  | METADATA & CATALOG: Unity Catalog / Glue Catalog / Hive Metastore /   |  |
|  |                     DataHub / Apache Atlas / Amundsen / OpenMetadata  |  |
|  | DATA QUALITY: Great Expectations / Soda Core / Monte Carlo / Datafold |  |
|  | OBSERVABILITY: OpenTelemetry / Datadog / Monte Carlo / Bigeye /      |  |
|  |                Grafana / Prometheus                                    |  |
|  | SECURITY: IAM (RBAC/ABAC) / Vault / KMS / SSO / OAuth2/OIDC /        |  |
|  |           Apache Ranger / AWS Lake Formation / Column-level Masking   |  |
|  | GOVERNANCE: PII Discovery / Lineage (OpenLineage) / Data Contracts /  |  |
|  |             Consent Mgmt / Retention Policy / Master Data Mgmt        |  |
|  | DEVOPS/DATAOPS: dbt + Git (CI/CD) / Terraform / Docker / K8s /        |  |
|  |                  ArgoCD / Pulumi / Schema Registry / Backfill tools    |  |
|  +------------------------------------------------------------------------+  |
+------------------------------------------------------------------------------+
```

**전통적 방식 vs 종합 아키텍처 접근 비교**

| 관점 | 전통적 방식 (Point Solution) | 종합 아키텍처 (Master Map) |
|---|---|---|
| 파이프라인 | 부서별 독립 ETL, 중복 50%+ | 도메인별 표준 패턴, 재사용 컴포넌트 |
| 데이터 지연 | D+1 야간 배치 위주 | 실시간 CDC + 마이크로 배치 + 배치 하이브리드 |
| 거버넌스 | 사후 관리, 스프레드시트 카탈로그 | 자동 메타데이터 수집, Lineage 추적 |
| 비용 | 전용 클러스터 유휴 70% | 분리 컴퓨트·스토리지, 오토스케일링 |
| 장애 대응 | 수동 재처리, SLA 미정의 | 데이터 SLO 정의, 자동 알림, Backfill 자동화 |

- **📢 섹션 요약 비유**: 종합 아키텍처는 **병원 진료 시스템**과 같습니다. 응급실(실시간 스트리밍), 외래(배치 처리), 검사실(데이터 검증), 의무기록실(메타데이터 카탈로그), 약국(서빙 레이어)이 각자의 역할을 하면서도 **환자(데이터)** 한 명에 대해 모든 기록이 통합되고, 감염관리(거버넌스)와 보안요원(보안)이 전체를 감시하는 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 6계층(Layer) 아키텍처 상세

#### ① Source Layer (데이터 발생원)

데이터 엔지니어링의 시작점이며, 다음 4가지 특성을 분류합니다.

- **OLTP Source**: MySQL, PostgreSQL, Oracle, SQL Server — CDC가 핵심
- **NoSQL/Semi-structured**: MongoDB, Cassandra, DynamoDB, Redis — CDC 한계로 애플리케이션 이중 쓰기 또는 Oplog Tail
- **SaaS/API**: Salesforce, HubSpot, Stripe, Workday — Pull-based API (Fivetran/Airbyte) 또는 Webhook Push
- **IoT/Edge**: MQTT(Kafka Connect MQTT), Kinesis Agent, OPC-UA — 시계열 특화 처리

#### ② Ingestion Layer (수집)

데이터의 **속도와 신뢰성**을 결정하는 첫 관문입니다.

- **CDC(Change Data Capture)**: Debezium 기반 MySQL Binlog -> Kafka Connect -> Kafka Topic 구조가 표준. **단, Debezium은 Snapshot 시 Lock-less algorithm**(consistent snapshot via binlog position)으로 운영 DB 부하 최소화가 핵심
- **Event Streaming**: Kafka(파티션 1개당 순서 보장, exactly-once semantics는 트랜잭션 프로듀서 + idempotent 컨슈머 조합), Pulsar(계층 스토리지), AWS Kinesis(완전관리형)
- **Batch Ingestion**: Airbyte(300+ 커넥터 오픈소스), Fivetran(매니지드), Spark Sqoop, AWS DMS

#### ③ Storage Layer (Lakehouse)

2020년 이후 데이터 엔지니어링의 가장 큰 패러다임 변화가 일어난 계층입니다.

```text
[Lakehouse 내부 구조 - Delta Lake 기준]

+------------------------------------------------------------+
|                      DELTA LAKE PROTOCOL                    |
|  +--------------+  +--------------+  +----------------+   |
|  | _delta_log/  |  | Parquet Files|  | Checkpoint     |   |
|  | JSON/Parquet |  | (Columnar)   |  | _last_checkpoint|   |
|  | (Transaction |  | Compressed   |  | (10 commits)   |   |
|  |  Log)        |  | Snappy/ZSTD  |  |                |   |
|  +--------------+  +--------------+  +----------------+   |
|  ACID | Schema Evolution | Time Travel | OPTIMIZE | VACUUM |
+------------------------------------------------------------+
         ^                                    |
         |                                    |
    Write Path                          Read Path
   (Streaming)                       (Spark/Trino/Flink)
         |                                    |
+--------+--------+                  +--------+--------+
| Medallion       |                  |  Query Engine   |
| Architecture    |                  |  Spark / Trino  |
|                |                  |  Photon / DBI   |
| Bronze (Raw)   | -----► Read ---► |  Presto/Polars  |
| - 원본 그대로   |                  |                 |
| - append-only  |                  +-----------------+
| - ingestion ts |
|                |
| Silver (Clean) |
| - 중복 제거    |
| - 스키마 강제  |
| - PII 마스킹   |
| - 데이터 품질  |
|                |
| Gold (Curated) |
| - 비즈니스 집계|
| - 도메인별 모델|
| - SCD Type 2   |
| - KPI/Metric   |
+----------------+
```

| Open Table Format | 개발사 | 핵심 차별점 | 컴퓨트 엔진 |
|---|---|---|---|
| **Delta Lake** | Databricks (Linux Foundation) | 가장 성숙, UniForm으로 Iceberg 호환 | Spark, Trino, Flink, Snowflake, BigQuery |
| **Apache Iceberg** | Netflix -> Apache | Hidden Partition, 강한 스키마 진화 | Spark, Trino, Flink, Snowflake, BigQuery, Dremio |
| **Apache Hudi** | Uber -> Apache | Record-level Index, 빠른 Upsert
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 299 / 300

<- **이전**: [298. AI 에이전트 도구 사용 자율 워크플로 (AI Agent Tool Use Autonomous Workflow)](/studynote/14_data_engineering/05_exam_keywords/298_ai_agent_workflow/)
**다음**: [300. 300. 데이터 및 AI 아키텍트 전용 고득점 암기 단어장 집대성](/studynote/14_data_engineering/05_exam_keywords/300_summary/) ->

---
