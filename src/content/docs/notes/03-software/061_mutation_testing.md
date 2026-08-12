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
  priority_note: "뮤테이션은 테스트 탐지력 검증 기법"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Mutation Testing (뮤테이션 테스트, 변이 테스트)**: 원본 소스코드에 인위적인 결함(Mutant, 변이체)을 주입한 뒤 기존 단위 테스트를 수행하여, 테스트가 해당 변이체를 탐지하여 살상(Kill)하는지 측정함으로써 테스트 케이스의 신뢰도와 결함 탐지력을 평가하는 고급 화이트박스 기법.
- **Mutant (변이체)**: 원본 소스코드의 연산자나 조건문을 인위적으로 변형(e.g., `+` $\rightarrow$ `-`, `>` $\rightarrow$ `>=`)시켜 만든 결함 주입 프로그램 버전.
- **Killed vs Survived Mutant**: 변이체 실행 시 테스트가 실패하여 결함을 찾아내면 '사멸(Killed)', 변이체임에도 불구하고 테스트가 `PASS`하면 결함 탐지에 실패한 '생존(Survived)' 상태.

</details>

- 정의/개념: 원본 소스코드에 의도적인 변이체(Mutant)를 주입하여 기존 단위 테스트의 검증력 및 Assertion 유효성을 역으로 검증하는 고급 화이트박스 결함 주입 기법인 **Mutation Testing**
- 배경/필요성: 코드 커버리지(Code Coverage) 100% 달성 시에도 Assertion(단언문) 누락으로 결함을 놓치는 커버리지의 함정(Coverage Fallacy) 극복 요구성

#### 한줄 요약

- 인위적 결함 주입으로 결함 탐지력을 평가하는 변이 테스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Mutation Score (뮤테이션 점수)**: 전체 생성된 비등가 변이체(Mutants) 대비 테스트 스위트에 의해 사멸된 변이체의 백분율 비율로, 테스트 세트의 정합성을 나타내는 평가 지표.
- **Equivalent Mutant (등가 변이체)**: 소스코드를 인위적으로 변경했으나 런타임 결과나 로직상 원본 프로그램과 완벽히 동일하여 어떤 테스트로도 사멸시킬 수 없는 불사 변이체.

</details>

- 테스트 케이스 자체의 품질 및 **Fault Detection Capability (결함 탐지 능력)** 검증
- **Killed Mutant / Survived Mutant / Equivalent Mutant** 3대 상태 분류
- **Mutation Score (MS)** 정량 지표 제공 및 높은 연산 컴퓨팅 자원 오버헤드

#### 한줄 요약

- 단일 변경, 기준 검증, 원인 분류가 핵심이다.

## Ⅲ. 구조 및 연산자 (Mutation Operators)

<details><summary>핵심 용어</summary>

- **Mutation Operators (변이 연산자)**: 원본 코드에 결함을 주입하는 규칙으로 산술 연산자 교체(AOR), 관계 연산자 교체(ROR), 논리 연산자 교체(LOR) 등 포함.

</details>

```text
[원본 코드: if (a > b) return a + b;]
                   │
                   ▼ (Mutation Operator 주입)
┌────────────────────────────────────────────────────────┐
│ Mutant 1: if (a >= b) return a + b;  (ROR 변이)        │
│ Mutant 2: if (a > b)  return a - b;  (AOR 변이)        │
│ Mutant 3: if (false)  return a + b;  (UOI 변이)        │
└──────────────────────────┬─────────────────────────────┘
                           ▼
            [기존 Unit Test Suite 실행]
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
 [Test Fail: Mutant Killed (성공)]  [Test Pass: Mutant Survived (보강필요)]
```

선의 의미: 원본 코드에 AOR/ROR 변이 연산자가 결함을 주입하여 Mutant를 생성하고, 기존 Unit Test가 이를 사멸(Killed)시키는지 검증하는 아키텍처.

| 구분 변이 연산자 | 연산자 명칭 (Operator) | 결함 주입 코드 변환 예시 |
|:---|:---|:---|
| **AOR** | Arithmetic Operator Replacement | `+` $\rightarrow$ `-`, `*` $\rightarrow$ `/` (산술 연산자 변환) |
| **ROR** | Relational Operator Replacement | `>` $\rightarrow$ `>=`, `==` $\rightarrow$ `!=` (관계 연산자 변환) |
| **LOR** | Logical Operator Replacement | `&&` $\rightarrow$ `||`, `!` 제거 (논리 연산자 변환) |
| **UOI** | Unary Operator Insertion | `x` $\rightarrow$ `-x`, `x++` $\rightarrow$ `x--` (단항 연산자 변환) |
| **ABS** | Absolute Value Insertion | `x` $\rightarrow$ `Math.abs(x)` (절댓값 주입 변환) |

