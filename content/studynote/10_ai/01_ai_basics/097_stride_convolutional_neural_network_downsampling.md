+++
title = "97. 스트라이드 (Stride) - CNN 필터 이동 보폭과 특징 맵 축소"
date = 2026-04-10

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스트라이드 (Stride)는 [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) ([Convolutional Neural Network](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/))에서 필터 (Filter)가 입력 이미지를 순회하며 특성을 추출할 때, 한 번에 이동하는 픽셀(보폭)의 간격이다.
> 2. **가치**: 보폭을 크게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(Stride $\ge$ 2)하면 연산량이 감소하고 출력 [특성 맵](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/) ([Feature Map](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))의 차원이 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)되어, [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Pooling](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) 층 없이도 공간적 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) (Downsampling) 효과를 낸다.
> 3. **판단 포인트**: 정보 손실을 최소화하며 특징을 세밀하게 추출할 것인지, 아니면 약간의 정보 유실을 감수하고 연산 속도와 메모리 효율을 극대화할 것인지 결정하는 핵심 하이퍼파라미터다.

---

## Ⅰ. 개요 및 필요성

스트라이드 (Stride)는 [합성곱 층](/knowledge-base/studynote/10_ai/01_ai_basics/096_convolution_layer_filter_stride_padding/) ([Convolution Layer](/knowledge-base/studynote/10_ai/01_ai_basics/096_convolution_layer_filter_stride_padding/))이 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 스캔할 때 필터가 이동하는 픽셀 수를 정의하는 매개변수다. 스트라이드가 1이면 필터가 한 칸씩 이동하며 촘촘하게 이미지를 훑고, 2 이상이면 듬성듬성 건너뛰며 이동한다.

이 개념이 필요한 이유는 이미지 해상도가 커질수록 모델이 처리해야 할 연산량이 기하급수적으로 증가하기 때문이다. 모든 픽셀을 1칸씩 스캔하면 미세한 특징을 전부 보존할 수 있지만, 수백만 개의 픽셀을 처리하느라 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리와 계산 자원에 심각한 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))이 발생한다. 따라서 공간적 차원을 줄이면서도 의미 있는 전역 특징(Global Feature)을 유지하기 위해 보폭을 조절하는 기법이 필수적이다.

- **📢 섹션 요약 비유**: 스트라이드는 해변에서 금속 탐지기로 동전을 찾는 보폭과 같다. 보폭이 작으면 모래사장 전체를 꼼꼼히 뒤져 모든 동전을 찾지만 하루 종일 걸리고, 보폭이 크면 작은 동전은 놓칠 수 있지만 해변 전체를 순식간에 탐색할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[합성곱 연산](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)에서 스트라이드는 입력 이미지의 크기, 필터의 크기, [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))과 결합하여 출력 [특성 맵](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 크기를 결정한다. 스트라이드가 커질수록 출력 크기는 반비례하여 작아진다.

<strong>출력 <a href="/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/">특성 맵</a> 크기 계산 공식:</strong>
$$ \text{Output Size} = \lfloor \frac{\text{Input} + 2 \times \text{[Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)} - \text{Filter}}{\text{Stride}} \rfloor + 1 $$



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stride 1 vs Stride 2 의 스캔 방식 비교 (1D 예시)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력 데이터</div><div class="kb-diagram-note">1 2 3 4 5</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Stride = 1</div><div class="kb-diagram-note">─ ─</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">필터 이동 1,2,3 -&gt; 2,3,4 -&gt; 3,4,5 (출력 크기: 3)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Stride = 2</div><div class="kb-diagram-note">─ ─</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">필터 이동 1,2,3 ----------&gt; 3,4,5 (출력 크기: 2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* Stride가 커지면 필터의 중첩(Overlap) 영역이 줄어듦</div></div>
</div>
</div>



이 다이어그램은 스트라이드의 크기에 따라 필터가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 건너뛰는 방식을 보여준다. `Stride=2`를 적용하면 가로와 세로 차원이 각각 1/2로 줄어들어 전체 [특성 맵](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)의 면적(연산량)은 1/4로 극적으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)된다.

- **📢 섹션 요약 비유**: 스트라이드는 카메라의 사진 촬영 해상도를 낮추는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 같다. 원본(입력)은 4K지만, 저해상도 요약 모드(Stride 2)로 렌즈를 훑으면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 용량이 1/4로 줄어든 1080p 요약본([특성 맵](/knowledge-base/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/))이 나온다.

---

## Ⅲ. 비교 및 연결

해상도를 줄이는 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) (Downsampling) 기법으로는 맥스 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/))과 스트라이드 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Strided [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))이 자주 비교된다.

| 항목 | 맥스 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) | 스트라이드 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Strided [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)) |
| :--- | :--- | :--- |
| **방식** | 촘촘히 스캔(Stride 1) 후 가장 큰 값만 남김 | 처음부터 듬성듬성 스캔(Stride $\ge$ 2) |
| **연산량** | 특징 추출 연산 후 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) 연산 추가 (비효율 발생 가능) | 특징 추출과 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)를 한 번에 처리 |
| **정보 손실** | 정해진 규칙(Max/Average)에 의해 강제로 정보 폐기 | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)([Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)) 학습을 통해 중요한 정보를 스스로 유지 |
| **적용 트렌드** | 과거 아키텍처 (VGGNet 등) | 현대 아키텍처 ([ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/), MobileNet 등) |

