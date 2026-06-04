+++
title = "495. IT 경영 관리 핵심 토픽 495번 시험 요약 (IT Management Core Topic 495 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 **COBIT 2019의 거버넌스 시스템(Governance System, 40개 GO/ME 목표)** + **ITIL 4의 34개 실무(Practices, 14개 일반 + 17개 서비스 + 3개 기술)** + **ISO 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 통해 **EDM(평가-지휘-모니터링) 사이클**과 **RACI 매트릭스**로 의사결정권과 실행 책임을 분리·통제하는 **3계층(Governance-Management-Operational) 통합 프레임워크**이다.
> 2. **가치**: ISACA/PMI 보고 기준 효과적 IT 거버넌스 적용 시 **IT 예산 20-30% 절감, 프로젝트 성공률 35%->75%(PMI 2021 Pulse), MTTR(Mean Time To Recover) 60% 단축, 사이버보안 컴플라이언스 비용 40% 절감, 가치 실현 시간(TTV: Time To Value) 2.4배 단축, ROI 1.8배 개선** 등 정량적 효과를 도출한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ①**거버넌스 과잉(Over-Governance) vs 민첩성(Agile)**, ②**중앙집중(CoE) vs 분산(Federated) 모델**, ③**CSF/KPI 선정의 5-7개 도메인 균형**(EDM·APO·BAI·DSS·MEA), ④**DevOps 환경에서 ITIL 4의 4가지 영향(SBTab/SW價值사슬) 적용**이며, 이를 위해 **COBIT 2019 Design Factor 11개(Enterprise Strategy, Goals, Risk Profile, etc.)**와 **Capability Level 0-5** 기반 점진적 채택이 필수이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX: Digital Transformation) 가속화로 기업의 IT는 비용센터(Cost Center)에서 **전략적 가치 창출 엔진(Value Driver)**으로 전환되었으나, 한국정보화진흥원(NIA)의 2023년 정보화 실태조사 결과 국내 대기업의 **62%가 IT-비즈니스 정렬(Alignment) 부재**, **48%가 이중 투자(Shadow IT)**로 인한 예산 낭비, **71%가 사이버 위협 대응체계 미비**를 호소하고 있다. IT 경영 관리는 이러한 문제를 해결하기 위해 **COBIT 2019, ITIL 4, ISO 38500, ISO 27001, PMBOK 7th, ISO 21500** 등 글로벌 프레임워크를 통합 적용하여 **거버넌스-관리-운영 3계층 모델**을 구현하는 학문이자 실무 영역이다.

특히 2020년 코로나19 이후 **원격근무(Remote Work) 환경 확산, SaaS 기반 업무 시스템 급증, AI/ML 기반 의사결정 자동화, 제로트러스트(Zero Trust) 보안 패러다임** 등 IT 운영 환경이 근본적으로 변화함에 따라, 전통적인 **ITIL v3 2011**의 26개 프로세스(Function-Process 중심)로는 한계가 드러나 **ITIL 4**의 **Service Value System(SVS)** + **4 Dimensions Model**(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes) + **Guiding Principles 7개**(Focus on Value, Start Where You Are, Progress Iteratively with Feedback, Collaborate and Promote Visibility, Think and Work Holistically, Keep It Simple and Practical, Optimize and Automate) 기반의 **민첩·통합·가치지향 거버넌스**가 요구된다.

