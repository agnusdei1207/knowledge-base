---
sidebar:
  order: 174
  label: "174. OAuth 2.0•OIDC"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
date: "2026-08-26T10:25:00+09:00"
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

- **OAuth 2.0 & OIDC**: 비밀번호 공유 없이 자원 접근 권한을 위임하는 OAuth 2.0 인가 프레임워크와 ID Token(JWT)을 통해 사용자 신원을 인증하는 OIDC(OpenID Connect) 표준 프로토콜.
- **Access Token vs ID Token**: 리소스 API 호출 인가용 불투명/JWT 토큰(Access Token)과 사용자 로그인 신원 증명용 JWT(ID Token).

</details>

- 정의/개념: 비밀번호 노출 없이 제3자 앱에 자원 접근 권한을 위임하는 **OAuth 2.0과 ID Token 기반 사용자 신원 인증을 제공하는 OIDC 표준 프로토콜**
- 배경/필요성: 제3자 앱에 비밀번호를 직접 전달하던 기존 방식의 **크리덴셜 탈취 위험, 과도한 권한 노출 및 안전한 통합 로그인(SSO) 구현 불가**

#### 한줄 요약
- 인가(권한 위임)의 OAuth 2.0과 인증(신원 증명)의 OIDC를 결합하여 안전한 로그인과 API 보안을 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PKCE(Proof Key for Code Exchange)**: 모바일/SPA 환경에서 Secret 노출 없이 코드 탈취 공격을 방어하는 동적 챌린지 검증 표준(RFC 7636).
- **JWKS(JSON Web Key Set)**: 리소스 서버가 인가 서버의 공개키 목록을 조회하여 ID/Access Token의 전자서명을 비대칭 검증하는 엔드포인트.

</details>

- 사용자 비밀번호를 클라이언트에 제공하지 않는 **안전한 권한 위임(Delegated Authorization)**
- 표준 JWT 클레임(iss, sub, aud, exp)을 포함하는 **사용자 신원 확인(ID Token / SSO)**
- 모바일/SPA 등 공개 클라이언트(Public Client)의 코드 탈취를 차단하는 **PKCE 보안 확장**

#### 한줄 요약
- Access Token과 ID Token의 분리 및 PKCE 챌린지를 통해 웹/모바일 환경의 인증·인가를 통제한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OAuth/OIDC 4대 신뢰 주체**: Resource Owner(사용자), Client(앱), Authorization Server(인가 서버), Resource Server(API 서버).

</details>

```text
[OAuth 2.0 및 OIDC 신뢰 경계 및 4대 엔티티 구조]
|-- 1. Resource Owner (사용자: 브라우저/모바일에서 로그인 및 권한 위임 동의)
|-- 2. Client Application (SPA / 모바일 앱)
|   |-- PKCE Engine (code_verifier 생성 및 code_challenge S256 해시)
|   `-- Token Storage (ID Token 및 Bearer Access Token 보관)
|-- 3. Authorization Server / IdP (Google, Kakao, Keycloak 인가 서버)
|   |-- Login & Consent UI (사용자 인증 및 스코프 동의 화면 제공)
|   |-- Token Issuer (Authorization Code 발급 및 ID/Access Token JWT 서명)
|   `-- JWKS Endpoint (토큰 검증용 공개키 제공)
`-- 4. Resource Server (백엔드 API 서버: Access Token 서명 및 Scope 검증 후 데이터 반환)
```

선의 의미: 계층 및 사용자가 인가 서버에서 로그인하면 클라이언트가 인가 코드로 토큰을 교환받아 리소스 서버에 접근하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 자원 소유자 (Resource Owner)| 자신의 데이터에 대한 **제3자 애플리케이션의 접근을 승인/동의하는 실제 사용자** | 권한 승인 주체 |
| 클라이언트 (Client App) | 사용자를 대신하여 **인가 서버에 로그인을 요청하고 발급받은 토큰으로 API 호출** | Public / Confidential |
| 인가 서버 (Auth Server/IdP)| 사용자 인증 후 **인가 코드, Access Token, ID Token(JWT) 발급·서명**| IdP (Keycloak, Auth0) |
| 자원 서버 (Resource Server)| **Access Token의 유효성·Scope를 검증하고 보호 자원 반환**| API 백엔드 |

#### 한줄 요약
- 자원 소유자, 클라이언트, 인가 서버, 자원 서버가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OIDC Auth Code with PKCE 5단계**: 인가 요청 $\to$ 사용자 로그인/동의 $\to$ 1회용 Code 회신 $\to$ PKCE 토큰 교환 $\to$ ID/Access Token 사용.

</details>

```text
클라이언트의 소셜 로그인 및 API 접근 요청
        │
   1. [인가 요청] Client가 PKCE(code_challenge)와 state/nonce를 생성하여 `/authorize`로 리다이렉트
        │
   2. [사용자 인증 및 동의] 사용자가 IdP 화면에서 로그인하고 프로필 접근 권한(Scope) 동의
        │
   3. [인가 코드 회신] Auth Server가 사전에 등록된 Redirect URI로 일회용 Authorization Code 회신
        │
   4. [토큰 교환] Client가 `/token`으로 Code와 원본 `code_verifier`를 전송하여 PKCE 일치 검증
        │
   Client는 ID Token으로 로그인 처리하고, Access Token을 API 요청 헤더에 담아 자원 수신
