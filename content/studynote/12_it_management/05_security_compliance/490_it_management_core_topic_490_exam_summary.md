---
title: "490. IT 경영 관리 핵심 토픽 490번 시험 요약 (IT Management Core Topic 490 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019, ISO/IEC 38500, ITIL 4 등 국제 표준 프레임워크를 기반으로, IT 거버넌스-전략-포트폴리오-위험-성과의 5대 영역을 통합적으로 운용하여 기업의 디지털 경쟁력을 극대화하는 경영 체계이다. 특히 Balanced Scorecard(BSC)와 IT BSC를 연계하여 전략적 목표(Strategic Objective)와 핵심 성과지표(KPI)를 4관점(재무/고객/내부프로세스/학습성장)으로 정량 측정한다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 IT 투자 대비 ROI 25~40% 향상(McKinsey 2023 보고서), 정보화 사업 실패율 60%에서 25%로 감소(Standish Group CHAOS Report 2023 기준), 그리고 ISO 38500 인증 기업은 평균 18%의 운영비용 절감 및 의사결정 속도 3.2배 향상을 달성한다.
> 3. **판단 포인트**: 중앙집중식(Centralized) vs 분산형(Decentralized, DevOps 페덱스 모델) IT 조직 구조 선택, CapEx 중심의 전통적 IT 투자 대비 OpEx 기반 Cloud FinOps 모델 전환 여부, 그리고 RICE/WSJF/PI Planning 등 애자일-포트폴리오 관리 방법론 채택 시 To-Be 거버넌스 모델의 성숙도(Gartner 5단계: Awareness->Commitment->Competence->Excellence->Leadership) 진단이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

정보기술은 더 이상 단순 비용센터(Cost Center)가 아닌 **전략적 가치 창출의 핵심 엔진**으로 격상되었다. 4차 산업혁명(AI, IoT, Blockchain, Cloud, Big Data) 시대를 맞아 기업 CIO의 역할은 IT 운영자(IT Operator)에서 **디지털 비즈니스 설계자(Digital Business Architect)**로 진화하고 있으며, 가트너(Gartner)는 2026년까지 전 세계 기업의 75%가 디지털 트랜스포메이션(DX) 실패 위험에 노출될 것으로 전망했다(Gartner Top Strategic Technology Trends 2024). 이러한 패러다임 전환 속에서 **IT 경영관리(IT Management)**는 단순한 시스템 운영이 아닌, **거버넌스-전략-실행-측정-개선**의 연속적 사이클을 통해 IT 자산을 비즈니스 성과로 전환하는 종합 관리 체계의 정착이 절실하다.

```text
+---------------------------------------------------------------------+
|              IT 경영관리 5대 도메인 통합 프레임워크                    |
+---------------------------------------------------------------------+
|                                                                     |
|   +--------------+    +--------------+    +--------------+         |
|   | 1. 거버넌스  |◄--►|  2. 전략수립 |◄--►| 3. 포트폴리오 |         |
|   |  Governance  |    |  Strategy    |    |  Portfolio   |         |
|   | (COBIT 2019) |    | (TOWS/BMC)   |    | (SAFe Lean)  |         |
|   +------+-------+    +------+-------+    +------+-------+         |
|          |                   |                   |                 |
|          v                   v                   v                 |
|   +------------------------------------------------------+         |
|   |          4. IT 투자·예산·성과 통합관리 (IT BSC)        |         |
|   +------------------------+-----------------------------+         |
|                            |                                       |
|          +-----------------+-----------------+                     |
|          v                 v                 v                     |
|   +--------------+  +--------------+  +--------------+            |
|   | 5. 위험관리  |  | 6. 서비스운용 |  | 7. 컴플라이언스|           |
|   |  (ISO 27005) |  |  (ITIL 4 SVS)|  |  (GDPR/PIPA) |            |
|   +--------------+  +--------------+  +--------------+            |
|                            |                                       |
|                            v                                       |
|              +------------------------------+                       |
|              |  기업가치 극대화 & ROIC 향상  |                       |
|              +------------------------------+                       |
+---------------------------------------------------------------------+
```

