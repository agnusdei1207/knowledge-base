+++
title = "167. 큐-러닝 (Q-Learning)"
date = 2026-04-17

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 큐-러닝 ([Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/))은 상태 ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))와 행동 (Action) 조합마다 미래 누적 보상을 Q값으로 학습하는 모델 프리 (Model-Free) [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)의 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 환경의 내부 전이 모델을 몰라도 실제 보상과 다음 상태의 최대 기대가치를 이용해, 시행착오만으로도 최적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)에 가까운 선택 기준을 구축한다.
> 3. **판단 포인트**: 상태·행동 공간이 작고 이산적이면 강력하지만, 고차원 입력·연속 제어·안전 제약이 커지는 순간에는 [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/) ([Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/))이나 [액터-크리틱](/knowledge-base/studynote/10_ai/02_dl_architecture_new/172_actor_critic/) ([Actor-Critic](/knowledge-base/studynote/10_ai/02_dl_architecture_new/172_actor_critic/)) 계열로 확장해야 한다.

---

## Ⅰ. 개요 및 필요성

큐-러닝 ([Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/))은 에이전트가 환경과 상호작용하며 "지금 이 행동이 결국 얼마나 이득인가"를 학습하는 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)처럼 정답 레이블이 주어지지 않고, 동적 계획법 ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/))처럼 환경의 전이 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)도 미리 알 필요가 없다. 대신 시행착오로 받은 보상을 바탕으로 상태-행동 [가치 함수](/knowledge-base/studynote/10_ai/02_dl_architecture_new/163_value_function/)를 점진적으로 고쳐 나간다.

이 방식이 필요한 이유는 현실의 의사결정 문제가 대부분 <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 보상 (Delayed Reward)</strong> 구조를 갖기 때문이다. 지금 한 행동은 즉시 보상이 0일 수 있지만, 몇 단계 뒤 큰 이득이나 큰 손실로 이어질 수 있다. 큐-러닝은 이 미래 가치를 현재 선택에 끌어와 반영함으로써, 단기 반응이 아니라 장기 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 학습하게 만든다.

아래 그림은 큐-러닝이 왜 필요한지, 즉 "지금의 선택이 나중 결과와 연결된다"는 점을 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│        큐-러닝이 푸는 문제: 지금 행동의 미래 가치를 추정        │
├──────────────────────────────────────────────────────────────┤
│ S0(출발) ──오른쪽──▶ S1 ──오른쪽──▶ Goal(+10)                │
│    │                                                         │
│    └──아래쪽──▶ Trap(-5)                                     │
│                                                              │
│ S0에서 '오른쪽'의 즉시 보상은 0일 수 있다.                    │
│ 그래도 두 단계 뒤 Goal(+10) 가능성이 높다면                  │
│ 현재 행동의 Q값은 크게 평가되어야 한다.                      │
└──────────────────────────────────────────────────────────────┘
```

즉, 큐-러닝은 "당장 받은 점수"만 보는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 아니라 "앞으로 벌어질 결과"를 현재 의사결정에 접어 넣는 방법이다. 이 특징 덕분에 미로 탐색, 게임 플레이, 로봇 경로 선택처럼 순차 의사결정이 필요한 문제에서 기본 기준점으로 자주 사용된다.

- **📢 섹션 요약 비유**: 큐-러닝은 골목길에서 바로 보이는 사탕보다, 두 블록 뒤에 있는 큰 놀이터를 기억하며 길을 고르는 아이와 같다. 지금 당장은 평범해 보여도 나중에 더 큰 즐거움으로 이어지는 길을 배우는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

큐-러닝의 핵심 저장소는 Q-테이블 (Q-Table)이다. 행에는 상태, 열에는 행동이 놓이고, 각 셀에는 해당 상태에서 해당 행동을 했을 때 기대되는 장기 가치가 기록된다. 학습 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 값은 거의 비어 있지만, 반복 경험을 통해 점점 더 현실적인 값으로 수렴한다.

업데이트는 벨만 최적 방정식 (Bellman Optimality Equation) 아이디어를 따른다. [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) `s`에서 행동 `a`를 하고 보상 `r`을 받은 뒤 다음 상태 `s'`로 이동했다면, 현재 Q값은 `r + γ max_a' Q(s', a')` 방향으로 조정된다. 여기서 `α`는 얼마나 빠르게 새 정보를 반영할지, `γ`는 미래 보상을 얼마나 중시할지 결정한다.

```text
Q(s, a) ← Q(s, a) + α [ r + γ max_a' Q(s', a') - Q(s, a) ]
```

아래 흐름은 에이전트가 값을 갱신하는 순환 구조를 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│              큐-러닝 학습 루프 (Learning Loop)               │
├──────────────────────────────────────────────────────────────┤
│ 현재 상태 s 관측                                             │
│      │                                                       │
│      ▼                                                       │
│ ε-탐욕 정책 (ε-Greedy Policy)으로 행동 a 선택                │
│      │                                                       │
│      ▼                                                       │
│ 환경이 보상 r, 다음 상태 s' 반환                             │
│      │                                                       │
│      ▼                                                       │
│ Q(s,a) 갱신: 현재 보상 + 다음 상태의 최대 기대가치 반영      │
│      │                                                       │
│      └────────────── 다음 상태 s'에서 반복 ──────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

| 요소 | 의미 | 설계 포인트 |
| :--- | :--- | :--- |
| Q-테이블 (Q-Table) | 상태-행동 가치 저장소 | 상태 수가 커지면 메모리 급증 |
| [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) `α` | 새 경험 반영 비율 | 너무 크면 불안정, 너무 작으면 학습 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| 할인율 `γ` | 미래 보상 반영 정도 | 1에 가까울수록 장기 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선호 |
| ε-탐욕 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)과 활용의 균형 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/), 후반에는 활용 비중 증가 |
| `max_a' Q(s', a')` | 다음 상태의 최적 행동 가정 | 오프-폴리시 ([Off-Policy](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/464_q_learning_off_policy/))의 핵심 |

여기서 중요한 점은 큐-러닝이 실제로 무엇을 했든 업데이트 시점에는 <strong>다음 상태에서 가장 좋은 행동</strong>을 기준으로 계산한다는 것이다. 그래서 에이전트가 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/) 과정에서 다소 엉뚱한 행동을 했더라도, 학습 자체는 최적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 방향으로 수렴하려고 한다. 이것이 큐-러닝이 오프-폴리시 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)되는 이유다.

