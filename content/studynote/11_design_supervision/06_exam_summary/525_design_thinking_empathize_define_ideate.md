---
title: "525. 디자인 씽킹 공감 정의 아이디어 (Design Thinking Empathize Define Ideate)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디자인 씽킹의 공감(Empathize)·정의(Define)·아이디어(Ideate)는 "사용자-문제-솔루션"의 3축을 분리해 다루는 **이탬릭(Iterative) 문제 프레이밍 프레임워크**이며, 공감맵(Empathy Map)·POV(Point of View)·HMW(How Might We)·브레인라이팅(Brainwriting) 등 정형화된 산출물을 통해 비구조적(Unstructured) 요구사항을 구조화한다.
> 2. **가치**: 초기 잘못된 문제정의로 인한 재작업 비용을 **30~70% 절감**(Standish Group CHAOS Report 기준)하며, 사용자 니즈 기반 MVP의 시장 적중률을 **2~5배** 향상시키고, 후속 UX/UI·Agile 스프린트·Lean 실험과의 핸드오프를 위한 **공통 언어와 산출물(페르소나·저니맵·Kano 우선순위)**을 제공한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (a) 공감의 **정성 데이터 수집 깊이 vs 시간·비용**, (b) 정의 단계의 **문제 범위(Scope) 축소 vs 본질 회피**, (c) 아이디어 단계의 **양(Quantity) 확장 vs 점수화(Score) 조기수렴(Early Convergence)**이며, 기술사적 판단 기준은 "사용자 페인포인트의 객관적 검증 여부"와 "솔루션 구현 시 DX(Developer Experience)·보안·확장성 제약 반영"이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)·AI 서비스·초연결 플랫폼 시대의 소프트웨어 프로젝트는 **불확실성 하의 비구조적 문제(Unstructured Problem)**가 60% 이상을 차지한다(PMI 2018, Pulse of the Profession). 전통적 Waterfall 모델은 "요구사항 정의 -> 설계 -> 구현"의 순차 구조로, 사용자 컨텍스트가 왜곡된 채 솔루션이 결정되는 **Solution-First Anti-pattern**을 유발한다. 디자인 씽킹(Design Thinking)은 Stanford d.school·IDEO·IBM 등에서 2008~2015년 사이 체계화된 **Human-Centered Design(HCD)** 방법론으로, 특히 **공감(Empathize)-> 정의(Define)-> 아이디어(Ideate)** 3단계는 문제공간(Problem Space)을 솔루션공간(Solution Space)으로 전환하는 **가치 발견(Value Discovery) 단계**로서, Agile·Lean Startup·DevOps·SRE와 같은 후속 방법론과 결합될 때 시너지를 극대화한다.

```text
+-------------------- 디자인 씽킹 5단계 + α (d.school / Double Diamond) --------------------+
|                                                                                          |
|  ◆ Problem Space (왼쪽 다이아몬드)               ◆ Solution Space (오른쪽 다이아몬드)    |
|                                                                                          |
|   +---------+     +---------+     +---------+      +--------------+    +----------+    |
|   |Empathize|----->| Define  |----->|  Ideate |------>|  Prototype   |---->|   Test   |--+ |
|   | 공감     |     | 정의    |     | 아이디어 |      |  프로토타입  |    |   테스트 |  | |
|   |(탐색)   |     |(수렴)   |     | (확산)  |      |  (구축)      |    |(검증)   |  | |
|   +---------+     +---------+     +---------+      +--------------+    +----------+  | |
|        ^                                                                    |         | |
|        |              [Agile Sprint] [Lean MVP] [A/B Test] [UX Research]      |         | |
|        |                                                                    |         | |
|        +---------------------- 피드백 루프(Feedback Loop) <---------------------+         | |
|                                                                                          |
|  * 핵심 산출물: Empathy Map, Persona, User Journey Map, POV Statement, HMW Questions,    |
|                Idea Cluster(SCAMPER, Brainwriting, 6-3-5), Concept Selection Matrix     |
+------------------------------------------------------------------------------------------+
```

**왜 필요한가?**
- **기존 패러다임의 한계**: ① Waterfall은 요구사항 동결 시점 이후 변경비용이 50~200배 증가(Barry Boehm, 1981), ② Feature-First 방식은 사용자가 원하지 않는 기능을 64% 포함(Build-Then-Sell), ③ 마케팅·개발·운영 간 **사일로(Silo)**로 사용자 진실(Ground Truth)이 손실.
- **새 패러다임의 강점**: ① 비지정형 문제의 **발산(Diverge)->수렴(Converge)->발산->수렴** 이중 다이아몬드(Double Diamond) 구조, ② 공감 단계의 정성 데이터로 **잠재 니즈(Latent Need)** 발굴, ③ 정형화된 산출물(아티팩트)로 **팀·이해관계자 간 공유심모델(Shared Mental Model)** 형성.
- **연계 가능성**: 정의된 POV/HMW는 **Epic -> User Story -> Acceptance Criteria**로 변환되어 Scrum 백로그에 직접 적재 가능하며, 아이디어 산출물은 **Lean Canvas -> MVP**로 이어진다.

