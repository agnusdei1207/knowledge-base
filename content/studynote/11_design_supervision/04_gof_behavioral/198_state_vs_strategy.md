+++
title = "198. 상태 vs 전략 패턴 비교 (State vs Strategy Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))과 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 GoF 행위 패턴으로, 구조가 동일([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) + 인터페이스 + 구체 구현 클래스)하지만 해결하는 문제와 교체 주체가 다르다. [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)은 '상태에 따른 동작 + [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)'를, [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 '교체 가능한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)'을 목적으로 한다.
> 2. **가치**: 두 패턴의 차이를 명확히 이해하면 설계 상황에 맞는 패턴을 선택할 수 있다. [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)은 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 로직이 복잡한 FSM(유한 상태 기계) 구현에, [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 동일한 인터페이스의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 런타임에 교체해야 할 때 적합하다.
> 3. **판단 포인트**: 핵심 판단 기준은 '교체 주체'다. 외부(클라이언트)가 교체 → [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), 내부([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 객체)가 스스로 전이 → [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/). [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 여부가 없으면 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)이 더 적합하다.

---

## Ⅰ. 개요 및 필요성

GoF 패턴 학습에서 가장 많이 혼동되는 두 패턴이다. [UML](/knowledge-base/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/) 클래스 다이어그램이 거의 동일하여 코드만 봐서는 구분이 어렵다. 의도([Intent](/knowledge-base/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/))를 보고 구분해야 한다.

[전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 의도: "[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)군을 정의하고, 각각을 캡슐화하여 교환 가능하게 만든다. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 사용하는 클라이언트와 독립적으로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 변경할 수 있다."

[상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)의 의도: "객체의 내부 상태가 변할 때 객체의 행위를 변경한다. 객체는 클래스를 바꾸는 것처럼 보인다."

```text
┌─────────────────────────────────────────────────────────────┐
│          구조 비교 (UML 거의 동일)                           │
├─────────────────────────────────────────────────────────────┤
│  전략 패턴                  상태 패턴                        │
│  Context                    Context                         │
│  - strategy: Strategy       - state: State                  │
│  + setStrategy(s)           + setState(s)  ← State 내부 호출│
│  + execute()                + request()                     │
│        │ (위임)                   │ (위임)                  │
│   Strategy (인터페이스)      State (인터페이스)              │
│  + algorithm()              + handle(ctx)                   │
│        ▲                          ▲                         │
│  StrategyA  StrategyB       StateA  StateB                  │
│                             (StateA.handle에서 ctx.setState  │
│                              (new StateB()) 호출)            │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 같은 '교체 메커니즘'을 사용하지만, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 요리사가 레시피를 선택(외부 교체), 상태는 신호등이 스스로 다음 상태로 전환(내부 전이)하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

결정적 차이점 정리:

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 교체 주체 | 클라이언트 (외부) | [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 객체 자신 (내부) |
| 인터페이스 상호 인식 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 서로를 모름 | 상태가 다른 상태를 알 수 있음 |
| [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | X | O (핵심 기능) |
| Context의 역할 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 보유·실행 | 상태 보유·위임 |
| 주 관심사 | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체 | 상태에 따른 행동 변경 |
| 클라이언트 인식 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 종류 알아야 함 | [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)를 알 필요 없음 |

```text
┌─────────────────────────────────────────────────────────────┐
│       코드 수준 차이                                         │
├─────────────────────────────────────────────────────────────┤
│  // 전략 패턴: 외부에서 교체                                │
│  context.setStrategy(new FastSortStrategy());               │
│  context.executeStrategy(data);                             │
│                                                             │
│  // 상태 패턴: 내부 전이                                    │
│  // 클라이언트는 상태 전이를 모름                           │
│  order.process(); // 내부에서 상태 전이 발생                │
│  // ReceivedState.process(ctx) {                            │
│  //   ctx.setState(new ProcessingState()); // 내부 전이     │
│  // }                                                       │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 리모컨(클라이언트)이 채널([전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 선택하는 것이고, [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)은 자판기가 내부 상태에 따라 자동으로 모드를 전환하는 것이다.

---
## Ⅲ. 비교 및 연결

두 패턴이 함께 사용되는 경우: [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)의 각 상태가 내부적으로 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)을 사용하여 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 교체할 수 있다. 예: 주문 상태([상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/))에 따라 적용되는 할인 계산 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/))이 다를 수 있다.

