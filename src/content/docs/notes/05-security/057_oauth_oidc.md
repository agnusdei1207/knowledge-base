---
sidebar:
  order: 57
  label: "057. OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "인가 위임 및 분산 신원 인증 표준 : OAuth 2.0 및 OIDC (OpenID Connect & RFC 6749/7636)"
date: "2026-08-26T14:46:06+09:00"
tags:
  - "notes-security"
weight: 57
extra:
  question_no: "057"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "RFC 6749/6750(OAuth 2.0 권한 위임), OpenID Connect Core 1.0(신원 인증 레이어), Access Token vs ID Token(JWT), PKCE(RFC 7636/9700) 및 Refresh Token Rotation"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OAuth 2.0(Open Authorization 2.0 / IETF RFC 6749)**: 사용자가 자신의 자격증명(패스워드)을 제3자 애플리케이션(Client)에 직접 노출하지 않고, 인가 서버(Authorization Server)를 통해 특정 API 자원에 대한 제한된 접근 권한(Scope)을 위임(Authorization)할 수 있도록 지원하는 프레임워크.
- **OIDC(OpenID Connect Core 1.0)**: OAuth 2.0 인가 프레임워크 위에 구축된 분산 신원 인증(Authentication) 레이어로, 클라이언트가 인가 서버에 의해 수행된 사용자 인증 결과와 프로필 정보(Claims)를 서명된 **ID 토큰(ID Token / JWT)** 형태로 획득할 수 있도록 지원하는 표준 프로토콜.

</details>

- 정의/개념: 권한 위임 표준인 **OAuth 2.0(Access Token/Refresh Token)** 과 신원 증명 표준인 **OIDC(ID Token)** 를 계층적으로 결합하여, **인가 코드 발급 $\rightarrow$ PKCE 검증 $\rightarrow$ 토큰 교환 $\rightarrow$ JWT 서명/클레임 검증 $\rightarrow$ API 자원 접근** 을 수행하는 **현대 분산 신원 및 권한 관리(IAM) 아키텍처**
- 배경/필요성: 서드파티 패스워드 공유로는 **권한 위임** 범위 통제 불가

#### 한줄 요약
- OAuth 2.0으로 API 자원 접근 권한을 위임하고, OIDC로 사용자 신원을 증명하여 패스워드 없는 안전한 연동을 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Access Token vs ID Token**:
  - **Access Token (OAuth 2.0)**: 자원 서버(API)에 제시하여 비즈니스 데이터를 요청하는 권한 증명용 무상태(JWT) 또는 불투명(Opaque) 문자열.
  - **ID Token (OIDC)**: 클라이언트 앱이 사용자의 신원(이름, 이메일, 고유 식별자 `sub`)을 확인하기 위해 사용하는 암호학적으로 서명된 JWT(JSON Web Token).
- **PKCE(Proof Key for Code Exchange / RFC 7636)**: 클라이언트 시크릿을 은닉할 수 없는 퍼블릭 클라이언트(모바일/SPA)에서 악성 앱의 인가 코드 가로채기(Interception)를 방어하는 동적 챌린지 검증 기술.

</details>

- **권한 위임(AuthZ)과 신원 인증(AuthN)의 기능적 분리**: 인가(OAuth 2.0)와 인증(OIDC)의 목적별 토큰 이원화 관리
- **모바일/SPA 보안 표준화 (PKCE 강제)**: RFC 9700 지침에 따라 모바일 앱 및 브라우저 기반 SPA 환경에서 PKCE 적용 의무화
- **토큰 수명주기 및 회전 관리 (Refresh Token Rotation)**: Refresh Token 사용 시마다 새로운 Refresh Token으로 교체하여 탈취 시 지속 사용 차단

#### 한줄 요약
- 권한(Access)과 신원(ID) 분리, PKCE 기반 인가 코드 탈취 방어, Refresh Token Rotation 수명 관리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OAuth 2.0 / OIDC 4대 핵심 엔티티**:
  1. **Resource Owner (사용자)**: 자원의 소유자이자 인증 주체.
  2. **Client (서드파티 애플리케이션)**: 사용자를 대신하여 자원 서버에 접근을 요청하는 앱.
  3. **Authorization Server / OpenID Provider (OP)**: 신원을 인증하고 인가 코드 및 토큰을 발급하는 서버.
  4. **Resource Server (자원 서버 / API)**: Access Token을 검증하고 보호된 API 데이터를 제공하는 백엔드.

