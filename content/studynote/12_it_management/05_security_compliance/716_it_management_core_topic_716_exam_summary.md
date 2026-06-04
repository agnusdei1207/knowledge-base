+++
title = "716. IT 경영 관리 핵심 토픽 716번 시험 요약 (IT Management Core Topic 716 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 716번 토픽은 **IT 거버넌스(COBIT 2019) ↔ 전략 포트폴리오 ↔ 디지털 전환(DX) ↔ IT 성과평가(BSC/OKR/KPI)**를 하나의 통합 프레임워크로 연결하여, **EA(Enterprise Architecture) 기반 투자우선순위(Weighted Scoring Model)**, **PMO 운영**, **R&R/RACI**, **Balanced Scorecard 4관점**, **OKR/MBO**, **AGILE/DevOps**를 통해 IT-Business Value Chain을 정량화하는 경영 관리 체계임.
> 2. **가치**: COBIT 2019 적용 시 **IT-비즈니스 정렬도 30~45% 향상**, BSC 4관점 KPI 운영 시 **프로젝트 ROI 20~35% 개선**, IT 거버넌스 성숙도 모델(IT-CMF, CMMI-SVC) Level 2->4 도달 시 **운영 비용 15~25% 절감**, EA 기반 투자포트는 **중복투자 40% 제거 및 ROI 2.5배 향상** 효과 검증.
> 3. **판단 포인트**: **거버넌스 모델(중앙집중/연방형/하이브리드)** 선택 시 조직 규모·산업 특성·규제 강도 고려, **BSC vs OKR**은 안정성·혁신성 trade-off, **Cloud-First vs On-Premise 우선**은 TCO·데이터 주권·legacy 의존성 trade-off, **Agile 도입 시 Spotify Model vs SAFe vs LeSS**는 팀 규모·문화적 수용성·규제 요건에 따른 선택.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(716번)는 단순한 "IT 운영"이 아닌, **기업의 전략적 목표(SO: Strategic Objective)를 IT 투자·프로세스·아키텍처·인적자원으로 변환(Value Chain Mapping)하고, 정량적 KPI/BSC로 성과를 측정·피드백하여 거버넌스 체계를 지속적으로 개선(Continuous Improvement Loop)**하는 경영 과학입니다.

기존(Pre-Digital) 환경에서는 IT가 "지원 부서(Back Office)"로 인식되어 **CapEx 일회성 투자 + Capex/Opex 분리 회계** 위주로 관리되었고, CIO는 "데이터센터 운영자" 수준에 그쳤습니다. 그러나 **4차 산업혁명(AI, Cloud, IoT, Blockchain, Data Analytics)** 으로 인해 IT가 **"Business Differentiator"**로 격상됨에 따라, 경영진은 **IT 투자 대비 비즈니스 가치(ROIT: Return on IT Investment)** 를 요구하게 되었고, 이를 위해 **IT 거버넌스 프레임워크(COBIT 2019, ITIL 4, TOGAF, PMBOK 7)** 와 **성과관리 체계(BSC, OKR, KPI Tree)** 통합이 필수화되었습니다.

```text
   +----------------------------------------------------------------------+
   |         716번 IT 경영 관리 통합 프레임워크 (Strategic -> Tactical)      |
   +----------------------------------------------------------------------+

   +-----------------------+         +--------------------------+
   |  1. 경영 전략 (CEO)    |         | 2. IT 거버넌스 위원회     |
   |  - 비전/미션/BSC 상위  |<--------->|  - CIO, CFO, CDO, COO   |
   |  - 3~5년 Strategic Map |         |  - 이사회 산하 Risk&Audit|
   +---------+-------------+         +----------+---------------+
             |                                   |
             v                                   v
   +-----------------------+         +--------------------------+
   | 3. EA(Enterprise       |         | 4. IT 투자 포트폴리오     |
   |    Architecture)       |<--------->|  - Demand Pipeline       |
   |  - TOGAF ADM 9 Phase   |         |  - Weighted Scoring      |
   |  - BIZ/APP/DATA/TECH   |         |  - NPV/IRR/Payback 분석  |
   +---------+-------------+         +----------+---------------+
             |                                   |
             v                                   v
   +-----------------------+         +--------------------------+
   | 5. 프로젝트 실행       |         | 6. 성과 측정 & 피드백     |
   |  - PMO(프로젝트/프로  |<--------->|  - BSC 4관점 KPI         |
   |    그램/포트폴리오)    |         |  - OKR/MBO/EFQM         |
   |  - Agile/SAFe/Waterfall|         |  - PDCA/DMAIC            |
   +---------+-------------+         +----------+---------------+
             |                                   |
             +---------------+-------------------+
                             v
                +--------------------------+
                | 7. Continuous Improvement |
                |  - CSI(Continual Service  |
                |    Improvement) ITIL 4    |
                |  - COBIT 2019 Cascade    |
                |    Goals (13) -> Alignment|
                |    Goals (13) -> Mgmt     |
                |    Objectives (40)        |
                +--------------------------+
```

