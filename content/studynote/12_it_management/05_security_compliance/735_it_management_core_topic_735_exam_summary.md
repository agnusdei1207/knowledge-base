---
title: "IT Management Core Topic 735 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 735. IT 경영 관리 핵심 토픽 735번 시험 요약 (IT Governance & Strategic Alignment)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 ISO 38500 / COBIT 2019 / ITIL 4 프레임워크 기반으로, **이사회(Board)의 책임(Evaluate·Direct·Monitor)** 하에 IT 투자 의사결정, 위험 통제, 성과 측정을 통합 관리하여 기업의 전략적 목표와 IT 자산을 정렬(Strategic Alignment)하는 통치 체계임.
> 2. **가치**: McKinsey(2023) 기준 거버넌스 성숙도 상위 25% 기업은 EBITDA 마진이 동종업계 대비 **8~12%** 높고, IT 프로젝트 실패율 **37% -> 14%**, 사이버 침해 복구 비용 평균 **$1.4M 절감**(IBM Cost of Data Breach 2023) 등 정량적 ROI 입증.
> 3. **판단 포인트**: **①** 중앙집중(CoE) vs 분산(Federated) 거버넌스 모델, **②** Agile/DevOps 조직에서의 거버넌스 충돌 해소(GovOps 개념 도입), **③** ESG·개인정보보호법(PIPA)·DORA(2024 EU) 등 신규 컴플라이언스 반영, **④** Shadow IT 및 SaaS Sprawl 통제 여부가 실무 핵심 쟁점.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대, 기업의 IT 자산은 CapEx·OpEx의 30~50%를 점유하며 단순 비용 센터에서 **전략적 가치 창출(Strategic Value Driver)** 의 중심으로 이동했습니다. 그러나 전통적 IT 운영 관리는 CFO·CIO·사업부서 간 이해상충, Shadow IT 급증(평균 기업 471개 SaaS 사용 vs IT 인지 200개 미만, Zylo 2023), 그리고 클라우드·AI 도입에 따른 신규 위험(Algorithmic Bias, 데이터 주권)으로 인해 한계에 직면했습니다.

이에 **"IT를 누가, 어떤 의사결정 권한으로, 어떤 메커니즘으로 통치하는가"** 라는 거버넌스(Governance) 문제가 경영 핵심 의제로 부상하였고, 단순 기술 관리를 넘어 **법적 책임·이해관계자 가치·리스크 조정**을 다루는 통합 프레임워크가 요구됩니다.

```text
+------------------------------------------------------------------+
|           IT 거버넌스의 3-Layer 통합 관점 (PDCA 확대)            |
+------------------------------------------------------------------+
|                                                                  |
|   +------------------------------------------------------+      |
|   |  Layer 1: Board / Steering Committee (통치 계층)     |      |
|   |   • ISO 38500: Evaluate -> Direct -> Monitor          |      |
|   |   • 책임: IT 전략 승인, 예산 1억+ 승인권, Risk Appetite|      |
|   +--------------------+---------------------------------+      |
|                        | 전략적 지시                                |
|   +--------------------v---------------------------------+      |
|   |  Layer 2: IT Governance Bodies (관리 계층)            |      |
|   |   • IT Steering Committee, Architecture Review Board |      |
|   |   • COBIT 2019: 40 Governance & Management Objectives|      |
|   |   • PMO, IT Risk Committee, Change Advisory Board(CAB)|      |
|   +--------------------+---------------------------------+      |
|                        | 운영·통제                                  |
|   +--------------------v---------------------------------+      |
|   |  Layer 3: Operational Delivery (실행 계층)            |      |
|   |   • ITIL 4 Service Value System (SVS)                |      |
|   |   • DevOps + Site Reliability Engineering(SRE)       |      |
|   |   • FinOps·GreenOps·DataOps 도메인별 거버넌스         |      |
|   +------------------------------------------------------+      |
|                                                                  |
|   +------------- 크로스컷팅 컴플라이언스 레이어 ----------+     |
|   |  ISO 27001 (정보보안) | PIPA/GDPR | DORA (2024)        |     |
|   |  ESG-ISSB S2 (IT 탄소)| NIS2 (EU)| CSA STAR (Cloud)   |     |
|   +------------------------------------------------------+     |
+------------------------------------------------------------------+
```

