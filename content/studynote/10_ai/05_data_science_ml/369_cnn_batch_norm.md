+++
title = "369. 배치 정규화 (Batch Normalization) in CNN"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/)([Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/), BN)는 미니배치의 각 특성을 평균 0, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 1로 표준화한 뒤 학습 가능한 스케일(γ)과 이동(β) 파라미터로 재조정하여, 각 층의 입력 분포를 안정화시키는 [정규화 기법](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/)이다.
> 2. **가치**: 내부 공변량 이동(Internal Covariate Shift) 현상을 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)해 더 큰 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 사용을 가능하게 하고, [드롭아웃](/knowledge-base/studynote/10_ai/03_llm_nlp/280_dropout/)([Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)) 없이도 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 효과를 내어 깊은 신경망(Deep Network)의 훈련을 극적으로 가속한다.
> 3. **판단 포인트**: 훈련([Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) 시에는 미니배치의 μ_B, σ²_B를 사용하고, 추론(Inference) 시에는 훈련 중 계산한 이동 평균(Moving Average) μ̄, σ̄²를 사용한다.

---

## Ⅰ. 개요 및 필요성

[심층 신경망](/knowledge-base/studynote/10_ai/01_ai_basics/065_dnn_deep_neural_network/)(Deep Neural Network)에서 각 층의 파라미터가 업데이트될 때마다 이전 층의 출력 분포가 변한다. 이를 내부 공변량 이동([ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/), Internal Covariate Shift)이라 한다. ICS가 심하면 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 작게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 하고 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화에 민감해져 훈련이 느리고 불안정해진다. BN은 각 미니배치에서 활성화(Activation) 이전 또는 이후에 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 수행해 분포를 안정시킨다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: BN이 없는 깊은 신경망은 "전화 게임(끝말잇기)"이다. [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0명이 속삭이면 첫 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지가 왜곡되어 마지막엔 완전히 다른 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지가 된다([ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)). BN은 매 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)명마다 "원본 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 다시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))"하는 체크포인트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────┐
│           배치 정규화 (Batch Normalization) 수식          │
├──────────────────────────────────────────────────────────┤
│  미니배치 B = {x₁, ..., xₘ}                             │
│                                                          │
│  1. 배치 평균:  μ_B = (1/m) Σᵢ xᵢ                     │
│  2. 배치 분산:  σ²_B = (1/m) Σᵢ (xᵢ - μ_B)²          │
│  3. 정규화:     x̂ᵢ = (xᵢ - μ_B) / √(σ²_B + ε)       │
│  4. 스케일·이동: yᵢ = γ · x̂ᵢ + β                     │
│     (γ, β: 학습 가능 파라미터)                          │
│                                                          │
│  추론 시:                                               │
│  μ̄ = EMA(μ_B), σ̄² = EMA(σ²_B) 사용                  │
│  (이동 지수 평균, 훈련 중 누적)                         │
└──────────────────────────────────────────────────────────┘
```

| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 방법 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 축 | 사용 상황 |
|:---|:---|:---|
| Batch Norm (BN) | 배치 × 공간 | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), 대배치 |
| Layer Norm (LN) | 특성 차원 | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/), NLP |
| Instance Norm | 각 샘플 개별 | 스타일 변환 |
| Group Norm | 특성 그룹 | 소배치, 탐지 |

- **📢 섹션 요약 비유**: γ와 β 파라미터는 "표준화 후 원래대로 되돌릴 수 있는 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)"다. 무조건 평균 0, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 1이 최선이 아닐 수 있다. γ와 β가 있으면 네트워크가 "이 층에서는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 2인 분포가 최적"이라는 것을 스스로 학습할 수 있다.

---

## Ⅲ. 비교 및 연결

Layer [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(레이어 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)): 배치 방향이 아닌 특성 차원으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/). 시퀀스 길이가 가변적인 NLP(배치 크기가 작거나 1인 경우)에서 BN은 불안정하지만 LN은 각 샘플 독립적으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하므로 안정적이다. [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 아키텍처는 LN을 기본으로 사용한다. Pre-LN(레이어 전 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))과 Post-LN(레이어 후 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))의 수렴 특성 차이도 중요한 아키텍처 선택이다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/) ([Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/)) in [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: BN vs LN은 "가로 줄 맞추기 vs 세로 줄 맞추기"다. BN은 배치의 같은 특성을 세로(배치 방향)로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하고, LN은 한 샘플의 모든 특성을 가로(특성 방향)로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)한다. CNN은 가로 줄, Transformer는 세로 줄을 선호한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

BN 적용 위치: Conv → BN → [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) 순서가 일반적이나, 최근 연구에서 Conv → [ReLU](/knowledge-base/studynote/10_ai/03_llm_nlp/269_relu_activation/) → BN이 더 나은 경우도 있다. 배치 크기가 너무 작을 때(배치 크기 < 8) BN 통계 추정이 부정확해지므로 Group Norm 또는 Layer Norm으로 대체한다. [전이 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)([Transfer Learning](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))에서 사전 훈련된 모델의 BN 레이어를 고정(freeze)할지 여부가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 큰 영향을 준다.

- **📢 섹션 요약 비유**: 작은 배치에서 BN이 불안정한 것은 "3명을 보고 전 국민 평균 키를 추정"하는 것과 같다. 표본이 너무 작으면 통계가 왜곡된다. Group Norm은 "키를 연령대별로 따로 평균 내는" 접근으로 작은 배치에서도 안정적이다.

---

## Ⅴ. 기대효과 및 결론

BN은 2015년 도입 이후 깊은 신경망 훈련의 표준 도구가 됐다. 더 큰 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 허용, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 민감도 감소, [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) 대체 등으로 훈련 속도와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 개선한다. 현대 모델에서는 Transformer의 Layer Norm, Vision Transformer의 Pre-LN이 주류가 되었으나, [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 아키텍처에서 BN은 여전히 기본값이다.

- **📢 섹션 요약 비유**: BN은 신경망의 "교정기"다. 층을 거칠수록 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 왜곡되는 것을 매 층마다 교정해 신경망이 깊어져도 안정적으로 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 전달한다. 이 교정기 덕분에 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0층 이상의 초깊은 신경망([ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/)-152)이 처음으로 실용화됐다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Layer [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) / BN의 NLP 대안 |
| 내부 공변량 이동 ([ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)) | 분포 불안정 / BN이 해결하는 핵심 문제 |
| Group [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 소배치 / BN 대안 (탐지 모델) |
| [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) / BN으로 부분 대체 가능 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [배치 정규화 (Batch Normalization) in CNN] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/)는 "각 층에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 키를 평균 170cm, 표준편차 10cm로 조정하는 마법"이에요.
2. 이렇게 하면 AI가 각 층을 통과할 때 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 너무 크거나 작아지지 않아요.
3. 덕분에 100층 이상의 아주 깊은 AI도 안정적으로 학습할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 369 / 420

← **이전**: [368. RBF 커널 (Radial Basis Function Kernel)](/knowledge-base/studynote/10_ai/05_data_science_ml/368_rbf_kernel/)
**다음**: [370. BPTT (Backpropagation Through Time)](/knowledge-base/studynote/10_ai/05_data_science_ml/370_bptt/) →

---
