+++
weight = 103
title = "103. CNN 주요 아키텍처의 발전 (AlexNet, VGG, ResNet 등)"
date = "2026-04-10"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 주요 아키텍처 발전은 신경망의 층(Layer)을 더 깊게(Deep) 쌓으면서도 연산량과 최적화 문제를 해결하기 위한 구조적 혁신의 역사다.
> 2. **가치**: [[129_activation_function|활성화 함수]]([[269_relu_activation|ReLU]]), 필터 크기 최적화(3x3), [[430_index_fast_full_scan|병렬]] 연산(Inception), 잔차 연결(Skip Connection) 등의 기법을 통해 이미지 인식 오류율을 인간 이하 수준으로 낮추었다.
> 3. **판단 포인트**: 실무 적용 시 무조건 최신 아키텍처를 고집하기보다, 가용 컴퓨팅 자원([[418_gpu|GPU]] 메모리, 연산력)과 정확도 간의 트레이드오프를 고려해 모델을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] ([[089_CNN_Convolutional|Convolutional Neural Network]]) 아키텍처는 컴퓨터 비전 분야에서 이미지의 특징을 스스로 학습하는 인공신경망 구조다. 1990년대 LeNet-5가 [[228_cnn_1d_2d_3d_video_medical|합성곱]]([[284_convolution_stride_padding|Convolution]])과 [[285_pooling_layer|풀링]]([[285_pooling_layer|Pooling]])을 반복하는 기본 골격을 제시했지만, 컴퓨팅 파워의 한계와 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 문제로 오랫동안 암흑기를 겪었다. 

이러한 한계를 극복하고 모델의 [[282_performance_tactics|성능]]을 비약적으로 높이기 위해, 학계는 "어떻게 하면 신경망을 더 깊게 쌓을 수 있을까?"에 집중했다. 깊은 신경망은 더 복잡하고 추상적인 특징을 추출할 수 있지만, 파라미터 폭발과 학습 정체라는 치명적인 문제를 동반한다. 따라서 이를 해결하기 위한 혁신적인 구조 변경이 필수적이었으며, 그 결과물들이 오늘날 딥러닝의 부흥을 이끈 전설적인 아키텍처들이다.

- **📢 섹션 요약 비유**: 건물(신경망)을 높이 지으려면 단순히 벽돌만 많이 쌓는다고 되는 것이 아니라, 튼튼한 철골 구조(새로운 아키텍처)와 고속 엘리베이터(최적화 기법)가 필요했던 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 아키텍처의 발전은 연산 효율성을 높이면서 깊이를 극대화하는 방향으로 이루어졌다.

1. **AlexNet (2012)**: 딥러닝 르네상스의 시작. 기존의 [[268_sigmoid_vanishing_gradient|Sigmoid]] 대신 **[[269_relu_activation|ReLU]] ([[269_relu_activation|Rectified Linear Unit]])** [[129_activation_function|활성화 함수]]를 도입하여 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 문제를 완화하고 학습 속도를 높였다. 또한 [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]] 처리와 Dropout을 통해 과적합([[245_overfitting_variance|Overfitting]])을 [[656_ir_containment|억제]]했다.
2. **VGGNet (2014)**: 구조의 단순화. 5x5, 7x7 같은 큰 필터를 버리고, 오직 **3x3 [[228_cnn_1d_2d_3d_video_medical|합성곱]] 필터**만을 중첩 사용했다. 작은 필터를 겹쳐 쓰면 파라미터 수는 줄이면서 비선형성은 증가시킬 수 있다.
3. **GoogLeNet (2014)**: 파라미터 경량화. **인셉션(Inception) [[192_module_independence|모듈]]**을 통해 여러 크기의 필터(1x1, 3x3, 5x5)를 [[430_index_fast_full_scan|병렬]]로 적용하고, [[105_one_by_one_convolution_bottleneck_dimension_reduction|1x1 합성곱]]을 통해 차원을 축소하여 연산량을 획기적으로 줄였다.
4. **[[287_resnet_skip_connection|ResNet]] (2015)**: 깊이의 한계 돌파. 네트워크가 깊어질수록 오히려 [[282_performance_tactics|성능]]이 저하되는 열화 현상을 해결하기 위해 **잔차 연결(Skip Connection)**을 도입했다. 입력값을 출력값에 직접 더해주는(F(x) + x) 우회로를 만들어, 오차 [[130_signal|신호]]가 소실되지 않고 깊은 층까지 전달되게 했다.

