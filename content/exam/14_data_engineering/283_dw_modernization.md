---
title: "DW Modernization Cloud Migration"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단일 노드에서 결합된 스토리지-컴퓨트 구조를 가진 레거시 DW(Teradata, Netezza, Oracle Exadata, SAS)를 S3/ADLS/GCS 기반 객체 스토리지와 독립적으로 확장 가능한 MPP 컴퓨트 엔진(Snowflake, BigQuery, Redshift, Synapse, Databricks)으로 분리·재구축하는 과정이며, ETL 중심에서 **ELT + Lakehouse + DataOps** 패러다임으로 전환하는 것을 포함한다.
> 2. **가치**: 동일 워크로드 대비 인프라 비용 40~70% 절감(Teradata->Snowflake 사례 평균), 신규 분석 워크로드 가용 시간(Time-to-Insight) 1/5~1/10 단축, 페타바이트급 데이터에 대한 **auto-scaling, zero-copy clone, data sharing**을 통해 TCO 절감과 동시에 분석 민첩성(Analytical Agility)을 동시 확보.
> 3. **판단 포인트**: 단순 **Lift & Shift(Rehost)** 는 소스 호환성(예: Teradata SQL -> Snowflake) 문제로 실패율이 높으므로, **워크로드 프로파일링·쿼리 재작성·ETL to ELT 전환·데이터 거버넌스 재설계**를 포함한 Refactor/Replatform 전략이 필수이며, 네트워크 egress 비용·데이터 주권·하이브리드 운영 정책을 사전에 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

데이터 웨어하우스(DW) 모더나이제이션은 단순한 "서버 이관"이 아니라 **분석 아키텍처 패러다임의 전환**이다. 1990~2010년대 구축된 1세대 DW는 MPP(Exadata, Teradata, Netezza, Vertica, Greenplum) 엔진을 중심으로 **Storage-Compute Tight Coupling** 구조를 채택해, 디스크 I/O 확장이 곧 컴퓨트 노드 확장을 의미했다. 또한 운영계(OLTP) 시스템에서 야간 배치로 데이터를 추출·변환·적재하는 **ETL(Extract-Transform-Load)** 패턴이 표준이었다.

그러나 2020년대에 들어 **클라우드 객체 스토리지**(S3, ADLS Gen2, GCS)의 가격 급락, **칼럼형 압축**(Parquet, ORC, Delta), **분산 MPP 엔진의 SaaS화**, 그리고 **데이터 레이크하우스(Lakehouse)** 개념의 등장으로 DW의 정체성이 재정의되었다. Gartner는 2024년 기준 신규 DW 구축의 80% 이상이 클라우드 기반임을 보고했으며, 기존 DW의 60% 이상이 3년 내 모더나이제이션 대상이 될 것으로 전망했다.

```text
+---------------------------------------------------------------------+
|           레거시 DW(2000s) vs 클라우드 DW(2020s) 패러다임 비교      |
+---------------------------------------------------------------------+
|                                                                     |
|  [레거시 On-Premise DW]                  [Cloud-Native DW]          |
|  +------------------+                   +------------------+        |
|  |  ETL Tool        |                   |  ELT/Streaming   |        |
|  | (Informatica,    |                   | (dbt, Fivetran,   |        |
|  |  DataStage)      |                   |  Airbyte, Kafka) |        |
|  +---------+--------+                   +---------+--------+        |
|            |                                        |                |
|  +---------v--------+                   +---------v--------+        |
|  | Staging Area     |                   | Bronze Layer     |        |
|  | (전처리 수행)    |                   | (Raw Lake)       |        |
|  +---------+--------+                   +---------+--------+        |
|            |                                        |                |
|  +---------v--------+                   +---------v--------+        |
|  | Warehouse Engine | ◄-- 결합 --►      | Storage(S3/ADLS)|        |
|  | (Teradata,       |    Storage/Compute | + Compute(MPP)  |        |
|  |  Exadata,        |                   | Decoupled       |        |
|  |  Netezza)        |                   +---------+--------+        |
|  +---------+--------+                             |                  |
|            |                              +------v------+           |
|  +---------v--------+                     | Silver/Gold |           |
|  | BI Tool          |                     | (Refined)   |           |
|  | (Cognos, BO)     |                     +------+------+           |
|  +------------------+                            |                  |
|                                       +----------v--------+        |
|                                       | BI/AI/ML          |        |
|                                       | (Tableau, PowerBI,|        |
|                                       |  ML/AI 통합)      |        |
|                                       +-------------------+        |
+---------------------------------------------------------------------+
```

