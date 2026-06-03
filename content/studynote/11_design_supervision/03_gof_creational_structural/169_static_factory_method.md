---
title: 169. 정적 팩토리 메서드 (Static Factory Method)
date: '2026-04-21'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] (Static [[254_factory_method_pattern_subclass_creation|Factory Method]])는 [[087_process_state_transition|생성]]자 대신 이름 있는 정적 메서드로 객체를 제공해, [[087_process_state_transition|생성]] 의도와 반환 [[164_policy|정책]]을 외부에 명확히 드러내는 [[087_process_state_transition|생성]] 기법이다.
> 2. **가치**: [[456_caching|캐싱]], 하위 타입 반환, 입력 조건에 따른 구현 선택처럼 [[087_process_state_transition|생성]]자가 하지 못하는 제어를 제공해 [[193_cohesion_levels|응집도]] 높은 API와 느슨한 결합을 만들 수 있다.
> 3. **판단 포인트**: [[087_process_state_transition|생성]] 의미를 이름으로 구분해야 하거나 구현 클래스를 숨겨야 할 때는 유리하지만, 발견성이 낮고 [[234_uml_class_relationships_generalization_dependency|상속]] 확장이 제한될 수 있어 프레임워크 요구사항과 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] (Static [[254_factory_method_pattern_subclass_creation|Factory Method]])는 `new` [[087_process_state_transition|생성]]자 호출 대신 클래스가 제공하는 정적 메서드로 인스턴스를 반환하는 방식이다. [[087_process_state_transition|생성]]자는 문법이 단순하지만 이름을 가질 수 없고, 항상 자신의 타입 인스턴스를 새로 만든다는 제약이 있다. 그래서 같은 시그니처로 서로 다른 의미의 [[087_process_state_transition|생성]]이 필요하거나, 실제 구현을 감추고 인터페이스 타입만 노출하고 싶을 때 표현력이 부족해진다.

예를 들어 `new LocalDate(2026, 4, 21)`보다 `LocalDate.of(2026, 4, 21)`는 "날짜 조립"이라는 의도가 더 잘 보인다. `Boolean.valueOf(true)`는 매번 새 객체를 만들지 않고 이미 있는 인스턴스를 재사용할 수 있다. 즉 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 단순 문법 취향이 아니라, **[[087_process_state_transition|생성]] 책임을 설계적으로 통제하려는 선택**에서 등장했다.

- **📢 섹션 요약 비유**: 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 손님이 주방에 직접 들어가 요리하지 않고, 메뉴 이름을 보고 주문해 주방이 가장 알맞은 요리를 내주는 식당 주문창구와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]의 핵심은 "객체 [[087_process_state_transition|생성]]"을 하나의 [[164_policy|정책]] 함수로 다루는 데 있다. 호출자는 무엇을 원한다고 말하고, 클래스는 새 객체를 만들지, 캐시를 돌려줄지, 하위 구현체를 선택할지 결정한다. 이 덕분에 클라이언트는 [[087_process_state_transition|생성]] 세부사항보다 **의도와 계약**에 집중할 수 있다.

