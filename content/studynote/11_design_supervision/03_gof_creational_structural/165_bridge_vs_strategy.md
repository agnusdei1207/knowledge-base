+++
title = "165. 브리지 vs 전략 패턴 (Bridge vs Strategy Pattern)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [브리지 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/384_bridge_pattern_summary/) ([Bridge Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/153_bridge_pattern/))은 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 구현을 분리해 <strong>두 축이 독립적으로 확장</strong>되게 만들고, [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 캡슐화해 <strong>행동을 교체 가능</strong>하게 만든다.
> 2. **가치**: 두 패턴 모두 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)보다 합성 (Composition)을 택하지만, [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 구조 복잡도를 줄이고 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 조건 분기와 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 결합도를 낮춘다.
> 3. **판단 포인트**: 문제의 핵심이 "추상 계층과 구현 계층의 2차원 확장"이면 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/), "동일 문맥에서 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택"이면 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 보는 것이 가장 실무적이다.

---

## Ⅰ. 개요 및 필요성

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)와 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 클래스 다이어그램만 보면 비슷해 보인다. 둘 다 인터페이스를 두고 구현체를 바꿔 끼우며, 클라이언트는 구체 클래스 대신 추상 타입에 의존한다. 그래서 설계 리뷰에서 자주 혼동되지만, 두 패턴의 출발 질문은 다르다.

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 "[추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 구현이 함께 늘어날 때 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 폭발을 어떻게 막을 것인가"에 답한다. 예를 들어 화면 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 종류와 렌더링 엔진 종류가 동시에 늘어나면 `버튼-OpenGL`, `버튼-DirectX`, `대화상자-OpenGL` 같은 조합 클래스가 급격히 늘어난다. [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 이 두 축을 분리해 각 축이 독립적으로 진화하도록 설계한다.

[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "같은 일을 여러 방법으로 수행해야 할 때 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 어떻게 교체할 것인가"에 답한다. 정렬 방식, 할인 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방식처럼 문맥은 같고 행동만 바뀌는 경우 `if-else`가 커지기 쉽다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 이 분기를 객체로 분리해 런타임 선택을 쉽게 만든다.

- **📢 섹션 요약 비유**: [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 차체와 엔진을 따로 설계해 서로 독립적으로 바꿀 수 있게 만드는 자동차 플랫폼이고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 같은 차에 주행 모드를 [에코](/knowledge-base/studynote/03_network/01_data_communication/031_에코_반향/)·스포츠로 갈아끼우는 기능과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

두 패턴의 차이는 연결 구조보다 <strong>확장 방향</strong>에서 가장 선명하게 드러난다. [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 `Abstraction ↔ Implementor`의 두 계층을 만들고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 `Context -> Strategy`의 한 방향 교체 지점을 만든다.

아래 그림은 왜 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)가 2차원 확장이고 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 1차원 교체인지 보여준다.

```text
+---------------------------- Bridge ----------------------------+
| Abstraction                                                    |
|   +-- RemoteControl                                            |
|   +-- AdvancedRemoteControl                                    |
|            | has-a                                              |
|            v                                                    |
| Implementor                                                    |
|   +-- TV                                                        |
|   +-- Radio                                                     |
| Result: Remote 종류와 Device 종류가 독립 확장                  |
+----------------------------------------------------------------+

+--------------------------- Strategy ---------------------------+
| Context                                                        |
|   +-- PaymentService                                           |
|            | uses                                               |
|            v                                                    |
| Strategy                                                       |
|   +-- CardPaymentStrategy                                      |
|   +-- AccountTransferStrategy                                  |
|   +-- SimplePayStrategy                                        |
| Result: 동일 문맥에서 결제 알고리즘만 교체                     |
+----------------------------------------------------------------+
```

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)에서는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층이 구현 세부사항을 직접 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)하지 않고 구현자 인터페이스에 위임한다. 그래서 `RemoteControl` 계열이 늘어나도 `TV`, `Radio` 계열과 곱셈으로 증가하지 않는다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에서는 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)가 특정 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 품고 있다가 상황에 따라 다른 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 교체한다. 핵심은 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)의 책임은 유지하고, 변하는 계산 방식만 외부 객체로 분리한다는 점이다.

