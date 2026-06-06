---
title: "IT Management Core Topic 517 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 같은 글로벌 거버넌스 프레임워크를 기반으로 IT 거버넌스(EGIT)-전략 정렬(SA)-포트폴리오 관리(PMO)-서비스 운영(ITSM)-정보 보안(ISMS) 5대 영역을 통합하여, 경영 목표와 IT 투자·운영·리스크를 End-to-End로 연결하는 **가치 중심(Value-Driven) 경영 체계**임.
> 2. **가치**: BAI(Balanced Architecture Investment) 관점에서 IT 투자 수익률(ROIT)을 15~25% 개선하고, SLA 기반 서비스 가용성 99.99% 달성, ISMS-P 인증을 통한 보안 사고 60% 감소, 프로젝트 성공률(PMI 기준) 30% -> 70% 향상 등 정량·정성적 효과를 동시에 창출.
> 3. **판단 포인트**: 중앙집중식(Centralized) vs 분산형(Distributed/Federated) 거버넌스 모델 선택 시 **규모(Business Scale)**, **규제 강도(Regulatory Pressure)**, **디지털 전환 속도(Agility Demand)**의 트레이드오프를 정량적으로 평가하고, COBIT의 7대 컴포넌트(Process/Organizational Structures/Information Flow/People/Skills/Competencies/Principles/Policies/Frameworks/Culture/Etc) 중 조직 문화(Culture)·역량(People)·원칙(Principles) 3대 비기술적 요소를 우선 성숙화해야 함.

---

## Ⅰ. 개요 및 필요성

정보기술의 전략적 가치가 IT 비용의 5~10배에 달하는 현대 비즈니스 환경에서, IT는 단순 비용센터(Cost Center)에서 **전략적 파트너(Strategic Partner)**이자 **가치 창출 엔진(Value Creation Engine)**으로 역할이 전환되었습니다. 기술사 시험에서 다루는 "IT 경영 관리"는 단순한 IT 운영을 넘어, 기업의 미션·비전·전략과 IT 간의 **전략적 정렬(Strategic Alignment)**을 체계적으로 관리하고, IT 투자·프로젝트·서비스·리스크·정보보호·컴플라이언스를 통합적으로 운영하는 학제적 경영 영역입니다.

과거 1990년대까지의 IT 관리는 **기술 중심(Tech-Driven)**, **부서별 단절(Silo)**, **사후 대응(Reactive)** 방식이었습니다. 그러나 SOA·Cloud·Big Data·AI·Zero-Trust가 보편화되고, ESG·공급망 보안(Supply Chain Security)·개인정보보호법(PIPA)·ISMS-P 같은 규제 환경이 강화되면서, **거버넌스 기반(Governance-Driven)**, **가치 중심(Value-Driven)**, **사전 예방(Proactive)**, **연속적 적응(Continuously Adaptive)** 패러다임으로의 전환이 필수불가결해졌습니다.

```text
+------------------------------------------------------------------+
|      IT 경영 관리의 5대 핵심 영역(5 Domains of IT Management)    |
|                                                                  |
|  +------------+   +------------+   +------------+               |
|  |  ① IT      |   |  ② IT      |   |  ③ IT      |               |
|  | Governance |◄--+  Strategy  |--►| Portfolio  |               |
|  | (COBIT,    |   | (SAMM,EA)  |   | (PMO,PPM)  |               |
|  |  ISO38500) |   |            |   |            |               |
|  +-----+------+   +-----+------+   +-----+------+               |
|        |                |                |                       |
|        |  +-------------+------------+    |                       |
|        |  |  Strategy Alignment(SA)  |    |                       |
|        |  |  - Henderson & Venkatraman|   |                       |
|        |  |  - SAM:Strategic         |    |                       |
|        |  |    Alignment Maturity    |    |                       |
|        |  +--------------------------+    |                       |
|        |                |                |                       |
|  +-----v------+   +-----v--------------v------+                |
|  |  ④ IT      |   |  ⑤ Information            |                |
|  | Service    |◄--+  Security & Risk         |                |
|  | Management |   | (ISMS-P, ISO27001,        |                |
|  | (ITIL4)    |   |  NIST CSF, Zero Trust)    |                |
|  +------------+   +---------------------------+                |
|                                                                  |
|  + ESG, Compliance(PIPA, GDPR), BCP/DR, FinOps, AI 거버넌스    |
+------------------------------------------------------------------+
        |
        v
   +--------------------------------------+
   |  비즈니스 가치(Business Value) 극대화 |
   |  - ROIT, EVA, ROI, TCO, NPV        |
   |  - KPI: SLA 99.99%, MTTR < 1h       |
   |  - NPS, CSAT, ESAT                 |
   +--------------------------------------+
```

