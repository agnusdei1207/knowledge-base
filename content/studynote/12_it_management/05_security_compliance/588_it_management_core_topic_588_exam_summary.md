+++
title = "588. IT 경영 관리 핵심 토픽 588번 시험 요약 (IT Management Core Topic 588 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Management)는 **COBIT 2019 거버넌스 프레임워크**를 중핵으로 ISO/IEC 38500(거버넌스 원칙), ITIL 4(서비스 가치 사슬), TBM(Technology Business Management), FinOps, ISO 27001(정보보안), PMBOK 7(프로젝트), CMMI v2.0(프로세스 성숙도) 등 7대 표준/프레임워크를 **Plan->Build->Run->Monitor 가치 실현 루프(Value Realization Loop)**로 통합·운용하는 경영 체계이다.
> 2. **가치**: 정량적 효과로는 ① IT 투자 대비 ROI 평균 18~27% 개선(McKinsey 2023), ② Shadow IT 비율 35%->8% 감소(Gartner), ③ MTTR(평균 복구시간) 47% 단축, ④ TBM 기반 IT 원가 투명성 확보로 비핵심 IT 비용 22% 절감, ⑤ ISO 38500·COBIT 인증 기업에서 프로젝트 성공률 72%->89% 상승(PMI 2022) 효과를 거둘 수 있다.
> 3. **판단 포인트**: 핵심 Trade-off는 ① **중앙집권형 거버넌스 vs 분권형 페더레이션**(COBIT 집중도 5단계 중 어디에 위치시킬 것인가), ② **Build(신규개발) vs Run(운영) 예산 배분**(통상 30:70~40:60 권장), ③ **Waterfall vs Agile vs Hybrid**(프로젝트 성격별 SAFe/Scrum/XP 선택), ④ **내부 SI 내재화 vs 외부 Outsourcing vs Cloud MSP**, ⑤ **Compliance-First vs Innovation-First** — 이 5개 의사결정 축에서 조직의 디지털 성숙도(Digital Maturity Index)와 산업 규제 강도(금융/공공/의료 등)를 가중치로 반영해 최적안을 도출한다.

---

## Ⅰ. 개요 및 필요성

**IT 경영 관리(Information Technology Management, ITM)**는 단순한 시스템 운영을 넘어, 기업의 **전략적 목표와 IT 자산을 연결**하고, **거버넌스·포트폴리오·서비스·리스크·컴플라이언스**를 하나의 통합된 가치 흐름(Value Stream)으로 관리하는 경영학문 분야이다. 정보시스템 기술사 시험에서는 이 분야가 **거버넌스(70%), 서비스관리(15%), 프로젝트/포트폴리오(10%), 보안/리스크(5%)** 비중으로 출제되며, 특히 **COBIT 2019의 40개 거버넌스·관리 목표(Governance & Management Objectives)**와 **ISO/IEC 38500의 6대 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**은 거의 매년 단답형·서술형 양대 축으로 등장한다.

