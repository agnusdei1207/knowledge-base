+++
title = "277. Adam (Adaptive Moment Estimation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Adam(Adaptive Moment Estimation)은 1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)(기울기 지수 이동 평균, [Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))과 2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)(기울기 제곱 지수 이동 평균, RMSProp)을 결합하고 편향 보정([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) Correction)을 추가해 빠르고 안정적인 학습을 실현하는 적응형 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)다.
> 2. **가치**: 파라미터별 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 자동 조정하므로 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 하이퍼파라미터에 덜 민감하고, 희소 기울기(Sparse Gradient)가 많은 자연어 처리(NLP)나 비전 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에서 우수한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보인다.
> 3. **판단 포인트**: 기술사 시험에서 Adam 수식(m_t, v_t, 편향 보정, β1=0.9/β2=0.999/ε=1e-8)과 AdamW([Weight Decay](/knowledge-base/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/) 분리)의 차이, 그리고 Adam의 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계를 묻는 문제가 출제된다.

---

## Ⅰ. 개요 및 필요성

기존 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 한계:
- **SGD**: 단순하지만 느리고, [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에 매우 민감
- **[Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)**: 수렴 방향 가속, 그러나 모든 파라미터에 동일한 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)
- **AdaGrad(Adaptive Gradient)**: 파라미터별 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 조정, 그러나 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 단조 감소해 결국 0에 수렴
- **RMSProp**: AdaGrad의 단조 감소 문제 해결(지수 이동 평균), 그러나 관성 없음

Adam(Adaptive Moment Estimation)은 **Momentum의 관성 효과 + RMSProp의 적응형 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)**을 결합하여 두 장점을 모두 취한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Adam은 슈퍼 내비게이션이다. 이전에 자주 다닌 방향(1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))을 기억하고, 최근 도로 상황(2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))에 맞게 속도를 자동 조절하며, 처음 출발할 때의 부정확한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(편향 보정)도 스스로 교정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Adam [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 수식

```
1단계: 1차 모멘텀 (기울기 지수 이동 평균)
   m_t = β1 · m_{t-1} + (1 - β1) · ∇L(w_t)

2단계: 2차 모멘텀 (기울기 제곱 지수 이동 평균)
   v_t = β2 · v_{t-1} + (1 - β2) · (∇L(w_t))²

3단계: 편향 보정 (Bias Correction)
   m̂_t = m_t / (1 - β1^t)
   v̂_t = v_t / (1 - β2^t)

4단계: 가중치 갱신
   w_{t+1} = w_t - α · m̂_t / (√v̂_t + ε)
```

### 하이퍼파라미터 기본값

| 파라미터 | 기본값 | 역할 |
|:---|:---:|:---|
| α ([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)) | 0.001 | 전체적인 갱신 보폭 |
| β1 (1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 계수) | 0.9 | 기울기 방향 관성 ([10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 스텝 기억) |
| β2 (2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 계수) | 0.999 | 기울기 크기 평활화 (1000 스텝 기억) |
| ε (수치 안정성) | 1e-8 | 분모가 0이 되는 것 방지 |

### Adam 내부 동작 흐름

```
┌───────────────────────────────────────────────────────┐
│                  Adam 알고리즘 흐름                    │
│                                                       │
│  기울기 ∇L(w)                                         │
│      │                                                │
│      ├──→ [1차 모멘텀] m_t = β1·m + (1-β1)·∇L       │
│      │         → 기울기 방향의 이동 평균 (관성)        │
│      │                                                │
│      └──→ [2차 모멘텀] v_t = β2·v + (1-β2)·(∇L)²    │
│                → 기울기 크기의 이동 평균 (RMSProp)     │
│                                                       │
│  편향 보정: m̂ = m/(1-β1^t), v̂ = v/(1-β2^t)         │
│       ↓                                               │
│  가중치 갱신: w = w - α · m̂ / (√v̂ + ε)             │
│                                                       │
│  효과: 자주 등장하는 파라미터 → 작은 학습률          │
│        드물게 등장하는 파라미터 → 큰 학습률           │
└───────────────────────────────────────────────────────┘
```

### 편향 보정([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) Correction)의 필요성

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시점(t가 작을 때) m_0 = 0, v_0 = 0으로 시작하므로, **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 추정값이 0 방향으로 편향**된다. 편향 보정은 이를 실제 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)에 가깝게 [스케일 업](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)하는 과정이다.

```
t=1: β1=0.9 → (1-β1^1) = 0.1 → m̂ = m/0.1 = 10배 확대
t=10: (1-β1^10) ≈ 0.65 → 점점 보정 감소
t→∞: (1-β1^∞) → 1.0 → 보정 불필요
```

- **📢 섹션 요약 비유**: 편향 보정은 새벽에 체온계가 실온 온도에 맞춰져 있을 때 보정하는 것과 같다. 막 시작했을 때는 체온계([모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))가 실제보다 낮게 표시되므로, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)엔 값을 올려서 읽고 시간이 지나면 자연스럽게 정확해진다.

---

## Ⅲ. 비교 및 연결

### [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 계보 비교

