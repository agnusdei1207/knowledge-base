---
title: "767. IT 경영 관리 핵심 토픽 767번 시험 요약 (IT Management Core Topic 767 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 767. IT 경영 관리 핵심 토픽 767번 시험 요약 (IT Governance & Service Management)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019(40개 관리 목적/Governance & Management Objectives), ITIL 4(SVS 7가지 구성요소), ISO/IEC 20000, CMMI 등 글로벌 표준 프레임워크를 **EDF(Enterprise Digital Fabric)** 수준으로 통합하여 IT 의사결정 권한·책무·성과체계를 정렬하는 것
> 2. **가치**: 성숙도 2단계(Performed -> Managed) 도약 시 **MTTR 60% 단축**, IT 투자 ROI **20~35% 향상**, 서비스 가용성 SLA **99.9% -> 99.99%** 도달, 컴플라이언스 감사 대응 시간 **70% 절감**
> 3. **판단 포인트**: COBIT의 **Design Factors 11개** 기반 컨텍스트 튜닝, ITIL 4의 **34개 Practice** 중 조직 우선순위 선정, 거버넌스-관리-운영 3-Layer 분리, 그리고 **RACI 매트릭스**와 **Value Stream** 매핑 트레이드오프

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화로 인해 IT 부서는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 가치 창출의 핵심 엔진**으로 재정의되어야 한다. 전통적 IT 관리는 ITIL v3의 **Service Lifecycle**(Strategy->Design->Transition->Operation->CSI) 중심의 **프로세스 지향(Process-oriented)** 접근이었던 반면, 2019년 이후 등장한 **COBIT 2019**와 **ITIL 4**는 **Value Stream**·**Governance System**·**Agile/DevOps 통합**으로 패러다임을 전환시켰다. 특히 COBIT 2019는 **ISO/IEC 38500(거버넌스 표준)**과 **ISO/IEC 33000(프로세스 성숙도)**를 정렬하면서, 기술사 시험에서 **"거버넌스-관리-운영의 분리"**와 **"Design Factor 기반 컨텍스트 맞춤형 설계"**가 핵심 논점으로 부상했다.

```text
[전통적 IT 관리 (2000~2015)]              [모던 IT 거버넌스 (2019~현재)]
+---------------------+                    +----------------------------------+
|  COBIT 5 (Process)  |                    |      COBIT 2019 (40 Goals)       |
|  ITIL v3 (Lifecycle)|  ------ 진화 --->  |  ITIL 4 (SVS, 34 Practices)     |
|  ISO 20000:2011     |                    |  ISO/IEC 38500, 33000 정렬       |
|  ---- 실리콘(기능)   |                    |  ---- 가치(Value) 중심 전환      |
+---------------------+                    +----------------------------------+
        |                                            |
        v                                            v
  Process Silo 사고                          End-to-End Value Stream
  Compliance-Centric                         Business Outcome-Centric
  Reactive Monitoring                        Predictive & AI-Driven
```

**왜 필요한가?**

- **사이버보안 위협의 기하급수적 증가**: 2023년 랜섬웨어 피해액 42억 달러 돌파 -> **Zero Trust + GRC 통합** 필수
- **규제 강화**: 개인정보보호법, GDPR, DORA, AI Act -> **컴플라이언스 거버넌스** 내재화
- **클라우드·SaaS 종속성**: Shadow IT 증가로 **ITAM(IT Asset Management)** + **FinOps** 융합 필요
- **Agile/DevOps 도입**: 전통 ITIL Change Management와 **Continuous Delivery** 충돌 -> **ITIL 4의 7가지 Guiding Principle** 필요

- **📢 섹션 요약 비유**: 마치 **도시의 도시계획(Urban Planning)**처럼, IT 거버넌스는 "어떤 도로(IT 시스템)를 짓고, 어떤 교통규칙(프로세스)을 적용할 것인가"를 결정하는 **헌장(Constitution)**과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019의 5단 도메인 구조 (40개 Governance & Management Objectives)

