---
sidebar:
  order: 174
  label: "174. OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **OAuth 2.0 (Open Authorization 2.0)**: 사용자의 비밀번호를 제3자 앱(Client)에 넘기지 않고, 구글이나 카카오 등 인가 서버(Authorization Server)를 통해 한시적인 접근 권한(Access Token)만 안전하게 위임하는 표준 프레임워크.
- **OIDC (OpenID Connect)**: OAuth 2.0 프레임워크 위에서 작동하며, 사용자가 '누구인지(Identity)' 증명하는 ID Token(JWT)을 추가 발급하여 간편 로그인(SSO)을 표준화한 인증 프로토콜.
- **Authentication(인증) vs Authorization(인가)**: 인증은 사용자의 신원을 확인(Who you are)하는 과정이며, 인가는 인증된 사용자가 특정 자원에 접근할 권한(What you can do)이 있는지 제어하는 과정.

</details>

- 정의/개념: 타사 서비스 자원에 대한 권한 위임 체계인 **OAuth 2.0**과, 이를 기반으로 사용자 신원 확인 계층을 추가한 확장 인증 프로토콜인 **OIDC**의 결합 아키텍처
- 배경/필요성: 사용자가 새로운 서비스에 가입할 때마다 구글/네이버 비밀번호를 직접 입력해야 했던 과거 방식의 보안 취약성(자격 증명 유출 위험)을 원천 차단하기 위한 통제 기법 요구성

#### 한줄 요약

- OAuth는 API 문을 열 수 있는 출입증을 주고 OIDC는 누가 로그인했는지 확인하는 신분 확인서를 별도로 제공한다.

## Ⅱ. 특징 (OAuth 2.0 및 OIDC 핵심 차별화 요소)

<details><summary>핵심 용어</summary>

- **Access Token (접근 토큰)**: 리소스 서버(구글 캘린더 API 등)에 접근하기 위한 랜덤 문자열(또는 JWT) 출입증. OAuth 2.0의 핵심 결과물.
- **ID Token (신원 토큰)**: 사용자의 이름, 이메일, 발급자 정보 등 신원(Identity) 정보를 담고 있는 무조건적인 JWT 포맷의 토큰. OIDC의 핵심 결과물.

</details>

- **Delegated Authorization (사용자 개입 없이 권한 위임을 처리하는 OAuth 2.0 메커니즘)**
- **Identity Layer (OAuth 2.0 위에 얹혀진 사용자 프로필 제공 OIDC 계층)**
- **Token Separation (자원 접근용 Access Token과 신원 확인용 ID Token의 명확한 분리)**
- **PKCE (Proof Key for Code Exchange) (인가 코드 가로채기를 방지하는 보안 확장 표준)**

#### 한줄 요약

- 브라우저를 지나는 일회용 인가 코드는 PKCE로 묶고 실제 API 출입증은 서버 간 채널에서 교환해 코드 탈취와 비밀번호 노출을 줄인다.

## Ⅲ. 구조 및 구성요소 (OAuth 2.0 / OIDC 4대 참여자)

<details><summary>핵심 용어</summary>

- **Authorization Server (인가 서버)**: 사용자를 로그인시키고 동의 화면을 띄운 뒤, 인가 코드(Code)와 최종 토큰(Access/ID Token)을 발급하는 중앙 권한 관리 주체(예: Google 서버).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   OAuth 2.0 / OIDC Actor Relationships                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Resource Owner : [사용자 (당신)] ──(동의)──► [Authorization Server] │
│ 2. Client         : [제3자 앱 (당근마켓)] ◄──(토큰 발급)──┘            │
│                       │                                                │
│                       ▼ (Access Token 제시)                            │
│ 3. Resource Server: [구글 캘린더 API (당신의 캘린더 보유)]             │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 사용자가 인가 서버에 로그인하고 동의하면, 인가 서버가 제3자 앱(Client)에게 토큰을 쥐여주고, 제3자 앱은 그 토큰을 Resource Server에 제시하여 데이터를 읽어가는 위임 구조.

| 핵심 구성요소 | 개념적 역할 | 실무 예시 |
|:---|:---|:---|
| **Resource Owner** | **보호된 자원의 소유권을 가진 실제 사용자** | **스마트폰 앞의 사용자** |
| **Client** | **사용자를 대신하여 자원에 접근하려는 제3자 애플리케이션** | **배달의민족, 쏘카 앱** |
| **Authorization Server** | **사용자 인증, 동의 처리 후 토큰을 발급하는 서버** | **카카오/구글 로그인 서버**|
| **Resource Server**| **Access Token을 검증하고 실제 데이터를 내어주는 API 서버**| **구글 캘린더, 카카오페이**|

#### 한줄 요약

- 사용자는 인가 서버에서만 비밀번호를 입력하고 클라이언트는 일회용 교환표로 신분 확인서와 API 출입증을 따로 받는다.

## Ⅳ. 흐름도 (Authorization Code Grant 흐름)

<details><summary>핵심 용어</summary>

