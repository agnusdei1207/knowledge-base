---
title: 118. 차원 모델링 (Dimensional Modeling) - 스타 스키마·스노우플레이크·팩트/디멘전
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 차원 모델링은 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]])에서 **분석 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]을 극대화**하기 위해, [[001_dikw_pyramid|데이터]]를 **[[210_fact_dimension_table_snowflake_schema|팩트 테이블]](측정값)과 디멘전 테이블(분석 축)**로 구성하는 설계 기법이다.
> 2. **가치**: [[105_third_normal_form_3nf_transitive|3NF]] [[093_normalization|정규화]]는 OLTP에 최적이지만, 분석 [[298_qkv_attention|쿼리]]([[522_group_by|GROUP BY]]·SUM·AVG)에는 JOIN이 과다하여 느리다. 차원 모델링은 **비정규화된 디멘전**으로 JOIN을 최소화하여 **[[298_qkv_attention|쿼리]] 속도를 [[489_raid_10_hybrid|10]]~100배 향상**시킨다.
> 3. **판단 포인트**: **[[334_star_schema|스타 스키마]](팩트 중심 1단계 [[521_join|JOIN]])**와 **[[335_snowflake_schema|스노우플레이크 스키마]](디멘전 [[093_normalization|정규화]], 다단계 [[521_join|JOIN]])**를 구분하고, 현대 컬럼 스토어([[263_storage_compute_separation_bigquery|BigQuery]]·[[541_cassandra|Snowflake]])에서는 [[334_star_schema|스타 스키마]]가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    스타 스키마 구조                                    │
├───────────────────────────────────────────────────────┤
│        [DIM_날짜]                                     │
│            │                                          │
│  [DIM_상품]──[FACT_매출]──[DIM_고객]                  │
│            │                                          │
│        [DIM_매장]                                     │
│                                                       │
│  FACT_매출: 날짜KEY, 상품KEY, 고객KEY, 매장KEY,       │
│            매출액, 수량, 할인액 (측정값)               │
│  DIM_상품: 상품KEY, 상품명, 카테고리, 브랜드 (분석 축)│
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[210_fact_dimension_table_snowflake_schema|팩트 테이블]]은 "무엇이 일어났는가(매출 3만원)"를 기록하고, 디멘전 테이블은 "어디서, 언제, 누가, 무엇을(분석 축)"을 설명한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 팩트 vs 디멘전

| 구분 | [[210_fact_dimension_table_snowflake_schema|팩트 테이블]] | 디멘전 테이블 |
|:---|:---|:---|
| **내용** | 측정값 (매출, 수량) | 분석 축 (날짜, 상품, 고객) |
| **행 수** | 매우 많음 (수억) | 적음 (수천~수만) |
| **키** | FK (디멘전 [[316_reference_pattern_nosql|참조]]) | PK ([[314_surrogate_key|Surrogate Key]]) |
| **변경** | 추가만 (Append) | [[277_scd_slowly_changing_dimension_modeling|SCD]] (Slowly Changing) |

### 스타 vs 스노우플레이크

| 비교 | [[334_star_schema|스타 스키마]] | 스노우플레이크 |
|:---|:---|:---|
| **디멘전** | 비정규화 (1테이블) | [[093_normalization|정규화]] (다단계) |
| **[[521_join|JOIN]]** | **1단계** | 다단계 |
| **[[298_qkv_attention|쿼리]] 속도** | **빠름** | 느림 |
| **중복** | 있음 | 최소 |
| **현대 [[209_data_warehouse_schema_on_write|DW]]** | **표준** | 드물게 사용 |

- **📢 섹션 요약 비유**: [[334_star_schema|스타 스키마]]는 백화점 안내판(한 곳에 모든 정보)이고, 스노우플레이크는 안내판→층별 안내→매장별 안내로 나뉜 체계다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[105_third_normal_form_3nf_transitive|3NF]] ([[327_hint_handoff|OLTP]]) | [[334_star_schema|스타 스키마]] ([[316_olap|OLAP]]) |
|:---|:---|:---|
| **목적** | [[191_transaction_concept_states|트랜잭션]] [[003_integrity|무결성]] | **분석 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** |
| **[[521_join|JOIN]]** | 많음 | **최소** |
| **중복** | 없음 | 허용 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[277_scd_slowly_changing_dimension_modeling|SCD]] ([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]])
- **Type 1**: 덮어쓰기 (이력 없음).
- **Type 2**: 새 행 추가 (이력 보존, 유효 기간).
- **Type 3**: 이전/현재 값 컬럼 (제한된 이력).

---

## Ⅴ. 기대효과 및 결론

| 지표 | [[105_third_normal_form_3nf_transitive|3NF]] 분석 | [[334_star_schema|스타 스키마]] | 개선 |
|:---|:---|:---|:---|
| [[298_qkv_attention|쿼리]] 속도 | 느림 (다단 [[521_join|JOIN]]) | **빠름 (1단 [[521_join|JOIN]])** | [[489_raid_10_hybrid|10]]~100× |
| 사용자 이해 | 어려움 | **직관적** | 셀프 [[090_service_kubernetes_network_load_balancing|서비스]] BI |

차원 모델링은 [[312_kimball|Kimball]] 방법론의 핵심이며, 현대 클라우드 [[209_data_warehouse_schema_on_write|DW]]([[263_storage_compute_separation_bigquery|BigQuery]], [[541_cassandra|Snowflake]])에서도 [[334_star_schema|스타 스키마]]가 표준으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[210_fact_dimension_table_snowflake_schema|팩트 테이블]]** | 측정값(매출·수량) 저장 |
| **디멘전 테이블** | 분석 축(날짜·상품·고객) |
| **[[334_star_schema|스타 스키마]]** | 팩트 중심 1단계 [[521_join|JOIN]] |
| **[[277_scd_slowly_changing_dimension_modeling|SCD]]** | 디멘전 변경 이력 관리 |
| **[[312_kimball|Kimball]] 방법론** | 차원 모델링의 이론적 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ER 모델 3NF (OLTP, 1970s)]
    │
    ▼
[Kimball 차원 모델링 (1996) — 스타 스키마·팩트/디멘전]
    │
    ▼
[스노우플레이크 스키마 (디멘전 정규화 변형)]
    │
    ▼
[컬럼 스토어 DW (BigQuery, 2010s) — 스타 스키마 최적]
    │
    ▼
[현재: dbt + 스타 스키마 — 분석 엔지니어링 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[210_fact_dimension_table_snowflake_schema|팩트 테이블]]은 "가게에서 **무엇이 일어났는지**(매출 3만원)"를 기록하는 일지예요.
2. 디멘전 테이블은 "**어디서, 언제, 누가** 샀는지"를 설명하는 사전이에요.
3. [[334_star_schema|스타 스키마]]는 일지와 사전을 **별(Star) 모양으로 연결**해서 빠르게 분석할 수 있게 한 거예요!
