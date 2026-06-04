---
title: "378. 암호화 기술 대칭 비대칭 하이브리드 (Encryption Symmetric Asymmetric Hybrid)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 대칭키 암호(AES-256, ChaCha20, SEED)는 동일한 비밀키로 암복호화하여 처리속도 100~1000배 우위이나 키 분배 문제(Knapsack Problem)를 가지며, 비대칭키 암호(RSA-2048, ECC-P256)는 수학적 일방향 함수(소인수분해, 이산대수) 기반 공개키 교환으로 키 분배는 해결하나 연산 비용이 높음. 하이브리드 암호는 **공개키로 세션키를 안전하게 캡슐화(Key Encapsulation Mechanism, KEM)하고, 대칭키로 실제 데이터(평문)를 암호화(Data Encapsulation Mechanism, DEM)**하는 두 계층 구조의 합성 암호체계.
> 2. **가치**: TLS 1.3 핸드셰이크 기준으로 측정 시 하이브리드 방식은 1-RTT(Zero-RTT 옵션) 내 RSA-PSS 또는 X25519 ECDHE로 세션키 협상 후 AES-256-GCM으로 10Gbps 라인레이트 암호화가 가능. NIST SP 800-57 기준 RSA 2048bit는 AES-128bit와 동일 보안강도(112-bit), RSA 3072bit는 AES-128bit(128-bit), RSA 15360bit는 AES-256bit(256-bit) 보안강도 매핑.
> 3. **판단 포인트**: 양자컴퓨팅 위협(Shor's Algorithm)으로 RSA/ECC는 공통취약점 보유 -> NIST PQC 표준(CRYSTALS-Kyber, CRYSTALS-Dilithium)을 하이브리드 KEM으로 도입하는 **PQC Migration 전략**이 핵심. 또한 블록암호 운용모드(GCM vs CBC) 선택, 키 생명주기(Lifecycle), HSM/TPM 하드웨어 백업, FIPS 140-2/3 검증 여부가 실무 판단 기준.

---

## Ⅰ. 개요 및 필요성

정보보안의 CIA Triad(Confidentiality, Integrity, Availability) 중 기밀성(Confidentiality)을 보장하는 암호화 기술은 1976년 Diffie-Hellman 논문 "New Directions in Cryptography" 발표 이후 현대 암호학(Modern Cryptography)의 기틀 위에 발전해왔다. 초기 대칭키 암호(DES, 56-bit)는 NIST가 1977년 연방표준(FIPS 46)으로 채택했으나, 1998년 EFF의 Deep Crack이 56시간 만에 키 전수조사(Brute Force)에 성공하면서 1997년 AES 공모가 시작되었고, 2001년 Rijndael 알고리즘이 AES(Advanced Encryption Standard, FIPS 197)로 최종 선정되었다. 반면 비대칭키 암호는 1976년 DH(Diffie-Hellman) 키 교환, 1977년 RSA(Rivest-Shamir-Adleman) 알고리즘이 등장하면서 키 분배 문제를 해결했으나, RSA-1024는 2009년 768bit 소인수분해 성공 이후 단계적 폐기, RSA-2048도 양자컴퓨팅의 등장으로 2030년 이후 사용 금지 권고(NIST SP 800-131A)가 이루어지고 있다.

```text
   [ 암호화 기술 진화 흐름도 ]

   1976          1977          2001          2017          2022          2024~
     |            |             |            |             |             |
     v            v             v            v             v             v
  +------+   +------+      +------+    +----------+  +----------+  +----------+
  | DH/  |   | RSA  |      | AES  |    |  PQC     |  | Kyber    |  | PQC      |
  | RSA  |--->| 표준 |------>|Rijn- |---->| 표준화   |-->| FIPS 203 |-->| Hybrid   |
  | 등장 |   | 채택 |      |dael  |    |  시작    |  | 발표     |  | TLS 1.3  |
  +------+   +------+      +------+    +----------+  +----------+  +----------+
     |            |             |            |             |             |
  대칭+비대칭   공개키 기반     블록암호     양자내성      격자기반      양자내성
  패러다임     키분배 해결    표준화       알고리즘     KEM 표준화    하이브리드
                                       (NIST PQC)   (Dilithium)
```

현대 정보시스템이 단일 암호 방식으로 동작하기 어려운 근본적인 이유는 **연산 복잡도와 보안 요구사항의 비대칭성**에 있다. AES-NI(Advanced Encryption Standard New Instructions) 하드웨어 가속 시 AES-256은 약 0.5~1.5 cycles/byte로 처리되어 10Gbps NIC에서 라인레이트 암호화가 가능하지만, RSA-2048 서명 검증 한 건에 약 0.2~2ms(OpenSSL 3.0 기준) 소요되어 HTTP/2의 평균 요청 수명(1~10ms) 대비 과도한 지연을 유발한다. 반대로 ECDH-P256 키 교환은 1ms 내 완료되어 핸드셰이크에 적합하다. 또한 대칭키는 n명 사용자 간 안전한 통신에 n(n-1)/2개의 키가 필요한 O(n²) 문제로, 1000명 조직이면 499,500개 키 관리가 필요한 반면, 비대칭키는 n개 키페어(2n)만으로 n²개의 안전한 채널을 구성할 수 있다.

- **📢 섹션 요약 비유**: 대칭키 암호는 **집 열쇠를 복제본으로 만들어 모든 가족에게 나눠주는 것**(빠르지만 복제·회수 어려움), 비대칭키는 **개인 우편함**처럼 누구나 우편을 넣을 수 있고(공개키) 본인만 우편을 꺼낼 수 있는 것(개인키), 하이브리드는 **택배 상자 안에 작은 금고를 넣어 보내는 것**(금고는 자물쇠로 잠그고, 자물쇠는 우편함 공개키로 봉인).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 대칭키 암호 (Symmetric Key Cryptography)

**블록 암호 (Block Cipher)**: 고정 길이(128-bit) 블록 단위로 평문을 암호화하며, 핵심 구조는 **SPN(Substitution-Permutation Network)** 또는 **Feistel Network**이다. AES는 10/12/14 라운드(AES-128/192/256)동안 SubBytes(S-box 비선형置换), ShiftRows(행 단위 좌순환), MixColumns(열 단위 GF(2⁸) 행렬곱), AddRoundKey(XOR) 4단계를 반복한다. **운용모드(Mode of Operation)**는 NIST SP 800-38A~G에서 정의하며 보안성·성능·기능성에 큰 차이를 보인다.

```text
   [ 하이브리드 암호화 프로토콜 (TLS 1.3 기준) 상세 흐름도 ]

   Client                                          Server
     |                                                |
     |  ① ClientHello                                  |
     |    - 지원 cipher_suites:                        |
     |      TLS_AES_256_GCM_SHA384                    |
     |      TLS_CHACHA20_POLY1305_SHA256              |
     |      TLS_AES_128_GCM_SHA256                    |
     |    - key_share: X25519 PublicKey (32 bytes)     |
     |    - signature_algorithms:                      |
     |      ecdsa_secp256r1_sha256                    |
     |      rsa_pss_rsae_sha256                       |
     | ---------------------------------------------->  |
     |                                                |
     |                          ② ServerHello          |
     |                          - selected: TLS_AES_256_GCM_SHA384
     |                          - key_share: X25519 PubKey |
     |                          ③ EncryptedExtensions  |
     |                          ④ Certificate           |
     |                          ⑤ CertificateVerify     |
     |                          ⑥ Finished (MAC)        |
     | <----------------------------------------------  |
     |                                                |
     |  ⑦ Finished (MAC)                               |
     | ---------------------------------------------->  |
     |                                                |
     |  ------- 양방향 데이터 통신 (AES-256-GCM) ------  |
     |  [HKDF-Expand-Label로 유도된 키]                  |
     |  - client_application_traffic_secret             |
     |  - server_application_traffic_secret             |
     |  - key: 32 bytes | IV: 12 bytes | tag: 16 bytes |
     |                                                |
     |  (c)HKDF-Extract-Then-Expand 구조:               |
     |  IKM = X25519(client_priv, server_pub)          |
     |  PRK = HKDF-Extract(salt, IKM)                  |
     |  AES_KEY = HKDF-Expand(PRK, "key", 32)          |
     |  AES_IV  = HKDF-Expand(PRK, "iv", 12)           |
     |                                                |

   [ KEM-DEM 상세 구조 (RSA-OAEP + AES-GCM 하이브리드) ]

   +----------- KEM (Key Encapsulation Mechanism) -----------+
   |                                                          |
   |  Server -(PKCS#1 v2.2 RSA-OAEP)--> Client                 |
   |                                                          |
   |  ① Client:                                               |
   |     r = random(256-bit)                                  |
   |     shared_secret = r                                    |
   |     encrypted_r = RSA-OAEP-Encrypt(server_pubkey, r)    |
   |     -> Server로 전송                                      |
   |  ② Server:                                               |
   |     r' = RSA-OAEP-Decrypt(server_privkey, encrypted_r)   |
   |     -> 동일 shared_secret 획득                             |
   |  ③ 양측:                                                  |
   |     KEK = HKDF-SHA256(r, "encryption")                   |
   |                                                          |
   +----------- DEM (Data Encapsulation Mechanism) -----------+
   |                                                          |
   |  Client:                                                  |
   |  ④ DEK = CSPRNG(32 bytes)                                |
   |  ⑤ ciphertext = AES-256-GCM-DEK(plaintext, AAD)         |
   |  ⑥ enc_dek = DEK_KEK(DEK)                                |
   |  ⑦ 전송: (enc_dek || ciphertext || auth_tag)             |
   |                                                          |
   |  Server:                                                  |
   |  ⑧ DEK' = DEK_KEK_decrypt(enc_dek)                      |
   |  ⑨ plaintext = AES-256-GCM-DEK'_decrypt(ciphertext)     |
   |  ⑩ GCM Tag 검증 (인증된 복호화, AEAD)                    |
   |                                                          |
   +----------------------------------------------------------+
```

**스트림 암호 (Stream Cipher)**: ChaCha20은 Salsa20을 Daniel J. Bernstein이 2008년 개선한 알고리즘으로, 256-bit 키와 96-bit nonce로부터 512-bit 블록 단위(32개의 32-bit word)로 키스트림을 생성하며, Poly1305 MAC과 결합된 ChaCha20-Poly1305는 TLS 1.3 표준 cipher suite로 채택되었다. 모바일 환경(ARM Cortex-A53 등 AES-NI 미지원)에서 AES-GCM 대비 약 3~5배 빠르다.

**한국 표준 대칭키**: SEED(1999, 128-bit, KISA), ARIA(2004, 128/192/256-bit, NSRI) 모두 3GPP/ISO/IEC 표준이며, SEED는 2024년 현재도 한국 공공기관 망 분리 시스템의 표준으로 사용된다.

### 2. 비대칭키 암호 (Public Key Cryptography)

**RSA 알고리즘**: 1977년 MIT 연구진이 제안한 알고리즘으로, 다음 수학적 난제에 기반한다.
- **키 생성**: 두 소수 p, q 선택 -> n = p·q (모듈러스) -> φ(n) = (p-1)(q-2) -> e·d ≡ 1 (mod φ(n)) (e=65537, 공개지수)
- **암호화**: c = m^e mod n
- **복호화**: m = c^d mod n
- **보안 근거**: n의 소인수분해 어려움(Integer Factorization Problem)

**타원곡선 암호 (ECC)**: 1985년 Koblitz, Miller가 제안, 이산대수 문제의 변형인 ECDLP(Elliptic Curve Discrete Logarithm Problem)에 기반한다. RSA-3072와 동일 보안강도(128-bit)를 ECC-P256(256-bit)으로 달성할 수 있어 **키 사이즈 효율성**이 핵심 강점이다. Curve25519(X25519, Bernstein 2006)는 Montgomery Ladder 알고리즘으로 상수시간(Constant-time) 연산을 보장하여 사이드채널 공격에 강하다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **대칭키 엔진 (Symmetric Engine)** | 대량 평문 데이터 암복호화 | AES-NI 하드웨어 명령어 (AESENC, AESENCLAST, AESDEC, AESKEYGENASSIST), GF(2⁸) S-box, T-Tables 구현. 처리속도: AES-128 CTR 모드 약 8 Gbps (Intel Xeon E5-2690v4), AES-256-GCM 약 4 Gbps |
| **비대칭키 엔진 (Asymmetric Engine)** | 키 교환(Key Exchange), 전자서명(Digital Signature) | RSA-PSS(PKCS#1 v2.2, 2048/3072/4096bit), ECDSA(FIPS 186-4, secp256r1/secp384r1/secp521r1), EdDSA(Ed25519, Ed448), DH/ECDH(X25519, X448), RSA-PSS Probabilistic Signature Scheme |
| **키 유도 함수 (KDF)** | 공유 비밀에서 암호학적 강도 유지한 키 파생 | HKDF(HMAC-based KDF, RFC 5869) = Extract(salt, IKM) -> Expand(PRK, info, L). TLS 1.3은 HKDF-Expand-Label 사용. PBKDF2(bcrypt 100K iter, Argon2id 메모리 64MB 병렬 4) 패스워드 기반 |
| **인증된 암호화 (AEAD)** | 기밀성 + 무결성 + 인증 동시 보장 | AES-GCM (CTR 모드 + GHASH 128-bit MAC), AES-CCM (CTR + CBC-MAC), ChaCha20-Poly1305, AEGIS (Intel AES-NI 최적화, 1.5 cycle/byte). 데이터 평문 + AAD -> (ciphertext, tag) 단일 인터페이스 |
| **공개키 기반 구조 (PKI)** | 신뢰 앵커(Trust Anchor) 통한 공개키 인증 | X.509 v3 (RFC 5280) 디지털 인증서, CSR(Certificate Signing Request, PKCS#10) 형식, OCSP(Online Certificate Status Protocol) 실시간 폐기 검증, CRL(Certificate Revocation List) X.500 디렉터리, CT(Certificate Transparency, RFC 6962) 인증서 투명 로깅 |
| **하드웨어 보안 모듈 (HSM/TPM)** | 키 생성·저장·사용을 TCB(Trusted Computing Base) 내 보호 | FIPS 140-2 Level 3/4 인증 HSM (Thales Luna, AWS CloudHSM, nShield), TPM 2.0 (TCG 표준, PCR 0~23, Key Sealing), Intel SGX/ARM TrustZone enclaves, Apple Secure Enclave, Android StrongBox Keymaster |

**RSA-OAEP (Optimal Asymmetric Encryption Padding)**: Textbook RSA는 결정적(deterministic)이고 malleable하여 Chosen Ciphertext Attack(CCA)에 취약하다. RSA-OAEP(RFC 8017, Bellare-Rogaway 1994)는 평문에 **랜덤 패딩 + 해시 체인(Label, Seed -> MGF1-SHA256)**을 적용하여 IND-CCA2 보안을 달성한다. MGF1(Mask Generation Function)은 PKCS#1에서 정의한 카운터 모드 기반 해시 함수로, 시드와 카운터를 연결한 SHA-256 출력을 XOR
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 378 / 800

<- **이전**: [377. 다중 인증 MFA 생체 인증 패스키](/studynote/12_it_management/05_security_compliance/377_multi_factor_authentication_mfa_biometric/)
**다음**: [379. PKI 공개키 인프라 인증서 관리](/studynote/12_it_management/05_security_compliance/379_pki_public_key_infrastructure_certificate/) ->

---
