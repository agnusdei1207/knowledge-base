---
title: "679. IT 경영 관리 핵심 토픽 679번 시험 요약 (IT Management Core Topic 679 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 679. IT 거버넌스 및 COBIT 2019 기반 IT 경영 관리

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 6개 거버넌스 시스템 원리, 40개 관리 목표(APO/DSS/MEA/EDM/BAI), 7개 컴포넌트(Process/Organizational Structures/Information/Flows/People/Skills/Culture)를 통해 비즈니스 가치와 IT를 정렬시키는 개방형 거버넌스 프레임워크임
> 2. **가치**: ISACA 보고서 기준 COBIT 적용 조직은 IT 위험 감소 38%, 컴플라이언스 비용 27% 절감, 프로젝트 성공률 1.7배 향상, ROI 30~45% 개선 효과를 입증함
> 3. **판단 포인트**: 집중형(Federal) vs 분산형(Divisional) 거버넌스 모델 선택, Agile-Safe-Scrum 환경과의 통합, ISO 38500/27001/CMMI와 매핑 정밀도, 그리고 사이버보안·ESG 컴플라이언스 통합 수준이 핵심 의사결정 변수

---

## Ⅰ. 개요 및 필요성

전통적인 IT 관리는 기술 도입과 운영 효율에 집중했으나, 2010년대 이후 클라우드·AI·데이터 경제로 패러다임이 전환되면서 IT 자체가 **비즈니스 핵심 자산**이자 **전략적 경쟁 무기**로 재정의되었다. 이에 따라 ISO/IEC 38500:2015, COBIT 2019, ITIL 4, ISO/IEC 27001:2022 등 다수의 거버넌스 표준이 등장했으며, 특히 **COBIT 2019**는 ISACA가 2018년 12월 발표(2019년 4월 정식 공개)하면서 7년 만의 전면 개편을 통해 6개 원칙, 5개 도메인, 40개 관리목표 체계로 재구성되었다.

기존 COBIT 5는 폐쇄형 5개 원리(Enabler) 기반이었으나, COBIT 2019은 **개방형 6원리(Governance System Principles) + 3원리(Goals Cascade)**로 확장되어 DevOps, Agile, Lean, 디자인씽킹 등 현대적 관리방법론을 유연하게 흡수할 수 있게 되었다. 또한 **Focus Area**(예: 사이버보안, DevOps, 위험, 컴플라이언스, ESG, 디지털 윤리 등 40여 개) 개념을 도입하여, 조직이 자사의 우선순위에 맞춰 목표·프로세스를 커스터마이징할 수 있는 구조로 진화했다.

