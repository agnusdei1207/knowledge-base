+++
title = "764. IT 경영 관리 핵심 토픽 764번 시험 요약 (IT Management Core Topic 764 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리의 핵심은 **COBIT 2019**의 40개 거버넌스/관리 목표를 **Cascade Goals** 메커니즘으로 기업 KPI(예: EBITDA, NPV)까지 연동하고, **ITIL 4**의 34개 실무 프로세스·**ISO 38500**의 6원칙(RACI 매트릭스 기반)으로 실행·감독 체계를 이원화하는 것이다.
> 2. **가치**: McKinsey(2023) 보고 기준, **Mature IT Governance 기업**은 TCO 23~31% 절감, Time-to-Market 41% 단축, Major Incident MTTR 67% 개선을 달성하며, **COBIT 2019 Design Factor 11개**를 통해 컨텍스트-특화 거버넌스 시스템 1회 구축 비용 기준 약 1.2억 원/엔터프라이즈의 ROI 3.4배를 실현한다.
> 3. **판단 포인트**: **Build vs. Buy(거버넌스 도구)**, **Centralized(CoE) vs. Federated(사업부별 CoE) 거버넌스 모델**, **Push(규제 준수) vs. Pull(가치 실현) 거버넌스 전략**, 그리고 **Capex/Opex 배분(70:30 vs 50:50)**의 4축 트레이드오프를 **RACI 매트릭스 × Risk Appetite × BSC 4관점**으로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입(1980년대~2000년대)을 넘어, 2020년대 이후의 기업 IT는 **"디지털 트랜스포메이션(DX)"**과 **"ESG·규제 준수"**라는 두 축 위에서 작동한다. Gartner(2024)에 따르면 글로벌 CEO의 89%가 "IT 거버넌스 미성숙이 사업 실패의 Top-3 리스크"라고 답변했으며, 한국은 2024년 전자증권, 가명정보, EU AI Act 등 **Cross-Border 규제**가 동시 적용되면서 IT 경영 체계의 통합적 재정립이 필수 과제가 되었다.

기존의 **"IT 부서 중심의 프로젝트 관리"** 패러다임은 다음과 같은 한계를 보인다:
- **사일로(Silo) 문제**: 사업부(BU)별 IT 투자 중복으로 동일 시스템 중복 도입률 35% 이상(한국정보화진흥원, 2023)
- **가치 비가시성**: IT 투자의 사업 기여도(ROI) 측정 부재로 CFO-주도 IT 예산 삭감 빈발
- **규제 대응 지연**: 개인정보보호법, ESG, AI Basic Act 등 7개 이상 규제 동시 대응 시 컨플라이언스 팀 과부하
- **인시큐어 디폴트**: Secure-by-Design 미적용으로 인한 랜섬웨어 피해액 평균 18억 원/사건(방통위, 2024)

이를 해결하기 위해 **"Enterprise Governance of IT (EGIT)"** 개념이 등장했고, **ISO/IEC 38500(거버넌스 원칙) + COBIT 2019(거버넌스/관리 목표) + ITIL 4(서비스 실행) + ISO 27001(정보보안) + ISO 20000(서비스 품질)**의 5대 프레임워크가 통합 적용되는 **"Integrated IT Management System"**이 글로벌 스탠다드로 자리 잡았다.

