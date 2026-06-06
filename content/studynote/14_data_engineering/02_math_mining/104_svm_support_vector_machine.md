---
title: "SVM, Support Vector Machine"
date: "2024-05-22"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서포트 벡터 머신 ([Support Vector Machine](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/), [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/))은 두 클래스 간의 거리가 최대가 되도록 결정 경계 (Hyperplane)를 찾는 기하학적 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 알고리즘이다.
> 2. **가치**: [커널 트릭](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/) ([Kernel Trick](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/))을 활용하여 저차원에서는 선형으로 분리할 수 없는 복잡한 비선형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 고차원으로 매핑해 효과적으로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 낸다.
> 3. **판단 포인트**: 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰지 않고 경계 근처의 '서포트 벡터'만 모델 학습에 사용하므로 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) ([Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))에 강건하며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모가 작고 차원이 높을 때 딥러닝보다 가성비 높은 선택이 된다.

---

## Ⅰ. 개요 및 필요성

서포트 벡터 머신 ([SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/))은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들을 두 개의 그룹으로 나눌 때, 단순히 나누는 선을 긋는 것을 넘어 "가장 여유 공간이 넓게 안전한 선을 긋는" 기계학습 모델이다. [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 및 회귀 문제에 모두 사용될 수 있으나 주로 이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 강력한 성능을 발휘한다.

단순한 [로지스틱 회귀](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) ([Logistic Regression](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 나누는 수많은 선들 중에서 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 오류만 줄이려 하기 때문에 새로운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어오면 쉽게 오작동할 수 있다. 이와 달리 SVM은 결정 경계와 가장 가까운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들 사이의 마진 (Margin)을 수학적으로 극대화함으로써 미지의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Unseen [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 대한 일반화 (Generalization) 성능을 높인다. 이 때문에 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 텍스트 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)처럼 차원이 매우 높은 문제에서 딥러닝 등장 이전에 가장 완벽한 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기로 칭송받았다.

- **📢 섹션 요약 비유**: SVM은 두 마을 사이에 국경을 그을 때, 단순히 대충 선을 긋는 것이 아니라 양쪽 마을의 가장 외곽에 있는 집(서포트 벡터)에서 최대한 멀리 떨어지도록 정확히 정중앙에 폭넓은 비무장지대(마진)를 설정하는 측량사와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SVM은 기하학적인 최적화 문제로 작동하며, 핵심 메커니즘은 초평면 (Hyperplane), 마진 극대화, 그리고 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 함수다.

```text
+--------------------------------------------------------------+
|                  SVM의 기하학적 마진 극대화                  |
+--------------------------------------------------------------+
|         (Class A)                   (Class B)                |
|             o                           x                    |
|      o             o       |       x             x           |
|           o(SV)  <-+-------+-------+->  x(SV)                |
|                    |       |       |                         |
|       Margin(-1)   | Hyperplane(0) |   Margin(+1)            |
|                 최대 거리 (Max Margin)                       |
+--------------------------------------------------------------+
```

이 그림은 결정 초평면(Hyperplane, 중앙선)과 가장 가까운 양쪽의 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트인 서포트 벡터([SV](/studynote/12_it_management/04_sdlc_testing/157_sv_schedule_variance/))를 보여준다. 마진은 이 두 서포트 벡터 사이의 폭을 의미하며, SVM은 수식 $\frac{2}{||w||}$ 를 최대화하는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 벡터 $w$를 [라그랑주 승수법](/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/) (Lagrange Multipliers)을 통해 계산해 낸다.

또한, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 선형으로 나뉘지 않을 때 SVM은 <strong><a href="/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/">커널 트릭</a> (<a href="/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/">Kernel Trick</a>)</strong>을 쓴다. RBF (Radial Basis Function)나 [다항식](/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) ([Polynomial](/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/)) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 사용해, 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 무한 차원의 공간으로 변환하는 계산 비용 없이 내적 ([Dot](/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/) Product)만으로 고차원 공간에서 평면으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 깔끔하게 갈라낸다.

- **📢 섹션 요약 비유**: 평면에 섞여 있는 빨간 구슬과 파란 구슬을 선 하나로 나눌 수 없다면, SVM은 판을 세게 내리쳐 구슬들을 공중으로 띄운 뒤(고차원 매핑), 공중에 뜬 구슬들 사이에 커다란 판자를 끼워 넣어(초평면) 완벽히 분리하는 마술을 부린다.

---

## Ⅲ. 비교 및 연결

SVM은 트리 기반의 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 기법이나 딥러닝과 확연히 다른 접근법을 취한다.

| 항목 | [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) ([Support Vector Machine](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/)) | [랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/) ([Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/)) | [심층 신경망](/studynote/10_ai/01_ai_basics/065_dnn_deep_neural_network/) (Deep Neural Network) |
| :--- | :--- | :--- | :--- |
| **작동 원리** | 기하학적 마진 극대화 (최적화) | 의사결정 나무의 다수결 (규칙 분할) | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 연쇄 업데이트 ([역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/)) |
| **특화 영역** | 고차원, 소/중규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 대규모 정형(Tabular) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 비정형(이미지/음성), 초거대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **비선형 처리** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 함수 ([Kernel Trick](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/)) | 계층적 분기 (조건문 트리) | 비선형 [활성화 함수](/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/) ([ReLU](/studynote/10_ai/03_llm_nlp/269_relu_activation/) 등) |
| **해석 가능성** | 낮음 (수학적 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 공간) | 중간 ([Feature Importance](/studynote/10_ai/05_data_science_ml/355_random_forest_feature_importance/)) | 매우 낮음 (블랙박스) |

SVM은 경계선에 위치한 소수의 서포트 벡터로만 결정되므로, 멀리 떨어져 있는 엉뚱한 노이즈 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 영향을 거의 받지 않는다(Robustness). 반면 신경망은 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 오차를 최소화하려다 전체 네트워크 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 흔들릴 수 있다. 하지만 SVM은 샘플 수가 수십만 개를 넘어가면 내적 연산량($O(N^2)$)이 폭증해 학습 시간이 비현실적으로 길어지는 뚜렷한 경계를 가진다.

- **📢 섹션 요약 비유**: [랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/)가 수십 명의 심사위원이 투표로 결정하는 '다수결 재판'이고 신경망이 수천 번의 시행착오를 거쳐 요령을 깨닫는 '[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)'라면, SVM은 단 한 번의 기하학적 공식으로 완벽한 균형점을 찾아내는 '수학자'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델을 구축할 때 SVM은 항상 강력한 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) 후보로 고려되어야 하지만, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특성에 따라 채택 여부가 갈린다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> (Scaling)</strong>: SVM은 거리 기반 알고리즘이다. 변수들의 단위 차이가 크면 마진 계산이 왜곡되므로 `StandardScaler`나 `MinMaxScaler` 적용이 필수적인가?
2. <strong><a href="/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a> 허용도 (C 하이퍼파라미터)</strong>: 소프트 마진 (Soft Margin) 전략을 사용할 때, 규제 파라미터 `C`를 어떻게 잡을 것인가? (`C`가 크면 하드 마진에 가까워져 과적합 위험, 작으면 언더피팅)
3. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수가 10만 건 이상인가? (그렇다면 RBF [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) SVM은 학습이 너무 느려지므로 선형 [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) (LinearSVC)이나 LightGBM으로 우회해야 한다)

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 수백만 건의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 무작정 RBF [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) SVM을 돌려 서버의 메모리와 CPU를 며칠씩 마비시키는 행위.
- 전처리 없이 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(몸무게 kg과 키 cm 등)를 그대로 넣어 거리 계산이 엉망이 되게 방치하는 것.

- **📢 섹션 요약 비유**: [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 튜닝은 기타 줄을 맞추는 것과 같다. 줄(C 파라미터)을 너무 팽팽하게 조이면 맑은 소리(완벽한 훈련 세트 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/))가 나지만 쉽게 끊어지고(과적합), 너무 느슨하게 풀면 소리가 뭉개진다(과소적합).

---

## Ⅴ. 기대효과 및 결론

SVM을 올바르게 활용하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특성이 복잡하게 얽혀 있는 고차원 문제(예: 수천 개의 단어가 포함된 텍스트 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)나 바이오인포매틱스 유전자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에서 딥러닝 이상의 날카롭고 안정적인 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 성능을 달성할 수 있다.

하지만 빅데이터 시대에 접어들며 초대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세트 처리의 한계로 인해 딥러닝과 트리 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 계열에 다소 주도권을 내주었다. 그럼에도 불구하고, SVM이 증명한 '마진을 통한 일반화'와 '[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 통한 차원 확장'이라는 수학적 통찰은 여전히 기계학습의 근간을 이루고 있다. SVM은 "가장 중요한 소수의 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)(서포트 벡터)에만 집중하라"는 전략적 교훈을 남긴 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공학의 위대한 클래식이다.

- **📢 섹션 요약 비유**: SVM은 무술 고수와 같다. 수많은 적([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 몰려올 때 모든 적을 다 상대하지 않고, 가장 앞장서서 위협하는 몇 명의 핵심 적(서포트 벡터)만 제압하여 전체 전선을 지켜내는 기하학적 무술의 결정체다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 결정 초평면 (Hyperplane) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 두 클래스로 분리하는 N차원 공간의 평평한 경계선 |
| [커널 트릭](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/) ([Kernel Trick](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/)) | 비선형 분리를 위해 내적 연산만으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 고차원으로 매핑하는 기법 |
| 서포트 벡터 ([Support](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) Vector) | 초평면과 가장 가까이 위치하여 마진의 크기를 결정하는 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [라그랑주 승수법](/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/) ([Lagrange Multiplier](/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/)) | 제약 조건(모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 올바르게 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)됨) 하에서 마진을 최대화하는 최적화 수학 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
퍼셉트론 (선형 분류의 기초)
    |
    v
하드 마진 SVM (선형 데이터 완벽 분리)
    |
    v
소프트 마진 SVM (노이즈 허용 및 일반화 향상)
    |
    v
커널 트릭 (Kernel Trick) 도입 (비선형 데이터 해결)
    |
    v
SVR (Support Vector Regression, 회귀 문제로의 확장)
```

이 흐름도는 단순한 선 긋기에서 시작해 오류를 수용하는 소프트 마진을 거쳐, 비선형 차원의 확장을 통해 수학적 완성도를 높여온 [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 알고리즘의 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 호랑이 팀과 사자 팀이 싸우지 않게 운동장에 가장 튼튼하고 넓은 '안전지대(마진)' 선을 긋는 똑똑한 로봇이에요.
2. 로봇은 멀리 있는 동물을 신경 쓰지 않고, 가장 앞에 나와서 으르렁거리는 동물들(서포트 벡터) 사이의 거리만 재서 선을 그어요.
3. 동물들이 너무 섞여서 선을 못 그을 때는, 마법의 돋보기([커널 트릭](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/))를 써서 입체로 띄운 다음 깔끔하게 판자로 나눠버린답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 104 / 258

<- **이전**: [로지스틱 회귀 (Logistic Regression) 및 시그모이드 (Sigmoid) 함수](/studynote/14_data_engineering/02_math_mining/103_logistic_regression_sigmoid/)
**다음**: [TF-IDF 및 코사인 유사도 (TF-IDF & Cosine Similarity)](/studynote/14_data_engineering/02_math_mining/105_tf_idf_cosine_similarity/) ->

---
