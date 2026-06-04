---
title: "647. IT 경영 관리 핵심 토픽 647번 시험 요약 (IT Management Core Topic 647 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 거버넌스 프레임워크를 통해 **전략(Strategy) -> 아키텍처(Architecture) -> 포트폴리오(Portfolio) -> 운영(Operation) -> 가치(Value)** 의 Value Governance Chain을 구현하고, BSC(Balanced Scorecard)와 KPI 트리 구조로 전략-전술-운영을 연동하는 경영 과학이다.
> 2. **가치**: 성숙도 모델 기반 Gap Analysis 수행 시 평균 **23~35%의 IT 비용 절감**(Gartner 2023), EA 기반 중복 투자 제거로 **TCO 18~27% 감소**, ITIL 도입으로 **MTTR 40~60% 단축**, COBIT 통제 항목 100% 매핑 시 **컴플라이언스 감사 소요 시간 70% 절감** 효과를 기대할 수 있다.
> 3. **판단 포인트**: 중앙집중식(COE) vs 분산식(Federated) 거버넌스 모델, Build vs Buy vs Rent 의사결정 프레임워크, Run-the-Business(60~70%) vs Change-the-Business(20~30%) vs Grow-the-Business(5~10%) IT 예산 배분 비율, 그리고 사이버보안 위험과 비즈니스 민첩성(Business Agility) 간의 Trade-off가 핵심 설계 변수이다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 관리는 1990년대까지 **Cost Center**(비용 센터) 관점에서 "최소 비용으로 시스템 운영"에 초점을 맞추었다. 그러나 2000년대 이후 비즈니스 환경이 VUCA(Volatility, Uncertainty, Complexity, Ambiguity)로 전환되면서, IT는 단순 지원 기능을 넘어 **Business Value Creator**로 격상되어야 한다는 요구가 제기되었다. 2020년대에는 디지털 트랜스포메이션(DX), 생성형 AI(GenAI), ESG(Environmental, Social, Governance) 컴플라이언스, 그리고 데이터 주권(Data Sovereignty) 이슈가 IT 경영의 핵심 어젠다로 부상했다.

특히 한국 환경에서는 **전자정부법**, **클라우드컴퓨팅법**, **개인정보보호법(PIPA)**, **정보통신망법**, **AI 기본법(2026년 시행 예정)** 등 다양한 규제 하에서 IT 거버넌스를 설계해야 하므로, 글로벌 프레임워크를 그대로 도입하는 것이 아니라 **Regulatory Mapping**을 통한 한국형 IT 경영 체계 구축이 필수적이다.

기술사 시험에서는 단순히 COBIT이나 ITIL의 정의적 이해가 아니라, **"A 기업은 이러이러한 IT 문제를 겪고 있다. 어떤 프레임워크를 어떤 순서로 적용할 것인가? 자원 배분과 위험 통제는 어떻게 할 것인가?"** 와 같은 케이스 기반 응용 문제가 출제된다.

