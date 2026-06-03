---
title: 173. A3C (Asynchronous Advantage Actor-Critic) 및 PPO (Proximal Policy Optimization)
date: '2026-04-17'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: A3C (Asynchronous Advantage [[172_actor_critic|Actor-Critic]])는 여러 워커가 비동기로 경험을 수집해 [[172_actor_critic|액터-크리틱]] 학습을 확장한 방법이고, [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]])는 [[164_policy|정책]]이 한 번에 너무 멀리 움직이지 않도록 제한해 학습을 안정화한 방법이다.
> 2. **가치**: A3C는 "경험 수집 병목"을, PPO는 "[[164_policy|정책]] 붕괴와 과도한 업데이트"를 줄여 현대 강화학습을 연구실 실험에서 실무형 학습 [[123_pipe|파이프]]라인으로 끌어올렸다.
> 3. **판단 포인트**: A3C는 [[430_index_fast_full_scan|병렬]] [[315_exploration_exploitation|탐험]] 구조가 핵심이고 PPO는 업데이트 안전장치가 핵심이므로, [[001_dikw_pyramid|데이터]] 수집이 문제인지 [[164_policy|정책]] 안정성이 문제인지 먼저 구분해야 올바른 [[001_algorithm_definition|알고리즘]]을 고를 수 있다.

---

## Ⅰ. 개요 및 필요성

A3C와 PPO는 [[172_actor_critic|액터-크리틱]] ([[172_actor_critic|Actor-Critic]]) 계열이 부딪힌 두 가지 대표 병목을 해결한 [[001_algorithm_definition|알고리즘]]이다. [[459_quic_fec_forward_error_correction|초기]] [[171_policy_gradient|정책 경사법]]은 보상이 늦고 [[136_variance|분산]]이 커서 학습이 쉽게 흔들렸고, [[465_dqn_deep_q_network|DQN]] ([[465_dqn_deep_q_network|Deep Q-Network]])은 연속 행동 제어나 큰 [[164_policy|정책]] 분포를 직접 다루는 데 한계가 있었다. [[172_actor_critic|액터-크리틱]]이 행동 [[087_process_state_transition|생성]]과 가치 평가를 분리해 문제를 줄였지만, 여전히 한쪽에는 경험 수집 속도 문제가, 다른 한쪽에는 [[164_policy|정책]] 업데이트 폭주 문제가 남아 있었다.

