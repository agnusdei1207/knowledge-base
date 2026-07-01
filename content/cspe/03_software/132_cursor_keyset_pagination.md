---
title: "DB 커서·키셋 페이지네이션 (Cursor Keyset Pagination)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 132
---

# 📖 【암기용】 개념 완전 이해

> 목적: 커서·키셋 페이지네이션이 OFFSET 방식의 어떤 병목을 줄이는지 이해하게 만든다.

## 한눈에
- **개요**: 마지막으로 본 정렬 키를 기준으로 다음 페이지를 조회하는 방식
- **왜 필요한가**: `OFFSET 100000 LIMIT 20`은 앞 100000건을 건너뛰는 비용과 중복·누락 문제가 발생함.
- **핵심 직관**: 책의 100000쪽을 매번 세는 대신, 책갈피 위치 다음부터 20개를 읽는 방식임.

## 깊이 이해
- **배경·문제의식**: 무한 스크롤·피드·주문 목록은 페이지가 뒤로 갈수록 OFFSET 비용이 증가함. 동시에 새 row가 삽입되면 사용자가 같은 항목을 다시 보거나 일부를 건너뛸 수 있음.
- **작동 원리**: 정렬 기준을 `(created_at, id)`처럼 유일하게 만들고, 마지막 row의 key를 cursor로 전달함. 다음 조회는 `where (created_at, id) < (:last_created_at, :last_id)` 조건과 index range scan으로 수행함.
- **비유**: 번호표를 들고 줄을 서는 방식임. "50번째 사람부터"가 아니라 "번호 835 다음 사람부터"라고 찾음.
- **구체 예시**: `order by created_at desc, id desc limit 20`에서 마지막 값이 `2026-07-01 10:00, 931`이면 다음 페이지는 그보다 작은 tuple 20건을 index로 읽음.
- **흔한 오해·주의점**: 키셋은 임의 페이지 이동에 약함. "37페이지로 이동"이 필요한 관리자 화면은 OFFSET 또는 search_after 보완이 필요함.

## 연결 개념
- B-Tree Index — range scan 기반
- Covering Index — 목록 조회 I/O 절감
- MVCC — 조회 중 삽입·삭제 가시성 제어

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 페이지네이션 문제에서 OFFSET 병목, 정렬 키 설계, 인덱스·일관성 판단을 답안화함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 커서·키셋 페이지네이션은 이전 페이지 마지막 정렬 키를 cursor로 사용해 다음 범위를 조회하는 방식임.
> 2. **가치**: deep page에서 OFFSET 스캔을 제거하고, 삽입·삭제 중 목록 중복·누락 가능성을 줄임.
> 3. **판단 포인트**: 유일 정렬 키, 복합 인덱스, cursor 인코딩, 역방향 조회 지원 여부가 설계 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SQL 성능 병목 이해 확인 | OFFSET scan vs index range scan | LIMIT만 쓰면 해결된다고 서술 |
| API 설계 역량 확인 | cursor token, sort key, next/prev 방향 | cursor 위변조·만료 정책 누락 |
| 데이터 일관성 판단 확인 | tie-breaker id, MVCC snapshot | created_at 단일 정렬로 중복 발생 |

> 요약: 이 문제는 페이지 UI가 아니라 정렬 키와 인덱스로 조회 비용과 일관성을 통제하는 설계를 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: 키셋 페이지네이션은 마지막 정렬 키 이후 조회 방식임.
- 배경: 대량 목록에서 OFFSET은 페이지 후반으로 갈수록 스캔 비용이 증가하고 동시 삽입·삭제 시 중복·누락이 생김.
- 필요성: 정렬 키 기반 range scan으로 API 응답 지연과 목록 일관성 문제를 줄임.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> cursor token -> API -> SQL Predicate
                         / Sort Key: created_at + id
                         / Composite Index -> Result + next_cursor
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Sort Key | 목록 순서 결정 | created_at 단독 금지, id tie-breaker 필요 |
| Cursor Token | 마지막 key 전달 | Base64+HMAC, 만료시간 포함 |
| Predicate | 다음 범위 조건 | tuple comparison 또는 OR 조건 |
| Composite Index | range scan 수행 | order by와 where 순서 일치 |

