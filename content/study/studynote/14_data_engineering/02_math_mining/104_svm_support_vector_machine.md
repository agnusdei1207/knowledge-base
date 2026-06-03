---
title: 서포트 벡터 머신 (SVM, Support Vector Machine)
date: '2024-05-22'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서포트 벡터 머신 ([[238_svm_margin_kernel_trick_naive_bayes|Support Vector Machine]], [[238_svm_margin_kernel_trick_naive_bayes|SVM]])은 두 클래스 간의 거리가 최대가 되도록 결정 경계 (Hyperplane)를 찾는 기하학적 [[104_classification_analysis|분류]] 알고리즘이다.
> 2. **가치**: [[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]])을 활용하여 저차원에서는 선형으로 분리할 수 없는 복잡한 비선형 [[001_dikw_pyramid|데이터]]를 고차원으로 매핑해 효과적으로 [[104_classification_analysis|분류]]해 낸다.
> 3. **판단 포인트**: 모든 [[001_dikw_pyramid|데이터]]를 쓰지 않고 경계 근처의 '서포트 벡터'만 모델 학습에 사용하므로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] ([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]])에 강건하며, [[001_dikw_pyramid|데이터]] 규모가 작고 차원이 높을 때 딥러닝보다 가성비 높은 선택이 된다.

---

## Ⅰ. 개요 및 필요성

서포트 벡터 머신 ([[238_svm_margin_kernel_trick_naive_bayes|SVM]])은 [[001_dikw_pyramid|데이터]]들을 두 개의 그룹으로 나눌 때, 단순히 나누는 선을 긋는 것을 넘어 "가장 여유 공간이 넓게 안전한 선을 긋는" 기계학습 모델이다. [[104_classification_analysis|분류]] 및 회귀 문제에 모두 사용될 수 있으나 주로 이진 [[104_classification_analysis|분류]]에서 강력한 성능을 발휘한다.

단순한 [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]])는 [[001_dikw_pyramid|데이터]]를 나누는 수많은 선들 중에서 [[130_probability|확률]] 오류만 줄이려 하기 때문에 새로운 [[001_dikw_pyramid|데이터]]가 들어오면 쉽게 오작동할 수 있다. 이와 달리 SVM은 결정 경계와 가장 가까운 [[001_dikw_pyramid|데이터]]들 사이의 마진 (Margin)을 수학적으로 극대화함으로써 미지의 [[001_dikw_pyramid|데이터]] (Unseen [[001_dikw_pyramid|Data]])에 대한 일반화 (Generalization) 성능을 높인다. 이 때문에 비정형 [[001_dikw_pyramid|데이터]]나 텍스트 [[104_classification_analysis|분류]]처럼 차원이 매우 높은 문제에서 딥러닝 등장 이전에 가장 완벽한 [[104_classification_analysis|분류]]기로 칭송받았다.

- **📢 섹션 요약 비유**: SVM은 두 마을 사이에 국경을 그을 때, 단순히 대충 선을 긋는 것이 아니라 양쪽 마을의 가장 외곽에 있는 집(서포트 벡터)에서 최대한 멀리 떨어지도록 정확히 정중앙에 폭넓은 비무장지대(마진)를 설정하는 측량사와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SVM은 기하학적인 최적화 문제로 작동하며, 핵심 메커니즘은 초평면 (Hyperplane), 마진 극대화, 그리고 [[022_kernel_role|커널]] 함수다.

```text
┌──────────────────────────────────────────────────────────────┐
│                  SVM의 기하학적 마진 극대화                  │
├──────────────────────────────────────────────────────────────┤
│         (Class A)                   (Class B)                │
│             o                           x                    │
│      o             o       │       x             x           │
│           o(SV)  <─┼───────┼───────┼─>  x(SV)                │
│                    │       │       │                         │
│       Margin(-1)   │ Hyperplane(0) │   Margin(+1)            │
│                 최대 거리 (Max Margin)                       │
└──────────────────────────────────────────────────────────────┘
```

이 그림은 결정 초평면(Hyperplane, 중앙선)과 가장 가까운 양쪽의 핵심 [[001_dikw_pyramid|데이터]] 포인트인 서포트 벡터([[157_sv_schedule_variance|SV]])를 보여준다. 마진은 이 두 서포트 벡터 사이의 폭을 의미하며, SVM은 수식 $\frac{2}{||w||}$ 를 최대화하는 [[267_weight_bias_activation|가중치]] 벡터 $w$를 [[166_lagrange_multiplier|라그랑주 승수법]] (Lagrange Multipliers)을 통해 계산해 낸다.

