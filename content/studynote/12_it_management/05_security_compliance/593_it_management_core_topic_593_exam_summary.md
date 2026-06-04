+++
title = "593. IT 경영 관리 핵심 토픽 593번 시험 요약 (IT Management Core Topic 593 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(593번)는 COBIT 2019, ITIL 4, ISO 38500 등 글로벌 거버넌스 프레임워크를 기반으로 **IT 거버넌스(Governance) ↔ IT 관리(Management) ↔ IT 운영(Operation)**의 3계층 구조를 통해 기업의 디지털 전환(Digital Transformation) 전략과 IT 투자의 정렬(Strategic Alignment)을 실현하는 종합 관리 체계이다.
> 2. **가치**: McKinsey & Company 연구에 따르면 효과적인 IT 거버넌스 도입 기업은 **IT 투자 대비 ROI가 25~40% 향상**, 프로젝트 실패율 30% 감소, Time-to-Market 20% 단축, IT 비용의 15~25% 절감( Gartner, 2023) 효과를 달성하며, ESG·컴플라이언스 리스크를 사전 예방한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 표준 프레임워크 도입 vs. 조직 맞춤화(As-Is vs. To-Be Gap)**, **② 중앙집중적 거버넌스(Centralized) vs. 분산형 거버넌스(Federated)**, **③ Agile/DevOps 속도 vs. 거버넌스 통제(Control) 균형**이며, 기술사적 판단은 RACI 매트릭스, 거버넌스 성숙도 모델(Process Maturity Model), 그리고 Cost of Governance vs. Value of Governance의 정량적 분석을 기반으로 내려야 한다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 단순한 IT 운영 관리를 넘어, 기업의 비즈니스 전략과 IT 서비스·프로세스·인프라를 통합적으로 정렬(Alignment)하고, 가치(Value)를 극대화하며 리스크를 통제하는 **엔터프라이즈 차원의 관리 체계**이다. 4차 산업혁명 시대에 기업의 60~70% 비즈니스 프로세스가 IT에 의존하고, 클라우드·AI·데이터 분석 등 신기술 도입이 가속화되면서 IT 투자의 규모와 복잡성이 폭증하였다. 그러나 McKinsey Global Survey(2023)에 따르면 **대기업의 70% 이상이 디지털 전환 이니셔티브에서 기대 ROI를 달성하지 못하고** 있으며, CIO Survey(2024)에 따르면 IT 리더의 최대 관심사 1위가 **"IT 거버넌스 및 비용 최적화"**로 집계될 정도로 IT 경영의 체계화가 시급한 과제이다.

기존의 IT 관리(Traditional IT Management)는 ITIL v2 기반의 프로세스 중심·기능 중심(Funtional Silo) 접근으로, **① IT와 비즈니스 간 전략적 괴리(Strategy Gap)**, **② 부서별 중복 투자와 사일로(Silo) 현상**, **③ 리스크·컴플라이언스 통제 미흡**, **④ 프로젝트 중심 사고로 인한 Portfolio 최적화 부재**, **⑤ ROI 측정의 비정량성** 등의 한계를 노출했다. 이를 극복하기 위해 등장한 현대 IT 경영 관리(Modern IT Governance & Management)는 **COBIT 2019(거버넌스·관리 목표 프레임워크)**, **ITIL 4(서비스 가치 시스템)**, **ISO/IEC 38500(거버넌스 원칙)**, **TOGAF 10(엔터프라이즈 아키텍처)**, **ISO 27001(정보보안경영)**, **ISO 22301(비즈니스 연속성)**, **CMMI(프로세스 성숙도)** 등 다중 프레임워크를 통합 적용하는 **Integrated Governance System**으로 진화하였다.

