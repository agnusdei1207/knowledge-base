---
sidebar:
  order: 95
  label: "095. 실행 계획•쿼리 최적화 (Query Execution Plan Optimization)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "실행 계획•쿼리 최적화 (Query Execution Plan Optimization)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 95
extra:
  question_no: "095"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 실행계획 기반 병목 개선"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Query Execution Plan (쿼리 실행 계획)**: SQL 질의를 처리하기 위해 DBMS 옵티마이저(Optimizer)가 테이블 스캔 방식(Index Scan/Full Scan), 조인 알고리즘(Nested Loop/Hash Join), 조인 순서(Join Order)를 정형화하여 결정한 물리적 연산 실행 트리의 명세서.
- **Cost-Based Optimizer (CBO, 비용 기반 옵티마이저)**: 카디널리티(Cardinality), 인덱스 상태, 데이터베이스 통계 정보(Statistics)를 바탕으로 각 실행 가능한 물리적 경로의 CPU/Disk I/O 비용(Cost)을 계산하여 최저 비용 경로를 선택하는 엔진.
- **Parameter Sniffing**: 쿼리 최초 실행 시 전달된 바인드 변수(Parameter)의 스케일에 맞춰 캐시된 실행 계획이 생성된 후, 전혀 다른 범위의 변수가 들어올 때 비효율적 실행 계획으로 작동하는 오작동 현상.

</details>

- 정의/개념: 선언적 언어인 SQL 구문을 데이터베이스가 최단 시간에 실행할 수 있도록 옵티마이저가 인덱스 스캔, 조인 알고리즘, 연산 순서를 기계적으로 조합해 결정하는 실행 트리인 **Query Execution Plan**
- 배경/필요성: 대용량 테이블 조인 시 비효율적 실행 계획(Full Scan / Cartesian Join)으로 인한 CPU/IO 100% 락업(Lockup) 방지, CBO 비용 예측 오류 교정을 통한 쿼리 성능 극대화 요구성

#### 한줄 요약

- 예상 교통량으로 길을 고른 뒤 실제 이동 시간과 비교해 더 빠른 경로를 찾는 작업과 같다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Cost Estimation based on Statistics**: 데이터베이스 `ANALYZE` 통계 기반의 정량적 비용 계산.
- **Tree-structured Operator Architecture**: Root에서 Leaf 노드 방향으로 데이터 조인/필터링 연산이 전달되는 트리 아키텍처 구조.

</details>

- **CBO (비용 기반 옵티마이저)** 의 정량적 최적 경로 자동 도출
- **Tree-Structure Operator (트리 연산 구조: Table Access, Join, Sort, Aggregate)**
- 통계 정보 노후화 시 **Sub-optimal Plan (아최적 경로) 진입 위험성** 상존

#### 한줄 요약

- 데이터 분포 예상이 틀리면 나쁜 경로를 고르므로 계획의 예상값과 실제 처리량을 함께 봐야 한다.

## Ⅲ. 구조 및 구성요소 (실행 계획 4대 핵심 가독 포인트)

<details><summary>핵심 용어</summary>

- **Cardinality (카디널리티)**: 특정 연산 단계에서 반환될 것으로 옵티마이저가 예측한 튜플(행)의 수.
- **Filtered (필터링 비율)**: Table Scan 또는 Index Scan 후 `WHERE` 조건에 의해 남겨진 튜플의 백분율($\%$).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   MySQL EXPLAIN Query Execution Plan                   │
├───────┬─────────────┬───────────┬────────┬────────┬────────────────────┤
│ id    │ select_type │ table     │ type   │ rows   │ Extra              │
├───────┼─────────────┼───────────┼────────┼────────┼────────────────────┤
│ 1     │ SIMPLE      │ orders    │ ref    │ 150    │ Using index condition│
│ 1     │ SIMPLE      │ users     │ eq_ref │ 1      │ NULL               │
└───────┴─────────────┴───────────┴────────┴────────┴────────────────────┘
```

선의 의미: `orders` 테이블을 먼저 `ref` 인덱스 스캔 후 `users` 테이블을 `eq_ref` (PK 조인) 조인하는 실행 계획의 연산 순서 명세.

| 실행 계획 구성 항목 | 대표적 값 및 의미 | 튜닝 핵심 관점 |
|:---|:---|:---|
| **type (접근 방식)** | **`system > const > eq_ref > ref > range > index > ALL`** | `ALL` (Full Table Scan) 발생 여부 파악 |
| **rows (예상 행 수)**| 옵티마이저가 예측한 스캔 대상 튜플 수 (**Cardinality**) | 실제 반환 튜플 수와의 오차율 계산 |
| **Extra (부가 정보)** | **`Using index (커버링), Using temporary, Using filesort`**| `Using filesort/temporary` 발견 시 지우기 |
| **Join Algorithm** | **Nested Loop Join, Hash Join, Sort Merge Join** | 데이터 스케일에 맞는 조인 방식 배치 |

#### 한줄 요약

- 통계로 실행 경로를 고르고 실제 처리량과 예상값을 비교한다.

## Ⅳ. 흐름도 (SQL 최적화 4단계 프로세스)

<details><summary>핵심 용어</summary>

- **Query Rewrite (쿼리 재작성)**: 뷰(View) 펴기, 서브쿼리 불내포화(Unnesting), 정적 조건절 전파 등을 통해 옵티마이저가 처리하기 쉬운 형태로 SQL 구문을 등가 변환하는 기법.

</details>

```text
[SQL 구문 입력] ──► [1. Parser (구문/의미 분석)] ──► [2. Query Rewrite (동등 쿼리 재작성)]
                                                                │
                                                                ▼
 [Execution Execution] ◄── [4. Code Generator (실행계획 생성)] ◄── [3. CBO Estimator (비용 계산)]
