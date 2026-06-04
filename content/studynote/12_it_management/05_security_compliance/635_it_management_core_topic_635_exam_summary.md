+++
title = "635. IT 경영 관리 핵심 토픽 635번 시험 요약 (IT Management Core Topic 635 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019, ITIL 4, ISO/IEC 38500, ISO 27001** 등 거버넌스 프레임워크를 기반으로, **IT 전략-투자-운영-평가-리스크**의 전生命周期(Lifecycle)을 **EA(Enterprise Architecture)**, **BPM**, **BSC(균형성과표)**로 통합 정렬하여 비즈니스 가치(ROI/NPV/ROA)를 극대화하는 경영 체계이다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 **IT 투자 대비 ROI 20~40% 향상**(Gartner 2023), **프로젝트 실패율 30% -> 10% 감소**(Standish Group CHAOS Report), **IT 운영 비용 15~25% 절감**, **컴플라이언스 위반 리스크 60% 이상 감소**, 의사결정 속도 2~3배 향상을 통한 **디지털 전환(DX) 경쟁력 확보**가 가능하다.
> 3. **판단 포인트**: **(①) Frameworks(COBIT vs ITIL vs PMBOK) 선택과 통합 범위, (②) Balanced Scorecard 4관점(재무/고객/내부/학습성장) KPI 설계, (③) 중앙집중형(Federal) vs 분산형(Devolved) 거버넌스 모델 채택, (④) Agile-Waterfall 하이브리드 방법론(SAFe, Spotify) 적용, (⑤) 사이버 리스크 제로트러스트(Zero Trust) 연계**가 기술사 핵심 판단 포인트이다.

---

## Ⅰ. 개요 및 필요성

현대 기업 환경에서 IT는 단순한 **비용센터(Cost Center)**에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)** 및 **프로핏 센터(Profit Center)**로 역할이 전환되었다. 4차 산업혁명, 생성형 AI(Generative AI), 클라우드 네이티브, 데이터 경제(Data Economy) 환경에서 IT 경영은 **"Right IT, Right Time, Right Cost, Right Quality"** 원칙 하에 비즈니스 전략과 IT의 정렬(IT-Business Alignment)을 보장해야 한다.

그러나 현실에서는 **연간 IT 예산의 약 30%가 실패한 프로젝트에 낭비**(McKinsey 2022), **CxO와 CIO 간의 IT 가치 인식 괴리(Value Gap)**, **Shadow IT로 인한 보안 사고**, **규제 준수(Compliance) 부담 증가** 등의 문제가 상존한다. 이를 해결하기 위해 **IT 거버넌스(IT Governance)**는 이사회 및 경영진의 책임하에 **의사결정 권한, 책임 구조, 통제 메커니즘**을 체계화하고, **IT 서비스 관리(ITSM)**는 ITIL 기반으로 서비스 품질을 관리하며, **프로젝트 관리**는 PMBOK/PRINCE2로 표준화한다.

```text
+------------------------------------------------------------------+
|        IT 경영 관리 통합 프레임워크 (IT Management Framework)      |
+------------------------------------------------------------------+
|                                                                  |
|  +-------------- 이사회/경영진 (Board / Executive Mgmt) ---------+|
|  |   ◈ IT 거버넌스 정책 결정  ◈ IT 투자 승인  ◈ 리스크 감독       ||
|  +-------------------------+------------------------------------+|
|                            |                                     |
|  +-------------------------v------------------------------------+|
|  |       전략 정렬 계층 (Strategy Alignment Layer)               ||
|  |  +-------------+  +-------------+  +----------------------+  ||
|  |  |  ISP/BSP    |  |  EA(TOGAF)  |  |  IT 투자 포트폴리오  |  ||
|  |  | 정보화전략  |  |  아키텍처   |  |   관리(IT PMO)       |  ||
|  |  +-------------+  +-------------+  +----------------------+  ||
|  +-------------------------+------------------------------------+|
|                            |                                     |
|  +-------------------------v------------------------------------+
|  |       거버넌스·운영 계층 (Governance & Operations)            |
|  |  +-------------+  +-------------+  +----------------------+  |
|  |  |   COBIT     |  |   ITIL 4    |  |   PMBOK 7 / PRINCE2 |  |
|  |  |  (통제·평가)|  | (서비스관리)|  |   (프로젝트 관리)    |  |
|  |  +-------------+  +-------------+  +----------------------+  |
|  |  +-------------+  +-------------+  +----------------------+  |
|  |  | ISO 38500   |  | ISO 27001   |  |   ISO 20000          |  |
|  |  |(거버넌스)   |  |(정보보안)   |  |   (서비스 품질)      |  |
|  |  +-------------+  +-------------+  +----------------------+  |
|  +-------------------------+------------------------------------+
|                            |                                     |
|  +-------------------------v------------------------------------+
|  |       평가·지표 계층 (Measurement & Performance)              |
|  |  +-------------+  +-------------+  +----------------------+  |
|  |  |  BSC        |  |  KPI / SLA  |  |  CMMI / TMMi         |  |
|  |  | (균형성과표)|  | (성과지표)  |  |  (성숙도 모델)        |  |
|  |  +-------------+  +-------------+  +----------------------+  |
|  +--------------------------------------------------------------+
|                                                                  |
+------------------------------------------------------------------+
```

