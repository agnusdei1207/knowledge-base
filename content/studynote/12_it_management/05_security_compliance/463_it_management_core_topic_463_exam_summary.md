---
title: "IT Management Core Topic 463 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 사슬(SVC), ISO 27001/22301 보안·연속성 표준을 통합하여 IT 투자 대비 비즈니스 가치(Value Realization)를 극대화하는 체계적 프레임워크임.
> 2. **가치**: 정량적으로는 TCO 20~30% 절감, ROI 15~25% 향상, MTTR 50% 단축, 정성적으로는 의사결정 투명성, 리스크 가시화, 규제 준수(Compliance) 확보를 통해 경영 신뢰도(Trust)를 제고함.
> 3. **판단 포인트**: 거버넌스(Governance) vs 관리(Management) 경계, Build vs Run 예산 배분(통상 30:70), 중앙화(Centralized) vs 분권화(Federated) 거버넌스 모델 선택, 그리고 BSC·KPI·CSF의 인과관계(Causal Chain) 설계가 핵심 의사결정 변수임.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 시대에 IT는 더 이상 단순한 비용 센터(Cost Center)가 아닌 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 자리매김했다. 그러나 한국 정보화진흥원의 조사에 따르면 국내大中型企業의 약 62%가 "IT 투자의 비즈니스 성과 측정이 어렵다"고 응답하며, Gartner의 IT Key Metrics Data에서도 전 세계 CIO의 71%가 "IT-Business Alignment 실패"를 최우선 과제로 꼽고 있다.

기존 IT 운영은 ITIL v2/v3의 프로세스 중심(PBS, Process-Based Service) 관리에 머물렀으나, 클라우드·DevOps·AI 워크로드의 등장으로 인해 **서비스 가치 사슬(Service Value Chain, SVC)** 중심의 통합 거버넌스가 필수적으로 요구된다. IT 경영 관리(Information Technology Management, 주제 463번)는 COBIT 2019의 거버넌스/관리 목적(Governance/Management Objectives), ITIL 4의 34개 실무 가이드(Practice), ISO/IEC 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 통합하여, IT 의사결정의 **효율성(Efficiency)·효과성(Effectiveness)·준거성(Conformance)**를 동시에 달성하는 메타-프레임워크이다.

특히 2024년 이후 주목받는 **NIS2(Network and Information Security Directive 2)**, **DORA(Digital Operational Resilience Act)**, 그리고 한국 **전자금융거래법 개정안**은 IT 거버넌스를 단순 모범 사례(Best Practice)에서 **법정 의무(Legal Obligation)**로 격상시켰다. 따라서 기술사 응시자는 단일 프레임워크 암기가 아닌, **상호 참조(Cross-Reference)** 능력과 **맥락 기반 의사결정(Context-Driven Decision)** 능력을 갖춰야 한다.

