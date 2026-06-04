---
title: "193. 전략 패턴 (Strategy Pattern)"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 GoF 행위 패턴으로, [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)군([Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) Family)을 각각 독립적인 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) 인터페이스의 구현으로 캡슐화하고, [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)([Context](/studynote/02_operating_system/01_overview_architecture/033_context/)) 객체가 런타임에 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 교체할 수 있게 하는 패턴이다.
> 2. **가치**: [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변형마다 서브클래스를 만드는 조건 분기(if-else, [switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) 코드를 제거하고, 런타임에 동적으로 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 교체하여 [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/)([개방-폐쇄 원칙](/studynote/11_design_supervision/06_exam_summary/356_process/))를 달성한다. 정렬 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 결제 방법, 암호화 방식처럼 다양한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 존재하는 도메인에 적합하다.
> 3. **판단 포인트**: [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 두세 가지 이상이고 런타임 교체가 필요할 때 적합하다. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 하나거나 고정된 경우에 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)을 적용하면 불필요한 복잡성이 추가된다. 함수형 언어에서는 [고차 함수](/studynote/04_software_engineering/06_software_architecture/325_higher_order_function_closure/)(First-Class Function)로 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)을 더 간결하게 표현한다.

---

## Ⅰ. 개요 및 필요성

조건 분기로 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 선택하면: `if (type == "credit") { ... } else if (type == "kakao") { ... } else if (type == "toss") { ... }` — 새로운 결제 방법 추가 시 기존 코드를 수정해야 하고([OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) 위반), 조건 분기가 점점 길어진다.

[전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 각 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 독립적인 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 클래스로 캡슐화한다. `PaymentStrategy` 인터페이스를 `CreditCardStrategy`, `KakaoPayStrategy`, `TossPayStrategy`가 구현하고, [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)만 교체하면 된다.

```text
+-------------------------------------------------------------+
|            전략 패턴 구조                                    |
+-------------------------------------------------------------+
|  Context                                                    |
|  - strategy: Strategy                                       |
|  + setStrategy(s: Strategy)                                 |
|  + executeStrategy()                                        |
|       | (위임)                                              |
|       v                                                     |
|  Strategy (인터페이스)                                       |
|  + execute(data): Result                                    |
|       ^                                                     |
|  +----+--------------------------+                          |
|  ConcreteStrategyA   ConcreteStrategyB   ConcreteStrategyC  |
|  (알고리즘 A)       (알고리즘 B)       (알고리즘 C)         |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 내비게이션([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))이 경로 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 교체하듯, '최단 경로', '최소 요금', '고속도로 우선' [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 런타임에 선택한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Java에서 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 함수형 인터페이스와 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)로 더 간결하게 표현된다. `Comparator<T>`가 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 대표 예시로, `sort(list, (a, b) -> a.compareTo(b))` 처럼 정렬 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)로 전달한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 클래스 기반 | implements [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 클래스 | 명시적, 복잡한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에 적합 |
| 익명 클래스 | [new](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)() { ... } | Java 8 이전 방식 |
| [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | ([data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) -> result | 간결, 단순 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에 적합 |
| 메서드 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | ClassName::method | 최간결 |

```text
+-------------------------------------------------------------+
|       스프링에서 전략 패턴 활용                              |
+-------------------------------------------------------------+
|  // 인터페이스 (Strategy)                                   |
|  interface PaymentStrategy {                                |
|    PaymentResult pay(amount: Money);                        |
|  }                                                          |
|                                                             |
|  // 스프링 DI로 전략 주입                                   |
|  @Service class OrderService {                              |
|    OrderService(PaymentStrategy paymentStrategy) { ... }    |
|  }                                                          |
|                                                             |
|  // 런타임 전략 교체: Map<String, PaymentStrategy>로 관리   |
|  paymentStrategies.get(paymentType).pay(amount);            |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 스마트폰([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))이 통신 방식([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))으로 WiFi, [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/), 5G를 런타임에 교체하듯, [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스만 알고 구체 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 모른다.

---
## Ⅲ. 비교 및 연결

[전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)과 [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)은 구조가 동일하지만 의도가 다르다. [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 외부에서 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 교체하고, 상태는 상태 객체 자신이 다음 상태로 전이를 결정한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 교체 주체 | 외부 (클라이언트) | 내부 (상태 객체 자신) |
| 상태 인식 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 서로 독립 | 상태가 다른 상태를 알 수 있음 |
| 의도 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체 | 상태에 따른 동작 변경 |
| 대표 예시 | 정렬 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 결제 방법 | 주문 상태 (접수->처리->완료) |

- **📢 섹션 요약 비유**: [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 요리사([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))가 레시피([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))를 선택하는 것이고, [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)은 신호등([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))이 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(빨강/노랑/초록)에 따라 자동으로 다음 상태로 전이하는 것이다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링에서 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 고급 활용: `Map<String, Strategy>`로 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 맵을 관리하면 if-else 없이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택이 가능하다. `@Qualifier`로 특정 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 주입하거나, `ApplicationContext.getBeansOfType(Strategy.class)`로 동적으로 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 검색한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 두 가지 이상이고 런타임 교체가 필요한가?
2. [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스를 구현하여 Context와 분리되어 있는가?
3. 새로운 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 추가 시 기존 [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 코드를 수정하지 않아도 되는가([OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))?
4. 함수형 인터페이스+[람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)로 단순한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 더 간결하게 표현할 수 있는가?
5. [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)과 [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/)의 의도 차이를 이해하고 올바른 패턴을 선택했는가?

- **📢 섹션 요약 비유**: 결제 시스템([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))이 신용카드·카카오페이·토스페이([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))를 런타임에 교체하듯, 새 결제 방법 추가 시 기존 결제 시스템 코드를 수정하지 않아도 된다.

---

## Ⅴ. 기대효과 및 결론

[전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)을 적용하면 조건 분기 코드가 제거되고, 새 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 추가가 기존 코드 수정 없이 가능해져 OCP를 달성한다. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 독립적으로 테스트·교체·재사용할 수 있어 코드 품질이 향상된다.

한계는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수가 많아지면 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 클래스가 많아지고, 클라이언트가 어떤 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 선택할지 알아야 한다. 함수형 언어에서는 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·[고차 함수](/studynote/04_software_engineering/06_software_architecture/325_higher_order_function_closure/)로 [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 장점을 더 간결하게 달성한다.

- **📢 섹션 요약 비유**: [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 요리책([전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스)에 있는 다양한 레시피(구체 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) 중 하나를 선택하여 요리([알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 실행)하는 방식이다.

---

### 📌 관련 개념 맵

[조건 분기 코드 문제] -> [전략 패턴] -> OCP 달성] -> [함수형 고차 함수] -> [스프링 [DI](/studynote/11_design_supervision/10_patterns_antipatterns/661_enterprise_di_framework_lifecycle/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 주입]

| 개념 | 연결 포인트 |
|:---|:---|
| [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([개방-폐쇄 원칙](/studynote/11_design_supervision/06_exam_summary/356_process/)) | [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)으로 달성하는 핵심 원칙 |
| [상태 패턴](/studynote/11_design_supervision/06_exam_summary/394_process/) | [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)과 구조 동일, 의도 다름 |
| 함수형 인터페이스 | Java 8+ [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)의 간결한 구현 |
| [의존성 주입](/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)에 주입하는 방법 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(1994)] -> OCP 달성] -> [Java 함수형 인터페이스+람다] -> [스프링 [DI](/studynote/11_design_supervision/10_patterns_antipatterns/661_enterprise_di_framework_lifecycle/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 맵] -> [함수형 프로그래밍 [고차 함수](/studynote/04_software_engineering/06_software_architecture/325_higher_order_function_closure/) 대체]

### 👶 어린이를 위한 3줄 비유 설명

1. [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 내비게이션처럼, 최단 경로·최소 요금·고속도로 우선 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 선택하는 것이에요.
2. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)마다 별도 클래스로 만들고, 런타임에 원하는 것을 선택해요.
3. 새 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 추가할 때 기존 코드를 수정하지 않아도 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 254 / 530

<- **이전**: [192. 옵저버 패턴 (Observer Pattern)](/studynote/11_design_supervision/04_gof_behavioral/192_observer_pattern/)
**다음**: [194. 템플릿 메서드 패턴 (Template Method Pattern)](/studynote/11_design_supervision/04_gof_behavioral/194_template_method_pattern/) ->

---
