---
title: 151. 다중 계층 아키텍처 (Multi-Tier Architecture) — Bronze/Silver/Gold
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. 다중 계층 아키텍처는 [[208_data_lake_schema_on_read|데이터 레이크]]를 **Bronze(원시)·Silver(정제)·Gold(집계)** 3계층으로 나누어 [[001_dikw_pyramid|데이터]] 품질과 변환 이력을 단계별로 관리하는 설계 패턴이다.
2. 각 계층은 소비자가 다르며, Bronze는 [[001_dikw_pyramid|데이터]] 엔지니어, Silver는 [[001_dikw_pyramid|데이터]] 과학자, Gold는 BI 분석가와 비즈니스 의사결정자를 위한 [[001_dikw_pyramid|데이터]]를 제공한다.
3. 계층 간 [[001_dikw_pyramid|데이터]] 변환은 **증분 처리(Incremental Processing)**로 운영되어 전체 재처리 없이 새로운 원시 [[001_dikw_pyramid|데이터]]를 효율적으로 하위 계층에 반영한다.

---

## Ⅰ. 개요 및 필요성

[[459_quic_fec_forward_error_correction|초기]] [[208_data_lake_schema_on_read|데이터 레이크]]는 모든 [[001_dikw_pyramid|데이터]]를 단일 저장소에 무분별하게 쌓아 '[[288_data_swamp_metadata_management_absence|데이터 늪]]([[288_data_swamp_metadata_management_absence|Data Swamp]])'이 되는 문제가 있었다. [[001_dikw_pyramid|데이터]] 품질 수준이 뒤섞이면 분석가가 신뢰할 수 있는 [[001_dikw_pyramid|데이터]]를 찾기 어렵고, [[123_pipe|파이프]]라인 장애 시 어느 단계에서 문제가 발생했는지 추적도 힘들다.

다중 계층 아키텍처는 이 문제를 **관심사 분리(Separation of Concerns)** 원칙으로 해결한다. 각 계층이 명확한 [[001_dikw_pyramid|데이터]] 품질 수준과 변환 규칙을 가지며, 장애 시 해당 계층만 재처리하면 된다.

| 계층 | 다른 이름 | 목적 | 소비자 |
|:---|:---|:---|:---|
| Bronze | [[225_raw|Raw]] / Landing | 원시 [[001_dikw_pyramid|데이터]] 보존, [[606_auditing_linux_auditd|감사]] 추적 | [[001_dikw_pyramid|데이터]] 엔지니어 |
| Silver | Cleaned / Refined | 정제·[[395_verification_process_review|검증]]·조인 [[001_dikw_pyramid|데이터]] | [[001_dikw_pyramid|데이터]] 과학자 |
| Gold | Curated / Business | 집계·[[018_kpi|KPI]] 지향 [[001_dikw_pyramid|데이터]] | BI 분석가·경영진 |

