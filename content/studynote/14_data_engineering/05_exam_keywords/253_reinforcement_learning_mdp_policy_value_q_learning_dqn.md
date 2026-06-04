+++
title = "253. 강화 학습 (Reinforcement Learning) MDP 정책 가치 Q러닝 DQN"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 강화 학습([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/))은 시행착오(Trial-and-Error)를 통해 누적 보상(Cumulative Reward)을 최대화하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))을 스스로 학습하는 패러다임이다.
> 2. **가치**: [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/)([Markov Decision Process](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/)) 수학적 프레임워크와 Q러닝([Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/))·[DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)([Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/))은 게임·로봇 제어·금융 트레이딩 등 순차적 의사결정 문제를 자동화한다.
> 3. **판단 포인트**: 탐색([Exploration](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/))과 활용(Exploitation)의 균형, 보상 설계(Reward Shaping)의 품질, 샘플 효율성(Sample Efficiency)이 강화 학습 시스템의 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

### 1.1 강화 학습의 세 가지 핵심 구성요소

강화 학습은 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/))과 달리 정답 레이블(Label)이 없다. 대신 환경([Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/))과 상호작용하며 보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)(Reward [Signal](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/))를 통해 학습한다.

| 요소 | 설명 | 예시(자율주행) |
|:---|:---|:---|
| **에이전트(Agent)** | 행동을 결정하는 학습 주체 | 자율주행 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| <strong>환경(<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">Environment</a>)</strong> | 에이전트가 상호작용하는 세계 | 도로·교통 상황 |
| <strong>상태(<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a>, S)</strong> | 현재 환경 관찰 정보 | 차량 위치·속도·주변 차량 |
| **행동(Action, A)** | 에이전트의 선택 | 가속·감속·조향 |
| **보상(Reward, R)** | 행동 결과의 피드백 | +1(안전), -[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)(충돌) |
| <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>(<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a>, π)</strong> | 상태->행동 매핑 함수 | "이 상황에서 무엇을 할지" |

### 1.2 강화 학습이 필요한 이유

정답 데이터를 수집하기 어렵거나 탐색 공간이 너무 큰 문제(바둑 경우의 수 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^170)에서 강화 학습은 유일한 해답이다. 알파고(AlphaGo)는 자기 자신과 대국(셀프 플레이, Self-play)하며 인간 최고수를 넘어섰다.

📢 **섹션 요약 비유**: 강화 학습은 아이가 자전거 타는 법을 배우는 방식이다. 넘어지면(마이너스 보상), 잘 달리면(플러스 보상) — 아무도 "이렇게 핸들을 잡아야 해"라고 가르쳐주지 않아도 수백 번의 시행착오로 스스로 익힌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/)([Markov Decision Process](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/)) 수학적 정의

MDP는 (S, A, P, R, γ) 다섯 요소의 튜플로 정의된다.

| 기호 | 의미 | 설명 |
|:---|:---|:---|
| **S** | 상태 공간([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Space) | 가능한 모든 상태 집합 |
| **A** | 행동 공간(Action Space) | 가능한 모든 행동 집합 |
| **P(s'|s,a)** | 전이 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)(Transition [Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) | 상태 s에서 a 수행 후 s'로 이동할 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) |
| **R(s,a)** | 보상 함수(Reward Function) | 상태 s에서 a 수행 시 즉각 보상 |
| **γ** | 할인율(Discount Factor, 0~1) | 미래 보상의 현재 가치 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) |

<strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/141_markov_property/">마르코프 성질</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/141_markov_property/">Markov Property</a>)</strong>: 현재 상태만으로 미래를 예측하는데 충분하다. P(S_{t+1}|S_t, A_t) = P(S_{t+1}|S_0, ..., S_t, A_t)

### 2.2 [가치 함수](/knowledge-base/studynote/10_ai/02_dl_architecture_new/163_value_function/)([Value Function](/knowledge-base/studynote/10_ai/02_dl_architecture_new/163_value_function/))와 Q함수

