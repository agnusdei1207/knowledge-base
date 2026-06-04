+++
title = "211. OLAP (Online Analytical Processing) 드릴다운·롤업·서로게이트 키"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)(Online Analytical Processing)는 다차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 큐브를 통해 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다양한 관점에서 빠르게 집계·분석하는 기술로, [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)(Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing)의 행(Row) 중심과 달리 열(Column)·차원(Dimension) 중심의 읽기 최적화 구조다.
> 2. **가치**: 드릴다운(Drill-Down)·[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)([Roll-Up](/knowledge-base/studynote/05_database/06_dw_olap_trends/330_olap_rollup_drilldown/))·[슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)([Slice](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/))·다이스(Dice) 연산으로 [비즈니스 인텔리전스](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/282_business_intelligence_bi_technology_framework/)(BI, Business Intelligence) 분석가가 억 건 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수초 내에 탐색하며, [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/)([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/))로 [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)의 변경 이력을 추적한다.
> 3. **판단 포인트**: [MOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/)([Multidimensional OLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/))은 사전 집계로 속도가 빠르나 공간 낭비가 크고, [ROLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/)([Relational OLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/))은 유연하나 느리다 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모·갱신 빈도·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴으로 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [OLTP vs OLAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) — 두 세계의 설계 철학 차이

| 항목 | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) (Online Analytical Processing) |
|:---|:---|:---|
| **목적** | 실시간 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 | 다차원 집계 분석 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 유형</strong> | INSERT / UPDATE / DELETE 단건 | [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) 집계, 복잡 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기</strong> | GB 단위, 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | TB~PB 단위, 히스토리 포함 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a></strong> | [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) 이상 높은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 비정규화(스타·스노우플레이크) |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a></strong> | ms 이하 | 초~분 단위 |
| **대표 시스템** | MySQL, PostgreSQL | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), Redshift, [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) |

OLTP는 빠른 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 위해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잘게 쪼개 중복을 제거하지만, OLAP은 집계 성능을 위해 의도적으로 비정규화([Denormalization](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/))하여 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 횟수를 줄인다.

### 1.2 다차원 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) (Multidimensional [Data Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/))

OLAP의 핵심은 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 큐브(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Cube)</strong> — 측정값(Measure)을 여러 차원(Dimension)의 교차점에 배치한 구조다.

```
          제품 차원
          +--------------+
시간 차원  |  매출 큐브   |  지역 차원
    ------►|  [날짜][제품]|◄------
          |  [지역][금액]|
          +--------------+
```

- **측정값(Measure)**: 매출액, 수량, 이익률 등 집계 대상 숫자
- **차원(Dimension)**: 분석 관점 — 시간, 제품, 지역, 고객
- **계층(Hierarchy)**: 연도->분기->월->일, 국가->시도->시군구

📢 **섹션 요약 비유**: OLAP은 거대한 루빅스 큐브다 — 회사 전체 매출이라는 큐브를 시간·제품·지역 축으로 돌리면서 원하는 단면만 꺼내 보는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 유형 비교

| 유형 | 전체 명칭 | 저장 방식 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/">ROLAP</a></strong> | [Relational OLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB 테이블 | 유연, 대용량 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 느림 |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/">MOLAP</a></strong> | [Multidimensional OLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/) | 다차원 큐브 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 집계 | 공간 낭비, 희소성 문제 |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/338_holap/">HOLAP</a></strong> | [Hybrid OLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/338_holap/) | 세부->RDB, 집계->큐브 | 균형 | 복잡한 관리 |

### 2.2 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) ([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/)) 구조

```
             +-----------------+
             |  DIM_시간       |
             |  surrogate_key  |
             |  날짜/월/분기   |
             +--------+--------+
                      |
+-------------+  +----+--------------+  +-------------+
|  DIM_제품   |  |  FACT_매출        |  |  DIM_지역   |
| product_sk  +--+  time_sk          +--+ region_sk   |
| 제품명/카테 |  |  product_sk       |  | 도시/국가   |
+-------------+  |  region_sk        |  +-------------+
                 |  customer_sk      |
                 |  매출액 / 수량    |
                 +-------------------+
                         |
             +-----------+----------+
             |  DIM_고객            |
             |  customer_sk         |
             |  고객명/등급/연령대  |
             +----------------------+
```