```text
[ IT 경영 관리 Value Governance Chain ]

  +-------------------------------------------------------------+
  |  Strategy Layer (전략 계층)                                  |
  |  +-------------+  +--------------+  +-----------------+    |
  |  | Business    |  | IT Strategy  |  | Digital         |    |
  |  | Vision/Mission|-| Alignment   |-| Transformation  |    |
  |  | (BV/BM)     |  | (SAM, BSP)   |  | Roadmap (DX)    |    |
  |  +-------------+  +--------------+  +-----------------+    |
  +------------------------+------------------------------------+
                           | Cascade (연결)
  +------------------------+------------------------------------+
  |  Architecture Layer (아키텍처 계층)                          |
  |  +-------------+  +--------------+  +-----------------+    |
  |  | EA (TOGAF)  |  | Solution     |  | Technology      |    |
  |  | ADM Cycle   |-| Architecture |-| Reference Model |    |
  |  | B/D/A/T     |  | (SA)         |  | (TRM)           |    |
  |  +-------------+  +--------------+  +-----------------+    |
  +------------------------+------------------------------------+
                           | Trace (추적)
  +------------------------+------------------------------------+
  |  Portfolio Layer (포트폴리오 계층)                          |
  |  +-------------+  +--------------+  +-----------------+    |
  |  | Demand      |  | Investment   |  | Risk &          |    |
  |  | Management  |-| Prioritization|-| Compliance      |    |
  |  | (DMM)       |  | (NPV, IRR)   |  | (ISO 27001)     |    |
  |  +-------------+  +--------------+  +-----------------+    |
  +------------------------+------------------------------------+
                           | Operate (운영)
  +------------------------+------------------------------------+
  |  Operation Layer (운영 계층)                                 |
  |  +-------------+  +--------------+  +-----------------+    |
  |  | Service     |  | Incident/    |  | SLA/OLA/UC      |    |
  |  | Desk (ITIL4)|-| Problem Mgmt |-| (Service Level) |    |
  |  +-------------+  +--------------+  +-----------------+    |
  +------------------------+------------------------------------+
                           | Measure (측정)
  +------------------------+------------------------------------+
  |  Value Layer (가치 계층)                                    |
  |  +-------------+  +--------------+  +-----------------+    |
  |  | Benefits    |  | KPI / OKR    |  | Realized Value  |    |
  |  | Realization |-| Scorecard    |-| (BSC 4 Perspective)|  |
  |  | (BRM)       |  | (BSC)        |  |                 |    |
  |  +-------------+  +--------------+  +-----------------+    |
  +-------------------------------------------------------------+
```

**구 시대(Old Paradigm) vs 신 시대(New Paradigm) 비교**

| 관점 | Old Paradigm (1990~2010) | New Paradigm (2015~현재) |
|---|---|---|
| IT 인식 | Cost Center, Back Office | Business Partner, Value Creator |
| 거버넌스 | 컴플라이언스 중심 통제 | 가치 중심(Benefits Realization) |
| 아키텍처 | 모놀리식(On-Premise) | 하이브리드/멀티클라우드 |
| 투자 결정 | 3년 단위 Capex 일회성 | Agile Portfolio, 지속적 OpEx |
| 위험 관리 | 사후 대응(Reactive) | 제로 트러스트, 선제적(Proactive) |
| 조직 모델 | 기능별(Silo) 조직 | Product/Platform Team, SRE |
| 측정 | 시스템 가용률(%) | NPS, CX, Time-to-Market |
| 규제 대응 | 개별 법규 대응 | 통합 GRC(Governance·Risk·Compliance) |

- **📢 섹션 요약 비유**: IT 경영 관리를 **배의 항해**에 비유하면, **비전은 목적지(Strategy)**, **EA는 해도(Architecture)**, **포트폴리오는 화물 적재 계획(Investment)**, **운영은 기관실(Operation)**, **가치 평가는 도착지의 성과(Value)** 입니다. 어느 하나라도 어긋나면 배는 목적지에 도달하지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **"전략의 연결(Strategic Alignment)"** 입니다. Henderson & Venkatraman(1993)의 **SAM(Strategic Alignment Model)** 은 4개 영역(Business Strategy, IT Strategy, Organizational Infrastructure, IS Infrastructure) 간의 **Cross-Mapping Fit**을 강조하며, 이를 **Strategic Fit + Functional Integration**의 2차원 매트릭스로 표현합니다.

현대 IT 경영에서는 이 SAM을 확장하여 **SAM+ 4.0** (Luftman & Zadeh, 2011) 형태로, **Agility, Flexibility, Modularity, Interoperability** 의 4대 IT 역량을 Business Strategy의 Dynamism(역동성)과 매핑합니다.

