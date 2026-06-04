+++
title = "697. IT 경영 관리 핵심 토픽 697번 시험 요약 (IT Management Core Topic 697 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리의 핵심은 **COBIT 2019 기반 거버넌스 체계**, **ITIL 4 서비스 가치 체계(SVS)**, **TOGAF ADM 아키텍처 개발 방법론**을 통합하여 **전략(Strategy) -> 포트폴리오(Portfolio) -> 프로그램(Program) -> 프로젝트(Project) -> 운영(Operation)**의 End-to-End 가치 사슬을 구축하는 것이다.
> 2. **가치**: McKinsey(2023) 보고에 따르면成熟的한 IT 거버넌스 체계 보유 기업은 **EBITDA 마진 8~12%p 향상**, **프로젝트 성공률 67%->82% 개선**, **TCO(Total Cost of Ownership) 평균 23% 절감**, **Time-to-Market 35% 단축**의 정량적 효과를 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스**, **② Waterfall vs Agile 거버넌스**, **③ Build vs Run 예산 배분(70:30 -> 50:50 전환)**, **④ 표준화(Standardization) vs 혁신(Innovation)**이며, 기업 성숙도(CMMI 1~5)와 산업별 규제 강도(Banking/Healthcare/Public)에 따라 최적점(Optimal Point)이 동적으로 변한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험 697번은 **"IT 경영 관리"** 영역의 종합적 주제를 다루며, 핵심은 **IT-비즈니스 전략 정렬(Strategic Alignment)**, **IT 가치 실현(Value Realization)**, **리스크 관리(Risk Management)**, **자원 최적화(Resource Optimization)**, **성과 측정(Performance Measurement)**의 5대 영역을 아우르는 통합 프레임워크 구축 능력을 평가한다.

기존 IT 관리는 **기술 중심(Technology-Centric)**의 **"Build-and-Run"** 패러다임으로, 각 부서·시스템 단위로 독립적 운영되어 **사일로(Silo) 현상**, **중복 투자(Redundancy)**, **Shadow IT**, **ROI 불명확성** 문제를 야기했다. 반면 현대 IT 경영은 **"Outcome-Driven"**, **"Product-Centric"**, **"Platform Thinking"** 패러다임으로 전환되어, **Wardley Maps**, **Value Stream Mapping**, **OKR(Objective and Key Results)** 기반의 가치 흐름 최적화가 필수적이다.

특히 **COVID-19 이후 가속화된 Digital Transformation(DX)**, **생성형 AI(Generative AI)**, **클라우드 네이티브(Cloud-Native)**, **규제 변화(EU AI Act, DORA, CSAP)** 등 VUCA 환경에서 IT 경영 관리는 단순 비용센터(Cost Center)에서 **전략적 가치센터(Value Center)**로 그 역할이 근본적으로 재정의되고 있다.

```text
[ 전통 IT 관리(Old Paradigm) vs 현대 IT 경영(New Paradigm) 아키텍처 ]

   +---------------------------------+         +---------------------------------+
   |  [Old] 1990~2010 IT 관리 구조  |         |  [New] 2020~2030 IT 경영 구조   |
   |                                  |         |                                 |
   |   CEO                              |         |   CEO                           |
   |    |                               |         |    |                            |
   |   CFO -- CIO -- IT Dept          |         |   CDO/CIO -- CoE(Center of Ex)  |
   |         |        |                |         |    |      |      |              |
   |         |   +----+----+           |         |    |   Biz  Tech Data  Risk     |
   |         |   |    |    |           |  ----►   |    |    |   |     |      |      |
   |       Dev  Ops  Sec  Infra       |         |  Product  Platform Squad Tribe |
   |       (분절/사일로)              |         |  (DevOps+GitOps+Platform Eng)  |
   |                                  |         |                                 |
   |   - CapEx 80% / OpEx 20%         |         |   - FinOps 기반 Pay-as-you-go  |
   |   - 연 1회 계획 / 연 단위 예산    |         |   - 분기 OKR / 월 단위 재배분   |
   |   - 프로젝트 중심 / TCO 불명     |         |   - 제품 중심 / 가치 흐름 측정  |
   |   - 내부 통제 중심 / 소극적      |         |   - 외부 가치+ESG+리스크 통합   |
   +---------------------------------+         +---------------------------------+
```

