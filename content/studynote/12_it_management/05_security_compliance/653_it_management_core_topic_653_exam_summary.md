---
title: "653. IT 경영 관리 핵심 토픽 653번 시험 요약 (IT Management Core Topic 653 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(40개 관리목표/5개 도메인) + ITIL 4(34개 Practices) + ISO/IEC 38500(Evaluate-Direct-Monitor 3원칙) + ISO 31000(리스크 사이클)**의 4대 표준을 통합한 **거버넌스-전략-포트폴리오-운영-평가의 5계층 의사결정 체계**이며, 핵심은 **"Value Creation(가치창출)"**의 사슬(거버넌스 의사결정 -> 전략 정렬 -> 포트폴리오 배분 -> 서비스 운영 -> 성과 피드백)을 단일화된 KPI 사슬로 연결하는 것이다.
> 2. **가치**: 정량적으로 **IT 투자 ROI 15~30% 개선**(McKinsey 2023 산업 평균), **프로젝트 성공률 28%->68% 향상**(PMI Pulse of Profession 2024), **IT 운영 비용 20~40% 절감**(Tier 1 기업 ITIL 도입 기준), **장애 복구 시간 MTTR 60% 단축**을 달성하며, 정성적으로는 **이사회-경영진-IT 부서 간 정합성(Alignment)** 확보 및 **규제 컴플라이언스(전자금융감독규정, 개인정보보호법, ESG 공시)** 대응력을 동시에 확보한다.
> 3. **판단 포인트**: **(a) 중앙집중형(Federal) vs 분산형(Federated) 거버넌스**, **(b) 표준화(Standard) vs 유연화(Tailored) 프레임워크 채택**, **(c) 단기 ROI vs 장기 디지털전환 투자 비중**, **(d) Zero Trust 보안 vs 사용자 편의성**, **(e) Build(자체) vs Buy(패키지) vs Outsource(클라우드) 의사결정**의 5대 트레이드오프가 핵심이며, 기술사적 판단은 **EA(Enterprise Architecture) 참조모델과 연계한 ROI 시뮬레이션(시나리오 3종 이상)**으로 입증해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation)이 4차 산업혁명의 핵심 동력으로 부상하면서, IT는 더 이상 **"비용 센터(Cost Center)"**가 아닌 **"가치 창출 엔진(Value Driver)"**으로 재정의되어야 한다. 그러나 2018년 한국정보화진흥원의 조사에 따르면 국내 대기업 IT 사업 중 **42.7%가 ROI 미달**, **65%가 전략 정렬 실패**, **78%가 사후 사후 평가 부재**의 문제를 겪고 있다. 이러한 배경에서 **IT 경영 관리(IT Management)**는 단순한 시스템 운영을 넘어 **거버넌스-전략-포트폴리오-운영-평가를 하나의 가치 사슬로 통합**하는 경영 체계로 자리 잡았다.

기존의 **"프로젝트 단위 IT 관리"**에서는 각 부서별, 시스템별 독립적 의사결정이 이루어져 **중복 투자(예: 동일 CRM 3개 부서 도입)**, **사일로(Silo) 현상**, **Shadow IT**(전사 IT 자산의 약 30~40%를 차지, Gartner 2024) 문제가 만성화되었다. 새로운 패러다임인 **"Value-Driven IT Management"**는 **COBIT 2019의 EDM(평가-지휘-모니터링) -> APO(정렬·계획·조직) -> BAI(구축·인수·변경) -> DSS(운영·지원·서비스) -> MEA(모니터링·평가·평가)**의 5개 도메인을 통해 **전략에서 운영까지 End-to-End 정합성**을 확보한다.

