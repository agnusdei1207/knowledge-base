---
title: "687. IT 경영 관리 핵심 토픽 687번 시험 요약 (IT Management Core Topic 687 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019·ISO 38500·TOGAF ADM·ITIL 4·PMBOK 7·ISO 27001·CMMI 2.0 등 다중 거버넌스 프레임워크를 통합하여 **전략 정렬(Strategy Alignment) -> 가치 전달(Value Delivery) -> 위험 최적화(Risk Optimization) -> 자원 관리(Resource Management) -> 성과 측정(Performance Measurement)**의 5대 영역에서 의사결정 권한과 책임을 체계화한 Enterprise Governance of IT 체계
> 2. **가치**: 정량적 효과로 McKinsey 보고 기준 **디지털 전환成熟 기업은 수익성 26%·EBITDA 9%p 우위**, 한국정보화진흥원 2023년 조사에서 **IT 거버넌스 체계 구축 기업의 IT 투자 대비 ROI 평균 287%(미구축 142%)**, 또한 프로젝트 성공률 67% -> 89% 향상(PMI Pulse of Profession 2023)
> 3. **판단 포인트**: ① **Plan-driven(폭포수) vs Agile(스크럼/SAFe)**, ② **Centralized COE(센터) vs Federated(사업부 자율) vs Hybrid(CoE+사업부) IT 거버넌스 모델**, ③ **TOGAF ADM 준수 vs Lightweight EA**, ④ **Bimodal IT(Mode 1 안정성+Mode 2 민첩성)**, ⑤ **국내 개인정보보호법·정보통신망법·클라우드컴퓨팅법·전자금융거래법·전자상거래법** 규제 매트릭스 준수 설계

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Enterprise IT Management, EITM)는 1990년대 말 이후 **반트르(Rayport)·사시아르나미(Sasiarnani)의 IS 전략 정렬 모델(Strategic Alignment Model, SAM)**에서 출발하여, 2000년대 초 IT 거버넌스 위기(사베린사·월마트·SOX법) 이후 **감사가능성(Auditability)·책임성(Accountability)·전략적 가치(Strategic Value)** 확보를 위한 통합 관리 체계로 진화해 왔습니다. 특히 4차 산업혁명·Web 3.0·메타버스·생성형 AI(LLM/MFM)·양자컴퓨팅·클라우드 네이티브 환경에서 IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**이자 **데이터·플랫폼·AI의 통합 자산 운용** 체계로 변모했습니다.

기술사 시험 관점에서 IT 경영 관리는 단순히 "IT 부서 관리"가 아니라, **Board-CEO-CIO-IT Steering Committee-IT Governance Office-PMO-Service Owner-Product Team**으로 이어지는 **3 Lines Model(IIA, 2020)** 기반 의사결정 체계와, **COBIT 2019의 40개 관리 목표(Management Objective)와 5개 도메인(EDM/APO/BAI/DSS/MEA)**을 비즈니스 요구사항에 맞게 **Cascade·Customize**하는 능력을 측정합니다.

