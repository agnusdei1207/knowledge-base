---
title: 163. 싱글톤 패턴의 단점과 DI (Singleton Drawbacks & Dependency Injection)
date: '2026-04-21'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[382_singleton_summary|싱글톤 패턴]] ([[144_singleton_pattern|Singleton Pattern]])은 인스턴스를 하나만 두고 전역 접근점을 제공하는 기법이지만, 그 편의성 때문에 전역 상태 (Global [[272_state_pattern|State]])와 숨겨진 결합 (Hidden [[195_coupling_levels|Coupling]])을 만들기 쉽다.
> 2. **가치**: [[190_enterprise_di_framework_lifecycle|DI]] ([[337_dependency_injection|Dependency Injection]], [[337_dependency_injection|의존성 주입]])와 IoC (Inversion of Control, 제어 역전) [[561_container_based_deployment|컨테이너]]는 "하나만 쓴다"는 운영상의 요구는 유지하면서도, [[087_process_state_transition|생성]] 책임과 사용 책임을 분리해 테스트성과 유지보수성을 높인다.
> 3. **판단 포인트**: 전통적인 `getInstance()` 방식은 변경 가능한 상태, 외부 자원, 테스트 대체가 필요한 객체에 특히 취약하므로, [[561_container_based_deployment|컨테이너]] 관리형 [[253_singleton_pattern_single_instance|Singleton]] 스코프나 명시적 [[087_process_state_transition|생성]]자 주입으로 전환하는 판단이 중요하다.

---

## Ⅰ. 개요 및 필요성

[[382_singleton_summary|싱글톤 패턴]]은 클래스의 인스턴스를 오직 하나만 [[087_process_state_transition|생성]]하고, 어디서든 그 인스턴스에 접근할 수 있게 만드는 [[252_creational_patterns_overview|생성 패턴]]이다. [[009_config|설정]] 관리자, [[568_logs_distributed_logging_elk_fluentd|로그]] 기록기, 캐시 관리자처럼 프로세스 수준에서 하나만 있으면 되는 자원에 자주 적용된다. 문제는 "하나만 존재"해야 한다는 요구와 "어디서나 직접 꺼내 쓴다"는 구현을 쉽게 동일시한다는 데 있다.

초기에 [[253_singleton_pattern_single_instance|싱글톤]]이 매력적인 이유는 사용이 간단하기 때문이다. 객체 [[087_process_state_transition|생성]] 코드를 따로 전달하지 않아도 되고, 호출하는 쪽은 `getInstance()`만 알면 된다. 그러나 시스템이 커질수록 전역 접근점은 의존성을 코드 표면에서 숨기고, 누가 언제 상태를 바꾸는지 추적하기 어렵게 만든다.

즉 [[253_singleton_pattern_single_instance|싱글톤]]의 진짜 쟁점은 "인스턴스 개수"보다 "[[087_process_state_transition|생성]] 책임과 접근 방식"이다. 같은 1개 인스턴스라도 외부 [[561_container_based_deployment|컨테이너]]가 관리하면 통제 가능한 공유 자원이 되지만, 전역 정적 접근으로 고정하면 설계 유연성이 급격히 떨어진다.

- **📢 섹션 요약 비유**: [[253_singleton_pattern_single_instance|싱글톤]]은 회사에 공용 열쇠 한 개만 두는 방식과 같다. 열쇠가 하나인 것 자체는 문제없지만, 아무나 보관함에서 꺼내 쓸 수 있으면 누가 언제 가져갔는지 관리가 어려워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전통적 [[253_singleton_pattern_single_instance|싱글톤]]의 구조에서는 클라이언트 클래스가 직접 정적 메서드를 호출해 객체를 가져온다. 이때 의존성은 [[087_process_state_transition|생성]]자나 인터페이스에 드러나지 않고, 코드 내부 깊숙한 곳에 박혀 버린다. 반면 [[190_enterprise_di_framework_lifecycle|DI]] 방식에서는 [[561_container_based_deployment|컨테이너]]가 객체 [[087_process_state_transition|생성]]과 생명주기를 맡고, 사용하는 쪽은 필요한 의존성을 [[087_process_state_transition|생성]]자나 인터페이스로 선언한다.

