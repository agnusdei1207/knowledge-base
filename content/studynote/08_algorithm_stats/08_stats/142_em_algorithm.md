---
title: 13. EM 알고리즘 (Expectation-Maximization) — 잠재변수 추정
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트

> EM [[001_algorithm_definition|알고리즘]](Expectation-Maximization [[001_algorithm_definition|Algorithm]])은 "관측 [[001_dikw_pyramid|데이터]]만으로 [[143_mle|MLE]](Maximum Likelihood Estimation)가 불가능할 때, 잠재변수(Latent Variable)에 대한 [[135_expected_value|기댓값]]을 계산하고 파라미터를 갱신하는 과정을 반복해 수렴시키는" 우아한 반복 최적화 기법이다.
> E-단계(Expectation Step)와 M-단계(Maximization Step)를 교대 반복할 때마다 [[568_logs_distributed_logging_elk_fluentd|로그]] 우도(Log-Likelihood)는 단조 증가(Monotonically Non-Decreasing)가 보장된다 — 이것이 EM의 수학적 핵심이다.
> [[360_gmm_em_algorithm|GMM]](Gaussian Mixture Models) 클러스터링, HMM(Hidden [[755_markov_model|Markov Model]]) 학습, 결측 [[001_dikw_pyramid|데이터]] 대체까지 — EM은 "불완전한 [[001_dikw_pyramid|데이터]]"를 다루는 통계학의 만능 열쇠다.

---

## Ⅰ. 문제 [[009_config|설정]]: 잠재변수와 불완전 [[001_dikw_pyramid|데이터]]

**완전 [[001_dikw_pyramid|데이터]] (Complete [[001_dikw_pyramid|Data]])**: (X, Z) — 관측값 X와 잠재변수 Z 모두 알 때  
**불완전 [[001_dikw_pyramid|데이터]] (Incomplete [[001_dikw_pyramid|Data]])**: X만 관측, Z는 숨겨져 있음

**[[143_mle|MLE]](Maximum Likelihood Estimation) 목표**:

```
θ* = argmax log P(X|θ) = argmax log Σ_Z P(X, Z|θ)
```

잠재변수 Z에 대한 합산(marginalization) 때문에 log 안에 Σ가 생겨 **직접 미분 최적화가 불가능**하다. log(합)은 합(log)보다 훨씬 복잡하다.

**EM의 핵심 아이디어**: 직접 최적화하는 대신, **완전 [[001_dikw_pyramid|데이터]]의 [[568_logs_distributed_logging_elk_fluentd|로그]] 우도에 대한 [[135_expected_value|기댓값]](Q 함수)**을 반복 최대화한다.

📢 **섹션 요약 비유**: 잠재변수 문제는 "배달 기록 없이 창고 재고 파악하기"와 같다. 어떤 상품이 어디로 갔는지 모르지만(Z 숨겨짐), 남은 재고(X)를 보면서 "아마 이런 패턴이겠지"를 추론하는 것이 EM이다.

---

## Ⅱ. EM [[001_algorithm_definition|알고리즘]] 수식

**Q 함수 (보조 함수)**:

```
Q(θ | θ_old) = E_{Z|X, θ_old} [ log P(X, Z | θ) ]
             = Σ_Z P(Z|X, θ_old) · log P(X, Z|θ)
```

**E-단계 (Expectation Step)**:  
현재 파라미터 θ_old를 고정하고, 잠재변수 Z의 사후 분포 P(Z|X, θ_old)를 계산해 Q 함수를 구성.

**M-단계 (Maximization Step)**:  
Q 함수를 최대화하는 새 파라미터를 찾음:

```
θ_new = argmax_θ Q(θ | θ_old)
```

**반복**: θ_old ← θ_new, 수렴까지 반복.

**EM 반복 사이클**:

