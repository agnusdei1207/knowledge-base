---
title: 241. 옵티마이저 SGD (Stochastic Gradient Descent) 미니배치 Adam 모멘텀 적응 학습률
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[088_optimizer|Optimizer]])는 [[075_loss_function_cost_function|손실 함수]]([[087_loss_function|Loss Function]])의 기울기(Gradient)를 이용해 모델 파라미터를 반복 갱신하는 [[001_algorithm_definition|알고리즘]]으로, 수렴 속도와 안정성의 균형이 핵심이다.
> 2. **가치**: [[277_adam_optimizer|Adam]]([[277_adam_optimizer|Adaptive Moment Estimation]])은 [[276_momentum_optimizer|모멘텀]]([[276_momentum_optimizer|Momentum]])의 방향 관성과 RMSProp의 적응 [[080_gradient_descent_learning_rate|학습률]]을 결합하여 대부분의 딥러닝 작업에서 뛰어난 기본 선택지가 된다.
> 3. **판단 포인트**: 배치 크기([[346_batch_size_generalization|Batch Size]])와 [[080_gradient_descent_learning_rate|학습률]]([[240_switch_learning_forwarding_flooding|Learning]] Rate) 스케줄링 [[268_strategy_pattern|전략]]의 조합이 훈련 안정성과 일반화 [[282_performance_tactics|성능]]을 결정짓는 실무의 핵심 변수이다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델 훈련은 [[075_loss_function_cost_function|손실 함수]] L(θ)를 최소화하는 파라미터 θ를 찾는 최적화 문제다. 이를 위해 [[275_gradient_descent_sgd|경사 하강법]]([[165_gradient_descent|Gradient Descent]])이 사용된다.

**[[275_gradient_descent_sgd|경사 하강법]]의 기본 갱신 규칙**

```
θ_{t+1} = θ_t - η · ∇L(θ_t)
```

여기서 η는 [[080_gradient_descent_learning_rate|학습률]]([[240_switch_learning_forwarding_flooding|Learning]] Rate), ∇L은 [[075_loss_function_cost_function|손실 함수]]의 기울기다.

### 배치 유형 비교

| 구분 | 배치 [[275_gradient_descent_sgd|GD]] (Batch [[275_gradient_descent_sgd|GD]]) | SGD (Stochastic [[275_gradient_descent_sgd|GD]]) | 미니배치 SGD (Mini-batch SGD) |
|:---|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 사용량 | 전체 [[001_dikw_pyramid|데이터]]셋 | 샘플 1개 | N개 (32~512) |
| 기울기 정확도 | 높음 | 낮음(노이즈 큼) | 중간 |
| 메모리 | 많이 필요 | 적음 | 적당 |
| 수렴 속도 | 느림 | 빠르나 불안정 | 균형 우수 |
| [[418_gpu|GPU]] 효율 | 낮음 | 낮음 | 높음(벡터화) |

**핵심**: 실무에서는 미니배치 SGD가 표준이며, 배치 크기는 하드웨어 메모리와 일반화 [[282_performance_tactics|성능]]을 고려해 선택한다.

📢 **섹션 요약 비유**: [[275_gradient_descent_sgd|경사 하강법]]은 안개 낀 산을 내려올 때 발밑 경사만 보고 걷는 것이다. 배치 GD는 GPS로 전체 지형을 파악하지만 느리고, SGD는 눈 감고 뛰어 빠르지만 위험하며, 미니배치는 짧게 살펴보고 빠르게 걷는 현실적 타협이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[276_momentum_optimizer|모멘텀]]([[276_momentum_optimizer|Momentum]]) — 관성 기반 최적화

이전 기울기 방향의 관성을 유지해 진동을 줄이고 수렴을 가속한다.

```
v_t   = β·v_{t-1} + (1-β)·∇L(θ_t)
θ_t+1 = θ_t - η·v_t
```

