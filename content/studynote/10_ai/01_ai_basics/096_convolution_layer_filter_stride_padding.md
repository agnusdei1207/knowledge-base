---
title: "096. Convolution Layer Filter Stride Padding"
date: "2026-04-10"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층 ([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) Layer)은 2차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 공간적 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)을 유지한 채, 작은 필터(Filter)를 이동시키며 지역적 특징을 추출하는 연산 계층이다.
> 2. **가치**: 파라미터 공유 (Parameter Sharing)와 지역적 연결 (Local Connectivity)을 통해, 위치가 변해도 동일한 패턴을 찾아내며(이동 불변성) 학습 파라미터 수를 획기적으로 줄인다.
> 3. **판단 포인트**: 모델을 설계할 때 [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) ([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/))와 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) ([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))의 크기를 조절하여, 연산량과 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/) ([Feature Map](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))의 해상도를 목적에 맞게 균형 맞춰야 한다.

---

## Ⅰ. 개요 및 필요성

이미지나 시계열 같은 다차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 인접한 픽셀 혹은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 공간적, 시간적 연관성이 매우 중요하다. 과거의 MLP (Multi-Layer [Perceptron](/studynote/14_data_engineering/05_exam_keywords/239_perceptron_mlp_hidden_layer_weight_activation_sigmoid/)) 모델은 이러한 2차원 이미지를 1차원 벡터로 길게 펼쳐서 처리했기 때문에, 원래 픽셀 간의 위치 정보(예: 눈 옆에 코가 있다)가 완전히 파괴되는 문제가 있었다.

[합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층은 이 공간적 맥락을 보존하기 위해 등장했다. 인간의 시각 세포가 시야의 좁은 영역(Local Receptive Field)에만 반응하는 원리에서 착안하여, 픽셀의 상하좌우 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 그대로 유지하며 이미지를 분석한다. 이것이 없으면 수천만 개의 픽셀을 처리하기 위해 기하급수적으로 많은 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 필요해져 메모리가 폭발하고 학습이 불가능해진다.

- **📢 섹션 요약 비유**: 큰 그림을 볼 때 종이를 길게 찢어서 한 줄로 늘어놓고(MLP) 보는 대신, 원래 그림의 형태를 유지한 채 작은 돋보기(필터)를 대고 상하좌우로 훑어보는(Conv Layer) 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[합성곱 연산](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)은 <strong>필터(Filter 또는 <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a>)</strong>, <strong><a href="/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">스트라이드</a>(<a href="/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">Stride</a>)</strong>, <strong><a href="/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">패딩</a>(<a href="/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">Padding</a>)</strong>이라는 세 가지 핵심 요소로 작동한다. 필터가 입력 이미지 위를 슬라이딩하며 원소 간 곱(Element-wise Multiplication)의 합(내적)을 구하여 하나의 스칼라 값을 도출하고, 이 결과들을 모아 새로운 2차원 행렬인 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)을 만든다.

```text
+------------------------------------------------------------------------+
|                   합성곱 연산과 파라미터의 역할                        |
+------------------------------------------------------------------------+
|  [입력 이미지 (Input)]        [필터 (Filter)]        [특성 맵 (Map)]   |
|  +-+-+-+-+ (Padding=0)        +-+-+               +-+-+-+              |
|  |1|0|1|0|                    |1|0|               |2|1|3|              |
|  +-+-+-+-+ (Stride=1)  (내적) +-+-+     ====>     +-+-+-+              |
|  |0|1|1|1| *--------* -------> |0|1|               |1|2|2|              |
|  +-+-+-+-+                    +-+-+               +-+-+-+              |
|  |1|0|1|0|                                        |1|1|1|              |
|  +-+-+-+-+                                        +-+-+-+              |
+------------------------------------------------------------------------+
```