```
┌─────────────────────────────────────────────────────┐
│                   EM 반복 사이클                      │
│                                                      │
│   초기화 θ⁽⁰⁾                                        │
│        │                                             │
│        ▼                                             │
│   ┌─────────────────────────────────────────────┐   │
│   │  E-단계: Z 사후 분포로 Q(θ|θ_old) 계산      │   │
│   └──────────────────┬──────────────────────────┘   │
│                      │                               │
│                      ▼                               │
│   ┌─────────────────────────────────────────────┐   │
│   │  M-단계: Q 함수 최대화 → θ_new 갱신         │   │
│   └──────────────────┬──────────────────────────┘   │
│                      │                               │
│          수렴?   ────▶ Yes → 종료                    │
│           No ◀────────                               │
└─────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: EM은 "가구 배치 최적화"와 같다. E-단계는 "사람들이 이 방에서 주로 어디 있는지 관찰"하고, M-단계는 "그 패턴에 맞게 가구를 옮기는" 것이다. 반복할수록 가구 배치가 점점 나아진다.

---

## Ⅲ. 단조 증가 보장 (Jensen's Inequality)

EM이 각 반복마다 [[568_logs_distributed_logging_elk_fluentd|로그]] 우도를 감소시키지 않는 이유는 **Jensen 부등식(Jensen's Inequality)** 때문이다.

**Jensen 부등식**: f가 오목 함수(concave)이면, E[f(X)] ≤ f(E[X]).  
log는 오목 함수이므로:

```
log Σ_Z P(Z|X, θ_old) · [P(X,Z|θ) / P(Z|X, θ_old)]
≥ Σ_Z P(Z|X, θ_old) · log [P(X,Z|θ) / P(Z|X, θ_old)]
```

이를 정리하면: **log P(X|θ_new) ≥ log P(X|θ_old)**

즉 매 반복마다 관측 [[001_dikw_pyramid|데이터]]의 [[568_logs_distributed_logging_elk_fluentd|로그]] 우도는 줄어들지 않는다. **단조 증가 보장**.

**수렴 특성**:
- 국소 최대값(Local Maximum)에 수렴 — 전역 최대값(Global Maximum) 보장 없음
- 해결책: 다양한 [[459_quic_fec_forward_error_correction|초기]]값으로 여러 번 실행 (Multiple Random Restarts)
- 안장점(Saddle Point)에서 멈출 수 있음

📢 **섹션 요약 비유**: EM의 단조 증가 보장은 "낮은 곳으로만 흐르는 물"과 같다. 물은 절대 위로 흐르지 않듯, EM의 [[568_logs_distributed_logging_elk_fluentd|로그]] 우도는 절대 낮아지지 않는다. 다만 산의 최고봉(전역 최대)이 아닌 언덕 위(국소 최대)에서 멈출 수 있다.

---

## Ⅳ. GMM에서의 EM 구체 적용

**[[360_gmm_em_algorithm|GMM]](Gaussian Mixture Models, [[114_gaussian_mixture_model|가우시안 혼합 모델]])**은 K개 가우시안 분포의 가중합:

```
P(x) = Σ_{k=1}^{K} π_k · N(x | μ_k, Σ_k)
```

파라미터: π_k (혼합 [[267_weight_bias_activation|가중치]]), μ_k (평균), Σ_k (공분산 행렬)  
잠재변수 Z_i = k: i번째 [[001_dikw_pyramid|데이터]]가 k번째 클러스터에 속함

**GMM의 E/M 단계 구체 계산**:

| 단계 | 계산 항목 | 수식 |
|:---:|:---|:---|
| **E-단계** | 책임도 (Responsibility) | r_ik = π_k·N(xᵢ\|μ_k,Σ_k) / Σ_j π_j·N(xᵢ\|μ_j,Σ_j) |
| **M-단계** | 혼합 [[267_weight_bias_activation|가중치]] 갱신 | π_k^[[087_process_state_transition|new]] = (1/N) Σᵢ r_ik |
| **M-단계** | 평균 갱신 | μ_k^[[087_process_state_transition|new]] = Σᵢ r_ik·xᵢ / Σᵢ r_ik |
| **M-단계** | 공분산 갱신 | Σ_k^[[087_process_state_transition|new]] = Σᵢ r_ik·(xᵢ-μ_k)(xᵢ-μ_k)ᵀ / Σᵢ r_ik |

**K-평균(K-Means)과의 [[083_relationship_in_er_model|관계]]**: K-Means는 **하드 EM(Hard EM)**으로 해석 가능하다. r_ik ∈ {0, 1} (단 하나의 클러스터에만 완전 배정). GMM의 r_ik ∈ (0,1)인 소프트 EM과 달리, [[130_probability|확률]]적 배정 없이 가장 가까운 클러스터에만 완전 배정한다.

📢 **섹션 요약 비유**: GMM의 EM은 "설문 결과 분석"과 같다. 응답자가 어느 집단(Z)에 속하는지 모른 채 설문 [[001_dikw_pyramid|데이터]](X)만 있을 때, 먼저 "아마 이 집단이겠지" [[130_probability|확률]]을 추정(E-단계)하고, 그 [[130_probability|확률]]로 각 집단의 평균·분산을 갱신(M-단계)하는 것이다.

---

## Ⅴ. 응용: HMM 학습, 결측 [[001_dikw_pyramid|데이터]], 변형

**Baum-Welch [[001_algorithm_definition|알고리즘]]**: HMM 파라미터 추정을 위한 EM 특수 케이스.
- E-단계: Forward-Backward Algorithm으로 숨겨진 상태의 사후 [[130_probability|확률]] 계산
- M-단계: 전이 [[130_probability|확률]]·방출 [[130_probability|확률]]·[[459_quic_fec_forward_error_correction|초기]] [[130_probability|확률]] 갱신

**결측 [[001_dikw_pyramid|데이터]](Missing [[001_dikw_pyramid|Data]]) 대체([[367_missing_value_imputation_mice|Imputation]])**:
- 결측값을 잠재변수 Z로 취급
- E-단계: 결측값의 [[135_expected_value|기댓값]](조건부 평균) 계산
- M-단계: 완전화된 [[001_dikw_pyramid|데이터]]로 파라미터 추정

**EM 변형 [[001_algorithm_definition|알고리즘]]**:

```
┌───────────────────────────────────────────────┐
│             EM 알고리즘 변형 계열               │
├──────────────┬──────────────┬─────────────────┤
│  표준 EM     │   변분 EM    │   온라인 EM      │
│ (Batch)     │ (Variational) │ (Stochastic)    │
├──────────────┼──────────────┼─────────────────┤
│ 전체 데이터  │ 근사 사후    │ 미니배치 갱신    │
│ 한 번에 처리 │ 분포 사용    │ (대규모 데이터)  │
└──────────────┴──────────────┴─────────────────┘
```

📢 **섹션 요약 비유**: EM [[001_algorithm_definition|알고리즘]]의 응용은 "불완전한 퍼즐 맞추기"와 같다. 빠진 조각(잠재변수)을 "아마 이 모양이겠지"로 임시 채우고 전체 그림을 맞춰보고, 다시 빠진 조각 모양을 수정하기를 반복하면 결국 완성된 그림이 나타난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|:---|
| EM [[001_algorithm_definition|알고리즘]] | [[143_mle|MLE]] (잠재변수) | 해결 방법 |
| E-단계 | 사후 분포 P(Z\|X,θ) | 계산 대상 |
| M-단계 | Q 함수 최대화 | 파라미터 갱신 |
| Jensen 부등식 | 단조 증가 보장 | 수학적 근거 |
| [[360_gmm_em_algorithm|GMM]] | 소프트 EM | 주요 응용 |
| K-Means | 하드 EM | EM 특수 케이스 |
| Baum-Welch | HMM 학습 | EM 특수 케이스 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[잠재 변수 모델 (Latent Variable Model) — 관측 불가능한 숨겨진 변수 포함]
    │
    ▼
[EM 알고리즘 (Expectation-Maximization) — E단계(기댓값 계산) + M단계(파라미터 최적화) 반복]
    │
    ▼
[GMM (Gaussian Mixture Model) — EM으로 혼합 가우시안 파라미터 추정]
    │
    ▼
[베이지안 EM (Bayesian EM) — 사전 분포를 결합한 MAP 추정으로 과적합 방지]
    │
    ▼
[변분 추론 (Variational Inference) — EM의 확장, 복잡한 사후 분포 근사]
```

