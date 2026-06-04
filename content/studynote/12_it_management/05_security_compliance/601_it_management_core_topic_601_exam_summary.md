---
title: "601. IT 경영 관리 핵심 토픽 601번 시험 요약 (IT Management Core Topic 601 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 601번은 **COBIT 2019 거버넌스 체계**, **IT 전략-포트폴리오-아키텍처 정렬(Strategy-Architecture-Project Alignment)**, **BSC-IT 성과측정**의 3축을 통해 기업 가치(Value Delivery)를 극대화하는 경영 프레임워크 통합 운용 능력을 평가하는 시험이다.
> 2. **가치**: 글로벌 스탠더드(COBIT 2019, ITIL 4, PMBOK 7, ISO 38500, TOGAF 10) 기반의 정량적 ROI·TCO 분석을 통해 **IT 투자 수익률(ROIT) 15~25% 향상**, **프로젝트 실패율 30% -> 10% 미만 감소**, **IT 거버넌스 성숙도 Level 2->4 도약**이라는 측정 가능한 경영 가치를 창출한다.
> 3. **판단 포인트**: 중앙집중형 거버넌스 vs 분산형 페더레이션(Federated) 모델, **"Governance(거버넌스) ≠ Management(관리)"** 의 경계, **Quick-Win(단기성과) vs Strategic Initiative(장기투자)** 간의 자원배분 비율(통상 30:70), 그리고 **Run(운영)·Grow(성장)·Transform(혁신)** 의 IT 포트폴리오 밸런스(RGT 밸런스 스코어카드) 결정이 핵심 trade-off이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI, 클라우드, 빅데이터, IoT, 블록체인) 시대에 기업은 **연평균 4~6조 원의 IT 예산**(글로벌 500대 기업 기준, 전체 매출의 3.3~5.1%)을 운용한다. 그러나 McKinsey Global Institute(2023) 보고서에 따르면 **대규모 디지털 전환 프로젝트의 70%가 기대 ROI 미달** 또는 **실패**로 끝나며, Gartner(2024)는 **"CIO의 89%가 IT-Biz 정렬(Alignment) 부족을 최대 경영 리스크 1순위"** 로 지목했다. 이는 **"IT 부서가 기술을 잘 아는 것"** 과 **"IT가 경영 목표에 기여하는 것"** 이 다르다는 근본적 문제에서 비롯된다.

정보관리기술사 601번(전형적으로 IT 경영관리 분야 단답·서술형)은 **"기술적 사실"이 아닌 "경영 의사결정 정당화"** 를 평가한다. 즉, **PMBOK의 WBS, ITIL의 Incident Management 같은 절차적 지식**을 넘어, **"왜 이 프레임워크를 선택했는가?", "투자 우선순위를 어떻게 정했는가?", "거버넌스 리스크를 어떻게 측정했는가?"** 에 대한 **근거 기반 판단력**을 검증한다. 과거의 IT 운영 중심(Operation-centric) 사고에서 **가치 중심(Value-centric) 거버넌스** 패러다임으로의 전환이 이 시험의 본질이다.

```text
+----------------------------------------------------------------------------+
|         601번 시험이 요구하는 "IT 경영관리" 패러다임 진화                    |
+----------------------------------------------------------------------------+
|                                                                            |
|  [과거] 1980~2000        [전환기] 2000~2015         [현재] 2015~현재        |
|  +--------------+        +--------------+         +------------------+    |
|  | Data Center  |        | Process-Centric|       | Value-Centric   |    |
|  | Operations   |   ->    | Service Desk  |   ->    | Business Outcome |    |
|  |              |        | ITIL v2-v3    |         | COBIT 2019       |    |
|  | Cost Center  |        | PMBOK v4-v6   |         | PMBOK 7          |    |
|  |              |        | CMMI          |         | Lean Portfolio   |    |
|  +--------------+        +--------------+         +------------------+    |
|                                                                            |
|  - "IT는 비용"            - "IT는 서비스"             - "IT는 가치"        |
|  - 기술 중심 의사결정       - 프로세스 표준화           - 전략-투자-성과 정렬|
|  - CIO = 데이터센터장       - CIO = 서비스총괄          - CIO = Value Officer|
|                                                                            |
|  ※ 601번은 "왜 비용 -> 서비스 -> 가치로 변했는가"를 답하게 만든다           |
+----------------------------------------------------------------------------+
```

**시대의 요구**: IFRS 16(리스회계), ESG 공시(환경·사회·지배구조), EU AI Act, 개인정보보호법(한국, 2023 전면개정)에 따라 **IT 의사결정 과정 자체의 투명성·책임성·감사 가능성**이 법적 의무가 되었다. 이로 인해 **"거버넌스 -> 전략 -> 포트폴리오 -> 프로젝트 -> 운영 -> 가치측정"** 의 End-to-End 사슬을 이해하는 것이 601번의 핵심 출제 범위가 되었다.

