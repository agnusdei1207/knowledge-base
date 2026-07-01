---
title: "OAuth 2.0·OIDC (OAuth 2.0 OIDC)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 203
---

# 📖 【암기용】 개념 완전 이해

> 목적: OAuth 2.0과 OIDC를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: OAuth 2.0은 권한 위임, OIDC는 사용자 인증을 위한 ID 계층
- **왜 필요한가**: 사용자가 비밀번호를 여러 서비스에 맡기지 않고, 필요한 범위(scope)의 접근 권한만 제3자 애플리케이션에 줄 수 있어야 한다.
- **핵심 직관**: OAuth는 호텔 키카드처럼 특정 방만 열게 하는 권한표이고, OIDC는 체크인한 사람이 누구인지 확인하는 신분 확인서이다.

## 깊이 이해
- **배경·문제의식**: 비밀번호 공유 방식은 계정 탈취와 권한 과다 부여 문제가 발생한다. OAuth 2.0은 access token으로 위임 범위를 제한하고, OIDC는 ID token으로 로그인 주체를 검증한다.
- **작동 원리**: Client가 Authorization Server에 사용자를 보낸 뒤 authorization code를 받는다. Client는 code를 token endpoint에 제출해 access token, refresh token, ID token을 획득한다.
- **비유**: 주차 대행 직원에게 집 열쇠를 주지 않고, 주차장 출입만 가능한 임시 카드만 주는 방식임.
- **구체 예시**: 모바일 앱은 Authorization Code + PKCE를 사용해 `code_verifier`와 `code_challenge`를 검증하고, 탈취된 code 단독 재사용을 차단함.
- **흔한 오해·주의점**: OAuth 2.0만으로 로그인 인증이 완성되지 않는다. 사용자 식별은 OIDC의 ID token, nonce, issuer, audience 검증이 필요하다.

## 연결 개념
- JWT — access token 또는 ID token 표현 형식
- PKCE — public client의 authorization code 탈취 방지
- Zero Trust — 토큰 기반 접근통제와 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: OAuth 2.0은 인가, OIDC는 인증이라는 경계를 먼저 고정해야 감점 없이 답안을 전개할 수 있다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OAuth 2.0은 resource 접근 권한을 token으로 위임하는 인가 프레임워크이고, OIDC는 OAuth 위에 ID token을 추가한 인증 계층이다.
> 2. **가치**: 비밀번호 공유 없이 scope, audience, expiry로 권한 범위를 제한하고 SSO를 구현한다.
> 3. **판단 포인트**: Authorization Code + PKCE, token 검증, refresh token 회전, logout·revocation 설계가 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인증·인가 구분 확인 | OAuth 2.0 인가, OIDC 인증, ID token | OAuth를 로그인 프로토콜로 단정 |
| 보안 플로우 설계 확인 | Authorization Code, PKCE, scope, audience | implicit flow를 현대 SPA 기본값으로 제시 |
| 운영 통제 역량 확인 | token expiry, rotation, revocation, audit | access token 장기 보관, refresh token 보호 누락 |

> 요약: 이 문제는 토큰 종류보다 인증·인가 경계와 안전한 flow 선택 기준을 묻는다.

---

## Ⅰ. 개요 및 필요성

OAuth 2.0은 권한 위임 인가 표준이고 OIDC는 인증 확장이다. 클라우드·모바일·API 연계에서는 비밀번호 공유 대신 제한된 token 기반 접근이 필요하다. OAuth 2.0·OIDC는 SSO, API 접근통제, 제3자 연계를 표준 flow로 처리한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Client -> Authorization Server -> Token
                         +-> Resource Server -> Protected API
                         +-> OIDC ID Token -> User Identity
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Resource Owner | 권한을 가진 사용자 | consent와 scope 승인 |
| Client | token을 요청하는 애플리케이션 | confidential/public 구분 |
| Authorization Server | code와 token 발급 | issuer, JWKS, discovery 제공 |
| Resource Server | access token 검증 후 API 제공 | audience, scope 검증 |

