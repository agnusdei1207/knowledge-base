+++
title = "579. IT 경영 관리 핵심 토픽 579번 시험 요약 (IT Management Core Topic 579 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽은 **COBIT 2019 거버넌스 체계(Governance & Management Objectives 40개)**, **TOGAF 10 ADM 사이클**, **ITIL 4 Service Value System**을 통합한 **"전략–아키텍처–운영–성과" 4축** 의사결정 프레임워크로, 정보시스템의 투자 정당화(ROI/NPV/IRR/TCO)부터 EA 정합성 평가, SLA/KPI 기반 운영 통제, 감리·컴플라이언스(내부통제 5개 일반원칙, IS审计)까지 End-to-End로 다룬다.
> 2. **가치**: 정량적 효과로는 **IT 투자 ROI 평균 25~35% 개선**(Gartner 2023), **시스템 장애 MTTR 40% 단축**, **EA 적용 시 중복 투자 30% 절감**(The Open Group 사례); 정성적 효과로는 **이사회-경영진-IT 정렬(Alignment)** 강화, **ISO 38500/27001/COBIT** 다중 컴플라이언스 달성, **디지털 전환** 시 비즈니스-기술 간 갭 제거.
> 3. **판단 포인트**: 핵심 Trade-off는 ①**표준 프레임워크 채택 범위**(Full COBIT vs Domain-limited) ②**거버넌스-관리(Governance vs Management) 분리 수준** ③**Center of Excellence(CoE) vs Federated 모델** ④**Agile/DevOps 환경에서의 Waterfall 거버넌스 충돌** ⑤**클라우드/AI 도입 시 Shadow IT 통제**이며, 기술사는 **"비즈니스 요구->EA 원칙->프로세스->기술->측정"의 캐스케이드 일관성**을 기준으로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 업무의 단순 지원 수단을 넘어 **"디지털 비즈니스 코어"**로 자리잡은 4차 산업혁명 시대, IT 부서는 더 이상 **"Cost Center"**가 아닌 **"Value Creator"**로서 경영 성과에 직접 기여해야 한다. 그러나 국내·외 통계에 따르면 IT 프로젝트의 **약 70%(Standish Group CHAOS Report 2020)**가 실패 또는 성과 미달로 종료되며, 그 핵심 원인은 **전략 부재(37%)**, **요구사항 불완전(34%)**, **거버넌스 부재(29%)** 순으로 분석된다. 이에 **정보시스템 감리법**(2023년 전면 개정), **클라우드 컴퓨팅 발전 이용자 보호법**, **개인정보 보호법(PIPA)**, **AI 기본법(2025년 시행)** 등 규제 환경이 강화되면서 IT 경영 관리에 대한 체계적 접근이 필수적이다.

**기존 패러다임(전통적 IT 관리)**:
- 개별 시스템 단위 운영(Silo), 부서별 Vendor 종속, 사후 통제(Post-audit)
- ROI/TCO 측정 부재, 기술 중심 의사결정, IT와 비즈니스 전략 분리
- CapEx(자본적 지출) 위주 예산, 폐쇄형 아키텍처

**신규 패러다임(거버넌스 기반 IT 경영)**:
- **EA-거버넌스-ITSM 통합**, 표준 프레임워크(COBIT/TOGAF/ITIL) 기반 의사결정
- **BMC(Balanced Scorecard) + KPI/SLA** 기반 정량 평가, 비즈니스 가치 중심 투자
- **OpEx 전환**(클라우드), **플랫폼화**, **Data-Driven 의사결정**
- **Two-speed IT**(Mode 1: 안정성, Mode 2: 민첩성) 공존

