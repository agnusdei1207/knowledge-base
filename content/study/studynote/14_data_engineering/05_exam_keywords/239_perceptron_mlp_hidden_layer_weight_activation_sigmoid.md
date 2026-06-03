+++
weight = 239
title = "239. 퍼셉트론 (Perceptron) MLP 은닉층 가중치 활성화 시그모이드 (Sigmoid)"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[265_single_layer_perceptron_xor|단층 퍼셉트론]]([[265_single_layer_perceptron_xor|Single-Layer Perceptron]])은 선형 결정 경계만 학습할 수 있어 XOR 문제를 풀 수 없지만, [[266_mlp_hidden_layers|다층 퍼셉트론]](MLP, Multi-Layer Perceptron)은 은닉층(Hidden Layer)을 통해 비선형 함수를 근사한다.
> 2. **가치**: [[272_backpropagation|역전파]]([[272_backpropagation|Backpropagation]]) [[001_algorithm_definition|알고리즘]]은 미분의 연쇄 법칙(Chain Rule)을 이용해 각 [[267_weight_bias_activation|가중치]]([[267_weight_bias_activation|Weight]])의 손실 기여도를 효율적으로 계산하며, 이것이 딥러닝의 핵심 학습 메커니즘이다.
> 3. **판단 포인트**: [[268_sigmoid_vanishing_gradient|시그모이드]]([[268_sigmoid_vanishing_gradient|Sigmoid]]) [[129_activation_function|활성화 함수]]는 출력을 (0,1)로 제한해 [[130_probability|확률]] 해석에 유용하지만 깊은 네트워크에서 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 문제를 야기하므로, 은닉층에는 ReLU가 더 적합하다.

## Ⅰ. 개요 및 필요성

### 생물학적 뉴런에서 인공 뉴런으로

```
생물학적 뉴런                 인공 뉴런 (퍼셉트론)

   수상돌기 (Dendrites)          입력 x₁, x₂, ..., xₙ
       │ 신호 수신                     │ 가중합 계산
       ▼                               ▼
   세포체 (Cell Body)             가중합: z = Σ(wᵢ·xᵢ) + b
   신호 통합·처리                        │
       │                               ▼
       ▼                         활성화 함수 f(z)
   축삭 (Axon)                         │
   신호 전달                            ▼
       │                          출력 y = f(z)
       ▼
   다음 뉴런으로

  생물 뉴런의 핵심: 역치 이상이면 발화
  인공 뉴런의 핵심: 활성화 함수로 비선형 변환
```

### [[265_single_layer_perceptron_xor|단층 퍼셉트론]]의 한계 — XOR 문제

```
AND 문제: 선형 분리 가능 ✅
  ○○            선 하나로
    ●            분리 가능
  (0,0)(0,1)(1,0) = 0  (1,1) = 1

XOR 문제: 선형 분리 불가 ❌
  ●○
  ○●    어떤 직선으로도
         두 클래스를 분리 불가

  (0,0)=0  (1,1)=0  → ●
  (0,1)=1  (1,0)=1  → ○

Minsky & Papert (1969): 단층 퍼셉트론으로
XOR 풀 수 없음 → 첫 번째 AI 겨울
```

📢 **섹션 요약 비유**: [[265_single_layer_perceptron_xor|단층 퍼셉트론]]은 자로 직선만 그을 수 있는 [[104_classification_analysis|분류]]기다. 모든 문제가 직선 하나로 풀린다면 좋겠지만, XOR처럼 곡선이 필요한 문제는 손이 묶인다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[266_mlp_hidden_layers|다층 퍼셉트론]] (MLP, Multi-Layer Perceptron) 구조

