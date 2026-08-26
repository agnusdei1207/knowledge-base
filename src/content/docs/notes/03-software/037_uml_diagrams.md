---
sidebar:
  order: 37
  label: "037. UML 다이어그램 분류•표기법"
  badge:
    text: "미출 · 50%"
    variant: note
title: "UML 다이어그램 분류•표기법 (UML Diagrams)"
date: "2026-08-27T00:20:00+09:00"
tags:
  - "notes-software"
weight: 37
extra:
  question_no: "037"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "구조•행위 다이어그램 체계 및 관계 표기법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **UML(Unified Modeling Language)**: 객체지향 소프트웨어의 산출물을 명세화, 시각화, 문서화하기 위해 OMG가 표준화한 모델링 언어.
- **OMG(Object Management Group)**: UML, CORBA, SysML 등의 개방형 객체지향 표준을 제정하고 관리하는 국제 컴퓨터 소프트웨어 컨소시엄.

</details>

- 정의/개념: 소프트웨어 시스템의 정적 구조(Structure)와 동적 행위(Behavior)를 시각화·명세화하는 **OMG 표준 모델링 언어**
- 배경/필요성: 자연어 설계서의 다의성과 주관적 해석으로 인한 **개발자 간 아키텍처 불일치 및 설계 왜곡 해결 불가**

#### 한줄 요약
- 정적 구조(7종)와 동적 행위(7종) 총 14개 다이어그램으로 시스템 설계를 표준 시각화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **구조 vs 행위 다이어그램**: 시스템의 정적 물리/논리 구성요소를 표현하는 구조 다이어그램과 시간 흐름에 따른 동적 동작을 표현하는 행위 다이어그램.
- **MDA(Model-Driven Architecture)**: 플랫폼 독립 모델(PIM)을 플랫폼 종속 모델(PSM) 및 코드로 자동 변환하는 모델 주도 개발 패러다임.

</details>

- 시스템의 시각화 관점에 따라 **정적 구조(7종)와 동적 행위(7종)의 14개 표준 다이어그램** 제공
- 객체 간 관계를 표현하는 **일반화, 실체화, 의존, 합성, 집합의 명확한 화살표 표기 규격**
- 도메인 분석부터 상세 설계, 자동 코드 생성(**MDA: Model-Driven Architecture**)까지 전주기 지원

#### 한줄 요약
- 구조와 행위 관점의 14개 도면과 표준 관계 표기법으로 설계의 일관성을 확립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **클래스 다이어그램(Class Diagram)**: 시스템의 클래스, 속성, 메서드 및 클래스 간의 정적 관계를 표현하는 대표적 구조 다이어그램.
- **시퀀스 다이어그램(Sequence Diagram)**: 객체들이 주고받는 메시지의 시간적 순서(Sequence)를 생명선(Lifeline) 위에 표현하는 행위 다이어그램.

</details>

```text
[UML 2.x 다이어그램 14종 분류 체계]
|-- 구조 다이어그램 (Structural Diagrams: 7종 - 정적 뼈대)
|   |-- 클래스 (Class), 객체 (Object), 패키지 (Package)
|   |-- 컴포넌트 (Component), 복합체 구조 (Composite Structure)
|   `-- 배치 (Deployment), 프로파일 (Profile)
`-- 행위 다이어그램 (Behavioral Diagrams: 7종 - 동적 실행)
    |-- 유스케이스 (Use Case), 활동 (Activity), 상태 머신 (State Machine)
    `-- 상호작용 다이어그램 (Interaction Diagrams: 4종)
        |-- 시퀀스 (Sequence), 통신 (Communication)
        `-- 상호작용 개요 (Interaction Overview), 타이밍 (Timing)
```

선의 의미: 계층 및 UML 2.x 상하위 다이어그램 분류

| 구성요소 | 책임 |
|:---|:---|
| 정적 구조 (7종) | **클래스·컴포넌트·배치** 등 정적 관계 표현 |
| 동적 행위 (7종) | **유스케이스·활동·상태 머신** 등 행위 표현 |
| 상호작용 (4종) | **시퀀스·통신** 등 객체 간 메시지 교환 표현 |

#### 한줄 요약
- 7종의 구조 다이어그램과 상호작용을 포함한 7종의 행위 다이어그램으로 분류된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Lifeline & Message**: 시퀀스 다이어그램에서 객체의 생존 기간을 나타내는 수직 점선(Lifeline)과 객체 간 호출을 나타내는 수평 화살표(Message).