```text
+----------------------------------------------------------------------+
|              Enterprise IT Management 통합 프레임워크                |
+----------------------------------------------------------------------+
|                                                                      |
|  [Strategy Layer]  <------ Board / CEO / CIO                          |
|   +----------------------------------------------------------+       |
|   |  ISO/IEC 38500 (6 Principles)                             |       |
|   |  +-----+-----+-----+-----+-----+-----+                   |       |
|   |  |Resp.|Strat|Acq  |Perf.|Conf.|Human| <- Evaluate+Direct |       |
|   |  |     |     |     |     |     |Behav|   +Monitor        |       |
|   |  +-----+-----+-----+-----+-----+-----+                   |       |
|   +--------------------+-------------------------------------+       |
|                        v                                             |
|  [Governance Layer]  <------ IT Steering Committee / CIO              |
|   +----------------------------------------------------------+       |
|   |  COBIT 2019                                              |       |
|   |  +- 5 Domains (EDM, APO, BAI, DSS, MEA)                  |       |
|   |  +- 40 Governance & Management Objectives                |       |
|   |  +- 11 Design Factors (Context-specific tailoring)       |       |
|   +--------------------+-------------------------------------+       |
|                        v                                             |
|  [Management Layer]   <------ IT Managers / PMO                       |
|   +----------------------------------------------------------+       |
|   |  ITIL 4 (34 Practices) + ISO 20000-1:2018                |       |
|   |  +- Service Value System (SVS)                           |       |
|   |  +- 4 Dimensions (Org&People, Info&Tech,                  |       |
|   |  |   Partners&Suppliers, Value Streams&Process)         |       |
|   |  +- 34 Practices (General+Service+Technical)             |       |
|   +--------------------+-------------------------------------+       |
|                        v                                             |
|  [Control Layer]      <------ Internal Audit / External Auditor        |
|   +----------------------------------------------------------+       |
|   |  ISO 27001 (Annex A 93 Controls) + NIST CSF 2.0          |       |
|   |  +- Risk Treatment Plan (RTP)                            |       |
|   |  +- Statement of Applicability (SoA)                     |       |
|   |  +- PDCA Cycle (Plan-Do-Check-Act)                       |       |
|   +----------------------------------------------------------+       |
|                                                                      |
|  [Cross-Cutting]                                                      |
|   - PMBOK 7 / PRINCE2 / SAFe (프로젝트·프로그램 실행)                |
|   - ISO 31000 / COSO ERM (리스크 통합)                                |
|   - Balanced Scorecard (성과 측정)                                    |
|   - TBM (Technology Business Management) (FinOps)                    |
+----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **"오케스트라 지휘자"**와 같다. **COBIT 2019**는 악보(총보), **ITIL 4**는 각 악기 연주법, **ISO 27001**은 음향 장비 안전 점검표이며, **ISO 38500**은 객석의 청중(경영진)이 원하는 무대(가치)를 지휘자에게 알려주는 소통 체계다. 지휘자(CIO) 혼자 연주하면 시끄럽기만 하고, 악보·연주·안전·소통이 맞아야 비로소 "교향곡(Value Stream)"이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019의 Cascade Goals 메커니즘

COBIT 2019는 **40개 Govern/Manage Objective**를 통해 **Enterprise Goals(13개) -> Alignment Goals(13개) -> Governance/Management Objectives(40개)**의 3단 캐스케이드로 IT-사업 정합을 실현한다. 핵심 수식은 다음과 같다:

```
매핑 확률(%) = Σ(Cascade Mapping Weight × Process Capability) / 100
우선순위 점수 = Risk × Impact × (1 - Current Maturity) / Cost-to-Implement
```

```text
[Step 1] Enterprise Goals (13) - 재무/고객/내부/학습 4관점 BSC 매핑
  EG01  Portfolio of competitive products/services
  EG06  Customer-oriented service culture
  EG08  Optimization of internal business process costs
  ...
       |
       |  (Primary Mapping, Weight: 0~1)
       v
[Step 2] Alignment Goals (13) - IT 4관점 BSC 매핑
  AG01  I&T compliance and support for business compliance
  AG04  Quality of financial information
  AG09  Delivering programs on time, on budget
  ...
       |
       |  (Secondary Mapping)
       v
[Step 3] Governance & Management Objectives (40)
  EDM01  Governance Framework Setting & Maintenance
  EDM02  Benefits Delivery
  EDM03  Risk Optimization
  EDM04  Resource Optimization
  EDM05  Stakeholder Transparency
  APO01  I&T Management Framework
  APO12  Risk Management
  BAI03  Manage Solutions
  DSS02  Manage Service Requests and Incidents
  MEA01  Performance & Conformance Monitoring
  ...

[Step 4] Design Factors (11) - 40개 목표의 우선순위 자동 조정
  DF1  Enterprise Strategy (Cost Leader / Differentiation / Innovation)
  DF2  Enterprise Goals (위에서 매핑)
  DF3  Risk Profile (risk map y-axis)
  DF4  I&T-related issues (관련 이슈 17개)
  DF5  Threat Landscape (사이버 위협 환경)
  DF6  Compliance Requirements (GDPR, AI Act, ISMS-P)
  DF7  Role of IT (Factory / Turnaround / Strategic / Factory+Support)
  DF8  Sourcing Model for IT (Outsourcing/In-house/Hybrid)
  DF9  IT Implementation Methods (Agile/DevOps/Traditional)
  DF10 Technology Adoption Strategy (Early Adopter/Follower/Laggard)
  DF11 Enterprise Size (Large/Medium/Small)
