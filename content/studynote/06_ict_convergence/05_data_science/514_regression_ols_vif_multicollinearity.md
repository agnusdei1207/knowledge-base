---
title: '514. 회귀 분석: OLS, VIF, 다중공선성 (Regression OLS VIF Multicollinearity)'
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OLS(Ordinary Least Squares, 최소 자승법)는 잔차(Residual) 제곱합을 최소화해 독립변수와 종속변수의 선형 [[083_relationship_in_er_model|관계]]를 추정하며, 회귀 계수의 최량 선형 불편 추정량(BLUE)을 보장한다.
> 2. **가치**: 다중공선성([[080_multicollinearity_vif_variance_inflation_factor_regression|Multicollinearity]])은 독립변수들 간 강한 상관관계로 회귀 계수 추정이 불안정해지는 현상 — VIF([[136_variance|Variance]] Inflation Factor) > 10이면 변수 제거 또는 [[093_normalization|정규화]] 필요.
> 3. **판단 포인트**: R²는 높지만 VIF도 높은 모델은 신뢰 불가 — 조정된 R²(Adjusted R²)와 VIF를 함께 [[396_validation|확인]]하고, 릿지(Ridge) 또는 라쏘([[102_lasso_ridge_regression_regularization|Lasso]]) [[093_normalization|정규화]]로 다중공선성을 대처한다.

---

## Ⅰ. 개요 및 필요성

회귀 분석은 예측(Prediction)과 [[122_causal_inference|인과 추론]]([[122_causal_inference|Causal Inference]]) 양쪽에 활용된다. OLS는 가장 기본적이지만 가정이 위배되면 결과를 신뢰할 수 없다.

### OLS의 가우스-마르코프 가정 (Gauss-Markov Assumptions)

1. **선형성 (Linearity)**: Y = β₀ + β₁X₁ + ε
2. **등분산성 (Homoscedasticity)**: Var(ε) = σ² (상수)
3. **잔차 정규성 (Normality of Residuals)**
4. **독립성 ([[133_independence|Independence]])**: 관측값 간 상관 없음
5. **다중공선성 없음**: 독립변수들 간 완전한 선형 [[083_relationship_in_er_model|관계]] 없음

**BLUE 정리**: 위 가정이 모두 만족되면 OLS 추정량이 최량 선형 불편 추정량(BLUE, Best Linear Unbiased Estimator).

- **📢 섹션 요약 비유**: OLS는 점들을 가로지르는 선을 그을 때 모든 점에서 선까지의 수직 거리 제곱합을 가장 작게 만드는 선을 선택하는 방법이야. 완벽한 선 하나를 [[001_dikw_pyramid|데이터]]에서 뽑아내는 거지.

---

## Ⅱ. 아키텍처 및 핵심 원리

### VIF 계산 흐름과 다중공선성 진단

```
다중 회귀 모델 구축
        │
        ▼
┌─────────────────────────────────┐
│  VIF 계산: VIFⱼ = 1/(1 - Rⱼ²)  │
│  Rⱼ² = Xⱼ를 나머지로 회귀한 R²  │
└─────────────────────────────────┘
        │
   ┌────┴────┐
VIF < 5   VIF > 10
  정상     심각한 다중공선성
            │
    ┌───────┴────────┐
  변수 제거       Ridge / Lasso
  (Dropping)      정규화(Regularization)
```

### R² vs 조정된 R²

| 지표 | 공식 | 특성 |
|:---|:---|:---|
| R² | 1 − SS_res / SS_tot | 변수 추가 시 항상 증가 (과적합 위험) |
| Adjusted R² | 1 − (1−R²)(n−1)/(n−k−1) | 쓸모없는 변수 추가 시 감소 → 모델 선택 지표 |
| RMSE | √(SS_res/n) | 예측 오차 원래 단위 |

**β 계수 해석**: β₁ = "X₁이 1단위 증가할 때 다른 변수를 고정한 상태에서 Y의 평균 변화량."

- **📢 섹션 요약 비유**: 다중공선성은 두 선수가 항상 같이 움직이는 것처럼, 키와 몸무게를 함께 독립변수로 쓰면 어느 쪽이 성적에 영향을 주는지 모델이 구별하지 못하는 문제야.

---

## Ⅲ. 비교 및 연결

### [[093_normalization|정규화]] 방법 비교

| 방법 | 패널티 항 | 특성 | 다중공선성 대처 |
|:---|:---|:---|:---|
| Ridge (L2) | λΣβⱼ² | 계수 축소, 0으로 만들지 않음 | 강건 |
| [[102_lasso_ridge_regression_regularization|Lasso]] (L1) | λΣ|βⱼ| | 일부 계수 = 0 (변수 선택) | 자동 제거 |
| [[374_elastic_net_regression|Elastic Net]] | α·L1 + (1-α)·L2 | 두 방법의 혼합 | 균형적 |

