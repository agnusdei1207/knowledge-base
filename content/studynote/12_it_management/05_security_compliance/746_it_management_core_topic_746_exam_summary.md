+++
title = "746. IT 경영 관리 핵심 토픽 746번 시험 요약 (IT Management Core Topic 746 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(746번)는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로, IT 전략-아키텍처-운영-감리(Value Delivery)를 End-to-End로 정렬(Alignment)하여 기업의 디지털 전환(DX) 가치를 극대화하는 통합 관리 체계이다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 IT 투자 대비 ROI 25~40% 향상, 주요 장애(Major Incident) 50% 감소, 컴플라이언스 위반 비용 60% 절감이 가능하며, 정보화사업의 PMO 성숙도 Level 3→Level 5 도달로 프로젝트 성공률 72%→89%로 개선된다.
> 3. **판단 포인트**: 중앙집중형(COBIT) vs 분산형(Federated IT) 거버넌스 모델 선택, Build vs Run 예산 배분 비율(통상 30:70), 사이버보안 제로트러스트 도입 시 CAPEX/OPEX 비율, 그리고 ESG 및 개인정보보호법(PIPA) 컴플라이언스를 위한 통제 항목(Control Objective) 설계가 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대에 기업 IT 부서는 단순한 비용센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 역할이 전환되었다. 그러나 한국 정보화 통계 조사에 따르면 정보화 사업의 약 35%가 예산 초과, 27%가 일정 지연, 18%가 목표 미달로 종료되어 IT 경영 관리 체계의 부재가 경영 리스크로 부상하고 있다. 특히 2024년 개인정보보호법 개정, EU AI Act, 클라우드 보안인증(CSAP) 등 규제 환경이 급변하면서 **IT 거버넌스(Governance) + IT 관리(Management) + IT 감리(Audit)**의 3축 통합 체계가 필수 불가결한 경영 인프라가 되었다.

기존의 "프로젝트 단위 관리"에서 "포트폴리오 기반 가치 중심 관리"로의 패러다임 전환이 요구되며, 이는 PMBOK 7th(원리 기반 접근), PRINCE2, ISO 21500 등 프로젝트 관리 표준과 COBIT 2019의 거버넌스 시스템 목표(Governance System Goals), ITIL 4의 Service Value System(SVS)을 통합적으로 운용해야 함을 의미한다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│           IT 경영 관리 746번 - 3축 통합 거버넌스 프레임워크          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│   │  거버넌스     │    │   IT 관리    │    │   IT 감리    │        │
│   │ (Governance) │◄──►│ (Management) │◄──►│   (Audit)    │        │
│   │              │    │              │    │              │        │
│   │ COBIT 2019   │    │ ITIL 4 SVS   │    │ ISACA 감사   │        │
│   │ ISO 38500    │    │ PMBOK 7th    │    │ TTA 인증     │        │
│   │  ● 방향     │    │  ● 실행     │    │  ● 검증     │        │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘        │
│          │                   │                   │                  │
│          └───────────────────┼───────────────────┘                  │
│                              ▼                                      │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │        기업 가치 창출 (Enterprise Value Creation)         │      │
│   │   • 디지털 전환(DX) ROI  • 운영 효율성  • 리스크 통제   │      │
│   └─────────────────────────────────────────────────────────┘      │
│                              ▲                                      │
│                              │                                      │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │  Stakeholders: 이사회, CEO, CIO, CFO, CISO, CCO    │           │
│   │  외부 규제: PIPA, AI Basic Act, CSAP, DORA, ESG    │           │
│   └─────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

