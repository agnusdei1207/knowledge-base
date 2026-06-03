---
title: 8. 데이터 레이크하우스 (Data Lakehouse) - 데이터 레이크의 유연성/저비용과 DW의 ACID 트랜잭션, SQL 성능을 단일
  계층에 결합한 현대 아키텍처 (Databricks, Snowflake)
date: '2024-05-15'
description: 데이터 레이크의 확장성과 DW의 신뢰성을 결합한 레이크하우스의 등장 배경, Iceberg/Delta 기반의 오픈 테이블 포맷
  원리 및 실무 도입 전략을 분석합니다.
tags:
- data_engineering
---

# [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] ([[210_data_lakehouse_delta_lake|Data Lakehouse]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[208_data_lake_schema_on_read|데이터 레이크]]의 무한한 확장성(비용 효율성, [[004_unstructured_data|비정형 데이터]] 지원)과 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]의 [[001_dikw_pyramid|데이터]] 관리 기능(ACID [[191_transaction_concept_states|트랜잭션]], [[001_dikw_pyramid|데이터]] 품질 보장)을 단일 시스템으로 결합한 차세대 개방형 [[001_dikw_pyramid|데이터]] 아키텍처입니다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]가 레이크와 DW로 이중 복제되는 투 투어(2-Tier) 구조의 [[002_silo_hyeonhyung|사일로]] 현상과 막대한 [[215_etl_vs_elt_pipeline|ETL]] 병목을 제거하여, 스토리지 비용을 최소화하면서 실시간 BI 분석과 머신러닝을 하나의 단일 플랫폼에서 동시에 처리합니다.
> 3. **융합**: AWS S3 같은 클라우드 객체 스토리지 위에 [[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]] 등 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 통제하는 '[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]([[196_opentableformat|Open Table Format]])' [[012_metadata|메타데이터]] 계층을 융합하여 구현됩니다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

**[[210_data_lakehouse_delta_lake|데이터 레이크하우스]] ([[210_data_lakehouse_delta_lake|Data Lakehouse]])**는 전통적인 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]])와 1세대 [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])가 가진 각각의 치명적 한계를 극복하기 위해 탄생한 융합형 아키텍처입니다.

최근 10년간 기업들은 [[002_structured_data|정형 데이터]]를 다루는 고가의 DW와 [[004_unstructured_data|비정형 데이터]]를 모아두는 저렴한 [[208_data_lake_schema_on_read|데이터 레이크]]를 분리하여 운영하는 **2-Tier(투 티어) 아키텍처**를 고수해 왔습니다. 하지만 이 구조는 [[001_dikw_pyramid|데이터]]가 레이크에 먼저 쌓인 뒤, 분석을 위해 다시 DW로 복제되어야 하는 근본적인 비효율성을 낳았습니다. 끊임없는 [[215_etl_vs_elt_pipeline|ETL]](Extract, Transform, Load) 복사 과정에서 [[001_dikw_pyramid|데이터]] 정합성이 깨지고, 파이프라인 유지보수 비용이 폭증했으며, [[208_data_lake_schema_on_read|데이터 레이크]] 자체는 ACID [[191_transaction_concept_states|트랜잭션]](수정/삭제)을 지원하지 않아 [[791_gdpr_eu|GDPR]] 같은 규제 대응이나 실시간 [[001_dikw_pyramid|데이터]] 갱신에 속수무책이었습니다. 이를 해결하기 위해 레이크의 저렴한 스토리지 위에 DW의 신뢰성을 직접 이식하려는 시도가 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]로 결실을 맺었습니다.

