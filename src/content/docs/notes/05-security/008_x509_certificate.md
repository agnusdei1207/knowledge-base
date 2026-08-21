---
sidebar:
  order: 8
  label: "008. X.509 인증서 (X.509 Certificate)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "디지털 신원 증명 표준 포맷 : ITU-T X.509 v3 인증서 (Public Key Certificate)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 8
extra:
  question_no: "008"
  source_status: "기출"
  source_history: "120회, 138회"
  priority: 70
  priority_note: "TBSCertificate 구조, Subject/Issuer/Validity, SAN/KeyUsage/BasicConstraints 확장 필드(RFC 5280)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ITU-T X.509 v3 인증서(RFC 5280)**: 비대칭 공개키(Public Key)에 소유자의 식별 정보(Subject DN / SAN), 유효기간(Validity), 허용 용도(Key Usage)를 결합하고 신뢰할 수 있는 공인 인증기관(CA)의 전자서명을 첨부하여 위변조를 방지한 국제 표준 디지털 증명서 포맷.
- **TBS 인증서(TBSCertificate / To-Be-Signed Certificate)**: 인증서 내에서 발급자 CA가 전자서명을 수행하기 전의 원시 메타데이터 블록(버전, 일련번호, 서명 알고리즘, 발행자, 유효기간, 주체, 주체 공개키 정보, 확장 필드 일체).

</details>

- 정의/개념: ASN.1 DER(Distinguished Encoding Rules) 바이너리 포맷으로 인코딩된 **TBSCertificate 구조** 에 대해 인증기관(CA)의 비대칭 개인키로 전자서명($\text{Sign}_{\text{CA}}(\text{Hash}(\text{TBS}))$)을 수행하여 소유권과 진본성을 공인하는 **디지털 신원 증명서**
- 배경/필요성: 공개키 텍스트 자체만으로는 해당 키의 실제 소유자가 누구인지, 어느 도메인에 바인딩되어 있는지, 어떤 암호 용도로 사용 가능한지 판별할 수 없는 보안 사각지대를 해소할 요구

#### 한줄 요약
- 공개키와 소유자 신원 및 용도 제약 조건을 TBS 블록에 담고 CA 전자서명으로 무결성을 보증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **주체 대체 이름(Subject Alternative Name, SAN)**: 단일 인증서에 다수의 도메인 FQDN(예: `example.com`, `api.example.com`), 와일드카드(`*.example.com`), IP 주소(`192.168.1.1`)를 등록하여 유연한 식별을 가능하게 하는 필수 확장 필드.
- **기본 제약(Basic Constraints / isCA)**: 해당 인증서가 다른 하위 인증서를 서명 발급할 수 있는 CA 인증서인지(`isCA=TRUE`), 아니면 단지 트래픽 통신에만 사용되는 최종 단말(End-Entity) 인증서인지(`isCA=FALSE`)를 엄격히 제한하는 필드.

</details>

- **표준화된 계층형 메타데이터 구조**: ASN.1 구문 표기법 및 DER 엄격 인코딩을 통해 이종 OS/언어 간 완벽한 상호운용성 제공
- **다차원 접근 제어 및 용도 제한 (Extensions)**: SAN(도메인 바인딩), Key Usage(서명/키 교환), Extended Key Usage(서버 인증, 클라이언트 인증, 코드 서명)
- **자체 완결적 무결성 검증**: CA의 공개키로 인증서 자체의 서명값만 대조하면 1비트의 변조도 즉시 판정 가능

