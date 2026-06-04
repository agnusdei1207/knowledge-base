---
title: "725. IT 경영 관리 핵심 토픽 725번 시험 요약 (IT Management Core Topic 725 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, PMBOK 7th, TOGAF 10 등 글로벌 프레임워크를 기반으로 **IT-Business Alignment(전략적 정렬)** 와 **Value Realization(가치 실현)** 을 체계화하여, IT를 비용 중심의 지원 기능에서 **기업의 경쟁우위 창출 엔진**으로 전환하는 통합 거버넌스 체계이다.
> 2. **가치**: McKinsey 보고에 따르면 디지털 성숙도 상위 25% 기업은 수익성 2.6배, 영업마진 1.8배, EBITDA 1.7배 향상을 달성하며, EA 기반의 이니셔티브 포트폴리오 관리는 ROI를 평균 23% 개선하고 IT 투자 실패율(전통 30~40%)을 5% 이하로 축소한다.
> 3. **판단 포인트**: Balanced Scorecard(BSC)의 4관점(재무/고객/내부/학습성장) × COBIT 2019의 40개 Governance/Management Objective × ITIL 4의 34개 Practice를 **조직의 성숙도와 산업 특성(Banking, Manufacturing, Public)** 에 맞춰 적절히 커스터마이징하는 것이 핵심이며, 잦은 프레임워크 혼용(Framework Sprawl) 안티패턴 회피가 관건이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 기업 내 역할은 1960년대 IBM의 MIS(Mainframe 기반 데이터 처리) -> 1980년대 전략적 정보시스템(SIS, MIS->SIS 패러다임 전환) -> 2000년대 Web 2.0과 SaaS 기반 업무혁신(BPM) -> 2020년대 AI·클라우드 기반 **Digital Business Platform** 으로 진화했다. 그러나 한국정보화진흥원의 조사에 따르면 국내 대기업 IT 예산의 **약 65%가 운영/유지보수(OpEx)** 에 편중되어 혁신 투자(NEW/NewNEW) 비중이 15% 미만으로, **"Innovation Deficit(혁신 적자)"** 현상이 심화되고 있다. 이러한 문제를 해결하기 위해 1992년 Strassmann이 제안한 **"Information Productivity"** 개념, 1993년 Henderson & Venkatraman의 **Strategic Alignment Model(Strategy-Organization-IT 간 4영역 정렬)** , 그리고 ISACA의 **COBIT 2019** 등 IT 경영 관리 프레임워크가 등장했다.

```text
   [기업 전략(Business Strategy)]
        |
        | ① Strategic Alignment (정렬)
        v
   +------------------------------+
   |   IT 거버넌스(Governance)    |  <- COBIT 2019, ISO 38500
   |   - 원칙/구조/프로세스       |     "Value Creation" 6단계
   +--------------+---------------+
                  | ② Portfolio Mgmt
                  v
   +------------------------------+
   | IT 전략기획(Planning)         | <- BSC, EA(TOGAF), 투자우선순위
   | - As-Is / To-Be Gap Analysis |    APQC Process Classification
   +--------------+---------------+
                  | ③ 실행(Execution)
                  v
   +------------------------------+
   | IT 운영 및 서비스 관리        | <- ITIL 4, DevOps, SRE, AIOps
   | - 변경·장애·문제·사고 관리   |    SLA/OLA/UC
   +--------------+---------------+
                  | ④ 성과측정(Measurement)
                  v
   +------------------------------+
   | 성과/위험 모니터링 & 개선     | <- KPI, CSF, KRI, Risk Register
   | (Continuous Improvement)     |    PDCA -> Lean Six Sigma
   +------------------------------+
                  |
                  v
        [Feedback Loop -> 다시 ①로]
```

기존 IT 관리 패러다임(전통적 SI 중심)과 새로운 IT 경영관리 패러다임(플랫폼·생태계 중심)의 차이는 다음과 같다: 전통적 방식은 **프로젝트 단위**의 일회성(One-off) 납품, TCO 미고려, 사용자 부서와의 수직적 관계, CAPEX(자본) 중심 예산 편성이었으나, 현대적 IT 경영관리는 **서비스 단위의 지속적 가치 창출(Continuous Value Delivery)**, TCO·TVO(Total Value of Ownership)·ROO(Return on Objectives) 다차원 평가, 거버넌스 기반 의사결정 정렬(Strategy->Portfolio->Project->Operation), 그리고 CAPEX/OPEX 유연 조합(클라우드 전환 시 OPEX 70% 이상) 으로 전환되었다. 한국정보통신기술협회(TTA)의 KC스마트워커스 표준, 전자정부 프레임워크, 그리고 **클라우드컴퓨팅법(2021.10 시행)** 이 이를 제도적으로 뒷받침한다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라의 지휘자** 와 같다. 여러 악기(애플리케이션, 인프라, 데이터, 인력, 프로세스) 가 각자 자기 소리만 내면 카오스가 되듯, IT 자산들을 COBIT의 **5지배 원칙(Evaluate, Direct, Monitor + 합의된 목표 + 위험 최적화 + 자원 최적화 + 성과 모니터링)** 으로 조율해야 비로소 하나의 **가치 있는 교향곡(Value Symphony)** 이 연주된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 국제적으로 통용되는 **4대 프레임워크(COBIT·ITIL·PMBOK·TOGAF)** 와 이를 관통하는 **BSC, GRC(Governance-Risk-Compliance), EA(Enterprise Architecture)** 의 3개 횡단 레이어로 구성된다. 한국 공공부문은 전자정부법(제50조의2, 정보화사업 관리), 정보시스템 구축·운영 지침, 그리고 디지털정부혁신 추진계획(매년 범부처)에 따라 자체 거버넌스 체계를 운용한다.