| 비교 축 | A | B |
|:---|:---|:---|
| 상태 + [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 각 상태가 다른 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 사용 | 주문 상태별 할인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)만 | 단순 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체 | 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 |
| 상태만 | 복잡한 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | 주문 처리 워크플로우 |

- **📢 섹션 요약 비유**: 게임 캐릭터([상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/): 일반·전투·[회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) 상태)가 각 상태에서 공격 방식([전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/): 원거리·근접·마법)을 바꾸는 것처럼 두 패턴을 조합할 수 있다.

---
## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험에서 두 패턴 비교 문제 풀이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): 핵심 키워드 ① "[상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)"가 있으면 → [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/), ② "[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체"가 있으면 → [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), ③ "외부 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)"이면 → [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), ④ "자동 전환"이면 → [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/).

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 요구사항에 '[상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)'(A 상태에서 B 상태로 자동 변환)가 있는가? → [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)
2. 요구사항에 '[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체'(클라이언트가 선택)가 있는가? → [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)
3. 두 패턴을 혼동할 때 '교체 주체'(내부 vs 외부)로 구분하고 있는가?
4. 두 패턴이 함께 사용될 수 있는 경우를 인식하는가?
5. 구조 다이어그램이 아닌 '의도([Intent](/knowledge-base/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/))'로 패턴을 구분하고 있는가?

- **📢 섹션 요약 비유**: 면접관이 "[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)의 차이?"를 물으면, '교체 주체'(외부 vs 내부)와 '[상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 유무'로 명확히 구분하라.

---

## Ⅴ. 기대효과 및 결론

[상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)과 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 차이를 명확히 이해하면 복잡한 상태 기반 시스템과 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체 시스템을 올바르게 설계할 수 있다. 두 패턴을 혼동하면 의도에 맞지 않는 설계가 되어 유지보수가 어려워진다.

결론: 구조가 같더라도 의도([Intent](/knowledge-base/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/))로 패턴을 구분하라. [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 필요하면 [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/), [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체가 필요하면 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), 상태+[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 모두 필요하면 두 패턴을 조합하라.

- **📢 섹션 요약 비유**: 같은 '채널 변경' 메커니즘이라도, 사용자가 직접 변경([전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))하는 것과 프로그램이 자동으로 변경(상태)하는 것은 다른 설계 의도를 가진다.

---

### 📌 관련 개념 맵

[GoF 패턴 비교] → [전략 패턴(외부 교체)] vs [상태 패턴(내부 전이)] → [두 패턴 조합] → [FSM 프레임워크]

| 개념 | 연결 포인트 |
|:---|:---|
| GoF 의도([Intent](/knowledge-base/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/)) | 구조가 같아도 의도로 패턴 구분 |
| 유한 상태 기계(FSM) | [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)의 이론적 기반 |
| 함수형 패턴 | [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·고차 함수로 두 패턴 간결화 |
| 스프링 [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine | [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)의 프레임워크 구현 |

### 📈 관련 키워드 및 발전 흐름도

[GoF 두 패턴 비교] → [의도 기반 구분 기준] → [두 패턴 조합 설계] → [FSM 프레임워크 적용]

### 👶 어린이를 위한 3줄 비유 설명

1. [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 리모컨처럼 내가 직접 채널([알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))을 바꾸는 것이에요.
2. [상태 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/394_process/)은 신호등처럼 현재 상태에 따라 자동으로 다음 상태로 바뀌는 것이에요.
3. 구조는 같지만 '누가 바꾸는지'(외부 vs 내부)가 핵심 차이예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 259 / 530

← **이전**: [197. 상태 패턴 (State Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/197_state_pattern/)
**다음**: [199. 책임 연쇄 패턴 (Chain of Responsibility Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/199_chain_of_responsibility_pattern/) →

---