한국 정보화진흥법 제14조(정보화사업의 감리), 클라우드컴퓨팅법 제23조(클라우드 서비스 보안 인증), 공공데이터법 등 강력한 법적 근거 하에 IT 경영 관리는 이제 선택이 아닌 **의무 사항**이며, 특히 매출 1,000억 원 이상 또는 정보화 투자 100억 원 이상 기업의 경우 정기 감리가 의무화되어 있다. 또한, K-ICT 2023 전략에 따라 AI·데이터·클라우드 중심의 디지털 전환이 가속화되면서 전통적 IT 운영 모델(Waterfall, On-Premise)에서 Agile, DevSecOps, FinOps 기반의 운영 모델로의 전환이 핵심 화두로 대두되었다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판과 블랙박스**와 같습니다. 엔진(IT 시스템)이 아무리 좋아도, 계기판(거버넌스 지표)이 없으면 과속·과열 사고를 막을 수 없고, 블랙박스(감리 로그)가 없으면 사고 원인을 분석할 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 크게 **5대 영역(Evaluate, Direct, Monitor + Plan, Build, Run)**으로 구성되며, 이는 COBIT 2019의 거버넌스/관리 목표와 ITIL 4의 SVS(Service Value System)를 통합한 것이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│     COBIT 2019 + ITIL 4 통합 거버넌스/관리 참조 모델(GRC)         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [거버넌스 3단계 - EDM]           [관리 5단계 - PBRR]              │
│   ┌─────────────────┐             ┌─────────────────────────────┐   │
│   │ E: Evaluate     │             │ P: Plan (계획/전략)         │   │
│   │  - 옵션 평가    │             │  - 전략맵, TOGAF ADM        │   │
│   │  - KPI/CSF 도출 │             │  - 투자 우선순위 결정       │   │
│   ├─────────────────┤             ├─────────────────────────────┤   │
│   │ D: Direct       │             │ B: Build (구축/전환)        │   │
│   │  - 의사결정 위임│             │  - Agile/DevSecOps          │   │
│   │  - 책임 할당    │             │  - CI/CD Pipeline           │   │
│   ├─────────────────┤             ├─────────────────────────────┤   │
│   │ M: Monitor      │             │ R: Run (운영/서비스)       │   │
│   │  - 성과 측정    │             │  - ITIL 4 SVS, AIOps       │   │
│   │  - 컴플라이언스 │             │  - FinOps, SRE              │   │
│   └─────────────────┘             ├─────────────────────────────┤   │
│                                   │ R: Run 개선/지속 (CSI)      │   │
│                                   │  - Continual Improvement     │   │
│                                   └─────────────────────────────┘   │
│                                                                      │
│   ──────── 7대 구성요소 (COBIT 2019 Core Model) ────────              │
│   ① 프로세스(Process)  ② 구조(Structure)  ③ 정보(Flows)            │
│   ④ 사람/스킬(People)  ⑤ 서비스/인프라   ⑥ 문화/윤리               │
│   ⑦ 목표 연쇄(Cascading Goals)                                      │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (Governance System)** | 이사회-경영진-IT 조직 간 의사결정 정렬 | RACI 매트릭스, COBIT 2019 40개 관리목표 + 5개 거버넌스 목표, ISO 38500 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) |
| **전략-아키텍처 연계 (Strategy-Architecture Alignment)** | 비즈니스 전략 ↔ EA(Enterprise Architecture) 정렬 | TOGAF ADM(Architecture Development Method) 8단계: Preliminary→A(비전)→B(비즈니스)→C(데이터/앱)→D(기술)→E(기회/솔루션)→F(마이그레이션)→G(구현거버넌스)→H(아키텍처 변경관리), Zachman Framework 6x6 매트릭스 |
| **IT 서비스 관리 (ITSM)** | IT 서비스의 기획-설계-전환-운영-개선 전주기 | ITIL 4 Service Value Chain(Plan→Engage→Design&Transition→Obtain/Build→Deliver&Support→Improve), 34개 Practice, SLA/OLA/UC(Service Level Agreement/Operational Level Agreement/Underpinning Contract) |
| **정보화사업 관리 (Project Portfolio Mgmt)** | 다수 프로젝트의 투자·일정·품질 통합 관리 | PMBOK 7th 12원리, PRINCE2 7원리(7 Principles), MSP(Managing Successful Programmes), 포트폴리오 차원화(Compulsory/Operational/Strategic) |
| **리스크·컴플라이언스 (GRC)** | 사이버 리스크·규제 준수·내부 통제 통합 | ISO 27001(ISMS), ISO 31000(리스크관리), NIST CSF 2.0(Govern-Identify-Protect-Detect-Respond-Recover), ISACA Risk IT, 3 Lines of Defense Model(IIA) |
| **성과 측정 및 평가 (Performance Mgmt)** | KPI/CSF/BSC 기반 가치 정량 측정 | Balanced Score Card 4관점(Financial/Customer/Internal Process/Learning&Growth), NSM(National ICT Service Management)成熟도 모델 5단계, CMMI 5단계, KPI SMART 원칙 |
| **디지털 전환 거버넌스 (DX Governance)** | AI·클라우드·데이터 기반 신기술 도입 통제 | AI 거버넌스 위원회, Model Card / Datasheet, FinOps Foundation Framework(Inform-Optimize-Operate), Cloud Center of Excellence(CCoE) |