```text
[ IT 경영 관리 5계층 통합 프레임워크 아키텍처 ]

                    +-------------------------------------+
                    |  ① 거버넌스 계층 (Governance)        |  <- ISO 38500, COBIT EDM
                    |  - 이사회/IT전략위원회 의사결정         |     "WHY, WHAT"
                    |  - Risk Appetite, 정책, 권한 위임      |
                    +--------------+----------------------+
                                   | Cascade (정책·목표 하향 전파)
                    +--------------v----------------------+
                    |  ② 전략 계층 (Strategy)              |  <- ISO 38500, COBIT APO
                    |  - IT 전략 맵 (Strategy Map)         |     "WHICH"
                    |  - BSC 4관점, OKR, EA 참조모델       |
                    +--------------+----------------------+
                                   | Allocation (예산·자원 배분)
                    +--------------v----------------------+
                    |  ③ 포트폴리오 계층 (Portfolio)        |  <- COBIT APO05/06, PMO
                    |  - Demand Mgmt -> Portfolio Mgmt     |     "HOW MUCH"
                    |     -> Program Mgmt -> Project Mgmt   |
                    +--------------+----------------------+
                                   | Execution (실행·전달)
                    +--------------v----------------------+
                    |  ④ 운영 계층 (Operations)            |  <- ITIL 4, COBIT DSS
                    |  - Service Value System (SVS)        |     "HOW"
                    |  - Incident/Problem/Change/CSI      |
                    +--------------+----------------------+
                                   | Feedback (성과·리스크 보고)
                    +--------------v----------------------+
                    |  ⑤ 평가 계층 (Evaluation)            |  <- COBIT MEA, ISO 33000
                    |  - KPI/KRI 측정, 내부감사, BSC       |     "SO WHAT"
                    |  - Continuous Improvement Loop       |
                    +--------------+----------------------+
                                   |
                            +------v------+
                            |   KPI Chain  |  -> ROI 23%, NPS 45, MTTR 12min,
                            |  (성과연결)  |    Availability 99.99%, Risk v
                            +-------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **"항공우주 산업의 미션 컨트롤(Mission Control)"**과 같다. 발사(전략)부터 착륙(운영)까지 우주비행사(IT 조직)·관제탑(거버넌스)·통신망(프로세스)·관측장비(평가)가 한 체계로 움직여야 임무 성공(가치창출)에 도달한다. 부품 하나라도 정렬이 어긋나면 Challenger호처럼 폭발한다(시한폭탄 IT 프로젝트).

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. COBIT 2019 핵심 체계

COBIT 2019는 **거버넌스 5개 + 관리 35개 = 총 40개 관리목표(Management Objective)**를 정의하며, 각 목표는 **Process Activity + Organizational Structure + Information Flow + People/Skills + Policies/Procedures**의 5대 구성요소를 갖는다. 핵심은 **"Governance System Components(7가지: 프로세스, 조직구조, 정보흐름, 사람/역량, 정책, 문화/행동, 서비스/인프라/응용)"**와 **"Focus Area(예: 사이버보안, DevOps, 디지털 윤리 등 40여 개 도메인별 커스터마이징)"** 메커니즘이다.

### B. ITIL 4 Service Value System (SVS)

ITIL 4는 **SVS(Service Value System)**을 통해 **"Opportunity/Demand -> Value"**로 변환하는 체계를 제시한다. 핵심은 **34개 관리 Practice**와 **"Guiding Principles(7가지: Focus on value, Start where you are, Progress iteratively, etc.)"**이다. **Service Value Chain(Service Value Chain Activity 6단계: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)**이 활동의 백본이다.

### C. IT 전략 정렬 메커니즘

전략 정렬은 **Henderson & Venkatraman(1993) Strategic Alignment Model(SAM)**의 4개 도메인(전략, 구조, 시스템, 문화)을 **"Fit(적합성)"** 관점에서 최적화하는 것이다. 실측 시 **SAM 점수 1점 상승당 기업가치 5~8% 상승**(Luftman & Brier 1999, 평균 5,500 기업 메타분석) 효과가 입증되었다.

```text
[ IT 거버넌스 의사결정 흐름 (COBIT 2019 EDM Cycle) ]

   이사회/IT전략위원회
           |
           v
   +--------------+
   |   EVALUATE   | -> ① 현황 진단: IT 성과, 리스크, 자원, 역량 평가
   |   (평가)     |   (CSF/KPI, Maturity Model 0~5단계)
   +------+-------+
          | Scorecard (예: BSC 재무관점 ROI 12% 목표)
          v
   +--------------+
   |   DIRECT     | -> ② 방향 설정: 전략, 정책, Risk Appetite, 예산 가이드
   |   (지휘)     |   (예: 클라우드 우선 정책, AI 윤리 가이드라인)
   +------+-------+
          | Directive
          v
   +--------------+
   |   MONITOR    | -> ③ 모니터링: KPI 대시보드, 내부감사, 컴플라이언스
   |   (모니터링) |   (예: SLA 99.95%, 보안사고 0건, ROI 18%)
   +------+-------+
          |
          +---> Feedback Loop -> EVALUATE (연속적 개선)
