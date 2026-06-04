+++
title = "286. 1×1 합성곱 (1x1 Convolution)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(1x1 [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/), Pointwise [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))은 공간 정보(Spatial Information)를 그대로 유지하면서 채널(Channel) 수만 선택적으로 변환하는 연산으로, 채널 간 선형 결합(Linear Combination)을 학습한다.
> 2. **가치**: [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/))로 계산량을 대폭 줄이고, 비선형 [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)(Non-linear Activation)와 결합하여 표현력을 높이면서도 파라미터를 효율적으로 사용한다.
> 3. **판단 포인트**: 시험에서는 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)이 채널 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)로 어떻게 연산량을 줄이는지 계산, 보틀넥 구조([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/) [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))에서의 역할, NIN (Network in Network), GoogLeNet(Inception), ResNet에서의 활용 맥락을 묻는다.

---

## Ⅰ. 개요 및 필요성

### 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 등장 배경

딥러닝 네트워크가 깊어질수록 채널 수가 수백~수천 개로 늘어나고, 이후의 3×3 [합성곱 연산](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)량이 <strong>채널 수의 제곱에 비례</strong>하여 증가한다. 예를 들어 256채널 입력에 3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)으로 256채널 출력을 만들면 약 5900만(256×256×9) 번의 곱셈이 필요하다.

1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 이를 해결하기 위해 <strong>2014년 NIN (Network in Network, Lin et al.)</strong>에서 처음 제안되었고, GoogLeNet(Inception)과 ResNet에 채택되어 현대 CNN의 표준 기법이 되었다.

### 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 핵심 특성

| 특성 | 설명 |
|:---|:---|
| 공간 크기 유지 | H×W는 변하지 않음 ([패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 없이 [Stride](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/)=1) |
| 채널 수 변환 | C_in -> C_out (증가 또는 축소 가능) |
| 학습 파라미터 | C_in × C_out (공간 차원 없음) |
| 계산 복잡도 | O(H × W × C_in × C_out) |
| [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/) | ReLU와 결합하여 비선형성 추가 |

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 '채널 믹싱 DJ'다. 공간 위치는 건드리지 않고, 여러 채널(악기)의 소리를 섞어 새로운 채널(믹스 트랙)을 만드는 작업이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1×1 [합성곱 연산](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/) 원리

```
입력 특징 맵: H × W × C_in
                    |
           1×1 합성곱 필터 C_out개
           (각 필터 크기: 1×1×C_in)
                    |
                    v
출력 특징 맵: H × W × C_out

예시: 입력 28×28×256, 1×1 Conv, 64 필터
+----------------------------------------------+
|  입력 (28×28×256)                            |
|  각 위치 (i,j) 에서 256차원 벡터             |
|         v                                   |
|  W (64×256) 행렬과 내적 연산                 |
|  = 채널 방향 선형 결합                       |
|         v                                   |
|  출력 (28×28×64)                             |
|  채널 수 256 -> 64 로 축소                    |
+----------------------------------------------+
파라미터 수: 256 × 64 = 16,384 (바이어스 제외)
```

### 보틀넥 구조 ([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/) [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))

ResNet의 50층 이상 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에서 사용되는 보틀넥 블록은 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)으로 채널을 줄인 뒤 3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)을 수행하고, 다시 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)으로 채널을 복원한다.

```
보틀넥 블록 (ResNet-50 기준):

입력: 256채널
    |
    v
+----------------------+
| 1×1 Conv, 64채널     |  <- 채널 축소 (256->64)
| BN + ReLU            |     파라미터: 256×64 = 16K
+----------------------+
    |
    v
+----------------------+
| 3×3 Conv, 64채널     |  <- 공간 특징 추출
| BN + ReLU            |     파라미터: 64×64×9 = 36K
+----------------------+
    |
    v
+----------------------+
| 1×1 Conv, 256채널    |  <- 채널 복원 (64->256)
| BN + ReLU            |     파라미터: 64×256 = 16K
+----------------------+
    |
    + (Shortcut)
    v
출력: 256채널

총 파라미터: 68K
vs 2개의 3×3 Conv만 사용 시: 256×256×9×2 = 1,179K
-> 약 17배 파라미터 감소!
```

### Inception [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에서의 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)

GoogLeNet의 인셉션(Inception) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)은 여러 크기의 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 적용하기 전에 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)으로 채널을 줄여 계산량을 제어한다.

```
입력 특징 맵
      |
 +----+----------------------+
 |         |         |      |
1×1       1×1->3×3  1×1->5×5  MP->1×1
Conv      Conv      Conv    Conv
 |         |         |      |
 +----+----------------------+
      |
Concatenate (채널 방향 결합)
      |
출력 특징 맵
```

### 연산량 비교 (1×1 Conv 유무)

| 구성 | 연산량 (곱셈 횟수) | 절감 비율 |
|:---|:---:|:---:|
| 입력 28×28×256, 3×3->256 직접 | 28×28×256×256×9 = 462M | - |
| 1×1(->64) + 3×3(->64) + 1×1(->256) | 약 27M | **약 17배 감소** |

- **📢 섹션 요약 비유**: 보틀넥 구조는 '병목이 있는 모래시계'다. 넓은 위에서(256채널) 좁은 목(64채널)을 통과하며 핵심만 추려내고, 다시 넓은 아래로(256채널) 퍼진다. 좁은 목 덕분에 가운데 3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 계산량이 확 줄어든다.

---

## Ⅲ. 비교 및 연결

### 관련 기법과의 비교

