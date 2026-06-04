+++
title = "434. 소프트웨어 개발 방법론 워터폴 애자일 (Software Development Waterfall Agile)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 소프트웨어 개발 방법론은 **요구사항의 안정성(Stability)**, **변경 빈도(Volatility)**, **팀 규모(Span of Control)**에 따라 워터폴(예측형), 애자일(적응형), 하이브리드(반복-증분형) 중 최적의 거버넌스 모델을 선택하는 엔지니어링 의사결정 프레임워크이다.
> 2. **가치**: 워터폴은 **CMMI Level 5**, **ISO/IEC 12207** 기반의 명세 중심 계약으로 초기 비용 100% 사전 확정 및 **결함 탐지율 95% 이상**의 V&V 추적이 가능하며, 애자일(Scrum/Kanban/XP)은 **Lead Time 30~50% 단축**, **Time-to-Market 40% 개선**, **고객 만족도(CSAT) 20% 이상 향상**을 통해 비즈니스 가치 중심의 지속적 배포(Continuous Delivery)를 실현한다.
> 3. **판단 포인트**: 규제/안전 필수 도메인(항공·의료·금융 코어뱅킹)에서는 **DO-178C, IEC 62304, PCI-DSS** 등 인증 요건 충족을 위해 워터폴+V-Model을 유지하되, **SafeScrum**, **Regulated Agile**로 점진 전환하며, B2C/플랫폼 도메인에서는 **Spotify Squad 모델**, **SAFe 6.0**, **Dual-Track Agile**(Discovery+Delivery)로 전환하여 시장 반응 속도(Feedback Loop)를 압축한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 방법론은 1970년 **Winston W. Royce**의 *Managing the Development of Large Software Systems* 논문에서 제시된 **순차적(sequential) 모델**을 시초로, 이후 **Barry Boehm**의 나선형 모델(1986), **Jacobson**의 객체지향 라이프사이클(1992), **Kent Beck**의 Extreme Programming(1996), **Jeff Sutherland**의 Scrum(1995)을 거쳐, **Agile Manifesto(2001. 02)** 선언으로 본격적인 방법론 패러다임 전환이 일어났다. 특히 **DevOps**(2009), **Lean Startup**(2011), **SRE**(2016), **Platform Engineering**(2022~)의 등장으로 방법론의 경계는 **문화·자동화·측정·공유(CAMS)** 축으로 확장되었다.

기술사적 관점에서 방법론 선택은 단순한 프로세스 도입이 아니라 **계약 구조(FFP vs T&M)**, **거버넌스(거버넌스 보드/Change Control Board)**, **감리/인증 체계**, **아키텍처 결정 기록(ADR)** 수준을 좌우하는 **엔지니어링 전략 의사결정**이다. 예를 들어, 한국 정보시스템 감리는 **감리원**: 5단계(설계->구현->시험->초과운영), **발주자-PM-감리원** 3자 관계, **단계별 산출물 287종**의 검수를 요구하므로 순수 Scrum 적용이 아닌 **Agile@Scale + 감리 체크포인트 융합 모델**이 필요하다.

```text
[소프트웨어 개발 방법론 진화 타임라인]

1968 NATO SW Crisis  ->  1970 Royce Waterfall  ->  1986 Boehm Spiral
        |                     |                      |
        v                     v                      v
   +---------+         +------------+         +--------------+
   |  구조화  |         | 단계게이트  |         |  위험驱动     |
   |  프로그래밍|        |  (Stage-Gate)|        |  프로토타이핑  |
   |  Jackson|          | V-Model     |         |  Win-Win    |
   +----+----+         +------+-----+         +------+-------+
        |                      |                       |
        +----------+-----------+-----------------------+
                   v
        +----------------------+
        | 1996  CMM/CMMI      | <-  5단계 성숙도 모델 (Initial->Optimizing)
        | 2001  Agile Manifesto| <-  4가치, 12원칙 선언
        | 2010  DevOps         | <-  CAMS (Culture, Automation, Measure, Sharing)
        | 2016  SRE            | <-  SLO/Error Budget
        | 2021  SAFe 6.0       | <-  7 Core Values, 4 Configurations
        | 2023  Platform Eng.  | <-  IDP(Internal Developer Platform)
        +----------------------+
                   |
                   v
        [미래 방향: AI-Native SDLC]
        LLM 기반 요구사항 분석 -> 코드 생성 -> 자동 테스트
        + 인간-AI 협업 거버넌스 (Human-in-the-Loop)
```

