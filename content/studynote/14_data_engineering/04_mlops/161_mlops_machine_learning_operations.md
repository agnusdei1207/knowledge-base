---
title: "161. Mlops Machine Learning Operations"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 ML 모델의 개발(Dev)과 운영(Ops)을 통합하여, 실험실 모델을 신뢰할 수 있는 프로덕션 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 자동화하는 전체 생명주기 관리 체계다.
> 2. **가치**: [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))을 더해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·코드·모델 3축을 동시에 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리하고, [모델 드리프트](/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/)에 자동으로 반응함으로써 운영 비용을 절감하고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질을 지속 보장한다.
> 3. **판단 포인트**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도(Level 0->2)가 높을수록 자동화 범위가 넓어지고 재현성(Reproducibility)·[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit Trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/))이 강화되나, [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 인프라 투자와 조직 문화 변화가 선행되어야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 MLOps란?

<strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> (<a href="/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/">Machine Learning Operations</a>)</strong>는 기계학습 시스템의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 배포와 유지 관리를 위해 ML, [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링의 교집합에서 탄생한 실천 방법론이다.

기존 소프트웨어는 코드만 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리하면 되었지만, ML 시스템은 <strong>코드 + <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> + 모델</strong> 3요소가 모두 변하기 때문에 기존 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 관행만으로는 운영이 어렵다.

```
전통 소프트웨어           ML 시스템
+-----------------+     +------------------------------+
|   Code (코드)   |     |  Code  |  Data  |  Model     |
|   버전 관리     |     |  코드  |  데이터|  모델       |
|   테스트/배포   |     |  변화  |  변화  |  드리프트   |
+-----------------+     +------------------------------+
        v                           v
  CI/CD 충분           CI / CD / CT (3축 자동화) 필요
```

### 1.2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 등장 배경

| 문제 | 설명 |
|:---|:---|
| **재현성 부재** | 같은 코드라도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 다르면 다른 모델이 나옴 |
| **배포 병목** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트가 만든 모델을 엔지니어가 다시 구현하는 "번역 비용" |
| **모델 부패** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 변화로 시간이 지날수록 예측 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 (Model Decay) |
| **실험 관리 부재** | 수천 번의 실험 결과를 수동으로 관리하는 비효율 |
| <strong>규제·<a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong> | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act 등에서 모델 의사결정 설명 및 추적 요구 |

### 1.3 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) vs [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 비교

| 항목 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) |
|:---|:---|:---|
| **관리 대상** | 코드 | 코드 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + 모델 |
| **테스트 기준** | 유닛/[통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) + 모델 품질 테스트 |
| <strong>배포 <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong> | 코드 변경 | 코드 변경 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경 + [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 |
| **모니터링** | 시스템 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) (CPU, 메모리) | 모델 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) (정확도, 드리프트) |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 단위</strong> | 코드 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| **자동화 추가** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD + [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) |

