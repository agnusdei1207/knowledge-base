+++
title = "650. IT 경영 관리 핵심 토픽 650번 시험 요약 (IT Management Core Topic 650 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(650번)는 IT 거버넌스(COBIT 2019), IT 전략 기획(BSC, Porter 5 Forces), EA(TOGAF/ArchiMate), ITSM(ITIL 4), 프로젝트 관리(PMBOK 7th/Agile), 정보보안 거버넌스(ISO 27001), 컴플라이언스(개인정보보호법, ISMS-P), 그리고 디지털 전환(DX) 전 과정을 통합적으로 다루는 메타-관리 프레임워크의 총합이다.
> 2. **가치**: 효과적 IT 경영 체계 구축 시 ROI 200~400% 향상, IT 비용의 매출 대비 비중(영업비율) 2~5%p 절감, 시스템 장애 downtime 60~80% 감소, Time-to-Market 40~50% 단축, 그리고 ISO 27001/ISMS-P/ISMS-C 인증을 통한 컴플라이언스 위반 리스크를 70% 이상 저감한다.
> 3. **판단 포인트**: Build vs Buy(자체 개발 vs 솔루션 도입), On-Premise vs Cloud(공공/금융 규제 환경의 데이터 주권), Waterfall vs Agile(프로젝트 성격과 규제 강도에 따른 방법론), 중앙 집중형 vs 분산형 거버넌스(Matrix 조직의 RACI 설계), 그리고 CapEx vs OpEx(클라우드 전환 시 재무제표 영향)의 트레이드오프가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(IT Management) 기술사 650번은 정보시스템의 기획부터 폐기까지(E2E: End-to-End) 전 생애주기(Lifecycle)를 **거버넌스·전략·아키텍처·운영·보안·컴플라이언스** 6개 축으로 통합 관리하는 메타-관리 역량을 평가한다. 과거 1990년대 말~2000년대 초의 IT 관리는 단순히 데이터센터 운영과 ERP 도입에 집중했으나, 현재는 **클라우드 네이티브, AI/ML 기반 의사결정, Zero-Trust 보안, ESG 대응**이라는 새로운 패러다임 위에서 재정의되어야 한다.

2024년 기준 국내 정보화 사업 예산은 약 23조 원(2023년 21.4조 대비 7.5% 증가) 규모이며, 이 중 약 32%가 신규 시스템 구축, 41%가 운영·유지보수, 18%가 정보보안, 9%가 디지털 전환 사업으로 편성된다. 그러나 한국정보화진흥원(KIAT)의 「2023년 공공 정보화 사업 실태조사」에 따르면, 전체 정보화 사업의 **42.3%가 요구사항 정의 단계에서 이미 예산·일정 초과 징후**를 보이며, 최종 완료 시점에는 평균 **초기 예산 대비 167%, 초기 일정 대비 234%**가 초과된다. 이는 체계적 거버넌스 부재로 인한 구조적 실패 패턴이다.

```text
+---------------------------------------------------------------------+
|         IT 경영 관리 6대 축 (650번 토픽 통합 프레임워크)              |
+---------------------------------------------------------------------+
|                                                                     |
|   +----------+  +----------+  +----------+  +----------+           |
|   | Governance|  | Strategy |  |   EA     |  |  ITSM    |           |
|   |  거버넌스  |  |  전략기획 |  | 아키텍처 |  |  서비스   |           |
|   | COBIT'19 |  | BSC/5F   |  | TOGAF ADM|  | ITIL 4   |           |
|   +-----+----+  +----+-----+  +----+-----+  +----+-----+           |
|         |            |             |             |                  |
|         +------------+------+------+-------------+                  |
|                             |                                       |
|                  +----------+----------+                            |
|                  |   IT Steering       | <- 의사결정 정점             |
|                  |   Committee(ISC)    |                            |
|                  +----------+----------+                            |
|                             |                                       |
|         +-------------------+-------------------+                   |
|         |                   |                   |                   |
|   +-----+-----+      +-----+-----+      +-----+-----+             |
|   |  Security |      | Compliance|      |   Project  |             |
|   |   보안    |      | 컴플라이언스|      |    관리    |             |
|   | ISO27001 |      | 개인정보법  |      | PMBOK 7   |             |
|   | Zero-Trust|      | ISMS-P/C  |      | Agile/Dev |             |
|   +----------+      +----------+      +----------+                 |
|                                                                     |
|  <--- 6대 축 통합 관리가 650번의 핵심 평가 영역 --->                   |
+---------------------------------------------------------------------+
```

**왜 필요한가?**

