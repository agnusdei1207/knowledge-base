---
title: "283. CNN (Convolutional Neural Network)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)([Convolutional Neural Network](/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/), [합성곱 신경망](/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/))은 [합성곱 연산](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))으로 이미지의 <strong>지역적 공간 패턴</strong>을 추출하고, <strong><a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 공유(<a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">Weight</a> Sharing)</strong>와 <strong>이동 불변성(Translation Invariance)</strong>으로 파라미터를 대폭 줄이면서 이미지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·탐지·분할에 탁월한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 발휘한다.
> 2. **가치**: [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)(Fully Connected Layer) 대비 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 수를 수천 배 이상 줄이고, 이미지 내 위치가 달라도 동일한 특성(엣지, 텍스처, 객체 부분)을 인식하는 이동 불변성으로 이미지 인식의 혁명을 이끌었다.
> 3. **판단 포인트**: 기술사 시험에서 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 출력 크기 계산 공식, [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)의 역할, [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)([Feature Map](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))의 의미, 그리고 LeNet->AlexNet->VGG->ResNet의 발전 계보를 묻는 문제가 출제된다.

---

## Ⅰ. 개요 및 필요성

### [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 레이어의 한계

전통적인 완전 연결층([FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/), Fully Connected Layer)은 이미지를 1차원 벡터로 펼쳐 처리한다. 224×224×3 이미지라면 <strong>150,528개의 입력 노드</strong>가 필요하고, 첫 은닉층에 1,000개 뉴런만 있어도 <strong>1억 5천만 개의 <a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a></strong>가 필요해 학습 불가능에 가깝다.

또한 FC는 <strong>공간 구조(Spatial Structure)를 무시</strong>한다. 이미지에서 근접한 픽셀들은 높은 상관관계를 가지는데, FC는 이를 전혀 활용하지 못한다.

