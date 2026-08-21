---
sidebar:
  order: 9
  label: "009. CA 인증 기관•인증서 발급 절차 (Certificate Authority)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "인증기관 아키텍처 및 발급 절차 : CA (Certificate Authority & PKCS#10/ACME)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 9
extra:
  question_no: "009"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "Root CA/Intermediate CA/Issuing CA 3계층 구조, CP/CPS(RFC 3647), CSR(PKCS#10) 및 자동화 ACME(RFC 8555)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **인증기관(Certificate Authority, CA)**: 공개키 기반구조(PKI)에서 신청자의 신원(Identity)과 공개키의 소유권(Proof of Possession)을 엄격히 검증한 후, 인증기관 자신의 비대칭 개인키로 전자서명한 X.509 디지털 인증서를 발행·배포·폐기 관리하는 공인 신뢰 주체.
- **인증 정책(CP, RFC 3647) 및 인증업무 준칙(CPS)**: 해당 CA가 인증서를 발급하기 위해 요구하는 보안 등급 및 신원 확인 기준을 정의한 **CP(Certificate Policy)** 와, 이를 기술적·물리적·관리적으로 이행하는 구체적 운영 절차를 명시한 **CPS(Certification Practice Statement)**.

</details>

- 정의/개념: 최상위 신뢰점인 **Root CA**, 정책 위임 계층인 **Intermediate CA**, 최종 서명을 집행하는 **Issuing CA**의 3계층 위임 모델과 **RFC 3647 CP/CPS 거버넌스** 에 기반하여 무결점 인증서를 발급하는 **디지털 신뢰 발급 체계**
- 배경/필요성: 단일 CA 구조에서 발생할 수 있는 루트 개인키 탈취 위험(단일 장애점: SPOF)을 계층적 격리로 원천 차단하고, 도메인/신원 위조를 방지하기 위한 표준화된 발급 검증 파이프라인을 확립할 요구

#### 한줄 요약
- 계층적 CA 아키텍처와 엄격한 CP/CPS 기준에 따라 신원을 검증하고 X.509 인증서를 발행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **다중 통제(Multi-Person Control / $M$-of-$N$ Quorum)**: Root CA 개인키를 활성화하거나 최상위 인증서를 발급할 때, 단독 관리자의 전횡 및 침해를 방지하기 위해 $N$명의 보안 책임자 중 최소 $M$명 이상의 암호키 파편(SmartCard / HSM Token)이 물리적으로 동시 인증되어야 연산이 승인되는 접근 통제 기법.
- **CAA(Certificate Authority Authorization / RFC 8659)**: 도메인 소유자가 DNS 영역에 `CAA` 레코드를 등록하여(예: `issue "letsencrypt.org"`), 지정되지 않은 타 CA가 해당 도메인의 인증서를 임의 발급하는 것을 사전 차단하는 보안 메커니즘.

</details>

- **3계층 권한 위임 및 장애 격리 (Fault Isolation)**: Issuing CA 키가 유출되더라도 상위 Intermediate CA에서 해당 인증서만 폐기하면 Root CA 및 타 도메인 신뢰는 100% 보존
- **하드웨어 보안 모듈(HSM) 필수화**: Root 및 Intermediate CA 개인키는 FIPS 140-3 Level 3 인증 하드웨어 보안 칩셋 내부에 영구 격리
- **발급 내역 공개 감사 (Certificate Transparency, CT)**: CA가 발급한 모든 X.509 인증서를 공개된 분산 덧붙임 전용 머클 트리 로그(CT Log)에 등록 강제

#### 한줄 요약
- 3계층 권한 분립, HSM 격리 및 다중 통제($M$-of-$N$), CAA DNS 통제, CT 로그 감사성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ACME 프로토콜(Automated Certificate Management Environment / RFC 8555)**: 웹 서버가 CA 서버와 통신하여 도메인 소유권 검증(HTTP-01, DNS-01 챌린지)부터 인증서 발급, 갱신, 설치 전 과정을 사람의 개입 없이 API로 자동화하는 표준 프로토콜.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 오프라인 최상위 루트 기관 (Offline Root CA) ]                      │
│  ├─ 자체 서명(Self-Signed) Root X.509 인증서 탑재                        │
│  └─ 물리적 에어갭(Air-Gapped) 격리 + FIPS 140-3 HSM ($M$-of-$N$ 다중 통제)│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Sub CA 인증서 발급: 수년에 1회 가동)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 정책/중간 인증기관 (Intermediate / Policy CA) ]                   │
│  ├─ 조직별/용도별(서버용, 코드서명용, 기기 mTLS용) 서명 권한 분리       │
│  └─ 온라인 발급 CA에 발급 권한 위임 및 경로 제약(Path Length Constraint) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Issuing CA 인증서 발급)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 온라인 발급 인증기관 (Online Issuing CA) & 등록기관 (RA) ]          │
│  ├─ 등록기관(RA): 도메인 소유권(ACME Challenge) 및 CSR PoP 검증 심사    │
│  ├─ 온라인 HSM: 승인된 End-Entity 인증서 실시간 고속 전자서명            │
│  └─ 폐기 및 감사: CRL/OCSP 저장소 갱신 + 공공 CT Log(RFC 6962) 자동 제출  │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 오프라인 Root CA가 최상위 신뢰를 제공하고, Intermediate CA가 정책을 통제하며, 온라인 Issuing CA/RA가 가입자의 인증서를 발급하고 CT 로그에 기록하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **오프라인 Root CA** | 신뢰 기준점(Trust Anchor)으로 하위 Intermediate CA 인증서만을 서명 교부 | Offline Air-Gap |
| **중간 CA (Intermediate)** | 인증 정책(CP) 집행, 발급 경로 제약 설정 및 도메인/용도별 하위 CA 통제 | RFC 5280 Sub-CA |
| **등록기관 (RA)** | 신청자의 실명·도메인 DNS 검증 및 CSR 서명의 키 소유권(PoP) 심사 | ACME Server |
| **온라인 Issuing CA** | 승인된 신청자에게 HSM 내부 개인키로 서명된 최종 단말 X.509 인증서 발행 | FIPS 140-3 HSM |
| **CT Log 서버** | 발급된 모든 인증서의 SHA-256 다이제스트를 공개 머클 트리에 영구 기록 | RFC 6962 CT Log |

