---
sidebar:
  order: 59
  label: "059. 테스트 주도 개발 (TDD)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "테스트 주도 개발 (Test-Driven Development)"
date: "2026-08-25T10:48:00+09:00"
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

- **TDD(Test-Driven Development)**: 켄트 벡(Kent Beck)이 정립한 기법으로, 실제 코드를 작성하기 전에 실패하는 단위 테스트를 먼저 작성하는 개발 방법론.
- **Red-Green-Refactor**: 실패 테스트 작성(Red) $\to$ 최소한의 통과 코드 작성(Green) $\to$ 중복 제거 및 구조 개선(Refactor)의 초단기 순환 주기.

</details>

- 정의/개념: 실제 구현 전 실패하는 테스트를 먼저 작성하고 **Red-Green-Refactor 사이클**로 설계를 발전시키는 개발 방법론
- 배경/필요성: 사후 테스트 작성 시 발생하는 **테스트 불가 스파게티 코드 양산 및 리팩터링 시 회귀 결함 공포 해결 불가**

#### 한줄 요약
- 테스트를 먼저 작성하여 설계를 주도하고 Red-Green-Refactor 반복으로 품질을 완성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **FIRST 원칙**: Fast(빠른 실행), Independent(독립성), Repeatable(반복 가능), Self-Validating(자가 검증), Timely(적시성)의 단위 테스트 5대 품질 척도.
- **실행 가능한 명세(Executable Specification)**: 테스트 코드 자체가 최신의 API 사용법과 비즈니스 요구사항을 설명하는 살아있는 문서 역할을 수행.

</details>

- **Red $\to$ Green $\to$ Refactor** 초단기(수 분 단위) 마이크로 사이클 기반 개발
- 테스트 가능한 설계를 강제하는 **Test-First Development** 및 자연스러운 결합도 완화
- 개발과 동시에 구축되는 **자동화된 회귀 방탄조끼(Regression Safety Net)** 확보

#### 한줄 요약
- Red-Green-Refactor 사이클로 설계를 이끌고 FIRST 원칙 기반의 회귀 안전망을 구축한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Baby Steps**: 한 번에 거대한 코드를 짜지 않고, 1~2줄 단위의 작은 테스트와 최소 구현을 징검다리처럼 밟아나가는 TDD 핵심 실행 원칙.

</details>

```text
[TDD Red-Green-Refactor 사이클 구조]
|-- 1. [Red 단계] 실패하는 단위 테스트 작성 (존재하지 않는 클래스/메서드 호출)
|-- 2. [Green 단계] 가장 단순하고 빠른 방법으로 테스트 통과 (가짜 구현, 상수 반환 허용)
`-- 3. [Refactor 단계] 테스트 통과를 유지하며 코드 냄새 제거
    |-- 중복 코드 제거 (DRY 원칙)
    |-- 디자인 패턴(Strategy, Factory) 적용
    `-- 객체지향 5대 원칙(SOLID) 준수
```

선의 의미: 계층 및 TDD 3단계 순환 파이프라인

| 단계 (Phase) | 상태 및 활동 | 핵심 엔지니어링 책임 |
|:---|:---|:---|
| **Red (실패)** | 컴파일 오류 또는 단언(Assertion) 실패 | 구현할 비즈니스 **요구사항의 인터페이스와 입출력 명세 확정** |
| **Green (성공)** | 단위 테스트 100% 통과 | 하드코딩을 포함하여 **가장 빠르게 테스트를 통과시키는 최소 코드 작성** |
| **Refactor (개선)** | 모든 테스트가 통과하는 안전한 상태 | 동작 변경 없이 **중복 제거, 가독성 향상, 클린 코드 구조화** |

#### 한줄 요약
- Red(실패 명세), Green(최소 구현), Refactor(구조 개선)가 3대 톱니바퀴로 맞물린다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Fake It Till You Make It**: Green 단계에서 일단 고정 상수 값을 리턴하여 테스트를 통과시킨 후, 점진적으로 일반화된 코드로 리팩토링하는 기법.