기존 2000년대 ISMS(Information Security Management System) 단독 운영, ITIL v2 단계별(siloed) 운영, COBIT 4.1의 프로세스 중심 접근은 **"통합 거버넌스(Integrated Governance)"** 요구를 충족하지 못했습니다. COBIT 2019는 7대 컴포넌트와 40개 거버넌스/관리 목표(Governance & Management Objectives)로, ITIL 4는 34개 Practices와 Service Value System(SVS)으로 진화하여, 이를 **연결·통합(Connect & Integrate)**하는 것이 핵심입니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라 지휘자**와 같습니다. 바이올린(거버넌스), 첼로(전략), 트럼펫(운영), 팀파니(보안) 등 각 악기(영역) 모두가 최고의 연주자라도, 지휘자(거버넌스 프레임워크)가 없으면 카타클리즘한 소음(사일로, 중복 투자)만 나옵니다. COBIT가 악보, ITIL이 연주 기법, ISO 27001이 음정 정확도, ISO 38500이 무대 매너라면, 이 모든 것을 조화롭게 만드는 것이 진정한 IT 경영 관리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 영역은 **계층적·연계적 아키텍처**로 구성되며, 각 계층은 **상위 계층의 목표를 하위 계층의 실행으로 변환**하는 **Cascade(폭포) 모델**을 따릅니다. COBIT 2019의 핵심 원리는 **6가지 거버넌스 원칙(Governance System Principles)**입니다: (1) Every Enterprise Has Different Needs, (2) The Governance System Should Cover the Enterprise End-to-End, (3) Applying a Single Integrated Framework, (4) Enabling a Holistic Approach, (5) Distinguishing Governance From Management, (6) Tailoring the Governance System to Suit the Enterprise Needs.