또한, [[001_dikw_pyramid|데이터]]가 선형으로 나뉘지 않을 때 SVM은 **[[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]])**을 쓴다. RBF (Radial Basis Function)나 [[195_polynomial_generator_crc|다항식]] ([[195_polynomial_generator_crc|Polynomial]]) [[022_kernel_role|커널]]을 사용해, 실제 [[001_dikw_pyramid|데이터]]를 무한 차원의 공간으로 변환하는 계산 비용 없이 내적 ([[519_dot_dns_over_tls|Dot]] Product)만으로 고차원 공간에서 평면으로 [[001_dikw_pyramid|데이터]]를 깔끔하게 갈라낸다. 

- **📢 섹션 요약 비유**: 평면에 섞여 있는 빨간 구슬과 파란 구슬을 선 하나로 나눌 수 없다면, SVM은 판을 세게 내리쳐 구슬들을 공중으로 띄운 뒤(고차원 매핑), 공중에 뜬 구슬들 사이에 커다란 판자를 끼워 넣어(초평면) 완벽히 분리하는 마술을 부린다.

---

## Ⅲ. 비교 및 연결

SVM은 트리 기반의 [[257_ensemble_learning|앙상블]] 기법이나 딥러닝과 확연히 다른 접근법을 취한다. 

| 항목 | [[238_svm_margin_kernel_trick_naive_bayes|SVM]] ([[238_svm_margin_kernel_trick_naive_bayes|Support Vector Machine]]) | [[353_random_forest|랜덤 포레스트]] ([[353_random_forest|Random Forest]]) | [[065_dnn_deep_neural_network|심층 신경망]] (Deep Neural Network) |
| :--- | :--- | :--- | :--- |
| **작동 원리** | 기하학적 마진 극대화 (최적화) | 의사결정 나무의 다수결 (규칙 분할) | [[267_weight_bias_activation|가중치]] 연쇄 업데이트 ([[272_backpropagation|역전파]]) |
| **특화 영역** | 고차원, 소/중규모 [[001_dikw_pyramid|데이터]] | 대규모 정형(Tabular) [[001_dikw_pyramid|데이터]] | 비정형(이미지/음성), 초거대 [[001_dikw_pyramid|데이터]] |
| **비선형 처리** | [[022_kernel_role|커널]] 함수 ([[059_kernel_trick_rbf_polynomial|Kernel Trick]]) | 계층적 분기 (조건문 트리) | 비선형 [[129_activation_function|활성화 함수]] ([[269_relu_activation|ReLU]] 등) |
| **해석 가능성** | 낮음 (수학적 [[267_weight_bias_activation|가중치]] 공간) | 중간 ([[355_random_forest_feature_importance|Feature Importance]]) | 매우 낮음 (블랙박스) |

SVM은 경계선에 위치한 소수의 서포트 벡터로만 결정되므로, 멀리 떨어져 있는 엉뚱한 노이즈 [[001_dikw_pyramid|데이터]]의 영향을 거의 받지 않는다(Robustness). 반면 신경망은 모든 [[001_dikw_pyramid|데이터]]의 오차를 최소화하려다 전체 네트워크 [[267_weight_bias_activation|가중치]]가 흔들릴 수 있다. 하지만 SVM은 샘플 수가 수십만 개를 넘어가면 내적 연산량($O(N^2)$)이 폭증해 학습 시간이 비현실적으로 길어지는 뚜렷한 경계를 가진다.

- **📢 섹션 요약 비유**: [[353_random_forest|랜덤 포레스트]]가 수십 명의 심사위원이 투표로 결정하는 '다수결 재판'이고 신경망이 수천 번의 시행착오를 거쳐 요령을 깨닫는 '[[190_ai_llm_requirements_specification|AI]]'라면, SVM은 단 한 번의 기하학적 공식으로 완벽한 균형점을 찾아내는 '수학자'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[104_classification_analysis|분류]] 모델을 구축할 때 SVM은 항상 강력한 [[159_baseline_requirements_configuration_management|베이스라인]] 후보로 고려되어야 하지만, [[001_dikw_pyramid|데이터]]의 특성에 따라 채택 여부가 갈린다.

