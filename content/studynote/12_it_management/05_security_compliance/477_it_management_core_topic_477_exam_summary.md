---
title: "477. IT 경영 관리 핵심 토픽 477번 시험 요약 (IT Management Core Topic 477 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019, ITIL 4, ISO/IEC 38500, EA(Enterprise Architecture) 4축(BA·DA·AA·TA) 프레임워크를 기반으로 **IT 전략-거버넌스-서비스-투자-아키텍처-아웃소싱** 6대 영역을 통합 운영하는 경영 체계이며, CSF/KPI/CSF-Cascade를 통해 Board-Level 의사결정과 IT Operation을 End-to-End로 연결하는 것이 핵심이다.
> 2. **가치**: McKinsey(2023) 기준 체계적 IT 거버넌스 도입 기업은 IT 투자 대비 ROI 평균 **23%** 향상, Incident MTTR **42%** 단축, Shadow IT 비용 **31%** 절감 효과가 있으며, ISO/IEC 38500 인증 보유 시 regulator penalty risk **68%** 감소, 디지털 트랜스포메이션 성공률 **2.4배** 향상이 Deloitte(2024) 보고를 통해 정량 입증되었다.
> 3. **판단 포인트**: 핵심 Trade-off는 (a) **Centralized vs Federated 거버넌스** (CoE 집중 vs BU 분산 - 통제력 vs 속도), (b) **Build vs Buy vs Rent** (내부 개발 vs 패키지 vs SaaS - TCO 3~5년 회수 vs Time-to-Market), (c) **Tailoring Level** (Full COBIT vs Light-weight ITIL vs Agile@Scale) 의사결정이며, 조직의 Digital Maturity Index(초기·확장·확립·최적화·혁신)에 따라 EDM(Evaluate-Direct-Monitor) 사이클의 강도를 차등 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 IT 경영 관리 영역은 **"IT가 경영의 Strategic Enabler로 기능하기 위한 End-to-End 거버넌스 체계를 설계하고 평가할 수 있는 역량"** 을 측정한다. 2000년대 이후 IT-Business Alignment(Stratford Sherman, 1993; Henderson & Venkatraman, 1999), Sarbanes-Oxley Act(2002), GDPR(2018), ESG Disclosure(2024~) 등 규제 환경이 강화됨에 따라, IT는 단순 Cost Center에서 **Value Center**(Gartner, 2018) 및 **Strategic Asset**(Weill & Ross, 2004) 으로 재정의되었다.

특히 4차 산업혁명(AI, IoT, Cloud, Blockchain, BigData, Metaverse) 환경에서 **Digital Business Transformation**(DX) 실패율이 약 60~70%(McKinsey, 2023)에 달하는 이유는, **IT 거버넌스 부재**, **ROI 측정 체계 결여**, **조직-프로세스-기술 정렬 실패** 가 근본 원인으로 지목된다. 따라서 기술사 응시자는 단순 암기가 아닌, **CobiT 2019 EDM/Domain 체계 ↔ ITIL 4 Service Value Chain ↔ TOGAF ADM ↔ PMBOK 7th Performance Domain** 간 **Cross-Mapping** 능력을 보유해야 한다.

```text
+-------------------------------------------------------------------------+
|              IT 경영 관리 6대 핵심 영역 (6 Domains Framework)            |
+-------------------------------------------------------------------------+
|                                                                         |
|  +----------+   +----------+   +----------+   +----------+              |
|  | ①전략/거버|--->|②서비스  |--->|③투자/ROI|--->|④EA/표준 |              |
|  |  넌스     |   |  관리    |   |  경제성  |   |  화      |              |
|  |COBIT 2019|   |ITIL 4    |   |TCO/ROI/ |   |TOGAF/   |              |
|  |ISO 38500 |   |ISO 20000|   |NPV/EVA  |   |FEAF/DODAF|              |
|  +----+-----+   +----+-----+   +----+-----+   +----+-----+              |
|       |              |              |              |                    |
|       +--------------+------+-------+--------------+                    |
|                             v                                          |
|                  +------------------+                                   |
|                  | ⑤프로세스혁신/   |   +----------+                     |
|                  |  아웃소싱/계약   |<---|⑥측정/BSC |                     |
|                  | BPR/SLA/KPI     |   |BSC/CSF  |                     |
|                  | SLA Penalty/    |   |KPI/PI   |                     |
|                  | Service Credit  |   |ITSC     |                     |
|                  +------------------+   +----------+                     |
|                                                                         |
|        [연결] SWOT -> IT전략 -> Portfolio -> Project -> Service -> Measure |
+-------------------------------------------------------------------------+
        ^
        | Board/CxO Level 의사결정 (EDM Cycle)
        | v
   +------------+
   | Audit/Eval | (IT Balanced Scorecard / COBIT Maturity Model)
   +------------+
```

