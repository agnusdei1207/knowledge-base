---
title: "IT Management Core Topic 710 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019 거버넌스 프레임워크, ITIL 4 서비스 가치 시스템(SVS), TOGAF ADM 아키텍처 개발 방법론, PMBOK 7th 프로젝트 관리, ISO 27001 ISMS 정보보안 체계를 통합적으로 운용하여 비즈니스 전략-정보기술 정렬(Business-IT Alignment)을 달성하는 종합 관리 체계이다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 프로젝트 성공률 28%->66% 향상(Standish Group 2020), IT 운영 비용 20-30% 절감, ROI 3-5배 개선, 정보보안 사고 대응시간 70% 단축, 컴플라이언스 위반 리스크 80% 감소 효과를 통한 기업가치 극대화.
> 3. **판단 포인트**: 중앙집중형 거버넌스(COBIT) vs 분산형 거버넌스(Federated) 선택, Agile/DevOps 도입 시 거버넌스 통제 수준 완화 vs 규제 준수 확보 간 균형, IT 투자 포트폴리오에서 Run-the-Business(70%) vs Grow-the-Business(20%) vs Transform-the-Business(10%) 배분 최적화가 핵심 의사결정 포인트.

---

## Ⅰ. 개요 및 필요성

정보기술이 기업의 핵심 경쟁력이 되면서 IT는 단순 비용센터(Cost Center)에서 전략적 비즈니스 파트너(Strategic Partner)로 전환되었다. 4차 산업혁명, 디지털 트랜스포메이션(DX), 클라우드 네이티브, AI/ML, 메타버스 등 기술 패러다임의 급격한 변화 속에서 기업은 **"IT를 어떻게 경영 자산으로 관리할 것인가"**라는 본질적 질문에 직면하고 있다.

기술사 시험에서 IT 경영 관리는 단순히 이론적 지식만이 아니라, 실무적 의사결정 능력을 평가하는 영역이다. 즉, "왜(Why)" 이 프레임워크를 도입해야 하는지, "어떻게(How)" 설계하고 운영할 것인지, "무엇을(What)" 우선순위로 추진할 것인지에 대한 통합적 사고력을 요구한다.

```text
+---------------------------------------------------------------------+
|              IT 경영 관리 5대 핵심 영역 통합 프레임워크                |
+---------------------------------------------------------------------+
|                                                                     |
|   [Business Strategy] ---> [IT Strategy] ---> [IT Governance]         |
|         ^                       |                    |              |
|         |                       v                    v              |
|   [Portfolio Mgmt] <---- [Enterprise Architecture] <---+              |
|         |                       |                    |              |
|         v                       v                    v              |
|   [Program/Project] ---> [Service Operations] ---> [Risk/Security]   |
|         |                       |                    |              |
|         +-----------------------+--------------------+              |
|                              |                                      |
|                              v                                      |
|                  [Continuous Improvement]                            |
|                  (PDCA + OODA Loop)                                 |
|                                                                     |
+---------------------------------------------------------------------+
```

기존의 IT 관리 방식은 부서별 사일로(Silo) 운영, 기술 중심 의사결정, 단기 ROI 추구, 사후 통제 중심이었다. 그러나 현재는 **가치 중심(Value-Driven)**, **플랫폼 기반(Platform-Based)**, **데이터 기반 의사결정(Data-Driven)**, **사전 예방 통제(Preventive Control)** 중심으로 패러다임이 전환되었다. 이를 위해 COBIT, ITIL, TOGAF, PMBOK, ISO 27001, ISO 20000, ISO 38500 등의 국제 표준 프레임워크를 통합적으로 활용하는 것이 필수적이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 오케스트라의 지휘자와 같다. 첼로(프로젝트), 바이올린(서비스), 트럼펫(보안), 드럼(아키텍처) 등 각 악기가 제 역할을 하면서도, 전체적으로 조화로운 symphony를 연주하도록 만드는 것이 IT 거버넌스의 본질이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019 거버넌스 시스템

