+++
weight = 243
title = "243. CNN (Convolutional Neural Network) 스트라이드 풀링 ResNet 잔차 연결 YOLO 객체 탐지"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CNN([[089_CNN_Convolutional|Convolutional Neural Network]])은 [[228_cnn_1d_2d_3d_video_medical|합성곱]] 필터([[284_convolution_stride_padding|Convolution]] Filter)로 [[248_spatial_locality|공간적 지역성]]([[248_spatial_locality|Spatial Locality]])과 이동 불변성(Translation Invariance)을 활용해 이미지 특성을 계층적으로 추출하는 신경망이다.
> 2. **가치**: ResNet의 잔차 연결(Residual Connection)은 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 문제를 극복해 100층 이상의 초심층 네트워크 훈련을 가능하게 했으며, 현대 비전 모델의 기반이 되었다.
> 3. **판단 포인트**: YOLO(You Only Look Once)는 단일 패스(Single Pass)로 전체 이미지를 처리해 실시간 [[288_object_detection_yolo_rcnn|객체 탐지]]를 달성하며, [[132_transfer_learning|전이 학습]]([[132_transfer_learning|Transfer Learning]])으로 소량 [[001_dikw_pyramid|데이터]] 문제를 해결한다.

---

## Ⅰ. 개요 및 필요성

이미지 [[001_dikw_pyramid|데이터]]에 단순 MLP(Multi-Layer [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]])를 적용하면 공간 구조 정보가 소실되고 파라미터 수가 폭증한다. CNN은 이를 해결하기 위해 세 가지 핵심 아이디어를 도입했다.

| 아이디어 | 설명 | 효과 |
|:---|:---|:---|
| 지역 연결 (Local Connectivity) | 작은 필터로 인접 픽셀만 연결 | 파라미터 대폭 감소 |
| [[267_weight_bias_activation|가중치]] 공유 ([[267_weight_bias_activation|Weight]] Sharing) | 동일 필터를 이미지 전체에 적용 | 이동 불변성 확보 |
| 계층적 특성 추출 | 저수준→고수준 특성 순차 학습 | 추상화된 표현 학습 |

📢 **섹션 요약 비유**: CNN은 사진을 보는 것이 아니라 사진을 스캔하는 돋보기 팀이다. 첫 번째 팀은 선과 모서리를 찾고, 두 번째는 눈·코를 찾고, 세 번째는 얼굴을 인식한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[284_convolution_stride_padding|합성곱 연산]] ([[284_convolution_stride_padding|Convolution]] [[329_delta_encoding|Operation]])

```
입력 이미지 (6×6)    필터 (3×3)      특성 맵 (4×4)
┌─────────────┐    ┌─────────┐    ┌───────────┐
│ 1 0 1 0 1 0 │    │ 1  0 -1 │    │  ?  ?  ?  │
│ 0 1 0 1 0 1 │ ⊛  │ 2  0 -2 │ →  │  ?  ?  ?  │
│ 1 0 1 0 1 0 │    │ 1  0 -1 │    │  ?  ?  ?  │
│ 0 1 0 1 0 1 │    └─────────┘    └───────────┘
│ 1 0 1 0 1 0 │
│ 0 1 0 1 0 1 │
└─────────────┘

출력 크기 = (N - F + 2P) / S + 1
  N: 입력 크기, F: 필터 크기, P: 패딩, S: 스트라이드
```

### 핵심 하이퍼파라미터

| 파라미터 | 역할 | 일반값 |
|:---|:---|:---|
| [[097_stride_convolutional_neural_network_downsampling|스트라이드]] ([[097_stride_convolutional_neural_network_downsampling|Stride]]) | 필터 이동 간격, 클수록 출력 축소 | 1~2 |
| [[098_padding_convolutional_neural_network_same_valid|패딩]] ([[098_padding_convolutional_neural_network_same_valid|Padding]]) | 경계 픽셀 보존 ('same' [[098_padding_convolutional_neural_network_same_valid|패딩]]) | 0~F/2 |
| 필터 수 (Channels) | 추출할 [[099_feature_map_activation_map_cnn_output|특성 맵]] 수 | 32, 64, 128... |
| 필터 크기 | 수용 영역 (Receptive Field) 크기 | 3×3, 5×5, 1×1 |

### [[285_pooling_layer|풀링]] ([[285_pooling_layer|Pooling]]) 연산

```
Max Pooling (2×2, stride=2)
┌───────────┐        ┌─────────┐
│  1  3  2  4│        │  3  4  │
│  5  6  1  2│  →     │  9  8  │
│  9  3  8  1│        └─────────┘
│  2  7  4  6│
└───────────┘
Max: 각 구역의 최댓값 추출 → 위치 불변성, 특성 압축
Average: 평균값 → 전체적 특성 유지
```

### [[287_resnet_skip_connection|ResNet]] ([[287_resnet_skip_connection|Residual Network]]) — 잔차 연결

