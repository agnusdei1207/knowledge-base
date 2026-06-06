---
title: "069. Sigmoid Function Vanishing Gradient"
tags:
  - "ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 함수는 입력을 0과 1 사이로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 S자형 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)다.
> 2. **가치**: [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석이 가능해 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 신경망과 출력층에서 많이 쓰였다.
> 3. **판단**: 포화 구간에서 기울기가 작아져 [vanishing gradient](/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/) 문제를 만들 수 있다.

---

## Ⅰ. 개요 및 필요성

[시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 값을 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)처럼 다루고 싶을 때 직관적이다. 그러나 깊은 신경망에서는 학습을 방해할 수 있다.

그래서 현대 은닉층에서는 [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) 계열이 더 선호된다.

- **📢 섹션 요약 비유**: 모든 값을 0과 1 사이로 눌러 담는 스펀지다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Input
  v sigmoid
0 ~ 1
```

| 특징 | 의미 |
| :-- | :-- |
| S-curve | 부드러운 변환 |
| Saturation | 양끝에서 포화 |
| Derivative | 양끝에서 작아짐 |

[시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 출력이 부드럽고 해석이 쉽지만, 양끝으로 갈수록 기울기가 작아진다.

- **📢 섹션 요약 비유**: 미끄러운 언덕의 위아래 끝에서 잘 안 움직이는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 함수 | 장점 | 단점 |
| :-- | :-- | :-- |
| [Sigmoid](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석 | [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) |
| [Tanh](/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/) | 중심화 | 포화 |
| [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) | 단순/빠름 | 죽은 뉴런 |

| 맥락 | 의미 |
| :-- | :-- |
| Output Layer | 이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| Hidden Layer | 비선호 |

[시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 신경망과 [로지스틱 회귀](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)에서 중요한 역할을 했지만, 깊은 모델에서는 한계가 드러났다.

- **📢 섹션 요약 비유**: 부드럽지만 너무 눌리면 힘이 잘 전달되지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)의 출력 범위를 아는가?
2. 포화와 [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/)을 설명할 수 있는가?
3. 출력층과 은닉층의 사용 차이를 아는가?
4. 현대 대안([ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) 등)을 비교할 수 있는가?
5. [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석의 장단을 아는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 은닉층에 무조건 [시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)를 쓰는 설계
- 포화 구간의 [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/)을 무시하는 설계
- 출력 해석만 보고 학습성을 무시하는 설계
- [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) 계열과 구분 없이 쓰는 설계

기술사 관점에서는 [시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)를 "[확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 친화적이지만 깊은 학습에는 약한 함수"로 설명해야 한다.

- **📢 섹션 요약 비유**: 보기 좋지만 깊게 누르면 힘이 덜 전달된다.

---

## Ⅴ. 기대효과 및 결론

[시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 직관적 출력을 제공하지만, 딥러닝 학습에서는 한계가 있다.

결론적으로 [시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 0~1 범위의 부드러운 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)다.

- **📢 섹션 요약 비유**: 부드러운 문지기지만 오래 쓰면 지친다.

---

## 관련 개념 맵

```text
Input
  v
Sigmoid
  v
Probability-like Output
  v
Binary Classification
```

---

## 관련 키워드 및 발전 흐름도

```text
Step Function
  v
Sigmoid
  v
Vanishing Gradient
  v
ReLU
```

---

## 어린이를 위한 3줄 비유 설명

값을 0과 1 사이로 눌러요.
부드럽지만 끝에서는 힘이 약해요.
[시그모이드](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)는 그런 함수예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 420

<- **이전**: [68. 계단 함수 (Step Function) - 0 이하면 0, 0 이상이면 1 반환 (미분 불가)](/studynote/10_ai/01_ai_basics/068_step_function_activation/)
**다음**: [70. 하이퍼볼릭 탄젠트 (tanh) - -1~1 사이 반환, 중심이 0으로 수렴 (시그모이드보다 우수)](/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/) ->

---
