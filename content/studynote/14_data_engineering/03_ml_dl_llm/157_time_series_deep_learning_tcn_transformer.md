---
title: "Time Series Deep Learning Tcn Transformer"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 157
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCN (Temporal Convolutional Network, 시간 [합성곱 신경망](/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/))은 팽창 인과 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Dilated Causal [Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))으로 긴 시계열을 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리해 [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/)/LSTM의 순차 처리 병목을 제거한다.
> 2. **가치**: 팽창률(Dilation Rate)을 지수적으로 키워 적은 레이어로 긴 역사(Long History)를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하며, [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) Time-Series 모델과 함께 현대 시계열 예측의 표준이 되었다.
> 3. **판단 포인트**: TCN은 고정 수용 영역(Receptive Field)과 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 학습에 강하고, [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 계열(PatchTST, iTransformer)은 긴 시퀀스·전역 패턴 포착에 강하다.

## Ⅰ. 개요 및 필요성

주가 예측, 수요 예측, [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석은 모두 시계열(Time Series) 문제다. LSTM이 주류였지만 시퀀스가 길어질수록 훈련이 느리고 메모리 병목이 발생한다.

TCN은 CNN의 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 시계열에 적용하고, 팽창 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)(Dilated [Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/))으로 지수적으로 넓은 역사를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한다. 2018년 연구에서 TCN이 대부분의 시계열 태스크에서 LSTM을 능가함이 증명됐다.

<strong><a href="/studynote/10_ai/03_llm_nlp/206_tcn_time_series/">시계열 딥러닝</a> 발전 경로</strong>
- [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) (2012~): 순차 처리, [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) 문제
- TCN (2018): [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), 고정 수용 영역
- [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 계열 (2020~): 셀프 어텐션 전역 의존성
- PatchTST, iTransformer (2023~): 장기 예측 특화

📢 **섹션 요약 비유**: TCN은 여러 망원경을 동시에 다른 시점에 겨냥해 하늘을 촬영하는 것처럼, 여러 시점을 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 분석한다.

## Ⅱ. 아키텍처 및 핵심 원리

| 개념 | 설명 |
|:---|:---|
| 인과 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Causal Conv) | 현재 시점은 과거만 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) (미래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누설 방지) |
| 팽창 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Dilated Conv) | 필터 사이에 간격(dilation)을 두어 수용 영역 확장 |
| 팽창률 (Dilation Rate) | 레이어마다 2배 증가 (1,2,4,8,16,...) |
| 수용 영역 (Receptive Field) | L개 레이어, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) k, 최대 dilation d -> RF=(k-1)×d_max+1 |
| 잔차 연결 (Residual Connection) | [기울기 소실](/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) 방지, 깊은 TCN 학습 |

```
[팽창 인과 합성곱 (Dilation=1,2,4)]

입력 시계열: t₁ t₂ t₃ t₄ t₅ t₆ t₇ t₈

Layer 1 (dilation=1):
  | | | | | | | |
  o o o o o o o o  <- 커널 크기 3, 매 1칸

Layer 2 (dilation=2):
  |   |   |   |
  o   o   o   o  <- 매 2칸 건너뜀

Layer 3 (dilation=4):
  |       |
  o       o  <- 매 4칸 건너뜀

수용 영역: (3-1)×4 + 1 = 9 타임스텝
3개 레이어만으로 9 타임스텝 역사 참조!

[TCN 전체 구조]
입력 시퀀스
     |
+----v----------------------------+
|  Dilated Causal Conv (d=1)       |
|  + 배치 정규화 + ReLU            |
+--------------------------------+
     |
+----v----------------------------+
|  Dilated Causal Conv (d=2)       |
+--------------------------------+
     |
+----v----------------------------+
|  Dilated Causal Conv (d=4)       |
+--------------------------------+
     |
   Residual Block 반복
     |
   예측 출력
```

<strong>시계열 <a href="/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a> 모델 비교</strong>

| 모델 | 핵심 아이디어 | 장점 |
|:---|:---|:---|
| Informer ([2021](/studynote/04_software_engineering/11_testing_validation/869_owasp_top_10_2021/)) | Sparse Attention (ProbSparse) | 긴 시퀀스 O(n log n) |
| Autoformer ([2021](/studynote/04_software_engineering/11_testing_validation/869_owasp_top_10_2021/)) | 자동 상관 기반 어텐션 | 주기 패턴 |
| PatchTST (2023) | 시계열을 패치로 분할 | 장기 예측, [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) |
| iTransformer (2024) | 변수 축으로 어텐션 | 다변량 시계열 |
| TimesNet (2023) | 1D -> 2D 시간 이미지 변환 | 복잡 패턴 |

📢 **섹션 요약 비유**: 팽창 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 과거를 보는 창문 크기가 레이어마다 2배씩 커지는 망원경이다. 적은 층으로도 수백 타임스텝 전을 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한다.

## Ⅲ. 비교 및 연결

