---
title: "123. Reinforcement Learning"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 123
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 <strong>에이전트(Agent)가 환경(<a href="/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">Environment</a>)과 상호작용하면서 보상(Reward)을 최대화하는 행동 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>(<a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a>)을 학습</strong>하는 ML 패러다임이며, 별도의 정답 라벨 없이 <strong>시행착오(Trial and Error)</strong>를 통해 학습한다.
> 2. **가치**: 바둑(AlphaGo)·로봇 제어·게임·[추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 정렬([RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/))에서 <strong>최적 행동 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>을 자동으로 발견</strong>할 수 있으며, 지도 학습처럼 정답 라벨이 필요 없다.
> 3. **판단 포인트**: 탐색([Exploration](/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)) vs 활용(Exploitation) 딜레마가 핵심이며, [Q-Learning](/studynote/10_ai/04_ai_ops_ethics/316_q_learning/)(Value 기반)·[Policy Gradient](/studynote/10_ai/04_ai_ops_ethics/318_policy_gradient_actor_critic/)([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반)·[Actor-Critic](/studynote/10_ai/02_dl_architecture_new/172_actor_critic/)(하이브리드)의 3대 접근법을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    강화 학습 프레임워크                                |
+-------------------------------------------------------+
|  [Agent]                                              |
|   현재 상태 s -> 행동 a 선택 (Policy π)               |
|      |                                                |
|      v                                                |
|  [Environment]                                        |
|   행동 a 수행 -> 보상 r + 새 상태 s' 반환             |
|      |                                                |
|      v                                                |
|  [Agent] 보상 r을 기반으로 Policy 업데이트            |
|   -> 반복하여 누적 보상 최대화                        |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 게임을 처음 하는 아이가 <strong>점수(보상)</strong>를 올리기 위해 여러 버튼을 눌러보면서(시행착오) 최적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 스스로 터득하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 접근법

| 접근법 | 학습 대상 | 대표 | 특징 |
|:---|:---|:---|:---|
| **Value 기반** | Q(s,a) [가치 함수](/studynote/10_ai/02_dl_architecture_new/163_value_function/) | <strong><a href="/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/">DQN</a></strong> | 이산 행동 |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a> 기반</strong> | π(a\|s) 직접 | **REINFORCE** | 연속 행동 |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/172_actor_critic/">Actor-Critic</a></strong> | 둘 다 | <strong><a href="/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a>, <a href="/studynote/10_ai/02_dl_architecture_new/173_a3c_ppo/">A3C</a></strong> | **실용 표준** |

### [RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) ([강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) + 인간 피드백)
[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))을 인간 선호도 피드백으로 정렬하는 기법. <strong>ChatGPT의 핵심 학습 방법</strong>이다.

- **📢 섹션 요약 비유**: RLHF는 작문 선생님(인간)이 학생([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))의 글에 "이 답변이 더 좋아"라고 <strong>피드백(보상)</strong>하면서 글쓰기를 가르치는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 지도 | 비지도 | 강화 |
|:---|:---|:---|:---|
| **피드백** | 정답 라벨 | 없음 | **보상** |
| **목표** | 예측 | 구조 발견 | **행동 최적화** |
| **대표** | XGBoost | K-Means | <strong><a href="/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a>, <a href="/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/">DQN</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 분야
1. **게임**: AlphaGo(바둑), Atari([DQN](/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)).
2. **로봇**: 보행·조작 제어.
3. <strong><a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a></strong>: [RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) ([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 정렬).
4. **추천**: 장기 사용자 만족도 최적화.

---

## Ⅴ. 기대효과 및 결론

[강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 <strong>"정답이 없는 순차적 의사결정 문제"의 유일한 해법</strong>이며, RLHF를 통해 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 정렬의 핵심 기술로 자리잡았다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Agent** | 행동을 선택하는 학습 주체 |
| **Reward** | 행동의 좋고 나쁨을 알려주는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a></strong> | 상태->행동 매핑 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/">RLHF</a></strong> | [강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) + 인간 피드백 ([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)) |
| <strong><a href="/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a></strong> | 실용적 [Policy Gradient](/studynote/10_ai/04_ai_ops_ethics/318_policy_gradient_actor_critic/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Q-Learning (1989) — 테이블 기반]
    |
    v
[DQN (2013, DeepMind) — 딥 Q-Network]
    |
    v
[AlphaGo (2016) — 바둑 세계 챔피언 달성]
    |
    v
[PPO (2017, OpenAI) — 실용적 Policy Gradient]
    |
    v
[현재: RLHF (ChatGPT) + GRPO — LLM 정렬]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [강화 학습](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 **게임을 처음 하면서** 점수(보상)를 올리는 방법을 배우는 거예요.
2. 좋은 행동(높은 점수)은 **더 많이 하고**, 나쁜 행동(낮은 점수)은 **줄여요**.
3. AlphaGo도 이 방법으로 바둑을 배워서 <strong>세계 챔피언</strong>을 이겼답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 258

<- **이전**: [122. 비지도 학습 (Unsupervised Learning) - 라벨 없는 데이터의 구조 발견](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)
**다음**: [124. 의사결정 트리 (Decision Tree) - 해석 가능한 분류·회귀 알고리즘](/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/) ->

---
