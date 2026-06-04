---
title: "275. 경사 하강법 (GD) / SGD (Stochastic Gradient Descent)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 경사 하강법(GD, [Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))은 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/studynote/12_it_management/02_itsm_itil/087_loss_function/))의 기울기(Gradient) 반대 방향으로 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 반복 갱신해 최솟값을 찾는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, 배치 크기에 따라 Batch GD / SGD / Mini-batch GD 세 가지로 구분된다.
> 2. **가치**: 미니배치 경사 하강법(Mini-batch GD)은 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 SGD([Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))의 속도를 균형 있게 결합해 현대 딥러닝의 사실상 표준 학습 방법이다.
> 3. **판단 포인트**: [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/)(Local Minimum)과 안장점(Saddle Point) 문제는 기술사 시험 단골 주제이며, SGD의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 노이즈가 이 문제를 오히려 완화하는 메커니즘을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

신경망 학습의 목표는 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) L(w)를 최소화하는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 벡터 w를 찾는 것이다. 이를 위해 경사 하강법(GD, [Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))은 다음 갱신 규칙을 반복 적용한다:

```
w <- w - α · ∇L(w)
```

여기서 α는 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate), ∇L(w)은 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)의 기울기(Gradient)다.

그러나 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋으로 기울기를 계산하면 **계산 비용이 매우 크므로**, 배치 크기([Batch Size](/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/))를 달리하는 세 가지 변형이 존재한다.

- **📢 섹션 요약 비유**: 경사 하강법은 눈을 가린 채 산에서 내려오는 것과 같다. 발 밑(기울기)을 느끼며 내리막 방향으로 한 걸음씩 내딛고, 계곡(최솟값)에 도달할 때까지 반복한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 배치 크기에 따른 경사 하강법 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)

```
+----------------------------------------------------------+
|              경사 하강법(GD) 세 가지 변형                 |
+--------------+-------------------+-----------------------+
|  Batch GD    |  SGD              |  Mini-batch GD        |
|              |  (Stochastic GD)  |                       |
+--------------+-------------------+-----------------------+
| 전체 N개     | 1개 샘플로        | k개(32~512)로         |
| 데이터로     | 매 스텝 갱신      | 매 스텝 갱신          |
| 한 번 갱신   |                   |                       |
+--------------+-------------------+-----------------------+
| 정확한 기울기| 노이즈 많음       | 균형 잡힌 기울기       |
| 느린 갱신    | 빠른 갱신         | GPU 병렬 최적          |
| 메모리 한계  | 지역 최솟값 탈출  | 현대 DL 표준          |
+--------------+-------------------+-----------------------+
```

### 손실 곡면의 문제점

```
손실(Loss)
    |
    |    지역 최솟값        안장점
    |    (Local Min)        (Saddle)
    |      v                  v
높음|  ∩--●--∩         ------●------
    |  |  |  |             / | \
    |  |  |  |            /  |  \
낮음|--+  |  +--      ---    |    ---
    |     v                  |
    |  전역 최솟값            기울기=0
    |  (Global Min)          이지만 최솟값 아님
    +---------------------------------> 가중치
```

### [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) vs 안장점

고차원 공간에서는 <strong><a href="/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/">지역 최솟값</a>보다 안장점(Saddle Point)이 훨씬 더 큰 문제</strong>다. 모든 방향에서 기울기가 0이지만 일부 방향은 상승, 일부 방향은 하강하는 지점이다.

| 구분 | 특징 | SGD의 대응 |
|:---|:---|:---|
| [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) (Local Minimum) | 주변보다 낮지만 전역 최솟값 아님 | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 노이즈로 탈출 가능 |
| 안장점 (Saddle Point) | 기울기=0이지만 최솟값 아님 | 다차원 노이즈로 어느 방향으로든 이동 |
| 편평한 고원 (Plateau) | 기울기 거의 0인 넓은 영역 | 느리지만 결국 탈출 |
| 전역 최솟값 (Global Minimum) | 가장 낮은 손실값 | 수렴 목표 지점 |

### SGD의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 노이즈 효과

SGD([Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))는 1개 또는 미니배치 샘플의 기울기로 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 갱신하므로 <strong>매 스텝 기울기에 노이즈(Noise)가 포함</strong>된다. 이 노이즈가 오히려:
- [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) 탈출 가능
- 안장점에서 벗어나는 힘 제공
- 더 <strong>평탄한(Flat) 최솟값</strong>에 수렴 -> 일반화 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상

- **📢 섹션 요약 비유**: SGD의 노이즈는 미끄럼틀 탈 때 엉덩이가 좌우로 흔들리는 것과 같다. 항상 직선으로만 내려오면 함정([지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/))에 빠지지만, 흔들림 덕분에 함정을 넘어 진짜 아래로 내려올 수 있다.

---

## Ⅲ. 비교 및 연결

### 에포크(Epoch) vs 이터레이션(Iteration) vs 배치(Batch)

- **에포크(Epoch)**: 전체 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 번 모두 학습한 횟수
- **이터레이션(Iteration)**: 한 번의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 갱신 = 미니배치 1개 처리
- **배치(Batch)**: 한 번의 이터레이션에 사용되는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 묶음

