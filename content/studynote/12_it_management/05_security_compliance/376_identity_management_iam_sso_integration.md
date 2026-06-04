+++
title = "376. 신원 관리 IAM 통합 인증 SSO (Identity Management IAM SSO Integration)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IAM은 신원(Identity), 인증(Authentication), 권한(Authorization), 감사(Auditing)의 4A 통합 거버넌스 체계이며, SSO는 SAML 2.0, OAuth 2.0/OIDC, Kerberos, FIDO2/WebAuthn 등 신뢰된 토큰/Assertion 교환 프로토콜을 통해 N개의 애플리케이션에 대한 단일 로그온을 실현하는 신원 페더레이션(Identity Federation) 아키텍처이다.
> 2. **가치**: 평균 기업 내 25~150개의 SaaS 애플리케이션에서 사용자가 기억하는 패스워드 수를 평균 2.7개(Forrester)로 줄이고, 헬프데스크 패스워드 리셋 비용의 70% 절감, 피싱 성공률 약 99% 감소(MFA 적용 시, Microsoft 2019), 사용자 온보딩 시간을 주 단위에서 시간 단위로 단축시킨다.
> 3. **판단 포인트**: SAML 2.0(엔터프라이즈 B2E, XML/Assertion) vs OIDC(모던 클라우드/SPA/API, JWT) vs Kerberos(사내 AD, 티켓 기반) 프로토콜 선택, IdP 집중화(Single Point of Failure) 대비 페일오버 및 다중 IdP 전략, 토큰 수명(Access Token TTL 5~15분, Refresh Token 8~24시간)과 세션 하이재킹 방어 설계가 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

전통적인 사용자 계정 관리 모델은 각 애플리케이션·시스템이 자체적으로 사용자 ID/패스워드 저장소(User Store)를 보유하는 **Siloed Identity Model**이었다. 이는 ① 사용자 입장에서 평균 70~100개의 계정(ID Chaos) 관리 부담, ② 관리자 입장의 계정 생성/폐기/권한 변경의 비일관성(Provisioning 지연 평균 3~5일), ③ 보안 측면의 약한 패스워드 재사용와 유출 시 Lateral Movement 위험이라는 3중 고충(Triple Burden)을 야기했다. 2017년 NIST SP 800-63B의 Digital Identity Guidelines는 "Memorized Secret" 만으로 인증하는 모델을 deprecated로 규정하고, 이후 클라우드 전환과 Zero Trust Architecture(ZTA) 가속화로 IAM + SSO는 **신뢰의 뿌리(Root of Trust)** 로 자리 잡았다.

```text
[Before: Siloed Identity Chaos]                    [After: Federated IAM with SSO]
+----------+  +----------+  +----------+          +----------------------------+
|  ERP     |  |  CRM     |  |  Mail    |          |       IdP (Identity Hub)   |
|  [ID/PW] |  |  [ID/PW] |  |  [ID/PW] |          | +----------------------+  |
|  Local   |  |  Local   |  |  Local   |    ---►  | | SAML 2.0 / OIDC /   |  |
+----------+  +----------+  +----------+          | | Kerberos / FIDO2    |  |
   N개 ID     N개 ID      N개 ID                  | +----------------------+  |
   관리 곤란    정책 불일치    감사 불가            |  AD/LDAP ◄-- SCIM 2.0 --+|
                                                   +----+------+------+-----+ |
                                                        |      |      |       |
                                                   +----v-+ +--v--+ +-v---+  |
                                                   | ERP  | | CRM | | Mail| ◄+
                                                   |(SP)  | |(SP) | |(SP) |
                                                   +------+ +-----+ +-----+
                                                   Single Sign-On + 중앙 집중 거버넌스
```

최근 5년간의 패러다임 전환을 정리하면 다음과 같다.

| 시대 | 패러다임 | 인증 수단 | 위험/한계 |
| :--- | :--- | :--- | :--- |
| 1990s | Siloed ID/PW | 사용자 기억 | 패스워드 재사용, 관리 비용 |
| 2000s | LDAP 중앙화 | Directory 기반 | 도메인 종속, Federation 미지원 |
| 2010s | SAML 2.0 SSO | XML Assertion, IdP/SP | 모바일/JSON 미흡, X.509 PKI 복잡 |
| 2020s | OAuth 2.0 + OIDC | JWT, Token-based | 토큰 탈취, Refresh Token 관리 |
| 2025+ | Passwordless / ZTA | FIDO2, Passkey, MFA | 디바이스 신뢰, Step-up Auth |

- **📢 섹션 요약 비유**: 시루대(Silo)마다 다른 열쇠를 들고 다녀야 했던 것이, 단 하나의 만능 키카드(IdP 발급 토큰) 로 건물 전체 출입이 가능해지고, 출입 기록이 중앙 관제실(Identity Governance)에 모두 기록되는 시스템으로 진화한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IAM 통합 인증 SSO는 크게 **신원 저장(Identity Store)**, **인증(Authentication)**, **권한(Authorization)**, **프로비저닝(Provisioning)**, **감사(Audit)** 의 5계층으로 구성된다. 핵심 동작은 사용자가 처음 로그인할 때 **신원 확인(AuthN)** 으로 토큰(또는 Assertion)을 발급받고, 이후 다른 서비스 접근 시에는 **재인증 없이** 신뢰할 수 있는 **토큰 재사용(AuthZ delegation)** 으로 권한만 검증하는 방식이다.

