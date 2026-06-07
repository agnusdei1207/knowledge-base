---
title: "Markov Chain"
date: "2026-04-21"
tags:
  - "studynote-algorithm-stats"
weight: 140
---
## 핵심 인사이트

> 마르코프 체인(Markov Chain)의 핵심은 "미래는 오직 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)에만 의존한다"는 [마르코프 성질](/studynote/08_algorithm_stats/08_stats/141_markov_property/)([Markov Property](/studynote/08_algorithm_stats/08_stats/141_markov_property/))이며, 이 단순한 가정 위에서 강력한 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 모델이 탄생한다.
> 전이 행렬(Transition Matrix) P를 반복 거듭제곱하면 어떤 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 분포에서 출발하더라도 결국 정상 분포(Stationary Distribution) π에 수렴한다 — 시스템이 "균형"을 찾는 과정이다.
> [MCMC](/studynote/06_ict_convergence/05_data_science/376_mcmc_markov_chain_monte_carlo/)(Markov Chain Monte Carlo)는 이 수렴 성질을 역이용해, 직접 샘플링하기 어려운 복잡한 분포에서 간접적으로 표본을 추출하는 혁신적 기법이다.

---

## Ⅰ. 마르코프 체인의 정의

<strong><a href="/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a>(Stochastic <a href="/studynote/12_it_management/05_security_compliance/943_process/">Process</a>, <a href="/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a> 과정)</strong>란 시간에 따라 변화하는 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 변수의 수열 {X₀, X₁, X₂, ...}이다. 이 중 <strong><a href="/studynote/08_algorithm_stats/08_stats/141_markov_property/">마르코프 성질</a>(<a href="/studynote/08_algorithm_stats/08_stats/141_markov_property/">Markov Property</a>)</strong>을 만족하는 것이 마르코프 체인이다.

```
P(X_{t+1} = j | X_t = i, X_{t-1}, ..., X_0) = P(X_{t+1} = j | X_t = i)
```

과거 전체 이력은 무관하고, <strong><a href="/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/">현재 상태</a> i만 알면 다음 상태 j의 <a href="/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>을 결정할 수 있다</strong>.

<strong>전이 행렬(Transition Matrix) P</strong>는 이 조건부 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 행렬로 표현한 것이다.

- P_ij = P(X_{t+1} = j | X_t = i)
- 각 행의 합 = 1 ([확률](/studynote/08_algorithm_stats/08_stats/130_probability/)의 합 = 1)
- 모든 원소 ≥ 0

n 상태 체인의 전이 행렬은 n×n [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 행렬(Stochastic Matrix)이다. t-단계 후의 전이 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)은 **P^t** (행렬 거듭제곱)으로 계산한다.

📢 **섹션 요약 비유**: 마르코프 체인은 "오늘 날씨만 보고 내일 날씨를 예측하는 기상 앱"과 같다. 어제나 그제 날씨는 필요 없다 — 오늘이 맑으면 내일 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)은 오늘 상태만으로 결정된다.

---

## Ⅱ. 상태 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)

마르코프 체인의 각 상태는 다음과 같이 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)된다.

| 상태 유형 | 영문명 | 정의 | 특성 |
|:---:|:---:|:---|:---|
| 일시적 | Transient | 한번 떠나면 돌아올 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) < 1 | 유한 번 방문 후 탈출 |
| [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/)적 | Recurrent | 돌아올 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) = 1 | 무한히 반복 방문 |
| 양의 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) | Positive Recurrent | 평균 재방문 시간 < ∞ | 정상 분포 존재 |
| 영의 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) | Null Recurrent | 평균 재방문 시간 = ∞ | 정상 분포 미존재 |
| 흡수 상태 | Absorbing [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) | P_ii = 1, 탈출 불가 | 최종 종착지 |
| 에르고딕 | Ergodic | 양의 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) + 비주기적 | 유일 정상 분포로 수렴 |

