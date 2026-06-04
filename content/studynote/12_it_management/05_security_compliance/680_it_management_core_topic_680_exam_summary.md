+++
title = "680. IT 경영 관리 핵심 토픽 680번 시험 요약 (IT Management Core Topic 680 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019의 거버넌스 시스템(Governance System) 5개 도메인(EDM/APO/BAI/DSS/MEA) 40개 관리 목적(Management Objective)을 통해 조직의 가치 창출(Value Creation)을 IT로 실현하는 체계이며, 거버넌스-관리-운영 3계층 구조에서 의사결정 권한과 책임( 책임소재 : RACI )을 분리·연결하는 것이 핵심이다.
> 2. **가치**: COBIT 2019 도입 기업의 경우 IT 투자 대비 ROI가 평균 18~25% 향상되고, ITIL 4 기반 서비스 운영 적용 시 MTTR(평균 복구시간) 40~60% 단축, ISO/IEC 20000 인증 취득으로 SLA 미달률 70% 감소 등 정량적 효과가 입증되어 있으며, IT-BSC(정보화 성과측정체계) 연계 시 전략적 IT 정렬도(Strategic Alignment Maturity) 3단계 도달 가능하다.
> 3. **판단 포인트**: COBIT vs ITIL vs CMMI 중 어느 표준을 채택할지(거버넌스-서비스-개발 관점), 중앙집중형(Federal) vs 분산형(Decentralized) IT 조직 구조 선택, EA(엔터프라이즈 아키텍처) 기반 TOGAF vs FEAF 적용 여부, 그리고 클라우드·AI 도입 시 Dual Track Governance(기존+신기술 병행) 운영 방식의 Trade-off를 종합적으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원 역할(Back-office Utility)에서 비즈니스 핵심 가치 창출의 동인(Business Value Driver) 으로 그 위상이 변모함에 따라, IT 투자의 정당성 확보·리스크 통제·전략 정렬을 통합 관리할 수 있는 IT 경영 관리(Information Technology Management) 체계의 필요성이 대두되었다. 한국정보화진흥원(구 NIA)의 「정보시스템 감리」, 「정보기술아웃소싱 표준계약」, 그리고 공공부문 「정보화사업 성능·품질 평가」, 민간부문 COBIT·ITIL·ISO 27001 인증 확대가 그 사회적 요구를 반영한다.

기존 패러다임은 **IT 운영 효율성**(단위 시스템별 비용 절감) 중심이었으나, 신규 패러다임은 **IT 거버넌스**(전략적 의사결정·리스크·컴플라이언스·성과 통합) 중심으로 전환되었다. 또한 4차 산업혁명(AI, IoT, Blockchain, Cloud) 환경에서는 전통적 IT 관리 체계로 감당하기 어려운 **Digital Disruption 대응**, **사이버 레질리언스**, **데이터 거버넌스** 이슈가 부상하면서, COBIT 2019의 6원칙(Principle 1~6), 3체계(Governance/Management/Operations) 통합 모델이 사실상 글로벌 디팩토(De Facto) 표준으로 자리매김했다.

