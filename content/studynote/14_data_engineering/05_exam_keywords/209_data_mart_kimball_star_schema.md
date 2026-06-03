+++
title = "209. 데이터 마트 (Data Mart) Kimball 다차원 분석 스타 스키마 (Star Schema)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mart)는 특정 부서나 비즈니스 도메인을 위해 최적화된 분석 전용 소규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소이며, [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론의 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/))가 핵심 설계 패턴이다.
> 2. **가치**: [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)([Fact Table](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)) 중심의 비정규화 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 복잡한 조인 없이 빠른 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 가능하게 하여, 비즈니스 분석가가 SQL만으로 다차원 분석을 수행할 수 있다.
> 3. **판단 포인트**: 독립형 마트(Independent Mart)는 부서별 신속 구축에 유리하지만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 문제를 야기하므로, 콘포밍 차원([Conformed Dimension](/knowledge-base/studynote/05_database/06_dw_olap_trends/574_conformed_dimension/))으로 전사 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 확보하는 설계가 필수다.

---

## Ⅰ. 개요 및 필요성

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트 정의

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트는 <strong>전사 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">데이터 웨어하우스</a>(EDW: Enterprise <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/">Data Warehouse</a>)의 부분집합</strong>으로, 특정 사업부·기능·주제 영역을 위한 분석 저장소다.

- **판매 마트**: 지역별·제품별·채널별 매출 분석
- **인사 마트**: 직원 성과·이직률·채용 비용 분석
- <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 마트</strong>: 재고·납품 시간·공급업체 분석

### [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론의 핵심 원칙

랄프 킴볼(Ralph [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/))이 주창한 [차원 모델링](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/)([Dimensional Modeling](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/))의 4원칙:
1. **비즈니스 프로세스 선택**: 분석 대상 프로세스 확정 (예: 판매 주문)
2. **세분성(Grain) 정의**: [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)의 행 하나가 나타내는 단위 확정 (예: 개별 주문 라인)
3. **차원 결정**: 분석 축 정의 (날짜, 고객, 제품, 지역 등)
4. **팩트 결정**: 측정값 확정 (매출액, 수량, 할인율 등)

📢 **섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트는 <strong>부서 전용 분석 냉장고</strong>다. 전사 냉장고(EDW)에서 각 팀이 자주 쓰는 재료만 꺼내 놓은 소형 냉장고다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) ([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/)) 구조

```
                    ┌─────────────────┐
                    │  DimDate (날짜)  │
                    │  date_key (PK)  │
                    │  year, month    │
                    │  quarter, day   │
                    └────────┬────────┘
                             │
┌───────────────┐            │             ┌────────────────┐
│ DimCustomer   │            │             │  DimProduct    │
│ (고객 차원)    │            │             │  (제품 차원)   │
│ customer_key  ├────────────┤             │  product_key   │
│ customer_name │            │             │  product_name  │
│ city, region  │     ┌──────▼──────┐      │  category      │
│ segment       │     │FactSales    │      │  brand, price  │
└───────────────┘     │ (판매 팩트)  │      └────────────────┘
          ┌───────────┤ date_key(FK)├──────────────┐
          │           │ cust_key(FK)│               │
          │           │ prod_key(FK)│               │
          │           │ store_key(FK│               │
          │           │ sales_amt   │               │
          │           │ quantity    │               │
          │           │ discount    │               │
          │           └─────────────┘               │
          │                   │                     │
          │           ┌───────▼───────┐             │
          │           │  DimStore     │             │
          │           │  (매장 차원)  │             │
          └───────────┤  store_key    ├─────────────┘
                      │  store_name   │
                      │  city, region │
                      └───────────────┘
```

### 마트 유형 비교

| 유형 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| **의존형 마트** | EDW에서 서브셋 추출 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 | EDW 구축 선행 필요 |
| **독립형 마트** | 소스에서 직접 구축 | 신속한 구현 | 부서 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 |
| **논리적 마트** | 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))로 구현 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 없음 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 가능 |

### 콘포밍 차원 ([Conformed Dimension](/knowledge-base/studynote/05_database/06_dw_olap_trends/574_conformed_dimension/))

여러 마트에서 <strong>동일한 <a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/">차원 테이블</a>을 공유</strong>하여 부서 간 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보:
- 날짜 차원(Date Dimension): 모든 마트에서 동일한 날짜 기준 사용
- 고객 차원([C고객](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) Dimension): 판매 마트·[CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) 마트·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 마트 공유