```text
+--------------------------------------------------------------------------+
|         IT 경영 관리의 3계층 통합 거버넌스 프레임워크                     |
+--------------------------------------------------------------------------+
|                                                                          |
|   +------------------------------------------------------------+         |
|   |  1계층: IT 거버넌스 (Governance) - "What & Why"            |         |
|   |  - 의사결정 권한·책임·구조 정의                              |         |
|   |  - 이해관계자(Stakeholder) 가치 최적화                       |         |
|   |  - 프레임워크: COBIT 2019, ISO 38500                        |         |
|   |  - 평가: 40개 거버vernance/Management Objectives             |         |
|   |  - 책임 주체: 이사회·CIO·전략위원회                          |         |
|   +------------------------^-----------------------------------+         |
|                            | (전략적 정렬 Strategic Alignment)          |
|   +------------------------+-----------------------------------+         |
|   |  2계층: IT 관리 (Management) - "How & Who"                |         |
|   |  - 계획·구축·운영·모니터링(Plan/Build/Run/Monitor)          |         |
|   |  - 프레임워크: ITIL 4 SVS, PMBOK 7, PRINCE2, Agile         |         |
|   |  - 조직: PMO, SMO, IT Service Owner                         |         |
|   |  - 핵심 KPI: SLA, ROI, TCO, TBM 비용 분류                  |         |
|   +------------------------^-----------------------------------+         |
|                            | (전술적 실행 Tactical Execution)            |
|   +------------------------+-----------------------------------+         |
|   |  3계층: IT 운영 (Operation) - "Do & Support"               |         |
|   |  - 일상의 IT 서비스 제공·기술 운영                           |         |
|   |  - 프레임워크: ITIL 4 Practices(34개), DevOps, SRE          |         |
|   |  - 조직: Service Desk, NOC, SOC, DevOps Team                |         |
|   |  - 핵심 KPI: MTTR, MTBF, 가용성, 보안사고 수               |         |
|   +------------------------------------------------------------+         |
|                                                                          |
|   ※ 3계층을 관통하는 횡단(Cross-cutting) 요소:                          |
|      - Enterprise Architecture (TOGAF ADM Cycle)                        |
|      - Risk Management (ISO 31000, COSO ERM)                             |
|      - Security & Compliance (ISO 27001, ISMS-P, GDPR, 개인정보보호법)   |
|      - BCM/DR (ISO 22301)                                                |
+--------------------------------------------------------------------------+
```

IT 경영 관리가 필요한 핵심 이유는 다음과 같이 5가지로 요약된다: ① **전략적 정렬(Strategic Alignment)**: 비즈니스 목표와 IT 투자·프로젝트·서비스를 1:1·N:1로 매핑하여 사일로 제거, ② **가치 실현(Value Delivery)**: IT 투자의 정량적 ROI 측정 및 최적 Portfolio 구성, ③ **리스크 관리(Risk Management)**: 정보보안·규제·운영 리스크의 통합 관리 및 ISO 27001·ISMS-P 인증, ④ **자원 최적화(Resource Optimization)**: 인력·예산·인프라의 TCO 분석과 TBM(Tech Business Management) 기반 비용 가시화, ⑤ **성숙도 및 지속가능성(Maturity & Sustainability)**: CMMI·P-CMM 기반 프로세스 개선과 ESG·탄소중립 대응.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **대형 항공사(예: 대한항공)의 종합 운영센터(OCC)**와 같다. OCC는 비행기(시스템·서비스) 한 대의 이륙·운항·착륙(거버넌스)뿐 아니라, 기상(리스크)·유가(비용)·승객(사용자)·항로(아키텍처)·정비(운영)를 통합 관리한다. 아무리 좋은 비행기(IT 시스템)도 OCC가 없으면 사고가 나고, OCC는 기상청·관제탑·정비소 등 외부 기관(외부 프레임워크)과 실시간 협력한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 시스템의 아키텍처는 크게 **거버넌스 시스템(Governance System)**, **관리 시스템(Management System)**, **지원 인프라(Enablers)**로 구성된다. COBIT 2019 기준 40개의 거버넌스/관리 목표(Governance & Management Objectives, 이하 GMO)를 5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess)으로 분류하고, 각 목표는 **Process(프로세스)**, **Organizational Structures(조직)**, **Information Flows(정보 흐름)**, **People/Skills(인력)**, **Policies/Procedures(정책)** 등 7가지 Enablers로 구성된다.

**COBIT 2019의 핵심 메커니즘**은 다음과 같이 4단계로 동작한다: ① **Identify Needs & Problems**: 비즈니스 목표·리스크·문제 정의 -> ② **Design Tailored Governance System**: 40개 GMO 중 우선순위 선정, Design Factors(기업 규모, 산업, 컴플라이언스 등 11개) 적용 -> ③ **Implement(Implementation)**: Quick-Win 우선, 단계적 확대 -> ④ **Monitor & Improve**: Process Capability(0~5단계) 측정 및 지속 개선.

ITIL 4는 2019년 발표된 최신 버전으로, **Service Value System(SVS)** 중심으로 재설계되었다. 핵심 구성은 ① **Opportunity/Demand(Value)**, ② **Engage(Value를 위한 이해관계자 참여)**, ③ **Value(가치 공동창조)**, ④ **Guiding Principles(7개 원칙)**, ⑤ **Governance(거버넌스)**, ⑥ **Service Value Chain(6개 활동: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)**, ⑦ **Practices(34개)**이다. 7가지 Guiding Principles는 Focus on Value, Start Where You Are, Progress Iteratively with Feedback, Collaborate and Promote Visibility, Think and Work Holistically, Keep It Simple and Practical, Optimize and Automate이다.

