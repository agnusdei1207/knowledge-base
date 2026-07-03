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
- **개요**: 인덱스는 테이블 전체를 읽지 않고 원하는 행을 빠르게 찾기 위해 key와 행 위치를 별도로 저장한 **보조 자료구조**이자 DB의 **접근 경로(access path)**다.
- **왜 필요한가**: 1억 행 테이블에서 고객번호 1건을 찾을 때, full scan은 테이블 전체 page를 다 읽어야 하지만 B+Tree 인덱스는 높이 3~4단 탐색만으로 후보 행 위치를 찾는다.
- **핵심 직관**: 책을 처음부터 끝까지 읽는 대신, 뒤쪽 색인에서 단어가 있는 쪽번호를 먼저 찾고 그 쪽만 펼치는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 접근 경로 (Access Path, 상위 개념) | DBMS가 원하는 행에 도달하는 방법 전체(full scan 포함) — 인덱스는 그 하나 | 목적지까지 가는 여러 경로 중 하나 |
| B+Tree Index | root-branch-leaf로 key를 정렬 저장, 등가·범위 검색 모두 지원 | 가나다순 색인, 범위도 한 번에 훑을 수 있음 |
| Hash Index | key의 해시값으로 등가 검색만 지원, 정렬 성질 없음 | 사물함 번호로 정확히 찾는 것, "번호 순으로 쭉" 은 못 함 |
| Composite Index (복합 인덱스) | 여러 컬럼을 지정한 순서대로 결합한 인덱스 | 전화번호부의 "성 → 이름" 순 정렬 |
| Leftmost Prefix | 복합 인덱스에서 앞쪽 컬럼부터 순서대로 조건에 걸려야 인덱스가 유효함 | 성 없이 이름만으로는 전화번호부를 못 찾음 |
| 선택도 (Selectivity) | 조건을 걸었을 때 걸러지는 행의 비율(낮을수록 좁혀짐) | 그물눈이 촘촘할수록(선택도 낮을수록) 적게 걸림 |
| 카디널리티 (Cardinality) | 컬럼이 가질 수 있는 distinct 값의 개수 | 성별(2가지) vs 이메일(거의 행 수만큼) |
| Full Scan / Index Scan | 테이블 전체를 읽는 방식 vs 인덱스를 거쳐 필요한 부분만 읽는 방식 | 책 전체 읽기 vs 색인으로 쪽만 펼치기 |

## 깊이 이해

### B+Tree 탐색이 왜 빠른가 — 높이로 계산해 보기
- 한 페이지에 key를 100개씩 저장할 수 있다고 하면, 1억 행을 담은 B+Tree의 높이는 log₁₀₀(1억) ≈ 4단이다. 즉 root에서 leaf까지 4번의 페이지 읽기로 원하는 key 근처에 도달한다.
- Full scan은 1억 행을 담은 페이지를 처음부터 끝까지 읽어야 하므로, 페이지 수 기준으로 인덱스 탐색보다 수만~수십만 배 많은 I/O가 발생한다. 이 차이가 "고객번호 1건 조회"에서 인덱스가 결정적인 이유다.

### 선택도·카디널리티로 인덱스 효과를 판별하는 법
- 카디널리티 = distinct 값 개수, 선택도 = distinct 값 개수 ÷ 전체 행 수(낮을수록 조건 하나로 많이 걸러짐을 의미).
- 성별 컬럼(카디널리티 2, 선택도 50%)에 인덱스를 걸어도 조건을 걸면 여전히 절반 가까운 행이 걸린다. 이 경우 인덱스를 통해 흩어진 행들을 랜덤 I/O로 찾아오는 비용이 순차로 다 읽는 full scan보다 오히려 커질 수 있다.
- 반대로 이메일 컬럼(카디널리티 ≈ 행 수, 선택도 ≈ 0%)은 조건 하나로 거의 1건만 남으므로 인덱스 효과가 크다. 실무 경험칙으로는 선택도 5% 이하일 때 index scan이 유리하다고 본다.

### Hash Index와 B+Tree, 언제 무엇을 쓰나
- Hash는 평균 O(1)로 등가 검색이 가장 빠르지만, 해시값에는 정렬 순서가 없어 `BETWEEN`, `<`, `>`, `ORDER BY` 같은 범위 조건에는 쓸 수 없다.
- B+Tree는 O(log n)으로 Hash보다 느리지만 key가 정렬돼 있어 등가·범위·정렬을 모두 지원한다. 그래서 `=` 조건만 반복되는 캐시성 테이블(세션 조회 등)이 아니라면 대부분 B+Tree가 기본 선택이다.

### 복합 인덱스와 Leftmost Prefix — 구체 예
- `(tenant_id, created_at)` 인덱스는 tenant_id 순으로 먼저 정렬하고, 같은 tenant_id 안에서 created_at 순으로 다시 정렬한다.
- `WHERE tenant_id = 10 AND created_at BETWEEN '2026-07-01' AND '2026-07-31'`은 이 인덱스를 그대로 탄다(앞쪽 컬럼부터 순서대로 조건이 걸림).
- `WHERE created_at BETWEEN ...`만 단독으로 쓰면 tenant_id라는 앞쪽 컬럼이 빠져 있어 인덱스를 활용하지 못하고 대부분 full scan이 된다. 전화번호부에서 "성"을 모른 채 "이름"만으로 찾으려는 것과 같다.

### 인덱스가 항상 이득은 아닌 이유 — 쓰기 비용
- 인덱스가 5개 걸린 테이블에 1건을 insert하면, 테이블 본체 1번 쓰기에 더해 인덱스 leaf도 5번 각각 갱신해야 하므로 총 6번의 쓰기가 발생한다. 로그성 테이블처럼 쓰기 비중이 높은 곳에 인덱스를 과도하게 만들면 insert 지연이 눈에 띄게 늘어난다.

## 연결 개념
- 클러스터드·커버링 인덱스 (107) — 인덱스의 물리적 배치와 포함 컬럼을 다루는 심화 개념
- 실행 계획(Explain Plan) — 옵티마이저가 선택도·카디널리티 통계를 근거로 접근 경로를 고르는 과정을 확인하는 도구
- 정규화·비정규화 — 인덱스 설계와 함께 조회 성능을 좌우하는 또 다른 축

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
