---
title: "526. IT 경영 관리 핵심 토픽 526번 시험 요약 (IT Management Core Topic 526 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT경영관리는 COBIT 2019/ISO 38500 거버넌스, ITIL 4 서비스관리, ISO 20000/27001 인증체계, EA(TOGAF/Zachman), BSC-KPI 연계, SW사업법·발주자 관점의 PMBOK/Agile-Hybrid를 통합하여 **Strategy->Portfolio->Project->Operation->Value** 5단계 가치사슬을 End-to-End로 통제하는 경영체계이다.
> 2. **가치**: McKinsey(2023) 기준 효과적 IT거버넌스 도입 기업은 디지털 ROI 2.3배, TCO 30~40% 절감, Time-to-Market 50% 단축, 프로젝트 성공률 28%->72%(Standish Group 2023 CHAOS Report) 향상되며, ISO 27001 인증 시 보안사고 67% 감소(ENISA 2022) 효과가 검증되어 있다.
> 3. **판단 포인트**: 중앙집중(COE) vs 분권형(BU별) 거버넌스, Waterfall vs Agile-Hybrid(SAFe/Spotify) 방법론, Build vs Buy vs Cloud(SaaS) vs Composable Architecture, CapEx vs OpEx 재무구조, Zero Trust vs Defense-in-Depth 보안모델, 내부통제(ISO 37301) vs 외부규제(전자금융감독규정) 준수전략의 Trade-off가 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)·AI·클라우드·데이터3법(개인정보보호법, 정보통신망법, 신용정보법) 규제 강화로 인해 IT는 단순 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Strategic Value Center)**로 격상되었으며, 전사적자원관리(ERP)에서 데이터 중심 의사결정으로의 패러다임 전환이 가속화되고 있다. 한국 정보화진흥법(국가정보화법), 클라우드컴퓨팅법(2024.1.시행), SW사업 대가지급기준, 공공데이터법, AI기본법(2026.1.시행예정) 등 규제 환경이 급변함에 따라, IT투자의 **정당성·합리성·효율성·형평성**을 객관적으로 입증할 수 있는 거버넌스 체계의 필요성이 절대적이다.

특히 **정보관리기술사** 시험은 단순 암기가 아닌 "현실 제약조건(예산·일정·규제·조직저항) 하에서 최적 아키텍처·방법론·거버넌스를 설계하고 그 트레이드오프를 논리적으로 정당화하는 능력"을 평가한다. 따라서 PMBOK 7th, ITIL 4, COBIT 2019, TOGAF 10, ISO 38500/20000/27001/37301, BABOK, DMBOK 2.0, Zachman 같은 글로벌 표준들을 단순 나열하는 것이 아니라, **"어떤 상황에서 어떤 프레임워크를 왜 선택하는가"**의 의사결정론적 관점으로 통합 이해해야 한다.

```text
+------------------------------------------------------------------------+
|           IT경영관리 5단계 가치사슬 (Value Chain) & 거버넌스 루프       |
+------------------------------------------------------------------------+
|                                                                        |
|  [전략기획]      [포트폴리오]      [프로젝트]        [운영/서비스]      |
|   Strategy ---► Portfolio ---► Program/Project --► Service Operation   |
|       |            |                |                  |               |
|       |            |                |                  |               |
|  BSC·SWOT    Stage-Gate        PMBOK 7th          ITIL 4 / ISO 20000  |
|  McKinsey    BCG 2x2          SAFe 6.0 / Scrum    SRE / AIOps        |
|  3C/5-Forces  Bubble Chart    Hybrid-Agile        FinOps              |
|       |            |                |                  |               |
|       v            v                v                  v               |
|  +--------------------------------------------------------------+    |
|  |  [가치측정·피드백] Value Realization & Continuous Improvement |    |
|  |  COBIT 2019 | BSC-KPI | Earned Value | NPS | CSAT | TCO/ROI |    |
|  +--------------------------------------------------------------+    |
|                              ^                                        |
|                              |                                        |
|                    [거버넌스/컴플라이언스/리스크]                       |
|                    ISO 38500, COBIT 2019, ISO 37301                    |
|                    ISO 27001/27701, NIST CSF 2.0, Zero Trust          |
|                    SW사업법, 개인정보보호법, ISMS-P                    |
+------------------------------------------------------------------------+
```

기존 1990~2000년대 IT경영은 **"시스템 개발 후 사후 운영"**의 Waterfall·사일로(Silo)·부서별 독자 시스템(Shadow IT) 중심이었으나, 2010년대 이후 Platform·API Economy·2020년대 **Cloud-Native·AI-Native·Composable Enterprise**로 진화하며, IT와 Business의 경계가 사라진 **Bimodal IT(Gartner)**->**Fusion Team**->**Product-centric Organization** 패러다임으로 전환되었다. 이에 따라 ITIL v3의 26개 프로세스 -> ITIL 4의 **34 Practices (Service Value System)**로, COBIT 5(5원칙 7촉진자 37목표) -> COBIT 2019(40 Governance/Management Objectives, Focus Areas, Design Factors)로 진화하며, **"표준의 통합적 적용"**이 핵심 역량으로 부상했다.

