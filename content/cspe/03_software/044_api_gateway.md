---
title: "API 게이트웨이 (API Gateway)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 44
---

# 📖 【암기용】 개념 완전 이해

> 목적: API Gateway를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라이언트와 내부 서비스 사이의 단일 API 진입점
- **왜 필요한가**: MSA에서 클라이언트가 수십 개 서비스를 직접 호출하면 인증, 라우팅, 버전 관리, rate limit이 흩어짐. Gateway는 공통 정책을 한곳에서 처리함.
- **핵심 직관**: 건물의 안내 데스크처럼 방문자를 확인하고, 목적지로 보내고, 출입 기록과 혼잡을 관리함.

## 깊이 이해
- **배경·문제의식**: 서비스가 늘어나면 클라이언트는 여러 endpoint, 인증 방식, 응답 형식을 알아야 함. 모바일 앱은 한번 배포하면 수정 주기가 길어 API 변화에 취약함.
- **작동 원리**: Gateway는 요청을 받아 인증·인가, 라우팅, rate limit, 프로토콜 변환, 응답 조합을 수행함. BFF는 웹·모바일별 API 형태를 분리함.
- **비유**: 콜센터가 고객 요구를 듣고 담당 부서로 연결하며, 고객에게는 한 번호만 공개하는 방식임.
- **구체 예시**: 모바일 앱이 `/orders/me`를 호출하면 Gateway가 JWT를 검증하고 주문 서비스와 배송 서비스를 호출해 200ms 안에 통합 응답을 구성함.
- **흔한 오해·주의점**: Gateway에 업무 로직을 넣으면 병목과 결합이 생김. Gateway는 정책·중계·변환 중심이고 도메인 판단은 서비스가 담당해야 함.

## 연결 개념
- MSA: Gateway가 서비스 진입점을 통합
- BFF: 클라이언트 유형별 API 최적화
- Rate Limiting: 과도한 요청과 장애 전파 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: API Gateway는 라우팅 장비가 아니라 인증, rate limit, 변환, BFF, 관측성, 단일 장애점 대응을 포함한 API 통제 계층이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API Gateway는 클라이언트 요청을 단일 진입점에서 받아 내부 서비스로 라우팅하고 공통 API 정책을 집행하는 계층이다.
> 2. **가치**: 인증·인가, rate limit, routing, transformation, aggregation을 중앙에서 처리해 클라이언트 복잡도와 정책 중복을 줄임.
> 3. **판단 포인트**: Gateway는 병목과 단일 장애점이 될 수 있으므로 HA 구성, timeout, circuit breaker, cache, observability가 필수임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Gateway 역할 이해 확인 | routing, auth, rate limit, transformation, aggregation | 단순 reverse proxy로만 설명 |
| MSA 연계 판단 확인 | BFF, service discovery, circuit breaker | Gateway에 도메인 로직 집중 |
| 운영 리스크 확인 | HA, 단일 장애점, latency, observability | Gateway 병목과 장애 전파 누락 |

> 요약: 이 문제는 API 진입점 통합과 정책 집행을 분리해, Gateway의 가치와 위험을 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라이언트 API 단일 진입점
- 배경: MSA에서 서비스 수가 증가하면 인증, 라우팅, 버전, rate limit, CORS 정책이 각 서비스에 흩어져 정책 누락과 클라이언트 결합이 발생함.
- 필요성: API Gateway로 OAuth2/OIDC, routing, throttling, request aggregation을 중앙 적용하고 4xx/5xx 비율과 upstream latency를 관측해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway
          / AuthN/AuthZ -> Token validation
          / Routing -> Service Discovery -> Service
          / Policy -> Rate Limit / Quota / WAF
          / Transform -> REST / gRPC / JSON mapping
Gateway -> Log / Metric / Trace
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Routing Engine | URI, header, version 기반 서비스 전달 | service discovery 연계 |
| Security Filter | JWT, OAuth2, API key 검증 | RBAC, scope 기반 권한 |
| Traffic Policy | rate limit, quota, timeout, retry | tenant별 TPS 제한 |
| Transformation/BFF | 응답 조합, 포맷 변환 | 업무 로직 집중 금지 |

