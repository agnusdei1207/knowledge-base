+++
title = "147. 집계 함수 (Aggregate Function) - SUM, AVG, MAX, MIN, COUNT"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 집계 함수([Aggregate](/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) Function)는 여러 행(Row)의 값을 하나의 결과값으로 요약하는 SQL(Structured Query Language) 함수로, `GROUP BY`와 결합하여 그룹별 통계를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석의 핵심 도구다.
> 2. **가치**: 수백만 건의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)에서 일 매출 합계, 평균 주문금액, 최대·최소 거래액을 단일 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 추출할 수 있어, 보고서·대시보드·BI(Business Intelligence) 분석의 기반이 된다.
> 3. **판단 포인트**: `NULL` 처리 방식이 함수마다 다르며, `HAVING`은 집계 후 필터링, `WHERE`는 집계 전 필터링이라는 처리 순서가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 결과의 핵심 차이를 만든다.

---

## Ⅰ. 개요 및 필요성

집계 함수는 SQL에서 다수의 행을 하나의 요약 값으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하는 연산이다. 단일 행 함수(UPPER, SUBSTR 등)가 행마다 독립적으로 동작하는 것과 달리, 집계 함수는 <strong>행 집합 전체를 입력으로 받아 스칼라(Scalar) 값 하나를 반환</strong>한다.

비즈니스 현장에서 "이번 달 총 매출은 얼마인가?", "지역별 평균 배송 시간은?", "가장 많이 팔린 상품은?" 같은 질문은 집계 없이 답할 수 없다. 집계 함수는 이런 질문에 SQL 한 문장으로 답하는 능력을 제공한다.

**집계 함수 없으면 발생하는 문제**:
- 애플리케이션 레이어에서 루프를 돌며 합산 -> 수백만 건 처리 시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 재앙
- RDBMS의 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)·통계 최적화를 우회 -> 전체 테이블 스캔 반복
- 코드 복잡도 증가 -> 버그 유입 및 유지보수 비용 급증

- **📢 섹션 요약 비유**: 집계 함수는 **'창고 재고 조사 시 스캐너로 모든 상자를 찍고 총계를 내는 자동화 장치'** 와 같습니다. 직원이 하나씩 세는 대신 스캐너(집계 함수)가 순식간에 총합, 평균, 최대·최소를 뽑아냅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 5대 집계 함수 특성

| 함수 | 기능 | NULL 처리 | 반환 타입 |
|:---|:---|:---|:---|
| `COUNT(*)` | 전체 행 수 | NULL 포함 | 정수 |
| `COUNT(열)` | NULL 아닌 행 수 | NULL 제외 | 정수 |
| `SUM(열)` | 합계 | NULL 제외 | 숫자 |
| `AVG(열)` | 평균 | NULL 제외 | 실수 |
| `MAX(열)` | 최대값 | NULL 제외 | 열과 동일 |
| `MIN(열)` | 최소값 | NULL 제외 | 열과 동일 |

### 2. GROUP BY와 HAVING의 처리 순서

```text
SQL 실행 논리 순서 (집계 관련)

  ① FROM        — 테이블 읽기
  |
  v
  ② WHERE       — 행 단위 필터 (집계 전!)
  |
  v
  ③ GROUP BY    — 그룹 단위 묶기
  |
  v
  ④ 집계 함수   — SUM, AVG, MAX 등 계산
  |
  v
  ⑤ HAVING     — 그룹 단위 필터 (집계 후!)
  |
  v
  ⑥ SELECT     — 출력 열 선택
  |
  v
  ⑦ ORDER BY   — 정렬
```

**핵심 판단**: 집계 결과(SUM, COUNT 등)를 조건으로 필터링하려면 반드시 `HAVING`을 써야 한다. `WHERE` 절에서는 집계 함수를 쓸 수 없다.

### 3. 실전 예시