- **구 방법론(워터폴)의 한계**: 요구사항 동결(Freeze)로 시장 변화 대응 불가, **Brook's Law**("인력을 늦게 추가하면 일정이 더 늦어진다"), **Integration Hell**(말단 통합 시 결함 폭증), **Plan-Driven Trap**(초기 잘못된 가정이 전 단계 전파).
- **신 방법론(애자일)의 등장 배경**: **CHAOS Report**(Standish Group)에 따르면 전통 방법론 프로젝트 성공률은 1994년 **16%** -> 2020년 **31.6%**로 정체, Agile 프로젝트는 **42.6%** 성공률, 기능/시간/예산 트레이드오프에서 압도적 우위.
- **📢 섹션 요약 비유**: 워터폴은 **"건물 청사진을 한 번 확정하고 지은 후에는 외벽 색깔도 못 바꾸는 건축"**이고, 애자일은 **"골격은 짓되, 입주자 피드백을 받아 1층부터 인테리어를 계속 바꿔가는 리노베이션"**이다. 핵심은 "어떤 건물이냐"가 아니라 "어떤 사용 패턴을 수용해야 하느냐"다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. 워터폴 모델(Waterfall) — 예측형(Plan-Driven) 거버넌스

Royce의 원래 정의는 **피드백 루프가 없는 선형 모델**이었으나, 실무에서는 **V-Model**(Verification & Validation, 1980년대 독일 연방군 표준 **V-Modell XT**에서 정형화)로 진화하여 각 개발 단계에 대응하는 시험 단계를 우측에 매핑한다.

```text
[Waterfall + V-Model 구조: 요구사항 -> 인수시험의 양방향 추적성]

  +------------------+                          +------------------+
  | 사용자 요구사항   |  ---- (Validation) -----> | 인수시험 (AT)     |
  | (User Req.)      |                          | User Acceptance   |
  +--------+---------+                          +--------^---------+
           |                                            |
           v (Allocation)                              | (Trace)
  +------------------+                          +------+-----------+
  | 시스템 요구사항   |  ---- (Validation) -----> | 시스템 시험 (ST)  |
  | (System Req.)    |                          | Integration Test  |
  +--------+---------+                          +--------^---------+
           |                                            |
           v (Allocation)                              | (Trace)
  +------------------+                          +------+-----------+
  | SW 요구사항      |  ---- (Verification) ---> | 통합시험 (IT)     |
  | (SW Req./SRS)    |                          | Component Int.    |
  +--------+---------+                          +--------^---------+
           |                                            |
           v (Refinement)                              | (Trace)
  +------------------+                          +------+-----------+
  | 상세설계 (SDD)    |  ---- (Verification) ---> | 단위시험 (UT)     |
  | HLD/LLD          |                          | Unit Test         |
  +--------+---------+                          +--------^---------+
           |                                            |
           v                                          |
  +------------------+                                  |
  | 구현 (Coding)    |  ---- (Static) --------> (Code Review, 정적분석)
  +------------------+                                  |
                                                          |
   <--- 좌측: 개발(Development)  |  우측: 시험(Test) ---> |
   <----------- 추적성 매트릭스(RTM)로 양방향 연결 -----------> |
```

### B. 애자일 모델(Agile) — 적응형(Adaptive) 거버넌스

