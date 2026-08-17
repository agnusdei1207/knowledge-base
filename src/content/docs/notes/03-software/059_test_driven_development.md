---
sidebar:
  order: 59
  label: "059. 테스트 주도 개발 (TDD)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "테스트 주도 개발 (Test-Driven Development)"
date: "2026-08-17T20:20:00+09:00"
tags:
  - "notes-software"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "125회 기출, Red-Green-Refactor 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **테스트 주도 개발(TDD, Test-Driven Development)**: 구현 코드 작성 이전에 실패하는 테스트를 먼저 작성하고, 테스트를 통과하는 최소 구현 후 리팩터링을 반복하는 개발 방법론.
- **레드-그린-리팩터(Red-Green-Refactor)**: 실패하는 테스트 작성(Red)→테스트 통과 최소 구현(Green)→코드 구조 개선(Refactor)의 TDD 핵심 반복 주기.
- **실행 가능한 명세(Executable Specification)**: 테스트 코드가 시스템의 동작 규격을 명시적으로 정의하고 실행을 통해 검증되는 살아있는 명세 역할.

</details>

- 정의/개념: Red(실패 테스트 작성)→Green(최소 구현으로 통과)→Refactor(코드 구조 개선)의 짧은 반복 주기로 설계 품질과 테스트 커버리지를 동시에 확보하는 **TDD(Test-Driven Development)**
- 배경/필요성: 구현 후 테스트 작성은 강한 결합 구조로 격리 테스트가 불가능하고 테스트 누락이 빈번하므로, **테스트 선행으로 설계 품질·결함 조기 탐지·실행 가능 명세를 동시에 확보 필수**

#### 한줄 요약

- 테스트를 먼저 작성하여 설계를 이끌고 Red-Green-Refactor 반복으로 품질과 회귀 방탄조끼를 동시에 구축

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **최소 구현(Minimal Code)**: Green 단계에서 테스트 통과를 목적으로 하드코딩을 포함한 가장 단순한 방법으로 구현하여 Baby Steps 리듬을 유지하는 원칙.
- **작동하는 깔끔한 코드(Clean Code That Works)**: 기능적으로 결함 없이 동작하면서 구조적으로 가독성·유지보수성이 높은 코드를 TDD의 최종 목표로 정의.

</details>

- **Red→Green→Refactor** 마이크로 사이클로 짧은 피드백 주기 실현
- 테스트가 설계를 이끄는 **Test-First Development**로 자연스러운 의존성 분리 달성
- 반복 누적으로 **회귀 테스트 스위트(Regression Test Suite)** 자동 구축

#### 한줄 요약

- Red-Green-Refactor 반복으로 설계를 이끌고 회귀 방탄조끼를 자동 구축

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **FIRST 원칙(FIRST Principle)**: TDD 단위 테스트가 갖춰야 할 빠른 실행(Fast)·독립성(Independent)·반복 가능성(Repeatable)·자가 검증(Self-Validating)·적시 작성(Timely) 5가지 품질 기준.

</details>

```text
[ TDD Red-Green-Refactor 구조 ]
테스트 목록 (To-do)
   │
   ▼
1. Red: 실패하는 테스트 코드 작성
   └─ 구현 코드 없어 컴파일·런타임 실패
   │
   ▼
2. Green: 최소 구현으로 테스트 통과
   └─ 하드코딩 포함 가장 단순한 방법으로 통과
   │
   ▼
3. Refactor: 테스트 통과 상태 유지하며 코드 구조 개선
   └─ 중복 제거·가독성 향상·디자인 패턴 적용
   │ 다음 To-do로 반복
   ▼
회귀 테스트 스위트 누적 완성
```

선의 의미: 단계 간 화살표는 TDD 반복 주기, 마지막 화살표는 반복이 누적되어 회귀 테스트 스위트가 구축되는 관계

| 구성요소 | 책임 |
|:---|:---|
| **테스트 목록(To-do)** | 구현할 기능·예외 케이스를 사전 열거한 작업 목록 |
| **실패 테스트(Red)** | 존재하지 않는 기능을 검증하는 의도적으로 실패하는 테스트 |
| **최소 구현(Green)** | 테스트 통과만을 목적으로 한 가장 단순한 구현 |
| **리팩터링(Refactor)** | 테스트가 보호하는 상태에서 코드 구조와 품질을 개선 |
| **회귀 테스트 스위트** | 반복 누적으로 구축된 시스템 방호 테스트 집합 |