#### 한줄 요약

- 변이 연산자, 테스트 스위트, 세 변이 상태의 분류 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **PITest (PIT)**: Java 생태계에서 가장 널리 쓰이는 표준 바이트코드 수준의 뮤테이션 테스트 자동화 프레임워크.

</details>

```text
┌──────────────────────────────┐
│ 원본 코드 & 기존 Test 준비   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Mutation Operator 결함 주입│
│ 2. N개 Mutant 변이체 동시 생성│
│ 3. 기존 Unit Test Suite 실행  │
│ 4. Killed / Survived 판정    │
│ 5. Mutation Score (MS) 계산  │
└──────────────┬───────────────┘
               ▼
 [Survived 분석 & Test Case 보강]
```

### 동작 원리

1. **Mutant Generation**: PIT 도구가 바이트코드를 조작하여 AOR, ROR 규칙으로 수십~수백 개의 **Mutant** 주입 생성.
2. **Test Execution**: 생성된 개별 Mutant 마다 기존 단윗 테스트 세트 자동 수행.
3. **Killed / Survived 판정**: 단 하나라도 `Fail`을 일으켜 결함을 잡으면 **Killed**, 테스트가 다 통과해 버리면 **Survived**.
4. **Mutation Score 계산**: 아래 수식에 의해 정량적 결함 탐지 점수 산출 및 Survived 항목 테스트 단언문(Assertion) 보강.

$$MS = \frac{\text{Killed Mutants}}{\text{Total Mutants} - \text{Equivalent Mutants}} \times 100 (\%)$$

#### 한줄 요약

- 기준 테스트 검증부터 변이 결과 분류까지의 탐지력 평가 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Code Coverage vs Mutation Score**: Code Coverage는 라인/분기의 실행 유무(Quantity)만 측정, Mutation Score는 테스트 단언문의 정합성 및 결함 탐지력(Quality) 측정.

</details>

| 비교 항목 | Code Coverage (라인/분기 커버리지) | Mutation Score (뮤테이션 점수) |
|:---|:---|:---|
| 측정 대상 | 코드의 실행 여부 (단순 통과 관점) | **테스트 단언문(Assertion)의 결함 탐지 품질** |
| Assertion 검증 | `assert` 문이 없어도 커버리지 100% 가능 | **`assert` 문이 엉터리면 Survived 로 점수 추락** |
| 컴퓨팅 비용 | 매우 낮음 (1회 실행) | **매우 높음 (Mutant 개수 수만큼 반복 빌드/실행)**|
| 실무 유용성 | 기본적인 미실행 코드 조망 | **핵심 금융/도메인 로직의 완벽한 테스트 검증** |

#### 한줄 요약

- 실행 범위는 구조 커버리지, 탐지력은 변이 테스트로 평가한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Equivalent Mutant Problem**: 논리상 원본과 차이가 없는 등가 변이체가 생성되어 수동으로 이를 제거해야 하는 분석 오버헤드 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수천 개 Mutant 생성에 따른 극심한 빌드 시간 지연 | **PITest Incremental Analysis (변경 파일만 델타 스캔)** | 테스트 시간 대폭 단축 |
| **Equivalent Mutant (등가 변이체)** 로 인한 점수 왜곡 | PITest 서프레스 Annotations 또는 수동 등가 제거 | MS 점수 정확도 확보 |
| 전체 코드베이스 적용 시 CI 파이프라인 과부하 | 핵심 금융/계산 모듈 도메인에만 핀포인트 적용 | 효율성 극대화 |

> 사례: Java 오픈소스 및 금융권 핵심 파이낸스 엔진 대상 **PITest (PIT Mutation Testing)** 검증 정착

#### 한줄 요약

- 선택적 뮤테이션과 고위험 생존 변이 중심 보강이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **뮤테이션 테스트 도입 기준(Mutation Testing Adoption Standards)**: 시스템 안전 등급, 도메인 중요도 및 CI/CD 컴퓨팅 리소스 쿼터에 의거한 체계.

</details>

- **뮤테이션 테스트 도입 기준**에 따라 미션 크리티컬 결제/보안 로직 구축 시 **PITest 기반 Mutation Score 80%+** 필수 인가

#### 한줄 요약

- 고위험 코드의 생존 변이를 우선 보강하는 변이 시험 적용 기준이 핵심이다.