**📢 섹션 요약 비유**: 기존 IT 관리가 **각 부서마다 따로 짓고 따로 관리하는 마을**(분산된 우물, 개별 발전소)이었다면, 현대 IT 경영은 **상하수도·전기·도로가 통합된 스마트시티**의 도시계획(Urban Planning)에 비유할 수 있습니다. 도시계획가가 어디에 도로를 내고, 발전소를 세울지 통합 설계하듯, CIO/CDO가 기업 전체의 IT 가치 흐름을 통합 설계하는 것이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 표준 아키텍처는 **ISO/IEC 38500 IT 거버넌스 국제표준**을 최상위 프레임으로 하고, **COBIT 2019**(거버넌스/관리 목표), **ITIL 4**(서비스 운영), **CMMI**(성숙도), **ISO 27001**(보안), **ISO 20000**(서비스), **TOGAF**(아키텍처), **PMBOK 7th/PRINCE2**(프로젝트), **SAFe/Scrum@Scale**(애자일)을 하위 레이어로 통합하는 **레이어드 거버넌스 아키텍처(Layered Governance Architecture)**이다.

```text
[ 통합 IT 경영 관리 아키텍처 (Layered Governance Architecture) ]

    +--------------------------------------------------------------------+
    |  Layer 0: 원칙 및 윤리 (Principles & Ethics)                       |
    |  +--------------------------------------------------------------+  |
    |  | ISO/IEC 38500 (6원칙) | OECD Guidelines | UNGPs | AI Ethics |  |
    |  | Responsibility | Strategy | Acquisition | Performance | Conformance | Human |
    |  +--------------------------------------------------------------+  |
    +--------------------------------------------------------------------+
    |  Layer 1: 거버넌스 체계 (Governance System)                         |
    |  +--------------------------------------------------------------+  |
    |  |   Board/CISO  --►  Audit Committee  --►  STEER Committee   |  |
    |  |           |                |                    |            |  |
    |  |   +------+------+  +------+------+  +--------+--------+    |  |
    |  |   | Strategy    |  | Risk Mgmt   |  | Value Delivery  |    |  |
    |  |   | Committee   |  | Committee   |  |   Office        |    |  |
    |  |   +-------------+  +-------------+  +-----------------+    |  |
    |  +--------------------------------------------------------------+  |
    +--------------------------------------------------------------------+
    |  Layer 2: 관리 체계 (Management System) - COBIT 2019 EDM/APR/BAI/DSS/MEA |
    |  EDM: Evaluate, Direct, Monitor  | 5 Governance Objectives        |
    |  APR: Align, Plan, Organize (13) |  BAI: Build, Acquire, Implement(11)|
    |  DSS: Deliver, Service, Support(6) | MEA: Monitor, Evaluate, Assess(5)|
    +--------------------------------------------------------------------+
    |  Layer 3: 운영 프레임워크 (Operational Frameworks)                  |
    |  +----------+  +----------+  +----------+  +----------+          |
    |  |  ITIL 4  |  |  DevOps  |  |  FinOps  |  |  MLOps   |          |
    |  |  SVS     |  |  +SRE    |  |  +Green  |  |  +AIOps  |          |
    |  | 34 Prac. |  | CALMR    |  | Inform   |  | Model    |          |
    |  +----------+  +----------+  +----------+  +----------+          |
    +--------------------------------------------------------------------+
    |  Layer 4: 실행 체계 (Execution)                                     |
    |  Portfolio(SAFe LPM) -> Program -> Project(Agile/Waterfall) -> Squad |
    +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (40 Governance/Management Objectives)** | IT 거버넌스/관리 목표 체계를 5개 도메인(EDM, APR, BAI, DSS, MEA) × 40개 objective로 표준화 | **EDM(5)**: 거버넌스 의사결정·감독 / **APR(13)**: 전략·포트폴리오·조직 정렬 / **BAI(11)**: 솔루션 식별·구축·전환 / **DSS(6)**: 운영·지원·보안 / **MEA(5)**: 성과·내부통제·규제 준수 측정. **핵심 11개 관리목표**(예: DSS01 managed operations, DSS02 managed service requests, BAI03 managed solutions, MEA01 performance)을 기업 상황에 따라 우선순위화(Design Factors 11종) |
| **ITIL 4 Service Value System (SVS)** | IT 서비스의 End-to-End 가치 사슬 정의 | **7 Guiding Principles**(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize) / **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) / **34 Practices**(일반 14, 서비스 17, 기술 3) |
| **OKR + KPI + KRI 통합 측정 체계** | 목표·성과·리스크 통합 측정 | **Leading Indicator**(DORA Metrics: Deployment Frequency, Lead Time, MTTR, Change Failure Rate)와 **Lagging Indicator**(CSAT, NPS, Revenue Impact, ROI, NPV) 결합. **Balanced Scorecard 4관점**(Financial, Customer, Internal Process, Learning&Grow) 적용 |
| **FinOps Framework (FinOps Foundation)** | 클라우드 비용 최적화 및 가치 극대화 | 3단계 라이프사이클(Inform->Optimize->Operate) / **단위 경제학(Unit Economics)**: Cost per Transaction, Cost per Customer, Cost per API Call / **할당(Allocation)·예측(Forecasting)·이상탐지(Anomaly Detection)·Showback/Chargeback** / CFM(Cloud FinOps) 도구: CloudHealth, Vantage, Apptio, Kubecost |

**핵심 동작 메커니즘 - 워드포크(Workforce) 정렬 루프**:

```text
[IT-Business 정렬 6단계 루프 (Strategy-to-Execution Loop)]

  ① Strategy Decomposition    :  기업전략 -> IT 임팩트 맵핑 (e.g., Bain Strategy Map)
                                v
  ② Portfolio Prioritization  :  BCG Matrix + Wardley Map + RICE Scoring
                                v
  ③ Funding & Governance      :  Stage-Gate + Zero-Based Budgeting + Continuous Funding
                                v
  ④ Execution & Delivery      :  SAFe LPM(Lean Portfolio Mgmt) + PI Planning + Scrum
                                v
  ⑤ Operation & Value Capture :  SRE + FinOps + AIOps + Customer Journey Analytics
                                v
  ⑥ Feedback & Adaptation     :  OKR Review + Retrospective + Strategy Refresh (Quarterly)
                                v (loop back to ①)