```sql
-- 부서별 평균 연봉이 500만 원 이상인 부서만 조회
SELECT   dept_id,
         AVG(salary)   AS avg_salary,
         COUNT(*)      AS headcount
FROM     employees
WHERE    hire_date >= '2020-01-01'   -- ① 집계 전 행 필터
GROUP BY dept_id                      -- ② 그룹화
HAVING   AVG(salary) >= 5000000       -- ③ 집계 후 그룹 필터
ORDER BY avg_salary DESC;
```

- **📢 섹션 요약 비유**: WHERE와 HAVING의 차이는 **'시험 전 응시 자격 필터링(WHERE)과 시험 후 합격 그룹 필터링(HAVING)'** 의 차이입니다. 자격 조건은 시험 보기 전에 걸러내고(WHERE), 그룹 평균 점수가 기준 이상인 팀만 선발하는 것은 시험 후에 결정합니다(HAVING).

---

## Ⅲ. 비교 및 연결

### 집계 함수 vs. 윈도우 함수

집계 함수와 윈도우 함수([Window Function](/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/))는 모두 집계 연산을 수행하지만, 핵심 차이는 <strong>행의 수</strong>다.

| 구분 | 집계 함수 + [GROUP BY](/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/) | 윈도우 함수 (OVER) |
|:---|:---|:---|
| 결과 행 수 | 그룹당 1행으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 원본 행 수 유지 |
| 개별 행 접근 | 불가 | 가능 |
| 사용 위치 | [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/), HAVING | [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/), ORDER BY |
| 예시 | `GROUP BY dept, SUM(salary)` | `SUM(salary) OVER (PARTITION BY dept)` |

```sql
-- 윈도우 함수: 각 직원의 행을 유지하면서 부서 합계도 같이 조회
SELECT emp_name,
       salary,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
FROM   employees;
```

### NULL과 AVG의 함정

```sql
-- 주의: AVG는 NULL을 제외하고 계산한다
-- 실제 데이터: [100, 200, NULL, 300] -> AVG = (100+200+300)/3 = 200
-- NULL을 0으로 처리하려면: AVG(COALESCE(score, 0))
```

- **📢 섹션 요약 비유**: 집계 함수와 윈도우 함수의 차이는 **'반 평균 성적표'** 와 **'개인 성적표에 반 평균 추가 열기재'** 의 차이입니다. 집계 함수는 반 전체를 한 줄로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하고, 윈도우 함수는 학생별 성적표는 그대로 두면서 옆에 반 평균 칸을 추가합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 요구사항 | 적용 함수·방법 | 이유 |
|:---|:---|:---|
| 특정 열의 NULL 포함 전체 행 수 | `COUNT(*)` | NULL 포함 카운트 |
| NULL 제외 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 행 수 | `COUNT(열명)` | NULL 자동 제외 |
| 그룹별 소계+총계 동시 | `GROUP BY ROLLUP` | 다차원 집계 |
| 행 유지하면서 그룹 통계 | 윈도우 함수 `OVER()` | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 없는 집계 |
| 중간값(Median) | `PERCENTILE_CONT(0.5)` | AVG는 중간값 아님 |

### [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 판단 포인트

<strong>집계 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 병목은 대부분 GROUP BY의 정렬·해시 연산</strong>: 집계 대상 열에 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있어도 GROUP BY는 전체 행을 처리해야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수억 건이면 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 자체보다 <strong>사전 집계(Materialized <a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a>, <a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a>, 요약 테이블)</strong> 가 필수다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

<strong>SELECT에 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/">GROUP BY</a> 미포함 열 사용 (MySQL 비표준 동작)</strong>: 표준 SQL에서는 `GROUP BY` 절에 없는 열을 `SELECT`에 쓸 수 없다. MySQL의 `only_full_group_by` 비활성화 시 비결정적 값이 반환되어 잘못된 분석 결과를 낳는다. 반드시 표준 SQL 모드를 사용해야 한다.

- **📢 섹션 요약 비유**: [GROUP BY](/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/) 미포함 열을 SELECT에 쓰는 것은 **'반 평균을 구하면서 아무 학생이나 대표로 찍어 이름을 쓰는 것'** 과 같습니다. 평균은 반 전체 것이지만, 이름은 누가 될지 모르는 비결정적 오류입니다.