### [[435_checklist_based_testing|체크리스트]]
1. **[[001_dikw_pyramid|데이터]] [[249_scaling_normalization_standardization|스케일링]] (Scaling)**: SVM은 거리 기반 알고리즘이다. 변수들의 단위 차이가 크면 마진 계산이 왜곡되므로 `StandardScaler`나 `MinMaxScaler` 적용이 필수적인가?
2. **[[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 허용도 (C 하이퍼파라미터)**: 소프트 마진 (Soft Margin) 전략을 사용할 때, 규제 파라미터 `C`를 어떻게 잡을 것인가? (`C`가 크면 하드 마진에 가까워져 과적합 위험, 작으면 언더피팅)
3. **[[001_dikw_pyramid|데이터]] 크기**: [[001_dikw_pyramid|데이터]] 수가 10만 건 이상인가? (그렇다면 RBF [[022_kernel_role|커널]] SVM은 학습이 너무 느려지므로 선형 [[238_svm_margin_kernel_trick_naive_bayes|SVM]] (LinearSVC)이나 LightGBM으로 우회해야 한다)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 수백만 건의 [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]]에 무작정 RBF [[022_kernel_role|커널]] SVM을 돌려 서버의 메모리와 CPU를 며칠씩 마비시키는 행위.
- 전처리 없이 원시 [[001_dikw_pyramid|데이터]](몸무게 kg과 키 cm 등)를 그대로 넣어 거리 계산이 엉망이 되게 방치하는 것.

- **📢 섹션 요약 비유**: [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 튜닝은 기타 줄을 맞추는 것과 같다. 줄(C 파라미터)을 너무 팽팽하게 조이면 맑은 소리(완벽한 훈련 세트 [[104_classification_analysis|분류]])가 나지만 쉽게 끊어지고(과적합), 너무 느슨하게 풀면 소리가 뭉개진다(과소적합).

---

## Ⅴ. 기대효과 및 결론

SVM을 올바르게 활용하면 [[001_dikw_pyramid|데이터]]의 특성이 복잡하게 얽혀 있는 고차원 문제(예: 수천 개의 단어가 포함된 텍스트 [[104_classification_analysis|분류]]나 바이오인포매틱스 유전자 [[001_dikw_pyramid|데이터]])에서 딥러닝 이상의 날카롭고 안정적인 [[104_classification_analysis|분류]] 성능을 달성할 수 있다. 

하지만 빅데이터 시대에 접어들며 초대용량 [[001_dikw_pyramid|데이터]] 세트 처리의 한계로 인해 딥러닝과 트리 [[257_ensemble_learning|앙상블]] 계열에 다소 주도권을 내주었다. 그럼에도 불구하고, SVM이 증명한 '마진을 통한 일반화'와 '[[022_kernel_role|커널]]을 통한 차원 확장'이라는 수학적 통찰은 여전히 기계학습의 근간을 이루고 있다. SVM은 "가장 중요한 소수의 [[167_sql_hint_optimizer_override|힌트]](서포트 벡터)에만 집중하라"는 전략적 교훈을 남긴 [[001_dikw_pyramid|데이터]] 공학의 위대한 클래식이다.

- **📢 섹션 요약 비유**: SVM은 무술 고수와 같다. 수많은 적([[001_dikw_pyramid|데이터]])이 몰려올 때 모든 적을 다 상대하지 않고, 가장 앞장서서 위협하는 몇 명의 핵심 적(서포트 벡터)만 제압하여 전체 전선을 지켜내는 기하학적 무술의 결정체다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 결정 초평면 (Hyperplane) | [[001_dikw_pyramid|데이터]]를 두 클래스로 분리하는 N차원 공간의 평평한 경계선 |
| [[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]]) | 비선형 분리를 위해 내적 연산만으로 [[001_dikw_pyramid|데이터]]를 고차원으로 매핑하는 기법 |
| 서포트 벡터 ([[084_support_association_rule_transaction|Support]] Vector) | 초평면과 가장 가까이 위치하여 마진의 크기를 결정하는 핵심 [[001_dikw_pyramid|데이터]] |
| [[166_lagrange_multiplier|라그랑주 승수법]] ([[166_lagrange_multiplier|Lagrange Multiplier]]) | 제약 조건(모든 [[001_dikw_pyramid|데이터]]가 올바르게 [[104_classification_analysis|분류]]됨) 하에서 마진을 최대화하는 최적화 수학 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
퍼셉트론 (선형 분류의 기초)
    │
    ▼
하드 마진 SVM (선형 데이터 완벽 분리)
    │
    ▼
소프트 마진 SVM (노이즈 허용 및 일반화 향상)
    │
    ▼
커널 트릭 (Kernel Trick) 도입 (비선형 데이터 해결)
    │
    ▼
SVR (Support Vector Regression, 회귀 문제로의 확장)
```

이 흐름도는 단순한 선 긋기에서 시작해 오류를 수용하는 소프트 마진을 거쳐, 비선형 차원의 확장을 통해 수학적 완성도를 높여온 [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 알고리즘의 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 호랑이 팀과 사자 팀이 싸우지 않게 운동장에 가장 튼튼하고 넓은 '안전지대(마진)' 선을 긋는 똑똑한 로봇이에요.
2. 로봇은 멀리 있는 동물을 신경 쓰지 않고, 가장 앞에 나와서 으르렁거리는 동물들(서포트 벡터) 사이의 거리만 재서 선을 그어요.
3. 동물들이 너무 섞여서 선을 못 그을 때는, 마법의 돋보기([[059_kernel_trick_rbf_polynomial|커널 트릭]])를 써서 입체로 띄운 다음 깔끔하게 판자로 나눠버린답니다!