```

**📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **대형 화물선의 항해 시스템**과 같습니다. **나침반(COBIT)**, **항로도(TOGAF)**, **엔진룸 운영 매뉴얼(ITIL)**, **연료 관리 시스템(FinOps)**, **승무원 훈련 매뉴얼(CMMI)**이 모두 통합되어야 목적지(비즈니스 가치)에 안전히 도착할 수 있습니다. 어느 하나만 잘 만들어서는 배가 침몰합니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 개념들은 서로 밀접하게 연결되면서도 명확한 차이가 있다. 시험에서 자주 혼동되는 개념을 명확히 구분해야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **IT 거버넌스 (Governance)** | **IT 관리 (Management)** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | 거버넌스+관리 통합 프레임워크 | 서비스 운영 최적화 프레임워크 | 의사결정·감독·책임·통제 체계 | 계획·실행·모니터링 운영 체계 |
| **대상** | 엔드투엔드(IT 전영역) | 주로 IT 서비스 운영(Operation) | 이사회·경영진·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 697 / 800

<- **이전**: [696. IT 경영 관리 핵심 토픽 696번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/696_it_management_core_topic_696_exam_summary/)
**다음**: [698. IT 경영 관리 핵심 토픽 698번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/698_it_management_core_topic_698_exam_summary/) ->

---
