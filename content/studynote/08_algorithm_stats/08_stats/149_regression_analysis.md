+++
title = "20. 회귀 분석 (Regression Analysis) — 단순/다중/로지스틱"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트

> 회귀 분석(Regression Analysis)의 본질은 변수 간 함수 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 추정하는 것으로, OLS(Ordinary Least Squares, [최소 제곱법](/knowledge-base/studynote/06_ict_convergence/05_data_science/327_ordinary_least_squares_ols/))는 잔차(Residual)의 제곱합을 최소화해 가장 잘 맞는 선(최적 적합선)을 찾는다.
> [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)([Logistic Regression](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/))는 이름과 달리 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 알고리즘이며, 선형 결합을 [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)) 함수로 변환해 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 해석할 수 있게 한다 — 딥러닝 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 레이어의 직접 조상이다.
> 릿지(Ridge)와 라쏘([Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/)) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/)) 방지와 변수 선택의 도구이며, 베이즈 관점에서는 각각 가우시안 사전(Gaussian Prior)과 라플라스 사전(Laplace Prior)에 해당한다.

---

## Ⅰ. 단순 선형 회귀

**단순 선형 회귀 (Simple Linear Regression)** 모델:

```
y = β₀ + β₁x + ε

β₀: 절편 (Intercept)
β₁: 기울기 (Slope)
ε ~ N(0, σ²): 오차항 (Error Term)
```

<strong>OLS(Ordinary Least Squares, <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/327_ordinary_least_squares_ols/">최소 제곱법</a>) 추정량</strong>:

```
최소화: Σᵢ εᵢ² = Σᵢ (yᵢ - β₀ - β₁xᵢ)²

β̂₁ = Cov(X, Y) / Var(X) = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²
β̂₀ = ȳ - β̂₁x̄
```

<strong>회귀선과 잔차 <a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a></strong>:

```
   y
    ▲         ★
    │       ╱  ↑ 잔차 (Residual) = y - ŷ
    │     ★╱
    │   ╱★ ↓
    │ ╱★
    │╱
    └─────────────────▶ x
     회귀선 ŷ = β̂₀ + β̂₁x
     OLS = 모든 잔차 제곱합 최소화
```

<strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/098_coefficient_of_determination_r_squared/">결정 계수</a> (R², <a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/098_coefficient_of_determination_r_squared/">Coefficient of Determination</a>)</strong>:

```
R² = 1 - SS_Res / SS_Tot = SS_Reg / SS_Tot

R² = 0: 모델이 아무것도 설명 못함
R² = 1: 모델이 분산을 완벽하게 설명
```

📢 **섹션 요약 비유**: 단순 회귀는 "점들 사이를 가장 잘 통과하는 줄 긋기"와 같다. OLS는 모든 점에서 줄까지의 거리 제곱의 합이 최소가 되도록 줄의 방향과 위치를 결정한다.

---

## Ⅱ. 다중 회귀와 다중공선성

**다중 회귀 (Multiple Regression)**:

```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₚxₚ + ε

행렬 표현: y = Xβ + ε
OLS: β̂ = (XᵀX)⁻¹Xᵀy   (XᵀX 역행렬 존재 시)
```

**R² vs 수정 R² (Adjusted R²)**:
- R²은 변수를 추가할수록 단조 증가 (과적합 위험)
- 수정 R² = 1 - [(1-R²)(n-1)/(n-p-1)]: 불필요한 변수 추가 시 감소

