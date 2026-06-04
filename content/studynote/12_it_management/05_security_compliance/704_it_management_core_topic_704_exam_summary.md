+++
title = "704. IT 경영 관리 핵심 토픽 704번 시험 요약 (IT Management Core Topic 704 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 704번은 **COBIT 2019(거버넌스/관리목표 40개), ITIL 4(34개 Practice), PMBOK 7th(12 Principle of Project Management), ISO/IEC 38500(거버넌스 6원칙)** 등 4대 글로벌 프레임워크를 통합적으로 이해하고, 이를 **정보화 전략 수립(ISP) -> EA(Enterprise Architecture) -> IT 거버넌스 -> 서비스 운영 -> 감리/평가**의 5단계 수명주기(SDLC) 위에 정렬하는 것이 핵심이다.
> 2. **가치**: 정량적 효과로는 **TCO 20~30% 절감, ROI 150~300% 달성, IT 인시던트 MTTR 60% 단축(평균 4.2시간->1.7시간), 변경 성공률 70%->92% 향상, 정보시스템 감리 지적사항 50% 감소** 효과가 보고되며, 정성적 효과로는 경영진과 IT 간의 **전략적 정렬(Strategic Alignment)**과 **가치 실현(Value Realization)**의 가시화가 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 중앙집중식 거버넌스 vs 분산형 페더레이션 모델, ② 빠른 속도(Agile) vs 통제(Governance), ③ 표준화(Standard) vs 유연성(Customization)**, 그리고 **④ Compliance 우선 vs Innovation 우선**이다. 기술사적 판단 기준은 **"CSF(Critical Success Factor) × KGI(Goal) × KPI(Indicator)"의 3축 매트릭스**로 측정 가능한 거버넌스 체계 설계 여부다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입에서 **"비즈니스 가치 실현(Business Value Realization)"**으로의 패러다임 전환은 IT 경영 관리 영역에 대한 새로운 접근을 요구한다. 과거 1990년대까지는 **"기술 중심의 IT 운영(Technology-Driven IT)"**이 주류였으나, 2000년대 들어 **사브린(Sambamurthy, 2003)**의 **디지털 옵션(Digital Options)** 이론과 **Henderson & Venkatraman(1993)**의 **SAM(Strategic Alignment Model)**이 제시되면서 **"전략적 정렬(Strategic Alignment)"**이 핵심 이슈로 부상했다. 2010년대 이후에는 **클라우드 전환, AI/ML 도입, 디지털 트랜스포메이션(DX)** 등 비즈니스와 IT의 경계가 사라지면서 **IT 거버넌스(COBIT 2019)**, **IT 서비스 관리(ITIL 4)**, **프로젝트 관리(PMBOK 7th)**, **정보보안 관리(ISO 27001)**가 4대 핵심 축으로 자리 잡았다.

기술사 시험 704번은 **"IT 경영관리"** 세부과목으로, 위 4대 프레임워크를 **ISP(정보화전략계획) 방법론** 위에서 통합적으로 이해하고, 실제 엔터프라이즈 환경에서 **거버넌스-관리-운영-평가** 4계층을 어떻게 설계·구현·감리하는지를 평가한다. 특히 2020년 이후 **클라우드 최적화(FinOps), DevSecOps, AI 윤리 거버넌스(AI Governance)**가 새로운 화두로 등장하면서 단순 이론 암기를 넘어 **"현실 적용 가능한 거버넌스 모델 설계"** 능력이 요구된다.

```text
+----------------------------------------------------------------------+
|          704번 IT 경영 관리 5단계 프레임워크 토폴로지 (Top-Down)        |
+----------------------------------------------------------------------+
|                                                                      |
|   +------------------------------------------------------------+    |
|   | [Level 1] 경영 전략 (Business Strategy)                      |    |
|   |  - 비전/미션 -> BSC 4관점(재무/고객/내부/학습성장) KPI         |    |
|   |  - CSF 도출 -> Porter's Value Chain, McKinsey 7S              |    |
|   +---------------------+--------------------------------------+    |
|                         | Strategic Alignment (SAM)                  |
|   +---------------------v--------------------------------------+    |
|   | [Level 2] 정보화 전략 (ISP) — 정보시스템 전략수립 방법론        |    |
|   |  - 현행분석(As-Is) -> To-Be 모델 -> 갭 분석(Gap Analysis)      |    |
|   |  - TOGAF ADM(Architecture Development Method) 9단계           |    |
|   |  - 정보화 투자 우선순위: AHP(Analytic Hierarchy Process)      |    |
|   +---------------------+--------------------------------------+    |
|                         | EA(Enterprise Architecture) 연계           |
|   +---------------------v--------------------------------------+    |
|   | [Level 3] IT 거버vernance & 관리 (COBIT 2019)                |    |
|   |  - 5개 도메인 / 40개 Governance & Management Objectives      |    |
|   |  - EDM(평가/지시/모니터) + 4개 도메인(APO/BAI/DSS/MEA)       |    |
|   |  - 7개 컴포넌트: 원칙/정책/프로세스/조직/문화/인력/정보      |    |
|   +---------------------+--------------------------------------+    |
|                         | Service Value Chain                         |
|   +---------------------v--------------------------------------+    |
|   | [Level 4] IT 서비스 운영 (ITIL 4)                            |    |
|   |  - 34개 Practice (14 General / 17 Service / 3 Technical)     |    |
|   |  - SVC: Plan->Engage->Design&Transition->Obtain/Build->          |    |
|   |         Deliver&Support->Improve                              |    |
|   |  - 4P: People/Product/Partner/Process                        |    |
|   +---------------------+--------------------------------------+    |
|                         | DevSecOps & FinOps                          |
|   +---------------------v--------------------------------------+    |
|   | [Level 5] 평가 및 감리 (Audit & Compliance)                  |    |
|   |  - 정보시스템 감리: 11개 감리영역, 5단계 수행절차              |    |
|   |  - ISACA COBIT Assessment, ISO 27001/20000 인증              |    |
|   |  - KPI/MPI 측정 -> BSC 연동 보고                              |    |
|   +------------------------------------------------------------+    |
|                                                                      |
+----------------------------------------------------------------------+
```

