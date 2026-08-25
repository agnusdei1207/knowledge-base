---
sidebar:
  order: 47
  label: "047. 디자인 패턴: GoF 23종"
  badge:
    text: "미출 · 50%"
    variant: note
title: "디자인 패턴: GoF 23종 (Design Patterns GoF)"
date: "2026-08-25T10:48:00+09:00"
tags:
  - "notes-software"
weight: 47
extra:
  question_no: "047"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "객체지향 설계 문제 해결을 위한 3대 패턴 분류"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **GoF(Gang of Four) 디자인 패턴**: 에리히 감마(Erich Gamma) 등 4명의 저자가 정립한 객체지향 소프트웨어 설계의 23가지 재사용 가능한 해결 템플릿.
- **생성·구조·행위 패턴**: 객체의 인스턴스화(생성 5종), 클래스/객체의 합성(구조 7종), 상호작용 및 책임 분배(행위 11종)의 3대 분류.

</details>

- 정의/개념: 객체지향 설계의 유연성과 재사용성을 높이기 위해 검증된 객체 생성, 구조 결합, 행위 위임 전략을 정립한 **GoF 23종 디자인 패턴**
- 배경/필요성: 객체 간 하드코딩과 강결합으로 인한 **요구사항 변경 시 전역 파급 효과 및 코드 재사용 불가 해결 불가**

#### 한줄 요약
- 생성(5종), 구조(7종), 행위(11종)의 23개 표준 설계 템플릿으로 객체지향 유연성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **공통 설계 어휘(Common Vocabulary)**: "이 클래스는 Factory Method로 구현하고 Strategy로 알고리즘을 주입합시다"와 같이 개발자 간 소통 비용을 줄이는 표준 용어.
- **Composition over Inheritance**: 상속의 강결합을 피하고 객체 합성(Composition)과 인터페이스 위임을 통해 런타임 유연성을 확보하는 원칙.

</details>

- 목적별 3대 분류 체계: **생성 패턴 5종, 구조 패턴 7종, 행위 패턴 11종** 구조화
- 인터페이스 다형성과 객체 합성을 활용하여 **개방 폐쇄 원칙(OCP) 및 의존역전 원칙(DIP)** 실현
- 개발자 간 아키텍처 설계 의도를 명확하고 간결하게 소통하는 **공통 설계 어휘** 역할

#### 한줄 요약
- 3대 분류 체계와 공통 어휘를 제공하며, 상속 대신 합성을 활용해 OCP/DIP를 달성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Factory vs Adapter vs Strategy**: 생성(Factory: 인스턴스화 위임), 구조(Adapter: 인터페이스 변환), 행위(Strategy: 알고리즘 교체)의 대표 패턴.

</details>

```text
[GoF 23종 디자인 패턴 분류 트리]
|-- 생성 패턴 (Creational: 5종 - 객체 생성 캡슐화)
|   |-- Singleton, Factory Method, Abstract Factory
|   `-- Builder, Prototype
|-- 구조 패턴 (Structural: 7종 - 클래스/객체 합성)
|   |-- Adapter, Bridge, Composite, Decorator
|   `-- Facade, Flyweight, Proxy
`-- 행위 패턴 (Behavioral: 11종 - 책임 분배 및 알고리즘 교체)
    |-- Strategy, Template Method, Observer, State
    |-- Command, Chain of Responsibility, Iterator
    `-- Mediator, Memento, Visitor, Interpreter
```

선의 의미: 23종 디자인 패턴의 목적별 3대 계층 분류

| 분류 그룹 | 패턴 종류 (23종) | 핵심 책임 및 의도 |
|:---|:---|:---|
| **생성 패턴 (5종)** | **Singleton, Factory Method, Abstract Factory, Builder, Prototype** | 객체 생성 과정을 추상화하여 **인스턴스화 결합도 제거** |
| **구조 패턴 (7종)** | **Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy** | 인터페이스 호환성 변환, **동적 기능 추가 및 구조적 합성** |
| **행위 패턴 (11종)** | **Strategy, Template Method, Observer, State, Command, Iterator 등** | 런타임 **알고리즘 교체, 이벤트 구독 통지 및 상태 전이 위임** |

#### 한줄 요약
- 생성(인스턴스화 캡슐화), 구조(객체 합성), 행위(알고리즘 교체 및 협업)로 완벽히 구조화된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **설계 냄새(Design Smell)**: if-else 분기문 폭증, 거대 클래스, 상속 깊이 과다 등 패턴 적용이 필요한 결함 징후.

