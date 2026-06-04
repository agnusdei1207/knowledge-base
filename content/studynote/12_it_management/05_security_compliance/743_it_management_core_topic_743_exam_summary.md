+++
title = "743. IT 경영 관리 핵심 토픽 743번 시험 요약 (IT Management Core Topic 743 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019의 40개 Governance/Management Objective와 5개 도메인(EDM, APO, BAI, DSS, MEA)을 기반으로, IT 전략(Strategy) ↔ 포트폴리오(Portfolio) ↔ 프로그램(Program) ↔ 프로젝트(Project) ↔ 운영(Operation)의 5계층 가치사슬(Value Chain)을 정량적 목표(EGM cascade)로 종속연결(Cascade)하여 기업 거버넌스(EG)와 정렬(Alignment)시키는 체계이다.
> 2. **가치**: McKinsey & Company(2023) 조사에 따르면成熟的 IT 거버넌스 체계 도입 기업은 DX 프로젝트 성공률 67%(전체 평균 32%), TCO 28% 절감, Time-to-Market 41% 단축, IT 투자 ROI 평균 4.7배(미도입 기업 1.9배) 효과를 달성하며, ISO/IEC 38500 기반 의사결정 프레임워크 적용 시 이사회-경영진 간 IT 리스크 인지 격차(Score Gap)를 평균 38% 축소한다.
> 3. **판단 포인트**: 중앙집권형(Centralized, COBIT 5 Enabler 기반) vs 연방형(Federated, COBIT 2019 Focus Area 기반) 거버넌스 모델 선택, BSC 4관점(재무/고객/내부/학습성장) ↔ COBIT 13개 Enterprise Goal 간 매핑(Mapping) 가중치(Weight) 결정, Agile(WIP Limit 5±2) vs Plan-driven(Phase Gate) vs Hybrid(Scaled Agile SAFe 6.0) 개발방법론 채택, 그리고 국내 정보화진흥법·전자정부법·개인정보보호법 3대 법령과 글로벌 ISMS-P·ISO 27001·SOX 404의 Dual Compliance 설계가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

한국 정보화 환경은 2024년 기준 정보화진흥법 개정(2023.6. 시행) 및 인공지능 발전법(안) 논의, 클라우드 컴퓨팅 발전 및 이용자 보호에 관한 법률(클라우드 이용자 보호법, 2024.1. 시행) 등으로 급격한 규제 환경 변화에 직면해 있다. 공공부문 연간 정보화 사업 예산은 약 8.4조 원(2024년 디지털정부 품질관리 시행계획, 행정안전부), 민간부문은 금융권 IT투자 약 12조 원(금융감독원 IT투자 통계) 규모로 GDP 대비 약 4.8%에 달한다. 그러나 한국정보화진흥원(KAIT) 「2023 정보시스템 감리 결과 분석」에 따르면 전체 정보화 사업의 약 34.7%가 사업비 증액(평균 27.3% 증액), 약 22.1%가 사업기간 연기로 종료되어 **성공률(Success Rate) 43.2%**에 그치고 있다(세계 평균 McKinsey 기준 32% 대비 우위이나 글로벌 Top Quartile 75% 대비 현격한 격차).

이러한 문제의 본질은 (1) IT-Business Alignment 부재로 인한 전략 부적합(Strategic Misfit), (2) PMO 부재 또는 권한 미약으로 인한 프로젝트 통제 실패, (3) KPI 미정의 및 측정체계 부재로 인한 정량적 의사결정 불가, (4) Risk/Infrastructure 미관리로 인한 운영 중단(예: 2023.11. 금융권 IDC 화재, 약 612억 원 피해), (5) Shadow IT 및 Citizen Developer 증가(Forrester 2024, 평균 35% 증가)에 따른 통제 공백(Control Gap) 등이다. 기술사 입장에서 IT 경영 관리는 단순한 비용 관리가 아니라 **IT 자산을 기업의 전략적 자원으로 전환시키는 Value Realization Mechanism**으로 정의해야 한다.

