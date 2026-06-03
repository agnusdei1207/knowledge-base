---
title: 355. 랜덤 포레스트 변수 중요도 (Feature Importance)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]])의 변수 중요도(Feature Importance)는 각 특성(Feature)이 모든 트리에서 분할 시 불순도(Gini/[[151_entropy|Entropy]])를 얼마나 감소시켰는지의 가중 평균으로, 예측에 가장 기여한 특성을 수치화한다.
> 2. **가치**: 블랙박스 [[257_ensemble_learning|앙상블]] 모델에서 어떤 변수가 중요한지 자동으로 파악할 수 있어, 특성 선택(Feature [[022_mcts_four_stages|Selection]])과 [[064_relation_domain|도메인]] [[395_verification_process_review|검증]]([[177_dv_domain_validation_certificate|Domain Validation]])에 활용된다.
> 3. **판단 포인트**: MDI(Mean Decrease Impurity)는 연속형 변수나 고유값 많은 범주형 변수에 편향([[094_bias|Bias]])되므로, 순열 중요도(Permutation Importance, MDA)를 함께 사용해야 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]이 높다.

---

## Ⅰ. 개요 및 필요성

[[353_random_forest|랜덤 포레스트]]는 수백~수천 개의 결정 트리를 [[259_bagging_random_forest|배깅]]([[259_bagging_random_forest|Bagging]])으로 [[257_ensemble_learning|앙상블]]한 모델이다. 각 트리가 훈련 [[001_dikw_pyramid|데이터]]의 부트스트랩(Bootstrap) 샘플로 독립 학습하므로 단독 트리보다 [[136_variance|분산]]이 낮다. 이 수백 개 트리에서 "어떤 특성이 분할에 가장 자주, 효과적으로 사용됐는가?"를 종합하면 [[001_dikw_pyramid|데이터]] 구조를 드러내는 변수 중요도 지도(Feature Importance Map)가 완성된다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[353_random_forest|랜덤 포레스트]]의 변수 중요도는 "500명의 심사위원(트리)이 매긴 평점 평균"이다. 500명이 각자 심사(분할)할 때 "이 기준(특성)을 쓰면 심사가 훨씬 쉬워졌다"고 투표한 횟수와 효과를 합산한 것이 중요도다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────┐
│       MDI (Mean Decrease Impurity) 계산 과정             │
├──────────────────────────────────────────────────────────┤
│  for 각 트리 t in 랜덤 포레스트:                        │
│    for 각 분할 노드 v in 트리 t (특성 j 사용):          │
│      ΔI(v) = I(부모) - [Nₗ/N·I(왼쪽) + Nᵣ/N·I(오른쪽)]│
│      → 불순도 감소량 계산                               │
│                                                          │
│  특성 j의 중요도:                                       │
│  VI(j) = (1/|T|) · Σₜ Σᵥ(특성j 사용) ΔI(v) / N(v)     │
│                                                          │
│  정규화: VI(j) = VI(j) / Σⱼ VI(j)  (합이 1이 되도록)  │
└──────────────────────────────────────────────────────────┘
```

| 방법 | 계산 방식 | 장점 | 단점 |
|:---|:---|:---|:---|
| MDI (Mean Decrease Impurity) | 트리 훈련 중 불순도 감소 합산 | 빠름, 훈련 비용 없음 | 고유값 많은 변수 편향 |
| MDA (Mean Decrease Accuracy) | 변수 순열 후 OOB [[282_performance_tactics|성능]] 변화 | 공정, 상관 변수 처리 가능 | 느림, 계산 비용 큼 |
| [[327_shap|SHAP]] | 샤플리 값 기반 기여도 | 개별 예측 설명 가능 | 매우 느림 |

- **📢 섹션 요약 비유**: MDI는 "경기 중 기록한 어시스트 통계"이고 MDA(Permutation Importance)는 "그 선수가 없을 때 팀 성적이 얼마나 떨어지는지"다. 어시스트 숫자(MDI)는 빠르지만 왜곡될 수 있고, 없을 때 성적 하락(MDA)이 진짜 기여도다.

---

## Ⅲ. 비교 및 연결

OOB(Out-Of-Bag) 오차: [[259_bagging_random_forest|배깅]]에서 각 트리는 전체 [[001_dikw_pyramid|데이터]]의 약 63.2%만 사용하므로, 나머지 36.8% (OOB 샘플)로 [[395_verification_process_review|검증]]이 자동 수행된다. [[250_cross_validation_kfold|교차 검증]] 없이 훈련과 동시에 [[395_verification_process_review|검증]] 점수를 얻는 효율적 기법이다. [[127_boosting|부스팅]]([[127_boosting|Boosting]]) 계열(XGBoost, LightGBM)도 유사한 Feature Importance를 제공하지만, gain(불순도 감소), [[267_weight_bias_activation|weight]](분할 횟수), cover(샘플 커버) 등 더 다양한 방식을 지원한다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [[009_config|설정]] | 작은 규모, 개념 학습 |
| [[353_random_forest|랜덤 포레스트]] 변수 중요도 (Feature Importance) | [[282_performance_tactics|성능]]과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [[090_service_kubernetes_network_load_balancing|서비스]] 고도화 단계 |

- **📢 섹션 요약 비유**: OOB 오차는 "일부 선수를 경기에 안 쓰고 관중석에서 보게 한 뒤 그 선수의 평가 점수로 활용"하는 것이다. 훈련에 안 쓴 선수(OOB 샘플)를 관찰자로 활용해 별도 [[395_verification_process_review|검증]] 세트 없이 모델 [[282_performance_tactics|성능]]을 평가한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

변수 중요도 실무 사용 시 주의 사항: ① 높은 상관관계를 가진 두 변수(A, B)는 MDI 중요도를 나눠가져 둘 다 낮게 나올 수 있다. ② 범주형 변수의 [[459_dummy_test_double|더미]] 인코딩 방식(원핫 vs 레이블)이 중요도 계산에 영향을 준다. ③ 재현성(Reproducibility)을 위해 random_state 고정 필수. [[327_shap|SHAP]]([[327_shap|SHapley Additive exPlanations]]) 값은 개별 예측에서 각 특성의 기여도를 섀플리 값으로 계산하여 가장 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 높은 설명을 제공한다.

- **📢 섹션 요약 비유**: 상관 변수의 MDI [[136_variance|분산]]은 "한 팀에서 쌍둥이 선수의 어시스트 통계"다. 쌍둥이 선수 A, B가 서로 패스를 주고받으면 어시스트가 절반씩 나뉘어 둘 다 중간 정도로 나온다. 실제론 한 명만 있어도 충분하지만 MDI는 이를 구분 못한다.

---

## Ⅴ. 기대효과 및 결론

[[353_random_forest|랜덤 포레스트]] 변수 중요도는 블랙박스 모델에서 해석가능성([[227_xai_explainable_ai_lime_shap|XAI]])을 얻는 가장 간단한 방법이다. 불필요한 특성을 제거해 모델 경량화, [[001_dikw_pyramid|데이터]] 수집 비용 절감, [[064_relation_domain|도메인]] 전문가와의 소통에 활용된다. SHAP과 결합하면 전역 중요도(Global Importance)와 개별 예측 설명(Local Explanation) 모두 달성할 수 있다.

- **📢 섹션 요약 비유**: 변수 중요도는 "팀 공헌도 점수표"다. [[353_random_forest|랜덤 포레스트]]라는 팀에서 500번의 경기(트리) 동안 어떤 선수(특성)가 팀 승리(불순도 감소)에 가장 많이 기여했는지 집계한 [[036_mvp|MVP]] 점수표다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[259_bagging_random_forest|배깅]] ([[259_bagging_random_forest|Bagging]]) | 부트스트랩, [[257_ensemble_learning|앙상블]] / [[353_random_forest|랜덤 포레스트]]의 기반 |
| [[327_shap|SHAP]] | 섀플리 값 / 가장 정교한 Feature Importance |
| OOB (Out-Of-Bag) | [[395_verification_process_review|검증]] / 별도 [[395_verification_process_review|검증]] 세트 없는 평가 |
| XGBoost / LightGBM | [[127_boosting|부스팅]] / 유사한 Feature Importance 제공 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [랜덤 포레스트 변수 중요도 (Feature Importance)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[353_random_forest|랜덤 포레스트]]는 500명의 전문가가 각자 [[001_dikw_pyramid|데이터]]를 보고 투표하는 AI예요.
2. 변수 중요도는 500명이 "이 정보가 결정에 얼마나 도움됐나요?"라고 평가한 평균 점수예요.
3. 점수가 높은 특성이 AI의 예측에 가장 큰 영향을 미치는 핵심 정보예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 355 / 420

← **이전**: [[354_pca_covariance|354. PCA (Principal Component Analysis)]]
**다음**: [[356_mahalanobis_distance|356. 마할라노비스 거리 (Mahalanobis Distance)]] →

---
