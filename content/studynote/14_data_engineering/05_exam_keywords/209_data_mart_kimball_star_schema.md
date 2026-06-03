---
title: 209. 데이터 마트 (Data Mart) Kimball 다차원 분석 스타 스키마 (Star Schema)
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[001_dikw_pyramid|데이터]] 마트([[001_dikw_pyramid|Data]] Mart)는 특정 부서나 비즈니스 도메인을 위해 최적화된 분석 전용 소규모 [[001_dikw_pyramid|데이터]] 저장소이며, [[312_kimball|Kimball]] 방법론의 [[334_star_schema|스타 스키마]]([[296_star_schema|Star Schema]])가 핵심 설계 패턴이다.
> 2. **가치**: [[210_fact_dimension_table_snowflake_schema|팩트 테이블]]([[210_fact_dimension_table_snowflake_schema|Fact Table]]) 중심의 비정규화 [[334_star_schema|스타 스키마]]는 복잡한 조인 없이 빠른 집계 [[298_qkv_attention|쿼리]]를 가능하게 하여, 비즈니스 분석가가 SQL만으로 다차원 분석을 수행할 수 있다.
> 3. **판단 포인트**: 독립형 마트(Independent Mart)는 부서별 신속 구축에 유리하지만 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 문제를 야기하므로, 콘포밍 차원([[574_conformed_dimension|Conformed Dimension]])으로 전사 [[194_consistency_database_integrity|일관성]]을 확보하는 설계가 필수다.

---

## Ⅰ. 개요 및 필요성

### [[001_dikw_pyramid|데이터]] 마트 정의

[[001_dikw_pyramid|데이터]] 마트는 **전사 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]](EDW: Enterprise [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]])의 부분집합**으로, 특정 사업부·기능·주제 영역을 위한 분석 저장소다.

- **판매 마트**: 지역별·제품별·채널별 매출 분석
- **인사 마트**: 직원 성과·이직률·채용 비용 분석
- **[[520_supply_chain_attack_and_ci_cd_security|공급망]] 마트**: 재고·납품 시간·공급업체 분석

### [[312_kimball|Kimball]] 방법론의 핵심 원칙

