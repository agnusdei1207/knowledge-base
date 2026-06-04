---
title: "81. 확률적 경사 하강법 (SGD, Stochastic Gradient Descent)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 학습 시 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 한 번 업데이트하기 위해 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다 계산하는 것(Full Batch)을 포기하고, 통계학적 '샘플링(Stochastic)'에 기반하여 일부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(예: 32개, 64개)만 랜덤하게 뽑아내어 재빨리 오차를 구하고 업데이트를 시도하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 학습 속도를 수백 배 이상 미친 듯이 끌어올리며, 그래픽 카드([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))의 제한된 메모리 용량(VRAM) 안에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 뭉치를 쏙 들어가게 맞춰주어 거대한 딥러닝 모델의 현실적인 학습을 가능케 한 1등 공신이다.
> 3. **판단 포인트**: 일부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 보고 걷기 때문에 방향이 비틀비틀(노이즈 발생) 지그재그로 내려가지만, 오히려 이 요동치는 스텝 덕분에 깊은 함정([Local Minima](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/))에 갇히지 않고 튕겨 나오는 예상치 못한 '탈출 효과'라는 축복을 얻게 되었다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수백만 개로 늘어나자 기존의 완벽한 훈련법은 더 이상 쓸 수 없게 되었다.

1. <strong>배치 <a href="/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/">경사 하강법</a> (Batch <a href="/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/">Gradient Descent</a>, BGD)</strong>:
   - [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 단 한 번 업데이트하기 위해 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 100만 개의 오차를 모두 더하고 평균을 내는 '완벽주의자'다.
   - 100만 번의 연산이 끝나야 비로소 $W$가 아주 살짝 1스텝 움직인다. 한 걸음 내디딜 때마다 지구 전체 인구를 투표시켜야 하니 속도가 절망적으로 느리고, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리에 100만 개 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 다 들어가지도 않아 에러([OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/))가 터진다.
2. **속도의 필요성**:
   - 딥러닝은 보통 수십만 번(Epoch)의 스텝을 밟아야 바닥(정답)에 도달한다. 완벽한 방향으로 1번 걷는 것보다, 조금 삐뚤빼뚤하더라도 1,000번 빠르게 걷는 것이 목적지에는 훨씬 빨리 도착한다는 사실을 깨달았다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 전국 맛집 지도를 완성하기 위해, 한 걸음 내디딜 때마다 전 국민 5천만 명에게 설문조사를 돌리고 그 평균값으로 다음 식당을 고르는 짓(BGD)을 하니 10년이 걸렸습니다. 그래서 이 바보 같은 짓을 멈추고 거리에 보이는 무작위 사람 1명에게만 물어보고 번개처럼 튀어가는 기법이 등장한 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

1개만 뽑으면 너무 비틀거리고, 다 뽑으면 너무 느리다. 황금비율을 찾아야 한다.

1. <strong>순수 <a href="/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>적 <a href="/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/">경사 하강법</a> (Pure SGD)</strong>:
   - 이름 그대로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 **딱 1개만** 랜덤하게 쑥 뽑아서 그 오차만 보고 걷는다.
   - 속도는 총알 같지만 1개의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 하필 '[이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/), 노이즈)'라면 산 밑이 아니라 산꼭대기로 거꾸로 뛰어 올라가는 등 발걸음이 만취한 사람처럼 널을 뛴다.
2. <strong>타협의 미학: 미니배치 <a href="/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/">경사 하강법</a> (Mini-Batch SGD)</strong>:
   - 오늘날 우리가 흔히 'SGD'라고 부르는 것은 사실 이 미니배치 방식을 말한다.
   - 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 100만 개라면, 무작위로 <strong>32개, 64개, 256개(<a href="/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/">Batch Size</a>)</strong> 씩 한 움큼만 바구니에 퍼 담아 이들의 평균 오차를 구하고 한 발짝 걷는다.
   - 이 적당한 바구니 크기(2의 거수제곱)는 엔비디아(NVIDIA) [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리에 한 번에 꽉 차게 쏙 들어가서 칩의 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 코어([CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/))를 100% 효율로 갈구며 엄청난 가속을 끌어낸다.

| 요소 | 역할 |
|:---|:---|
| [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) | 모델이 줄여야 할 오차를 정의하며 학습 방향을 만든다. |
| [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) | 업데이트 폭을 결정해 수렴 속도와 발산 위험을 좌우한다. |
| 일반화 | 훈련 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 아니라 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 품질을 판단하게 만든다. |
| [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 | 대규모 모델에서 학습 속도와 자원 배치를 현실화한다. |

```text
+----------------------------------------------+
| Input -> Transform -> Score -> Apply            |
+----------------------------------------------+
| state -> update    -> monitor -> feedback       |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 전 국민에게 다 물어보기(BGD)는 너무 느리고, 지나가는 아무나 1명에게 물어보기(순수 SGD)는 사기꾼을 만나면 길을 완전히 잃습니다. 그래서 길거리에 모여있는 64명의 군중(Mini-Batch)에게 다수결을 물어보고 빠르게 걷는 타협안이, GPU라는 64인승 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)와 완벽하게 규격이 맞아떨어져 대박을 친 것입니다.

---

## Ⅲ. 비교 및 연결

미니배치 SGD의 덜덜거리는 진동은 치명적 단점이 아니라 신이 내린 축복이었다.

1. **노이즈 (Noise) 수반**:
   - 미니배치마다 표본 집단이 다르기 때문에, [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 내려가는 발걸음이 깔끔한 직선이 아니라 사시나무 떨리듯 지그재그 진동(Fluctuation)을 그리며 내려간다.
2. **안장점(Saddle Point)과 웅덩이 탈출**:
   - 만약 딥러닝이 계곡을 내려가다 작은 웅덩이([Local Minima](/studynote/10_ai/01_ai_basics/083_local_minima_vs_global_minimum/))나 평평한 고원(안장점)에 갇혔다고 치자. 완벽한 BGD는 "기울기가 0이네? 여긴 바닥이야"라며 영원히 멈춰버린다.
   - 하지만 SGD는 이상한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 64개를 뽑았을 때 발생하는 **'순간적인 엉뚱한 방향의 미분값(강력한 노이즈 펀치)'** 때문에, 차가 덜컹거려 구덩이 밖으로 확 튕겨 튕겨 나가게 된다. 이 덕분에 진짜 깊은 바닥(Global Minimum)을 향해 다시 굴러갈 수 있는 극강의 안정성을 확보하게 되었다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) (SGD, [Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: 완벽하게 둥글고 매끄러운 바퀴(BGD)로 산을 내려가면 작은 움푹 파인 웅덩이에 빠졌을 때 매끄러워서 절대 빠져나올 수 없습니다. 하지만 짱돌이 잔뜩 박힌 울퉁불퉁한 찌그러진 바퀴(SGD의 노이즈)로 산을 구르면, 그 덜컹거리는 요동치는 힘(반동) 때문에 얕은 웅덩이 따위는 퉁! 하고 치고 넘어버리는 엄청난 오프로드 탈출 능력을 얻게 된 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) (SGD, [Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))을(를) 단독 기술이 아니라 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질, 시스템 제약, 규제 요구와 함께 판단해야 한다. 언제 채택하고 언제 회피할지, 어떤 지표로 운영 상태를 볼지까지 적어야 기술사 답안으로 완성된다.

- **📢 섹션 요약 비유**: 현장에서 장비를 실제로 켤 때 안전 수칙과 점검표를 함께 보는 운영 절차와 같다.

---

## Ⅴ. 기대효과 및 결론

[확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) (SGD, [Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))은(는) 단일 기술이 아니라 배경·원리·비교·운영 판단이 함께 묶여야 제대로 기억된다. 기대효과는 분명하지만 전제 조건과 한계를 같이 적어야 과장 없는 결론이 된다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우지 않고 언제 쓰고 언제 멈출지까지 적어 둔 사용 설명서와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) | 모델이 줄여야 할 오차를 정의하며 학습 방향을 만든다. |
| [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) | 업데이트 폭을 결정해 수렴 속도와 발산 위험을 좌우한다. |
| 일반화 | 훈련 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 아니라 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 품질을 판단하게 만든다. |
| [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 | 대규모 모델에서 학습 속도와 자원 배치를 현실화한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [확률적 경사 하강법 (SGD, Stochastic Gradient Descent)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 [경사 하강법](/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) (SGD, [Stochastic Gradient Descent](/studynote/14_data_engineering/05_exam_keywords/241_optimizer_sgd_minibatch_adam_momentum_adaptive/))은(는) 복잡해 보여도 일정한 순서와 규칙을 따라 움직여요.
2. 중간 과정을 잘 이해하면 왜 그런 결과가 나오는지 스스로 설명할 수 있어요.
3. 그래서 겉모습보다 흐름과 비교 기준을 함께 기억하는 것이 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 420

<- **이전**: [080. 학습률 (Learning Rate in Gradient Descent)](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)
**다음**: [82. 미니배치 사이즈 (Mini-batch Size) / 에폭 (Epoch) / 이터레이션 (Iteration)](/studynote/10_ai/01_ai_basics/082_mini_batch_size_epoch_iteration/) ->

---
