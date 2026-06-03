---
title: 351. 지니 불순도 (Gini Impurity) 와 정보 획득량 (Information Gain)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[108_gini_impurity|지니 불순도]]([[108_gini_impurity|Gini Impurity]])와 [[151_entropy|엔트로피]]([[151_entropy|Entropy]]) 기반 정보 획득량(Information Gain)은 결정 트리([[124_decision_tree|Decision Tree]])가 어느 특성(Feature)으로 [[001_dikw_pyramid|데이터]]를 분할할 때 가장 순수한(Pure) 그룹이 만들어지는지를 측정하는 분할 기준이다.
> 2. **가치**: Gini는 계산이 빠르고(CART [[001_algorithm_definition|알고리즘]] 사용), [[151_entropy|Entropy]] 기반 정보 획득량은 이론적으로 정교하나(ID3/C4.5 사용) 계산이 느리다. 실무에서 scikit-learn 기본은 Gini다.
> 3. **판단 포인트**: 순수 노드(한 클래스만)에서 Gini=0, [[151_entropy|Entropy]]=0이 되고, 완전 불순 노드(균등 분포)에서 Gini=1-1/K, [[151_entropy|Entropy]]=log₂K가 최대가 된다.

---

## Ⅰ. 개요 및 필요성

결정 트리는 [[001_dikw_pyramid|데이터]]를 이진(Binary) 질문으로 반복 분할하여 [[104_classification_analysis|분류]]한다. "나이 < 30인가? → 예/아니오"처럼 분할할 때 어떤 기준으로 가장 좋은 질문을 고르는가가 핵심이다. 무작위로 고르면 트리가 깊어지고 과적합([[245_overfitting_variance|Overfitting]])이 발생한다. 분할 후 각 그룹이 얼마나 순수한지(한 클래스만 모였는지)를 측정하는 지표가 [[108_gini_impurity|지니 불순도]]와 [[151_entropy|엔트로피]]다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 결정 트리 분할은 "사탕통 정리"다. 빨간 사탕과 파란 사탕이 섞인 통을 나눌 때, "모양으로 나눌까? 색으로 나눌까?" 중 각 통이 가장 한 가지 색으로만 가득 차는(순수한) 방법을 찾는 것이 [[108_gini_impurity|지니 불순도]]다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────┐
│         분할 기준 수식 비교                               │
├──────────────────────────────────────────────────────────┤
│  지니 불순도 (Gini Impurity):                            │
│  Gini(t) = 1 - Σ pᵢ²                                   │
│  → 완전 순수: Gini=0,  2클래스 균등: Gini=0.5           │
│                                                          │
│  엔트로피 (Entropy):                                     │
│  H(t) = -Σ pᵢ · log₂(pᵢ)                              │
│  → 완전 순수: H=0,  2클래스 균등: H=1.0 (bits)         │
│                                                          │
│  정보 획득량 (Information Gain):                         │
│  IG(D,A) = H(D) - Σ |Dᵥ|/|D| · H(Dᵥ)                 │
│                                                          │
│  예) [30 양성, 70 음성] 노드:                           │
│  Gini = 1 - (0.3² + 0.7²) = 1 - 0.58 = 0.42           │
│  H    = -(0.3·log₂0.3 + 0.7·log₂0.7) ≈ 0.881          │
└──────────────────────────────────────────────────────────┘
```

| 지표 | 수식 | 범위 | 사용 [[001_algorithm_definition|알고리즘]] |
|:---|:---|:---|:---|
| [[108_gini_impurity|지니 불순도]] | 1 - Σpᵢ² | [0, 1-1/K] | CART |
| [[151_entropy|엔트로피]] | -Σpᵢ·log₂pᵢ | [0, log₂K] | ID3, C4.5 |
| 정보 획득량 | H(부모) - 가중 H(자식) | [0, H(부모)] | ID3, C4.5 |
| 획득 비율 (GR) | IG / H(A) | [[093_normalization|정규화]]된 IG | C4.5 |

- **📢 섹션 요약 비유**: Gini는 "빠른 암산 점수", Entropy는 "정밀 계산기 점수"다. 둘 다 순수도를 측정하지만 Gini는 제곱 연산만 써서 빠르고, Entropy는 [[568_logs_distributed_logging_elk_fluentd|로그]] 연산을 써서 정밀하다. 대용량 [[001_dikw_pyramid|데이터]]에서는 빠른 Gini가 압도적으로 선호된다.

---

## Ⅲ. 비교 및 연결

정보 획득량(IG)의 단점은 다값 특성(많은 카테고리 값)에 편향([[094_bias|Bias]])된다는 것이다. 고유 ID 같은 특성은 IG가 최대가 되지만 실제로는 쓸모없다. C4.5가 획득 비율(Gain Ratio, GR) = IG/H(A)로 이를 보정했다. CART([[107_classification|Classification]] And Regression Tree)는 Gini를 사용하고 이진 분할만 지원하며, scikit-learn의 DecisionTreeClassifier 기본 기준이다. [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]])는 여러 결정 트리의 Gini 불순도 감소량을 합산하여 변수 중요도([[355_random_forest_feature_importance|Feature Importance]])를 계산한다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [[009_config|설정]] | 작은 규모, 개념 학습 |
| [[108_gini_impurity|지니 불순도]] ([[108_gini_impurity|Gini Impurity]]) 와 정보 획득량 (Information Gain) | [[282_performance_tactics|성능]]과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [[090_service_kubernetes_network_load_balancing|서비스]] 고도화 단계 |

- **📢 섹션 요약 비유**: 정보 획득량의 편향은 "학번으로 출석 체크하기"다. 학번은 학생마다 고유하니 IG가 최고지만, 출석 예측에는 무쓸모다. GR은 "이 특성이 얼마나 다양한가"로 나눠서 공정하게 보정하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

결정 트리 과적합 방지를 위한 사전 [[435_pruning_hardware|가지치기]](Pre-[[435_pruning_hardware|pruning]]): max_depth, min_samples_split, min_samples_leaf 등 파라미터 제한. 사후 [[435_pruning_hardware|가지치기]](Post-[[435_pruning_hardware|pruning]]): 비용-복잡도 [[435_pruning_hardware|가지치기]](CCP, Cost-Complexity [[435_pruning_hardware|Pruning]]) α 파라미터로 트리를 단순화. 불균형 [[001_dikw_pyramid|데이터]]에서 Gini는 다수 클래스 편향이 심해지므로 class_weight='balanced' 옵션과 함께 사용한다. 회귀 트리(Regression Tree)에서는 [[076_mse_mean_squared_error_regression|MSE]]([[076_mse_mean_squared_error_regression|Mean Squared Error]]) 감소량을 분할 기준으로 사용한다.

- **📢 섹션 요약 비유**: [[435_pruning_hardware|가지치기]]([[435_pruning_hardware|Pruning]])는 "과도하게 자란 나무 다듬기"다. 트리를 너무 깊이 자라게 두면(과적합) 훈련 [[001_dikw_pyramid|데이터]]만 완벽히 외운 쓸모없는 나무가 된다. 적당히 잘라 단순하게 만들어야 새 [[001_dikw_pyramid|데이터]](테스트)에도 잘 작동하는 강건한 나무가 된다.

---

## Ⅴ. 기대효과 및 결론

[[108_gini_impurity|지니 불순도]]와 정보 획득량은 결정 트리 계열 모델(의사결정나무, [[353_random_forest|랜덤 포레스트]], [[034_gradient_boosting|그래디언트 부스팅]])의 핵심 수학 도구다. 수식을 암기할 뿐 아니라, "왜 순수 노드에서 0이 되는가?"를 직관적으로 이해하면 기술사 답안에서 차별화된다. Gini = CART = 실무 기본, [[151_entropy|Entropy]] = ID3/C4.5 = 이론적 정교함이라는 매핑도 중요하다.

- **📢 섹션 요약 비유**: 지니와 [[151_entropy|엔트로피]]는 "두 종류의 혼탁도 측정기"다. 지니는 유리잔에 색깔 모래가 얼마나 섞였는지 눈으로 빠르게 재는 방식, [[151_entropy|엔트로피]]는 화학적으로 정밀하게 측정하는 방식이다. 둘 다 깨끗할수록(순수 노드) 0이 된다는 공통점이 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 결정 트리 ([[124_decision_tree|Decision Tree]]) | 분할 기준 / Gini/[[151_entropy|Entropy]] 적용 대상 |
| CART [[001_algorithm_definition|알고리즘]] | 이진 분할 / Gini 불순도 사용 |
| [[353_random_forest|랜덤 포레스트]] ([[353_random_forest|Random Forest]]) | [[257_ensemble_learning|앙상블]] / Gini 감소량 = [[355_random_forest_feature_importance|Feature Importance]] |
| 정보 이론 ([[150_information_theory|Information Theory]]) | [[151_entropy|엔트로피]] / Entropy의 수학적 기원 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [지니 불순도 (Gini Impurity) 와 정보 획득량 (Information Gain)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[108_gini_impurity|지니 불순도]]는 "사탕통에 빨간 사탕과 파란 사탕이 얼마나 섞여있는지"를 측정하는 숫자예요.
2. 한 가지 사탕만 있으면 지니=0 (완전 순수!), 반씩 섞여있으면 지니=0.5 (최대 혼탁!)이에요.
3. [[190_ai_llm_requirements_specification|AI]] 나무(결정 트리)는 이 혼탁도를 가장 많이 줄여주는 질문을 찾아서 [[001_dikw_pyramid|데이터]]를 나눠요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 351 / 420

← **이전**: [[350_laplace_smoothing|350. 라플라스 스무딩 (Laplace Smoothing)]]
**다음**: [[352_perceptron_linear_separability|352. 퍼셉트론 (Perceptron)]] →

---
