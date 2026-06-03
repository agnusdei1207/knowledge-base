---
title: 227. ELT (Extract, Load, Transform)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[034_elt|ELT]](Extract, Load, Transform)는 원시 [[001_dikw_pyramid|데이터]]를 먼저 클라우드 [[209_data_warehouse_schema_on_write|DW]]/레이크에 고속 적재(L)한 후, [[209_data_warehouse_schema_on_write|DW]] 내부의 강력한 MPP 컴퓨팅으로 [[001_dikw_pyramid|데이터]]를 변환(T)하는 **[[531_cloud_native_architecture|클라우드 네이티브]] [[001_dikw_pyramid|데이터]] 통합 방식**이다.
> 2. **가치**: ETL의 변환 서버 병목을 제거하고, 원시 [[001_dikw_pyramid|데이터]]를 보존하여 **나중에 다른 관점으로 재분석**할 수 있으며, 클라우드 DW의 수평 확장으로 빅데이터 규모에 탄력적 대응이 가능하다.
> 3. **판단 포인트**: dbt([[001_dikw_pyramid|data]] build tool)가 [[034_elt|ELT]] 패러다임의 Transform 단계를 SQL 기반으로 표준화한 핵심 도구이며, **[[541_cassandra|Snowflake]]·[[263_storage_compute_separation_bigquery|BigQuery]]·Redshift + dbt** 조합이 현대 클라우드 [[001_dikw_pyramid|데이터]] 스택의 표준이다.

---

## Ⅰ. 개요 및 필요성

[[215_etl_vs_elt_pipeline|ETL]] 시대의 가장 큰 병목은 "변환 서버"였다. 아무리 빠르게 추출해도 중간 서버 성능이 한계였다. 클라우드 [[209_data_warehouse_schema_on_write|DW]]([[263_storage_compute_separation_bigquery|BigQuery]]·[[541_cassandra|Snowflake]]·Redshift)가 MPP(Massively Parallel Processing)로 수백 노드를 [[430_index_fast_full_scan|병렬]] 동원할 수 있게 되자, **"왜 비싼 전용 서버에서 변환하지? [[209_data_warehouse_schema_on_write|DW]] 내부에서 하면 훨씬 빠르잖아"**라는 인식이 생겼다.

```
[ETL 한계]
소스 → 추출 → [변환 서버 병목] → DW 적재
                    ↑ 이 병목이 ETL 전체 속도 결정

[ELT 개선]
소스 → 추출 → [DW에 원시 적재] → [DW 내부 MPP 변환]
                                       ↑ DW 수평 확장으로 병목 해소
```

ELT가 특히 효과적인 이유:
- 클라우드 DW는 스토리지-컴퓨팅 분리로 변환 시 컴퓨팅만 확장 가능
- 원시 [[001_dikw_pyramid|데이터]] 보존으로 재분석·재처리 가능
- [[001_dikw_pyramid|데이터]] 엔지니어가 SQL만으로 변환 로직 작성 가능 (dbt)

📢 **섹션 요약 비유**: ELT는 식재료(원시 [[001_dikw_pyramid|데이터]])를 먼저 대형 주방([[209_data_warehouse_schema_on_write|DW]])으로 가져온 뒤, 수십 명의 요리사(MPP 노드)가 동시에 손질하는 방식이다. 작은 주방([[215_etl_vs_elt_pipeline|ETL]] 서버) 한 곳에서 모든 걸 처리하는 ETL보다 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[034_elt|ELT]] 파이프라인 아키텍처

```
┌────────────────────────────────────────────────────────────┐
│                     ELT 파이프라인                          │
│                                                            │
│  소스 시스템   ─── Extract ───▶  Raw/Staging Schema        │
│  (SaaS API,        (Fivetran,     (원시 테이블 그대로)       │
│   CDC,             Airbyte,                                │
│   플랫파일)         Custom)                                 │
│                                 ↓ dbt Transform            │
│                              Marts Schema                  │
│                              (비즈니스 도메인 모델)           │
│                                 ↓                         │
│                              BI 도구 / ML 플랫폼             │
└────────────────────────────────────────────────────────────┘
```