```text
+----------------------------------------------------------------------+
|    COBIT 2019 × ITIL 4 통합 거버넌스·관리 아키텍처                  |
+----------------------------------------------------------------------+
|                                                                      |
|   +---------------- COBIT 2019 40개 GMO 도메인 --------------+       |
|   |                                                             |       |
|   |  EDM (Governance)                |  APO (Plan/Organize)    |       |
|   |  - EDM01 Governance Framework   |  - APO01 Mgt Framework  |       |
|   |  - EDM02 Benefits Delivery       |  - APO02 Strategy       |       |
|   |  - EDM03 Risk Optimization       |  - APO04 Organization   |       |
|   |  - EDM04 Resource Optimization   |  - APO05 Portfolio      |       |
|   |  - EDM05 Stakeholder Engagement  |  - APO12 Risk           |       |
|   |                                  |  - APO13 Security       |       |
|   |  BAI (Build/Acquire/Implement)   |  DSS (Deliver/Service)  |       |
|   |  - BAI01 Programs                |  - DSS01 Operations     |       |
|   |  - BAI02 Requirements            |  - DSS02 Service Desk   |       |
|   |  - BAI03 Solutions               |  - DSS04 Continuity     |       |
|   |  - BAI05 Organizational Change   |  - DSS05 Security       |       |
|   |                                  |                         |       |
|   |  MEA (Monitor/Evaluate/Assess)                               |       |
|   |  - MEA01 Performance Management  |  - MEA02 Sytem Internal |       |
|   |  - MEA03 External Compliance    |  - MEA04 Assurance      |       |
|   +-------------------------------------------------------------+       |
|                              <-> 매핑(Mapping) <->                          |
|   +--------------- ITIL 4 Service Value Chain (SVC) -----------+       |
|   |                                                              |       |
|   |   [Plan]--->[Engage]--->[Design & Transition]                 |       |
|   |     |                                       |                 |       |
|   |     v                                       v                 |       |
|   |   [Obtain/Build]--->[Deliver & Support]--->[Improve]          |       |
|   |                                                              |       |
|   |   34 Practices: Incident, Problem, Change, SLM,              |       |
|   |                 Service Desk, Monitoring, Release,            |       |
|   |                 Service Request, etc.                        |       |
|   +--------------------------------------------------------------+       |
|                                                                      |
|   +-------- Enablers (COBIT 2019) --------+                            |
|   |  1. Processes (40)                    |                            |
|   |  2. Organizational Structures          |                            |
|   |  3. Information Flows                  |                            |
|   |  4. People, Skills & Competencies      |                            |
|   |  5. Policies & Procedures              |                            |
|   |  6. Services, Infrastructure & Apps    |                            |
|   |  7. Culture, Ethics & Behavior         |                            |
|   +----------------------------------------+                            |
|                                                                      |
|   +--- Cross-Cutting Integration ------------------------------+      |
|   |  TOGAF 10 ADM (ADM Cycle) <- EA 아키텍처 정렬               |      |
|   |  ISO 27001:2022 ISMS <- 정보보안 통제                        |      |
|   |  ISO 22301:2019 BCMS <- 비즈니스 연속성                      |      |
|   |  ISO 31000:2018 Risk <- 리스크 관리                          |      |
|   |  CMMI-DEV v2.0 / P-CMM 3.0 <- 프로세스·인력 성숙도          |      |
|   |  PMBOK 7th / PRINCE2 7 / SAFe 6.0 <- 프로젝트·Agile         |      |
|   +------------------------------------------------------------+      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (Control Objectives for Information and Related Technologies) | IT 거버넌스·관리 목표 통합 프레임워크 | 5개 도메인(EDM/APO/BAI/DSS/MEA) × 40개 GMO, 7개 Enablers, 11개 Design Factors(Strategy, Goals, Risk, I&T Issues, Enterprise Size, etc.), Process Capability Model(0~5단계, ISO/IEC 33020 PAM 기반) |
| **ITIL 4 Foundation/Managing Professional** | IT 서비스 관리(Service Management) 프레임워크 | SVS(Service Value System) - Guiding Principles 7개, SVC 6개 Activity, 34개 Practices(General, Service, Technical), 4축 PESTEL 모델(People/Products/Partners/Process) |
| **ISO/IEC 38500:2015** | IT 거버넌스 국제 표준 | 3대 원칙(Evaluate, Direct, Monitor), 6개 거버넌스 모델(Rule, System Model, Techniques, Owner, Transparency, Accountability), Board·CEO·IT Director 책임 |
| **TOGAF 10 (2022)** | 엔터프라이즈 아키텍처 개발 방법론 | ADM(Architecture Development Method) Cycle 8단계(Preliminary->A:Vision->B:Business
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 593 / 800

<- **이전**: [592. IT 경영 관리 핵심 토픽 592번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/592_it_management_core_topic_592_exam_summary/)
**다음**: [594. IT 경영 관리 핵심 토픽 594번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/594_it_management_core_topic_594_exam_summary/) ->

---
