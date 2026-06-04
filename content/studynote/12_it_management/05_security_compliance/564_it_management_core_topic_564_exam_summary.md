+++
title = "564. IT 경영 관리 핵심 토픽 564번 시험 요약 (IT Management Core Topic 564 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# IT 경영 관리 핵심 토픽 564번 시험 요약 — 디지털 전환 시대의 IT 거버넌스 및 전략적 성과관리

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기업 가치 창출을 위해 IT를 전략 자산으로 관리하기 위한 **COBIT 2019 거버넌스 체계(EDM→Align, Plan, Organize→Build, Acquire, Implement→Deliver, Service, Support→Monitor, Evaluate, Evaluate)**, **ISO/IEC 38500 6원칙(DCEE: Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**, 그리고 **IT-BSC(4관점: Financial, Customer, Internal Process, Learning & Growth)**를 통합한 경영 프레임워크.
> 2. **가치**: 거버넌스 체계 도입 시 **IT 투자 ROI 25~40% 향상**(Gartner 2023), **이해관계자 요구 충족률 78%→94%**, **컴플라이언스 위반 60% 감소**, **Time-to-Market 30% 단축** 등 정량적 효과 입증.
> 3. **판단 포인트**: (a) **집중형(중앙) vs 분산형(페더레이션) 거버넌스** 모델 선택, (b) **규범적(Prescriptive) vs 결과기반(Outcomes-based)** 통제 방식, (c) **Quick-Win vs Big-Bang** 도입 전략, (d) **NIST CSF 7-function**과의 매핑 정합성, (e) **ESG/지속가능경영** 거버넌스 통합 여부.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation, DX) 가속화로 기업 IT는 단순 비용 센터에서 **전략적 가치 창출의 핵심 엔진**으로 변모했습니다. 그러나 McKinsey(2023) 조사에 따르면 DX 프로젝트의 **70%만이 비즈니스 목표 달성에 성공**하며, 실패의 주요 원인은 기술 부재가 아닌 **거버넌스·리더십·성과관리 체계의 결여**입니다. IT 관리의 핵심 과제는 "어떤 기술을 도입할 것인가"에서 "**어떻게 IT 의사결정·투자·운영을 기업 전략과 정렬하여 측정·통제할 것인가**"로 이동했습니다.

특히 **클라우드·AI·데이터 거버넌스**의 등장으로 기존의 ITIL/COBIT 5 체계만으로는 한계가 있으며, **COBIT 2019(2018년 12월 발표, 2019년 정식 출시)**, **ISO/IEC 38500:2015(2nd Edition)**, **CMMI V2.0**, 그리고 국내 **클라우드컴퓨팅법·데이터산업법** 등 새로운 규제 환경에 맞는 통합 거버넌스가 요구됩니다.

```text
[ 디지털 전환 시대의 IT 거버넌스 통합 프레임워크 ]

                    ┌─────────────────────────────────┐
                    │    기업 전략 & 비즈니스 목표      │
                    │  (Vision / Mission / OKR)        │
                    └────────────────┬────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │  IT 거버넌스     │  │  IT 전략 및       │  │  IT 성과관리     │
   │  (Governance)    │  │  투자관리         │  │  (Performance)   │
   │                  │  │  (Strategy & PMO) │  │                  │
   │ • COBIT 2019     │  │ • TOGAF 10 ADM    │  │ • IT-BSC 4관점   │
   │ • ISO 38500      │  │ • Zachman FA      │  │ • KPI Tree       │
   │ • NIST CSF 2.0   │  │ • FEAF            │  │ • EVA/NPV 회수   │
   │   7-Function     │  │ • DoDAF           │  │ • SLA/SLM        │
   │ • 3-lines model  │  │ • 포트폴리오 관리  │  │ • CSF Goal Casc. │
   └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
            │                     │                      │
            └─────────────────────┼──────────────────────┘
                                  ▼
                  ┌──────────────────────────────┐
                  │   거버넌스·전략·성과 통합 체계  │
                  │   (Governance-Strategy-       │
                  │    Performance Integration)    │
                  └──────────────────────────────┘
                                  │
        ┌─────────────────┬───────┴───────┬─────────────────┐
        ▼                 ▼               ▼                 ▼
   ┌─────────┐      ┌──────────┐    ┌──────────┐      ┌──────────┐
   │ 측정·모니터│      │ 의사소통·보고 │    │ 위험·컴플 │      │ 지속적 개선 │
   │ (Monitor) │      │ (Communication)│  │ (Risk/Cmp)│      │ (Continuous)│
   └─────────┘      └──────────┘    └──────────┘      └──────────┘
```

