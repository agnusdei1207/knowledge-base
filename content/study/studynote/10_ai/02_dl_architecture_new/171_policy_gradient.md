---
title: 171. 정책 경사법 (Policy Gradient)
date: '2026-04-17'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[318_policy_gradient_actor_critic|정책 경사]]법 ([[318_policy_gradient_actor_critic|Policy Gradient]])은 행동가치 함수 `Q(s, a)`를 우회해, [[164_policy|정책]] `πθ(a|s)` 자체를 파라미터화하고 기대 보상 `J(θ)`를 직접 최대화하는 강화학습 방법이다.
> 2. **가치**: 행동을 [[130_probability|확률]] 분포로 다루기 때문에 연속 제어와 [[130_probability|확률]]적 [[268_strategy_pattern|전략]]이 자연스럽고, "어떤 행동이 얼마나 자주 나와야 하는가"를 직접 설계할 수 있다.
> 3. **판단 포인트**: 순수 REINFORCE는 [[136_variance|분산]]이 커서 실무 안정성이 낮으므로, [[159_baseline_requirements_configuration_management|베이스라인]]·어드밴티지·[[172_actor_critic|액터-크리틱]] ([[172_actor_critic|Actor-Critic]])·[[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]]) 같은 [[136_variance|분산]] 저감 장치와 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

[[318_policy_gradient_actor_critic|정책 경사]]법은 상태를 입력받아 행동의 [[130_probability|확률]] 분포를 바로 출력하는 강화학습 계열이다. 가치 기반 방법인 Q-러닝 ([[316_q_learning|Q-Learning]])이나 [[465_dqn_deep_q_network|DQN]] ([[465_dqn_deep_q_network|Deep Q-Network]])은 각 행동의 점수를 계산한 뒤 최고 점수 행동을 고르는 구조라서, 행동 후보가 몇 개 안 되는 이산 공간에서는 강력하다. 그러나 로봇 관절 각도, 드론 추력, 자율주행 조향각처럼 연속적으로 변하는 행동 공간에서는 점수표를 전부 계산하는 방식이 금방 비효율적이 된다.

또 하나의 이유는 최적 행동이 항상 하나의 고정 답이 아닐 수 있다는 점이다. 포커, 경매, 다중 에이전트 게임처럼 상대가 내 패턴을 읽는 환경에서는 일부러 행동 [[130_probability|확률]]을 섞는 혼합 [[268_strategy_pattern|전략]]이 필요하다. [[318_policy_gradient_actor_critic|정책 경사]]법은 이 [[130_probability|확률]] 자체를 학습 대상으로 삼기 때문에, "가끔은 다른 행동을 해야 이긴다"는 문제를 더 직접적으로 다룬다.

아래 그림은 가치 기반과 [[164_policy|정책]] 기반의 차이를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Value-based vs Policy-based decision                                 │
├──────────────────────────────┬──────────────────────────────────────┤
│ state s                      │ state s                              │
│   │                          │   │                                  │
│   ▼                          │   ▼                                  │
│ Q(s,a1), Q(s,a2), ...        │ πθ(a1|s), πθ(a2|s), ...             │
│   │                          │   │                                  │
│ argmax action                │ sample / choose from distribution    │
│ best for finite actions      │ natural for stochastic/continuous    │
└──────────────────────────────┴──────────────────────────────────────┘
```

즉 [[318_policy_gradient_actor_critic|정책 경사]]법은 "점수표를 잘 맞히는 문제"에서 "행동 [[130_probability|확률]]을 잘 조정하는 문제"로 초점을 바꾼다. 이 전환 덕분에 강화학습의 표현력은 커지지만, 대신 학습 [[130_signal|신호]]의 [[136_variance|분산]]을 어떻게 낮출지가 핵심 과제가 된다.

- **📢 섹션 요약 비유**: 가치 기반은 식당마다 점수를 매겨 항상 1등 가게만 가는 방식이고, [[318_policy_gradient_actor_critic|정책 경사]]법은 상황과 분위기에 따라 "오늘은 이 메뉴 70%, 저 메뉴 30%"처럼 선택 [[130_probability|확률]] 자체를 조절하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[318_policy_gradient_actor_critic|정책 경사]]법의 출발점은 [[164_policy|정책]]을 파라미터 `θ`를 가진 신경망으로 두고, 기대 누적 보상 `J(θ)`를 최대화하는 것이다. 대표적인 기본형이 REINFORCE이며, 한 에피소드에서 얻은 궤적 `(s_t, a_t, r_t)`를 모은 뒤 각 시점의 할인 누적 보상 `G_t`를 계산해 [[164_policy|정책]]을 업데이트한다. 실무 프레임워크에서는 보통 최대화 대신 손실 최소화를 쓰므로 `-log πθ(a_t|s_t) * G_t` 형태의 loss로 구현한다.

### 핵심 업데이트 직관

- 목적 함수: `J(θ) = E[Σ γ^t r_t]`
- 기본 업데이트: `θ ← θ + α Σ ∇θ log πθ(a_t|s_t) G_t`
- [[136_variance|분산]] 저감형: `θ ← θ + α Σ ∇θ log πθ(a_t|s_t) (G_t - b_t)`

여기서 `b_t`는 [[159_baseline_requirements_configuration_management|베이스라인]] ([[025_baseline|Baseline]])이다. 평균적인 기대치만큼은 빼고, 그보다 더 잘했는지 못했는지만 반영해 [[136_variance|분산]]을 줄인다. 이 아이디어가 더 발전하면 어드밴티지 (Advantage)와 [[172_actor_critic|액터-크리틱]] 계열로 이어진다.

아래 그림은 학습 루프를 [[347_compaction|압축]]한 것이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Policy Gradient training loop                                        │
├──────────────────────────────────────────────────────────────────────┤
│ state s_t ──> policy πθ(a|s) ──> sample action a_t                  │
│      ▲                              │                                │
│      │                              ▼                                │
│ next state s_{t+1} <── environment reward r_t                       │
│                                                                      │
│ trajectory {s,a,r} ──> discounted return G_t                         │
│                               │                                      │
│                               └─> ∇θ log πθ(a_t|s_t) · G_t           │
│                                          │                           │
│                                          └─ update θ                 │
└──────────────────────────────────────────────────────────────────────┘
```

