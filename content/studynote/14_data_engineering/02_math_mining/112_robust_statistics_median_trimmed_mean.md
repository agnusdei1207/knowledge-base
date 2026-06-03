+++
title = "112. 로버스트 통계 (Robust Statistics) - 중앙값·절사 평균·이상치 저항 추정량"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로버스트 통계(Robust [Statistics](/knowledge-base/studynote/05_database/03_relational_model/168_clustering_factor_index_physical_alignment/))는 <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a>(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">Outlier</a>)와 분포 가정 위반에 둔감한(<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/">저항</a>성 있는) 통계적 추정량</strong>을 사용하여, 오염된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서도 안정적인 모집단 추론을 가능하게 하는 분야다.
> 2. **가치**: 산술 평균은 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 1개에 극단적으로 왜곡되지만, <strong>중앙값(Median)·절사 평균(Trimmed Mean)·MAD(Median Absolute Deviation)</strong>는 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)의 영향을 제한하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 진정한 중심·산포를 반영한다.
> 3. **판단 포인트**: 붕괴점(Breakdown Point)이 로버스트 추정량의 핵심 지표이며, 중앙값의 붕괴점은 **50%** ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 절반이 오염되어도 유효), 산술 평균의 붕괴점은 **0%** (1개 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에도 무한 왜곡)이다.

---

## Ⅰ. 개요 및 필요성

연봉 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/): [3000, 3200, 3500, 3800, [4000](/knowledge-base/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/), **100,000,000**]. 산술 평균 = 16,670,917원 → 현실과 동떨어진 숫자. 중앙값 = 3,650원 → 실제 중심을 정확히 반영. 이것이 로버스트 통계의 존재 이유다.

```text
┌───────────────────────────────────────────────────────┐
│     산술 평균 vs 중앙값: 이상치 저항성 비교             │
├───────────────────────────────────────────────────────┤
│  데이터: [3, 3.2, 3.5, 3.8, 4, 100,000]              │
│                                                       │
│  산술 평균: 16,670  ← 이상치 1개에 폭발 💥            │
│  중앙값:    3.65    ← 이상치에 무덤덤 😌              │
│  절사 평균: 3.5     ← 양극단 제거 후 평균             │
│                                                       │
│  붕괴점(Breakdown Point):                             │
│   평균:  0%  (이상치 1개로 ∞ 왜곡 가능)               │
│   중앙값: 50% (절반이 오염돼도 유효!)                  │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 산술 평균은 반 평균 키를 구할 때 **거인 1명이 끼면 모두가 농구 선수가 되는** 환상을 만든다. 중앙값은 거인을 무시하고 <strong>진짜 가운데 키</strong>를 알려준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 로버스트 추정량

| 추정량 | 대상 | 붕괴점 | 계산 |
|:---|:---|:---|:---|
| **중앙값 (Median)** | 중심 | **50%** | 정렬 후 가운데 값 |
| **절사 평균 (Trimmed Mean)** | 중심 | $\[alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)$ (절사율) | 양극단 $\[alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)$% 제거 후 평균 |
| **MAD** | 산포 | **50%** | $\text{Median}(\|x_i - \text{Median}(X)\|)$ |
| **Huber M-추정량** | 중심 | ~28% | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 축소 |

### 붕괴점 (Breakdown Point)

추정량이 무한대로 왜곡되지 않고 버틸 수 있는 **오염 비율의 최대값**. 높을수록 로버스트하다.

- **📢 섹션 요약 비유**: 붕괴점은 배(추정량)가 침몰하지 않고 버틸 수 있는 <strong>최대 파도(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a>) 높이</strong>다. 중앙값은 태풍(50%)에도 안 가라앉고, 평균은 잔물결(0%)에도 침몰한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 산술 평균 | 중앙값 | 절사 평균 |
|:---|:---|:---|:---|
| **붕괴점** | 0% | **50%** | $\[alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)$% |
| <strong>효율성 (<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/">정규 분포</a>)</strong> | **100%** | 64% | 중간 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a> <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/">저항</a></strong> | 없음 | **최고** | 높음 |
| **계산 복잡도** | O(n) | O(n log n) | O(n log n) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 시나리오
1. **연봉 통계**: 중앙값 사용 (상위 1%가 평균을 왜곡하므로).
2. <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a></strong>: MAD 기반 Z-score → 전통 표준편차보다 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에 강건.
3. **ML 전처리**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 시 중앙값·IQR 사용 (RobustScaler).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **무조건 중앙값**: [정규 분포](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/)에서는 산술 평균이 더 효율적(분산이 작음). [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 선택해야 한다.

---

## Ⅴ. 기대효과 및 결론

로버스트 통계는 "현실 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 깨끗하지 않다"는 전제에서 출발한다. [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 오작동, 금융 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 극단값, 의료 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기록 오류 등 <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a>가 불가피한 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a></strong>에서 신뢰할 수 있는 분석 결과를 보장하는 필수 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">Outlier</a>)</strong> | 로버스트 통계가 [저항](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)하려는 대상 |
| **중앙값 (Median)** | 붕괴점 50%의 대표적 로버스트 추정량 |
| **MAD** | 로버스트 산포 추정량, 표준편차의 대안 |
| **붕괴점 (Breakdown Point)** | 로버스트 추정량의 핵심 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| **RobustScaler (sklearn)** | ML 전처리에서 중앙값·IQR 기반 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[고전 통계 (평균·표준편차) — 정규 분포 가정]
    │
    ▼
[Tukey (1960s) — 탐색적 데이터 분석, 중앙값·IQR 강조]
    │
    ▼
[Huber (1964) — M-추정량, 이상치 가중치 축소]
    │
    ▼
[붕괴점 이론 (Hampel, 1970s) — 로버스트 추정량 평가 체계]
    │
    ▼
[현재: ML 전처리 표준 — RobustScaler, MAD 기반 이상 탐지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 반에서 키 평균을 구할 때 **NBA 선수 1명이 끼면** 평균 키가 190cm가 돼서 이상해져요.
2. 중앙값(가운데 키)은 NBA 선수를 무시하고 <strong>진짜 우리 반 키</strong>를 알려줘요.
3. 로버스트 통계는 이렇게 <strong>이상한 값에 속지 않는 똑똑한 계산법</strong>이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 258

← **이전**: [111. 마르코프 체인 (Markov Chain) - 전이 행렬과 상태 확률 수렴](/knowledge-base/studynote/14_data_engineering/02_math_mining/111_markov_chain_transition_matrix/)
**다음**: [113. 매니폴드 가설 (Manifold Hypothesis) - 고차원 데이터와 차원 축소의 수학적 근거](/knowledge-base/studynote/14_data_engineering/02_math_mining/113_manifold_hypothesis_dimensionality_reduction/) →

---
