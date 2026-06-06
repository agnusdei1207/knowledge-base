---
title: "Digital Signature Non-repudiation Integrity"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디지털 서명은 비대칭키 암호화(RSA, ECDSA, EdDSA)와 일방향 해시 함수(SHA-256/512, SHA-3)의 결합으로, 서명자의 **개인키(Private Key)**로 메시지 다이제스트를 암호화하여 *부인방지(Non-repudiation)*와 *무결성(Integrity)*을 동시에 보장하는 암호학적 원리이다.
> 2. **가치**: 전자문서의 법적 효력(전자서명법 제3조 공인전자서명)과 감사 추적성(Audit Trail)을 확보하여, paper-based 계약 대비 처리 시간을 90% 이상 단축하고 위·변조 탐지율을 100%에 가깝게 달성하며, 장기 보존 시에도 PAdES/XAdES LTV(Long-Term Validation) 프로파일을 통해 수십 년간 검증 가능성을 유지한다.
> 3. **판단 포인트**: RSA-2048 vs ECDSA-P256 vs EdDSA-Ed25519의 알고리즘 선택, 인증서 신뢰 모델(X.509 단일 vs 매트릭 인증 vs DID/블록체인), 키 보관 방식(Software Token vs HSM vs Cloud KMS), 그리고 양자내성암호(PQC: CRYSTALS-Dilithium, FALCON)로의 전환 시점과 마이그레이션 전략이 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

전자문서时代的 도래와 COVID-19 이후 비대면 거래의 폭발적 증가(연간 약 35% 성장)로 인해 종이 기반 서명·인감 시스템의 한계가 명확해졌다. 종이 계약서의 경우 (1) 물리적 훼손·분실 위험, (2) 위·변조 가능성(형광등, 화학약품 등을 이용한 변조), (3) 사후 증명 곤란(법원 소송 시 감정 필요, 평균 6개월 이상 소요), (4) 당사자가 "내가 서명하지 않았다"고 주장하는 *부인(Repudiation)* 문제 등 구조적 취약점을 내포한다. 디지털 서명은 이러한 문제를 **수학적 불가능성**으로 해결한다.

```text
+----------------------------------------------------------------------------+
|                  종이 서명 vs 디지털 서명 패러다임 비교                     |
+----------------------------------------------------------------------------+
|                                                                            |
|   [기존] 종이 문서 + 인감/자필 서명                  [신] 전자문서 + 디지털 서명|
|   +----------------------+                          +----------------------+|
|   | • 물리적 매체 의존    |                          | • 논리적 비트열       ||
|   | • 감정(鑑定) 의존     |                          | • 수학적 검증(공개키) ||
|   | • 당사자 진술 중요    |    ---> 진화 --->          | • 서명·검증 알고리즘  ||
|   | • 복제·변조 용이      |                          | • 해시 함수로 위변조  ||
|   | • 보존 비용 ^(창고)   |                          |   탐지, 부인방지     ||
|   +----------------------+                          +----------------------+|
|                                                                            |
|   법적 근거:           전자서명법(2024 개정), 전자문서법,                   |
|                        eIDAS Regulation (EU 910/2014),                     |
|                        U.S. ESIGN Act(2000), UNCITRAL Model Law            |
+----------------------------------------------------------------------------+
```

전자서명법 제3조는 "공인전자서명은 서명자의 서명意思(고의)와 그 서명을 타인이 확인할 수 있도록 하는 전자적 형태의 정보"로 정의하며, 공인인증기관(CA) 발급 인증서 기반 서명 시 **추정력**(작성자의 진정한 의사표시로 추정)을 부여한다. 하지만 2020년 12월 「전자서명법」 개정으로 공인인증서 의무사용이 폐지되어, **다양한 수단**(공동인증서, 간편인증, 민간인증, DID, 블록체인 기반 서명)이 인정되는 체계로 전환되었다.

**왜 디지털 서명이 필수적인가?**
- **무결성(Integrity)**: SHA-256 해시 충돌 확률 2⁻¹²⁸로 사실상 0에 수렴. NIST SP 800-107에 따라 1비트 변조 시 해시값이 약 50% 확률로 변화(애벌런치 효과).
- **인증(Authentication)**: 공개키 인증서(X.509 v3)가 신원(Subject DN + SAN)과 공개키를 CA의 전자서명으로 결합.
- **부인방지(Non-repudiation)**: 개인키의 유일성(개인키는 단독 소유자가 보관)을 전제로, Origin, Receipt, Submission, Transport 등 다양한 형태의 부인방지 서비스를 제공.
- **기밀성(Confidentiality)**: 디지털 서명 자체는 기밀성을 제공하지 않으므로, 별도로 AES-256-GCM 등 대칭키 암호화 또는 봉투암호화(Envelope Encryption) 적용 필요.