📢 **섹션 요약 비유**: MLOps는 자동차 공장의 품질관리 시스템과 같다. 소프트웨어 개발이 자동차 설계 도면(코드) 하나만 관리하면 됐다면, ML은 도면(코드) + 원자재 규격([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) + 완성차 품질(모델) 세 가지를 동시에 품질 보증해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 3대 자동화 축

| 자동화 | 설명 | [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
|:---|:---|:---|
| <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a> (<a href="/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/">Continuous Integration</a>)</strong> | 코드 변경 시 자동 빌드·테스트·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | Git push |
| <strong>CD (<a href="/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>)</strong> | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 모델을 자동으로 스테이징/프로덕션 배포 | 모델 품질 통과 |
| <strong><a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a> (<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>)</strong> | 새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유입 또는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 시 자동 재학습 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |

### 2.2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 전체 아키텍처

```
+-----------------------------------------------------------------+
|                        MLOps 생명주기                            |
+----------+----------+----------+----------+----------+----------+
|  데이터  |  피처    |  모델    |  모델    |  서빙    |  모니터  |
|  수집    |  엔지니  |  학습    |  평가    |  배포    |  링      |
|  검증    |  어링    |  실험    |  검증    |  &API    |  알람    |
+----------+----------+----------+----------+----------+----------+
|                     자동화 레이어                                 |
|   CI (코드/데이터 검증) | CD (모델 배포) | CT (자동 재학습)      |
+-----------------------------------------------------------------+
|                     인프라 레이어                                 |
|   피처 스토어 | 모델 레지스트리 | 실험 추적 | 오케스트레이션     |
+-----------------------------------------------------------------+
```

### 2.3 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도 3단계 (Google [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도 모델)

```
Level 0 (수동)              Level 1 (자동 파이프라인)    Level 2 (CI/CD 파이프라인)
+--------------------+     +------------------------+  +--------------------------+
| 데이터 사이언티스트|     |  자동화된 ML 파이프라인 |  |  CI/CD + CT 완전 자동화  |
| 가 수동으로        |     |  데이터 -> 학습 -> 배포  |  |  코드 변경만으로         |
| 데이터 처리        | ->   |  자동화                 |-> |  전체 파이프라인 실행    |
| -> 모델 학습        |     |  CT 자동 재학습         |  |  다중 팀 협업 가능       |
| -> 수동 배포        |     |  실험 추적              |  |  모델 레지스트리 연동    |
+--------------------+     +------------------------+  +--------------------------+
  특징: Jupyter Notebook     특징: Kubeflow, MLflow       특징: 완전 자동화
  한계: 재현 불가, 느림       한계: 파이프라인만 자동화    수준: 대규모 ML 서비스
```

#### 성숙도별 상세 비교

| 항목 | Level 0 | Level 1 | Level 2 |
|:---|:---|:---|:---|
| **학습 방식** | 수동 스크립트 | 자동 파이프라인 | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
| **배포 방식** | 수동 배포 | 자동 배포 | 자동 배포 + [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **재학습** | 없음/수동 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 자동화 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) + [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 |
| **실험 추적** | 없음 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)/W&B | 완전 자동화 |
| <strong><a href="/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">모델 레지스트리</a></strong> | 없음 | 있음 | 완전 연동 |
| **적합 조직** | 스타트업 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) | 성장기 기업 | 대규모 ML 조직 |

### 2.4 핵심 구성요소 상세

```
+-----------------------------------------------------------------+
|                    MLOps 핵심 구성요소                           |
+----------------+------------------------------------------------+
| 데이터 파이프  |  데이터 수집 -> 검증(Great Expectations)        |
| 라인           |  -> 전처리 -> 피처 스토어 저장                   |
+----------------+------------------------------------------------+
| 모델 학습      |  실험 추적(MLflow) -> 하이퍼파라미터 튜닝        |
| 파이프라인     |  -> 분산 학습(Horovod) -> 모델 평가              |
+----------------+------------------------------------------------+
| 모델 레지스트  |  버전 관리 -> Staging -> Production              |
| 리             |  -> Archived 상태 전이                          |
+----------------+------------------------------------------------+
| 모델 서빙      |  REST/gRPC API -> 동적 배치 -> A/B 테스트        |
| 플랫폼         |  -> 카나리 배포 -> 롤백                          |
+----------------+------------------------------------------------+
| 모니터링       |  데이터 드리프트 -> 모델 성능 -> 인프라 메트릭   |
| & 알람         |  -> 자동 재학습 트리거                          |
+----------------+------------------------------------------------+
```

### 2.5 주요 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도구 생태계

| 카테고리 | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 클라우드 관리형 |
|:---|:---|:---|
| <strong>파이프라인 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a></strong> | [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/), Airflow | Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Pipelines, SageMaker Pipelines |
| **실험 추적** | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), Weights & Biases | SageMaker Experiments |
| <strong><a href="/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/">피처 스토어</a></strong> | Feast, Hopsworks | Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), SageMaker [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) |
| <strong><a href="/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">모델 레지스트리</a></strong> | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/), SageMaker [Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) |
| **모델 서빙** | Triton, TF Serving, KServe | SageMaker Endpoints, Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Endpoints |
| **모니터링** | Evidently [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), WhyLogs | SageMaker Model [Monitor](/studynote/02_operating_system/04_synchronization/229_monitor/) |

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 아키텍처는 자동화된 자동차 조립 라인과 같다. Level 0은 장인이 손으로 한 대씩 만드는 방식이고, Level 1은 컨베이어 벨트로 부품을 이어주는 방식이며, Level 2는 센서가 품질 이상을 감지하면 라인 자체가 레시피를 바꾸는 완전 자동화 공장이다.

---

## Ⅲ. 비교 및 연결

### 3.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) vs [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) vs [AIOps](/studynote/12_it_management/02_itsm_itil/883_aiops_chatbot_itsm_automation/)

