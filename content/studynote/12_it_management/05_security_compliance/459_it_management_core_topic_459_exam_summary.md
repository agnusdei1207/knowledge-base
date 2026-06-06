---
title: "IT Management Core Topic 459 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(459번)는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 시스템(SVS), ISO 38500 IT 거버넌스 국제표준, Balanced Scorecard(BSC) 4관점, 그리고 EA(Enterprise Architecture) 기반의 TOGAF ADM을 통합하여 IT-Business Alignment와 가치 창출을 최적화하는 경영 프레임워크 체계이다.
> 2. **가치**: IDC 및 Gartner 분석에 따르면 성숙한 IT 거버넌스 체계 도입 시 IT 투자 대비 ROI가 평균 25~40% 향상되고, IT 프로젝트 실패율은 McKinsey 기준 70%에서 30% 이하로 감소하며, 디지털 트랜스포메이션 성공률은 Boston Consulting Group(BCG) 조사에서 35% -> 75%로 증가한다.
> 3. **판단 포인트**: 거버넌스-관리-운영(Govern-Build-Run) 계층 분리, RACI 매트릭스 기반 의사결정 권한 분배, 포트폴리오-PMO-프로젝트 3계층 거버넌스, 그리고 CSF(KPI) -> KGI(목표) -> KPI(성과지표) 의 인과사슬 설계 시 Balanced vs Focused 전략 간 trade-off가 핵심 쟁점이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management, ITM)는 기업의 미션·비전·전략을 IT 역량과 연결하여, 제한된 자원 내에서 최대의 비즈니스 가치를 창출하기 위한 통합 관리 체계이다. 4차 산업혁명, 클라우드 전환, 생성형 AI(LLM, RAG), ESG 컴플라이언스(CSRD, TCFD), 그리고 사이버보안 위협의 고도화(제로트러스트, 양자내성암호 PQC)로 인해 IT의 역할이 단순 비용센터(Cost Center)에서 전략적 비즈니스 파트너(Strategic Enabler)로 전환됨에 따라 체계적 IT 경영 관리의 필요성이 부각되고 있다.

기존의 IT 관리(2000년대 이전)는 시스템별 개별 운영(Siloed Operation)과 CapEx 중심의 예산 관리가 주를 이루었으나, 현재는 다음과 같은 패러다임 전환이 발생하였다:

```text
+-----------------------------------------------------------------------------+
|           IT 경영 관리 패러다임 전환 (Legacy -> Modern)                       |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [Legacy Paradigm]                      [Modern Paradigm]                   |
|                                                                             |
|   +------------------+                   +------------------+                |
|   | Cost Center 관점  |  ---------------► | Value Center 관점 |                |
|   | TCO 최소화가 목표 |                   | EBITDA 기여 극대화|                |
|   +------------------+                   +------------------+                |
|                                                                             |
|   +------------------+                   +------------------+                |
|   | Siloed 시스템 운영|  ---------------► | E2E 가치사슬 통합 |                |
|   | 부서별 독자 SW/HW|                   | API-first, iPaaS  |                |
|   +------------------+                   +------------------+                |
|                                                                             |
|   +------------------+                   +------------------+                |
|   | CapEx 일시집중투자|  ---------------► | OpEx + CapEx 혼합 |                |
|   | HW 구매 중심     |                   | SaaS, IaaS 구독형 |                |
|   +------------------+                   +------------------+                |
|                                                                             |
|   +------------------+                   +------------------+                |
|   | 프로젝트 단위 관리|  ---------------► | 포트폴리오 관리   |                |
|   | 개별 일정·품질   |                   | PPM, OKR 연계     |                |
|   +------------------+                   +------------------+                |
|                                                                             |
|   +------------------+                   +------------------+                |
|   | 통제 중심(Control)|  ---------------► | 유연성+통제(Agile)|                |
|   | Waterfall, CMMI  |                   | DevSecOps, SAFe  |                |
|   +------------------+                   +------------------+                |
|                                                                             |
+-----------------------------------------------------------------------------+
```

기술사적 관점에서 IT 경영 관리는 ① IT 거버넌스(Governance), ② IT 서비스 관리(Service Management), ③ IT 전략·포트폴리오 관리, ④ IT 성과·위험 관리, ⑤ 엔터프라이즈 아키텍처(EA) 운용의 5대 축으로 구성되며, 이들이 **"Value Optimization Loop"**를 형성하여 지속적으로 개선되어야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'운전대(전략) + 계기판(성과측정) + 브레이크(위험통제) + 엔진룸(아키텍처) + 정비소(ITSM)'**가 한 시스템으로 통합된 **'F1 레이싱 카의 통합 텔레메트리 시스템'**과 같다. 각 부분이 독립적이 아니라 실시간 데이터로 연결되어야 최적의 레이싱(비즈니스 성과)을 달성할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 축은 다음과 같은 계층적 참조 모델(Hierarchical Reference Model)로 구성된다. 이는 ISO 38500의 6개 원칙(Direct, Plan, Source, Deliver, Support, Monitor)과 COBIT 2019의 40개 관리 목표(Management Objective)를 포괄한다.

