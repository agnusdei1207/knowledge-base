---
sidebar:
  order: 8
  label: "008. X.509 인증서"
  badge:
    text: "기출 · 70%"
    variant: note
title: "디지털 신원 증명 표준 포맷 : ITU-T X.509 v3 인증서"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: **TBSCertificate**·CA 서명 기반 **X.509 v3** 공개키 증명서
- 배경/필요성: 네트워크를 통해 전달되는 원시 비트열 형태의 공개키는 소유자의 신원(주체), 유효기간, 허용된 암호화 용도(서명/키교환) 및 발급 기관에 대한 구조화된 메타데이터를 포함하지 않아 주체 식별 및 권한 제약 검증이 불가능한 한계를 가짐에 따라, ITU-T 및 IETF RFC 5280 표준에 따라 공개키와 주체 식별 정보(Subject), 발급자(Issuer), 유효기간(Validity) 및 확장 필드(SAN, Key Usage, Basic Constraints)를 ASN.1 DER 바이너리 구조로 캡슐화하고 발급 CA의 전자서명으로 봉인한 X.509 v3 디지털 인증서 포맷을 도입하여 공개키와 신원의 암호학적 결속(Binding), 다중 도메인(SAN) 및 용도별 엄격한 권한 제약 집행, 글로벌 이기종 시스템 간 완벽한 상호운용성을 달성할 필요

#### 한줄 요약
- TBS 구조체와 CA 전자서명을 결합하여 공개키의 소유권과 신원을 암호학적으로 증명한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SAN (Subject Alternative Name)**: 단일 인증서로 복수의 서브도메인(예: `*.domain.com`) 및 IP 주소를 안전하게 바인딩하는 표준 확장 필드.
- **Basic Constraints**: 해당 인증서가 하위 인증서를 발행할 수 있는 CA 인증서인지(`CA:TRUE`) 최종 단말 인증서인지(`CA:FALSE`) 정의하는 제약 필드.

</details>

- ASN.1 DER 기반 결정적 바이너리 인코딩
- **SAN**·Key Usage·**Basic Constraints** 확장 제어
- 상위 CA 공개키 기반 SignatureValue 체인 검증

#### 한줄 요약
- DER의 결정적 인코딩은 사람이 읽기 어려운 대신 같은 인증서가 항상 같은 바이트열이 되게 하여 서명 대상이 흔들릴 여지를 없앤 선택이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SPKI (Subject Public Key Info)**: 인증서 소유자의 공개키 알고리즘(OID)과 공개키 원시 비트열을 담고 있는 핵심 필드.

</details>

```text
[X.509 v3 인증서]
  │
  ├─ [TBSCertificate (서명 대상)]
  │    ├─ 기본 메타데이터 (Version/SN/Validity)
  │    ├─ 주체 및 발급자 (Subject/Issuer DN)
  │    ├─ 공개키 정보 (SPKI: OID & Key)
  │    └─ 표준 확장 필드 (SAN/KeyUsage/Basic)
  │
  └─ [전자서명 블록]
       ├─ 서명 알고리즘 (AlgorithmIdentifier)
       └─ 서명값 (CA 개인키 SignatureValue)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Metadata | 버전·일련번호·유효기간 정의 |
| Issuer and Subject | 발급자와 주체 식별 |
| **SPKI** | 공개키 알고리즘과 키 보관 |
| **Basic Constraints** | CA 여부와 경로 길이 제한 |
| SAN and Key Usage | 이름과 허용 용도 제한 |
| AIA and CDP | OCSP·CRL 위치 제공 |
| Signature | TBSCertificate의 CA 서명 제공 |

#### 한줄 요약
- 서명은 TBSCertificate 전체를 덮으므로 확장 필드에 적힌 제약도 함께 봉인되지만, 그 제약을 실제로 강제하는 책임은 검증자 구현에 남아 필드만으로는 아무것도 막지 못한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EKU (Extended Key Usage)**: 인증서가 쓰일 수 있는 목적(serverAuth, clientAuth, codeSigning 등)을 OID 목록으로 제한하는 확장 필드로, 검증자가 접속 목적과 대조해 다른 용도로 발급된 인증서의 전용을 거부하게 함.

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
- 4. 확장 필드(**EKU**·Basic Constraints) 및 폐기 검증

#### 한줄 요약
- 앞의 네 단계는 수신한 인증서만으로 국소 판정이 끝나지만 마지막 폐기 확인만 외부 응답에 의존하므로, 이 단계의 실패를 통과로 볼지 차단으로 볼지가 가용성과 안전성을 가르는 지점이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DV (Domain Validation, 도메인 검증)**: CA가 DNS TXT 레코드나 HTTP 파일 챌린지로 신청자의 도메인 통제권만 확인해 발급하는 등급으로, 조직 실재는 검증하지 않아 사람 개입 없는 ACME 자동화가 가능함.

</details>

| 비교 항목 | 도메인 검증 (DV: Domain Validation) | 조직 검증 (OV: Organization Validation) | 확장 검증 (EV: Extended Validation) |
|:---|:---|:---|:---|
| 신원 심사 | 도메인 제어 확인 | 조직 실재 확인 | 강화된 조직 실재 확인 |
| 자동화 | ACME **DV**에 적합 | CA 절차에 좌우 | CA 절차에 좌우 |
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
| EKU 무시로 **Key Usage Abuse** | **EKU**·Key Usage 검증 | 허용 연산 제한 |
| CN만 확인해 도메인 스푸핑 | RFC 6125 **SAN** 검증 | 접속 이름과 인증서 결합 |
| 제약 누락으로 가짜 하위 CA | **Basic Constraints** CA:FALSE | 엔드 엔티티 발급 제한 |
| 폐기 확인 실패 | OCSP Must-Staple(Hard-Fail) | 폐기 상태 미확인 접속 제한 |

#### 한줄 요약
- 네 문제는 모두 인증서에 적힌 제약을 검증자가 읽지 않아 생기므로, X.509의 안전성은 발급 프로파일보다 검증 구현이 확장 필드를 얼마나 강제하느냐에 달린다.

## Ⅶ. 결론

- 인터넷의 모든 엔드포인트(웹 서버, 클라이언트, IoT 기기, 컨테이너)의 신원을 암호학적으로 증명하는 전 세계 표준 공인 디지털 신분증이자 PKI 생태계의 절대적 핵심 데이터 규격(ITU-T X.509 v3 / IETF RFC 5280)으로 확고히 자리 잡았으며, 양자내성 복합 알고리즘(Composite PQC X.509)으로 진화하는 가운데, 실무 X.509 인증서 프로파일 설계 및 검증 시에는 단일 도메인(CN) 폐지 및 RFC 6125 표준 SAN(Subject Alternative Name) 기반 다중 FQDN 바인딩, 일반 서버 인증서의 불법 하위 CA 생성을 원천 차단하는 Basic Constraints(CA:FALSE) 및 용도 제한(Key Usage/EKU) 강제, 실시간 폐기 검증 오버헤드를 제거하는 OCSP Stapling 및 Must-Staple 확장 적용을 결합하여 완벽한 인증서 무결성을 완성

#### 한줄 요약
- 인증서 프로파일은 SAN·EKU·Basic Constraints 세 확장을 최소 권한으로 조이는 것이 기본이고, 여기서 느슨하게 둔 필드가 곧 공격자의 전용 경로가 된다.