기존 IT 관리는 **사일로(Silo)형** 접근 — 즉, **개발팀, 운영팀, 보안팀, 기획팀**이 각자의 KPI로 움직이며 전체 최적화가 아닌 부분 최적화에 머물렀다. 704번은 이를 **"Value Stream"** 관점으로 통합하여, **요구사항(Requirement) -> 설계(Design) -> 구현(Build) -> 배포(Deploy) -> 운영(Operate) -> 개선(Improve)** 전 과정에서 거버넌스가 끊김 없이 흐르는 **"Continuous Governance"** 모델을 요구한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시계획과 같다**. 상부 계획(도시기본계획)이 없으면 빌딩(IT 시스템)들이 무질서하게 들어서고, 결과적으로 교통체증(인시던트), 무허가 건물(컴플라이언스 위반), 도시 빈부격차(Shadow IT)가 발생한다. 704번은 이 도시의 **토지이용계획(EA), 건축허가(거버넌스), 도로·상하수도(서비스), 그리고 감리(감사)**가 어떻게 통합 작동해야 하는지를 다룬다.

---

## Ⅱ. 아키텍처 및 핵심 원리

704번의 핵심은 **COBIT 2019의 Governance System**과 **ITIL 4의 Service Value System(SVS)**을 양대 축으로, 여기에 **PMBOK 7th의 12 Principle**과 **ISO 38500의 6원칙**을 얹는 것이다. 아래는 각 구성 요소의 역할과 기술적 동작 방식이다.

