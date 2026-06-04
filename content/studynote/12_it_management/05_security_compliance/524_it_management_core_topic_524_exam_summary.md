+++
title = "524. IT 경영 관리 핵심 토픽 524번 시험 요약 (IT Management Core Topic 524 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019 거버넌스 프레임워크를 중심으로 ITIL 4 서비스 관리, ISO 27001 정보보안, ISO 22301 BCMS, PMBOK 7th 프로젝트 관리를 통합하여 **Governance(지휘) -> Management(관리) -> Operations(운영)** 3계층으로 전사 IT 자원의 가치를 극대화하는 체계이다.
> 2. **가치**: DORA(DevOps Research & Assessment) 메트릭 기준 Elite팀은 Lead Time 1시간 미만, Deploy Frequency 일 수회, Change Failure Rate 0~15%, MTTR 1시간 미만을 달성하며, COBIT 2019 적용 시 IT 투자 대비 ROI 평균 12~25% 향상, ISO 27001 인증 취득 후 보안 사고 60% 감소 효과가 보고되고 있다.
> 3. **판단 포인트**: **①** 거버넌스·관리·운영의 RACI 매트릭스 명확화, **②** Agile(반복적 가치 전달) vs Waterfall(단계별 문서화) 트레이드오프, **③** Zero Trust(미크로세그멘테이션·MFA·최소권한) vs 전통적 경계 보안(Perimeter-based) 선택, **④** Build vs Buy vs SaaS TCO 분석, **⑤** 클라우드·온프레미스 하이브리드 아키텍처의 책임 분담 모델(Shared Responsibility Model) 설계가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

현대 기업 환경에서 IT는 단순한 비용 센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 역할이 변화했다. McKinsey 보고서에 따르면 디지털 전환을 성공적으로 수행한 기업은 동종업계 대비 매출 성장률 2배, EBITDA 성장률 1.5배를 달성한다. 이러한 환경에서 정보관리기술사는 **IT 거버넌스 체계를 수립하고, IT 서비스 품질을 측정·개선하며, 정보자산을 보호**할 수 있는 종합적 역량을 입증해야 한다.

기존 IT 운영은 사일로(Silo) 형태로 부서별·시스템별로 독립 관리되어 **투자 중복(평균 25~35%), 데이터 불일치(Master Data 오류율 20~30%), 보안 취약점(미패치 시스템 비율 40% 이상)** 등의 문제가 지속적으로 발생했다. 이를 해결하기 위해 **1986년 ISACA의 COBIT**이 등장하여 IT 거버넌스 체계를 표준화하였고, 2019년 리비전에서는 40개의 Governance/Management Objectives를 통해 **End-to-End 거버넌스 모델**을 제시하였다.

