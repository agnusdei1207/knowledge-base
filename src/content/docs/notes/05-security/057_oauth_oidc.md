---
sidebar:
  order: 57
  label: "057. OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "OAuth 2.0•OIDC (OAuth 2.0 OIDC)"
date: "2026-08-13T19:54:00+09:00"
tags:
  - "notes-security"
weight: 57
extra:
  question_no: "057"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "123회 기출이며 웹•모바일 권한위임의 기본 구조임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **개방형 권한 위임 2.0(Open Authorization 2.0, OAuth 2.0)**: 사용자 비밀번호 노출 없이 제3자 애플리케이션(Client)에게 자원 접근 권한을 안전하게 위임하는 오픈 표준 프레임워크.
- **오픈아이디 연결(OpenID Connect, OIDC)**: OAuth 2.0 프로토콜 레이어 상단에 사용자 신원 인증(Authentication) 및 ID 토큰(JWT) 전달 기능을 확장한 신원 표준.

</details>

- 정의/개념: 권한 위임 **OAuth 2.0**과 신원 인증 **OIDC**
- 배경/필요성: 자격증명 공유는 **비밀번호 노출•과다 권한** 유발

#### 한줄 요약

- OAuth 2.0 기반의 리소스 접근 권한 위임과 OIDC 기반의 사용자 신원 인증을 통합 연계함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **권한 코드(Authorization Code)**: 인가 서버가 사용자 동의 승인 후 클라이언트에 임시 발급하는 일회성/단기 교환용 코드.
- **코드 교환용 증명 키(Proof Key for Code Exchange, PKCE)**: 모바일/SPA의 인가 코드 탈취 및 재전송 공격을 막기 위해 챌린지/검증 키를 결합하는 표준 확장.
- **Redirect URI**: 인가 코드 및 토큰을 수신할 사전에 인가 서버에 등록된 클라이언트의 정식 주소.
- **접근 토큰(Access Token)**: 자원 서버의 API 리소스에 접근할 수 있는 권한 및 Scope가 담긴 서명 토큰.
- **신원 토큰(Identity Token, ID Token)**: 사용자 식별자(sub), 발급자(iss), 만료시간(exp)이 담긴 OIDC 전용 JWT 서명 문서.
- **Nonce**: OIDC에서 Replay 공격 및 ID 토큰 주입 공격을 막기 위해 검증하는 일회성 난수.
- **갱신 토큰 회전(Refresh Token Rotation)**: Access Token 재발급 시 Refresh Token도 동시에 재발급하여 탈취된 토큰의 재사용을 무력화하는 기술.

</details>

- **권한 코드** 교환 시 **PKCE** 및 엄격한 **Redirect URI** 결속 검증.
- API 자원 접근용 **접근 토큰**과 클라이언트 사용자 신원확인용 **신원 토큰** 역할 분리.
- 서명(iss, aud, exp) 및 **Nonce** 검증, 보안성 강화를 위한 **갱신 토큰 회전** 적용.

#### 한줄 요약

- PKCE 기반 인가 코드 결속, Access/ID 토큰 역할 분리 및 Refresh Token Rotation을 통한 세션 관리.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **자원 소유자(Resource Owner)**: 보호 대상 자원 접근 권한을 소유한 실제 사용자.
- **클라이언트(Client)**: 사용자의 자원에 접근하기 위해 인가 서버에 권한 위임을 요청하는 서드파티 앱.
- **인가 서버(Authorization Server / IdP)**: 사용자를 인증하고 접근 동의를 받아 Authorization Code 및 Access/ID Token을 발급하는 서버.
- **자원 서버(Resource Server)**: Access Token의 유효성 및 Scope를 검증하여 API 데이터를 제공하는 백엔드.

</details>

```text
OAuth 2.0•OIDC 구조
├─ 자원 소유자: 인증•제한 권한 동의
├─ 클라이언트: 인가 요청•토큰 사용
├─ 인가•OIDC 제공자: 코드•토큰 발급
├─ 자원 서버: 대상•범위•객체 권한 집행
└─ 토큰•키 관리: 서명 키•수명 관리
```

| 구성요소 | 책임 |
|:---|:---|
| 자원 소유자 | 신원 인증 및 클라이언트 접근 권한 동의 표명 |
| 클라이언트 | **OAuth 2.0/PKCE** 인가 요청, 토큰 수신 및 API 호출 |
| 인가•OIDC 제공자 | **인가 서버**로서 사용자 인증, Authorization Code, Access Token 및 ID Token 발급 |
| 자원 서버 | API 호출 시 제출된 Access Token 서명, 만료, Scope 및 객체 권한 2차 검증 |
| 토큰•키 관리 | JWKS 공개키 배포, 토큰 유효기간(TTL) 및 Refresh Token 수명 통제 |

#### 한줄 요약