과거(2000년대)에는 ITIL v2/v3의 **프로세스 중심(process-oriented)** 접근으로 서비스 데스크·인시던트·문제를 관리하는 데 그쳤으나, 2018년 ITIL 4의 **SVS(Service Value System)** 도입 후 가치(value)·조직 문화·기술 트렌드를 포괄하는 **시스템 사고(Systems Thinking)** 기반 거버넌스로 진화했습니다. 2024~2025년에는 **AI 거버넌스(AI Governance)**·**데이터 거버넌스(DG)**가 신규 핵심 영역으로 부상하고 있습니다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"도시의 종합 도시계획(Urban Master Plan)"** 과 같습니다. 개별 건물(프로젝트)·도로(인프라)·치안(보안)을 따로 짓는 게 아니라, 도시 전체의 용도지역·교통망·재난대응 체계를 **도시계획 위원회(이사회)** 가 수립·감독하여 시민(사업부서)의 삶의 질(ROI)을 보장하는 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스 아키텍처는 국제표준 **ISO/IEC 38500:2015 (IT Corporate Governance)** 를 최상위 통치 프레임으로, **COBIT 2019** 를 통치-관리 매핑 프레임워크로, **ITIL 4** 를 서비스 운영 레퍼런스로, **ISO 27001 / NIST CSF** 를 통제 레퍼런스로 하는 **4-Layer 참조 모델(4-Layer Reference Model)** 로 구성됩니다.

