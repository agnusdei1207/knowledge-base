---
title: 24. 학습 패러다임 3종 — 지도·비지도·강화학습
date: '2026-04-29'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[241_machine_learning_basics|머신러닝]](ML)의 3대 학습 패러다임은 [[121_supervised_learning|지도 학습]]([[121_supervised_learning|Supervised Learning]], 레이블 있는 [[001_dikw_pyramid|데이터]]), [[122_unsupervised_learning|비지도 학습]]([[122_unsupervised_learning|Unsupervised Learning]], 레이블 없는 [[001_dikw_pyramid|데이터]]), [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]([[094_reinforcement_learning|Reinforcement Learning]], 보상 기반 환경 상호작용)으로 구분되며, 각각 다른 [[001_dikw_pyramid|데이터]] 구조와 목적 함수를 갖는다.
> 2. **가치**: 이 3가지 패러다임의 경계를 이해하는 것이 ML 문제 정의의 첫 단계다 — 레이블 수집 비용, [[001_dikw_pyramid|데이터]] 구조, 목표([[104_classification_analysis|분류]]/군집/[[164_policy|정책]])에 따라 어떤 패러다임을 선택하느냐가 모델 설계 전체를 결정한다.
> 3. **판단 포인트**: 현대 AI는 순수한 3종 패러다임보다 반지도 학습(Semi-supervised), [[266_self_supervised_learning|자기 지도 학습]](Self-supervised, [[302_gpt_autoregressive|GPT]]·BERT의 기반), [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]+사람 피드백([[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]])처럼 경계를 허무는 하이브리드 방식이 주류이므로, 패러다임의 조합이 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[241_machine_learning_basics|머신러닝]] 문제를 정의할 때 가장 먼저 결정해야 할 것이 "어떤 [[001_dikw_pyramid|데이터]]가 있고, 무엇을 학습시킬 것인가"이다. 이 결정이 학습 패러다임을 결정한다.

```text
┌────────────────────────────────────────────────────────────┐
│            3대 학습 패러다임 비교                             │
├──────────────┬────────────────────────┬────────────────────┤
│  지도 학습   │     비지도 학습          │    강화 학습        │
├──────────────┼────────────────────────┼────────────────────┤
│ 레이블 데이터 │ 레이블 없는 데이터       │ 환경·보상 신호      │
│ f(x) → y    │ 숨겨진 패턴 발견         │ 최적 정책 π 학습    │
│ 분류·회귀    │ 군집·차원 축소·생성      │ 게임·로봇·추천      │
│ CNN, SVM    │ K-means, VAE, GAN       │ DQN, PPO, AlphaGo  │
└──────────────┴────────────────────────┴────────────────────┘
```

- **📢 섹션 요약 비유**: [[121_supervised_learning|지도 학습]]은 정답이 있는 시험(레이블), [[122_unsupervised_learning|비지도 학습]]은 정답 없이 스스로 [[104_classification_analysis|분류]]하는 탐구 활동, [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 게임을 하며 점수로 [[268_strategy_pattern|전략]]을 배우는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[121_supervised_learning|지도 학습]] ([[121_supervised_learning|Supervised Learning]])

```text
입력 x → 모델 f → 예측 ŷ → 손실(Loss) = L(y, ŷ) → 역전파(Backprop) → 가중치 업데이트
레이블 y ─────────────────────────────────────────────↗
```

- [[104_classification_analysis|분류]]: 스팸 메일 탐지, 이미지 [[104_classification_analysis|분류]], 의료 진단
- 회귀: 집값 예측, 주가 예측, 수요 예측

### [[122_unsupervised_learning|비지도 학습]] ([[122_unsupervised_learning|Unsupervised Learning]])

| 유형 | 목적 | 대표 [[001_algorithm_definition|알고리즘]] |
|:---|:---|:---|
| **[[105_clustering_analysis|군집화]] ([[105_clustering_analysis|Clustering]])** | 유사한 [[001_dikw_pyramid|데이터]] [[535_grouping_counting_free_space|그룹화]] | K-means, [[351_dbscan_density_based_clustering|DBSCAN]] |
| **[[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]** | 고차원 [[283_data_visualization_dashboard_report|데이터 시각화]] | [[163_pca|PCA]], t-SNE, UMAP |
| **[[087_process_state_transition|생성]] 모델** | 새 [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]] | [[315_autoencoder_vae|VAE]], [[154_gan_generative_adversarial_network|GAN]], Diffusion |
| **[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]** | 정상 패턴 학습 후 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] | [[335_autoencoder|Autoencoder]] |

### [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] ([[094_reinforcement_learning|Reinforcement Learning]])

```text
[에이전트 (Agent)]
       │ 행동(Action) a
       ▼
[환경 (Environment)]
       │ 상태(State) s', 보상(Reward) r
       ▼
[에이전트] → 정책(Policy) π 업데이트
목표: 누적 보상(Cumulative Reward) 최대화
```

- **📢 섹션 요약 비유**: [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 강아지 훈련이다. 올바른 행동(앉아!)에 간식(보상)을 주고, 잘못된 행동에는 보상을 주지 않으면서 개(에이전트)가 최적 행동 [[164_policy|정책]]을 스스로 학습한다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[121_supervised_learning|지도 학습]] | [[122_unsupervised_learning|비지도 학습]] | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]]** | 레이블 필요 | 레이블 불필요 | 환경 시뮬레이션 |
| **목표** | 예측 함수 학습 | 구조 발견 | 최적 [[164_policy|정책]] 학습 |
| **피드백** | 즉각 (레이블) | 없음 | [[015_지연_데이터_관점|지연]] (보상) |
| **난이도** | 낮음 | 중간 | 높음 |

