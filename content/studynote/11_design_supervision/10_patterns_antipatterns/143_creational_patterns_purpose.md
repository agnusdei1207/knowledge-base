---
title: 143. 생성 패턴의 목적 (Creational Patterns Purpose)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[252_creational_patterns_overview|생성 패턴]] ([[252_creational_patterns_overview|Creational Patterns]])은 객체 인스턴스 [[087_process_state_transition|생성]] 책임을 캡슐화해 클라이언트가 구체 클래스와 직접 결합되지 않게 만든다.
> 2. **가치**: [[087_process_state_transition|생성]] 로직을 분리하면 확장성, 테스트 용이성, 제품군 교체 유연성이 함께 높아진다.
> 3. **판단 포인트**: 무엇을 만들까보다 누가 어떤 기준으로 만들까를 분리해야 [[252_creational_patterns_overview|생성 패턴]]의 효과가 나온다.

---

## Ⅰ. 개요 및 필요성

객체지향 설계에서 가장 흔한 [[459_quic_fec_forward_error_correction|초기]] 실수는 클라이언트가 `new ConcreteClass()`를 직접 호출하며 [[087_process_state_transition|생성]] 책임을 스스로 떠안는 것이다. 처음에는 단순하지만, [[087_process_state_transition|생성]] 규칙이 늘어나면 클라이언트는 구체 클래스, [[009_config|설정]] 값, 조립 순서, 환경 분기까지 모두 알게 된다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                   직접 생성이 만드는 결합 구조                       │
├──────────────────────────────────────────────────────────────────────┤
│ Client ──new──▶ ConcreteA                                            │
│ Client ──new──▶ ConcreteB                                            │
│ Client ──if/else──▶ 환경별 생성 규칙                                 │
│                                                                      │
│ 결과: 생성 규칙 변경 ──▶ Client 수정 ──▶ 테스트/확장 비용 증가        │
└──────────────────────────────────────────────────────────────────────┘
```

[[252_creational_patterns_overview|생성 패턴]]의 목적은 이 [[087_process_state_transition|생성]] 책임을 별도 계층, 메서드, 객체, 원형으로 옮기는 데 있다. 즉 클라이언트는 무슨 역할의 객체가 필요하다까지만 알고, 구체적으로 어떻게 만들어지는가는 숨긴다. 이 구조가 OCP와 DIP를 실무 수준에서 돕는다.

- **📢 섹션 요약 비유**: 손님이 주방에 들어가 직접 요리하는 대신, 주문만 하고 요리는 주방 시스템이 알아서 하게 만드는 것이 [[252_creational_patterns_overview|생성 패턴]]이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[252_creational_patterns_overview|생성 패턴]]은 모두 [[087_process_state_transition|생성]] 책임을 분리하지만, 해결하는 [[087_process_state_transition|생성]] 문제가 다르다. 유일 인스턴스 보장, 서브클래스 위임, 패밀리 [[087_process_state_transition|생성]], 단계적 조립, [[016_replication_factor|복제]] 기반 [[087_process_state_transition|생성]]처럼 문제 유형별로 초점이 달라진다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    생성 책임 분리의 기본 흐름                         │
├──────────────────────────────────────────────────────────────────────┤
│ Client                                                               │
│   │                                                                  │
│   ├──▶ Singleton ─────▶ 유일 인스턴스 보장                           │
│   ├──▶ Factory Method ─▶ 생성할 하위 타입 결정                       │
│   ├──▶ Abstract Factory ─▶ 관련 객체 묶음 생성                       │
│   ├──▶ Builder ───────▶ 복잡한 조립 순서 분리                        │
│   └──▶ Prototype ─────▶ 기존 객체 복제로 생성                        │
└──────────────────────────────────────────────────────────────────────┘
```

| 패턴 | 해결하는 [[087_process_state_transition|생성]] 문제 | 핵심 메커니즘 |
|:---|:---|:---|
| [[253_singleton_pattern_single_instance|Singleton]] | 인스턴스가 하나만 있어야 함 | private [[087_process_state_transition|생성]]자와 전역 접근점 |
| [[254_factory_method_pattern_subclass_creation|Factory Method]] | [[087_process_state_transition|생성]]할 타입을 하위 클래스가 결정 | [[087_process_state_transition|생성]] 메서드 오버라이드 |
| [[255_abstract_factory_pattern_object_families|Abstract Factory]] | 관련 객체 세트를 일관되게 [[087_process_state_transition|생성]] | 제품군별 팩토리 인터페이스 |
| [[256_builder_pattern_step_by_step_creation|Builder]] | 복잡한 객체를 단계적으로 조립 | 조립 과정과 표현 분리 |
| [[257_prototype_pattern_object_cloning|Prototype]] | [[087_process_state_transition|생성]] 비용이 큰 객체를 빠르게 [[016_replication_factor|복제]] | [[149_clone_system_call|clone]] 또는 원형 복사 |

