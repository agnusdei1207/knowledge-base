+++
weight = 172
title = "172. 빌더 패턴을 활용한 불변 객체 (Immutable Object) 설계"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[380_builder_pattern_summary|빌더 패턴]] ([[148_builder_pattern|Builder Pattern]])은 객체 [[087_process_state_transition|생성]] 과정에서만 허용할 상태 변경을 [[256_builder_pattern_step_by_step_creation|Builder]] 안에 가두고, `build()` 시점에 완성된 불변 객체 ([[298_immutable|Immutable]] Object)를 반환하는 [[087_process_state_transition|생성]] 패턴이다.
> 2. **가치**: 텔레스코핑 [[087_process_state_transition|생성]]자 (Telescoping Constructor)의 [[333_readability_vs_efficiency|가독성]] 문제와 자바빈즈 (JavaBeans)의 불완전 상태 노출 문제를 동시에 줄여, 복잡한 [[064_relation_domain|도메인]] 객체를 읽기 쉽고 안전하게 만든다.
> 3. **판단 포인트**: 필수·선택 필드가 섞여 있거나, 필드 간 [[395_verification_process_review|검증]] 규칙이 있거나, 멀티스레드 공유가 필요한 경우에는 [[256_builder_pattern_step_by_step_creation|빌더]] + 불변 객체 조합이 강력하지만, 단순 값 객체에는 과설계가 될 수 있다.

---

## Ⅰ. 개요 및 필요성

불변 객체는 [[087_process_state_transition|생성]] 이후 내부 상태가 바뀌지 않는 객체다. 한 번 만들어진 뒤 값이 흔들리지 않기 때문에, [[092_thread_lwp|스레드]] 안전성 ([[092_thread_lwp|Thread]] Safety), 예측 가능성, 캐시 재사용성 측면에서 매우 유리하다. 문제는 현실의 객체가 종종 필수 필드와 선택 필드, 그리고 "이 값이 있으면 저 값도 있어야 한다" 같은 규칙을 함께 가진다는 점이다.

이때 [[087_process_state_transition|생성]]자만으로 해결하려 하면 파라미터가 길게 늘어선다. 반대로 기본 [[087_process_state_transition|생성]]자와 setter를 열어 두면, 객체가 완성되기 전 중간 상태가 외부에 드러난다. 즉 불변 객체를 원하지만, [[087_process_state_transition|생성]] 과정 자체는 어느 정도 가변적일 수밖에 없는 딜레마가 생긴다. [[380_builder_pattern_summary|빌더 패턴]]은 이 "[[087_process_state_transition|생성]] 중의 가변성"과 "[[087_process_state_transition|생성]] 후의 불변성"을 분리해서 다루려는 해법이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Why Builder is needed                                                │
├───────────────────────────────┬──────────────────────────────────────┤
│ Constructor only              │ Setters / JavaBeans                  │
│ - parameter order confusion   │ - incomplete state can leak          │
│ - optional fields awkward     │ - mutation remains open              │
├───────────────────────────────┴──────────────────────────────────────┤
│ Builder = mutate only during construction, freeze after build        │
└──────────────────────────────────────────────────────────────────────┘
```

즉 [[256_builder_pattern_step_by_step_creation|빌더]]는 객체 [[087_process_state_transition|생성]]을 "여러 번 바꾸는 행위"가 아니라 "완성 전 설계 단계"로 격리한다. 그 덕분에 최종 객체는 불변성을 유지하면서도, [[087_process_state_transition|생성]] 과정은 읽기 쉬운 단계형 인터페이스를 가질 수 있다.

- **📢 섹션 요약 비유**: 집을 짓는 동안에는 벽 위치를 바꾸고 창문을 더 달 수 있지만, 준공 검사 후 입주가 시작되면 함부로 구조를 뜯어고치면 안 된다. [[256_builder_pattern_step_by_step_creation|빌더]]는 공사 기간의 변경을 공사장 안에만 가두는 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[256_builder_pattern_step_by_step_creation|빌더]] 기반 불변 객체 설계의 핵심은 "가변 상태를 어디까지 허용할 것인가"를 명확히 자르는 데 있다. Builder는 내부적으로 필드를 변경하며 입력을 수집하지만, 최종 객체는 `private final` 필드만 가지며 setter를 노출하지 않는다. 그리고 `build()` 시점에 필수값 [[395_verification_process_review|검증]], 범위 [[395_verification_process_review|검증]], 상호 의존 규칙 [[395_verification_process_review|검증]], 방어적 복사 (Defensive Copy)를 한 번에 수행한다.

| 단계 | Builder의 역할 | 최종 객체의 역할 |
| :--- | :--- | :--- |
| 입력 수집 | 선택 필드·기본값·메서드 체이닝 처리 | 없음 |
| 유효성 [[395_verification_process_review|검증]] | `build()`에서 필수값 및 조합 규칙 [[396_validation|확인]] | 이미 [[395_verification_process_review|검증]] 완료된 상태만 유지 |
| 컬렉션 처리 | 임시 mutable 컬렉션 보관 가능 | `List.copyOf()` 등으로 불변 복사 |
| 상태 변경 | [[087_process_state_transition|생성]] 중에만 허용 | [[087_process_state_transition|생성]] 후 금지 |

아래 그림은 Builder와 [[298_immutable|Immutable]] Object의 경계를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Builder lifecycle                                                    │
├──────────────────────────────────────────────────────────────────────┤
│ Client                                                               │
│   │                                                                  │
│   ▼                                                                  │
│ Builder (mutable, defaults, step-by-step input)                      │
│   │                                                                  │
│   ├─ validate required fields                                        │
│   ├─ validate cross-field rules                                      │
│   ├─ defensive copy collections                                      │
│   ▼                                                                  │
│ build()                                                              │
│   │                                                                  │
│   ▼                                                                  │
│ Immutable Object (final fields, no setters, safe sharing)            │
└──────────────────────────────────────────────────────────────────────┘
```

