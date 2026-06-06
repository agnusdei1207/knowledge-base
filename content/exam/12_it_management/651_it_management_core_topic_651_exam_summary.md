---
title: "IT Management Core Topic 651 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 Topic 651은 **COBIT 2019, ISO 38500, ITIL 4, TOGAF** 등 글로벌 거버넌스 프레임워크를 통합하여 **이해관계자 가치(Value Goals) -> 정렬(Alignment) -> 거버넌스 시스템(Governance System) -> 성능 측정(Metrics & Maturity)** 의 4계층 사슬로 IT를 경영 자산화하는 체계이며, 핵심은 **EDM(Evaluate, Direct, Monitor) -> APO -> BAI -> DSS -> MEA** 의 40개 관리 목표(Process Capability Level 0~5)를 조직의 통제 환경에 매핑하는 것이다.
> 2. **가치**: McKinsey 조사에서成熟된 IT 거버넌스 도입 기업은 **IT 투자 ROI 23% 향상, 프로젝트 실패율 38% 감소, IT 운영비 15~20% 절감, 감사 적발 건수 50%v** 효과를 보이며, **ISO 38500 인증 기업의 주주환원율(SROE)**이 비인증 대비 평균 1.7%p 높다. 정량 KPI(가용성 99.95%, MTTR ≤ 30분, 변경 성공률 ≥ 97%, 보안사고 MTTC ≤ 4시간) 기반 운영이 가능하다.
> 3. **판단 포인트**: **① 프레임워크 선택**(COBIT 단독 vs ITIL+ISO 38500 이원화 vs 통합 거버넌스), **② 거버넌스 성숙도 진단 도구**(CMMI 5단계 vs COBIT PAM 0~5), **③ IT 투자평가 기법**(NPV/IRR/PP/ROI/TCO), **④ EA-거버넌스-서비스의 3축 연계 수준**, **⑤ Risk Appetite와 Control의 균형** — 이 5가지 의사결정 축을 경영진 관점에서 기술적 근거와 함께 제시할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 **Back-office 지원 기능**(1980~90년대)에서 **경영 핵심 자산**(2000년대~)으로 재편되면서, IT 투자는 전체 매출의 3~10%(은행·통신의 경우 8~15%)에 이른다. 그러나 다수의 글로벌 통계(McKinsey 2023, KPMG 2022)는 **전체 IT 예산 중 30~40%가 "비가치(non-value)" 또는 "중복"**에 낭비되며, 디지털 전환(DX) 프로젝트의 **70%가 기대 ROI 미달**로 종료된다고 보고한다. 이는 **명확한 거버넌스 체계, 투자 우선순위 의사결정 기준, 정량 성과측정 체계의 부재**가 근본 원인이다.

Topic 651은 이러한 문제를 해결하기 위해 **IT 전략 수립 -> 투자 포트폴리오화 -> 거버넌스 체계 설계 -> 성과 측정 -> 지속적 개선**의 End-to-End 라이프사이클을 다루며, **COBIT 2019의 40 Governance & Management Objectives, ISO 38500의 6 원칙, ITIL 4의 34 Practices, TOGAF ADM 10단계, ISO 27001 통제영역 14개, COSO ERM 5요소**가 통합 참조 모델로 작동한다.

```text
[정보관리기술사 Topic 651: IT 경영 관리 통합 프레임워크]

  +--------------------------------------------------------------------+
  |        +--------------------------------------------------+        |
  |        |  LEVEL 4: 거버넌스 목표 (Governance Objectives)   |        |
  |        |  • 주주가치 극대화  • 컴플라이언스  • 리스크관리   |        |
  |        |  • 이해관계자 가치  • 지속가능성(ESG-IT)          |        |
  |        +------------------+-------------------------------+        |
  |                           | (Translate)                            |
  |        +------------------v-------------------------------+        |
  |        |  LEVEL 3: 거버넌스 시스템 (COBIT 2019)            |        |
  |        |  EDM (5) -► APO (14) -► BAI (11) -► DSS (6) -► MEA (4)|       |
  |        |   평가    정렬/계획   구축/변경    서비스운영   모니터링|      |
  |        +------------------+-------------------------------+        |
  |                           |                                       |
  |        +------------------v-------------------------------+        |
  |        |  LEVEL 2: 컴포넌트 & 원칙 (ISO 38500 / ITIL 4)    |        |
  |        |  ①Responsibility ②Strategy ③Acquisition          |        |
  |        |  ④Performance  ⑤Conformance ⑥Human Behavior       |        |
  |        |  + 34 Service Value Chain Activities              |        |
  |        +------------------+-------------------------------+        |
  |                           |                                       |
  |        +------------------v-------------------------------+        |
  |        |  LEVEL 1: 실행 계층 (EA + 운영 + 보안)            |        |
  |        |  TOGAF ADM | 서비스데스크 | SIEM/SOC | DevOps | DB ||     |
  |        +--------------------------------------------------+        |
  +--------------------------------------------------------------------+
```