다음 그림은 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]가 [[087_process_state_transition|생성]] [[164_policy|정책]]을 감싸는 구조를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│        Static Factory Method: 생성 요청과 실제 생성 정책을 분리      │
├──────────────────────────────────────────────────────────────────────┤
│ Client                                                               │
│   │ create / of / from / valueOf                                     │
│   ▼                                                                  │
│ Static Factory Method                                                 │
│   ├─ 입력 검증                                                       │
│   ├─ 캐시 조회                                                       │
│   ├─ 구현 클래스 선택                                                │
│   └─ 새 객체 생성 또는 기존 객체 반환                                │
│            │                                                         │
│            ├─▶ Interface Type 반환                                   │
│            └─▶ Concrete Subtype 은닉                                 │
└──────────────────────────────────────────────────────────────────────┘
```

대표적인 설계 효과는 아래와 같다.

| 핵심 원리 | 설명 | 실무적 의미 |
| :--- | :--- | :--- |
| 이름 있는 [[087_process_state_transition|생성]] | `of`, `from`, `parse`, `valueOf`처럼 의미를 이름에 담음 | 같은 파라미터라도 [[087_process_state_transition|생성]] 의도를 분리 가능 |
| 인스턴스 통제 | 싱글턴, 캐시, [[285_pooling_layer|풀링]] 구현 가능 | 메모리 절감, 객체 동일성 제어 |
| 반환 타입 [[198_abstraction_control_data_process|추상화]] | 인터페이스나 하위 타입 반환 가능 | 구현 교체가 쉬워지고 [[746_ocp|OCP]] ([[244_ocp_open_closed_principle|Open-Closed Principle]])에 유리 |
| 전처리/[[395_verification_process_review|검증]] 일원화 | null [[395_verification_process_review|검증]], 범위 [[395_verification_process_review|검증]], [[093_normalization|정규화]] 수행 | [[087_process_state_transition|생성]] 규칙이 흩어지지 않음 |

자주 쓰는 네이밍도 설계 의도를 드러낸다.

| 이름 패턴 | 의미 | 예시 |
| :--- | :--- | :--- |
| `of` | 여러 값을 조합해 [[087_process_state_transition|생성]] | `LocalDate.of(2026, 4, 21)` |
| `from` | 다른 타입에서 변환 | `Date.from(instant)` |
| `valueOf` | 값을 대응 객체로 매핑 | `Boolean.valueOf(true)` |
| `getInstance` | 조건에 맞는 기존 인스턴스 반환 가능 | `Calendar.getInstance()` |
| `newInstance` / `create` | 새 객체 [[087_process_state_transition|생성]]을 강조 | `Array.newInstance(type, len)` |

- **📢 섹션 요약 비유**: 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 단순 출입문이 아니라, 손님의 주문 내용을 보고 좌석 배정·재고 [[396_validation|확인]]·요리 선택까지 처리하는 프런트 데스크와 같다.

---

## Ⅲ. 비교 및 연결

정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 자주 "[[087_process_state_transition|생성]]자 대체 수단"으로 소개되지만, 실제로는 **[[087_process_state_transition|생성]]자**, **정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]**, **GoF [[378_factory_method_summary|팩토리 메서드 패턴]] ([[146_factory_method_pattern|Factory Method Pattern]])**을 구분해서 봐야 한다. [[087_process_state_transition|생성]]자는 언어 문법이고, 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 클래스 내부의 [[087_process_state_transition|생성]] 관용구이며, GoF [[378_factory_method_summary|팩토리 메서드 패턴]]은 [[234_uml_class_relationships_generalization_dependency|상속]]을 통해 [[087_process_state_transition|생성]] 책임을 하위 클래스로 미루는 패턴이다.

| 구분 | [[087_process_state_transition|생성]]자 | 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] | GoF [[378_factory_method_summary|팩토리 메서드 패턴]] |
| :--- | :--- | :--- | :--- |
| [[087_process_state_transition|생성]] 주체 | 클래스 문법 | 클래스의 정적 메서드 | 상위 클래스 + 하위 클래스 |
| 이름 부여 | 불가 | 가능 | 가능 |
| 반환 타입 유연성 | 낮음 | 높음 | 높음 |
| [[234_uml_class_relationships_generalization_dependency|상속]] 활용 | 직접 `super()` 호출 | 정적이라 오버라이드 불가 | 하위 클래스 오버라이드 핵심 |
| 주 용도 | 단순 [[087_process_state_transition|생성]] | [[087_process_state_transition|생성]] [[164_policy|정책]] 통제 | 제품군 확장 |

트레이드오프도 분명하다. 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 구현 은닉과 [[014_api_posix|API]] 표현력에 유리하지만, IDE 자동완성에서 [[087_process_state_transition|생성]]자만큼 눈에 잘 띄지 않는다. 또한 [[087_process_state_transition|생성]]자를 `private`으로 닫아 버리면 [[234_uml_class_relationships_generalization_dependency|상속]] 기반 확장이 어려워진다. 따라서 [[336_library_vs_framework|라이브러리]] 설계에서는 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]가 강력하지만, 프레임워크가 기본 [[087_process_state_transition|생성]]자나 리플렉션 기반 [[087_process_state_transition|생성]]을 요구한다면 [[087_process_state_transition|생성]]자 공개가 더 현실적일 수 있다.

- **📢 섹션 요약 비유**: [[087_process_state_transition|생성]]자는 누구나 바로 문을 열고 들어가는 일반 출입문이고, 정적 팩토리는 안내 데스크가 있는 전용 입구이며, GoF [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 지점마다 다른 매니저가 손님을 맞는 체인점 운영 방식과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]가 특히 "구현 은닉"과 "[[087_process_state_transition|생성]] 규칙 통합"에서 힘을 발휘한다. 예를 들어 결제 클라이언트를 만드는 API를 설계할 때 `PaymentClient.of(region, mode)`처럼 제공하면, 내부적으로는 `HttpPaymentClient`, `GrpcPaymentClient`, `SandboxPaymentClient` 중 무엇을 쓸지 [[336_library_vs_framework|라이브러리]]가 결정할 수 있다. 사용자는 인터페이스만 의존하고 구현 변경의 파급을 줄일 수 있다.

다음 체크리스트는 설계 판단 시 유용하다.

1. **이름이 필요한가**: 같은 파라미터 타입으로 여러 [[087_process_state_transition|생성]] 의미가 존재하면 정적 팩토리가 유리하다.
2. **반환 구현을 숨겨야 하는가**: 인터페이스 기반 API면 정적 팩토리가 적합하다.
3. **재사용 [[164_policy|정책]]이 있는가**: 불변 객체, 캐시 객체, [[285_pooling_layer|풀링]] 객체는 정적 팩토리가 효과적이다.
4. **프레임워크 제약이 있는가**: 직렬화, [[264_proxy_pattern_surrogate_access_control|프록시]], [[337_dependency_injection|의존성 주입]] ([[337_dependency_injection|Dependency Injection]], [[190_enterprise_di_framework_lifecycle|DI]]) 도구가 기본 [[087_process_state_transition|생성]]자를 요구하면 [[087_process_state_transition|생성]]자와 병행 공개를 고려한다.

반면 다음 안티패턴은 피해야 한다.

- `create1`, `create2`, `createFast`처럼 의미 없는 이름 남발
- 숨겨진 네트워크 호출이나 무거운 초기화를 가벼운 [[087_process_state_transition|생성]] 메서드처럼 보이게 만드는 설계
- [[234_uml_class_relationships_generalization_dependency|상속]]이 필요한 도메인인데 [[087_process_state_transition|생성]]자를 모두 막아 확장을 불가능하게 만드는 설계

- **📢 섹션 요약 비유**: 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 좋은 매표소면 줄을 줄여 주지만, 이름 없는 표를 여러 장 찍어내면 오히려 어떤 문으로 들어가야 하는지 더 헷갈리게 만든다.

---

## Ⅴ. 기대효과 및 결론

정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 API를 더 읽기 쉽게 만들고, 구현 은닉과 객체 수명 제어를 통해 유지보수성을 높인다. 불변 객체 [[456_caching|캐싱]], [[090_service_kubernetes_network_load_balancing|서비스]] 제공자 프레임워크 ([[535_sp_service_provider|Service Provider]] Framework), 인터페이스 반환 API처럼 확장성과 성능을 함께 고려해야 하는 설계에서 특히 효과적이다. 또한 [[087_process_state_transition|생성]] 규칙을 한곳에 모아 두기 때문에 [[601_input_validation|입력 검증]], 로깅, 모니터링 [[164_policy|정책]]을 일관되게 적용하기 쉽다.

하지만 발견성이 낮고 [[234_uml_class_relationships_generalization_dependency|상속]] 친화성이 떨어질 수 있다는 한계는 남는다. 따라서 이 기법은 "[[087_process_state_transition|생성]]자를 모두 없애는 정답"이 아니라, [[087_process_state_transition|생성]] 의미를 설계적으로 통제해야 할 때 선택하는 도구로 기억해야 한다. 한마디로 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 **객체 [[087_process_state_transition|생성]] 문법을 비즈니스 의미와 설계 [[164_policy|정책]]으로 끌어올리는 방법**이다.

- **📢 섹션 요약 비유**: 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 재료를 직접 꺼내 조립하는 공구함이 아니라, 필요한 목적을 말하면 가장 알맞은 제품을 건네주는 전문 상담 매장과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[087_process_state_transition|생성]]자 (Constructor) | 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]가 대체하거나 보완하는 기본 [[087_process_state_transition|생성]] 메커니즘 |
| 싱글턴 ([[253_singleton_pattern_single_instance|Singleton]]) | `getInstance()` 계열의 대표 활용 사례 |
| [[265_flyweight_pattern_instance_sharing|플라이웨이트]] ([[265_flyweight_pattern_instance_sharing|Flyweight]]) | 동일한 불변 객체를 [[456_caching|캐싱]]해 재사용하는 인스턴스 통제 [[268_strategy_pattern|전략]] |
| [[090_service_kubernetes_network_load_balancing|서비스]] 제공자 프레임워크 ([[535_sp_service_provider|Service Provider]] Framework) | 런타임에 구현체를 바꾸며 인터페이스로 노출하는 확장 방식 |
| [[146_factory_method_pattern|Factory Method Pattern]] | 이름은 비슷하지만 [[234_uml_class_relationships_generalization_dependency|상속]] 기반 [[087_process_state_transition|생성]] 확장을 다루는 GoF 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
생성자 (Constructor)의 한계
        │
        ▼
정적 팩토리 메서드 (Static Factory Method)
        │
        ├─▶ 캐싱 / 싱글턴 / 플라이웨이트
        │
        ├─▶ 인터페이스 반환 / 구현 은닉
        │
        └─▶ 서비스 제공자 프레임워크 / 확장형 API 설계
```

이 흐름은 "단순 [[087_process_state_transition|생성]]"에서 출발해 "[[087_process_state_transition|생성]] [[164_policy|정책]] 통제"와 "구현 은닉"으로 설계 관심사가 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 정적 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 장난감을 직접 만들지 않고, 원하는 이름을 말하면 가게가 알맞은 장난감을 꺼내 주는 거예요.
2. 같은 장난감이 이미 있으면 새로 만들지 않고, 있는 것을 다시 줄 수도 있어요.
3. 그래서 우리는 만드는 방법보다 "무엇을 원하느냐"에 더 집중할 수 있어요.
