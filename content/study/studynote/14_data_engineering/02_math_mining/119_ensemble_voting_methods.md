+++
weight = 119
title = "119. 앙상블 보팅 (Ensemble Voting Methods) - 하드/소프트 보팅·다수결 원리"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[257_ensemble_learning|앙상블]] [[258_voting_ensemble|보팅]]은 **여러 분류기의 예측 결과를 투표([[258_voting_ensemble|Voting]])**로 결합하여 최종 예측을 도출하는 기법이며, **하드 [[258_voting_ensemble|보팅]](다수결)**과 **소프트 [[258_voting_ensemble|보팅]]([[130_probability|확률]] 평균)**으로 나뉜다.
> 2. **가치**: 단일 모델의 예측은 편향·분산에 취약하지만, 서로 다른 모델을 결합하면 **개별 모델의 약점이 상쇄**되어 일반적으로 단일 모델보다 높은 정확도를 보인다("군중의 지혜").
> 3. **판단 포인트**: 소프트 [[258_voting_ensemble|보팅]]은 [[130_probability|확률]]값의 평균을 사용하므로 **[[130_probability|확률]] 보정이 잘된 모델(calibrated)에서 더 효과적**이며, 다양성(Diversity)이 높은 모델 조합이 [[257_ensemble_learning|앙상블]] [[282_performance_tactics|성능]]의 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    하드 보팅 vs 소프트 보팅                            │
├───────────────────────────────────────────────────────┤
│  [하드 보팅 (다수결)]                                 │
│   모델 A: 고양이      모델 B: 개      모델 C: 고양이  │
│   → 다수결: 고양이 (2:1)                              │
│                                                       │
│  [소프트 보팅 (확률 평균)]                            │
│   모델 A: 고양이 0.7   모델 B: 개 0.6   모델 C: 고양이 0.9│
│   고양이 평균: (0.7+0.4+0.9)/3 = 0.67                │
│   개 평균: (0.3+0.6+0.1)/3 = 0.33                    │
│   → 소프트 보팅: 고양이 (0.67 > 0.33)                │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 하드 [[258_voting_ensemble|보팅]]은 선거(1인 1표, 다수결)이고, 소프트 [[258_voting_ensemble|보팅]]은 전문가 점수(확신도 반영)의 평균이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[258_voting_ensemble|보팅]] 유형

| 유형 | 방법 | 장점 | 적합 |
|:---|:---|:---|:---|
| **하드 [[258_voting_ensemble|보팅]]** | 다수결 | 단순 | [[130_probability|확률]] 미제공 모델 |
| **소프트 [[258_voting_ensemble|보팅]]** | [[130_probability|확률]] 평균 | **정보 활용 많음** | [[130_probability|확률]] 보정 모델 |
| **가중 [[258_voting_ensemble|보팅]]** | [[267_weight_bias_activation|가중치]] 부여 | **우수 모델 반영** | [[282_performance_tactics|성능]] 차이 큰 경우 |

### 다양성(Diversity)의 중요성
모든 모델이 같은 패턴을 학습하면 [[258_voting_ensemble|보팅]] 효과가 없다. **서로 다른 [[001_algorithm_definition|알고리즘]]([[238_svm_margin_kernel_trick_naive_bayes|SVM]]+RF+LR)**을 조합해야 약점이 상쇄된다.

- **📢 섹션 요약 비유**: 같은 과목 전문가 3명보다 국어·수학·영어 전문가 3명이 모여야 더 다양한 문제를 풀 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 모델 | [[258_voting_ensemble|보팅]] | [[259_bagging_random_forest|배깅]] | [[127_boosting|부스팅]] |
|:---|:---|:---|:---|:---|
| **다양성** | 없음 | **이종 모델** | 동종 (샘플링) | 동종 (순차) |
| **결합** | - | 투표/평균 | 평균 | 가중합 |
| **대표** | - | VotingClassifier | **[[353_random_forest|Random Forest]]** | **XGBoost** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Scikit-learn VotingClassifier
```python
from sklearn.ensemble import VotingClassifier
vc = VotingClassifier(
    estimators=[('lr', lr), ('rf', rf), ('svm', svm)],
    voting='soft'  # 소프트 보팅
)
```

---

## Ⅴ. 기대효과 및 결론

[[257_ensemble_learning|앙상블]] [[258_voting_ensemble|보팅]]은 **가장 단순하면서도 효과적인 [[257_ensemble_learning|앙상블]] 기법**이며, Kaggle 상위권 솔루션의 대부분이 [[258_voting_ensemble|보팅]]·스태킹 기반 [[257_ensemble_learning|앙상블]]을 사용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **하드 [[258_voting_ensemble|보팅]]** | 다수결, 단순 |
| **소프트 [[258_voting_ensemble|보팅]]** | [[130_probability|확률]] 평균, 정보량 많음 |
| **[[259_bagging_random_forest|배깅]]** | 동종 모델 + 샘플링 ([[353_random_forest|Random Forest]]) |
| **[[127_boosting|부스팅]]** | 동종 모델 + 순차 학습 (XGBoost) |
| **스태킹** | 메타 모델이 개별 모델 출력을 학습 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 모델 (Decision Tree, SVM)]
    │
    ▼
[보팅 (이종 모델 결합, 다수결/확률)]
    │
    ▼
[배깅 (1996, Breiman) — 동종 모델 + 샘플링]
    │
    ▼
[부스팅 (1997, AdaBoost → XGBoost)]
    │
    ▼
[현재: 스태킹 + AutoML — 자동 앙상블 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 하드 [[258_voting_ensemble|보팅]]은 **선거**예요. 3명이 투표해서 **많이 나온 답**이 정답이에요.
2. 소프트 [[258_voting_ensemble|보팅]]은 각 사람이 **얼마나 확신하는지(점수)**를 평균 내서 결정해요.
3. 여러 전문가가 모이면 **혼자보다 더 정확한 답**을 낼 수 있답니다!
