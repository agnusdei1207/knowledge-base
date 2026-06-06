---
title: "243. Cnn Stride Pooling Resnet Residual Yolo Object Detection"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CNN([Convolutional Neural Network](/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/))은 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 필터([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) Filter)로 [공간적 지역성](/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/)([Spatial Locality](/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/))과 이동 불변성(Translation Invariance)을 활용해 이미지 특성을 계층적으로 추출하는 신경망이다.
> 2. **가치**: ResNet의 잔차 연결(Residual Connection)은 [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/)([Vanishing Gradient](/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/)) 문제를 극복해 100층 이상의 초심층 네트워크 훈련을 가능하게 했으며, 현대 비전 모델의 기반이 되었다.
> 3. **판단 포인트**: YOLO(You Only Look Once)는 단일 패스(Single Pass)로 전체 이미지를 처리해 실시간 [객체 탐지](/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/)를 달성하며, [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)([Transfer Learning](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))으로 소량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 문제를 해결한다.

---

## Ⅰ. 개요 및 필요성

이미지 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 단순 MLP(Multi-Layer [Perceptron](/studynote/14_data_engineering/05_exam_keywords/239_perceptron_mlp_hidden_layer_weight_activation_sigmoid/))를 적용하면 공간 구조 정보가 소실되고 파라미터 수가 폭증한다. CNN은 이를 해결하기 위해 세 가지 핵심 아이디어를 도입했다.