**왜 클라우드 이관이 필요한가?**

- **비용 구조의 전환**: 라이선스 + 하드웨어 CAPEX 기반 -> 종량 과금(OPEX) + Auto-suspend. Snowflake의 경우 컴퓨트가 60초 이상 유휴 시 자동 중단되어 비용이 0으로 수렴.
- **워크로드 격리**: 레거시 DW는 BI 대시보드, 배치 리포팅, ETL 작업이 동일 클러스터 리소스를 점유해 SLA 보장이 어려웠다. Snowflake/BigQuery는 **Multi-Cluster Warehouse** 및 **워크로드 분리(ETL 전용, BI 전용)**로 QoS 보장.
- **데이터 볼륨 폭증**: 일 평균 수십 TB의 로그, IoT, 클릭스트림을 야간 배치로 처리하던 체계로는 한계. **스트리밍 CDC + 마이크로 배치 + 컬럼 압축**으로 처리량 10배 이상 향상.
- **ML/AI 워크로드 통합**: 기존 DW는 정형 분석에만 최적화되어 비정형 데이터(이미지, 텍스트, 로그)와의 통합이 불가. Lakehouse는 Delta Lake, Iceberg, Hudi를 통해 ML 피처 스토어 역할까지 수행.
- **거버넌스 및 컴플라이언스**: GDPR, 데이터 3법, 클라우드 보안인증(ISMS-P, ISO 27001, SOC 2) 대응을 위해 통합 카탈로그(Unity Catalog, Glue Catalog, Purview) 필요.

- **📢 섹션 요약 비유**: 레거시 DW가 "**주방, 식당, 창고를 모두 합쳐놓은 단독주택**"이었다면, 클라우드 DW는 "**대형 냉장창고(S3)** + 필요할 때만 빌려 쓰는 **공용 주방(MPP 엔진)** + 여러 손님이 동시에 즐기는 **뷔페 레스토랑**"이다. 음식(데이터)이 들어오면 창고에 쌓아두고, 손님(분석가)이 주문을 할 때만 요리사(컴퓨트)를 고용하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 DW 모더나이제이션의 핵심은 **Storage-Compute Decoupling**, **컬럼형 스토리지 + Micro-partition**, **Multi-Cluster Elasticity**, **Data Sharing**, **Lakehouse Pattern(Medallion Architecture)** 의 5대 기술 원리이다.