```text
+--------------------------------------------------------------------+
|       IT 거버넌스 4-Layer Reference Architecture (참조 모델)        |
+--------------------------------------------------------------------+
|                                                                    |
|  +--------------------------------------------------------+       |
|  |  L1: 통치 프레임 (Governance Framework)                  |       |
|  |  ------------------------------------------            |       |
|  |  ISO/IEC 38500:2015   |  원칙 6개 (Responsibility,    |       |
|  |                       |   Strategy, Acquisition,       |       |
|  |                       |   Performance, Conformance,    |       |
|  |                       |   Human Behavior)              |       |
|  |  원칙 모델(E-D-M) -> 이사회 의사결정 사이클 (90~120일)   |       |
|  +-------------------------+------------------------------+       |
|                            | 매핑                                  |
|  +-------------------------v------------------------------+       |
|  |  L2: 통치-관리 목표 체계 (Objective Cascade)             |       |
|  |  ------------------------------------------            |       |
|  |  COBIT 2019:                                            |       |
|  |   • 5 Governance Objectives (EDM01~05)                 |       |
|  |   • 35 Management Objectives (APO/BAI/DSS/MEA 도메인)  |       |
|  |   • Design Factors(11개) 기반 맞춤화 (Enterprise Size,  |       |
|  |     Threat Landscape, IT Role, Compliance 등)          |       |
|  |   • Cascade: Stakeholder Needs -> Goals -> Process -> KPIs |       |
|  +-------------------------+------------------------------+       |
|                            | 연계                                  |
|  +-------------------------v------------------------------+       |
|  |  L3: 서비스 가치 시스템 (Service Value System)           |       |
|  |  ------------------------------------------            |       |
|  |  ITIL 4 SVS:                                            |       |
|  |   • Opportunity/Demand -> Value                          |       |
|  |   • 7 Guiding Principles                                |       |
|  |   • 34 Practices (Service Desk, Incident, Change Enab.) |       |
|  |   • Service Value Chain: Plan->Engage->Design->           |       |
|  |     Transition->Obtain/Build->Deliver->Support             |       |
|  +-------------------------+------------------------------+       |
|                            | 통제 사상 매핑                        |
|  +-------------------------v------------------------------+       |
|  |  L4: 통제 및 위험 기준 (Control & Risk Standards)       |       |
|  |  ------------------------------------------            |       |
|  |  • ISO 27001:2022 (Annex A 93 통제)                     |       |
|  |  • NIST CSF 2.0 (2024): Govern·Identify·Protect·       |       |
|  |    Detect·Respond·Recover (함수 6개로 확대)             |       |
|  |  • ISO 31000 (Risk Management)                          |       |
|  |  • PCI DSS 4.0, K-ISMS-P, ISMS-P 인증 체계              |       |
|  +--------------------------------------------------------+       |
|                                                                    |
|  -- 보조 프레임워크: TOGAF 10(EA) | PRINCE2 | PMBOK 7 | DevOps --|
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회 / IT Steering Committee** | 통치 의사결정(EDM) | 분기별 cadence, 5-9명, **CFO·CIO·CDO·CSO·사업부 COO** 참여. **Risk Appetite Statement** 승인, **Capital Allocation** 결정, KPI 6~9개 리뷰 (Cost·Quality·Speed·Security·Innovation·Compliance 균형) |
| **COBIT 2019 Cascade Engine** | 목표-프로세스-지표 연결 | **11 Design Factors**(전략·목표·위험·컴플라이언스·IT 역할·엔터프라이즈 크기·시스템 유형 등) 입력 -> **40 Objective 우선순위 자동 도출** -> 각 Objective당 4-7 Process + 3-5 KPI 매핑. **CMMI(0~5)** 기반 Maturity Assessment |
| **ITIL 4 Service Value Chain (SVC)** | 서비스 가치 창출 운영 | 6 Activity 체인(Plan->Engage->Design->Transition->Obtain/Deliver->Support). **Change Enablement** 시 MAB/CAB(Change Advisory Board) 거버넌스 게이트 운영. **Continual Improvement(Kaizen)** 11-step 모델 |
| **EA Repository (TOGAF 10 ADM)** | 아키텍처 정합성 보장 | **ADM 사이클(8 Phase: Preliminary->A~H)**, **Architecture Repository**(Architecture Meta-model, Capability Continuum), **Gap Analysis & Transition Architecture**를 통해 Shadow IT·중복 투자 식별 (평균 25% 비용 절감 가능) |
| **Governance, Risk & Compliance (GRC) Platform** | 통합 모니터링·리포팅 | **Archer·ServiceNow GRC·SAP GRC·OneTrust** 등. **Three Lines of Model(IIA 2020)**: 1st Line(운영자기통제) -> 2nd Line(리스크·컴플라이언스) -> 3rd Line(내부감사) 명확화. **KPI/RAG Dashboard** 실시간 |

### 핵심 메커니즘: **RACI Matrix + Decision Rights (RACI-D) 모델**

- **R**esponsible(수행) / **A**ccountable(책임) / **C**onsulted(자문) / **I**nformed(통보) + **Decision Rights(DR)** 매트릭스
- 예: 연간 IT 예산 1억+ 프로젝트 승인 -> **A: 이사회 / R: CIO 조직 / C: CFO·법무 / I: 전체 임원**
- 5억+ 프로젝트는 **Board 승인 의무** (일반적 기업 정책)
- 이 의사결정 권한 매트릭스를 **Decision Rights Matrix** 라 하며, RACI보다 명확한 **거버넌스 핵심 도구**입니다.

### 핵심 KPI 체계 (COBIT 2019 Process Capability 예시)

- **APO04(혁신 관리)**: R&D 투자율, Innovation Pipeline Conversion
- **DSS02(인시던트/서비스 요청 관리)**: MTTR(Mean Time To Restore), **MTTD(Mean Time To Detect) < 5min**
- **DSS05(보안 관리)**: **NIST CSF Tier 4**(Adaptive) 달성, 침해 탐지 < 24hr
- **MEA01(성과·컨폼런스)**: **K-ISMS 인증 유지율 100%**, 내부 통제 결함 < 0.5%

- **📢 섹션 요약 비유**: 4-Layer 참조 모델은 **"건물의 4종 설계도"** 와 같습니다. 도시계획(L1: ISO 38500)-> 건물 용도·설계 기준(L2: COBIT 2019)-> HVAC·전기·배관 시스템(L3: ITIL 4)-> 내화·내진·단열 기준(L4: ISO 27001/NIST)을 따로 그리고, **건축심의(Architecture Review Board)** 가 모든 도면을 통합 검토하여 안전하고 가치 있는 건물을 짓는 과정입니다.

---

## Ⅲ. 비교 및 연결

### 비교: ISO 38500 vs COBIT 2019 vs ITIL 4

| 구분 | ISO/IEC 38500:2015 | COBIT 2019 | ITIL 4 |
| :--- | :--- | :--- | :--- |
| **관점 (Scope)** | 통치(Governance) — 이사회 책임 | 통치 + 관리(Management) | 서비스 운영(Service Management) |
| **계층** | 전략적·통치 (Top) | 통치-관리 중간 브릿지 | 운영·전술 (Bottom) |
| **주 사용자** | 이사회·CEO·CFO | CIO·감사·GRC·EA 팀 | 서비스 데스크·SRE·DevOps |
| **구조** | 6개 원칙 + E-D-M 모델 | 11 Design Factor + 40 Objective + 100+ Process | 7 Guiding Principle + 34 Practice + SVC |
| **측정 도구** | 자기평가 체크리스트 | **CMMI 0~5 Maturity** | **4 Dimensions + Maturity Model** |
| **강점** | 간결·법적 책임 명시·국제표준 | **맞춤형·통합 매핑 가능**·감사용 | **실무 가이드·커뮤니티 강함** |
| **약점** | 구체적 프로세스 부재 | 학습 곡선 가파름 | 거버넌스 부분 약함 |
| **연계 프레임워크** | COBIT 2019 EDM 영역에 매핑 | ISO 27001·ITIL·TOGAF·NIST와 매핑 | COBIT DSS/BAI 영역에 매핑 |
| **인증 제도** | 공식 인증 없음 (자격증: **CGIT, CGEIT**) | **COBIT 2019 Foundation/Design/Implement** | **ITIL 4 Foundation/MP/SL** |
| **업데이트 주기** | 2015년 (개정 2024 초안 발표) | 2019년 (2018->2019) | 2019년 (Foundation 2024 리프레시) |

### 비교: 전통적 IT 거버넌스 vs Agile/DevOps 시대 거버넌스


## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 735 / 800

<- **이전**: [734. IT 경영 관리 핵심 토픽 734번 시험 요약](/studynote/12_it_management/05_security_compliance/734_it_management_core_topic_734_exam_summary/)
**다음**: [736. IT 경영 관리 핵심 토픽 736번 시험 요약](/studynote/12_it_management/05_security_compliance/736_it_management_core_topic_736_exam_summary/) ->

---
