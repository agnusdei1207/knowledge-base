---
title: "598. IT 경영 관리 핵심 토픽 598번 시험 요약 (IT Management Core Topic 598 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Governance·Strategy·Portfolio·Service·Risk 통합)는 **COBIT 2019(34개 governance/process objective) × ITIL 4(SVS 34 practices) × ISO/IEC 38500(6 principles) × PMBOK 7(8 performance domains)**를 4-Layer Control Model(전략-전술-운영-감시)로 융합하여 **"Value Realization(EVT×BR×RR / [Cost+Risk])"** 공식을 기반으로 IT 투자를 비즈니스 성과로 정량 전환하는 경영 체계이다.
> 2. **가치**: McKinsey Digital(2023) 기준 COBIT+ITIL 통합 적용 기업은 **IT 비용 대비 비즈니스 성과 23% 향상, 프로젝트 실패율 38%->9% 감소, MTTR 62% 단축, 감사 지적사항 71% 감소, TCO 5년 누적 34% 절감** 효과를 거두며, 디지털 트랜스포메이션(DX) 성공률(Industry 평균 30%)을 **67%까지 제고**시킨다.
> 3. **판단 포인트**: 거버넌스-관리(Governance vs Management) 경계, **RACI matrix**(Responsible/Accountable/Consulted/Informed) 명확화, **3 Lines of Defense(비즈니스·위험관리·내부감사)** 모델 적용, Agile-DevOps-Cloud 전환 시 **Dual Operating System(기존 체계 + 디지털 코어)** 설계, 그리고 측정 가능한 **KPI Tree(CSF->KPI->KGI)** 구축 여부가成败를 가른다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 운영(CIO 중심 비용 센터, CapEx 위주, 사일로 부서, Waterfall)은 4차 산업혁명(AI/Cloud/Data/Bio/IoT) 환경에서 비즈니스 속도·규모·복잡성 증가에 따른 **3대 패러다임 붕괴**를 겪고 있다:

1. **기술-비즈니스 간 시간차 붕괴**: 평균 36개월->9개월(Forrester, 2024)
2. **데이터 규모·속도 붕괴**: Zettabyte 시대(전 세계 데이터 2025년 175ZB), 실시간 의사결정 요구
3. **규제·보안 환경 붕괴**: GDPR(€20M/4%), KR ISO 27001/27701, DORA, ESG 공시 의무화

이에 IT 경영 관리는 단순 IT 운영을 넘어 **"전략적 비즈니스 파트너"**로 진화해야 하며, 이는 **ISO/IEC 38500(거버넌스 표준)**, **COBIT 2019(관리 목표 프레임워크)**, **ITIL 4(서비스 가치 체계)**, **TOGAF 10(EA 방법론)**, **PMBOK 7(프로젝트/프로그램/포트폴리오)** 5대 프레임워크의 통합적 적용을 요구한다. 정보관리기술사 관점에서는 **"IT가 비즈니스에 정량적 가치를 창출하는가"**를 입증할 수 있는 거버넌스 체계를 설계·감리하는 능력이 핵심 평가 포인트다.

```text
+----------------------------------------------------------------------+
|                  IT 경영 관리 4-Layer 통합 아키텍처                   |
+----------------------------------------------------------------------+
|                                                                      |
|  +-------------------------------------------------------------+    |
|  |  Layer 1: 전략 거버넌스 (Strategy & Governance)              |    |
|  |  • ISO/IEC 38500 6원칙  • Board/CDO/Steering Committee     |    |
|  |  • IT Strategy Map  • Value Realization Framework           |    |
|  +----------------------+--------------------------------------+    |
|                         | Cascading                                 |
|  +----------------------v--------------------------------------+    |
|  |  Layer 2: 전술 기획 (Tactical Portfolio & EA)                |    |
|  |  • COBIT 2019 (40 Governance/Management Objectives)         |    |
|  |  • TOGAF ADM (Preliminary->Vision->Business->IS->Tech->...)     |    |
|  |  • Portfolio Prioritization (NPV/IRR/ROIC/Strategic Fit)    |    |
|  +----------------------+--------------------------------------+    |
|                         | Allocation                                |
|  +----------------------v--------------------------------------+    |
|  |  Layer 3: 운영 실행 (Service & Project Delivery)             |    |
|  |  • ITIL 4 SVS (Service Value System, 34 Practices)           |    |
|  |  • PMBOK 7 (8 Performance Domains)                          |    |
|  |  • DevOps/Agile/SRE/IT4IT                                   |    |
|  +----------------------+--------------------------------------+    |
|                         | Monitoring                                |
|  +----------------------v--------------------------------------+    |
|  |  Layer 4: 감시·통제 (Assurance & Risk)                       |    |
|  |  • 3 Lines of Defense  • Internal Audit  • GRC               |    |
|  |  • KPI/KGI/SLA Reporting  • Continuous Improvement           |    |
|  +-------------------------------------------------------------+    |
|                                                                      |
|  Cross-cutting: ISO 27001(보안) · ISO 20000(서비스) · ISO 31000(리스크)|
+----------------------------------------------------------------------+
```

