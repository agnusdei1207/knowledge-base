---
title: "PSP TSP Personal Team Software Process"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PSP는 개발자 개인의 작업 데이터를 정량적으로 수집·분석하여 프로세스 성숙도를 5단계(PSP0->PSP3)로 향상시키는 Watts Humphrey의 개인 단위 SW 프로세스이며, TSP는 이를 팀 차원으로 확장하여 Launch->Strategy->Plan->Requirements->Design->Implementation->Test->Post-mortem의 8단계 팀 워크플로우를 통해 CMM/CMMI Level 5 실현을 목표とする 디시플린된 팀 프로세스입니다.
> 2. **가치**: SEI 사례 연구에서 PSP 적용 시 초기에 평균 21.5%->68.5%로 결함 제거 효율(DRE, Defect Removal Efficiency)이 상승하고, TSP 적용 시 생산성이 35-78% 향상, 결함 주입률이 50% 이상 감소하는 정량적 효과가 보고되었으며, 개발자 개인의 자기 추정 정확도가 ±20% 오차 범위에서 ±10% 이내로 개선됩니다.
> 3. **판단 포인트**: PSP는 "측정 없는 개선은 불가능하다(Garbage In, Garbage Out)"는 원칙 아래 시간·결함·규모의 3대 메트릭을 모두 수집해야 하므로 초기 오버헤드 15-30%가 발생하며, TSP는 팀 규모 3-20명, 동질적 기술 스택, 명확한 역할 분담이 가능한 프로젝트에서 ROI가 극대화됩니다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 위기(Software Crisis) 이후 1968년 NATO 회의에서 등장한 SW 공학은 1980년대까지 주로 거시적 프로세스(Waterfall, Spiral, RUP 등)에 집중했습니다. 그러나 1990년대 초 SEI(Carnegie Mellon University Software Engineering Institute)의 **Watts S. Humphrey**는 "공정의 성숙도 향상을 위해서는 결국 개발자 개개인의 작업 습관과 프로세스 개선이 선행되어야 한다"는 핵심 통찰을 통해 개인 단위 프로세스인 **PSP(1995)**를 발표하고, 이를 확장한 팀 단위 프로세스인 **TSP(1996~2000)**를 통해 "Process-Centric 품질 경영" 패러다임을 완성했습니다.

기존 SW 개발의 문제점: 통상적인 SW 프로젝트에서 요구사항 결함·설계 결함·코딩 결함이 약 **5:3:2** 비율로 발생하며, 개발자 1인당 평균 결함 주입률(Defect Injection Rate)은 KLOC(Kilo Lines of Code) 당 25-100개에 달합니다. 그러나 1990년대 이전에는 결함 발생 시 그 원인을 개인의 "부주의"로 치부하고 정량적 데이터 없이 재작업하는 일이 반복되어, 동일 형태의 결함이 재발생하는 **결함 재발률(Recurrence Rate) 60% 이상**의 악순환이 지속되었습니다. 또한 CMM(Capability Maturity Model) Level 4-5 달성을 위해 요구되는 정량적 프로젝트 관리(QPM, Quantitative Project Management)는 조직 차원의 메트릭을 위해서는 결국 개인의 원시 데이터가 필수적이므로, PSP 없이는 TSP/CMMI Level 5 달성이 불가능합니다.

```text
[PSP/TSP 필요성 도식도]

   +----------------------------------------------+
   |      거시적 프로세스만으로는 해결 불가              |
   |  (Waterfall / RUP / Agile - 조직 단위)          |
   +--------------------+-------------------------+
                        | 한계 노출
                        v
   +----------------------------------------------+
   | 문제 1. 결함 원인 분석 불가 (측정 부재)            |
   | 문제 2. 개인별 생산성 편차 ±200% 이상             |
   | 문제 3. 규모/일정 추정의 ±50% 이상 오차           |
   | 문제 4. 결함 재발률 60% 이상 (학습 부재)          |
   +--------------------+-------------------------+
                        | Humphrey의 통찰
                        v
   +----------------------------------------------+
   |  "개인의 프로세스 개선이 조직의 성숙도를 좌우한다"   |
   |        -- Watts S. Humphrey --                |
   +--------------------+-------------------------+
                        |
          +-------------+--------------+
          v                            v
   +-------------+              +--------------+
   |   PSP       |              |   TSP        |
   | (1995~)     | ----------->  | (1996~2000)  |
   | 개인 단위    |              | 팀 단위       |
   | 5단계 성숙도 |              | 8단계 워크플로  |
   +-------------+              +--------------+
          |                            |
          +-------------+--------------+
                        v
            +--------------------+
            |  CMMI Level 4-5    |
            |  정량적 프로젝트 관리|
            |  (QPM, OPP)        |
            +--------------------+
```

