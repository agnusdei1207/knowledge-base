---
title: "Cloud Security Certification CSAP FedRAMP"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CSAP(클라우드 보안 인증제, KISA 운영)와 FedRAMP(Federal Risk and Authorization Management Program, GSA·JAB 운영)는 모두 NIST SP 800-53 기반의 클라우드 서비스 제공자(CSP)에 대한 보안 인증·인가 프레임워크로, CSAP는 한국 공공기관, FedRAMP은 미국 연방기관 대상의 강제성 있는 보안 통제 검증 체계입니다.
> 2. **가치**: 두 인증 모두 ①클라우드 조달 시 반복적인 보안 심사를 일원화하여 70% 이상 심사 비용·기간 절감, ②연간 취약점 점검·월간 ConMon(Continuous Monitoring)을 통한 지속적 보안 수준 보장, ③국제 상호인정(ISO 27017/27018, CSA STAR) 기반의 글로벌 시장 진출 기반을 제공합니다.
> 3. **판단 포인트**: 인증 등급(CSAP 1·2등급, FedRAMP Low/Moderate/High), 인가 경로(CSAP-KISA vs FedRAMP-JAB ATO vs Agency ATO), FIPS 140-2/3 암호모듈 적용 여부, 데이터 주권/잔존성 정책에 따라 아키텍처·운영·비용 구조가 결정되므로, 대상 기관·워크로드·데이터 등급을 사전에 정의해야 합니다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 IaaS·PaaS·SaaS 형태로 공공·민간 부문의 IT 인프라를 빠르게 재편하였지만, 전통적인 보안 통제(perimeter firewall, on-premise SIEM, DC 물리보안)만으로는 다중 테넌트(Multi-tenancy) 환경, 가상화 하이퍼바이저, 공유 책임 모델(Shared Responsibility Model)에서의 데이터 주권, API 기반 공격 표면 확대 위협에 효과적으로 대응하기 어렵습니다. 특히 공공·연방 부문은 법적·규제적 요구사항(개인정보 보호법, FISMA, FedRAMP Authorization Act 2022, 클라우드컴퓨팅법)으로 인해 클라우드 도입 시 독립적 보안 인증을 강제하고 있으며, 이를 위해 한국은 CSAP, 미국은 FedRAMP이라는 국가 단위 인증 체계를 운영합니다.

CSAP는 2015년 KISA(한국인터넷진흥원)가 MSIT(과학기술정보통신부) 지침으로 제정한 「클라우드서비스 보안인증管理制度」로, 클라우드 서비스 보안 인증 기준(클라우드 서비스 보안 가이드라인)에 따라 CSP를 평가·인증합니다. 공공기관이 클라우드를 도입할 때 CSAP 인증을 받은 CSP만을 우선 고려하도록 「클라우드컴퓨팅발전 및 이용자 보호에 관한 법률」 및 공공부문 클라우드 이용지침에서 규정하고 있어, 사실상 **한국 공공 클라우드 시장 진입의 디 팩토 표준**입니다.

FedRAMP은 2011년 OMB(White House Office of Management and Budget)가 발표한 「Federal Cloud Computing Strategy」에 따라 GSA 산하 PMO(Program Management Office)가 운영하며, NIST SP 800-53 Rev. 5(2020), FIPS 199, FIPS 200, NIST SP 800-137(ConMon) 등을 통합한 단일 보안 인가 프레임워크입니다. FedRAMP Authorization Act가 2022년에 법률로 제정되면서 모든 연방기관은 FedRAMP 인가를 받은 CSP만 사용해야 하는 법적 구속력을 갖게 되었습니다.

```text
[ 클라우드 보안 인증의 등장 배경 ]

+-------------------------+         +--------------------------+
|  Traditional On-Premise  |         |   Cloud Computing Era    |
+-------------------------+         +--------------------------+
|  ▸ 물리적 경계(Premise)  |         |  ▸ Hypervisor 기반       |
|  ▸ 단일 조직 통제         |         |    Multi-tenant 격리     |
|  ▸ 내부 감사 일회성        |         |  ▸ Shared Responsibility |
|  ▸ perimeter firewall    |         |  ▸ 동적 워크로드, Auto-  |
|  ▸ DC 출입통제 일원화     |         |    scaling, API surface  |
+------------+------------+         +-----------+--------------+
             |                                    |
             |   감사·통제 갭 발생                 |
             v                                    v
   +----------------------------------------------------------+
   |  반복적 비효율(Customer마다 다른 심사)                     |
   |  + 데이터 주권·법적 책임 불명확                            |
   |  + 하이퍼바이저/VM escape, 컨테이너 탈출 등 신규 위협        |
   +----------------------------------------------------------+
                                |
                                v
   +----------------------------------------------------------+
   |   정부 주도의 표준화된 클라우드 보안 인증 체계 필요         |
   |   +--------------+              +--------------+          |
   |   |     CSAP     |              |   FedRAMP    |          |
   |   |   (KISA)     |              |  (GSA, JAB)  |          |
   |   |  한국 공공     |              |  미국 연방     |          |
   |   +--------------+              +--------------+          |
   +----------------------------------------------------------+
```