```text
+---------------------------------------------------------------------+
|         IT 경영 관리 3계층 통합 프레임워크 (3-Layer Model)            |
+---------------------------------------------------------------------+
|                                                                     |
|  [Layer 1] 거버넌스 계층 (Governance Layer)                          |
|  +-------------------------------------------------------------+    |
|  |  Board / Steering Committee / IT Committee                  |    |
|  |  +- COBIT 2019 EDM Domain (5 GO)                            |    |
|  |  |   · GO 01: Governance Framework Setting                 |    |
|  |  |   · GO 02: Benefits Delivery                            |    |
|  |  |   · GO 03: Risk Optimization                            |    |
|  |  |   · GO 04: Resource Optimization                         |    |
|  |  |   · GO 05: Stakeholder Transparency                      |    |
|  |  +- ISO 38500 6 Principles (Responsibility, Strategy...)   |    |
|  +-------------------------------------------------------------+    |
|                              ^ Direction                            |
|                              v Accountability                       |
|  [Layer 2] 관리 계층 (Management Layer)                              |
|  +-------------------------------------------------------------+    |
|  |  CIO / IT Steering / PMO / Service Owner                    |    |
|  |  +- COBIT 2019 Management Domain (35 ME)                    |    |
|  |  |   APO (Align, Plan, Organize) 14개                       |    |
|  |  |   BAI (Build, Acquire, Implement) 11개                   |    |
|  |   DSS (Deliver, Service, Support) 6개                       |    |
|  |  |   MEA (Monitor, Evaluate, Assess) 4개                   |    |
|  |  +- ITIL 4 SVS Components (34 Practices)                    |    |
|  +-------------------------------------------------------------+    |
|                              ^ Operation                            |
|                              v Performance                          |
|  [Layer 3] 운영 계층 (Operational Layer)                             |
|  +-------------------------------------------------------------+    |
|  |  Service Desk / DevOps Team / SOC / SRE / DBA              |    |
|  |  +- ITIL 4 Service Value Chain (Plan->Engage->Design->         |    |
|  |  |  Transition->Obtain/Build->Deliver/Support)                |    |
|  |  +- ISO 20000-1:2018 (SMS 요구사항 10개 절)                |    |
|  +-------------------------------------------------------------+    |
|                                                                     |
|  ★ 핵심 흐름:  거버넌스 의사결정 -> 관리 실행/조율 -> 운영 수행       |
|              <- 성과보고/리스크피드백 <- 서비스지표/인시던트 <-         |
+---------------------------------------------------------------------+
```

기존 2000년대 **ITIL v2/v3**의 26개 프로세스(Function-Process 구조)가 **IT 부서 내부의 효율성** 위주의 폐쇄적(Inside-Out) 접근이었다면, **ITIL 4 + COBIT 2019 + ISO 38500** 기반의 현대 IT 경영 관리는 **외부 가치(Value, Outside-In)** 창출을 위해 **이해관계자(Stakeholder)·가치사슬(Value Stream)·SLA/SLM·경험지수(XI: eXperience Indicator)**를 통합 관리하는 **체계적·지속가능(Sustainable)·자동화(Automation)** 거버넌스로 패러다임이 전환되었다.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'운전 시스템(거버넌스) + 내비게이션(관리) + 엔진·바퀴·핸들(운영)'**이 한몸처럼 통합되어야 하는 것과 같다. 핸들(거버넌스) 없이 엔진(운영)만 가속하면 사고가 나고, 내비게이션(관리) 없이 핸들만 돌리면 목적지에 도달하지 못한다. **3계층이 실시간 데이터(예: 속도계·연료계·CCTV)로 연결**되어야 안전한 자율주행이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **COBIT 2019의 거버넌스 시스템 5개 컴포넌트(Components) + ITIL 4의 SVS + ISO 38500의 거버넌스 모델**의 3대 축을 통합한 **40개 목표(Goals) × 34개 실무(Practices) × 6원칙(Principles)** 매트릭스 기반의 의사결정-실행-모니터링 루프이다.

### 1. COBIT 2019 거버넌스 시스템 핵심 아키텍처

