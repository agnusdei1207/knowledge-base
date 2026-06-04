+++
title = "485. IT 경영 관리 핵심 토픽 485번 시험 요약 (IT Management Core Topic 485 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(IT Management)는 COBIT 2019 거버넌스 체계와 ITIL 4 서비스 가치 시스템(SVS)을 통합해 **전략-설계-구축-운영-평가**의闭环(Closed-loop) 가치 사슬을 구축하며, 이는 EA(Enterprise Architecture)와 PMO의 연계로 실현된다.
> 2. **가치**: McKinsey 보고 기준 디지털 전환 성공 기업은 매출 성장률 23%p, 영업이익률 5%p 우위를 보이며, IT-Portfolio ROI 최적화 시 TCO 평균 28%, Time-to-Market 40% 단축이 가능하다.
> 3. **판단 포인트**: Build vs Buy, On-Premise vs Cloud, Waterfall vs Agile, Centralized vs Federated 거버넌스의 4대 트레이드오프에서 **비용-속도-통제-혁신**의 균형점을 찾아야 하며, 기술사적 판단의 핵심은 "기술 도입"이 아닌 "변화 관리(Change Management)"와 "가치 실현(Value Realization)"이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 IT 경영 관리 영역은 4차 산업혁명(Digital Transformation, AI, Cloud, Data) 시대의 핵심 의사결정 프레임워크를 다룬다. 과거 1990년대 IT는 **Cost Center**(비용 부서)로 인식되었으나, 2010년대 후반부터 Gartner의 **Bimodal IT**(Mode 1: 안정성/예측가능성, Mode 2: 민첩성/실험)를 거쳐 2024년 현재는 **Digital Business Platform**으로서의 역할로 진화했다.

기술사 시험에서 빈출되는 핵심 이슈는 다음과 같다:
- **전략적 정렬(Strategic Alignment)**: Henderson & Venkatraman의 **SAM(Strategic Alignment Model)**에서 биз니스 전략 ↔ IT 전략 ↔ 조직/프로세스 ↔ IT 인프라의 4P(Perspective) 정렬
- **가치 측정(Value Measurement)**: 전통 ROI/NPV에서 **VOI(Value of Investment)**, **ROO(Return on Opportunity)**로 확장
- **거버넌스**: COSO ERM, ISO 38500, **COBIT 2019**의 40개 Governance/Management Objectives
- **포트폴리오 관리**: 프로젝트-프로그램-포트폴리오의 3계층 구조(PPM)
- **변화 관리**: Kotter의 8단계 모델, ADKAR 모델

```text
┌─────────────────────────────────────────────────────────────────┐
│                  IT 경영 관리 5단계 가치 사슬                     │
│         (Strategic Value Chain for IT Management)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1.전략]        [2.기획]         [3.구축]        [4.운영]       │
│  Biz Strategy ──▶ IT Strategy ──▶ EA Design ──▶ Service Ops    │
│   │                │               │              │            │
│   ▼                ▼               ▼              ▼            │
│  BSC/KPI       Portfolio      TOGAF ADM       ITIL 4 SVS        │
│  SWOT/PEST     Prioritization Zachman         SIAM              │
│                FinOps                                                │
│                                              │            │
│                          [5.평가]◀──────────┘            │
│                          Governance & Audit                          │
│                          COBIT 2019, ISO 38500                       │
│                          Balanced Scorecard                          │
│                                                                 │
│  ◀─── 피드백 루프 (Continuous Improvement / Kaizen) ────▶          │
└─────────────────────────────────────────────────────────────────┘
```

