+++
title = "706. IT 경영 관리 핵심 토픽 706번 시험 요약 (IT Management Core Topic 706 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 706. IT 경영 관리 핵심 토픽 706번 시험 요약 (IT Management Core Topic 706 Exam Summary)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019의 40개 Governance/Management Objective, ITIL 4의 34개 Practice, ISO/IEC 38500의 6원칙(Principle)**을 기반으로 IT-Business Alignment를 실현하는 통합 거버넌스 체계이며, Board->Executive->Management->Operational의 4계층 의사결정 구조를 통해 **Evaluate-Direct-Monitor(EDM) 사이클**로 통제 책임을 분산한다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 **IT 투자 ROI 20~35% 향상**(Gartner 2024), **인시던트 MTTR 40% 단축**, **규제 준수 비용 25% 절감**, **프로젝트 성공률 28%->72% 개선**(PMI 2023) 등의 정량적 효과를 거두며, ESG·정보보호법·개인정보보호법 등 컴플라이언스 리스크를 사전 차단한다.
> 3. **판단 포인트**: 중앙집중형(Centralized, COBIT RACI 모델) vs 분산형(Federated, DevOps 거버넌스) 간의 **Trade-off**, **Zero Trust vs 경계 기반 보안** 모델 선택, **Build vs Buy vs Rent(클라우드)** 의사결정의 TCO(3~5년) 산정, 그리고 **Agile 거버넌스 vs Plan-based 거버넌스**의 조직 문화 적합성 평가가 핵심 설계 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대에 기업 전체 예산의 **5~15%**를 차지하는 IT 투자가 전략적 가치를 창출하지 못하는 **"IT-Business Gap"** 현상이 심화되면서, IT를 단순 비용(Cost Center)이 아닌 **가치 창출 엔진(Value Driver)**으로 전환할 수 있는 통합 관리 체계의 필요성이 대두되었다. 한국 정보화진흥원(NIA)의 「2024 디지털 전환 실태조사」에 따르면 국내 대기업의 **67%가 IT-Business 정렬도(Strategic Alignment Index)를 5점 만점 중 3점 이하**로 자평하고 있으며, CIO 역할의 **42%**가 "전략적 리더"가 아닌 "운영 관리자"로 머물러 있다.

전통적 IT 관리(1990~2010, **Mainframe->Client/Server 시대**)는 **Silo별 독립 예산, 프로젝트 중심 투자, ITIL v2의 프로세스 중심(Service Desk->Incident->Problem->Change)** 체계를 따랐으나, **Cloud·AI·DevOps·Data Platform** 중심의 디지털 시대에서는 다음과 같은 한계가 드러났다.

| 패러다임 | 전통적 IT 관리 (2000년대) | 디지털 시대 IT 경영 관리 (2020년대~) |
| :--- | :--- | :--- |
| **관점** | IT = 비용(Cost) | IT = 전략 자산(Strategic Asset) |
| **구조** | 기능별 수직 사일로 | 플랫폼 기반 수평 통합 |
| **투자 기준** | ROI(재무적 회수기간) | VOI(Value of Investment) + TCO + NPV + 전략적 옵션가치 |
| **관리 방식** | 프로젝트 단위(Waterfall) | 제품/플랫폼 단위(Agile, Product-centric) |
| **리스크 관리** | 사후 통제(Detection) | 사전 예방(Prevention, Zero Trust) |
| **컴플라이언스** | 국내법 중심 | 글로벌 규제(GDPR, DORA, AI Act, ESG) |
| **평가 체계** | Balanced Scorecard(4관점) | OKR + BSC + COBIT Performance Mgmt + Value Stream Metrics |

2024년 기준 국내 IT 경영 관리의 핵심 규범은 **전자정부법, 개인정보보호법(PIPA), 정보통신망법, 클라우드컴퓨팅법, AI기본법(2026.1 시행)**이며, 글로벌 표준은 **ISO/IEC 38500(거버넌스), ISO/IEC 20000(서비스), ISO/IEC 27001(보안), ISO/IEC 42001(AI경영)**로 통합 추세이다.