A3C는 2016년 DeepMind가 제안해, 여러 워커가 서로 다른 환경을 [[430_index_fast_full_scan|병렬]]로 [[315_exploration_exploitation|탐험]]하며 중앙 [[164_policy|정책]]을 비동기로 갱신하는 방식을 보였다. 이어 2017년 OpenAI가 제안한 PPO는 TRPO (Trust Region [[164_policy|Policy]] Optimization)의 "[[164_policy|정책]]을 너무 멀리 움직이지 말라"는 아이디어를 더 단순한 1차 최적화 형태로 바꿔, 구현 난이도와 안정성의 균형을 크게 개선했다. 그래서 강화학습의 역사에서 A3C는 **확장성의 전환점**, PPO는 **실용성의 전환점**으로 자주 묶여 설명된다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Why A3C and PPO mattered                                             │
├──────────────────────────────────────────────────────────────────────┤
│ Policy Gradient                                                      │
│   ├─ high variance                                                   │
│   └─ slow single-worker sampling                                     │
│        │                                                             │
│        ▼                                                             │
│ Actor-Critic                                                         │
│   ├─ better evaluation signal                                        │
│   ├─ but sampling bottleneck remains  -> A3C                         │
│   └─ but update instability remains -> TRPO -> PPO                   │
└──────────────────────────────────────────────────────────────────────┘
```

즉 두 [[001_algorithm_definition|알고리즘]]은 같은 가계도에 있지만 해결하는 pain point가 다르다. A3C는 "여러 명이 동시에 경험을 모으게 하자"는 답이고, PPO는 "[[164_policy|정책]]이 급발진하지 않게 안전벨트를 매자"는 답이다.

- **📢 섹션 요약 비유**: A3C는 선수 한 명 대신 여러 선수가 동시에 연습하게 만든 훈련 체계이고, PPO는 코치가 "폼은 한 번에 너무 많이 바꾸지 마"라고 교정 폭을 제한하는 규칙과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

A3C의 핵심은 여러 워커가 각자 환경과 상호작용하면서 로컬 네트워크로 경험을 쌓고, 그 기울기를 글로벌 네트워크에 비동기로 반영하는 구조다. 이 방식은 한 워커의 연속 경험만 보는 것보다 샘플 상관관계를 줄이고, 재현 버퍼 없이도 다양한 상태를 빠르게 모으게 해 준다. 대신 업데이트 시점이 완전히 [[212_synchronization_mechanisms|동기화]]되지 않기 때문에, 어떤 워커는 이미 오래된 [[164_policy|정책]]으로 [[001_dikw_pyramid|데이터]]를 모아 약간의 stale gradient를 보낼 수 있다.

PPO의 핵심은 [[001_dikw_pyramid|데이터]]를 모으는 방식보다 **업데이트를 제한하는 목적 함수**에 있다. 보통 rollout을 모은 뒤 어드밴티지 추정값을 계산하고, `r_t = π_new(a_t|s_t) / π_old(a_t|s_t)` 비율이 너무 커지거나 작아지면 `clip(r_t, 1-ε, 1+ε)`로 잘라낸다. 여기서 `ε`는 흔히 0.1~0.2 수준이며, [[164_policy|정책]]이 한 번에 급격히 이동하는 것을 막는다. PPO는 여기에 가치 손실, [[151_entropy|엔트로피]] 보너스, GAE (Generalized Advantage Estimation) 같은 보조 장치를 결합해 안정성을 높인다.

```text
┌──────────────────────────────┬───────────────────────────────────────┐
│ A3C                          │ PPO                                   │
├──────────────────────────────┼───────────────────────────────────────┤
│ worker_1 -> env -> grad ----┐│ rollout with π_old                    │
│ worker_2 -> env -> grad ----┼┼-> advantage estimate                 │
│ worker_n -> env -> grad ----┘│        │                              │
│                │             │        ▼                              │
│                ▼             │ ratio r_t = π_new / π_old             │
│         global parameters    │        │                              │
│                ▲             │        ▼                              │
│         sync local copy      │ clipped objective + mini-batch epochs │
│ solved bottleneck: sampling  │ solved bottleneck: unstable updates   │
└──────────────────────────────┴───────────────────────────────────────┘
```

| 항목 | A3C | [[395_ppo_clipping|PPO]] |
| :--- | :--- | :--- |
| [[001_dikw_pyramid|데이터]] 수집 | 다중 워커 비동기 on-[[164_policy|policy]] 수집 | 벡터 환경 또는 동기 rollout 수집 |
| 업데이트 방식 | 워커별 비동기 gradient 반영 | 클리핑 기반 mini-batch 반복 학습 |
| 강점 | [[430_index_fast_full_scan|병렬]] [[315_exploration_exploitation|탐험]], CPU (Central Processing Unit) 친화성 | 안정성, 구현 단순성, 재현성 |
| 약점 | stale gradient, [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 활용 비효율 | on-policy라 샘플 재사용 한계 존재 |
| 대표 활용 | [[430_index_fast_full_scan|병렬]] 시뮬레이션, 경량 연구 환경 | 로보틱스, 게임, [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]]) |

A3C가 경험 수집을 [[136_variance|분산]]해 학습을 전진시켰다면, PPO는 TRPO의 신뢰 영역 철학을 더 가볍게 구현해 실무 표준이 되었다. 그래서 현대 [[123_pipe|파이프]]라인은 A3C의 정신을 계승한 [[136_variance|분산]] 수집 구조를 쓰면서도, 실제 업데이트는 [[395_ppo_clipping|PPO]] 계열로 수행하는 경우가 많다.

- **📢 섹션 요약 비유**: A3C가 여러 [[315_exploration_exploitation|탐험]]대를 동시에 현장에 보내는 지휘 체계라면, PPO는 보고를 받았을 때 본부가 [[164_policy|정책]]을 너무 급하게 바꾸지 않도록 브레이크를 거는 장치다.

---

## Ⅲ. 비교 및 연결

A3C와 PPO를 비교할 때는 "누가 더 최신인가"보다 "무엇을 제어하는가"를 봐야 한다. A3C는 비동기 [[430_index_fast_full_scan|병렬]]성으로 샘플 다양성을 확보했고, TRPO는 Kullback-Leibler (KL) 거리 제약으로 [[164_policy|정책]] 이동 폭을 엄격히 통제했으며, PPO는 그 통제를 더 단순한 클리핑과 KL penalty 형태로 바꿨다. 따라서 A3C와 PPO는 경쟁 [[083_relationship_in_er_model|관계]]라기보다, **[[430_index_fast_full_scan|병렬]]화와 안정화라는 서로 다른 축의 해법**이다.

| [[001_algorithm_definition|알고리즘]] | 핵심 제어 축 | 장점 | 한계 |
| :--- | :--- | :--- | :--- |
| A3C | 비동기 워커 [[430_index_fast_full_scan|병렬]]성 | 다양한 경험, 재현 버퍼 없이도 학습 가능 | 업데이트 시점 불일치, 하드웨어 활용 한계 |
| TRPO | 명시적 신뢰 영역 제약 | 이론적으로 보수적이고 안정적 | 구현 복잡, 2차 최적화 부담 |
| [[395_ppo_clipping|PPO]] | 클리핑 또는 KL penalty 기반 근접 업데이트 | 단순 구현, 높은 안정성, 실무 채택 폭 넓음 | 여전히 on-policy라 샘플 비용이 큼 |

이 연결은 오늘날 [[136_variance|분산]]형 [[395_ppo_clipping|PPO]], [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]], 대규모 로보틱스 학습에서도 이어진다. 예를 들어 언어 모델 정렬에서는 PPO의 "기존 [[164_policy|정책]]에서 너무 멀어지지 않기" 철학이 [[116_reference_model|참조 모델]] KL 제약으로 변형되어 사용된다. 반대로 A3C의 아이디어는 여러 환경 인스턴스를 [[430_index_fast_full_scan|병렬]]로 굴리는 벡터 환경, actor-learner 분리 구조, [[136_variance|분산]] rollout 시스템으로 확장되었다.

따라서 시험 답안에서는 "A3C는 [[136_variance|분산]] 경험 수집의 이정표, PPO는 안정적인 [[164_policy|정책]] 최적화의 표준"이라고 구분하면 경계가 분명해진다. 같은 [[172_actor_critic|액터-크리틱]] 계열이라도 어디에 혁신이 있었는지 보여 주는 것이 핵심이다.

- **📢 섹션 요약 비유**: A3C는 더 많은 정찰병을 보내 전장을 빨리 파악하는 방법이고, PPO는 작전 계획을 한 번에 뒤집지 않도록 본부 회의 규칙을 세우는 방법이다. 둘 다 승리에 필요하지만 다루는 지점이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 새로운 강화학습 [[123_pipe|파이프]]라인을 설계할 때는 [[001_algorithm_definition|알고리즘]] 이름보다 운영 조건을 먼저 봐야 한다. 시뮬레이터가 빠르고 [[430_index_fast_full_scan|병렬]] 실행이 쉽다면 A3C나 그 후속 구조가 경험 수집 속도를 끌어올리는 데 유리하다. 반면 안정적 튜닝, 재현 가능한 실험, mini-batch 기반 학습, [[164_policy|정책]] 품질 [[229_monitor|모니터]]링이 중요하다면 PPO가 더 현실적인 기본 선택이 된다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. 환경 인스턴스를 여러 개 [[430_index_fast_full_scan|병렬]] 실행할 수 있는가, 아니면 실제 장비라 샘플이 비싼가?
2. [[164_policy|정책]]이 급격히 무너지는 현상이 있는가? 있다면 PPO의 클리핑·KL 제어가 우선이다.
3. PPO에서 KL, [[408_clip|clip]] fraction, [[151_entropy|entropy]], value loss를 함께 [[229_monitor|모니터]]링하고 있는가?
4. A3C라면 워커 [[164_policy|정책]]이 너무 오래 stale되지 않도록 [[212_synchronization_mechanisms|동기화]] 주기를 관리하는가?
5. on-[[164_policy|policy]] [[001_dikw_pyramid|데이터]] 비용이 지나치게 크다면, PPO를 고집하기보다 오프폴리시 계열을 검토해야 하는가?

### 적용 시나리오

| 상황 | 더 적합한 선택 | 이유 |
| :--- | :--- | :--- |
| 다수의 CPU 시뮬레이터를 빠르게 돌리는 연구 환경 | A3C 계열 | [[430_index_fast_full_scan|병렬]] [[315_exploration_exploitation|탐험]]과 구현 단순성이 강점 |
| 로봇 제어, 게임 [[190_ai_llm_requirements_specification|AI]], 일반 [[164_policy|정책]] 최적화의 [[025_baseline|기준선]] | [[395_ppo_clipping|PPO]] | 안정성, 튜닝 경험치, 재현성 확보가 쉬움 |
| [[263_llm_large_language_model|LLM]] ([[263_llm_large_language_model|Large Language Model]]) 정렬·선호 학습 | [[395_ppo_clipping|PPO]] 계열 | 기준 [[164_policy|정책]]에서 멀어지지 않는 제어가 중요 |

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- PPO에서 같은 rollout을 너무 많은 epoch로 재사용해 사실상 on-[[164_policy|policy]] 가정을 깨는 것
- 평균 리턴만 보고 KL, [[151_entropy|entropy]], value error를 무시하는 것
- A3C에서 워커 수만 늘리고 글로벌 모델 [[212_synchronization_mechanisms|동기화]] 비용을 관리하지 않는 것
- 샘플이 매우 비싼 문제에 PPO를 기본값처럼 적용하는 것

기술사 답안에서는 "PPO가 무조건 우월하다"고 [[289_cqrs_db|쓰기]]보다, **A3C는 수집 구조 혁신, PPO는 업데이트 안정화 혁신**이라고 분리해 적는 편이 좋다. 그래야 [[430_index_fast_full_scan|병렬]]성, 안정성, 샘플 효율의 세 축을 기준으로 설계 판단을 설명할 수 있다.

- **📢 섹션 요약 비유**: 연습생을 많이 뽑는 것과 훈련 규칙을 잘 만드는 것은 다른 문제다. A3C는 연습생 숫자를 늘리는 쪽이고, PPO는 훈련 도중 무리해서 다치지 않게 코칭 강도를 조절하는 쪽이다.

---

## Ⅴ. 기대효과 및 결론

A3C와 PPO는 강화학습이 "느리고 불안정한 실험"에서 "확장 가능하고 관리 가능한 학습"으로 넘어가는 데 핵심 역할을 했다. A3C는 [[430_index_fast_full_scan|병렬]] 샘플링과 [[172_actor_critic|액터-크리틱]]의 실용화를 밀어 올렸고, PPO는 복잡한 신뢰 영역 아이디어를 현업 엔지니어도 구현 가능한 수준으로 단순화했다. 그 결과 로보틱스, 게임, 추천 최적화, 언어 모델 정렬까지 같은 철학이 넓게 퍼졌다.

하지만 둘 다 만능은 아니다. A3C는 비동기 노이즈와 하드웨어 비효율이 약점이고, PPO는 안정적이지만 샘플 비용이 큰 on-[[164_policy|policy]] [[001_algorithm_definition|알고리즘]]이라는 한계가 있다. 따라서 기억해야 할 핵심은 "A3C냐 PPO냐"의 이분법이 아니라, **경험 수집을 어떻게 넓히고 [[164_policy|정책]] 업데이트를 어떻게 안전하게 만들 것인가**라는 설계 질문이다.

- **📢 섹션 요약 비유**: A3C는 많은 손을 확보해 연습량을 늘린 방법이고, PPO는 한 번에 자세를 너무 바꾸지 않게 만든 안전 훈련법이다. 강화학습의 성숙은 결국 이 두 가지를 함께 다루는 방향으로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[172_actor_critic|Actor-Critic]] | A3C와 PPO가 공통으로 의존하는 기본 구조다. |
| Advantage | [[164_policy|정책]] 업데이트에 쓰이는 상대적 성과 [[130_signal|신호]]다. |
| TRPO | PPO가 단순화한 신뢰 영역 기반 선행 [[001_algorithm_definition|알고리즘]]이다. |
| GAE (Generalized Advantage Estimation) | PPO에서 [[136_variance|분산]]과 편향의 균형을 잡는 대표 어드밴티지 추정법이다. |
| [[153_kl_divergence|KL divergence]] | [[164_policy|정책]]이 이전 [[164_policy|정책]]에서 얼마나 멀어졌는지 재는 제어 지표다. |
| [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] | [[395_ppo_clipping|PPO]] 철학이 언어 모델 정렬에 응용된 대표 사례다. |
| Distributed rollout | A3C가 남긴 [[430_index_fast_full_scan|병렬]] 수집 사상이 발전한 운영 구조다. |

### 📈 관련 키워드 및 발전 흐름도

```text
정책 경사법 (Policy Gradient)
    │
    ▼
