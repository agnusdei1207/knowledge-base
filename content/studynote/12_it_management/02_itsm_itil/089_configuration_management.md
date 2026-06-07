---
title: "089. Cnn Convolutional"
date: "2026-04-05"
description: "CNN의 구조, 합성곱 연산, 필터, 풀링, 이미지 인식에서의 역할과 한계점"
tags:
  - "it_management"
---

# 89. [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 신경망 (Convolutional Neural Network) - 공간 패턴 인식자

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 신경망 (Convolutional Neural Network, [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))은 이미지나 영상 같은 다차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 '공간적 구조'와 '인접성'을 유지한 채 특징을 추출하도록 고안된 [심층 신경망](/studynote/10_ai/01_ai_basics/065_dnn_deep_neural_network/) 아키텍처다.
> 2. **가치**: 기존 완전연결 (Fully Connected) 신경망이 픽셀의 위치 정보를 잃어버리고 파라미터가 폭발하던 문제를 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유 ([Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Sharing)와 국소 연결 (Local Connectivity)을 통해 해결하여, 적은 연산량으로 시각적 패턴을 압도적으로 잘 잡아낸다.
> 3. **판단 포인트**: 이미지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), [객체 탐지](/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/) 등 시각 비전 영역에서는 무조건적인 표준이지만, 이미지의 전체적 문맥(글로벌 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/))을 파악하는 데는 제한이 있어 최근에는 Vision [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) (ViT) 등과 융합하거나 대체되는 추세도 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

과거의 인공신경망인 [다층 퍼셉트론](/studynote/10_ai/03_llm_nlp/266_mlp_hidden_layers/)(MLP)에 이미지를 입력하려면, 가로세로의 픽셀 구조를 1차원 선으로 길게 펼쳐야만(Flatten) 했다. 이 과정에서 '코 바로 아래에 입이 있다'는 중요한 2차원 공간 정보와 위상 배열이 완전히 파괴되었다. 또한, 이미지 픽셀 수만큼 수십만 개의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 층마다 필요해져 메모리가 폭발하고 과적합이 발생했다.

이러한 한계를 극복하기 위해 등장한 것이 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) (Convolutional Neural Network)이다. CNN은 이미지를 펼치지 않고 2차원 구조 그대로 유지하며, 조그만 돋보기(필터)를 이미지 전체에 슬라이딩(Sliding)시키면서 특징을 뽑아낸다. 이 돋보기는 동일한 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 공유하므로 연산 파라미터 수가 극적으로 줄어들며, 고양이의 귀가 사진 왼쪽 끝에 있든 오른쪽 끝에 있든 동일하게 인식할 수 있는 위치 이동 불변성(Translation Invariance)을 획득하게 되었다.

- **📢 섹션 요약 비유**: 옛날 신경망은 모나리자 그림을 잘게 잘라 한 줄로 이어 붙인 뒤 "누구게?" 하고 맞히는 방식이었다면, CNN은 돋보기를 들고 그림의 눈, 코, 입을 요리조리 훑어보며 원래 형태 그대로 패턴을 찾아내는 똑똑한 감식반이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CNN은 특징을 추출하는 '[합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 계층' 및 '[풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) 계층'과, 마지막에 결과를 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 '완전연결 계층'으로 나뉜다.

핵심 원리인 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 연산은, 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위를 필터(Filter, 또는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 지정된 간격([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/))만큼 이동하며 겹치는 부분의 요소끼리 곱하고 더하는 연산이다. 이렇게 만들어진 결과물을 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)([Feature Map](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))이라고 한다.

