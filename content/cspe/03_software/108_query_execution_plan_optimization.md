---
title: "실행 계획·쿼리 최적화 (Query Execution Plan Optimization)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 108
---

# 📖 【암기용】 개념 완전 이해

> 목적: 실행 계획과 쿼리 최적화를 처음 보는 사람도 DBMS가 어떤 경로로 SQL을 실행할지 고르는 과정을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: SQL을 실제로 실행할 최소 비용 경로를 고르는 DBMS의 **쿼리 최적화(Query Optimization)** 과정이며, 그 결과물이 **실행 계획(Execution Plan)**이다.
- **왜 필요한가**: SQL은 "무엇을 원하는지"만 선언하고 "어떻게 가져올지"는 DBMS가 정한다. 같은 결과를 내는 경로가 여러 개이고 그 비용 차이가 수십~수백 배이므로, 최적 경로를 고르는 절차가 필요하다.
- **핵심 직관**: 내비게이션이 같은 목적지라도 거리·정체·통행료를 계산해 경로를 고르는 것과 같다. SQL 문장은 "목적지"만 말하고, 옵티마이저가 "경로"를 정한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 쿼리 최적화(Query Optimization) | 여러 후보 실행 경로 중 비용이 최소인 것을 고르는 과정 — 이 개념의 상위 범주 | 내비게이션의 경로 탐색 엔진 |
| 실행 계획(Execution Plan) | 옵티마이저가 고른 구체적 연산자 트리(스캔 방식·조인 순서·조인 알고리즘) | 내비게이션이 최종 표시하는 경로 한 줄 |
| Parser | SQL 문법·객체(테이블·컬럼) 존재를 검사해 구문 트리를 만드는 단계 | 맞춤법·문법 검사 |
| Rewriter | 뷰를 원본 테이블 조회로 풀어쓰고 조건을 동치식으로 단순화하는 단계 | 초안을 다듬어 처리하기 쉬운 형태로 재작성 |
| Optimizer(CBO) | 여러 후보 계획의 비용을 통계로 계산해 최소 비용 계획을 선택하는 단계 | 이사업체 견적 3곳을 비교해 최저가 선택 |
| Cardinality(추정 행 수) | 특정 연산(스캔·조인·필터)이 반환할 것으로 예측되는 행 개수 | 예상 손님 수를 미리 세어보기 |
| 통계(Statistics)·히스토그램 | 테이블의 행 수, distinct 값 수, 값 분포 구간별 빈도를 기록해둔 메타데이터 | 인구조사 자료 — 옵티마이저가 참고하는 지도 |
| 비용 모델(Cost Model) | CPU 연산, 디스크 I/O, 메모리 사용량을 하나의 숫자(비용)로 환산하는 공식 | 이사 견적서(인건비+차량비+거리) |
| 접근 경로(Access Path) | 한 테이블에 도달하는 개별 방법 — Full Scan(전체 순차 읽기) 또는 Index Scan(색인 경유) | 목적지까지 가는 개별 도로 하나 |
| 조인 순서(Join Order) | 3개 이상 테이블을 조인할 때 어느 테이블부터 결합할지 정하는 순서 | 여러 재료를 어떤 순서로 섞을지 |
| Predicate Pushdown | WHERE 조건을 최대한 이른 단계(스캔 시점)로 내려보내 불필요한 행을 조기에 걸러내는 기법 | 정문 입구에서 먼저 신분 확인해 안까지 안 들여보내기 |
| EXPLAIN ANALYZE | 실행 계획을 실제로 실행하면서 예측 행 수(estimated)와 실제 행 수(actual)를 함께 보여주는 진단 도구 | 내비게이션의 예상 도착시간과 실제 도착시간을 나란히 비교 |

## 깊이 이해

### 처리 파이프라인 — SQL이 결과가 되기까지
- SQL 문장이 들어오면 ① Parser가 문법·객체를 검사해 구문 트리로 바꾸고, ② Rewriter가 뷰 병합·조건 단순화로 트리를 정리하고, ③ Optimizer가 통계를 이용해 여러 후보 실행 계획의 비용을 계산·비교해 최소 비용 계획을 고르고, ④ Executor가 그 계획대로 실제 데이터를 읽어 결과를 만든다.
- 이 중 튜닝의 핵심은 ③ Optimizer 단계다. 여기서 통계가 낡거나 부정확하면 이후 모든 단계가 잘못된 경로로 실행된다.