액터-크리틱 (Actor-Critic)
    │
    ├─ 병렬 경험 수집 문제 해결 ──▶ A3C
    │
    └─ 정책 급변 문제 해결
            │
            ▼
TRPO (Trust Region Policy Optimization)
            │
            ▼
PPO (Proximal Policy Optimization)
            │
            ▼
분산형 PPO · 로보틱스 · RLHF
```

이 흐름은 강화학습이 "평가 구조 확립 → [[430_index_fast_full_scan|병렬]]화 → 안정화 → 대규모 응용" 순으로 실용화된 과정을 요약한다.

### 👶 어린이를 위한 3줄 비유 설명

1. A3C는 로봇 한 명만 연습시키지 않고 여러 로봇이 동시에 놀이터를 돌아다니며 빨리 배우게 하는 방법이에요.
2. PPO는 로봇이 한 번 잘했다고 갑자기 습관을 확 바꾸지 못하게 해서 넘어지지 않게 도와주는 안전벨트예요.
3. 그래서 둘을 이해하면 "빨리 많이 배우는 법"과 "안전하게 배우는 법"을 함께 알 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 420

← **이전**: [[172_actor_critic|172. 액터-크리틱 (Actor-Critic) 모델]]
**다음**: [[174_mlops|174. MLOps (Machine Learning Operations)]] →

---