- β ([[276_momentum_optimizer|모멘텀]] 계수): 보통 0.9
- 평탄한 방향은 가속, 진동 방향은 감쇠

### RMSProp — 적응 [[080_gradient_descent_learning_rate|학습률]]([[137_edutech_adaptive_learning_lms|Adaptive Learning]] Rate)

각 파라미터별 최근 기울기 크기의 제곱 이동 평균으로 [[080_gradient_descent_learning_rate|학습률]]을 조정한다.

```
s_t   = ρ·s_{t-1} + (1-ρ)·(∇L)²
θ_t+1 = θ_t - (η / √(s_t + ε)) · ∇L
```

- 자주 업데이트되는 파라미터: [[080_gradient_descent_learning_rate|학습률]] ↓
- 드물게 업데이트되는 파라미터: [[080_gradient_descent_learning_rate|학습률]] ↑

### [[277_adam_optimizer|Adam]] ([[277_adam_optimizer|Adaptive Moment Estimation]]) — [[276_momentum_optimizer|모멘텀]] + RMSProp

```
m_t = β₁·m_{t-1} + (1-β₁)·∇L          ← 1차 모멘텀 (방향)
v_t = β₂·v_{t-1} + (1-β₂)·(∇L)²       ← 2차 모멘텀 (크기)

m̂_t = m_t / (1 - β₁ᵗ)                  ← 편향 보정 (Bias Correction)
v̂_t = v_t / (1 - β₂ᵗ)                  ← 편향 보정

θ_t+1 = θ_t - η · m̂_t / (√v̂_t + ε)
```

기본 하이퍼파라미터: η=0.001, β₁=0.9, β₂=0.999, ε=1e-8

### [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 비교 다이어그램

```
손실 곡면 (Loss Landscape)
     ┌─────────────────────────────────────────┐
     │ ↘↘↘  SGD: 노이즈 많은 지그재그 경로  ↙↙ │
     │  ↘──────────────────────────────→  글로벌 최솟값 │
     │   모멘텀: 관성으로 진동 감소              │
     │    ↘═══════════════════════→           │
     │     Adam: 적응적, 빠르고 안정적 수렴     │
     │      ↘━━━━━━━━━━━━━━━━━━━→ ★          │
     └─────────────────────────────────────────┘
     
옵티마이저 성능 요약
┌──────────────┬───────────┬───────────┬───────────┐
│  옵티마이저  │  수렴속도 │  안정성   │  메모리   │
├──────────────┼───────────┼───────────┼───────────┤
│ SGD          │   느림    │   낮음    │   낮음    │
│ SGD+Momentum │   중간    │   중간    │   낮음    │
│ RMSProp      │   빠름    │   중간    │   중간    │
│ Adam         │   빠름    │   높음    │   높음    │
│ AdamW        │   빠름    │   최고    │   높음    │
└──────────────┴───────────┴───────────┴───────────┘
```

📢 **섹션 요약 비유**: Adam은 경험 많은 등산가다. [[276_momentum_optimizer|모멘텀]]으로 발걸음의 방향 관성을 유지하고(어디로 가던 중이었는지 기억), RMSProp으로 가파른 곳은 조심스럽게 평탄한 곳은 빠르게 걷는다. 두 [[268_strategy_pattern|전략]]을 동시에 쓰니 대부분의 지형에서 최적이다.

---

## Ⅲ. 비교 및 연결

### [[080_gradient_descent_learning_rate|학습률]] 스케줄링([[240_switch_learning_forwarding_flooding|Learning]] Rate Scheduling) [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 방법 | 적용 시점 |
|:---|:---|:---|
| Step Decay | 일정 에폭마다 [[080_gradient_descent_learning_rate|학습률]] 감소 | 단순 이미지 [[104_classification_analysis|분류]] |
| [[309_cosine_annealing|Cosine Annealing]] | 코사인 함수로 주기적 감소 | Vision [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] |
| Warm-up + Decay | 초반 증가 후 점진적 감소 | [[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]] 사전 학습 |
| Cyclical LR | 주기적 증감 반복 | 안장점(Saddle Point) 탈출 |
| One-Cycle [[164_policy|Policy]] | 단일 주기 급격한 증가 후 감소 | 빠른 수렴 필요 시 |