**Scrum**은 **3-5-3 구조**(3 역할, 5 이벤트, 3 산출물)를 가지며, **Sprint**(보통 2주, 1~4주 범위) 단위로 **Inspect & Adapt** 사이클을 반복한다.

```text
[스크럼(Scrum) 프레임워크 상세 구조]

        +----------------------------------------------+
        |  Product Owner (PO)                          |
        |  • Product Backlog 우선순위 결정             |
        |  • 사용자 스토리(User Story) 작성             |
        |    As a [persona], I want [feature],          |
        |    so that [business value]                   |
        |  • 수용 기준(Acceptance Criteria): Gherkin    |
        +--------------------+-------------------------+
                             | Backlog Refinement
                             v
        +----------------------------------------------+
        |  Scrum Master (SM) — Servant-Leader          |
        |  • impediment 제거, team velocity 보호        |
        |  • 스크럼 이벤트 facilitation                 |
        +--------------------+-------------------------+
                             |
                             v
        +----------------------------------------------+
        |  Developers (3~9명)                          |
        |  • Sprint Planning -> Daily Scrum -> Review    |
        |  • Definition of Done (DoD) 기준 충족        |
        |  • Self-organization, Cross-functional       |
        +--------------------+-------------------------+
                             |
                             v  <--- Inspect & Adapt
        +----------------------------------------------+
        |  Scrum Events (5)                            |
        |  1. Sprint (≤1개월, 일관)                    |
        |  2. Sprint Planning (≤8h)                    |
        |  3. Daily Scrum (15분, 3질문)                |
        |  4. Sprint Review (≤4h, 인크리먼트 시연)     |
        |  5. Sprint Retrospective (≤3h, 개선 액션)    |
        +----------------------------------------------+
                             |
                             v
        +----------------------------------------------+
        |  Scrum Artifacts (3) + Commitment            |
        |  • Product Backlog    -- Product Goal         |
        |  • Sprint Backlog     -- Sprint Goal          |
        |  • Increment (DoD)    -- Definition of Done  |
        +----------------------------------------------+
```

### C. 핵심 구성 요소 비교표

