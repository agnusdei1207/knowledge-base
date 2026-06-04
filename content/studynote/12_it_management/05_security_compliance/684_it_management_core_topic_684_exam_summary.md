---
title: "684. IT 경영 관리 핵심 토픽 684번 시험 요약 (IT Management Core Topic 684 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 시험의 IT 경영관리(684번) 영역은 **IT 거버넌스-전략-투자-운영-감리-컴플라이언스**를 잇는 End-to-End 가치사슬(Value Chain)을, COSO·COBIT·ITIL·ISO 38500·PMP·SWEBOK 같은 글로벌 표준 프레임워크로 정량적 의사결정(ROI/NPV/IRR, BSC/KPI, SLM)으로 변환하는 능력을 평가한다.
> 2. **가치**: 정성·정량 평가 모델(예: NPV 12% 할인율, IRR≥WACC+3%p, payback period 5년 이내 등)의 일관된 적용으로 **IT 투자 실패율(전통 30~40%)을 1/3 수준으로 절감**하고, EA·거버넌스 정착 시 **TCO 15~25% 감축, 현업 만족도 20%^, 감사 적정판정 비율 90% 이상**을 달성 가능하다.
> 3. **판단 포인트**: "거버넌스 3축(의사결정·리스크·컴플라이언스)"을 **One-Page Framework**로 압축해 White Paper 수준으로 설명하되, 반드시 **① 기간/범위/제약 ② 정량 KPI ③ 대안 Trade-off ④ 발생/탐지/대응 리스크 ⑤ 거버넌스/감리 단계** 5박자를 채워야 만점이 되며, "기술만 나열"하거나 "경영 원칙만 추상화"하는 양극단 서술이 가장 큰 탈락 포인트다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 684번(IT 경영관리) 영역은 단순한 "경영학 일반"이 아니다. 기업의 **Mission -> 전략 -> IT 전략 -> IT 거버넌스 -> IT 운영 -> IT 감리/평가** 로 이어지는 가치사슬 전체를, **측정 가능한 정량 지표(NPV, IRR, TCO, EVA, KPI, SLA)** 와 **글로벌 표준 프레임워크(COBIT 2019, ITIL 4, ISO 38500, PMBOK 7th, BABOK, CMMI, ISO 27001)** 로 풀어내야 하는 **실무 의사결정 시뮬레이션**이다.

과거(1990년대)에는 CIO가 "데이터센터 증설"·"ERP 도입" 같은 대규모 프로젝트 단위로 의사결정했고, ROI도 경험적·정치적으로 결정되는 경우가 많았다. 그러나 클라우드·SaaS·AI·데이터 거버넌스 시대에는 **연간 CapEx/OpEx 50:50 -> 20:80** 으로 사업 구조가 바뀌었고, 이로 인해 **TCO 모델링, FinOps, Zero-Trust, AI 거버넌스(EU AI Act, 한국 AI 기본법 2026.1 시행)** 같은 새로운 경영 통제 요구가 폭증했다.

```text
+--------------------------------------------------------------------------+
|          IT 경영관리 Value Chain (684번 도메인 전체 지도)                  |
+--------------------------------------------------------------------------+
|  [Mission / Vision]                                                     |
|        |                                                                |
|        v                                                                |
|  +------------------+    +------------------+    +------------------+  |
|  | ① IT 전략수립    | ->  | ② IT 거버넌스    | ->  | ③ IT 투자경제성  |  |
|  |  - SWOT/TOWS     |    |  - COBIT 2019    |    |  - TCO/ROI/NPV   |  |
|  |  - Porter 5Force |    |  - ISO 38500     |    |  - IRR/Payback   |  |
|  |  - EA(TOGAF)     |    |  - RACI/3 Lines  |    |  - EVA/SCM       |  |
|  +------------------+    +------------------+    +------------------+  |
|        |                       |                       |                 |
|        +------------+----------+-----------+-----------+                 |
|                     v                      v                             |
|            +------------------+    +------------------+                  |
|            | ④ IT 운영관리    |    | ⑤ 평가/감리      |                  |
|            |  - ITIL 4 SVS    |    |  - 정보시스템감리 |                  |
|            |  - SLA/OLA/UC    |    |  - BSC/KPI       |                  |
|            |  - DevOps/FinOps |    |  - 성과측정/BSC  |                  |
|            +------------------+    +------------------+                  |
|                     |                      |                             |
|                     +----------+-----------+                             |
|                                v                                         |
|                  +--------------------------+                            |
|                  | ⑥ 컴플라이언스·리스크     |                            |
|                  |  - ISO 27001/27701/31000 |                            |
|                  |  - GDPR/개인정보보호법    |                            |
|                  |  - AI 거버넌스/공급망     |                            |
|                  +--------------------------+                            |
+--------------------------------------------------------------------------+
```