```text
+----------------------------------------------------------------------------+
|         IT 경영 관리 5계층 프레임워크 (IT Management 5-Layer Framework)    |
+----------------------------------------------------------------------------+
|                                                                            |
|   [Layer 1] IT 거버넌스 (Governance) — "무엇을, 왜(Why) 할 것인가"        |
|      +----------------------------------------------------------+          |
|      |  - ISO/IEC 38500:2015 (6 Principles: Responsibility,     |          |
|      |    Strategy, Acquisition, Performance, Conformance,      |          |
|      |    Human Behavior)                                       |          |
|      |  - COBIT 2019 (40 Governance/Management Objectives)      |          |
|      |  - Board of Directors -> CEO -> CIO -> IT Steering Com.    |          |
|      +----------------------------------------------------------+          |
|                                  |                                         |
|                                  v (Cascade & Alignment)                   |
|   [Layer 2] IT 전략 및 포트폴리오 (Strategy & Portfolio)                  |
|      +----------------------------------------------------------+          |
|      |  - Enterprise Goal 13개(EG01~EG13) ↔ IT Goal 13개(IG01   |          |
|      |    ~IG13) Goal Cascade                                    |          |
|      |  - Portfolio Mgmt: Demand -> Evaluate -> Prioritize ->      |          |
|      |    Optimize (5단계, 4-quadrant BCG Matrix)                |          |
|      |  - IT-BSC 4관점 + ESG 5관점 통합 (6P Map)                |          |
|      +----------------------------------------------------------+          |
|                                  |                                         |
|                                  v (Roadmap & Funding)                    |
|   [Layer 3] 프로그램/프로젝트 관리 (Program/Project)                      |
|      +----------------------------------------------------------+          |
|      |  - PMBOK 7th (8 Performance Domains, 12 Principles)     |          |
|      |  - PRINCE2 2023 (7 Principles, 7 Themes/Practices)       |          |
|      |  - Scaled Agile SAFe 6.0 (4 Configurations, 7 Core       |          |
|      |    Values, 9 Course)                                      |          |
|      |  - 한국 정보화사업관리 5단계 (계획->분석->설계->구축->운영)  |          |
|      +----------------------------------------------------------+          |
|                                  |                                         |
|                                  v (Service Transition)                    |
|   [Layer 4] IT 서비스 운영 (IT Service Operation)                          |
|      +----------------------------------------------------------+          |
|      |  - ITIL 4 Service Value System (SVS): Opportunity/Demand|          |
|      |    -> Value -> Guiding Principles(7) -> Governance->Service  |          |
|      |    Value Chain(6 Activity) -> Continual Improvement       |          |
|      |  - 34 Practices (General Mgmt 14, Service Mgmt 17,       |          |
|      |    Technical Mgmt 3)                                      |          |
|      |  - SLM: SLA 99.9%(3 nines) / 99.95%(2.5)/ 99.99%(4)     |          |
|      +----------------------------------------------------------+          |
|                                  |                                         |
|                                  v (Measure, Monitor, Audit)               |
|   [Layer 5] IT 품질·리스크·컴플라이언스 (Quality/Risk/Compliance)          |
|      +----------------------------------------------------------+          |
|      |  - CMMI 2.0 (5 Level, 20 Practice Area)                 |          |
|      |  - ISO 9001:2015 + ISO/IEC 20000-1:2018                 |          |
|      |  - ISO 27001:2022(Annex A 93 Control) + ISMS-P          |          |
|      |  - ISO 31000:2018 Risk Mgmt Process(6단계)              |          |
|      |  - ESG(TCFD, GRI Standards) + Privacy(PIPL, GDPR)        |          |
|      +----------------------------------------------------------+          |
|                                                                            |
+----------------------------------------------------------------------------+
```

기존 패러다임(1980~2000년대)에서는 IT가 **Cost Center**(비용 센터)로 인식되어 CapEx 위주의 예산 통제와 프로젝트별 사후 감리에 집중했다. 그러나 2010년 이후 디지털 전환과 4차 산업혁명(AI, BigData, Cloud, IoT, 5G) 흐름 속에서 IT는 **Strategic Asset & Value Driver**로 격상되었고, 2020년대 이후에는 AI·데이터 중심 경제로의 전환(예: 생성형 AI 시장 규모 CAGR 36.6%, IDC 2024 예측)에 따라 IT 경영의 초점이 **Risk-adjusted Value Optimization**(위험조정 가치 최적화)과 **Sustainable Digital Ecosystem**(지속가능 디지털 생태계) 조성으로 이동하고 있다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 종합건설계획(Urban Master Plan)**과 같다. 개별 빌딩(프로젝트)만 잘 지어서는 안 되고, 교통(서비스), 안전(리스크), 환경(ESG), 재정(Budget), 시민 만족도(BSC)이라는 다층적 관점에서 도시 전체(엔터프라이즈)를 바라보는 전략이 필요하며, COBIT은 도시 기본계획, ITIL은 상하수도 운영 매뉴얼, PMBOK은 건축공정표, ISO 38500은 도시 헌장(Charter)에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. COBIT 2019 Governance System 상세 아키텍처

COBIT 2019는 ISACA(Information Systems Audit and Control Association)가 2018년 12월 발표한 차세대 거버넌스 프레임워크로, 이전 버전 COBIT 5(2012)와 달리 **40개 Governance/Management Objective(GMO)**를 **5개 도메인**으로 재구성하고, **Design Factors**(설계 인자)와 **Focus Areas**(집중 영역) 개념을 도입하여 기업별 맞춤형 거버넌스 시스템 설계를 가능하게 했다. 핵심 구성요소는 다음과 같다.

