---
title: "IT Management Core Topic 747 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance, ITG)는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로, 기업의 IT 전략·아키텍처·서비스·리스크·자원을 End-to-End로 정렬(Value Alignment)하여 Stakeholder Value를 극대화하는 통합 관리 체계이다.
> 2. **가치**: McKinsey 보고 기준 체계적 IT 거버넌스 도입 조직은 TCO 20~30% 절감, Time-to-Market 40% 단축, 프로젝트 성공률 35%->75% 향상, 디지털 전환 ROI 2.3배 개선 효과를 거둘 수 있으며, ISO/IEC 38500 인증 시 입찰 가산점 5~15% 확보가 가능하다.
> 3. **판단 포인트**: 중앙집중(Centralized) vs 분산(Federated) 거버넌스 모델 선택, COBIT 2019의 40 Governance/Management Objectives와 조직 7대 구성요인(Principles, Policies, Frameworks)의 맞춤화 정도, Agile/DevOps 환경에서의 거버넌스 경량화(Governee-first) 수준이 핵심 trade-off이다.

---

## Ⅰ. 개요 및 필요성

21세기 디지털 전환(DX) 환경에서 IT는 단순 비용센터(Cost Center)에서 가치 창출의 핵심 동력(Value Driver)으로 격상되었으며, Gartner(2024) 보고에 따르면 글로벌 IT 지출은 5.1조 USD에 달하고 CIO의 78%가 "IT 성과의 사업적 가치 입증"을 최대 과제로 선정하고 있다. 그러나 McKinsey 조사에서 DX 프로젝트의 70%가 성과를 거두지 못하고 있으며, 그 핵심 원인은 전략-아키텍처-운영-리스크 사슬의 단절(Disconnected Value Chain)에 있다. 기술사 시험에서 747번 토픽은 바로 이 **"전략적 정렬(Strategic Alignment) + 가치 실현(Value Realization) + 리스크 최적화(Risk Optimization) + 자원 관리(Resource Management)" 4대 축**을 통합적으로 이해하고 설계할 수 있는 역량을 평가한다.

```text
+------------------------------------------------------------------------------+
|                    IT 경영 관리 4대 도메인 통합 프레임워크                     |
+------------------------------------------------------------------------------+
|                                                                              |
|   +-----------------+         +-----------------+                          |
|   | ① 전략/거버넌스 |◄-------►|  ② 아키텍처/표준 |                          |
|   |  (Strategy &    |         |   (Enterprise   |                          |
|   |   Governance)   |         |   Architecture) |                          |
|   |  • COBIT 2019   |         |  • TOGAF 10     |                          |
|   |  • ISO 38500    |         |  • Zachman 3.0  |                          |
|   |  • IT Strategy  |         |  • FEAF/DODAF   |                          |
|   +--------+--------+         +--------+--------+                          |
|            |                           |                                    |
|            |  +---------------------+  |                                    |
|            +-►|   ③ 서비스/운영    |◄-+                                    |
|               |  (Service & Ops)   |                                       |
|               |  • ITIL 4         |                                       |
|               |  • SIAM/VeriSM    |                                       |
|               |  • DevOps/SRE    |                                       |
|               +---------+--------+                                       |
|                         |                                                  |
|            +------------v------------+                                    |
|            | ④ 리스크/컴플라이언스   |                                    |
|            |  (Risk & Compliance)    |                                    |
|            |  • ISO 27001/27005      |                                    |
|            |  • NIST CSF 2.0         |                                    |
|            |  • GDPR/PIPA            |                                    |
|            +-------------------------+                                    |
|                                                                              |
|   +--------------------------------------------------------------------+   |
|   | 🎯 상위 피드백 루프: Strategy -> Architecture -> Service -> Risk     |   |
|   |    -> 측정(BSC/KPI) -> 개선(PDCA/OKR) -> Strategy 순환 구조          |   |
|   +--------------------------------------------------------------------+   |
+------------------------------------------------------------------------------+
```

**전통적 IT 관리 vs 현대 IT 경영 관리 비교**:
- **전통적(2000년대 이전)**: IT는 백오피스 지원 기능, SLI/SLO 개념 부재, CAPEX 중심, 프로젝트별 관리(Waterfall), 기술 중심 의사결정
- **현대(2020년대)**: IT는 사업 핵심, NOC/Service Desk + AI Ops 통합, OPEX+Subscription, 제품 중심 관리(Agile/SRE), 가치 중심 의사결정, ESG/Digital Ethics 포함

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'통합 차량 제어 시스템(Vehicle Dynamics Control, VDC)'** 과 같다. 엔진(전략), 변속기(아키텍처), 브레이크(리스크), 내비게이션(서비스) 4개 시스템이 실시간으로 데이터를 교환하며, 운전자가 의도한 목적지(사업 목표)에 안전하고 효율적으로 도달하도록 통합 제어하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. COBIT 2019 거버넌스 시스템 설계 (40 Objectives 기반)

