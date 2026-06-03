---
title: 6. 기울기 하강법 (Gradient Descent) — 최적화 기본
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기울기 하강법 (Gradient Descent) 은 함수의 *음의 기울기 방향으로 조금씩 이동*하며 최솟값을 찾는 반복 최적화 — f(x)가 감소하는 방향은 항상 -∇f(x)다.
> 2. **가치**: SGD ([[241_optimizer_sgd_minibatch_adam_momentum_adaptive|Stochastic Gradient Descent]], [[081_stochastic_gradient_descent_sgd|확률적 경사 하강법]]) 와 그 변형 ([[276_momentum_optimizer|Momentum]], [[277_adam_optimizer|Adam]]) 이 현대 딥러닝의 사실상 유일한 학습 방법이며, [[080_gradient_descent_learning_rate|학습률]] η가 수렴 속도와 안정성의 핵심 하이퍼파라미터다.
> 3. **판단 포인트**: 배치 크기 ↑ → 그래디언트 정확↑, [[430_index_fast_full_scan|병렬]] 효율↑ / 배치 크기 ↓ → 노이즈↑ ([[083_local_minima_vs_global_minimum|지역 최솟값]] 탈출), 메모리 효율↑ — 실무에서 배치 크기와 [[080_gradient_descent_learning_rate|학습률]] 스케줄링이 함께 조정된다.

---

## Ⅰ. 개요 및 필요성

최적화 목표: minimize f(x) over x ∈ ℝⁿ

**기울기 하강법 업데이트 규칙**:

```
x_{t+1} = x_t - η · ∇f(x_t)

η (에타): 학습률 (Learning Rate), 스텝 크기
∇f(x_t): x_t에서의 그래디언트 (기울기 벡터)
```

### [[080_gradient_descent_learning_rate|학습률]] η의 영향

```
손실 L
   │
   │╲         η 너무 큰 경우: 발산 (Diverge)
   │ ╲  ╱╲   ↗
   │  ╲╱  ╲─╱
   │
   │╲                 η 적절: 수렴 (Converge)
   │ ╲
   │  ╲─────────
   │
   │╲              η 너무 작음: 매우 느린 수렴
   │ ╲
   │  ╲─────────────────────────────
   └────────────────────────────────►
                   반복 횟수 t
```

📢 **섹션 요약 비유**: 기울기 하강법은 "안개 속 산 내려가기"다 — 현재 위치의 기울기(∇f)만 보고 가장 가파르게 내려가는 방향(-∇f)으로 조금씩(η) 발걸음을 옮긴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기울기 하강 변형 비교

| 방식 | 그래디언트 계산 | 업데이트 빈도 | 노이즈 | 용도 |
|:---|:---|:---:|:---:|:---|
| Batch [[275_gradient_descent_sgd|GD]] | 전체 데이터셋 | 1회/에포크 | 없음 | 소규모, 볼록 문제 |
| SGD | 단일 샘플 | n회/에포크 | 높음 | 빠른 [[459_quic_fec_forward_error_correction|초기]] 학습 |
| Mini-batch SGD | 배치 (32~512) | n/B회/에포크 | 중간 | 딥러닝 표준 |

### [[277_adam_optimizer|Adam]] ([[277_adam_optimizer|Adaptive Moment Estimation]]) [[163_optimizer_sql_execution_plan_generator|옵티마이저]]

```
m_t = β₁·m_{t-1} + (1-β₁)·g_t          (1차 모멘트: 기울기 EMA)
v_t = β₂·v_{t-1} + (1-β₂)·g_t²         (2차 모멘트: 분산 EMA)

m̂_t = m_t / (1-β₁ᵗ)   (바이어스 보정)
v̂_t = v_t / (1-β₂ᵗ)

x_{t+1} = x_t - η · m̂_t / (√v̂_t + ε)
```

기본값: β₁=0.9, β₂=0.999, ε=1e-8

특징: 각 파라미터마다 개별 [[080_gradient_descent_learning_rate|학습률]] 적응 → 희소 그래디언트에 강함.

### 주요 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 비교