#### 한줄 요약
- 오프라인 Root CA, 정책 중간 CA, 등록기관(RA), 온라인 Issuing CA, CT Log 서버가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ACME DNS-01 챌린지**: CA가 무작위 토큰을 클라이언트에 제공하면, 클라이언트가 자신의 DNS 도메인 TXT 레코드(`_acme-challenge.domain.com`)에 해당 토큰 해시값을 등록하고, CA가 DNS 질의를 통해 도메인 제어권을 입증하는 자동화 검증 기법.

</details>

```text
1. 웹 서버(Client)가 비대칭 키 쌍을 생성하고 PKCS#10 형식의 CSR(공개키 + 도메인명 + 자체 서명) 작성
            │
            ▼
2. ACME 클라이언트(Cert-Manager)가 RFC 8555 프로토콜을 통해 CA의 RA 엔드포인트로 CSR 전송
            │
            ▼
3. RA가 DNS-01/HTTP-01 챌린지를 발행하여 도메인 제어권 및 DNS CAA 레코드 적합성 자동 검증
            │
            ▼
4. 검증 통과 ➔ 온라인 Issuing CA가 사전 인증서(Pre-certificate)를 생성하여 공공 CT Log 서버에 제출
            │
            ▼
5. CT Log 서버로부터 SCT(Signed Certificate Timestamp) 토큰 수신 ➔ 인증서 확장에 임베딩
            │
            ▼
6. Issuing CA가 HSM 개인키로 최종 X.509 v3 인증서 전자서명 및 발급 완료 ➔ 웹 서버로 전달
```

**동작 원리**

1. **CSR 생성 및 PoP 증명**: 비대칭 개인키를 외부 반출 없이 내부 생성하고 CSR 자체 서명 수행
2. **도메인 인가 챌린지**: CA가 임의의 챌린지 난수를 전달하고 DNS TXT 레코드 또는 웹 경로(`.well-known`) 검증
3. **CAA 정책 검사**: DNS 상의 CAA 레코드를 조회하여 해당 CA가 정당한 발급 인가 기관인지 확인
4. **CT 로그 선행 등록**: 인증서 발급 전 공공 분산 원장에 메타데이터를 등록하여 SCT 토큰 확보
5. **HSM 서명 및 교부**: 변조 불가능한 하드웨어 내부에서 최종 전자서명을 완성하여 클라이언트에 설치

#### 한줄 요약
- CSR 작성, ACME 도메인 챌린지 검증, CAA 레코드 확인, CT Log 등록 및 SCT 획득, HSM 최종 서명 교부 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **인증서 발급 방식 비교**: 전통적 수동 신청 방식, 엔터프라이즈 SCEP/EST 방식, 클라우드 네이티브 ACME 표준의 비교.

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

- **오발급 사태(Mis-issuance / DigiNotar 사건)**: 해커가 취약한 공인 CA 시스템을 해킹하여 Google, Microsoft 등 타사 도메인의 가짜 인증서를 무단 발급받아 전 세계 수백만 사용자를 도청한 보안 참사.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공격자가 취약한 해외 CA를 경유하여 자사 도메인의 **부정 위조 인증서를 몰래 발급받는 위협** | **DNS 영역에 CAA(RFC 8659) 레코드 구성 및 CT Log 모니터링 경보 시스템** 구축 | 승인되지 않은 타 CA의 인증서 발급 차단 및 부정 발급 즉각 적발 |
| 온라인 발급 CA의 개인키가 메모리 덤프나 취약점으로 **비인가 유출되는 치명적 침해 사고** | **FIPS 140-3 Level 3 HSM 내 키 격리 및 Intermediate CA 레벨 즉각 폐기** 절차 | 개인키 원천 반출 차단 및 하위 체인 격리 폐기로 Root CA 신뢰 보호 |
| 90일 단기 인증서 환경에서 수동 갱신 누락으로 인한 **전사 대규모 서비스 중단 장애** | **K8s Cert-Manager 기반 ACME 자동 갱신 및 만료 30일 전 자동 재시도** 구성 | 만료 휴먼 에러 0% 달성 및 100% 무중단 서비스 연속성 확보 |

#### 한줄 요약
- CAA/CT 로그로 부정 발급을 차단하고, HSM 격리로 키를 보호하며, ACME 자동화로 만료 장애를 예방한다.

## Ⅶ. 결론

- 글로벌 디지털 신뢰 생태계의 발행 주체인 **인증기관(CA) 아키텍처**는 제로 트러스트 보안 거버넌스의 가장 핵심적인 신뢰 근원(Root of Trust)이며, 실무 구축 시 **오프라인 Root CA와 온라인 Issuing CA의 엄격한 계층 분리**, **ACME 기반 인증서 수명주기 전면 자동화**, **DNS CAA 및 CT Log 기반 전역 모니터링**을 통합 구현하여 오발급 제로의 완벽한 신뢰 인프라를 완성

#### 한줄 요약
- 3계층 CA 위임 모델과 HSM 격리 및 ACME/CT 감시 체계를 결합하여 고신뢰 인증서 발급 환경을 구현한다.
