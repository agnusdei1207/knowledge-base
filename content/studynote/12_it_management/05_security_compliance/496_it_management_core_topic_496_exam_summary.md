---
title: "496. IT 경영 관리 핵심 토픽 496번 시험 요약 (IT Management Core Topic 496 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Governance)와 포트폴리오 관리(Portfolio Management)는 **COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7th** 프레임워크를 통합하여 IT 투자 의사결정의 **Evaluate-Direct-Monitor** 3단계 책임 구조를 구현하고, 비즈니스 전략 ↔ IT 자산 ↔ 프로젝트 파이프라인의 정렬(Alignment)을 보장하는 경영 체계이다.
> 2. **가치**: Gartner(2024) 기준 성숙 IT 거버넌스 도입 기업의 **IT-Business Alignment 지수**가 2.3 -> 4.1(5점 척도)로 상승, **Stranded IT 자산 비율**이 평균 28% -> 8%로 감소하며, **IT 투자 ROI**가 평균 18% -> 34%로 개선된다. 또한 **프로젝트 실패율**을 42%에서 19%로 낮추는 정량적 효과가 보고된다.
> 3. **판단 포인트**: 중앙집중(Federal) vs 분산형(Decentralized) 거버넌스 모델 선택 시 **통제 강도-민첩성 트레이드오프**, **COBIT 2019의 40개 Governance/Management Objective**와 **ITIL 4의 34개 Practice** 간 중복/상보 관계 매핑, **Run-Grow-Transform(RGT)** 예산 배분 비중 결정(70-20-10 vs 60-30-10), 그리고 **Agile/DevOps 환경**에서의 거버넌스 경량화(Lightweight Governance) 설계가 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

현대 기업에서 IT는 더 이상 단순 지원(Back-office) 기능이 아닌 **비즈니스 차별화의 핵심 동력**이다. McKinsey(2023) 보고서에 따르면 Forbes Global 2000 기업의 **연간 IT 예산**이 평균 매출의 8.2%(약 4.7조 원 규모)에 달하며, 이 중 **23%가 사장(Stranded)되거나 비효율적으로 사용**된다. 즉, 기업의 IT 투자가 비즈니스 가치로 제대로 전환되지 못하는 **"IT Value Gap"** 문제가 발생하고 있다.

이러한 문제의 근본 원인은 **3가지 거버넌스 실패 패턴**에 있다:

1. **전략 부재(Strategy Void)**: IT 투자가 비즈니스 우선순위와 단절되어 의사결정
2. **이해관계자 갈등(Stakeholder Conflict)**: CIO, CFO, 사업부 간 권한/책무 모호
3. **가시성 결여(Visibility Gap)**: IT 성과/리스크/가치의 측정 및 보고 체계 부재

```text
+---------------------------------------------------------------------+
|              IT 거버넌스 부재 시 발생하는 Value Leakage             |
+---------------------------------------------------------------------+
|                                                                     |
|  +----------+    +----------+    +----------+    +----------+      |
|  | CEO/CTO  |---->| CIO/CISO |---->| IT PMO   |---->| Project  |      |
|  | 전략 의도|    | 번역 실패 |    | 우선순위  |    | 실행/완료 |      |
|  |  (Vision)|    |(Misalign)|    |  갈등     |    |  (Delivery)|    |
|  +----------+    +----------+    +----------+    +----------+      |
|        |               |               |               |          |
|        v               v               v               v          |
|   Strategic        Tactical         Portfolio       Operational    |
|   Gap 31%          Gap 28%         Conflict 24%    Waste 17%       |
|                                                                     |
|  [총 IT 예산 대비 비효율 비율: 평균 28-35%, Gartner 2023]           |
+---------------------------------------------------------------------+

거버넌스 적용 후 변화:
  Before: 전략(Strategy) ----X-----> 실행(Execution)  [단절]
  After : 전략 ---> 거버넌스 ---> 포트폴리오 ---> 실행   [연결]
         (Board)  (COBIT)    (RGT)        (PMBOK)
```

**Old Paradigm (Pre-2010)**: IT는 "Cost Center" 관점에서 비용 절감과 안정성 위주로 관리되며, **"Build and Run"** 사일로 조직, **연간 예산(Annual Budget) 중심 의사결정**, **워터폴(Waterfall) 거버넌스**가 주류였다.

