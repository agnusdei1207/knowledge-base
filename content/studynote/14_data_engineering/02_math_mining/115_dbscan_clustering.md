+++
title = "115. DBSCAN 클러스터링 - 밀도 기반 군집화·노이즈 분리·비구형 클러스터"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/)([Density-Based Spatial Clustering](/knowledge-base/studynote/10_ai/05_data_science_ml/357_dbscan/) of Applications with Noise)은 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 밀도가 높은 영역을 클러스터로 묶고</strong>, 밀도가 낮은 영역의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>노이즈(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a>)</strong>로 자동 분리하는 밀도 기반 클러스터링 알고리즘이다.
> 2. **가치**: K-Means가 K(클러스터 수)를 사전 지정해야 하고 원형 클러스터만 탐지하는 반면, DBSCAN은 <strong>K를 자동 결정</strong>하고 <strong>비구형(초승달·고리 형태) 클러스터</strong>도 탐지하며 <strong>노이즈를 자동 분리</strong>한다.
> 3. **판단 포인트**: 두 파라미터 <strong>ε(epsilon, 반경)</strong>과 <strong>MinPts(최소 이웃 수)</strong>가 결과를 결정하며, ε이 너무 크면 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 1개 클러스터, 너무 작으면 모두 노이즈가 되는 민감성이 있다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DBSCAN 핵심 개념</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ε-이웃(ε-Neighborhood): 반경 ε 안의 데이터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Core Point: ε 안에 MinPts개 이상 이웃이 있는 점</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Border Point: Core의 ε 안에 있지만 자신은 Core 아닌</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Noise: Core도 Border도 아닌 점 → 이상치!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Core</div><div class="kb-diagram-node">Core</div><div class="kb-diagram-node">Core</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">클러스터 1</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Border</div><div class="kb-diagram-node">Border</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">· (Noise)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: DBSCAN은 사람이 모인 곳(밀도 높은 영역)을 "파티(클러스터)"로 인식하고, 혼자 떨어진 사람은 "방관자(노이즈)"로 분류하는 알고리즘이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) vs K-Means

| 비교 | K-Means | [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) |
|:---|:---|:---|
| **K 지정** | 필수 | **자동 결정** |
| **클러스터 형태** | 원형 | **비구형 (자유 형태)** |
| **노이즈 처리** | 없음 (강제 할당) | **자동 분리** |
| **파라미터** | K | **ε, MinPts** |
| **밀도 변화** | 대응 불가 | 대응 불가 (HDBSCAN으로 해결) |

- **📢 섹션 요약 비유**: K-Means는 사전에 "3개 그룹으로 나눠!"라고 명령하는 것이고, DBSCAN은 "알아서 모인 사람끼리 그룹 짓고, 혼자 있는 사람은 제외해"라고 하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | K-Means | [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) | HDBSCAN |
|:---|:---|:---|:---|
| **K 지정** | 필수 | 불필요 | 불필요 |
| **밀도 변화** | 대응 불가 | **대응 불가** | **대응 가능** |
| **노이즈** | 없음 | ✅ | ✅ |
| **속도** | O(nK) | O(n log n) | O(n log n) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### ε·MinPts [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 가이드
- **ε**: k-distance 그래프의 "팔꿈치(elbow)" 지점.
- **MinPts**: 일반적으로 `2 × 차원 수`. 2D → MinPts=4.

### 활용 시나리오
1. **지리적 클러스터링**: GPS 좌표로 상점 밀집 지역 탐지.
2. <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a></strong>: 네트워크 트래픽에서 정상 패턴 밖 접근 = 노이즈(공격).

---

## Ⅴ. 기대효과 및 결론

DBSCAN은 K-Means가 실패하는 <strong>비구형·노이즈 혼재 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>에서 강력하며, HDBSCAN으로 확장하면 밀도 변화까지 대응 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Core Point** | ε 내 MinPts 이상 이웃을 가진 핵심 점 |
| **Noise** | 어떤 클러스터에도 속하지 않는 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) |
| **ε (epsilon)** | 이웃 탐색 반경, 민감 파라미터 |
| **HDBSCAN** | DBSCAN의 밀도 변화 대응 확장 |
| **K-Means** | 원형·K 지정 클러스터링 (비교 대상) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">K-Means (1957) — 원형 클러스터, K 지정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DBSCAN (1996, Ester &amp; Kriegel) — 밀도 기반, 노이즈 분리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OPTICS (1999) — 가변 밀도 대응</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">HDBSCAN (2013) — 계층적 밀도 기반, ε 자동</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: 딥 클러스터링 — Autoencoder + DBSCAN 결합</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. K-Means는 "3개 그룹으로 나눠!"라고 <strong>미리 정해</strong>야 해요.
2. DBSCAN은 사람이 <strong>많이 모인 곳</strong>을 자동으로 그룹으로 묶고, **혼자 있는 사람은 따로 빼요** (노이즈).
3. 그래서 초승달 모양 같은 **이상한 모양의 그룹도 잘 찾아낼 수** 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 258

← **이전**: [114. 가우시안 혼합 모델 (GMM, Gaussian Mixture Model) - EM 알고리즘·소프트 클러스터링](/knowledge-base/studynote/14_data_engineering/02_math_mining/114_gaussian_mixture_model/)
**다음**: [116. 커널 밀도 추정 (KDE, Kernel Density Estimation) - 비모수 확률 밀도 추정](/knowledge-base/studynote/14_data_engineering/02_math_mining/116_kernel_density_estimation/) →

---
