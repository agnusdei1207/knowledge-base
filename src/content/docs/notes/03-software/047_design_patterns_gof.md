---
sidebar:
  order: 47
  label: "047. 디자인 패턴: GoF 23종 (Design Patterns GoF)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "디자인 패턴: GoF 23종 (Design Patterns GoF)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 47
extra:
  question_no: "047"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "GoF 패턴은 생성•구조•행위 선택 정본"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **GoF Design Patterns (GoF 23가지 디자인 패턴)**: Erich Gamma 등 4명의 저자(Gang of Four)가 객체지향 소프트웨어 설계 시 자주 발생하는 23가지 문제 상황과 이에 대한 재사용 가능한 최적의 모범 구조 솔루션 모음집.
- **Creational / Structural / Behavioral Patterns**: GoF 23종 패턴을 목적에 따라 객체 생성을 다루는 생성 패턴(5종), 클래스/객체 합성을 다루는 구조 패턴(7종), 객체 간 상호작용/알고리즘을 다루는 행위 패턴(11종)으로 3대 분류한 체계.

</details>

- 정의/개념: 객체지향 소프트웨어 설계에서 반복적으로 나타나는 구조적 문제들을 체계적으로 분류하고 재사용 가능한 클래스/객체 설계 구조로 정리한 23가지 정본 모음집인 **GoF Design Patterns**
- 배경/필요성: 동일 설계 문제에 대한 주구장창 재발명(Reinventing the wheel) 방지, 개발자 간 커뮤니케이션 어휘(Vocabulary) 통일 및 재사용성 향상 요구성

#### 한줄 요약

- GoF 디자인 패턴과 이를 체계화한 GoF의 역할•협력 구조가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Patternitis (패턴 중독)**: 단순하고 직관적인 코드로 충분한 상황임에도 디자인 패턴의 기교를 무리하게 대입하여 오히려 구조를 복잡하게 만드는 오남용 상태.

</details>

- 목적에 따른 3대 분류 (**Creational 5종, Structural 7종, Behavioral 11종**)
- **SOLID 원칙** (특히 OCP, DIP)을 객체 수준에서 구현한 실체적 가이드
- 개발자 간의 공통 어휘 기반 아키텍처 커뮤니케이션 표준화

#### 한줄 요약

- 패턴 의도, 적용 조건, 참여자, 협력, 결과, 상충 관계가 패턴 선택의 근거이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **3대 패턴 분류**: 생성(Creational - 객체 생성을 유연하게), 구조(Structural - 클래스/객체를 크게 합성), 행위(Behavioral - 객체 간 책임을 유연하게 분배).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        GoF Design Patterns (23종)                      │
├─────────────────────┬──────────────────────┬───────────────────────────┤
│ Creational (5종)    │ Structural (7종)     │ Behavioral (11종)         │
│ (생성 패턴)         │ (구조 패턴)          │ (행위 패턴)               │
└─────────────────────┴──────────────────────┴───────────────────────────┘
```

선의 의미: 23가지 GoF 패턴이 목적에 따라 생성 5종, 구조 7종, 행위 11종으로 분화되는 전체 매트릭스 아키텍처.

| 분류 (Type) | 분류 정의 | 패턴 종류 (GoF 23종) |
|:---|:---|:---|
| **Creational (생성 5종)** | 객체 생성 프로세스 추상화, 생성과 상용의 격리 | **Abstract Factory, Builder, Factory Method, Prototype, Singleton** |
| **Structural (구조 7종)**| 더 큰 구조를 얻기 위해 클래스/객체 합성 | **Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy** |
| **Behavioral (행위 11종)**| 객체 간 알고리즘과 책임 분배 및 비동기 협력 | **Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor** |

#### 한줄 요약

- 문제 맥락과 변동 지점이 패턴 명세의 출발점이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Pattern Selection Flow**: 문제 맥락(Context) 분석 $\rightarrow$ 3대 분류(Creational/Structural/Behavioral) 결정 $\rightarrow$ 23종 패턴 중 최적 솔루션 선택.

</details>

```text
┌──────────────────────────────┐
│ 객체지향 설계 문제 발생      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 문제 맥락 분석 (Context)  │
│ 2. 3대 분류 결정 (생성/구조/행위)│
│ 3. 최적 GoF 패턴 매핑        │
│ 4. Trade-off 평가           │
└──────────────┬───────────────┘
               ▼
       [클린 모듈 구현]
