---
title: 데이터 웨어하우스 (Data Warehouse)
date: '2024-05-22'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. 기업의 의사결정을 지원하기 위해 여러 시스템의 [[001_dikw_pyramid|데이터]]를 **주제 중심적, 통합적, 시계열적, 비휘발성**으로 구성한 [[001_dikw_pyramid|데이터]] 저장소이다.
2. 저장 전 [[001_dikw_pyramid|데이터]]를 [[093_normalization|정규화]]하고 가공하는 **[[010_schema_on_write|스키마 온 라이트]]([[010_schema_on_write|Schema-on-Write]])** 방식을 사용하여 높은 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]과 [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 보장한다.
3. [[282_business_intelligence_bi_technology_framework|비즈니스 인텔리전스]](BI)와 리포팅의 핵심 인프라이며, 최근에는 클라우드 기반의 MPP(Massive Parallel Processing) 아키텍처로 진화했다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
운영 시스템([[327_hint_handoff|OLTP]])은 [[191_transaction_concept_states|트랜잭션]] 처리에 최적화되어 있어 복잡한 분석 [[298_qkv_attention|쿼리]]에는 부적합하다. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 빌 인먼(Bill [[311_inmon|Inmon]])과 랄프 킴벌(Ralph [[312_kimball|Kimball]])의 이론을 바탕으로, 과거부터 현재까지의 [[001_dikw_pyramid|데이터]]를 분석하기 좋은 형태로 통합하여 기업의 [[268_strategy_pattern|전략]]적 의사결정을 돕는 기술이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 [[215_etl_vs_elt_pipeline|ETL]] 과정을 통해 원천 시스템에서 [[001_dikw_pyramid|데이터]]를 가져와 전용 저장소에 적재한다.

```text
[ Data Warehouse Architecture / 데이터 웨어하우스 아키텍처 ]

    Source Systems (ERP, CRM)          Data Warehouse (DW)             BI & Analytics
    +-------------------+       +-----------------------+       +-------------------+
    | [Operational DB]  |       |     [Staging Area]    |       |  Reporting Tools  |
    | [Flat Files]      | ----> |     [Data Vault]      | ----> |  (SQL, Dashboards)|
    | [External API]    |       +-----------+-----------+       +---------+---------+
    +---------+---------+                   |                             |
                                            v                             v
                                +-----------+-----------+       +---------+---------+
                                |      Data Marts       | ----> |  Ad-hoc Analysis  |
                                | (Sales, Finance, etc) |       |  (Excel, BI)      |
                                +-----------------------+       +-------------------+
```

1. **4대 특징 ([[311_inmon|Inmon]])**:
   - **주제 중심적 (Subject Oriented)**: 고객, 상품 등 특정 주제별 [[001_dikw_pyramid|데이터]] 구성.
   - **통합적 (Integrated)**: 전사의 [[001_dikw_pyramid|데이터]]를 표준화된 포맷으로 통합.
   - **시계열적 (Time Variant)**: 과거의 이력 [[001_dikw_pyramid|데이터]]를 보존.
   - **비휘발성 (Non-volatile)**: 한 번 적재된 [[001_dikw_pyramid|데이터]]는 삭제되지 않음.
2. **모델링**: [[334_star_schema|스타 스키마]]([[296_star_schema|Star Schema]])와 눈송이 [[005_schema|스키마]]([[313_snowflake_schema|Snowflake Schema]])를 사용하여 분석 속도를 최적화한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]]) | 운영 [[002_database_definition|데이터베이스]] ([[327_hint_handoff|OLTP]]) |
| :--- | :--- | :--- |
| **주요 목적** | 의사결정 지원 및 분석 | 일상적 [[191_transaction_concept_states|트랜잭션]] 처리 |
| **[[001_dikw_pyramid|데이터]] 범위** | 과거 이력 포함 (수년) | [[178_as_is_to_be_analysis|현재 상태]] 위주 (수개월) |
| **작업 단위** | 복잡한 대량의 [[298_qkv_attention|쿼리]] | 작고 빠른 [[191_transaction_concept_states|트랜잭션]] |
| **핵심 기술** | [[316_olap|OLAP]], MPP, [[234_columnar_storage_parquet_orc|Columnar Storage]] | SQL, Indexing, [[093_normalization|Normalization]] |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **MPP 아키텍처**: 최신 클라우드 [[209_data_warehouse_schema_on_write|DW]]([[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]])는 수많은 컴퓨팅 노드를 [[430_index_fast_full_scan|병렬]]로 사용하여 수조 건의 [[001_dikw_pyramid|데이터]]를 초 단위로 [[298_qkv_attention|쿼리]]한다.
2. **ELT의 부상**: 클라우드 DW의 강력한 연산력을 활용하기 위해 정제 작업을 [[209_data_warehouse_schema_on_write|DW]] 내부에서 수행하는 [[034_elt|ELT]](Extract, Load, Transform) 방식이 선호된다.
3. **PE 관점의 판단**: DW는 품질이 [[395_verification_process_review|검증]]된 '[[119_gitops_single_source_of_truth|Single Source of Truth]]'여야 한다. [[001_dikw_pyramid|데이터]] 정합성([[194_consistency_database_integrity|Consistency]])과 계보 관리가 뒷받침되지 않으면 신뢰할 수 없는 분석 결과를 낳게 된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[209_data_warehouse_schema_on_write|데이터 웨어하우스]]는 사라지지 않고 [[208_data_lake_schema_on_read|데이터 레이크]]와 결합하여 '[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]'로 진화하고 있다. [[002_structured_data|정형 데이터]]의 정밀함과 [[004_unstructured_data|비정형 데이터]]의 방대함을 동시에 아우르는 하이브리드 [[268_strategy_pattern|전략]]이 향후 기업 [[104_da_as_is_analysis|데이터 아키텍처]]의 표준이 될 것이며, 이는 [[190_ai_llm_requirements_specification|AI]] 기반의 자동화된 통찰([[308_ai_bi_augmented_analytics|Augmented Analytics]])을 이끌어낼 것이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: [[001_dikw_pyramid|Data]] Infrastructure, Business Intelligence
- **하위 개념**: [[209_data_mart_kimball_star_schema|Data Mart]], [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]], [[296_star_schema|Star Schema]], [[316_olap|OLAP]]
- **연관 개념**: [[294_oltp_vs_olap|OLTP vs OLAP]], MPP, [[210_data_lakehouse_delta_lake|Data Lakehouse]]

---

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: Data Infrastructure, Business Intelligence]
    │
    ▼
[하위 개념: Data Mart, ETL/ELT, Star Schema, OLAP]
    │
    ▼
[연관 개념: OLTP vs OLAP, MPP, Data Lakehouse]
```

이 흐름도는 상위 개념: [[001_dikw_pyramid|Data]] Infrastructure, Business Intelligence에서 출발해 연관 개념: [[294_oltp_vs_olap|OLTP vs OLAP]], MPP, [[001_dikw_pyramid|Data]] Lakehouse까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **[[209_data_warehouse_schema_on_write|데이터 웨어하우스]]**: 학교 도서관에서 책들을 종류별(과학, 소설)로 아주 깔끔하게 정리해둔 책장과 같아요.
2. **정확함**: 이름표가 정확하게 붙어 있어서, 내가 원하는 정보를 아주 빠르게 찾을 수 있어요.
3. **용도**: "지난달에 대출이 가장 많았던 책이 뭐지?" 같은 어려운 질문에 대답할 때 최고예요.
