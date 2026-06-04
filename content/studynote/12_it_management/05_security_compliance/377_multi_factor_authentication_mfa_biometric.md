+++
title = "377. 다중 인증 MFA 생체 인증 패스키 (Multi-Factor Authentication MFA Biometric)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사용자가 보유한 단말기의 **TPM/SE(Secure Enclave)** 내부에서 **ECDSA P-256 / Ed25519** 기반 공개키 쌍을 생성·저장하고, **FIDO2(WebAuthn + CTAP2)** 프로토콜로 챌린지-서명 방식의 **Passwordless 인증**을 수행하는 비대칭키 기반 신원확인 체계
> 2. **가치**: 피싱·크리덴셜 스터핑 공격 표면을 제거하고(피싱 저항성 99.9% 이상, Microsoft/Google 실증), UX 측면에서 비밀번호 재설정 비용을 평균 **$70/건 -> 0원** 수준으로 절감하며 평균 로그인 소요시간 30초 -> 3초 단축
> 3. **판단 포인트**: **Device-bound Passkey(사내 단말 종속)** vs **Synced Passkey(클라우드 동기화)** 정책 결정, 생체정보 **TEE/SE 내부 매칭 후 T/F 반환** vs 서버 매칭 방식의 프라이버시 트레이드오프, **Fallback Recovery** 채널의 설계가 핵심 의사결정 사항

---

## Ⅰ. 개요 및 필요성

전통적 ID/Password 방식은 NIST SP 800-63B 기준 "Knowledge Factor" 단독으로는 **Entropy 한계(8자리 영숫자 약 30bit)**, **리사용(Reuse)**, **피싱(Phishing)**의 3대 결함을 구조적으로 해결할 수 없다. Verizon DBIR 2024에 따르면 브루트포스·크리덴셜 스터핑이 전체 침해사고의 **약 36%**를 차지하며, MFA 우회 공격(SMS SIM Swapping, Push Fatigue, AiTM Adversary-in-The-Middle) 또한 2023년 대비 **156%** 증가했다.

이에 대한 해답으로 등장한 것이 **FIDO Alliance**의 **FIDO2** 표준이며, Apple·Google·Microsoft 3사가 2022년 5월 공통 지원 합의 후, 2023년 WWDC/Google I/O에서 **Passkey** 브랜드로 통합 명명되었다. Passkey는 **Passwordless FIDO Authentication**의 사용자 경험(UX) 최적화 버전으로, 사용자 기기에 저장된 크리덴셜이 **클라우드 동기화(Synced)** 되어 다중 디바이스·크로스 플랫폼 로그인을 가능케 한다.

```text
[ 패스워드 기반 인증의 문제점 ]

   사용자 --(ID/PW 평문 입력)---> [ 피싱 사이트 / 키로거 / DB 유출 ]
                                       |
                                       v
                                ① Reuse 공격     (동일 PW 다계정 시도)
                                ② Credential     (유출 DB 매칭 로그인)
                                   Stuffing
                                ③ Phishing        (가짜 도메인 입력 유도)
                                ④ Brute-force     (오프라인 해시 크래킹)
                                       |
                                       v
                              평균 침해 MTTC : 277일
                              Reset 비용      : $70/건
                              Helpdesk 부하   : 전체 티켓 30~50%

[ MFA / Passkey 패러다임 전환 ]

   +----------------------------------------------------------+
   |  Knowledge  (PW)  --->  ✕ 제거  (Passwordless)            |
   |  Possession (단말) --->  ◯ 단말 내 비공개키 서명           |
   |  Inherence  (생체) --->  ◯ TEE/SE 내부 1:1 매칭(T/F)      |
   +----------------------------------------------------------+
                              |
                              v
                  Origin-bound + Phishing-resistant
                  (도메인 종속 + 피싱 저항)
```

**기존 패러다임 -> 신규 패러다임 비교**

- **기존**: "사용자가 기억하는 것(비밀번호)"을 매번 평문 전송 -> 서버에서 해시 비교 -> 단방향 취약점 다수
- **신규**: "사용자가 가진 단말이 비공개키로 서명한 서명값"을 전송 -> 서버는 등록된 공개키로 검증 -> 도메인(Origin) 종속, 재전송 불가, 피싱 사이트에서 도용 불가

- **📢 섹션 요약 비유**: 기존 자물쇠가 "비밀번호"라는 깃털 열쇠 한 자루였다면, FIDO2는 **"현관문 DNA 인식 + 도어락이 1회용 암호문 생성"**이 결합된 차세대 잠금장치라 할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. FIDO2 3-Layer 아키텍처

FIDO2는 **W3C WebAuthn**(웹 API) + **FIDO CTAP2**(클라이언트↔인증기 간) 두 표준의 합으로, **3계층** 구조를 가진다.