| 항목 | [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | TCN | [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |
|:---|:---|:---|:---|
| [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 | ❌ | ✅ | ✅ |
| [장기 의존성](/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/) | 보통 | 고정 RF | ✅ 전역 |
| 메모리 | 낮음 | 중간 | 높음 |
| 학습 속도 | 느림 | 빠름 | 중간~빠름 |
| 추론 속도 | 빠름 | 빠름 | 중간 |
| 인과성 보장 | ✅ | ✅ | ✅ (Masked) |

📢 **섹션 요약 비유**: LSTM이 역사 기록을 한 페이지씩 읽는다면, TCN은 여러 시대의 책을 동시에 펼쳐보는 것이고, Transformer는 책 전체를 동시에 훑는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

**시계열 태스크별 모델 선택**
- 단기 예측 (1~24 스텝): [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/), TCN 모두 적합
- 장기 예측 (96~720 스텝): PatchTST, iTransformer
- [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/): TCN 기반 [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)
- 실시간 스트리밍: TCN (빠른 추론)

<strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 전처리 핵심</strong>
- 정상성 ([Stationarity](/studynote/10_ai/05_data_science_ml/377_time_series_stationarity/)): ADF 테스트, 차분(Differencing)
- 계절 분해: STL, X-13 [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/)-SEATS
- [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/): MinMax 또는 z-score (윈도우 단위)

**시계열 특수 고려사항**
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누설 방지: 미래 정보를 훈련에 사용하지 않도록 워킹-포워드 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
- 멀티 스텝 예측: [Direct](/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) (각 스텝 독립 예측) vs Recursive
- Covariates: 날씨, 공휴일 등 외부 변수 통합

**기술사 출제 포인트**
- "TCN의 팽창 인과 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)이 [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) 대비 갖는 장점을 설명하시오"
- "시계열 예측에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누설([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage)이 발생하는 원인과 방지 방법을 설명하시오"

📢 **섹션 요약 비유**: [시계열 딥러닝](/studynote/10_ai/03_llm_nlp/206_tcn_time_series/)은 과거 패턴에서 미래를 예측하는 타임머신이다. 단, 미래 정보가 훈련에 섞이면 무용지물이 된다.

## Ⅴ. 기대효과 및 결론

TCN과 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 시계열 모델은 전통 통계 방법([ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/), [Exponential Smoothing](/studynote/06_ict_convergence/05_data_science/344_exponential_smoothing_moving_average/))의 한계를 넘어, 복잡한 비선형 패턴과 외부 변수를 통합한 예측이 가능하다. 수요 예측의 5% 개선만으로도 글로벌 공급망에서 수천억 원의 재고 비용을 절감할 수 있다.

📢 **섹션 요약 비유**: [시계열 딥러닝](/studynote/10_ai/03_llm_nlp/206_tcn_time_series/)은 과거 날씨 기록을 학습해 내일 날씨를 예측하는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기상청이다. 더 많은 패턴을 학습할수록 예측이 정확해진다.

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 | TCN (Temporal Convolutional Network) | 팽창 인과 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) |
| 기법 | 팽창 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Dilated [Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)) | 수용 영역 지수 확장 |
| 기법 | 인과 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) (Causal [Convolution](/studynote/10_ai/04_ai_ops_ethics/284_convolution_stride_padding/)) | 미래 누설 방지 |
| 발전 | PatchTST, iTransformer | 장기 예측 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |
| 경쟁 | [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | 순차 처리, [장기 의존성](/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/) |
| 평가 | MAE, MAPE, RMSE | 시계열 예측 지표 |

### 👶 어린이를 위한 3줄 비유 설명
1. TCN은 시간의 흐름을 여러 창문으로 동시에 바라보는 방법이에요 — 창문이 클수록 더 오래전까지 볼 수 있어요.
2. 팽창 [합성곱](/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)은 창문을 레이어마다 2배씩 크게 만들어, 몇 개 층만으로도 수백 단계 과거를 볼 수 있어요.
3. 덕분에 주가, 날씨, 수요 예측을 LSTM보다 훨씬 빠르고 정확하게 할 수 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
통계 모델: ARIMA · SARIMA · Prophet
    |
    v
RNN / LSTM / GRU — 순차적 시계열 처리
    |
    v
TCN (Temporal Convolutional Network)
    +-► 인과적 합성곱 (미래 정보 차단)
    +-► 팽창 합성곱 (Dilated Convolution) — 수용 영역 확장
    +-► 잔차 연결 (Residual Connection)
    |
    v
Transformer 기반 시계열
    +-► Informer (희소 Attention)
    +-► Autoformer (자기상관 분해)
    +-► PatchTST (패치 기반)
    |
    v
Foundation Model for Time Series (TimesFM, Chronos)
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 258

<- **이전**: [156. 추천 시스템 DeepFM (Deep Factorization Machine) 협업 필터링](/studynote/14_data_engineering/03_ml_dl_llm/156_recommendation_system_deepfm_collaborative_filtering/)
**다음**: [158. 멀티모달 (Multimodal) 비전/오디오 동시 인코딩 CLIP](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) ->

---
