+++
title = "665. IT 경영 관리 핵심 토픽 665번 시험 요약 (IT Management Core Topic 665 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 **COBIT 2019**(40개 거버넌스/관리 목표, 5개 도메인), **ITIL 4**(Service Value System, 34개 Practice), **ISO 38500**(6원칙/3과제) 프레임워크를 통해 **비즈니스-IT 정렬(Business-IT Alignment)**, **가치 실현(Value Realization)**, **위험 최적화(Risk Optimization)**, **자원 관리(Resource Management)**를 달성하는 의사결정·통제·책임 체계이다.
> 2. **가치**: ISACA(2023) 조사에서 성숙한 COBIT 적용 조직은 **IT-Business 정렬도 67%->89% 향상**, **프로젝트 실패율 31% 감소**, **규제 컴플라이언스 비용 평균 23% 절감**, ISO 38500 적용 기업의 **이사회-현업 간 IT 의사결정 속도 2.4배 개선** 효과를 보고한다.
> 3. **판단 포인트**: 조직의 **규모(전사/부서/프로젝트)**, **규제 강도(금융/공공/일반)**, **운영 성숙도(Plan->Build->Run->Improve)**, **Agile/DevOps/Cloud-Native 전환 여부**에 따라 거버넌스 모델을 **중앙집중형(Federal)↔분산형(Devolved)↔하이브리드(Hybrid)**로 선택하고, **Design Factor 10종**(전략, 목표, 위험, 문제, 등)을 활용해 COBIT 5단계를 1단계 Governance System로 압축 적용하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 환경에서 IT는 더 이상 단순 지원(Support) 기능이 아니라 **전략적 차별화 자산(Strategic Differentiator)**이다. 그러나 2024년 Gartner 보고에 따르면 **전 세계 IT 예산의 약 30%(약 4.3조 달러)가 비즈니스 가치에 기여하지 못하는 'Shadow IT' 또는 'Zombie Project'**에 흡수되고 있으며, CIO의 **66%가 "IT 투자에 대한 비즈니스 정당화 부족"**을 최대 과제로 꼽았다. 이러한 **IT 가치 실현 실패(Value Leakage)** 문제는 디지털 전환(DX)·AI 도입 시대에 더욱 심화되고 있다.

특히 **근본 원인**은 기술 부재가 아니라 **거버넌스 부재**다. ① **이사회-경영진-IT 부서 간 책임 경계 모호**, ② **위험 관리와 가치 평가의 비연계**, ③ **프로세스·데이터·시스템의 사일로화**, ④ **규제(개인정보보호법, DORA, AI Basic Act, ESG) 대응의 사후적·단편적 접근**이 그것이다. 2000년대 닷컴버블, 2008 금융위기, 2017 Equifax, 2023 23andMe 해킹 등은 모두 **거버넌스 실패**에서 비롯되었다.

따라서 **IT 경영 관리**는 **"적정 IT가 적정 비즈니스 문제를 적정 시기에 적정 비용으로 적정 위험 수준으로 해결하는 것"**을 보장하는 통합 관리 체계이며, 이는 **COBIT 2019 + ITIL 4 + ISO 38500 + TOGAF + PMBOK/SAFe + ISO 27001/31000**의 다중 프레임워크 정렬(Multi-Framework Alignment)로 구현된다.

```text
+--------------------------------------------------------------------------+
|                 IT 경영 관리 거버넌스 스택 (Zachman 5W1H 매핑)            |
+--------------------------------------------------------------------------+
|  WHAT(데이터)     |  HOW(기능)         |  WHERE(네트워크)   |  WHO(조직) |
|  -------------    |  -------------     |  --------------   |  ---------|
|  데이터 거버넌스  |  프로세스 거버넌스 |  인프라/보안      |  역할/책임|
|  (DAMA-DMBOK)    |  (COBIT 2019 BPM)  |  (TOGAF/Togaf ADM)| (RACI/RASCI)|
|                  |                    |                    |  ISO 38500 |
|  WHY(동기)        |  WHEN(시간)         |                   |            |
|  -------------    |  -------------     |                   |            |
|  전략/사상/원칙   |  라이프사이클       |                   |            |
|  (Strategy)      |  (Plan->Build->Run)  |                   |            |
|  ISO 38500 6원칙  |  ITIL 4 SVS        |                   |            |
+--------------------------------------------------------------------------+
|      가치(Value) <------ 의사결정·통제·책임(Governance) ------> 위험(Risk)|
|      실현(Realization)     (COBIT 2019 EDM 도메인)         최적화     |
+--------------------------------------------------------------------------+
```

**구 vs 신 패러다임 비교**:
- **Old Paradigm (2000s)**: IT는 비용센터(Cost Center) -> CapEx 일회성 투자 -> 사후적 통제(Ex-post Audit) -> **기술 중심 의사결정** -> Waterfall 프로젝트 단위 거버넌스
- **New Paradigm (2024+)**: IT는 가치자본(Value Capital) -> **총비용(TCO)·총가치(TVO) 라이프사이클 관점** -> **사전 예방·실시간 통제(Continuous Assurance)** -> **비즈니스-공동 의사결정(Bimodal IT/BizDevOps)** -> **제품/플랫폼 단위 지속적 거버넌스**

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 도시계획(Urban Planning)**과 같습니다. 건물(시스템) 하나가 잘 지어져도 상하수도·도로·공원·치안 계획이 없으면 도시가 무너집니다. COBIT는 **종이도면**, ISO 38500은 **헌법 원칙**, ITIL 4는 **일상 운영 매뉴얼**에 해당하며, 이 셋이 맞물려야 **살고 싶은 디지털 도시**가 만들어집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 핵심 아키텍처

