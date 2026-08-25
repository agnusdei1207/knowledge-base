---
sidebar:
  order: 9
  label: "009. CA 인증 기관•인증서 발급 절차"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증기관 아키텍처 및 발급 절차 : CA"
date: "2026-08-25T13:00:00+09:00"
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

- 정의/개념: Root CA, Intermediate CA, Issuing CA 3계층 구조 상에서 **CP/CPS 규정에 따라 CSR을 심사하고 X.509 인증서를 발행·폐기하는 공인 신뢰 기관**
- 배경/필요성: 인증서 발급 기관의 신뢰성 검증 체계 부재 시 발생하는 **비인가 가짜 인증서 난립, 주먹구구식 발급 심사 및 글로벌 신뢰 사슬 붕괴**

#### 한줄 요약
- 3계층 CA 구조와 엄격한 CP/CPS 기준을 통해 X.509 인증서의 신뢰성과 무결성을 공인한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Air-Gapped Offline Root CA**: 네트워크가 물리적으로 단절된 안전 금고 내에 보관되어 최상위 서명키 탈취를 원천 차단하는 루트 인증기관.
- **ACME Protocol (RFC 8555)**: 웹 서버와 CA 간에 DNS/HTTP 챌린지를 통해 사람의 개입 없이 인증서를 자동 발급·갱신하는 표준 프로토콜.

</details>

- **3계층 계층형 위임 신뢰 모델**: 오프라인 Root CA, **정책 중간 CA, 온라인 발급 CA로 역할을 분리하여 서명키 위험 격리**
- **엄격한 규정 기반 운영(CP/CPS)**: RFC 3647 표준을 준수하여 **물리적 보안, 감사 로깅, 신원 심사 절차를 공적으로 보증**
- **ACME 기반 인증서 발급 자동화**: RFC 8555 표준을 통해 **90일 단기 인증서의 자동 발급 및 무중단 갱신 실현**

#### 한줄 요약
- 3계층 위임 신뢰 모델, CP/CPS 거버넌스, ACME 발급 자동화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CT Log (Certificate Transparency, RFC 6962)**: CA가 발급한 모든 인증서의 해시값을 공개 머클 트리에 영구 기록하여 오발급을 감시하는 분산 원장.

</details>

```text
[3계층 CA 아키텍처 및 발급 파이프라인]
|-- 1. Offline Root CA (최상위 신뢰 앵커: Air-Gap 격리 보관, 자체 서명 Root 인증서)
`-- 2. Intermediate / Policy CA (정책 중간 CA: 조직/용도별 서명 권한 위임 및 경로 제약)
`-- 3. Online Issuing CA & RA (온라인 발급 기관)
    |-- RA (Registration Authority: 도메인 소유권 ACME Challenge 심사)
    |-- Online HSM (FIPS 140-3: 승인된 End-Entity 인증서 실시간 전자서명)
    `-- CT Log Client (RFC 6962: 발급 전 Pre-certificate 공공 로그 제출 및 SCT 획득)
```

선의 의미: 오프라인 Root CA가 최상위 신뢰를 제공하고 Intermediate CA가 정책을 통제하며 온라인 Issuing CA/RA가 가입자의 인증서를 발급하고 CT 로그에 기록하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **오프라인 Root CA** | 신뢰 기준점(Trust Anchor)으로 **하위 Intermediate CA 인증서만을 서명 교부** | Offline Air-Gap |
| **중간 CA (Intermediate)**| 인증 정책(CP) 집행, **발급 경로 제약 설정 및 도메인/용도별 하위 CA 통제** | RFC 5280 Sub-CA |
| **등록기관 (RA)** | 신청자의 실명·도메인 DNS 검증 및 **CSR 서명의 키 소유권(PoP) 심사** | ACME Server |
| **온라인 Issuing CA** | 승인된 신청자에게 **HSM 내부 개인키로 서명된 최종 단말 인증서 발행** | FIPS 140-3 HSM |
| **CT Log 서버** | 발급된 모든 인증서의 **다이제스트를 공개 머클 트리에 영구 기록** | RFC 6962 CT Log |

#### 한줄 요약
- 오프라인 Root CA, 정책 중간 CA, 등록기관(RA), 온라인 Issuing CA, CT Log 서버가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SCT (Signed Certificate Timestamp)**: 공공 CT Log 서버가 해당 인증서를 감사 원장에 정상 등록했음을 보증하는 암호 영수증 토큰.

</details>

```text
ACME 도메인 검증, CT Log 등록 및 HSM 최종 서명 발급 파이프라인
        │
   1. [CSR 작성 및 전송] 웹 서버가 개인키 생성 후 PKCS#10 CSR을 ACME 클라이언트를 통해 RA로 전송
        │
   2. [ACME 도메인 챌린지] RA가 DNS-01/HTTP-01 챌린지를 발행하여 도메인 소유권 및 DNS CAA 레코드 검증
        │
   3. [CT Log 사전 제출] 검증 통과 후 Issuing CA가 사전 인증서(Pre-cert)를 생성하여 공공 CT Log 제출
        │
   4. [SCT 토큰 임베딩] CT Log 서버로부터 SCT 토큰을 수신하여 인증서 확장 필드에 임베딩
        │
   ▼
