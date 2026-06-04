---
title: "515. IT 경영 관리 핵심 토픽 515번 시험 요약 (IT Management Core Topic 515 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(515번)는 COBIT 2019, ITIL 4, ISO/IEC 38500, EA(Enterprise Architecture) 4계층 프레임워크를 통합하여 **Value Governance(가치 거버넌스)** 체계를 수립하고, **NED(Senior Manager) -> APM(各级 관리자) -> 운영자**로 이어지는 3계층 의사결정 구조에서 **RACI 매트릭스**와 **KGI/KPI平衡計分卡(BSC)**를 통해 IT 투자 대비 사업 가치(ROIT, Return on IT Investment)를 최적화하는 경영과학 분야입니다.
> 2. **가치**: McKinsey 2023년 연구에 따르면 성숙한 IT 거버넌스 체계 도입 기업은 **IT 비용 23% 절감, 프로젝트 성공률 67%->89% 상승, Time-to-Market 41% 단축**, ISO 38500 인증 기업은 **컴플라이언스 위반 건수 78% 감소, 감사 대응 시간 56% 단축**, COBIT 2019 완전 도입 시 **이해관계자 만족도(Stakeholder Satisfaction) 35% 향상** 효과를 달성합니다.
> 3. **판단 포인트**: **①** 중앙집중형(Centralized) vs 분산형(Democratized) 거버넌스 모델 선택, **②** Cobit(Controls) 중심 vs ITIL(Services) 중심 철학 채택, **③** Plan-Driven(폭포수) vs Agile-Fed(스크럼·SAFe) 거버넌스 조화, **④** Balanced Scorecard 4관점(재무/고객/내부/학습성장) 가중치 배분, **⑤** Zero Trust 보안 vs 운영 편의성 트레이드오프, **⑥** Cloud First 전략 시 FinOps 도입 여부 — 이 6대 의사결정 변수가 경영 성과(TCO, ROI, NPV)를 결정합니다.

---

## Ⅰ. 개요 및 필요성

IT 경영관리(Information Technology Management & Governance, 515번)는 1980년대 MIS(경영정보시스템)에서 시작하여 1990년대 IT 거버넌스 개념의 등장(UK Cadbury Report 1992, OECD 1999), 2000년대 COBIT·ITIL의 글로벌 표준화, 2010년대 디지털 전환(DX) 가속화, 2020년대 ESG·AI 윤리·클라우드 네이티브 환경으로 진화해 온 **정보시스템의 전략·재무·운영·위험·컴플라이언스를 통합 관리하는 최상위 경영과학**입니다.

최근 5년간 IT 환경은 **①** 하이퍼스케일러(AWS·Azure·GCP) 기반 멀티클라우드화, **②** 생성형 AI(LLM·RAG)·MLOps 확산, **③** 데이터3법(개인정보보호법·정보통신망법·신용정보법) 개정 및 EU AI Act(2024.8 시행), **④** KR/US/EU 3극 규제 동조화, **⑤** SaaS·PaaS·IaaS 경계의 모호화로 인해 CFO·CIO·CDO·CISO·DPO 5대 역할의 책임 소재가 복잡하게 얽히며, **이사회 수준의 거버넌스 메커니즘 부재 시 평균 손실액이 연간 4.7백만 USD**에 달합니다(Ponemon Institute 2023).

```text
+----------------------------------------------------------------------+
|        IT 경영관리 4대 핵심 영역(515번 통합 프레임워크)             |
+----------------------------------------------------------------------+
|                                                                      |
|   +-------------------+    +-------------------+                    |
|   | ① IT Strategy     |◄--►| ② IT Governance   |                    |
|   |   (전략·투자)      |    |   (의사결정·통제)  |                    |
|   |                   |    |                   |                    |
|   | • IS 전략수립      |    | • COBIT 2019      |                    |
|   | • TOGAF·FEAF EA   |    | • ISO 38500       |                    |
|   | • Port. Mgmt      |    | • RACI            |                    |
|   +---------+---------+    +---------+---------+                    |
|             |                        |                              |
|             v                        v                              |
|   +-------------------+    +-------------------+                    |
|   | ③ IT Operation    |◄--►| ④ IT Risk &      |                    |
|   |   (운영·서비스)    |    |   Compliance      |                    |
|   |                   |    | (리스크·컴플라이언스)                    |
|   | • ITIL 4          |    | • ISO 27001·27701 |                    |
|   | • DevOps·SRE     |    | • GDPR·PIPL·APPI  |                    |
|   | • FinOps          |    | • NIST CSF 2.0    |                    |
|   +-------------------+    +-------------------+                    |
|                                                                      |
|   +------------------------------------------------------------+    |
|   |        수직 통합: Business Strategy -> IT Strategy          |    |
|   |   Mission/Vision -> Strategic Goal -> IT Principle -> EA    |    |
|   +------------------------------------------------------------+    |
|                                                                      |
+----------------------------------------------------------------------+
```

