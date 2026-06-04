+++
title = "678. IT 경영 관리 핵심 토픽 678번 시험 요약 (IT Management Core Topic 678 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리의 핵심은 COBIT 2019, ISO/IEC 38500, ITIL 4 등 거버넌스 프레임워크를 기반으로, 정보화 전략(ISP) → 아키텍처(EA) → 사업관리(PMO) → 서비스 운영(ITSM) → 감사/감리(감리법) 의 End-to-End Value Chain을 설계·운영하는 것이다.
> 2. **가치**: EA 기반 중복 투자 제거로 TCO 20~30% 절감, ITIL 4 도입으로 MTTR 40% 단축·MTRS 50% 개선, COBIT 2019 maturity level 1단계 상승 시 ROI 평균 12~18% 향상, 정보시스템 감리를 통한 결함 조기 발견으로 재작업 비용 25% 절감 효과가 보고된다.
> 3. **판단 포인트**: Build vs. Buy vs. Cloud 의사결정, 중앙집중(CoE) vs. 분산(Federated) 거버넌스 모델 선택, Agile vs. Plan-driven 프로젝트 수행 방식, 그리고 BaaS/BPaaS 도입 시 Legacy 시스템의 Technical Debt 관리 및 데이터 거버넌스(Data Governance) 확보가 핵심 Trade-off이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입을 넘어, IT가 기업의 경영 목표(Strategic Goal)와 가치를 연계(Value Linkage)하여 Risk·Performance·Compliance를 통합 관리하는 **IT 거버넌스(IT Governance)** 체계를 확립하는 것이 기술사 시험의 핵심 평가 영역이다. 과거 CIO가 개별 시스템 단위로 운영하던 **"IT 운영 관리(Operations Management)"** 중심 패러다임에서, 2020년대 이후에는 COSO ERM, ISO 37000(거버넌ンス), 그리고 ESG·데이터 3법(개인정보보호법, 정보통신망법, 데이터산업법)·AI기본법 등 규제 환경 변화에 따라 **"IT 경영 관리(Enterprise IT Governance)"** 로 진화하였다.

특히 공공·금융·의료 분야는 전자정부법, 정보시스템의 효율적 도입 및 운영에 관한 지침(행안부 고시), 클라우드컴퓨팅법, 정보시스템 감리법에 따라 법적·규제적 의무가 존재하며, 민간은 ISMS-P, ISO 27001, PCI-DSS, SOX 등 인증 요구로 인해 IT 거버넌스 성숙도가 곧 사업의 자격요건(Gate to Market)이 되었다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│            IT 경영 관리 End-to-End Value Chain (토픽 678)            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [전략]            [설계]            [구축]            [운영]      │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐  │
│  │ ISP 수립 │ ──▶  │ EA/표준 │ ──▶  │ 사업관리 │ ──▶  │ ITSM    │  │
│  │ BSC/CSF │      │ TOGAF   │      │ PMO/Agile│      │ ITIL 4  │  │
│  └─────────┘      └─────────┘      └─────────┘      └─────────┘  │
│       │                │                │                │         │
│       ▼                ▼                ▼                ▼         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │        거버넌스 오버레이: COBIT 2019 / ISO 38500              │  │
│  │   ──── Governance Objectives ──── EDM(05) ── DSS(13)         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│       │                                                              │
│       ▼                                                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │     Audit & Assurance: 감리(감리법) / ISMS-P / ISO 27001      │  │
│  │     Risk: ISO 27005, 31000, NIST CSF 2.0                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

기존의 "IT = 비용(Cost Center)" 관점에서는 CAPEX 위주의 개별 도입으로 Shadow IT가 양산되어 동일 기능의 시스템이 3~5개씩 중복 구축(예: 부서별 상이한 ERP, BPM, CRM)되는 비효율이 발생했다. 그러나 **"IT = 가치(Value Driver)"** 관점의 IT 거버넌스 하에서는, BPI(Business Process Innovation)와 연계된 Portfolio 관리, Architecture Compliance 검증, 그리고 Benefit Realization 관리를 통해 IT 투자 대비 성과(예: NPV, IRR, Payback Period)를 정량적으로 입증한다.

