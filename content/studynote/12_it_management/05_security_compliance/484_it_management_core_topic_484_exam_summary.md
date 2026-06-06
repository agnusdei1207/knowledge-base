---
title: "IT Management Core Topic 484 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스·관리 목표 40개), ITIL 4(SVS 34개 실무 가이드), ISO 38500(6원칙 모델)을 통합해 **전략-아키텍처-서비스-리스크-포트폴리오** 5계층을 한 개의 Value Stream으로 연결하는 경영 체계이며, BSC/KPI/RAF(Responsible-Accountable-Consulted-Informed) 기반의 정량 거버넌스가 핵심이다.
> 2. **가치**: McKinsey 2023 survey 기준成熟 IT 거버넌스 도입 기업은 **Time-to-Market 38% 단축, IT 비용 대비 ROI 2.4배, Critical Incident MTTR 61% 감소, 컴플라이언스 위반 74% 절감** 효과를 얻으며, ISACA 통계에서는 COBIT 2019 적용 조직의 프로젝트 성공률이 비적용 대비 **28%->71%**로 향상된다.
> 3. **판단 포인트**: 중앙집중式(CoE + Center-Led) vs 분권式(BU별 자율) 모델 선택, Agile/DevOps 적용 시 거버넌스 경량화(SIG Light vs Full COBIT) trade-off, CapEx/OpEx 혼합 비율(클라우드 70% 이상 시 FinOps 강제), 그리고 사이버 리스크 ISO 27005·NIST CSF 2.0 매핑 강도는 사업의 **Criticality Tier(Tier 0~3)**에 따라 달라진다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management, 이하 ITM)는 1990년대 후반 *Strategic Alignment Model* (Henderson & Venkatraman, 1999)에서 출발하여, 2000년대 *IT Governance Institute (ITGI)*의 COBIT 4.0, 2012년 COBIT 5, 2018년 COBIT 2019로 진화해왔다. 기술사 시험 484번은 이러한 **거버넌스-전략-서비스-리스크-포트폴리오** 5대 축을 통합적으로 이해하고, 실제 기업의 IT 투자(연 평균 매출의 3.5~5.2%, Gartner 2024), 디지털 전환(DX), 그리고 사이버 회복력(Resilience)을 동시 최적화하는 능력을 평가한다.

핵심 과제는 (1) **사장과 CIO의 전략 갭** — McKinsey 분석에 따르면 글로벌 500대 기업의 67%가 IT-사업 정렬 실패를 겪고, (2) **Shadow IT의 폭증** — 평균 대기업의 IT 지출 중 35%가 비인가 영역(Gartner 2023), (3) **규제 복잡성** — 개인정보보호법, ESG 공시, DORA(유럽), AI Act, NIS2 등 동시 다발적 컴플라이언스, (4) **클라우드/AI 전환에 따른 CapEx->OpEx** 모델 변화이다. 기술사는 이를 한 장의 거버넌스 청사진으로 통합 설계할 수 있어야 한다.

```text
+--------------------------------------------------------------------------+
|                  IT 경영 관리 5계층 통합 아키텍처 (ISA-Lite)               |
|                                                                          |
|  +------------ Tier 0: Stakeholder & Value ------------+                 |
|  |  Board | CEO | CFO | CIO | CISO | CDO | 사업부서장  |                 |
|  |      <-> (BSC, OKR, Risk Appetite Statement)          |                 |
|  +------------------------------------------------------+                 |
|                          |                                                |
|  +------------ Tier 1: Strategy & Governance ----------+                 |
|  |  ◈ ISO 38500 6원칙  ◈ COBIT 2019 EDM(5개 목표)      |                 |
|  |  ◈ ITIL 4 SVS       ◈ 정책·표준·예산 배분            |                 |
|  +------------------------------------------------------+                 |
|                          |                                                |
|  +------------ Tier 2: Architecture & Portfolio -------+                 |
|  |  ◈ TOGAF 10 ADM     ◈ Zachman 6x6       ◈ EA Repo   |                 |
|  |  ◈ PMO + PPM Tool (Planview, Clarity)               |                 |
|  +------------------------------------------------------+                 |
|                          |                                                |
|  +------------ Tier 3: Service & Delivery --------------+                 |
|  |  ◈ ITIL 4 34 Practice ◈ DevOps(SRE) ◈ FinOps        |                 |
|  |  ◈ SLM/SLM/SLO (예: Availability 99.95%, RTO 4h)    |                 |
|  +------------------------------------------------------+                 |
|                          |                                                |
|  +------------ Tier 4: Risk, Security & Compliance ----+                 |
|  |  ◈ ISO 27001/27005   ◈ NIST CSF 2.0(6 Function)     |                 |
|  |  ◈ DORA/K-ISMS-P    ◈ BCP/DR (RTO/RPO)              |                 |
|  +------------------------------------------------------+                 |
|                                                                          |
|  <--------- Continuous Feedback: KPI, RASCI, Internal Audit ---------->     |
+--------------------------------------------------------------------------+
```