```text
[ IT 거버넌스 진화 흐름도 ]

   1992          2000        2005         2012         2018~2019         2023~
 +------+     +------+    +------+    +------+      +----------+    +--------+
 |COBIT |----->|COBIT3|---->|COBIT4|---->|COBIT5|------>|COBIT 2019|---->|COBIT  |--->
 |초기판|     |프로세|    |통제  |    |원리  |      |개방형    |    |2025+   |
 |      |     |스중심|    |목표중|    |5원리 |      |6원리체계 |    |AI/Native
 +------+     +------+    +------+    +------+      +----------+    +--------+
     |            |           |           |               |              |
     v            v           v           v               v              v
  감사중심     ITIL v2     ITIL v3    ISO 38500      ITIL 4       NIST CSF 2.0
  통제위주     ITSM 등장   서비스전략  IT거버넌스     SVS(Value     Zero Trust
                                          원칙         Co-creation)  통합
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | Old Paradigm (Pre-2015) | New Paradigm (2019~) |
| :--- | :--- | :--- |
| 관점 | IT는 비용센터(Cost Center) | IT는 가치창출 동인(Value Driver) |
| 통제 | 사후감사, 정적 통제 | 실시간 Risk Posture, 동적 통제 |
| 조직 | 수직적(Waterfall), 부서별 사일로 | Agile/Squad 기반, 플랫폼 엔지니어링 |
| 컴플라이언스 | 연 1회 점검, 문서 중심 | Continuous Compliance, GRC 자동화 |
| 투자관점 | CapEx 위주, TCO 5년 회수 | OpEx/Pay-as-you-go, TBM(Tech Business Mgmt) |
| 보안접근 | Perimeter, Network-Centric | Zero Trust, Identity-Centric |

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **'도시의 종합规划设计(토지이용·교통·환경·안전을 통합 설계하는 도시계획)'** 과 같다. 개별 건물을 잘 짓는 것(프로젝트 관리)만으로는 도시 전체가 혼잡해지므로, 도시 차원의 청사진(거버넌스 프레임워크)이 필요하며 그 안에서 개별 건물(프로세스/프로젝트)을 유연하게 짓는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 다음의 **3계층 구조**로 설계되었다.

1. **Governance System (거버넌스 시스템)**: 6원리 + 목표연쇄(Goals Cascade) + 컴포넌트
2. **Governance Framework (거버넌스 프레임워크)**: Focus Area, 설계요인(Design Factors), 목표 계보
3. **Governance and Management Objectives (거버넌스 및 관리목표)**: 5개 도메인의 40개 목표

**6대 거버넌스 시스템 원리(Governance System Principles)**
- ① **Each Enterprise has different needs (조직별 상이성)**
- ② **Governance system should cover the enterprise end-to-end (전사적 커버리지)**
- ③ **Apply a single integrated framework (단일 통합 프레임워크)**
- ④ **Enable a holistic approach (총체적 접근)**
- ⑤ **Distinguish governance from management (거버넌스와 관리의 분리)**
- ⑥ **Tailor the system to enterprise needs (맞춤형 설계)**

**3대 거버넌스 시스템 원리(Goals Cascade 원리)**
- ① **Stakeholder needs -> Enterprise Goals -> IT-related Goals -> Enablers**
- ② **Goals Cascade 적용 시 Realistic, Measurable, Time-bound 조건 충족**
- ③ **각 단계에서 RACI 매트릭스로 책임 소재 명확화**

```text
[ COBIT 2019 거버넌스 시스템 아키텍처 ]

+--------------------------------------------------------------------+
|                       Stakeholder Needs                            |
|            (수익성, 리스크 최적화, 고객만족, ESG 등)                  |
+-------------------------+------------------------------------------+
                          v Goals Cascade (13 Enterprise Goals)
+--------------------------------------------------------------------+
|                  Enterprise Goals (13개)                            |
|  EG01 포트폴리오, EG02 경쟁력, EG05 재무, EG06 서비스, EG09 최적화  |
+-------------------------+------------------------------------------+
                          v Alignment (13 -> 13 IT Goals)
+--------------------------------------------------------------------+
|              IT-related Goals (13개)                               |
|  EG01 만족, EG02 IT전략, EG03 위험관리, EG04 품질, EG09 보안 등     |
+-------------------------+------------------------------------------+
                          v Map to Objectives (40개 관리목표)
+--------------------------------------------------------------------+
|  EDM(5)   | APO(14)   | BAI(11)   | DSS(6)    | MEA(4)            |
| 거버넌스   | 정렬·계획   | 구축·인수  | 운영·지원  | 모니터링·평가      |
+-------------------------+------------------------------------------+
                          v 7 Components (Components of the System)
+--------------------------------------------------------------------+
| ① Process  ② Org Structure  ③ Information  ④ People/Skills        |
| ⑤ Flow/Items ⑥ Culture/Ethics ⑦ Service/Infrastructure/Apps      |
+--------------------------------------------------------------------+
                          v Focus Areas (40+ Contextual)
  +---------+ +---------+ +---------+ +---------+ +---------+
  |Cybersec | |DevOps   | |Risk     | |Privacy  | |ESG/    |
  |urity    | |         | |Mgmt     | |         | |Digital |
  |         | |         | |         | |         | |Ethics  |
  +---------+ +---------+ +---------+ +---------+ +---------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·경영진의 거버넌스 의사결정 | EDM01 전략설정, EDM02 Benefit Realization, EDM03 Risk Optimization, EDM04 Resource Optimization, EDM05 Stakeholder Transparency — 의사결정 권한과 책임의 분리 |
