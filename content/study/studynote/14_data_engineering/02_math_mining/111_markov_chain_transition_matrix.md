+++
weight = 111
title = "111. 마르코프 체인 (Markov Chain) - 전이 행렬과 상태 확률 수렴"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[140_markov_chain|마르코프 체인]]([[140_markov_chain|Markov Chain]])은 **"미래 상태는 오직 현재 상태에만 의존하고 과거 경로와 무관하다"**는 [[141_markov_property|마르코프 성질]]([[141_markov_property|Markov Property]], 무기억성)을 만족하는 [[130_probability|확률]]적 [[632_state_transition_diagram_testing|상태 전이]] 모델이다.
> 2. **가치**: 전이 [[130_probability|확률]] 행렬(Transition Matrix) $P$를 정의하면, $\[[009_process_innovation|pi]] P = \[[009_process_innovation|pi]]$를 만족하는 **정상 분포(Stationary Distribution)**로 수렴하는 장기 균형 상태를 예측할 수 있어 PageRank·날씨 예측·금융 모델링의 수학적 기반이 된다.
> 3. **판단 포인트**: 이산 시간·유한 상태의 기본 [[140_markov_chain|마르코프 체인]]에서 출발하여, 연속 시간(CTMC)·은닉 상태(HMM)·[[463_markov_decision_process_mdp|마르코프 결정 과정]]([[463_markov_decision_process_mdp|MDP]], 강화학습 기초)으로 확장된다.

---

## Ⅰ. 개요 및 필요성

"내일 날씨는 오늘 날씨에만 달려있다(어제·그저께 무관)"라는 단순한 가정이 놀라울 만큼 강력한 예측 모델을 만든다. Google PageRank는 "사용자가 현재 [[286_page_frame|페이지]]에서 다음 [[286_page_frame|페이지]]로 넘어갈 [[130_probability|확률]]"을 [[140_markov_chain|마르코프 체인]]으로 모델링하여 검색 순위를 결정한다.

