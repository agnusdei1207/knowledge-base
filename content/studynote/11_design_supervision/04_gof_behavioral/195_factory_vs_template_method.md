+++
title = "195. 팩터리 메서드 vs 템플릿 메서드 (Factory Method vs Template Method)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 팩터리 메서드 패턴과 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) 패턴은 모두 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)과 서브클래스 위임을 사용하지만, 팩터리 메서드는 '어떤 객체를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할지'를 서브클래스에 위임하고, [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 '[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 어떤 단계를 어떻게 수행할지'를 서브클래스에 위임하는 것이 핵심 차이다.
> 2. **가치**: 두 패턴의 차이를 이해하면 설계 상황에 맞는 패턴을 선택할 수 있다. 팩터리 메서드는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 관심사, [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 행위 관심사에 적용되며, 종종 함께 사용되어 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 모두 서브클래스에 위임된다.
> 3. **판단 포인트**: 두 패턴이 함께 사용되는 대표 사례는 스프링의 AbstractApplicationContext다. `createBeanFactory()`(팩터리 메서드)로 BeanFactory를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, `refresh()`([템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/))로 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 초기화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 실행한다.

---

## Ⅰ. 개요 및 필요성

두 패턴은 모두 GoF 패턴이며 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)을 기반으로 서브클래스에 결정을 위임한다. 비슷해 보이지만 해결하는 문제가 다르다.

팩터리 메서드의 질문: "어떤 클래스의 인스턴스를 만들어야 하는가?" -> [생성 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/252_creational_patterns_overview/)

[템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)의 질문: "[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 이 단계를 어떻게 수행해야 하는가?" -> [행위 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/)

```text
+-------------------------------------------------------------+
|          팩터리 메서드 vs 템플릿 메서드 비교                 |
+-------------------------------------------------------------+
|  팩터리 메서드                                              |
|  Creator.someOperation() {                                  |
|    Product p = createProduct(); // 팩터리 메서드 (생성)     |
|    p.doSomething();                                         |
|  }                                                          |
|  ConcreteCreator.createProduct() { return new ProductA(); } |
|                                                             |
|  템플릿 메서드                                              |
|  AbstractClass.templateMethod() {  // final                 |
|    step1(); // 공통                                         |
|    step2(); // abstract - 서브클래스 구현 (행위)            |
|  }                                                          |
|  ConcreteClass.step2() { // A만의 행위 구현 }              |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 팩터리 메서드는 '무엇을 만들지'를 결정하는 것이고(요리 재료 선택), [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 '어떻게 만들지'를 결정하는 것이다(조리 방법 선택).

---

## Ⅱ. 아키텍처 및 핵심 원리

두 패턴이 함께 사용되는 예: 스프링의 `AbstractRefreshableApplicationContext`는 `createBeanFactory()`(팩터리 메서드)와 `refresh()`([템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/))를 조합한다. `refresh()`가 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 골격이고, 그 안에서 `createBeanFactory()`가 적절한 BeanFactory를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 위임 대상 | 객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 단계 |
| 패턴 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [생성 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/252_creational_patterns_overview/) | [행위 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/266_behavioral_patterns_overview/) |
| 반환값 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 객체 | (없거나 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 결과) |
| 주요 사용 | 다형적 객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 코드 재사용·[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변형 |

```text
+-------------------------------------------------------------+
|       두 패턴 조합 예시 (AbstractApplicationContext)        |
+-------------------------------------------------------------+
|  AbstractApplicationContext.refresh() { // 템플릿 메서드    |
|    1. createBeanFactory()   <- 팩터리 메서드                 |
|    2. loadBeanDefinitions() <- 추상 메서드 (행위)           |
|    3. invokeBeanFactoryPostProcessors()                     |
|    4. registerBeanPostProcessors()                          |
|    5. finishBeanFactoryInitialization()                     |
|  }                                                          |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 식당(AbstractApplicationContext)이 개장(refresh [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)) 시 주방 도구(BeanFactory, 팩터리 메서드)를 준비하고, 음식 조리법(행위 단계)을 따라 운영을 시작한다.

---
## Ⅲ. 비교 및 연결

