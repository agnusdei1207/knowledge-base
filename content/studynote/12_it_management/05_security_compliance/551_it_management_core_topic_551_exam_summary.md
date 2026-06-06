---
title: "IT Management Core Topic 551 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019, ISO/IEC 38500, ITIL 4 등 글로벌 거버넌스 프레임워크를 기반으로 **Value Governance(가치 거버넌스)** 관점에서 IT를 경영 자원으로 편입시켜, 거버넌스-전략-포트폴리오-프로젝트-운영-성과측정의 End-to-End 체인을 구축하는 통합 관리 체계이다.
> 2. **가치**: McKinsey(2023) 보고에 따르면 디지털 트랜스포메이션(DX) 성공 기업 대비 실패 기업의 ROI 격차가 35% 이상 벌어지며, 성숙도 Level 3 이상의 IT 거버넌스 체계 보유 시 IT 투자 대비 사업 성과(Operating Margin) 약 2.4배, Time-to-Market 40% 단축 효과가 검증된다(전사아키텍처 EA-KI 2024).
> 3. **판단 포인트**: 기술사는 **"거버넌스 모델(중앙집중형 CoE vs 분산형 Federation vs 하이브리드), 투자 우선순위 프레임워크(포트폴리오 Quadrant), 성과측정 모델(BSC 4관점 vs OKR), 변화관리(ADKAR vs Kotter 8단계)"**의 트레이드오프를 사업·기술·조직 맥락에서 정량적 근거로 판단할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원 역할(SOA·업무 자동화)에서 벗어나, **"Digital Business Platform"** 시대로 전환되면서 IT는 더 이상 CIO 산하의 한 기능이 아니라 **CDO(Chief Digital Officer)·CEO·CFO와 동등한 거버넌스 주체**가 되었다. 한국은 2013년 「클라우드컴퓨팅법」, 2020년 「데이터 3법」(개인정보보호법·정보통신망법·신용정보법 개정), 2022년 「지능형 정부 기본법」, 2024년 AI 기본법(안)을 통해 IT 거버넌스의 법적·제도적 토대를 강화해 왔다. 또한 2025년 현재 「전자정부법」 시행령 개정으로 **공공기관 EA·데이터·AI 거버넌스의 3축 의무화**가 본격 적용된다.

기존 패러다임은 개별 시스템 단위의 SLM(Service Level Management)에 머물렀으나, 현대는 **E2E(End-to-End) 가치 흐름(Value Stream)** 관점에서 IT를 관리한다. 이는 ITIL v3의 "Service Strategy -> Design -> Transition -> Operation -> Continual Improvement" 라이프사이클을 ITIL 4의 **Service Value System(SVS)** + **34개 Practice** + **Value Stream**으로 확장시켰고, COBIT 2019는 40개 Governance/Management Objective를 5개 도메인(EDM·APO·BAI·DSS·MEA)으로 재편해 **"Governance System Principle(6개 원칙) + Governance Framework(컴포넌트 7개) + Focus Area(연속적 변화)"** 구조로 전환되었다.

```text
[ IT 경영관리 3대 거버넌스 통합 체계 (EA · ITIL · COBIT Convergence) ]

                    +--------------------------------------------+
                    |   Board / Steering Committee (이사회/IT전략위) |
                    |   - ISO 38500 6 Principle 준수 감독            |
                    |   - IT 성과 최종 책임                          |
                    +--------------------+-----------------------+
                                         | (EDM: Evaluate, Direct, Monitor)
            +----------------------------+----------------------------+
            v                            v                            v
   +-----------------+         +-----------------+         +-----------------+
   |  Strategy Layer |         |  Portfolio Layer|         | Operation Layer |
   |  (전략/계획)     |         |  (투자/우선순위) |         |  (운영/서비스)   |
   | --------------- |         | --------------- |         | --------------- |
   | • ISP/BPR       |         | • PMO          |         | • ITIL 4 SVS    |
   | • EA(TOGAF)     |         | • Portfolio    |         | • AIOps/Observ. |
   | • Digital       |         |   Quadrant     |         | • FinOps        |
   |   Strategy      |         | • Benefits      |         | • SRE/SLI/SLO   |
   |                 |         |   Realization  |         |                 |
   +--------+--------+         +--------+--------+         +--------+--------+
            | APO (Align, Plan, Organize)|                            | DSS (Deliver)
            +------------+---------------+------------+---------------+
                         v                            v
                +--------------------+      +--------------------+
                |  Project Layer     |      |  Risk & Security   |
                |  (BAI: Build..)    |      | ------------------|
                |  • PMBOK 7         |      | • ISMS-P           |
                |  • Agile@Scale     |      | • ISO 27001/27701  |
                |  • DevSecOps       |      | • Risk=N×I×C       |
                +--------------------+      +--------------------+
                                          |
                                          v
                                +--------------------+
                                |  MEA (Monitor,     |
                                |  Evaluate, Assess) |
                                |  • BSC · KPI · OKR |
                                |  • IT Audit · 감리 |
                                +--------------------+
```

