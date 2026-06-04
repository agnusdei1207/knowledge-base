---
title: "174. MLOps (Machine Learning Operations)"
date: "2026-04-17"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 코드, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 모델, 실행 환경, 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 하나의 관리 체계로 묶어 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 개발·배포·재학습·[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링을 반복 가능하게 만드는 운영 아키텍처다.
> 2. **가치**: 오프라인 실험의 높은 정확도를 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질로 연결하려면 재현성, 배포 자동화, 드리프트 감시, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 체계가 함께 있어야 하며, MLOps는 이 "실험실-운영 간 단절"을 줄인다.
> 3. **판단 포인트**: 모든 모델에 최고 수준 자동화를 강요할 필요는 없으며, 비즈니스 임계성·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화 속도·라벨 확보 주기·규제 요구에 따라 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도를 단계적으로 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

MLOps는 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델을 한 번 학습해 배포하는 작업이 아니라, <strong>변하는 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 함께 모델을 계속 운영하는 체계</strong>다. 일반 소프트웨어는 코드가 같으면 동작도 거의 같지만, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)은 같은 코드라도 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 학습했고 어떤 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 만들었는지에 따라 결과가 달라진다. 따라서 배포의 대상이 단순한 애플리케이션 바이너리가 아니라, `코드 + 데이터 스냅샷 + 모델 아티팩트 + 실행 환경`의 조합이 된다.

이 차이 때문에 노트북에서 95% 정확도를 낸 모델이 운영 환경에서는 곧바로 무너질 수 있다. 훈련 때와 다른 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포가 유입되거나, 서빙 전처리가 훈련 전처리와 어긋나거나, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))·[라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 달라 재현이 실패할 수 있기 때문이다. MLOps는 바로 이 불일치를 줄이기 위해 등장했다.

```text
+----------------------------------------------------------------------+
| Why ML needs operations beyond normal deployment                     |
+----------------------------------------------------------------------+
| Software release                                                    |
|   Code change -> build -> test -> deploy                            |
|                                                                      |
| Machine Learning release                                             |
|   Data change + Code change + Feature change + Label delay          |
|        -> train -> evaluate -> register -> deploy -> monitor        |
|        -> retrain / rollback when quality shifts                    |
+----------------------------------------------------------------------+
```

즉 MLOps의 필요성은 "AI를 더 자동화하자"가 아니라, <strong><a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> 시스템이 본질적으로 불안정한 입력 현실을 상대한다</strong>는 데서 나온다. 운영을 설계하지 않으면 좋은 모델도 금방 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)가 된다.

- **📢 섹션 요약 비유**: MLOps는 자동차를 한 번 조립해 전시하는 일이 아니라, 매일 도로 상태와 연료 품질이 달라지는 택시를 계속 점검하고 부품을 갈아 끼우며 운행하는 정비 체계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MLOps의 핵심은 세 가지다. 첫째, **재현성 (Reproducibility)**: 같은 코드와 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)면 같은 모델이 다시 나와야 한다. 둘째, **자동화된 전달 체계**: 실험 결과가 사람 손을 거치며 깨지지 않도록 학습·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·배포를 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 연결해야 한다. 셋째, **폐루프 운영 (Closed Loop Operations)**: 배포 후 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 감지하면 다시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·학습 단계로 돌아갈 수 있어야 한다.

