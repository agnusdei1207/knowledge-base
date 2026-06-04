+++
title = "464. IT 경영 관리 핵심 토픽 464번 시험 요약 (IT Management Core Topic 464 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 성과관리 및 가치측정(Performance Management & Value Measurement)은 COBIT 2019의 EDM( Evaluate, Direct, Monitor) 영역, ITIL 4의 가치 흐름(Value Stream), BSC(Balanced Scorecard) for IT 프레임워크를 통합하여 IT 투자(TCO) 대비 실현된 비즈니스 가치(ROI, NPV, IRR)를 정량·정성적으로 측정·평가하는 거버넌스 체계이다.
> 2. **가치**: Forrester(2023) 및 Gartner(2024) 보고 기준, 체계적 IT 성과관리 체계 도입 기업은 IT 투자 회수 기간 평균 **38% 단축**, 프로젝트 실패율 **24% -> 9% 감소**, Shadow IT 비용 **연간 12~18% 절감**, 그리고 IT-Business Alignment 성숙도(ACEM 모델 기준) 평균 **Level 2.3 -> Level 3.7 향상** 효과를 달성한다.
> 3. **판단 포인트**: 핵심 Trade-off는 (a) **측정 정밀도 vs. 측정 비용**(과도한 KPI는 관료적 부담 유발, KPI 과소는 거버넌스 사각지대 발생), (b) **Lead Indicator vs. Lag Indicator** 균형, (c) **단기 ROI vs. 전략적 옵션 가치(Real Option Theory)**, (d) **정량 KPI vs. 정성적 비즈니스 효과**(예: Brand Equity, 고객만족도 NPS) — 기술사 판단 기준은 **CMMI/COBIT Maturity Level 3 이상**을 달성하면서 KPI 수를 **Tier별 5~7개**로 제한하는 것이다.

---

## Ⅰ. 개요 및 필요성

IT 투자 규모는 글로벌 연평균 4.8조 USD(2024, IDC)에 달하며, 한국 기업 IT 예산도 GDP 대비 약 3.2~4.1%를 차지한다. 그러나 McKinsey(2023) 조사에 따르면 **CIO의 68%가 "IT가 창출한 가치를 CEO/이사회에 정량적으로 증명하지 못한다"**고 답변했으며, 동일 조사에서 **IT 프로젝트 중 17%가 명시적 ROI 검증 없이 착수**되는 것으로 나타났다. 이는 IT가 **Cost Center -> Value Center**로 패러다임이 전환됨에도 불구하고, 가치 측정 체계(Value Realization Framework)가 IT 투자의 속도를 따라가지 못하는 **"Value Gap"** 문제 때문이다.

본 토픽(464)은 정보관리기술사 시험에서 **"IT 경영관리"** 영역의 핵심으로, IT 성과관리·투자대비성과분석·가치측정·Portfolio 관리·Maturity 평가·감리·BSC for IT 등을 통합적으로 다룬다. IT 거버넌스 국제 표준인 **COBIT 2019의 5 Governance Objectives(EDM 01~05)**, ITIL 4의 **7 Guiding Principles**, 그리고 **ISO/IEC 38500(Governance of IT)** 의 6개 원칙(Model, Principle, Policy, Practice, Conformance, Performance)을 IT 성과관리의 표준 레퍼런스로 활용한다.

