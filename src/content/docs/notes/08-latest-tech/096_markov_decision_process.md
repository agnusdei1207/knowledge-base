---
sidebar:
  order: 96
  label: "096. 마르코프 결정과정 (Markov Decision Process)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "마르코프 결정과정 (Markov Decision Process)"
date: "2026-09-07T16:00:00+09:00"
tags:
  - "notes-latest-tech"
weight: 96
extra:
  question_no: "096"
  source_status: "기출"
  source_history: "131회, 132회"
  priority: 50
  priority_note: "상태•행동•보상 모델이 강화학습 기반"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **마르코프 결정과정(Markov Decision Process, MDP)**: 상태•행동•전이확률•보상으로 순차 결정을 표현한다.
- **순차 의사결정(Sequential Decision Making)**: 행동이 미래 상태와 누적 보상에 영향을 주는 문제.

</details>

- 정의/개념: 상태•행동•전이•보상으로 순차 결정을 표현한 **MDP**
- 배경/필요성: 동적 제어 및 인공지능 에이전트의 순차적 의사결정(**Sequential Decision Making**) 문제에서 과거의 모든 이력(History)을 매 순간 조건으로 고려할 경우, 시간 경과에 따라 상태 공간(State Space)과 계산 복잡도가 지수적으로 폭증하는 차원의 저주(Curse of Dimensionality)가 발생함에 따라, "미래의 상태는 과거의 전체 이력이 아닌 오직 현재의 상태와 행동에 의해서만 결정된다"는 마르코프 성질(Markov Property)을 기반으로 수학적 5-튜플 $\langle S, A, P, R, \gamma \rangle$ 체계를 정립한 마르코프 결정과정(Markov Decision Process: MDP / Partially Observable MDP: POMDP / State-Action-Reward-Transition Dynamics)을 도입하여 복잡한 시계열 동적 의사결정 문제를 현재 상태 기반의 간결하고 엄밀한 수학적 모델로 정형화, 할인율(**$\gamma$**)을 반영한 장기 누적 보상 기댓값의 최적화 목적함수 도출, 동적 계획법(Dynamic Programming) 및 강화학습(RL) 알고리즘 적용을 위한 표준 이론적 토대 확립을 달성할 필요

#### 한줄 요약
- 순차 의사결정의 상태•행동•전이•보상 모델링

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **마르코프 성질(Markov Property)**: 현재 상태만으로 다음 상태 분포가 결정되는 성질.
- **전이확률(Transition Probability)**: 특정 상태 $s$에서 행동 $a$를 취했을 때 다음 상태 $s'$로 이동할 확률 분포 $P(s'|s,a)$
- **할인율(Discount Factor, $\gamma$)**: 미래 보상을 현재 가치로 환산하는 계수.

</details>

- **마르코프 성질**: 현재 상태 기반의 독립적 미래 상태 전이
- **환경 동역학**: 상태•행동별 전이확률 및 보상 함수 정의
- **장기 최적화**: 정책 및 할인율 기반 누적 가치 계산

#### 한줄 요약
- 마르코프성•환경 동역학•할인 가치 기반 장기 최적화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **상태(State)**: 의사결정에 필요한 환경 정보를 압축한 표현.
- **행동 집합(Action Set)**: 각 상태에서 선택 가능한 행동 모음.
- **보상 함수(Reward Function)**: 상태 전이 시점의 즉시 성과.

</details>

