+++
weight = 211
title = "211. OLAP (Online Analytical Processing) 드릴다운·롤업·서로게이트 키"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[316_olap|OLAP]](Online Analytical Processing)는 다차원 [[001_dikw_pyramid|데이터]] 큐브를 통해 대규모 [[001_dikw_pyramid|데이터]]를 다양한 관점에서 빠르게 집계·분석하는 기술로, [[327_hint_handoff|OLTP]](Online [[191_transaction_concept_states|Transaction]] Processing)의 행(Row) 중심과 달리 열(Column)·차원(Dimension) 중심의 읽기 최적화 구조다.
> 2. **가치**: 드릴다운(Drill-Down)·[[042_rollup_l2_solution|롤업]]([[330_olap_rollup_drilldown|Roll-Up]])·[[331_neuromorphic_ai_db|슬라이스]]([[331_neuromorphic_ai_db|Slice]])·다이스(Dice) 연산으로 [[282_business_intelligence_bi_technology_framework|비즈니스 인텔리전스]](BI, Business Intelligence) 분석가가 억 건 [[001_dikw_pyramid|데이터]]를 수초 내에 탐색하며, [[276_surrogate_key_artificial_identifier|서로게이트 키]]([[314_surrogate_key|Surrogate Key]])로 [[273_dimension_table_analysis_perspective|차원 테이블]]의 변경 이력을 추적한다.
> 3. **판단 포인트**: [[336_molap|MOLAP]]([[336_molap|Multidimensional OLAP]])은 사전 집계로 속도가 빠르나 공간 낭비가 크고, [[337_rolap|ROLAP]]([[337_rolap|Relational OLAP]])은 유연하나 느리다 — [[001_dikw_pyramid|데이터]] 규모·갱신 빈도·[[298_qkv_attention|쿼리]] 패턴으로 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[294_oltp_vs_olap|OLTP vs OLAP]] — 두 세계의 설계 철학 차이

| 항목 | [[327_hint_handoff|OLTP]] (Online [[191_transaction_concept_states|Transaction]] Processing) | [[316_olap|OLAP]] (Online Analytical Processing) |
|:---|:---|:---|
| **목적** | 실시간 [[191_transaction_concept_states|트랜잭션]] 처리 | 다차원 집계 분석 |
| **[[298_qkv_attention|쿼리]] 유형** | INSERT / UPDATE / DELETE 단건 | [[520_select|SELECT]] 집계, 복잡 [[521_join|JOIN]] |
| **[[001_dikw_pyramid|데이터]] 크기** | GB 단위, 최신 [[001_dikw_pyramid|데이터]] | TB~PB 단위, 히스토리 포함 |
| **[[093_normalization|정규화]]** | [[105_third_normal_form_3nf_transitive|3NF]] 이상 높은 [[093_normalization|정규화]] | 비정규화(스타·스노우플레이크) |
| **[[138_response_time|응답 시간]]** | ms 이하 | 초~분 단위 |
| **대표 시스템** | MySQL, PostgreSQL | [[541_cassandra|Snowflake]], Redshift, [[263_storage_compute_separation_bigquery|BigQuery]] |

OLTP는 빠른 [[289_cqrs_db|쓰기]]를 위해 [[001_dikw_pyramid|데이터]]를 잘게 쪼개 중복을 제거하지만, OLAP은 집계 성능을 위해 의도적으로 비정규화([[111_denormalization_performance_tradeoff|Denormalization]])하여 [[521_join|JOIN]] 횟수를 줄인다.

### 1.2 다차원 [[014_data_model_components|데이터 모델]] (Multidimensional [[014_data_model_components|Data Model]])

OLAP의 핵심은 **[[001_dikw_pyramid|데이터]] 큐브([[001_dikw_pyramid|Data]] Cube)** — 측정값(Measure)을 여러 차원(Dimension)의 교차점에 배치한 구조다.

```
          제품 차원
          ┌──────────────┐
시간 차원  │  매출 큐브   │  지역 차원
    ──────►│  [날짜][제품]│◄──────
          │  [지역][금액]│
          └──────────────┘
```

- **측정값(Measure)**: 매출액, 수량, 이익률 등 집계 대상 숫자
- **차원(Dimension)**: 분석 관점 — 시간, 제품, 지역, 고객
- **계층(Hierarchy)**: 연도→분기→월→일, 국가→시도→시군구

