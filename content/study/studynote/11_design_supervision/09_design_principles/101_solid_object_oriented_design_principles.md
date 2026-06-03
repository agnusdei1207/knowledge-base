+++
weight = 101
title = "객체 지향 설계 원칙 (SOLID)"
date = "2026-03-04"
[extra]
categories = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SOLID는 소프트웨어의 구조를 견고하게 유지하기 위해 로버트 C. 마틴 (Robert C. Martin)이 제안한 5가지 객체 지향 설계 ([[322_oop_4_characteristics|OOP]], Object-Oriented Programming) 원칙의 집합이다.
> 2. **가치**: [[192_module_independence|모듈]] 간의 [[195_coupling_levels|결합도]] ([[195_coupling_levels|Coupling]])를 낮추고 [[193_cohesion_levels|응집도]] ([[193_cohesion_levels|Cohesion]])를 높여, 요구사항이 변하더라도 기존 코드를 부수지 않고 안전하게 확장할 수 있는 아키텍처를 제공한다.
> 3. **판단 포인트**: 이 원칙들은 무조건 [[459_quic_fec_forward_error_correction|초기]]부터 강박적으로 적용하기보다는, 코드가 얽히기 시작하거나 변경의 필요성이 대두되는 [[213_refactoring_cloud_native_rearchitecture|리팩토링]] 시점에 점진적으로 적용하는 것이 실용적이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어는 끊임없이 변한다. [[459_quic_fec_forward_error_correction|초기]]에 깔끔했던 코드는 요구사항이 추가됨에 따라 조건문이 덕지덕지 붙고, 하나의 클래스가 수백 가지 일을 처리하는 스파게티 코드로 부패하기 쉽다. 이러한 코드 냄새 ([[365_5_solid_code_smell|Code Smell]])를 방지하고 [[346_maintainability_portability|유지보수성]] ([[346_maintainability_portability|Maintainability]])을 극대화하기 위해 탄생한 철학이 바로 [[242_solid_object_oriented_design_principles|SOLID]] 원칙이다.

SOLID는 5가지 원칙([[243_srp_single_responsibility_principle|SRP]], [[746_ocp|OCP]], [[245_lsp_liskov_substitution_principle|LSP]], [[101_isp_information_strategy_planning_4_steps|ISP]], [[247_dip_dependency_inversion_principle|DIP]])의 앞 글자를 딴 것으로, 각 원칙은 '어디를 분리하고 어떻게 연결할 것인가'에 대한 구체적인 가이드라인을 제공한다. 이 원칙이 무너지면 작은 기능 하나를 수정할 때 시스템 전체에 버그가 퍼지는 경직성 (Rigidity)과 취약성 (Fragility)에 시달리게 되며, 결국 막대한 [[100_technical_debt_monitoring_release_policy|기술 부채]] ([[100_technical_debt_monitoring_release_policy|Technical Debt]])를 짊어지게 된다.

- **📢 섹션 요약 비유**: [[242_solid_object_oriented_design_principles|SOLID]] 원칙은 레고 블록의 표준 규격과 같다. 규격(원칙)이 잘 맞춰져 있으면 기존 블록을 허물지 않고도 새로운 블록을 쉽게 끼울 수 있지만, 본드로 붙여버린 장난감은 팔 하나를 바꾸기 위해 몸통 전체를 부숴야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SOLID의 5가지 원칙은 각각 객체의 책임, 확장, [[234_uml_class_relationships_generalization_dependency|상속]], 인터페이스, 의존성에 대한 명확한 규칙을 정의한다.

```text
┌──────────────────────────────────────────────────────────────┐
│                  [SOLID 5대 원칙의 메커니즘]                   │
├──────────────────────────────────────────────────────────────┤
│ 1. SRP (단일 책임): 클래스가 변경되어야 할 이유는 단 하나뿐이어야 함.  │
│    [User] ──(분리)──▶ [UserAuthenticator], [UserRepository]  │
│                                                              │
│ 2. OCP (개방-폐쇄): 확장에는 열려 있고, 수정에는 닫혀 있어야 함.    │
│    [Payment] ──▶ [interface PayMethod] ◀── [Card], [Cash]    │
│                                                              │
│ 3. LSP (리스코프 치환): 자식은 부모의 역할을 온전히 대체할 수 있어야 함.│
│    [Bird] ◀── [Penguin] (날기 기능 오버라이딩 시 계약 위반 발생)  │
│                                                              │
│ 4. ISP (인터페이스 분리): 클라이언트는 자신이 쓰지 않는 메서드에 의존 X.│
│    [IWorker] ──(분리)──▶ [IEater], [IDuty]                   │
│                                                              │
│ 5. DIP (의존성 역전): 고수준 모듈은 저수준 모듈의 구현체에 의존하면 안 됨.│
│    [Service] ──▶ (Interface) ◀── [Database MySQL]           │
└──────────────────────────────────────────────────────────────┘
```

