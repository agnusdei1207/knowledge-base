---
title: "513. IT 경영 관리 핵심 토픽 513번 시험 요약 (IT Management Core Topic 513 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 513. IT 경영 관리 핵심 토픽 513번 시험 요약 (IT Management Core Topic 513 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance, ITG)는 COSO/COBIT 2019/ISO 38500 기반의 **3단계 거버넌스(Governance-Risk-Compliance, GRC)** 체계 아래, 기업의 **전략적 IT 포트폴리오(Strategic IT Portfolio)**, **IT 서비스 카탈로그(ITSCE)**, **전사적 자원관리(ERP)**, **프로젝트 관리(PMBOK/PRINCE2)** 를 통합 운영하는 경영 프레임워크이다.
> 2. **가치**: McKinsey 2023 보고 기준 디지털 성숙도 Top-quartile 기업은 매출 성장률 2.6배(연평균 11% vs 4.2%), TCO 27% 절감, Time-to-Market 41% 단축의 정량 효과를 달성하며, ISACA 연구에서는 COBIT 2019 도입 기업 78%가 **IT-Risk 사각지대 53% 감소**, 감사 지적 사항 62% 감소를 입증했다.
> 3. **판단 포인트**: **①** Balanced Scorecard 4관점 재무/고객/내부/학습균형(BSC)  vs **COBIT 2019 40개 거버넌스/관리 목적(GO/MG)**, **②** 중앙 집중형(CoE) vs **Bimodal IT( Mode 1/2)**, **③** ITSM 도구(Cherwell/ServiceNow/Remedy) 선택 시 **TCO 5년 누적 비용**, **④** 프로젝트 관리 방법론 **Waterfall vs Agile(Scrum/Kanban) vs 하이브리드(SAFe/DA)**, **⑤** 위험관리 **위험 매트릭스(L×I 5×5)** 의 조직 역량 매핑 — 이 5대 의사결정 축이 기술사의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

정보기술의 **전략적 투자 규모**가 글로벌 GDP 대비 5.2%(IDC 2023, 약 4.6조 USD)를 돌파하면서, IT 투자의 ROI 검증, IT 위험 통제, 서비스 품질 보장이 단순 운영 이슈가 아닌 **이사회(Board) 의사결정 사항**으로 격상되었다. 과거 2000년대 초반의 IT 거버넌스 부재(예: SOX Act 2002, Enron 사건) 는 재무제표 신뢰성 붕괴라는 기업 존폐의 위기로 이어졌으며, 이를 계기로 **COSO-ERM(Enterprise Risk Management, 2004)**, **COBIT 2019**, **ISO/IEC 38500(2015)** 등 글로벌 표준이 체계화되었다. 4차 산업혁명(AI, IoT, Blockchain, Cloud) 환경에서는 **디지털 트랜스포메이션(Digital Transformation, DT)** 이 핵심 전략 변수가 되었고, 이에 따라 IT-Balanced Scorecard(BSC), Portfolio Rationalization, FinOps(Financial Operations), DevSecOps 같은 **신경영관리 패러다임**이 등장했다.

기존 패러다임: **기술 중심(Technology-Centric)** — “시스템이 안정적이면 잘 관리된 것”
신규 패러다임: **가치 중심(Value-Driven IT Governance)** — “전략-투자-성과-위험의 폐루프(Closed-Loop) 실현”

```text
  +-------------------------------------------------------------+
  |  IT 경영 관리의 4대 축(Eisner & Blobel, 2014 변형)        |
  |                                                             |
  |          +--------------+                                  |
  |          |  전략 연계    | <- Balanced Scorecard, EA(TOGAF) |
  |          | (Alignment)  |                                  |
  |          +------+-------+                                  |
  |                 | 화살표(양방향)                              |
  |                 v                                          |
  |   +--------------------------+   +------------------+      |
  |   |   가치(Value) 실현       | <-->|  위험(Risk) 관리 |      |
  |   | - ROI, NPV, EVA          |   | - ISO 27005      |      |
  |   | - FinOps, TBM            |   | - NIST CSF       |      |
  |   | - IT-BSC 4관점           |   | - KRIs, KCIs     |      |
  |   +------------+-------------+   +--------+---------+      |
  |                |                          |                |
  |                v                          v                |
  |         +--------------------------------------+            |
  |         |  성과(Performance) 측정 및 개선       |            |
  |         |  - KPI(CSF), SLA, OLAs, SLOs         |            |
  |         |  - CMMI, ITIL 4 34개 Practice         |            |
  |         |  - COBIT 2019 Capability Level(0~5)  |            |
  |         +--------------------------------------+            |
  +-------------------------------------------------------------+

  * 폐루프(Closed-Loop) 전략-실행-측정-개선(PDCA + Deming Cycle)
  * 이사회 -> CISO/CDO/CIO -> PMO -> CoE -> 실무 PM/엔지니어
```