### 2.3 [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) ([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/))

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/">서로게이트 키</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/">Surrogate Key</a>)</strong>는 비즈니스 의미가 없는 시스템 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 일련번호(예: 1, 2, 3...)로, [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/), [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))의 [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)에서 자연 키(Natural [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 대신 사용된다.

**왜 필요한가?**

| 문제 상황 | 자연 키의 한계 | [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) 해법 |
|:---|:---|:---|
| 고객번호 체계 변경 | FK 모두 수정 필요 | SK([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/))는 불변 |
| [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/)([Slowly Changing Dimension](/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/)) 이력 | 변경 전후 구분 불가 | 버전별 별도 SK 부여 |
| NULL 허용 소스 시스템 | [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 실패 | Unknown(-1) SK 처리 |
| 소스 통합(멀티소스) | 중복 키 충돌 | 통합 SK로 충돌 방지 |

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/">SCD</a>(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/575_scd_slowly_changing_dimension_type_history_management/">Slowly Changing Dimension</a>) Type 2</strong> 적용 예:

```
고객_SK  고객_자연키  고객명  등급  시작일      종료일      현재
-------  ----------  ------  ----  ----------  ----------  ------
1001     C-00123     홍길동  GOLD  2020-01-01  2022-05-31  N
1002     C-00123     홍길동  VIP   2022-06-01  9999-12-31  Y
```

### 2.4 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 연산 4종

```
+---------------------------------------------------------+
|  롤업 Roll-Up : 세부 -> 요약 (일->월->분기->연도)          |
|  ^                                                      |
|  드릴다운 Drill-Down : 요약 -> 세부 (연도->분기->월->일)   |
|  v                                                      |
|  슬라이스 Slice : 한 차원을 고정값으로 필터링           |
|  (예: 지역='서울'로 고정 -> 2D 단면 추출)               |
|                                                         |
|  다이스 Dice : 여러 차원을 범위 필터링                  |
|  (예: 지역 IN('서울','부산') AND 월 IN(1,2,3))         |
+---------------------------------------------------------+
```

📢 **섹션 요약 비유**: [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 연산은 지도 앱과 같다 — [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 줌아웃(전국 보기), 드릴다운은 줌인(골목길 보기), [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)는 서울만 보기, 다이스는 서울·부산 겨울철만 보기다.

---

## Ⅲ. 비교 및 연결

### 3.1 MDX (Multidimensional Expressions) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)

MDX(Multidimensional Expressions)는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 큐브를 SQL처럼 조회하는 전용 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어다.

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

### 3.2 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) vs 다른 분석 기법

| 기법 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 | 특징 |
|:---|:---|:---|
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) | 다차원 큐브 | 사전 집계, 빠른 드릴다운 |
| SQL 집계 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 테이블 | 유연하나 집계 속도 한계 |
| 인메모리 BI | 컬럼형 인메모리 | [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/), [Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/) — 실시간 |
| [Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색에 특화 |

📢 **섹션 요약 비유**: MDX는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 큐브의 리모컨이다 — 어느 축에서 볼지, 어느 면을 자를지를 명령하면 큐브가 즉시 원하는 단면을 꺼내 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 설계 시 [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
ETL 파이프라인 내 SK 생성 흐름:

소스DB     ->  스테이징 영역     ->  DW 차원 테이블
고객ID(자)     중복제거/정제         customer_sk(SK)=시퀀스
C-00123    ->  C-00123          ->  1001
C-00456    ->  C-00456          ->  1002
```

<strong>실무 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>:
- SK는 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract, Transform, Load) 레이어에서 자동 증가(IDENTITY/SEQUENCE)로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- Unknown 멤버(-1, 0)를 [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)에 미리 삽입해 NULL FK 처리
- [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) Type 1(덮어쓰기), Type 2(이력 보존), Type 3(이전값 컬럼 추가) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 비즈니스 요건으로 결정

### 4.2 [MOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/) vs [ROLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/) 선택 기준

```
데이터 크기가 크고 갱신 빈도가 높다면?
       v
  ROLAP or HOLAP

데이터 크기가 작고 쿼리 속도가 최우선이라면?
       v
  MOLAP (사전 집계 큐브)

혼합 워크로드라면?
       v
  HOLAP (세부 데이터->ROLAP, 집계->MOLAP)
```

📢 **섹션 요약 비유**: MOLAP은 미리 요리해 놓은 도시락(빠르나 메뉴 고정), ROLAP은 즉석 주문 조리(느리나 메뉴 무한대)다. 둘의 장점을 합친 게 HOLAP이다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 도입 효과

| 효과 | 설명 |
|:---|:---|
| **분석 속도** | 집계 사전 계산으로 분 단위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 초 단위로 단축 |
| <strong>셀프 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> BI</strong> | 비기술 사용자도 드릴다운/[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)으로 자율 분석 |
| **일관된 집계 기준** | [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)([Metric](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)) 정의 중앙화로 "매출 기준 불일치" 해소 |
| **히스토리 분석** | SCD와 [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/)로 시점별 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 가능 |

### 5.2 결론 — 기술사 작성 포인트

기술사 시험에서는 "[OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 연산 4종 + [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) 필요성 + [MOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/)/[ROLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/)/[HOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/338_holap/) 비교"를 묶어서 설명하는 것이 고득점 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 특히 <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/">서로게이트 키</a>가 <a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/">SCD</a> Type 2를 가능하게 하는 메커니즘</strong>을 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램과 함께 논술하면 차별화된다.

📢 **섹션 요약 비유**: [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 전체는 회사 경영을 위한 '맞춤 안경'이다 — [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/)가 안경 프레임(구조), 드릴다운/[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이 렌즈 조절(초점), MDX가 안경을 쓰고 읽는 책([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))이다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 저장 방식 | [ROLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/337_rolap/) / [MOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/336_molap/) / [HOLAP](/knowledge-base/studynote/05_database/06_dw_olap_trends/338_holap/) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형·다차원·혼합 저장 |
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 연산 | 드릴다운·[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)·[슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)·다이스 | 다차원 탐색 4종 연산 |
| 차원 설계 | [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/) ([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/)) | 자연 키 대체, [SCD](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/277_scd_slowly_changing_dimension_modeling/) 이력 관리 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | 스타 / 스노우플레이크 | 팩트·[차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/) 구조 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | MDX (Multidimensional Expressions) | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 전용 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 |
| 대비 개념 | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. OLAP는 마트 매출 장부를 날짜별·지역별·제품별로 뒤집어 볼 수 있는 마법 큐브야 — 어떤 각도로 돌려도 합계가 뚝딱 나온단다.

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP (행 기반 트랜잭션)
    |
    v
OLAP: 다차원 분석 (Cube · Drill-Down · Roll-Up)
    +-► MOLAP: 사전 집계 큐브 (빠름 · 유연성v)
    +-► ROLAP: RDBMS 기반 (유연 · 속도v)
    +-► HOLAP: 혼합 방식
    |
    v
Surrogate Key: 비즈니스 키 대체 인조키 (SCD 연동)
    |
    v
클라우드 MPP DW: BigQuery · Snowflake (OLAP 현대화)
```
2. 드릴다운은 전국 매출에서 서울, 서울에서 강남, 강남에서 특정 매장으로 점점 깊이 파고드는 거야 — 마치 지도 줌인처럼!
3. [서로게이트 키](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/276_surrogate_key_artificial_identifier/)는 고객 번호가 바뀌어도 변하지 않는 '도서관 등록 번호'야 — 이름이 바뀌거나 주소가 바뀌어도 도서관 카드 번호는 그대로지.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 211 / 258

<- **이전**: [210. 팩트 테이블 (Fact Table)·차원 테이블 (Dimension Table)·스노우플레이크 스키마 (Snowflake Schema)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)
**다음**: [212. ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/212_etl_elt_cloud_transformation_bottleneck/) ->

---
