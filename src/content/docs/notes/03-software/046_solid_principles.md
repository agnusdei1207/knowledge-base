---
sidebar:
  order: 46
  label: "046. 객체지향 설계 원칙 SOLID"
  badge:
    text: "기출 · 70%"
    variant: note
title: "객체지향 설계 원칙 SOLID (SOLID Principles)"
date: "2026-08-26T17:17:00+09:00"
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

<details><summary>용어 설명</summary>

- **SOLID 원칙**: 로버트 C. 마틴(Uncle Bob)이 정립한 5대 객체지향 설계 원칙(SRP, OCP, LSP, ISP, DIP)의 앞 글자를 딴 약어.
- **높은 응집도 & 낮은 결합도**: 모듈 내부는 밀접한 책임에 집중(응집도)하고, 모듈 간 상호 의존성은 최소화(결합도)하는 소프트웨어 품질 기준.

</details>

- 정의/개념: 유지보수성과 확장성을 극대화하기 위해 **SRP, OCP, LSP, ISP, DIP** 5가지 책임을 규정한 객체지향 설계 원칙
- 배경/필요성: 강결합 코드 변경으로 **연쇄 부수효과·재사용 제약**

#### 한줄 요약
- 책임 분리와 추상화 의존으로 높은 응집도와 낮은 결합도를 달성하는 5대 객체지향 설계 원칙이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SRP (Single Responsibility)**: 단일 책임 원칙 - 클래스는 단 하나의 변경 이유(책임)만 가져야 함.
- **OCP (Open-Closed)**: 개방 폐쇄 원칙 - 확장에 열려 있고(Open), 기존 코드 수정에는 닫혀(Closed) 있어야 함.
- **LSP (Liskov Substitution)**: 리스코프 치환 원칙 - 자식 클래스는 언제나 부모 클래스를 대체 가능해야 함.
- **ISP (Interface Segregation)**: 인터페이스 분리 원칙 - 클라이언트가 사용하지 않는 메서드에 의존하지 않도록 분리.
- **DIP (Dependency Inversion)**: 의존역전 원칙 - 고수준 모듈은 저수준 모듈의 구체 클래스가 아닌 추상화(인터페이스)에 의존해야 함.

</details>

- **SRP·ISP** 기반 클래스 및 인터페이스의 책임 세분화로 **높은 응집도(High Cohesion)** 확보
- **DIP·OCP** 기반 추상화 의존과 인터페이스 다형성으로 **낮은 결합도(Low Coupling)** 달성
- **LSP** 준수를 통한 상속 계층의 올바른 계약 이행 및 런타임 오류 방지

#### 한줄 요약
- SRP/ISP로 응집도를 높이고, DIP/OCP로 결합도를 낮추며, LSP로 다형성 안전성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IoC Container(Inversion of Control)**: Spring Framework 등에서 객체의 생성과 의존성 주입(DIP 실현)을 전담 관리하는 프레임워크 엔진.

</details>

```text
[SOLID 5대 원칙 상호 연계 구조]
|-- 응집도 강화 영역 (Cohesion)
|   |-- SRP (Single Responsibility: 클래스당 단일 책임 캡슐화)
|   `-- ISP (Interface Segregation: 역할별 작고 명확한 인터페이스 분리)
|-- 결합도 완화 및 확장 영역 (Coupling & Extensibility)
|   |-- DIP (Dependency Inversion: 구체 구현체가 아닌 추상 인터페이스 의존)
|   `-- OCP (Open-Closed: 전략 패턴 기반 기존 코드 무수정 신규 확장)
`-- 다형성 무결성 보장 영역 (Polymorphism Safety)
    `-- LSP (Liskov Substitution: 부모의 행위 계약을 위반하지 않는 자식 구현)
```

선의 의미: 5대 원칙 간의 품질 속성 연계 구조

| 구성요소 | 책임 |
|:---|:---|
| SRP | 클래스의 **단일 변경 이유** 유지 |
| OCP | 기존 코드 수정 없이 **기능 확장** |
| LSP | 하위 타입의 **상위 타입 계약 준수** |
| ISP | 역할별 **작은 인터페이스 분리** |
| DIP | 구체 구현 대신 **추상화 의존** |

