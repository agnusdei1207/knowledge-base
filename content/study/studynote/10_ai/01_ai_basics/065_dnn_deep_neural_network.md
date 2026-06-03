+++
title = "65. 심층 신경망 (DNN, Deep Neural Network) - 2개 이상의 은닉층을 가진 다층 퍼셉트론"
weight = 65
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DNN(Deep Neural Network)은 2개 이상의 은닉층을 가진 신경망으로, 더 깊은 비선형 표현을 학습한다.
> 2. **가치**: 이미지, 음성, 자연어처럼 복잡한 패턴을 단계적으로 [[198_abstraction_control_data_process|추상화]]해 높은 표현력을 얻는다.
> 3. **판단**: 깊게 쌓는 것만으로 [[282_performance_tactics|성능]]이 오르지 않으므로, 학습 안정성과 과적합 제어가 함께 필요하다.

---

## Ⅰ. 개요 및 필요성

[[266_mlp_hidden_layers|다층 퍼셉트론]](MLP)보다 더 복잡한 패턴을 다루려면 은닉층을 여러 개 쌓아야 한다. 이때 DNN이 등장한다.

깊은 층은 입력에서 고수준 특징으로 가는 중간 표현을 단계적으로 만들어 준다.

- **📢 섹션 요약 비유**: 사물을 한 번에 보는 대신, 스케치 → 색칠 → 완성본처럼 단계별로 그려 가는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Input
  ↓
Hidden Layer 1
  ↓
Hidden Layer 2
  ↓
...
  ↓
Output
```

| 요소 | 역할 |
| :-- | :-- |
| Hidden Layers | 단계적 표현 학습 |
| Activation | 비선형성 부여 |
| [[272_backpropagation|Backpropagation]] | 역방향으로 [[267_weight_bias_activation|가중치]] 학습 |
| [[087_loss_function|Loss Function]] | 예측 오차 측정 |

DNN은 층이 깊어질수록 더 복잡한 특징을 [[198_abstraction_control_data_process|추상화]]할 수 있지만, 학습이 어려워진다. 그래서 [[459_quic_fec_forward_error_correction|초기]]화, [[093_normalization|정규화]], [[280_dropout|드롭아웃]] 같은 기법이 중요하다.

- **📢 섹션 요약 비유**: 한 번에 큰 퍼즐을 맞추는 게 아니라, 작은 조각을 층층이 맞춰 가는 느낌이다.

---

## Ⅲ. 비교 및 연결

| 모델 | 은닉층 | 표현력 | 학습 난이도 |
| :-- | :-- | :-- | :-- |
| [[265_single_layer_perceptron_xor|Single-Layer Perceptron]] | 없음 | 낮음 | 낮음 |
| MLP | 1개 이상 | 중간 | 중간 |
| DNN | 2개 이상 | 높음 | 높음 |

| 기법 | 역할 |
| :-- | :-- |
| [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]] | 과적합 완화 |
| [[282_batch_normalization|Batch Normalization]] | 학습 안정화 |
| [[269_relu_activation|ReLU]] 계열 | [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 완화 |

DNN은 단순히 "더 깊은 MLP"가 아니라, 계층적 표현 학습을 통해 복잡한 문제를 푸는 구조다.

- **📢 섹션 요약 비유**: 얇은 옷 한 겹보다, 계절별 옷을 여러 겹 입어야 더 다양한 날씨에 대응할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 깊이가 정말 필요한 문제인가?
2. 과적합을 막는 장치가 있는가?
3. [[129_activation_function|활성화 함수]] 선택이 적절한가?
4. 학습 안정화 기법을 적용했는가?
5. [[001_dikw_pyramid|데이터]]가 충분한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 깊이만 늘리고 [[001_dikw_pyramid|데이터]]는 늘리지 않는 설계
- 과적합 제어 없이 큰 모델만 쓰는 설계
- [[129_activation_function|활성화 함수]]와 [[459_quic_fec_forward_error_correction|초기]]화를 무시하는 설계
- DNN을 만능으로 생각하는 설계

기술사 관점에서는 DNN을 "깊어서 좋은 모델"이 아니라 "계층적 표현을 배우는 모델"로 설명해야 한다.

- **📢 섹션 요약 비유**: 높은 탑이 아니라, 여러 층의 방을 쌓아 올린 집이다.

---

## Ⅴ. 기대효과 및 결론

DNN은 복잡한 [[001_dikw_pyramid|데이터]]를 계층적으로 표현해 현대 AI의 핵심이 되었다. 하지만 깊이와 안정성의 균형이 중요하다.

결론적으로 DNN은 다층 신경망을 더 깊게 확장한 표현 학습 구조다.

- **📢 섹션 요약 비유**: 얇은 그림보다, 여러 레이어가 쌓인 그림이 더 풍부하다.

---

## 관련 개념 맵

```text
MLP
  ↓
Deep Neural Network
  ↓
Representation Learning
  ↓
Backpropagation
```

---

## 관련 키워드 및 발전 흐름도

```text
Perceptron
  ↓
MLP
  ↓
DNN
  ↓
Deep Learning
```

---

## 어린이를 위한 3줄 비유 설명

한 겹만 있는 그림보다 여러 겹이 더 자세해요.  
DNN은 그런 식으로 여러 층을 쌓아요.  
그래서 더 복잡한 문제를 풀 수 있어요.
