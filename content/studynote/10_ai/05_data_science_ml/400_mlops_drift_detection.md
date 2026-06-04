+++
title = "400. MLOps 드리프트 탐지 (Mlops Drift Detection)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ML [모델 드리프트](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/) (Drift)는 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 변화 ([데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))나 입력-출력 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화 ([컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/))로 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되는 현상이며, K-S 검정과 PSI가 통계적 탐지의 표준 도구다.
> 2. **가치**: K-S 검정 (Kolmogorov-Smirnov Test)은 두 분포의 CDF (Cumulative Distribution Function) 최대 차이로 분포 변화를 검정하고, PSI ([Population Stability Index](/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/))는 훈련/[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분포의 수치적 안정성 지표를 제공한다.
> 3. **판단 포인트**: PSI < 0.1이면 안정, 0.1~0.25이면 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 강화, > 0.25이면 모델 재학습을 의미하는 경험적 임계값이 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 표준으로 사용된다.

---

## Ⅰ. 개요 및 필요성

프로덕션 ML 모델은 시간이 지나면서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하된다. 이를 조기에 탐지하지 못하면 비즈니스 손실이 발생한다.

드리프트 유형:
- <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">데이터 드리프트</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">Data Drift</a>)</strong>: 입력 분포 변화 (X의 P(X) 변화)
- <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/">컨셉 드리프트</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/">Concept Drift</a>)</strong>: 입력-출력 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화 (P(Y|X) 변화)
- **레이블 드리프트 (Label Drift)**: 출력 분포 변화 (P(Y) 변화)

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 드리프트 탐지는 "강이 계속 같은 물인지, 아니면 오염된 물이 들어왔는지" 수질 검사하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### K-S 검정 (Kolmogorov-Smirnov Test)

```
두 샘플 F₁(x), F₂(x) (경험적 CDF)의 최대 거리:
D = max_x |F₁(x) - F₂(x)|

귀무가설 H₀: 두 분포가 같음
D > D_임계값 -> H₀ 기각 -> 분포 차이 존재 (드리프트)

D_임계값(α=0.05): c(α) · √((n₁+n₂)/(n₁·n₂))
c(0.05) = 1.358
```

### PSI ([Population Stability Index](/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/))

```
PSI = Σᵢ (Actual_i - Expected_i) · ln(Actual_i / Expected_i)

Expected_i: 훈련 데이터의 구간 i 비율
Actual_i: 서비스 데이터의 구간 i 비율
```

**해석 기준**:

| PSI 값 | 해석 | 권고 조치 |
|:---|:---|:---|
| < 0.[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 분포 변화 없음 | [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 유지 |
| 0.[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ~ 0.25 | 약한 변화 | 조사 및 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 강화 |
| > 0.25 | 유의한 변화 | 모델 재학습/교체 |

### [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 아키텍처

```
+----------------------------------------------------------+
|  [프로덕션 서비스] -> 예측 로그 + 실제 레이블             |
|         v                                                |
|  [Feature Store] -> 입력 분포 통계 저장                   |
|         v                                                |
|  [드리프트 탐지 서비스]                                   |
|  매일/매주: K-S 검정, PSI 계산                           |
|         v                                                |
|  [알림/자동 재학습] -> PSI > 0.25 시 트리거              |
+----------------------------------------------------------+
```

**추가 드리프트 탐지 방법**:
- **MMD (Maximum Mean Discrepancy)**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 방법으로 분포 거리 측정
- **JS 다이버전스**: 두 분포 대칭 유사도
- **CUSUM**: 누적 합 기반 변화점 탐지

- **📢 섹션 요약 비유**: PSI는 "강물 표본 검사지"다. 기준치 이상이면 "경보", 훨씬 높으면 "강 폐쇄 후 오염원 제거(재학습)"다.

---

## Ⅲ. 비교 및 연결

| 방법 | 측정 대상 | 통계 | 연속/범주 |
|:---|:---|:---|:---|
| K-S 검정 | 단변량 분포 | D 통계량 | 연속형 |
| PSI | 단변량 분포 | PSI 지수 | 연속/범주 |
| MMD | 다변량 분포 | 평균 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 거리 | 연속형 |
| χ^ 검정 | 범주형 분포 | χ^ 통계량 | 범주형 |
| ADWIN | 개념 드리프트 | 슬라이딩 윈도우 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) |

- **📢 섹션 요약 비유**: K-S는 "두 성적표 점수 분포를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 겹쳐서 가장 차이나는 지점 거리 측정", PSI는 "두 반 학생 성적 구간 분포 비율 차이 측정"이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링 대상</strong>:
1. [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 분포: 각 입력 변수별 K-S/PSI
2. 예측 분포: 모델 출력 분포 변화
3. 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/): 레이블 가용 시 AUC, F1 직접 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링
4. [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중요도: [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) 값 분포 변화

**도구**: WhyLabs, Evidently [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), Great Expectations, [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/)

기술사 포인트: K-S 검정의 CDF 기반 원리와 D 통계량, PSI 수식과 0.[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)/0.25 임계값, 각 드리프트 유형([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/컨셉/레이블)을 명확히 설명.

- **📢 섹션 요약 비유**: 드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링은 모델의 "건강 검진"이다. 주기적으로 혈액 검사(분포 검정)를 하고, 이상 소견(드리프트)이 있으면 치료(재학습)한다.

---

## Ⅴ. 기대효과 및 결론

MLOps에서 드리프트 탐지는 모델의 지속적 품질을 보장하는 핵심 운영 기능이다. K-S 검정의 통계적 엄밀성과 PSI의 직관적 해석 기준을 결합하면 실용적인 드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 시스템을 구축할 수 있다. 자동화된 드리프트 탐지 -> 재학습 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 ML 모델의 장기 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 담보한다.

- **📢 섹션 요약 비유**: PSI > 0.25는 "오래된 지도로는 더 이상 길을 못 찾겠다"는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)다. 새 지도(재학습된 모델)가 필요한 시점이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | P(X) 변화 / 입력 분포 변화 |
| [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) | P(Y / X) 변화 / [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 구조 변화 |
| K-S 검정 | CDF 거리, D 통계량 / 연속 분포 검정 |
| PSI | 구간 비율 차이 / 분포 안정성 지표 |
| [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | 모델 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링, 재학습 / 드리프트 탐지 응용 |
| CUSUM | 변화점 탐지, 누적 합 / 온라인 드리프트 탐지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [MLOps 드리프트 탐지 (Mlops Drift Detection)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 드리프트는 AI가 "작년에 배웠는데 올해 세상이 달라져서 틀리기 시작하는" 것이야.
2. K-S 검정은 "작년 성적 분포와 올해 성적 분포를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 겹쳐보고 가장 차이나는 지점을 측정"하는 거야.
3. PSI가 0.25보다 크면 "세상이 너무 많이 바뀌었으니 AI를 다시 훈련시키자!"는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 400 / 420

<- **이전**: [399. 액티브 러닝 (Active Learning)](/knowledge-base/studynote/10_ai/05_data_science_ml/399_active_learning_qbc/)
**다음**: [401. SMT (Statistical Machine Translation) vs NMT (Neural Machine Translation)](/knowledge-base/studynote/10_ai/05_data_science_ml/401_smt_vs_nmt/) ->

---