- **📢 섹션 요약 비유**: 큐-러닝은 여행 가계부와 같다. 오늘은 길을 잘못 들어 택시비를 더 냈더라도, 가계부를 정리할 때는 "다음엔 가장 좋은 길로 가면 얼마를 아낄 수 있는지"까지 함께 적어 두는 방식이다.

---

## Ⅲ. 비교 및 연결

큐-러닝의 경계는 SARSA ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)-Action-Reward-[State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)-Action)와 비교할 때 가장 잘 드러난다. 두 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 모두 상태-행동 가치를 배우지만, 큐-러닝은 다음 상태의 **최대** Q값을 사용하고, SARSA는 실제로 선택한 다음 행동의 Q값을 사용한다. 따라서 큐-러닝은 더 공격적으로 최적해를 향하고, SARSA는 실제 행동 경로를 더 보수적으로 반영한다.

| 항목 | 큐-러닝 ([Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/)) | SARSA |
| :--- | :--- | :--- |
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 성격 | 오프-폴리시 ([Off-Policy](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/464_q_learning_off_policy/)) | 온-폴리시 (On-[Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)) |
| 업데이트 기준 | `max_a' Q(s', a')` | `Q(s', a')` |
| 성향 | 최적 행동을 가정하며 학습 | 실제 행동을 반영하며 학습 |
| 장점 | 빠른 수렴, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재활용 용이 | 위험한 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)을 더 현실적으로 반영 |
| 주의점 | 가치 과대평가 가능성 | 보수적이라 수렴이 느릴 수 있음 |

또 다른 경계는 표 기반 큐-러닝과 DQN의 차이다. 표 기반 방식은 상태가 수백~수천 개일 때 해석이 쉽고 안정적이지만, 이미지·센서·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 벡터처럼 상태가 커지면 테이블 자체를 만들 수 없다. 이때는 Q-테이블 대신 신경망이 Q함수를 근사하는 DQN으로 넘어간다.

즉, 큐-러닝은 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) 전체에서 <strong>출발점이자 <a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">기준선</a></strong> 역할을 한다. [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/) ([Markov Decision Process](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/)), [벨만 방정식](/knowledge-base/studynote/10_ai/05_data_science_ml/372_bellman_equation/), [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)-활용 균형, 함수 근사 확장이라는 주요 개념이 모두 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 주변에서 연결된다.

- **📢 섹션 요약 비유**: 큐-러닝과 SARSA의 차이는 운전 연습과 비슷하다. 큐-러닝은 "가장 이상적인 주행"을 기준으로 배우고, SARSA는 "내가 실제로 몰았던 서툰 주행"까지 그대로 반영해 더 조심스럽게 배우는 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 큐-러닝을 적용할지 판단할 때 가장 먼저 볼 것은 상태와 행동의 크기다. 예를 들어 20×20 격자 창고에서 로봇이 상·하·좌·우 네 방향만 선택한다면 상태는 400개, 행동은 4개이므로 Q-테이블 1,600칸이면 시작할 수 있다. 반면 자율주행처럼 카메라 입력과 연속 조향각이 들어오면 표 기반 접근은 즉시 한계에 도달한다.

또한 보상 설계와 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/) 안전성도 중요하다. 보상이 너무 희소하면 에이전트는 무엇이 좋은 행동인지 오랫동안 학습하지 못하고, [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)이 위험한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서는 실제 시스템에서 무작정 시행착오를 허용할 수 없다. 그래서 산업 현장에서는 시뮬레이터 학습, 안전 제약 필터, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 오프라인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 함께 붙인다.

