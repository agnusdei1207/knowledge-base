---
sidebar:
  order: 8
  label: "008. X.509 인증서"
  badge:
    text: "기출 · 70%"
    variant: note
title: "디지털 신원 증명 표준 포맷 : ITU-T X.509 v3 인증서"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 8
extra:
  question_no: "8"
  source_status: "기출"
  source_history: "120회, 138회"
  priority: 70
  priority_note: "TBSCertificate 구조, Subject/Issuer/Validity, SAN/KeyUsage/BasicConstraints 확장 필드(RFC 5280)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **X.509 v3 (RFC 5280)**: 비대칭 공개키에 신원 정보, 유효기간, 확장 필드를 결합하고 CA의 전자서명을 첨부한 국제 표준 디지털 증명서.
- **TBSCertificate (To-Be-Signed Certificate)**: 인증서 내에서 발급자 CA의 전자서명이 적용되는 원시 데이터 블록.

</details>

- 정의/개념: ASN.1 DER 구조의 **TBSCertificate에 인증기관(CA)의 개인키 전자서명을 결합하여 공개키의 소유권을 공인하는 국제 표준 디지털 증명서**
- 배경/필요성: 공개키 단독 배포 시의 **공개키 주체 신원 확인 불가, 비인가 용도 오남용 및 중간자 공격(MITM) 방어 불가**

#### 한줄 요약
- TBS 구조체와 CA 전자서명을 결합하여 공개키의 소유권과 신원을 암호학적으로 증명한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SAN (Subject Alternative Name)**: 단일 인증서로 복수의 서브도메인(예: `*.domain.com`) 및 IP 주소를 안전하게 바인딩하는 표준 확장 필드.
- **Basic Constraints**: 해당 인증서가 하위 인증서를 발행할 수 있는 CA 인증서인지(`CA:TRUE`) 최종 단말 인증서인지(`CA:FALSE`) 정의하는 제약 필드.

</details>

- **ASN.1 DER 기반 엄격한 바이너리 인코딩**: 모호성 없는 일관된 바이트 구조를 통해 **플랫폼 독립적 디지털 서명 검증 보장**
- **v3 확장 필드를 통한 정밀 제어**: SAN(다중 도메인), **Key Usage(용도 제한), Basic Constraints(경로 제어) 기능 제공**
- **암호학적 서명 체인 검증**: 상위 CA의 공개키로 **SignatureValue를 검증하여 Root CA까지의 무결성 증명**

#### 한줄 요약
- ASN.1 DER 인코딩, v3 확장 필드 정밀 제어, 암호학적 체인 검증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SPKI (Subject Public Key Info)**: 인증서 소유자의 공개키 알고리즘(OID)과 공개키 원시 비트열을 담고 있는 핵심 필드.

</details>

```text
[X.509 v3 인증서 내부 ASN.1 DER 구조]
|-- TBSCertificate (To-Be-Signed 원시 데이터 블록)
|   |-- Version (v3: 0x02) & Serial Number (CA 내 유일값)
|   |-- Signature Algorithm Identifier (ecdsa-with-SHA256)
|   |-- Issuer DN (발행 CA 식별자: C=KR, O=KISA, CN=Root CA)
|   |-- Validity (유효기간: NotBefore ~ NotAfter)
|   |-- Subject DN (소유자 식별자) & SubjectPublicKeyInfo (소유자 공개키)
|   `-- Extensions (v3 확장 필드)
|       |-- Basic Constraints (critical, isCA=FALSE)
|       |-- Key Usage (digitalSignature, keyEncipherment) & EKU (serverAuth)
|       |-- SAN (Subject Alternative Name: DNS:api.domain.com, IP:1.1.1.1)
|       `-- AIA (OCSP URL) & CDP (CRL Distribution Points URL)
`-- SignatureAlgorithm & SignatureValue (CA 개인키로 서명된 비트열)
```

선의 의미: TBSCertificate 블록 전체를 해싱한 후 CA의 개인키로 서명하여 SignatureValue를 생성하고 클라이언트는 Issuer 공개키로 이를 검증하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **기본 메타데이터** | Version(v3), Serial Number, **Validity(유효 시작/만료 시각) 정의** | RFC 5280 Base |
| **발행자 및 주체** | **Issuer(발급 CA 식별자) 및 Subject(소유자 식별자) 명시** | X.500 DN |
| **주체 공개키 (SPKI)**| **AlgorithmIdentifier 및 소유자의 비대칭 공개키 데이터 보관** | Public Key |
| **Basic Constraints** | `critical, CA:FALSE`로 **최종 단말의 불법 하위 CA 인증서 발행 차단** | Path Control |
| **SAN / Key Usage** | **인증서가 유효한 FQDN 목록 및 허용 암호 연산(서명, 암호화) 정의** | Extensions |
| **폐기 배포점 (AIA/CDP)**| **CRL 다운로드 URL(CDP) 및 실시간 OCSP 응답 서버 URL(AIA) 명시** | Revocation Point |

#### 한줄 요약
- TBSCertificate(기본 정보, SPKI, 확장 필드)와 CA 전자서명(SignatureValue)이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RFC 5280 5단계 검증**: 1. 유효기간 점검, 2. SAN 도메인 대조, 3. CA 서명 체인 역추적, 4. EKU/KeyUsage 제약 확인, 5. OCSP/CRL 폐기 상태 판정.

</details>

```text
X.509 인증서 수신, 도메인 대조, 체인 역추적 및 OCSP 폐기 검증 파이프라인
        │
   1. [인증서 체인 수신] 클라이언트가 HTTPS 접속 시 서버로부터 X.509 체인(Server + Intermediate CA) 수신
        │
   2. [1단계: 유효기간 검증] 현재 UTC 시각이 Validity(NotBefore ~ NotAfter) 범위 내인지 확인
        │
   3. [2단계: SAN 도메인 대조] 접속 대상 FQDN이 인증서의 SAN 목록과 일치하는지 대조
        │
   4. [3단계: CA 서명 체인 검증] Intermediate CA의 공개키로 Server 서명 검증 ➔ Root CA까지 반복
        │
   ▼
