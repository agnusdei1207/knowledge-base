+++
weight = 129
title = "129. 활성화 함수 (Activation Function) - 신경망의 비선형 변환 핵심"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 활성화 함수는 **신경망의 각 뉴런 출력에 적용되는 비선형 변환**이며, 이것이 없으면 아무리 깊은 신경망도 **단일 선형 변환과 동일**(표현력 없음)하다.
> 2. **가치**: [[268_sigmoid_vanishing_gradient|Sigmoid]]→[[070_hyperbolic_tangent_tanh_activation|Tanh]]→[[269_relu_activation|ReLU]]→GELU→SwiGLU의 발전이 딥러닝 [[282_performance_tactics|성능]]을 직접적으로 향상시켰으며, **ReLU가 [[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]] 문제를 해결**하여 딥러닝 르네상스를 열었다.
> 3. **판단 포인트**: [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]/MLP는 [[269_relu_activation|ReLU]], Transformer는 GELU, 최신 [[263_llm_large_language_model|LLM]](Llama)은 SwiGLU가 표준이며, 출력층은 [[104_classification_analysis|분류]]([[270_softmax|Softmax]])·회귀(Linear)·[[130_probability|확률]]([[268_sigmoid_vanishing_gradient|Sigmoid]])로 구분한다.

---

## Ⅰ. 개요 및 필요성

```text
활성화 함수 비교:
Sigmoid: σ(x) = 1/(1+e⁻ˣ)     → 0~1, Vanishing
ReLU:    f(x) = max(0, x)       → 현재 표준, Dead Neuron
GELU:    f(x) = x·Φ(x)         → Transformer 표준
SwiGLU:  f(x) = Swish(xW₁)⊙xW₂ → LLM 최신
```

- **📢 섹션 요약 비유**: 활성화 함수는 신경망의 **[[238_switch_operation_principles|스위치]]**이다. [[238_switch_operation_principles|스위치]]가 없으면 전기(정보)가 그냥 흐를 뿐 아무 기능을 못 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 함수 | 범위 | 장점 | 문제 |
|:---|:---|:---|:---|
| **[[268_sigmoid_vanishing_gradient|Sigmoid]]** | 0~1 | [[130_probability|확률]] 출력 | Vanishing |
| **[[269_relu_activation|ReLU]]** | 0~∞ | **Vanishing 해결** | Dead Neuron |
| **GELU** | 연속 | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 최적 | - |
| **SwiGLU** | 연속 | **[[263_llm_large_language_model|LLM]] 최고 [[282_performance_tactics|성능]]** | 파라미터↑ |

---

## Ⅲ. 비교 및 연결

| 용도 | 함수 |
|:---|:---|
| **은닉층** | [[269_relu_activation|ReLU]] / GELU / SwiGLU |
| **이진 [[104_classification_analysis|분류]]** | [[268_sigmoid_vanishing_gradient|Sigmoid]] |
| **다중 [[104_classification_analysis|분류]]** | [[270_softmax|Softmax]] |
| **회귀** | Linear (없음) |

---

## Ⅳ~Ⅴ. 결론

활성화 함수는 **딥러닝의 비선형 표현력의 원천**이며, [[269_relu_activation|ReLU]]→GELU→SwiGLU의 진화가 모델 [[282_performance_tactics|성능]]을 직접 견인한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[269_relu_activation|ReLU]]** | [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]/MLP 표준 |
| **GELU** | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 표준 |
| **SwiGLU** | [[263_llm_large_language_model|LLM]] 최신 (Llama/PaLM) |
| **[[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]** | [[268_sigmoid_vanishing_gradient|Sigmoid]]/[[070_hyperbolic_tangent_tanh_activation|Tanh]] 문제 |
| **[[270_softmax|Softmax]]** | 출력층 [[104_classification_analysis|분류]] 활성화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sigmoid (1980s)] → [Tanh (1990s)] → [ReLU (2010, Nair)]
    → [GELU (2016)] → [SwiGLU (2022, PaLM/Llama)]
    → [현재: 학습 가능 활성화 (KAN, 2024)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 활성화 함수는 신경망의 **[[238_switch_operation_principles|스위치]]**예요. 켜야(비선형) 뇌가 **생각**할 수 있어요.
2. 옛날 [[238_switch_operation_principles|스위치]]([[268_sigmoid_vanishing_gradient|Sigmoid]])는 **느렸지만**, 새 [[238_switch_operation_principles|스위치]]([[269_relu_activation|ReLU]])는 빠르고 강해요.
3. 최신 [[238_switch_operation_principles|스위치]](SwiGLU)는 AI가 **더 똑똑하게 생각**할 수 있게 해줘요!