```text
[OIDC Authorization Code Flow with PKCE — 표준 SSO 시퀀스]

User          Client App (RP)        IdP (Authorization Server)        Resource Server
 |                |                          |                              |
 | ① 로그인요청   |                          |                              |
 +---------------►|                          |                              |
 |                | ② /authorize (scope,    |                              |
 |                |   code_challenge)        |                              |
 |                +-------------------------►|                              |
 |                |                          | ③ 인증 (MFA/WebAuthn)         |
 |                |                          |◄---- 사용자 인증 -------+     |
 |                | ④ Authorization Code     |                           |     |
 |                |◄-------------------------+                           |     |
 |                | ⑤ /token (code+verifier) |                              |
 |                +-------------------------►|                              |
 |                |                          | ⑥ Access Token(JWT) +       |
 |                |  {sub, aud, iss, exp,    |     Refresh Token 발급       |
 |                |   iat, scope, amr, acr}  |                              |
 |                |◄-------------------------+                              |
 |                | ⑦ Bearer <access_token>  |                              |
 |                +---------------------------------------------------------►|
 |                |                          |                              |
 |                |                          | ⑧ JWT 검증 (서명, 만료,     |
 |                |                          |    audience, claims)         |
 |                |                          |◄-----------------------------+
 |                |                          | ⑨ Protected Resource 응답    |
 |                |◄---------------------------------------------------------+
 | ⑩ 데이터 표시 |                          |                              |
 |◄---------------+                          |                              |
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Identity Store (저장소)** | 신원·속성·자격의 영속 보관 | LDAP(RFC 4511) 디렉터리, 관계형 DB, Microsoft AD(Windows 인증 통합), Azure Entra ID(Graph API), Okta Universal Directory |
| **IdP (Identity Provider)** | 인증 수행 및 토큰/Assertion 발급 | SAML 2.0(Assertion XML), OIDC(ID Token + Access Token JWT), Kerberos(KDC가 TGT/ST 발급), FIDO2(WebAuthn 디지털 서명) |
| **SP / RP (Relying Party)** | 사용자 신원 신뢰 후 서비스 제공 | SAML SP(AcsUrl, Signed Assertion 검증), OIDC Client(JWKS로 IdP 공개키 검증, RS256/ES256 서명 알고리즘) |
| **Token / Assertion** | 신원·권한·세션 정보를 담은 검증 가능한 객체 | SAML Assertion(XML, XMLDSig/EncryptedAssertion), JWT(Header.Payload.Signature, JWE로 암호화 가능), Kerberos Ticket(TGS, PAC 구조체) |
| **Provisioning Engine** | 사용자/권한의 생성·수정·삭제 자동화 | SCIM 2.0(RFC 7644) REST API, Just-In-Time(JIT) Provisioning, HR-Driven(Workday/SAP SuccessFactors 동기화), Deprovisioning Hook |
| **MFA / Risk Engine** | 추가 인증 요소 및 위험 기반 적응형 인증 | TOTP(RFC 6238), WebAuthn(FIDO2, CTAP2.1), Push(Okta Verify/Duo), Adaptive(Risk Score > 0.7 시 Step-up), Risk Signal(IP/디바이스 핑거프린트) |
| **Audit / SIEM** | 인증/인가 이벤트 통합 로깅 및 분석 | syslog/CEF, Splunk/Elastic, 인증 로그 보존(ISMS-P 1년, PCI-DSS 1년), UEBA(User Entity Behavior Analytics) |

**JWT 상세 구조 (OIDC ID Token 예시)**:
```
Header  : { "alg": "RS256", "typ": "JWT", "kid": "Gaidop..." }
Payload : { "iss": "https://idp.example.com",
            "sub": "user-uuid-1234",
            "aud": "client-id-abc",
            "exp": 1717660800,    <- 1시간 후 만료
            "iat": 1717657200,
            "nonce": "abc-123",   <- replay 방지
            "amr": ["pwd","mfa"], <- 인증 방법
            "acr": "urn:mace:incommon:iap:silver" }