```text
+-----------------------------------------------------------------------------+
|           IT 경영 관리 3계층 통합 프레임워크 (3-Tier Integrated Model)        |
+-----------------------------------------------------------------------------+
|                                                                             |
|  +----------------------------------------------------------------------+  |
|  |  1계층: 거버넌스(Governance) — 이사회/CEO/CTO 의사결정                 |  |
|  |  +----------------------------------------------------------------+  |  |
|  |  | EDM : Evaluate, Direct, Monitor (5개 관리목적)                 |  |  |
|  |  |   +- EDM01 거버넌스 프레임워크 설정·유지                       |  |  |
|  |  |   +- EDM02 가치 제공(Value Delivery) 최적화                    |  |  |
|  |  |   +- EDM03 위험 최적화(Risk Optimization)                      |  |  |
|  |  |   +- EDM04 자원 최적화(Resource Optimization)                  |  |  |
|  |  |   +- EDM05 이해관계자 투명성(Stakeholder Transparency)         |  |  |
|  |  +----------------------------------------------------------------+  |  |
|  +----------------------------------------------------------------------+  |
|                                  v                                          |
|  +----------------------------------------------------------------------+  |
|  |  2계층: 관리(Management) — CIO/IT Director/PMO                       |  |
|  |  +----------------------------------------------------------------+  |  |
|  |  | APO : Align, Plan, Organize (14개) - 전략·계획·조직             |  |  |
|  |  | BAI : Build, Acquire, Implement (11개) - 구축·도입              |  |  |
|  |  | DSS : Deliver, Service, Support (6개) - 운영·지원               |  |  |
|  |  | MEA : Monitor, Evaluate, Assess (4개) - 모니터링·평가          |  |  |
|  |  +----------------------------------------------------------------+  |  |
|  +----------------------------------------------------------------------+  |
|                                  v                                          |
|  +----------------------------------------------------------------------+  |
|  |  3계층: 운영(Operations) — 실무팀/사용자                                |  |
|  |  +----------------------------------------------------------------+  |  |
|  |  |  · 일상적 IT 서비스 운영 (Help Desk, Incident Management)      |  |  |
|  |  |  · 변경 관리(Change Management) / 배포(Release)                |  |  |
|  |  |  · 인프라 운영(Infra Ops) / DevOps / SRE                       |  |  |
|  |  |  · 사용자 지원(End-User Support)                                |  |  |
|  |  +----------------------------------------------------------------+  |  |
|  +----------------------------------------------------------------------+  |
|                                                                             |
|  ---------------- 횡단(Transversal) 연결 고리 -----------------             |
|   RACI Matrix | KPI/CSF | Risk Register | Compliance Mapping | EA          |
+-----------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **배의 항해**와 같다. 거버넌스(이사회·선장)는 목적지·항로·안전을 결정하고, 관리(부선장·항해사)는 돛·속도·인원을 조율하며, 운영(선원·기관사)은 실제로 돛을 펴고 기관을 돌린다. 돛(COBIT·ITIL 표준)과 해도(EA·KPI) 없이는 아무리 좋은 선원도 항해할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **Governance System**과 **Governance Framework**를 분리 정의한 것이 가장 큰 특징이다. 시스템은 조직이 목표를 달성하기 위해 채택해야 할 6원칙(Principle)을, 프레임워크는 이를 실현하는 40개 관리 목적과 7개 컴포넌트(Component of Governance System)으로 구성된다. 7개 컴포넌트는 ① Process(프로세스), ② Organizational Structure(조직구조), ③ Information(정보), ④ People, Skills, Competencies(인적자원), ⑤ Policies and Procedures(정책·절차), ⑥ Culture, Ethics and Behavior(문화·윤리), ⑦ Services, Infrastructure and Applications(서비스·인프라·응용)이다.

ITIL 4(Service Value System, SVS)은 7가지 guiding principle(관점: Focus on value, Start where you are, Progress iteratively with feedback, Collaborate and promote visibility, Think and work holistically, Keep it simple and practical, Optimize and automate) 기반으로, **Service Value Chain**(Plan->Engage->Design & Transition->Obtain/Build->Deliver & Support->Improve)의 6개 활동(Value Chain Activity)으로 구성되어 IT 서비스의 End-to-End 가치를 관리한다.

```text
+---------------------------------------------------------------------------+
|              COBIT 2019 + ITIL 4 통합 거버넌스-서비스 흐름도              |
+---------------------------------------------------------------------------+
|                                                                           |
|  [전략적 목표] --+                                                        |
|   · 비용절감     |                                                        |
|   · 경쟁우위     |   +-----------------+                                  |
|   · 규범준수     +--->|  Cascade 단계   |                                  |
|   · 고객만족     |   | (위계적 연계)    |                                  |
|                  |   +--------+--------+                                  |
|                  v            v                                           |
|   +---------------------+  +---------------------+                       |
|   | Enterprise Goal(13) |  | Alignment Goal(13)  |                       |
|   | : 사업 목표          |  | : IT 정렬 목표      |                       |
|   +----------+----------+  +----------+----------+                       |
|              |  Goals Cascade 매핑      |                                  |
|              v                         v                                   |
|   +---------------------------------------------+                          |
|   |       Management Objective (40)            |                          |
|   |  EDM(5) + APO(14) + BAI(11) + DSS(6) + MEA(4)                       |
|   +------------------+--------------------------+                         |
|                      |                                                    |
|        +-------------+-------------+                                      |
|        v             v             v                                      |
|   +--------+    +--------+    +--------+                                  |
|   | Process|    |People  |    |  Info  |  <--- 7 Components of Gov Sys     |
|   |  (40)  |    | Skill  |    | Flow   |                                  |
|   +----+---+    +----+---+    +----+---+                                  |
|        +-------------+-------------+                                      |
|                      v                                                    |
|        +-----------------------------+                                    |
|        |     Capability/Maturity    |   Process Assessment Model (PAM)     |
|        |   Level 0-5 (ISO 33020)     |   · Level 0 : Incomplete           |
|        |   · Level 3 : Established   |   · Level 1 : Initial              |
|        |   · Level 4 : Predictable   |   · Level 2 : Managed              |
|        |   · Level 5 : Optimizing    |   · Level 3 : Defined              |
|        +-----------------------------+   · Level 4 : Quantitatively Mgmt  |
|                                            · Level 5 : Optimizing          |
|                                                                           |
|  ------------ ITIL 4 Service Value Chain (SVC) ------------                |
|   Plan -> Engage -> Design & Transition -> Obtain/Build -> Deliver & Support  |
|                                          ↘ Improve ↗                       |
+---------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·최고위층 거버넌스 의사결정 | EDM01~05로 구분, 전략적 의사결정·리스크·자원·투명성·가치 제공 5영역의 거버넌스 메커니즘 수행, COBIT 2019에서 신규로 강조된 영역 |
| **APO (Align, Plan, Organize)** | IT 전략·계획·조직 정렬 | APO01(관리 프레임워크), APO02(전략), APO04(혁신), APO12(리스크), APO13(보안) 등 14개 관리목적, IT-BSC·IT Portfolio·EA 연계의 핵심 계층 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축·도입·통합 | BAI01(프로그램), BAI02(요구사항), BAI03(솔루션), BAI05(조직변화), BAI11(프로젝트) 등 11개, SDLC·Agile·DevOps 전반의 관리체계 포함 |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영·지원 | DSS01(운영), DSS02(서비스 요청·사고), DSS03(문제), DSS04(연속성), DSS05(보안운영), DSS06(비즈니스 통제) 6개, ITIL 4와 가장 밀접한 영역 |
| **MEA (Monitor, Evaluate, Assess)** | 성과 모니터링·평가·감리 | MEA01(성과·준수 모니터링), MEA02(내부 통제), MEA03(외부 요구사항 준수), MEA04(감사) 4개, 내부감사·외부감사·컴플라이언스의 통합 체계 |
| **RACI Matrix** | 책임·역할 분담 매트릭스 | Responsible(수행), Accountable(책임/의사결정), Consulted(자문), Informed(통보) 4분면으로 정의, IT 프로젝트·운영의 책임소재 명확화 필수 도구 |
| **Process Capability (PAM)** | 프로세스 성숙도 측정 | ISO/IEC 33020 기반 0~5 단계(6단계) 평가, ISO 15504 SPICE(Software Process Improvement and Capability dEtermination) 방법론 적용 |