```text
[ COBIT 2019 Governance & Management Objectives 체계 ]

  +------------------------------------------------------------+
  |  EDM (Evaluate, Direct, Monitor) - 거버넌스 5개 영역       |
  |  +------------------------------------------------------+  |
  |  | EDM01 - 거버넌스 프레임워크 설정 및 유지              |  |
  |  | EDM02 - Benefits Delivery 보장                        |  |
  |  | EDM03 - Risk Optimization 보장                        |  |
  |  | EDM04 - Resource Optimization 보장                    |  |
  |  | EDM05 - Stakeholder Transparency 보장                 |  |
  |  +------------------------------------------------------+  |
  +------------------------+-----------------------------------+
                           | 40 Governance & Management Objectives
  +------------------------+-----------------------------------+
  |  Align, Plan, Organize (APO) - 14개 관리 실무              |
  |  APO01~14: 관리 프레임워크, 전략, 아키텍처, 혁신, 포트폴리오|
  |             예산, 인간자원, 관계, 합의, 공급자, 품질, 위험  |
  |             보안, 데이터                                      |
  +------------------------------------------------------------+
  |  Build, Acquire, Implement (BAI) - 11개 관리 실무           |
  |  BAI01~11: 관리 프로그램, 요구사항 정의, 솔루션 식별/구축,  |
  |             가용성/용량, 조직 변경, 변경, 변경 수락/전환,   |
  |             지식, 자산, 구성, 프로젝트                        |
  +------------------------------------------------------------+
  |  Deliver, Service, Support (DSS) - 6개 관리 실무            |
  |  DSS01~06: 운영, 서비스 요청/사고, 문제, 연속성,             |
  |             보안 서비스, 비즈니스 통제                        |
  +------------------------------------------------------------+
  |  Monitor, Evaluate, Assess (MEA) - 4개 관리 실무            |
  |  MEA01~04: 성과/규제 준수/통제 시스템/목표 모니터링         |
  +------------------------------------------------------------+
       |
       v
  +------------------------------------------------------------+
  |  Components: 7가지(원리, 정책, 프로세스, 조직구조, 문화,    |
  |  정보, 사람/기술/시설) × 40목표 = 280개 통제 포인트         |
  +------------------------------------------------------------+
       |
       v
  +------------------------------------------------------------+
  |  Focus Area: 산업/규제별 맞춤(예: DevOps, Risks,        |
  |  Compliance, Information Security, Digital Transformation) |
  +------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 시스템(Governance System)** | 이사회-경영진-IT의 3계층 의사결정 구조 정의 | COBIT 2019의 EDM->APO->BAI->DSS->MEA 5개 도메인, RACI 매트릭스 적용 |
| **전략 연동 메커니즘(Alignment Engine)** | BV/BS(Business Vision/Strategy)와 IT Strategy의 양방향 매핑 | SAM(Sam-Zhang 모델), BSP(Business Scenario Planning), PESTEL 분석, SWOT-Cross 매트릭스 |
| **아키텍처 프레임워크(EA Framework)** | Business-Data-Application-Technology 4계층 일관성 보장 | TOGAF ADM 8단계(Phase A~H: Architecture Vision, Business/Information/Technology Architecture, Opportunities/Solutions, Migration Planning, Implementation Governance, Architecture Change Management) + Zachman 6×6 매트릭스 |
| **포트폴리오 관리(Portfolio Mgmt)** | 투자 의사결정 및 자원 배분의 최적화 | PCM(Priority/Capacity Model): 80/20 Pareto, WSJF(Weighted Shortest Job First), RICE(Reach/Impact/Confidence/Effort), NPV/IRR 계산, FinOps(클라우드 비용 가시화) |
| **성과 측정 체계(Performance Mgmt)** | BSC 4관점(재무/고객/내부/학습성장)의 KPI 도출 | Cascading Scorecard: BSC -> Strategy Map -> Initiative -> KPI -> Target -> Actual, 4CX(Cause-Effect Chain), OKR(Quarter 단위) |
| **위험 및 컴플라이언스(GRC)** | 위험 식별-평가-대응-모니터링의 PDCA | ISO 31000(리스크 매니지먼트), ISO 27001(ISMS), NIST CSF 2.0(Identify/Protect/Detect/Respond/Recover + Govern), 한국 ISMS-P 인증 |
| **IT 서비스 운영(ITSMOps)** | 서비스 수명주기 관리 및 SLA 준수 | ITIL 4 Service Value System(SVS): Opportunity/Demand->Value->Service Value Chain(Plan/Engage/Design&Transition/Obtain/Build/Deliver&Support)->Value |

**핵심 알고리즘 및 의사결정 공식**

```text
[ IT 투자 우선순위 산정 공식 (예시) ]
---------------------------------------------------------
1. NPV (Net Present Value):
   NPV = Σ [ CFt / (1+r)^t ] - C0
   (CFt: t년도 현금흐름, r: 할인율(가중평균자본비용 WACC), C0: 초기투자)