COBIT(Control Objectives for Information and Related Technologies)은 ISACA에서 제정한 IT 거버넌스 및 관리 프레임워크의 de facto 표준이다. 2019 버전은 5대 도메인(EDM: Evaluate, Direct, Monitor / APO: Align, Plan, Organize / BAI: Build, Acquire, Implement / DSS: Deliver, Service, Support / MEA: Monitor, Evaluate, Assess) 체계를 40개 거버넌스/관리 목표로 재구성했다.

```text
+------------------------------------------------------------------+
|              COBIT 2019 거버넌스 시스템 구조                        |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------------------------------------------+          |
|  |   ① Governance System Principles (거버넌스 원칙)   |          |
|  |   - Each enterprise has different needs            |          |
|  |   - Enterprise goals cascade down                  |          |
|  |   - Apply single integrated framework              |          |
|  |   - Enable holistic approach                       |          |
|  |   - Distinguish governance from management         |          |
|  |   - Tailor to enterprise needs (Focus Area)        |          |
|  +----------------------------------------------------+          |
|                          |                                       |
|                          v                                       |
|  +----------------------------------------------------+          |
|  |   ② Governance Framework Components                 |          |
|  |   - Process / Organizational Structure / Principles |          |
|  |   - Information Flow / People/Skills/Competencies  |          |
|  |   - Policies/Procedures / Culture/Ethics/Behavior  |          |
|  |   - Services/Infrastructure/Applications/Technology |          |
|  +----------------------------------------------------+          |
|                          |                                       |
|                          v                                       |
|  +----------------------------------------------------+          |
|  |   ③ Governance and Management Objectives (40개)     |          |
|  |   EDM: 5개 / APO: 14개 / BAI: 11개 / DSS: 6개 / MEA: 4개 |  |
|  +----------------------------------------------------+          |
|                          |                                       |
|                          v                                       |
|  +----------------------------------------------------+          |
|  |   ④ Components: 7가지 (위 ② 참조)                  |          |
|  |   - 5가지 Process Capability Levels (0-5)           |          |
|  |   - Focus Areas (DEVOPS, RISK, SECURITY, COMPLIANCE)|          |
|  +----------------------------------------------------+          |
|                          |                                       |
|                          v                                       |
|  +----------------------------------------------------+          |
|  |   ⑤ Performance Management (CMMI 기반)             |          |
|  |   - Process Activity Rating (PA: 0-100%)           |          |
|  |   - Capability Level (0: Incomplete ~ 5: Optimizing)|          |
|  +----------------------------------------------------+          |
|                                                                  |
+------------------------------------------------------------------+
```

### 2) ITIL 4 서비스 가치 시스템(SVS)

ITIL v4는 2019년 AXELOS에서 발표된 최신 서비스 관리 프레임워크로, 2011년 ITIL v3의 26개 프로세스를 **34개 Practice**로 재구성하고, **Service Value Chain(SVC)** 활동을 통해 가치를 창출한다. 핵심은 **4가지 차원(Organizations & People / Information & Technology / Partners & Suppliers / Value Streams & Processes)**과 **7가지 guiding principles(Guiding Principles)**이다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Service Value Chain (SVC)** | 가치 창출 활동 체인 | Plan -> Engage -> Design & Transition -> Obtain/Build -> Deliver & Support -> Improve의 6개 활동이 입력(Opportunity/Demand/Value)을 가치 출력으로 전환 |
| **4 Dimensions (4P)** | 서비스 운영 환경 분석 | Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes 관점에서 holistic view 제공 |
| **7 Guiding Principles** | 의사결정 원칙 | Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize/Automate |
| **34 Practices** | 운영 실무 모범사례 | General(14): Continual Improvement, Change Enablement 등 / Service(17): Incident Mgmt, Problem Mgmt, Service Desk 등 / Technical(3): Deployment Mgmt, Infrastructure Mgmt, Software Dev Mgmt |
| **Governance & Practice** | 정책/표준 준수 | Risk management, Portfolio management, Workforce management, Architecture management, Measurement method |
| **Continual Improvement (CI)** | 지속적 개선 | Vision -> Where are we now? -> Where do we want to be? -> How do we get there? -> Did we get there? -> How do we keep the momentum? |

