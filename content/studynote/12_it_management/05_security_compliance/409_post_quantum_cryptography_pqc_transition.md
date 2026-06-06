---
title: "Post Quantum Cryptography PQC Transition"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 양자 컴퓨터(Shor 알고리즘)가 현재 비대칭키(RSA-2048, ECDSA-P256)와 해시 기반 구조를 무력화함에 따라, NIST PQC 표준(FIPS 203 ML-KEM, 204 ML-DSA, 205 SLH-DSA) 및 한국 KpqC(LAFHE, NTRU+) 알고리즘으로 전환하는 체계적 마이그레이션 전략
> 2. **가치**: HNDL(Harvest Now Decrypt Later) 공격에 대한 10~20년 장기 기밀성 보장과, 양자 안전성 + 알고리즘 유연성(Crypto-Agility) 확보를 통한 미래 규제·감사 대응력 제고
> 3. **판단 포인트**: Mosca 부등식(X+Y>Z) 기반 위험 시점 산정, 하이브리드 모드(X25519+ML-KEM) 우선 적용 여부, 인증서·PKI·HSM·TLS 라이브러리 갱신에 따른 마이그레이션 비용 vs. 양자 위협 시점의 트레이드오프

---

## Ⅰ. 개요 및 필요성

Shor(1994) 알고리즘은 양자 비트(Qubit)의 중첩·얽힘 특성을 활용하여 큰 정수의 소인수분해(RSA)와 이산로그(ECC) 문제를 다항식 시간(O((log N)^3)) 내에 해결할 수 있다. IBM Condor(1,121 qubit, 2023) -> Google Willow(105 qubit, 2024, 오류정정 임계 돌파) -> 양자 우월성 로드맵에 따라 2029~2035년경 논리 큐비트 4,096~20,000개급 CRQC(Cryptographically Relevant Quantum Computer) 등장 가능성이 거론된다. RSA-2048 격파에는 약 4,096 논리 큐비트, ECC P-256 격파에는 약 2,500 논리 큐비트가 필요한 것으로 NIST SP 800-208 및 ETSI GR QSC 006에서 산정한다.

이에 NIST는 2016년 PQC 표준화 프로젝트를 착수하여 2022년 7월 4개 1차 선정 알고리즘을 발표했고, 2024년 8월 ML-KEM(FIPS 203), ML-DSA(FIPS 204), SLH-DSA(FIPS 205) 등 3개 FIPS 표준을 확정 발표하였다. 한국은 KISA 주도로 2022년 KpqC( Korea Post-Quantum Cryptography) 공모를 통해 LAFHE(Learning with Errors 기반 KEM)와 SMAUG-T(부채널 안전 격자 서명), AIMer(해시 기반 서명) 등 2차 winner를 선정했다.

```text
[기존 RSA/ECC 체계의 양자 취약점과 PQC 전환 동기]

   +--------------------+
   |  Classical Computer |         +---------------------+
   |  - RSA-2048: 안전   |         |  Quantum Computer    |
   |  - ECC P-256: 안전  |         |  - Shor 알고리즘     |
   |  - AES-128: 안전(양자|  --->   |  - RSA/ECC 무력화    |
   |    공격시 256-bit)  |         |  - Grover: AES-128   |
   +--------------------+         |     -> 64-bit 보안강도 |
            ^                      +---------------------+
            |                                ^
            |     Mosca 부등식 (X+Y > Z)     |
            |  X: 데이터 보존기간             |
            |  Y: 양자컴퓨터 도달 시간(5~15년)|
            |  Z: 현재 자산의 남은 수명       |
            |                                |
   +--------+------------------------+       |
   |  HNDL (Harvest Now, Decrypt Later)|------+
   |  - 현재 수집된 암호화 데이터      |
   |  - 10~20년 후 양자컴으로 복호화   |
   +---------------------------------+
```

Mosca의 양자 위협 시뮬레이션 결과, 정부·국방·의료·금융 데이터의 평균 보존 요구사항(10~50년)과 양자컴 도달 시점(평균 10년)을 합산하면, 이미 **모든 장기 기밀 데이터가 위험 영역**에 진입했다. 이것이 PQC 전환이 단순 옵션이 아닌 **국가 사이버 안보 필수 과제**인 이유다.

- **📢 섹션 요약 비유**: 양자컴퓨터는 현재 자물쇠(RSA)를 마술 지팡이(Shor 알고리즘)로 한 번에 열어버리는 마법사이고, PQC는 자물쇠 자체를 마법사가 풀 수 없는 신소재(격자 문제)로 교체하는 작업이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PQC 전환은 단일 알고리즘 교체가 아니라 **암호학적 기반 패러다임 전환**이다. NIST가 선정한 PQC 알고리즘은 4개의 서로 다른 수학적 난제에 기반하며, 각각 트레이드오프가 존재한다.