### 적용 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 상태와 행동이 **이산적 (Discrete)** [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)?
2. Q-테이블 크기가 메모리와 학습 시간 안에 들어오는가?
3. 잘못된 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)이 실제 피해로 이어지지 않도록 시뮬레이션 또는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치가 있는가?
4. 보상이 너무 늦거나 희소하지 않도록 중간 피드백을 설계했는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 연속 제어 문제에 큐-러닝을 그대로 적용하려는 설계
- [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 노이즈를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 믿어 Q값 과대평가를 방치하는 설계
- 실환경에서 안전 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 공격적 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)을 허용하는 설계

이때 과대평가 문제가 크면 더블 [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/) (Double [Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)), 상태가 크면 [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/), [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어가 핵심이면 [PPO](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/) ([Proximal Policy Optimization](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/)) 같은 다른 계열로 전환하는 판단이 필요하다. 기술사 답안에서도 "큐-러닝은 언제 유효하고 언제 확장해야 하는가"를 함께 적어야 완성도가 높다.

- **📢 섹션 요약 비유**: 큐-러닝은 동네 보드게임에서는 최고 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)표가 되지만, 실제 도로처럼 변수가 너무 많아지면 종이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)표만 들고는 버틸 수 없다. 그때는 더 큰 지도와 더 똑똑한 보조 장치가 필요하다.

---

## Ⅴ. 기대효과 및 결론

큐-러닝의 가장 큰 장점은 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)의 핵심 원리를 작고 명확한 형태로 보여준다는 점이다. 상태-행동 가치, [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)과 활용, 벨만 기반 업데이트, 오프-폴리시 학습이라는 개념을 한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 안에서 모두 설명할 수 있다. 그래서 교육용 예제뿐 아니라 작은 제어 문제의 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 모델로도 여전히 의미가 크다.

반면 한계도 분명하다. 상태 공간이 커지면 메모리와 표본 수 요구가 폭증하고, 연속 행동 공간에서는 직접 적용하기 어렵다. 미래 확장 방향은 함수 근사, 경험 재플레이 ([Experience Replay](/knowledge-base/studynote/10_ai/02_dl_architecture_new/169_experience_replay/)), 더블 추정, 분포형 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)처럼 "큐-러닝 철학을 유지하면서 규모 문제를 해결하는 것"에 있다.

결국 큐-러닝은 "행동의 즉시 결과가 아니라 미래 가치까지 포함해 평가하는 법"으로 기억하면 된다. [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)의 많은 최신 기법은 형태만 달라졌을 뿐, 이 핵심 생각을 더 큰 문제로 확장한 결과물이다.

- **📢 섹션 요약 비유**: 큐-러닝은 작은 동네에서 길 찾는 법을 완벽히 익히게 해 주는 기본 지도다. 도시가 커지면 내비게이션으로 발전해야 하지만, 방향을 점수로 판단한다는 원리는 그대로 남는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MDP](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/) ([Markov Decision Process](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/)) | 상태, 행동, 보상, 전이로 큐-러닝 문제를 정의하는 수학적 틀 |
| 벨만 최적 방정식 (Bellman Optimality Equation) | 현재 가치가 즉시 보상과 미래 최적 가치로 구성된다는 업데이트 근거 |
| ε-탐욕 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) (ε-Greedy [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)) | [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)과 활용을 섞어 Q-테이블을 채우는 대표 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| SARSA | 온-폴리시 비교 대상으로 큐-러닝의 오프-폴리시 성격을 드러냄 |
| [DQN](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/) ([Deep Q-Network](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)) | 큰 상태 공간에서 Q함수를 신경망으로 근사한 확장형 |

### 📈 관련 키워드 및 발전 흐름도

```text
MDP (Markov Decision Process)
    │
    ▼
상태 가치 · 행동 가치 · 보상 설계
    │
    ▼
큐-러닝 (Q-Learning) · ε-탐욕 정책 (ε-Greedy Policy)
    │
    ▼
SARSA · 오프-폴리시/온-폴리시 비교
    │
    ▼
DQN (Deep Q-Network) · Double DQN · Deep RL
```

이 흐름도는 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)이 "작은 표 기반 문제"에서 출발해 "함수 근사 기반 대규모 문제"로 확장되는 경로를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큐-러닝은 미로 속에서 "이 칸에서 어느 쪽으로 가면 나중에 더 좋은 일이 생길까?"를 점수표로 적어 두는 방법이에요.
2. 처음에는 아무 점수도 모르니 이리저리 돌아다니지만, 좋은 길을 찾을수록 점수표가 점점 똑똑해져요.
3. 나중에는 점수가 가장 높은 화살표만 따라가도 목적지에 빨리 도착할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 167 / 420

← **이전**: [166. 엡실론-그리디 (Epsilon-Greedy)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/166_epsilon_greedy/)
**다음**: [168. 딥 큐 네트워크 (DQN)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/168_dqn/) →

---