기존에는 위 Value Chain의 각 단계가 "별도 과목" 처럼 분리되어 있었지만, 최근 시험은 **"AI 도입 시 데이터 거버넌스·TCO·리스크를 통합 평가"** 하거나 **"클라우드 마이그레이션 시 CapEx->OpEx 전환에 따른 거버넌스 변화"** 처럼 **시나리오 통합형**으로 출제된다. 따라서 단순 암기형 답안이 아니라, **"5박자(기간·정량 KPI·대안·리스크·거버넌스)"** 를 일관되게 채우는 서술력이 합격의 핵심이다.

- **📢 섹션 요약 비유**: IT 경영관리는 "자동차의 계기판 + 운전면허 + 정비 매뉴얼"이 한 권으로 합쳐진 책과 같다. 엔진(IT 기술)이 아무리 좋아도, **계기판(KPI)**이 고장나면 과속·과부하로 사고가 나고, **면허(거버넌스)**가 없으면 법규·보안 위반으로 벌점을 받고, **정비 매뉴얼(ITIL/COBIT)**이 없으면 연비(TCO)가 망가진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

684번 영역의 "아키텍처"는 **3-Layer Governance Architecture(의사결정-통제-운영)** 와 이를 뒷받침하는 **측정 메커니즘**으로 구성된다.

```text
+-------------------------------------------------------------------------+
|            IT 경영관리 3-Layer Architecture (COBIT 기반)                |
+-------------------------------------------------------------------------+
|                                                                         |
|  +-----------------------------------------------------------------+   |
|  | Layer 1: 의사결정 (Board / Steering Committee)                   |   |
|  |  - 이사회의 IT oversight (ISO 38500 Principle 1: Responsibility) |   |
|  |  - IT 전략위원회, IT Steering Committee                          |   |
|  |  - 1차 거버넌스: Risk Appetite, Portfolio, Budget Cap           |   |
|  |  +---------------------------------------------------------+    |   |
|  |  | 입력: 사업전략/리스크허용도/규제환경                       |    |   |
|  |  | 출력: IT 원칙 / 표준 / 투자 우선순위 / 정량 KPI(BSC)      |    |   |
|  |  +---------------------------------------------------------+    |   |
|  +-----------------------------------------------------------------+   |
|                              |                                          |
|                              v                                          |
|  +-----------------------------------------------------------------+   |
|  | Layer 2: 통제 (Management / CIO / EA)                           |   |
|  |  - COBIT 2019 Governance & Management Objectives (40 EDM/MEA)  |   |
|  |  - EA(TOGAF ADM) - As-Is -> To-Be -> Transition Architecture     |   |
|  |  - 2차 거버넌스: 3 Lines of Defense (1LoD: 사업, 2LoD: IT,      |   |
|  |                   3LoD: 내부감사/내부통제)                        |   |
|  |  +---------------------------------------------------------+    |   |
|  |  | KPI: TCO 감축률, ROI, SLA 달성률, 감사 적정판정 비율    |    |   |
|  |  +---------------------------------------------------------+    |   |
|  +-----------------------------------------------------------------+   |
|                              |                                          |
|                              v                                          |
|  +-----------------------------------------------------------------+   |
|  | Layer 3: 운영/서비스 (Operations / Service Desk)                |   |
|  |  - ITIL 4 Service Value System(SVS): 7 Guiding Principles,     |   |
|  |    4 Dimensions, 34 Practices, Value Chain Activities            |   |
|  |  - SLA / OLA / UC(Service Catalogue / Service Level)            |   |
|  |  - DevOps / SRE / AIOps / FinOps                                |   |
|  |  +---------------------------------------------------------+    |   |
|  |  | KPI: MTTR, MTBF, 가용성(%), 사건건수, CSAT/NPS         |    |   |
|  |  +---------------------------------------------------------+    |   |
|  +-----------------------------------------------------------------+   |
|                              |                                          |
|                              v                                          |
|   [Feedback Loop: BSC, KPI DashBoard, 내부감사, 정보시스템 감리]         |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스의 메타 프레임워크 | 5 Governance Principles(Stakeholder Value, Holistic Approach, Dynamic Governance System, Tailored to Enterprise Needs, End-to-End) + 40 Objectives(EDM 5개, MEA 4개, Align/Plan/Organize 14, Build/Acquire/Implement 11, Deliver/Service/Support 6) + Focus Area(예: DevOps, RPA, AI, Cybersecurity) |
| **ISO/IEC 38500** | 이사회 수준 IT 거버넌스 국제표준 | 6 Principle(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) - "Direct, Monitor, Evaluate" 3단계 거버넌스 사이클 |
| **ITIL 4 (SVS)** | IT 서비스 운영·가치공급 실무체계 | Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) + 34 Practice(Incident, Problem, Change Enablement, Service Desk, SLO/SLI) + 4 Dimension(Org/People, Information, Technology, Partners/Suppliers) |
| **EA(TOGAF ADM)** | 전사 아키텍처 방법론 | ADM Cycle: Preliminary -> Vision -> Business Architecture -> Information Systems -> Technology -> Opportunities/Solutions -> Migration Planning -> Implementation Governance -> Change Management. **Architecture Repository(ABD/ABeD/Standards/Governance Log)** |
| **TCO/ROI 모델** | IT 투자 정량 의사결정 | TCO = 직접비(HW/SW/Lic/인건비) + 간접비(교육/다운타임/통합/전환/운용). 5년 TCO로 환산, 할인율(WACC) 8~12% 적용. **Gartner TCO 모델 / IDC TCO 모델 / Microsoft TCO Tool** 등이 대표적 |

### 핵심 산식과 임계치

- **NPV(순현재가치)**: NPV = Σ [CFₜ / (1+r)ᵗ] − Initial Investment. **r = WACC(가중평균자본비용), 통상 8~12%**. 의사결정 기준: NPV > 0 -> GO, NPV < 0 -> STOP.
- **IRR(내부수익률)**: NPV=0 이 되는 r. **판정: IRR ≥ Hurdle Rate(보통 WACC + 3~5%p) -> 채택**.
- **Payback Period(투자회수기간)**: 누적 CF가 0이 되는 시점. **전략적 시스템은 5년 이내, 인프라 7년 이내** 가 일반적 가이드라인.
- **EVA(Economic Value Added)**: NOPAT − (WACC × 투하자본). **EVA > 0 지속**이 shareholder value 창출의 핵심.
- **BSC(Balanced Scorecard) 4관점**: ① 재무 ② 고객 ③ 내부프로세스 ④ 학습·성장. **인과관계 맵(Cause-effect Map)** 으로 전략을 KPI 사슬로 변환.
- **SLA 등급**: 계층화(Tier1: 99.9% / 월가동시간 43.8분, Tier2: 99.99% / 4.38분, Tier3: 99.999% / 0.44분). 금융·의료 등 미션크리티컬은 Tier2~3 요구.

### 정보시스템 감리의 5단계

```text
[계획(Plan)] -> [분석(Analysis)] -> [설계(Review)] -> [구축(Inspection)] -> [종료(Closure)]
   |              |                 |                |                 |
   v              v                 v                v                 v
 사업요구      요구사항 정의       상세설계         구현/테스트         인수/이행
 적합성        적정성             적정성           적합성             효과성