```
┌───────────────────────────────────────────────────────┐
│              MLP 네트워크 구조                          │
│                                                       │
│  입력층         은닉층 1        은닉층 2       출력층   │
│  (Input)       (Hidden 1)     (Hidden 2)    (Output)  │
│                                                       │
│   x₁ ──────── h₁₁ ─────── h₂₁ ────────         │
│   x₂ ────── × h₁₂ ──── × h₂₂ ────── × ──→ ŷ  │
│   x₃ ──────── h₁₃ ─────── h₂₃ ────────         │
│                                                       │
│   × = 가중치·편향 연산 + 활성화 함수 적용              │
│                                                       │
│  계층별 수식:                                          │
│    z = W·x + b      (선형 변환)                       │
│    a = f(z)         (비선형 활성화)                    │
└───────────────────────────────────────────────────────┘
```

### 보편 근사 정리 (Universal Approximation Theorem)

> 하나 이상의 은닉층과 비선형 [[129_activation_function|활성화 함수]]를 가진 MLP는 임의의 연속 함수를 원하는 정밀도로 근사할 수 있다.

이것이 딥러닝이 이론적으로 어떤 문제든 풀 수 있다는 근거다.

### [[267_weight_bias_activation|가중치]]([[267_weight_bias_activation|Weight]])와 편향([[094_bias|Bias]])

```
가중치 W: 입력 신호의 중요도 조절
  w > 0: 양의 영향 (활성화 촉진)
  w < 0: 음의 영향 (활성화 억제)
  w = 0: 해당 연결 무시

편향 b: 활성화 함수의 임계값 이동
  b > 0: 활성화 임계값 낮춤 (더 쉽게 활성화)
  b < 0: 활성화 임계값 높임 (더 어렵게 활성화)

학습 목표: W, b를 반복 조정해 손실 L(ŷ, y)을 최소화
```

### [[129_activation_function|활성화 함수]] — [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]])

```
σ(x) = 1 / (1 + e^(-x))

특성:
  출력 범위:  (0, 1)
  미분:      σ'(x) = σ(x) × (1 - σ(x))
  최대 미분: 0.25 (x=0에서)

그래프:
  σ(x)
  1.0 │          ─────────
      │        ╱
  0.5 │      ╱  ← 변곡점 (x=0)
      │    ╱
  0.0 │─────────
      └──────────────────── x
       -5   0    5

장점:
  ✅ 출력 (0,1) → 확률 해석 가능
  ✅ 미분 가능 (연속 함수)
  ✅ 이진 분류 출력층에 적합

단점:
  ❌ 기울기 소실 (Vanishing Gradient)
     → |x|가 크면 σ'(x) ≈ 0
     → 깊은 레이어 학습 불가
  ❌ 출력 중심이 0이 아님 (비대칭)
  ❌ 지수 연산으로 계산 비용 높음
```

### [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) [[001_algorithm_definition|알고리즘]]

```
순전파 (Forward Pass):
  x → [Layer 1] → a₁ → [Layer 2] → a₂ → ŷ → 손실 L

역전파 (Backward Pass):
  손실 L → ∂L/∂W₂ → ∂L/∂a₁ → ∂L/∂W₁ → 가중치 업데이트

연쇄 법칙 (Chain Rule) 적용:
  ∂L/∂W₁ = (∂L/∂ŷ) × (∂ŷ/∂a₂) × (∂a₂/∂a₁) × (∂a₁/∂W₁)

가중치 업데이트 (경사 하강법, Gradient Descent):
  W ← W - η × ∂L/∂W
  여기서 η = 학습률 (Learning Rate)
```

**[[272_backpropagation|역전파]] 흐름 다이어그램:**
```
순전파:   x → W₁ → a₁ → W₂ → ŷ → L (손실 계산)
               ↑                        │
역전파:   ∂L/∂W₁ ←─────────────────────╯ (기울기 역방향 전달)
```

📢 **섹션 요약 비유**: [[272_backpropagation|역전파]]는 요리 실패 후 원인을 찾는 것이다. "음식이 짜다(손실 크다)" → "어디서 소금이 많이 들어갔나?" → 각 조리 단계를 거슬러 올라가며 원인을 찾는다.

## Ⅲ. 비교 및 연결

### [[129_activation_function|활성화 함수]] 비교