```text
+---------------------------------------------------------------------+
|          IT 경영 관리 통합 프레임워크 (Topic 463)                      |
+---------------------------------------------------------------------+
|                                                                     |
|  [ 전략 계층 ]                                                      |
|   +------------------+  +------------------+  +----------------+   |
|   | ISO/IEC 38500    |  |  COBIT 2019      |  |  BSC/KPI 체계  |   |
|   |  (6원칙)         |◄-+  (40 Governance  |◄-+  (CSF->KPI->    |   |
|   |                  |  |   & Mgmt Obj.)   |  |   KGI)         |   |
|   +--------+---------+  +---------+--------+  +--------+-------+   |
|            |                      |                     |          |
|            v                      v                     v          |
|  +--------------------------------------------------------------+  |
|  |      서비스 가치 사슬 (SVC) - ITIL 4 Service Value Chain       |  |
|  |  Plan -> Engage -> Design & Transition -> Obtain/Build ->        |  |
|  |           Deliver & Support -> Improve                        |  |
|  +--------------------------------------------------------------+  |
|            |                      |                     |          |
|            v                      v                     v          |
|  +------------------+  +------------------+  +----------------+   |
|  |  ISO 27001       |  |  ISO 22301       |  |  ISO 20000     |   |
|  |  (정보보안 ISMS) |  |  (BCP/DR)        |  |  (서비스관리)  |   |
|  +------------------+  +------------------+  +----------------+   |
|            |                      |                     |          |
|            +----------------------+---------------------+          |
|                                   v                                |
|  +--------------------------------------------------------------+  |
|  |        운영 계층: CMDB -> AIOps -> SRE -> FinOps                 |  |
|  |   (Configuration -> Observability -> Reliability -> Cost)        |  |
|  +--------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

기존 패러다임(ITIL v3의 26개 프로세스 단순 매핑)과 신규 패러다임(ITIL 4 + COBIT 2019 + Agile/DevOps 통합 거버넌스)의 핵심 차이는 다음과 같다. v3는 **프로세스 -> 활동 -> 절차(Process->Activity->Procedure)**의 위계적 구조로 경직성이 컸으나, v4는 **원리(Guiding Principles) 7개**, **4차원 모델(Four Dimensions: 조직·사람·정보·파트너·가치흐름·기술)**, **SVC**를 통해 **컨텍스트-드리븐** 의사결정을 지원한다. 결과적으로 사고 대응 시간이 평균 40% 단축되고, 변경 성공률(Change Success Rate)이 70%->92%로 향상된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획(Urban Planning)**과 같다. 도로(네트워크)·상하수도(데이터)·공원(보안)·건축물(애플리케이션)을 각 부서가 따로 짓는 게 아니라, 도시总体规划(Master Plan) 아래 통합 설계하고, 교통 흐름(서비스 흐름)을 실시간으로 관제하며, 지진·홍수(리스크)에 대비한 내진 설계(BCP)를 반드시 포함하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **PDCA(Plan-Do-Check-Act) -> EDM(evaluate, direct, monitor) -> APO-BAI-DSS-MEA(Align, Plan, Organize; Build, Acquire, Implement; Deliver, Service, Support; Monitor, Evaluate, Assess)**의 중첩 루프 구조로 이해해야 한다. COBIT 2019의 40개 목적(Objective)은 상위 5개 거버넌스 목적(EDM01~05)과 35개 관리 목적(APO01~14, BAI01~11, DSS01~06, MEA01~04)로 구성되며, 각 목적은 **Process Capability**(0~5단계, PAM v3.1 기반)와 **Risk/Issue/Benefit Realization**을 통해 측정된다.

```text
+------------------------------------------------------------------+
|        COBIT 2019 거버넌스-관리 연계 (Cascade Mechanism)          |
+------------------------------------------------------------------+
|                                                                  |
|  [Stakeholder Drivers & Concerns]                                |
|         |   Benefits Realization  |  Risk Optimization          |
|         |   Resource Optimization |  Transparency                |
|         v                        v                              |
|  +----------------------------------------------------------+   |
|  |                 GOAL CASCADE (목표 연쇄)                  |   |
|  |  Enterprise Goals (13) -> Alignment Goals (13) ->          |   |
|  |  -> Governance/Management Objectives (40)                  |   |
|  +----------------------------------------------------------+   |
|           |                    |                    |            |
|           v                    v                    v            |
|  +--------------+  +------------------+  +------------------+  |
|  | EDM 계층     |  |  APO/BAI/DSS/MEA |  | 구성요소         |  |
|  | (거버넌스)   |  |  (관리 35개)     |  | (Process/People  |  |
|  |              |  |                  |  |  /Tech/Info)     |  |
|  +--------------+  +------------------+  +------------------+  |
|           |                    |                    |            |
|           +--------------------+--------------------+            |
|                                v                                 |
|  +----------------------------------------------------------+   |
|  |        측정 체계: KPI + KGI + CSF + KSF                   |   |
|  |   (예: SLA 99.95% = KGI, MTTR 30분 = KPI)                |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·IT 전략위원회(IT Steering Committee) 차원의 거버넌스 | EDM01(프레임워크 유지), EDM02(이익 실현), EDM03(리스크 최적화), EDM04(자원 최적화), EDM05(투명성 확보). 연 4회 이상 의사결정 사이클 운영 |
| **APO (Align, Plan, Organize)** | IT 전략-비즈니스 정렬, 거버넌스 시스템 설계, 예산·포트폴리오 관리 | APO05(포트폴리오 관리 - Stage-Gate), APO12(리스크 관리 - ISO 31000 연계), APO13(보안 관리 - ISMS), APO14(데이터 거버넌스 - DAMA-DMBOK) |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·구축·전환, 변경 관리 | BAI03(변경 관리 - CAB 승인), BAI06(배포 - Blue/Green, Canary), BAI10(구성 관리 - CMDB, ServiceNow CMDB) |
| **DSS (Deliver, Service, Support)** | 서비스 운영·지원·사고·문제 관리 | DSS02(사고 관리 - P1은 15분 내 대응), DSS03(문제 관리 - Known Error DB), DSS04(연속성 관리 - RTO/RPO), DSS05(보안 서비스) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정·내부 통제·규제 준수 | MEA01(성과·준거성 모니터링 - 내부감사), MEA02(내부 통제 시스템 - SOX 404), MEA03(규제 준수 - ISO 38500, NIS2), MEA04(자체평가) |