```text
┌──────────────────────────────────────────────────────────────┐
│                  ResNet의 핵심: 잔차 연결 (Skip Connection)      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│        [입력 x] ───────┐                                     │
│           │            │ (그대로 복사하여 우회)                 │
│           ▼            │                                     │
│      [Weight Layer]    │                                     │
│           │            │                                     │
│           ▼            │                                     │
│        [ReLU]          │                                     │
│           │            │                                     │
│           ▼            │                                     │
│      [Weight Layer]    │                                     │
│           │            │                                     │
│           ▼            ▼                                     │
│          ( + ) ◀───────┘ 더하기 (F(x) + x)                    │
│           │                                                  │
│           ▼                                                  │
│        [ReLU]  ──▶ 다음 층으로 전달                           │
└──────────────────────────────────────────────────────────────┘
```

이 구조 덕분에 ResNet은 152층이라는 엄청난 깊이에서도 안정적인 학습이 가능해졌다.

- **📢 섹션 요약 비유**: 일반 도로에서는 차가 막히면 끝까지 갈 수 없지만([[088_vanishing_gradient_relu_skip_connection|기울기 소실]]), ResNet은 중간중간 톨게이트를 거치지 않는 다이렉트 고속도로(잔차 연결)를 뚫어 차(오차 [[130_signal|신호]])가 막힘없이 출발지까지 도달하게 만든 것입니다.

---

## Ⅲ. 비교 및 연결

주요 아키텍처들은 각기 다른 철학으로 [[282_performance_tactics|성능]]과 효율의 트레이드오프를 해결했다.

