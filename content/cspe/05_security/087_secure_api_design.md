---
title: "보안 API 설계 - JWT·OAuth·mTLS (Secure API Design)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 87
---

# 📖 【암기용】 개념 완전 이해

> 목적: 보안 API 설계를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: API 호출자를 인증하고 권한·토큰·전송 구간·호출량을 통제하는 설계 방식
- **왜 필요한가**: API는 내부 서비스, 모바일 앱, 파트너 시스템이 직접 호출한다. 토큰 검증, audience 제한, mTLS, rate limit이 없으면 탈취 토큰 재사용·권한 초과·대량 호출이 발생한다.
- **핵심 직관**: API 보안은 "누가", "어떤 서비스에", "얼마나", "어떤 채널로" 들어오는지 계속 확인하는 검문소임

## 깊이 이해
- **배경·문제의식**: 세션 기반 웹과 달리 API는 Stateless 호출이 많아 매 요청마다 JWT, scope, client certificate, quota를 검증해야 한다. OAuth2는 위임 권한, OIDC는 사용자 신원, mTLS는 클라이언트 인증서 기반 채널 신뢰를 담당한다.
- **작동 원리**: Client가 Authorization Server에서 access token을 발급받고 API Gateway에 제시한다. Gateway와 Resource Server는 issuer, audience, exp, nbf, signature, scope를 검증하고, 고위험 B2B 호출은 mTLS로 클라이언트 인증서를 추가 확인한다.
- **비유**: 건물 출입증(JWT), 방문 목적(scope), 출입문별 허용 구역(audience), 회사 배지(mTLS), 혼잡 제한(rate limit)을 함께 확인하는 절차와 같다.
- **구체 예시**: `aud=payment-api`, `iss=https://idp.example.com`, `exp` 5분, `scope=payment:write`가 모두 맞아야 결제 API를 호출한다. 인증서 CN/SAN은 등록된 client_id와 매핑한다.
- **흔한 오해·주의점**: JWT 서명만 맞으면 충분하지 않다. `alg`, `kid`, `iss`, `aud`, `exp`, `scope`, token binding, revocation 전략까지 봐야 한다.

## 연결 개념
- OAuth 2.0/OIDC - 위임 권한과 신원 확인 표준
- Zero Trust - 요청마다 인증·인가·컨텍스트 검증
- API Gateway - 인증, 인가, rate limit, 로깅의 집행 지점

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: JWT·OAuth·mTLS를 표준명으로 나열하지 않고, API 신뢰 경계에서 토큰·인증서·호출량을 어디서 검증하는지로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 보안 API 설계는 OAuth2/OIDC JWT 검증, scope 기반 인가, mTLS 클라이언트 인증, rate limit을 요청 경계마다 집행하는 구조임
> 2. **가치**: 탈취 토큰 재사용, audience 혼동, 권한 초과 호출, 대량 요청을 API Gateway와 Resource Server에서 이중 검증함
> 3. **판단 포인트**: issuer, audience, exp, nbf, signature, scope, certificate binding, quota 로그를 누락 없이 연결해야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 인증·인가 구조 설계 확인 | OAuth2/OIDC, JWT validation, scope/RBAC/ABAC | JWT 발급 절차만 쓰고 Resource Server 검증 누락 |
| 신뢰 경계와 전송 채널 통제 확인 | API Gateway, mTLS, certificate pinning, TLS 1.2+ | HTTPS만 쓰면 충분하다고 단정 |
| 운영 통제와 실패 모드 확인 | 401/403/429 분리, rate limit, audit log | 인증 실패와 권한 실패를 같은 오류로 처리 |

> 요약: 이 문제는 API 표준 암기가 아니라 토큰·인증서·권한·호출량을 어느 경계에서 검증하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: API 요청 보안 통제 구조
- 배경: API는 브라우저 밖의 서버, 앱, 파트너가 호출하므로 탈취 토큰, 과도한 scope, audience 혼동, 자동화 요청이 매 호출에서 발생할 수 있음.
- 필요성: OAuth 2.0, OIDC, JWT validation, mTLS, rate limit, Gateway·Resource Server 이중 검증을 API 보안 설계 기준으로 적용해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Authorization Server -> Access Token
Client -> mTLS/API Gateway -> JWT Validation -> Resource Server -> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Authorization Server | client 인증, token 발급, key 관리 | OAuth2, OIDC, JWKS rotation |
| API Gateway | TLS 종료, JWT 1차 검증, rate limit | 401/403/429 응답 분리 |
| Resource Server | scope, audience, 업무 권한 재검증 | 토큰 claim과 DB 권한 매핑 |
| mTLS | 클라이언트 인증서 기반 호출자 확인 | B2B, 내부 서비스, SPIFFE/SPIRE |
| Observability | 인증 실패, quota, latency 로그 | SIEM, APM, trace-id 연계 |

