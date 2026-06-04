+++
title = "285. 풀링 (Pooling)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 풀링(Pooling)은 특징 맵([Feature Map](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))의 공간 해상도를 줄이는 다운샘플링(Downsampling) 연산으로, **학습 파라미터 없이** 이동·변형에 강건한 공간 불변성(Spatial Invariance)을 제공한다.
> 2. **가치**: 계산량과 메모리를 줄이고, 소규모 위치 변화에 대한 불변성을 부여하여 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 정확도를 높인다.
> 3. **판단 포인트**: 시험에서는 [최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/))과 평균 풀링(Average Pooling)의 차이, 전역 평균 풀링(GAP, Global Average Pooling)이 완전 연결 계층([FC Layer](/knowledge-base/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/))을 대체하는 원리, 최근 [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)이 풀링을 대체하는 트렌드를 묻는다.

---

## Ⅰ. 개요 및 필요성

### 풀링의 탄생 배경

[합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 계층(Conv Layer)을 쌓을수록 특징 맵의 채널(Channel) 수는 늘어나고 공간 크기는 유지되어 <strong>메모리와 연산량이 폭발</strong>한다. 또한 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서는 물체가 이미지의 정확히 어느 픽셀에 있는지보다 '무엇이 있는지'가 중요하다.

풀링은 다음 두 가지 목표를 동시에 달성한다:
1. **다운샘플링**: 공간 크기를 줄여 이후 계층의 계산량 감소
2. **공간 불변성**: 작은 이동이나 왜곡에도 동일한 출력을 유도

### 풀링의 위치와 역할

```
합성곱 -> 활성화 -> 풀링 -> 합성곱 -> 활성화 -> 풀링 -> FC (분류)
 Conv      ReLU   Pool    Conv     ReLU   Pool   Layer
 3×3       --     2×2     3×3       --     2×2
 v         v      v       v         v      v
32×32     32×32  16×16   16×16    16×16   8×8
```

- **📢 섹션 요약 비유**: 풀링은 '사진 축소' 버튼이다. 100×100 사진을 50×50으로 줄이더라도 고양이인지 강아지인지는 충분히 알 수 있다. 세세한 픽셀 위치보다 전체적인 특징이 중요하기 때문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/))

각 풀링 윈도우(Window) 내에서 <strong>가장 큰 값</strong>을 선택한다. 가장 강한 특징(활성화가 최대인 뉴런)을 보존하므로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에 효과적이다.

```
입력 특징 맵 (4×4)            최대 풀링 (2×2, Stride=2)
+--------------------+       +------------+
|  1   3   2   4     |       |  max(1,3,  |
|  5   6   1   2     |  ->    |  5,6) = 6  | ...
|  3   2   1   0     |       |            |
|  1   2   3   4     |       +------------+
+--------------------+
          v
+--------------------+
|  6   4             |   각 2×2 블록에서 최댓값 선택
|  3   4             |   -> 출력 크기: 2×2
+--------------------+
```

### 평균 풀링 (Average Pooling)

각 윈도우 내 값의 <strong>평균</strong>을 계산한다. 배경 정보를 골고루 반영하므로 부드러운 특징 표현에 유리하다.

| 비교 항목 | [최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) | 평균 풀링 (Average Pooling) |
|:---|:---|:---|
| 선택 방식 | 최댓값 | 평균값 |
| 강점 | 강한 특징 보존, 노이즈에 강함 | 전체적 특징 반영, 부드러운 표현 |
| 사용 예 | VGG, LeNet, [ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) | GoogLeNet 최종층, 시맨틱 분할 |
| 공간 불변성 | 더 강함 | 상대적으로 약함 |

### 전역 평균 풀링 (GAP, Global Average Pooling)

