+++
title = "707. IT 경영 관리 핵심 토픽 707번 시험 요약 (IT Management Core Topic 707 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 707번 토픽은 IT 거버넌스(COBIT 2019, ISO/IEC 38500), IT 서비스 관리(ITIL 4 Service Value System), 정보화 사업 관리(PMBOK 7, Agile/DevOps), EA(TOGAF, FEAF), IT 성과 관리(BSC, KPI/CSF), 그리고 컴플라이언스·감리 체계를 통합한 IT 경영 관리 전반을 다루며, 거버넌스-전략-운영-평가의 4계층 정렬(Alignment) 메커니즘이 핵심이다.
> 2. **가치**: 잘 정립된 IT 경영 체계는 IT 투자 ROI를 평균 20~35% 향상시키고, 정보화 사업 실패율을 PMI 기준 31%에서 12% 수준으로 축소하며, ISMS 인증·감리 대응 시간을 약 40% 단축하여 정량적·정성적 가치를 동시에 제공한다.
> 3. **판단 포인트**: 거버넌스 프레임워크 채택 시 산업·조직 성숙도(COBIT Capability Level 3 이상), 규제 환경(전자금융감독규정, 개인정보보호법, 클라우드이용자보호법), 그리고 기존 IT 운영 체계(내부통제, ITSM) 간의 통합 비용과 레퍼런스 모델의 적용 비율을 트레이드오프해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX), 클라우드 네이티브 전환, AI 기반 업무 자동화, 그리고 사이버 위협의 고도화로 인해 IT는 단순 비용 센터(Cost Center)에서 비즈니스 가치 공헌 센터(Value Center)로 역할이 전환되었다. 이러한 환경에서 707번(IT 경영 관리)은 기업이 IT 자산을 전략적으로 기획·구축·운영·평가하기 위한 통합 관리 체계를 다루며, 정보관리기술사 시험에서는 특히 다음 세 가지 통찰력을 평가한다.

- **① 거버넌스-관리-운영의 3층 분리(Governance-Management-Operations Decoupling)**: ISO/IEC 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) 기반 의사결정 구조와 COBIT 2019의 Governance/Management Objectives 40개를 연계하여 Evaluate-Direct-Monitor(EDM) 사이클을 구현하는 능력
- **② 가치 흐름(Value Stream) 중심 사고**: 전통적 기능별·사일로별 관리에서 벗어나 ITIL 4의 Service Value Chain(Plan-Engage-Design&Transition-Obtain/Build-Deliver&Support-Improve) 기반의 종단간(End-to-End) 가치 흐름 설계 능력
- **③ 정량적 성과 측정과 지속적 개선**: BSC(균형성과표) 4관점(재무·고객·내부프로세스·학습성장) 기반 KPI/CSF, COBIT Process Capability Assessment(0~5단계), 그리고 PDCA/ITIL CSI(Continual Service Improvement) 기반의 측정·개선 체계 운용 능력

전통적 IT 관리(2000년대 이전)는 **프로젝트 단위 하드웨어 도입, IT 예산 통제, 헬프데스크 운영** 수준에 머물렀으나, 현재의 IT 경영 관리는 **클라우드 FinOps, SaaS 거버넌스, AI 거버넌스, ESG-연동 IT, 제로트러스트 보안 거버넌스**까지 포괄하는 전사 차원의 관리 체계로 진화했다.

