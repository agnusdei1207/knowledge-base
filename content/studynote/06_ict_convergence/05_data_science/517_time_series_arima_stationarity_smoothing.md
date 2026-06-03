---
title: 517. 시계열 ARIMA 정상성과 평활법 (Time Series ARIMA Stationarity Smoothing)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정상성([[377_time_series_stationarity|Stationarity]]) — 평균·[[136_variance|분산]]이 시간에 따라 변하지 않음 — 은 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 모델링의 전제 조건이며, ADF 검정(Augmented Dickey-Fuller Test)으로 [[396_validation|확인]] 후 차분(Differencing)으로 달성한다.
> 2. **가치**: [[342_arima_auto_regressive_integrated_moving_average|ARIMA]]([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]] Integrated Moving Average)의 p, d, q 파라미터는 ACF(Autocorrelation Function)/PACF(Partial ACF) 패턴으로 체계적으로 결정하고, AIC/BIC로 최적 모델을 선택한다.
> 3. **판단 포인트**: 계절성이 있으면 SARIMA, 딥러닝이 필요하면 [[292_lstm|LSTM]]·TCN([[157_time_series_deep_learning_tcn_transformer|Temporal Convolutional Network]]) — 단, [[001_dikw_pyramid|데이터]] 양이 충분해야 딥러닝이 통계 모델을 능가한다.

---

## Ⅰ. 개요 및 필요성

시계열 [[001_dikw_pyramid|데이터]](Time Series [[001_dikw_pyramid|Data]])는 시간 순서가 의미를 갖는 [[001_dikw_pyramid|데이터]]다. 주가, 기온, 서버 트래픽 등이 대표 예시다. 일반 ML 모델과 달리 시간적 의존성을 명시적으로 모델링해야 한다.

### 정상성 ([[377_time_series_stationarity|Stationarity]]) 조건

| 조건 | 수식 | 의미 |
|:---|:---|:---|
| 평균 불변 | E[Xₜ] = μ (상수) | 트렌드(Trend) 없음 |
| [[136_variance|분산]] 불변 | Var(Xₜ) = σ² (상수) | 변동성 변화 없음 |
| 공분산 시차 의존 | Cov(Xₜ, Xₜ₊ₖ) = f(k)만 의존 | 계절성 없음 |

**비정상 시계열 변환**:
- 트렌드 제거: 1차 차분 (d=1) → Xₜ' = Xₜ − Xₜ₋₁
- [[136_variance|분산]] 안정화: [[568_logs_distributed_logging_elk_fluentd|로그]] 변환 → ln(Xₜ)
- 계절성 제거: 계절 차분 → Xₜ − Xₜ₋ₛ (s: 계절 주기)

- **📢 섹션 요약 비유**: 정상성은 강물이 일정한 수위로 흘러야 예측이 가능한 것처럼, [[001_dikw_pyramid|데이터]]가 들쭉날쭉 올라가거나 내려가면(비정상) 모델이 패턴을 찾기 어려워. 차분은 강물의 수위 변화를 분석하는 것과 같아.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[342_arima_auto_regressive_integrated_moving_average|ARIMA]](p, d, q) 파라미터 결정 흐름

```
시계열 데이터
      │
      ▼
ADF 검정 → 비정상? → d회 차분 (I 부분 결정)
      │                 │
      ▼                 ▼
  정상성 달성         d=1 or 2
      │
      ├─ PACF 분석 → AR 차수 p 결정
      │  (절단점 = p)
      │
      └─ ACF 분석 → MA 차수 q 결정
         (절단점 = q)
      │
      ▼
ARIMA(p,d,q) 적합 → AIC/BIC 최소 모델 선택
```

### ACF vs PACF 패턴 해석

| 패턴 | AR(p) [[130_signal|신호]] | MA(q) [[130_signal|신호]] |
|:---|:---|:---|
| ACF | 지수적 감소 또는 진동 감소 | q 시차 후 절단 |
| PACF | p 시차 후 절단 | 지수적 감소 또는 진동 감소 |