**전통적 IT 관리 vs 현대 IT 경영 비교**

| 구분 | 전통적 IT 관리 (Pre-2010) | 현대 IT 경영 (2020~) |
|:---|:---|:---|
| **관점** | 비용(Cost) · 기술 중심 | 가치(Value) · 비즈니스 중심 |
| **구조** | 기능별 실리콘(Silo) 조직 | 수평적 Agile/Squad 조직 |
| **투자** | CapEx 일회성 대규모 투자 | OpEx 구독형, 점진적(Iterative) |
| **위험** | 사후 대응(Reactive) | 사전 예측(Predictive, AI 기반) |
| **거버넌스** | 중앙 집중 통제 | 분산형 거버넌스 + 중앙 정책 |
| **측정** | 가용성(Uptime) 중심 | 가치·경험·탄소 등 ESG 통합 |
| **기술** | On-premise, Monolith | Cloud-native, SaaS, MASA |

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판과 내비게이션**과 같습니다. 엔진(IT 인프라)이 아무리 좋아도 **방향(전략)**, **속도(KPI)**, **연료 효율(ROI)**, **안전벨트(보안·리스크)**이 통합되어 있어야 목적지(비즈니스 가치)에 안전하고 효율적으로 도착할 수 있습니다. COBIT은 도로교통법, ITIL은 정비 매뉴얼, PMBOK은 여행 일정표에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 아키텍처는 크게 **① 전략 계층(Strategy Layer)**, **② 거버넌스 계층(Governance Layer)**, **③ 운영 계층(Operations Layer)**, **④ 평가 계층(Measurement Layer)**의 4계층으로 구성되며, 각 계층은 **PDCA(Plan-Do-Check-Act)** + **Deming Cycle** + **COBIT의 EDM(평가·지휘·모니터)** 프로세스로 연결된다.

