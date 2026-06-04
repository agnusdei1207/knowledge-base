---
title: "740. IT 경영 관리 핵심 토픽 740번 시험 요약 (IT Management Core Topic 740 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(740번)는 **COBIT 2019 거버넌스 ↔ ITIL 4 서비스 운영 ↔ PMBOK 7th 프로젝트 ↔ ISO 27001 보안 ↔ TOGAF EA** 5대 프레임워크를 Business-IT Alignment 축으로 통합하여, IT를 비용센터(Cost Center)에서 가치창출센터(Value Center)로 전환시키는 경영 체계임.
> 2. **가치**: Forrester Research(2023) 기준 정렬된(Aligned) 기업은 EBITDA 2.3배, 디지털 전환 성공률 68%(McKinsey 2022) 향상, ISMS-P 인증 기업의 보안사고 평균 복구비용 47% 절감(IBM Cost of Data Breach 2023) 등 정량적 ROI 확보.
> 3. **판단 포인트**: **"거버넌스-관리-운영" 3계층 분리**, **RACI 매트릭스 기반 의사결정 권한 분배**, **IT 투자 포트폴리오의 Run/Grow/Transform 비중 최적화**가 핵심 트레이드오프이며, 특히 클라우드-온프레미스 하이브리드 환경에서 Zero Trust, FinOps, AIOps 도입 우선순위 결정이 기술사 출제 핵심.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화로 IT는 더 이상 후방지원 기능이 아닌 **전략 동력원(Strategic Enabler)**입니다. 740번 IT 경영 관리 토픽은 정보관리기술사, 컴퓨터시스템응용기술사 시험에서 매년 1~2문항씩 출제되며, **"IT와 경영을 어떻게 연결할 것인가"**에 대한 통합적 판단 능력을 검증합니다. 과거(2010년대 이전)에는 IT 관리를 **시스템 개발·운영의 기술적 문제**로 국한했으나, 현재는 **거버넌스-전략-포트폴리오-서비스-프로젝트-보안-아키텍처**를 아우르는 경영학(Management Science) 영역으로 확장되었습니다.

특히 2024년 이후 **AI 거버넌스(AI Act, NIST AI RMF)**, **클라우드 FinOps**, **제로트러스트(Zero Trust)**, **ESG-IT(그린 IT)**가 신규 출제 키워드로 부상하면서, 단순 암기형 답안이 아닌 **상황별 의사결정 시나리오 문제** 비중이 60% 이상으로 증가했습니다.

```text
+--------------------------------------------------------------------+
|         740번 IT 경영 관리 5대 영역 통합 프레임워크 (BLAPES)        |
+--------------------------------------------------------------------+
                            +----------+
                            |  Board   | <- 이사회/경영진 (전략·예산)
                            +----+-----+
                                 | 의사결정
            +--------------------+--------------------+
            v                    v                    v
   +----------------+   +----------------+   +----------------+
   |  Governance    |   |   Management   |   |   Operations   |
   |   (거버넌스)    |<--->|     (관리)     |<--->|    (운영)      |
   |  COBIT 2019    |   |  ITIL 4 / PMBOK|   |  AIOps / SRE   |
   |  ISO 38500     |   |  ISO 27001     |   |  DevOps        |
   +--------+-------+   +--------+-------+   +--------+-------+
            |                    |                    |
            +--------------------+--------------------+
                                 v
                  +--------------------------+
                  |  Business-IT Alignment   |
                  |  (비즈니스-IT 정렬)       |
                  +------------+-------------+
                               v
                  +--------------------------+
                  |  Enterprise Architecture |
                  |  (TOGAF ADM / Zachman)   |
                  +--------------------------+
```

**📢 섹션 요약 비유**: IT 경영 관리는 **"도시 계획(Urban Planning)"**과 같습니다. 건물 하나(시스템)만 짓는 게 아니라, 도로·상하수도·전기·보안·법규·재정·시민만족도를 **동시에 설계**해야 도시에 사는 사람들이 행복해집니다. 740번 시험은 "도시 설계자(Chief Architect)"의 자격증을 시험하는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 740번은 5개의 핵심 메가 프로세스로 구성되며, 각각은 국제 표준 프레임워크에 매핑됩니다.