- **📢 섹션 요약 비유**: 종이 계약서에 인감을 찍으면 "도장이 누구 것인지" 감정해야 하지만, 디지털 서명은 도장 자체가 **수학적으로 위조 불가능한 양자역학적 도장**인 셈이다. 위조하려고 시도하면 우주가 무너질 확률(2⁻²⁵⁶)만큼 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

디지털 서명의 핵심 알고리즘은 크게 두 단계로 구성된다: (1) 가변 길이 메시지 M을 고정 길이 다이제스트 h = Hash(M)로 압축, (2) 다이제스트에 서명 알고리즘 Sign(PrivateKey, h) 적용하여 서명값 σ 생성. 검증은 Verify(PublicKey, M, σ)로 수행한다.

```text
+-----------------------------------------------------------------------------+
|           디지털 서명 생성·검증 프로토콜 상세 아키텍처                       |
+-----------------------------------------------------------------------------+
|                                                                            |
|  [서명자(Alice)]                                    [검증자(Bob)/제3자]      |
|  +--------------+                                  +--------------+        |
|  | 원본 메시지 M |                                  | 수신 메시지 M'|        |
|  | (계약서 PDF)  |                                  | + 서명값 σ    |        |
|  +------+-------+                                  +------+-------+        |
|         |                                                 |                |
|         v                                                 v                |
|  +--------------+                                  +--------------+        |
|  | Hash Function |                                  | Hash Function |        |
|  | SHA-256/512  |                                  | SHA-256/512  |        |
|  | SHA3-256     |                                  | SHA3-256     |        |
|  | (FIPS 180-4) |                                  | (FIPS 180-4) |        |
|  +------+-------+                                  +------+-------+        |
|         | h = H(M)                                         | h' = H(M')     |
|         |                                                 |                |
|         v                                                 v                |
|  +--------------+    공개키(PKI/CA)                +--------------+        |
|  | Sign Algorithm| ◄--- 인증서 검증 ------------►   | Verify Algo. |        |
|  | (개인키 sk)   |    X.509 v3 + CRL/OCSP          | (공개키 pk)  |        |
|  +------+-------+    또는 RFC 3161 TSA            +------+-------+        |
|         | σ = Sign(sk, h)                                | Accept/Reject  |
|         |                                                 |                |
|  -------+-------- M, σ 전송 (HTTPS/TLS) ------------------+                |
|         |                                                 |                |
|         |              [장기 검증 보강 옵션]               |                |
|         |              +------------------+                |                |
|         +-------------►| TSA(시각 인증)   |----------------+                |
|                        | + Revocation Info|  RFC 5280, RFC 5816             |
|                        | + Cert. History   |  ETSI PAdES/AdES               |
|                        +------------------+                                 |
+-----------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **해시 함수 (Hash Function)** | 메시지 고정 길지 다이제스트 생성, 압축·애벌런치·충돌저항성 보장 | SHA-256(32B), SHA-384, SHA-512(64B), SHA3-256/512(Keccak sponge), SM3(중국 표준, 한국 KCMVP 미승인). FIPS 180-4 기반, MD5/SHA-1은 2017년 Google SHAttered 공격으로 충돌 발견되어 **사용 금지**. |
| **서명 알고리즘 (Signature Scheme)** | 개인키 sk로 다이제스트 h에 대한 서명값 σ 산출 | **RSA-PSS**(PKCS#1 v2.2, RSASSA-PSS with MGF1, 2048~4096bit), **ECDSA**(FIPS 186-4, NIST P-256/P-384/P-521/secp256k1), **EdDSA**(Ed25519: 128bit, Ed448: 224bit 보안강도, RFC 8032), **SM2**(중국 표준), **KCDSA/ECDSA**(한국 KCMVP 검증). |
| **공개키 인증서 (X.509 v3)** | 서명자 신원(SUBJECT, SAN) ↔ 공개키(pk) 바인딩, CA 전자서명으로 신뢰 연결 | RFC 5280 프로파일, 확장 필드(KeyUsage: digitalSignature/nonRepudiation, ExtendedKeyUsage: clientAuth/codeSigning, SAN, AIA, CRL Distribution Points). OCSP stapling(RFC 6961) 및 OCSP Multi-stapling 적용. |
| **PKI 신뢰 계층 (CA Hierarchy)** | Root CA -> Intermediate CA -> End Entity 인증서 체인 구성, OCSP/CRL로 폐기 정보 제공 | 신뢰 앵커(Trust Anchor)는 OS/브라우저 Trust Store에 사전 설치(Mozilla NSS, Microsoft Root, Apple, Android CA Store). RFC 3647 CP/CPS, WebTrust/ETSI EN 319 411-1~3 감사 기준. |
| **시각 인증 (TSA, RFC 3161)** | 서명 시점의 공증, 인증서 만료·폐지 후에도 검증 가능성 보존 | TSU(Time Stamping Unit)로부터 `TimeStampToken` 발급, 서명값에 timestampToken 임베드. 한국 KISA 공인 TSA, Digicert, GlobalSign 등. |
| **장기 검증 (LTV: Long-Term Validation)** | 인증서·서명 알고리즘의 장기 보존·재검증 | ETSI EN 319 142 (PAdES), 319 132 (XAdES), 319 122 (CAdES). T, LT, LTA 등 4단계 베이스라인(T/B/T-LT/T-LTA). |
| **키 저장소 (Key Store)** | 개인키의 안전한 생성·저장·사용 | PKCS#11 토큰, PKCS#12(.pfx), Microsoft CSP/CNG, Apple Keychain, OpenSSL Engine, **HSM**(FIPS 140-2 Level 3/4, e.g., Thales Luna, Utimaco, AWS CloudHSM), **KMS**(AWS KMS, Azure Key Vault, Google Cloud KMS), 스마트카드/보안토큰(YubiKey, PIV, JavaCard). |

### 알고리즘별 핵심 파라미터

**1) RSA-PSS 서명/검증**
- 키 생성: `n = p·q` (p, q는 2048bit 이상 소수), e=65537 고정
- 서명: `σ = (H(M) || PS || 0xBC || MaskGen1(MGF1, saltLen))^(d) mod n`
- 보안강도: RSA-2048 ≒ 112bit, RSA-3072 ≒ 128bit, RSA-7680 ≒ 192bit (NIST SP 800-57 Part 1 Rev. 5)

**2) ECDSA (FIPS 186-4)**
- 곡선: NIST P-256/384/521, Brainpool, secp256k1
- 서명: `k ∈ ℤ_n*`(임의), `r = (k·G).x mod n`, `s = k⁻¹(z + r·d) mod n`
- 보안강도: P-256 ≒ 128bit, P-384 ≒ 192bit, P-521 ≒ 256bit
- ⚠️ **주의**: 임의 k 생성 실패 시(예: Sony PS3 ECDSA) 개인키 노출 -> RFC 6979 결정적 nonce(k) 생성, EdDSA는 본질적으로 결정적

**3) EdDSA Ed25519 (RFC 8032)**
- 곡선: Edwards25519 (Curve25519의 Edwards form)
- 서명: 64byte 고정 출력, 약 50,000 sign/sec, 25,000 verify/sec (상용 HSM 기준)
- 보안강도: ~128bit, 슬라이딩 공격·타이밍 공격·부채널 공격 면역

**4) 양자내성 서명 (PQC: NIST FIPS 203/204/205)**
- **CRYSTALS-Dilithium** (ML-DSA, FIPS 204): 격자(LWE/Module-LWE) 기반, 공개키 ~1,312B, 서명 ~2,420B
- **FALCON** (FN-DSA, FIPS 206 예정): NTRU 격자 + FFT, 더 작은 서명(~666B) but 구현 복잡
- **SPHINCS+** (SLH-DSA, FIPS 205): 해시 기반, 서명 크기 7~50KB, 보수적 대안

- **📢 섹션 요약 비유**: 디지털 서명은 **"봉인된 유리병에 편지를 넣는 행위"**와 같다. 메시지(편지)는 해시(유리병)로 압축되고, 개인키(도장)는 병의 입구에 각인된다. 누구나(공개키로) 병이 깨졌는지, 누가 도장 찍었는지 검증할 수 있지만, 도장을 만들어내려면(개인키 위조) 우주의 모든 원자를 뒤져야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | 전자서명 (Electronic Signature) | 디지털 서명 (Digital Signature) | 종이서명 + 인감 |
| :--- | :--- | :--- | :--- |
| **정의/범위** | 전자적 형태의 서명 정보 총칭(포괄). 클릭, 생체, 아이핀 등 포함 | 암호학적 알고리즘(공개키)으로 생성된 **수학적 서명** | 물리적 종이 + 인장/자필 |
| **법적 효력 (한국)** | 전자서명법 §3 — "전자적 형태 정보" 일반 | 공인전자서명 = 추정력 인정(§3②) | 증거능력 강함(형사·민사) |
| **기반 기술** | 다양(생체, 패스워드, OTP, 그래픽 등) | RSA/ECDSA/EdDSA + 해시함수 | 물리적 매체 + 인감도장 |
| **위·변조 탐지** | 방식에 따라 다름(시각적 비교) | **수학적 100% 탐지**(해시 불일치 시 검증 실패) | 물리적 감
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 380 / 800

<- **이전**: [379. PKI 공개키 인프라 인증서 관리](/studynote/12_it_management/05_security_compliance/379_pki_public_key_infrastructure_certificate/)
**다음**: [381. 침입 탐지 IDS 침입 방지 IPS 비교](/studynote/12_it_management/05_security_compliance/381_intrusion_detection_ids_prevention_ips/) ->

---
