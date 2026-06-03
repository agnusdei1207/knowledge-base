---
title: 249. 스케일링 (Scaling Normalization Standardization)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스케일링(Scaling)은 서로 다른 범위를 가진 수치형 [[247_feature_label_variables|피처]]들을 동일한 척도로 맞추어, 모델이 특정 [[247_feature_label_variables|피처]]에 편향되지 않고 균등하게 학습하게 하는 전처리 기법이다.
> 2. **가치**: 경사하강법([[165_gradient_descent|Gradient Descent]]) 기반 모델(선형 회귀, 신경망)과 거리 기반 모델([[238_svm_margin_kernel_trick_naive_bayes|SVM]], [[262_knn|KNN]])에서 스케일링은 수렴 속도와 예측 정확도에 직접적인 영향을 미친다.
> 3. **판단 포인트**: [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]])가 없으면 [[093_normalization|정규화]]([[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]] [[093_normalization|Normalization]]), [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]가 있으면 표준화(Standardization) 또는 로버스트 스케일링(Robust Scaling)을 선택한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 스케일링이 필요한 이유
[[247_feature_label_variables|피처]]들의 단위와 범위가 다를 경우 발생하는 문제:

| [[247_feature_label_variables|피처]] | 범위 | 스케일링 전 영향 |
|:---|:---|:---|
| 나이 | 0 ~ 100 | 작은 값, 모델 [[267_weight_bias_activation|가중치]] 영향 小 |
| 연봉 | 2000만 ~ 1억 | 큰 값, 모델 [[267_weight_bias_activation|가중치]] 지배 |
| BMI | [[489_raid_10_hybrid|10]] ~ 40 | 중간 값 |

→ 스케일링 없이 경사하강법 적용 시 연봉 방향으로 기울어진 손실 지형(Loss Landscape) [[087_process_state_transition|생성]] → 수렴 속도 저하 또는 발산

### 1.2 스케일링이 필수인 [[001_algorithm_definition|알고리즘]]

| [[001_algorithm_definition|알고리즘]] | 스케일링 필요 여부 | 이유 |
|:---|:---|:---|
| 선형 회귀(Linear Regression) | ✅ 필요 | 경사하강법 수렴 |
| [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]]) | ✅ 필요 | 동일 이유 |
| [[238_svm_margin_kernel_trick_naive_bayes|SVM]] ([[238_svm_margin_kernel_trick_naive_bayes|Support Vector Machine]]) | ✅ 필요 | 거리 기반 마진 |
| [[262_knn|KNN]] ([[262_knn|K-Nearest Neighbors]]) | ✅ 필요 | 유클리드 거리 왜곡 |
| 신경망(Neural Network) | ✅ 필요 | 그래디언트 소실/폭발 |
| 결정 트리([[124_decision_tree|Decision Tree]]) | ❌ 불필요 | 분기 기준이 절댓값 불변 |
| [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]]) | ❌ 불필요 | 트리 기반 |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 스케일링은 달리기 경주에서 모든 선수의 출발선을 같은 위치로 맞추는 것이다. 한 선수가 1미터를 달리고 다른 선수가 1킬로미터를 달리는 경주는 공정한 비교가 되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 스케일링 기법 비교 도식

