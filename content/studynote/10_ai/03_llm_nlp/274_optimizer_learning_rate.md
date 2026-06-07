---
title: "Optimizer"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 274
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/studynote/12_it_management/02_itsm_itil/087_loss_function/))를 최소화하기 위해 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)([Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 갱신하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate, α)은 한 번에 얼마나 이동할지 결정하는 핵심 하이퍼파라미터다.
> 2. **가치**: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 너무 크면 손실이 발산(Diverge)하고, 너무 작으면 수렴이 느려지므로 적절한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)과 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링이 학습 품질을 좌우한다.
> 3. **판단 포인트**: SGD -> [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) -> RMSProp -> [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 순으로 발전했으며, 기술사 시험에서는 각 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 구분과 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 역할을 묻는 문제가 출제된다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 학습은 결국 <strong><a href="/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/">손실 함수</a>(<a href="/studynote/12_it_management/02_itsm_itil/087_loss_function/">Loss Function</a>)를 최소화하는 <a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a>를 찾는 최적화 문제</strong>다. [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 이 최적화를 수행하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/)([Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))을 기반으로 동작한다.

[학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate, α)은 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 가장 핵심적인 하이퍼파라미터다.

- **α 너무 큼** -> [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)의 곡면을 과도하게 건너뛰어 발산(Divergence)
- **α 너무 작음** -> 극소값(Minimum)으로 수렴하는 속도가 극히 느림
- **α 적절** -> 안정적이고 빠른 수렴

딥러닝 모델은 수백만 개의 파라미터를 가지므로, 모든 파라미터에 동일한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 적용하는 것은 비효율적이다. 이를 해결하기 위해 <strong>적응형 <a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a>(<a href="/studynote/07_enterprise_systems/02_erp_systems/137_edutech_adaptive_learning_lms/">Adaptive Learning</a> Rate)</strong> 개념이 등장했다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 산에서 내려갈 때 한 걸음의 보폭이다. 보폭이 너무 크면 건너편 산으로 튀어오르고, 보폭이 너무 작으면 평생 내려가도 산 중턱을 못 벗어난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)과 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

```
손실(Loss)
    |
    |  <- α 너무 큼: 발산
    |        ↗↘↗↘
높음|       /    \
    |      /      \   <- α 적절: 수렴
    |     /        ↘↗↘↗-> 최솟값
    |    /                  ●
낮음|___/____________________
    +-----------------------> 가중치(Weight)
```

### [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 발전 계보

```
+-----------------------------------------------------+
|             옵티마이저(Optimizer) 계보                |
+--------------+--------------+-----------------------+
|  SGD         |  Momentum    |  Adam                 |
|  기본 경사   |  관성 추가   |  Momentum +           |
|  하강법      |  지역 최솟값 |  RMSProp 결합         |
|              |  탈출 가능   |  적응형 학습률         |
+--------------+--------------+-----------------------+
         v               v               v
+--------------+  +-------------+  +------------------+
|  w = w - α∇L |  | v = βv-α∇L  |  | m̂, v̂ 보정 후 갱신|
|              |  | w = w + v   |  |                  |
+--------------+  +-------------+  +------------------+
```

### [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 종류 비교

| [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) | 핵심 아이디어 | [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 적응 | 장점 | 단점 |
|:---|:---|:---:|:---|:---|
| SGD | 기울기만 사용 | ✗ | 단순, 일반화 우수 | 느린 수렴, 진동 |
| [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | 속도 벡터 누적 | ✗ | [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) 탈출 | 하이퍼파라미터 추가 |
| RMSProp | 기울기 제곱 평균 | ✓ | 비정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 강건 | 전역 최솟값 보장 없음 |
| [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) | [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)+RMSProp | ✓ | 빠른 수렴, 범용성 | 일반화 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 가능 |
| AdamW | [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/)+[Weight Decay](/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/) | ✓ | 규제 효과 개선 | 추가 하이퍼파라미터 |

### [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) ([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate Scheduler)

[학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 학습 도중 동적으로 조절하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/):

1. **스텝 감소(Step Decay)**: 일정 에포크마다 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 γ 배로 감소
2. <strong><a href="/studynote/10_ai/05_data_science_ml/407_cosine_annealing/">코사인 어닐링</a>(<a href="/studynote/06_ict_convergence/04_ai_llm/309_cosine_annealing/">Cosine Annealing</a>)</strong>: 코사인 함수 모양으로 부드럽게 감소
3. **워밍업(Warmup)**: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 낮게 시작해 점진적으로 증가 후 감소
4. <strong>사이클릭 <a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a>(Cyclical <a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a> Rate, <a href="/studynote/05_database/04_transactions_concurrency/245_clr_compensation_log_record_undo_recovery/">CLR</a>)</strong>: 주기적으로 증감 반복

- **📢 섹션 요약 비유**: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 마라톤 페이스 조절 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 처음엔 워밍업으로 천천히, 중반엔 전력질주, 마지막엔 [코사인 어닐링](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/)처럼 부드럽게 속도를 줄여 결승선에 정확히 도착한다.

---

## Ⅲ. 비교 및 연결

### [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) vs 배치 크기

[학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)과 배치 크기([Batch Size](/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/))는 상호 연관된다. <strong>배치 크기를 k배 늘리면 <a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a>도 √k배 또는 k배 늘려야</strong> 동일한 수렴 특성을 유지한다는 선형 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 규칙이 있다.

### 하이퍼파라미터 탐색

[학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 스케일(Log Scale)</strong> 로 탐색하는 것이 일반적이다.
- 예: 0.0001, 0.001, 0.01, 0.1, 1.0

<strong><a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a> 범위 테스트(<a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a> Rate Range Test, LR Range Test)</strong>: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 점진적으로 증가시키면서 손실이 최소인 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 범위를 찾는 방법.

### 연결 개념
- <strong><a href="/studynote/10_ai/03_llm_nlp/282_batch_normalization/">배치 정규화</a>(<a href="/studynote/10_ai/03_llm_nlp/282_batch_normalization/">Batch Normalization</a>)</strong>: 활성화 값을 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)해 더 높은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 사용 가능
- <strong>그래디언트 클리핑(Gradient <a href="/studynote/06_ict_convergence/05_data_science/389_ppo_proximal_policy_optimization/">Clipping</a>)</strong>: [기울기 폭발](/studynote/10_ai/01_ai_basics/089_exploding_gradient_clipping/)(Gradient Explosion) 방지로 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 안정화
- <strong><a href="/studynote/10_ai/01_ai_basics/087_weight_initialization_xavier_he_glorot/">가중치 초기화</a>(<a href="/studynote/10_ai/01_ai_basics/087_weight_initialization_xavier_he_glorot/">Weight Initialization</a>)</strong>: 적절한 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화로 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)의 효과 극대화

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) ([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)과 배치 크기는 자동차의 엑셀과 기어 같다. 고속 기어(큰 배치)를 쓰면 엑셀도 더 세게(높은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)) 밟아야 같은 가속을 낼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 판단 포인트