GAP (Global Average Pooling)은 각 채널의 전체 공간에 대해 **단일 평균값** 하나를 출력하는 특수 풀링이다. 이는 <strong>완전 연결 계층(<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/">FC Layer</a>)을 대체</strong>하여 파라미터를 획기적으로 줄인다.

```
일반 완전 연결 (FC) 방식:
+-----------------------------------------+
| 특징 맵 7×7×512 -> Flatten -> FC(25088->1000) |
| 파라미터: 25,088 × 1,000 = 약 2,500만   |
+-----------------------------------------+

GAP (Global Average Pooling) 방식:
+-----------------------------------------+
| 특징 맵 7×7×1024                        |
|    v 각 채널별 7×7 평균                  |
| 벡터 1024 -> Softmax(1000)               |
| 파라미터: 1,024 × 1,000 = 약 100만      |
+-----------------------------------------+
```

GoogLeNet(Inception), MobileNet, [ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) 등 현대 아키텍처에서 GAP는 [FC Layer](/knowledge-base/studynote/10_ai/02_dl_architecture_new/102_fully_connected_layer_dense_flatten_softmax/) 직전에 배치된다.

### 풀링 파라미터 및 출력 크기

풀링도 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)과 동일한 출력 크기 공식을 따른다:

$$O = \left\lfloor \frac{I - F}{S} \right\rfloor + 1$$

([패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 없는 경우, F=2, S=2가 일반적 -> 출력 = 입력의 절반)

| 풀링 크기 | [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) | 비율 | 용례 |
|:---:|:---:|:---:|:---|
| 2×2 | 2 | 1/4 면적 | 일반적 [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) (VGG, AlexNet) |
| 3×3 | 2 | 약 1/4 | AlexNet 일부 계층 |
| 전역 (Global) | - | 채널당 스칼라 | GoogLeNet, MobileNet |

- **📢 섹션 요약 비유**: [최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)은 반 학생 중 '가장 잘하는 학생' 점수를 대표로 뽑는 것, 평균 풀링은 '반 평균' 점수를 뽑는 것이다. GAP는 학교 전체 반 평균을 내서 학교 대표 점수 하나를 만드는 방법이다.

---

## Ⅲ. 비교 및 연결

### 풀링 vs [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (최신 트렌드)

최근에는 <strong>풀링 없이 <a href="/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">스트라이드</a> <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a>(Strided <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/">Convolution</a>)으로 다운샘플링</strong>하는 경향이 증가하고 있다.

| 비교 항목 | 풀링 (Pooling) | [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Strided Conv) |
|:---|:---|:---|
| 학습 파라미터 | 없음 | 있음 (학습 가능) |
| 공간 불변성 | 높음 | 낮음 |
| 특징 학습 | 고정 집약 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 적응적 집약 |
| 사용 예 | 고전 [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) | DCGAN, [ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) 일부 |

<strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/">GAN</a> (<a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/">Generative Adversarial Network</a>)</strong> 의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)자(Generator)에서는 정보 손실을 줄이기 위해 풀링 없이 [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)과 전치 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Transposed [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))을 사용한다.

### 시맨틱 분할에서의 풀링 문제