예를 들어 [[009_config|설정]] 객체가 `host`, `port`는 필수이고 `timeout`, `sslEnabled`, `allowedIps`는 선택이라고 하자. [[087_process_state_transition|생성]]자만 쓰면 순서 기억이 어렵고, setter를 쓰면 `host` 없이 `build()` 이전 상태가 떠돌 수 있다. 반면 Builder는 `new Config.Builder("api.example.com", 443).timeout(...).sslEnabled(true).build()`처럼 읽기 쉽고, `build()`에서 `port > 0`, `sslEnabled`일 때 인증서 경로 필요 같은 규칙을 강제할 수 있다.

핵심은 [[256_builder_pattern_step_by_step_creation|빌더]]가 final 객체의 "우회 setter"가 아니라는 점이다. [[256_builder_pattern_step_by_step_creation|빌더]]는 최종 객체와 생명주기가 다르며, build 이후에는 폐기되는 임시 조립 도구여야 한다.

- **📢 섹션 요약 비유**: 요리할 때는 재료를 더 넣고 빼며 간을 맞추지만, 완성된 도시락을 밀봉하고 나면 안의 구성은 더 이상 바뀌지 않는다. [[256_builder_pattern_step_by_step_creation|빌더]]는 조리대이고, 불변 객체는 포장 완료된 도시락이다.

---

## Ⅲ. 비교 및 연결

[[380_builder_pattern_summary|빌더 패턴]]의 의미는 다른 [[087_process_state_transition|생성]] 방식과 비교할 때 더 또렷해진다. 같은 객체 [[087_process_state_transition|생성]]이라도 어떤 방식은 읽기 쉽지만 안전하지 않고, 어떤 방식은 안전하지만 유연하지 않다.

| 방식 | [[333_readability_vs_efficiency|가독성]] | 불변성 | [[395_verification_process_review|검증]] 시점 | 주된 약점 |
| :--- | :--- | :--- | :--- | :--- |
| 텔레스코핑 [[087_process_state_transition|생성]]자 | 낮음 | 가능 | [[087_process_state_transition|생성]]자 내부 | 파라미터 순서 혼동, [[323_overloading_vs_overriding|오버로딩]] 폭증 |
| 자바빈즈 (JavaBeans) | 높음 | 어려움 | 호출자 책임 | 중간 상태 노출, [[092_thread_lwp|스레드]] 불안정 |
| [[380_builder_pattern_summary|빌더 패턴]] | 높음 | 가능 | `build()` 일괄 [[395_verification_process_review|검증]] | 추가 클래스와 코드량 |
| `record` | 매우 높음 | 가능 | compact constructor | 선택 필드와 복잡 규칙 표현 한계 |

