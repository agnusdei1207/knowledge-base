---
title: "377. 시계열 정상성 (Stationarity)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정상성 (Stationarity)은 시계열의 평균·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·자기공분산이 시간에 따라 변하지 않는 성질로, [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) ([AutoRegressive Integrated Moving Average](/studynote/14_data_engineering/05_exam_keywords/229_time_series_arima_stationarity_collaborative_filtering/)) 등 고전 시계열 모델의 필수 전제 조건이다.
> 2. **가치**: 비정상 시계열을 차분 (Differencing)·변환으로 정상화한 뒤 모델링하면 허위 회귀 (Spurious Regression)를 방지하고 예측 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 높인다.
> 3. **판단 포인트**: ADF (Augmented Dickey-Fuller) 검정과 KPSS (Kwiatkowski-Phillips-Schmidt-Shin) 검정을 상호 보완적으로 사용해 정상성 여부를 통계적으로 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

---

## Ⅰ. 개요 및 필요성

시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 세 가지 비정상 요소가 공존한다:
- **추세 (Trend)**: 장기적 상승/하락 경향
- **계절성 (Seasonality)**: 일정 주기로 반복되는 패턴
- **불규칙 변동 (Irregular)**: 예측 불가능한 노이즈

비정상 시계열을 그대로 회귀 모델에 투입하면, 두 시계열이 실제로는 무관해도 높은 R^가 나타나는 허위 회귀 (Spurious Regression) 문제가 발생한다. 정상성 확보는 시계열 모델링의 첫 번째 단계다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 정상성은 "파도 높이가 매일 다른 해변(비정상)"과 "잔잔한 호수처럼 항상 일정한 물결(정상)"의 차이다. 예측하려면 일단 잔잔하게 만들어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 정상성의 정의

**강정상성 (Strictly Stationary)**:
```
(Xₜ₁, …, Xₜₖ) ≡ (Xₜ₁₊h, …, Xₜₖ₊h)  ∀k, h
```

**약정상성 (Weakly Stationary, 실무 사용)**:
```
E[Xₜ] = μ (상수)
Var(Xₜ) = σ^ (상수)
Cov(Xₜ, Xₜ₊h) = γ(h)  (시간 차이 h에만 의존)
```

### 비정상 시계열 처리 흐름

```
+------------------------------------------------------+
|  원시 시계열                                          |
|       v                                              |
|  [추세 제거]  로그변환, 1차 차분                      |
|       v                                              |
|  [계절성 제거]  계절 차분(lag=s), STL 분해            |
|       v                                              |
|  [정상성 검정]  ADF / KPSS                           |
|       v                                              |
|  정상 시계열 -> ARMA 모델링                            |
+------------------------------------------------------+
```

### 차분 (Differencing)

**1차 차분**: ΔXₜ = Xₜ - Xₜ₋₁ (추세 제거)
**2차 차분**: Δ^Xₜ = ΔXₜ - ΔXₜ₋₁ (강한 추세)
**계절 차분**: ΔₛXₜ = Xₜ - Xₜ₋ₛ (주기 s 계절성 제거)

### ADF 검정 (Augmented Dickey-Fuller Test)

귀무가설: 단위근(Unit Root) 존재 = 비정상
대립가설: 단위근 없음 = 정상

```
ΔXₜ = α + βt + γXₜ₋₁ + Σδᵢ ΔXₜ₋ᵢ + εₜ
H₀: γ = 0 (단위근 존재, 비정상)
H₁: γ < 0 (정상)
```

| 검정 | 귀무가설 | 기각 -> | 채택 -> |
|:---|:---|:---|:---|
| ADF | 비정상 (단위근) | 정상 | 비정상 |
| KPSS | 정상 | 비정상 | 정상 |
| [PP](/studynote/12_it_management/01_governance_strategy/015_payback_period/) (Phillips-Perron) | 비정상 (단위근) | 정상 | 비정상 |

두 검정 병행: ADF p < 0.05 & KPSS p > 0.05 -> 정상성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)

