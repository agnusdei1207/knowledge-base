---
title: "인덱스 구조 — B+Tree·해시·복합 (Index Structure)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 106
---

# 📖 【암기용】 개념 완전 이해

> 목적: 인덱스 구조를 처음 보는 사람도 왜 어떤 쿼리는 인덱스를 타고 어떤 쿼리는 full scan이 되는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 테이블 행을 더 적은 I/O로 찾기 위해 key와 row 위치를 별도 구조로 저장한 접근 경로
- **왜 필요한가**: 1억 행 테이블에서 고객번호 1건을 찾을 때 full scan은 수십만 page를 읽지만 B+Tree는 높이 3~4회 탐색으로 후보 행을 찾는다.
- **핵심 직관**: 책 전체를 처음부터 읽지 않고 뒤쪽 색인에서 단어 위치를 찾은 뒤 해당 쪽만 여는 방식이다.

## 깊이 이해
- **배경·문제의식**: 테이블은 저장 순서와 조회 조건이 항상 일치하지 않는다. 조건 컬럼에 인덱스를 만들면 DBMS가 선택도와 카디널리티를 근거로 full scan 대신 index scan을 선택할 수 있다.
- **작동 원리**: B+Tree는 root, branch, leaf 노드로 정렬된 key를 저장해 등가·범위 검색을 지원한다. Hash index는 key 해시값으로 등가 검색을 처리하나 범위 검색에는 맞지 않는다. Composite index는 컬럼 순서에 따라 leftmost prefix 규칙을 따른다.
- **비유**: 도서관에서 저자명 색인은 가나다 범위 검색이 가능하고, 사물함 번호 해시는 정확한 번호 검색에만 맞는 것과 같다.
- **구체 예시**: `(tenant_id, created_at)` 복합 인덱스는 `tenant_id = 10 and created_at between '2026-07-01' and '2026-07-31'`에는 쓰이나 `created_at` 단독 조건에는 선행 컬럼 누락으로 활용도가 낮다.
- **흔한 오해·주의점**: 인덱스가 많을수록 조회가 모두 개선되는 것은 아니다. INSERT, UPDATE, DELETE마다 인덱스도 갱신되어 쓰기 지연과 저장공간이 증가한다.

## 연결 개념
- Selectivity — 조건이 줄이는 행 비율
- Cardinality — 컬럼 값의 distinct 수
- Query Optimizer — 통계를 기반으로 접근 경로 선택

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 인덱스는 자료구조 암기가 아니라 쿼리 패턴, 선택도, 쓰기 비용을 함께 보는 접근 경로 설계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인덱스는 key와 row locator를 B+Tree, Hash, Bitmap, Composite 구조로 저장해 테이블 접근 I/O를 줄이는 자료구조이다.
> 2. **가치**: 선택도 높은 조건에서 full scan page 수를 줄이고 정렬·조인·범위 검색 비용을 낮춘다.
> 3. **판단 포인트**: 카디널리티, 선택도, 범위 조건, 컬럼 순서, DML 유지 비용을 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DB 접근 경로 설계 이해 확인 | B+Tree, Hash, Composite 구조와 사용 조건 | 인덱스를 무조건 조회 개선 수단으로 단정 |
| 옵티마이저 판단 기준 확인 | selectivity, cardinality, statistics, range scan | 컬럼 순서와 leftmost prefix 누락 |
| 운영 비용 인식 확인 | write overhead, storage, fragmentation, rebuild | DML 성능 영향 설명 누락 |

> 요약: 이 문제는 인덱스 종류를 쿼리 조건과 유지 비용에 맞게 선택하는 판단력을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 인덱스는 테이블 행 접근 경로이다.
- 배경: 대용량 테이블에서 조건 검색, 조인, 정렬을 full scan으로 처리하면 buffer read, CPU, temp I/O 비용이 증가한다.
- 필요성: B+Tree, Hash, Composite Index를 선택도, 카디널리티, leftmost prefix, DML 유지 비용 기준으로 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Query Predicate -> Index Key -> Leaf Entry -> Row Locator -> Table Row
                 / B+Tree
                 / Hash
                 / Composite
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| B+Tree Index | 정렬된 key로 등가·범위 검색 지원 | height 3~4 수준, range scan 가능 |
| Hash Index | 해시 bucket으로 등가 검색 지원 | `=` 조건 중심, range 조건 부적합 |
| Composite Index | 여러 컬럼을 순서대로 결합 | leftmost prefix 규칙 적용 |
| Leaf Entry | key와 row locator 저장 | covering index면 테이블 접근 생략 |
| Statistics | 카디널리티·히스토그램 제공 | optimizer plan 선택 근거 |