또한 [[256_builder_pattern_step_by_step_creation|빌더]]는 단독 패턴이 아니라 다른 설계 개념과 자주 연결된다. 메서드 체이닝을 이용하므로 플루언트 인터페이스 (Fluent Interface) 스타일과 잘 맞고, 최종 산출물이 값 객체 (Value Object)나 [[009_config|설정]] 객체일 때 특히 효과적이다. 반면 팩터리 메서드 ([[254_factory_method_pattern_subclass_creation|Factory Method]])는 객체 선택 로직에 강하고, [[256_builder_pattern_step_by_step_creation|빌더]]는 **객체 조립 과정과 불변성 확보**에 강하다.

실무에서는 `record`와 자주 비교된다. 모든 필드가 필수이고 구조가 단순하면 `record`가 더 간결할 수 있다. 하지만 선택 필드가 많거나 컬렉션 방어적 복사, 필드 간 제약 조건, 조건부 기본값이 필요한 순간에는 [[256_builder_pattern_step_by_step_creation|빌더]]가 더 자연스럽다.

- **📢 섹션 요약 비유**: [[087_process_state_transition|생성]]자는 미리 정해진 세트 메뉴 주문이고, 자바빈즈는 주문 후에도 재료를 계속 바꾸는 방식이다. [[256_builder_pattern_step_by_step_creation|빌더]]는 주문서를 보며 하나씩 체크한 뒤, 최종 [[396_validation|확인]] 후 주방이 봉인해서 내보내는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[256_builder_pattern_step_by_step_creation|빌더]]를 쓸지 말지는 객체의 복잡도와 불변성 요구를 함께 봐야 한다. 단순한 [[001_dikw_pyramid|데이터]] 전달 객체 (DTO, [[001_dikw_pyramid|Data]] Transfer Object) 하나에 필드 2~3개만 있다면 [[087_process_state_transition|생성]]자나 `record`가 더 낫다. 하지만 [[009_config|설정]] 객체, [[064_relation_domain|도메인]] [[164_policy|정책]] 객체, [[014_api_posix|API]] 요청 모델처럼 선택값과 제약 조건이 많아질수록 [[256_builder_pattern_step_by_step_creation|빌더]]의 장점이 커진다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. [[087_process_state_transition|생성]]자 파라미터가 4개 이상이거나 같은 타입이 반복되어 순서 실수가 발생하는가?
2. 필수 필드와 선택 필드가 명확히 구분되는가?
3. 컬렉션, 날짜, 배열처럼 mutable 객체를 안전하게 복사해야 하는가?
4. 멀티스레드 환경에서 같은 객체를 공유하거나 캐시할 계획이 있는가?
5. "A가 있으면 B도 필요" 같은 [[250_cross_validation_kfold|교차 검증]] 규칙을 [[087_process_state_transition|생성]] 시점에 보장해야 하는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Builder를 여러 [[092_thread_lwp|스레드]]에서 재사용해 임시 상태가 섞이는 것
- `build()` 후에도 내부 컬렉션 참조를 그대로 노출해 사실상 mutable 객체가 되는 것
- 단순 값 객체까지 무조건 Builder로 감싸 코드량만 늘리는 것
- [[395_verification_process_review|검증]]을 [[256_builder_pattern_step_by_step_creation|Builder]] 밖 [[090_service_kubernetes_network_load_balancing|서비스]] 계층으로 미뤄, "완성되었지만 유효하지 않은 객체"를 허용하는 것

### 기술사적 판단 포인트

| 상황 | 권장 선택 |
| :--- | :--- |
| 필수값만 2~3개, 규칙 단순 | [[087_process_state_transition|생성]]자 또는 `record` |
| 선택값 많음, 읽기 쉬운 [[087_process_state_transition|생성]] 필요 | [[380_builder_pattern_summary|빌더 패턴]] |
| 불변 객체 + 방어적 복사 필요 | [[256_builder_pattern_step_by_step_creation|빌더]] + final 필드 |
| 객체 [[087_process_state_transition|생성]] 분기 자체가 중요 | 팩터리 메서드와 병행 검토 |