```text
+------------------------------------------------------------------+
|         IT 경영 관리 5대 메가프로세스 및 표준 매핑                  |
+------------------------------------------------------------------+
   +------------------+
   | 1) IT 전략/거버넌스| --->  COBIT 2019, ISO/IEC 38500
   +--------+---------+
            v
   +------------------+
   | 2) IT 포트폴리오  | --->  Stage-Gate, BCG Matrix, WSJF (SAFe)
   +--------+---------+
            v
   +------------------+
   | 3) IT 프로젝트관리 | --->  PMBOK 7th, PRINCE2, Agile (Scrum/Kanban)
   +--------+---------+
            v
   +------------------+
   | 4) IT 서비스운영   | --->  ITIL 4 Service Value System, ISO 20000
   +--------+---------+
            v
   +------------------+
   | 5) IT 보안/리스크  | --->  ISO 27001, ISMS-P, NIST CSF, Zero Trust
   +------------------+
```

### (1) IT 거버넌스 (IT Governance) - COBIT 2019

**COBIT 2019**는 ISACA에서颁布한 전 세계 가장 보편적인 IT 거버넌스 프레임워크로, 5개 도메인(40개 관리목표)을 통해 IT를 평가·지도·모니터링합니다.

| COBIT 2019 도메인 | 관리 목표 수 | 핵심 질문 | 연계 표준 |
| :--- | :---: | :--- | :--- |
| **EDM** (Evaluate, Direct, Monitor) | 5 | IT가 비즈니스 목표에 부합하는가? | ISO 38500 |
| **APO** (Align, Plan, Organize) | 14 | IT 전략과 포트폴리오를 어떻게 수립? | PMBOK, ISO 38500 |
| **BAI** (Build, Acquire, Implement) | 11 | 솔루션을 어떻게 구축·도입? | PMBOK, ITIL 4 |
| **DSS** (Deliver, Service, Support) | 6 | IT 서비스를 어떻게 안정 운영? | ITIL 4, ISO 20000 |
| **MEA** (Monitor, Evaluate, Assess) | 4 | 성과를 어떻게 측정·감사? | ISO 27001, ISMS-P |

**핵심 원리**: COBIT 2019는 **"Governance System"**을 5가지 **연관 요인(Design Factors)**으로 구성합니다:
- 전략적 목표(Strategy)
- 목표 cascaded(Enterprise Goals ↔ Alignment Goals ↔ IT Goals)
- 리스크 프로파일(Risk Profile)
- 이슈/사고 관련성(Issues/Concerns)
- 위협 환경(Threat Landscape)
- **준거 요건(Compliance Requirements)** <- 2024년 신규 중시

### (2) IT 서비스 관리 - ITIL 4

**ITIL 4**(2019, AXELOS)는 **Service Value System(SVS)** 중심으로 재설계되었으며, 7가지 Guiding Principles와 34개 Practices로 구성됩니다.

```text
+--------------------------------------------------------------+
|                  ITIL 4 Service Value System (SVS)            |
+--------------------------------------------------------------+
   +----------+    Opportunity/Demand    +------------------+
   |  기회/   | -----------------------> |   Service Value   |
   |  수요    |                         |      Chain        |
   +----------+                         |  (6개 활동)       |
        ^                                +------+-----------+
        |  Value                              |
        |                                       v
   +----------+                         +------------------+
   | 가치공급 | <----------------------- |    Practices      |
   |  조직    |   결과/성과             |  (34개 관행)      |
   +----------+                         +------------------+
                  ^
                  | Guiding Principles (7)
                  | 1) Focus on Value
                  | 2) Start Where You Are
                  | 3) Progress Iteratively with Feedback
                  | 4) Collaborate and Promote Visibility
                  | 5) Think and Work Holistically
                  | 6) Keep It Simple and Practical
                  | 7) Optimize and Automate
```

### (3) IT 프로젝트 관리 - PMBOK 7th vs Agile

PMBOK 7th(2021)는 **12 Principles of Project Management + 8 Performance Domains** 구조로 전환되어, 방법론 중립(Methodology-agnostic)입니다. 740번 시험에서는 **Predictive(Waterfall) vs Adaptive(Agile) vs Hybrid** 선택 기준을 묻는 문제가 빈출됩니다.

