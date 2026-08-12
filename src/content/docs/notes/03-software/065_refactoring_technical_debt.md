---
sidebar:
  order: 65
  label: "065. 소프트웨어 리팩터링•기술부채 (Refactoring Technical Debt)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "소프트웨어 리팩터링•기술부채 (Refactoring Technical Debt)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 65
extra:
  question_no: "065"
  source_status: "기출"
  source_history: "123회, 129회"
  priority: 70
  priority_note: "123•129회 반복, 구조 개선•부채 관리"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Refactoring (소프트웨어 리팩터링)**: 마틴 파울러(Martin Fowler)가 정의한 기법으로, 소프트웨어의 외부적 행위(External Behavior)는 전혀 변경하지 않고 내부 구조(Internal Structure)를 개선하여 가독성과 유지보수성을 극대화하는 코드 정제 활동.
- **Technical Debt (기술 부채)**: 워드 커닝햄(Ward Cunningham)이 금융 부채 개념에 비유한 용어로, 당장의 빠른 배포를 위해 임시방편(Quick & Dirty)으로 작성된 코드가 향후 지연 이자(Interest) 형태로 개발 생산성을 기하급수적으로 저하시키는 비용 한계.
- **Code Smell (코드 악취)**: 코드에 잠재된 심각한 설계 결함(Duplicated Code, Long Method, Large Class)을 암시하는 기교적 이상 징후.

</details>

- 정의/개념: 빠른 시장 출시(Time-to-Market)를 위해 누적된 **Technical Debt (기술 부채)**를 상환하기 위해, 애플리케이션의 외부적 동작 결과를 100% 보존하며 내부 코드를 개선하는 **Refactoring**
- 배경/필요성: 스파게티 코드로 인한 신규 기능 개발 속도 마비(유지보수 생산성 저하) 방지, 시스템 변경 내구성 및 가독성 확보 요구성

#### 한줄 요약

- 외부 동작을 보존하는 리팩터링으로 기술부채를 줄이는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Behavior-Preserving Transformation**: 리팩터링 전후에 동일한 입력값에 대해 항상 동일한 출력값과Side-effect를 보장하는 행위 보존 변환 속성.
- **Regression Safety Net**: 단위 테스트(Unit Test Suite)를 안전망으로 구축하여, 리팩터링 과정에서 기존 기능이 붕괴(Regression)되는 것을 자동 감지하는 구조.

</details>

- **Behavior-Preserving Transformation (외부 행위 완전 보존)**
- **Code Smell 제거** 및 가독성/응집도 극대화
- 자동화된 **Regression Safety Net (단위 테스트 안전망)** 필수 상주

#### 한줄 요약

- 작은 구조 변경과 회귀 테스트 안전망이 핵심이다.

## Ⅲ. 구조 및 구성요소 (Refactoring 2대 기법 & Code Smell)

<details><summary>핵심 용어</summary>

- **Extract Method / Rename Method**: 긴 메서드에서 일관된 단위 로직을 떼어내어 독립 메서드로 추출하거나, 의도가 명확하도록 이름을 재정의하는 대표적 리팩터링 패턴.

</details>

```text
[기술 부채 누적 (Code Smell 발생)]
                 │
                 ▼ (경고: Long Method, Duplicated Code)
┌────────────────────────────────────────────────────────┐
│ 1. Automated Unit Test 안전망 작동 확증                │
│ 2. Small Steps 리팩터링 수행 (Extract Method / Rename) │
│ 3. Unit Test 수시 PASS 확인 (Behavior Preserved)       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
          [Clean Code & 기술 부채 상환 완결]
```

선의 의미: Code Smell을 발견하고 단위 테스트 안전망 아래에서 Extract Method 등 소규모 리팩터링을 수행하여 Clean Code로 승화시키는 프로세스 구조.

| 구성요소 | 핵심 정의 및 대표 패턴 | 효과 및 목적 |
|:---|:---|:---|
| **Code Smell (징후)** | Duplicated Code, Long Method, Primitive Obsession, Feature Envy | 기술 부채의 존재를 암시하는 코드 이상 징후 발견 |
| **Composing Methods** | **Extract Method, Inline Method, Replace Temp with Query** | 거대 메서드를 작고 명확한 단위로 분할 정제 |
| **Moving Features** | **Move Method, Move Field, Extract Class** | 객체 간 책임을 알맞은 클래스로 옮겨 결합도 해제 |
| **Simplifying Expressions**| **Decompose Conditional, Replace Conditional with Polymorphism**| 무거운 `if-else` 분기를 다형성(Polymorphism)으로 전환 |