- 자원 소유자, 클라이언트, 인가 서버(IdP), 자원 서버 및 JWKS 키 관리 구조로 구성됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **클라이언트•Redirect URI 검증**: 사전 등록된 Client ID 및 정확한 Redirect URI 매칭 확인 단계.
- **권한 코드 생성**: 사용자 동의 후 일회성 Authorization Code 발급 단계.
- **코드•PKCE 결속 검증**: code_verifier와 code_challenge 서명을 검증하는 단계.
- **접근•ID 토큰 발급**: Access Token(JWT/Opaque) 및 ID Token(JWT) 동시 발급 단계.
- **발급자•대상•범위 검증**: 자원 서버에서 iss, aud, exp, scope 검증 단계.

</details>

```text
범위•PKCE•Nonce 인가 요청
            │
            ▼
1. 클라이언트•Redirect URI 검증
            │
            ▼
사용자 인증•동의
            │
            ▼
2. 권한 코드 생성
            │
            ▼
3. 코드•PKCE 결속 검증
            │
            ▼
4. 접근•ID 토큰 발급
            │
            ▼
API 자원 요청
            │
            ▼
5. 발급자•대상•범위 검증
            │
            ▼
제한된 자원 응답
```

### 동작 원리

1. **클라이언트•Redirect URI 검증**: 클라이언트 요청의 Redirect URI 및 PKCE 조건 1차 대조.
2. **권한 코드 생성**: 자원 소유자 인증 및 Scope 동의 후 Authorization Code 발급.
3. **코드•PKCE 결속 검증**: 클라이언트가 제출한 code_verifier 검증 후 코드 교환 허용.
4. **접근•ID 토큰 발급**: API용 **접근 토큰** 및 사용자 정보용 **신원 토큰** 생성 전송.
5. **발급자•대상•범위 검증**: 자원 서버에서 토큰 서명(iss, aud), exp 및 Scope 인가 판정.

#### 한줄 요약

- Redirect URI/PKCE 검증, Authorization Code 발급, PKCE 대조, Access/ID Token 발급 및 API 서명 검증을 집행함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OAuth•OIDC 역할 분리(OAuth vs OIDC Separation)**: OAuth 2.0은 API 리소스 접근 권한 위임(Authorization), OIDC는 사용자 신원 인증(Authentication)을 담당하는 명확한 기술적 역할 분담.

</details>

| 표준 | 역할 | 핵심 토큰 및 산출물 | 검증 핵심 |
|:---|:---|:---|:---|
| **OAuth 2.0** | 자원 접근 권한 위임(Authorization) | Access Token, Refresh Token | Scope 범위, Redirect URI, PKCE |
| **OIDC** | 사용자 신원 인증(Authentication) | ID Token (JWT) | iss, sub, aud, Nonce 서명 검증 |

#### 한줄 요약

- 권한 위임 프로토콜 OAuth 2.0과 신원 인증 레이어 OIDC를 역할에 맞게 명확히 분리 적용함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IETF RFC 9700**: OAuth 2.0 Security Best Current Practice(BCP) 표준 문서로 Implicit Grant 사용 금지 및 PKCE 의무화 지정.
- **OIDC Core 1.0**: OpenID Connect 1.0 핵심 명세로 ID 토큰 무결성 및 사용자 인증 흐름 검증 지침.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 인가 코드 탈취 및 재전송 공격 | **IETF RFC 9700** 가이드 준수 및 **PKCE** 적용 | 모바일/SPA 환경의 코드 탈취 및 재전송 완전 차단 |
| ID Token 서명 검증 누락 | **OIDC Core 1.0** 지침 준수 및 iss, aud, Nonce 검증 | 위조 ID Token 주입 및 사용자 신원 도용 차단 |
| Access Token 및 Refresh Token 탈취 | **갱신 토큰 회전** 및 mTLS/DPoP 결속 | 토큰 유출 시에도 재사용 및 권한 남용 불가능 조치 |

#### 한줄 요약

- IETF RFC 9700 모범 사례를 준수하여 PKCE를 적용하고, OIDC Core 1.0 기준 ID 토큰 검증 및 Refresh Token Rotation을 집행함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **연동 목적별 표준 선택 기준(Standard Selection Criteria)**: API 권한 위임은 OAuth 2.0, 사용자 SSO 및 신원 전달은 OIDC를 선택하고 PKCE와 DPoP 보안을 적용하는 아키텍처 지침.

</details>

- **연동 목적별 표준 선택 기준**을 수립하여 리소스 접근은 **OAuth 2.0**, SSO 신원 연동은 **OIDC**를 적용하고 **PKCE** 및 **갱신 토큰 회전**을 필수로 구축.

#### 한줄 요약

- API 권한은 **OAuth 2.0**, SSO 신원은 **OIDC** 적용
