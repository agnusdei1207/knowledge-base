---
title: "Project Management PMBOK Application"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PMBOK는 PMI가 발간하는 프로젝트 관리 지식 체계로, 7th Edition(2021)에서 5 Process Groups × 10 Knowledge Areas의 프로세스 기반에서 **12 Principles of Project Management + Value Delivery System** 원칙 기반으로 패러다임이 전환되었으며, 프로젝트 성공을 "Triple Constraint(Scope·Schedule·Cost)" 충족에서 "Value Delivery" 관점으로 재정의함.
> 2. **가치**: PMI의 *Pulse of the Profession 2023* 보고에 따르면 PMBOK 기반 표준화된 프로젝트 관리는 **스케줄 초과 28% 감소, 예산 초과 24% 감소, 실패율 21% 절감** 효과를 제공하며, 특히 EVM·Risk Register·WBS 도입 시 ROI가 평균 3.5배(Forrester Research) 향상됨.
> 3. **판단 포인트**: **Predictive(Waterfall) / Iterative / Adaptive(Agile) / Hybrid** 4가지 개발 라이프사이클 중 프로젝트 특성(불확실성·규제성·변경빈도)에 따라 **Tailoring** 해야 하며, IT 시스템 구축 시 Agile 도입 압력과 PMBOK의 체계성을 융합한 **Hybrid(예: SAFe + PMBOK Governance)** 적용 여부가 핵심 의사결정임.

---

## Ⅰ. 개요 및 필요성

IT 프로젝트의 실패율은 업계 통계(Standish Group CHAOS Report 2023)에 따르면 **전체 IT 프로젝트의 약 30%가 실패, 50%가 부분 실패** 상태이며, 그 핵심 원인은 (1) 요구사항 불명확, (2) 이해관계자 갈등, (3) 위험 관리 부재, (4) 변경 통제 미흡으로 분석됩니다. PMBOK는 이러한 문제를 해결하기 위해 PMI(Project Management Institute)가 1996년 1판을 발간한 이래 5차 개정(2013, 6th Edition: 5 Process Groups + 10 Knowledge Areas + 49 Processes)을 거쳐 **2021년 7th Edition에서 원칙(Principles) 기반 접근**으로 전환되었습니다.

특히 7th Edition은 Agile·DevOps·Lean 등 현대 프로젝트 환경 변화에 대응하여, 8개 Performance Domains(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)과 12개 원칙(예: "Be a diligent, respectful, and caring steward", "Build shared understanding")을 통해 **"How to manage"보다 "Why we manage"** 관점을 강조합니다.

```text
+-------------------------------------------------------------------------+
|            PMBOK 7th Edition Value Delivery System                      |
+-------------------------------------------------------------------------+
                                  |
        +-------------------------+-------------------------+
        v                                                    v
   [Inputs/Outputs]                                  [Business Value]
   • Strategy Docs                                   • Utility + Warranty
   • Market Conditions                               • Net Present Value
   • Stakeholder Needs                               • Customer Satisfaction
        |                                                    ^
        v                                                    |
   +--------------------------------------------------------------+
   |                  Organizational Strategy                     |
   +-------------+---------------------+--------------------+---+
                 v                     v                    v
           [Portfolio]           [Programs]            [Projects]
                 |                     |                    |
                 v                     v                    v
        Strategic Benefits      Tactical Benefits     Operational Benefits
                 +---------------------+--------------------+
                                       v
                              [Operations / Sustainment]
                                       |
                                       v
                              [Continuous Value]
```

**Old vs New Paradigm**:
- **Old(6th Edition, 2017)**: Process-based · 49 Processes · 10 KAs · Waterfall 친화적 · ITTO(Input·Tool·Technique·Output) 중심
- **New(7th Edition, 2021)**: Principles-based · 12 Principles · 8 Performance Domains · Agile/Adaptive 내재화 · Value 중심

