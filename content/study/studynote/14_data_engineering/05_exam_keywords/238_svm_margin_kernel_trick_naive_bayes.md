+++
weight = 238
title = "238. SVM (Support Vector Machine) 마진 커널 트릭 나이브 베이즈 (Naive Bayes)"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SVM([[084_support_association_rule_transaction|Support]] Vector Machine)은 클래스 간 마진(Margin)을 최대화하는 하이퍼플레인(Hyperplane)을 찾는 [[104_classification_analysis|분류]]기로, 서포트 벡터([[084_support_association_rule_transaction|Support]] Vector)만이 결정 경계를 결정한다.
> 2. **가치**: [[059_kernel_trick_rbf_polynomial|커널 트릭]]([[059_kernel_trick_rbf_polynomial|Kernel Trick]])은 저차원 비선형 [[001_dikw_pyramid|데이터]]를 고차원 공간에 암묵적으로 매핑해 선형 분리를 가능하게 하며, 명시적 변환 없이 내적 연산만으로 구현된다.
> 3. **판단 포인트**: SVM은 고차원 소규모 [[001_dikw_pyramid|데이터]](텍스트, 생물정보)에 강점이 있고, [[264_naive_bayes|나이브 베이즈]]([[078_Naive_Bayes|Naive Bayes]])는 학습이 빠르고 소규모 [[001_dikw_pyramid|데이터]]에 효과적이어서 스팸 필터 등 실시간 [[104_classification_analysis|분류]]의 [[159_baseline_requirements_configuration_management|베이스라인]]으로 활용된다.

## Ⅰ. 개요 및 필요성

### 선형 [[104_classification_analysis|분류]]기의 딜레마

같은 [[001_dikw_pyramid|데이터]]를 선형으로 분리할 수 있는 직선(하이퍼플레인)은 무한히 많다. 어떤 것이 가장 좋은가?

```
        ○  ○                ○  ○
    ○       ○           ○       ○
        ●  ●    A선          ●  ●
    ●       ●  /         ●       ●
              /                B선
    ● = 클래스 1              \
    ○ = 클래스 2               \

  A선과 B선 모두 훈련 오류 0이지만
  A선은 마진이 좁아 새 데이터에 취약
  B선(최대 마진)이 일반화 성능 높음
```

SVM의 핵심 아이디어: **마진을 최대화하는 유일한 하이퍼플레인을 찾는다.**

📢 **섹션 요약 비유**: SVM은 두 팀 사이에 가장 넓은 통로를 만드는 것이다. 양 팀에서 가장 가까운 선수(서포트 벡터)까지의 거리(마진)를 최대로 하는 중앙선을 그린다.

## Ⅱ. 아키텍처 및 핵심 원리

### SVM 최대 마진 [[104_classification_analysis|분류]]기

```
하이퍼플레인: w·x + b = 0

마진 (Margin) = 2 / ||w||

서포트 벡터 (Support Vector):
  양성 경계: w·x + b = +1
  음성 경계: w·x + b = -1

최적화 목표: ||w||를 최소화 (마진 최대화)
  subject to: y_i(w·x_i + b) ≥ 1  for all i

ASCII 구조:
  ─────────────────────────────────────────
           ◉ ← 서포트 벡터 (양성)
       ○  |마|  ●
     ○    |진|    ●
       ○  |  |  ●
           ◉ ← 서포트 벡터 (음성)
  ─────────────────────────────────────────
       ↑         ↑
   양성 경계  음성 경계
         하이퍼플레인 (w·x+b=0)
```

### 소프트 마진 (Soft Margin) — C 파라미터

현실 [[001_dikw_pyramid|데이터]]는 완전히 선형 분리되지 않는다. 소프트 마진은 일부 오분류를 허용한다.