```text
+---------------------------------------------------------------------+
|         COBIT 2019 Governance System 통합 아키텍처 (40 Objectives)   |
+---------------------------------------------------------------------+
|                                                                      |
|  [지속적 개선 루프: Plan->Do->Check->Act + Capability Assessment]        |
|                                                                      |
|   +----------------------------------------------------------+      |
|   | ★ EDM Domain (Evaluate/Direct/Monitor) — 5개 Objectives |      |
|   |   EDM01 거버넌스 프레임워크 설정/유지                       |      |
|   |   EDM02 혜택 전달                                       |      |
|   |   EDM03 위험 최적화                                       |      |
|   |   EDM04 자원 최적화                                       |      |
|   |   EDM05 이해관계자 투명성                                  |      |
|   +---------------------+------------------------------------+      |
|                         |                                            |
|   +---------------------v------------------------------------+      |
|   | -> APO Domain (Align/Plan/Organize) — 14개 Objectives     |      |
|   |   APO01 관리 프레임워크 / APO02 전략 / APO03 엔터프라이즈 |      |
|   |   아키텍처 / APO04 혁신 / APO05 포트폴리오 / APO06 예산   |      |
|   |   / APO07 인적자원 / APO08 관계 / APO09 SLA /             |      |
|   |   APO10 공급업체 / APO11 품질 / APO12 위험 /              |      |
|   |   APO13 보안 / APO14 데이터                                |      |
|   +---------------------+------------------------------------+      |
|                         |                                            |
|   +---------------------v------------------------------------+      |
|   | -> BAI Domain (Build/Acquire/Implement) — 11개 Objectives |      |
|   |   BAI01 프로그램 / BAI02 요구사항 / BAI03 솔루션 /        |      |
|   |   BAI04 가용성/용량 / BAI05 변경 / BAI06 변경 수용 /      |      |
|   |   BAI07 도입 / BAI08 지식 / BAI09 자산 /                 |      |
|   |   BAI10 구성 / BAI11 프로젝트                              |      |
|   +---------------------+------------------------------------+      |
|                         |                                            |
|   +---------------------v------------------------------------+      |
|   | -> DSS Domain (Deliver/Service/Support) — 6개 Objectives  |      |
|   |   DSS01 운영 / DSS02 서비스 요청/인시던트 /               |      |
|   |   DSS03 문제 / DSS04 연속성 / DSS05 보안 서비스 /         |      |
|   |   DSS06 비즈니스 프로세스 통제                              |      |
|   +---------------------+------------------------------------+      |
|                         |                                            |
|   +---------------------v------------------------------------+      |
|   | -> MEA Domain (Monitor/Evaluate/Assess) — 4개 Objectives  |      |
|   |   MEA01 성과/컨formance 모니터 / MEA02 거버넌스 시스템 /   |      |
|   |   MEA03 외부요구 준수 / MEA04 IT 관리                        |      |
|   +----------------------------------------------------------+      |
|                                                                      |
|  [7 Components of Governance System]                                  |
|  +----------+----------+----------+----------+----------+            |
|  | Principles| Processes| Org.Struct| Information| People, |            |
|  |   (원칙)  |  (프로세스)|  (조직)  |  (정보)   | Skills.. |            |
|  +----------+----------+----------+----------+----------+            |
|                                                                      |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Governance System** | IT 거버넌스의 **단일 진실 공급원(Single Source of Truth)** | 5개 도메인 × 40개 목표. **Cascade Goals(목표 캐스케이드)** — Enterprise Goals 13개 -> Alignment Goals 13개 -> Management Goals 40개로 분해. **Capability Level 0~5** (PA 1.2~5.2)로 성숙도 측정. 7개 컴포넌트(원칙/정책/프레임워크/문화/인적자원/서비스/정보) |
| **ITIL 4 Service Value System (SVS)** | 서비스 제공 측의 **End-to-End 가치 흐름** | **Opportunity/Demand -> Value**: SVC 6단계(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) + 4D(조직/사람/정보/공급자) + **Guiding Principles 7개(Focus on value, Start where you are, Progress iteratively, etc.)**. **34 Practices**(일반 14, 서비스 17, 기술 3) |
| **PMBOK 7th (PMI)** | 프로젝트·프로그램·포트폴리오의 **Delivery Discipline** | **12 Principles of Project Management**(Stewardship, Team, Planning, etc.) + **8 Performance Domains**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) + Tailoring. **Predictive/Adaptive/Hybrid** 접근 |
| **ISO/IEC 38500 (IT Governance Standard)** | 이사회 수준 거버넌스의 **국제 표준** | **6 Principles**: 책임성(Responsibility), 전략(Strategy), 인수(Acquisition), 성과(Performance), 적합성(Conformance), 인간행태(Human Behavior). **3-Layer Model**: **Direct(Monitor) -> Manage -> Operate**. PDCA 사이클과 결합 |
| **TOGAF ADM (EA)** | 아키텍처 수준의 **거버넌스 청사진** | **9단계(Phase A->H + Requirements Management)** + **ADM Cycle Iteration**. **4 Architecture Domain**: Business/Data/Application/Technology. **Architecture Repository**(ABB/ABB/SBB/ABB). **ArchiMate 3.1** 표기법 |
| **정보시스템 감리법/감리원리** | 국내 컴플라이언스 거버넌스의 **법적 기반** | **11개 감리영역**(사업/계약/정보화전략/시스템구축/시스템운영/정보보호/성능/품질/법·제도/이행/최종성과). **시작->준비->실행->보고->사후관리** 5단계. **NIA/SO/AS** 인증 체계 |
| **Balanced Scorecard (BSC, Kaplan-Norton)** | IT 성과 측정의 **전략적 대시보드** | 4관점(재무/고객/내부프로세스/학습성장) × **Strategy Map(인과관계 맵)**. **Cause-and-Effect Logic**: 학습성장->프로세스->고객->재무의 가치 사슬. **Hoshin Kanri** 전략 전개 결합 |
| **CSF/KGI/KPI Framework** | 거버넌스 측정 가능한 **3축 메트릭** | **CSF(Critical Success Factor)**: "무엇이 성공에 필수인가". **KGI(Key Goal Indicator)**: "어디에 도달했나(결과)". **KPI(Key Performance Indicator)**: "어떻게 측정하나(선행/후행)". Rockwell/IBM 모델 |

**핵심 메커니즘 — Cascading Goals(목표 캐스케이드)**:
COBIT 2019의 가장 강력한 설계 원리는 **"Enterprise Goal -> Alignment Goal -> Management Goal"**의
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 704 / 800

<- **이전**: [703. IT 경영 관리 핵심 토픽 703번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/703_it_management_core_topic_703_exam_summary/)
**다음**: [705. IT 경영 관리 핵심 토픽 705번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/705_it_management_core_topic_705_exam_summary/) ->

---
