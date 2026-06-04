+++
title = "617. IT 경영 관리 핵심 토픽 617번 시험 요약 (IT Management Core Topic 617 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 기술사 617번은 COBIT 2019, ITIL 4, ISO 27001, ISO 20000, CMMI v2.0, PMBOK 7, BABOK v3 등 글로벌 표준 프레임워크를 통합적으로 이해하고, IT 거버넌스·전략·프로젝트·서비스·보안·품질·아키텍처 7대 영역을 End-to-End로 연결하는 의사결정 능력을 평가한다.
> 2. **가치**: 단순 암기가 아닌 "현업 Issue -> 프레임워크 적용 -> 정량적 KPI 도출 -> 거버넌스 보고"의 4단계 Chain of Thought를 통해, 기업이 평균 23~35% IT 비용 절감(Forrester, 2023) 및 컴플라이언스 위반 67% 감소(McKinsey, 2024)를 달성할 수 있는 실무형 통찰을 제공한다.
> 3. **판단 포인트**: Frameworks는 "따라야 할 종교"가 아니라 "측정 가능한 Control Objective"임을 인지하고, 조직의 Maturity Level(CMMI 1~5)에 맞는 Right-Sized 도입, Quick-Win과 Long-Term Balance, RACI 매트릭스 기반의 책임 소재 명확화가 핵심 Trade-off이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 1990년대 Y2K 문제와 ERP 붐을 거치며 "IT는 비용(Cost Center)"이라는 인식에서, 2010년대 클라우드·모바일·데이터 폭증으로 "IT는 전략 자산(Value Driver)"으로 패러다임이 전환되면서 본격화된 학문·실무 영역이다. 기술사 617번 시험은 이러한 시대적 흐름을 반영하여, 단순 이론 암기가 아닌 **"경영 환경 변화 -> IT 전략 수립 -> 솔루션 도입 -> 성과 측정 -> 지속적 개선"**의 전(全) 라이프사이클을 통합적으로 다룬다.

특히 2020년 이후 팬데믹, 공급망 재편, 생성형 AI(LLM, RAG, Agentic AI)의 등장으로 IT 거버넌스의 중요성이 극대화되었으며, EU의 DORA(Digital Operational Resilience Act), AI Act, 한국의 AI 기본법, 개인정보보호법 개정, ISMS-P 인증 의무화 등 규제 환경이 급격히 강화되면서 **"컴플라이언스 기반 IT 경영"**이 필수가 되었다.

```text
+------------------------------------------------------------------+
|           IT 경영 관리 7대 영역 통합 거버넌스 프레임워크           |
+------------------------------------------------------------------+
|  +----------+  +----------+  +----------+  +----------+         |
|  | ① 전략   |  | ② 거버넌 |  | ③프로젝트|  | ④ 서비스 |         |
|  | Strategy |<-->|Governance|<-->|  PMO    |<-->|  ITIL   |         |
|  +----------+  +----------+  +----------+  +----------+         |
|        ^             ^              ^              ^             |
|        +-------------+------+-------+--------------+             |
|                             v                                     |
|  +----------+  +----------+  +----------+                        |
|  | ⑤ 보안   |<-->| ⑥ 품질   |<-->| ⑦ EA/BA  |                        |
|  |  ISMS-P  |  | CMMI/ISO |  | TOGAF/BIZ|                        |
|  +----------+  +----------+  +----------+                        |
|        ^             ^              ^                             |
|        +-------------+-------+------+                             |
|                               v                                    |
|              +------------------------------+                      |
|              |  외부 환경: 규제, 시장, 기술  |                      |
|              |  (DORA, AI Act, ESG, 생성AI)  |                      |
|              +------------------------------+                      |
+------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 관점 | 전통적 IT 경영 (1990~2010) | 현대 IT 경영 (2020~) |
|---|---|---|
| **관점** | 비용 중심 (Cost Center) | 가치 중심 (Value Center) |
| **구조** | 수직·사일로 (Silo) 조직 | 수평·플랫폼·프로덕트팀 |
| **거버넌스** | Sarbanes-Oxley, IT 통제 | DORA, AI Act, ESG, ISMS-P |
| **방법론** | 폭포수(Waterfall) | Agile, DevSecOps, Platform Engineering |
| **측정** | Uptime, 예산 준수 | NPV, ROI, NPS, Time-to-Market |
| **기술** | Mainframe, Client-Server | Cloud, AI/ML, Edge, Quantum |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 도시계획(Urban Planning)"**과 같습니다. 건물 하나 짓는 것이 프로젝트 관리라면, 도시 전체의 토지이용·교통·환경·안전 규정을 통합 설계하는 것이 IT 경영 관리이며, COBIT이 "도시기본계획", ITIL이 "교통운영규정", ISMS가 "치안규칙"에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"Strategy -> Architecture -> Implementation -> Operation -> Audit"**의 5단계 Value Chain과, 이를 가로지르는 **Governance/Control/Measure**의 3축 메타 프레임워크로 구성된다. COBIT 2019는 이를 40개의 Governance/Management Objective로 정형화하고, 각 Objective를 5단계 능력 수준(0~5) 및 Process Capability(RACEF: Realized, Achieved, Confirmed, Established, Fully Managed)로 측정한다.

```text
    +--------------------------------------------------------------+
    |  COBIT 2019 Cascade: Governance에서 Operational로의 연계    |
    +--------------------------------------------------------------+
    |                                                              |
    |  +-----------------+                                         |
    |  | Stakeholder     |  Needs & Drivers                         |
    |  | Concerns        |  (Benefit Realization, Risk Optimization,|
    |  +--------+--------+   Resource Optimization, Compliance)     |
    |           v                                                   |
    |  +-----------------+                                         |
    |  | Enterprise Goals|  13개의 일반적 목표 (예: 포트폴리오,     |
    |  | (13개)          |   서비스 품질, 비용 최적화)              |
    |  +--------+--------+                                         |
    |           v                                                   |
    |  +-----------------+                                         |
    |  | Alignment Goals |  Alignment 목표 (예: AG01: IT 표준 준수,  |
    |  | (13개)          |   AG04: 통합·표준화)                     |
    |  +--------+--------+                                         |
    |           v                                                   |
    |  +-----------------+                                         |
    |  | Governance &    |  EDM(5개), Evaluate/Direct/Monitor       |
    |  | Management Obj. |  APO(14), BAI(11), DSS(6), MEA(4)        |
    |  | (40개)          |                                         |
    |  +--------+--------+                                         |
    |           v                                                   |
    |  +-----------------+                                         |
    |  | Process/Activity|  RACI 차트, 프로세스 맵, 컨트롤 목적     |
    |  +-----------------+                                         |
    +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 이사회·최고위층 거버넌스 | 5개 프로세스: EDM01(거버넌스 체계), EDM02(이익 배분), EDM03(위험 관리), EDM04(자원 관리), EDM05(투명성). 핵심: **"Direct ≠ Manage"** - 이사회는 방향 제시, 경영진이 운영. |
