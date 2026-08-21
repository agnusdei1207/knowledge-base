---
sidebar:
  order: 20
  label: "020. 오토마타 이론: DFA•NFA (Automata Theory)"
  badge:
    text: "미출 · 30%"
    variant: note
title: "오토마타 이론: DFA•NFA (Automata Theory)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-basic-theory"
weight: 20
extra:
  question_no: "020"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "정규•형식 언어를 포괄하는 오토마타 정본"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **유한 오토마타(Finite Automaton)**: 유한한 개수의 상태와 입력 기호에 따른 전이 함수를 통해 정규 언어(Regular Language)의 수용 여부를 판정하는 추상 계산 기계 모델.
- **DFA(Deterministic Finite Automaton)**: 주어진 현재 상태와 입력 기호에 대해 전이할 수 있는 다음 상태가 오직 하나로 결정론적으로 정의되는 유한 상태 기계.
- **NFA(Nondeterministic Finite Automaton)**: 하나의 상태와 입력 기호에 대해 여러 개의 다음 상태 전이 또는 빈 문자열($\varepsilon$) 전이를 허용하는 비결정론적 상태 기계.

</details>

- 정의/개념: 유한 상태 집합과 입력 기호별 전이 함수 $\delta$를 통해 입력 문자열이 정규 문법(Regular Grammar)에 부합하는지 판정하는 **형식 언어 인식기 모델**
- 배경/필요성: 컴파일러 어휘 분석기(Lexer), 정규식 엔진, 네트워크 프로토콜 상태 머신 등에서 결정론적이고 무오류의 텍스트 패턴 매칭 체계 필요

#### 한줄 요약

- 입력 알파벳 $\Sigma$에 대한 상태 전이 함수 $\delta(q, a)$의 결정적/비결정적 매핑을 통해 정규 언어의 수용 여부를 판정

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **정규 언어(Regular Language)**: 유한 오토마타(DFA/NFA) 또는 정규 표현식(Regular Expression)으로 정확히 표현 및 인식 가능한 형식 언어.
- **부분집합 구성법(Subset / Powerset Construction)**: $N$개의 상태를 가진 NFA를 최대 $2^N$개의 상태를 가진 등가의 DFA로 결정화(Determinization) 변환하는 알고리즘.
- **언어 인식 등가성(Expressive Equivalence)**: DFA와 NFA가 인식할 수 있는 정규 언어의 집합과 표현 능력이 수학적으로 완벽히 일치하는 성질.

</details>

![NFA 상태 수와 DFA 결정화 상태 수 상한을 비교한 차트](/study/diagrams/automata-subset-growth.svg)

> NFA 상태가 1개에서 5개로 늘 때 원래 상태 수는 1→5지만 부분집합 결정화의 이론적 상한은 2→32로 지수 증가함

- 유한한 메모리(상태)만을 사용하여 입력 문자열을 $O(n)$ 선형 시간에 스캔하는 **순차적 스트림 처리**
- Subset Construction 알고리즘을 통해 상호 변환 가능하며 **DFA와 NFA의 언어 표현력은 완벽히 등가**
- DFA는 문자당 $O(1)$ 즉시 전이 속도를 보장하나 최악 $O(2^{|Q|})$ **상태 폭증(State Explosion)** 가능성 상존

#### 한줄 요약

- Subset Construction 알고리즘으로 NFA $\rightarrow$ DFA 변환이 가능하며, 두 오토마타의 정규 언어 인지 능력은 등가

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **5-튜플 $(Q, \Sigma, \delta, q_0, F)$**:
  - $Q$: 유한 상태 집합 (Finite Set of States).
  - $\Sigma$: 입력 알파벳 집합 (Input Alphabet).
  - $\delta$: 상태 전이 함수 ($\text{DFA: } Q \times \Sigma \to Q, \text{ NFA: } Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$).
  - $q_0$: 시작 상태 ($q_0 \in Q$).
  - $F$: 최종 수용 상태 집합 ($F \subseteq Q$).

</details>

```text
[ 유한 오토마타 5-튜플 아키텍처 ]
┌──────────────────────────────┐
│ 상태 집합 Q (Finite States)  │ ── {q0, q1, q2,.. qk}
├──────────────────────────────┤
│ 입력 알파벳 Σ (Alphabet)     │ ── 유효 입력 심볼 집합 {0, 1} 또는 ASCII
├──────────────────────────────┤
│ 전이 함수 δ (Transition)     │ ── DFA: δ(q, a) = p / NFA: δ(q, a) = {p1, p2}
├──────────────────────────────┤
│ 시작 상태 q0 (Initial State) │ ── 머신 가동 시 최초 진입 상태
├──────────────────────────────┤
│ 수용 상태 집합 F (Accepting) │ ── 입력 종료 시 도달하면 'Accept' 판정
└──────────────────────────────┘
```

선의 의미: 유한 상태, 입력 알파벳, 전이 규칙, 시작 및 수용 상태 간의 5-튜플 수학적 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 상태 집합 Q | 기계가 가질 수 있는 유한한 상태 집합 정의 |
| 입력 알파벳 Σ | 처리 가능한 유효 입력 기호 집합 정의 |
| 전이 함수 δ | 현재 상태와 입력 기호를 다음 상태로 매핑 |
| 시작 상태 q0 | 문자열 처리를 시작하는 최초 진입 상태 지정 |
| 수용 상태 집합 F | 입력 종료 후 문자열 수용 여부를 판정하는 상태 집합 |

#### 한줄 요약

