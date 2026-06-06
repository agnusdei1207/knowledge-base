---
title: "517. PMBOK 프로젝트 관리 지식 체계 (PMBOK Project Management Body of Knowledge)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PMBOK(Project Management Body of Knowledge)는 PMI(1996년 첫 발간, 2021년 7th Edition 전면 개편)가 제시하는 프로젝트 관리 표준 프레임워크로, **5대 프로세스 그룹(Initiating/Planning/Executing/M&C/Closing) × 10대 지식 영역(Integration·Scope·Schedule·Cost·Quality·Resource·Communication·Risk·Procurement·Stakeholder) = 49개 프로세스**를 체계적으로 결합한 방법론 집합이며, 7판에서는 8개 성과 도메인(Performance Domain)과 12개 핵심 원칙(Principles of Project Management) 기반으로 패러다임 전환이 이루어졌다.
> 2. **가치**: 통계적으로 PMBOK 기반 표준 관리를 적용한 프로젝트는 **Schedule Performance Index(SPI) 평균 0.78->0.95, Cost Performance Index(CPI) 0.82->1.02 개선**되었고(PMI 2017 Pulse of the Profession), 실패율 9.4%(표준 미적용 21.4%)로 2배 이상의 성공률 차이를 보이며, 조직의 **OPM(Organizational Project Management) 성숙도 모델(OPM3)**과 연계 시 PMO 운영 효율성을 30~40% 향상시킨다.
> 3. **판단 포인트**: **Predictive(Waterfall) ↔ Adaptive(Agile/Hybrid)** 접근법의 선택이 핵심 트레이드오프이며, **요구사항 명확성(Volatility < 20%)**, **규제/감리 강도**, **납기 압박 정도**, **이해관계자 분포**에 따라 적절한 개발 접근법 및 수명주기(Development Approach)를 결정해야 한다. 또한 7판에서는 49개 프로세스를 모두 따르기보다 12개 원칙을 가치 기반으로 해석하여 **"Tailoring(맞춤화)"**가 강조된다.

---

## Ⅰ. 개요 및 필요성

프로젝트는 일상적 운영(Operation)과 달리 **"한정된 자원(3제약: 범위·일정·비용) 하에서 유일한 산출물(Deliverable)을 창출하는 임시적( temporary) 노력"**으로 정의된다(PMBOK 6판 §1.2.1). 그러나 2010년대 이후 IT 프로젝트의 **40~70%가 일정·예산 초과**(Standish Group CHAOS Report 2020: 성공 31%, 실패 58%, 도전 11%)라는 현실은, 프로젝트 관리가 담당자의 **개인 역량(Drive-by management)**에 의존해서는 안 됨을 시사한다.

PMBOK는 이러한 문제를 해결하기 위해 PMI가 **IEEE·ANSI 표준(ANSI/PMI 99-001-2017)**으로 채택한, 검증된 **Good Practice(우수 관행) 사전(辭典)**이다. 6판까지는 **프로세스 중심(process-based)**으로 49개 ITPs(Input-Tools-Techniques-Output) 컴포넌트를 명세했으나, 실무에서는 "이 49개 프로세스를 다 따라야 하는가?"라는 경직성 비판이 제기되었다. 이에 7판(2021)에서는 **원칙 중심(principles-based)**으로 전환하여, Agile·Lean·Design Thinking 등 다양한 접근법을 **"상황에 맞게 조율(tailoring)"**할 수 있도록 한 것이다.

기존 5대 프로세스 그룹 + 10대 지식 영역의 **Hard Master(통제·규범) 지향** 모델이, 7판의 **8대 성과 도메인 + 12대 원칙의 Soft Master(가치·맥락) 지향**으로 패러다임이 이동한 것은, **VUCA(Volatility·Uncertainty·Complexity·Ambiguity) 시대**의 프로젝트 거버넌스 요구를 반영한 것이다.

```text
         +---------------- PMBOK 진화 흐름(Evolution Roadmap) ----------------+
         |                                                                     |
         |   [1996 1st]      [2000 3rd]      [2008 4th]      [2017 6th]     [2021 7th]     |
         |   -------         --------        --------        --------       --------      |
         |   PM Framework    5PG×9KA         5PG×9KA         5PG×10KA        8 Performance  |
         |   (PMI 시작)      44 Processes    42 Processes    49 Processes    Domains       |
         |                                  + ITTO 명세      + Agile Annex   + 12 Principles|
         |                                                                     |
         |   <---- Process-Centric (How) ------>         <--- Value-Centric (Why) --->         |
         |   <---- Predictive 중심 ------------>         <---- Hybrid/Adaptive 병행 ---->       |
         +-----------------------------------------------------------------------------+
                                          |
                                          v
               +--------------- 왜 PMBOK이 필요한가? --------------+
               |                                                    |
               |  [프로젝트 실패 요인 Top 5]                          |
               |   1. 불완전한 요구사항(37%) -+                       |
               |   2. 사용자 저항(20%)        |  ->  PMBOK 5대 그룹  |
               |   3. 자원 부족(14%)          |     + 10대 영역이   |
               |   4. 비현실적 일정(11%)      |     시스템적으로    |
               |   5. 경영진 미지원(9%)  -----+     해결             |
               |                                                    |
               |  [연계 표준] ISO 21500:2021, ISO 21502, PRINCE2,  |
               |              CMMI v2.0, OPM3, BABOK, ITIL 4        |
               +----------------------------------------------------+
```