| 시대 | IT 관리 패러다임 | 한계점 | 650번의 대응 |
| :--- | :--- | :--- | :--- |
| 1990s | **데이터센터 운영 중심** (Mainframe -> Client-Server) | 비용·장애 대응 위주, 비즈니스 연계 부재 | ITIL v1 도입, Help Desk 체계화 |
| 2000s | **프로세스 혁신·ERP** (SAP R/3, Oracle EBS) | 부서별 silos, 프로젝트 실패 多 (Standish 1994 CHAOS Report) | PMBOK, BSC 기반 성과관리 |
| 2010s | **클라우드·모바일·빅데이터** (SMAC) | Shadow IT, 보안사고 급증, 거버넌스 부재 | COBIT 5, ISO 38500, ISMS-P |
| 2020s~ | **AI/DX/Zero-Trust/ESG** | 기술 부채(Technical Debt), 규제 복잡성, AI 윤리 | COBIT 2019, ITIL 4, ITIL CSI, EA 참조모델(정부) |
| 2025s+ | **AI-Native IT 운영, Agentic AI, 양자 보안** | AI 거버넌스, 신기술 위험, 탄소배출 측정 | AI 거버넌스, Green IT, Post-Quantum Crypto |

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 종합 행정 체계**와 같다. 거버넌스는 헌법(법·제도), 전략은 도시계획(20년 마스터플랜), 아키텍처는 토지이용계획(높이·용도), ITSM은 상하수도·도로 운영, 보안은 경찰·소방, 컴플라이언스는 환경규제·건축허가에 각각 대응한다. 이 중 하나라도 빈틈이 있으면 도시 전체가 마비된다(예: 2017년 SK C&C 정전 사고, 2023년 카카오 장애).

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 650번의 핵심 아키텍처는 **3계층 거버넌스 모델**(Strategic-Tactical-Operational)을 기반으로, 4개의 핵심 메커니즘(의사결정·평가·조정·보고)이 작동하는 구조다.

