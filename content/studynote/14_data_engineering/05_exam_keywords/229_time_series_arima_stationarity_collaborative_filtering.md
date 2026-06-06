---
title: "229. Time Series Arima Stationarity Collaborative Filtering"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/)([AutoRegressive](/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/) Integrated Moving Average, 자기회귀 누적 이동평균)는 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 과거 패턴(AR)·차분(I)·오차 패턴(MA)을 결합하여 미래를 예측하는 고전 통계 모델이며, 정상성([Stationarity](/studynote/10_ai/05_data_science_ml/377_time_series_stationarity/)) 확보가 전제조건이다.
> 2. **가치**: [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)([Collaborative Filtering](/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/))은 "나와 비슷한 사용자가 좋아한 것을 나도 좋아한다"는 원리로 [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)을 구현하며, [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/)([Matrix Factorization](/studynote/06_ict_convergence/05_data_science/348_matrix_factorization/))로 희소성(Sparsity) 문제를 극복한다.
> 3. **판단 포인트**: ARIMA는 선형·정상 시계열에 강하고, 딥러닝([LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/)·[Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))은 비선형·복잡 패턴에 강하다. [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)([Cold Start](/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/)) 문제를 콘텐츠 기반 필터링으로 보완해야 한다.

---

## Ⅰ. 개요 및 필요성

[시계열 분석](/studynote/06_ict_convergence/05_data_science/341_time_series_ar_ma_arma/)과 [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)은 두 가지 다른 분야처럼 보이지만, 모두 <strong>과거 패턴에서 미래/선호를 예측</strong>한다는 점에서 공통 수학 기반([행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/)·자기상관)을 공유한다.

### [시계열 분석](/studynote/06_ict_convergence/05_data_science/341_time_series_ar_ma_arma/) 응용 분야