- **📢 섹션 요약 비유**: **"요리사 자격증"이 아니라 "외식 경영 컨설턴트 자격증"** 입니다. 도마 위 칼질(기술)도 알아야 하지만, **메뉴 구성·원가 관리·고객 니즈 분석·시장 positioning**까지 다 알아야 1등급 식당을 운영할 수 있습니다. 601번은 후자를 묻는 시험입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 601번의 **5대 핵심 레이어 아키텍처**는 다음과 같다. 각각의 레이어는 **상위 -> 하위로 전략을 cascading**하고, **하위 -> 상위로 성과(performance)를 reporting**하는 양방향 피드백 구조다.

```text
+----------------------------------------------------------------------------+
|      IT 경영관리 5-Layer Reference Architecture (601번 마인드맵)           |
+----------------------------------------------------------------------------+
|                                                                            |
|  Layer 1: GOVERNANCE (거버넌스) -- COBIT 2019, ISO/IEC 38500, SOX         |
|  +----------------------------------------------------------------------+  |
|  | Evaluate -> Direct -> Monitor (EDM 5대 프로세스)                       |  |
|  | Board --- IT Steering Committee --- CIO --- Architecture Board       |  |
|  +----------------------------------------------------------------------+  |
|                              | Cascading (Top-Down)                       |
|                              v                                            |
|  Layer 2: STRATEGY (전략) -- IT Strategy Map, McFarlan Strategic Grid    |
|  +----------------------------------------------------------------------+  |
|  | Vision -> Mission -> CSF -> KPI -> Initiative (BMK: Business Motivation) |  |
|  | [Support] [Factory] [Turnaround] [Strategic] 4-Quadrant Positioning  |  |
|  +----------------------------------------------------------------------+  |
|                              | Cascading                                  |
|                              v                                            |
|  Layer 3: PORTFOLIO (포트폴리오) -- PfM, RGT Balance, BSC-IT              |
|  +----------------------------------------------------------------------+  |
|  | Run : Grow : Transform = 통상 60% : 20% : 20% (RGT 밸런스)          |  |
|  | Investment Categorization: ROI, NPV, IRR, Payback Period            |  |
|  +----------------------------------------------------------------------+  |
|                              |                                            |
|                              v                                            |
|  Layer 4: PROGRAM/PROJECT (수행) -- PMBOK 7, PRINCE2, MSP, SAFe           |
|  +----------------------------------------------------------------------+  |
|  | Charter -> Plan -> Execute -> Monitor -> Close (5 Process Groups)       |  |
|  | 8 Performance Domains: Stakeholder, Team, Planning, Delivery, etc.  |  |
|  +----------------------------------------------------------------------+  |
|                              |                                            |
|                              v                                            |
|  Layer 5: OPERATION/SERVICE (운영) -- ITIL 4 SVS, DevOps, SRE             |
|  +----------------------------------------------------------------------+  |
|  | Service Value Chain: Plan->Engage->Design->Obtain->Build->Transition     |  |
|  |                  ->Deliver->Support (34 Practices)                     |  |
|  +----------------------------------------------------------------------+  |
|                                                                            |
|  <-------- Feedback Loop (성과측정 -> 전략 재조정) --------                 |
|  BSC Scorecard: Financial / Customer / Internal Process / Learning&Growth |
+----------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (거버넌스 프레임워크)** | IT 의사결정의 책임·권한·보고 체계 정의 | **EDM(평가·지휘·모니터링) 5대 프로세스** + **Align, Plan, Organize(APO) 14개** + **Build, Acquire, Implement(BAI) 11개** + **Deliver, Service, Support(DSS) 6개** + **Monitor, Evaluate, Assess(MEA) 4개** = 총 40개 Governance/Management Objective. **40개 핵심 관리목표**(2019년 40개 -> 2019 패치 후 안정화). Design Factor 11개(기업전략, 목표, 위험, 문제 등) 기반으로 거버넌스 시스템 맞춤 설계. |
| **IT Strategy Map (전략 지도)** | IT 목표와 기업 목표의 시각적·인과적 연결 | Kaplan & Norton BSC 기반. **4 Perspectives**(재무/고객/내부프로세스/학습·성장)로 CSF(Critical Success Factor) -> KPI -> Initiative 3단계 cascading. 예) "고객 만족도 ^" -> "셀프서비스 채널 가용성 99.99%" -> "AWS Multi-AZ + Auto Scaling 투자 8억 원" |
| **McFarlan Strategic Grid** | IT의 전략적 위치(positioning) 진단 | **4-Quadrant**: Support(지원) / Factory(공장) / Turnaround(전환) / Strategic(전략). 자사 IT가 어느 사분면에 위치하는지 진단 후, 사분면별 거버넌스 모델 차별화(Strategic 사분면은 CEO 직보, Support 사분면은 비용최적화). |
| **IT Portfolio Management (PfM)** | 제한된 IT 예산의 최적 배분 | **RGT( Run-Grow-Transform ) Balance**: 운영안정 60% + 성장 20% + 혁신 20% (※ 산업별 상이, 핀테크는 R:G:T = 30:30:40). 투자평가기법: **NPV(순현재가치)**, **IRR(내부수익률)**, **Payback Period(투자회수기간)**, **BCR(비용편익비율)**. 위험-수익 Trade-off Matrix로 우선순위 도출. |
| **PMBOK 7th Edition** | 프로젝트 관리의 글로벌 표준 | **8대 Performance Domain**(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) + **12 Principles of Project Management**(Stewardship, Team, Systems Thinking, etc.). 기존 6판의 5 Process Groups + 10 Knowledge Areas는 **Predictive 지침**으로 강등. **Agile/Adaptive/Hybrid** 3개 개발접근법. |
| **ITIL 4 (서비스 운영)** | IT 서비스의 End-to-End 가치사슬 | **Service Value System (SVS)**: Opportunity/Demand -> Value -> Guiding Principles(7개) -> Governance -> Practices(34개) -> Continual Improvement. **Service Value Chain**: 6개 Activity(Plan, Engage, Design&Transition, Obtain/Build, Deliver&Support, Improve). **4 Dimension Model**: 조직/사람/정보/기술/파트너/가치사슬/외부요인. |
| **TOGAF 10 / ADM (아키텍처)** | EA(Enterprise Architecture) 수립 | **Architecture Development Method (ADM) Cycle**: Preliminary -> Vision -> Business Arch -> Data/App/Tech Arch -> Opportunities -> Migration Planning -> Implementation Governance -> Architecture Change Management -> Requirements Management. **TOGAF 10**(2022년) 추가: **Digital Business Model Canvas, Agile Architecture, Microservices 패턴**. |
| **Balanced Scorecard (BSC) for IT** | IT 성과 측정 | 4 Perspectives × IT 관점 KPI. 재무(예: IT 비용/매출 비율 ≤ 4%), 고객(예: 사용자 만족도 ≥ 4.2/5), 내부프로세스(예: SLA 준수율 ≥ 99.5%), 학습성장(예: 직원 역량 인증률). |

### 핵심 알고리즘·공식·판단 기준

- **Cobb-Douglas 기반 IT 투자함수**: $Y = A \cdot K^\alpha \cdot L^\beta$ (Y=IT 가치, K=자본, L=인력, α+β=1). α, β를 해당 산업 벤치마크로 설정.
- **COBIT 성숙도 측정**: **CMMI 5단계**(Initial->Managed->Defined->Quantitatively Managed->Optimizing)와 **ISO 15504 SPICE 6단계**를 혼용. 통상 0~5 점수 척도(Not Performed -> Optimized).
- **Risk = Likelihood × Impact**: 5×5 Matrix, 통상 Risk Score ≥ 15는 상시 모니터링, ≥ 20은 즉시 대응.
- **Real Options for IT Investment**: 불확실성이 큰 IT 투자(예: 신기술 도입)는 **"옵션 프리미엄"** 관점에서 평가. NPV가 음수라도 **Embedded Option(중단/확장/유예 권리)** 가치가 더 크면 GO 결정.

- **📢 섹션 요약 비유**: **5층 빌딩의 엘리베이터 시스템**과 같습니다. **1층 거버넌스(Board, 이사회)**가 누르고 **5층 운영(HelpDesk, 현장)**까지 내려와야 하며, 매 층마다 **"이 결정이 위층 목표에 부합하는가?"** 를 검증합니다. 엘리베이터가 한 층씩 끊기면 빌딩 전체가 무너집니다 — 601번은 **"각 층이 자기 역할만 알고 있다"** 는 함정 질문을 자주 냅니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 601번은 **유사 프레임워크 간의 미묘한 차이**를 정확히 구분하는지를 평가한다. 단순 암기가 아니라 **"우리 상황에 어떤 게 맞는가?"** 라는 선택 기준을 이해해야 한다.

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7 | ISO/IEC 38500 |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT **거버넌스** (의사결정) | IT **서비스 관리** (운영) | 프로젝트 **일·자·위험 관리** | IT **거버넌스 국제표준** |
| **적용 범위** | Enterprise-wide | Service Lifecycle | Project Boundary | Board/Top Management |
| **핵심 키워드** | Governance Objectives 40개, EDM 5개 | Service Value System, 34 Practices | 8 Performance Domain, 12 Principle | 6 Principles (Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) |
| **관점** | Top-Down (Board->CIO) | Bottom-Up (Service->Value) | Project-Centric | Top-Down, Principle-Based |
| **성과 측정** | Maturity Level 0~5 | Service KPI (SLA, MTTR) | Earned Value (SPI, CPI) | Principle 준수 여부 |
| **AGILE 적합성** | 중 (Design Factor로 Agility 반영) | 상 (Practices에 Agile
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 601 / 800

<- **이전**: [600. IT 경영 관리 핵심 토픽 600번 시험 요약](/studynote/12_it_management/05_security_compliance/600_it_management_core_topic_600_exam_summary/)
**다음**: [602. IT 경영 관리 핵심 토픽 602번 시험 요약](/studynote/12_it_management/05_security_compliance/602_it_management_core_topic_602_exam_summary/) ->

---