1. <strong><a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a> 발산 진단</strong>: 학습 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에서 손실(Loss)이 진동하거나 NaN이 되면 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 감소
2. **워밍업 필요 시점**: 배치 크기가 매우 크거나 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 계열 모델 학습 시 필수
3. <strong><a href="/studynote/10_ai/05_data_science_ml/407_cosine_annealing/">코사인 어닐링</a> 적용</strong>: 장시간 학습이 필요한 대형 모델에서 안정적 수렴을 위해 적용
4. <strong><a href="/studynote/10_ai/03_llm_nlp/277_adam_optimizer/">Adam</a> vs SGD 선택</strong>: 빠른 프로토타이핑에는 [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/), 최종 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화에는 SGD+[Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 고려

### 실무 시나리오

- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a> 사전 학습</strong>: 워밍업 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000 스텝 후 선형 감소 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 사용, [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 1e-4
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/">ResNet</a> 이미지 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>: SGD with [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)(β=0.9), [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 0.1에서 시작해 30/60/90 에포크에서 0.1배 감소
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a> <a href="/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/">미세 조정</a>(<a href="/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/">Fine-tuning</a>)</strong>: AdamW, [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 5e-5, [코사인 어닐링](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/) 적용

- **📢 섹션 요약 비유**: 기술사 관점에서 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 선택은 요리사가 불 세기를 조절하는 것과 같다. 처음엔 약불로 재료를 익히고(워밍업), 중불에서 충분히 조리하며(안정 학습), 마지막엔 약불로 마무리해야(어닐링) 최고의 요리가 완성된다.

---

## Ⅴ. 기대효과 및 결론

적절한 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)와 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 선택하면:

1. **수렴 속도 향상**: [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 계열 사용 시 SGD 대비 수렴 속도 3-10배 빠름
2. **최적해 품질 개선**: [코사인 어닐링](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/)으로 [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) 탈출 및 더 나은 일반화
3. **학습 안정성**: 워밍업으로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 불안정한 그래디언트 문제 완화
4. **하이퍼파라미터 민감도 감소**: 적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 사용 시 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 민감도 대폭 감소

현대 딥러닝에서 <strong><a href="/studynote/10_ai/03_llm_nlp/277_adam_optimizer/">Adam</a> 또는 AdamW가 기본 <a href="/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/">옵티마이저</a></strong>로 사용되며, 최고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해선 SGD with [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) + [코사인 어닐링](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/) 조합이 여전히 경쟁력 있다.

- **📢 섹션 요약 비유**: 좋은 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)와 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 GPS 내비게이션과 같다. 목적지(최솟값)로 가는 최적 경로를 계산하고, 교통 상황(그래디언트 변화)에 맞게 경로를 실시간 조정해 가장 빠르고 안전하게 도착하게 해준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) ([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | SGD, [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/), RMSProp / [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 갱신 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) ([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate, α) | 하이퍼파라미터, 발산, 수렴 / 갱신 보폭 결정 |
| [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | [코사인 어닐링](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/), 워밍업 / 학습 중 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 동적 조절 |
| [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) ([GD](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/)) | [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/), 기울기 / [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 기반 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [모멘텀](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) ([Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)) | 속도 벡터, 관성 / SGD의 진동 완화 |
| 적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) | AdaGrad, RMSProp, [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) / 파라미터별 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 자동 조절 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [옵티마이저 (Optimizer)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 산 정상(손실 최댓값)에서 계곡(최솟값)으로 내려가는 등산가예요.
2. [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 한 걸음의 크기인데, 너무 크게 걸으면 반대 산으로 튀어오르고 너무 작으면 평생 내려가도 계곡에 못 닿아요.
3. [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 처음엔 조심조심 발 디디다가 익숙해지면 빠르게, 계곡 가까이선 다시 천천히 걷도록 안내하는 지도예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 274 / 420

<- **이전**: [273. MSE / 크로스 엔트로피 (Cross-Entropy) 손실 함수](/studynote/10_ai/03_llm_nlp/273_mse_cross_entropy_loss/)
**다음**: [275. 경사 하강법 (GD) / SGD (Stochastic Gradient Descent)](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) ->

---
