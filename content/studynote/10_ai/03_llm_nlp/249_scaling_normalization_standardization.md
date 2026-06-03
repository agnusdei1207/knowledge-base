+++
title = "249. 스케일링 (Scaling Normalization Standardization)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스케일링(Scaling)은 서로 다른 범위를 가진 수치형 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)들을 동일한 척도로 맞추어, 모델이 특정 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)에 편향되지 않고 균등하게 학습하게 하는 전처리 기법이다.
> 2. **가치**: 경사하강법([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/)) 기반 모델(선형 회귀, 신경망)과 거리 기반 모델([SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/), [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/))에서 스케일링은 수렴 속도와 예측 정확도에 직접적인 영향을 미친다.
> 3. **판단 포인트**: [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([Outlier](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))가 없으면 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/) [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)), [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 있으면 표준화(Standardization) 또는 로버스트 스케일링(Robust Scaling)을 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 스케일링이 필요한 이유
[피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)들의 단위와 범위가 다를 경우 발생하는 문제:

| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) | 범위 | 스케일링 전 영향 |
|:---|:---|:---|
| 나이 | 0 ~ 100 | 작은 값, 모델 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 영향 |
| 연봉 | 2000만 ~ 1억 | 큰 값, 모델 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 지배 |
| BMI | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ~ 40 | 중간 값 |

→ 스케일링 없이 경사하강법 적용 시 연봉 방향으로 기울어진 손실 지형(Loss Landscape) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 수렴 속도 저하 또는 발산

### 1.2 스케일링이 필수인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 스케일링 필요 여부 | 이유 |
|:---|:---|:---|
| 선형 회귀(Linear Regression) | ✅ 필요 | 경사하강법 수렴 |
| [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)([Logistic Regression](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)) | ✅ 필요 | 동일 이유 |
| [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) ([Support Vector Machine](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/)) | ✅ 필요 | 거리 기반 마진 |
| [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/) ([K-Nearest Neighbors](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/)) | ✅ 필요 | 유클리드 거리 왜곡 |
| 신경망(Neural Network) | ✅ 필요 | 그래디언트 소실/폭발 |
| 결정 트리([Decision Tree](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)) | ❌ 불필요 | 분기 기준이 절댓값 불변 |
| [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)([Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)) | ❌ 불필요 | 트리 기반 |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure │
│ New requirement │ Design decision point │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 스케일링은 달리기 경주에서 모든 선수의 출발선을 같은 위치로 맞추는 것이다. 한 선수가 1미터를 달리고 다른 선수가 1킬로미터를 달리는 경주는 공정한 비교가 되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 스케일링 기법 비교 도식

```
┌─────────────────────────────────────────────────────────┐
│ 스케일링 기법 비교 │
│ │
│ 원본 데이터 분포: │
│ ──────[min]─────────────────────[max]────── │
│ 이상치◀ ▶이상치 │
│ │
│ 1. 정규화 (Min-Max): [0, 1] 범위로 압축 │
│ ──[0]────────────────────────────────[1]── │
│ (이상치에 의해 전체 분포가 압축될 수 있음) │
│ │
│ 2. 표준화 (Z-Score): 평균=0, 표준편차=1 │
│ ────────[-3]──[-2]──[-1]──[0]──[1]──[2]──[3]── │
│ (이상치도 수치 변환되나 분포 형태는 유지) │
│ │
│ 3. 로버스트 스케일링: 중앙값, IQR 기준 │
│ ──────[Q1]───────[중앙값]───────[Q3]────── │
│ (이상치에 강건, 중앙 분포 집중) │
└─────────────────────────────────────────────────────────┘
```

### 2.2 각 기법의 수식과 특징

#### [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/) [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))
```
x' = (x - x_min) / (x_max - x_min)
→ 결과: 0 ≤ x' ≤ 1
→ 이상치 영향: 매우 큼 (이상치가 x_min 또는 x_max 결정)
```

#### 표준화 (Z-Score Standardization)
```
x' = (x - μ) / σ
→ 결과: 평균 0, 표준편차 1 (단, [0,1] 범위 보장 없음)
→ 이상치 영향: 중간 수준 (평균과 표준편차에 영향)
```

#### 로버스트 스케일링 (Robust Scaling)
```
x' = (x - 중앙값(Median)) / IQR(사분위 범위)
→ IQR = Q3 - Q1
→ 이상치 영향: 가장 적음 (중앙값과 IQR은 이상치에 강건)
```

### 2.3 경사하강법과 스케일링 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

| 조건 | 손실 지형 모양 | 수렴 특성 |
|:---|:---|:---|
| 스케일링 없음 | 길쭉한 타원형(편향된 등고선) | 지그재그로 느린 수렴 |
| 스케일링 적용 | 원형에 가까운 등고선 | 최적점으로 빠른 직선 수렴 |