[[266_self_supervised_learning|자기 지도 학습]]([[266_self_supervised_learning|Self-supervised Learning]])은 [[001_dikw_pyramid|데이터]] 자체에서 레이블을 [[087_process_state_transition|생성]](ex: 문장 다음 단어 예측)하여 [[582_llm_based_code_generation_tools|대규모 언어 모델]]([[302_gpt_autoregressive|GPT]], [[301_bert_mlm|BERT]])을 훈련하는 [[122_unsupervised_learning|비지도 학습]]의 현대적 발전 형태다.

- **📢 섹션 요약 비유**: [[266_self_supervised_learning|자기 지도 학습]]은 책을 읽으며 스스로 퀴즈를 만들고 답하는 독학이다. 선생님(레이블)이 없어도 책(비레이블 [[001_dikw_pyramid|데이터]])에서 스스로 배운다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 이커머스 [[211_recommendation_system|추천 시스템]] 설계
- **[[122_unsupervised_learning|비지도 학습]] (1단계)**: 구매 이력 [[105_clustering_analysis|군집화]] → 고객 세그먼트 발견.
- **[[121_supervised_learning|지도 학습]] (2단계)**: 세그먼트 레이블 + 구매 [[001_dikw_pyramid|데이터]] → 클릭률([[090_ctr_mode|CTR]]) 예측 모델.
- **[[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] (3단계)**: 추천 → 클릭 보상 → [[164_policy|정책]] 최적화 (장기 구매 전환 극대화).

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 레이블 없이 [[121_supervised_learning|지도 학습]]을 시도하거나, 레이블이 풍부한데 [[122_unsupervised_learning|비지도 학습]]을 선택하는 패러다임 불일치 [[128_water_scrum_fall_anti_pattern|안티패턴]]. 각 패러다임은 [[001_dikw_pyramid|데이터]] 구조에 의해 결정되므로, [[001_dikw_pyramid|데이터]] 탐색([[064_eda|EDA]])을 먼저 수행하고 패러다임을 선택해야 한다.

- **📢 섹션 요약 비유**: 정답지(레이블)가 있는데 스스로 탐구하는 것은 시험 답안지를 갖고도 스스로 풀겠다고 옆으로 치우는 것이다. 반대로 정답지가 없는데 [[121_supervised_learning|지도 학습]]을 쓰는 건 없는 답안지를 만들어내는 헛수고다.

---

## Ⅴ. 기대효과 및 결론

| 패러다임 | 대표 성과 |
|:---|:---|
| **[[121_supervised_learning|지도 학습]]** | 의료 [[190_ai_llm_requirements_specification|AI]] 진단 정확도 95%+ |
| **[[122_unsupervised_learning|비지도 학습]]** | 고객 세그먼트 자동 발견 |
| **[[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]** | AlphaGo 세계 챔피언 격파, 로봇 제어 |

[[263_llm_large_language_model|LLM]] ([[263_llm_large_language_model|Large Language Model]], 대형 언어 모델)의 등장으로 [[266_self_supervised_learning|자기 지도 학습]] + [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]])의 조합이 [[190_ai_llm_requirements_specification|AI]] 패러다임의 새 표준이 되었으며, 3대 패러다임의 경계는 더욱 흐려지고 있다.

- **📢 섹션 요약 비유**: 3대 학습 패러다임은 인간 학습의 3가지 방식이다. [[121_supervised_learning|지도 학습]]은 선생님에게 배우기, [[122_unsupervised_learning|비지도 학습]]은 스스로 탐구하기, [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 경험으로 깨닫기. 현대 AI는 이 세 가지를 모두 혼합하여 사용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[075_loss_function_cost_function|손실 함수]] ([[087_loss_function|Loss Function]])** | [[121_supervised_learning|지도 학습]]의 학습 방향 결정 |
| **K-means / [[351_dbscan_density_based_clustering|DBSCAN]]** | 비지도 [[105_clustering_analysis|군집화]] 대표 [[001_algorithm_definition|알고리즘]] |
| **[[316_q_learning|Q-Learning]] / [[395_ppo_clipping|PPO]]** | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] [[164_policy|정책]] 최적화 [[001_algorithm_definition|알고리즘]] |
| **[[266_self_supervised_learning|자기 지도 학습]]** | [[122_unsupervised_learning|비지도 학습]]의 현대적 발전; [[302_gpt_autoregressive|GPT]], [[301_bert_mlm|BERT]] |
| **[[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]]** | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] + 인간 피드백; ChatGPT 훈련 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[지도 학습 — 레이블 데이터, 예측 함수 학습]
    │
    ▼
[비지도 학습 — 패턴·구조 발견, 생성 모델]
    │
    ▼
[강화 학습 — 환경 상호작용, 보상 기반 정책 최적화]
    │
    ▼
[자기 지도 학습 — 데이터 자체에서 레이블 생성 (GPT, BERT)]
    │
    ▼
[RLHF — 인간 피드백 강화 학습 (ChatGPT, Claude)]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[121_supervised_learning|지도 학습]]은 선생님이 정답을 알려주며 가르치는 것, [[122_unsupervised_learning|비지도 학습]]은 스스로 탐구하며 패턴을 찾는 것, [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 게임을 하면서 점수를 올리는 법을 배우는 것이에요!
2. 스팸 메일 잡기는 [[121_supervised_learning|지도 학습]], 고객 취향 자동 [[104_classification_analysis|분류]]는 [[122_unsupervised_learning|비지도 학습]], 바둑 [[190_ai_llm_requirements_specification|AI]](알파고)는 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]이에요.
3. 요즘 챗GPT 같은 AI는 이 세 가지를 모두 섞어서 훨씬 더 똑똑해졌답니다!
