---
title: "321. MLOps (Machine Learning Operations)"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 321
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 ML (Machine [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 모델의 개발(Development)·배포([Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))·운영(Operations) 전 주기를 자동화·표준화하는 엔지니어링 철학으로, [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 원칙을 ML 시스템에 적용하여 모델이 지속적으로 학습·배포·[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링되는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 구축한다.
> 2. **가치**: 연구소 실험 단계 모델이 실제 프로덕션 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 안정적으로 전환되지 못하는 "ML 프로젝트의 87% 배포 실패"라는 실무 문제를 해결하여, 모델 개발 사이클을 단축하고 운영 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 확보한다.
> 3. **판단 포인트**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도 레벨(Level 0: 수동, Level 1: 자동화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인, Level 2: [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD)에 따라 조직의 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 생산성이 결정되며, [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 감지와 자동 재학습이 Level 2의 핵심 구성 요소다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 정확도 95%의 고객 이탈 예측 모델을 개발했다. 하지만 이 모델을 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 서버에 배포하고 6개월 후 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링하는 전 과정을 수동으로 하면, 다음 문제가 발생한다:
- 모델 코드가 서버 환경과 다른 Python [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 실행 오류
- 6개월 후 고객 행동 패턴 변화로 정확도 70%로 하락 ([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))
- 어떤 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 프로덕션에 있는지 추적 불가 ([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 부재)

<strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a></strong>는 DevOps의 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD([지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포), [인프라 코드](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)화, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 원칙을 ML 시스템에 적용해 이 문제를 해결한다. 모델 학습에서 서빙까지 전 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 자동화되고 추적 가능하게 된다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 없는 ML 배포는 레스토랑 주방에서 셰프가 매번 손으로 모든 레시피를 처음부터 조리하는 것이다. 메뉴가 조금 바뀌면([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) 모든 조리법을 수동으로 다시 설계해야 한다. MLOps는 자동화된 식품 공장 라인처럼, 재료가 들어오면 자동으로 가공·품질검사·포장·배송되는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|         MLOps 성숙도 레벨 및 자동화 파이프라인 구조                   |
+------------------------------------------------------------------+
|                                                                  |
|  Level 0: 수동 ML (Script-Based)                                 |
|  데이터 준비 -> 실험 (Jupyter) -> 수동 배포 -> 수동 모니터링            |
|  문제: 재현 불가, 버전 관리 없음, 확장 불가                          |
|                                                                  |
|  Level 1: 자동화 ML 파이프라인                                     |
|  +----------------------------------------------------------+   |
|  | 데이터 파이프라인   특징 엔지니어링   모델 학습   모델 평가   |   |
|  |       |                  |              |           |     |   |
|  |    자동화 ------------------------------------------     |   |
|  +----------------------------------------------------------+   |
|  + 피처 스토어, 모델 레지스트리                                      |
|                                                                  |
|  Level 2: CI/CD ML 시스템 (완전 자동화)                            |
|  +----------------------------------------------------------+   |
|  | 데이터 트리거 -> 자동 파이프라인 실행 -> 모델 검증 -> 자동 배포  |   |
|  |       ^                                        |         |   |
|  | 모니터링 <--- 드리프트 감지 <--------- 서빙 모니터링          |   |
|  +----------------------------------------------------------+   |
|  자동 재학습(CT: Continuous Training) + CD: 지속적 배포            |
+------------------------------------------------------------------+
```

| [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 핵심 구성 요소 | 역할 | 대표 도구 |
|:---|:---|:---|
| 실험 추적 (Experiment Tracking) | 파라미터·[메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 기록 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), Weights & Biases |
| [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)) | 특징 공유·재사용·[캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) | Feast, Tecton, Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ([Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)) | 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·상태 관리 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), AWS SageMaker |
| [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | 워크플로우 자동화 | [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/), Airflow, Argo |
| 서빙 인프라 | 모델 추론 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | BentoML, Triton, TorchServe |
| [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 드리프트·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 감시 | Evidently, WhyLogs |

- **📢 섹션 요약 비유**: [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) 실험 추적은 요리 경연대회 심사 일지다. 참가자(모델)별로 레시피(하이퍼파라미터), 재료 원산지([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)), 심사 점수(평가 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)), 최종 요리 사진(모델 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/))을 모두 기록한다. 나중에 "어느 레시피가 제일 맛있었나?"를 바로 찾아볼 수 있다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/">DevOps</a> vs MLOps의 차이</strong>:
| 항목 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) |
|:---|:---|:---|
| [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) | 코드(소프트웨어) | 코드 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + 모델 |
| 테스트 | 유닛/[통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) + 모델 [성능 테스트](/studynote/04_software_engineering/11_testing_validation/837_performance_test_types/) |
| 배포 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | 코드 커밋 | 코드 커밋 + 새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + 드리프트 감지 |
| [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 시스템 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) (CPU, 에러율) | 시스템 + [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) + 모델 정확도 |

- **📢 섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) = [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) + "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라는 생물체 관리". 소프트웨어(코드)는 한 번 작성하면 변하지 않지만, ML 모델의 입력([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 세상이 바뀌면 함께 변한다. DevOps는 공장 기계 유지보수, MLOps는 공장 기계 + 원재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 품질 변화까지 감시하는 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> 플랫폼 선택 기준</strong>:
1. **클라우드 의존**: AWS SageMaker, GCP Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), Azure ML -> 완전 관리형, 높은 비용
2. <strong><a href="/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 자체 구축</strong>: [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) + [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) + Airflow -> 유연성, 구축·운영 부담
3. <strong><a href="/studynote/12_it_management/05_security_compliance/951_saas/">SaaS</a> 하이브리드</strong>: Weights & Biases + Feast + BentoML 조합

<strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> 도입 <a href="/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a> (투자 대비 수익)</strong>:
- 모델 배포 주기: 월 1회 -> 일 1회로 단축
- 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 탐지: 수동 발견(수주) -> 자동 감지(시간 내)
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자 생산성: 비기술 인프라 작업 70% 감소

- **📢 섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입 ROI는 세탁기 구입 효과와 같다. 손빨래(수동 ML)는 매번 시간과 노력이 크지만, 세탁기([MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 자동화) 구입 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용 후에는 훨씬 적은 노력으로 더 자주, 더 깨끗하게 처리할 수 있다. 세탁기(자동화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인)가 있어야만 대규모 세탁(다수 ML 모델 운영)이 가능하다.

---

## Ⅴ. 기대효과 및 결론

MLOps는 AI를 실험실에서 세상으로 꺼내는 다리다. 아무리 뛰어난 모델도 안정적으로 배포·운영되지 않으면 아무 가치가 없다. [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) Level 2의 완전 자동화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어오면 모델이 자동으로 재학습되고, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되면 자동으로 프로덕션에 배포되는 "살아있는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템"을 구현한다. 이 역량이 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 프로젝트의 [지속 가능성](/studynote/04_software_engineering/06_software_architecture/386_sustainability_green_coding/)과 비즈니스 가치를 결정한다.

- **📢 섹션 요약 비유**: MLOps가 없는 AI는 레이싱카만 있고 정비소가 없는 것이다. 처음 레이스([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 배포)는 잘 달리지만 몇 바퀴 후(시간 경과) 타이어가 닳고([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) 엔진이 과열(시스템 오류)되어도 수리할 체계가 없다. MLOps는 모든 레이스에서 최고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하는 자동화된 피트 스톱 팀이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | 분포 변화, 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 / [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링의 핵심 감시 대상 |
| [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 특징 공유, 재사용 / [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이어 |
| [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) | [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, 배포 상태 / MLOps의 모델 관리 중앙 저장소 |
| [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | [지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포, 자동화 / MLOps의 소프트웨어 엔지니어링 기반 |
| [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) | [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/), ML [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 / 대표적 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 플랫폼 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [MLOps (Machine Learning Operations)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a></strong>는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 만들고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 올리고, 잘 작동하는지 감시하는 **전 과정을 자동으로** 처리하는 시스템이에요!
2. "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 -> 모델 학습 -> 배포 -> [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 -> 다시 학습" 사이클을 사람 손 없이 **컨베이어 벨트처럼 자동으로** 돌아가게 해요.
3. AI를 연구실에서 <strong>실제 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>로 안정적으로 이전</strong>하는 데 반드시 필요한, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 엔지니어의 필수 기술이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 321 / 420

<- **이전**: [320. 디퓨전 모델 (Diffusion Model)](/studynote/10_ai/04_ai_ops_ethics/320_diffusion_model/)
**다음**: [322. 데이터 드리프트 (Data Drift) / 컨셉 드리프트 (Concept Drift)](/studynote/10_ai/04_ai_ops_ethics/322_data_concept_drift/) ->

---
