---
title: "API Security OAuth JWT Token Management"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 보안의 핵심은 OAuth 2.0/2.1 기반의 위임 인가(Delegated Authorization) 프레임워크와 RFC 7519 기반의 JWT(JSON Web Token) 또는 RFC 9068의 JWT Bearer Access Token Profile을 결합하여, 무상태(Stateless) 환경에서 클라이언트·리소스·인가서버 간의 신뢰 사슬(Chain of Trust)을 JWS 서명·JWKS(Key Set) 회전·PKCE(code_challenge/S256)·DPoP(cnf claim) 등으로 구축하는 표준 메커니즘이다.
> 2. **가치**: 세션 DB 조회 없이 마이크로서비스·Edge 게이트웨이·Serverless 환경에서 평균 0.5~3ms의 토큰 검증 레이턴시로 수평 확장이 가능하며, 중앙 IdP(Okta/Keycloak/Auth0) 연동 시 신규 시스템 추가에 따른 인증 로직 중복 구현을 약 70% 절감하고, OAuth 2.0 + OIDC는 FAPI(Financial-grade API)·PSD2·한국전자금융감독규정 등 컴플라이언스 감사 통과의 사실상 디팩트 스탠다드다.
> 3. **판단 포인트**: `alg=none`·HS256 키 혼용·취약한 시크릿(JWT Inspector 자동화 공격 시 5분 내 크랙) 등 JOSE(Javascript Object Signing & Encryption) 헤더 신뢰 위험, Refresh Token Rotation 도입 여부, JWT vs Opaque Token(introspection), HMAC vs RSA/ECDSA 서명 선택, Token 사이즈와 HTTP/2 헤더 압축 고려, JWKS 캐시 TTL vs 키 회전(Key Rollover) 윈도우 설계가 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

전통적인 웹 애플리케이션은 Cookie + Session ID 기반의 서버 세션(Stateful Session) 모델로 인증·인가를 처리했다. 하지만 **MSA(Microservices Architecture)**, **BFF(Backend-for-Frontend)**, **Open Banking(오픈뱅킹)**, **3rd Party API 플랫폼**, **SPA/모바일 하이브리드 앱** 환경으로 패러다임이 전환되면서, (1) 수십~수백 개의 서비스가 사용자 컨텍스트를 공유해야 하고, (2) Same-Origin이 아닌 외부 클라이언트도 자원에 접근해야 하며, (3) Cross-Domain SSO가 필수 요구사항이 되었다. 이러한 환경에서 자체 세션 구현은 SSRF·CSRF·세션 고정(Session Fixation)·CORS 정책 충돌·세션 동기화(Sticky Session) 문제로 한계에 부딪힌다.

**API 보안의 트라이어드**는 크게 ①인증(Authentication: 누구인가), ②인가(Authorization: 무엇을 할 수 있는가), ③감사(Auditing/Logging: 무엇을 했는가)로 나뉘며, OAuth 2.0(RFC 6749)은 ②의 표준 프레임워크, OIDC(OpenID Connect, OpenID Foundation 2014)는 ①의 표준 프로파일, JWT(RFC 7519)는 토큰의 **자기완결적(Self-contained)** 표현 포맷을 담당한다. 2012년 IETF OAuth WG에서 JWT가 OAuth 2.0의 토큰 포맷으로 채택된 이후, RFC 9068(JWT Profile for OAuth 2.0 Access Tokens, 2021)로 표준이 정착되었으며, 2024년 기준 전 세계 약 89%의 신규 API가 OAuth 2.0 기반의 토큰을 사용한다(Okta State of Secure Identity Report).

```text
[ 전통 웹 vs API-First 환경 보안 모델 비교 ]

  [전통 모놀리식 웹 - Stateful Cookie Session]
  +----------+                    +------------------+
  |  Browser | <-- Set-Cookie ----> |  App Server      |
  |  + HTML  | <-- JSESSIONID -----> |  + SessionStore  |
  +----------+                    |  (Redis/MemDB)   |
                                  +------------------+
       문제: ①Scale-out 시 세션 동기화 필요
             ②Same-Origin 한정, CORS 제약
             ③3rd Party 연동 불가 (위임 불가)

  [API-First / MSA 환경 - Stateless OAuth+JWT]
  +--------+   ①Authz Req    +------------+
  | Client | ---------------> | Auth Server|
  |(App/API| <----code+state-- |  (IdP)     |
  | SPA)   |   ②Token Req    +----+-------+
  |        | --------------->      | AT(RT)
  |        | <-- JWT(RS256) ------+
  |        |                      |
  |        |  ③API Call(+Bearer)  v
  |        | ---- GET /users ---> +--------------+
  |        |                     | Resource API |
  |        | <--- 200 OK+JWT ---> | (Stateless)  |
  |        |                     |  JWKS Verify |
  +--------+                     +--------------+
       장점: ①Stateless -> 수평확장 용이
             ②Cross-Domain 표준 (CORS, mTLS)
             ③Scope/RBAC/ABAC 위임 가능
```