| 아이디어 | 설명 | 효과 |
|:---|:---|:---|
| 지역 연결 (Local Connectivity) | 작은 필터로 인접 픽셀만 연결 | 파라미터 대폭 감소 |
| [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공유 ([Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Sharing) | 동일 필터를 이미지 전체에 적용 | 이동 불변성 확보 |
| 계층적 특성 추출 | 저수준->고수준 특성 순차 학습 | 추상화된 표현 학습 |

📢 **섹션 요약 비유**: CNN은 사진을 보는 것이 아니라 사진을 스캔하는 돋보기 팀이다. 첫 번째 팀은 선과 모서리를 찾고, 두 번째는 눈·코를 찾고, 세 번째는 얼굴을 인식한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [합성곱 연산](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) ([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) [Operation](/studynote/05_database/06_dw_olap_trends/329_delta_encoding/))

```
입력 이미지 (6×6)    필터 (3×3)      특성 맵 (4×4)
+-------------+    +---------+    +-----------+
| 1 0 1 0 1 0 |    | 1  0 -1 |    |  ?  ?  ?  |
| 0 1 0 1 0 1 | ⊛  | 2  0 -2 | ->  |  ?  ?  ?  |
| 1 0 1 0 1 0 |    | 1  0 -1 |    |  ?  ?  ?  |
| 0 1 0 1 0 1 |    +---------+    +-----------+
| 1 0 1 0 1 0 |
| 0 1 0 1 0 1 |
+-------------+

출력 크기 = (N - F + 2P) / S + 1
  N: 입력 크기, F: 필터 크기, P: 패딩, S: 스트라이드
```

### 핵심 하이퍼파라미터

| 파라미터 | 역할 | 일반값 |
|:---|:---|:---|
| [스트라이드](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) ([Stride](/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)) | 필터 이동 간격, 클수록 출력 축소 | 1~2 |
| [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) ([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) | 경계 픽셀 보존 ('same' [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) | 0~F/2 |
| 필터 수 (Channels) | 추출할 [특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/) 수 | 32, 64, 128... |
| 필터 크기 | 수용 영역 (Receptive Field) 크기 | 3×3, 5×5, 1×1 |

### [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Pooling](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) 연산

```
Max Pooling (2×2, stride=2)
+-----------+        +---------+
|  1  3  2  4|        |  3  4  |
|  5  6  1  2|  ->     |  9  8  |
|  9  3  8  1|        +---------+
|  2  7  4  6|
+-----------+
Max: 각 구역의 최댓값 추출 -> 위치 불변성, 특성 압축
Average: 평균값 -> 전체적 특성 유지
```

### [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) ([Residual Network](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/)) — 잔차 연결

```
일반 레이어           잔차 연결 (Skip Connection)

입력 x               입력 x ------------------+
   v                    v                      |
[Conv Layer]         [Conv Layer]              |
   v                    v                      | (identity)
[Conv Layer]         [Conv Layer]              |
   v                    v                      |
출력 F(x)           출력 F(x) + x <------------+
                    = H(x) = F(x) + x

핵심: F(x) = H(x) - x (잔차만 학습)
-> 기울기가 직통 경로로 역전파 -> 기울기 소실 극복
```

<strong><a href="/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">ResNet</a> 핵심 수식</strong>: `H(x) = F(x) + x`

- F(x): 레이어가 학습하는 잔차 (잔류 오차)
- x: 입력 (직접 연결, 기울기 고속도로)
- 100층 이상에서도 안정적 훈련 가능

📢 **섹션 요약 비유**: ResNet의 잔차 연결은 엘리베이터 같다. 계단(레이어)을 올라가면서 배우는 것도 있지만, 엘리베이터로 처음 정보를 바로 위로 전달하는 직통 경로가 있어서 정보가 사라지지 않는다.

---

## Ⅲ. 비교 및 연결

### 주요 CNN 아키텍처 발전사

| 모델 | 연도 | 층 수 | 특징 | Top-5 Error |
|:---|:---|:---|:---|:---|
| AlexNet | 2012 | 8 | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 딥러닝 시작 | 15.3% |
| VGGNet | 2014 | 16/19 | 3×3 필터 통일 | 7.3% |
| GoogLeNet/Inception | 2014 | 22 | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 필터 조합 | 6.7% |
| [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) | 2015 | 152 | 잔차 연결 | 3.57% |
| DenseNet | 2017 | 201 | 모든 층 직접 연결 | 3.46% |
| EfficientNet | 2019 | - | 복합 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) | 1.8% |

### YOLO (You Only Look Once) — 실시간 [객체 탐지](/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/)

```
기존 2-Stage 탐지 (R-CNN 계열)
입력 -> [Region Proposal] -> [Classification] -> 결과
       (느림)

YOLO 1-Stage 탐지
       S×S 그리드 분할
+------------------------------+
| +----+----+----+----+----+  |
| |    |    |    |    |    |  |
| +----+----+----+----+----+  |
| |    |[★]|    |    |    |  | <- 각 셀이 B개 박스 예측
| +----+----+----+----+----+  |   + 클래스 확률 동시 출력
| |    |    |    |    |    |  |
| +----+----+----+----+----+  |
+------------------------------+
-> 단일 CNN 패스로 위치+분류 동시 예측
-> 실시간(30~100fps) 처리 가능
```

| 방식 | 정확도 | 속도 | 사용 사례 |
|:---|:---|:---|:---|
| R-CNN | 높음 | 느림 (2s/img) | 정밀 분석 |
| Fast R-CNN | 높음 | 중간 | [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) |
| Faster R-CNN | 높음 | 적당 (7fps) | 균형 필요 시 |
| YOLO (v1~v8) | 중간~높음 | 빠름 (30~100fps) | 실시간 탐지 |
| [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) | 중간 | 빠름 | 엣지 디바이스 |

📢 **섹션 요약 비유**: YOLO는 그림을 보자마자 "저기 고양이, 저기 자동차!"라고 한 번에 외치는 것이다. R-CNN은 그림을 조각조각 잘라 각각 "이게 뭐지?"라고 물어보는 방식이라 더 정확하지만 느리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) ([Transfer Learning](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))

```
사전 학습 단계 (ImageNet 1.2M 이미지)
+-----------------------------------------+
| ResNet-50 / VGG-16 / EfficientNet      |
| [Conv Block] [Conv Block] [Conv Block] |
|          [Global Avg Pool]              |
|            [FC: 1000 classes]           |
+-----------------------------------------+
              v 미세조정 (Fine-tuning)
타겟 태스크 (의료 이미지 100장)
+-----------------------------------------+
| ResNet-50 (동결 레이어 <--- 가중치 유지) |
|          [Global Avg Pool]              |
|     [FC: 2 classes (정상/비정상)]       |
+-----------------------------------------+
```

<strong><a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 상위 레이어만 [fine-tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/), 하위 특성 추출 레이어 동결

### 배포 최적화 기법

| 기법 | 설명 | 용도 |
|:---|:---|:---|
| [모델 양자화](/studynote/10_ai/04_ai_ops_ethics/312_quantization/) ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | FP32 -> INT8 변환 | 엣지 디바이스 |
| [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)) | 큰 모델->작은 모델 전달 | 경량화 |
| [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) ([Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 불필요 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 제거 | 메모리 절감 |
| TensorRT | NVIDIA 추론 최적화 | 실시간 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

📢 **섹션 요약 비유**: [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)은 영어를 잘하는 사람이 일본어를 배울 때 외국어 학습 기술 자체를 재활용하는 것과 같다. 처음부터 모국어 감각을 새로 만들 필요가 없다.

---

## Ⅴ. 기대효과 및 결론

### 비전 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 파이프라인

```
이미지 입력
    v
[전처리: 리사이즈, 정규화]
    v
[CNN Backbone: 특성 추출]
    v
[Task-specific Head]
  +-- 분류 (Classification): Softmax FC
  +-- 탐지 (Detection): YOLO / Faster R-CNN
  +-- 분할 (Segmentation): U-Net / Mask R-CNN
  +-- 생성 (Generation): GAN / Diffusion
    v
[후처리: NMS (Non-Maximum Suppression)]
    v
결과 출력
```

### 기술사 시험 핵심 포인트

1. <strong><a href="/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a> 출력 크기 공식</strong>: `(N - F + 2P) / S + 1`
2. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">ResNet</a> 잔차 연결 수식</strong>: `H(x) = F(x) + x` 및 [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) 극복 원리
3. <strong><a href="/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/">Max Pooling</a> vs Average <a href="/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/">Pooling</a></strong> 특성 및 사용 목적
4. **YOLO 1-Stage vs 2-Stage** 속도·정확도 트레이드오프
5. <strong><a href="/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/">전이 학습</a> <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 동결 레이어와 [fine-tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 레이어 결정 기준

📢 **섹션 요약 비유**: CNN은 인간의 시각 피질을 모방한 것이다. 눈에서 V1(선 감지)->V2(모서리)->V4(색상·형태)->IT(물체 인식)로 계층적으로 처리하듯, CNN도 저수준에서 고수준으로 특성을 계층적으로 학습한다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 연산 | [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) ([Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)) | 필터로 공간 특성 추출 |
| [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 연산 | [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Pooling](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) | 공간 해상도 감소, 위치 불변성 |
| 핵심 혁신 | 잔차 연결 (Residual Connection) | [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) 극복 |
| 대표 모델 | [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) | 초심층 네트워크 표준 |
| 탐지 모델 | YOLO | 단일 패스 실시간 탐지 |
| 활용 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) ([Transfer Learning](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)) | 사전 학습 지식 재활용 |
| 경량화 | [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)) | 큰 모델 -> 작은 모델 |
| 연관 분야 | 의미론적 분할 (Semantic [Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/)) | 픽셀 단위 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |

### 👶 어린이를 위한 3줄 비유 설명
1. CNN은 그림을 찾아보는 여러 단계의 돋보기야. 처음엔 선을 찾고, 다음엔 도형을 찾고, 마지막에 고양이라고 알아채는 것처럼 점점 복잡한 것을 찾아.

### 📈 관련 키워드 및 발전 흐름도

```text
MLP (전결합) -> 이미지에 비효율
    |
    v
CNN: Conv + Pooling + Stride -> 공간 특징 추출
    |
    v
발전: LeNet -> AlexNet -> VGG -> ResNet (잔차 연결)
    |
    v
객체 탐지: YOLO · Faster R-CNN · DETR (Transformer)
```
2. ResNet의 잔차 연결은 계단을 오르면서도 엘리베이터로 원래 모습을 꼭대기로 바로 보내는 것이야. 올라가면서 배운 것과 원래 모습을 합쳐서 더 잘 볼 수 있어.
3. YOLO는 그림 전체를 한 번만 보고 "여기 고양이, 저기 자동차"라고 동시에 말하는 것이야. 조각조각 따로 보는 것보다 훨씬 빠르게 모든 물체를 찾을 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 243 / 258

<- **이전**: [242. 규제 드롭아웃 (Dropout) 조기 종료 L1 L2 라쏘 릿지 종합](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)
**다음**: [244. RNN (Recurrent Neural Network) 시계열 LSTM 셀 게이트 장기 의존성 극복](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) ->

---