```text
+----------------------------------------------------------------------+
|        Cloud DW Modernized Architecture (Lakehouse Reference)       |
+----------------------------------------------------------------------+
|                                                                      |
|   [Sources]                                                          |
|   +----+ +----+ +----+ +----+ +----+                                |
|   |OLTP| |SaaS| |IoT | |Log | |API |                                |
|   +-+--+ +-+--+ +-+--+ +-+--+ +-+--+                                |
|     +------+------+------+------+                                    |
|                     |                                                 |
|   +-----------------v------------------+                             |
|   |  Ingestion Layer                  |                             |
|   |  - CDC: Debezium, AWS DMS, Striim |                             |
|   |  - Streaming: Kafka, Kinesis,      |                             |
|   |    Pub/Sub, Event Hubs             |                             |
|   |  - Batch: Fivetran, Airbyte,      |                             |
|   |    Informatica, NiFi               |                             |
|   +-----------------+------------------+                             |
|                     |                                                 |
|   +-----------------v------------------+  +-----------------+       |
|   |  BRONZE Layer (Raw Lake)           |  |  Catalog        |       |
|   |  Object Storage: S3 / ADLS / GCS   |◄-|  Unity / Glue / |       |
|   |  Format: Delta / Iceberg / Parquet |  |  Purview / Hive |       |
|   |  Schema-on-Read, Time-Travel       |  +-----------------+       |
|   +-----------------+------------------+                             |
|                     |  dbt / Spark / Snowpipe / Auto Loader          |
|   +-----------------v------------------+                             |
|   |  SILVER Layer (Cleansed, Conformed)|                             |
|   |  - 데이터 품질 검증(Great Expectations)|                          |
|   |  - 중복 제거, 타입 표준화          |                             |
|   |  - Slowly Changing Dimensions 처리 |                             |
|   +-----------------+------------------+                             |
|                     |                                                 |
|   +-----------------v------------------+                             |
|   |  GOLD Layer (Business-Ready)       |                             |
|   |  - 도메인별 Conformed Dimension    |                             |
|   |  - KPI, Aggregate, Mart            |                             |
|   |  - Feature Store for ML            |                             |
|   +-----------------+------------------+                             |
|                     |                                                 |
|   +-----------------v------------------------------------------+     |
|   |  Consumption Layer                                         |     |
|   |  BI: Tableau, Power BI, Looker, Superset                   |     |
|   |  AI/ML: Databricks ML, SageMaker, Vertex AI, Bedrock       |     |
|   |  Data Sharing: Secure Data Sharing, Delta Sharing, Clean Rooms|   |
|   |  Reverse ETL: Hightouch, Census -> CRM/Marketing             |     |
|   +------------------------------------------------------------+     |
|                                                                      |
|   [Cross-Cutting Concerns]                                           |
|   +------------+ +------------+ +------------+ +------------+        |
|   |  Security  | | Observab.  | | FinOps     | | DataOps    |        |
|   | RBAC/ABAC  | | OpenLineage| | Usage Mon. | | CI/CD      |        |
|   | KMS, Vault | | Prometheus | | Reserved   | | dbt Cloud  |        |
|   | Row-Level  | | DataDog    | | Capacity   | | Airflow    |        |
|   +------------+ +------------+ +------------+ +------------+        |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Storage Layer** (객체 스토리지) | 데이터의 영구 저장소. 컴퓨트와 분리되어 무제한 확장 가능. | S3/ADLS Gen2/GCS는 11 9s(99.999999999%) 내구성. 데이터는 **Parquet/ORC + Snappy/ZSTD** 컬럼 압축. Snowflake는 **Micro-partition**(50~500MB 단위 자동 분할) + 컬럼별 통계(min/max/null count) 자동 수집으로 **Pruning** 최적화. |
| **Compute Layer** (MPP 엔진) | 쿼리 실행·변환 처리. 워크로드별로 독립 스케일. | Snowflake **Virtual Warehouse**(XS~6XL, Multi-cluster), BigQuery **Slot**(예약/온디맨드), Redshift **Cluster/Concurrency Scaling**, Databricks **Job Cluster vs All-purpose Cluster**, Synapse **Dedicated SQL Pool vs Serverless**. |
| **Metadata/Catalog Layer** | 테이블 스키마, 라인리지, 파티션, 통계, 거버넌스 정보 | **Hive Metastore, AWS Glue Data Catalog, Azure Purview, Unity Catalog, DataHub, Amundsen, Atlas**. **OpenLineage** 표준으로 데이터 흐름 추적. |
| **Ingestion/CDC** | 운영계->DW 실시간·배치 적재 | **CDC**: Debezium, AWS DMS, Fivetran HVR, Striim, Oracle GoldenGate. **Streaming**: Kafka Connect + Schema Registry, Kinesis Data Streams, Pub/Sub Lite. **Auto Loader**(Databricks) - 파일 도착 디렉토리 기반 증분 수집. |
| **Transformation Layer** | 데이터 정제·비즈니스 로직 적용 | **dbt**(SQL 기반 변환 + 테스트 + 문서화), **Spark Structured Streaming**, **Snowpark**(Snowflake 내 Python/Java UDF), **BigQuery Scripting + Stored Procedures**, **Dataform**(Google 인수). |
| **Orchestration/Workflow** | 의존성·스케줄·재시도 관리 | **Apache Airflow, Dagster, Prefect, AWS Step Functions, Azure Data Factory, GCP Cloud Composer**. SLA·backfill·idempotency 보장 필수. |
| **Observability/FinOps** | 비용·성능·품질 모니터링 | **Monte Carlo, Soda, Great Expectations, Datafold**(데이터 품질), **CloudZero, Vantage, Apptio**(FinOps), **OpenTelemetry + Grafana**(쿼리 성능). |

**핵심 원리 심화**

1. **Storage-Compute Decoupling**: Snowflake는 "데이터는 S3에, 컴퓨트는 EC2에서, 메타데이터는 자체 서비스 레이어에서" 관리. 컴퓨트 종료 시에도 데이터는 유지되며, 다른 컴퓨트가 즉시 이어서 처리 가능. 이는 레거시 DW의 "노드 추가 = 스토리지·컴퓨트 동시 증가" 비효율 제거.

2. **Micro-partition + Columnar Pruning**: 1억 행 테이블에서 쿼리 조건이 `date='2024-01-01'`이면, Snowflake는 메타데이터에서 해당 파티션만 스캔(Partition Pruning). 컬럼 단위 저장이므로 `SELECT name FROM t WHERE ...`에서 name 컬럼만 읽음. Teradata 대비 스캔량 1/100~1/1000.

3. **Zero-Copy Clone**: Snowflake/Databricks의 `CREATE TABLE CLONE`은 메타데이터만 복사해 즉시 완료. 테스트/개발 환경을 위한 데이터 복제 비용 0. 이를 통해 Dev/Stage/Prod 격리 용이.

4. **Data Sharing**: Snowflake의 **Secure Data Sharing**은 물리적 복사 없이 계정/리전 간 테이블 공유. Databricks의 **Delta Sharing**은 오픈 프로토콜로 AWS·Azure·GCP·On-Prem 어디서든 소비 가능. SAP·Salesforce·공급사가 외부 파트너에게 실시간 데이터 제공.

5. **Result Cache / Materialized View**: BigQuery는 동일 쿼리 24시간 내 재실행 시 캐시 반환(무료). Snowflake는 24시간 Result Cache. **Dynamic Tables / Materialized Views**는 자동 증분 갱신.

- **📢 섹션 요약 비유**: 클라우드 DW는 "**도서관의 무한 창고** + **필요할 때만 부르는 번역가들** + **찾아주는 도서 분류 시스템**"이 합쳐진 것이다. 책(데이터)은 무한 창고(S3)에 한 권도 안 잃고 보관되고, 손님이 번역(쿼리)을 요청하면 그때만 번역가(컴퓨트)가 투입되어 빨리 찾아준다.

---

## Ⅲ.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 283 / 300

<- **이전**: [282. 오픈 데이터 공공데이터 포털 표준 API (Open Data Public Data Portal Standard API)](/studynote/14_data_engineering/05_exam_keywords/282_open_data_portal/)
**다음**: [284. 실시간 분석 HTAP 하이브리드 트랜잭션 (Real-time Analytics HTAP Hybrid Transaction)](/studynote/14_data_engineering/05_exam_keywords/284_htap_realtime_analytics/) ->

---