**New Paradigm (Post-2020)**: IT는 "Value Center"로 전환되며, **제품 중심(Product-Centric) 조직**, **연중 유동 예산(Continuous Funding)** 및 **Funded-Team 모델(SAFe), FinOps**, **Agile Governance**가 도입된다. 또한 ESG(Environmental, Social, Governance) 규제와 **EU AI Act, DORA(2025.1 시행)** 등 신 규제 대응을 위해 IT 거버넌스는 **컴플라이언스 필수 요소**로 격상되었다.

- **📢 섹션 요약 비유**: IT 거버넌스 없이는 **"가계부 없이 신용카드를 쓰는 것"**과 같다. 돈이 새는 곳을 모르지만, **체계적 가계부(거버넌스 프레임워크)** 를 두면 "어디서 얼마를 쓰고, 어디서 얼마를 아꼈는지" 한눈에 보여 **가치 있는 곳에 집중 투자**할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. IT 거버넌스 3층 아키텍처

ISO/IEC 38500(2024 개정안) 기반의 IT 거버넌스는 **3계층 의사결정 구조**로 구성된다.

```text
+----------------------------------------------------------------------+
|                    IT Governance 3-Layer Architecture                |
+----------------------------------------------------------------------+
|                                                                      |
|  +--------------------------------------------------------------+    |
|  | Tier 1: Board / Executive Governance Layer                   |    |
|  |   - IT Steering Committee (월 1회)                            |    |
|  |   - 책임: Evaluate(평가) - Direction(지시) - Monitor(모니터) |    |
|  |   - 산출물: IT 전략, 정책, 예산 승인, Risk Appetite 설정     |    |
|  |   - 프레임워크: ISO 38500, COBIT 2019 EDM Domain             |    |
|  +--------------------------------------------------------------+    |
|                              |                                       |
|                              v                                       |
|  +--------------------------------------------------------------+    |
|  | Tier 2: Management / Portfolio Layer                         |    |
|  |   - IT Portfolio Review Board (격주)                          |    |
|  |   - 책임: 수요-공급 매칭, 우선순위, RGT 배분, Capability Mgmt|    |
|  |   - 산출물: Portfolio Roadmap, Investment Business Case      |    |
|  |   - 프레임워크: COBIT 2019 (APO/BAI), PMBOK 7th, SAFe LPM   |    |
|  +--------------------------------------------------------------+    |
|                              |                                       |
|                              v                                       |
|  +--------------------------------------------------------------+    |
|  | Tier 3: Operational / Delivery Layer                        |    |
|  |   - PMO, ART, Squad, Service Owner                           |    |
|  |   - 책임: 서비스 운영, 프로젝트 실행, 변경 관리, SLM         |    |
|  |   - 산출물: KPI 대시보드, Incident Report, Change Log       |    |
|  |   - 프레임워크: ITIL 4, DevOps, ITSM (ServiceNow)            |    |
|  +--------------------------------------------------------------+    |
|                                                                      |
|  [Feedback Loop: 모니터링 결과 -> Tier 1 보고 -> 전략 조정]            |
+----------------------------------------------------------------------+
```