기술사적 관점에서 IT 경영관리는 **①** IT 전략이 경영전략과 1:1로 매핑(Strategy Map) 되어야 하고, **②** ISO/IEC 38500의 6원칙(책임, 전략, 인수, 성과, 규칙, 인간행위) 이 의사결정 프레임으로 작동해야 하며, **③** 모든 IT 투자가 **TBM(Tech Business Management)** 의 **Technology Tower(Application/Infrastructure/Service/Project)** 단위로 비용·가치·품질 가시화되어야 한다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **“항공우주국의 통합 관제 시스템”** 과 같다 — 우주선(IT 시스템)이 비행(운영)하기 전, 발사 계획(전략), 관제탑(거버넌스), 지상관제(서비스 운영), 비상대응(리스크) 이 모두 실시간 통합되어야 임무 성공이 보장된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### (1) IT 거버넌스(Governance) 3계층 구조

```text
  +------------------------------------------------------------+
  |  [Tier 1] 이사회 / 경영진 (Board / Executive)              |
  |  +- 역할: 의사결정, 감독, 책임(E = "Evaluate")              |
  |  +- 도구: 전략맵, IT-BSC, Risk Appetite Statement          |
  |  +- 산출물: IT Strategy, IT Charter, Risk Tolerance        |
  |          |                                                 |
  |          v (P = "Plan & Prepare")                          |
  |  +----------------------------------------------------+   |
  |  |  [Tier 2] 거버넌스 협의회 / IT Steering Committee   |   |
  |  |  +- 역할: 방향성 결정, 우선순위, 예산 배분          |   |
  |  |  +- 도구: COBIT 2019 EDM(40개 GO 중 5개)         |   |
  |  |  |        - EDM01 Governance Framework            |   |
  |  |  |        - EDM02 Benefits Delivery               |   |
  |  |  |        - EDM03 Risk Optimization               |   |
  |  |  |        - EDM04 Resource Optimization            |   |
  |  |  |        - EDM05 Stakeholder Transparency         |   |
  |  |  +- 산출물: Portfolio Charter, Architecture Roadmap |   |
  |          |                                                 |
  |          v (O = "Operate" via COBIT 2019 MG)               |
  |  +----------------------------------------------------+   |
  |  |  [Tier 3] 운영 조직 (PMO / SMO / CoE / DevOps)    |   |
  |  |  +- 역할: 일일 운영, 서비스 제공, 모니터링          |   |
  |  |  +- 도구: ITIL 4 SVS, PMBOK 7th, DevOps Pipeline   |   |
  |  |  +- 산출물: SLA, Run Book, Change Record            |   |
  |  +----------------------------------------------------+   |
  +------------------------------------------------------------+
```

### (2) COBIT 2019 핵심 메커니즘

COBIT 2019는 **6원칙 + 40 Governance/Management Objectives** + **7 Component(Principles/Goals/Systems/Risk/Metrics/Components/Succcess)** 구조다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance System(거버넌스 시스템)** | 이사회의 책임 영역(E,D,M 중 **E·D**) | 5개 EDM 도메인(EDM01~05), 요구사항 이해관계자-목표-위험-자원-규제 매핑, **Focus Area**(예: 사이버보안, BCP, DevOps, 위험, 규정 준수) 32개 사전 정의 |
| **Management System(관리 시스템)** | C-level/실무 책임 영역(**P·B·R·M** = Plan, Build, Run, Monitor) | 5개 도메인 **APO**(Align Plan Organize 13개), **BAI**(Build Acquire Implement 11개), **DSS**(Deliver Service Support 6개), **MEA**(Monitor Evaluate Assess 4개), 총 35개 MG 목표 |
| **Component Model(7요소)** | 거버넌스 시스템의 7가지 구성 | ① Process, ② Organizational Structure(3-Lines Model: 운영/리스크·컴플/내부감사), ③ Information Flows, ④ People/Skills/Roles(RACI), ⑤ Principles/Policies/Frameworks, ⑥ Culture/Ethics/Behavior(Tone at the Top), ⑦ Services/Infrastructure/Applications |
| **Capability Level(0~5)** | 성숙도 평가(Process PAM 기반) | 0(불완전) -> 1(초기) -> 2(관리) -> 3(설정) -> 4(예측) -> 5(혁신). **PAM 2-5 영역**(Process, Information, People, Technology) 별로 측정 |
| **Goals Cascade(목표 연쇄)** | 13개 Enterprise Goal -> 13개 Alignment Goal -> 40개 GO/MG | “EG01 포트폴리오 경쟁우위” -> “AG01 IT 준수·지원” -> “APO02 관리 전략” 식으로 자동 매핑. **Implementation Guide I&T 이슈 7대 영역**: Benefits Realization, Risk Optimization, Resource Optimization, … |
| **Design Factor(설계 요인 11개)** | 거버넌스 시스템 맞춤화 | ① Enterprise Strategy, ② Goals, ③ Risk Profile, ④ I&T 이슈, ⑤ Threat Landscape, ⑥ Compliance Requirements, ⑦ IT Role(Support/Factory/Strategic/Factory), ⑧ Sourcing Model, ⑨ IT Implementation Methods, ⑩ Technology Adoption, ⑪ Size(Enterprise Size) |