| 항목 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) | [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) | [AIOps](/studynote/12_it_management/02_itsm_itil/883_aiops_chatbot_itsm_automation/) |
|:---|:---|:---|:---|
| **정의** | ML 모델 생명주기 자동화 | [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 자동화 | IT 운영의 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 적용 |
| **목적** | 모델 품질·속도 향상 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·속도 향상 | IT 장애 예측·자동 해결 |
| **핵심** | [모델 드리프트](/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/) 관리 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 관리 | [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)·자동화 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) 위에서 동작 | MLOps의 기반 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 결과물 활용 |

### 3.2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 핵심 개념 간 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

```
데이터 드리프트 감지
        |
        v
  CT 트리거 발동
        |
        v
피처 스토어에서 최신 피처 조회
        |
        v
  모델 재학습 실행
        |
        v
모델 레지스트리에 새 버전 등록
        |
        v
카나리 배포 -> A/B 테스트 -> 전체 배포
        |
        v
  모니터링 -> 이상 시 롤백
```

### 3.3 ML 프로젝트 실패 원인 Top 5

| 원인 | 발생 비율 | MLOps로 해결 |
|:---|:---:|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 문제</strong> | 40% | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화 |
| <strong>모델 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하</strong> | 25% | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) + 드리프트 모니터링 |
| **배포 복잡성** | 15% | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인 |
| **재현성 부재** | 12% | 실험 추적, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) |
| **팀 협업 부재** | 8% | 표준화된 워크플로우 |

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/), [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/), AIOps의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 건설 현장의 기반([DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/)) 위에 건물([MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/))을 짓고, 건물 관리 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([AIOps](/studynote/12_it_management/02_itsm_itil/883_aiops_chatbot_itsm_automation/))가 모든 설비를 자동 점검·수리하는 구조와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입 단계별 로드맵

| 단계 | 기간 | 주요 작업 |
|:---|:---|:---|
| **기반 구축** | 1~3개월 | 실험 추적 도구 도입, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| **파이프라인 자동화** | 3~6개월 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인 구축, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) 도입 |
| **서빙 자동화** | 6~12개월 | A/B 테스트, [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/), 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |
| **완전 자동화** | 12개월+ | 드리프트 감지 -> [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) -> 배포 전 과정 자동화 |

### 4.2 기술사 시험 핵심 포인트

<strong>Q. MLOps에서 <a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD/CT의 역할을 설명하시오.</strong>