**[[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 구성 요소**:
- AR(p): Xₜ = φ₁Xₜ₋₁ + ... + φₚXₜ₋ₚ + εₜ (자기회귀)
- I(d): d회 차분으로 정상성 달성
- MA(q): Xₜ = εₜ + θ₁εₜ₋₁ + ... + θqεₜ₋q (이동평균)

- **📢 섹션 요약 비유**: AR은 "오늘 기온은 어제 기온과 비슷할 거야"처럼 과거 값을 사용하는 부분이고, MA는 "어제 예측이 틀렸으니 오늘 예측에 반영하자"처럼 과거 오차를 사용하는 부분이야.

---

## Ⅲ. 비교 및 연결

### 지수 평활법 ([[344_exponential_smoothing_moving_average|Exponential Smoothing]]) 비교

| 방법 | 대응 패턴 | 파라미터 |
|:---|:---|:---|
| 단순 지수 평활 (SES) | 트렌드·계절성 없음 | α (평활 계수) |
| Holt의 이중 지수 평활 | 트렌드 있음 | α, β |
| Holt-Winters | 트렌드+계절성 | α, β, γ |

**Holt-Winters vs SARIMA**:
- Holt-Winters: 계산 빠르고 단순, 단기 예측에 강점.
- SARIMA(p,d,q)(P,D,Q)[s]: 통계적 추론 가능, AIC/BIC로 모델 선택 체계적.

### 딥러닝 시계열 모델

- **[[292_lstm|LSTM]] ([[292_lstm|Long Short-Term Memory]])**: RNN의 [[291_long_term_dependency|장기 의존성]] 학습. [[001_dikw_pyramid|데이터]] ≥ 수천 포인트 권장.
- **TCN ([[157_time_series_deep_learning_tcn_transformer|Temporal Convolutional Network]])**: 인과 합성곱으로 [[430_index_fast_full_scan|병렬]] 학습 가능, LSTM보다 빠름.
- **Prophet (Facebook)**: 트렌드 + 계절성 + 휴일 효과 분리 모델, 비전문가도 사용 용이.

- **📢 섹션 요약 비유**: 지수 평활은 최근 기억에 더 [[267_weight_bias_activation|가중치]]를 두는 인간의 기억 방식이야. 오래된 기억은 흐릿해지고(작은 [[267_weight_bias_activation|가중치]]), 최근 기억은 선명해(큰 [[267_weight_bias_activation|가중치]]). 어제 있었던 일이 일주일 전보다 더 잘 기억되는 것처럼.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시나리오 - 소매점 매출 예측**:
- 3년치 주간 매출 [[001_dikw_pyramid|데이터]] 분석.
- 1단계: ADF 검정 p-값 = 0.48 > 0.05 → 비정상 → 1차 차분 후 p-값 = 0.003 → 정상 (d=1).
- 2단계: ACF가 12시차(연간 계절성) 반복 → SARIMA 적용.
- 3단계: 모델 탐색 SARIMA(1,1,1)(1,1,1)[52] → AIC 최소.
- RMSE = 4,200만 원 (MAPE 3.8%) → 재고 최적화 연 1.2억 원 절감.

**잔차 진단**:
- Ljung-Box 검정: 잔차에 자기상관 없음 → 모델 적합 [[396_validation|확인]].
- 잔차 정규성: Q-Q 플롯 [[396_validation|확인]].

**기술사 판단 포인트**:
- [[001_dikw_pyramid|데이터]] < 50 포인트: 단순 지수 평활 또는 Holt-Winters 우선 고려.
- 구조 변화(Structural Break) 탐지: Chow Test → 변환점 전후 별도 모델링.
- 이상값 탐지: 시계열 이상값(Innovational [[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]], Additive [[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]]) 유형별 처리.

- **📢 섹션 요약 비유**: 시계열 예측은 날씨 예보처럼, "오늘이 맑으면 내일도 맑을 가능성이 높다(AR)"는 규칙과 "어제 예보가 틀렸으니 오늘은 보정하자(MA)"는 두 가지 논리를 합쳐서 미래를 예측하는 거야.

---

## Ⅴ. 기대효과 및 결론

[[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 계열 모델과 딥러닝 시계열 모델을 [[001_dikw_pyramid|데이터]] 특성에 맞게 선택하면 재고 관리·에너지 수요 예측·금융 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 관리 등 다양한 영역에서 예측 정확도를 높일 수 있다.

- **재고 최적화**: 정확한 수요 예측으로 과재고·품절 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 감소.
- **[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]**: 예측값과 실제값 차이(잔차) 모니터링으로 시스템 이상 조기 감지.
- **운영 효율**: 자동화된 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 파라미터 탐색(Auto-[[342_arima_auto_regressive_integrated_moving_average|ARIMA]])으로 모델 유지 비용 절감.

- **📢 섹션 요약 비유**: 시계열 분석은 역사책을 읽고 미래를 예측하는 거야. 과거 패턴(AR), 과거 실수(MA), 그리고 계절 반복(S)을 모두 고려해야 좋은 예측이 나와.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 정상성 | ADF 검정, 차분 · [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 전처리 |
| [[342_arima_auto_regressive_integrated_moving_average|ARIMA]](p,d,q) | ACF/PACF, AIC/BIC · 시계열 예측 |
| SARIMA | 계절성, 계절 차분 · 월별/분기별 [[001_dikw_pyramid|데이터]] |
| Holt-Winters | 지수 평활, 트렌드+계절 · 단기 예측 |
| [[292_lstm|LSTM]]/TCN | [[291_long_term_dependency|장기 의존성]], 딥러닝 · 복잡 비선형 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ADF 검정 · 차분] → [시계열 ARIMA 정상성과 평활법] → [장기 의존성 · 딥러닝]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 시계열은 매일 기온을 기록한 일기장처럼, 시간 순서가 중요한 [[001_dikw_pyramid|데이터]]야.
2. ARIMA는 "어제 기온이 오늘에 영향을 주고(AR), 어제 예측 실수도 반영해서(MA)" 미래 기온을 예측하는 방법이야.
3. 계절이 있으면 SARIMA로 "작년 여름이 올해 여름에도 영향을 준다"는 패턴까지 추가로 학습해!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 517 / 552

← **이전**: [[516_markov_chain_absorbing_ergodic_transition|516. 마르코프 체인: 흡수, 에르고딕, 전이 상태 (Markov Chain Absorbing Ergodic Transition)]]
**다음**: [[518_tfidf_cosine_similarity_text_mining_word2vec|518. TF-IDF, 코사인 유사도, 텍스트 마이닝 (TF-IDF Cosine Similarity Text Mining Word2Vec)]] →

---
