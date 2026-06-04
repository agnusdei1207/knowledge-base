+++
title = "703. IT 경영 관리 핵심 토픽 703번 시험 요약 (IT Management Core Topic 703 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 703번은 COBIT 2019, ITIL 4, ISO/IEC 38500, Balanced Scorecard를 통합한 **IT 거버넌스-전략-운영-성과** 4계층 프레임워크로, 기업의 디지털 전환(DX) 과정에서 IT 투자 대비 가치 실현(Value Delivery)을 체계적으로 관리하는 것이 본질이다.
> 2. **가치**: EGIS(Enterprise Governance of IT & Strategy) 모델 적용 시 IT 투자 ROI 평균 25~40% 개선, 프로젝트 실패율 30%→8% 감소, IT 부채(Technical Debt) 50% 절감, Time-to-Market 60% 단축 등 정량적 효과를 창출한다.
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프는 ①중앙화 vs 분권화(CoE vs Federated), ②Waterfall vs Agile 거버넌스, ③CAPEX vs OPEX 투자 구조, ④내부 역량 vs Outsourcing 전략으로, 조직의 디지털 성숙도(Level 1~5)에 따라 최적 모델이 달라진다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 "시스템 안정 운영" 중심의 Cost Center에서, 4차 산업혁명 이후 "비즈니스 가치 창출" 중심의 **Value Center**로 패러다임이 전환되었다. 2020년 이후 COVID-19를 기점으로 한 비대면 업무, 클라우드 전면 전환, 생성형 AI 도입 가속화로 인해, IT 부서의 역할은 단순 백오피스를 넘어 **전략적 비즈니스 파트너**로 재정의되고 있다. 그러나 한국 정보화진흥원의 조사에 따르면 국내 대기업의 약 67%가 IT-비즈니스 전략 정렬(Strategic Alignment)에 실패하며, Gartner 보고서에서도 기업의 IT 예산 중 **30%만 실제 가치를 창출**한다고 분석된다. 이러한 실패의 근본 원인은 ①IT 거버넌스 부재, ②성과 측정 체계 미비, ③리스크 관리 한계, ④조직 역량 갭에 있으며, 이를 해결하기 위해 본 토픽에서는 **IT 거버넌스-전략-서비스-포트폴리오**의 4축 통합 관리 체계와 의사결정 프레임워크를 다룬다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│          703번 IT 경영 관리 4계층 통합 프레임워크 (EGIS Model)        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │  Layer 1: IT 거버넌스 (Governance) - "바람직한 방향 설정"  │     │
│   │  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐    │     │
│   │  │ 이사회/IT   │ │ 정책/표준    │ │ 리스크/컴플라이언스│    │     │
│   │  │ 전략위      │ │ (COBIT 2019) │ │ (ISO 38500/27001)│    │     │
│   │  └──────┬──────┘ └──────┬───────┘ └────────┬────────┘    │     │
│   └─────────┼────────────────┼──────────────────┼────────────┘     │
│             │                │                  │                   │
│             ▼                ▼                  ▼                   │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │  Layer 2: IT 전략 (Strategy) - "가치 창출 로드맵"         │     │
│   │  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐    │     │
│   │  │ 비즈니스    │ │ 디지털 전환  │ │ IT 포트폴리오    │    │     │
│   │  │ 정렬(BSA)   │ │ (DX) 전략    │ │ 관리(PPM)       │    │     │
│   │  └──────┬──────┘ └──────┬───────┘ └────────┬────────┘    │     │
│   └─────────┼────────────────┼──────────────────┼────────────┘     │
│             │                │                  │                   │
│             ▼                ▼                  ▼                   │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │  Layer 3: IT 운영/서비스 (Operation) - "안정적 가치 전달" │     │
│   │  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐    │     │
│   │  │ 서비스 운영 │ │ 프로젝트/    │ │ 인프라/플랫폼    │    │     │
│   │  │ (ITIL 4)    │ │ 애자일(SAFe) │ │ (Cloud/K8s)     │    │     │
│   │  └──────┬──────┘ └──────┬───────┘ └────────┬────────┘    │     │
│   └─────────┼────────────────┼──────────────────┼────────────┘     │
│             │                │                  │                   │
│             ▼                ▼                  ▼                   │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │  Layer 4: 성과/측정 (Performance) - "지속적 개선"          │     │
│   │  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐    │     │
│   │  │ KPI/BSC     │ │ IT 성숙도    │ │ ROI/TCO/NPV     │    │     │
│   │  │ 대시보드    │ │ 진단 모델    │ │ 분석            │    │     │
│   │  └─────────────┘ └──────────────┘ └─────────────────┘    │     │
│   └───────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ◀───── 피드백 루프: PDCA + OKR + Balanced Scorecard ─────▶         │
└─────────────────────────────────────────────────────────────────────┘
```

**패러다임 전환 비교**:
- **Old Paradigm (1990~2010)**: IT는 "비용", "백오피스", "프로젝트 단위 관리", "사일로 조직", "연 1회 예산 편성"
- **New Paradigm (2010~현재)**: IT는 "투자", "프론트오피스 가치창출", "제품/서비스 단위 관리", "DevSecOps/플랫폼 팀", "Rolling Wave 예산"

- **📢 섹션 요약 비유**: IT 경영 관리는 **배의 키잡이(Rudder)** 와 같습니다. 배(기업)가 아무리 크고 강력해도 키잡이가 없으면 방향을 잃고 표류합니다. 703번 토픽은 그 키잡이가 어떤 나침반(COBIT)을 보고, 어떤 돛대 전략(Strategy)을 세우며, 어떤 선원(Service)들을 지휘할지에 대한 종합 항해술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 기반 거버넌스 시스템 (Governance System)

COBIT 2019는 **40개의 거버넌스/관리 목표(Governance & Management Objectives)** 를 5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess)으로 구성한다. 핵심 원리는 **"목표 계단식 연결(Cascading Goals)"** 로, Stakeholder Needs → Enterprise Goals → Alignment Goals → IT Goals → Process Goals의 5단계 인과 사슬을 통해 IT가 비즈니스 목표에 어떻게 기여하는지 정량적으로 추적한다.

```text
┌──────────────────────────────────────────────────────────────┐
│        COBIT 2019 Cascading Goals 의사결정 흐름도             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Level 0] Stakeholder Needs (이해관계자 니즈)                │
│       │  수익성, 성장, 위험관리, 규제준수, 지속가능성          │
│       ▼                                                      │
│  [Level 1] Enterprise Goals (기업 목표, 13개)                 │
│       │  EG01: 포트폴리오 경쟁력, EG05: 고객서비스,           │
│       │  EG08: 디지털 제품/서비스, EG13: 디지털 혁신          │
│       ▼                                                      │
│  [Level 2] Alignment Goals (정렬 목표, 13개)                  │
│       │  AG01: IT 준수 및 지원, AG05: IT 투자 실현,           │
│       │  AG09: 디지털 혁신, AG11: 정보 보안                    │
│       ▼                                                      │
│  [Level 3] IT Goals (IT 목표, 13개)                           │
│       │  ITG01: 비즈니스 정렬, ITG04: 리스크 관리,            │
│       │  ITG09: 정보 처리, ITG13: 지식·전문성                 │
│       ▼                                                      │
│  [Level 4] Process Goals (프로세스 목표, 40개)                │
│       │  EDM01: 거버넌스 체계, APO12: 리스크 관리,            │
│       │  BAI03: 솔루션 관리, DSS02: 서비스 요청 처리          │
│       ▼                                                      │
│  [Level 5] Activity Metrics (활동 측정지표)                   │
│          KPI, CSF, KGI 3단계 측정 체계                         │
└──────────────────────────────────────────────────────────────┘
```

### 2. IT 성과 측정의 3단계 모델 (KGI → CSF → KPI)

- **KGI (Key Goal Indicator)**: "What" - 목표 달성 여부 (예: ROI 18%, 고객만족도 90%)
- **CSF (Critical Success Factor)**: "What" + "Where" - 성공을 위한 핵심 영역 (예: 사용자 경험, 시스템 안정성)
- **KPI (Key Performance Indicator)**: "How" - 일상적 측정 (예: 응답시간 2초, 가용성 99.95%)

### 3. 핵심 구성 요소 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (ITGC)** | 최고 의사결정 기구, 의사결정 권한 위임 구조 (RACI 매트릭스) | CIO/CTO 의장, CEO·CFO·CDO·사업본부장 참여, 월 1회 정례 회의, 이사회 직속 보고 체계 (Dual Reporting) |
| **전략 정렬 매핑 (BSA Matrix)** | 비즈니스-IT 목표 간 인과관계 시각화 | Business Capability Map + IT Investment Portfolio, MECE 원칙으로 5×5 매트릭스 도출, Gap Analysis로 우선순위 산정 |
| **IT 포트폴리오 관리 (PPM)** | 프로젝트/프로그램/제품 단위 투자 최적화 | DARE 모델 (Decide/Architect/Realize/Exploit), Stage-Gate 프로세스, 3-Tier 분류(Must-Run/Should-Run/Could-Run) |
| **서비스 운영 (ITIL 4 SVS)** | 34개 서비스 관리 관행(Value Stream 중심) | Service Value System: Opportunity/Demand→Value, 7가지 가이드 원칙(Guiding Principles), 4개 차원(조직/사람/정보/공급자) |
| **성과 대시보드** | 실시간 KPI/BSC 모니터링 | Power BI/Grafana/Tableau, BSC 4관점(재무/고객/내부/학습성장), OKR 통합 추적, Critical Metric Threshold Alert |

### 4. 핵심 수식 및 알고리즘

**IT 투자 우선순위 산정 공식 (AHP + TCO/ROI 통합)**:
```
Priority Score = (ROI × Strategic Alignment) / (TCO × Risk Factor)

