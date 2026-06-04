+++
title = "471. IT 경영 관리 핵심 토픽 471번 시험 요약 (IT Management Core Topic 471 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 471. IT 경영 관리 핵심 토픽 (IT Management Core Topic)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019, ISO/IEC 38500, ITIL 4, BSC, 포터의 가치사슬 등 글로벌 거버넌스 프레임워크를 기반으로 **비즈니스 목표(EG)와 IT 거버넌스(EDM), 자원관리, 위험 통제, 성과측정(MEA)** 을 통합 운영하여 기업 가치를 극대화하는 경영체계이다.
> 2. **가치**: Gartner(2023) 보고에 따르면成熟된 IT 거버넌스 체계 구축기업은 **IT 투자 ROI 23~35% 향상, 프로젝트 실패율 40% 감소, TCO 18% 절감, 컴플라이언스 위반 60% 감소** 효과를 달성하며, McKinsey는 디지털 전환 성공 확률을 26%에서 76%로 끌어올린다.
> 3. **판단 포인트**: **"통제(Control) ↔ 유연성(Agility)"** 및 **"비용(Cost) ↔ 가치(Value)"** 트레이드오프의 정량적 균형점 도출이 핵심이며, **BMC(Business Model Canvas) + EA(Enterprise Architecture) + GRC(Governance-Risk-Compliance) + PMO** 4축 통합 설계 시 조직 성숙도(Level 1~5)에 맞는 점진적 도입 전략이成败를 가른다.

---

## Ⅰ. 개요 및 필요성

IT 경영관리는 2000년대 들어 IT가 단순 비용(Cost Center)에서 **전략적 가치 창출원(Value Driver)** 으로 전환되면서, CFO·CEO·CIO가 공동으로 의사결정하는 **삼자 거버넌스(Three Lines of Defense)** 체계로 진화했다. 과거(1990년대)에는 IT 관리를 **"데이터센터 운영, 네트워크 가용성, 라이선스 관리"** 의 기술적 관점에 국한했으나, 현재는 **사이버보안 위협(연간 8.4조 손실 - IBM 2023), GDPR·개인정보보호법 등 규제강화, AI·클라우드 전환으로 인한 CapEx->OpEx 모델 변화** 등 경영환경의 구조적 변화로 인해 **IT 자체가 아닌 IT를 통해 무엇을 달성할 것인가(Outcomes)** 가 핵심 질문이 되었다.

정보관리기술사 시험 471번 유형은 주로 **(1) IT 전략수립 및 평가, (2) IT 성과측정 및 KPI 설계, (3) IT 거버넌스 프레임워크 비교, (4) IT 투자우선순위(Portfolio) 결정, (5) IT 위험 및 컴플라이언스 통합관리** 가 출제되며, **"프레임워크 암기"보다 "비즈니스 요구에 맞는 프레임워크 선택과 운영 모델(Operating Model) 설계"** 를 평가한다.

```text
+------------------------------------------------------------------+
|           IT 경영관리 4대 영역 통합 참조모델 (I-T-O-M)            |
+------------------------------------------------------------------+
|                                                                  |
|  +--------------+  +--------------+  +--------------+          |
|  | ① 전략/기획  |  | ② 거버넌스   |  | ③ 운영/전달  |          |
|  |  (Strategy)  |-> | (Governance) |-> | (Operation)  |          |
|  +------+-------+  +------+-------+  +------+-------+          |
|         |                  |                  |                  |
|         v                  v                  v                  |
|  +--------------+  +--------------+  +--------------+          |
|  | • SWOT/5-Forces| | • COBIT 2019 |  | • ITIL 4     |          |
|  | • BMC Canvas  | | • ISO 38500  |  | • DevOps     |          |
|  | • TOGAF EA    | | • SOX/내부통제|  | • SLA/OLa    |          |
|  | • BPO/BPR     | | • GRC(통합)  |  | • FinOps     |          |
|  +------+-------+  +------+-------+  +------+-------+          |
|         |                  |                  |                  |
|         +------------------+------------------+                  |
|                            v                                     |
|                  +------------------+                            |
|                  | ④ 측정/개선(PSI) |                            |
|                  | • BSC(4관점)     |                            |
|                  | • KPI/KGI/CFS   |                            |
|                  | • CSF/CSF-Map   |                            |
|                  | • PDCA/DFSS     |                            |
|                  +------------------+                            |
|                                                                  |
+------------------------------------------------------------------+
        [CobiT 2019 EDM(직접) ↔ APO(계획) ↔ BAI(실행) ↔ DSS(운영) ↔ MEA(측정)]
```

**왜 필요한가? (구 vs 신 패러다임)**