```
손실 경관 (Loss Landscape)
          ╭──────────────────────────────╮
          │     ╭───────────╮            │
          │  ╭──╯           ╰──╮         │
          │ ╱  안장점(Saddle)   ╲        │
SGD ──────│─────────────────────X────────┼──► 지역 최소
Momentum ─│──────────────────/──X────────┼──► 빠른 수렴
Adam ─────│────────────────/────X────────┼──► 안장점 탈출 잘함
          ╰──────────────────────────────╯
```

| [[163_optimizer_sql_execution_plan_generator|옵티마이저]] | 아이디어 | 장점 | 단점 |
|:---|:---|:---|:---|
| SGD | 기본 | 단순, 볼록에 최적 | 안장점 취약 |
| [[276_momentum_optimizer|Momentum]] | 과거 방향 누적 | 빠른 수렴, 진동 감소 | lr 튜닝 필요 |
| RMSProp | [[136_variance|분산]] [[093_normalization|정규화]] | [[080_gradient_descent_learning_rate|학습률]] 자동 조정 | [[459_quic_fec_forward_error_correction|초기]]화 민감 |
| [[277_adam_optimizer|Adam]] | 1st+2nd 모멘트 | 빠르고 안정적 | 오버슈팅 가능 |
| AdamW | [[277_adam_optimizer|Adam]] + [[267_weight_bias_activation|가중치]] 감소 | 일반화 향상 | 추가 하이퍼파라미터 |

📢 **섹션 요약 비유**: Momentum은 "눈썰매 타기"다 — 단순 SGD가 매번 현재 기울기로만 방향을 정하는 것에 비해, Momentum은 이전 방향의 관성을 유지해 구불구불한 경로 대신 직선에 가깝게 내려간다.

---

## Ⅲ. 비교 및 연결

### [[164_convex_function|볼록 함수]]에서의 수렴 보장

| [[001_algorithm_definition|알고리즘]] | [[164_convex_function|볼록 함수]] 수렴률 | 강볼록 함수 수렴률 |
|:---|:---:|:---:|
| Batch [[275_gradient_descent_sgd|GD]] (고정 lr) | O(1/t) | O(ρᵗ) 선형 |
| SGD (감소 lr) | O(1/√t) | O(1/t) |
| Nesterov 가속 [[275_gradient_descent_sgd|GD]] | O(1/t²) | O(ρᵗ) 더 빠름 |

**Nesterov [[276_momentum_optimizer|모멘텀]]**:

```
y_{t+1} = x_t + γ(x_t - x_{t-1})   (미리보기 위치)
x_{t+1} = y_{t+1} - η·∇f(y_{t+1})  (보정된 위치에서 업데이트)
```

일반 Momentum의 O(1/t) → Nesterov의 O(1/t²) 개선 ([[164_convex_function|볼록 함수]]).

### [[080_gradient_descent_learning_rate|학습률]] 스케줄링 (LR Scheduling)

```
시간에 따른 lr 변화 전략:
Step Decay:    lr = lr₀ × γ^(epoch / step_size)
Cosine:        lr = lr_min + ½(lr_max - lr_min)(1 + cos(πt/T))
Warmup:        초기 몇 스텝 lr 천천히 증가 → 안정화
OneCycleLR:    lr 상승 → 하강 (1 사이클)
```

