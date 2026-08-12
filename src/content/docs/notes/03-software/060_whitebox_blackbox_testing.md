---
sidebar:
  order: 60
  label: "060. 화이트박스•블랙박스 테스트 (White-box Black-box Testing)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "화이트박스•블랙박스 테스트 (White-box Black-box Testing)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 60
extra:
  question_no: "060"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "내부•외부 관점 테스트 선택 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **White-box Testing (화이트박스 테스트, Structural Testing)**: 소스코드의 내부 구조, 제어 흐름(Control Flow), 조건문 및 실행 경로(Path)를 투명하게 들여다보며 커버리지(Coverage)를 측정하고 테스트 케이스를 설계하는 기법.
- **Black-box Testing (블랙박스 테스트, Functional Testing)**: 소스코드의 내부 구조를 전혀 보지 않고, 시스템에 입력값(Input)을 투입하여 기대되는 출력값(Output) 사양 명세 준수 여부를 검증하는 기법.
- **Gray-box Testing (그레이박스 테스트)**: 내부 데이터 구조나 알고리즘 지식을 일부 알고 있는 상태에서 블랙박스 입출력 테스트를 결합하여 수행하는 하이브리드 검증 기법.

</details>

- 정의/개념: 소스코드 내부 구조 투명성을 기준으로 구조적 제어 경로를 들여다보는 **White-box Testing** 대 입출력 사양 명세 중심의 **Black-box Testing** 비교 체계
- 배경/필요성: 외부 입출력 성공만으로 내부 미실행 Dead Code/Infinite Loop 누락 차단, 반대로 코드 커벌리지만으로 요구사항 명세 누락(Omission Bug)을 잡아내지 못하는 한계 극복 요구성

#### 한줄 요약

- 화이트박스 테스트와 블랙박스 테스트의 서로 다른 테스트 근거를 결합하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Control Flow Graph (CFG)**: 프로그램 내부의 제어 흐름 분기(If/Switch/Loop)를 노드(Node)와 엣지(Edge)로 시각화하여 화이트박스 경로를 추출하는 그래프.
- **Specification-based Technique**: 블랙박스 테스트의 근본 사상으로, 소프트웨어 요구사항 사양서(SRS)만을 근거로 입력 조건 분할 및 테스트 케이스 설계.

</details>

- 소스코드 100% 참조 (**White-box**) 대 사용자 요구사항 명세 참조 (**Black-box**)
- 제어 흐름/데이터 흐름 검증 (**White-box**) 대 입력값 범위/상태 전이 검증 (**Black-box**)
- **Unit Test 수준 (White-box)** 대 **System / Acceptance Test 수준 (Black-box)** 주력 적용

#### 한줄 요약

- 제어 흐름, 데이터 흐름, 상태 전이를 함께 검증하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소 (기법 세부 분류)

<details><summary>핵심 용어</summary>

- **Statement/Branch/Condition Coverage**: 구문 커버리지(모든 문장 1회 이상 실행), 분기 커버리지(모든 True/False 분기 실행), 조건 커버리지(각 조건식의 True/False 분리 실행).
- **Equivalence Partitioning (동등 분할)**: 블랙박스 기법으로, 입력값 영역을 유효/무효 동등 클래스로 분할하여 각 구역 대표값 1개씩을 추출하는 설계.
- **Boundary Value Analysis (경계값 분석)**: 동등 분할의 경계선 부근(Min-1, Min, Min+1, Max-1, Max, Max+1)에서 결함 발생율이 가장 높음을 이용한 블랙박스 설계.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     Software Test Design Techniques                    │
├───────────────────────────────────┬────────────────────────────────────┤
│ White-box Testing (구조 중심)     │ Black-box Testing (명세 중심)      │
├───────────────────────────────────┼────────────────────────────────────┤
│ 1. 구문/문장 커버리지 (Statement) │ 1. 동분 분할 (Equivalence Part.)   │
│ 2. 분기/결정 커버리지 (Branch)    │ 2. 경계값 분석 (Boundary Value)    │
│ 3. 조건 커버리지 (Condition)      │ 3. 의사결정 테이블 (Decision Table)│
│ 4. 조건/결정 커버리지 (MC/DC)     │ 4. 상태 전이 테스트 (State Trans.) │
│ 5. 기본 경로 테스트 (Basis Path)  │ 5. 유스케이스 테스트 (Use Case)    │
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: 소프트웨어 테스트 기법이 화이트박스 5대 구조 기법 및 블랙박스 5대 명세 기법으로 2원화 분류되는 체계.

| 구분 분류 | 주요 테스트 기법 명칭 | 핵심 개념 및 특징 |
|:---|:---|:---|
| **White-box** | **Statement Coverage (구문)** | 코드의 모든 실행 문장을 최소 1번 이상 통과시키는 비중 측정 ($C_0$) |
| | **Branch Coverage (분기)** | 조건문의 참(True)/거짓(False) 분기를 100% 실행 검증 ($C_1$) |
| | **Condition Coverage (조건)**| 조건문 내 개별 조건식들의 T/F를 각각 최소 1회 이상 다르게 검증 ($C_2$) |
| | **MC/DC Coverage** | 항공/자동차 안전(DO-178C) 표준, 조건식들이 결과에 독립 영향을 줌 검증 |
| **Black-box** | **Equivalence Partitioning** | 입력 유효/무효 영역을 등가 집합으로 쪼개 대표 샘플 추출 |
| | **Boundary Value Analysis**| 등가 집합 경계선 부근($N-1, N, N+1$) 집중 검증 (결함 탐지율 최고) |
| | **Decision Table Testing** | 논리적 조건 결합과 그에 따른 수행 행동을 행렬 표 형태로 검증 |
| | **State Transition Testing**| 이벤트에 따라 시스템 상태가 변경되는 순서 및 전이 흐름 검증 |

