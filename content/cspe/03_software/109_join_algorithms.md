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
- **개요**: 두 테이블의 관련 행을 실제로 결합하는 DBMS의 **물리 조인 연산(Physical Join Operator)**이며, 대표적으로 Nested Loop, Hash, Merge 세 가지 **조인 알고리즘(Join Algorithm)**이 있다.
- **왜 필요한가**: SQL의 `JOIN`은 "무엇을 결합할지"만 말하고 "어떻게 결합할지"는 명시하지 않는다. 입력 크기·인덱스·메모리 조건에 따라 최적 결합 방식이 달라지므로 옵티마이저가 매번 선택해야 한다.
- **핵심 직관**: 두 명단에서 공통 이름을 찾을 때, 한 명씩 상대 명단 전체를 뒤질지(Nested Loop), 작은 명단으로 해시표를 만들어 대조할지(Hash), 양쪽을 정렬해 나란히 짚어갈지(Merge) 고르는 문제다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 물리 조인 연산(Join Algorithm) | 두 입력 행 집합을 실제로 결합하는 실행 방식 — 이 개념의 상위 범주 | 명단 대조 작업 방식 자체 |
| Nested Loop Join(NLJ) | outer 테이블의 각 행마다 inner 테이블 전체를 반복 탐색해 조건이 맞는 행을 결합 | 명단A 한 명씩 명단B 전체를 처음부터 훑기 |
| outer / inner (NLJ 용어) | outer=바깥 반복문이 도는 테이블(보통 작은 쪽), inner=매번 안쪽에서 탐색당하는 테이블 | 이중 for문의 바깥 루프 변수 vs 안쪽 루프 변수 |
| Index Nested Loop Join | inner 테이블에 인덱스가 있어, 반복 탐색이 순차 검사가 아니라 인덱스 조회(O(log n))로 바뀐 NLJ | 전화번호부 전체를 뒤지지 않고 색인으로 바로 찾기 |
| Hash Join | 작은 입력(build)으로 해시 테이블을 만들고, 큰 입력(probe)의 각 행을 해시 테이블에 대조 | 작은 명단을 해시표로 만들어 큰 명단을 한 번씩 대조 |
| build input / probe input | build=해시 테이블을 만드는 재료(보통 작은 입력), probe=만들어진 해시 테이블을 조회하는 쪽(보통 큰 입력) | 색인을 만들 재료 vs 색인으로 찾아볼 대상 |
| Merge Join(Sort-Merge Join) | 양쪽 입력을 조인 키 기준으로 정렬한 뒤, 두 포인터를 동시에 이동시키며 순차 비교·결합 | 정렬된 두 줄의 명단을 처음부터 동시에 짚어가며 비교 |
| Equi-Join(등가 조인) | `=` 조건으로 결합하는 조인 — Hash Join·Merge Join이 쓸 수 있는 조건 형태 | 정확히 같은 값끼리만 짝짓기 |
| work_mem(작업 메모리) | 해시 테이블 구축·정렬 작업에 DB가 할당하는 메모리 공간 | 서류를 정리할 책상 크기 |
| Spill(스필) | work_mem이 부족해 해시 테이블·정렬 중간 결과를 디스크 임시 파일로 내보내는 현상 | 책상이 좁아 서류를 바닥에 늘어놓기 |

## 깊이 이해

### 왜 알고리즘이 여러 개 필요한가 — 입력 크기의 비대칭
- SQL은 `A JOIN B ON A.id = B.id`처럼 결합 대상만 말한다. 실제로 A가 100건이고 B가 1억 건인 경우와, A·B가 둘 다 5,000만 건인 경우는 최적 결합 방식이 전혀 다르다. 그래서 옵티마이저는 매번 통계를 보고 알고리즘을 고른다.