기술사 시험 관점에서 716번은 **"어떻게 IT를 경영의 핵심으로 끌어올려 ROI를 정량화할 것인가"** 에 대한 답을 요구합니다. 단순히 "BSC 4관점"을 외우는 것이 아니라, **금융권의 FinOps, 제조업의 Smart Factory, 공공의 G-Cloud 전환** 등 도메인별 적용 차이를 보여주어야 합니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판(스피도미터·연료계·엔진RPM)**과 같습니다. 운전자가 직접 엔진을 볼 수 없듯이, CEO가 IT 현장을 다 알 수 없으므로 **KPI(속도), ROIT(연비), BSC(종합 대시보드)** 같은 계기판이 필요합니다. COBIT 2019는 이 계기판의 **표준화된 디자인 규약(ISO)**이라 할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 3축 아키텍처

IT 거버넌스는 **(1) Decision Rights(의사결정 권한)**, **(2) Accountability(성과 책임)**, **(3) Transparency(투명성·감사)** 의 3축으로 구성됩니다. COBIT 2019는 이를 40개의 관리 목적(Management Objectives)과 5개 도메인(EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess)으로 체계화합니다.

```text
   +--------------- COBIT 2019 Cascading Goals (의사결정 캐스케이드) -------------+
   |                                                                            |
   |  Enterprise Goals (13)                                                     |
   |  +------------------------------------------------------------+            |
   |  | EG01 Portfolio of Competitive Products & Services          |            |
   |  | EG06 Business Service Continuity & Availability            |            |
   |  | EG12 Managed Digital Transformation Programs                |            |
   |  | EG13 Innovation & Emerging Technologies                    |            |
   |  +------------------------+-----------------------------------+            |
   |                           | I↔T 관련성 매핑 (Primary/Secondary)              |
   |                           v                                                |
   |  Alignment Goals (13)                                                      |
   |  +------------------------------------------------------------+            |
   |  | AG01 I&T Compliance & Support                              |            |
   |  | AG04 Managed Information & Data Assets                      |            |
   |  | AG09 Resource Optimization (FinOps)                         |            |
   |  | AG11 Enabled & Supported Change                             |            |
   |  | AG12 Knowledge, Skills & Behaviors                          |            |
   |  +------------------------+-----------------------------------+            |
   |                           |                                                |
   |                           v                                                |
   |  Management Objectives (40) + Component: Process/Org Structure/Info Flow  |
   |  +------------------------------------------------------------+            |
   |  | EDM01 Governance Framework Setting & Maintenance            |            |
   |  | EDM02 Benefits Delivery (ROI/Payback/IRR)                   |            |
   |  | EDM03 Risk Optimization (R=R=I×V×Likelihood)                |            |
   |  | APO02 Strategy & Portfolio Management                       |            |
   |  | APO05 Managed Workforce (역량/성과평가)                      |            |
   |  | BAI03 Manage Solutions (Agile/SAFe/Waterfall)                |            |
   |  | DSS02 Managed Service Requests & Incidents                  |            |
   |  | MEA01 Performance & Conformance Monitoring                  |            |
   |  +------------------------------------------------------------+            |
   +----------------------------------------------------------------------------+
```

### 2. IT 투자 우선순위 결정 모델 (Weighted Scoring Model)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Demand Intake Portal** (Jira/ServiceNow PPM) | 비즈니스 부서의 IT 수요 수집·분류 | 비즈니스 케이스 작성 (Strategic Fit, Business Value, Risk, Cost, Time) -> 자동 점수화 (5개 기준 × 1~5점) |
| **② EA Architecture Review** (TOGAF ADM Phase A~F) | 솔루션 아키텍처 적합성 검증 | **ATAM(Architecture Trade-off Analysis Method)** 활용, 비기능 요건(NFR: Scalability, Security, Availability) 7개 항목 평가 |
| **③ Weighted Scoring Engine** | 정량 우선순위 산출 | **AHP(Analytic Hierarchy Process)** 일관성 비율 CR<0.1, 가중치: 전략정합성 30%, ROI 25%, 리스크 20%, 긴급성 15%, 자원 가용성 10% |
| **④ Financial Analysis** (NPV/IRR/Payback) | 재무적 타당성 분석 | **DCF(Discounted Cash Flow)**: NPV = Σ(CFₜ/(1+r)ᵗ) - I₀, **Hurdle Rate** 일반 12~15%, **Payback Period** 3~5년 이내 |
| **⑤ Portfolio Balancing** | 전략적 포트폴리오 분산 | **BCG Matrix 적용**: Stars(고성장-고점유), Cash Cows(저성장-고점유), Question Marks(고성장-저점유), Dogs(저성장-저점유) 배분 |

