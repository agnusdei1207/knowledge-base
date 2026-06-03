---
title: 318. 정책 경사 (Policy Gradient)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[164_policy|정책]] 경사 ([[164_policy|Policy]] Gradient)는 Q값을 통해 행동을 간접 유도하는 Q-러닝과 달리, **[[164_policy|정책]]([[164_policy|Policy]]) π_θ(a|s)를 파라미터 θ로 직접 표현하고 기대 보상의 그래디언트로 [[164_policy|정책]] 파라미터를 직접 최적화**하는 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] 방법론이다.
> 2. **가치**: 연속 행동 공간(로봇 관절 토크, 자율주행 핸들 각도)에서 DQN이 불가능한 문제를 처리 가능하고, [[172_actor_critic|Actor-Critic]]([[155_ac_actual_cost|AC]]) 구조는 [[164_policy|정책]] 경사의 [[136_variance|분산]]([[136_variance|Variance]]) 문제를 [[163_value_function|가치 함수]](Critic)로 안정화하여 현대 Deep RL의 표준 구조가 됐다.
> 3. **판단 포인트**: [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]])에서 [[263_llm_large_language_model|LLM]] 정렬에 사용되는 [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]])가 Actor-Critic의 대표 [[001_algorithm_definition|알고리즘]]이며, ChatGPT·Claude·Gemini 모두 [[395_ppo_clipping|PPO]] 기반 RLHF로 정렬됐다는 것이 기술사 필수 지식이다.

---

## Ⅰ. 개요 및 필요성

로봇 팔이 공을 잡으려면 관절 토크를 연속 실수값으로 출력해야 한다. DQN은 "버튼 3번 누르기" 같은 이산 행동에만 적합하고, 이런 연속 제어에는 부적합하다. 또한 DQN은 Q값 최대화를 통해 [[164_policy|정책]]을 간접 유도하여, Q값 과대추정 등의 문제가 있다.

