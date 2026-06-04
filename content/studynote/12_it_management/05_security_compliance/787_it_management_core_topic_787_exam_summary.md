+++
title = "787. IT 경영 관리 핵심 토픽 787번 시험 요약 (IT Management Core Topic 787 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019·ITIL 4·ISO 38500을 골격으로 한 거버넌스-관리-운영 3계층 체계이며, 전략(Strategy)→포트폴리오(Portfolio)→프로그램(Program)→프로젝트(Project)→운영(Operation) 가치사슬(Value Chain)을 통해 거버넌스 목표(GOAL)와 관리 목표(MGM)과 상호 매핑되어야 한다.
> 2. **가치**: McKinsey Digital研究表明 디지털 전환 성공 기업은 매출 20~30%, EBITDA 마진 2~5%p 개선, AX/EA 기반 SW사업 대가 산정 정확도 향상(±20% 이내), SLA 기반 인시던트 MTTR 60% 단축, 사이버보안 투자 ROI 3.2배(Based on Gartner 2024), 정보시스템 감리 부적정 판정률 5% 이하 유지.
> 3. **판단 포인트**: 중앙집중·분산형 조직 간 IT 거버넌스 모델 선택, BSC·CSF·KPI 3단 연계, B2B·B2C·B2G별 정보화사업 발주방식(턴키/분리발주/CM at Risk) 트레이드오프, BCM·DRS RTO/RPO 등급별 설계, 공공부문 DPL(Digital Public Ledger) 및 전자조달(나라장터·조달청 G2B) 컴플라이언스 확보가 핵심 의사결정 포인트.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입을 넘어 **디지털 전환(Digital Transformation)**·**AI 전환(AX)**·**ESG 경영**이 융합되는 VUCA 환경에서, IT 경영관리는 기업의 비즈니스 전략과 IT 자산·서비스·프로젝트를 **측정 가능한 가치(Value)**로 연결하는 체계적 관리 프레임워크를 요구한다. 한국정보화진흥원의 「정보시스템 감리」, 행정안전부의 「국가정보화 기본법」, 과기정통부의 「소프트웨어 진흥법」은 IT 경영관리의 법적 근거를 형성하며, 2024년 기준 약 187조 원 규모의 SW 산업 생태계에서 IT 거버넌스의 부재는 평균 23%의 사업 실패율(Standish Group CHAOS Report 2023)로 직결된다.

기존의 IT 관리(2000년대 이전)는 인프라·라이선스·인력을 **Cost Center**로 단순 관리했으나, 현재는 데이터를 핵심 무형자산으로 인식하는 **Data-Driven Governance** 패러다임으로 전환되었다. 클라우드·DevOps·FinOps·AIOps·제로트러스트·ISO 42001(AI 거버넌스)·NIST CSF 2.0·DORA(DevOps Research Assessment) 등 신규 표준의 등장으로 IT 경영관리는 정적 통제(Static Control)에서 **동적·연속적 통제(Continuous Controls Monitoring, CCM)** 중심으로 진화하고 있다.