| 아키텍처 | 핵심 기여 (Contribution) | 깊이 (Layers) | 주요 특징 |
|:---|:---|:---|:---|
| **AlexNet** | [[129_activation_function|활성화 함수]]의 혁신 | 8층 | [[269_relu_activation|ReLU]], [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]], [[418_gpu|GPU]] 활용 |
| **VGGNet** | 필터 크기의 최소화 | 16~19층 | 3x3 필터 고집, 구조적 단순함 |
| **GoogLeNet** | 연산 [[192_module_independence|모듈]]의 [[430_index_fast_full_scan|병렬]]화 | 22층 | Inception [[192_module_independence|모듈]], 1x1 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] |
| **[[287_resnet_skip_connection|ResNet]]** | 깊이 확장의 패러다임 전환 | 152층 | Skip Connection, [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 극복 |

VGGNet은 직관적이고 [[132_transfer_learning|전이 학습]]([[132_transfer_learning|Transfer Learning]])에 유리하지만 파라미터 수가 매우 많아 무겁다. 반면 GoogLeNet은 파라미터를 극단적으로 줄였지만 구조가 복잡하다. ResNet은 이 둘의 장점을 넘어서, 단순한 구조를 유지하면서도 깊이를 무한정 늘릴 수 있는 새로운 표준을 제시했다.

- **📢 섹션 요약 비유**: VGG가 무겁지만 튼튼한 정통 벽돌집이라면, GoogLeNet은 가볍고 정교한 조립식 주택이고, ResNet은 중력의 한계를 무시하고 무한정 쌓아 올릴 수 있는 마법의 엘리베이터를 단 마천루입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 이미지 [[104_classification_analysis|분류]], [[288_object_detection_yolo_rcnn|객체 탐지]] 모델을 설계할 때 뼈대(Backbone) 네트워크의 선택은 [[282_performance_tactics|성능]]과 추론 속도를 결정짓는 가장 중요한 판단이다.

1. **학습 자원이 제한된 경우**: 파라미터 수가 많은 VGG는 피하고, GoogLeNet 기반의 모바일용 경량화 모델(MobileNet 등)이나 ResNet의 얕은 [[288_version_ihl_tos_total_length|버전]]([[287_resnet_skip_connection|ResNet]]-50)을 채택해야 한다.
2. **높은 정확도가 최우선인 경우**: [[287_resnet_skip_connection|ResNet]]-101 이상이나 그 발전형(ResNeXt, DenseNet)을 백본으로 사용하여 깊이에서 오는 표현력을 극대화한다.
3. **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: 최신 논문에 나온 가장 깊은 모델만 무조건 고집하는 것. 실제 비즈니스 환경에서는 밀리초(ms) 단위의 추론 [[015_지연_데이터_관점|지연]]시간([[141_latency|Latency]])과 [[418_gpu|GPU]] 메모리 한계가 더 중요할 때가 많다.

- **📢 섹션 요약 비유**: 레이싱카(최신 초거대 모델)가 아무리 빨라도 동네 마트(단순 [[104_classification_analysis|분류]] 앱)에 갈 때는 기름만 많이 먹고 주차도 어렵습니다. 용도에 맞는 적절한 연비의 자동차(최적화된 백본)를 고르는 것이 실력입니다.

---

## Ⅴ. 기대효과 및 결론

AlexNet부터 ResNet에 이르는 [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 아키텍처의 혁신은 컴퓨터 비전이 인간의 눈을 뛰어넘는 정확도를 달성하게 만들었다. 깊이를 더하면서도 연산 효율과 최적화의 난제를 해결한 이 아이디어들은 이후 자연어 처리([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 등 다른 딥러닝 분야의 발전에도 결정적인 영감을 주었다.

앞으로는 단순히 인간이 설계한 구조를 넘어, [[231_ai_turing_test|인공지능]]이 스스로 최적의 아키텍처를 찾아내는 [[492_nas_network_attached_storage|NAS]](Neural [[319_architecture|Architecture]] Search) 모델이나, ViT(Vision [[246_transformer_self_attention_parallel_positional_encoding|Transformer]])처럼 [[228_cnn_1d_2d_3d_video_medical|합성곱]] 자체를 대체하려는 흐름으로 진화하고 있다. 따라서 각 아키텍처가 "어떤 문제를 해결하기 위해 등장했는지" 그 본질적 아이디어를 이해하는 것이 가장 중요하다.

- **📢 섹션 요약 비유**: 바퀴의 발명부터 제트 엔진까지 발전 과정을 알면, 앞으로 나올 우주선이 왜 그런 모양을 하고 있는지 단번에 이해할 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[088_vanishing_gradient_relu_skip_connection|기울기 소실]] ([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]])** | 층이 깊어질수록 학습 [[130_signal|신호]]가 약해지는 고질적 문제 |
| **[[132_transfer_learning|전이 학습]] ([[132_transfer_learning|Transfer Learning]])** | ImageNet으로 미리 학습된 VGG, ResNet의 [[267_weight_bias_activation|가중치]]를 가져다 쓰는 기법 |
| **[[105_one_by_one_convolution_bottleneck_dimension_reduction|1x1 합성곱]] ([[284_convolution_stride_padding|Convolution]])** | 공간 정보는 유지하면서 채널 수(두께)만 줄이는 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 마법 |
| **DenseNet** | ResNet을 확장하여 모든 층의 출력을 다음 모든 층에 연결하는 아키텍처 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통적 머신러닝 (수동 특징 추출)
    │
    ▼
LeNet-5 (CNN 뼈대 확립, CPU 한계)
    │
    ▼
AlexNet (ReLU 활성화 함수, GPU 연산 도입)
    │
    ├───────────┐
    ▼           ▼
VGGNet          GoogLeNet 
(3x3 필터)      (Inception 모듈, 경량화)
    │           │
    └─────┬─────┘
          ▼
ResNet (잔차 연결, 기울기 소실 극복, 초심층화)
          │
          ▼
ViT (Vision Transformer) 및 NAS (자동 탐색)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 똑똑한 [[231_ai_turing_test|인공지능]]을 만들려면 뇌세포 층을 아파트처럼 높게 쌓아야 해요.
2. 하지만 너무 높게 쌓으면 맨 꼭대기 층까지 정보가 전달되지 않아서 똑똑해지지 않았어요.
3. 과학자들이 중간에 막히지 않는 '고속 엘리베이터(잔차 연결)'를 발명해서 100층 넘게 지을 수 있게 된 거랍니다!