기존의 **IT 부서 중심 운영 모델**(CIO가 기술만 책임, 사업 부서와 단절, KPI는 가용성·MTBF)로는 디지털 트랜스포메이션 시대의 비즈니스 요구에 대응할 수 없어, **CDO(Chief Data Officer)·CISO(Chief Information Security Officer)·CPO(Chief Privacy Officer)를 포함한 확장 C-Suite 거버넌스**로 진화해야 합니다. ISO/IEC 38500(2008년 제정, 2015년 개정)은 이사회가 IT를 **"Evaluate -> Direct -> Monitor"** 3단계 사이클로 감독하도록 규정하며, 한국 정보통신산업진흥원(NIPA)의 2022년 조사에 따르면 도입 기업의 **이해관계자 신뢰도(Stakeholder Trust Index)가 평균 2.4배** 상승했습니다.

- **📢 섹션 요약 비유**: IT 경영관리는 **'도시의 도시계획(Urban Planning)'** 과 같습니다. 도로(네트워크), 건물(애플리케이션), 상하수도(데이터), 공원(보안), 소방서(BCP)가 개별 최적화되면 정체·침수·정전이 발생하듯, **IT 구성요소를 도시 단위에서 통합 설계·감리·재개발하는 것이 IT 거버넌스**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. COBIT 2019 거버넌스 시스템 (40단계 Governance & Management Objectives)

COBIT 2019는 **Governance Objectives 5개(EDM: Evaluate, Direct, Monitor)** + **Management Objectives 35개**(APO: Align Plan Organize 14개, BAI: Build Acquire Implement 11개, DSS: Deliver Service Support 6개, MEA: Monitor Evaluate Assess 4개)로 구성되며, **40개 목적(Objective)** 각각이 **Process -> Practice -> Activity -> Work Product** 4계층으로 분해됩니다.

```text
+----------------------------------------------------------------------+
|              COBIT 2019 거버넌스 시스템 6대 구성요소                |
+----------------------------------------------------------------------+
|                                                                      |
|  ① 설계 팩터(Design Factors) 10개                                     |
|   +- 1. Enterprise Strategy (전략)                                    |
|   +- 2. Enterprise Goals (목표 13개)                                  |
|   +- 3. Risk Profile (위험 프로파일)                                  |
|   +- 4. I&T 관련 이슈 (20개)                                          |
|   +- 5. 위협 환경 (Threat Landscape)                                  |
|   +- 6. 컴플라이언스 요구 (요구사항 맵)                                |
|   +- 7. 역할 주체 (Role Players)                                      |
|   +- 8. IT 도입 이슈 (Sourcing)                                       |
|   +- 9. IT 구현 방법 (DevOps, Agile)                                  |
|   +-10. 기술 채택 (AI, Cloud, Blockchain)                             |
|                                                                      |
|  ② 초점 영역(Focus Areas) 30+개: 사이버보안, DevOps, 디지털 거버      |
|  ③ 목표 계보(Goals Cascade): Stakeholder -> Enterprise -> Alignment     |
|  ④ 컴포넌트 변형(Variants): 13개 컴포넌트 조합                        |
|  ⑤ 핵심 모델(Core Model): 40 Objective + 5 프로세스 속성              |
|  ⑦ 성능관리: NRR(Not/Rarely/0-15%), PRINCE2·CMMI·ITIL 매핑           |
|                                                                      |
|  +----------+   +----------+   +----------+   +----------+         |
|  |  EDM 01  |   |  EDM 02  |   |  EDM 03  |   |  EDM 04  |         |
|  | 거버넌스 |   | 이사회   |   | 위험최적화|   | 자원최적화|         |
|  | 체계평가  |   | 활동감독 |   |          |   |          |         |
|  +----+-----+   +----+-----+   +----+-----+   +----+-----+         |
|       +--------------+--------------+--------------+                 |
|                              |                                       |
|              +---------------+---------------+                       |
|              v               v               v                       |
|         +---------+    +----------+    +---------+                   |
|         |  APO    |    |   BAI    |    |   DSS   |                   |
|         | 14개    |    |  11개    |    |   6개   |                   |
|         | Plan    |    | Build    |    | Service |                   |
|         | Org     |    | Acquire  |    | Support |                   |
|         +----+----+    +----+-----+    +----+----+                   |
|              +--------------+---------------+                        |
|                              |                                       |
|                              v                                       |
|                         +---------+                                  |
|                         |  MEA 4개 |                                  |
|                         | Monitor |                                  |
|                         +---------+                                  |
+----------------------------------------------------------------------+
```

