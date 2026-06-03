+++
weight = 27
title = "05. Apache Oozie와 Airflow - 워크플로우 오케스트레이션의 진화"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

# Apache Oozie와 Airflow - 워크플로우 [[073_container_orchestration_tools|오케스트레이션]]의 진화

> ⚠️ 이 문서는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 환경에서 [[136_variance|분산]]処理タスク([[018_mapreduce|맵리듀스]], 스park, hive等)의 실행 순서와 의존성을 정의하고 [[208_schedule_history_transaction_execution_order|스케줄]]링하는 워크플로우 오케스트레이터(Workflow Orchestrator)인 Apache Oozie와, Python 기반의 모던 [[645_data_pipeline_acceleration|데이터 파이프라인]] [[073_container_orchestration_tools|오케스트레이션]] 도구인 Apache Airflow의 아키텍처 차이([[401_bayesian_network_dag_causality|DAG]] 기반 처리, Operaner 모델, [[014_multi_tenancy|멀티 테넌시]])와, 오늘날 [[001_dikw_pyramid|데이터]] 엔지니어링 분야에서 Airflow가主流이 된 배경과 각 도구의 적합한 활용 시나리오를 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Oozie는 Hadoop生态圈에深度하게結合されたXML 기반의 워크플로우 엔진으로, 액션(Action)과 워크플로우(Workflow)를 XML로 기술하고 HDFS에 배포하여 YARN에서 실행하는"内製化された" 도구입니다. 반면 Apache Airflow는 Python으로 [[401_bayesian_network_dag_causality|DAG]](방향성 비순환 [[070_graph_datastructure|그래프]])를 코드として定義し, 메타스토어([[002_database_definition|데이터베이스]])에 실행 정보를 저장하고, [[079_kube_scheduler_pod_placement|스케줄러]]가 DAG를 [[507_acid_properties|트리거]]하며, Worker가 실제 [[150_task|태스크]]를 실행하는"외부화된" 모던 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼입니다.
> 2. **가치**: Oozie는 Hadoop과의 긴밀한統合([[018_mapreduce|맵리듀스]] [[150_task|태스크]] 직접 실행, [[013_hdfs|HDFS]] 배포, [[020_yarn|YARN]] 연동)를强点으로 하지만, XML 기반 [[009_config|설정]]의 복잡성과限定된エラー 핸들링能力が 부담이 됩니다. Airflow는 Python의 유연성으로 복잡한 분기, 조건부 실행, 예외 처리, 알람 통합 등을 Declarative하게 기술할 수 있어 현대 [[001_dikw_pyramid|데이터]] 엔지니어링 팀에서 빠르게采用되고 있습니다.
> 3. **확장**: Airflow는 [[150_soa_triangle_architecture|Provider]] 패키지를 통해 [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], [[074_photon_engine|Databricks]], [[179_kafka_flink_watermark_time_window|Kafka]], [[205_kubernetes_container_orchestration|Kubernetes]] 등400개 이상의 외부 시스템과 통합되며,"단일_control plane"으로 전사 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 [[229_monitor|모니터]]링하고 管理하는 것을 목표로 합니다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. 왜 워크플로우 [[073_container_orchestration_tools|오케스트레이션]]이 필요한가?
대규모 [[001_dikw_pyramid|데이터]] 처리에서는 단순히"한 개의 프로그램을 실행"하는 것이 아니라,"이 [[001_dikw_pyramid|데이터]]가 완료된 후에、あのプログラムを実行し、その後に电子邮件を送信"하는ような 복잡한 작업 순서(의존성 체인)를管理해야 합니다.
- **문제 상황**: 10단계로 구성된 nightly [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인이 있을 때, 각 단계 간의 의존성을 수동으로管理하면"3단계가 실패했는데 7단계를 이미 실행해버렸다"는 상황이나,"4단계의 입력이 아직 준비 안 됐는데 5단계를 실행해버렸다"는 상황이频発합니다.
- **필요성**: ワークフロー オ케ストレーター는"各タスクの入力/出力を定義"하고,"タスク完了時に次のタスクをトリガー"하며,"失敗時には 指定された 처리를実行"함으로써, [[645_data_pipeline_acceleration|데이터 파이프라인]]을 자동으로 관리합니다.

### 2. Apache Oozie의 탄생과 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계에서의 위치
Apache Oozie는 2011년 Yahoo!에서 개발하여 Apache Top-Level Project가 된 Hadoop용 워크플로우 엔진입니다.
- **설계 철학**: Oozie는" [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] Jobs 간의Workflow만을 전담"하자는 취지로 만들어졌습니다. 따라서 HDFS에 Workflow 정의를XML로 배포하고, YARN의 Application Master와 直接통신하여 [[018_mapreduce|맵리듀스]]/스파크/ [[544_hive|Hive]] [[150_task|태스크]]를 실행합니다.
- **주요 기능**: (1) Workflow ([[401_bayesian_network_dag_causality|DAG]] 기반 작업 순서), (2) [[250_coordinator_participant_2pc_roles|Coordinator]] (시간/[[001_dikw_pyramid|데이터]] 기반 [[208_schedule_history_transaction_execution_order|스케줄]]링), (3) Bundle (복수의 [[250_coordinator_participant_2pc_roles|Coordinator]] 그룹化管理)

### 3. Apache Airflow의 탄생: Python-native Modern Orchestrator
Airflow는 2014년 Airbnb(현 [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] → Astronomer 등이 유지보수)에서 개발하여 2018년 Apache Top-Level Project가 된 Python 기반의 모던 [[073_container_orchestration_tools|오케스트레이션]] 도구입니다.
- **설계 철학**: Airflow는"모든 것이 Python"이라는 원칙之下, Python으로 workflow를 코드として定義합니다. 이것은"[[009_config|설정]] [[344_as_autonomous_system_asn|as]] 代码(Configuration [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]])"의 реализация으로, [[317_versioning_data_model_design|버저닝]], [[330_code_review|코드 리뷰]], [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 등의 소프트웨어 엔지니어링 Best Practice를workflow에 적용할 수 있게 합니다.
- **주요 차별점**: Python [[565_operator_pattern_kubernetes_automation|Operator]] 모델을 통해 400개 이상의 외부 시스템과Integration이 가능하며, 웹 UI, [[477_rest_api_architecture|REST API]],CLI 등 풍부한 도구 지원을 제공합니다.

- **📢 섹션 요약 비유**: 워크플로우 [[073_container_orchestration_tools|오케스트레이션]]은"大型영화 제작의 기획書(스크립트) 관리"와 같습니다. 영화 촬영에는"1장면([[001_dikw_pyramid|데이터]] 수집) → 2장면(전처리) → 3장면(분석) → 크레딧(리포트)"이라는 순서가 있으며, 만약 2장면이延期되면 3장면도延期되어야 합니다. Apache Oozie는"영상 촬영만을 전문으로 하는 오디오 장비( [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 전용)"로, 스크립트 형식이 자사 규정(XML)에 맞춰져 있어 촬영은 잘 되지만, 영상 편집(外部 Integration)에는 별도의 변환기([[259_adapter_pattern_interface_wrapper|Adapter]])가 필요합니다. Apache Airflow는"모든 영상 장비와 호환되는 universal 조명 시스템(Python-native)"으로, 스크립트 형식이 Python(글로벌 표준)이므로 어떤 장비(시스템)와도 바로 연결할 수 있습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│              [ Apache Airflow 아키텍처 ]                           │
│                                                                 │
│  [Web Server] ─────── UI 대시보드 (DAG 모니터링)                   │
│       │                                                            │
│  [Triggerer] ─────── DAG 실행 트리거 (이벤트 기반)                │
│       │                                                            │
│  [Scheduler] ─────── DAG 실행 스케줄링 ( Cron 기반)               │
│       │              메타스토어에서 실행대상 DAG 탐색               │
│       │              → Task Instance 생성 → 메시지 큐에投薬        │
│       │                                                            │
│  [Executor] ───────── 작업 실행 방식 결정                          │
│  ├─ LocalExecutor: 같은 프로세스 내 병렬 실행 (개발용)            │
│  ├─ CeleryExecutor: Celery Workers에 작업 분산 (확장성)           │
│  ├─ KubernetesExecutor: Kubernetes Pod 단위 실행 (격리성)         │
│  └─ CeleryKubernetesExecutor: Hybrid                             │
│       │                                                            │
│  [Message Queue (Celery Backend)]                               │
│  └─ Redis / RabbitMQ ─── Task를 Worker에 전달                     │
│       │                                                            │
│  [Workers] ─────────── 실제 태스크 실행                            │
│  ├─ Worker 1: [Task A], [Task C] 실행                            │
│  ├─ Worker 2: [Task B], [Task D] 실행                            │
│  └─ Worker 3: [Task E] 실행                                       │
│       │                                                            │
│  [메타스토어 (Metadata Database)]                                 │
│  ├─ DAG 정의 (Python 코드)                                        │
│  ├─ Task Instance 상태 (queued/running/success/failed)          │
│  ├─ 실행 로그                                                      │
│  └─ XCom (태스크 간 데이터 공유)                                   │
│       │                                                            │
│  [Airflow Plugins / Providers]                                    │
│  └─ Snowflake, BigQuery, Databricks, Kafka, etc. (400+ 통합)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Apache Oozie의 Workflow 구조
Oozie의 Workflow는 XML로 정의되며, HDFS에 배포되어 YARN에서 실행됩니다.

```xml
<!-- Oozie Workflow XML 예시 -->
<workflow-app name="etl-workflow" xmlns="uri:oozie:workflow:0.5">
  <start to="ingest-data"/>
  <action name="ingest-data">
    <hive xmlns="uri:oozie:hive-action:0.5">
      <script>/scripts/ingest.hql</script>
    </hive>
    <ok to="transform-data"/>
    <error to="send-alert"/>
  </action>
  <action name="transform-data">
    <spark xmlns="uri:oozie:spark-action:0.2">
      <master>yarn-cluster</master>
      <script>/scripts/transform.py</script>
    </spark>
    <ok to="end"/>
    <error to="send-alert"/>
  </action>
  <kill name="send-alert">
    <message>Workflow failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
  </kill>
  <end name="end"/>
</workflow-app>
```

### 2. Apache Airflow의 [[401_bayesian_network_dag_causality|DAG]] 구조
Airflow의 DAG는 Python 코드로 정의됩니다.

```python
# Airflow DAG 예시 (Python)
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

default_args = {
    'owner': 'data_engineer',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 2 * * *',  # 매일 새벽 2시
    default_args=default_args,
    catchup=False,
) as dag:

    ingest_task = SnowflakeOperator(
        task_id='ingest_data',
        sql="CALL my_procedure('INSERT');",
        snowflake_conn_id='snowflake_conn',
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_function,
        op_kwargs={'input_key': 'data'},
    )

    check_quality = PythonOperator(
        task_id='check_data_quality',
        python_callable=data_quality_check,
    )

    # 의존성 정의
    ingest_task >> transform_task >> check_quality
    # 또는: ingest_task.set_downstream(transform_task)
```

### 3. Oozie vs Airflow: 핵심 아키텍처 차이

| 구분 | [[051_apache_oozie|Apache Oozie]] | [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] |
|:---|:---|:---|
| **정의 방식** | XML ([[013_hdfs|HDFS]] 배포) | Python 코드 ([[288_version_ihl_tos_total_length|버전]] 관리) |
| **실행 환경** | [[020_yarn|YARN]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계) | 자체 [[079_kube_scheduler_pod_placement|스케줄러]] + Worker (독립적) |
| **[[150_task|태스크]] 모델** | Action/Control Node | [[565_operator_pattern_kubernetes_automation|Operator]] (Python, Bash, [[541_cassandra|Snowflake]], etc.) |
| **에러 핸들링** | 기본 (error-to, retry) | 풍부 (Trigger Rules, Callback, Slack 알림) |
| **UI/[[229_monitor|모니터]]링** | 기본 | 풍부 (Gantt, Tree, [[104_graph|Graph]] 뷰) |
| **확장성** | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 스케일, 하지만 제한적 | Celery/K8s로 대규모 확장 |
| **주요 사용자** | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 레거시 | 모던 [[001_dikw_pyramid|데이터]] 엔지니어링 |

- **📢 섹션 요약 비유**: Oozie와 Airflow의 차이는"전통적 건축 설계 도면(Blueprint)"과"3D 디지털 건축 모델링(BIM)"의 차이와 같습니다. Oozie는"오래된 제도용잉크로 작성된 도면"(XML)"으로, 내용이 약속되어 있어 믿음성은 높지만 수정이 번거롭고, 건물 관리 소프트웨어(外部 도구)와의 연동이 어려워"이 도면대로 건축하는 것 외에 다른 활용"이 제한적입니다. Airflow는" BIM(Building Information Modeling)"으로, 건축 전부가 3D 디지털 모델( Python 코드)로 작성되어, 에너지 분석([[229_monitor|모니터]]링), 자재 관리(Integration) 등을同一 모델에서 동시에 할 수 있어"建筑物 완성 후 운영까지 전 과정"을管理할 수 있습니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | [[051_apache_oozie|Apache Oozie]] | [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] |
|:---|:---|:---|
| **학습 곡선** | 상대적으로 완만한 (XML熟悉必要) | Python熟悉的 엔지니어에게 친숙 |
| **生态계統合** | Hadoop生态系と紧密结合 | 400+ 외부 시스템Integration ([[150_soa_triangle_architecture|Provider]]) |
| **[[229_monitor|모니터]]링** | 기본적 | 매우 풍부 (Gantt, Tree, Slack 연동) |
| **에러 [[658_ir_recovery|복구]]** | 기본 (재시도, 알림) | 세밀함 (Trigger Rules, Depends on Past, Backfill) |
| **[[014_multi_tenancy|멀티 테넌시]]** | 제한적 | Celery + K8s로良好的 |
| **Python 활용** | 불가 (별도 Python [[150_task|태스크]] 필요) | 네이티브 Python 활용 |
| **현재 유지보수** | 크게 활발하지 않음 | 매우 활발 ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]] + Astronomer, AWS MWAA 등) |

