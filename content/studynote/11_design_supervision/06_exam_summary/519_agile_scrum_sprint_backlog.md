---
title: "519. 애자일 스크럼 스프린트 백로그 (Agile Scrum Sprint Backlog)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스프린트 백로그(Sprint Backlog)는 **Product Backlog에서 해당 스프린트에 커밋된 PBI(Product Backlog Item) + 이를 구현하기 위한 기술적 작업(Task) + 단일의 Sprint Goal + 실시간 진척도(스프린트 번다운 차트)**로 구성되며, **Scrum Team 내 Developers(개발팀)가 단독으로 소유(owned)**하는 1~4주 한정의 실행 단위 백로그이다.
> 2. **가치**: 스프린트 계획 회의(Sprint Planning)의 산출물로서 "**약속(Promise) -> 실행(Execution) -> 검증(Verification)**"의 추적성을 제공하며, 이를 통해 Scrum의 핵심 메트릭인 **Sprint Predictability(속도 안정성, 통상 ±10% 이내 변동)**, **Sprint Goal 달성률**, **Daily Progress Visibility**를 정량화하여 Empirical Process Control의 3대 Pillar(Transparency/Inspection/Adaptation)를 실현한다.
> 3. **판단 포인트**: **Sprint Goal의 단일성(Single Sprint Goal 원칙) vs Product Backlog Refinement의 항시성**, **Task 분해의 세분화 수준(보통 4~16시간 단위)**, **Definition of Done(DoD)의 팀별 표준화**, **Scrum Master의 강제 해체(Sprint Cancellation) 권한 사용 기준**이 핵심 판단 포인트이며, 잘못 운영될 경우 "**Fake Sprint Backlog(스프린트 목표 없는 작업 목록)**" 또는 "**Sprint Backlog Anti-pattern(전 스프린트 백로그를 다음 스프린트로 단순 이관)**"이 발생한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 패러다임이 폭포수(Waterfall) 모델에서 **반복적(Iterative)·점증적(Incremental) 개발**으로 전환됨에 따라, **V-Model**, **Rational Unified Process(RUP)** 등의 계획 중심(Plan-driven) 방법론은 **요구사항 변경 대응(Time-to-Market)**, **고객 가치 조기 제공(Early ROI)**, **리스크 조기 발견(Early Defect Detection)** 측면에서 한계를 드러냈다. 1995년 Jeff Sutherland와 Ken Schwaber가 Sutherland의 Easel Corporation 프로젝트에서 처음 도입한 **Scrum 프레임워크**는 Rugby의 "Scrum"에서 차용한 용어처럼, 팀이 한곳에 모여 **공(공)을 가지고 함께 전진하는 형태**로 일정한 리듬(1~4주 스프린트)을 가지고 점증적 가치를 전달하는 경량(lightweight) 프레임워크다.

**스프린트 백로그**는 Scrum Framework의 **3가지 Artifacts(제품 백로그, 스프린트 백로그, 인크리먼트)** 중 두 번째에 해당하며, **2020년 Scrum Guide 2.0 개정**을 통해 그 의미가 더욱 정교해졌다. 기존에는 "개발팀이 스프린트 동안 수행하기로 한 작업 항목"이라는 단순 정의였으나, 현재는 **"Sprint Goal, Developers가 선택한 Product Backlog 항목들, 이를 Product Increment로 전환하기 위한 작업 계획, 그리고 Sprint Burndown Chart로 구성된, 실시간으로 가시화되는 작업의 그림"**으로 정의된다. 이는 단순한 To-Do 리스트가 아니라 **"목표-작업-진척"이 통합된 living document**임을 강조한다.

기존 프로젝트 관리에서는 WBS(Work Breakdown Structure)와 Gantt Chart를 통해 **Push 방식**으로 작업이 할당되었으나, **스프린트 백로그는 Self-Organization**을 통해 **Pull 방식**으로 작업이 진행된다. 즉, **Product Owner**가 "**무엇을(What)**"을 정렬하면, **Developers**는 "**어떻게(How)**"와 "**누가(Who)**"를 자율적으로 결정한다. 이러한 책임 분리는 Conway's Law와 복잡계 이론(Complex Adaptive Systems)에 기반하며, **"팀이 목표를 이해하면 가장 효율적인 경로를 스스로 발견한다"**는 Empiricism의 핵심 철학이 반영되어 있다.