기존 패러다임(전통적 IT 감사, ISMS, PCI-DSS)은 조직·시스템 단위 1회성 인증에 가까웠지만, 클라우드 환경에서는 **지속적 모니터링(Continuous Monitoring, ConMon)**, **동적 자산 가시성(Continuous ATO)**, **API·컨테이너 보안**, **데이터 주권·암호화 키 관리(KMS, BYOK/HYOK)** 가 핵심 통제 항목으로 부상했습니다. CSAP와 FedRAMP은 이러한 변화를 반영하여 월 1회 취약점 스캔, 분기 1회 PoC(Plan of Action & Milestone) 갱신, 연 1회 정기 재심사, 실시간 SIEM 연동, FIPS 140-2/3 검증 암호모듈 사용 등 **상시 검증(Continuous Compliance)** 체계를 요구합니다.

- **📢 섹션 요약 비유**: CSAP와 FedRAMP은 마치 **"국제공항의 출국장 보안 검색"** 과 같습니다. 비행기(클라우드 서비스)마다 매번 각 항공사(고객사)가 개별적으로 기내·연료·엔진까지 검사하면 수천 시간이 걸리지만, IATA 표준 인증(CSAP/FedRAMP)을 통과한 항공사는 항공사 코드(IC AO)로 한 번 인가되면 전 세계 공항에서 바로 게이트 통과가 가능해지는 것과 같은 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. CSAP 인증 체계

CSAP는 **클라우드서비스 보안 인증 기준**(KISA 고시)에 따라 ①인증 신청, ②문서 심사, ③기술 심사(현장 실사), ④인증 결정, ⑤사후 관리(연 1회 정기 심사, 변경 심사)의 5단계로 진행됩니다. 통제 항목은 **기반 보안**(물리·네트워크·호스트), **서비스 보안**(IaaS/PaaS/SaaS별 별첨 기준), **데이터 보안**(암호화, 키 관리, 데이터 잔존성), **운영 보안**(모니터링, 사고 대응, 취약점 관리), **관리 체계**(정책, 조직, 교육)로 구성되며, **클라우드 서비스 보안 가이드라인 v3.0**(2023) 기준 약 97개~140여 개의 통제 항목이 적용됩니다.

CSAP는 **2단계 등급 체제**를 운영합니다:
- **1등급(기본)**: 중·저위험 공공 정보, 일반 행정업무 대상, 인증 심사 주기 3년
- **2등급(상)**: 고위험 정보(개인정보, 기밀정보) 취급, 강화된 통제 적용

### 나. FedRAMP 인증 체계

FedRAMP은 NIST RMF(Risk Management Framework)와 1:1 매핑되는 **7단계 인가 프로세스**(Ready -> In Process -> Low/Moderate/High 인가 -> JAB/Agency ATO -> ConMon)를 따르며, 3개의 영향 등급(Impact Level)을 정의합니다:
- **Low**: 일반 정보 공개 자료, 약 125개 통제
- **Moderate**: 비공개 PII·연방 정보, 약 325개 통제 (가장 보편적)
- **High**: 기밀·법집행·재난 대응 정보, 약 421개 통제

인가 경로는 ①**JAB(Joint Authorization Board)** ATO — DoD, DHS, GSA 자체 인가, ②**Agency ATO** — 단일 연방기관의 자체 인가 후 PMO 등록, ③**LI-SaaS** 경량 인가 — Slack·Zoom 같은 SaaS용 약 36개 통제 축소형의 세 가지가 있습니다.

### 다. 핵심 통제 아키텍처 (NIST SP 800-53 Rev. 5 매핑)