```text
[IT 경영 관리 통합 참조 모델 (Integrated IT Management Reference Model)]

   +----------------------------------------------------------+
   |    Board / CEO / Audit Committee (최고 의사결정 기구)   |
   +---------------------+------------------------------------+
                         | Strategic Intent / Risk Appetite
                         v
   +----------------------------------------------------------+
   |   IT Steering Committee + CIO + CDO + CISO + CPO        |
   |  (전략적 IT 거버넌스 의사결정 + Risk + Compliance)        |
   +----+-------------+-------------+-------------+----------+
        |             |             |             |
        v             v             v             v
  +----------+  +----------+  +----------+  +----------+
  | 전략     |  | 아키텍처 |  | 서비스   |  | 보안·    |
  | 기획     |  | (EA)     |  | 운영     |  | 컴플라이 |
  | 영역     |  | TOGAF    |  | ITIL 4   |  | 언스     |
  |          |  | Zachman  |  | SIAM     |  | ISO 27001|
  | -Portfolio|  | FEAF     |  | AIOps    |  | NIST CSF |
  | -투자평가|  | DoDAF    |  | SRE      |  | ISMS-P   |
  | -성과측정|  |          |  | FinOps   |  | PIPC     |
  +----+-----+  +----+-----+  +----+-----+  +----+-----+
       |             |             |             |
       +-------------+-------------+-------------+
                         |
                         v
   +----------------------------------------------------------+
   |  Value Stream: 아이디어 -> 투자 -> 설계 -> 구축 -> 운영 -> 폐기|
   |   (PMBOK/PRINCE2/SAFe + DevOps + SRE + FinOps)         |
   +----------------------------------------------------------+
                         |
                         v
   +----------------------------------------------------------+
   |  측정·개선: BSC, KPI/KCI, CSF, OKR, CMMI 2.0 Maturity   |
   |  (COBIT 2019 MEA 도메인 + ISO 33000 Process Assessment) |
   +----------------------------------------------------------+
```

**기존 패러다임 대비 신패러다임의 차별점**

| 구분 | 기존(Era 2000~2015) | 신패러다임(2020~) |
|:---|:---|:---|
| **IT 역할** | 비용 센터(Cost Center), Back-office | 가치 창출 센터(Value Creator), P&L 기여 |
| **거버넌스** | 중앙 집중(COE), 통제 중심, Audit | 분산-공존(Federated), Risk-Based |
| **투자 기준** | TCO·ROI 단일 회수 분석 | NPV·IRR·TCO·VOI(Value on Investment)·NPS·ESG Score |
| **아키텍처** | 모놀리식(On-Prem), SOA, ESB | 클라우드 네이티브, MSA(Micro Service), Edge-Fog-Cloud, 하이퍼컨버지드 |
| **운영** | ITIL v3 5권 26 프로세스, Reactive | ITIL 4 SVS(34 Practice), AIOps·SRE·Chaos Engineering |
| **프로젝트** | 폭포수/PMBOK 5·6 단일 | PMBOK 7(원리+8도메인), Bimodal(Plan+Agile), SAFe/Spotify |
| **데이터** | DW·DWH(배치), RDBMS | Data Lakehouse(Databricks/Iceberg), Data Mesh, Streaming |
| **보안** | Perimeter, 방화벽, EDR | Zero Trust(NIST SP 800-207), SASE, XDR, SBOM |
| **규제** | SOX·PCI-DSS·ISO 27001 | + PIPC·DPR·EU GDPR·AI 기본법(잠정)·DORA·NIS2 |

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'통합 계기판(Integrated Cockpit)'**과 같습니다. RPM(전략 정렬도)·연료(자원/예산)·속도(성과)·엔진온도(리스크)·내비게이션(아키텍처)·사고감지 카메라(보안)·보험(컴플라이언스)·정비 예약(서비스 운영)·출발지-목적지(비즈니스 전략) 정보를 하나의 **CAN Bus(거버넌스 통합 프레임워크)**로 묶어 운전자(경영진)에게 **Single Pane of Glass**를 제공합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **5대 거버넌스 영역(Strategy·Architecture·Service·Project·Security/Risk)**을 **PDCA(Plan-Do-Check-Act) + COBIT EDM(평가·지시·모니터링) 사이클**로 통합 운영하는 것입니다. 2023년 AXELOS·ISACA·PMI의 통합 참조 모델에 따르면, **전략(Strategy)**은 **COBIT 2019 EDM·APO**, **아키텍처(Architecture)**는 **TOGAF ADM + ArchiMate 3.2**, **서비스 운영(Service)**은 **ITIL 4 SVS(Service Value System) + SIAM**, **프로젝트(Project)**는 **PMBOK 7 8대 Performance Domain + PRINCE2 7 Principle + SAFe/Agile**, **보안(Security)**은 **NIST CSF 2.0(Identify·Protect·Detect·Respond·Recover + Govern) + ISO 27001:2022 Annex A 93 통제 항목**으로 구성됩니다.

