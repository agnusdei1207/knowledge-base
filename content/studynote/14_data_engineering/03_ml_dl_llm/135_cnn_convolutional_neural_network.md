+++
title = "135. CNN (Convolutional Neural Network) - 합성곱 신경망의 구조와 원리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CNN은 <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a>(<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/">Convolution</a>) 연산으로 입력의 지역적 패턴(엣지·텍스처·형태)을 계층적으로 추출</strong>하는 신경망이며, 이미지·영상 처리의 핵심 아키텍처이다.
> 2. **가치**: 전결합층([FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/))은 이미지를 1D로 펼쳐 공간 정보를 잃지만, CNN은 <strong>2D 구조를 유지하며 파라미터를 공유(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 공유)</strong>하여 효율적으로 학습한다.
> 3. **판단 포인트**: Conv→[ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/)→Pool의 반복이 기본 구조이며, AlexNet→VGGNet→[ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/)→EfficientNet의 발전과 함께 Vision [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)(ViT)가 대안으로 부상했다.

---

## Ⅰ. 개요 및 필요성

```text
CNN 구조: [Conv → ReLU → Pool] × N → FC → Softmax
  Conv: 필터(커널)로 지역 특징 추출
  Pool: 다운샘플링 (Max/Average)
  FC:   분류 출력
```

- **📢 섹션 요약 비유**: CNN은 **돋보기로 그림을 부분적으로 훑으며** 패턴을 찾는 것이다. 전체를 한 번에 보는 것보다 효율적이다.

---

## Ⅱ~Ⅴ. 결론

CNN은 <strong>컴퓨터 비전의 기본 아키텍처</strong>이며, ResNet의 Skip Connection이 딥러닝 심화의 돌파구였다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Conv** | [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (패턴 추출) |
| **Pool** | 다운샘플링 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">ResNet</a></strong> | Skip Connection |
| **EfficientNet** | 효율적 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| **ViT** | Vision [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) (대안) |

### 📈 관련 키워드 및 발전 흐름도

```text
[LeNet (1998)] → [AlexNet (2012, ImageNet 우승)]
    → [VGGNet (2014)] → [ResNet (2015, Skip Connection)]
    → [EfficientNet (2019)] → [ViT (2020, Transformer 기반)]
    → [현재: ConvNeXt — CNN의 반격]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CNN은 <strong>돋보기로 그림의 부분</strong>을 하나씩 살펴보는 거예요.
2. 먼저 <strong>선(엣지)</strong>을 찾고, 다음에 **모양(형태)**, 마지막에 <strong>물체(고양이!)</strong>를 인식해요.
3. 사진 인식·얼굴 인식 등 <strong>눈(비전) 관련 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>의 핵심이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 258

← **이전**: [134. 정규화 기법 (Regularization) - Dropout·BatchNorm·L1/L2](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/)
**다음**: [136. RNN (Recurrent Neural Network) - 순환 신경망과 시퀀스 처리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/136_rnn_recurrent_neural_network/) →

---
