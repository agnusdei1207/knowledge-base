+++
title = "662. IT 경영 관리 핵심 토픽 662번 시험 요약 (IT Management Core Topic 662 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500 등 거버넌스 프레임워크를 기반으로 IT 전략(Strategy)-구조(Structure)-프로세스(Process)-기술(Technology)-사람(People)의 5요소를 정렬하여 기업 가치를 극대화하는 체계적 경영 활동이다.
> 2. **가치**: BMC(Balanced Scorecard) 기반 성과관리 시 4관점(재무/고객/내부프로세스/학습성장) 균형 시 ROI 평균 28% 향상, IT 거버넌스 성숙도 1단계 상승 시 운영 비용 15-20% 절감 효과가 검증되었다.
> 3. **판단 포인트**: 중앙집중형 vs 분산형 거버넌스, Build vs Buy, Quick-Win vs Strategic-Bet 투자 포트폴리오, Agile-Waterfall 하이브리드 프로세스 등 4대 트레이드오프에서 조직 성숙도와 규제 환경을 기준으로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화로 인해 IT는 단순 지원 기능을 넘어 기업의 생존과 직결된 핵심 전략 자산으로 격상되었다. 그러나 한국 정보시스템 감리 통계(2023)에 따르면 전체 IT 프로젝트의 41%가 일정 초과, 37%가 예산 초과, 28%가 기대 효과 미달로 종료되어, IT 경영 관리 체계의 부재가 기업 경쟁력 약화의 주요 원인으로 부상하고 있다. 이러한 문제의 근본 원인은 CEO/CIO 간 IT 가치 인식 괴리, 부서별 사일로(Silo)화된 IT 투자, 측정 불가능한 성과 지표(KPI) 운영으로 요약된다.

```text
[IT 경영 관리 프레임워크 전체 구조도]

  ┌─────────────────────────────────────────────────────────────┐
  │              Mission / Vision / 전략적 목표                  │
  └──────────────────────────┬──────────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────────┐
  │                  IT 거버넌스 (Governance)                     │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
  │  │ 전략위   │  │  CIO     │  │  EA위    │  │ PMO      │    │
  │  │ (Steering│  │ (의사결정)│  │ (표준화) │  │ (집행)   │    │
  │  │  Committee)│ │          │  │          │  │          │    │
  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
  └───────┼─────────────┼─────────────┼─────────────┼───────────┘
          │             │             │             │
  ┌───────▼─────────────▼─────────────▼─────────────▼───────────┐
  │                    IT 관리 프로세스                          │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
  │  │전략기획  │→ │포트폴리오│→ │프로젝트  │→ │서비스   │    │
  │  │(ISP)     │  │관리(PPM) │  │관리(PMO) │  │운영(ITSM)│    │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
  └───────┬─────────────────────────────────────────┬───────────┘
          │                                         │
  ┌───────▼───────────────────┐  ┌─────────────────▼───────────┐
  │   BSC 기반 성과 측정       │  │   리스크/컴플라이언스        │
  │  (4관점 KPI)              │  │  (ISO 27001, GDPR, PIPC)   │
  └───────────────────────────┘  └─────────────────────────────┘
```

기존 패러다임은 IT를 비용 중심(Cost Center)으로 인식하여 CAPEX(자본적 지출) 회계 방식에 머물렀으나, 새로운 패러다임은 IT를 가치 창출 센터(Value Center)로 재정의하고, 클라우드/구독 모델 기반 OPEX(운영적 지출)와 TCO(Total Cost of Ownership) 기반 의사결정을 수행한다. 이를 위해 BSIMM(Building Security In Maturity Model), CMMI(Capability Maturity Model Integration) 등 성숙도 모델을 활용한 정량적 거버넌스가 필수적이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 계기판과 같습니다. 엔진(IT 시스템)이 아무리 좋아도 계기판(거버넌스/성과지표) 없이는 속도, 연료, 엔진 상태를 알 수 없으며, 운전자는 과속하거나 연료 부족으로 멈춰버립니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 아키텍처는 크게 **거버넌스 계층(Governance Layer)**, **관리 프로세스 계층(Management Process Layer)**, **운영 계층(Operation Layer)**의 3-tier 구조로 설계된다. 각 계층은 RACI 매트릭스(Responsible, Accountable, Consulted, Informed)로 역할과 책임을 명확히 정의하며, COBIT 2019의 40개 관리 목표(Management Objective)와 5개 도메인(EDM: Evaluate-Direct-Monitor; Align-Plan-Organize; Build-Acquire-Implement; Deliver-Service-Support; Monitor-Evaluate-Assess)에 매핑된다.