```text
[기존 2-Tier 아키텍처의 한계와 데이터 레이크하우스의 통합]

[과거: 2-Tier 아키텍처 (데이터 이중 복제 및 ETL 병목)]
다양한 소스 ──> [ Data Lake (S3/HDFS) ] ──(복잡한 ETL 복사)──> [ Data Warehouse ]
                - 저렴하지만 ACID 불가                           - 비싸고 정형 데이터만 가능
                - ML/AI 엔지니어 사용                            - BI/SQL 분석가 사용
                             └─────────────────(데이터 불일치 및 지연 발생)

[현재: Data Lakehouse 단일 아키텍처]
다양한 소스 ──> ┌───────────────────────────────────────────────┐
               │              [ Data Lakehouse ]               │
               │  [ ACID Transaction / Open Table Format ]     │ <─ 트랜잭션 계층 추가
               │  [ Cloud Object Storage (S3, Parquet)   ]     │ <─ 레이크의 저렴한 스토리지
               └───────────────────────┬───────────────────────┘
                                       │ (단일 복사본으로 동시 지원)
                     ┌─────────────────┴─────────────────┐
                 [ ML / AI 파이프라인 ]             [ BI / 실시간 SQL 분석 ]
```
이 도식은 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]가 어떻게 [[001_dikw_pyramid|데이터]]의 불필요한 물리적 이동([[215_etl_vs_elt_pipeline|ETL]])을 근절하는지를 보여줍니다. 기존에는 [[190_ai_llm_requirements_specification|AI]] 엔지니어는 레이크를 보고, 비즈니스 분석가는 DW를 보았기 때문에 동일한 '매출액'에 대해 서로 다른 숫자를 리포팅하는 문제가 빈번했습니다. [[146_lakehouse|레이크하우스]]는 단일 스토리지(S3) 원본 위에 [[012_metadata|메타데이터]] [[191_transaction_concept_states|트랜잭션]] 계층을 올려, 하나의 [[001_dikw_pyramid|데이터]]를 수정(Update)하면 [[190_ai_llm_requirements_specification|AI]] 모델과 BI 대시보드 양쪽에 실시간으로 정합성 있게 반영되는 단일 진실 공급원(SSOT)을 완성합니다.

> 📢 **섹션 비유**: 과거에는 값싼 원자재 창고([[208_data_lake_schema_on_read|데이터 레이크]])에서 물건을 꺼내 비싼 백화점([[209_data_warehouse_schema_on_write|DW]])으로 매일 트럭으로 퍼 나르는 중복 비용이 들었지만, 이제는 창고 자체에 고급 진열장과 POS 결제 시스템([[191_transaction_concept_states|트랜잭션]] 계층)을 달아 창고형 대형 할인매장([[146_lakehouse|레이크하우스]]) 하나로 통합한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]를 가능하게 하는 마법의 핵심은 하드웨어가 아니라, 클라우드 스토리지와 연산 엔진 사이에 끼어들어가는 **[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] ([[196_opentableformat|Open Table Format]])**이라는 논리적 [[012_metadata|메타데이터]] 계층입니다. 대표적으로 **[[147_delta_lake|Delta Lake]] ([[074_photon_engine|Databricks]] 주도)**, **[[148_apache_iceberg|Apache Iceberg]] (Netflix 주도)**, **[[149_apache_hudi|Apache Hudi]] (Uber 주도)**가 있습니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 실무 비유 |
|:---|:---|:---|:---|
| **[[494_object_storage|Object Storage]] Layer** | 무한한 [[001_dikw_pyramid|데이터]]의 물리적 저장 | S3나 GCS에 [[001_dikw_pyramid|데이터]]가 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 등 열(Column) 지향 [[501_file_definition_logical_record|파일]]로 흩어져 보관됨 | 도서관 지하의 방대한 서고 |
| **[[196_opentableformat|Open Table Format]] Layer** | ACID [[191_transaction_concept_states|트랜잭션]] 및 테이블 [[203_metadata_management|메타데이터 관리]] | [[343_json|JSON]]/Avro 형태의 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 유지하여 [[501_file_definition_logical_record|파일]]들의 [[087_process_state_transition|생성]]/수정/삭제 [[022_snapshot_backup_architecture|스냅샷]] 추적 | 서고를 관리하는 사서의 대출/반납 장부 |
| **Compute / Query Engine** | [[136_variance|분산]] SQL [[298_qkv_attention|쿼리]] 및 [[001_dikw_pyramid|데이터]] 처리 | Spark, Presto, Trino 등이 테이블 포맷을 읽어 최적화된 [[501_file_definition_logical_record|파일]]만 타겟팅하여 연산 | 장부를 보고 책을 찾아주는 조수 |
| **Time Travel ([[022_snapshot_backup_architecture|스냅샷]] [[098_rollback_strategy_pipeline_error_threshold|롤백]])** | 과거 특정 시점의 [[001_dikw_pyramid|데이터]] 상태 조회 | [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] 기반으로 덮어써진 과거 [[501_file_definition_logical_record|파일]] 포인터를 유지하여 특정 타임스탬프 [[298_qkv_attention|쿼리]] 가능 | 과거로 돌아가는 타임머신 |
| **[[505_schema|Schema]] Evolution** | 운영 중 다운타임 없는 [[005_schema|스키마]] 변경 | 컬럼 추가/삭제 시 테이블 전체 재작성 없이 [[012_metadata|메타데이터]]만 갱신하여 점진적 [[005_schema|스키마]] 진화 | 건물을 부수지 않고 증축하는 리모델링 |

