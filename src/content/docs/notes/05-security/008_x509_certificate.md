---
sidebar:
  order: 8
  label: "008. X.509 인증서"
  badge:
    text: "기출 · 70%"
    variant: note
title: "디지털 신원 증명 표준 포맷 : ITU-T X.509 v3 인증서"
date: "2026-08-26T14:33:08+09:00"
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

- 정의/개념: **TBSCertificate·CA 서명** 기반 공개키 증명서
- 배경/필요성: 공개키만으로는 **주체·용도·유효기간 확인 불가**

#### 한줄 요약
- TBS 구조체와 CA 전자서명을 결합하여 공개키의 소유권과 신원을 암호학적으로 증명한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SAN (Subject Alternative Name)**: 단일 인증서로 복수의 서브도메인(예: `*.domain.com`) 및 IP 주소를 안전하게 바인딩하는 표준 확장 필드.
- **Basic Constraints**: 해당 인증서가 하위 인증서를 발행할 수 있는 CA 인증서인지(`CA:TRUE`) 최종 단말 인증서인지(`CA:FALSE`) 정의하는 제약 필드.

</details>

- **ASN.1 DER** 기반 결정적 바이너리 인코딩
- **SAN·Key Usage·Basic Constraints** 확장 제어
- 상위 CA 공개키 기반 **SignatureValue 체인 검증**

#### 한줄 요약
- ASN.1 DER 인코딩, v3 확장 필드 정밀 제어, 암호학적 체인 검증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SPKI (Subject Public Key Info)**: 인증서 소유자의 공개키 알고리즘(OID)과 공개키 원시 비트열을 담고 있는 핵심 필드.

</details>

```text
X.509 Certificate
|-- TBSCertificate
|   |-- Metadata
|   |-- Issuer and Subject
|   |-- SPKI
|   |-- Basic Constraints
|   |-- SAN and Key Usage
|   `-- AIA and CDP
`-- Signature
```

선의 의미: TBSCertificate 블록 전체를 해싱한 후 CA의 개인키로 서명하여 SignatureValue를 생성하고 클라이언트는 Issuer 공개키로 이를 검증하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Metadata** | 버전·일련번호·유효기간 정의 |
| **Issuer and Subject** | 발급자와 주체 식별 |
| **SPKI** | 공개키 알고리즘과 키 보관 |
| **Basic Constraints** | CA 여부와 경로 길이 제한 |
| **SAN and Key Usage** | 이름과 허용 용도 제한 |
| **AIA and CDP** | OCSP·CRL 위치 제공 |
| **Signature** | TBSCertificate의 CA 서명 제공 |

#### 한줄 요약
- TBSCertificate(기본 정보, SPKI, 확장 필드)와 CA 전자서명(SignatureValue)이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RFC 5280 5단계 검증**: 1. 유효기간 점검, 2. SAN 도메인 대조, 3. CA 서명 체인 역추적, 4. EKU/KeyUsage 제약 확인, 5. OCSP/CRL 폐기 상태 판정.

</details>

```text
X.509 인증서 수신, 도메인 대조, 체인 역추적 및 OCSP 폐기 검증 파이프라인
        │
       [인증서 체인 수신]
        │
   1. [유효기간 검증]
        │
   2. [SAN 이름 대조]
        │
   3. [CA 서명 체인 검증]
        │
   ▼
   4. [확장 필드 및 폐기 검증]
```

- 1. 유효기간 검증
- 2. SAN 이름 대조
- 3. CA 서명 체인 검증
- 4. 확장 필드 및 폐기 검증

#### 한줄 요약
- 인증서 수신 → 유효기간 점검 → SAN 도메인 대조 → CA 서명 체인 검증 → OCSP 폐기 확인 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DV (도메인 검증)** vs **OV (조직 검증)** vs **EV (확장 검증)**.

</details>

| 비교 항목 | 도메인 검증 (DV: Domain Validation) | 조직 검증 (OV: Organization Validation) | 확장 검증 (EV: Extended Validation) |
|:---|:---|:---|:---|
| 신원 심사 | 도메인 제어 확인 | 조직 실재 확인 | 강화된 조직 실재 확인 |
| 자동화 | **ACME DV**에 적합 | CA 절차에 좌우 | CA 절차에 좌우 |
| 주체 정보 | 도메인 중심 | 조직 정보 포함 | 검증된 조직 정보 포함 |
| 주요 대상 | 일반 HTTPS·API | 조직 신원 표시 요구 | 강화된 심사 요구 |

#### 한줄 요약
- DV는 도메인 자동 검증용, OV는 기업 실존 검증용, EV는 금융/공공 최고 수준 검증용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Key Usage Abuse**: 클라이언트 인증용(ClientAuth)으로 발급된 인증서를 가짜 웹 서버의 TLS 인증서(ServerAuth)로 전용하여 중간자 공격을 시도하는 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| EKU 무시로 **인증서 용도 전용** | **EKU·Key Usage** 검증 | 허용 연산 제한 |
| CN만 확인해 **도메인 스푸핑** | RFC 6125 **SAN 검증** | 접속 이름과 인증서 결합 |
| 제약 누락으로 가짜 하위 CA | **Basic Constraints CA:FALSE** | 엔드 엔티티 발급 제한 |
| 폐기 확인 실패 | **OCSP Must-Staple·Hard-Fail** | 폐기 상태 미확인 접속 제한 |

#### 한줄 요약
- EKU/KeyUsage로 용도 전용을 막고, SAN 필드로 도메인을 검증하며, Basic Constraints로 가짜 CA를 차단한다.

## Ⅶ. 결론

- 일반 HTTPS는 **DV**, 조직 신원 심사는 **OV·EV** 선택

#### 한줄 요약
- X.509 v3 인증서는 ASN.1 DER 표준 포맷과 CA 전자서명 및 엄격한 확장 필드 검증을 통해 무결점 디지털 신원 증명을 구현하는 핵심 규격이다.