핵심 메커니즘은 **목표 연쇄(Cascading Goals)**다. 거버넌스 목표(예: 이해관계자 가치 실현)에서 출발해 정보/기술 목표, 프로세스 목표, 사람/스킬 목표로 하향 전파(Cascade)되며, 각 단계의 KPI가 정의되어야 한다. 예컨대 "이해관계자 가치 실현"이라는 거버넌스 목표는 "IT 운영 효율성 20% 향상"이라는 정보/기술 목표로 구체화되고, 이는 "MTTR(Mean Time To Repair) 30분 이내"라는 프로세스 KPI로 측정된다.

정보화사업의 경제성 분석은 **B/C(비용편익비) 분석, NPV(순현재가치), IRR(내부수익률), Payback Period(회수기간)**의 4대 재무지표를 동시에 활용한다. 한국 정보화진흥기본법 시행령은 B/C ≥ 1.0을 사업 타당성의 최소 기준으로 명시하며, NPV는 할인율 4.5% (사회적 할인율 기준)를 적용한다. 또한 종합평가 시 정량효과(60%) + 정성효과(40%) 가중치를 적용하며, PI(Performance Index: EV/AC), SPI(Schedule Performance Index: EV/PV), CPI(Cost Performance Index: EV/AC) 등의 EVM(Earned Value Management) 지표로 진행 상황을 모니터링한다.

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **도시의 상수도 시스템**과 같습니다. 취수장(전략), 정수장(설계), 배수관(운영), 수도꼭지(서비스), 누수감지 센서(감리)가 하나의 순환 체계로 연결되어야 시민(비즈니스)에 깨끗한 물(가치)을 안정적으로 공급할 수 있습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 혼동되기 쉬운 유사 개념들을 명확히 구분하는 것이 기술사 시험의 핵심이다.

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (서비스 관리) | PMBOK 7th (프로젝트 관리) | ISO 38500 (IT 거버넌스 표준) |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 초점** | Value Creation을 위한 IT 거버넌스/관리 시스템 | IT 서비스의 End-to-End 운영·개선 | 프로젝트의 성공적 수행을 위한 12원리 | 이사회급 IT 의사결정 6원칙 |
| **대상 범위** | 전체 IT (전략→운영→감리) | IT 서비스 운영·전환 | 단위 프로젝트(일시적) | 거버넌스 의사결정(상위) |
| **구조** | 40 관리목표 + 5 거버넌스목표, 7개 컴포넌트 | 34 Practice, Service Value Chain | 8 Performance Domains | 6 Principles + 5 Governance Model |
| **수명 주기** | 지속적(Continuous) | 서비스 수명주기(Strategy→Design→Transition→Operation→CSI) | 프로젝트 수명주기(Initiate→Plan→Execute→Monitor→Close) | 지속적(상시 모니터링) |
| **측정 지표** | Governance/Management Objectives KPI | SLA, SLO, SLI, CX(Customer Experience) | SPI, CPI, EVM, OKR | Maturity Level (1~5) |
| **인증/감사** | COBIT 인증 심사, ISACA 감사 연계 | ITIL 4 Foundation/Master | PMP, CAPM | ISO 인증 (심사원 자격) |
| **적용 계층** | C-Level (CIO, 이사회) | 서비스 매니저, ITSM 운영팀 | PMO, 프로젝트 매니저 | 이사회, CEO, CIO |
| **주요 연계 표준** | ISO 27001, NIST CSF, CMMI | ISO 20000, DevOps, SIAM | PRINCE2, ISO 21500, MSP | COBIT 2019, ISO 37000 |
| **한국 적용 사례** | 공공부문 정보화 사업 감리 (정통부 가이드) | 기업 ITSM 구축, 네이버/카카오 SRE | 발주청 PMO, SI 프로젝트 | 중대재해 대비 IT 안전 거버넌스 |

**연계 통합 아키텍처**: 실무에서는 단일 프레임워크만으로는 부족하며, **COBIT 2019 (What/Why)** + **ITIL 4 (How to Run)** + **PMBOK 7th (How to Build)** + **ISO 27001/38500 (Risk/Compliance)** + **TOGAF (How to Architect)**의 5각 통합이 표준이다. 이를 **"GART-P" 통합 모델**(Governance-Architecture-Risk-Technology-Project)이라 한다.

최근에는 **DevOps Research and Assessment (DORA) 4대 지표**(Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service)와 **Google SRE(Service Reliability Engineering)**의 SLO/SLI
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 746 / 800

← **이전**: [745. IT 경영 관리 핵심 토픽 745번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/745_it_management_core_topic_745_exam_summary/)
**다음**: [747. IT 경영 관리 핵심 토픽 747번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/747_it_management_core_topic_747_exam_summary/) →

---