- **📢 섹션 요약 비유**: 공감-정의-아이디어는 마치 **의사가 환자의 증상(공감)-> 진단명(정의)-> 치료 옵션(아이디어)**을 도출하는 임상 프로세스와 같다. 잘못된 진단은 좋은 약(솔루션)보다 위험하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 단계별 핵심 메커니즘

```text
+----------------- Empathize -----------------+   +----------------- Define -----------------+
|                                              |   |                                            |
|  ① 리서치 계획(Research Plan)                |   |  ① 정성 데이터 클러스터링                 |
|      + 사용자군(User Group) 정의             |   |      + Affinity Diagram(KJ법)             |
|      + 리서치 목표·윤리 동의서 작성           |   |      + 테마(Theme) -> 인사이트(Insight)     |
|  ② 데이터 수집(Qualitative Data Collection)  |   |  ② 페르소나(Persona) 도출                 |
|      + 1:1 심층 인터뷰(20~45분×5~8명)        | -->|      + 데모그래픽 + 행동 + 목표 + 페인    |
|      + 현장 관찰(Field Observation/Shadowing)|   |      + 시나리오 매핑                      |
|      + 사용자 저널(Diary Study)              |   |  ③ 사용자 저니맵(Journey Map)             |
|      + 공감 워크숍(Appreciative Inquiry)     |   |      + 단계별 Touchpoint + 감정 곡선       |
|  ③ 원시 데이터(Raw Data) -> 패턴화            |   |  ④ POV(Point of View) 문장 작성            |
|      + 4-Quadrant Empathy Map               |   |      [사용자]는 [니즈]를 원하지만 [장애물] |
|        (Says / Thinks / Does / Feels)       |   |        때문에 [불만족]을 겪는다             |
|                                              |   |  ⑤ HMW(How Might We) 질문 변환            |
|  * 산출물: Empathy Map, Interview Transcript, |   |      + HMW ~할 수 있을까?                  |
|           User Behavior Log                  |   |      + ① 늘리기 ② 줄이기 ③ 대체 ④ 뒤집기  |
|                                              |   |                                            |
+----------------------------------------------+   +--------------------------------------------+
                                                          |
                                                          v
+-------------------------------------------- Ideate -----------------------------------------+
|                                                                                             |
|  ① 규칙 기반 발산(Diverge)                                                                       |
|      + 브레인스토밍(Osborn 1953) — 판단중지(Defer Judgment), 양 추구(Quantity)                  |
|      + 6-3-5 / Brainwriting(6명이 3개씩 5회 작성) — 생산성 ×3, 평가편향 감소                    |
|      + SCAMPER 체크리스트 — Substitute·Combine·Adapt·Modify·Put to other use·Eliminate·Reverse |
|      + Six Thinking Hats(de Bono) — 병렬 사고 채널화                                          |
|  ② 아이디어 클러스터링(Idea Cluster)                                                              |
|      + 50~100개 raw ideas -> 7±2 토픽으로 그룹핑                                                 |
|  ③ 수렴(Converge) — 아이디어 선정                                                                 |
|      + Dot Voting / Impact-Effort Matrix(2×2)                                                  |
|      + Kano Model(기본/일차/매력/무관심/역)                                                      |
|      + Concept Selection Matrix(가중치 5개 기준: Reach·Impact·Confidence·Ease·Innovation)       |
|  ④ 선택 아이디어 -> Prototype로 핸드오프                                                            |
|      + Storyboard -> Paper Prototype -> Wireframe                                                 |
|                                                                                                |
|  * 산출물: Idea Backlog, Prioritized Concept, Storyboard                                          |
+------------------------------------------------------------------------------------------------+
```