- **📢 섹션 요약 비유**: IT경영관리는 마치 **"도시의 종합 도시계획 + 교통관제센터 + 재정감사원"**을 동시에 운영해야 하는 도시행정가 역할과 같다. 건물(시스템) 하나만 짓는 건축가가 아니라, 교통흐름(데이터), 예산(투자), 법규(컴플라이언스), 주민만족도(사용자경험)을 모두 관장하는 **"스마트시티 총괄 디렉터"**가 바로 IT경영관리 기술사의 역할이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT경영관리의 4대 핵심 축은 **① 거버넌스(Governance) ② 서비스관리(Service) ③ 프로젝트관리(Project) ④ 컴플라이언스·보안(Compliance)**이며, 이를 **EA(Enterprise Architecture)**가 통합 Backbone 역할을 수행한다. 각 축의 핵심 원리는 다음과 같다.

```text
+---------------------------------------------------------------------+
|        COBIT 2019 Governance System + ITIL 4 SVS 통합 참조모델      |
+---------------------------------------------------------------------+
|                                                                     |
|   +----------------------------------------------------------+    |
|   |  EDM (Evaluate, Direct, Monitor) -- 거버넌스 의사결정층   |    |
|   |  +- Benefits Realization    +- Risk Optimization          |    |
|   |  +- Resource Optimization   +- Stakeholder Transparency   |    |
|   +----------------------------------------------------------+    |
|                              |  Cascade                            |
|   +----------------------------------------------------------+    |
|   |  PBR / APO / BAI / DSS / MEA (5 Domain, 40 Objectives)    |    |
|   |  Plan->Build->Run->Monitor  Value Creation Lifecycle         |    |
|   +----------------------------------------------------------+    |
|                              |  Integrate                           |
|   +----------------------------------------------------------+    |
|   |  ITIL 4 SVS: Opportunity/Demand->Value (34 Practices)     |    |
|   |  +- General (4) +- Service (17) +- Technical (13)        |    |
|   |  +- Guiding Principles (7) +- 4D Model (Discover/Engage)  |    |
|   +----------------------------------------------------------+    |
|                              |  Control                             |
|   +----------------------------------------------------------+    |
|   |  ISO 38500 Principles: 책임·전략·수행·적합성·규율·인간·리스크 |    |
|   |  ISO 37301(Comp) | ISO 27001(Sec) | ISO 20000(Svc)         |    |
|   +----------------------------------------------------------+    |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019 거버넌스 체계** | IT목표와 비즈니스목표 정렬, 의사결정 권한·책임 구조 정의 | **Design Factors 11개**(전략, 목표, 리스크, 이슈, 위협, 준수요건, 역할, IT 이슈, 기술采纳, 위협취약성, 구현 방법론)로 **Governance System**을 ①Context ②Direction ③Control ④Operate ⑤Monitor ⑥Evaluate의 **6단계 사이클**로 운영, **40개 Governance/Management Objectives** 중 APM(Align, Plan, Organize), BAI(Build, Acquire, Implement), DSS(Deliver, Service, Support), MEA(Monitor, Evaluate, Assess) 4도메인·EDM 5단계로 **RACI Matrix** 기반 책임 할당 |
| **ITIL 4 Service Value System (SVS)** | IT서비스의 End-to-End 가치 창출 및 지속적 개선 | **Opportunity/Demand -> Value** 흐름의 핵심인 **34 Practices**(예: Incident Mgmt, Change Enablement, Service Desk, Problem Mgmt, SLM, SRE, AIOps, Service Catalog, CMDB, Knowledge Mgmt), **7 Guiding Principles**(Focus on Value, Start Where You Are, Progress Iteratively, Collaborate, Think Systematically, Keep It Simple, Optimize), **4D Model**(Discover-Agree-Design-Transition), **Continual Improvement Model**(Vision->Where->How->Does it Work?), **Service Desk 4-Tier**(L0:Self-Service->L1:Service Desk->L2:Technical->L3:Expert) |
| **ISO 38500 IT 거버넌스** | 이사회·경영진의 IT 의사결정 원칙 및 평가 프레임 | **6원칙**(책임 Responsibility, 전략 Strategy, 수행 Acquisition, 적합성 Conformance, 규율 Performance, 인간 Human Factor, 리스크 Risk) × **3영역**(Evaluate, Direct, Monitor) × **5모델**(Direct/Advisory/Consensus/Steering/Information), 6개월 주기 Self-Assessment + 외부 Audit |
| **TOGAF 10 / Zachman EA** | 전사 아키텍처의 통합 청사진, 비즈니스-데이터-애플리케이션-기술 정렬 | **ADM(Architecture Development Method) 8단계**(Preliminary->A:Vision->B:Business->C:Data/App/Technology->D:Opportunities->E:Migration->F:Governance->G:Implementation Management->H:Change Management), **Zachman 6×6 Matrix**(What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Functioning), **ArchiMate 3.2**(모티베이션-구조-행위 3계층+물리/의미계층), **Architecture Repository**(Architecture Meta-model, Continuum: Foundation->Common->Industry->Organization) |
| **PMBOK 7th / PRINCE2 / SAFe 6.0** | 프로젝트·프로그램·포트폴리오 통합 관리 | **PMBOK 7th**: 12 Principles + 5 Process Groups(Init/Plan/Exec/Monitor/Closing) + 10 Knowledge Areas + **Tailoring** 강조, **PRINCE2 7th**(2023): 7원칙·7실무·7프로세스, **SAFe 6.0**: 4 Configurations(Essential/Large Solution/Portfolio/Full) + 10 L要素(PI Planning, ART, Scrum Master, Product Owner, Release Train Engineer, System Architect, Business Owner), PI(8~12주), Agile Release Train(ART, 50~125명) |
| **BSC(Kaplan-Norton) + KPI Tree** | 전략-전술-운영지표 연계 성과관리 | **4 Perspective**(Financial/Customer/Internal Process/Learning & Growth), **Strategy Map**(학습->내부->고객->재무 Cause-Effect Chain), **KPI Tree**(목표->CSF->KPI->Target->Action Plan), **OKR**(Objectives & Key Results)과의 하이브리드, **Lagging vs Leading Indicator** 구분, **North Star Metric** + **NSM Tree**(Airbnb·Spotify 모델) |

**핵심 알고리즘/산식:**

1. **EVM(Earned Value Management) 핵심 지표**:
   - `PV(Planned Value)`: 계획 대비 예산 계획
   - `EV(Earned Value) = BAC × % Complete`: 실제 수행된 작업의 계획 가치
   - `AC(Actual Cost)`: 실제 투입 비용
   - `CV(Cost Variance) = EV − AC`, `SV(Schedule Variance) = EV − PV`
   - `CPI(Cost Performance Index) = EV/AC ≥ 1.0`, `SPI(Schedule Performance Index) = EV/PV ≥ 1.0`
   - `EAC(Estimate At Completion) = BAC / CPI`, `VAC(Variance At Completion) = BAC − EAC`
   - `TCPI(To Complete Performance Index) = (BAC−EV)/(BAC−AC)`

2. **COBIT 2019 Capability/Maturity 평가**:
   - **PAM(Performance Management)**: 능력수준 0(Incomplete)~5(Optimizing)
   - `능력수준 = Σ(Process Attribute Rating × Weight) / 100`
   - 0(불완전)~5(최적화) 6단계, **Process Attribute 9개**(PA1.1~5.2)

3. **ROI/NPV/IRR 산식**:
   - `ROI = (총 이익 − 총 비용) / 총 비용 × 100`
   - `NPV = Σ[CFt / (1+r)^t] − Initial Investment`
   - `IRR = Σ[CFt / (1+IRR)^t] = 0`을 만족하는 할인율
   - **TCO(Total Cost of Ownership)**: 도입비(HW+SW+구축) + 운영비(인건비+유지보수+전력+소모품) + 폐기비, 보통 5~7년 분석, **POC/ROI 1:3~5** 기준 확보

4. **IT 거버넌스 KPI** (BSC 기반):
   - 재무: IT Cost Ratio(IT 비용/매출), ROI, NPV
   - 고객: CSAT, NPS, SLA Compliance
   - 내부: 가용성(Availability=MTBF/(MTBF+MTTR) × 100), MTTR, 변경 성공률, Incident 해결율
   - 학습: 직원역량, 자격증 취득률, 교육이수시간, 지식공유 기여도

- **📢 섹션 요약 비유**: COBIT는 회사의 **"이사회 의사결정 규정집"**, ITIL은 **"서비스 운영 매뉴얼"**, PMBOK은 **"프로젝트 진행 메뉴얼"**, ISO 38500은 **"기업지배구조 준칙"**이다. 이 4권을 따로 보는 것이 아니라 **"같은 그림의 4개 챕터"**로 통합 이해해야 한다. 마치 자동차의 **"운전석(거버넌스), 엔진룸(서비스), 정비매뉴얼(프로젝트), 법규(컴플라이언스)"**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 526 / 800

<- **이전**: [525. IT 경영 관리 핵심 토픽 525번 시험 요약](/studynote/12_it_management/05_security_compliance/525_it_management_core_topic_525_exam_summary/)
**다음**: [527. IT 경영 관리 핵심 토픽 527번 시험 요약](/studynote/12_it_management/05_security_compliance/527_it_management_core_topic_527_exam_summary/) ->

---