- $M=(Q,\Sigma,\delta,q_0,F)$로 상태•입력•전이•시작•수용 조건을 정의

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **$\varepsilon$-Closure(엡실론 폐쇄)**: NFA에서 어떠한 입력 기호도 소비하지 않고 $\varepsilon$-전이만을 따라 도달할 수 있는 모든 상태들의 집합.

</details>

```text
입력 문자열 W = a1 a2.. an
   │
   ▼
[ 1. 초기 상태 설정 ] : DFA: q = q0 / NFA: S = ε-Closure(q0)
   │
   ▼
입력 기호 ai 존재 여부 검사
├─ 심볼 잔여
│  │
│  ▼
│  [ 2. 입력 기호 소비 및 전이 ] : DFA: q = δ(q, ai) / NFA: S = ε-Closure(δ(S, ai))
│  │
│  └─ 다음 기호 검사로 반복
└─ 입력 소진 (EOF)
   │
   ▼
[ 3. 수용 상태 판정 ]
├─ DFA: q ∈ F  / NFA: S ∩ F ≠ ∅  ⟹  [ Accept (문자열 수용) ]
└─ DFA: q ∉ F  / NFA: S ∩ F = ∅  ⟹  [ Reject (문자열 거부) ]
```

**동작 원리** 1. **초기 상태 설정**: DFA는 시작 상태 $q_0$를, NFA는 $q_0$의 $\varepsilon$-폐쇄 집합을 현재 활성 상태로 초기화
2. **입력 기호 소비 및 전이**: 입력 스트림에서 기호를 하나씩 읽으며 전이 함수 $\delta$를 적용하여 다음 상태(또는 상태 집합) 갱신
3. **수용 상태 판정**: 입력 문자열을 모두 소비한 후 최종 상태가 수용 상태 $F$에 포함되는지(NFA는 교집합 존재 여부) 확인하여 수용/거부 확정

#### 한줄 요약

- 입력 기호마다 상태를 갱신하고, 입력 소진 뒤 현재 상태와 수용 상태의 교집합으로 수용 여부를 판정

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DFA vs NFA 매핑 차이**:
  - DFA: $\delta: Q \times \Sigma \to Q$ (단일 상태, 직관적 구현, 상태 폭증 위험).
  - NFA: $\delta: Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$ (멱집합 다중 상태, 설계 용이, 런타임 추적 비용).

</details>

| 비교 항목 | DFA (Deterministic) | NFA (Nondeterministic) |
|:---|:---|:---|
| 적용 기준 | 컴파일러 Lexer 및 고속 고정 패턴 매칭 시 | 정규식(Regex) 파싱 및 문법 모델링 시 |
| 핵심 특징 | 각 입력마다 **단일 상태 전이** 보장 ($O(1)$) | **$\varepsilon$-전이** 및 다중 상태 분기 허용 |
| 한계 및 위험 | 복잡한 정규식 변환 시 **상태 폭증($O(2^N)$)** | 매 단계 다중 상태 추적 오버헤드 ($O(N^2)$) |

#### 한줄 요약

- DFA는 기호마다 단일 상태를 갱신하고, NFA는 상태 집합과 엡실론 폐쇄를 추적

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ReDoS(Regular Expression Denial of Service)**: NFA 백트래킹 엔진의 지수적 역추적 취약점을 악용하여 CPU 사용률을 100%로 고갈시키는 공격.
- **Hopcroft 상태 최소화(Minimization)**: DFA의 동치 상태(Equivalent States)를 병합하여 상태 수가 가장 적은 유일한 최소 DFA를 도출하는 $O(N \log N)$ 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NFA 결정화 시 발생하는 **상태 폭증(State Explosion)** | **Hopcroft 상태 최소화** 및 Lazy DFA(지연 결정화) 적용 | 전이표 메모리 최소화 및 상태 압축 |
| 악성 입력에 의한 백트래킹 엔진의 **ReDoS 공격** | DFA 기반 선형 엔진(RE2, Rust Regex) 및 매칭 타임아웃 | $O(N)$ 선형 시간 보장 및 **ReDoS 차단** |
| 다중 정규식 패턴 간 **토큰 우선순위 충돌** | 수용 상태에 규칙 순서 기반 **우선순위 가중치** 부여 | Lexer의 결정적 최장 일치(Longest Match) 보장 |
| NFA의 **$\varepsilon$-전이 연쇄** 기반  인한 수용 판정 누락 | 상태 전이 전후 **$\varepsilon$-Closure 집합 연산** 정밀 수행 | NFA 시뮬레이션의 수학적 정합성 확보 |

#### 한줄 요약

- 상태 폭증은 Hopcroft 최소화나 Lazy DFA로 억제하고, 백트래킹 엔진은 RE2 같은 선형 시간 DFA로 교체해 ReDoS를 차단하며, 토큰 충돌은 규칙 순서 우선순위로 해결한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **어휘 분석 엔진 현대화**: 프로덕션 컴파일러(LLVM/Clang) 및 보안 필터(WAF)는 NFA의 간결한 정규식 표현을 파싱한 후 Lazy DFA 또는 최소 DFA로 컴파일하여 초고속 패턴 매칭을 실현.

</details>

- 고속 토큰 매칭은 **DFA**, 동적 정규식 파싱은 **NFA 및 지연 결정화(Lazy DFA)** 선택

#### 한줄 요약

- 고정 패턴의 고속 처리는 DFA, 상태 폭증 우려는 시간 한도를 둔 지연 결정화를 선택