```text
[707번 IT 경영 관리 도메인 맵 - 5대 핵심 영역 통합 구조]
+--------------------------------------------------------------------+
|             ① IT 거버넌스 (Governance) - ISO 38500/COBIT          |
|  ----------------------------------------------------------------- |
|  +--------------+  +--------------+  +------------------------+    |
|  | 의사결정체계  |  | 이해관계자   |  | 정책/표준/절차 체계    |    |
|  |(이사회-위원회)|-> | (Stakeholder)|<- | (Policy/Std/Process)   |    |
|  +--------------+  +--------------+  +------------------------+    |
+------------+-------------------------------------+-----------------+
             |                                     |
             v                                     v
+-----------------------+             +------------------------------+
| ② IT 전략·기획        |             | ③ IT 서비스·프로젝트 관리    |
| (EA, 정보화전략계획)  |             | (ITIL4, PMBOK7, Agile)      |
| --------------------- |             | ---------------------------- |
| TOGAF ADM / FEAF      |             | Service Value Chain          |
| - Architecture Repo   |             | - 34 Practices               |
| - Gap Analysis (SAD)  |             | - Change/Release/Incident    |
| - Capability Assess   |             | - SLO/SLA/SLI                |
+----------+------------+             +---------------+--------------+
           |                                          |
           +--------------+---------------------------+
                          v
        +---------------------------------------------+
        | ④ IT 성과·위험·컴플라이언스 관리            |
        | - BSC/KPI/CSF, COBIT PAM(40 Process)       |
        | - Risk Mgmt(ISO 31000), BCM(ISO 22301)     |
        | - ISMS-P, PIMS, IS审计, ESG-GITC            |
        +---------------------+-----------------------+
                              |
                              v
        +---------------------------------------------+
        | ⑤ IT 조직·인재·문화 관리                    |
        | - PMO/CoE, Agile@Scale(SAFe/LeSS/Disciplined)|
        | - DevOps, SRE, FinOps, AI 거버넌스          |
        | - 직무/역량 모델(SFIA, ICT Competency)      |
        +---------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 종합 운영 체계**와 같다. 상위계획(거버넌스)은 도시기본계획, EA는 토지이용계획도, ITSM은 교통·수도·전기·통신 인프라 운영, 성과관리는 도시 성과지표(예: 교통혼잡도, 상수도 수질), 조직관리는 시청 조직·인사 시스템에 각각 대응한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) IT 거버넌스 계층 (COBIT 2019 + ISO 38500 통합)

IT 거버넌스는 **이사회-경영진-IT 리더십** 3계층 간의 의사결정 권한과 책임 배분을 정의하는 상위 통제 구조다. COBIT 2019는 5개 도메인(EDM: Evaluate-Direct-Monitor 5개 목표, APO: Align-Plan-Organize 14개, BAI: Build-Acquire-Implement 11개, DSS: Deliver-Service-Support 6개, MEA: Monitor-Evaluate-Assess 4개) 총 40개 Governance/Management Objective를 통해 IT 활동을 포괄한다.

```text
[COBIT 2019 + ISO 38500 의사결정 흐름]

   +-------------------+
   |  Stakeholders     |  이해관계자(股东, 고객, 임직원, 감독기관)
   +---------+---------+
             | 가치요구사항(Drive)
             v
   +-------------------+
   |  Board / Steering |  <- ISO 38500 Evaluate (평가)
   |   Committee       |  <- COBIT EDM01~EDM05
   +---------+---------+
             | 정책/의사결정(Decisions)
             v
   +-------------------+
   |  CIO / IT Exec    |  <- ISO 38500 Direct (지시)
   |                    |  <- COBIT APO 계열
   +---------+---------+
             | 실행지시/자원배분
             v
   +-------------------+
   | IT Manager / PMO  |  <- ISO 38500 Monitor (모니터링)
   | / Service Owner   |  <- COBIT BAI/DSS/MEA
   +---------+---------+
             | 운영데이터(KRI/KPI)
             +--------------► Board 피드백 루프(Continuous)
```

### 2) IT 서비스 관리 - ITIL 4 Service Value System(SVS)

ITIL 4는 2019년 발표되어 이전 버전(v3 2011의 Service Lifecycle 5단계)을 **Service Value System(SVS)** 으로 재구조화했다. 핵심은 **Opportunity/Demand -> Value** 로의 전환이며, 7가지 guiding principle(Focus on value, Start where you are, Progress iteratively with feedback, Collaborate and promote visibility, Think and work holistically, Keep it simple and practical, Optimize and automate)과 34개 Practice, Service Value Chain 6활동으로 구성된다.

```text
[ITIL 4 Service Value Chain (SVC) 흐름]

   [Opportunity/Demand] ---+
                           v
   +-----------------------------------------------------+
   |  Plan --► Engage --► Design & Transition --► Obtain/Build |
   |      |            |              |              |       |
   |      v            v              v              v       |
   |   Deliver & Support ◄----- Improve ◄----- (피드백)    |
   +-----------------------------------------------------+
                              |
                              v
                       [Value (가치)]
                        - Utility(기능적 적합)
                        - Warranty(보증: 가용성/용량/보안/지속성)
                              |
                              v
                   [4 Dimensions of Service Mgmt]
                   - Organizations & People
                   - Information & Technology
                   - Partners & Suppliers
                   - Value Streams & Processes
