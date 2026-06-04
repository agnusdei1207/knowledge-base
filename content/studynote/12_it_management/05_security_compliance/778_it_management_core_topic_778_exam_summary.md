---
title: "778. IT 경영 관리 핵심 토픽 778번 시험 요약 (IT Management Core Topic 778 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance, ITG)는 COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7th, Balanced Scorecard(BSC), TOGAF 10.0 등 6대 글로벌 프레임워크를 **"거버넌스-전략-포트폴리오-운영-리스크-평가"** 6계층으로 통합하여, 이사회(Board)의 IT 의사결정부터 전사 EA(Enterprise Architecture) 정합성까지 End-to-End로 정렬하는 메타관리 체계이다.
> 2. **가치**: IDC(2024)에 따르면 성숙한 IT 거버넌스 체계 도입 기업은 IT 투자 대비 ROI를 **평균 2.4배**, IT 프로젝트 실패율을 **35%->11%**, 감사 적발 비용을 **40%** 절감하며, McKinsey(2023)는 디지털 전환( DX ) 프로젝트의 Time-to-Value를 **18개월->7개월**로 단축시킨다고 보고한다.
> 3. **판단 포인트**: 핵심 trade-off는 (a) **"표준 프레임워크 채택 vs 조직成熟도 맞춤 Customization"** — COBIT 2019의 40개 Governance/Management Objectives 중 어디까지 적용할지, (b) **"집중형(Centralized) vs 연합형(Federated) IT 조직"** — Shadow IT 억제 vs 사업부 자율성, (c) **"Zero Trust 보안 vs 운영 편의성"** 의 세 축에서 기술사적 판단이 요구된다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사·컴퓨터시스템응용기술사 시험에서 **"778번"** 류로 분류되는 IT 경영 관리 토픽은, 단순한 IT 운영 관리를 넘어 **"IT가 어떻게 기업 가치(Enterprise Value)를 창출하는가"** 를 다루는 메타-관리 영역이다. 2020년자반정 이후 클라우드·AI·데이터 거버넌스 이슈가 폭증하면서, 정보시스템감사통제기준(통감원), 개인정보보호법(2024 개정), EU AI Act(2024), DORA( Digital Operational Resilience Act, 2025.01 발효) 등 글로벌 컴플라이언스가 동시다발적으로 강화됨에 따라, IT 경영 관리의 **"단일 진실 원천(Single Source of Truth, SSoT)"** 확보가 생존 전략이 되었다.

과거 IT 부서는 **"Cost Center(비용 센터)"** 로 인식되어 CAPEX(자본적 지출) 통제와 시스템 안정성만이 KPI였다. 그러나 4차 산업혁명( AI, BigData, Cloud, IoT, Blockchain, 5G/6G, Quantum) 시대에는 IT가 **"Value Driver(가동 동인)"** 로서, **"AI 도입으로 영업전환율 27% 개선"** , **"데이터 레이크하우스 구축으로 의사결정 속도 60% 단축"** 같은 정량적 가치를 입증해야 한다. 또한 **"Shadow IT"(사업부의 비공식 SaaS 도입)** 가 평균 기업 IT 예산의 **30~40%** 를 잠식한다는 Gartner(2023) 보고서는, IT 거버넌스 부재의 비용을 명백히 보여준다.

```text
+---------------------------------------------------------------------+
|           IT 경영 관리의 6계층 통합 프레임워크 (Top-Down)            |
+---------------------------------------------------------------------+
|                                                                     |
|   ① 이사회(Board) / C-Level                                         |
|      |  ISO 38500 6 원칙: 책임·전략·취득·성과·규율·인간·배치        |
|      |  +- IT 전략위원회(Steering Committee)                        |
|      |  +- CIO / CDO / CISO / CRO (4-CIO 모델)                     |
|      v                                                              |
|   ② 거버넌스 프레임워크 (Governance Layer)                          |
|      |  COBIT 2019 -- EDM(05) -- APO/BAI/DSS/MEA (40 Objectives)   |
|      |  -- 연계: ISO 27001(ISMS), ISO 20000(ITSM), ISO 22301(BCM)  |
|      v                                                              |
|   ③ 전략 및 포트폴리오 (Strategy & Portfolio)                       |
|      |  IT Strategy Map(BSC 4관점) -> IT Portfolio 분류(투자·운영· |
|      |  혁신·위험) -> Prioritization(NPV, IRR, Risk-Adjusted ROI)   |
|      v                                                              |
|   ④ 아키텍처 및 운영 (Architecture & Operations)                    |
|      |  TOGAF 10 ADM -- EA Repository -- SOA/Microservices --      |
|      |  -- ITSM(ITIL 4 Service Value System: Plan-Engage-Design-   |
|      |      Transition-Obtain/Build-Deliver-Support/Improve)        |
|      v                                                              |
|   ⑤ 리스크 및 컴플라이언스 (Risk & Compliance)                      |
|      |  ISO 31000 리스크관리 -- 3 Lines of Defense Model --         |
|      |  -- 통감원 정보시스템감사통제, PIPC, NIST CSF 2.0,        |
|      |      DORA, EU AI Act, GDPR, ESG-ISMS                        |
|      v                                                              |
|   ⑥ 측정 및 지속적 개선 (Measure & Improve)                         |
|         KPI/KRI/CSF -> BSC Scorecard -> MEA Audits -> PDCA/PDSA       |
+---------------------------------------------------------------------+
```