두 패턴을 혼동하는 가장 흔한 실수: 팩터리 메서드 패턴을 '단순한 객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 메서드'로 오해하는 것이다. 팩터리 메서드의 핵심은 '서브클래스가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 클래스를 결정한다'는 것이며, [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 없는 static 팩터리 메서드(`LocalDate.of()`)는 다른 패턴이다.

| 비교 축 | A | B |
|:---|:---|:---|
| [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) | O (서브클래스에 위임) | X |
| 다형성 | O | X |
| GoF 패턴 | O | X (명명 관례만) |

- **📢 섹션 요약 비유**: 팩터리 메서드 패턴은 각 지점(서브클래스)이 자신의 특산물(제품)을 결정하는 것이고, static 팩터리는 단순히 물건을 만들어 주는 공장 기계다.

---
## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험에서 두 패턴의 차이를 명확히 서술해야 한다. 핵심 키워드: ① 팩터리 메서드: "[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)", "어떤 클래스의 인스턴스", "Creator-Product 계층", ② [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/): "[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 골격", "공통 흐름", "가변 단계 서브클래스 위임", "[할리우드 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/)".

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 서브클래스에 위임하는 것이 '객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)'[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)? -> 팩터리 메서드
2. 서브클래스에 위임하는 것이 '[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 단계'[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)? -> [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)
3. 두 패턴이 함께 사용될 때 각 메서드의 역할을 명확히 구분할 수 있는가?
4. static 팩터리 메서드를 팩터리 메서드 패턴으로 혼동하지 않는가?
5. 두 패턴이 모두 '[할리우드 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/)'을 구현하는 것을 이해하는가?

- **📢 섹션 요약 비유**: 팩터리 메서드는 '어떤 차종을 생산할지'를 각 공장(서브클래스)이 결정하고, [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 '차 조립 순서'를 본사(상위 클래스)가 정하고 세부 단계를 각 공장이 구현한다.

---

## Ⅴ. 기대효과 및 결론

팩터리 메서드와 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)의 차이를 명확히 이해하면 설계 상황에 맞는 패턴을 선택할 수 있다. 두 패턴은 종종 함께 사용되어 강력한 확장성을 제공하며, 스프링 프레임워크가 이 조합의 대표 사례다.

두 패턴 모두 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 기반이므로, 런타임 교체가 필요하면 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)(구성 기반)을 고려해야 한다. 현대 개발에서는 함수형 인터페이스·람다로 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 없이 유사한 패턴을 구현하는 경향이 있다.

- **📢 섹션 요약 비유**: 두 패턴 모두 '서브클래스야, 네가 결정해([할리우드 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/))'라고 하지만, 하나는 '무엇을 만들지'(팩터리), 다른 하나는 '어떻게 할지'(템플릿)를 결정한다.

---

### 📌 관련 개념 맵

[GoF 패턴 비교] -> [팩터리 메서드([생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/))] vs [템플릿 메서드(행위)] -> [두 패턴 조합(스프링 AbstractApplicationContext)] -> [함수형 대체]

| 개념 | 연결 포인트 |
|:---|:---|
| [할리우드 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/) | 두 패턴 모두 상위 클래스가 서브클래스를 제어 |
| [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) | [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)의 런타임 교체 가능한 대안 |
| 스프링 AbstractApplicationContext | 두 패턴 조합의 대표 사례 |
| static 팩터리 메서드 | 팩터리 메서드 패턴과 구별되는 명명 관례 |

### 📈 관련 키워드 및 발전 흐름도

[GoF 두 패턴 비교] -> [스프링 프레임워크 적용] -> [함수형 인터페이스 대체] -> [콜백 패턴으로 단순화]

### 👶 어린이를 위한 3줄 비유 설명

1. 팩터리 메서드는 '어떤 장난감을 만들지'를 각 공장(서브클래스)이 결정해요.
2. [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 '장난감 만드는 순서'를 본사(상위 클래스)가 정하고, 세부 단계를 공장이 구현해요.
3. 스프링이 두 패턴을 같이 써서 IoC [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 초기화해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 256 / 530

<- **이전**: [194. 템플릿 메서드 패턴 (Template Method Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/194_template_method_pattern/)
**다음**: [196. 커맨드 패턴 (Command Pattern)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/196_command_pattern/) ->

---