</details>

```text
구현할 기능 To-do 목록 작성 (예: 금액 계산기)
        │
   1. [Red] 1000원 입력 시 100원 할인되는 실패 테스트 작성 (`calc(1000) == 900`)
        │
   2. [Green] `return 900;` 하드코딩으로 일단 테스트 통과 (초록 불 확인)
        │
   3. [Red] 2000원 입력 시 200원 할인되는 실패 테스트 추가 (`calc(2000) == 1800`)
        │
   4. [Green] `return price * 0.9;` 일반화 공식으로 구현하여 둘 다 통과
        │
   5. [Refactor] 할인율 0.1을 `DISCOUNT_RATE` 상수로 추출 및 메서드 분리
        │
   모든 테스트 여전히 통과(Green) 확인 후 다음 To-do 항목으로 이동
```

#### 한줄 요약
- 실패 테스트 작성 → 상수 반환 Green 통과 → 일반화 테스트 추가 → 리팩토링 순으로 점진 발전한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 구현 후 테스팅(Test-Last) vs TDD(Test-First)**: 코드를 다 짜고 나서 테스트를 붙이는 방식과 테스트가 코드를 이끄는 방식의 비교.

</details>

| 비교 항목 | 전통적 개발 (Test-Last) | 테스트 주도 개발 (Test-First / TDD) |
|:---|:---|:---|
| 테스트 작성 시점 | 구현 코드 완성 후 (일정 압박 시 생략됨) | **구현 코드 작성 전 필수 선행** |
| 클래스 결합도 | 강결합 스파게티 구조 (Mocking 불가) | **테스트 가능한 느슨한 결합(DIP) 자연 유도** |
| 리팩토링 안정성 | 기존 기능 파괴 공포로 코드 수정 기피 | **회귀 테스트 슈트 보호 하에 적극적 리팩토링** |
| 산출물 성격 | 코드와 별개인 관리 안 되는 설계 문서 | **스스로 검증되는 실행 가능한 명세서** |

#### 한줄 요약
- Test-Last는 결합도가 높고 리팩토링이 두렵지만, TDD는 느슨한 결합과 적극적 코드 개선을 보장한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Mocking Overuse(과도한 모킹)**: 내부 구현 세부사항(Private 메서드, 단순 호출 횟수)까지 지나치게 Mock으로 검증하여 리팩토링할 때마다 테스트가 깨지는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| TDD 초기 도입 시 개발 리드타임 20~30% 증가 저항 | **복잡한 핵심 도메인 로직에 우선 선별 적용** | 핵심 비즈니스 결함 조기 차단 및 성공 체험 |
| 구현 세부사항에 과도하게 결합된 취약한 테스트 | **상태(State)와 행위의 결과(Outcome) 중심 검증** | 내부 리팩토링 시 테스트 깨짐 방지 |
| Green 단계에서 완벽한 설계를 하려다 리듬 상실 | **Baby Steps 준수 (일단 통과시키고 Refactor에서 개선)** | TDD 고유의 개발 리듬 및 집중력 유지 |
| DB 및 외부 API 연계 시 단위 테스트 불가 | **Repository 인터페이스 분리 및 Mockito/Test Double 주입** | 외부 네트워크 의존 없는 1초 미만 고속 검증 |

#### 한줄 요약
- 핵심 도메인 선별 적용, 결과 중심 단언, Baby Steps 준수, Mock 격리로 생산성을 높인다.

## Ⅶ. 결론

- 복잡한 엔터프라이즈 비즈니스 로직은 **TDD의 Red-Green-Refactor 사이클과 FIRST 원칙**을 기본 개발 표준으로 채택하여 결함 없는 클린 코드와 회귀 방탄망 동시 확립

#### 한줄 요약
- TDD는 단순한 테스트 기법이 아니라, 테스트를 통해 인터페이스와 아키텍처를 진화시키는 최고의 객체지향 설계 실천법이다.