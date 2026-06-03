+++
weight = 128
title = "128. ANN & MLP (인공 신경망 & 다층 퍼셉트론) - 딥러닝의 기본 구조"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[350_ann|ANN]]([[061_artificial_neural_network_ann_neuron_model|인공 신경망]])은 **생물학적 뉴런을 모방**하여 입력→[[267_weight_bias_activation|가중치]] 곱→[[129_activation_function|활성화 함수]]→출력의 구조를 컴퓨터로 구현한 것이며, MLP([[266_mlp_hidden_layers|다층 퍼셉트론]])는 **은닉층(Hidden Layer)이 1개 이상인 피드포워드 신경망**이다.
> 2. **가치**: [[265_single_layer_perceptron_xor|단층 퍼셉트론]]은 XOR 문제를 풀 수 없는(선형 분리 불가) 근본 한계가 있었으나, **은닉층 추가(MLP) + [[272_backpropagation|역전파]]([[272_backpropagation|Backpropagation]])**로 비선형 문제를 해결하며 딥러닝의 기초가 되었다.
> 3. **판단 포인트**: [[129_activation_function|활성화 함수]]([[268_sigmoid_vanishing_gradient|Sigmoid]]→[[269_relu_activation|ReLU]]), [[272_backpropagation|역전파]] [[001_algorithm_definition|알고리즘]], [[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]] 문제와 해결([[269_relu_activation|ReLU]]·BatchNorm·[[287_resnet_skip_connection|ResNet]])을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    MLP 구조                                           │
├───────────────────────────────────────────────────────┤
│  [입력층]    x₁, x₂, ..., xₙ                        │
│     ↓ (가중치 W₁)                                     │
│  [은닉층 1]  h₁ = σ(W₁·x + b₁)                      │
│     ↓ (가중치 W₂)                                     │
│  [은닉층 2]  h₂ = σ(W₂·h₁ + b₂)                     │
│     ↓ (가중치 W₃)                                     │
│  [출력층]    y = softmax(W₃·h₂ + b₃)                 │
│                                                       │
│  학습: 역전파 (Backpropagation)로 가중치 업데이트    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: MLP는 여러 층의 **체(필터)**이다. 입력이 여러 체를 통과하면서 점점 세밀하게 [[104_classification_analysis|분류]]된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[129_activation_function|활성화 함수]] 진화

| 함수 | 특징 | 문제 |
|:---|:---|:---|
| **[[268_sigmoid_vanishing_gradient|Sigmoid]]** | 0~1 출력 | [[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]] |
| **[[070_hyperbolic_tangent_tanh_activation|Tanh]]** | -1~1 출력 | [[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]] |
| **[[269_relu_activation|ReLU]]** | max(0,x) | **현재 표준** |
| **GELU** | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 표준 | [[302_gpt_autoregressive|GPT]]/[[301_bert_mlm|BERT]] 사용 |

- **📢 섹션 요약 비유**: Sigmoid는 느린 수도꼭지(미세 조절), ReLU는 빠른 [[238_switch_operation_principles|스위치]](on/off)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[265_single_layer_perceptron_xor|단층 퍼셉트론]] | MLP |
|:---|:---|:---|
| **비선형** | 불가 (XOR ✗) | **가능** |
| **깊이** | 0 은닉층 | **1+ 은닉층** |
| **학습** | [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] 규칙 | **[[272_backpropagation|역전파]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### MLP의 위치
- Transformer의 FFN(Feed-Forward Network) = **2층 MLP**.
- 현대 딥러닝: [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]·[[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]·[[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 모두 MLP를 구성 요소로 포함.

---

## Ⅴ. 기대효과 및 결론

MLP는 **딥러닝의 가장 기본 빌딩 블록**이며, Transformer의 FFN으로 현재까지 핵심 역할을 수행한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]]** | 단층 신경망 (XOR 불가) |
| **MLP** | [[266_mlp_hidden_layers|다층 퍼셉트론]] (비선형 가능) |
| **[[272_backpropagation|역전파]]** | MLP 학습 [[001_algorithm_definition|알고리즘]] |
| **[[269_relu_activation|ReLU]]** | 현대 표준 [[129_activation_function|활성화 함수]] |
| **FFN** | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 내 MLP |

### 📈 관련 키워드 및 발전 흐름도

```text
[퍼셉트론 (Rosenblatt, 1958)]
    │
    ▼
[XOR 문제 (Minsky, 1969) — 인공지능 겨울]
    │
    ▼
[MLP + 역전파 (Rumelhart, 1986)]
    │
    ▼
[딥러닝 (Hinton, 2006~) — GPU·ReLU·데이터]
    │
    ▼
[현재: MLP-Mixer / gMLP — MLP만으로 Vision 처리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]]은 **1단 필터**예요. 간단한 것만 걸러낼 수 있어요.
2. MLP는 **여러 단 필터**예요. 복잡한 것도 **세밀하게 [[104_classification_analysis|분류]]**할 수 있어요.
3. 틀린 답이 나오면 **[[272_backpropagation|역전파]](피드백)**로 필터를 조정해서 더 정확해져요!