> 요약: OAuth/OIDC는 사용자, 클라이언트, 인증 서버, 리소스 서버의 역할 분리로 권한 위임과 인증을 처리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
로그인 요청 -> code 발급 -> token 교환 -> ID token 검증 -> API 호출 -> 감사 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Client가 authorization endpoint로 redirect | state, nonce 생성 |
| 2 | 사용자 인증·동의 후 authorization code 발급 | redirect URI exact match |
| 3 | code + PKCE로 token endpoint 교환 | code_verifier 검증 |
| 4 | access token으로 API 호출, ID token으로 사용자 확인 | iss, aud, exp, signature 검증 |

> 요약: 안전한 플로우는 code 탈취 방지, token 검증, 제한된 scope, 감사 로그가 순서대로 결합되어야 한다.

---

## Ⅳ. 특징

| 구분 | OAuth 2.0 | OIDC | 판단 포인트 |
|:---|:---|:---|:---|
| 목적 | API 접근 인가 | 사용자 인증 | 로그인은 OIDC 사용 |
| 주요 token | access token, refresh token | ID token 추가 | ID token은 API 인가용 사용 금지 |
| 검증 | scope, audience, expiry | issuer, nonce, claim | clock skew 5분 이하 허용 |
| 권장 flow | Authorization Code + PKCE | Code + PKCE + nonce | implicit flow 신규 적용 배제 |

> 요약: OAuth와 OIDC는 토큰 구조가 유사해도 목적이 다르므로 access token과 ID token 용도를 분리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | ID/PW 직접 전달 | Authorization Server token 위임 | 외부 연계·SSO·모바일 앱 존재 |
| 비용/성능 | 세션 DB 조회 | JWT local validation 또는 introspection | token TTL 5~15분, revocation 요구 여부 |
| 운영/위험 | 계정 공유 위험 | scope·audience 제한 | 최소 권한과 감사 로그 필요 |

> 요약: OAuth/OIDC는 외부 연계와 SSO가 필요한 시스템에서 비밀번호 공유를 token 위임으로 대체할 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| code 탈취 | public client 비밀키 보관 불가 | PKCE S256 필수 | PKCE 적용률 100% |
| token 재사용 | refresh token 장기 노출 | refresh token rotation, reuse detection | reuse 탐지 0건 목표 |
| 권한 과다 | broad scope 발급 | least privilege scope, consent 검토 | unused scope 0개 |

> 요약: 토큰 탈취와 권한 과다 부여는 PKCE, rotation, 최소 scope로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 토큰 검증 | iss·aud·exp·signature 검증 100% | API gateway policy test |
| 세션 보안 | access token TTL 15분 이하 | 설정 점검 |
| 감사 | login·consent·revocation 로그 보존 1년 | SIEM, audit log |

> 요약: 인증·인가 품질은 token 검증률, TTL, 감사 로그 보존으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. Web·SPA·Mobile 모두 Authorization Code + PKCE(S256)를 기본 flow로 정하고 implicit flow 신규 사용을 차단함.
2. API Gateway에서 JWT `iss`, `aud`, `exp`, `scope`를 검증하고 관리자 API는 step-up authentication을 요구함.
3. Refresh token rotation, reuse detection, revocation endpoint, logout propagation을 IAM 정책으로 운영함.

**결론 (2줄):**
- 기술사 판단: API 권한 위임은 OAuth 2.0, 사용자 로그인과 SSO는 OIDC를 적용하고 token 용도를 분리함.
- 향후 방향: FAPI, mTLS, DPoP, passkey와 결합해 금융·공공 API의 소유 증명 기반 token 통제로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OAuth 2.0과 OIDC를 설명하시오" | code flow, token 교환, 검증 순서 | OAuth 인가와 OIDC 인증 차이 |
| 요구사항 명시형 | "보안 방안을 제시하시오", "SSO를 설계하시오" | PKCE, token 검증, revocation | 리스크 대응, TTL, 감사 지표 |

> 요약: 설명형은 인증·인가 경계, 설계·보안형은 안전한 flow와 token 운영 통제를 중심으로 전환한다.
