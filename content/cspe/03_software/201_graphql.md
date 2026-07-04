---
title: "GraphQL (GraphQL)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 201
---

# 📖 【암기용】 개념 완전 이해

> 목적: GraphQL을 처음 보는 사람도 REST와 무엇이 다르고 왜 필요한지, 내부 동작 원리까지 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: GraphQL은 클라이언트가 **타입 스키마**를 기준으로 필요한 필드만 선언해 받는 **API 질의 언어(Query Language)**이며, REST의 엔드포인트별 고정 응답 방식을 대체하는 대안이다.
- **왜 필요한가**: REST API는 화면마다 엔드포인트를 늘리거나(under-fetching 회피), 불필요한 필드까지 함께 받는(over-fetching) 문제가 생긴다. GraphQL은 단일 엔드포인트에서 필요한 데이터 모양을 클라이언트가 직접 선언하게 한다.
- **핵심 직관**: 서버가 정한 정식 메뉴(코스 요리)를 통째로 받는 방식이 아니라, 필요한 반찬만 주문서에 적어 받는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| API 질의 언어 (상위 개념) | 클라이언트가 필요한 데이터의 형태를 직접 요청하는 언어 — REST의 "고정 응답" 방식과 대비됨 | 정해진 메뉴판이 아니라 직접 적는 주문서 |
| 스키마 (Schema, SDL) | 서버가 제공하는 모든 타입·필드·연산을 정의한 계약 | 식당이 만들 수 있는 모든 요리와 재료 목록 |
| 타입 (Type) | 스키마에서 데이터 구조를 정의하는 단위(예: `Product`, `Review`) | 요리 레시피 하나하나 |
| Query / Mutation / Subscription | 조회(Query) / 변경(Mutation) / 실시간 구독(Subscription) — GraphQL의 3가지 연산 종류 | 주문서의 "조회 / 주문 변경 / 실시간 알림 신청" 세 종류 |
| Resolver | 스키마의 필드 하나하나에 대해 실제 데이터를 가져오는 함수 | 각 반찬을 실제로 만들어 오는 담당 주방 담당자 |
| Over-fetching / Under-fetching | 필요 이상으로 많이 받음 / 여러 번 나눠 받아야 함 — REST에서 자주 발생하는 두 가지 문제 | 코스 요리 통째로 받기(과다) / 반찬 하나마다 새로 주문하기(부족) |
| N+1 문제 | 목록 1건 조회 후 각 항목마다 추가 쿼리가 발생해 총 요청이 N+1번이 되는 문제 | 학생 명단 1번 조회 후, 학생마다 담임 선생님을 한 명씩 따로 물어보는 것 |
| DataLoader | 같은 요청 처리 흐름 안에서 발생한 여러 개별 조회를 모아 한 번의 배치 쿼리로 합치는 패턴 | 반 전체 담임을 한 번에 물어보는 것 |

## 깊이 이해

### 왜 GraphQL이 나왔나 (배경)
- 2012년 Facebook이 뉴스피드 화면을 모바일 앱에서 렌더링할 때, 화면마다 필요한 데이터 모양이 달라 REST 엔드포인트가 계속 늘어나거나 불필요한 필드까지 받아오는 문제를 겪으며 내부적으로 개발했다. 2015년 오픈소스로 공개됐다.
- 모바일·웹·파트너 채널(BFF)이 같은 도메인 데이터를 서로 다른 모양으로 요구할수록, REST에서는 "화면 전용 엔드포인트"가 기하급수적으로 늘어난다. GraphQL은 엔드포인트를 1개로 고정하고, **응답 모양을 요청 쪽에서 결정**하게 바꿔 이 문제를 해결했다.

### N+1 문제를 숫자로 이해하기 (워크드 예제)
- 쿼리 `posts { title author { name } }`로 게시글 10건과 각 작성자 이름을 요청한다고 하자.
- Resolver를 단순 구현하면: 게시글 목록 조회 쿼리 1회(`SELECT * FROM posts LIMIT 10`) 후, 게시글마다 작성자를 조회하는 쿼리가 10회 추가로 실행된다(`SELECT * FROM users WHERE id=?`를 10번). 총 **1 + 10 = 11회** DB 호출 — 이것이 N+1 문제다(N=10).
- DataLoader를 적용하면: 같은 실행 틱(tick) 안에서 발생한 10개의 author 조회 요청을 모아 `SELECT * FROM users WHERE id IN (1,2,...,10)` 배치 쿼리 1회로 합친다. 총 호출은 **1 + 1 = 2회**로 줄어든다.
- 판별 원리: 목록 안에서 각 항목마다 관계 필드(author, reviews 등)를 다시 조회하는 구조라면 N+1을 의심해야 한다.