```text
+--------------------------------------------------------------------+
|              Scrum Framework 에서의 스프린트 백로그 위치              |
+--------------------------------------------------------------------+

            +--------------------------------------+
            |  Product Backlog (우선순위 정렬된 요구사항)  |
            |  - Epic -> Feature -> User Story -> Task  |
            |  - Product Owner가 단독 소유 (Single Owner) |
            |  - DEEP 원칙: Detailed/Emergent/Estimated/Prioritized |
            +-------------+------------------------+
                          | (Sprint Planning 시)
                          | PBIs의 일부(7~12개) + Sprint Goal 결정
                          v
            +--------------------------------------+
            |    🎯 Sprint Backlog (개발팀 단독 소유)     |
            |  +----------------------------------+  |
            |  | 1. Sprint Goal (단일, 단수형)        |  |
            |  |    "결제 시스템 PG사 다중화 및 SLA 보장"   |  |
            |  +----------------------------------+  |
            |  +----------------------------------+  |
            |  | 2. Selected PBIs (4~12개)         |  |
            |  |    - PBI-101: 카드 결제 모듈 리팩토링    |  |
            |  |    - PBI-102: Toss/KakaoPay PG 어댑터   |  |
            |  |    - PBI-103: 결제 SLA 모니터링 대시보드   |  |
            |  |    - PBI-104: 결제 실패 Retry 로직 강화   |  |
            |  +----------------------------------+  |
            |  +----------------------------------+  |
            |  | 3. Tasks (각 PBI당 3~7개)          |  |
            |  |    [PBI-101]                      |  |
            |  |     □ PaymentService.java 인터페이스 추출  |  |
            |  |     □ Legacy 코드에 Adapter 패턴 적용     |  |
            |  |     □ JUnit5 + Mockito 테스트 작성     |  |
            |  |     □ SonarQube Quality Gate 통과     |  |
            |  +----------------------------------+  |
            |  +----------------------------------+  |
            |  | 4. Sprint Burndown Chart (실시간)   |  |
            |  |    Ideal -----╲                    |  |
            |  |    Actual    ---╲____              |  |
            |  +----------------------------------+  |
            +--------------------------------------+
                          | (Sprint Review 시)
                          v
            +--------------------------------------+
            |  Increment (잠재적으로 출하 가능한 Done)  |
            |  - DoD 충족 + 모든 CI/CD 파이프라인 통과   |
            |  - "Done"의 객관적 검증 (수동 X, 자동화)     |
            +--------------------------------------+
```

**📢 섹션 요약 비유**: 스프린트 백로그는 마치 **한 끼 식사의 코스요리(Full-course Meal)**와 같다. **Product Backlog은 냉장고의 모든 식재료**(돼지고기, 채소, 양념 등), **Sprint Goal은 "오늘은 양식 정식"이라는 단일한 요리 컨셉**, **Sprint Backlog는 그 요리에 필요한 구체적인 메뉴(에피타이저, 메인, 디저트)와 레시피, 조리 진척도**다. 냉장고에서 모든 재료를 꺼내 요리하는 것이 아니라, **컨셉에 맞는 재료만 콕 집어**(Sprint Goal 정렬) **요리사가 스스로 불 조절과 플레이팅까지 결정**하는 것이다(Self-Organization).

---

## Ⅱ. 아키텍처 및 핵심 원리

스프린트 백로그는 단순한 문서가 아니라 **Scrum Team의 5가지 Events(Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective)**와 **5가지 Accountabilities(Product Owner, Scrum Master, Developers)**가 교차하는 **데이터 허브(Hub)**이다. 기술적으로는 다음의 **3-Tier 정보 모델**을 따른다.

### 📐 스프린트 백로그의 3-Tier 정보 모델

```text
+----------------------------------------------------------------------+
| Tier 1: STRATEGIC LAYER (전략 계층)                                  |
|  +----------------------------------------------------------------+ |
|  |  Sprint Goal (단일, 측정 가능, 비즈니스 가치)                    | |
|  |  - Example: "신규 결제 시스템의 첫 10,000건 트랜잭션에서         | |
|  |             99.9% SLA(응답시간 < 200ms) 달성"                  | |
|  |  - SMART 원칙: Specific, Measurable, Achievable, Relevant,     | |
|  |    Time-boxed                                                   | |
|  +----------------------------------------------------------------+ |
|                              v (분해 / Decomposition)                |
| Tier 2: TACTICAL LAYER (전술 계층)                                   |
|  +----------------------------------------------------------------+ |
|  |  Selected PBIs (4~12개, 보통 1~3일 단위로 완료 가능)             | |
|  |  - 각 PBI는 Acceptance Criteria 2~5개 포함                     | |
|  |  - INVEST 원칙 준수: Independent, Negotiable, Valuable,        | |
|  |    Estimable, Small, Testable                                   | |
|  |  - Story Point (Fibonacci: 1, 2, 3, 5, 8, 13, 21)             | |
|  +----------------------------------------------------------------+ |
|                              v (세분화 / Granularization)             |
| Tier 3: OPERATIONAL LAYER (운영 계층)                                |
|  +----------------------------------------------------------------+ |
|  |  Tasks (각 PBI당 평균 4~10개, 통상 4~16시간 단위)               | |
|  |  - Daily Scrum에서 "어제 한 일 / 오늘 할 일 / 장애물" 보고 단위   | |
|  |  - To Do / In Progress / Done 상태 머신                         | |
|  |  - WIP Limit (옵션, Kanban-style 적용 시)                       | |
|  +----------------------------------------------------------------+ |
+----------------------------------------------------------------------+
                              v (실시간 측정)
                +----------------------------------+
                |  Sprint Burndown/Burnup Chart     |
                |  - X축: Sprint Day (Day 1 ~ 10)    |
                |  - Y축: 남은 Story Point 또는 Task 수|
                |  - Ideal Line: 시작SP / Working Days |
                |  - 실제: 매일 업데이트, DevOps 도구 연동|
                +----------------------------------+
```