### (3) IT-Balanced Scorecard(4관점 + 4성과면)

Kaplan & Norton의 BSC를 IT에 적용한 **Van Grembergen(2000)** 모델은 다음과 같다.

```text
  +--------------+   +--------------+
  | 재무(Financial) |   | 고객(Customer) |
  | 관점           |   | 관점          |
  | - IT 비용률    |   | - 사용자 만족 |
  | - ROI/ROA     |   | - SL 만족도   |
  | - 예산 준수율  |   | - CSAT/NPS   |
  +-------+-------+   +-------+------+
          | 화살표            |
          v                   v
  +--------------+   +--------------+
  | 내부프로세스  |   | 학습/성장    |
  | (Internal)   |   | (Learning)   |
  | - 변경 성공률 |   | - 직원 교육  |
  | - 인시던트   |   | - 핵심역량   |
  | - PM 성공률  |   | - 혁신 지수  |
  +--------------+   +--------------+

  * 4대 균형 = Lead(선행) vs Lag(후행) 지표
  * Strategy Map(전략맵): 4관점 인과관계(원인->결과) 시각화
  * Theme(전략주제) 4~6개 권장 (Strategy Focused Org, 2005)
```

### (4) ITSM(IT Service Management) — ITIL 4 Service Value System

ITIL 4(2019, AXELOS) 의 **SVS(Service Value System)** 은 5대 컴포넌트가 **Opportunity/Demand -> Value** 로 변환하는 폐루프 시스템이다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SVS(Service Value System)** | 전체 가치 흐름 | Opportunity/Demand -> Engage -> Offer(Portfolio/Service/Product) -> **Service Value Chain(Plan/Improve/Engage/Design&Transition/Obtain/Build/Deliver&Support)** -> Value |
| **Guiding Principles(9대 지침)** | 의사결정 원칙 | ① Focus on Value, ② Start Where You Are, ③ Progress Iteratively with Feedback, ④ Collaborate and Promote Visibility, ⑤ Think and Work Holistically, ⑥ Keep It Simple and Practical, ⑦ Optimize and Automate, ⑧ Make the Whole Journey, ⑨ Start the Journey |
| **4P + 4D(Products/Services/Systems/WOW × Plan/Design/Operate/Improve)** | 거버넌스 적용 영역 | 4P(Products/Services/Systems/Way of Working) 와 4D(Plan/Design/Operate/Improve) 의 매트릭스로 거버넌스/관리 적용 |
| **34개 Practice** | 실행 단위 | ① Service Desk, ② Incident Mgmt, ③ Problem Mgmt, ④ Change Enablement, ⑤ Service Request Mgmt, ⑥ Service Level Mgmt, ⑦ Continual Improvement, ... ⑨ Monitoring/Event Mgmt, ⑩ Release Mgmt, ⑪ Deployment Mgmt, ... ⑩ Portfolio Mgmt, ⑪ Architecture Mgmt, ⑫ Risk Mgmt, ⑬ Supplier Mgmt, ⑭ Information Security, ... ⑮ Service Configuration Mgmt, ⑯ IT Asset Mgmt, ⑰ Knowledge Mgmt 등 |
| **Capability Model(CSF + KPI)** | 측정 및 개선 | 4-Level Capability: 0(Incomplete) -> 1(Performed) -> 2(Managed) -> 3(Defined) -> 4(Quantitatively Managed) -> 5(Optimizing) |

### (5) IT 포트폴리오 관리(IT Portfolio Management, ITPM)

```text
  [IT 투자 포트폴리오의 3대 축]
  +-------------------------------------------------+
  |  Application Portfolio  (애플리케이션)           |
  |  +- Quadrant Matrix: 운영 효율 vs 전략 가치     |
  |  +- Time-to-Market, TCO, 기술 부채, Risk       |
  |  +- App Modernization (Rehost/Refactor/Rebuild) |
  |  ------------------------------------------    |
  |  Infrastructure Portfolio  (인프라/클라우드)     |
  |  +- Hybrid(Multi) Cloud: AWS+Azure+GCP/On-prem|
  |  +- FinOps: Cloud 비용 가시화(Showback/Charge) |
  |  +- CapEx->OpEx 전환, TBM(Tech Business Mgmt)  |
  |  ------------------------------------------    |
  |  Project/Program Portfolio  (프로젝트/프로그램) |
  |  +- NPV/IRR/Payback/Benefit-Cost Ratio         |
  |  +- 포트폴리오 분산: 분산효과 + 집중도         |
  |  +- Stage-Gate(Killian) / Lean Startup Canvas  |
  +-------------------------------------------------+

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 513 / 800

<- **이전**: [512. IT 경영 관리 핵심 토픽 512번 시험 요약](/studynote/12_it_management/05_security_compliance/512_it_management_core_topic_512_exam_summary/)
**다음**: [514. IT 경영 관리 핵심 토픽 514번 시험 요약](/studynote/12_it_management/05_security_compliance/514_it_management_core_topic_514_exam_summary/) ->

---
