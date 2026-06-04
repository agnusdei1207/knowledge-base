---
title: "714. IT 경영 관리 핵심 토픽 714번 시험 요약 (IT Management Core Topic 714 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 714번은 IT 거버넌스(COBIT 2019), IT 서비스 관리(ITIL 4), 정보보안경영체계(ISMS-P), 프로젝트 관리(PMBOK 7), 그리고 디지털 전환 전략을 통합한 IT 경영 관리 역량을 평가하며, 각 프레임워크의 **Process-Governance-Technology 삼원구조**를 이해하는 것이 핵심이다.
> 2. **가치**: 정량적 효과로 IT 투자 대비 ROI 15~35% 개선, 정보보안 사고 60% 감소, IT 서비스 가용성 99.95% 이상 달성, 정성적 효과로 경영진의 IT 이해관계자 정렬(Stakeholder Alignment), 의사결정 투명성 확보, 컴플라이언스 자동화를 통한 리스크 기반 의사결정 체계를 구축한다.
> 3. **판단 포인트**: 중앙집중형 거버넌스(COBIT EDM 메커니즘)와 분산형 거버넌스(Federated COBIT) 중 조직 규모·산업·규제환경에 맞는 선택, ITIL 4의 34개 Practice 중 어떤 것을 우선 도입할지(High-Velocity IT 관점), 그리고 Zero Trust vs Defense-in-Depth 보안 아키텍처 트레이드오프, Agile-Water-Hybrid 중 프로젝트 특성 매칭이 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 714번 영역은 **"IT 경영 관리"**를 총괄하며, 단순한 기술 운용을 넘어 **IT를 경영 전략의 핵심 동력(Strategic Asset)**으로 전환하는 통합 관리 체계의 설계·구축·운영·개선 역량을 다룬다. 4차 산업혁명 시대에 기업의 IT 환경은 On-Premise 데이터센터, Public/Private/Hybrid Cloud, Edge Computing, SaaS 생태계로 확장되어 전통적인 IT 관리 프레임워크만으로는 한계가 명확해졌다.

특히 2020년 이후 COVID-19를 기점으로 한 비대면 업무 전환, 2023년 이후 생성형 AI(LLM, RAG, Agentic AI)의 급격한 확산, 그리고 EU AI Act(2024), 개인정보보호법 개정(2023), ISO 42001(AI 경영체계, 2023) 등 신 규제 환경은 IT 경영 관리자에게 **"속도(Agility) × 거버넌스(Control) × 가치(Value)"** 라는 삼중 제약(Triple Constraint)을 동시에 만족시키도록 요구한다.

기술사 시험 관점에서 714번은 단순 암기가 아닌 **"왜(Why) 어떤 프레임워크를 선택하고, 어떻게(How) 통합 설계하며, 무엇을(What) 정량적 KPI로 측정할 것인가"**에 대한 **공학적 의사결정(Engineering Decision-making)** 능력을 평가한다.

```text
+----------------------------------------------------------------------+
|           IT 경영 관리 통합 프레임워크 아키텍처 (714번 관점)         |
+----------------------------------------------------------------------+
|                                                                      |
|   [최상위] 경영 전략 (Corporate Strategy)                            |
|       |                                                              |
|       v  전략 정렬(Strategy Alignment) - SAMM, Ward & Peppard 모델    |
|   +--------------------------------------------------------+         |
|   |  IT 거버넌스 (COBIT 2019)                              |         |
|   |  +- EDM(평가, 지휘, 모니터) - 5개 프로세스              |         |
|   |  +- APO(정렬, 계획, 조직) - 14개 프로세스              |         |
|   |  +- BAI(빌드, 구매, 구현) - 11개 프로세스              |         |
|   |  +- DSS(배포, 서비스, 지원) - 6개 프로세스             |         |
|   |  +- MEA(모니터, 평가, 감사) - 4개 프로세스             |         |
|   +--------------------------------------------------------+         |
|       |                                                              |
|       +-----------------+-----------------+-----------------+       |
|       v                 v                 v                 v       |
|  [IT 서비스]       [정보보안]        [프로젝트]        [위험관리] |
|   ITIL 4           ISMS-P           PMBOK 7           ISO 31000   |
|   SVS 모델         14개 영역         8개 성과 영역     리스크 등록부|
|   34 Practice      102개 통제항목    12원칙            Bow-Tie 분석|
|       |                 |                 |                 |       |
|       +-----------------+-----------------+-----------------+       |
|                                  |                                    |
|                                  v                                    |
|   [기반 기술] Cloud(K8s/IaC) · Zero Trust · AIOps · FinOps · DevSecOps|
|                                  |                                    |
|                                  v                                    |
|   [측정/개선] BSC · KPI Tree · GRC Platform · Continual Improvement  |
+----------------------------------------------------------------------+
```