| **APO (Align, Plan, Organize)** | IT 전략·포트폴리오·아키텍처 계획 | 14개 프로세스: APO01(관리 프레임워크), APO04(혁신), APO05(포트폴리오), APO12(위험 관리), APO13(보안 관리). 핵심 산출물: **SBP(Strategic/Budgeting Plan), Architecture Blueprint** |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·구축 | 11개 프로세스: BAI01(프로그램·프로젝트), BAI02(요구사항 정의), BAI03(솔루션 설계·구축), BAI08(지식 관리). 핵심: **PMBOK 7, PRINCE2, MSP** 연계 |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영·지원 | 6개 프로세스: DSS02(서비스 요청·사고), DSS03(문제), DSS04(연속성), DSS05(보안 서비스). 핵심: **ITIL 4 Service Value System (SVS)** 연계 |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정·감사·평가 | 4개 프로세스: MEA01(성과 모니터링), MEA02(내부 통제), MEA03(외부 컴플라이언스), MEA04(감사). 핵심: **BSC(Balanced Scorecard), OKR, KGI/KPI** |

**핵심 측정 체계 (CMMI v2.0 5단계 + ITIL 4 Maturity)**

| Maturity Level | 명칭 | 핵심 특성 | 조직 예시 |
|---|---|---|---|
| Level 1 | Initial (초기) | 개인 영웅에 의존, 재현 불가 | 스타트업 초기 |
| Level 2 | Managed (관리) | 프로젝트 단위 관리, 재현 가능 | 일반 SI 프로젝트 |
| Level 3 | Defined (정의) | 조직 표준 프로세스, Proactive | CMMI Level 3 인증사 |
| Level 4 | Quantitatively Managed (정량 관리) | SPM(SET/Data), 통계적 통제 | KT, 삼성SDS |
| Level 5 | Optimizing (최적화) | 지속적 혁신, Causal Analysis | Google, Microsoft |

- **📢 섹션 요약 비유**: COBIT의 5개 도메인(EDM, APO, BAI, DSS, MEA)은 **"병원 운영 시스템"**과 같습니다. EDM은 이사회(전체 방향), APO는 진료과 기획(자원 배분), BAI는 진료·수술 행위, DSS는 입원·간호 서비스, MEA는 QI(Quality Improvement)/의료감사입니다. 환자가 건강해지는 것이 곧 **"Value Delivery"**입니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역은 유사한 명칭의 프레임워크가 혼재하므로, 그 차이를 정확히 구분하는 것이 기술사 답안의 핵심이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001/20000** | **TOGAF 10** | **PMBOK 7** |
|---|---|---|---|---|---|
| **주 목적** | IT 거버넌스·통제 | IT 서비스 운영 | 정보보안·서비스 인증 | EA 방법론 | 프로젝트 관리 |
| **개발 주체** | ISACA | AXELOS (PeopleCert) | ISO/IEC | The Open Group | PMI |
| **핵심 개념** | 40개 Governance Objective | 34 Practices, SVS | ISMS, SMS, PDCA | ADM(8단계) Cycle | 8 Performance Domain, 12 Principles |
| **측정 단위** | Process Capability (0~5) | Maturity Model | Control Objective | Architecture Maturity | Performance Domain Score |
| **적용 범위** | Enterprise 전체 IT | Service Operation | 보안/서비스 | EA 산출물 | 프로젝트 단위 |
| **연계 영역** | EDM, APO, BAI, DSS, MEA | Service Value Chain | Annex A 93개 통제 | Business->Data->App->Tech | Stakeholder, Team, Planning, Delivery |
| **인증/감사** | COBIT Assessor | ITIL Foundation~Master | 인증 심사원 (IRCA) | TOGAF Certified | PMP, PfMP |
| **주 사용자** | CIO, IT 감사, 컨설턴트 | 서비스 매니저, ITSM | CISO, 보안감사원 | EA 아키텍트 | PMO, 프로젝트 매니저 |

