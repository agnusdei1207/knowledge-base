---
title: 208. 데이터 웨어하우스 (Data Warehouse) 스키마 온 라이트 Inmon 설계
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[001_dikw_pyramid|Data]] Warehouse)는 여러 운영 시스템의 [[001_dikw_pyramid|데이터]]를 주제 지향적(Subject-Oriented)으로 통합·정제하여 의사결정 지원에 최적화된 분석용 [[001_dikw_pyramid|데이터]]베이스다.
> 2. **가치**: [[010_schema_on_write|스키마 온 라이트]]([[010_schema_on_write|Schema-on-Write]]) 방식으로 [[001_dikw_pyramid|데이터]] 적재 전 품질을 보장하여, 경영진이 일관된 단일 진실 공급원(Single Source of Truth)을 기반으로 의사결정할 수 있도록 한다.
> 3. **판단 포인트**: [[311_inmon|Inmon]] 방법론([[402_top_down_integration|Top-Down]], [[093_normalization|정규화]] 중심)과 [[312_kimball|Kimball]] 방법론([[403_bottom_up_integration|Bottom-Up]], [[118_dimensional_modeling_star_schema|차원 모델링]] 중심)의 트레이드오프를 명확히 이해하고, 기업 규모·분석 요건에 따라 선택 근거를 논술할 것.

---

## Ⅰ. 개요 및 필요성

### [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] 정의

빌 인몬(Bill [[311_inmon|Inmon]])이 1990년대 정의한 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]의 4대 특성:

- **주제 지향(Subject-Oriented)**: 판매, 고객, 제품 등 비즈니스 주제별로 구성
- **통합(Integrated)**: 이기종 소스 시스템의 [[001_dikw_pyramid|데이터]]를 일관된 형식으로 통합
- **시간 변형(Time-Variant)**: 시간 흐름에 따른 변화를 보존하여 이력 분석 지원
- **비휘발성(Non-Volatile)**: 적재된 [[001_dikw_pyramid|데이터]]는 수정·삭제되지 않고 분석 용도로만 읽힘

### 운영 DB vs [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]

| 항목 | 운영 DB ([[327_hint_handoff|OLTP]]) | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[316_olap|OLAP]]) |
|:---|:---|:---|
| **목적** | [[191_transaction_concept_states|트랜잭션]] 처리 | 분석·의사결정 지원 |
| **[[298_qkv_attention|쿼리]] 유형** | 단순 읽기/[[289_cqrs_db|쓰기]] | 복잡한 집계 [[298_qkv_attention|쿼리]] |
| **[[001_dikw_pyramid|데이터]] 범위** | 현재 [[001_dikw_pyramid|데이터]] | 수년간 이력 [[001_dikw_pyramid|데이터]] |
| **[[005_schema|스키마]] 설계** | [[093_normalization|정규화]]([[105_third_normal_form_3nf_transitive|3NF]]) | 비정규화(스타/스노우플레이크) |
| **갱신 주기** | 실시간 | 배치(일/주/월) |
| **사용자 수** | 수천~수만 명 | 수십~수백 명 |