5. [4단계: 확장 필드 및 폐기 검증] EKU(serverAuth) 확인 및 AIA URL로 OCSP 실시간 폐기 여부 조회 ➔ 통신 개시
```

#### 한줄 요약
- 인증서 수신 → 유효기간 점검 → SAN 도메인 대조 → CA 서명 체인 검증 → OCSP 폐기 확인 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DV (도메인 검증)** vs **OV (조직 검증)** vs **EV (확장 검증)**.

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

- **Key Usage Abuse**: 클라이언트 인증용(ClientAuth)으로 발급된 인증서를 가짜 웹 서버의 TLS 인증서(ServerAuth)로 전용하여 중간자 공격을 시도하는 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 클라이언트가 EKU를 무시하여 발생하는 **인증서 불법 용도 전용 및 MITM** | **`RFC 5280 검증 엔진에 EKU(serverAuth) 및 KeyUsage 필수 검사`** | 비인가 용도 전용 차단 및 보안 컴플라이언스 준수 |
| 인증서 주체 식별 시 레거시 Common Name(CN)만 확인하여 발생하는 **도메인 스푸핑** | **CN 의존 완전 폐기 및 `RFC 6125 SAN(Subject Alternative Name) 강제`** | 다중 도메인 및 와일드카드 검증 무결성 100% 확보 |
| 사설 인증서 발급 시 Basic Constraints 누락으로 **가짜 하위 CA 행세 위험** | 엔드포인트 인증서 발급 시 **`Basic Constraints: critical, CA:FALSE` 강제** | 비인가 하위 인증서 임의 발행 원천 차단 |
| 인증서 폐기(CRL/OCSP) 확인 실패 시 폐기된 탈취 인증서로의 접속 허용 | **`OCSP Must-Staple 확장 필드` 명시 및 클라이언트 하드 페일(Hard-Fail)** | 탈취된 무효 인증서 접속 100% 즉시 차단 |

#### 한줄 요약
- EKU/KeyUsage로 용도 전용을 막고, SAN 필드로 도메인을 검증하며, Basic Constraints로 가짜 CA를 차단한다.

## Ⅶ. 결론

- 글로벌 인터넷 신뢰 통신의 핵심 데이터 규격인 **ITU-T X.509 v3 인증서는 제로 트러스트 아키텍처의 엔드포인트 신원 증명과 mTLS 상호 인증의 기본 표준**이며, 실무 운영 시 **RFC 5280 경로 검증 규칙 준수, SAN 기반 도메인 바인딩, 엄격한 EKU 용도 제한, ACME 기반 자동 갱신 체계**를 통합 구현하여 완결성 높은 고신뢰 인증 인프라 완성

#### 한줄 요약
- X.509 v3 인증서는 ASN.1 DER 표준 포맷과 CA 전자서명 및 엄격한 확장 필드 검증을 통해 무결점 디지털 신원 증명을 구현하는 핵심 규격이다.