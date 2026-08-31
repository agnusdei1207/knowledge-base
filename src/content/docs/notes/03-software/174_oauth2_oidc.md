---
sidebar:
  order: 174
  label: "174. OAuth 2.0•OIDC"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 서드파티 애플리케이션 및 모바일/SPA 환경에서 사용자의 패스워드를 직접 공유할 경우 발생하는 자격증명 유출, 과도한 전체 권한 부여 및 특정 서비스 접근 차단의 불가능성을 해결하고, 권한 위임(Authorization)과 사용자 신원 인증(Authentication)이 혼용되어 발생하는 보안 취약점을 방어하기 위해, 범위(Scope)와 수명이 제한된 Access Token을 발급하는 OAuth 2.0과 표준 JWT 기반 ID Token으로 사용자 신원을 증명하는 OIDC(OpenID Connect)를 도입하여 **안전한 권한 위임과 전사 통합 싱글 사인온(SSO)을 달성**할 필요

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
|-- Resource Owner
|-- Client Application
|   |-- PKCE Engine (code_verifier 생성 및 code_challenge S256 해시)
|   `-- Token Storage (ID Token 및 Bearer Access Token 보관)
|-- Authorization Server / IdP
|   |-- Login & Consent UI (사용자 인증 및 스코프 동의 화면 제공)
|   |-- Token Issuer (Authorization Code 발급 및 ID/Access Token JWT 서명)
|   `-- JWKS Endpoint (토큰 검증용 공개키 제공)
`-- Resource Server
```

선의 의미: 계층 및 사용자가 인가 서버에서 로그인하면 클라이언트가 인가 코드로 토큰을 교환받아 리소스 서버에 접근하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 자원 소유자 | 클라이언트의 **자원 접근 권한** 승인 |
| 클라이언트 | 인가 요청과 토큰 기반 API 호출 |
| 인가 서버·IdP | 코드·Access Token·ID Token 발급 |
| 자원 서버 | **Access Token·Scope** 검증과 자원 제공 |

#### 한줄 요약
- 인가 서버가 자원 소유자의 승인을 토큰이라는 증표로 바꿔 주므로, 클라이언트는 비밀번호를 한 번도 보지 않고 자원 서버는 사용자에게 다시 묻지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OIDC Code with PKCE**: 인가 요청, 인증·동의, 코드 회신, 토큰 교환.

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

동작 원리:

1. 인가 요청: PKCE·state·nonce와 요청 전송
2. 사용자 인증 및 동의: IdP 인증과 Scope 승인
3. 인가 코드 회신: 등록 Redirect URI로 코드 전달
4. 토큰 교환: code_verifier 검증 후 토큰 발급

#### 한줄 요약
- 코드 발급과 토큰 교환을 분리해 브라우저 구간에는 한 번만 쓰이는 코드만 노출되므로, 리다이렉트가 가로채여도 공격자가 얻는 값어치가 크게 줄어든다.

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
| 공개 클라이언트의 인가 코드 탈취 | **PKCE S256** 적용 | 탈취 코드의 토큰 교환 위험 감소 |
| ID Token과 Access Token 혼용으로 인한 API 권한 검증 누락 | **API는 Access Token만 검증, ID Token은 클라이언트 로그인 전용** | 권한 상승 및 토큰 오용 방지 |
| CSRF와 ID Token 재사용 공격 | **state·nonce 검증** | 요청 상관관계와 재사용 여부 확인 |
| Access Token 탈취와 폐기 지연 | 위험 기반 **수명·회전·폐기 정책** 적용 | 토큰 노출 시간과 피해 범위 제한 |

#### 한줄 요약
- 네 대책은 토큰이 주는 편의가 낳은 탈취·오용 위험을 검증 절차와 짧은 수명으로 되사는 선택이며, 수명을 줄일수록 피해 범위는 좁아지고 재발급 트래픽은 늘어난다.

## Ⅶ. 결론

- 현대 웹, 모바일, SaaS 및 마이크로서비스 생태계에서 가장 기본적이고 필수적인 **글로벌 표준 인증·인가(AuthN/AuthZ) 인프라 프레임워크**로 확립되었으며, 실무 구축 시에는 **공개 클라이언트(SPA/Mobile)의 코드 탈취를 방어하는 PKCE(S256) 강제, CSRF 및 재생 공격을 차단하는 `state`/`nonce` 검증, 신원 확인용 ID Token과 API 인가용 Access Token의 엄격한 역할 분리, Access Token의 초단기 수명(15분) 및 Refresh Token Rotation(RTR)**을 결합하여 무결점 제로 트러스트 API 보안을 완성

#### 한줄 요약
- ID Token은 클라이언트, Access Token은 자원 서버에서 검증한다.
