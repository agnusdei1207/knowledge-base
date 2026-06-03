---
title: 115. DBSCAN 클러스터링 - 밀도 기반 군집화·노이즈 분리·비구형 클러스터
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[351_dbscan_density_based_clustering|DBSCAN]]([[357_dbscan|Density-Based Spatial Clustering]] of Applications with Noise)은 **[[001_dikw_pyramid|데이터]] 밀도가 높은 영역을 클러스터로 묶고**, 밀도가 낮은 영역의 [[001_dikw_pyramid|데이터]]를 **노이즈([[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]])**로 자동 분리하는 밀도 기반 클러스터링 알고리즘이다.
> 2. **가치**: K-Means가 K(클러스터 수)를 사전 지정해야 하고 원형 클러스터만 탐지하는 반면, DBSCAN은 **K를 자동 결정**하고 **비구형(초승달·고리 형태) 클러스터**도 탐지하며 **노이즈를 자동 분리**한다.
> 3. **판단 포인트**: 두 파라미터 **ε(epsilon, 반경)**과 **MinPts(최소 이웃 수)**가 결과를 결정하며, ε이 너무 크면 모든 [[001_dikw_pyramid|데이터]]가 1개 클러스터, 너무 작으면 모두 노이즈가 되는 민감성이 있다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    DBSCAN 핵심 개념                                   │
├───────────────────────────────────────────────────────┤
│  ε-이웃(ε-Neighborhood): 반경 ε 안의 데이터          │
│                                                       │
│  Core Point: ε 안에 MinPts개 이상 이웃이 있는 점      │
│  Border Point: Core의 ε 안에 있지만 자신은 Core 아닌  │
│  Noise: Core도 Border도 아닌 점 → 이상치!            │
│                                                       │
│  [Core]─────[Core]─────[Core]   ← 클러스터 1         │
│    │                     │                             │
│  [Border]             [Border]                        │
│                                                       │
│                  · (Noise)                             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: DBSCAN은 사람이 모인 곳(밀도 높은 영역)을 "파티(클러스터)"로 인식하고, 혼자 떨어진 사람은 "방관자(노이즈)"로 분류하는 알고리즘이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[351_dbscan_density_based_clustering|DBSCAN]] vs K-Means

| 비교 | K-Means | [[351_dbscan_density_based_clustering|DBSCAN]] |
|:---|:---|:---|
| **K 지정** | 필수 | **자동 결정** |
| **클러스터 형태** | 원형 | **비구형 (자유 형태)** |
| **노이즈 처리** | 없음 (강제 할당) | **자동 분리** |
| **파라미터** | K | **ε, MinPts** |
| **밀도 변화** | 대응 불가 | 대응 불가 (HDBSCAN으로 해결) |

- **📢 섹션 요약 비유**: K-Means는 사전에 "3개 그룹으로 나눠!"라고 명령하는 것이고, DBSCAN은 "알아서 모인 사람끼리 그룹 짓고, 혼자 있는 사람은 제외해"라고 하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | K-Means | [[351_dbscan_density_based_clustering|DBSCAN]] | HDBSCAN |
|:---|:---|:---|:---|
| **K 지정** | 필수 | 불필요 | 불필요 |
| **밀도 변화** | 대응 불가 | **대응 불가** | **대응 가능** |
| **노이즈** | 없음 | ✅ | ✅ |
| **속도** | O(nK) | O(n log n) | O(n log n) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### ε·MinPts [[009_config|설정]] 가이드
- **ε**: k-distance 그래프의 "팔꿈치(elbow)" 지점.
- **MinPts**: 일반적으로 `2 × 차원 수`. 2D → MinPts=4.

### 활용 시나리오
1. **지리적 클러스터링**: GPS 좌표로 상점 밀집 지역 탐지.
2. **[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]**: 네트워크 트래픽에서 정상 패턴 밖 접근 = 노이즈(공격).

---

## Ⅴ. 기대효과 및 결론

DBSCAN은 K-Means가 실패하는 **비구형·노이즈 혼재 [[001_dikw_pyramid|데이터]]**에서 강력하며, HDBSCAN으로 확장하면 밀도 변화까지 대응 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Core Point** | ε 내 MinPts 이상 이웃을 가진 핵심 점 |
| **Noise** | 어떤 클러스터에도 속하지 않는 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] |
| **ε (epsilon)** | 이웃 탐색 반경, 민감 파라미터 |
| **HDBSCAN** | DBSCAN의 밀도 변화 대응 확장 |
| **K-Means** | 원형·K 지정 클러스터링 (비교 대상) |

### 📈 관련 키워드 및 발전 흐름도

```text
[K-Means (1957) — 원형 클러스터, K 지정]
    │
    ▼
[DBSCAN (1996, Ester & Kriegel) — 밀도 기반, 노이즈 분리]
    │
    ▼
[OPTICS (1999) — 가변 밀도 대응]
    │
    ▼
[HDBSCAN (2013) — 계층적 밀도 기반, ε 자동]
    │
    ▼
[현재: 딥 클러스터링 — Autoencoder + DBSCAN 결합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K-Means는 "3개 그룹으로 나눠!"라고 **미리 정해**야 해요.
2. DBSCAN은 사람이 **많이 모인 곳**을 자동으로 그룹으로 묶고, **혼자 있는 사람은 따로 빼요** (노이즈).
3. 그래서 초승달 모양 같은 **이상한 모양의 그룹도 잘 찾아낼 수** 있답니다!