```

### D. IT 포트폴리오 관리 3단계

| 단계 | 핵심 활동 | 적용 도구/기법 |
|------|----------|---------------|
| **Demand Management** | 비즈니스 요구 수집, 우선순위 평가 | Kano Model, MoSCoW, Weighted Scoring |
| **Portfolio Management** | IT 투자의 균형(Balance) 확보 | Bubble Diagram (Value vs Risk vs Cost), BCG Matrix |
| **Program/Project Management** | 실행 통제 | PMBOK 7th(8개 도메인), PRINCE2(7가지 원칙), MSP |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (40개 목표)** | 거버넌스/관리 통합 프레임워크 | EDM(5) + APO(14) + BAI(11) + DSS(6) + MEA(4) = 40개 목표; **"Governance & Management Objectives"** 체계; 능력수준 0~5(NRR/RPA 모델) |
| **ITIL 4 (34 Practices)** | 서비스 운영·개선 체계 | SVS(서비스 가치 시스템) + Value Chain 6단계; **Change Enablement, Incident Mgmt, Service Desk, SLA, CSI** |
| **ISO/IEC 38500 (3원칙)** | 이사회 수준 IT 거버넌스 국제표준 | Responsibility(책무), Strategy(전략), Acquisition(취득), Performance(성과), Conformance(준법), Human Behavior(인간행동) **6개 지침**; 3원칙 Model: **Evaluate -> Direct -> Monitor** |
| **BSC (Balanced Scorecard)** | 전략 성과 다차원 측정 | **4관점(재무 25%, 고객 25%, 내부프로세스 30%, 학습성장 20%)**; 인과관계 사슬(Learning->Process->Customer->Finance); **Strategy Map 5계층** |
| **PMBOK 7th Edition** | 프로젝트 관리 지식체계 | **8개 Performance Domain**(Stakeholder, Team, Planning, Work, Delivery, Measurement, Uncertainty, Tailoring) + **12개 Principle** |
| **ISO 31000 (Risk)** | 리스크 관리 국제표준 | **Principles-Framework-Process** 3층; ISO 31000:2018 **6단계 프로세스**(Communication, Scope, Assessment, Treatment, Monitoring, Recording) |
| **TOGAF 10 / EA** | EA 방법론 | **ADM(Architecture Development Method) 8단계**; Preliminary->A(비전)->B(비즈니스)->C(정보시스템·데이터·응용)->D(기술)->E(기회&솔루션)->F(구축계획)->G(구현거버넌스)->H(변경관리) |
| **IT 투자평가 모델** | ROI/TCO/Payback/NPV/IRR | **TCO = 직접비(20%) + 간접비(40%) + Hidden Cost(40%)**; ROI = (Tangible+Intangible Benefit) / Cost × 100 |

### E. SLA /
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 653 / 800

<- **이전**: [652. IT 경영 관리 핵심 토픽 652번 시험 요약](/studynote/12_it_management/05_security_compliance/652_it_management_core_topic_652_exam_summary/)
**다음**: [654. IT 경영 관리 핵심 토픽 654번 시험 요약](/studynote/12_it_management/05_security_compliance/654_it_management_core_topic_654_exam_summary/) ->

---
