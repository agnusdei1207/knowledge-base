+++
title = "780. IT 경영 관리 핵심 토픽 780번 시험 요약 (IT Management Core Topic 780 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT경영관리는 COBIT 2019(거버넌스·관리목표 40개), ITIL 4(Service Value System 34개 실무 권고), ISO/IEC 38500(6원칙), PMBOK 7(8개 성과영역) 등 글로벌 프레임워크를 기반으로 IT 전략-거버넌스-포트폴리오-서비스-프로젝트-운영-리스크를 End-to-End로 정렬(Alignment)하는 경영체계임.
> 2. **가치**: McKinsey 2023 보고 기준 잘 정렬된 IT조직은 EBITDA 마진 11%p, Time-to-Market 60% 단축, IT 예산 대비 Business Value ROI 평균 4.2배 달성하며, 미성숙 조직 대비 감사 지적사항 73% 감소 및 보안사고 복구시간(MTTR) 4.1시간 → 47분으로 단축.
> 3. **판단 포인트**: 중앙집권(CoE) vs 분권(BU별 IT), Build vs Buy vs Borrow(클라우드 SaaS), Agile@Scale(Spotify 모델 vs SAFe), Zero Trust vs 경계보안, CapEx→OpEx 전환 시 SLA·TCO·Exit Clause 설계, 그리고 BSC 4관점(재무/고객/내부/학습성장) 지표 간 인과관계(Cause-Effect Chain) 검증이 핵심 Trade-off.

---

## Ⅰ. 개요 및 필요성

정보기술의 역할이 단순 업무자동화(Back-office 지원)에서 디지털 비즈니스 코어(매출 직접 발생, Operating Model 자체를 재정의)로 이동함에 따라, IT경영관리는 "비용센터 통제"가 아닌 "가치공급(Value Delivery)을 위한 전략 자산화"로 패러다임이 전환되었습니다. 4차 산업혁명 이후 780번 시험 범위에서 가장 빈도 높은 키워드는 ①디지털전환(DX) 거버넌스, ②데이터 기반 의사결정, ③사이버 리스크, ④IT-OT-IT-PT 융합, ⑤ESG-친화 그린 IT이며, 전통적 EDP 감사를 넘어 전략적 포트폴리오 관리, EA(Enterprise Architecture) 정합성, 정보보호 인증(ISO 27001/27701/42001) 사후 관리까지를 다룹니다.

특히 클라우드 전환, 생성형 AI(LLM), SaaS 확산으로 IT자산의 경계가 사라지면서, **"누가, 무엇을, 어떤 권한으로, 어떤 데이터를, 어떻게 통제하는가"**라는 거버넌스 문제가 CFO·CDO·CISO·CIO 4-CXO 협업 이슈로 격상되었습니다. 이에 780번 시험은 단순 암기형이 아닌, **주어진 시나리오에서 최적의 프레임워크(COBIT vs ITIL vs ISO38500)를 선택·통합하고, 정량적 KPI·ROI·TCO를 산출하여 경영진에게 보고하는 능력**을 평가합니다.

```text
[ IT경영관리 5대 영역 통합 프레임워크 (상위→하위) ]

┌──────────────────────────────────────────────────────────────┐
│  Tier 1: 전략(Strategy) ─ BSC, IT전략맵, 중장기 로드맵       │
│           ↓ (Strategy↔IT Alignment)                          │
│  Tier 2: 거버넌스(Governance) ─ COBIT 2019, ISO 38500       │
│           ↓ (Portfolio Prioritization)                       │
│  Tier 3: 포트폴리오(Portfolio) ─ Portfolio Mgmt, BOB(Best  │
│           of Breed), Build/Buy/Borrow 의사결정               │
│           ↓ (Program/Project Authorization)                  │
│  Tier 4: 실행(Delivery) ─ PMBOK/PRINCE2/SAFe, ITIL 4        │
│           ↓ (Operational Integration)                        │
│  Tier 5: 운영·서비스·리스크 ─ ITSM, SLA, ISO 27001, BCP/DR  │
└──────────────────────────────────────────────────────────────┘
       ↑ 모든 Tier에서 측정·개선:  KPI Tree, PDCA, Audit
       ↑ ESG·AI 윤리·정보보호는 Cross-cutting Concern
```

