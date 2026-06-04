---
title: "669. IT 경영 관리 핵심 토픽 669번 시험 요약 (IT Management Core Topic 669 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 40개 Governance/Management Objective, ITIL 4의 34개 Service Management Practice, ISO 38500의 6대 원칙, 그리고 BSC·TCO·ROI·NPV를 통합한 **IT 거버넌스-성과측정闭环(Closed-Loop) 체계**가 핵심이며, Evaluate-Direct-Monitor(E-D-M) 사이클을 통해 IT 투자와 비즈니스 가치를 정량적으로 연결한다.
> 2. **가치**: 성숙도 1단계 상승 시 IT 비용 10~15% 절감, 프로젝트 성공률 25->75% 향상, ROI 15~25% 개선, 거버넌스 의사결정 리드타임 40% 단축, 규제 컴플라이언스(전자정부법, PIPA, GDPR) 위반 리스크 60% 감소.
> 3. **판단 포인트**: 프레임워크 채택 범위(전사 COBIT vs. 영역별 ITIL), KPI 정량/정성 비율(7:3 권장), 거버넌스 구조(중앙집중 RACI vs. 분산형 Three Lines of Defense), 측정 주기(실시간 vs. 월·분기), Balanced Scorecard 4관점 가중치 배분 등 5대 설계 트레이드오프를 비즈니스 Criticality와 규제 강도에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)이 가속화되면서 전 세계 IT 지출은 2024년 기준 5조 USD를 돌파했으며, 국내 주요 그룹사들의 연간 IT 투자 규모는 1조 원 단위에 이른다. 그러나 McKinsey의 연구에 따르면 전체 IT 프로젝트 중 **성공률은 30% 미만**이며, Standish Group의 CHAOS Report는 평균 66%의 프로젝트가 예산·일정·범위(Scope) 측면에서 실패한다고 보고한다. 이러한 투자 대비 성과(Value Leakage) 문제를 해결하기 위해 등장한 것이 **IT 거버넌스(IT Governance)** 이다.

정보관리 기술사 시험에서 빈출되는 669번대 토픽은 "IT 투자 대비 가치 실현(Value Realization) 및 성과 측정"이며, 이는 단순한 프로젝트 관리를 넘어 **전략적 의사결정-투자 포트폴리오-운영 통제-성과 피드백**의 전 과정을 다루는 경영관리(Governance) 영역이다.

과거(1990~2000년대)에는 IT 부서가 **Cost Center(비용 센터)** 로 인식되어, "IT는 비용이다"라는 관점에서 무조건적인 비용 절감 압력만 받았다. 그러나 2010년 이후 클라우드·AI·데이터 분석이 비즈니스 핵심으로 자리매김하면서 IT는 **Value Center(가치 센터)** 로 재정의되었고, 이에 따라 IT 투자의 **정량적 정당화**와 **지속적인 가치 측정**이 경영 최우선 과제로 부상했다.

```text
[ IT 거버넌스 진화 패러다임 비교 ]

[과거: Cost Center 시대]                    [현재: Value Center 시대]
+----------------------+                  +----------------------+
| CEO: "IT 비용 줄여라" |                  | CEO: "IT로 매출 올려라"|
+----------+-----------+                  +----------+-----------+
           |                                         |
           v                                         v
   +---------------+                          +---------------+
   |  IT 예산 통제  |                          | 비즈니스 가치  |
   |  (CapEx 위주) |                          | (ROI/BSC 중심)|
   +-------+-------+                          +-------+-------+
           |                                         |
           v                                         v
   +---------------+                          +---------------+
   | 프로젝트별     |                          | 포트폴리오 단위|
   | 사후 평가      |                          | 실시간 모니터링|
   +-------+-------+                          +-------+-------+
           |                                         |
           v                                         v
   +---------------+                          +---------------+
   |   "쓴 만큼    |                          |  "딸 수 있는  |
   |    청구"      |                          |   과일 나무"  |
   +---------------+                          +---------------+
     (Cost Recovery)                          (Value Creation)
```

또한 **규제 환경의 강화**(GDPR 2018, PIPA 2023 개정, 전자정부법, DORA 2025) 로 인해 IT 거버넌스는 '선택'이 아닌 '의무'가 되었으며, **ESG 경영 공시** 의무화에 따라 IT의 Green IT·탄소배출 측정까지 거버넌스 범위에 포함되었다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **배의 키잡이(Rudder)** 와 같습니다. 돛(프로젝트·기술)이 아무리 커도 키가 없으면 풍향에 휩쓸려 암초에 부딪히고, 바람이 순풍일 때도 목적지(비즈니스 가치)에 도달할 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 4대 글로벌 프레임워크(COBIT 2019, ITIL 4, ISO 38500, PMBOK 7th)와 성과측정 방법론(BSC, KPI Tree, TCO/ROI/NPV/IRR)의 통합적 운용이다. 아래는 5계층 아키텍처이다.

