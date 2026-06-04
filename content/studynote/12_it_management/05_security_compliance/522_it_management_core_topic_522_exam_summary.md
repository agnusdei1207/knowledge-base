+++
title = "522. IT 경영 관리 핵심 토픽 522번 시험 요약 (IT Management Core Topic 522 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(Control Objectives for Information and Related Technologies)**의 40개 거버넌스/관리 목표(Governance & Management Objectives)를 핵심축으로, **EA(Enterprise Architecture)·ITSM(IT Service Management)·감리(Audit)·투자관리(Portfolio/Investment)**를 통합 운용하여 **Strategy -> Portfolio -> Project -> Operation -> Value**의 가치 사슬(Value Chain)을 완성하는 경영 체계이다.
> 2. **가치**: McKinsey(2022) 기준 COBIT 2019 + ITIL 4 + ISO 38500 통합 적용 시 **IT-Business Alignment 성숙도 평균 2.4 -> 3.8단계 상승**, **프로젝트 실패율 약 35% 감소**, **연간 IT 운영비용 12~18% 절감**(TCO 최적화), **감리 부적합 판정률 28% -> 6%로 하락** 효과를 정량적으로 기대할 수 있다.
> 3. **판단 포인트**: 중앙집중형(Centralized)·연방형(Federated)·하이브리드형 거버넌스 모델 중 조직 문화·규모·업종(Banking/Manufacturing/Public)에 맞는 모델 선택, **RACI 매트릭스** 기반 의사결정 권한 위계 설계, **CSF(Key Goal Indicator) + KPI(Key Performance Indicator) + KRI(Key Risk Indicator)**의 3축 균형 측정 체계 확립, 그리고 PMO(Project Management Office)·EAO·SMO(Service Management Office) 간 역할 충돌 방지 설계가 핵심 쟁점이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입(Tactical IT)을 넘어, 기업 전략과 IT 자산·서비스·리스크를 **지속적으로 정렬·최적화·측정**하는 체계가 요구되면서 IT 경영 관리(Information Technology Management)는 C-Level 의사결정 영역으로 격상되었다. 과거 1990년대 후반~2000년대 Y2K, ERP 폭증기에는 프로젝트 단위 관리(PMBOK·PMP 중심)가 주류였으나, 2010년대 클라우드·모바일·빅데이터·AI로 인한 **Shadow IT·프로젝트 중복 투자(평균 25% 중복, Gartner 2021)**, 2020년대 **GDPR·개인정보보호법·AI기본법·ESG 공시(DCP 230)** 등 규제 강화로 인해 **사후 통제(Audit/감리)** 중심에서 **사전 예방(Governance/Risk/Compliance, GRC)** 중심으로 패러다임이 전환되었다.

특히 2024년 이후 **AI 거버넌스**(NIST AI RMF·EU AI Act)와 **제로트러스트**(Zero Trust Architecture), **레귤레이터리 테크**(RegTech)가 새로운 통제 영역으로 부상하면서, 전통적 IT 거버넌스 프레임워크에 **AI Ethics Board·Cybersecurity Risk Committee·Sustainability KPI**를 통합하는 **"확장형 IT 거버넌스(Extended IT Governance)"**가 기술사 시험의 핵심 논점이 되고 있다.

```text
+---------------------------------------------------------------------+
|              IT 경영 관리 통합 거버넌스 프레임워크 (GIV)             |
+---------------------------------------------------------------------+
|                                                                     |
|  +------------------- Strategy Layer -------------------+           |
|  |  Corporate Vision / Mission / Strategic Objectives  |           |
|  |       <-> (Strategy Alignment via Balanced Scorecard) |           |
|  +----------------------+-------------------------------+           |
|                         |                                           |
|  +---------- Governance Layer (COBIT 2019 EDM) --------+             |
|  |  EDM01 (프레임워크 유지) | EDM02 (이해관계자 요구)   |             |
|  |  EDM03 (위임·구조화)     | EDM04 (리스크 최적화)    |             |
|  |  EDM05 (자원 투명성)     |                          |             |
|  +----------------------+-------------------------------+           |
|                         |                                           |
|  +---------- Management Layer (COBIT 2019 APO/BAI/DSS) ----------+  |
|  |  APO (Align/Plan/Organize) | BAI (Build/Acquire/Implement)     |  |
|  |  DSS (Deliver/Service/Support) | MEA (Monitor/Evaluate/Assess)  |  |
|  +-----+---------------+--------------+-------------+------------+  |
|        |               |              |             |                |
|   +----v----+    +-----v-----+  +-----v----+  +-----v-----+         |
|   |  EA     |    |   ITSM    |  | Portfolio|  |   Audit   |         |
|   |(TOGAF)  |    | (ITIL 4)  |  |   Mgmt   |  |  (ISACA)  |         |
|   +----+----+    +-----+-----+  +-----+----+  +-----+-----+         |
|        |               |              |             |                |
|   +----v----+    +-----v-----+  +-----v----+  +-----v-----+         |
|   |Cloud·AI |    |Incident·  |  |Project·  |  |내부통제·  |         |
|   |Data·Sec |    |Change·    |  |Investment|  |컴플라이언스|         |
|   |Architecture| |Problem·  |  |ROI/TCO   |  |리스크평가  |         |
|   +----+----+    |ServiceReq |  +----------+  +------------+         |
|        |         +-----------+                                       |
|   +----v-----------------------------------------------------+       |
|   |  Measurement & Feedback (CSF/KPI/KRI) + Audit Findings   |       |
|   +----+-----------------------------------------------------+       |
|        +----------------------+-------------------------------------+
|                               |
|                  +------------v------------+
|                  |    Continuous Loop      |
                  | (PDCA + Kaizen + Audit) |
                  +-------------------------+
```

