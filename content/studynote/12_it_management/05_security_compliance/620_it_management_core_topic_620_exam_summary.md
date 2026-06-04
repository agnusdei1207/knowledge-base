---
title: "620. IT 경영 관리 핵심 토픽 620번 시험 요약 (IT Management Core Topic 620 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500, PMBOK 7th 등 글로벌 거버넌스 프레임워크를 기반으로, **전략-구조-프로세스-성과(SPP) 4축**을 통해 기업의 IT 자산을 비즈니스 가치로 전환하는 종합 관리 체계임.
> 2. **가치**: 성숙도 기반 거버넌스 체계 확립 시 IT 투자 대비 ROI 25~40% 향상, 프로젝트 성공률 28%->68% 개선(McKinsey, 2023), 보안 사고 대응 시간 70% 단축, IT 운영 비용 15~30% 절감 효과를 정량적으로 달성 가능함.
> 3. **판단 포인트**: **In-House vs Outsourcing vs Hybrid** 모델, **Centralized vs Federated vs DeCentralized** 거버넌스 구조, **Waterfall vs Agile vs Hybrid** 개발 방법론, **CAPEX vs OPEX** 회계 처리, **Build vs Buy vs Reuse** 의사결정 등 5대 핵심 트레이드오프를 비즈니스 임팩트와 리스크 허용도 기준으로 정량 평가해야 함.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화와 ESG·AI 거버넌스 규제 강화로 인해 IT 경영 관리의 패러다임이 **"비용 중심 IT 운영"**에서 **"가치 중심 IT 비즈니스 파트너십"**으로 전환되었습니다. 2024년 기준 국내 기업 78%가 CIO 직속 IT 거버넌스 위원회를 운영 중이며, IT 예산 대비 거버넌스 활동 비중은 평균 3.2%(IDC Korea, 2024)를 차지합니다. 기술사 시험에서는 단순 암기형 지식보다 **"왜(Why) 어떤 프레임워크를 어떤 시점에 적용하는가"**에 대한 의사결정 역량을 평가합니다.

```text
+-------------------------------------------------------------+
|        IT 경영 관리 4대 도메인 통합 프레임워크 (SPP-E)        |
+-------------------------------------------------------------+
                              |
        +---------------------+---------------------+
        v                     v                     v
+--------------+      +--------------+      +--------------+
|  Strategy    |      |   Process    |      |  Evaluation  |
|   (전략)      |◄----►|  (프로세스)   |◄----►|   (성과)     |
+--------------+      +--------------+      +--------------+
        |                     |                     |
        |                     v                     |
        |            +--------------+              |
        +-----------►|  Structure   |◄-------------+
                     |   (구조)      |
                     +--------------+
                              |
        +---------------------+---------------------+
        v                     v                     v
  +-----------+         +-----------+         +-----------+
  |  Plan     |         |  Build    |         |   Run     |
  |  (기획)   |         |  (구축)   |         |  (운영)   |
  +-----------+         +-----------+         +-----------+
   - EA/To-Be             - SI/구축              - ITIL/관제
   - RFP/BPR              - DevOps               - SLM/BCM
   - TCO/ROI              - Agile/Scrum          - FinOps
```

**기존 IT 관리 vs 현대 IT 경영 관리**의 핵심 차이는 다음과 같습니다:
- **기존(1980~2000)**: 시스템별 개별 운영, CAPEX 중심, CapEx 예산 80% 이상, 기술 중심 의사결정
- **현대(2010~현재)**: 전사 통합 거버넌스, OPEX·SUBSCRIPTION 혼합, FinOps 기반 클라우드 비용 최적화, 비즈니스 가치 중심 의사결정, Zero Trust 보안 모델
- **미래(2025~)**: AI-Driven 거버넌스, Autonomous IT Management, Algorithmic Decision Making, 지속가능성(Sustainable IT) KPI 통합

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 통합 계기판(Cluster Display)**과 같습니다. RPM(프로젝트 진행률), 속도(성과), 연료(예산), 엔진온도(리스크), 네비게이션(전략) 모든 지표를 실시간 통합 모니터링하여 운전자가 최적의 코스를 선택할 수 있게 하는 것이며, 계기판이 없으면 아무리 좋은 엔진(기술)도 사고로 끝납니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 축(SPP-E)을 구성하는 핵심 컴포넌트와 각 영역의 메커니즘은 다음과 같이 정의됩니다.