```text
+---------------------------------------------------------------------+
|                IT 경영 관리 3계층 프레임워크 (3-Layer Model)           |
+---------------------------------------------------------------------+
|                                                                     |
|  +--------------------------------------------------------------+  |
|  | Layer 1: IT GOVERNANCE (지휘·의사결정 계층)                    |  |
|  |  • 의사결정 권한: 이사회(Board) -> CISO -> CIO -> IT Steering    |  |
|  |  • 프레임워크: COBIT 2019, ISO 38500, KING IV                 |  |
|  |  • 핵심 활동: Strategic Alignment, Value Delivery,            |  |
|  |              Risk Optimization, Resource Management,           |  |
|  |              Performance Measurement (5 focus areas)           |  |
|  +----------------------+---------------------------------------+  |
|                         | (RACI Matrix)                             |
|  +----------------------v---------------------------------------+  |
|  | Layer 2: IT MANAGEMENT (계획·제어 계층)                        |  |
|  |  • 프레임워크: ITIL 4 (SVS: Service Value System)             |  |
|  |  • 핵심 프로세스:                                          |  |
|  |     - Strategy: Strategy Management, Portfolio Management     |  |
|  |     - Design: Service Design, Architecture, Risk              |  |
|  |     - Transition: Change Enablement, Release Mgmt             |  |
|  |     - Operation: Incident, Problem, Service Request           |  |
|  |     - Continual Improvement: CSI Register                    |  |
|  |  • PMBOK 7th: 8 Performance Domains, 12 Principles           |  |
|  +----------------------+---------------------------------------+  |
|                         | (Operational Level Agreements)           |
|  +----------------------v---------------------------------------+  |
|  | Layer 3: IT OPERATIONS (실행·운영 계층)                       |  |
|  |  • Site Reliability Engineering (SRE): SLI/SLO/SLA            |  |
|  |  • DevOps: CI/CD, IaC(Terraform/Ansible), Observability       |  |
|  |  • AIOps: 이상탐지, 자동 근본원인분석(RCA)                    |  |
|  |  • DORA Metrics: Lead Time, Deploy Freq, CFR, MTTR            |  |
|  +--------------------------------------------------------------+  |
|                                                                     |
|  +--------------------------------------------------------------+  |
|  | Cross-Cutting Concerns (횡단 관심사)                          |  |
|  |  • 정보보안: ISO 27001/27002, NIST CSF 2.0, Zero Trust        |  |
|  |  • BCM/DR: ISO 22301, RTO/RPO 정의, BIA(Business Impact)     |  |
|  |  • 컴플라이언스: GDPR, 개인정보보호법, ISMS-P, PCI-DSS        |  |
|  |  • EA: TOGAF 10 ADM, Zachman Framework, FEAF                 |  |
|  +--------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

기존에는 ITIL v3의 **27개 프로세스를 5단계 Lifecycle**(Service Strategy -> Design -> Transition -> Operation -> Continual Improvement)로 관리했으나, 2019년 ITIL 4에서는 **34개 Practice와 4D 모델**(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes)로 전환하여 **Lean, Agile, DevOps**와의 융합을 강화했다. **정보관리기술사 시험은 이러한 프레임워크의 진화 과정을 명확히 이해하고, 실무 적용 시의 트레이드오프를 판단할 수 있는 역량을 평가**한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 도시의 **종합행정체계**와 같다. 시议会(이사회)가 도시 기본방침을 정하고(거버넌스), 시청 각 부서가 정책을 집행하며(매니지먼트), 현장 공무원과 시민이 도로·상하수도를 운영·유지보수(운영)한다. 이 세 계층이 단절되면 도로가 파손되어도 복구할 수 없고, 잘못된 정책은 도시 전체의 혼란을 야기한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **CobiT 2019의 Cascade Goals 메커니즘**을 통해 기업 목표(Enterprise Goals)와 IT 관련 목표(Alignment Goals), 지원 말단 목표(Management Objectives)가 연계된다. 각 단계에서 **Goal Cascade -> Enterprise Goal(13개) -> Alignment Goal(13개) -> Management Objective(40개) -> Process Activity**로 분해되며, 각 단계별로 **Primary(R), Secondary(S) Stakeholder가 매핑**된다.

```text
+---------------------------------------------------------------------+
|         COBIT 2019 Cascade Goals & ITIL 4 Value Chain 연동          |
+---------------------------------------------------------------------+
|                                                                     |
|  +--------------+      +--------------+      +--------------+     |
|  | Stakeholder  |------>| Enterprise   |------>|  Alignment   |     |
|  | Needs        |      |   Goals      |      |    Goals     |     |
|  |              |      |   (13 EA)    |      |   (13 AG)    |     |
|  | • Benefits   |      |              |      |              |     |
|  | • Risk       |      | EG01: Profit |      | AG01: I&T    |     |
|  | • Resources  |      | EG08:        |      | Compliance   |     |
|  | • Acceptance |      | Optimization |      | AG12: Managed|     |
|  +--------------+      | EG11:        |      |   Security   |     |
|                        | Compliance   |      |   Services   |     |
|                        +------+-------+      +------+-------+     |
|                               |                     |              |
|                               |  +------------------v------+       |
|                               |  | Management Objectives   |       |
|                               |  |      (40 MOs)           |       |
|                               |  |  EDM: 5 (Evaluate,      |       |
|                               |  |        Direct, Monitor) |       |
|                               |  |  APO: 14 (Align, Plan,  |       |
|                               |  |         Organize)       |       |
|                               |  |  BAI: 11 (Build,        |       |
|                               |  |         Acquire,        |       |
|                               |  |         Implement)      |       |
|                               |  |  DSS: 6 (Deliver,       |       |
|                               |  |        Service, Support)|       |
|                               |  |  MEA: 4 (Monitor,       |       |
|                               |  |        Evaluate, Assess)|       |
|                               |  +------------+------------+       |
|                               |               |                    |
|                               |  +------------v------------+       |
|                               |  | ITIL 4 Service Value    |       |
|                               |  | Chain (SVC) Activities  |       |
|                               |  |                         |       |
|                               |  | Plan->Engage->Design &    |       |
|                               |  | Transition->Obtain/Build |       |
|                               |  | ->Deliver & Support->     |       |
|                               |  | Improve                |       |
|                               |  +-------------------------+       |
|                               |                                     |
|  +----------------------------v---------------------------------+  |
|  | Continual Improvement: ①Vision -> ②Where are we now?          |  |
|  |                        ③Where do we want to be?             |  |
|  |                        ④How do we get there?                |  |
|  |                        ⑤Did we get there?                   |  |
|  |                        ⑥How do we keep momentum?            |  |
|  |   (Deming Cycle: Plan-Do-Check-Act)                          |  |
|  +--------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스 프레임워크 | 40개 Management Objective(EDM 5, APO 14, BAI 11, DSS 6, MEA 4), **Design Factors 11개**를 통한 조직 맞춤화, **7개 컴포넌트(Process, Organizational Structure, Information, People/Skills, Policies/Procedures, Culture/Ethics, Services/Applications/Infrastructure)** 정의, **Capability Level 0~5**(ISO/IEC 15504 PAM 기반) 측정 |
| **ITIL 4** | IT 서비스 관리 프레임워크 | **Service Value System(SVS)** 중심: Opportunity/Demand -> Value -> Value Streams, **34개 Practice** (General 14, Service 17, Technical 3), **4D Model**(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes), **Service Value Chain 6단계**(Plan->Engage->Design & Transition->Obtain/Build->Deliver & Support->Improve) |
| **ISO 27001:2022** | 정보보안 경영체계(ISMS) | **Annex A 93개 통제항목**(4개 영역: Organisational 37, People 8, Physical 14, Technological 34), **Plan-Do-Check-Act** 사이클, **Statement of Applicability(SoA)**, **위험평가 방법론**(ISO 27005 기반 자산 식별 -> 위협·취약점 -> 영향도/가능성 -> 위험 등급 산정) |
| **ISO 22301** | 사업연속성 경영체계(BCMS) | **BIA(Business Impact Analysis)** 통한 RTO(Recovery Time Objective)/RPO(Recovery Point Objective) 산정, 전략 선택(Hot/Warm/Cold Site, Active-Active, Pilot Light), **BCP/DRP** 수립 및 정기 모의훈련(연 1회 이상), **MBCO(Minimum Business Continuity Objective)** 정의 |
| **PMBOK 7th** | 프로젝트 관리 표준 | **8개 Performance Domain**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty), **12 Principles of Project Management**(Stewardship, Team, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability/Resilience, Change, Value, Behavioral), **6형 Deliverable** (Final, Phase, Stage, Sub-Component, Component, Deliverable) |
| **NIST CSF 2.0** | 사이버보안 프레임워크 | **6개 Function**(GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER) **22개 Category**, **Tier 1~4** 조직成熟도(Partial->Risk Informed->Repeatable->Adaptive), **Profile** 통한 현 상태 vs 목표 상태 비교 |
| **DORA Metrics** | DevOps 성과 측정 | 4대 지표: **Lead Time for Changes**(Commit->Production), **Deployment Frequency**(배포 빈도), **Change Failure Rate**(변경 실패율), **Mean Time to Restore(MTTR)**(장애 복구 시간), Elite/High/Medium/Low 4단계 분류 |