핵심 원리는 수천만 개의 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]] 덩어리를 RDB의 테이블처럼 다루게 해주는 **[[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[191_transaction_concept_states|Transaction]] Log)**의 제어입니다.

```text
[오픈 테이블 포맷 (예: Apache Iceberg/Delta)의 트랜잭션 원리]

[ SQL: UPDATE users SET status='VIP' WHERE id = 5 ]  ──> (레이크하우스 엔진에 인입)

                       ┌───────── [ Metadata / Transaction Log 계층 ] ─────────┐
                       │ 1. 스냅샷 V1: [File_A.parquet], [File_B.parquet]      │
                       │ 2. 엔진이 ID=5가 포함된 File_A를 메모리로 읽어옴      │
                       │ 3. 상태를 수정한 새로운 [File_A_v2.parquet] 생성      │
                       │ 4. 스냅샷 V2 커밋: [File_A_v2.parquet], [File_B.parquet]│ 
                       └──────────────────────────┬────────────────────────────┘
                                                  │ (포인터 변경 / 기존 파일 유지)
       ┌──────────────────────────────────────────▼──────────────────────────────────┐
       │ [ S3 Object Storage ]                                                       │
       │  (File_A.parquet) <─ 기존 파일은 놔둠 (Time Travel 용도 보존)               │
       │  (File_A_v2.parquet) <─ 신규 파일 기록                                      │
       │  (File_B.parquet)                                                           │
       └─────────────────────────────────────────────────────────────────────────────┘
```
이 흐름도는 객체 스토리지(S3)의 치명적 단점인 '[[501_file_definition_logical_record|파일]] 일부만 수정(In-place Update) 불가' 문제를 [[146_lakehouse|레이크하우스]]가 어떻게 우회하는지를 보여줍니다. [[501_file_definition_logical_record|파일]] 내부의 레코드 하나를 지우기 위해 전체 [[501_file_definition_logical_record|파일]]을 덮어쓰면 읽기-쓰기 충돌([[510_lock|Lock]])이 발생합니다. [[146_lakehouse|레이크하우스]]의 [[012_metadata|메타데이터]] 계층은 변경된 새 [[501_file_definition_logical_record|파일]]을 조용히 옆에 만들고, [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]의 '포인터'만 V1에서 V2로 순간적으로 스위칭(Commit)합니다. 이를 통해 다수의 분석가가 [[298_qkv_attention|쿼리]]를 던지는 중에도 [[001_dikw_pyramid|데이터]]가 끊김 없이 업데이트되는 완벽한 **ACID [[195_isolation_concurrency_control|격리성]]([[195_isolation_concurrency_control|Isolation]])**을 달성합니다.

> 📢 **섹션 비유**: 두꺼운 백과사전(S3 [[501_file_definition_logical_record|파일]])에서 오타 하나를 고치기 위해 책 전체를 다시 인쇄하는 대신, 수정된 [[286_page_frame|페이지]](새 [[501_file_definition_logical_record|파일]])를 복사해서 책갈피([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]])의 위치만 새 [[286_page_frame|페이지]]로 옮겨 꽂아두는 매우 영리한 속임수 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 과거의 플랫폼들과 명확한 스펙 차이를 가지며, 아키텍처 진화의 종착점으로 평가받고 있습니다.

**1. [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]] vs [[208_data_lake_schema_on_read|Data Lake]] vs [[210_data_lakehouse_delta_lake|Data Lakehouse]] 매트릭스**