```

#### 한줄 요약
- 인가 요청 → 사용자 인증 → 코드 회신 → 토큰 교환 → 토큰 사용 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OAuth 2.0 vs OIDC**: 권한 위임 전용 프레임워크(OAuth)와 사용자 신원 증명 및 로그인 전용 프로토콜(OIDC).

</details>

| 비교 항목 | OAuth 2.0 (순수 권한 위임) | OIDC (OpenID Connect: 인증 확장) |
|:---|:---|:---|
| 핵심 목적 | **타사 API 호출 권한 위임 (무엇을 할 수 있는가)** | **사용자 신원 증명 및 단일 로그인 (누구인가)** |
| 핵심 발급 토큰 | **Access Token (API 접근 인가용)** | **ID Token (JWT 포맷 신원 정보) + Access Token** |
| 사용자 정보 표준 | 표준 사용자 프로필 규격 부재 (벤더별 상이) | **표준 `/userinfo` 엔드포인트 및 JWT 클레임 규격** |
| 최적 적용 사례 | **구글 캘린더 연동, 깃허브 저장소 접근 권한 위임** | **소셜 간편 로그인 (Google/Kakao), 전사 통합 SSO** |

#### 한줄 요약
- API 호출 권한 위임은 OAuth 2.0, 사용자 신원 확인 및 로그인은 OIDC를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Token Misuse**: 리소스 API 호출 시 ID Token을 전송하거나, 반대로 로그인 검증에 Access Token을 사용하여 검증 체계가 무력화되는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모바일/SPA 브라우저에서 인가 코드(Code) 가로채기 공격 발생 | **모든 Public Client에 PKCE (S256 챌린지) 의무 적용** | 인가 코드 탈취 및 도용 원천 차단 |
| ID Token과 Access Token 혼용으로 인한 API 권한 검증 누락 | **API는 Access Token만 검증, ID Token은 클라이언트 로그인 전용** | 권한 상승 및 토큰 오용 방지 |
| CSRF 공격 및 토큰 재사용(Replay Attack) 침해 | **`state` 난수 파라미터 및 `nonce` 클레임 일치 여부 필수 검증** | 세션 하이재킹 및 위조 방지 |
| 토큰 탈취 시 유효기간 만료 전까지 강제 만료 불가 | **Access Token 유효기간 단축(15분) 및 Redis 기반 토큰 블랙리스트 구축** | 침해 피해 최소화 |

#### 한줄 요약
- PKCE 의무화, 토큰 역할 분리, State/Nonce 검증, 블랙리스트 구축으로 운영한다.

## Ⅶ. 결론

- 클라우드 및 마이크로서비스 환경에서 안전한 신원 관리와 권한 위임을 실현하기 위해 **OIDC 기반의 ID Token으로 사용자 인증(SSO)을 일원화하고, OAuth 2.0 Access Token과 PKCE 보안 확장을 결합**하여 제로 트러스트 엔터프라이즈 인증·인가 체계 완성

#### 한줄 요약
- OAuth 2.0과 OIDC는 권한 위임과 신원 증명을 계층적으로 결합하여 현대 웹과 모바일 환경의 보안 로그인을 구현하는 핵심 글로벌 표준이다.