```text
+------------------------------------------------------------------+
|         COBIT 2019 거버넌스 시스템 (Governance System)            |
+------------------------------------------------------------------+
|                                                                  |
|   +----------------------------------------------------------+   |
|   |  Governance System Components (거버넌스 시스템 5대 원칙) |   |
|   |  ① Each enterprise needs its own system                  |   |
|   |  ② Governance system covers all enterprise activities    |   |
|   |  ③ Apply a single integrated framework                   |   |
|   |  ④ Enabling a holistic approach                          |   |
|   |  ⑤ Distinguishing governance from management             |   |
|   +----------------------------------------------------------+   |
|                              |                                   |
|   +--------------------------v------------------------------+   |
|   |   ① Governance Objectives (40개 목표)                   |   |
|   |       ↕ 정렬                                            |   |
|   |   ② Components: Process / Organizational Structures /    |   |
|   |      Information Flows / People, Skills & Competencies / |   |
|   |      Policies & Procedures / Culture, Ethics & Behavior /|   |
|   |      Services, Infrastructure & Applications             |   |
|   |       ↕ 매핑                                            |   |
|   |   ③ Design Factors (13개) -> 시스템 맞춤화                |   |
|   +----------------------------------------------------------+   |
|                              |                                   |
|   +--------------------------v------------------------------+   |
|   |   EDM : Evaluate, Direct, Monitor (거버넌스 5개 도메인) |   |
|   |   APO : Align, Plan, Organize (관리 14개 도메인)         |   |
|   |   BAI : Build, Acquire, Implement (11개 도메인)          |   |
|   |   DSS : Deliver, Service, Support (6개 도메인)           |   |
|   |   MEA : Monitor, Evaluate, Assess (4개 도메인)           |   |
|   +----------------------------------------------------------+   |
|                              |                                   |
|   +--------------------------v------------------------------+   |
|   |   Focus Areas (포커스 영역) : 사이버보안, DevOps,        |   |
|   |   위험, 디지털 윤리, 클라우드, AI 거버넌스 등            |   |
|   +----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

### 핵심 프레임워크별 세부 구성

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019** | IT 거버넌스·관리 통합 프레임워크 | 40개 거버넌스/관리 목표, **5개 도메인(EDM, APO, BAI, DSS, MEA)**, 13개 디자인 팩터(전략, 목표, 리스크, 사이버보안 등)로 조직 맞춤화, **Capability/Maturity Model(0~5단계)** 기반 성숙도 평가 |
| **ITIL 4 (2019)** | IT 서비스 관리(ITSM) 모범 사례 | **Service Value System(SVS)**: Opportunity/Demand -> Value -> Guiding Principles(7원칙) -> Governance -> Practices -> Continual Improvement, **34개 Practice**(변경관리, 인시던트, 문제관리, 서비스데스크 등), **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) |
| **ISO/IEC 38500:2015** | IT 거버넌스 국제표준 | **3원칙(책임, 전략, 획득)**, **6개 거버넌스 영역(Principle)**: Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior, **Governance->Management->Operational** 3계층 책임 분리(RACI) |
| **PMBOK 7th (2021)** | 프로젝트 관리 지식 체계 | **8개 Performance Domains**(팀, 개발방식/수명주기, 계획, 프로젝트 작업, 전달, 측정, 불확실성, 콘텐츠), **12가지 Principle**(Stewardship, Team, Development Approach, Planning, …), **Predictive/Adaptive/Hybrid** 3대 개발방식 |
| **Balanced Scorecard(BSC)** | 전략적 성과 측정 체계 | **4관점(재무/고객/내부프로세스/학습성장) × 4단계(임무->전략->측정지표->과제)**, **Strategy Map**으로 인과관계(Causality) 시각화, **KPI + CSF(Critical Success Factor) + KGI(Key Goal Indicator)** |

### 핵심 측정 지표 및 공식

```text
  +------------------------------------------------------+
  |  ① IT 투자 가치 측정 공식                              |
  |  -------------------------------------------------   |
  |  • ROI = (IT 투자로 인한 이익 / IT 투자 비용) × 100   |
  |  • NPV = Σ [CFt / (1+r)^t] - 초기 투자비             |
  |  • EVA = NOPAT - (WACC × 투자 자본)                   |
  |  • TCO = 직접비용 + 간접비용 + 기회비용 + 위험비용     |
  |  • Payback Period = 투자비 / 연간 현금유입액           |
  +------------------------------------------------------+
  |  ② IT 운영 효율 측정                                   |
  |  -------------------------------------------------   |
  |  • SLA 준수율 = (SLA达标 / 총 SLA) × 100              |
  |  • MTTR = Σ(장애복구시간) / 장애 건수                 |
  |  • MTBF = 총 가동시간 / 장애 건수                      |
  |  • 가용성(Availability) = MTBF / (MTBF + MTTR) × 100  |
  |  • CSAT(고객만족도) = 5점 척도 설문 평균              |
  +------------------------------------------------------+
  |  ③ 거버넌스 성숙도 (COBIT/Capability Level 0~5)       |
  |  -------------------------------------------------   |
  |  Level 0 : Incomplete (불완전)                         |
  |  Level 1 : Initial/Performed (초기·수행)               |
  |  Level 2 : Managed (관리됨)  -> Process Attribute 1.1~ |
  |  Level 3 : Defined (정의됨) -> PA 2.1~2.2              |
  |  Level 4 : Quantitative (정량적) -> PA 3.1~3.2         |
  |  Level 5 : Optimizing (최적화) -> PA 4.1~4.2           |
  +------------------------------------------------------+
```

- **📢 섹션 요약 비유**: COBIT은 **건축물의 설계도·건축법·시공 매뉴얼이 통합된 건축기준법**과 같습니다. EDM은 도시계획(상위), APO는 건축설계, BAI는 시공, DSS는 입주 후 운영·유지보수, MEA는 준공검사·성능평가에 해당합니다. 13개 디자인 팩터는 "이 부지에 어떤 건물을 지을 것인가"를 결정하는 토지 조건, 예산, 사용자 니즈 같은 변수입니다.

---

## Ⅲ. 비교 및 연결

### 프레임워크 간 비교 분석

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 635 / 800

<- **이전**: [634. IT 경영 관리 핵심 토픽 634번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/634_it_management_core_topic_634_exam_summary/)
**다음**: [636. IT 경영 관리 핵심 토픽 636번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/636_it_management_core_topic_636_exam_summary/) ->

---