CNN은 다음 핵심 아이디어로 이를 해결한다:
1. **지역 수용 영역(Local Receptive Field)**: 한 번에 작은 영역(예: 3×3)만 처리
2. <strong><a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 공유(<a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">Weight</a> Sharing)</strong>: 동일한 필터를 이미지 전체에 반복 적용
3. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">풀링</a>(<a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">Pooling</a>)</strong>: 공간 해상도 축소로 이동 불변성 확보

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: CNN은 이미지를 한꺼번에 전체를 보는 것이 아니라, 돋보기로 작은 부분씩 훑으며([합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)) 패턴을 찾고, 같은 돋보기([가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유)를 이미지 전체에 재사용하는 효율적인 탐정 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 전체 아키텍처

```
입력 이미지 (H × W × C)
    |
    v
+--------------------------------------------------------------+
|  합성곱 블록 (Conv Block)                                    |
|  +--------------------------------------------------------+  |
|  | Conv(3×3, F filters) -> BN -> ReLU                      |  |
|  | 출력: H' × W' × F  (특성 맵, Feature Map)             |  |
|  +--------------------------------------------------------+  |
|                  × 여러 회 반복                              |
+--------------------------------------------------------------+
|  풀링 레이어 (Pooling Layer)                                 |
|  MaxPooling(2×2, stride=2) -> H/2 × W/2 × F (공간 축소)     |
+--------------------------------------------------------------+
|  깊어질수록: 공간 크기(H,W)v, 채널 수(F)^                 |
|  저수준 특성(엣지) -> 중수준(텍스처) -> 고수준(객체 부분)   |
+--------------------------------------------------------------+
    |
    v
Flatten -> FC Layer -> Softmax -> 분류 결과
```

### [합성곱 연산](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))

```
입력 (5×5)         필터 (3×3)         출력 특성 맵 (3×3)
+-------------+   +---------+        +---------+
| 1  2  3  0  1|  | 1  0 -1 |        |  ●  ●  ● |
| 4  5  6  1  2|× | 1  0 -1 |   ->    |  ●  ●  ● |
| 7  8  9  2  1|  | 1  0 -1 |        |  ●  ●  ● |
| 0  1  2  3  0|  +---------+        +---------+
| 1  0  1  2  3|
+-------------+
출력 크기 = (N - F + 2P) / S + 1
  N: 입력 크기, F: 필터 크기, P: 패딩, S: 스트라이드
예) (5 - 3 + 0) / 1 + 1 = 3
```

### 출력 크기 계산 공식

| 파라미터 | 의미 | 예시 |
|:---|:---|:---:|
| N (Input Size) | 입력 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 크기 | 32 |
| F (Filter Size) | 필터([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))의 크기 | 3 |
| P ([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) | 입력 주변 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 크기 | 1 |
| S ([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)) | 필터 이동 간격 | 1 |
| **출력 크기** | **(N - F + 2P) / S + 1** | **(32-3+2)/1+1=32** |

[패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) P=1로 Same Padding을 적용하면 입력과 출력 크기가 같다 (32->32).

### [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)([Pooling](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) 레이어

```
Max Pooling (2×2, stride=2):
+-----------------------------------+
|  입력 4×4  ->  출력 2×2           |
|  +---+---+                        |
|  | 1  3  |  max-> 9               |
|  | 2  9  |                        |
|  +---+---+                        |
|  | 5  2  |  max-> 7               |
|  | 7  1  |                        |
|  +---+---+                        |
|  이동 불변성: 패턴이 조금 이동해도 |
|  동일한 최대값이 출력됨            |
+-----------------------------------+
```

### 대표 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 아키텍처 계보

| 아키텍처 | 연도 | 핵심 기여 | 파라미터 수 |
|:---|:---:|:---|:---:|
| LeNet-5 | 1998 | CNN의 시작, 필기체 인식 | ~60K |
| AlexNet | 2012 | [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/), [Dropout](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/), [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 학습 | ~62M |
| VGGNet | 2014 | 3×3 필터 깊은 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | ~138M |
| GoogLeNet | 2014 | Inception [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 1×1 Conv | ~6.8M |
| [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) | 2015 | 잔차 연결(Skip Connection) | ~25M(50층) |
| EfficientNet | 2019 | 복합 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)(Width/Depth/Resolution) | ~5.3M(B0) |

- **📢 섹션 요약 비유**: CNN의 발전은 도시가 성장하는 것과 같다. LeNet이 작은 마을이라면, AlexNet은 고속도로([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)), ResNet은 다리(Skip Connection)로 교통 체증(그래디언트 소실)을 해결한 현대 도시다.

---

## Ⅲ. 비교 및 연결

### [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유([Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Sharing)의 의미

[FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 레이어: 각 연결마다 별도의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) -> 파라미터 수 = 입력 × 출력
[CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/): 동일한 필터가 전체 이미지를 슬라이딩 -> 파라미터 수 = F × F × C_in × C_out

예) 224×224×3 입력, 첫 레이어:
- [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/): 150,528 × 1,000 = **1억 5천만 개**
- [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) (3×3×3 필터, 64개): 3×3×3×64 = **1,728개** (87,000배 절감)

### 이동 불변성(Translation Invariance) vs 이동 등변성(Translation Equivariance)

- <strong><a href="/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a> 레이어</strong>: **이동 등변성(Equivariance)** - 입력이 이동하면 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)도 같이 이동
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">풀링</a> 레이어</strong>: **이동 불변성(Invariance)** - 입력이 조금 이동해도 출력이 동일

두 개념의 결합으로 "고양이가 이미지의 어느 위치에 있든 고양이로 인식"이 가능하다.

### [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) vs [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)

| 항목 | [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) | [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) (ViT) |
|:---|:---|:---|
| 귀납적 편향 | 지역성, 이동 불변성 (강함) | 없음 ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 학습) |
| 장거리 의존성 | 깊은 레이어 필요 | Self-Attention으로 직접 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 효율성 | 적은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 우수 | 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 |
| 현재 트렌드 | 하이브리드 (ConvNeXt) | ViT, Swin [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |

- **📢 섹션 요약 비유**: CNN은 오랜 경험(귀납적 편향)이 쌓인 전문 화가가 그림의 부분부분을 보며 그리는 방식이다. Transformer는 그림 전체를 한눈에 보는 능력이 있지만 처음엔 경험이 없어 많은 그림을 봐야 한다. 최신 아키텍처는 두 방법을 결합한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 판단 포인트

1. **출력 크기 계산**: (N - F + 2P) / S + 1 공식 암기
2. <strong><a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 공유 효과</strong>: 파라미터 수 대폭 절감 이유
3. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">풀링</a>의 역할</strong>: 공간 크기 축소 + 이동 불변성 + 과적합 방지
4. **ResNet의 잔차 연결**: 그래디언트 소실 방지, H(x) = F(x) + x

### 잔차 연결(Residual Connection, Skip Connection)

```
입력 x
  |   +--------------------------+
  v                              | (지름길)
Conv -> BN -> ReLU -> Conv -> BN    |
  v                              |
  (+)◄--------------------------+
  v
ReLU -> 출력 H(x) = F(x) + x
```

잔차 연결로 그래디언트가 곱셈 없이 덧셈으로 직접 전달 -> 100층 이상의 네트워크 학습 가능.

### 주요 응용 분야

- <strong>이미지 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>(Image <a href="/studynote/12_it_management/03_ea_isp/107_classification/">Classification</a>)</strong>: [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/), EfficientNet
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/">객체 탐지</a>(<a href="/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/">Object Detection</a>)</strong>: YOLO, Faster R-[CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) ([CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 백본 사용)
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/289_image_segmentation/">이미지 분할</a>(<a href="/studynote/10_ai/04_ai_ops_ethics/289_image_segmentation/">Image Segmentation</a>)</strong>: U-Net ([인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/), Skip Connection)
- **의료 영상**: X-ray 진단, MRI 분석 (소량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))

- **📢 섹션 요약 비유**: ResNet의 잔차 연결은 100층짜리 건물에 엘리베이터를 설치하는 것과 같다. 계단(순방향 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/))으로만 올라가면 너무 힘들어 그래디언트가 사라지지만(그래디언트 소실), 엘리베이터(잔차 경로)로 정보가 직접 전달된다.

