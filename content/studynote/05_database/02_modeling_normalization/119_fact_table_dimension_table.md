+++
title = "119. 팩트 테이블과 디멘전 테이블 (Fact & Dimension Table) - DW 스타 스키마 핵심 구성 요소"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)은 <strong>비즈니스 이벤트의 측정값(매출액·수량·클릭 수)</strong>을 저장하는 대용량 테이블이고, 디멘전 테이블은 <strong>분석 축(날짜·상품·고객·지역)</strong>의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 저장하는 마스터 테이블이다.
> 2. **가치**: "2024년 1월 서울 매장의 전자제품 매출"을 분석할 때, 팩트(매출)에 디멘전(날짜·지역·카테고리)을 <strong>JOIN하면 자유로운 다차원 분석(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a> Cube)</strong>이 가능하다.
> 3. **판단 포인트**: 팩트 유형([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·Periodic·Accumulating [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/))과 디멘전 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)([SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 1/2/3)를 정확히 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    팩트 테이블 구조                                    │
├───────────────────────────────────────────────────────┤
│  FACT_매출                                            │
│  ┌─────────┬─────────┬─────────┬──────┬──────┐       │
│  │ 날짜KEY  │ 상품KEY  │ 고객KEY  │ 매출액│ 수량 │       │
│  ├─────────┼─────────┼─────────┼──────┼──────┤       │
│  │ 20240101│ P001    │ C100    │30000 │  2   │       │
│  │ 20240101│ P002    │ C101    │15000 │  1   │       │
│  └─────────┴─────────┴─────────┴──────┴──────┘       │
│  FK(날짜KEY) → DIM_날짜                               │
│  FK(상품KEY) → DIM_상품                               │
│  FK(고객KEY) → DIM_고객                               │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 팩트는 "무슨 일이 일어났는가(숫자)"이고, 디멘전은 "그 일의 맥락(누가·언제·어디서·무엇을)"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) 유형

| 유형 | 설명 | 예 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">Transaction</a></strong> | 이벤트 발생 시마다 1행 | 주문·클릭 |
| <strong>Periodic <a href="/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/">Snapshot</a></strong> | 정해진 주기로 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) | 월말 재고·잔액 |
| <strong>Accumulating <a href="/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/">Snapshot</a></strong> | 프로세스 전체 추적 | 주문→배송→반품 |

### [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) ([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) 유형

| Type | 방법 | 이력 |
|:---|:---|:---|
| **Type 1** | 덮어쓰기 | 없음 |
| **Type 2** | 새 행 + 유효기간 | **보존** |
| **Type 3** | 이전/현재 컬럼 | 제한적 |

- **📢 섹션 요약 비유**: [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 2는 "이사 기록"이다. 서울→부산 이사 시 서울 행(만료)과 부산 행(현재)을 모두 유지한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/) | 디멘전 테이블 |
|:---|:---|:---|
| **내용** | 측정값 (숫자) | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) (텍스트) |
| **행 수** | 수억 | 수천~수만 |
| **변경** | Append (추가) | [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) (갱신) |
| **키** | FK (디멘전 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)) | PK ([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/)) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/) vs Natural [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)
- <strong>Natural <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a></strong> (상품코드 "P001"): 비즈니스 의미 있음, 변경 가능.
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/">Surrogate Key</a></strong> (자동증가 정수): [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부 전용, <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/">SCD</a> Type 2에 필수</strong>.

---

## Ⅴ. 기대효과 및 결론

팩트/디멘전 분리 설계는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 분석의 기본이며, 현대 클라우드 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))에서도 이 패턴이 표준으로 사용된다. dbt([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool)가 팩트/디멘전 모델 자동 생성을 지원한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/">스타 스키마</a></strong> | 팩트 중심 + 1단 디멘전 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/">SCD</a></strong> | 디멘전 변경 이력 관리 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/">Surrogate Key</a></strong> | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 디멘전의 내부 PK |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a> Cube</strong> | 팩트+디멘전으로 구성하는 다차원 분석 |
| **dbt** | 팩트/디멘전 모델 자동 [빌드 도구](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/070_build_tools_maven_gradle_npm/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[ER 모델 3NF (OLTP)]
    │
    ▼
[Kimball 차원 모델링 (1996) — 팩트/디멘전 분리]
    │
    ▼
[SCD Type 2 (이력 보존 표준)]
    │
    ▼
[클라우드 DW (BigQuery, 2010s) — 스타 스키마 최적화]
    │
    ▼
[현재: dbt + 팩트/디멘전 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)은 "가게 매출 일지"예요. **얼마를 벌었는지** 숫자를 기록해요.
2. 디멘전 테이블은 "누가, 언제, 어디서, 무엇을"이라는 <strong>맥락 사전</strong>이에요.
3. 일지와 사전을 합치면 "서울 매장에서 1월에 전자제품이 얼마나 팔렸는지" <strong>다차원 분석</strong>이 가능해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 119 / 600

← **이전**: [118. 차원 모델링 (Dimensional Modeling) - 스타 스키마·스노우플레이크·팩트/디멘전](/knowledge-base/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/)
**다음**: [120. 데이터 역공학 (Data Reverse 엔진ering) - 기존 DB에서 ERD·모델 복원](/knowledge-base/studynote/05_database/02_modeling_normalization/120_data_reverse_engineering/) →

---