기술사 답안에서는 [[256_builder_pattern_step_by_step_creation|빌더]]를 단순 문법 편의로 쓰기보다, **상태 변이 로직을 [[087_process_state_transition|생성]] 단계로 한정하고 최종 객체의 불변성을 확보하는 설계 원리**로 설명하는 편이 좋다. 그래야 멀티스레드 안전성, [[395_verification_process_review|검증]] 시점, 유지보수성까지 함께 연결된다.

- **📢 섹션 요약 비유**: 자동차는 조립 라인에서는 볼트를 조이고 옵션을 추가하지만, 출고 검사 후에는 봉인된 제품이 된다. [[256_builder_pattern_step_by_step_creation|빌더]]는 조립 라인이고, 불변 객체는 출고 완료 차량이다.

---

## Ⅴ. 기대효과 및 결론

[[380_builder_pattern_summary|빌더 패턴]]과 불변 객체를 함께 쓰면 코드 [[333_readability_vs_efficiency|가독성]], 상태 [[194_consistency_database_integrity|일관성]], [[014_concurrency|동시성]] 안전성을 동시에 얻기 쉽다. 호출부는 메서드 이름 덕분에 의도가 드러나고, 객체 내부는 final 필드와 [[395_verification_process_review|검증]] 완료 상태 덕분에 안정적이다. 특히 [[009_config|설정]] 객체나 [[164_policy|정책]] 객체처럼 한번 만들고 오래 참조하는 구조에서 효과가 크다.

반면 비용도 있다. 별도 [[256_builder_pattern_step_by_step_creation|Builder]] 코드가 필요하고, 작은 객체에 남용하면 구조가 과해질 수 있다. 따라서 기억해야 할 핵심은 "무조건 [[256_builder_pattern_step_by_step_creation|Builder]]"가 아니라, **복잡한 [[087_process_state_transition|생성]] 과정의 가변성을 [[256_builder_pattern_step_by_step_creation|Builder]] 안에 가두고 최종 객체는 불변으로 잠그는 것**이다.

- **📢 섹션 요약 비유**: 설계도와 공사장을 분리하면 건물이 완성된 뒤에는 더 이상 매일 벽이 움직이지 않는다. [[380_builder_pattern_summary|빌더 패턴]]도 객체의 공사 기간과 사용 기간을 분리해, 완성 후 흔들리지 않는 구조를 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 불변 객체 ([[298_immutable|Immutable]] Object) | [[256_builder_pattern_step_by_step_creation|빌더]]가 최종적으로 만들어 내는 목표 산출물 |
| 텔레스코핑 [[087_process_state_transition|생성]]자 | [[256_builder_pattern_step_by_step_creation|빌더]]가 해결하려는 대표 [[087_process_state_transition|생성]]자 [[128_water_scrum_fall_anti_pattern|안티패턴]] |
| 자바빈즈 (JavaBeans) | 읽기 쉽지만 중간 상태 노출 위험이 있는 비교 대상 |
| 플루언트 인터페이스 (Fluent Interface) | [[256_builder_pattern_step_by_step_creation|빌더]] 메서드 체이닝을 설명하는 [[014_api_posix|API]] 스타일 |
| 방어적 복사 (Defensive Copy) | 불변성 유지를 위해 컬렉션·배열을 복사하는 기법 |
| `record` | 단순 불변 [[001_dikw_pyramid|데이터]] 구조의 언어 차원 대안 |
| 값 객체 (Value Object) | [[256_builder_pattern_step_by_step_creation|빌더]] + 불변 객체 조합이 특히 잘 맞는 설계 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
Simple constructor
        │
        ▼
Optional fields increase
        │
        ▼
Builder Pattern
        │
        ▼
Validation at build()
        │
        ▼
Immutable Object + defensive copy
        │
        ▼
Safe sharing / readable construction / domain consistency
```

이 흐름은 객체 [[087_process_state_transition|생성]] 요구가 복잡해질수록 [[256_builder_pattern_step_by_step_creation|빌더]]가 단순 편의가 아니라 불변성 확보 도구로 발전한다는 점을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[256_builder_pattern_step_by_step_creation|빌더]]는 장난감을 조립하는 작업판이라서, 만들 때는 부품을 붙였다 떼었다 할 수 있어요.
2. 다 만들고 나면 본드로 딱 붙여서 더 이상 모양이 바뀌지 않는 불변 장난감이 돼요.
3. 그래서 친구들이 같이 가지고 놀아도 누가 몰래 부품을 바꿔 버릴 걱정을 덜 수 있어요.