<strong>다중공선성 (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/">Multicollinearity</a>)</strong>: 독립 변수들 간 높은 상관관계

<strong>VIF (<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a> Inflation Factor, <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 팽창 인수)</strong>:

```
VIF_j = 1 / (1 - R²_j)

R²_j: j번째 변수를 나머지 변수들로 회귀했을 때의 R²
```

| VIF 값 | 해석 |
|:---:|:---|
| 1 | 다중공선성 없음 |
| 1~5 | 경미한 다중공선성 |
| 5~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 중간 수준, 주의 필요 |
| > [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 심각한 다중공선성 → 제거 or Ridge 적용 |

📢 **섹션 요약 비유**: 다중공선성은 "두 목격자가 똑같은 진술"을 하는 것과 같다. 두 증인이 완전히 동일한 말을 한다면, 한 명은 법정(모델)에 불필요하다 — 오히려 판사(모델)가 혼란스러워진다.

---

## Ⅲ. [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)

<strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/">로지스틱 회귀</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/">Logistic Regression</a>)</strong>: 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 위한 선형 모델

```
log-odds = logit(p) = log(p/(1-p)) = β₀ + β₁x₁ + ... + βₚxₚ = Xβ

확률로 변환: p = σ(Xβ) = 1 / (1 + e^(-Xβ))
```

<strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/069_sigmoid_function_vanishing_gradient/">시그모이드 함수</a> (<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/">Sigmoid</a> Function)</strong>: σ(z) = 1/(1+e^(-z))
- 출력 범위: (0, 1) → [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 해석 가능
- 결정 경계 (Decision Boundary): p = 0.5 일 때, Xβ = 0

**학습**: [MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/)(Maximum Likelihood Estimation)로 파라미터 추정

```
ℓ(β) = Σᵢ [yᵢ log σ(xᵢᵀβ) + (1-yᵢ) log(1-σ(xᵢᵀβ))]
     = -Binary Cross-Entropy (이진 교차 엔트로피)
```

[경사 하강법](/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/)([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/))으로 최적화 (닫힌 형식 해 없음).

<strong>다중 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>: [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) 함수로 확장

```
P(y=k|x) = exp(Xβ_k) / Σ_j exp(Xβ_j)
```

📢 **섹션 요약 비유**: [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)는 "이메일이 스팸일 가능성을 0~100%로 평가하는 점수판"이다. 여러 단서(단어 빈도)를 선형 결합해 점수를 매기고, [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)로 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 변환 후 50% 기준으로 스팸/정상을 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)한다.

---

## Ⅳ. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/): Ridge와 [Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/)

**과적합 문제**: 변수가 많으면 학습 데이터에 과도하게 맞아 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하.

<strong>Ridge 회귀 (L2 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>)</strong>:

```
최소화: Σ(yᵢ - ŷᵢ)² + λ Σ βⱼ²
                          ↑ L2 페널티

β̂_Ridge = (XᵀX + λI)⁻¹Xᵀy   (항상 역행렬 존재)
```

- 계수를 0에 가깝게 수축(Shrinkage)하지만 완전히 0이 되지는 않음
- 다중공선성 해결에 효과적

<strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/">Lasso</a> 회귀 (L1 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>, Least Absolute Shrinkage and <a href="/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/">Selection</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/">Operator</a>)</strong>:

```
최소화: Σ(yᵢ - ŷᵢ)² + λ Σ |βⱼ|
                          ↑ L1 페널티
```

- 일부 계수를 정확히 0으로 만듦 → <strong>자동 변수 선택(Feature <a href="/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/">Selection</a>)</strong>
- 희소 모델(Sparse Model) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

```
┌────────────────────────────────────────────────────┐
│           Ridge vs Lasso 비교                       │
├──────────────────────┬─────────────────────────────┤
│        Ridge          │          Lasso              │
├──────────────────────┼─────────────────────────────┤
│ L2 페널티 ||β||₂²    │ L1 페널티 ||β||₁            │
│ 계수 수축, 0 미도달  │ 계수 정확히 0 (변수 선택)   │
│ 다중공선성 해결      │ 희소 모델 (Sparse)           │
│ 가우시안 사전 MAP    │ 라플라스 사전 MAP            │
│ 닫힌 형식 해 존재    │ 수치 최적화 필요             │
└──────────────────────┴─────────────────────────────┘
```

<strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/374_elastic_net_regression/">Elastic Net</a></strong>: Ridge + [Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/) 결합: λ₁||β||₁ + λ₂||β||₂²  
변수 선택 + 상관 변수 함께 선택(Group [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/)).

📢 **섹션 요약 비유**: Ridge는 "모든 직원 급여를 조금씩 삭감", Lasso는 "성과 없는 직원은 해고"와 같다. Ridge는 모든 변수를 유지하며 작게 만들고, Lasso는 중요하지 않은 변수를 완전히 제거한다.

---

## Ⅴ. 회귀 가정과 잔차 분석