```text
+------------------------------------------------------------------------------+
|        IT 경영 관리 5대 축 통합 참조 모델 (ITM-5A Reference Model)            |
+------------------------------------------------------------------------------+
|                                                                              |
|  Layer 5: Enterprise Strategy (ISO 38500, COBIT EDM)                        |
|  +--------------------------------------------------------------------+      |
|  | 비전/미션 -> IT 전략 -> BSC 4관점(재무/고객/내부/학습성장)         |      |
|  | 의사결정: 이사회 -> CEO -> CIO(CXO 레벨) -> IT steering Committee  |      |
|  +--------------------------------------------------------------------+      |
|            ^                           ^                          ^          |
|  Layer 4: IT Governance (COBIT 2019)    |                          |          |
|  +--------------------------------------------------------------------+      |
|  | EDM (Evaluate, Direct, Monitor) --+                               |      |
|  | 거버넌스 시스템: 원칙/정책/지표/문화/인프라/사람/리스크 7요소     |      |
|  | Stakeholder Needs -> Goals Cascade (13 Enterprise Goals -> 13 IT  |      |
|  | Related Goals -> Alignment Goals)                                |      |
|  +--------------------------------------------------------------------+      |
|            ^                                                              |   |
|  Layer 3: IT Service Management (ITIL 4 SVS)                                |   |
|  +--------------------------------------------------------------------+      |
|  |  +-------------+  +--------------+  +--------------+               |   |
|  |  | Service     |  | Service      |  | Continual    |               |   |
|  |  | Strategy    |--| Design (SD)  |--| Improvement  |               |   |
|  |  +-------------+  +--------------+  +--------------+               |   |
|  |  +-------------+  +--------------+  +--------------+               |   |
|  |  | Service     |  | Service      |  | Service      |               |   |
|  |  | Transition  |--| Operation    |--| Value Chain  |               |   |
|  |  +-------------+  +--------------+  +--------------+               |   |
|  |  34 Practices (신규/개편) ------------------------------------    |   |
|  +--------------------------------------------------------------------+      |
|            ^                                                              |   |
|  Layer 2: Portfolio & Project (PPM) + Agile                                |   |
|  +--------------------------------------------------------------------+      |
|  | 전략적 포트폴리오 -> 전술적 프로그램 -> 실행 프로젝트 -> 백로그      |      |
|  | 방법론: SAFe 6.0 / Scrum / Kanban / Hybrid / PMBOK 7th           |      |
|  | PMO: Enterprise PMO -> Divisional PMO -> Project PMO              |      |
|  +--------------------------------------------------------------------+      |
|            ^                                                              |   |
|  Layer 1: Enterprise Architecture (TOGAF ADM + Zachman)                     |   |
|  +--------------------------------------------------------------------+      |
|  |  ADM Cycle:                                                       |      |
|  |  Preliminary -> A(Architecture Vision) -> B~D(BSD) -> E,F(Opportunities|   |
|  |  & Solutions) -> G(Implementation Governance) -> H(Architecture      |   |
|  |  Change Management) -> Requirements Management (RM)                |      |
|  |  Zachman 6x6: What/How/Where/Who/When/Why × Planner/Owner/        |      |
|  |  Designer/Builder/Subcontractor/Operational                        |      |
|  +--------------------------------------------------------------------+      |
|                                                                              |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Layer 5: 전략 거버넌스 (EDM)** | 비전·미션과 IT 정렬(Alignment) | COBIT 2019 EDM 도메인의 Evaluate/Direct/Monitor 5단계 사이클, ISO 38500 6원칙(Risk, Strategy, Performance, Conformance, Human Behavior, Environment), BSC(Kaplan & Norton) 4관점 인과지도(Cause-and-Effect Map) |
| **Layer 4: IT 거버넌스 시스템** | 의사결정·책임·통제 구조 확립 | COBIT 2019의 40개 관리목표(예: EDM01, APO01, BAI01, DSS01, MEA01), RACI 매트릭스(Responsible/Accountable/Consulted/Informed), Three Lines Model(IIA 2020), 7가지 거버넌스 컴포넌트(원칙/정책/프레임워크/정보/문화/인프라/인적자원) |
| **Layer 3: ITIL 4 SVS** | 서비스 가치(Value) 창출·전달·지원 | SVS 핵심요소: Opportunity/Demand -> Value -> Guiding Principles(7개: Focus on Value, Start Where You Are, Progress Iteratively, etc.) -> 4 Dimensions(P-O-V-I: 조직/사람/정보기술/공급자/파트너/가치흐름), 34 Practices(예: Incident Mgmt, Problem Mgmt, Change Enablement, Service Desk, SLM, SLO/SLI) |
| **Layer 2: PPM + Agile** | 전략을 실행으로 전환 | 포트폴리오 분류(Compliance/Operational/Strategic/High-Risk) -> NPV/IRR/ROIC 분석 -> OKR(Objectives & Key Results) -> SAFe 6.0 PI Planning(Big Room Event) -> Epic->Feature->Story->Task 분해, WSJF(Weighted Shortest Job First) 우선순위 산정 |
| **Layer 1: EA (TOGAF/Zachman)** | 표준화된 아키텍처 청사진 | TOGAF ADM 8단계 + RM 반복, Architecture Repository(ABD/ABB/AB/ARB/Compliance/Governance), Zachman 6x6 셀 매트릭스, BIZ-META-APP-TECH 4-레이어(ArchiMate 3.2), MOF(Microsoft Operations Framework), FEAF(연방 EA) |

**핵심 원리 ① - Goals Cascade (목표 연쇄)**: COBIT 2019는 **Stakeholder Drivers -> 13 Enterprise Goals -> 13 IT-Related Goals -> 40+ Management Objectives**로 이어지는 인과사슬을 통해 상위 거버넌스 목표가 하위 운영 단위로 변환되는 메커니즘을 정의한다. 각 단계의 연결은 **Primary/Secondary Mapping**으로 표시되며, KPI 예시는 다음과 같다:

- EG01 (포트폴리오의 경쟁제품/서비스): EG08 (정보 기반 의사결정) -> ITG02 (정보처리인프라) -> MG(DSS02 - Managed Service Requests) -> KPI(서비스요청 평균처리시간 MTRS, SLA 준수율)
- EG06 (비즈니스 기능 비용 최적화) -> ITG04 (관리된 IT 자원) -> MG(APO04 - Managed Innovation) -> KPI(TCO 절감률, Cost per Transaction)

**핵심 원리 ② - VFQ(Value, Fitness, Quality) 트레이드오프**: ITIL 4에서는 어떤 서비스를 우선 개선할지 결정할 때 Utility(기능/적합성) × Warranty(보증/신뢰성) × Cost를 동시에 고려한다. Utility는 "What it does"(적합한 기능), Warranty는 "How well it does"(가용성, 용량, 보안, 연속성)로 분리된다.

**핵심 원리 ③ - BSC의 4관점 인과관계**:
- 재무 -> 내부 프로세스 -> 학습·성장 -> 고객 -> 재무 (가치 창출의 인과 루프)
- Lagging Indicator(결과) vs Leading Indicator(선행) 균형 (예: ROI(Lag) -> 프로세스 자동화율(Lead))

- **📢 섹션 요약 비유**: IT 경영 관리의 5대 축은 **'건물의 구조 시스템'**과 같다. EA(설계도), PPM(공사 일정), ITIL(설비 운영), Governance(소방·안전 규정), 전략(건물의 목적·임대 전략)이 서로 연결되어야 건물이 무너지지 않고 가치를 창출한다. 설계도 없이 짓거나, 정비를 안 하는 건물은 시간이 지날수록 **'IT 부채(Technical Debt)'**라는 균열이 생긴다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 프레임워크는 각각 다른 영역에 최적화되어 있으며, 실무에서는 상호 보완적으로 적용된다. 다음은 주요 프레임워크 간의 비교이다:

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO 38500:2015** | **TOGAF 10 (2022)** | **PMBOK 7th (2021)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주요 목적** | IT 거버넌스·관리 통합 | IT 서비스 라이프사이클 관리 | IT 의사결정의 거버넌스 원칙 | 엔터프라이즈 아키텍처 개발 | 프로젝트 관리 원칙·도메인 |
| **관리 범위** | End-to-End (전략->운영) | 주로 운영·전달 단계 | 거버넌스(상위 의사결정) | 아키텍처 설계·구현 | 단일 프로젝트 |
| **구조** | 40 관리목표 + 7 컴포넌트 | SVS + 34 Practices | 6 원칙 + 5 거버넌스 모델 | ADM 8단계 + Repository | 12 Principles + 8 Domains |
| **핵심 산출물** | Goals Cascade, RACI, Maturity Model | Service Value Chain, SLO/SLI | Governance Charter, Decision Rights | Architecture Deliverable (ABD) | Project Charter, Risk Register |
| **적합 조직** | 대규모·규제 산업(금융, 공공) | 모든 서비스 조직 | 글로벌·다국적 기업 | 아키텍처 성숙도 높은 조직 | 프로젝트 성숙도 낮은 조직 |
| **연계 가능 프레임워크** | ISO 27001(보안), NIST CSF, CMMI | DevOps, SRE, SLO(SRE), Lean IT | ISO 27014, COBIT EDM | ArchiMate 3.2, BPMN, DMN | PRINCE2, ISO 21502, SAFe |
| **측정 모델** | Maturity 0~5 (CMMI 호환) | Service Maturity, 4D Assessment | Principles Compliance Audit | ADM Maturity Model | 12 Project Performance Domains |
| **2020년대 트렌드** | Focus Area (예: DevOps, Risk) | 4 Dimensions, VUCA 대응 | 책임성(Accountability) 강조 | Microservices EA, Cloud Native | Principles-based,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 459 / 800

<- **이전**: [458. IT 경영 관리 핵심 토픽 458번 시험 요약](/studynote/12_it_management/05_security_compliance/458_it_management_core_topic_458_exam_summary/)
**다음**: [460. IT 경영 관리 핵심 토픽 460번 시험 요약](/studynote/12_it_management/05_security_compliance/460_it_management_core_topic_460_exam_summary/) ->

---
