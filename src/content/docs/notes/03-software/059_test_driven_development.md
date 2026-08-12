---
sidebar:
  order: 59
  label: "059. 테스트 주도 개발 TDD (Test-Driven Development)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "테스트 주도 개발 TDD (Test-Driven Development)"
date: "2026-08-10T23:40:00+09:00"
tags:
  - "notes-software"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, 테스트 우선 개발 순환"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Test-Driven Development (TDD, 테스트 주도 개발)**: 켄트 백(Kent Beck)이 정립한 익스트림 프로그래밍(XP)의 실천법으로, 실제 코드를 작성하기 전에 실패하는 단윗 테스트(Red)를 먼저 작성하고, 이를 통과하는 최소한의 코드(Green)를 작성한 뒤, 리팩터링(Refactor)을 반복하는 소프트웨어 개발 기법.
- **Red-Green-Refactor Cycle**: TDD의 3단계 핵심 마이크로 피드백 루프 (Red: 실패하는 테스트 작성 $\rightarrow$ Green: 최소한의 코드로 통과 $\rightarrow$ Refactor: 중복 제거 및 가독성 개선).
- **Executable Specification (실행 가능한 명세)**: 작성된 단위 테스트 코드가 그 자체로 소프트웨어의 요구사항 사양서(Specification) 역할을 수행하는 특성.

</details>

- 정의/개념: "실패하는 테스트 작성(Red) $\rightarrow$ 통과하는 최소 구현(Green) $\rightarrow$ 코드 리팩터링(Refactor)"의 짧은 반복 주기를 통해 피드백을 극대화하는 소프트웨어 개발 방법론인 **Test-Driven Development (TDD)**
- 배경/필요성: 구현 완결 후 사후 테스트(Test-Last) 작성 시 발생하는 테스트 누락, 과도한 결합도(High Coupling) 및 리팩터링에 대한 공포(Fear of Change) 극복 요구성

#### 한줄 요약

- 실패 시험과 최소 구현 및 리팩터링을 반복하는 테스트 주도 개발이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Minimal Code (최소 구현)**: Red 테스트를 통과시키기 위한 가장 작고 단순한 하드코딩 수준의 코드만 빠르게 작성하는 원칙.
- **Clean Code That Works**: 론 제프리스(Ron Jeffries)가 말한 TDD의 목표로, "작동하는 깔끔한 코드"를 얻기 위해 설계 품질과 동작 정합성을 동시에 달성하는 속성.

</details>

- **Red $\rightarrow$ Green $\rightarrow$ Refactor** 3대 핵심 마이크로 서클
- 테스트가 설계를 주도하는 **Test-First Development**
- **Executable Specification** 및 **Regression Test Suite (회귀 테스트 세트)** 자동 구축

#### 한줄 요약

- 실행 가능한 명세, 회귀 테스트, 리팩터링이 핵심이다.

## Ⅲ. 구조 및 구성요소 (TDD 3단계 사이클)

<details><summary>핵심 용어</summary>

- **FIRST Principle**: TDD 단위 테스트 작성을 위한 5가지 대원칙 (Fast: 빠름, Independent: 독립적, Repeatable: 반복 가능, Self-Validating: 자가 검증, Timely: 적시성).

</details>

```text
       ┌──────────────────────────────┐
       │     1. RED (실패 테스트)     │
       └──────────────┬───────────────┘
                      │ (테스트 실패 확인)
                      ▼
       ┌──────────────────────────────┐
       │    2. GREEN (최소 코드 통과) │
       └──────────────┬───────────────┘
                      │ (테스트 통과 확인)
                      ▼
       ┌──────────────────────────────┐
       │  3. REFACTOR (구조 리팩터링) │
       └──────────────┬───────────────┘
                      │ (모든 테스트 유지)
                      └───────────────┘ (반복 순환)
```

선의 의미: RED(실패 테스트) $\rightarrow$ GREEN(최소 코드 구현) $\rightarrow$ REFACTOR(구조 개선)가 1개 요구사항 메서드 단위로 수 분 내에 반복 순환(Loop)되는 체계.

| TDD 3단계 | 주요 역할 및 액션 | 주의사항 및 지침 |
|:---|:---|:---|
| **1. RED (실패)** | 요구사항을 표현하는 **실패하는 단위 테스트** 작성 | 구현체가 없으므로 반드시 컴파일/Assertion 에러 발생 |
| **2. GREEN (성공)** | 테스트를 통과시키는 **최소한의 소스코드(Minimal Code)** 작성| 죄책감 없이 하드코딩이나 삼항연산자로 일단 통과 |
| **3. REFACTOR (개선)**| 통과된 안전 상태에서 중복 제거 및 클린 아키텍처 리팩터링 | **외부 행위(Behavior)는 변함없이 유지하며 내부 개선** |

