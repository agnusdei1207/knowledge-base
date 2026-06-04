---
title: "361. 다중 공선성 (Multicollinearity) 과 VIF (Variance Inflation Factor)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)([Multicollinearity](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/))은 회귀 모델에서 [독립 변수](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)들 간에 강한 선형 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 존재할 때 발생하는 현상으로, 계수 추정이 불안정해지고 해석이 불가능해진다. VIF([Variance](/studynote/08_algorithm_stats/08_stats/136_variance/) Inflation Factor, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 팽창 지수)는 이를 수치화한 진단 도구다.
> 2. **가치**: VIF > 10인 변수는 [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)이 심각하다고 판단하여 Ridge [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(L2), [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/), 또는 변수 제거로 대응한다. 트리 계열 모델([랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/), XGBoost)은 분할 기반이라 [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)에 면역이다.
> 3. **판단 포인트**: VIF_j = 1/(1-R^_j) (j번째 변수를 나머지 변수로 회귀한 R^). VIF=1이면 무관, VIF=10이면 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 10배 팽창(표준 오차 √[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ≈ 3.16배 증가).

---

## Ⅰ. 개요 및 필요성

주택 가격 예측 모델에서 "방 개수"와 "거실 면적"이 모두 특성으로 들어갔을 때 이 둘은 강한 상관관계를 가진다. 회귀 계수를 추정할 때 "(방 개수 효과) + (거실 면적 효과)"를 분리하기 어려워, 작은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변동에도 계수가 크게 요동친다. 이것이 [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)이다. 해석 관점에서 "방 개수를 1개 늘리면 가격이 500만원 오른다"는 결론을 내릴 수 없게 된다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)은 "두 탐정이 서로 같은 증거만 제출하는 상황"이다. 탐정 A(방 개수)와 탐정 B(거실 면적)가 거의 같은 증거(상관관계)를 제출하면, 판사(회귀 모델)가 "둘 중 누가 진짜 결정적 증인인가?"를 판단하지 못하고 계수가 불안정해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------+
|         VIF (Variance Inflation Factor) 계산             |
+----------------------------------------------------------+
|  VIF_j = 1 / (1 - R^_j)                                |
|                                                          |
|  R^_j: 특성 j를 나머지 특성들로 선형 회귀한 결정 계수   |
|                                                          |
|  해석:                                                   |
|  VIF = 1.0  -> 다중 공선성 없음 (완전 독립)             |
|  VIF = 5.0  -> 주의 필요 (R^ = 0.80)                   |
|  VIF = 10.0 -> 심각한 다중 공선성 (R^ = 0.90)          |
|  VIF = ∞   -> 완전 공선성 (R^ = 1.00)                  |
|                                                          |
|  분산 팽창 의미:                                        |
|  Var(β̂_j) = VIF_j · σ^/(n·Var(Xj))                   |
|  -> VIF가 크면 계수 분산 ^ -> 표준 오차 ^ -> t값 v      |
|  -> 통계적 유의성 상실                                   |
+----------------------------------------------------------+
```

| VIF 값 | 공선성 정도 | 대응 방법 |
|:---|:---|:---|
| 1 ~ 5 | 없음~약함 | 문제 없음 |
| 5 ~ [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 보통 | [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 필요 |
| > [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 심각 | Ridge/[PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)/변수 제거 |
| > 100 | 극심 | 즉시 조치 |

- **📢 섹션 요약 비유**: VIF는 "공선성 온도계"다. 온도(VIF)가 1+C면 건강(무관), 37+C면 미열(주의), 40+C면 고열(위험)이다. 열이 나는 원인(공선성 변수)을 찾아 약(Ridge/변수 제거)을 처방한다.

---

## Ⅲ. 비교 및 연결

Ridge 회귀(L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)): 비용 함수에 ||β||^ 페널티를 추가하면 (XᵀX + λI)를 역행렬로 사용해 완전 공선성(XᵀX 특이 행렬)에서도 안정적으로 역행렬 계산이 가능하다. 트리 기반 모델(결정 트리, [랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/), XGBoost)은 특성을 독립적으로 분할하므로 [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)의 영향을 받지 않는다. 단, 변수 중요도 해석에서 상관 변수들이 중요도를 나눠 가지는 문제는 여전히 존재한다.

- **📢 섹션 요약 비유**: Ridge vs 트리 모델의 공선성 대응: Ridge는 "공선성 탐정들을 공평하게 처리"하는 반면, 트리는 "증인 한 명만 채택해 판결"하므로 공선성 자체가 문제되지 않는다. 하지만 어느 탐정이 더 중요한지 해석은 여전히 어렵다.

---

## Ⅳ. 실무 적용 및 기술사 판단

공선성 탐지 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/): ① VIF 계산 -> ② 상관 행렬(Correlation Matrix) 히트맵 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) -> ③ 조건 지수(Condition [Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) > 30 체크. 대응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택: 해석가능성 중요 -> Ridge + 변수 제거, 예측 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 중요 -> [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) + Ridge, 블랙박스 허용 -> 트리 기반 모델. 표준화(Standardization) 후 VIF 계산이 수치 안정성을 높인다.

- **📢 섹션 요약 비유**: 공선성 대응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "겹치는 과목 정리"와 같다. 수학과 물리가 90% 겹친다면(공선성) ① 물리 제거(변수 제거), ② 두 과목 평균 점수 사용([PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)), ③ Ridge로 둘 다 약하게 반영, 중 하나를 선택하는 것이다.

---

## Ⅴ. 기대효과 및 결론

[다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/) 진단과 VIF는 통계 모델의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 보장하는 핵심 전처리 단계다. 기업 의사결정 지원 모델에서 계수 해석의 오류를 방지하고, 규제 환경(금융 모델 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))에서 모델의 안정성을 입증하는 데 필수적이다. 기술사 시험에서 VIF 수식, VIF>[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 기준, Ridge와의 연결을 명확히 서술하면 고득점이다.

- **📢 섹션 요약 비유**: VIF 검사는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 "건강 검진"이다. 회귀 모델을 의사에게 데리고 가서 "계수들 사이에 너무 비슷한 게 있어서 판단이 흔들리지 않나요?"를 VIF로 체크받는 과정이다. 고열(VIF>[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/))이 발견되면 약(Ridge/[PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))을 처방해 건강한 모델을 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Ridge 회귀 (L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | λI 추가 / 공선성 해결의 표준 처방 |
| [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)) | [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) / 공선성 제거 + [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) |
| OLS (Ordinary Least Squares) | 선형 회귀 / 공선성에 가장 취약한 방법 |
| 트리 기반 모델 (Tree-based Models) | [랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/) / 공선성 면역 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [다중 공선성 (Multicollinearity) 과 VIF (Variance Inflation Factor)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [다중 공선성](/studynote/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression/)은 "두 친구가 항상 붙어다니는 상황"이에요. AI가 "A가 문제야? B가 문제야?"를 구분 못해요.
2. VIF는 "얼마나 붙어다니는지" 측정하는 온도계예요. VIF > 10이면 너무 붙어다녀 문제가 생겨요.
3. Ridge [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)나 PCA로 이 문제를 해결하거나, 트리 AI처럼 애초에 이 문제가 없는 방법을 쓰면 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 361 / 420

<- **이전**: [360. GMM (Gaussian Mixture Model) 과 EM 알고리즘](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)
**다음**: [362. ROC 곡선과 AUC (Receiver Operating Characteristic / Area Under Curve)](/studynote/10_ai/05_data_science_ml/362_roc_auc_math/) ->

---
