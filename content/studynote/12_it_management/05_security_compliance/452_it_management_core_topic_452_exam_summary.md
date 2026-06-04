+++
title = "452. IT 경영 관리 핵심 토픽 452번 시험 요약 (IT Management Core Topic 452 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Management)는 COBIT 2019, ITIL 4, ISO/IEC 38500 IT 거버넌스 표준을 기반으로 **전략(Strategy)-포트폴리오(Portfolio)-프로그램(Program)-프로젝트(Project)-운영(Operation)**의 5계층 가치 사슬(Value Chain)을 통해 IT 투자 대비 사업 가치(ROI, NPV, VOI)를 극대화하는 경영 학문이다.
> 2. **가치**: McKinsey(2023) 기준 효과적인 IT 거버넌스 체계 구축 시 **프로젝트 성공률 35%→72% 향상**, IT 운영 비용 평균 **23% 절감**, 디지털 전환 과제 Time-to-Market **40% 단축**, ISMS-P 인증 기업은 보안사고 발생 시 **평균 손실액 47% 감소**(KISA, 2022) 효과를 실현한다.
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프로는 (①중앙집중형 vs 분산형 거버넌스 모델) (②Build vs Buy vs Cloud SaaS) (③Agile vs Waterfall vs Hybrid SDLC) (④Capex vs Opex 회계 처리) (⑤내부통제 vs 아웃소싱) 있으며, 기술사는 **EA(Enterprise Architecture) 4.x + BSC 4관점 + COBIT 2019 40개 관리목표**를 통합한 거버넌스 체계 설계 역량을 보여주어야 합격선에 도달한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation)이 가속화되면서 IT는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 역할이 전환되었다. Gartner(2024) 보고에 따르면 글로벌 CEO의 89%가 "IT가 사업 성장의 핵심 동력"이라고 답하고 있으나, 동시에 McKinsey의 조사에서는 디지털 전환 프로젝트의 **70%만이 비즈니스 목표를 달성**하는 것으로 나타나, **IT-Biz Alignment Gap**이 핵심 경영 이슈로 부상하고 있다.

이러한背景下 IT 경영 관리(Information Technology Management)는 단순한 시스템 운영을 넘어, **"올바른 일을 올바르게 하는(Doing the Right Things Right)"** 프레임워크를 제공하며, 거버넌스(Governance)·전략(Strategy)·포트폴리오(Portfolio)·운영(Operation)·컴플라이언스(Compliance)를 통합 관리하는 경영 체계이다.

특히 2024년 이후 **클라우드 네이티브(Cloud-Native)**, **생성형 AI(Generative AI)**, **제로트러스트(Zero Trust)**, **ESG(Environmental, Social, Governance) 컴플라이언스**가 필수 요구사항이 되면서, 전통적인 ITIL v3 기반 운영 관점에서 **ITIL 4의 SVS(Service Value System)** 및 **COBIT 2019의焦点영역(Focus Area)** 개념으로 패러다임 전환이 진행 중이다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│        IT 경영 관리 5계층 가치 사슬 (IT Value Chain Framework)          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [1] 전략계층 (Strategy Layer)                                          │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  • 디지털 전환 로드맵 (DX Roadmap 2024-2027)                  │     │
│   │  • IT 전략계획(ISP, Information Strategy Planning)            │     │
│   │  • BSC 4관점(Financial·Customer·Internal·Learning&Growth)     │     │
│   │  • 거버넌스 구조(위원회·CIO·CDO·CISO·DPO)                     │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                              ↓ IT-Strategy Alignment                   │
│   [2] 포트폴리오계층 (Portfolio Layer)                                   │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  • App Portfolio (Build/Buy/Sunset 분류)                      │     │
│   │  • 투자배분: Run(60%)·Grow(30%)·Transform(10%)                 │     │
│   │  • 우선순위 평가: 사업전략가치×기술위험도×비용효율              │     │
│   │  • PMO(Project Management Office) 관할                        │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                              ↓ Program/Project Execution               │
│   [3] 프로그램/프로젝트 계층 (Program/Project Layer)                    │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  • PMBOK 7th + PRINCE2 + Agile(Scrum/Kanban) + SAFe 6.0     │     │
│   │  • 단계별 게이트(Gate) 관리: Idea→Feasibility→Plan→Build→     │     │
│   │    Deploy→Operate→Retire (ISO 21502)                          │     │
│   │  • EVM(Earned Value Management): PV/EV/AC, SPI, CPI          │     │
│   │  • 리스크 관리: 정성·정량 분석(Monte Carlo Simulation)         │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                              ↓ Service Transition                      │
│   [4] 서비스운영 계층 (Service Operation Layer)                          │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  • ITIL 4 SVS: 7가지 guiding principles, 34 practices         │     │
│   │  • ITSM 도구: ServiceNow, Jira Service Mgmt, BMC Remedy      │     │
│   │  • SLA/SLO/SLI 정의 및 모니터링 (예: 가용성 99.95% 이상)      │     │
│   │  • DevOps + SRE: DORA 4 Metrics (배포빈도·리드타임·변경실패율 │     │
│   │    ·복구시간) 측정                                             │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                              ↓ Compliance & Continuous Improvement     │
│   [5] 컴플라이언스/개선 계층 (Compliance & Improvement Layer)           │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  • 컴플라이언스: ISMS-P, ISO 27001, ISO 20000, GDPR/PIPA     │     │
│   │  • 내부통제: COSO 2013 + SOX 404 IT General Controls (ITGC)   │     │
│   │  • 측정: KPI/KRI/CSF, NIST CSF 2.0 (Govern-Identify-Protect- │     │
│   │    Detect-Respond-Recover)                                    │     │
│   │  • 지속적 개선: PDCA + Kaizen + Retrospective + Post-Mortem   │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
        ──────────────── Feedback Loop (성과 → 전략) ────────────────