기존(As-Is)인 **"CIO 직할 IT 부서, 연간 CapEx 예산 중심, 개별 시스템 단위 운영, 사후 감리"** 모델은 **To-Be**인 **"BizDevOps + Value Steward + 실증 거버넌스 + 연속적 의사결정"** 모델로 전환되어야 하며, 이때 핵심은 **"측정 가능성(Measurability) × 정당성(Justification) × 지속가능성(Sustainability)"** 의 3축 균형이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 도시계획 + 교통관제 + 소방서 + 감사관"**을 한 시스템으로 묶은 것과 같다. 도시계획(전략), 교통관제(운영), 소방서(리스크), 감사관(컴플라이언스) 어느 하나라도 어긋나면 도시 전체가 마비되는 것처럼, IT의 4계층이 동시에 조화롭게 돌아가야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ISO/IEC 38500 IT 거버넌스 — 6대 원칙 프레임워크

ISO/IEC 38500:2015는 **"Direct, Monitor, Evaluate"** 3단계 모델과 **6 Principles(책임, 전략, 획득, 성능, 적합성, 인간행동)** 을 제시하며, 이사회·경영진이 IT 의사결정의 5가지 관점(현재·미래·계획·최적·실행)을 지속적으로 검토하도록 요구한다.

### 2. COBIT 2019 — 40 Governance/Management Objectives

**EDM(5) -> Align/Plan/Organize(14) -> Build/Acquire/Implement(11) -> Deliver/Service/Support(6) -> Monitor/Evaluate/Assess(4)** 의 5개 도메인, 40개 목표 체계. 핵심은 **"Goal Cascade(Enterprise Goal->Alignment Goal->Process Goal)"** 로 비-IT KPI(S/N/P 등 13개)와 IT KPI를 자동 매핑하는 메커니즘이다.

### 3. ITIL 4 — Service Value System (SVS)

**Opportunity/Demand -> Value -> Value Chain(Plan/Engage/Design/Obtain/Build/Deliver/Support) -> 34 Practices(General, Service, Technical Management)** 구조. 핵심은 **"SLA -> OLA -> UC(Service Catalogue)"** 의 3단 서비스 계약 체계와 **"Incident->Problem->Known Error->Change"** 의 ITIL Service Operation Life-cycle이다.

### 4. Value Realization Formula (가치 실현 공식)

```
Value = (Enterprise Value × Benefits Realization × Risk Reduction)
        -------------------------------------------------
              (Total Cost of Ownership + Risk Cost)
```

이 공식을 **연속 측정(Continuous Measurement)** 하기 위해 **CSF(Critical Success Factor) -> KPI(Key Performance Indicator) -> KGI(Key Goal Indicator)** 의 3단계 인과 사슬을 설계한다. 예: "고객 이탈률 5% 감소(KGI)" <- "모바일 앱 가용성 99.95%(KPI)" <- "MSA 전환 및 Active-Active DR 구성(CSF)".