**핵심 원리 #1 - BSC 4관점 인과모델**: 재무(F) -> 고객(C) -> 내부 프로세스(I) -> 학습·성장(L)의 인과 체인(Chain of Cause and Effect)을 IT에 적용. 예: "DevOps 도구 투자(L)" -> "배포 빈도 4배^(I)" -> "Time-to-Market 60%v(C)" -> "매출 12%^(F)".

**핵심 원리 #2 - RACI 매트릭스**: Responsible(수행), Accountable(책임, 단 1인), Consulted(자문), Informed(통보)의 역할 구분. COBIT 2019는 각 관리 목적별로 RACI 차트를 기본 제공하며, 이중 보고선(Dotted Line)을 통해 IT-Business 간 매트릭스 조직을 지원한다.

**핵심 원리 #3 - 7단 인에이블러(Enabler) 모델**: People, Process, Technology, Information, Principles/Policies/Frameworks, Culture/Ethics/Behavior, Services/Infrastructure/Applications. 모든 거버넌스 결정은 최소 3개 인에이블러에 영향을 미치는지 평가해야 한다.

**핵심 원리 #4 - 워크플로우 자동화**: Power Automate, ServiceNow Flow Designer, Jira Service Management, Camunda 8 등 BPMN 2.0 기반 도구로 사고 대응(Service Request Fulfillment)·승인·변경 관리 SLA를 자동화. 평균 MTTR 50% 단축 효과.

**핵심 원리 #5 - 측정 메트릭스 계층**: CSF(Critical Success Factor, "무엇이") -> KPI(Key Performance Indicator, "어떻게") -> KGI(Key Goal Indicator, "왜"). 예: CSF="IT 신뢰성" -> KPI="가용성 99.95%, 장애 4건/월v" -> KGI="매출 손실 5%v".

- **📢 섹션 요약 비유**: COBIT의 EDM-APO-BAI-DSS-MEA 구조는 마치 **병원 운영 체계**와 같다. EDM은 병원 이사회(진료 방향 결정), APO는 진료과 기획(자원·예산 배분), BAI는 진료·수술(실제 시술), DSS는 입원·간호(지속적 케어), MEA는 QI(Quality Improvement, 의료 질 평가)에 해당한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되는 유사 프레임워크들의 정확한 차이를 이해하는 것이 기술사 시험의 핵심이다. 단순 암기형이 아니라 **"왜 다른가"**의 인과관계를 설명할 수 있어야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001/22301** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스·관리 목표 달성 | 서비스 가치 창출(Value Co-Creation) | 정보보호·연속성 인증 | 프로젝트 성과 달성 | 기업 아키텍처 일관성 |
| **구조/방법론** | 40개 목적(Goal Cascade) | 34개 Practice + 7원리 + SVC | P-D-C-A + 93개 통제(Annex A) | 8개 성과 영역 + 12원리 | ADM 8단계(Phase A~H) |
| **대상 범위** | 전사 IT 거버넌스(End-to-End) | IT 서비스 운영 중심 | 보안·연속성 특정 영역 | 단일 프로젝트/프로그램 | EA 설계·구현 |
| **측정/평가** | Capability 0~5, PAM v3.1 | Maturity Model(MI 보고서) | ISO 27002 통제 감사 | 성과 도메인(8개) 평가 | ADM 단계별 Deliverable |
| **강점** | 거버넌스/관리 분리 명확, 이사회 보고 최적화 | 유연성, Agile/DevOps 친화 | 법적 인증, 제3자 감사 | 정량적·정성적 통합 관리 | 아키텍처 뷰(View) 체계화 |
| **약점** | 운영 깊이 부족(추상적) | 거버넌스 약함 | IT 운영·서비스 미포함 | 거버넌스·운영 연계 부족 | 구현·변화관리 미흡 |
| **업데이트 주기** | 2018/2019/2024 | v3(2011) -> v4(2019) -> Foundation 2023 | 2013->2022(Annex A 93개) | v6(2017)->v7(2021) | v9.2(2018)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 463 / 800

<- **이전**: [462. IT 경영 관리 핵심 토픽 462번 시험 요약](/studynote/12_it_management/05_security_compliance/462_it_management_core_topic_462_exam_summary/)
**다음**: [464. IT 경영 관리 핵심 토픽 464번 시험 요약](/studynote/12_it_management/05_security_compliance/464_it_management_core_topic_464_exam_summary/) ->

---
