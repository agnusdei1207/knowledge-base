+++
title = "488. IT 경영 관리 핵심 토픽 488번 시험 요약 (IT Management Core Topic 488 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(SVS 34개 Practice), TOGAF ADM, ISO 27001/27701, ISO 20000, BSC-IT** 등 글로벌 표준 프레임워크를 기반으로, **Strategy -> Portfolio -> Architecture -> Project -> Service -> Risk -> Value**의 Value Chain을 통해 IT를 경영 자산(Strategic Asset)화 하는 것임.
> 2. **가치**: 정량적 성과로 **IT 예산 대비 ROI 15~25% 개선, MTTR 60% 단축(3,600분->1,440분), SLA 준수율 99.95% 달성, Change Failure Rate 5% 이하, Lead Time for Change 주 단위->일 단위**로 단축되며, 정성적으로는 **CEO-CIO 정렬(Alignment)**, **규제 준수(Compliance)**, **디지털 전환 가속화** 효과를 얻음.
> 3. **판단 포인트**: 핵심 Trade-off는 **①거버넌스(Control, 중앙집중형) vs 아키텍처 자율성(BizDevOps, 분산형), ②안정성(Stability, Change Advisory Board 다단계 승인) vs 속도(Speed, SRE Error Budget 99.9% SLO), ③표준화(Standard, One-size-fits-all) vs 맞춤화(Custom, Federated EA), ④내부통제(Preventive Control) vs 시장민첩성(Time-to-Market)** 4가지 축의 균형점 설계임.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험에서 빈출되는 IT 경영 관리 영역은 단순한 이론 암기가 아닌, **"프레임워크 간 상호운용성(Interoperability)"** 과 **"Value Realization(가치 실현)"** 관점에서 답해야 합격선이 됩니다. 2024년 기준 NCS(국가직무능력표준) 디지털 직무와도 연계되어, IT 경영 관리의 핵심은 **①전략 정렬(Strategic Alignment) ②가치 전달(Value Delivery) ③리스크 최적화(Risk Optimization) ④자원 관리(Resource Management) ⑤성과 측정(Performance Measurement)** — COBIT 2019의 5대 도메인으로 귀결됩니다.

과거(2000년대) IT 관리는 **"코스트 센터(Cost Center)"** 관점으로, **CAPEX(자본적 지출) 위주의 예산 통제, 부서별 독립 SI, 사일로(Silo)형 시스템, 연간 단위 변경 통제(CAB)** 중심이었습니다. 그러나 2015년 이후 클라우드, AI, 데이터 경제로 전환되며 **"Value Center / Business Enabler"** 로 재정의되었고, **FinOps(클라우드 비용 최적화), SRE(Service Reliability Engineering, Google 모델), Product Operating Model(제품 중심 조직), BizDevOps** 등 새로운 거버넌스가 등장했습니다. 기술사 답안에서는 이 **Paradigm Shift(코스트->밸류, CAPEX->OPEX+FinOps, 프로젝트->제품, 통제->자율+책임)** 4가지를 명확히 대비하여 서술해야 합니다.

```text
       [Legacy IT Management: 2000s]              [Modern IT Management: 2024+]
  +----------------------------------+      +----------------------------------+
  |  CFO-centric: "IT는 비용이다"      |      | CEO-CIO 정렬: "IT는 성장동력"        |
  |                                  |      |                                  |
  |  +---------+    +---------+      |      |   +--------+    +----------+     |
  |  | 사업부A  |    | 사업부B  |      |      |   | BizDev |    | Data&AI  |     |
  |  | (ERP-A) |    | (ERP-B) |      |      |   |  Ops   |    | Platform |     |
  |  +----+----+    +----+----+      |      |   +---+----+    +----+-----+     |
  |       | Silo         |           |      |       | Federated    |           |
  |  -----+--------------+---- IT    |      |  -----+--------------+-- IT      |
  |  중앙 IT(인프라·보안·헬프데스크)  |      |  중앙 Platform Team(공통기반)      |
  |  CAPEX, 연단위 예산, CAB 7단계   |      |  OPEX+FinOps, 분기 OKR, SRE SLO  |
  |  KPI: 가용성·예산집행률·결재건수 |      |  KPI: NSM·DORA·NPS·ROI·LTV      |
  +----------------------------------+      +----------------------------------+
                  |                                       |
                  +----------- Paradigm Shift ------------+
              ① Cost Center -> Value Center
              ② Project-centric -> Product-centric
              ③ Annual Plan -> Rolling Wave(3+3+3월 롤링)
              ④ Control-first -> Risk-based + Zero Trust
```

