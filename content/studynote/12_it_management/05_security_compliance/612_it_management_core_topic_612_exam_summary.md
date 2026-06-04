+++
title = "612. IT 경영 관리 핵심 토픽 612번 시험 요약 (IT Management Core Topic 612 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019, ITIL 4, ISO/IEC 38500, TOGAF** 4대 글로벌 프레임워크를 통합적으로 운용하여, **거버넌스(Governance)->관리(Management)->운영(Operations)** 의 3계층 책임구조에서 **가치(Value) 창출·위험(Risk) 최적화·자원(Resource) 효율성** 의 균형을 달성하는 경영학문입니다.
> 2. **가치**: 성숙도 Level 3 이상 도달 시 IT 투자 대비 ROI **20~35% 향상**, 계획 대비 예산 편차 **±5% 이내**, 중대 IT 장애 **MTTR 60% 단축**, 감사 적발 사항 **70% 감소**, 그리고 디지털 전환(DX) 프로젝트 성공률 **35% -> 75%** 수준으로 개선됩니다.
> 3. **판단 포인트**: 사업-IT 정렬(Business-IT Alignment)도, 거버넌스 모델(집중형 vs 분산형 vs 하이브리드), 투자 우선순위 결정 모델(Financial/Strategic/Compliance 포트폴리오), 그리고 EA·ITSM·PMP·ISMS 인증 여부 및 통합 수준이 핵심 의사결정 변수이며, **"표준 채택"이 아닌 "목표 상태(To-Be) 역설계"** 가 합격 포인트입니다.

---

## Ⅰ. 개요 및 필요성

정보시스템을 단순한 **비용센터(Cost Center)** 에서 **전략적 가치창출 센터(Value Center)** 로 전환하기 위해서는, 사업 전략과 IT 역량을 연결하는 통합적 관리 체계가 필수적입니다. 한국 정보관리기술사(기술사) 612번 계열 시험은 이러한 IT 경영 관리의 **프레임워크 선정·거버넌스 구조·성과측정·리스크 최적화** 능력을 측정합니다.