- <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a> (<a href="/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/">Continuous Integration</a>)</strong>: 코드 변경 및 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경 시 자동 빌드, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 실행
- <strong>CD (<a href="/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>/<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a>)</strong>: [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 모델을 스테이징 환경 자동 배포, 프로덕션 승인 후 자동 적용
- <strong><a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a> (<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>)</strong>: 새 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 도착, [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 감지, 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 임계값 하락 시 자동 재학습 파이프라인 실행

**Q. MLOps와 DevOps의 차이점을 설명하시오.**

핵심 차이는 <strong>관리 대상의 복잡성</strong>에 있다. DevOps는 결정론적(Deterministic) 소프트웨어를 다루지만, MLOps는 확률론적(Probabilistic) 모델과 진화하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룬다. 따라서 코드 변경 없이도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화만으로 배포가 실패할 수 있고, [모델 드리프트](/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/)라는 새로운 운영 개념이 추가된다.

### 4.3 실무 아키텍처 예시 (전자상거래 [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/))

```
사용자 행동 데이터 (실시간)
        |
        v
Kafka -> Spark Streaming -> 피처 스토어 (Feast)
                                |
                                +--> 오프라인 스토어 (S3/BigQuery)
                                |         -> 주기적 모델 재학습
                                |
                                +--> 온라인 스토어 (Redis)
                                          -> 실시간 추천 API

모델 재학습 파이프라인 (Kubeflow)
  데이터 검증 -> 피처 추출 -> 학습 -> 평가 -> 모델 레지스트리 등록
                                              -> 카나리 배포 (5%)
                                              -> A/B 테스트 (CTR 비교)
                                              -> 전체 배포 또는 롤백
```

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입은 수작업 요리사에서 HACCP [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 식품공장으로 전환하는 것과 같다. 맛(모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))을 유지하면서 위생([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질), 레시피 이력 관리(실험 추적), 자동 이상 감지(드리프트 모니터링)까지 모두 갖춰야 진정한 대량 생산(스케일아웃)이 가능하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **모델 배포 시간** | 수주 | 수시간 | 90% 단축 |
| **실험 재현성** | 불가 | 완전 재현 | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 가능 |
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/">모델 드리프트</a> 감지</strong> | 수동/늦음 | 자동/즉시 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 유지 |
| **팀 협업** | [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) | 표준화 | 전달 비용 제거 |
| **규정 준수** | 어려움 | 자동 기록 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act 대응 |

### 5.2 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성공 요인

1. **조직 문화**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트와 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 엔지니어 간 협업 문화
2. <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a></strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·보안·접근 제어 체계
3. **표준화**: 재사용 가능한 파이프라인 컴포넌트와 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의
4. **점진적 도입**: Level 0 -> Level 1 -> Level 2 단계적 전환

### 5.3 결론

MLOps는 ML 프로젝트가 PoC (Proof of [Concept](/studynote/14_data_engineering/02_math_mining/120_concept/))에 머무르지 않고 실제 비즈니스 가치를 창출하는 프로덕션 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 되기 위한 핵심 인프라다. [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 3축 자동화와 [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/), 드리프트 모니터링의 유기적 통합이 고품질 ML [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 지속 운영을 가능케 한다.

📢 **섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 없는 ML은 운전 실력은 있지만 정비소가 없는 자동차와 같다. 처음엔 잘 달리지만 시간이 지나면 고장([모델 드리프트](/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/))이 나고, 언제 어떻게 고장났는지도 모른 채 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 멈춘다. MLOps는 자동 정비소([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)), 부품 이력 관리([레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)), 주행 기록계(모니터링)를 모두 갖춘 종합 자동차 관리 시스템이다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 구성요소 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화 시 자동 재학습 |
| 구성요소 | [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)) | 훈련/서빙 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 |
| 구성요소 | [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ([Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)) | 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·라이프사이클 관리 |
| 문제 해결 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) | 입력 분포 변화 감지 |
| 문제 해결 | [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | 입출력 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화 감지 |
| 도구 | [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) | [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반 ML 파이프라인 |
| 도구 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | 실험 추적 + [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) |
| 도구 | [Apache Airflow](/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 워크플로우 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |
| 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | A/B 테스트 | 트래픽 분할 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 |
| 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 ([Canary Rollout](/studynote/14_data_engineering/04_mlops/170_ab_test_canary_rollout_shadow_mirroring/)) | 점진적 트래픽 증가 |
| 상위 개념 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | 코드 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 자동화의 원형 |
| 연관 개념 | [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) | [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 자동화 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. MLOps는 학교 급식 공장과 같아요. 맛있는 레시피(모델)를 만들고, 재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 바뀌면 레시피를 자동으로 업데이트하고, 급식이 맛없어지기 전에 알아서 고쳐요.
2. 로봇 청소기처럼 처음에 사람이 길을 가르쳐주면(학습), 이후엔 혼자 청소하다가(서빙), 새 가구가 생기면([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) 다시 지도를 배워요([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)).
3. 자동화된 과자 공장처럼, 과자(모델) 레시피를 만들고, 맛 검사(모니터링)를 통과하면 포장해서 판매하고(배포), 맛이 변하면 자동으로 레시피를 수정해요([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)).

### 📈 관련 키워드 및 발전 흐름도

```text
DevOps (코드 CI/CD)
    |
    v
MLOps Level 0 — 수동 ML 파이프라인
    |
    v
MLOps Level 1 — ML 파이프라인 자동화 (CT 도입)
    +-► 피처 스토어 (훈련/서빙 일관성)
    +-► 모델 레지스트리 (버전 관리)
    +-► 드리프트 모니터링 (데이터/컨셉)
    |
    v
MLOps Level 2 — CI/CD/CT 완전 자동화
    +-► A/B 테스트 · 카나리 배포 · 자동 롤백
    +-► 실험 추적 (MLflow · W&B)
    |
    v
LLMOps — 프롬프트 관리 · RAG 파이프라인 · PEFT 스케줄링
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 258

<- **이전**: [160. 지식 그래프 (Knowledge Graph) + GraphRAG 연동망](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)
**다음**: [162. CT (Continuous Training) 파이프라인 - 모델 성능 저하 시 자동 재학습](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ->

---
