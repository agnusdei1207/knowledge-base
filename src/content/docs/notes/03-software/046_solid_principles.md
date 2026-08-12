---
sidebar:
  order: 46
  label: "046. SOLID 원칙 (SOLID Principles)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SOLID 원칙 (SOLID Principles)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 46
extra:
  question_no: "046"
  source_status: "기출"
  source_history: "128회, 132회"
  priority: 70
  priority_note: "128•132회 반복, 객체 설계 책임 원칙"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **SOLID Principles**: 로버트 C. 마틴(Uncle Bob)이 정립한 객체지향 설계(OOD) 및 아키텍처의 5가지 핵심 원칙(SRP, OCP, LSP, ISP, DIP)으로, 유지보수성과 확장성이 뛰어난 소프트웨어 구조를 구축하기 위한 설계 가이드라인.
- **Maintainability (유지보수성)**: 시스템 변경 요구사항 발생 시, 주변 코드에 예기치 못한 부작용(Side Effect) 없이 안전하고 손쉽게 수정/확장 가능한 코드 성질.
- **Coupling & Cohesion**: 모듈 간 의존도인 결합도(Coupling)는 낮추고(Loose Coupling), 모듈 내부 연관성인 응집도(Cohesion)는 높이는(High Cohesion) 객체지향의 기본 대원칙.

</details>

- 정의/개념: 객체지향 프로그래밍에서 코드의 유지보수성, 가독성 및 확장성을 극대화하기 위해 준수해야 할 5가지 핵심 설계 원칙의 두문자어인 **SOLID Principles**
- 배경/필요성: 강한 결합도(High Coupling)와 낮은 응집도(Low Cohesion)로 인한 스파게티 코드 방지, 요구사항 변경 시 기존 코드 수정 최소화 요구성

#### 한줄 요약

- SOLID와 책임 경계로 변경 영향을 줄이는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **SRP (Single Responsibility Principle)**: 클래스(모듈)는 단 하나의 변경 이유(Single Reason to Change)만을 가져야 한다는 단일 책임 원칙.
- **OCP (Open-Closed Principle)**: 소프트웨어 개체는 확장에는 열려 있어야 하고(Open for Extension), 수정에는 닫혀 있어야 한다는(Closed for Modification) 개방 폐쇄 원칙.
- **LSP (Liskov Substitution Principle)**: 하위 타입은 언제나 상위 타입으로 교체(치환)할 수 있어야 하며, 상위 타입의 계약(Behavior)을 훼손하지 않아야 한다는 리스코프 치환 원칙.
- **ISP (Interface Segregation Principle)**: 클라이언트는 자신이 사용하지 않는 메서드에 의존하지 않도록 범용 인터페이스 하나보다 구체적인 여러 인터페이스로 분리해야 한다는 인터페이스 분리 원칙.
- **DIP (Dependency Inversion Principle)**: 고수준 모듈은 저수준 모듈의 구체 구현에 의존하면 안 되며, 두 모듈 모두 추상화(Interface/Abstract Class)에 의존해야 한다는 의존 역전 원칙.

</details>

- 5대 객체지향 원칙 (**SRP, OCP, LSP, ISP, DIP**)
- **High Cohesion, Loose Coupling** 아키텍처 형성
- 인터페이스 및 다형성(Polymorphism)을 활용한 변경 파급 효과 최소화

#### 한줄 요약

- 변경 이유, 치환 가능성, 추상화가 반복 변경 경계를 통제한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Polymorphism (다형성)**: 하나의 추상 인터페이스를 통해 여러 구체 클래스가 다양한 방식으로 작동하도록 하는 객체지향의 핵심 특성으로 OCP/DIP의 기반.

</details>

```text
+------------------------------ SOLID 원칙 ------------------------------+
|                                                                        |
|        [SRP]        [OCP]        [LSP]        [ISP]        [DIP]       |
|                                                                        |
+------------------------------------------------------------------------+
```

선의 의미: 5가지 원칙(SRP, OCP, LSP, ISP, DIP)이 유기적으로 조합되어 고품질 객체지향 설계 아키텍처를 지탱하는 구조.

| 약 어 | 원칙 명칭 | 핵심 정의 및 대표적 예시 |
|:---|:---|:---|
| **S** | **Single Responsibility (SRP)** | 클래스는 단 1개의 책임만 가짐 (e.g. UserReport는 보고서 생성만, 저장/출력 분리) |
| **O** | **Open-Closed (OCP)** | 인터페이스 기반 확장은 가능하되 기존 코드 수정은 불필요 (e.g. Strategy Pattern) |
| **L** | **Liskov Substitution (LSP)** | 자식 클래스는 부모 클래스의 기대 동작 계약 준수 (e.g. 직사각형-정사각형 문제 예방) |
| **I** | **Interface Segregation (ISP)** | 거대한 1개 인터페이스보다 세분화된 N개 인터페이스 제공 (e.g. Printable, Workable) |
| **D** | **Dependency Inversion (DIP)** | 구체 클래스가 아닌 **추상화(Interface)**에 의존 (e.g. Spring DI/IoC Container) |

