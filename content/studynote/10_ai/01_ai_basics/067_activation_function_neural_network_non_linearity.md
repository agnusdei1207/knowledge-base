---
title: "067. Activation Function Neural Network Non Linearity"
tags:
  - "ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 신경망의 선형 결합 결과에 비선형성을 넣어 표현력을 높이는 함수다.
> 2. **가치**: [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)가 없으면 깊은 신경망도 결국 하나의 선형 모델로 붕괴된다.
> 3. **판단**: 함수 선택은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/), 계산 비용을 함께 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

신경망은 입력을 단순히 더하는 것만으로는 복잡한 패턴을 배울 수 없다. 비선형성이 있어야 학습이 가능해진다.

[활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 뉴런이 다음 층으로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보낼지, 얼마나 보낼지 결정한다.

- **📢 섹션 요약 비유**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 켤지 말지 결정하는 문지기다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Weighted Sum
  v
Activation Function
  v
Non-linear Output
```

| 함수 | 특징 |
| :-- | :-- |
| [Sigmoid](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | 0~1, [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 해석 가능 |
| [Tanh](/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/) | -1~1, 중심화 |
| [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) | 단순하고 빠름 |
| [Softmax](/studynote/10_ai/03_llm_nlp/270_softmax/) | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 출력 |

[활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 선형 조합을 비선형 변환으로 바꾼다. 그래서 층을 많이 쌓아도 표현력이 유지된다.

- **📢 섹션 요약 비유**: 같은 재료라도 굽고 익히면 다른 맛이 난다.

---

## Ⅲ. 비교 및 연결

| 함수 | 장점 | 단점 |
| :-- | :-- | :-- |
| [Sigmoid](/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 해석 | [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) |
| [Tanh](/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/) | 중심화 | 포화 영역 |
| [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) | 단순/빠름 | 죽은 뉴런 |
| [Softmax](/studynote/10_ai/03_llm_nlp/270_softmax/) | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 적합 | 출력층 전용 |

| 역할 | 의미 |
| :-- | :-- |
| Non-linearity | 복잡한 경계 학습 |
| Gradient Flow | 학습 안정성 |

[활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 신경망의 성질을 바꾸는 핵심 요소다. 어떤 함수를 쓰느냐가 학습 속도와 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 좌우한다.

- **📢 섹션 요약 비유**: 문을 열 때 손잡이 모양이 다르면 힘 주는 방식도 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 문제에 맞는 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)를 선택했는가?
2. [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/)과 폭주를 고려했는가?
3. 출력층과 은닉층의 함수를 구분하는가?
4. 계산 비용과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 함께 봤는가?
5. [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) 계열의 장단을 아는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)를 생략하는 설계
- 모든 층에 같은 함수를 무작정 쓰는 설계
- 포화 구간과 죽은 뉴런을 무시하는 설계
- 출력층 함수와 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 혼동하는 설계

기술사 관점에서는 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)를 "비선형성을 넣는 장치"로 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: 직선만 그리면 그림이 단조롭고, 꺾임이 있어야 형태가 살아난다.

---

## Ⅴ. 기대효과 및 결론

[활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 신경망이 복잡한 패턴을 학습하게 하는 필수 요소다. 그래서 DNN의 성패에 직접 영향을 준다.

결론적으로 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 신경망의 비선형 엔진이다.

- **📢 섹션 요약 비유**: 불을 켜고 끄는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 있어야 기계가 일한다.

---

## 관련 개념 맵

```text
Weighted Sum
  v
Activation Function
  v
Non-linearity
  v
Deep Learning
```

---

## 관련 키워드 및 발전 흐름도

```text
Perceptron
  v
Activation Function
  v
MLP / DNN
  v
Deep Learning
```

---

## 어린이를 위한 3줄 비유 설명

그냥 더하기만 하면 단순해요.
중간에 꺾어 주는 함수가 필요해요.
[활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)는 그런 꺾임이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 420

<- **이전**: [66. 가중치 (Weight, W) / 편향 (Bias, b) - 선형 방정식의 파라미터 (y = Wx + b)](/studynote/10_ai/01_ai_basics/066_weight_bias_linear_equation/)
**다음**: [68. 계단 함수 (Step Function) - 0 이하면 0, 0 이상이면 1 반환 (미분 불가)](/studynote/10_ai/01_ai_basics/068_step_function_activation/) ->

---
