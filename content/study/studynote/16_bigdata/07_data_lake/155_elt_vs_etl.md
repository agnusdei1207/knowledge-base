---
title: 155. ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. [[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load)은 변환 후 적재하는 전통 방식으로 스토리지 비용이 비쌌던 [[061_on_premise_legacy_infrastructure|온프레미스]] [[209_data_warehouse_schema_on_write|DW]] 환경에 최적화되었으나, 클라우드 시대에는 **먼저 적재하고 나중에 변환하는 [[034_elt|ELT]] (Extract, Load, Transform)**가 표준으로 전환되었다.
2. dbt ([[001_dikw_pyramid|data]] build tool)는 [[034_elt|ELT]] 패러다임의 핵심 도구로, [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]·[[146_lakehouse|레이크하우스]] 내부에서 SQL로 선언적 변환을 수행하며 테스트·문서화·리니지를 자동 관리한다.
3. ELT는 **원시 [[001_dikw_pyramid|데이터]]([[225_raw|Raw]]) 보존**, **반복적 변환 가능**, **타임 트래블 기반 소급 재처리**를 가능하게 하여 [[645_data_pipeline_acceleration|데이터 파이프라인]]의 유연성과 [[606_auditing_linux_auditd|감사]] 추적성을 극대화한다.

---

## Ⅰ. 개요 및 필요성

1990~2010년대 [[061_on_premise_legacy_infrastructure|온프레미스]] [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[188_pl_sql_t_sql_procedural|Oracle]], Teradata) 환경에서는 스토리지가 고가였고 컴퓨팅 자원도 제한적이었다. ETL은 이 제약 안에서 필요한 [[001_dikw_pyramid|데이터]]만 정제·[[347_compaction|압축]]하여 DW에 적재하는 최적 방식이었다.

클라우드 시대(2010년 이후)에는 S3/ADLS 스토리지 비용이 [[061_on_premise_legacy_infrastructure|온프레미스]] 대비 [[489_raid_10_hybrid|10]]~100분의 1 수준으로 하락하고, Spark/[[263_storage_compute_separation_bigquery|BigQuery]]/Snowflake의 [[136_variance|분산]] 컴퓨팅이 변환 비용을 [[093_normalization|정규화]]했다. 이 변화가 [[034_elt|ELT]] 패러다임으로의 전환을 이끌었다.

| 비교 항목 | [[215_etl_vs_elt_pipeline|ETL]] | [[034_elt|ELT]] |
|:---|:---|:---|
| 변환 위치 | 스테이징 서버 (외부) | [[209_data_warehouse_schema_on_write|DW]]/[[146_lakehouse|레이크하우스]] 내부 |
| 원시 [[001_dikw_pyramid|데이터]] 보존 | 없음 (변환 후 버림) | 있음 ([[225_raw|Raw]] 계층 보존) |
| 스토리지 사용 | 최소화 (정제 후 적재) | 최대 ([[225_raw|Raw]] + 변환 결과) |
| 재처리 유연성 | 낮음 (원본 없음) | 높음 (Raw에서 재변환) |
| 적합 환경 | [[061_on_premise_legacy_infrastructure|온프레미스]] [[209_data_warehouse_schema_on_write|DW]] | 클라우드 [[209_data_warehouse_schema_on_write|DW]] / [[146_lakehouse|레이크하우스]] |
| 대표 도구 | Informatica, SSIS, Talend | dbt, [[056_spark_sql|Spark SQL]], Dataflow |

> 📢 **섹션 요약 비유**: ETL은 식재료를 요리해서만 냉장고에 넣는 방식이고, ELT는 식재료를 그대로 냉장고에 넣고 필요할 때 꺼내서 요리하는 방식이다. 냉장고(스토리지)가 저렴해지면서 후자가 유리해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌────────────────────────────────────────────────────────────────┐
│                   ETL vs ELT 비교                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  【ETL 흐름】                                                   │
│                                                                │
│  [소스] ──Extract──▶ [스테이징 서버]                            │
│                      Transform (정제·집계)                      │
│                           │                                    │
│                           └──Load──▶ [DW] ──▶ [BI 도구]        │
│                                                                │
│  【ELT 흐름】                                                   │
│                                                                │
│  [소스] ──Extract──▶ [레이크하우스 / 클라우드 DW]               │
│                      (Bronze: Raw 적재)                         │
│                           │                                    │
│                    Transform (dbt / Spark SQL)                  │
│                    Silver: 정제  Gold: 집계                     │
│                           │                                    │
│                           └──▶ [BI / ML 도구]                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**dbt ([[001_dikw_pyramid|data]] build tool) 핵심 기능**