[[164_policy|정책]] 네트워크의 출력 형태는 행동 공간에 따라 달라진다. 이산 행동이면 [[270_softmax|softmax]] [[130_probability|확률]]을, 연속 행동이면 가우시안 분포의 평균 `μ`와 표준편차 `σ`를 내보내는 식이 흔하다. 즉 [[318_policy_gradient_actor_critic|정책 경사]]법은 단순히 "왼쪽/오른쪽"을 고르는 모델이 아니라, **행동 분포의 모양 자체를 학습하는 모델**이다.

| 행동 공간 | [[164_policy|정책]] 출력 예 | 장점 | 주의점 |
| :--- | :--- | :--- | :--- |
| 이산 행동 | [[270_softmax|softmax]] [[130_probability|확률]] | [[315_exploration_exploitation|탐험]]과 활용을 한 분포로 표현 | [[130_probability|확률]] 붕괴 시 [[315_exploration_exploitation|탐험]] 부족 |
| 연속 행동 | Gaussian `μ`, `σ` | 부드러운 제어 가능 | 범위 제한, [[136_variance|분산]] 튜닝 필요 |
| 제한된 연속 구간 | Beta 분포 등 | 행동 범위 내 샘플링 쉬움 | 구현 복잡도 증가 |

- **📢 섹션 요약 비유**: [[318_policy_gradient_actor_critic|정책 경사]]법은 시험이 끝난 뒤 "이번에 맞힌 답은 더 자주 쓰고, 틀린 답은 덜 쓰자"고 습관을 교정하는 방식이다. 정답표를 외우는 게 아니라, 선택하는 버릇 자체를 바꾸는 훈련이다.

---

## Ⅲ. 비교 및 연결

[[318_policy_gradient_actor_critic|정책 경사]]법을 제대로 이해하려면 가치 기반, 순수 [[164_policy|정책]] 기반, 그리고 그 절충형을 함께 봐야 한다. 같은 강화학습이라도 "무엇을 학습하느냐"가 다르기 때문이다.

| 구분 | 가치 기반 ([[465_dqn_deep_q_network|DQN]]) | [[318_policy_gradient_actor_critic|정책 경사]]법 (REINFORCE) | [[172_actor_critic|액터-크리틱]] |
| :--- | :--- | :--- | :--- |
| 직접 학습 대상 | 행동가치 `Q(s,a)` | [[164_policy|정책]] `πθ(a|s)` | [[164_policy|정책]] + 가치함수 |
| 행동 공간 | 주로 이산 | 이산·연속 모두 가능 | 이산·연속 모두 가능 |
| [[315_exploration_exploitation|탐험]] 방식 | ε-greedy 등 별도 설계 | [[164_policy|정책]] 분포 내부에 내장 | [[164_policy|정책]] 분포 + 가치 평가 |
| 샘플 효율 | 비교적 좋음 | 낮은 편 | 중간 이상 |
| 핵심 위험 | 과대추정, moving target | 높은 [[136_variance|분산]] | 학습 불균형 |