```text
[IT 성과관리 및 가치측정 통합 프레임워크 아키텍처]

   +----------------------------------------------------------------+
   |                IT 거버넌스 의사결정 계층 (3-Tier)              |
   |                                                                |
   |   +------------------------------------------------------+    |
   |   |  Tier 1: 이사회/CEO (Governance)                      |    |
   |   |  - EDM01(Framework), EDM02(Benefits Delivery),       |    |
   |   |  - EDM03(Risk Optimization), EDM04(Resource),        |    |
   |   |  - EDM05(Stakeholder Transparency)                    |    |
   |   +------------------------------------------------------+    |
   |                            <-> 전략 연계                        |
   |   +------------------------------------------------------+    |
   |   |  Tier 2: CIO/CFO (Management)                        |    |
   |   |  - IT Portfolio Mgmt, IT-BSC, IT Financial Mgmt     |    |
   |   |  - EDM ↔ MEA(01~04) ↔ APO(01~14) ↔ BAI(01~11)      |    |
   |   +------------------------------------------------------+    |
   |                            <-> 운영 연계                        |
   |   +------------------------------------------------------+    |
   |   |  Tier 3: PM/Service Owner (Operational)              |    |
   |   |  - KPI/SLA 측정, Incident/MTTR, CSAT/NPS            |    |
   |   |  - DSS(01~06) ↔ BAI 측정 데이터 수집                 |    |
   |   +------------------------------------------------------+    |
   +----------------------------------------------------------------+
                  ^                                ^
        [정량 지표: ROI/NPV/IRR/CF]   [정성 지표: Brand/Agility/Innovation]
                  v                                v
   +----------------------------------------------------------------+
   |        통합 가치 측정 레이어 (Integrated Value Layer)          |
   |   +--------------+  +--------------+  +------------------+    |
   |   |  TCO 분석    |  |  BSC for IT  |  |  Benefit          |    |
   |   |  - CapEx/OpEx|  |  - 4 Perspectives|  - Benefit Plan   |    |
   |   |  - 5-Year    |  |  - Strategy Map|  - Realization    |    |
   |   |  - Risk-Adj. |  |  - KPI Cascade|  - Tracking        |    |
   |   +--------------+  +--------------+  +------------------+    |
   +----------------------------------------------------------------+
                  v
   [Reporting -> Board / CEO / CFO / Audit Committee / Regulator]
```

**기존 패러다임 vs. 신규 패러다임 비교**

| 구분 | 전통적 IT 관리 (Pre-2010) | 현대적 IT 경영관리 (2020~) |
|------|--------------------------|--------------------------|
| **관점** | IT는 비용(Cost Center) | IT는 가치(Value Center) |
| **측정** | 예산 소진율, 가용률(Availability) | ROI, NPV, IRR, BSC, EVA |
| **관리 범위** | 단일 시스템/프로젝트 | Enterprise IT Portfolio + Ecosystem |
| **의사결정** | CIO 독단적, 사후 보고 | 이사회 거버넌스 + 실시간 대시보드 |
| **평가 기준** | 일정/예산/범위(삼각형) | 비즈니스 성과 + 사용자 경험 + 혁신 |
| **리스크** | 무시(또는 보험) | Risk-Adjusted ROI, Real Option |
| **표준** | ITIL v2/v3, COBIT 4/5 | COBIT 2019, ITIL 4, ISO 38500, VeriSM |

- **📢 섹션 요약 비유**: IT 성과관리는 마치 **"회계 감사(Audit)에서 CFO가 CEO에게 보고하는 재무제표"** 와 같다. 단순히 돈을 썼는지가 아니라, **그 돈으로 얼마의 가치(이익, 현금흐름, 시장가치, 전략적 옵션)를 창출했는가**를 증명하는 "IT의 재무제표"를 만드는 작업이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 성과관리 시스템은 크게 **① 입력(Input) -> ② 처리(Process) -> ③ 출력(Output) -> ④ 피드백(Feedback)** 의 4단계闭环(Closed-Loop) 구조로 설계된다. COBIT 2019의 40개 Governance/Management Objectives 중 본 토픽과 직결되는 핵심 구성요소는 다음과 같다.