#### 한줄 요약
- SRP/ISP는 응집도를, DIP/OCP는 결합도를, LSP는 상속의 안전성을 보장한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DI(Dependency Injection)**: 객체가 사용할 의존 객체를 직접 `new`로 생성하지 않고 외부 생성자나 프레임워크로부터 주입받는 기법.

</details>

```text
기존 레거시 코드: 주문 서비스가 결제 클래스를 직접 생성 (`new KakaoPay()`) - [DIP/OCP 위반]
        │
   [DIP 적용] 구체 결제 클래스 위에 `Payment` 추상 인터페이스 정의
        │
   [OCP 적용] `KakaoPay`, `NaverPay`, `ApplePay`가 `Payment` 인터페이스를 구현
        │
   [DI 적용] 주문 서비스는 오직 `Payment` 인터페이스만 참조하고 생성자로 주입받음
        │
   [확장 검증] 신규 결제(`TossPay`) 추가 시 주문 서비스 코드 수정 0줄로 완료
```

#### 한줄 요약
- 구체 클래스 직결 → 추상 인터페이스 추출 → 다형성 구현체 분리 → DI 주입으로 OCP를 완성한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Code Smell(코드 냄새)**: SOLID 원칙을 위반하여 향후 유지보수 장애를 초래할 가능성이 높은 나쁜 코드 패턴.

</details>

| 위반 냄새 (Code Smell) | 위반된 SOLID 원칙 | 올바른 리팩토링 해결책 |
|:---|:---|:---|
| 수천 줄의 God Object 클래스 | **SRP 위반** | 책임별 세부 Service/DAO 분리 |
| 기능 추가할 때마다 `if-else / switch` 수정 | **OCP 위반** | **전략 패턴 (Strategy Pattern) 적용** |
| 자식 클래스가 `throw new UnsupportedException` 발생 | **LSP 위반** | **상속 대신 합성(Composition) 사용** |
| 구현하지 않는 빈 메서드가 인터페이스에 다수 존재 | **ISP 위반** | 역할 인터페이스로 잘게 분리 |
| 클래스 내부에서 `new` 키워드로 하위 객체 직접 생성 | **DIP 위반** | **생성자 주입 (Constructor Injection) 전환** |

#### 한줄 요약
- if-else 분기는 OCP, 빈 메서드는 ISP, 자식 예외는 LSP, new 직접 생성은 DIP를 적용해 해결한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **YAGNI(You Aren't Gonna Need It)**: 실제로 요구사항이 발생하기 전에는 불필요한 과도한 추상화나 인터페이스를 미리 만들지 말라는 원칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 변경 가능성 없는 단순 로직에 과도한 인터페이스 생성(**오버 엔지니어링**) | **YAGNI 원칙 준수** 및 구현체 1개일 때는 인터페이스 생략 | 코드 복잡도 및 학습 비용 절감 |
| 잘못된 상속으로 인한 LSP 위반 및 부모 계약 파괴 | **"상속보다는 합성(Composition over Inheritance)"** 원칙 | 런타임 사이드 이펙트 원천 차단 |
| DIP 적용 시 객체 조립 및 라이프사이클 관리 복잡 | **Spring IoC Container** 기반 자동 빈(Bean) 주입 활용 | 비즈니스 로직과 객체 생성 책임 완전 분리 |
| 단위 테스트 작성이 불가능한 강결합 구조 | **DIP 인터페이스 기반 Mock/Stub 주입 테스트** | 테스트 커버리지 90% 이상 달성 |

#### 한줄 요약
- YAGNI 과잉 방지, 상속 대신 합성, Spring IoC 활용, Mock 테스트 주입으로 설계를 완성한다.

## Ⅶ. 결론

- 객체 설계는 **SOLID 5대 원칙**, 결합 완화는 **DI** 선택

#### 한줄 요약
- SOLID는 객체 간 결합도를 낮추고 응집도를 높여 변화에 빠르고 안전하게 적응할 수 있게 하는 객체지향 설계의 표준 원칙이다.
