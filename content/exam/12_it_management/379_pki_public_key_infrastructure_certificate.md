---
title: "PKI Public Key Infrastructure Certificate"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PKI는 **X.509 v3 인증서**(RFC 5280)와 **CA(인증기관) 신뢰 계층 모델**을 통해 공개키의 신원과 진위를 보증하는 인프라로, `Subject DN + Issuer DN + Serial Number + Validity Period + SubjectPublicKeyInfo + Extensions(CRL Distribution Points, AIA, Key Usage, EKU, SAN)` 구조와 **RSA/ECDSA 서명 알고리즘**, **SHA-2/3 해시**, **CRL/OCSP/OCSP Stapling 폐기 검증 체계**로 구성된다.
> 2. **가치**: TLS 1.3 핸드셰이크에서 인증서 체인 검증 시 **상위 CA 인증서로 거슬러 올라가는 Path Validation(2.5~15ms)**, **OCSP Stapling 적용 시 50~200ms RTT 절감**, **ECDSA P-256 키(32B) 대비 RSA-2048(256B) 저장/전송 효율 8배**, **HSM 내 키 보관 시 FIPS 140-2 Level 3** 물리적 보호를 통해 **연간 인증서 라이프사이클 100% 가시성** 및 **MITM 공격 0건** 보안 KPI 달성이 가능하다.
> 3. **판단 포인트**: Root CA는 **오프라인 + 에어갭(7년 이상 갱신)**, Issuing CA는 **온라인 + HSM**, 인증서 프로파일은 **DV/OV/EV** 등급별(검증 강도 4단계) 분기, 폐기 검증은 **CRL(네트워크 부하) vs OCSP(실시간, 프라이버시 이슈) vs OCSP Stapling(권장) vs CRLite(차세대)** 중 트래픽/지연/개인정보 요건에 따라 결정, **PQC(Post-Quantum Cryptography) 전환 로드맵**(ML-DSA/ML-KMS, 2025 NIST FIPS 203/204/205 표준화)에 따른 **하이브리드 인증서 전략**이 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

인터넷은 기본적으로 **비연결·비신뢰·평문(plaintext)** 환경이다. 1970년대 이후 TCP/IP의 **패킷 스위칭 모델**은 송신자와 수신자의 신원, 메시지 무결성, 기밀성을 기본적으로 보장하지 않는다. 1976년 **Diffie-Hellman 키 교환**과 1978년 **RSA 알고리즘**이 등장하면서 **비대칭키(공개키) 암호**가 가능해졌으나, "Alice의 공개키가 진짜 Alice 것인가?"라는 **키 분배 문제(Key Distribution Problem)**가 핵심 이슈로 남았다.

이를 해결하기 위해 **MIT(Loren Kohnfelder, 1978, "Towards a Practical Public-Key Cryptosystem")**에서 인증서 개념이 제안되었고, **ITU-T X.509(1988, v1 -> 1993 v2 -> 1996 v3)**, **IETF PKIX WG(RFC 2459 -> 1999, RFC 3280 -> 2002, RFC 5280 -> 2008, RFC 9598 -> 2024)** 표준으로 정착되었다. 한국은 1999년 **정보통신망 이용촉진 및 정보보호 등에 관한 법률** 개정과 **한국정보인증(한국CA)**, **금융결제원 공동인증(구 공인인증서)**, **행정안전부 정부GPKI**, **국방부 NPKI**, **한국인터넷진흥원(KISA) 행정용 인증** 등 단계적 도입을 거쳐 **2020년 전자서명법 개정(공인인증서 폐지 -> 민간 인증서 자율화)**로 전환되었다.

기존 **대칭키 공유(Pre-shared Key, Diffie-Hellman Key Exchange)**만으로는 **N(N-1)/2 = 1,000명 시 499,500개 키** 관리 불가능한 **N² 스케일링 문제**와 **중간자 공격(Man-in-the-Middle)** 취약점이 존재했다. PKI는 **신뢰 앵커(Trust Anchor) -> 인증서 체인 -> 서명 검증** 구조로 이를 해결한다.

```text
+---------------------------------------------------------------------+
|          PKI 신뢰 계층 구조 (X.509 Certificate Chain)              |
+---------------------------------------------------------------------+
                              ^
                              | Self-signed (자기서명)
                              | Subject == Issuer
                              | Root CA: 20~30년 유효
                              | ⚠ 오프라인 + 에어갭 운영
                  +-----------------------+
                  |  Root CA (최상위)     |  <- Trust Anchor
                  |  "CN=SecureSign Root  |
                  |   CA, O=RootCA Corp" |
                  +----------+------------+
                             | Cross-signed (크로스 인증)
                             | 또는 단일 체인
              +--------------+--------------+
              v                              v
      +----------------+             +----------------+
      | Intermediate   |             | Intermediate   |
      | CA (정책 CA)   |             | CA (발급 CA)   |
      | 유효 10~15년   |             | 유효 7~10년    |
      | HSM 보관       |             | HSM 보관       |
      +--------+-------+             +--------+-------+
               | CA-issuing (AIA: Authority Info Access)
               |                            |
   +-----------+------------+    +----------+------------+
   v                        v    v                       v
+---------+            +---------+              +---------+
|Server   |            |Server   |              |Client   |
|Cert     |            |Cert     |              |(Smart   |
|(TLS)    |            |(Code    |              | Card)   |
|1~2년    |            |Signing) |              |1~3년    |
+---------+            +---------+              +---------+
   EKU=TLS Server Auth   EKU=Code Signing         EKU=Client Auth
```

