---
title: "조인 알고리즘 — NLJ·Hash Join·Merge Join (Join Algorithms)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 109
---

# 📖 【암기용】 개념 완전 이해

> 목적: 조인 알고리즘을 처음 보는 사람도 DBMS가 Nested Loop, Hash, Merge 중 어떤 방식을 고르는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 두 테이블의 관련 행을 결합하기 위해 DBMS가 사용하는 물리 연산 방식
- **왜 필요한가**: 조인은 DB 비용의 큰 비중을 차지한다. 작은 테이블 100건과 큰 테이블 1억 건을 붙일 때 인덱스가 있으면 Nested Loop가 유리하고, 대량 등가 조인은 Hash Join이 유리하다.
- **핵심 직관**: 작은 명단을 들고 전화번호부에서 한 명씩 찾을지, 양쪽 명단을 해시표로 만들지, 둘 다 정렬해 줄 맞춰 비교할지 선택하는 문제이다.

## 깊이 이해
- **배경·문제의식**: SQL은 조인 결과만 표현하고 실제 결합 방법은 옵티마이저가 결정한다. 테이블 크기, 카디널리티, 인덱스, 메모리, 정렬 여부에 따라 비용이 달라진다.
- **작동 원리**: Nested Loop Join은 outer row마다 inner를 탐색한다. Index Nested Loop는 inner index가 있을 때 적합하다. Hash Join은 작은 입력으로 hash table을 만들고 큰 입력을 probe한다. Merge Join은 양쪽 입력을 join key로 정렬한 뒤 순차 병합한다.
- **비유**: 회의 참석자 10명을 회사 전체 명부에서 찾는 것은 한 명씩 검색이 맞고, 두 대형 회원 목록의 공통 고객을 찾는 것은 해시표나 정렬 병합이 맞다.
- **구체 예시**: `orders` 1억 행과 `customers` 100만 행을 customer_id로 조인할 때 필터 후 주문 100건이면 Index NLJ, 주문 5,000만 건이면 Hash Join 또는 Merge Join 후보이다.
- **흔한 오해·주의점**: Hash Join이 항상 낮은 비용인 것은 아니다. 메모리 부족으로 spill이 발생하면 temp I/O가 증가하고, 범위 조인·비등가 조인에는 제한이 있다.

## 연결 개념
- Cardinality Estimation — 입력 행 수 추정
- Join Order — 어떤 테이블을 먼저 결합할지 결정
- Work Memory — hash table과 sort 메모리 크기

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 조인 알고리즘은 명칭 암기가 아니라 입력 크기, 인덱스, 메모리, 정렬 상태에 따른 물리 연산 선택 문제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 조인 알고리즘은 두 입력을 Nested Loop, Hash, Merge 방식으로 결합해 SQL 조인 결과를 만드는 DBMS 물리 연산이다.
> 2. **가치**: 입력 행 수와 접근 경로에 맞는 알고리즘을 선택하면 buffer read, temp I/O, CPU 사용률을 낮출 수 있다.
> 3. **판단 포인트**: outer cardinality, inner index, hash memory, sort cost, join key 정렬 여부를 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DB 물리 연산 이해 확인 | NLJ, Index NLJ, Hash Join, Merge Join | 알고리즘 이름만 나열 |
| 옵티마이저 선택 기준 확인 | cardinality, index, memory, sort | 작은 테이블/큰 테이블 기준 누락 |
| 튜닝 적용 역량 확인 | EXPLAIN PLAN, join order, spill, hint | Hash Join을 모든 대량 조인 해법으로 단정 |

> 요약: 이 문제는 조인 알고리즘별 적합 조건과 실행 계획 지표를 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 조인 알고리즘은 테이블 결합 연산이다.
- 배경: DBMS는 조인 순서와 NLJ, Hash Join, Merge Join을 통계, 인덱스, 메모리 비용으로 선택한다.
- 필요성: outer cardinality, inner index, work memory, sort cost를 기준으로 temp spill과 buffer read를 통제해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Join Query -> Optimizer -> Join Order -> Join Algorithm -> Joined Result
             / Nested Loop
             / Hash Join
             / Merge Join
             / Index Nested Loop
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Nested Loop Join | outer 각 행마다 inner 탐색 | outer가 작고 inner index 있을 때 적합 |
| Hash Join | build input 해시 후 probe | 등가 조인, 대량 입력에 적합 |
| Merge Join | 정렬된 두 입력을 순차 병합 | 양쪽 정렬 또는 인덱스 순서 활용 |
| Join Order | 여러 테이블 조인 순서 결정 | 중간 결과 cardinality 최소화 |
| Work Memory | hash table과 sort 작업 공간 | 부족 시 temp spill 발생 |