</details>

```text
코드 냄새 및 설계 문제 식별 (예: 결제 수단별 if-else 분기 폭증)
        │
   문제 성격 분석 (생성 문제인가, 구조적 결합인가, 행위/알고리즘 교체인가?)
        │
   적합한 GoF 패턴 매핑 (알고리즘 교체 -> Strategy 패턴 선정)
        │
   복잡도 대비 유연성 트레이드오프 평가 (YAGNI 위반 여부 검토)
        │
   인터페이스 정의 및 구현체 분리 리팩토링 (`PaymentStrategy` 구현)
        │
   신규 결제 수단 추가 시 기존 코드 무수정 OCP 확장 완료
```

#### 한줄 요약
- 문제 식별 → 3대 영역 분석 → 최적 패턴 매핑 → 트레이드오프 검토 → OCP 리팩토링 순으로 적용한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Strategy vs Template Method**: 인터페이스 위임(Composition)을 통한 런타임 알고리즘 교체(Strategy)와 상속(Inheritance)을 통한 컴파일 타임 알고리즘 뼈대 재사용(Template Method).

</details>

| 핵심 패턴 | 분류 | 핵심 의도 및 해결책 | 코드 설계 특징 |
|:---|:---|:---|:---|
| **Singleton** | 생성 | 전역에서 단 하나의 인스턴스만 보장 | `private` 생성자 + `static getInstance()` |
| **Factory Method** | 생성 | 객체 생성을 하위 서브클래스에 위임 | 상속을 통한 인스턴스화 분리 |
| **Adapter** | 구조 | 호환되지 않는 인터페이스를 맞춤 변환 | 래퍼(Wrapper) 클래스로 중계 |
| **Decorator** | 구조 | 상속 없이 런타임에 동적으로 기능 덧붙임 | 동일 인터페이스를 감싸며 부가기능 실행 |
| **Proxy** | 구조 | 실제 객체 접근 제어, 지연 로딩, 보안 검증 | 실제 객체와 동일 인터페이스 대리자 |
| **Strategy** | 행위 | **런타임에 알고리즘(전략)을 자유롭게 교체** | **인터페이스 위임 (Composition)** |
| **Observer** | 행위 | 상태 변화 시 다수의 구독자에게 자동 통지 | **발행/구독 (Event Listener) 구조** |

#### 한줄 요약
- Singleton/Factory(생성), Adapter/Decorator/Proxy(구조), Strategy/Observer(행위)가 실무 최다 빈출 패턴이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Pattern Overengineering(패턴 과용)**: 단순한 10줄짜리 코드에 5개의 클래스와 인터페이스를 만들어 가독성과 유지보수성을 해치는 설계 과잉.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단순한 로직에 불필요한 다중 패턴 적용(**패턴 과용**) | **YAGNI / KISS 원칙** 준수 및 실제 3회 이상 중복 시 도입 | 코드 단순성 및 가독성 유지 |
| 패턴 적용으로 인한 클래스 수 급증 및 보일러플레이트 | 최신 언어의 **함수형 인터페이스 및 람다식(Lambda)** 활용 | 별도 Strategy 클래스 없이 1줄로 전략 주입 |
| 멀티스레드 환경에서 Singleton 동시성 버그 | **Initialization-on-demand Holder Idiom 또는 Enum** 사용 | 스레드 세이프(Thread-Safe) 및 지연 로딩 완벽 보장 |
| 상속 기반 Template Method의 강결합 문제 | 인터페이스 위임 기반 **Strategy 패턴으로 리팩토링** | 상속 결합도 제거 및 런타임 교체 유연성 확보 |

#### 한줄 요약
- YAGNI 원칙 준수, 람다식 간소화, Holder 싱글톤, 전략 패턴 전환으로 실무 최적화를 달성한다.

## Ⅶ. 결론

- 변화가 빈번한 핵심 비즈니스 도메인은 **GoF 디자인 패턴(Strategy, Factory, Observer)** 을 적극 활용하여 OCP를 실현하고, 단순 CRUD는 **YAGNI 원칙**을 지켜 오버엔지니어링 차단

#### 한줄 요약
- GoF 디자인 패턴은 객체지향 5대 원칙(SOLID)을 실현하는 검증된 설계 청사진이며, 문제의 본질에 부합하는 선별적 적용이 핵심이다.