- **📢 섹션 요약 비유**: PMBOK 6판이 "정해진 레시피대로 요리하는 요리책"이었다면, PMBOK 7판은 **"어떤 상황에서도 좋은 음식을 만들기 위한 12가지 미식의 원칙(Principle)"** 입니다. 레시피(Process)만 따르면 요리가 완성되지만, 원칙(Principle)은 요리사가 시장 상황(Agile/Regulated)에 맞춰 창의적으로 응용할 수 있게 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PMBOK 7th Edition의 핵심 구조는 **12 Principles of Project Management**, **8 Project Performance Domains**, **Value Delivery System**의 3대 축으로 구성됩니다. IT 프로젝트에서 이를 적용할 때는 PMBOK의 거버넌스 체계(Charter, WBS, EVM, Risk Register)와 Agile의 실행 메커니즘(Sprint, Backlog, Retrospective)을 통합한 Hybrid 모델이 실질적 운영 프레임워크가 됩니다.

```text
+-----------------------------------------------------------------------+
|          PMBOK 7th 12 Principles × 8 Performance Domains              |
+-----------------------------------------------------------------------+
                    +--------------------------+
                    |  12 Project Management   |
                    |      Principles          |
                    |  (Why we do)             |
                    +------------+-------------+
                                 | (Guides)
                                 v
+-----------------------------------------------------------------------+
|  8 Project Performance Domains (How we do)                            |
+-----------------------------------------------------------------------+
|  1. Stakeholders  | 5. Project Work    | 7. Measurement               |
|  2. Team          | 6. Delivery        | 8. Uncertainty (Risk)        |
|  3. Development   | 4. Planning        |                              |
|     Approach      |                    |                              |
+-----------------------------------------------------------------------+
                                 |
                                 v
                +--------------------------------+
                |  Value Delivery Outcomes      |
                |  • Business Value Achievement |
                |  • Stakeholder Satisfaction    |
                |  • Product/Service Quality     |
                +--------------------------------+

        [Cross-cutting IT Toolchain Integration]
        +------------------------------------------+
        |  JIRA/Azure DevOps / GitLab / MS Project |
        |  Confluence · Power BI · ServiceNow      |
        |  SonarQube · Selenium · Prometheus       |
        +------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **5 Process Groups (6th)** | 프로젝트 전生命周期 관리 | **Initiating**(Charter, ID Stakeholders) -> **Planning**(WBS, Schedule, Budget) -> **Executing**(Team Direction, Procurement) -> **Monitoring & Controlling**(EVM, CCB) -> **Closing**(Lessons Learned). IT 시스템 구축 시 Waterfall·Iterative 모델에서 **Phase Gate Review** 단위로 적용. |
| **10 Knowledge Areas (6th)** | 전문 영역별 관리 기법 | **Integration**(PM Plan, Change Control) · **Scope**(WBS, Requirements Traceability Matrix) · **Schedule**(CPM, PDM Network) · **Cost**(EVM, BAC/EAC) · **Quality**(QA/QC, Six Sigma) · **Resource**(RACI Matrix, Resource Histogram) · **Communications**(Comm. Mgmt Plan, Push/Pull/Interactive) · **Risk**(Qualitative/Quantitative Analysis, Monte Carlo) · **Procurement**(Make-or-Buy Analysis, Contract Types FFP/FP/T&M/CPFF) · **Stakeholder**(Engagement Assessment Matrix). |
| **12 Principles (7th)** | 프로젝트 수행 철학 및 가치 판단 | ① Steward(책임감) ② Team(팀) ③ Development Approach(개발 방식) ④ Planning(계획) ⑤ Work(작업) ⑥ Delivery(전달) ⑦ Measurement(측정) ⑧ Uncertainty(불확실성) ⑨ Tailoring(맞춤) ⑩ Quality(품질) ⑪ Complexity(복잡성) ⑫ Risk(위험) · *Change* (각 에디션 미세 차이). |
| **8 Performance Domains (7th)** | 프로젝트 실행 핵심 영역 | Stakeholder Engagement, Team Performance, Development Approach(Adaptive/Predictive/Hybrid 선택), Planning(Delivery Cadence), Project Work(Manage Issues, Changes), Delivery(Scope/Quality), Measurement(KPI/OKR), Uncertainty(Risk Opportunity). |
| **Value Delivery System** | 조직 차원의 가치 흐름 | Portfolio -> Program -> Project -> Operations -> Sustainment -> Disposal로 이어지는 가치 사슬, IT에서는 **Project -> Hypercare -> BAU(Business As Usual)** 운영 모델로 매핑. |
| **Tailoring** | 프로젝트별 최적화 | 6th의 49개 Process 또는 7th의 Principles·Domains를 **경험적·규제적·문화적** 요인에 따라 가감. 예: 금융권은 DORA/BSA Compliance를 위해 Predictive 비중^, 스타트업은 Adaptive 100% 적용. |
| **Earned Value Management (EVM)** | 성과 정량 측정 | `EV = % Complete × BAC`, `CV = EV - AC`, `SV = EV - PV`, `CPI = EV/AC`, `SPI = EV/PV`. IT 프로젝트에서 CPI<0.85, SPI<0.85이면 **자동 Risk Escalation** 트리거. |
| **Risk Register & Monte Carlo** | 확률론적 위험 분석 | PERT β분포(Optimistic/Most Likely/Pessimistic) 기반 **@Risk**, **Crystall Ball** 도구로 S-Curve 도출. IT 신규 시스템 도입 시 **P80 일정(80% 확률로 준수 가능한 일정)** 채택이 업계 표준. |

### PMBOK 6th Edition 49 Processes (대표 예)

| Knowledge Area | Initiating | Planning | Executing | M&C | Closing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Integration** | Develop Project Charter | Develop Project Mgmt Plan | Direct & Manage Project Work | Monitor & Control Project Work, Perform Integrated Change Control | Close Project or Phase |
| **Scope** | - | Plan Scope Mgmt, Collect Requirements, Define Scope, Create WBS | Validate Scope | Control Scope | - |
| **Schedule** | - | Plan/Define/Sequence Activities, Estimate Activity Durations, Develop Schedule | - | Control Schedule | - |
| **Cost** | - | Plan Cost Mgmt, Estimate Costs, Determine Budget | - | Control Costs | - |
| **Quality** | - | Plan Quality Mgmt | Manage Quality | Control Quality | - |
| **Resource** | - | Plan Resource Mgmt, Estimate Activity Resources | Acquire/Develop/Manage Team | Control Resources | - |
| **Communications** | - | Plan Communications Mgmt | Manage Communications | Monitor Communications | - |
| **Risk** | - | Plan Risk Mgmt, Identify Risks, Qualitative/Quantitative Analysis, Plan Risk Responses | Implement Risk Responses | Monitor Risks | - |
| **Procurement** | - | Plan Procurement Mgmt | Conduct Procurements | Control Procurements | - |
| **Stakeholder** | Identify Stakeholders | Plan Stakeholder Mgmt | Manage Stakeholder Engagement | Monitor Stakeholder Engagement | - |

### IT 도구 통합 매핑

| PMBOK Process | 대표 IT 도구 | 활용 방식 |
| :--- | :--- | :--- |
| Develop WBS | **MS Project, Smartsheet, Monday.com** | Deliverable-Oriented WBS Dictionary 작성, OBS(Organization Breakdown Structure) 연동 |
| Earned Value | **Primavera P6, Deltek Cobra** | EAC(Estimate At Completion) = BAC/CPI 산출, 자동 Dashboard |
| Risk Register | **JIRA Risk Plugin, Azure DevOps Boards, Active Risk Manager** | Prob/Impact Matrix, Heat Map 시각화 |
| Change Control | **ServiceNow ITSM, ServiceDesk Plus** | RFC(Request For Change) -> CCB 승인 -> Build/Deploy 연동 |
| Stakeholder Engagement | **Power BI Stakeholder Matrix, Lucidspark** | Power/Interest Grid, Engagement Assessment Matrix |
| Lessons Learned | **Confluence, Notion, SharePoint** | 프로젝트 종료 시 Knowledge Base 축적, AI 검색 인덱싱 |

- **📢 섹션 요약 비유**: PMBOK 6판의 49개 프로세스는 **"비행기의 계기판 49개"** 와 같습니다. 이륙 전(Planning)·비행 중(Executing)·착륙 후(Closing) 모든 순간을 측정합니다.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 432 / 800

<- **이전**: [431. IT 인력 관리 역량 모델 교육](/studynote/12_it_management/05_security_compliance/431_it_human_resource_capability_model/)
**다음**: [433. 프로그램 관리 포트폴리오 최적화](/studynote/12_it_management/05_security_compliance/433_program_management_portfolio_optimization/) ->

---