```
┌─────────────────────────────────────────────────────────┐
│              스케일링 기법 비교                            │
│                                                         │
│  원본 데이터 분포:                                         │
│  ──────[min]─────────────────────[max]──────             │
│   이상치◀                                    ▶이상치      │
│                                                         │
│  1. 정규화 (Min-Max): [0, 1] 범위로 압축                  │
│  ──[0]────────────────────────────────[1]──             │
│    (이상치에 의해 전체 분포가 압축될 수 있음)                │
│                                                         │
│  2. 표준화 (Z-Score): 평균=0, 표준편차=1                  │
│  ────────[-3]──[-2]──[-1]──[0]──[1]──[2]──[3]──         │
│    (이상치도 수치 변환되나 분포 형태는 유지)                 │
│                                                         │
│  3. 로버스트 스케일링: 중앙값, IQR 기준                     │
│  ──────[Q1]───────[중앙값]───────[Q3]──────             │
│    (이상치에 강건, 중앙 분포 집중)                          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 각 기법의 수식과 특징

#### [[093_normalization|정규화]] ([[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]] [[093_normalization|Normalization]])
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

### 2.3 경사하강법과 스케일링 [[083_relationship_in_er_model|관계]]

| 조건 | 손실 지형 모양 | 수렴 특성 |
|:---|:---|:---|
| 스케일링 없음 | 길쭉한 타원형(편향된 등고선) | 지그재그로 느린 수렴 |
| 스케일링 적용 | 원형에 가까운 등고선 | 최적점으로 빠른 직선 수렴 |

- **📢 섹션 요약 비유**: [[093_normalization|정규화]]는 모든 것을 0~100점 척도로 바꾸는 것이고, 표준화는 "평균에서 몇 표준편차 떨어져 있냐"로 표현하는 편차 성적표 같은 것이다. [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]가 있는 반에서는 편차 성적표(표준화)가 더 공정하다.

---

## Ⅲ. 비교 및 연결

### 3.1 스케일링 기법 선택 가이드

| 상황 | 권장 기법 | 이유 |
|:---|:---|:---|
| [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 없음, 분포 균등 | [[093_normalization|정규화]]([[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]]) | 범위 명확, 해석 쉬움 |
| [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 있음, [[138_normal_distribution|정규 분포]] | 표준화(Z-Score) | [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 영향 완화 |
| [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 다수, 치우침 심함 | 로버스트 스케일링 | 중앙값 기반으로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 무력화 |
| 이미지 픽셀값 (0~255) | [[093_normalization|정규화]](÷255) | 0~1 [[093_normalization|정규화]]로 단순 처리 |
| 신경망 입력 | 표준화 또는 [[282_batch_normalization|배치 정규화]] | [[129_activation_function|활성화 함수]] 포화 방지 |

### 3.2 Train-Test [[001_dikw_pyramid|데이터]]에서의 스케일링 주의사항

**[[001_dikw_pyramid|데이터]] 누수([[001_dikw_pyramid|Data]] Leakage) 방지 규칙:**
```
❌ 잘못된 방법: 전체 데이터(train+test)에 fit_transform
✅ 올바른 방법: train 데이터에만 fit → train/test 모두 transform

이유: 테스트 데이터는 미래 데이터를 대표해야 하므로
      테스트 데이터의 통계(min, max, μ, σ)가 스케일링에 반영되면
      현실적이지 않은 스케일러가 만들어짐
```

### 3.3 [[282_batch_normalization|배치 정규화]] ([[282_batch_normalization|Batch Normalization]], BN)
딥러닝에서 레이어 내부의 활성화값을 [[093_normalization|정규화]]하는 기법:
- 각 미니배치(Mini-batch) 내에서 평균=0, 표준편차=1로 [[093_normalization|정규화]]
- 학습 속도 향상, 그래디언트 소실([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 완화
- [[093_normalization|정규화]] 파라미터(γ, β)를 학습으로 최적화

- **📢 섹션 요약 비유**: Train/Test 스케일링 규칙은 요리사가 국물 간을 맞출 때 손님이 먹을 국물을 시식용으로 쓰면 안 되는 것과 같다. 간을 맞추는 데는 반드시 주방 전용 시식 국물(훈련 [[001_dikw_pyramid|데이터]])만 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 SVM과 KNN에서 스케일링 중요성

**[[262_knn|KNN]] ([[262_knn|K-Nearest Neighbors]], K-최근접 이웃) 예시:**
```
피처 A: 나이 (20~60)   피처 B: 연봉 (2000만~1억)

샘플 X: (30세, 5000만원)
샘플 Y: (35세, 5100만원)
샘플 Z: (31세, 8000만원)

스케일링 없는 유클리드 거리:
d(X,Y) = √((5)² + (100만)²) ≈ 100만   ← 나이 차이는 무의미
d(X,Z) = √((1)² + (3000만)²) ≈ 3000만

