---
sidebar:
  order: 48
  label: "048. 지도 학습•비지도 학습•강화 학습 (Learning Paradigms)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "지도 학습•비지도 학습•강화 학습 (Learning Paradigms)"
date: "2026-08-17T17:03:00+09:00"
tags:
  - "notes-basic-theory"
weight: 48
extra:
  question_no: "048"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "학습 신호 기반 상위 분류와 선택 기준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **머신러닝 3대 학습 패러다임**: 학습 신호(Feedback Signal)의 성격에 따라 지도 학습(Supervised), 비지도 학습(Unsupervised), 강화 학습(Reinforcement)으로 구분되는 AI 방법론 체계.
- **지도 학습(Supervised Learning)**: 입력 데이터 $X$와 정답 타깃 $Y$의 쌍($(X, Y)$)을 바탕으로 사상 함수($f: X \to Y$)를 학습하는 패러다임.
- **비지도 학습(Unsupervised Learning)**: 정답 레이블 없이 데이터 자체의 내재된 분포, 군집, 차원 축소 구조를 탐색하는 패러다임.
- **강화 학습(Reinforcement Learning, RL)**: 환경(Environment)과 상호작용하며 시도착오(Trial-and-Error)를 통해 누적 보상(Cumulative Reward)을 극대화하는 최적 정책($\pi$)을 학습하는 패러다임.

</details>

- 정의/개념: 정답 라벨(오차 피드백), 데이터 구조(재구성/밀도 피드백), 환경 보상(지연 보상 피드백) 중 어떤 **학습 신호(Feedback Signal)를 기반으로 모델을 갱신하는지에 따른 머신러닝 3대 분류 체계**
- 배경/필요성: 문제의 목적, 데이터 수집 가능성(라벨 비용) 및 환경과의 상호작용 제약에 따라 **적합한 알고리즘 및 목적 함수(Loss/Reward) 선정 필수**

#### 한줄 요약

- 정답 라벨, 데이터 내재 구조, 환경 보상 신호에 따라 지도, 비지도, 강화 학습으로 분기

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **마르코프 결정 과정(MDP, Markov Decision Process)**: 강화 학습의 수학적 프레임워크로 상태($S$), 행동($A$), 전이확률($P$), 보상($R$), 할인율($\gamma$)의 5-튜플로 정의.
- **보상 해킹(Reward Hacking)**: 강화 학습 에이전트가 개발자의 원래 의도를 벗어나 보상 함수의 허점을 악용하여 편법으로 점수만 극대화하는 현상.

</details>

- 지도 학습은 **명시적 손실 함수($L(\hat{y}, y)$) 최소화를 통한 높은 예측 정확도** 제공
- 비지도 학습은 **비용 소모적인 라벨링 없이 데이터의 기저 패턴 및 이상 징후 자율 추출**
- 강화 학습은 **지연된 보상(Delayed Reward) 환경에서의 순차적 의사결정(Sequential Decision Making) 최적화**

#### 한줄 요약

- 정답 오차 최소화(지도), 내재 패턴 탐색(비지도), 누적 보상 극대화(강화)를 지향

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **피드백 루프 메커니즘**:
  - 지도: $(x, y) \to \text{Model} \to \text{Loss} \to \text{Gradient}$.
  - 비지도: $x \to \text{Model} \to \text{Distance/Recon Loss} \to \text{Latent/Cluster}$.
  - 강화: $s_t \to \text{Agent} \to a_t \to \text{Env} \to (s_{t+1}, r_{t+1}) \to \text{Policy Gradient}$.

</details>

```text
[ 머신러닝 3대 패러다임 피드백 비교 구조도 ]
 
 1. 지도 학습:   [ 입력 X ] ──► [ 모델 f ] ──► [ 예측 y_hat ] ──► [ 손실 L(y_hat, y) ] ──► 가중치 갱신
                                                        ▲
                                     [ 정답 레이블 Y ] ─┘
 
 2. 비지도 학습: [ 입력 X ] ──► [ 인코더/군집 ] ──► [ 잠재 표현 Z / 클러스터 C ] ──► 구조 도출
 
 3. 강화 학습:   [ 상태 S_t ] ──► [ 에이전트 정책 π ] ──► [ 행동 A_t ] ──► [ 환경 (Environment) ]
                      ▲                                                         │
                      └───────────── [ 보상 R_(t+1) 및 차기 상태 S_(t+1) ] ─────┘
```

선의 의미: 3대 패러다임별 입력, 모델/에이전트, 피드백 신호(라벨/구조/보상) 간의 파이프라인.