```text
+----------------------------------------------------------------------+
|         COBIT 2019 기반 IT 거버넌스·관리 통합 아키텍처              |
|                                                                      |
|  <------ STAKEHOLDER NEEDS & GOALS ------>                            |
|  +----------------------------------------------------------+       |
|  |  Step 1: Stakeholder Drivers -> Step 2: Goals Cascade    |       |
|  |  (13 Enterprise Goals -> 13 Alignment Goals -> 40 G&M)   |       |
|  +-------------------------+--------------------------------+       |
|                            v                                         |
|  +----------------------------------------------------------+       |
|  |          7 Components of Governance System               |       |
|  |  +------------+  +------------+  +------------+         |       |
|  |  |1.Process   |  |2.Org       |  |3.Info Flow |         |       |
|  |  | (40 G&M)   |  | Structures |  |            |         |       |
|  |  +------------+  +------------+  +------------+         |       |
|  |  +------------+  +------------+  +------------+         |       |
|  |  |4.People &  |  |5.Policies  |  |6.Culture,  |         |       |
|  |  | Skills     |  | & Framewks |  | Ethics,    |         |       |
|  |  +------------+  +------------+  | Behavior   |         |       |
|  |  +------------+                  +------------+         |       |
|  |  |7.Services, |                                         |       |
|  |  | Infra, App |  <--- 7번째: Services, Infrastructure,   |       |
|  |  +------------+      Applications(Most newer)         |       |
|  +-------------------------+--------------------------------+       |
|                            v                                         |
|  +----------------------------------------------------------+       |
|  |    5 Focus Areas: EDM(거버넌스5) + 4 Management Domains |       |
|  |  EDM: Eval/Direct/Monitor (EDM01~05)                    |       |
|  |  APO(Align, Plan, Organize) 14개                        |       |
|  |  BAI(Build, Acquire, Implement) 11개                    |       |
|  |  DSS(Deliver, Service, Support) 6개                     |       |
|  |  MEA(Monitor, Evaluate, Assess) 4개                     |       |
|  +-------------------------+--------------------------------+       |
|                            v                                         |
|  +----------------------------------------------------------+       |
|  |       Goals Cascade Measurement & Target Setting        |       |
|  |  Process Capability: 0(Incomplete)~5(Optimizing)        |       |
|  |  Maturity: PAM(Process Assessment Model) ISO 33000      |       |
|  +----------------------------------------------------------+       |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① IT 거버넌스 시스템** (COBIT 2019) | 이사회~현업까지 End-to-End 거버넌스 체계 | 7대 컴포넌트 + 40 Governance & Management Objectives(GMO) + Goals Cascade(13 Enterprise Goals -> 13 Alignment Goals) + 7 Focus Areas + Design Factors(11개) 기반 맞춤형 설계 |
| **② IT 전략 정렬** (SAM, SAMM) | 비즈니스 전략과 IT 전략의 정렬도 측정·개선 | Henderson-Venkatraman Strategic Alignment Model(SA Model): Business Strategy ↔ IT Strategy ↔ Organization/Infrastructure ↔ IS/IT Processes. SAM(SAMM) 4개 영역(Communication/Competency/Governance/Partnership) × 3 Maturity Level, Strategic Fit 5단계(L0~L4) |
| **③ IT 포트폴리오 관리** (PMO, PPM) | IT 투자·프로젝트 우선순위 결정 및 성과 관리 | PMO 3유형(Supportive/Controlling/Directive) + 7단계 PPM 성숙도 + Stage-Gate(Go/Kill 결정) + NPV/IRR/Payback 분석 + EA(Enterprise Architecture) 기반 Application Portfolio Management(APM): TRM(Time, Risk, Maturity) 9셀 매트릭스 |
| **④ IT 서비스 관리** (ITIL 4) | IT 서비스의 End-to-End 가치 공학(Value Engineering) | SVS(Service Value System): Opportunity/Demand -> Value -> Guiding Principles(7개) -> Governance -> Practices(34개) -> SVC(Service Value Chain): Plan/Engage/Design&Transition/Obtain&Build/Deliver&Support/Improve + 4D 모델(Dimension): Organizations/People/Information/Technology/Partners/Value Streams |
| **⑤ 정보 보안·리스크 관리** (ISMS-P, ISO 27001) | CIA(Confidentiality, Integrity, Availability) + 거버넌스 리스크 | ISMS-P 인증(한국인터넷진흥원) 104개 통제항목 + ISO 27001:2022 93 Annex A 통제(4개 카테고리) + NIST CSF 2.0(Govern/Identify/Protect/Detect/Respond/Recover) + ISO 31000 리스크 관리 프로세스(Context->Risk Identification->Analysis->Evaluation->Treatment->Monitoring) |

**핵심 메커니즘 - Goals Cascade 작동 원리**:
1. **Step 1**: Stakeholder Needs -> Enterprise Goals(13개) — 예: "EG01 포트폴리오 경쟁 제품·서비스", "EG08 내부 비즈니스 기능의 최적화", "EG13 정보의 활용 극대화"
2. **Step 2**: Enterprise Goals -> Alignment Goals(13개) — 예: "AG01 I&T 준수 및 지원 지원", "AG12(IT) 직원 역량·기술·성장 관리"
3. **Step 3**: Alignment Goals -> Governance/Management Objectives(40개) — 예: "APO12 위험 관리", "BAI03 솔루션 관리", "DSS02 서비스 요청 및 사고 관리"
4. **Step 4**: GMO -> Process Practices(250+ Activities) — 실제 실행 가능한 산출물

**Process Capability vs Maturity 구분**:
- **Capability**(ISO 33020): 개별 프로세스 평가, 6단계(0~5) — PA(Process Attribute) 9개 기반
- **Maturity**: 조직 전체 성숙도, 5단계(1:Initial ~ 5:Optimizing) — PAM(Process Assessment Model) 기반
- Capability Profile(능력 프로파일) + Maturity Profile(성숙도 프로파일)을 병행 산출

- **📢 섹션 요약 비유**: COBIT의 Goals Cascade는 **건축물의 하중 전달 시스템**과 같습니다. 지붕의 적재하중(S stakeholder needs) -> 기둥(Enterprise Goals) -> 보(Alignment Goals) -> 슬래브(GMO) -> 철근(Process Activities)으로 전달되어야 건물이 무너지지 않습니다. 만약 중간에 하중이 끊기면(정렬 실패), 건물은 균열(투자 실패)이 가고 결국 붕괴(프로젝트 실패)합니다. 이 하중 전달을 검증하는 도구가 **Process Assessment Model(PAM)**입니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 프레임워크들은 서로 **중복·보완 관계**에 있으며, 실제 적용 시 **3-Framework Integration(COBIT + ITIL + ISO 27001/38500)**이 표준 패턴입니다.

| 구분 | **COBIT 2019** (거버넌스) | **ITIL 4** (서비스 관리) | **ISO/IEC 38500:2015** (거버넌스 표준) | **ISO/IEC 27001:2022** (보안) | **TOGAF 10** (EA) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 | IT 서비스 가치 창출 | IT 의사결정 거버넌스 | 정보보안경영체계 | EA 방법론·프레임워크 |
| **대상** | 이사회~전사(End-to-End) | IT 서비스 조직·고객 | 이사회·경영진 | CISO·정보보안 조직 | EA 아키텍트·CIO |
| **핵심 구조** | 40 GMO + 7 Components + 11 Design Factors | SVS + 34 Practices + SVC(6
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 517 / 800

<- **이전**: [516. IT 경영 관리 핵심 토픽 516번 시험 요약](/studynote/12_it_management/05_security_compliance/516_it_management_core_topic_516_exam_summary/)
**다음**: [518. IT 경영 관리 핵심 토픽 518번 시험 요약](/studynote/12_it_management/05_security_compliance/518_it_management_core_topic_518_exam_summary/) ->

---
