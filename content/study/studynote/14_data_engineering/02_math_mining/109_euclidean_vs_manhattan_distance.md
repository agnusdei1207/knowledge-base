---
title: 109. 유클리드 거리 vs 맨해튼 거리 (Euclidean vs Manhattan Distance)
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 유클리드 거리(L2 Norm)는 두 점 사이의 **최단 직선 거리** $\sqrt{\sum(x_i-y_i)^2}$이고, 맨해튼 거리(L1 Norm)는 축을 따라 이동하는 **격자형 거리** $\sum|x_i-y_i|$로, 동일한 민코프스키 거리(Minkowski Distance)의 $p=2$, $p=1$ 특수 케이스다.
> 2. **가치**: 거리 함수 선택에 따라 [[352_knn_distance_metrics|K-NN]], K-Means, [[102_lasso_ridge_regression_regularization|Lasso]]/Ridge 등 ML 알고리즘의 **결과와 수렴 속도가 크게 달라지며**, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]]) 민감도에서 결정적 차이가 발생한다.
> 3. **판단 포인트**: 연속적·물리적 거리가 중요하면 유클리드, 이산적·독립 차원 [[001_dikw_pyramid|데이터]]이거나 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]에 강건해야 하면 맨해튼을 사용하며, 어떤 경우든 **[[249_scaling_normalization_standardization|스케일링]](표준화/[[093_normalization|정규화]])이 필수 전제**다.

---

## Ⅰ. 개요 및 필요성

ML에서 [[001_dikw_pyramid|데이터]] 간 '유사도'를 수치화하려면 거리 함수(Distance [[342_routing_metric_hop_bandwidth_delay|Metric]])가 필요하다. 같은 [[001_dikw_pyramid|데이터]]셋에 유클리드를 쓰느냐 맨해튼을 쓰느냐에 따라 K-NN의 이웃이 달라지고, K-Means의 클러스터 형태가 바뀐다.