#### 한줄 요약

- SRP, OCP, LSP, ISP, DIP가 SOLID를 구성한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Dependency Injection (DI)**: DIP 원칙을 실현하기 위해 외부에 있는 컨테이너가 객체 간 의존 관계를 주입(Injection)해 주는 기술.

</details>

```text
┌──────────────────────────────┐
│ 설계 문제점 발생             │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. SRP: 다중 책임 분리       │
│ 2. OCP: 인터페이스 확장점 도입│
│ 3. LSP: 상위 계약 규칙 보존   │
│ 4. ISP: 인터페이스 쪼개기     │
│ 5. DIP: DI 컨테이너 연동     │
└──────────────┬───────────────┘
               ▼
   [유지보수 용이 코드 완료]
```

### 동작 원리

1. **SRP 적용**: 단일 클래스 내 데이터베이스 저장 + 리포트 렌더링 + 이메일 전송이 섞여있을 때, 3개 클래스로 분리.
2. **OCP/DIP 적용**: 구체적인 결제 PG사 클래스 직접 호출 대신 `PaymentService` 인터페이스 정의 및 구현체 바인딩.
3. **LSP/ISP 적용**: 부모 인터페이스 규칙 훼손 검증 및 클라이언트별 전용 `Printable`, `Renderable` 인터페이스 분격화.
4. **DI 연동**: Spring IoC / Spring DI 컨테이너를 통한 의존성 주입으로 런타임 결합도 완전 해제.

#### 한줄 요약

- 다섯 변경 증상에 대응하는 변경 이유 혼합부터 구체 구현 직접 의존까지의 판정이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Bad Smells in Code**: SOLID 원칙을 위반했을 때 발생하는 코드 악취 (Rigidity: 경직성, Fragility: 취약성, Immobility: 부동성).

</details>

| 원칙 위반 증상 (Code Smell) | 위반된 SOLID 원칙 | 대책 패턴 및 해결책 |
|:---|:---|:---|
| 한 클래스 수정 시 무관한 여러 기능이 함께 파손됨 | **SRP 위반** | 클래스를 변경 이유(Actor)별로 분리 |
| 신규 기능 추가 시마다 `if-else / switch` 문 대대적 수정 | **OCP 위반** | **Strategy Pattern** 적용 및 인터페이스 추출 |
| 부모 클래스 호출 시 특정 자식 객체에서 `UnsupportedOperation` 예외 발생 | **LSP 위반** | 상속 구조 재검토 및 **Composition(합성)** 전환 |
| 불필요한 메서드를 빈 형태로 강제 오버라이딩함 | **ISP 위반** | 인터페이스를 세분화하여 나눔 |
| 구체 클래스 `new ServiceImpl()`을 직접 인스턴스화 | **DIP 위반** | **Spring DI (의존성 주입)** 수용 |

#### 한줄 요약

- 고정 구현은 직접 결합, 반복 변경은 SOLID 적용이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Over-Engineering**: 실무 요구사항에 대비해 과도하게 인터페이스와 클래스를 잘게 쪼개어 가독성을 해치고 구조를 복잡하게 만드는 행위.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지나친 원칙 교조적 적용으로 인터페이스 폭증 (**Over-Engineering**) | 변경 가능성이 거의 없는 고정 로직은 단순 구현 유지 (YAGNI 원칙) | 가독성 및 복잡도 균형 |
| LSP 위반을 차단하기 위한 상속 오남용 | "상속(Inheritance)보다 **합성(Composition)**을 우대하라" 원칙 채택 | 부작용 없는 치환성 확보 |
| DIP 원칙을 적용하려 하나 객체 생성이 난해함 | **Spring Framework IoC Container / Guice** 활용 | 객체 생명주기 분리 |

> 사례: **Clean Code & Clean Architecture** 기반 SOLID 5대 원칙 리팩토링 가이드 정착

#### 한줄 요약

- 계약 시험, 응집도, 인터페이스 소유, 의존 방향을 검증한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **SOLID 적용 기준(SOLID Adoption Criteria)**: 시스템 수명주기, 요구사항 변경 빈도 및 코드 복잡도에 의거한 수립 체계.

</details>

- **SOLID 적용 기준**에 따라 장기 유지보수 및 MSA 도메인 서비스 구축 시 **SOLID 5대 원칙** 엄격 인가

#### 한줄 요약

- 반복 변경 경계와 고정 구현 여부를 함께 평가하는 것이 핵심이다.
