+++
weight = 224
title = "224. 데이터 레이크하우스 (Data Lakehouse)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]([[210_data_lakehouse_delta_lake|Data Lakehouse]])는 [[208_data_lake_schema_on_read|데이터 레이크]]의 **저비용·유연성**과 [[001_dikw_pyramid|데이터]] 웨어하우스의 **ACID [[191_transaction_concept_states|트랜잭션]]·고성능 [[298_qkv_attention|쿼리]]**를 [[494_object_storage|오브젝트 스토리지]](S3) 위에서 통합한 차세대 아키텍처다.
> 2. **가치**: DW와 레이크를 이중으로 운영하는 비용·복잡성을 제거하고 **단일 플랫폼에서 BI 분석·ML·실시간 스트리밍을 동시 지원**한다.
> 3. **판단 포인트**: [[147_delta_lake|Delta Lake]]([[074_photon_engine|Databricks]]), [[148_apache_iceberg|Apache Iceberg]], Apache Hudi가 [[494_object_storage|오브젝트 스토리지]] 위에 **[[191_transaction_concept_states|트랜잭션]] 레이어**를 추가하는 방식이며, [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]](Bronze·Silver·Gold)가 표준 설계 패턴이다.

---

## Ⅰ. 개요 및 필요성

2020년대 초 Databricks가 제창한 **[[210_data_lakehouse_delta_lake|Data Lakehouse]]** 아키텍처는 [[208_data_lake_schema_on_read|데이터 레이크]]와 [[001_dikw_pyramid|데이터]] 웨어하우스의 장점을 융합하려는 시도에서 출발했다.

**기존 이중 구조의 문제점:**
- DW와 레이크를 별도 운영 → 비용 2배, 파이프라인 중복
- DW에 있는 [[001_dikw_pyramid|데이터]] → ML은 레이크에서 학습 → 최신성 불일치
- 레이크의 ACID 부재 → [[276_write_through|동시 쓰기]] 충돌, 부분 실패 후 [[001_dikw_pyramid|데이터]] 오염

```
[기존 이중 아키텍처]                  [레이크하우스 통합]
┌─────────────────┐                 ┌──────────────────────┐
│   Data Lake      │                 │    Data Lakehouse     │
│  (ML/탐색용)     │                 │                      │
│  S3 + Parquet   │   → 통합 →     │  S3 + Delta Lake     │
└─────────────────┘                 │  ┌────────────────┐   │
┌─────────────────┐                 │  │ ACID 트랜잭션   │   │
│  Data Warehouse │                 │  │ 스키마 진화     │   │
│  (BI/SQL용)     │                 │  │ 타임트래블      │   │
│  Snowflake/BQ   │                 │  │ ML + BI 통합   │   │
└─────────────────┘                 │  └────────────────┘   │
                                    └──────────────────────┘
```

📢 **섹션 요약 비유**: [[146_lakehouse|레이크하우스]]는 "캠핑카"다. 텐트(레이크, 저렴·유연)와 집(웨어하우스, 편안·안전)의 장점을 하나의 차량에 담아, 어디서든 집처럼 생활하면서 비용도 아끼는 최신 아키텍처다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]] ([[194_medallion_architecture_bronze_silver_gold|메달리온 아키텍처]])

```
┌──────────────────────────────────────────────────────────────┐
│                  Data Lakehouse (S3 기반)                     │
│                                                              │
│  ┌─────────────────┐                                         │
│  │   Bronze Zone    │ ← 원시 수집 (CDC/배치/스트리밍)          │
│  │  (Raw/원시)      │   스키마 없음, 원본 보존                  │
│  └────────┬────────┘                                         │
│           │ Spark ETL (데이터 정제)                           │
│           ▼                                                  │
│  ┌─────────────────┐                                         │
│  │   Silver Zone    │   중복 제거, NULL 처리, 타입 통일         │
│  │  (Cleansed/정제) │   ACID 보장, 스키마 등록                 │
│  └────────┬────────┘                                         │
│           │ Spark 집계·비즈니스 로직                           │
│           ▼                                                  │
│  ┌─────────────────┐                                         │
│  │    Gold Zone     │   BI 대시보드 전용 집계 테이블            │
│  │  (Curated/가공)  │   ML Feature Store 연결                 │
│  └─────────────────┘                                         │
└──────────────────────────────────────────────────────────────┘
         ↓ SQL 쿼리 엔진 (Spark SQL / Presto / Athena)
         ↓ BI 도구 (Tableau / Power BI / Looker)
         ↓ ML 플랫폼 (MLflow / SageMaker)
```

### [[146_lakehouse|레이크하우스]] 핵심 기능 비교

