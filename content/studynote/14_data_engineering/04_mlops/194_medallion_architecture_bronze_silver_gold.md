---
title: "194. Medallion Architecture Bronze Silver Gold"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 194
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 메달리온 아키텍처(Medallion [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))는 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Bronze) -> 정제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Silver) -> 비즈니스 집계(Gold) 3계층으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질을 점진적으로 향상하는 [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) 설계 패턴이다.
> 2. **가치**: Delta Lake의 ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), Time Travel, [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution 기능과 결합하여 신뢰할 수 있는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)를 구성하고, 계층별 접근 권한 분리로 보안과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 달성한다.
> 3. **판단 포인트**: [Inmon](/studynote/12_it_management/05_security_compliance/953_inmon/) [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)), [Kimball](/studynote/12_it_management/05_security_compliance/954_kimball/) DM([스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [볼트](/studynote/15_devops_sre/05_devsecops/236_vault_dynamic_secrets_ttl/)([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Vault](/studynote/09_security/11_iam_access_control/567_vault/)) 대비 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성과 원본 보존이 강점이며, 빠르게 변하는 비즈니스 요구에 민첩하게 대응한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 메달리온 아키텍처 배경

Databricks가 정의한 메달리온 아키텍처는 전통적 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 경직성과 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 품질 문제를 동시에 해결하는 <strong><a href="/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/">데이터 레이크하우스</a>(<a href="/studynote/16_bigdata/07_data_lake/146_lakehouse/">Lakehouse</a>)</strong> 설계 패턴이다.

### 1.2 전통 아키텍처의 한계

| 아키텍처 | 문제점 |
|:---|:---|
| 전통 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 어려움, [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리 불가 |
| [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) (단순) | "[데이터 늪](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)([Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))" — 품질 관리 부재 |
| [람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/) | 배치/스트림 코드 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 운영 복잡성 |

### 1.3 메달리온 아키텍처 3계층 개요

```
외부 데이터 소스
(운영 DB, 로그, API, 스트림)
        |
        v
+-------------------+
|   BRONZE 레이어    |  <- 원시 데이터 그대로 적재
|   (동메달)         |    스키마 없음, 이력 보존
+--------+----------+
         | 정제/검증 ETL
         v
+-------------------+
|   SILVER 레이어    |  <- 정제·표준화 데이터
|   (은메달)         |    PII 마스킹, 중복 제거
+--------+----------+
         | 집계/비즈니스 로직
         v
+-------------------+
|    GOLD 레이어     |  <- 비즈니스 집계 데이터
|   (금메달)         |    Feature Store, 대시보드
+-------------------+
```

📢 **섹션 요약 비유**: 메달리온 아키텍처는 원석(Bronze) -> 세공(Silver) -> 완성 보석(Gold)으로 가공하는 보석 제작 과정이다. 각 단계에서 가치가 더해지지만, 원석은 항상 보존된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Bronze 레이어 (원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

Bronze는 소스 시스템에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>있는 그대로(<a href="/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/">Raw</a>)</strong> 적재하는 레이어다. 변환 없이 원본 보존이 핵심이다.

| 특성 | 내용 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형태 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), CSV, [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), Avro, 이진 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) | Schemaless 또는 느슨한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) |
| 목적 | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)), 재처리 원본 |
| 보존 기간 | 무기한 (규정에 따라) |
| 접근 권한 | 엔지니어만 접근 |

```
Bronze 레이어 적재 예시 (Databricks)

df = spark.read \
     .format("kafka") \
     .option("kafka.bootstrap.servers", "...") \
     .load()

# 원본 그대로 Delta 저장 (변환 없음)
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/orders/")
```

### 2.2 Silver 레이어 (정제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