- **📢 섹션 요약 비유**: PSP/TSP는 마치 **운동선수의 코칭 시스템**과 같습니다. 단순히 "더 잘 달리라"고 외치는 코치(전통적 관리자)가 아니라, 달리기 시간·심박수·발구르기 각도·산소 흡입량을 정량적으로 측정하여 개인별 맞춤 훈련 처방을 내리고, 이를 팀 단위 전술로 통합하는 **데이터 기반 코칭 체계**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PSP는 **스크립트(Script)**, **양식(Form)**, **표준(Standard)**, **측정(Measurement)**의 4대 구성요소를 통해 개인의 작업 흐름을 표준화합니다. PSP의 가장 핵심적인 메커니즘은 **사이클(cycle)** 단위의 PDCA(Plan-Do-Check-Act) 적용입니다. 한 사이클은 Plan(계획) -> Development(개발: 설계·코딩·컴파일·테스트) -> Post-mortem(사후 분석) 3단계로 구성되며, 각 단계에서 **LOG 양식**에 시간·결함·규모 데이터를 실시간 기록합니다.

**PROBE(Proxy-Based Estimating) 방법**은 PSP2/PSP2.1에서 사용하는 핵심 규모 추정 기법으로, 기능(function) 또는 클래스/메서드 단위로 과거 사이클의 Proxy Size(중간 산출물 라인 수, LOC/Method 또는 LOC/Object)를 기반으로 신규 작업의 **Size = (B + √Σ(Pi-B)² / (n-1)) × (1-β)** 공식을 적용하여 베이지안 추정합니다. 여기서 B는 베이스 추정치, Pi는 과거 데이터, β는 프로젝트별 보정 계정(보통 0~0.5)입니다.

TSP는 4단계 팀 빌드 사이클(Launch->Steady) 반복과 8개의 프로세스 스크립트로 구성됩니다. 각 스크립트는 명확한 입력(Input), 역할(Role), 결과물(Artifact)을 정의하며, **개발자별 역할(Developer Role)**, **테스터(Test Role)**, **설계자(Designer Role)**, **PM/팀 리더(Team Leader)**의 4-Role 모델이 표준입니다. 특히 **TSP Coach**는 별도 역할을 맡아 프로세스 준수를 모니터링합니다.