### Nested Loop Join — 연산량을 숫자로 확인
- 인덱스가 없는 순수 NLJ의 비용은 outer 행 수 × inner 스캔 비용이다. outer=100건, inner=100만 건을 인덱스 없이 결합하면 매 outer 행마다 inner 100만 건을 훑어야 하므로 최악 100 × 1,000,000 = 1억 번 비교가 발생한다.
- inner에 인덱스가 있으면(Index Nested Loop) 매번 훑는 대신 인덱스로 바로 찾는다. B-Tree 인덱스는 100만 건 기준 트리 높이가 3~4단계 수준이므로, 조회 1건이 약 3~4번의 페이지 접근으로 끝난다. 그러면 총 비용은 100 × 4 = 400번 수준으로 줄어든다 — 순수 NLJ 대비 약 25만 배 차이다.
- 그래서 NLJ는 **outer가 작고 inner에 유효한 인덱스가 있을 때만** 유리하다.

### Hash Join — 왜 대량 데이터에 강한가
- Hash Join의 비용은 build 비용(작은 입력 크기만큼) + probe 비용(큰 입력 크기만큼)으로, 대략 O(build_rows + probe_rows)다. `customers` 100만 건과 `orders` 5,000만 건을 조인할 때, customers로 해시 테이블(100만 건 규모)을 만들고 orders 5,000만 건을 한 번씩 조회하면 총 연산량은 약 5,100만 수준이다. 같은 규모를 NLJ로 처리하면 100만 × 5,000만이 되어 비교가 불가능할 정도로 커진다.
- 단, 해시 테이블은 메모리(work_mem)에 올라가야 빠르다. build input이 800MB인데 work_mem이 4MB뿐이면 해시 테이블 일부가 디스크로 spill되어 temp I/O가 급증한다 — "Hash Join은 항상 빠르다"가 아니라 "메모리가 충분할 때 빠르다"이다.

### Merge Join — 이미 정렬돼 있을 때의 지름길
- 양쪽 입력을 조인 키로 정렬하는 비용은 각각 O(n log n)이지만, 정렬만 끝나면 이후 병합은 두 포인터를 한 번씩만 앞으로 이동시키는 O(n+m)으로 끝난다. 이미 인덱스 덕분에 정렬된 순서로 데이터가 나온다면 별도 정렬 비용 없이 바로 병합할 수 있어 매우 효율적이다.
- 반대로 정렬되지 않은 대용량 데이터를 Merge Join을 위해 새로 정렬해야 한다면, 그 정렬 비용이 Hash Join의 build 비용보다 클 수 있다.

### 세 알고리즘을 고르는 판별 원리
- **outer가 작고 inner에 인덱스가 있음** → Index Nested Loop (OLTP의 소량 조회에 전형적)
- **대량 데이터의 등가 조인이고 메모리가 충분함** → Hash Join (배치·집계 쿼리에 전형적)
- **양쪽이 이미 정렬돼 있거나 범위 조인이 필요함** → Merge Join
- 등가 조건이 아닌 범위 조인(`A.start <= B.date AND B.date < A.end`)은 해시 테이블의 "정확히 같은 값" 특성과 맞지 않아 Hash Join을 쓸 수 없고, NLJ나 Merge Join 계열로만 처리된다.

### 흔한 오해
- "Hash Join이 항상 최선이다"는 틀렸다 — 메모리 부족 시 spill로 temp I/O가 Merge Join·NLJ보다 오히려 커질 수 있다.
- "테이블이 크면 무조건 Hash Join"도 틀렸다 — 필터 조건 때문에 실제로 결합에 참여하는 행이 적다면(예: 5,000만 건 중 100건만 조건에 맞음) Index Nested Loop가 더 쌀 수 있다. 판단 기준은 원본 테이블 크기가 아니라 **필터 후 실제 조인 대상 행 수(cardinality)**다.

## 연결 개념
- Cardinality Estimation — 어느 알고리즘이 유리한지 판단하는 입력값(108 참고)
- Join Order — 3개 이상 테이블 조인 시 어떤 두 테이블을 먼저 결합할지 결정(108 참고)
- Work Memory — Hash Join build·Merge Join sort가 쓰는 메모리, 부족하면 spill 발생

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