---

## Ⅴ. 기대효과 및 결론

집계 함수는 SQL의 분석 능력을 애플리케이션 레이어에서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 엔진 레이어로 끌어내려, <strong>RDBMS의 최적화 엔진이 집계 연산을 가장 효율적으로 수행</strong>할 수 있게 한다. [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 집계 등을 활용해 수억 건도 빠르게 처리한다.

**한계**: 실시간 집계는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)([Online Analytical Processing](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) 워크로드로 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)(Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) 시스템에 부하를 준다. 대규모 환경에서는 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 집계 뷰(Materialized [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)), [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 큐브 등의 사전 집계 아키텍처가 필수다.

**미래 방향**: ① 컬럼 스토어 DB([BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift, [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))의 벡터화 집계 연산, ② 스트리밍 집계(Flink, [Spark Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/)), ③ [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화.

집계 함수는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보는 눈을 만드는 것"이다 — 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 의사결정에 쓸 수 있는 인사이트로 변환하는 SQL의 핵심 역량이다.

- **📢 섹션 요약 비유**: 집계 함수는 **'수백만 개의 조각 퍼즐을 순식간에 하나의 그림으로 합쳐주는 기계'** 와 같습니다. 조각 하나하나(개별 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 행)를 눈으로 볼 수는 없지만, 집계 함수가 완성된 그림(합계, 평균, 최대·최소)을 보여줘서 경영 판단이 가능해집니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/">GROUP BY</a></strong> | 집계 함수와 항상 함께 등장하는 [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) 절 |
| **HAVING** | 집계 결과에 대한 필터링; WHERE와 처리 순서가 다름 |
| <strong>윈도우 함수 (<a href="/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/">Window Function</a>)</strong> | 행을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하지 않고 집계하는 집계 함수의 확장 형태 |
| <strong>Materialized <a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a></strong> | 집계 결과를 사전에 저장해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이는 기법 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/">Online Analytical Processing</a>)</strong> | 집계 중심의 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 워크로드 처리 시스템 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 SELECT 조회 (개별 행)
    |
    v
집계 함수 SUM / AVG / MAX / MIN / COUNT
    |
    v
GROUP BY — 그룹별 집계
    |
    +-► HAVING — 집계 후 필터링
    |
    +-► 윈도우 함수 OVER (PARTITION BY) — 행 유지 집계
    |
    v
Materialized View / ROLLUP / CUBE — 사전 집계
    |
    v
OLAP 엔진 / 컬럼 스토어 / 데이터 웨어하우스
```

### 👶 어린이를 위한 3줄 비유 설명

1. 집계 함수는 **'마트 계산대에서 모든 물건의 가격을 한 번에 더해주는 스캐너'** 예요! `SUM`은 총합, `AVG`는 평균, `MAX`는 가장 비싼 거, `MIN`은 가장 싼 거를 알려줘요.
2. `GROUP BY`는 **'물건을 과자·음료·채소로 종류별로 나눈 다음 각각 계산하는 것'** 이에요. 그러면 "과자 총합이 얼마, 음료 총합이 얼마"처럼 그룹별로 알 수 있어요!
3. `HAVING`은 **'계산 다 한 후에 총합이 1만 원 넘는 카테고리만 영수증에 표시하는 조건'** 이에요. `WHERE`는 계산 전에 특정 물건을 빼는 것이고, `HAVING`은 계산 후에 결과를 거르는 것이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 600

<- **이전**: [146. PARTITION BY & ORDER BY - Window 함수 핵심 절](/knowledge-base/studynote/05_database/03_relational_model/146_window_function_partition_by_order_by/)
**다음**: [148. 그룹 바이 (GROUP BY) / 해빙 (HAVING) - HAVING은 그룹화 결과에 대한 조건](/knowledge-base/studynote/05_database/03_relational_model/148_sql_group_by_having_clause/) ->

---
