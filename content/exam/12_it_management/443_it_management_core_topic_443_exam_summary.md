---
title: "IT Management Core Topic 443 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽은 COBIT 2019, ITIL 4, ISO/IEC 38500, ISO/IEC 27001, PMBOK 7th, BSC-IT 등 거버넌스-서비스-보안-성과의 4축 통합 프레임워크를 통해 IT를 전략 자산으로 정렬(Value Delivery)하고, 위험(Resource Risk Optimization)과 자원(Optimize Resources)을 균형 있게 통제하는 경영 체계임
> 2. **가치**: 성숙도 3단계(Maturity Level 1->5) 도달 시 IT 프로젝트 실패율 약 60%->25% 감소, IT 투자 ROI 평균 28% 개선(Forrester 2023), ISMS 인증 기업 기준 보안사고 대응시간 73% 단축, COBIT 적용 기업 TCO 18~34% 절감 효과 검증
> 3. **판단 포인트**: 중앙집중형(COBIT Cascade) vs 분산형(Federated) 거버넌스, Push형(ITIL Service Value Chain) vs Pull형(Agile/DevOps) 운영, CapEx(전통 인프라) vs OpEx(클라우드/EaaS) 재무구조, Zero Trust(내부위험 차단) vs Perimeter Security(외부위협 차단) 보안전략의 트레이드오프

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(IT Management & Governance)는 디지털 전환(DX) 시대에 기업이 IT를 단순 비용 중심(Cost Center)에서 가치 창출 중심(Value Center) 및 전략 파트너(Strategic Partner)로 전환하기 위한 총체적 경영 체계이다. 한국정보화진흥원(KIAT)의 「2024 ICT 산업 동향」에 따르면 국내 CIO의 87%가 "IT와 사업 전략의 정렬(Strategic Alignment)"을 최우선 과제로 응답했으며, 디지털 트랜스포메이션 투자액은 2019년 9.2조원에서 2024년 42.7조원으로 5년간 약 4.6배 증가하였다. 그러나 McKinsey의 「2023 Tech Value Survey」에 따르면 글로벌 IT 이니셔티브의 약 70%가 EBIT(세전이익) 목표를 달성하지 못하고 있으며, 이러한 실패의 근본 원인은 (1) IT 거버넌스 부재로 인한 의사결정 비효율, (2) ITIL 등 서비스 운영 체계 미성숙, (3) 사이버보안 위험 관리 실패, (4) IT 성과 측정 지표 부재로 보고되고 있다.

특히 클라우드 네이티브, 생성형 AI(GenAI), 양자내성암호(PQC) 등 신기술 도입이 가속화되면서, IT 경영 관리의 범위는 전통적 데이터센터 운영을 넘어 데이터 거버넌스(DAMA-DMBOK 2.0), AI 거버넌스(NIST AI RMF 1.0), ESG-IT(ISO/IEC 30134 시리즈) 등으로 확장되고 있다. 이에 ISO/IEC 38500 IT Governance Standard는 **"Evaluate-Direct-Monitor(평가-지시-모니터링)"**의 3단계 원칙을 통해 이사회 및 경영진의 IT 의사결정 책임을 명문화하고 있으며, COBIT 2019은 **Governance and Management Objectives(40개 목표)** 체계를 통해 실무 적용성을 강화했다.

```text
[기업의 IT 경영 관리 통합 프레임워크 통합 구조도]

+---------------------------------------------------------------------+
|          Board / 이사회의 IT 거버넌스 의사결정 (ISO 38500 EDM)        |
|      Evaluate ------► Direct ------► Monitor (3-원칙 주기)        |
+----------------------------+----------------------------------------+
                             | Cascading(연결)
        +--------------------+--------------------+
        v                    v                    v
+--------------+   +------------------+   +------------------+
| COBIT 2019   |   |   ITIL 4         |   |  ISO 27001/27701 |
| (40 Objectives|   |  (SVS: Service   |   |  (ISMS/PIMS)     |
|  Governance  |   |   Value System)  |   |  Annex A 통제 93|
|  & Mgmt)     |   |  34 Practice     |   |  항목            |
+------+-------+   +--------+---------+   +--------+---------+
       |                    |                       |
       v                    v                       v
+--------------+   +------------------+   +------------------+
| Balanced     |   | DevOps / SRE     |   |  Zero Trust      |
| Scorecard IT |   | (CI/CD + Observ- |   |  Architecture    |
| (BSC-IT)     |   |  ability+IaC)    |   | (NIST SP 800-207)|
| 4관점 KPI    |   | DORA 4 Metrics   |   | ZTA 3-원칙      |
+------+-------+   +--------+---------+   +--------+---------+
       |                    |                       |
       +--------------------+-----------------------+
                            v
              +------------------------------+
              |   사업 성과(Value Realization)|
              |   ROI 28%^, 사고 대응 73%v |
              |   TCO 18~34% 절감, SLA 99.99|
              +------------------------------+

  <---- 정렬(Alignment) ----> <---- 실현(Realization) ----> <---- 통제(Control) ---->
```