</details>

```text
[ 자원 소유자 (Resource Owner / User) ]
                 │ (1. 로그인 및 권한 위임 동의)
                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 클라이언트 (Client: 모바일 앱 / SPA 프론트엔드) ]                 │
│  ├─ `code_verifier` 생성 ➔ `code_challenge = SHA256(verifier)` 계산   │
│  └─ [ 인가 요청 전송: `/authorize?client_id=...&code_challenge=...` ] │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. 인가 코드 발급 ➔ 토큰 교환 요청)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 인가 서버 / 신원 제공자 (Authorization Server / OpenID Provider) ]│
│  ├─ Redirect URI 엄격 대조 및 PKCE `code_verifier` 수학적 일치성 검증   │
│  ├─ OIDC 레이어: 사용자 신원 증명 **ID Token (JWT)** 발급 (RS256 서명)  │
│  └─ OAuth 레이어: API 자원 접근용 **Access Token** & **Refresh Token** 발급│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (3. Access Token 첨부 API 호출)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 자원 서버 (Resource Server: REST API 백엔드) ]                     │
│  ├─ JWKS(JSON Web Key Set) 기반 서명 무결성 및 만료(`exp`), Scope 검증 │
│  └─ [ 권한 검증 통과 ➔ 비즈니스 API 데이터 정상 응답 반환 ]            │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 클라이언트가 PKCE 챌린지로 인가 코드를 교환하여 ID/Access 토큰을 발급받고, 자원 서버에서 서명 검증을 거쳐 API 데이터를 제공받는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **Resource Owner** | 자신의 신원을 인증하고 특정 권한 범위(Scope) 위임에 동의하는 사용자 | User |
| **Client** | 사용자를 대리하여 인가 서버로부터 토큰을 발급받고 API를 호출하는 앱 | Relying Party |
| **Authorization Server** | 사용자 인증, PKCE 검증, 인가 코드 발급, ID/Access/Refresh Token 생성 | OpenID Provider|
| **Resource Server** | Access Token의 서명, 만료일, 스코프를 검증하고 실제 비즈니스 자원 제공 | API Server |
| **JWKS 엔드포인트** | 비대칭 공개키 목록을 제공하여 자원 서버가 무상태(Stateless)로 토큰을 검증하도록 지원 | Key Discovery |

#### 한줄 요약
- Resource Owner, Client, Authorization Server, Resource Server, JWKS 엔드포인트가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인가 코드 부여(Authorization Code Grant with PKCE) 5단계 흐름**:
  1. 클라이언트가 `code_challenge`를 포함하여 인가 요청
  2. 사용자 인증 및 동의 후 인가 코드(`code`) 반환
  3. 클라이언트가 인가 코드와 `code_verifier`를 전송하여 토큰 교환 요청
  4. 인가 서버가 PKCE 검증 후 Access Token 및 ID Token 발급
  5. 클라이언트가 Access Token으로 자원 서버 API 호출

</details>

```text
1. [인가 요청] 클라이언트가 `code_challenge`와 함께 인가 서버의 `/authorize` 엔드포인트로 리다이렉트
            │
            ▼
2. [인증 및 동의] 사용자가 신원을 인증하고 권한 요청(Scope: `openid profile read:orders`)에 동의
            │
            ▼
3. [인가 코드 수신] 인가 서버가 등록된 화이트리스트 `redirect_uri`로 일회용 인가 코드(`code`) 전달
            │
            ▼
4. [토큰 교환 및 PKCE 검증]
    ├─ 클라이언트가 `/token` 엔드포인트로 `code`와 `code_verifier` 원본 전송
    └─ 인가 서버가 `SHA256(code_verifier) == code_challenge` 일치성 검증 ➔ [ID Token + Access Token 발급]
            │
            ▼
5. [토큰 검증 및 자원 접근]
    ├─ 클라이언트: ID Token의 JWT 서명(`iss`, `aud`, `nonce`) 검증 후 사용자 로그인 처리
    └─ 자원 서버: HTTP Header(`Authorization: Bearer <Access_Token>`) 수신 후 Scope 확인 및 데이터 반환