📢 **섹션 요약 비유**: 운영 DB는 **편의점 계산대**(빠른 처리), [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 **경영진의 통계 보고서실**(느리지만 깊은 통찰)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Inmon의 CIF (Corporate Information Factory) 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│              Inmon CIF (기업 정보 팩토리)                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 운영 DB  │  │ ERP 시스 │  │ 외부 데이 │              │
│  │ (OLTP)   │  │ 템(SAP)  │  │ 터 소스   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       └─────────────┴─────────────┘                     │
│                          │                               │
│              ┌───────────▼───────────┐                  │
│              │   ETL 계층            │                  │
│              │  (추출→변환→적재)      │                  │
│              └───────────┬───────────┘                  │
│                          │                               │
│              ┌───────────▼───────────┐                  │
│              │   ODS (Operational    │                  │
│              │   Data Store)         │                  │
│              │   실시간 통합 뷰       │                  │
│              └───────────┬───────────┘                  │
│                          │                               │
│              ┌───────────▼───────────┐                  │
│              │   EDW (Enterprise     │                  │
│              │   Data Warehouse)     │                  │
│              │   3NF 정규화 통합 저장 │                  │
│              └───────────┬───────────┘                  │
│                          │                               │
│         ┌────────────────┼────────────────┐             │
│         │                │                │             │
│  ┌──────▼──┐     ┌───────▼───────┐ ┌─────▼────┐       │
│  │영업 마트 │     │ 재무 마트      │ │인사 마트  │       │
│  │(Sales   │     │(Finance Mart) │ │(HR Mart) │       │
│  │Mart)    │     │               │ │          │       │
│  └─────────┘     └───────────────┘ └──────────┘       │
└──────────────────────────────────────────────────────────┘
```

### [[010_schema_on_write|Schema-on-Write]] ([[010_schema_on_write|스키마 온 라이트]]) 메커니즘

[[209_data_warehouse_schema_on_write|데이터 웨어하우스]]의 핵심 특성: **[[001_dikw_pyramid|데이터]] 적재 전 [[005_schema|스키마]] 확정**

```
소스 데이터 → [ETL 변환] → [스키마 검증] → [DW 적재]
              ↑                ↑
          타입 변환         NULL 검사
          코드 매핑         참조 무결성
          중복 제거         비즈니스 규칙
```

📢 **섹션 요약 비유**: [[010_schema_on_write|스키마 온 라이트]]는 **도서관에 책이 들어올 때 즉시 [[104_classification_analysis|분류]]·라벨링하는 것**이다. 찾기는 쉽지만 입고 작업이 오래 걸린다.

---

## Ⅲ. 비교 및 연결

### [[311_inmon|Inmon]] vs [[312_kimball|Kimball]] 방법론 비교

| 항목 | [[311_inmon|Inmon]] ([[402_top_down_integration|Top-Down]]) | [[312_kimball|Kimball]] ([[403_bottom_up_integration|Bottom-Up]]) |
|:---|:---|:---|
| **접근 방식** | 전사 EDW 우선 구축 | [[209_data_mart_kimball_star_schema|데이터 마트]] 우선 구축 |
| **[[005_schema|스키마]]** | [[105_third_normal_form_3nf_transitive|3NF]] [[093_normalization|정규화]] | 비정규화([[334_star_schema|스타 스키마]]) |
| **구현 난이도** | 높음(장기 프로젝트) | 낮음(빠른 성과) |
| **유지보수** | 쉬움(중복 없음) | 어려움(마트 간 [[194_consistency_database_integrity|일관성]]) |
| **[[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** | 조인 증가로 느릴 수 있음 | 빠름(비정규화) |
| **적합 기업** | 대기업(전사 [[194_consistency_database_integrity|일관성]] 중요) | 중소기업(빠른 [[012_roi_return_on_investment|ROI]] 필요) |

### [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] 연결 개념

- **[[291_ods|ODS]] ([[264_ods_operational_data_store_realtime|Operational Data Store]])**: 실시간에 가까운 통합 운영 뷰 (DW와 구별됨)
- **[[317_etl_vs_elt|ETL vs ELT]]**: DW는 전통적으로 [[215_etl_vs_elt_pipeline|ETL]], 클라우드 DW는 ELT로 전환
- **[[209_data_mart_kimball_star_schema|데이터 마트]]**: DW에서 부서별로 서브셋을 추출한 분석 저장소

📢 **섹션 요약 비유**: Inmon은 **도시 전체 하수도망 먼저 설계**하고 건물을 짓는 방식, Kimball은 **각 건물 화장실부터 만들고 나중에 연결**하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 현대 클라우드 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]

| 제품 | 특징 |
|:---|:---|
| **[[541_cassandra|Snowflake]]** | 컴퓨트·스토리지 분리, [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]], [[386_data_clean_room_sharing|데이터 공유]] |
| **Google [[263_storage_compute_separation_bigquery|BigQuery]]** | [[206_serverless_cold_start|서버리스]], 열 지향 스토리지, ML 내장([[263_storage_compute_separation_bigquery|BigQuery]] ML) |
| **Amazon Redshift** | 열 지향, Spectrum으로 S3 직접 [[298_qkv_attention|쿼리]], RA3 노드 |
| **Azure Synapse** | 전통 [[209_data_warehouse_schema_on_write|DW]] + [[208_data_lake_schema_on_read|데이터 레이크]] 통합 |

### 기술사 판단 포인트

1. **설계 방법론 선택**: 전사 [[194_consistency_database_integrity|일관성]] 중요 → [[311_inmon|Inmon]], 빠른 비즈니스 가치 → [[312_kimball|Kimball]]
2. **[[209_data_warehouse_schema_on_write|DW]] vs [[146_lakehouse|레이크하우스]]**: ACID [[191_transaction_concept_states|트랜잭션]] 필요 → [[209_data_warehouse_schema_on_write|DW]], ML 학습 [[001_dikw_pyramid|데이터]] 병행 → [[146_lakehouse|레이크하우스]]
3. **[[014_data_model_components|데이터 모델]] 진화**: [[277_scd_slowly_changing_dimension_modeling|SCD]]([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]) 타입 2로 이력 보존 [[268_strategy_pattern|전략]] 필수

📢 **섹션 요약 비유**: 클라우드 DW는 **자동화된 도서관 로봇**과 같다. 입고부터 [[104_classification_analysis|분류]]까지 자동으로 처리하며, 수백만 권도 순식간에 검색한다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 설명 |
|:---|:---|
| 단일 진실 공급원 | 부서 간 [[001_dikw_pyramid|데이터]] 불일치 해소 |
| 의사결정 가속 | 임원 대시보드·[[018_kpi|KPI]] 실시간 조회 |
| 규정 준수 | [[791_gdpr_eu|GDPR]]·SOX 규정 이력 [[001_dikw_pyramid|데이터]] 보존 |
| 분석 [[282_performance_tactics|성능]] | 열 지향 스토리지로 집계 [[298_qkv_attention|쿼리]] 100배+ 향상 |

### 결론

[[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 기업 [[001_dikw_pyramid|데이터]] 분석의 **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 기반**이다. Inmon의 엄격한 통합 모델은 수십 년간 대기업의 분석 인프라를 지탱해왔으며, 현대 클라우드 DW는 [[206_serverless_cold_start|서버리스]]·무제한 확장·SQL 호환성으로 이 유산을 계승한다. [[208_data_lake_schema_on_read|데이터 레이크]]와의 경계가 [[146_lakehouse|레이크하우스]]로 수렴하는 현재, DW의 [[005_schema|스키마]] 규율과 ACID 보장은 여전히 핵심 가치로 남아 있다.

📢 **섹션 요약 비유**: [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 기업의 **역사 기록실**이다. 모든 것이 정확히 기록되어 있어서, 10년 전 매출도 오늘 매출처럼 정확하게 조회할 수 있다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 설계 방법론 | [[311_inmon|Inmon]] CIF | [[402_top_down_integration|Top-Down]] 전사 EDW 구축 |
| 설계 방법론 | [[312_kimball|Kimball]] [[118_dimensional_modeling_star_schema|차원 모델링]] | [[403_bottom_up_integration|Bottom-Up]] [[209_data_mart_kimball_star_schema|데이터 마트]] 우선 |
| 구성 요소 | [[291_ods|ODS]] ([[264_ods_operational_data_store_realtime|Operational Data Store]]) | 실시간 통합 운영 뷰 |
| 하위 개념 | [[209_data_mart_kimball_star_schema|데이터 마트]] | 부서별 서브셋 분석 저장소 |
| 핵심 프로세스 | [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] | [[001_dikw_pyramid|데이터]] 추출·변환·적재 |
| [[005_schema|스키마]] 패턴 | 스타/[[335_snowflake_schema|스노우플레이크 스키마]] | [[312_kimball|Kimball]] 차원 모델 |
| 진화형 | [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] | [[209_data_warehouse_schema_on_write|DW]]+Lake 결합 아키텍처 |
| 클라우드 제품 | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift | 현대 클라우드 [[209_data_warehouse_schema_on_write|DW]] |

### 👶 어린이를 위한 3줄 비유 설명

1. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 **회사의 모든 기록을 모아놓은 거대한 도서관**이야. 판매 기록, 고객 기록, 재고 기록이 다 모여 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP (운영 DB: MySQL · PostgreSQL)
    │ ETL
    ▼
Data Warehouse: Schema-on-Write · 정형 분석 (Inmon · Kimball)
    ├─► Star Schema · Snowflake Schema
    └─► OLAP Cube: Drill-Down · Roll-Up · Slice · Dice
    │
    ▼
클라우드 DW: BigQuery · Snowflake · Redshift
    │
    ▼
Lakehouse: DW 기능 + Lake 유연성 통합
```
2. 이 도서관은 책을 넣을 때 **미리 꼼꼼히 [[104_classification_analysis|분류]]해서 정리**해. 그래서 찾을 때는 아주 빠르게 찾을 수 있어.
3. 한 번 넣은 기록은 **지우지 않고 영원히 보관**해. 5년 전 기록도 오늘처럼 정확하게 볼 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 208 / 258

← **이전**: [[207_data_lake_schema_on_read_raw_storage|207. 데이터 레이크 (Data Lake) 스키마 온 리드 (Schema-on-Read)]]
**다음**: [[209_data_mart_kimball_star_schema|209. 데이터 마트 (Data Mart) Kimball 다차원 분석 스타 스키마 (Star Schema)]] →

---