### [[080_gradient_descent_learning_rate|학습률]]과 배치 크기의 [[083_relationship_in_er_model|관계]] (Linear Scaling Rule)

```
배치 크기를 k배 키우면 → 학습률도 k배 증가 (선형 스케일링)
이유: 기울기 추정 분산이 1/k 감소 → 더 큰 보폭 가능
```

**주의**: 매우 큰 배치(>8K)는 일반화 [[282_performance_tactics|성능]] 저하 → Warm-up 필수

📢 **섹션 요약 비유**: [[080_gradient_descent_learning_rate|학습률]] 스케줄링은 자동차 속도 조절과 같다. 처음 도로(Warm-up)는 천천히, 고속도로 구간은 빠르게, 복잡한 교차로(수렴 근처)에서는 다시 천천히 접근한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### AdamW — [[267_weight_bias_activation|가중치]] 감쇠([[091_l1_l2_regularization_weight_decay|Weight Decay]]) 분리

일반 Adam은 L2 [[093_normalization|정규화]]를 기울기에 흡수하지만, AdamW는 [[267_weight_bias_activation|가중치]] 감쇠를 파라미터 갱신에 직접 적용한다.

```
θ_t+1 = θ_t - η·(m̂_t / (√v̂_t + ε)) - η·λ·θ_t
```

- [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 계열 모델에서 표준 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]
- λ ([[267_weight_bias_activation|가중치]] 감쇠): 0.01~0.1

### 실무 선택 가이드

| 상황 | 추천 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] | 이유 |
|:---|:---|:---|
| 일반 딥러닝 | [[277_adam_optimizer|Adam]] / AdamW | 기본 [[282_performance_tactics|성능]] 안정적 |
| 이미지 [[104_classification_analysis|분류]](대규모) | SGD + [[276_momentum_optimizer|Momentum]] + LR Decay | 최종 정확도 우수 |
| NLP / [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] | AdamW + Warm-up | L2 [[093_normalization|정규화]] 효과 분리 |
| [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] | [[277_adam_optimizer|Adam]] / RMSProp | 비정상 [[001_dikw_pyramid|데이터]]에 강인 |
| 초경량 모델 | SGD | 메모리 절약 |

### 기울기 클리핑(Gradient [[389_ppo_proximal_policy_optimization|Clipping]])

```python
# 기울기 폭발 방지
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

[[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|Recurrent Neural Network]])·[[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 학습 시 필수적으로 적용한다.

📢 **섹션 요약 비유**: [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 선택은 공사 현장 장비 선택과 같다. 정밀 작업(NLP)에는 다기능 공구(AdamW)를, 오래된 표준 작업(이미지 [[104_classification_analysis|분류]])에는 검증된 단순 공구(SGD+[[276_momentum_optimizer|Momentum]])를, 빠른 실험에는 만능 드릴([[277_adam_optimizer|Adam]])을 쓴다.

---

## Ⅴ. 기대효과 및 결론

### 최적화 [[001_algorithm_definition|알고리즘]] 발전사

```
Gradient Descent (1847)
      ↓
SGD (Stochastic GD) — 노이즈를 정규화 효과로 활용
      ↓
Momentum (1986) — Polyak, 관성 도입
      ↓
AdaGrad (2011) — 적응 학습률 최초
      ↓
RMSProp (2012) — Hinton, 이동 평균 도입
      ↓
Adam (2014) — Kingma & Ba, 모멘텀+RMSProp
      ↓
AdamW (2019) — Loshchilov, 가중치 감쇠 분리
      ↓