| 구성요소 | 책임 |
|:---|:---|
| 지도 학습기 | 정답 라벨($y$)과의 오차를 줄여 **미래 입력의 분류/회귀 예측** |
| 비지도 학습기 | 데이터 간의 거리/밀도를 분석하여 **차원 축소, 군집화, 이상 탐지** |
| 강화 학습 에이전트 | 환경의 보상 피드백을 통해 **가치 함수($Q$) 및 최적 행동 정책($\pi$) 도출** |
| 환경 (Environment) | 에이전트의 행동에 반응하여 **차기 상태($s'$)와 스칼라 보상($r$) 반환** |

#### 한줄 요약

- 정답 오차, 데이터 자체 구조, 환경 보상 신호가 각각의 학습기와 모델을 갱신하는 피드백으로 작용

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **준지도 학습(Semi-Supervised Learning)**: 소량의 라벨 데이터와 대량의 언라벨 데이터를 결합하여 지도 학습 성능을 비약적으로 끌어올리는 하이브리드 패러다임.

</details>

```text
비즈니스 과업 및 데이터 자산 분석
   │
   ▼
[ 1. 학습 신호 유형 판별 ]
├─ 입력 $X$에 대응하는 정답 타깃 $Y$ 확보됨 ⟹ [ 2. 지도 학습 (Supervised: Classification / Regression) ]
├─ 정답 라벨 부재 & 데이터 분포 탐색 필요 ⟹ [ 3. 비지도 학습 (Unsupervised: Clustering / PCA / Anomaly) ]
└─ 상호작용 가능한 시뮬레이터/환경 & 보상 신호 ⟹ [ 4. 강화 학습 (RL: Policy Optimization / Q-Learning) ]
   │
   ▼
[ 5. 패러다임별 품질 평가 ]
├─ 지도: Accuracy, F1-Score, RMSE, ROC-AUC
├─ 비지도: Silhouette Score, Reconstruction Error
└─ 강화: Cumulative Episode Return, Policy Convergence
```

**동작 원리**

1. **데이터 자산 분석**: 정답 라벨 유무, 환경 상호작용 가능 여부 판별
2. **지도 학습 분기**: 정답 데이터가 존재할 경우 분류/회귀 알고리즘(XGBoost, CNN, ResNet) 적용
3. **비지도 학습 분기**: 라벨이 없을 경우 K-Means, DBSCAN, Autoencoder 적용
4. **강화 학습 분기**: 게임, 로보틱스, 자율주행 등 보상 기반 의사결정 과업에 PPO, SAC, DQN 적용
5. **품질 검증**: 패러다임에 맞는 검증 지표로 최종 안정성 평가

#### 한줄 요약

- 정답 라벨, 데이터 자체, 환경 보상 신호를 판별하여 패러다임을 선택하고 특화된 지표로 평가

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **3대 패러다임 비교**:
  - 지도 학습: 정답 $(X, Y)$, 오차 역전파, 즉각적 피드백, 분류/회귀.
  - 비지도 학습: 언라벨 $X$, 기하학적 거리/밀도, 피드백 없음, 군집화/차원축소.
  - 강화 학습: 상태/행동 $(S, A, R)$, 보상 극대화, 지연된 피드백, 로보틱스/자율제어.

</details>

| 비교 항목 | 지도 학습 (Supervised) | 비지도 학습 (Unsupervised) | 강화 학습 (Reinforcement) |
|:---|:---|:---|:---|
| 훈련 데이터 | **입력-라벨 쌍 ($(X, Y)$)** | **라벨 없는 입력 데이터 ($X$)** | **상태-행동-보상 궤적 ($(S, A, R, S')$)** |
| 피드백 시점 | **즉각적인 정답 오차 피드백** | 명시적 외부 피드백 없음 | **지연된 환경 보상 피드백** |
| 핵심 목표 | $P(Y|X)$ 매핑 및 일반화 | 데이터 구조 $P(X)$ 및 잠재 표현 학습 | **기대 누적 할인 보상($\mathbb{E}[\sum \gamma^t R_t]$) 극대화** |
| 대표 알고리즘 | SVM, XGBoost, ResNet, Transformer | K-Means, PCA, Autoencoder, GMM | PPO, SAC, DQN, AlphaGo |
| 한계 및 위험 | **고비용의 라벨링 데이터 필수** | 정량적 성능 평가의 객관성 부족 | **탐색-활용 딜레마, 보상 해킹 위험** |

#### 한줄 요약

- 정답 예측은 지도 학습, 구조 발견은 비지도 학습, 상호작용 정책 최적화는 강화 학습을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RLHF(Reinforcement Learning from Human Feedback)**: 대규모 언어 모델(LLM)을 인간의 선호도 보상 모델(Reward Model)과 PPO 알고리즘을 통해 안전하고 유용하게 정렬(Alignment)하는 하이브리드 강화 학습 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 라벨링 비용 폭증으로 인한 **지도 학습 데이터 부족** | **자기지도 사전학습 + 전이학습(Fine-Tuning)** | 라벨 요구량 90% 절감 |
| 비지도 군집/이상 탐지의 **비즈니스 타당성 검증 난해** | **실루엣 계수 + 도메인 전문가 휴먼 검수** 병행 | 실무 설명력 및 신뢰도 확보 |
| 강화 학습의 보상 허점 악용인 **보상 해킹(Reward Hacking)** | **다중 목적 보상 설계 및 안전 제약(Constrained MDP)** | 의도된 안전 정책으로의 정렬 |
| 시뮬레이션과 실제 환경의 괴리인 **Sim-to-Real 갭** | **도메인 무작위화(Domain Randomization)** 기법 적용 | 실제 물리 환경 전이 성공률 향상 |

#### 한줄 요약

- 라벨 비용은 자기지도 사전학습으로 절감하고, 라벨 품질은 도메인 전문가 검수로 확보하며, 강화학습의 보상 설계에는 안전 제약을 포함하고, 시뮬레이션 갭은 도메인 무작위화로 극복한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **현대 복합 AI 파이프라인**: 현대 최고 성능의 AI(예: ChatGPT)는 비지도/자기지도 사전학습(Pre-training) $\to$ 지도 학습 미세조정(SFT) $\to$ 인간 피드백 강화 학습(RLHF)의 3대 패러다임을 순차 융합하여 구축.

</details>

- 정답 라벨 매핑은 **지도 학습**, 잠재 패턴/구조 발견은 **비지도 학습**, 환경 상호작용 의사결정은 강화 학습 선택

#### 한줄 요약

- 과업 목표와 데이터 피드백 형태에 맞춰 패러다임을 선택하고, 실무에서는 3대 기법을 유기적으로 융합