**구 vs 신 패러다임 비교**

| 구분 | 구 패러다임 (Project-Centric) | 신 패러다임 (Value-Centric) |
|---|---|---|
| 관리 대상 | 개별 프로젝트 (Project) | 포트폴리오 + 서비스 (Portfolio+Service) |
| 통제 시점 | 사후 (Post-Implementation Review) | 사전 + 사중 + 사후 (Continuous) |
| 평가 지표 | 일정·예산·범위 (Triple Constraint) | 비즈니스 가치·ROI·TCO·Bene-Risk Ratio |
| 거버넌스 | CIO 독단, IT 부서 한정 | IT Steering Committee, Board-level Governance |
| 프레임워크 | PMBOK 단독 | COBIT 2019 + ITIL 4 + ISO 38500 + TOGAF 통합 |
| 리스크 | 프로젝트 리스크 중심 | Operational·Cyber·Compliance·AI Ethics Risk 통합 |

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판(스피도미터·연료계·경고등)**과 같습니다. 엔진(IT 인프라)만 좋다고 잘 달리는 것이 아니라, **운전자(경영진)**가 계기판의 수치를 실시간으로 보면서 **방향(전략)**을 조정해야 목적지(비즈니스 가치)에 안전하게 도착할 수 있습니다. 과거에는 엔진룸만 점검했다면, 지금은 운전자석의 종합 계기판이 필수입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 핵심 캐스케이드(Goals Cascade) 메커니즘

COBIT 2019는 **13개 Enterprise Goals -> 13개 Alignment Goals -> 40개 Governance/Management Objectives**의 3단계 캐스케이드 구조로, **"이해관계자 니즈 -> 기업 목표 -> IT 정렬 목표 -> 통제 목표"**로의 변환을 체계화한다. 핵심은 **"Goal ↔ Process ↔ Component ↔ Metric"**의 4-P связь이며, 각 통제 목표(예: EDM04 Ensured Risk Optimization)는 평균 3~4개의 프로세스(예: APO12 Manage Risk)와 연결된다.

### 2. RACI 매트릭스 기반 의사결정 위계

IT 거버넌스의 실질적 작동은 **RACI(Responsible, Accountable, Consulted, Informed)** 매트릭스로 구현된다. 한 가지 통제 목표당 **A(Accountable) 1명, R(Responsible) 2~3명, C(Consulted) 4~7명, I(Informed) 다수**로 설계하며, **"Single A, Multiple R" 원칙**을 통해 책임 공백(Responsibility Gap)과 중복(Duplication)을 방지한다.

### 3. CSF·KPI·KRI 3축 측정 체계

- **CSF(Critical Success Factor)**: "무엇이 성공에 필요한가" (정성적, 전략적) - 예: "고객 만족도 향상"
- **KPI(Key Performance Indicator)**: "어떻게 성과를 측정하는가" (정량적, 결과) - 예: "NPS 60 이상"
- **KRI(Key Risk Indicator)**: "리스크 수준을 어떻게 조기에 감지하는가" (선행지표) - 예: "Critical Incident MTTR 30분 이내"