| 핵심 구성 요소 | 동작 원리 및 역할 |
| :--- | :--- |
| <strong><a href="/studynote/10_ai/01_ai_basics/096_convolution_layer_filter_stride_padding/">합성곱 층</a> (Conv Layer)</strong> | 여러 개의 필터가 이미지를 훑으며 모서리, 질감 등의 특징 패턴을 추출한다. [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유를 통해 연산량을 극적으로 줄인다. |
| <strong><a href="/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/">활성화 함수</a> (<a href="/studynote/10_ai/03_llm_nlp/269_relu_activation/">ReLU</a>)</strong> | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 결과에 비선형성을 부여한다. 음수 값을 0으로 차단하여 네트워크가 깊어져도 수렴할 수 있게 한다. |
| <strong><a href="/studynote/10_ai/01_ai_basics/100_pooling_layer_max_pooling_downsampling_cnn/">풀링 층</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">Pooling Layer</a>)</strong> | [최대 풀링](/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/) ([Max Pooling](/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) 등을 통해 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 크기(해상도)를 반으로 줄여, 계산량을 압축하고 미세한 위치 변화에 강건해지도록 만든다. |

```text
+--------------------------------------------------------------+
|                  합성곱 (Convolution) 연산의 과정             |
+--------------------------------------------------------------+
|  [입력 이미지 (5x5)]         [필터 (3x3)]       [특성 맵 (3x3)] |
|  +-+-+-+-+-+                                                   |
|  |1|1|1|0|0|          +-+-+-+               +-+-+-+          |
|  +-+-+-+-+-+          |1|0|1|               |4|3|4|          |
|  |0|1|1|1|0|   (X)    +-+-+-+     ---->      +-+-+-+          |
|  +-+-+-+-+-+          |0|1|0|               |2|4|3|          |
|  |0|0|1|1|1|          +-+-+-+               +-+-+-+          |
|  +-+-+-+-+-+          |1|0|1|               |2|3|4|          |
|  |0|0|1|1|0|          +-+-+-+               +-+-+-+          |
|  +-+-+-+-+-+                                                   |
|  * 겹치는 부분의 숫자를 곱하고 모두 더해 한 칸을 채움           |
+--------------------------------------------------------------+
```

얕은 층에서는 선, 윤곽 등 단순한 특징을 잡고, 층이 깊어질수록 눈, 코, 귀처럼 복잡한 추상적 패턴을 조합해 나가는 계층적 학습 구조를 가진다.

- **📢 섹션 요약 비유**: 작업 반장들이 공장에 서 있습니다. 첫 번째 반장(얕은 층 필터)은 불량품의 '긁힌 자국'만 찾고, 두 번째 반장([풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/))은 그 결과를 요약해 넘깁니다. 세 번째 반장(깊은 층 필터)은 자국들이 모여 만든 '파손 부위'를 판별합니다. 각자 자기 모양만 찾는 도장([가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유)을 쓰는 철저한 분업 시스템입니다.

---

## Ⅲ. 비교 및 연결

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 형태에 따라 유리한 신경망 구조가 명확하게 갈린다. CNN과 다른 아키텍처의 경계를 비교해 보면 CNN의 입지가 명확해진다.

| 특성 | [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) ([합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 신경망) | [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) ([순환 신경망](/studynote/10_ai/02_dl_architecture_new/111_rnn_recurrent_neural_network_sequential_data/)) | ViT (비전 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) |
| :--- | :--- | :--- | :--- |
| <strong>타겟 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 2D 이미지, 공간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 텍스트 | 대규모 이미지 패치 |
| **핵심 기법** | 공간적 국소 연결, [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유 | 이전 상태의 순환 메모리 | 어텐션 ([Self-Attention](/studynote/10_ai/02_dl_architecture_new/124_self_attention/)) 메커니즘 |
| **문맥 파악 범위** | 지역적 특징 중심 (Local) | 순차적 흐름 파악 | 전체적 특징 동시 파악 (Global) |
| **연산 복잡도** | 상대적으로 낮음 | 순차 연산으로 병렬화 어려움 | 파라미터가 매우 방대함 |

초기에는 이미지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서만 쓰이던 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 아키텍처는 점차 진화하여 [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) (잔차 연결을 통한 층수 극대화), YOLO (객체의 바운딩 박스를 실시간으로 회귀 예측) 등으로 발전하며 컴퓨터 비전 생태계의 절대 권력자가 되었다. 최근에는 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 기술이 비전 분야로 넘어오며 ViT와 상호 보완적으로 융합되고 있다.

- **📢 섹션 요약 비유**: CNN이 현미경으로 세포 하나하나의 모양(지역 특징)을 찾아가는 방식이라면, 비전 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)(ViT)는 열기구를 타고 숲 전체의 모양(글로벌 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/))을 한눈에 내려다보는 방식입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 이미지 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리를 기획할 때 CNN은 무조건적인 1순위 후보다. 하지만 만능은 아니며 하드웨어와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제약에 따라 아키텍처를 영리하게 채택해야 한다.

### 실무 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **실시간성이 중요한가?**: 자율주행이나 [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 등 실시간 탐지가 생명이라면 정확도 최상단 모델보다는 연산량이 압축된 MobileNet, YOLO 등 경량화 1-Stage 구조를 도입해야 한다.
2. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 볼륨 한계 극복</strong>: 의료 이미지처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1,000장 구하기가 하늘의 별 따기라면, 모델을 바닥부터 학습시키지 말고 이미 ImageNet으로 학습된 거대 모델을 가져와 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) ([Transfer Learning](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))하는 전략이 필수다.
3. <strong>글로벌 <a href="/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a>의 필요성</strong>: 이미지 안의 물체들이 서로 너무 멀리 떨어져 있어서 전체 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 파악이 중요하다면, 순수 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 대신 어텐션(Attention)이 가미된 모델을 혼합해야 한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 무작정 가장 깊고 무거운 최신 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)(예: 거대 [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/))을 가져다 쓰느라 모바일 디바이스에서 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 심각하게 터지는 설계
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증강 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Augmentation, 회전/반전 등) 없이 적은 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만으로 CNN을 학습시켜 극심한 과적합에 빠지는 행위

