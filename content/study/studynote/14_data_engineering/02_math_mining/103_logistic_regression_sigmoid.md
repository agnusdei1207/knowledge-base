+++
weight = 103
title = "로지스틱 회귀 (Logistic Regression) 및 시그모이드 (Sigmoid) 함수"
date = "2024-05-22"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]])는 '회귀'라는 이름을 가졌지만, 실제로는 결과값을 0과 1 사이의 [[130_probability|확률]]로 변환하여 두 범주 중 하나를 예측하는 '이진 [[104_classification_analysis|분류]] (Binary [[107_classification|Classification]])' 알고리즘이다.
> 2. **가치**: [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) 함수를 통해 무한대 범위의 선형 결합 결과를 [[130_probability|확률]](0~1)로 압축하며, 각 변수가 결과에 미치는 영향력을 수학적으로 해석할 수 있다.
> 3. **판단 포인트**: 복잡한 딥러닝(비선형)으로 넘어가기 전, 선형적인 [[083_relationship_in_er_model|관계]]를 바탕으로 결과를 빠르고 명확하게 설명해야 하는 금융(신용평가) 및 의료(질병 진단) 실무에서 [[159_baseline_requirements_configuration_management|베이스라인]]([[025_baseline|Baseline]]) 모델로 채택된다.

---

## Ⅰ. 개요 및 필요성

[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]])는 독립 변수들의 선형 결합을 이용하여 사건의 발생 가능성을 예측하는 통계 기법이다. 선형 회귀(Linear Regression)는 주택 가격처럼 연속적인 숫자를 예측하는 데는 적합하지만, "스팸 메일인가 아닌가?", "암인가 아닌가?" 같은 이산적인(0 또는 1) [[104_classification_analysis|분류]] 문제에 적용하면 결과값이 1을 초과하거나 0 미만으로 떨어지는 치명적인 문제가 발생한다.

이러한 선형 회귀의 한계를 극복하기 위해, 어떤 실수 값을 입력해도 항상 0과 1 사이의 값으로 맵핑([[010_schema_mapping|Mapping]])해주는 장치가 필요해졌다. 이 역할을 수행하는 것이 바로 [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) 함수이며, 이를 통해 우리는 산출된 값을 "사건이 발생할 [[130_probability|확률]]"로 합리적으로 해석할 수 있게 된다. 

- **📢 섹션 요약 비유**: 선형 회귀가 온도계를 보고 "내일은 25.5도일 것"이라고 숫자를 맞추는 일이라면, [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 구름의 양을 보고 "내일 비가 올 [[130_probability|확률]]은 80%"라고 이분법적 판단의 근거를 알려주는 일기예보관이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]의 핵심 메커니즘은 승산 (Odds)과 로짓 (Logit) 변환, 그리고 [[069_sigmoid_function_vanishing_gradient|시그모이드 함수]]를 통한 [[130_probability|확률]] 산출이다. 

1. **승산 (Odds)**: 성공 [[130_probability|확률]]($P$)과 실패 [[130_probability|확률]]($1-P$)의 비율이다. ($Odds = P / (1-P)$)
2. **로짓 (Logit) 변환**: 승산에 자연로그를 취해, $0 \sim 1$ 사이의 [[130_probability|확률]]을 $-\infty \sim +\infty$ 범위의 실수로 확장한다. 이를 통해 선형 회귀식($\beta_0 + \beta_1 X$)과 연결 고리를 만든다.
3. **[[069_sigmoid_function_vanishing_gradient|시그모이드 함수]] ([[268_sigmoid_vanishing_gradient|Sigmoid]] Function)**: 로짓 함수의 역함수로, 무한대의 선형식 결과를 다시 $0 \sim 1$ 사이의 곡선으로 압축한다. $\sigma(z) = 1 / (1 + e^{-z})$

```text
┌──────────────────────────────────────────────────────────────┐
│                  로지스틱 회귀의 데이터 변환 흐름                 │
├──────────────────────────────────────────────────────────────┤
│ 1. [입력 데이터 X] ───▶ 선형 결합 (Linear Combination)          │
│                          z = β0 + β1X1 + β2X2 + ...          │
│                                 │                            │
│ 2. [시그모이드 S-곡선] ◀──────────┘                            │
│      1.0 ┤         .──────                                   │
│          │       /                                           │
│      0.5 ┤   ──*── (임계값 Threshold)                        │
│          │    /                                              │
│      0.0 ┤──/───────────  (z값)                              │
│                                 │                            │
│ 3. [출력 확률 P] ◀───────────────┘                            │
│      P > 0.5 이면 클래스 1 (합격/양성)                          │
│      P ≤ 0.5 이면 클래스 0 (불합격/음성)                         │
└──────────────────────────────────────────────────────────────┘
```