COBIT 2019는 **거버넌 목적(Governance Objectives) 5개 + 관리 목적(Management Objectives) 35개 = 총 40개**로 구성되며, 각 목적은 **Process Component**(구성요소)와 **관련 Goal Cascade**(목표 연쇄)를 통해 기업 목표와 연결된다. 핵심은 **EDM( Evaluate, Direct, Monitor )** 사이클로, 이사회/이사회위가 IT 성과·리스크·자원 활용을 지속 평가-지시-감독하는 구조다.

```text
+-----------------------------------------------------------------------+
|                    COBIT 2019 거버넌스 시스템 토폴로지                  |
+-----------------------------------------------------------------------+
|                                                                       |
|   +--------------------------------------------------------------+  |
|   |         Enterprise Goals (13개, 사업 목표 연쇄)              |  |
|   |   EG01 포트폴리오 혁신     EG05 고객 만족                    |  |
|   |   EG02 리스크 관리          EG08 내부 운영 최적화            |  |
|   |   EG13 디지털 제품/서비스  ... 등                            |  |
|   +------------------------+-------------------------------------+  |
|                            | Alignment Goals(13개) 매핑              |
|                            v                                         |
|   +--------------------------------------------------------------+  |
|   |  EDM(거버넌스) 5개 + 관리(Management) 35개                    |  |
|   |  +------+ +------+ +------+ +------+ +------+               |  |
|   |  |EDM01 | |EDM02| |EDM03| |EDM04| |EDM05|   <- 거버넌스     |  |
|   |  |평가/ | |리스크| |자원 | |문화 | |투명 |      영역       |  |
|   |  |지시  | |최적 | |최적 | |정렬 | |보고 |                  |  |
|   |  +------+ +------+ +------+ +------+ +------+               |  |
|   |  +------+ +------+ +------+ +------+ ... +------+           |  |
|   |  |APO   | |APO  | |BAI  | |DSS  |     |MEA  |  <- 관리     |  |
|   |  |Align | |Build| |Deli | |Supp |     |Moni |     영역    |  |
|   |  |Plan  | |Orga | |Acq  | |Serv |     |Eval |             |  |
|   |  |Orga  | |nize| |Impl | |vice |     |u    |             |  |
|   |  +------+ +------+ +------+ +------+     +------+           |  |
|   +------------------------+-------------------------------------+  |
|                            | Component: 7개 요소                   |
|                            v                                         |
|   +--------------------------------------------------------------+  |
|   | Process Components (구성요소 7종)                             |  |
|   |  ① Process Practices(활동, RACI)                             |  |
|   |  ② Process Goals(목표, 메트릭)                               |  |
|   |  ③ Life Cycle Models(계획/설계/운영/폐기)                    |  |
|   |  ④ Good Practices(모범사례)                                  |  |
|   |  ⑤ Information Flow(정보 흐름, 입력/출력)                    |  |
|   |  ⑥ People, Skills & Competencies(역할)                      |  |
|   |  ⑦ Policies & Procedures(정책/절차)                          |  |
|   +------------------------+-------------------------------------+  |
|                            v                                         |
|   +--------------------------------------------------------------+  |
|   | 7 Components of Governance System                            |  |
|   |  (1) Principles  (2) Processes  (3) Organizational Structures |  |
|   |  (4) Information Flows (5) People & Skills (6) Culture        |  |
|   |  (7) Services, Infrastructure & Applications                 |  |
|   +--------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

### B. ITIL 4 Service Value System (SVS)

ITIL 4는 **Service Value System(SVS)** 을 통해 34개 Practice(실무)를 14개 영역(Value Chain Activity)으로 통합 운영한다. 핵심은 **Service Value Chain(SVC)** 의 6단계 Plan->Engage->Design & Transition->Obtain/Build->Deliver & Support->Improve 흐름이며, **Guiding Principles 7개**(Focus on value, Start where you are, Progress iteratively, etc.)가 모든 의사결정의 판단 기준이 된다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Governance Body(COBIT EDM)** | 전략 지침, 리스크 한계, 자원 배분 결정 | ISO/IEC 38500 6원칙(DH ARRRR: Duty, Accountability, Responsibility, Reward, Risk, Resource) 적용, 이사회 -> IT Steering Committee -> PMO 계층적 의사결정 구조 |
| **Strategy & Portfolio Layer** | IT 투자 포트폴리오 최적화, NPV/IRR/Payback 분석 | BCG/Gartner Magic Quadrant 분석, Stage-Gate(Discover->Scope->Build->Test->Launch) 게이트 관리, Run/Grow/Transform 70-20-10 자원 배분 원칙 |
| **Enterprise Architecture** | 비즈니스-데이터-애플리케이션-기술 정렬 | TOGAF ADM(Architecture Development Method) 8단계 Phase B,C,D(비즈니스/데이터/애플리케이션/기술), Zachman 6x6 매트릭스, Architecture Repository(ABD/ABM/ABB) |
| **Service Management Plane** | SLA/SLO/SLI 기반 IT 서비스 운영 | ITIL 4 Service Value Chain 6 Activity, Incident->Problem->Change->Release 파이프라인, AIOps + Observability(Logs/Metrics/Traces 통합) |
| **Risk & Security Layer** | 정보 보호 및 컴플라이언스 통제 | ISO 27001:2022 Annex A 93 통제 항목, ISO 31000 Risk Treatment(회피/전가/완화/수용), 3 Lines of Defense 모델(1LoD 운영·2LoD 리스크·3LoD 내부감사) |
| **Performance & Value Layer** | 정량적 가치 측정 및 보고 | IT BSC 4관점(재무/내부/학습/고객), KPI Tree(CSF->KPI->KGI), OKR(Objective & Key Results), Balanced Scorecard Cascade |

### C. 핵심 알고리즘/모델 - 거버넌스 성숙도 측정 공식

거버넌스 수준은 **CMMI 5단계**(Initial->Managed->Defined->Quantitatively Managed->Optimizing) 또는 **COBIT Maturity Model(NBR 5단계: Incomplete->Initial->Managed->Defined->Quantitative->Optimized)** 로 측정하며, 다음 공식으로 정량화한다:

```
Governance Maturity Index (GMI) = Σ(Wi × Pi) / ΣWi
  Wi = i번째 Process의 중요도 가중치(0~1)
  Pi = i번째 Process의 성숙도 점수(0~5, COBIT PAM 기반)