> 요약: Gateway는 라우팅, 보안, 트래픽 정책, 변환을 담당하고 서비스는 도메인 로직을 유지한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request 수신 -> TLS 종료 -> 인증/인가 검증
-> Rate Limit 확인 -> Route 매칭 -> Backend 호출
-> 응답 변환/집계 -> 로그/메트릭/트레이스 기록 -> Response 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | mTLS/TLS 종료와 token 검증 | 401/403 비율, 인증 지연 |
| 2 | rate limit과 quota 적용 | tenant별 TPS, 429 비율 |
| 3 | service discovery 기반 라우팅 | route miss 0건, endpoint health |
| 4 | 응답 변환과 aggregation | p95 Gateway latency 50ms 이하 |
| 5 | 로그·메트릭·트레이스 수집 | access log 100%, trace ID 전파 |

> 요약: Gateway는 요청 수신부터 정책 검증, 라우팅, 변환, 관측까지 API 경계 처리를 순차 수행한다.

---

## Ⅳ. 특징

| 구분 | 직접 서비스 호출 | API Gateway 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 클라이언트 복잡도 | 서비스 endpoint 직접 관리 | 단일 endpoint 제공 | 모바일 API 변경 횟수 감소 |
| 보안 정책 | 서비스별 중복 구현 | 중앙 인증·인가 | OAuth2, JWT, mTLS |
| 트래픽 제어 | 서비스별 제각각 | TPS, quota, burst 통제 | 429 비율 1% 이하 |
| 장애 리스크 | 일부 서비스 영향 | Gateway 병목 가능 | active-active 2개 AZ 구성 |

> 요약: Gateway는 API 정책을 통합하지만 고가용성과 지연 관리가 없으면 전체 API 경계의 병목이 된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | client to service 직접 호출 | Gateway 단일 진입점 | 공개 API 10개 이상, 인증 정책 중복 |
| 비용/성능 | 홉 1개 적음 | Gateway hop 추가 | Gateway p95 latency 50ms 이하 |
| 운영/위험 | 정책 분산 | 정책 중앙화 | HA 99.9%, config rollback 10분 |

> 요약: Gateway는 API 정책 중복과 클라이언트 복잡도가 임계치를 넘을 때 적용하며 지연 예산을 별도로 둔다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단일 장애점 | Gateway 장애 | multi-AZ active-active, health check | availability 99.9% 이상 |
| 지연 증가 | aggregation, filter 과다 | cache, timeout, BFF 분리 | p95/p99 latency |
| 정책 오류 | route/rate limit 오설정 | config canary, policy test | 5xx, 429 급증 탐지 |

> 요약: Gateway 리스크는 장애점과 지연 증가이며, HA 구성과 정책 테스트로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | 99.9% 이상, RTO 10분 이하 | synthetic monitoring, health check |
| 지연 | Gateway p95 50ms 이하 | APM, access log |
| 보안·정책 | 인증 실패율, rate limit hit ratio | audit log, WAF log |

> 요약: Gateway 운영은 가용성, 지연, 정책 집행 지표를 동시에 관리해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Kong, Apigee, NGINX, Spring Cloud Gateway 중 조직 표준을 선정하고 OAuth2/JWT, mTLS, API key 정책을 표준화함.
2. 모바일·웹별 BFF를 분리하고 aggregation API는 p95 200ms 목표와 backend timeout 1초 이하 기준을 둠.
3. Gateway config를 GitOps로 관리하고 route, rate limit, auth policy를 CI에서 테스트한 뒤 canary 10%로 배포함.

**결론 (2줄):**
- 기술사 판단: 공개 API와 인증 정책이 분산되면 Gateway를 적용하고, 서비스 간 내부 통신 정책은 service mesh와 역할을 분리함.
- 향후 방향: Gateway는 zero trust, API security, GraphQL federation, BFF와 결합해 API 제품 관리 계층으로 확장됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "API Gateway를 설명하시오" | 인증, 라우팅, 변환, rate limit 흐름 | 직접 호출 대비 정책 중앙화 |
| 요구사항 명시형 | "설계하시오", "장애 대응 방안을 제시하시오" | HA, timeout, circuit breaker, BFF 구성 | 단일 장애점, 지연, 정책 오류 대응 |

> 요약: 설명형은 역할과 흐름, 설계형은 고가용성·지연 예산·정책 검증 중심으로 전환한다.