```

### 3) Enterprise Architecture - TOGAF ADM

TOGAF(현행 10판)는 **Architecture Development Method(ADM)** 8단계(Phase A: Architecture Vision ~ Phase H: Architecture Change Management)와 Requirements Management, Architecture Repository(ABB, ABBs, AS-IS/TO-BE), 그리고 ADM Iteration Cycle을 제공한다. 핵심 산출물인 **SAD(Statement of Architecture Definition), SBD(Statement of Business/Digital Capability)** 는 의사결정 자료로 활용된다.

### 4) 핵심 구성 요소 비교표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회** (Steering Committee) | 의사결정·감독 기구, EDM 5개 목표 수행 | 정례 월간 회의(월 1회), 주요 의사결정(20% 예산 이상/규제 영향), RACI 매트릭스 기반 역할 분담, 정족수(과반수) 기반 의결 |
| **EA(Enterprise Architecture) 조직** | 전사 아키텍처 표준화·통합 | TOGAF ADM 8단계 사이클, Architecture Repository 운영(ArchiMate 3.2 모델링), 거버넌스 보드(ARB) 통한 표준 준수 검토, Capstone Road Map(3~5년) 수립 |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오·프로그램 관리 | 단계별 게이트 프로세스(Stage Gate: Initiation->Planning->Execution->Closure), EVM(Earned Value Management) 성과 측정, 리스크 레지스터·이슈 로그 운영, 단계-게이트별 Go/No-Go 의사결정 |
| **ITSM(Service Desk/Operation)** | 서비스 운영·지원·개선 | ITIL 4 SVC 6활동, Incident/Problem/Change/Request Fulfilment 4대 프로세스, CMDB(Configuration Management DB) 기반 자산 추적, SLO/SLA 기반 우선순위(P1~P4) 결정 |
| **정보보안 거버넌스** | 보안 전략·통제·감사 | ISMS-P(ISO 27001:2022 + 27017 + 27018), 위험평가(ISO 27005), 통제 93개(Annex A 4영역), 정기 내부감사(연 1회) + 인증감사(3년 주기) |
| **DR/BCP** | 사업연속성·재해복구 | ISO 22301 BCM, BIA(Business Impact Analysis) 기반 RTO/RPO 산정, DR Drill(연 1~2회), Hot/Warm/Cold Site 등급별 전략 |
| **IT 성과·측정 체계** | 정량적 관리·보고 | COBIT 2019의 Process Capability Model(0~5단계, PAM 7단계), BSC 4관점 KPI(20~30개), CSF(CSF Linkage Diagram), Cascading Scorecard |
| **IT 조직·인재** | 직무·역량·문화 관리 | SFIA 8(Skills Framework for the Information Age) 6수준, 직무기술서(JD)·역량평가(연 1회), Agile@Scale(SAFe 6.0, LeSS) 도입 시 릴리스 트레인·PI Planning |

### 5) 핵심 알고리즘·모델·공식

- **COBIT Process Capability 산정식**: PAM(Process Assessment Model) 7단계(Not Performed->Performed->Managed->Established->Predictable->Optimizing) × PA(Process Attribute) 9개(PA 1.1~5.2). 능력 등급 = Σ(PRM 평가점수 × 가중치) ÷ 속성 가중치 합
- **EVM(Earned Value Management) 핵심 지표**:
  - **PV(Planned Value)**: 계획값, **EV(Earned Value)**: 실적값, **AC(Actual Cost)**: 실제 비용
  - **CV = EV - AC** (비용편차, >0 절감)
  - **SV = EV - PV** (일정편차, >0 선행)
  - **CPI = EV/AC** (비용성과지수, ≥1 양호)
  - **SPI = EV/PV** (일정성과지수, ≥1 양호)
  - **EAC(Estimate At Completion) = BAC ÷ CPI**, **ETC = EAC - AC**, **VAC = BAC - EAC**
- **가치 흐름 가치 측정(VSM 기반)**: Lead Time, Process Time, %C&A(Complete & Accurate) 지표. ITIL 4 VSM에서는 **Value Stream Effectiveness = (실제 고객가치 기여 시간 / 총 Lead Time) × 100**
- **ROI/NPV/IRR**: TCO(Total Cost of Ownership) = CapEx + OpEx(3~5년). NPV = Σ[CFt/(1+r)^t] - 초기투자. IRR은 NPV=0이 되는 할인율

- **📢 섹션 요약 비유**: IT 거버넌스는 **자동차의 핸들·브레이크·엑셀** 3패달 시스템이다. 거버넌스(핸들)는 방향 결정, 프로젝트 관리(엑셀)는 추진력, 컴플라이언스·감사(브레이크)는 안전 통제이며, 이 셋이 동시에 작동해야 차량(기업)이 목적지(전략 목표)에 안전하게 도달한다.

---

## Ⅲ. 비교 및 연결

### 1) 주요 IT 경영 프레임워크 비교

| 구분 | COBIT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 707 / 800

<- **이전**: [706. IT 경영 관리 핵심 토픽 706번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/706_it_management_core_topic_706_exam_summary/)
**다음**: [708. IT 경영 관리 핵심 토픽 708번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/708_it_management_core_topic_708_exam_summary/) ->

---