📢 **섹션 요약 비유**: OLAP은 거대한 루빅스 큐브다 — 회사 전체 매출이라는 큐브를 시간·제품·지역 축으로 돌리면서 원하는 단면만 꺼내 보는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[316_olap|OLAP]] 유형 비교

| 유형 | 전체 명칭 | 저장 방식 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| **[[337_rolap|ROLAP]]** | [[337_rolap|Relational OLAP]] | [[083_relationship_in_er_model|관계]]형 DB 테이블 | 유연, 대용량 | [[298_qkv_attention|쿼리]] 느림 |
| **[[336_molap|MOLAP]]** | [[336_molap|Multidimensional OLAP]] | 다차원 큐브 [[501_file_definition_logical_record|파일]] | [[148_5g_embb_urllc_mmtc|초고속]] 집계 | 공간 낭비, 희소성 문제 |
| **[[338_holap|HOLAP]]** | [[338_holap|Hybrid OLAP]] | 세부→RDB, 집계→큐브 | 균형 | 복잡한 관리 |

### 2.2 [[334_star_schema|스타 스키마]] ([[296_star_schema|Star Schema]]) 구조

```
             ┌─────────────────┐
             │  DIM_시간       │
             │  surrogate_key  │
             │  날짜/월/분기   │
             └────────┬────────┘
                      │
┌─────────────┐  ┌────┴──────────────┐  ┌─────────────┐
│  DIM_제품   │  │  FACT_매출        │  │  DIM_지역   │
│ product_sk  ├──┤  time_sk          ├──┤ region_sk   │
│ 제품명/카테 │  │  product_sk       │  │ 도시/국가   │
└─────────────┘  │  region_sk        │  └─────────────┘
                 │  customer_sk      │
                 │  매출액 / 수량    │
                 └───────────────────┘
                         │
             ┌───────────┴──────────┐
             │  DIM_고객            │
             │  customer_sk         │
             │  고객명/등급/연령대  │
             └──────────────────────┘
```

### 2.3 [[276_surrogate_key_artificial_identifier|서로게이트 키]] ([[314_surrogate_key|Surrogate Key]])

**[[276_surrogate_key_artificial_identifier|서로게이트 키]]([[314_surrogate_key|Surrogate Key]])**는 비즈니스 의미가 없는 시스템 [[087_process_state_transition|생성]] 일련번호(예: 1, 2, 3...)로, [[209_data_warehouse_schema_on_write|DW]]([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]], [[209_data_warehouse_schema_on_write|데이터 웨어하우스]])의 [[273_dimension_table_analysis_perspective|차원 테이블]]에서 자연 키(Natural [[067_db_key_uniqueness_minimality|Key]]) 대신 사용된다.

**왜 필요한가?**

| 문제 상황 | 자연 키의 한계 | [[276_surrogate_key_artificial_identifier|서로게이트 키]] 해법 |
|:---|:---|:---|
| 고객번호 체계 변경 | FK 모두 수정 필요 | SK([[314_surrogate_key|Surrogate Key]])는 불변 |
| [[277_scd_slowly_changing_dimension_modeling|SCD]]([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]) 이력 | 변경 전후 구분 불가 | 버전별 별도 SK 부여 |
| NULL 허용 소스 시스템 | [[521_join|JOIN]] 실패 | Unknown(-1) SK 처리 |
| 소스 통합(멀티소스) | 중복 키 충돌 | 통합 SK로 충돌 방지 |