| [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) | 1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | 2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | 편향 보정 | 특징 |
|:---|:---:|:---:|:---:|:---|
| SGD | ✗ | ✗ | ✗ | 기본, 일반화 우수 |
| [Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | ✓ | ✗ | ✗ | 관성, [지역 최솟값](/knowledge-base/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) 탈출 |
| AdaGrad | ✗ | 누적합 | ✗ | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 단조 감소 (희소 특성 우수) |
| RMSProp | ✗ | ✓ (지수) | ✗ | AdaGrad의 감소 문제 해결 |
| Adam | ✓ | ✓ (지수) | ✓ | 현대 표준 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) |
| AdamW | ✓ | ✓ (지수) | ✓ | Adam + [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠 분리 |

### AdamW와의 차이

Adam의 L2 규제는 **기울기에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 항을 더하는 방식**이지만, 이는 적응형 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)과 상호작용해 규제 효과가 약해진다.

**AdamW(Adam with [Weight Decay](/knowledge-base/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/))**는 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠([Weight Decay](/knowledge-base/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/))를 그래디언트가 아닌 **[가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 갱신 단계에서 직접 적용**한다:

```
Adam:   w = w - α · m̂/(√v̂+ε) - α · λ · w   (불완전한 L2)
AdamW:  w = w · (1 - α·λ) - α · m̂/(√v̂+ε)   (올바른 Weight Decay)
```

- **📢 섹션 요약 비유**: Adam과 AdamW의 차이는 다이어트할 때 매일 식사량 줄이기(Adam의 L2)와 매일 몸무게 일정 비율 빼기(AdamW)의 차이다. 두 번째 방법이 더 직접적이고 일관된 규제 효과를 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Adam의 한계와 대응

1. **일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제**: Adam은 SGD보다 훈련 손실은 빠르게 줄지만, 테스트 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(일반화)이 낮을 수 있음
   - 원인: 적응형 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 일부 파라미터에 과도하게 큰 업데이트를 허용
   - 대응: 학습 후반에 SGD로 전환하는 SWATS 기법, 또는 AdamW 사용

2. **메모리 사용량**: m, v 두 변수를 추가로 저장 → SGD 대비 약 2배 메모리 소비

3. **수렴 보장 없음**: 특정 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)에서 수렴하지 않는 이론적 사례 존재

### 기술사 시험 판단 포인트

- β1=0.9: 기울기 1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (약 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 스텝의 평균 방향)
- β2=0.999: 기울기 2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (약 1000 스텝의 평균 크기)
- ε=1e-8: 수치 안정성 (분모 0 방지)
- AdamW가 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 학습에 사실상 표준임을 언급

### 실무 활용

- **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 사전 학습**: AdamW + 워밍업 + 선형/코사인 감소 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)
- **[ResNet](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) 이미지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)**: SGD with [Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)), Adam (빠른 실험)
- **[GAN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/) 학습**: Adam(β1=0.5, β2=0.999) – 학습 안정화를 위해 β1을 낮춤

- **📢 섹션 요약 비유**: Adam은 모든 선수가 자신의 체력(파라미터)에 맞는 페이스([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/))로 달리게 해주는 스마트 코치다. 지칠 것 같은 선수(자주 갱신되는 파라미터)는 천천히, 여유 있는 선수(드물게 갱신되는 파라미터)는 빠르게 달리게 조율한다.

---

## Ⅴ. 기대효과 및 결론

Adam이 딥러닝 표준 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)로 자리잡은 이유:

1. **빠른 수렴**: 대부분의 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에서 SGD 대비 빠른 수렴
2. **[학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 민감도 감소**: α=0.001 기본값이 대부분의 문제에서 잘 작동
3. **희소 기울기 처리**: NLP의 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 레이어처럼 드물게 갱신되는 파라미터에 큰 업데이트 적용
4. **범용성**: 비전, 언어, 음성 등 다양한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 일관된 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)

그러나 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 필요할 때는 SGD+Momentum이, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 학습에는 AdamW가 권장된다.

- **📢 섹션 요약 비유**: Adam은 자동 변속기 자동차다. 누구나 운전([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))을 쉽게 할 수 있고 대부분 상황에서 잘 달린다. 하지만 레이싱(최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))에서는 수동 변속기(SGD+[Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 수동 조절)가 더 빠를 수도 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Adam | Adaptive Moment Estimation, β1, β2 / 1차+2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 결합 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) |
| 1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (m_t) | [Momentum](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/), 기울기 방향 평균 / 수렴 방향 관성 제공 |
| 2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (v_t) | RMSProp, 기울기 제곱 평균 / 파라미터별 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 조정 |
| 편향 보정 ([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) Correction) | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화, 0 편향 / [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 불안정 추정 보정 |
| AdaGrad | 누적 기울기 제곱, 희소 기울기 / Adam의 전신 ([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 단조 감소 문제) |
| RMSProp | 지수 이동 평균, 비정상 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) / Adam의 2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) 원형 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [Adam (Adaptive Moment Estimation)] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Adam은 두 가지를 동시에 기억하는 아주 똑똑한 로봇이에요. 어느 방향으로 가야 하는지(1차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))와 얼마나 빠르게 가야 하는지(2차 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))를 따로 기억해요.
2. 처음엔 기억이 아직 불완전하니까 편향 보정으로 스스로 오차를 고쳐가면서 더 정확하게 움직여요.
3. 덕분에 대부분의 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 학습에서 "일단 Adam 쓰면 대충 잘 된다"는 게 실무의 표준이 됐어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 277 / 420

← **이전**: [276. 모멘텀 (Momentum)](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)
**다음**: [278. 과적합 방지 기법 (Regularization Techniques) 모음](/knowledge-base/studynote/10_ai/03_llm_nlp/278_regularization_overview/) →

---
