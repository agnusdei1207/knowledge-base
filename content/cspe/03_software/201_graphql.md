---
title: "GraphQL (GraphQL)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 201
---

# 📖 【암기용】 개념 완전 이해

> 목적: GraphQL을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 클라이언트가 필요한 필드를 쿼리로 지정하는 API 질의 언어
- **왜 필요한가**: REST API는 화면마다 엔드포인트를 늘리거나 불필요한 필드를 함께 받는 문제가 생긴다. GraphQL은 단일 엔드포인트에서 필요한 데이터 모양을 클라이언트가 선언한다.
- **핵심 직관**: 서버가 정한 메뉴를 통째로 받는 방식이 아니라, 필요한 반찬만 주문서에 적어 받는 방식이다.

## 깊이 이해
- **배경·문제의식**: 모바일·웹·BFF가 같은 도메인 데이터를 서로 다른 모양으로 요구하면서 over-fetching과 under-fetching이 반복됨.
- **작동 원리**: 스키마에 타입과 필드를 정의하고, 클라이언트는 Query·Mutation·Subscription으로 필요한 필드만 요청함. Resolver는 필드별 데이터 소스를 호출해 응답 JSON을 조립함.
- **비유**: 도서관 사서에게 "책 제목, 저자, 대출 가능 여부만" 적어 요청하면 전체 서지 원장을 복사하지 않고 필요한 칸만 받는 구조임.
- **구체 예시**: 상품 상세 화면에서 `product(id){name price reviews{score}}` 요청 시 3개 REST 호출을 1회 GraphQL 호출로 통합 가능하나, Resolver N+1 방지를 위해 DataLoader 배치 처리 필요.
- **흔한 오해·주의점**: GraphQL은 DB 질의어가 아니다. 인증·인가, 쿼리 깊이 제한, 캐시 정책을 설계하지 않으면 단일 엔드포인트가 과부하 지점이 됨.

## 연결 개념
- BFF(Backend for Frontend) — 화면별 API 조합 계층
- OpenAPI — REST 계약 문서화 방식과 비교 대상
- DataLoader — Resolver N+1 호출 완화 패턴

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