스케일링 후: 나이와 연봉이 동등하게 기여 → 정확한 이웃 탐색
```

### 4.2 스케일링 [[123_pipe|파이프]]라인 구성

```
[원시 데이터]
     ↓
[결측치 처리]
     ↓
[이상치 탐지 및 처리]
     ↓
[스케일링 기법 선택]  ← 이상치 여부, 알고리즘 유형 판단
     ↓
[train.fit → train/test.transform]
     ↓
[모델 학습/예측]
```

### 4.3 기술사 핵심 판단 포인트
- **트리 기반 모델(RandomForest, XGBoost)에 스케일링 불필요** — 분기 기준이 특성 스케일에 독립적
- **스케일링과 인코딩 순서**: [[079_one_hot_encoding_categorical_dummy_variable|원-핫 인코딩]] 후 스케일링 (이진 [[247_feature_label_variables|피처]]는 스케일링 제외 가능)
- **역변환(Inverse Transform) 필요성**: 회귀 모델의 예측값이 스케일링된 타깃일 경우 원래 단위로 복원

- **📢 섹션 요약 비유**: KNN에서 스케일링 없이 "나이와 연봉"으로 이웃을 찾는 것은 km와 mm를 더해서 거리를 재는 것이다. 단위가 통일되지 않으면 절대 공정한 비교가 되지 않는다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 스케일링 적용 효과
- 경사하강법 수렴 속도 수십 배 향상
- [[262_knn|KNN]]/[[238_svm_margin_kernel_trick_naive_bayes|SVM]] 거리 계산 정확도 개선
- 신경망 그래디언트 소실/폭발 방지
- [[247_feature_label_variables|피처]] 간 공정한 기여도 보장

### 5.2 결론
스케일링은 거리 기반, 경사하강법 기반 모델에서 필수적인 전처리 단계다. [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 유무에 따라 [[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]] [[093_normalization|정규화]], Z-Score 표준화, 로버스트 스케일링 중 선택하고, 반드시 훈련 [[001_dikw_pyramid|데이터]]에서만 스케일러를 학습시켜 [[001_dikw_pyramid|데이터]] 누수를 방지해야 한다. 기술사 시험에서는 각 기법의 수식, 적용 시기, [[001_dikw_pyramid|데이터]] 누수 방지 원칙을 명확히 서술할 수 있어야 한다.

- **📢 섹션 요약 비유**: 스케일링은 오케스트라 악기들의 음량을 조정하는 것이다. 트럼펫이 너무 크면 바이올린 소리가 묻히듯, [[247_feature_label_variables|피처]] 스케일이 맞지 않으면 중요한 정보가 숫자 크기에 묻혀버린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[093_normalization|정규화]]([[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]]) | 0~1 범위, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 민감 / 스케일링 기법 |
| 표준화(Z-Score) | 평균=0, 표준편차=1 / 스케일링 기법 |
| 로버스트 스케일링 | 중앙값, IQR, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 강건 / 스케일링 기법 |
| 경사하강법 | 손실 지형, 수렴 속도 / 스케일링 필요성 근거 |
| [[238_svm_margin_kernel_trick_naive_bayes|SVM]]/[[262_knn|KNN]] | 거리 기반 [[001_algorithm_definition|알고리즘]] / 스케일링 필수 모델 |
| [[001_dikw_pyramid|데이터]] 누수 | Train에만 fit / 스케일링 적용 주의사항 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [스케일링 (Scaling Normalization Standardization)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 스케일링은 모든 물건의 무게를 같은 저울로 재는 것과 같아요.
2. 나이(0~100)와 연봉(0~1억)을 그대로 쓰면 컴퓨터가 연봉만 중요하게 생각해요.
3. [[093_normalization|정규화]](0~1로 맞추기)나 표준화(평균에서 얼마나 멀리 있나)로 모두 공평하게 비교할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 249 / 420

← **이전**: [[248_one_hot_encoding|248. 원-핫 인코딩 (One-Hot Encoding)]]
**다음**: [[250_cross_validation_kfold|250. 교차 검증 (Cross-Validation)]] →

---
