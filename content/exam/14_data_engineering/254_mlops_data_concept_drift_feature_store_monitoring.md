---
title: "254. Mlops Data Concept Drift Feature Store Monitoring"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/)([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 ML 모델을 실험 단계에서 프로덕션(Production)까지 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있게 운영하는 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 확장 패러다임이다.
> 2. **가치**: [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)([Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))와 [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) 자동 탐지 및 [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)([Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/))를 통한 특징 재사용이 ML 시스템의 안정성과 개발 생산성을 동시에 높인다.
> 3. **판단 포인트**: 드리프트 탐지 후 자동 재훈련(Retraining) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 임계값(Threshold) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 과민 재훈련(비용 낭비)과 방치([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하) 사이의 균형을 결정한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 MLOps가 필요한 이유: ML [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)(ML [Technical Debt](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/))

구글 논문 "Hidden [Technical Debt](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) in Machine [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Systems"에 따르면, ML 시스템에서 실제 ML 코드의 비중은 전체의 5% 미만이다. 나머지 95%는 인프라·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·모니터링·서빙 코드다.

```
ML 시스템 구성 요소:
+-----------------------------------------------------+
|                                                     |
|  +---------+                          +----------+  |
|  |데이터 수집|  +----------+          |  서빙   |  |
|  | 파이프라인|  |          |          |  인프라  |  |
|  +---------+  |  ML 코드  |          +----------+  |
|  +---------+  |  (5%)    |          +----------+  |
|  |피처 추출 |  |          |          |  모니터링 |  |
|  | 변환    |  +----------+          |  알람    |  |
|  +---------+                        +----------+  |
|  +---------+                        +----------+  |
|  |데이터 검증|                        | 구성 관리 |  |
|  +---------+                        +----------+  |
|                                                     |
|  ^ 나머지 95%: MLOps가 관리하는 영역                 |
+-----------------------------------------------------+
```

### 1.2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도 레벨(Maturity Level)

| 레벨 | 특징 | 자동화 수준 |
|:---|:---|:---|
| **Level 0** | 수동 훈련·배포 | 없음 |
| **Level 1** | ML 파이프라인 자동화, [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | 부분 |
| **Level 2** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 완전 자동화, [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), 모니터링 | 완전 |

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 없는 ML은 자동차를 만들어 놓고 정비소가 없는 것과 같다. 처음엔 잘 달리지만 시간이 지나면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 떨어지고, 문제가 생겨도 언제 어디서 망가졌는지 알 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)([Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) vs [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/))

```
+-----------------------------------------------------------------+
|               드리프트 유형 비교                                  |
+-----------------------+-----------------------------------------+
|   데이터 드리프트      |          컨셉 드리프트                   |
|   (Data Drift)        |          (Concept Drift)                |
+-----------------------+-----------------------------------------+
|                       |                                         |
|  입력 데이터 X의       |  입력-출력 관계 P(Y|X) 변화             |
|  분포 P(X) 변화        |                                         |
|                       |                                         |
|  예시: 이커머스 사이트  |  예시: 코로나 전후 소비 패턴 변화       |
|  - 신규 고객층 유입    |  - 같은 X(나이·소득)지만               |
|  - 연령대 분포 변화    |    구매 행동 Y가 달라짐                 |
|                       |                                         |
|  탐지: KL발산,         |  탐지: 모델 성능 지표                   |
|       PSI(Population  |       (정확도·F1) 저하 모니터링          |
|       Stability Index)|                                         |
+-----------------------+-----------------------------------------+
```

### 2.2 드리프트 탐지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| 방법 | 수식/원리 | 적합 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
|:---|:---|:---|
| <strong>PSI(<a href="/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/">Population Stability Index</a>)</strong> | Σ(실제%-기대%)×ln(실제%/기대%) | 범주형, 연속형 |
| **KS Test(Kolmogorov-Smirnov)** | 두 누적분포 함수 최대 차이 | 연속형 |
| **ADWIN(Adaptive Windowing)** | 슬라이딩 윈도우 평균 변화 탐지 | 스트림 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **CUSUM(Cumulative Sum)** | 누적 합 변화점 탐지 | 단변량 시계열 |

PSI 해석 기준: PSI < 0.1 (안정), 0.1~0.2 (경고), > 0.2 (재훈련 필요)

### 2.3 [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)([Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)) 아키텍처

```
+-----------------------------------------------------------------+
|                  피처 스토어 (Feature Store)                     |
+-----------------------------------------------------------------+
|                                                                  |
|  데이터 소스                피처 변환 파이프라인                   |
|  +--------+  +------+    +---------------------+               |
|  | 원시   |  | 배치 |    |  피처 엔지니어링      |               |
|  | 데이터  |-►| ETL  |---►|  (Feature Engineering|               |
|  +--------+  +------+    |   Spark/Flink)       |               |
|                           +----------+----------+               |
|                                      |                           |
|                    +-----------------+--------------+           |
|                    |                                |           |
|            +-------v------+              +----------v------+   |
|            |  오프라인 스토어 |              |  온라인 스토어   |   |
|            | (Offline Store)|              | (Online Store)  |   |
|            |  S3/Hive      |              |  Redis/DynamoDB |   |
|            |  (배치 학습용) |              |  (실시간 서빙용) |   |
|            +--------------+              +----------------+   |
|                    |                              |             |
|                    +----------+-------------------+             |
|                               |                                 |
|                       +-------v-------+                         |
|                       |  피처 레지스트리|                         |
|                       | (Feature Registry|                        |
|                       |  메타데이터·버전)|                        |
|                       +---------------+                         |
+-----------------------------------------------------------------+
```

### 2.4 ML 플랫폼 비교

| 플랫폼 | 제공사 | 핵심 강점 | 적합 환경 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a></strong> | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) | 실험 추적, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/), [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) |
| <strong><a href="/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/">Kubeflow</a></strong> | Google | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 기반, 파이프라인 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | GCP/온프렘 |
| **SageMaker** | AWS | 완전 관리형, 엔드투엔드 | AWS 중심 |
| <strong>Vertex <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong> | Google | [AutoML](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/), [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) 통합 | GCP 중심 |
| **Azure ML** | Microsoft | .NET 생태계, [Responsible AI](/studynote/09_security/19_ai_advanced_security/973_responsible_ai/) 도구 | Azure 중심 |

📢 **섹션 요약 비유**: [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)는 회사의 공용 식자재 창고다. 각 팀이 똑같은 재료([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/))를 각자 준비하는 낭비 대신, 한 곳에 잘 손질된 재료를 보관해두고 빠르게 꺼내 쓴다. 오프라인 스토어는 냉동 창고(학습용), 온라인 스토어는 바로 꺼내 쓰는 냉장고(서빙용)다.

---

## Ⅲ. 비교 및 연결

### 3.1 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인 비교

| 개념 | 의미 | ML 맥락 |
|:---|:---|:---|
| <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>(<a href="/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/">Continuous Integration</a>)</strong> | 코드 지속 통합·테스트 | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 코드·훈련 코드 [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) |
| <strong>CD(<a href="/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>)</strong> | 자동 배포 준비 | 검증된 모델 스테이징 자동 배포 |
| <strong><a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a>(<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>)</strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화 시 자동 재훈련 | 드리프트 탐지 -> 재훈련 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |

### 3.2 모델 재훈련 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 조건 | 장단점 |
|:---|:---|:---|
| **시간 기반** | 주 1회·월 1회 정기 재훈련 | 단순, 과훈련 위험 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 기반</strong> | F1 점수 < 0.85 하락 시 | 정확, 탐지 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 있음 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반</strong> | PSI > 0.2 드리프트 탐지 시 | 예방적, 임계값 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 어려움 |
| **이벤트 기반** | 시장 이벤트·[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경 감지 시 | 맥락 반영, 자동화 어려움 |

📢 **섹션 요약 비유**: 모델 재훈련 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 자동차 엔진 오일 교체와 같다. 주행 거리(시간 기반), 경고등 점등([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기반), 오일 품질 직접 측정([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반) 세 가지 방법을 모두 병행하는 것이 최선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 구현 로드맵

```
1단계 (즉시): 실험 추적 (MLflow Tracking)
  -> 모든 실험의 파라미터·지표·아티팩트 자동 기록

2단계 (1~3개월): 모델 레지스트리 (Model Registry)
  -> 스테이징/프로덕션 모델 버전 관리

3단계 (3~6개월): 모니터링 대시보드
  -> Prometheus + Grafana로 드리프트·성능 시각화

4단계 (6~12개월): 자동 재훈련 파이프라인
  -> 드리프트 탐지 -> 재훈련 -> 검증 -> 자동 배포

5단계 (완성): 피처 스토어 구축
  -> Feast/Tecton으로 피처 재사용·버전 관리
```

### 4.2 기술사 논술 핵심 포인트

- **테스트 피라미드(Test Pyramid)**: [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 변환) -> [통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/)(파이프라인) -> [E2E](/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트(전체 서빙)
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/">섀도우 배포</a>(<a href="/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/">Shadow Deployment</a>)</strong>: 새 모델을 실 트래픽에 그대로 노출하지 않고 복사본으로 테스트
- <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a>(<a href="/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">Canary Deployment</a>)</strong>: 5% 트래픽에만 새 모델 적용 후 점진 확대

📢 **섹션 요약 비유**: MLOps는 항공기 정비 시스템이다. 비행기(ML 모델)는 한 번 만들어 출고하면 끝이 아니라, 지속적 점검(모니터링), 부품 교체(재훈련), 새로운 유형의 모델로의 점진적 전환([카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/))이 필수적이다. 정비 없는 항공기는 언젠가 추락한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입 효과

| 지표 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 전 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 후 |
|:---|:---|:---|
| **모델 배포 시간** | 수 주~수 개월 | 수 시간~수 일 |
| **드리프트 탐지** | 수동·사후 | 실시간 자동 탐지 |
| <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 재사용률</strong> | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 미만 | 60~80% |
| <strong>모델 장애 <a href="/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a></strong> | 수 일 | 수 시간 이내 |
| **재현성(Reproducibility)** | 낮음 | 완전 재현 가능 |

### 5.2 결론

MLOps는 ML을 연구 프로젝트에서 신뢰할 수 있는 비즈니스 인프라로 격상시키는 운영 철학이다. [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)·드리프트 모니터링·[CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인의 삼각 구도가 완성될 때, ML 시스템은 자가 치유(Self-healing)에 가까운 자동화된 생명 주기를 갖추게 된다.

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 완성은 자율주행 자동차와 같다. 처음엔 사람이 직접 운전했고(수동 ML), 다음엔 GPS·브레이크 보조 장치가 생겼고(Level 1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/)), 완전 자율주행(Level 2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/))에서는 차가 스스로 경로를 수정하고 정비소를 예약한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 패러다임 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/)([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/)) | ML [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 자동화 |
| 문제 탐지 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)([Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) | 입력 분포 P(X) 변화 |
| 문제 탐지 | [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | 입력-출력 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) P(Y\|X) 변화 |
| 탐지 지표 | PSI([Population Stability Index](/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/)) | 분포 안정성 수치화 |
| 인프라 | [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)([Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)) | 온·오프라인 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중앙 관리 |
| 플랫폼 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | 실험 추적·[모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) |
| 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)([Canary Deployment](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)) | 소규모 트래픽 점진 확대 |
| 자동화 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | 드리프트 탐지 -> 자동 재훈련 |

### 👶 어린이를 위한 3줄 비유 설명
1. MLOps는 AI를 만들고 잊어버리는 것이 아니라, 계속 건강하게 유지하는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 병원이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 ML 실험 (노트북 기반)
    |
    v
MLOps: CI/CD/CT -> 모델 자동 학습·배포·모니터링
    +-► Data Drift · Concept Drift 탐지
    +-► Feature Store: 피처 재사용 · 일관성
    +-► Model Registry · A/B Test · Canary
    |
    v
LLMOps · AIOps: 차세대 운영 자동화
```
2. [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 "환자가 바뀌었는데 옛날 처방전을 그대로 쓰는 것"이고, [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)는 "환자는 같은데 병의 특성이 바뀐 것"이에요—둘 다 새 처방(재훈련)이 필요해요.
3. [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)는 학교 공용 실험실 재료 창고예요. 모든 반이 같은 재료를 따로 준비하는 낭비 없이 한 곳에서 꺼내 쓰니까 시간이 훨씬 절약돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 254 / 258

<- **이전**: [253. 강화 학습 (Reinforcement Learning) MDP 정책 가치 Q러닝 DQN](/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)
**다음**: [255. XAI (Explainable AI) 설명 가능 AI LIME SHAP 기여도 분할](/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/) ->

---