- **📢 섹션 요약 비유**: 포크레인(무거운 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))이 흙을 잘 파긴 하지만, 화분 분갈이(모바일 환경)를 할 때 포크레인을 부를 필요는 없습니다. 환경과 제약에 맞는 삽(경량화 [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/))을 골라 쓰는 것이 엔지니어의 핵심 판단입니다.

---

## Ⅴ. 기대효과 및 결론

CNN은 이미지 처리 기술의 패러다임을 사람이 일일이 특징 수식을 짜던 방식에서, 기계가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보고 스스로 필터를 학습하는 방식으로 완벽하게 전환시켰다. 이를 통해 안면 인식, 자율 주행, 암 진단 등 시각을 다루는 모든 인류 기술의 비약적 진보를 이뤄냈다.

결론적으로 CNN은 공간 구조 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Spatial [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))의 규칙을 파악하는 가장 우아한 수학적 메커니즘이다. 비록 글로벌 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)를 파악하는 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 등 새로운 아키텍처의 도전을 받고 있지만, 강력한 특징 추출 능력과 연산 효율성 덕분에 앞으로도 시각 지능 시스템의 가장 튼튼한 척추 역할을 수행할 것이다.

- **📢 섹션 요약 비유**: CNN은 스스로 세상을 보는 법을 터득한 인공 눈동자입니다. 이 눈동자 덕분에 컴퓨터는 단순히 픽셀의 색깔만 외우는 기계에서 벗어나 세상의 형태와 패턴을 인식하는 진정한 관찰자가 되었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/">특성 맵</a> (<a href="/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/">Feature Map</a>)</strong> | 입력에 필터를 통과시켜 얻어낸 결과물, 이미지의 특징을 압축한 장 |
| <strong><a href="/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">스트라이드</a> (<a href="/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">Stride</a>)와 <a href="/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">패딩</a> (<a href="/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">Padding</a>)</strong> | 필터의 이동 보폭([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/))과 입력 가장자리의 정보 손실을 막는 여백([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">ResNet</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">Residual Network</a>)</strong> | 깊은 CNN에서 발생하는 기울기 소실을 잔차 연결(Skip Connection)로 해결한 혁신적 구조 |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/">전이 학습</a> (<a href="/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/">Transfer Learning</a>)</strong> | 거대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 미리 학습된 CNN의 앞쪽 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 내 프로젝트에 재활용하는 실무 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
이미지 플래트닝 (Flattening) 문제점 대두
    |
    v
CNN (합성곱, 풀링) · 가중치 공유 (Weight Sharing)
    |
    v
LeNet (초기 구조) · AlexNet (GPU 도입 딥러닝 부흥)
    |
    v
VGG (깊이 심화) · ResNet (잔차 연결로 초심층 학습)
    |
    v
YOLO (실시간 객체 탐지) · ViT (비전 트랜스포머 융합)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 큰 코끼리 사진을 한 번에 눈에 담으려면 너무 복잡해서 어지러워요.
2. CNN은 작은 돋보기를 들고 코끼리 사진의 귀 부분, 코 부분, 꼬리 부분을 조금씩 조금씩 이동하면서 살펴보는 방법이에요.
3. 그렇게 작은 특징들을 하나씩 찾아서 합치다 보면 "아하, 코끼리구나!" 하고 똑똑하게 알아맞히게 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 587

<- **이전**: [88. 서비스 카탈로그 (Service Catalog)](/studynote/12_it_management/02_itsm_itil/872_service_catalog/)
**다음**: [89. 구성 관리 (Configuration Management)](/studynote/12_it_management/02_itsm_itil/873_configuration_management/) ->

---