```

**동작 원리**

1. **비밀정보 비공개 원칙**: 사용자 패스워드가 제3자 클라이언트 애플리케이션으로 직접 전달되지 않음
2. **동적 가로채기 방어**: 인가 코드가 중간에 탈취되더라도 공격자는 `code_verifier`를 알 수 없어 토큰 교환 불가
3. **무상태 암호학적 신원 증명**: OIDC ID 토큰은 비대칭 서명(RS256)을 포함하여 서버 측 세션 조회 없이 클라이언트 자체 검증 가능
4. **최소 권한 범위 제어**: 요청된 Scope 내의 기능만 Access Token에 인코딩하여 자원 서버 접근 한정
5. **토큰 재사용 무력화**: Refresh Token 사용 시 기존 토큰을 즉시 무효화하고 새 토큰 발급(Rotation)

#### 한줄 요약
- 인가 요청, 인증 동의, 인가 코드 수신, PKCE 검증 및 토큰 교환, 서명 검증 및 자원 접근 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OAuth 2.0 vs OpenID Connect(OIDC) 핵심 비교**: 권한 위임과 신원 인증의 비교.

</details>

| 비교 항목 | OAuth 2.0 (권한 위임 프레임워크) | OpenID Connect (신원 인증 프로토콜) |
|:---|:---|:---|
| **프로토콜의 핵심 목적** | **제3자 애플리케이션에 API 자원 접근 권한 위임** | **사용자의 신원 확인 및 싱글 사인온(SSO) 인증** |
| **기반 표준 규격** | IETF RFC 6749, RFC 6750 | OpenID Connect Core 1.0 (OAuth 2.0 확장) |
| **핵심 발행 토큰** | **Access Token (API 접근용), Refresh Token** | **ID Token (JWT 형식의 신원 증명서)** |
| **토큰의 주요 수신자** | **자원 서버 (Resource Server / API)** | **클라이언트 애플리케이션 (Client App)** |
| **주요 검증 항목** | **Scope (권한 범위), 유효기간(`exp`)** | **`iss`(발급자), `aud`(수신자), `nonce`, 서명** |

#### 한줄 요약
- OAuth 2.0은 API 자원 권한 위임(What), OIDC는 사용자 신원 인증(Who)을 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IETF RFC 9700 (OAuth 2.0 Security Best Current Practice)**: 암시적 부여(Implicit Grant) 및 자격증명 직접 입력(ROPC) 방식을 보안 취약으로 전면 폐기하고, 모든 클라이언트에 인가 코드 부여 + PKCE 적용을 권고하는 최신 보안 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모바일 앱 환경에서 인가 코드가 가로채기 공격에 노출되어 **공격자가 불법적으로 Access Token을 교환/탈취** | **IETF RFC 9700** 지침에 따라 모바일 및 SPA 환경에서 **OAuth 2.0 PKCE(RFC 7636) 확장 규격 의무 적용** | 클라이언트 시크릿 부재 환경에서의 인가 코드 탈취 공격 100% 원천 차단 |
| 서명 검증 없이 ID Token의 페이로드만 디코딩하여 사용하여 **위조된 사용자 신원으로 로그인되는 스푸핑 침해** | **OIDC Core 1.0** 준수, JWKS 기반 비대칭 서명 검증 및 **`iss`, `aud`, `exp`, `nonce` 클레임 전수 검증** | 위조 ID Token 주입 및 사용자 신원 도용(Replay) 공격 100% 무력화 |
| 장기 수명의 Refresh Token이 탈취되어 **공격자가 정상 사용자의 Access Token을 지속 재발급받는 사고** | **Access Token 갱신 시마다 새 갱신 토큰을 발급하고 이전 토큰을 폐기하는 갱신 토큰 회전(RTR)** 적용 | 유출된 Refresh Token의 재사용을 탐지하고 해당 토큰 패밀리 전체를 즉각 무효화 |

#### 한줄 요약
- PKCE로 인가 코드를 보호하고, OIDC 클레임을 전수 검증하며, RTR로 갱신 토큰 탈취를 방어한다.

## Ⅶ. 결론

- 권한 위임에는 **OAuth 2.0**, 신원 인증에는 OIDC를 쓰고 PKCE·RTR 적용

#### 한줄 요약
- OAuth 2.0 권한 위임과 OIDC 신원 인증에 PKCE 및 RTR을 결합하여 안전한 분산 인증을 완성한다.