```text
   ┌──────────────────────────────────────────────────────────────┐
   │          IT 경영관리 3계층 통합 거버넌스 구조                │
   │                                                              │
   │   ┌──────────── 상위(Governance) ─────────────┐              │
   │   │  [이사회/IT전략위원회]                      │              │
   │   │      ↓ (정렬/Align)                        │              │
   │   │  COBIT 2019 · ISO 38500 · ISO 37000       │              │
   │   │      ↓ (연결/Connect)                      │              │
   │   │   ┌──── 중위(Management) ────┐            │              │
   │   │   │  PMO · EA · ITSM · BCM   │            │              │
   │   │   │  전략→포트폴리오→프로그램 │            │              │
   │   │   │  →프로젝트→운영 가치사슬  │            │              │
   │   │   └──────────────────────────┘            │              │
   │   │      ↓ (실행/Execute)                      │              │
   │   │   ┌───── 하위(Operational) ─────┐         │              │
   │   │   │ AIOps · DevSecOps · FinOps │         │              │
   │   │   │ SLA·SLO·SLI·Error Budget   │         │              │
   │   │   └────────────────────────────┘         │              │
   │   └────────────────────────────────────────────┘             │
   │                                                              │
   │   외부: 컴플라이언스(IS감리·개인정보보호법·ESG·DORA)         │
   └──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: IT 경영관리는 자동차의 '통합 계기판 클러스터(Cluster)'와 같다. 속도계(BSC/KPI), 연료계(FinOps/Cost), 경고등(컴플라이언스), 내비게이션(EA/전략) 모두를 한 화면에서 끊임없이 운전자(이사회·경영진)에게 보여주는 통합 가시화 체계가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 **5대 핵심 축**(① IT 거버넌스, ② IT 전략·기획, ③ IT 프로젝트·사업관리, ④ IT 서비스·운영관리, ⑤ 정보화 사업법·컴플라이언스)으로 구성되며, 각 축은 다음의 기술적 원리로 구현된다.

```text
         ┌─────────────── IT 경영관리 통합 아키텍처 ───────────────┐
         │                                                          │
         │  [1] IT 거버넌스:  COBIT 2019 (40 Governance &          │
         │       Management Objectives) + ISO/IEC 38500 (6 원칙)    │
         │            │                                             │
         │            ▼                                             │
         │  [2] IT 전략 기획:  TOGAF 10 ADM + Zachman 6×6         │
         │            │    + BCG/Porter 가치사슬 정렬                │
         │            ▼                                             │
         │  [3] 프로젝트 관리: PMBOK 7 (8 Performance Domains)     │
         │            │    + PRINCE2 + SAFe 6.0 + ISO 21500         │
         │            │    + Agile/Waterfall/Hybrid                 │
         │            ▼                                             │
         │  [4] 서비스 운영:  ITIL 4 (34 Practices, SVS)             │
         │            │    + DevOps DORA 4 Metrics                   │
         │            │    + SRE(Error Budget·SLO)                   │
         │            ▼                                             │
         │  [5] 컴플라이언스: 정보시스템 감리법 + SW 진흥법         │
         │                    + 개인정보보호법 + ISO 27001/42001   │
         │            │                                             │
         │            ▼                                             │
         │   ┌────────── 측정·개선(Measure & Improve) ──────┐      │
         │   │ KPI Tree → CSF → Goal Cascade → CSF/KPI →   │      │
         │   │ RACI Matrix → Risk Register → Audit Trail    │      │
         │   └──────────────────────────────────────────────┘      │
         └──────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 의사결정기구** (IT Steering Committee / IT 거버넌스 위원회) | 전략적 의사결정·리스크 승인·예산 심의 | ISO/IEC 38500 6원칙(Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior), RACI 매트릭스, 분기별 Cadence 회의 운영, 의사결정 트리(Decision Tree) 적용, 이사회의 IT 리터러시(BoD IT Literacy) 제고 |