| 함수 | 공식 | 범위 | [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] | 주요 용도 |
|:---|:---|:---:|:---:|:---|
| [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) | 1/(1+e^-x) | (0,1) | ❌ 발생 | 이진 출력층 |
| [[070_hyperbolic_tangent_tanh_activation|하이퍼볼릭 탄젠트]] ([[070_hyperbolic_tangent_tanh_activation|Tanh]]) | (e^x-e^-x)/(e^x+e^-x) | (-1,1) | ❌ 발생 | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 은닉층 |
| [[269_relu_activation|ReLU]] | max(0,x) | [0,∞) | ✅ 해결 | 일반 은닉층 |
| Leaky [[269_relu_activation|ReLU]] | max(αx,x) | (-∞,∞) | ✅ 해결 | 죽은 [[269_relu_activation|ReLU]] 방지 |
| [[270_softmax|소프트맥스]] ([[270_softmax|Softmax]]) | exp(x_i)/Σexp(x_j) | (0,1) | - | 다중 [[104_classification_analysis|분류]] 출력층 |

### 단층 vs [[266_mlp_hidden_layers|다층 퍼셉트론]]

| 항목 | [[265_single_layer_perceptron_xor|단층 퍼셉트론]] | MLP (다층) |
|:---|:---|:---|
| 결정 경계 | 선형 (직선·초평면) | 비선형 (곡면) |
| XOR 해결 | ❌ 불가 | ✅ 가능 |
| 표현력 | 낮음 | 높음 |
| 학습 규칙 | 퍼셉트론 학습 규칙 | [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) |
| 활성화 | [[068_step_function_activation|계단 함수]] | [[268_sigmoid_vanishing_gradient|시그모이드]]·[[269_relu_activation|ReLU]] |

📢 **섹션 요약 비유**: MLP의 은닉층은 레고 블록의 중간 연결 부품이다. 블록(입력)을 직접 작품(출력)에 붙이기 어려울 때, 중간 부품이 변환을 담당해 복잡한 형태를 만든다.

## Ⅳ. 실무 적용 및 기술사 판단

### MLP 아키텍처 설계 가이드

```
입력 피처 수에 따른 은닉층 뉴런 수 경험적 규칙:
  1번째 은닉층: 입력 수의 2/3 ~ 2배
  이후 층:     점차 줄이거나 유지

예시 (입력 100차원, 10클래스 분류):
  Input(100) → Hidden(200) → Hidden(100) → Output(10)
             ReLU          ReLU           Softmax

과적합 방지:
  → 드롭아웃(Dropout) 0.3~0.5 각 은닉층 후 추가
  → 배치 정규화(Batch Normalization) 적용
```

### XOR 문제 MLP 해결 과정

```
레이어 구성: Input(2) → Hidden(2) → Output(1)
            ReLU         Sigmoid

학습 데이터:
  (0,0) → 0    (0,1) → 1
  (1,0) → 1    (1,1) → 0

은닉층의 역할:
  h₁: "둘 다 0이거나 둘 다 1" 탐지 (AND+AND)
  h₂: "적어도 하나가 1" 탐지 (OR)
  출력: h₂ AND NOT(h₁) = XOR
```

### 기술사 판단 포인트

