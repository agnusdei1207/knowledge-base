+++
title = "465. IT 경영 관리 핵심 토픽 465번 시험 요약 (IT Management Core Topic 465 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보보안 관리체계(ISMS-P, ISO 27001)·제로트러스트(ZTNA, mTLS, SDP)·AI 기반 위협탐지(UEBA, XDR, SOAR)를 통합한 사이버보안 거버넌스로, **Risk = Asset × Threat × Vulnerability × Impact** 공식을 기반으로 사이버 킬체인(Recon->Weaponize->Deliver->Exploit->Install->C2->Actions on Objectives) 전 단계에 대한 예방·탐지·대응 역량을 확립하는 것
> 2. **가치**: NIST CSF 2.0·COBIT 2019 기반 거버넌스 정착 시 평균 MTTD(Mean Time To Detect) 65% 단축(IBM 2024 보고서), 침해사고 평균 비용 USD 4.88M -> 1.5M 절감 가능, ISMS-P 인증 기업 99.2%에서 regulatory·감사 대응 공수 50% 이상 감소
> 3. **판단 포인트**: On-prem SIEM vs Cloud-native XDR(Splunk vs Sentinel vs Chronicle), EDR 단독 vs NDR+XDR+CDR 통합(가시성 vs 복잡성), 마이크로세그멘테이션(VXLAN, NSX) 레벨 결정(L2/L3/L7), 제로트러스트 도입 시 Identity Provider(IdP) 고가용성(99.99% SLA) 확보가 single point of failure 방지 핵심

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화, 랜섬웨어·공급망 공격(Supply Chain Attack: SolarWinds, 3CX, MOVEit, Log4j, XZ Utils) 증가, 생성형 AI 기반 피싱·딥페이크 공격 등 사이버 위협 환경이 **지능화·산업화·민주화**되고 있다. 특히 2024년 대한민국 개인정보보호법 개정, EU DORA(2025.01 시행), 미국 SEC 사이버공시 규정(8-K Item 1.05) 등으로 인해 **이사회급 사이버 거버넌스**가 필수가 되었으며, 정보보안은 더 이상 IT 부서의 전담 영역이 아닌 **엔터프라이즈 리스크 관리(ERM)**의 핵심축으로 재편되었다.

기존의 "경계 기반 보안(Perimeter Security, Castle-and-Moat)" 패러다임은 클라우드·SaaS·원격근무·IoT·OT 환경에서 무력화되었다. 공격자는 이미 침투했다는 전제(**"Assume Breach"**)하에, **제로트러스트(Zero Trust, NIST SP 800-207)**, **XDR(Extended Detection & Response)**, **SOAR(Security Orchestration, Automation & Response)** 기반의 **지능형 탐지·자동화 대응 체계**가 요구된다. 정보보안의 본질은 **"위험을 0으로 만드는 것"이 아니라, 비즈니스 허용 범위(ALE: Annual Loss Expectancy) 내로 관리하는 리스크 최적화**임을 명확히 해야 한다.

```text
[ 기존 경계 보안 vs 제로트러스트 보안 패러다임 비교 ]

기존 (Castle & Moat)                제로트러스트 (Zero Trust)
+----------------------+           +----------------------+
|  내부 = 신뢰, 외부=불신 |           | 모든 요청 = 기본 불신 |
+----------------------+           +----------------------+
         |                                    |
   +-----v-----+                       +-----v-----+
   |  방화벽/WAF |                       |   PDP/PEP  |
   |   DMZ/VPN  |                       | IdP + MFA  |
   +-----+-----+                       | mTLS/SDP   |
         |                             | mSEG/EDR   |
   +-----v-----+                       +-----+-----+
   | 내부=암묵신뢰|                             |
   |  East-West |                       +-----v-----+
   |  트래픽 무검증|                       | 지속 검증  |
   +-----------+                       | 최소 권한  |
                                       | (PoLP/Just|
                                       |  in Time) |
                                       +-----------+
   약점: 측면이동(Lateral)              장점: 내부 침투 후에도
   랜섬웨어 확산 90%                    East-West 차단으로
   (Sophos State of Ransomware 2024)   피해 반경(Blast Radius)
                                       72% 감소 (Forrester)
```

과거에는 방화벽·IDS/IPS·DLP 단일 솔루션 도입 후 "보안은 끝났다"는 인식이 팽배했으나, 현대의 **MITRE ATT&CK** 프레임워크는 공격자가 평균 277일(IBM) 동안 환경 내에 은밀히潜伏할 수 있음을 보여준다. 따라서 **위험 가시성(Visibility) -> 탐지(Detection) -> 대응(Response) -> 복구(Recovery)** 의 사이클이 끊임없이 돌아가야 하며, 이를 **자동화(Automation)·오케스트레이션(Orchestration)** 으로 구현하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 옛날 성벽 보안은 "성벽만 두껍게 쌓으면 된다"는 castle-and-moat 사고였지만, 현대 보안은 **공항 보안**과 같습니다. 탑승권(Identity), 검색대(Authentication), 게이트(Policy Enforcement), 기내 CCTV(Continuous Monitoring) 어느 하나도 빠질 수 없으며, **승객이 비행기 안(내부)에 있다 해도 수하물·행동을 계속 확인**하는 지속적 검증이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정보보안 거버넌스 아키텍처는 **5계층 레이어드 모델**로 구성되며, 각 계층은 명확한 책임과 기술 스택을 갖는다. 가장 하위 **데이터/자산 계층**부터 상위 **거버넌스/리스크 계층**까지 양방향 피드백 루프(Plan-Do-Check-Act, ISO 27001 Clause 4-10)로 운영된다.