```
일반 레이어           잔차 연결 (Skip Connection)
                    
입력 x               입력 x ──────────────────┐
   ↓                    ↓                      │
[Conv Layer]         [Conv Layer]              │
   ↓                    ↓                      │ (identity)
[Conv Layer]         [Conv Layer]              │
   ↓                    ↓                      │
출력 F(x)           출력 F(x) + x ←───────────┘
                    = H(x) = F(x) + x

핵심: F(x) = H(x) - x (잔차만 학습)
→ 기울기가 직통 경로로 역전파 → 기울기 소실 극복
```

**[[287_resnet_skip_connection|ResNet]] 핵심 수식**: `H(x) = F(x) + x`

- F(x): 레이어가 학습하는 잔차 (잔류 오차)
- x: 입력 (직접 연결, 기울기 고속도로)
- 100층 이상에서도 안정적 훈련 가능

📢 **섹션 요약 비유**: ResNet의 잔차 연결은 엘리베이터 같다. 계단(레이어)을 올라가면서 배우는 것도 있지만, 엘리베이터로 처음 정보를 바로 위로 전달하는 직통 경로가 있어서 정보가 사라지지 않는다.

---

## Ⅲ. 비교 및 연결

### 주요 CNN 아키텍처 발전사

| 모델 | 연도 | 층 수 | 특징 | Top-5 Error |
|:---|:---|:---|:---|:---|
| AlexNet | 2012 | 8 | [[418_gpu|GPU]] 딥러닝 시작 | 15.3% |
| VGGNet | 2014 | 16/19 | 3×3 필터 통일 | 7.3% |
| GoogLeNet/Inception | 2014 | 22 | [[430_index_fast_full_scan|병렬]] 필터 조합 | 6.7% |
| [[287_resnet_skip_connection|ResNet]] | 2015 | 152 | 잔차 연결 | 3.57% |
| DenseNet | 2017 | 201 | 모든 층 직접 연결 | 3.46% |
| EfficientNet | 2019 | - | 복합 [[249_scaling_normalization_standardization|스케일링]] | 1.8% |

### YOLO (You Only Look Once) — 실시간 [[288_object_detection_yolo_rcnn|객체 탐지]]

```
기존 2-Stage 탐지 (R-CNN 계열)
입력 → [Region Proposal] → [Classification] → 결과
       (느림)

YOLO 1-Stage 탐지
       S×S 그리드 분할
┌──────────────────────────────┐
│ ┌────┬────┬────┬────┬────┐  │
│ │    │    │    │    │    │  │
│ ├────┼────┼────┼────┼────┤  │
│ │    │[★]│    │    │    │  │ ← 각 셀이 B개 박스 예측
│ ├────┼────┼────┼────┼────┤  │   + 클래스 확률 동시 출력
│ │    │    │    │    │    │  │
│ └────┴────┴────┴────┴────┘  │
└──────────────────────────────┘
→ 단일 CNN 패스로 위치+분류 동시 예측
→ 실시간(30~100fps) 처리 가능
```

| 방식 | 정확도 | 속도 | 사용 사례 |
|:---|:---|:---|:---|
| R-CNN | 높음 | 느림 (2s/img) | 정밀 분석 |
| Fast R-CNN | 높음 | 중간 | [[228_batch_processing_hadoop_spark|배치 처리]] |
| Faster R-CNN | 높음 | 적당 (7fps) | 균형 필요 시 |
| YOLO (v1~v8) | 중간~높음 | 빠름 (30~100fps) | 실시간 탐지 |
| [[327_ssd|SSD]] | 중간 | 빠름 | 엣지 디바이스 |

📢 **섹션 요약 비유**: YOLO는 그림을 보자마자 "저기 고양이, 저기 자동차!"라고 한 번에 외치는 것이다. R-CNN은 그림을 조각조각 잘라 각각 "이게 뭐지?"라고 물어보는 방식이라 더 정확하지만 느리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[132_transfer_learning|전이 학습]] ([[132_transfer_learning|Transfer Learning]])

```
사전 학습 단계 (ImageNet 1.2M 이미지)
┌─────────────────────────────────────────┐
│ ResNet-50 / VGG-16 / EfficientNet      │
│ [Conv Block] [Conv Block] [Conv Block] │
│          [Global Avg Pool]              │
│            [FC: 1000 classes]           │
└─────────────────────────────────────────┘
              ↓ 미세조정 (Fine-tuning)
타겟 태스크 (의료 이미지 100장)
┌─────────────────────────────────────────┐
│ ResNet-50 (동결 레이어 ←── 가중치 유지) │
│          [Global Avg Pool]              │
│     [FC: 2 classes (정상/비정상)]       │
└─────────────────────────────────────────┘
```

**[[268_strategy_pattern|전략]]**: 상위 레이어만 [[304_fine_tuning|fine-tuning]], 하위 특성 추출 레이어 동결

### 배포 최적화 기법