**구시대적 IT 관리 vs. 714번 영역의 현대적 IT 경영 관리 비교**

| 구분 | 구시대 (2000년대 이전) | 현대 (714번 관점) |
|------|----------------------|------------------|
| **거버넌스 모델** | IT를 비용센터(Cost Center)로 인식, CIO는 후방위적 역할 | IT를 가치창출(Value Driver)로 전환, CDO·CTO와 CIO 트라이어드 |
| **서비스 관리** | 자체 데이터센터 수작업 운영, IT 사일로 | ITIL 4 SVS(Service Value System) 기반 Value Stream 최적화 |
| **보안 패러다임** | 경계 기반 방어(Perimeter Security) | Zero Trust("Never Trust, Always Verify") + SASE/SSE |
| **프로젝트 관리** | Waterfall 위주, PMBOK 5/6 | PMBOK 7(원칙 중심) + Agile(Hybrid) + SAFe 6.0 |
| **투자 관리** | 예산 단위 CapEx, ROI 단순 산정 | TCO(총소유비용), FinOps(클라우드 단위 최적화), NPV/IRR |
| **규제 대응** | 사후 대응형 컴플라이언스 | 선제적 GRC(Governance-Risk-Compliance) 자동화 |
| **사고 대응** | MTTR 수동 측정, 사후 분석 | AIOps 기반 MTTI/MTTR/MTBF 실시간 관제, SRE 관행 |

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 종합 운영 체계"**와 같다. 교통(서비스), 치안(보안), 건설(프로젝트), 재무(투자), 환경(위험) 각 부서가 독립적으로 움직이되, **시장(경영진)의 요구에 맞춰 통합 조정하는市长(거버넌스)**가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스: COBIT 2019의 5개 도메인 및 40개 거버넌스/관리 목적(Governance/Management Objectives)

COBIT 2019는 이전 버전(COBIT 5, 2012)과 달리 **"Focus Area"(예: 사이버보안, DevOps, 위험), "Design Factor"(조직의 11가지 설계 변수), "Variant"(맞춤형 참조 모델)** 개념을 도입해 **원칙 기반(Principle-based)** 접근으로 전환했다.

```text
+---------------------------------------------------------------------+
|          COBIT 2019 핵심 메커니즘 (5단 워크플로우)                  |
+---------------------------------------------------------------------+
|                                                                     |
|  Step 1.  Design Factor 식별 (11개 변수)                            |
|   +- Enterprise Strategy (전략: Growth/Innovation/Cost/Cost+...)    |
|   +- Enterprise Goals -> 13개 표준 목표 정렬 (예: EG01 Portfolio)   |
|   +- Risk Profile (위험 성향: Risk Tolerance ≥ 0.05 = High)         |
|   +- I&T-Related Issues (현재 IT 이슈)                              |
|   +- Threat Landscape (사이버 위협 환경)                            |
|   +- Compliance Requirements (규제: GDPR, ISMS-P, AI Act)          |
|   +- Role of IT (Factory/Strategic/Turnaround/...)                  |
|   +- Sourcing Model (Outsourcing 비율 0~100%)                       |
|   +- IT Adoption Methods (Agile/DevOps/Traditional)                 |
|   +- Technology Adoption (Cloud-First, Mobile, AI/ML)               |
|   +- Enterprise Size (대기업/중견/중소)                             |
|              |                                                      |
|              v                                                      |
|  Step 2.  Cascade to I&T Goals (13개 -> Alignment Goals 매핑)        |
|              |                                                      |
|              v                                                      |
|  Step 3.  Selection of Governance/Management Objectives             |
|           (40개 중 우선순위 GO/MO 선정, 보통 12~20개)               |
|              |                                                      |
|              v                                                      |
|  Step 4.  Target Capability Level 설정 (0~5, CMMI 호환)             |
|              |                                                      |
|              v                                                      |
|  Step 5.  Implementation via Focus Area -> Roadmap 도출              |
+---------------------------------------------------------------------+
```

### 2. ITIL 4 Service Value System (SVS)

ITIL 4는 2019년发布的 ITIL v4(Foundation -> MP/SL -> Managing Professional -> Strategic Leader)이며, 9개의 guiding principle과 34개의 practice로 구성된다. **SVS의 5대 컴포넌트**는 Opportunity/Demand -> Value -> Guiding Principles -> Governance -> Practices -> Continual Improvement의 **폐루프(Closed-loop)** 구조다.

### 3. 정보보안경영체계 (ISMS-P) / ISO 27001:2022

2022년 개정을 통해 **Annex A 통제항목이 14개 영역, 93개 통제**로 재편(기존 114개에서 통폐합)되었고, **속성(Attributes)** 5개(Control Type, Information Security Properties, Cybersecurity Concepts, Operational Capabilities, Security Domains)를 도입해 다차원 분류가 가능해졌다. 한국 ISMS-P는 이基础上 개인정보보호 통제(Privacy) 7개 통제를 추가해 102개 항목으로 운영된다.