과거(2000년대)에는 **"IT는 비용 센터"** 라는 인식 하에 **ITIL v2**(9권 분량, 프로세스 중심) + **COBIT 4.0**(34개 IT 프로세스 통제)이 개별 사일로로 운영되어, Change Advisory Board에서 87%가 수동 승인, 평균 Lead Time 23일이 발생했다. 현대의 **2024~2026년 패러다임**은 **"IT는 Value Engine"** 으로, **COBIT 2019**(40 Governance/Management Objectives, 7 Component, Focus Area 11개) + **ITIL 4**(34 Practices, Value Stream 중심) + **ISO 38500**(6 Governance Principles)을 하나의 통합 거버넌스 체계로 운영하며, **Site Reliability Engineering**(Google SRE 모델, Error Budget), **FinOps**(cloud cost allocation), **DevSecOps**(shift-left security)를 내장한다. 결과적으로 **Change Lead Time은 23일 -> 4.2시간, Deployment Frequency는 월 1회 -> 일 4.7회, Change Failure Rate 15% -> 0.8%**(DORA 2023 State of DevOps Report Elite 기준)로 개선된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **공항 관제탑(Tower)** 과 같다. 비행기(프로젝트·서비스·데이터)가 수시로 이착륙하지만, ①활주로(아키텍처)·②관제사(거버넌스 위원회)·③레이더(모니터링 KPI)·④비상대응(BCP/DR)·⑤유료탑승구(FinOps)가 모두 정밀하게 맞물려야 **연착륙(IT 장애)·충돌(규제 위반)·연료 낭비(예산 초과)** 없이 운영된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **COBIT 2019의 5 Domains × 7 Components × 11 Focus Areas** 매트릭스를 ITIL 4 Value Stream과 ISO 38500 6원칙으로 **Bridge** 하는 것이다. 아래는 **EDM(Evaluate, Direct, Monitor) -> APO(Align, Plan, Organize) -> BAI(Build, Acquire, Implement) -> DSS(Deliver, Service, Support) -> MEA(Monitor, Evaluate, Assess)** 의 5 Domain을 중심으로 한 작동 메커니즘이다.

