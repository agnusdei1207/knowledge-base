+++
title = "597. IT 경영 관리 핵심 토픽 597번 시험 요약 (IT Management Core Topic 597 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스 목표) ↔ ITIL 4(서비스 가치사슬) ↔ PMBOK 7(성과 도메인)**의 3대 프레임워크를 **ISO/IEC 38500** 거버넌스 원칙(책임·전략·수행·적합성·규율·행위·투명) 위에서 통합 운영하여, **EA(TOGAF ADM)**를 통해 전략-포트폴리오-프로젝트-운영-감리 5계층의 엔드투엔드 정렬(Alignment)을 달성하는 경영 시스템이다.
> 2. **가치**: McKinsey 2023 보고에 따르면成熟的 IT 거버넌스 도입 기업은 **프로젝트 실패율 38%↓, TCO 25~40%↓, ROI 3.2배↑, Time-to-Market 45%↓** 효과를 얻으며, COBIT 2019 적용 시 **컴플라이언스 비용 평균 22% 절감** 및 **감리 적정 소요시간 50% 단축** 효과가 검증되었다.
> 3. **판단 포인트**: 핵심 의사결정축은 ①**거버넌스 모델 선택**(집중형 vs 연방형 vs 네트워크형) ②**프레임워크 통합 수준**(독립운영 vs 매핑 통합 vs 네이티브 융합) ③**자동화 범위**(수동감리 vs GRC 도구 vs AI 기반 지속감리) ④**측정 체계**(BSC-IT 4관점 vs OKR vs KPI)이며, 조직의 **디지털 성숙도(DTM 5단계)**에 따라 단계적 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation) 가속화로 기업 IT는 단순 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Value Driver)**로 역할이 전환되었으며, 이에 따라 IT 투자의 정당성, 거버넌스의 투명성, 운영의 효율성을 통합 관리하는 **IT 경영관리 체계(ITES: IT Enterprise Management System)**가 필수 역량으로 부상하였다. 2024년 기준 국내 CIO 설문조사에서 **73.2%**가 "IT 거버넌스 부재가 디지털 전환의 최대 장애물"이라고 응답한 만큼, IT 전략-거버넌스-운영-감리를 아우르는 통합 프레임워크 설계는 기술사의 핵심 출제 영역이다.

기존의 **사일로(Silo)형 IT 관리**(SI는 SI회사, 운영은 정보화사업팀, 감리는 외부감리기관)는 ①책임 소재 불명확 ②투자 효과 미측정 ③리스크 사후 인지 ④이해관계자 갈등 구조라는 4대 한계를 가지며, 이를 극복하기 위해 **End-to-End 가치사슬 기반의 통합 거버넌스**가 요구된다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│          IT 경영관리 5계층 통합 프레임워크 (ITMS 5-Layer Model)       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Layer 5  ┌─────────────────────────────────────────────────────┐  │
│  (감리)   │  IS Audit │정보시스템 감리│ISACA CISA│ISO 27001 인증 │  │
│           │  ┌──────────────┐    ┌──────────────┐              │  │
│           │  │ 3E Audit     │    │ Compliance   │              │  │
│           │  │ Economic·    │    │ Compliance·  │              │  │
│           │  │ Efficiency·  │    │ Adequacy·    │              │  │
│           │  │ Effectiveness│    │ Reliability  │              │  │
│           │  └──────────────┘    └──────────────┘              │  │
│           └────────────────────────┬────────────────────────────┘  │
│                                    ▼ (지속감리)                       │
│  Layer 4  ┌─────────────────────────────────────────────────────┐  │
│  (운영)   │  ITSM │ITIL 4 SVS│서비스 데스크│인시던트│문제│변경│  │
│           │  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐        │  │
│           │  │Plan  ││Design││Transit││Oper. ││Improve│        │  │
│           │  └──────┘└──────┘└──────┘└──────┘└──────┘        │  │
│           │  SLA 99.9% │ MTTR │ MTBF │ CSAT │ NPS              │  │
│           └────────────────────────┬────────────────────────────┘  │
│                                    ▼                                │
│  Layer 3  ┌─────────────────────────────────────────────────────┐  │
│  (프로젝트)│  PPM │PMBOK 7│PRINCE2│Agile(SAFe)│PgM│PfM│        │  │
│           │  ┌──────────────────────────────────────────────┐  │  │
│           │  │ Initiation→Planning→Execution→M&C→Closing   │  │  │
│           │  │ + 8 Performance Domains (Stakeholder, Plan, │  │  │
│           │  │   Uncertainty, Delivery, Measurement, Team) │  │  │
│           │  └──────────────────────────────────────────────┘  │  │
│           │  EVM │SPI │CPI │ROI │PV │EV │AC │BAC │EAC         │  │
│           └────────────────────────┬────────────────────────────┘  │
│                                    ▼                                │
│  Layer 2  ┌─────────────────────────────────────────────────────┐  │
│  (포트폴리오)│ PfM │전략→포트폴리오→프로젝트→운영 (Value Flow) │  │
│           │  ┌─────────┐  ┌──────────┐  ┌──────────┐         │  │
│           │  │전략맵    │  │BSC-IT    │  │Prioritize│         │  │
│           │  │Strategy │→ │4관점      │→ │Scoring   │         │  │
│           │  │Map      │  │재무·고객 │  │Model     │         │  │
│           │  └─────────┘  └──────────┘  └──────────┘         │  │
│           │  NPV │IRR │BCR │PI │Payback Period │ROIC         │  │
│           └────────────────────────┬────────────────────────────┘  │
│                                    ▼                                │
│  Layer 1  ┌─────────────────────────────────────────────────────┐  │
│  (거버넌스)│ COBIT 2019 │ 5 Governance Principles                │  │
│           │  ①Needs of Stakeholders  ②End-to-End Coverage      │  │
│           │  ③Apply Single Integrated Framework              │  │
│           │  ④Enabling Holistic Approach                      │  │
│           │  ⑤Separating Governance from Management           │  │
│           │  + 40 Management Objectives (5 Domains)            │  │
│           │  EDM(05)│APO(14)│BAI(11)│DSS(06)│MEA(04)          │  │
│           └────────────────────────┬────────────────────────────┘  │
│                                    ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Foundation: ISO/IEC 38500 IT Governance │ 38500:2015       │  │
│  │  ISO 27001 │ISO 20000 │ISO 21500 │ISO 33000 (SPICE)        │  │
│  │  EA: TOGAF ADM(8단계) │ Zachman 6×6 │ DoDAF │ FEAF          │  │
│  └─────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