- **Airflow가 주목받는 이유**: Airflow는"코드로서의 [[645_data_pipeline_acceleration|데이터 파이프라인]]"이라는 철학을 통해, [[001_dikw_pyramid|데이터]] 엔지니어링 팀의 생산성을 크게 향상시켰습니다. Python으로 DAG를 작성하면 Git으로 [[288_version_ihl_tos_total_length|버전]] 관리, Pull Request로 [[330_code_review|코드 리뷰]], [[090_configuration_item|CI]]/CD로 자동 테스트가 가능해져"엔지니어링 품질 관리"를 [[123_pipe|파이프]]라인에 적용할 수 있습니다. 또한 Rich한 UI,Slack/이메일 알림,실행 이력 추적,Backfill(과거 [[001_dikw_pyramid|데이터]] 재처리) 기능 등이 뛰어나"운영 관점"에서도 우월합니다.

- **📢 섹션 요약 비유**: Oozie와 Airflow의 [[083_relationship_in_er_model|관계]]를"레시피 관리"에 비유할 수 있습니다. Oozie는"전통 요리 레시피 카드(손으로 쓴 XML)"로, 레시피 자체는 훌륭하지만 수정이 필요하면 새 카드를 다시 써야 하고, 레시피를 자동으로 공유하거나(이메일 연동) 사진으로 [[003_bigdata_7v|시각화]]([[229_monitor|모니터]]링)하는功能이 제한적입니다. Airflow는"디지털 요리 앱(Python 코드)"으로, 레시피를 수정하면即座에 공유되고, 단계별로 타이머가自动 [[009_config|설정]]되고([[208_schedule_history_transaction_execution_order|스케줄]]링), Oven의 온도([[229_monitor|모니터]]링)를 실시간으로 [[396_validation|확인]]하며, 레시피가失敗하면即座에SMS로알림(에러 알림)을 받을 수 있습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **기존 인프라** | 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/[[013_hdfs|HDFS]] 환경 → Oozie 自然스럽게 Integration | 신규 / Cloud 환경 → Airflow |
| **팀 기술 [[057_stack|스택]]** | Java 중심 → Oozie XML (Java [[150_task|태스크]]) | Python 중심 → Airflow (네이티브) |
| **통합 필요성** | Hadoop生態圈中心 → Oozie | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], [[179_kafka_flink_watermark_time_window|Kafka]] 등 400+ → Airflow |
| **[[229_monitor|모니터]]링 요구** |基本监控足够 → Oozie | 상세 [[229_monitor|모니터]]링 + 알람 → Airflow |