> 요약: 조인 구조는 조인 순서와 물리 알고리즘을 함께 선택해 중간 결과와 I/O 비용을 줄이는 방식이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
조인 조건 분석 -> 입력 cardinality 추정 -> 인덱스/정렬 확인 -> 알고리즘 선택 -> 실행 지표 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 조인 키와 등가·범위 조건 구분 | equi join 여부 |
| 2 | 필터 후 입력 행 수 추정 | estimated/actual row 오차 10배 이하 |
| 3 | inner index와 정렬 상태 확인 | index seek 가능 여부 |
| 4 | NLJ, Hash, Merge 중 비용 비교 | cost, buffer read, temp I/O |
| 5 | 실행 후 spill과 row count 검증 | temp spill 0건 |

> 요약: 조인 알고리즘 선택은 조건 형태, 입력 크기, 인덱스, 메모리, 정렬 상태를 순서대로 확인한다.

---

## Ⅳ. 특징

| 구분 | Nested Loop Join | Hash Join | Merge Join |
|:---|:---|:---|:---|
| 적합 조건 | outer 작음, inner index | 대량 등가 조인, 메모리 충분 | 양쪽 정렬, 범위 병합 |
| 주요 비용 | 반복 index lookup | hash build, memory spill | sort cost, 순차 scan |
| 장점 | 소량 조회 응답 지연 낮음 | 대량 결합 처리량 확보 | 정렬 결과 재사용 |
| 주의 지표 | loop count, key lookup | hash spill MB | sort spill, merge pass |

> 요약: NLJ는 소량+인덱스, Hash는 대량 등가, Merge는 정렬된 입력에서 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 조인 방식 고정 | 통계 기반 알고리즘 선택 | 데이터 분포와 필터 조건 변화 |
| 비용/성능 | full scan 조인 | index lookup, hash, sort 병행 | buffer read와 temp I/O 최소 |
| 운영/위험 | 힌트 남용 | plan baseline과 통계 관리 | plan regression 방지 |

> 요약: 조인 튜닝은 알고리즘 강제보다 cardinality 추정과 인덱스·메모리 조건을 먼저 맞춰야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| NLJ 폭증 | outer 추정 오류 | 통계 갱신, join order 조정 | loop count, buffer read |
| Hash spill | work memory 부족 | work_mem 조정, build input 축소 | temp write MB 0 |
| Sort spill | Merge Join 전 정렬 공간 부족 | 정렬 인덱스, memory 조정 | sort pass count |

> 요약: 조인 리스크는 반복 lookup, hash spill, sort spill로 나누어 실행 계획에서 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 추정 정확도 | estimated/actual row 10배 이하 | EXPLAIN ANALYZE |
| I/O 비용 | buffer read 50% 감소 | DB statistics IO |
| 메모리 사용 | hash/sort spill 0건 | wait event, temp file log |

> 요약: 조인 개선은 row 추정 정확도, buffer read, temp spill 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. EXPLAIN ANALYZE로 outer/inner actual row를 확인하고 오차 10배 초과 시 통계·히스토그램·필터 조건을 먼저 보정함
2. 소량 outer+inner index 조합은 Index NLJ, 대량 등가 조인은 Hash Join, 정렬 입력은 Merge Join 후보로 검토함
3. hash/sort spill이 발생하면 work memory, build input 축소, covering index, partition pruning을 적용해 temp write 0MB를 목표로 함

**결론 (2줄):**
- 기술사 판단: 조인 알고리즘 선택은 데이터 크기보다 필터 후 cardinality와 인덱스·메모리 조건으로 결정해야 함
- 향후 방향: adaptive join, runtime statistics feedback을 활용하되 plan regression 감시와 baseline을 병행해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "조인 알고리즘을 설명하시오" | 조건 분석 -> cardinality -> 알고리즘 선택 | NLJ·Hash·Merge 비교 |
| 요구사항 명시형 | "튜닝 방안을 제시하시오", "비교하시오" | actual row와 spill 기반 원인 분석 | 알고리즘 선택 기준과 리스크 대응 |

> 요약: 설명형은 알고리즘 원리, 튜닝형은 실행 계획 지표와 spill 제거 중심으로 작성한다.
