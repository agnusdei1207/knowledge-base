---
title: 64. 다층 퍼셉트론 (MLP, Multi-Layer Perceptron) - 은닉층(Hidden Layer) 도입으로 비선형 문제 해결
  가능
date: '2026-04-07'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[266_mlp_hidden_layers|다층 퍼셉트론]](MLP, Multi-Layer [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]])은 은닉층(Hidden Layer)과 비선형 [[129_activation_function|활성화 함수]]를 통해 복잡한 경계를 학습하는 신경망이다.
> 2. **가치**: [[265_single_layer_perceptron_xor|단층 퍼셉트론]]이 못 풀던 XOR 같은 비선형 문제를 해결할 수 있어, 현대 신경망의 기본 구조가 되었다.
> 3. **판단**: 층을 깊게 쌓는 것보다, [[001_dikw_pyramid|데이터]]와 문제에 맞는 표현력과 학습 안정성을 함께 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

[[265_single_layer_perceptron_xor|단층 퍼셉트론]]은 직선 하나로 나눌 수 있는 문제에만 강하다. 현실의 [[001_dikw_pyramid|데이터]]는 훨씬 복잡해서, 비선형 경계가 필요하다.

MLP는 은닉층을 넣어 입력 공간을 새로운 특징 공간으로 바꾸고, 그 공간에서 더 잘 나눌 수 있게 한다.

- **📢 섹션 요약 비유**: 납작한 종이로 못 자르면 한 번 접어서 여러 방향으로 자르는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Input Layer
  ↓
Hidden Layer(s)
  ↓
Output Layer
```

| 요소 | 역할 |
| :-- | :-- |
| Input Layer | 원래 특징 수신 |
| Hidden Layer | 비선형 표현 학습 |
| Activation | 선형 한계를 깨는 비선형성 부여 |
| Output Layer | 최종 예측 [[087_process_state_transition|생성]] |

은닉층은 단순히 층을 더하는 것이 아니라, 입력을 다른 좌표계로 바꿔 더 잘 구분하게 만드는 장치다. 그래서 XOR 같은 문제도 표현 가능해진다.

- **📢 섹션 요약 비유**: 같은 재료라도 한 번 섞고 모양을 바꾸면 전혀 다른 그림이 된다.

---

## Ⅲ. 비교 및 연결

| 모델 | 표현력 | 대표 한계 |
| :-- | :-- | :-- |
| [[265_single_layer_perceptron_xor|Single-Layer Perceptron]] | 선형 | XOR 불가 |
| MLP | 비선형 | 학습 복잡도 증가 |
| Deep Neural Network | 더 강한 표현력 | 과적합/학습 안정성 |

| 구성 | 역할 |
| :-- | :-- |
| [[267_weight_bias_activation|Weight]] | 연결 강도 |
| [[094_bias|Bias]] | 경계 이동 |
| [[272_backpropagation|Backpropagation]] | [[267_weight_bias_activation|가중치]] 학습 |

MLP는 [[265_single_layer_perceptron_xor|단층 퍼셉트론]]의 한계를 넘어서는 첫 단계다. 이후 더 깊은 신경망이 등장했지만, 핵심 아이디어는 은닉층과 비선형성에 있다.

- **📢 섹션 요약 비유**: 직선 자로 안 되는 문제를 풀려면 여러 번 꺾는 자가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 은닉층이 왜 필요한지 설명할 수 있는가?
2. [[129_activation_function|활성화 함수]]의 역할을 이해하는가?
3. [[080_gradient_descent_learning_rate|학습률]]과 과적합을 고려했는가?
4. XOR 같은 비선형 사례를 연결할 수 있는가?
5. 입력 특징이 충분한지 [[396_validation|확인]]했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 층만 늘리면 다 해결된다고 믿는 설계
- [[129_activation_function|활성화 함수]] 없이 선형 조합만 쌓는 설계
- [[001_dikw_pyramid|데이터]] 특성을 보지 않고 모델만 키우는 설계
- 과적합 제어 없이 복잡도만 올리는 설계

기술사 관점에서는 MLP를 "깊은 신경망의 출발점"으로 설명해야 한다. 은닉층의 의미를 모르고는 비선형 학습을 설명할 수 없다.

- **📢 섹션 요약 비유**: 한 번 접은 종이로는 안 되면 여러 번 접어 입체를 만드는 셈이다.

---

## Ⅴ. 기대효과 및 결론

MLP는 선형 분리 불가능 문제를 해결하며 신경망 시대를 열었다. 그래서 [[265_single_layer_perceptron_xor|단층 퍼셉트론]]의 한계와 함께 배우면 더 잘 이해된다.

결국 핵심은 "층을 쌓는 것"이 아니라 "비선형 표현을 배우는 것"이다.

- **📢 섹션 요약 비유**: 곧은 길만으로는 못 가는 곳에 굽은 길이 생긴다.

---

## 관련 개념 맵

```text
Perceptron
  ↓
Hidden Layer
  ↓
MLP
  ↓
Nonlinear Representation
```

---

## 관련 키워드 및 발전 흐름도

```text
XOR Problem
  ↓
Hidden Layer
  ↓
MLP
  ↓
Deep Learning
```

---

## 어린이를 위한 3줄 비유 설명

한 줄만으로는 못 나누는 문제가 있어요.  
그래서 중간 층을 하나 더 넣어요.  
MLP는 그렇게 더 똑똑하게 나누는 모델이에요.