| 기능 | [[208_data_lake_schema_on_read|데이터 레이크]] | [[001_dikw_pyramid|데이터]] WH | [[146_lakehouse|레이크하우스]] |
|:---|:---:|:---:|:---:|
| ACID [[191_transaction_concept_states|트랜잭션]] | ❌ | ✅ | ✅ |
| [[005_schema|스키마]] 진화 | 어려움 | 가능 | ✅ |
| BI SQL 지원 | 제한 | ✅ | ✅ |
| ML/[[001_dikw_pyramid|데이터]]과학 | ✅ | 제한 | ✅ |
| 스트리밍 | ✅ | 제한 | ✅ |
| 저장 비용 | 저 | 고 | 저 |
| 오픈 포맷 | ✅ | ❌ | ✅ |
| 타임트래블 | ❌ | ❌ | ✅ |

📢 **섹션 요약 비유**: [[146_lakehouse|레이크하우스]]의 Medallion Architecture는 물 정화 시스템이다. 빗물(원시 [[001_dikw_pyramid|데이터]], Bronze)이 모래 필터(Silver 정제)를 거쳐 정수기(Gold 집계)에서 마시기 좋은 상태가 되는 것처럼, 단계별 정제로 품질을 보장한다.

---

## Ⅲ. 비교 및 연결

### [[147_delta_lake|Delta Lake]] vs [[148_apache_iceberg|Apache Iceberg]] vs [[149_apache_hudi|Apache Hudi]]

| 비교 항목 | [[147_delta_lake|Delta Lake]] | [[148_apache_iceberg|Apache Iceberg]] | [[149_apache_hudi|Apache Hudi]] |
|:---|:---|:---|:---|
| **개발 주체** | [[074_photon_engine|Databricks]] | Netflix | Uber |
| **주요 특징** | [[074_photon_engine|Databricks]] 통합 최적화 | [[012_metadata|메타데이터]] 확장성 우수 | Upsert/[[217_cdc_binlog_change_capture_debezium|CDC]] 특화 |
| **타임트래블** | ✅ VACUUM | ✅ [[637_zfs_snapshot_cow_architecture|Snapshot]] | ✅ Savepoints |
| **ACID** | ✅ | ✅ | ✅ |
| **[[005_schema|스키마]] 진화** | ✅ | ✅ | ✅ |
| **클라우드 지원** | [[074_photon_engine|Databricks]] (AWS/Azure/GCP) | AWS, [[541_cassandra|Snowflake]], Spark | AWS EMR, Spark |
| **컴퓨팅 엔진** | Spark, Trino | Spark, Flink, Trino | Spark, Flink |
| **[[217_cdc_binlog_change_capture_debezium|CDC]] 최적화** | 보통 | 보통 | 우수 (Upsert) |

### [[146_lakehouse|레이크하우스]] 플랫폼 비교

| 플랫폼 | 특성 | 적합 사례 |
|:---|:---|:---|
| **[[074_photon_engine|Databricks]]** | [[147_delta_lake|Delta Lake]] 원조, [[180_mlflow|MLflow]] 통합 | ML+BI 통합, 대형 기업 |
| **AWS Glue + S3** | [[206_serverless_cold_start|서버리스]] [[215_etl_vs_elt_pipeline|ETL]], Iceberg 지원 | AWS 중심 아키텍처 |
| **Azure Synapse** | [[147_delta_lake|Delta Lake]] + SQL Pools | Microsoft 에코시스템 |
| **Google BigLake** | GCS 위 [[263_storage_compute_separation_bigquery|BigQuery]] 테이블 포맷 | GCP 중심 아키텍처 |

📢 **섹션 요약 비유**: [[147_delta_lake|Delta Lake]]·Iceberg·Hudi는 같은 목적지([[146_lakehouse|레이크하우스]])로 가는 세 개의 도로다. Delta Lake는 다분히 고속도로(빠르고 잘 정비됨), Iceberg는 멀티레인 국도(범용성), Hudi는 물류 전용 도로(Upsert 특화)다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[074_photon_engine|Databricks]] 기반 [[146_lakehouse|레이크하우스]] 구현 예시

```python
# Delta Lake 테이블 생성 및 ACID 쓰기
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

# Bronze → Silver 변환 (Upsert with MERGE)
deltaTable = DeltaTable.forPath(spark, "s3://bucket/silver/customers")
deltaTable.alias("silver").merge(
    updates.alias("new"),
    "silver.customer_id = new.customer_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# 타임트래블: 7일 전 데이터 조회
df_old = spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("s3://bucket/silver/customers")
```

### 실무 도입 의사결정 체계