### dbt([[001_dikw_pyramid|data]] build tool) 역할

```
[dbt 핵심 기능]
┌──────────────────────────────────────────────────┐
│              dbt (데이터 변환 프레임워크)             │
│                                                  │
│  .sql 파일  ──▶  SELECT * FROM raw_orders        │
│               WHERE created_at > '2024-01-01'   │
│               → 자동으로 DW 내 VIEW/TABLE 생성   │
│                                                  │
│  기능:                                            │
│  ① SQL 기반 변환 로직 버전 관리 (Git)              │
│  ② 데이터 테스트 (NOT NULL, UNIQUE, 참조 무결성)  │
│  ③ 의존성 자동 해결 (DAG 생성)                    │
│  ④ 문서 자동 생성 (컬럼 설명, 계보)               │
│  ⑤ CI/CD 파이프라인 통합                          │
└──────────────────────────────────────────────────┘
```

### [[178_modern_data_stack|Modern Data Stack]] 구성

| 계층 | 역할 | 주요 도구 |
|:---|:---|:---|
| **Extract & Load** | 소스 → [[209_data_warehouse_schema_on_write|DW]] 원시 적재 | Fivetran, Airbyte, Stitch |
| **Storage** | 클라우드 [[209_data_warehouse_schema_on_write|DW]] | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift |
| **Transform** | [[209_data_warehouse_schema_on_write|DW]] 내 SQL 변환 | dbt, Dataform |
| **[[073_container_orchestration_tools|Orchestration]]** | 파이프라인 스케줄링 | Airflow, Prefect, Dagster |
| **BI & Analytics** | [[003_bigdata_7v|시각화]]·분석 | [[164_tableau|Tableau]], [[166_looker|Looker]], Metabase |
| **[[278_reverse_etl_operational_analytics|Reverse ETL]]** | [[209_data_warehouse_schema_on_write|DW]] → [[309_saas|SaaS]] 도구 역방향 | Census, Hightouch |

📢 **섹션 요약 비유**: dbt는 SQL로 된 레시피 북이다. 어떤 재료(원시 테이블)를 어떻게 조합([[521_join|JOIN]]·집계)해 어떤 요리(비즈니스 테이블)를 만드는지 Git으로 관리되는 레시피북이며, 매번 같은 맛을 보장하는 자동화 주방이다.

---

## Ⅲ. 비교 및 연결

### [[317_etl_vs_elt|ETL vs ELT]] 심층 비교

| 비교 항목 | [[215_etl_vs_elt_pipeline|ETL]] | [[034_elt|ELT]] |
|:---|:---|:---|
| **변환 주체** | 전용 [[215_etl_vs_elt_pipeline|ETL]] 서버 | 클라우드 [[209_data_warehouse_schema_on_write|DW]]/레이크 |
| **원시 [[001_dikw_pyramid|데이터]] 보존** | 미보존 (변환 후 적재) | 보존 (원시 테이블 유지) |
| **빅데이터 확장성** | 제한적 | 탁월 ([[209_data_warehouse_schema_on_write|DW]] MPP 활용) |
| **변환 도구** | Informatica, DataStage | dbt, SQL, Spark |
| **[[001_dikw_pyramid|데이터]] 이동량** | 적음 (정제 후 이동) | 많음 (원시 그대로 이동) |
| **[[209_data_warehouse_schema_on_write|DW]] 저장 비용** | 낮음 | 높음 (원시+정제 중복) |
| **[[005_schema|스키마]] 유연성** | 낮음 | 높음 (원시 보존) |
| **기술 요건** | [[215_etl_vs_elt_pipeline|ETL]] 전문가 | SQL 능숙 [[001_dikw_pyramid|데이터]] 엔지니어 |
| **적합 환경** | [[061_on_premise_legacy_infrastructure|온프레미스]], 레거시 | 클라우드 [[209_data_warehouse_schema_on_write|DW]], 스타트업 |

