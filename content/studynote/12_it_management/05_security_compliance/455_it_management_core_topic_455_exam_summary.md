---
title: "455. IT 경영 관리 핵심 토픽 455번 시험 요약 (IT Management Core Topic 455 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 455번은 **IT 거버넌스(COBIT 2019) ↔ IT 전략(BSC/EA) ↔ IT 운영(ITIL 4/ISO 20000) ↔ 프로젝트(PMBOK 7) ↔ 보안(ISO 27001)** 5대 축을 하나의 통합 프레임워크로 정렬하고, 디지털 전환(DX) 환경에서 **Value Governance(가치 거버넌스)** 로 전환하는 능력을 평가하는 종합 사지선다/서술형 문항이다.
> 2. **가치**: COBIT 2019의 **Governance & Management Objectives(40개)**, ITIL 4의 **Service Value System(SVS)**, PMBOK 7의 **8 Performance Domains**를 정합하면, IT 투자 ROI를 평균 **15~25% 개선**하고, 감사 적발 사항을 **40~60% 감소**시키며, EA 기반 중복 투자를 **20~30% 절감** 가능하다.
> 3. **판단 포인트**: ① **Top-Down(GOVERNANCE)** vs **Bottom-Up(MANAGEMENT)** 균형, ② **Center-Led EA(중앙집중)** vs **Federated EA(연방형)** 트레이드오프, ③ **Agile(적응형)** vs **Predictive(예측형)** 프로젝트 라이프사이클, ④ **Zero Trust(영점 신뢰)** vs **Perimeter Security(경계 보안)** 보안 모델, ⑤ **Build(자체 구축)** vs **Buy(패키지)** vs **Borrow(클라우드)** 의사결정 — 이 5가지 축에서 조직의 maturity level(1~5)과 risk appetite에 따라 최적의 하이브리드 모델을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

**IT 경영관리 455번**은 한국정보통신기술사(정보관리·컴퓨터시스템응용) 시험에서 빈번히 출제되는 **IT 거버넌스-전략-운영-프로젝트-보안 통합 관리** 영역의 종합 문항이다. 최근 5년간 출제 경향을 분석하면, 단순 암기형(COBIT 구성요소 나열)이 아니라 **사례 기반 시나리오**(예: "금융사가 DX 추진 중 IT 투자 우선순위 분쟁 발생, 거버넌스 체계 재설계")가 **80% 이상**을 차지한다.

핵심 출제 키워드는 ① **IT-사업 정합(Strategic Alignment)** ② **가치 실현(Value Realization)** ③ **위험 최적화(Risk Optimization)** ④ **자원 관리(Resource Management)** ⑤ **성과 측정(Performance Measurement)** — COBIT 2019의 **5원칙(Principles)** 과 정확히 매핑된다.

기존 패러다임은 **"IT는 비용(cost center)"** 이라는 인식 하에 COBIT 5(2012), ITIL v3(2011), PMBOK 5(2013) 기반의 **프로세스 중심(process-oriented)** 관리였으나, 현재는 **"IT는 가치 창출 동인(value driver)"** 으로 전환되어 **Agile·DevOps·클라우드·AI/ML** 기반의 **능동적·지능형·자동화** 경영관리 체계가 요구된다.

```text
  [455번 IT 경영관리 통합 프레임워크 — 5대 축 정합도 분석]

        +--------------------------------------------------+
        |         거버넌스 (GOVERNANCE — 결정)              |
        |   COBIT 2019 / ISO 38500 / King IV              |
        |   +--------------------------------------+       |
        |   |  Board ---> Steering Committee       |       |
        |   |    |              |                  |       |
        |   |    |   전략 (STRATEGY — 계획)        |       |
        |   |    v              v                  |       |
        |   |  IT Strategy / EA / Portfolio       |       |
        |   |  (BSC, TOGAF, Wardley Maps)         |       |
        |   |    |                                 |       |
        |   |    |   운영 (OPERATIONS — 실행)      |       |
        |   |    v                                 |       |
        |   |  ITIL 4 SVS / ISO 20000 / DevOps    |       |
        |   |  (34 Practices, CI/CD, SRE)         |       |
        |   |    |                                 |       |
        |   |    |   프로젝트 (PROJECT — 전달)     |       |
        |   |    v                                 |       |
        |   |  PMBOK 7 / PRINCE2 / SAFe           |       |
        |   |  (8 Domains, 12 Principles)         |       |
        |   |    |                                 |       |
        |   |    |   보안·리스크 (SECURITY — 보호) |       |
        |   |    v                                 |       |
        |   |  ISO 27001/27002 / NIST CSF / Zero  |       |
        |   |  (114 Controls, Identify~Recover)   |       |
        |   +--------------------------------------+       |
        +--------------------------------------------------+
                          |  통합 KPI: ROI, NPS, MTTR, CSAT
                          v
                +----------------------+
                |   비즈니스 가치 실현   |
                |   (Business Value)    |
                |  Revenue^ / Riskv /   |
                |  Costv / Agility^     |
                +----------------------+
```

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라 지휘자** 와 같다. 5대 악기(거버넌스·전략·운영·프로젝트·보안)가 각자 잘 연주해도, 지휘자(거버넌스)가 없으면 **불협화음** 이 발생하고, **단일 악기만** 연주하면 **편협한 음악** 이 나온다. 455번은 이 **"5악기 협연의 예술"** 을 묻는 문제다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 거버넌스 계층 — COBIT 2019 기반 의사결정 구조