```text
[ IT 거버넌스 & 성과관리 5계층 아키텍처 ]

+--------------------------------------------------------------+
|  Layer 1: 전략 정렬 (Strategy Alignment)                     |
|  - 정보전략계획(ISP) ↔ 업무전략(Business Strategy) 동기화   |
|  - SWOT, Porter 5-Forces, McFarlan Strategic Grid            |
+--------------------------+-----------------------------------+
                           v
+--------------------------------------------------------------+
|  Layer 2: 거버^nance Framework (COBIT 2019 / ISO 38500)      |
|  - Evaluate -> Direct -> Monitor (E-D-M Cycle)                |
|  - 40개 Governance & Management Objectives                    |
|  - 7개 컴포넌트(원리, 정책, 구조, 프로세스, 정보, 문화,인력) |
+--------------------------+-----------------------------------+
                           v
+--------------------------------------------------------------+
|  Layer 3: 서비스 관리 (ITIL 4 Service Management)            |
|  - 34개 Service Management Practice                          |
|  - SVS(Service Value System) -> Value Chain -> Practices        |
|  - SLA/SLO/SLI 3-tier 계층                                   |
+--------------------------+-----------------------------------+
                           v
+--------------------------------------------------------------+
|  Layer 4: 운영 통제 (PMBOK 7th + DevOps + Agile)             |
|  - 8개 Performance Domain                                    |
|  - CI/CD 파이프라인, GitOps, Observability                   |
|  - 변경관리, 형상관리, incident/Problem 관리                 |
+--------------------------+-----------------------------------+
                           v
+--------------------------------------------------------------+
|  Layer 5: 성과 측정 & 가치 실현 (BSC + KPI + 재무분석)        |
|  - BSC 4관점: 재무(25%)/고객(25%)/내부프로세스(30%)/학습(20%)|
|  - TCO, ROI, NPV, IRR, Payback Period                       |
|  - OKR 기반 전략실행 연계                                   |
+--------------------------------------------------------------+
                           |
                           v
              +------------------------+
              |  Continuous Improvement |  <- Kaizen, PDCA,
              |  & Feedback Loop        |    Retrospective
              +------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019 (거버넌스 코어)** | 전사 IT 통제 체계 수립 및 감사 표준 제공 | 40개 Governance/Management Objective를 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 구분. **Design Factors 11개**(전략, 목표, 위험, 문제 등)로 조직 상황에 맞는 거버넌스 시스템 설계. Capability Level 0~5 모델로 성숙도 측정. |
| **ITIL 4 (서비스 운영)** | IT 서비스의 End-to-End 가치 흐름 관리 | **Service Value System(SVS)**: Opportunity/Demand -> Value -> Service Value Chain(Plan/Engage/Design&Transition/Obtain&Build/Deliver&Support/Improve) -> Value. 34개 Practice 중 핵심 7개(Incident, Problem, Change, Service Desk, Service Level, Continual Improvement, Monitoring & Event Management) 운영. |
| **ISO/IEC 38500 (이사회 수준 거버^nance)** | IT 의사결정의 최상위 원칙 제시 | 6대 원칙: **Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior**. 이사회(Board)가 IT를 "Govern"하도록 하는 3단계 모델(Evaluate->Direct->Monitor). 2015년 이후 4개 상세표준(38500-1~38500-4) 제공. |
| **BSC (Balanced Scorecard)** | 전략을 4관점 KPI로 분해 및 연계 | Kaplan-Norton 모델: 재무(Financial: 매출/비용/ROIC) / 고객(Customer: NPS, CSAT) / 내부 프로세스(Internal: MTTR, 처리량) / 학습·성장(Learning: 직원역량, 혁신지수). 각 관점별 **Lead/Lag Indicator** 구분, **Strategy Map**으로 인과관계 시각화. |
| **Three Lines of Defense (3LoD)** | 리스크·컴플라이언스 통제 구조 | 1st Line(운영부서, 셀프컨트롤) -> 2nd Line(리스크/컴플라이언스, 정책·모니터링) -> 3rd Line(내부감사, 독립적 검증). IIA(Institute of Internal Auditors) 표준. |
| **ROI/NPV/IRR 분석 엔진** | IT 투자의 재무적 정당화 산출 | ROI = (순편익/총투자비용) × 100, NPV = Σ(CFₜ/(1+r)ᵗ) - 초기투자, IRR은 NPV=0이 되는 할인율. **할인율(WACC)** 적용 필수, **Total Cost of Ownership(TCO)** 5개년 산정(도입 20%, 운영 60%, 폐기 20%) 권장. |
| **OKR (Objectives & Key Results)** | 전략집행의 분기별 트래킹 | 1~3개의 Objective(질적 목표) + 3~5개의 Key Results(정량 측정). Google, Intel 사례
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 669 / 800

<- **이전**: [668. IT 경영 관리 핵심 토픽 668번 시험 요약](/studynote/12_it_management/05_security_compliance/668_it_management_core_topic_668_exam_summary/)
**다음**: [670. IT 경영 관리 핵심 토픽 670번 시험 요약](/studynote/12_it_management/05_security_compliance/670_it_management_core_topic_670_exam_summary/) ->

---
