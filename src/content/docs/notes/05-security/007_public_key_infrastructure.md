---
sidebar:
  order: 7
  label: "007. PKI 공개키 기반구조"
  badge:
    text: "기출 · 70%"
    variant: note
title: "공개키 신뢰 사슬 및 인증서 생명주기 관리 : PKI"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 7
extra:
  question_no: "7"
  source_status: "기출"
  source_history: "120회, 138회"
  priority: 70
  priority_note: "Root CA/Intermediate CA 계층 신뢰 체인(RFC 5280), RA의 소유권 증명(PoP), CRL/OCSP 폐기 및 X.509 수명주기"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PKI (Public Key Infrastructure)**: 공개키가 특정 주체의 소유임을 보증하기 위해 X.509 인증서의 생성, 발급, 검증, 폐기 전 생애주기를 관리하는 신뢰 프레임워크.
- **Chain of Trust (신뢰 체인, RFC 5280)**: 최상위 Root CA부터 중간 CA를 거쳐 최종 엔티티 인증서까지 전자서명으로 이어지는 인증 경로.

</details>

- 정의/개념: 비대칭 공개키에 신원을 바인딩하여 공인 CA의 전자서명으로 공인하는 **X.509 인증서 발급·관리 체계와 루트 신뢰점 기반의 종합 공개키 신뢰 인프라**
- 배경/필요성: 비대칭 공개키 단독 사용 시의 **소유자 신원 확인 불가, 공격자의 위조 공개키 중간자 바꿔치기(MITM) 및 도청 방어 불가**

#### 한줄 요약
- CA 전자서명과 X.509 인증서 체인을 통해 공개키의 소유권을 공인하고 중간자 공격을 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Proof of Possession (PoP, 소유권 증명)**: 인증서 신청자가 제출한 공개키에 대응하는 개인키를 실제로 소유하고 있음을 증명하기 위해 CSR을 자체 개인키로 서명하는 절차.
- **Trust Anchor (신뢰 앵커)**: OS나 웹 브라우저에 기본 내장되어 별도의 상위 검증 없이 무조건 신뢰하는 최상위 Root CA 인증서.

</details>

