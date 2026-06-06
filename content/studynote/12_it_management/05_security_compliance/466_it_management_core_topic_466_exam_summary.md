---
title: "IT Management Core Topic 466 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 사슬(SVC), ISO 38500 이사회 거버넌스 원칙, PMBOK 7th 프로젝트 도메인의 4대 축을 통합하여 **전략(Strategy) -> 포트폴리오(Portfolio) -> 프로그램(Program) -> 프로젝트(Project) -> 운영(Operation)** 의 Value Chain으로 IT 투자 대비 비즈니스 가치(ROI/NPV/Payback)를 극대화하는 경영 과학이다.
> 2. **가치**: McKinsey 보고 기준 효과적 IT 거버넌스 도입 시 **IT 비용 20~30% 절감, 프로젝트 성공률 35%->65% 상승, Time-to-Market 40% 단축**, ISO/IEC 38500 인증 기업은 컴플라이언스 위반 리스크를 평균 60% 감소시키며, GDPR/개인정보보호법 규제 하에서 IT 거버넌스 미비는 평균 매출의 4% 벌금 위험을 내포한다.
> 3. **판단 포인트**: 중앙집중형(COBIT RACI) vs 분산형(Federated) 거버넌스, Build vs Run 비율(70:30 -> 60:40 트레이드오프), Agile(SAFe/Spotify) vs Waterfall(PRINCE2) 적용 경계, 내부 통제(SOX 404) vs 외부 감사(SSAE18 SOC2) 비중, CapEx vs OpEx 클라우드 전환의 TCO 3년 회계 사이클을 종합 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화로 기업 IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 비즈니스 파트너**이자 **공급망의 핵심 인프라**로 격상되었다. 2020년 코로나19 이후 원격근무·전자상거래·클라우드 전환이 폭증하면서, Gartner에 따르면 전 세계 IT 지출은 2023년 **4.6조 달러**, 2024년 **5조 달러**를 돌파하며 GDP 대비 비중이 5% 내외로 확대되었다. 그러나 동일 조사에서 **IT 프로젝트 실패율은 여전히 30~40%**, IDC는 "Forrester's Failed IT Project Statistics"에서 연간 약 1조 7,000억 달러가 실패한 IT 프로젝트로 낭비된다고 추산한다. 한국 정보통신산업진흥원(NIPA)의 국내 SI 프로젝트 성공률 통계도 **완전 성공 29.3%, 부분 성공 52.4%, 실패/논쟁 18.3%** 로 절반 이상이 일정·예산·품질 목표를 부분 초과한다.

이러한 문제의 근본 원인은 (1) **이사회-경영진-IT 삼자 간 책임 소재 불명확**, (2) **프로젝트 단위 실행 vs 포트폴리오 단위 가치 관리의 미스매치**, (3) **규제·표준 준수(Compliance) 와 혁신 속도(Agility) 간 충돌**, (4) **정량 KPI 부재로 인한 ROI 불투명성** 이다. IT 경영 관리는 이러한 문제를 해결하기 위해 **거버넌스(Governance) -> 관리(Management) -> 운영(Operation)** 의 3계층 프레임워크를 수립하고, COBIT 2019의 40개 Governance & Management Objectives, ITIL 4의 34개 Practice, PMBOK 7th의 8개 Project Domain, ISO 27001/22301/20000의 통제 항목(Control)을 통합 매핑하여 **단일 통합 거버넌스 체계(SIG: Single Integrated Governance)** 를 구현하는 것을 목표로 한다.