```
+-----------------------------------------------------------------+
|           가치 함수 계층 구조                                    |
+-----------------------------------------------------------------+
|                                                                  |
|  V^π(s) = 상태 가치 함수 (State Value Function)                  |
|         = 상태 s에서 정책 π를 따를 때 기대 누적 보상             |
|         = E[R_t + γR_{t+1} + γ^R_{t+2} + ...]                  |
|                                                                  |
|  Q^π(s,a) = 행동-가치 함수 (Action-Value Function, Q함수)        |
|           = 상태 s에서 행동 a를 취한 후 정책 π를 따를 때         |
|             기대 누적 보상                                        |
|           = E[R_t + γ·max_a Q(s_{t+1}, a)]                     |
|                                                                  |
|  최적 정책: π*(s) = argmax_a Q*(s,a)                            |
|                                                                  |
|  벨만 방정식 (Bellman Equation):                                  |
|  Q(s,a) <- Q(s,a) + α[r + γ·max_a' Q(s',a') - Q(s,a)]         |
|            ^업데이트   ^ TD 에러 (Temporal Difference Error)    |
+-----------------------------------------------------------------+
```

### 2.3 [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)([Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)) 구조

```
+-----------------------------------------------------------------+
|                DQN (Deep Q-Network) 아키텍처                     |
+-----------------------------------------------------------------+
|                                                                  |
|  상태 입력(State)                                                |
|  [게임 화면 픽셀 84x84x4]                                        |
|         |                                                        |
|         v                                                        |
|  +-----------------+                                            |
|  |  CNN 레이어      |  특징 추출 (Feature Extraction)            |
|  |  Conv->Pool×3    |                                            |
|  +--------+--------+                                            |
|           |                                                      |
|           v                                                      |
|  +-----------------+                                            |
|  |  FC 레이어       |  Q값 예측                                  |
|  |  Dense×2        |                                            |
|  +--------+--------+                                            |
|           |                                                      |
|           v                                                      |
|  Q값 출력: [Q(s,left)=2.3, Q(s,right)=1.5, Q(s,fire)=3.1]     |
|  행동 선택: argmax -> fire 선택                                    |
|                                                                  |
|  +--------------------------------------------+                 |
|  |  경험 재생 버퍼 (Experience Replay Buffer)  |                 |
|  |  (s, a, r, s') 100만개 저장                |                 |
|  |  미니배치 랜덤 샘플링으로 학습              |                 |
|  +--------------------------------------------+                 |
|                                                                  |
|  타겟 네트워크 (Target Network): 주기적으로 가중치 복사           |
|  -> 학습 안정화 (TD 에러 발산 방지)                               |
+-----------------------------------------------------------------+
```

### 2.4 DQN의 두 가지 핵심 혁신

| 기법 | 문제 | 해결 방법 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/">경험 재생</a>(<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/">Experience Replay</a>)</strong> | 연속된 경험은 상관관계가 높아 학습 불안정 | 경험을 버퍼에 저장 후 랜덤 샘플링 |
| <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/">타겟 네트워크</a>(<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/">Target Network</a>)</strong> | Q 업데이트 목표가 계속 변해 발산 | 별도 고정 [타겟 네트워크](/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/)로 안정화 |

📢 **섹션 요약 비유**: DQN은 비디오 게임을 연습하는 선수와 같다. 과거 경기 녹화본([경험 재생](/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/) 버퍼)을 무작위로 다시 보며 편향 없이 연습하고, "이 정도면 합격"하는 명확한 기준점([타겟 네트워크](/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/))을 고정해두어 목표가 흔들리지 않게 한다.

---

## Ⅲ. 비교 및 연결