### [[278_reverse_etl_operational_analytics|Reverse ETL]] (역방향 [[215_etl_vs_elt_pipeline|ETL]])

ELT의 발전으로 등장한 개념으로, DW에서 분석·변환된 [[001_dikw_pyramid|데이터]]를 **운영 [[309_saas|SaaS]] 도구([[107_crm_customer_relationship_management|CRM]]·이메일·광고 플랫폼)로 역방향 [[212_synchronization_mechanisms|동기화]]**한다.

```
[Reverse ETL 흐름]
DW (Gold 테이블) ──▶ Census/Hightouch ──▶ Salesforce CRM
                                       ──▶ Marketo (이메일)
                                       ──▶ Google Ads
"분석 결과를 곧바로 마케팅 실행에 활용"
```

📢 **섹션 요약 비유**: Reverse ETL은 주방에서 완성된 요리(분석 결과)를 배달 앱([[107_crm_customer_relationship_management|CRM]]·광고 플랫폼)으로 바로 전송하는 것이다. 창고([[209_data_warehouse_schema_on_write|DW]])에만 보관하지 않고, 요리를 손님(비즈니스 팀)에게 실시간으로 서빙한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### dbt 변환 모델 예시

```text
-- models/marts/sales/fact_daily_sales.sql
-- dbt Jinja: config(materialized='table')

WITH orders AS (
    SELECT * FROM stg_orders     -- ref('stg_orders')
    WHERE status = 'completed'
),
products AS (
    SELECT * FROM stg_products   -- ref('stg_products')
),
final AS (
    SELECT
        o.order_date,
        p.category,
        p.brand,
        SUM(o.amount)    AS total_sales,
        COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY 1, 2, 3
)

SELECT * FROM final
```

```yaml
# models/marts/sales/schema.yml
models:
  - name: fact_daily_sales
    description: "일별 카테고리별 매출 집계"
    columns:
      - name: total_sales
        tests:
          - not_null
      - name: order_count
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

### 실무 도입 단계

```
1단계: Extract & Load 자동화
       Fivetran으로 SaaS 소스 → Snowflake Raw 스키마 자동 적재

2단계: dbt 변환 계층 구성
       Staging → Intermediate → Marts 3단계 모델 구조

3단계: 테스트 및 문서화
       dbt test + dbt docs generate → 데이터 품질 자동 검증

4단계: 오케스트레이션
       Airflow DAG 또는 dbt Cloud 스케줄러로 일일 배치

5단계: Reverse ETL (선택)
       Census로 Snowflake Gold → Salesforce 고객 세그먼트 동기화
