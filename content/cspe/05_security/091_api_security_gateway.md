---
title: "API 보안 게이트웨이 (API Security Gateway)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 91
---

# 📖 【암기용】 개념 완전 이해

> 목적: API 보안 게이트웨이를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: API 앞단에서 인증, 인가, 호출량, 입력 스키마, 공격 패턴, 로그를 한 번에 집행하는 보안 경계
- **왜 필요한가**: MSA와 외부 연계 API는 수십 개 서비스로 분산된다. 각 서비스가 토큰 검증과 rate limit을 따로 구현하면 누락 지점이 생기므로 Gateway에서 공통 통제를 먼저 적용해야 한다.
- **핵심 직관**: API Gateway는 건물 1층 보안검색대이고, 각 서비스는 층별 출입문이다. 1층에서 신분과 반입 물품을 확인하고, 층별 문에서도 권한을 다시 확인한다.

## 깊이 이해
- **배경·문제의식**: API는 모바일 앱, 파트너, 내부 서비스, 자동화 도구가 직접 호출한다. 토큰 검증 위치가 서비스마다 다르면 만료 토큰, scope 초과, JSON schema 우회, DDoS성 호출이 특정 API로 유입된다.
- **작동 원리**: Gateway는 TLS 종료 후 OAuth2/OIDC JWT, API Key, mTLS 인증서를 검증한다. 이후 path/method별 scope와 RBAC/ABAC 정책, JSON Schema, WAF rule, token bucket rate limit을 적용하고, 실패 사유를 401/403/429/4xx 로그로 남긴다.
- **비유**: 공항 출국장처럼 여권 확인, 탑승권 확인, 수하물 검사, 대기열 제한, CCTV 기록이 한 곳에서 먼저 수행되는 구조이다.
- **구체 예시**: `/payment/refund`는 `aud=payment-api`, `scope=refund:write`, mTLS SAN 등록, JSON Schema 검증, client별 100 TPS 제한을 통과해야 백엔드로 전달한다.
- **흔한 오해·주의점**: Gateway만 통과하면 백엔드는 신뢰해도 된다는 판단은 위험하다. Resource Server는 소유권, tenant-id, 업무 권한을 재검증해야 한다.

## 연결 개념
- OAuth2/OIDC - 토큰 발급과 사용자 신원 확인
- WAF/API Schema Validation - 입력과 공격 패턴 차단
- Zero Trust - Gateway 이후 서비스 계층 재검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: API Gateway 제품명을 나열하지 않고, 신뢰 경계에서 인증·인가·스키마·호출량·관측성을 어디서 집행하는지로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 보안 게이트웨이는 API 진입점에서 authn, authz, rate limit, schema validation, WAF, observability를 공통 집행하는 보안 프록시임
> 2. **가치**: 토큰 검증 누락, 권한 초과, JSON 구조 변조, 자동화 대량 호출을 Gateway와 Resource Server의 이중 경계로 통제함
> 3. **판단 포인트**: Gateway는 1차 검증, 백엔드는 객체 소유권과 업무 권한 재검증, 로그는 401/403/429와 trace-id로 분리해야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 신뢰 경계 설계 확인 | Gateway, Resource Server, IdP, WAF, SIEM 역할 분리 | Gateway만 두면 보안 통제가 끝난다고 서술 |
| 인증·인가·입력 검증 연결 확인 | JWT iss/aud/exp/scope, RBAC/ABAC, JSON Schema | 인증과 인가를 같은 단계로 처리 |
| 운영 탐지 역량 확인 | rate limit, 401/403/429, audit log, trace-id | 실패 로그와 재인증 기준 누락 |

> 요약: 이 문제는 API 진입점의 통제와 백엔드 재검증을 연결하는 보안 아키텍처 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: API 진입점 보안 통제
- 배경: API가 외부 파트너와 내부 MSA로 확산되면 토큰 검증, 호출량 제한, 스키마 검증을 서비스별 코드에 맡기기 어렵다.
- 필요성: OAuth 2.0/OIDC 토큰 검증, API rate limit, JSON Schema 검증을 게이트웨이에 집행하고 백엔드는 업무 권한을 재확인해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> TLS/mTLS -> API Gateway -> Policy/WAF/Rate Limit -> Backend API -> Audit/SIEM
                     / IdP JWKS
                     / Schema Registry
                     / Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Gateway | TLS 종료, 라우팅, JWT 1차 검증 | 401/403/429 응답 분리 |
| Policy Engine | scope, RBAC, ABAC 판단 | path/method/resource 기준 정책 |
| WAF/Schema Validation | OWASP API 공격과 JSON 구조 검증 | JSON Schema, OpenAPI 계약 |
| Rate Limiter | client/IP/token별 호출량 통제 | token bucket, quota, burst |
| Observability | 인증 실패, 지연, 추적 로그 수집 | trace-id, SIEM, APM 연계 |

