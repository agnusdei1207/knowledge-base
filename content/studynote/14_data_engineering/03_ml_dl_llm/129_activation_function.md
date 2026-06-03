+++
title = "129. 활성화 함수 (Activation Function) - 신경망의 비선형 변환 핵심"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 활성화 함수는 **신경망의 각 뉴런 출력에 적용되는 비선형 변환**이며, 이것이 없으면 아무리 깊은 신경망도 **단일 선형 변환과 동일**(표현력 없음)하다.
> 2. **가치**: [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)→[Tanh](/knowledge-base/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/)→[ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)→GELU→SwiGLU의 발전이 딥러닝 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 직접적으로 향상시켰으며, **ReLU가 [Vanishing Gradient](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/) 문제를 해결**하여 딥러닝 르네상스를 열었다.
> 3. **판단 포인트**: [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)/MLP는 [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/), Transformer는 GELU, 최신 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(Llama)은 SwiGLU가 표준이며, 출력층은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/))·회귀(Linear)·[확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/))로 구분한다.

---

## Ⅰ. 개요 및 필요성

```text
활성화 함수 비교:
Sigmoid: σ(x) = 1/(1+e⁻ˣ)     → 0~1, Vanishing
ReLU:    f(x) = max(0, x)       → 현재 표준, Dead Neuron
GELU:    f(x) = x·Φ(x)         → Transformer 표준
SwiGLU:  f(x) = Swish(xW₁)⊙xW₂ → LLM 최신
```

- **📢 섹션 요약 비유**: 활성화 함수는 신경망의 **[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)**이다. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 없으면 전기(정보)가 그냥 흐를 뿐 아무 기능을 못 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 함수 | 범위 | 장점 | 문제 |
|:---|:---|:---|:---|
| **[Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)** | 0~1 | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 출력 | Vanishing |
| **[ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)** | 0~∞ | **Vanishing 해결** | Dead Neuron |
| **GELU** | 연속 | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 최적 | - |
| **SwiGLU** | 연속 | **[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)** | 파라미터↑ |

---

## Ⅲ. 비교 및 연결

| 용도 | 함수 |
|:---|:---|
| **은닉층** | [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) / GELU / SwiGLU |
| **이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)** | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) |
| **다중 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)** | [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) |
| **회귀** | Linear (없음) |

---

## Ⅳ~Ⅴ. 결론

활성화 함수는 **딥러닝의 비선형 표현력의 원천**이며, [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)→GELU→SwiGLU의 진화가 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 직접 견인한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)** | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)/MLP 표준 |
| **GELU** | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 표준 |
| **SwiGLU** | [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 최신 (Llama/PaLM) |
| **[Vanishing Gradient](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/)** | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)/[Tanh](/knowledge-base/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/) 문제 |
| **[Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)** | 출력층 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 활성화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sigmoid (1980s)] → [Tanh (1990s)] → [ReLU (2010, Nair)]
    → [GELU (2016)] → [SwiGLU (2022, PaLM/Llama)]
    → [현재: 학습 가능 활성화 (KAN, 2024)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 활성화 함수는 신경망의 **[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)**예요. 켜야(비선형) 뇌가 **생각**할 수 있어요.
2. 옛날 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/))는 **느렸지만**, 새 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)([ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/))는 빠르고 강해요.
3. 최신 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(SwiGLU)는 AI가 **더 똑똑하게 생각**할 수 있게 해줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 258

← **이전**: [128. ANN & MLP (인공 신경망 & 다층 퍼셉트론) - 딥러닝의 기본 구조](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/128_ann_mlp/)
**다음**: [130. ReLU 활성화 함수 - 딥러닝 르네상스를 연 비선형 변환](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/130_relu_activation_function/) →

---