#### 한줄 요약
- ASN.1/DER 구조, SAN 도메인 확장, Key Usage 용도 제약, Basic Constraints CA 권한 분리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **주체 공개키 정보(SubjectPublicKeyInfo, SPKI)**: 인증서가 증명하고자 하는 소유자의 공개키 알고리즘 OID(예: RSA, ECDSA, Ed25519)와 실제 공개키 비트열 데이터를 담고 있는 핵심 필드.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ X.509 v3 Certificate 구조 (RFC 5280) ]                                │
│                                                                         │
│ ┌─ [ TBSCertificate (To-Be-Signed: 서명 대상 메타데이터 블록) ] ───────┐│
│ │  ├─ Version (v3: 0x02) & Serial Number (고유 일련번호)               ││
│ │  ├─ Signature Algorithm Identifier (예: ecdsa-with-SHA256)           ││
│ │  ├─ Issuer (발행자 CA 고유 명칭: DN) & Validity (NotBefore ~ NotAfter)││
│ │  ├─ Subject (주체 소유자 명칭: DN)                                    ││
│ │  ├─ SubjectPublicKeyInfo (SPKI: 알고리즘 OID + 공개키 비트열)         ││
│ │  └─ Extensions (확장 필드 v3):                                       ││
│ │       ├─ Basic Constraints: isCA=FALSE, PathLenConstraint=None        ││
│ │       ├─ Key Usage: Digital Signature, Key Encipherment               ││
│ │       ├─ Extended Key Usage (EKU): ServerAuth, ClientAuth             ││
│ │       ├─ Subject Alternative Name (SAN): DNS:api.domain.com, IP:1.1.1.1││
│ │       └─ CRL Distribution Points (CDP) & Authority Info Access (AIA:OCSP)│
│ └──────────────────────────────────────────────────────────────────────┘│
│                                    │                                    │
│                                    ▼ (SHA-256 다이제스트 추출)           │
│ ├─ SignatureAlgorithm (서명 알고리즘: ecdsa-with-SHA256)                 │
│ └─ SignatureValue (CA 개인키로 서명된 암호학적 서명 비트열)              │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: TBSCertificate 블록 전체를 해싱한 후 CA의 개인키로 서명하여 SignatureValue를 생성하고, 클라이언트는 Issuer의 공개키로 이를 검증하는 구조

| 구성요소 | 핵심 필드명 및 역할 | 비고 |
|:---|:---|:---|
| **기본 메타데이터** | Version(v3), Serial Number(CA 내 유일값), Validity(유효 시작/만료 시각) | RFC 5280 Base |
| **발행자 및 주체** | Issuer(발급 CA 식별자: C=KR, O=KISA, CN=Root CA), Subject(소유자 식별자) | X.500 DN |
| **주체 공개키 (SPKI)** | AlgorithmIdentifier(OID) 및 소유자의 비대칭 공개키(Public Key Raw Data) | Public Key |
| **Basic Constraints** | `critical, CA:FALSE` 지정을 통해 최종 단말 인증서의 불법 하위 CA 인증서 발행 차단 | Path Control |
| **SAN / Key Usage** | 인증서가 유효한 FQDN/IP 주소 목록 및 허용 암호 연산(서명, 암호화) 정의 | Extensions |
| **폐기 배포점 (AIA/CDP)**| CRL 다운로드 URL(CDP) 및 실시간 OCSP 응답 서버 URL(AIA) 명시 | Revocation Point |

#### 한줄 요약
- TBSCertificate(기본 정보, SPKI, 확장 필드)와 CA 전자서명(SignatureValue)이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RFC 5280 인증서 경로 검증**: 클라이언트가 서버 인증서를 수신했을 때 수행하는 5단계 필수 검증:
  1. 현재 시각이 Validity(NotBefore ~ NotAfter) 범위 내인지 확인
  2. 접속한 URL의 도메인이 인증서의 SAN(Subject Alternative Name)과 일치하는지 확인
  3. 상위 CA의 공개키로 SignatureValue의 수학적 서명 일치 확인
  4. Extensions 필드의 Basic Constraints 및 EKU(ServerAuth) 적합성 확인
  5. OCSP/CRL을 질의하여 인증서의 폐기(Revocation) 여부 확인

</details>

```text
1. 클라이언트(브라우저)가 서버(HTTPS)에 접속 ➔ 서버가 X.509 인증서 체인(Server + Intermediate CA) 전송
            │
            ▼
2. [1단계: 유효기간 검증] 현재 UTC 시각이 NotBefore와 NotAfter 사이에 존재하는지 확인
            │
            ▼
3. [2단계: 도메인 일치 검증] 접속 대상 FQDN이 인증서의 SAN(Subject Alternative Name) 목록에 일치하는지 대조
            │
            ▼
4. [3단계: CA 서명 체인 검증] Intermediate CA의 공개키로 Server TBS 서명 검증 ➔ Root CA까지 역추적 반복
            │
            ▼
5. [4단계: 확장 필드 및 폐기 검증] EKU(ServerAuth) 확인 및 AIA URL로 OCSP 실시간 폐기 여부 조회 ➔ 통신 허용
```

**동작 원리**