```text
+----------- IT 경영 관리 상세 아키텍처 (4-Layer Reference Model) -----------+
|                                                                            |
|  +--------------------------------------------------------------------+    |
|  | Layer 1: 거버넌스 의사결정층 (Governance Decision Layer)             |    |
|  |   +- 이사회(IT Steering Committee) - 분기 1회 정례                 |    |
|  |   +- CIO/CTO - 의사결정 권한 위임 (RACI Matrix)                    |    |
|  |   +- IT 전략 위원회 - 월 1회                                         |    |
|  |   +- PMO/CoE - 일일/주간 단위 운영                                  |    |
|  +--------------------------------------------------------------------+    |
|                              | Cascade                                     |
|  +--------------------------------------------------------------------+    |
|  | Layer 2: 프레임워크·정책층 (Framework & Policy Layer)                |    |
|  |   +- COBIT 2019 (40 Governance/Management Objectives)              |    |
|  |   +- ITIL 4 (34 Practices in 4 Dimensions)                          |    |
|  |   +- ISO 38500 (6 Principles) / ISO 27001 (Annex A 93 Controls)    |    |
|  |   +- PMBOK 7 (8 Performance Domains, 12 Principles)                 |    |
|  |   +- TOGAF 10 ADM (Architecture Development Method)                 |    |
|  |   +- 내부 정책/표준/지침(Policy/Standard/Guideline)                 |    |
|  +--------------------------------------------------------------------+    |
|                              | Implement                                   |
|  +--------------------------------------------------------------------+    |
|  | Layer 3: 운영 프로세스층 (Operational Process Layer)                  |    |
|  |   +- Plan(EA, BCP, IT 재무) -> Build(SDLC, DevOps) ->                |    |
|  |   |  Run(ITSM, 관제) -> Evaluate(KPI, Balanced Scorecard)           |    |
|  |   +- Risk Mgmt(ISO 31000), Compliance(PCI-DSS, PIPA, GDPR)         |    |
|  |   +- Vendor Mgmt(SLA/SLM, SaaS 거버넌스, 제3자 리스크)             |    |
|  +--------------------------------------------------------------------+    |
|                              | Measure                                     |
|  +--------------------------------------------------------------------+    |
|  | Layer 4: 측정·성과층 (Measurement & Performance Layer)               |    |
|  |   +- KPI Tree(CSF->KPI->KGI) - 4관점(재무/고객/내부/학습)              |    |
|  |   +- CMMI(1~5단계), TMMi, COBIT Maturity(0~5)                       |    |
|  |   +- ROI/NPV/IRR, TCO 분석 모델                                     |    |
|  |   +- 감사/이행 검증(Internal/External Audit)                       |    |
|  +--------------------------------------------------------------------+    |
+----------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 거버넌스 시스템** | IT 의사결정·통제·모니터링 체계 | 40개 Governance/Management Objectives를 EDM(evaluate/Direct/Monitor), APO(Align/Plan/Organize), BAI(Build/Acquire/Implement), DSS(Deliver/Service/Support), MEA(Monitor/Evaluate/Assess) 5개 도메인에 매핑, Design Factor 11개로 조직별 맞춤 설계 |
| **ITIL 4 Service Value System** | IT 서비스 End-to-End 가치 흐름 | 34개 Practice(General/Service/Technical Management), 4가지 Dimension(Organizations/People/Information/Technology/Partners/Value Streams/Processes), Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 통합 관리 | Portfolio-PMO/Program-PMO/Project-PMO 3계층, EPMO(Enterprise)->DPMO(Divisional)->SPMO(Strategic), KPI: SPI(Schedule Performance Index), CPI(Cost Performance Index), EAC(Estimate At Completion) |
| **EA(Enterprise Architecture)** | 전사 IT 정합성·표준화 | TOGAF 10 ADM 8단계(Preliminary->A->B->C->D->E->F->G->Requirements Mgmt), Zachman 6x6 Matrix, FEAF 5계층(Business->Data->Application->Technology->Presentation), ARIS(Architecture of Integrated Information Systems) |
| **BCM(Business Continuity Mgmt)** | 업무 연속성·재해복구 | ISO 22301 PDCA, BIA(Business Impact Analysis)->RTO/RPO 산정->DR 전략(Synchronous/Asynchronous/Pilot Light/Warm Standby/Multi-Site Active-Active), 연간 RTO 기준 4시간 이내 권장 |
| **IT 재무관리/FinOps** | IT 비용 투명성·최적화 | IT 회계(직접/공통/간접비 배부), Showback/Chargeback 모델, TCO(Total Cost of Ownership) 5개년 분석, 클라우드 FinOps(Commit/Use/Restore 단계별 할인율 30~70%) |
| **IT 성과관리/BSC** | 전략-성과 연계 | Balanced Scorecard 4관점(Financial/Customer/Internal Process/Learning&Growth), Strategy Map 인과관계 체인, OKR(Objective Key Results) 연계 |

**핵심 의사결정 알고리즘**:
```
Step 1: 요구사항 도출 -> 비즈니스 목표와 IT 투자 정렬도 분석
Step 2: 다중 평가기준 의사결정(AHP - Analytic Hierarchy Process)
        가중치(사업 임팩트 40% + 리스크 25% + 비용 20% + 기술성숙도 10% + 전략정합 5%)
        일관성 비율(CR) < 0.1 일관성 검증
