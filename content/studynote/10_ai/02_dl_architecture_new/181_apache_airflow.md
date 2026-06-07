---
title: "Apache Airflow"
date: "2026-05-06"
tags:
  - "studynote-ai"
weight: 181
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [아파치 에어플로우](/studynote/13_cloud_architecture/05_data_engineering/233_apache_airflow_dag_orchestration/) ([Apache Airflow](/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리, 배치 학습, 리포트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)처럼 순서와 의존성이 있는 작업을 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/))로 정의해 실행·재시도·관찰하게 만드는 워크플로 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 플랫폼이다.
> 2. **가치**: 단순 시간 예약 도구인 Cron이 놓치기 쉬운 의존성, 실패 추적, 백필 (Backfill), 재시도, 실행 이력을 Airflow가 표준화해 주므로 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 운영 가능성과 재현성이 크게 올라간다.
> 3. **판단 포인트**: Airflow는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직접 대규모 처리하는 엔진이 아니라 작업 순서를 조율하는 제어 평면이므로, 무거운 연산은 Spark·[BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)·DBT·Ray 같은 외부 실행기로 넘기고 Airflow는 상태 관리와 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)에 집중시켜야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)은 "몇 시에 돌리느냐"보다 "무엇이 끝난 뒤 무엇이 시작되느냐"가 더 중요하다. 예를 들어 새벽 배치에서는 원천 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재, [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 정제, [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 모델 재학습, 결과 배포가 정해진 순서로 이어져야 한다. 이 흐름 중 하나라도 실패하면 뒤 단계는 멈추거나 다시 계산해야 한다.

단순한 Cron은 시간 기반 예약에는 강하지만 의존성, 실패 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 실행 이력 관리에는 약하다. 스크립트가 중간에 실패해도 뒤 작업이 그냥 시작되거나, 어느 날 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 비어 있었는지 추적하기 어렵고, 과거 날짜를 다시 계산하는 백필도 번거롭다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀이 커질수록 이런 문제는 "스크립트 몇 개"의 수준을 넘어 운영 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 된다.

Airflow는 이 문제를 DAG라는 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 바꿔 해결한다. 작업([Task](/studynote/02_operating_system/02_process_thread/150_task/))을 노드로, 선행 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 에지로 표현하면 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 단순 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 모음이 아니라 "[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)"이 된다. 그래서 Airflow의 필요성은 멋진 UI가 아니라, <strong>배치와 <a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인을 반복 가능하고 관찰 가능한 운영 자산으로 만드는 데</strong> 있다.

- **📢 섹션 요약 비유**: Airflow는 알람시계가 아니라 공연 무대 감독과 같다. 배우가 준비되지 않았는데 다음 장면을 시작시키지 않고, 누가 늦었는지와 어디서 다시 시작해야 하는지를 끝까지 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Airflow의 핵심 구성은 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 코드, Scheduler, [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) [Database](/studynote/05_database/04_transactions_concurrency/501_database/), Executor, Worker, Web UI다. 개발자는 Python으로 DAG를 정의하고, Scheduler는 이를 해석해 어떤 [Task](/studynote/02_operating_system/02_process_thread/150_task/) Instance를 언제 큐에 넣을지 판단한다. Executor는 LocalExecutor, CeleryExecutor, KubernetesExecutor 같은 방식으로 실제 실행 자원에 작업을 배분하고, [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) Database는 실행 이력과 상태를 저장한다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | 작업 의존성과 일정 정의 | 순환이 없어야 하며, 지나친 동적 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 운영성을 해침 |
| Scheduler | 실행 시점과 선행 조건 판단 | [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 파싱 부하와 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 관리 필요 |
| [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) [Database](/studynote/05_database/04_transactions_concurrency/501_database/) | 상태·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 포인터·이력 저장 | 병목이 되기 쉬워 운영 DB 품질이 중요 |
| Executor | 작업 분배 방식 결정 | 규모에 따라 Local, Celery, [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 선택 |
| Worker / [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) | 실제 [Task](/studynote/02_operating_system/02_process_thread/150_task/) 실행 | 연산은 외부 [시스템 호출](/studynote/02_operating_system/01_overview_architecture/013_system_call/) 중심으로 유지하는 것이 안전 |
| XCom | [Task](/studynote/02_operating_system/02_process_thread/150_task/) 간 소량 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 전달 | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 통로로 쓰면 안 됨 |

아래 그림은 Airflow가 "작업을 직접 처리하는 엔진"이 아니라 "상태와 순서를 제어하는 플랫폼"이라는 점을 보여 준다.

```text
+----------------------------------------------------------------------+
| Apache Airflow control plane                                        |
+----------------------------------------------------------------------+
| DAG code (.py)                                                      |
|    | parse                                                          |
|    v                                                                |
| Scheduler <-> Metadata DB <-> Web UI                               |
|    | create task instances                                          |
|    v                                                                |
| Executor (Local / Celery / Kubernetes)                              |
|    | dispatch                                                       |
|    +- SQL task                                                      |
|    +- Spark submit                                                  |
|    +- Python / Bash task                                            |
|    v                                                                |
| Worker / Pod -> log + state -> queued / running / success / retry   |
+----------------------------------------------------------------------+
```

Airflow의 중요한 원리는 세 가지다. 첫째, DAG가 있으므로 선행 작업이 완료되어야 후행 작업이 실행된다. 둘째, 실패한 작업은 재시도 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 알림 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 따라 통제된다. 셋째, 실행 날짜(Logical Date)와 백필 개념 덕분에 "오늘 못 돌린 어제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"를 다시 계산할 수 있다.

따라서 좋은 Airflow 설계는 Task를 작게 쪼개되, 각 Task가 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/))을 가져야 한다. 같은 날짜 작업을 두 번 실행해도 결과가 누적 오염되지 않아야 재시도와 백필이 안전해진다. 또한 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체는 저장소나 처리 엔진에 맡기고, Airflow는 명령 발행과 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)에 머물러야 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 플랫폼으로서 안정적이다.

- **📢 섹션 요약 비유**: Airflow는 공사 현장에서 삽질을 직접 하는 인부가 아니라, 어떤 장비를 언제 투입하고 어디서 다시 작업할지 지휘하는 현장 소장과 같다.

---

## Ⅲ. 비교 및 연결

Airflow는 다른 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 도구와 경쟁하기보다 역할을 나눠 쓰는 경우가 많다. 특히 [Cron](/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/), [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/), Prefect와의 차이를 구분해 두면 도입 판단이 쉬워진다.

| 도구 | 중심 역할 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| [Cron](/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/) | 시간 기반 단순 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) | 가볍고 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 단순 | 의존성, 이력, 재시도, 백필이 약함 |
| [Apache Airflow](/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | 범용 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | 이종 시스템 연결, UI, 재시도, 백필, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 | 저지연 이벤트 처리에는 부적합 |
| [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | 실험 추적·모델 관리 | 파라미터·[메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 기록 | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 순서 제어는 약함 |
| [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) Pipelines | [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반 ML [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 모델 학습·서빙과의 연계, 자원 격리 | 범용 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 운영에는 과하거나 복잡할 수 있음 |
| Prefect | 현대적 Python [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | 유연한 동적 흐름, 개발 경험 우수 | Airflow만큼 넓은 생태계는 아님 |

실무에서는 Airflow와 MLflow를 함께 쓰는 구성이 흔하다. Airflow는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집->전처리->학습 호출을 관리하고, 학습 코드 내부에서는 MLflow가 파라미터와 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 기록하는 식이다. 즉 Airflow가 "언제 무엇을 돌릴지"를 맡고, MLflow가 "무엇이 가장 좋은 결과였는지"를 기록한다.

또한 Airflow는 스트리밍 엔진과도 구분해야 한다. [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), Flink, Spark Structured Streaming은 실시간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리에 가깝고, Airflow는 분·시간·일 단위의 배치 제어에 더 적합하다. 배치 제어와 실시간 처리를 한 도구로 모두 해결하려 하면 아키텍처가 흔들린다.

- **📢 섹션 요약 비유**: Cron이 벽시계라면 Airflow는 공장 일정실이고, MLflow는 실험 기록실이며, Kubeflow는 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 전용 생산 라인에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

Airflow를 도입할 때 가장 먼저 판단할 것은 "의존성이 있는 반복 작업인가"다. 매일 혹은 매시간 같은 절차가 반복되고, 실패 시 어느 단계부터 재실행해야 하며, 누가 언제 어떤 결과를 냈는지 추적해야 한다면 Airflow가 적합하다. 반대로 단순한 단일 스크립트나 초저지연 이벤트 처리에는 과할 수 있다.

| 실무 판단 항목 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 다단계 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) / [ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 도입 적합 | 의존성, 백필, 재시도, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 가치가 큼 |
| 모델 재학습 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링 | 도입 적합 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비와 학습 단계를 연결하기 좋음 |
| 초당 이벤트 처리 | 별도 스트리밍 도구 우선 | Scheduler 기반 구조라 초저지연에 부적합 |
| [Task](/studynote/02_operating_system/02_process_thread/150_task/) 내부 대용량 연산 | 외부 엔진 위임 | Airflow Worker 안정성 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 필요 |

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Task가 재시도와 백필에 견딜 수 있도록 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 있게 설계되었는가?
2. 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 XCom이 아니라 객체 저장소, [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 등 외부 저장소로 주고받는가?
3. Executor 선택이 현재 규모와 맞는가? 소규모는 Local, 팀 단위 운영은 Celery, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 확장은 Kubernetes가 일반적이다.
4. [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수와 파싱 비용을 고려해 Scheduler 부하를 측정하고 있는가?
5. Secrets, 연결 정보, 알림 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) ([Service Level Agreement](/studynote/12_it_management/02_itsm_itil/869_sla/)) 경고를 표준화했는가?

### 자주 발생하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- `PythonOperator` 안에 대용량 Pandas 처리를 넣어 워커 메모리를 소진시키는 구조
- 하나의 거대한 DAG에 모든 업무를 몰아 넣어 실패 지점을 찾기 어려운 설계
- [Task](/studynote/02_operating_system/02_process_thread/150_task/) 간 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 XCom으로 전달하는 오용
- 로컬 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로에 의존해 개발 환경에서는 되지만 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 실행에서 깨지는 배포
- Catchup과 Backfill 개념을 이해하지 못해 과거 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)이 대량으로 밀려 실행되는 사고

기술사 답안에서는 <strong>"Airflow는 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 및 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 배치 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인의 제어 평면으로서 <a href="/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a> 기반 의존성 관리, 재시도, 백필, 실행 이력 관리를 제공하며, 실제 대용량 연산은 외부 처리 엔진으로 분리하는 것이 핵심 설계 원칙"</strong>이라고 정리하면 된다.

- **📢 섹션 요약 비유**: Airflow를 잘 쓰는 팀은 무대 뒤에서 조명·음향·배우 순서를 정확히 맞추는 공연팀과 같고, 못 쓰는 팀은 감독에게 직접 무대 장치까지 들게 만드는 셈이다.

---

## Ⅴ. 기대효과 및 결론

Airflow를 도입하면 배치 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 "누가 알음알음 돌리던 스크립트"에서 "조직이 관리하는 운영 자산"으로 바뀐다. 실행 이력, 실패 지점, 재시도, 백필, 알림이 표준화되므로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제와 운영 공백을 더 빨리 발견할 수 있다. 특히 여러 시스템을 엮는 ETL과 모델 재학습 환경에서는 이 효과가 크다.

다만 Airflow는 도입만으로 품질이 보장되는 도구는 아니다. DAG가 무분별하게 늘어나거나, 워커가 처리 엔진 역할까지 떠맡거나, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 병목이 되면 오히려 새로운 운영 문제를 만든다. 그래서 Airflow는 "자동화 도구"라기보다 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a> 규율을 강제하는 플랫폼</strong>으로 보는 편이 정확하다.

결론적으로 Airflow는 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 계산 능력이 아니라 통제 능력을 높이는 도구다. 무엇을 언제 어떤 순서로 실행하고, 실패하면 어떻게 다시 돌릴지 명확히 설명할 수 있을 때 Airflow의 진짜 가치가 드러난다.

- **📢 섹션 요약 비유**: Airflow는 공항의 관제탑과 같다. 관제탑이 비행기를 직접 날리지는 않지만, 이착륙 순서를 잘못 잡으면 공항 전체가 멈춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)) | Airflow가 작업 의존성을 표현하는 핵심 구조다. |
| Scheduler | 실행 시점과 선행 조건을 계산하는 제어 핵심이다. |
| Executor | 작업을 어떤 실행 자원에 분배할지 결정한다. |
| XCom | [Task](/studynote/02_operating_system/02_process_thread/150_task/) 간 소량 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 전달 수단이지 대용량 [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)가 아니다. |
| Backfill / Catchup | 과거 시점 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 재실행하는 운영 기능으로 배치 품질 관리와 직결된다. |
| [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | Airflow와 결합해 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 실행과 실험 추적을 분리하는 대표 도구다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Cron 기반 단일 스크립트
    |
    v
DAG 기반 의존성 관리
    |
    +- retry / alert / SLA
    +- logical date / backfill
    +- metadata-driven observability
    |
    v
분산 Executor와 외부 처리 엔진 연동
    |
    v
ETL + MLOps 파이프라인 오케스트레이션
```

이 흐름은 Airflow가 단순 예약에서 출발해, 실행 상태와 재현성을 포함한 운영 플랫폼으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow는 공장에서 어떤 기계를 먼저 돌리고 다음에 무엇을 할지 순서를 정해 주는 반장님이에요.
2. 기계 하나가 고장 나면 뒤 기계들을 잠깐 멈추고, 고친 뒤 그 자리부터 다시 시작하게 해 줘요.
3. 반장님은 무거운 짐을 직접 나르지 않고, 누가 언제 일할지만 똑똑하게 지시해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 181 / 420

<- **이전**: [180. MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)
**다음**: [182. 분산 처리 컴퓨팅 AI 훈련 인프라 (Apache Spark, Ray)](/studynote/10_ai/02_dl_architecture_new/182_spark_ray_distributed/) ->

---
