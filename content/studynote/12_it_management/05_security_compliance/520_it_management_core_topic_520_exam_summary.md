---
title: "520. IT 경영 관리 핵심 토픽 520번 시험 요약 (IT Management Core Topic 520 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 520번은 COBIT 2019, ITIL 4, ISO 38500, NIST CSF 등 글로벌 거버넌스 프레임워크를 기반으로 IT-비즈니스 전략 정렬(Strategic Alignment), 가치 전달(Value Delivery), 위험 최적화(Risk Optimization), 자원 관리(Resource Management), 성과 측정(Performance Measurement)의 5대 핵심 영역을 통합적으로 평가하는 종합 관리 체계임.
> 2. **가치**: 성숙한 IT 거버넌스 도입 시 IT 투자 ROI 20~35% 향상, 프로젝트 성공률 70% 이상 도달, 보안 사고 대응 시간 60% 단축, EA(Enterprise Architecture) 기반 중복 투자 제거로 TCO 15~25% 절감 효과를 정량적으로 달성 가능함.
> 3. **판단 포인트**: 중앙 집중형(Centralized) vs 분산형(Decentralized) IT 거버넌스 구조, Agile-DevOps-Cloud 네이티브 환경에서의 거버넌스 라이트(Lightweight Governance) 적용 여부, 그리고 KPI/KGI/CSF 간의 인과적 연계 구조 설계가 기술사의 핵심 판단 영역임.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원 역할에서 비즈니스 동인(Driver)으로의 전환이 가속화되면서, IT 경영 관리는 CFO·CDO·CIO의 의사결정 체계와 직결되는 전략적 역량으로 재정의되었습니다. 토픽 520번은 이러한 패러다임 전환을 다룰 수 있는 포괄적 프레임워크로, IT 거버넌스(Governance)·IT 관리(Management)·IT 운영(Operation)의 3계층 구조를 통합적으로 다룹니다.

특히 4차 산업혁명 시대를 맞아 클라우드 전환(Cloud Migration), AI/ML 기반 의사결정, 데이터 거버넌스(Data Governance), 사이버 리질리언스(Cyber Resilience) 등 새로운 통제 포인트(Control Point)가 등장하면서, 전통적 ITIL v3 기반 운영 모델로는 더 이상 비즈니스 요구를 충족할 수 없게 되었습니다. IT 거버넌스 표준인 ISO/IEC 38500:2015, 제어 목표 프레임워크 COBIT 2019, 그리고 NIST CSF 2.0(2024)을 통합한 통합 거버넌스 체계(Integrated Governance System) 구축이 요구됩니다.

```text
+------------------------------------------------------------------+
|          IT 경영 관리 3계층 통합 프레임워크 (520번 토픽)         |
+------------------------------------------------------------------+
|  +----------------------------------------------------------+  |
|  |  1계층: IT 거버넌스 (Governance) - "무엇을, 왜 할 것인가" |  |
|  |  • 이사회의 책임 (Directorate Responsibility)             |  |
|  |  • ISO/IEC 38500 6원칙: 책임·전략·취득·성과·준수·인적    |  |
|  |  • COBIT 2019: 40개 관리 목표, 5개 도메인                 |  |
|  +----------------------------------------------------------+  |
|                              |                                   |
|                              v                                   |
|  +----------------------------------------------------------+  |
|  |  2계층: IT 관리 (Management) - "어떻게 계획하고 통제"      |  |
|  |  • 전략·포트폴리오·프로젝트·서비스·위험 운영              |  |
|  |  • BSC 기반 KPI/KGI/CSF 연계                              |  |
|  |  • PMO, EA Team, ITSM Process Owner                       |  |
|  +----------------------------------------------------------+  |
|                              |                                   |
|                              v                                   |
|  +----------------------------------------------------------+  |
|  |  3계층: IT 운영 (Operation) - "일상적 서비스 제공"         |  |
|  |  • ITIL 4 Service Value System (SVS)                      |  |
|  |  • 34개 ITIL Practices, DevOps 통합                        |  |
|  |  • SRE, AIOps, Observability (3-pillar)                   |  |
|  +----------------------------------------------------------+  |
|                                                                  |
|  -> 외부 환경: 규제 (개인정보보호법, ISMS-P), 시장, 기술           |
|  -> 내부 환경: 문화, 역량, 조직구조, 투자재원                       |
+------------------------------------------------------------------+
```