최적의 파라미터($\beta$)를 찾을 때 선형 회귀는 최소제곱법([[076_mse_mean_squared_error_regression|MSE]])을 쓰지만, [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 [[332_maximum_likelihood_estimation_mle|최대 우도 추정법]] ([[143_mle|MLE]], Maximum Likelihood Estimation)을 사용하여 실제 관측치가 나올 [[130_probability|확률]]을 가장 극대화하는 계수를 찾는다.

- **📢 섹션 요약 비유**: [[069_sigmoid_function_vanishing_gradient|시그모이드 함수]]는 압축기다. 제아무리 거대한 숫자(+10000)나 작은 숫자(-10000)가 들어와도, 강제로 0과 1 사이의 부드러운 S자 미끄럼틀 안에 가둬버려 '[[130_probability|확률]]'이라는 예쁜 포장지로 묶어낸다.

---

## Ⅲ. 비교 및 연결

[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 [[104_classification_analysis|분류]] 문제를 푸는 가장 기초적인 방법이므로, 목적과 형태가 다른 알고리즘들과 경계를 명확히 해야 한다.

| 항목 | 선형 회귀 (Linear) | [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] (Logistic) | [[270_softmax|소프트맥스]] 회귀 ([[270_softmax|Softmax]]) |
| :--- | :--- | :--- | :--- |
| **목적** | 연속형 수치 예측 | 이진 [[104_classification_analysis|분류]] (Binary) | 다중 [[104_classification_analysis|분류]] (Multi-class) |
| **[[129_activation_function|활성화 함수]]** | 항등 함수 (Identity) | [[268_sigmoid_vanishing_gradient|시그모이드]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) | [[270_softmax|소프트맥스]] ([[270_softmax|Softmax]]) |
| **오차 함수** | 평균 제곱 오차 ([[076_mse_mean_squared_error_regression|MSE]]) | 교차 [[151_entropy|엔트로피]] ([[154_cross_entropy|Cross-Entropy]])| 교차 [[151_entropy|엔트로피]] ([[154_cross_entropy|Cross-Entropy]])|
| **결과 해석** | 단위 변화 당 값 증감 | 단위 변화 당 승산(Odds) 증감 | 클래스 간 상대적 [[130_probability|확률]] 비교 |

[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]가 두 개의 선택지(합격/불합격)만 처리한다면, [[270_softmax|소프트맥스]] 회귀는 이를 확장하여 여러 선택지(A학점/B학점/C학점)의 [[130_probability|확률]] 합이 1이 되도록 일반화한 모델이다. 또한 [[069_sigmoid_function_vanishing_gradient|시그모이드 함수]]와 [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]의 구조는 딥러닝 신경망에서 가장 작은 단위인 **[[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] ([[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]])**의 활성화 과정과 완벽히 동일하다.

- **📢 섹션 요약 비유**: 선형 회귀가 주관식 답안의 점수를 맞추는 것이라면, [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 O/X 퀴즈의 정답을 찍는 것이고, [[270_softmax|소프트맥스]]는 4지선다 객관식의 정답을 고르는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 블랙박스(Black-box) 성향의 딥러닝과 달리, '설명 가능한 [[190_ai_llm_requirements_specification|AI]] ([[227_xai_explainable_ai_lime_shap|XAI]])'가 필수적인 도메인에서 절대적인 우위를 가진다. 신용대출 승인 거절 시, 고객에게 "AI가 안 된다고 합니다"가 아니라 "연체 횟수 변수의 회귀 계수가 높아 거절 [[130_probability|확률]]이 80%를 넘었습니다"라고 수학적으로 증명할 수 있기 때문이다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]] 및 의사결정

1. **임계값 (Threshold) 튜닝**: 기본 임계값은 0.5지만 목적에 따라 조정해야 한다. 암 진단처럼 병을 놓치지 않는 것([[092_recall_sensitivity_hit_rate|재현율]], [[254_recall_sensitivity|Recall]] 중시)이 중요하면 0.3으로 낮추고, 스팸 필터처럼 정상 메일을 실수로 버리지 않는 것([[233_precision_recall_f1_roc_auc_threshold|정밀도]], [[233_precision_recall_f1_roc_auc_threshold|Precision]] 중시)이 중요하면 0.8로 높여 방어적으로 설정한다.
2. **다중공선성 ([[080_multicollinearity_vif_variance_inflation_factor_regression|Multicollinearity]]) 점검**: 입력 변수끼리 상관관계가 너무 높으면 회귀 계수가 왜곡되므로, VIF(분산팽창지수)를 확인하고 변수를 제거해야 한다.
3. **선형성 가정의 한계**: [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 기본적으로 X와 로짓 간의 '선형 [[083_relationship_in_er_model|관계]]'를 가정한다. 비선형적인 복잡한 패턴이 강하다면 [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]])나 비선형 SVM으로 넘어가야 한다.

- **📢 섹션 요약 비유**: 임계값 튜닝은 보안 검색대의 민감도를 조절하는 것과 같다. 도둑을 무조건 잡으려면 민감도를 올려 모든 사람의 주머니를 뒤져야 하고([[254_recall_sensitivity|Recall]]), 무고한 시민의 불편을 줄이려면 확실한 사람만 잡아야([[233_precision_recall_f1_roc_auc_threshold|Precision]]) 한다.

---

## Ⅴ. 기대효과 및 결론

[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 모델 학습 비용이 매우 저렴하고 배포가 가벼워 대용량 트래픽 환경의 실시간 [[104_classification_analysis|분류]]기로 적합하다. 또한 각 변수의 통계적 유의성([[337_p_value_significance|p-value]])을 명확하게 뽑아낼 수 있어, [[001_dikw_pyramid|데이터]]가 가진 패턴의 '이유'를 비즈니스 조직에 설득하는 데 강력한 힘을 발휘한다.

결론적으로, 아무리 화려하고 복잡한 [[257_ensemble_learning|앙상블]]([[257_ensemble_learning|Ensemble]]) 기법이나 딥러닝이 등장해도 [[001_dikw_pyramid|데이터]] 과학의 파이프라인에서 가장 먼저 시도해야 할 '[[159_baseline_requirements_configuration_management|베이스라인]]([[025_baseline|Baseline]]) 모델'은 변함없이 [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]다. 단순함과 해석력, 통계적 엄밀함을 모두 갖춘 [[104_classification_analysis|분류]] 문제의 근간으로 기억해야 한다.

- **📢 섹션 요약 비유**: [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 화려한 최신식 스마트워치가 아니라 튼튼하고 정확한 아날로그 나침반이다. 복잡한 길을 찾기 전에, 우선 동서남북의 기본 방향이 어디인지 가장 빠르고 확실하게 알려준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[332_maximum_likelihood_estimation_mle|최대 우도 추정법]] ([[143_mle|MLE]]) | [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]가 최적의 파라미터를 찾아내는 통계적 학습 방법 |
| 교차 [[151_entropy|엔트로피]] ([[154_cross_entropy|Cross-Entropy]]) | 예측 [[130_probability|확률]]과 실제 정답(0 또는 1) 간의 정보량 차이를 계산하는 [[075_loss_function_cost_function|손실 함수]] |
| [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] ([[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]]) | 신경망의 기본 단위로, [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] 알고리즘과 수학적 구조가 동일 |
| 설명 가능한 [[190_ai_llm_requirements_specification|AI]] ([[227_xai_explainable_ai_lime_shap|XAI]]) | 결과 도출의 이유를 해석할 수 있는 특징 덕분에 [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]가 부합하는 방향성 |

### 📈 관련 키워드 및 발전 흐름도

```text
선형 예측의 한계 (Linear Regression)
    │
    ▼
승산 및 로짓 변환 (Odds & Logit)
    │
    ▼
확률 매핑 함수 도입 (Sigmoid Function)
    │
    ▼
이진 분류의 표준 (Logistic Regression)
    │
    ▼
다중 분류 (Softmax) 및 신경망(Deep Learning)으로 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. 선형 회귀는 친구가 던진 공이 날아간 거리를 줄자로 정확히 재는 거예요.
2. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]는 친구가 던진 공이 바구니에 '들어갈지 안 들어갈지'를 퍼센트 [[130_probability|확률]]로 알려주는 마법 안경이에요.
3. 숫자가 너무 크거나 작아도, '[[268_sigmoid_vanishing_gradient|시그모이드]]'라는 미끄럼틀을 타면 무조건 0퍼센트와 100퍼센트 사이로 예쁘게 맞춰진답니다.
