+++
title = "514. IT 경영 관리 핵심 토픽 514번 시험 요약 (IT Management Core Topic 514 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Enterprise IT Management)는 COBIT 2019·ITIL 4·PMBOK 7·ISO 27001·TOGAF 등 글로벌 표준 프레임워크를 **거버넌스-전략-운영-프로젝트-보안-아키텍처 6대 축**으로 통합하여, IT 투자 대비 비즈니스 가치(ROI, NPV, IRR)를 극대화하고 리스크를 통제하는 경영 체계임.
> 2. **가치**: McKinsey 보고에 따르면 체계적 IT 거버넌스 도입 기업은 프로젝트 성공률 35%→75%, TCO 20~30% 절감, Time-to-Market 40% 단축, 보안 사고 대응 시간 평균 62% 감소 등 정량적 임팩트를 창출하며, 디지털 전환(DX) 시대의 경쟁력 핵심 자산화.
> 3. **판단 포인트**: 기술사 답안 작성 시 **① 거버넌스 구조(RACI, 3 Lines Model) ② 표준 프레임워크 매핑 ③ 정량 KPI(BSC 4관점, CSF/KPI) ④ 라이프사이클 단계별 통제점 ⑤ 컴플라이언스(개인정보보호법, ISMS-P, ESG)** 5가지를 반드시 명시해야 채점기준(적합성·타당성·실현가능성) 확보 가능.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 1980년대 MIS(경영정보시스템) 시대를 거쳐 2000년대 e-Biz, 2010년대 클라우드/모바일, 2020년대 AI·메타버스·양자컴퓨팅 환경으로 패러다임이 진화하면서, 단순 시스템 구축에서 **"비즈니스 전략과 IT의 정렬(Strategic Alignment)"** 및 **"가치 실현(Value Realization)"** 중심으로 재정의되었습니다. 기술사 시험에서는 이러한 시대적 배경과 함께, ISO/IEC 38500 IT 거버넌스 국제표준, COBIT 2019의 40개 거버넌스/관리 목적(GO/PO), 디지털 전환 거버넌스 등 최신 트렌드를 반영한 답안을 요구합니다.

