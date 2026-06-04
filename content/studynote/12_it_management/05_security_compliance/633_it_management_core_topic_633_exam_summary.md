+++
title = "633. IT 경영 관리 핵심 토픽 633번 시험 요약 (IT Management Core Topic 633 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(IT Management)는 COBIT 2019, ITIL 4, ISO 38500 등 글로벌 거버넌스 프레임워크를 기반으로, IT 전략(Strategy) → 아키텍처(Architecture) → 운영(Operation) → 성과평가(Performance) → 혁신(Innovation)으로 이어지는 5단계 Value Chain을 통해 기업 가치를 극대화하는 경영 활동임.
> 2. **가치**: IT 투자 대비 수익률(ROIT) 평균 25~40% 향상, IT 서비스 가용성 99.99% SLA 달성, 정보보안 사고 대응시간(MTTR) 60% 단축, 디지털 전환 성공률 70% 이상 확보가 가능하며, EBITDA 대비 IT 비용 비율을 업종 벤치마크(금융 8.2%, 제조 4.5%, 유통 3.1%) 수준으로 최적화.
> 3. **판단 포인트**: Build vs. Buy vs. Cloud vs. SaaS 의사결정, 중앙집권형(Centralized) vs. 페데레이션형(Federated) IT 운영 모델 선택, Agile-DevOps-Waterfall 하이브리드 방법론 적용, 그리고 Zero Trust 보안 모델과 Legacy 시스템의 단계적 모더니제이션 전략이 핵심 Trade-off.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 1980~2000년대까지 "비용 센터(Cost Center)"로 인식되어 왔으나, 4차 산업혁명(AI, BigData, Cloud, IoT, Blockchain, Metaverse) 시대에는 "전략적 가치 창출 중심(Value Driver)"으로 그 패러다임이 전환되었습니다. Gartner 보고에 따르면 2026년 글로벌 IT 지출 규모는 5.1조 USD에 달하며, 이 중 70% 이상이 단순 운영이 아닌 디지털 트랜스포메이션(DX) 및 Innovation에 투입됩니다. 특히 COVID-19 이후 Remote Work, 비대면 서비스, 초연결(Hyper-connected) 비즈니스 환경이 일반화되면서, IT는 더 이상 Back-office 지원 기능이 아니라 **Core Business Engine**으로 기능합니다.

```text
┌────────────────────────────────────────────────────────────────────┐
│         IT 경영 관리 5단계 Value Chain (ITIL/COBIT 기반)            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  [1] IT 전략 기획        [2] IT 거버넌스      [3] IT 아키텍처       │
│   ┌──────────┐          ┌──────────┐        ┌──────────┐         │
│   │비전/미션 │─────────▶│COBIT2019 │───────▶│EA Framework│        │
│   │BSC/KPI  │          │ISO 38500 │        │TOGAF 10  │        │
│   │Portfolio│          │IT 정책/통제│        │Reference │        │
│   └──────────┘          └──────────┘        │Model    │        │
│        │                                        └──────────┘         │
│        ▼                                            │                │
│  [4] IT 운영 및 서비스    [5] IT 혁신 및 성과    [반복/환류]            │
│   ┌──────────┐          ┌──────────┐                                │
│   │ITIL 4 SVS│─────────▶│KPIs/BSC │──┐                             │
│   │DevOps/Agile│        │Innovation │  │                             │
│   │SLA/SLM  │          │AI/Automation│  │                             │
│   └──────────┘          └──────────┘                                │
│        │                       │                                      │
│        └───────────────────────┴──▶ [Board / Executive Report]      │
└────────────────────────────────────────────────────────────────────┘
```

