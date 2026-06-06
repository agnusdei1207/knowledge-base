---
title: "State Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/) ([State Pattern](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))은 GoF 행위 패턴으로, 객체([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))의 내부 상태에 따라 행동(동작)이 달라질 때, 각 상태를 독립적인 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 클래스로 캡슐화하여 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)와 행동 변경을 상태 객체 자신에게 위임하는 패턴이다.
> 2. **가치**: 상태 증가 시 발생하는 거대한 조건 분기([switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)/if-else)를 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 클래스로 분산시켜 코드 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)과 유지보수성을 높이고, 새 상태 추가 시 [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 코드를 수정하지 않아도 되어 OCP를 달성한다.
> 3. **판단 포인트**: [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)에서 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 객체 자신이 결정한다([Context](/studynote/02_operating_system/01_overview_architecture/033_context/).setState()를 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 내부에서 호출). 외부에서 상태를 교체하는 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)과의 차이점이다. 상태 수가 2~3개에 불과하고 전이가 단순하다면 패턴 적용 없이 조건 분기가 더 명확할 수 있다.

---

## Ⅰ. 개요 및 필요성

주문 처리 시스템에서 주문 상태(접수->처리->배송->완료·취소)에 따라 가능한 동작이 다르다. 상태별 조건 분기로 구현하면: `if (state == "접수") { ... } else if (state == "처리") { ... }` — 상태 수 증가로 코드가 폭발하고, 새 상태 추가 시 여러 곳을 수정해야 한다.

[상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)은 각 상태를 `OrderState` 인터페이스의 구현 클래스(`ReceivedState`, `ProcessingState`, `ShippedState`, `CancelledState`)로 캡슐화한다.

```text
+-------------------------------------------------------------+
|              상태 패턴 구조                                   |
+-------------------------------------------------------------+
|  Context (Order)                                            |
|  - state: OrderState                                        |
|  + setState(s: OrderState): void                            |
|  + process(): void { state.process(this); }                 |
|  + cancel(): void  { state.cancel(this); }                  |
|                                                             |
|  OrderState (인터페이스)                                     |
|  + process(ctx: Order): void                                |
|  + cancel(ctx: Order): void                                 |
|       ^                                                     |
|  ReceivedState  ProcessingState  ShippedState  CancelledState|
|  (각 상태에서 가능한 동작 구현 + 다음 상태 전이 결정)       |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 신호등([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))은 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(빨강·노랑·초록)에 따라 동작이 다르고, 각 상태가 다음 상태로의 전이 규칙을 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)에서 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 어디서 결정되는지가 핵심이다. 두 가지 방식: ① [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 내부 전이: `ReceivedState.process(ctx) { ctx.setState(new ProcessingState()); }` — 상태 객체 자신이 다음 상태를 결정(GoF 권장), ② [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 중앙 전이: Context가 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 테이블을 갖고 결정 — 전이 규칙이 한 곳에 집중됨.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 내부 전이 | 상태 캡슐화, [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) | 상태 간 결합 |
| [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 중앙 전이 | 전이 규칙 한 눈에 파악 | [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 비대화 |
| 상태 머신 프레임워크 | 선언적 전이 정의 | 학습 곡선 |

```text
+-------------------------------------------------------------+
|       주문 상태 전이 다이어그램                               |
+-------------------------------------------------------------+
|  [접수] -> process() -> [처리중] -> ship() -> [배송중]          |
|     |                    |                    |             |
|  cancel()            cancel()             (취소 불가)       |
|     |                    |                                  |
|     v                    v                                  |
|  [취소됨]            [취소됨]                                |
|                                            -> complete()     |
|                                               [완료]        |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 주문([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))은 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 객체에게 동작을 위임하고, 상태 객체가 다음 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)를 결정한다. 주문 시스템은 상태 내부 구현을 알 필요 없다.

---
## Ⅲ. 비교 및 연결