이 다섯 패턴은 서로 경쟁 관계라기보다 문제 [[104_classification_analysis|분류]] 관계다. 예를 들어 UI 테마처럼 버튼·체크박스를 함께 바꿔야 하면 Abstract Factory가 맞고, [[343_json|JSON]] 응답처럼 선택 필드가 많은 객체를 안전하게 만들려면 Builder가 더 적합하다.

- **📢 섹션 요약 비유**: 같은 만든다라는 행위라도 공장 생산, 맞춤 제작, 복사, 한정 수량 관리가 서로 다른 방식인 것처럼 [[252_creational_patterns_overview|생성 패턴]]도 [[087_process_state_transition|생성]] 문제의 종류가 다르다.

---

## Ⅲ. 비교 및 연결

[[252_creational_patterns_overview|생성 패턴]]의 실무 판단은 [[087_process_state_transition|생성]]의 복잡성을 어디서 느끼는가에 달려 있다. [[087_process_state_transition|생성]] 개수, [[087_process_state_transition|생성]] 타입, 조립 절차, 패밀리 [[194_consistency_database_integrity|일관성]], [[087_process_state_transition|생성]] 비용 중 무엇이 핵심인지에 따라 패턴 선택이 갈린다.

| 문제 상황 | 우선 검토 패턴 | 이유 |
|:---|:---|:---|
| 애플리케이션 전역에서 인스턴스 1개만 유지 | [[253_singleton_pattern_single_instance|Singleton]] | [[087_process_state_transition|생성]] 수 자체가 핵심 제약 |
| [[087_process_state_transition|생성]] 타입이 서브클래스나 [[009_config|설정]]에 따라 달라짐 | [[254_factory_method_pattern_subclass_creation|Factory Method]] | [[087_process_state_transition|생성]] 결정을 하위 계층에 위임 |
| [[001_operating_system_purpose|운영체제]]·테마별 관련 객체를 세트로 교체 | [[255_abstract_factory_pattern_object_families|Abstract Factory]] | 제품군 [[194_consistency_database_integrity|일관성]]을 함께 보장 |
| 선택 파라미터가 많아 [[087_process_state_transition|생성]]자 폭발 발생 | [[256_builder_pattern_step_by_step_creation|Builder]] | 조립 단계와 표현을 분리 |
| [[459_quic_fec_forward_error_correction|초기]]화 비용이 큰 객체를 반복 [[087_process_state_transition|생성]] | [[257_prototype_pattern_object_cloning|Prototype]] | 새 [[087_process_state_transition|생성]]보다 [[016_replication_factor|복제]]가 효율적 |

[[252_creational_patterns_overview|생성 패턴]]은 IoC [[561_container_based_deployment|컨테이너]]와도 연결된다. Spring 같은 프레임워크는 [[254_factory_method_pattern_subclass_creation|Factory Method]], [[255_abstract_factory_pattern_object_families|Abstract Factory]], [[253_singleton_pattern_single_instance|Singleton]] 개념을 시스템 수준으로 확장한 예다. 그래서 [[252_creational_patterns_overview|생성 패턴]]을 이해하면 [[190_enterprise_di_framework_lifecycle|DI]] [[561_container_based_deployment|컨테이너]] 동작도 더 명확하게 보인다.

- **📢 섹션 요약 비유**: 어떤 집은 열쇠 하나만 있으면 되고, 어떤 집은 가구 세트를 통째로 맞춰야 하며, 어떤 집은 샘플 하우스를 복사해 짓는 것이 더 빠른 것과 같은 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[252_creational_patterns_overview|생성 패턴]]은 [[190_enterprise_di_framework_lifecycle|DI]], [[009_config|설정]] 기반 객체 [[087_process_state_transition|생성]], 멀티 플랫폼 UI, 복잡한 DTO 조립, 캐시 가능한 원형 객체 관리 등에 널리 쓰인다. 중요한 것은 [[087_process_state_transition|생성]] 코드를 감춘다가 아니라 **[[087_process_state_transition|생성]] 변경의 파급을 어디서 끊을지 설계하는 것**이다.

기술사 답안에서는 5개 패턴을 단순 나열하기보다, 직접 [[087_process_state_transition|생성]]의 문제 → [[087_process_state_transition|생성]] 책임 분리 → 적합한 패턴 선택 → 기대효과 흐름으로 서술하면 구조적 완성도가 높다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. 클라이언트가 구체 클래스 이름과 [[087_process_state_transition|생성]] 절차를 직접 알고 있는가?
2. [[087_process_state_transition|생성]]할 타입, 제품군, 조립 순서, 인스턴스 개수 중 무엇이 핵심 문제인가?
3. 새 구현 추가 시 클라이언트 수정 없이 확장 가능한가?
4. 테스트에서 [[462_mock_test_double|Mock]] 또는 대체 구현으로 쉽게 바꿔 끼울 수 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]] 및 오답 포인트