```text
+----------------------------------------------------------------------+
|                  COBIT 2019 Core Model (5 Domains, 40 Objectives)    |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+      |
|  |  GOVERNANCE OBJECTIVES (5개) — Board/Executive 책임       |      |
|  |  EDM01 Governance Framework & Maintenance                 |      |
|  |  EDM02 Benefits Delivery                                  |      |
|  |  EDM03 Risk Optimization                                  |      |
|  |  EDM04 Resource Optimization                              |      |
|  |  EDM05 Stakeholder Transparency                           |      |
|  +------------------------------------------------------------+      |
|                          |  (RACI: Accountable)                      |
|  +----------------------+---------------------------------------+    |
|  |  MANAGEMENT OBJECTIVES (35개) — Mgmt/Operational 책임      |    |
|  |  +----------+ +----------+ +----------+ +----------+ +----+ |    |
|  |  | APO(14)  | | BAI(11)  | | DSS(6)   | | MEA(4)   | |(※) | |    |
|  |  | Align    | | Build    | | Deliver  | | Monitor  | |    | |    |
|  |  | Plan     | | Acquire  | | Service  | | Evaluate | |    | |    |
|  |  | Organize | | Implement| | Support  | | Assess   | |    | |    |
|  |  +----------+ +----------+ +----------+ +----------+ +----+ |    |
|  +------------------------------------------------------------+    |
|                                                                      |
|  ※ + 1 신규: 評(컴플라이언스 관련)  ->  Total 40 Management Goals    |
+----------------------------------------------------------------------+
         |                  |                    |
         v                  v                    v
   Design Factors 11개   Focus Area 커스텀    Goal Cascade
   (전략·위험·규모)      (DevOps, Security)   (Stakeholder->Goals)
```

### 2. ITIL 4 Service Value System (SVS)

```text
                  +---------------------------------+
                  |  Opportunity/Demand (ITIL 4)    |
                  +----------------+----------------+
                                   v
   +----------------------------------------------------------+
   |                                                          |
   |   +--------------------------------------------------+   |
   |   |              GUIDING PRINCIPLES (7)               |   |
   |   |  1) Focus on value  2) Start where you are        |   |
   |   |  3) Progress iteratively 4) Collaborate/promote   |   |
   |   |  5) Think/work holistically 6) Keep it simple     |   |
   |   |  7) Optimize & automate                           |   |
   |   +--------------------------------------------------+   |
   |                          v                                |
   |   +--------------------------------------------------+   |
   |   |              GOVERNANCE (3 Activities)            |   |
   |   |  • Evaluate   • Direct   • Monitor               |   |
   |   +--------------------------------------------------+   |
   |                          v                                |
   |   +--------------------------------------------------+   |
   |   |            SERVICE VALUE CHAIN (6)                |   |
   |   |  Plan -> Improve -> Engage -> Design&Transition     |   |
   |   |  -> Obtain/Build -> Deliver&Support                 |   |
   |   +--------------------------------------------------+   |
   |                          v                                |
   |   +--------------------------------------------------+   |
   |   |           PRACTICES (34개 — 3 General + 17        |   |
   |   |           Service + 14 Technical Management)      |   |
   |   |  Incident Mgmt, Change Enablement, Service Desk,  |   |
   |   |  Service Request, Problem, SLA, CSI, ...          |   |
   |   +--------------------------------------------------+   |
   |                          v                                |
   |                   VALUE (Customer Outcome)                 |
   +----------------------------------------------------------+
```