기존(Pre-2000) IT 관리는 **"Siloed Application 개발"**, **"Reactive 장애 대응"**, **"CapEx 중심 HW 투자"** 위주였으나, 현재는 **"Platform Business 모델"**, **"AI-Driven AIOps"**, **"OpEx 기반 Pay-as-you-go"** 로 패러다임이 전환되었다. 이에 따라 ITIL v2(2001) -> ITIL v3(2007) -> ITIL 4(2019), COBIT 4.1 -> COBIT 5(2012) -> COBIT 2019, EA: TOGAF 8 -> TOGAF 9.2 -> TOGAF 10(2023) 등으로 각 프레임워크도 **Agile / Cloud-native / Sustainability** 요소를 흡수하며 진화해 왔다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **"건물의 내진설계"** 에 비유할 수 있다. 평소에는 그 필요성을 못 느끼지만, 지진(규제 강화·경쟁 심화·사이버 공격) 시 무너지는 건물(IT 시스템)은 재건 비용이 신축비의 **3.2배**(NIST, 2020)에 달한다. COBIT은 설계도, ITIL은 운영 매뉴얼, EA는 구조 계산서, BSC는 건전성 진단서, SLA는 입주 계약서이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"Plan -> Build -> Run -> Measure -> Improve"** 의闭环(Closed-Loop) 사이클이며, 이를 **COBIT 2019의 5 Domains / 40 Objectives** 와 **ITIL 4의 Service Value System(SVS)** 이 상호 보완한다.