**왜 필요한가? — 기존 vs 새로운 패러다임 비교**

| 구분 | 전통적 IT 관리(2000년대 이전) | 디지털 시대 IT 거버넌스(2020년 이후) |
|------|----------------------------|----------------------------------|
| **관점** | IT는 비용·지원 기능 | IT는 가치 창출·전략 자산 |
| **조직** | CIO 단일 리더십 | CDO/CAIO/CCO/CRMO 다기능 리더십 |
| **결정권** | 중앙 집중, 수직적 | 분산형(Edge Computing), 페더레이션 |
| **측정** | 예산 준수율, 가용성 | OKR, NPS, Time-to-Value, ROI/ROIC |
| **위험** | 가용성·보안 중심 | 사이버 회복탄력성, ESG, AI 윤리 |
| **표준** | ITIL v3, COBIT 5 | COBIT 2019, NIST CSF 2.0, ISO 38500:2015 |
| **규제** | SOX, ISMS | 데이터3법, EU AI Act, DORA, 클라우드컴퓨팅법 |

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **한 나라의 헌법과 예산 국회**와 같습니다. 기술(군대)은 강해야 하지만, 헌법(거버넌스) 없이 군대만 강하면 독재가 되고, 의사결정(예산) 절차가 없으면 국가는 혼란에 빠집니다. COBIT는 헌법, ISO 38500은 헌법 정신, IT-BSC는 성과 보고서입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. COBIT 2019 — 거버넌스·관리 체계(Governance & Management Objectives)

COBIT 2019는 **6개의 거버넌스 목적과 35개의 관리 목적(총 40개 목표)**으로 구성되며, **카테고리(5개: Benefits Realization, Risk Optimization, Resource Optimization, Internal Transparency, Stakeholder Focus)**와 **도메인(5개)**의 두 축으로 정렬됩니다.

```text
[ COBIT 2019 핵심 구성 요소 및 상호작용 ]

                    ┌─────────────────────────────────────┐
                    │    COBIT 2019 Core Model             │
                    │  (40 Objectives: EDM×5 + APO×14 +    │
                    │   BAI×11 + DSS×6 + MEA×4)            │
                    └──────────────┬──────────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
      ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
      │  Cascading Goals│ │  Components of  │ │  Focus Areas     │
      │  (13 Enterprise │ │  Governance &   │ │ (40+ specific    │
      │   Goals → 13    │ │  Management     │ │  topics: DevOps,│
      │   Alignment     │ │  System: Process│ │  Cybersecurity,  │
      │   Goals → 40    │ │  /Structure/    │ │  Privacy, Cloud, │
      │   Governance/   │ │  Information/   │ │  Digital Ethics, │
      │   Mgmt Goals)   │ │  People/Skill/  │ │  ESG, RPA, etc.) │
      │                 │ │  Service/Infr/  │ │                  │
      │                 │ │  Policy/Culture)│ │                  │
      └─────────────────┘ └─────────────────┘ └─────────────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                  ┌─────────────────────────────────┐
                  │  Design Factors (11가지 설계요인)│
                  │  ─────────────────────────────  │
                  │ ① Enterprise Strategy           │
                  │ ② Enterprise Goals (13개)       │
                  │ ③ Risk Profile                  │
                  │ ④ I&T-related Issues            │
                  │ ⑤ Threat Landscape              │
                  │ ⑥ Compliance Requirements        │
                  │ ⑦ Role of IT                    │
                  │ ⑧ IT Implementation Methods     │
                  │ ⑨ Technology Adoption Strategy  │
                  │ ⑩ Enterprise Size               │
                  │ ⑪ Industry/Market               │
                  └─────────────────────────────────┘
```

### 나. ISO/IEC 38500:2015 — IT 거버넌스 6대 원칙(DCEE 원칙)

| 원칙 | 영문 | 핵심 의미 | 실무 적용 |
|------|------|----------|----------|
| **① 책임 (Responsibility)** | Responsibility | IT 의사결정에 대한 명확한 책임 소재 | 이사회→CEO→CIO 책임 위임 체계, RACI 매트릭스 |
| **② 전략 (Strategy)** | Strategy | IT가 조직의 전략·목표와 부합 | IT-Strategy Map(전략 맵), 3-Year IT Strategy Plan |
| **③ 획득 (Acquisition)** | Acquisition | IT 투자는 적절한 의사결정 기반으로 | BOCR 분석, NPV/IRR/회수기간, 벤더 평가 |
| **④ 성과 (Performance)** | Performance | IT가 비즈니스 요구 충족 | IT-BSC, SLA/SLM(Service Level Management) |
| **⑤ 적합성 (Conformance)** | Conformance | IT가 외부·내부 법규 준수 | ISMS, PIPC, ISO 27001, ESG 보고 |
| **⑥ 인간 행동 (Human Behavior)** | Human Behavior | IT 의사결정이 인간·문화 존중 | 변화관리(Kotter 8단계), ADKAR 모델 |