- **Authorization Code (인가 코드)**: 클라이언트가 토큰을 직접 받기 전, 브라우저(프론트)를 통해 전달받는 1회용 교환권. 이 코드를 백엔드 서버로 가져가야만 실제 토큰으로 교환 가능.

</details>

```text
[Client]                                  [Authorization Server]
   │                                               │
   ├─ 1. Login Request (client_id, redirect_uri) ─►│
   │                                               │
   │◄─ 2. Auth & Consent (로그인 및 권한 동의) ───┤ (Resource Owner 개입)
   │                                               │
   │◄─ 3. Return Authorization Code (인가 코드) ───┤ (Redirect URI로 전달)
   │                                               │
   ├─ 4. Exchange Code for Tokens ────────────────►│ (서버 대 서버 통신)
   │     (Code + Client Secret)                    │
   │                                               │
   │◄─ 5. Return Access Token & ID Token ──────────┤
   │                                               │
[Client (Token 보유)] ──(Access Token)──► [Resource Server]
```

### 동작 원리

1. **Auth Request**: 클라이언트가 유저를 인가 서버의 로그인 창으로 Redirect (파라미터: `response_type=code`).
2. **Consent & Code**: 유저가 로그인/동의 완료 시, 인가 서버가 `Redirect URI`로 1회용 `Authorization Code`를 실어 브라우저로 반환.
3. **Token Exchange**: 클라이언트 백엔드 서버가 방금 받은 Code와 자신의 암호(Client Secret)를 인가 서버로 직접 보내어, Access Token과 ID Token을 발급받음 (**OIDC 인증 완결**).

#### 한줄 요약

- 클라이언트는 상태값와 PKCE를 확인한 뒤 ID 토큰으로 로그인만 만들고 별도 접근 토큰으로 API를 호출한다.

## Ⅴ. 종류 및 비교 (OAuth 2.0 대 OIDC 1:1 비교)

<details><summary>핵심 용어</summary>

- **Scope (스코프)**: Access Token이 허용하는 권한의 범위(예: `calendar.read`, `profile`). OIDC를 사용하려면 반드시 `openid` 스코프를 요청해야 함.

</details>

| 비교 항목 | OAuth 2.0 (순수 인가) | OIDC (인증 확장) |
|:---|:---|:---|
| **목적 (Purpose)** | **권한 위임 (Authorization)** | **신원 확인 및 로그인 (Authentication)**|
| **핵심 결과물** | **Access Token** | **ID Token (JWT 포맷 강제)** |
| **토큰의 내용** | 서버만 알면 되는 랜덤 문자열 (Opaque Token 가능) | **반드시 사용자의 속성(Claim)이 담긴 구조화된 JWT**|
| **표준 Scope** | 리소스 서버가 정의 (예: `email`, `contacts`) | **`openid` 스코프 필수 요청** |

#### 한줄 요약

- OAuth는 사용자가 무엇을 허용했는지를 자원 서버에 전달하고 OIDC는 누가 인증됐는지를 클라이언트에 전달한다.

## Ⅵ. 실무 고려사항 및 대책 (OAuth/OIDC 3대 실무 보안 파행)

<details><summary>핵심 용어</summary>

- **PKCE (Proof Key for Code Exchange)**: 모바일 앱처럼 `Client Secret`을 안전하게 숨길 수 없는 환경(Public Client)에서, 인가 코드(Code) 가로채기 공격(Interception Attack)을 방어하기 위해 도입된 암호학적 챌린지 기법.

</details>

| 3대 보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Token Misuse (혼용)** | 개발자가 ID Token을 API 헤더에 넣고 호출 | **리소스 서버는 반드시 Access Token만 인가(Authorization) 처리**|
| **2. Code Interception** | 해커가 브라우저 리다이렉트 시 인가 코드 탈취| **모든 Public Client(모바일, SPA)에 PKCE 무조건 의무화**|
| **3. CSRF 및 Replay Attack**| 공격자가 조작된 로그인 링크를 클릭 유도 | **`state` 난수 및 `nonce` 값을 검증하여 위조 방지**|

> 사례: **카카오 / 네이버 OIDC(OpenID Connect) 연동 시 JWT 검증(서명, 만료일, Audience) 누락으로 인한 계정 탈취 사례**

#### 한줄 요약

- 포털 로그인에는 ID 토큰의 발급자·대상·논스를 확인하고 API는 자신의 대상과 범위가 담긴 접근 토큰만 받아야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Token Validation (토큰 검증)**: 수신한 ID Token의 서명(Signature), 발급자(Issuer), 대상(Audience), 만료 시간(Expiration)을 클라이언트가 직접 검증해야 하는 OIDC 핵심 보안 수칙.

</details>

- **OAuth/OIDC 보안 기준**에 따라 B2C 인증 및 인가 구현 시 **Authorization Code Grant Flow 및 PKCE 적용** 필수

#### 한줄 요약

- ID 토큰은 로그인 확인에만, 접근 토큰은 자원 접근에만 사용하고 인가 코드 흐름에는 PKCE·상태값·논스 검증을 모두 적용해야 한다.