- **📢 섹션 요약 비유**: ADF는 "범인(단위근)이 없다고 주장하는 경찰", KPSS는 "범인이 있다고 주장하는 검사"다. 두 주장이 모두 정상성을 지지할 때만 믿을 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | 추세 정상화 | 계절 정상화 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 정상화 |
|:---|:---|:---|:---|
| 방법 | 1차 차분, 회귀 추세 제거 | 계절 차분, [더미 변수](/studynote/06_ict_convergence/05_data_science/330_dummy_variable/) | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 변환, Box-Cox |
| [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) | d 차수 결정 | SARIMA의 D 차수 | 전처리로 선행 |

<strong><a href="/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/">ARIMA</a>(p,d,q) 모델과 정상성</strong>:
- d = 차분 횟수 -> 정상화를 위한 통합(Integration) 차수
- 정상화 후 AR(p) + MA(q) 구조 추정

- **📢 섹션 요약 비유**: ARIMA에서 d는 "계단(비정상)을 몇 번 내려와야 평지(정상)에 도달하는지" 층수다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**주식 가격**: 전형적 비정상 (추세+[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 증가) -> [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 수익률 = log(Pₜ/Pₜ₋₁) 로 정상화
**전력 수요**: 추세 + 주별·일별 계절성 -> 차분 + 계절 차분 병행
<strong><a href="/studynote/02_operating_system/02_process_thread/130_signal/">신호</a> 처리</strong>: [FFT](/studynote/08_algorithm_stats/07_numerical/126_fft/) (Fast Fourier Transform)로 주파수 성분 분석 후 계절성 분해

기술사 판단 포인트:
1. 차분 횟수(d)는 최소화 -> 과차분(Overdifferencing)은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 증가
2. ADF 단독 사용 금지, KPSS 병행
3. ACF (자기상관함수)/PACF ([편자기상관함수](/studynote/10_ai/05_data_science_ml/411_pacf_partial_autocorrelation/)) 플롯으로 모델 오더 결정

- **📢 섹션 요약 비유**: 차분은 "오르막(추세)을 평지로 만드는 고도 조정"이다. 너무 많이 조정하면 땅이 파여(과차분) 오히려 걸어 다니기 더 힘들다.

---

## Ⅴ. 기대효과 및 결론

정상성 확보는 시계열 예측 모델의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 담보하는 핵심 전처리다. 딥러닝 [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/), [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 시계열 모델에서도 정상화된 입력이 학습 안정성과 예측 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높인다. 허위 회귀 방지라는 통계적 엄밀성은 실무 의사결정의 품질을 직접 좌우한다.

- **📢 섹션 요약 비유**: 정상성 확보는 요리 전 재료 손질이다. 재료가 신선하고 균일해야(정상 시계열) 맛있는 요리(정확한 예측)가 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 정상성 (Stationarity) | 평균·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·공분산 불변 / 시계열 모델링 전제 |
| 차분 (Differencing) | d, 단위근 제거 / 정상화 방법 |
| ADF 검정 | 단위근, [p-value](/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) / 정상성 통계 검정 |
| KPSS 검정 | 정상성 귀무가설 / ADF 보완 검정 |
| [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) | p, d, q / 정상화 후 모델 |
| 허위 회귀 | Spurious Regression / 비정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위험 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [시계열 정상성 (Stationarity)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 시계열 정상성은 "파도가 항상 같은 높이로 치는 조용한 호수"야. 예측 모델은 이런 잔잔한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 좋아해.
2. 차분은 마치 롤러코스터의 오르내림을 평평한 땅으로 만드는 과정이야. 한 번 내리막으로 빼면 더 평평해지거든.
3. ADF 검정은 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 진짜 잔잔한지 아닌지" 수학적으로 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 테스트야. KPSS는 반대 방향에서 한 번 더 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해주는 친구야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 377 / 420

<- **이전**: [376. 마르코프 체인 (Markov Chain)](/studynote/10_ai/05_data_science_ml/376_markov_chain/)
**다음**: [378. 동적 시간 워핑 (DTW, Dynamic Time Warping)](/studynote/10_ai/05_data_science_ml/378_dtw/) ->

---