전통적 인가 모델(ACL·RBAC·ABAC)이 "내부 시스템"에 초점을 맞췄다면, OAuth 2.0은 "외부 위임 인가"를 1급 시민으로 다룬다는 결정적 차이가 있다. 즉, 자원 소유자(Resource Owner)가 자신의 자격증명을 노출하지 않고도, 클라이언트에게 제한된 접근권(Scope)을 위임할 수 있게 한다. 이는 한국인터넷진흥원(KISA)의 「개인정보의 기술적·관리적 보호조치 기준」과 OWASP API Security Top 10(2023)의 API1(BOLA)·API2(Broken Authentication)·API3(BOPLA)을 충족하기 위한 핵심 토대가 된다.

- **📢 섹션 요약 비유**: 옛날 호텔의 "수건 묶음 키(Room Key with #)"가 세션 쿠키라면, OAuth+JWT는 **체크인 시 프론트 데스크가 발급하는 보안카드+신분증**(Keycard+ID Badge)이다. 객실(API)마다 신분증을 보여주기만 하면 되고, 프론트 데스크(IdP)에 물어볼 필요가 없으며, 카드 유효기간·권한 등급·발급자 서명이 모두 카드 한 장에 인쇄되어 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OAuth 2.0의 4대 역할은 **Resource Owner(자원 소유자, 일반 사용자)**, **Client(자원에 접근하려는 앱)**, **Authorization Server(인가 서버, 토큰 발급)**, **Resource Server(자원 서버, API)** 이며, OIDC는 여기에 **ID Token**과 **UserInfo Endpoint**를 추가해 SSO·프로필 정보를 표준화한다. 토큰 흐름의 핵심은 **Authorization Code + PKCE(RFC 7636)** 패턴이며, 2022년 OAuth 2.1 초안(IETF draft-ietf-oauth-v2-1)으로 deprecate된 Implicit Grant와 Resource Owner Password Credentials Grant는 신규 시스템에서 사용 금지다.

```text
[ OAuth 2.0 Authorization Code + PKCE Flow (RFC 6749 + RFC 7636) ]

 Client                 Authorization Server              Resource Server
(Public/Confidential)    (AS / IdP)                       (API Gateway)
   |                          |                                |
   |  0. PKCE 생성             |                                |
   |  code_verifier = rand(43-128)                              |
   |  code_challenge = B64URL( SHA256(code_verifier) )          |
   |                          |                                |
   |  1. /authorize?          |                                |
   |     response_type=code   |                                |
   |     &client_id=app123    |                                |
   |     &redirect_uri=...    |                                |
   |     &scope=read:user...  |                                |
   |     &state=xyz           |                                |
   |     &code_challenge=...  |                                |
   |     &code_challenge_     |                                |
   |      method=S256         |                                |
   | ------------------------> |                                |
   |   (User Login & Consent) |                                |
   | <------------------------ |                                |
   |  2. 302 Redirect         |                                |
   |     ?code=AnQ7...        |                                |
   |     &state=xyz           |                                |
   |                          |                                |
   |  3. /token               |                                |
   |     grant_type=          |                                |
   |      authorization_code  |                                |
   |     &code=AnQ7...        |                                |
   |     &code_verifier=...   |                                |
   | ------------------------> |                                |
   |                          | 4. Verify:                     |
   |                          |  SHA256(verifier)==challenge?  |
   |                          |  Authenticate client           |
   |                          |                                |
   | <------------------------ |                                |
   |  5. {access_token,       |                                |
   |     refresh_token,       |                                |
   |     id_token,            |                                |
   |     expires_in=3600,     |                                |
   |     token_type=Bearer,   |                                |
   |     scope="read:user"}   |                                |
   |                          |                                |
   |  6. GET /api/v1/user -------------------------------------->|
   |     Authorization: Bearer eyJhbGciOi...                  |
   |                          |  7. JWKS fetch <--- Verify Sig |
   |                          |     sub, aud, exp, iss, nbf   |
   | <----------------------------------------------- 200 OK    |
   |                          |                                |
   |  8. (AT 만료 후)          |                                |
   |  POST /token             |                                |
   |   grant_type=            |                                |
   |    refresh_token         |                                |
   | ------------------------> |                                |
```