```text
+----------------------------------------------------------------------+
|          IT 경영 관리 3계층 아키텍처 (S-T-O Hierarchy)                |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+      |
|  |  TIER 1: 전략 계층 (Strategic Layer)                        |      |
|  |  · IT Steering Committee (ISC) - CIO/CDO/CTO + 사업본부장   |      |
|  |  · 역할: 중장기 IT 로드맵(3~5년), 예산 총량, 투자우선순위    |      |
|  |  · 도구: BSC, Porter 5F, BCG Matrix, Wardley Maps           |      |
|  |  · 주기: 분기 1회 + 수시 (임원 회의)                         |      |
|  +------------------------+-----------------------------------+      |
|                           |  v KPI 전파 (BSC 4관점)                  |
|  +------------------------+-----------------------------------+      |
|  |  TIER 2: 전술 계층 (Tactical Layer)                         |      |
|  |  · IT-PMO, EA 팀, 정보보안실, 거버넌스·컴플라이언스 팀      |      |
|  |  · 역할: 아키텍처 표준, 프로젝트 포트폴리오 관리, 정책수립   |      |
|  |  · 도구: TOGAF ADM, ArchiMate 3.2, COBIT 2019, ISO 27001   |      |
|  |  · 주기: 월 1회 + 수시 (심의위원회)                          |      |
|  +------------------------+-----------------------------------+      |
|                           |  v SLA/OLA 전파                          |
|  +------------------------+-----------------------------------+      |
|  |  TIER 3: 운영 계층 (Operational Layer)                      |      |
|  |  · 인프라팀, 개발팀, 운영팀, 보안관제(SOC), 서비스데스크     |      |
|  |  · 역할: 시스템 운영, 장애 대응, 변경관리, 사용자 지원      |      |
|  |  · 도구: ITIL 4 Service Value Chain, ServiceNow, Jira       |      |
|  |  · 주기: 일/주 단위 (War Room) + 24x7 (L1/L2/L3)            |      |
|  +------------------------------------------------------------+      |
|                                                                      |
|  <- 4대 핵심 메커니즘: 의사결정(Decide) -> 평가(Evaluate) ->            |
|                       조정(Align) -> 보고(Report) ->                    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (거버넌스·관리 목표)** | IT 거버넌스 프레임워크의 de-facto 표준. **40개 거버넌스·관리 목표(EDM: 5, Align/Plan/Organize: 14, Build/Acquire/Implement: 11, Deliver/Service/Support: 6, Monitor/Evaluate/Assess: 4)**로 구성. | **Cascade Goals 메커니즘**: 기업 KPI -> IT KPI -> 프로세스 KPI -> 활동 KPI의 4단계 연쇄 매핑. Maturity Level(0~5) + Capability Level(0~5) 평가. ISO/IEC 38500(거버넌스 원칙: 책임, 전략, 인수, 성과, 적합, 인간행동)을 내부에 통합. |
| **TOGAF ADM (아키텍처 개발 방법론)** | 엔터프라이즈 아키텍처 개발의 국제 표준. **8단계 ADM 사이클**(Preliminary -> A: Vision -> B: Business -> C: Data/Application -> D: Technology -> E: Opportunities -> F: Migration -> G: Implementation -> H: Change Management). | **Architecture Repository**(Architecture Landscape, Standards, Reference Models, Patterns) + **ADM Cycle**(Phase A~H)의 반복적(Iterative) 수행. **ArchiMate 3.2** 표기법: Business Layer(워크플로우·서비스), Application Layer(컴포넌트·인터페이스), Technology Layer(노드·장비)의 3계층 + Strategy/Physical 2개 추가. |
| **ITIL 4 (서비스 가치 시스템)** | IT 서비스 관리의 글로벌 표준. **34개 관리 실무(Practice)** + **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support)의 6개 액티비티. | **4 Dimensions Model**(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes) 기반 운영. SLA(서비스수준협약) 99.9% = 월 43분, 99.99% = 월 4.3분, 99.999% = 월 26초 다운타임 허용. |
| **BSC & KPI 시스템** | IT 성과 측정의 4관점 프레임워크: **재무/고객/내부프로세스/학습·성장**. | Strategy Map(인과관계 맵) + Balanced Scorecard(성과지표) + Initiatives(과제)의 3요소. KPI SMART 원칙(Specific, Measurable, Achievable, Relevant, Time-bound). IT 프로젝트 성공률 측정: 품질·일정·예산·ROI 4축. |
| **PMBOK 7th & Agile** | 프로젝트 관리의 2대 축. PMBOK은 **8개 성과영역**(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) + **12가지 원칙**. | **Predictive(Waterfall)** vs **Adaptive(Agile: Scrum, SAFe, LeSS)** 접근. 하이브리드: **Hybrid-Agile**(Wagile). IT 프로젝트 성격별 적용: 신규 구축=Predictive, 고도화/유지보수=Agile, 데이터 마이그레이션=Predictive+Agile. |
| **ISO 27001/ISMS-P** | 정보보안 경영시스템(ISMS) 인증. **Annex A 93개 통제항목**(2022년新版)을 4개 영역(Organizational: 37, People: 8, Physical: 14, Technological: 34)으로 분류. | **Plan-Do-Check-Act(PDCA)**: ISMS 수립(위험평가·처리계획) -> 실행(통제 구현) -> 모니터링(내부감사·경영검토) -> 개선(시정조치). ISMS-P(공공): 64개 필수 통제(전자금융 16 + 개인정보 47 + 시스템 1). ISMS-C(클라우드): 74개 통제. |
| **컴플라이언스 체계** | 법적 요구사항 준수 체계. 주요 법률: **개인정보보호법**(2023.9 개정: 가명정보 도입, 영상정보 30일->60일 보관), 정보통신망법, 전자금융거래법, 클라우드컴퓨팅법, AI기본법(2025.1 시행예정), EU AI Act, GDPR. | **RoPA(Record of Processing Activities)**: 개인정보 처리활동 기록·관리. **DPIA(데이터영향평가)**: 고위험 처리 시 의무. **GDPR 7대 원칙**: 합법성·공정성·투명성, 목적제한, 데이터최소화, 정확성, 저장제한, 무결성·기밀성, 책임성. |
| **EA 참조모델(한국)** | 정부·공공 EA 표준. **표준프레임워크**(업무/데이터/응용/기술/보안/인프라 6개 영역) + **EA-View**(현황As-Is/목표To-Be/전환Transition) + **아키텍처 산출물 9종**. | **국가 EA(NEIS)**: 디지털정부서비스·공공데이터·공공 클라우드. **정부24, 정부데이터셋, 공공데이터포털, KS X 6701, 6702, 6703** 등 표준 준수. |

**핵심 운영 메커니즘의 의사결정 흐름 (예: 신규 시스템 도입 결정 시)**

```text
+-----------------------------------------------------------------+
|  Step 1. 비즈니스 요구사항 (Business Case)                        |
|   +- ROI 분석: NPV(순현재가치), IRR(내부수익률), Payback Period  |
|   |   · NPV = Σ(CF_t / (1+r)^t) - 초기투자비                     |
|   |   · IRR: NPV=0이 되는 할인율, 일반적 기준: WACC+5%p 이상     |
|   |   · Payback: 투자금 회수까지 소요 기간 (3년 이내 권고)         |
|   |   · TCO(총소유비용): 초기 30% + 운영 60% + 폐기 10%           |
|   +- 정성 효과: 경쟁력, 고객만족, 컴플라이언스, 리스크 저감         |
|                          v                                        |
|  Step 2. 아키텍처 적합성 평가 (EA Review)                          |
|   +- 표준 적합성: 정부 EA 참조모델·표준프레임워크 준수 여부       |
|   +- 재사용성: 기존 컴포넌트 활용률 30%^ 권고 (TDR 30^)          |
|   +- 상호운용성: 표준 API(REST/
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 650 / 800

<- **이전**: [649. IT 경영 관리 핵심 토픽 649번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/649_it_management_core_topic_649_exam_summary/)
**다음**: [651. IT 경영 관리 핵심 토픽 651번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/651_it_management_core_topic_651_exam_summary/) ->

---
