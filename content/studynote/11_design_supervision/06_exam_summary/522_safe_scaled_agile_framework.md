---
title: "522. SAFe 대규모 애자일 프레임워크 (SAFe Scaled Agile Framework)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAFe(Scaled Agile Framework)는 Dean Leffingwell이 체계화한 엔터프라이즈 규모 Agile 확장 프레임워크로, Agile Release Train(ART)이라는 50~125명 단위의 장기 팀을 중심으로 Lean-Agile 원칙, Cadence-based PI Planning, 그리고 4계층(Team/Program/Large Solution/Portfolio) 구조를 통해 Business Agility를 구현한다.
> 2. **가치**: Forbes Insights 조사(2018)에 따르면 SAFe 도입 기업의 75%가 시장 출시 시간(TTM) 단축, 70%가 생산성 향상, 60%가 품질 개선 효과를 보고했으며, PI Planning을 통한 8~12주 단위의 동기화된 실행으로 Portfolio Epics의 Flow Time을 평균 30~50% 감소시킬 수 있다.
> 3. **판단 포인트**: 단순 팀 단위 Agile로는 해결 불가능한 엔터프라이즈 규모의 의존성 관리, 전략 정렬(Strategic Alignment), 아키텍처 런웨이(Architectural Runway) 확보 문제를 다루지만, 경직성(Bureaucracy) 증가, 역할 중복(RTE/RTM/PM 중첩), "SAFe in name only(SINO)" 안티패턴 발생 위험이 있어 조직 문화 성숙도(Level 2~3)와 도메인 적합성(규제 산업 vs 일반 SW) 평가가 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

기존 Scrum, XP, Kanban 등 단일 팀(5~9명) 대상 Agile 방법론은 팀 내 Delivery는 가속화할 수 있으나, 100명 이상의 다수 팀이 참여하는 엔터프라이즈 시스템(예: 자동차 SDV(Software Defined Vehicle), 금융 코어뱅킹, 통신 BSS) 개발에서는 **팀 간 의존성(Inter-team Dependency)**, **전략-실행 갭(Strategy-Execution Gap)**, **아키텍처 통합(Architectural Runway)**, **규제 준수(Compliance)** 문제를 해결하지 못한다. SAFe v6.0(2023)은 Scaled Agile Inc.가 2011년 v1.0 출시 이후 5차례 주요 개정을 거친 프레임워크로, **Lean-Agile Mindset**, **7가지 Core Values**, **21가지 Lean-Agile Principles**, **4가지 Configurations**(Essential, Large Solution, Portfolio, Full)를 통해 **Business Agility** 달성을 목표로 한다.

핵심 도입 동기는 ① **디지털 트랜스포메이션**(Legacy -> Cloud-Native 전환), ② **규제 대응**(FDA, ISO 26262, PCI-DSS 등 Safety/Security 요구사항), ③ **고정가(Fixed-Price) 계약에서의 예측 가능성(PI 단위 데모 기반)** 등이다. SAFe는 단순 프로세스가 아닌 **Lean 사고방식 + Agile 실행 + 시스템 사고(System Thinking)**를 결합한 운영체제(Operating System for Business Agility)로 기능한다.

```text
+------------------------------------------------------------------------+
|                    엔터프라이즈 Agile 확장 문제 공간                        |
+------------------------------------------------------------------------+
|                                                                        |
|  단일 팀 Scrum      -> 다수 팀 협업 필요성 증가 (수십~수백 팀)             |
|         |                         |                                    |
|         v                         v                                    |
|  +----------+             +------------------+                         |
|  | 1~2 Teams|             | 50~125 Teams     |                         |
|  | (5~18명)  |             | (ART 단위)        |                         |
|  |          |             |                  |                         |
|  | 의존성:  |             | 의존성:           |                         |
|  | - 백로그 |             | - API 계약        |                         |
|  | - 스탠드 |             | - 공유 컴포넌트    |                         |
|  | - 회고   |             | - 데이터 스키마    |                         |
|  +----------+             | - 인프라           |                         |
|                          | - 규제             |                         |
|   ❌ 한계 도달            +------------------+                         |
|                                |                                        |
|                                v                                        |
|              +--------------------------------------+                  |
|              |  SAFe 4-Layer Scalable Architecture  |                  |
|              |  +--------------------------------+  |                  |
|              |  | Portfolio (전략/투자)           |  |                  |
|              |  +--------------------------------+  |                  |
|              |  | Large Solution (솔루션 트레인)   |  |                  |
|              |  +--------------------------------+  |                  |
|              |  | Program (ART) <- 50~125명/팀단위|  |                  |
|              |  +--------------------------------+  |                  |
|              |  | Team (Scrum/Kanban/XP)         |  |                  |
|              |  +--------------------------------+  |                  |
|              +--------------------------------------+                  |
+------------------------------------------------------------------------+
```

