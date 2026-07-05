---
title: "OAuth 2.0·OIDC (OAuth 2.0 OIDC)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 96
---

# 📖 【암기용】 개념 완전 이해

> 목적: OAuth 2.0과 OIDC를 처음 봐도 인증과 인가의 차이를 구분하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: OAuth 2.0은 API 권한 위임, OIDC는 로그인 인증 계층
- **왜 필요한가**: 사용자가 비밀번호를 제3자 앱에 주지 않고도 특정 API 권한만 위임해야 한다. 로그인까지 확인하려면 OAuth 2.0 위에 OIDC ID Token 검증이 필요하다.
- **핵심 직관**: OAuth Access Token은 "API 사용권", OIDC ID Token은 "사용자 신분증"임.

## 깊이 이해
- **배경·문제의식**: 과거 앱은 사용자 ID/PW를 직접 받아 외부 서비스에 접근했으나, 비밀번호 재사용·권한 과다·회수 불가 문제가 발생함. OAuth 2.0은 Authorization Server가 제한된 권한의 토큰을 발급하게 하여 이 문제를 분리함.
- **작동 원리**: Authorization Code + PKCE는 브라우저 경유 code 탈취를 줄이기 위해 code_verifier와 code_challenge를 사용함. Resource Server는 Access Token의 issuer, audience, expiry, scope를 검증하고, Client는 OIDC ID Token의 nonce와 서명을 JWKS로 검증함.
- **비유**: 호텔 프런트가 객실키를 발급하면 투숙객은 방에 들어가지만 금고 마스터키는 받지 않는다. Access Token은 객실키, ID Token은 투숙객 신분 확인서에 해당함.
- **구체 예시**: 모바일 앱에서 `openid profile email` scope 요청, PKCE S256 사용, ID Token exp 5분, Access Token exp 10분, Refresh Token 회전으로 탈취 재사용 차단.
- **흔한 오해·주의점**: OAuth 2.0만으로 로그인 인증을 했다고 쓰면 감점. 사용자 인증은 OIDC의 ID Token, API 인가는 OAuth Access Token으로 분리해야 함.

## 연결 개념
- SAML 2.0 - XML Assertion 기반 기업 Federation
- SSO - IdP 로그인 세션을 여러 SP가 공유하는 구조
- RBAC/ABAC - 토큰 검증 이후 실제 권한 결정에 사용하는 정책 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. OAuth 흐름 암기가 아니라 인증/인가 분리, 토큰 검증 위치, 정책 평가와 감사 지표를 연결한다.
> 핵심: Authorization Code + PKCE, Access Token/ID Token, JWKS, iss/aud/exp/nonce 검증을 빠뜨리지 않는다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OAuth 2.0은 권한 위임 프레임워크이고, OIDC는 OAuth 2.0 위에 ID Token을 추가한 인증 프로토콜이다.
> 2. **가치**: Client는 비밀번호를 보관하지 않고 Authorization Server의 토큰으로 API 접근 범위(scope)를 제한한다.
> 3. **판단 포인트**: 인증은 ID Token 검증, 인가는 Access Token 검증과 Resource Server 정책 평가로 분리해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인증과 인가 구분 역량 확인 | OAuth=인가, OIDC=인증, Access Token과 ID Token 역할 분리 | OAuth 2.0을 로그인 프로토콜로 단정 |
| 안전한 표준 흐름 설계 확인 | Authorization Code + PKCE, redirect_uri 고정, state/nonce, JWKS 검증 | Implicit Flow 중심 설명, PKCE 누락 |
| 토큰 검증과 감사 기준 확인 | iss, aud, exp, scope, nonce, key rotation, token replay 탐지 | 토큰 발급 흐름만 나열하고 Resource Server 검증 누락 |

> 요약: OAuth/OIDC 답안은 흐름보다 "누가 어떤 토큰을 어디서 검증하는가"를 중심으로 작성해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | OAuth 2.0은 API 권한 위임, OIDC는 로그인 인증 계층 | "신분증 확인" |
| **왜 필요한가** | 사용자가 비밀번호를 제3자 앱에 주지 않고도 특정 API 권한만 위임해야 한다 | "식당 메뉴판" |
| **핵심 직관** | OAuth Access Token은 "API 사용권", OIDC ID Token은 "사용자 신분증"임 | "입장권" |
| **배경·문제의식** | 과거 앱은 사용자 ID/PW를 직접 받아 외부 서비스에 접근했으나, 비밀번호 재사용·권한 과다·회수 불가 문제가 발생함 | "핵심 기술 요소" |
| **작동 원리** | Authorization Code + PKCE는 브라우저 경유 code 탈취를 줄이기 위해 code_verifier와 code_challe... | "신분증 확인" |
| **비유** | 호텔 프런트가 객실키를 발급하면 투숙객은 방에 들어가지만 금고 마스터키는 받지 않는다 | "핵심 기술 요소" |
| **흔한 오해·주의점** | OAuth 2.0만으로 로그인 인증을 했다고 쓰면 감점 | "신분증 확인" |

---


## Ⅰ. 개요 및 필요성

- 개요: API 권한 위임·인증 표준
- 배경: 제3자 앱에 사용자 비밀번호를 공유하면 권한 회수, 범위 제한, 접속 감사가 서비스별 구현에 묶인다.
- 필요성: OAuth 2.0 scope와 OIDC ID Token으로 권한 위임, MFA 연계, 토큰 감사를 표준 흐름으로 처리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Agent -> Client -> Authorization Server -> Token Endpoint
                         +-> JWKS / Metadata