기존 패러다임(비대칭키 직접 교환, SSH 호스트키 핑거프린트 수동 비교, IPSec IKEv1 PSK)과 비교하여 PKI는 **신뢰 위임(Delegation of Trust)**, **만료 자동화(Automated Expiry)**, **폐기 검증(Revocation)**, **책임 추적(Non-repudiation)** 측면에서 우위를 가진다. 다만 초기 한국 공인인증서는 **ActiveX + 독점 규격 + 단일 CA 종속**으로 사용자 불편이 극심했고, 2020년 **전자서명법 전면 개정**(공인인증서 폐지) 및 **웹 표준 기반**으로 전환된 점이 큰 변화다.

- **📢 섹션 요약 비유**: PKI는 여권 발급 시스템과 같다. 여권은 **내무부(Root CA)**가 발급한 **신원증명서(인증서)**이고, 그 안에 **지문(공개키)**과 **사진(Subject 정보)**이 있으며, 입국 시 **공항 검문소(브라우저/OS)**가 여권의 진위와 발급기관 신뢰 여부를 확인하여 비자를 인정(신뢰 체인 검증)하는 것과 같은 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PKI는 **RA(Registration Authority) -> CA(Certification Authority) -> VA(Validation Authority) -> CPS(Certification Practice Statement)** 4대 기능과 **디렉터리(LDAP/X.500)**, **타임스탬프(TSA, RFC 3161)**, **OCSP responder** 지원 컴포넌트로 구성된다. 인증서 포맷은 **ASN.1 DER(Distinguished Encoding Rules) -> X.509 v3 구조**이며, **PEM(Base64 + -----BEGIN CERTIFICATE-----)**, **DER(Binary)**, **PKCS#7/CMS(Signed Data)**, **PKCS#12/PFX(개인키+인증서 번들, AES-256/SHA-256)** 형태로 저장된다.