```text
+--------------------------------------------------------------------------+
|        COBIT 2019 Governance/Management Objective Flow (5 Domain)         |
|                                                                          |
|   Board & Exec      CIO/Steering       Architecture     Service Ops      |
|   Committee         Committee          Review Board     Center (SOC)      |
|       |                  |                   |                |           |
|       v                  v                   v                v           |
|  +--------+        +--------+          +--------+      +--------+       |
|  |  EDM   |-------->|  APO   |---------->|  BAI   |------>|  DSS   |       |
|  |  (5)   |        | (14)   |          |  (11)  |      |  (6)   |       |
|  +---+----+        +----+---+          +----+---+      +----+---+       |
|      |                  |                   |                |           |
|      |                  v                   v                v           |
|      |           +------------------------------------------------+      |
|      |           |              MEA (4) — Monitoring Loop          |      |
|      +----------->|  Performance | Compliance | Risk | Internal    |      |
|                  |  Measurement | Audit      | Mgt  | Control     |      |
|                  +----------------+-------------------------------+      |
|                                   |                                      |
|                                   v                                      |
|                       +--------------------+                            |
|                       |  Continuous Improve |                            |
|                       |  (PDCA + ITIL CSI)  |-----> EDM(feedback)         |
|                       +--------------------+                            |
+--------------------------------------------------------------------------+

   ◈ 40 G/O Objective  ◈ 7 Component (Process, Org, Info, People, Skill, Service, Infrastructure)
   ◈ NCSF/Togaf Map   ◈ Design Factor 11개  ◈ Capability Level 0~5
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·CIO 위원회 수준 거버넌스 의사결정 | COBIT 2019 EDM01~05(예: EDM02 Ensured Benefits Delivery, RACI=Board/CEO); ISO 38500 Principle 1~6 매핑; **Risk Appetite Statement(RAS)** 기반 의사결정 임계값(예: Critical Incident 발생 시 30분 내 CEO 보고) |
| **APO (Align, Plan, Organize)** | IT 전략-사업 정렬, 포트폴리오, 예산, 아키텍처 수립 | APO01~14(예: APO04 Managed Innovation, APO12 Managed Risk); **TOGAF 10 ADM**(Preliminary -> A->H -> Requirements Mgmt 8단계, 30% 빠른 Phase C/E 재사용); **Balanced Scorecard** 4관점(Financial/Customer/Internal Process/Learning) + Strategy Map |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·구현·테스트·전환 | BAI01~11(예: BAI03 Managed Solutions, BAI11 Managed Projects); **SAFe 6.0**(PI Planning, ART, 11개 Core Value), **DORA 4 Metrics**(Lead Time, Deploy Freq, MTTR, Change Fail %), **Shift-Left Testing**(SonarQube SAST, OWASP ZAP DAST) |
| **DSS (Deliver, Service, Support)** | 일일 운영·서비스 품질·사용자 지원 | DSS01~06(예: DSS02 Managed Service Requests, DSS05 Managed Security Service); **ITIL 4 34 Practice 중 14개** 적용(SLM, Incident, Problem, Change Enablement, Service Desk), **SRE SLO/SLI**(예: SLI=체크아웃 성공률, SLO=99.95%->Error Budget 월 21.9분) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정, 내부 통제, 컴플라이언스, 내부 감사 | MEA01~04(예: MEA03 Managed Compliance, MEA04 Managed Assurance); **KGI/KPI/CSFs** 3-tier 측정(예: KGI=매출 증가율, KPI=시스템 가용성 99.95%, CSF=Active-Active DR 구성), **COSO 2013 Internal Control** 17원칙 × 5 Component |
| **7 Component System** | 거버넌스 7가지 활성화 요소 | Process(PRM Maturity Level 0~5), Organizational Structures(Steering Committee, PMO, SMO, CoE), Information Flows(Decision Package, COBIT 2019 Cascade Goals), People·Skills·Competencies(SFIA 8 Framework 122 Skills), Services & Infrastructure(ServiceNow, Jira Align, Archer GRC) |
| **Focus Area(11개)** | 전략적 우선순위(예: 사이버보안, 클라우드, ESG, AI 거버넌스) | Cybersecurity Focus Area(NIST CSF 2.0 매핑), Cloud Focus Area(CMF/CNCF), Data Mgmt(DAMA-DMBOK 2.0 11 지식영역), DevOps, Digital Transformation, ESG-IT, Risk, Information Security, Privacy(K-PIPA), Regulatory(AI Act) |
| **Design Factor(11개)** | 거버넌스 시스템 맞춤형 설계 변수 | Enterprise Strategy(Agile/Conservative), Enterprise Size(SMB vs Large), Role of IT(Support/Factory/Strategic), Sourcing(Insource/Outsource/Cloud), Compliance(PIPL, GDPR, K-PIPA), IT Implementation Methods(Agile/DevOps/Traditional) -> **N=2^11 = 2,048개 시스템 형태 가능** |

핵심 작동 원리는 **Goal Cascade**(40개 Governance/Management Objective를 Business Goal -> Alignment Goal -> IT Goal로 3-tier 연결, 1:N 매핑)와 **Capability Level(0: Incomplete ~ 5: Optimizing)** 이다. 2024년 ISACA 발표에 따르면 글로벌 평균 Capability Level은 **2.3 (Performed->Managed)**, Elite 조직은 **4.1 (Quantitative)**, 한국 대기업 평균은 **2.7**로, **Maturity 갭이 1.8 level**에 달한다. 이를 좁히기 위해 **Process Reference Model(PRM)**의 40개 프로세스 중 우선 8~12개를 선정, **Quick-Win(6개월) + Foundation(12개월) + Optimization(24개월)** 의 3-Wave 로드맵을 권고한다.

또한, **COBIT 2019은 ISO/IEC 38500의 6 Govern 모델(Evaluate, Direct, Monitor, Accountability, Responsibility, Competence)을 EDM에 1:1 매핑**하며, ITIL 4의 **Service Value System(SVS)** — Opportunity/Demand -> Value -> Value Stream(34 Practice) -> Continual Improvement — 와 **Governance(EDM)** Layer로 연결된다. 기술사 시험에서는 이 **3 Framework Integration Map**을 그릴 수 있어야 한다.

- **📢 섹션 요약 비유**: **COBIT의 5 Domain**은 회사의 **5개 부서**(전략실/기획실/개발실/운영실/감사실)이고, **ITIL 4의 34 Practice**는 **34가지 업무 메뉴판**이며, **ISO 38500의 6원칙**은 **회사의 헌법**이다. 기술사는 이 셋을 한 장의 조직도에 모아 CEO가 한 번에 볼 수 있도록 그려야 한다.

---

## Ⅲ. 비교 및 연결

아래는 **IT 경영 관리의 3대 핵심 프레임워크(COBIT 2019, ITIL 4, ISO 38500)** 과, 자주 혼동되는 **PMBOK 7 / PRINCE2 / ISO 21502, TOGAF, COSO ERM 2017, NIST CSF 2.0, IT4IT**와의 비교이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500:2015** | **PMBOK 7 (2021)** | **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 484 / 800

<- **이전**: [483. IT 경영 관리 핵심 토픽 483번 시험 요약](/studynote/12_it_management/05_security_compliance/483_it_management_core_topic_483_exam_summary/)
**다음**: [485. IT 경영 관리 핵심 토픽 485번 시험 요약](/studynote/12_it_management/05_security_compliance/485_it_management_core_topic_485_exam_summary/) ->

---