```text
+--------------------------------------------------------------------+
|            IT 경영 관리 4대 글로벌 프레임워크 통합 구조             |
+--------------------------------------------------------------------+
|                                                                    |
|   [사업 전략 / Business Strategy]                                  |
|      |   미션·비전·목표 (예: 2026 매출 1조, 신사업 30%)            |
|      v                                                             |
|   +--------------------------------------------+                   |
|   | ① ISO/IEC 38500 (거버넌스 원칙 6대)        | <--- 최상위 책임  |
|   |   Responsibility, Strategy, Acquisition,   |     (이사회/경영진)|
|   |   Performance, Conformance, Human Behavior |                   |
|   +--------------------------------------------+                   |
|      |            |             |                                  |
|      v            v             v                                  |
|   +----------+ +----------+ +----------+                           |
|   |COBIT 2019| |  TOGAF   | |  ITIL 4  |                           |
|   |(관리/통제)| |(아키텍처)| |(서비스)  |                           |
|   |40개 관리 | |ADM 8단계| |SVS 34개  |                           |
|   |목표     | |(A~H)     | |실무     |                           |
|   +----------+ +----------+ +----------+                           |
|      |            |             |                                  |
|      v            v             v                                  |
|   +------------------------------------+                          |
|   | PMBOK 7th / PRINCE2 / ISO 21500   | <--- 프로젝트 단위 실행 |
|   | (프로젝트 관리)                     |                          |
|   +------------------------------------+                          |
|      |                                                             |
|      v                                                             |
|   [운영: ITSM, DevOps, SRE, AIOps, Zero-Trust]                    |
|                                                                    |
+--------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | 전통적 IT 관리 (1980~2000) | 현대 IT 경영 관리 (2020~) |
|:---|:---|:---|
| **관점** | IT = 비용, 백오피스 지원 기능 | IT = 사업 혁신·신성장 동력 |
| **구조** | CIO 1인 의사결정, 사일로 조직 | **삼중 거버넌스(Two-tier)** — 전략위원회+IT운영위원회+프로젝트실무 |
| **측정** | 예산 집행률, 가동률(Uptime) | **BSC 4관점(재무/고객/프로세스/학습)** + OKR, NPS, TCO |
| **투자** | CapEx 중심 일회성 | **CapEx + OpEx 하이브리드**(FinOps, Pay-as-you-go) |
| **위험** | 사후 대응(Reactive) | **GRC 통합**(Governance·Risk·Compliance), Zero-Trust |
| **아키텍처** | 모놀리식(On-Prem) | 하이브리드·멀티클라우드, SaaS + IaaS + PaaS |
| **방법론** | Waterfall | **Agile + DevSecOps + SAFe** 대규모 확장 |
| **컴플라이언스** | 내부 통제 | **ISO 27001, ISMS-P, GDPR, ESG, CSAP** 다중 인증 |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라 지휘자** 와 같습니다. 첼리스트(개발팀), 바이올리니스트(운영팀), 타악기(인프라팀) 각자가 최고로 잘 연주해도, **지휘자(거버넌스)** 없이는 **합주곡(사업 가치)** 이 만들어지지 않습니다. COBIT은 악보, TOGAF는 공연장 설계도, ITIL은 리허설 규칙, ISO 38500은 공연 윤리강령입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"평판시스템의 3계층 (Strategy -> Governance -> Operation)"** 이며, 각 계층은 명확한 의사결정 권한·KPI·보고체계를 가집니다.

```text
+--------------------------------------------------------------+
|         IT 경영 관리 3계층 의사결정·보고 구조 (RACI 기반)     |
+--------------------------------------------------------------+
|                                                              |
|  +---- Tier 1: 전략·거버넌스 계층 (이사회·경영진) ----+      |
|  |  [IT전략위원회]  의장: CEO, 위원: CIO·CFO·CDO·CSO|      |
|  |  +- 의사결정: R(Responsible)                      |      |
|  |  +- 보고주기: 분기 1회 (BSC 대시보드)              |      |
|  |  +- KPI: IT-Business Alignment, TCO, ROIC, NPV  |      |
|  |  +- 산출물: IT 전략맵(Strategy Map)               |      |
|  |  |             정책/표준/원칙 (Policy/Standard)   |      |
|  |  +- 프레임워크: ISO 38500, COBIT 2019 EDM Domain  |      |
|  +----------------------------------------------------+      |
|                          ^ 보고                              |
|  +---- Tier 2: 관리 계층 (CIO·EA·PMO·CISO) -----------+     |
|  |  [IT운영위원회] 의장: CIO                          |     |
|  |  +- 의사결정: A(Accountable)                       |     |
|  |  +- 보고주기: 월 1회                                |     |
|  |  +- KPI: 프로젝트 성공률, SLA, 보안사고 건수        |     |
|  |  +- 산출물: EA 산출물, 서비스 카탈로그, 포트폴리오   |     |
|  |  +- 프레임워크: ITIL 4, TOGAF ADM, COBIT BAI/MEA  |     |
|  +----------------------------------------------------+     |
|                          ^ 보고                              |
|  +---- Tier 3: 운영·실행 계층 (현업·개발·인프라) ------+     |
|  |  [실무조직] Agile팀, SRE팀, SOC, 데이타거버넌스팀    |     |
|  |  +- 의사결정: C(Consulted)/I(Informed)             |     |
|  |  +- 보고주기: 주·일 단위 (Scrum, SLO/SLI)          |     |
|  |  +- KPI: 배포 빈도, MTTR, 결함 누출률, 위협탐지     |     |
|  |  +- 방법론: DevSecOps, ITIL 4 Operational Practice |     |
|  +----------------------------------------------------+     |
|                                                              |
|   ※ RACI 매트릭스: R=1, A=1, C=다수, I=다수 (Single A!)   |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **IT 전략위원회 (Tier 1)** | 사업-IT 정렬, 투자 의사결정, 위험 한도 설정 | COBIT 2019 **EDM 5개 도메인**(Evaluate·Direct·Monitor) + **ISO 38500 6원칙** + **BSC 4관점** (재무/고객/내부프로세스/학습성장), 연간 **IT전략맵(Strategy Map)** 수립, ROI/ROIC/NPV 기준 투자 우선순위 결정 |
| **EA(Enterprise Architecture) 거버넌스 (Tier 2)** | To-Be 아키텍처 설계, 표준 준수 검토 | **TOGAF ADM 8단계**(Preliminary->A:Architecture Vision->B:Business->C:Information Systems->D:Technology->E:Opportunities->F:Migration Planning->G:Implementation Governance->H:Architecture Change Management), **Zachman 6×6 매트릭스**, **ArchiMate 3.2** 표기법, **FEAF**(연방 EA) 참고, ADM Phase 별 산출물 32종(Architecture Definition Document, Solution Building Block 등) |
| **프로젝트 관리 거버넌스 (PMO)** | 다중 프로젝트 우선순위·자원 배분·성과 측정 | **PMBOK 7th(원리 12개+8개 성과도메인)**, **PRINCE2 7원칙·7실무·7프로세스**, **ISO 21500**, **SAFe 6.0**(Agile at Scale), 포트폴리오 차원의 **PPM 도구**(Planview, MS Project Online, Jira Align) 활용, **EVM(Earned Value Management)** — CPI/SPI ≥ 0.95 목표 |
| **IT 서비스 관리 (ITSM)** | 서비스 카탈로그, 인시던트·변경·문제·배포·레벨 관리 | **ITIL 4 SVS**(Service Value System) — 7대 지침(Guiding Principle), 34개 실무(실무 흐름 4단계: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support), **CSI(Continuous Service Improvement)** 등록, **ISO/IEC 20000-1:2018** 인증, **CMDB**(Configuration Management DB) 기반 자산 100% 가시화 |
| **정보보안 거버넌스 (CISO/SOC)** | 보안 정책·위협 대응·컴플라이언스 | **ISO 27001:2022**(Annex A 93통제), **ISMS-P**(한국, 14개영역 102개통제), **NIST CSF 2.0**(Identify·Protect·Detect·Respond·Recover + Govern), **Zero-Trust**(NIST SP 800-207, BeyondCorp), **SOC 2 Type II**, **GDPR/PIPA** 컴플라이언스 자동화, **KSI(핵심보안지표)** 대시보드 운영 |
| **위험 관리 (ERM 통합)** | IT 리스크 식별·평가·대응·모니터링 | **ISO 31000:2018**(원리·프레임워크·프로세스), **COSO ERM 2017**(5대요소 20원칙), **FAIR**(Factor Analysis of Information Risk) 정량모델, **Bow-Tie 분석**, **KRI**(핵심위험지표)와 **KPI** 통합 대시보드, 리스크 appetite/stolerance 문서화 |
| **성과 측정 및 평가** | KPI/KRI 대시보드, BSC/OKR | **Balanced Scorecard** 4관점 + **OKR** 동기부여, **IT4IT** 참조 모델, **CMMI Level 1~5** 성숙도 평가, **COBIT 2019 CMMI 연계**, **Net Promoter Score(NPS)** 사용자만족도 |
| **디지털 전환 (DX) 거버넌스** | 신기술 도입 의사결정, 혁신 촉진 | **Innovation Funnel**(아이디어->PoC->MVP->Pilot->Scale), **Lean Startup** 원칙, **실험 예산(20% Rule)**, **Technology Radar**(ThoughtWorks 방식 — Adopt/Trial/Assess/Hold 4단계), 데이터 거버넌스(**DAMA-DMBOK 2.0**), AI 거버넌스
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 612 / 800

<- **이전**: [611. IT 경영 관리 핵심 토픽 611번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/611_it_management_core_topic_611_exam_summary/)
**다음**: [613. IT 경영 관리 핵심 토픽 613번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/613_it_management_core_topic_613_exam_summary/) ->

---