| 비교 항목 | [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]] ([[209_data_warehouse_schema_on_write|DW]]) | [[208_data_lake_schema_on_read|Data Lake]] | [[210_data_lakehouse_delta_lake|Data Lakehouse]] |
|:---|:---|:---|:---|
| **저장 비용** | 매우 높음 (컴퓨팅 종속) | 매우 낮음 (객체 스토리지) | **매우 낮음** (객체 스토리지 유지) |
| **[[001_dikw_pyramid|데이터]] 타입** | [[002_structured_data|정형 데이터]] 위주 | 정형, 반정형, 비정형 모두 | **모든 [[001_dikw_pyramid|데이터]] 타입 완벽 지원** |
| **ACID [[191_transaction_concept_states|트랜잭션]]** | 강력하게 지원 (Row 레벨) | 미지원 ([[001_dikw_pyramid|데이터]] 수정 불가) | **지원** (Table Format 메타 기반) |
| **SQL [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** | 매우 빠름 (BI 최적화) | 느림 (스토리지 풀스캔 병목) | **빠름** ([[394_catalog_metadata|카탈로그]] 인덱싱 및 [[456_caching|캐싱]] 최적화) |
| **ML / [[190_ai_llm_requirements_specification|AI]] 적합성** | 부적합 (스토리지 접근 제한) | 우수 (원본 탐색 가능) | **최상** (단일 소스로 ML과 BI 동시 활용) |

**2. 융합 관점: 스토리지와 컴퓨팅의 완전한 분리**
[[146_lakehouse|레이크하우스]] 아키텍처의 가장 큰 시너지는 [[531_cloud_native_architecture|클라우드 네이티브]] 환경과의 융합입니다. [[001_dikw_pyramid|데이터]]는 AWS S3에 100TB가 쌓여 있더라도 유지 비용은 월 수백 달러에 불과합니다. 필요할 때만 Snowflake나 [[074_photon_engine|Databricks]] 클러스터(Compute)를 초 단위로 할당받아 [[298_qkv_attention|쿼리]]를 실행하고 즉시 종료할 수 있습니다. 이는 과거 [[209_data_warehouse_schema_on_write|DW]] 장비를 365일 켜두어야 했던 비용 낭비를 극적으로 해결하며, 컴퓨팅 엔진(Spark, Presto, Trino)을 목적에 맞게 갈아 끼울 수 있는 생태계의 유연성을 제공합니다.

> 📢 **섹션 비유**: [[146_lakehouse|레이크하우스]]는 DW의 엄격한 모범생(관리/[[282_performance_tactics|성능]])적 기질과 [[208_data_lake_schema_on_read|데이터 레이크]]의 자유로운 예술가(확장/다양성)적 기질을 하나의 몸에 완벽히 융합해 낸 르네상스형 통합 아키텍처입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]를 도입할 때 가장 치열하게 고민하는 지점은 **어떤 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]](Iceberg, Delta, Hudi)을 표준으로 채택할 것인가**와 스몰 [[501_file_definition_logical_record|파일]] 병목([[269_small_file_problem_data_lakehouse|Small File Problem]])의 방어입니다.

**실무 시나리오: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 3파전 선택 기준**
- **상황**: 기업 내에 스트리밍 [[568_logs_distributed_logging_elk_fluentd|로그]]([[217_cdc_binlog_change_capture_debezium|CDC]])와 대용량 배치 [[001_dikw_pyramid|데이터]]가 혼재되어 있으며, 기존에는 AWS S3와 Spark를 사용 중임. [[146_lakehouse|레이크하우스]] 전환을 위한 기술 [[057_stack|스택]] 선택이 필요함.
- **해결 (아키텍처 [[124_decision_tree|의사결정 트리]])**:

```text
[레이크하우스 테이블 포맷 선택 의사결정 트리]

[도입 목적과 기존 생태계 분석]
         ↓
[Q1. Databricks 환경에 종속되어도 무방하며, 가장 성숙한 상용 성능이 필요한가?]
 ├── (Yes) ──> [ Delta Lake 선택 ]: Spark 최적화 및 벤더 지원(Databricks)이 가장 강력함
 └── (No) ─> [Q2. CDC 실시간 스트리밍 처리와 잦은 Update/Upsert가 주력인가?]
               ├── (Yes) ──> [ Apache Hudi 선택 ]: 레코드 수준의 점진적 업서트(Upsert)에 독보적 강점
               └── (No) ─> [Q3. 엔진에 종속되지 않는 범용성과 완벽한 메타데이터 확장이 중요한가?]
                            └──> [ Apache Iceberg 선택 ]: Snowflake, Trino 등 다양한 엔진과의 완벽한 호환성 (최근 대세)
```
이 의사결정 흐름도는 기술사적 관점에서 특정 벤더에 종속([[362_lock_in_portability|Lock-in]])되지 않는 아키텍처 설계의 중요성을 보여줍니다. 최근 실무에서는 특정 연산 엔진(Spark)에 강하게 묶인 포맷보다, [[012_metadata|메타데이터]] 설계가 가장 깔끔하여 어떤 [[298_qkv_attention|쿼리]] 엔진(Athena, Trino, [[541_cassandra|Snowflake]])이든 자유롭게 붙일 수 있는 **[[148_apache_iceberg|Apache Iceberg]]**가 사실상의 산업 표준(De facto Standard)으로 급부상하고 있습니다.

**운영 및 [[282_performance_tactics|성능]] [[435_checklist_based_testing|체크리스트]]**
1. **Z-Ordering 및 [[347_compaction|Compaction]]**: 계속되는 Update로 S3에 KB 단위의 스몰 [[501_file_definition_logical_record|파일]](Small Files)이 수백만 개 생기면 [[012_metadata|메타데이터]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 읽는 시간 자체가 길어져 [[282_performance_tactics|성능]]이 폭락합니다. 주기적으로 [[501_file_definition_logical_record|파일]]을 [[347_compaction|압축]]([[347_compaction|Compaction]])하고 정렬(Z-Order)하는 최적화 파이프라인(OPTMIZE [[158_instruction|명령어]])이 스케줄링되어 있는가?
2. **Vacuum ([[380_garbage_collection|가비지 컬렉션]])**: Time Travel을 위해 남겨둔 과거 버전의 [[501_file_definition_logical_record|파일]]들이 스토리지 비용을 낭비하지 않도록, 보존 기한(예: 7일)이 지난 구버전 [[501_file_definition_logical_record|파일]]을 물리적으로 삭제(VACUUM)하고 있는가?

> 📢 **섹션 비유**: 훌륭한 장부 시스템([[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]])을 도입했더라도, 책상 위에 찢어진 메모장(스몰 [[501_file_definition_logical_record|파일]])이 너무 많으면 장부를 읽는 데 하루 종일 걸립니다. 주기적으로 메모를 큰 노트에 옮겨 적는 청소([[347_compaction|Compaction]])가 필수적입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 현존하는 [[001_dikw_pyramid|데이터]] 엔지니어링 아키텍처의 최종 진화 형태로 평가받습니다.

| 기대 효과 구분 | 도입 전 ([[178_as_is_to_be_analysis|As-Is]] 2-Tier) | 도입 후 (To-Be [[146_lakehouse|Lakehouse]]) |
|:---|:---|:---|
| **[[052_data_governance_framework|데이터 거버넌스]]** | 레이크와 [[209_data_warehouse_schema_on_write|DW]] 간 지표 불일치로 인한 [[002_silo_hyeonhyung|사일로]] 및 혼란 | 단일 [[001_dikw_pyramid|데이터]] 원본(SSOT) 기반으로 전사 지표의 완벽한 일치 보장 |
| **운영/유지보수 비용** | 레이크 → [[209_data_warehouse_schema_on_write|DW]] 간 끝없는 [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 개발/수정 비용 발생 | 직접 테이블 포맷 위에서 [[298_qkv_attention|쿼리]]하므로 [[215_etl_vs_elt_pipeline|ETL]] 계층 절반 이상 증발 |

**미래 전망 및 결론**
앞으로의 [[001_dikw_pyramid|데이터]] 생태계는 '저장은 개방형 포맷(Iceberg/Delta)을 사용한 객체 스토리지'에 고정해 두고, 그 위에서 연산만 [[541_cassandra|Snowflake]], [[074_photon_engine|Databricks]], [[263_storage_compute_separation_bigquery|BigQuery]] 등 다양한 상용 엔진들이 치열하게 [[282_performance_tactics|성능]] 경쟁을 벌이는 형태로 재편될 것입니다. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 더 이상 특정 벤더의 마케팅 용어가 아니라, 스토리지 독점주의를 깨고 기업에게 [[001_dikw_pyramid|데이터]]의 완전한 소유권을 돌려주는 **개방성(Openness)의 상징**이 되었습니다. [[190_ai_llm_requirements_specification|AI]] 모델 훈련과 실시간 비즈니스 의사결정이 밀리초 단위로 융합되는 현대 기업 환경에서, [[146_lakehouse|레이크하우스]]는 선택이 아닌 생존을 위한 필수 아키텍처로 자리매김하고 있습니다.

> 📢 **섹션 비유**: 과거에는 기찻길(컴퓨팅)과 기차(스토리지)를 세트로만 사야 했다면, [[146_lakehouse|레이크하우스]]는 표준 레일([[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]])을 깔아두어 어떤 회사의 고속열차(Spark, [[541_cassandra|Snowflake]])든 내 짐을 싣고 자유롭게 달릴 수 있게 만든 철도 혁명입니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[148_apache_iceberg|Apache Iceberg]] / [[147_delta_lake|Delta Lake]]** | [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]를 물리적으로 구현하게 해주는 핵심 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]].
- **ACID [[191_transaction_concept_states|Transaction]]** | 여러 [[191_transaction_concept_states|트랜잭션]]이 충돌 없이 [[001_dikw_pyramid|데이터]]를 수정/삭제할 수 있도록 보장하는 [[001_dikw_pyramid|데이터]]베이스의 4대 [[082_attribute_types_er_model|속성]] ([[193_atomicity_all_or_nothing|원자성]], [[194_consistency_database_integrity|일관성]], [[195_isolation_concurrency_control|격리성]], 지속성).
- **Time Travel** | [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 활용하여 과거 특정 시점의 [[001_dikw_pyramid|데이터]] [[022_snapshot_backup_architecture|스냅샷]] 상태로 되돌아가 [[298_qkv_attention|쿼리]]하는 기능.
- **[[347_compaction|Compaction]] ([[378_lsm_compaction_tombstone|콤팩션]])** | 스트리밍 적재로 인해 [[087_process_state_transition|생성]]된 수많은 작은 [[501_file_definition_logical_record|파일]]들을 큰 [[178_parquet_rle_encoding_columnar_compression|파케이]]([[178_parquet_rle_encoding_columnar_compression|Parquet]]) [[501_file_definition_logical_record|파일]]로 병합하여 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]을 높이는 유지보수 작업.
- **Separation of Compute and Storage** | 컴퓨팅 엔진과 저장 스토리지를 물리적으로 분리하여 각각 독립적으로 탄력적 스케일링을 가능하게 하는 [[531_cloud_native_architecture|클라우드 네이티브]]의 핵심 사상.

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 웨어하우스 (DW) — ACID, 고비용 스키마 고정]
    │
    ▼