```

기존 패러다임(1990-2010)은 **Cost Center 관점의 IT 운영**에 초점을 맞추어, "IT 비용을 얼마나 절감했는가?"가 핵심 KPI였다. 그러나 현대 패러다임(2020-)는 **Value Center 관점의 IT 경영**으로 전환되어, "IT가 창출한 사업 가치는 얼마인가?"가 핵심 KPI가 되었다. 이는 COBIT 2019의 5원칙(Principle 1~5: Stakeholder Value, Holistic Approach, Dynamic Governance System, Tailoring to Enterprise Needs, End-to-End Governance)에서 명시적으로 반영되어 있다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **배(Ba = 場) 개념**으로 이해하면 쉽습니다. 일반 공장은 원자재 투입 → 제조 → 출하의 단방향 흐름이지만, **현대 IT 공장은 '전략(요리사) - 포트폴리오(냉장고) - 프로젝트(주방) - 운영(홀) - 고객(피드백)'의 순환 구조**로, 고객 한 입의 반응이 다음 메뉴 개발의 핵심 정보가 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019 Governance System**을 중심으로 **ITIL 4**, **ISO/IEC 38500**, **ISO 21502(Project)**, **ISO 27001(Security)** 표준이 통합된 **Multi-Framework Convergence Architecture**이다. 각 프레임워크는 서로 다른 관점(Governance, Management, Operation, Security)을 담당하며, 이를 효과적으로 통합 운영하는 것이 기술사의 핵심 역량이다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│        IT 경영 관리 Multi-Framework 통합 아키텍처 (Convergence Map)    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────── 5단계 계층 (5 Layer Architecture) ──────┐    │
│   │                                                                │    │
│   │  L5. 거버넌스 원칙(Governance Principles)                       │    │
│   │  ┌──────────────────────────────────────────────────────────┐  │    │
│   │  │ ISO/IEC 38500:2024 — 6 Principles: Responsibility,       │  │    │
│   │  │ Strategy, Acquisition, Performance, Conformance, Human   │  │    │
│   │  │ Behavior (3-Evaluate, 3-Direct, 3-Monitor)              │  │    │
│   │  └──────────────────────────────────────────────────────────┘  │    │
│   │                          ↕ Bidirectional Alignment             │    │
│   │  L4. 거버넌스 시스템(Governance System)                         │    │
│   │  ┌──────────────────────────────────────────────────────────┐  │    │
│   │  │ COBIT 2019: 40 Governance & Management Objectives        │  │    │
│   │  │ 5 Components: Principles·Policies·Processes·Org·         │  │    │
│   │  │ Culture·People·Skills·Services·Infrastructure·Apps·Info  │  │    │
│   │  │ 7 Components of Governance System: Process/Org/Info      │  │    │
│   │  │  ·People/Skills/Culture/Service/Infrastructure/Apps      │  │    │
│   │  │ Focus Areas: DevOps, Cybersecurity, Digital Transformation│  │    │
│   │  └──────────────────────────────────────────────────────────┘  │    │
│   │                          ↕ Mapping                             │    │
│   │  L3. 운영관리 시스템(Service Management)                       │    │
│   │  ┌──────────────────────────────────────────────────────────┐  │    │
│   │  │ ITIL 4 Service Value System (SVS)                        │  │    │
│   │  │  • Opportunity/Demand → Value                            │  │    │
│   │  │  • 7 Guiding Principles: Focus on Value, Start Where     │  │    │
│   │  │    You Are, Progress Iteratively, Collaborate, Think     │  │    │
│   │  │    Holistically, Keep It Simple, Optimize/Automate       │  │    │
│   │  │  • 34 Practices (14 General + 17 Service + 3 Technical)  │  │    │
│   │  │  • 4 Dimensions of Service Mgmt: Org·People·Info·       │  │    │
│   │  │    Technology·Partners·Value Streams·Processes           │  │    │
│   │  └──────────────────────────────────────────────────────────┘  │    │
│   │                          ↕ Integration                          │    │
│   │  L2. 프로젝트/프로그램 (Project/Program)                        │    │
│   │  ┌──────────────────────────────────────────────────────────┐  │    │
│   │  │ PMBOK 7th (8 Performance Domains) + PRINCE2 (7 Themes)  │  │    │
│   │  │ + SAFe 6.0 (5 Core Values) + ISO 21502:2020              │  │    │
│   │  │ Stage Gate: Feasibility→Design→Build→Test→Deploy→Close  │  │    │
│   │  └──────────────────────────────────────────────────────────┘  │    │
│   │                          ↕ Security Overlay                     │    │
│   │  L1. 보안/컴플라이언스 (Security & Compliance)                  │    │
│   │  ┌──────────────────────────────────────────────────────────┐  │    │
│   │  │ ISO 27001:2022 (Annex A 93 Controls) + ISMS-P 인증      │  │    │
│   │  │ + NIST CSF 2.0 (6 Functions) + 개인정보보호법(PIPA)     │  │    │
│   │  │ + GDPR + PCI-DSS + HIPAA + ESG 정보공시                  │  │    │
│   │  └──────────────────────────────────────────────────────────┘  │    │
│   │                                                                │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│   ──────────────────── Cross-Cutting Concerns ─────────────────────    │
│   • EA (Enterprise Architecture): TOGAF 10 ADM / DoDAF / FEA           │
│   • BSC (Balanced Scorecard): 4 Perspectives + Strategy Map            │
│   • 리스크 관리: ISO 31000 + COSO ERM 2017 + NIST RMF               │
│   • 비용 관리: TCO(5년) + ROI/NPV/IRR/Payback Period                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 위원회 (IT Steering Committee)** | 최고 의사결정 기구, IT 투자·우선순위·정책 승인 | 월 1회 정례회의, KPI 대시보드 리뷰, 의사결정 권한 매트릭스(RACI) 운영, 정족수 2/3 이상 |
| **CIO / CDO / CISO** | IT·데이터·정보보안 책임 (3직위 분리 권장) | CIO: IT 전략·거버넌스, CDO: 데이터 거버넌스·분석, CISO: 보안·프라이버시. C레벨 회의 동등한석, 예산 한도별 승인권 |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리·표준·품질 | EPMO(Enterprise PMO): 전략 연계 / PMO: 프로젝트 모음 / CoE: 방법론 전문. 단계별 게이트 심사, EVM 매트릭스 운영 |
| **서비스운영 조직 (IT Operations)** | 일일 서비스 제공·모니터링·장애대응 | ITIL 4 Incident/Problem/Change Mgmt + SRE(Site Reliability Engineering) + AIOps(예: Splunk ITSI, Datadog) |
| **컴플라이언스 조직 (GRC)** | 규제 준수·리스크 관리·내부통제 | GRC 플랫폼 활용 (예: SAP GRC, ServiceNow GRC, Archer). ISMS-P 인증 심사, 내부감사, 리스크 레지스터 운영 |
| **아키텍처 조직 (EA Team)** | 전사 아키텍처 표준·로드맵·가이드라인 | TOGAF 10 ADM 8단계(준비→전략비전→아키텍처비전→사업·데이터·애플리케이션·기술 아키텍처→이행계획) 수행, 아키텍처 원장(Repository) 관리 |

COBIT 2019의 **40개 관리 목표(Management Objectives)**는 5개 도메인(EDM: Evaluate/Direct/Monitor 5개, APO: Align/Plan/Organize 14개, BAI: Build/Acquire/Implement 11개, DSS: Deliver/Service/Support 6개, MEA: Monitor/Evaluate/Assess 4개)으로 구성된다. 각 목표는 **프로세스 관점(Process) + 조직 구조(Organizational Structure) + 정보 흐름(Information Flow) + 사람/역량(People/Skills) + 정책/절차(Policy/Procedure) + 문화/윤리(Culture/Ethics) + 서비스/인프라/앱/정보(Services/Infrastructure/Applications/Information)**의 7가지 구성요소로 평가된다. **핵심 성숙도 모델은
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 452 / 800

← **이전**: [451. IT 경영 관리 핵심 토픽 451번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/451_it_management_core_topic_451_exam_summary/)
**다음**: [453. IT 경영 관리 핵심 토픽 453번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/453_it_management_core_topic_453_exam_summary/) →

---