아래 그림은 같은 단일 인스턴스 요구가 전혀 다른 결합 구조를 만들 수 있음을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│           전통 Singleton vs DI 컨테이너 관리형 Singleton            │
├───────────────────────────────┬──────────────────────────────────────┤
│ 전통 Singleton                │ DI + IoC 컨테이너                   │
│                               │                                      │
│ ServiceA ── getInstance() ─┐  │ Container ── 생성/보관 ── SharedObj │
│ ServiceB ── getInstance() ─┼─▶│    │                    ┌───────────┐ │
│ ServiceC ── getInstance() ─┘  │    ├─ inject ────────▶ │ ServiceA   │ │
│                               │    ├─ inject ────────▶ │ ServiceB   │ │
│ 숨겨진 직접 의존              │    └─ inject ────────▶ │ ServiceC   │ │
│ 전역 상태 변경 파급           │       의존성 명시      └───────────┘ │
└───────────────────────────────┴──────────────────────────────────────┘
```

| 단점 | 왜 발생하는가 | 실제 문제 |
| :--- | :--- | :--- |
| 전역 상태 오염 | 하나의 객체 상태를 여러 곳이 공유 | 테스트 순서에 따라 결과가 달라짐 |
| 테스트 격리 실패 | `getInstance()` 호출을 Mock으로 바꾸기 어려움 | 실 DB, 실 캐시를 붙인 채 테스트하게 됨 |
| 숨겨진 강결합 | 의존성이 [[087_process_state_transition|생성]]자 시그니처에 드러나지 않음 | 영향 범위 분석과 리팩터링이 어려움 |
| 생명주기 경직 | [[087_process_state_transition|생성]]·종료 시점을 코드가 직접 고정 | 초기화 순서, 종료 훅 관리가 어려움 |
| [[014_concurrency|동시성]] 위험 | 잘못 구현하면 멀티스레드에서 중복 [[087_process_state_transition|생성]] 또는 상태 경쟁 발생 | 간헐적 장애, 재현 어려운 버그 |

특히 변경 가능한 상태를 가진 [[253_singleton_pattern_single_instance|싱글톤]]은 위험하다. [[009_config|설정]] 값을 읽기만 하는 불변 객체는 비교적 안전하지만, 내부 캐시나 세션성 데이터를 계속 바꾸는 객체는 전역 가변 변수와 사실상 같은 성격을 띤다. 이 지점에서 [[253_singleton_pattern_single_instance|싱글톤]]은 패턴이라기보다 [[128_water_scrum_fall_anti_pattern|안티패턴]]에 가까워진다.

- **📢 섹션 요약 비유**: 전통 [[253_singleton_pattern_single_instance|싱글톤]]은 아파트 공용 전등 스위치가 모든 집 안에 연결된 구조와 같다. 한 집이 스위치를 바꾸면 다른 집도 동시에 영향을 받는다.

---

## Ⅲ. 비교 및 연결

[[253_singleton_pattern_single_instance|싱글톤]]을 평가할 때는 "한 개를 유지한다"는 요구와 "전역 정적 접근"이라는 구현을 분리해서 봐야 한다. 같은 단일 인스턴스라도 정적 [[253_singleton_pattern_single_instance|싱글톤]], 정적 유틸리티, [[561_container_based_deployment|컨테이너]] 관리형 [[253_singleton_pattern_single_instance|Singleton]] 스코프는 유지보수성과 테스트성에서 큰 차이를 만든다.

| 비교 항목 | 전통 [[253_singleton_pattern_single_instance|Singleton]] | 정적 유틸리티 (Static Utility) | [[190_enterprise_di_framework_lifecycle|DI]] [[561_container_based_deployment|컨테이너]] [[253_singleton_pattern_single_instance|Singleton]] 스코프 |
| :--- | :--- | :--- | :--- |
| 인스턴스 존재 | 1개 | 인스턴스 없음 | [[561_container_based_deployment|컨테이너]]당 1개 |
| 의존성 표현 | 암묵적 | 암묵적 | 명시적 |
| 테스트 대체 | 어려움 | 매우 어려움 | 쉬움 |
| 생명주기 관리 | 클래스 자체 | 없음 | [[561_container_based_deployment|컨테이너]]가 담당 |
| 적합 대상 | 매우 제한적 | 순수 계산 로직 | 공유 인프라 [[090_service_kubernetes_network_load_balancing|서비스]] |

설계 원칙으로 보면 [[253_singleton_pattern_single_instance|싱글톤]] 남용은 [[247_dip_dependency_inversion_principle|DIP]] ([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]], 의존관계 역전 원칙)와 [[243_srp_single_responsibility_principle|SRP]] ([[243_srp_single_responsibility_principle|Single Responsibility Principle]], [[355_process|단일 책임 원칙]])를 함께 흔든다. 객체가 비즈니스 로직 수행과 자기 자신 [[087_process_state_transition|생성]]·보호를 동시에 떠안기 때문이다. 반면 DI는 객체가 필요한 [[198_abstraction_control_data_process|추상화]]만 의존하게 만들어 결합을 낮추고, IoC [[561_container_based_deployment|컨테이너]]가 [[087_process_state_transition|생성]] 책임을 가져간다.

따라서 실무에서는 "[[253_singleton_pattern_single_instance|싱글톤]]을 금지"하기보다 "전통 정적 [[253_singleton_pattern_single_instance|싱글톤]]을 기본값으로 쓰지 않는다"가 더 정확한 원칙이다. 공유가 필요한 객체는 [[561_container_based_deployment|컨테이너]] 스코프로 관리하고, 상태가 있는 [[064_relation_domain|도메인]] 객체는 요청 범위 (Request [[512_oauth_scope|Scope]])나 [[257_prototype_pattern_object_cloning|프로토타입]] ([[257_prototype_pattern_object_cloning|Prototype]]) 같은 더 좁은 생명주기를 고려해야 한다.

- **📢 섹션 요약 비유**: 전통 [[253_singleton_pattern_single_instance|싱글톤]]이 공용 열쇠를 벽에 걸어 두는 방식이라면, DI는 총무팀이 출입 권한과 대여 기록을 관리하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 흔한 실패 사례는 [[090_service_kubernetes_network_load_balancing|서비스]] 로직이 내부에서 직접 `PaymentGateway.getInstance()`나 `ConfigManager.getInstance()`를 호출하는 구조다. 이렇게 되면 테스트에서 대체 구현을 넣기 어렵고, 개발·운영·테스트 환경별 [[009_config|설정]]도 유연하게 바꾸기 힘들다. 특히 Spring 같은 프레임워크에서는 이미 IoC [[561_container_based_deployment|컨테이너]]가 있으므로, 전통 [[253_singleton_pattern_single_instance|싱글톤]]을 새로 만들 이유가 거의 없다.

### 채택/회피 판단 기준

1. **채택 가능**: 불변 [[009_config|설정]], 프로세스 전역 [[568_logs_distributed_logging_elk_fluentd|로그]] 기록기처럼 상태 변경이 거의 없고 대체 필요가 낮은 인프라 객체
2. **회피 권장**: 사용자별 상태, 캐시 내용, 외부 연결 상태를 직접 들고 있는 [[090_service_kubernetes_network_load_balancing|서비스]] 객체
3. **우선 대안**: [[087_process_state_transition|생성]]자 주입 (Constructor [[480_injection|Injection]]) + 인터페이스 [[198_abstraction_control_data_process|추상화]] + [[561_container_based_deployment|컨테이너]] 스코프 [[009_config|설정]]
4. **예외 구현**: 언어 차원에서 안전한 `enum` [[253_singleton_pattern_single_instance|Singleton]] 같은 방식은 가능하지만, 여전히 테스트성과 생명주기 문제는 별도로 검토해야 함

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 상태를 가진 [[064_relation_domain|도메인]] [[090_service_kubernetes_network_load_balancing|서비스]]를 [[253_singleton_pattern_single_instance|싱글톤]]으로 고정하는 설계
- 정적 호출 때문에 순환 의존성이 숨어 있는 설계
- 멀티스레드 안전성을 검토하지 않은 [[015_지연_데이터_관점|지연]] 초기화 ([[380_computational_graph_lazy_eager_execution|Lazy]] Initialization)

예를 들어 주문 [[090_service_kubernetes_network_load_balancing|서비스]]가 전역 할인 [[164_policy|정책]] 객체를 직접 참조하면, A/B 테스트나 고객군별 [[164_policy|정책]] 교체가 매우 어려워진다. 반대로 `DiscountPolicy` 인터페이스를 주입받으면 테스트에서는 [[462_mock_test_double|Mock]] [[164_policy|정책]]을, 운영에서는 실제 [[164_policy|정책]]을 선택적으로 바꿔 끼울 수 있다. 기술사 답안에서는 이처럼 공유 필요와 전역 정적 접근을 구분해 설명하는 것이 핵심이다.

- **📢 섹션 요약 비유**: DI로 바꾸는 것은 공용차를 없애는 일이 아니라, 차량 배차를 관리팀이 맡도록 바꾸는 일과 같다. 차는 여전히 한 대일 수 있지만, 누가 어떤 목적으로 쓰는지는 훨씬 투명해진다.

---

## Ⅴ. 기대효과 및 결론

[[190_enterprise_di_framework_lifecycle|DI]] 기반으로 전환하면 단일 인스턴스의 장점은 유지하면서도 의존성 가시성, 테스트 용이성, 교체 가능성을 동시에 얻을 수 있다. [[330_code_review|코드 리뷰]] 시 [[087_process_state_transition|생성]]자만 봐도 필요한 의존성을 파악할 수 있고, 테스트에서는 모의 객체 ([[399_mock_object|Mock Object]])로 쉽게 대체할 수 있다. 운영 측면에서도 초기화 순서, 종료 처리, 스코프 관리가 체계화된다.

다만 모든 객체를 무조건 [[253_singleton_pattern_single_instance|Singleton]] 스코프로 두는 것도 정답은 아니다. 상태 범위가 사용자별인지, 요청별인지, 프로세스 전체인지 먼저 판단해야 한다. 결국 설계의 핵심은 몇 개를 만들 것인가보다 누가 [[087_process_state_transition|생성]]과 생명주기를 책임질 것인가다.

정리하면 [[382_singleton_summary|싱글톤 패턴]]의 단점은 패턴 그 자체보다 전역 정적 접근에 과도하게 의존할 때 폭발한다. 따라서 현대적 해법은 전통 [[253_singleton_pattern_single_instance|싱글톤]]을 반복 구현하는 것이 아니라, DI와 IoC를 통해 공유 자원을 통제 가능한 형태로 관리하는 것이다.

- **📢 섹션 요약 비유**: 좋은 설계는 열쇠를 한 개로 유지할지보다, 그 열쇠를 누가 보관하고 기록할지를 먼저 정하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[252_creational_patterns_overview|생성 패턴]] (Creational Pattern) | [[253_singleton_pattern_single_instance|싱글톤]]이 속한 GoF (Gang of Four) 패턴 [[104_classification_analysis|분류]] |
| 전역 상태 (Global [[272_state_pattern|State]]) | [[253_singleton_pattern_single_instance|싱글톤]]의 대표적 부작용 |
| [[190_enterprise_di_framework_lifecycle|DI]] ([[337_dependency_injection|Dependency Injection]]) | 의존성을 외부에서 주입해 결합도를 낮추는 대안 |
| IoC [[561_container_based_deployment|컨테이너]] (Inversion of Control [[194_container_virtualization_docker_namespace|Container]]) | 객체 [[087_process_state_transition|생성]]과 생명주기를 관리하는 운영 주체 |
| [[247_dip_dependency_inversion_principle|DIP]] ([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]]) | 구체 클래스가 아닌 [[198_abstraction_control_data_process|추상화]]에 의존하게 만드는 설계 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
전역 객체 공유 요구
    │
    ▼
전통 Singleton Pattern
    │
    ├─ 장점: 단일 인스턴스 보장
    └─ 한계: 전역 상태 · 숨겨진 결합 · 테스트 어려움
    │
    ▼
DI (Dependency Injection) · IoC 컨테이너
    │
    ▼
컨테이너 관리형 Singleton 스코프
    │
    ▼
명시적 의존성 · 테스트 가능 설계 · 유연한 스코프 관리
```

이 흐름도는 공유 자원 필요가 전통 [[253_singleton_pattern_single_instance|싱글톤]]으로 출발해, 결국 의존성 관리 체계로 진화하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[253_singleton_pattern_single_instance|싱글톤]]은 반 친구들이 연필 한 자루를 같이 쓰는 것과 같아요.
2. 그런데 누가 지우개를 떼어 가거나 부러뜨리면 모두가 같이 불편해져요.
3. DI는 선생님이 연필을 맡아서 필요한 친구에게 빌려주는 방식이라서, 누가 무엇을 쓰는지 훨씬 잘 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 219 / 530

← **이전**: [[162_god_class_blob|162. 갓 클래스/블랍 (God Class / Blob)]]
**다음**: [[164_adapter_vs_facade|164. 어댑터 vs 퍼사드 (Adapter vs Facade)]] →

---