랄프 킴볼(Ralph [[312_kimball|Kimball]])이 주창한 [[118_dimensional_modeling_star_schema|차원 모델링]]([[118_dimensional_modeling_star_schema|Dimensional Modeling]])의 4원칙:
1. **비즈니스 프로세스 선택**: 분석 대상 프로세스 확정 (예: 판매 주문)
2. **세분성(Grain) 정의**: [[210_fact_dimension_table_snowflake_schema|팩트 테이블]]의 행 하나가 나타내는 단위 확정 (예: 개별 주문 라인)
3. **차원 결정**: 분석 축 정의 (날짜, 고객, 제품, 지역 등)
4. **팩트 결정**: 측정값 확정 (매출액, 수량, 할인율 등)

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 마트는 **부서 전용 분석 냉장고**다. 전사 냉장고(EDW)에서 각 팀이 자주 쓰는 재료만 꺼내 놓은 소형 냉장고다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[334_star_schema|스타 스키마]] ([[296_star_schema|Star Schema]]) 구조

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
| **의존형 마트** | EDW에서 서브셋 추출 | [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 보장 | EDW 구축 선행 필요 |
| **독립형 마트** | 소스에서 직접 구축 | 신속한 구현 | 부서 간 [[001_dikw_pyramid|데이터]] 불일치 |
| **논리적 마트** | 뷰([[151_sql_view_virtual_table|View]])로 구현 | [[001_dikw_pyramid|데이터]] 중복 없음 | [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] 저하 가능 |

### 콘포밍 차원 ([[574_conformed_dimension|Conformed Dimension]])

여러 마트에서 **동일한 [[273_dimension_table_analysis_perspective|차원 테이블]]을 공유**하여 부서 간 [[194_consistency_database_integrity|일관성]] 확보:
- 날짜 차원(Date Dimension): 모든 마트에서 동일한 날짜 기준 사용
- 고객 차원([[026_three_c_analysis|Customer]] Dimension): 판매 마트·[[107_crm_customer_relationship_management|CRM]] 마트·[[090_service_kubernetes_network_load_balancing|서비스]] 마트 공유

📢 **섹션 요약 비유**: [[334_star_schema|스타 스키마]]는 **별자리 지도**와 같다. 중앙의 팩트(별)를 여러 차원(행성)이 둘러싸는 구조로, 각 행성이 분석의 관점이 된다.

---

## Ⅲ. 비교 및 연결

### [[311_inmon|Inmon]] vs [[312_kimball|Kimball]] 방법론

| 관점 | [[311_inmon|Inmon]] | [[312_kimball|Kimball]] |
|:---|:---|:---|
| 접근 방향 | [[402_top_down_integration|Top-Down]] (EDW 우선) | [[403_bottom_up_integration|Bottom-Up]] (마트 우선) |
| [[005_schema|스키마]] | [[105_third_normal_form_3nf_transitive|3NF]] [[093_normalization|정규화]] | 비정규화 스타/스노우플레이크 |
| 구현 속도 | 느림 (수년) | 빠름 (수개월) |
| 전사 [[194_consistency_database_integrity|일관성]] | 높음 | 콘포밍 차원으로 확보 필요 |
| 분석 [[282_performance_tactics|성능]] | 조인 증가로 느릴 수 있음 | 빠른 집계 [[298_qkv_attention|쿼리]] |

### [[334_star_schema|스타 스키마]] vs [[335_snowflake_schema|스노우플레이크 스키마]]

- **[[334_star_schema|스타 스키마]]**: [[273_dimension_table_analysis_perspective|차원 테이블]] 비정규화 → 조인 수 최소화, [[298_qkv_attention|쿼리]] [[484_elt_extract_load_transform|성능 우수]]
- **[[335_snowflake_schema|스노우플레이크 스키마]]([[313_snowflake_schema|Snowflake Schema]])**: [[273_dimension_table_analysis_perspective|차원 테이블]] [[093_normalization|정규화]] → 저장 공간 절약, 유지보수 용이

📢 **섹션 요약 비유**: Inmon은 **먼저 도시 전체 설계도 그리기**, Kimball은 **각 동네부터 빠르게 개발하기**다. 어느 쪽이 맞다기보다 상황에 따라 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[334_star_schema|스타 스키마]] 설계 실무 단계

1. **비즈니스 요건 수집**: 분석 질문 목록 (예: "지역별·제품군별 월매출 비교")
2. **세분성 정의**: 팩트의 원자 단위 결정 (개별 거래 라인 vs 일별 집계)
3. **[[273_dimension_table_analysis_perspective|차원 테이블]] 설계**: [[277_scd_slowly_changing_dimension_modeling|SCD]]([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]) 타입 결정
4. **[[210_fact_dimension_table_snowflake_schema|팩트 테이블]] 설계**: 가산적(Additive)·반가산적(Semi-Additive)·비가산적(Non-Additive) 팩트 [[104_classification_analysis|분류]]
5. **집계 [[210_fact_dimension_table_snowflake_schema|팩트 테이블]]**: [[282_performance_tactics|성능]]을 위한 사전 집계 테이블 추가

### 기술사 판단 포인트