- **📢 섹션 요약 비유**: IT 경영 관리를 자동차 산업에 비유하면, 전략(ISP)은 내비게이션 목적지, EA(아키텍처)는 도로 설계도, 사업관리는 차량 제작 공장, ITSM은 정비소, 감리는 정기검사소, 그리고 COBIT은 운전면허 시험 매뉴얼에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **"Strategy ↔ Architecture ↔ Project ↔ Service"** 4계층을 **Governance·Risk·Compliance(GRC)** 3축으로 횡단 통합하는 것이다. COBIT 2019의 **EDM( Evaluate, Direct and Monitor) 5개 프로세스**와 **Align, Plan and Organize(APO) / Build, Acquire and Implement(BAI) / Deliver, Service and Support(DSS) / Monitor, Evaluate and Assess(MEA)** 의 4개 도메인, 총 40개 Governance/Management Objectives(GO/MO)가 이 통합의 표준 참조 모델이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         COBIT 2019 기반 IT 경영 관리 5단 계층 아키텍처               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Tier 1: Governance (이사회 / IT Steering Committee)                  │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │  EDM01 거버넌스 프레임워크 설정/유지                        │    │
│   │  EDM02 Benefit Delivery 보장                               │    │
│   │  EDM03 Risk Optimization                                   │    │
│   │  EDM04 Resource Optimization                               │    │
│   │  EDM05 Stakeholder Transparency                            │    │
│   └────────────────────────────────────────────────────────────┘    │
│                          │                                          │
│  Tier 2: Management (CISO / EA / PMO)                                │
│   ┌──────────┬──────────┬──────────┬──────────┐                     │
│   │   APO    │   BAI    │   DSS    │   MEA    │                     │
│   │  전략/    │  구축/   │  서비스  │  모니터  │                     │
│   │  기획(14) │  도입(11)│  지원(6) │  평가(5) │                     │
│   └──────────┴──────────┴──────────┴──────────┘                     │
│                          │                                          │
│  Tier 3: Execution (BA / Dev / Ops)                                 │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │  Program / Project / Service Pipeline                    │      │
│   │  ── Plan ── Build ── Test ── Deploy ── Operate ──       │      │
│   │      (PMBOK 7)  (DevOps)  (TDD)  (CI/CD)  (SRE)        │      │
│   └─────────────────────────────────────────────────────────┘      │
│                          │                                          │
│  Tier 4: Infrastructure & Data                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Hybrid Cloud │ Data Lake │ AI/ML │ IoT │ Blockchain        │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                          │                                          │
│  Tier 5: Assurance (감리 / 내부감사 / 컴플라이언스)                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  ISMS-P │ ISO 27001/27017/27701 │ 감리법 │ SOX │ ESG │   │   │
│   └─────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee (ITSC)** | 의사결정 거버넌스 기구 | 분기별 Portfolio Prioritization, Architecture Review Board(ARB) 운영, Benefit Realization 리뷰; 의사결정 권한(RACI) 매트릭스 기반 CIO/CDO/CISO/BA 권한 분리 |
| **EA(Enterprise Architecture)** | 전략-구축 간 정합성 보장 | TOGAF 10 ADM(Architecture Development Method) 8단계( Preliminary → Vision → Business → Information Systems → Technology → Opportunities → Migration → Governance ) 반복; ArchiMate 3.2 표기법 사용 |
| **PMO(Project Management Office)** | 다수 프로젝트 포트폴리오 관리 | 전략적 PMO(SPMO) → 지휘통제 PMO → 운영지원 PMO 위계; P3O(Portfolio, Program and Project Office) 프레임워크, Earned Value Management(EVM: CPI, SPI), Kanban/SAFe 적용 |
| **ITSM (IT Service Management)** | 운영 단계 서비스 품질 | ITIL 4의 34개 Practices(General / Service / Technical Management), 4D 모델(Design & Strategy → Plan & Improve → Engage → Deliver & Support), Service Value System(SVS) 기반 Value Stream 매핑 |
| **GRC & Audit** | 통제 및 신뢰성 확보 | Three Lines Model(IIA 2020): 1st Line(운영 자기통제) → 2nd Line(리스크·컴플라이언스) → 3rd Line(내부감사); 정보시스템 감리법상 감리원 자격: 기술사, 감리사 |

핵심 운영 메커니즘은 **"전략 ↔ 실행 간 정합성(Strategic Alignment)"** 측정이다. 이를 위해 Balanced Scorecard(BSC) 4관점(Financial / Customer / Internal Process / Learning & Growth)에 IT KPI를 연계한 **IT BSC**를 활용하며, 대표 KPI는 다음과 같다:

- **전략 정합도**: Strategic Alignment Maturity(SAM) 5단계 모델에서 Level 3 이상 유지
- **아키텍처 준수율**: Architecture Compliance Assessment(ACA) 결과 85% 이상
- **프로젝트 성공률**: PMI 기준 On-time/On-budget/Scope 충족 3개 동시 충족 프로젝트 비율(세계 평균 31% → 우수 조직 75%)
- **서비스 품질**: ITIL SLA 기준 가용성 99.9%(연 8.76h 장애 허용), MTTR < 30분, FCR(First Call Resolution) > 70%
- **정보보안**: ISMS-P 인증 유지, 침해사고 Zero(또는 MTTD < 24h, MTTC < 1h)
- **재무 성과**: IT 투자 ROI 측정, TCO 3년 회수율, OpEx/CapEx 비율(클라우드 전환 시 OpEx 비중 확대)

기술사적 관점에서 가장 중요한 원리는 **"Value Creation vs. Risk Control"** 의 균형점 탐색이다. COBIT 2019의 **Goals Cascade** 메커니즘은 Stakeholder Drivers → Enterprise Goals(13개) → Alignment Goals(13개) → Governance/Management Objectives(40개)로 계층적 매핑하여, IT 투자가 기업 목표에 미치는 영향(예: EG01 Portfolio of Competitive Products & Services ↔ AG11 Managed I&T Investment & Portfolio)을 정량화한다.

- **📢 섹션 요약 비유**: COBIT 2019의 5계층을 "병원 시스템"에 비유하면, Tier 1(이사회)은 병원 운영위원회, Tier 2(CISO 등)는 진료과장, Tier 3(개발팀)는 전문의, Tier 4(인프라)는 수술실·MRI·CT 장비, Tier 5(감사)는 의료감사팀과 JCI 인증에 해당한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 혼동하기 쉬운 핵심 프레임워크/개념들의 차이점을 명확히 구분하는 것이 기술사 시험의 핵심이다.

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (서비스 관리) | ISO/IEC 38500 (이사회 거버넌스) | PMBOK 7 (프로젝트 관리) | TOGAF 10 (아키텍처) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 목표 40개 표준화 | IT 서비스의 End-to-End Value Stream 최적화 | 이사회 수준 IT 의사결정 6원칙 | 프로젝트 단위 Deliverable 산출 | EA 구축/관리 방법론 |
| **대상** | 거버넌스 기구 + IT 관리자 | IT 운영 실무자(SOC, Help Desk) | 이사진·CEO·CIO | PM/PMO | EA 아키텍트(BA, DA, SA, TA) |
| **핵심 원리** | EDM + APO/BAI/DSS/MEA 도메인 | 34 Practices + SVS + 4D 모델 | Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior 6원칙 | 12 Principles of Project Management + 8 Performance Domains | ADM 8단계 반복, Architecture Repository |
| **산출물** | Maturity Model(0~5), Risk Profile | SLA, Service Catalog, CSI 등록부 | 정책·지침·성과측정 | Charter, WBS, Risk Register, Lessons Learned | Architecture Document, Gap Analysis, Roadmap |
| **연계 관계** | 상위 거버넌스, 모든 IT 활동 포괄 | COBIT의 DSS 도메인에서 서비스 운영 부분 | COBIT EDM과 중첩, 이사회 관점 강조 | COBIT의 BAI(11) 영역과 직결 | COBIT APO12(Managed Risk)와 APO02(Managed Strategy)와 연결 |
| **측정 단위** | Maturity Level, Goal Cascade 달성도 | Service Value(Utility + Warranty) | 거버넌스 6원칙 준수율 | SPI, CPI, Schedule/Cost/Scope Performance | Architecture Maturity(TOGAF ACMP) |
| **주 사용 주체** | CIO, CISO, Internal Audit | Service Desk Manager, SRE, DevOps | Board of Directors | PMO, Project Manager | Chief Architect, EA Team |
| **법적 연계** | 감리법 시행령 제49조(거버넌스) | - | ISO 38500 단독 표준 | 국가계약법, 발주자 책임 (조달청 지침) | - |
| **최신 버전** | 2019 (2018) | 4 (2019, 2020년 Foundation) | 2015 (개정 논의 중) | 7th (2021) | 10th (2022) |

**연계 통합 패턴**은 실무에서 다음과 같이 구성된다:
1. **전략 단계**: ISO 38500(거버넌스 원칙) → COBIT EDM(목표) → ISP(BSC) → TOGAF Phase A/B(비전·비즈니스)
2. **설계 단계**: TOGAF Phase C/D/E(데이터·응용·기술) → ArchiMate 3.2 모델링 → 표준화(EA Repository)
3. **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 678 / 800

← **이전**: [677. IT 경영 관리 핵심 토픽 677번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/677_it_management_core_topic_677_exam_summary/)
**다음**: [679. IT 경영 관리 핵심 토픽 679번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/679_it_management_core_topic_679_exam_summary/) →

---
