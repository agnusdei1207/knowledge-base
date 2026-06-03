+++
title = "278. 과적합 방지 기법 (Regularization Techniques) 모음"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 규제([Regularization](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/))는 모델이 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 과도하게 맞춰지는 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/))을 방지하고, 새로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(테스트 셋)에서도 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하는 일반화(Generalization) 능력을 키우기 위한 기법 모음이다.
> 2. **가치**: L1/L2 페널티, [드롭아웃](/knowledge-base/studynote/10_ai/03_llm_nlp/280_dropout/)([Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)), [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/)([Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/)), [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증강([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Augmentation)은 각각 다른 메커니즘으로 과적합을 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)하므로, 문제 유형에 따라 조합해 사용한다.
> 3. **판단 포인트**: 기술사 시험에서 각 규제 기법의 원리·적용 시나리오·상호 보완 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 묻는 비교 문제가 자주 출제된다.

---

## Ⅰ. 개요 및 필요성

### 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/))과 과소적합([Underfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/246_underfitting_bias/))

- <strong>과적합(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/">Overfitting</a>)</strong>: 훈련 오차 ↓, 테스트 오차 ↑ → 모델이 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 노이즈까지 암기
- <strong>과소적합(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/246_underfitting_bias/">Underfitting</a>)</strong>: 훈련 오차 ↑, 테스트 오차 ↑ → 모델 복잡도 부족
- **적절한 fitting**: 훈련/테스트 오차 모두 낮음 → 일반화 [성능 우수](/knowledge-base/studynote/05_database/07_exam_summary/484_elt_extract_load_transform/)

규제 기법은 <strong>과적합을 방지하기 위한 다양한 접근법</strong>이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 모델 구조, [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/), 학습 과정 각 단계에서 개입할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Background Problem → Need → Adoption Value</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Existing limitation</div><div class="kb-diagram-cell">Operational pressure</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">New requirement</div><div class="kb-diagram-cell">Design decision point</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 과적합 방지는 학생이 기출문제만 달달 외워서 시험을 통과하려는 것을 막고, 개념을 진짜로 이해하도록 유도하는 교육 방법이다. 규제가 없으면 AI도 답을 외우고, 규제가 있으면 진짜 패턴을 학습한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 규제 기법 전체 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">규제(Regularization) 기법 분류</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">손실 함수 기반</div><div class="kb-diagram-cell">L1 규제 (Lasso) : λΣ</div><div class="kb-diagram-cell">w</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L2 규제 (Ridge) : λΣw²</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Elastic Net : L1 + L2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구조/학습 기반</div><div class="kb-diagram-cell">Dropout : 뉴런 무작위 비활성화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Early Stopping : 검증 손실 기반 중단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Batch Norm : 활성화 분포 정규화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Max-Norm : 가중치 노름 제한</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 기반</div><div class="kb-diagram-cell">Data Aug. : 훈련 데이터 증강</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Mixup/CutMix : 샘플 혼합</div></div>
</div>
</div>



### 규제 기법 비교표

| 기법 | 원리 | 장점 | 단점 | 주 사용처 |
|:---|:---|:---|:---|:---|
| L1 규제 ([Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/)) | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 절댓값 페널티 | 희소 모델, 특성 선택 | 미분 불연속 | 특성 선택이 필요한 경우 |
| L2 규제 (Ridge) | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 제곱 페널티 | 부드러운 수렴 | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 0으로 만들지 않음 | 대부분의 딥러닝 |
| [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) | 뉴런 무작위 비활성화 | [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 효과 | 학습 시간 증가 | [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 레이어 |
| [Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 손실 기반 중단 | 구현 단순 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 셋 필요 | 모든 딥러닝 |
| Batch Norm | 활성화 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 학습 가속 | 추론 시 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 | 딥 네트워크 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Augmentation | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 인위 증가 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부족 보완 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 필요 | 이미지/음성 |

### 과적합 발생 진단



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">에포크</div>
<div class="kb-diagram-note">↓ 과적합 시작</div>
<div class="kb-diagram-note">손 │ \ 훈련 손실 (계속 감소)</div>
<div class="kb-diagram-note">실 │ \</div>
<div class="kb-diagram-note">\ 검증 손실 (증가 시작)</div>
<div class="kb-diagram-tree-item" style="--depth:2">→ 에포크</div>
<div class="kb-diagram-note">← 정상 학습 →↑← 과적합 →</div>
</div>
</div>



- **📢 섹션 요약 비유**: 규제 기법들은 학생의 공부 방법 교정 도구들이다. L1/L2는 "중요하지 않은 내용은 잊어버려"이고, Dropout은 "매번 교과서 일부를 가리고 공부해봐"이며, Early Stopping은 "점수가 더 이상 안 오르면 그만해"다.

---

## Ⅲ. 비교 및 연결

### 각 기법의 적용 레이어

- <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/">FC</a> 레이어(Fully Connected Layer)</strong>: [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/), L1/L2 규제
- <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/">CNN</a> 컨볼루션 레이어</strong>: [Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/), Spatial [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)
- <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/">RNN</a>/<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a></strong>: [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/), Layer [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠([Weight Decay](/knowledge-base/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/))
- **훈련 루프**: [Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/), [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)

### 상호 보완 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

- <strong>Batch Norm + <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/">Dropout</a></strong>: BN이 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 어느 정도 수행하므로, 함께 쓰면 [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) 비율 낮춰도 됨
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Augmentation + L2</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 적을 때 두 가지 모두 적용해 일반화 강화
- <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/">Early Stopping</a> + 모델 체크포인트(Checkpoint)</strong>: [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 손실 최솟값 시점의 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 저장

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| 과적합 방지 기법 ([Regularization](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/) Techniques) 모음 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: 규제 기법들은 요리의 양념과 같다. 소금(L2), 후추([Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)), 불 조절([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/))을 각각 따로 써도 되고 조합해서 써도 된다. 너무 많이 쓰면 맛이 없어지고(과소적합), 너무 적게 쓰면 맛이 없어진다(과적합).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 판단 포인트

1. **L1 vs L2**: L1은 희소 해(Sparse Solution), L2는 부드러운 축소
2. <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/">Dropout</a> vs Batch Norm</strong>: 함께 쓸 때 [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) 비율을 줄여야 함
3. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/">Early Stopping</a></strong>: 인내심(Patience) 파라미터와 모델 체크포인트의 역할
4. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Augmentation</strong>: 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부족 시 가장 먼저 적용할 기법

### 규제 강도(λ) 선택 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">λ (정규화 강도) 선택 가이드:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">λ 너무 큼 → 과소적합 (모든 가중치 → 0)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">λ 너무 작음 → 규제 효과 없음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">λ 적절 → 일반화 성능 극대화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐색 범위: 1e-5 ~ 1e-1 (로그 스케일)</div></div>
</div>
</div>



### 최신 규제 기법

- **Mixup**: 두 샘플을 선형 보간해 혼합된 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- **CutMix**: 이미지의 일부를 잘라 다른 이미지에 붙이는 증강
- **Label Smoothing**: 원-핫 레이블을 부드럽게 만들어 과적합 방지
- **Stochastic Depth**: 레이어를 무작위로 skip ([ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) 계열)

- **📢 섹션 요약 비유**: 규제 기법의 세계는 마치 면역 체계와 같다. 하나의 방어선이 뚫리더라도(한 가지 규제 실패) 여러 겹의 방어선(다중 규제 조합)이 과적합이라는 병을 막아준다.

---

## Ⅴ. 기대효과 및 결론

적절한 규제 기법 적용의 효과:

1. <strong>일반화 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 향상</strong>: 테스트 오차 감소, 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 환경에서의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 안정화
2. **모델 경량화**: L1 규제로 불필요한 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 제거 → 추론 속도 향상
3. **학습 안정성**: Batch Norm으로 그래디언트 흐름 안정화
4. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 효율성</strong>: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Augmentation으로 적은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로도 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 달성

현대 딥러닝에서는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Augmentation + Batch Norm + <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/">Dropout</a> + AdamW(L2 내포)</strong> 조합이 컴퓨터 비전 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)의 표준이며, <strong>Layer Norm + <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/">Dropout</a> + Label Smoothing</strong>이 [트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 계열의 표준이다.

- **📢 섹션 요약 비유**: 좋은 규제 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 아이를 키우는 균형 잡힌 교육과 같다. 너무 엄격하면(강한 규제) 창의성이 없어지고, 너무 자유로우면(규제 없음) 나쁜 습관이 생긴다. 다양한 방법을 균형 있게 적용해야 똑똑하고 사회성 있는(일반화 잘 되는) AI가 탄생한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 과적합 ([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) | 훈련 오차↓ [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 오차↑ / 규제 기법이 해결하는 핵심 문제 |
| L1 규제 ([Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/)) | 희소 해, 특성 선택, λΣ / w / [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)에 절댓값 페널티 추가 |
| L2 규제 (Ridge) | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 축소, λΣw² / [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)에 제곱 페널티 추가 |
| [Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) | 뉴런 비활성화, [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) / 학습 시 무작위 뉴런 제거 |
| [Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) | Patience, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 손실 / 훈련 중단 시점 결정 |
| [Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/) | 내부 공변량 이동, γ, β / 활성화 분포 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [과적합 방지 기법 (Regularization Techniques) 모음] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 과적합은 시험 문제를 통째로 외워버린 학생처럼, AI가 정답을 외워서 새 문제는 못 푸는 상태예요.
2. 규제는 "외우지 말고 이해해!"라고 가르치는 방법들의 모음이에요. [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 페널티, 뉴런 끄기, 공부 일찍 멈추기 등 다양한 방법이 있어요.
3. 여러 규제를 함께 쓰면 마치 여러 선생님이 함께 가르치는 것처럼, AI가 훨씬 더 잘 이해하고 일반화할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 278 / 420

← **이전**: [277. Adam (Adaptive Moment Estimation)](/knowledge-base/studynote/10_ai/03_llm_nlp/277_adam_optimizer/)
**다음**: [279. L1/L2 규제 (Regularization)](/knowledge-base/studynote/10_ai/03_llm_nlp/279_l1_l2_regularization/) →

---