### 비용 기반 최적화(CBO)가 경로를 고르는 방법 — 선택도로 판단
- 옵티마이저는 조건절의 **선택도(selectivity)** = 조건을 만족하는 행 수 / 전체 행 수를 계산해 인덱스 스캔과 풀 스캔 중 하나를 고른다.
- **구체 수치 예시**: `orders` 테이블 1,000만 행에서 `WHERE status='CANCELLED'`가 2,000건만 해당하면 선택도는 0.02%다. 이때는 인덱스로 2,000건만 콕 집어 읽는 것이 훨씬 싸다. 반대로 `WHERE created_at > '2020-01-01'`이 900만 건(90%)에 해당하면, 인덱스를 따라 900만 번 흩어진 위치를(random I/O) 읽는 것보다 테이블을 처음부터 순서대로(sequential I/O) 읽는 Full Scan이 더 빠르다.
- 실무 경험칙으로는 선택도가 대략 5~15% 미만이면 인덱스 스캔이, 그 이상이면 풀 스캔이 유리한 경우가 많다(정확한 임계값은 저장 매체·DB 버전마다 다르다). 이것이 "인덱스가 있다고 항상 쓰이지 않는" 이유다.

### 통계가 틀리면 벌어지는 일 — Cardinality 추정 오류
- 옵티마이저의 판단은 통계에 전적으로 의존한다. 통계가 갱신되지 않아 실제로는 10건뿐인 조건을 100만 건으로 잘못 추정하면, 옵티마이저는 "행이 많다"고 착각해 소량 조회에 적합한 Nested Loop 대신 대량 처리용 Hash Join을 고를 수 있다. 그 결과 불필요한 해시 테이블 생성과 temp 영역 I/O가 발생한다.
- `EXPLAIN ANALYZE`를 실행하면 계획 단계의 예측치(estimated rows)와 실제 실행 결과(actual rows)가 함께 출력된다. 이 둘의 차이가 10배 이상이면 통계가 낡았다는 강한 신호다.

### 조인 순서가 중간 결과 크기를 좌우하는 예
- 세 테이블 A(회원, 필터 후 100건), B(주문, 100만 건), C(상품, 50건)를 조인한다고 하자. B와 C를 먼저 결합하면 조인 조건이 맞기 전까지 중간 결과가 최대 100만×50에 근접할 수 있다. 반대로 이미 필터링된 A(100건)와 C(50건)를 먼저 결합해 소량의 중간 결과(최대 5,000건)를 만든 뒤 B와 결합하면, 이후 단계가 다뤄야 할 행 수가 훨씬 작아진다.
- 옵티마이저는 이런 중간 결과 크기를 통계로 추정해 비용이 최소가 되는 순서를 찾는다. 통계가 틀리면 이 순서 선택도 함께 틀어진다.

### Predicate Pushdown — 조건을 최대한 앞으로
- `SELECT * FROM (SELECT * FROM orders) o WHERE o.status='CANCELLED'`처럼 서브쿼리로 감싸도, 옵티마이저는 `status='CANCELLED'` 조건을 서브쿼리 내부 스캔 단계로 밀어넣어 애초에 필터링된 행만 읽는다. 조건을 상위 레이어에서 뒤늦게 거르면 불필요한 행까지 디스크에서 읽고 버리는 낭비가 생기기 때문이다.

## 연결 개념
- Cost Model — CPU·I/O·메모리 비용을 수치화하는 옵티마이저의 판단 근거
- Statistics/Histogram — Cardinality 추정의 원재료, 낡으면 전체 실행 계획이 틀어짐
- 조인 알고리즘(NLJ·Hash·Merge) — 실행 계획이 조인 순서 다음으로 선택하는 물리 연산(109 참고)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 쿼리 최적화는 SQL 문장 수정이 아니라 통계, 비용 모델, 실행 계획, 관측 지표를 함께 검증하는 절차이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 실행 계획 최적화는 Parser, Rewriter, Optimizer, Executor가 SQL을 최소 비용 경로로 실행하도록 접근 경로와 조인 순서를 선택하는 과정이다.
> 2. **가치**: full scan, 잘못된 join order, 부정확한 cardinality 추정을 줄여 p95 지연, CPU, temp I/O를 낮춘다.
> 3. **판단 포인트**: estimated row와 actual row 차이, statistics 신선도, predicate pushdown, join algorithm을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DBMS SQL 처리 흐름 이해 확인 | parser, optimizer, cost model, executor | Explain Plan을 단순 출력 도구로만 설명 |
| 튜닝 원인 분석 역량 확인 | cardinality, statistics, join order, predicate pushdown | 인덱스 추가만 답안으로 제시 |
| 운영 검증 능력 확인 | EXPLAIN ANALYZE, actual row, wait event | 테스트 없는 힌트 적용 |

> 요약: 이 문제는 실행 계획을 읽고 원인별로 통계·SQL·인덱스·조인 전략을 조정하는 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 실행 계획은 SQL 처리 경로이다.
- 배경: 대용량 DB에서는 같은 결과라도 full scan, index scan, join order, hash join 선택에 따라 I/O와 CPU 비용이 달라진다.
- 필요성: Statistics, Cost Model, EXPLAIN ANALYZE로 estimated row와 actual row 차이를 검증해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
SQL Text -> Parser -> Rewriter -> Optimizer -> Execution Plan -> Executor
                      / Statistics
                      / Cost Model
                      / Access Path
                      / Join Order
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Parser | SQL 문법 분석과 객체 해석 | syntax, semantic check |
| Rewriter | 뷰 병합, 조건 단순화 | predicate transformation |
| Optimizer | 후보 계획 비용 비교 | CBO, cardinality estimation |
| Statistics | row count, distinct, histogram 제공 | 노후 시 plan 오류 |
| Executor | 선택 계획 수행 | actual row, wait event 발생 |

