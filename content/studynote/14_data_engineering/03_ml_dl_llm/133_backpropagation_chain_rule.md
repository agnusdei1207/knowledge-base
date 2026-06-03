---
title: 133. 역전파 & 연쇄 법칙 (Backpropagation & Chain Rule)
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[272_backpropagation|역전파]]([[272_backpropagation|Backpropagation]])는 **출력층에서 입력층 방향으로 손실의 기울기(Gradient)를 전파**하여 각 [[267_weight_bias_activation|가중치]]가 손실에 기여하는 정도를 계산하는 [[001_algorithm_definition|알고리즘]]이며, 미적분의 연쇄 법칙(Chain Rule)이 핵심 수학이다.
> 2. **가치**: [[272_backpropagation|역전파]] 없이는 수백만 파라미터의 **최적 [[267_weight_bias_activation|가중치]]를 찾는 것이 불가능**하며, 1986년 Rumelhart의 [[272_backpropagation|역전파]] 논문이 신경망 학습의 실용적 돌파구였다.
> 3. **판단 포인트**: [[272_backpropagation|역전파]]의 Vanishing/[[089_exploding_gradient_clipping|Exploding Gradient]] 문제를 이해하고, [[269_relu_activation|ReLU]]·BatchNorm·Residual Connection·Gradient Clipping이 해결 기법이다.

---

## Ⅰ. 개요 및 필요성

```text
순전파: x → 은닉층 → 출력 → 손실(L)
역전파: ∂L/∂W = ∂L/∂y · ∂y/∂h · ∂h/∂W  (연쇄 법칙)
  → 각 가중치가 손실에 기여하는 정도 → 가중치 업데이트
```

- **📢 섹션 요약 비유**: [[272_backpropagation|역전파]]는 **"왜 시험 점수가 낮은지" 거꾸로 추적**하는 것이다. 출력(점수)→공부법→교재 순으로 원인을 찾는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 문제 | 현상 | 해결 |
|:---|:---|:---|
| **Vanishing** | 기울기→0 | [[269_relu_activation|ReLU]], [[287_resnet_skip_connection|ResNet]] |
| **Exploding** | 기울기→∞ | Gradient [[389_ppo_proximal_policy_optimization|Clipping]] |

---

## Ⅲ~Ⅴ. 결론

[[272_backpropagation|역전파]]는 **딥러닝 학습의 유일한 실용적 [[001_algorithm_definition|알고리즘]]**이며, 연쇄 법칙의 효율적 구현(Computational [[104_graph|Graph]])이 PyTorch·TensorFlow의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[272_backpropagation|역전파]]** | 기울기 역방향 전파 |
| **연쇄 법칙** | 합성 함수 미분 |
| **[[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]** | 깊은 층에서 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] |
| **[[381_autograd_chain_rule|AutoGrad]]** | 자동 미분 (PyTorch) |
| **Computational [[104_graph|Graph]]** | 연산 [[070_graph_datastructure|그래프]] 기반 [[272_backpropagation|역전파]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[역전파 이론 (Werbos, 1974)] → [실용화 (Rumelhart, 1986)]
    → [Vanishing 문제 인식 (1990s)]
    → [ReLU+BatchNorm+ResNet (2010s) — 해결]
    → [현재: AutoGrad (PyTorch) — 자동 역전파]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[272_backpropagation|역전파]]는 시험에서 **"왜 틀렸지?" 거꾸로 추적**하는 거예요.
2. 정답(출력)→풀이(은닉층)→공식([[267_weight_bias_activation|가중치]]) 순으로 **원인을 찾아요**.
3. 원인을 알면 **공식([[267_weight_bias_activation|가중치]])을 고쳐서** 다음 시험에 점수가 올라요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 258

← **이전**: [[132_adam_optimizer|132. Adam 옵티마이저 - 적응형 학습률의 사실상 표준]]
**다음**: [[134_regularization_dropout_batch_norm|134. 정규화 기법 (Regularization) - Dropout·BatchNorm·L1/L2]] →

---