```text
[최상위] Business Strategy & Governance
   |
   +-- (1) 전략 정렬: Henderson-Venkatraman Strategic Alignment Model
   |        +------------+    +------------+
   |        |  Business  |◄--►|     IT     |
   |        |  Strategy  |    |  Strategy  |
   |        +------------+    +------------+
   |              |                  |
   |              v                  v
   |        +------------+    +------------+
   |        | Organization|◄--►|Information |
   |        |   Infra    |    |  Infra/IS  |
   |        +------------+    +------------+
   |
   +-- (2) 거버넌스 프레임워크: COBIT 2019 (40 G/O)
   |        +-- EDM(5) + Align/Plan/Org(4) + Build/Acquire/Implement(5)
   |            + Deliver/Service/Support(6) + Monitor/Evaluate/Assess(4) + Focus Area(40)
   |
   +-- (3) 서비스 관리: ITIL 4 Service Value System (SVS)
   |        +-- Opportunity/Demand -> Value
   |        +-- Guiding Principles(7), Governance(4), Practices(34)
   |        +-- Service Value Chain(Plan->Engage->Design->Obtain->Build->
   |        |   Test->Transition->Operate->Deliver/Support)
   |        +-- Continual Improvement(Model 7-step)
   |
   +-- (4) 프로젝트 관리: PMBOK 7th (8 Domains + 12 Principles)
   |        +-- Integration, Scope, Schedule, Cost, Quality, Resource,
   |        |   Communications, Risk, Procurement, Stakeholder
   |        +-- Tailoring -> 5 Project Approaches (Predictive, Hybrid, Agile, etc.)
   |
   +-- (5) EA: TOGAF 10 (ADM 8 Phases)
            Preliminary -> Vision -> Business Architecture -> Information Systems
            Architecture -> Technology Architecture -> Opportunities&Solutions ->
            Migration Planning -> Implementation Governance -> Change Management
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스의 "What" 정의 | ISACA의 40개 Governance/Management Objective, 7개 컴포넌트(Process/Structure/People/Skills/Information/Service/Technology), 5개 Focus Area(예: 사이버보안, DevOps, 디지털전환), **Cascade Goals(13개 연쇄 목표)** 로 비즈니스 KPI와 IT KPI 연결 |
| **ITIL 4** | IT 서비스 관리의 "How" 정의 | 34개 Practice(General Mgmt 14, Service Mgmt 17, Technical Mgmt 3), **Four Dimensions of Service Mgmt**(Organization & People, Information & Technology, Partners & Suppliers, Value Streams & Processes), Service Value Chain 6 Activity로 구성 |
| **PMBOK 7th** | 프로젝트 관리의 방법론 | 8개 Project Performance Domain(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty), 12개 Principle 기반의 **Tailoring** 강조, 5가지 개발접근법(Predictive/Adaptive/Hybrid) |
| **TOGAF 10** | EA 수립 및 정렬 | ADM(Architecture Development Method) 8단계 사이클, **ArchiMate 3.2** 표준 모델링 언어, Business/Application/Data/Technology 4계층, 재무·공공·통신·금융 등 7개 Reference Model |
| **Balanced Scorecard (BSC)** | 성과측정 4관점 | 재무/고객/내부프로세스/학습성장 4관점의 KPI, **Strategy Map(원인-결과 인과지도)** , Kaplan-Norton 모델(1992), 한국 300대 기업 60% 이상 도입 |
| **GRC(Governance-Risk-Compliance)** | 위험·규제 통합관리 | ISO 31000(Risk), ISO 27001(Security), ISO 37301(Compliance), **OCEG GRC Capability Model(Principled Performance)** , 통합 RCM(Risk Control Matrix) 운용 |

핵심 메커니즘은 **"Strategy -> Portfolio -> Project -> Operation -> Value"** 의 Value Chain 이다. 예를 들어 삼성SDS의 Neプラットフォーム, 네이버의 하이퍼클로버X, LG CNS의 DAP(데이터 애널리틱스 플랫폼) 사례에서 공통적으로 발견되는 것은 ①BSC 상위 KPI 도출 -> ②EA To-Be 모델 -> ③COBIT 2019의 EDM(Evaluate-Direct-Monitor) 사이클 -> ④투자 우선순위 매트릭스(Net Present Value 5억 원 이상, Strategic Fit High, Risk Medium 이상) -> ⑤PMO(Project Management Office) 통한 통합 관리 -> ⑥ITIL Change Enablement 통한 안정적 운영 -> ⑦KPI Dashboard(예: 서비스 가용성 99.95%, MTTR 30분 이내, CSAT 4.5/5) 으로의 폐루프이다. 특히 PMBOK 7th의 **8가지 Project Performance Domain** 중 "Delivery" 와 "Measurement" 도메인이 Value Realization의 핵심으로, Earned Value Management(EVM: CPI, SPI, EAC, ETC, VAC) 지표를 통해 프로젝트 성과를 **정량적** 으로 추적한다.

- **📢 섹션 요약 비유**: 4대 프레임워크는 마치 **자동차의 4륜구동 시스템** 과 같다. COBIT은 **스티어링 휠(방향, 거버넌스)**, ITIL은 **엔진과 변속기(서비스 운영)**, PMBOK은 **서스펜션과 바퀴(프로젝트 실행)**, TOGAF는 **섀시 프레임(전체 구조)** 다. 어느 하나만 강화하면 코너링에서 차체가 기울어지듯, 4개를 균형 있게 통합 운용해야 안정적인 Value Delivery가 가능하다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역의 주요 프레임워크와 개념 비교는 기술사 시험의 단골 출제 영역이다. 특히 COBIT 2019 vs ITIL 4, PMBOK vs PRINCE2, BSC vs OKR, EA vs Solution Architecture의 비교가 핵심이다.

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7th | PRINCE2 7 |
| :--- | :--- | :--- | :--- | :--- |
| **관리 대상 (What)** | IT 전반의 거버넌스(전략/리스크) | IT 서비스 운영(서비스 라이프사이클) | 프로젝트 단위(일회성 산출물) | 프로젝트 단위(프로젝트 거버넌스) |
| **주 발행처** | ISACA(미국) | AXELOS(Cabinet Office UK) | PMI(미국) | AXELOS(Cabinet Office UK) |
| **구성 요소** | 40 G/O, 7 Component, 5 Focus Area | 34 Practice, 4 Dimension, SVS | 8 Domain, 12 Principle, 5 Approach | 7 Principle, 7 Process, 7 Theme |
| **성숙도 모델** | 없음(단, CMMI 연계 가능) | ITIL Maturity Model | OPM3(5단계 600+ Practice) | P2M3(5단계) |
| **적용 범위** | 엔터프라이즈 전체(E2E) | IT 서비스 부서(Service Desk -> 운영) | 프로젝트 단위(Start -> End) | 프로젝트 단위(Start -> End) |
| **가치 측정** | Cascade Goals(13개) | Value Stream + Co-Creation | EVM, Benefit Realization | Business Case + Benefits Review |
| **도입 난이도** | 중(상) - 거버넌스 위원회 필수 | 중 - 기존 ITSM 역량 활용 | 하 - Process Group 단위 학습 | 중 - 7 Process + 7 Theme 학습 |
| **한국 공공 적용** | 전자정부 EA, 정부24 연계 | SI/SM 운영지침 | 정보화사업 PMO 표준 가이드 | 일부 글로벌 기업 |

**EA vs Solution Architecture** 의 차이: EA(Enterprise Architecture)는 **엔터프라이즈 전체(LOB 다수)** 의 전략적 정렬과 표준화(As-Is / To-Be / Transition)를 다루며 TOGAF, Zachman Framework(6x6 매트릭스: What/How/Where/Who/When/Why × Scope/Business/Information/Technology 등) 을 사용한다. 반면 **Solution Architecture** 는 **특정 솔루션/프로젝트 단위** 의 기술 설계를 다루며, C4 Model(Context/Container/Component/Code), UML, AWS Well-Architected Framework 등을 사용한다. EA는 **"왜 만들 것인가(Why)"** 에 집중하고, Solution Architecture는 **"어떻게 만들 것인가(How)"** 에 집중한다고 구분할 수 있다.

**BSC vs OKR** 비교: BSC는 1년 단위의 전략 KPI(3~5개), 재무적 측정 강조, Top-Down, 무관용 평가에 강하며 대규모 조직(국가공공·금융)에 적합하다. OKR은 1분기 단위, 60~70% 달성률이 좋은 결과(Stretch Goal), Bottom-Up, 공개형이며 Google, Intel 등 혁신 조직에 적합하다. 최근 Netflix, Spotify 등은 **"Outcomes over Outputs"** 원칙으로 OKR을 부분 도입하고, **Hybrid(BSC + OKR)** 도活跃히 사용된다.

다른 시스템 컴포넌트와의 통합 관점에서 IT 경영관리는: ① **ERP(SAP S/4HANA, Oracle Cloud ERP)** 와의 통합 - BSC KPI의 재무 데이터를 ERP에서 실시간 추출, ② **BPM(Business Process Management, Appian·Pega·Camunda)** 와의 통합 - 프로세스
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 725 / 800

<- **이전**: [724. IT 경영 관리 핵심 토픽 724번 시험 요약](/studynote/12_it_management/05_security_compliance/724_it_management_core_topic_724_exam_summary/)
**다음**: [726. IT 경영 관리 핵심 토픽 726번 시험 요약](/studynote/12_it_management/05_security_compliance/726_it_management_core_topic_726_exam_summary/) ->

---