핵심 원리로는 **① Goals Cascade(목표 위계)**, **② Component Variants(컴포넌트 변형 적용)**, **③ Focus Areas(중점 영역: DevOps, Risk, Security, Privacy)**, **④ Design Factor(설계 인자 11개)**가 있다. Design Factor에는 기업전략, 거버넌스 목표, IT 관련 문제, 위험도, 컴플라이언스 요구, IT 역할, 정보기술 채택 전략, IT 구현 방법론, 기술 채택 전략, 조직 규모, 외부 환경이 포함된다. PAM(Process Assessment Model)은 ISO 33000 시리즈 기반 9단계(PA 1.1~PA 5.2) 세분화 평가 체계를 채택한다.

- **📢 섹션 요약 비유**: COBIT의 5개 도메인은 마치 **오케스트라**와 같다. EDM(지휘자·악장)이 전체 음악의 흐름과 방향을 결정하고, APO(작곡가·편곡자)가 악보를 쓰며, BAI(악기 제작자·연주자)가 음악을 만들어내고, DSS(무대감독·음향감독)가 청중에게 전달하며, MEA(평론가·청취자 평가)가 비평과 개선을 제안한다. 7개 컴포넌트는 악기·악보·무대·청중석 같은 필수 요소들이다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 표준·프레임워크는 관점·범위·적용 대상에 따라 명확한 차이를 보인다. **COBIT**은
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 680 / 800

<- **이전**: [679. IT 경영 관리 핵심 토픽 679번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/679_it_management_core_topic_679_exam_summary/)
**다음**: [681. IT 경영 관리 핵심 토픽 681번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/681_it_management_core_topic_681_exam_summary/) ->

---