Signature: RSA-SHA256(base64url(header) + "." + base64url(payload), IdP_private_key)
```

**핵심 설계 파라미터**:

| 파라미터 | 권장 값 | 근거 |
| :--- | :--- | :--- |
| Access Token TTL | 5~15분 | 탈취 시 피해 최소화 (RFC 6749 권장 1시간 이하) |
| Refresh Token TTL | 8~24시간 (앱) / 30일 (모바일, Rotation) | UX vs 보안 균형 |
| SAML Assertion 유효시간 | 2~5분 | Replay Attack 방지 (SAML 2.0 Profiles §4.1.4.5) |
| MFA Step-up 임계값 | Risk Score ≥ 70 / 24시간 무활동 | NIST SP 800-63B AAL2/AAL3 |
| Cookie `SameSite` | `Strict` (1st party) / `Lax` (cross-site redirect) | CSRF 방어 |
| `Secure`, `HttpOnly` | 필수 | XSS 토큰 탈취 방지 |
| 토큰 서명 알고리즘 | `RS256`/`ES256` 이상 (HS256은 비권장) | 대칭키 유출 방지 |
| 세션 동시성 | 동시 1~2 디바이스 | 세션 하이재킹 탐지 |

- **📢 섹션 요약 비유**: **공항 출국장**에 비유할 수 있다. 여권(Identity)은 한 번만 검사(IdP 인증)받고, 이후 탑승 게이트마다 **탑승권(Token)** 만 보여주며, 위험물 탐지(MFA/Risk Engine) 가 추가 수색를 결정한다. 탑승권에는 좌석·목적지·유효시간(Claims/TTL) 이 인쇄되어 있어 위조가 어렵다(서명 검증).

---

## Ⅲ. 비교 및 연결

| 구분 | **SAML 2.0** | **OIDC (OAuth 2.0 기반)** | **Kerberos** | **FIDO2 / Passkey** |
| :--- | :--- | :--- | :--- | :--- |
| **데이터 형식** | XML (Assertion) | JSON / JWT | Binary Ticket (ASN.1) | CBOR / Public Key |
| **전송 프로토콜** | HTTP Redirect/POST (Browser) | HTTP REST + JSON | UDP 88 (KDC), TCP 88 | CTAP2 over USB/NFC/BLE |
| **주 용도** | B2E 엔터프라이즈 SaaS, 정부 | 모바일/SPA/API, B2C, 모던 클라우드 | 사내 AD 환경, Windows 통합 | Passwordless, Phishing-resistant MFA |
| **서명 알고리즘** | XMLDSig (RSA, ECDSA) | JWS (RS256/ES256/EdDSA) | AES-256 (Ticket 암호화) | ECDSA P-256 (디바이스 개인키) |
| **토큰 유효시간** | Assertion 2~5분 (NotOnOrAfter) | Access 5~15분, Refresh 8~24h | TGT 10h, ST 4~8h | Session 의존, 디바이스 바인딩 |
| **장점** | 검증된 표준(2005), 풍부한 Attribute | REST/JSON 친화, 모던 SPA 적합 | 단방향/상호 인증, 투명 SSO | 피싱 내성(Origin-bound), 패스워드 제거 |
| **단점** | XML 파서 취약점, 모바일 불편 | 토큰 저장·갱신 복잡, IdP 과부하 | 도메인 신뢰 한계, KDC SPOF | 디바이스 분실 시 Recovery 필요 |
| **적합 조직** | 금융·공공·대기업 레거시 | 스타트업·모바일 1st | Windows Active Directory | Zero Trust, B2C 확장 |

**다른 시스템과의 연결 관계**:

- **API Gateway / Zero Trust Network Access (ZTNA)**: Zscaler ZIA/ZPA, Cloudflare Access가 JWT/Header 검증을 통해 사용자 신원을 경계에서 강제.
- **PAM (Privileged Access Management)**: CyberArk, BeyondTrust가 IdP 인증을 받아 Admin 계정 자격증명 Vault 임시 발급(Just-in-Time Elevation).
- **HR 시스템**: Workday, SAP HR -> SCIM 2.0 -> IdP로 사용자 라이프사이클(Join/Move/Leave) 자동 동기화.
- **DevOps / IaC**: SPIFFE/SPIRE로 워크로드 아이덴티티(SVID) 발급, IAM과 Workload Identity 통합.
- **감사/컴플라이언스**: ISMS-P, ISO 27001, PCI-DSS 8장(식별·인증), GDPR Article 32(보안 처리) 충족을 위한 인증 로그/세션 정책.

| 통합 패턴 | 대표 사례 | 적용 시 고려사항 |
| :--- | :--- | :--- |
| **HR-Driven Provisioning** | Workday -> SCIM -> Okta -> 200개 SaaS | 동시성 이슈(Source of Truth 단일화) |
| **Federation (Cross-Org)** | A회사 직원 -> B회사 IdP에 인증 위임 | 신뢰 메타데이터 교환, AssertionConsumerService URL 화이트리스트 |
| **Conditional Access** | Entra ID Conditional Access (위치/디바이스/위험 기반) | 토큰 클레임(groups, roles) 에 정책 매핑 |
| **Just-In-Time Access** | JIT Elevation (CyberArk, AWS IAM Identity Center) | TTL 짧게, 자동 회수, 감사 이벤트
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 376 / 800

<- **이전**: [375. 접근 제어 모델 MAC DAC RBAC ABAC](/knowledge-base/studynote/12_it_management/05_security_compliance/375_access_control_model_mac_dac_rbac_abac/)
**다음**: [377. 다중 인증 MFA 생체 인증 패스키](/knowledge-base/studynote/12_it_management/05_security_compliance/377_multi_factor_authentication_mfa_biometric/) ->

---
