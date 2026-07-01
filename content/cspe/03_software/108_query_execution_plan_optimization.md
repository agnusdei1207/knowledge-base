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
- **개요**: SQL을 파싱한 뒤 통계와 비용 모델로 접근 경로, 조인 순서, 연산자를 선택하는 과정
- **왜 필요한가**: 같은 결과를 내는 SQL도 full scan, index scan, hash join, nested loop에 따라 I/O가 100배 이상 차이 날 수 있다.
- **핵심 직관**: 목적지는 같아도 내비게이션이 거리, 교통량, 통행료를 계산해 경로를 고르는 것과 같다.

## 깊이 이해
- **배경·문제의식**: SQL은 선언형 언어라 사용자는 결과를 말하고 실행 순서는 DBMS가 정한다. 옵티마이저는 통계, 히스토그램, 인덱스, 비용 모델로 여러 후보 계획을 비교한다.
- **작동 원리**: Parser가 SQL을 구문 트리로 만들고, Rewrite가 뷰 병합·조건 단순화를 수행한다. Optimizer는 cardinality를 추정해 join order, access path, join algorithm을 선택한다. Executor는 선택된 plan을 실행한다.
- **비유**: 물류센터가 주문을 받으면 어떤 창고에서 먼저 꺼낼지, 어떤 차량에 실을지, 어느 경로로 보낼지를 비용표로 결정하는 과정이다.
- **구체 예시**: 통계가 오래되어 실제 10건인 조건을 100만 건으로 추정하면 nested loop 대신 hash join을 선택해 temp I/O가 증가할 수 있다. `EXPLAIN ANALYZE`로 estimated row와 actual row 차이를 확인한다.
- **흔한 오해·주의점**: 실행 계획은 SQL 텍스트만으로 고정되지 않는다. 통계, 바인드 변수, 데이터 분포, 파라미터 스니핑, DB 버전에 따라 바뀐다.

## 연결 개념
- Cost Model — CPU, I/O, memory 비용을 수치화
- Statistics — 카디널리티와 히스토그램 기반 추정값
- Predicate Pushdown — 조건을 하위 연산으로 밀어 조기 필터링

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

실행 계획은 DBMS가 SQL을 처리하기 위해 선택한 연산 순서와 접근 경로이다. 대용량 DB에서는 같은 결과라도 계획에 따라 I/O와 CPU 비용이 크게 달라진다. 최적화는 통계와 비용 모델로 낮은 비용의 계획을 선택·검증하는 활동이다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