```
[레이크하우스 도입 판단 기준]
Q1: 현재 DW와 레이크를 둘 다 운영 중인가?
  → YES: 레이크하우스로 통합 비용 절감 검토
  → NO: 신규 구축 시 레이크하우스 우선 고려

Q2: ML/AI 워크로드가 BI와 동일한 데이터를 사용하는가?
  → YES: 레이크하우스 도입 강력 권장 (피처 일관성)

Q3: 실시간 데이터 변경(CDC/Upsert)이 필요한가?
  → YES: Hudi 또는 Delta Lake 선택
```

📢 **섹션 요약 비유**: [[146_lakehouse|레이크하우스]] 도입은 사무실과 공장을 따로 쓰다가 스마트팩토리(사무+생산 통합)로 전환하는 것과 같다. [[459_quic_fec_forward_error_correction|초기]] 전환 비용이 있지만, 장기적으로 커뮤니케이션([[001_dikw_pyramid|데이터]] 이동) 비용과 관리 복잡성을 크게 줄인다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 정량 기준 |
|:---|:---|
| **비용 절감** | [[209_data_warehouse_schema_on_write|DW]]+레이크 이중 운영 대비 30~50% 비용 절감 |
| **[[001_dikw_pyramid|데이터]] 신선도** | BI와 ML이 동일 Gold 테이블 사용 → 지표 [[194_consistency_database_integrity|일관성]] |
| **파이프라인 단순화** | [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 수 30~50% 감소 |
| **ACID 보장** | [[276_write_through|동시 쓰기]] 충돌·부분 실패로 인한 [[001_dikw_pyramid|데이터]] 오염 제거 |
| **타임트래블** | 과거 [[001_dikw_pyramid|데이터]] 롤백으로 규정 [[606_auditing_linux_auditd|감사]] 대응 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **성숙도** | 전통 [[209_data_warehouse_schema_on_write|DW]] 대비 운영 노하우 부족 |
| **Small Files 문제** | 빈번한 소량 [[289_cqrs_db|쓰기]] 시 [[501_file_definition_logical_record|파일]] 수 폭발 (OPTIMIZE 정기 실행 필요) |
| **[[012_metadata|메타데이터]] 오버헤드** | Delta Log 관리 비용 증가 |
| **벤더 락인** | Delta Lake는 [[074_photon_engine|Databricks]] 의존성 강함 (Iceberg로 대안 가능) |

📢 **섹션 요약 비유**: [[146_lakehouse|레이크하우스]]는 새로 지은 올인원 복합 공간이다. 처음엔 설계(Delta/Iceberg 선택, Medallion 설계)에 공을 들여야 하지만, 잘 구축하면 ML팀·BI팀·[[001_dikw_pyramid|데이터]]팀 모두 같은 공간에서 협업하여 생산성이 크게 오른다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[147_delta_lake|Delta Lake]] | [[146_lakehouse|레이크하우스]]를 구현하는 핵심 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] |
| [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]] | Bronze-Silver-Gold Zone 설계 패턴 |
| [[148_apache_iceberg|Apache Iceberg]] | Delta Lake의 [[191_oss_license_compliance|오픈소스]] 대안, Netflix 기원 |
| [[009_schema_on_read|Schema-on-Read]] | [[146_lakehouse|레이크하우스]] Bronze Zone의 철학 |
| [[010_schema_on_write|Schema-on-Write]] | [[146_lakehouse|레이크하우스]] Gold Zone의 철학 |
| [[074_photon_engine|Databricks]] | [[147_delta_lake|Delta Lake]] 기반 [[146_lakehouse|레이크하우스]] 상용 플랫폼 |
| ACID [[191_transaction_concept_states|트랜잭션]] | [[146_lakehouse|레이크하우스]]가 레이크와 구분되는 핵심 특성 |

### 👶 어린이를 위한 3줄 비유 설명
1. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 레고로 만든 집이다. 창고(레이크)처럼 아무 레고나 보관하면서도, 집(웨어하우스)처럼 방이 잘 정리되어 있어 원하는 걸 언제든 찾을 수 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
Data Lake: 유연 저장 (거버넌스 약함)
Data Warehouse: ACID + 고성능 쿼리 (비쌈)
    │
    ▼
Lakehouse: Lake 위에 DW 기능 구현
    ├─► Delta Lake (Databricks) · Apache Iceberg · Hudi
    └─► ACID + Time Travel + Schema Evolution
```
2. 마치 스위스 아미 나이프처럼, 하나의 도구([[146_lakehouse|레이크하우스]])가 분석·[[241_machine_learning_basics|머신러닝]]·실시간 [[001_dikw_pyramid|데이터]] 처리를 모두 해결해 주는 만능 [[001_dikw_pyramid|데이터]] 플랫폼이다.
3. 타임트래블 기능은 "되돌리기(Ctrl+Z)" 버튼과 같다. 실수로 [[001_dikw_pyramid|데이터]]를 잘못 바꿔도, 이전 버전으로 돌아갈 수 있어서 안전하게 작업할 수 있다.