SRP가 클래스의 덩치를 통제한다면, OCP는 다형성을 이용해 변경 여파를 막는다. LSP는 [[234_uml_class_relationships_generalization_dependency|상속]]의 신뢰성을 보장하고, ISP는 비대한 인터페이스를 잘게 쪼갠다. 마지막으로 DIP는 이 모든 객체가 구체적인 클래스가 아닌 [[198_abstraction_control_data_process|추상화]](인터페이스)에 의존하도록 의존성의 화살표를 뒤집는다.

- **📢 섹션 요약 비유**: SRP는 요리사와 웨이터의 역할을 나누는 것이고, OCP는 새로운 메뉴가 추가되어도 주방 공사를 하지 않는 것이다. DIP는 요리사가 특정 가스레인지 브랜드에 얽매이지 않고 표준 콘센트([[198_abstraction_control_data_process|추상화]])에 연결된 도구라면 무엇이든 쓰는 방식이다.

---

## Ⅲ. 비교 및 연결

[[242_solid_object_oriented_design_principles|SOLID]] 원칙은 GoF (Gang of Four) [[251_design_patterns_gof_overview|디자인 패턴]]과 밀접하게 연결된다. [[251_design_patterns_gof_overview|디자인 패턴]]이 구체적인 '전술'이라면, SOLID는 그 전술이 지향하는 '[[268_strategy_pattern|전략]](목표)'이다.

| 원칙 | 위반 시 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]] | 해결을 위한 연결 패턴 / 기법 |
| :--- | :--- | :--- |
| **[[243_srp_single_responsibility_principle|SRP]]** (단일 책임) | 갓 클래스 (God Class, 만능 객체) | 파사드 ([[263_facade_pattern_simplified_interface|Facade]]), [[264_proxy_pattern_surrogate_access_control|프록시]] ([[264_proxy_pattern_surrogate_access_control|Proxy]]) |
| **[[746_ocp|OCP]]** (개방-폐쇄) | if-else 조건문의 무한 증식 | [[268_strategy_pattern|전략]] ([[268_strategy_pattern|Strategy]]), [[262_decorator_pattern_dynamic_wrapper|데코레이터]] ([[262_decorator_pattern_dynamic_wrapper|Decorator]]) |
| **[[245_lsp_liskov_substitution_principle|LSP]]** (리스코프) | 자식 클래스에서 예외(Exception) 던지기 | [[269_template_method_pattern|템플릿 메서드]] ([[269_template_method_pattern|Template Method]]) |
| **[[101_isp_information_strategy_planning_4_steps|ISP]]** (인터페이스) | 뚱뚱하고 쓸모없는 [[459_dummy_test_double|더미]] 메서드 구현 | [[259_adapter_pattern_interface_wrapper|어댑터]] ([[259_adapter_pattern_interface_wrapper|Adapter]]) |
| **[[247_dip_dependency_inversion_principle|DIP]]** (의존성 역전) | [[192_module_independence|모듈]] 간 강결합으로 인한 테스트 불가 | [[337_dependency_injection|의존성 주입]] ([[190_enterprise_di_framework_lifecycle|DI]], [[337_dependency_injection|Dependency Injection]]) |

최근의 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]]) 설계에서도 이 원칙들이 적용된다. SRP는 각 서비스의 경계([[221_bounded_context_ddd_msa_boundary|Bounded Context]])를 나누는 기준이 되고, DIP는 외부 API와의 통신을 [[198_abstraction_control_data_process|추상화]]하여 장애 격리를 돕는다. 결국 SOLID는 단일 메모리 상의 객체 지향을 넘어, [[136_variance|분산]] 시스템 설계의 근간으로 확장된다.

- **📢 섹션 요약 비유**: [[251_design_patterns_gof_overview|디자인 패턴]]이 목수가 쓰는 톱과 망치(도구)라면, [[242_solid_object_oriented_design_principles|SOLID]] 원칙은 집이 바람에 무너지지 않게 설계하는 무게 중심과 기둥 배치의 역학(이론)이다. 

---

## Ⅳ. 실무 적용 및 기술사 판단

현업에서는 [[242_solid_object_oriented_design_principles|SOLID]] 원칙을 교조적으로 지키려다 오히려 구조가 과도하게 복잡해지는 과엔지니어링 (Over-Engineering)에 빠지기 쉽다.

### [[435_checklist_based_testing|체크리스트]]
1. **변경의 발생**: 코드가 실제로 변경될 확률이 높은가? 한 번 짜고 버릴 스크립트에 OCP를 위한 인터페이스를 도입하는 것은 낭비다. ([[362_yagni|YAGNI]] 원칙 고려)
2. **테스트 용이성**: 현재 클래스에 대한 [[397_unit_test|단위 테스트]] ([[397_unit_test|Unit Test]]) 작성이 어려운가? 모의 객체([[462_mock_test_double|Mock]]) 주입이 힘들다면 [[247_dip_dependency_inversion_principle|DIP]] 원칙을 위반한 강결합 상태인지 확인해야 한다.
3. **[[234_uml_class_relationships_generalization_dependency|상속]]의 오용**: 코드 재사용만을 목적으로 [[234_uml_class_relationships_generalization_dependency|상속]]을 사용했는가? 부모 클래스의 메서드를 자식이 억지로 퇴화시키거나 UnsupportedException을 던진다면 [[245_lsp_liskov_substitution_principle|LSP]] 위반이므로 [[234_uml_class_relationships_generalization_dependency|상속]] 대신 합성(Composition)을 고려해야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 처음부터 있지도 않은 미래의 확장을 대비해 모든 클래스에 무의미한 인터페이스를 1:1로 매핑하는 습관.
- 단일 책임 원칙을 잘못 이해하여 클래스를 메서드 1개 수준으로 잘게 쪼개어 [[501_file_definition_logical_record|파일]] 탐색 비용만 폭증시키는 설계.

