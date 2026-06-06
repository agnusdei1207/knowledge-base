---
title: "Nexus Multi Team Scrum Coordination"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Nexus는 단일 제품(Shared Product Backlog) 위에서 3~9개 Scrum Team을 동기화하기 위한 **경량 스케일링 프레임워크**로, 별도의 새로운 방법론이 아닌 Scrum의 이벤트/아티팩트에 **Nexus Integration Team(NIT)**과 **통합 이벤트(Nexus Sprint Planning·Review·Retrospective·Daily Scrum)**를 최소 침습적으로 추가한 구조다.
> 2. **가치**: 팀 간 통합(Integration) 실패로 발생하는 **재작업 비용을 Sprint 단위로 제거**하고, 모든 팀이 공유한 **Nexus Sprint Goal** 하에서 **"Done"된 통합 Increment**를 매 Sprint 종료 시 보장한다. 실증 사례(Jurgen Appelo, Mountain Goat Software 등)에서는 6개 팀 규모에서 통합 결함 70% 감소, Lead Time 40% 단축 효과가 보고된다.
> 3. **판단 포인트**: **단일 제품 vs 다중 제품**, **팀 수(3~9 권장)**, **도메인 결합도(Domain Coupling)**, **CI/CD 파이프라인 성숙도**가 채택 결정의 핵심이다. 10개 팀 초과·다중 제품·아키텍처 팀 분리가 필요하면 **LeSS Huge / SAFe / Scrum@Scale**로 이행해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 등장 배경 — "Scrum은 단일 팀을 위한 것"

단일 Scrum Team(3~9명) 모델은 1995년 Ken Schwaber & Jeff Sutherland의 OOPSLA 논문 이후, *하나의 Product Owner, 하나의 Product Backlog, 하나의 Increment*라는 가정 위에서 동작한다. 그러나 실제 엔터프라이즈 환경에서는 다음과 같은 한계가 발생한다.

| 한계 | 구체적 현상 | 임팩트 |
| :--- | :--- | :--- |
| **팀 간 의존성(Inter-team Dependency)** | 결제팀 ↟ 회원팀이 같은 `Order` 도메인 클래스를 동시 수정 | 코드 충돌, 머지 지옥, 통합 결함 |
| **백로그 분할 실패** | 한 Product Backlog Item(PBI)을 두 팀이 분할·수정 | 통합 시 인터페이스 불일치로 Hotfix 폭증 |
| **Done의 불일치** | 팀 A는 Unit Test까지, 팀 B는 E2E까지 Done으로 정의 | **Integrated Increment** 미보장 -> Sprint Review에서 "데모 불가" 사태 |
| **커뮤니케이션 비대화** | N개 팀이면 가능한 통신 경로 = N(N-1)/2 (5팀이면 10개) | 결정 지연, 결정권 모호(Who Decides What) |

Nexus는 2015년 Schwaber가 공표한 **최소 스케일링 프레임워크**로, Scrum.org에서 인증 프로그램(Nexus Guide 2020년 v3.0 갱신)도 운영된다. 키워드는 **"Less is More — Scrum을 가능한 한 그대로 유지하고, 통합에 필요한 최소한의 장치만 추가"** 이다.

### 1.2 시스템 컨셉 다이어그램

```text
+---------------------------------------------------------------+
|                  Single Product / Shared Vision               |
|                          v                                    |
|              +-------------------------+                      |
|              |  Product Backlog (단일) | <- 단일 PO 책임        |
|              +-------------------------+                      |
|                          |                                    |
|          Nexus Sprint Goal (모든 팀이 공유)                   |
|                          |                                    |
|   +--------------+-------+--------+--------------+            |
|   |              |                |              |            |
| +-v---+      +---v-+        +----v--+       +---v-+         |
| |Team1|      |Team2|        |Team3 |       |Team4 | (3~9)    |
| |SB #1|      |SB #2|        |SB #3 |       |SB #4 |         |
| +--+--+      +--+--+        +--+---+       +--+--+          |
|    |             |              |              |              |
|    +-------------+------+-------+--------------+              |
|                  +------v------+                              |
|                  |   CI/CD     | <- 매시간 자동 통합           |
|                  |  Pipeline   |                              |
|                  +------+------+                              |
|                  +------v------+                              |
|                  | Integrated  |  <- Scrum Definition of Done   |
|                  |  Increment  |     (모든 팀 공통 적용)      |
|                  +-------------+                              |
|                                                               |
|     +----------------------------------------------+          |
|     |    Nexus Integration Team (NIT, 5±2 명)      |          |
|     |  · Product Owner  · Scrum Master              |          |
|     |  · 팀별 Integration Member (3~9명)            |          |
|     |  -> 의존성/충돌 식별, 통합 정책 결정          |          |
|     +----------------------------------------------+          |
+---------------------------------------------------------------+
```

