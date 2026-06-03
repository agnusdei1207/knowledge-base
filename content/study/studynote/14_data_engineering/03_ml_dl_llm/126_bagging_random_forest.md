---
title: 126. Bagging & Random Forest - 배깅 앙상블과 랜덤 포레스트
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[259_bagging_random_forest|Bagging]](Bootstrap Aggregating)은 **학습 [[001_dikw_pyramid|데이터]]를 부트스트랩(복원 추출)으로 여러 부분 집합을 만들고, 각 부분 집합으로 독립 모델을 학습 → 다수결/평균으로 결합**하는 [[257_ensemble_learning|앙상블]] 기법이다.
> 2. **가치**: 단일 의사결정 트리는 [[001_dikw_pyramid|데이터]] 변화에 민감(높은 [[136_variance|분산]])하지만, 100개 트리를 Bagging하면 **[[136_variance|분산]]이 극적으로 감소**하여 과적합이 줄어든다.
> 3. **판단 포인트**: [[353_random_forest|Random Forest]] = [[259_bagging_random_forest|Bagging]] + **[[247_feature_label_variables|피처]] 랜덤 선택**이며, 각 트리가 전체 [[247_feature_label_variables|피처]]의 √p개만 사용하여 **트리 간 상관관계를 낮추어** [[257_ensemble_learning|앙상블]] 효과를 극대화한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Random Forest 동작                                 │
├───────────────────────────────────────────────────────┤
│  원본 데이터 (N개 샘플, p개 피처)                     │
│  ├── 부트스트랩 1 (N개 복원 추출) + √p 피처 → 트리 1│
│  ├── 부트스트랩 2 (N개 복원 추출) + √p 피처 → 트리 2│
│  ├── ...                                              │
│  └── 부트스트랩 100 → 트리 100                       │
│                                                       │
│  분류: 다수결 투표                                    │
│  회귀: 평균                                           │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Bagging은 100명의 의사가 독립 진단 후 **다수결**로 최종 진단을 내리는 것이다. Random Forest는 각 의사가 **다른 검사 항목([[247_feature_label_variables|피처]])**으로 진단하여 다양성을 높인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[259_bagging_random_forest|Bagging]] vs [[353_random_forest|Random Forest]]

| 비교 | [[259_bagging_random_forest|Bagging]] | [[353_random_forest|Random Forest]] |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]]** | 부트스트랩 | 부트스트랩 |
| **[[247_feature_label_variables|피처]]** | 전체 사용 | **√p 랜덤 선택** |
| **다양성** | [[001_dikw_pyramid|데이터]]만 | **[[001_dikw_pyramid|데이터]] + [[247_feature_label_variables|피처]]** |
| **[[282_performance_tactics|성능]]** | 좋음 | **더 좋음** |

### OOB (Out-of-Bag)
부트스트랩에서 선택되지 않은 ~37% [[001_dikw_pyramid|데이터]]로 자체 [[395_verification_process_review|검증]] → **별도 [[395_verification_process_review|검증]] 세트 불필요**.

- **📢 섹션 요약 비유**: OOB는 시험에 출제되지 않은 문제로 **자체 모의고사**를 보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 트리 | [[353_random_forest|Random Forest]] | XGBoost |
|:---|:---|:---|:---|
| **과적합** | 높음 | **낮음** | 낮음 |
| **학습** | 빠름 | [[430_index_fast_full_scan|병렬]] | 순차 |
| **해석** | 가능 | [[247_feature_label_variables|피처]] 중요도 | [[247_feature_label_variables|피처]] 중요도 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[353_random_forest|Random Forest]] 장점
1. 하이퍼파라미터 튜닝이 쉬움 (기본값도 잘 동작).
2. [[247_feature_label_variables|피처]] 중요도([[355_random_forest_feature_importance|Feature Importance]]) 제공.
3. 결측치·이상치에 강건.

---

## Ⅴ. 기대효과 및 결론

Random Forest는 **가장 안정적이고 실용적인 ML [[001_algorithm_definition|알고리즘]] 중 하나**이며, [[247_feature_label_variables|피처]] 선택·[[159_baseline_requirements_configuration_management|베이스라인]] 모델·비전문가 ML에 최적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[259_bagging_random_forest|Bagging]]** | 부트스트랩 + 다수결 |
| **[[353_random_forest|Random Forest]]** | [[259_bagging_random_forest|Bagging]] + [[247_feature_label_variables|피처]] 랜덤화 |
| **OOB** | 자체 [[395_verification_process_review|검증]] [[001_dikw_pyramid|데이터]] |
| **[[247_feature_label_variables|피처]] 중요도** | Random Forest의 해석 도구 |
| **XGBoost** | [[127_boosting|부스팅]] [[257_ensemble_learning|앙상블]] (비교 대상) |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 의사결정 트리 (CART, 1984)]
    │
    ▼
[Bagging (Breiman, 1996)]
    │
    ▼
[Random Forest (Breiman, 2001) — 피처 랜덤화 추가]
    │
    ▼
[Extra Trees (2006) — 더 랜덤한 분할]
    │
    ▼
[현재: AutoML — RF vs XGBoost 자동 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Random Forest는 **100명의 의사**가 각자 진단 후 **다수결**로 결정하는 거예요.
2. 각 의사가 **다른 검사 항목**으로 진단해서 **다양한 의견**이 모여요.
3. 혼자보다 100명이 **함께 판단하면** 훨씬 정확하답니다!