풀링은 공간 위치 정보를 손실시키므로 픽셀 단위 예측이 필요한 시맨틱 분할(Semantic [Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/))에서는 <strong>팽창 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a>(Dilated <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/">Convolution</a>)</strong>으로 대체하거나, [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)([Encoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))에서의 풀링 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)(Pooling [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))를 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)([Decoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))에서 재사용하는 <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/">최대 풀링</a> 언풀링(Max Unpooling)</strong> 을 사용한다.

- **📢 섹션 요약 비유**: 풀링은 '요약하는 사람'이고 [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 '스스로 요약 방법을 배우는 사람'이다. 고정된 방법(풀링)은 빠르고 안정적이지만, 배워가는 방법([스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/))은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 더 잘 맞는 요약을 만든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 선택 기준

- <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/">최대 풀링</a> 선택</strong>: 물체 탐지([Object Detection](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/)), [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 등 강한 특징 보존이 중요한 경우
- **평균 풀링 / GAP 선택**: 최종 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 직전, 전체 특징 분포가 중요한 경우, 경량 모델
- <strong>풀링 제거 (<a href="/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/">스트라이드</a> <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a> 대체)</strong>: [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델([GAN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/)), 정보 손실 최소화가 필요한 경우

### CAM (Class Activation [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) 과의 연관성

GAP (Global Average Pooling)는 CAM (Class Activation [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))의 핵심 전제이다. GAP 이후 [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) Layer의 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 각 채널 맵을 선형 결합하면 <strong>클래스 활성화 지도(CAM)</strong>를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여, CNN이 어느 영역을 보고 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 결정을 내렸는지 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)할 수 있다.

```
GAP -> FC(softmax) -> 클래스 예측
 ^
채널 × FC 가중치의 선형 결합
= CAM (어느 위치가 분류에 기여했나)
```

### 기술사 서술 포인트

> "풀링 계층은 파라미터 없이 공간 해상도를 줄이고 이동 불변성을 부여한다. 전역 평균 풀링(GAP)은 완전 연결 계층 대비 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) 위험을 줄이고 파라미터를 감소시키며, 클래스 활성화 지도(CAM)를 통한 해석 가능성(Interpretability)을 제공한다는 점에서 현대 CNN의 표준 구성 요소가 되었다."

- **📢 섹션 요약 비유**: GAP는 '채점표 없이 느낌으로 합격자를 고르는 게 아니라, 전체 성적 평균을 내서 객관적으로 판단하는 것'이다. 동시에 그 평균 계산 과정이 투명해서 나중에 왜 합격했는지(CAM)도 설명할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 풀링의 핵심 기여

1. **계산 효율성**: 2×2 [Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/) ([Stride](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)=2)으로 공간 크기 1/4, 이후 연산량 1/4
2. <strong>과적합 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a></strong>: 공간 정보 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)으로 모델이 위치에 집착하지 않도록 함
3. **수용 영역 확대**: 동일한 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이더라도 풀링 후 레이어는 더 넓은 영역 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)

### 풀링 유형 정리

```
+----------------------------------------------------------+
|                     풀링 분류                             |
|                                                          |
|  공간 풀링 --+-- Max Pooling   (최댓값, 가장 강한 특징)   |
|             +-- Avg Pooling   (평균값, 부드러운 특징)     |
|             +-- Stochastic    (랜덤 샘플, 드롭아웃 효과) |
|                                                          |
|  전역 풀링 --+-- GAP          (채널당 전역 평균)          |
|             +-- GMP          (채널당 전역 최댓값)         |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 풀링은 CNN의 '다이어트 전문가'다. 중요하지 않은 위치 세부 정보를 버리고 핵심 특징만 남겨 모델을 날씬하고 튼튼하게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) | 특징 보존, 불변성 / 강한 특징 선택적 추출 |
| 평균 풀링 (Average Pooling) | 부드러운 표현 / 전체 분포 반영 |
| 전역 평균 풀링 (GAP) | [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 대체, CAM / 파라미터 감소 + 해석 가능성 |
| 공간 불변성 (Spatial Invariance) | 이동 강건성 / 풀링의 핵심 효과 |
| [스트라이드](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) | 다운샘플링, 학습 가능 / 풀링 대체 최신 트렌드 |
| CAM (Class Activation [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) | GAP, [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) / GAP 기반 해석 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [풀링 (Pooling)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 풀링은 '큰 그림 보기'야. 4개 칸 중에서 가장 중요한 숫자([최대 풀링](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) 하나만 골라서, 그림을 절반 크기로 작게 만드는 거야.
2. 고양이 사진이 왼쪽에 있든 오른쪽에 있든 풀링 덕분에 컴퓨터는 "어쨌든 고양이네!"라고 알 수 있어.
3. 전역 평균 풀링(GAP)은 반 전체 점수를 평균 내서 번호표 하나로 정리하는 것처럼, 큰 특징 지도를 숫자 하나로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하는 마법이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 285 / 420

<- **이전**: [284. 합성곱 연산 (Convolution)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)
**다음**: [286. 1×1 합성곱 (1x1 Convolution)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/286_1x1_convolution/) ->

---