### 2) 구성 요소 및 역할 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Empathy Map (4-Quadrant)** | 사용자 정성 데이터 시각화 | Says(말) / Thinks(생각) / Does(행동) / Feels(감정). 1인칭("나는 ~한다")으로 작성해 **진정성(Authenticity)** 확보. 항목당 최소 3개 이상 수집 후 인사이트 도출. |
| **Persona (Cooper, 1999)** | 대표 사용자 모델링 | Demographic + Psychographic + Behavior + Goals + Frustrations. 1차/2차/3차 페르소나 구분, **Negative Persona**(서비스에서 배제할 사용자군) 함께 정의. Alan Cooper의 Goal-Directed Design 기반. |
| **User Journey Map** | 시나리오별 경험 흐름 분석 | 단계(Stage) -> 행동(Behavior) -> 사고(Thoughts) -> 감정(Emotion) -> 페인포인트(Pain Point) -> 기회(Opportunity). 5단계 표준 모델: Awareness -> Consideration -> Decision -> Use -> Loyalty. |
| **POV (Point of View) Statement** | 재정의된 문제 진술문 | "[User] needs [Need] because [Insight]." 형태로 한 문장. 모호한 "좋은 UX"가 아닌 **검증 가능한 행동(Verifiable Action)**으로 표현. |
| **HMW (How Might We) Question** | POV -> 솔루션 도출 질문 | "How might we [verb] [object] so that [outcome]?" 형식. 산정범위(Scope) 명시: HMW(We, 우리조직), HMW users(사용자), HMW stakeholders(이해관계자). |
| **Brainwriting 6-3-5** | 아이디어 발산 | 6명 × 3아이디어 × 5라운드 = 90개 아이디어. 익명성으로 **생산 저하자(Production Blocking)** 해결. |
| **SCAMPER** | 기존 아이디어 변형 | 7가지 변환 연산자로 발산 촉진. 제품/서비스 고도화 시 강력. |
| **Dot Voting + Impact-Effort Matrix** | 아이디어 우선순위화 | 투표수 1차 필터 -> Impact(High/Low) × Effort(High/Low) 2×2 매트릭스로 Quick Win(High Impact·Low Effort) 선정. |
| **Storyboard** | 아이디어 시각화 | 4-Panel Comic 형식(상황->행동->결과->학습)으로 사용 시나리오 공유. Nielsen Norman Group 권장. |

### 3) 핵심 알고리즘·수식

**아이디어 우선순위 가중치 산정 (RICE Score 예시)**
```
RICE = (Reach × Impact × Confidence) / Effort
  · Reach: 기간 내 영향받는 사용자 수
  · Impact: 0.25(최소) / 0.5(낮음) / 1(중간) / 2(높음) / 3(대규모)
  · Confidence: 백분율 (50~100%)
  · Effort: 인-주(人-週) 기준
```

**정의(Define) 단계의 검증도(V&V) 체크**
- **Smart(지혜로운) 문제 기준**: Specific(구체)·Measurable(측정)·Achievable(실현)·Relevant(관련)·Time-bound(기한)
- **5 Whys 기법**: 1Why->2Why->3Why... 5회 이상 Why를 던져 근본원인(Root Cause) 도출. Toyota Production System 기반.

- **📢 섹션 요약 비유**: 공감은 **"흙속의 씨앗 발굴"**, 정의는 **"씨앗의 품종 식별"**, 아이디어는 **"씨앗에서 무성한 가지를 치기"**에 비유할 수 있다. 씨앗도 없이 가지를 만들면 가짜 잎사귀만 무성한 솔루션이 된다.

---

## Ⅲ. 비교 및 연결

### 1) 디자인 씽킹 vs 인접 방법론

| 구분 | **Design Thinking** | **Agile (Scrum)** | **Lean Startup** | **Double Diamond (UK Design Council)** |
| :--- | :--- | :--- | :--- | :--- |
| **주안점** | 사용자 이해 + 창의적 문제해결 | 반복적 인도(Delivery)·팀 셀프조직화 | 가설 검증·실험 중심 사업모델 | 문제/솔루션 공간의 발산-수렴 구조 |
| **시간 단위** | 스프린트(2~4주) × 다수 | 스프린트(1~4주) | Build-Measure-Learn 루프 | 단계별(Discover/Define/Develop/Deliver) |
| **핵심 산출물** | Empathy Map, POV, HMW, Storyboard | User Story, Increment, Burndown | MVP, Validated Learning, Pivot | Diamond Phase 산출물 |
| **데이터 유형** | 정성(Qualitative) 우세 | 정성+정량 혼합 | 정량(Metric) 우세 | 정성+정량 균형 |
| **적용 시점** | 신규/리디자인/0->1 | 구축·운영 단계 | 사업모델 불확실 시 | 광범위(정책/서비스/제품) |
| **리스크 관리** | Solution 리스크 조기 제거 | 일정·기술 리스크 지속 제거 | 시장·사업 리스크 조기 제거 | 양립 |
| **한계** | 측정·재현성 부족 | 사용자 진실 왜곡 가능 | 실험 설계 비용·B2B 적용 난이도 | 단계 간 핸드오프 모호 |

### 2) 공감·정의 도구 간 비교

| 구분 | **1:1 심층 인터뷰** | **현장 관찰 (Field Study)** | **사용자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 525 / 600

<- **이전**: [524. Nexus 다중 팀 스크럼 조율](/studynote/11_design_supervision/06_exam_summary/524_nexus_multi_team_scrum_coordination)
**다음**: [526. 린 스타트업 MVP 가설 검증](/studynote/11_design_supervision/06_exam_summary/526_lean_startup_mvp_hypothesis_validation/) ->

---