---

## Ⅴ. 기대효과 및 결론

CNN이 이미지 인식 혁명을 이끈 이유:

1. **파라미터 효율성**: [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유로 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 대비 수만 배 파라미터 절감
2. **이동 불변성**: 객체 위치에 무관한 강건한 인식
3. **계층적 특성 추출**: 엣지 -> 텍스처 -> 부분 -> 객체의 계층적 표현 학습
4. <strong><a href="/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/">전이 학습</a>(<a href="/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/">Transfer Learning</a>)</strong>: ImageNet 사전 학습 모델을 다양한 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 적용

AlexNet이 2012년 ImageNet에서 압도적 1위를 기록한 이후, CNN은 컴퓨터 비전(Computer Vision)의 표준이 되었다. 현재는 Vision [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)(ViT)와의 하이브리드 형태(ConvNeXt, Swin [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 등)로 발전하고 있다.

- **📢 섹션 요약 비유**: CNN은 동물의 시각 피질처럼, 간단한 엣지(V1)에서 복잡한 형태(상위 피질)까지 계층적으로 처리하는 생물학적 영감을 받은 구조다. 자연의 설계를 모방했기 때문에 이미지 인식에서 이렇게 강력한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보이는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) (Conv Net) | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/), [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/) / 이미지 처리 특화 신경망 |
| [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) ([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)) | 필터, [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) / 지역 패턴 추출 연산 |
| [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유 ([Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Sharing) | 파라미터 절감, 필터 재사용 / CNN의 핵심 효율화 기법 |
| [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/) ([Feature Map](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)) | 채널, 활성화, 응답 / [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 출력 표현 |
| [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Pooling](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) | MaxPool, 이동 불변성 / 공간 축소 + 이동 불변성 |
| 이동 불변성 (Translation Invariance) | [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/), 위치 무관 인식 / CNN의 핵심 특성 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [CNN (Convolutional Neural Network)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. CNN은 그림의 작은 부분씩 같은 돋보기로 훑어보며 패턴을 찾는 방법이에요. 같은 돋보기를 모든 곳에 쓰니까 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 아주 적게 쓸 수 있어요.
2. [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)은 "어디쯤에 고양이가 있네"를 알면 정확히 어느 픽셀인지 몰라도 되는 것처럼, 위치가 조금 달라도 같은 패턴으로 인식하게 해줘요.
3. ResNet은 100층짜리 건물에 엘리베이터를 설치한 것처럼, 정보가 직접 뛰어넘어 전달되어 아무리 깊어도 잘 학습할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 283 / 420

<- **이전**: [282. 배치 정규화 (Batch Normalization)](/studynote/10_ai/03_llm_nlp/282_batch_normalization/)
**다음**: [284. 합성곱 연산 (Convolution)](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) ->

---