#### 한줄 요약

- 테스트 케이스, 테스트 오라클, 구조 커버리지의 결합 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Basis Path Testing (기본 경로 테스트)**: McCabe의 순환 복잡도(Cyclomatic Complexity: $V(G) = E - N + 2P$)를 계산하여 소프트웨어의 독립적인 실행 경로 수를 산출하고 검증하는 화이트박스 기법.

</details>

```text
┌──────────────────────────────┐
│ 테스트 대상 및 근거 산출     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ [White-box]                  │ [Black-box]
│ 1. CFG 추출                  │ 1. 동등 분할/경계값 추출
│ 2. 순환 복잡도 V(G) 산출     │ 2. 의사결정 테이블 렌더링
│ 3. 분기/조건 커버리지 측정   │ 3. 입출력 Assertion 검증
└──────────────┬───────────────┘
               ▼
   [종합 결함 탐지 완결]
```

### 동작 원리

1. **White-box 수행**: 소스코드에서 CFG 노드/엣지 도출 $\rightarrow$ 순환 복잡도 $V(G)$ 계산 $\rightarrow$ $C_1$ 분기 커버리지 100% 지향 단위 테스트 실행.
2. **Black-box 수행**: 요구사항 명세서 수거 $\rightarrow$ 입력 파라미터 경계값($N-1, N, N+1$) 도출 $\rightarrow$ System API 엔드포인트 호출.
3. **결함 교차 수거**: 화이트박스로 미실행 Dead Code 및 분기 결함 탐지, 블랙박스로 요구사항 명세 누락 결함 조율 탐지.

#### 한줄 요약

- 블랙박스 케이스와 화이트박스 경로를 기능•구조 통합 판정으로 보강하는 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **White-box vs Black-box Comparison**: 화이트박스는 개발자 중심의 단윗 테스트에 최적, 블랙박스는 QA/사용자 중심의 시스템/인수 테스트에 최적.

</details>

| 비교 항목 | White-box Testing (화이트박스) | Black-box Testing (블랙박스) |
|:---|:---|:---|
| 테스트 근거 (Basis) | 소스코드 알고리즘, 제어 구조, 분기 | 요구사항 명세서 (SRS), 유스케이스 |
| 주 수행자 | **소프트웨어 개발자 (Developer)** | **QA 엔지니어, 최종 사용자 (User)** |
| 테스트 레벨 | **단위 테스트 (Unit Test)** | **통합/시스템/인수 테스트** |
| 주요 결함 탐지 유형| 미실행 코드, 분기 오류, 메모리 누수 | 요구사항 불일치, 입출력 오류, 기능 누락 |
| 소스코드 지식 필요성| **필수 (100% 코드 이해 필요)** | **불필요 (코드 지식 0% 가능)** |

#### 한줄 요약

- 내부 구조 관점에는 화이트박스 테스트, 외부 명세 관점에는 블랙박스 테스트가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Coverage Fallacy (커버리지의 함정)**: 코드 커버리지 100%를 달성하더라도 요구사항 누락이나 비즈니스 로직 오류를 완전히 보장하지는 못하므로 블랙박스 테스트와 수평 연동 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 구문 커버리지 100% 달성했으나 비즈니스 예외에서 에러 방출 | **Branch Coverage($C_1$) 및 MC/DC 적용 + 경계값 분석 병행** | 결함 탐지 정합성 대폭 향상 |
| 소스코드 전체 파악에 막대한 비용 소요 (White-box 한계) | 핵심 알고리즘에만 White-box 적용, 나머지는 Black-box 집중 | 테스트 비용 최소화 |
| 요구사항 명세 누락으로 인한 기능 미구현 탐지 불가 | **Use Case 기반 Black-box Acceptance Test 연동** | 명세 누락 조기 차단 |

> 사례: 자동차 안전 표준 ISO 26262 내 **MC/DC White-box 스캔 + 경계값 분석 Black-box 스위트** 동시 운용

#### 한줄 요약

- 독립 오라클, 커버리지 도구, 요구 추적성, 코드 추적성에 기반한 시험 공백 보강이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **테스트 기법 선택 기준(Test Technique Selection Standards)**: 검증 대상 테스트 레벨(Unit vs System), 코드 공개성 및 도메인 위협 수준에 의거한 체계.

</details>

- **테스트 기법 선택 기준**에 따라 단윗 테스트 시 **White-box (Branch/MC/DC)**, 시스템/인수 테스트 시 **Black-box (경계값/상태전이)** 상호 보완 채택

#### 한줄 요약

- 요구 위험과 경로 위험에 맞춰 두 시험 관점을 조합하는 것이 핵심이다.