```

### 동작 원리

1. **Parsing**: SQL 문법 검사 및 릴레이션/컬럼 존재 유무 체크.
2. **Query Rewriting**: `WHERE 1=1` 등 불필요 조건 제거 및 서브쿼리를 조인 형태로 변환 (`Unnesting`).
3. **CBO Estimation**: 인덱스 스캔 비용과 Full Scan 비용을 DB 통계 메트릭 기반으로 정량 계산.
4. **Plan Generation**: 최적의 물리적 연산 트리(Plan Tree)를 확정하여 실행 엔진으로 이전.

#### 한줄 요약

- 지도 통계로 경로를 고르고 실제 운행 기록이 예상과 다르면 통계와 경로를 다시 점검한다.

## Ⅴ. 종류 및 비교 (RBO 대 CBO)

<details><summary>핵심 용어</summary>

- **Rule-Based Optimizer (RBO)**: 우선순위 규칙(15가지 규칙)에 따라 무조건 정적으로 실행 계획을 세우는 과거 방식.
- **Cost-Based Optimizer (CBO)**: 데이터 통계를 바탕으로 동적 비용을 산출하여 실행 계획을 선택하는 현대 표준 방식.

</details>

| 비교 항목 | RBO (규칙 기반 옵티마이저) | CBO (비용 기반 옵티마이저) |
|:---|:---|:---|
| 최적화 기준 | 정해진 15가지 우선순위 규칙 (Rule) | **통계 기반 CPU / Disk I/O 정량 비용 (Cost)** |
| 통계 정보 필요성| 전혀 필요 없음 | **주기적인 `ANALYZE` 통계 수집 필수** |
| 데이터 변화 대응| 데이터 양이 커져도 실행 계획 고정 | **데이터 크기 및 분포 변화에 맞춰 동적 변환** |
| 상용 DBMS 채택| 과거 레거시 DB 용 | **현대 모든 RDBMS 표준 채택 (Oracle, MySQL 등)**|

#### 한줄 요약

- 어떤 길이 항상 빠른 것이 아니라 데이터 양과 분포에 맞는 길을 선택해야 한다.

## Ⅵ. 실무 고려사항 및 대책 (실행 계획 튜닝 3대 기법)

<details><summary>핵심 용어</summary>

- **Optimizer Hint**: 옵티마이저의 판단 대신 개발자가 직접 인덱스나 조인 방식을 강제 지정하는 주석 힌트 (`/*+ INDEX(a idx_user) USE_HASH(b) */`).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DB 통계 노후화로 잘못된 Full Table Scan 선택 | **`ANALYZE TABLE` 실행으로 DB 통계 정보 최신화** | 정밀한 CBO 비용 산출 |
| `Using filesort / Using temporary` 발생으로 메모리 폭증 | **Composite Index에 `ORDER BY/GROUP BY` 컬럼 포함 배치** | Sort Avoidance (정렬 소멸) |
| CBO가 인덱스를 외면하고 잘못된 조인 선택 | **Optimizer Hint (`/*+ INDEX(...) */`) 조치 및 SQL 튜닝** | 의도한 실행 경로 강제 |

> 사례: **PostgreSQL / MySQL `EXPLAIN ANALYZE` 쿼리 실측 분석 및 B-Tree 인덱스 힌트 조치**

#### 한줄 요약

- 느린 단계만 바꾸지 말고 왜 예상보다 많은 데이터가 흘렀는지부터 찾는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **실행 계획 튜닝 수립 기준(Query Optimization Standards)**: CBO 통계 정보 최신성, EXPLAIN 실행 계획 검증 및 Optimizer Hint 가이드라인에 의거한 체계.

</details>

- **실행 계획 튜닝 수립 기준**에 따라 Slow Query 개선 시 **`EXPLAIN ANALYZE` 기반 병목 도출 및 인덱스/쿼리 재작성** 필수 적용

#### 한줄 요약

- 쿼리 최적화 대응 기준은 예상과 실제가 어긋난 지점에서 통계와 실행 경로를 바로잡는다.