기존(1990년대)에는 IT 관리가 **프로젝트 단위(Waterfall)**의 **TCO(Total Cost of Ownership)**와 **데이터센터 가용성** 위주로 운영되어, **"IT 비용은 통제하되 비즈니스 성과는 비가시"**라는 한계가 있었다. 새로운 패러다임(2020년대~)은 **"Value-driven IT"**로 전환되어, **① 비금융 KPI(사용자 경험 NPS, Time-to-Market), ② ESG-IT, ③ AI/ML 기반 의사결정 자동화, ④ Zero Trust 보안**을 통합 거버넌스 객체로 다룬다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **배(B vessel)의 항해**와 같다. **COBIT은 선체(설계도)**, **ISO 38500은 6가지 항해 규칙(원칙)**, **ITIL은 엔진룸 운영 매뉴얼**, **TOGAF는 항로도(EA)**, **BSC/성과 KPI는 속도계·나침반**이다. 이 5가지가 어긋나면 아무리 좋은 엔진(IT 인프라)도 **좌초(Project Failure)**한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 핵심 메커니즘

COBIT 2019는 **40개 Governance & Management Objectives**를 **5개 도메인**(EDM, APO, BAI, DSS, MEA)으로 분류하며, 각 목표는 **Process Capability Level 0(Incomplete) ~ 5(Optimizing)**로 측정한다. 핵심 작동 원리는 다음과 같다:

1. **Stakeholder Needs & Goals** 식별 (13개 Cascade 목표: Benefits Realization, Risk Optimization, Resource Optimization, Compliance, etc.)
2. **Enterprise Goals**로 1차 변환 (13개) -> **Alignment Goals**로 2차 변환 (13개) -> **Management Objectives** 매핑
3. **Governance System Components 7종**: 프로세스, 조직구조, 정보 흐름, 사람/역량, 정책/원칙, 문화/윤리, 서비스/인프라
4. **Design Factors 11종**: Enterprise Strategy, Goals, Risk Profile, etc. -> **거버넌스 시스템의 우선순위/형태 결정**
5. **Focus Area**: 사이버보안, DevOps, RPA 등 특정 영역의 **맞춤형 목표 집합**

### 2. ISO/IEC 38500 IT 거버넌스 3-레이어

```text
[ISO 38500: 6 Principles × 5 Responsibilities × 3 Governance Model Layers]

   +---------------------------------------------------------------+
   |  Layer 1: GOVERNANCE (Board / CISO / CDO)                     |
   |   E --► D --► M                                                |
   |   Evaluate | Direct | Monitor                                   |
   |             |         |                                         |
   |   +---------v---------v--------------------------------+        |
   |   | Principle 1: Responsibility  (역할/책임 명확화)   |        |
   |   | Principle 2: Strategy       (비즈니스-IT 정렬)    |        |
   |   | Principle 3: Acquisition    (IT 조달 의사결정)    |        |
   |   | Principle 4: Performance    (KPI/SLA 측정)        |        |
   |   | Principle 5: Conformance    (법·규정·정책 준수)   |        |
   |   | Principle 6: Human Behavior (문화/윤리/행동)      |        |
   |   +----------------------------------------------------+       |
   |   Layer 2: MANAGEMENT  (CIO / IT Steering Committee)          |
   |   Planning | Implementation | Operation | Monitoring           |
   |   +----------------------------------------------------+       |
   |   | Plan: 거버넌스 정책, 예산, 자원, 위험 계획         |       |
   |   | Implement: 표준, 절차, 프로젝트, 변경 구현        |       |
   |   | Operate: 일상적 서비스 운영과 성과 보고            |       |
   |   | Monitor: 측정, 평가, 감사, 개선 활동               |       |
   |   +----------------------------------------------------+       |
   |   Layer 3: OPERATIONS  (Service Owner / Dev Team / SOC)        |
   |   실제 시스템, 프로세스, 인력 운영                              |
   +---------------------------------------------------------------+
```

### 3. ITIL 4 Service Value System (SVS)