| **EA(Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층 정렬 | TOGAF 10 ADM(Architecture Development Method) 8단계(Phase A~H) — Preliminary→A(Vision)→B~D(BA/DI/TA)→E(기회)→F·G(마이그레이션/구현 거버넌스)→H(변경 관리), Zachman 6×6 매트릭스(What·How·Where·Who·When·Why × Planner·Owner·Designer·Builder·Subcontractor·Operational), DoDAF·FEAF·ArchiMate 3.2 표준 모델 |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 통제·자원 배분·성과 측정 | PMBOK 7th 8 Performance Domain(Stakeholder·Team·Development·Planning·Project Work·Delivery·Measurement·Uncertainty), Earned Value Management(EVM: PV·EV·AC·CV·SV·CPI·SPI), Portfolio Kanban, Benefits Realization(ROI·NPV·IRR), Tailoring & Hybrid(예측형·반복형·애자일 혼합) |
| **ITSM(IT Service Management)** | 서비스 카탈로그·인시던트·문제·변경·릴리즈 관리 | ITIL 4 Service Value System(SVS) — Opportunity/Demand → Value → Guiding Principles(7) → Governance→Practices(34)→Continual Improvement, Service Desk Tier 1~3, Knowledge-Centered Service(KCS), CMDB(구성항목 DB) CSDM(CMDB Service Management) 모델 |
| **컴플라이언스·감리 체계** | 법·내부통제·IS감리·보안 통제 검증 | 정보시스템 감리법(2024년 5개 영역: 사업·재무·성능·보안·재산), SW 진흥법(대기업 SW 발주 의무), ISO/IEC 27001:2022(Annex A 93통제), ISO/IEC 42001:2023(AI 관리체계), 3 Lines of Defense(3LoD), SOX 404 IT General Controls, COBIT 2019 Design Factors 11개(전략·목표·리스크·문제·인자) |

각 계층의 핵심 알고리즘·파라미터는 다음과 같이 정량화된다.

- **CSF/Critical Success Factor → KPI 도출 공식**: `KPI = (실제값/목표값) × 100` 또는 `KPI = (Baseline - Actual) / (Baseline - Target) × 100` (지표 정상화 공식)
- **EVM(Earned Value)**: `CV = EV - AC` (Cost Variance), `SV = EV - PV` (Schedule Variance), `CPI = EV / AC` (≥1 양호), `SPI = EV / PV` (≥1 양호), `EAC = BAC / CPI` (예상 완료 비용), `TCPI = (BAC - EV) / (BAC - AC)`
- **BSC 4관점**: 재무(Financial)·고객(Customer)·내부 프로세스(Internal Process)·학습·성장(Learning & Growth) — 전략 맵(Strategy Map)으로 인과관계 시각화
- **SW사업 대가 산정** (SW 진흥법 시행령): ① 기능점수(FP) 기반, ② LOC·COCOMO·Putnam·COCOMO II·SLIM, ③ 원가계산(노무비·경비·이윤·일반관리비·기술료), 보정계수(규모·복잡도·신뢰도) 적용
- **RTO/RPO/MTPD**: BCM·DRS 핵심 파라미터 — Tier1(0~1h/0/near 0), Tier2(4h/1h/8h), Tier3(24h/4h/72h), Tier4(72h/24h/7d)
- **FinOps 분배 모델**: `Showback = (서비스별 리소스사용량 × 단가)` / `Chargeback = (Showback × 배부 비율 + 간접비)`
- **AIOps 이상탐지**: 시계열 ARIMA·Prophet·LSTM 기반 MTTD < 5분, MTTR < 30분 (업계 기준: MTTR 1시간 대비 50%↓)
- **DORA 4 Metrics**: 배포 빈도(Deployment Frequency)·리드 타임(Lead Time for Change)·변경 실패율(Change Failure Rate)·복구 시간(MTTR) — Elite, High, Medium, Low 4등급 (2024년 Elite 기준: 일 1회 이상 배포·1일 이내 리드타임·0~15% 실패율·1시간 이내 복구)

- **📢 섹션 요약 비유**: 5대 축은 '의료 시스템'과 같다. 거버넌스는 예방의학(질병 예방), EA는 해부학(전체 구조 이해), PMO는 외과수술(정밀한 시술), ITSM은 응급실(서비스 복구), 컴플라이언스는 진단검사(법·규정 검증)다. 어느 하나라도 빠지면 환자는 회복할 수 없다.

---

## Ⅲ. 비교 및 연결

IT 경영관리의 핵심 프레임워크 간 비교는 기술사 시험에서 빈도가 높다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7th** | **ISO 27001/42001** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 목표 표준화 | IT 서비스 운영·가치 창출 | 이사회·경영진의 IT 통제 원칙 | 프로젝트 관리 지식체계 | 정보보안·AI 보안 통제 |
| **구조/원리** | 40 Governance & Management Objectives, 11 Design Factors | SVS (Service Value System), 34 Practices, 7 Guiding Principles | 6 Principles (Responsibility~Human Behavior) | 8 Performance Domains, 12 Principles, Tailoring | Plan-Do-Check-Act + Annex A 통제항목 |
| **대상** | CIO·IT 거버넌스 위원회·감사인 | ITSM 운영자·실무자 | 이사·최고 의사결정권자 | 프로젝트 매니저·PMO | CISO·보안 책임자·AI 거버넌스 위원회 |
| **평가·인증** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | 인증 없음(원칙만 제시) | PMI 인증(PMP, PfMP) | ISO 27001·42001 인증심사 |
| **연계성** | ITIL/ISO 27001/PMBOK과 매핑(메타·관리 시스템) | DevOps·SIAM·SRE와 통합 운영 | 정책·전략 레벨 거버넌스 정합 | EVM·Agile·SAFe·DevOps 연계 | ISMS-P 인증·정보통신망법·NIS 2.0 |
| **측정 지표** | Process Capability Level 0~5 (ISO 15504 PAM) | SLA·SLO·CSAT·MTTR·MTBF | Maturity Level(자체 평가) | SPI·CPI·TCPI·ROI | KRI·KCI·보안 통제 준수율 |

| 구분 | **예측형(Waterfall)** | **반복형(Iterative)** | **애자일(Agile
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 787 / 800

← **이전**: [786. IT 경영 관리 핵심 토픽 786번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/786_it_management_core_topic_786_exam_summary/)
**다음**: [788. IT 경영 관리 핵심 토픽 788번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/788_it_management_core_topic_788_exam_summary/) →

---