### 1.3 기존 단일 팀 Scrum 대비 변화 — 비교

| 항목 | 단일 Scrum Team | Nexus Multi-Team |
| :--- | :--- | :--- |
| 제품 수 | 1 | **1 (Single Product, Non-negotiable)** |
| 백로그 | 1 | 1 (단, N개의 Sprint Backlog) |
| Sprint 주기 | 자유 | **모든 팀 동기화(Sprint Start/End 동일)** |
| PO | 1 | 1 (단, PO가 NIT의 일원) |
| Scrum Master | 1 | N (각 팀 1명, 그 중 1명이 NIT Scrum Master) |
| 추가 역할 | 없음 | **Nexus Integration Team, Integration Member** |
| 추가 이벤트 | 없음 | **Nexus Sprint Planning(2단계), Nexus Sprint Review, Nexus Sprint Retrospective(2단계), Nexus Daily Scrum** |
| Definition of Done | 팀별 가능 | **반드시 팀 간 동일** (통합의 전제) |

- **📢 섹션 요약 비유**: 단일 Scrum Team이 한 손으로 요리하는 셰프라면, Nexus는 **"같은 주방(Shared Product Backlog)을 쓰는 셰프 5명이 같은 시간에 같은 코스(Nexus Sprint Goal)를 각자 맡아 요리하고, 마지막 5분 전 헤드셰프(NIT)가 디시 통일성을 검수"**하는 구조다. 주방을 두 개(다중 제품)로 쪼개야 한다면 Nexus가 아니라 LeSS Huge·SAFe를 써야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Nexus의 4대 메커니즘

Nexus는 Scrum의 3개 pillar(Transparency / Inspection / Adaptation)에 다음 4가지를 더한다.

1. **Nexus Integration Team (NIT)** — 조정 거버넌스
2. **Nexus Sprint Goal** — 모든 팀의 단일 동기
3. **Nexus 통합 이벤트 4종** — 동기화 및 통합 보장
4. **공유 Definition of Done + Shared Product Backlog** — 통합의 전제조건

### 2.2 Nexus Integration Team (NIT) 상세 구조

```text
                   +--------------------------+
                   |     Nexus Integration     |
                   |          Team             |
                   |  (권장 5±2명, 가이드 3~9) |
                   +--------------------------+
                              ^
        +---------------------+---------------------+
        |                     |                     |
 +------+------+       +------+------+       +------+------+
 | Product     |       | Nexus       |       | Integration |
 | Owner       |       | Scrum Master|       | Members(IM) |
 | (1명, 필수) |       | (1명, 필수) |       | (팀당 1명)  |
 +-------------+       +-------------+       +-------------+
                                                     ^
                              +----------------------+----------+
                              |                      |          |
                       IM_Team1                  IM_Team2   IM_TeamN
                       (개발자)                  (개발자)    (개발자)
                       -> 5~10% 시간만 NIT에 헌납(권장)
```

| 역할 | 책임 | 주요 의사결정 |
| :--- | :--- | :--- |
| **Product Owner** | 단일 Product Backlog 우선순위 결정, ROI最大化 | "어떤 PBI를 먼저 통합할 것인가", "MVP 범위 재정의" |
| **Nexus Scrum Master** | Nexus 프로세스 퍼실리테이션, 장애물 제거, Scrum Master 코호드 조율 | "팀 간 대기시간을 어떻게 줄일 것인가" |
| **Integration Member (IM)** | 각 팀에서 선임된 개발자, 통합 기술의사결정 실무 | "API 버전 정책", "Branch 전략", "DB 마이그레이션 순서" |
| **NIT 전체** | **의존성·충돌 식별**, 공유 DoD 정의, **자동화 도구** 채택 결정 | "Trunk-based vs GitFlow", "Feature Flag 정책" |

> **핵심 포인트**: NIT는 *명령통제(Command & Control) 조직이 아니다*. Scrum Guide는 "NIT는 통합에 관련된 의사결정만 한다"고 명시한다. 팀 자율(Self-organization)을 침해하면 안티패턴이 된다.

### 2.3 Nexus Sprint Events — 4단계 동기화 프로토콜