### B. 핵심 프레임워크 통합 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO/IEC 38500** | 거버넌스 원칙(Principles) | 6대 원칙: **Responsibility(책임), Strategy(전략), Acquisition(획득), Performance(성과), Conformance(준수), Human Behavior(인적 행동)**. Board 레벨의 "Evaluate-Direct-Monitor" 사이클 적용 |
| **COBIT 2019** | 거버넌스/관리 목표 체계 | **40개 Governance/Management Objective**(EDM 5개 + APO 14 + BAI 11 + DSS 6 + MEA 4). Design Factors 11개로 맞춤형 거버넌스 시스템 설계. **Capability/Maturity 모델**: 0(Incomplete) ~ 5(Optimizing) |
| **ITIL 4** | 서비스 관리 실무 | **34개 Service Management Practice**(General 14, Service 5, Technical 17). **Service Value System(SVS)** 5대 컴포넌트: Opportunity/Demand -> Value -> Guiding Principles -> Governance -> Practices -> Continual Improvement |
| **PMBOK 7th / PRINCE2** | 프로젝트 거버넌스 | 12 Principle of Project Management, **8 Performance Domain**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty). Stage Gate 기반 Business Case 갱신 |
| **SAFe LPM / Lean Portfolio Mgmt** | 애자일 포트폴리오 | **3대 흐름: Strategic -> Operational -> Implementation**. **FPI(Fixed, Planned, Intact)** 예산 배분, **WSJF(Weighted Shortest Job First)** 우선순위 = (Business Value + Time Criticality + Risk Reduction) / Job Duration |
| **FinOps Framework** | 클라우드 비용 거버넌스 | 3단계: **Inform(가시화) -> Optimize(최적화) -> Operate(자동화)**. **Showback/Chargeback** 모델, **Reserved Instance / Savings Plan** 활용, **RI Utilization 목표 ≥ 90%** |
| **Risk & Compliance Layer** | 리스크/규제 관리 | **ISO 27005, NIST CSF 2.0, COSO ERM 2017**, **KR(Korea) ISMS-P**, **DORA(2025.1), NIS2(2024.10), EU AI Act(2024.8)**. **3 Lines of Defense** 모델(1차: 운영, 2차: 리스크/컴플, 3차: 내부감사) |
| **Value Stream / KPI 계층** | 성과 측정 | **BSC(Balanced Scorecard)** 4관점: Financial/Customer/Internal Process/Learning. **North Star Metric -> OKR -> KPI** 계층, **Leading vs Lagging Indicator** 조합 |

### C. IT 포트폴리오 우선순위 의사결정 알고리즘

**WSJF (Weighted Shortest Job First)** 계산식 (SAFe LPM 공식):

```
WSJF = Cost of Delay (CoD) / Job Duration
     = (User-Business Value + Time Criticality + Risk Reduction
        - Opportunity Enablement) / Job Size
```

**투자 우선순위 매트릭스 (5x5 이중 기준)**:

```text
        High |  ★Quick Wins    |  ★Strategic Bets  |  ★Big Rocks
             |  (High V, Low C)|  (High V, High C) |  (High V, Mid C)
  Business   |  -> 즉시 착수    |  -> 단계적 분할   |  -> PI 단위 배분
   Value     |                 |                   |
             +-----------------+-------------------+------------------
             |  Fill-Ins       |  Money Pits       |  Re-evaluate
             |  (Low V, Low C) |  (Low V, High C)  |  (Mid V, High C)
        Low  |  -> Backlog      |  -> Kill or Pivot  |  -> Defer/Renegotiate
             +-----------------+-------------------+------------------
                  Low               Mid                High
                          Cost / Risk / Complexity
```

### D. 예산 배분 RGT 모델

```text
+--------------------------------------------------------------+
|         IT 예산 RGT 배분 모델 (예: 1,000억 원 규모)          |
+--------------------------------------------------------------+
|                                                              |
|   +------------+------------+------------+                   |
|   |   RUN      |   GROW     | TRANSFORM  |                   |
|   |   60-70%   |   20-30%   |   5-10%    |                   |
|   |  (운영/유지)|  (확장/개선)|  (혁신/전환)|                   |
|   +------------+------------+------------+                   |
|   |  - 인프라  |  - 디지털  |  - AI/ML   |                   |
|   |  - 라이선스|    채널    |  - 블록체인|                   |
|   |  - 인력    |  - 데이터  |  - 플랫폼  |                   |
|   |  - 보안    |    분석    |    재설계   |                   |
|   |  - AMS    |  - CRM/마케팅|  - 신사업  |                   |
|   +------------+------------+------------+                   |
|       600억        250억        100억   (총 950억, 50억 여유)|

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 496 / 800

<- **이전**: [495. IT 경영 관리 핵심 토픽 495번 시험 요약](/studynote/12_it_management/05_security_compliance/495_it_management_core_topic_495_exam_summary/)
**다음**: [497. IT 경영 관리 핵심 토픽 497번 시험 요약](/studynote/12_it_management/05_security_compliance/497_it_management_core_topic_497_exam_summary/) ->

---