```text
  +----------------------------------------------------------------------+
  |              [4차 산업혁명时代的 IT 경영 관리 통합 프레임워크]            |
  |                                                                      |
  |    +----------- 비즈니스 전략(Strategy) -----------+                  |
  |    |  • SWOT/Porter 5 Forces  • BMC/OKR           |                  |
  |    |  • 디지털 전환 로드맵(3~5년)                  |                  |
  |    +----------------+-----------------------------+                  |
  |                     | Cascading(연결)                                |
  |    +----------------v-----------------------------+                  |
  |    |      IT 거버넌스(Governance) — ISO 38500       |                  |
  |    |  • Responsibility(Evaluate-Direct-Monitor)    |                  |
  |    |  • COBIT 2019 40 Governance/Management Obj.   |                  |
  |    |  • RACI Matrix, Risk Appetite 정의            |                  |
  |    +----------------+-----------------------------+                  |
  |                     |                                                |
  |    +----------------v-----------------------------+                  |
  |    |        EA 아키텍처(Architecture) — TOGAF      |                  |
  |    |  • ADM(Architecture Development Method) Cycle |                  |
  |    |  • 4A: BA/DA/AA/TA -> 보안·데이터 아키텍처    |                  |
  |    |  • Repository(ArchiMate 3.2) 정합성           |                  |
  |    +----------------+-----------------------------+                  |
  |                     |                                                |
  |    +----------------v-----------------------------+                  |
  |    |   운영 및 서비스 관리(Operations) — ITIL 4     |                  |
  |    |  • SVS(Service Value System) 7 Guiding Princ. |                  |
  |    |  • 34 Practices, Service Value Chain(I->D->O)   |                  |
  |    |  • SLA/OLA/UC, Incident/Problem/Change        |                  |
  |    +----------------+-----------------------------+                  |
  |                     |                                                |
  |    +----------------v-----------------------------+                  |
  |    |     성과측정 및 개선(Measure) — BSC + KPI      |                  |
  |    |  • 4 관점(재무/고객/내부/학습성장)            |                  |
  |    |  • TCO·ROI·NPV·IRR·PP, EVA                   |                  |
  |    |  • 감리·IS Audit, 내부통제(5 Principles)       |                  |
  |    +---------------------------------------------+                  |
  |                                                                      |
  |   ↻ [Feedback Loop] -> 전략 재수립 및 Continual Improvement           |
  +----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **"건물의 설계도·건축 감리·하자 보수"** 시스템과 같다. EA는 **설계도**(어떻게 지을 것인가), 거버넌스는 **건축 감리**(규칙대로 짓고 있는가), ITIL은 **건물 운영·관리 매뉴얼**(지속 유지보수), KPI/BSC는 **건물의 수치화된 안전·만족도 지표**다. 이 중 하나라도 빠지면 빌라·아파트가 무너질 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **"전략->거버넌스->아키텍처->운영->성과"의 Cascading Model**이며, 이를 구현하는 3대 표준 프레임워크는 **상호 보완 관계**에 있다. COBIT은 **"무엇을(What) 관리할 것인가"**, TOGAF는 **"어떻게(How) 설계할 것인가"**, ITIL은 **"어떻게(How) 운영할 것인가"**에 답한다. ISO 38500은 이 모든 것을 **이사회(Board) 관점의 거버넌스 원칙(6 Principles: Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**으로 묶어준다.

```text
       +-------------------------------------------------------------+
       |           [3대 프레임워크의 통합 관계 및 적용 계층]            |
       +-------------------------------------------------------------+
                                   |
       +---------------------------+-------------------------------+
       |                           |                               |
       v                           v                               v
 +-------------+          +-----------------+            +--------------+
 |  COBIT 2019 |          |    TOGAF 10     |            |   ITIL 4     |
 |  (What)     |◄--------►|    (How-Design)  |◄----------►|   (How-Oper) |
 |             |   연계   |                  |   연계     |              |
 | • 40 Obj.   |          | • ADM Cycle     |            | • 34 Prac.   |
 | • 7 Compo.  |          | • 4 Architecture |            | • SVS        |
 | • 5 Focus   |          | • ADM Phases    |            | • 4 Dimens.  |
 |   Areas     |          |   A->B->C->D->E->F->G  |            |              |
 +------+------+          +--------+--------+            +------+-------+
        |                          |                             |
        |     +--------------------+---------------------+       |
        +-----►                                          ◄-------+
              |   +----------------------------------+   |
              |   |   ISO 38500 (이사회 거버넌스 원칙) |   |
              |   |  ① Responsibility  ② Strategy      |   |
              |   |  ③ Acquisition     ④ Performance   |   |
              |   |  ⑤ Conformance     ⑥ Human Beh.   |   |
              |   +----------------------------------+   |
              |                                          |
              +------------------+-----------------------+
                                 v
              +----------------------------------------+
              |  [성과측정 Layer]  BSC + KPI + 감리     |
              |   • 재무관점: ROI, NPV, IRR, TCO       |
              |   • 고객관점: SLA, NPS, 가용성         |
              |   • 내부: Change Success Rate, MTTR    |
              |   • 학습: 직원자격, 기술부채지수       |
              +----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (Control Objectives for Information and Related Technologies) | **IT 거버넌스·관리 목표 체계** | 40개 Governance/Management Objectives를 **5개 도메인**(EDM=5, APO=14, BAI=11, DSS=6, MEA=4)으로 분류. **7가지 구성요소(Components)**: Process, Organizational Structure, Information Flow, People/Skills, Policies/Procedures, Culture/Ethics, Services/Infrastructure/Applications. **Design Factor 11개**로 조직 상황에 맞는 거버넌스 시스템 맞춤 설계. |