전통적 Waterfall 대비 SAFe는 ① 고정 박자(Cadence)와 동기화(Synchronization)를 통한 변동성 흡수, ② Cadence-based PI Planning으로 8~12주 단위 비즈니스 가치 전달, ③ WIP(Work In Progress) 제한과 클래스-A/B/C 분기로 Flow 최적화를 달성한다. 그러나 이는 **Lean 원리 기반의 전사적 변화**를 전제로 하므로, 단순 프로세스 도입만으로는 효과가 미미하다(SAFe SINO 현상).

- **📢 섹션 요약 비유**: SAFe는 마치 **도시의 종합 교통 시스템**과 같습니다. 단일 팀 Agile은 자전거(빠르지만 적재량 한계)이고, SAFe는 지하철·고속도로·물류 네트워크(ART=노선, PI=배차간격, Program Increment=정기 운행 스케줄)처럼 도시 전체의 흐름을 설계하는 메타 운영 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SAFe v6.0 아키텍처는 **4계층 구조**와 **3가지 Body of Knowledge**로 구성된다. 본질적으로 Toyota Production System의 **Heijunka(평준화)**, **Jidoka(自働화)**, **Pull System**을 IT 개발에 적용한 것이다. 아래 ASCII 다이어그램은 Full Configuration의 4계층 및 주요 Artifact 흐름을 나타낸다.