| 구분 | 1990s-2000s (Legacy) | 2020s (New Paradigm) |
| :--- | :--- | :--- |
| **IT의 위치** | 비용(Cost)·지원(Support) | 가치(Value)·전략(Strategy) |
| **투자관점** | CapEx 일회성 대형프로젝트 | OpEx 구독·과금형 서비스 |
| **거버넌스** | CIO 독심체, 사후통제 | C-Level 위원회, 실시간 Risk-based |
| **측정지표** | 시스템 가용성(99.9%), 처리량 | 비즈니스 임팩트, NPS, TTV |
| **프레임워크** | ITIL v2, COBIT 4.1 | COBIT 2019, ITIL 4, ISO 38500 |
| **조직** | 기능별 수직(Functional Silos) | 제품 중심 횡단(Agile/Platform) |
| **아키텍처** | Monolith, On-Premise | MSA, Cloud-Native, AI-First |
| **리스크** | 자연재해, HW장애 | 랜섬웨어, 공급망(Supply Chain) |

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **자동차의 계기판(스피도·연비·엔진온도·타이어공기압)** 과 같습니다. 엔진(IT 시스템)이 아무리 좋아도 계기판(거버넌스·측정체계)이 없으면 운전자는 과속·과부하를 인지하지 못하고 사고를 냅니다. **전략 = 목적지, 거버넌스 = 운전면허, 운영 = 운전행위, 측정 = 계기판**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **"전략(Why/What) -> 거버넌스(Who/How) -> 운영(Do) -> 측정(Check) -> 개선(Act)"** 의 폐루프(Closed-Loop)이며, 이를 **COBIT 2019의 5개 도메인(EDM, APO, BAI, DSS, MEA)** 과 매핑한다. 각 구성요소는 다음과 같이 작동한다.

