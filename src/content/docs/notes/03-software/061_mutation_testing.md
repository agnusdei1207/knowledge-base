---
sidebar:
  order: 61
  label: "061. 뮤테이션 테스트 (Mutation Testing)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "뮤테이션 테스트 (Mutation Testing)"
date: "2026-08-10T23:40:00+09:00"
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

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Testing (MT, 변이 테스트)**: 원본 코드에 의도적 오류(Mutant)를 주입하여 단위 테스트의 결함 탐지력(Kill)을 검증하는 화이트박스 테스트 기법.
- **Mutant (변이체)**: 원본 소스코드의 연산자, 조건을 인위적으로 변경(e.g., `+` $\rightarrow$ `-`)하여 만든 결함 주입 프로그램 버전.
- **Killed vs Survived (사멸 vs 생존)**: 테스트 실패로 결함이 발견되면 '사멸(Killed)', 통과하면 '생존(Survived)'으로 판정.
- **Mutation Score (MS, 변이 점수)**: 전체 생성 변이체 중 테스트에 의해 사멸된 비율로 테스트 정합성을 나타내는 평가 지표.

</details>

- 정의: 테스트 코드의 **단언문(Assertion)** 유효성과 결함 탐지 능력을 역으로 검증하는 **화이트박스(White-box) 테스트** 기법.
- 배경: 높은 **코드 커버리지(Code Coverage)** 달성 시에도 단언문 부재로 인한 결함 탐지 실패(**Coverage Fallacy**) 극복 필요.

#### 한줄 요약
- 인위적 결함 주입 기반 테스트 결함 탐지력 검증.

## Ⅱ. 특징

- **검증 중심**: 테스트 케이스의 결함 탐지 능력(Fault Detection Capability) 검증을 통한 품질 향상.
- **변이 상태**: 사멸(Killed), 생존(Survived), 등가 변이체(Equivalent) 3단계 분류.
- **정량적 평가**: 변이 점수(MS) 제공을 통한 객관적 테스트 정합성 측정.

#### 한줄 요약
- 결함 탐지 품질 중심의 테스트 정량 평가.

## Ⅲ. 구조 및 연산자 (Mutation Operators)

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Operators (변이 연산자)**: 산술(AOR), 관계(ROR), 논리(LOR) 등 결함 주입 규칙.

</details>

```text
[Original: if (a > b) return a + b;]
                │
                ▼ (Mutation Operator Injection)
┌──────────────────────────────────────────────┐
│ Mutant 1: if (a >= b) return a + b; (ROR)    │
│ Mutant 2: if (a > b) return a - b;  (AOR)    │
│ Mutant 3: if (False) return a + b;  (LOR)    │
└───────────────────────┬──────────────────────┘
                        ▼
            [Unit Test Execution]
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
  [Test Fail: Killed]            [Test Pass: Survived]
```

선의 의미: 원본 코드에 변이 연산자가 결함을 주입하여 변이체(Mutant)를 생성하고, 기존 단위 테스트가 이를 사멸(Killed)시키는지 검증하는 아키텍처.

| 구분 변이 연산자 | 연산자 명칭 (Operator) | 결함 주입 코드 변환 예시 |
|:---|:---|:---|
| **AOR** | Arithmetic Operator Replacement | `+` $\rightarrow$ `-`, `*` $\rightarrow$ `/` (산술 연산자 변환) |
| **ROR** | Relational Operator Replacement | `>` $\rightarrow$ `>=`, `==` $\rightarrow$ `!=` (관계 연산자 변환) |
| **LOR** | Logical Operator Replacement | `&&` $\rightarrow$ `||`, `!` 제거 (논리 연산자 변환) |
| **UOI** | Unary Operator Insertion | `x` $\rightarrow$ `-x`, `x++` $\rightarrow$ `x--` (단항 연산자 변환) |
| **ABS** | Absolute Value Insertion | `x` $\rightarrow$ `Math.abs(x)` (절댓값 주입) |

#### 한줄 요약
- 변이 연산자 기반 결함 주입 및 탐지력 검증.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **PITest (PIT)**: 자바 생태계 표준 바이트코드 수준 뮤테이션 테스트 자동화 프레임워크.

</details>

```text
┌──────────────────────────────┐
│ Original Code & Unit Tests   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Inject Mutation Operator  │
│ 2. Generate N Mutants        │
│ 3. Execute Unit Test Suite   │
│ 4. Evaluate (Killed/Survived)│
│ 5. Calculate MS              │
└──────────────┬───────────────┘
               ▼
 [Analyze Survived & Reinforce Test]
```

### 동작 원리

1. **Mutant Generation**: PIT 도구가 바이트코드를 조작하여 규칙에 따른 다수 변이체 생성.
2. **Test Execution**: 생성된 변이체별 단위 테스트 자동 수행.
3. **Killed / Survived 판정**: 테스트 실패 시 **Killed**, 통과 시 **Survived**.
4. **Mutation Score 산출**: 정량적 결함 탐지 점수 산출 및 단언문 보강.

$$MS = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \times 100 (\%)$$

#### 한줄 요약
- 변이 기반 테스트 탐지력 평가 프로세스.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Code Coverage vs Mutation Score**: Code Coverage는 실행 여부(Quantity), Mutation Score는 단언문의 정합성 및 결함 탐지력(Quality) 측정.

</details>

| 비교 항목 | Code Coverage (라인/분기 커버리지) | Mutation Score (뮤테이션 점수) |
|:---|:---|:---|
| 측정 대상 | 코드 실행 여부 | 테스트 단언문(Assertion) 결함 탐지 품질 |
| Assertion 검증 | 단언문 없어도 100% 가능 | 단언문 미흡 시 생존(Survived) 발생 |
| 컴퓨팅 비용 | 매우 낮음 | 매우 높음 (변이체별 반복 실행) |
| 실무 유용성 | 기본적인 미실행 코드 조망 | 핵심 도메인 로직 테스트 검증 |

#### 한줄 요약
- 코드 커버리지는 양적 실행, 변이 점수는 질적 탐지력 평가.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Equivalent Mutant Problem**: 로직상 원본과 차이가 없는 변이체 생성으로 인한 수동 분석 오버헤드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 시간 지연 | PITest Incremental Analysis (델타 스캔) | 테스트 시간 단축 |
| 등가 변이체(Equivalent) 점수 왜곡 | 서프레스 어노테이션 및 수동 제거 | 점수 정확도 확보 |
| CI 파이프라인 과부하 | 핵심 도메인 핀포인트 적용 | 효율성 극대화 |

> 사례: Java 오픈소스 및 금융권 핵심 파이낸스 엔진 대상 **PITest (PIT Mutation Testing)** 검증 정착

#### 한줄 요약
- 전략적 변이 테스트 적용 및 생존 변이 중심 테스트 보강.

## Ⅶ. 결론

- 미션 크리티컬 로직 대상 변이 점수 80% 이상 확보 및 지속적 테스트 케이스 보강 체계 적용.