```text
+----------------------------------------------------------------------+
|         IT 가치 실현을 위한 KPI Tree & 인과관계 매핑 예시             |
+----------------------------------------------------------------------+
|                                                                      |
|   [CSF] Strategic ---------------------------------------------+    |
|      | DX 가속화 & 글로벌 SaaS 전환                              |    |
|      v                                                          |    |
|   [KPI-1] Time-to-Market 18개월->6개월                          |    |
|   [KPI-2] 신규 SaaS 통합 MTTR < 2h                              |    |
|   [KPI-3] Cloud TCO YoY -15%                                   |    |
|      |                                                          |    |
|      v                                                          |    |
|   [KGI] 매출신장률 +12%  | 고객이탈률 -5% | EBITDA +3%p        |    |
|      ^                                                          |    |
|      |                                                          |    |
|   [CSF] Operational --------------------------------------------+    |
|      |                                                            |
|      +-- Incident MTTR < 30min  (L1)                              |
|      +-- Change Success Rate > 98%                                |
|      +-- Major Incident ≤ 1/분기                                  |
|      +-- Problem RCA 100% (5-Whys + Fishbone)                    |
|                                                                      |
|   [CSF] Compliance/Security                                        |
|      +-- KR ISO 27001 인증 유지                                    |
|      +-- 취약점 Critical 0건, High ≤ 3건                           |
|      +-- 개인정보 영향평가 100% 사전 이행                          |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Board / Steering Committee** | 거버넌스 의사결정 최고 기구 | 6원칙 책임, 분기별 Review, 화이트페이퍼 기반 의사결정, **RACI Matrix** 명문화 |
| **CDO/CIO + PMO** | 전략-전술 연결, 프로젝트 우선순위화 | **COBIT EDM(01~05)** 수행, **MoSCoW/AHP/Weighted Scoring** 으로 포트폴리오 우선순위 산정, **Stage-Gate Process**(Idea->Feasibility->Planning->Delivery->Closure) 운영 |
| **EA Team (TOGAF ADM)** | 아키텍처 표준·로드맵 | **Preliminary->A(Architecture Vision)->B(Business)->C(IS)->D(Technology)->E(Opportunities)->F(Migration)->G(Implementation)->H(Change Management)** 의 9단계 사이클, **ArchiMate 3.2** 표기 |
| **Service Operation Center (SOC/NOC)** | 일일 운영·모니터링 | **ITIL 4 34 Practices** 중 Incident/Problem/Change/Service Desk/Continuity 운영, **ServiceNow/Jira Service Management** 같은 ITSM Tool로 워크플로우 자동화 |
| **GRC Platform** | 정책·리스크·컴플라이언스 통합 | **3 Lines of Defense** 매핑, ISO 27001 Annex A 93 통제 + ISO 31000 리스크 레지스터 통합, **RSA Archer / ServiceNow GRC / SAP GRC** 활용 |
| **Continuous Improvement (CSI)** | 측정·학습·개선 | **Lean/DMAIC, PDCA, NPS, KPT 회고**, SRI(Service Request Index)/SPI/CSI 등록 및 추적 |
| **Assurance Function** | 내부감사·제3자 검증 | **ISAE 3402 / SOC 2 Type II**, **GDPR/ISMS-P/PCI-DSS** 인증, **통제 테스트(Control Test)** 6개월 주기 |

### 5. Risk Management 심화 (ISO 31000 + NIST CSF 2.0)

**Risk = Threat × Vulnerability × Asset Value / Control Effectiveness**. 리스크 평가 시 **Qualitative(매트릭스) + Quantitative(FAIR/ALE)** 하이브리드 접근을 권장한다. **NIST CSF 2.0(2024)** 의 **6 Function(Govern, Identify, Protect, Detect, Respond, Recover)** + **Tier(1~4)** 모델과 매핑한다.

### 6. IT Portfolio & Investment Management

**"Run(50~60%) / Grow(30~35%) / Transform(10~15%)"** 의 IT 예산 배분(Jeff Bezos 2-Pizza Team 원칙 변형)이 글로벌 표준이며, **NPV(순현재가치), IRR(내부수익률), Payback Period, ROIC, Strategic Fit Score, Risk-adjusted Return(RAROC)** 의 6대 지표로 우선순위화한다.

- **📢 섹션 요약 비유**: IT 경영 관리 4계층은 마치 **"오케스트라 지휘자(Board) -> 악장(PMO) -> 연주자(Service Ops) -> 비평가(Audit)"**의 관계와 같다. 지휘자가 명확한 악보(전략)를 주지 않으면, 아무리 좋은 연주자도 엇나가고, 비평가는 객관적·독립적이어야만 신뢰할 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 목표 | 서비스 가치 창출 | 이사회 수준 IT 거버넌스 | 프로젝트/프로그램 관리 | 기업 아키텍처 |
| **계층 위치** | 전술·관리(Tactical) | 운영(Operational) | 전략·거버넌스(Strategic) | 전술(Tactical) | 전술·설계(Tactical/Design) |
| **핵심 산출물** | 40 Governance Objectives | 34 Practices, SVS | 6 Principles + 5 Tasks | 8 Performance Domains | ADM Cycle, ArchiMate 모델 |
| **측정 중심** | Maturity Level(0~5) / Process Capability | SLA / SLO / Error Budget | Conformance + Performance | Project KPIs(SP/PI/CV/SV) | Architecture Roadmap |
| **통합 인터페이스** | **APO(Align-Plan-Org)** 모듈 | **Service Value Chain** | **Direct/Monitor/Evaluate** | **Plan/Execution/Work** | **Architecture Repository** |
| **적합 조직 단계** | 중·대규모, 규격 준수 산업 | 서비스 중심 기업 | 대기업·공공기관 | 프로젝트 비중 30%^ | 디지털 전환 추진 기업 |
| **결합 시너지** | **지표 정의** | **실행 운영** | **원칙·책무** | **일정·범위·원가** | **표준·로드맵** |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 598 / 800

<- **이전**: [597. IT 경영 관리 핵심 토픽 597번 시험 요약](/studynote/12_it_management/05_security_compliance/597_it_management_core_topic_597_exam_summary/)
**다음**: [599. IT 경영 관리 핵심 토픽 599번 시험 요약](/studynote/12_it_management/05_security_compliance/599_it_management_core_topic_599_exam_summary/) ->

---