| 구분 | Predictive (Waterfall) | Adaptive (Agile) | Hybrid |
| :--- | :--- | :--- | :--- |
| **요구사항 명확성** | 높음 (정형 요건) | 낮음 (불확실) | 부분 명확 |
| **변경 빈도** | 낮음 | 높음 | 중간 |
| **적합 프로젝트** | 건설, ERP, SI | SaaS, 앱, AI 모델 | SI+운영 동시 |
| **측정 지표** | CV, SV, CPI, SPI | Velocity, Burn-down | 결합 KPI |
| **리스크 관리** | 사전 분석, 베이스라인 | 백로그 우선순위 | 페이즈별 게이트 |

### (4) 정보 보안 관리 - ISO 27001:2022

2022년 개정된 ISO 27001은 **Annex A 통제 항목이 114개에서 93개로 통폐합**되었으며, 4개 영역(Organizational, People, Physical, Technological)으로 재분류되었습니다.

```text
+--------------------------------------------------------------+
|       ISO 27001:2022 Annex A 통제영역 (4 Themes)             |
+--------------------------------------------------------------+
   +------------------+  +------------------+
   | A.5 Organizational|  |  A.6 People      |
   |    (37 통제)       |  |   (8 통제)        |
   +--------+---------+  +--------+---------+
            |                       |
            +-----------+-----------+
                        v
            +-------------------------+
            |  ISMS (정보보호경영체계)  |
            |  PDCA + 위험평가 + SOA   |
            +------------+------------+
                         |
            +------------+------------+
            v                         v
   +------------------+  +------------------+
   | A.7 Physical     |  | A.8 Technological|
   |   (14 통제)       |  |   (34 통제)        |
   +------------------+  +------------------+
   * 한국: ISMS-P (정보보호 및 개인정보보호 관리체계) 인증
   * NIST CSF 2.0 (2024) -> Govern 신규 추가
```

**제로트러스트(Zero Trust)**: 2024년 기준 740번 출제 키워드 1위. NIST SP 800-207 기준으로 **"Never Trust, Always Verify"** 원칙, **Policy Decision Point(PDP) / Policy Enforcement Point(PEP)** 분리, **마이크로세그멘테이션**, **최소 권한(Least Privilege)** 기반. 한국에서는 2023년 **클라우드 보안인증制度(CSAP)** 강화로 가시화.

### (5) 엔터프라이즈 아키텍처 (EA) - TOGAF ADM

**TOGAF**(The Open Group Architecture Framework) 9.2 + 10차 개정예고(2024~)는 **Architecture Development Method(ADM)** 8단계 사이클로 EA를 수립합니다.

```text
+--------------------------------------------------------------+
|                  TOGAF ADM Cycle (8 Phases)                   |
+--------------------------------------------------------------+
              +-----------------------+
              |  Preliminary (준비)    |
              +-----------+-----------+
                          v
        +----------+   A   +----------+
        | Business |◄-----►|  Data    |  ◄-- Architecture
        | Arch.    |       |  App.    |      Repositories
        +----+-----+       +----+-----+      (Continuum)
             |                  |
        +----v-----+       +----v-----+
        |  Tech.   |◄-----►| Opport. |
        |  Arch.   |       | & Sol.  |
        +----+-----+       +----+-----+
             +----------+--------+
                        v
              +-----------------------+
              | H. Architecture      |
              |    Change Management  |
              +-----------+-----------+
                          v
              +-----------------------+
              | F. Migration Planning |
              | G. Implementation     |
              |    Governance         |
              | E. Requirements Mgmt. |
              |  (전 단계 공통)         |
              +-----------------------+
```

**📢 섹션 요약 비유**: 이 5대 영역은 **"병원의 5개 진료과"**와 같습니다. **거버넌스=원무과(보험·법규)**, **프로젝트관리=진료과(치료)**, **서비스관리=간호과(돌봄)**, **보안=감염관리실(안전)**, **EA=건축과(설계)**. 종합병원처럼 5개가 동시에 돌아가야 환자가 회복(=비즈니스 목표 달성)됩니다.

---

## Ⅲ. 비교 및 연결

### (1) 5대 프레임워크 비교

| 구분 | **COBIT 201
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 740 / 800

<- **이전**: [739. IT 경영 관리 핵심 토픽 739번 시험 요약](/studynote/12_it_management/05_security_compliance/739_it_management_core_topic_739_exam_summary/)
**다음**: [741. IT 경영 관리 핵심 토픽 741번 시험 요약](/studynote/12_it_management/05_security_compliance/741_it_management_core_topic_741_exam_summary/) ->

---