#### 한줄 요약

- 코드 스멜, 부채 백로그, 회귀 테스트, 리팩터링의 상환 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Technical Debt Quadrant (기술 부채 4분면)**: 마틴 파울러가 기술 부채의 원인을 4가지(Deliberate/Inadvertent $\times$ Reckless/Prudent)로 분류한 프레임워크.

</details>

```text
┌──────────────────────────────┐
│ Code Smell / 결함 징후 발견  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 단위 테스트 통과 상태 확인│
│ 2. Small Steps 단위 리팩터링 │
│ 3. 단위 테스트 PASS 재확인   │
│ 4. Git Commit (Small Commit) │
└──────────────┬───────────────┘
               ▼
 [기술 부채 원금/이자 상환 완료]
```

### 동작 원리

1. **Safety Net Check**: 코드 수정 전, 기존 단윗 테스트 세트가 100% `PASS`함을 보장.
2. **Small Steps**: 단 1개의 메서드만 추출(`Extract Method`)하거나 변수명 변경.
3. **Test Re-run**: 수정한 즉시 단윗 테스트 재구동하여 외부 행위 파손 여부 `PASS` 인가.
4. **Small Commit**: 테스트가 통과된 최적 상태에서 `git commit` 래칭 후 다음 Smell 정복.

#### 한줄 요약

- 부채 항목•이자 근거 등록부터 회귀 검증까지의 상환 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Refactoring vs Performance Optimization**: Refactoring은 가독성과 유지보수성(Clean Code) 개선 목적, Performance Optimization은 실행 속도 및 자원 효율성(Efficiency) 개선 목적.

</details>

| 비교 항목 | Refactoring (리팩터링) | Performance Optimization (성능 최적화) |
|:---|:---|:---|
| 주 주요 목적 | **코드 가독성, 응집도 상승, 기술 부채 상환**| **실행 속도, CPU/메모리 연산 오버헤드 단축** |
| 외부 행위 변경 | **절대 없음 (Behavior Preserved)** | **없음 (동일 결과 반환)** |
| 소스코드 형태 | 작고 명확하게 분할 (클래스/메서드 증가) | 때로는 가독성을 희생하여 튜닝 (알고리즘 튜닝) |
| 실행 안전망 | **단위 테스트 필수** | **성능 벤치마크 테스트 (JMH) 필수** |

#### 한줄 요약

- 잦은 변경은 점진 개선, 종료 임박은 현 상태 유지가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Boy Scout Rule (보이스카우트 원칙)**: "캠핑장을 떠날 때는 처음 왔을 때보다 더 깨끗하게 치워라"라는 구호로, 코드를 수정할 때마다 주변 작은 스멜을 조금씩 정돈하는 문화적 원칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 테스트 안전망 없이 리팩터링 수행하다 결함 폭발 | **TDD 기반 단위 테스트 100% 구축 후 리팩터링 진입** | 시스템 파손 제어 |
| 별도 대규모 리팩터링 스프린트 일정을 잡기 어려움 | **Boy Scout Rule (일상 개발 시 소규모 릴레이 개선)** | 지속적 부채 상환 |
| 일정을 앞당기기 위해 무분별한 의도적 기술 부채 발생 | **Technical Debt Backlog 작성 및 부채 이자 관리** | 명확한 기술부채 통제 |

> 사례: **SonarQube 정적 분석 + IntelliJ 자동 Refactoring Tool + Boy Scout Rule** 연동

#### 한줄 요약

- 변경 빈도, 장애 영향, 반복 검증에 기반한 점진 상환이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **기술 부채 관리 기준(Technical Debt Management Standards)**: 코드 복잡도(Cyclomatic), SonarQube 부채 지수 및 단위 테스트 커버리지에 의거한 체계.

</details>

- **기술 부채 관리 기준**에 따라 코드 유지보수성 확보 시 **Boy Scout Rule + Behavior-Preserving Refactoring** 필수 수용

#### 한줄 요약

- 미래 비용을 가장 크게 줄이는 상환 순서와 부채 대응 선택 기준이 핵심이다.