```text
┌─────────────────────────────────────────────────────────────┐
│          IT 경영 관리 6대 핵심 축 (Topic 514 통합 모델)      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [1. IT 거버넌스]      [2. IT 전략 기획]                  │
│   COBIT 2019            BSC, Porter Value Chain             │
│   ISO 38500             SWOT/PEST, ROI/NPV/IRR              │
│   3 Lines Model         EA(TOGAF, FEAF)                      │
│         │                     │                             │
│         ▼                     ▼                             │
│   ┌─────────────────────────────────────┐                  │
│   │   [통합 거버넌스 위원회(IGC)]         │                  │
│   │   - CIO/CDO/CTO Steering Committee  │                  │
│   │   - RACI 매트릭스 기반 의사결정      │                  │
│   └─────────────────────────────────────┘                  │
│         │                     │                             │
│         ▼                     ▼                             │
│   [3. 프로젝트 관리]    [4. IT 서비스 관리]                 │
│   PMBOK 7 / PRINCE2     ITIL 4 (SVS)                       │
│   Agile/Scrum/SAFe      DevOps, SRE                        │
│   Earned Value Mgmt     SLA/OLA/UC                         │
│         │                     │                             │
│         ▼                     ▼                             │
│   [5. 정보보안 거버넌스] [6. 아키텍처 거버넌스]             │
│   ISO 27001/27701       TOGAF ADM                          │
│   ISMS-P, PIPC          Zachman Framework                   │
│   Zero Trust, SASE       클라우드 네이티브 (K8s, MSA)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

IT 도입 비용 대비 성과 부재, 부서별 시스템 silos, Shadow IT 증가, 사이버 위협 고도화, 규제 강화(개인정보보호법, EU GDPR, AI Basic Act), ESG 공시 의무화 등 복합적 도전 과제로 인해, **"계획(Plan)-실행(Do)-모니터링(Monitor)-평가(Evaluate)"** 사이클을 거버넌스 차원에서 자동화·지속 개선하는 통합 관리 체계가 필수입니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같습니다. 첼로(IT 거버넌스), 바이올린(프로젝트), 트럼펫(보안), 팀파니(아키텍처) 등 각 악기가 제때 정확한 음표(목표·KPI)로 연주되어야 비로소 훌륭한 교향곡(비즈니스 가치)이 만들어집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019를 메타 프레임워크로, ITIL 4를 서비스 운영 프레임워크로, PMBOK 7을 프로젝트 거버넌스로, ISO 27001을 보안 거버넌스로 통합한 **"거버넌스 시스템(Governance System) + 가치 실현(Value Realization)"** 이중 구조가 핵심 원리입니다. COBIT 2019의 **40 Governance/Management Objectives**는 5개 도메인(EDM: Evaluate, Direct, Monitor / APO: Align, Plan, Organize / BAI: Build, Acquire, Implement / DSS: Deliver, Service, Support / MEA: Monitor, Evaluate, Assess) 내에서 5가지 핵심 컴포넌트(원리·정책·프로세스·조직구조·정보)와 7가지 집중 영역(문화·인적자원·역량 등)으로 분해됩니다.

```text
┌──── COBIT 2019 Governance System 매핑 흐름 ─────────────┐
│                                                           │
│  외부 환경(법·규제·시장·기술)                              │
│         │                                                 │
│         ▼                                                 │
│  ┌──────────────────┐    ┌──────────────────┐            │
│  │ Governance Obj.  │◄──►│  Stakeholder    │            │
│  │ (EDM 5개)        │    │  Needs & Goals  │            │
│  └──────────────────┘    └──────────────────┘            │
│         │                       │                         │
│         ▼                       ▼                         │
│  ┌──────────────────┐    ┌──────────────────┐            │
│  │ 5 Core Components│    │ 7 Focus Areas    │            │
│  │ - Principles      │    │ - Culture         │            │
│  │ - Policies        │    │ - People/Skills   │            │
│  │ - Processes       │    │ - Information     │            │
│  │ - Org Structure   │    │ - Services/Infra  │            │
│  │ - Information     │    │ - Applications    │            │
│  └──────────────────┘    └──────────────────┘            │
│         │                       │                         │
│         ▼                       ▼                         │
│  ┌──────────────────────────────────────────┐            │
│  │  Cascading Goals:                        │            │
│  │  Enterprise → IT → Process → Activity    │            │
│  │  (Balanced Scorecard 4관점 연계)         │            │
│  └──────────────────────────────────────────┘            │
└───────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 최고 의사결정층 거버넌스 | 이사회의 IT 전략 승인, ROI/NPV 평가, 리스크 한도 설정, COBIT EDM01~05 5개 GO 수행 |
| **APO (Align, Plan, Organize)** | 전략 정렬 및 기획 | IT 전략 맵(BSC 4관점), 포트폴리오 관리(PfM), 아키텍처 비전, 예산 편성(ITCAPEX/OPEX 70:30 원칙) |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축 및 도입 | PMBOK 7 8대绩效域, 애자일(Scrum/SAFe), CI/CD 파이프라인, 형상관리(GitOps) |
| **DSS (Deliver, Service, Support)** | 운영 및 서비스 제공 | ITIL 4 34개 실무 가이드, SLA/OLA/UC 3계층 계약, 인시던트/문제/변경 관리, AIOps |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 통제 | CSF/KPI(예: 시스템 가용성 99.95%, MTTR ≤ 30분), 내부감사, 외부감사, BCM/DR 훈련 |

**핵심 공식 및 정량 지표**:
- **TCO(Total Cost of Ownership)** = 직접비(HW/SW) + 간접비(운영·교육·다운타임) + 기회비용. 일반적으로 4년간 HW 27%, SW 17%, 운영·인력 45%, 다운타임 11% 구성
- **TBM(Technology Business Management)**: Gartner 프레임워크로 IT 비용을 서비스 단위($/user, $/transaction)로 분류
- **NPV(순현재가치)** = Σ[CFt/(1+r)^t] - 초기투자, **IRR(내부수익률)** = NPV=0이 되는 할인율
- **EVM(성과측정)**: CPI = EV/AC, SPI = EV/PV → CPI<1, SPI<1 일 때 Cost & Schedule 오버런 경고

- **📢 섹션 요약 비유**: COBIT 2019는 마치 **건물의 설계도**와 같습니다. EDM은 1층 입구의 안내 데스크(거버넌스), APO·BAI는 설계 부서(계획/구축), DSS는 24시간 경비·청소(운영), MEA는 감사팀(성과 평가)처럼 역할이 분리되어 있어야 건물이 무너지지 않습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 4대 글로벌 표준 프레임워크는 서로 경쟁 관계가 아닌 **상호 보완적 관계**입니다. 기술사 답안에서는 이들의 적용 범위·관점·출력물을 명확히 구분하고 통합 거버넌스 모델을 제시해야 합니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리(SM) 최적화 | 프로젝트 관리 지식 체계 | 정보보안 관리체계(ISMS) |
| **관점** | What/Why (거버넌스) | How (운영 실무) | How (프로젝트 수행) | What (보안 통제) |
| **구조** | 5도메인·40 GO·5 컴포넌트 | 4차원·34 Practice·SVS | 12 Principle·8 Perf Domain | 93 Annex A 통제(4 영역) |
| **대상** | CIO, 이사회, 감사인 | 서비스 매니저, 운영팀 | PM, 프로젝트 팀 | CISO, 보안 담당자 |
| **측정** | BSC 4관점, CSF/KPI | SLA, CSAT, NPS | EVM(CPI, SPI) | KRI, ISMS 인증 |
| **결합 방식** | 메타 프레임워크로 다른 표준 매핑 | COBIT DSS 도메인에 매핑 | COBIT BAI 도메인에 매핑 | COBIT APO13, DSS06에 매핑 |