```text
+-----------------------------------------------------------------------+
|             COBIT 2019 Governance System (40 Goals 구조)              |
+-----------------------------------------------------------------------+
|                                                                       |
|  +------------------- Goal Cascade (연쇄) -------------------+       |
|  |  Stakeholder Needs -> Enterprise Goals (13) ->              |       |
|  |  Alignment Goals (13) -> Governance/Management Goals (40)  |       |
|  +------------------------------------------------------------+       |
|                                                                       |
|  +-- 5 Domains & 40 Objectives ------------------------------+       |
|  |  EDM  : Evaluate, Direct, Monitor        (GO 01~05)      |       |
|  |  APO  : Align, Plan, Organize            (APO 01~14)     |       |
|  |  BAI  : Build, Acquire, Implement        (BAI 01~11)     |       |
|  |  DSS  : Deliver, Service, Support        (DSS 01~06)     |       |
|  |  MEA  : Monitor, Evaluate, Assess        (MEA 01~04)     |       |
|  +------------------------------------------------------------+       |
|                                                                       |
|  +-- 7 Components of Governance System ----------------------+       |
|  |  ① Process              ② Organizational Structures       |       |
|  |  ③ Information Flows     ④ People, Skills and Competencies|       |
|  |  ⑤ Policies and Procedures ⑥ Culture, Ethics, Behavior    |       |
|  |  ⑦ Services, Infrastructure and Applications              |       |
|  +------------------------------------------------------------+       |
|                                                                       |
|  +-- 11 Design Factors (맞춤형 설계) -------------------------+      |
|  |  DF1: Enterprise Strategy (Acquisition/Custom/etc.)       |       |
|  |  DF2: Enterprise Goals (Portfolio/Quality/Growth...)     |       |
|  |  DF3: Risk Profile (Financial/Operational/Compliance)     |       |
|  |  DF4: I&T-related Issues (22 Typical Issues 매핑)         |       |
|  |  DF5: Threat Landscape (Cyber/Regulatory/Market)         |       |
|  |  DF6~11: Compliance, Role of IT, IT Sourcing, etc.        |       |
|  +------------------------------------------------------------+       |
|                                                                       |
|  +-- Capability/Maturity Level (0-5) -------------------------+      |
|  |  Level 0: Incomplete   Level 1: Initial   Level 2: Managed|       |
|  |  Level 3: Defined      Level 4: Quantitatively Managed     |       |
|  |  Level 5: Optimizing (CMMI v2.0 / PAM 4.0 연계)          |       |
|  +------------------------------------------------------------+       |
+-----------------------------------------------------------------------+
```

### 2. ITIL 4 Service Value System (SVS) 아키텍처

```text
+----------------------------------------------------------------------+
|            ITIL 4 Service Value System (SVS) 구조                    |
+----------------------------------------------------------------------+
|                                                                      |
|                +-----------------------------+                      |
|                |    Opportunity/Demand       |                      |
|                |    (기회/수요)              |                      |
|                +--------------+--------------+                      |
|                               v                                     |
|   +---------------------------------------------------+             |
|   |  Guiding Principles (7개 원칙)                    |             |
|   |  · Focus on Value · Start Where You Are          |             |
|   |  · Progress Iteratively with Feedback             |             |
|   |  · Collaborate and Promote Visibility             |             |
|   |  · Think and Work Holistically                    |             |
|   |  · Keep It Simple and Practical                   |             |
|   |  · Optimize and Automate                          |             |
|   +-------------------+-------------------------------+             |
|                       v                                              |
|   +-------------------------------------------------------+         |
|   |  Governance (거버넌스 조직·정책·위원회)              |         |
|   +-------------------------------------------------------+         |
|   |  Service Value Chain (6개 활동)                       |         |
|   |  +--------+ +--------+ +--------+                    |         |
|   |  |  Plan  |->| Engage |->| Design |                    |         |
|   |  +--------+ +--------+ +--------+                    |         |
|   |  +--------+ +---------+ +------------+               |         |
|   |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 495 / 800

<- **이전**: [494. IT 경영 관리 핵심 토픽 494번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/494_it_management_core_topic_494_exam_summary/)
**다음**: [496. IT 경영 관리 핵심 토픽 496번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/496_it_management_core_topic_496_exam_summary/) ->

---