> 요약: 인덱스는 key, leaf, row locator, 통계를 통해 조건에 맞는 행 위치를 빠르게 찾는 접근 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
조건 분석 -> 통계 조회 -> 인덱스 후보 선택 -> leaf 탐색 -> row fetch 또는 index-only scan
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | WHERE, JOIN, ORDER BY 컬럼 식별 | 실행 빈도 상위 SQL |
| 2 | 카디널리티와 선택도 계산 | 선택도 5% 이하 후보 |
| 3 | B+Tree, Hash, Composite 선택 | 범위 검색은 B+Tree |
| 4 | Explain Plan으로 access path 확인 | index seek/scan 여부 |
| 5 | DML 유지 비용과 저장공간 측정 | insert p95, index size 확인 |

> 요약: 인덱스 설계는 조건 컬럼 분석, 통계 확인, 구조 선택, 실행 계획 검증, DML 비용 측정 순서로 수행한다.

---

## Ⅳ. 특징

| 구분 | B+Tree | Hash | Composite |
|:---|:---|:---|:---|
| 적합 조건 | 등가, 범위, 정렬 | 등가 검색 | 다중 조건, 조인 |
| 부적합 조건 | 선택도 낮은 컬럼 단독 | range, order by | 선행 컬럼 누락 |
| 비용 | leaf split, fragmentation | bucket collision | 컬럼 순서 설계 비용 |
| 판단 지표 | selectivity, clustering factor | equality hit ratio | leftmost prefix 사용률 |

> 요약: B+Tree는 범용, Hash는 등가 조건, Composite는 컬럼 순서가 맞는 다중 조건에서 사용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Full Table Scan | Index Scan/Seek | 선택도 5% 이하, 반환 행 적음 |
| 비용/성능 | 순차 I/O 많음 | 랜덤 I/O와 leaf 탐색 | 반환 행 20% 이상이면 full scan 검토 |
| 운영/위험 | DML 유지 비용 없음 | 인덱스 갱신·저장공간 증가 | write-heavy 테이블은 개수 제한 |

> 요약: 인덱스는 반환 행이 적고 조건 컬럼 선택도가 높을 때 유리하며, 대량 반환은 full scan이 더 낮은 비용일 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 미사용 인덱스 | 쿼리 패턴 변경 | usage statistics 기반 제거 | index scan count 0건 |
| 쓰기 지연 | 인덱스 과다, leaf split | 인덱스 개수 제한, fillfactor 조정 | insert p95 100ms 이하 |
| 잘못된 실행 계획 | 통계 노후, skew 데이터 | analyze, histogram 생성 | estimated vs actual row 오차 10배 이하 |

> 요약: 인덱스 운영은 사용률, 쓰기 지연, 통계 정확도를 지속 점검해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접근 경로 | 핵심 SQL index seek 사용 | Explain Plan, AWR |
| 선택도 | 후보 컬럼 selectivity 5% 이하 | distinct count, histogram |
| 유지 비용 | index size/table size 30% 이하 | catalog, storage report |

> 요약: 인덱스 적합성은 실행 계획, 선택도, 저장공간 비율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 상위 20개 slow SQL의 WHERE, JOIN, ORDER BY 컬럼을 추출하고 선택도 5% 이하 컬럼부터 B+Tree 후보로 선정함
2. 복합 인덱스는 등가 조건 컬럼, 범위 조건 컬럼, 정렬 컬럼 순으로 배치하고 leftmost prefix 사용률을 Explain Plan으로 확인함
3. 월 1회 미사용 인덱스와 중복 인덱스를 제거해 index size/table size 30% 이하, insert p95 100ms 이하를 유지함

**결론 (2줄):**
- 기술사 판단: 읽기 병목은 인덱스 후보이나, 쓰기 비중 50% 이상 테이블은 인덱스 개수와 컬럼 폭을 제한함
- 향후 방향: 자동 튜닝, adaptive statistics, workload 기반 인덱스 추천을 운영 승인 체계와 결합해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "인덱스 구조를 설명하시오" | 조건 분석 -> 통계 -> 접근 경로 선택 | B+Tree·Hash·Composite 비교 |
| 요구사항 명시형 | "튜닝 방안을 제시하시오", "비교하시오" | slow SQL 기반 설계 절차 | 선택도·쓰기 비용·미사용 인덱스 리스크 |

> 요약: 설명형은 구조와 원리, 튜닝형은 선택도와 실행 계획 검증 중심으로 작성한다.