### 3.1 강화 학습 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 계보

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 특징 | 대표 적용 |
|:---|:---|:---|:---|
| **모델 프리(Model-Free) 가치 기반** | [Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/), [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/) | Q함수 직접 학습 | Atari 게임 |
| <strong>모델 프리 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 기반</strong> | REINFORCE, [A3C](/knowledge-base/studynote/10_ai/02_dl_architecture_new/173_a3c_ppo/) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 직접 최적화 | 로봇 제어 |
| <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/172_actor_critic/">액터-크리틱</a>(<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/172_actor_critic/">Actor-Critic</a>)</strong> | [PPO](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/), SAC | 가치+[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결합 | 범용 RL |
| **모델 기반(Model-Based)** | AlphaZero, Dreamer | 환경 모델 학습 후 계획 | 보드게임 |

### 3.2 탐색-활용 딜레마([Exploration](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)-Exploitation Tradeoff)

```
ε-탐욕(ε-greedy) 전략:
- ε 확률로 무작위 행동 (탐색, Exploration)
- (1-ε) 확률로 최적 행동 선택 (활용, Exploitation)
- 학습 초기: ε=1.0 -> 후기: ε=0.1 (점진적 감소)

UCB (Upper Confidence Bound):
- 불확실성이 큰 행동을 우선 탐색
- a = argmax[Q(a) + c√(ln(N)/n(a))]
  c: 탐색 강도, N: 총 스텝, n(a): a 선택 횟수
```

📢 **섹션 요약 비유**: 탐색-활용 딜레마는 단골 식당과 새 식당 사이의 선택이다. 항상 단골 식당만 가면(활용) 더 맛있는 식당을 발견 못 하고, 항상 새 식당만 가면(탐색) 맛없는 집에서 식사를 자주 한다. ε-탐욕 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 90%는 검증된 맛집, [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%는 새 식당 시도하는 균형잡힌 식도락가 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 알파고(AlphaGo) 강화 학습 적용 사례

```
AlphaGo 학습 파이프라인:
1단계: 지도 학습 (SL Policy Network)
  -> 인간 기보 16만 게임으로 정책 초기화

2단계: 자기 대국 강화 학습 (RL Policy Network)
  -> SL 모델과 셀프 플레이로 승리 보상 최대화

3단계: 가치 네트워크 (Value Network)
  -> 각 포지션의 승률 예측 학습

4단계: MCTS(Monte Carlo Tree Search) + 두 네트워크 결합
  -> 정책 네트워크(이동 선택) + 가치 네트워크(포지션 평가)
```

### 4.2 산업 적용 사례별 보상 설계

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 에이전트 | 보상 설계 |
|:---|:---|:---|
| 자율주행 | 자동차 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | +1(안전 주행), -100(충돌), -0.1(급제동) |
| [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 냉각 | Google DeepMind | 에너지 효율 40% 개선 보상 |
| 금융 트레이딩 | 매매 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 샤프 비율(Sharpe Ratio) 최대화 |
| 로보틱스 | 조립 로봇 | 조립 성공/실패 바이너리 보상 |

### 4.3 기술사 논술 핵심

- **샘플 효율성(Sample Efficiency)**: 실세계 로봇은 실험 비용이 높아 가상 환경(Sim-to-Real) 선행 학습 필수
- **보상 해킹(Reward Hacking)**: 잘못 설계된 보상 함수를 에이전트가 예상치 못한 방식으로 달성
- <strong>안전 강화 학습(<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/">Safe</a> RL)</strong>: 학습 과정에서 위험 행동을 제한하는 제약 조건(Constraint) 추가

📢 **섹션 요약 비유**: 강화 학습의 보상 설계는 회사 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 설정과 같다. KPI를 잘못 설정하면(예: "매출만 극대화") 직원들이 고객 만족을 포기하고 매출만 올린다. RL 에이전트도 잘못된 보상 함수를 발견하면 우리가 원하지 않는 방식으로 목표를 달성해버린다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 강화 학습 미래 전망

| 발전 방향 | 핵심 기술 | 기대 효과 |
|:---|:---|:---|
| **오프라인 RL(Offline RL)** | 온라인 탐색 없이 데이터만으로 학습 | 위험한 환경 안전 학습 |
| **계층적 RL(Hierarchical RL)** | 서브 목표(Sub-goal) 분해 | 장기 계획 수립 |
| **멀티 에이전트 RL(MARL)** | 협력·경쟁 에이전트 군 | [스마트 그리드](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/161_smart_grid_architecture/)·교통 최적화 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/">RLHF</a>(RL from Human Feedback)</strong> | 인간 선호도 보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) | ChatGPT 등 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 정렬(Alignment) |

### 5.2 결론

강화 학습은 [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/) 프레임워크와 [벨만 방정식](/knowledge-base/studynote/10_ai/05_data_science_ml/372_bellman_equation/)이라는 수학적 기반 위에 딥러닝(Deep [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))을 결합한 DQN으로 복잡한 현실 문제에 적용 가능해졌다. [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/)([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/) from Human Feedback)는 ChatGPT와 같은 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 정렬(Alignment)에 핵심적으로 사용되며, 강화 학습은 이제 단순 게임 AI를 넘어 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 안전성의 핵심 기술로 자리 잡았다.

📢 **섹션 요약 비유**: 강화 학습은 인류의 진화 방식을 압축한 것이다. 수백만 년의 시행착오 대신, 컴퓨터 시뮬레이션 안에서 수백만 번의 경험을 압축하여 며칠 안에 전문가 수준에 도달한다. 알파고가 바둑 역사를 하룻밤에 배운 것처럼.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 수학적 프레임워크 | [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/)([Markov Decision Process](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/)) | 순차 의사결정 수학 모델 |
| 핵심 함수 | Q함수(Action-[Value Function](/knowledge-base/studynote/10_ai/02_dl_architecture_new/163_value_function/)) | 상태-행동 쌍의 기대 누적 보상 |
| 학습 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | Q러닝([Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/)) | [벨만 방정식](/knowledge-base/studynote/10_ai/05_data_science_ml/372_bellman_equation/) 기반 가치 업데이트 |
| 딥러닝 결합 | [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)([Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)) | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) + Q러닝, [경험 재생](/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/) |
| 학습 안정화 | [경험 재생](/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/)([Experience Replay](/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/)) | 상관 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 제거, 랜덤 샘플링 |
| 학습 안정화 | [타겟 네트워크](/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/)([Target Network](/knowledge-base/studynote/10_ai/02_dl_architecture_new/170_target_network/)) | TD 에러 발산 방지 |
| 탐색 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | ε-탐욕(ε-greedy) | 탐색-활용 균형 |
| [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 연계 | [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) | 인간 피드백 기반 모델 정렬 |

### 👶 어린이를 위한 3줄 비유 설명
1. 강화 학습은 게임을 하다가 점수가 올라가면 "잘 했네!" 하고 계속하고, 떨어지면 "아 이건 나쁜 방법이구나" 깨닫는 것처럼 스스로 배우는 AI예요.

### 📈 관련 키워드 및 발전 흐름도

```text
MDP: 상태(S) · 행동(A) · 보상(R) · 전이(T)
    |
    v
가치 기반: Q-Learning -> DQN (딥러닝 결합)
정책 기반: REINFORCE -> PPO · A3C
    |
    v
모델 기반 RL · Offline RL · Multi-Agent RL
    |
    v
응용: 게임 AI · 로봇 · RLHF (LLM 정렬)
```
2. Q러닝은 각 상황에서 어떤 선택이 미래에 제일 많은 점수를 줄지 표를 만들어 기억하는 것이고, DQN은 그 표가 너무 커질 때 신경망([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 두뇌)으로 대신 계산하는 방법이에요.
3. 알파고는 이 방법으로 사람과 수백만 번 바둑을 두면서 세계 챔피언보다 강해졌어요—인간이 5000년 동안 쌓은 바둑 지식을 단 몇 달 만에 배운 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 253 / 258

<- **이전**: [252. 지식 증류 (Knowledge Distillation) 양자화 (Quantization) 경량 SLM 디퓨전 생성](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)
**다음**: [254. MLOps 데이터·컨셉 드리프트 피처 스토어 모니터링 종합](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/254_mlops_data_concept_drift_feature_store_monitoring/) ->

---