기존에는 IT 부서가 기술적 요구사항에만 집중하는 **"Technology-Driven"** 접근이 주를 이루었으나, 현재는 비즈니스 가치(Value) 중심의 **"Value-Driven"** 접근으로 전환되었습니다. 이는 Ward & Peppard의 IS/IT 전략 정렬 모델(2002)이나 Henderson & Venkatraman의 Strategic Alignment Model(1993)의 핵심 사상과도 일치하며, 토픽 520번의 출제 의제(Exam Agenda)에 직접 반영됩니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 도시의 '종합행정 체계'와 같습니다. 시장(거버넌스)이 정책 방향을 정하면, 구청(관리)이 실행 계획을 세우고, 동 주민센터(운영)가 일상 서비스를 제공합니다. 이 3계층이 서로 데이터를 공유하지 않으면, 같은 시민에게 여러 번 세금을 걷는 비효율이 발생합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

토픽 520번의 핵심은 COBIT 2019의 **Governance System Principles**(6개)와 **Components of a Governance System**(7개, 40개 세부 요소)입니다. 이를 ITIL 4의 Service Value Chain(34개 Practice)과 연계하고, ISO 38500의 6대 원칙(Evaluate, Direct, Monitor)으로 감독 체계를 구성하는 것이 표준적 아키텍처입니다.