```text
+----------------------------------------------------------------------+
| Reference MLOps loop                                                 |
+----------------------------------------------------------------------+
| Raw Data -> Validation -> Feature Pipeline -> Training -> Evaluation |
|    ^                                                |                |
|    |                                                v                |
| Monitoring <- Serving <- Deployment <- Registry <- Model Artifact    |
|    |                                                                  |
|    +- drift / latency breach / new labels -> retraining trigger      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 없을 때 생기는 문제 |
| :--- | :--- | :--- |
| [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Validation](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), 결측치, [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 잘못된 입력이 학습/서빙에 그대로 유입된다. |
| Feature [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) / [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 훈련-서빙 전처리 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보 | [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew가 발생한다. |
| Experiment Tracking | 파라미터, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기록 | 왜 특정 모델이 좋았는지 재현 불가다. |
| [Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) | 승인된 모델 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)와 상태 관리 | 배포 기준 모델과 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 대상이 모호해진다. |
| Orchestrator | 학습·평가·배포 작업 순서 자동화 | 사람 의존적 수동 운영이 된다. |
| Serving Platform | 온라인 추론 또는 배치 추론 제공 | 운영 환경마다 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·형식이 제각각이 된다. |
| Monitoring | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 에러율, 드리프트, 비즈니스 성과 감시 | 모델이 망가져도 뒤늦게 알게 된다. |

실무에서는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)), [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)), CD ([Continuous Delivery](/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)/[Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))를 구분해 이해하면 좋다. CI는 코드와 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 변경이 기본 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 통과하게 만드는 단계이고, CT는 드리프트·신규 라벨·정기 주기 같은 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 모델을 다시 학습시키는 단계이며, CD는 승인된 모델을 점진적으로 운영에 반영하는 단계다. 특히 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)에서는 <strong>배포 이후의 <a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링이 다시 학습 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인을 호출하는 구조</strong>가 중요하다.

재현성을 위해서는 보통 다음 식의 릴리스 단위를 관리한다.

`Machine Learning Release = Code Version + Data Snapshot + Feature Definition + Model Artifact + Runtime Environment`

이 다섯 요소가 함께 묶여야 "왜 이 모델이 이런 예측을 했는가"를 나중에 설명할 수 있다.

- **📢 섹션 요약 비유**: MLOps는 요리책만 관리하는 주방이 아니라, 재료 입고표, 조리 순서, 완성 사진, 냉장고 온도 기록까지 같이 남기는 식당 운영 시스템과 같다.

---

## Ⅲ. 비교 및 연결

MLOps는 DevOps의 연장선에 있지만, 단순히 "ML [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)"라고 보면 절반만 이해한 것이다. DevOps의 주된 실패 원인이 코드 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)과 배포 오류라면, MLOps의 실패 원인은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 변화, 라벨 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 불일치처럼 <strong>코드 밖에서 발생하는 품질 붕괴</strong>가 훨씬 크다.

| 항목 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) | [LLMOps](/studynote/12_it_management/05_security_compliance/221_llmops_large_language_model_ops/) ([Large Language Model Operations](/studynote/14_data_engineering/04_mlops/174_llmops_prompt_template_rag_pipeline/)) |
| :--- | :--- | :--- | :--- |
| 핵심 산출물 | 애플리케이션 코드/[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) | 코드 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + 모델 | 프롬프트 + 검색기 + 모델 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 단위/[통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) + 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) + 드리프트 | 응답 품질 + grounding + safety |
| 주요 장애 원인 | 버그, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류 | [Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/), [Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/), 전처리 불일치 | [Hallucination](/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/), [prompt injection](/studynote/09_security/19_ai_advanced_security/955_prompt_injection/), retrieval miss |
| [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 기준 | 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 되돌림 | 이전 모델 + 이전 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)/[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기준 복원 | 프롬프트/[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)/검색 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 동시 복원 |
| 운영 핵심 | 빠른 배포 | 재현성 + 지속적 재학습 | 평가 체계 + [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어 + 비용 최적화 |

이 차이는 테스트 방식에도 영향을 준다. 일반 소프트웨어는 기대 출력이 분명한 경우가 많지만, 모델은 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적이어서 오프라인 정확도가 곧 운영 품질을 뜻하지 않는다. 그래서 MLOps는 `accuracy`, `F1 score`, `latency`뿐 아니라 전환율, 이탈률, 오탐 비용 같은 <strong>비즈니스 지표와 연결된 운영 관측</strong>이 필요하다.

또한 MLOps는 [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/), [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/), [피처 스토어](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), A/B 테스트와 긴밀하게 연결된다. 즉 MLOps는 단독 기술이 아니라, <strong>학습 시스템을 운영 가능한 제품으로 바꾸는 묶음 개념</strong>이다.

- **📢 섹션 요약 비유**: DevOps가 제품 공장의 조립 라인을 다루는 일이라면, MLOps는 자라나는 작물 농장을 관리하는 일에 가깝다. 기계는 같은 나사를 끼우면 되지만, 작물은 날씨와 토양이 바뀌면 관리법도 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

좋은 MLOps는 도구를 많이 붙인 시스템이 아니라, <strong>조직이 감당할 수 있는 수준으로 운영 위험을 줄이는 시스템</strong>이다. 모든 프로젝트에 [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/), [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), 자동 재학습을 한꺼번에 도입하면 복잡성만 커질 수 있다. 따라서 성숙도는 단계적으로 올리는 것이 좋다.

| 성숙도 | 특징 | 적합한 상황 | 주의점 |
| :--- | :--- | :--- | :--- |
| Level 0 | 수동 학습, 수동 배포, 기록 최소화 | 연구·개념 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) (PoC, Proof of [Concept](/studynote/14_data_engineering/02_math_mining/120_concept/)) | 재현성과 운영 연속성이 매우 낮다. |
| Level 1 | 실험 추적, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/), 재현 가능한 학습 | 내부 분석, 월 단위 갱신 모델 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/환경 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리는 필수다. |
| Level 2 | 자동 배포, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 고객 대면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기준과 배포 승인 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요하다. |
| Level 3 | 드리프트 기반 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), champion-challenger, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 자동화 | 고가치 실시간 의사결정 | 잘못된 자동 재학습이 오히려 위험할 수 있다. |

### 실무 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 서빙 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 로직이 동일한가?
2. 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 탐지할 운영 지표와 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)가 정의되어 있는가?
3. 신규 모델을 바로 전면 배포하지 않고 shadow/[canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는가?
4. 라벨이 늦게 도착하는 문제를 고려해 온라인 지표와 오프라인 지표를 분리했는가?
5. 규제 산업이라면 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 의사결정을 내렸는지 추적 가능한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 노트북 결과 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 수동으로 운영 서버에 복사하는 배포
- 훈련 정확도만 보고 운영 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용을 보지 않는 평가
- 드리프트 경고가 났다고 무조건 전체 재학습부터 수행하는 대응
- 모델 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)은 준비하지 않고 최신 모델만 남기는 운영
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 라벨 품질을 무시한 채 도구만 도입하는 "[MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 포장"

기술사 관점에서는 "[MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) = ML 자동 배포"라고 축약하면 부족하다. 더 정확한 설명은 <strong>"<a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a>의 실험, 배포, <a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링, 재학습, 추적성을 하나의 생명주기 통제로 엮어 운영 <a href="/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a>를 줄이는 체계"</strong>다. 이 정의 안에 재현성, 드리프트 대응, 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성이 모두 포함된다.

- **📢 섹션 요약 비유**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도입은 작은 화분에 자동 급수 시스템을 바로 붙이는 일이 아니라, 집 화분인지 대형 온실인지에 맞춰 관수 장치를 고르는 일과 같다. 규모와 위험에 맞지 않으면 장치가 오히려 관리 부담이 된다.

---

## Ⅴ. 기대효과 및 결론

MLOps를 제대로 구축하면 모델 개선 주기가 짧아지고, 장애 원인 분석이 쉬워지며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화에 따른 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 더 빨리 발견할 수 있다. 특히 여러 팀이 함께 일하는 조직에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학, 플랫폼, 백엔드, 보안, 거버넌스를 공통 프로세스로 묶어 주는 효과가 크다. 즉 MLOps의 진짜 가치는 "모델을 빨리 올린다"보다 <strong>모델을 계속 믿고 운영할 수 있게 만든다</strong>는 데 있다.

다만 고성숙도 MLOps는 비용과 복잡성을 수반한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리, 라벨링 체계, 배포 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 부실하면 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인만 자동화해도 품질은 좋아지지 않는다. 따라서 기억해야 할 관점은 MLOps를 도구 목록으로 외우는 것이 아니라, <strong>변하는 현실 속에서 모델의 수명주기를 통제하는 운영 설계</strong>로 이해하는 것이다.

- **📢 섹션 요약 비유**: MLOps는 좋은 운동화를 한 번 사는 일이 아니라, 매일 발 상태를 보며 끈을 조이고 밑창을 교체해 오래 달릴 수 있게 만드는 러닝 관리법과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 변화가 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)가 되는 대표 원인이다. |
| [Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) | 단순 재학습으로 해결되지 않을 수 있는 더 근본적 변화다. |
| [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 훈련-서빙 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장하는 핵심 인프라다. |
| [Model Registry](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) | 승인 모델의 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 상태, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 기준을 관리한다. |
| Shadow / [Canary Deployment](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) | 새 모델을 점진적으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. |
| [LLMOps](/studynote/12_it_management/05_security_compliance/221_llmops_large_language_model_ops/) | [대규모 언어 모델](/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/) 환경에서 MLOps가 확장된 운영 형태다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Notebook experiment
    |
    v
Reproducible training
    |
    v
Experiment tracking + model registry
    |
    v
CI / CD for ML pipelines
    |
    v
Monitoring + drift detection
    |
    v
CT (Continuous Training) + safe rollout
    |
    v
LLMOps / governed AI operations
```

이 흐름은 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)이 개인 실험에서 출발해, 배포 자동화와 [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)을 거쳐 조직 차원의 운영 체계로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MLOps는 똑똑한 로봇을 한 번 만드는 게 아니라, 로봇이 매일 잘 배우고 잘 일하는지 계속 돌봐주는 관리 방법이에요.
2. 로봇이 이상한 음식을 먹거나 낯선 길을 만나면 실수할 수 있어서, 누가 보고 있다가 다시 연습도 시켜 줘야 해요.
3. 그래서 MLOps는 로봇 공장, 검사실, 수리실을 한 줄로 연결해 놓은 시스템이라고 생각하면 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 174 / 420

<- **이전**: [173. A3C (Asynchronous Advantage Actor-Critic) 및 PPO (Proximal Policy Optimization)](/studynote/10_ai/02_dl_architecture_new/173_a3c_ppo/)
**다음**: [175. 데이터 드리프트 (Data Drift)](/studynote/10_ai/02_dl_architecture_new/175_data_drift/) ->

---