1. **은닉층 깊이 vs 너비**: 깊이(층 수)는 추상 표현 학습, 너비(뉴런 수)는 세부 패턴 수용
2. **[[268_sigmoid_vanishing_gradient|시그모이드]] 사용 주의**: 은닉층에는 [[269_relu_activation|ReLU]] 권장, 출력층에만 [[268_sigmoid_vanishing_gradient|시그모이드]]/[[270_softmax|소프트맥스]]
3. **[[080_gradient_descent_learning_rate|학습률]] [[009_config|설정]]**: 너무 크면 발산, 너무 작으면 수렴 느림 → [[277_adam_optimizer|Adam]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 권장
4. **[[087_weight_initialization_xavier_he_glorot|가중치 초기화]]**: 0으로 초기화 금지 → He/Xavier 초기화 사용

📢 **섹션 요약 비유**: 은닉층은 화가가 스케치를 하기 전 밑그림을 그리는 과정이다. 바로 최종 그림을 그리는 것보다, 중간 단계를 거치면 훨씬 복잡한 그림이 가능해진다.

## Ⅴ. 기대효과 및 결론

### XOR 문제: 모델별 [[282_performance_tactics|성능]] 비교

| 모델 | XOR 정확도 | 이유 |
|:---|:---:|:---|
| [[265_single_layer_perceptron_xor|단층 퍼셉트론]] | 50% (랜덤) | 선형 분리 불가 |
| MLP (1 은닉층, 2 뉴런) | 100% | 비선형 경계 학습 |
| [[238_svm_margin_kernel_trick_naive_bayes|SVM]] (RBF [[022_kernel_role|커널]]) | 100% | [[022_kernel_role|커널]]로 비선형 처리 |

### 결론

[[265_single_layer_perceptron_xor|단층 퍼셉트론]]의 XOR 한계를 극복한 MLP는 딥러닝의 시작점이다. [[272_backpropagation|역전파]] [[001_algorithm_definition|알고리즘]](1986, Rumelhart et al.)은 연쇄 법칙을 이용해 다층 네트워크를 효율적으로 학습시키는 핵심 돌파구였다. 그러나 [[268_sigmoid_vanishing_gradient|시그모이드]] [[129_activation_function|활성화 함수]]는 깊은 네트워크에서 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 문제를 야기하며, 이것이 [[269_relu_activation|ReLU]] 등 현대 [[129_activation_function|활성화 함수]] 개발의 동기가 되었다.

📢 **섹션 요약 비유**: 퍼셉트론에서 MLP로의 발전은 자동차에 기어박스를 달아 직선만 가던 차가 굽은 길도 달릴 수 있게 된 것과 같다. 은닉층이 그 기어박스 역할이다.

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 기원 | [[265_single_layer_perceptron_xor|단층 퍼셉트론]] ([[265_single_layer_perceptron_xor|Single-Layer Perceptron]]) | 선형 분리, XOR 불가 |
| 한계 극복 | MLP (Multi-Layer Perceptron) | 은닉층으로 비선형 학습 |
| 핵심 기능 | 은닉층 (Hidden Layer) | 비선형 특징 변환 |
| 학습 파라미터 | [[267_weight_bias_activation|가중치]] ([[267_weight_bias_activation|Weight]]) / 편향 ([[094_bias|Bias]]) | 경사 하강법으로 업데이트 |
| [[129_activation_function|활성화 함수]] | [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) | (0,1) 출력, [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 단점 |
| 학습 [[001_algorithm_definition|알고리즘]] | [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) | 연쇄 법칙으로 기울기 계산 |
| 이론적 근거 | 보편 근사 정리 | MLP는 임의 함수 근사 가능 |

### 👶 어린이를 위한 3줄 비유 설명

1. [[265_single_layer_perceptron_xor|단층 퍼셉트론]]은 자로만 선을 그어 [[104_classification_analysis|분류]]하는 것이다—XOR처럼 곡선이 필요한 문제는 못 풀지만, 은닉층을 추가한 MLP는 곡선도 그릴 수 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
단층 퍼셉트론 → XOR 문제 (선형 분리 불가)
    │
    ▼
MLP (다층 퍼셉트론): 은닉층 + 비선형 활성화 함수
    ├─► Sigmoid · Tanh → ReLU · Swish
    └─► 역전파 (Backpropagation) + Chain Rule
    │
    ▼
CNN · RNN · Transformer → 딥러닝 시대
```
2. [[267_weight_bias_activation|가중치]]는 선생님 말씀 중 중요한 것에 귀를 쫑긋 세우는 것(w 큼)이고, 편향은 기본적으로 긍정적이거나 부정적인 선입견(b)이다.
3. [[272_backpropagation|역전파]]는 요리가 실패했을 때 "마지막에 소금을 넣었나, 그 전에 간장을 넣었나" 거슬러 올라가며 잘못된 단계를 찾아 고치는 과정이다.