```text
+--------------------------------------------------------------------+
|         COBIT 2019 + ITIL 4 + ISO 38500 통합 거버넌스 아키텍처     |
+--------------------------------------------------------------------+
|                                                                    |
|   [이사회/경영진] ---- ISO 38500 ED cycle -----> [감사위원회]       |
|        |                                              |            |
|        | ① 책임 (Responsibility)                       | 검증       |
|        | ② 전략 (Strategy)                             |            |
|        | ③ 취득 (Acquisition)                          |            |
|        | ④ 성과 (Performance)                          v            |
|        | ⑤ 준수 (Compliance)               [내부감사/외부감사]      |
|        | ⑥ 인적 행동 (Human Behavior)                  |            |
|        |                                              |            |
|        v                                              |            |
|   +------------------------------------------------------+        |
|   |            COBIT 2019 - 5개 도메인 + 40 목표          |        |
|   |  EDM: Evaluate, Direct, Monitor (5)                  |        |
|   |  APO: Align, Plan, Organize (14)                      |        |
|   |  BAI: Build, Acquire, Implement (11)                  |        |
|   |  DSS: Deliver, Service, Support (6)                   |        |
|   |  MEA: Monitor, Evaluate, Assess (4)                   |        |
|   +------------------------------------------------------+        |
|        |                                                           |
|        v                                                           |
|   +------------------------------------------------------+        |
|   |        ITIL 4 Service Value System (SVS)              |        |
|   |  -> Opportunity/Demand -> Value -> Service Provider     |        |
|   |  -> Service Value Chain: Plan->Engage->Design->          |        |
|   |      Transition->Obtain/Build->Deliver&Support->        |        |
|   |      Improve                                         |        |
|   |  -> 34 Practices: Incident, Problem, Change Enablement|        |
|   +------------------------------------------------------+        |
|        |                                                           |
|        v                                                           |
|   +------------------------------------------------------+        |
|   |         기술사 판단: KPI/KGI/CSF 연계 모델            |        |
|   |  KGI(Goal) <- CSF(Factor) <- KPI(Metric)               |        |
|   |  예: IT 비용 절감률(KGI) <- 인프라 자동화율(CSF)      |        |
|   |         <- CPU 사용률, 배포 빈도(KPI)                  |        |
|   +------------------------------------------------------+        |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 위원회 (IT Steering Committee)** | 의사결정·감독 | CFO·CDO·COO 합동 분기별 회의, RACI Matrix 기반 권한 위임, 의사결정 기록(Decision Log) 보관 |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리 | PPMS(Project Portfolio Management System) 활용, Earned Value Management(EVM, EAC/ETC/CPI/SPI), Stage-Gate 프로세스 운영 |
| **EA (Enterprise Architecture)** | 아키텍처 정합성 확보 | TOGAF 10 ADM(Architecture Development Method) 8단계, ArchiMate 3.2 표현 언어, Zachman Framework 6×6 매트릭스 |
| **ITSM (IT Service Management)** | 서비스 운영·개선 | ITIL 4 34개 Practice, CMDB(Configuration Management DB), AIOps 기반 Incident 자동 분류(MTTR 50%v) |
| **GRC (Governance, Risk, Compliance)** | 리스크·규제 통합 관리 | 통합 GRC 플랫폼(예: ServiceNow GRC, Archer), Three Lines of Defense 모델, KRI(Key Risk Indicator) 대시보드 |
| **정보보안 거버넌스** | 사이버 리스크 통제 | NIST CSF 2.0(Govern/Identify/Protect/Detect/Respond/Recover), Zero Trust Architecture, ISMS-P 인증 |

### 핵심 메커니즘: COBIT 2019의 7가지 거버넌스 구성요소

1. **Principles, Policies, Frameworks**: 의사결정 가이드라인 및 통제 정책
2. **Processes**: EDM, APO, BAI, DSS, MEA의 40개 관리 목표와 연계된 100여 개 활동
3. **Organizational Structures**: 이사회의 IT 전략 위원회, 운영위, 사용자 그룹
4. **Information Flows & Items**: BR(비즈니스 요구), PI(성과 지표), RC(리스크 인시던트)
5. **People, Skills, Competencies**: SFIA(Skills Framework for the Information Age) 7단계 역량 모델
6. **Culture, Ethics, Behavior**: 행동 강령(Code of Conduct), IT 윤리 헌장
7. **Services, Infrastructure, Applications**: IT 자원 (예: ServiceNow, Jira, Confluence, Power BI)

### KPI/KGI/CSF 인과 모델링 (Balanced Scorecard 4관점)

| BSC 관점 | KGI (최종 목표) | CSF (Critical Success Factor) | KPI (측정 지표) |
| :--- | :--- | :--- | :--- |
| 재무 (Financial) | IT 투자 ROI 20% 이상 | IT 비용 최적화, 포트폴리오 우선순위화 | TCO 절감률, Cost per Transaction |
| 고객 (Customer) | 사용자 만족도 4.5/5.0 | 서비스 카탈로그 다양화, 셀프 서비스 | CSAT, NPS, First Contact Resolution |
| 내부 프로세스 | 인시던트 MTTR 1시간 이내 | 자동화, 지식 관리 | MTTR, MTBF, Change Failure Rate |
| 학습·성장 | 디지털 역량 내재화 | 교육, 채용, 문화 | 인증 보유자 수, 직원 Engagement Score |

- **📢 섹션 요약 비유**: 거버넌스 시스템은 자동차의 '운전 보조 시스템(ADAS)'과 같습니다. COBIT는 도로 표지판(원칙), ISO 38500은 운전자의 윤리(책임), ITIL은 엔진 제어(운영) 역할을 합니다. KPI는 속도계·연료계·온도계 같은 계기판이고, 이를 통해 KGI(목적지 도착) 달성 여부를 실시간으로 판단합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 (ISACA) | ITIL 4 (AXELOS) | ISO/IEC 38500:2015 | PMBOK 7 (PMI) | NIST CSF 2.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 | IT 서비스 관리 | IT 거버넌스 원칙 | 프로젝트 관리 | 사이버보안 거버넌스 |
| **대상** | 전사 IT | 서비스 운영 | 이사회의 IT 책임 | 프로젝트 단위 | 보안 통제 |
| **구조** | 40 관리목표, 5 도메인 | 34 Practice, SVS | 6 원칙, ED 사이클 | 8 퍼포먼스 도메인 | 6 기능(Govern~Recover) |
| **적합 환경** | 대규모·규제 산업 | 운영成熟 조직 | 공공·대기업 | 단발성·프로젝트형 | 모든 사이버 환경 |
| **강점** | 정량적 목표·측정 | 실용적 운영 노하우 | 거버넌스 원칙의 단순화 | 정통 PM 방법론 | 사이버 리스크 통합 |
| **약점** | 구현 복잡성 높음 | 거버넌스 측면 약함 | 세부 통제 부재 | 거버넌스 측면 부재 | IT 운영 통제 미흡 |
| **연계 프레임워크** | ITIL, ISO 27001, TOGAF | COBIT, DevOps, SRE | COBIT, ISO 27001 | COBIT(거버넌스 연계) | COBIT, ISO 27001, RMF |
| **핵심 용어** | Capability Level (0~5) | Practice, Service Value Chain | Evaluate·Direct·Monitor | Principle, Domain | Function, Category, Subcategory |
| **인증 제도** | CGEIT, COBIT Foundation | ITIL 4 Foundation/MP/SL | ISO 38500 Lead Auditor | PMP, PfMP | CSF 인증 없음(자가진단) |
| **적용 시점** | 전략·감독 단계 | 운영 단계 | 최상위 감독 | 실행 단계 | 보안 운영 전 영역 |

### 통합 연계 아키텍처

```text
[전략] --- COBIT 2019 EDM 도메인 ----> [거버넌스 원칙]
              |                              |
              v                              v
