---
title: 70. 하이퍼볼릭 탄젠트 (tanh) - -1~1 사이 반환, 중심이 0으로 수렴 (시그모이드보다 우수)
tags:
- ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: tanh는 입력을 -1에서 1 사이로 [[347_compaction|압축]]하는 S자형 [[129_activation_function|활성화 함수]]다.
> 2. **가치**: 출력이 0 중심이라 [[268_sigmoid_vanishing_gradient|시그모이드]]보다 학습이 안정적인 경우가 많다.
> 3. **판단**: 여전히 포화 구간이 있어 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 문제는 완전히 사라지지 않는다.

---

## Ⅰ. 개요 및 필요성

[[268_sigmoid_vanishing_gradient|시그모이드]]의 출력이 0 중심이 아니어서 생기는 불편함을 줄이기 위해 tanh가 많이 쓰였다.

은닉층에서 중심화가 필요한 경우 특히 유용하다.

- **📢 섹션 요약 비유**: 양쪽으로 균형 잡힌 저울이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Input
  ↓ tanh
-1 ~ 1
```

| 특징 | 의미 |
| :-- | :-- |
| [[585_zero_skipping|Zero]]-centered | 중심이 0 |
| S-curve | 부드러운 비선형 |
| Saturation | 양끝 포화 |

tanh는 [[268_sigmoid_vanishing_gradient|시그모이드]]보다 출력이 균형적이어서 [[267_weight_bias_activation|가중치]] 업데이트가 더 안정적일 수 있다.

- **📢 섹션 요약 비유**: 가운데를 기준으로 위아래가 고르게 퍼지는 미끄럼틀이다.

---

## Ⅲ. 비교 및 연결

| 함수 | 장점 | 단점 |
| :-- | :-- | :-- |
| [[268_sigmoid_vanishing_gradient|Sigmoid]] | [[130_probability|확률]] 해석 | 0 중심 아님 |
| tanh | 0 중심 | 포화 |
| [[269_relu_activation|ReLU]] | 단순/빠름 | 죽은 뉴런 |

| 맥락 | 의미 |
| :-- | :-- |
| Hidden Layer | 자주 사용 |
| Output Layer | 보통 덜 사용 |

tanh는 [[268_sigmoid_vanishing_gradient|시그모이드]]보다 나은 경우가 많지만, [[269_relu_activation|ReLU]] 계열이 대세가 된 이유도 함께 이해해야 한다.

- **📢 섹션 요약 비유**: 균형은 좋지만, 아주 긴 언덕에서는 역시 힘이 빠진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 0 중심 출력의 장점을 아는가?
2. [[268_sigmoid_vanishing_gradient|시그모이드]]와 비교할 수 있는가?
3. 포화 구간의 문제를 이해하는가?
4. 은닉층에서의 사용 이유를 아는가?
5. ReLU와의 [[083_relationship_in_er_model|관계]]를 설명할 수 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- tanh를 만능으로 보는 설계
- 포화 문제를 무시하는 설계
- 출력층에 무조건 쓰는 설계
- [[268_sigmoid_vanishing_gradient|시그모이드]]와 구분하지 않는 설계

기술사 관점에서는 tanh를 "0 중심의 부드러운 [[129_activation_function|활성화 함수]]"로 설명해야 한다.

- **📢 섹션 요약 비유**: 가운데가 잘 맞아야 흔들림이 덜하다.

---

## Ⅴ. 기대효과 및 결론

tanh는 [[268_sigmoid_vanishing_gradient|시그모이드]]보다 학습 안정성이 좋은 경우가 많았다. 그래서 딥러닝 [[459_quic_fec_forward_error_correction|초기]] 은닉층에서 중요했다.

결론적으로 tanh는 -1~1 범위의 중심화된 [[129_activation_function|활성화 함수]]다.

- **📢 섹션 요약 비유**: 양쪽이 균형 잡힌 부드러운 문지기다.

---

## 관련 개념 맵

```text
Input
  ↓
tanh
  ↓
Zero-centered Output
  ↓
Hidden Layer
```

---

## 관련 키워드 및 발전 흐름도

```text
Sigmoid
  ↓
tanh
  ↓
ReLU
  ↓
Deep Learning
```

---

## 어린이를 위한 3줄 비유 설명

위아래가 균형 잡혀 있어요.  
가운데가 0이에요.  
tanh는 그런 부드러운 함수예요.