기존 패러다임(2000년대)과 새로운 패러다임(2020년대) 비교:
- **2000년대**: "IT for Cost Reduction" → BPO/Offshoring, ERP(MM/FI/HR), 데이터센터 통합
- **2010년대**: "IT for Efficiency" → Cloud Migration, SaaS 도입, Agile/DevOps
- **2020년대**: "IT for Business Innovation" → AI/ML, Hyperautomation, Data Mesh, 생성형 AI, Cloud-Native, Edge Computing

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 바이올린(개발팀), 첼로(운영팀), 트럼펫(영업), 팀파니(경영진)라는 다양한 악기(부서)가 각자 다른 음(목표)을 연주할 때, 지휘자(CDO/CIO)는 **악보(전략)**, **파트 배정(거버넌스)**, **음정 조율(EA)**, **공연 평가(BSC)**를 통해 하나의 아름다운 협주곡(디지털 비즈니스)을 만들어낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 표준 아키텍처는 **COBIT 2019**의 체계와 **TOGAF ADM**(Architecture Development Method)을 결합한 형태가 일반적이다. COBIT의 5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess)이 40개 관리 목표로 분해되며, TOGAF의 8단계 ADM 사이클(Phase A: Architecture Vision ~ Phase H: Architecture Change Management)과 상호 매핑된다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│             통합 IT 경영 관리 아키텍처 (Reference Model)              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─── Strategic Layer (전략 계층) ────────────────────────┐          │
│  │  • 비즈니스 전략    • IT 거버넌스 위원회 (ITGC)            │          │
│  │  • 디지털 로드맵    • 투자 우선순위(FinOps/Business Case)  │          │
│  └────────────────────────────────────────────────────┘          │
│                          ↕ 정렬(Alignment)                              │
│  ┌─── Planning Layer (기획 계층) ─────────────────────────┐          │
│  │  • 포트폴리오 관리(PPM)  • PMO(3-tier: Portfolio/Program)│       │
│  │  • 자원 배분(Budgeting)  • 위험 관리(Risk Register)     │          │
│  └────────────────────────────────────────────────────┘          │
│                          ↕ 변환(Transformation)                          │
│  ┌─── Execution Layer (수행 계층) ────────────────────────┐          │
│  │  • EA 구현(TOGAF ADM)  • Agile/Scrum/SAFe              │       │
│  │  • DevOps 파이프라인    • SRE 관행(Error Budget)         │          │
│  └────────────────────────────────────────────────────┘          │
│                          ↕ 제공(Delivery)                                │
│  ┌─── Operations Layer (운영 계층) ──────────────────────┐          │
│  │  • ITIL 4 SVS(34 Practices)                            │       │
│  │  • AIOps/관측가능성(Observability: M/E/L/T)             │       │
│  │  • FinOps(클라우드 비용 최적화)                          │       │
│  └────────────────────────────────────────────────────┘          │
│                          ↕ 측정(Measurement)                            │
│  ┌─── Governance Layer (거버넌스 계층) ──────────────────────┐      │
│  │  • COBIT 2019(40 Goals)  • ISO 38500                   │       │
│  │  • BSC 4관점(Financial/Customer/Process/Learning)        │       │
│  │  • 내부 통제(감사/컴플라이언스/SOX/K-ISMS)                  │       │
│  └────────────────────────────────────────────────────┘          │
│                                                                      │
│  ※ 모든 계층은 PDCA(Deming Cycle) + OODA Loop로 연결                    │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CDO/CIO/CISO 거버넌스 위원회** | 의사결정 최고 권위 | 분기별 ITGC 운영, RACI 매트릭스 활용, 의사결정 5단계(식별-분석-평가-결정-실행) |
| **EA(Enterprise Architecture)** | 비즈니스-IT 정렬 | TOGAF ADM 8단계, Zachman 6×6 매트릭스, ArchiMate 3.2 언어, FEAF/DODAF 연동 |
| **PPM 도구 (Planview, ServiceNow SPM)** | 프로젝트-프로그램-포트폴리오 통합 관리 | 자원 100% 배분, What-if 시뮬레이션, Prioritization Matrix(가치-위험-비용) |
| **Agile/DevOps 플랫폼 (Jira, GitLab, Azure DevOps)** | 민첩한 구축-배포-운영 | SAFe 6.0(ART/Pi Planning), DORA 4 Metrics(배포 빈도/리드타임/MTTR/변경실패율), GitOps/ArgoCD |
| **FinOps 플랫폼 (Apptio, CloudHealth, Kubecost)** | 클라우드 비용 최적화 | Inform-Optimize-Operate 3단계, RI/SP(예약 인스턴스/Savings Plans) 활용률, Showback/Chargeback |
| **ITSM/관측가능성 (ServiceNow, Datadog, Splunk)** | 서비스 운영 및 SRE | ITIL 4 34개 Practice(중심: Incident/Problem/Change/Service Desk), SLI/SLO/SLA, MTTR/MTTD/MTBF |

**핵심 공식 및 프레임워크 심화**:

1. **SAM (Strategic Alignment Model) 정렬도 측정**:
   `Alignment Index = Σ(wᵢ × |Bᵢ - Iᵢ|)⁻¹`
   - Bᵢ: 비즈니스 전략 점수, Iᵢ: IT 전략 점수, wᵢ: 가중치(0~1)

2. **NPV(순현재가치)와 TCO(총소유비용)**:
   `NPV = Σ[CFₜ/(1+r)ᵗ] - C₀`
   `TCO = 직접비용 + 간접비용 + Hidden Cost(Shadow IT, 통합 비용)`

3. **DORA 4대 메트릭 (DevOps 성능 지표)**:
   - **Deployment Frequency**: Elite(일간+) vs Low(월간 이하)
   - **Lead Time for Changes**: Elite(< 1일) vs Low(1~6개월)
   - **Change Failure Rate**: Elite(0~15%) vs Low(46~60%)
   - **MTTR(Mean Time To Recovery)**: Elite(< 1시간) vs Low(1주~1개월)

4. **COBIT 2019 Cascade of Goals**:
   Stakeholder Needs → Enterprise Goals → Alignment Goals → Management Goals → Component(Process/Structure/People/Skills/Information)