- 단순 값 객체에도 과도한 Builder를 적용해 코드만 비대하게 만드는 설계
- Singleton을 상태 많은 [[064_relation_domain|도메인]] 객체에 남용해 [[014_concurrency|동시성]] 문제를 만드는 설계
- Abstract Factory가 필요한데 개별 Factory Method만 흩뿌려 제품군 [[194_consistency_database_integrity|일관성]]을 잃는 설계

- **📢 섹션 요약 비유**: 주문서를 정리하지 않은 식당은 메뉴가 늘어날수록 주방이 혼란해지지만, [[252_creational_patterns_overview|생성 패턴]]을 쓰면 누가 무엇을 어떤 규칙으로 만들지 주방 동선이 정리된다.

---

## Ⅴ. 기대효과 및 결론

[[252_creational_patterns_overview|생성 패턴]]을 잘 쓰면 클라이언트는 역할에만 의존하고 [[087_process_state_transition|생성]] 세부사항에서는 자유로워진다. 이는 구현 교체, 테스트 대역 주입, 제품군 전환, [[009_config|설정]] 기반 확장에 모두 유리하다. 특히 시스템이 커질수록 [[087_process_state_transition|생성]] 로직 중앙화의 효과가 커진다.

결론적으로 [[252_creational_patterns_overview|생성 패턴]]의 목적은 객체를 예쁘게 만드는 것이 아니라 **[[087_process_state_transition|생성]] 변화와 클라이언트 코드를 분리하는 것**이다. 이 관점을 잡으면 5개 패턴을 문제 중심으로 훨씬 쉽게 구분할 수 있다.

| 기대효과 | 구체적 내용 |
|:---|:---|
| [[195_coupling_levels|결합도]] 감소 | 클라이언트가 구체 클래스 [[087_process_state_transition|생성]] 세부사항에서 분리됨 |
| 확장성 향상 | 새 구현 추가 시 기존 호출부 수정 최소화 |
| 테스트 용이성 | [[462_mock_test_double|Mock]], [[460_stub_test_double|Stub]], 대체 구현 주입이 쉬워짐 |
| [[087_process_state_transition|생성]] 규칙 중앙화 | [[087_process_state_transition|생성]] 정책과 조립 순서를 한곳에서 관리 가능 |

- **📢 섹션 요약 비유**: [[252_creational_patterns_overview|생성 패턴]]은 건물을 예쁘게 칠하는 기술이 아니라, 자재 반입과 조립 순서를 통제하는 공정 관리 체계에 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[746_ocp|OCP]] | [[087_process_state_transition|생성]] 방식 확장 시 기존 호출부 수정을 줄이는 기준 |
| [[247_dip_dependency_inversion_principle|DIP]] | 구체 클래스 대신 추상화에 의존하게 만드는 기반 |
| [[190_enterprise_di_framework_lifecycle|DI]] / IoC | [[252_creational_patterns_overview|생성 패턴]]이 프레임워크 수준으로 확장된 대표 사례 |
| [[256_builder_pattern_step_by_step_creation|Builder]] | 복잡한 조립형 객체 [[087_process_state_transition|생성]]의 대표 패턴 |
| [[255_abstract_factory_pattern_object_families|Abstract Factory]] | 관련 객체 패밀리 [[087_process_state_transition|생성]]의 대표 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 생성(new) 남용
    │
    ▼
구체 클래스 결합 · 테스트 어려움
    │
    ▼
생성 패턴 (Creational Patterns)
    │
    ├──▶ Singleton
    ├──▶ Factory Method
    ├──▶ Abstract Factory
    ├──▶ Builder
    └──▶ Prototype
            │
            ▼
생성 책임 분리 · 확장성 · 테스트 용이성 향상
```

이 흐름은 [[087_process_state_transition|생성]] 문제가 단순 코딩 습관이 아니라 구조적 의존 문제이며, [[252_creational_patterns_overview|생성 패턴]]이 그 결합을 끊는 방식임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감을 만들 때 친구가 매번 공장에 직접 들어가 부품을 꺼내 오면 너무 복잡해져요.
2. 그래서 누가 만들어 줄지, 세트로 만들지, 복사해서 만들지 정하는 규칙이 필요해요.
3. [[252_creational_patterns_overview|생성 패턴]]은 장난감 만드는 방법을 똑똑하게 나누는 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 199 / 530

← **이전**: [[142_gof_23_patterns_classification|142. GoF 23가지 패턴 분류 (GoF 23 Design Patterns Classification)]]
**다음**: [[144_singleton_pattern|144. 싱글턴 패턴 (Singleton Pattern)]] →

---