```text
[ PQC 전환 아키텍처: Crypto-Agility 기반 계층화 ]

  +----------------------------------------------------------+
  |  Application Layer (ERP, 금융앱, IoT, 문서보안)          |
  |  - 알고리즘 호출 추상화 (Abstraction Layer)              |
  |  - Crypto Provider 패턴 (OpenSSL ENGINE, PKCS#11)        |
  +----------------------------------------------------------+
  |  Protocol Layer (TLS 1.3, IKEv2, S/MIME, JWT, CMS)      |
  |  - Hybrid Key Exchange: X25519 + ML-KEM-768              |
  |  - Hybrid Signature: RSA-PSS + ML-DSA-65                 |
  +----------------------------------------------------------+
  |  PKI / Certificate Authority Layer                       |
  |  - 신규 OID 등록: 2.16.840.1.101.3.4.3.17 (id-ml-kem-768)|
  |  - 인증서 체인 갱신 및 듀얼 알고리즘 발급                 |
  |  - HSM (Hardware Security Module) PQC 지원 검증          |
  +----------------------------------------------------------+
  |  Cryptographic Library Layer                             |
  |  - OpenSSL 3.5+ (ML-KEM 네이티브), BoringSSL, liboqs    |
  |  - Bouncy Castle 1.78+, Java SunJCE 21+                 |
  +----------------------------------------------------------+
  |  Hardware / Firmware Layer (HSM, TPM 2.0, Secure Enclave)|
  |  - 양자 안전 키 생성/저장 (PQC 알고리즘 가속기)           |
  |  - TPM 2.0 PCR 확장 (영지키 보호)                         |
  +----------------------------------------------------------+

  [ PQC 알고리즘 분류 (NIST FIPS 2024) ]

  +----------------+--------------+--------------+--------------+
  |  KEM (Key Enc) | ML-KEM-512   | ML-KEM-768   | ML-KEM-1024  |
  |  (FIPS 203)    | NIST L1      | NIST L3      | NIST L5      |
  +----------------+--------------+--------------+--------------+
  |  Digital Sig.  | ML-DSA-44    | ML-DSA-65    | ML-DSA-87    |
  |  (FIPS 204)    | NIST L2      | NIST L3      | NIST L5      |
  +----------------+--------------+--------------+--------------+
  |  Hash-based    | SLH-DSA-SHA2 | SLH-DSA-SHAKE| SLH-DSA-SHA2 |
  |  Sig (FIPS205) | 128s/f       | 192s/f       | 256s/f       |
  +----------------+--------------+--------------+--------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ML-KEM (Module-Lattice-KEM)** | 양자 안전 키 캡슐화 (KEM) | Module-LWE 문제 기반; 공개키 1,184B / 암호문 1,088B (768), NTT 변환 + 압축; Kyber의 후속으로 부채널 마스킹 통합 |
| **ML-DSA (Module-Lattice-DSA)** | 양자 안전 전자서명 | Module-LWE + Short Integer Solution (SIS) 이중 난제; Dilithium 후속; Fiat-Shamir with Aborts + rejection sampling |
| **SLH-DSA (Stateless Hash-DSA)** | 격자 대안 서명 | SPHINCS+ 기반; 다중 해시 함수(SHA-2, SHAKE, Haraka); 서명 크기 7.8~49KB로 큼, 부채널 안전 최고 수준 |
| **Hybrid KEM (X25519+ML-KEM)** | 전환기 양방향 안전성 | IETF TLS WG draft-ietf-tls-kyber; 두 KEM의 공유 비밀을 HKDF(SHA-256)으로 결합; 기존 X.509 인증서와 호환 |
| **Crypto-Agility 엔진** | 알고리즘 추상화 및 핫스왑 | OpenSSL 3.x OQS-provider, AWS s2n, Google Tink, PKCS#11 v3.0 (CKA_NSS_PARAMETER_VALIDATE) |

**핵심 파라미터 분석 (ML-KEM-768 기준):**
- 공개키: 1,184 bytes (RSA-2048: 256 bytes 대비 4.6배)
- 암호문: 1,088 bytes
- 공유 비밀: 32 bytes (SHA3-256 출력)
- 클라이언트 Hello 확장 크기: 약 1.6KB -> TLS 핸드셰이크 MTU 영향 분석 필수

**부채널 공격 저항성:** ML-KEM은 Barrett reduction 및 bit slicing 구현 시 타이밍/캐시 공격에 취약할 수 있어, masking(Shuffling + Boolean masking) 및 constant-time 코딩이 필수이다. NIST CAVP(Algorithm Validation Program) 및 CAVS(KAT - Known Answer Test) 검증이 필요하다.

**한국 KpqC 알고리즘 동향:**
- KEM: LAFHE (Lattice-based, LWE + Module 구조), NTRU+ (3라운드 승자 후보)
- Signature: SMAUG-T (lattice, 작은 서명 크기 강점), AIMer (해시 기반, SLH-DSA 대안)

- **📢 섹션 요약 비유**: ML-KEM은 격자(Lattice)라는 다차원 미로에 함정을 숨기는 것이고, ML-DSA는 그 미로의 출구 비밀번호를 만드는 도구이며, SLH-DSA는 해시 함수만으로 만든 양자 안전 도장이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 기존 RSA/ECC | PQC (격자 기반) | PQC (해시 기반) | QKD (Quantum Key Distribution) |
| :--- | :--- | :--- | :--- | :--- |
| **기반 난제** | 정수 소인수분해, 이산로그 | Module-LWE / SIS | 해시 함수 충돌 저항성 | 양자역학적 측정 불가침 |
| **양자 공격** | Shor로 다항식시간 격파 | 최선의 알려진 공격은 지수적 (BKZ lattice reduction) | Grover로 √n (해시 출력 2배 키) | 이론적 도청 불가능 (BB84, E91 프로토콜) |
| **키/서명 크기** | RSA-2048 PK=256B, Sig=256B | ML-KEM-768 PK=1,184B, ML-DSA-65 Sig=3,293B | SLH-DSA-128f Sig=17KB | 키 1회당 256bit (1회성) |
| **성능 (ops/sec)** | RSA-2048 sign: ~1,000/s (SW) | ML-KEM-768 encap: ~50,000/s (AVX2) | SLH-DSA-128s: ~100/s (느림) | 1Mbps (BB84 전용선) |
| **하드웨어 의존** | 범용 CPU/HSM | HSM 지원 진행중 (Entrust, Thales, Utimaco) | 표준 SW 가능 | 광자 검출기, 단일광자 소스, 양자채널 필요 |
| **도입 난이도** | 50년 검증 완료 | NIST 표준화 완료 (2024), TLS 1.3 실험적 | 검증된 수학적 기반, 서명 크기 부담 | 전용 인프라, 중계기 신뢰 문제, 비용 > 1억원/km |
| **적용 시나리오** | 현재 모든 인터넷 트래픽 | 일반 TLS, PKI, 문서서명, VPN 대체 | 펌웨어 업데이트, 장기기록 인증 | 국방/금융 전용선, 백본 데이터센터간 |

**다른 시스템 계층과의 연결:**

1. **PKI/CA 계층:** 루트 CA(한국정보인증, GlobalSign 등)는 2025~2026년부터 PQC 인증서 발급 시작 예정. 인증서 프로파일은 RFC 9881 (draft-ietf-lamps-x509-alg) 및 X.509 v3에 PQC OID 추가 필요. OCSP Stapling 응답자도 ML-DSA 서명 지원 필수.

2. **TLS/SSL 라이브러리:** OpenSSL 3.5(2025.1), BoringSSL (Chrome 124+ X25519Kyber768 기본 활성화), AWS s2n (PQ-Support branch), wolfSSL (ML-KEM 지원). Java는 SunJCE 21+ 및 Bouncy Castle 1.78+에서 PQC 활성화.

3. **HSM/PKI 하드웨어:** Thales Luna HSM v7.8.7 (ML-KEM FIPS 140-3 Level 3 인증 중), Entrust nShield, Utimaco CryptoServer (FIPS 140-3 + PQC add-on). TPM 2.0은 Microsoft Pluton / Google Titan M3에서 PQC 부팅 측정(measured boot) 지원 예정.

4. **클라우드/IAM:** AWS KMS는 2024년 말 ML-KEM 비대칭키 지원 시작, Azure Key Vault HSM(신형), Google Cloud KMS 비대칭 키 PQC. AWS s2n-tls, GCP의 hybrid PQ key exchange는 X25519+ML-KEM-768 기본 적용.

5. **블록체인/스마트계약:** 이더리움 EIP-7569 (PQC-friendly signature verification opcode), 비트코인 taproot PQC migration 토론 진행 중.

- **📢 섹션 요약 비유**: QKD는 광케이블이 필요해 특정 도로만 운행하는 전용 고속도로이고, PQC는 모든 기존 도로를 양자 안전 차선으로 재포장하는 전국 도로 개수선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **자산의 양자 위험 등급 분류 (Crypto-Bill of Materials, CBOM)**: 전사 시스템의 TLS 종단점, PKI 인증서, HSM 키, SSH 키, 코드서명, API 키, IoT 펌웨어 서명을 점검하고, 데이터 보존기간과 양자 도달 시점을 매트릭스로 작성했는가? (예: 의료 DICOM 영상 30년 보존 -> PQC 우선순위 최상)
2. **Crypto-Agility 아키텍처 설계**: 알고리즘 호출부를 인터페이스(예: Java JCA `KeyFactory.getInstance("ML-KEM")` 또는 Go `crypto.Signer` 추상화)로 분리하고, 설정 기반 핫스왑이 가능한가? 컴파일 타임 알고리즘 하드코딩을 제거했는가?
3. **하이브리드 KEM 우선 도입 전략**: IETF draft-ietf-tls-kyber-06 (또는 최신 draft-ietf-tls-kyber.html)의 X25519+ML-KEM-768 concat KEM을 TLS 1.3 연결에서 우선 활성화했는가? downgrade attack 방어를 위해 `
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 409 / 800

<- **이전**: [408. AI 보안 적대적 공격 방어 전략](/studynote/12_it_management/05_security_compliance/408_ai_security_adversarial_attack_defense/)
**다음**: [410. IT 거버넌스 프레임워크 COBIT 2019](/studynote/12_it_management/05_security_compliance/410_it_governance_framework_cobit_2019/) ->

---