```text
[IT 성과관리 4단계 Closed-Loop 아키텍처]

   [1. Input Layer]           [2. Process Layer]
   +-------------+            +--------------------------+
   | 전략 입력   | --------->  | EDM02: Benefits Delivery |
   | - Biz Goal  |            | +- Benefit Plan 수립     |
   | - IT Goal   |            | +- KPI 정의 (Cascade)   |
   | - IT Risk   |            | +- Baseline 측정        |
   | - IT Budget |            | +- Realization Tracking  |
   +-------------+            +--------------------------+
                                       <->
   [4. Feedback Layer]        [3. Output Layer]
   +----------------------+   +--------------------------+
   | MEA01: Perf&Eval     | <-- | MEA02: Assurance        |
   | - 성과 vs 목표 분석  |   | +- Dashboard (Power BI)  |
   | - Gap 분석           |   | +- Board Report         |
   | - 개선 액션(PDCA)    |   | +- Audit Trail          |
   | - Maturity Re-assess |   | +- Regulatory Compliance|
   +----------------------+   +--------------------------+

   [데이터 흐름: ETL 파이프라인]
   IT 시스템(SAP, Salesforce, ServiceNow, Jira)
        -> API Gateway (REST/GraphQL)
        -> Data Lake (S3, ADLS Gen2)
        -> ETL (Informatica, dbt, Spark)
        -> Data Warehouse (Snowflake, BigQuery, Redshift)
        -> BI Layer (Tableau, Power BI, Looker)
        -> Executive Dashboard
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회/CIO 거버넌스 의사결정 | COBIT 2019의 5개 목표(EDM01~05). 목표-측정-보고-조치 4단계를 정의. EDM02(Benefits Delivery)가 본 토픽의 중심 |
| **BSC for IT (Balanced Scorecard)** | 4관점 전략 KPI 정의 | (1) Financial: ROI, TCO, Cost-per-Transaction (2) Customer: CSAT, NPS, First Contact Resolution (3) Internal Process: Incident MTTR, Change Success Rate, Project On-Time (4) Learning/Growth: Skill Index, Innovation Rate |
| **KPI Cascade (KPI 위계)** | Tier별 KPI 분해 | 전략 KPI(CIO Tier 1) -> Portfolio KPI(CIO Tier 2) -> Service/Project KPI(Service Owner Tier 3) -> Operational Metric(엔지니어 Tier 4). **"1-3-9-27 Rule"** 적용: CIO 1개, 부서장 3개, 실무자 9개, 운영 27개 |
| **Benefits Realization Plan** | 투자-성과 연결 | (1) Benefit Identification -> (2) Benefit Planning -> (3) Execution -> (4) Transition to Operations -> (5) Benefit Realization Review. **CRR(Current Reality Review)** 와 **IRR(Investment Reality Review)** 차이로 손실 측정 |
| **TCO (Total Cost of Ownership)** | 5년 총 소유 비용 | CapEx(HW, SW 라이선스, 구축) + OpEx(인건비, 유지보수, 전산실, 교육, 폐기) + Hidden Cost(다운타임, 통합, 보안사고). Gartner TCO 모델은 **초기비용 100% 대비 운영비 300~500%** 누적 |
| **Portfolio Management** | IT 투자 포트폴리오 최적화 | (1) 분류: Run(운영, 60~70%) / Grow(혁신, 20~30%) / Transform(전환, 10~15%) (2) 우선순위: Strategic Fit, Risk, ROI, Time-to-Value. **Bubble Chart (Value-Effort-Risk)** 활용 |
| **Maturity Assessment** | 성숙도 측정 | CMMI(1~5단계), COBIT(0~5단계), ITIL Maturity Model, OP-3 (Organization Process). 한국형 **e-CMM(전자정부 SW 성숙도)** 모델 |
| **Reporting & Analytics** | 의사결정 지원 | Board-level: 1-page Scorecard, Drill-down BI, Real-time Dashboard, Narrative Reporting(사례+데이터) |

### 핵심 산식 및 정량 모델

**(1) IT ROI 산식**
```
ROI (%) = (Total Benefit - Total Cost) / Total Cost × 100

단, Benefits는 다음으로 분해:
  +- Tangible (정량): Cost Saving, Revenue Increase, Working Capital Improvement
  +- Intangible (정성): Brand, Compliance, Agility, Employee Satisfaction

* Shadow Value 환산: 정성 효과를 Surrogate Monetary Value로 환산
  예: NPS +1 -> Retention 3%^ -> LTV(Lifetime Value) $200^ -> Annualized $400K
```

**(2) NPV (순현재가치)**
```
NPV = Σ [ (Benefit_t - Cost_t) / (1 + r)^t ]   for t = 0 to N
       where r = WACC(가중평균자본비용, 7~12%), N = 3~7년

* NPV > 0 이면 투자 승인, NPV < 0 이면 기각
* 한국 정보화 사업: 정보화사업법 시행령에 따라 "B/C Ratio(Benefit/Cost) ≥ 1.0" 요건
```

**(3) Risk-Adjusted ROI**
```
Risk-Adjusted ROI = ROI × (1 - Probability of Failure) - Expected Loss
                   = ROI × Confidence Factor
   where Confidence Factor = 0.7 ~ 0.95 (Stage-Gate 별 검증)
```

**(4) IT Productivity (MeriTalk 202
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 464 / 800

<- **이전**: [463. IT 경영 관리 핵심 토픽 463번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/463_it_management_core_topic_463_exam_summary/)
**다음**: [465. IT 경영 관리 핵심 토픽 465번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/465_it_management_core_topic_465_exam_summary/) ->

---
