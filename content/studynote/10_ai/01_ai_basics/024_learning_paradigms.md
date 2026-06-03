+++
title = "24. 학습 패러다임 3종 — 지도·비지도·강화학습"
date = 2026-04-29

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(ML)의 3대 학습 패러다임은 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/), 레이블 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/), 레이블 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/), 보상 기반 환경 상호작용)으로 구분되며, 각각 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조와 목적 함수를 갖는다.
> 2. **가치**: 이 3가지 패러다임의 경계를 이해하는 것이 ML 문제 정의의 첫 단계다 — 레이블 수집 비용, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조, 목표([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)/군집/[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))에 따라 어떤 패러다임을 선택하느냐가 모델 설계 전체를 결정한다.
> 3. **판단 포인트**: 현대 AI는 순수한 3종 패러다임보다 반지도 학습(Semi-supervised), [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)(Self-supervised, [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·BERT의 기반), [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)+사람 피드백([RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/))처럼 경계를 허무는 하이브리드 방식이 주류이므로, 패러다임의 조합이 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 문제를 정의할 때 가장 먼저 결정해야 할 것이 "어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있고, 무엇을 학습시킬 것인가"이다. 이 결정이 학습 패러다임을 결정한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3대 학습 패러다임 비교</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">지도 학습</div><div class="kb-diagram-cell">비지도 학습</div><div class="kb-diagram-cell">강화 학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">레이블 데이터</div><div class="kb-diagram-cell">레이블 없는 데이터</div><div class="kb-diagram-cell">환경·보상 신호</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">f(x) → y</div><div class="kb-diagram-cell">숨겨진 패턴 발견</div><div class="kb-diagram-cell">최적 정책 π 학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분류·회귀</div><div class="kb-diagram-cell">군집·차원 축소·생성</div><div class="kb-diagram-cell">게임·로봇·추천</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CNN, SVM</div><div class="kb-diagram-cell">K-means, VAE, GAN</div><div class="kb-diagram-cell">DQN, PPO, AlphaGo</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 정답이 있는 시험(레이블), [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 정답 없이 스스로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 탐구 활동, [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 게임을 하며 점수로 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 배우는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) ([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">입력 x → 모델 f → 예측 ŷ → 손실(Loss) = L(y, ŷ) → 역전파(Backprop) → 가중치 업데이트</div>
<div class="kb-diagram-note">레이블 y ↗</div>
</div>
</div>



- [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/): 스팸 메일 탐지, 이미지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 의료 진단
- 회귀: 집값 예측, 주가 예측, 수요 예측

### [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) ([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))

| 유형 | 목적 | 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/">군집화</a> (<a href="/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/">Clustering</a>)</strong> | 유사한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) | K-means, [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/">차원 축소</a></strong> | 고차원 [데이터 시각화](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/283_data_visualization_dashboard_report/) | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), t-SNE, UMAP |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 모델</strong> | 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [VAE](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/315_autoencoder_vae/), [GAN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/), Diffusion |
| <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a></strong> | 정상 패턴 학습 후 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | [Autoencoder](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) |

### [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) ([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">에이전트 (Agent)</div></div>
<div class="kb-diagram-note">행동(Action) a</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">환경 (Environment)</div></div>
<div class="kb-diagram-note">상태(State) s', 보상(Reward) r</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">에이전트</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">정책(Policy) π 업데이트</div></div>
<div class="kb-diagram-note">목표: 누적 보상(Cumulative Reward) 최대화</div>
</div>
</div>