```text
+---------------------------------------------------------------------+
|         X.509 v3 인증서 발급 및 검증 프로토콜 플로우                |
+---------------------------------------------------------------------+

[1단계: 키 생성 (Key Generation)]
  +---------+    openssl ecparam -name prime256v1 -genkey -noout
  | End-    |    또는 HSM 내부: PKCS#11 C_GenerateKeyPair (CKM_EC_KEY_PAIR_GEN)
  | Entity  |    결과: { priv, pub } (개인키는 안전 저장)
  +----+----+
       | CSR 제출 (PKCS#10, RFC 2986)
       | Subject DN: CN=www.example.com, O=Example, C=KR
       | SubjectPublicKeyInfo: AlgoID + PublicKey Bit String
       | Attributes: extensionRequest (SAN, EKU)
       | Signature: priv.sign(SHA-256(CSR Info)) [ECDSA/RSA]
       v
[2단계: RA 신원 검증 (Identity Vetting)]
  +---------+    DV: 도메인 제어 검증 (HTTP-01 challenge, DNS-01 TXT, ACME)
  |   RA    |    OV: 사업자등록증 + 도메인 + 전화 검증 (3~5일)
  |  (등록) |    EV: 확장 검증 (법적 문서 + 계약 + 면담, 7~14일)
  +----+----+         결과: 검증된 Subject 정보 + 정책 OID
       | 승인
       v
[3단계: CA 발급 (Certificate Issuance)]
  +---------+    X.509 v3 구조 생성 (RFC 5280 §4.1):
  |   CA    |      Version: 3 (0x02)
  | (발급)  |      Serial: 128-bit random (CA 정책)
  |  HSM    |      Signature Algo: sha256WithRSAEncryption (1.2.840.113549.1.1.11)
  |  서명   |              또는 ecdsa-with-SHA256 (1.2.840.10045.4.3.2)
  |         |      Issuer: CN=Issuing CA, O=Example CA
  |         |      Validity: notBefore (UTCTime/GeneralizedTime)
  |         |                notAfter  (최대 398일/825일, CA/B Forum BR)
  |         |      Subject: CN=www.example.com
  |         |      SubjectPublicKeyInfo: { Algo, PublicKey }
  |         |      Extensions:
  |         |        KeyUsage: digitalSignature, keyEncipherment (CRITICAL)
  |         |        ExtKeyUsage: id-kp-serverAuth, id-kp-clientAuth
  |         |        BasicConstraints: cA=FALSE (CRITICAL)
  |         |        SAN: DNS:www.example.com, DNS:api.example.com
  |         |        CRL Distribution Points: URI:http://ca.example.com/crl.crl
  |         |        Authority Info Access: OCSP URI:http://ocsp.example.com
  |         |        Certificate Transparency: SCT (Signed Certificate Timestamp)
  |         |        SubjectAltName: Critical=False
  |         |      Signature: CA_priv.sign(SHA-256(DER-encoded TBSCertificate))
  +----+----+
       | 인증서 반환 (PEM/DER)
       v
[4단계: 배포 (Deployment)]
  +---------+    웹서버: nginx ssl_certificate, Apache SSLCertificateFile
  | End-    |    클라이언트: PKCS#12 -> 브라우저/HSM/스마트카드 import
  | Entity  |    자동화: ACME (Let's Encrypt) certbot --nginx
  +----+----+    또는: cert-manager (Kubernetes), Vault PKI Engine
       |
       | 사용: TLS 1.3 핸드셰이크
       v
[5단계: 검증 (Validation, RFC 5280 §6)]
  +-------------+
  | Verifier    |    ① 체인 빌드: End-Entity <- Intermediate <- ... <- Trust Anchor
  |(브라우저/   |    ② 서명 검증: 각 인증서의 서명 = Issuer_pub.verify(Sig)
  | TLS 클라이언|       ECDSA: (r, s) 서명 -> NIST P-256 곡선 위 검증
  | 트)         |    ③ 유효기간: now ∈ [notBefore, notAfter]
  |             |    ④ 폐기 검증: CRL/OCSP 조회
  |             |    ⑤ 정책 매핑: ExtKeyUsage 확인
  |             |    ⑥ 이름 제약: NameConstraints extension
  |             |    ⑦ 키 사용: KeyUsage 확인
  |             |    ⑧ 신뢰 앵커 매칭: 자체 Trust Store (Mozilla, Apple, MS)
  +-------------+
       |
       v
  [신뢰/거부 결정]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Root CA** | 최상위 신뢰 앵커, 자기서명 인증서 | **X.509 v3, SHA-256/RSA-4096 또는 SHA-384/ECDSA P-384**, **20~30년 유효**, **CRL/ARL(Authority Revocation List) 발행**, **오프라인 + 에어갭 + HSM FIPS 140-2 Level 4**, **CA/B Forum BR §1.2.1** 정책 준수 |
| **Intermediate CA** | 정책 분리, 발급 격리 (Compromise 시 Root 보호) | **Cross-certificate**로 Root 서명, **10~15년 유효**, **온라인 가능**, **OCSP 응답자 운영**, **CPS(Certification Practice Statement) 문서화**, **WebTrust/ETSI审计** 매년 |
| **RA (Registration Authority)** | 신원 검증, 등록 승인 | **DV (Domain Validation)**: ACME HTTP-01, DNS-01(CAA record), TLS-ALPN-01 (RFC 8737), **OV (Organization Validation)**: 사업자등록증 + 도메인 + 전화, **EV (Extended Validation)**: 증빙 7단계 + 계약 + 재검증 매년 |
| **VA (Validation Authority)** | 실시간 폐기 검증 | **CRL (Certificate Revocation List)**: X.509 v2 CRL, **RFC 5280 §5.1**, **nextUpdate(7일)**, **deltaCRL**(증분), **파티션 CRL**(대규모), **OCSP (RFC 6960)**: 클라이언트 HTTP GET, 서명된 응답, **must-staple** (RFC 7633), **OCSP Stapling (RFC 6066 §8)**, **CRLite**: Bloom filter 기반 |
| **HSM (Hardware Security Module)** | 키 생성/저장/서명, FIPS 140-2/3 | **PKCS#11 (C_Login, C_Sign, C_GenerateKey)**, **FIPS 140-2 Level 3/4** (물리적 침입 탐지, tamper-evident), **nShield, Thales Luna, AWS CloudHSM, YubiHSM 2**, **클라우드 HSM API**: Azure Dedicated HSM, GCP Cloud HSM, AWS PKCS#11 SDK |
| **디렉터리 (LDAP/X.500)** | 인증서/CRL 배포, 조회 | **LDAP v3 (RFC 4511)**, **X.500 DN(Distinguished Name)**: `CN=www.example.com,OU=Eng,O=Example Corp,C=KR`, **CRL Distribution Point (CDP)** URI, **AIA (Authority Information Access)** OCSP responder URI, **DNS CAA record** (`issue "letsencrypt.org"`, `issuewild ";")` |
| **TSA (Time Stamp Authority)** | 부인방지, RFC 3161 | **Time-Stamp Protocol (TSP)**, **PKCS#9 signing-time attribute**, **RFC 5816 ESI (Evidence Record Syntax)**, **eIDAS AdES (B/LT/LTA)**: archive timestamp |
| **CMP/CRMF/SCEP/ACME/EST** | 자동 등록/갱신 프로토콜 | **CMP (RFC 4210/4211)**: CA
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 379 / 800

<- **이전**: [378. 암호화 기술 대칭 비대칭 하이브리드](/studynote/12_it_management/05_security_compliance/378_encryption_symmetric_asymmetric_hybrid/)
**다음**: [380. 전자서명 디지털 서명 비부인 무결성](/studynote/12_it_management/05_security_compliance/380_digital_signature_non_repudiation_integrity/) ->

---