```text
+-----------------------------------------------------------------------+
|           COBIT 2019 ↔ ITIL 4 ↔ TOGAF Cross-Mapping 구조             |
+-----------------------------------------------------------------------+
|                                                                       |
| [COBIT 2019 EDM Cycle]            [ITIL 4 SVS]                        |
|   E(evaluate) -+                  +- Plan/Improve -+                 |
|   D(direct)   -+  --Align--->      +- Engage       |                 |
|   M(monitor)  -+                  +- Design&Transit|                 |
|      |                              +- Obtain/Build |                 |
|      |                              +- Deliver/Supp |                 |
|      |                              +- Value Chain  |                 |
|      v                                            v                  |
| [Align, Plan & Organize - APO]     [Strategy Mgmt]                  |
| [Build, Acquire & Implement - BAI] [Design/Transition]               |
| [Deliver, Service & Support - DSS] [Operation/Support]               |
| [Monitor, Evaluate & Assess - MEA] [CSI - Continual Improvement]     |
|                                                                       |
| [TOGAF ADM]                                                           |
|   Preliminary -> A(Arch Vision) -> B/D(Bus/Dat Arch)                  |
|   -> C(App Arch) -> E(Opportunit&Sol) -> F(Migration Plan)             |
|   -> G(Governance) -> H(Architecture Change Mgmt) -> Rqmt Mgmt          |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (COBIT 2019)** | IT 의사결정 권한·책임·보고 체계 정의 | 5 Domains(EDM, APO, BAI, DSS, MEA) × 40 Objectives, 7 Component(Process/Structure/People/Skills/Information/Service/Infrastructure), Focus Area 46종, Design Factor 11개로 조직별 Tailoring 지원 |
| **서비스 관리 (ITIL 4)** | IT 서비스 End-to-End 운영 체계 | 34 Practices (General Mgmt×14, Service Mgmt×17, Technical Mgmt×3), 4 Dimensions(Org/People/Info/Technology/Partners/Value Streams), SVS(Value/Organization/People/Information/Technology/Partner/ValueStream), 7 Guiding Principles |
| **투자 경제성 평가** | IT 프로젝트/서비스의 재무적 정당성 | TCO(Total Cost of Ownership, 5~7년), ROI(Return on Investment), NPV(Net Present Value, 할인율 보통 WACC+α 8~12%), IRR(Internal Rate of Return), EVA(Economic Value Added), Payback Period, Benefit Realization(Month 6/12/18/24) |
| **엔터프라이즈 아키텍처 (EA)** | 조직-비즈니스-데이터-애플리케이션-기술 정렬 | TOGAF ADM(Architecture Development Method) 10단계, ArchiMate 3.2 notation(Strategy->Business->Application->Technology 4 Layer), Zachman 6×6 Matrix, FEAF(Federal EA), DoDAF(View-based) |
| **성과 측정 (BSC/KPI)** | IT 성과 정량 측정 및 전략 연계 | Kaplan-Norton Balanced Scorecard 4관점(Financial/Customer/Internal Process/Learning&Growth), IT BSC(Process Excellence/Operational Excellence/Future Orientation/Financial Performance), CSF(Critical Success Factor)->KPI->KPI Tree 3단 cascade |
| **아웃소싱/SLA 관리** | 외부 IT 서비스 조달·계약·성과관리 | 계약유형(FP/T&M/Unit Price/Output-based/Outcome-based/Gainsharing 6종), Service Credit Penalty(평균 5~15% 월정액 공제), KPI/SLA Tier(Tier-1 가용성 99.9%, Tier-2 99.99%), RTO/RPO 정의, Exit Plan(통상 6~12개월 transition) |
| **프로세스 혁신 (BPR/BPM)** | 업무 프로세스 재설계 및 자동화 | Hammer-Champy BPR 7원칙, Six Sigma(DMADV/DMAIC, 3.4 DPMO), Lean(8 Waste/Muda), BPMN 2.0, RPA(UiPath/Automation Anywhere), Low-Code(OutSystems/Mendix), Hyperautomation(Gartner 2023) |
| **SW 비용 산정** | SW 개발 규모/비용/일정 산정 | COCOMO II(2000), COCOMO 2010, Function Point(ISBSG 평균 생산성 8.5 FP/MM), Use-Case Point, COSMIC, SLIM, Putnam, Estimation by Analogy |

핵심 파라미터 및 산식 예시:

- **TCO 산식**: TCO = Direct Cost(HW+SW+인건비) + Indirect Cost(다운타임/교육/지원) + Hidden Cost(Integration/Governance/Switching) - 일반적으로 초기 도입비의 **3~5배**(Gartner, 2022)
- **NPV 산식**: NPV = Σ[t=1..n] (B_t - C_t) / (1+r)^t - I_0, 여기서 r=할인율, B=Benefits, C=Cost, I_0=Initial Investment
- **COBIT Maturity Level**: 0(Non-existent) -> 1(Initial) -> 2(Managed) -> 3(Defined) -> 4(Quantitative) -> 5(Optimizing) - **CMMI 5단계 모델**과 유사
- **SLA Penalty 공식**: Penalty(월) = (목표가용성 - 실제가용성) × 월정액 × Penalty Rate, 예: 99.9% 목표 시 실제가용성 99.7% -> 0.2% × 월정액 × 100% = 0.2% 차감 (Service Credit)
- **Function Point 공식**: FP = UFP × VAF, VAF = 0.65 + 0.01 × Σ(14개 General System Characteristics 점수, 0~5점)

- **📢 섹션 요약 비유**: 위 6대 영역은 **"자동차 운전 시스템"** 과 같다. EA(Enterprise Architecture)는 차체/엔진 설계도, COBIT은 운전자 면허/교통법규, ITIL은 정비 매뉴얼, BSC는 계기판, SLA는 보험/약정, BPR은 도로 시스템이다. **"COBIT이 운전 매너를 정의하고, ITIL이 엔진 관리, EA가 차체, BSC가 연비, SLA가 사고 보장"** 처럼 각 영역이 유기적으로 작동해야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** (Control 중심) | **ITIL 4** (Service 중심) | **ISO/IEC 38500** (Governance 원칙) |
| :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 & 관리 목표 달성 | IT 서비스 가치 창출 | IT 의사결정 책임·원칙 정의 |
| **구조** | 5 Domains × 40 Objectives | 34 Practices, 4 Dimensions | 6 Principles(Evaluate/Direct/Monitor × 3영역) |
| **수준** | Strategic + Tactical + Operational | Tactical + Operational | Strategic(Board) |
| **적용 범위** | 전사 IT(End-to-End) | IT 서비스(SVC 전반) | 이사회·경영진 의사결정 |
| **측정 도구** | Maturity Model(0~5), PAM/GSI(2019) | Maturity Model(0~5), 4D Diagnostic | MOF(ISO 38500 Maturity), 6 Principles Audit |
| **결합 시점** | IT 전략 정렬 단계 | 서비스 디자인·전환 단계 | 책임 분담·감독 단계 |
| **강점** | Risk/Compliance 강력, Audit 친화 | Agile/Practices, 실전 활용성 | 6 Principle(책임·전략·조달·성과·규정·인간) |
| **약점** | 운영 디테일 부족, 복잡 | 거버넌스 의사결정
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 477 / 800

<- **이전**: [476. IT 경영 관리 핵심 토픽 476번 시험 요약](/studynote/12_it_management/05_security_compliance/476_it_management_core_topic_476_exam_summary/)
**다음**: [478. IT 경영 관리 핵심 토픽 478번 시험 요약](/studynote/12_it_management/05_security_compliance/478_it_management_core_topic_478_exam_summary/) ->

---