Step 3: TCO 산정(초기 CAPEX + 5년 OPEX + 전환/폐기비용)
Step 4: ROI/NPV/IRR 계산
        - ROI(%) = (총편익 - 총비용) / 총비용 × 100
        - NPV = Σ[CFt / (1+r)^t] - 초기투자
        - IRR: NPV=0이 되는 할인율 r
Step 5: Portfolio 최적화(Bubble Diagram: 가치^, 리스크v 우선선정)
```

- **📢 섹션 요약 비유**: IT 경영 관리의 4개 계층은 **건물의 구조 시스템**과 같습니다. 기초(거버넌스 의사결정층) 위에 기둥(프레임워크), 바닥과 벽(운영 프로세스층), 그리고 창문과 문(측정·성과층)이 올라야 비로소 사람이 살 수 있는 '가치 있는 공간'이 만들어지며, 어느 한 층이 무너지면 건물 전체가 위험해집니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 핵심 토픽들은 상호 보완적이면서도 적용 맥락에 따라 차별적으로 사용됩니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·통제 | IT 서비스 관리 | 프로젝트 관리 | 정보보안 관리 | 전사 아키텍처 |
| **관점** | What(무엇을) | How(어떻게) | When(언제/범위) | Secure(안전하게) | Blueprint(설계도) |
| **도메인/구조** | 5도메인 40목표 | 34 Practice 4 Dimension | 8 Performance Domain | Annex A 93 통제항목 | ADM 8단계 |
| **대상** | 임원·이사회 | 서비스 운영자 | 프로젝트 매니저 | CISO·보안팀 | 아키텍트 |
| **측정 기준** | Maturity(0~5) | SVS 가치 흐름 | Value Delivery | Risk Level | ADM 준수율 |
| **결합 활용** | ITIL·ISO 27001 매핑 | COBIT 프로세스 연계 | Agile/Hybrid | COBIT DSS06 | Zachman 매핑 |
| **인증/감사** | COBIT Certified | ITIL Foundation~Master | PMP/PfMP | ISMS 인증 | TOGAF Certified |
| **강점** | 의사결정·통제 명확 | 실용적 운영 | 예측 가능성 | 보안 통제 | 정합성·표준화 |
| **약점** | 운영 디테일 부족 | 거버넌스 약함 | 반복·예측 프로젝트 한정 | 비즈니스 연계 약함 | 구축 복잡도 |

**상호 연계 매핑 사례**:
- **COBIT EDM02(거버넌스)** ↔ **ISO 38500 원칙 1(Responsibility)** ↔ **이사회 IT 위원회 운영규정**
- **COBIT BAI02(요구사항 관리)** ↔ **PMBOK Needs Assessment** ↔ **TOGAF Phase A(Architecture Vision)**
- **COBIT DSS02(서비스 요청·사고)** ↔ **ITIL Incident Mgmt** ↔ **ISO 20000(서비스 품질)**
- **COBIT DSS05(보안)** ↔ **ITIL Security Mgmt** ↔ **ISO 27001 A.5~A.8 통제**

- **📢 섹션 요약 비유**: 이 5대 프레임워크는 **오케스트라의 악기**와 같습니다. COBIT은 **지휘자(전체 흐름)**, ITIL은 **제1바이올린(현장 운영)**, PMBOK은 **타악기(마일스톤·리듬)**, ISO 27001은 **방음벽(안전)**, TOGAF는 **악보(설계도)**이며, 각 악기만 연주하면 소음이지만 지휘자 아래 통합되면 교향곡이 완성됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험의 답안 작성 시 단순 정의 나열이 아니라 **"현황-문제-해결-효과"** 4단계 논리 구조와 정량적 근거를 반드시 포함해야 합니다. 특히 K-ISMS, 개인정보보호법, 클라우드 보안인증(CSAP), 디지털서비스 혁신 등의 한국형 규제 환경을 정확히 이해해야 합니다.

### 기술사형 판단 체크리스트

1. **거버넌스 성숙도 진단**: ISO 38500 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) 기반 As-Is/To-Be 갭 분석, COBIT Maturity Level 0~5 중 현재 수준 정량 측정(예: Level 2.3 -> Level 3.5 목표)
2. **TCO/ROI 정량 분석**: 5개년 TCO(초기투자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 620 / 800

<- **이전**: [619. IT 경영 관리 핵심 토픽 619번 시험 요약](/studynote/12_it_management/05_security_compliance/619_it_management_core_topic_619_exam_summary/)
**다음**: [621. IT 경영 관리 핵심 토픽 621번 시험 요약](/studynote/12_it_management/05_security_compliance/621_it_management_core_topic_621_exam_summary/) ->

---
