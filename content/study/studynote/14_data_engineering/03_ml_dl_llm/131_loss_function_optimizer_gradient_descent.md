+++
weight = 131
title = "131. 손실 함수·옵티마이저·경사 하강법 - 딥러닝 학습의 3대 축"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 딥러닝 학습은 **①[[075_loss_function_cost_function|손실 함수]]([[087_loss_function|Loss Function]])로 예측과 정답의 차이를 측정**하고, **②[[275_gradient_descent_sgd|경사 하강법]]([[165_gradient_descent|Gradient Descent]])으로 손실을 줄이는 방향을 계산**하며, **③[[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[088_optimizer|Optimizer]])가 가중치를 업데이트**하는 3단계 순환이다.
> 2. **가치**: 이 3가지가 잘못되면 학습이 수렴하지 않거나(발산), 지역 최솟값에 갇히거나(과소적합), 과적합되므로 **각 요소의 선택이 모델 성능을 직접 결정**한다.
> 3. **판단 포인트**: [[104_classification_analysis|분류]]([[154_cross_entropy|Cross-Entropy]]), 회귀([[076_mse_mean_squared_error_regression|MSE]]), [[163_optimizer_sql_execution_plan_generator|옵티마이저]](Adam이 사실상 표준), [[080_gradient_descent_learning_rate|학습률]] [[079_kube_scheduler_pod_placement|스케줄러]]([[309_cosine_annealing|Cosine Annealing]])가 현대 딥러닝의 표준 조합이다.

---

## Ⅰ. 개요 및 필요성

```text
학습 루프: 예측 → 손실 계산 → 역전파 → 가중치 업데이트 → 반복
  Loss: Cross-Entropy (분류), MSE (회귀)
  Optimizer: SGD → Momentum → Adam (표준)
```

- **📢 섹션 요약 비유**: [[075_loss_function_cost_function|손실 함수]]는 **시험 채점**, [[275_gradient_descent_sgd|경사 하강법]]은 **"어떻게 공부하면 점수가 오를까" 방향 계산**, [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 **실제 공부 [[268_strategy_pattern|전략]]**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[163_optimizer_sql_execution_plan_generator|옵티마이저]] | 특징 |
|:---|:---|
| **SGD** | 기본, 느림 |
| **[[276_momentum_optimizer|Momentum]]** | 관성 추가, 진동↓ |
| **[[277_adam_optimizer|Adam]]** | **[[276_momentum_optimizer|Momentum]]+RMSProp, 표준** |
| **AdamW** | [[277_adam_optimizer|Adam]]+[[091_l1_l2_regularization_weight_decay|Weight Decay]] |

---

## Ⅲ~Ⅴ. 결론

[[075_loss_function_cost_function|손실 함수]]·[[163_optimizer_sql_execution_plan_generator|옵티마이저]]·[[275_gradient_descent_sgd|경사 하강법]]은 **딥러닝 학습의 핵심 엔진**이며, [[277_adam_optimizer|Adam]]/AdamW가 현재 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[087_loss_function|Loss Function]]** | 예측↔정답 차이 측정 |
| **[[165_gradient_descent|Gradient Descent]]** | 손실 최소화 방향 |
| **[[277_adam_optimizer|Adam]]** | 적응형 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (표준) |
| **[[240_switch_learning_forwarding_flooding|Learning]] Rate** | 학습 보폭 |
| **[[272_backpropagation|Backpropagation]]** | [[272_backpropagation|역전파]] (기울기 계산) |

### 📈 관련 키워드 및 발전 흐름도

```text
[SGD (1951)] → [Momentum (1964)] → [AdaGrad (2011)]
    → [RMSProp (2012)] → [Adam (2014) — 표준]
    → [AdamW (2018)] → [현재: Lion·Sophia — 차세대 옵티마이저]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[075_loss_function_cost_function|손실 함수]]는 **시험 채점**이에요. 틀린 게 많으면 점수(손실)가 높아요.
2. [[275_gradient_descent_sgd|경사 하강법]]은 **"어떻게 공부하면 점수가 오를까"** 방향을 알려줘요.
3. [[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[277_adam_optimizer|Adam]])는 **가장 효율적인 공부법**이라 시험 점수가 빨리 올라요!