COBIT 2019는 **Governance System(거버넌스 시스템)** + **Governance Framework(거버넌스 프레임워크)** 의 이중 구조로, 40개의 **Governance & Management Objectives(GMOs)** 를 5개 도메인(EDM: 5개 / Evaluate, Direct, Monitor / APO: 14개 / BAI: 11개 / DSS: 6개 / MEA: 4개)으로 분류한다. 핵심 메커니즘은 **Cascade(캐스케이드)** 로, **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> GMOs -> Components** 의 5단계 인과 사슬로 변환한다.

```text
  [COBIT 2019 Cascade Mechanism — 인과 사슬 5단계]

  Stakeholder Needs (내부: ROI, Risk, Agility / 외부: 규제, 고객)
      |   (Goal Cascade Step 1)
      v
  Enterprise Goals (13개 — 재무/고객/내부/학습 관점 BSC 정합)
      |   (Step 2: Mapping)
      v
  Alignment Goals (13개 — IT-사업 정합 목표)
      |   (Step 3: Mapping)
      v
  Governance & Management Objectives (40개 GMO)
      |   (Step 4: Process 구성요소로 분해)
      v
  Components (7종: Process / Organizational Structures /
              Information Flows / People, Skills & Competencies /
              Policies & Procedures / Culture, Ethics & Behavior /
              Services, Infrastructure & Applications)
      |   (Step 5: Activity/Task)
      v
  Practices (각 GMO당 6~20개 Practice) -> Activity -> Work Product
```

### 2. 전략 계층 — BSC, EA, Portfolio 삼각 정합

**Balanced Scorecard(BSC)** 는 4관점(Financial / Customer / Internal Process / Learning & Growth)으로 전략을 KPI화하고, **Enterprise Architecture(EA)** 는 TOGAF ADM(Architecture Development Method)의 8단계(Phase A~H: Preliminary -> Vision -> Business -> Information Systems -> Technology -> Opportunities -> Migration -> Implementation Governance)로 **As-Is -> To-Be -> Gap -> Transition** 을 도출한다. **Portfolio Management** 는 이 두 산출물을 **의사결정 트리(NPV, IRR, Payback, Strategic Fit Score)** 로 우선순위화한다.

### 3. 운영 계층 — ITIL 4 Service Value System (SVS)

ITIL 4(2019)의 SVS는 5대 구성요소로 **"Opportunity/Demand -> Value"** 변환 체계를 구현한다: ① **Opportunity/Demand**, ② **Value(다양한 이해관계자에게 다양한 가치)**, ③ **Guiding Principles(7원칙)**, ④ **Governance(거버넌스 조직)**, ⑤ **Service Value Chain(SVC: Plan->Improve->Engage->Design&Transition->Obtain/Build->Deliver&Support)**, 그리고 34개 **Practices**(General 14, Service 17, Technical 3). 핵심 변화는 **"4 Dimensions"(Organizations & People / Information & Technology / Partners & Suppliers / Value Streams & Processes)** 와 **SLA -> Service Level Quality** 로의 전환이다.

### 4. 프로젝트 계층 — PMBOK 7 Performance Domains

PMBOK 7(2021)은 **6판의 10 Knowledge Areas** 를 **8 Performance Domains**(Stakeholder / Team / Development Approach & Life Cycle / Planning / Project Work / Delivery / Measurement / Uncertainty)로 재편하고, **12 Principles of Project Management**(Stewardship / Team / Development Approach & Life Cycle / Planning / Project Work / Delivery / Measurement / Uncertainty / Tailoring 등)를 도입했다. 455번에서는 특히 **Predictive(Waterfall) vs Adaptive(Agile/Scrum) vs Hybrid** 의 **Life Cycle Selection** 의사결정 기준이 자주 출제된다.

### 5. 보안 계층 — ISO 27001:2022 + Zero Trust