- **📢 섹션 요약 비유**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 모든 것을 0~100점 척도로 바꾸는 것이고, 표준화는 "평균에서 몇 표준편차 떨어져 있냐"로 표현하는 편차 성적표 같은 것이다. [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 있는 반에서는 편차 성적표(표준화)가 더 공정하다.

---

## Ⅲ. 비교 및 연결

### 3.1 스케일링 기법 선택 가이드

| 상황 | 권장 기법 | 이유 |
|:---|:---|:---|
| [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 없음, 분포 균등 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/)) | 범위 명확, 해석 쉬움 |
| [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 있음, [정규 분포](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/) | 표준화(Z-Score) | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 영향 완화 |
| [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 다수, 치우침 심함 | 로버스트 스케일링 | 중앙값 기반으로 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 무력화 |
| 이미지 픽셀값 (0~255) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(÷255) | 0~1 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 단순 처리 |
| 신경망 입력 | 표준화 또는 [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/) | [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/) 포화 방지 |

### 3.2 Train-Test [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서의 스케일링 주의사항

**[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage) 방지 규칙:**
```
❌ 잘못된 방법: 전체 데이터(train+test)에 fit_transform
✅ 올바른 방법: train 데이터에만 fit → train/test 모두 transform

이유: 테스트 데이터는 미래 데이터를 대표해야 하므로
테스트 데이터의 통계(min, max, μ, σ)가 스케일링에 반영되면
현실적이지 않은 스케일러가 만들어짐
```

### 3.3 [배치 정규화](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/) ([Batch Normalization](/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/), BN)
딥러닝에서 레이어 내부의 활성화값을 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하는 기법:
- 각 미니배치(Mini-batch) 내에서 평균=0, 표준편차=1로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)
- 학습 속도 향상, 그래디언트 소실([Vanishing Gradient](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/)) 완화
- [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 파라미터(γ, β)를 학습으로 최적화

- **📢 섹션 요약 비유**: Train/Test 스케일링 규칙은 요리사가 국물 간을 맞출 때 손님이 먹을 국물을 시식용으로 쓰면 안 되는 것과 같다. 간을 맞추는 데는 반드시 주방 전용 시식 국물(훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 SVM과 KNN에서 스케일링 중요성

**[KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/) ([K-Nearest Neighbors](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/), K-최근접 이웃) 예시:**
```
피처 A: 나이 (20~60) 피처 B: 연봉 (2000만~1억)

샘플 X: (30세, 5000만원)
샘플 Y: (35세, 5100만원)
샘플 Z: (31세, 8000만원)

스케일링 없는 유클리드 거리:
d(X,Y) = √((5)² + (100만)²) ≈ 100만 ← 나이 차이는 무의미
d(X,Z) = √((1)² + (3000만)²) ≈ 3000만

스케일링 후: 나이와 연봉이 동등하게 기여 → 정확한 이웃 탐색
```

### 4.2 스케일링 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구성

```
[원시 데이터]
↓
[결측치 처리]
↓
[이상치 탐지 및 처리]
↓
[스케일링 기법 선택] ← 이상치 여부, 알고리즘 유형 판단
↓
[train.fit → train/test.transform]
↓
[모델 학습/예측]
```

### 4.3 기술사 핵심 판단 포인트
- **트리 기반 모델(RandomForest, XGBoost)에 스케일링 불필요** — 분기 기준이 특성 스케일에 독립적
- **스케일링과 인코딩 순서**: [원-핫 인코딩](/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/) 후 스케일링 (이진 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)는 스케일링 제외 가능)
- **역변환(Inverse Transform) 필요성**: 회귀 모델의 예측값이 스케일링된 타깃일 경우 원래 단위로 복원

- **📢 섹션 요약 비유**: KNN에서 스케일링 없이 "나이와 연봉"으로 이웃을 찾는 것은 km와 mm를 더해서 거리를 재는 것이다. 단위가 통일되지 않으면 절대 공정한 비교가 되지 않는다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 스케일링 적용 효과
- 경사하강법 수렴 속도 수십 배 향상
- [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/)/[SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 거리 계산 정확도 개선
- 신경망 그래디언트 소실/폭발 방지
- [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 간 공정한 기여도 보장

### 5.2 결론
스케일링은 거리 기반, 경사하강법 기반 모델에서 필수적인 전처리 단계다. [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 유무에 따라 [Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), Z-Score 표준화, 로버스트 스케일링 중 선택하고, 반드시 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서만 스케일러를 학습시켜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수를 방지해야 한다. 기술사 시험에서는 각 기법의 수식, 적용 시기, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 방지 원칙을 명확히 서술할 수 있어야 한다.

- **📢 섹션 요약 비유**: 스케일링은 오케스트라 악기들의 음량을 조정하는 것이다. 트럼펫이 너무 크면 바이올린 소리가 묻히듯, [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스케일이 맞지 않으면 중요한 정보가 숫자 크기에 묻혀버린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/)) | 0~1 범위, [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 민감 / 스케일링 기법 |
| 표준화(Z-Score) | 평균=0, 표준편차=1 / 스케일링 기법 |
| 로버스트 스케일링 | 중앙값, IQR, [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 강건 / 스케일링 기법 |
| 경사하강법 | 손실 지형, 수렴 속도 / 스케일링 필요성 근거 |
| [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/)/[KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/) | 거리 기반 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) / 스케일링 필수 모델 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 | Train에만 fit / 스케일링 적용 주의사항 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [스케일링 (Scaling Normalization Standardization)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 스케일링은 모든 물건의 무게를 같은 저울로 재는 것과 같아요.
2. 나이(0~100)와 연봉(0~1억)을 그대로 쓰면 컴퓨터가 연봉만 중요하게 생각해요.
3. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(0~1로 맞추기)나 표준화(평균에서 얼마나 멀리 있나)로 모두 공평하게 비교할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 249 / 420

← **이전**: [248. 원-핫 인코딩 (One-Hot Encoding)](/knowledge-base/studynote/10_ai/03_llm_nlp/248_one_hot_encoding/)
**다음**: [250. 교차 검증 (Cross-Validation)](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/) →

---