Capability Level(0~5) 기준:
  Level 0: Incomplete(138 미만)
  Level 1: Initial/Performed(138~164점, 27.5% 달성)
  Level 2: Managed(165~220점, 33%)
  Level 3: Defined(221~275점, 44%)
  Level 4: Quantitative(276~331점, 55%)
  Level 5: Optimized(332~400점, 66%+)

ROI 계산 (IT 투자 가치 입증):
  NPV = Σ(CFt / (1+r)^t) - CAPEX
  TCO = Direct Cost(HW/SW/Lic) + Indirect Cost(운영/다운로스) + Hidden Cost(학습/전환)
  Payback Period = Initial Investment / Annual Cash Flow
```

- **📢 섹션 요약 비유**: COBIT 2019의 40 Objectives는 마치 **'비행기의 40개 계기판'** 과 같다. 어느 하나가 적색등(Red)이라도 비행이 위험하지만, 모든 계기판이 적색(0~1 Level)이면 이륙 자체가 불가능하고, 모두 녹색(5 Level)이면 자동착륙까지 가능한 안정 상태인 셈이다.

---

## Ⅲ. 비교 및 연결

### A. 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI 2.0** |
|:---|:---|:---|:---|:---|
| **목적/범위** | IT 거버넌스/관리 통합 프레임워크 | IT 서비스 관리(SM) 실무 가이드 | IT 이사회 거버넌스 국제표준 | 조직 성숙도 통합 모델 |
| **구조/원리** | 40 Objectives + 7 Components + Cascade | SVS + SVC + 34 Practice + 7 Guiding Principles | 6 Principles(DH ARRRR) + 5 Model Clauses | 5 Maturity Level + 4 Category(Workforce/Customer/Product/Partner) |
| **대상** | CIO/이사회/감사/컨설팅 | Service Desk/IT 운영/실무자 | 이사/경영진/이사회위 | 개발팀/PM/품질 |
| **측정성** | CMMI 6단계 PAM + ISO 15504 | Maturity Model 5단계 + KPI | 6원칙 준거 감사 체크리스트 | 5단계 표현 모델(0~5) |
| **통합성** | 매우 높음(Val IT + Risk IT + BMIS 통합) | 중간(서비스 관점) | 낮음(원칙만 제공) | 중간(모델만 제공) |
| **DX 친화성** | 높음(2019부터 Agile 반영) | 매우 높음(VeriSM/SIAM 연계) | 중간(원칙 중립) | 높음(2024 v2.0으로 Agile 통합) |
| **인증/감사** | COBIT Certified Assessor | PeopleCert/AICPA 인증 | ISO 인증(BSI/AFNOR) | CMMI Institute 인스티튜트 |
| **적합 조직** | 금융/공공/대기업(거버넌스 강조) | 통신/제조/서비스업(운영 강조) | 글로벌 법인/공공기관 | R&D 조직/CMMI 인증 수요 |
| **비용(연간)** | 컨설팅 2,000~5,000만원 | 교육 50~300만원/인 | 심사 1,500~4,000만원 | 평가 3,000~8,000만원 |

### B. 다른 시스템/도구와의 연결

| 연결 영역 | 통합 방식 | 도구/표준 예시 |
|:---|:---|:---|
| **프로젝트 관리** | PMBOK/Prince2 + COBIT BAI02(Manage Requirements) 매핑 | MS Project, JIRA, ServiceNow PPM |
| **Agile/DevOps** | ITIL 4 Service Value Chain + DORA 4 Metrics(배포빈도, 리드타임
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 747 / 800

<- **이전**: [746. IT 경영 관리 핵심 토픽 746번 시험 요약](/studynote/12_it_management/05_security_compliance/746_it_management_core_topic_746_exam_summary/)
**다음**: [748. IT 경영 관리 핵심 토픽 748번 시험 요약](/studynote/12_it_management/05_security_compliance/748_it_management_core_topic_748_exam_summary/) ->

---