> 요약: 키셋 페이지네이션은 유일 정렬 키와 복합 인덱스가 맞아야 deep page에서도 index range scan으로 동작함.

---

## Ⅲ. 동작원리 및 흐름도

```text
첫 요청 -> ORDER BY key LIMIT N -> last key 추출
-> cursor 생성 -> 다음 요청 -> WHERE key < last key
-> index range scan -> N건 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 첫 페이지 조건 없이 최신 N건 조회 | index only scan 여부 |
| 2 | 마지막 row의 복합 key 추출 | key null·중복 여부 |
| 3 | cursor 서명·인코딩 | HMAC 검증, TTL 확인 |
| 4 | 다음 페이지 range 조건 실행 | examined rows와 returned rows 비율 |

> 요약: cursor는 페이지 번호가 아니라 마지막 row의 위치이며, 다음 조회는 그 위치 이후의 index 범위만 읽음.

---

## Ⅳ. 특징

| 구분 | OFFSET 페이지네이션 | 키셋 페이지네이션 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 조회 비용 | offset+limit만큼 스캔 | limit 범위 중심 스캔 | 100000 offset 시 examined rows 100020 |
| 일관성 | 삽입·삭제 시 중복·누락 | 마지막 key 기준 연속성 | created_at+id 유일 정렬 |
| UX | 임의 페이지 이동 가능 | 다음/이전 이동 중심 | 검색 결과·피드에 적합 |
| 구현 | 단순 SQL | cursor token·복합 조건 필요 | HMAC, TTL, 방향 정보 |

> 요약: 키셋은 대량 피드와 무한 스크롤에 적합하고, 임의 페이지 이동 요구가 강하면 OFFSET과 병행 검토함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | page number + offset | cursor + sort key | 무한 스크롤, deep page 조회 |
| 비용/성능 | 후반 페이지 스캔 증가 | index range scan | p95 목록 API 100ms 이하 목표 |
| 운영/위험 | 구현 단순 | cursor 위변조·버전 관리 | public API는 signed cursor 필수 |

> 요약: 키셋은 조회 패턴이 순차 탐색일 때 선택하고, 보고서형 화면은 OFFSET·검색 엔진 조합을 고려함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복·누락 | 정렬 키 중복 | id tie-breaker 추가 | duplicate item 0건 |
| full scan | 인덱스 순서 불일치 | `(created_at, id)` 복합 인덱스 | rows examined/returned 5 이하 |
| cursor 위변조 | client token 노출 | HMAC 서명, TTL 24시간 | invalid cursor rate |

> 요약: 정렬 키와 인덱스가 맞지 않으면 키셋도 full scan이 되므로 실행계획 검증이 필수임.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| API 지연 | p95 100ms 이하 | APM, DB slow query |
| 스캔 효율 | examined/returned 5 이하 | EXPLAIN ANALYZE |
| 일관성 | 중복·누락 재현 0건 | 동시 삽입 부하 테스트 |

> 요약: 키셋 도입 효과는 지연, 스캔 행 수, 중복·누락 재현 여부로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. `order by created_at desc, id desc`와 동일한 복합 인덱스를 생성하고 LIMIT는 20~100 범위로 제한함
2. cursor token은 sort key, direction, page size, expires_at을 JSON으로 담고 HMAC-SHA256으로 서명함
3. 이전 페이지는 반대 비교 연산과 reverse order를 사용하고, 임의 페이지 이동 화면은 별도 검색 조건으로 분리함

**결론 (2줄):**
- 기술사 판단: 무한 스크롤·피드·로그 목록은 키셋, 페이지 번호 이동이 핵심인 관리자 목록은 OFFSET 또는 검색 엔진을 선택함
- 향후 방향: API pagination은 cursor 표준화와 GraphQL Connection 모델 기반으로 확산됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "커서 페이지네이션을 설명하시오" | cursor 생성과 range scan 흐름 | OFFSET 대비 비용·일관성 |
| 요구사항 명시형 | "성능 개선 방안을 제시하시오" | 실행계획, 복합 인덱스, token 검증 | deep page 병목 제거와 UX 선택 기준 |

> 요약: 설명형은 원리 중심, 개선 방안형은 EXPLAIN 수치와 인덱스 설계 중심으로 전개함.