**Legacy Paradigm(전통)** vs **Modern Paradigm(현대)** 비교:
- **비용관점(1980s)**: CapEx 중심의 일회성 대형 프로젝트 → "시스템이 1년에 한 번도 장애가 없으면 성공" → ROI 측정 불가
- **가치관점(2020s)**: OpEx 기반의 지속적 가치 창출(Continuous Value Delivery) → "매주 Release 가능한 속도와 사용자 만족도(CSAT/NPS)가 핵심 KPI" → Real-time ROI Dashboard

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 계기판과 운전대입니다. 엔진(기술)만 좋다고 좋은 차가 아니듯, COBIT(방향타), KPI(속도계), SLA(연비계), Risk Dashboard(경고등) 등 4대 계기판이 통합적으로 작동해야 기업이 목적지(경영 목표)에 안전하게 도달할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 크게 **4개의 레이어(Governance-Architecture-Operation-Innovation)**와 **3개의 횡단 통제(Security-Compliance-Performance)**로 구성됩니다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ [Layer 1] IT 거버넌스 (Governance) - "무엇을(What) 왜(Why) 할 것인가"  │
│  ┌────────────┬────────────┬────────────┬──────────────┐            │
│  │COBIT 2019  │ISO 38500   │ISO 27001   │ISMS-P 인증   │            │
│  │40 Governance│6 Principles │114 Annex A  │국내 법적요건 │            │
│  │Objectives   │(책임/전략/ │Controls    │PIPC 통지/이용 │            │
│  │(EGM/EDM)    │획득/성능/  │(암호화/접근 │정보통신망법   │            │
│  │             │준수/인간)  │통제/물리)   │전자금융거래법 │            │
│  └────────────┴────────────┴────────────┴──────────────┘            │
├──────────────────────────────────────────────────────────────────────┤
│ [Layer 2] IT 아키텍처 (Architecture) - "어떻게(How) 만들 것인가"      │
│  ┌────────────┬────────────┬────────────┬──────────────┐            │
│  │TOGAF 10    │Zachman     │FEAF/DODAF  │ArchiMate 3.2 │            │
│  │ADM Cycle   │6W1H×6 셀  │전술/운용뷰  │Business/App  │            │
│  │(A-H단계)   │Planner/    │SV-1~SV-10  │/Tech Layer   │            │
│  │             │Owner/Builder│           │              │            │
│  └────────────┴────────────┴────────────┴──────────────┘            │
├──────────────────────────────────────────────────────────────────────┤
│ [Layer 3] IT 운영 (Operation) - "일상적으로 어떻게 굴릴 것인가"        │
│  ┌────────────┬────────────┬────────────┬──────────────┐            │
│  │ITIL 4 SVS  │DevOps/GitOps│Observability│FinOps/AIOps │            │
│  │34 Practices│CI/CD/CT    │(Logs/Metrics│Cloud비용최적화│            │
│  │Service Value│Pipeline   │Traces)     │자동복구/예측  │            │
│  │Chain       │SRE/SLI/SLO│Prometheus  │              │            │
│  └────────────┴────────────┴────────────┴──────────────┘            │
├──────────────────────────────────────────────────────────────────────┤
│ [Layer 4] IT 혁신 (Innovation) - "내일을 어떻게 바꿀 것인가"            │
│  ┌────────────┬────────────┬────────────┬──────────────┐            │
│  │AI/MLOps    │DataOps     │Low-Code    │Edge/Quantum  │            │
│  │LLM/RAG     │Lakehouse   │RPA/IPA     │Web3/Blockchain│            │
│  │Responsible │Data Quality │Citizen Dev │Digital Twin  │            │
│  │AI(윤리/편향│Cataloging   │Platform    │              │            │
│  └────────────┴────────────┴────────────┴──────────────┘            │
└──────────────────────────────────────────────────────────────────────┘
            ▲                                                            │
            │ 횡단 통제(Cross-cutting Controls)                          │
   ┌────────┴────────┬──────────────┬──────────────┐                    │
   │Security: Zero   │Compliance:   │Performance:  │                    │
   │Trust/NIST CSF  │GDPR/PIPA/   │BSC Balanced   │                    │
   │/SASE/SBOM     │PCI-DSSe     │Scorecard/     │                    │
   │                │SOX 404      │OKR/KPI Tree   │                    │
   └─────────────────┴──────────────┴──────────────┘                    │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스/관리 체계 | 40개의 Governance/Management Objectives를 EDM(Evaluate-Direct-Monitor) + APO/BAI/DSS/MEA 4개 도메인으로 구성. Design Factors 11개로 조직 맞춤 설계. |
| **ITIL 4** | IT 서비스 운영 체계 | 34개 Service Management Practices와 3개 General/Service/Technical Management Practices. Service Value System(SVS) 통해 Opportunity/Demand → Value 변환. |
| **TOGAF 10** | EA 방법론 | ADM(Architecture Development Method) 8단계 A→H Cycle. Preliminary Phase(비전), A(비전아키텍처), B~D(비즈니스/데이터/애플리케이션/기술), E(기회/해결책), F(마이그레이션), G(거버넌스), H(아키텍처 변경). |
| **BSC (Balanced Scorecard)** | 전략 성과 측정 | 4관점(재무/고객/내부프로세스/학습성장) × 4단계(목표→측정지표→목표치→액션플랜). Kaplan-Norton 모형, Strategy Map으로 인과관계 시각화. |
| **FinOps** | 클라우드 비용 최적화 | Inform(가시성) → Optimize(최적화) → Operate(자동화) 3단계 성숙도. Reserved Instance/Savings Plan(최대 72% 절감) vs Spot Instance(최대 90% 절감) 조합. |

**핵심 공식 및 의사결정 모델**:
- **TCO(Total Cost of Ownership)** = CAPEX(HW/SW/License) + OPEX(인건비/전력/관리/교육/다운타임) × 5년
- **NPV(순현재가치)** = Σ [CF_t / (1+r)^t] - I₀ (r:할인율, 통상 8~12%)
- **ROIT(Return on IT Investment)** = (IT기여 이익 / IT총투자액) × 100, 일반적으로 5배 이상 시 성공
- **IT Portfolio 균형도** = (Run-the-Business) : (Grow-the-Business) : (Transform-the-Business) = 70 : 20 : 10 (Gartner 권고)
- **Build vs. Buy 결정 매트릭스**: 핵심경쟁력(Core) → Build, 차별화(Strategic) → Build or Configure-to-Order, 비핵심(Commodity) → Buy/SaaS

- **📢 섹션 요약 비유**: IT 경영 관리는 도시계획과 같습니다. 토지이용계획(EA), 도로/상하수도(IT인프라), 소방서(Security), 시청(Governance), 시민서비스(End-User Service)가 따로 노는 것이 아니라 종합 계획(Integrated Plan) 아래에 일관성 있게 운영되어야 "살고 싶은 도시(Agile Enterprise)"가 만들어집니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스/관리 표준 | IT 서비스 운영 표준 | IT 의사결정 거버넌스 국제표준 | 프로세스 성숙도 평가 |
| **주관기관** | ISACA | Axelos(PeopleCert) | ISO/IEC | ISACA/CMMI Institute |
| **관점** | Governance(What/Why) | Service Operation(How) | Board/C-Level(책임) | Process Maturity(5 Level) |
| **구조** | 40 Objectives, 5 Domains | 34 Practices, 4D Model | 6 Principles | 5 Maturity Level, 20 Process Area |
| **적용범위** | 전사 IT(Enterprise-wide) | IT 서비스팀(Operating) | 이사회/경영진(Boardroom) | 개발/운영 조직 |
| **측정방법** | Process Capability(0-5) | 4D Model(Diagnose) | Maturity Model(R-3) | SCAMPI 평가 |
| **인증제도** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | 인증 없음(표준) | CMMI v2.0 Maturity Level 1~5 |
| **연계성** | ITIL/ISO27001/PMI와 매핑 | COBIT의 DSS 영역 보완 | COBIT 상위거버넌스 원칙 | DevOps/Agile 통합 |
| **도입비용** | 중(컨설팅+인증) | 중(연간라이선스) | 저(원칙 위주) | 고(SCAMPI 50~200M) |
| **주 활용** | 금융/공공 대기업 | MSP/IDC/통신사 | 글로벌 MNC Board | SW공학 조직 |

**다른 시스템과의 통합(Integration Architecture)**:
- **ERP(Oracle/SAP)**: COBIT의 B
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 633 / 800

← **이전**: [632. IT 경영 관리 핵심 토픽 632번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/632_it_management_core_topic_632_exam_summary/)
**다음**: [634. IT 경영 관리 핵심 토픽 634번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/634_it_management_core_topic_634_exam_summary/) →

---