### 다. IT-BSC(Balanced Scorecard) — Norton & Kaplan 확장 모델

| 관점 | 핵심 질문 | KPI 예시 (재무 30%, 고객 25%, 프로세스 25%, 학습 25%) |
|------|----------|--------------------------------------------------------|
| **재무(Financial)** | "IT가 재무적 가치를 창출하는가?" | IT ROI(%), 비용 회수율, EVA(Economic Value Added) |
| **고객(Customer)** | "내·외부 고객 가치를 높이는가?" | 사용자 만족도(CSAT), NPS, 비즈니스 능력 향상도 |
| **내부 프로세스(Internal Process)** | "효율적 IT 운영인가?" | 인시던트 해결률(MTTR), 변경 성공률, 가용성(99.9%) |
| **학습·성장(Learning & Growth)** | "미래 역량·인재에 투자하는가?" | 직원 역량 지수, 혁신 프로젝트 수, 지식 공유 KPI |

### 라. 핵심 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회(Board) / IT 전략위원회** | 거버넌스 최고 의사결정 기구, EDM 도메인 소유 | 전략 연계·리스크 감독, 정관/이사회 운영규정에 명시, 분기별 회의, MECE 의사결정 |
| **CIO(Chief Information Officer)** | IT 전략·거버넌스 총괄, CDO·CAO 등 신규 직능과 Co-Governance | C-Level 보고(통상 CEO 직보), 3-Year Roadmap, Portfolio Prioritization(BOCR·AHP) |
| **PMO(Project Management Office)** | 프로젝트·프로그램·포트폴리오(3P) 관리 중추 | EPMO/EPMO+ 모델, Stage-Gate, P3O(Portfolio, Programme, Project Office) 프레임워크, KPI 대시보드 |
| **BSC/KPI 시스템** | 전략→목표→측정지표로 계단식 정렬(Cascading) | OKR+BSC 하이브리드, 실시간 대시보드(Tableau/Power BI/Qlik), 분기별 성과 리뷰 |
| **SLA/OLA(Service Level Agreement/Operation Level Agreement)** | IT 서비스 품질 계약, 내부·외부·다단계 | OLAP(Service Catalog→SLA→OLA→UC), 99.9% 가용성, 1시간 MTTD/4시간 MTTR, 손해배상 조항 |
| **위험·컴플라이언스 관리(Risk & Compliance)** | NIST CSF 2.0 7-Function(Identify, Protect, Detect, Respond, Recover, Govern, Recover-test) 매핑 | ISO 31000(리스크 관리), ISO 27001:2022 Annex A 93통제, RMF(발견→평가→대응→모니터링) |
| **아키텍처 거버넌스(EA Governance)** | TOGAF 10 ADM(8단계: Preliminary→Vision→Business→IS→Tech→Opportunity→Migration→Implementation→Change) | ArchiMate 3.2 6-Layer(Strategy/Business/Application/Technology/Physical/Implementation), 레퍼런스 모델 |
| **지속적 개선(CSI: Continual Service Improvement)** | ITIL 4 7가지 지렛대(Technology, Information, Strategy, Supplier, People, Process, Value) | PDCA, Deming Cycle, CSI Register, 4-P(Model/Plan→Do→Check→Act 통합) |

### 마. 핵심 알고리즘·수식 — IT 투자 우선순위 결정 모델

**(1) BOCR(Benefit, Opportunity, Cost, Risk) 분석 — Saaty AHP 확장**

- 우선순위 점수 = (B × wB + O × wO) / (C × wC + R × wR)
- wB, wO, wC, wR: AHP 쌍대비교를 통한 가중치(Σ=1)
- **AHP 일관성 비율(CR) < 0.1** 일 때 신뢰 가능
- 예: 클라우드 마이그레이션 BOCR 점수 = (8×0.4 + 7×0.2) / (5×0.25 + 4×0.15) = 4.6 / 1.85 = **2.49**

**(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 564 / 800

← **이전**: [563. IT 경영 관리 핵심 토픽 563번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/563_it_management_core_topic_563_exam_summary/)
**다음**: [565. IT 경영 관리 핵심 토픽 565번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/565_it_management_core_topic_565_exam_summary/) →

---