### Over-fetching / Under-fetching을 REST와 비교하기
- REST에서 상품 상세 화면에 이름·가격·리뷰 평점이 필요하면, `GET /products/1`(상품 정보에 설명·재고 등 안 쓰는 필드까지 포함 → over-fetching)과 `GET /products/1/reviews`(리뷰 요약을 위해 별도 호출 필요 → under-fetching)처럼 최소 2회 호출이 필요할 수 있다.
- GraphQL에서는 `product(id:1){ name price reviews{score} }` 쿼리 1회로 필요한 필드만 정확히 받는다 — REST의 여러 호출을 1회로 통합하되, Resolver 뒤에서 발생하는 N+1은 DataLoader로 별도 관리해야 한다.

### 비유와 흔한 오해
- **비유**: 도서관 사서에게 "책 제목, 저자, 대출 가능 여부만" 적어 요청하면, 전체 서지 원장을 복사하지 않고 필요한 칸만 받는 것과 같다.
- **오해**: GraphQL은 DB 질의어(SQL 대체)가 아니다. 스키마와 Resolver 뒤에 어떤 데이터 소스(RDB, REST, gRPC)든 연결할 수 있는 **API 계층**일 뿐이다. 또한 단일 엔드포인트라고 보안이 자동으로 강화되는 것도 아니다 — 인증·인가, 쿼리 깊이 제한(depth limit), 캐시 정책을 별도로 설계하지 않으면 그 하나의 엔드포인트가 과부하·과다 조회의 단일 장애점이 된다.

## 연결 개념
- BFF(Backend for Frontend) — 화면별 API 조합 계층, GraphQL이 대체하려는 패턴
- OpenAPI — REST 계약 문서화 방식과 비교 대상
- DataLoader — Resolver N+1 호출을 배치로 완화하는 패턴

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: GraphQL은 REST 대체 명칭이 아니라, 화면 요구사항 변화와 API 계약 통제를 함께 다루는 질의 계층이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GraphQL은 타입 스키마 기반으로 클라이언트가 필요한 필드만 선언해 받는 API 질의 언어이다.
> 2. **가치**: over-fetching·under-fetching을 줄이고, 웹·모바일·파트너 채널별 응답 모양을 단일 스키마로 통제한다.
> 3. **판단 포인트**: 도입 판단은 화면 다양성, Resolver N+1, 쿼리 복잡도 제한, 필드 단위 인가를 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| REST 한계와 GraphQL 적용 판단 확인 | 단일 엔드포인트, 스키마, Resolver, Query·Mutation·Subscription | GraphQL을 SQL 또는 단순 REST 문서화 도구로 설명 |
| API 설계 역량 확인 | over-fetching, under-fetching, N+1, query depth limit | 장점만 나열하고 운영 통제 누락 |
| 보안·운영 리스크 확인 | 인증, 필드 인가, persisted query, rate limit | 단일 엔드포인트라 보안 통제가 자동 적용된다고 단정 |

> 요약: 이 문제는 GraphQL 구성요소보다 REST 대비 선택 조건과 운영 통제 방안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 응답 필드 선언형 API 질의 언어
- 배경: REST는 리소스별 엔드포인트가 늘어 화면 변경 때 API 조합 비용이 커진다.
- 필요성: schema, resolver, query complexity 제한으로 계약을 고정하고 화면별 데이터 모양을 조정한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Query -> GraphQL Endpoint -> Schema Validation -> Resolver -> Data Source
                              +-> AuthZ / Complexity Limit / Cache
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Schema | 타입, 필드, 입력값, 반환값 계약 정의 | SDL, introspection 통제 |
| Resolver | 필드별 데이터 조회·조립 | N+1 방지 위해 batching 적용 |
| Operation | Query·Mutation·Subscription 실행 | 읽기·쓰기·이벤트 구분 |
| Gateway | Federation·schema stitching | 다중 서비스 스키마 통합 |