```text
[IT 투자 의사결정 및 가치 실현 흐름 - 5단계 Value Realization Model]

  Stage 1        Stage 2        Stage 3        Stage 4        Stage 5
  [아이디어]  →  [평가/선정]  →  [실행]      →  [운영]      →  [성과측정]
  Idea          Selection       Execution      Operation      Evaluation
  ─────────────────────────────────────────────────────────────────────
  ┌─────┐     ┌─────────┐     ┌─────────┐   ┌─────────┐   ┌─────────┐
  │     │     │ Business│     │ Project │   │ Service │   │ KPI    │
  │Idea │────▶│ Case    │────▶│ Mgmt    │──▶│ Mgmt    │──▶│ BSC    │
  │Pool │     │ (NPV,   │     │ (PMO)   │   │ (ITSM)  │   │ Score  │
  │     │     │ IRR,    │     │         │   │ SLA    │   │        │
  └─────┘     │ Payback)│     └─────────┘   └─────────┘   └─────────┘
              └─────────┘            │              │            │
                                    │              │            │
                              ┌─────▼─────┐   ┌─────▼─────┐  ┌──▼──────┐
              [Stage 3 Gate]   │Scope/    │   │Benefit    │  │Value   │
              일정/품질/예산   │Schedule/ │   │Realization│  │Capture │
              Triple Constraint│Budget   │   │Plan       │  │        │
                              └──────────┘   └────────────┘  └─────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 전략위원회 (Steering Committee)** | CIO·CEO·CFO·COO 등 C-Level 의사결정 기구 | 월 1회 정례 회의, IT 투자 포트폴리오 승인, BSC 관점별 KPI 리뷰, ISO 38500 6원칙(Evaluate-Direct-Monitor-Decide) 적용 |
| **COBIT 2019 거버넌스 시스템** | IT 목표-기업 목표 정렬, 40개 관리 목표 | Cascade Goal: 기업 13목표 → IT 13목표 → Enabler 7종(원리/정책/프레임워크/프로세스/조직/정보/인프라) |
| **BSC (Balanced Scorecard)** | 4관점 균형 성과 측정 | 재무관점(ROI, NPV) / 고객관점(NPS, CSAT) / 내부프로세스(처리속도, 결함률) / 학습성장(직원역량, 혁신률) |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 통합 관리 | Earned Value Management(EVM: CPI, SPI), 위험도-가치 매트릭스, Stage-Gate Process, KPI 대시보드 |
| **EA (Enterprise Architecture)** | 업무-정보-시스템-기술 4계층 표준화 | TOGAF ADM(Architecture Development Method) 8단계, Zachman Framework 6x6 매트릭스, ARIS/EA플랫폼 |
| **ITSM (IT Service Management)** | 서비스 설계-전이-운영-개선 | ITIL 4 Service Value Chain, SLA/OLa/UC(서비스수준/조직간/내부지원) 3계층 계약 |
| **GRC (Governance-Risk-Compliance)** | 리스크/규제 통합 관리 | ISO 27001(ISMS), ISO 31000(리스크), GDPR/PIPC(개인정보), RMF(Risk Management Framework) |

### 핵심 가치 산정 모델 (Quantitative)

- **NPV (Net Present Value)**: `NPV = Σ[CFt / (1+r)^t] - 초기투자` — 순현재가치. WACC(가중평균자본비용) 기준 r 적용, 양수일 경우 투자 채택
- **IRR (Internal Rate of Return)**: NPV=0이 되는 할인율. IRR > hurdle rate(일반 12-15%)일 때 투자
- **Payback Period**: 누적 현금흐름이 투자금을 회수하는 시점. 통상 3-5년 이내 권장
- **TCO (Total Cost of Ownership)**: 직접비용(HW/SW/Lic) + 간접비용(운영/훈련/다운타임) + 기회비용. 일반적으로 초기투자비의 3-5배
- **VOI (Value on Investment)**: 재무적 가치 + 전략적 가치 + 위험회피 가치의 정성/정량 통합 측정. BSC와 연계

### 거버넌스 의사결정 모델

- **RACI 매트릭스**: 각 활동에 대해 1명의 A(Accountable), 1-2명의 R(Responsible), 다수의 C(Consulted), I(Informed) 배정
- **Stage-Gate Process**: Idea → Business Case → Plan → Develop → Test → Launch → Operate의 7단계별 Go/Kill 결정
- **Risk-Value Matrix**: 4분면(고위험-고가치/고위험-저가치/저위험-고가치/저위험-저가치)으로 투자 우선순위 결정

- **📢 섹션 요약 비유**: COBIT과 BSC는 회사의 '두뇌'와 '심장'과 같습니다. COBIT(거버넌스)이 두뇌처럼 합리적 의사결정 구조를 짜고, BSC(성과측정)가 심장처럼 4가지 혈관(4관점)으로 가치를 온몸에 공급합니다. 둘 중 하나라도 없으면 조직은 죽거나 방향을 잃습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 자주 혼동되는 주요 프레임워크와 개념을 비교한다. 기술사 시험에서는 각 프레임워크의 적용 범위(Scope), 목적(Objective), 핵심 산출물(Key Artifact), 조직 성숙도 적용 단계를 명확히 구분할 수 있어야 한다.

| 구분 | **COBIT 2019** (거버넌스) | **ITIL 4** (서비스 운영) | **PMBOK 7** (프로젝트 관리) | **ISO 38500** (IT 거버넌스 표준) |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT와 비즈니스 목표 정렬 | IT 서비스 가치 공동창조 | 프로젝트 성공적 수행 | IT 의사결정의 책임·투명성 |
| **적용 범위** | 엔터프라이즈 전체 (전략→운영) | 서비스 라이프사이클 중심 | 단일 프로젝트 한정 | 거버넌스 의사결정 원칙 |
| **핵심 산출물** | 40 관리목표, 7 Enabler, Maturity Model | 34 Practice, Service Value Chain | 12 Project Principles, 8 Domains | 6 원칙(책임/전략/취득/성능/규정/인간) |
| **프로세스 수** | 40개 관리목표 | 34개 Practice | 8개 Performance Domain | 6개 원칙 + 5개 거버넌스 모델 |
| **성숙도 모델** | CMMI 0-5단계 (6단계) | 4-Dimension 모델 | Organizational Maturity | 자체 평가 체크리스트 |
| **연계 프레임워크** | ISO 27001, NIST CSF, COSO ERM | DevOps, Agile, Lean | PRINCE2, Agile (Scrum/Kanban) | COBIT, ISO 27001, ISO 31000 |
| **주 사용자** | CIO, IT 거버넌스 위원회 | 서비스 매니저, ITSM 운영자 | PMO, 프로젝트 매니저 | 이사회, CEO, CIO |
| **업데이트 주기** | 2019 (이전 2005, 2012) | 2019 (이전 v3 2011) | 2021 (이전 v6 2017) | 2015 (이전 2008) |
| **인증 제도** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | PMP, CAPM | 인증 없음 (표준) |
| **한국 적용** | 공공부문 EA 5개년 계획, DTO | 데이터센터 운영, 클라우드 MSP | NIPA 프로젝트 관리 표준 | 전자정부 거버넌스 가이드 |

### 다른 시스템 컴포넌트와의 통합

```text
[IT 경영 관리 통합 아키텍처 - 거버넌스/관리/운영/인프라 4계층]

  ┌─────────────────────────────────────────────────────────────┐
  │ [1] 거버넌스 계층: ISO 38500 / COBIT 2019                   │
  │      - 이사회/전략위 / BSC / GRC 대시보드                    │
  │         ↓ KPI/CSF (Critical Success Factor)                 │
  ├─────────────────────────────────────────────────────────────┤
  │ [2] 관리 계층: ISP / EA / PPM / Portfolio Mgmt              │
  │      - TOGAF / Zachman / Stage-Gate / Risk-Value Matrix     │
  │         ↓ 서비스 카탈로그 / 프로젝트 헌장(Project Charter)   │
  ├─────────────────────────────────────────────────────────────┤
  │ [3] 운영 계층: ITIL 4 / DevOps / Agile / SRE               │
  │      - Service Value Chain / CI-CD Pipeline / AIOps        │
  │         ↓ SLA / OLA / UC (계약서)                            │
  ├─────────────────────────────────────────────────────────────┤
  │ [4] 인프라/플랫폼 계층: Cloud / Container / Data Platform    │
  │      - AWS/Azure/GCP / K8s / Snowflake / Data Lake         │
  │         ↓ IaC(Terraform) / Observability(Prometheus-Grafana)│
  └─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: COBIT과 ITIL의 관계는 도시계획(COBIT)과 건물 관리(ITIL)의 차이입니다. 도시계획이 전체 도시의 토지이용·도로·공원 배치를 결정(거버넌스)한다면, 건물 관리는 개별 건물의 HVAC·소방·청소를 관리(운영)합니다. 둘 다 필요하지만 책임 영역이 다릅니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험은 단순 암기형이 아닌 **상황 판단형 사례 문제**가 다수 출제된다. 다음과 같은 실무 의사결정 시나리오에서 최적의 판단 기준을 제시할 수 있어야 한다.

### 실무 적용 시나리오별 의사결정 프레임워크

**시나리오 1: IT 투자 포트폴리오 배분**
총 IT 예산 100억 원, 신규 디지털 전환 투자 30억, 운영 유지보수 50억, 혁신 실험 10억, 규제 준수 10억 배분 시, BCG 매트릭스를 활용하여 (①Quick-Win: 60%, ②Strategic Bet: 30%, ③Option: 10%)로 구분하고, 분기별 Stage-Gate에서 Go/Pivot/Kill 결정한다.

**시나
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 662 / 800

← **이전**: [661. IT 경영 관리 핵심 토픽 661번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/661_it_management_core_topic_661_exam_summary/)
**다음**: [663. IT 경영 관리 핵심 토픽 663번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/663_it_management_core_topic_663_exam_summary/) →

---
