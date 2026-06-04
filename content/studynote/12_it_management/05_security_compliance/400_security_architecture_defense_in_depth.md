---
title: "400. 보안 아키텍처 디자인 원칙 심층 방어 (Security Architecture Defense in Depth)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 심층 방어(Defense in Depth, DiD)는 NIST SP 800-53의 AC/SC/SI 제어 항목과 ISO 27001의 A.13/A.14 통제 영역을 기반으로, 네트워크·호스트·애플리케이션·데이터·관리 거버넌스의 5개 계층에 예방(Preventive)·탐지(Detective)·대응(Responsive)·회복(Recovery) 4대 기능을 N-Versioning처럼 중첩 배치하여 단일 실패 지점(Single Point of Failure)을 구조적으로 제거하는 보안 아키텍처 설계 원칙이다.
> 2. **가치**: Verizon DBIR 2024 기준 74%의 침해가 단일 통제 미흡에서 발생하며, DiD 적용 시 MTTD(Mean Time To Detect)를 197일->9일로 단축(IBM Cost of a Data Breach 2023), 침해 비용을 평균 $1.5M 절감하고, ISMS-P 인증 심사 시 '관리적·물리적·기술적 영역 통제' 동시 충족을 통한 인증 리드타임 30% 단축 효과를 제공한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (1) **레이어 수 vs 운영 복잡도(OpEx)**: 7계층 이상 시 SIEM 로그 볼륨 2TB/일 초과로 탐지 정확도 저하, (2) **Zero Trust 대비 정적 경계 가정**: 클라우드·SaaS·원격근무 환경에서 전통적 Perimeter-DiD는 무력화되므로 SDP/ZTNA로의 진화 필요, (3) **CAPEX vs Risk-Based 우선순위**: 모든 자산에 동일 통제 적용 시 ROI 38% 저하(HMS 2022)이므로 BIA(Business Impact Analysis) 기반 자산 분류 후 Critical 자산 우선 적용.

---

## Ⅰ. 개요 및 필요성

정보시스템 보안 위협은 1990년대 단순 Worm·바이러스에서 2020년대의 **공급망 공격(SolarWinds, 3CX, MOVEit)**, **랜섬웨어 듀얼 익스톨션(Cl0p, LockBit)**, **제로데이 익스플로잇(BlueKeep, Log4Shell, CitrixBleed)**, **생성형 AI 기반 피싱/딥페이크**로 진화했다. 단일 방어선(예: 방화벽만 운영)은 2024년 Palo Alto Unit 42 통계 기준 침해 성공률 81%를 보이며, 이는 *Castle-and-Moat* 모델이 현대 **경계가 없는(perimeterless)**, **API-first**, **Multi-Cloud** 환경에서 구조적으로 한계를 드러냈기 때문이다.

특히 클라우드 네이티브 환경에서는 EKS Pod, Lambda Function, API Gateway, SaaS Workspace 등 **자산 경계가 1초 단위로 변화**하며, Gartner가 2023년 경고한 *"Identity is the new perimeter"* 트렌드는 NACL·보안그룹 같은 네트워크 레이어 DiD가 아닌 **ID/맥락 기반 동적 DiD**로의 전환을 요구한다. 한국 환경에서는 **ISMS-P(정보보호 및 개인정보보호 관리체계)**, **개인정보보호법 제29조(안전조치의무)**, **전자금융감독규정 제14조(정보기술부문 안전성)**, **KISA 클라우드 보안 인증(CSAP)** 등 규제 준거성 확보를 위해 DiD가 사실상 의무 통제 패턴으로 자리 잡았다.

기존 단일 보안 통제 패러다임은 **'예방 중심(Prevention-First)'** 사고로, 탐지·대응 거버넌스가 부재하여 침해 후 평균 204일간潜伏(Dwell Time, Mandiant M-Trends 2023)되는 문제를 야기했다. 현대 DiD는 **'Assume-Breach(침해 전제)'** 사고로 전환하여, "차단할 수 없는 공격은 탐지하고, 탐지할 수 없는 침해는 격리하며, 격리할 수 없는 손상은 복구한다"는 **NIST CSF 2.0(2024.02 발표)의 6대 기능** Govern·Identify·Protect·Detect·Respond·Recover 전체를 아우르는 거버넌스 통합 모델로 재정립되었다.

