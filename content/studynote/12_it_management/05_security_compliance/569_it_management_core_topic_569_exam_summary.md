---
title: "569. IT 경영 관리 핵심 토픽 569번 시험 요약 (IT Management Core Topic 569 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 569번은 **IT 거버넌스(COBIT 2019), IT 서비스 관리(ITIL 4), 전략적 성과 관리(Balanced Scorecard), 엔터프라이즈 아키텍처(TOGAF/Zachman), IT 포트폴리오 관리(APM)** 등 5대 프레임워크를 통합적으로 운용하여 기업의 디지털 전환(DX) 가치사슬(Value Chain)을 최적화하는 경영 체계임.
> 2. **가치**: McKinsey(2023) 조사에 따르면 5대 프레임워크를 통합 적용한 기업은 **DX 성공률 35%->78%**, IT 투자 ROI **2.4배**, 인시던트 MTTR **62% 단축**, 컴플라이언스 감사 비용 **40% 절감**의 정량 효과를 달성하며, 정보시스템 감리(IT Audit) 및 ISMS-P 인증에서도 핵심 평가 항목으로 활용됨.
> 3. **판단 포인트**: 프레임워크 간 중복 영역(예: COBIT의 EDM vs ITIL의 Strategy)의 **역할 중복(Role Overlap)** 문제, Agile/DevOps 환경에서 무거운 거버넌스 프로세스 적용 시 **속도 저하(Governance Overhead)** 트레이드오프, 그리고 ESG·AI 윤리 규제 대응을 위한 **동적 거버넌스 모델(Dynamic Governance)**로의 전환 여부를 의사결정 핵심으로 판단해야 함.

---

## Ⅰ. 개요 및 필요성

**IT 경영 관리**는 단순한 IT 운영을 넘어, 기업의 **전략적 목표(Strategic Goals)** 와 **IT 서비스·자산·프로세스**를 정렬(Alignment)시켜 비즈니스 가치를 극대화하는 경영 활동의 총칭임. 기술사 시험 569번 토픽은 다음 5대 축을 통합적으로 다룸:

1. **IT 거버넌스(Governance)**: COBIT 2019, ISO/IEC 38500 기반 의사결정 구조
2. **IT 서비스 관리(Service Management)**: ITIL 4 SVS(Service Value System)
3. **전략적 성과 관리**: Balanced Scorecard(BSC), OKR
4. **엔터프라이즈 아키텍처(EA)**: TOGAF ADM, Zachman Framework
5. **IT 포트폴리오·프로젝트 관리**: SAFe, APM(Agile Portfolio Management)

### 🎯 등장 배경 및 기술적 도전

과거(2000년대)에는 **COBIT 4.1 + ITIL v3 + PMBOK 5th**로 대표되는 **사일로(Silo)형 거버넌스**가 주류였음. 그러나 2015년 이후 클라우드 전환, Agile/DevOps, GDPR·AI Basic Act 같은 규제 폭증, 그리고 COVID-19 이후의 비대면 업무 가속화로 인해 다음의 **3대 도전**이 발생함:

| 도전 과제 | 구체적 증상 | 정량 영향 |
|:---|:---|:---|
| **프레임워크 파편화(Framework Sprawl)** | COBIT, ITIL, ISO27001, NIST CSF, PCI-DSS 등 중복 통제 항목 연간 1,200건 이상 발생 | 감리 인력 1인당 생산성 35% 저하 |
| **Agile-DevOps 속도 vs 거버넌스 저항** | Scrum Sprint(2주) vs Change Advisory Board(CAB) 평균 승인 7일 | Time-to-Market 4.2배 지연 |
| **디지털 윤리·ESG 규제 미비** | AI 결정의 설명가능성(XAI), 탄소 배출 측정, 공급망 SBOM 미흡 | EU AI Act 위반 시 매출의 7% 과징금 |

### 🏗️ 통합 거버넌스 참조 모델(IGRM: Integrated Governance Reference Model)