2. IRR (Internal Rate of Return):
   NPV = 0 이 되는 r을 역산 (일반적으로 r > WACC일 때 투자 승인)

3. TCO (Total Cost of Ownership) - Gartner 5-Layer Model:
   TCO = (HW + SW + NW) + (설치) + (운영) + (지원) + (사용자 생산성 손실)
        + (잔존가치 회수)

4. Payback Period:
   BP = 초기투자 / 연평균 현금흐름 (보통 3~5년 이내면 우선)

5. IT 포트폴리오 위험 조정 수익률:
   Sharpe-IT Ratio = (R_portfolio - R_riskfree) / σ_portfolio
---------------------------------------------------------
[ BSC 4관점 KPI 예시 ]
- 재무: IT 비용/매출 비율(%), CapEx 회수 기간
- 고객: CX-IT 만족도(NPS), 서비스 요청 해결률(%), 가용률(99.9% SLA)
- 내부 프로세스: MTTR, MTBF, Change Failure Rate, Deployment Frequency
- 학습/성장: 직원 인증률, 혁신 프로젝트 수, Retention Rate
```

- **📢 섹션 요약 비유**: 이 아키텍처를 **의료 시스템**에 비유하면, **COBIT은 해부학 교과서(전신 구조)**, **TOGAF는 X-ray/CT(MRI 영상으로 뼈와 장기 확인)**, **ITIL은 응급실/입원/퇴원 절차 매뉴얼**, **BSC는 건강검진 결과표(KPI)**, **ISO 27001은 감염 관리 매뉴얼**입니다. 환자의 상태(기업 상황)에 따라 어떤 검사를 어떤 순서로 할지 판단하는 것이 **기술사의 역할**입니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** |
| :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스 및 관리(Governance & Management) | IT 서비스 관리(Service Management) | IT 거버넌스 원칙(Governance Principles) |
| **관점** | What(어떤 목표/통제?) | How(어떻게 서비스 운영?) | Why(왜 거버넌스가 필요한가?) |
| **구조** | EDM + 4개 도메인(APO/BAI/DSS/MEA), 40개 목표 | SVS(Service Value System), 34개 Practice | 6가지 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) |
| **적용 계층** | 이사회/경영진 -> IT 전 부서 | ITSM 실무자/서비스 운영팀 | 이사회/경영진 |
| **성숙도 측정** | CMMI 5단계, PAM(Process Assessment Model) | ITIL Maturity Model | 자체 자가진단 체크리스트 |
| **강점** | 컴플라이언스 매핑,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 647 / 800

<- **이전**: [646. IT 경영 관리 핵심 토픽 646번 시험 요약](/studynote/12_it_management/05_security_compliance/646_it_management_core_topic_646_exam_summary/)
**다음**: [648. IT 경영 관리 핵심 토픽 648번 시험 요약](/studynote/12_it_management/05_security_compliance/648_it_management_core_topic_648_exam_summary/) ->

---
