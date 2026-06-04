+++
title = "데이터 웨어하우스 (Data Warehouse)"
date = 2024-05-22

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. 기업의 의사결정을 지원하기 위해 여러 시스템의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>주제 중심적, 통합적, 시계열적, 비휘발성</strong>으로 구성한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소이다.
2. 저장 전 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하고 가공하는 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">스키마 온 라이트</a>(<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">Schema-on-Write</a>)</strong> 방식을 사용하여 높은 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 보장한다.
3. [비즈니스 인텔리전스](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/282_business_intelligence_bi_technology_framework/)(BI)와 리포팅의 핵심 인프라이며, 최근에는 클라우드 기반의 MPP(Massive Parallel Processing) 아키텍처로 진화했다.

---

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
운영 시스템([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리에 최적화되어 있어 복잡한 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에는 부적합하다. [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 빌 인먼(Bill [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/953_inmon/))과 랄프 킴벌(Ralph [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/954_kimball/))의 이론을 바탕으로, 과거부터 현재까지의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분석하기 좋은 형태로 통합하여 기업의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 의사결정을 돕는 기술이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 과정을 통해 원천 시스템에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져와 전용 저장소에 적재한다.

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

1. <strong>4대 특징 (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/953_inmon/">Inmon</a>)</strong>:
   - **주제 중심적 (Subject Oriented)**: 고객, 상품 등 특정 주제별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구성.
   - **통합적 (Integrated)**: 전사의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 표준화된 포맷으로 통합.
   - **시계열적 (Time Variant)**: 과거의 이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보존.
   - **비휘발성 (Non-volatile)**: 한 번 적재된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 삭제되지 않음.
2. **모델링**: [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/))와 눈송이 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)([Snowflake Schema](/knowledge-base/studynote/12_it_management/05_security_compliance/955_snowflake_schema/))를 사용하여 분석 속도를 최적화한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) | 운영 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) ([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) |
| :--- | :--- | :--- |
| **주요 목적** | 의사결정 지원 및 분석 | 일상적 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 범위</strong> | 과거 이력 포함 (수년) | [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 위주 (수개월) |
| **작업 단위** | 복잡한 대량의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 작고 빠른 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) |
| **핵심 기술** | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/), MPP, [Columnar Storage](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/) | SQL, Indexing, [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. **MPP 아키텍처**: 최신 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/))는 수많은 컴퓨팅 노드를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 사용하여 수조 건의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 초 단위로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)한다.
2. **ELT의 부상**: 클라우드 DW의 강력한 연산력을 활용하기 위해 정제 작업을 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서 수행하는 [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/)(Extract, Load, Transform) 방식이 선호된다.
3. **PE 관점의 판단**: DW는 품질이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 '[Single Source of Truth](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)'여야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))과 계보 관리가 뒷받침되지 않으면 신뢰할 수 없는 분석 결과를 낳게 된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)는 사라지지 않고 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)와 결합하여 '[데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)'로 진화하고 있다. [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)의 정밀함과 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)의 방대함을 동시에 아우르는 하이브리드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 향후 기업 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 표준이 될 것이며, 이는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반의 자동화된 통찰([Augmented Analytics](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/308_ai_bi_augmented_analytics/))을 이끌어낼 것이다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Infrastructure, Business Intelligence
- **하위 개념**: [Data Mart](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/), [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/), [Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/), [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)
- **연관 개념**: [OLTP vs OLAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/), MPP, [Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)

---

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: Data Infrastructure, Business Intelligence]
    |
    v
[하위 개념: Data Mart, ETL/ELT, Star Schema, OLAP]
    |
    v
[연관 개념: OLTP vs OLAP, MPP, Data Lakehouse]
```

이 흐름도는 상위 개념: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Infrastructure, Business Intelligence에서 출발해 연관 개념: [OLTP vs OLAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/), MPP, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lakehouse까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">데이터 웨어하우스</a></strong>: 학교 도서관에서 책들을 종류별(과학, 소설)로 아주 깔끔하게 정리해둔 책장과 같아요.
2. **정확함**: 이름표가 정확하게 붙어 있어서, 내가 원하는 정보를 아주 빠르게 찾을 수 있어요.
3. **용도**: "지난달에 대출이 가장 많았던 책이 뭐지?" 같은 어려운 질문에 대답할 때 최고예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 262

<- **이전**: [데이터 늪 (Data Swamp)](/knowledge-base/studynote/16_bigdata/07_data_lake/144_data_swamp/)
**다음**: [146. 레이크하우스 (Lakehouse) — 데이터 레이크 + 웨어하우스 융합](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) ->

---