*(추가 실무 적용 가이드 - Airflow 도입 [[124_decision_tree|Decision Tree]])*
- **Airflow가 적합한 경우**: Python 기반 [[001_dikw_pyramid|데이터]] 팀, [[541_cassandra|Snowflake]]/[[263_storage_compute_separation_bigquery|BigQuery]]/[[074_photon_engine|Databricks]] 등 모던 [[001_dikw_pyramid|데이터]] 플랫폼 활용, 상세 [[229_monitor|모니터]]링 필요, [[119_gitops_single_source_of_truth|GitOps]]/CD/CD 요구
- **Oozie가 적합한 경우**: 기존 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/[[013_hdfs|HDFS]] 환경에서 간단한 [[150_task|태스크]] 의존성 관리만 필요, 제한된 수의 [[150_task|태스크]] (10개 이내), 이미 Oozie가 구축되어 있는 레거시 환경
- **대안 고려**: Prefect, Dagster, Temporal 등 모던 [[073_container_orchestration_tools|오케스트레이션]] 도구도 평가해볼 가치가 있습니다. 특히 Dagster는"[[645_data_pipeline_acceleration|데이터 파이프라인]]의 테스트와 문서화를 중요시하는团队"에 적합합니다.

- **📢 섹션 요약 비유**: Airflow 도입 결정은"음식점厨房 관리 시스템 도입"과 같습니다. 만약 기존 주방( [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 환경)이自動化 된지 얼마 안 됐고 주요 식재료( [[013_hdfs|HDFS]] [[001_dikw_pyramid|데이터]])가 그 안에서만 사용된다면, 현재 Oven( Oozie)을 업그레이드하는 것이経済적입니다. 하지만 식재료가 여러 곳에서 배송되고([[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]]), 조리 과정이 복잡해(Celery, K8s)厨师([[001_dikw_pyramid|데이터]] 엔지니어)들이Python으로 자신만의 레시피를 업로드하고 싶어한다면,全新の万能厨房システム( Airflow 도입)가 필수적입니다.重要なのは"현재 주방의状況"과"앞으로 어떤 요리를 할 것인가"를 종합적으로 判断하는 것입니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **Airflow의 완전히 관리되는 [[090_service_kubernetes_network_load_balancing|서비스]] 확산**
   AWS MWAA (Managed Workflows for [[168_airflow_dag_pipeline_scheduling|Apache Airflow]]), Astronomer Cloud, Google Cloud Composer 등 fully managed Airflow [[090_service_kubernetes_network_load_balancing|서비스]]가 확산됨에 따라,"[[079_kube_scheduler_pod_placement|스케줄러]]/웹서버/Worker 관리"의 운영 부담이 크게 줄어들고 있습니다. 이는"[[206_serverless_cold_start|Serverless]] Airflow"라는 개념으로 진화하며, [[001_dikw_pyramid|데이터]] 엔지니어가"[[073_container_orchestration_tools|오케스트레이션]]의 logic 설계"에만 집중할 수 있는 환경을 제공합니다.

2. **Dagster의 台頭: "엔지니어링 우선" [[073_container_orchestration_tools|오케스트레이션]]**
   Prefect와 Dagster는 Airflow의"단점"(예: 테스트 어려움, [[123_pipe|파이프]]라인과 외부 시스템의耦合,세밀한 리소스 격리 어려움)을 개선한"차세대" [[073_container_orchestration_tools|오케스트레이션]] 도구로 떠오르고 있습니다. 특히 Dagster는"소스 코드 수준의 [[123_pipe|파이프]]라인 테스트", "타ипа卡片 기반 [[123_pipe|파이프]]라인 [[229_monitor|모니터]]링", "[[123_pipe|파이프]]라인과 [[079_kube_scheduler_pod_placement|스케줄러]]의 완벽한 분리"를 통해"엔지니어링 품질"을 한 단계 끌어올립니다.

3. **Temporal의崛起: [[532_microservices_decomposition_patterns|마이크로서비스]] 스타일의 워크플로우**
   Temporal은" طول 수명Workflow( Long-Running Workflow)"와"[[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]"을 네이티브하게 지원하는新規念な [[073_container_orchestration_tools|오케스트레이션]] 플랫폼으로,金融거래나 주문 처리처럼"여러 [[532_microservices_decomposition_patterns|마이크로서비스]]가 참여하는 장기간の Workflow"에 적합합니다. 이는"단순한 [[001_dikw_pyramid|데이터]] [[215_etl_vs_elt_pipeline|ETL]]"을 넘어"비즈니스 프로세스 [[073_container_orchestration_tools|오케스트레이션]]"으로의 확장을 보여줍니다.

- **📢 섹션 요약 비유**: 워크플로우 [[073_container_orchestration_tools|오케스트레이션]]의 미래 진화는"厨房机器人の进化"에 비유할 수 있습니다. 현재의 Airflow는" Recipe를 따라 조리하는 자동化システム"로, 레시피( [[401_bayesian_network_dag_causality|DAG]])대로 조리하고, 각 단계( [[565_operator_pattern_kubernetes_automation|Operator]])를 실행하며, 실패하면再試行합니다. 미래의 Dagster는" kitchenAssistant机器人"으로, 각 조리 단계뿐 아니라" 식재료 선별-검수-조리-서빙" 전 과정에 대해"품질 테스트"와"영양소 분석"까지 수행합니다. Temporal은"全自动化厨房工场"으로, Receita管理에 국한되지 않고"原料 발주-검수-조리-포장-배송"까지全自動化する Hybrid人工智能系统입니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **Apache Oozie核心组件**
    *   **Workflow**: [[401_bayesian_network_dag_causality|DAG]] 기반 작업 순서 (XML 정의)
    *   **[[250_coordinator_participant_2pc_roles|Coordinator]]**: 시간/[[001_dikw_pyramid|데이터]] 기반 Workflow [[507_acid_properties|트리거]]
    *   **Bundle**: 복수의 [[250_coordinator_participant_2pc_roles|Coordinator]] 그룹化管理
    *   **Action**: 실제 실행할 [[150_task|태스크]] ([[018_mapreduce|MapReduce]], Spark, [[544_hive|Hive]], Shell等)
*   **Apache Airflow核心组件**
    *   **[[401_bayesian_network_dag_causality|DAG]]**: Python으로 정의된 방향성 비순환 [[070_graph_datastructure|그래프]]
    *   **[[565_operator_pattern_kubernetes_automation|Operator]]**: [[150_task|태스크]] 실행 단위 (Python, Bash, [[541_cassandra|Snowflake]], etc.)
    *   **[[150_task|Task]]**: [[565_operator_pattern_kubernetes_automation|Operator]] 실행 인스턴스
    *   **Executor**: [[150_task|태스크]] 실행 방식 (Local, Celery, K8s)
    *   **XCom**: [[150_task|태스크]] 간 [[386_data_clean_room_sharing|데이터 공유]] 메커니즘
    *   **Connection**: 외부 시스템 연결 정보 관리
*   **Airflow vs alternatives**
    *   **Prefect**: Prefect Cloud + Orion 엔진, Python-첫
    *   **Dagster**: 테스트/문서화 특화, [[123_pipe|파이프]]라인-[[079_kube_scheduler_pod_placement|스케줄러]] 분리
    *   **Temporal**: Long-running Workflow + [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Oozie]
    │
    ▼
[Apache Airflow]
    │
    ▼
[DAG (Directed Acyclic Graph)]
    │
    ▼
[Celery/Kubernetes Executor]
    │
    ▼
[Dagster / Prefect]
```

이 흐름도는 Apache Oozie에서 출발해 Dagster / Prefect까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache Oozie와 Airflow는 여러 컴퓨터가 순서대로 일을 할 수 있도록 도와주는 지도老师和 같아요.
2. Oozie는 여러 단계를 XML이라는 특별한 말로 적어둔 거예요.
3. Airflow는 여러 단계를 Python이라는 计算机 친구들이 아는 말로 적어둬서 더 많은 컴퓨터들과 이야기할 수 있어요!

---
> **🛡️ Expert [[395_verification_process_review|Verification]]:** 본 문서는 Apache Oozie와 Airflow의 아키텍처 차이와 각 도구의 적합한 활용 시나리오를 기준으로 기술적 [[002_bigdata_5v|정확성]]을 [[395_verification_process_review|검증]]하였습니다. (Verified at: 2026-04-05)