```

📢 **섹션 요약 비유**: Modern [[001_dikw_pyramid|Data]] Stack은 레고 블록 세트다. Fivetran(Extract+Load), [[541_cassandra|Snowflake]](Storage), dbt(Transform), Airflow([[073_container_orchestration_tools|Orchestration]]), [[164_tableau|Tableau]](BI)라는 각각의 블록을 조립하여 [[001_dikw_pyramid|데이터]] 파이프라인을 완성한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **처리 속도 향상** | [[215_etl_vs_elt_pipeline|ETL]] 변환 서버 병목 제거, [[209_data_warehouse_schema_on_write|DW]] MPP로 수~수십 배 속도 |
| **원시 [[001_dikw_pyramid|데이터]] 보존** | 재분석·새로운 비즈니스 요건 발생 시 재처리 가능 |
| **민첩성** | SQL 기반 dbt로 변환 로직 빠른 수정 및 배포 |
| **비용 최적화** | [[215_etl_vs_elt_pipeline|ETL]] 전용 서버 제거, 클라우드 [[209_data_warehouse_schema_on_write|DW]] 컴퓨팅 온디맨드 |
| **[[001_dikw_pyramid|데이터]] 계보** | dbt 의존성 DAG로 소스~타겟 전체 계보 자동 문서화 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **[[209_data_warehouse_schema_on_write|DW]] 비용 증가** | 원시 [[001_dikw_pyramid|데이터]] 보존으로 스토리지 및 컴퓨팅 비용 ↑ |
| **[[052_data_governance_framework|데이터 거버넌스]]** | [[209_data_warehouse_schema_on_write|DW]] 내 원시 테이블 과잉 → 정리 [[164_policy|정책]] 필요 |
| **SQL 의존성** | 복잡한 ML [[247_feature_label_variables|피처]], 비정형 처리는 Python/Spark 병행 필요 |
| **실시간 한계** | 기본적으로 배치 지향, 실시간 처리는 스트리밍 파이프라인 별도 |

📢 **섹션 요약 비유**: ELT는 큰 창고([[209_data_warehouse_schema_on_write|DW]])에 재료를 다 쌓아두고 요리하는 방식이다. 창고 공간([[209_data_warehouse_schema_on_write|DW]] 비용)은 더 필요하지만, 언제든 다른 레시피(분석 관점)로 요리할 수 있고, 주방([[209_data_warehouse_schema_on_write|DW]] MPP)이 크니 한꺼번에 많은 양을 빠르게 처리할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[215_etl_vs_elt_pipeline|ETL]] | ELT의 전신, 변환 위치(외부 서버)가 핵심 차이 |
| dbt ([[001_dikw_pyramid|data]] build tool) | [[034_elt|ELT]] Transform 단계의 표준 SQL 변환 프레임워크 |
| 클라우드 [[209_data_warehouse_schema_on_write|DW]] | [[034_elt|ELT]] 변환 엔진 역할 담당 ([[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]]) |
| Fivetran/Airbyte | ELT의 Extract+Load 자동화 도구 |
| [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | [[034_elt|ELT]] 파이프라인 스케줄링·[[073_container_orchestration_tools|오케스트레이션]] |
| [[278_reverse_etl_operational_analytics|Reverse ETL]] | [[209_data_warehouse_schema_on_write|DW]] → 운영 [[309_saas|SaaS]] 역방향 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]] |
| [[009_schema_on_read|Schema-on-Read]] | ELT에서 원시 적재 후 변환하는 철학과 연결 |

### 👶 어린이를 위한 3줄 비유 설명
1. ELT는 장난감([[001_dikw_pyramid|데이터]])을 일단 큰 방([[209_data_warehouse_schema_on_write|DW]])에 다 가져온 뒤, 방 안에서 여러 명이 함께 정리하는 것이다. 한 명([[215_etl_vs_elt_pipeline|ETL]] 서버)이 바깥에서 다 정리하고 들어오는 것보다 훨씬 빠르다.

### 📈 관련 키워드 및 발전 흐름도

```text
ETL: 외부 서버에서 변환 (병목)
    │
    ▼
ELT: DW/Lake 내부에서 변환 (BigQuery · Snowflake MPP)
    ├─► dbt: SQL 기반 변환 오케스트레이션
    └─► Materialized View · CTAS
    │
    ▼
Reverse ETL: DW → SaaS 도구로 데이터 역전달
```
2. dbt는 "이 장난감들을 이렇게 분류해라"라는 정리 규칙서(SQL [[501_file_definition_logical_record|파일]])다. 규칙서를 고치면 다음번에 자동으로 새로운 방식으로 정리된다.
3. 원시 [[001_dikw_pyramid|데이터]]를 보존하는 것은 장난감 설명서를 버리지 않는 것과 같다. 나중에 다른 방법으로 조립(재분석)하고 싶을 때 다시 꺼내볼 수 있다.
