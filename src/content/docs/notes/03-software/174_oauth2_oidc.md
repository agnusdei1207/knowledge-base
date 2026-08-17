---
sidebar:
  order: 174
  label: "174. OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
date: "2026-08-18T03:05:00+09:00"
tags:
  - "notes-software"
weight: 174
extra:
  question_no: "174"
  source_status: "기출"
  source_history: "123회"
  priority: 70
  priority_note: "권한 위임과 신원 확인의 역할 구분 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OAuth 2.0 (Open Authorization 2.0)**: 사용자의 비밀번호를 제3자 앱에 노출하지 않고 인가 서버(Authorization Server)를 통해 한시적 접근 토큰(Access Token)을 발급하여 자원 접근 권한을 위임하는 프레임워크.
- **OIDC (OpenID Connect)**: OAuth 2.0 프로토콜 상단에 신원 확인(Authentication) 계층을 얹어 사용자의 프로필 정보가 담긴 ID Token(JWT)을 발급하는 표준 싱글 사인온(SSO) 인증 프로토콜.

</details>

- 정의/개념: 비밀번호 노출 없이 제3자 앱에 자원 접근 권한을 위임하는 **OAuth 2.0과 사용자 신원 인증(ID Token)을 제공하는 OIDC** 표준 프로토콜
- 배경/필요성: 제3자 애플리케이션에 사용자 계정 비밀번호를 직접 전달함에 따른 **크리덴셜 탈취, 과도한 권한 노출 및 통합 로그인(SSO) 부재 위험** 직면

#### 한줄 요약

- 인가(권한 위임)를 위한 OAuth 2.0과 인증(신원 확인)을 위한 OIDC를 결합하여 안전한 소셜 로그인과 API 권한 위임을 완성

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **토큰의 역할 분리(Token Separation)**: 리소스 API 접근용 Access Token(권한 증명)과 클라이언트 로그인 신원 증명용 ID Token(JWT 포맷)의 명확한 분리.
- **PKCE(Proof Key for Code Exchange)**: 모바일 및 SPA 환경에서 Secret 노출 없이 동적 챌린지 코드를 검증하여 인가 코드 가로채기를 방어하는 보안 확장 표준.

</details>

- 사용자 비밀번호를 클라이언트에 전혀 제공하지 않는 **안전한 권한 위임(Delegated Authorization)**
- 표준 JWT 클레임(iss, sub, aud, exp)을 포함하는 **사용자 신원 확인(ID Token / SSO)**
- 모바일/SPA 등 공개 클라이언트(Public Client)의 코드 탈취를 차단하는 **PKCE 보안 확장**

#### 한줄 요약

- Access Token과 ID Token의 분리 및 PKCE 챌린지를 통해 웹/모바일 환경의 인증·인가를 완벽히 통제

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OAuth/OIDC 4대 신뢰 주체**: Resource Owner(사용자), Client(앱), Authorization Server(인가 서버), Resource Server(API 서버).

</details>

```text
[ OAuth 2.0 및 OIDC 신뢰 경계 및 4대 엔티티 구조도 ]

 1. [ Resource Owner (사용자) ] ── (브라우저 로그인 및 권한 위임 동의)
               │                                      │
               ▼                                      ▼
 2. [ Client App (SPA / Mobile) ]        3. [ Authorization Server (IdP) ]
    • Access Token / ID Token 수신          • 사용자 인증 및 동의 화면 제공
    • PKCE (code_verifier / challenge)      • Auth Code 및 Tokens 발급 (JWT)
               │                                      ▲
               │ (Bearer Access Token 요청)           │ (서명 공개키 JWKS 제공)
               ▼                                      │
 4. [ Resource Server (API / UserInfo) ] ─────────────┘
    • Access Token 서명 및 Scope 검증 후 비즈니스 데이터 반환
```

선의 의미: 사용자가 인가 서버에서 로그인하면 클라이언트가 인가 코드로 토큰을 교환받아 리소스 서버에 접근하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 자원 소유자 (Resource Owner) | 자신의 데이터에 대한 **제3자 애플리케이션의 접근을 승인/동의하는 실제 사용자** |
| 클라이언트 (Client App) | 사용자를 대신하여 **인가 서버에 로그인을 요청하고 발급받은 토큰으로 API 호출** |
| 인가 서버 (Auth Server/IdP) | 사용자를 직접 인증하고 **인가 코드, Access Token, ID Token(JWT)을 발급/서명** |
| 자원 서버 (Resource Server) | API 요청에 포함된 **Access Token의 유효성과 Scope를 검증하고 보호된 자원 반환** |

#### 한줄 요약