| 기법 | 설명 | 용도 |
|:---|:---|:---|
| [[312_quantization|모델 양자화]] ([[434_quantization|Quantization]]) | FP32 → INT8 변환 | 엣지 디바이스 |
| [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) | 큰 모델→작은 모델 전달 | 경량화 |
| [[435_pruning_hardware|가지치기]] ([[435_pruning_hardware|Pruning]]) | 불필요 [[267_weight_bias_activation|가중치]] 제거 | 메모리 절감 |
| TensorRT | NVIDIA 추론 최적화 | 실시간 [[090_service_kubernetes_network_load_balancing|서비스]] |

📢 **섹션 요약 비유**: [[132_transfer_learning|전이 학습]]은 영어를 잘하는 사람이 일본어를 배울 때 외국어 학습 기술 자체를 재활용하는 것과 같다. 처음부터 모국어 감각을 새로 만들 필요가 없다.

---

## Ⅴ. 기대효과 및 결론

### 비전 [[190_ai_llm_requirements_specification|AI]] 파이프라인

```
이미지 입력
    ↓
[전처리: 리사이즈, 정규화]
    ↓
[CNN Backbone: 특성 추출]
    ↓
[Task-specific Head]
  ├── 분류 (Classification): Softmax FC
  ├── 탐지 (Detection): YOLO / Faster R-CNN
  ├── 분할 (Segmentation): U-Net / Mask R-CNN
  └── 생성 (Generation): GAN / Diffusion
    ↓
[후처리: NMS (Non-Maximum Suppression)]
    ↓
결과 출력
```

### 기술사 시험 핵심 포인트

1. **[[228_cnn_1d_2d_3d_video_medical|합성곱]] 출력 크기 공식**: `(N - F + 2P) / S + 1`
2. **[[287_resnet_skip_connection|ResNet]] 잔차 연결 수식**: `H(x) = F(x) + x` 및 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 극복 원리
3. **[[101_max_pooling_average_pooling_global_average_pooling|Max Pooling]] vs Average [[285_pooling_layer|Pooling]]** 특성 및 사용 목적
4. **YOLO 1-Stage vs 2-Stage** 속도·정확도 트레이드오프
5. **[[132_transfer_learning|전이 학습]] [[268_strategy_pattern|전략]]**: 동결 레이어와 [[304_fine_tuning|fine-tuning]] 레이어 결정 기준

📢 **섹션 요약 비유**: CNN은 인간의 시각 피질을 모방한 것이다. 눈에서 V1(선 감지)→V2(모서리)→V4(색상·형태)→IT(물체 인식)로 계층적으로 처리하듯, CNN도 저수준에서 고수준으로 특성을 계층적으로 학습한다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 기반 연산 | [[228_cnn_1d_2d_3d_video_medical|합성곱]] ([[284_convolution_stride_padding|Convolution]]) | 필터로 공간 특성 추출 |
| [[347_compaction|압축]] 연산 | [[285_pooling_layer|풀링]] ([[285_pooling_layer|Pooling]]) | 공간 해상도 감소, 위치 불변성 |
| 핵심 혁신 | 잔차 연결 (Residual Connection) | [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 극복 |
| 대표 모델 | [[287_resnet_skip_connection|ResNet]] | 초심층 네트워크 표준 |
| 탐지 모델 | YOLO | 단일 패스 실시간 탐지 |
| 활용 [[268_strategy_pattern|전략]] | [[132_transfer_learning|전이 학습]] ([[132_transfer_learning|Transfer Learning]]) | 사전 학습 지식 재활용 |
| 경량화 | [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) | 큰 모델 → 작은 모델 |
| 연관 분야 | 의미론적 분할 (Semantic [[364_segmentation|Segmentation]]) | 픽셀 단위 [[104_classification_analysis|분류]] |

### 👶 어린이를 위한 3줄 비유 설명
1. CNN은 그림을 찾아보는 여러 단계의 돋보기야. 처음엔 선을 찾고, 다음엔 도형을 찾고, 마지막에 고양이라고 알아채는 것처럼 점점 복잡한 것을 찾아.

### 📈 관련 키워드 및 발전 흐름도

```text
MLP (전결합) → 이미지에 비효율
    │
    ▼
CNN: Conv + Pooling + Stride → 공간 특징 추출
    │
    ▼
발전: LeNet → AlexNet → VGG → ResNet (잔차 연결)
    │
    ▼
객체 탐지: YOLO · Faster R-CNN · DETR (Transformer)
```
2. ResNet의 잔차 연결은 계단을 오르면서도 엘리베이터로 원래 모습을 꼭대기로 바로 보내는 것이야. 올라가면서 배운 것과 원래 모습을 합쳐서 더 잘 볼 수 있어.
3. YOLO는 그림 전체를 한 번만 보고 "여기 고양이, 저기 자동차"라고 동시에 말하는 것이야. 조각조각 따로 보는 것보다 훨씬 빠르게 모든 물체를 찾을 수 있어.