기존 **수직적·기능별** 관리에서 **수평적·가치사슬 기반** 관리로 패러다임이 전환되었으며, 특히 **클라우드·AI·데이터** 등 신규 기술의 도입으로 IT 운영의 복잡성이 기하급수적으로 증가하면서, **통합 거버넌스 + 자동화 + 지속적 측정**이 불가능한 조직은 디지털 경쟁에서 도태된다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라의 지휘자**와 같다. 첼리스트(프로젝트), 바이올리니스트(서비스 운영), 타악기(인프라), 목관(데이터)가 각자 잘 연주해도 **지휘자(거버넌스)** 없이는 **하나의 교향곡(가치사슬)**이 되지 못하며, **악보(프레임워크)**와 **컨덕터(COBIT)**, **악기 조율(ITIL)**, **공연 평가(감리)**가 함께 어우러져야 비로소 완벽한 공연이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 시스템은 **전략(Strategy) → 거버넌스(Governance) → 포트폴리오(Portfolio) → 프로젝트(Project) → 운영(Operation) → 감리(Audit)**의 6단계 가치 흐름(Value Flow)으로 구성되며, 각 단계는 특정 프레임워크와 메트릭으로 제어된다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         IT 경영관리 6-Phase Value Flow (전략-감리 End-to-End)         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 1: STRATEGY (전략 수립)                                │   │
│  │  Input:  사업전략, 시장분석, 규제요구                        │   │
│  │  Process: SWOT→TOWS→전략맵(Strategy Map)→BSC-IT 4관점      │   │
│  │  Output: IT 전략계획서, 디지털 로드맵                       │   │
│  │  Tool:  IBM Blueworks, Mega Hopex, Bizzdesign               │   │
│  │  KPI:   Strategic Alignment Index(SAI), Digital Maturity   │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 2: GOVERNANCE (거버넌스 설계)                          │   │
│  │  Framework: COBIT 2019 + ISO 38500                           │   │
│  │  Components:                                                 │   │
│  │   • 5 Governance Principles (원칙)                          │   │
│  │   • 40 Governance/Management Objectives (목표)              │   │
│  │   • 5 Domains: EDM, APO, BAI, DSS, MEA                      │   │
│  │   • 7 Components: Process, Organizational Structures,       │   │
│  │     Information Flows, People/Skills, Services/Infrastructure│   │
│  │     Policies/Procedures, Culture/Ethics                     │   │
│  │  Output:  RACI Matrix, Decision Rights, Governance Charter  │   │
│  │  Role:    Board→Steering Committee→IT Council→PMO→Service   │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 3: PORTFOLIO (포트폴리오 관리)                        │   │
│  │  Frameworks: PfM(PfM3), MoP, SAFe Portfolio                 │   │
│  │  Categorization: Run(60%) / Grow(20%) / Transform(20%)      │   │
│  │  Selection Methods:                                         │   │
│  │   ① Financial: NPV, IRR, Payback, BCR, PI, ROIC            │   │
│  │   ② Scoring Model: Strategic·Risk·Financial·Operational    │   │
│  │   ③ Optimization: Integer Linear Programming, Portfolio Mgr │   │
│  │  Balancing: Pie Chart (Risk/Reward/Quick-win/Strategic)     │   │
│  │  Tool:  MS Project Online, Planview, Clarity PPM, ServiceNow│   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 4: PROGRAM/PROJECT (프로그램/프로젝트 실행)           │   │
│  │  Frameworks: PMBOK 7th (Predictive/Agile/Hybrid)            │   │
│  │   • 5 Process Groups: Initiating, Planning, Executing, M&C, │   │
│  │                       Closing                               │   │
│  │   • 8 Performance Domains:                                  │   │
│  │     1. Stakeholders  2. Team      3. Development Approach   │   │
│  │     4. Planning      5. Project Work 6. Delivery            │   │
│  │     7. Measurement   8. Uncertainty                         │   │
│  │   • 12 Principles: Stewardship, Team, Plans, Uncertainty,   │   │
│  │     Risk, Stakeholders, Value, Quality, Complexity, etc.    │   │
│  │  Metrics: EVM (PV·EV·AC·BAC·EAC·ETC·VAC)                   │   │
│  │           SPI=EV/PV │CPI=EV/AC │TCPI                       │   │
│  │  Methodologies: PRINCE2, Scrum, SAFe, LeSS, DSDM, XP        │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 5: OPERATION (서비스 운영)                            │   │
│  │  Framework: ITIL 4 Service Value System (SVS)               │   │
│  │   • 7 Guiding Principles: Focus on Value, Start Where You   │   │
│  │     Are, Progress Iteratively, Collaborate, Think Holistically│  │
│  │   • 34 Practices (formerly Processes):                      │   │
│  │     General(14): Service Strategy, Architecture, Continuity,│   │
│  │       Availability, Capacity, InfoSec, Risk, etc.          │   │
│  │     Service(17): Incident, Problem, Change Enablement,      │   │
│  │       Service Request, Service Desk, SLA, etc.              │   │
│  │     Technical(3): Deployment, Infrastructure, Software Dev   │   │
│  │  KPIs: SLA(99.9%), MTTR, MTBF, FCR, CSAT, NPS, MTRS        │   │
│  │  Tool:  ServiceNow, BMC Remedy, Ivanti, Jira Service Mgmt  │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Phase 6: AUDIT & ASSURANCE (감리 및 검증)                  │   │
│  │  Frameworks:                                                │   │
│  │   • IS Audit: CISA, COBIT 2019 Audit, ISO 27001 ISMS       │   │
│  │   • 3E Audit: Economic·Efficiency·Effectiveness             │   │
│  │   • 3CA: Compliance·Confidentiality·Availability·Accuracy  │   │
│  │   • Big 4: SOX 404 ITGC, ISAE 3402 SOC 1/2/3              │   │
│  │  Process: Risk Assessment→Audit Plan→Fieldwork→Reporting  │   │
│  │  Output: 적정/개선 권고사항, IS 감리보고서                   │   │
│  │  Tool:  ACL, IDEA, OpenPages, SAP GRC, ServiceNow GRC      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ◀─── Feedback Loop (MEA: Monitor, Evaluate, Assess) ───▶           │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | 거버넌스 프레임워크 | 5원칙 + 40관리목표 + 5도메인(EDM/APO/BAI/DSS/MEA) + 7컴포넌트 + 설계요소 11개(전략·목표·리스크 등) +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 597 / 800

← **이전**: [596. IT 경영 관리 핵심 토픽 596번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/596_it_management_core_topic_596_exam_summary/)
**다음**: [598. IT 경영 관리 핵심 토픽 598번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/598_it_management_core_topic_598_exam_summary/) →

---