Bronze [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>정제, <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>, 표준화</strong>하여 분석 가능한 형태로 변환한다.

| 처리 항목 | 상세 내용 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 캐스팅 | 문자열 -> 날짜, 정수 등 |
| 결측값 처리 | NULL 처리, 기본값 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| 중복 제거 | deduplicate by primary [key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) |
| PII 마스킹 | 이메일, 전화번호 해시화 |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 표준화 | 컬럼명 통일, 단위 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | not_null, [referential integrity](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) |

```
Silver 레이어 변환 예시

from pyspark.sql.functions import col, sha2, to_timestamp

df_bronze = spark.read.format("delta") \
                      .load("/mnt/bronze/orders/")

df_silver = df_bronze \
    .dropDuplicates(["order_id"]) \
    .withColumn("email_masked", sha2(col("email"), 256)) \
    .withColumn("created_at", to_timestamp("created_at_str")) \
    .filter(col("order_id").isNotNull()) \
    .drop("email", "created_at_str")

df_silver.write \
         .format("delta") \
         .mode("overwrite") \
         .option("mergeSchema", "true") \
         .save("/mnt/silver/orders/")
```

### 2.3 Gold 레이어 (비즈니스 집계)

Silver [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 <strong>비즈니스 로직을 적용한 집계 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>로, 최종 사용자가 직접 소비한다.

| 사용 목적 | 구현 방식 |
|:---|:---|
| 비즈니스 대시보드 | 일/주/월 집계 [KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/) 테이블 |
| ML [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 모델 학습용 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 집계 |
| [데이터 마트](/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) | 부서별 최적화 뷰 |
| 실시간 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서빙 | 사전 집계된 고성능 조회 |

### 2.4 Delta Lake와의 결합

```
+---------------------------------------------------------+
|              Delta Lake 핵심 기능                         |
|                                                         |
|  +------------------+  +------------------------------+ |
|  | ACID 트랜잭션     |  | Time Travel (시간 여행)        | |
|  |                  |  |                              | |
|  | 동시 읽기/쓰기    |  | DESCRIBE HISTORY orders;     | |
|  | 충돌 없는 업데이트|  | SELECT * FROM orders         | |
|  | Commit Log 기반  |  | VERSION AS OF 5;             | |
|  +------------------+  +------------------------------+ |
|                                                         |
|  +------------------+  +------------------------------+ |
|  | Schema Evolution  |  | Z-Ordering (클러스터링)        | |
|  |                  |  |                              | |
|  | 컬럼 추가 자동 반영|  | 쿼리 성능 최적화              | |
|  | 하위 호환성 유지  |  | 데이터 스킵핑                 | |
|  +------------------+  +------------------------------+ |
+---------------------------------------------------------+
```

| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 기능 | 메달리온 활용 |
|:---|:---|
| ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | Bronze 동시 적재 안전성 |
| Time Travel | Silver 재처리 시 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 조회 |
| [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution | Gold 새 컬럼 추가 무중단 |
| OPTIMIZE/VACUUM | 소파일 병합, 만료 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 정리 |
| Change [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Feed | Bronze -> Silver 증분 처리 |

📢 **섹션 요약 비유**: Delta Lake는 메달리온 공장의 안전 설비다. 제품([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 동시에 여러 라인에서 처리되어도 충돌이 없고(ACID), 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 되돌아갈 수 있는 타임머신(Time Travel)도 제공한다.

---

## Ⅲ. 비교 및 연결

### 3.1 메달리온 vs 전통 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 아키텍처 비교

| 항목 | [Inmon](/studynote/12_it_management/05_security_compliance/953_inmon/) [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Kimball](/studynote/12_it_management/05_security_compliance/954_kimball/) DM | [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Vault](/studynote/09_security/11_iam_access_control/567_vault/) | 메달리온 |
|:---|:---|:---|:---|:---|
| 설계 원칙 | [3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | [스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/) | [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-Satellite | 계층별 품질 향상 |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성 | 낮음 | 중간 | 높음 | 매우 높음 |
| 원본 보존 | 없음 | 없음 | 있음([Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) | 완전 보존(Bronze) |
| 학습 난이도 | 높음 | 중간 | 높음 | 낮음 |
| [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) | 불가 | 불가 | 어려움 | 가능 |
| 재처리 용이성 | 어려움 | 어려움 | 중간 | 쉬움(Bronze 재처리) |
| 주요 도구 | Teradata, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) | Redshift, [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/), dbt | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/), Delta |

### 3.2 계층별 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)

```
데이터 접근 권한 계층화

+------------------------------------------+
|  GOLD          (비즈니스 사용자, 분석가)  |
|  - 최종 집계 데이터 조회                 |
|  - BI 도구 (Tableau, Power BI) 연결     |
+------------------------------------------+
|  SILVER         (데이터 분석가, 데이터팀) |
|  - 정제된 데이터 분석                    |
|  - 머신러닝 피처 엔지니어링              |
+------------------------------------------+
|  BRONZE          (데이터 엔지니어만)      |
|  - 원시 데이터 접근                     |
|  - 재처리 및 디버깅                     |
+------------------------------------------+
```

### 3.3 실시간 스트림 처리와 메달리온 결합

| 계층 | 스트리밍 처리 방식 |
|:---|:---|
| Bronze | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)/Kinesis -> Delta Streaming Writer |
| Silver | [Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) + Trigger.Once |
| Gold | Micro-batch 집계 (5분~1시간 윈도우) |

📢 **섹션 요약 비유**: 메달리온 vs [Inmon](/studynote/12_it_management/05_security_compliance/953_inmon/)/Kimball은 현대식 공장 vs 전통 공장의 차이다. 전통 공장은 설계도([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/))를 먼저 완벽히 만들어야 하지만, 메달리온은 일단 원재료(Bronze)를 쌓아두고 필요에 따라 가공하는 유연한 공장이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 메달리온 아키텍처 도입 단계

```
단계 1: Bronze 구성 (1주)
  +- 소스 시스템별 Kafka 토픽 연결
  +- Delta Lake 테이블 생성
  +- Auto Loader로 자동 적재 설정

단계 2: Silver 구성 (2~4주)
  +- 데이터 품질 규칙 정의
  +- PII 마스킹 정책 적용
  +- Great Expectations 데이터 검증

단계 3: Gold 구성 (지속적)
  +- 비즈니스 지표 정의 (KPI)
  +- dbt 모델로 변환 로직 관리
  +- BI 도구 연결
```

### 4.2 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리 도구

| 도구 | 계층 | 기능 |
|:---|:---|:---|
| Great Expectations | Bronze->Silver | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 규칙 |
| dbt Tests | Silver->Gold | SQL 기반 테스트 |
| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) Constraints | Bronze | 제약 조건 강제 |
| [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) [DLT](/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) (Delta Live Tables) | 전체 | 선언적 파이프라인 |

### 4.3 실무 예시: e커머스 주문 파이프라인

```
[주문 이벤트 발생]

    Kafka Topic: order-events
         |
         v
    BRONZE: orders_raw
    +-------------------------------------+
    | order_id, raw_json, ingested_at,    |
    | source_system, partition, offset    |
    | (변환 없음, 장기 보존)               |
    +----------------+--------------------+
                     | Spark Streaming
                     v
    SILVER: orders_cleaned
    +-------------------------------------+
    | order_id, user_id_hash, amount,     |
    | status, created_at(timestamp),      |
    | (중복 제거, PII 해시, 타입 변환)     |
    +----------------+--------------------+
                     | dbt 모델
                     v
    GOLD: daily_order_summary
    +-------------------------------------+
    | date, total_orders, total_revenue,  |
    | avg_order_value, cancellation_rate  |
    | (일별 KPI 집계)                     |
    +-------------------------------------+
```

### 4.4 기술사 논술 핵심 판단 기준

| 비교 항목 | 선택 기준 |
|:---|:---|
| 메달리온 선택 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 불확실, [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 많음, [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 환경 |
| [Kimball](/studynote/12_it_management/05_security_compliance/954_kimball/) 선택 | 안정적 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴, [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최우선 |
| [Inmon](/studynote/12_it_management/05_security_compliance/953_inmon/) 선택 | 대기업 표준화, 복잡한 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) |
| [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Vault](/studynote/09_security/11_iam_access_control/567_vault/) 선택 | 이력 관리 최우선, 규제 산업 |

📢 **섹션 요약 비유**: 메달리온 아키텍처 도입은 도서관 정리 시스템을 도입하는 것이다. 처음에는 기증받은 책(Bronze)을 모두 받아두고, 사서([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어)가 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·정리(Silver)한 후, 독자(사용자)가 찾기 쉬운 추천 목록(Gold)을 만든다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 메달리온 아키텍처 기대효과

| 효과 | 정량 지표 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 향상 | Bronze -> Gold 오류율 95% 감소 |
| 재처리 용이성 | Bronze 원본으로 언제든 재처리 |
| 거버넌스 강화 | 계층별 접근 권한으로 보안 강화 |
| 개발 생산성 | dbt 모듈화로 변환 로직 재사용 |
| 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | Delta Time Travel로 즉시 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |

### 5.2 메달리온 + [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 연계

```
메달리온 데이터로 ML 파이프라인 구성

GOLD 레이어 피처 데이터
    |
    v
Feature Store (Databricks / Feast)
    |
    +---> 모델 학습 (MLflow 추적)
    +---> 온라인 서빙 (Redis 조회)
         실시간 예측 API
```

### 5.3 결론 요약

메달리온 아키텍처는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 "[데이터 늪](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)" 문제를 계층별 품질 향상으로 해결하는 실용적 패턴이다. Delta Lake와의 결합으로 ACID 보장, 시간 여행, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화를 모두 지원하며, 기술사 관점에서는 <strong><a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 유연성 vs <a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> 트레이드오프를 이해하고, 조직의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 성숙도에 맞는 아키텍처 선택 근거를 제시할 수 있어야 한다.

📢 **섹션 요약 비유**: 메달리온 아키텍처의 최종 가치는 원석(원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 항상 보존하면서 점점 더 가치 있는 보석(비즈니스 인사이트)으로 가공하는 것이다. 언제든 원석으로 돌아가 새로운 가공 방법을 시도할 수 있다는 점이 전통 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)와의 결정적 차이다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 아키텍처 패턴 | Medallion [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) (메달리온) | Bronze/Silver/Gold 3계층 품질 향상 |
| 스토리지 엔진 | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | ACID + Time Travel + [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution |
| 비교 | [Inmon](/studynote/12_it_management/05_security_compliance/953_inmon/) [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 기반 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) |
| 비교 | [Kimball](/studynote/12_it_management/05_security_compliance/954_kimball/) DM | [스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/) 기반 DM |
| 비교 | [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Vault](/studynote/09_security/11_iam_access_control/567_vault/) | [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-Satellite 이력 관리 |
| 플랫폼 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) [Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/) | 메달리온 표준 구현 환경 |
| 품질 관리 | Great Expectations | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 프레임워크 |
| 변환 관리 | dbt | SQL 기반 Silver->Gold 변환 |
| 실시간 처리 | Delta Live Tables ([DLT](/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/)) | 선언적 스트리밍 파이프라인 |

### 👶 어린이를 위한 3줄 비유 설명

1. 메달리온 아키텍처는 원석(Bronze) -> 다듬기(Silver) -> 완성 보석(Gold) 순으로 보석을 만드는 과정이에요. 각 단계에서 더 예쁘고 가치 있어지죠.

### 📈 관련 키워드 및 발전 흐름도

```text
Raw 데이터 수집 (CSV · JSON · 로그)
    |
    v
Bronze 계층: 원시 데이터 그대로 적재 (append-only)
    |
    v
Silver 계층: 정제 · 스키마 적용 · 중복 제거 · 조인
    |
    v
Gold 계층: 비즈니스 KPI · 집계 테이블 · ML 피처
    |
    v
소비: BI 대시보드 · ML 파이프라인 · Ad-hoc 분석
```
2. Bronze는 마치 창고에 쌓아둔 재료 상자예요. 버리지 않고 다 보관해서, 나중에 "아, 이게 필요했구나!" 할 때 꺼낼 수 있어요.
3. Gold는 손님(사용자)이 바로 쓸 수 있도록 예쁘게 포장된 선물 같아요. 복잡한 계산은 이미 다 끝났고, 바로 숫자만 보면 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 194 / 258

<- **이전**: [193. 뉴로모픽 반도체 (Neuromorphic Chip) SNN 저전력 추론](/studynote/14_data_engineering/04_mlops/193_neuromorphic_chip_snn_low_power_inference/)
**다음**: [195. 연방 쿼리 (Federated Query) 데이터 패브릭 분산 메타 통계망 조인](/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) ->

---
