---
title: "클러스터드 인덱스·커버링 인덱스 (Clustered Covering Index)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 107
---

# 📖 【암기용】 개념 완전 이해

> 목적: 클러스터드 인덱스와 커버링 인덱스를 처음 보는 사람도 데이터 배치와 테이블 접근 생략의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 클러스터드 인덱스는 데이터 행의 물리적 순서를 좌우하고, 커버링 인덱스는 쿼리 필요 컬럼을 인덱스만으로 제공한다.
- **왜 필요한가**: 범위 조회는 데이터가 key 순서로 모여 있을 때 I/O가 줄고, 목록 화면은 인덱스 leaf에 필요한 컬럼이 있으면 테이블 fetch를 생략한다.
- **핵심 직관**: 클러스터드는 책을 가나다 순으로 꽂아두는 방식, 커버링은 색인에 쪽번호뿐 아니라 요약까지 적어 본문을 열지 않는 방식이다.

## 깊이 이해
- **배경·문제의식**: 일반 인덱스는 row locator를 통해 테이블을 다시 읽는다. 반환 행이 많으면 bookmark lookup이 반복되어 랜덤 I/O가 증가한다.
- **작동 원리**: 클러스터드 인덱스는 leaf level이 실제 데이터 페이지이거나 데이터 행 순서를 결정한다. 커버링 인덱스는 검색 조건, 정렬, SELECT 컬럼을 모두 포함해 index-only scan을 가능하게 한다.
- **비유**: 창고 물품을 주문번호 순서로 쌓아두면 주문 범위 피킹이 짧고, 피킹 리스트에 가격·수량까지 있으면 창고 장부를 다시 보지 않는다.
- **구체 예시**: `orders(tenant_id, created_at) include (status, amount)` 인덱스는 테넌트별 최근 주문 목록에서 1,000건 bookmark lookup을 0건으로 줄여 buffer read를 크게 낮춘다.
- **흔한 오해·주의점**: 커버링 인덱스는 SELECT 컬럼이 늘면 폭이 커져 캐시 적중률이 떨어지고 쓰기 비용이 증가한다. 모든 컬럼을 넣는 설계는 피해야 한다.

## 연결 개념
- Bookmark Lookup — 인덱스 후 테이블 행 재조회
- Index-Only Scan — 인덱스만으로 결과 반환
- Clustering Factor — 인덱스 순서와 테이블 배치 일치도

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 클러스터드·커버링 인덱스는 단순 인덱스 추가가 아니라 데이터 배치와 테이블 접근 횟수를 줄이는 물리 설계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클러스터드 인덱스는 데이터 행의 저장 순서를 key와 맞추고, 커버링 인덱스는 질의 필요 컬럼을 leaf에 포함한다.
> 2. **가치**: 범위 스캔 page 수와 bookmark lookup을 줄여 p95 지연과 buffer read를 낮춘다.
> 3. **판단 포인트**: 조회 패턴, 정렬 조건, 반환 컬럼, 쓰기 증폭, 인덱스 폭을 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인덱스 물리 구조 이해 확인 | clustered leaf, covering, index-only scan | 두 개념을 동일한 인덱스 종류로 혼동 |
| 실행 계획 해석 역량 확인 | bookmark lookup, key lookup, table fetch | SELECT 컬럼 폭과 include 컬럼 영향 누락 |
| 운영 트레이드오프 판단 확인 | page split, fragmentation, write overhead | PK를 항상 clustered로 두는 단정 |

> 요약: 이 문제는 데이터 순서와 필요 컬럼 포함 여부가 I/O 경로를 어떻게 바꾸는지 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

클러스터드 인덱스와 커버링 인덱스는 테이블 접근 비용을 줄이는 물리 설계 기법이다. 클러스터드는 데이터 배치를 인덱스 key 순서와 맞추고, 커버링은 쿼리 결과를 인덱스만으로 반환한다. 범위 조회와 목록 화면에서 효과가 크다.

---

## Ⅱ. 구조 및 구성요소

