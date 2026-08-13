---
sidebar:
  order: 37
  label: "037. UML 다이어그램 유형 (UML Diagrams)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "UML 다이어그램 유형 (UML Diagrams)"
date: "2026-08-13T14:37:00+09:00"
tags:
  - "notes-software"
weight: 37
extra:
  question_no: "037"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "UML은 구조•행위 모델 선택의 기본 표기"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **UML (Unified Modeling Language)**: 객체지향 소프트웨어 시스템의 아키텍처, 정적 구조(Structural) 및 동적 행위(Behavioral)를 시각화하여 명세하는 표준 객체 모델링 언어 (OMG 표준).
- **Structural Diagrams (구조 다이어그램)**: 시스템의 정적(Static) 컴포넌트, 클래스, 물리 배치를 표현하는 다이어그램 체계.
- **Behavioral Diagrams (행위 다이어그램)**: 시스템 내 동적(Dynamic) 객체 간 메시지 흐름, 상태 변화 및 작업 시퀀스를 표현하는 다이어그램 체계.

</details>

- 정의/개념: 시스템의 정적 아키텍처 및 동적 실행 행위를 OMG 표준 시각 표기법(Graphical Notation)으로 추상화 표현하는 객체지향 설계 언어인 **UML (Unified Modeling Language)**
- 배경: 관점과 표기 규칙이 다르면 이해관계자 간 **설계 해석 불일치** 발생

#### 한줄 요약

- 구조•행위•상호작용을 표준 기호로 구분하는 UML이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **OMG (Object Management Group)**: UML, CORBA 등의 객체지향 기술 국제 표준 사양을 제정 관리하는 컨소시엄.
- **Sequence Diagram**: 객체들 간에 주고받는 메시지(Message) 송수신 순서를 시간의 흐름(Time Sequence)에 따라 시각화하는 핵심 상호작용 다이어그램.

</details>

- 정적(Structure)과 동적(Behavior) 2대 관점 14가지 다이어그램 제공
- 아키텍처 가시성 제공 및 MDA (Model Driven Architecture) 자동 코드 생성 호환성
- 직관적 가독성 및 **OMG 국제 표준 표기법** 준수

#### 한줄 요약

- 다중 관점 통합, 방법론 독립성, 모델 기준선, 정합성을 함께 관리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Class Diagram**: 시스템의 정적 구조를 구성하는 클래스, 속성(Attribute), 메서드(Method) 및 관계(Association, Aggregation, Composition, Generalization)를 시각화하는 대표적 구조 다이어그램.

</details>

```text
                         [UML 다이어그램]
                          /             \
              [구조 다이어그램]     [행위 다이어그램]
                                          |
                                [상호작용 다이어그램]
```

선의 의미: UML 2.0 기준 14가지 다이어그램이 크게 정적 Structure와 동적 Behavior 분류로 나뉘며, Interaction Diagram은 Behavior 하위에 속함.

| 구성요소 | 책임 |
|:---|:---|
| UML 다이어그램 | 표준 모델 요소와 관계의 전체 집합 제공 |
| 구조 다이어그램 | 클래스•컴포넌트•배치 등 **정적 구조** 표현 |
| 행위 다이어그램 | 상태•활동•유스케이스 등 동적 행위 표현 |
| 상호작용 다이어그램 | 행위 하위에서 **메시지 교환**과 순서 표현 |

#### 한줄 요약

- UML을 구조 다이어그램, 행위 다이어그램, 상호작용 다이어그램으로 분류한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Generalization vs Realization**: Generalization은 일반화/상속(IS-A), Realization은 인터페이스의 구체화/구현 관계.

</details>

```text
┌──────────────────────────────┐
│ 모델링할 설계 질문         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 정적•동적 관점 판정     │
│ 2. 구조 다이어그램 작성     │
│ 3. 행위 다이어그램 작성     │
│ 4. 관계 표기법 정립        │
└──────────────┬───────────────┘
               ▼
       [UML 청사진 완성]
```

### 동작 원리

1. **정적·동적 관점 판정**: 도표화 대상이 데이터/클래스 구조(Static)인지 런타임 이벤트(Dynamic)인지 구분.
2. **구조 다이어그램 작성**: Class Diagram을 통해 필드, 메서드, 관계(Generalization/Composition) 작성.
3. **행위 다이어그램 작성**: Sequence Diagram을 통해 Lifeline 및 synchronous/asynchronous 메시지 호출 정의.
4. **관계 표기법 정립**: Aggregation(채워지지 않은 다이아몬드) vs Composition(검은 다이아몬드) 등 엄격 표기 준수.

#### 한줄 요약

- 정적•동적 관점 판정과 메시지 교환 중심 판정으로 UML 유형을 선택한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Composition vs Aggregation**: Composition은 전체-부분이 생명주기를 공유하는 강한 결합(포함 관계 소멸 시 부분도 소멸), Aggregation은 생명주기가 독립적인 약한 집합 관계.

</details>

| 관계 표기법 | 의미 | 선 형태 및 화살표 |
|:---|:---|:---|
| **Generalization (상속)** | 부모-자식 간 IS-A 관계 | 실선 + 빈 삼각형 화살표 (`──▷`) |
| **Realization (구현)** | 인터페이스-구현체 간 관계 | 점선 + 빈 삼각형 화살표 (`--▷`) |
| **Dependency (의존)** | 파라미터/지역변수로 연관 | 점선 + 화살표 (`-->`) |
| **Composition (합성)** | 생명주기 공유 포함 관계 | 실선 + **검은 다이아몬드** (`──◆`) |
| **Aggregation (집합)** | 생명주기 독립 포함 관계 | 실선 + 빈 다이아몬드 (`──◇`) |

#### 한줄 요약

- 소유•배치는 구조, 상태•메시지는 행위가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Model-Implementation Drift**: 시스템 수정 진행 중 UML 설계서가 업데이트되지 않아 실제 코드와 UML 간 불일치가 유발되는 설계 부패.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| UML 문서 작성이 과도하여 실제 코딩 속도 지연 | **Agile Modeling (필요 최저한의 Class/Sequence만 기재)** | 커뮤니케이션 효율화 |
| 코드와 UML 간 불일치 발생 (**Model Drift**) | **Reverse Engineering (역공학 툴)** 및 PlantUML CI 연동 | 코드-모델 동기화 유지 |
| 복잡한 텍스트 기반 다이어그램 툴 관리 난항 | **PlantUML / Mermaid** 텍스트 기반 코드형 다이어그램(Diagram-as-Code) 채택 | Git 버전 관리 가능 |

> 사례: GitHub Actions 내 **PlantUML** 자동 빌드를 통합하여 Markdown 문서 내 UML 자동 렌더링 정착

#### 한줄 요약

- 모델링 규약, 공통 식별자, 코드 변경 연결로 구현과 모델을 동기화한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **UML 선택 기준(UML Diagram Selection Criteria)**: 아키텍처 레이어, 런타임 제어 복잡도 및 동적/정적 모듈성에 따른 도면 채택 체계.

</details>

- **UML 선택 기준**에 따라 클래스 데이터 아키텍처는 **Class Diagram**, 객체 간 복잡한 비동기 호출 흐름은 **Sequence Diagram** 선택

#### 한줄 요약

- 소유•배치•상태•메시지 질문을 구분하는 것이 핵심이다.