> 요약: Gateway는 인증·정책·입력·호출량·로그를 공통 처리하고, 백엔드는 업무 객체 권한을 재검증한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> TLS/mTLS 확인 -> JWT/API Key 검증 -> scope/RBAC 판단
-> JSON Schema/WAF 검사 -> rate limit 확인 -> 백엔드 전달 -> 실패 로그 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 채널과 클라이언트 확인 | TLS 1.2+, mTLS SAN, API Key allowlist |
| 2 | 토큰 검증 | `iss`, `aud`, `exp`, `nbf`, `kid`, signature |
| 3 | 인가 판단 | scope, role, tenant, method/path 정책 |
| 4 | 입력·남용 통제 | JSON Schema, OWASP API rule, client별 TPS |
| 5 | 관측·대응 | 401/403/429 로그, trace-id, 재인증 trigger |

> 요약: API 호출은 채널, 토큰, 권한, 입력, 호출량 순서로 검증되고 실패 위치는 로그 코드로 구분된다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | API 보안 게이트웨이 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 인증 | 서비스별 토큰 검증 | Gateway 1차 JWT 검증 | access token 5~15분, JWKS rotation |
| 인가 | URL 단위 허용 | scope+RBAC/ABAC 정책 | 403 사유 코드, tenant 분리 |
| 입력 통제 | 백엔드 파서 의존 | OpenAPI/JSON Schema 검사 | 필수 필드, 타입, 길이 제한 |
| 남용 통제 | 무제한 요청 | token bucket, quota, burst 제한 | client별 TPS, 429 비율 |

> 요약: Gateway는 공통 통제를 앞단에서 표준화하지만, 객체 소유권과 업무 규칙은 백엔드가 다시 확인해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서비스별 보안 코드 | Gateway 공통 정책+서비스 재검증 | API 30개 이상, 파트너 연계 |
| 비용/성능 | 직접 구현 | 관리형 Gateway 또는 Envoy 기반 | p95 gateway latency 20ms 이하 |
| 운영/위험 | 로그 분산 | 중앙 audit, SIEM rule | 401/403/429 분리와 trace-id |

> 요약: API 30개 이상 또는 파트너 연계가 있으면 Gateway 공통 통제를 선택하되, 지연과 정책 편류를 지표로 관리해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 권한 우회 | 백엔드 재검증 누락 | Resource Server에서 소유권·tenant 검증 | IDOR 테스트 0건 |
| 정책 편류 | Gateway와 코드 정책 불일치 | policy-as-code, CI 계약 테스트 | 정책 배포 실패율 |
| 대량 호출 | credential stuffing, bot | rate limit, CAPTCHA trigger, IP reputation | 429 비율, 로그인 실패율 |

> 요약: Gateway 리스크는 백엔드 재검증 누락과 정책 편류이며, 테스트와 로그 지표로 확인해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 토큰 검증 | 부정 JWT 테스트 100% 실패 | negative token corpus, CI |
| 스키마 검증 | OpenAPI 계약 위반 요청 100% 차단 | contract test, gateway log |
| 관측성 | 401/403/429/5xx trace-id 100% 수집 | SIEM dashboard, APM trace |

> 요약: 도입 효과는 부정 토큰, 스키마 위반, 실패 코드 로그가 누락 없이 잡히는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Gateway 정책: OAuth2/OIDC JWT 검증, `iss/aud/exp/scope` 검사, path/method별 RBAC/ABAC 정책을 policy-as-code로 배포
2. 입력·호출량 통제: OpenAPI 기반 JSON Schema, OWASP API rule, client별 token bucket과 429 응답 기준을 운영 지표로 관리
3. 재검증·관측: 백엔드에서 object owner와 tenant-id를 재확인하고 401/403/429 로그를 SIEM, trace-id, 재인증 정책과 연결

**결론 (2줄):**
- 기술사 판단: 공개 API는 Gateway 공통 통제와 백엔드 객체 권한 재검증을 결합하고, B2B 고위험 API는 mTLS를 추가해야 함
- 향후 방향: API 보안은 단일 프록시 통제에서 Zero Trust 기반 요청별 정책 평가와 실시간 위험 점수 반영으로 이동함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "API 보안 게이트웨이를 설명하시오", "기술하시오" | TLS, JWT, scope, schema, rate limit 순서 | Gateway와 Resource Server 역할 차이 |
| 요구사항 명시형 | "설계하시오", "방안을 제시하시오", "비교하시오" | 요구 API별 정책·로그·재인증 흐름 | p95 지연, 401/403/429, IDOR 테스트 기준 |

> 요약: 설명형은 구성과 흐름을 넓게 쓰고, 설계형은 검증 위치와 운영 지표를 중심으로 목차를 바꾼다.
