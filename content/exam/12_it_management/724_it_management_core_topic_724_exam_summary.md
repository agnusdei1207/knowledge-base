---
title: "IT Management Core Topic 724 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 40개 거버넌스/관리 목표(Governance & Management Objectives)를 EDM·APO·BAI·DSS·MEA 5개 도메인에 매핑하여, Design Factor 11개로 조직 맥락에 최적화된 거버넌스 시스템을 엔지니어링하는 체계이며, 디지털 전환은 Strategy(전략) -> Technology(기술) -> Operation(운영) -> People(사람/문화) 4-Layer에 Capability Maturity Model Integration(CMMI) Level 2~5 단계를 적용해 전사적 비즈니스 가치(Value Realization)를 달성하는 프레임워크다.
> 2. **가치**: COBIT 2019 적용 시 Value Office(VO)와 Performance Management를 통한 IT 투자 대비 ROI 평균 23%(ISACA 2023 Benchmark) 향상, 디지털 전환 성공률 비적용 대비 2.4배(Gartner 2024) 증가, NIST CSF 2.0·ISO 27001:2022·ISO 38500:2015 3대 표준 동시 충족으로 컴플라이언스 비용 약 35% 절감.
> 3. **판단 포인트**: ① 거버넌 체계 선택 시 중앙화(Centralized, COBIT 2019 Design Factor 1: Enterprise Strategy=Aggressive) vs 분산화(Federated, Conservative) 간 RACI 매트릭스权衡, ② 클라우드 전환 시 Build-Operate-Transfer(BOT) -> Multi-Cloud(Brokerage) -> Cloud-Native(MSA) 단계별 Risk Appetite 설정, ③ MSP/SIEM/SOX/ISMS-P 인증 요구사항 충족을 위한 Control Objective 매핑 우선순위 결정.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 1990년대 ITIL v1·v2 기반의 프로세스 운영에 초점을 두었으나, 2000년대 이후 SOX법·ISMS-P·ESG 공시 의무화로 인해 단순 서비스 데스크 수준을 넘어 **이사회-경영진-IT가 연계된 엔터프라이즈 거버넌스**가 요구된다. 또한 4차 산업혁명(AI·Cloud·BigData·IoT) 시대의 Legacy System(평균 수명 17.3년, Deloitte 2023)은 TCO(Total Cost of Ownership) 한계와 Time-to-Market 지연(평균 18.7개월)으로 인해 사업 경쟁력을 저하시킨다. IT 거버넌스(IT Governance)와 디지털 전환 전략(Digital Transformation Strategy)은 이 두 가지 난제를 동시에 해결하기 위한 현대 정보시스템 분야의 핵심 토픽이다.

COBIT 2019는 기존 COBIT 5(2012)의 5단 원칙(Principle)을 6단 거버넌 시스템 원리(Governance System Principles)로 확장하고, 7단 거버넌 프레임워크 원리(Framework Principles)를 통해 40개 Governance/Management Objective를 조직의 11개 Design Factor(Enterprise Strategy, Enterprise Goals, Risk Profile, I&T-Related Issues, Threat Landscape, Compliance Requirements, Role of IT, IT Adoption, Sourcing Model, IT Implementation, Technology Adoption)별로 가중치 적용하여 커스터마이징한다. 이는 ISO/IEC 38500:2015의 **3개 모델(Direct, Monitor, Evaluate)**, ISO/IEC 27001:2022의 **Annex A 93개 통제 항목**, NIST CSF 2.0(2024)의 **Function(Identify, Protect, Detect, Respond, Recover) 6개·Category 22개**와 1:1 또는 N:M 매핑이 가능해 통합 거버넌스 운영이 가능하다.

### 4-Layer 디지털 전환 아키텍처 (Strategy-Tech-Ops-People)