- **계층적 신뢰 체인 모델(Hierarchical Trust Model)**: 최상위 **오프라인 Root CA와 온라인 Intermediate CA 계층 분리로 침해 범위 최소화**
- **인증서 신청 시 소유권 증명(PoP)**: CSR(PKCS#10) 제출 시 **개인키 전자서명을 검증하여 타인의 공개키 도용 방지**
- **실시간 폐기 상태 검증 체계**: CRL 파일 배포 및 **OCSP/OCSP Stapling을 통해 폐기된 무효 인증서 실시간 차단**

#### 한줄 요약
- 계층적 신뢰 모델, CSR 소유권 증명(PoP), 실시간 CRL/OCSP 폐기 검증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RA (Registration Authority)**: 신청자의 신원과 도메인 소유권을 실질적으로 심사하는 등록 대행 기관.

</details>

```text
[PKI 계층적 인증서 발급 및 검증 토폴로지]
|-- Offline Root CA (최상위 신뢰 앵커: 물리적 Air-Gap 격리 보관, 자체 서명 Root 인증서)
`-- Issuing / Intermediate CA (온라인 발급 CA: HSM 기반 X.509 v3 서명 발급)
|   |-- RA (Registration Authority: 도메인 소유권 심사, CSR PoP 검증)
|   `-- Certificate Repository (CRL 배포점 & OCSP Responder)
`-- End-Entity (서버/클라이언트: X.509 인증서 수취 및 TLS 통신 제시)
`-- Trust Store (클라이언트 OS/브라우저 내장 Root CA 번들 기반 경로 검증)
```

선의 의미: 신청자의 CSR이 RA의 신원 검증을 통과한 후 발급 CA의 HSM 서명을 거쳐 X.509 인증서로 발행되고 최상위 Root CA가 신뢰의 앵커를 제공하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **등록기관 (RA)** | 신청자의 실명·도메인 유효성 심사, **CSR의 PoP 서명 검증 및 발급 승인** | ACME / RFC 4210 |
| **발급 인증기관 (CA)**| 승인된 신청자에게 **CA 개인키(HSM)로 서명된 X.509 인증서 발행** | RFC 5280 |
| **최상위 루트 CA (Root)**| 전체 PKI의 **신뢰 기준점(Trust Anchor)으로 하위 중간 CA 인증서만 서명** | Offline Air-Gap |
| **인증서 저장소** | 발급된 인증서, **CRL(폐기 목록 파일) 및 OCSP 실시간 응답 서비스 제공** | LDAP / HTTP |
| **신뢰 저장소 (Trust Store)**| 클라이언트 OS 및 브라우저에 **사전 탑재된 공인 Root CA 인증서 번들** | Windows / NSS |

#### 한줄 요약
- 등록기관(RA), 발급 CA, 최상위 루트 CA, 폐기 저장소(CRL/OCSP), 클라이언트 신뢰 저장소가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Path Validation Algorithm (경로 검증 알고리즘, RFC 5280)**: 엔드 엔티티 인증서부터 Root CA까지 서명 체인, 유효기간, Basic Constraints, Key Usage, 폐기 상태를 순차 검증하는 절차.

</details>

```text
PKI CSR 신청, 신원 심사, X.509 발급 및 체인 경로 검증 파이프라인
        │
   1. [CSR 생성 및 제출] 신청자가 키 쌍을 생성하고 공개키와 신원 정보를 담은 CSR을 RA에 제출
        │
   2. [신원 심사 및 PoP 검증] RA가 도메인 제어(ACME) 및 개인키 소유권(PoP)을 심사 후 승인
        │
   3. [X.509 전자서명 발급] 발급 CA가 HSM 내부 개인키로 서명하여 X.509 v3 인증서 생성 및 교부
        │
   4. [체인 경로 역추적 검증] 클라이언트가 서버 인증서부터 로컬 Root CA까지 서명 체인을 순차 검증
        │
   ▼
5. [OCSP 폐기 확인 및 통신] OCSP로 폐기 여부 조회 후 정상 시 공개키를 신뢰하고 TLS 보안 채널 수립
```

#### 한줄 요약
- CSR 제출 → RA 신원 심사 → CA 전자서명 발급 → 클라이언트 체인 경로 검증 → OCSP 폐기 확인 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Web PKI** vs **Private PKI (사설 PKI)**.

</details>

| 비교 항목 | 글로벌 공개 웹 PKI (Web PKI) | 사설 엔터프라이즈 PKI (Private PKI) |
|:---|:---|:---|
| **신뢰 기준점 (Trust Anchor)**| **OS/브라우저에 기본 탑재된 상용 Root CA** | **기업 내부에서 자체 생성하여 단말에 배포한 사설 Root CA** |
| **발급 및 운영 비용** | 인증서당 유료 과금 (또는 Let's Encrypt 무료) | **초기 구축 후 무제한 무료 발급** |
| **적용 영역** | **대고객 HTTPS 웹 서비스, 공인 이메일(S/MIME)** | **사내 인트라넷, 마이크로서비스 mTLS, 사내 VPN, IoT** |
| **운영 통제권 및 유연성** | CA/Browser 포럼의 엄격한 규정 준수 (수명 90일 제한) | **인증서 프로파일, 수명, 확장 필드 기업 맞춤형 통제** |
| **외부 접속 호환성** | 전 세계 모든 기기에서 경고창 없이 자동 신뢰 | **사설 Root CA 미설치 외부 단말 접속 시 보안 경고 발생** |

#### 한줄 요약
- 공개 웹 PKI는 글로벌 범용 신뢰용, 사설 PKI는 내부 통제 및 mTLS 마이크로서비스용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Certificate Transparency (CT, RFC 6962)**: CA가 인증서를 발행할 때마다 공개된 불변 분산 로그에 기록하여 부정 발급을 전 세계에 실시간 공개하는 감사 체계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공인 CA 침해 또는 내부자 실수로 인한 **위조/부정 인증서 몰래 발급 사고** | **`RFC 6962 인증서 투명성(CT) 로그 모니터링` 및 CAA(DNS) 레코드 구성** | 도메인 부정 발급 실시간 탐지 및 미승인 CA 발급 차단 |
| Root CA 개인키 온라인 노출로 인한 **전사 신뢰 기준점 붕괴(Total Compromise)** | **`Root CA 오프라인(Air-Gapped) 유지` 및 HSM 키 분할(M of N Quorum)** | Root CA 키 탈취 원천 방어 및 신뢰 사슬 보호 |
| 인증서 만료일 관리 실패로 인한 **전사 서비스 접속 불가 및 대규모 장애** | **`ACME 프로토콜(RFC 8555) 기반 인증서 자동 발급·갱신(Cert-Manager)`** | 만료 휴먼 에러 0% 달성 및 무중단 인증서 생애주기 자동화 |
| 폐기 목록(CRL) 파일 비대화로 인한 네트워크 대역폭 낭비 및 검증 지연 | **`OCSP Stapling (TLS 인증서 번들링)`** 기술 전면 활성화 | 클라이언트의 폐기 서버 직접 질의 제거 및 TLS 지연 극소화 |

#### 한줄 요약
- CT 로그로 오발급을 감시하고, Air-Gap Root CA로 키를 보호하며, ACME 자동화로 만료 장애를 방지한다.

## Ⅶ. 결론

- 초연결 디지털 사회의 모든 보안 통신과 신원 증명의 신뢰 기반인 **PKI(공개키 기반구조)는 제로 트러스트(mTLS), 전자서명, 공급망 보안(SBOM 서명)의 핵심 인프라**이며, 실무 구현 시 **오프라인 Root CA와 온라인 Issuing CA의 계층적 분리, ACME 기반 인증서 자동 갱신 체계, CT 로그 모니터링 및 실시간 OCSP Stapling**을 통합 구현하여 완결성 높은 고신뢰 보안 인프라 완성

#### 한줄 요약
- PKI는 계층적 CA 신뢰 체인과 엄격한 수명주기 관리 및 ACME 자동화를 통해 인터넷 전반의 디지털 신뢰를 보장하는 핵심 인프라다.