최근의 딥러닝 트렌드는 별도의 [풀링 층](/knowledge-base/studynote/10_ai/01_ai_basics/100_pooling_layer_max_pooling_downsampling_cnn/)을 두는 대신, [합성곱 층](/knowledge-base/studynote/10_ai/01_ai_basics/096_convolution_layer_filter_stride_padding/) 내부에서 스트라이드를 키워 모델이 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 과정 자체를 "학습"하게 만드는 방향으로 발전했다.

- **📢 섹션 요약 비유**: [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)이 고화질로 사진을 찍은 뒤 포토샵으로 강제로 픽셀을 뭉개버리는(가위질) 2중 작업이라면, 스트라이드 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 애초에 사진을 찍을 때부터 필요한 정보만 골라 담는 스마트 렌즈를 사용하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 아키텍처를 설계할 때 스트라이드 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 연산 자원과 모델 정확도를 결정짓는 핵심 의사결정이다. 자원이 제한된 엣지 디바이스(Edge Device)나 실시간 처리가 필요한 시스템에서는 스트라이드 튜닝이 필수적이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **입출력 차원 매칭**: [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)한 스트라이드 값으로 나눈 결과가 정수로 딱 떨어지는가? (나머지가 생기면 프레임워크에 따라 비대칭 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 문제가 발생할 수 있다.)
2. **미세 특징의 중요도**: 질병 진단 의료 이미지처럼 1픽셀의 미세한 점이 중요한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)인가? (이 경우 전반부에 너무 큰 스트라이드를 주면 치명적이다.)
3. **병목 구간 회피**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 층(Layer)의 입력 해상도가 너무 커서 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out Of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))이 발생하지 않는가?

### 실무 판단 가이드
- **채택 (Stride $\ge$ 2)**: 스마트폰 얼굴 인식, 자율주행 차량의 [객체 탐지](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/)처럼 초당 프레임(FPS)과 연산 속도가 생명인 실시간 비전 모델 설계 시 우선 채택한다.
- **회피 (Stride 1 유지)**: 초고해상도 복원 (Super Resolution), 의료 영상 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)) 등 원본 이미지의 디테일과 픽셀 단위의 정확한 위치 정보가 필요한 경우엔 공간 차원을 줄이지 말아야 한다.

- **📢 섹션 요약 비유**: 스트라이드 결정은 돋보기로 책을 읽을 때 속독을 할지 정독을 할지 고르는 것과 같다. 만화책(대략적인 객체)은 듬성듬성 속독해도 내용을 알지만, 계약서(의료 영상)는 한 글자씩 정독해야 사기를 당하지 않는다.

---

## Ⅴ. 기대효과 및 결론

스트라이드의 도입은 딥러닝 모델이 무거운 이미지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르고 효율적으로 소화하게 만든 일등 공신이다. 이를 통해 연산 병목을 제거하고, 전체 네트워크를 더 깊게 쌓을 수 있는(Deep Network) 토대를 마련했다. 

하지만 스트라이드를 과도하게 높이면 중요한 위치 정보(Spatial Information)가 영구적으로 유실될 한계가 존재한다. 따라서 현대의 CNN은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 층에서는 미세한 특징을 뽑고(Stride 1), 깊어질수록 공간을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하며 추상적인 특징을 잡는(Stride 2) 계층적 구조를 통해 속도와 정확도의 최적 타협점을 찾는다.

- **📢 섹션 요약 비유**: 스트라이드는 자동차의 기어 변속과 같다. 저단 기어(Stride 1)로 묵직하고 꼼꼼하게 힘을 쓰다가, 고단 기어(Stride 2)로 변속해 휙휙 속도를 내며 모델이라는 차를 효율적으로 굴린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) ([Convolutional Neural Network](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/)) | 스트라이드가 동작하는 딥러닝 아키텍처의 기반 환경 |
| [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) ([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) | 스트라이드 적용 시 가장자리 정보 유실과 차원을 보정하는 짝꿍 기법 |
| 맥스 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Max Pooling](/knowledge-base/studynote/10_ai/02_dl_architecture_new/101_max_pooling_average_pooling_global_average_pooling/)) | 스트라이드 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)과 동일하게 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)를 담당하는 경쟁적 기법 |
| 수용 영역 (Receptive Field) | 스트라이드가 누적될수록 다음 층 뉴런이 바라보는 원본 이미지의 범위가 기하급수적으로 커짐 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">합성곱 층 연산 기초 확립</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">스트라이드 (Stride) · 필터 이동 보폭 제어</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">맥스 풀링 (Max Pooling) 대체 · Strided Convolution 활성화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">모바일 최적화 네트워크 (MobileNet 등) · 연산량 감소</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">확장 합성곱 (Dilated Convolution) · 해상도 유지하며 수용 영역 확장</div>
</div>
</div>



이 흐름도는 "보폭 제어 → [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) 대체 → 경량화 → 단점(해상도 저하) 보완"으로 이어지는 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 구조의 진화 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 큰 그림을 돋보기로 살필 때, 오른쪽으로 1칸씩 촘촘히 옮기면 시간이 너무 오래 걸려요.
2. 그래서 돋보기를 2칸씩 껑충껑충 건너뛰면서 살피는 방법을 '스트라이드'라고 불러요.
3. 이렇게 껑충 뛰면 시간도 절약되고, 그림의 핵심만 뽑은 작은 요약본을 순식간에 만들 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 420

← **이전**: [96. 합성곱 층 (Convolution Layer) - 필터 스캐닝 특징 추출](/knowledge-base/studynote/10_ai/01_ai_basics/096_convolution_layer_filter_stride_padding/)
**다음**: [98. 패딩 (Padding) - 이미지 크기 축소 방지와 가장자리 보존](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) →

---