| **TOGAF 10** (The Open Group Architecture Framework) | **EA(Enterprise Architecture) 수립 방법론** | **ADM(Architecture Development Method)**: Preliminary->A(Vision)->B/Business->C/Data·Application->D/Technology->E(Opportunities)->F/Migration->G/Implementation->H/Change Management의 **Phase A->H 반복 사이클**. **ArchiMate 3.2 표기법**(26개 요소) 기반 통합 모델링. **4A**(BA/DA/AA/TA) 정합성 평가. |
| **ITIL 4** (Information Technology Infrastructure Library) | **IT 서비스 관리(Service Management) 프레임워크** | **SVS(Service Value System)**: Opportunity/Demand -> Value -> **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) -> Value. **34개 Practice**, **7 Guiding Principles**(Focus on Value, Start Where You Are, Progress Iteratively, etc.). **4 Dimensions**: Organizations, Information, Technology, Partners & Suppliers. |
| **ISO 38500:2015** | **이사회 수준 IT 거버넌스 국제표준** | **3개 태스크 사이클**: **Evaluate**(현황 평가) -> **Direct**(지시/의사결정) -> **Monitor**(모니터링). **6 Principles**로 모든 IT 결정의 정당성 평가. 이사회 보고 체계(Board Reporting). |
| **성과측정 체계** (BSC + KPI + 감리) | **정량적 평가 및 책임 추적** | **Balanced Scorecard 4 관점** 기반 KPI 계층화(전략 KPI -> 프로세스 KPI -> 운영 KPI). **정보시스템 감리**(일반감리/상시감리/수시감리), **내부통제 5개 일반원칙**(COSO: Control Environment, Risk Assessment, Control Activities, Information & Communication, Monitoring Activities). |

**핵심 알고리즘/수식 — IT 경제성 분석**:

1. **ROI (투자수익률)** = (순이익 / 총 투자비용) × 100% ≥ 조직 Hurdle Rate(통상 10~15%)
2. **NPV (순현재가치)** = Σ[CFₜ / (1+r)ᵗ] - 초기투자; r=할인율, NPV≥0 시 투자 적정
3. **IRR (내부수익률)** = NPV=0이 되는 r; IRR > 할인율(r)일 때 투자 적정
4. **TCO (총소유비용)** = 직접비용(HW·SW·인력) + 간접비용(교육·다운타임·보안·감가) × 연수. 클라우드 전환 시 **CapEx -> OpEx** 모델로 TCO 구조 변화 고려
5. **Payback Period (회수기간)** = 초기투자 / 연평균 순현금흐름; 통상 3~5년 이내

**Cascading 원리** (전략적 일관성):
> "한 번의 결정이 하위 계층으로 전파되어야 한다" — Kaplan & Norton
> Strategy Map -> Scorecard -> Strategic Initiatives -> Projects -> Operational Metrics -> Individual Goals

- **📢 섹션 요약 비유**: COBIT은 **"회사 규정집"**, TOGAF는 **"설계 도면 작성 매뉴얼"**, ITIL은 **"매장 운영 SOP"**, ISO 38500은 **"이사회 의사결정 규칙"**, BSC/KPI는 **"경영 실적 보고서 양식"**이다. 이들은 서로 다른 책이지만, **한 서가의 같은 경영 시리즈**로서 시너지를 낸다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역은 유사하지만 서로 다른 철학을 가진 다수의 프레임워크가 존재한다. 기술사 시험에서는 이들의 **정확한 차이와 상호 연계**를 구분할 수 있어야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **TOGAF 10** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표 통제 | IT 서비스 관리 실무 표준 | 이사회 IT 거버넌스 원칙 | EA 개발·관리 방법론 | 프로젝트 관리 지식체계 |
| **대상 계층** | 이사회·CIO·감사·경영진 | IT 운영·서비스 매니저 | 이사회·최고 의사결정권자 | EA 아키텍트·전략기획 | 프로젝트 매니저·PMO |
| **핵심 산출물
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 579 / 800

<- **이전**: [578. IT 경영 관리 핵심 토픽 578번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/578_it_management_core_topic_578_exam_summary/)
**다음**: [580. IT 경영 관리 핵심 토픽 580번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/580_it_management_core_topic_580_exam_summary/) ->

---