```text
  +------------------------------------------------------------+
  |  Nexus Sprint (모든 팀 동일 길이, 권장 2~4주)              |
  |                                                            |
  |  +------------------------------------------+              |
  |  | 1. Nexus Sprint Planning                 |              |
  |  |    Part 1: 각 팀 독립 PBI 선택·분해      |              |
  |  |            (단일 Product Backlog에서)     |              |
  |  |                    |                     |              |
  |  |                    v                     |              |
  |  |    Part 2: 모든 팀 합동 회의(NIT 주관)   |              |
  |  |            · 의존성 매트릭스 작성         |              |
  |  |            · 충돌 해결(누가 먼저/나중)   |              |
  |  |            · 통합 전략 합의               |              |
  |  |            · Nexus Sprint Goal 확정      |              |
  |  +------------------------------------------+              |
  |                    |                                       |
  |                    v                                       |
  |  +------------------------------------------+              |
  |  | 2. Sprint Execution (모든 팀 병렬)       |              |
  |  |    · 각 팀 Daily Scrum (15분)            |              |
  |  |    · Nexus Daily Scrum (15분, IM 참여)   |              |
  |  |      -> 의존성 이슈 보고·해결             |              |
  |  |    · 매시간 CI: 모든 PR 머지 & 빌드 검증 |              |
  |  +------------------------------------------+              |
  |                    |                                       |
  |                    v                                       |
  |  +------------------------------------------+              |
  |  | 3. Nexus Sprint Review (합동)            |              |
  |  |    · Integrated Increment 데모            |              |
  |  |    · 이해관계자 피드백 수집               |              |
  |  |    · Product Backlog 갱신                 |              |
  |  +------------------------------------------+              |
  |                    |                                       |
  |                    v                                       |
  |  +------------------------------------------+              |
  |  | 4. Nexus Sprint Retrospective            |              |
  |  |    Part 1: 각 팀 개별 Retrospective       |              |
  |  |                    |                     |              |
  |  |                    v                     |              |
  |  |    Part 2: Nexus Retrospective(NIT 주관) |              |
  |  |            · 통합 관련 장애물 식별        |              |
  |  |            · DoD·CI 개선 액션             |              |
  |  +------------------------------------------+              |
  +------------------------------------------------------------+
```

### 2.4 Nexus Daily Scrum (NDS) — 통합 관제탑

```text
  +--------------------------------------------------------+
  |          Nexus Daily Scrum (15분)                       |
  |          주관: NIT Scrum Master                         |
  +--------------------------------------------------------+
  |  Q1. 어제 Integrated Increment에 병합된 코드?           |
  |  Q2. 오늘 통합을 막을 의존성은?                          |
  |  Q3. 우리 팀 외 누가 막혀 있는가? (Ask for help)         |
  +--------------------------------------------------------+
                  ^        ^        ^
            IM_T1 보고  IM_T2 보고  IM_TN 보고
            (각 1~2분)  (각 1~2분)  (각 1~2분)
```

**핵심 제약**: NDS는 *팀 전체의 Daily Scrum을 대체하지 않는다*. 각 팀은 30분 전후로 자체 Daily Scrum을 끝내고, IM만 NDS에 합류한다.

### 2.5 Nexus Sprint Goal vs 통합된 Increment

| 개념 | 정의 | 검증 가능성 |
| :--- | :--- | :--- |
| **Nexus Sprint Goal** | NIT Sprint Planning Part 2에서 합의된 *한 문장* 목표 (예: "2024-Q4 결제 정합성 99.9% 도달") | 모든 팀의 Sprint Backlog가 이를 향해 정렬되어 있는가 |
| **Integrated Increment** | 모든 팀의 코드가 **공유 main/trunk 브랜치에 머지**되어 **공유 Definition of Done**을 통과한 실행 가능한 산출물 | 매 Sprint 말 미배포 가능한 상태인가 |

> **Nexus의 통합 공식**: `∫ (Sprint Backlog_i) dt  ->  Integrated Increment`
> i ∈ {1..N}, 모든 팀의 작업이 합산·통합되어야 한다.

### 2.6 아키텍처 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Product Owner (1명)** | 단일 백로그 소유, ROI 최적화 | SAFe의 *PMO*와 달리 *단일 인간*이어야 함(권고). 백로그 정제(Refinement
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 524 / 600

<- **이전**: [523. LeSS 대규모 스크럼](/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum)
**다음**: [525. 디자인 씽킹 공감 정의 아이디어](/studynote/11_design_supervision/06_exam_summary/525_design_thinking_empathize_define_ideate/) ->

---