```text
+------------------------------------------------------------------+
| Layer 1: Strategy (전략) - Balanced Scorecard, OKR, EA(TOGAF)    |
|  +------------------------------------------------------------+ |
|  | Vision  ->  Mission  ->  Strategic Goal  ->  CSF  ->  KPI  ->  | |
|  |           (5Y)        (Annual OKR)     (CSF=12)  (KPI=36)| |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
| Layer 2: Technology (기술) - Cloud, AI/ML, Blockchain, IoT, 5G   |
|  +------------------------------------------------------------+ |
|  | Public Cloud(AWS/Azure/GCP)  <---->  Private(K8s/OCP)       | |
|  | AI/ML Platform (MLOps)        <---->  Data Lakehouse         | |
|  | (Kubeflow/MLflow/SageMaker)  <---->  (Iceberg/Delta/Hudi)  | |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
| Layer 3: Operation (운영) - ITIL 4, SRE, AIOps, FinOps          |
|  +------------------------------------------------------------+ |
|  | 34 Practice(서비스 5·기술 9·사업 5·디지털 6·관리 9)        | |
|  | SRE 4 Golden Signal(Latency/Traffic/Errors/Saturation)    | |
|  | FinOps: Inform->Optimize->Operate (Phase)                   | |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
| Layer 4: People (사람/문화) - 조직역량, Change Mgmt, Agile/SAFe |
|  +------------------------------------------------------------+ |
|  | Skills Inventory(현재역량) - GAP -> L&D Plan -> KPI         | |
|  | ADKAR(Model) : Awareness->Desire->Knowledge->Ability->Reinforce| |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

### Old vs New Paradigm 비교

| 항목 | 구 패러다임(2000~2015) | 신 패러다임(2016~현재) |
|------|------------------------|------------------------|
| 거버넌스 프레임워크 | COBIT 5(원칙 5개) | **COBIT 2019**(원리 13개·Design Factor 11개·Focus Area 40+) |
| 운영 체계 | ITIL v2/v3(26 Process) | **ITIL 4**(34 Practice, 4 Dimension) |
| 인프라 | On-Premise(Mainframe) | **Hybrid/Multi-Cloud**(CSP 5개 활용) |
| 개발 방법론 | Waterfall | **Agile(Scrum) / SAFe / DevOps / GitOps** |
| SLA | Mean Time Between Failure | **SLO/SLI/SLI + Error Budget(연 99.99%=52.6분)** |
| 보안 | Perimeter Firewall | **Zero Trust(마이크로세그멘테이션 + MFA + BeyondCorp)** |
| 데이터 관리 | RDBMS(OLTP) 단독 | **Lakehouse(Iceberg/Delta) + Data Mesh** |
| 의사결정 | CIO 독단 | **CoE(센터오브엑설런스) + RACI + Federated 모델** |

- **📢 섹션 요약 비유**: IT 거버넌스는 회사의 **"주식회사 정관(Articles of Association) + 이사회의사록(Board Minutes)"** 같아서, 어떤 사업을 어디까지(Scope)·어떤 권한으로(RACI)·어떤 리스크 허용수준(Risk Appetite) 안에서 할지를 문서화한 **최상위 규범 체계**다. 디지털 전환은 그 정관 아래 **"신성장동력 사업계획서"** 라고 할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 거버넌 시스템은 **5개 도메인 × 40개 목표** 구조로, 각 목표는 Process Practice(Industry/Standard/Regulation 참조), Information Flow, People/Skills/Competencies, Policies/Procedures, Culture/Ethics/Behavior, Services/Infrastructure/Applications, Goals Cascade 7개 컴포넌트(Components of a Governance System)로 구성된다.

### COBIT 2019 Core Model — 40 Objectives Mapping

```text
        +----------------------- GOVERNANCE (5 Obj.) ---------------------+
        |                                                                |
        |   EDM01  EDM02    EDM03    EDM04    EDM05                       |
        |   +----+ +----+   +----+   +----+   +----+                     |
        |   | Frm| |Ben|   |Risk|   |Res|   |Tran|  (Evaluate, Direct,   |
        |   |work| |efit|   |Opt|   |src |   |sprn|   Monitor)            |
        |   +-+--+ +--+-+   +-+--+   +-+--+   +-+--+                     |
        +-----+-------+-------+-------+-------+--------------------------+
              |       |       |       |       |
   +----------v-------v-------v-------v-------v----------------------+
   |                  MANAGEMENT (35 Obj.)                          |
   |  +----------+  +----------+  +----------+  +----------+         |
   |  |   APO    |  |   BAI    |  |   DSS    |  |   MEA    |         |
   |  | (Align-  |  | (Build-  |  | (Deliver |  | (Monitor |         |
   |  | Plan-Or- |  | Acquire- |  |  Service |  |  Eval-   |         |
   |  | ganize)  |  | Implemt) |  |  Support)|  |  Assess) |         |
   |  | 14 Obj.  |  | 11 Obj.  |  |  6 Obj.  |  |  4 Obj.  |         |
   |  +----------+  +----------+  +----------+  +----------+         |
   +----------------------------------------------------------------+
     APO01(전략) - APO02(거버넌스체) - APO03(아키텍처) - APO04(혁신)
     APO05(포트폴리오) - APO06(예산) - APO07(인력) - APO08(관계)
     APO09(서비스계약) - APO10(공급자) - APO11(품질) - APO12(리스크)
     APO13(보안) - APO14(데이터)
     BAI01(프로그램) - BAI02(요구사항) - BAI03(솔루션) - BAI04(가용성)
     BAI05(조직변화) - BAI06(변경) - BAI07(이행) - BAI08(지식)
     BAI09(자산) - BAI10(구성) - BAI11(프로젝트)
     DSS01(운영) - DSS02(서비스요청) - DSS03(문제) - DSS04(연속성)
     DSS05(보안운영) - DSS06(비즈니스통제)
     MEA01(성과·규제) - MEA02(내부통제) - MEA03(외부감사) - MEA04(보고)