```text
+------------------------------------------------------------------------------+
|        COBIT 2019 Governance & Management Objectives (40개) — 도메인 매핑    |
+------------------------------------------------------------------------------+
|                                                                              |
|   +--- EDM (Evaluate, Direct, Monitor) — 거버넌 의사결정 (5개) ---+        |
|   |  EDM01 Governance Framework Setting & Maintenance            |        |
|   |  EDM02 Benefits Delivery (가치 실현)                          |        |
|   |  EDM03 Risk Optimization (리스크 최적화)                      |        |
|   |  EDM04 Resource Optimization (자원 최적화)                    |        |
|   |  EDM05 Stakeholder Transparency (이해관계자 투명성)           |        |
|   +------------------------------------------------------------+        |
|                              <-> (상호연결: RACI Matrix)                    |
|   +--- APO (Align, Plan, Organize) — 계획·조직 (14개) -------------+        |
|   |  APO01 Mgt Framework | APO02 Strategy | APO03 Enterprise Arch|        |
|   |  APO04 Innovation    | APO05 Portfolio| APO06 Budget & Cost  |        |
|   |  APO07 HR Mgmt       | APO08 Relations| APO09 Service Agree  |        |
|   |  APO10 Suppliers     | APO11 Quality  | APO12 Risk Mgmt      |        |
|   |  APO13 Security Mgmt | APO14 Data Mgmt                         |        |
|   +------------------------------------------------------------+        |
|                              <->                                              |
|   +--- BAI (Build, Acquire, Implement) — 구축·도입 (11개) --------+        |
|   |  BAI01 Mgt Programs| BAI02 Reqmts Mgmt| BAI03 Solutions Id |        |
|   |  BAI04 Availability & Capacity | BAI05 Org Change | BAI06 Changes| |
|   |  BAI07 IM Transition | BAI08 Knowledge | BAI09 Assets | BAI10 Config| |
|   |  BAI11 Projects Mgmt                                             |        |
|   +------------------------------------------------------------+        |
|                              <->                                              |
|   +--- DSS (Deliver, Service, Support) — 인도·지원 (6개) ----------+        |
|   |  DSS01 Operations| DSS02 Service Requests| DSS03 Incidents  |        |
|   |  DSS04 Continuity| DSS05 Security Services| DSS06 Bus Process|        |
|   |     Ctl                                                              |        |
|   +------------------------------------------------------------+        |
|                              <->                                              |
|   +--- MEA (Monitor, Evaluate, Assess) — 모니터·평가 (4개) ---------+        |
|   |  MEA01 Performance & Conformance| MEA02 Sytem of Internal Ctl|        |
|   |  MEA03 Compliance w/ External Reqmts| MEA04 Assurance        |        |
|   +------------------------------------------------------------+        |
|                                                                              |
|   [Design Factors 11개]                                                      |
|   DF1 Strategy|DF2 Goals|DF3 Risk|DF4 I&T Issues|DF5 Threat|DF6 Compliance||
|   DF7 Role of IT|DF8 IT Sourcing|DF9 IT Methods|DF10 Tech|DF11 Adoption|  |
|                                                                              |
|   [Focus Areas 예] Custom, DevOps, Digital Transformation, ESG, GRC,        |
|                    Risk, Cybersecurity, Cloud, AI, Privacy, BCM            |
+------------------------------------------------------------------------------+
```

### 나. Goal Cascade(목표 계단식 연결) 메커니즘

COBIT 2019의 가장 중요한 운영 원리는 **Goal Cascade**다. 기업의 **13개 Enterprise Goal(EG01~EG13)**과 IT의 **13개 IT-related Goal(IG01~IG13)**이, 그리고 **40개 GMO**가 일대일·다대다(M:N) 관계로 매핑되어 있다. 각 매핑에는 **S(Strong, 주연결)**, **P(Primary, 핵심)**, **L(Less Important, 부수적)** 등급이 부여되며, 이를 통해 **Traceability Matrix**(추적성 매트릭스)가 자동 생성된다.

| 구분 | 매핑 대상 | 가중치(Weight) | 예시 |
| :--- | :--- | :--- | :--- |
| **EG-IG Cascade** | EG01(포트폴리오 경쟁제품/서비스) -> IG01(기업IT준거) | S=3, P=2, L=1 | Score 9 =
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 743 / 800

<- **이전**: [742. IT 경영 관리 핵심 토픽 742번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/742_it_management_core_topic_742_exam_summary/)
**다음**: [744. IT 경영 관리 핵심 토픽 744번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/744_it_management_core_topic_744_exam_summary/) ->

---