[프로젝트] -- PMBOK 7, PRINCE2 -----> [사업 성과]
              |
              v
[서비스] ---- ITIL 4 SVS -----------> [운영 우수성]
              |                              |
              v                              v
[아키텍처] -- TOGAF, Zachman -------> [정합성]
              |
              v
[보안] ------ NIST CSF 2.0, ISO 27001 --> [리스크 관리]
              |
              v
[데이터] ---- DAMA-DMBOK, DCAM -----> [데이터 거버넌스]
```

토픽 520번의 핵심 시험 포인트는 **"각 프레임워크가 서로 보완적 관계"**임을 이해시키는 데 있습니다. COBIT 2019는 "WHAT(무엇을)" 정의하고, ITIL 4는 "HOW TO DELIVER(어떻게 제공할지)"를, PMBOK 7은 "HOW TO EXECUTE(어떻게 실행할지)"를, ISO 38500은 "WHY & WHO(왜, 누가)"를 다룹니다.

- **📢 섹션 요약 비유**: COBIT이 '헌법', ITIL이 '행정절차법', ISO 38500이 '대통령 훈령', PMBOK이 '각 부처 실무지침', NIST CSF가 '국방부 보안 규정'인 셈입니다. 이 5개가 서로 충돌하지 않고 위계적으로 작동해야 건강한 IT 국가 체제가 갖춰집니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **거버넌스 성숙도 진단**: COBIT 2019의 **Capability Level 0~5** 척도(ISO/IEC
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 520 / 800

<- **이전**: [519. IT 경영 관리 핵심 토픽 519번 시험 요약](/studynote/12_it_management/05_security_compliance/519_it_management_core_topic_519_exam_summary/)
**다음**: [521. IT 경영 관리 핵심 토픽 521번 시험 요약](/studynote/12_it_management/05_security_compliance/521_it_management_core_topic_521_exam_summary/) ->

---