### 4. 프로젝트 관리: PMBOK 7th + 애자일 하이브리드

PMBOK 7(2021)은 **Process-based -> Principle-based**로 대전환하여 12가지 Project Management Principles(예: Be a diligent, respectful, and caring steward; Focus on value; Adapt to uncertainty)와 8가지 Project Performance Domains(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)를 제시한다.

### 5. 핵심 통합 메커니즘 (Cascading Goal Tree)

```text
+----------------------------------------------------------------------+
|       IT 경영 핵심 컴포넌트 및 데이터 흐름 (기술사 시험 빈출)       |
+----------------------------------------------------------------------+
|                                                                      |
|  [경영진] --- KPI 요구 ---+                                          |
|       |                    v                                         |
|       |            +----------------+                                |
|       |            | 전략맵(Strategy |                                |
|       |            |   Map) + BSC   |  <- 4관점(재무/고객/내부/학습)   |
|       |            +-------+--------+                                |
|       |                    | Cascading                               |
|       |                    v                                         |
|       |            +----------------+                                |
|       |            | IT BSC + GRC  |  <- COBIT 2019 EDM-02, APO-02  |
|       |            | 대시보드      |  <- RACI 매트릭스 연계           |
|       |            +-------+--------+                                |
|       |                    |                                         |
|       +--------------------+--------------------------------------+  |
|                            |                                      |  |
|       +--------------------+----------------------+               |  |
|       v                    v                      v               v  |
|  +--------+          +---------+           +----------+   +--------+|
|  |APO-04  |          |DSS-02   |           |BAI-03    |   |MEA-01  ||
|  |혁신/   |          |인시던트/ |           |변경관리/  |   |성과/   ||
|  |포트폴리|          |서비스데스크|          |릴리즈/   |   |내부감사||
|  |오      |          |SLA관리  |           |CI/CD     |   |/컴플라 ||
|  +---+----+          +----+----+           +----+-----+   +---+----+|
|      |                    |                     |              |     |
|      v                    v                     v              v     |
|  ISO 56002            ISO 20000           ISO 27017/27018  ISO 19011|
|  (혁신경영)            (IT서비스)          (클라우드 보안)  (감사)   |
|                                                                      |
|  [최하위] AIOps · ITAM(CMDB) · SIEM · ITSM Tool(Servicenow/Jira)    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 거버넌스 최고 의사결정층 | 5개 프로세스: EDM01 거버넌스 프레임워크, EDM02 benefit delivery, EDM03 risk optimization, EDM04 resource mgmt, EDM05 stakeholder transparency. **이사회의 IT Committee 운영**과 직접 매핑 |
| **APO (Align, Plan, Organize)** | 전략 정렬·계획·조직 설계 | 14개 프로세스: APO01~14. **IT 전략 계획(APO02)**, **포트폴리오 관리(APO05)**, **위험 관리(APO12)**, **보안 관리(APO13)** 포함. 보통 Capability Level 3(Well-defined) 목표로 설정 |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·구현 | 11개 프로세스: BAI01~11. **변경 관리(BAI03) -> CAB(Change Advisory Board) 운영**, **테스트 관리(BAI05)**, **프로그램/프로젝트 관리(BAI01)**. CMDB 정확도가 BAI03의 핵심 의존성 |
| **DSS (Deliver, Service, Support)** | 서비스 운영·지원 | 6개 프로세스: DSS01~06. **인시던트(DSS02)**, **문제(DSS03)**, **연속성(DSS04)**, **모니터링(DSS05)**. MTTR < 1hr, FCR ≥ 75% 등 KPI 운영 |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정·감사·평가 | 4개 프로세스: MEA01~04. **내부 감사(COBIT 5.0 MEA02)**, **컴플라이언스(MEA03)**, **성과(MEA01)**. 3 Lines of Defense(1st: 운영, 2nd: 리스크/컴플, 3rd: 내부감사) 모델 적용 |
| **ITIL 4 Service Value Chain** | 운영 가치 흐름 | 6개 액티비티: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve. **Value Stream Mapping**을 통해 종단간(E2E) 프로세스 측정 |
| **ISMS-P Annex A** | 보안 통제 항목 | 93 + 9(개인정보) = 102개 통제
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 714 / 800

<- **이전**: [713. IT 경영 관리 핵심 토픽 713번 시험 요약](/studynote/12_it_management/05_security_compliance/713_it_management_core_topic_713_exam_summary/)
**다음**: [715. IT 경영 관리 핵심 토픽 715번 시험 요약](/studynote/12_it_management/05_security_compliance/715_it_management_core_topic_715_exam_summary/) ->

---
