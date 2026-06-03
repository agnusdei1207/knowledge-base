+++
title = "210. 팩트 테이블 (Fact Table)·차원 테이블 (Dimension Table)·스노우플레이크 스키마 (Snowflake Schema)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 팩트 테이블(Fact Table)은 측정 가능한 비즈니스 이벤트를 기록하고, [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)([Dimension Table](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/))은 그 이벤트의 맥락(누가·언제·어디서·무엇을)을 제공하며, 둘의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설계 방식이 스타 vs [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/)를 결정한다.
> 2. **가치**: [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/)([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 차원의 역사적 변화를 추적하면, 과거 특정 시점의 비즈니스 상태를 정확하게 재현할 수 있어 이력 분석의 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)을 보장한다.
> 3. **판단 포인트**: [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 우선)와 [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/)([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)·유지보수 우선) 중 선택은 조직의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴과 스토리지 비용 트레이드오프에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

### 팩트 테이블 정의

팩트 테이블은 비즈니스 프로세스에서 발생한 <strong>측정 가능한 사실(Fact)</strong>을 저장하는 테이블이다.

<strong>팩트의 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>:</strong>
- **가산적 팩트(Additive Fact)**: 모든 차원에서 합산 가능 (예: 매출액, 수량)
- **반가산적 팩트(Semi-Additive Fact)**: 일부 차원에서만 합산 가능 (예: 계좌 잔액 - 시간 차원 합산 불가)
- **비가산적 팩트(Non-Additive Fact)**: 합산 불가 (예: 비율, 퍼센트)

### [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) 정의

[차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)은 팩트를 <strong>해석하기 위한 맥락</strong>을 제공하는 테이블이다.

- **DimDate**: 날짜, 월, 분기, 연도, 공휴일 여부 등
- **DimC고객**: 고객 이름, 주소, 세그먼트, 등록일 등
- **DimProduct**: 제품명, 카테고리, 브랜드, 가격 등

📢 **섹션 요약 비유**: 팩트 테이블은 <strong>가계부의 금액</strong>이고, [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)은 <strong>그 지출의 날짜·장소·카테고리</strong>다. 금액만 있으면 아무 의미가 없고, 맥락이 있어야 분석이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) vs [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/)

```
  ── 스타 스키마 ──          ── 스노우플레이크 스키마 ──

  DimDate                    DimDate
     │                          │
  DimCustomer──FactSales──DimProduct       DimCategory
     │             │                          │
  DimStore     DimCustomer──FactSales──DimProduct──DimBrand
                   │             │
               DimCity        DimStore
                │                 │
            DimRegion          DimCity─DimRegion
```

| 항목 | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) | [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/) |
|:---|:---|:---|
| <strong>차원 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a></strong> | 비정규화(Denormalized) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(Normalized) |
| **조인 횟수** | 적음 (팩트↔차원 1단계) | 많음 (다단계 조인) |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 빠름 | 느릴 수 있음 |
| **저장 공간** | 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 더 큼 | 중복 제거로 작음 |
| **유지보수** | 차원 수정 시 전체 갱신 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 변경 용이 |
| **이해하기 쉬움** | 매우 간단 | 복잡함 |
| **적합 케이스** | 분석 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 중요 | 차원 재사용·정합성 중요 |

### [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) ([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) 타입

차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 시간에 따라 변할 때의 처리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/):