- **📢 섹션 요약 비유**: 좋은 도구 상자([[242_solid_object_oriented_design_principles|SOLID]])를 가졌다고 해서, 작은 액자 하나를 걸 때 콘크리트 전동 드릴과 비계를 설치할 필요는 없다. 원칙은 벽에 금이 가기 시작(변경 요구)할 때 꺼내 쓰는 방어구다.

---

## Ⅴ. 기대효과 및 결론

[[242_solid_object_oriented_design_principles|SOLID]] 원칙이 정착된 시스템은 요구사항 변경에 따른 코드 수정 범위가 예측 가능해진다. 독립적인 [[192_module_independence|모듈]] 구성 덕분에 다수의 개발자가 충돌 없이 병렬로 작업할 수 있으며, [[397_unit_test|단위 테스트]]를 촘촘하게 작성할 수 있어 코드의 신뢰성이 급상승한다.

물론 원칙 준수에는 클래스 [[501_file_definition_logical_record|파일]] 증가와 간접 [[316_reference_pattern_nosql|참조]](Indirection)로 인한 [[459_quic_fec_forward_error_correction|초기]] 복잡도 상승이라는 트레이드오프가 따른다. 그러나 시스템의 수명이 길어질수록 [[242_solid_object_oriented_design_principles|SOLID]] 원칙이 방어해 주는 유지보수 비용 절감 효과가 이 단점을 압도한다. 결론적으로 SOLID는 훌륭한 소프트웨어를 만드는 절대적인 법전이 아니라, 변화의 고통을 줄이기 위해 개발자가 지녀야 할 나침반이다.

- **📢 섹션 요약 비유**: 잘 정리된 도서관([[242_solid_object_oriented_design_principles|SOLID]] 적용)은 처음 책을 분류하고 라벨을 붙이는 데 시간이 오래 걸리지만, 나중에 책이 1만 권으로 늘어나도 원하는 책을 1분 만에 찾고 새 책을 꽂을 수 있는 시스템을 만들어준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[251_design_patterns_gof_overview|디자인 패턴]] ([[251_design_patterns_gof_overview|Design Patterns]]) | [[242_solid_object_oriented_design_principles|SOLID]] 원칙을 달성하기 위해 검증된 표준 해결책 (GoF 패턴) |
| [[193_cohesion_levels|응집도]]와 [[195_coupling_levels|결합도]] ([[193_cohesion_levels|Cohesion]] & [[195_coupling_levels|Coupling]]) | SOLID가 궁극적으로 목표로 하는 [[192_module_independence|모듈]]의 품질 지표 |
| [[337_dependency_injection|의존성 주입]] ([[190_enterprise_di_framework_lifecycle|DI]], [[337_dependency_injection|Dependency Injection]]) | [[247_dip_dependency_inversion_principle|DIP]]([[106_dip_dependency_inversion_principle|의존성 역전 원칙]])를 소프트웨어 프레임워크 수준에서 구현하는 기법 |
| [[217_clean_architecture_dependency_rule|클린 아키텍처]] ([[217_clean_architecture_dependency_rule|Clean Architecture]]) | [[242_solid_object_oriented_design_principles|SOLID]] 원칙을 애플리케이션의 계층(Layer) 분리 모델로 확장한 아키텍처 |

### 📈 관련 키워드 및 발전 흐름도

```text
절차적 프로그래밍 · 스파게티 코드 방치
    │
    ▼
객체 지향 프로그래밍 (OOP) · 캡슐화, 상속, 다형성 도입
    │
    ▼
SOLID 설계 원칙 · 유지보수성과 확장성의 체계화
    │
    ▼
디자인 패턴 (GoF) · 원칙에 기반한 정형화된 해결책
    │
    ▼
클린 아키텍처 및 MSA · 분산 시스템과 모듈 경계로의 원칙 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. SOLID는 레고 장난감을 오래오래 튼튼하게 가지고 놀기 위한 5가지 조립 규칙이에요.
2. 각 레고 블록은 하나의 일만 하고([[243_srp_single_responsibility_principle|SRP]]), 새로운 날개를 달고 싶을 때 기존 몸통을 부수지 않아도 되게([[746_ocp|OCP]]) 만들어요.
3. 이 규칙을 잘 지키면 장난감이 아무리 커져도 블록을 쉽게 뺐다 꼈다 하면서 멋지게 업그레이드할 수 있답니다!
