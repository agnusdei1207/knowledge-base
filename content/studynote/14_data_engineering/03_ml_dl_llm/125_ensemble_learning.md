---
title: 125. 앙상블 학습 (Ensemble Learning) - 여러 모델의 결합으로 성능 극대화
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[257_ensemble_learning|앙상블]] 학습은 **여러 약한 학습기(Weak Learner)를 결합하여 하나의 강한 학습기(Strong Learner)**를 만드는 기법이며, [[259_bagging_random_forest|Bagging]]·[[127_boosting|Boosting]]·Stacking이 3대 전략이다.
> 2. **가치**: 단일 의사결정 트리는 과적합되기 쉽지만, 100개 트리를 [[257_ensemble_learning|앙상블]]([[353_random_forest|Random Forest]])하면 **과적합↓·정확도↑·안정성↑**이 동시에 달성된다.
> 3. **판단 포인트**: [[259_bagging_random_forest|Bagging]]([[430_index_fast_full_scan|병렬]], [[136_variance|분산]]↓)은 [[353_random_forest|Random Forest]], [[127_boosting|Boosting]](순차, 편향↓)은 XGBoost/LightGBM이 대표이며, **Kaggle 대회 우승 솔루션의 90%+가 [[257_ensemble_learning|앙상블]]**이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    앙상블 3대 전략                                    │
├───────────────────────────────────────────────────────┤
│  [Bagging (병렬)]                                     │
│   데이터 부트스트랩 → 독립 학습기 → 다수결/평균      │
│   대표: Random Forest                                │
│                                                       │
│  [Boosting (순차)]                                    │
│   이전 모델의 오류 집중 학습 → 가중 합               │
│   대표: XGBoost, LightGBM, AdaBoost                  │
│                                                       │
│  [Stacking (적층)]                                    │
│   기본 모델 예측 → 메타 모델이 최종 예측             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Bagging은 100명에게 물어서 다수결, Boosting은 틀린 문제만 반복 연습, Stacking은 전문가 의견을 종합하는 편집장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[259_bagging_random_forest|Bagging]] vs [[127_boosting|Boosting]]

| 비교 | [[259_bagging_random_forest|Bagging]] | [[127_boosting|Boosting]] |
|:---|:---|:---|
| **학습** | [[430_index_fast_full_scan|병렬]] (독립) | **순차 (의존)** |
| **효과** | [[136_variance|분산]]↓ | **편향↓** |
| **과적합** | 강함 | 위험 있음 |
| **대표** | [[353_random_forest|Random Forest]] | **XGBoost** |

- **📢 섹션 요약 비유**: Bagging은 여러 의사가 독립 진단 후 다수결, Boosting은 한 의사가 오진한 케이스를 다음 의사가 집중 진료하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 모델 | [[257_ensemble_learning|앙상블]] |
|:---|:---|:---|
| **정확도** | 보통 | **높음** |
| **과적합** | 위험 | **안정** ([[259_bagging_random_forest|Bagging]]) |
| **해석** | 가능 | 어려움 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 [[257_ensemble_learning|앙상블]] [[001_algorithm_definition|알고리즘]]

| [[001_algorithm_definition|알고리즘]] | 유형 | 특징 |
|:---|:---|:---|
| **[[353_random_forest|Random Forest]]** | [[259_bagging_random_forest|Bagging]] | [[247_feature_label_variables|피처]] 랜덤 선택 |
| **XGBoost** | [[127_boosting|Boosting]] | [[093_normalization|정규화]]·속도 |
| **LightGBM** | [[127_boosting|Boosting]] | 대용량·빠름 |
| **CatBoost** | [[127_boosting|Boosting]] | 범주형 자동 처리 |

---

## Ⅴ. 기대효과 및 결론

[[257_ensemble_learning|앙상블]]은 **[[002_structured_data|정형 데이터]] ML의 사실상 최강 기법**이며, XGBoost/LightGBM이 Kaggle·실무에서 표준으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[259_bagging_random_forest|Bagging]]** | [[430_index_fast_full_scan|병렬]], [[136_variance|분산]]↓ ([[353_random_forest|Random Forest]]) |
| **[[127_boosting|Boosting]]** | 순차, 편향↓ (XGBoost) |
| **Stacking** | 메타 모델 결합 |
| **[[353_random_forest|Random Forest]]** | [[259_bagging_random_forest|Bagging]] + [[247_feature_label_variables|피처]] 랜덤화 |
| **XGBoost** | [[034_gradient_boosting|Gradient Boosting]] + [[093_normalization|정규화]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 의사결정 트리 (1986)]
    │
    ▼
[Bagging + Random Forest (Breiman, 2001)]
    │
    ▼
[AdaBoost (1997) → Gradient Boosting (2001)]
    │
    ▼
[XGBoost (2014) / LightGBM (2017)]
    │
    ▼
[현재: AutoML — 최적 앙상블 자동 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[257_ensemble_learning|앙상블]]은 **100명에게 물어서 다수결([[259_bagging_random_forest|Bagging]])**로 답을 정하는 거예요.
2. 또는 **틀린 문제만 반복 연습([[127_boosting|Boosting]])**해서 점수를 올리는 거예요.
3. 혼자보다 **여러 명이 모이면** 더 정확한 답을 찾을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 258

← **이전**: [[124_decision_tree|124. 의사결정 트리 (Decision Tree) - 해석 가능한 분류·회귀 알고리즘]]
**다음**: [[126_bagging_random_forest|126. Bagging & Random Forest - 배깅 앙상블과 랜덤 포레스트]] →

---