**왜 필요한가 (Old vs New Paradigm)**

| 구분 | Legacy Paradigm (1990~2010) | Modern Paradigm (2015~) |
|---|---|---|
| **관점** | IT는 Cost Center (비용 부서) | IT는 Value Driver (가치 동인) |
| **관리 단위** | 개별 Application, Server | Value Stream, Business Capability |
| **거버넌스 모델** | 중앙 CIO 독점형 | 분산형(Federation), Two-Speed IT, Bimodal |
| **성과 측정** | Uptime, 응답시간 중심 | NPS, CX, Time-to-Market, ROIC |
| **변화 속도** | Waterfall, 3~5년 주기 | Agile, Lean, Continuous Delivery |
| **위험 관리** | 사후 통제(Detect) | 사전 예방(Shift-Left) + 회복력(Resilience) |
| **한국 법·제도** | 전산장비 도입 위주 | 데이터·AI·플랫폼 거버넌스 의무화 |

- **📢 섹션 요약 비유**: IT 경영관리는 **"스마트시티의 도시계획"**과 같다. 도로(인프라)·치안(보안)·교통(프로세스)·예산(투자)을 통합적으로 설계하지 않으면, 빌딩(시스템)은 지어져도 도시 전체는 혼란에 빠진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 3대 프레임워크 (Trinity Framework)

```text
[ COBIT 2019 × ITIL 4 × ISO/IEC 38500 3-Layer Integration ]

   +---------------------------------------------------------------+
   | ISO/IEC 38500 — "WHY & WHO" (거버넌스의 철학적 토대)            |
   |  • 6 Principles: Responsibility, Strategy, Acquisition,       |
   |    Performance, Conformance, Human Behavior                    |
   |  • "Govern" 3-Task: Evaluate -> Direct -> Monitor               |
   +-----------------------------+---------------------------------+
                                 |  거버넌스 원칙 제공
                                 v
   +---------------------------------------------------------------+
   | COBIT 2019 — "WHAT" (40 Governance/Management Objective)      |
   |  • 5 Domain: EDM, APO, BAI, DSS, MEA                          |
   |  • 7 Component: Principles·Goals·Process·Org·Info·Skill·Tool |
   |  • 11 Design Factor (Enterprise Strategy, Threat, Sourcing…)  |
   |  • Focus Area: SME, DevOps, Risk, Cybersecurity, AI, ESG…    |
   +-----------------------------+---------------------------------+
                                 |  목표/측정항목 구체화
                                 v
   +---------------------------------------------------------------+
   | ITIL 4 — "HOW" (Service Value System 운영·실행)                |
   |  • SVS: Opportunity/Demand -> Value -> SVS -> Value             |
   |  • 4 Dimension: Org·People·Info·Tech·Partners·Value Streams  |
   |  • 34 Practice: Incident, Change, Service Desk, SLO…         |
   +---------------------------------------------------------------+
```