```text
                  +---------------------------------------------+
                  |   기업 미션·비전 (Corporate Mission/Vision) |
                  |   BSC 4관점: 재무/고객/내부/학습성장         |
                  +------------------+--------------------------+
                                     | 전략 매핑(Strategy Map)
                  +------------------v--------------------------+
                  |  ① EA 전략 (TOGAF ADM Phase A-H)            |
                  |    - 비즈니스 / 데이터 / 애플리케이션 / 기술 |
                  |    - Zachman 6x6 매트릭스                     |
                  +------------------+--------------------------+
                                     | 포트폴리오 라우팅
                  +------------------v--------------------------+
                  |  ② IT 거버넌스 (COBIT 2019 EDM)              |
                  |    - 40 Governance/Management Objectives     |
                  |    - EDM: Evaluate, Direct, Monitor          |
                  |    - 핵심 모델: Cascade Goals -> Issues ->    |
                  |      Process Practices -> Metrics             |
                  +------------------+--------------------------+
                                     | 거버넌스 목표 하달
       +-----------------------------+-----------------------------+
       |                             |                             |
+------v--------+           +--------v---------+          +-------v-------+
| ③ 서비스 운영 |           | ④ 프로젝트·Agile |          | ⑤ 리스크·컴플 |
| (ITIL 4 SVS)  |           |  (SAFe, PMBOK 7) |          | (ISO27001,    |
|  - SVC, 7 Guiding|         |  - ART, PI Plan  |          |  NIST CSF,    |
|    Principles   |         |  - Scrum/Kanban  |          |  ISO 38500)   |
+------+--------+           +--------+---------+          +-------+-------+
       |                             |                             |
       +-----------------------------+-----------------------------+
                                     |
                  +------------------v--------------------------+
                  |  📊 측정·개선 (Metrics & Feedback Loop)      |
                  |  - KPI/KRI/KCI / OKR Check-in              |
                  |  - Maturity Model: CMMI 2.0 (5단계)        |
                  |  - Continual Improvement (CSI Register)    |
                  +---------------------------------------------+
```

### 🆚 구 vs 신 패러다임 비교

| 구분 | 구 패러다임 (2000s) | 신 패러다임 (2024~) |
|:---|:---|:---|
| 거버넌스 구조 | 중앙 집중형, 계층적 CAB | 분산형, **Federated Governance** + GitOps Policy |
| 프로세스 문서 | Word/PDF 200페이지+ | **Lean PRD + Architecture Decision Record(ADR)** |
| 통제 방식 | 사후 감사(After-the-fact Audit) | **Continuous Control Monitoring(CCM)** + GRC 자동화 |
| 위험 관리 | 연 1회 위험 평가 | **실시간 KRI 대시보드** + Chaos Engineering |
| 인력 구조 | IT 전문가 분리 | **BizDevSecOps** + Platform Engineering 팀 |
| 기술 도구 | BMC Remedy, HP Service Manager | **ServiceNow ITSM, Jira Service Mgmt, Backstage(IDP)** |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"스마트시티의 통합 관제센터"** 와 같음. 교통(서비스), 건축(EA), 재정(BSC), 치안(거버넌스) 부서가 각자 노하우를 갖고 있지만, **한 화면에 통합**되어야 시민(사업)이 안전하고 빠르게 움직일 수 있음. 과거에는 각 부서가 **라디오로만 소통**했다면, 지금은 **5G 통합 관제 + AI 예측**으로 작동하는 것과 같음.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 🔧 5대 프레임워크 상세 아키텍처

#### 1) COBIT 2019 (Control Objectives for Information and Related Technologies)

- **40개 관리 목표(Management Objective)** + **5개 거버넌스 목표**를 5개 도메인(EDM, Align Plan Organize, Build Acquire Implement, Deliver Service Support, Monitor Evaluate Assess)으로 분류
- 핵심 사이클: **Cascade Goals(목표 계층화) -> Issues 식별 -> Process Practices 매핑 -> Metrics 측정**
- **Focus Area**: 일반·규제·위험·DevOps·정보보안·디지털 등 11개 맞춤형 영역
- **Design Factor 11개**로 시스템 조직에 최적화된 거버넌스 시스템 설계