**[[164_policy|정책]] 경사([[164_policy|Policy]] Gradient)**는 [[164_policy|정책]] π_θ(a|s)를 신경망 파라미터 θ로 직접 모델링하고, 그래디언트 상승(Gradient Ascent)으로 기대 누적 보상 J(θ)를 직접 최대화한다. "직접 [[164_policy|정책]]을 학습"하는 것이 핵심 철학이다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: DQN이 "각 식당의 맛 점수표를 보고 가장 맛있는 곳을 선택"하는 것이라면, [[164_policy|정책]] 경사는 "식당 선택 습관 자체([[164_policy|정책]])를 직접 최적화"하는 것이다. 점수표 없이 "어떤 날, 어떤 기분에 어떤 종류 식당이 최고인가"를 직관적으로 학습해서 점점 더 만족스러운 선택 패턴을 발전시킨다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│         정책 경사 및 Actor-Critic 아키텍처                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  정책 경사 수식 (REINFORCE):                                        │
│  ∇J(θ) = E[Σ ∇ log π_θ(a|s) · G_t]                            │
│  θ ← θ + α · ∇J(θ)  (경사 상승, Gradient Ascent)                │
│                                                                  │
│  직관: 보상이 높은 행동(G_t 큰 경우)의 확률을 올려라!                │
│  문제: G_t의 분산이 커서 학습 불안정 (REINFORCE 의 단점)             │
│                                                                  │
│  Actor-Critic 구조 (A2C, A3C, PPO의 기반):                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  입력: 상태 s                                            │    │
│  │       │                                                 │    │
│  │  ┌────┴────────────────────────────┐                    │    │
│  │  │         공유 신경망 (Backbone)    │                    │    │
│  │  └────┬────────────────────────────┘                    │    │
│  │       ├─────────────────┐                               │    │
│  │  [Actor Head]     [Critic Head]                         │    │
│  │  π_θ(a|s)         V_φ(s)                                │    │
│  │  (정책, 행동 확률)   (가치, 상태 평가)                     │    │
│  │       │                 │                               │    │
│  │   행동 a 선택       어드밴티지 A(s,a) = R + γV(s') - V(s)  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  PPO (Proximal Policy Optimization):                            │
│  목표: L^CLIP = E[min(r_t(θ)·A_t, clip(r_t(θ), 1-ε, 1+ε)·A_t)]│
│  r_t = π_θ(a|s) / π_θ_old(a|s) (새 정책 / 이전 정책 비율)       │
│  클리핑으로 정책이 너무 급격히 변하지 않게 제한                      │
└──────────────────────────────────────────────────────────────────┘
```

| [[001_algorithm_definition|알고리즘]] | 특징 | 적합 환경 |
|:---|:---|:---|
| REINFORCE | 몬테카를로 [[164_policy|정책]] 경사, 에피소드 후 업데이트 | 단순 환경 |
| [[373_actor_critic_advantage|A2C]] (Advantage [[172_actor_critic|Actor-Critic]]) | 동기식 멀티-환경 학습, 어드밴티지 사용 | 보통 복잡도 |
| [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]]) | 클리핑으로 안정적 학습, 실무 표준 | 대부분 환경 |
| SAC (Soft [[172_actor_critic|Actor-Critic]]) | [[151_entropy|엔트로피]] [[093_normalization|정규화]], 연속 행동 최강 | 로봇 제어, 연속 행동 |

- **📢 섹션 요약 비유**: Actor-Critic은 야구의 투수(Actor)와 포수(Critic)다. 포수(Critic)는 현재 상황(상태 가치 V(s))을 평가해서 "지금 커브를 던지면 얼마나 유리한가(어드밴티지)"를 투수에게 알려준다. 투수(Actor)는 포수의 [[130_signal|신호]]를 받아 최적의 구종(행동 [[130_probability|확률]])을 선택한다. 둘이 협력해야 타자(환경)를 삼진 아웃(목표 달성)시킬 수 있다.

---

## Ⅲ. 비교 및 연결

**[[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]])**:
1. SFT (Supervised [[304_fine_tuning|Fine-Tuning]]): 이상적 응답으로 [[263_llm_large_language_model|LLM]] [[304_fine_tuning|파인 튜닝]]
2. [[403_rlhf_reward_model|Reward Model]] ([[197_rm_rate_monotonic_scheduling|RM]]) 학습: 인간 평가자의 선호도 순위로 보상 모델 학습
3. [[395_ppo_clipping|PPO]] 최적화: [[197_rm_rate_monotonic_scheduling|RM]] 보상을 최대화하도록 LLM을 PPO로 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]

ChatGPT, Claude, Gemini 모두 이 3단계 [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] [[123_pipe|파이프]]라인을 사용하여 "사람이 원하는" 방식으로 응답하도록 정렬(Alignment)됐다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [[009_config|설정]] | 작은 규모, 개념 학습 |
| [[164_policy|정책]] 경사 ([[164_policy|Policy]] Gradient) | [[282_performance_tactics|성능]]과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [[090_service_kubernetes_network_load_balancing|서비스]] 고도화 단계 |

- **📢 섹션 요약 비유**: RLHF는 [[190_ai_llm_requirements_specification|AI]] 신입사원 교육 3단계다. 1단계(SFT): "이상적인 업무 보고서(이상적 응답)"로 기초 교육, 2단계([[197_rm_rate_monotonic_scheduling|RM]]): "팀장들이 여러 보고서 중 어느 것이 더 좋은지(인간 선호도)"로 평가 기준 학습, 3단계([[395_ppo_clipping|PPO]]): "팀장 점수가 높은 보고서를 더 많이 쓰도록([[395_ppo_clipping|PPO]])" 반복 훈련. 이 세 단계가 신입사원을 최고 직원으로 만든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[395_ppo_clipping|PPO]] 하이퍼파라미터 설계**:
- `clip_range` ε: 0.1~0.2. [[164_policy|정책]] 변화 허용 범위. 클수록 빠르지만 불안정
- `n_steps`: 2048~4096. 업데이트 전 수집할 샘플 수. 클수록 [[136_variance|분산]] 감소
- `n_epochs`: 3~[[489_raid_10_hybrid|10]]. 같은 [[001_dikw_pyramid|데이터]]로 업데이트 반복 횟수
- `entropy_coeff`: 0.01~0.05. [[315_exploration_exploitation|탐험]] 촉진을 위한 [[151_entropy|엔트로피]] 보너스

**연속 제어에서 SAC 선택**: 로봇팔 조작, 드론 제어, 자율주행 등 연속 행동 공간에서는 PPO보다 SAC가 일반적으로 더 빠른 수렴과 높은 최종 [[282_performance_tactics|성능]]을 달성한다. SAC의 [[151_entropy|엔트로피]] 목표가 자동으로 [[315_exploration_exploitation|탐험]] 수준을 조절하는 장점이 있다.

- **📢 섹션 요약 비유**: PPO의 클리핑은 운전 교습소의 안전 규칙이다. 핸들을 너무 급격히 꺾으면([[164_policy|정책]]이 급변) 전복(학습 불안정) 위험이 있어서, "한 번에 최대 10도만 꺾어"(clip_range)라고 제한한다. 조금씩 안전하게 코너를 돌면서 점점 더 빠른 드라이버(최적 [[164_policy|정책]])가 된다.

---

## Ⅴ. 기대효과 및 결론

[[164_policy|정책]] 경사와 Actor-Critic은 Deep RL의 연속 제어 문제를 해결하고, RLHF를 통해 [[263_llm_large_language_model|LLM]] 정렬의 핵심이 됐다. PPO는 구현 단순성과 강건성 덕분에 OpenAI Gym부터 ChatGPT까지 거의 모든 RL 응용의 첫 번째 선택지로 자리 잡았다. Actor([[087_process_state_transition|생성]])와 Critic(평가)의 이중 구조는 GAN의 [[087_process_state_transition|생성]]자-판별자와 개념적으로 유사하며, "두 네트워크의 경쟁·협력으로 최적화"하는 철학이 현대 AI의 핵심 패턴으로 자리 잡고 있다.

- **📢 섹션 요약 비유**: Actor-Critic은 [[190_ai_llm_requirements_specification|AI]] 세계의 감독-배우 시스템이다. 감독(Critic)이 "이 연기는 70점"이라고 평가하면, 배우(Actor)는 더 좋은 점수를 받기 위해 연기를 개선한다. 감독과 배우가 함께 성장하면서 결국 아카데미상(최적 [[164_policy|정책]])에 도달한다. ChatGPT도 이 방식으로 "인간이 원하는 대답"을 배웠다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[164_policy|정책]] 경사 ([[164_policy|Policy]] Gradient) | ∇J(θ), 직접 [[164_policy|정책]] 최적화 / Actor-Critic의 이론적 기반 |
| [[172_actor_critic|Actor-Critic]] | [[164_policy|정책]] 네트워크 + 가치 네트워크 / [[164_policy|정책]] 경사의 [[136_variance|분산]] 문제 해결 구조 |
| [[395_ppo_clipping|PPO]] | 클리핑, 안정적 학습 / 실무 표준 [[172_actor_critic|Actor-Critic]] [[001_algorithm_definition|알고리즘]] |
| [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] | 인간 피드백, [[263_llm_large_language_model|LLM]] 정렬 / PPO를 [[263_llm_large_language_model|LLM]] 정렬에 적용한 패러다임 |
| SAC | [[151_entropy|엔트로피]] [[093_normalization|정규화]], 연속 행동 / 로봇 제어에서 PPO와 경쟁하는 [[001_algorithm_definition|알고리즘]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [정책 경사 (Policy Gradient)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **[[164_policy|정책]] 경사**는 Q값 표 대신 **"이 상황에서 이 행동을 할 [[130_probability|확률]]"을 직접 신경망으로 배우는** 방법으로, 버튼 고르기가 아닌 **핸들 각도(연속값)** 결정에 딱 맞아요!
2. **[[172_actor_critic|Actor-Critic]]**은 행동을 결정하는 배우(Actor)와 "그 행동이 얼마나 좋았나" 평가하는 감독(Critic)이 협력하는 구조예요.
3. **ChatGPT가 좋은 대답을 하도록 훈련**한 RLHF도 이 [[172_actor_critic|Actor-Critic]]([[395_ppo_clipping|PPO]]) 방식이에요!