1. **인증서 수신**: TLS 핸드셰이크의 Certificate 메시지를 통해 DER 인코딩 인증서 바이트열 수신
2. **파싱 및 날짜 점검**: ASN.1 구조체를 디코딩하여 시스템 RTC 시각과 비교
3. **이름 제약 대조**: HTTP 요청 헤더의 Host/SNI와 인증서 SAN 필드의 와일드카드 매칭 수행
4. **암호학적 서명 역추적**: 상위 CA 인증서의 SPKI 공개키를 추출하여 서명값 검증
5. **폐기 확인**: OCSP Stapling 응답 또는 직접 질의를 통해 인증서 유효성 최종 확정

#### 한줄 요약
- 인증서 수신, 유효기간 점검, SAN 도메인 대조, CA 서명 체인 검증, OCSP 폐기 확인 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **X.509 인증서 심사 수준별 분류**: 도메인 소유권만 자동 확인하는 DV, 조직 실존성을 심사하는 OV, 법적 실체와 물리적 실재성을 최고 수준으로 검증하는 EV 인증서.

</details>

| 비교 항목 | 도메인 검증 (DV: Domain Validation) | 조직 검증 (OV: Organization Validation) | 확장 검증 (EV: Extended Validation) |
|:---|:---|:---|:---|
| **신원 심사 수준** | **도메인 DNS/HTTP 소유권만 자동 확인** | **사업자등록증, 조직 실존 여부 서류 심사** | **법적 실체, 공인 재직 확인, 전화 실사** |
| **발급 소요 시간** | **수 분 이내 (ACME 완전 자동화)** | 1 ~ 3 영업일 | 3 ~ 7 영업일 |
| **인증서 주체 정보** | 주체명(Subject)에 도메인명만 표기 | **조직명(O), 지역(L), 국가(C) 명시** | **사업자등록번호, 상세 주소 명시** |
| **구축 비용** | 무료 (Let's Encrypt) ~ 저가 | 중간 | 고가 |
| **주요 적용 대상** | **개인 블로그, 소규모 웹사이트, API 서버**| **일반 기업 웹사이트, 전자상거래 포털** | **금융권(은행, 증권사), 공공기관 결제망** |

#### 한줄 요약
- DV는 도메인 자동 검증용, OV는 기업 실존 검증용, EV는 금융/공공 최고 수준 검증용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **인증서 용도 위반 공격(Key Usage Abuse)**: 공격자가 클라이언트 인증용(ClientAuth) 또는 S/MIME 이메일용으로 발급받은 인증서를 가짜 웹 서버의 TLS 인증서(ServerAuth)로 전용하여 중간자 공격(MITM)을 시도하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 클라이언트가 인증서의 EKU 및 Key Usage를 무시하여 발생하는 **인증서 불법 용도 전용 및 MITM** | **RFC 5280 검증 엔진에 EKU(id-kp-serverAuth) 및 KeyUsage(digitalSignature) 필수 검사** | 인가되지 않은 용도의 인증서 전용 차단 및 엄격한 보안 컴플라이언스 준수 |
| 인증서 주체 식별 시 레거시 Common Name(CN)만 확인하여 발생하는 **도메인 스푸핑 위협** | **Common Name(CN) 의존 완전 폐기 및 RFC 6125 SAN(Subject Alternative Name) 강제** | FQDN 다중 도메인 및 와일드카드 검증 무결성 100% 확보 |
| 사설 인증서 발급 시 Basic Constraints 누락으로 최종 단말이 **가짜 하위 CA 행세를 하는 위험** | 엔드포인트 인증서 발급 시 **`Basic Constraints: critical, CA:FALSE` 강제 적용** | 비인가 하위 인증서 임의 발행 원천 차단 및 PKI 신뢰 체인 보호 |

#### 한줄 요약
- EKU/KeyUsage로 용도 전용을 막고, SAN 필드로 도메인을 검증하며, Basic Constraints로 가짜 CA를 차단한다.

## Ⅶ. 결론

- 글로벌 인터넷 신뢰 통신의 핵심 데이터 규격인 **ITU-T X.509 v3 인증서**는 제로 트러스트 아키텍처의 엔드포인트 신원 증명과 mTLS 상호 인증의 기본 표준이며, 실무 운영 시 **RFC 5280 경로 검증 규칙 준수**, **SAN 기반 도메인 바인딩**, **엄격한 EKU 용도 제한**, **ACME 기반 자동 갱신 체계**를 통합 구현하여 완결성 높은 고신뢰 인증 인프라를 완성

#### 한줄 요약
- ASN.1 DER 표준 포맷과 CA 전자서명 및 엄격한 확장 필드 검증을 통해 무결점 X.509 신원 증명을 구현한다.