예) 총 1,000개 샘플, 배치 크기 100이면:
- 1 에포크 = [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이터레이션

### 경사 하강법과 [역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/)([Backpropagation](/studynote/10_ai/03_llm_nlp/272_backpropagation/))의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

[역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/)([Backpropagation](/studynote/10_ai/03_llm_nlp/272_backpropagation/))는 기울기를 <strong>효율적으로 계산</strong>하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이고, 경사 하강법은 그 기울기를 <strong>어떻게 활용해 <a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a>를 갱신할지</strong> 결정하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 두 개념은 항상 함께 동작한다.

```
순전파(Forward Pass)  ->  손실 계산(Loss)  ->  역전파(Backward Pass)  ->  경사 하강법(GD)으로 갱신
```

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| 경사 하강법 (GD) / SGD ([Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: [역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/)가 지도(기울기)를 그리는 역할이라면, 경사 하강법은 그 지도를 보고 실제로 걸음을 내딛는 역할이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 판단 포인트

1. **배치 크기 선택의 트레이드오프**: 배치가 클수록 메모리 필요량^, [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 효율^, 일반화 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)v
2. **SGD의 노이즈 효과**: 노이즈가 [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/)과 안장점 탈출에 기여한다는 점
3. <strong>미니배치 크기 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리에 맞게 32, 64, 128, 256 중 선택. 2의 거듭제곱 권장
4. **에포크 수 결정**: [조기 종료](/studynote/10_ai/03_llm_nlp/281_early_stopping/)([Early Stopping](/studynote/10_ai/03_llm_nlp/281_early_stopping/))와 연계해 과적합 방지

### 실무 시나리오

- <strong>이미지 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> (ImageNet)</strong>: 배치 크기 256, SGD with [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/), 90 에포크 학습
- <strong>자연어 처리 (<a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a> <a href="/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/">Fine-tuning</a>)</strong>: 배치 크기 32, [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/), 3~5 에포크
- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/">강화 학습</a></strong>: 배치 크기 32~256, 경험 재현([Experience Replay](/studynote/10_ai/02_dl_architecture_new/169_experience_replay/)) 버퍼에서 미니배치 샘플링

### 그래디언트 소실/폭발 문제

- **그래디언트 소실(Gradient Vanishing)**: [역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/) 시 기울기가 0에 수렴 -> [ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/), [배치 정규화](/studynote/10_ai/03_llm_nlp/282_batch_normalization/)로 완화
- **그래디언트 폭발(Gradient Explosion)**: 기울기가 기하급수적으로 커짐 -> 그래디언트 클리핑(Gradient [Clipping](/studynote/06_ict_convergence/05_data_science/389_ppo_proximal_policy_optimization/))으로 완화

- **📢 섹션 요약 비유**: 미니배치는 마라톤 대회 운영진이 참가자를 한꺼번에 출발시키지 않고 100명씩 나눠 보내는 것과 같다. 한 번에 너무 많이 보내면 혼잡하고(메모리 초과), 한 명씩 보내면 느리다(SGD). 100명씩이 가장 효율적이다.

---

## Ⅴ. 기대효과 및 결론

미니배치 SGD는 다음 이점을 제공한다:

1. **계산 효율성**: GPU의 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산을 최대한 활용
2. **메모리 효율성**: 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메모리에 올리지 않아도 됨
3. **수렴 안정성**: 노이즈로 인한 국부 최적해 탈출 능력
4. <strong>일반화 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: 배치 GD보다 좋은 일반화 경향

현대 딥러닝에서 미니배치 SGD(Mini-batch SGD)는 [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) 등 고급 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 기반이 되며, <strong>배치 크기 32~512가 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 최적화의 실용적 선택</strong>이다.

- **📢 섹션 요약 비유**: 경사 하강법은 학생이 수능 공부를 할 때 매일 조금씩 약점을 고쳐나가는 것과 같다. 전체 문제집을 한 번에 다 풀고 고치면 시간이 너무 걸리고(Batch GD), 문제 하나씩 보면 흐름을 놓치기 쉽다(SGD). 챕터 단위(미니배치)로 나눠 공부하는 게 가장 효율적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 경사 하강법 (GD) | [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/), 기울기, [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 갱신 / 신경망 학습의 핵심 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| SGD (Stochastic GD) | 1개 샘플, 노이즈, 빠른 갱신 / Batch GD의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 근사 |
| 미니배치 (Mini-batch) | 배치 크기, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 / SGD와 Batch GD의 균형 |
| [지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/) (Local Minimum) | 안장점, Plateau / SGD 노이즈로 탈출 가능 |
| 안장점 (Saddle Point) | 기울기=0, 고차원 / 딥러닝의 주요 최적화 도전 |
| [역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/) ([Backpropagation](/studynote/10_ai/03_llm_nlp/272_backpropagation/)) | 기울기 계산, 체인 룰 / GD에 공급할 기울기 계산 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [경사 하강법 (GD) / SGD (Stochastic Gradient Descent)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 경사 하강법은 눈을 가린 채 언덕에서 내려오는 것처럼, 발밑이 어느 쪽으로 기울어졌는지 느끼며 조금씩 내려오는 방법이에요.
2. 전체 땅을 다 살펴보고 한 걸음 딛는 것(Batch GD)보다 조금씩 살펴보며 빠르게 걷는 것(SGD)이 실제로 더 빨리 도착해요.
3. 가끔 흔들리는 게(노이즈) 오히려 함정([지역 최솟값](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/))을 피하게 해줘서, 완벽하지 않아도 더 좋은 결과를 낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 275 / 420

<- **이전**: [274. 옵티마이저 (Optimizer)](/studynote/10_ai/03_llm_nlp/274_optimizer_learning_rate/)
**다음**: [276. 모멘텀 (Momentum)](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) ->

---