순수 [[318_policy_gradient_actor_critic|정책 경사]]법은 개념이 깔끔하지만, 좋은 보상을 얻은 긴 궤적 전체를 한꺼번에 칭찬하거나 벌하기 때문에 [[136_variance|분산]]이 크다. 그래서 실제 연구와 산업에서는 가치함수를 함께 두는 [[172_actor_critic|액터-크리틱]], 일반화된 어드밴티지 추정 (GAE, Generalized Advantage Estimation), [[395_ppo_clipping|PPO]] 같은 구조로 진화했다. 즉 현대 강화학습의 핵심은 [[318_policy_gradient_actor_critic|정책 경사]] 철학을 유지하되, **학습 [[130_signal|신호]]를 얼마나 안정적으로 만들 것인가**에 있다.

또한 연속 제어에서는 결정론적 [[318_policy_gradient_actor_critic|정책 경사]] (Deterministic [[318_policy_gradient_actor_critic|Policy Gradient]]) 계열도 중요하다. DDPG (Deep Deterministic [[318_policy_gradient_actor_critic|Policy Gradient]]), TD3 (Twin Delayed DDPG) 등은 [[318_policy_gradient_actor_critic|정책 경사]] 사상을 유지하면서도 샘플 효율과 안정성을 보강한 변형으로 볼 수 있다.

- **📢 섹션 요약 비유**: 순수 [[318_policy_gradient_actor_critic|정책 경사]]법은 감각은 뛰어나지만 기복이 큰 선수이고, 가치 기반은 계산은 정확하지만 움직임이 둔한 선수다. [[172_actor_critic|액터-크리틱]]은 감각 좋은 선수 옆에 실시간 코치를 붙여 둘의 장점을 섞은 팀 전술에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[318_policy_gradient_actor_critic|정책 경사]]법은 로보틱스, 게임 [[190_ai_llm_requirements_specification|AI]], 자율 제어, 인간 선호 정렬 같은 영역에서 널리 쓰인다. 다만 실무에서는 "[[318_policy_gradient_actor_critic|정책 경사]]법을 쓸 것인가"보다 "어떤 안정화 장치를 함께 둘 것인가"가 더 중요한 질문이다. 예를 들어 연속 제어에서 처음부터 순수 REINFORCE를 쓰는 경우는 드물고, 보통 PPO나 [[172_actor_critic|액터-크리틱]] 기반 [[001_algorithm_definition|알고리즘]]으로 출발한다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. 행동 공간이 연속적이거나, [[130_probability|확률]]적 [[164_policy|정책]] 자체가 문제 정의에 중요한가?
2. [[164_policy|정책]] 출력이 실제 행동 범위와 맞는가? 예: 조향각 제한, 토크 상한, [[130_probability|확률]] 합 1.
3. 어드밴티지 [[093_normalization|정규화]], 리워드 [[249_scaling_normalization_standardization|스케일링]], [[151_entropy|엔트로피]] 보너스 ([[151_entropy|Entropy]] Bonus) 같은 [[136_variance|분산]] 제어 장치를 넣었는가?
4. KL 발산 ([[347_cross_entropy_kld|Kullback-Leibler Divergence]]), [[164_policy|정책]] [[151_entropy|엔트로피]], 평균 리턴을 함께 [[229_monitor|모니터]]링하고 있는가?
5. [[090_service_kubernetes_network_load_balancing|서비스]]/제품 단계라면 순수 [[318_policy_gradient_actor_critic|정책 경사]]법보다 PPO나 [[395_verification_process_review|검증]]된 [[172_actor_critic|액터-크리틱]] 계열이 더 적합하지 않은가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 학습 중에도 항상 argmax만 사용해 [[164_policy|정책]] 분포가 사실상 [[315_exploration_exploitation|탐험]]하지 못하게 만드는 것
- 연속 행동에서 평균만 출력하고 [[136_variance|분산]]을 고정하지 않아 행동 다양성이 사라지는 것
- [[159_baseline_requirements_configuration_management|베이스라인]] 없이 긴 에피소드 전체를 한 번에 강화해 [[136_variance|분산]]이 폭증하는 것
- 큰 [[080_gradient_descent_learning_rate|학습률]]로 [[164_policy|정책]]을 급격히 바꿔 [[164_policy|정책]] 붕괴 ([[164_policy|Policy]] Collapse)를 일으키는 것

언어 모델 정렬에서도 같은 철학이 보인다. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]])는 사람 선호를 보상 [[130_signal|신호]]로 바꿔 [[164_policy|정책]]을 조정하는데, 이 역시 "행동 [[130_probability|확률]]을 원하는 방향으로 밀어준다"는 점에서 [[318_policy_gradient_actor_critic|정책 경사]]적 사고를 따른다. 다만 실제 시스템은 KL 제약, 보상 모델, 배치 안정성 같은 추가 안전장치가 필수다.