이 그림은 [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)가 어떻게 돋보기의 보폭을 결정하고, 필터가 어떻게 이미지를 스캔하는지 보여준다. [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)를 키우면 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 크기가 작아지며 공간 정보가 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)된다. 반대로 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)은 원본 이미지 주변에 0([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-[padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))을 덧대어, 테두리 부분의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실을 막고 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 크기를 입력과 동일하게 유지하는 역할을 한다.

- **📢 섹션 요약 비유**: 도장(필터)을 찍을 때 한 칸씩 꼼꼼히 찍을지([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)=1), 두 칸씩 성큼 뛸지([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)=2) 결정하며, 종이 밖으로 도장이 벗어나 무늬가 짤리는 것을 막기 위해 밑에 이면지를 덧대는 것([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))이다.

---

## Ⅲ. 비교 및 연결

[합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층을 깊이 이해하려면, 모든 뉴런이 촘촘하게 연결된 [완전 연결 층](/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/) (Fully Connected Layer, Dense Layer)과 비교해야 한다.

| 비교 항목 | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층 ([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) Layer) | [완전 연결 층](/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/) (Fully Connected Layer) |
| :--- | :--- | :--- |
| **연결 방식** | 지역적 연결 (Local Connectivity) | 전역적 연결 (Global Connectivity) |
| **파라미터 수** | 매우 적음 (필터 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유) | 매우 많음 (입력 차원 × 출력 차원) |
| **공간 정보** | 2차원/3차원 공간 구조 보존 | 1차원으로 펴지며 공간 정보 소실 |
| **장점** | 이미지 등 공간적 패턴 인지에 탁월 | 최종 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 결정에 유리 |

[합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층은 선행하는 [풀링 층](/studynote/10_ai/01_ai_basics/100_pooling_layer_max_pooling_downsampling_cnn/) ([Pooling Layer](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/))과 결합하여 이미지의 크기를 점진적으로 줄이고 특징을 응축하며, 최종적으로 [완전 연결 층](/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/)과 연결되어 물체를 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) ([Convolutional Neural Network](/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/)) 아키텍처로 확장된다.

- **📢 섹션 요약 비유**: [완전 연결 층](/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/)은 경찰관 100명이 사진의 픽셀 100개를 각자 1명씩 전담 마크하는 비효율적 방식이라면, [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층은 순찰차 1대(필터)가 동네 전체를 돌아다니며 단속을 수행하는 고효율 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 모델을 설계할 때 가장 빈번한 판단은 <strong>필터의 크기와 개수 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>이다. 과거에는 $7 \times 7$이나 $5 \times 5$의 큰 필터를 단일 층으로 사용했으나, 현대에는 작은 $3 \times 3$ 필터를 여러 층으로 깊게 쌓는 방식을 표준으로 채택한다.

### 기술사 판단: 설계 시 고려사항
1. **필터 분해 (Filter Factorization)**: $5 \times 5$ 필터 1개를 쓰는 것보다 $3 \times 3$ 필터 2개를 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)로 쓰는 것이 수용 영역(Receptive Field)은 같으면서 연산량 파라미터가 적고, 비선형 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)([ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/))를 더 많이 거쳐 모델의 표현력이 증가한다.
2. **다운샘플링 시점**: [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) 2를 줄 것인가, 아니면 [최대 풀링](/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)([Max Pooling](/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/))을 쓸 것인가를 결정해야 한다. 최근 추세는 [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) 없이 [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)만으로 특징 맵 크기를 줄이는 방식이 자주 쓰인다.
3. **가장자리 중요성**: [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)(Same [Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) 없이 층을 통과시키면 외곽 픽셀 정보가 급격히 사라지므로, 깊은 망을 설계할 때는 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 필수적으로 적용해야 한다.

- **📢 섹션 요약 비유**: 큰 망원경 하나(큰 필터)로 한 번에 보는 것보다, 작은 돋보기(작은 필터)를 여러 장 겹쳐서 보는 것이 렌즈 비용(연산량)도 싸고 왜곡(특징 추출)도 더 잘 교정할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층을 통해 딥러닝은 단순한 숫자 예측을 넘어 인간 이상의 이미지 인식 능력을 갖추게 되었다. 이동 불변성을 확보하여 객체의 위치가 달라져도 정확히 인식할 수 있고, [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유 덕분에 모바일 기기에서도 동작 가능한 수준으로 모델이 경량화되었다.

하지만 [합성곱 연산](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)은 결국 지정된 필터 크기 안의 지역적 정보만 본다는 한계가 있어, 멀리 떨어진 픽셀 간의 전역적(Global) 연관성을 잡기 어렵다. 이러한 한계를 보완하기 위해 최근에는 전체 문맥을 보는 비전 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) (Vision [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 계열이 등장했다. 따라서 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층은 "지역적 패턴 추출의 가장 효율적인 기초 공사"로 기억해야 한다.

- **📢 섹션 요약 비유**: 돋보기는 주변의 디테일을 기가 막히게 잘 보여주지만 숲 전체의 풍경을 보지는 못한다. 그래서 완벽한 시야를 위해 돋보기와 드론 카메라를 함께 사용해야 하는 시대가 오고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/">CNN</a> (<a href="/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/">Convolutional Neural Network</a>)</strong> | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층을 수십~수백 층 쌓아 올린 딥러닝 아키텍처 |
| <strong><a href="/studynote/10_ai/01_ai_basics/100_pooling_layer_max_pooling_downsampling_cnn/">풀링 층</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">Pooling Layer</a>)</strong> | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층 뒤에 붙어 특징 맵을 요약하고 크기를 줄이는 계층 |
| **수용 영역 (Receptive Field)** | 최종 출력 뉴런 하나가 보고 있는 원본 이미지의 영역 크기 |
| **이동 불변성 (Translation Invariance)** | 피사체가 왼쪽이나 오른쪽으로 이동해도 동일하게 인식하는 특성 |

### 📈 관련 키워드 및 발전 흐름도

```text
MLP (다층 퍼셉트론) · 공간 정보 손실
    |
    v
LeNet-5 (초기 CNN) · 합성곱 층(Conv) 개념 정립
    |
    v
VGGNet · 작은 3x3 필터(Filter)의 깊은 누적
    |
    v
ResNet · 잔차 연결과 패딩(Padding)을 통한 초심층망
    |
    v
Vision Transformer (ViT) · 합성곱 한계 극복을 위한 어텐션 도입
```

### 👶 어린이를 위한 3줄 비유 설명

1. [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 층은 커다란 그림책을 읽을 때 사용하는 마법의 돋보기예요.
2. 돋보기를 책 위로 슥슥 밀면서(슬라이딩) "어! 여기 강아지 코가 있네!" 하고 중요한 부분만 찾아내요.
3. 돋보기를 한 번에 얼마나 멀리 뛸지([스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)), 책 바깥으로 안 나가게 방석을 깔지([패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) 정할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 96 / 420

<- **이전**: [95. 합성곱 신경망 (CNN) - 공간 정보 보존 이미지 인식 아키텍처](/studynote/10_ai/01_ai_basics/095_cnn_convolutional_neural_network_image_recognition/)
**다음**: [97. 스트라이드 (Stride) - CNN 필터 이동 보폭과 특징 맵 축소](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) ->

---