기존 패러다임(1960~1990 EDP 시대)은 **"프로젝트 성공 = 예산·일정·범위(Success Triangle) 3대 제약 충족"**이었습니다. 그러나 현대(2020~)는 **"프로젝트 성공 = Benefits Realization(실질적 사업가치 실현) + 사용자 채택(Adoption) + 운영안정성"**으로 정의되며, PMBOK 7th(2021)는 "Project = Temporary endeavor to deliver value"로 재정의, **Value Delivery Focus**가 절대 원칙이 되었습니다.

- **📢 섹션 요약 비유**: IT경영관리는 마치 **"항공우주 프로그램의 PMO(Program Management Office)"**와 같습니다. 단순히 우주선(프로젝트)을 잘 만드는 것이 아니라, NASA 전체 미션 전략(거버넌스) ↔ 발사체 라인업(포트폴리오) ↔ 다중 프로젝트(아폴로·아르테미스) ↔ 발사·관제(운영)까지 전체 Value Chain을 통합 운영하는 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 (Control Objectives for Information and Related Technologies)

COBIT 2019는 **거버넌스 시스템(5개 영역, 40개 Governance/Management Objective)**과 **핵심 모델(Principles, Goals Cascade, Components, Focus Areas, Design Factors)**로 구성된 프레임워크입니다. **Goals Cascade** 메커니즘은 Stakeholder Needs → Enterprise Goals(13개) → Alignment Goals(13개) → Management Objectives(40개)로 흘러내려가며, 각 단계는 1:N 매핑이 아닌 **다대다(M:N)** 관계입니다.

### 2. ITIL 4 (Information Technology Infrastructure Library)

ITIL 4는 2019년 출시되어 **Service Value System(SVS)** 중심으로 재설계되었습니다. 핵심은 **"Value는 수요(Provider)와 공급(Consumer)의 공동 창조(Value Co-creation)"**이며, 7가지 guiding principle(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize)을 통해 34개 실무 권고(Practice)를 운영합니다.

### 3. ISO/IEC 38500 (IT Governance International Standard)

ISO 38500은 **6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 이사회/경영진이 IT 의사결정에 적용하도록 요구하는 상위 표준이며, COBIT이 IT관리체계 상세화를, ITIL이 운영 Best Practice를, ISO 38500이 거버넌스 원칙을 담당하는 **3-Layer GRC(Governance, Risk, Compliance)** 구조입니다.