```text
[ FIDO2 / WebAuthn 등록(Registration) 프로토콜 ]

   +--------+         +--------------+         +------------------+
   | Browser|         |   Web Server |         | Authenticator    |
   | (Relying|         |  (RP Server) |         | (TPM/SE/보안키)   |
   |  Party)|         |              |         |                  |
   +---+----+         +------+-------+         +--------+---------+
       |  ① navigator.       |                          |
       |  credentials.       |                          |
       |  create()           |                          |
       | ------------------>  |                          |
       |                     |  ② challenge             |
       |                     |  (32B random nonce)      |
       | <------------------- |                          |
       |  ③ challenge 전달    |                          |
       | ----------------------------------------------->|
       |                     |                          |
       |                     |  ④ User Verification     |
       |                     |     (생체/PIN/Touch)     |
       |                     |                          |
       |                     |  ⑤ KeyPair 생성           |
       |                     |     (ECDSA P-256 /       |
       |                     |      Ed25519 / RSA-PSS)  |
       |                     |                          |
       |                     |  ⑥ attestation Object    |
       |  <--------------------------------------------- |
       |  { id, rawId,      |                          |
       |    response:{       |                          |
       |     attestationObject,                          |
       |     clientDataJSON } }                         |
       |  ⑦ RP 서버로 전송   |                          |
       | ------------------>  |                          |
       |                     |  ⑧ 공개키 + CredentialID |
       |                     |     DB 저장 (회원가입)   |
       +---------------------+--------------------------+
```

### 2. 인증(Assertion) 프로토콜

```text
[ FIDO2 / WebAuthn 인증(Login) 프로토콜 ]

   Client(UA)                RP Server              Authenticator
       |                         |                        |
       |  ① login()              |                        |
       | -----------------------> |                        |
       |                         |  ② challenge(Nonce)    |
       | <----------------------- |                        |
       |  ③ challenge 전달        |                        |
       | ------------------------------------------------>|
       |                         |                        |
       |                         |  ④ User Verify         |
       |                         |     (생체 매칭)         |
       |                         |                        |
       |                         |  ⑤ assertion           |
       |                         |     { signature,       |
       |                         |       authenticatorData,|
       |                         |        counter++ }     |
       | <------------------------------------------------|
       |  ⑥ assertion 전송       |                        |
       | -----------------------> |                        |
       |                         |  ⑦ 공개키로 서명검증    |
       |                         |     + counter 증가 확인 |
       |                         |     + origin 검증       |
       |                         |                        |
       |  ⑧ Session 발급         |                        |
       | <----------------------- |                        |
       +-------------------------+------------------------+

   * Signature 검증 식 (ECDSA):
     verify( Puk, SHA256(authData || clientDataHash) ) = true
   * counter: Replay 방지용 단조증가 카운터
```

### 3. 핵심 데이터 구조 (CBOR 인코딩)