기존 IT 관리는 **기술 중심(Technology-Driven)**의 **프로젝트 단위 관리(Project-based Management)**로, 정보화 사업별 예산 투입 대비 정성적 효과(Qualitative Benefits)에만 의존했다. 그러나 **PMBOK 7th Edition(2021)**의 프로젝트 성과 도메인(Project Performance Domains)과 **PRINCE2 7(2023)**의 7대 테마(Themes) 도입, 그리고 **SAFe 6.0(Scaled Agile Framework)**의 Lean Portfolio Management(LPM) 개념 확산으로, IT는 **가치 흐름(Value Stream)** 단위의 지속적 전달 체계로 재편되고 있다. 이러한 변화의 핵심은 **"프로젝트가 끝나면 끝"이 아니라, 포트폴리오-프로그램-프로젝트-제품(Product)의 4계층 구조에서 각 단계별 KPI와 OKR(Objectives and Key Results)을 연결하여 비즈니스 임팩트를 연속 측정하는 것"**이다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라 지휘자**와 같다. 첼리스트(개발팀), 바이올리니스트(운영팀), 트럼펫 연주자(영업/마케팅) 등 각기 다른 악기(IT 시스템)를 연주하는 악수들을 **하나의 악보(전략·거버넌스)**로 통합하여, **시너지 하모니(기업가치)**를 만들어내는 것이 본질이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 국제 표준화 기구(ISO), ISACA, AXELOS, Scaled Agile Inc. 등 글로벌 기관에서 제정한 **거버넌스-관리-실행 3계층 모델(Governance-Management-Operations 3-Layer Model)**로 통합된다. 최상위 **거버넌스 계층**은 이사회-경영진의 의사결정 구조(예: ISO 38500의 Evaluate-Direct-Monitor 사이클)와 COBIT 2019의 40개 관리목표(Management Objective)를, 중위 **관리 계층**은 전략 맵(Strategy Map)과 IT 포트폴리오 관리, 그리고 최하위 **실행 계층**은 ITIL 4의 34개 서비스 관리 실무(SMP)와 DevOps Value Stream Mapping을 통해 운영된다.