```text
+-------------------------------------------------------------------------+
|  Portfolio Layer (전략/투자 거버넌스)                                    |
|  +-------------------------------------------------------------------+  |
|  | LPM(Lean Portfolio Management) | Strategic Themes | Portfolio    |  |
|  | Backlog | Epic Owners | Value Stream | Lean Budget Guardrails     |  |
|  +----------------+--------------------------------------------------+  |
|                   | Epic (투자 단위, MMF=Minimum Marketable Feature 집합)|
|                   v                                                      |
|  +-------------------------------------------------------------------+  |
|  | Large Solution Layer (솔루션 트레인, 선택적)                        |  |
|  | +----------+  +----------+  +----------+  Capability              |  |
|  | | Solution |  | Solution |  | Solution |  Enabler                 |  |
|  | |   Train  |  |   Train  |  |   Train  |  (아키텍처/규제)         |  |
|  | +----+-----+  +----+-----+  +----+-----+                          |  |
|  +------+-------------+-------------+---------------------------------+  |
|         |             |             |                                    |
|         v             v             v                                    |
|  +-------------------------------------------------------------------+  |
|  | Program Layer (ART = Agile Release Train, 핵심)                    |  |
|  | +----------+  +----------+  +----------+  +----------+            |  |
|  | | Agile    |  | Agile    |  | Agile    |  | Agile    |  ...       |  |
|  | | Team #1  |  | Team #2  |  | Team #3  |  | Team #N  |            |  |
|  | |(5~11명)  |  |(5~11명)  |  |(5~11명)  |  |(5~11명)  |            |  |
|  | +----+-----+  +----+-----+  +----+-----+  +----+-----+            |  |
|  |      | Feature    | Feature    | Feature    | Feature             |  |
|  |      v            v            v            v                     |  |
|  |  +--------------------------------------------------+             |  |
|  |  |  ART: 50~125명, 5~12개 Agile Team                |             |  |
|  |  |  Events: PI Planning, ART Sync, Scrum of Scrums, |             |  |
|  |  |          System Demo, Inspect & Adapt            |             |  |
|  |  |  Roles: RTE, Product Management, SA, SM,         |             |  |
|  |  |         Business Owners, Release Train Engineer  |             |  |
|  |  +--------------------------------------------------+             |  |
|  +---------------------------+-------------------------------------------+
|                              | Story/Task
|                              v
|  +-------------------------------------------------------------------+
|  | Team Layer (실행 단위)                                              |
|  |  +-------------+  +-------------+  +-------------+               |
|  |  | Scrum Team  |  | Kanban Team |  | XP Team     |               |
|  |  | 1~4주 Sprint|  | Continuous  |  | Pair/TDD    |               |
|  |  | PO + SM     |  | Flow-based  |  | Engineering |               |
|  |  +-------------+  +-------------+  +-------------+               |
|  +-------------------------------------------------------------------+

  보조 구성: 7 Core Values / 21 Principles / 10 Implementation Steps
  가로축 보강: Lean-Agile Leadership | Team & Technical Agility |
              DevOps & Release on Demand | Business Solutions &
              Lean Portfolio Management | Organizational Agility
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Agile Release Train (ART)** | 50~125명, 5~12 Agile Team으로 구성된 장기(LTS, Long-Lived) 조직 단위. Value Stream 중심으로 구성되며 PI 단위로 솔루션 증분(System Increment) 출시. | Scrum-of-Scrums 구조, Shared Cadence(8~12주 PI + 2주 Iteration), DevOps Culture(SafePath to Production), 24h 내 System Demo 후 Fix |
| **PI Planning (Program Increment Planning)** | 분기 1회(8~12주) 2일간의 대면(또는 분산) 이벤트. 모든 팀이 동일 Business Context, Vision, Backlog 하에 Iteration별 Commitment(committed vs uncommitted) 도출. | 1일차: Business Context -> Tech Vision -> Team Breakouts -> Draft Plan, 2일차: Final Plan -> Risk/Dependency 식별 -> Confidence Vote (Fist-of-Five). 핵심 산출물: PI Objectives (각 팀 8~12개) |
| **Lean Portfolio Management (LPM)** | Portfolio Backlog, Epic Owner, Strategic Theme, Lean Budget Guardrails로 전략-실행 정렬 및 투자 거버넌스 수행. | 기능별 예산(Function-based Budget) -> Value Stream별 예산으로 전환, Epic Kanban 시스템(Epic -> Lean Business Case -> MVP -> Arch Runway) 적용, OKR + Weighted Shortest Job First(WSJF) 우선순위 |
| **Core Values (7개)** | Alignment, Built-in Quality, Transparency, Program Execution, Leadership, Customer, Relentless Improvement. | SAFe v5.0에서 Customer, Relentless Improvement 추가. 의사결정/리뷰/retro 시 체크리스트로 활용, "Inspect & Adapt" 워크숍의 기준 프레임 |
| **21 Lean-Agile Principles** | Lean Thinking, Systems Thinking, Flow 기반 실행, Innovation, Decentralization 등 4개 카테고리로 분류된 운영 원칙. | 예: #4 "Build incrementally with fast, integrated learning cycles", #14 "Remain open to new information" — Toyota Kata 기반 지속 개선 |
| **Lean-Agile Leader (LAL)** | Lean-Agile Transformation 촉진자. Servant Leadership 기반, 팀/ART/Portfolio 단위에서 Mindset 변화 주도. | SAFe LPM, SA, RTE, SPC 등 모든 역할의 공통 리더십 역량, "Go See" (Gemba), "Ask 5 Whys", "Lead by Example" 적용 |
| **Inspect & Adapt (I&A)** | PI 종료 시점 Workshop: (1) System Demo 측정 결과 (2) PI 측정 retrospective (3) Problem-Solving Workshop 3단계로 구성. | PI Metrics: Predictability (점속 계획 실행률), Velocity Trend, Quality (Defect Escape Rate, MTTR), Business Value Delivered |
| **Value Stream** | 고객 가치를 전달하는 End-to-End 활동 흐름(Development -> Ops -> Customer). SAFe 도입 시 Value Stream Identification가 1순위 과제. | Operational Value Stream(현행) vs Development Value Stream(개선 대상) 구분, VSM(Value Stream Mapping)으로 Lead Time, Process Time, %C&A 분석 |

**주요 정량 메트릭 및 알고리즘 핵심 원리**:
- **WSJF (Weighted Shortest Job First)**: 우선순위 = (Cost of Delay / Job Size). CoD는 User-Business Value + Time Criticality + Risk Reduction의 합. PI Planning의 Program Backlog 우선순위 결정에 사용.
- **Cadence vs 동기화**: Cadence(고정 박자, 예: 2주 Iteration)는 변동성 흡수, 동기화(여러 ART/팀의 동시 이벤트)는 의존성 통합을 위함. Ford Motor Company 사례에서 PI Planning을 통해 5개 ART 간 30% 의존성 사전 식별.
- **Architectural Runway**: Enabler Story/Epic으로 정의, 미래 Business Need를 지원하기에 충분한 아키텍처 기반(API, 플랫폼, 컴포넌트)을 사전 구축. 보통 1~2개 PI 분량 유지 권장.
- **Kanban WIP 제한**: ART Sync/Scrum of Scrums에서 클래스-A/B/C/C-Service Class 분기(Class A: 새 기능, B: 결함, C: 운영 변경, SVC: 서비스 요청), Explicit WIP 한계치 적용.

- **📢 섹션 요약 비유**: SAFe의 PI Planning은 **대도시의 4분기 통합 교통계획 회의**와 같습니다. 각 구(Agile Team)가 계획을 발표하지만, 지하철/버스 환승(의존성)이 맞물려야 시민(고객)이 한 번에 이동할 수 있으므로, 도시 교통국(RTE)이 전체 흐름을 조율합니다.

---

## Ⅲ. 비교 및 연결

SAFe는 단일 Agile 확장 프레임워크 중 가장 광범위하나, 모든 상황에 최적은 아니다. **LeSS(Large-Scale Scrum, Craig Larman & Bas Vodde)**, **Nexus(Scrum.org, Ken Schwaber)**, **Spotify Model**, **DAD(Disciplined Agile Delivery)**와의 비교를 통해 적합 의사결정 기준을 도출한다.

| 구분 | **SAFe** | **LeSS (Large-Scale Scrum)** | **Nexus (Scrum.org)** | **Spotify Model** |
| :--- | :--- | :--- | :--- | :--- |
| **확장 범위** | Portfolio~Team (4계층) | Team~Product (최대 8팀) | Team~Product (3~9팀) | Squad~Tribes (문화 중심) |
| **팀 수** | 50~125+명/ART | 2~8팀 (40~80명) | 3~9팀 (15~45명) | Squad 6~12명, Tribe 100+명 |
| **핵심 단위** | ART (Agile Release Train) | 1 Product, 1 Product Backlog | 1 Product Backlog, Nexus Team | Squad, Tribe, Chapter, Guild |
| **Planning Cadence** | PI Planning (8~12주, 2일) | Sprint Planning (1~4주, 팀별) | Nexus Sprint Planning (단일) | Quarter Planning + Squad별 |
| **역할 추가** | RTE, PM, SA, BO, EPC, SSM | 없음 (기존 Scrum 역할 유지) | Nexus Integration Team, PO, SM | Tribe Lead, Chapter Lead, Guild |
| **Artifacts 추가** | Feature, Epic, Capability, Enabler | 없음 (Product Backlog 단일
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 522 / 600

<- **이전**: [521. XP 익스트림 프로그래밍 실천법](/studynote/11_design_supervision/06_exam_summary/522_xp_extreme_programming_practice/)
**다음**: [523. LeSS 대규모 스크럼](/studynote/11_design_supervision/06_exam_summary/523_less_large_scale_scrum/) ->

---
