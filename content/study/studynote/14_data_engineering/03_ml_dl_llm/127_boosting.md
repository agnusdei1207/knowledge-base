+++
weight = 127
title = "127. Boosting (부스팅) - 순차적 오류 보정 앙상블 학습"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Boosting은 **이전 모델이 틀린 샘플에 [[267_weight_bias_activation|가중치]]를 높여 다음 모델이 집중 학습**하는 순차적 [[257_ensemble_learning|앙상블]] 기법이며, 약한 학습기를 순서대로 결합하여 강한 학습기를 만든다.
> 2. **가치**: Bagging이 [[136_variance|분산]]을 줄이는 데 효과적이라면, Boosting은 **편향([[094_bias|Bias]])을 줄이는 데 탁월**하여 더 정확한 모델을 만들며, XGBoost·LightGBM이 Kaggle 우승의 대부분을 차지한다.
> 3. **판단 포인트**: [[077_Adaboost|AdaBoost]]([[267_weight_bias_activation|가중치]])→[[034_gradient_boosting|Gradient Boosting]](잔차)→XGBoost([[093_normalization|정규화]])→LightGBM(대용량)→CatBoost(범주형)의 발전을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Boosting 동작 원리                                 │
├───────────────────────────────────────────────────────┤
│  Round 1: 모델₁ 학습 → 오분류 샘플 가중치↑          │
│  Round 2: 모델₂ 학습 (가중치 높은 샘플 집중)         │
│  Round 3: 모델₃ 학습 (이전 오류 집중 보정)           │
│  ...                                                  │
│  Round N: 모델ₙ 학습                                 │
│                                                       │
│  최종: 모든 모델의 가중 합 → 강한 학습기             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Boosting은 **틀린 문제만 반복 연습**하는 공부법이다. 1회차에서 틀린 문제를 2회차에서 집중적으로 풀면 점수가 올라간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Boosting [[001_algorithm_definition|알고리즘]] 발전

| [[001_algorithm_definition|알고리즘]] | 핵심 | 특징 |
|:---|:---|:---|
| **[[077_Adaboost|AdaBoost]]** | [[267_weight_bias_activation|가중치]] 기반 | 최초 Boosting (1997) |
| **[[034_gradient_boosting|Gradient Boosting]]** | 잔차(Residual) 학습 | 경사하강법 |
| **XGBoost** | [[093_normalization|정규화]]+[[430_index_fast_full_scan|병렬]]화 | **Kaggle 표준** |
| **LightGBM** | Leaf-wise 분할 | **대용량·빠름** |
| **CatBoost** | 범주형 자동 처리 | Ordered Boosting |

- **📢 섹션 요약 비유**: AdaBoost는 1세대 교사(틀린 학생에게 더 관심), XGBoost는 [[190_ai_llm_requirements_specification|AI]] 과외(체계적·효율적), LightGBM은 대형 학원(대규모 [[001_dikw_pyramid|데이터]]).

---

## Ⅲ. 비교 및 연결

| 비교 | [[259_bagging_random_forest|Bagging]] | Boosting |
|:---|:---|:---|
| **학습** | [[430_index_fast_full_scan|병렬]] (독립) | **순차 (의존)** |
| **효과** | [[136_variance|분산]]↓ | **편향↓** |
| **과적합** | 강건 | 위험 있음 |
| **대표** | [[353_random_forest|Random Forest]] | **XGBoost** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### XGBoost vs LightGBM

| 비교 | XGBoost | LightGBM |
|:---|:---|:---|
| **분할** | Level-wise | **Leaf-wise** |
| **속도** | 빠름 | **더 빠름** |
| **메모리** | 보통 | **적음** |
| **[[001_dikw_pyramid|데이터]]** | 중소 | **대용량** |

---

## Ⅴ. 기대효과 및 결론

Boosting은 **[[002_structured_data|정형 데이터]] ML의 최강 기법**이며, XGBoost/LightGBM이 산업·경진대회에서 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[077_Adaboost|AdaBoost]]** | 최초 Boosting ([[267_weight_bias_activation|가중치]]) |
| **XGBoost** | [[093_normalization|정규화]] [[034_gradient_boosting|Gradient Boosting]] |
| **LightGBM** | Leaf-wise, 대용량 |
| **CatBoost** | 범주형 자동 처리 |
| **GBDT** | Gradient Boosted [[124_decision_tree|Decision Tree]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[AdaBoost (Freund & Schapire, 1997)]
    │
    ▼
[Gradient Boosting (Friedman, 2001)]
    │
    ▼
[XGBoost (Chen, 2014) — Kaggle 혁명]
    │
    ▼
[LightGBM (MS, 2017) / CatBoost (Yandex, 2017)]
    │
    ▼
[현재: TabNet / AutoML — 딥러닝 vs 부스팅 융합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Boosting은 **틀린 문제만 반복 연습**하는 공부법이에요.
2. 1회차에서 틀린 문제를 **2회차에서 집중적으로** 풀면 점수가 올라요.
3. XGBoost는 이 방법의 **최고 [[288_version_ihl_tos_total_length|버전]]**이라 대회에서 항상 우승한답니다!