이 흐름은 잠재 변수를 포함한 [[130_probability|확률]] 모델의 우도 최대화를 위해 EM [[001_algorithm_definition|알고리즘]]이 개발되고, [[360_gmm_em_algorithm|GMM]] 등의 응용을 거쳐 베이지안 방법과 변분 추론으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

반 아이들을 키와 성격으로 두 팀으로 나누고 싶은데, 누가 어느 팀인지 모를 때 — 먼저 "아마 이 아이는 A팀이겠지" [[130_probability|확률]]로 나눠보고(E-단계), 그 기준으로 팀 평균 키를 다시 계산해(M-단계), 반복하면 딱 맞는 팀 구분이 나와!
이건 "가구 배치"랑 똑같아 — 사람들이 어디 많이 모이는지 보고(E), 거기에 소파를 두고(M), 다시 관찰하고 반복하다 보면 가장 좋은 배치가 완성돼.
EM [[001_algorithm_definition|알고리즘]]은 절대로 결과가 나빠지지 않아 — 반복할수록 점점 더 좋아지는 게 수학으로 증명됐거든!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 175

← **이전**: [[141_markov_property|12. 마르코프 성질 (Markov Property) — 미래 ⊥ 과거 | 현재]]
**다음**: [[143_mle|14. 최대 우도 추정 (MLE, Maximum Likelihood Estimation)]] →

---
