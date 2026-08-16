---
sidebar:
  order: 61
  label: "061. 뮤테이션 테스트 (Mutation Testing)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "뮤테이션 테스트 (Mutation Testing)"
date: "2026-08-13T16:20:00+09:00"
tags:
  - "notes-software"
weight: 61
extra:
  question_no: "061"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "변이 테스트(Mutation Testing)는 테스트 결함 탐지력(Fault Detection Capability) 검증의 정량적 기법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Mutation Testing (MT, 변이 테스트)**: 원본 코드에 의도적 오류(Mutant)를 주입하여 단위 테스트의 결함 탐지력(Kill)을 검증하는 화이트박스 테스트 기법.
- **Mutant (변이체)**: 원본 소스코드의 연산자, 조건을 인위적으로 변경(e.g., `+` $\rightarrow$ `-`)하여 만든 결함 주입 프로그램 버전.
- **Killed vs Survived (사멸 vs 생존)**: 테스트 실패로 결함이 발견되면 '사멸(Killed)', 통과하면 '생존(Survived)'으로 판정.
- **Mutation Score (MS, 변이 점수)**: 전체 생성 변이체 중 테스트에 의해 사멸된 비율로 테스트 정합성을 나타내는 평가 지표.

</details>

- 정의: 테스트 코드의 **단언문** 유효성과 결함 탐지 능력을 역으로 검증하는 **화이트박스(White-box) 테스트** 기법.
- 배경/필요성: 높은 **코드 커버리지**만으로 단언문 탐지력 확인 불가

#### 한줄 요약
- 인위적 결함 주입 기반 테스트 결함 탐지력 검증.

## Ⅱ. 특징

- **검증 중심**: 테스트 케이스의 결함 탐지 능력(Fault Detection Capability) 검증을 통한 품질 향상.
- **변이 상태**: 사멸(Killed), 생존(Survived), 등가 변이체(Equivalent) 3단계 분류.
- **정량적 평가**: 변이 점수(MS) 제공을 통한 객관적 테스트 정합성 측정.

#### 한줄 요약
- 결함 탐지 품질 중심의 테스트 정량 평가.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Mutation Operators (변이 연산자)**: 산술(AOR), 관계(ROR), 논리(LOR) 등 결함 주입 규칙.

</details>

```text
 [원본 코드] ─── [변이 연산자]
      │                │
 [단위 시험 모음] ─ [변이체]
      │                │
      └──── [판정 결과]
```

선의 의미: 원본 코드에 변이 연산자가 결함을 주입하여 변이체(Mutant)를 생성하고, 기존 단위 테스트가 이를 사멸(Killed)시키는지 검증하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 원본 코드 | 변이 주입 전 기준 동작 제공 |
| 변이 연산자 | 산술•관계•논리 연산을 규칙에 따라 변경 |
| 변이체 | 의도적 결함이 포함된 프로그램 버전 |
| 단위 시험 모음 | 변이체별 기존 시험 실행 |
| 판정 결과 | Killed•Survived•Equivalent 상태 기록 |

#### 한줄 요약
- 변이 연산자 기반 결함 주입 및 탐지력 검증.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PITest (PIT)**: 자바 생태계 표준 바이트코드 수준 뮤테이션 테스트 자동화 프레임워크.

</details>

```text
┌──────────────────────────────┐
│ Original Code & Unit Tests   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 변이 연산자 선택          │
│ 2. 변이체 생성               │
│ 3. 단위 시험 실행            │
│ 4. 변이체 상태 판정          │
│ 5. 변이 점수 산출            │
└──────────────┬───────────────┘
               ▼
 [Analyze Survived & Reinforce Test]
```

### 동작 원리

1. **변이 연산자 선택**: 코드 특성에 맞는 결함 주입 규칙 선택.
2. **변이체 생성**: PIT가 연산자별 프로그램 버전 생성.
3. **단위 시험 실행**: 각 변이체에 기존 시험 모음 수행.
4. **변이체 상태 판정**: 실패는 Killed, 통과는 Survived 분류.
5. **변이 점수 산출**: 등가 변이체를 제외해 탐지력 계산.

$$MS = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \times 100 (\%)$$

#### 한줄 요약
- 변이 기반 테스트 탐지력 평가 프로세스.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Code Coverage vs Mutation Score**: Code Coverage는 실행 여부(Quantity), Mutation Score는 단언문의 정합성 및 결함 탐지력(Quality) 측정.

</details>

| 비교 항목 | Code Coverage (라인/분기 커버리지) | Mutation Score (뮤테이션 점수) |
|:---|:---|:---|
| 측정 대상 | 코드 실행 여부 | 테스트 단언문(Assertion) 결함 탐지 품질 |
| Assertion 검증 | 단언문 없어도 100% 가능 | 단언문 미흡 시 생존(Survived) 발생 |
| 컴퓨팅 비용 | 단일 시험 실행 중심 | 변이체별 반복 실행으로 비용 증가 |
| 실무 유용성 | 기본적인 미실행 코드 조망 | 핵심 도메인 로직 테스트 검증 |

#### 한줄 요약
- 코드 커버리지는 양적 실행, 변이 점수는 질적 탐지력 평가.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Equivalent Mutant Problem**: 로직상 원본과 차이가 없는 변이체 생성으로 인한 수동 분석 오버헤드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 시간 지연 | PITest Incremental Analysis (델타 스캔) | 테스트 시간 단축 |
| 등가 변이체(Equivalent) 점수 왜곡 | 서프레스 어노테이션 및 수동 제거 | 점수 정확도 확보 |
| CI 파이프라인 과부하 | 핵심 도메인과 변경 범위에 선별 적용 | 계산 비용 대비 탐지 가치 향상 |

> 사례: Java 오픈소스 및 금융권 핵심 파이낸스 엔진 대상 **PITest (PIT Mutation Testing)** 검증 정착

#### 한줄 요약
- 전략적 변이 테스트 적용 및 생존 변이 중심 테스트 보강.

## Ⅶ. 결론

- 핵심 결정 로직은 **변이 테스트**, 일반 경로는 **코드 커버리지** 우선 적용

#### 한줄 요약

- 결함 위험과 실행 비용에 따라 변이 시험 범위를 정하는 것이 핵심이다.