- **📢 섹션 요약 비유**: [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 강아지 훈련이다. 올바른 행동(앉아!)에 간식(보상)을 주고, 잘못된 행동에는 보상을 주지 않으면서 개(에이전트)가 최적 행동 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 스스로 학습한다.

---

## Ⅲ. 비교 및 연결

| 항목 | [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) | [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 레이블 필요 | 레이블 불필요 | 환경 시뮬레이션 |
| **목표** | 예측 함수 학습 | 구조 발견 | 최적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 학습 |
| **피드백** | 즉각 (레이블) | 없음 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (보상) |
| **난이도** | 낮음 | 중간 | 높음 |

[자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)([Self-supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/))은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체에서 레이블을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)(ex: 문장 다음 단어 예측)하여 [대규모 언어 모델](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/)([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))을 훈련하는 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 현대적 발전 형태다.

- **📢 섹션 요약 비유**: [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)은 책을 읽으며 스스로 퀴즈를 만들고 답하는 독학이다. 선생님(레이블)이 없어도 책(비레이블 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에서 스스로 배운다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 이커머스 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) 설계
- <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a> (1단계)</strong>: 구매 이력 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) → 고객 세그먼트 발견.
- <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/">지도 학습</a> (2단계)</strong>: 세그먼트 레이블 + 구매 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) → 클릭률([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/)) 예측 모델.
- <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/">강화 학습</a> (3단계)</strong>: 추천 → 클릭 보상 → [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화 (장기 구매 전환 극대화).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 레이블 없이 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)을 시도하거나, 레이블이 풍부한데 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)을 선택하는 패러다임 불일치 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). 각 패러다임은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조에 의해 결정되므로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/))을 먼저 수행하고 패러다임을 선택해야 한다.

- **📢 섹션 요약 비유**: 정답지(레이블)가 있는데 스스로 탐구하는 것은 시험 답안지를 갖고도 스스로 풀겠다고 옆으로 치우는 것이다. 반대로 정답지가 없는데 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)을 쓰는 건 없는 답안지를 만들어내는 헛수고다.

---

## Ⅴ. 기대효과 및 결론

| 패러다임 | 대표 성과 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/">지도 학습</a></strong> | 의료 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 진단 정확도 95%+ |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a></strong> | 고객 세그먼트 자동 발견 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/">강화 학습</a></strong> | AlphaGo 세계 챔피언 격파, 로봇 제어 |

[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) ([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), 대형 언어 모델)의 등장으로 [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/) + [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) ([Reinforcement Learning from Human Feedback](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/))의 조합이 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 패러다임의 새 표준이 되었으며, 3대 패러다임의 경계는 더욱 흐려지고 있다.

- **📢 섹션 요약 비유**: 3대 학습 패러다임은 인간 학습의 3가지 방식이다. [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 선생님에게 배우기, [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 스스로 탐구하기, [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 경험으로 깨닫기. 현대 AI는 이 세 가지를 모두 혼합하여 사용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/">손실 함수</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/">Loss Function</a>)</strong> | [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)의 학습 방향 결정 |
| <strong>K-means / <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/">DBSCAN</a></strong> | 비지도 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/">Q-Learning</a> / <a href="/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a></strong> | [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/">자기 지도 학습</a></strong> | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 현대적 발전; [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/">RLHF</a></strong> | [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) + 인간 피드백; ChatGPT 훈련 방법 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">지도 학습 — 레이블 데이터, 예측 함수 학습</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비지도 학습 — 패턴·구조 발견, 생성 모델</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">강화 학습 — 환경 상호작용, 보상 기반 정책 최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">자기 지도 학습 — 데이터 자체에서 레이블 생성 (GPT, BERT)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">RLHF — 인간 피드백 강화 학습 (ChatGPT, Claude)</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 선생님이 정답을 알려주며 가르치는 것, [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 스스로 탐구하며 패턴을 찾는 것, [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 게임을 하면서 점수를 올리는 법을 배우는 것이에요!
2. 스팸 메일 잡기는 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/), 고객 취향 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/), 바둑 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(알파고)는 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)이에요.
3. 요즘 챗GPT 같은 AI는 이 세 가지를 모두 섞어서 훨씬 더 똑똑해졌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 420

← **이전**: [23. 머신러닝 개념 (Machine Learning Concept)](/knowledge-base/studynote/10_ai/01_ai_basics/023_machine_learning_concept/)
**다음**: [25. 편향-분산 트레이드오프 (Bias-Variance Tradeoff)](/knowledge-base/studynote/10_ai/01_ai_basics/025_bias_variance_tradeoff/) →

---
