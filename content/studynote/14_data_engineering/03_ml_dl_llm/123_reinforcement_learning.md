---
title: 123. 강화 학습 (Reinforcement Learning) - 보상 기반 행동 최적화
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 **에이전트(Agent)가 환경([[066_gitlab_flow_environment_branch_strategy|Environment]])과 상호작용하면서 보상(Reward)을 최대화하는 행동 [[164_policy|정책]]([[164_policy|Policy]])을 학습**하는 ML 패러다임이며, 별도의 정답 라벨 없이 **시행착오(Trial and Error)**를 통해 학습한다.
> 2. **가치**: 바둑(AlphaGo)·로봇 제어·게임·[[211_recommendation_system|추천 시스템]]·[[263_llm_large_language_model|LLM]] 정렬([[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]])에서 **최적 행동 [[268_strategy_pattern|전략]]을 자동으로 발견**할 수 있으며, 지도 학습처럼 정답 라벨이 필요 없다.
> 3. **판단 포인트**: 탐색([[315_exploration_exploitation|Exploration]]) vs 활용(Exploitation) 딜레마가 핵심이며, [[316_q_learning|Q-Learning]](Value 기반)·[[318_policy_gradient_actor_critic|Policy Gradient]]([[164_policy|Policy]] 기반)·[[172_actor_critic|Actor-Critic]](하이브리드)의 3대 접근법을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    강화 학습 프레임워크                                │
├───────────────────────────────────────────────────────┤
│  [Agent]                                              │
│   현재 상태 s → 행동 a 선택 (Policy π)               │
│      │                                                │
│      ▼                                                │
│  [Environment]                                        │
│   행동 a 수행 → 보상 r + 새 상태 s' 반환             │
│      │                                                │
│      ▼                                                │
│  [Agent] 보상 r을 기반으로 Policy 업데이트            │
│   → 반복하여 누적 보상 최대화                        │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 게임을 처음 하는 아이가 **점수(보상)**를 올리기 위해 여러 버튼을 눌러보면서(시행착오) 최적 [[268_strategy_pattern|전략]]을 스스로 터득하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 접근법

| 접근법 | 학습 대상 | 대표 | 특징 |
|:---|:---|:---|:---|
| **Value 기반** | Q(s,a) [[163_value_function|가치 함수]] | **[[465_dqn_deep_q_network|DQN]]** | 이산 행동 |
| **[[164_policy|Policy]] 기반** | π(a\|s) 직접 | **REINFORCE** | 연속 행동 |
| **[[172_actor_critic|Actor-Critic]]** | 둘 다 | **[[395_ppo_clipping|PPO]], [[173_a3c_ppo|A3C]]** | **실용 표준** |

### [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] + 인간 피드백)
[[263_llm_large_language_model|LLM]]([[302_gpt_autoregressive|GPT]])을 인간 선호도 피드백으로 정렬하는 기법. **ChatGPT의 핵심 학습 방법**이다.

- **📢 섹션 요약 비유**: RLHF는 작문 선생님(인간)이 학생([[263_llm_large_language_model|LLM]])의 글에 "이 답변이 더 좋아"라고 **피드백(보상)**하면서 글쓰기를 가르치는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 지도 | 비지도 | 강화 |
|:---|:---|:---|:---|
| **피드백** | 정답 라벨 | 없음 | **보상** |
| **목표** | 예측 | 구조 발견 | **행동 최적화** |
| **대표** | XGBoost | K-Means | **[[395_ppo_clipping|PPO]], [[465_dqn_deep_q_network|DQN]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 분야
1. **게임**: AlphaGo(바둑), Atari([[465_dqn_deep_q_network|DQN]]).
2. **로봇**: 보행·조작 제어.
3. **[[263_llm_large_language_model|LLM]]**: [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[302_gpt_autoregressive|GPT]] 정렬).
4. **추천**: 장기 사용자 만족도 최적화.

---

## Ⅴ. 기대효과 및 결론

[[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 **"정답이 없는 순차적 의사결정 문제"의 유일한 해법**이며, RLHF를 통해 [[263_llm_large_language_model|LLM]] 정렬의 핵심 기술로 자리잡았다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Agent** | 행동을 선택하는 학습 주체 |
| **Reward** | 행동의 좋고 나쁨을 알려주는 [[130_signal|신호]] |
| **[[164_policy|Policy]]** | 상태→행동 매핑 [[268_strategy_pattern|전략]] |
| **[[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]]** | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] + 인간 피드백 ([[302_gpt_autoregressive|GPT]]) |
| **[[395_ppo_clipping|PPO]]** | 실용적 [[318_policy_gradient_actor_critic|Policy Gradient]] [[001_algorithm_definition|알고리즘]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[Q-Learning (1989) — 테이블 기반]
    │
    ▼
[DQN (2013, DeepMind) — 딥 Q-Network]
    │
    ▼
[AlphaGo (2016) — 바둑 세계 챔피언 달성]
    │
    ▼
[PPO (2017, OpenAI) — 실용적 Policy Gradient]
    │
    ▼
[현재: RLHF (ChatGPT) + GRPO — LLM 정렬]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 **게임을 처음 하면서** 점수(보상)를 올리는 방법을 배우는 거예요.
2. 좋은 행동(높은 점수)은 **더 많이 하고**, 나쁜 행동(낮은 점수)은 **줄여요**.
3. AlphaGo도 이 방법으로 바둑을 배워서 **세계 챔피언**을 이겼답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 258

← **이전**: [[122_unsupervised_learning|122. 비지도 학습 (Unsupervised Learning) - 라벨 없는 데이터의 구조 발견]]
**다음**: [[124_decision_tree|124. 의사결정 트리 (Decision Tree) - 해석 가능한 분류·회귀 알고리즘]] →

---