```text
[ 현대 정보보안 거버넌스 5계층 아키텍처 (PDCA + Zero Trust Loop) ]

+-------------------------------------------------------------+
|  Tier 5: 거버넌스 & 컴플라이언스 (Governance & Compliance)    |
|  +----------+ +----------+ +----------+ +--------------+    |
|  |  COBIT   | | NIST CSF | | ISMS-P   | |  RMF/NIST    |    |
|  |   2019   | |   2.0    | |(한국ISMS) | |  800-37 r2   |    |
|  +----------+ +----------+ +----------+ +--------------+    |
+-------------------------+-----------------------------------+
                          | KPI/Risk Metrics (KRIs/KPIs)
+-------------------------v-----------------------------------+
|  Tier 4: GRC & 위협 인텔리전스 (Threat Intel & Risk Mgmt)    |
|  +----------+ +----------+ +----------+ +--------------+    |
|  |   GRC    | |  TIP/STIX | |  CTI     | |   VM/ASM     |    |
|  |(Archer,  | |(MISP,    | |(Mandiant,| | (Tenable,    |    |
|  | ServiceNow| |Anomali)  | | Recorded | |  Qualys)     |    |
|  +----------+ +----------+ +----------+ +--------------+    |
+-------------------------+-----------------------------------+
                          | Threat Feeds (STIX/TAXII 2.1)
+-------------------------v-----------------------------------+
|  Tier 3: SOC & 자동화 대응 (Detect-Respond-Automate)         |
|  +----------+ +----------+ +----------+ +--------------+    |
|  |  SIEM    | |   XDR    | |   SOAR   | |   UEBA/NDR   |    |
|  |(Splunk,  | |(Crowd-   | |(Cortex,  | | (Exabeam,    |    |
|  | Sentinel)| | Strike,  | |  Splunk  | |  Darktrace)  |    |
|  |          | | Sentinel)| |  SOAR)   | |              |    |
|  +----------+ +----------+ +----------+ +--------------+    |
+-------------------------+-----------------------------------+
                          | Telemetry (EDR logs, NetFlow, CloudTrail)
+-------------------------v-----------------------------------+
|  Tier 2: 엔드포인트/네트워크/클라우드 보안 (Protect Layer)    |
|  +------+ +------+ +------+ +------+ +------+ +------+    |
|  | EDR  | |NDR/  | |CSPM/ | |CWPP/ | | DLP  | |ZTNA/ |    |
|  |EDR   | |IDS   | |CIEM  | |CNAPP | |CASB  | | SWG  |    |
|  +------+ +------+ +------+ +------+ +------+ +------+    |
+-------------------------+-----------------------------------+
                          | Telemetry
+-------------------------v-----------------------------------+
|  Tier 1: 자산 & 데이터 (Identify & Classify)                 |
|  +----------+ +----------+ +----------+ +--------------+    |
|  | CMDB/ASM | |DLP/IRM   | |DSPM      | |Crypto/PKI    |    |
|  |(ServiceNow| |(MS Purview| |(Dig,     | | (DigiCert,   |    |
|  |  CMDB)   | |  Symantec)| | Cyera)   | |  HashiCorp   |    |
|  +----------+ +----------+ +----------+ +--------------+    |
+-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Tier 1: 자산 식별 및 분류** | Attack Surface 파악, 데이터 흐름 매핑 | CMDB(ServiceNow CMDB, Device42), Active Directory 쿼리(LDAP/SCIM), SaaS Shadow IT 탐지(CASB: Netskope, Zscaler), 데이터 분류 자동화(MS Purview Information Protection, Varonis, Cyera DSPM), PII/PHI/PCI 마스킹, 암호화 키 관리(KMS/HSM: AWS KMS, Thales Luna) |
| **Tier 2: 예방 통제 (Preventive)** | 공격 표면 축소, 취약점 제거 | **EPP/EDR**(CrowdStrike Falcon, SentinelOne, MS Defender for Endpoint): 커널 후킹, AMSI, ETW 기반 행위탐지 + ML 모델 95% 정확도 / **CSPM**(Wiz, Prisma Cloud): CIS Benchmark 1,200+ 규칙, IaC(Terraform) 스캔, 클라우드 설정 오류 자동 탐지 / **CWPP**: 워크로드 런타임 보호, 컨테이너 이미지 스캔(Trivy, Snyk) / **DLP**(Symantec DLP, MS Purview): Regex·Dictionary·Exact Data Match(EDM)·Fingerprint 기반 채널(email, HTTPS, USB, Printer) 통제 |
| **Tier 3: 탐지·대응 (Detective/Responsive)** | 이상행위 탐지, 자동화 대응 | **SIEM**(Splunk SPL 검색, Microsoft Sentinel KQL, Elastic EQL): 평균 TPS(Terra Bytes Per Second) 100+ 처리, UEBA 머신러닝 / **XDR**: EDR+NDR+Cloud+Email 통합 상관분석, **MITRE ATT&CK T-code 자동 매핑** / **SOAR**(Cortex XSOAR, Splunk SOAR): 300+ 플레이북 자동화, MTTR(Mean Time To Respond) 평균 28일 -> 30분 단축 |
| **Tier 4: 위협 인텔리전스 & 리스크 정량화** | 선제적 위협 예측, 위험 우선순위화 | **STIX 2.1 / TAXII 2.1** 프로토콜 기반 CTI(Cyber Threat Intelligence)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 465 / 800

<- **이전**: [464. IT 경영 관리 핵심 토픽 464번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/464_it_management_core_topic_464_exam_summary/)
**다음**: [466. IT 경영 관리 핵심 토픽 466번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/466_it_management_core_topic_466_exam_summary/) ->

---
