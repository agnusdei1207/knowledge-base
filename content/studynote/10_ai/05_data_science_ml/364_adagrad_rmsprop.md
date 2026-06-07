---
title: "Adagrad Rmsprop"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 364
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Adagrad(Adaptive Gradient [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))와 RMSProp(Root Mean [Square](/studynote/04_software_engineering/06_software_architecture/341_iso_iec_25010/) Propagation)은 각 파라미터마다 다른 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 적응적으로 조정하는 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)로, 희소(Sparse) 특성이 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 SGD보다 빠른 수렴을 달성한다.
> 2. **가치**: Adagrad는 자주 나타나는 특성은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 줄이고 드문 특성은 크게 유지해 텍스트 모델에 강력하지만, 학습이 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)될수록 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 0에 수렴하는 치명적 소멸 문제가 있고 RMSProp이 이를 지수 이동 평균(EMA)으로 해결한다.
> 3. **판단 포인트**: [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) = RMSProp (2차 모멘트, [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 적응) + [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) (1차 모멘트)의 결합이며, Adam이 실무에서 가장 널리 사용되는 이유가 여기에 있다.

---

## Ⅰ. 개요 및 필요성

기본 SGD([Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))는 모든 파라미터에 동일한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)(η)을 적용한다. 텍스트 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 "the"같은 자주 나오는 단어의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)는 그래디언트가 크므로 큰 업데이트가, "quasar" 같은 드문 단어는 작은 업데이트가 필요하다. Adagrad는 이를 각 파라미터의 과거 그래디언트 제곱 합(G_t)을 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 분모에 넣어 자동으로 조정한다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: Adagrad는 "자주 쓰는 도로는 속도를 줄이고, 처음 가는 샛길은 빠르게" 학습하는 지능형 내비게이션이다. 이미 많이 업데이트된 파라미터(자주 쓴 도로)는 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 줄여 안정화하고, 거의 업데이트 안 된 파라미터(새 샛길)는 빠르게 학습시킨다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------+
|      Adagrad vs RMSProp 수식 비교                        |
+----------------------------------------------------------+
|  Adagrad:                                                |
|  G_t = G_{t-1} + g_t^          (누적 제곱 합)          |
|  θ_t = θ_{t-1} - η/√(G_t+ε) · g_t                     |
|  문제: G_t는 단조 증가 -> η/√(G_t) -> 0 (학습률 소멸!)  |
|                                                          |
|  RMSProp:                                               |
|  E[g^]_t = ρ·E[g^]_{t-1} + (1-ρ)·g_t^  (EMA)         |
|  θ_t = θ_{t-1} - η/√(E[g^]_t+ε) · g_t                |
|  해결: EMA로 최근 그래디언트만 반영 -> 학습률 안정!     |
|                                                          |
|  Adam (결합):                                           |
|  m_t = β₁·m_{t-1} + (1-β₁)·g_t  (1차 모멘트)         |
|  v_t = β₂·v_{t-1} + (1-β₂)·g_t^  (2차 모멘트)        |
|  θ_t = θ_{t-1} - η·m̂_t/√(v̂_t+ε)                    |
+----------------------------------------------------------+
```

| [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) | [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 누적 | 소멸 문제 | 특이 사항 |
|:---|:---|:---|:---|
| SGD | 고정 | ❌ 없음 | 튜닝 어려움 |
| Adagrad | 전체 누적 | ✅ 발생 | 희소 특성에 강함 |
| RMSProp | EMA (지수) | ❌ 없음 | 비정상 시계열에 강함 |
| [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) | EMA + [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | ❌ 없음 | 실무 기본값 |

- **📢 섹션 요약 비유**: Adagrad의 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 소멸은 "계단 내려가는 로봇"이다. 처음엔 큰 걸음(η)으로 빠르게 내려오지만, 걸음 수(G_t)가 쌓일수록 걸음이 점점 작아져 결국 아예 멈춰버린다(학습 정지). RMSProp은 최근 몇 걸음(EMA)만 기억해 항상 적정 속도를 유지한다.

---

## Ⅲ. 비교 및 연결

AMSGrad는 Adam의 과거 최대 2차 모멘트를 유지해 수렴 보장 문제를 해결한다. AdamW는 Adam에 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠([Weight Decay](/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/))를 L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 분리하여 더 정확한 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 구현한다([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 훈련의 표준). Lion(Evolved Sign [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)) [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 Google이 진화 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 발견한 Adam보다 메모리 효율적인 최신 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| Adagrad / RMSProp [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) (Adagrad Rmsprop) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: AdamW는 "다이어트와 운동을 분리하는 체중 관리"다. 기존 Adam의 L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 그래디언트 업데이트와 뒤섞여 효과가 감소했다. AdamW는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠를 별도로 적용해 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 같은 대형 모델의 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 효과를 극대화한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

하이퍼파라미터 기본값([Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/)): η=0.001, β₁=0.9, β₂=0.999, ε=1e-8. Warmup [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/): 학습 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 0에서 천천히 올려 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 학습 불안정성 방지([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 훈련 필수). [Cosine Annealing](/studynote/06_ict_convergence/04_ai_llm/309_cosine_annealing/): [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 코사인 커브로 감소시켜 수렴 말기 섬세한 조정. Cyclic LR: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 주기적으로 올렸다 내렸다 하며 다양한 Loss Landscape 탐색.

- **📢 섹션 요약 비유**: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) Warmup은 "엔진 예열"이다. 차(모델)를 처음 출발시킬 때 갑자기 최고 속도로 달리면(큰 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)) 엔진이 망가진다. 천천히 예열(작은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/))한 뒤 최적 속도로 올리는 것이 Warmup이다.

---

## Ⅴ. 기대효과 및 결론

Adagrad -> RMSProp -> Adam으로 이어지는 적응적 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)의 진화는 딥러닝 최적화의 핵심 발전사다. RMSProp의 EMA 아이디어가 Adam의 2차 모멘트가 되었고, Momentum이 1차 모멘트가 되어 Adam이 완성됐다. 기술사 시험에서 Adagrad 소멸 문제 -> RMSProp EMA 해결 -> [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 수식까지 진화 경로를 설명하면 최고 수준의 답안이다.

- **📢 섹션 요약 비유**: Adagrad->[Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 진화는 "손으로 페달 밟기 -> 자전거 -> 전기자동차"다. 손으로 걷기(SGD)에서 자전거 기어(Adagrad 적응 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)), 자동 기어(RMSProp EMA), 최첨단 전기차([Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) [모멘텀](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)+적응 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)) 순으로 편리하고 효율적으로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) | β₁, β₂모멘트 / RMSProp + Momentum의 결합 |
| AdamW | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 감쇠 분리 / [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 훈련 표준 |
| [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링 | Warmup, Cosine / [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)와 함께 사용 |
| 그래디언트 소실 | 학습 정지 / Adagrad의 핵심 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [Adagrad / RMSProp 옵티마이저 (Adagrad Rmsprop)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Adagrad는 "자주 쓰는 도구는 조금씩, 새 도구는 많이" 업데이트하는 똑똑한 AI예요.
2. 하지만 시간이 지나면 모든 도구를 너무 조금씩 업데이트해서 AI가 성장을 멈추는 문제가 있어요.
3. RMSProp은 이를 고쳐서 "최근에 쓴 것만 기억"하게 해서 AI가 계속 성장할 수 있게 했어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 364 / 420

<- **이전**: [363. 소프트맥스 역전파 (Softmax Backpropagation)](/studynote/10_ai/05_data_science_ml/363_softmax_backprop/)
**다음**: [365. GloVe (Global Vectors for Word Representation)](/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/) ->

---
