+++
title = "130. ReLU 활성화 함수 - 딥러닝 르네상스를 연 비선형 변환"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)([Rectified Linear Unit](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/))는 **f(x) = max(0, x)**로 정의되는 [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)이며, 양수는 그대로 통과, 음수는 0으로 차단하는 단순한 구조로 **[Vanishing Gradient](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/) 문제를 해결**하여 딥러닝을 실용화했다.
> 2. **가치**: Sigmoid의 [기울기 소실](/knowledge-base/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/)로 깊은 신경망 학습이 불가능했던 한계를 ReLU가 극복하여 **2012년 AlexNet의 ImageNet 우승**을 이끌었다.
> 3. **판단 포인트**: Dead Neuron(음수 영역 영구 0) 문제가 있어 Leaky [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)·PReLU·ELU 등 변형이 존재하며, Transformer에서는 GELU·SwiGLU가 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
ReLU: f(x) = max(0, x)
  x > 0 → x (그대로), x ≤ 0 → 0 (차단)
  기울기: x > 0 → 1, x ≤ 0 → 0
  → Vanishing Gradient 없음 (기울기=1 유지)
```

- **📢 섹션 요약 비유**: ReLU는 문(양수=열림, 음수=닫힘)이다. Sigmoid는 반쯤 열린 문([기울기 소실](/knowledge-base/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) 위험).

---

## Ⅱ. 아키텍처 및 핵심 원리

| 변형 | 수식 | 특징 |
|:---|:---|:---|
| **Leaky [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)** | max(0.01x, x) | Dead Neuron 방지 |
| **PReLU** | max(αx, x) | α 학습 |
| **ELU** | α(eˣ-1), x | 부드러운 음수 |

---

## Ⅲ~Ⅴ. 결론

ReLU는 **딥러닝의 가장 기본적이고 중요한 [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)**이며, [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)/MLP에서 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)** | max(0,x) — [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 표준 |
| **[Vanishing Gradient](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/)** | Sigmoid의 문제 → [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) 해결 |
| **Dead Neuron** | ReLU의 문제 → Leaky [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) 해결 |
| **GELU** | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 표준 |
| **AlexNet** | ReLU를 최초 대규모 적용 (2012) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sigmoid (1980s)] → [ReLU (2010, Nair)] → [AlexNet ReLU 성공 (2012)]
    → [Leaky/PReLU (2015)] → [GELU (2016, Transformer)]
    → [SwiGLU (2022, LLM)] → [현재: KAN (2024)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ReLU는 **문**이에요. 좋은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)(양수)는 **열어서 통과**, 나쁜 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)(음수)는 **닫아서 차단**해요.
2. 옛날 문([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/))은 **반만 열려서** [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 점점 약해졌어요(Vanishing).
3. [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) 덕분에 **깊은 신경망**도 잘 학습할 수 있게 됐답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 258

← **이전**: [129. 활성화 함수 (Activation Function) - 신경망의 비선형 변환 핵심](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)
**다음**: [131. 손실 함수·옵티마이저·경사 하강법 - 딥러닝 학습의 3대 축](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/131_loss_function_optimizer_gradient_descent/) →

---