### 3. 성과관리 핵심 원리 (BSC + OKR + KPI)

**Balanced Scorecard (BSC)**는 Kaplan & Norton이 제안한 4관점(Financial, Customer, Internal Process, Learning & Growth) 프레임워크이며, **Strategy Map**을 통해 인과관계(Cause-Effect Chain)를 시각화합니다. **OKR(Objectives & Key Results)** 는 Andy Grove(Intel)에서 시작되어 Google이 도입한 **"Stretch Goal + 0.7 달성률"** 기반의 Agile 성과관리 도구입니다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Strategic Map** | 전략 인과관계 시각화 | Learning->Process->Customer->Financial 상향식 인과 (예: "직원 역량^ -> 프로세스 효율^ -> 고객만족^ -> 매출^") |
| **② KPI Tree** (Top-down 분해) | 조직 KPI -> 개인 KPI 연결 | **SMART 원칙**(Specific, Measurable, Achievable, Relevant, Time-bound), **KPI 분해**: 기업 KPI -> BU KPI -> 부서 KPI -> 개인 KPI (SmartSheet, Anaplan 활용) |
| **③ BSC Scorecard** | 4관점 정량 측정 | Financial(ROE, EBITDA), Customer(NPS, CSAT, Churn Rate), Process(Lead Time, MTTR), Learning(직원교육시간, Retention Rate) |
| **④ OKR Cycle** (Quarterly) | 분기 단위 Agile 목표 관리 | Objective(질적 목표, 3~5개) + Key Results(정량 결과, 각 3~4개), Google/OKR Dashboard(WorkBoard, Ally.io) 활용, Review 주기 1주/1월/1분기 |
| **⑤ RACI Matrix** | 역할·책임 명확화 | Responsible(수행), Accountable(책임, 1명), Consulted(자문), Informed(통보) — **Single A 원칙** (책임은 반드시 1명) |

### 4. PMO(Project/Program/Portfolio Management) 3계층 구조

PMO는 **Project Management Office(프로젝트 관리)** -> **Program Management(관련 프로젝트 묶음, 시너지 추구)** -> **Portfolio Management(전략 정합성, 자원배분)** 의 3계층으로 구성되며, Gartner는 PMO를 **Supportive PMO / Controlling PMO / Directive PMO** 3유형으로 분류합니다.

- **📢 섹션 요약 비유**: IT 거버넌스는 **항공 관제탑(ATC)**과 같습니다. COBIT 2019가 **국제 항공 표준**, BSC가 **이륙·순항·착륙 단계별 계기**, PMO가 **관제탑 요원**, EA가 **공항 청사진**입니다. 관제탑이 없으면 항공기는 충돌하고, 거버넌스 없으면 IT 투자는 "산발적 발사"되어 비즈니스 가치 없이 추락합니다.

---

## Ⅲ. 비교 및 연결

### 1. IT 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** (ISACA) | **ITIL 4** (AXELOS) | **ISO 27001/38500** | **CMMI-SVC** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 (What/Why) | IT 서비스 운영 (How) | 보안·이사회 거버넌스 표준 | 조직 성숙도 모델 |
| **구조** | 5도메인, 40관리목적, 7컴포넌트 | 34 Practice, 4 Dimension, SVS | 27001(Annex A 93 통제), 38500(거버넌스 원칙 6개) | 5 Level(1~5), 22 Process Area |
| **적용 범위** | Enterprise 전체 I&T | IT Service(Operate/Deliver) | 정보보안 + 의사결정 거버넌스 | 서비스 조직 역량 진단 |
| **강점** | **Cascading Goals** 통한 비즈니스 정렬, **40 Design Factors** 맞춤형 거버넌스 설계 | **Service Value System(SVS)**, Value Stream 중심, Agile·DevOps·SIAM 통합 | **법적 컴플라이언스** 강제, 국제 인증 | **정량적 성숙도** 측정(소프트웨어 신뢰성 등) |
| **약점** | 구현 가이드 부족
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 716 / 800

<- **이전**: [715. IT 경영 관리 핵심 토픽 715번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/715_it_management_core_topic_715_exam_summary/)
**다음**: [717. IT 경영 관리 핵심 토픽 717번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/717_it_management_core_topic_717_exam_summary/) ->

---