| 기능 | 설명 | 장점 |
|:---|:---|:---|
| Model | SQL SELECT로 변환 정의 | 선언적, 재사용 가능 |
| Test | `not_null`, `unique`, `accepted_values` | 변환 결과 자동 품질 검사 |
| [[378_software_documentation|Documentation]] | `description` 필드로 컬럼 문서화 | 자동 [[213_data_catalog_metadata|데이터 카탈로그]] [[087_process_state_transition|생성]] |
| Lineage [[104_graph|Graph]] | 모델 간 의존성 자동 [[003_bigdata_7v|시각화]] | 영향 분석 즉시 파악 |
| Materialization | Table / [[151_sql_view_virtual_table|View]] / Incremental / Ephemeral | [[282_performance_tactics|성능]]·비용 트레이드오프 선택 |
| Seed | CSV로 정적 [[316_reference_pattern_nosql|참조]] [[001_dikw_pyramid|데이터]] 관리 | 코드와 [[001_dikw_pyramid|데이터]] 함께 [[288_version_ihl_tos_total_length|버전]] 관리 |

**dbt Incremental 모델 패턴**
```text
-- models/silver/orders_cleaned.sql
-- dbt Jinja 매크로 사용
-- { { config(materialized='incremental',
--           unique_key='order_id',
--           on_schema_change='sync_all_columns') } }

SELECT
    order_id,
    customer_id,
    amount,
    created_at
FROM source('bronze', 'orders_raw')
WHERE status != 'cancelled'
-- incremental 조건: 마지막 실행 이후 데이터만 처리
-- AND created_at > (SELECT MAX(created_at) FROM this_model)
```

> 📢 **섹션 요약 비유**: dbt는 요리 레시피 북이다. 각 요리(모델)의 재료(소스)와 조리법(SQL)이 정해져 있고, 완성된 요리(결과 테이블)가 예상대로 나왔는지 검사(test)하는 과정도 포함된다.

---

## Ⅲ. 비교 및 연결

**[[034_elt|ELT]] 도구 비교**

| 도구 | 실행 위치 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| dbt Core | [[209_data_warehouse_schema_on_write|DW]]/[[146_lakehouse|레이크하우스]] 내부 | [[191_oss_license_compliance|오픈소스]], SQL 선언적 | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], [[074_photon_engine|Databricks]] |
| dbt Cloud | 관리형 [[309_saas|SaaS]] | IDE + [[079_kube_scheduler_pod_placement|스케줄러]] + 협업 | 팀 규모 조직 |
| [[056_spark_sql|Spark SQL]] | [[146_lakehouse|레이크하우스]] | Python/Scala 병행 | 대규모 배치 변환 |
| Dataflow | GCP 관리형 | Apache Beam 기반 | GCP 생태계 |
| Glue | AWS 관리형 | Spark 기반, S3 통합 | AWS 생태계 |

**연관 개념 연결**

- **[[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]]**: ELT의 Bronze→Silver→Gold가 Medallion 계층과 완벽히 매핑
- **[[154_data_product|Data Product]]**: dbt 모델이 Gold 계층 [[154_data_product|데이터 제품]]의 변환 로직을 담당
- **[[214_data_lineage_tracking|Data Lineage]]**: dbt가 자동으로 리니지 [[070_graph_datastructure|그래프]]를 [[087_process_state_transition|생성]]하여 Unity Catalog와 연계

> 📢 **섹션 요약 비유**: ETL은 택배 물건을 포장해서 배송하는 방식이고, ELT는 원재료를 창고에 다 넣어두고 주문이 오면 그때 포장하는 방식이다. 창고(스토리지) 비용이 싸지면서 후자가 더 효율적이 됐다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[034_elt|ELT]] 전환 [[435_checklist_based_testing|체크리스트]]**
- [ ] 원시 [[001_dikw_pyramid|데이터]]를 Bronze 계층에 보존하는 [[123_pipe|파이프]]라인 설계
- [ ] dbt 프로젝트 [[459_quic_fec_forward_error_correction|초기]]화 및 소스 등록 (`dbt source freshness` [[009_config|설정]])
- [ ] Silver 모델: `materialized='incremental'` + `unique_key` [[009_config|설정]]
- [ ] Gold 모델: `materialized='table'` + [[514_partition_slice_volume|파티션]] [[009_config|설정]]
- [ ] `dbt test` 실행 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 통합

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| [[215_etl_vs_elt_pipeline|ETL]] → [[034_elt|ELT]] 전환 이유 | 클라우드 스토리지 저비용화, [[136_variance|분산]] 컴퓨팅 확장성 |
| dbt의 역할 | [[209_data_warehouse_schema_on_write|DW]] 내부 SQL 선언적 변환 + 테스트 + 리니지 자동화 |
| Incremental 모델 장점 | 전체 재처리 없이 새 [[001_dikw_pyramid|데이터]]만 변환 → 비용·시간 절감 |
| [[034_elt|ELT]] 한계 | 원시 [[001_dikw_pyramid|데이터]] 보존으로 스토리지 비용 증가, 민감 [[001_dikw_pyramid|데이터]] 보안 관리 필요 |

