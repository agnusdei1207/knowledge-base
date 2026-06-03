---
title: 181. 데이터 파이프라인 전처리 (Apache Airflow)
date: '2026-05-06'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[233_apache_airflow_dag_orchestration|아파치 에어플로우]] ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]])는 [[001_dikw_pyramid|데이터]] 전처리, 배치 학습, 리포트 [[087_process_state_transition|생성]]처럼 순서와 의존성이 있는 작업을 [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]])로 정의해 실행·재시도·관찰하게 만드는 워크플로 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼이다.
> 2. **가치**: 단순 시간 예약 도구인 Cron이 놓치기 쉬운 의존성, 실패 추적, 백필 (Backfill), 재시도, 실행 이력을 Airflow가 표준화해 주므로 [[645_data_pipeline_acceleration|데이터 파이프라인]]의 운영 가능성과 재현성이 크게 올라간다.
> 3. **판단 포인트**: Airflow는 [[001_dikw_pyramid|데이터]]를 직접 대규모 처리하는 엔진이 아니라 작업 순서를 조율하는 제어 평면이므로, 무거운 연산은 Spark·[[263_storage_compute_separation_bigquery|BigQuery]]·DBT·Ray 같은 외부 실행기로 넘기고 Airflow는 상태 관리와 [[073_container_orchestration_tools|오케스트레이션]]에 집중시켜야 한다.

---

## Ⅰ. 개요 및 필요성

[[645_data_pipeline_acceleration|데이터 파이프라인]]은 "몇 시에 돌리느냐"보다 "무엇이 끝난 뒤 무엇이 시작되느냐"가 더 중요하다. 예를 들어 새벽 배치에서는 원천 [[001_dikw_pyramid|데이터]] 적재, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 정제, [[247_feature_label_variables|피처]] [[087_process_state_transition|생성]], 모델 재학습, 결과 배포가 정해진 순서로 이어져야 한다. 이 흐름 중 하나라도 실패하면 뒤 단계는 멈추거나 다시 계산해야 한다.

단순한 Cron은 시간 기반 예약에는 강하지만 의존성, 실패 [[658_ir_recovery|복구]], 실행 이력 관리에는 약하다. 스크립트가 중간에 실패해도 뒤 작업이 그냥 시작되거나, 어느 날 [[001_dikw_pyramid|데이터]]가 비어 있었는지 추적하기 어렵고, 과거 날짜를 다시 계산하는 백필도 번거롭다. [[001_dikw_pyramid|데이터]] 팀이 커질수록 이런 문제는 "스크립트 몇 개"의 수준을 넘어 운영 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 된다.

Airflow는 이 문제를 DAG라는 [[070_graph_datastructure|그래프]]로 바꿔 해결한다. 작업([[150_task|Task]])을 노드로, 선행 [[083_relationship_in_er_model|관계]]를 에지로 표현하면 [[123_pipe|파이프]]라인이 단순 [[208_schedule_history_transaction_execution_order|스케줄]] 모음이 아니라 "[[395_verification_process_review|검증]] 가능한 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]"이 된다. 그래서 Airflow의 필요성은 멋진 UI가 아니라, **배치와 [[241_machine_learning_basics|머신러닝]] [[123_pipe|파이프]]라인을 반복 가능하고 관찰 가능한 운영 자산으로 만드는 데** 있다.