| **APO (Align, Plan, Organize)** | IT 전략과 기업목표 정렬, 계획수립 | APO01~14 (예: APO12 위험관리, APO13 보안관리) — Balanced Scorecard, OKR, Portfolio Mgmt, TBM |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·변경·도입 | BAI01~11 (예: BAI03 변경관리, BAI11 프로젝트관리) — Agile/DevOps 통합, CI/CD 파이프라인 |
| **DSS (Deliver, Service, Support)** | 일상의 서비스 운영과 지원 | DSS01~06 (예: DSS02 인시던트, DSS05 보안운영) — ITIL 4 Service Value System, AIOps |
| **MEA (Monitor, Evaluate, Assess)** | 성과, 통제, 컴플라이언스 모니터링 | MEA01~04 (예: MEA03 컴플라이언스, MEA04 Assurance) — GRC 도구, Continuous Audit |
| **7개 컴포넌트** | 시스템 운영의 총체적 토대 | Process 40개 + Org Structure(예: IT Steering Committee) + Information Layer + People/Skills(역량모델) + Flows(예: 보고체계) + Culture(윤리·행동강령) + Services/Infrastructure |
| **Focus Areas** | 컨텍스트 기반 맞춤형 적용 | 사이버보안, DevOps, 디지털 윤리, ESG, 클라우드 거버넌스, 데이터 거버넌스, AI 거버넌스 등 40여 개 |

**핵심 기법: Goals Cascade와 Capability/Maturity 매핑**

Goals Cascade는 13개 Enterprise Goal과 13개 IT-related Goal, 40개 Management Objective를 매핑하는 핵심 메커니즘이다. 각 매핑은 **Primary(P, 1.0)** / **Secondary(S, 0.5)** 가중치로 표현된다. 예를 들어 EG01(재무적 가치창출) -> IT-related Goal 01(IT의 이해관계자 가치 제공) -> EDM02(Benefit Realization) -> APO05(Portfolio Management)의 연쇄 구조를 가진다.

**Maturity Level (ISO/IEC 15504 PAM 기반)**
- Level 0: Incomplete
- Level 1: Initial (정형화 부재, 성공 우연)
- Level 2: Managed (프로젝트 단위 관리)
- Level 3: Defined (조직 표준화, 프로세스 자산화)
- Level 4: Quantitatively Managed (KPI 측정 가능)
- Level 5: Optimizing (지속적 개선, Innovation)

**Process Capability Rating**: N -> P -> L -> F -> I (Not Achieved -> Partially -> Largely -> Fully -> Innovating)

- **📢 섹션 요약 비유**: COBIT 2019의 6원리는 **'헌법'**, 40개 관리목표는 **'법률 조항'**, Focus Area는 **'특별법(특정 산업/이슈에 적용되는 법)'**, 그리고 조직의 실제 운영은 **'판례·행정 실무'** 와 같다. 헌법의 기본 정신 위에 다양한 법률이 있고, 특별법으로 특화 산업을 다스리며, 실무는 구체적 판례로 구현된다.

---

## Ⅲ. 비교 및 연결

IT 거버넌스는 단일 프레임워크가 아니라 **다중 프레임워크의 통합 체계**로 이해해야 한다. 다음은 자주 혼동되는 핵심 프레임워크 간 비교이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI 2.0** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 관점** | IT 거버넌스·관리 통합 | IT 서비스 운영·가치공동창조 | IT 의사결정 거버넌스 원칙 | 프로세스 능력·성숙도 | 엔터프라이즈 아키
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 679 / 800

<- **이전**: [678. IT 경영 관리 핵심 토픽 678번 시험 요약](/studynote/12_it_management/05_security_compliance/678_it_management_core_topic_678_exam_summary/)
**다음**: [680. IT 경영 관리 핵심 토픽 680번 시험 요약](/studynote/12_it_management/05_security_compliance/680_it_management_core_topic_680_exam_summary/) ->

---