**다중공선성 vs 과적합 구분**:
- 다중공선성: 독립변수 간 [[083_relationship_in_er_model|관계]] 문제 → 계수 불안정, [[090_configuration_item|CI]] 넓어짐.
- 과적합([[245_overfitting_variance|Overfitting]]): 훈련 [[001_dikw_pyramid|데이터]]에 너무 맞춤 → 일반화 [[282_performance_tactics|성능]] 저하.

- **📢 섹션 요약 비유**: Ridge는 팀원 모두의 역할을 조금씩 줄이는 것이고, Lasso는 기여도가 낮은 팀원을 아예 팀에서 빼버리는 거야. 중복된 역할의 팀원(다중공선성)이 있을 때 Lasso가 더 깔끔하게 정리해줘.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시나리오 - 부동산 가격 예측 모델**:
- 독립변수: 면적, 층수, 연식, 주변 편의시설 수, 지하철 거리.
- VIF 결과: 면적 VIF=12.3 (심각), 연식 VIF=1.8 (정상).
- 면적과 가격의 상관이 너무 높아 직접 제거 대신 Ridge [[093_normalization|정규화]] 적용.
- Adjusted R²: OLS=0.82 → Ridge(λ=0.1)=0.81 (약간 감소)
- 그러나 Test RMSE: OLS=4,200만 원 → Ridge=3,600만 원 (일반화 [[282_performance_tactics|성능]] 향상).

**잔차 진단 절차**:
1. 잔차 vs 적합값 플롯 → 등분산성(Homoscedasticity) [[396_validation|확인]].
2. Q-Q 플롯 → 잔차 정규성 [[396_validation|확인]].
3. Durbin-Watson 검정 → 잔차 독립성(자기상관 없음).

**기술사 판단 포인트**:
- VIF > [[489_raid_10_hybrid|10]] 독립변수: 상관 높은 변수 중 하나 제거 or [[338_pca_principal_component_analysis|주성분 분석]]([[163_pca|PCA]]) 전처리.
- 이분산성(Heteroscedasticity) 발견: WLS(Weighted Least Squares) 또는 [[568_logs_distributed_logging_elk_fluentd|로그]] 변환.

- **📢 섹션 요약 비유**: VIF 검사는 팀 프로젝트에서 두 명이 완전히 같은 일을 하고 있는지 [[396_validation|확인]]하는 거야. 둘이 하는 일이 똑같으면 한 명은 빼거나 역할을 나눠야 효율이 올라가.

---

## Ⅴ. 기대효과 및 결론

OLS의 가정 검토와 VIF 진단을 체계적으로 수행하면 예측 [[282_performance_tactics|성능]]과 해석 가능성을 동시에 확보할 수 있다.

- **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 계수 해석**: VIF 관리로 안정적인 β 추정 → [[122_causal_inference|인과 추론]] 가능.
- **과적합 방지**: Ridge/[[102_lasso_ridge_regression_regularization|Lasso]] [[093_normalization|정규화]]로 일반화 [[282_performance_tactics|성능]] 유지.
- **모델 선택 체계화**: Adjusted R², AIC(Akaike Information Criterion), BIC(Bayesian Information Criterion) 기준으로 변수 선택.

- **📢 섹션 요약 비유**: 좋은 회귀 모델은 좋은 팀 편성처럼, 서로 다른 역할을 하는 선수들로 구성되어야(다중공선성 없음) 각자의 기여를 정확히 측정하고 미래를 정확히 예측할 수 있어.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| OLS | 최소 자승법, BLUE · 선형 회귀 추정 |
| VIF | 다중공선성 진단 · 변수 선택 |
| Adjusted R² | 모델 비교 · 변수 추가 여부 판단 |
| Ridge/[[102_lasso_ridge_regression_regularization|Lasso]] | [[093_normalization|정규화]], 과적합 방지 · 고차원 [[001_dikw_pyramid|데이터]] |
| 잔차 진단 | 등분산성, 정규성 · 가정 위배 탐지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[최소 자승법 · BLUE] → [회귀 분석: OLS · VIF] → [등분산성 · 정규성]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 회귀 분석은 점들이 찍힌 종이에서 가장 잘 맞는 선을 긋는 거야 — OLS는 모든 점과 선의 거리 제곱합이 가장 작은 선을 찾아줘.
2. 다중공선성은 여러 [[167_sql_hint_optimizer_override|힌트]] 중에 완전히 똑같은 [[167_sql_hint_optimizer_override|힌트]]가 있으면 정답을 맞히기 어려운 것처럼, 비슷한 변수들이 겹치면 모델이 헷갈려.
3. VIF는 이 겹침이 얼마나 심한지 알려주는 숫자야 — 10보다 크면 "이건 너무 겹쳐!"라는 경고야!