Lion (2023) — Google, 사인 기반 업데이트
```

### 기술사 시험 핵심 포인트

1. **[[277_adam_optimizer|Adam]] 수식** 완전히 기술: 1차·2차 [[276_momentum_optimizer|모멘텀]], 편향 보정
2. **배치 크기-[[080_gradient_descent_learning_rate|학습률]] [[083_relationship_in_er_model|관계]]**: Linear Scaling Rule 명시
3. **[[163_optimizer_sql_execution_plan_generator|옵티마이저]] 선택 근거**: 태스크별 추천과 이유
4. **[[080_gradient_descent_learning_rate|학습률]] 스케줄링** 종류와 적용 시점
5. **기울기 클리핑** 필요성 ([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]], [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]])

📢 **섹션 요약 비유**: 좋은 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 마라톤 코치와 같다. 선수(파라미터)가 어디로 달려야 하는지 방향을 잡고([[276_momentum_optimizer|모멘텀]]), 오르막과 내리막에 따라 페이스를 조절하며(적응 [[080_gradient_descent_learning_rate|학습률]]), 무리하지 않도록 에너지를 관리한다([[267_weight_bias_activation|가중치]] 감쇠). 최종 목표는 최단 시간에 결승선(전역 최솟값)에 도달하는 것이다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [[275_gradient_descent_sgd|경사 하강법]] ([[165_gradient_descent|Gradient Descent]]) | 손실 최소화의 기반 [[001_algorithm_definition|알고리즘]] |
| 핵심 변형 | [[276_momentum_optimizer|모멘텀]] ([[276_momentum_optimizer|Momentum]]) | 이전 기울기 방향 관성 유지 |
| 핵심 변형 | RMSProp | 파라미터별 적응 [[080_gradient_descent_learning_rate|학습률]] |
| 통합 방법 | [[277_adam_optimizer|Adam]] | [[276_momentum_optimizer|모멘텀]] + RMSProp 결합 |
| 실용 확장 | AdamW | [[267_weight_bias_activation|가중치]] 감쇠 명시적 분리 |
| 연관 [[268_strategy_pattern|전략]] | LR 스케줄링 | 훈련 단계별 [[080_gradient_descent_learning_rate|학습률]] 조정 |
| 안정화 기법 | 기울기 클리핑 | [[089_exploding_gradient_clipping|기울기 폭발]] 방지 |
| 관련 개념 | 배치 크기 ([[346_batch_size_generalization|Batch Size]]) | 미니배치 선택이 수렴에 영향 |

### 👶 어린이를 위한 3줄 비유 설명
1. [[275_gradient_descent_sgd|경사 하강법]]은 눈 감고 언덕을 내려올 때 발이 닿는 기울기를 느끼며 한 걸음씩 내딛는 것이야.

### 📈 관련 키워드 및 발전 흐름도

```text
BGD (Batch GD) → 느림
    │
    ▼
SGD → Mini-Batch SGD: 속도 + 안정성 균형
    │
    ▼
모멘텀 → RMSprop → Adam (모멘텀 + 적응 학습률)
    │
    ▼
AdamW · LAMB · 스케줄러 (Cosine · Warmup)
```
2. [[277_adam_optimizer|Adam]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 "어디로 가던 중이었지?"([[276_momentum_optimizer|모멘텀]])와 "이 길이 얼마나 가파르지?"(RMSProp)를 동시에 기억하는 똑똑한 탐험가야.
3. [[080_gradient_descent_learning_rate|학습률]] 스케줄링은 처음엔 천천히 주변을 살피고, 익숙해지면 빠르게 달리다가, 목적지 근처에서 다시 천천히 걷는 여행 계획이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 241 / 258

← **이전**: [[240_relu_vanishing_gradient_softmax_backprop_chain|240. ReLU 기울기 소실 (Vanishing Gradient) 복원 소프트맥스 역전파 연쇄 법칙]]
**다음**: [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|242. 규제 드롭아웃 (Dropout) 조기 종료 L1 L2 라쏘 릿지 종합]] →

---
