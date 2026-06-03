+++
title = "208. 데이터 웨어하우스 (Data Warehouse) 스키마 온 라이트 Inmon 설계"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Warehouse)는 여러 운영 시스템의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주제 지향적(Subject-Oriented)으로 통합·정제하여 의사결정 지원에 최적화된 분석용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스다.
> 2. **가치**: [스키마 온 라이트](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)([Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) 방식으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재 전 품질을 보장하여, 경영진이 일관된 단일 진실 공급원(Single Source of Truth)을 기반으로 의사결정할 수 있도록 한다.
> 3. **판단 포인트**: [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) 방법론([Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/), [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 중심)과 [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론([Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/), [차원 모델링](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/) 중심)의 트레이드오프를 명확히 이해하고, 기업 규모·분석 요건에 따라 선택 근거를 논술할 것.

---

## Ⅰ. 개요 및 필요성

### [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 정의

빌 인몬(Bill [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/))이 1990년대 정의한 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 4대 특성:

- **주제 지향(Subject-Oriented)**: 판매, 고객, 제품 등 비즈니스 주제별로 구성
- **통합(Integrated)**: 이기종 소스 시스템의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 일관된 형식으로 통합
- **시간 변형(Time-Variant)**: 시간 흐름에 따른 변화를 보존하여 이력 분석 지원
- **비휘발성(Non-Volatile)**: 적재된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 수정·삭제되지 않고 분석 용도로만 읽힘

### 운영 DB vs [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)

| 항목 | 운영 DB ([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)) |
|:---|:---|:---|
| **목적** | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 | 분석·의사결정 지원 |
| **[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 유형** | 단순 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 복잡한 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 범위** | 현재 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 수년간 이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 설계** | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)) | 비정규화(스타/스노우플레이크) |
| **갱신 주기** | 실시간 | 배치(일/주/월) |
| **사용자 수** | 수천~수만 명 | 수십~수백 명 |

📢 **섹션 요약 비유**: 운영 DB는 **편의점 계산대**(빠른 처리), [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 **경영진의 통계 보고서실**(느리지만 깊은 통찰)이다.

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

### [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) ([스키마 온 라이트](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) 메커니즘

[데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 핵심 특성: **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재 전 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 확정**

```
소스 데이터 → [ETL 변환] → [스키마 검증] → [DW 적재]
              ↑                ↑
          타입 변환         NULL 검사
          코드 매핑         참조 무결성
          중복 제거         비즈니스 규칙
```

📢 **섹션 요약 비유**: [스키마 온 라이트](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)는 **도서관에 책이 들어올 때 즉시 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·라벨링하는 것**이다. 찾기는 쉽지만 입고 작업이 오래 걸린다.

---

## Ⅲ. 비교 및 연결

### [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) vs [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론 비교

| 항목 | [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) ([Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/)) | [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) ([Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/)) |
|:---|:---|:---|
| **접근 방식** | 전사 EDW 우선 구축 | [데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) 우선 구축 |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)** | [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 비정규화([스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)) |
| **구현 난이도** | 높음(장기 프로젝트) | 낮음(빠른 성과) |
| **유지보수** | 쉬움(중복 없음) | 어려움(마트 간 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) |
| **[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)** | 조인 증가로 느릴 수 있음 | 빠름(비정규화) |
| **적합 기업** | 대기업(전사 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 중요) | 중소기업(빠른 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 필요) |

### [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 연결 개념

- **[ODS](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/291_ods/) ([Operational Data Store](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/264_ods_operational_data_store_realtime/))**: 실시간에 가까운 통합 운영 뷰 (DW와 구별됨)
- **[ETL vs ELT](/knowledge-base/studynote/12_it_management/05_security_compliance/317_etl_vs_elt/)**: DW는 전통적으로 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/), 클라우드 DW는 ELT로 전환
- **[데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/)**: DW에서 부서별로 서브셋을 추출한 분석 저장소

📢 **섹션 요약 비유**: Inmon은 **도시 전체 하수도망 먼저 설계**하고 건물을 짓는 방식, Kimball은 **각 건물 화장실부터 만들고 나중에 연결**하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 현대 클라우드 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)

| 제품 | 특징 |
|:---|:---|
| **[Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)** | 컴퓨트·스토리지 분리, [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/), [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) |
| **Google [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)** | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), 열 지향 스토리지, ML 내장([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) ML) |
| **Amazon Redshift** | 열 지향, Spectrum으로 S3 직접 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), RA3 노드 |
| **Azure Synapse** | 전통 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) + [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 통합 |

### 기술사 판단 포인트

1. **설계 방법론 선택**: 전사 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 중요 → [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/), 빠른 비즈니스 가치 → [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/)
2. **[DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) vs [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)**: ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 필요 → [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), ML 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 병행 → [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)
3. **[데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 진화**: [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/)([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) 타입 2로 이력 보존 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필수

📢 **섹션 요약 비유**: 클라우드 DW는 **자동화된 도서관 로봇**과 같다. 입고부터 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)까지 자동으로 처리하며, 수백만 권도 순식간에 검색한다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 설명 |
|:---|:---|
| 단일 진실 공급원 | 부서 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 해소 |
| 의사결정 가속 | 임원 대시보드·[KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 실시간 조회 |
| 규정 준수 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·SOX 규정 이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 |
| 분석 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 열 지향 스토리지로 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 100배+ 향상 |

### 결론

[데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 기업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석의 **[신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 기반**이다. Inmon의 엄격한 통합 모델은 수십 년간 대기업의 분석 인프라를 지탱해왔으며, 현대 클라우드 DW는 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)·무제한 확장·SQL 호환성으로 이 유산을 계승한다. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)와의 경계가 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)로 수렴하는 현재, DW의 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 규율과 ACID 보장은 여전히 핵심 가치로 남아 있다.

📢 **섹션 요약 비유**: [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 기업의 **역사 기록실**이다. 모든 것이 정확히 기록되어 있어서, 10년 전 매출도 오늘 매출처럼 정확하게 조회할 수 있다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 설계 방법론 | [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) CIF | [Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/) 전사 EDW 구축 |
| 설계 방법론 | [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) [차원 모델링](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/) | [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/) [데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) 우선 |
| 구성 요소 | [ODS](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/291_ods/) ([Operational Data Store](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/264_ods_operational_data_store_realtime/)) | 실시간 통합 운영 뷰 |
| 하위 개념 | [데이터 마트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) | 부서별 서브셋 분석 저장소 |
| 핵심 프로세스 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 추출·변환·적재 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 패턴 | 스타/[스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/) | [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 차원 모델 |
| 진화형 | [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)+Lake 결합 아키텍처 |
| 클라우드 제품 | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift | 현대 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) |

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 **회사의 모든 기록을 모아놓은 거대한 도서관**이야. 판매 기록, 고객 기록, 재고 기록이 다 모여 있어.

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
2. 이 도서관은 책을 넣을 때 **미리 꼼꼼히 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해서 정리**해. 그래서 찾을 때는 아주 빠르게 찾을 수 있어.
3. 한 번 넣은 기록은 **지우지 않고 영원히 보관**해. 5년 전 기록도 오늘처럼 정확하게 볼 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 208 / 258

← **이전**: [207. 데이터 레이크 (Data Lake) 스키마 온 리드 (Schema-on-Read)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/207_data_lake_schema_on_read_raw_storage/)
**다음**: [209. 데이터 마트 (Data Mart) Kimball 다차원 분석 스타 스키마 (Star Schema)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) →

---