</details>

```text
설계 대상 관점 판정 (정적 구조 표현 vs 동적 런타임 상호작용)
        │
   ┌────┴───────────────────────────┐
[정적 구조 설계]                 [동적 행위 설계]
도메인 엔티티 및 속성 도출         시나리오별 참여 객체(Lifeline) 배치
        │                                │
클래스 다이어그램 작성            시퀀스 다이어그램 작성 (동기/비동기 메시지)
        │                                │
   └────┬───────────────────────────┘
        │
   OMG 표준 관계 표기법 적용 (상속 `──▷`, 구현 `--▷`, 합성 `──◆`, 집합 `──◇`)
        │
   아키텍처 설계 검증 및 코드 구현 매핑
```

#### 한줄 요약
- 관점 판정 → 정적/동적 다이어그램 작성 → OMG 관계 표기법 적용 → 코드 매핑 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **합성 vs 집합(Composition vs Aggregation)**: 부모 객체 소멸 시 자식도 함께 소멸하는 강한 소유(합성: 검은 마름모)와 독립 생명주기를 갖는 약한 소유(집합: 빈 마름모).

</details>

| 관계 표기법 | 의미 및 결합도 | OMG 표준 화살표 표기법 | 코드 매핑 예시 |
|:---|:---|:---|:---|
| 일반화 (Generalization) | 부모 클래스를 상속받는 IS-A 관계 | 실선 + 빈 삼각형 화살표 (`──▷`) | `class Dog extends Animal` |
| 실체화 (Realization) | 인터페이스의 명세를 구현하는 관계 | 점선 + 빈 삼각형 화살표 (`--▷`) | `class ServiceImpl implements Service` |
| 의존 (Dependency) | 메서드 파라미터나 로컬 변수로 일시 참조 | 점선 + 열린 화살표 (`-->`) | `void send(Message msg)` |
| 합성 (Composition) | 생명주기를 공유하는 강한 전체-부분 관계 | 실선 + **채워진 마름모 (`──◆`)** | `class House { Room room = new Room(); }` |
| 집합 (Aggregation) | 독립적 생명주기를 갖는 약한 전체-부분 관계 | 실선 + 빈 마름모 (`──◇`) | `class Department { List<Employee> emps; }` |

#### 한줄 요약
- 일반화(상속), 실체화(구현), 의존(참조), 합성(강한소유), 집합(약한소유)으로 관계를 정밀 표현한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **모델 드리프트(Model Drift)**: 코드 변경 시 설계를 동기화하지 않아 UML 다이어그램과 실제 소스 코드가 불일치하게 되는 부패 현상.
- **DaC(Diagram-as-Code)**: 마우스 GUI 도구 대신 PlantUML, Mermaid 등 텍스트 코드로 다이어그램을 작성하여 Git 버전 관리하는 방식.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 14종 다이어그램 과도한 작성으로 문서화 오버헤드 | **애자일 모델링**: 클래스, 시퀀스, 배치의 3대 핵심 다이어그램 집중 | 설계 소통 효율 극대화 및 작성 비용 절감 |
| 코드 수정 후 다이어그램 미갱신으로 **모델 드리프트 발생** | **역공학(Reverse Engineering)** 도구 및 CI 문서 자동화 연동 | 소스 코드와 설계 다이어그램 간 100% 일치 보장 |
| GUI 도구 사용으로 인한 협업 및 버전 관리 곤란 | **Diagram-as-Code (PlantUML, Mermaid)** 표준화 | Git 기반 형상 관리 및 마크다운 문서 통합 |
| 객체 간 결합도 표기 모호성으로 인한 오구현 | **합성(`──◆`)과 집합(`──◇`) 표기 엄격 분리** | 메모리 누수 방지 및 명확한 수명주기 설계 |

#### 한줄 요약
- 핵심 도면 집중, 역공학 자동화, Diagram-as-Code(PlantUML), 표기법 엄수로 모델의 실효성을 유지한다.

## Ⅶ. 결론

- 핵심 설계는 **클래스/시퀀스**, 형상 관리는 **DaC** 선택

#### 한줄 요약
- UML은 정적 구조와 동적 행위를 표준 표기법으로 시각화하여 설계 품질과 팀 간 소통을 보증하는 객체지향 공학의 핵심 언어다.