COBIT 2019는 **5개 도메인(Domain)**, **40개 거버넌스/관리 목표(GO/MO)**, **40개 Process**, **목표 연쇄(Goals Cascade)**, **설계 요인(Design Factors 11종)**으로 구성된다.

```text
                +-------------------------------------+
                |  Stakeholder Drivers & Concerns     |
                |  (이해관계자 Needs: 가치/위험/자원)  |
                +--------------+----------------------+
                               | Goals Cascade (13 Enterprise Goals
                               |  ↕ Alignment ↕ 13 IT Goals)
                +--------------v----------------------+
                |  Enterprise Goals (EG)              |
                |  EG01 포트폴리오 적정 수익          |
                |  EG05 고객 중심 문화                |
                |  EG12 디지털 트랜스포메이션 관리     |
                +--------------+----------------------+
                               | Mapping(우선순위 기반)
                +--------------v----------------------+
                |  IT-Related Goals (13개)            |
                |  ITG01 IT 준수·지원                 |
                |  ITG06 Agile/Digital 전환 지원       |
                |  ITG09 정보 처리 시설 사용 최적화    |
                +--------------+----------------------+
                               | Process Goals -> Enabler Goals
                +--------------v----------------------+
                |  COBIT 2019 40 Objectives (도메인 매핑)|
                |  EDM(5)  APO(14)  BAI(11)  DSS(6)  MEA(4)|
                +--+------+------+------+------+------+
                   |      |      |      |      |
                +--v--++--v--++--v--++--v--++--v--+
                |EDM  ||APO  ||BAI  ||DSS  ||MEA  |
                |평가 ||정렬 ||구축 ||운영 ||모니터|
                |지시 ||계획 ||변경 ||서비스||평가 |
                |감시 ||조직 ||수용 ||요청 ||성능 |
                |     ||위험 ||전환 ||장애 ||내부통제|
                |     ||품질 ||     ||보안 ||외부감사|
                |     || 등  ||     ||연속성||컴플라이언스|
                +-----++-----++-----++-----++-----+
                       |      |      |      |      |
                +------v------v------v------v------v-----+
                |   7 Components (Enablers)              |
                | ① Processes  ② Structures(Org)         |
                | ③ Information Flows  ④ People/Skills  |
                | ⑤ Services/Infrastructure              |
                | ⑥ Culture/Ethics  ⑦ Technology/Apps   |
                +---------------------------------------+
```

### 2. ITIL 4 Service Value System (SVS)

ITIL 4는 **서비스 가치 사슬(Service Value Chain, 6개 활동: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)** 중심의 **운영 거버넌스**를 다룬다.

```text
+------------------------------------------------------------+
|                  ITIL 4 Service Value System                |
+------------------------------------------------------------+
|  Opportunity/Demand <----> Value (Co-Creation)              |
|   +--------------------------------------------------+    |
|   |  Guiding Principles (7)                          |    |
|   |  ① Focus on value  ② Start where you are        |    |
|   |  ③ Progress iteratively  ④ Collaborate          |    |
|   |  ⑤ Think holistically  ⑥ Keep it simple         |    |
|   |  ⑦ Optimize and automate                         |    |
|   +--------------------------------------------------+    |
|                            v                               |
|  +---------+  +---------+  +---------+  +---------+     |
|  |Governance|  | Practices|  |Continual |  | 4 Dimens|    |
|  |(지배구조)|  |  (34)   |  | Improve  |  | Org·Info|    |
|  |         |  |일반14   |  |          |  | ·Tech·  |    |
|  |         |  |서비스19 |  |          |  | Partner |    |
|  |         |  |기술3    |  |          |  | ·Value  |    |
|  +---------+  +---------+  +---------+  +---------+     |
|                            ^                               |
|   Service Value Chain (Engage->Plan->Design&Transition       |
|   ->Obtain/Build->Deliver&Support->Improve)                  |
+------------------------------------------------------------+
```

### 3. ISO 38500 거버넌스 3-Task 모델

ISO/IEC 38500:2015 (Corporate governance of IT)는 **3-Task(Evaluate, Direct, Monitor)** 와 **6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 통해 **이사회-경영진의 IT 의사결정 거버넌스**를 정의한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (40 Objectives) | **E2E(End-to-End) IT 관리체계** | EDM(5)·APO(14)·BAI(11)·DSS(6)·MEA(4) 5도메인 40목표. **목표연쇄(Goals Cascade)**로 사업목표->IT목표->Enabler 자동 매핑, **Process Reference Model/PRM**에 RACI 매트릭스 내장, **Capability Level(0-5)** 및 **Maturity Model** 지원 |
| **ITIL 4** (34 Practices) | **서비스 운영·공급 거버넌스** | **SVS(Service Value System)**+Service Value Chain 6활동+34 Practice(일반관리 14+서비스 19+기술 3), **4 Dimensions**(조직·정보·기술·파트너·가치 흐름), **Continual Improvement Model** (Vision->Where->Where to be->How->Take action->Did we get there?), **ITIL Maturity Model** 5단계 |
| **ISO 38500** (6 Principles) | **이사회급 의사결정 거버넌스** | **3과제(Evaluate-Direct-Monitor)**+**6원칙**: 책임성(Responsibility), 전략(Strategy), 획득(Acquisition), 성능(Performance), 적합성(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 665 / 800

<- **이전**: [664. IT 경영 관리 핵심 토픽 664번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/664_it_management_core_topic_664_exam_summary/)
**다음**: [666. IT 경영 관리 핵심 토픽 666번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/666_it_management_core_topic_666_exam_summary/) ->

---