```text
[PSP 단계별 성숙도 다이어그램]

   PSP0          PSP0.1          PSP1           PSP1.1
   (기초)         (측정)          (추정)         (품질관리)
     |              |              |              |
     | 현재 프로세스 | 표준 측정     | Size 추정    | Code Review
     | 시간 기록     | 결함 추적     | LOC/시간     | 품질 기준
     |              |              | Test Report  |
     |              |              |              |
     +--------------+------+-------+--------------+
                            |
                            v
                  PSP2           PSP2.1           PSP3
                  (디자인)        (통합)            (고도화)
                    |              |                |
                    | Code         | 통합 테스트     | CBB Database
                    | Templates    | Cyclic         | Process
                    | Design       | Development    | Customization
                    | Review       | PSP2.1 Script  | Quality Mgmt
                    |              |                |
                    +--------------+----------------+

[TSP 8단계 워크플로우]

   +--------+  +--------+  +--------+  +--------+
   | Launch |-> |Strategy|-> |  Plan  |-> | Req.   |
   |        |  |        |  |        |  |Design  |
   +--------+  +--------+  +--------+  +--------+
                                              |
   +--------+  +--------+  +--------+  +--------+
   | Post-  |<- |Integr. |<- |  Test  |<- |  Impl. |
   |mortem  |  |  Test  |  |        |  |        |
   +--------+  +--------+  +--------+  +--------+

   ※ 각 단계에서 4-Role(Role Assignment) 수행
   ※ 각 단계 종료 시 Team Meeting(30-60분) 필수
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **PSP Script** | 단계별 작업 절차 표준화 | PSP0~3 단계별 입력/출력/역할/체크리스트 정의. 각 단계마다 Plan-Time(계획), Development-Time(설계·코딩·컴파일·테스트), Postmortem-Time(분석) 3개 스크립트 합계 21개 표준 스크립트 제공 |
| **LOG / Forms (양식)** | 정량적 데이터 수집 | **Time LOG**(단계별 분 단위 시간), **Defect LOG**(유형·주입·제거 단계·고친 시간·설명), **Size LOG**(LOC/Proxy Size), **Plan Summary**, **PIP(Productivity Improvement Plan)**. 결함 유형 10가지(10 types: Syntax, Assignment, Interface, Checking, Data, Function, System, Environment, Build, Documentation)로 분류 |
| **PROBE Method** | 베이지안 규모/공수 추정 | Size = (베이스 + 표준편차·보정) 공식 적용, 기능 단위 Proxy Size(Pi) 수집 후 베이지안 업데이트. A/AS(Available/Allocated Size) 구분, **A/AF(Added/Adapted/Function) 분류법** 사용 |
| **Design & Code Review** | 결함 조기 발견 | PSP2의 **Design Review Checklist**(30-40개 항목)와 **Code Review Checklist**(50-70개 항목)를 통한 Walkthrough. 결함 발견 시 Defect Type별 분류 및 Fix Time 기록 |
| **TSP Team Process** | 팀 단위 프로세스 통합 | 8단계 스크립트, 4-Role 모델(Dev/Quality/Process-Support/Managerial), **TSP Coach**의 독립적 모니터링. Team Meeting Protocol(Agenda->Issue List->Action Item), **Inspection Rate** 목표(소스 200 LOC/h, 문서 2-3 page/h) |
| **CBB (Component-Based Development)** | 재사용 자산 관리 | PSP3의 CBB Database, 재사용 컴포넌트별 Size/Defect/Time 데이터 축적, 신규 프로젝트에서 재사용 시 추정 정확도 향상 및 결함률 감소 |
| **PIP (Process Improvement Plan)** | 개인 개선 로드맵 | 6주 단위 학습 사이클, 매 사이클 종료 시 결함 추이 그래프(PAD, Process Appraisal Data)와 PIP 갱신. 4가지 결함 제거 효율(DRE) 측정: **Compile DRE, Unit Test DRE, System Test DRE, Total DRE** |
| **QPM & OPP** | 정량적 프로젝트 관리 | TSP 상위 레벨로, Ray Stratton의 Quality Management Maturity Grid 기반. **가설검정(Hypothesis Testing)**, **Causal Analysis**, **Pareto Chart**, **Control Chart** 활용, CMMI Level 4-5의 Process Performance Model과 Baseline 확보 |

PSP에서 사용하는 **결함 주입 단계(Defect Injection Phase)** 와 **제거 단계(Defect Removal Phase)** 의 추적은 핵심입니다. 개발자 본인이 "이 결함을 어느 단계에서 만들었는가(Injection)"와 "어느 단계에서 발견했는가(Removal)"를 기록하면, 이를 통해 **결함 제거 효율 DRE = (Removed in Phase / Total Injected in Process)×100%** 을 산출할 수 있습니다. 예: 요구사항 결함 10개 주입 -> 8개 제거 -> DRE 80%.

- **📢 섹션 요약 비유**: PSP의 데이터 수집은 **비행기의 블랙박스**와 같습니다. 조종사(개발자)는 비행(코딩)이 끝난 후 블랙박스를 분석하여 비행 패턴을 개선하고, PSP 단계는 블랙박스를 더 정교하게 만드는 업그레이드(PSP0->3)이며, TSP는 여러 비행기의 블랙박스 데이터를 합쳐 항공 관제 시스템(팀 프로세스)을 만드는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

PSP/TSP를 다른 SW 공학 프레임워크와 비교합니다. 특히 PSP/TSP는 다른 방법론을 대체하는 것이 아니라 **측정 기반의 보완 계층**이라는 점이 핵심입니다.

| 구분 | **PSP/TSP** | **CMM/CMMI** | **Agile/Scrum** | **6 Sigma** | **ISO 15504 (SPICE)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **적용 단위** | 개인(PSP) + 팀(TSP) | 조직 | 팀 | 조직/프로세스 | 조직/프로세스 |
| **핵심 활동** | 정량적 자기 측정·개선 | 5-Level 성숙도 평가 | 반복-점진(Sprint) | DMAIC, 통계적 품질 관리 | 프로세스 능력 평가/측정 |
| **데이터 수집** | Time/Defect/Size 3대 메트릭 100% | 프로세스별 Evidence | Velocity/Burn-down | DPMO, Sigma Level | Process Attribute 점수 |
| **추정 방법** | PROBE (베이지안) | QPM (Process Performance Model) | Story Point/Planning Poker | CTQ(Yield) 기반 | Capability Level |
| **주 저자/출처** | Watts Humphrey / SEI-CMU | SEI-CMU | Beck/Sutherland (1995~) | Motorola (1986) | ISO/IEC JTC1/SC7 |
| **문서 중시도** | 매우 높음 (LOG/표준) | 높음 (Policy/Procedure) | 낮음 (Working Software) | 중간 (DMAIC Artifacts) | 높음 (Process Reference Model) |
| **장점** | 개인별 정량적 개선, Causal Analysis 가능 | 조직 정렬, 평가 가능 | 변화 대응력, 빠른 피드백 | 통계적 결함 분석, ROI 명확 | 국제 표준, 측정 가능 |
| **단점** | 초기 오버헤드 15-30%, 학습 곡선 가파름 | 평가 비용, 경직 | 개인 추정 정확도 낮음, 측정 부족 | SW 도메인 적용 사례 부족 | 평가 복잡, 인증 비용 |
| **결합 시너지** | **CMMI Level 4-5의 데이터 소스** | **PSP/TSP를 조직 차원 통합** | **Scrum + PSP(Scrum+PSP)** | 통계적 결함 분석 보완 | **CMMI와의 호환성** |

**연결 관계:**
- **CMMI ↔ PSP/TSP**: PSP는 CMMI Level 4-5의 PP(QP, Quantitative Process Management) 영역에서 요구하는 "개인 단위 원시 데이터"의 원천입니다. CMMI 모델에서 IPP(Integrated Product Development)의 측정 요구사항(MA, Measurement & Analysis)을 PSP LOG 데이터가 충족합니다.
- **TSP ↔ Scrum**: Scrum은 PO(PO, Product Owner), SM(Scrum Master), Dev Team의 3-Role 모델이며, TSP는 4-Role(개발/QA/PM/Coach) 모델입니다. TSP의 **Team Meeting** 은 Scrum의 **Daily Stand-up** 보다 무겁지만, **PSP/TSP**를 Scrum과 결합한 사례(Scrum+PSP, 평균 Velocity 25-40% 향상 보고)가 있습니다.
- **PSP ↔ 6 Sigma**: PSP는 6 Sigma의 DMAIC 중 **Measure/Analyze** 단계를 개인 차원에서 수행하며, 결함 유형별 Pareto 분석(상위 3개 결함 유형이 70% 이상 차지)을 통해 **DFSS(Design for Six Sigma)** 의 통계적 사고를 제공합니다.
- **PSP ↔ TDD/BDD**: PSP의 Test-First 스크립트와 TDD(테스트 주도 개발)는 철학적으로 일치합니다. PSP가 강조하는 **Test Report LOG**는 TDD의 Red-Green-Refactor 사이클 데이터를 자연스럽게 수집합니다.
- **TSP
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 512 / 600

<- **이전**: [511. SPICE ISO 15504 프로세스 평가](/studynote/11_design_supervision/06_exam_summary/511_spice_iso_15504_process_assessment)
**다음**: [513. FPA 기능점 분석 규모 산정](/studynote/11_design_supervision/06_exam_summary/513_fpa_function_point_analysis_size_estimat/) ->

---