| 항목 | [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ([Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)) | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) |
| :-- | :-- | :-- |
| GoF (Gang of Four) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [구조 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) (Structural Pattern) | [행위 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/) (Behavioral Pattern) |
| 해결 문제 | [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 폭발, 플랫폼 결합 | 조건 분기, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 결합 |
| 확장 방향 | [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) × 구현의 2차원 | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 1차원 교체 |
| 교체 시점 | 설계 시 구조화 + 런타임 교체 가능 | 주로 런타임 교체 |
| 핵심 질문 | "무엇을 분리할 것인가" | "어떤 방식을 선택할 것인가" |

- **📢 섹션 요약 비유**: [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 옷장과 옷걸이 규격을 표준화해 옷 종류와 보관 방식이 따로 늘어나게 하는 설계이고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 오늘 날씨에 맞춰 같은 옷장에서 코트나 우산을 고르는 선택이다.

---

## Ⅲ. 비교 및 연결

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)와 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 모두 [의존성 역전 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/106_dip_dependency_inversion_principle/) ([Dependency Inversion Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/), [DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/))과 [개방-폐쇄 원칙](/knowledge-base/studynote/11_design_supervision/06_exam_summary/356_process/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 실천한다. 그러나 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 "변화 축이 둘 이상"일 때 강하고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "하나의 규칙 집합을 자주 바꿔야 할 때" 강하다. 이 경계를 정확히 잡지 못하면 패턴을 잘못 적용해 오히려 구조가 복잡해진다.

| 시나리오 | 적합한 패턴 | 이유 |
| :-- | :-- | :-- |
| UI [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)와 렌더러를 분리 | [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) | [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 축과 렌더러 축이 독립 증가 |
| [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 종류와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)를 분리 | [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) | 추상 API와 실제 드라이버가 별도 진화 |
| 할인 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 회원 등급별로 교체 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 동일 주문 흐름에서 계산 방식만 다름 |
| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ZIP/GZIP/LZ4 선택 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)는 같고 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만 바뀜 |
| 보고서 형식 PDF/HTML와 출력 장치 조합 | [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) | 표현 형식과 출력 장치의 2차원 조합 |
| 경로 탐색 방식 [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/)/[DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/)/A* 선택 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 탐색 규칙 교체 문제 |

비슷해 보이는 이유는 둘 다 합성 구조를 사용하기 때문이다. 하지만 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 "이 객체가 다른 계층의 구현을 참조한다"는 관계가 오래 유지되고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "상황에 맞는 동작을 골라 쓴다"는 선택성이 중심이다. 즉 같은 합성이라도 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 구조 분리, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 행위 선택에 무게가 있다.

또한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 [템플릿 메서드 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/392_process/) ([Template Method Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/))과 자주 비교되고, [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 [어댑터 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/383_adapter_pattern_summary/) ([Adapter Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/151_adapter_pattern/))과 혼동되기도 한다. [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 기반 변형이고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 합성 기반 교체다. [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 기존 인터페이스 호환이 목적이지만, [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 처음부터 두 계층을 독립적으로 진화시키는 구조 설계가 목적이다.

- **📢 섹션 요약 비유**: [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 아파트 구조와 인테리어 회사를 분리해 각각 따로 고를 수 있게 하는 것이고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 같은 집에서 난방 방식을 전기·[가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/) 중 선택하는 것이다. 겉보기는 비슷해도 바꾸는 축이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 플랫폼 독립 계층을 만들 때 자주 보인다. 예를 들어 JDBC (Java [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) Connectivity)는 애플리케이션 코드가 `Connection` 같은 추상 인터페이스를 사용하고, 실제 벤더 드라이버 구현이 뒤에서 교체된다. ORM (Object-Relational [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) 프레임워크와 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 종류가 함께 늘어나는 환경에서도 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 사고방식이 구조적 안정성을 준다.

[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 결제, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 캐시 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)처럼 런타임 분기가 많은 영역에서 효과적이다. 예를 들어 `AuthenticationStrategy`를 `Password`, `OAuth 2.0`, `SAML (Security Assertion Markup Language)` 방식으로 나누면, [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 서비스는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 절차를 바꾸지 않고도 새로운 방식만 추가할 수 있다. 이는 테스트 분리에도 유리하다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 변화 축이 둘 이상이며 서로 독립적으로 증가하는가? -> [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 우선 검토
2. 동일 문맥에서 규칙·[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만 바꾸면 되는가? -> [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 우선 검토
3. 새로운 경우 추가 시 기존 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)를 수정해야 하는가? -> [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 누락 가능성 점검
4. 조합 클래스 수가 `M × N`으로 늘어나는가? -> [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 필요성 점검

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 하나만 필요한데 계층을 과도하게 쪼개 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)처럼 만드는 설계
- [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층이 구현 세부사항을 다시 직접 알아 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 분리를 무너뜨리는 설계
- [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택 로직이 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 내부 `switch`문으로 남아 있는 반쪽짜리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 설계

- **📢 섹션 요약 비유**: 공구함을 정리할 때, 드릴과 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 규격을 분리해 여러 조합을 만들려는 문제면 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)이고, 같은 드릴에 오늘은 나무용 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/), 내일은 금속용 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 꽂는 문제면 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅴ. 기대효과 및 결론

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)를 잘 쓰면 구조가 장기적으로 버틴다. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 구현이 따로 버전업되므로 플랫폼 변경, 벤더 교체, 기능 확장에 강해진다. 특히 조합이 많은 시스템에서 클래스 폭발을 줄여 설계 복잡도를 통제하는 데 유효하다.

[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 잘 쓰면 코드가 읽히고 테스트되기 쉬워진다. [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)는 안정적으로 유지되고, 다양한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 독립 클래스에서 실험·교체·확장할 수 있다. 이는 기능 확장 속도와 [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/) 품질을 동시에 높인다.

결론적으로 두 패턴은 "[상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대신 합성"이라는 공통 철학을 공유하지만, 기억해야 할 핵심은 의도다. [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 **구조의 두 축을 분리하는 패턴**, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 <strong>행동의 선택지를 교체하는 패턴</strong>으로 이해하면 실전 구분이 훨씬 쉬워진다.

- **📢 섹션 요약 비유**: 좋은 설계자는 부품 창고를 나누어야 할지, 오늘 사용할 공구만 갈아끼우면 될지를 먼저 판단한다. 그 판단이 맞아야 패턴도 맞게 쓴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [브리지 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/384_bridge_pattern_summary/) ([Bridge Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/153_bridge_pattern/)) | [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 구현의 독립 확장을 위한 [구조 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) |
| [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 교체를 위한 대표 [행위 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/) |
| 합성 우선 원칙 (Favor Composition over Inheritance) | 두 패턴 모두 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대신 합성으로 유연성을 얻는다 |
| [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)) | 새 구현·새 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 추가 시 기존 코드 수정을 줄이는 기준 |
| [DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/) ([Dependency Inversion Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/)) | 구체 클래스 대신 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)에 의존하게 만드는 설계 토대 |

### 📈 관련 키워드 및 발전 흐름도

```text
상속 중심 설계
    |
    v
조합 폭발 · 조건 분기 증가
    |
    +-- 구조 분리 필요 ---> 브리지 패턴 (Bridge Pattern)
    |
    +-- 알고리즘 교체 필요 ---> 전략 패턴 (Strategy Pattern)
                                  |
                                  v
합성 우선 설계 · OCP · DIP 강화
```

이 흐름은 같은 합성 기반 설계라도 문제의 초점이 구조 분리인지, 행위 교체인지에 따라 서로 다른 패턴으로 갈라짐을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 장난감 자동차 몸체와 바퀴를 따로 만들어서, 몸체 종류와 바퀴 종류를 마음대로 섞을 수 있게 하는 거예요.
2. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 같은 자동차에 오늘은 빠른 바퀴, 내일은 미끄럼 방지 바퀴를 끼워서 달리는 방법을 바꾸는 거예요.
3. 그래서 [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 "부품 세계를 나누는 방법"이고, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "행동 방법을 바꾸는 방법"이라고 생각하면 쉬워요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 221 / 530

<- **이전**: [164. 어댑터 vs 퍼사드 (Adapter vs Facade)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/164_adapter_vs_facade/)
**다음**: [166. 데코레이터 vs 프록시 (Decorator vs Proxy)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/166_decorator_vs_proxy/) ->

---
