---
sidebar:
  order: 9
  label: "009. CA 인증 기관•인증서 발급 절차"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증기관 아키텍처 및 발급 절차 : CA"
date: "2026-08-26T14:42:00+09:00"
tags:
  - "notes-security"
weight: 9
extra:
  question_no: "9"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "Root CA/Intermediate CA/Issuing CA 3계층 구조, CP/CPS(RFC 3647), CSR(PKCS#10) 및 자동화 ACME(RFC 8555)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CA (Certificate Authority, 인증기관)**: 신청자의 신원과 공개키 소유권을 검증하고 자신의 개인키로 서명된 X.509 인증서를 발행하는 공인 신뢰 주체.
- **CP & CPS (RFC 3647)**: 인증서 발급에 요구되는 보안 등급 기준인 CP(인증 정책)와 이를 이행하는 운영 절차 규정인 CPS(인증업무 준칙).

</details>

- 정의/개념: **CP·CPS**에 따라 인증서를 발급·폐기하는 신뢰 주체
- 배경/필요성: 중앙 검증 없이는 **공개키와 신원 결속 불가**

#### 한줄 요약
- 3계층 CA 구조와 엄격한 CP/CPS 기준을 통해 X.509 인증서의 신뢰성과 무결성을 공인한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Air-Gapped Offline Root CA**: 네트워크가 물리적으로 단절된 안전 금고 내에 보관되어 최상위 서명키 탈취를 원천 차단하는 루트 인증기관.
- **ACME Protocol (RFC 8555)**: 웹 서버와 CA 간에 DNS/HTTP 챌린지를 통해 사람의 개입 없이 인증서를 자동 발급·갱신하는 표준 프로토콜.

</details>

- Root·Intermediate·Issuing의 **3계층 역할 분리**
- RFC 3647 기반 **CP·CPS 운영 통제**
- **ACME** 기반 도메인 검증·발급·갱신 자동화

#### 한줄 요약
- 3계층 위임 신뢰 모델, CP/CPS 거버넌스, ACME 발급 자동화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CT Log (Certificate Transparency, RFC 6962)**: CA가 발급한 모든 인증서의 해시값을 공개 머클 트리에 영구 기록하여 오발급을 감시하는 분산 원장.

</details>

```text
CA
|-- Root CA
|   `-- Intermediate CA
|       `-- Issuing CA
|           |-- RA
|           |-- HSM
|           `-- CT Log Client
```

선의 의미: 오프라인 Root CA가 최상위 신뢰를 제공하고 Intermediate CA가 정책을 통제하며 온라인 Issuing CA/RA가 가입자의 인증서를 발급하고 CT 로그에 기록하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Root CA** | 신뢰 앵커와 하위 CA 서명 |
| **Intermediate CA** | 정책·경로 제약 위임 |
| **Issuing CA** | 엔드 엔티티 인증서 발급 |
| **RA** | 신원·도메인·PoP 심사 |
| **HSM** | CA 개인키 보관과 서명 연산 |
| **CT Log Client** | 사전 인증서 제출과 SCT 수신 |

#### 한줄 요약
- 오프라인 Root CA, 정책 중간 CA, 등록기관(RA), 온라인 Issuing CA, CT Log 서버가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SCT (Signed Certificate Timestamp)**: 공공 CT Log 서버가 해당 인증서를 감사 원장에 정상 등록했음을 보증하는 암호 영수증 토큰.

</details>

```text
ACME 도메인 검증, CT Log 등록 및 HSM 최종 서명 발급 파이프라인
        │
       [CSR 작성 및 전송]
        │
   1. [ACME 도메인 챌린지]
        │
   2. [CT Log 사전 제출]
        │
   3. [SCT 토큰 임베딩]
        │
   ▼
   4. [HSM 전자서명]
        │
       [인증서 교부]
```

- 1. ACME 도메인 챌린지
- 2. CT Log 사전 제출
- 3. SCT 토큰 임베딩
- 4. HSM 전자서명

#### 한줄 요약
- CSR 검증 후 CT Log의 SCT를 포함해 HSM으로 서명하고 인증서를 교부한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **수동 웹 발급** vs **SCEP/EST (기기 등록)** vs **ACME (클라우드 웹 자동화)**.

</details>

| 비교 항목 | 수동 웹 포털 발급 (Legacy) | SCEP / EST 프로토콜 (RFC 7030) | ACME 자동화 프로토콜 (RFC 8555) |
|:---|:---|:---|:---|
| 발급 트리거 | 관리자 CSR 제출 | 단말·MDM 등록 | 서버·Controller 자동 요청 |
| 검증 방식 | 서류·조직 심사 | 기존 신뢰·등록 정보 | **DNS-01·HTTP-01** |
| 갱신 방식 | 수동 절차 | 단말 관리 연동 | **ACME 자동 갱신** |
| 주요 대상 | 수동 심사 인증서 | Wi-Fi·VPN 단말 | HTTPS·Kubernetes Ingress |

#### 한줄 요약
- 수동 발급은 고비용 EV 전용, SCEP/EST는 MDM 단말 전용, ACME는 현대 클라우드 웹 표준 자동화 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DNS CAA (Certification Authority Authorization, RFC 8659)**: 도메인 소유자가 자신의 DNS에 특정 CA(예: `letsencrypt.org`)만 인증서를 발급할 수 있도록 명시하여 타 CA를 통한 위조 발급을 차단하는 레코드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 타 CA를 통한 **부정 인증서 발급** | **CAA·CT Log** 모니터링 | 발급 CA 제한·오발급 탐지 |
| Issuing CA 개인키 유출 | **HSM 격리·하위 CA 폐기** | Root 신뢰 범위 보호 |
| 갱신 누락으로 서비스 중단 | **Cert-Manager·ACME** 자동 갱신 | 수동 만료 오류 완화 |
| CRL 생성 지연 | 단축 CRL 주기와 **OCSP 동기화** | 폐기 정보 전파 지연 완화 |

#### 한줄 요약
- CAA/CT 로그로 부정 발급을 차단하고, HSM 격리로 키를 보호하며, ACME 자동화로 만료 장애를 예방한다.

## Ⅶ. 결론

- 웹 자동 발급은 **ACME**, 관리 단말 등록은 **EST** 선택

#### 한줄 요약
- CA는 3계층 위임 모델과 HSM 격리 및 ACME/CT 감시 체계를 결합하여 고신뢰 인증서 발급 환경을 구현하는 공인 주체다.