```text
   +------------------- COBIT 2019 계층 구조 -------------------+
   |                                                          |
   |  Level 0: Stakeholder Needs (이해관계자 니즈)            |
   |            v                                              |
   |  Level 1: Enterprise Goals (13개 기업 목표)               |
   |            v  "Cascade Goals"                             |
   |  Level 2: Alignment Goals (13개 IT 정렬 목표)            |
   |            v  "Goals Cascade"                             |
   |  Level 3: Process / Component Goals (40 MG)              |
   |            v  "Process Practices"                         |
   |  Level 4: Activities / Metrics (RACI, KPI Tree)           |
   |                                                          |
   +----------------------------------------------------------+
```

#### 2) ITIL 4 (Information Technology Infrastructure Library v4)

- **SVS(Service Value System)**: Opportunity/Demand -> Value -> Value -> **7 Guiding Principles**(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize) -> 4 Dimensions(Organizations, Information, Value Streams, Partners) -> **Service Value Chain(SVC)** 6활동(Plan, Improve, Engage, Design&Transition, Obtain/Build, Deliver&Support)
- **34 Practices** (일반 14 + 서비스 17 + 기술 3)
- 변화: 프로세스 중심 -> **Value Stream** 중심, IT 서비스 -> **Product/Service Offering**

#### 3) TOGAF ADM (Architecture Development Method)

- **8 Phases**(Preliminary, A: Architecture Vision, B: Business, C: Information Systems, D: Technology, E: Opportunities, F: Migration Planning, G: Implementation Governance, H: Architecture Change Management) + **Requirements Management**(전 단계 공통)
- **ADM Cycle Iteration**으로 EA 거버넌스 지속
- Zachman 6x6 (What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Functioning Enterprise)

#### 4) Balanced Scorecard(BSC) & OKR

- **4 Perspective**: Financial(재무) / Customer(고객) / Internal Process(내부) / Learning&Growth(학습성장)
- **Strategy Map**으로 30~40개 목표의 인과관계(Causality) 시각화
- **OKR**: Objectives(질적) + Key Results(정량, 0.0~1.0 점수), 분기 단위

#### 5) SAFe / Agile Portfolio Management

- **5 Level**: Team -> Program(ART) -> Large Solution -> Portfolio -> Enterprise
- **PI Planning**(8~12주 단위), **Lean Portfolio Management(LPM)**: Strategic Themes -> Epic -> Lean Business Case -> WSJF(Weighted Shortest Job First) 우선순위

### 📊 통합 아키텍처 및 데이터 흐름

```text
   +-------------------------------------------------------------+
   |  전략 계층 (Strategy Layer)                                 |
   |  +--------------+   +--------------+   +--------------+    |
   |  |  BSC / OKR   |   |  ISO 38500   |   |  비즈니스    |    |
   |  |  4관점 목표  |   | 6 거버넌스   |   |  전략문서    |    |
   |  |              |   | 원칙(Evalu-  |   |              |    |
   |  |              |   | ate/Direct/  |   |              |    |
   |  |              |   | Monitor)     |   |              |    |
   |  +------+-------+   +------+-------+   +------+-------+    |
   |         |                  |                  |            |
   +---------+------------------+------------------+------------+
             |     Goals Cascade & Strategy Map     |
   +---------v------------------v------------------v------------+
   |  거버넌스 계층 (Governance Layer)                           |
   |  +------------------------------------------------------+  |
   |  |  COBIT 2019: 40 MG + 11 Design Factors               |  |
   |  |  EDM(5) -> APO(14) -> BAI(11) -> DSS(6) -> MEA(4)        |  |
   |  +------------------------------------------------------+  |
   |  +------------------------------------------------------+  |
   |  |  TOGAF ADM: 8 Phases + ADM Cycle                     |  |
   |  |  Architecture Repository(ABP, AS-IS, TO-BE, Gap)     |  |
   |  +------------------------------------------------------+  |
   +---------+--------------------------------------------------+
             |     Portfolio Backlog & Architecture Roadmap
   +---------v--------------------------------------------------+
   |  실행 계층 (Execution Layer)                               |
   |  +--------------+  +--------------+  +--------------+    |
   |  |  ITIL 4 SVC  |  |  SAFe ART    |  |  PMBOK 7     |    |
   |  |  6 Activity  |  |  PI Plan     |  |  8 Domains   |    |
   |  |  34 Practice |  |  Scrum/Kanban|  |  12 Principles|    |
   |  +------+-------+  +------+-------+  +------+-------+    |
   |         |                 |                  |            |
   |         +-----------------+------------------+            |
   |                           |                                |
   |                  DevOps Pipeline                           |
   |                  (CI/CD + GitOps + Policy as Code)        |
   +---------+--------------------------------------------------+
             |     Metrics & Feedback (KPI/KRI)
   +---------v--------------------------------------------------+
   |  측정·개선 계층 (Measurement Layer)                        |
   |  +----------------------------------------------------+   |
   |  | GRC Platform (ServiceNow GRC, Archer, OpenPage)    |   |
   |  | BI 대시보드 (Tableau, Power BI) + AIOps            |   |
   |  | CSI Register -> Continual Improvement Service (CIS) |   |
   |  +----------------------------------------------------+   |
   +-----------------------------------------------------------+
```