### 2. 핵심 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **EDM (Evaluate, Direct, Monitor)** | 이사회·IT전략위원회 수준 거버넌스 | COBIT 2019 EDM01~05; 성과 목표 정의, 위험 appetite 설정, 모니터링·개선 지시. RACI Matrix: **Accountable=이사회, Responsible=CIO, Consulted=CFO/CDO, Informed=사업부** |
| **APO (Align, Plan, Organize)** | 전략 정렬·투자 계획·조직 설계 | APO01~14; ISP(정보화 전략 계획), 포트폴리오 분류(BCG Matrix 변형), 거버넌스 시스템 설계 11 Design Factor, **TOGAF ADM Phase A~C** 연결 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축 및 변경 | BAI01~11; PMBOK 7th (8 Performance Domain), Agile@Scale (SAFe/LeSS/Disciplined), DevSecOps 파이프라인, V-Model, TDD/ATDD |
| **DSS (Deliver, Service, Support)** | 서비스 운영·지원 | DSS01~06; **ITIL 4 34 Practice** 매핑, AIOps·Observability(ELK·Prometheus·Grafana), SRE Error Budget, **FinOps** (클라우드 비용 최적화) |
| **MEA (Monitor, Evaluate, Assess)** | 성과·내부통제·감사·준수 | MEA01~04; **BSC 4관점 KPI** (재무·고객·내부프로세스·학습성장), **OKR** (Objectives & Key Results), 내부감사(3 Lines Model: 1st=사업부, 2nd=준수·리스크, 3rd=내부감사), 정보시스템 감리 |
| **SLA / OLA / UC** | 서비스 수준 협약 | **SLA(외부) – OLA(내부 팀간) – UC(Underpinning Contract, 외부 벤더)**, **SLI(지표) -> SLO(목표) -> Error Budget(허용오차)** 구조, **9-Step SLA Design** (ISO/IEC 20000-1:2018) |
| **EA (Enterprise Architecture)** | 전사 아키텍처 정렬 | **TOGAF ADM 10 Phase**(Preliminary~Requirements Mgmt), **EA-KI**(한국행정안전부 표준 프레임워크), Zachman 6×6 Matrix, **ArchiMate 3.2** 표기법, Capability Map -> Value Stream -> Application/Technology 매핑 |

### 3. 핵심 알고리즘·모델 (기술사 빈출)

- **BSC (Balanced Scorecard)**: Kaplan·Norton 4관점(Financial, Customer, Internal Process, Learning & Growth) + Strategy Map(인과관계 링크). 2010년 이후 **"Sustainability BSC 5th Perspective"** 추가 -> ESG 통합.
- **OKR**: Intel·Google 방식, **Objective(질적) + 3~5 Key Results(정량)**, 분기 단위, "Stretch Goal(도전 목표 0.7달성률=정상)" 원칙. BSC와의 차이: OKR은 **Alignment + Stretch**, BSC는 **Cascading + Balance**.
- **Six Sigma / DMAIC**: D(Define)->M(Measure)->A(Analyze)->I(Improve)->C(Control), DPMO(Defects Per Million Opportunities) 기반, 6σ ≈ 3.4 DPMO. IT 적용 시 **DPMO × Cost of Defect**로 ROI 산출.
- **IT Portfolio Quadrant**: McFarlan·McKenney `Strategic Grid`(Support / Factory / Turnaround / Strategic) + Gartner `Magic Quadrant` 변형으로 **High Impact·High Risk** 프로젝트 우선 투자 의사결정.
- **Risk = Likelihood × Impact** (COBIT 2019는 추가 × Vulnerability / 또는 Inherent Risk - Control Effectiveness = Residual Risk)
- **COBIT 2019 11 Design Factor**: 기업전략, 목표달성 이슈, 위험 프로파일, 거버넌스 사고 관련 이슈, 위협 환경, 준수 요구, IT 역할, IT outsourcing, 구현 방식, 기술 도입 전략, **Enterprise Size**(SME 4종 / Large Enterprise 1종) -> **Customized Governance System** 도출.
- **TOGAF ADM**: Preliminary -> A(Vision) -> B(Business) -> C(Info Systems) -> D(Technology) -> E(Opportunities) -> F(Migration) -> G(Implementation) -> H(Change Mgmt) -> R(Requirements) — 각 Phase 산출물 50여 종(Architecture Definition Document, Architecture Roadmap, Transition Architecture 등).
- **FinOps**: Inform(가시화) -> Optimize(최적화) -> Operate(자동화), **예측비용 vs 실제비용 단위(unit economics)**, **Showback / Chargeback** 모델.

- **📢 섹션 요약 비유**: ISO 38500은 **헌법**, COBIT 2019는 **민법/형법(전체 법체계)**, ITIL 4는 **실무 매뉴얼(판례·지침)**, EA는 **도시계획도**이며, BSC/OKR는 **성과측정 계기판**이다.

---

## Ⅲ. 비교 및 연결

### 1. 거버넌스 프레임워크 비교

| 구분 | COBIT 2019
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 551 / 800

<- **이전**: [550. IT 경영 관리 핵심 토픽 550번 시험 요약](/studynote/12_it_management/05_security_compliance/550_it_management_core_topic_550_exam_summary/)
**다음**: [552. IT 경영 관리 핵심 토픽 552번 시험 요약](/studynote/12_it_management/05_security_compliance/552_it_management_core_topic_552_exam_summary/) ->

---