여기서:
  ROI = (총 편익 - 총 비용) / 총 비용 × 100
  TCO = CAPEX + OPEX(3~5년) + Risk-Adjusted Cost
  Strategic Alignment = Σ(BCS_i × W_i), BCS: Business Criticality Score(1~5)
  Risk Factor = P(실패) × Impact Cost
```

**IT 성숙도 평가 모델 (CMMI 5단계 + 보정)**:
- **Level 1 (Initial)**: 프로세스 비공식, 성공 = 개인 역량
- **Level 2 (Managed)**: 프로젝트 단위 반복, 기본 측정
- **Level 3 (Defined)**: 조직 표준 프로세스, ProPI(Process Performance Model)
- **Level 4 (Quantitatively Managed)**: 통계적 기법(SPC), 예측 가능
- **Level 5 (Optimizing)**: 지속적 혁신, Causal Analysis & Resolution

- **📢 섹션 요약 비유**: COBIT Cascading Goals는 **"건물의 하중 전달 경로"** 와 같습니다. 지붕의 비(Stakeholder Needs) → 보(Enterprise Goals) → 기둥(Alignment Goals) → 슬라브(IT Goals) → 기초(Process Goals)로 하중이 안전하게 전달되어야 건물이 무너지지 않습니다. 어느 한 단계에서 부실 시공이 발생하면 전체가 흔들리죠.

---

## Ⅲ. 비교 및 연결

### 거버넌스 프레임워크 비교

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 (IT Governance) | CMMI Institute |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리(SM) 운영 지침 | IT 의사결정 책임·원칙 표준 | 조직 프로세스 성숙도 평가 |
| **Scope** | End-to-End (Strategy~Operation) | 주로 Service Operation/Delivery | Governance 원칙 + 6대 원칙 | 프로세스 품질 + 성숙도 |
| **핵심 구성** | 40 Objectives, 5 Domain | 34 Practices, 4 Dimensions | 6 Principles, Model | 5 Maturity Levels |
| **측정 방식** | Process Capability (0~5) | Maturity Model | Conformance/Performance | Appraisal 결과 등급 |
| **적용 대상** | 전사 IT 조직, CIO | ITSM 팀, 운영 조직 | 이사회·경영진 | SW 개발, 서비스 조직 |
| **상호보완** | ↔ Balanced Scorecard | ↔ DevOps, SIAM | ↔ COBIT, ISO 27001 | ↔ CMMI-SVC, CMMI-DEV |

### 다른 표준/프레임워크와의 연결 관계

- **TOGAF + COBIT**: TOGAF의 ADM(Architecture Development Method) Phase E(기회/솔루션)와 Phase F(변경 계획) 단계에서 COBIT의 APO/BAI 도메인을 활용하여 아키텍처 거버넌스 연결
- **PMBOK/PRINCE2 + COBIT**: 프로젝트 관리 표준을 COBIT의 BAI 도메인에 매핑, Gate Review 시 BAI01~BAI11 체크리스트 활용
- **Agile/SAFe + ITIL 4**: Scaled Agile의 PI Planning과 ITIL 4의 Service Value Stream 통합, DevOps 파이프라인과 Incident/Change Management 자동화
- **ISO 27001 + ISO 38500**: 정보 보안 거버넌스(27001)와 IT 거버넌스(38500) 통합 감사 체계, ISMS 인증 시 38500 준수 여부 확인

### 아키텍처 통합 패턴

```text
┌─────────────────────────────────────────────────────────────┐
│        기업 거버넌스 - IT 거버넌스 통합 아키텍처             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────────────────────────────────────┐          │
│   │   Enterprise Governance (COSO, King IV)      │          │
│   │   ┌──────────────┐    ┌──────────────┐       │          │
│   │   │ Strategy      │    │ Risk         │       │          │
│   │   │ Committee     │◄──►│ Committee    │       │          │
│   │   └──────┬───────┘    └──────┬───────┘       │          │
│   └──────────┼────────────────────┼────────────────┘          │
│              │                    │                            │
│              ▼                    ▼                            │
│   ┌──────────────────────────────────────────────┐          │
│   │   IT Governance (COBIT 2019 + ISO 38500)     │          │
│   │   ┌──────────┐ ┌──────────┐ ┌──────────┐    │          │
│   │   │ EDM(전략)│ │ APO(계획)│ │ BAI(구축)│    │          │
│   │   └──────────┘ └──────────┘ └──────────┘    │          │
│
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 703 / 800

← **이전**: [702. IT 경영 관리 핵심 토픽 702번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/702_it_management_core_topic_702_exam_summary/)
**다음**: [704. IT 경영 관리 핵심 토픽 704번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/704_it_management_core_topic_704_exam_summary/) →

---