### 📊 Daily Scrum을 통한 스프린트 백로그의 동적 갱신 흐름

```text
     +-------------+     Daily Scrum (15분, 24h 주기)     +--------------+
     |   Today     | <---------------------------------> |  Task Status |
     |   Plan      |                                     |  Update      |
     +------+------+                                     +------+-------+
            | Pull (자가 할당)                                    | Push (실시간)
            v                                                     v
     +----------------------------------------------------------------+
     |              Sprint Backlog (3-Tier 정보 모델)                 |
     |  +----------+  +----------+  +----------+  +----------+      |
     |  | To Do    |-> | In Prog  |-> | Review   |-> | Done ✅  |      |
     |  | (3 tasks)|  | (4 tasks)|  | (2 tasks)|  |(1 task)  |      |
     |  +----------+  +----------+  +----------+  +----------+      |
     |       ^             |              |            |              |
     |       |             v              v            v              |
     |       |       CI/CD 자동화      PR Review     DoD 검증        |
     |       |       (Jenkins/GH Actions)(4-eyes) (SonarQube)        |
     |       |                                                        |
     |       +------- 새 Task 추가 (Sprint Backlog Emergent) ---------|
     +----------------------------------------------------------------+
                              | (방사형 전파)
                              v
            +------------------------------------------+
            |  Velocity Calculation (Sprint 종료 시)     |
            |  V = Σ(Completed Story Points)            |
            |  예: 35 SP (전 스프린트 평균 32.5 SP)       |
            |  -> Predictability = 35/32.5 = 107.7%      |
            +------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Sprint Goal** | 스프린트의 단일 목적, 모든 작업의 North Star | Scrum Team 전체가 합의한 1개의 문장(Sentence). Sprint Backlog 내 PBI들은 이 목표와 정렬되어야 하며, 목표 달성이 어려울 경우 PB를 동결하고 Goal 변경 또는 Sprint Cancellation 검토 |
| **Selected PBIs** | 스프린트 동안 완성할 약속된 제품 기능 단위 | Product Backlog의 상위 항목 중 Sprint Planning에서 선정. Acceptance Criteria, Story Point 추정치(Planning Poker로 산정), 우선순위(Product Owner의 ROI 기준 정렬) 포함 |
| **Tasks** | PBI를 실제 코드로 구현하기 위한 개발자 단위 작업 | T-Shirt Size(1일, 반나절, 4시간 등) 또는 시간(h) 기반 추정. Daily Scrum의 보고 단위. PR(Pull Request) 1개 = Task 1~2개의 매핑이 일반적 |
| **Sprint Burndown Chart** | 스프린트 진척도의 실시간 가시화 | X축: Sprint Day(예: Day 1~10), Y축: 남은 Story Point. Ideal Line은 `(Start_SP / Working_Days) × Day`로 계산. Jira, Azure DevOps, GitHub Projects에서 자동 생성 |
| **Sprint Backlog Board** | 물리적/디지털 칸반 보드 | To Do / In Progress / Review / Done의 4~6개 컬럼. WIP Limit 적용으로 멀티태스킹 억제. Swimlane으로 PBI별 그룹화 가능 |
| **DoD (Definition of Done)** | 작업 항목의 "완료" 기준의 객관화 | 코드 리뷰, 단위 테스트(80% 이상 커버리지), 통합 테스트, SonarQube Quality Gate, 보안 스캔, 문서화, 성능 테스트, 스테이징 배포 등 5~15개 체크리스트 |
| **Impediments List** | 작업 진행을 방해하는 장애물 목록 | Scrum Master가 관리. 예: "운영 DB 접근 권한 미부여", "외부 API 응답 지연", "테스트 환경 다운타임". Daily Scrum에서 보고됨 |

### 🔍 핵심 메커니즘: Definition of Done (DoD) vs Acceptance Criteria

기술사 시험에서 자주 혼동되는 두 개념을 명확히 구분해야 한다.

- **Acceptance Criteria (수락 기준)**: PBI(Story) 단위로 존재. **"PBI-101: 카드 결제 모듈 리팩토링"**이 완료되었다고 판단하는 **기능적 조건** (예: "Visa/Master/JCB 카드 결제 성공률 99.9% 이상", "잔액 부족 시 명확한 에러 메시지 반환"). 보통 Given-When-Then(Gherkin) 형식으로 작성.
- **Definition of Done (완료의 정의)**: **팀 전체가 합의한 품질 기준**. 모든 PBI에 공통 적용되는 **비기능적/공정적 조건** (예
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 519 / 600

<- **이전**: [518. 프린스2 프로젝트 관리 방법론](/studynote/11_design_supervision/06_exam_summary/519_prince2_project_management_methodology/)
**다음**: [520. 칸반 WIP 제한 흐름 최적화](/studynote/11_design_supervision/06_exam_summary/520_kanban_wip_limit_flow_optimization/) ->

---