- **📢 섹션 요약 비유**: Airflow는 알람시계가 아니라 공연 무대 감독과 같다. 배우가 준비되지 않았는데 다음 장면을 시작시키지 않고, 누가 늦었는지와 어디서 다시 시작해야 하는지를 끝까지 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Airflow의 핵심 구성은 [[401_bayesian_network_dag_causality|DAG]] 코드, Scheduler, [[012_metadata|Metadata]] [[501_database|Database]], Executor, Worker, Web UI다. 개발자는 Python으로 DAG를 정의하고, Scheduler는 이를 해석해 어떤 [[150_task|Task]] Instance를 언제 큐에 넣을지 판단한다. Executor는 LocalExecutor, CeleryExecutor, KubernetesExecutor 같은 방식으로 실제 실행 자원에 작업을 배분하고, [[012_metadata|Metadata]] Database는 실행 이력과 상태를 저장한다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| [[401_bayesian_network_dag_causality|DAG]] | 작업 의존성과 일정 정의 | 순환이 없어야 하며, 지나친 동적 [[087_process_state_transition|생성]]은 운영성을 해침 |
| Scheduler | 실행 시점과 선행 조건 판단 | [[401_bayesian_network_dag_causality|DAG]] 파싱 부하와 [[208_schedule_history_transaction_execution_order|스케줄]] [[015_지연_데이터_관점|지연]] 관리 필요 |
| [[012_metadata|Metadata]] [[501_database|Database]] | 상태·[[568_logs_distributed_logging_elk_fluentd|로그]] 포인터·이력 저장 | 병목이 되기 쉬워 운영 DB 품질이 중요 |
| Executor | 작업 분배 방식 결정 | 규모에 따라 Local, Celery, [[205_kubernetes_container_orchestration|Kubernetes]] 선택 |
| Worker / [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 실제 [[150_task|Task]] 실행 | 연산은 외부 [[013_system_call|시스템 호출]] 중심으로 유지하는 것이 안전 |
| XCom | [[150_task|Task]] 간 소량 [[012_metadata|메타데이터]] 전달 | 대용량 [[001_dikw_pyramid|데이터]] 전달 통로로 쓰면 안 됨 |

아래 그림은 Airflow가 "작업을 직접 처리하는 엔진"이 아니라 "상태와 순서를 제어하는 플랫폼"이라는 점을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Apache Airflow control plane                                        │
├──────────────────────────────────────────────────────────────────────┤
│ DAG code (.py)                                                      │
│    │ parse                                                          │
│    ▼                                                                │
│ Scheduler <-> Metadata DB <-> Web UI                               │
│    │ create task instances                                          │
│    ▼                                                                │
│ Executor (Local / Celery / Kubernetes)                              │
│    │ dispatch                                                       │
│    ├─ SQL task                                                      │
│    ├─ Spark submit                                                  │
│    └─ Python / Bash task                                            │
│    ▼                                                                │
│ Worker / Pod -> log + state -> queued / running / success / retry   │
└──────────────────────────────────────────────────────────────────────┘
```

Airflow의 중요한 원리는 세 가지다. 첫째, DAG가 있으므로 선행 작업이 완료되어야 후행 작업이 실행된다. 둘째, 실패한 작업은 재시도 [[164_policy|정책]]과 알림 [[164_policy|정책]]에 따라 통제된다. 셋째, 실행 날짜(Logical Date)와 백필 개념 덕분에 "오늘 못 돌린 어제 [[001_dikw_pyramid|데이터]]"를 다시 계산할 수 있다.

따라서 좋은 Airflow 설계는 Task를 작게 쪼개되, 각 Task가 [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]])을 가져야 한다. 같은 날짜 작업을 두 번 실행해도 결과가 누적 오염되지 않아야 재시도와 백필이 안전해진다. 또한 대용량 [[001_dikw_pyramid|데이터]] 자체는 저장소나 처리 엔진에 맡기고, Airflow는 명령 발행과 상태 [[396_validation|확인]]에 머물러야 [[012_metadata|메타데이터]] 플랫폼으로서 안정적이다.

- **📢 섹션 요약 비유**: Airflow는 공사 현장에서 삽질을 직접 하는 인부가 아니라, 어떤 장비를 언제 투입하고 어디서 다시 작업할지 지휘하는 현장 소장과 같다.

---

## Ⅲ. 비교 및 연결

Airflow는 다른 [[001_dikw_pyramid|데이터]]·[[348_mlops|MLOps]] 도구와 경쟁하기보다 역할을 나눠 쓰는 경우가 많다. 특히 [[107_nightly_build_scheduled_cron_pipeline|Cron]], [[180_mlflow|MLflow]], [[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]], Prefect와의 차이를 구분해 두면 도입 판단이 쉬워진다.

| 도구 | 중심 역할 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| [[107_nightly_build_scheduled_cron_pipeline|Cron]] | 시간 기반 단순 [[208_schedule_history_transaction_execution_order|스케줄]] | 가볍고 [[009_config|설정]]이 단순 | 의존성, 이력, 재시도, 백필이 약함 |
| [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | 범용 [[401_bayesian_network_dag_causality|DAG]] [[073_container_orchestration_tools|오케스트레이션]] | 이종 시스템 연결, UI, 재시도, 백필, [[606_auditing_linux_auditd|감사]] 추적 | 저지연 이벤트 처리에는 부적합 |
| [[180_mlflow|MLflow]] | 실험 추적·모델 관리 | 파라미터·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·모델 [[288_version_ihl_tos_total_length|버전]] 기록 | [[123_pipe|파이프]]라인 순서 제어는 약함 |
| [[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]] Pipelines | [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 기반 ML [[123_pipe|파이프]]라인 | 모델 학습·서빙과의 연계, 자원 격리 | 범용 [[215_etl_vs_elt_pipeline|ETL]] 운영에는 과하거나 복잡할 수 있음 |
| Prefect | 현대적 Python [[073_container_orchestration_tools|오케스트레이션]] | 유연한 동적 흐름, 개발 경험 우수 | Airflow만큼 넓은 생태계는 아님 |

실무에서는 Airflow와 MLflow를 함께 쓰는 구성이 흔하다. Airflow는 [[001_dikw_pyramid|데이터]] 수집→전처리→학습 호출을 관리하고, 학습 코드 내부에서는 MLflow가 파라미터와 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 기록하는 식이다. 즉 Airflow가 "언제 무엇을 돌릴지"를 맡고, MLflow가 "무엇이 가장 좋은 결과였는지"를 기록한다.

또한 Airflow는 스트리밍 엔진과도 구분해야 한다. [[179_kafka_flink_watermark_time_window|Kafka]], Flink, Spark Structured Streaming은 실시간 [[001_dikw_pyramid|데이터]] 처리에 가깝고, Airflow는 분·시간·일 단위의 배치 제어에 더 적합하다. 배치 제어와 실시간 처리를 한 도구로 모두 해결하려 하면 아키텍처가 흔들린다.

- **📢 섹션 요약 비유**: Cron이 벽시계라면 Airflow는 공장 일정실이고, MLflow는 실험 기록실이며, Kubeflow는 [[241_machine_learning_basics|머신러닝]] 전용 생산 라인에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

Airflow를 도입할 때 가장 먼저 판단할 것은 "의존성이 있는 반복 작업인가"다. 매일 혹은 매시간 같은 절차가 반복되고, 실패 시 어느 단계부터 재실행해야 하며, 누가 언제 어떤 결과를 냈는지 추적해야 한다면 Airflow가 적합하다. 반대로 단순한 단일 스크립트나 초저지연 이벤트 처리에는 과할 수 있다.

| 실무 판단 항목 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 다단계 [[215_etl_vs_elt_pipeline|ETL]] / [[034_elt|ELT]] [[123_pipe|파이프]]라인 | 도입 적합 | 의존성, 백필, 재시도, [[229_monitor|모니터]]링 가치가 큼 |
| 모델 재학습 [[208_schedule_history_transaction_execution_order|스케줄]]링 | 도입 적합 | [[001_dikw_pyramid|데이터]] 준비와 학습 단계를 연결하기 좋음 |
| 초당 이벤트 처리 | 별도 스트리밍 도구 우선 | Scheduler 기반 구조라 초저지연에 부적합 |
| [[150_task|Task]] 내부 대용량 연산 | 외부 엔진 위임 | Airflow Worker 안정성 [[571_protection_vs_security|보호]] 필요 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. Task가 재시도와 백필에 견딜 수 있도록 [[171_idempotency_iac_terraform|멱등성]] 있게 설계되었는가?
2. 대용량 [[001_dikw_pyramid|데이터]]는 XCom이 아니라 객체 저장소, [[209_data_warehouse_schema_on_write|데이터 웨어하우스]], [[389_mesh_topology|메시]]지 큐 등 외부 저장소로 주고받는가?
3. Executor 선택이 현재 규모와 맞는가? 소규모는 Local, 팀 단위 운영은 Celery, [[561_container_based_deployment|컨테이너]] 확장은 Kubernetes가 일반적이다.
4. [[401_bayesian_network_dag_causality|DAG]] [[501_file_definition_logical_record|파일]] 수와 파싱 비용을 고려해 Scheduler 부하를 측정하고 있는가?
5. Secrets, 연결 정보, 알림 [[164_policy|정책]], [[085_sla|SLA]] ([[085_sla|Service Level Agreement]]) 경고를 표준화했는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- `PythonOperator` 안에 대용량 Pandas 처리를 넣어 워커 메모리를 소진시키는 구조
- 하나의 거대한 DAG에 모든 업무를 몰아 넣어 실패 지점을 찾기 어려운 설계
- [[150_task|Task]] 간 대용량 [[001_dikw_pyramid|데이터]]를 XCom으로 전달하는 오용
- 로컬 [[501_file_definition_logical_record|파일]] 경로에 의존해 개발 환경에서는 되지만 [[136_variance|분산]] 실행에서 깨지는 배포
- Catchup과 Backfill 개념을 이해하지 못해 과거 [[208_schedule_history_transaction_execution_order|스케줄]]이 대량으로 밀려 실행되는 사고

기술사 답안에서는 **"Airflow는 [[001_dikw_pyramid|데이터]] 및 [[190_ai_llm_requirements_specification|AI]] 배치 [[123_pipe|파이프]]라인의 제어 평면으로서 [[401_bayesian_network_dag_causality|DAG]] 기반 의존성 관리, 재시도, 백필, 실행 이력 관리를 제공하며, 실제 대용량 연산은 외부 처리 엔진으로 분리하는 것이 핵심 설계 원칙"**이라고 정리하면 된다.

- **📢 섹션 요약 비유**: Airflow를 잘 쓰는 팀은 무대 뒤에서 조명·음향·배우 순서를 정확히 맞추는 공연팀과 같고, 못 쓰는 팀은 감독에게 직접 무대 장치까지 들게 만드는 셈이다.

---

## Ⅴ. 기대효과 및 결론

Airflow를 도입하면 배치 [[123_pipe|파이프]]라인이 "누가 알음알음 돌리던 스크립트"에서 "조직이 관리하는 운영 자산"으로 바뀐다. 실행 이력, 실패 지점, 재시도, 백필, 알림이 표준화되므로 [[001_dikw_pyramid|데이터]] 품질 문제와 운영 공백을 더 빨리 발견할 수 있다. 특히 여러 시스템을 엮는 ETL과 모델 재학습 환경에서는 이 효과가 크다.

다만 Airflow는 도입만으로 품질이 보장되는 도구는 아니다. DAG가 무분별하게 늘어나거나, 워커가 처리 엔진 역할까지 떠맡거나, [[012_metadata|메타데이터]] [[002_database_definition|데이터베이스]]가 병목이 되면 오히려 새로운 운영 문제를 만든다. 그래서 Airflow는 "자동화 도구"라기보다 **[[073_container_orchestration_tools|오케스트레이션]] 규율을 강제하는 플랫폼**으로 보는 편이 정확하다.

결론적으로 Airflow는 [[645_data_pipeline_acceleration|데이터 파이프라인]]의 계산 능력이 아니라 통제 능력을 높이는 도구다. 무엇을 언제 어떤 순서로 실행하고, 실패하면 어떻게 다시 돌릴지 명확히 설명할 수 있을 때 Airflow의 진짜 가치가 드러난다.

- **📢 섹션 요약 비유**: Airflow는 공항의 관제탑과 같다. 관제탑이 비행기를 직접 날리지는 않지만, 이착륙 순서를 잘못 잡으면 공항 전체가 멈춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) | Airflow가 작업 의존성을 표현하는 핵심 구조다. |
| Scheduler | 실행 시점과 선행 조건을 계산하는 제어 핵심이다. |
| Executor | 작업을 어떤 실행 자원에 분배할지 결정한다. |
| XCom | [[150_task|Task]] 간 소량 [[012_metadata|메타데이터]] 전달 수단이지 대용량 [[345_data_bus|데이터 버스]]가 아니다. |
| Backfill / Catchup | 과거 시점 [[001_dikw_pyramid|데이터]]를 재실행하는 운영 기능으로 배치 품질 관리와 직결된다. |
| [[180_mlflow|MLflow]] | Airflow와 결합해 [[123_pipe|파이프]]라인 실행과 실험 추적을 분리하는 대표 도구다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Cron 기반 단일 스크립트
    │
    ▼
DAG 기반 의존성 관리
    │
    ├─ retry / alert / SLA
    ├─ logical date / backfill
    └─ metadata-driven observability
    │
    ▼
분산 Executor와 외부 처리 엔진 연동
    │
    ▼
ETL + MLOps 파이프라인 오케스트레이션
```

이 흐름은 Airflow가 단순 예약에서 출발해, 실행 상태와 재현성을 포함한 운영 플랫폼으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow는 공장에서 어떤 기계를 먼저 돌리고 다음에 무엇을 할지 순서를 정해 주는 반장님이에요.
2. 기계 하나가 고장 나면 뒤 기계들을 잠깐 멈추고, 고친 뒤 그 자리부터 다시 시작하게 해 줘요.
3. 반장님은 무거운 짐을 직접 나르지 않고, 누가 언제 일할지만 똑똑하게 지시해요.