```text
+------------------------------------------------------------------+
|            IT 경영 관리 4계층 의사결정 구조 (EDM Cycle)         |
+------------------------------------------------------------------+

  +-------------------------------------------------------------+
  |  L1: Board of Directors / 이사회                             |
  |   - IT 거버넌스 최고 의사결정 (책임: Director Liability)      |
  |   - 연간 IT 예산 승인, CIO 임명, 리스크 appetite 설정        |
  +------------------------+------------------------------------+
                           |  Report
                           v
  +-------------------------------------------------------------+
  |  L2: Executive (C-level) — CIO, CFO, CEO, CDO, CISO         |
  |   - IT Strategy 수립, Portfolio Prioritization              |
  |   - EDM 중 "Direct" 단계 수행 (전략적 방향성 제시)            |
  |   - Steering Committee 운영 (월 1회)                          |
  +------------------------+------------------------------------+
                           |  Cascading
                           v
  +-------------------------------------------------------------+
  |  L3: Management — IT 부서장, PMO, Architecture Office       |
  |   - COBIT 2019의 40 Governance/Management Objective 실행     |
  |   - EDM 중 "Monitor" 단계 수행 (KPI/SLA 측정)                |
  |   - Portfolio Mgmt, Resource Mgmt, Vendor Mgmt              |
  +------------------------+------------------------------------+
                           |  Operation
                           v
  +-------------------------------------------------------------+
  |  L4: Operational — DevOps Team, SRE, Service Desk, BA        |
  |   - ITIL 4의 34개 Practice 실행                              |
  |   - EDM 중 "Evaluate" 단계 데이터 생산                        |
  |   - Incident/Request/Change/Problem 실제 처리                 |
  +-------------------------------------------------------------+

  ※ EDM = Evaluate(평가) -> Direct(지시) -> Monitor(모니터링) 순환
     ISO/IEC 38500의 6원칙: Responsibility, Strategy, Acquisition,
     Performance, Conformance, Human Behavior
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **비행기의 자동조종장치(Autopilot) + 기장(CIO) + 관제탑(이사회)**이 합쳐진 시스템과 같다. 자동조종장치(거버넌스 프레임워크)가 비행 상태를 계속 측정(Evaluate)하고, 관제탑(Board)이 항로(전략)를 지시(Direct)하며, 기장(CIO)이 모니터링(Monitor)하며 조종간을 미세 조정하는 것이 EDM 사이클이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 기술적 핵심은 **① 전략-투자-운영-평가의 4단계 Value Loop**, **② 5대 거버넌스 컴포넌트**, **③ 메트릭 계층 구조**로 구성된다. ISO/IEC 38500:2024의 **3-tier 모델(Governance-Management-Operational)**과 COBIT 2019의 **Cascade Goals(연계 목표)** 메커니즘이 이론적 기반이며, 실제 구현 시에는 **RACI 매트릭스(Responsible, Accountable, Consulted, Informed)**로 역할과 책임을 분배한다.

```text
+------------------------------------------------------------------+
|         IT 경영 관리 5대 거버넌스 컴포넌트 아키텍처              |
+------------------------------------------------------------------+

   +-------------------------------------------------------+
   |  ① IT Strategy & Governance (전략 거버넌스)            |
   |  - ISO 38500 EDM Cycle, COBIT 2019 EDM Domain          |
   |  - 3-Year IT Roadmap, Capability Assessment (CMMI 2.0)|
   |  - Output: IT Strategy Map (BSC 4관점)                  |
   +---------------------+---------------------------------+
                         |  Translate
                         v
   +-------------------------------------------------------+
   |  ② IT Portfolio & Investment Management (투자관리)     |
   |  - Run/Grow/Transform 분류 (60/25/15 원칙)             |
   |  - NPV, IRR, Payback, Real Options Valuation           |
   |  - 프로젝트 우선순위 매트릭스 (Strategic Impact × Risk) |
   +---------------------+---------------------------------+
                         |  Allocate
                         v
   +-------------------------------------------------------+
   |  ③ IT Service & Operation Management (서비스 운영)     |
   |  - ITIL 4 Service Value System (SVS)                   |
   |  - 34 Practices (Change, Incident, Problem, SLA...)   |
   |  - Service Desk, CMDB, Knowledge Mgmt                   |
   +---------------------+---------------------------------+
                         |  Measure
                         v
   +-------------------------------------------------------+
   |  ④ IT Risk & Compliance Management (리스크·컴플라이언스)|
   |  - ISO 27001 ISMS, NIST CSF 2.0, PIPA/DPDP/GDPR       |
   |  - Risk = Threat × Vulnerability × Impact (ALE=SLE×ARO)|
   |  - K-Risk (KISA), nDepth (NIA) 활용                    |
   +---------------------+---------------------------------+
                         |  Feedback
                         v
   +-------------------------------------------------------+
   |  ⑤ Performance & Value Management (성과·가치 평가)     |
   |  - BSC 4관점(재무/고객/내부/학습성장) + OKR             |
   |  - COBIT Performance Management (Process capability)  |
   |  - KPI: IT ROI, TCO, VOI, NPS, MTTR, SLA Compliance   |
   +-------------------------------------------------------+

   ※ Value Loop: ①->②->③->④->⑤->① (연속 순환)
   ※ Cascade Goals: 기업 BSC -> IT BSC -> Process KPI -> 개인 OKR
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee** | 전략적 의사결정, 포트폴리오 승인 | 월 1회 정례회의, **RACI 매트릭스**상 Accountable, 의사결정 권한 80% 보유, 의사결정 시간 5일 SLA |
| **PMO (Project Management Office)** | 프로젝트 실행 통제, 표준화 | **PPM 도구**(Planview, ServiceNow PPM, MS Project Online) 활용, Gate Review(Initiation->Planning->Execution->Closing 4단계), Earned Value Mgmt(EVM, **CPI>0.95, SPI>0.95** 유지) |
| **EA (Enterprise Architecture)** | 업무-데이터-응용-기술 4계층 정렬 | **TOGAF 10 ADM(Architecture Development Method)** 8단계 적용, **ArchiMate 3.2** 모델링, Gap Analysis + Target State Roadmap |
| **Service Desk / SRE** | IT 서비스 운영, 인시던트 대응 | **ITIL 4 Incident Mgmt** 프로세스(P1: 15분 대응/4시간 복구, P2: 1시간/8시간), **SRE SLO/SLI** 기반(99.9% Availability, Error Budget), ChatOps(Slack/Mattermost) 통합 |
| **CISO / ISMS** | 정보보호 거버넌스, 컴플라이언스 | **ISO 27001:2022 Annex A 93 통제항목**, **NIST CSF 2.0**(6 Function: Govern, Identify, Protect, Detect, Respond, Recover), **Zero Trust Architecture**(NIST SP 800-207, mTLS + SDP) |
| **BI / Data Office** | 데이터 기반 의사결정, 가치 측정 | **데이터 거버넌스**(DAMA DMBOK 2.0 11 지식영역), **Data Mesh/Data Fabric**, Master Data Mgmt, Data Quality Score(**정확도>98%, 완전성>95%**) |
| **Vendor / Sourcing Mgmt** | 외부 파트너 관리, 아웃소싱 통제 | **Kraljic Portfolio Matrix**(Strategic/Leverage/Bottleneck/Non-critical), **Multi-sourcing 70-20-10 원칙**, SLA + 손해배상 조항, Exit Strategy 필수 |