```text
+------------------------------------------------------------------+
|              심층 방어(DiD) 전략 패러다임 전환 흐름도              |
+------------------------------------------------------------------+
|                                                                  |
|  [1세대: 1990s]           [2세대: 2000s]         [3세대: 2010s+]   |
|  Castle & Moat            Layered Defense       Defense in Breadth|
|  +---------+              +----------+          +--------------+ |
|  |Firewall | ---------►  |FW+IDS+DMZ| ------► |DiD + Zero    | |
|  |  only   |              |          |          |Trust + SASE  | |
|  +---------+              +----------+          +--------------+ |
|       |                        |                      |         |
|       v                        v                      v         |
|  • 80% 예방 중심          • 70% 예방/30% 탐지     • 40% 예방      |
|  • 정적 경계             • IPS/AV 추가          • 60% 탐지/대응  |
|  • 내부 신뢰 전제         • 일부 EDR 도입         • ID/데이터중심 |
|                                                                  |
|  ---------------- [현재: 4세대 - 2024~] --------------            |
|  +------------------------------------------------------+        |
|  |  Zero Trust + Continuous DiD + AI-Augmented SOC      |        |
|  |  +----+ +----+ +----+ +----+ +----+ +----+          |        |
|  |  |GOV |->|ID  |->|PRO |->|DET |->|RES |->|REC | (CSF 2.0)|       |
|  |  +----+ +----+ +----+ +----+ +----+ +----+          |        |
|  |  <------ Continuous Monitoring & Feedback ------>     |        |
|  +------------------------------------------------------+        |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 심층 방어는 성벽 하나만 있는 *성(城)* 이 아니라, **해자(moat) -> 외성(outer bailey) -> 내성(inner bailey) -> 망루(watchtower) -> 왕좌(keep) -> 지하 대피소**까지 다섯 겹으로 둘러싸인 중세 성채와 같다. 적이 해자를 건너도 외성에서, 외성을 뚫어도 내성에서, 그마저 통과해도 망루의 감시원이 즉시 경종을 울린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

심층 방어 아키텍처는 크게 **5계층 구조(P5-Layer) × 4대 보안 기능(F4-Function) 매트릭스**로 구성된다. 5계층은 OSI 7Layer의 물리부터 데이터까지 매핑되며, 4대 기능은 **P(Preventive) · D(Detective) · R(Responsive) · C(Corrective)** 4-tuple로 각 계층에 최소 2개 이상의 통제(Control)를 배치하여 **N+1 Redundancy**를 구현한다.

### 5계층 × 4기능 매트릭스 (P5 × F4)

```text
+----------------------------------------------------------------------+
|                    심층 방어 5계층 아키텍처 다이어그램                    |
+----------------------------------------------------------------------+
|                                                                      |
|   [External]                                                         |
|   +------------------------------------------------------------+    |
|   | L1: Governance & Risk Layer  (정책·규제·컴플라이언스)        |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   |  |P: 정책/  |  |D: GRC    |  |R: IRP/BCP |  |C: 정책   |    |    |
|   |  |  표준   |  |(Archer)  |  | (NIST SP  |  |  업데이트|    |    |
|   |  |ISMS-P   |  | 감사로그  |  |  800-61)  |  |  Cycle  |    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   +------------------------------------------------------------+    |
|                          | SIEM 상위분석                            |
|   +------------------------------------------------------------+    |
|   | L2: Network & Perimeter Layer                                |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   |  |P: NGFW/  |  |D: IDS/IPS |  |R: SOAR    |  |C: Backup |    |    |
|   |  |WAF/DDoS  |  |(Snort/   |  | 자동차단  |  |NetFlow   |    |    |
|   |  |Cloudflare|  | Suricata)|  | (Cortex)  |  | Forensics|    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   +------------------------------------------------------------+    |
|                          |                                         |
|   +------------------------------------------------------------+    |
|   | L3: Identity & Access Layer  (가장 중요 - "New Perimeter")   |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   |  |P: MFA/   |  |D: UEBA/  |  |R: 자동    |  |C: ID 정정|    |    |
|   |  |PAM/SSO  |  | 세션분석 |  | 계정잠금 |  |  attestation|  |    |
|   |  |Okta/    |  |(Sentinel)|  | + ZTNA    |  |  Quarterly|    |    |
|   |  |CyberArk |  |  Risk    |  |  Step-up  |  |  Review  |    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   +------------------------------------------------------------+    |
|                          |                                         |
|   +------------------------------------------------------------+    |
|   | L4: Endpoint & Application Layer                             |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   |  |P: EDR/   |  |D: RASP/  |  |R: EDR     |  |C: Patch  |    |    |
|   |  | 앱취약점 |  |SAST/DAST |  |  Isolatio |  |  Mgmt +  |    |    |
|   |  | 패치    |  |Snyk/Veracode| |n Process |  |  SBOM    |    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   +------------------------------------------------------------+    |
|                          |                                         |
|   +------------------------------------------------------------+    |
|   | L5: Data & Storage Layer  (최후의 방어선)                    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   |  |P: 암호화 |  |D: DLP/   |  |R: Data    |  |C: DR/    |    |    |
|   |  |KMS/HSM  |  | Database |  |  Masking  |  | Backup   |    |    |
|   |  |AES-256  |  | Activity  |  | + Tokeniz |  |  3-2-1   |    |    |
|   |  |FIPS 140-3|  | Monitoring| |  ation    |  |  Rule    |    |    |
|   |  +----------+  +----------+  +----------+  +----------+    |    |
|   +------------------------------------------------------------+    |
|                          |                                         |
|                       [Data Asset]                                  |
|                                                                      |
|  <------ Log Aggregation to SIEM (Splunk / QRadar / Sentinel) ----   |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L1: Governance & Risk** | 정책·규제·위험 관리 거버넌스 | ISMS-P 64개 통제, NIST CSF 2.0 Govern 기능, ISO 27005 Risk Assessment, RACI 매트릭스 기반 책임 소재 명확화, GRC(Governance·Risk·Compliance) 플랫폼(Archer·ServiceNow GRC)을 통한 단일 진실 공급원(SSOT) 운영. 정책 위반 시 자동 에스컬레이션 워크플로우 트리거 |
| **L2: Network & Perimeter** | 외부·내부 네트워크 트래픽 통제 | NGFW(Palo Alto PA-5400/CheckPoint Maestro), WAF(AWS WAF/Akamai Kona), DDoS Mitigation(Cloudflare Magic Transit/AWS Shield Advanced), Micro-Segmentation(Vmware NSX/Illumio Core), NAC(Cisco ISE/Aruba ClearPass), E/W(동-서) 트래픽 가시화 및 Zero-Segmentation |
| **L3: Identity & Access** | 사용자·시스템·서비스 신원 검증 | MFA(FIDO2/WebAuthn), RBAC+ABAC 하이브리드, PAM(CyberArk/BeyondTrust), CIEM(Cloud Infrastructure Entitlement Management) - AWS IAM Access Analyzer, Just-In-Time 권한 상승, OAuth 2.1 + OIDC, SAML 2.0, UEBA(User Entity Behavior Analytics) 통한 이상 행위 탐지 |
| **L4: Endpoint & Application** | 호스트·애플리케이션 무결성 보장 | EDR(CrowdStrike Falcon/SentinelOne Singularity/XDR), Application Allow-listing(AppLocker/WDAC), CSPM(Prisma Cloud/Wiz), SBOM(SBOM CycleTrack/CycloneDX), SAST/DAST(Snyk/Checkmarx/Veracode), RASP(Imperva RASP/Datadog ASM), Code Signing(HSM-backed) |
| **L5: Data & Storage** | 데이터 기밀성·무결성·가용성 | AES-256-GCM at-rest, TLS 1.3 in-transit, FIPS 140-3 Level 3 HSM, BYOK/HYOK(고객관리형 키), DLP(Symantec DLP/Forcepoint), DAM(Database Activity Monitoring - Imperva SecureSphere), Data Classification(Apache Ranger/Microsoft Purview), Air-gapped Immutable Backup(Veeam V12 Hardened Repository) |

### 핵심 원리: Defense-in-Breadth & Dependency

DiD의 수학적 근거는 **Defense in Depth = f(Layers, Independence, Coverage)** 로 표현할 수 있다. N개의 보안 통제 중 k개가 독립적으로 실패해야 침해가 성공한다면, 시스템 침해 확률 P(breach) = ∏(i=1 to k) Pi 이며, 각 Pi = 0.05(5% 우회 확률)일 때 **3중 통제 시 P = 0.000125 = 0.0125%** 로 단일 통제 대비 800배 향상된다(Gartner Hype Cycle 2023). 그러나 통제 간 **종속성(Common Mode Failure)** 이 존재하면 효과가
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 400 / 800

<- **이전**: [399. 사고 대응 IR 포렌식 분석 절차](/studynote/12_it_management/05_security_compliance/399_incident_response_ir_forensics_analysis/)
**다음**: [401. 보안 개발 생명주기 SDL 보안 코딩](/studynote/12_it_management/05_security_compliance/401_security_development_lifecycle_sdl_coding/) ->

---