#### 한줄 요약

- To-do 정의→Red→Green→Refactor의 반복 누적으로 설계 품질과 회귀 방탄조끼를 동시에 달성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **베이비 스텝(Baby Steps)**: 한 번에 큰 기능을 구현하려 하지 않고 작은 단위의 목표를 순차적으로 달성하여 TDD 리듬을 유지하는 점진적 구현 전략.

</details>

```text
1. To-do 목록에서 단일 소규모 목표 선택
   │
   ▼
2. Red: 해당 목표를 검증하는 실패 테스트 작성
   │
   ▼
3. Green: 최소한의 구현으로 테스트 통과 (Baby Steps)
   │
   ▼
4. Refactor: 테스트 보호 하에 코드 구조 개선
   └─ 모든 테스트 통과 상태 유지 확인
   │ To-do의 다음 항목으로 반복
   ▼
회귀 테스트 스위트 완성
```

**동작 원리**

1. **Red**: 구현 코드 없이 테스트를 먼저 작성하여 의도적 실패를 확인
2. **Green**: 하드코딩을 포함한 최소한의 방법으로 테스트를 통과시킴
3. **Refactor**: 테스트가 통과된 안전한 상태에서 코드의 중복 제거·설계 개선 수행
4. **반복**: Baby Steps 방식으로 To-do를 순차 처리하며 회귀 테스트 스위트를 누적

#### 한줄 요약

- Red→Green→Refactor의 짧고 빠른 주기로 기능을 조각 단위로 완성하며 회귀 방탄조끼를 축적

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Test-First vs Test-Last**: 구현 전 테스트 작성(Test-First)은 의존성 분리 설계를 자연스럽게 유도하지만, 구현 후 테스트(Test-Last)는 강한 결합 구조로 격리 테스트가 어렵고 테스트 누락 가능성이 높음.

</details>

| 비교 항목 | 전통적 방식 (Test-Last) | TDD (Test-First) |
|:---|:---|:---|
| 테스트 작성 시점 | 구현 완료 후 | **구현 이전** |
| 의존성 설계 | 강한 결합 구조로 격리 어려움 | **테스트 가능한 의존성 분리 설계** |
| 리팩터링 신뢰성 | 테스트 부재로 리팩터링 두려움 | **회귀 테스트 보호 하에 적극적 리팩터링** |
| 문서화 | 별도 문서·설계서 | **실행 가능 명세(Executable Specification)** |

#### 한줄 요약

- Test-First TDD는 테스트 가능한 설계를 강제하고 회귀 테스트 보호 하에 적극적 리팩터링을 가능하게 함

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TDD 도입 병목(TDD Adoption Bottleneck)**: 초기 TDD 도입 시 테스트 코드 작성으로 인한 일시적 개발 속도 저하로 팀 저항이 발생하는 현상으로, 장기적 결함 수정 비용 절감으로 상쇄됨.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| TDD 초기 도입 시 개발 속도 저하로 팀 저항 | 핵심 비즈니스 로직에 선별 적용하여 TDD 효과를 입증 | 피로도 최소화 및 TDD 효과 조기 확인 |
| Green 달성에 집착하여 완벽한 설계를 시도하다 시간 낭비 | **Baby Steps** 원칙으로 최소 구현 우선·리팩터링 단계에서 개선 | TDD 리듬 회복 |
| 외부 DB·API 의존성으로 단위 테스트 구성 불가 | **Mock/Stub(Test Double)** 적용으로 의존성 격리 | 외부 의존 없는 빠른 격리 테스트 실현 |

#### 한줄 요약

- 핵심 로직 선별 적용·Baby Steps 준수·Mock 기반 격리로 TDD 도입 장벽을 해소

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **TDD 도입 기준**: 도메인 복잡도·결함 비용·팀의 Mock 활용 역량을 기준으로 TDD 적용 범위와 강도를 결정하는 판단 기준.

</details>

- 복잡한 비즈니스 로직·높은 결함 비용 영역은 **TDD 강제 적용**, 단순 UI·일회성 스크립트는 **Test-Last** 선택

#### 한줄 요약

- 결함 비용이 높은 핵심 도메인에 TDD를 선별 적용하여 설계 품질·회귀 방탄조끼·실행 명세를 동시에 확보
