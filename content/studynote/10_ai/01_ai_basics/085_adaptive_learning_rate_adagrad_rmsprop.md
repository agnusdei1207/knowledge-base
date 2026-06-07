---
title: "Adaptive Learning Rate Adagrad Rmsprop"
date: "2026-04-10"
tags:
  - "studynote-ai"
weight: 85
---
## 핵심 인사이트 (3줄 요약)

> **본질**: 적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Adaptive Learning](/studynote/07_enterprise_systems/02_erp_systems/137_edutech_adaptive_learning_lms/) Rate)은 각 파라미터의 과거 그래디언트(Gradient)를 보고 보폭을 다르게 조절하는 최적화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> **가치**: Adagrad (Adaptive Gradient)는 희소 특징에 강하고, RMSProp (Root Mean [Square](/studynote/04_software_engineering/06_software_architecture/341_iso_iec_25010/) Propagation)은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 0에 가까워지는 문제를 완화한다.
> **판단 포인트**: 고정 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이 흔들리면 무작정 [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) ([Adaptive Moment Estimation](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/))으로 가지 말고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 희소성·비정상성·예산을 보고 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

딥러닝 최적화에서는 모든 파라미터가 같은 속도로 배우지 않는다. 어떤 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)는 자주 업데이트되고, 어떤 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)는 거의 업데이트되지 않으므로 고정 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)(Fixed [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate)만으로는 한쪽은 너무 크게, 다른 한쪽은 너무 작게 움직일 수 있다.

적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 이 불균형을 줄이기 위해 등장했다. Adagrad와 RMSProp은 "과거 그래디언트의 흔적을 저장해 현재 보폭을 조절한다"는 공통점이 있지만, 누적 방식이 달라 서로 다른 장단점을 만든다.

- 📢 섹션 요약 비유: 보폭 조절기

---

## Ⅱ. 아키텍처 및 핵심 원리

Adagrad는 그래디언트 제곱을 누적해, 자주 등장한 파라미터의 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 점점 낮춘다. 반면 RMSProp은 누적합 대신 지수이동평균(Exponential Moving Average)을 써서 오래된 정보를 조금씩 잊는다. 그래서 Adagrad는 희소 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에, RMSProp은 비정상(non-stationary) 손실 곡면에 잘 맞는다.

```text
Adagrad:  Gt = Gt-1 + gt^2
          theta = theta - eta / sqrt(Gt + eps) * gt

RMSProp:  vt = rho * vt-1 + (1-rho) * gt^2
          theta = theta - eta / sqrt(vt + eps) * gt
```

| 항목 | Adagrad | RMSProp |
| --- | --- | --- |
| 상태 저장 | 누적 합 | 이동 평균 |
| 장점 | 희소 특징에 강함 | [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 소멸이 덜함 |
| 약점 | 시간이 갈수록 너무 느려질 수 있음 | 감쇠 계수 튜닝이 필요함 |
| 적합 상황 | 단어 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/), 희소 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) | [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) ([Recurrent Neural Network](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/)), 비정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

핵심은 "과거를 얼마나 오래 기억할 것인가"이다. 기억이 길면 안정적이지만 둔해지고, 기억이 짧으면 민감하지만 흔들리기 쉽다.

- 📢 섹션 요약 비유: 기억하는 보폭

---

## Ⅲ. 비교 및 연결

SGD ([Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))는 단순하고 가볍지만 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 사람이 직접 맞춰야 한다. Momentum은 관성을 더해 진동을 줄이고, Adam은 1차 모멘트와 2차 모멘트를 함께 써서 RMSProp 계열의 장점을 확장한다. 그래서 Adagrad와 RMSProp은 Adam의 전단계 개념으로 이해하면 좋다.

| 비교 대상 | 핵심 차이 |
| --- | --- |
| SGD | 한 번 정한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 끝까지 주로 사용 |
| [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | 과거 방향을 누적해 진동 완화 |
| Adagrad | 자주 나온 파라미터의 보폭을 더 빨리 줄임 |
| RMSProp | 오래된 그래디언트를 서서히 잊으며 보폭 유지 |
| [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) | [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) + RMSProp 성격을 결합 |

즉 적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 "더 똑똑한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)"이 아니라, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조에 맞게 반응하는 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)이다.

- 📢 섹션 요약 비유: 비교표

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 희소 특징이 많고 한 번 등장한 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 놓치면 안 되는 경우 Adagrad를 우선 검토한다. 반대로 시계열, [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/), 온라인 학습처럼 분포가 계속 바뀌는 문제에서는 RMSProp이 더 안정적이다. 둘 다 베이스 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/), eps, 감쇠 계수(rho)를 함께 튜닝해야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 손실 곡선이 진동하는가, 아니면 너무 빨리 평평해지는가?
2. [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)가 희소한가, 아니면 분포가 계속 바뀌는가?
3. [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 손실이 아니라 훈련 손실만 보고 있지는 않은가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 모든 문제를 [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 한 가지로 퉁치는 것
- [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 소멸을 보지 않고 Epoch만 늘리는 것
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리와 최적화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 분리해 실험하지 않는 것

- 📢 섹션 요약 비유: 운영 중 조절대

---

## Ⅴ. 기대효과 및 결론

적응형 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)의 장점은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 학습을 빠르게 하고, 파라미터별 스케일 차이를 자동 완화한다는 점이다. 하지만 그만큼 내부 상태가 늘어나므로 메모리와 해석 가능성이 조금 희생된다. 결국 좋은 선택은 "가장 유행하는 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)"가 아니라 "문제의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조에 맞는 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)"다.

결론적으로 Adagrad는 희소성에, RMSProp은 비정상성에 강하다고 기억하면 된다. 그리고 두 방법 모두 "그래디언트를 얼마나 오래 기억할 것인가"라는 하나의 질문으로 묶여 있다.

- 📢 섹션 요약 비유: [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 자동변속기

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| Gradient | 파라미터를 움직이는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| Adagrad | 누적 제곱으로 보폭 감소 |
| RMSProp | 이동 평균으로 보폭 안정화 |
| SGD | 비교 기준이 되는 기본 최적화기 |
| [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) | 관성 추가로 진동 감소 |
| [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) | [Adaptive Learning](/studynote/07_enterprise_systems/02_erp_systems/137_edutech_adaptive_learning_lms/) Rate 계열의 대표 결합형 |

### 📈 관련 키워드 및 발전 흐름도

```text
손실 함수
   v
그래디언트 계산
   v
과거 그래디언트 누적
   v
파라미터별 학습률 조정
   v
가중치 업데이트
   v
다음 반복
```

### 👶 어린이를 위한 3줄 비유 설명

1. Adagrad는 자주 쓰는 페달은 점점 덜 밟고, 드문 페달은 더 세게 밟는 자동차 같아요.
2. RMSProp은 너무 오래된 길은 조금씩 잊고, 지금 길 상태를 더 중요하게 봐요.
3. 그래서 컴퓨터는 문제마다 다른 속도로 배우게 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 420

<- **이전**: [84. 모멘텀 (Momentum) 옵티마이저 - 관성 활용 최적화](/studynote/10_ai/01_ai_basics/084_momentum_optimizer_local_minima_escape/)
**다음**: [86. Adam (Adaptive Moment Estimation) - 최강의 결합 옵티마이저](/studynote/10_ai/01_ai_basics/086_adam_optimizer_momentum_rmsprop/) ->

---