### 3) TOGAF Architecture Development Method (ADM)

TOGAF(The Open Group Architecture Framework)는 1995년 출시 이후 현재 10th Edition까지 발전한 EA(Enterprise Architecture) 구축 방법론이다. **ADM(Architecture Development Method)**는 8단계(Phase A~H) 사이클로 구성되며, **Architecture Content Framework**(메타모델, 산출물, 빌딩블록), **Architecture Capability Framework**(거버넌스 조직, 역할, 책임), **Architecture Repository**(아키텍처 자산 저장소)로 구성된다.

```text
+----------------------------------------------------------+
|            TOGAF ADM 8단계 사이클 (Iterative Cycle)        |
+----------------------------------------------------------+
|                                                          |
|              +----------------------+                    |
|         H --->| Architecture Change  |                    |
|              | Management           |                    |
|              +----------+-----------+                    |
|                         |                                |
|   +----- G --+  - F -+ | +- A -+                       |
|   |Implementation|Migration| |Vision|                      |
|   |Governance    |Plan  | |Phase |                       |
|   +-----+----+  +----+ | |  |                       |
|         |               | |  |                       |
|   +-----E --+  +- D -+ | |  |                       |
|   |Opportunity|Technology| |  |                       |
|   | & Solution|Architecture| |  |                       |
|   +-----+----+  +----+ | |  |                       |
|         |               | |  |                       |
|   +-----C --+  +- B -+ | |  |                       |
|   |Information|Business | |  |                       |
|   |Systems Arch|Architecture||  |                       |
|   +-----+----+  +----+ | |  |                       |
|         |               | |  |                       |
|         +---------------+-+  |                       |
|              ADM Cycle        |                       |
|              (반복적 수행)     |                       |
|                                                          |
|   ※ 각 단계 산출물: Architecture Vision, Business        |
|     Architecture, Data/Application/Technology Architecture|
|     Definition, Migration Plan, Implementation Governance|
|                                                          |
+----------------------------------------------------------+
```

### 4) PMBOK 7th & 애자일/하이브리드 프로젝트 관리

PMBOK(Project Management Body of Knowledge) 7th Edition은 2021년 PMI에서 발표되었으며, 6th의 5개 프로세스 그룹/10개 지식 영역을 **12개 Principle of Project Management** + **8 Performance Domains**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)으로 재편했다. **Agile Practice Guide**를 함께 제공하여 Predictive/Agile/Hybrid 접근법을 선택할 수 있는 가이드를 제시한다.

### 5) ISO/IEC 27001:2022 ISMS 정보보안 경영체계

ISO 27001:2022은 2022년 10월 개정판이 발표되었으며, 2013년 93개 통제 항목에서 **93개 통제 항목(4개 절/14개 통제군)**으로 재편되었다. ISMS(Information Security Management System)의 PDCA 사이클과 Annex A 통제 항목, Statement of Applicability(SoA), Risk Treatment Plan(RTP)을 통해 정보자산의 CIA(Confidentiality, Integrity, Availability)를 보장한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스/관리 통합 프레임워크 | 5개 도메인 40개 목표, 7개 컴포넌트, 5단계 Capability Level, Focus Area(DEVOPS, RISK, SECURITY) |
| **ITIL 4** | IT 서비스 관리 및 가치 창출 | Service Value Chain 6개 활동, 34개 Practice, 4 Dimension, 7 Guiding Principles, Continual Improvement |
| **TOGAF 10th** | EA 개발 및 거버넌스 | ADM 8단계 사이클(Phase A~H), Architecture Content Framework, ADM Guidelines, Reference Models |
| **PMBOK 7th** | 프로젝트 관리 표준 | 12 Principles, 8 Performance Domains, Agile/Hybrid/Predictive 접근법, Delivery Domain |
| **ISO 27001:2022** | 정보보안 경영시스템 | PDCA 사이클, 93개 Annex A 통제항목, 14개 통제군, Risk Assessment Methodology, SoA |