> 요약: GraphQL은 스키마 계약, Resolver 실행, 게이트웨이 통제로 데이터 요청 모양을 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Query 작성 -> 스키마 검증 -> 인증/인가 -> Resolver 실행 -> 응답 조립 -> Metric 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 필드 선택 쿼리 작성 | schema validation error 0건 |
| 2 | 토큰·권한·쿼리 깊이 확인 | depth 10 이하, cost limit 적용 |
| 3 | Resolver가 DB·REST·gRPC 호출 | DataLoader batch hit ratio 측정 |
| 4 | JSON 응답 조립 및 오류 반환 | p95 지연 200ms 이하, error rate 1% 이하 |

> 요약: GraphQL 실행은 쿼리 검증, 권한 통제, Resolver 조합, 관측 지표 기록 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | REST API | GraphQL | 판단 포인트 |
|:---|:---|:---|:---|
| 계약 | 엔드포인트·HTTP method 중심 | 타입 스키마·필드 중심 | 화면 변화가 월 5회 이상이면 스키마 방식 검토 |
| 데이터 양 | 고정 응답으로 over-fetching 발생 | 필요한 필드만 선택 | 모바일 응답 payload 30% 이상 감소 사례 |
| 캐시 | URL·method 기반 CDN 캐시 | 쿼리 해시·persisted query 필요 | CDN hit ratio 목표 70% 이상 |
| 운영 | API별 모니터링 단순 | 단일 endpoint 내부 필드 관측 필요 | resolver p95, depth, error path 수집 |

> 요약: GraphQL은 화면 다양성에는 유리하나 캐시·권한·쿼리 비용 통제를 별도 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST 리소스 API | GraphQL schema + resolver | 클라이언트 채널 3개 이상, 응답 모양 차이 큼 |
| 비용/성능 | endpoint 수 증가 | resolver fan-out 증가 | p95 200ms, DB query count 20회 이하 |
| 운영/위험 | URL별 rate limit | query cost별 rate limit | depth·complexity·persisted query 적용 가능 여부 |

> 요약: GraphQL은 화면별 API 조합 비용이 Resolver 운영 비용보다 클 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| N+1 호출 | 필드 Resolver 반복 실행 | DataLoader, batch API | request당 DB query count |
| 과도한 쿼리 | 깊은 nested field 요청 | depth limit, cost analysis | rejected query ratio |
| 인가 누락 | 필드 단위 권한 미분리 | field policy, ABAC | unauthorized field access 0건 |

> 요약: 주요 리스크는 Resolver 폭증과 필드 인가 누락이며, 쿼리 비용과 권한 정책으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 200ms 이하 | Apollo tracing, APM |
| 호출 폭 | request당 DB query 20회 이하 | SQL log, resolver metric |
| 보안 | introspection 운영 차단, persisted query 90% 이상 | gateway policy, audit log |

> 요약: 성공 여부는 지연, 내부 호출 수, 운영 정책 준수율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. Schema-first 설계로 `Query`, `Mutation`, 공통 scalar를 정의하고 schema registry에서 breaking change를 차단함.
2. Resolver에 DataLoader, timeout 300ms, circuit breaker를 적용해 N+1과 fan-out 장애를 통제함.
3. 운영 환경에서 persisted query, depth 10 이하, field-level authorization, audit log를 gateway 정책으로 적용함.

**결론 (2줄):**
- 기술사 판단: 채널별 화면 요구가 잦으면 GraphQL, 리소스 CRUD와 CDN 캐시가 핵심이면 REST를 선택함.
- 향후 방향: Federation, schema registry, contract test를 결합해 다중 팀 API 거버넌스로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GraphQL을 설명하시오" | 쿼리 검증, Resolver 실행, 응답 조립 | REST 대비 계약·캐시·운영 차이 |
| 요구사항 명시형 | "REST와 비교하시오", "도입 방안을 제시하시오" | N+1, depth limit, field auth 통제 | 선택 기준, 리스크 대응, 지표 점검 |

> 요약: 설명형은 스키마와 실행 원리를, 비교·방안형은 REST 대비 선택 조건과 운영 통제를 중심으로 전환한다.
