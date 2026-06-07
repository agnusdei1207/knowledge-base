---
title: "Outlier Detection"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 397
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/) ([Mahalanobis Distance](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 공분산 구조를 반영해 특성 간 상관관계와 척도 차이를 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)한 거리 측정으로, 유클리드 거리가 포착하지 못하는 다변량 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) (Multivariate [Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))를 탐지한다.
> 2. **가치**: 역공분산 행렬 (Inverse Covariance Matrix, [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) Matrix)을 이용해 상관된 특성들의 이상도를 정확히 측정하며, 카이제곱 (Chi-squared) 분포 임계값으로 통계적 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 기준을 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)한다.
> 3. **판단 포인트**: 공분산 행렬 추정 오류, 고차원 저샘플 문제에서 역행렬 계산 불안정, 비가우시안 분포에서의 한계를 이해하고 Robust 추정법이나 [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest와 함께 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

[이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지 ([Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/))는 제조업 품질 관리, 금융 사기 탐지, 사이버 보안, 의료 진단 등에서 핵심적이다. 단변량 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)는 z-점수로 탐지하지만, 다변량에서는 변수 간 상관관계를 고려해야 한다.

예: 키 180cm / 체중 50kg -> 각 변수 개별로는 정상이지만, 조합으로는 비정상이다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 유클리드 거리는 "단순 자 거리", [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/)는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 분포 형태를 반영한 표준화 거리"다. 타원형 분포에서 진짜 거리를 측정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/) 수식

```
D_M(x) = √((x - μ)ᵀ Σ⁻¹ (x - μ))

x: 관측 벡터 (p차원)
μ: 평균 벡터
Σ: 공분산 행렬 (p×p)
Σ⁻¹: 역공분산 행렬 (Precision Matrix)
```

**유클리드 거리와의 비교**:
```
유클리드: D_E(x) = ||x - μ||₂ = √((x-μ)ᵀ(x-μ))
마할라노비스: D_M(x) = √((x-μ)ᵀ Σ⁻¹ (x-μ))
            = 유클리드 + 공분산 정규화
```

### 역공분산 행렬의 역할

```
상관관계가 높은 두 특성 x₁, x₂:
+------------------------------------------------------+
|  유클리드 기준:                                       |
|  A가 멀어 보임   B가 가까워 보임                      |
|        ↗                                             |
|       ↗ 데이터 분포 방향 (타원)                       |
|      ↗                                               |
|  마할라노비스 기준:                                   |
|  타원을 원으로 변환 후 거리 측정                       |
|  -> 분포 방향 기준으로 진짜 이상치 판별               |
+------------------------------------------------------+
```

**카이제곱 임계값**:
```
가우시안 데이터에서 D_M^ ~ χ^(p) (자유도 p)

이상치 판별:
D_M^ > χ^(p, α)  -> 이상치 (α = 0.01~0.05)
예: p=2, α=0.05 -> D_M^ > 5.99 이면 이상치
```

| 방법 | 다변량 | 척도 불변 | 상관 반영 | 계산 복잡도 |
|:---|:---|:---|:---|:---|
| z-점수 | ✗ | ✓ | ✗ | O(n) |
| 유클리드 거리 | ✓ | ✗ | ✗ | O(nd) |
| 마할라노비스 | ✓ | ✓ | ✓ | O(nd^+d³) |
| [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest | ✓ | ✓ | 암묵적 | O(n log n) |

- **📢 섹션 요약 비유**: 역공분산 행렬은 "상관관계 지도의 역방향 보정기"다. 특성들이 서로 다른 방향으로 연결된 구조를 펼쳐서 독립적으로 만들어 공정하게 거리를 잰다.

---

## Ⅲ. 비교 및 연결

**Robust 공분산 추정**: [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 공분산 추정을 왜곡하는 닭-달걀 문제
- MCD (Minimum Covariance [Determinant](/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)): 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 h부분에서 가장 작은 공분산 추정
- Robust Mahalanobis: MCD 추정값 사용

<strong>LOF (Local <a href="/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">Outlier</a> Factor)</strong>: 지역 밀도 기반 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지 -> 비가우시안 분포에 강함
<strong>One-Class <a href="/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/">SVM</a></strong>: 초구면 경계 기반 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지 ([Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: MCD는 "[이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)를 잠시 빼고 정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만으로 공분산을 추정하는" 더 공정한 방법이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**고차원 문제**: p > n 이면 Σ 역행렬 계산 불가 -> [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Regularization](/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/)): Σ_reg = Σ + λI
<strong>딥러닝 <a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> <a href="/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a></strong>: 특성 추출 -> [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공간에서 [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/) 계산
**마할라노비스 기반 OOD 탐지**: 각 클래스의 훈련 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 분포 학습 -> 새 입력의 최소 클래스 [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/)

기술사 포인트: 유클리드 vs 마할라노비스 비교, 역공분산 행렬의 역할, 카이제곱 임계값 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방법을 체계적으로 설명.

- **📢 섹션 요약 비유**: 고차원 역행렬 불안정성은 "변수가 너무 많아 공분산 행렬이 역행렬이 없는(비가역) 상태"다. [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 항 λI를 더하면 역행렬 계산이 안정된다.

---

## Ⅴ. 기대효과 및 결론

[마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/)는 다변량 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지의 통계적 기반으로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 내부 구조를 반영한 정확한 거리 측정을 제공한다. 딥러닝 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공간에서 OOD (Out-Of-Distribution) 탐지에 직접 적용되며, 모델 안전성과 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 평가의 핵심 도구다.

- **📢 섹션 요약 비유**: [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/)는 도시 지형(공분산 구조)을 반영한 실제 이동 거리다. 직선 거리(유클리드)보다 실제 생활 패턴에 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/) | Σ⁻¹, 공분산 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) / 다변량 거리 측정 |
| 역공분산 행렬 | [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) Matrix / 상관 구조 반영 |
| 카이제곱 임계값 | χ^(p), [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 기준 / 통계적 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 판별 |
| MCD | Robust 추정, h부분 집합 / 견고한 공분산 추정 |
| OOD 탐지 | Out-of-Distribution / 딥러닝 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 응용 |
| [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest | 비모수 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 탐지 / 마할라노비스 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [이상치 탐지 (Outlier Detection)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [마할라노비스 거리](/studynote/14_data_engineering/02_math_mining/106_mahalanobis_distance/)는 "단순 자 거리" 대신 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 생김새(타원형 분포)를 고려한 거리"야.
2. 역공분산 행렬은 특성들 사이의 상관관계를 "평평하게 펼쳐서" 공정하게 비교할 수 있게 해줘.
3. 카이제곱 임계값으로 "이 정도 거리면 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)야"라는 통계적 기준을 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)할 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 397 / 420

<- **이전**: [396. 차분 프라이버시 (Differential Privacy)](/studynote/10_ai/05_data_science_ml/396_differential_privacy/)
**다음**: [398. GAT (Graph Attention Network)](/studynote/10_ai/05_data_science_ml/398_gat/) ->

---