- 자원 소유자, 클라이언트, 인가 서버, 자원 서버가 신뢰 경계를 형성하여 안전하게 협력

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OIDC Authorization Code Flow with PKCE 5단계**: 인가 요청 $\to$ 사용자 로그인/동의 $\to$ 인가 코드 반환 $\to$ 토큰 교환 $\to$ ID/Access Token 검증.

</details>

```text
[ OIDC Authorization Code Flow with PKCE 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Client: PKCE 및 State/Nonce 생성 후 인가 요청
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Auth Server: 사용자 로그인 및 Scope 동의
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Auth Server: Redirect URI로 1회용 Code 전달
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Client: Code + code_verifier로 토큰 교환
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. ID Token으로 로그인 완료 & Access Token으로 API 호출
 └────────────────────────────────────────┘
```

### 동작 원리

1. 인가 요청: 클라이언트가 `code_challenge`, `state`, `nonce` 파라미터를 생성하여 인가 서버의 `/authorize`로 리다이렉트.
2. 사용자 인증: 사용자가 구글/카카오 화면에서 비밀번호를 입력하고 개인정보 제공 동의를 클릭.
3. 코드 반환: 인가 서버가 등록된 Redirect URI로 일회용 `Authorization Code`와 `state`를 회신.
4. 토큰 교환: 클라이언트가 `/token` 엔드포인트로 인가 코드와 원본 `code_verifier`를 전송하여 PKCE 일치 검증.
5. 토큰 사용: 클라이언트는 `ID Token` 서명을 검증하여 사용자를 로그인 처리하고, `Access Token`으로 리소스 API를 호출.

#### 한줄 요약

- 인가 요청 $\to$ 사용자 인증 $\to$ 코드 반환 $\to$ 토큰 교환 $\to$ 토큰 사용의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OAuth 2.0 vs OIDC**: 권한 위임 전용 프레임워크(OAuth)와 사용자 신원 증명 및 로그인 전용 프로토콜(OIDC).

</details>

| 구분 | OAuth 2.0 (순수 권한 위임) | OIDC (OpenID Connect: 인증 확장) |
|:---|:---|:---|
| **적용 기준** | 타사 API 호출 권한 위임 (구글 캘린더 읽기, 깃허브 레포 접근) | 소셜 간편 로그인 (구글/카카오 로그인), 통합 SSO |
| **핵심 특징** | **Access Token 발급, 자원에 무엇(What)을 할 수 있는지 인가** | **ID Token (JWT) 발급, 사용자가 누구(Who)인지 신원 증명** |
| **한계** | 사용자 신원 정보 포맷 표준 부재로 로그인 구현 시 보안 취약 | `openid` 스코프 및 JWT 서명 검증 라이브러리 연동 필수 |

#### 한줄 요약

- API 호출 권한 위임은 OAuth 2.0, 사용자 신원 확인 및 로그인은 OIDC를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **토큰 오용 위험(Token Misuse)**: 리소스 API 호출 시 ID Token을 전송하거나, 반대로 로그인 검증에 Access Token을 사용하여 보안 검증이 무력화되는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모바일/SPA 브라우저에서 인가 코드(Code) 가로채기 공격 발생 | **모든 Public Client에 PKCE (S256 챌린지) 의무 적용** | 인가 코드 탈취 및 도용 원천 차단 |
| ID Token과 Access Token 혼용으로 인한 API 권한 검증 누락 | **API 서버는 Access Token만 검증하고 ID Token은 클라이언트 로그인에만 한정** | 권한 상승 및 토큰 오용 방지 |
| CSRF 공격 및 토큰 재사용(Replay Attack) 침해 | **`state` 난수 파라미터 및 `nonce` 클레임 일치 여부 필수 검증** | 세션 하이재킹 및 위조 방지 |

#### 한줄 요약

- PKCE 의무화, 토큰 역할 분리, State/Nonce 검증을 통해 OAuth/OIDC 보안 취약점을 방어

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **CIAM (Customer Identity & Access Management)**: OAuth 2.0/OIDC를 기반으로 고객의 계정 라이프사이클과 다중 서비스 로그인을 통합 통제하는 차세대 신원 거버넌스.

</details>

- **OAuth 2.0과 OIDC**는 모던 웹·클라우드 환경의 인증 및 인가를 지탱하는 사실상의 글로벌 표준이며, ID Token을 통한 신원 증명과 Access Token을 통한 최소 권한 위임 원칙을 철저히 준수해야 함

#### 한줄 요약

- OAuth 2.0의 권한 위임과 OIDC의 신원 증명을 결합하여 안전한 제로 트러스트 인증·인가를 완성
