+++
title = "애자일 관리 (Agile Management)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

> **핵심 인사이트 3줄**
> 1. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 관리([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))는 짧은 반복 주기([스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/))를 통해 고객 가치를 지속 전달하고, 변화에 신속히 적응하는 인간 중심의 경량 프로젝트 관리 방식이다.
> 2. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 선언(2001년)의 4대 가치와 12원칙이 이론 기반이며, [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)·[Kanban](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/)·SAFe가 주요 실천 프레임워크로 대부분의 IT 프로젝트에 적용되고 있다.
> 3. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)의 핵심은 '계획 준수'가 아닌 '적응과 학습'이며, 측정 지표(벨로시티·[번다운 차트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/072_burndown_burnup_chart/)·사이클 타임)로 팀 성과를 가시화하고 지속적으로 개선하는 것이다.

---

## Ⅰ. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 선언과 4대 가치

### [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 선언 ([Agile Manifesto](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/061_agile_manifesto/), 2001)

> 우리는 소프트웨어를 개발하고, 또 다른 사람의 개발을 도와주면서 소프트웨어 개발의 더 나은 방법들을 찾아가고 있다.

| 더 가치 있는 것    | ← 보다       | 덜 가치 있는 것     |
|-----------------|------------|-------------------|
| 개인과 상호작용   | 프로세스와 도구 |
| 작동하는 소프트웨어| 포괄적인 문서   |
| 고객과의 협력     | 계약 협상      |
| 변화에 대응하기   | 계획을 따르기  |