```text
authenticatorData (최소 37B):
+-----------------------------------------------------+
|  rpIdHash (32B)        : SHA256("login.example.com") |
|  flags (1B)            : UP|UV|AT|ED|TFLAGS         |
|  signCount (4B)        : 0x0000000A (10회)          |
|  attestedCredentialData: {aaguid(16), credLen(2),  |
|                           credId, publicKey}        |
|  extensions (optional) : hmac-secret, credProps     |
+-----------------------------------------------------+

clientDataJSON:
  {"type":"webauthn.create",
   "challenge":"<base64url(32B)>",
   "origin":"https://login.example.com",
   "crossOrigin":false}

publicKey (COSE_Key):
  kty: 2 (EC2) / 1 (OKP)
  alg: -7 (ES256) / -8 (EdDSA)
  crv: 1 (P-256) / 6 (Ed25519)
  x, y: 공개키 좌표
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Relying Party (RP)** | 신원 검증 의존자, 웹/앱 서버 | Challenge 생성, CredentialID·공개키 DB 저장, Origin(=도메인) 검증 |
| **User Agent (UA)** | 브라우저/앱 (Chrome, Safari, Edge) | WebAuthn JS API 호출, clientDataJSON 생성, Origin 바인딩 |
| **Authenticator** | 키 보관·생체 처리 모듈 (TPM 2.0, Apple SE, Android StrongBox) | ECDSA P-256/Ed25519 키쌍 생성, 생체 매칭 후 Release Flag 설정, 서명 연산 |
| **Attestation CA** | 인증기 신뢰 체인 (예: Yubico, Apple, Google Root) | 인증기 모델·배치 증명, MDS(FIDO Metadata Service) v3.0 |
| **CA / Token Service** | OATH 토큰, SAML/OIDC IdP 연동 | TOTP RFC 6238(30초/8자리), HOTP RFC 4226, FIDO2를 OIDC `acr=phr` |

### 4. 생체 인증 정확도 지표

| 지표 | 정의 | 권장 임계값 (NIST SP 800-63B) |
| :--- | :--- | :--- |
| **FAR** (False Acceptance Rate) | 타인이 오인수락될 확률 | ≤ 1/10,000 (일반), 1/100,000 (고보안) |
| **FRR** (False Rejection Rate) | 정당한 본인 거부 확률 | ≤ 5% |
| **EER** (Equal Error Rate) | FAR = FRR 교차점 | 낮을수록 우수 |
| **CER** (Capture Rate) | 재현 공격 통과율 | ≤ 0.5% |
| **Liveness Detection** | 사진/영상/마스크 위조 차단 | ISO/IEC 30107-1 PAD(Presentation Attack Detection) |

### 5. Passkey 동기화 메커니즘

```text
[ Synced Passkey : E2EE 동기화 구조 ]

   +----------+    +----------+    +----------+
   |iPhone(A) |    | iPad (B) |    | Mac (C)  |
   |  SE encl.|    |  SE encl.|    |  SE encl.|
   +----+-----+    +----+-----+    +----+-----+
        |  Hardware-Backed Key(HBK)  |
        |  (device의 개인키로 wrap)  |
        +----------+------------------+
                   v
        +----------------------+
        | iCloud Keychain (E2EE) |  <- Apple은 HKDF+HPKE로
        |  또는 Google PMS     |     Apple/Google조차 복호화 불가
        |  또는 MS Account     |
        +----------+-----------+
                   v
        +----------------------+
        | 다른 디바이스로 sync  |
        |  (브랜드 생태계 한정)  |
        +----------------------+

   * Apple/Google 모두 E2EE(End-to-End Encryption) 적용
   * 단말 분실 시 icloud/family recovery 또는 신뢰 디바이스 quorum
   * Cross-ecosystem QR+CDA(Cross-Device Authentication) 흐름 제공
```

- **📢 섹션 요약 비유**: FIDO2 등록은 **"현관에 맞는 *고유* 도장(공개키)을 찍어두는 것"**, 인증은 **"그 도장이 도어록 안에서만 찍혀지는지 확인하는 것"**, 그리고 Passkey 동기화는 **"도장 자체는 두고, *사용 권한 정보*만 금고에 분산 보관"**하는 구조다.

---

## Ⅲ. 비교 및 연결

### 1. 인증 수단별 비교

| 구분 | Password | SMS OTP | TOTP (Google Auth) | FIDO2 보안키 | Passkey (생체) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Factor 종류** | Knowledge | Possession | Possession | Possession+Inherence | Inherence(+Possession) |
| **피싱 저항성** | ✕ 매우 낮음 | △ 낮음(SIM Swap) | △ 중간(AiTM 우회) | ◯ 높음(Origin 바인딩) | ◯ 매우 높음 |
| **UX(로그인)** | 30초+ | 15초 | 12초 | 5초 | 3초 |
| **Reusable Secret** | ◯(PW) | ✕ | ✕ | ✕(서명 매번 다름) | ✕ |
| **서버 침해 영향** | 치명적 | 보통 | 보통 | 무 영향 | 무 영향 |
| **단말 분실 시** | - | 재발급 | 재등록 | 대체 키 필요 | 동기화/복구 |
| **비용** | $0 | $0.05/건 | $0 | $25~70/키 | $0 (단말 내장) |
| **사용 사례** | 레거시 | 2FA | 2FA | 고보안/사내 | B2C/B2E 로그인 |

### 2. Passkey 유형 비교

| 구분 | Device-bound Passkey | Synced Passkey |
| :--- | :--- | :--- |
| **저장 위치** | 단일 디바이스 TPM/SE | 클라우드 E2EE 동기화 |
| **이식성** | ✕ 없음 (단말 종속) | ◯ 동일 생태계 내 |
| **단말 분실** | 즉시 잠금, 재등록 | 복구 메커니즘 |
| **적합 환경** | BYOD 통제 사내, PCI-DSS | 일반 사용자 B2C |
| **정책 예** | Windows Hello for Business (Cloud Trust) | Apple ID, Google Account |
| **회수 가능성** | 관리자 통제 가능 | 사용자/생체 의존 |

### 3. WebAuthn Attestation 종류

| Type | 내용 | 활용 |
| :--- | :--- | :--- |
| **None
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 377 / 800

<- **이전**: [376. 신원 관리 IAM 통합 인증 SSO](/knowledge-base/studynote/12_it_management/05_security_compliance/376_identity_management_iam_sso_integration/)
**다음**: [378. 암호화 기술 대칭 비대칭 하이브리드](/knowledge-base/studynote/12_it_management/05_security_compliance/378_encryption_symmetric_asymmetric_hybrid/) ->

---
