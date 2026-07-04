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
- **개요**: OAuth 2.0은 사용자 리소스에 대한 접근 권한을 제한된 범위로 위임하는 **인가(Authorization) 프레임워크**이고, OIDC(OpenID Connect)는 그 위에 사용자가 누구인지 검증하는 **인증(Authentication) 계층**이다.
- **왜 필요한가**: 제3자 앱에 아이디·비밀번호를 그대로 넘기면 앱이 사용자 권한 전체를 갖게 된다. OAuth 2.0은 "무엇을 할 수 있는지"만 담은 토큰을 발급해 이 문제를 없앤다.
- **핵심 직관**: OAuth는 호텔의 특정 층만 열리는 카드키(권한 위임)이고, OIDC는 체크인할 때 여권으로 신원을 확인하는 절차(신원 확인)이다. 카드키가 있다고 그 사람이 누구인지 알 수 없듯, access token만으로는 로그인이 되지 않는다 — 그래서 OIDC가 ID token을 추가한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 인가 (Authorization) | "무엇을 할 수 있는가" — 권한 범위 부여, OAuth 2.0의 본질 | 카드키로 열 수 있는 문 |
| 인증 (Authentication) | "누구인가" — 신원 확인, OIDC가 추가하는 계층 | 여권으로 신원 확인 |
| Resource Owner | 리소스(데이터)를 소유한 사용자 본인 | 집주인 |
| Client | 토큰을 요청해 API를 대신 호출하는 애플리케이션 | 대리인(제3자 앱) |
| Authorization Server | code·token 발급 주체 | 카드키 발급 프런트데스크 |
| Resource Server | access token을 검증하고 실제 API·데이터를 제공 | 카드키로 열리는 방 |
| Access Token | 리소스 서버 API 호출에 쓰는 권한 증표 | 카드키 자체 |
| Refresh Token | access token 만료 시 재발급용 장기 토큰 | 카드키 재발급 예약증 |
| ID Token | 로그인한 사용자가 누구인지 담은 JWT(OIDC 전용) | 여권 사본 |
| Authorization Code | 1회용 임시 코드, token으로 교환하기 전 단계 | 프런트데스크가 주는 대기표 |
| PKCE(code_verifier/code_challenge) | code 탈취 후 재사용을 막는 검증 쌍 | 대기표에 찍는 일회용 비밀 도장 |
| Scope | 위임 권한의 범위(예: read:email) | "몇 층까지만 열리는 카드" |
| state / nonce | CSRF 방지용 난수(state), 재생공격 방지용 난수(nonce, OIDC) | 대기표 위조·재사용 방지 도장 |

## 깊이 이해

### 왜 이 구조가 필요했나 (배경)
- 예전 방식은 제3자 앱이 사용자의 아이디·비밀번호를 직접 입력받아 서버에 대신 로그인했다(비밀번호 안티패턴). 이러면 앱이 비밀번호를 저장·유출할 위험이 있고, 권한을 일부만 주고 싶어도(예: 이메일 읽기만) 전체 권한이 그대로 넘어간다.
- OAuth 2.0(2012, RFC 6749)은 비밀번호 대신 제한된 권한의 토큰을 넘기는 방식으로 이 문제를 해결했다. 하지만 OAuth 2.0 자체는 "이 토큰을 가진 사람이 누구인지"는 정의하지 않는다 — 그래서 로그인(인증) 용도로 쓰면 취약점이 생긴다. 이 공백을 메우려고 2014년 OIDC가 OAuth 2.0 위에 ID Token을 얹어 표준화되었다.

### 동작 원리 — Authorization Code + PKCE를 단계로
1. Client가 사용자를 Authorization Server의 로그인 화면으로 redirect한다. 이때 `state`(CSRF 방지)와 PKCE의 `code_challenge`를 함께 보낸다.
2. 사용자가 로그인하고 동의(consent)하면, Authorization Server는 Client의 redirect_uri로 1회용 authorization code를 돌려준다.
3. Client는 이 code와 자신만 아는 `code_verifier`(1단계 code_challenge의 원본값)를 token endpoint에 함께 제출한다.
4. 서버는 code_verifier를 해시해 code_challenge와 일치하는지 검증한 뒤 access token(+refresh token, ID token)을 발급한다.
- **PKCE가 막는 공격을 수치로**: code_verifier 없이 code만 있으면, 공격자가 redirect 과정에서 code를 가로채(예: 악성 앱이 커스텀 URL 스킴을 가로챔) 자기 token endpoint 요청에 재사용할 수 있다. code_verifier는 Client 로컬에만 생성·보관되는 값이라, code를 훔쳐도 이 값이 없으면 4단계에서 해시 불일치로 거부된다.

### OAuth 2.0과 OIDC를 구분하는 판별 원리
- 질문이 "제3자 앱이 내 캘린더에 접근해도 되는가"이면 인가 → OAuth 2.0. 질문이 "로그인한 사람이 진짜 이 사용자인가"이면 인증 → OIDC.
- 판별 신호: OIDC를 쓰면 scope에 `openid`가 반드시 들어가고, 응답에 access token 외에 **ID Token**(JWT)이 추가된다. ID Token 안에는 `sub`(사용자 고유 ID), `iss`(발급자), `aud`(대상 Client), `exp`(만료), `nonce`가 들어있어 이를 검증한다.
- **자주 하는 실수**: access token 발급만으로 "로그인 성공"을 판단하는 것. access token은 리소스 서버 접근용일 뿐 신원 보증이 없다. 신원 확인은 반드시 ID Token의 서명·iss·aud·nonce 검증으로 해야 한다.

### 구체 예시로 보는 scope와 refresh token
- 예: 사용자가 캘린더 앱에 `scope=calendar.readonly`로 동의하면, 발급된 access token은 캘린더 "읽기"만 가능하고 "쓰기"나 이메일 접근은 불가능하다.
- access token은 보통 TTL을 15분~1시간처럼 짧게 잡는다. 탈취돼도 피해 시간을 줄이기 위해서다. 만료될 때마다 재로그인시키는 대신, TTL이 훨씬 긴(수일~수개월) refresh token으로 access token만 조용히 재발급한다.

## 연결 개념
- JWT — ID Token, 그리고 흔히 access token의 표현 형식
- PKCE — public client(모바일·SPA)의 code 탈취 방지 확장
- SSO(Single Sign-On) — OIDC ID Token으로 여러 서비스에 한 번 로그인 상태를 공유하는 응용

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

- 개요: 권한 위임 인가와 인증 표준
- 배경: 클라우드·모바일·API 연계에서는 비밀번호 공유 대신 제한된 token 기반 접근이 필요하다.
- 필요성: OAuth 2.0 flow와 OIDC ID Token으로 SSO, API 접근통제, 제3자 연계 기준을 제공한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