```text
[IT 경영 관리 5대 영역 상호작용 아키텍처]

  +--------------------------------------------------------------+
  |   ① 전략-투자 영역 (COBIT 2019: EDM04·05, APO05·06)        |
  |  Portfolio Mgmt · Investment Mgmt · Demand Mgmt · I&T Risk |
  |      v  Cascading Strategy                                |
  +--------------------------------------------------------------+
  |   ② 아키텍처 영역 (TOGAF ADM Phase A~H, ArchiMate 3.2)   |
  |  Business · Application · Data · Technology · Security     |
  |      v  Architecture Roadmap                              |
  +--------------------------------------------------------------+
  |   ③ 프로젝트-전달 영역 (PMBOK 7 + SAFe 6 + PRINCE2 7)    |
  |  Feasibility -> Chartering -> Planning -> Executing -> Closure |
  |  + DevOps CI/CD Pipeline + SRE Error Budget                |
  |      v  Service Transition                                |
  +--------------------------------------------------------------+
  |   ④ 서비스-운영 영역 (ITIL 4 SVS: 34 Practice)            |
  |  Incident·Problem·Change·SLM·Monitoring·FinOps·AIOps      |
  |      v  Service Quality KPI                               |
  +--------------------------------------------------------------+
  |   ⑤ 보안-리스크 영역 (NIST CSF 2.0 + ISO 27001:2022)      |
  |  Governance·Identify·Protect·Detect·Respond·Recover        |
  +--------------------------------------------------------------+
                              |
                              v  (MEA - Monitor, Evaluate, Assess)
            +--------------------------------------+
            |  COBIT 2019 MEA 도메인: 성과·내부통제|
            |  ·IT Balanced Scorecard(4관점)        |
            |  ·KPI Tree (CSF -> KRA -> KPI -> KCI)   |
            |  ·Process Capability (ISO 33020 PAM)  |
            |  ·Maturity Level 0~5                 |
            +--------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **① COBIT 2019** (ISACA) | IT 거버넌스·관리 통합 프레임워크 | **5개 도메인**(EDM 5·APO 14·BAI 11·DSS 6·MEA 4 = 40 Management Objective), **7개 컴포넌트**(Principles·Policies·Processes·Org Structures·Information·People·Skills·Services·Infrastructure·Tech), **Design Factors 11개**로 조직별 맞춤 설계. **Cascade Goals**가 Enterprise Goal(13개) -> Alignment Goal(13개) -> Management Objective로 매핑. **Capability Level**(0~5, ISO 33020 PAM 6단계) 측정 |
| **② TOGAF ADM** (The Open Group) | Enterprise Architecture 개발 방법론 | **ADM Cycle Phase A(Architecture Vision) -> B/C/D/Business·Data·Application·Technology) -> E(Opportunities) -> F(Migration Planning) -> G(Implementation Governance) -> H(Architecture Change Mgmt) -> Requirements Mgmt(연속)**. **ArchiMate 3.2** 언어(Strategy/Active/Structure/Behavior Layer + 6 Aspect). **Content Metamodel**(Work Product·Deliverable·Artifact 50+). Phase G에서 **Transition Architecture**로 Migration Project 우선순위 산정 |
| **③ ITIL 4** (AXELOS/PeopleCert) | IT Service Management(SVS) | **Service Value System(SVS)**: Opportunity/Demand -> Value -> 조직역량(Organization·People·Product·Partner·Supplier) -> Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) -> Value. **34 Practice**(General·Service·Technical Management). **4-Dimension Model**(Organizations
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 687 / 800

<- **이전**: [686. IT 경영 관리 핵심 토픽 686번 시험 요약](/studynote/12_it_management/05_security_compliance/686_it_management_core_topic_686_exam_summary/)
**다음**: [688. IT 경영 관리 핵심 토픽 688번 시험 요약](/studynote/12_it_management/05_security_compliance/688_it_management_core_topic_688_exam_summary/) ->

---