```text
[ CSAP / FedRAMP 공통 보안 통제 아키텍처 ]

                  +--------------------------------------+
                  |      Cloud Service Customer (CSC)     |
                  |   (공공기관/연방기관 = FedRAMP Agency) |
                  +------------------+-------------------+
                                     | 1) 서비스 요청
                                     | 2) 보안 통제 책임 분담 합의
                                     v
        +--------------------------------------------------------+
        |  Cloud Service Provider (CSP) : NHI Cloud / AWS GovCloud|
        |  +-------------------------------------------------+    |
        |  |        1) Inherited from FedRAMP / CSAP         |    |
        |  |  - 물리보안, Hypervisor, Network infra, IAM     |    |
        |  |        2) Hybrid (CSP + Customer 공동 책임)      |    |
        |  |  - OS patch, DB 접근통제, Application log      |    |
        |  |        3) Customer Responsibility (IaaS)        |    |
        |  |  - Guest OS, 데이터 암호화, ACL 정책           |    |
        |  +-------------------------------------------------+    |
        +--------+--------------------------+--------------------+
                 |                          |
                 v                          v
   +------------------------+   +------------------------+
   | 3PAO / 보안 감정원     |   |  KISA / FedRAMP PMO   |
   | (Third Party Assessor) |   | (인가를 결정하는 정부)  |
   |  - 취약점 스캔          |   |  - Authorization       |
   |  - 침투 테스트           |   |    Decision             |
   |  - 통제 항목 검증        |   |  - Continuous Monitoring|
   +------------------------+   +----------+-------------+
                                          | ConMon 보고서
                                          v
                           +--------------------------+
                           |  PMO / JAB (Revocation) |
                           |  - 격월/월별 검토         |
                           |  - ATO Revocation 가능   |
                           +--------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CSP (Cloud Service Provider)** | 클라우드 서비스(IaaS/PaaS/SaaS) 제공, 통제 항목 이행을 1차 책임 | AWS, Azure, GCP, NHN Cloud, KT Cloud, Samsung Cloud Platform 등. CSAP·FedRAMP 인가를 받은 서비스 카탈로그 운영, ISO 27001/27017/27018 동시 인증 보유. |
| **3PAO / 보안 감정원** | 독립적 보안 평가 수행 (FedRAMP의 3PAO, CSAP의 한국인터넷진흥원 인정 감정원) | FedRAMP은 A2LA(ANSI National Accreditation Board) 공인 3PAO만 참여 가능, CSAP은 KISA 등록 보안감정원 17개 기관. 침투 테스트, 취약점 스캔, 정책·구성 검토, SAR(Security Assessment Report) 작성. |
| **JAB / KISA PMO** | 인가 결정 및 ConMon 감독 (PMO) | FedRAMP JAB = DoD·CIO Council·GSA 기술위원(Chief Authorizing Official), 월 1회 JAB 회의, ATO 부여/철회 권한. CSAP 인증위원회는 KISA 내부 + 외부 위원. |
| **CSC (Cloud Service Customer)** | 클라우드 자산을 사용하는 기관, 고객 측 책임 통제 이행 | FedRAMP Agency ATO 시 자국 P-ATO(Provisional ATO) 후 시스템 본연의 인가. 한국 공공기관은 CSAP 인증 CSP 사용 시 보안성 검토(클라우드컴퓨팅법 §13) 추가 수행. |
| **ConMon (Continuous Monitoring)** | 인가 후 상시 보안 상태 검증 (FedRAMP의 핵심 차별점) | 월 1회 OS·DB·네트워크 취약점 스캔(Tenable Nessus, Qualys, Rapid7), 분기 1회 POA&M 갱신, 연 1회 Penetration Test, OS 패치 SLA 30일(Critical), 90일(High). |

### 라. 공통 기술 통제 항목 (상세)

| 통제 패밀리 (NIST 800-53 매핑) | 핵심 통제 항목 | 구현 기술 및 예시 |
| :--- | :--- | :--- |
| **AC (Access Control)** | AC-2, AC-3, AC-6 Least Privilege | IAM Role-Based, ABAC, MFA(FIDO2, TOTP), Just-in-Time Access (Azure AD PIM) |
| **AU (Audit and Accountability)** | AU-2 이벤트 로깅, AU-3, AU-6 | CloudTrail/Activity Log -> SIEM(Splunk, QRadar, Sentinel) -> 90일 핫, 7년 콜드 보관 |
| **SC (System & Communications Protection)** | SC-8 전송 암호화, SC-13 암호 사용 | TLS 1.2+ (TLS 1.3 권고), FIPS 140-2/3 검증 모듈(AWS KMS, HSM CloudHSM), mTLS |
| **SI (System & Information Integrity)** | SI-2 결함 수정, SI-4 정보 시스템 모니터링 | OS 패치 SLA, IDS/IPS(GuardDuty, WAF, Azure Defender), 파일 무결성 모니터링(Tripwire) |
| **CP (Contingency Planning)** | CP-2 BCP, CP-9 백업 | RTO 4h / RPO 1h, Cross-Region Backup, AWS Backup, Veeam, 3-2-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 395 / 800

<- **이전**: [394. 데이터 3법 가명정보 결합 활용](/studynote/12_it_management/05_security_compliance/394_data_3_acts_pseudonymization_combination/)
**다음**: [396. 제로 트러스트 보안 모델 NIST 800-207](/studynote/12_it_management/05_security_compliance/396_zero_trust_security_model_nist_800_207/) ->

---