**왜 필요한가? — 구(舊) 패러다임 vs 신(新) 패러다임**

| 구분 | 구(舊) IT 관리(1990~2010) | 신(新) IT 경영 관리(2020~) |
|:---|:---|:---|
| 조직 위치 | CIO = "전자계산실장" | CIO = Board Member, CDO·CISO·CAIO 협력 |
| KPI | 가용률(Uptime 99.9%), 예산 준수율 | NPS, Time-to-Market, Innovation Pipeline Value |
| 투자 기준 | TCO(총소유비용) 최소화 | NPV + Risk-Adjusted ROI + ESG 영향도 |
| 아키텍처 | 모놀리식 On-Premise | 하이브리드 멀티클라우드 (AWS+Azure+GCP) |
| 리스크 대응 | BCP(위기관리) | Zero Trust + Resilience + AI Risk Management |
| 컴플라이언스 | 정보통신망법, ISMS-P | + DORA, EU AI Act, ISO 42001(AIMS), PIPC 가명정보 |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"오케스트라의 지휘자"** 와 같습니다. 바이올린(IT 인프라), 첼로(데이터), 트럼펫(AI 서비스), 팀파니(보안) 등 다양한 악기(부서)가 각자 멋진 연주를 하지만, 지휘자(거버넌스)가 없으면 불협화음만 나옵니다. ISO 38500은 "악보의 6가지 원칙"이고, COBIT은 "연주 매뉴얼"이며, ITIL은 "악기 조율법", BSC는 "객석의 청취 평가표"라고 할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 거버넌스 핵심 프레임워크의 메타-구조

```text
+----------------------------------------------------------------------+
|        IT 거버넌스 4대 글로벌 프레임워크의 Scope 매핑                  |
+----------------------------------------------------------------------+
|                                                                      |
|    +--------------+    ISO/IEC 38500:2024                           |
|    |   BOARD      |<--- "6 Principles" for Directors                  |
|    |   LEVEL      |    (Responsibility, Strategy, Acquisition,      |
|    +------+-------+     Performance, Conformance, Human)            |
|           |                                                        |
|           v  +----------------------------------------------+       |
|  GOVERN     |  COBIT 2019 - 40 Governance & Management Obj. |       |
|  ANCE ------>|  EDM(5) | APO(14) | BAI(11) | DSS(6) | MEA(4)|       |
|             +--+---------------+---------------+--------------+       |
|                |               |               |                      |
|                v               v               v                      |
|         +----------+    +----------+    +--------------+            |
|         |PRACTICE  |    |SERVICE   |    |  PROJECT     |            |
|         |Layer     |    |Mgmt Layer|    |  Mgmt Layer  |            |
|         |(Control) |    |(Delivery)|    |  (Change)    |            |
|         +----+-----+    +----+-----+    +------+-------+            |
|              |               |                  |                    |
|              v               v                  v                    |
|        COBIT 2019      ITIL 4 (SVS)         PMBOK 7th Ed.          |
|        Control Obj.    34 Practices          12 Principles          |
|        + NIST CSF 2.0 + ISO 27001:2022      + PRINCE2 7             |
|                                                                      |
|   -----------------  Cross-cutting Concerns  -----------------       |
|        EA(TOGAF 10.0)  |  Risk(ISO 31000:2018) | BCM(ISO 22301)   |
|        Data(DAMA-DMBOK3)|  AI(ISO/IEC 42001 AIMS)| ESG(ISO 14097) |
+----------------------------------------------------------------------+
```