```

### 동작 원리

1. **문제 맥락 분석**: 해결하고자 하는 문제가 객체 생성 방식인가, 구조적 합성인가, 동작/알고리즘 분리인가 분석.
2. **3대 분류 결정**: 생성(Creational), 구조(Structural), 행위(Behavioral) 3대 범주 중 1개 선택.
3. **최적 GoF 패턴 매핑**: 23종 중 의도(Intent)에 부합하는 패턴(e.g., 알고리즘 교체 $\rightarrow$ Strategy Pattern) 인가.
4. **Trade-off 평가**: 인프라 복잡도와 클래스 개수 증가 대 가독성/유지보수성 유용성 판단.

#### 한줄 요약

- 변동 지점 판정, 패턴 범주 선택, 적용 조건 검증, 상충 관계 검증이 핵심이다.

## Ⅴ. 종류 및 상세 기재 (핵심 9선)

<details><summary>핵심 용어</summary>

- **Strategy vs Template Method**: Strategy는 위임(Composition)을 통해 알고리즘 전체를 런타임에 교체하고, Template Method는 상속(Inheritance)을 통해 알고리즘의 특정 서브 단계만 오버라이딩.

</details>

| 핵심 패턴 명칭 | 분류 | 패턴 핵심 의도 및 적용 사례 |
|:---|:---|:---|
| **Singleton** | 생성 | 단 1개의 인스턴스만 보장 및 전역 억세스 제공 (Spring Bean 기본 scope) |
| **Factory Method** | 생성 | 객체 생성 인스턴스화 로직을 서브클래스로 위임하여 결합도 소멸 |
| **Builder** | 생성 | 복잡한 객체의 생성 과정과 표현 과정을 분리하여 가독성 있는 체이닝 생성 |
| **Adapter** | 구조 | 호환되지 않는 인터페이스를 변환하여 함께 동작할 수 있도록 래핑 |
| **Decorator** | 구조 | 기존 객체를 수정하지 않고 동적으로 새로운 기능/책임을 덧붙임 (Java I/O Stream) |
| **Proxy** | 구조 | 타깃 객체 접근을 중계하여 가로채기(AOP, Lazy Loading, 보안) 기능 수행 |
| **Strategy** | 행위 | 알고리즘군을 정의하고 각각을 캡슐화하여 런타임에 유연하게 교체 수용 |
| **Observer** | 행위 | 일대다 객체 의존성을 정의하여 한 객체 상태 변경 시 구독자들에게 자동 통지 |
| **Template Method** | 행위 | 알고리즘의 골격(Structure)을 부모 메서드에 정의하고 세부 단계는 자식이 구현 |

#### 한줄 요약

- 생성•연결•협력의 변동 지점별 범주를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **YAGNI (You Aren't Gonna Need It)**: 실제로 당장 필요하지 않은 유연성이나 과도한 디자인 패턴을 사전에 구현하지 말라는 극단적 절제 원칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단순 코드에 무분별한 패턴 적용으로 복잡성 폭증 (**Patternitis**) | **YAGNI (You Aren't Gonna Need It)** 원칙 기반 최소한 설계 유지 | 유지보수 가독성 확보 |
| 패턴 적용으로 인한 클래스 개수 폭발적 증가 | Java Lambda, Stream 등 현대적 가벼운 언어적 기능으로 대체 | 코드 분량 최소화 |
| 팀원 간 패턴 이해도 격차로 인한 커뮤니케이션 장애 | 코드 주석 및 **ADR (아키텍처 결정 기록)** 에 디자인 패턴 사용 명시 | 팀 생산성 균형 |

> 사례: Spring Framework 내부의 **Factory Method, Singleton, Proxy (AOP), Template Method (JdbcTemplate)** 융합

#### 한줄 요약

- 패턴 중독, ADR, 성능 비용, 변경성, 관측 경계를 함께 검토한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **GoF 패턴 채택 기준(GoF Pattern Adoption Criteria)**: 확장 요구 빈도, 도메인 아키텍처 및 YAGNI 원칙에 따른 선택 체계.

</details>

- **GoF 패턴 채택 기준**에 따라 무조건적 패턴 도입을 경계하고, **SOLID 원칙** 보조 수단으로서 **GoF 23종 패턴** 적용

#### 한줄 요약

- 반복 변경 범위와 추상화 비용을 함께 평가하는 것이 핵심이다.