ITIL 4의 핵심은 **34 Practices × Service Value Chain(SVC) × 7 Guiding Principles**로, SVC는 **Plan->Engage->Design & Transition->Obtain/Build->Deliver & Support->Improve**의 6개 Activity로 구성되며, **Opportunity/Demand -> Value** 변환의 핵심 엔진이다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 거버넌스 최상위 | 5개 목표(EDM01~05): 거버넌스 체계 평가, Benefit Delivery, Risk Optimization, Resource Optimization, Transparency. C-suite/이사회 수준 의사결정 |
| **APO (Align, Plan, Organize)** | 전략-전술 정렬 | 14개 목표: APO01~14. **IT 전략**(APO02), **아키텍처**(APO03), **포트폴리오**(APO05), **예산**(APO06), **인력**(APO07), **관계**(APO08), **벤더**(APO10), **리스크**(APO12), **보안**(APO13) — Value Streams로 표현 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축/변경 | 11개 목표: **프로젝트 관리**(BAI01), **요구사항**(BAI02), **솔루션 설계**(BAI03), **가용성/용량**(BAI04), **조직 변경**(BAI05), **변경 관리**(BAI06), **수용/전환**(BAI07), **지식**(BAI08), **자산**(BAI09), **구성**(BAI10), **품질**(BAI11) |
| **DSS (Deliver, Service, Support)** | 일상 서비스 운영 | 6개 목표: **운영**(DSS01), **서비스 요청/사고**(DSS02), **문제**(DSS03), **연속성**(DSS04), **보안 서비스**(DSS05), **비즈니스 통제**(DSS06) — SLA/OLA/UC 기반 |
| **MEA (Monitor, Evaluate, Assess)** | 측정/감사/개선 | 4개 목표: **성과/준수**(MEA01), **내부 통제**(MEA02), **외부 감사**(MEA03), **성과/목표**(MEA04) — BSC, CSAT, NPS, OKR 활용 |

### 4. 핵심 측정 지표 (Key Metrics)

| 영역 | 정량 KPI | 산출식/기준 | 목표 수준 |
| :--- | :--- | :--- | :--- |
| **IT 서비스 가용성** | 시스템 가동률 | (총 시간-장애시간)/총 시간 | 99.9%(Tier-2) ~ 99.99%(Tier-1) |
| **사고 대응** | MTTR / MTTD | Mean Time To Recover / Detect | MTTD ≤ 5분, MTTR ≤ 30분(Critical) |
| **변경 관리** | 변경 성공률/비상변경률 | (성공변경건수/전체변경건수) | 성공률 ≥ 97%, 비상변경 ≤ 5% |
| **프로젝트 성과** | SPI / CPI | EV/PV, EV/AC (PMBOK) | SPI, CPI ≥ 1.0(±0.1) |
| **IT 투자 효율** | NPV / IRR / Payback | Σ(CFₜ/(1+r)ᵗ) - C₀ | NPV > 0, IRR > WACC+3%p |
| **보안 성숙도** | 인시던트 MTTC | Mean Time To Contain | MTTC ≤ 4시간 (NIST CSF) |
| **사용자 만족** | CSAT / NPS | 설문 5점 척도 / -100~+100 | CSAT ≥ 4.2, NPS ≥ 30 |
| **거버넌스 성숙도** | Process Capability | COBIT PAM 0~5 | 목표 Level 3(Defined) -> 4(Managed) |

- **📢 섹션 요약 비유**: COBIT의 5개 도메인은 **병원 시스템**과 같다. **EDM은 이사회/원장**, **APO는 진료계획실(진료과 배정, 자원), BAI는 시술/수술실(실제 구축), DSS는 병동/응급실(일상 운영), MEA는 QI(Quality Improvement)팀**이다. 환자(비즈니스 요구)가 오면 Plan(APO) -> Build(BAI) -> Operate(DSS) -> Check(MEA)의 흐름으로 진료가 진행된다.

---

## Ⅲ. 비교 및 연결

### 1. 주요 IT 관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스/관리 목표 통합 | 서비스 운영/가치 창출 | 거버넌스 6원칙 | 프로세스 성숙도 | EA 방법론 |
| **개발 주체** | ISACA (2019) | AXELOS (2019) | ISO/IEC (2015) | CMMI Institute (v2.0) | The Open Group (2022) |
| **핵심 구조** | 40 Objectives ×
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 651 / 800

<- **이전**: [650. IT 경영 관리 핵심 토픽 650번 시험 요약](/studynote/12_it_management/05_security_compliance/650_it_management_core_topic_650_exam_summary/)
**다음**: [652. IT 경영 관리 핵심 토픽 652번 시험 요약](/studynote/12_it_management/05_security_compliance/652_it_management_core_topic_652_exam_summary/) ->

---