기존 패러다임(2000년대 초반)에서는 IT를 **지원 기능(Support Function)**으로 인식하여 IT 부서 종속적 의사결정, CapEx 중심의 HW 투자, Reactive(사후 대응) 운영, 그리고 "Uptime 99.9%" 같은 기술 지표 중심의 성과 측정이 주류였다. 반면 DX 시대의 새로운 패러다임은 **전략적 동인(Strategic Enabler)**으로 IT를 인식하여 사업-기술 공동 의사결정(Gartner Bimodal IT), OpEx 기반 유연한 투자(Cloud FinOps), Proactive(예방 중심) 운영, 그리고 **EBIT, NPV, NPS, Time-to-Market** 등 사업 지표 중심의 성과 측정을 요구한다. 이 변화의 핵심 동인은 (1) 비지니스 속도 가속화(VUCA+ BANI 시대), (2) 규제 강화(개인정보보호법, AI 기본법, ESG 공시), (3) 사이버 위협의 산업화(Ransomware-as-a-Service, Supply Chain Attack), (4) IT 인재 확보 경쟁 심화로 요약된다.

- **📢 섹션 요약 비유**: IT 경영 관리를 "도시의 도시계획"에 비유할 수 있다. 과거에는 건물 하나하나(시스템)를 그때그때 지었지만(Ad-hoc), 이제는 상하수도·전기·교통·치안(거버넌스·서비스·보안·성과)을 통합 설계하는 스마트시티总体规划(마스터플랜)이 필요해진 시대이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 핵심 축(Governance-Service-Security-Performance)은 각각 독립된 표준 프레임워크를 가지지만, 실무에서는 상호 보완적으로 통합 운영된다. 아래는 각 축의 아키텍처와 핵심 동작 원리이다.