[상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)과 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 구조가 동일하지만 의도가 다르다. 이 비교는 기술사 시험의 단골 주제다.

| 비교 축 | A | B |
|:---|:---|:---|
| 상태/[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 교체 주체 | [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 객체 자신 (내부) | 클라이언트 (외부) |
| 상태/[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인식 | 상태가 다른 상태를 알 수 있음 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 서로 독립적 |
| 주요 관심사 | 상태에 따른 행동 + 전이 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체 |
| [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | O (핵심) | X |

- **📢 섹션 요약 비유**: [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)은 자판기([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))가 상태(동전 없음·동전 있음·제품 배출)에 따라 자동으로 동작이 바뀌고, [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 사용자가 자판기 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 직접 선택하는 것이다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine(Spring [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine) 프레임워크가 [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)을 선언적으로 구현한다. 주문 처리, 결제 흐름, 워크플로우 엔진에서 상태 머신을 정의하면 복잡한 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 로직을 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 있게 표현할 수 있다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 상태 수가 3개 이상이고 상태에 따른 동작 변경이 복잡한가?
2. 각 상태가 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 인터페이스를 구현하여 Context와 분리되어 있는가?
3. [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 객체 내부에서 결정되어 Context가 전이 규칙을 직접 관리하지 않는가?
4. 새 상태 추가 시 [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 코드를 수정하지 않아도 되는가([OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))?
5. 상태 수가 2~3개의 단순한 경우 패턴 적용이 과도하지 않은지 고려했는가?

- **📢 섹션 요약 비유**: 자판기([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))에 동전 투입·반환·선택 동작을 상태별로 분리하면, 새 상태(유지보수 모드) 추가 시 자판기 기본 로직을 수정할 필요가 없다.

---

## Ⅴ. 기대효과 및 결론

[상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)을 적용하면 상태별 동작이 독립 클래스에 캡슐화되어 코드 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)이 높아지고, 새 상태 추가가 기존 코드 수정 없이 가능해진다. 복잡한 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 로직을 명확하게 표현할 수 있다.

한계는 상태 클래스 수가 많아지고, 상태가 서로를 알아야 하는 경우 결합도가 높아진다. 단순한 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 열거형(Enum) + 전이 테이블로 더 간결하게 구현할 수 있다.

- **📢 섹션 요약 비유**: 신호등이 빨강 상태일 때 '초록을 기억'하고, 초록 상태일 때 '노랑으로 전이'하는 규칙을 각 상태 객체가 책임지는 것이 [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)의 핵심이다.

---

### 📌 관련 개념 맵

[조건 분기 폭발 문제] -> [상태 패턴] -> OCP 달성] -> [스프링 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine] -> [워크플로우 엔진]

| 개념 | 연결 포인트 |
|:---|:---|
| [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) | [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)과 구조 동일, 의도 다름 |
| 유한 상태 기계(FSM) | [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)의 이론적 기반 |
| 스프링 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine | [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)의 프레임워크 구현 |
| 열거형 + 전이 테이블 | 단순한 [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)의 대안 구현 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)(1994)] -> [유한 상태 기계(FSM)] -> [스프링 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine] -> [워크플로우 [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/) 엔진] -> [이벤트 소싱 상태 관리]

### 👶 어린이를 위한 3줄 비유 설명

1. [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)은 신호등처럼, [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(빨강·초록·노랑)에 따라 동작이 달라지는 것이에요.
2. 각 상태가 다음 상태로의 전환 규칙을 스스로 결정해요.
3. 주문 처리 시스템(접수->처리->배송->완료)이 바로 이 패턴을 사용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 258 / 530

<- **이전**: [196. 커맨드 패턴 (Command Pattern)](/studynote/11_design_supervision/04_gof_behavioral/196_command_pattern/)
**다음**: [198. 상태 vs 전략 패턴 비교 (State vs Strategy Pattern)](/studynote/11_design_supervision/04_gof_behavioral/198_state_vs_strategy/) ->

---