[데이터 레이크 (Data Lake) — 저비용, 무결성 부재]
    │
    ▼
[오픈 테이블 포맷 (Apache Iceberg / Delta Lake)]
    │
    ▼
[데이터 레이크하우스 (Data Lakehouse) — DW+Lake 통합]
    │
    ▼
[컴퓨팅·스토리지 분리 (Compute-Storage Separation)]
```

[[001_dikw_pyramid|데이터]] 저장 아키텍처가 구조화된 웨어하우스와 비정형 레이크를 거쳐 오픈 포맷 기반의 [[146_lakehouse|레이크하우스]]로 수렴하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 물건을 막 쌓아두는 '먼지 쌓인 창고([[208_data_lake_schema_on_read|데이터 레이크]])'와 깨끗하게 진열된 '비싼 백화점([[209_data_warehouse_schema_on_write|데이터 웨어하우스]])'을 따로 써서 물건을 옮기느라 너무 힘들었어요.
2. 그래서 똑똑한 엔지니어들이 창고 문 앞에 '마법의 장부([[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]])'를 하나 만들었어요.
3. 이제는 창고 안의 물건을 직접 찾을 필요 없이 마법의 장부만 보면 백화점처럼 쉽고 빠르게 물건을 찾아 쓸 수 있게 되었는데, 이것이 바로 '[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]'랍니다!