| 기법 | 공간 처리 | 채널 처리 | 파라미터 | 특징 |
|:---|:---:|:---:|:---:|:---|
| 일반 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (3×3 Conv) | O | O | C_in×C_out×9 | 공간+채널 동시 처리 |
| 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Pointwise) | X | O | C_in×C_out | 채널 믹싱만 |
| 깊이별 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Depthwise) | O | X | C_in×F^ | 채널별 독립 공간 처리 |
| 깊이별 분리 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (DS Conv) | O->X | X->O | C_in×F^+C_in×C_out | 위 두 개 순차 결합 |

### NIN (Network in Network)과의 연관

NIN (Network in Network, 2013년 Lin et al.)은 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 후 MLP (Multi-Layer [Perceptron](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/239_perceptron_mlp_hidden_layer_weight_activation_sigmoid/))를 적용하는 개념을 제안했는데, 이 MLP가 실질적으로 <strong>1×1 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/">합성곱</a>의 연속</strong>과 동일하다. 각 위치에서 채널 벡터에 다층 변환을 적용하는 것이기 때문이다.

### MobileNet의 깊이별 분리 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Depthwise Separable [Convolution](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))

MobileNet은 일반 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)을 깊이별 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Depthwise Conv)과 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Pointwise Conv)으로 분해하여 모바일 환경에서도 동작하는 경량 CNN을 구현했다.

- **📢 섹션 요약 비유**: 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 '채널 번역가'다. 256개 언어(채널)로 된 정보를 64개 언어로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 번역한다. 나중에 필요하면 다시 256개로 번역 복원도 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 사용 시나리오

1. <strong>채널 축소 (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/">Dimensionality Reduction</a>)</strong>: 연산량 줄이기 전 전처리 단계
2. **채널 증가**: 특징 공간을 풍부하게 확장할 때
3. **비선형성 추가**: ReLU와 결합하여 표현력 향상 (GAP 전 마지막 1×1 Conv)
4. **채널 정렬**: 잔차 연결(Skip Connection)에서 채널 수 맞추기

### ResNet에서의 채널 정렬

ResNet의 스킵 연결(Skip Connection)에서 입력과 출력의 채널 수가 다를 때, 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Projection Shortcut)으로 차원을 맞춘다.

```
입력 (64채널)   잔차 블록   출력 (256채널)
     |                         |
     +--- 1×1 Conv(->256) -----+
     |                         |
     +---- F(x) --------------++
     (보틀넥 연산 결과 256채널)
```

### 기술사 서술 포인트

> "1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 공간 특징을 유지하면서 채널 차원의 선형 변환을 학습한다. 보틀넥 구조에서 채널 축소-3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)-채널 복원 패턴으로 연산량을 수십 배 감소시키며, ReLU와의 결합으로 비선형 표현력도 증가시킨다. GoogLeNet과 ResNet에서 깊은 네트워크를 효율적으로 구성하는 핵심 수단이다."

- **📢 섹션 요약 비유**: 실무에서 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 '인력 효율화 전문가'다. 256명이 하던 일을 64명 핵심 인력으로 재편성해서 3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(주요 작업)을 시키고, 다시 256명 규모로 복귀한다. 비용(연산)은 줄이면서 품질(특징 표현)은 유지한다.

---

## Ⅴ. 기대효과 및 결론

### 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 3대 효과

1. **계산량 감소**: 보틀넥으로 3×3 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) 입력 채널 수 감소 -> 연산 비용 1/N^
2. **비선형성 증가**: 추가 파라미터 없이 표현력 향상
3. **채널 간 상호 정보 학습**: 채널 조합 최적화로 특징 재구성

### 채널 축소 연산량 공식

```
+------------------------------------------------------+
| 1×1 Conv 연산량 절감 계산                            |
|                                                      |
| 직접 3×3 Conv:                                       |
|   H×W × C_in × C_out × 9                            |
|                                                      |
| 1×1(->k) + 3×3(->k) + 1×1(->C_out):                  |
|   H×W×C_in×k + H×W×k×k×9 + H×W×k×C_out             |
|                                                      |
| k = C_in/4 일 때 약 4배 이상 절감                    |
+------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 CNN의 '[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.zip)'이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(채널)를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해서 전달하고, 받은 쪽에서 다시 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 해제하는 방식으로 통신 비용(연산량)을 극적으로 줄인다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Pointwise Conv) | 채널 축소, 비선형성 / 채널 차원 변환의 핵심 |
| 보틀넥 구조 ([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/)) | [ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/), 채널 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) / 1×1->3×3->1×1 패턴 |
| NIN (Network in Network) | MLP, 채널 변환 / 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 기원 |
| GoogLeNet (Inception) | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), 효율 / Inception [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 축소 역할 |
| 깊이별 분리 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (DS Conv) | MobileNet, 경량화 / Depthwise + Pointwise |
| [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) ([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/)) | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) / 채널 방향 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [1×1 합성곱 (1x1 Convolution)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 1×1 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 '색 섞기' 마법이야. 빨강·파랑·노랑(256채널)을 섞어서 보라·초록(64채널) 새 색을 만드는 것처럼 채널을 새롭게 조합해.
2. 공간(그림의 위치)은 전혀 바꾸지 않아. 오직 색깔(채널)만 바꿔서 다음 작업이 훨씬 가볍게 처리되도록 도와줘.
3. 보틀넥 구조는 좁은 빨대로 음료를 마시는 것과 같아. 입구를 좁혀서 한 번에 조금씩 처리하면 힘이 덜 들고, 다 마신 후엔 원래대로 돌아와.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 286 / 420

<- **이전**: [285. 풀링 (Pooling)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)
**다음**: [287. ResNet (Residual Network)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) ->

---