```text
+------------------ IT 경영 관리 아키텍처 (4-Layer Reference Model) --------------+
|                                                                                  |
|  Layer 1: Strategy & Governance (전략·거버넌스)                                 |
|  +------------------------------------------------------------------+           |
|  | IT Steering Committee (CSO/CIO/CFO/CDO/CISO 합동)               |           |
|  |   • 의사결정: 예산 승인 (>$1M), 아키텍처 표준, 투자 우선순위     |           |
|  |   • 주기: 월 1회 + 수시 (긴급 안건 시 24h 내 소집)              |           |
|  +----+-------------------------------------------------------------+           |
|       | 정책·표준·예산                                                          |
|  +----v-------------------------------------------------------------+           |
|  Layer 2: Management (관리)                                                    |
|  |  +--------+ +--------+ +--------+ +--------+ +--------+         |           |
|  |  |  PMO   | |  EAO   | |  SMO   | |  GRC   | |  SRO   |         |           |
|  |  |Portfolio| | TOGAF | | ITIL 4 | |COBIT 19| |Security|         |           |
|  |  |  /PMO  | |  ADM  | |  34Pr  | | 40Obj  | | NIST CSF|        |           |
|  |  +---+----+ +---+----+ +---+----+ +---+----+ +---+----+         |           |
|  +------+----------+----------+----------+----------+--------------+           |
|         |          |          |          |          |                          |
|  +------v----------v----------v----------v----------v--------------+           |
|  Layer 3: Operation & Delivery (운영·전달)                       |           |
|  |  +---------+ +---------+ +---------+ +----------+ +--------+  |           |
|  |  | Cloud   | | DevOps  | | Data    | | Service  | | Network|  |           |
|  |  | FinOps  | | CI/CD   | | Lake    | | Desk L1-3| | SDN    |  |           |
|  |  +---------+ +---------+ +---------+ +----------+ +--------+  |           |
|  +------+----------------------------------------------------------+           |
|         | 이벤트·메트릭                                                          |
|  +------v----------------------------------------------------------+           |
|  Layer 4: Measurement, Audit & Feedback (측정·감사·환류)           |           |
|  |  CSF 6개 | KPI 24개 | KRI 12개 | SLA 18개 | 감사조치 이행률   |           |
|  |  ------------------------------------------------------------   |           |
|  |  -> APM(Observability) -> BI 대시보드 -> 내부감사(IS Audit)        |           |
|  +------------------------------------------------------------------+           |
|                                                                                  |
|  Cross-Cutting Concerns: ① Security(ZTA) ② Privacy(PII/PIPA) ③ AI Ethics ④ ESG  |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee** | 최고 의사결정 기구 | CIO(의장)·CFO·CDO·CISO·사업부 CEO로 구성, **분기 1회 정기 + 월 1회 운영위원회**. 예산 $1M 이상 프로젝트 승인권, 표준 위반 시 VETO권 행사. 의사결정 시간 SLA: 긴급 24h, 일반 5BD |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리 | **3-tier 구조**(전략 PMO / 프로젝트 PMO / 운영 PMO), **PPM 도구**(Planview·Clarity PPM·ServiceNow SPM) 활용, **Stage-Gate 모델**(Idea->Feasibility->Planning->Execution->Closure) 적용, **Earned Value Management(EVM)**로 CPI/SPI 측정 |
| **EAO (Enterprise Architecture Office)** | 전사 아키텍처 거버넌스 | **TOGAF ADM(Architecture Development Method)** 10단계 순환, **ArchiMate 3.2** 모델링 언어, **관점(View)**: Business·Application·Data·Technology 4계층. **ARB(Architecture Review Board)**에서 아키텍처 적합성 심사(Compliance Rate ≥ 90% 목표) |
| **SMO (Service Management Office)** | IT 서비스 운영 | **ITIL 4 Service Value System(SVS)** 기반 34개 프로세스 운영, **서비스 카탈로그**(평균 150~300개 서비스)·**SLA**(가용성 99.9%/MTTR 4h/MTBF 720h), **CSI(Continual Service Improvement)**로 연 7% 효율 개선 목표 |
| **GRC (Governance·Risk·Compliance)** | 통합 컴플라이언스 | **Archer GRC / ServiceNow GRC / SAP GRC** 플랫폼, **내부통제 5개 컴포넌트**(COSO 2013) 기반 통제 활동 설계, **리스크 레지스터**(연 200~500개 리스크 항목), **KRI 대시보드** 실시간 모니터링, **감사 증적(Audit Trail)** 5~7년 보존 |
| **IS Audit (정보시스템 감리)** | 독립적 검증 | **ISACA CISA·CISM** 자격 보유 감사인, **감리 유형**: 종합감리/부분감리/특수감리, **IT 일반통제 11개 영역**(조직·문서
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 522 / 800

<- **이전**: [521. IT 경영 관리 핵심 토픽 521번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/521_it_management_core_topic_521_exam_summary/)
**다음**: [523. IT 경영 관리 핵심 토픽 523번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/523_it_management_core_topic_523_exam_summary/) ->

---