📢 **섹션 요약 비유**: [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 4대 가치는 회사 철학이다 — 규정집(프로세스)보다 대화(개인), 보고서(문서)보다 작동하는 제품, 계약서(계약)보다 파트너십(협력)을 중시한다.

---

## Ⅱ. [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) 프레임워크

### [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) 3대 역할

| 역할              | 책임                              |
|-----------------|----------------------------------|
| Product Owner (PO) | [제품 백로그](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/066_product_backlog_grooming/) 관리·우선순위 결정   |
| [Scrum Master](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/064_scrum_master_sm/) ([SM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/))  | 팀 코치·장애물 제거·[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 촉진  |
| [Development Team](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/065_development_team_scrum/)   | 자기 조직화 개발 (3~9명)         |

### [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) 이벤트 (2주 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 기준)

```
스프린트 계획 (Planning) — 2h
    ↓ 개발 (Sprint 1~10일)
       ↓ 데일리 스크럼 (Daily, 15분)
    ↓
스프린트 리뷰 (Review) — 2h (고객 데모)
스프린트 회고 (Retrospective) — 1.5h (팀 개선)
    ↓ 다음 스프린트 시작
```

### 산출물

| 산출물              | 설명                              |
|------------------|----------------------------------|
| [Product Backlog](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/066_product_backlog_grooming/)  | 전체 기능 목록 (PO가 우선순위 관리)|
| [Sprint](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) Backlog   | 현 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 목록            |
| Increment        | [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 결과물 (잠재 출시 가능)  |

📢 **섹션 요약 비유**: [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)는 마라톤 대신 릴레이 경주다 — 2주마다 배턴(Increment)을 넘기며 방향을 수정하고, 다음 구간을 더 잘 달릴 준비를 한다.

---

## Ⅲ. [Kanban](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) 보드와 WIP 제한

```
Kanban 보드:

To Do         In Progress     In Review      Done
┌──────────┐  ┌──────────┐   ┌──────────┐  ┌──────────┐
│ 기능 A   │  │ 기능 B   │   │ 기능 C   │  │ 기능 D   │
│ 기능 E   │  │ 기능 F   │   │          │  │ 기능 G   │
│ 기능 H   │  │ (WIP=2)  │   │ (WIP=1)  │  │          │
└──────────┘  └──────────┘   └──────────┘  └──────────┘
WIP 제한 없음   최대 2개        최대 1개
```

**WIP([Work In Progress](/knowledge-base/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/)) 제한**: 동시 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 작업 수를 제한해 흐름 개선·대기 시간 단축

**리틀의 법칙**: 사이클 타임 = WIP / [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)

📢 **섹션 요약 비유**: WIP 제한은 주방장이 동시에 요리할 수 있는 접시 수 제한이다 — 너무 많이 올리면 다 식고, 적당히 제한해야 따뜻한 요리가 나온다.

---

## Ⅳ. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 측정 지표

| 지표              | 계산·설명                         |
|-----------------|----------------------------------|
| 벨로시티 (Velocity) | [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)당 완료 [스토리 포인트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/082_story_point_velocity/)    |
| [번다운 차트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/072_burndown_burnup_chart/)        | 남은 작업량 vs 시간 (이상: 우하향) |
| 사이클 타임        | 작업 시작 → 완료까지 경과 시간   |
| [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)         | 요청 등록 → 완료까지 총 시간      |
| [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 탈출률        | 프로덕션에서 발견된 버그 비율      |

### [번다운 차트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/072_burndown_burnup_chart/)

```
포인트
40 ┤●
35 ┤  ●
30 ┤    ●
25 ┤      ●
20 ┤        ●
15 ┤          ● ← 이상적 번다운
10 ┤
 5 ┤
 0 ┤────────────────→ 날짜 (스프린트 기간)
```

📢 **섹션 요약 비유**: [번다운 차트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/072_burndown_burnup_chart/)는 눈사람 녹이기 게임이다 — 매일 얼마나 녹였는지(완료했는지) 그래프로 보여주며, [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 끝에 0이 되면 성공이다.

---

## Ⅴ. [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/) ([Scaled Agile Framework](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)) — [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/)

```
SAFe 계층:
Essential SAFe: 팀 + ART (Agile Release Train) 수준
Large SAFe:    Portfolio + Solution + ART + Team
```

### [PI](/knowledge-base/studynote/12_it_management/01_governance_strategy/009_process_innovation/) (Program Increment) Planning

- 전체 팀(100명+)이 분기별 8~12주 로드맵 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)
- 팀 간 의존성 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)·조율
- 공통 [PI](/knowledge-base/studynote/12_it_management/01_governance_strategy/009_process_innovation/) 목표 수립

### [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/) vs [Kanban](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) vs [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)

| 프레임워크  | 적합 팀 규모   | 주요 특징            |
|----------|-------------|---------------------|
| [Scrum](/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/)    | 3~9명 단일 팀 | 2주 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)·역할 분담 |
| [Kanban](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/)   | 운영·지원 팀  | 흐름 최적화·WIP 제한  |
| [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)     | 100명+ 기업  | 포트폴리오·[ART](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/) 조율   |

📢 **섹션 요약 비유**: SAFe는 여러 팀이 같은 악보로 연주하는 오케스트라다 — 각 파트(팀)가 독립적이지만 [PI](/knowledge-base/studynote/12_it_management/01_governance_strategy/009_process_innovation/) 계획(리허설)으로 전체 곡(제품)을 맞춘다.

---

## 📌 관련 개념 맵

```
애자일 관리 (Agile Management)
├── 이론 기반
│   ├── 애자일 선언 (4대 가치·12원칙)
│   └── 린(Lean) 사고방식
├── 프레임워크
│   ├── Scrum (반복·역할·이벤트)
│   ├── Kanban (흐름·WIP 제한)
│   └── SAFe (대규모 조율)
├── 측정 지표
│   ├── 벨로시티 / 번다운 차트
│   └── 사이클 타임 / 리드 타임
└── 관련 개념
    ├── DevOps (애자일 + 운영)
    ├── 스프린트 / PI Planning
    └── 지속적 개선 (카이젠)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
┌─────────────────────────────────────────────────────────────────┐
│               애자일 관리 발전 흐름                              │
├──────────────┬────────────────────┬─────────────────────────────┤
│ 1986년       │ Scrum 개념 등장    │ Takeuchi·Nonaka "럭비 팀"   │
│ 1995년       │ Scrum 공식화       │ Sutherland·Schwaber         │
│ 2001년       │ 애자일 선언        │ 17인 스노버드 모임           │
│ 2011년       │ SAFe 1.0 발표      │ 대기업 애자일 확장           │
│ 2016년       │ Scrum@Scale        │ Sutherland 확장 프레임워크   │
│ 2020년대     │ 디지털 네이티브    │ 전 산업 애자일 확산          │
└──────────────┴────────────────────┴─────────────────────────────┘

핵심 키워드 연결:
애자일 선언 → Scrum → 스프린트 → 벨로시티 → 번다운 차트
     ↓            ↓          ↓           ↓
4대 가치     PO/SM/Dev   2주 반복    측정·개선
     ↓
SAFe → 대규모 PI Planning → 포트폴리오 레벨 애자일
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)은 2주마다 숙제를 제출하는 방식이다 — 학기 말 한 번 내는 것보다 중간중간 피드백을 받으면 더 좋은 결과물이 나온다.
2. [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)는 짧은 달리기다 — 마라톤(폭포수)이 아니라 2주씩 전력 질주하고, 쉬면서 방향을 확인한다.
3. [Kanban](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) WIP 제한은 요리사가 동시에 담을 수 있는 접시 수다 — 너무 많이 담으면 다 식고, 적당히 제한하면 신선하게 나온다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 587

← **이전**: [32. 네트워크 효과 (Network Effect) / 메트칼프의 법칙](/knowledge-base/studynote/12_it_management/01_governance_strategy/032_network_effect/)
**다음**: [33. 플랫폼 비즈니스 모델 (Platform Business Model)](/knowledge-base/studynote/12_it_management/01_governance_strategy/033_platform_business_model/) →

---