**Why PMBOK? (Old vs New Paradigm)**
- **구(舊) 패러다임**: 프로젝트 관리 = CPM/EV 계산 같은 **기술적 스킬** -> 계획-실행-통제의 선형 흐름
- **신(新) 패러다임**: 프로젝트 관리 = **시스템 사고 + 리더십 + 비즈니스 가치 실현** -> 불확실성 하의 적응적 가치 전달

특히 7판은 **"Principle ≠ Process"**라는 점을 명시한다. 원칙(예: "Be a diligent, respectful, and caring steward")은 모든 프로젝트에서 항상 참(True)인 **가치 지침**이며, 프로세스는 프로젝트의 **맥락에 따라 선택·적용**되는 절차이다. 이는 **ISO 21500:2021**의 "subject groups" 구조 및 **PRINCE2 7th Edition(2023)**의 7대 원칙과 컨버전스 흐름을 공유한다.

- **📢 섹션 요약 비유**: PMBOK은 자동차 운전의 **"도로교통법 + 운전 매뉴얼 + 신호체계"**와 같다. 매 운전자가 49개 신호(프로세스)를 다 기억할 필요는 없지만, "정지 신호는 멈춘다(원칙)"라는 절대 규칙은 알아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PMBOK 6판과 7판의 구조적 차이를 명확히 이해해야 한다. 6판은 **2차원 매트릭스(프로세스 그룹 × 지식 영역)** 구조이고, 7판은 **8대 성과 도메인의 유기적 통합** 구조이다.

### [6판 아키텍처] 5 Process Groups × 10 Knowledge Areas

```text
                        ┃ Initiating |  Planning  | Executing |  M&C      |  Closing
        ━━━━━━━━━━━━━━━╂━━━━━━━━━━━━╂━━━━━━━━━━━━╂━━━━━━━━━━━╂━━━━━━━━━━━╂━━━━━━━━━
        Integration(7)  ┃    2(I)     ┃     1      ┃    2      ┃    2      ┃    1
        Scope(6)        ┃             ┃     4      ┃    1      ┃    1      |
        Schedule(6)     ┃             ┃     5      ┃            ┃    1      |
        Cost(4)         ┃             ┃     3      ┃            ┃    1      |
        Quality(3)      ┃             ┃     1      ┃    1      ┃    1      |
        Resource(6)     ┃             ┃     2      ┃    3      ┃    1      |
        Communications(3)┃           ┃     1      ┃    1      ┃    1      |
        Risk(7)         ┃             ┃     5      ┃    1      ┃    1      |
        Procurement(3)  ┃             ┃     1      ┃    1      ┃    1      |
        Stakeholder(4)  ┃    1(I)     ┃     1      ┃    1      ┃    1      |
        ━━━━━━━━━━━━━━━╂━━━━━━━━━━━━╂━━━━━━━━━━━━╂━━━━━━━━━━━╂━━━━━━━━━━━╂━━━━━━━━━
        Total = 49 Processes
        ※ (I) = Project Initiating에 한정되는 프로세스
```

각 프로세스는 **ITTO(Input-Tools & Techniques-Output)** 표준 형식을 따른다. 예: `6.4 Conduct Procurements` -> Input: Procurement Management Plan, Bid Documents, Proposals / Tools: Bidder Conferences, Proposal Evaluation, Independent Estimates, Advertising, Analytical Techniques, Expert Judgment, Procurement Negotiations / Output: Selected Sellers, Agreements, Change Requests, Project Management Plan Updates.

### [7판 아키텍처] 8 Performance Domains × 12 Principles