```text
Query Predicate -> Index Seek -> Leaf Page -> Row Data 또는 Included Columns -> Result
                 / Clustered: leaf includes row
                 / Covering: leaf includes selected columns
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Clustered Key | 데이터 행 배치 기준 | 테이블당 1개, 범위 조회에 유리 |
| Leaf Page | clustered에서는 실제 행 또는 행 순서 | page split과 fragmentation 발생 |
| Nonclustered Index | 별도 key와 row locator 저장 | clustered key를 locator로 보유 가능 |
| Included Column | 검색 key는 아니나 결과 반환에 필요한 컬럼 | WHERE에는 제한적 사용 |
| Index-Only Scan | 테이블 접근 없이 결과 반환 | visibility map, covering 조건 필요 |

> 요약: 클러스터드는 행 배치를, 커버링은 leaf 포함 컬럼을 통해 테이블 재접근을 줄인다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쿼리 조건 식별 -> 정렬/범위 조건 확인 -> key와 include 설계 -> 실행 계획 확인 -> DML 비용 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | WHERE, ORDER BY, SELECT 컬럼 분리 | 목록 화면 상위 SQL |
| 2 | clustered key 후보 선정 | range scan, insert pattern 확인 |
| 3 | covering key와 include 컬럼 결정 | key lookup 0건 목표 |
| 4 | Explain Plan에서 index-only scan 확인 | table fetch 0건 |
| 5 | page split, write latency 측정 | insert p95 100ms 이하 |

> 요약: 설계는 조건·정렬 컬럼을 key로, 반환 전용 컬럼을 include로 분리하고 실행 계획으로 lookup 제거를 확인한다.

---

## Ⅳ. 특징

| 구분 | 클러스터드 인덱스 | 커버링 인덱스 | 판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 데이터 저장 순서 최적화 | 테이블 재조회 제거 | range scan vs index-only scan |
| 개수 | 테이블당 1개 | 여러 개 가능 | 워크로드별 선별 |
| 장점 | 범위 조회 page locality | bookmark lookup 0건 | buffer read 감소 |
| 비용 | page split, key 변경 비용 | 인덱스 폭·쓰기 비용 증가 | 포함 컬럼 최소화 |

> 요약: 클러스터드는 배치 순서, 커버링은 반환 컬럼 포함으로 I/O를 줄이나 쓰기 비용과 저장공간이 증가한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 일반 B+Tree+table fetch | clustered 또는 covering | lookup 비율 30% 이상인 SQL |
| 비용/성능 | 랜덤 I/O 반복 | index-only 또는 연속 page scan | buffer read 50% 감소 목표 |
| 운영/위험 | 인덱스 폭 작음 | page split, storage 증가 | write-heavy 테이블은 컬럼 제한 |

> 요약: key lookup이 병목이면 커버링, 범위 page locality가 병목이면 클러스터드 키 재검토가 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| page split 증가 | 순서 없는 UUID clustered key | sequential key, fillfactor 조정 | fragmentation 30% 이하 |
| 인덱스 폭 증가 | include 컬럼 과다 | SELECT 컬럼 최소화, covering 후보 제한 | index size/table size 30% 이하 |
| 실행 계획 회귀 | 통계 변경, parameter sniffing | statistics update, plan baseline | key lookup count 0건 |

> 요약: 물리 인덱스 최적화는 page split, 인덱스 폭, 실행 계획 회귀를 함께 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Lookup 제거 | bookmark/key lookup 0건 | Explain Plan, actual plan |
| I/O 감소 | logical read 50% 이상 감소 | DB statistics IO |
| 쓰기 영향 | insert/update p95 100ms 이하 | APM, DB wait event |

> 요약: 적용 후에는 lookup 제거, logical read 감소, 쓰기 지연을 동시에 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 최근 주문 목록처럼 `tenant_id`, `created_at` 범위·정렬 조건이 반복되는 SQL에 `(tenant_id, created_at)` key와 `status, amount` include를 설계함
2. UUID PK 테이블은 clustered key를 별도 sequential key로 검토하고 fragmentation 30% 초과 시 rebuild 또는 fillfactor 조정을 수행함
3. 커버링 인덱스 후보는 상위 10개 read SQL로 제한하고 index size/table size 30% 초과 시 제거·통합을 검토함

**결론 (2줄):**
- 기술사 판단: 범위 조회 병목은 클러스터드 배치, lookup 병목은 커버링 인덱스로 풀되 쓰기 비중이 높으면 적용 범위를 제한함
- 향후 방향: workload replay와 automatic plan regression 검사를 통해 인덱스 변경의 I/O 효과와 회귀를 함께 검증해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "클러스터드·커버링 인덱스를 설명하시오" | key/include 설계와 index-only scan 흐름 | 두 인덱스의 목적·비용 비교 |
| 요구사항 명시형 | "튜닝 방안을 제시하시오", "비교하시오" | lookup 제거, logical read 측정 절차 | 쓰기 overhead와 fragmentation 대응 |

> 요약: 설명형은 구조 차이, 튜닝형은 lookup과 I/O 지표 중심으로 작성한다.