과거(2000년대 이전) IT 관리는 **"비용 센터(Cost Center)"** 관점이 지배적이었다. CFO는 IT를 통제 대상, 감시 대상으로 보았고, CIO는 "데이터센터 가동률, 헬프데스크 SLA" 같은 **기술 KPI**만 보고했다. 그러나 2010년대 클라우드·모바일·빅데이터가 폭발적으로 성장하면서 ① IT 비용이 매출 대비 7~12%로 급증, ② Shadow IT(비인가 클라우드 사용)가 연 IT 예산의 30~40%를 잠식, ③ 규제 요구(전자금융감독규정, GDPR, 개인정보보호법, ESG 공시)가 매년 강화, ④ AI/생성형 AI로 인한 신규 거버넌스 이슈(AI Bias, 데이터 주권) 등장 — 이 4대 압력으로 인해 **"가치 센터(Value Center) + 리스크 센터(Risk Center)"**로의 패러다임 전환이 불가피해졌다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리 패러다임 전환: 1990s -> 2030s                    |
+---------------------------------------------------------------------+
|                                                                     |
|  [1990s~2000s]         [2010s]              [2020s~2030s]            |
|   비용센터 시대       비즈니스 동반자시대    가치+리스크 통합 시대    |
|  +----------+        +----------+         +--------------+         |
|  |DataCenter|        |  CMO/CIO |         |   CDO/CISO   |         |
|  |  Uptime  |   ->    | Alignment|    ->    |  Value + ESG |         |
|  |  만족    |        |   B2B    |         | AI Governance|         |
|  +----------+        +----------+         +--------------+         |
|   COBIT 4.1             COBIT 5              COBIT 2019             |
|   ITIL v2/v3           ITIL 2011            ITIL 4 + FinOps        |
|   ISO 27001:2005       ISO 38500:2015       ISO 42001(AI)           |
|                                                                     |
|  관리관점: TCO 절감      관리관점: SLA     관리관점: NPV+옵션가치     |
|  KPI    : 가동률         KPI: 정합성       KPI: NRR/EBITDA 기여     |
+---------------------------------------------------------------------+
```

**왜 지금 IT 경영 관리가 필수인가?** ① **규제**: EU AI Act(2024), 한국 AI 기본법(2025 예정), DORA(금융권 디지털운영복원력), ESG 공시 의무화로 거버넌스 증빙자료가 법적 요구사항이 됨. ② **가시성**: 멀티클라우드(Multi-Cloud)·하이브리드 환경에서 IT 지출의 **할당·청구·최적화(Chargeback/Showback)**가 불가능하면 CFO·이사회 설득 불가. ③ **사이버韧性**: 랜섬웨어·공급망 공격(Supply Chain Attack) 증가로 **BIA(Business Impact Analysis)** 기반韧性 확보가 생존 이슈. ④ **인재**: IT-Business 융합 인재(BA, FinOps Engineer, AI Ethics Officer) 확보 경쟁.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"자동차의 계기판·엔진제어·내비게이션을 하나의 CAN 버스로 통합한 차량전자제어장치(ECU)"**와 같다. 과거에는 속도계(주황불 경고등)만 보는 '비용센터'였다면, 지금은 RPM·연료분사·자율주행센서·타이어공기압·ADAS 경보까지 통합 모니터링해 "운전자가 코너를 안전하게 돌도록 실시간 의사결정"을 지원하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**IT 경영 관리 5축 통합 아키텍처(5-Layer Integrated ITM Architecture)**는 ISO/IEC 38500을 최상위 거버넌스 원칙으로 두고, 그 아래에 **① 거버넌스(Governance) ② 전략·포트폴리오(Strategy & Portfolio) ③ 서비스·운영(Service & Operation) ④ 프로젝트·변화(Project & Change) ⑤ 리스크·컴플라이언스·보안(Risk, Compliance & Security, GRC)**의 5개 운영 레이어를 두는 구조이다. 각 레이어는 **Plan->Build->Run->Monitor(PBRM)** 사이클로 연결되며, **COBIT 2019의 EDM( Evaluate, Direct, Monitor) + APO(Align, Plan, Organize) + BAI(Build, Acquire, Implement) + DSS(Deliver, Service, Support) + MEA(Monitor, Evaluate, Assess)** 5개 도메인과 1:1 매핑된다.

```text
+---------------------------------------------------------------------+
|                  IT 경영 관리 5축 통합 아키텍처                       |
+---------------------------------------------------------------------+
|                                                                     |
|  +---------------------------------------------------------------+  |
|  | Layer 0: 거버넌스 원칙 (ISO/IEC 38500 - 6 Principles)        |  |
|  |   Responsibility · Strategy · Acquisition · Performance       |  |
|  |   Conformance · Human Behavior                                |  |
|  +---------------------------------------------------------------+  |
|                              ^                                      |
|  +---------------------------+-----------------------------------+  |
|  | Layer 1: Governance (COBIT 2019 EDM)                           |  |
|  |   - 이사회/IT전략위원회   - RACI 매트릭스   - 정책체계         |  |
|  +---------------------------+-----------------------------------+  |
|  +---------------------------+-----------------------------------+  |
|  | Layer 2: Strategy & Portfolio (APO)                            |  |
|  |   - TOGAF/EA   - PPM Tool(Planview, Clarity)                  |  |
|  |   - TBM(원가/가치 모델)   - FinOps(클라우드)                  |  |
|  +---------------------------+-----------------------------------+  |
|  +---------------------------+-----------------------------------+  |
|  | Layer 3: Service & Operation (DSS)                             |  |
|  |   - ITIL 4 SVC(33 Practices)  - AIOps/관측성                  |  |
|  |   - SRE(Error Budget)  - ITSM Tool(ServiceNow)                 |  |
|  +---------------------------+-----------------------------------+  |
|  +---------------------------+-----------------------------------+  |
|  | Layer 4: Project & Change (BAI)                                |  |
|  |   - PMBOK 7(8 domains)  - SAFe/Scrum  - DevOps                |  |
|  |   - CMMI v2.0  - Value Stream Mapping                         |  |
|  +---------------------------+-----------------------------------+  |
|  +---------------------------+-----------------------------------+  |
|  | Layer 5: GRC (MEA)                                            |  |
|  |   - ISO 27001/27005  - NIST CSF 2.0  - ISO 42001(AI)         |  |
|  |   - DORA·전자금융감독규정·개인정보보호법  - 내부회계관리(IACS) |  |
|  +---------------------------------------------------------------+  |
|                                                                     |
|   <------- Plan ------ Build ------ Run ------ Monitor ------->      |
|         (APO)        (BAI)        (DSS)         (MEA)               |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Layer 1: 거버넌스 위원회 (IT Steering Committee)** | 이사회 산하 의사결정 기구, CIO·CFO·CDO·CISO·사업부 COO 참여 | COBIT 2019 EDM 5개 목표(EDF: 거버넌스 체계 정립/이해관계자 욕구 파악/이행 통제), 분기 1회 정례 + 주요 투자건 발생 시 수시 개최. 의사결정 권한: 5,000만원 이상 IT 투자 승인, 보안사고 Severity-1 통보 |
| **Layer 2: 전략·포트폴리오 관리 (PPM + TBM + FinOps)** | IT 투자 포트폴리오 우선순위화, IT 원가/가치 가시화, 클라우드 비용 최적화 | **TBM(Tech Business Management)**: IDC/Gartner Taxonomy 기반 IT 비용을 "Run/Grow/Transform" 3색 분류. **FinOps Foundation 6단계 성숙도**: Inform->Optimize->Operate. AWS Cost Explorer·Azure Cost Management·CloudHealth 통합. **PPM**: Planview, ServiceNow SPM, Clarity PPM의 우선순위 점수화 모델(NPV/Strategic Fit/Risk) 활용 |
| **Layer 3: 서비스·운영 (ITIL 4 + SRE + AIOps)** | IT 서비스의 End-to-End 가치 흐름(Value Stream) 관리, 안정적 서비스 제공 | **ITIL 4 Service Value System(SVS)**: Opportunity/Demand->Value->Service Value Chain(Plan/Engage/Design/Obtain/Build/Deliver/Support). 34개 Best Practice. **SRE**: Google SRE Book의 SLI/SLO/Error Budget, Toil 50% 이하 원칙. **AIOps**: Datadog/New Relic/Dynatrace 기반 이상탐지·근본원인분석(RCA) 자동화 |
| **Layer 4: 프로젝트·변화 (PMBOK 7 + Agile + DevOps)** | 신규 IT 솔루션 도입, 비즈니스 변화 관리, 프로젝트 성공률 제고 | **PMBOK 7(2021)**: 8개 Performance Domain(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty). **Agile@Scale**: SAFe 6.0(4 Levels: Team->Program->Large Solution->Portfolio), LeSS, Nexus. **DevOps**: DORA 4 Metrics(Deployment Frequency, Lead Time, MTTR, Change Failure Rate) — Elite Performers: Deploy 1,460회/년, MTTR <1h |
| **Layer 5: GRC (Governance, Risk, Compliance)** | 리스크 식별·평가·대응, 규제 준수 증빙, 내부통제 | **ISO/IEC 27001:2022**: 93개 통제 항목(Annex A), ISMS 인증 사이클(3년). **NIST CSF 2.0(2024)**: Govern(신설)+Identify+Protect+Detect+Respond+Recover. **ISO/IEC 42001:2023(AI 거버넌스)**: AIMS(AI Management System) 인증. **DORA**: 금융 ICT 3rd Party Risk, ICT Incident Reporting, Digital Operational Resilience Testing |

**핵심 메커니즘 — "가치 실현(Value Realization) 루프"**: 단순한 예산 집행이 아니라, **① 전략적 목표 -> ② IT 투자 우선순위(PPM) -> ③ 서비스 설계/구축 -> ④ 운영 -> ⑤ 성과 측정(KPI) -> ⑥ 피드백/학습**으로 이어지는 6단계 폐루프이다. TBM에서는 이를 **"Investment Life Cycle(ILC)"**라
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 588 / 800

<- **이전**: [587. IT 경영 관리 핵심 토픽 587번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/587_it_management_core_topic_587_exam_summary/)
**다음**: [589. IT 경영 관리 핵심 토픽 589번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/589_it_management_core_topic_589_exam_summary/) ->

---