<strong>에르고딕(Ergodic) 체인</strong>은 특히 중요하다. 어떤 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태에서 출발해도 동일한 정상 분포 π로 수렴하는 성질을 보장한다.

📢 **섹션 요약 비유**: 상태 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 "도시 간 이동 패턴"과 같다. 흡수 상태는 한번 들어가면 나올 수 없는 블랙홀 도시, [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 상태는 언젠간 반드시 돌아오는 고향 도시, 일시적 상태는 잠깐 거쳐 가는 경유지다.

---

## Ⅲ. 정상 분포와 수렴

<strong>정상 분포(Stationary Distribution) π</strong>는 전이 후에도 분포가 변하지 않는 균형 상태다.

```
πP = π,  Σπᵢ = 1,  πᵢ ≥ 0
```

에르고딕 체인에서는 t -> ∞ 일 때 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 분포 π⁽⁰⁾에 무관하게 <strong>π⁽⁰⁾P^t -> π</strong>가 성립한다.

<strong>믹싱 타임(Mixing Time)</strong>은 현재 분포와 정상 분포의 전변동 거리(Total Variation Distance)가 ε 이하로 줄어드는 데 필요한 최소 단계 수다.

```
t_mix(ε) = min{t : max_{x} ||P^t(x, ·) - π||_TV ≤ ε}
```

믹싱 타임이 짧을수록 빠르게 균형에 도달하므로, [MCMC](/studynote/06_ict_convergence/05_data_science/376_mcmc_markov_chain_monte_carlo/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 효율성을 결정한다.

**3-상태 마르코프 체인 전이 다이어그램**:

```
         0.3
    +-------------+
    |             v
  +-+--+  0.5  +----+
  | A  |------->| B  |
  +----+       +-+--+
    ^     0.2    |
    |  +----+   |0.6
    +--| C  |<---+
  0.4  +----+
       |  ^
       +--+
        0.4
```

(각 상태 A, B, C 간 전이 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 예시. 실선 방향이 전이 방향, 숫자가 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/))

📢 **섹션 요약 비유**: 정상 분포로의 수렴은 잉크 한 방울을 물컵에 떨어뜨리는 것과 같다. 처음엔 한 곳에 집중되어 있지만, 충분히 오래 기다리면 균일하게 퍼져 더 이상 변하지 않는 균형 상태가 된다.

---

## Ⅳ. MCMC와 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)랭크

### [MCMC](/studynote/06_ict_convergence/05_data_science/376_mcmc_markov_chain_monte_carlo/) (Markov Chain Monte Carlo)

복잡한 분포 π에서 직접 샘플링이 불가능할 때, π를 정상 분포로 갖는 마르코프 체인을 설계해 충분히 오랜 시간 실행 후 표본을 수집한다.

<strong>Metropolis-Hastings <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>:
1. 제안 분포(Proposal Distribution) q(x'|x)에서 후보 x' [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
2. 수락 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) α = min(1, π(x')·q(x|x') / π(x)·q(x'|x))
3. [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) α로 x' 수락, 아니면 현재 x 유지

<strong>Gibbs <a href="/studynote/03_network/01_data_communication/056_표본화_Sampling/">Sampling</a></strong>: 다변량 분포에서 한 번에 한 변수씩 조건부 분포로 갱신. Metropolis-Hastings의 특수 케이스(수락률 = 1).

### PageRank ([페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)랭크)

웹 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 마르코프 체인으로 모델링한다.
- **상태**: 웹 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)
- **전이**: 하이퍼링크를 따라 이동 (0.85) + 무작위 점프 (0.15, Damping Factor)
- **정상 분포 π**: 각 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 PageRank 점수

```
PageRank(i) = (1-d)/N + d · Σ_{j->i} PageRank(j)/|out(j)|
```

d = 0.85 (감쇠 인수, Damping Factor), N = 전체 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 수

📢 **섹션 요약 비유**: MCMC는 "미로 속 랜덤 워크"와 같다. 오래 걸어다니면 자주 지나친 곳일수록 중요한 곳이고, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)랭크는 이 원리로 "인기 있는 웹페이지"를 찾는다.

---

## Ⅴ. 응용 분야

<strong>텍스트 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: 바이그램(Bigram) 모델에서 현재 단어 -> 다음 단어 전이 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로 문장 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/). [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 이전 언어 모델의 핵심.

**대기 이론 (Queuing Theory)**: M/M/1 큐 — 포아송 도착, 지수 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 서버 1개. 정상 분포로 평균 대기 시간, 큐 길이 분석.

<strong>강화학습 <a href="/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/">MDP</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/314_mdp_rl/">Markov Decision Process</a>)</strong>: 환경을 마르코프 체인으로 모델링. 에이전트의 행동에 따라 상태가 전이되고 보상을 받는 구조.

```
+------------------------------------------------------+
|              마르코프 체인 응용 계층                   |
+----------------+----------------+--------------------+
|  텍스트 생성   |   대기 이론    |    강화학습 MDP    |
| (언어 모델)    | (M/M/1 큐)    |   (Q-Learning)     |
+----------------+----------------+--------------------+
|                  마르코프 체인                         |
|         (전이 행렬 P + 정상 분포 π)                   |
+------------------------------------------------------+
|                   MCMC 샘플링                         |
|       (Metropolis-Hastings / Gibbs)                   |
+------------------------------------------------------+
```

📢 **섹션 요약 비유**: 마르코프 체인 응용은 "규칙 하나로 다 설명하는 만능 레시피"다. 날씨 예측이든, 구글 검색이든, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 게임 플레이든 — "현재만 보면 미래가 결정된다"는 단 하나의 원리가 모든 것을 가능하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|:---|
| 마르코프 체인 | [마르코프 성질](/studynote/08_algorithm_stats/08_stats/141_markov_property/) | 기반 가정 |
| 전이 행렬 P | 정상 분포 π | πP = π로 연결 |
| 에르고딕 체인 | 믹싱 타임 | 수렴 속도 측정 |
| [MCMC](/studynote/06_ict_convergence/05_data_science/376_mcmc_markov_chain_monte_carlo/) | Metropolis-Hastings / Gibbs | 구현 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| PageRank | 웹 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 마르코프 체인 | 응용 사례 |
| [MDP](/studynote/06_ict_convergence/04_ai_llm/463_markov_decision_process_mdp/) | 강화학습 | 마르코프 체인 확장 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[확률 과정 (Stochastic Process) — 시간에 따라 상태가 확률적으로 변화]
    |
    v
[마르코프 체인 (Markov Chain) — 미래 상태가 현재 상태만 의존 (마르코프 성질)]
    |
    v
[정상 분포 (Stationary Distribution) — 장기 실행 후 수렴하는 확률 분포]
    |
    v
[은닉 마르코프 모델 (HMM — Hidden Markov Model) — 상태 관측 불가 환경에 확장]
    |
    v
[마르코프 결정 과정 (MDP — Markov Decision Process) — 강화학습 이론 기반]
```

이 흐름은 단순 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 모델에서 강화학습의 MDP까지 마르코프 이론의 확장 계보를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명

비가 오는 날엔 내일도 비가 올 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이 높고, 맑은 날엔 내일도 맑을 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이 높아 — 오늘 날씨만 알면 내일을 예측할 수 있어.
오랫동안 날씨를 기록하면 "비 30%, 맑음 70%"처럼 평균 날씨 패턴이 나오는데, 그게 바로 정상 분포야.
구글은 이 원리로 "많이 방문하는 웹페이지"를 찾아내 — 계속 이동하다 보면 좋은 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 오래 머물게 되거든!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 175

<- **이전**: [10. 중심 극한 정리 (CLT, Central Limit Theorem) — 표본 평균의 정규성](/studynote/08_algorithm_stats/08_stats/139_clt/)
**다음**: [12. 마르코프 성질 (Markov Property) — 미래 ⊥ 과거 | 현재](/studynote/08_algorithm_stats/08_stats/141_markov_property/) ->

---