- **📢 섹션 요약 비유**: IT 경영 관리의 변화는 마치 **"회사 식당(사내 급식)" -> "구독형 도시락 서비스(매달 새로운 메뉴, 영양 분석 리포트 제공)"** 로 바뀐 것과 같습니다. 예전에는 연초에 메뉴와 예산을 정해놓고 비용을 통제했다면, 지금은 매월 고객(사업부)이 별점을 주고, KPI 대시보드(DORA, NSM)로 즉시 피드백하며, MRR·재구독률로 가치를 측정합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 표준 프레임워크는 각각 **관점(View)** 이 다르고, 실제 기업에서는 이들을 **레이어드(Layered) 구조**로 통합 운영합니다.

```text
                          +-----------------------------+
                          |     비즈니스 전략 / 목표        |  <- CEO, 이사회, BSC
                          |  (Vision, Mission, OKR)       |
                          +--------------+--------------+
                                         | Cascade
                          +--------------v--------------+
                          |  ① IT 거버넌스 (COBIT 2019)   |  <- 의사결정, 책임, 정렬
                          |   - Governance System        |
                          |   - 40 Governance/Management |
                          |     Objectives                |
                          |   - EDM(EDM01~05)            |
                          +--------------+--------------+
                                         | Design Factor->Portfolio
                          +--------------v--------------+
                          |  ② EA & 전략 (TOGAF ADM)      |  <- Target Operating Model
                          |   - Preliminary->A~H->Req.Mgmt |
                          |   - ADM Cycle (Iterative)     |
                          +--------------+--------------+
                                         | Roadmap
                          +--------------v--------------+
                          |  ③ PM/Agile (PMBOK7, SAFe)    |  <- Delivery Model
                          |   - Predictive / Hybrid /     |
                          |     Adaptive                  |
                          |   - PI Planning, ART         |
                          +--------------+--------------+
                                         | Transition
                          +--------------v--------------+
                          |  ④ 운영/서비스 (ITIL 4 SVS)    |  <- Service Value Chain
                          |   - 34 Practices              |
                          |   - Plan->Engage->Design->       |
                          |     Transition->Obtain->Build->  |
                          |     Deliver&Support           |
                          +--------------+--------------+
                                         | Measure & Improve
                          +--------------v--------------+
                          |  ⑤ 보안/리스크 (ISO 27001, NIST)|  <- Assurance
                          |   - ISMS-P, RMF, Zero Trust  |
                          |   - 114 Control(ISO 27001:2022)|
                          +-----------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① COBIT 2019 거버넌스 시스템** | IT 의사결정 체계 및 책임 할당 | **Governance/Management Objectives 40개**(EDM 5, APO 14, BAI 11, DSS 6, MEA 4), **Design Factors 11개**(전략, 목표, 리스크, 규모 등), **Focus Area(예: DevOps, RPA, Cyber Security)**, **Cascade Goals**(Enterprise->Alignment->Risk->Process->Skill) 메커니즘. 2019부터 **Customizable** + **Open Source**로 전환. |
| **② TOGAF ADM** | EA 수립 및 이행 로드맵 | **ADM(Architecture Development Method) Phase**: Preliminary->A(Vision)->B(Business)->C(Data/App)->D(Technology)->E(Opportunities)->F(Migration)->G(Implementation)->H(Change Mgmt)->Requirements Mgmt. **Artifact**: Architecture Building Block(ABB->SBB), **ADM Iteration**(Preliminary/Architecture/Transitions/Governance), **Content Framework**, **ArchiMate 3.2** 표기법. |
| **③ PMBOK 7 / SAFe / Scrum** | 프로젝트/제품 단위 가치 전달 | **PMBOK 7(2021)**은 Process-based->**Principle-based(12 Principles) + 8 Performance Domains** 전환. **SAFe 6.0**: 7 Core Values, **PI(Program Increment) Planning 8~10주 주기**, ART(Agile Release Train, 보통 50~125명), **5 Core Configurations**(Essential~Large Solution). 핵심 지표: **DORA Metrics**(Deployment Freq, Lead Time, MTTR, Change Fail Rate), **Flow Metrics**(WIP, Flow Time, Flow Velocity). |
| **④ ITIL 4 SVS** | 서비스 가치 사슬 운영 | **Service Value System**: Opportunity/Demand->Value->SVS(Guiding Principles 7개, Governance, Practices, Continual Improvement)->Value. **34 Practices**(General 14, Service 17, Technical 3) 중 핵심: Incident Mgmt, Problem Mgmt, Change Enablement(3단계: Normal/Standard/Emergency), Service Request, Service Level, Continual Improvement. **Four Dimensions of Service Mgmt**(Org&People, Information&Tech, Partners&Suppliers, Value Streams&Processes). |
| **⑤ ISO 27001:2022 + 27701** | 정보보안 및 개인정보 경영체계 | **93 Annex A 통제항목**(2022 4 domains: Organizational 37, People 8, Physical 14, Technological 34). **ISMS-P(한국)**: 인증기준 102개 + 통제항목 80여개. **Statement of Applicability(SoA)** 의무화. **PIMS(Privacy)** = ISO 27701(개인정보연결고리 통제: PII Controller/Processor 통제). 한국 **개인정보보호법(제29조 안전조치)**과 매핑 필수. |

**핵심 메커니즘 — "Value Realization Loop"**: **Portfolio(투자 결정) -> Architecture(표준/로드맵) -> Project(실행) -> Service(운영) -> Value(성과 측정) -> Continual Improvement(CSI) -> Portfolio 재투자**. 이 루프가 **6~12개월 주기**로 돌아야 IT가 진정한 Value Center가 됩니다. 기술사 답안에서 자주 출제되는 **"Moore's Maturity Model(계획->실행->측정->관리->최적화)"**, **"CMMI 5단계"**, **"COBIT Cascade Goals"** 를 섞어 서술하면 고득점입니다.

- **📢 섹션 요약 비유**: 5대 프레임워크는 **"건물의 설계-시공-입주-관리-보안 시스템"** 처럼 한 덩어리입니다. **COBIT**는 도시계획(어떤 건물 짓기), **TOGAF**는 건축설계(평면·구조), **PMBOK/SAFe**는 시공(공정표·안전관리), **ITIL**는 입주 후 관리(청소·보수·민원), **ISO 27001**은 CCTV·출입통제(보안) 입니다. 이 중 어느 하나만 강화해도 무너집니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 **기술사 시험에 빈출되는 비교 이슈**는 ① COBIT vs ITIL ② PMBOK vs SAFe vs Scrum ③ EA: TOGAF vs Zachman vs FEAF ④ ISO 27001 vs NIST CSF ⑤ CAPEX vs OPEX+FinOps ⑥ BSC vs OKR 입니다.

| 구분 | COBIT 2019 | ITIL 4 |
| :--- | :--- | :--- |
| **관점(View)** | **What**(무엇을 다룰 것인가, 거버넌스/관리 목표) | **How**(어떻게 서비스 가치를 창출/유지할 것인가) |
| **도입 목적** | **거버넌스·정렬·책임(RACI)** 중심, 이사회 보고용 | **운영 효율·사용자 경험·SLA** 중심, 실무자용 |
| **구조** | **40 Goals × 5 Domains**(EDM/APO/BAI/DSS/MEA) | **34 Practices** + SVS(Service Value System) |
| **측정** | **Process Capability(0~5)** + **CSF/KPI** | **Practice Maturity + 4D + Value Stream** |
| **연계** | 상위(전략/거버넌스) | 하위(서비스 운영) |
| **적용 시점** | 정책 수립, 감사업무, 컴플라이언스 | 헬프데스크, Change, Incident 대응 |

| 구분 | PMBOK 7 (Predictive/Hybrid) | SAFe 6 (Adaptive at Scale) | Scrum (Team-level) |
| :--- | :--- | :--- | :--- |
| **적용 규모** | 단일 프로젝트(중대형) | 엔터프라이즈(50~1000+) | 팀(3~9명) |
| **주체** | PMP(Project Manager) | RTE(Release Train Engineer), PM | Scrum Master, PO |
| **기간/주기** | Phase Gate(Stage Gate) | PI(8~12주) + Iteration(2주) | Sprint(1~4주) |
| **계획/추정** | WBS, EVM(Earned Value) | WSJF(Weighted Shortest Job First), Roadmap | Story Point, Velocity |
| **리스크** | Risk Register + Reserve | ROAM(Resolved/Owned/Accepted/Mitigated) | Sprint Retrospective |
| **지표** | SPI/CPI, EAC | **DORA + Flow Metrics** | Velocity, Burndown |

| 구분 | TOGAF 9.2/10 | Zachman 6x6 | FEAF (US Federal) |
| :--- | :--- | :--- | :--- |
| **행/열** | ADM Phases | What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Operational | 5 Reference Models
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 488 / 800

<- **이전**: [487. IT 경영 관리 핵심 토픽 487번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/487_it_management_core_topic_487_exam_summary/)
**다음**: [489. IT 경영 관리 핵심 토픽 489번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/489_it_management_core_topic_489_exam_summary/) ->

---