```text
+--------------------------------------------------------------------+
|         IT 경영관리 참조모델 통합 아키텍처 (Reference Model)       |
+--------------------------------------------------------------------+
|                                                                    |
|  [Tier 1] 거버넌스 계층 (ISO/IEC 38500 + COBIT 2019)              |
|  +--------------------------------------------------------+        |
|  |  ISO 38500 E-D-M Cycle                                 |        |
|  |  +----------+  +----------+  +----------+             |        |
|  |  | Evaluate |-►| Direct   |-►| Monitor  |-+           |        |
|  |  | (평가)   |  | (지시)   |  | (모니터) | |           |        |
|  |  +----------+  +----------+  +----------+ |           |        |
|  |       ^                                  |           |        |
|  |       +----------------------------------+           |        |
|  +--------------------------------------------------------+        |
|                              |                                     |
|                              v                                     |
|  [Tier 2] 관리 계층 (전략·포트폴리오·예산)                          |
|  +--------------------------------------------------------+        |
|  |  Balanced Scorecard (BSC) + IT BSC                    |        |
|  |  +---------+---------+----------+----------+          |        |
|  |  | 재무    | 고객    | 내부프로 | 학습·성장|          |        |
|  |  | (Finan.)| (Custom)| (Intern.)|(L&G)     |          |        |
|  |  | ROI/ROIC| NPS/CSAT| MTTR/MTBF| 직원만족 |          |        |
|  |  +---------+---------+----------+----------+          |        |
|  +--------------------------------------------------------+        |
|                              |                                     |
|                              v                                     |
|  [Tier 3] 실행 계층 (ITIL 4 SVS + SAFe LPM + DevOps)              |
|  +--------------------------------------------------------+        |
|  |  Service Value System (SVS)                            |        |
|  |  Opportunity/Demand --► Value --► Outcome              |        |
|  |       ^                          |                     |        |
|  |       +-------- Feedback --------+                     |        |
|  |                                                        |        |
|  |  Practices: 34개 (예: Incident Mgmt, Change Enablement)|        |
|  +--------------------------------------------------------+        |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (Control Objectives for Information and Related Technologies) | IT 거버넌스 목표체계 | 40개의 관리목표(Management Objective)를 5개 도메인(EDM: Evaluate-Direct-Monitor / APO: Align-Plan-Organize / BAI: Build-Acquire-Implement / DSS: Deliver-Service-Support / MEA: Monitor-Evaluate-Assess)으로 분류. **Cascade Goals(목표 연쇄)**를 통해 Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Goals로 분해 |
| **ITIL 4** (Information Technology Infrastructure Library v4) | IT 서비스 운영·관리 | **Service Value System(SVS)**의 7가지 구성요소(Guiding Principles, Governance, Service Value Chain, Practices, Continual Improvement, Technology, People&Culture). 34개 Practice를 General/Service/Technical Management로 구분하며, **Four Dimensions Model**(Organizations, People, Information, Technology, Partners, Suppliers, Value Streams - 총 7요소)을 통한 Holistic View 제공 |
| **ISO/IEC 38500:2015** | 이사회 수준 IT 거버넌스 | **6가지 원칙**(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) 기반의 **E-D-M(Evaluate-Direct-Monitor) 3단계 사이클**. 이사회(Board)가 IT 의사결정에 대해 최종 책임을 지며, **Governance Framework Maturity Model(GFMM)**로 5단계 성숙도 측정 |
| **Balanced Scorecard + IT BSC** | 전략-성과 연계 측정 | Norton & Kaplan(1992)의 4관점(Financial/Customer/Internal Process/Learning&Growth) 프레임워크를 IT에 적용. **Strategy Map**으로 인과관계(Cause-Effect Chain) 시각화, **KPI Tree**로 Strategic Objective -> Measure -> Target -> Initiative 4단계 분해 |
| **SAFe 6.0 + Lean Portfolio Management** | 애자일 포트폴리오 관리 | **Epic->Capability->Feature->Story->Task**의 5단계 계층, **WSJF(Weighted Shortest Job First)** = (Business Value + Time Criticality + Risk Reduction) / Job Duration, **PI(Program Increment) Planning**으로 8~12주 단위의 Agile Release Train(ART) 운영 |

**핵심 원리의 정량적 파라미터**:
- **IT ROI 계산식**: ROI(%) = (총 편익 - 총 비용) / 총 비용 × 100. 여기서 편익은 Tangible Benefits(예: 운영비 절감 2.4억원/年) + Intangible Benefits(예: 고객 만족도 15% 향상, 가중치 0.7 적용)
- **TCO(Total Cost of Ownership)**: TCO = 직접비용(HW/SW/License) + 간접비용(교육/다운타임/보안사고) + 기회비용. Gartner(2023) 기준 평균 5년 TCO 중 **간접비가 60~70%** 차지
- **NPV(순현재가치)**: NPV = Σ[CF_t / (1+r)^t] - I_0, IT 사업의 할인율(r) 통상 8~12% 적용, Payback Period 통상 3~5년 이내가 의사결정 기준
- **IT 성숙도 모델**: COBIT 2019의 **Performance Management**는 Process Capability(0~5 레벨: Incomplete->Performed->Managed->Established->Predictable->Optimizing)와 Focus Area Maturity(1~5 레벨) 2축으로 측정

- **📢 섹션 요약 비유**: 위의 3계층 아키텍처는 **정부의 입법부-행정부-사법부**처럼 작동한다. 이사회(입법부)가 거버넌스 원칙을 제정하면, CIO와 PMO(행정부)가 전략과 포트폴리오를 실행하고, 현장 운영팀(사법부)이 ITIL Practice를 통해 서비스를 제공한다. 세 계층 간 **체크앤밸런스(Check & Balance)**가 균형을 이룰 때 비로소 IT가 기업가치를 창출한다.

---

## Ⅲ. 비교 및 연결

IT 경영관리의 핵심 표준들은 **상호보완적 관계**에 있다. COBIT은 **"무엇을(What)"** 관리할지를 정의하고, ITIL 4는 **"어떻게(How)"** 서비스를 운영할지를, ISO 38500는 **"왜(Why) 그리고 누가(Who)"** 의사결정할지를, PMBOK/PRINCE2는 **"프로젝트를 어떻게(How) 전달"**할지를 각각 규정한다. 기술사 시험에서는 각 프레임워크의 **차별적 가치와 통합 시너지**를 명확히 설명할 수 있어야 한다.

| 구분 | COBIT 2019 | ITIL 4 | ISO/IEC 38500 | PMBOK 7 / PRINCE2 7 |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스 및 관리 목표체계 | IT 서비스 관리 운영체계 | 이사회 수준 거버넌스 원칙 | 프로젝트/프로그램 관리 |
| **대상 범위** | Enterprise 전체 IT | IT 서비스 전달·지원 | 거버넌스 의사결정자 | 일시적 프로젝트 |
| **구조** | 40개 관리목표 / 5개 도메인 | 34개 Practice / 7요소 SVS | 6원칙 / E-D-M 3단계 | 8대 성과도메인 / 5단계 프로세스 그룹(PMBOK 6) / 7대 테마(PRINCE2) |
| **측정 지표** | Process Capability (0~5), Lag/Lead Indicator | SLA, Service Availability, MTTR/MTBF | Governance Maturity (5단계) | SPI, CPI,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 490 / 800

<- **이전**: [489. IT 경영 관리 핵심 토픽 489번 시험 요약](/studynote/12_it_management/05_security_compliance/489_it_management_core_topic_489_exam_summary/)
**다음**: [491. IT 경영 관리 핵심 토픽 491번 시험 요약](/studynote/12_it_management/05_security_compliance/491_it_management_core_topic_491_exam_summary/) ->

---