```text
[ IT 거버넌스 의사결정 흐름도 (Evaluate→Direct→Monitor) ]

   Board / Executive Management
   ┌──────────────────────────────────┐
   │ ① Evaluate: IT 투자안 평가      │←── BSC, IT Strategy Map
   │ ② Direct:  전략·정책 결정        │←── COBIT Goals Cascade
   │ ③ Monitor: 성과·리스크 감독      │←── KPI Dashboard
   └──────────────────────────────────┘
              ↕ (ISO 38500 6원칙 적용)
   ┌──────────────────────────────────┐
   │  IT Steering Committee (ISC)     │←── CIO + 사업부서 CFO
   │  · Portfolio Prioritization      │←── NPV, IRR, VOI
   │  · Architecture Review Board     │←── EA 4-Layer
   │  · Change Advisory Board (CAB)   │←── ITIL Change Mgmt
   └──────────────────────────────────┘
              ↕ (Segregation of Duty)
   ┌──────────────────────────────────┐
   │  Operating Layer (PMO, SMO)      │←── PMBOK, PRINCE2
   │  · Program Manager               │←── Benefits Realization
   │  · Service Manager               │←── SLA/SLO/SLI
   │  · Risk & Compliance Officer     │←── ISO 27001, 27701
   └──────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/경영진** | 거버넌스 최종 의사결정 및 책임 | ISO 38500 6원칙 적용, "Direct, Monitor, Evaluate" 순환. eTOM(Level 0~3) 또는 ISO 38500 IT Score Card 활용 |
| **IT Steering Committee (ISC)** | 전략-사업-IT 정렬 중재, 포트폴리오 우선순위 결정 | 분기별 회의, PMO 보고 기반. Magic Quadrant(Gartner), Wave(Forrester) 등 외부 벤치마크 활용 |
| **Enterprise Architecture (EA)** | 업무·정보·시스템·기술 4계층 청사진 | TOGAF ADM(Architecture Development Method) 8 Phase, Zachman Framework 6×6 매트릭스, FEAF( Federal EA) |
| **PMO / Program Mgmt Office** | 프로젝트·프로그램 통합관리 | PMBOK 7th(8 Performance Domain: Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty), PRINCE2(7 Principle, 7 Process, 7 Theme) |
| **IT Service Mgmt (ITSM)** | 운영·서비스 안정성, 사용자 경험 | ITIL 4 SVS(Value→Organization→People→Partners→Value Stream→Value), 34 Practice 중 Incident, Problem, Change, Service Level, Service Request 등 |
| **정보보호·리스크 거버넌스** | 사이버 리스크, 컴플라이언스, BCP | ISO 27001:2022(Annex A 93 통제항목), ISO 27701(프라이버시), ISO 31000(리스크), NIST CSF 2.0(Gov/Identify/Protect/Detect/Respond/Recover 6 Function) |
| **BSC (Balanced Scorecard)** | 전략 KPI 모니터링 | 4관점(재무/고객/내부/학습성장) 인과관계(Lead-Lag Indicator). Strategy Map으로 시각화, OKR과 혼용 가능 |
| **Portfolio Management** | IT 투자 의사결정 | Build vs Buy vs Borrow, NPV/IRR/Payback, Scoring Model(가중치 합산), Stage-Gate(Fuzzy Front End) |

### 핵심 산식 및 정량 평가

1. **TCO (Total Cost of Ownership)** = 직접비(HW/SW) + 간접비(전력·냉각·인건비·교육·폐기) + 기회비용
2. **ROI (Return on Investment)** = (Benefits − Costs) / Costs × 100
3. **VOI (Value on Investment)** = 정성가치(전략·경쟁력·만족도) + 정량가치(ROI) — Balanced Card
4. **NPV (Net Present Value)** = Σ (CFₜ / (1+r)ᵗ) − Initial Investment
5. **IT-Alignment Index (Henderson & Venkatraman)** = 전략 적합성 × IT 기능 통합성 × 기능적·전략적 통합 4관점
6. **MTTR / MTBF / SLA 가용성** = MTBF / (MTBF + MTTR) × 100
7. **CMMI/CMMI v2.0 Level 1~5** = Initial → Managed → Defined → Quantitatively Managed → Optimizing

### 핵심 메커니즘: Goals Cascade & RACI

- **COBIT 2019 Goals Cascade**: Stakeholder Driver → Enterprise Goal(13) → Alignment Goal(13) → Management Objective(40) → Component Variants
- **RACI Matrix**: Responsible(수행) / Accountable(책임, 단 1명) / Consulted(자문) / Informed(통보) — Segregation of Duty 관점에서 R≠A 원칙 준수
- **Stage-Gate Process**: Idea → Scoping → Business Case → Development → Testing → Launch → Post-Implementation Review(PIR)

- **📢 섹션 요약 비유**: **COBIT은 헌법, ITIL은 판례, ISO 38500은 기본권 선언**과 같습니다. COBIT이 "어떤 통제 목표 40개를 달성해야 하는지" 정의하면, ITIL은 "Incident 발생 시 4단계(ITIL 4 Incident Practice)로 해결하라"는 실무 매뉴얼을, ISO 38500은 "이사회가 6원칙으로 책임져라"는 최상위 원칙을 제공합니다.

---

## Ⅲ. 비교 및 연결

### 1. 프레임워크 간 비교

| 구분 | COBIT 2019 | ITIL 4 | ISO/IEC 38500 | PMBOK 7th |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표 | IT 서비스 운영 Best Practice | IT 거버넌스 상위 원칙 | 프로젝트 관리 지식체계 |
| **대상** | CIO·CISO·감사·리스크 | Service Manager·운영팀 | 이사회·경영진 | PM·PMO |
| **Scope** | Enterprise-wide | Service-oriented | Principle-based | Project-based |
| **핵심 산출물** | 40개 Mgmt Objective, Maturity Model | SVS, 34개 Practice | 6원칙, 평가 모델 | 8개 Performance Domain |
| **측정/평가** | Process Assessment Model(PAM) ISO 33000 기반 | Maturity 1~5, KPI | IT Score Card | Earned Value Mgmt(EVM), SPI/CPI |
| **연계 표준** | ISO 27001, NIST CSF, COSO ERM | ISO 20000, DevOps | ISO 27001, 27014 | PRINCE2, SAFe, ISO 21500 |
| **업데이트 주기** | 2019, 5년 주기 | 2019(Foundation→MP→SL→Managing Professional→Master) | 2015, 안정적 | 2021(6th→7th 전환, Process→Principle 중심) |

### 2. 프로젝트 관리 vs 프로그램 vs 포트폴리오 비교

| 구분 | 프로젝트(Project) | 프로그램(Program) | 포트폴리오(Portfolio) |
| :--- | :--- | :--- | :--- |
| **범위** | 단일 결과물 | 관련 프로젝트 군집 | 전략 목표에 부합하는 모든 투자 |
| **기간** | 일시적(Temporary) | 중기 | 지속적(Ongoing) |
| **성공 기준** | Scope·Time·Cost | Benefits Realization | Strategic Alignment |
| **관리자** | PM | Program Manager | Portfolio Manager(PMI-PfMP) |
| **예시** | ERP 1차 모듈 | ERP 전체 + 조직변화 + 교육 | 전사 IT 투자 100건 우선순위 조정 |

### 3. EA 프레임워크 비교

| 구분 | TOGAF | Zachman | FEAF | DoDAF |
| :--- | :--- | :--- | :--- | :--- |
| **개발사** | The Open Group | John Zachman(IBM) | 미국 연방정부 | 미국 국방부 |
| **구조** | ADM 8 Phase | 6×6 매트릭스(5W1H) | 5-Layer Reference Model | 8 View(Viewpoint) |
| **강점** | 실용적 방법론 | 분류체계·원리 | 정부 표준 | 군사용·복합체계 |
| **약점** | 정형화 적음 | 복잡성 | 유연성 부족 | 학습곡선 높음 |

### 4. 연계 기술·도구

- **IT-OT Convergence**: ISO 62443(산업제어보안), Purdue Model(Level 0~5)
- **클라우드 거버넌스**: AWS Well-Architected, Azure CAF, Google Cloud Architecture Framework
- **AI 거버넌스**: NIST AI RMF(2023), ISO/IEC 42001(2023 AI Management System), EU AI Act
- **DevOps/DevSecOps**: DORA Metrics(Deployment Frequency, Lead Time, MTTR, Change Failure Rate), CALMS(Culture, Automation, Lean, Measurement, Sharing)
- **GRC Platform**: SAP GRC, ServiceNow
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 780 / 800

← **이전**: [779. IT 경영 관리 핵심 토픽 779번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/779_it_management_core_topic_779_exam_summary/)
**다음**: [781. IT 경영 관리 핵심 토픽 781번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/781_it_management_core_topic_781_exam_summary/) →

---