```text
[ IT 경영 관리 3계층 통합 거버넌스 구조 ]

+------------------------------------------------------------------------+
|  Tier 1: GOVERNANCE (전략·방향성)        ISO 38500 / COBIT EDM        |
|  +------------------------------------------------------------------+  |
|  | • 이사회(Board) ↔ CISO/CDO/CIO 거버넌스 위원회                  |  |
|  | • 원칙: 책임(R), 전략(S), 획득(A), 성능(P), 적합(C), 인위(H)   |  |
|  | • 주기: 분기 Review / 연도 Plan / 수시 Audit                    |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
                                  <-> RACI Matrix
+------------------------------------------------------------------------+
|  Tier 2: MANAGEMENT (전술·조정)           COBIT 2019 / ITIL SVC      |
|  +------------------------------------------------------------------+  |
|  | • PMO(Program Mgmt Office) ↔ SMO(Service Mgmt Office) ↔ BISO    |  |
|  | • 포트폴리오 관리: BCG Matrix · Value vs Risk 2x2               |  |
|  | • 서비스 가치사슬: Plan->Engage->Design&Transition->Obtain/Build   |  |
|  | •     ->Deliver&Support->Improve (7단계)                          |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
                                  <-> SLA / OLA / UC
+------------------------------------------------------------------------+
|  Tier 3: OPERATIONS (실행·운용)           ITIL OPS / DevOps/SRE      |
|  +------------------------------------------------------------------+  |
|  | • Agile Squad · Scrum Team · SRE On-Call · SOC Analyst          |  |
|  | • Incident->Problem->Change->Release (ITIL 4 PMLC)                |  |
|  | • DORA Metrics: Deployment Freq · MTTR · Change Fail · Lead    |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시 행정 시스템**과 같다. 시议会(이사회)가 도시 계획(비전)을 수립하고, 시청(PMO/SMO)이 부서 간 예산·인력을 조율하며, 각 구청·소방서(운영팀)가 민원 처리(Incident)와 시설 관리(Problem)를 수행한다. 도시가 잘 돌아가려면 마스터플랜(EA)·예산(FinOps)·민원시스템(CRM)·감사(IA)가 동시에 작동해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **COBIT 2019의 Cascading Goals** 와 **ITIL 4의 Service Value Chain(SVC)** 의 결합이다. COBIT 2019은 13개 Enterprise Goal -> 13개 Alignment Goal -> 40개 Governance/Management Objective의 3단 캐스케이딩을 통해 **"왜(Why) 무엇을(What)"** 를 정의하고, ITIL 4 SVC는 **"어떻게(How) 제공한다"** 를 6개 핵심 활동(Plan/Engage/Design&Transition/Obtain&Build/Deliver&Support/Improve)으로 구체화한다. 여기에 PMBOK 7th의 8 Performance Domain(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)과 ISO 21502 Project Governance가 프로젝트 레이어의 거버넌스를 보강한다.

데이터 흐름 관점에서 IT 경영 관리 시스템은 **PDCA(Plan-Do-Check-Act) + OODA(Observe-Orient-Decide-Act)** 의 이중 루프를 가진다. 외부 루프는 COBIT의 EDM( Evaluate, Direct, Monitor) 으로 **연 1~4회** 이사회에 보고되고, 내부 루프는 ITIL의 CSI(Continual Service Improvement) 로 **월/주 단위** 운영 개선을 수행한다. 핵심 KPI는 (1) 재무(Financial): IT 비용/매출 비율, ROI, TCO, (2) 내부 프로세스: SLA 준수율, MTTR, Change Success Rate, (3) 학습·성장: 직원 인증 수, 교육 시간, (4) 고객/비즈니스: NPS, CSAT, Incident Volume의 4 관점을 Balanced Scorecard로 측정한다.

```text
[ Cascading Goals & Service Value Chain 통합 흐름 ]

       +--------------------------------------------------+
       |  Stakeholder Needs & Expectations (ISO 38500 §3) |
       +---------------------+----------------------------+
                             v
       +--------------------------------------------------+
       |  Enterprise Goals (13) — 재무·고객·내부·성장    |
       |  ex) EG01 Portfolio of competitive products      |
       +---------------------+----------------------------+
                             v +- Goals Cascade -+
       +--------------------------------------------------+
       |  Alignment Goals (13) — IT↔Business 정렬       |
       |  ex) AG01 IT 준거·지원, AG09 정보·처리 인가     |
       +---------------------+----------------------------+
                             v
       +--------------------------------------------------+
       |  Governance/Management Objectives (40)           |
       |  EDM(5) · APO(14) · BAI(11) · DSS(6) · MEA(4)  |
       +---------------------+----------------------------+
                             v +- Service Value Chain -+
   +---------+  +----------+  +----------+  +----------+
   |  Plan   |<-->|  Engage  |<-->| Design & |<-->|  Obtain  |
   |         |  |          |  |Transition|  | & Build  |
   +----+----+  +-----+----+  +----+-----+  +----+-----+
        |             |            |             |
        v             v            v             v
   +---------+  +--------------------------------------+
   |Deliver &|<-->|        Improve (CSI)                |
   | Support |  |  • DORA 4 metrics • SLA 보고        |
   +---------+  +--------------------------------------+
        |             |
        +------> 측정·모니터링 (DSS: Monitor/Evaluate/Assess)
                     v
             +-----------------------+
             | 보고: 이사회·감사·규제 |
             +-----------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 거버넌스 의사결정 | 5개 목표: EDM01 거버넌스 체계, EDM02 이득 전달, EDM03 리스크 최적화, EDM04 자원 최적화, EDM05 이해관계자 투명성. 이사회 KPI 보고 주기는 EDM01에서 RACI Chart로 정의 |