COBIT 2019의 **Capability Level 평가는 Process Attribute(PA 1.1~5.2) 9개**를 통해 측정된다. PA 1.1(Process Performance), PA 1.2(Work Product Management), PA 2.1(Process Management), PA 2.2(Work Product Management), PA 3.1(Process Definition), PA 3.2(Process Deployment), PA 4.1(Process Measurement), PA 4.2(Process Control), PA 5.1(Process Innovation), PA 5.2(Process Optimization). **Level 0(Incomplete) -> Level 1(Performed) -> Level 2(Managed) -> Level 3(Established) -> Level 4(Predictable) -> Level 5(Optimizing)**으로 구성되며, Level 3부터가 조직 표준 프로세스로 인정된다.

**ITIL 4의 Value Stream**은 특정 시나리오에서 가치를 창출하기 위해 수행되는 일련의 활동으로, 예시로 "신규 사용자 온보딩"이 **Plan -> Design & Transition(Access Provisioning, License Assignment) -> Obtain/Build(Account Creation) -> Deliver & Support(Welcome Kit, Training) -> Improve(피드백 수집)**의 6단계로 구성된다.

**Zero Trust Architecture(NIST SP 800-207)**는 "절대 신뢰하지 말고, 항상 검증하라(Never Trust, Always Verify)" 원칙으로, **①Identity(Identity Provider, MFA), ②Device(Endpoint Detection), ③Network(Software-Defined Perimeter, Micro-segmentation), ④Application(API Gateway, OAuth 2.0/OIDC), ⑤Data(DLP, Encryption, Tokenization)** 5개 영역에서 **Policy Engine(PE) + Policy Administrator(PA)**가 Policy Enforcement Point(PEP)에
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 524 / 800

<- **이전**: [523. IT 경영 관리 핵심 토픽 523번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/523_it_management_core_topic_523_exam_summary/)
**다음**: [525. IT 경영 관리 핵심 토픽 525번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/525_it_management_core_topic_525_exam_summary/) ->

---