📢 **섹션 요약 비유**: [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 <strong>별자리 지도</strong>와 같다. 중앙의 팩트(별)를 여러 차원(행성)이 둘러싸는 구조로, 각 행성이 분석의 관점이 된다.

---

## Ⅲ. 비교 및 연결

### [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) vs [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론

| 관점 | [Inmon](/knowledge-base/studynote/12_it_management/05_security_compliance/311_inmon/) | [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) |
|:---|:---|:---|
| 접근 방향 | [Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/) (EDW 우선) | [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/) (마트 우선) |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 비정규화 스타/스노우플레이크 |
| 구현 속도 | 느림 (수년) | 빠름 (수개월) |
| 전사 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 높음 | 콘포밍 차원으로 확보 필요 |
| 분석 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 조인 증가로 느릴 수 있음 | 빠른 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |

### [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) vs [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/)

- <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/">스타 스키마</a></strong>: [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) 비정규화 → 조인 수 최소화, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능 우수](/knowledge-base/studynote/05_database/07_exam_summary/484_elt_extract_load_transform/)
- <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/">스노우플레이크 스키마</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/313_snowflake_schema/">Snowflake Schema</a>)</strong>: [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) → 저장 공간 절약, 유지보수 용이

📢 **섹션 요약 비유**: Inmon은 **먼저 도시 전체 설계도 그리기**, Kimball은 <strong>각 동네부터 빠르게 개발하기</strong>다. 어느 쪽이 맞다기보다 상황에 따라 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) 설계 실무 단계

1. **비즈니스 요건 수집**: 분석 질문 목록 (예: "지역별·제품군별 월매출 비교")
2. **세분성 정의**: 팩트의 원자 단위 결정 (개별 거래 라인 vs 일별 집계)
3. <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/">차원 테이블</a> 설계</strong>: [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/)([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) 타입 결정
4. <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/">팩트 테이블</a> 설계</strong>: 가산적(Additive)·반가산적(Semi-Additive)·비가산적(Non-Additive) 팩트 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)
5. <strong>집계 <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/">팩트 테이블</a></strong>: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위한 사전 집계 테이블 추가

### 기술사 판단 포인트

1. **마트 증식 위험**: 독립형 마트 남용 시 "분석 스파게티" 발생 → 콘포밍 차원으로 통제
2. <strong>클라우드 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a> 연계</strong>: [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·BigQuery에서 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화의 기본
3. **실시간 마트**: [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) + 스트리밍으로 준실시간 마트 구축 가능

📢 **섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트 설계는 <strong>요리 레시피 표준화</strong>와 같다. 각 요리사(부서)가 같은 재료(콘포밍 차원)를 쓰되, 자기 전문 요리(마트)를 만들 수 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 응답 속도 향상 | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 대비 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 향상 |
| 비즈니스 사용자 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | SQL/BI 도구로 독립적 분석 가능 |
| 부서 특화 분석 환경 | 판매·재무·HR 각 최적화된 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) |
| 의사결정 속도 개선 | 임원 리포트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시간 수일 → 실시간 |

### 결론

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트와 Kimball의 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 <strong>분석의 민주화</strong>를 실현하는 핵심 도구다. 비정규화된 차원 모델은 복잡한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 없이도 비즈니스 사용자가 다차원 분석을 수행할 수 있게 한다. 그러나 콘포밍 차원과 전사 거버넌스 없이는 마트 증식이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치로 이어지므로, [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론의 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 아키텍처([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) 원칙 준수가 필수다.

📢 **섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트의 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 <strong>각 팀 전용 분석 대시보드</strong>다. 공통 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(콘포밍 차원)를 공유하면서도 각 팀이 원하는 분석 뷰를 쉽게 만들 수 있다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 설계 방법론 | [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) [차원 모델링](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/) | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) 기반 [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/) 접근 |
| 핵심 구조 | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) | 팩트+차원 비정규화 구조 |
| 확장 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/) | 차원 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| 핵심 테이블 | [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) | 측정값·집계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 핵심 테이블 | [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) | 분석 맥락·[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보 | 콘포밍 차원 | 마트 간 공유 차원 |
| 이력 관리 | [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) ([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) | 차원 변경 이력 보존 |
| 상위 저장소 | [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 마트의 원천 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마트는 <strong>학급별 사물함</strong>이야. 학교 전체 창고([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))에서 우리 반에 필요한 것만 꺼내 넣어둔 것이지.

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP (운영 시스템)
    │
    ▼
Data Warehouse (전사 통합 저장소)
    │
    ▼
Data Mart (부서별 서브셋)
    ├─► 종속형: DW에서 추출 (Top-Down, Inmon)
    └─► 독립형: 직접 구축 (Bottom-Up, Kimball)
    │
    ▼
Star Schema · Kimball 차원 모델링
```
2. [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 <strong>별 모양 조직도</strong>야. 가운데 별(팩트)이 "우리가 분석할 것"이고, 주변 행성들(차원)이 "어떤 각도에서 볼지"를 나타내.
3. 같은 날짜 기준을 모든 반이 쓰면 <strong>"이번 달"이 다 같은 의미</strong>가 돼. 그게 콘포밍 차원이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 209 / 258

← **이전**: [208. 데이터 웨어하우스 (Data Warehouse) 스키마 온 라이트 Inmon 설계](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/)
**다음**: [210. 팩트 테이블 (Fact Table)·차원 테이블 (Dimension Table)·스노우플레이크 스키마 (Snowflake Schema)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) →

---