ISO 27001:2022는 Annex A 통제를 **14개 영역 93개 통제**(2013년 114개에서 축소·재편)로 정리하고, **4단계 PDCA + Statement of Applicability(SoA)** + **Risk Treatment Plan(RTP)** 으로 ISMS를 인증한다. **Zero Trust Architecture(NIST SP 800-207)** 는 "Never Trust, Always Verify" 원칙으로 **5대 핵심 요소**(Policy Engine / Policy Administrator / Policy Enforcement Point / Subject / Asset)를 통해 **동적·최소권한·연속검증** 마이크로 세그먼테이션을 구현한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Governance (COBIT 2019)** | 의사결정 권한과 책임 구조 정의, Stakeholder Needs -> Enterprise Value 변환 | 5원칙(Needs 기반 / End-to-End / 단일 통합 프레임워크 / Holistic / Customizable), 40 GMO, 7 Components, 5 Cascade Steps |
| **Strategy (BSC + EA + Portfolio)** | IT 투자 우선순위 결정 및 As-Is -> To-Be 로드맵 | BSC 4관점 20~25개 KPI / TOGAF ADM 8단계 / Wardley Maps(Evolution: Genesis->Custom->Product->Commodity) / NPV·IRR 계산 |
| **Operations (ITIL 4 SVS)** | 서비스 가치 사슬(Value Chain) 운영, Service Desk->Change->Incident->Problem 4대 핵심 프로세스 자동화 | SVS 5구성요소, 34 Practices, 4 Dimensions, CI/CD 파이프라인(설계->전이->운영 통합), AIOps(관측·이상탐지) |
| **Project (PMBOK 7)** | 일회성 목적의 결과물 전달, 예측형·적응형·하이브리드 라이프사이클 선택 | 8 Performance Domains, 12 Principles, Earned Value(EV=PV×%완료)·Velocity·Burn-down 측정, OKR 연계 |
| **Security (ISO 27001 + Zero Trust)** | CIA(Confidentiality·Integrity·Availability) 및 인증·인가·계정 통제 | ISMS-P 인증 / 93 통제 항목 / Zero Trust 3대 핵심(Subject->Resource 인증, Least Privilege, Continuous Verification) |

### 핵심 산식·알고리즘

- **ROI 계산**: `ROI(%) = (Total Benefit − Total Cost) / Total Cost × 100`. **NPV**: `NPV = Σ CF_t / (1+r)^t − I₀`. **IRR**: NPV=0이 되는 할인율 r. **EV(공급가치)**: `EV = BAC × (% Complete)`. **SPI(Schedule Performance Index)**: `EV/PV`, **CPI(Cost Performance Index)**: `EV/AC`. CPI < 0.9 -> 즉시 Corrective Action 필수.
- **Information Security Risk = Threat × Vulnerability × Asset Value × Impact** / **ALE(Annual Loss Expectancy) = SLE × ARO**.
- **CMMI/Capability Maturity Model**: Level 1(Initial) -> 2(Managed) -> 3(Defined) -> 4(Quantitatively Managed) -> 5(Optimizing). **ISO 15504 SPICE** 와 연계, Process Capability 0~5 등급.
- **BSC 전략 맵의 인과관계도**: 학습·성장 -> 내부 프로세스 -> 고객 -> 재무의 4단계 인과 체인. **Lead Indicator**(선행)와 **Lag Indicator**(결과) 균형 50:50 권장.

- **📢 섹션 요약 비유**: 이 5대 축은 마치 **피라미드** 와 같다. **보안(ISO 27001)** 이 **기반(Foundation)**, **운영(ITIL 4)** 이 **중앙층(Core)**, **프로젝트(PMBOK)** 가 **전달층(Build)**, **전략(BSC/EA)** 이 **중간통제(Control)**, **거버넌스(COBIT 2019)** 가 **정상(Cap)** — 한 층이라도 무너지면 전체가 흔들린다.

---

## Ⅲ. 비교 및 연결

### 1. 거버넌스 프레임워크 비교

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | King IV (남아공) |
|:---|:---|:---|:---|:---|
| **목적** | IT 거버넌스·관리 목표 통합 프레임워크 | IT 서비스 관리(SM) 운영 Best Practice | IT 의사결정에 대한 이사회·경영진 지침 | 통합 거버넌스(통합 17개 원칙) |
| **계층** | Strategy ↔ Operations 연결 | Service Value System(SVS) | 원칙 기반(6원칙) | 5대 결과: Ethics, Performance, Compliance, Sustainability |
| **Scope** | 전사 IT(GOVERNANCE+MANAGEMENT) | 서비스 생애주기 | 거버넌스만(EDM) | 전사 거버넌스 |
| **핵심 메커니즘** | Cascade + 7 Components + 40 GMO + 5 Principles | SVS 5구성요소 +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 455 / 800

<- **이전**: [454. IT 경영 관리 핵심 토픽 454번 시험 요약](/studynote/12_it_management/05_security_compliance/454_it_management_core_topic_454_exam_summary/)
**다음**: [456. IT 경영 관리 핵심 토픽 456번 시험 요약](/studynote/12_it_management/05_security_compliance/456_it_management_core_topic_456_exam_summary/) ->

---
