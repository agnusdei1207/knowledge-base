+++
weight = 112
title = "109. 시계열 분석 (Time Series Analysis) — ARIMA/Prophet/LSTM 시계열 예측"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[341_time_series_ar_ma_arma|시계열 분석]] (Time Series Analysis)은 시간 순서로 측정된 [[001_dikw_pyramid|데이터]]에서 추세 (Trend), 계절성 (Seasonality), 주기성 (Cyclicity), 잔차 (Residual) 네 가지 성분을 분리·모델링하여 미래 값을 예측하는 시간 의존적 [[001_dikw_pyramid|데이터]] 분석 기법이다.
> 2. **가치**: 수요 예측, 주가 예측, 기온 예측, 서버 부하 예측 등 "과거 패턴이 미래에도 반복된다"는 가정이 성립하는 모든 영역에서 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] ([[229_time_series_arima_stationarity_collaborative_filtering|AutoRegressive Integrated Moving Average]])부터 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 기반 모델까지 폭넓게 활용된다.
> 3. **판단 포인트**: 정상성 ([[377_time_series_stationarity|Stationarity]]) 검정 후 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 파라미터 (p, d, q)를 결정하고, 계절성이 명확하면 SARIMA/Prophet, 비선형 장기 패턴이 복잡하면 [[292_lstm|LSTM]], 다변량 고해상도라면 Temporal Fusion Transformer를 선택한다.

---

## Ⅰ. 개요 및 필요성

주식 가격, 월별 판매량, 일일 기온, 시간당 서버 요청 수—이 모두는 시간 축을 따라 변화하는 시계열 [[001_dikw_pyramid|데이터]]다. 과거 패턴이 미래에 반복될 것이라는 가정이 성립할 때, [[341_time_series_ar_ma_arma|시계열 분석]]은 강력한 예측 도구가 된다.

빅데이터 환경에서는 초 단위 센서 [[001_dikw_pyramid|데이터]], 실시간 거래 [[001_dikw_pyramid|데이터]], 소셜 미디어 타임스탬프 [[001_dikw_pyramid|데이터]] 등 수십억 개의 시계열이 [[087_process_state_transition|생성]]된다. 이를 효과적으로 처리하려면 개별 예측 [[001_algorithm_definition|알고리즘]]뿐만 아니라, 대용량 [[430_index_fast_full_scan|병렬]] 처리와 자동 [[247_feature_label_variables|피처]] 엔지니어링이 결합된 시스템 설계가 필요하다.