**연결 아키텍처**:
- **EA(Enterprise Architecture)**: TOGAF ADM 8단계(Phase A~H)와 Zachman Framework 6×6 매트릭스로 비즈니스↔데이터↔애플리케이션↔기술 4계층 모델링
- **프로젝트 관리**: 전통적(Waterfall, PRINCE2) vs 애자일(Scrum, SAFe, LeSS) vs 하이브리드(Disciplined Agile Delivery, Spotify Model)
- **서비스 운영**: ITIL 4의 **34 Practice** 중 17개 일반 운영, 17개 서비스 운영 → AIOps·SRE·DevOps로 진화
- **보안 거버넌스**: ISO 27001(정보보안) + 27701(개인정보) + 22301(BCMS) + NIST CSF 5함수(Identify, Protect, Detect, Respond, Recover) 통합
- **클라우드·DX**: FinOps(클라우드 비용 최적화), Cloud Center of Excellence(CCoE), MLOps/LLMOps

- **📢 섹션 요약 비유**: COBIT·ITIL·PMBOK·ISO 27001은 마치 **자동차의 4륜 구동**과 같습니다. COBIT이 엔진(거버넌스), ITIL이 변속기(서비스), PMBOK이 차체(프로젝트), ISO 27001이 안전벨트(보안) — 어느 하나라도 약하면 차는 목표 지점에 안전히 도착할 수 없습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험(정보관리, 컴퓨터시스템응용, 정보보안 등)에서는 단순 암기보다 **"기업 상황 → 문제 정의 → 표준 프레임워크 적용 → 정량 KPI → 리스크/비용 분석 → 개선 로드맵"** 의 6단계 논리 구조로 답안 작성이 요구됩니다.

### 기술사형 판단 체크리스트

1. **거버넌스 구조 정합성**: "해당 기업의 3 Lines Model(① 1st Line: 비즈니스, ② 2nd Line: IT·보안·리스크, ③ 3rd Line: 내부감사) 및 RACI 매트릭스(Responsible, Accountable, Consulted, Informed)가 COBIT EDM01~05와 정합한가?" — 5W1H(누가, 무엇을, 언제, 어디서, 왜, 어떻게)로 명문화
2. **전략 정렬(Strategic Alignment)**: "IT 전략 맵(BSC 4관점: 재무/고객/내부프로세스/학습성장)이 기업 BSC 및 Porter Value Chain의 Primary·Support Activity와 연계되는가?" — Luftman의 IT-Business Alignment Maturity 5단계(Level 1: Ad Hoc ~ Level 5: Optimized) 평가
3. **프로젝트 거버넌스**: "PMBOK 7 8대绩效域(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)에 EVM·Agile·Risk Register가 통합 적용되는가?" — 프로젝트 단계별 Stage Gate(Initiation→Planning→Execution→Closing) 정의
4. **서비스 운영 SLA**: "ITIL 4 Service Value Chain(Plan→Engage→Design&Transition→Obtain/Build→Deliver&Support→Improve)의 6개 활동이 SLA(예: 가용성 99.95%, 응답시간 ≤2초, 인시던트 해결 4시간 이내)와 매핑되는가?" — OLA/UC로 내부·외부 계약 연계
5. **보안·컴플라이언스 통합**: "ISO 27001:2022 93개 통제 + 개인정보보호법 28개 + ISMS-P 인증 기준이 Zero Trust(Network/Application/Data/Identity 4영역) 및 SASE 아키텍처로 구현되는가?" — K-ISMS, GDPR, HIPAA, PCI-DSS 등 다중 규제 동시 준수 매트릭스

### 피해야 할 안티패턴

- **"프레임워크 나열식 답안"**: COBIT, ITIL, PMBOK, ISO 27001을 단순 나열만 하고 통합 모델 부재. → **거버넌스 통합 아키텍
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 514 / 800

← **이전**: [513. IT 경영 관리 핵심 토픽 513번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/513_it_management_core_topic_513_exam_summary/)
**다음**: [515. IT 경영 관리 핵심 토픽 515번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/515_it_management_core_topic_515_exam_summary/) →

---