> 📢 **섹션 요약 비유**: 광산에서 원석(Bronze)을 캐고, 불순물을 제거하여 금속(Silver)을 만들고, 최종적으로 보석(Gold)으로 가공하는 제련 과정과 같다. 각 단계가 독립적으로 관리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌────────────────────────────────────────────────────────────────┐
│             Multi-Tier Data Lake 아키텍처                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [소스 시스템]                                                  │
│  (DB, 이벤트, API, 파일)                                        │
│          │ 수집 (Kafka / Spark / Airflow)                      │
│          ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🥉 BRONZE LAYER                                          │  │
│  │  - 원시 데이터 그대로 저장 (스키마 변경 없음)               │  │
│  │  - append-only (삭제·수정 없음)                            │  │
│  │  - 수집 타임스탬프 메타데이터 추가                          │  │
│  │  예: s3://datalake/bronze/orders/2026/04/21/              │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │ 변환 (Spark, dbt)                        │
│                     ▼                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🥈 SILVER LAYER                                          │  │
│  │  - 중복 제거, null 처리, 타입 통일                         │  │
│  │  - 테이블 조인, 비즈니스 키 정의                            │  │
│  │  - SCD (Slowly Changing Dimension) 적용                   │  │
│  │  예: Delta Table: sales.silver.orders_cleaned             │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │ 집계 (Spark SQL, dbt)                    │
│                     ▼                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🥇 GOLD LAYER                                            │  │
│  │  - 비즈니스 지향 집계 테이블 (일별 매출, 고객 LTV 등)       │  │
│  │  - Star/Snowflake 스키마 최적화                            │  │
│  │  - BI 도구 직접 연결                                       │  │
│  │  예: Delta Table: sales.gold.daily_revenue                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                     │                                          │
│            [BI / ML / 분석 소비자]                              │
└────────────────────────────────────────────────────────────────┘
```

**계층별 상세 특성**

| 항목 | Bronze | Silver | Gold |
|:---|:---|:---|:---|
| [[005_schema|스키마]] 방식 | [[009_schema_on_read|Schema-on-Read]] | 고정 [[005_schema|스키마]] | 고정 [[005_schema|스키마]] (집계형) |
| [[001_dikw_pyramid|데이터]] [[289_cqrs_db|쓰기]] | Append-only | Merge/Upsert | Overwrite/Merge |
| 보존 기간 | 장기 (수 년) | 중기 (수 개월) | 단기 (최신 집계) |
| [[514_partition_slice_volume|파티션]] 기준 | 수집 날짜 | 비즈니스 날짜 | 분석 기간 |
| 품질 [[085_sla|SLA]] | 없음 (원본 그대로) | 중간 ([[395_verification_process_review|검증]] 완료) | 높음 (비즈니스 [[018_kpi|KPI]]) |

> 📢 **섹션 요약 비유**: Bronze는 냉장고 채소 칸(신선 재료), Silver는 손질된 재료, Gold는 완성된 요리다. 요리(Gold)가 잘못됐을 때 재료(Bronze)부터 다시 추적할 수 있다.

---

## Ⅲ. 비교 및 연결

**2-계층 vs 3-계층 vs 4-계층**

| 항목 | 2-계층 ([[225_raw|Raw]]+Curated) | 3-계층 (B/S/G) | 4-계층 (+Archive) |
|:---|:---|:---|:---|
| 관리 복잡도 | 낮음 | 중간 | 높음 |
| 문제 추적성 | 어려움 | 좋음 | 매우 좋음 |
| 재처리 단위 | 전체 또는 반 | 계층 단위 | 계층+[[288_version_ihl_tos_total_length|버전]] 단위 |
| 적합 규모 | 소규모 | 중대규모 | 대규모 엔터프라이즈 |

**연관 기술 연결**

- **[[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]]**: Databricks에서 Bronze/Silver/Gold를 Delta Lake로 구현한 공식 패턴
- **dbt ([[001_dikw_pyramid|data]] build tool)**: Silver→Gold 변환을 SQL로 선언적 구현
- **AutoLoader**: Bronze 계층에 신규 [[501_file_definition_logical_record|파일]] 자동 적재
- **[[270_data_quality_great_expectations|Data Quality]] 도구 (Great Expectations, Soda)**: Silver 계층 진입 시 품질 검사

> 📢 **섹션 요약 비유**: 3계층 아키텍처는 공항 보안 검색대와 같다. 여권 검사(Bronze), 보안 검색(Silver), 탑승 게이트(Gold) 순으로 단계를 거치면서 문제 승객(불량 [[001_dikw_pyramid|데이터]])을 각 단계에서 걸러낸다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Bronze 계층 설계 원칙**
- 원본 [[001_dikw_pyramid|데이터]] 절대 수정 금지 (Immutability)
- 수집 타임스탬프(`_ingested_at`), 소스 시스템 ID [[012_metadata|메타데이터]] 필수 추가
- [[514_partition_slice_volume|파티션]]: 수집 연월일 기준 (재처리 용이)

**Silver 계층 핵심 변환**
- 중복 제거: `ROW_NUMBER() OVER (PARTITION BY pk ORDER BY updated_at DESC) = 1`
- [[315_scd_type_2|SCD Type 2]]: 이력 관리를 위한 `valid_from`, `valid_to`, `is_current` 컬럼
- [[001_dikw_pyramid|데이터]] 품질 게이트: NULL 비율, 이상값 범위 검사 통과 후 진입

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 각 계층 존재 이유 | 관심사 분리로 품질 수준·소비자·[[085_sla|SLA]] 독립 관리 |
| Bronze append-only 이유 | 원본 보존으로 언제든 재처리 가능, [[606_auditing_linux_auditd|감사]] 추적 보장 |
| Silver에서 [[277_scd_slowly_changing_dimension_modeling|SCD]] 적용 이유 | 천천히 변하는 [[539_mdm_master_data_management|마스터 데이터]](고객, 제품) 이력 보존 |
| Gold 집계 [[268_strategy_pattern|전략]] | Star [[005_schema|스키마]]로 BI [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] 최적화 |

> 📢 **섹션 요약 비유**: 3계층 설계는 음식점 주방 구조와 같다. 냉장 창고(Bronze)는 원재료 그대로, 조리 준비실(Silver)은 손질 완료, [[090_service_kubernetes_network_load_balancing|서비스]] [[059_counter|카운터]](Gold)는 즉시 제공 가능한 상태다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] 품질 관리 | 계층별 품질 게이트로 불량 [[001_dikw_pyramid|데이터]] 하위 전파 차단 |
| 재처리 효율 | 장애 시 해당 계층만 재처리 (전체 재처리 불필요) |
| 소비자 경험 향상 | 목적별 최적화된 계층 제공 (BI, ML, 분석 분리) |
| [[606_auditing_linux_auditd|감사]] 추적 | Bronze 원본 보존으로 규제 [[606_auditing_linux_auditd|감사]] 대응 가능 |

Multi-Tier Architecture는 현대 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]의 핵심 설계 원칙으로, [[074_photon_engine|Databricks]] Medallion Architecture로 표준화되어 있다. 기술사 시험에서는 **각 계층의 역할과 소비자 분리**, **Bronze의 append-only 원칙**, **Silver의 품질 변환([[277_scd_slowly_changing_dimension_modeling|SCD]]·중복 제거)**이 핵심 논점이다.

> 📢 **섹션 요약 비유**: 다중 계층은 물 정수 시스템과 같다. 강물(Bronze)→ 1차 여과(Silver)→ 정수 완료(Gold) 단계를 거치면서 각 단계의 물 품질이 명확히 보장되고, 오염 단계를 즉시 특정할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Bronze | 원시 계층 | append-only, 원본 보존 |
| Silver | 정제 계층 | 중복 제거, [[277_scd_slowly_changing_dimension_modeling|SCD]], 품질 검사 |
| Gold | 집계 계층 | BI/[[018_kpi|KPI]] 최적화, Star [[005_schema|스키마]] |
| [[315_scd_type_2|SCD Type 2]] | Silver 변환 기법 | 이력 보존형 천천히 변하는 차원 |
| AutoLoader | Bronze 수집 도구 | 신규 [[501_file_definition_logical_record|파일]] 자동 감지·Delta 적재 |
| Great Expectations | 품질 도구 | Silver 진입 전 [[001_dikw_pyramid|데이터]] 품질 검사 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 스토리지 한계]
    │
    ▼
[Hot/Warm/Cold 티어 분류]
    │
    ▼
[멀티 티어 아키텍처]
    │
    ▼
[자동 라이프사이클 정책]
    │
    ▼
[비용 최적화]
```

멀티 티어 아키텍처는 Hot/Warm/Cold 티어와 라이프사이클 [[164_policy|정책]]으로 비용을 최적화한다.

### 👶 어린이를 위한 3줄 비유 설명
1. Bronze는 슈퍼에서 사온 야채 그대로, Silver는 씻고 잘라놓은 재료, Gold는 다 만든 요리예요.
2. 요리(Gold)가 맛없을 때 재료(Bronze)를 다시 보면 어디서 문제가 생겼는지 알 수 있어요.
3. 각 단계가 분리되어 있어서 재료 손질(Silver)을 잘못해도 슈퍼에서 사온 야채(Bronze)는 그대로 보존돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 151 / 262

← **이전**: [[150_unity_catalog|150. Unity Catalog (Databricks) — 레이크하우스 통합 거버넌스]]
**다음**: [[152_medallion_architecture|152. 메달리온 아키텍처 (Medallion Architecture) — Delta Lake 기반 3계층]] →

---