1. **마트 증식 위험**: 독립형 마트 남용 시 "분석 스파게티" 발생 → 콘포밍 차원으로 통제
2. **클라우드 [[209_data_warehouse_schema_on_write|DW]] 연계**: [[541_cassandra|Snowflake]]·BigQuery에서 [[334_star_schema|스타 스키마]]는 [[282_performance_tactics|성능]] 최적화의 기본
3. **실시간 마트**: [[217_cdc_binlog_change_capture_debezium|CDC]]([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) + 스트리밍으로 준실시간 마트 구축 가능

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 마트 설계는 **요리 레시피 표준화**와 같다. 각 요리사(부서)가 같은 재료(콘포밍 차원)를 쓰되, 자기 전문 요리(마트)를 만들 수 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| [[298_qkv_attention|쿼리]] 응답 속도 향상 | [[327_hint_handoff|OLTP]] 대비 분석 [[298_qkv_attention|쿼리]] [[489_raid_10_hybrid|10]]~100배 향상 |
| 비즈니스 사용자 셀프 [[090_service_kubernetes_network_load_balancing|서비스]] | SQL/BI 도구로 독립적 분석 가능 |
| 부서 특화 분석 환경 | 판매·재무·HR 각 최적화된 [[014_data_model_components|데이터 모델]] |
| 의사결정 속도 개선 | 임원 리포트 [[087_process_state_transition|생성]] 시간 수일 → 실시간 |

### 결론

[[001_dikw_pyramid|데이터]] 마트와 Kimball의 [[334_star_schema|스타 스키마]]는 **분석의 민주화**를 실현하는 핵심 도구다. 비정규화된 차원 모델은 복잡한 [[001_dikw_pyramid|데이터]] 엔지니어링 없이도 비즈니스 사용자가 다차원 분석을 수행할 수 있게 한다. 그러나 콘포밍 차원과 전사 거버넌스 없이는 마트 증식이 [[001_dikw_pyramid|데이터]] 불일치로 이어지므로, [[312_kimball|Kimball]] 방법론의 [[344_bus|버스]] 아키텍처([[344_bus|Bus]] [[319_architecture|Architecture]]) 원칙 준수가 필수다.

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 마트의 [[334_star_schema|스타 스키마]]는 **각 팀 전용 분석 대시보드**다. 공통 [[001_dikw_pyramid|데이터]](콘포밍 차원)를 공유하면서도 각 팀이 원하는 분석 뷰를 쉽게 만들 수 있다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 설계 방법론 | [[312_kimball|Kimball]] [[118_dimensional_modeling_star_schema|차원 모델링]] | [[334_star_schema|스타 스키마]] 기반 [[403_bottom_up_integration|Bottom-Up]] 접근 |
| 핵심 구조 | [[334_star_schema|스타 스키마]] | 팩트+차원 비정규화 구조 |
| 확장 [[005_schema|스키마]] | [[335_snowflake_schema|스노우플레이크 스키마]] | 차원 [[093_normalization|정규화]] [[288_version_ihl_tos_total_length|버전]] |
| 핵심 테이블 | [[210_fact_dimension_table_snowflake_schema|팩트 테이블]] | 측정값·집계 [[001_dikw_pyramid|데이터]] |
| 핵심 테이블 | [[273_dimension_table_analysis_perspective|차원 테이블]] | 분석 맥락·[[082_attribute_types_er_model|속성]] |
| [[194_consistency_database_integrity|일관성]] 확보 | 콘포밍 차원 | 마트 간 공유 차원 |
| 이력 관리 | [[277_scd_slowly_changing_dimension_modeling|SCD]] ([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]) | 차원 변경 이력 보존 |
| 상위 저장소 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] | 마트의 원천 [[001_dikw_pyramid|데이터]] |

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]] 마트는 **학급별 사물함**이야. 학교 전체 창고([[209_data_warehouse_schema_on_write|DW]])에서 우리 반에 필요한 것만 꺼내 넣어둔 것이지.

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
2. [[334_star_schema|스타 스키마]]는 **별 모양 조직도**야. 가운데 별(팩트)이 "우리가 분석할 것"이고, 주변 행성들(차원)이 "어떤 각도에서 볼지"를 나타내.
3. 같은 날짜 기준을 모든 반이 쓰면 **"이번 달"이 다 같은 의미**가 돼. 그게 콘포밍 차원이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 209 / 258

← **이전**: [[208_data_warehouse_schema_on_write_inmon|208. 데이터 웨어하우스 (Data Warehouse) 스키마 온 라이트 Inmon 설계]]
**다음**: [[210_fact_dimension_table_snowflake_schema|210. 팩트 테이블 (Fact Table)·차원 테이블 (Dimension Table)·스노우플레이크 스키마 (Snowflake Schema)]] →

---
