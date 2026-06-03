+++
title = "73. 소프트맥스 함수 (Softmax) - 다중 클래스 분류 시 출 력층 적용, 결과값 총합을 1로 만들어 확률화"

[taxonomies]
tags = ["ai"]

[extra]
tags = ["ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 여러 점수를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포로 바꾸는 출력층 함수다.
> 2. **가치**: 다중 클래스 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 가장 높은 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 클래스를 쉽게 선택하게 한다.
> 3. **판단**: 입력 점수의 상대적 크기를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)한다.

---

## Ⅰ. 개요 및 필요성

신경망 출력은 점수로 나오기 쉽다. 사람이 이해하려면 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 좋다.

[소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)가 그 변환을 한다.

- **📢 섹션 요약 비유**: 여러 후보 점수를 100점 만점 비율로 바꾸는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Logits
  ↓ softmax
Probabilities (sum=1)
```

| 요소 | 의미 |
| :-- | :-- |
| Logit | 비정규화 점수 |
| Exponent | 강조 |
| [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |

[소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 큰 값을 더 크게 보이게 하고, 전체를 1로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)한다.

- **📢 섹션 요약 비유**: 점수판을 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)표로 바꾸는 마법이다.

---

## Ⅲ. 비교 및 연결

| 함수 | 역할 |
| :-- | :-- |
| [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) | 다중 클래스 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)화 |
| [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | 이진 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)화 |

| 특징 | 의미 |
| :-- | :-- |
| Sum to 1 | 총합 1 |
| Argmax | 가장 큰 값 선택 |

[소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 다중 클래스 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 출력층 표준이다.

- **📢 섹션 요약 비유**: 여러 후보 중 누가 몇 퍼센트인지 나눠 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 다중 클래스 문제인가?
2. logits를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 바꾸는가?
3. 총합이 1인지 이해하는가?
4. argmax로 선택하는가?
5. Sigmoid와 구분하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 이진 문제에 무조건 쓰는 설계
- 점수와 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)을 혼동하는 설계
- 수치 안정성을 무시하는 설계
- 클래스 수를 고려하지 않는 설계

기술사 관점에서는 [소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)를 "다중 클래스 출력 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 함수"로 설명해야 한다.

- **📢 섹션 요약 비유**: 점수를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 바꿔 주는 정리기다.

---

## Ⅴ. 기대효과 및 결론

[소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 결과 해석을 쉽고 일관되게 만든다.

결론적으로 [소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 점수를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 바꾸는 출력층 함수다.

- **📢 섹션 요약 비유**: 여러 점수를 1이 되게 나눠 주는 것이다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Logits</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Softmax</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Probabilities</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Classification</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Softmax</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Multiclass Classification</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Probability Output</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

점수를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 바꿔요.  
합치면 1이 돼요.  
[소프트맥스](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)는 그런 함수예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 420

← **이전**: [72. Leaky ReLU / ELU - ReLU의 죽은 뉴런(Dying ReLU, 음수 입력 시 가중치 미갱신) 문제 해결 (음수 구간에](/knowledge-base/studynote/10_ai/01_ai_basics/072_leaky_relu_elu_dying_relu_solution/)
**다음**: [74. 순전파 (Forward Propagation) - 신경망 계산 흐름](/knowledge-base/studynote/10_ai/01_ai_basics/074_forward_propagation_neural_network/) →

---