```

### Process Capability Model (PAM/CMMI 통합)

COBIT 2019은 **Process Activity Rating**을 PAM(Process Assessment Model) ISO/IEC 15504-2 기반으로 6단계(L0-Incomplete, L1-Performed, L2-Managed, L3-Established, L4-Predictable, L5-Optimizing)로 평가하며, **Maturity Level은 5단계(Initial->Repeatable->Defined->Managed->Optimizing)**로 산출한다. 각 단계의 핵심 KPI는 다음과 같다.

```text
  Maturity Level 5 (Optimizing)    <- Continuous Improvement
        ^  PI = Process Improvement Plan (12 mo cycle)
        |
  Level 4 (Predictable)            <- Quantitative Mgmt
        ^  Statistical Process Control (SPC), σ 6σ
        |
  Level 3 (Established)            <- Process Standardization
        ^  SOP + RACI + WBS (WBS=Work Breakdown Structure)
        |
  Level 2 (Managed)                <- Project Mgmt
        ^  PMBOK/PRINCE2, Earned Value Mgmt (EVM)
        |
  Level 1 (Performed)              <- Basic Process
        ^  Defined Owner, KPI existence
        |
  Level 0 (Incomplete)             <- Ad-hoc
```

### 구성 요소 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|-----------|------|----------------------|
| **Design Factor** | 조직 맥락 식별·가중치 산정 | 11개 Factor(Enterprise Strategy, Goals, Risk Profile, Issues, Threat, Compliance, Role of IT, IT Adoption, Sourcing, Implementation, Tech Adoption) 입력 -> 40개 목표별 우선순위 산출(0~100점 척도) |
| **Goals Cascade** | 전략->전사->IT->거버넌스 목표 정렬 | 13개 Enterprise Goal(EG) ↔ 13개 Alignment Goal(AG) ↔ 40개 Gov/Mgt Objective(OM) 매핑, RACI Matrix(Responsible, Accountable, Consulted, Informed)로 책임 할당 |
| **7 Components** | 거버넌 시스템 빌딩 블록 | Process·Organizational Structure·Information Flow·People·Policy·Culture·Services/Apps/Infrastructure — NIST CSF의 Function/Category/Subcategory와 N:M 매핑 |
| **Focus Area** | 특정 도메인 심화 거버넌스 | DevOps·Cybersecurity·Privacy·Cloud·Risk·Compliance·Innovation 등 40+개, 각 Focus Area는 3~5개 Governance Objective Subset으로 구성 |
| **Capability/Maturity** | 성과 측정·Gap 분석 | PAM(ISO 15504-2) 6단계 Process Rating, Maturity 5단계 — CMMI Institute 모델과 호환(Gap
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 724 / 800

<- **이전**: [723. IT 경영 관리 핵심 토픽 723번 시험 요약](/studynote/12_it_management/05_security_compliance/723_it_management_core_topic_723_exam_summary/)
**다음**: [725. IT 경영 관리 핵심 토픽 725번 시험 요약](/studynote/12_it_management/05_security_compliance/725_it_management_core_topic_725_exam_summary/) ->

---