### 2) 구성 요소별 상세 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **① COBIT 2019** (Control Objectives for Information and Related Technologies) | IT 거버넌스/관리의 **End-to-End 목표 체계** | ISACA(2024)가 전면 개정한 버전으로, 5개 **EDM**(Evaluate-Direct-Monitor) + 35개 관리 목표. 핵심은 **"Governance System Design Factors" 11개**(전략, 목표, 리스크, 위협, 컴플라이언스, IT 역할, IT 채택 방식, 기술 채택 전략, 조직 규모, 자원 제약)를 통해 **40개 목표를 가중치 기반 우선순위화**한다. |
| **② ISO/IEC 38500:2024** | 이사진(Directors) 레벨의 **거버넌스 6원칙** | 가장 최신 글로벌 표준으로, **"Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior"** 6원칙을 제시. **PDCA 모델(Ratify->Prepare->Implement->Operate->Review->Monitor)** 6단계 Govern-Apply-Evaluate 사이클이 있다. |
| **③ ITIL 4** (Information Technology Infrastructure Library) | IT 서비스의 **가치 공(Value Co-Creation)** 운영 프레임워크 | Axelos(2024, PeopleCert 인수) 발행. **SVS(Service Value System)** = Opportunity/Demand->Value->SVC(Service Value Chain: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve). **34개 Best Practice**, 4개 Dimension(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes). |
| **④ BSC for IT** (IT Balanced Scorecard) | IT 성과 측정의 **4관점 전략 맵** | Kaplan & Norton의 BSC를 IT에 적용. **(1) Financial** (TCO 절감, ROI), **(2) Customer**(사용자 만족도 NPS), **(3) Internal Process**(서비스 가용률 99.95%), **(4) Learning & Growth**(IT 인력 역량, 디지털 전환 역량). **Strategy Map**으로 인과관계 도식화. |
| **⑤ TOGAF 10.0** (2024년 4월 발표) | **EA(Enterprise Architecture) 수립 방법론** | **ADM(Architecture Development Method) 10단계**: Preliminary->A: Architecture Vision->B: Business Architecture->C: Information Systems->D: Technology->E: Opportunities & Solutions->F: Migration Planning->G: Implementation Governance->H: Architecture Change Management->Requirements Management(전 단계). **ADM Cycle** + **ADM Cycle Iteration**, **Architecture Repository**(ABB, SBB, ARB, Governance Log) 운영. |
| **⑥ IT Portfolio Management** | IT 투자 자원의 **최적 배분** | Gartner 분류: **(1) Run the Business** (70~80%, 운영·유지), **(2) Grow the Business** (10~20%, 혁신·신규), **(3) Transform the Business** (5~10%, 패러다임 전환). **Bubble Chart**(Value vs Risk vs Cost) 기반 시각적 우선순위화. |
| **⑦ IT Risk Management** (ISO 31000:2018) | IT 리스크의 **식별·평가·대응·모니터링** | **3 Lines of Defense Model**: 1st Line(사업부 자체 통제), 2nd Line(리스크·컴플라이언스·CISO), 3rd Line(내부감사). **KRI(Key Risk Indicator)** + **Risk Appetite/Tolerance** 임계치 기반 조기경보. |
| **⑧ IT 투자 경제성 평가** | 정량적 의사결정 근거 | **NPV**(순현재가치), **IRR**(내부수익률), **Payback Period**, **TCO**(총소유비용=직접+간접+Hidden), **VOI**(Value on Investment), **Risk-Adjusted ROI**(= ROI × (1-Risk Factor)). EVA(Economic Value Added) = NOPAT - WACC×투하자본. |

### 3) 핵심 알고리즘/수식/원리

- **COBIT 2019 우선순위 가중치 함수**:
  `Priority_i = Σ (w_j × GF_i,j)` where `GF ∈ {Strategic, Risk, Threat, Compliance, IT Role, ...}`
  *이때 w_j는 Design Factor별 가중치, GF_i,j는 목표 i의 Factor j 점수 (1~5).*

- **ITIL 4 가치 공동창출(VCC) 방정식**:
  `Value = (Utility + Warranty) × (P × I ×
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 778 / 800

<- **이전**: [777. IT 경영 관리 핵심 토픽 777번 시험 요약](/studynote/12_it_management/05_security_compliance/777_it_management_core_topic_777_exam_summary/)
**다음**: [779. IT 경영 관리 핵심 토픽 779번 시험 요약](/studynote/12_it_management/05_security_compliance/779_it_management_core_topic_779_exam_summary/) ->

---
