+++
title = "118. 차원 모델링 (Dimensional Modeling) - 스타 스키마·스노우플레이크·팩트/디멘전"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 차원 모델링은 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))에서 <strong>분석 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 극대화</strong>하기 위해, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/">팩트 테이블</a>(측정값)과 디멘전 테이블(분석 축)</strong>로 구성하는 설계 기법이다.
> 2. **가치**: [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 OLTP에 최적이지만, 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)([GROUP BY](/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/)·SUM·AVG)에는 JOIN이 과다하여 느리다. 차원 모델링은 <strong>비정규화된 디멘전</strong>으로 JOIN을 최소화하여 <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 속도를 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>~100배 향상</strong>시킨다.
> 3. **판단 포인트**: <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/">스타 스키마</a>(팩트 중심 1단계 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a>)</strong>와 <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/">스노우플레이크 스키마</a>(디멘전 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>, 다단계 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a>)</strong>를 구분하고, 현대 컬럼 스토어([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)·[Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))에서는 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스타 스키마 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DIM_날짜</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DIM_상품</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">FACT_매출</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">DIM_고객</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DIM_매장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">FACT_매출: 날짜KEY, 상품KEY, 고객KEY, 매장KEY,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">매출액, 수량, 할인액 (측정값)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DIM_상품: 상품KEY, 상품명, 카테고리, 브랜드 (분석 축)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)은 "무엇이 일어났는가(매출 3만원)"를 기록하고, 디멘전 테이블은 "어디서, 언제, 누가, 무엇을(분석 축)"을 설명한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 팩트 vs 디멘전

| 구분 | [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) | 디멘전 테이블 |
|:---|:---|:---|
| **내용** | 측정값 (매출, 수량) | 분석 축 (날짜, 상품, 고객) |
| **행 수** | 매우 많음 (수억) | 적음 (수천~수만) |
| **키** | FK (디멘전 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)) | PK ([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/)) |
| **변경** | 추가만 (Append) | [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) (Slowly Changing) |

### 스타 vs 스노우플레이크

| 비교 | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) | 스노우플레이크 |
|:---|:---|:---|
| **디멘전** | 비정규화 (1테이블) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) (다단계) |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | **1단계** | 다단계 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 속도</strong> | **빠름** | 느림 |
| **중복** | 있음 | 최소 |
| <strong>현대 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a></strong> | **표준** | 드물게 사용 |

- **📢 섹션 요약 비유**: [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 백화점 안내판(한 곳에 모든 정보)이고, 스노우플레이크는 안내판→층별 안내→매장별 안내로 나뉜 체계다.

---

## Ⅲ. 비교 및 연결

| 비교 | [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) ([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) ([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)) |
|:---|:---|:---|
| **목적** | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) | <strong>분석 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 많음 | **최소** |
| **중복** | 없음 | 허용 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) ([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/))
- **Type 1**: 덮어쓰기 (이력 없음).
- **Type 2**: 새 행 추가 (이력 보존, 유효 기간).
- **Type 3**: 이전/현재 값 컬럼 (제한된 이력).

---

## Ⅴ. 기대효과 및 결론

| 지표 | [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) 분석 | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) | 개선 |
|:---|:---|:---|:---|
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 | 느림 (다단 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) | <strong>빠름 (1단 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a>)</strong> | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100× |
| 사용자 이해 | 어려움 | **직관적** | 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) BI |

차원 모델링은 [Kimball](/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/) 방법론의 핵심이며, 현대 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))에서도 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)가 표준으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/">팩트 테이블</a></strong> | 측정값(매출·수량) 저장 |
| **디멘전 테이블** | 분석 축(날짜·상품·고객) |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/">스타 스키마</a></strong> | 팩트 중심 1단계 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/">SCD</a></strong> | 디멘전 변경 이력 관리 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/312_kimball/">Kimball</a> 방법론</strong> | 차원 모델링의 이론적 기반 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">ER 모델 3NF (OLTP, 1970s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Kimball 차원 모델링 (1996) — 스타 스키마·팩트/디멘전</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스노우플레이크 스키마 (디멘전 정규화 변형)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">컬럼 스토어 DW (BigQuery, 2010s) — 스타 스키마 최적</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: dbt + 스타 스키마 — 분석 엔지니어링 자동화</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)은 "가게에서 **무엇이 일어났는지**(매출 3만원)"를 기록하는 일지예요.
2. 디멘전 테이블은 "**어디서, 언제, 누가** 샀는지"를 설명하는 사전이에요.
3. [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)는 일지와 사전을 <strong>별(Star) 모양으로 연결</strong>해서 빠르게 분석할 수 있게 한 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 118 / 600

← **이전**: [117. 물리 데이터베이스 설계 (Physical DB Design) - 인덱스·파티셔닝·스토리지 최적화](/knowledge-base/studynote/05_database/02_modeling_normalization/117_physical_database_design_indexing/)
**다음**: [119. 팩트 테이블과 디멘전 테이블 (Fact & Dimension Table) - DW 스타 스키마 핵심 구성 요소](/knowledge-base/studynote/05_database/02_modeling_normalization/119_fact_table_dimension_table/) →

---