Client -> Resource Server -> Policy Check -> API Response
```

| 구성요소 | 역할 | 검증 포인트 |
|:---|:---|:---|
| Resource Owner | 사용자 동의와 인증 주체 | MFA, consent, session age |
| Client | 인가 요청과 토큰 수신 주체 | client_id, redirect_uri, PKCE |
| Authorization Server | code, access token, id token 발급 | issuer, signing key, token lifetime |
| Resource Server | API 요청 수신과 Access Token 검증 | aud, scope, exp, introspection |
| JWKS/Metadata | 공개키와 엔드포인트 배포 | kid rotation, HTTPS, cache TTL |

> 요약: Client는 토큰을 받는 주체이고, Resource Server는 Access Token을 검증해 실제 API 인가를 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Login Request -> Auth Code + PKCE -> Token Exchange
-> ID Token Verify / Access Token Store -> API Call
-> Resource Server Token Verify -> Policy Decision -> Audit Log
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Authorization Request 생성 | state, nonce, code_challenge S256 |
| 2 | 사용자 인증·동의 후 code 반환 | redirect_uri 완전 일치, code 1회 사용 |
| 3 | Token Endpoint에서 code 교환 | code_verifier, client authentication |
| 4 | ID Token과 Access Token 검증 | iss, aud, exp, iat, nonce, JWKS 서명 |
| 5 | API 인가와 감사 | scope, RBAC/ABAC policy, deny log |

> 요약: OIDC 인증은 ID Token 검증으로 끝나고, API 인가는 Resource Server의 Access Token 검증과 정책 평가에서 확정된다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | OAuth 2.0·OIDC | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 권한 위임 | ID/PW 공유 | Scope 기반 Access Token | RFC 6749, RFC 7636, RFC 8414 |
| 사용자 인증 | 앱별 로그인 | OIDC ID Token | OpenID Connect Core, nonce 검증 |
| 토큰 검증 | 세션 DB 조회 | JWT 서명/JWKS 또는 introspection | exp 5~15분, refresh token rotation |
| 공격 대응 | 장기 쿠키 의존 | state, PKCE, issuer/audience 검증 | code injection, replay 차단 |

> 요약: OAuth/OIDC는 비밀번호 공유를 제거하지만, 토큰 검증 누락 시 인증 우회와 API 권한 오남용이 발생한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | OAuth 2.0·OIDC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SAML XML Assertion | JSON/JWT 토큰과 REST API | 모바일·SPA·API 중심이면 OIDC |
| 비용/성능 | 세션 중앙 조회 | 로컬 JWT 검증 또는 introspection | p95 인증 확인 100ms 목표면 JWKS 캐시 |
| 운영/위험 | 앱별 계정 | 중앙 IdP와 토큰 정책 | 사용자 1만명 이상, 앱 10개 이상 |

> 요약: API·모바일·클라우드 환경은 OIDC를 우선 검토하고, 레거시 기업 SSO는 SAML 연계를 병행한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Code 탈취 | public client와 redirect 악용 | Authorization Code + PKCE S256, redirect_uri allowlist | PKCE 적용률 100% |
| Token Replay | Access Token 탈취 | exp 10분 이하, mTLS/DPoP, refresh token rotation | 재사용 탐지 건수, revoke 지연 60초 이하 |
| 검증 누락 | iss/aud/nonce 미확인 | OIDC library 고정, JWKS kid 검증, negative test | 토큰 검증 테스트 20건 이상 |

> 요약: OAuth/OIDC 리스크는 토큰 탈취보다 검증 누락에서 커지므로 필수 claim과 key rotation을 테스트로 고정한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 인증 정확도 | iss/aud/exp/nonce 검증 100% | 단위 테스트, OIDC conformance |
| 인가 통제 | scope/RBAC/ABAC deny 로그 100% 기록 | API Gateway·SIEM 로그 |
| 운영 감사 | token revoke 60초 이하, JWKS rotation 월 1회 | IdP 운영 리포트, 키 변경 훈련 |

> 요약: 성공 여부는 로그인 성공률이 아니라 claim 검증률, 정책 거부 로그, 키 회전 훈련으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Authorization Code + PKCE(S256)를 기본값으로 적용하고 Implicit Flow는 신규 서비스에서 제외함.
2. ID Token은 Client에서 iss/aud/exp/nonce를 검증하고, Access Token은 Resource Server에서 aud/scope/exp를 검증함.
3. JWKS 캐시 TTL 5분, access token 10분 이하, refresh token rotation과 revoke API를 SIEM 감사 로그에 연결함.

**결론 (2줄):**
- 기술사 판단: 사용자 로그인 문제면 OIDC ID Token 검증, API 권한 문제면 OAuth Access Token과 정책 평가를 답안 중심에 둠.
- 향후 방향: FAPI 2.0, PAR/JAR, DPoP, mTLS로 금융·공공 API의 토큰 탈취와 위조 요청 통제를 확대함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OAuth 2.0과 OIDC를 설명하시오" | Authorization Code + PKCE, ID/Access Token 검증 흐름 | OAuth와 OIDC 역할 차이, SAML 비교 |
| 요구사항 명시형 | "인증·인가 방안을 설계하시오", "비교하시오" | iss/aud/exp/nonce, scope, Resource Server 정책 평가 | 토큰 수명, JWKS, 감사 지표, 리스크 대응 |

> 요약: 포괄형은 표준 구성과 흐름을 쓰고, 설계형은 토큰 검증 위치와 정책 평가 기준을 먼저 배치한다.