```text
[Markov Decision Process]
├── [의사결정 계층]
│   ├── [상태 저장소 (State S)]
│   ├── [행동 선택기 (Action A)]
│   └── [정책·가치 평가기 (Policy π)]
└── [환경 동역학 계층]
    ├── [전이 모델 (Transition P)]
    └── [보상 함수 (Reward R)]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 상태 저장소 | 전이에 필요한 환경 정보 보관 |
| 행동 선택기 | 상태별 **행동 집합** 정의 |
| 전이 모델 | 행동별 다음 상태 확률 산출 |
| 보상 함수 | 전이의 즉시 성과 수치화 |
| 정책•가치 | 기대 누적 보상 기반 전략 최적화 |

#### 한줄 요약
- 상태•행동•전이•보상•정책•가치 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **상태 전이(State Transition)**: 전이확률에 따른 상태 변화 과정.
- **할인 가치(Discounted Value)**: 미래 보상을 현재 시점으로 환산한 값.

</details>

```text
┌─────── 에피소드 루프 ───────┐
│ 1. 현재 상태 관측           │
│ 2. 정책 기반 행동 선택      │
│ 3. 확률 기반 상태 전이      │
│ 4. 보상•다음 상태 산출      │
│ 5. 할인 가치•정책 평가      │
└─────────────┬─────────────┘
```

1. 현재 상태 관측: 전이 정보를 요약한 상태 파악
2. 정책 기반 행동 선택: 상태별 행동 규칙 적용
3. 확률 기반 **상태 전이**: 전이확률에 따라 환경 변화
4. 보상•다음 상태 산출: 즉시 성과와 새 상태 획득
5. **할인 가치**•정책 평가: 누적 가치로 정책 개선

#### 한줄 요약
- 상태•행동•전이•보상•할인 가치 평가 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **다중 선택 밴딧(Multi-armed Bandit)**: 상태 전이 없이 행동 보상을 학습한다.
- **부분 관측 MDP(Partially Observable MDP, POMDP)**: 관측값으로 숨은 상태를 추정한다.
- **믿음 상태(Belief State)**: 관측 이력 기반 상태 확률 분포.

</details>

| 모델 | MDP | 밴딧 | POMDP |
|:---|:---|:---|:---|
| 적용 기준 | 완전 상태 관측 | 상태 전이 없음 | 상태 일부 은닉 |
| 핵심 특징 | 상태•전이•보상 | 독립 행동 보상 | 관측 기반 믿음 상태 |
| 한계 | 관측 가정 엄격 | 순차 영향 배제 | 계산 복잡성 증가 |

#### 한줄 요약
- 관측 가능성•상태 전이 유무 대상 따라 모델 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **마르코프성 부족(Lack of Markov Property)**: 현재 상태의 전이•보상 정보가 불충분한 문제.
- **목표 불일치(Goal Misalignment)**: 보상 함수와 장기 성과가 다른 문제.
- **전이 모델 오차(Model Error)**: 추정 전이확률과 실제 변화의 차이.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **마르코프성 부족** | 이력•센서 기반 **상태 표현** 보강 | 전이 예측 정밀도 향상 |
| **보상 불일치** | 장기 목표•제약을 **보상 함수**에 반영 | 정책 왜곡 완화 |
| **전이 모델 오차** | 운영 데이터로 **전이확률** 검증 | 가치 추정 편향 감소 |

#### 한줄 요약
- 마르코프성•보상 정렬•전이 모델 오차 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **관측 가능성(Observability)**: 의사결정용 환경 정보를 파악할 수 있는 정도.
- **상태 표현(State Representation)**: 전이 예측에 필요한 정보 구조.

</details>

- 모든 순차적 의사결정 문제와 현대 강화학습 이론의 수학적 근간을 이루며 자율주행, 금융 트레이딩, 로보틱스 제어의 상태 전이를 완벽히 모델링하는 **강화학습 및 최적 제어 이론의 핵심 표준 프레임워크(Markov Decision Process / 5-Tuple Formulation $\langle S, A, P, R, \gamma \rangle$ / Markov Property / Transition Dynamics & Reward Function / Discounted Return / POMDP & Belief State)의 확고한 기반**으로 확고히 자리 잡았으며, 고차원 연속 공간 딥러닝과 결합된 Deep RL로 진화하는 가운데, 실무 MDP 모델링 시에는 센서 정보 누락이나 잡음으로 인한 마르코프성 결핍을 방어하기 위해 최근 $k$개 프레임 스태킹(Frame Stacking) 또는 RNN/트랜스포머 기반의 잠재 상태 표현을 도입하고, 환경의 불완전 관측 특성을 반영한 POMDP 및 믿음 상태(Belief State) 변환 적용, 의도치 않은 정책 편향을 방지하는 정밀한 보상 함수($R$) 정렬을 결합하여 완벽한 상태 표현력과 현실 세계 제어 안정성을 완성

#### 한줄 요약
- 상태 전이•**관측 가능성** 대상 따라 밴딧•MDP•POMDP 결정