**프레임워크 간 통합 관계**

```text
+------------------------------------------------------------+
|                  통합 거버넌스 메타 모델                    |
|                                                            |
|   COBIT (What & Why)  ->  ITIL (How - Service)             |
|        v                      v                            |
|   PMBOK (How - Project) <-  ISO 27001 (Secure)             |
|        v                      v                            |
|   CMMI (How - Process)   -> TOGAF (How - Architecture)     |
|                                                            |
|   * 모든 프레임워크는 조직의 "Value Realization"을         |
|     위한 Complementary Layer로 작동                        |
+------------------------------------------------------------+
```

**다른 시스템 구성요소와의 통합**

- **ERP (SAP, Oracle)**: APO/BAI 단계에서 프로세스 자동화의 Backbone
- **CRM (Salesforce, Dynamics 365)**: DSS 단계에서 End-User Service 품질 측정
- **DevSecOps (GitLab, Jenkins, SonarQube)**: BAI 단계의 CI/CD 파이프라인, MEA 단계의 정적 분석
- **SIEM (Splunk, QRadar)**: DSS05(보안 서비스) 실시간 모니터링
- **BPM/Workflow (Camunda, Appian)**: MEA03(컴플라이언스) 자동화
- **Data Lake (Snowflake, Databricks)**: MEA01(성과 모니터링)의 데이터 분석 기반

- **📢 섹션 요약 비유**: 이 5대 프레임워크는 **"오케스트라의 악기들"**과 같습니다. COBIT은 **지휘자**(전체 흐름), ITIL은 **제1바이올린**(서비스 멜로디), ISO 27001은 **보안요원**(안정성), TOGAF는 **건축가**(구조), PMBOK은 **팀장**(실행). 합주 없이 한 악기만 연주하면 어색하지만, 함께 연주하면 완벽한 IT 경영의 심포니가 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 IT 경영 관리 도입 시 가장 큰 실패 원인은 **"Frameworks are not Goals"**라는 점을 간과하는 것이다. McKinsey(2023) 보고에 따르면, 글로벌 기업의 70%가 Frameworks를 도입했으나 실제 Value를 창출한 경우는 23%에 불과하다. 성공의 핵심은 **"Right-Sized Adoption"** - 조직의 Maturity에 맞는 점진적 도입이다.

### 기술사형 판단 체크리스트

1. **현재 Maturity 진단**: COBIT 2019 Self-Assessment(또는 CMMI SCAMPI Appraisal)를 통해 Level 1~5 중 어디에 위치하는지 정량 측정했는가? 통상적으로 1단계 건너뛰기(Skip-Level)는 실패율 78% (Gartner, 2022).
2. **RACI 매트릭스 명확화**: 40개 COBIT Objective 별로 Responsible(수행), Accountable(책임), Consulted(자문), Informed(통보)를 정의했는가? 동일 Objective에 A가 2명이면 "Duck Syndrome" 발생.
3. **Value Goal ↔ IT Goal ↔ Process Metric의 3단 Cascade**: Enterprise Goal(예: "고객 만족도 20% 향상") -> Alignment Goal(예: "IT 서비스 가용성 99.95%") -> Process KPI(예: "인시던트 MTTR 30분 이내")로 정량 연계.
4. **Quick-Win + Big-Bet 균형**: 12개월 내 ROI 200% 가능한 Quick-Win(예: RPA 100개 도입)과 2~3년 ROI가 나오는 Big-Bet(예: 클라우드 마이그레이션)을 70:30 비율로 포트폴리오 편성.
5. **Risk-Based Approach & Compliance Mapping**: EU DORA, AI Act, 국내 ISMS-P, 개인정보보호법, 전자금융거래법 등 규제 요구사항을 Control Objective에 1:1 매핑하고, Residual Risk를 6개월 주기로 재평가.

### 피해야 할 안티패턴

- **"Big-Bang Framework 도입"**: 전
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 617 / 800

<- **이전**: [616. IT 경영 관리 핵심 토픽 616번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/616_it_management_core_topic_616_exam_summary/)
**다음**: [618. IT 경영 관리 핵심 토픽 618번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/618_it_management_core_topic_618_exam_summary/) ->

---