- **📢 섹션 요약 비유**: [[341_time_series_ar_ma_arma|시계열 분석]]은 계절마다 반복되는 날씨 패턴을 보고 내일 날씨를 예측하는 것이다. 과거가 없으면 미래를 예측할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 시계열 분해 (Time Series Decomposition)

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    시계열 성분 분해                                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  원본 시계열 Y(t) = 추세 T(t) + 계절성 S(t) + 잔차 R(t)              │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ T(t): 장기 추세        /──────────────────                     │ │
│  │                      /                                         │ │
│  │ S(t): 계절성   /\/\/\/\/\/\/\/\/\/\/\/\/\/\                     │ │
│  │                                                                │ │
│  │ R(t): 잔차    ⌇⌇⌇⌇ (예측 불가능한 노이즈)                       │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ADF 검정 (Augmented Dickey-Fuller Test) → 정상성 (Stationarity) 확인│
│  비정상 → d차 차분 (Differencing) → 정상 시계열로 변환              │
└──────────────────────────────────────────────────────────────────────┘
```

### 주요 모델 비교

| 모델 | 원리 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| **[[342_arima_auto_regressive_integrated_moving_average|ARIMA]](p,d,q)** | AR+차분+MA 결합 | 수학적 명료함, 소규모 [[001_dikw_pyramid|데이터]] | 비선형·장기 패턴 약함 | 단변량, 단기 예측 |
| **SARIMA** | [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] + 계절 파라미터(P,D,Q,m) | 계절성 명시적 처리 | 파라미터 튜닝 복잡 | 계절성 [[001_dikw_pyramid|데이터]] |
| **Holt-Winters** | 지수 평활 + 추세 + 계절 | 직관적, 빠름 | 비선형 패턴 약 | 소규모 계절 [[001_dikw_pyramid|데이터]] |
| **Facebook Prophet** | 가산 모델, 휴일 효과 자동 | 강건함, 결측 처리, 자동화 | 복잡한 비선형 약함 | 비즈니스 수요 예측 |
| **[[292_lstm|LSTM]]** | 게이트 기반 [[111_rnn_recurrent_neural_network_sequential_data|순환 신경망]] | 비선형 [[291_long_term_dependency|장기 의존성]] | 학습 비용, 과적합 | 복잡한 패턴, 다변량 |
| **Temporal Fusion [[246_transformer_self_attention_parallel_positional_encoding|Transformer]]** | 어텐션 + 공변량 통합 | 다변량, 설명 가능 | 대규모 [[001_dikw_pyramid|데이터]] 필요 | 고해상도 다변량 |

- **📢 섹션 요약 비유**: ARIMA는 수학 공식으로 내일을 예측하는 통계학자이고, LSTM은 수천 일의 역사를 공부해서 패턴을 체득한 학자다. Prophet은 "매주 월요일은 이렇다, 여름에는 저렇다"는 상식을 자동으로 반영하는 비즈니스 분석가다.

---

## Ⅲ. 비교 및 연결

| 항목 | 전통 통계 ([[342_arima_auto_regressive_integrated_moving_average|ARIMA]]/SARIMA) | 딥러닝 ([[292_lstm|LSTM]]/[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 요구량** | 수십~수백 포인트 | 수천~수만 포인트 |
| **해석 가능성** | 높음 (파라미터 명시적) | 낮음 (블랙박스) |
| **비선형 처리** | 제한적 | 우수 |
| **다변량 처리** | VAR 필요 | 자연스러운 통합 |
| **학습 비용** | 낮음 | 높음 ([[418_gpu|GPU]] 필요) |
| **자동화 용이성** | Auto-[[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 가능 | [[176_automl_hyperparameter_optimization_bayesian|AutoML]] [[123_pipe|파이프]]라인 |

정상성 ([[377_time_series_stationarity|Stationarity]]) 개념: 시계열의 평균과 [[136_variance|분산]]이 시간에 따라 변하지 않는 성질. ADF (Augmented Dickey-Fuller) 검정으로 [[396_validation|확인]]하며, [[337_p_value_significance|p-value]] < 0.05이면 정상. 비정상 시계열은 차분 (Differencing)으로 정상화.

- **📢 섹션 요약 비유**: 정상성은 시험 난이도가 항상 비슷해야 과거 점수로 미래 점수를 예측할 수 있다는 원칙이다. 난이도가 갑자기 확 올라가면 (비정상) 과거 [[001_dikw_pyramid|데이터]]가 미래를 예측하지 못한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. **리테일 수요 예측**: 주별·월별 SKU 단위 수요 → SARIMA/Prophet으로 재고 최적화
2. **서버 용량 계획**: 시간당 트래픽 [[292_lstm|LSTM]] 예측 → 오토스케일링 사전 준비
3. **에너지 수요 예측**: 기온·요일·계절 고려 → Temporal Fusion Transformer로 발전소 가동 계획
4. **금융 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]**: 주가 변동성 (Volatility) 예측 → GARCH 모델 ([[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 확장)

### 기술사 [[435_checklist_based_testing|체크리스트]]

1. ADF 검정으로 정상성을 [[396_validation|확인]]하고, 비정상이면 적절한 차수 d를 결정했는가?
2. ACF (Autocorrelation Function)와 PACF (Partial Autocorrelation Function) 플롯으로 AR(p), MA(q) 파라미터를 [[396_validation|확인]]했는가?
3. 계절성 주기 (m)가 명확하면 SARIMA 또는 Prophet을 우선 고려했는가?
4. 외부 변수 (날씨, 휴일, 프로모션)가 있다면 공변량 (Covariate)으로 모델에 통합했는가?
5. 평가 지표: RMSE (Root Mean [[341_iso_iec_25010|Square]] Error), MAE (Mean Absolute Error), MAPE (Mean Absolute Percentage Error) 중 비즈니스에 맞는 것을 선택했는가?

- **📢 섹션 요약 비유**: 시계열 모델 선택은 여행 교통수단 선택과 같다. 단거리·평탄한 길은 자전거([[342_arima_auto_regressive_integrated_moving_average|ARIMA]]), 계절 패턴이 있으면 [[344_bus|버스]](SARIMA/Prophet), 험한 비선형 산악길은 4WD([[292_lstm|LSTM]]), 복잡한 다변량 도로망은 자율주행차([[246_transformer_self_attention_parallel_positional_encoding|Transformer]])가 적합하다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 재고 최적화 | 과잉재고·품절 동시 감소, 물류 비용 절감 |
| 용량 계획 자동화 | 피크 부하 사전 대비로 [[090_service_kubernetes_network_load_balancing|서비스]] 안정성 향상 |
| 에너지 효율화 | 수요 예측 기반 발전 계획으로 낭비 전력 감소 |
| 금융 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 관리 | 변동성 예측으로 [[446_port_and_bus|포트]]폴리오 헤지 [[268_strategy_pattern|전략]] 개선 |
| 이상 조기 감지 | 예측 범위 초과 = 이상 [[130_signal|신호]], 시계열+[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] 결합 |

[[341_time_series_ar_ma_arma|시계열 분석]]은 과거가 미래를 말해준다는 인류의 가장 오래된 예측 본능을 수학으로 구현한 것이다. 통계 기반 ARIMA에서 딥러닝 기반 Transformer까지, [[001_dikw_pyramid|데이터]]의 크기와 복잡도에 따라 적합한 도구를 선택하는 기술사적 판단이 중요하다. 빅데이터 환경에서는 수천 개의 개별 시계열을 [[430_index_fast_full_scan|병렬]]로 예측하는 대규모 [[123_pipe|파이프]]라인 설계가 핵심 역량이 됐다.

- **📢 섹션 요약 비유**: [[341_time_series_ar_ma_arma|시계열 분석]]은 바다의 조류를 연구하는 것과 같다. 추세는 바다의 전반적 방향, 계절성은 조수간만, 잔차는 예측 불가한 파도다. 조류를 알아야 항해 계획을 세울 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| 정상성 ([[377_time_series_stationarity|Stationarity]]) | ARIMA의 전제 조건 |
| ADF 검정 (Augmented Dickey-Fuller Test) | 정상성 통계 검정 |
| [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] ([[229_time_series_arima_stationarity_collaborative_filtering|AutoRegressive Integrated Moving Average]]) | 전통 시계열 예측 표준 모델 |
| Facebook Prophet | 비즈니스 수요 예측 특화 자동화 모델 |
| [[292_lstm|LSTM]] ([[292_lstm|Long Short-Term Memory]]) | 딥러닝 기반 비선형 시계열 예측 |
| 차분 (Differencing) | 비정상 시계열을 정상으로 변환하는 전처리 |
| MAPE (Mean Absolute Percentage Error) | 시계열 예측 평가 지표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[시계열 데이터 (Time Series Data) — 시간 순서로 기록된 연속적 관측값]
    │
    ▼
[정상성 (Stationarity) — 평균·분산이 시간에 무관한 통계적 특성, 분석 전제 조건]
    │
    ▼
[ARIMA (AutoRegressive Integrated Moving Average) — 전통적 선형 시계열 예측 모델]
    │
    ▼
[LSTM / Transformer — 딥러닝 기반 비선형 장기 의존성 포착]
    │
    ▼
[Prophet / NeuralProphet — 추세·계절성 분해 기반 실무 시계열 예측 프레임워크]
```

이 흐름은 시계열 [[001_dikw_pyramid|데이터]]의 정상성 확보에서 출발하여 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 등 전통 모델을 거쳐 딥러닝 기반 예측 모델과 실용적 프레임워크로 발전하는 [[341_time_series_ar_ma_arma|시계열 분석]]의 진화 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- [[341_time_series_ar_ma_arma|시계열 분석]]은 "매년 여름에 아이스크림이 많이 팔렸으니, 올 여름에도 많이 팔릴 거야"처럼 과거 패턴으로 미래를 예측하는 거예요.
- 추세는 "요즘 점점 더워지는 것", 계절성은 "매년 여름에 더운 것", 잔차는 "예상치 못한 태풍"이에요.
- 컴퓨터가 이 세 가지를 자동으로 분리해서 내일, 다음 달, 내년을 예측해줘요!