**[[277_scd_slowly_changing_dimension_modeling|SCD]]([[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]) Type 2** 적용 예:

```
고객_SK  고객_자연키  고객명  등급  시작일      종료일      현재
───────  ──────────  ──────  ────  ──────────  ──────────  ──────
1001     C-00123     홍길동  GOLD  2020-01-01  2022-05-31  N
1002     C-00123     홍길동  VIP   2022-06-01  9999-12-31  Y
```

### 2.4 [[316_olap|OLAP]] 연산 4종

```
┌─────────────────────────────────────────────────────────┐
│  롤업 Roll-Up : 세부 → 요약 (일→월→분기→연도)          │
│  ↑                                                      │
│  드릴다운 Drill-Down : 요약 → 세부 (연도→분기→월→일)   │
│  ↓                                                      │
│  슬라이스 Slice : 한 차원을 고정값으로 필터링           │
│  (예: 지역='서울'로 고정 → 2D 단면 추출)               │
│                                                         │
│  다이스 Dice : 여러 차원을 범위 필터링                  │
│  (예: 지역 IN('서울','부산') AND 월 IN(1,2,3))         │
└─────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [[316_olap|OLAP]] 연산은 지도 앱과 같다 — [[042_rollup_l2_solution|롤업]]은 줌아웃(전국 보기), 드릴다운은 줌인(골목길 보기), [[331_neuromorphic_ai_db|슬라이스]]는 서울만 보기, 다이스는 서울·부산 겨울철만 보기다.

---

## Ⅲ. 비교 및 연결

### 3.1 MDX (Multidimensional Expressions) [[298_qkv_attention|쿼리]]

MDX(Multidimensional Expressions)는 [[316_olap|OLAP]] 큐브를 SQL처럼 조회하는 전용 [[298_qkv_attention|쿼리]] 언어다.

```sql
-- MDX 예: 2024년 서울 지역의 제품 카테고리별 매출 합계
SELECT
  [제품].[카테고리].MEMBERS ON COLUMNS,
  [시간].[년도].[2024] ON ROWS
FROM [매출큐브]
WHERE ([지역].[도시].[서울])
```

- `ON COLUMNS` / `ON ROWS`: 큐브의 축 지정
- `MEMBERS`: 해당 차원의 모든 멤버 전개
- `WHERE`: 슬라이서 — 특정 차원을 고정

### 3.2 [[316_olap|OLAP]] vs 다른 분석 기법

| 기법 | [[001_dikw_pyramid|데이터]] 구조 | 특징 |
|:---|:---|:---|
| [[316_olap|OLAP]] | 다차원 큐브 | 사전 집계, 빠른 드릴다운 |
| SQL 집계 | [[083_relationship_in_er_model|관계]]형 테이블 | 유연하나 집계 속도 한계 |
| 인메모리 BI | 컬럼형 인메모리 | [[165_power_bi|Power BI]], [[164_tableau|Tableau]] — 실시간 |
| [[039_graph_db|Graph DB]] | [[070_graph_datastructure|그래프]] 구조 | [[083_relationship_in_er_model|관계]] 탐색에 특화 |

📢 **섹션 요약 비유**: MDX는 [[316_olap|OLAP]] 큐브의 리모컨이다 — 어느 축에서 볼지, 어느 면을 자를지를 명령하면 큐브가 즉시 원하는 단면을 꺼내 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[209_data_warehouse_schema_on_write|DW]] 설계 시 [[276_surrogate_key_artificial_identifier|서로게이트 키]] [[268_strategy_pattern|전략]]

```
ETL 파이프라인 내 SK 생성 흐름:

소스DB     →  스테이징 영역     →  DW 차원 테이블
고객ID(자)     중복제거/정제         customer_sk(SK)=시퀀스
C-00123    →  C-00123          →  1001
C-00456    →  C-00456          →  1002
```

**실무 [[435_checklist_based_testing|체크리스트]]**:
- SK는 [[215_etl_vs_elt_pipeline|ETL]](Extract, Transform, Load) 레이어에서 자동 증가(IDENTITY/SEQUENCE)로 [[087_process_state_transition|생성]]
- Unknown 멤버(-1, 0)를 [[273_dimension_table_analysis_perspective|차원 테이블]]에 미리 삽입해 NULL FK 처리
- [[277_scd_slowly_changing_dimension_modeling|SCD]] Type 1(덮어쓰기), Type 2(이력 보존), Type 3(이전값 컬럼 추가) [[268_strategy_pattern|전략]]을 비즈니스 요건으로 결정

### 4.2 [[336_molap|MOLAP]] vs [[337_rolap|ROLAP]] 선택 기준

```
데이터 크기가 크고 갱신 빈도가 높다면?
       ↓
  ROLAP or HOLAP

데이터 크기가 작고 쿼리 속도가 최우선이라면?
       ↓
  MOLAP (사전 집계 큐브)

혼합 워크로드라면?
       ↓
  HOLAP (세부 데이터→ROLAP, 집계→MOLAP)
```

📢 **섹션 요약 비유**: MOLAP은 미리 요리해 놓은 도시락(빠르나 메뉴 고정), ROLAP은 즉석 주문 조리(느리나 메뉴 무한대)다. 둘의 장점을 합친 게 HOLAP이다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[316_olap|OLAP]] 도입 효과

| 효과 | 설명 |
|:---|:---|
| **분석 속도** | 집계 사전 계산으로 분 단위 [[298_qkv_attention|쿼리]]를 초 단위로 단축 |
| **셀프 [[090_service_kubernetes_network_load_balancing|서비스]] BI** | 비기술 사용자도 드릴다운/[[042_rollup_l2_solution|롤업]]으로 자율 분석 |
| **일관된 집계 기준** | [[342_routing_metric_hop_bandwidth_delay|메트릭]]([[342_routing_metric_hop_bandwidth_delay|Metric]]) 정의 중앙화로 "매출 기준 불일치" 해소 |
| **히스토리 분석** | SCD와 [[276_surrogate_key_artificial_identifier|서로게이트 키]]로 시점별 [[022_snapshot_backup_architecture|스냅샷]] [[298_qkv_attention|쿼리]] 가능 |

### 5.2 결론 — 기술사 작성 포인트

기술사 시험에서는 "[[316_olap|OLAP]] 연산 4종 + [[276_surrogate_key_artificial_identifier|서로게이트 키]] 필요성 + [[336_molap|MOLAP]]/[[337_rolap|ROLAP]]/[[338_holap|HOLAP]] 비교"를 묶어서 설명하는 것이 고득점 [[268_strategy_pattern|전략]]이다. 특히 **[[276_surrogate_key_artificial_identifier|서로게이트 키]]가 [[277_scd_slowly_changing_dimension_modeling|SCD]] Type 2를 가능하게 하는 메커니즘**을 [[103_ascii|ASCII]] 다이어그램과 함께 논술하면 차별화된다.

📢 **섹션 요약 비유**: [[316_olap|OLAP]] 전체는 회사 경영을 위한 '맞춤 안경'이다 — [[276_surrogate_key_artificial_identifier|서로게이트 키]]가 안경 프레임(구조), 드릴다운/[[042_rollup_l2_solution|롤업]]이 렌즈 조절(초점), MDX가 안경을 쓰고 읽는 책([[298_qkv_attention|쿼리]])이다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| [[316_olap|OLAP]] 저장 방식 | [[337_rolap|ROLAP]] / [[336_molap|MOLAP]] / [[338_holap|HOLAP]] | [[083_relationship_in_er_model|관계]]형·다차원·혼합 저장 |
| [[316_olap|OLAP]] 연산 | 드릴다운·[[042_rollup_l2_solution|롤업]]·[[331_neuromorphic_ai_db|슬라이스]]·다이스 | 다차원 탐색 4종 연산 |
| 차원 설계 | [[276_surrogate_key_artificial_identifier|서로게이트 키]] ([[314_surrogate_key|Surrogate Key]]) | 자연 키 대체, [[277_scd_slowly_changing_dimension_modeling|SCD]] 이력 관리 |
| [[005_schema|스키마]] | 스타 / 스노우플레이크 | 팩트·[[273_dimension_table_analysis_perspective|차원 테이블]] 구조 |
| [[298_qkv_attention|쿼리]] 언어 | MDX (Multidimensional Expressions) | [[316_olap|OLAP]] 전용 [[298_qkv_attention|쿼리]] 언어 |
| 대비 개념 | [[327_hint_handoff|OLTP]] (Online [[191_transaction_concept_states|Transaction]] Processing) | [[289_cqrs_db|쓰기]] 최적화 [[191_transaction_concept_states|트랜잭션]] 처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. OLAP는 마트 매출 장부를 날짜별·지역별·제품별로 뒤집어 볼 수 있는 마법 큐브야 — 어떤 각도로 돌려도 합계가 뚝딱 나온단다.

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP (행 기반 트랜잭션)
    │
    ▼
OLAP: 다차원 분석 (Cube · Drill-Down · Roll-Up)
    ├─► MOLAP: 사전 집계 큐브 (빠름 · 유연성↓)
    ├─► ROLAP: RDBMS 기반 (유연 · 속도↓)
    └─► HOLAP: 혼합 방식
    │
    ▼
Surrogate Key: 비즈니스 키 대체 인조키 (SCD 연동)
    │
    ▼
클라우드 MPP DW: BigQuery · Snowflake (OLAP 현대화)
```
2. 드릴다운은 전국 매출에서 서울, 서울에서 강남, 강남에서 특정 매장으로 점점 깊이 파고드는 거야 — 마치 지도 줌인처럼!
3. [[276_surrogate_key_artificial_identifier|서로게이트 키]]는 고객 번호가 바뀌어도 변하지 않는 '도서관 등록 번호'야 — 이름이 바뀌거나 주소가 바뀌어도 도서관 카드 번호는 그대로지.