[[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] ([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 모델의 Warmup + Cosine decay가 현대 [[263_llm_large_language_model|LLM]] 학습 표준.

📢 **섹션 요약 비유**: [[080_gradient_descent_learning_rate|학습률]] 스케줄링은 "내리막길 속도 조절"이다 — 처음에는 빠르게 내려오고(큰 lr), 바닥(최솟값) 근처에서는 천천히 정밀하게 탐색한다(작은 lr).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대규모 모델 학습 [[009_config|설정]] ([[263_llm_large_language_model|LLM]])

```
GPT-3 학습 설정:
  옵티마이저: Adam (β₁=0.9, β₂=0.95)
  lr: 최대 6×10⁻⁴, Cosine decay to 10%
  배치 크기: 3.2M 토큰 (그래디언트 누적)
  그래디언트 클리핑: max norm = 1.0
  Mixed precision: FP16 계산 + FP32 마스터 가중치
```

### 그래디언트 클리핑 (Gradient [[389_ppo_proximal_policy_optimization|Clipping]])

손실 경관의 급경사(Cliff)에서 그래디언트 폭발 방지:

```
‖g‖ > threshold이면: g ← g × threshold / ‖g‖
```

[[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]], [[292_lstm|LSTM]], [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 등 순환 구조에서 필수.

### 기술사 판단 포인트

1. **"SGD vs [[277_adam_optimizer|Adam]] 선택 기준은?"** → 볼록 문제/소규모: SGD (이론적 보장) / 딥러닝: [[277_adam_optimizer|Adam]] (빠른 수렴)
2. **"배치 크기와 [[080_gradient_descent_learning_rate|학습률]]의 관계는?"** → 배치 크기 2배 → [[080_gradient_descent_learning_rate|학습률]] √2 또는 2배 [[249_scaling_normalization_standardization|스케일링]] (Linear Scaling Rule)
3. **"그래디언트 소실/폭발 대응은?"** → 소실: [[269_relu_activation|ReLU]], 잔차 연결([[287_resnet_skip_connection|ResNet]]) / 폭발: 그래디언트 클리핑

📢 **섹션 요약 비유**: 그래디언트 클리핑은 "과속 방지 턱"이다 — 그래디언트가 너무 크면(급경사) 정해진 속도(threshold) 이상으로 달리지 못하게 제한한다.

---

## Ⅴ. 기대효과 및 결론

기울기 하강법은 **딥러닝 혁명의 계산 엔진**이다. SGD의 단순함에서 Adam의 적응적 [[080_gradient_descent_learning_rate|학습률]]까지, 최적화 [[001_algorithm_definition|알고리즘]]의 발전이 신경망의 규모 확장을 가능하게 했다.

실무 [[435_checklist_based_testing|체크리스트]]:
- [[080_gradient_descent_learning_rate|학습률]]: [[568_logs_distributed_logging_elk_fluentd|로그]] 스케일로 탐색 (1e-4 ~ 1e-1)
- 배치 크기: 메모리 허용 범위 내 최대 ([[418_gpu|GPU]] 활용률)
- [[163_optimizer_sql_execution_plan_generator|옵티마이저]]: 대부분의 딥러닝은 AdamW가 기본
- [[079_kube_scheduler_pod_placement|스케줄러]]: Warmup + Cosine ([[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]) 또는 Step Decay ([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]])
- 클리핑: [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/[[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]는 항상 적용 권장

📢 **섹션 요약 비유**: [[277_adam_optimizer|Adam]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 "GPS 내비게이션"이다 — 과거 경로([[276_momentum_optimizer|모멘텀]])와 속도 변화([[136_variance|분산]])를 동시에 고려해 목적지(최솟값)로 가는 최적 경로를 동적으로 안내한다.

---

### 📌 관련 개념 맵

| 개념 | 수식 | 연결 |
|:---|:---|:---|
| Batch [[275_gradient_descent_sgd|GD]] | x←x-η·∇f(전체) | [[164_convex_function|볼록 함수]] 수렴 보장 |
| SGD | x←x-η·∇f(단일) | 딥러닝 노이즈 탈출 |
| [[277_adam_optimizer|Adam]] | 1st+2nd 모멘트 적응 | 딥러닝 표준 |
| LR 스케줄링 | Cosine/Warmup | 대규모 모델 학습 |
| 그래디언트 클리핑 | ‖g‖>th → [[093_normalization|정규화]] | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/[[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수 (Loss Function)]
    │
    ▼
[경사 하강법 (Gradient Descent)]
    │
    ▼
[학습률 (Learning Rate)]
    │
    ▼
[최적화 (Optimization)]
```

이 흐름도는 손실 함수를 줄이기 위해 [[275_gradient_descent_sgd|경사 하강법]]과 [[080_gradient_descent_learning_rate|학습률]]이 최적화를 이끄는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

1. **기울기 하강은 "안개 속 언덕 내려가기"**: 현재 발밑 기울기만 보고 가장 가파른 아래 방향으로 한 발씩 내딛는다.
2. **Adam은 "관성 있는 지혜로운 하이커"**: 지금까지 어떤 방향으로 얼마나 빠르게 왔는지를 기억하며 다음 발걸음을 최적화한다.
3. **[[080_gradient_descent_learning_rate|학습률]] 스케줄링은 "속도 조절 여행"**: 처음엔 빠르게 달리다가 목적지에 가까워지면 천천히 정밀하게 이동한다.