```
최적화: minimize ||w||² + C × Σξ_i
  ξ_i: 슬랙 변수 (오분류 허용량)
  C: 정규화 파라미터

┌──────────────────────────────────────────────┐
│    C 파라미터 효과                              │
├──────────────────┬───────────────────────────┤
│  C 작음 (넓은 마진)│  C 큼 (좁은 마진)           │
│  일부 오분류 허용  │  오분류 강하게 페널티        │
│  고편향, 저분산    │  저편향, 고분산              │
│  → 과소적합 위험  │  → 과적합 위험              │
└──────────────────┴───────────────────────────┘
```

### [[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]])

비선형 [[104_classification_analysis|분류]] 문제를 고차원 공간에서 선형 문제로 변환하는 핵심 기법이다.

```
원리:
  저차원 비선형 데이터   →   고차원 선형 분리 가능
  (직접 매핑 불필요)         (커널 함수로 내적만 계산)

K(x_i, x_j) = φ(x_i) · φ(x_j)
  → φ()는 명시적 계산 불필요!

비선형 분류 예시:
  1차원: ●●○○●●  (선형 분리 불가)
        │
        ▼ 커널 매핑
  2차원: ○○  ← 위
         ●●  ← 아래  (선형 분리 가능!)
```

### 주요 [[022_kernel_role|커널]] 함수 비교

| [[022_kernel_role|커널]] | 공식 | 적합 상황 | 하이퍼파라미터 |
|:---|:---|:---|:---|
| 선형 (Linear) | K(x,y) = x·y | 선형 분리 가능 [[001_dikw_pyramid|데이터]] | 없음 |
| 다항 ([[195_polynomial_generator_crc|Polynomial]]) | K(x,y) = (x·y + c)^d | 중간 복잡도 | d (차수), c |
| **RBF (Radial Basis Function)** | K(x,y) = exp(-γ||x-y||²) | **가장 범용** | γ (방사폭) |
| [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) | K(x,y) = [[070_hyperbolic_tangent_tanh_activation|tanh]](αx·y + c) | 신경망 유사 | α, c |

**RBF [[022_kernel_role|커널]] γ 파라미터 효과:**
```
γ 작음: 넓은 영향권 → 부드러운 경계 → 고편향(과소적합)
γ 큼:  좁은 영향권 → 복잡한 경계 → 고분산(과적합)
```

### [[264_naive_bayes|나이브 베이즈]] ([[078_Naive_Bayes|Naive Bayes]]) [[104_classification_analysis|분류]]기