### B. ITIL 4 Service Value System (SVS)

ITIL 4(2019년 AXELOS 발표, 2020년 이후 5단계 인증체계: Foundation->MP/SL->Managing Professional->Strategic Leader->Master)는 **7개 지침(Guiding Principles) + SVS(Service Value System) + 34개 Practice**로 구성됩니다.

```text
   +--------------------------------------------------------------+
   |                  ITIL 4 SVS (Service Value System)           |
   |                                                              |
   |   Opportunity/Demand ◄----+    +----► Value (공동창조)        |
   |                           |    |                              |
   |   +-----------------+    v    ^    +-----------------+      |
   |   |  Guiding         |  +-----+  |  7 Guiding      |      |
   |   |  Principles 7    |  | SVS |  |  Principles     |      |
   |   |  1. Focus value  |  | Core|  |  1. Focus on    |      |
   |   |  2. Start where  |  |     |  |     value        |      |
   |   |  3. Progress     |  |     |  |  2. Start where  |      |
   |   |     iteratively  |  |     |  |     you are      |      |
   |   |  4. Collaborate  |  +-----+  |  3. Progress     |      |
   |   |  5. Think & work |     ^     |     iteratively  |      |
   |   |     holistically |     |     |  4. Collaborate  |      |
   |   |  6. Keep it      |     |     |  5. Think & work |      |
   |   |     simple       |     |     |     holistically |      |
   |   |  7. Optimize &   |     |     |  6. Keep it      |      |
   |   |     automate     |     |     |     simple       |      |
   |   +-----------------+     |     |  7. Optimize &   |      |
   |                          v     |     automate      |      |
   |   +------------------------------------------------------+   |
   |   |  Service Value Chain (6단계)                          |   |
   |   |  Plan -> Improve -> Engage -> Design&Transition ->       |   |
   |   |  Obtain/Build -> Deliver&Support                      |   |
   |   +------------------------------------------------------+   |
   |                          |                                    |
   |                          v                                    |
   |   +------------------------------------------------------+   |
   |   |  34 Practices (14 General + 17 Service + 3 Tech)    |   |
   |   |  General: Strategy, Portfolio, Architecture, Risk     |   |
   |   |  Service: Incident, Problem, Change, SLM, Monitoring |   |
   |   |  Technical: Deployment, Infra, SW Dev                |   |
   |   +------------------------------------------------------+   |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (40 Objective)** | **거버넌스·관리 체계** 수립 및 통제 | EDM 5(평가·지시·감독) -> APO 14(계획·조직·정렬) -> BAI 11(구축·획득·구현) -> DSS 6(서비스 제공·지원) -> MEA 4(모니터·평가·감사) 5도메인 40목표. **설계 팩터(Design Factor) 10개**를 가중치 기반 Priority로 조정하여 조직 맞춤 거버넌스 시스템 구축. **Goal Cascade**: Stakeholder Needs -> Enterprise Goals(13) -> Alignment Goals(13) -> Process Goals. **NRR(Negative Risk Rating) 4단계**(Not Yet=15%/Rarely=50%/Sometimes=85%/Almost Always=100%)로 프로세스 성숙도 측정. **CMMI·PRINCE2·ITIL·ISO 27001·NIST CSF** 등 14개 표준과 양방향 매핑(Conceptual Map) 지원. |
| **ITIL 4 SVS** | **서비스 가치 공동창조(Value Co-Creation)** 체계 | 7 Guiding Principles(가치중심, 현재에서 시작, 반복적 진보, 협업, 전체적 사고, 단순화, 최적화·자동화) + Service Value Chain 6단계(Plan->Improve->Engage->Design & Transition->Obtain/Build->Deliver & Support) + 34 Practices(General Management 14, Service Management 17, Technical Management 3). **Service Desk는 Tier 1(80% L1) -> Tier 2(15% L2) -> Tier 3(5% L3, Vendor)** 3-tier 에스컬레이션 구조. **SLI/SLO/SLA 3단계 계층**: SLI(Technical Indicator, e.g., 응답시간 200ms) -> SLO(Internal Objective, 99.9%) -> SLA(외부 계약, 99.5% 가용성). |
| **ISO/IEC 38500 (2015)** | **이사회 수준 IT 거버넌스** 국제표준 | 6개 원칙
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 515 / 800

<- **이전**: [514. IT 경영 관리 핵심 토픽 514번 시험 요약](/studynote/12_it_management/05_security_compliance/514_it_management_core_topic_514_exam_summary/)
**다음**: [516. IT 경영 관리 핵심 토픽 516번 시험 요약](/studynote/12_it_management/05_security_compliance/516_it_management_core_topic_516_exam_summary/) ->

---
