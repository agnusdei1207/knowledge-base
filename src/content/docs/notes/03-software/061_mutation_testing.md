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

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Testing (변이 테스트)**: 원본 코드에 의도적 오류(Mutant)를 주입하고 단위 테스트가 이를 탐지(Kill)하는지 검증하여 테스트 스위트의 결함 탐지력을 평가하는 화이트박스 기법.
- **Mutant (변이체)**: 원본 소스코드의 연산자나 조건을 인위적으로 변경(e.g., `+` $\rightarrow$ `-`)하여 만든 결함 주입 프로그램 버전.
- **Killed vs Survived Mutant**: 테스트 실패로 결함이 발견되면 '사멸(Killed)', 통과하면 '생존(Survived)'으로 판정하는 상태.

</details>

- 정의: 원본 소스코드에 의도적인 변이체(Mutant)를 주입하여 테스트 케이스의 Assertion(단언문) 유효성 및 결함 탐지 능력을 역으로 검증하는 화이트박스 기법.
- 배경: 높은 코드 커버리지(Code Coverage) 달성 시에도 Assertion 부재로 인해 발생하는 결함 탐지 실패(Coverage Fallacy) 극복 필요.

#### 한줄 요약

- 인위적 결함 주입으로 결함 탐지력을 평가하는 변이 테스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Score (MS)**: 전체 생성 변이체 중 테스트에 의해 사멸(Killed)된 비율로 테스트 정합성을 나타내는 평가 지표.
- **Equivalent Mutant (등가 변이체)**: 로직상 원본과 결과가 동일하여 어떤 테스트로도 사멸시킬 수 없는 불사 변이체.

</details>

- 결함 탐지 능력(Fault Detection Capability) 검증을 통한 테스트 품질 향상.
- Killed/Survived/Equivalent 3단계 변이 상태 분류 체계.
- 정량 지표(MS) 제공 및 연산 자원 오버헤드 발생.

#### 한줄 요약

- 단일 변경, 기준 검증, 원인 분류가 핵심이다.

## Ⅲ. 구조 및 연산자 (Mutation Operators)

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Operators (변이 연산자)**: 결함 주입 규칙으로 산술(AOR), 관계(ROR), 논리(LOR) 등 포함.

</details>

```text
[원본: if (a > b) return a + b;]
                │
                ▼ (변이 연산자 주입)
┌──────────────────────────────────────────────┐
│ 변이체 1: if (a >= b) return a + b; (관계변이) │
│ 변이체 2: if (a > b) return a - b;  (산술변이) │
│ 변이체 3: if (거짓) return a + b;   (논리변이) │
└───────────────────────┬──────────────────────┘
                        ▼
            [기존 단위 테스트 실행]
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 [테스트 실패: 사멸]              [테스트 통과: 생존]
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

<details><summary>핵심 용어 (Key Terminology)</summary>

- **Mutation Testing Adoption Standards**: 도메인 중요도 및 자원 쿼터에 기반한 변이 시험 적용 표준.

</details>

- 미션 크리티컬 로직 대상 변이 테스트 점수 80% 이상 확보 및 지속적 테스트 케이스 보강 체계 적용.