- **📢 섹션 요약 비유**: IT 경영 관리의 아키텍처는 **신체 기관**과 같다. **뇌**(거버넌스 위원회)가 전략적 결정을 내리고, **심장**(EA)이 조직 전체에 정렬된 비전과 표준을 펌프질하며, **근육**(DevOps/Agile 팀)이 실제 움직임을 만들고, **소화계**(운영/관측)가 자원을 흡수·배분하며, **신경계**(BSC/COBIT)가 모든 기관의 상태를 실시간 피드백한다. 어느 하나라도 멈추면 **디지털 비즈니스**라는 신체 전체가 쓰러진다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 자주 혼동되는 개념들의 정밀 비교는 기술사 시험의 단골 문제이다. 특히 **거버넌스 vs 관리**, **EA vs 시스템 아키텍처**, **프로젝트 vs 프로그램 vs 포트폴리오**, **ITIL vs COBIT**의 구분이 핵심이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **TOGAF 10** |
| :--- | :--- | :--- | :--- |
| **목적** | 거버넌스 및 관리 프레임워크 | IT 서비스 관리(ITSM) 모범 사례 | 기업 아키텍처(EA) 개발 방법론 |
| **대상** | 전체 IT(거버넌스+관리) | 서비스 운영 및 가치 실현 | 비즈니스-IT 아키텍처 정렬 |
| **핵심 구조** | 40 Governance/Management Objectives, 5 Domains | 34 Practices, 4 Dimensions, SVS | ADM 8 Phases(A~H), Architecture Repository |
| **주 사용자** | 이사회, CISO, 감사인, CIO | 서비스 매니저, 운영팀, SRE | EA 아키텍트, 수석 설계자 |
| **강점** | 컴플라이언스/통제, Risk 관리 | 고객 가치, 서비스 품질 | 정합성 있는 아키텍처 산출물 |
| **약점** | 구체적 실행 절차 부족 | 거버넌스 측면 약함 | 서비스 운영 연계 미흡 |
| **연동** | ISO 27001, NIST CSF, SOX | DevOps, SRE, AIOps | ArchiMate, BPMN, UML |
| **산출물** | RACI, Maturity Model, Cascade Goals | Value Stream, Practice Guide | ADM Deliverables, Architecture Views |
| **측정** | Process Capability(0~5), Goal Cascade | SLI/SLO, CSI Model | ADM Iteration, Architecture Maturity |
| **시장 점유** | 대기업/금융/공공 | 모든 규모/서비스 중심 | 글로벌 대기업/정부 |

**프로젝트-프로그램-포트폴리오(PPM) 3계층 비교**:

| 구분 | 프로젝트(Project) | 프로그램(Program) | 포트폴리오(Portfolio) |
| :--- | :--- | :--- | :--- |
| **범위** | 단일 결과물 | 관련 프로젝트 묶음 | 전략적 투자 전체 |
| **기간** | 수개월~1년 | 1~3년 | 지속적(연간 단위) |
| **목표** | Scope/Cost/Quality | Benefit Realization | Strategic Value Maximization |
| **관리자** | PM(Project Manager) | PgM(Program Manager) | PfM(Portfolio Manager) |
| **예시** | ERP 도입 프로젝트 | 디지털 트랜스포메이션 프로그램 | 전사 IT 투자 50개 프로젝트 |
| **핵심 KPI** | SPI/CPI(일정/원가) | Benefits Realization Index | Portfolio ROI, NPV 총합 |

**DevOps vs SRE vs Agile vs ITIL 비교**:

| 구분 | Agile | DevOps | SRE | ITIL 4 |
| :--- | :--- | :--- | :--- | :--- |
| **출신** | Software Dev(2001) | 개발+운영 융합(2009) | Google(2003) | UK Gov(1980s, ITIL 4: 2019) |
| **핵심 가치** | 협업, 반응, 변화 | CALMS(Culture/Automation/Lean/Measurement/Sharing) | Toil 제거, Error Budget | Service Value System |
| **측정** | Velocity, Burn-down | DORA 4 Metrics | SLI/SLO, Error Budget | Customer Satisfaction, CSI |
| **적용 범위** | 팀/제품 | 팀~조직 | 운영/플랫폼 | 전사 서비스 |

**연계/통합 아키텍처**:
- **상위**: ISO 38500(거버넌스 원칙: 책임/전략/수행/적합성/규율/인간행위) + 기업 거버넌스(COSO ERM)
- **중위**: COBIT 2019 + ISO 27001 + NIST CSF + PCI-DSS(산업별)
- **실행**: TOGAF(설계) + ITIL 4(운영) + DevOps(배포) + SAFe(확장)
- **측정**: BSC + OKR + KPI/KRI
- **지원**: ISO 20000(SMS), CMMI(SW 품질), ISO 33000(프로세스 평가)

- **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 485 / 800

← **이전**: [484. IT 경영 관리 핵심 토픽 484번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/484_it_management_core_topic_484_exam_summary/)
**다음**: [486. IT 경영 관리 핵심 토픽 486번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/486_it_management_core_topic_486_exam_summary/) →

---