### 6) 핵심 정량 지표 및 측정 방법

IT 경영 관리의 효과성을 측정하기 위해 다음과 같은 핵심 KPI를 활용한다:
- **ROI (Return on Investment)**: (총 이익 - 총 비용) / 총 비용 × 100
- **NPV (Net Present Value)**: Σ(현금흐름 / (1+r)^t) - 초기 투자비 (r: 할인율, t: 기간)
- **IRR (Internal Rate of Return)**: NPV = 0이 되는 할인율 r
- **TCO (Total Cost of Ownership)**: 직접비용(하드웨어, 소프트웨어, 라이선스) + 간접비용(관리, 교육, 다운타임)
- **ITIL 핵심 KPI**: First Call Resolution(FCR), Mean Time To Restore(MTTR), Mean Time Between Failures(MTBF), SLA Compliance Rate
- **COBIT Maturity Level**: 0(Incomplete) ~ 5(Optimizing), Process Attribute Rating (N, P, A, L, W)
- **CSF/KPI**: Critical Success Factor와 Key Performance Indicator cascade (Enterprise Goal -> IT Goal -> Process Goal -> Metric)

- **📢 섹션 요약 비유**: IT 경영 관리 프레임워크는 마치 자동차의 내비게이션, 엔진, 브레이크, 안전벨트와 같다. COBIT는 전체 운전 매뉴얼, ITIL은 정기 점검 시스템, TOGAF는 도로 설계도, PMBOK은 여행 일정표, ISO 27001은 안전벨트/에어백이다. 이 모든 것이 통합되어야 안전한 운행이 가능하다.

---

## Ⅲ. 비교 및 연결

### 1) 주요 프레임워크 간 비교

| 구분 | COBIT 2019 | ITIL 4 | TOGAF 10th | PMBOK 7th | ISO 27001:2022 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주요 목적** | IT 거버넌스 및 관리 | IT 서비스 관리 | EA 개발 및 거버넌스 | 프로젝트 관리 표준 | 정보보안 경영체계 |
| **관리 대상** | IT 전반(Governance+Mgmt) | IT 서비스 운영 | 아키텍처 자산 | 프로젝트 | 정보자산 |
| **핵심 구조** | 5도메인/40목표 | SVC/34 Practice | ADM 8단계 | 12원칙/8도메인 | PDCA/Annex A 93개 |
| **성숙도 모델** | CMMI 0~5단계 | 4 Dimension Maturity | ADM Maturity | Organizational Agility | ISMS 인증 등급 |
| **인증 체계** | COBIT 2019 Certificate | ITIL Foundation/MP/SL | TOGAF Certified | PMP/PfMP/PMI-ACP | ISO 27001 LA/LA |
| **강점** | 거버넌스 통합, 컴플라이언스 | 서비스 가치 창출, Agile | EA 통합, 비즈니스 정렬 | 프로젝트 성공, Agile 통합 | 보안 통제, Risk 기반 |
| **약점** | 구현 복잡도, 운영 부담 | v3 대비 변화 큼 | ADM 단계별 시간 소요 | 프로세스 의존, 도구 미흡 | 통제항목 과다, 인증 비용
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 710 / 800

<- **이전**: [709. IT 경영 관리 핵심 토픽 709번 시험 요약](/studynote/12_it_management/05_security_compliance/709_it_management_core_topic_709_exam_summary/)
**다음**: [711. IT 경영 관리 핵심 토픽 711번 시험 요약](/studynote/12_it_management/05_security_compliance/711_it_management_core_topic_711_exam_summary/) ->

---