**선형 회귀의 4가지 가정 (LINE)**:
1. **선형성 (Linearity)**: E[y|X] = Xβ — 비선형 패턴 시 변수 변환 필요
2. <strong>독립성 (<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/133_independence/">Independence</a>)</strong>: 잔차들이 서로 독립 — 시계열 데이터에서 자기상관(Autocorrelation) 위반 주의
3. **등분산성 (Homoscedasticity)**: 잔차 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 X에 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)없이 일정 — 위반 시 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 안정화 변환(log, √) 필요
4. **정규성 (Normality)**: 잔차 ~ N(0, σ²) — 소표본에서 추론(검정, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))에 필요

**진단 플롯 (Diagnostic Plots)**:

| 플롯 이름 | [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 가정 | 이상 패턴 |
|:---|:---:|:---|
| Residuals vs Fitted | 선형성, 등분산성 | 곡선 패턴, 깔때기 모양 |
| Normal Q-Q | 정규성 | 점들이 대각선에서 이탈 |
| Scale-Location | 등분산성 | 기울기가 있는 패턴 |
| Residuals vs Leverage | 영향력 점 | Cook's Distance > 1인 점 |

**회귀 분석 전체 흐름**:

```
┌─────────────────────────────────────────────────────┐
│              회귀 분석 워크플로우                     │
├───────────┬──────────┬──────────┬────────────────────┤
│  EDA       │  모델    │  가정    │   해석              │
│  탐색      │  적합    │  검진    │                    │
├───────────┼──────────┼──────────┼────────────────────┤
│ 산점도    │ OLS/MLE  │ 잔차 플롯│ β 해석             │
│ 상관 행렬 │ Ridge    │ VIF 확인 │ R² 확인            │
│ 이상값    │ Lasso    │ 정규성   │ 예측 구간          │
└───────────┴──────────┴──────────┴────────────────────┘
```

📢 **섹션 요약 비유**: 회귀 진단 플롯은 "자동차 계기판"과 같다. 엔진이 잘 돌아가도(모델 적합) 계기판(진단 플롯)을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 "등분산성 경고등(깔때기 패턴)", "정규성 경고등(Q-Q 이탈)"을 발견할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|:---|
| OLS | [최소 제곱법](/knowledge-base/studynote/06_ict_convergence/05_data_science/327_ordinary_least_squares_ols/) | 잔차 제곱합 최소화 |
| R² | [결정 계수](/knowledge-base/studynote/14_data_engineering/02_math_mining/098_coefficient_of_determination_r_squared/) | 모델 설명력 측정 |
| 다중공선성 | VIF | 진단 지표 |
| [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) | [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 변환 |
| Ridge | L2 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) / 가우시안 사전 | 수축 추정 |
| [Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/) | L1 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) / 라플라스 사전 | 변수 선택 |
| 잔차 분석 | 회귀 가정 | 모델 진단 방법 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 수집 및 탐색 (EDA)]
    │
    ▼
[단순 선형 회귀 — 독립변수 1개, OLS(최소제곱법) 추정]
    │
    ▼
[다중 회귀 — 독립변수 복수, 다중공선성·VIF 진단]
    │
    ▼
[정규화 회귀 (Ridge / Lasso / ElasticNet) — 과적합 방어]
    │
    ▼
[비선형·ML 회귀 (GBM / SVR / DNN) — 복잡 패턴 학습]
```
단순 선형 회귀에서 다중 회귀로 확장하고, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 기법으로 과적합을 방어한 뒤 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 회귀 모델로 진화하는 것이 실무 분석의 표준 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

회귀 분석은 "산점도의 점들을 가장 잘 관통하는 선 긋기"야 — 그 선으로 새 데이터의 값을 예측할 수 있어!
[로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)는 "이메일이 스팸일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 계산기"야 — "돈 벌기", "클릭하세요" 같은 단어가 많을수록 스팸 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 100%에 가까워져.
릿지(Ridge)는 "모든 변수를 조금씩 줄이기", 라쏘([Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/))는 "중요하지 않은 변수는 완전히 없애기"야 — 둘 다 모델이 과도하게 복잡해지는 걸 막아줘!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 149 / 175

← **이전**: [19. t-검정 / F-검정 / ANOVA — 평균 비교 검정](/knowledge-base/studynote/08_algorithm_stats/08_stats/148_t_f_anova/)
**다음**: [1. 정보이론 (Information Theory) — Shannon, 1948](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/150_information_theory/) →

---