### 🗂️ 구성 요소별 역할·기술 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Governance Board (이사회/IT전략위원회)** | EDM 의사결정 | ISO 38500 6원칙, RACI 매트릭스, 분기별 Steering Committee, **Board Portal**(Diligent, Nasdaq Boardvantage) |
| **COBIT 2019 Process Model** | 통제 목표·지표 정의 | **Goals Cascade**, **CMMI 5단계 Maturity**, Process Capability(ISO 15504), **Radar Chart**(5축: Process, People, Technology, Information, Culture) |
| **TOGAF ADM** | EA 진화 관리 | **Architecture Repository**(ABP, AS-IS, TO-BE, Gap, SBB), ADM Cycle(반복), **Architecture Patterns**(AWS Well-Architected, Google CAF) |
| **ITIL 4 Service Value Chain** | 가치 흐름 관리 | **6 Activity × 34 Practice**, Value Stream Mapping, **SLA/OLA/UC** 3계층 계약, **CSI Cascade**(비전->전략->전술->운영) |
| **Balanced Scorecard** | 전략 성과 측정 | **4 Perspective × Strategy Map**, **Balanced Scorecard Hall of Fame**(1997~Norton-Kaplan), **Strategy Map**(인과 다이어그램) |
| **OKR System** | Agile 정렬 | **0.0~1.0 Grading**, **Quarterly Check-in**, **Weekly pCheck-in**, **CFR**(Conversation/Feedback/Recognition) |
| **SAFe LPM** | 포트폴리오 자금 흐름 | **Lean Budget Guardrails**(전략 테마별 에픽 자금), **WSJF = (Business Value + Time Criticality + Risk Reduction) / Job Size**, **Kanban WIP Limit** |
| **GRC Platform** | 통합 컴플라이언스 | **Policy as Code**(OPA, HashiCorp Sentinel), **Continuous Control Monitoring**(ServiceNow CCM), **Risk Register**, **Vendor Risk** (BitSight, SecurityScorecard) |
| **DevOps Toolchain** | 실행 자동화 | **GitOps**(ArgoCD/Flux), **CI/CD**(Jenkins, GitLab, GitHub Actions), **SBOM**(CycloneDX, SPDX), **SLSA L3**(공급망 보안) |
| **AIOps/FinOps** | 지능화·비용 최적화 | **AIOps**(Moogsoft
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 569 / 800

<- **이전**: [568. IT 경영 관리 핵심 토픽 568번 시험 요약](/studynote/12_it_management/05_security_compliance/568_it_management_core_topic_568_exam_summary/)
**다음**: [570. IT 경영 관리 핵심 토픽 570번 시험 요약](/studynote/12_it_management/05_security_compliance/570_it_management_core_topic_570_exam_summary/) ->

---