JWT는 **Header.Payload.Signature**의 3-part Base64URL 인코딩 문자열로, Header에는 `alg`(RS256/ES256/HS256/EdDSA), `typ=JWT`, `kid`(Key ID) 등이, Payload(Claims Set)에는 **Registered Claims**(iss, sub, aud, exp, nbf, iat, jti), **Public Claims**(이름 충돌 방지 네임스페이스 권장), **Private Claims**(시스템 간 합의) 등이 위치한다. 서명은 JWS(JSON Web Signature, RFC 7515) 방식으로 `Base64URL(Header) + "." + Base64URL(Payload)`를 `alg`에 명시된 알고리즘으로 서명한 MAC(HS*) 또는 디지털서명(RS*/ES*/PS*/EdDSA)이다. 토큰의 위변조 무결성은 보장되지만, **페이로드는 평문**이므로 PII·비밀번호·API Key 등을 절대 넣지 않아야 한다. 민감 정보가 필요할 경우 JWE(RFC 7516, AES-GCM + RSA-OAEP)로 암호화하거나, **Token Reference Pattern**(Opaque Token + RFC 7662 Introspection)을 사용한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Authorization Server (AS)** | 토큰 발급·갱신·폐기·검증 엔드포인트 운영. 사용자 인증·동의(Consent) 수집 | OAuth 2.0(/authorize, /token, /revoke, /introspect), OIDC(/userinfo, /.well-known/openid-configuration, /jwks.json), PKCE·DPoP 검증, FAPI/PSD2 프로파일 |
| **Resource Server (RS)** | API 요청에 대해 JWT 서명·만료·스코프 검증 후 비즈니스 로직 수행 | JWKS 캐시(LRU, 1~24h TTL) + `kid` 매칭, **로컬 서명 검증**으로 AS 라운드트립 제거(평균 0.5~3ms), Scope/RBAC/ABAC 정책 매핑, API Gateway 또는 Sidecar(Istio-Envoy) 계층 |
| **Client** | PKCE code_verifier 생성, Token 저장·갱신, API 호출, Token 자동 회전(Rotation) | SPA: `localStorage` 비권장 -> **HttpOnly+SameSite=Strict 쿠키 + BFF Pattern**; 모바일: iOS Keychain/Android Keystore + Token Binding; 서버 간(M2M): **Client Credentials Grant** + mTLS |
| **JWKS (JSON Web Key Set)** | AS의 공개키 집합을 캐시 가능한 URL로 노출(`/jwks.json`). RS256/ES256/EdDSA 서명 검증의 신뢰 앵커 | `kid`별 알고리즘 명시, 키 회전 시 신규 키 pre-publish(overlap window 1~7일), 응답 캐싱 헤더 `Cache-Control: public, max-age=3600`, mTLS 또는 HTTPS로 전송 |
| **Token Storage** | AT·RT의 클라이언트 측 보관 위치 결정 — XSS·CSRF·탈취 위협 모델 균형 | HttpOnly+Secure+SameSite=Strict 쿠키, BFF Pattern, Service Worker, Secure Enclave, **Token Binding(DPoP, RFC 9449)**: `cnf` claim에 공개키 핀(Public Key Pin) |
| **Refresh Token Rotation (RTR)** | RT 1회 사용 후 폐기, 새 RT+AT 재발급. 탈취 감지 시 RT 가족 단위 폐기(RTF Detection) | RFC 6749 + OAuth 2.1 권고, Keycloak·Auth0·Okta 등 지원, RT 재사용 감지 시 모든 디바이스 세션 강제 로그아웃 |
| **PKCE (Proof Key for Code Exchange)** | 공개 클라이언트(SPA·모바일)에서도 Authorization Code 탈취(Man-in-the-Browser·Replay) 방지 | `code_verifier`(43~128자 entropy), `code_challenge = B64URL(SHA256(verifier))`, **S256 강제**(plain 금지), 2024년부터 Confidential Client도 PKCE 의무 권고 |
| **Token Introspection (RFC 7662)** | Opaque Token 또는 JWT의 실시간 폐기/스코프 확인 | `POST /introspect` + Basic Auth(client_id:secret) 또는 mTLS, 응답: `{active, scope, sub, exp, aud, ...}`, 캐시 30~300s로 AS 부하 분산 |

**JWT 알고리즘 선택의 기술적 고려사항**은 실무 핵심이다. **HS256**은 대칭키로 32바이트(256bit) 이상의 시크릿이 필수이며, 클라이언트가 서명 키를 알아야 하므로 일반적으로 Confidential Server-to-Server 시나리오에 한정한다. **RS256**(RSA-PKCS1v1.5+SHA-256, 2048bit 이상)은 가장 보편적이며 JWKS로 공개키 분배가 가능해 Public Client 검증에 적합하다. **ES256**(ECDSA P-256+SHA-256, 64바이트 서명)은 RS256 대비 약 1/8의 토큰 사이즈와 빠른 검증으로 모바일/IoT에서 유리하며, **EdDSA**(Ed25519, RFC 8037, 64바이트 고정)는 가장 현대적이고 side-channel 안전성이 우수하다. **PS256**(RSA-PSS+SHA-256)은 RS256보다 패딩 오라클에 강건해 FAPI-RW 1.0에서 강제된다. 2024년 기준 OWASP는 **`alg=none` 차단**, **`alg` 화이트리스트**(서버 측에서 서명 검증 시 accept 리스트에 명시된 알고리즘만 수락, 클라이언트가
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 404 / 800

<- **이전**: [403. 클라우드 네이티브 보안 CNAPP CWPP](/studynote/12_it_management/05_security_compliance/403_cloud_native_security_cnapp_cwpp/)
**다음**: [405. 모바일 보안 MDM MAM 앱 보호](/studynote/12_it_management/05_security_compliance/405_mobile_security_mdm_mam_app_protection/) ->

---