```text
[IT 경영 관리 4축 통합 아키텍처 및 데이터/의사결정 흐름도]

+------------------------------------------------------------------+
|                1축: 거버넌스 (COBIT 2019 + ISO 38500)              |
|                                                                   |
|  +-------------+    +--------------+    +-----------------+       |
|  | Governance  |    |  Management  |    |  Cascade        |       |
|  | Objectives  |    |  Objectives  |    |  (연락·전파)     |       |
|  | (5 domains) |    | (5 domains)  |    |  Enterprise ->   |       |
|  | EDM×5 목표  |    | BAI/DSS/MEA  |    |  Division -> IT  |       |
|  +------+------+    +------+-------+    +--------+--------+       |
+---------+-------------------+---------------------+---------------+
          |                   |                     |
          | Goal Cascade     | RACI Matrix         | Policy Tree
          v                   v                     v
+------------------------------------------------------------------+
|                2축: 서비스 운영 (ITIL 4 + DevOps)                  |
|                                                                   |
|  Service Value Chain (SVC) - 6 Activity:                          |
|  Plan -> Improve -> Engage -> Design & Transition -> Obtain/Build    |
|            -> Deliver & Support                                    |
|                                                                   |
|  +----------+  +----------+  +----------+  +--------------+      |
|  | Service  |  | Change   |  | Incident |  |  Continual   |      |
|  | Desk     |  | Enablement| | Mgmt     |  |  Improvement |      |
|  | (Tier1-3)|  | (CAB/ECAB)| | (P1~P5) |  |  (CSI Register)|    |
|  +----------+  +----------+  +----------+  +--------------+      |
+---------+---------------------------------------------------------+
          | CMDB(구성항목 DB) 연동
          v
+------------------------------------------------------------------+
|                3축: 정보보안 (ISO 27001 + Zero Trust)              |
|                                                                   |
|  Plan-Do-Check-Act (PDCA) + Annex A 93 통제항목:                  |
|  A.5 조직(37) / A.6 People(8) / A.7 Physical(14) /               |
|  A.8 Tech(34) (2022 개정)                                        |
|                                                                   |
|  +--------------+    +--------------+    +--------------+        |
|  |  Identity    |    |  Device      |    |  Application |        |
|  |  (IAM: SSO/  |    |  (MDM, EDR)  |    |  (CASB, WAF) |        |
|  |   MFA/PAM)   |    |              |    |              |        |
|  +--------------+    +--------------+    +--------------+        |
+---------+---------------------------------------------------------+
          | KRI(핵심위험지표) 연동
          v
+------------------------------------------------------------------+
|                4축: 성과측정 (BSC-IT + DORA + KPI Tree)            |
|                                                                   |
|  +----------+ +----------+ +----------+ +----------+              |
|  | Financial| | Customer | |Internal  | | Learning |              |
|  | (ROI,    | | (NPS,    | |(MTTR,    | |(자격증,  |              |
|  |  TCO,    | |  CSAT,   | | Change   | | 교육,    |              |
|  |  EVA)    | |  SLA)    | | Success) | | Retention|              |
|  +----------+ +----------+ +----------+ +----------+              |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Governance System** | IT 의사결정 및 통제 체계 | 40개 Governance/Management Objectives, 7개 구성요소(System Components), 5단계 성숙도 모델, Design Factor 11개로 조직 맞춤 설계. COBIT 2019는 2019년 5대 Design Factor 도입으로 "One-size-fits-all" 탈피, Cascading Goals로 사업 목표->IT 목표 정렬 |
| **ITIL 4 Service Value System (SVS)** | IT 서비스 운영 및 가치 창출 | Service Value Chain 6개 Activity(Plan/Improve/Engage/Design&Transition/Obtain&Build/Deliver&Support), 34개 Practice(2020 변경: 변경관리->Change Enablement), 4 Dimension Model(Organizations/People/Information&Technology/Partners&Suppliers/Value Streams&Processes) |
| **ISO/IEC 27001:2022 ISMS** | 정보보호 관리체계 | Plan-Do-Check-Act 사이클, Annex A 93개 통제항목(5.조직 37, 6.People 8, 7.Physical 14, 8.Technology 34), Statement of Applicability(SoA), Risk Treatment Plan(RTP), ISMS 인증 심사는 3년 주기 + 매년 Surveillance |
| **BSC-IT Balanced Scorecard** | IT 성과 측정 및 전략 맵 | Kaplan & Norton 4관점(Financial/Customer/Internal Process/Learning & Growth) + IT 특화 관점 추가. Strategy Map으로 인과관계 시각화, KPI는 Leading vs Lagging 지표 7:3 비율 권장 |
| **PMBOK 7th Edition** | 프로젝트 관리 표준 | PMI 표준, 12 Principles of Project Management, 8 Performance Domains(Stakeholders/Team/Development Approach/Planning/Project Work/Delivery/Measurement/Uncertainty), 5 Process Groups -> 7th에서 8 Performance Domain + Tailoring 강조 |

**핵심 동작 메커니즘 심화 분석**

1. **COBIT 2019의 Goal Cascade(목표 연계)**: 사업 목표 13개 -> IT 관련 목표 13개 -> Enabler(촉진자) 7개로 3단계 연계. 예: 사업 목표 05(고객 중심 문화) -> IT 목표 07(보안·프라이버시) -> Enabler: 프로세스(APO12 위험관리) + 정보(보안 정책) + 조직(CISO). Design Factor는 (1) Enterprise Strategy, (2) Enterprise Goals, (3) Risk Profile, (4) I&T 관련 이슈, (5) 위협 환경, (6) 준수 요구사항, (7) IT 역할, (8) IT 조달 방식, (9) IT 구현 방법, (10) 기술 채택 전략, (11) 조직 구조로 총 11개이며, 각 조직의 상황에 따라 우선순위 목표를 자동 산출한다.

2. **ITIL 4 SVC의 Value Stream**: 6개 Activity는 순차 실행이 아닌 상황에 따라 조합되며, 대표적인 3개 Value Stream은 (1) **Incident Resolution Stream**(Incident->Service Desk->Resolve->Close), (2) **New Service Onboarding Stream**(Engage->Design->Build->Transition->Operate), (3) **Major Change Stream**(CAB->RFC->Assessment->Approval->Implementation->Review). 34개 Practice 중 핵심은 Incident Management, Change Enablement(구 Change Management), Service Level Management, Continual Improvement, Problem Management, Service Request Management 등이다.

3. **ISO 27001:2022 Risk Treatment 프로세스**: 위험 식별 -> 자산 식별(Asset Inventory) -> 위협(Threat) 식별 -> 취약점(Vulnerability) 분석 -> 영향도(Impact) × 가능성(Likelihood) = Risk Score. 통제 선택 시 Annex A 93개 항목 중 적용 가능한 것을 SoA에 명시하고, 미적용 시 사유(Justification) 기재. SoA는 ISO 27001 인증의 핵심 문서이며, Statement of Applicability v1은 2022년 개정 시 Annex A 항목이 114개에서 93개로 통폐합(14개 신규, 57개 통합, 1개 삭제)되었다.

4. **BSC-IT의 Strategy Map 인과관계**: Learning&Growth(인재/문화) -> Internal Process(운영 효율) -> Customer(고객 가치) -> Financial(재무 성과)의 4단계 인과 사슬을 따라 KPI가 연결된다. 예: 개발자 역량 교육
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 443 / 800

<- **이전**: [442. IT 경영 관리 핵심 토픽 442번 시험 요약](/studynote/12_it_management/05_security_compliance/442_it_management_core_topic_442_exam_summary/)
**다음**: [444. IT 경영 관리 핵심 토픽 444번 시험 요약](/studynote/12_it_management/05_security_compliance/444_it_management_core_topic_444_exam_summary/) ->

---