| 구성 요소 | 워터폴 (Plan-Driven) | 애자일 - 스크럼 (Agile Scrum) | 애자일 - 칸반 (Kanban) | 애자일 - XP (Extreme Programming) |
| :--- | :--- | :--- | :--- | :--- |
| **수명주기 모델** | 순차적 (Sequential), 단계게이트 | 반복-증분 (Iterative-Incremental) | 흐름 기반 (Flow-based, Pull) | 반복-증분 (1~2주 iteration) |
| **계획 주기** | 1회 마스터 플랜 (Baseline) | 매 Sprint Planning (2~4주) | Rolling Wave (수시 우선순위 변경) | 매 Iteration Planning |
| **요구사항 관리** | SRS(SW Requirement Spec) 동결, 변경통제위원회(CCB) 승인 필요 | Product Backlog 동적 재우선순위화 (PO 권한) | WIP Limit 시각화로 흐름 제어 | 사용자 스토리 + 온사이트 고객 (On-site Customer) |
| **설계 단계** | Big Design Up Front (BDUF), 아키텍처 결정 후 변경비용 ^ | **YAGNI**, **Last Responsible Moment**, 점진적 설계 (Just Enough) | 변경 가능 구조, 작업 가시화 | **TDD/FDD**, **Refactoring**, **Simple Design** |
| **코드 품질 보증** | 단계말 통합시험, 정적분석(SonarQube, Coverity) | DoD(Definition of Done), Pair Programming, CI | 코드 리뷰, 자동화 파이프라인 | **Pair Programming**, **TDD**(Red-Green-Refactor), **CI/CD** |
| **측정 지표 (KPI)** | CPI/SPI (Cost/Schedule Performance Index), EAC/ETC | Velocity (Story Point/Sprint), Burndown/Burnup Chart | **Lead Time**, **Cycle Time**, **Throughput**, CFD(Cumulative Flow Diagram) | Velocity, 결함 누출률(Defect Leakage), 코드 커버리지 ≥ 80% |
| **거버넌스/계약** | **FFP**(Firm Fixed Price), 단계별 검수, 한국 SW 감리 5단계 | Time & Material, Product Increment 인수 | Pull-based 작업 흐름, 명시적 WIP Limit | 짧은 release cycle (2주), iteration별 인수 |
| **변경 대응** | 변경 요청서(CR) -> 영향 분석 -> CCB 승인 (Cycle: 주~월) | Sprint 내 변경 제한, Backlog Grooming 시 재조정 | WIP Limit 내 즉시 반영 | **Planning Game**, **Slack** 시간(20%)으로 신규 작업 흡수 |
| **팀 구조** | 기능별 분화 (분석가, 설계자, 개발자, 시험자 분리) | Cross-functional Self-organizing Team (3~9명) | 기존 팀 + Kanban 보드 시각화 (예: Jira, LeanKit) | Pair Programming, Collective Code Ownership |
| **산출물 (Artifacts)** | SRS, SDD, STD, SP, OP, OMM (정보시스템 감리 기준 287종) | Product Backlog, Sprint Backlog, Increment (Potentially Shippable) | Kanban Board (To Do/Doing/Done), CFD | User Story, Unit Test, Refactoring 기록 |
| **도구/표준 연계** | **CMMI-DEV v2.0**, **ISO/IEC 12207:2017**, **IEEE 830** | **Scrum Guide (2020)**, **Nexus**(5~9팀), **SAFe 6.0**(ART) | **Kanban Guide (2021)**, **STATIK** | **XP Explained 2nd Ed.(Beck, 2004)** |

### D. 핵심 파라미터 및 알고리즘

1. **버그다운 차트(Burndown Chart) 수식**
   - **이상적 잔여 작업량(Ideal Remaining Work)**: `W_ideal(t) = W_total × (1 − t/S)` (S: 총 Sprint 일수, t: 경과 일수)
   - **실제 잔여 작업량(W_actual)**: 매 Daily Scrum 업데이트
   - **Velocity**: `V = Σ(완료된 Story Point) / N_sprints` (이동 평균, 최근 3 Sprint 권장)

2. **CFD(Cumulative Flow Diagram) 분석**
   - **Lead Time** = Done 진입 시각 − Backlog 진입 시각 (고객 체감 시간)
   - **Cycle Time** = In-Progress 진입 시각 − Done 진입 시각 (작업 처리 시간)
   - **WIP(Work In Process)**: Little's Law `L = λ × W` (L: 평균 WIP, λ: 처리율, W: Cycle Time)

3. **SAFe 6.0의 Program Increment(PI) Planning**
   - **ART(Agile Release Train)** 단위: 보통 50~125명, 8~12개 Agile Team
   - **PI 길이**: 8~12주 (4 Iteration + 1 Innovation & Planning Iteration)
   - **PI Objectives**: 각 팀의 비즈니스/엔터프라이즈 목표 SMART 기반 수립

4. **EVM(Earned Value Management) — 워터폴/하이브리드**
   - **CPI** = EV / AC (Cost Performance Index, ≥ 0.9 양호)
   - **SPI** = EV / PV (Schedule Performance Index, ≥ 0.95 양호)
   - **TCPI** = (BAC − EV) / (BAC − AC) (완료 비용
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 434 / 800

<- **이전**: [433. 프로그램 관리 포트폴리오 최적화](/knowledge-base/studynote/12_it_management/05_security_compliance/433_program_management_portfolio_optimization/)
**다음**: [435. 요구사항 관리 추적 변경 제어](/knowledge-base/studynote/12_it_management/05_security_compliance/435_requirements_management_traceability/) ->

---