> 요약: API 보안은 Authorization Server, Gateway, Resource Server, mTLS, 로그 체계가 역할을 나눠 검증한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
클라이언트 등록 -> 토큰 발급 -> mTLS 연결 확인
-> JWT iss/aud/exp/signature 검증 -> scope 인가 -> rate limit -> 응답/로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Client 인증과 토큰 발급 | client_secret, private_key_jwt, PKCE |
| 2 | 전송 채널 검증 | TLS 1.2+, mTLS 인증서 CN/SAN |
| 3 | JWT 검증 | `iss`, `aud`, `exp`, `nbf`, `alg`, `kid`, signature |
| 4 | 권한·업무 규칙 검증 | scope, role, resource owner, tenant-id |
| 5 | 호출량·로그 처리 | token bucket, 429, audit event, trace-id |

> 요약: API 요청은 채널, 토큰, 권한, 호출량 순서로 통과하며 실패 위치별 응답 코드와 로그가 달라야 한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 키워드 적용 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 인증 | API Key 장기 공유 | OAuth2/OIDC access token | access token 5~15분, refresh 분리 |
| 인가 | URL 접근만 확인 | scope, RBAC, ABAC 재검증 | `aud` 서비스별 분리, scope 최소화 |
| 채널 | 단방향 TLS | mTLS, certificate rotation | 인증서 90~397일 주기 관리 |
| 남용 통제 | 무제한 호출 | rate limit, quota, anomaly rule | 429 비율, IP/client별 TPS |

> 요약: 보안 API는 토큰 수명 단축, audience 분리, mTLS, rate limit으로 호출자의 권한과 사용량을 제한한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 인증 방식 | API Key | OAuth2/OIDC JWT | 사용자 위임, scope 기반 API |
| 서비스 간 인증 | bearer token만 사용 | mTLS 또는 token binding | B2B, 내부 고위험 API |
| 권한 모델 | role 단일 기준 | scope+resource owner+tenant | 다중 테넌트, 금융·개인정보 API |

> 요약: 사용자 위임은 OAuth2/OIDC, 서비스 간 고신뢰 호출은 mTLS를 결합해 설계한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 토큰 오용 | audience·issuer 검증 누락 | iss/aud allowlist, JWKS pinning | invalid token 401 로그 |
| 권한 초과 | scope와 업무 권한 불일치 | Resource Server 소유권 재검증 | 403 발생 사유, 권한 테스트 커버리지 |
| 대량 호출 | 자동화 요청, credential stuffing | token bucket, IP/client quota, bot rule | 429 비율, 계정 잠금 이벤트 |

> 요약: API 위험은 토큰 오용, 권한 초과, 대량 호출이며 각 위험은 검증 claim과 운영 지표로 추적한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| JWT 검증 | iss/aud/exp/signature 검증 테스트 100% | unit test, negative token corpus |
| mTLS 운영 | 인증서 만료 30일 전 알림, 폐기 목록 반영 | PKI inventory, gateway log |
| 호출 통제 | client별 TPS, 401/403/429 분리 | API Gateway metric, SIEM dashboard |

> 요약: 성공 여부는 JWT 부정 테스트, 인증서 수명 관리, 실패 코드별 로그 분리로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. OAuth2/OIDC: Authorization Code+PKCE, access token 5~15분, `iss/aud/exp/nbf/signature/scope` 검증 테스트를 CI에 포함
2. mTLS: 파트너·서비스 간 API에 client certificate, SAN-client_id 매핑, 인증서 만료 30일 전 알림과 CRL/OCSP 점검 적용
3. 운영 통제: API Gateway에서 token bucket, IP/client quota, 401/403/429 분리 로그, SIEM 탐지 rule을 trace-id와 연결

**결론 (2줄):**
- 기술사 판단: 공개 사용자 API는 OAuth2/OIDC와 rate limit, B2B·내부 고위험 API는 mTLS와 Resource Server 재인가를 결합해야 함
- 향후 방향: API 보안은 Gateway 단일 검증에서 Zero Trust 기반 요청별 토큰·인증서·행위 점검으로 이동해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "보안 API 설계를 설명하시오" | 토큰 발급, JWT 검증, scope 인가, rate limit 흐름 | OAuth2/OIDC, JWT, mTLS 역할 분리 |
| 요구사항 명시형 | "JWT 검증 방안을 제시하시오", "mTLS 적용을 설계하시오" | iss/aud/exp/signature와 인증서 매핑 절차 | 실패 코드, quota, 감사로그, 운영 지표 |

> 요약: 설명형은 표준 역할을 넓게 쓰고, 설계형은 Gateway와 Resource Server의 검증 책임을 나눠 쓴다.
