---
title: "Kmeans EM"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 263
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: K-Means 클러스터링([K-Means Clustering](/studynote/10_ai/01_ai_basics/057_k_means_clustering_unsupervised_learning/))은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 K개의 군집으로 분할하기 위해 각 점을 가장 가까운 중심점(Centroid)에 할당하고, 중심점을 반복 재계산하는 EM([Expectation-Maximization](/studynote/08_algorithm_stats/08_stats/142_em_algorithm/)) 구조의 [비지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 단순하고 빠르지만 K값을 사전에 지정해야 하고, 구형(Spherical) 클러스터 외에는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되는 한계를 [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)([Gaussian Mixture Model](/studynote/14_data_engineering/02_math_mining/114_gaussian_mixture_model/))이나 DBSCAN으로 극복할 수 있다.
> 3. **판단 포인트**: 엘보우 방법(Elbow Method)과 실루엣 점수([Silhouette Score](/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/))로 최적 K를 선택하고, [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화에 K-Means++ [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 사용하면 지역 최적해(Local Optimum)에 빠지는 위험을 줄일 수 있다.

---

## Ⅰ. 개요 및 필요성

K-Means는 레이블 없이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 자동으로 [그룹화](/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)하는 가장 대표적인 <strong><a href="/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">비지도 학습</a>(<a href="/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/">Unsupervised Learning</a>)</strong> [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

**활용 사례**:
- **고객 세분화**: 구매 패턴으로 고객을 [그룹화](/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) -> 맞춤 마케팅
- <strong>이미지 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong>: 색상 팔레트 K개로 이미지 색상 축약
- **문서 클러스터링**: 유사한 주제의 기사를 [그룹화](/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)
- **이상값 탐지**: 어느 클러스터에도 속하지 않는 포인트 감지

**K-Means의 목표 함수 (이너시아, Inertia)**:

$$\text{Inertia} = \sum_{k=1}^{K} \sum_{x \in C_k} \|x - \mu_k\|^2$$

- $\mu_k$: k번째 클러스터의 중심점
- 이너시아를 최소화하는 할당과 중심점을 찾는 것이 목표

| 특성 | K-Means | [DBSCAN](/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) | [계층적 군집화](/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/) |
|:---|:---|:---|:---|
| K 사전 지정 | 필요 | 불필요 | 불필요 |
| 클러스터 형태 | 구형만 | 임의 형태 | 임의 형태 |
| 이상값 처리 | 약함 | 강함 (노이즈 포인트) | 중간 |
| [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | O(nKt) | O(n log n) | O(n^~n³) |
| 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 가능 | 중간 | 어려움 |

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: K-Means는 "K개의 모임 장소를 정하고, 각자 가장 가까운 장소에 모인 뒤, 모인 사람들의 무게중심으로 장소를 이동"하는 것을 반복하는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### K-Means [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) EM 구조

```
  K-Means EM (Expectation-Maximization) 구조
  +---------------------------------------------+
  |  1. 초기화: K개 중심점 μ_1,...,μ_K 무작위 선택|
  +----------------------+----------------------+
                         |
  +----------------------v----------------------+
  |  E-Step (할당):                             |
  |  각 포인트 x_i를 가장 가까운 중심점에 할당  |
  |  c_i = argmin_k ‖x_i - μ_k‖^               |
  +----------------------+----------------------+
                         |
  +----------------------v----------------------+
  |  M-Step (업데이트):                         |
  |  각 클러스터의 중심점을 멤버 평균으로 재계산 |
  |  μ_k = (1/|C_k|) · Σ_{x∈C_k} x             |
  +----------------------+----------------------+
                         |
  +----------------------v----------------------+
  |  수렴 판단: 중심점 변화 < ε 또는 최대 반복? |
  |  Yes -> 종료 / No -> E-Step으로 반복          |
  +---------------------------------------------+
```

### 엘보우 방법 (Elbow Method)으로 K 선택

```
  이너시아 (Inertia)
      |
  ----+  ●
      |   ╲
      |    ●
      |     ╲
      |      ●  <- "엘보우" 지점 (K=4 최적)
      |       ╲------●--------●
      |
      +--------------------------- K
          1   2   3   4   5   6

  엘보우 이후 이너시아 감소폭이 급격히 줄어드는 K가 최적
```

### 실루엣 점수 ([Silhouette Score](/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/))

각 샘플에 대한 군집 품질 지표:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

- $a(i)$: 같은 클러스터 내 다른 샘플과의 평균 거리 ([응집도](/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/))
- $b(i)$: 가장 가까운 **다른** 클러스터 샘플과의 평균 거리 (분리도)
- 범위: -1 (최악) ~ +1 (최상), 0.5 이상이 좋은 클러스터

| 실루엣 점수 | 해석 |
|:---:|:---|
| 0.7 ~ 1.0 | 우수한 군집 구조 |
| 0.5 ~ 0.7 | 합리적인 군집 구조 |
| 0.25 ~ 0.5 | 약한 군집 구조 |
| < 0.25 | 인위적이거나 무의미한 군집 |

### EM [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 GMM의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

K-Means는 EM [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 하드(Hard) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이고, [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)([Gaussian Mixture Model](/studynote/14_data_engineering/02_math_mining/114_gaussian_mixture_model/))은 소프트(Soft) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다.

```
  K-Means (Hard EM):           GMM (Soft EM):
  +----------------------+     +----------------------+
  | 각 점은 하나의       |     | 각 점은 여러 가우시안 |
  | 클러스터에만 속함     |     | 분포에 확률적으로 속함|
  | (0 또는 1 소속)      |     | (0~1 사이 확률 소속)  |
  |                      |     |                      |
  | 원형 등분산 클러스터  |     | 타원형, 다양한 공분산  |
  +----------------------+     +----------------------+
```

- **📢 섹션 요약 비유**: K-Means EM은 "반 배정 후 각 반의 교실 위치를 학생들의 집 위치 평균으로 이동"하는 과정이다. GMM은 "학생을 여러 반에 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 소속"시켜 더 유연하게 그룹을 형성한다.

---

## Ⅲ. 비교 및 연결

### K-Means의 한계와 대안

```
  K-Means 한계:
  +----------------------------------------------+
  | 1. 구형 클러스터만 잘 찾음                  |
  |    -> 해결: DBSCAN, GMM, Spectral Clustering  |
  |                                              |
  | 2. K 사전 지정 필요                          |
  |    -> 해결: 엘보우/실루엣, DBSCAN             |
  |                                              |
  | 3. 초기 중심점에 민감 (지역 최적해)          |
  |    -> 해결: K-Means++ 초기화                  |
  |                                              |
  | 4. 이상값에 민감 (중심점 왜곡)               |
  |    -> 해결: K-Medoids, 이상값 제거            |
  |                                              |
  | 5. 스케일에 민감                             |
  |    -> 해결: 표준화(StandardScaler) 전처리     |
  +----------------------------------------------+
```

### K-Means++ [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화

표준 K-Means는 무작위 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화로 지역 최적해에 빠질 수 있다. K-Means++는 중심점들이 서로 멀리 떨어지도록 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 선택한다.

- 첫 번째 중심점: 무작위 선택
- 이후 중심점: 기존 중심점과의 거리^에 비례한 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로 선택
- 효과: 수렴 속도 향상, 더 나은 최적해

### [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) vs K-Means

| 특성 | K-Means | [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) |
|:---|:---|:---|
| 클러스터 모양 | 구형 | 타원형 (공분산 행렬) |
| 소속 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) | Hard (0/1) | Soft (0~1 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)) |
| 모수 추정 | 중심점 | 평균, 공분산, 혼합 비율 |
| 이상값 | 약함 | 중간 |
| 해석 | 쉬움 | 복잡 |

- **📢 섹션 요약 비유**: K-Means는 "각자 하나의 부족(클러스터)에만 속하는 부족 사회"고, GMM은 "사람마다 여러 정체성(직장인이면서 부모이면서 운동선수)을 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 가지는 현대 사회"다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 고객 세분화 K-Means [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

```
  데이터 수집 (구매 이력, 방문 빈도, 금액)
       |
  전처리 (StandardScaler 정규화, 이상값 제거)
       |
  최적 K 탐색 (Elbow Method + Silhouette Score)
       |
  K-Means++ 학습 (n_init=10으로 여러 번 초기화)
       |
  클러스터 레이블 할당
       |
  클러스터 프로파일링 (각 그룹 특성 분석)
       |
  마케팅 전략 수립 (그룹별 맞춤 캠페인)
```

### Mini-Batch K-Means

대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 대신 미니 배치(Mini-Batch)로 중심점을 업데이트:
- 표준 K-Means: 메모리에 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요, O(nKt)
- Mini-Batch K-Means: 배치 크기 b만 메모리, O(bKt), 정확도 약간 감소

### 기술사 답안 포인트

- <strong>"K-Means가 EM <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>인 이유"</strong>: E-Step(할당) = [기댓값](/studynote/08_algorithm_stats/08_stats/135_expected_value/) 계산, M-Step(중심 업데이트) = 최대화
- **"K 선정 방법 두 가지"**: 엘보우(이너시아 기울기 변화점), 실루엣(군집 [응집도](/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)/분리도)
- <strong>"K-Means vs <a href="/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/">GMM</a> 선택 기준"</strong>: 클러스터가 원형이고 크기가 비슷하면 K-Means, 다양한 형태면 [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)
- **"K-Means 이상값 처리"**: 이상값 제거 후 적용 또는 K-Medoids(중위수 기반) 사용

- **📢 섹션 요약 비유**: 엘보우 방법은 팔을 구부렸을 때 꺾이는 지점처럼, K가 증가해도 이너시아가 더 이상 크게 줄지 않는 "더 이상 나눠도 의미 없는 지점"을 찾는 것이다.

---

## Ⅴ. 기대효과 및 결론

K-Means를 올바르게 활용하면:

1. **자동 패턴 발견**: 레이블 없는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 숨겨진 구조 발견 -> 비즈니스 인사이트
2. <strong><a href="/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/">차원 축소</a> 보완</strong>: [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 후 K-Means로 클러스터 구조 파악 -> 2단계 분석
3. **준지도 학습 지원**: 클러스터 레이블을 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 레이블로 활용 -> 적은 레이블로 [지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)
4. <strong><a href="/studynote/07_enterprise_systems/05_data_bi/300_realtime_data_streaming_kafka_cdc/">실시간 데이터 스트리밍</a></strong>: Mini-Batch K-Means로 온라인 [군집화](/studynote/16_bigdata/05_analysis/105_clustering_analysis/) 가능

K-Means는 단순하지만, **올바른 전처리 + K 선택 + 결과 해석** [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 구축하면 강력한 [탐색적 데이터 분석](/studynote/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis/)([EDA](/studynote/12_it_management/02_itsm_itil/064_eda/), [Exploratory Data Analysis](/studynote/12_it_management/03_ea_isp/889_exploratory_data_analysis/)) 도구가 된다.

- **📢 섹션 요약 비유**: K-Means는 "지도 없이 낯선 도시에서 주민들이 자연스럽게 모이는 동네를 찾는 것"이다. 처음엔 무작위로 동네 중심을 잡지만, 주민들이 모이고 중심이 이동하기를 반복하면 자연스러운 생활권(클러스터)이 드러난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| K-Means 클러스터링 | 중심점(Centroid), 이너시아 / 대표적 비지도 [군집화](/studynote/16_bigdata/05_analysis/105_clustering_analysis/) |
| 이너시아 (Inertia) | 군집 내 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 목표 함수 / K-Means 최소화 대상 |
| 엘보우 방법 (Elbow Method) | 이너시아 감소율, 최적 K / K 선택 시각적 방법 |
| 실루엣 점수 ([Silhouette Score](/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/)) | [응집도](/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/), 분리도, -1~1 / K 선택 정량적 방법 |
| EM [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Expectation-Maximization](/studynote/08_algorithm_stats/08_stats/142_em_algorithm/)) | E-Step, M-Step / K-Means의 수학적 프레임 |
| [GMM](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) ([Gaussian Mixture Model](/studynote/14_data_engineering/02_math_mining/114_gaussian_mixture_model/)) | 가우시안 혼합, Soft 할당 / K-Means의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 일반화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [K-Means 군집화 (Kmeans EM)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. K-Means는 운동장에서 친구들을 K개 팀으로 나눌 때, "각 팀 주장(중심점)에게 가장 가까운 사람들이 그 팀"이 되는 방식이야.
2. 팀이 정해지면 주장이 팀원들의 정가운데로 이동하고, 다시 가까운 사람들을 팀으로 묶는 걸 반복하지!
3. 엘보우 방법은 "팀을 더 늘려봤자 각 팀이 더 똘똘 뭉치지 않는 지점"을 찾아 딱 맞는 팀 수(K)를 결정하는 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 263 / 420

<- **이전**: [262. K-NN (K-Nearest Neighbors)](/studynote/10_ai/03_llm_nlp/262_knn/)
**다음**: [264. 나이브 베이즈 (Naive Bayes)](/studynote/10_ai/03_llm_nlp/264_naive_bayes/) ->

---