- **📢 섹션 요약 비유**: [[318_policy_gradient_actor_critic|정책 경사]]법을 실전에 쓰는 일은 본능 좋은 신입 사원에게 바로 전권을 주는 일이 아니다. 좋은 피드백 체계, 행동 범위, 평가 기준을 함께 붙여야 본능이 실력으로 바뀐다.

---

## Ⅴ. 기대효과 및 결론

[[318_policy_gradient_actor_critic|정책 경사]]법의 가장 큰 효과는 강화학습이 직접 행동 분포를 다루게 했다는 점이다. 덕분에 [[130_probability|확률]]적 [[268_strategy_pattern|전략]], 연속 제어, [[133_fine_tuning|미세 조정]]이 필요한 문제를 한 프레임 안에서 설명할 수 있게 됐다. 특히 "무엇을 할 것인가"뿐 아니라 "얼마나 자주 그렇게 할 것인가"를 학습한다는 점이 가치 기반 접근과의 본질적 차이다.

반면 비용도 있다. 샘플 효율이 낮고, 보상 설계에 민감하며, [[136_variance|분산]]과 안정화 문제가 늘 따라온다. 그래서 현대 실무에서는 [[318_policy_gradient_actor_critic|정책 경사]]법을 단독 [[001_algorithm_definition|알고리즘]]이라기보다, [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]]), [[373_actor_critic_advantage|A2C]] (Advantage [[172_actor_critic|Actor-Critic]]), [[173_a3c_ppo|A3C]] ([[173_a3c_ppo|Asynchronous Advantage Actor-Critic]]), SAC (Soft [[172_actor_critic|Actor-Critic]]) 같은 계열의 출발 철학으로 보는 것이 더 정확하다.

결론적으로 [[318_policy_gradient_actor_critic|정책 경사]]법은 **행동 점수표를 간접적으로 맞히는 대신, 행동 [[130_probability|확률]] 자체를 직접 훈련하는 강화학습 원리**로 기억하면 된다. 이 원리를 이해하면 왜 연속 제어와 인간 선호 정렬에서 [[164_policy|정책]] 기반 계열이 강한지 자연스럽게 연결된다.

- **📢 섹션 요약 비유**: [[318_policy_gradient_actor_critic|정책 경사]]법은 정답 노트를 외우는 공부가 아니라, 상황을 보고 적절한 선택이 몸에 배도록 습관을 훈련하는 공부법이다. 잘만 다듬으면 복잡한 상황에서도 몸이 먼저 자연스럽게 반응한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[164_policy|정책]] ([[164_policy|Policy]]) | 상태를 행동 [[130_probability|확률]] 분포로 바꾸는 직접 대상 |
| [[163_value_function|가치 함수]] ([[163_value_function|Value Function]]) | [[159_baseline_requirements_configuration_management|베이스라인]]과 [[172_actor_critic|액터-크리틱]]으로 이어지는 보조 평가 기준 |
| 어드밴티지 (Advantage) | 평균 수준 대비 얼마나 더 잘했는지 계산해 [[136_variance|분산]]을 낮춤 |
| [[151_entropy|엔트로피]] 보너스 ([[151_entropy|Entropy]] Bonus) | [[164_policy|정책]]이 너무 빨리 확정되지 않도록 [[315_exploration_exploitation|탐험]]성을 유지 |
| [[172_actor_critic|액터-크리틱]] ([[172_actor_critic|Actor-Critic]]) | [[318_policy_gradient_actor_critic|정책 경사]]와 가치 추정을 결합한 안정화 구조 |
| [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]]) | [[164_policy|정책]] 업데이트 폭을 제한해 실무 안정성을 높인 대표 계열 |

### 📈 관련 키워드 및 발전 흐름도

```text
MDP (Markov Decision Process)
        │
        ▼
Policy network πθ(a|s)
        │
        ▼
REINFORCE
        │
        ▼
Baseline / Advantage
        │
        ▼
Actor-Critic family
        │
        ▼
PPO · continuous control · RLHF
```

이 흐름은 [[318_policy_gradient_actor_critic|정책 경사]]법이 순수 [[130_probability|확률]] [[164_policy|정책]] 학습에서 출발해, [[136_variance|분산]] 저감과 안정화 장치를 더하며 현대 강화학습 핵심 계열로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[318_policy_gradient_actor_critic|정책 경사]]법은 로봇이 "이럴 때는 이런 행동을 해 볼 [[130_probability|확률]]"을 몸으로 배우는 연습이에요.
2. 잘된 행동은 다음에 더 자주 하도록 하고, 잘못된 행동은 덜 하도록 습관을 조금씩 고쳐요.
3. 그래서 정답표를 외우지 않아도, 비슷한 상황이 오면 몸이 자연스럽게 좋은 선택을 하게 돼요.