```text
┌───────────────────────────────────────────────┐
│    유클리드 vs 맨해튼 거리 시각화              │
├───────────────────────────────────────────────┤
│          (B)                                  │
│           *                                   │
│          /|                                   │
│   Euclid/ | Manhattan                         │
│   (직선)/ | (격자: 가로+세로)                  │
│        /  |                                   │
│   (A) *───┘                                   │
│                                               │
│  Euclid  = √((x2-x1)² + (y2-y1)²)           │
│  Manhattan = |x2-x1| + |y2-y1|               │
└───────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 유클리드는 새가 하늘을 직선으로 날아가는 거리, 맨해튼은 택시가 도시 격자 도로를 따라 꺾어가는 거리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 민코프스키 거리 일반화

$D_p(x,y) = \left(\sum_{i=1}^{n} |x_i - y_i|^p\right)^{1/p}$

| $p$ 값 | 이름 | 등고선 형태 | [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 영향 |
|:---|:---|:---|:---|
| $p=1$ | 맨해튼 (L1) | 다이아몬드(◇) | **절대값 → 상대적으로 작음** |
| $p=2$ | 유클리드 (L2) | 원(○) | **제곱 → 크게 증폭** |
| $p→∞$ | 체비셰프 (L∞) | 정사각형(□) | 최대 차이만 반영 |

### [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 민감도 메커니즘

유클리드는 차이를 **제곱**하므로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 1개가 거리를 폭발적으로 왜곡한다. 맨해튼은 **절대값**만 취하므로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]의 영향이 선형적이다. 따라서 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]가 많은 [[001_dikw_pyramid|데이터]]에서는 맨해튼이 더 강건(Robust)하다.

- **📢 섹션 요약 비유**: 유클리드는 시험에서 한 과목 0점을 받으면 평균이 폭락하는 제곱 방식이고, 맨해튼은 0점이어도 다른 과목으로 만회가 쉬운 절대값 방식이다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 유클리드 (L2) | 맨해튼 (L1) |
|:---|:---|:---|
| **기하학** | 최단 직선 | 격자형 이동 |
| **[[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]** | 제곱 → 매우 민감 | 절대값 → 상대적 강건 |
| **차원의 저주** | 더 취약 | 고차원에서 구별력 유지 |
| **[[093_normalization|정규화]] 연결** | Ridge (L2 [[134_regularization_dropout_batch_norm|Regularization]]) | [[102_lasso_ridge_regression_regularization|Lasso]] (L1 [[134_regularization_dropout_batch_norm|Regularization]]) |
| **K-Means** | 표준 K-Means | K-Medians |
| **주요 활용** | 회귀, K-Means, 신경망 | [[102_lasso_ridge_regression_regularization|Lasso]], 고차원·희소 [[001_dikw_pyramid|데이터]] |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선택 기준
1. **[[001_dikw_pyramid|데이터]] 특성**: 연속·물리적 거리 → 유클리드 / 이산·독립 차원 → 맨해튼
2. **[[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]**: [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 다수 → 맨해튼 (L1이 Robust)
3. **고차원**: 차원 > 100 → 맨해튼 또는 [[359_cosine_similarity|코사인 유사도]] 검토
4. **전제**: 두 거리 모두 **단위에 민감** → 표준화(StandardScaler) 또는 [[093_normalization|정규화]](MinMaxScaler) 필수

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[249_scaling_normalization_standardization|스케일링]] 없이 거리 계산**: 키(cm)와 체중(kg) 같은 이질 단위를 [[249_scaling_normalization_standardization|스케일링]] 없이 유클리드 거리로 계산 → 큰 단위 변수가 거리를 지배.

---

## Ⅴ. 기대효과 및 결론

거리 함수는 [[211_recommendation_system|추천 시스템]], 이미지 검색, 군집 분석 등 거의 모든 ML의 토대다. 최근에는 고차원 특성을 반영하기 위해 **[[359_cosine_similarity|코사인 유사도]]([[359_cosine_similarity|Cosine Similarity]])**나 **[[106_mahalanobis_distance|마할라노비스 거리]]([[106_mahalanobis_distance|Mahalanobis Distance]])**와 혼합하는 하이브리드 전략이 표준으로 자리잡고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **민코프스키 거리** | L1·L2를 일반화하는 상위 개념 ($p$ 파라미터) |
| **[[352_knn_distance_metrics|K-NN]]** | 거리 함수 선택이 이웃 결정에 직접 영향 |
| **K-Means / K-Medians** | L2 → K-Means, L1 → K-Medians |
| **[[102_lasso_ridge_regression_regularization|Lasso]] (L1) / Ridge (L2)** | 각각 맨해튼·유클리드 노름 기반 [[093_normalization|정규화]] |
| **차원의 저주** | 고차원에서 거리 간 격차가 축소되는 현상 |
| **[[359_cosine_similarity|코사인 유사도]]** | 방향 기반 유사도, 벡터 크기 무시 |

### 📈 관련 키워드 및 발전 흐름도

```text
[유클리드 거리 (피타고라스, BC) — 2차원 직선 거리]
    │
    ▼
[민코프스키 거리 (19C) — p-노름 일반화]
    │
    ▼
[맨해튼 거리 (Taxi Cab) — L1 노름, 이산 공간]
    │
    ▼
[코사인 유사도·마할라노비스 — 방향·공분산 고려]
    │
    ▼
[현재: Learned Distance (Metric Learning) — 신경망이 최적 거리 함수를 학습]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 유클리드 거리는 새가 하늘을 **직선으로 슝~** 날아가는 거리예요.
2. 맨해튼 거리는 자동차가 도시 골목길을 **ㄱ자, ㄴ자로 꺾어서** 가는 거리예요.
3. 학교까지 얼마나 먼지 재는 방법이 여러 가지가 있다는 뜻이랍니다!