| **APO (Align/Plan/Organize)** | 전략·계획·조직 | 14개 목표: APO01 관리 프레임워크, APO02 전략, APO04 조직, APO12 리스크 관리, APO13 보안. Agile@Scale 적용 시 APO02에서 SAFe PI Planning과 연동 |
| **BAI (Build/Acquire/Implement)** | 솔루션 도입·구축 | 11개 목표: BAI01 프로그램, BAI02 요구사항, BAI03 투자 결정, BAI11 프로젝트 관리. PRINCE2 7 Themes와 직접 매핑, Go/No-Go Gate 통과 시 BAI03 투자 결정 |
| **DSS (Deliver/Service/Support)** | 서비스 운영·지원 | 6개 목표: DSS01 운영, DSS02 서비스 요청·인시던트, DSS03 문제, DSS04 연속성, DSS05 보안 서비스, DSS06 비즈니스 프로세스 통제. ITIL 4 Incident Management Practice와 1:1 매핑 |
| **MEA (Monitor/Evaluate/Assess)** | 성과 평가·감사 | 4개 목표: MEA01 성능·준거 모니터링, MEA02 내부 통제 체계, MEA03 외부 감사 준수, MEA04 assurance. SOX 404 ICFR과 1:1 매핑, 연간 1회 이상 외부 감사(ISAE 3402/SOC2 Type II) |
| **PMO (Project Mgmt Office)** | 프로젝트 포트폴리오 조정 | EPMO(Enterprise)/TPMO(Transformational)/SPMO(Strategic) 3계층, 프로젝트 단계별 Gate Review 수행. Gartner 분류: Compliance/Strategic/Operational 3 Bin Portfolio |
| **SMO (Service Mgmt Office)** | 서비스 품질 거버넌스 | SLA/XLA(Experience Level Agreement)/OLA(Operational Level Agreement) 관리, CSI 등록부(CSI Register) 운영. SLO/SLI를 Prometheus·Datadog으로 자동 수집 |
| **Risk & Compliance Office** | 리스크·규제 통합 | 3 Lines Model: 1st Line 운영, 2nd Line 리스크·컴플라이언스, 3rd Line 내부감사(IIA). K-Risk(국가리스크), ISO 31000 Enterprise Risk Management 적용 |

핵심 알고리즘·산식으로, **포트폴리오 우선순위 결정**은 BCG Matrix 의 파생형인 **Lewis/Roche Value vs Risk Matrix** 를 사용한다. 우선순위 점수 = `Score = w1·(StrategicFit) + w2·(FinancialROI) + w3·(RiskMitigation) - w4·(ResourceConsumption)` 이며, 가중치는 AHP(Analytic Hierarchy Process) 로 Saaty의 1~9 척도로 산출한다. **IT 성과 측정**은 Cobb-Douglas 생산함수의 IT 버전인 `IT_Value = α·ln(Quality) + β·ln(Speed) + γ·ln(Cost) + ε` 형태로 회귀분석하며, **IT 비용 최적화**는 TOGAF ADM(Architecture Development Method) Phase E의 Opportunities & Solutions 단계에서 `CBA = Σ(DiscountedBenefit_t - DiscountedCost_t) / (1+r)^t` 의 NPV와 `PI = ΣPV(Benefit)/ΣPV(Cost)` 의 Profitability Index로 결정한다. **리스크 정량화**는 FAIR(Factor Analysis of Information Risk) 모델의 `ALE = SLE × ARO` (Annual Loss Expectancy = Single Loss Exposure × Annual Rate of Occurrence) 와 Monte Carlo Simulation(10,000회 반복) 으로 VaR(Value at Risk) 산출한다.

- **📢 섹션 요약 비유**: COBIT Cascading Goals는 **나무의 뿌리-줄기-가지-잎 구조** 와 같다. 햇빛(Stakeholder Needs)이 뿌리(Enterprise Goal)에 흡수되어 줄기(Alignment Goal)를 통해 양분을 운반하고, 가지(Governance Objective)에 영양을 공급해 결국 잎(Service Value Chain)에서 광합성(비즈니스 가치)을 만든다. 뿌리가 건조하면 잎은 시든다(거버넌스 부재 시 운영 가치 증발).

---

##
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 466 / 800

<- **이전**: [465. IT 경영 관리 핵심 토픽 465번 시험 요약](/studynote/12_it_management/05_security_compliance/465_it_management_core_topic_465_exam_summary/)
**다음**: [467. IT 경영 관리 핵심 토픽 467번 시험 요약](/studynote/12_it_management/05_security_compliance/467_it_management_core_topic_467_exam_summary/) ->

---