```text
+--------------------------------------------------------------------+
|        IT 경영관리 계층구조 및 정보흐름 (Closed-Loop Cycle)        |
+--------------------------------------------------------------------+
|                                                                    |
|   +------------------------------------------------------+        |
|   |  L1: 전략결정층 (C-LEVEL / STEERING COMMITTEE)        |        |
|   |  -> BSC, IT전략맵, Portfolio Prioritization            |        |
|   +--------------------+---------------------------------+        |
|                        | 1. Cascade (전략->목표->지표)               |
|                        v                                          |
|   +------------------------------------------------------+        |
|   |  L2: 거버넌스 실행층 (IT STEERING / PMO)               |        |
|   |  -> RACI, 단계별 Gate Review, 예산배분, Risk Log       |        |
|   +--------------------+---------------------------------+        |
|                        | 2. Plan & Schedule                       |
|                        v                                          |
|   +------------------------------------------------------+        |
|   |  L3: 서비스 전달층 (개발·운영 조직 / Squad)            |        |
|   |  -> Agile Sprint, ITIL Change, SRE Runbook            |        |
|   +--------------------+---------------------------------+        |
|                        | 3. Measure & Monitor                     |
|                        v                                          |
|   +------------------------------------------------------+        |
|   |  L4: 측정/피드백층 (DASHBOARD / MEA)                   |        |
|   |  -> 실시간 KPI, 변칙 탐지, COBIT Maturity Scoring     |        |
|   +--------------------+---------------------------------+        |
|                        | 4. Review & Adjust                       |
|                        +--------------+                           |
|                                       |                           |
|   +-----------------------------------v----------------------+    |
|   |  L5: 지속적 개선 (CONTINUOUS IMPROVEMENT)              |    |
|   |  -> CAPA, Lessons Learned, Maturity Level Up            |    |
|   +------------------------------------------------------+    |
|                                                                    |
+--------------------------------------------------------------------+
   ↕ (좌우 통합)  COSO 내부통제 / ISO 31000 리스크 / ISO 27001 정보보안
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략 기획 (Strategy & Planning)** | 비즈니스·IT 정렬(Strategic Alignment), 로드맵 수립 | Porter 5-Forces, SWOT, **BMC(Business Model Canvas) 9블록, Ward-Peppard 방법론, TOGAF ADM(8단계)**, 시나리오 플래닝 |
| **거버넌스 체계 (Governance)** | 의사결정·통제·책임 구조, 정책·표준 관리 | **COBIT 2019 (40개 Governance/Management Objectives), ISO/IEC 38500 6원칙(D-책임, E-전략, A-획득, P-성과, C-준수, H-인적행위), Raci Matrix**, Three Lines of Defense (1선: 운영, 2선: 리스크/컴플, 3선: 내부감사) |
| **투자관리 (Portfolio Mgmt)** | IT 투자 프로젝트 우선순위, 자원배분, 수익률 관리 | **NPV(순현재가치), IRR(내부수익률), Payback Period, TCO(총소유비용), ROI/TVO**, Stage-Gate, MoSCoW 우선순위 |
| **성과측정 (Performance Mgmt)** | 전략목표 달성도 정량 모니터링 | **BSC 4관점(재무/고객/내부/학습성장), KPI(Leading/Lagging), KGI(Key Goal Indicator), CSF(Critical Success Factor)**, COBIT Maturity Level(0~5: 불완전->최적화) |
| **위험관리 (Risk & Compliance)** | 식별->평가->대응->모니터링 전과정 | **ISO 31000(Risk = L×I×C), NIST CSF 5함수(Identify-Protect-Detect-Respond-Recover)**, Heat Map, GRC 플랫폼(SAP GRC, ServiceNow GRC) |
| **운영관리 (Service Delivery)** | 일관된 서비스 품질 제공, SLA 관리 | **ITIL 4 34개 Practice, SIAM(다중공급자)**, SLA/OLa/UC(Underpinning Contract) 3층 구조 |
| **아키텍처 거버넌스 (EA)** | 기술·데이터·업무 표준화, 통합성 보장 | **TOGAF ADM(8단계: Preliminary->A~H), FEAF, Zachman 6×6**, Architecture Review Board |

**핵심 메커니즘 (CSF 연계 원리)**

1. **Balanced Scorecard (BSC, Kaplan & Norton 1992)**: 4관점(Financial, Customer, Internal Process, Learning & Growth)에 **Mission -> Strategy -> Objectives -> Measures -> Targets -> Initiatives** 로 분해(Cascade). IT-BSC는 **"비즈니스 가치 기여도"** 를 정량화하며, 예: 재무관점(ROI 25%), 고객관점(시스템 만족도 4.5/5), 내부관점(평균 장애복구 2시간), 학습관점(개발자당 교육 60시간).
2. **COBIT 2019 5도메인 40목표**: **EDM(Evaluate, Direct, Monitor) 5개 -> APO(Align, Plan, Organize) 14개 -> BAI(Build, Acquire, Implement) 11개 -> DSS(Deliver, Service, Support) 6개 -> MEA(Monitor, Evaluate, Assess) 4개**. 각 목표는 **Process Capability Level 0~5(ISO 15504 PAM)** 로 측정.
3. **ISO 38500 IT 거버넌스 6원칙**: **Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior** — 경영진(Board)이 반드시 수행해야 할 의사결정 사항을 정의.
4. **Stage-Gate 모델**: 프로젝트 단계별 **Gate Review(개념->기획->개발->시험->출시)** 를 통해 **Go/Kill/Hold/Recycle** 결정. 통계적으로 Stage-Gate 적용 시 프로젝트 성공률 60%->80% (Cooper, 2017).

- **📢 섹션 요약 비유**: IT 경영관리는 **"비행기의 자동조종장치(Autopilot)"** 와 같습니다. 파일럿(거버넌스위원회)이 방향·고도·속도(전략)를 정하면, 자동조종장치(거버넌스 시스템)가 실시간 계기(측정)와 기상(리스크)을 보면서 끊임없이 보정합니다. 기상악화(사업환경변화) 시 파일럿이 직접 개입(예외결의)합니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 관련 프레임워크는 **역할·관점·성숙도** 가 다르므로 **상호보완적 통합**이 필수다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **ISO 27001/31000** | **CMMI** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 | IT 서비스 운영 우수성 | 경영진의 IT 의사결정 원칙 | 정보보안·리스크 체계 | 프로세스 성숙도 |
| **관점** | 거버넌스+관리(2단) | 서비스 가치사슬(SVC) | 6원칙 | 리스크·통제 | 조직 프로세스 |
| **대상** | CIO·감사·이사회 | IT운영·서비스매니저 | 이사회·경영진 | CISO·컴플라이언스 | SW·제품개발조직 |
| **핵심 산출물** | 40 Governance/Management Objective, Capability Level | 34 Practice, 4D 모델(조직·정보·파트너·가치흐름·자격) | 6 Principle, 정책·지침 | ISMS, Risk Register | 5 Level, PA(Process Area) |
| **측정 방법** | Process Capability (0-5) | Maturity Model (1-5) | Audit, Compliance | KPI + Annex A 통제항목 | SCAMPI Appraisal |
| **연도/
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 471 / 800

<- **이전**: [470. IT 경영 관리 핵심 토픽 470번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/470_it_management_core_topic_470_exam_summary/)
**다음**: [472. IT 경영 관리 핵심 토픽 472번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/472_it_management_core_topic_472_exam_summary/) ->

---