| [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 예측 대상 | 모델 |
|:---|:---|:---|
| 금융 | 주가, 환율, 변동성 | GARCH, [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) |
| 소매 | 판매량 예측, 재고 최적화 | SARIMA, Prophet |
| 에너지 | 전력 수요, 발전량 예측 | [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/), XGBoost |
| [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | 장비 이상 예측, 예방 정비 | [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/), [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest |

📢 **섹션 요약 비유**: 시계열 예측은 "과거 날씨 기록으로 내일 날씨 예측"이고, [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) 추천은 "비슷한 취향의 친구가 좋아한 영화를 나에게 추천"하는 것이다. 둘 다 "과거 패턴에서 미래 답 찾기"다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 시계열 분해 (Time Series Decomposition)

모든 시계열은 다음 성분의 조합이다.

```
시계열 = 트렌드(T) + 계절성(S) + 잔차(R)

또는 곱셈 분해:
시계열 = T × S × R

+--------------------------------------------+
| 트렌드 (Trend)      : 장기 증감 방향        |
| 계절성 (Seasonality): 주기적 반복 패턴      |
| 주기성 (Cyclicity)  : 불규칙 중기 파동      |
| 잔차 (Residual)     : 설명 불가 노이즈      |
+--------------------------------------------+

Python: from statsmodels.tsa.seasonal import seasonal_decompose
```

### 2-2. 정상성 ([Stationarity](/studynote/10_ai/05_data_science_ml/377_time_series_stationarity/)) 검정

[ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) 적용 전 반드시 정상성을 확인해야 한다. 정상성: 평균·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 시간에 따라 변하지 않음.

```
ADF Test (Augmented Dickey-Fuller Test, 확장 디키-풀러 검정):
-------------------------------------------------------------
H₀: 단위근 존재 (비정상, Non-Stationary)
H₁: 단위근 없음 (정상, Stationary)

결과 해석:
p-value < 0.05 -> H₀ 기각 -> 정상 시계열
p-value ≥ 0.05 -> 비정상 -> 차분(Differencing) 적용

차분(Differencing):
  1차 차분: Yₜ' = Yₜ - Yₜ₋₁     (트렌드 제거)
  2차 차분: Yₜ'' = Yₜ' - Yₜ'₋₁  (이차 트렌드 제거)
  계절 차분: Yₜ - Yₜ₋ₛ           (계절성 제거)
```

### 2-3. [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) (p, d, q) 모델

```
ARIMA(p, d, q) 구성:
--------------------------------------------------------
AR (AutoRegressive, 자기회귀, p):
  Yₜ = c + φ₁Yₜ₋₁ + φ₂Yₜ₋₂ + ... + φₚYₜ₋ₚ + εₜ
  -> 과거 p개 자신의 값으로 현재 예측

I  (Integrated, 누적, d):
  d번 차분하여 정상성 확보
  d=1: 1차 차분, d=2: 2차 차분

MA (Moving Average, 이동평균, q):
  Yₜ = c + εₜ + θ₁εₜ₋₁ + θ₂εₜ₋₂ + ... + θqεₜ₋q
  -> 과거 q개 오차항으로 현재 보정
--------------------------------------------------------

파라미터 선택:
  ACF (AutoCorrelation Function, 자기상관함수) -> q 결정
  PACF (Partial ACF, 편자기상관함수)           -> p 결정
  AIC/BIC 최소화                               -> 최적 (p,d,q) 탐색
```

| 모델 | 설명 | 사용 시점 |
|:---|:---|:---|
| AR(p) | 자기회귀 | 추세 없는 정상 시계열 |
| MA(q) | 이동평균 | 오차 패턴만 있는 경우 |
| ARMA(p,q) | AR+MA | 정상 시계열 |
| [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/)(p,d,q) | 차분 포함 | 비정상 트렌드 있는 경우 |
| SARIMA(p,d,q)(P,D,Q)ₛ | 계절 [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) | 주기적 패턴 있는 경우 |

### 2-4. [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) ([Collaborative Filtering](/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/)) 구조

```
사용자-아이템 평점 행렬 (User-Item Rating Matrix):

           영화A  영화B  영화C  영화D
  사용자1 [  5     ?     3     ?  ]
  사용자2 [  ?     4     ?     2  ]
  사용자3 [  4     ?     ?     5  ]
  사용자4 [  ?     3     5     ?  ]

? = 예측 대상 (빈 칸 채우기 = 추천)

방법 1: 사용자 기반 (User-Based CF)
  -> "사용자1과 유사한 사용자가 좋아한 것 추천"
  -> 유사도: 코사인 유사도, 피어슨 상관

방법 2: 아이템 기반 (Item-Based CF)
  -> "사용자가 좋아한 영화와 유사한 영화 추천"
  -> Amazon 초기 추천 시스템에서 사용

방법 3: 행렬 분해 (Matrix Factorization)
  -> R ≈ P × Qᵀ   (SVD, ALS, SGD)
  -> 희소 행렬에서도 잠재 요인(Latent Factor) 추출
```

| 방법 | 장점 | 단점 |
|:---|:---|:---|
| 사용자 기반 CF | 직관적, 설명 쉬움 | 사용자 증가 시 확장 어려움 |
| 아이템 기반 CF | 안정적, 확장 쉬움 | 새 아이템 [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) |
| [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) | 희소성 극복, 높은 정확도 | 해석 어려움 |

📢 **섹션 요약 비유**: [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 "비슷한 취향의 친구 [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)"이다. "넷플릭스가 비슷한 시청 패턴의 사람들이 다 봤다는 이유로 특정 드라마를 추천"하는 원리다.

---

## Ⅲ. 비교 및 연결

### 3-1. 시계열 예측 모델 비교

| 모델 | 특징 | 장점 | 단점 |
|:---|:---|:---|:---|
| [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) | 통계 기반 선형 | 해석 가능, 소규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 비선형 패턴 한계 |
| SARIMA | 계절 [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) | 계절성 명시적 처리 | 파라미터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 복잡 |
| Prophet | Facebook [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 계절성·휴일 자동 처리 | 긴 시계열에 한계 |
| [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | 딥러닝 [순환 신경망](/studynote/10_ai/02_dl_architecture_new/111_rnn_recurrent_neural_network_sequential_data/) | 비선형, 장기 의존 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 많이 필요 |
| [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) | 어텐션 기반 | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리, 장기 패턴 | 계산 비용 높음 |

### 3-2. [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) ([Cold Start](/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/)) 문제와 해결

[협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)의 최대 약점은 신규 사용자/아이템에 대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부재다.

```
콜드 스타트 유형 및 해결:
--------------------------------------------------------
신규 사용자 콜드 스타트:
  -> 온보딩 시 명시적 선호 수집 (별점·장르 선택)
  -> 인기도 기반 추천 (Popular Items)
  -> 콘텐츠 기반 필터링 병행

신규 아이템 콜드 스타트:
  -> 메타데이터 기반 콘텐츠 유사도 계산
  -> 하이브리드 추천 (CB + CF 결합)
--------------------------------------------------------
```

📢 **섹션 요약 비유**: [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)는 "새 학교에 전학 온 학생에게 친구를 소개해 주는 것"이다. 아직 친구 기록이 없으니 "관심사 설문(콘텐츠 기반)"으로 첫 소개를 시작한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 소매 판매량 예측 SARIMA 적용 시나리오

```
[데이터] 3년간 월별 의류 판매량 (36 관측치)

[전처리]
① 시계열 분해 -> 강한 계절성(12개월 주기) 확인
② ADF Test: p = 0.34 -> 비정상
③ 1차 차분 -> ADF: p = 0.01 -> 정상화

[모델 선택]
ACF, PACF 분석 -> SARIMA(1,1,1)(1,1,1)₁₂

[평가]
RMSE = 245, MAPE = 4.2% -> 예측 오차 4.2%
다음 6개월 재고 주문 계획 수립에 활용
```

### 4-2. Netflix Prize [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)

```
[문제] 17,770 영화 × 480,189 사용자 평점 행렬 예측

[SVD 기반 행렬 분해]
R(n×m) ≈ P(n×k) × Q(k×m)ᵀ

n = 사용자 수, m = 영화 수, k = 잠재 요인 수 (50~200)

[학습] ALS (Alternating Least Squares, 교대 최소제곱법)
       또는 SGD (Stochastic Gradient Descent, 확률적 경사하강법)

[결과] RMSE = 0.8563 (기준 대비 10% 이상 개선)
```

📢 **섹션 요약 비유**: [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) 추천은 "학생-과목 성적표의 빈 칸을 '학습 스타일(잠재 요인)'을 추출해서 채우는 것"이다. 학습 스타일이 비슷한 학생들은 같은 과목에서 비슷한 점수를 받는다는 가정이다.

---

## Ⅴ. 기대효과 및 결론

ARIMA와 [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 각각 시계열 예측과 추천 분야의 기초 알고리즘이지만, 현대에는 딥러닝([LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/), [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/), 신경 [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/))과 결합하여 더 강력해지고 있다.

### 핵심 정리

| 영역 | 방법 | 핵심 포인트 |
|:---|:---|:---|
| 시계열 | [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/)(p,d,q) | 정상성 필수, ACF/PACF로 파라미터 결정 |
| 시계열 계절 | SARIMA | 계절 파라미터 (P,D,Q)ₛ 추가 |
| 추천: CF | 사용자/아이템 기반 | 유사도 기반, 확장성 한계 |
| 추천: MF | [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) ([SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/), ALS) | 희소성 극복, 잠재 요인 |
| 공통 한계 | [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) | 콘텐츠 기반+협업 하이브리드로 보완 |

📢 **섹션 요약 비유**: ARIMA는 "과거 기상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 내일 날씨를 선형 방정식으로 예측"하고, [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 "비슷한 날씨 패턴의 날에 일어난 일로 오늘 날씨 영향을 추측"하는 것이다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 전처리 | [Stationarity](/studynote/10_ai/05_data_science_ml/377_time_series_stationarity/) (정상성) | 평균·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시간 불변 |
| 전처리 | [ADF Test](/studynote/06_ict_convergence/05_data_science/343_stationarity_adf_test/) (디키-풀러 검정) | 단위근 검정 |
| 전처리 | Differencing (차분) | 비정상 -> 정상 변환 |
| 모델 | AR ([AutoRegressive](/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/)) | 과거 자신의 값 이용 |
| 모델 | MA (Moving Average) | 과거 오차 이용 |
| 모델 | [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) (p,d,q) | AR+I+MA 통합 모델 |
| 모델 | SARIMA | 계절 [ARIMA](/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) 확장 |
| 추천 | User-Based CF | 유사 사용자 기반 |
| 추천 | Item-Based CF | 유사 아이템 기반 |
| 추천 | [Matrix Factorization](/studynote/06_ict_convergence/05_data_science/348_matrix_factorization/) | [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)·ALS 잠재 요인 분해 |
| 문제 | [Cold Start](/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/) ([콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)) | 신규 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부재 문제 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. ARIMA는 "지난 3년간 아이스크림 판매량 그래프를 보고 다음 달 판매량을 예측하는 수학 공식"이다. 여름엔 오르고 겨울엔 내리는 패턴까지 계산한다.

### 📈 관련 키워드 및 발전 흐름도

```text
이동 평균 · 지수 평활법 (단순 예측)
    |
    v
ARIMA(p,d,q): 자기회귀 + 차분 + 이동평균
    +-► 정상성 변환: ADF 검정 · 차분(d)
    +-► SARIMA: 계절성 패턴 반영
    |
    v
Prophet (Facebook) · DeepAR (Amazon) · Temporal Fusion Transformer
    |
    v
협업 필터링: 사용자-아이템 행렬 -> 추천 시스템
```
2. [협업 필터링](/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) 추천은 "나와 같은 책을 읽은 사람들이 다음에 읽은 책을 나에게 추천"하는 것으로, 직접 물어보지 않아도 취향을 알 수 있다.
3. [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 문제는 "아직 아무 책도 읽지 않은 신규 회원에게 추천하기 어렵다"는 것이고, 이를 해결하려면 처음에 좋아하는 장르를 물어보는 방법을 쓴다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 229 / 258

<- **이전**: [228. PCA (Principal Component Analysis) LDA t-SNE 차원 축소](/studynote/14_data_engineering/05_exam_keywords/228_pca_lda_tsne_dimensionality_reduction/)
**다음**: [230. SVD (Singular Value Decomposition) 행렬 분해 랜덤 포레스트 XGBoost 부스팅](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) ->

---