```

### 2) ITIL 4 Service Value System (SVS) 상세

ITIL 4의 **Service Value Chain(SVC)**은 **6개 활동(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)**으로 구성되며, 각 활동은 **34개 Practice** 중 관련 활동을 호출한다. Op-model(Operating Model)은 **CI(Configuration Item)** 단위로 추적되며, CMDB에는 일반적으로 **CI Type 200개 이상**(Application, Server, Network Device, Business Service, Contract 등)을 등록한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance(EDM)** | 전략·리스크·자원·이해관계자 4대 의사결정 | COBIT 2019 EDM01~05; 의사결정 권한은 **RACI**로 명확화(R: CIO, A: CEO, C: CFO, I: 사업부장); 분기 1회 거버넌스 위원회 |
| **Plan(APO)** | IT 전략·아키텍처·포트폴리오·예산 | COBIT 2019 APO01~14; **IT Portfolio**: Classify(Demand/Run/Transform), Prioritize(WSJF=Cost of Delay / Job Size); **TBM(Technology Business Management)**로 Application TCO 가시화 |
| **Build/Acquire(BAI)** | 솔루션 설계·구축·전환 | COBIT 2019 BAI01~11; **SAFe/Scrum**으로 Agile Delivery, **DORA Metrics**(Deployment Freq, Lead Time, MTTR, Change Fail Rate) 측정; **CI/CD Pipeline** 자동화 |
| **Deliver & Support(DSS)** | 서비스 운영·장애·요청 처리 | COBIT 2019 DSS01~06; **ITIL 4 Incident Management**: P1(전사 중단, MTTR ≤ 60분), P2(핵심 서비스, ≤ 4시간), P3(개별 사용자, ≤ 24시간), P4(요청, ≤ 5영업일) |
| **Monitor/Evaluate(MEA)** | 성능·규제·이행 측정 | COBIT 2019 MEA01~04; **CMMI/COBIT PAM** 기반 Capability Level(0~5) 측정; 내부감사(IS Audit) 연 1회, 외부감사(연 1회) |
| **Information Security(IS)** | 사이버 리스크·컴플라이언스 | **ISO 27001 Annex A 93개 통제항목** 중 11개 조직 통제 + 75개 기술 통제 + 7개 물리 통제; **NIST CSF 2.0 Govern 함수** 추가(2024) |

### 3) ISO/IEC 38500의 6원칙과 3-단계 거버넌스 사이클

ISO 38500은 **"Evaluate -> Direct -> Monitor"**의 3단계 사이클을 **"Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior"** 6원칙 위에서 수행한다. 이는 **PDCA의 상위 메타 거버넌스**로, COBIT 2019의 EDM 도메인과 직접 매핑된다.

```text
        Board / Governing Body
   +---------------------------------+
   |  Evaluate (Plan + Review)       |<--- 6 Principles
   |  - 환경 분석 (PESTLE + SWOT)    |    1.Responsibility
   |  - IT 전략 평가                  |    2.Strategy
   |  - 리스크 식별                  |    3.Acquisition
   +---------------------------------+    4.Performance
   |  Direct (Decide + Implement)    |    5.Conformance
   |  - 정책/표준 승인                |    6.Human Behavior
   |  - 자원 할당 (Capex/Opex)       |
   |  - 거버넌스 시스템 도입 결정     |
   +---------------------------------+
   |  Monitor (Audit + Correct)      |
   |  - KPI 대시보드                  |
   |  - 내부감사 (IS Audit)          |
   |  - 시정 조치 (Corrective Action) |
   +---------------------------------+
                  |
                  v
        Management (Executive)
        -------------------
        - COBIT 2019 Management Objectives (APO/BAI/DSS/MEA)
        - ITIL 4 Service Value System
        - PMBOK 7 / PRINCE2 / SAFe
```

### 4) 핵심 정량 파라미터

| 메트릭 | 정의 | 목표치(Industry Benchmark) | 측정 주기 |
| :--- | :--- | :--- | :--- |
| **COBIT Capability Level** | 프로세스 성숙도 (0~5) | Level 3(Defined) -> Level 4(Managed) | 연 1회 |
| **DORA Deployment Frequency** | 배포 빈도 | Elite: On-demand(1일 수회), High: 1일~1주 | 주간 |
| **DORA Lead Time for Change** | commit->prod 시간 | Elite: < 1시간, High:
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 764 / 800

<- **이전**: [763. IT 경영 관리 핵심 토픽 763번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/763_it_management_core_topic_763_exam_summary/)
**다음**: [765. IT 경영 관리 핵심 토픽 765번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/765_it_management_core_topic_765_exam_summary/) ->

---