5. [HSM 전자서명 및 교부] Issuing CA가 HSM 내부 개인키로 최종 서명 완료 후 웹 서버로 인증서 교부
```

#### 한줄 요약
- CSR 작성 → ACME 도메인 챌린지 검증 → CAA 레코드 확인 → CT Log 등록 및 SCT 획득 → HSM 최종 서명 교부 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **수동 웹 발급** vs **SCEP/EST (기기 등록)** vs **ACME (클라우드 웹 자동화)**.

</details>

| 비교 항목 | 수동 웹 포털 발급 (Legacy) | SCEP / EST 프로토콜 (RFC 7030) | ACME 자동화 프로토콜 (RFC 8555) |
|:---|:---|:---|:---|
| **발급 트리거** | **관리자의 수동 CSR 업로드 및 심사** | **단말 OS/MDM의 기기 등록 트리거** | **서버 데몬(Cert-Manager) 완전 자동화** |
| **신원/도메인 검증** | 이메일 확인, 전화 실사, 서류 제출 | 챌린지 패스워드, 기존 인증서 상호 검증| **DNS-01 / HTTP-01 챌린지 자동 풀이** |
| **만료 갱신 주기** | 1년 단위 (수동 갱신 시 장애 위험) | 1년 ~ 3년 단위 장기 인증서 | **90일 단기 인증서 (자동 무중단 갱신)** |
| **주요 적용 대상** | EV 웹 인증서, 수동 공인인증서 | **사내 Wi-Fi 802.1X 단말, VPN 클라이언트**| **Kubernetes 인그레스, 클라우드 HTTPS 웹**|

#### 한줄 요약
- 수동 발급은 고비용 EV 전용, SCEP/EST는 MDM 단말 전용, ACME는 현대 클라우드 웹 표준 자동화 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DNS CAA (Certification Authority Authorization, RFC 8659)**: 도메인 소유자가 자신의 DNS에 특정 CA(예: `letsencrypt.org`)만 인증서를 발급할 수 있도록 명시하여 타 CA를 통한 위조 발급을 차단하는 레코드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공격자가 취약한 타 CA를 경유하여 자사 도메인의 **부정 위조 인증서를 몰래 발급받는 위협** | **DNS 영역에 `CAA(RFC 8659) 레코드 구성 및 CT Log 모니터링 경보`** 구축 | 승인되지 않은 타 CA의 발급 차단 및 부정 발급 즉각 적발 |
| 온라인 발급 CA의 개인키가 메모리 덤프나 취약점으로 **비인가 유출되는 침해 사고** | **`FIPS 140-3 HSM 내 키 격리` 및 Intermediate CA 레벨 즉각 폐기** | 개인키 원천 반출 차단 및 하위 체인 격리 폐기로 Root CA 보호 |
| 90일 단기 인증서 환경에서 수동 갱신 누락으로 인한 **전사 서비스 중단 장애** | **`K8s Cert-Manager 기반 ACME 자동 갱신 및 만료 30일 전 재시도`** | 만료 휴먼 에러 0% 달성 및 무중단 서비스 연속성 확보 |
| 발급 CA의 CRL 파일 생성 지연으로 인한 폐기 정보 전파 지연 | **`단축된 CRL 발행 주기(1시간)` 및 실시간 OCSP Responder 동기화** | 폐기된 탈취 인증서의 무효화 정보 실시간 전파 |

#### 한줄 요약
- CAA/CT 로그로 부정 발급을 차단하고, HSM 격리로 키를 보호하며, ACME 자동화로 만료 장애를 예방한다.

## Ⅶ. 결론

- 글로벌 디지털 신뢰 생태계의 발행 주체인 **인증기관(CA) 아키텍처는 제로 트러스트 보안 거버넌스의 가장 핵심적인 신뢰 근원(Root of Trust)**이며, 실무 구축 시 **오프라인 Root CA와 온라인 Issuing CA의 엄격한 계층 분리, ACME 기반 인증서 수명주기 전면 자동화, DNS CAA 및 CT Log 기반 전역 모니터링**을 통합 구현하여 오발급 제로의 완벽한 신뢰 인프라 완성

#### 한줄 요약
- CA는 3계층 위임 모델과 HSM 격리 및 ACME/CT 감시 체계를 결합하여 고신뢰 인증서 발급 환경을 구현하는 공인 주체다.