> 요약: 실행 계획은 SQL 분석, 재작성, 비용 기반 최적화, 실행 단계가 통계와 비용 모델을 통해 연결된 결과이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SQL 수신 -> 구문 분석 -> 통계 조회 -> 후보 계획 생성 -> 비용 비교 -> 실행 및 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SQL parsing과 권한 확인 | hard parse 비율 관리 |
| 2 | 조건·조인 그래프와 통계 조회 | statistics age 24시간 이하 |
| 3 | access path와 join order 후보 생성 | index scan, full scan 후보 |
| 4 | 비용 모델로 plan 선택 | estimated cost 최소 |
| 5 | actual row와 wait event 측정 | 추정/실제 row 오차 10배 이하 |

> 요약: 최적화는 후보 계획을 만들고 비용을 비교한 뒤 실제 실행 지표로 추정 오류를 보정하는 반복 과정이다.

---

## Ⅳ. 특징

| 구분 | 규칙 기반 접근 | 비용 기반 최적화 | 판단 포인트 |
|:---|:---|:---|:---|
| 기준 | 고정 규칙, 인덱스 우선 | 통계·비용·카디널리티 | 데이터 분포 반영 여부 |
| 장점 | 예측 가능 | workload별 계획 선택 | histogram과 통계 필요 |
| 한계 | 데이터 변화 반영 제한 | 추정 오류 시 plan 회귀 | estimated vs actual 비교 |
| 통제 | SQL 구조 단순화 | stats update, plan baseline | 변경 전후 replay |

> 요약: 현대 DBMS는 비용 기반 최적화를 사용하므로 통계 품질과 추정 오차 관리가 실행 계획 품질을 좌우한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SQL 문장 튜닝만 수행 | 통계+계획+지표 기반 튜닝 | slow SQL p95 300ms 초과 |
| 비용/성능 | 인덱스 추가 위주 | join order, predicate pushdown, stats | temp I/O, CPU, buffer read 원인별 대응 |
| 운영/위험 | 힌트로 plan 고정 | baseline과 regression test | 데이터 분포 변화가 큰 업무 |

> 요약: 쿼리 튜닝은 인덱스보다 먼저 실행 계획의 cardinality 오류와 연산자 선택 원인을 확인해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Plan Regression | 통계 갱신, DB 패치 | plan baseline, query store | p95 증가 20% 이상 감지 |
| Cardinality 오류 | skew 데이터, 복합 조건 상관 | histogram, extended statistics | estimated/actual row 오차 10배 이하 |
| Temp I/O 폭증 | hash join spill, sort spill | work_mem 조정, 인덱스 정렬 활용 | temp read/write MB |

> 요약: 실행 계획 리스크는 계획 회귀, 추정 오류, 메모리 spill로 나누어 감시한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 시간 | 핵심 SQL p95 300ms 이하 | APM, slow query log |
| 추정 정확도 | estimated/actual row 10배 이하 | EXPLAIN ANALYZE |
| 자원 사용 | buffer read 50% 감소, temp spill 0건 | DB statistics, wait event |

> 요약: 최적화 성공은 지연시간, 추정 정확도, buffer·temp I/O 지표로 판정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. slow query 상위 20개에 대해 `EXPLAIN ANALYZE`를 수행하고 estimated/actual row 오차 10배 초과 지점을 먼저 수정함
2. 조인 조건과 필터 조건에 맞춰 statistics, histogram, extended statistics를 갱신하고 predicate pushdown 가능하도록 SQL을 재작성함
3. 개선 plan은 query store 또는 baseline으로 고정하고 workload replay에서 p95 300ms 이하, temp spill 0건을 검증함

**결론 (2줄):**
- 기술사 판단: 실행 계획 문제는 인덱스 부족, 통계 오류, 조인 순서 오류, 메모리 부족을 분리해 원인별로 처리해야 함
- 향후 방향: adaptive query optimization과 자동 튜닝을 사용하더라도 plan regression 검증과 승인 절차를 유지해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "실행 계획 최적화를 설명하시오" | parser -> optimizer -> executor 흐름 | 비용 기반 최적화와 규칙 기반 비교 |
| 요구사항 명시형 | "튜닝 방안을 제시하시오", "설계하시오" | EXPLAIN ANALYZE 기반 원인 분리 절차 | 통계, 인덱스, 조인, baseline 대응 |

> 요약: 설명형은 처리 흐름, 튜닝형은 지표 기반 원인 분석과 회귀 방지 중심으로 작성한다.