**핵심 메트릭 산출 공식 및 기준선** (기술사 출제 빈도 높음):

- **IT ROI** = (IT 투자로 인한 편익 − IT 투자 비용) / IT 투자 비용 × 100 -> 우수 기준 **> 25%**
- **TCO (Total Cost of Ownership)** = 직접비(HW/SW/인건비) + 간접비(교육/다운타임/통합) -> **3~5년 누적**, Gartner TCO 모델 활용
- **Risk = ALE (Annual Loss Expectancy)** = SLE(Single Loss Expectancy) × ARO(Annual Rate of Occurrence) -> **1년 예상 손실액**
- **MTTR (Mean Time To Repair)** = Σ(복구시간) / 인시던트 수 -> 우수 **< 30분**, 보통 < 4시간
- **MTBF (Mean Time Between Failures)** = 총 운영시간 / 장애 횟수 -> 우수 **> 720시간(30일)**
- **Process Capability (CMMI/COBIT)** = Level 1(Initial) ~ Level 5(Optimizing) -> 목표 **Level 3 이상**
- **SLA Compliance** = (SLA 충족 횟수 / 전체 SLA 적용 횟수) × 100 -> 목표 **> 99.5%**
- **Cascade Efficiency** = (전략 목표 연계 KPI 수 / 전체 KPI 수) × 100 -> 목표 **> 70%**

```text
+------------------------------------------------------------------+
|     IT 거버넌스 프레임워크 3대 표준 연계 구조                    |
+------------------------------------------------------------------+

        +----------------------+
        |  ISO/IEC 38500:2024  |  <- 거버넌스 원칙(WHY/WHO)
        |  (IT Governance)     |     6원칙, EDM Model
        |   Evaluate/Direct/   |
        |      Monitor         |
        +----------+-----------+
                   |  Provides principles to
                   v
        +----------------------+
        |   COBIT 2019         |  <- 거버넌스 시스템(HOW-WHAT)
        |  (Framework)         |     40 Governance/Management
        |   5 Domains          |     Objective + 7 Components
        |  EDM/APR/BAI/DSS/MEA |
        +----------+-----------+
                   |  Operationalized by
                   v
        +----------------------+
        |   ITIL 4 (2019~
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 706 / 800

<- **이전**: [705. IT 경영 관리 핵심 토픽 705번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/705_it_management_core_topic_705_exam_summary/)
**다음**: [707. IT 경영 관리 핵심 토픽 707번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/707_it_management_core_topic_707_exam_summary/) ->

---