```
SCD 유형 비교
┌─────────┬──────────────────────────────────────────────────────┐
│  타입   │  설명                                                 │
├─────────┼──────────────────────────────────────────────────────┤
│ Type 0  │ 변경 무시 (정적 차원)                                  │
├─────────┼──────────────────────────────────────────────────────┤
│ Type 1  │ 덮어쓰기 - 이전 값 소실, 이력 없음                    │
│         │ 예: 오타 수정, 참조 데이터 갱신                        │
├─────────┼──────────────────────────────────────────────────────┤
│ Type 2  │ 신규 행 추가 - 이력 완전 보존                          │
│         │ 서로게이트 키(Surrogate Key) + 유효기간(Start/End Date) │
│         │ 예: 고객 주소 변경, 조직 개편                           │
├─────────┼──────────────────────────────────────────────────────┤
│ Type 3  │ 별도 컬럼 추가 - 현재+이전 값만 보존                  │
│         │ 예: Previous_Region, Current_Region                  │
├─────────┼──────────────────────────────────────────────────────┤
│ Type 6  │ Type 1+2+3 복합 (Hybrid SCD)                        │
└─────────┴──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 2는 <strong>여권 갱신 기록</strong>과 같다. 새 여권을 발급받아도 이전 여권 정보(주소, 사진)가 기록 안에 남아 있다.

---

## Ⅲ. 비교 및 연결

### [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) ([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/))

[차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)의 기본 키로, 소스 시스템의 자연 키(Natural [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))와 별개로 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서 생성하는 대리 키.

**필요성:**
- 소스 시스템 키 변경에 독립적 (예: 고객 번호 체계 변경)
- [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 2에서 동일 고객의 여러 버전을 구별
- 정수형 작은 키로 조인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상

**예시:** `customer_id (소스 자연키: C001)` → `customer_key (서로게이트키: 10023)`

### [팩트리스 팩트 테이블](/knowledge-base/studynote/05_database/04_transactions_concurrency/576_factless_fact_table_event_tracking_coverage/) ([Factless Fact Table](/knowledge-base/studynote/05_database/04_transactions_concurrency/576_factless_fact_table_event_tracking_coverage/))

측정값 없이 이벤트 발생 자체를 기록하는 테이블:
- 예: "학생이 수업에 출석했다" - 출석 수(COUNT)를 팩트로 표현
- 예: "프로모션 대상 제품 목록" - 커버리지 분석용

📢 **섹션 요약 비유**: [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/)는 <strong>주민등록번호와 달리 회사가 직접 발행하는 사원증 번호</strong>다. 외부 번호가 바뀌어도 내부 번호는 유지된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 팩트 테이블 설계 모범 사례

1. **세분성(Grain) 명확히**: "하나의 행 = 하나의 주문 라인 아이템" 명세
2. <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/">서로게이트 키</a>만 FK로 사용</strong>: 자연 키 직접 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 금지
3. **축퇴 차원(Degenerate Dimension)**: [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) 없이 팩트에 포함 (예: 주문번호, 송장번호)
4. **날짜 차원 반드시 포함**: [시계열 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/341_time_series_ar_ma_arma/) 기본 요건

### 기술사 판단 포인트

1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/315_scd_type_2/">SCD Type 2</a> 선택 기준</strong>: 고객 세그먼트 변경, 지역 재편, 제품 카테고리 변경 시 필수
2. **스타 vs 스노우플레이크**: BI 도구([Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/)·[Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/)) 사용 환경 → 스타 선호; [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 중요 → 스노우플레이크 고려
3. **현대 컬럼 스토어**: [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)·Snowflake에서는 비정규화가 오히려 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 유리

📢 **섹션 요약 비유**: [SCD Type 2](/knowledge-base/studynote/12_it_management/05_security_compliance/315_scd_type_2/) 설계는 <strong>이사 때마다 주소록 새 줄을 추가</strong>하는 것이다. 덮어쓰면 예전 주소로 보낸 편지 이력이 사라지지만, 새 줄을 추가하면 언제 어디 살았는지 다 남는다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 설명 |
|:---|:---|
| 이력 분석 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) | [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 2로 과거 어느 시점 [상태도](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/065_state_diagram/) 재현 가능 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 | 비정규화 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)로 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 고속 처리 |
| BI 도구 친화성 | 단순한 스타 구조로 [Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/)·[Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) 직관적 활용 |
| 확장 용이성 | 새 차원·팩트 추가 시 기존 구조 영향 최소화 |

### 결론

팩트 테이블과 [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 그리고 스타/[스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/) 선택은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 웨어하우스의 <strong>분석 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>과 유지보수성의 균형</strong>을 결정한다. [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 단순한 기술 선택이 아니라 비즈니스의 이력 분석 요건을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델로 구현하는 핵심 의사결정이다. 기술사 논술에서는 각 선택의 <strong>비즈니스 근거</strong>를 명확히 제시할 수 있어야 한다.

📢 **섹션 요약 비유**: 팩트·차원 설계는 <strong>영화 제작</strong>과 같다. 팩트(이벤트)는 주인공의 행동이고, 차원(맥락)은 배경, 시간대, 등장인물이다. 두 요소가 조화로워야 이야기가 완성된다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 구조 | 팩트 테이블 | 측정값·이벤트 중심 테이블 |
| 핵심 구조 | [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) | 분석 맥락·[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 테이블 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 패턴 | [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) | 비정규화, 단순·고성능 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 패턴 | [스노우플레이크 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/335_snowflake_schema/) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 유지보수 용이 |
| 이력 관리 | [SCD Type 2](/knowledge-base/studynote/12_it_management/05_security_compliance/315_scd_type_2/) | 변경 이력 완전 보존 |
| 키 설계 | [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부 대리 키 |
| 특수 팩트 | [팩트리스 팩트 테이블](/knowledge-base/studynote/05_database/04_transactions_concurrency/576_factless_fact_table_event_tracking_coverage/) | 이벤트 발생 자체 기록 |
| 분석 처리 | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 드릴다운/[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) | 다차원 집계 탐색 |

### 👶 어린이를 위한 3줄 비유 설명

1. 팩트 테이블은 <strong>장난감 가게의 판매 영수증</strong>이야. 얼마짜리 어떤 장난감을 몇 개 샀는지 기록해.

### 📈 관련 키워드 및 발전 흐름도

```text
비정규화된 단일 테이블 (분석 비효율)
    │
    ▼
차원 모델링
    ├─► Fact Table: 측정값 (매출 · 수량 · 비용)
    └─► Dimension Table: 속성 (날짜 · 제품 · 고객)
    │
    ▼
Star Schema: 팩트 중심 1단계 조인
    │
    ▼
Snowflake Schema: 차원 정규화 (3NF)
    │
    ▼
SCD (Slowly Changing Dimension): Type 1/2/3
```
2. [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)은 <strong>장난감 설명서</strong>야. 그 장난감이 뭔지, 누가 샀는지, 언제 샀는지 자세히 설명해줘.
3. SCD는 <strong>고객 주소가 바뀌어도 예전 주소도 기억하는 것</strong>이야. 그래서 작년에 어디 살았는지도 알 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 210 / 258

← **이전**: [209. 데이터 마트 (Data Mart) Kimball 다차원 분석 스타 스키마 (Star Schema)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/)
**다음**: [211. OLAP (Online Analytical Processing) 드릴다운·롤업·서로게이트 키](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/) →

---