```

감리 단계별 **투입공수 = 10:20:30:30:10 (%)** 가 일반적 비율이며, 6대 감리영역(사업/요구/설계/구축/이행/운영) + 26개 중점검토사항을 기준으로 **적정(C) / 보통(B) / 미흡(A)** 3단계로 등급을 부여한다.

- **📢 섹션 요약 비유**: 3-Layer 거버넌스는 **"에어라인(항공사)의 3중 안전장치"** 와 같다. **Layer1(이사회)**=탑승 전 비행계획과 책임자 지정, **Layer2(관제탑·CIO)**=이륙~착륙 전 과정의 항로·고도 통제, **Layer3(조종사·운영팀)**=실시간 계기 비행. 3개 층 중 하나라도 끊기면 사고(IT 실패·규제 위반·보안 침해)로 직결된다.

---

## Ⅲ. 비교 및 연결

IT 경영관리의 핵심은 **"유사 프레임워크 간 경계와 보완 관계"** 를 명확히 구분하는 데 있다. 시험에서 가장 빈번하게 혼동되는 조합을 정리한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7th** |
| :--- | :--- | :--- | :--- | :--- |
| **계층/스코프** | 전사 거버넌스+관리(40 Objectives) | IT 서비스 운영/가치공급 | 이사회 차원의 IT 거버넌스 원칙 | 프로젝트 단위 일/이행 관리 |
| **관점** | What(무엇을 다룰 것인가) | How(서비스로
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 684 / 800

<- **이전**: [683. IT 경영 관리 핵심 토픽 683번 시험 요약](/studynote/12_it_management/05_security_compliance/683_it_management_core_topic_683_exam_summary/)
**다음**: [685. IT 경영 관리 핵심 토픽 685번 시험 요약](/studynote/12_it_management/05_security_compliance/685_it_management_core_topic_685_exam_summary/) ->

---
