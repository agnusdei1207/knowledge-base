+++
title = "74. 순전파 (Forward Propagation) - 신경망 계산 흐름"
weight = 74
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[271_forward_propagation|순전파]]는 입력이 신경망의 각 층을 지나 출력으로 계산되는 과정이다.
> 2. **가치**: 예측값을 만들고 손실을 계산하는 출발점이다.
> 3. **판단**: [[267_weight_bias_activation|가중치]]와 [[129_activation_function|활성화 함수]]가 층마다 적용된다.

---

## Ⅰ. 개요 및 필요성

신경망은 입력을 그냥 내보내지 않는다. 여러 층을 거쳐 계산한다.

그 계산 흐름이 [[271_forward_propagation|순전파]]다.

- **📢 섹션 요약 비유**: 공을 여러 사람에게 차례로 넘기는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Input
  ↓ weighted sum
Activation
  ↓
Output
```

| 요소 | 의미 |
| :-- | :-- |
| [[267_weight_bias_activation|Weight]] | [[267_weight_bias_activation|가중치]] |
| [[094_bias|Bias]] | 편향 |
| Activation | 비선형 함수 |

[[271_forward_propagation|순전파]]는 각 층에서 선형 결합 후 활성화를 거쳐 다음 층으로 전달된다.

- **📢 섹션 요약 비유**: 여러 필터를 차례로 통과하는 물건이다.

---

## Ⅲ. 비교 및 연결

| 단계 | 역할 |
| :-- | :-- |
| [[235_forward_backward_chaining|Forward]] | 계산 |
| Loss | 오차 |
| Backward | [[272_backpropagation|역전파]] |

| 관련 | 의미 |
| :-- | :-- |
| Neural Network | 구조 |
| Prediction | 출력 |

[[271_forward_propagation|순전파]]는 [[272_backpropagation|역전파]]와 짝을 이뤄 학습을 완성한다.

- **📢 섹션 요약 비유**: 앞으로 보내고 뒤로 돌아오며 배우는 과정이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 입력→은닉→출력 흐름을 아는가?
2. [[267_weight_bias_activation|가중치]]와 편향을 이해하는가?
3. [[129_activation_function|활성화 함수]]의 역할을 아는가?
4. 손실 계산과 연결하는가?
5. [[272_backpropagation|역전파]]와 구분하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[271_forward_propagation|순전파]]와 [[272_backpropagation|역전파]]를 혼동하는 설계
- 선형 결합만 보고 끝나는 설계
- [[129_activation_function|활성화 함수]]를 무시하는 설계
- 층별 계산을 대충 보는 설계

기술사 관점에서는 [[271_forward_propagation|순전파]]를 "신경망의 예측 계산 흐름"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 입력이 순서대로 계산되어 결과가 나온다.

---

## Ⅴ. 기대효과 및 결론

[[271_forward_propagation|순전파]]는 신경망이 예측값을 내는 기본 과정이다.

결론적으로 [[271_forward_propagation|순전파]]는 입력이 층을 통과하며 출력이 되는 계산 흐름이다.

- **📢 섹션 요약 비유**: 공이 앞으로 넘어가며 결과가 만들어진다.

---

## 관련 개념 맵

```text
Input
  ↓
Forward Propagation
  ↓
Output
```

---

## 관련 키워드 및 발전 흐름도

```text
Neural Network
  ↓
Forward Propagation
  ↓
Backward Propagation
```

---

## 어린이를 위한 3줄 비유 설명

앞으로 차례차례 가요.  
중간에서 계산해요.  
[[271_forward_propagation|순전파]]는 그런 과정이에요.
