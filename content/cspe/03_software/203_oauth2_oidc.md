---
title: "OAuth 2.0·OIDC (OAuth 2.0 OIDC)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 203
extra:
  question_no: "203"
  exam_status: "기출"
  exam_history: "123회"
---

## 미리 알고가기

- OAuth 2.0은 클라이언트가 사용자 암호 대신 범위·수명이 제한된 Access Token으로 보호 자원에 접근하는 권한 위임 체계임
- OIDC는 OAuth 2.0 위에 ID Token·UserInfo·표준 Claim을 추가해 최종 사용자의 인증 결과를 클라이언트에 전달함
- Access Token은 자원 접근 권한, ID Token은 인증 사건과 사용자 식별 정보를 각 대상에게 전달하므로 용도를 바꾸면 안 됨
- Authorization Code와 PKCE는 Code Challenge·Verifier를 결합해 탈취한 인가 코드의 토큰 교환을 차단함
- 현재 보안 권고는 Authorization Code·PKCE를 사용하고 Implicit를 피하며 Resource Owner Password Credentials 사용을 금지함

## 작성 근거(검토용)

- OAuth 2.0과 OIDC는 목적, 사용자, 토큰, Scope·Claim, 검증 주체, 결과, 적용 조건으로 비교함
- 구조와 절차는 Authorization Code·PKCE·state·nonce와 ID Token 검증의 연결을 중심으로 설명함
- 업무 SSO와 외부 저장소 권한 위임은 로그인 성공률·검증 실패율·과다 Scope 거부율로 확인함

## Ⅰ. 개요

- **정의/개념**: OAuth 2.0은 보호 자원 접근 권한을 Access Token으로 위임하고, OIDC는 이 흐름에 ID Token을 추가해 사용자의 로그인·식별 결과를 전달하는 인증 계층임
- **배경/필요성**: 클라이언트가 사용자 암호를 저장하지 않고 제한된 자원 권한을 얻으며 여러 응용이 동일 인증 제공자의 로그인 결과를 검증하도록 권한 위임과 인증 목적을 분리해야 함

## Ⅱ. 특징

- OAuth 2.0은 Resource Owner·Client·Authorization Server·Resource Server 역할과 Scope 기반 Access Token 흐름을 정의함
- OIDC는 `openid` Scope, ID Token, UserInfo Endpoint와 표준 Claim으로 로그인 세션과 사용자 속성을 전달함
- Authorization Code 흐름은 브라우저에 Access Token을 노출하지 않고 Client가 Token Endpoint에서 Code를 교환함
- PKCE의 Code Verifier, `state`의 요청 상관·CSRF 방어, `nonce`의 ID Token 재사용 방어를 각각 적용함
- 클라이언트는 ID Token의 서명·Issuer·Audience·만료·nonce를 검증하고 Resource Server는 Access Token의 대상·Scope를 검증함
- Redirect URI 정확 일치, 최소 Scope, 짧은 Access Token 수명, Refresh Token 회전·폐기로 토큰 탈취 범위를 제한함

## Ⅲ. 종류 및 비교

| 판단 기준 | OAuth 2.0 | OpenID Connect |
|:---|:---|:---|
| 주된 목적 | 보호 자원 접근 권한 위임 | 최종 사용자 인증과 식별 정보 전달 |
| 사용자 역할 | Resource Owner가 권한을 승인 | End-User가 OpenID Provider에서 인증 |
| 핵심 토큰 | Access Token·선택적 Refresh Token | ID Token과 OAuth Access Token |
| 정보 표현 | Scope가 허용된 자원 작업 범위 표현 | Claim이 인증 사건·Subject·사용자 속성 표현 |
| 검증 주체 | Resource Server가 Access Token 검증 | Relying Party가 ID Token 검증 |
| 처리 결과 | Client가 허용 범위의 API 호출 | Client가 로그인 세션과 사용자 식별자 생성 |
| 적합 조건 | 제3자·서비스에 제한된 API 권한 위임 | 웹·모바일·업무 시스템의 연합 로그인 |

> 요약: OAuth 2.0은 Access Token으로 자원 권한을 위임하고 OIDC는 ID Token으로 사용자 인증 결과를 전달함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Resource Owner·End-User | 자원 접근을 승인하고 OIDC 인증을 수행하는 사용자임 |
| Client·Relying Party | 권한을 요청하고 Code를 Token으로 교환하며 ID Token을 검증함 |
| Authorization Server·OP | 사용자를 인증·승인하고 Code·Access Token·ID Token을 발급함 |
| Resource Server·UserInfo | Access Token의 대상·Scope를 검증하고 보호 자원·Claim을 제공함 |
| Code·PKCE·state·nonce | 토큰 교환 주체와 요청·응답 상관성·재사용 방지를 검증함 |
| Access·ID·Refresh Token | 자원 권한·인증 결과·Access Token 재발급 권한을 각각 전달함 |

```text
End-User -> Client/RP -> Authorization Server/OP
                  <- Code -> Token Endpoint -> Access Token + ID Token
Client/RP -> Access Token -> Resource Server/UserInfo
```

> 요약: Client는 OP의 Code를 Token으로 교환하고 ID Token은 로그인에, Access Token은 보호 자원 호출에 사용함.

## Ⅴ. 원리 및 절차 흐름도

```text
PKCE·state·nonce 생성 -> 인증·동의 -> Code 반환 -> Token 교환 -> ID Token 검증 -> API 호출
```

1. **요청 값 생성**: Client가 Code Verifier·Challenge와 `state`·`nonce`를 생성해 세션에 연결함
2. **인증·동의**: 사용자가 OP에서 로그인하고 요청 Scope와 자원 접근을 승인함
3. **Code 반환**: OP가 등록 Redirect URI로 Authorization Code와 `state`를 반환함
4. **Token 교환**: Client가 Code·Verifier를 Token Endpoint에 보내 Access Token과 ID Token을 받음
5. **Token 검증·사용**: Client가 ID Token을 검증해 로그인하고 Access Token으로 Resource Server를 호출함

> 요약: Authorization Code·PKCE가 토큰 교환을 보호하고 ID Token 검증과 Access Token 사용이 인증·권한 위임을 분리함.

## Ⅵ. 실무 사례

1. 업무 포털 SSO는 OIDC Code·PKCE와 nonce 검증을 적용하고 로그인 성공률·Token 검증 실패율을 확인함
2. 외부 저장소 연계는 OAuth 최소 Scope와 Token 회전을 적용하고 과다 Scope 거부율·폐기 지연을 확인함

## Ⅶ. 결론

- OAuth 2.0·OIDC는 권한 위임과 인증을 구분하고 Code·PKCE·Token 대상·Scope·Claim 검증을 함께 설계해야 함