베이즈 정리(Bayes' Theorem)와 조건부 독립(Conditional [[133_independence|Independence]]) 가정을 결합한 [[130_probability|확률]]적 [[104_classification_analysis|분류]]기이다.

```
베이즈 정리:
  P(C|x₁,...,xₙ) = P(C) × P(x₁,...,xₙ|C) / P(x₁,...,xₙ)

나이브 가정 (Conditional Independence):
  P(x₁,...,xₙ|C) = P(x₁|C) × P(x₂|C) × ... × P(xₙ|C)
  → 피처들이 서로 독립 (실제로는 성립 안 해도 잘 동작!)

최종 분류:
  ĉ = argmax_C [ P(C) × ∏ P(xᵢ|C) ]
```

**스팸 필터링 예시:**
```
P(스팸 | "할인", "무료", "지금") 
  = P(스팸) × P("할인"|스팸) × P("무료"|스팸) × P("지금"|스팸)
  vs
P(정상 | "할인", "무료", "지금")
  = P(정상) × P("할인"|정상) × ...

더 큰 쪽을 클래스로 선택
```

📢 **섹션 요약 비유**: [[264_naive_bayes|나이브 베이즈]]는 "이 메일에 '무료'와 '할인'이 있으면 스팸일 [[130_probability|확률]]이 얼마나 올라가는지" 각 단어를 독립적으로 계산해 빠르게 판단하는 방법이다.

## Ⅲ. 비교 및 연결

### SVM vs [[264_naive_bayes|나이브 베이즈]] vs [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]

| 항목 | SVM | [[264_naive_bayes|나이브 베이즈]] | [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] |
|:---|:---|:---|:---|
| 원리 | 마진 최대화 | 베이즈 [[130_probability|확률]]론 | [[268_sigmoid_vanishing_gradient|시그모이드]] [[568_logs_distributed_logging_elk_fluentd|로그]] 오즈 |
| 학습 속도 | 느림 (O(n²~n³)) | ⚡ 매우 빠름 | 빠름 |
| [[130_probability|확률]] 출력 | ❌ (거리 기반) | ✅ | ✅ |
| 비선형 | ✅ ([[022_kernel_role|커널]]) | ❌ | ❌ (기본) |
| 고차원 | ✅ 강점 | ✅ | 보통 |
| 과적합 [[003_resistance|저항]] | ✅ (마진) | ✅ | 보통 |
| 적합 [[064_relation_domain|도메인]] | 텍스트·이미지 | 스팸·문서 [[104_classification_analysis|분류]] | 이진 [[104_classification_analysis|분류]] 일반 |

### [[264_naive_bayes|나이브 베이즈]] 변형

| 변형 | 적합 [[001_dikw_pyramid|데이터]] | 특징 |
|:---|:---|:---|
| 가우시안 [[264_naive_bayes|나이브 베이즈]] (Gaussian NB) | 연속 [[247_feature_label_variables|피처]] | [[138_normal_distribution|정규 분포]] 가정 |
| 다항 [[264_naive_bayes|나이브 베이즈]] (Multinomial NB) | 단어 빈도 | 텍스트 [[104_classification_analysis|분류]] |
| 베르누이 [[264_naive_bayes|나이브 베이즈]] (Bernoulli NB) | 이진 [[247_feature_label_variables|피처]] | 단어 존재/부재 |

📢 **섹션 요약 비유**: SVM은 두 군중 사이에 가장 넓은 길을 만드는 것, [[059_kernel_trick_rbf_polynomial|커널 트릭]]은 납작한 지도를 3D로 올려 분리선을 그린 뒤 다시 내려놓는 마법이다.

## Ⅳ. 실무 적용 및 기술사 판단

### SVM 적용 파이프라인

```
데이터 준비        전처리         모델 선택       튜닝
[원시 데이터] → [정규화]    → [커널 선택] → [C, γ/d]
                (필수!!)       Linear?       GridSearch
                표준화          RBF?          CV 평가
                MinMaxScaler    Poly?
```

**SVM에서 [[247_feature_label_variables|피처]] 스케일링이 필수인 이유:**
```
거리 기반 알고리즘 → 피처 단위에 민감
예: 나이(0~100) vs 연봉(0~10,000,000)
  → 연봉이 마진 계산을 지배
  → StandardScaler 또는 MinMaxScaler 전처리 필수
```

### 기술사 판단 포인트

1. **고차원 희소 [[001_dikw_pyramid|데이터]] (텍스트)**: 선형 SVM이 RBF보다 빠르고 효과적인 경우 많음
2. **소규모 [[001_dikw_pyramid|데이터]]**: SVM은 소규모에서 강점, 수백만 건 이상이면 SGD 기반 Linear SVM
3. **실시간 [[104_classification_analysis|분류]] [[159_baseline_requirements_configuration_management|베이스라인]]**: [[264_naive_bayes|나이브 베이즈]] → 빠르고 간단, 먼저 시도
4. **[[130_probability|확률]] 출력 필요**: SVM은 Platt Scaling 추가 필요, [[264_naive_bayes|나이브 베이즈]]/로지스틱은 기본 제공

📢 **섹션 요약 비유**: SVM은 정교한 경계선 긋기, [[264_naive_bayes|나이브 베이즈]]는 빠른 [[130_probability|확률]] 계산기다. 급하면 [[264_naive_bayes|나이브 베이즈]]로 먼저 시도하고, 정확도가 중요하면 SVM을 튜닝한다.

## Ⅴ. 기대효과 및 결론

### 텍스트 [[104_classification_analysis|분류]] [[282_performance_tactics|성능]] 비교 (스팸 필터링)

| 모델 | Accuracy | [[255_f1_score|F1 Score]] | 학습 시간 |
|:---|:---:|:---:|:---:|
| [[264_naive_bayes|나이브 베이즈]] | 97.2% | 0.971 | ⚡ 0.01s |
| 선형 SVM | 98.5% | 0.984 | 0.5s |
| RBF SVM | 98.1% | 0.980 | 12s |
| [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] | 97.8% | 0.977 | 0.2s |

### 결론

SVM은 마진 최대화라는 우아한 수학적 원리로 고차원·소규모 [[001_dikw_pyramid|데이터]]에서 강력한 [[282_performance_tactics|성능]]을 보인다. [[059_kernel_trick_rbf_polynomial|커널 트릭]]은 특히 비선형 [[104_classification_analysis|분류]]에서 차원의 저주를 우회하는 핵심 기법이다. [[264_naive_bayes|나이브 베이즈]]는 가정(조건부 독립)이 불완전하지만 실제 [[282_performance_tactics|성능]]이 놀랍도록 좋아 텍스트 [[104_classification_analysis|분류]]의 강력한 [[159_baseline_requirements_configuration_management|베이스라인]]으로 여전히 활용된다.

📢 **섹션 요약 비유**: SVM은 정밀한 경계선 장인, [[264_naive_bayes|나이브 베이즈]]는 빠른 [[130_probability|확률]] 요리사다. 장인은 작품 하나에 공을 들이고, 요리사는 빠르게 맛있는 음식을 낸다—상황에 맞게 선택하면 된다.

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 핵심 원리 | SVM ([[084_support_association_rule_transaction|Support]] Vector Machine) | 최대 마진 [[104_classification_analysis|분류]]기 |
| 핵심 요소 | 서포트 벡터 ([[084_support_association_rule_transaction|Support]] Vector) | 결정 경계 결정하는 경계 샘플 |
| 파라미터 | C (소프트 마진) | 오분류 허용량 조절 |
| 비선형 확장 | [[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]]) | 암묵적 고차원 매핑 |
| 대표 [[022_kernel_role|커널]] | RBF [[022_kernel_role|커널]] | 가장 범용적인 [[022_kernel_role|커널]] |
| [[130_probability|확률]] [[104_classification_analysis|분류]]기 | [[264_naive_bayes|나이브 베이즈]] ([[078_Naive_Bayes|Naive Bayes]]) | 베이즈+조건부 독립 |
| 응용 | 스팸 필터링 | [[264_naive_bayes|나이브 베이즈]] 대표 사례 |

### 👶 어린이를 위한 3줄 비유 설명

1. SVM은 파란 공과 빨간 공 사이에 가장 넓은 길을 만들어 분리하는 것이다—그 경계 바로 옆의 공들(서포트 벡터)이 길의 너비를 결정한다.

### 📈 관련 키워드 및 발전 흐름도

```text
선형 분류 (퍼셉트론)
    │
    ▼
SVM: 최대 마진 초평면 + 커널 트릭 (비선형 매핑)
    │
    ▼
나이브 베이즈: 조건부 독립 가정 분류
    │
    ▼
앙상블: Random Forest · XGBoost → 딥러닝
```
2. [[059_kernel_trick_rbf_polynomial|커널 트릭]]은 평평한 종이에 섞인 점을 분리하기 어려울 때 종이를 3D로 구겨 올리면 선을 그을 수 있게 되는 마법이다.
3. [[264_naive_bayes|나이브 베이즈]]는 "무료"라는 단어가 스팸 메일에 많이 나온다는 과거 통계를 보고 새 메일이 스팸인지 빠르게 판단하는 [[130_probability|확률]] 계산기다.