#### 한줄 요약

- 테스트 목록, 테스트 코드, 대상 코드, 테스트 실행기, 회귀 테스트 모음의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Baby Steps**: TDD에서 한 번에 거대한 기능을 테스트하려 하지 않고, 가장 작은 단위의 요구사항 포스트잇(Test List)을 쪼개어 단계별로 정복하는 개발 방식.

</details>

```text
┌──────────────────────────────┐
│ 테스트 목록 (Test List) 작성 │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Red: 실패하는 Test 작성   │
│ 2. Green: 최소 코드로 통과   │
│ 3. Refactor: 코드 깔끔히 정리│
│ 4. Test Suite 커버리지 누적  │
└──────────────┬───────────────┘
               ▼
   [설계 내구성 완성]
```

### 동작 원리

1. **Test List 작성**: 구현해야 할 기능들의 작은 단위 테스트 목록 나열.
2. **RED**: 목록 중 1개 선택 후 실패하는 `assertEq()` 단위 테스트 작성.
3. **GREEN**: 에러 메시지를 확인하고 이를 가장 빠르게 해결하는 최소 코드 작성 후 테스트 `PASS` 확인.
4. **REFACTOR**: `PASS`를 유지한 채 변수명 변경, 메서드 추출, 중복 코드를 깔끔히 제거.
5. **Next Loop**: 다음 Test List 항목으로 넘어간 후 **Baby Steps** 무한 반복.

#### 한줄 요약

- 레드-그린-리팩터의 반복 주기가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Test-First (TDD) vs Test-Last**: Test-First는 개발 전 테스트 코드가 설계를 주도하며 결합도를 낮추는 반면, Test-Last는 개발 완료 후 테스트를 끼워 맞춰 테스트 작성이 귀찮아지고 누락 폭증.

</details>

| 비교 항목 | Traditional Development (Test-Last) | Test-Driven Development (TDD) |
|:---|:---|:---|
| 테스트 작성 시점 | 소스코드 전체 개발 완결 후 | **소스코드 작성 전 (Test-First)** |
| 소스 결합도 | 강한 결합 (테스트하기 어려운 코드 발생) | **느슨한 결합 (테스트하기 쉬운 인터페이스 유도)**|
| 리팩터링 안전성 | 수정 시 부작용 공포로 리팩터링 기피 | **자동화 회귀 테스트 보장으로 자유로운 리팩터링**|
| 코드 문서화 | 별도 Word/Confluence 문서 작성 | **단위 테스트 코드 자체가 Executable Spec** |

#### 한줄 요약

- 결정적 로직에는 테스트 주도 개발, 불확실한 해법에는 탐색적 구현이 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **TDD Bottleneck**: 초기 TDD 도입 시 개발 속도가 1.5~2배 지연되는 현상이나, 중장기적으로 디버깅 시간 단축으로 전체 생산성 역전.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 초기 적응 단계에서 TDD 작성 속도가 느려 생산성 저하 | 도메인 핵심 비즈니스 로직 위주 선별 적용 | 학습 곡선 극복 |
| UI, DB 연동, 3rd Party API 테스트 작성이 너무 난해함 | **Mockito 등 Test Double 주입 및 BDD(Behavior-Driven) 병행**| 격리된 단위 테스트 가속 |
| Green 단계에서 너무 거대한 로직을 작성하려 함 | **Baby Steps 원칙 (하드코딩 수준부터 출발)** 준수 | TDD 리듬(Rhythm) 유지 |

> 사례: **JUnit 5 + AssertJ + Mockito** 기반 TDD 실천 체계 정착

#### 한줄 요약

- 공개 동작, 리팩터링 내성, 테스트 가능성 중심의 시험 설계가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **TDD 도입 수립 기준(TDD Adoption Standards)**: 시스템 도메인 복잡도, 유지보수 수명 및 팀 단위 테스트 자동화 숙련도에 의거한 체계.

</details>

- **TDD 도입 수립 기준**에 따라 장기 운용 핵심 비즈니스 로직 구현 시 **Red-Green-Refactor 기반 TDD** 필수 수용

#### 한줄 요약

- 규칙의 결정성과 격리 가능성에 따른 TDD 적용 기준이 핵심이다.
