+++
title = "23. 머신러닝 개념 (Machine Learning Concept)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(ML, Machine [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))은 인간이 규칙(Rule)을 직접 코딩하는 대신, 대량의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))와 정답(Label)을 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 주입하면 **기계가 스스로 수학적 패턴([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))을 최적화**하며 예측 함수를 완성하는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)의 핵심 하위 분야다. (Tom Mitchell, 1997)
> 2. **가치**: 인간의 두뇌로 모든 변수를 if-else로 코딩하기 불가능한 **복잡계 문제**(스팸 필터·암 진단·주가 예측)를 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)·통계·최적화 이론으로 해결하며, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) 인프라와 빅데이터의 결합으로 딥러닝(Deep [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 혁명을 촉발했다.
> 3. **판단 포인트**: "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 얼마나 있고, 해석 가능성(Explainability)이 얼마나 중요한가?"—[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부족·설명 필요 시 **전통적 ML ([Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/), XGBoost)**, 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최우선 시 **딥러닝**, 레이블 없음 시 **[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))**을 선택한다.

---

## Ⅰ. 개요 및 필요성

[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(ML, Machine [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))은 명시적으로 프로그래밍하지 않아도 경험([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))으로부터 자동으로 학습하고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 개선하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 시스템의 과학이다.

### 1. 전통적 프로그래밍의 한계 — 규칙 기반(Rule-based)의 붕괴

1990년대 스팸 필터 개발자의 일상을 상상해 보자.

- Day 1: `if "비아그라" in email: spam` — 작동!
- Day 2: 스패머가 "V.i.A.g.R.a"로 변경 → 우회 성공
- Day 3: 개발자가 정규식 패턴 추가 → 스패머가 또 우회
- Day 100: 스팸 필터 [코드베이스](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/007_codebase/) = 수십만 줄의 스파게티 코드 → 유지보수 불가능

인간이 명시적으로 모든 규칙을 하드코딩하는 방식은 **무한히 변화하는 실세계 패턴에 대응 불가능**하다.

### 2. 패러다임의 역전 — "기계에게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 정답을 주면, 기계가 규칙을 찾는다"

```text
전통 프로그래밍:   데이터 + 규칙(코드)  ──▶  출력(답)
머신러닝:          데이터 + 출력(답)    ──▶  규칙(모델)을 스스로 학습
```

이 패러다임 역전이 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 본질이다. 개발자는 스팸 단어를 찾는 대신, 1만 통의 스팸과 1만 통의 정상 메일을 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 던져준다. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 수학적 최적화([경사 하강법](/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/), [Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))를 통해 **스팸을 구분하는 최적의 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)([Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 스스로 학습**한다.

```text
┌─────────────────────────────────────────────────────────┐
│  AI(인공지능) > ML(머신러닝) > DL(딥러닝) 포함 관계        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │  AI (Artificial Intelligence)                  │     │
│  │  ┌───────────────────────────────────────┐    │     │
│  │  │  ML (Machine Learning)                 │    │     │
│  │  │  ┌─────────────────────────────────┐  │    │     │
│  │  │  │  DL (Deep Learning)              │  │    │     │
│  │  │  │  · 다층 신경망(MLP, CNN, RNN)     │  │    │     │
│  │  │  │  · Transformer, GPT, BERT        │  │    │     │
│  │  │  └─────────────────────────────────┘  │    │     │
│  │  │  · Random Forest, SVM, XGBoost       │    │     │
│  │  │  · 지도·비지도·강화 학습               │    │     │
│  │  └───────────────────────────────────────┘    │     │
│  │  · 지식 표현, 전문가 시스템, 계획 등           │     │
│  └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 전통 프로그래밍이 "요리 레시피를 모두 외워주는 선생님"이라면, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)은 "수천 개의 요리 영상을 혼자 보고 '맛있는 요리의 공통점'을 스스로 터득하는 천재 셰프"다. 선생님이 없어도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 충분하면 혼자 배운다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 3대 학습 패러다임

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 정답(Label)이 있는지, 상호작용 환경이 있는지에 따라 학습 방식이 갈린다.

```text
┌─────────────────┬──────────────────────┬───────────────────┐
│  지도 학습        │  비지도 학습           │  강화 학습          │
│ (Supervised)    │  (Unsupervised)       │ (Reinforcement)   │
├─────────────────┼──────────────────────┼───────────────────┤
│ 데이터 + 정답     │ 데이터만 (정답 없음)   │ 환경 + 보상 신호    │
│ 레이블 있음       │                      │                   │
├─────────────────┼──────────────────────┼───────────────────┤
│ · 회귀          │ · 군집화(Clustering)  │ · 에이전트 행동 선택 │
│ · 분류          │ · 차원 축소(PCA)       │ · 보상(Reward) 최대화│
│ · 이상 탐지      │ · 연관 규칙 학습       │ · 최적 정책 탐색    │
├─────────────────┼──────────────────────┼───────────────────┤
│ · 집값 예측      │ · 고객 세그멘테이션    │ · 알파고(AlphaGo)  │
│ · 스팸 분류      │ · 추천 시스템         │ · 자율주행, 로보틱스 │
│ · 암 진단        │ · 이상 거래 탐지       │ · 게임 AI          │
└─────────────────┴──────────────────────┴───────────────────┘
```

### 2. [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 학습 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 ([Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) → Inference)

```text
┌──────────────────────────────────────────────────────────────┐
│           머신러닝 파이프라인 (ML Pipeline)                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Phase 1] 학습 단계 (Training) — 오프라인/배치                  │
│                                                              │
│  ┌──────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │ 원시 데이터│─▶│ 전처리·피처     │─▶│  알고리즘 학습         │  │
│  │(Raw Data)│  │ 엔지니어링     │  │  (경사 하강법으로     │  │
│  └──────────┘  └───────────────┘  │   오차 최소화)        │  │
│                                   └──────────┬───────────┘  │
│                                              │               │
│                                              ▼               │
│                                   ┌──────────────────────┐  │
│                                   │  학습된 모델 (Model)   │  │
│                                   │  y = f(x; W, b)      │  │
│                                   │  (최적 가중치 W 내장)  │  │
│                                   └──────────┬───────────┘  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ │
│  [Phase 2] 추론 단계 (Inference) — 실시간 API                   │
│                                              │               │
│  ┌─────────────┐                             ▼               │
│  │ 새로운 데이터 │──▶ ┌──────────────────────┐ ──▶ 예측 결과   │
│  │ 입력        │    │  완성된 모델 (Model)   │    스팸 99.2%  │
│  └─────────────┘    └──────────────────────┘    집값 3.2억  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 3. 핵심 수학 원리 — [경사 하강법](/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) ([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))

모델 학습의 본질은 **[손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/))** 값을 최소화하는 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(W)를 찾는 최적화 문제다.

```text
손실(Loss)
    ▲
    │  ●  ← 초기 가중치 W₀ (무작위 출발)
    │ / \
    │/   \     기울기(Gradient) 반대 방향으로 조금씩 이동
    /     \    (학습률 η = 보폭 크기)
   /|      ●  ← 업데이트 W₁
  / |       \
 /  |        ● ← 최솟값 수렴 (최적 W*)
────┼────────────────────────────────▶  가중치(W)
```

`W_new = W_old − η × ∂L/∂W`

- η ([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/), [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate): 너무 크면 발산, 너무 작으면 수렴 속도 저하
- ∂L/∂W (기울기): 손실이 줄어드는 방향을 계산

📢 **섹션 요약 비유**: 학습은 "눈 감고 산 내려가기"와 같다. 발 아래 기울기를 느끼며(기울기 계산) 내리막 방향으로 한 걸음씩([학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)) 이동해 가장 낮은 골짜기(최솟값=최적 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 찾는다. 성급하게 너무 큰 발걸음을 내디디면 골짜기를 건너뛰어 버린다.

---

## Ⅲ. 비교 및 연결

### 1. 전통적 ML vs 딥러닝 아키텍처 비교

| 비교 항목 | 전통적 ML | 딥러닝 (Deep [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) |
|:---|:---|:---|
| **[피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링** | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문가가 직접 변수 설계 (필수) | [End-to-End](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/): 신경망이 자동 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추출 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 요구량** | 수천~수만 건으로도 동작 | 수십만~수백만 건 이상 필요 |
| **하드웨어** | CPU 충분 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) / [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) 클러스터 필수 |
| **해석 가능성** | 결정 트리 등 화이트박스 가능 | 블랙박스 ([XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) 기술로 부분 보완) |
| **학습 시간** | 분~시간 | 시간~수일 |
| **대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)** | [Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/), XGBoost, [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/), [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |
| **적합 영역** | [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/), 규제 산업 (금융·의료) | 이미지, 자연어, 음성 처리 |

### 2. 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) vs 과소적합([Underfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/246_underfitting_bias/)) 트레이드오프

```text
모델 성능
    ▲
    │           ★ 최적 지점
    │          ╱╲
    │         ╱  ╲  검증 성능(Validation)
    │        ╱    ╲____________________
    │  ___  ╱
    │ ╱    ╲        훈련 성능(Training)
    │╱      ╲___________________________________
    └─────────────────────────────────────────▶  모델 복잡도
         과소적합                  과적합
     (Underfitting)           (Overfitting)
     Bias↑ / Variance↓        Bias↓ / Variance↑
     해결: 복잡도↑, 피처 추가    해결: 정규화, 드롭아웃, 교차 검증
```

📢 **섹션 요약 비유**: 과적합은 "기출문제만 달달 외운 수험생"과 같다. 모의고사(훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 100점이지만, 수능 당일(실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에는 처음 보는 문제 앞에서 패닉이 온다. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Regularization](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/))는 기출 의존도를 낮추고 개념 이해를 강제하는 학습법이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 기준 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 상황 | 권장 접근법 | 이유 |
|:---|:---|:---|
| [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) + 레이블 있음 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1만 건 이하 | **XGBoost / [Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)** | 적은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에도 강건, 해석 가능 |
| [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) (이미지·텍스트) + 레이블 대량 | **[CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) / [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) ([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))** | 자동 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추출, 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| 레이블 없음 + 고객 세분화 | **K-Means / [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/)** | 비지도 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) |
| 금융·의료 규제 환경 + 설명 의무 | **[Logistic Regression](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) / [Decision Tree](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)** | [XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) ([Explainable AI](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/)) 대응 |
| 시계열 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | **[Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest / [LSTM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/292_lstm/)-[Autoencoder](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)** | 패턴 변화 감지 |

### 2. [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 아키텍처 — 프로덕션 ML의 필수 요소

```text
┌────────────────────────────────────────────────────────┐
│           MLOps 파이프라인 (Production ML)               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  데이터 수집·검증 ──▶ 피처 스토어 ──▶ 모델 학습           │
│       │                                   │           │
│       │ (Data Drift 감지)                  ▼           │
│       │                         모델 레지스트리          │
│       │                         (MLflow / W&B)         │
│       │                                   │           │
│       │                                   ▼           │
│       │                         쿠버네티스 서빙          │
│       │                         (KServe / Seldon)      │
│       │                                   │           │
│       └──────────── 모델 성능 모니터링 ◀───┘           │
│                     (Concept Drift 탐지)               │
│                     → 자동 재학습 트리거                 │
└────────────────────────────────────────────────────────┘
```

### 3. 기술사 빈출 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

**[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 1: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage)**
- 증상: 학습 시 미래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 훈련셋에 섞여 실험실 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(99%)이 실서비스(60%)와 엄청난 괴리
- 해결: 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 반드시 시간 순서로 분리 (TimeSeriesSplit)

**[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 2: 클래스 불균형 무시 (Class Imbalance)**
- 증상: 사기 탐지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 정상 99%, 사기 1% — 모두 정상이라고 예측해도 정확도 99% 달성
- 해결: [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) (Synthetic Minority [Oversampling](/knowledge-base/studynote/14_data_engineering/02_math_mining/096_oversampling_smote/) Technique), 가중 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 적용

**[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 3: [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 누락**
- 증상: [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) ([Support Vector Machine](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/))·KNN에서 값 범위가 큰 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)가 모델을 지배
- 해결: StandardScaler / MinMaxScaler 전처리 필수

📢 **섹션 요약 비유**: 실무 ML은 "요리 대회"와 같다. 재료 선별([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리)이 95%, 불 조절([하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/))이 나머지 5%다. 재료가 상한 채로 아무리 훌륭한 불 조절을 해도 손님(사용자)은 배탈이 난다.

---

## Ⅴ. 기대효과 및 결론

### 1. [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 도입 기대효과

| 영역 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **스팸 필터** | Rule 기반 — 매주 수동 업데이트 | ML 모델 — 새 패턴 자동 학습 | 운영 공수 80% 절감 |
| **금융 사기 탐지** | 규칙 수백 개 수동 관리 | XGBoost [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) — 실시간 스코어링 | 탐지율 40% 향상 |
| **수요 예측** | 과거 평균값 기반 발주 | 시계열 ML — 계절·이벤트 자동 반영 | 재고 비용 25% 절감 |
| **의료 영상 진단** | 전문의 수동 판독 (오진율 5~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%) | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 모델 — 양성 의심 소견 자동 표시 | 보조 탐지율 95% 이상 |

### 2. 미래 발전 방향

**방향 1: [AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) & No-[Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) ML**
하이퍼파라미터 탐색, [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 선택, 모델 선택 전 과정을 자동화하는 [AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) (Google Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/), H2O.[ai](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자의 진입장벽을 낮추고 있다.

**방향 2: [Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) & [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)**
[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), SAM 등 수천억 파라미터 [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)([Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/))을 소수 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))하여 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 특화하는 패러다임이 전통 ML을 빠르게 대체 중.

**방향 3: [Federated Learning](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) ([연합 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/))**
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 서버로 모으지 않고 각 디바이스에서 로컬 학습 후 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)만 집계, 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) + 규제 대응을 동시에 달성하는 [연합 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)이 의료·금융 분야에서 빠르게 확산.

📢 **섹션 요약 비유**: [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 미래는 "도제식 장인 교육(직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 → 수작업 모델 개발)"에서 "이미 만들어진 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 레시피([Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/))를 사다가 우리 가게 특색 소스만 추가([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))해 바로 판매"하는 프랜차이즈 모델로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **딥러닝 (Deep [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))** | ML의 하위 분야; 다층 신경망(MLP, [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/))으로 자동 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추출 |
| **[XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) ([Explainable AI](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/))** | 블랙박스 ML 모델의 결정 근거를 인간이 이해할 수 있게 해석 |
| **[MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/)** | ML 모델의 개발·배포·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링·재학습 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화 체계 |
| **[Feature Engineering](/knowledge-base/studynote/12_it_management/02_itsm_itil/081_feature_engineering/)** | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모델이 학습하기 좋은 형태의 변수로 변환하는 과정 |
| **과적합 ([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/))** | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과도 최적화 → 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 예측력 저하; [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 방지 |
| **[경사 하강법](/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/) ([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))** | [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 최소화하는 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 반복 업데이트로 찾는 핵심 최적화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| **[Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)** | 대규모 사전 학습 모델 ([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)); Fine-tuning으로 다양한 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에 적용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[규칙 기반 AI (Expert System) — 인간이 규칙 직접 코딩]
            │
            ▼
[전통적 머신러닝 — 통계·최적화 기반 자동 학습]
  (SVM, Decision Tree, Random Forest, XGBoost)
            │
            ├─── [비지도 학습 — 군집화·차원 축소]
            │
            ▼
[딥러닝 (Deep Learning) — 다층 신경망, GPU 혁명]
  (CNN, RNN, LSTM, Transformer)
            │
            ▼
[Foundation Model — GPT, BERT, SAM 등 대규모 사전 학습]
            │
            ▼
[MLOps + AutoML — 프로덕션 ML 자동화 파이프라인]
            │
            ▼
[Federated Learning + XAI — 프라이버시 보호·설명 가능 AI]
```

단순 규칙 코딩 → 통계 학습 → 신경망 → 대규모 사전 학습 → 자동화·민주화의 경로로 발전하며, 각 단계에서 컴퓨팅 파워와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모가 핵심 변수였다.

### 👶 어린이를 위한 3줄 비유 설명
1. 강아지 사진 1만 장을 보여주며 "이게 강아지야"라고 알려주면, 컴퓨터가 스스로 강아지의 생김새 비법([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))을 기억해 처음 보는 사진도 "강아지다!"라고 알아채는 것이 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)이에요.
2. 엄마가 요리 레시피를 알려주는 게 아니라, 맛있는 음식 사진 수천 장을 보고 스스로 "이런 색깔, 이런 모양이 맛있구나"를 깨닫는 아이처럼 컴퓨터도 혼자 배울 수 있어요.
3. 배우면 배울수록 더 똑똑해지지만, 가끔 기출문제만 외워서 진짜 새 시험은 망치는 것처럼 '과적합'이라는 함정도 조심해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 23 / 420

← **이전**: [22. MCTS 4단계 - 선택(Selection) -> 확장(Expansion) -> 시뮬레이션(Simulation) -> 역전파(Backpropagation)](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/)
**다음**: [24. 학습 패러다임 3종 — 지도·비지도·강화학습](/knowledge-base/studynote/10_ai/01_ai_basics/024_learning_paradigms/) →

---