```text
┌───────────────────────────────────────────────────────┐
│      날씨 마르코프 체인 예시                            │
├───────────────────────────────────────────────────────┤
│              0.7                                      │
│   ┌──────────────────┐                                │
│   │                  ▼                                │
│  [맑음] ─── 0.3 ──▶ [비]                              │
│   ▲                  │                                │
│   └──── 0.4 ─────────┘                                │
│                  0.6                                  │
│   ┌──────────────────┐                                │
│   │                  ▼                                │
│  전이행렬 P = | 0.7  0.3 |                            │
│              | 0.4  0.6 |                             │
│                                                       │
│  정상분포: π = (4/7, 3/7) ≈ (57%, 43%)               │
│  → 장기적으로 맑은 날이 57%, 비 오는 날이 43%         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[140_markov_chain|마르코프 체인]]은 "오늘이 맑으면 내일도 70% 맑다"는 규칙만으로 1년 치 날씨 비율을 예측하는 마법의 주사위다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 정의 | 비유 |
|:---|:---|:---|
| **상태 ([[272_state_pattern|State]])** | 시스템이 취할 수 있는 값 | 날씨(맑음/비) |
| **전이 [[130_probability|확률]]** | 상태 i → j로 이동할 [[130_probability|확률]] $P_{ij}$ | 주사위 눈금 [[130_probability|확률]] |
| **전이 행렬 (P)** | 모든 전이 [[130_probability|확률]]을 행렬로 정리 | 주사위 설계도 |
| **정상 분포 (π)** | $\[[009_process_innovation|pi]] P = \[[009_process_innovation|pi]]$, 장기 균형 [[130_probability|확률]] | 주사위를 무한 번 굴린 결과 |

### 수렴 조건
1. **비주기적(Aperiodic)**: 상태로 돌아오는 주기가 고정되지 않음.
2. **기약(Irreducible)**: 어느 상태에서든 다른 모든 상태로 도달 가능.
3. **에르고딕(Ergodic)**: 비주기 + 기약 → 유일한 정상 분포로 수렴 보장.

- **📢 섹션 요약 비유**: 전이 행렬은 보드게임 판의 이동 규칙이고, 정상 분포는 수만 번 게임 후 각 칸에 머무는 평균 비율이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[140_markov_chain|마르코프 체인]] | HMM | [[463_markov_decision_process_mdp|MDP]] |
|:---|:---|:---|:---|
| **상태 관측** | 직접 관측 | **은닉 (Hidden)** | 직접 관측 |
| **결정/[[130_probability|확률]]** | [[130_probability|확률]]적 전이 | [[130_probability|확률]]적 전이 | **행동 선택 + [[130_probability|확률]]적 전이** |
| **목적** | 상태 예측 | 관측으로 상태 추론 | **보상 최대화 (강화학습)** |
| **대표 응용** | PageRank | 음성 인식 | 로봇 제어 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 응용
1. **PageRank**: 웹 [[286_page_frame|페이지]] 간 전이 [[130_probability|확률]] → 정상 분포 = 검색 순위.
2. **[[376_mcmc_markov_chain_monte_carlo|MCMC]] ([[140_markov_chain|Markov Chain]] Monte Carlo)**: 복잡한 [[130_probability|확률]] 분포에서 샘플링.
3. **고객 이탈 예측**: 고객 상태(활성→휴면→이탈) 전이 [[130_probability|확률]] 모델링.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[141_markov_property|마르코프 성질]] 위반 시 적용**: 고객 행동이 1주일 전 행동에도 영향받는 경우 → 고차 [[140_markov_chain|마르코프 체인]] 또는 다른 모델 필요.

---

## Ⅴ. 기대효과 및 결론

[[140_markov_chain|마르코프 체인]]은 강화학습([[463_markov_decision_process_mdp|MDP]])·자연어 처리(HMM)·검색 엔진(PageRank)의 **수학적 뿌리**이며, 무기억성이라는 단순한 가정이 복잡한 현실 시스템의 장기 행동을 놀라울 만큼 정확하게 예측한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **전이 행렬** | [[140_markov_chain|마르코프 체인]]의 핵심 [[001_dikw_pyramid|데이터]] 구조 |
| **정상 분포** | 장기 균형 [[130_probability|확률]], $\[[009_process_innovation|pi]] P = \[[009_process_innovation|pi]]$ |
| **PageRank** | 웹 그래프를 [[140_markov_chain|마르코프 체인]]으로 모델링 |
| **HMM** | 은닉 상태 + 마르코프 전이 (음성 인식) |
| **[[463_markov_decision_process_mdp|MDP]]** | 행동 선택 + 마르코프 전이 (강화학습) |
| **[[376_mcmc_markov_chain_monte_carlo|MCMC]]** | [[140_markov_chain|마르코프 체인]]으로 복잡한 분포에서 샘플링 |

### 📈 관련 키워드 및 발전 흐름도

```text
[마르코프 체인 이론 (Markov, 1906) — 무기억성 확률 모델]
    │
    ▼
[HMM (1960s~) — 은닉 상태 추론, 음성 인식]
    │
    ▼
[MCMC (Metropolis, 1953→Hastings, 1970) — 베이지안 샘플링]
    │
    ▼
[PageRank (1998, Google) — 웹 검색 순위]
    │
    ▼
[MDP + 강화학습 (2010s~) — AlphaGo, 로보틱스]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[140_markov_chain|마르코프 체인]]은 **"오늘 맑으면 내일도 맑을 [[130_probability|확률]] 70%"**라는 간단한 규칙으로 날씨를 예측하는 거예요.
2. 이 규칙대로 주사위를 계속 굴리면, 1년 중 **맑은 날이 57%, 비 오는 날이 43%**라는 답이 나와요.
3. Google 검색 순위(PageRank)도 이 주사위 원리로 "어떤 [[286_page_frame|페이지]]가 중요한지" 결정한답니다!
