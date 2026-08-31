---
sidebar:
  order: 9
  label: "009. CA 인증 기관•인증서 발급 절차"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증기관 아키텍처 및 발급 절차 : CA"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 인터넷 참여자가 상대방의 신원과 도메인 소유권을 개별적으로 대면 심사하거나 검증하는 것은 막대한 인력과 시간이 소요되어 실시간 통신 환경에서 불가능하며, 단일 루트 인증기관이 전 세계 모든 최종 인증서를 직접 온라인으로 발행할 경우 루트 개인키 유출 시 글로벌 전체 신뢰 체계가 일시에 붕괴되는 치명적인 위험을 안고 있음에 따라, 최상위 Root CA, 중간 Intermediate CA, 발급 Issuing CA의 3계층 위임 모델과 공인된 인증 정책/준칙(CP/CPS: RFC 3647)을 준수하는 인증기관(CA: Certificate Authority) 아키텍처를 도입하여 **오프라인 루트 기반의 안전한 신뢰 격리, 표준 ACME(RFC 8555) 기반 인증서 발급/갱신 자동화 및 위조·오발급 방지를 위한 투명한 공인 인증 체계**를 달성할 필요

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
- 3계층 분리는 서명 능력을 나눠 Root 침해 시의 전면 재배포 비용을 하위 CA 폐기로 낮추는 대신, 검증자가 매번 더 긴 경로를 따라가는 비용을 감수한 구조다.

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
- CA를 신뢰한다는 전제는 CA 자신이 검증할 수 없으므로, 발급 행위의 감시는 CA 바깥의 공개 CT 로그 계층에 맡겨 오발급을 사후에라도 드러나게 한다.

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
- SCT를 최종 서명 전에 미리 받아 인증서 안에 박아 넣기 때문에, 클라이언트는 접속할 때마다 로그 서버에 따로 물어보는 비용 없이 감사 기록 여부를 확인할 수 있다.

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

- 전 세계 인터넷 생태계의 모든 공개키에 신원과 법적 공증력을 부여하는 **글로벌 웹 보안 및 제로 트러스트 인프라의 가장 핵심적인 신뢰 발행 주체(CA/B Forum 표준 및 IETF RFC 3647)**로 확고히 기능하고 있으며, 클라우드 네이티브 ACME 기반 초단기 인증서(Short-Lived Certs) 및 분산 신원(DID) 연계로 진화하는 가운데, 실무 CA 인프라 설계 및 운영 시에는 **네트워크 단절(Air-Gap) 금고 내 오프라인 Root CA와 FIPS 140-3 Level 3 HSM 기반 발급 키 격리, 수동 갱신 실패로 인한 서비스 다운을 방지하는 ACME(Let's Encrypt / Cert-Manager) 완전 자동화, 타 CA에 의한 부정 인증서 오발급을 차단하는 DNS CAA 레코드 설정 및 인증서 투명성(Certificate Transparency / SCT) 실시간 감사 모니터링**을 결합하여 완벽한 인증기관 신뢰성을 완성

#### 한줄 요약
- CA는 3계층 위임 모델과 HSM 격리 및 ACME/CT 감시 체계를 결합하여 고신뢰 인증서 발급 환경을 구현하는 공인 주체다.