### 3. 구성 요소 매핑 테이블

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Goals Cascade** | 전략->목표 정렬 | 13개의 Enterprise Goals -> 13개의 Alignment Goals -> 40개 Governance/Management Objectives. **예: EG01(포트폴리오 경쟁우위)** -> **AG09(정보 기반 의사결정)** -> **EDM02(Benefits Delivery)** + **APO05(Portfolio Mgmt)** + **BAI01(Managed Programs)** |
| **Design Factors 11개** | 컨텍스트 튜닝 | ① Strategy ② Goals ③ Risk ④ Issues ⑤ Threat Landscape ⑥ Compliance ⑦ Role of IT ⑧ Sourcing Model ⑨ IT Methods ⑩ Tech Adoption ⑪ Enterprise Size. 각 DF별 우선순위 가중치(1~3) 부여 -> 40개 Objective 우선순위 자동 산출 |
| **ITIL 4 34 Practices** | 운영 실행 | General(3): Continual Improvement, Information Security, Relationship Mgmt. Service Mgmt(17): Incident, Problem, Change Enablement, Service Request, Service Desk, Service Level, Supplier, etc. Technical(14): Deployment Mgmt, Infrastructure/Platform, Software Dev, etc. |
| **ISO/IEC 20000-1:2018** | 인증 기반 | 10개 프로세스 그룹(Service Delivery 5 + Relationship 3 + Resolution 2 + Control 2) + ISO/IEC 20000-2 가이드라인. **PDCA + Plan-Do-Check-Act** 사이클. 인증 유효기간 3년, 감시심사 매년 1회, 재인증 심사 3년차 |
| **CMMI V2.0 (2018)** | 성숙도 평가 | 5 Level(Initiated->Managed->Defined->Quantitatively Managed->Optimizing). **5 Practice Area**: Doing, Managing, Enabling, Improving, Sustaining Habitual. 벤치마킹 표준 |
| **RACI Matrix** | 책임 정렬 | **R**(Responsible)·**A**(Accountable, 단 1명)·**C**(Consulted)·**I**(Informed). COBIT 2019의 모든 Activity에 기본 RACI 매핑 제공 |
| **Value Stream Mapping** | E2E 가치 흐름 | ITIL 4의 **Service Value Chain 6단계**를 Value Stream 단위로 재구성. **VSM Tool**(예: ValueStreamGuru, Kanbanize)으로 Bottleneck 식별 |
| **KGI/KPI/CSF** | 성과 측정 | **KGI**(Key Goal Indicator) = 결과, **KPI**(Key Performance Indicator) = 프로세스, **CSF**(Critical Success Factor) = 성공조건. PRM-T(Process Reference Model Tree)와 연계 |

### 4. 핵심 알고리즘·수식·파라미터

- **COBIT 목표 우선순위 산정식**:

  `Priority(Obj_i) = Σ (DF_j_weight × DF_j_relevance_to_Obj_i) for j=1..11`

  - 11개 DF별 가중치(1~3) × 각 Objective의 관련도(0/1/2) -> Top-N Governance Goal 선정
- **성숙도 측정 (ISO/IEC 33000 PAM)**:

  - 6단계(L0 Incomplete~L5 Optimizing) 또는 **Process Profile**(PA: Process Attribute 9개, Rating 0~4)
- **ITIL 4 4-Dimension Model**:
  - **Organizations & People · Information & Technology · Partners & Suppliers · Value Streams & Processes** — 모든 Practice는 4-Dimension 균형으로 설계
- **SLA 산식**:
  - **가용성 = (Total Time − Downtime) / Total Time × 100**
  - **MTTR = Σ(장애복구시간) / 장애건수**, **MTBF = Σ(가동시간) / 장애건수**

- **📢 섹션 요약 비유**: COBIT의 40개 목표는 **병원 진료 과목**(내과, 외과 등)이고, Design Factor는 **환자 상태**(연령, 기왕력)이며, ITIL Practice는 **실제 진료 절차**다. ISO 20000은 **병원 인증서**(JCI 인증 등)라고 보면 된다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO 20000-1:2018** | **CMMI V2.0 (2018)** | **ISO 38500 (2015)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 프레임워크 | IT 서비스 관리(SM) 우수 관행 | 서비스관리 인증 표준 | 프로세스/조직 성숙도 모델 | IT 거버넌스 원칙 표준 |
| **적용 범위** | 전체 IT(전략->운영) | 서비스 라이프사이클 | 서비스관리 시스템(SMS) | 소프트웨어·시스템 개발·서비스 | 이사회 거버넌스 |
| **구조** | 40 Goals + 11 DF | SVS + 34 Practices | 10 프로세스 그룹 | 5 PA × 5 Level | 6 Principles + 6 Model |
| **인증 가능** | ❌ (자격증: COBIT 2019 Foundation/Design/Implement) | ❌ (자격증: ITIL Foundation/MP/SL) | ✅ ISO 20000 인증 | ✅ CMMI Maturity Level | ❌ (원칙 표준) |
| **핵심 산출물** | Goals Cascade, Design Factor Matrix, RACI | Value Stream Map, Service Value Chain, 4D Model | SMS Policy, Statement of Applicability | Appraisal Result, Maturity Profile | Governance Charter, Decision Rights |
| **Agile/DevOps 대응** | Focus Area: DevOps (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 767 / 800

<- **이전**: [766. IT 경영 관리 핵심 토픽 766번 시험 요약](/studynote/12_it_management/05_security_compliance/766_it_management_core_topic_766_exam_summary/)
**다음**: [768. IT 경영 관리 핵심 토픽 768번 시험 요약](/studynote/12_it_management/05_security_compliance/768_it_management_core_topic_768_exam_summary/) ->

---