> 📢 **섹션 요약 비유**: [[034_elt|ELT]] 도입은 즉석 조리 냉장고를 도입하는 것이다. 모든 식재료를 신선하게 보관하고(Bronze), 필요할 때 빠르게 조리(dbt 변환)하여 서빙(Gold)한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 재처리 유연성 | [[225_raw|Raw]] 보존으로 언제든 새 로직으로 소급 재처리 가능 |
| 운영 단순화 | 스테이징 서버 제거, [[209_data_warehouse_schema_on_write|DW]] 내부에서 모든 변환 처리 |
| 품질 가시성 | dbt test로 변환 결과 품질 자동 [[395_verification_process_review|검증]] |
| 협업 향상 | dbt 모델 = SQL 코드 → Git [[288_version_ihl_tos_total_length|버전]] 관리 + [[330_code_review|코드 리뷰]] |

ETL에서 ELT로의 패러다임 전환은 클라우드 빅데이터 인프라 확산과 함께 이미 완료된 흐름이다. dbt는 현재 [[001_dikw_pyramid|데이터]] 팀 표준 도구로 자리 잡았으며, [[074_photon_engine|Databricks]]·[[541_cassandra|Snowflake]]·[[263_storage_compute_separation_bigquery|BigQuery]] 모두 네이티브 dbt 통합을 지원한다. 기술사 시험에서는 **[[317_etl_vs_elt|ETL vs ELT]] 전환 이유**, **dbt 핵심 기능**, **Incremental 모델 동작 원리**가 핵심 논점이다.

> 📢 **섹션 요약 비유**: [[034_elt|ELT]] 시대는 사진 현상 방식의 변화와 같다. 필름 사진([[215_etl_vs_elt_pipeline|ETL]])은 찍자마자 현상해야 했지만, 디지털 사진([[034_elt|ELT]])은 [[225_raw|RAW]] [[501_file_definition_logical_record|파일]]로 보관하고 필요할 때 다양한 방식으로 편집할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| dbt | [[034_elt|ELT]] 핵심 도구 | SQL 선언적 변환·테스트·리니지 |
| Incremental 모델 | dbt [[282_performance_tactics|성능]] 최적화 | 신규 [[001_dikw_pyramid|데이터]]만 처리 패턴 |
| Bronze 계층 | [[034_elt|ELT]] 전제 조건 | [[225_raw|Raw]] [[001_dikw_pyramid|데이터]] 영구 보존 |
| [[214_data_lineage_tracking|Data Lineage]] | 자동화 산출물 | dbt가 [[087_process_state_transition|생성]]하는 모델 의존성 [[070_graph_datastructure|그래프]] |
| [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]] | 연관 패턴 | [[034_elt|ELT]] 흐름 = Bronze→Silver→Gold |
| [[009_schema_on_read|Schema-on-Read]] | [[034_elt|ELT]] 특성 | 적재 시 [[005_schema|스키마]] 강제 않음 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[ETL (Extract-Transform-Load) — 소스에서 추출 후 변환, 타겟 DW에 적재]
    │
    ▼
[데이터 웨어하우스 (DW) — 정제된 구조적 데이터 중앙 저장소, ETL 전제]
    │
    ▼
[ELT (Extract-Load-Transform) — 원시 데이터 먼저 적재, 클라우드 DW에서 변환]
    │
    ▼
[데이터 레이크 (Data Lake) — 원시 데이터 무제한 적재, ELT 패러다임과 친화적]
    │
    ▼
[레이크하우스 (Lakehouse) — Delta Lake·Iceberg 기반 ELT + ACID 트랜잭션 통합]
```

이 흐름은 [[061_on_premise_legacy_infrastructure|온프레미스]] DW를 위한 [[215_etl_vs_elt_pipeline|ETL]] 패러다임이 클라우드 규모에서 ELT로 전환되고, [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 아키텍처로 통합·발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. ETL은 재료를 사오자마자 다 손질해서 냉장고에 넣는 방식이고, ELT는 재료 그대로 일단 냉장고에 넣고 필요할 때 꺼내서 손질하는 방식이에요.
2. 냉장고(저장공간)가 저렴해지면서 미리 다 손질하지 않아도 되니 [[034_elt|ELT]] 방식이 더 편리해졌어요.
3. dbt는 냉장고 안 재료를 어떻게 요리할지 레시피 북이에요. 레시피(SQL)를 코드로 기록해두면 언제나 같은 요리가 나와요.