```text
              +------------- 12 Principles (모든 도메인에 횡단 적용) -------------+
              |  ① Be a diligent, respectful, and caring steward                   |
              |  ② Create a collaborative project team environment                |
              |  ③ Effectively engage with stakeholders                           |
              |  ④ Focus on value                                                 |
              |  ⑤ Recognize, evaluate, and respond to system interactions        |
              |  ⑥ Demonstrate leadership behaviors                               |
              |  ⑦ Tailor based on context                                       |
              |  ⑧ Build quality into processes and deliverables                 |
              |  ⑨ Navigate complexity                                           |
              |  ⑩ Optimize risk responses                                       |
              |  ⑪ Embrace adaptability and resiliency                           |
              |  ⑫ Enable change to achieve the envisioned future state          |
              +------------------------------------------------------------------+
                                          |  (Hollow Fiber: 모든 도메인을 관통)
                                          v
   +------------------+  +------------------+  +------------------+  +------------------+
   |  1. Stakeholders  |  |  2. Team         |  |  3. Development  |  |  4. Planning      |
   |                  |  |                  |  |  Approach &      |  |                  |
   | • 식별·분석·참여 |  | • 리더십·문화   |  |  Life Cycle      |  | • 배달 계획      |
   | • 기대치 관리    |  | • 역량 빌드업    |  | • 예측/적응/하이 |  | • 일정·비용·범위|
   | • 의사소통       |  | • 고성능 팀      |  |   브리드 선택    |  | • 변경 통제      |
   +------------------+  +------------------+  +------------------+  +------------------+
   +------------------+  +------------------+  +------------------+  +------------------+
   |  5. Project Work  |  |  6. Delivery     |  |  7. Measurement  |  |  8. Uncertainty   |
   |                  |  |                  |  |                  |  |                  |
   | • 자원·조달      |  | • 범위·일정·품질|  | • 성과 측정      |  | • 리스크 식별    |
   | • 변경·학습      |  | • 인수인계       |  | • EVM, KPI       |  | • 기회·위협 대응 |
   | • 의사소통·계약  |  | • 가치 전달      |  | • 개선 활동      |  | • 복잡성 관리    |
   +------------------+  +------------------+  +------------------+  +------------------+
                                          |
                                          v
                              +-------------------------+
                              |   Project Value Delivery|
                              |   (비즈니스 가치 실현)   |
                              +-------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **5 Process Groups (6판)** | 프로젝트 생명주기 단계화 | Initiating(2개) -> Planning(24개) -> Executing(10개) -> Monitoring & Controlling(12개) -> Closing(1개). **Iterative & Incremental** 가능(예: Agile Sprint 단위로 M&C 반복) |
| **10 Knowledge Areas (6판)** | 49개 프로세스를 주제별로 묶은 전문 영역 | Integration(7)·Scope(6)·Schedule(6)·Cost(4)·Quality(3)·Resource(6)·Communication(3)·Risk(7)·Procurement(3)·Stakeholder(4). 각 KA는 고유 ITTO를 통해 상호 의존성 매트릭스로 연결 |
| **8 Performance Domains (7판)** | 프로젝트 활동의 결과 지향적 묶음 | 6판의 "10개 KA"를 통합·재편: Stakeholder, Team, Development Approach & Life Cycle, Planning, Project Work, Delivery, Measurement, Uncertainty. 각 도메인은 **"Outcomes(성과)"**로 정의되어 측정 가능 |
| **12 Principles (7판)** | 모든 도메인에 횡단 적용되는 가치 기반 지침 | **"True in every project, true all the time"**. 프로젝트의 size/complexity/applicability에 무관하게 항상 참. **Tailoring(맞춤화)** 시 우선순위 가이드 역할 |

**핵심 메커니즘 (EVM: Earned Value Management)**

EVM은 **Schedule(일정) × Cost(비용) × Scope(범위)**를 통합 측정하는 6판의 핵심 도구이다. 다음 4개 지표의 2차원 매트릭스로 프로젝트 상태를 진단한다.

| 지표 | 공식 | 정상 범위 | 진단 |
|:---|:---|:---|:---|
| **PV(Planned Value)** | BCWS = 계획된 작업의 예산 | — | "지금까지 이만큼 *할당*되었어야 함" |
| **EV(Earned Value)** | BCWP = 실제 완료된 작업의 예산 | — | "지금까지 이만큼 *성취*함" |
| **AC(Actual Cost)** | ACWP = 실제 투입된 비용 | — | "지금까지 이만큼 *지출*함" |
| **SV(Schedule Variance)** | EV − PV | ≥ 0 | 음수면 **일정 지연** |
| **CV(Cost Variance)** | EV − AC | ≥ 0 | 음수면 **예산 초과** |
| **SPI(Schedule Performance Index)** | EV / PV | ≥ 1.0 | 0.8 이하 = 위험, 0.6 이하 = 즉시 시정 |
| **CPI(Cost Performance Index)** | EV / AC | ≥ 1.0 | 0.8 이하 = 비용 회수 불가 수준 |
| **EAC(Estimate At Completion)** | BAC / CPI | — | **완료 시 예상 총비용** |
| **ETC(Estimate To Complete)** | E
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 517 / 600

<- **이전**: [516. 위험 관리 프레임워크 리스크 평가](/studynote/11_design_supervision/06_exam_summary/516_risk_management_framework_assessment)
**다음**: [518. 프린스2 프로젝트 관리 방법론](/studynote/11_design_supervision/06_exam_summary/518_prince2_project_management_methodology/) ->

---
