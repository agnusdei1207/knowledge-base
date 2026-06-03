+++
title = "233. 아파치 에어플로우 (Apache Airflow)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Airflow는 복잡한 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 선후행 의존성을 <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a>(<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/">Directed Acyclic Graph</a>, 방향성 비순환 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>)</strong>로 Python 코드로 정의하고 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링·모니터링하는 워크플로우 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 도구다.
> 2. **가치**: 수십 개의 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 작업이 서로 복잡하게 의존할 때, 실패한 작업만 재실행하고 의존성 순서를 자동 관리하여 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/">데이터 파이프라인</a> 운영의 신뢰성과 가시성</strong>을 극대화한다.
> 3. **판단 포인트**: Airflow는 <strong>"코드로 파이프라인 정의(<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/072_declarative_pipeline_jenkinsfile_as_code/">Pipeline as Code</a>)"</strong> 철학이므로 Git [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 가능하지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직접 처리하지 않고 작업 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링·실행만 담당한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 파이프라인은 단순히 한 두 개의 작업이 아니다. 실무에서는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 추출 → 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) → 변환 → 테이블 A 적재 → 테이블 B 적재 → BI 갱신 → 슬랙 알림" 같은 복잡한 의존성 체인이 형성된다.

2014년 Airbnb에서 개발, 현재 Apache 최상위 프로젝트. **"워크플로우를 코드로"** 라는 철학이 핵심이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">복잡한 파이프라인 의존성 예시</div></div>
<div class="kb-diagram-note">extract_crm</div>
<div class="kb-diagram-note">validate_crm extract_erp extract_ga</div>
<div class="kb-diagram-note">transform_orders</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">load_fact_sales</div>
<div class="kb-diagram-note">update_bi train_ml send_alert</div>
</div>
</div>



이런 복잡한 의존성을 [cron](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/) 스크립트로 관리하면 실패 추적, 재실행, 모니터링이 불가능하다. Airflow가 이 문제를 해결한다.

📢 **섹션 요약 비유**: Airflow는 공장의 생산 관리 시스템([MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/))이다. 각 공정([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/))이 어떤 순서로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)되어야 하는지 공정도([DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/))를 정의하면, 자동으로 순서를 조율하고 어떤 공정이 지연되거나 실패했는지 실시간으로 모니터링한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Airflow 시스템 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Airflow 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Webserver</div><div class="kb-diagram-cell">Scheduler</div><div class="kb-diagram-cell">Executor</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(UI/API)</div><div class="kb-diagram-cell">(DAG 파싱</div><div class="kb-diagram-cell">(Task 실행)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAG 모니터</div><div class="kb-diagram-cell">일정 관리)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실행 로그</div><div class="kb-diagram-cell">Worker 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Worker 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Worker 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Task 큐</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Metadata</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Database</div><div class="kb-diagram-cell">◀ 상태 업데이트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(PostgreSQL)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAG 파일 저장소: Git Repo / S3 / Local filesystem</div></div>
</div>
</div>



### [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 정의 예시

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

with DAG(
    dag_id='daily_sales_pipeline',
    schedule='0 2 * * *',      # 매일 새벽 2시
    start_date=datetime(2024, 1, 1),
    catchup=False,              # 과거 실행 소급 방지
    default_args=default_args,
) as dag:

    extract = GlueJobOperator(
        task_id='extract_orders',
        job_name='extract-rds-orders',
    )
    
    validate = PythonOperator(
        task_id='validate_data_quality',
        python_callable=run_dq_checks,
    )
    
    transform = SnowflakeOperator(
        task_id='transform_fact_sales',
        sql='sql/transform_fact_sales.sql',
        snowflake_conn_id='snowflake_prod',
    )
    
    notify = PythonOperator(
        task_id='send_slack_alert',
        python_callable=send_success_alert,
    )
    
    # 의존성 정의
    extract >> validate >> transform >> notify
```

### 주요 [Operator](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/) 유형

| [Operator](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/) | 역할 | 예시 |
|:---|:---|:---|
| **PythonOperator** | Python 함수 실행 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 알림 |
| **BashOperator** | 쉘 명령 실행 | dbt 실행, 스크립트 |
| **SQLOperator** | SQL 실행 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **EmailOperator** | 이메일 발송 | 실패 알림 |
| **HttpOperator** | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 | [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
| **GlueJobOperator** | AWS Glue 잡 | S3 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) |
| **SparkSubmitOperator** | Spark 잡 제출 | 대용량 배치 |
| **DbtOperator** | dbt 모델 실행 | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) Transform |
| **KubernetesPodOperator** | K8s [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 실행 | 컨테이너화 작업 |

📢 **섹션 요약 비유**: Operator는 도구 상자 속 각종 공구다. 나사(Python), 망치(Bash), 전동 드릴(Spark) 등 각 작업에 맞는 도구를 골라 DAG에 조립하면 완성된 파이프라인이 된다.

---

## Ⅲ. 비교 및 연결

### 워크플로우 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 도구 비교

| 비교 항목 | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | Prefect | Dagster | Luigi |
|:---|:---|:---|:---|:---|
| **코드 방식** | Python [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | Python Flow | Python Asset | Python [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) |
| **UI** | 강력 | 좋음 | 좋음 | 기본 |
| <strong>동적 <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a></strong> | 제한적 | 우수 | 우수 | 기본 |
| <strong>관리형 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong> | AWS MWAA, Astronomer | Prefect Cloud | Dagster Cloud | - |
| **학습 곡선** | 높음 | 중간 | 중간 | 낮음 |
| **에코시스템** | 매우 풍부 | 성장 중 | 성장 중 | 제한적 |
| **엔터프라이즈 사용** | 매우 많음 | 증가 중 | 증가 중 | 소규모 |

### XCom (Cross-Communication)

```python
# Task 간 데이터 전달 (XCom)
def extract_task(**context):
    result = fetch_data()
    context['ti'].xcom_push(key='row_count', value=len(result))
    return result

def validate_task(**context):
    row_count = context['ti'].xcom_pull(
        task_ids='extract_orders', 
        key='row_count'
    )
    if row_count < 100:
        raise ValueError(f"Too few rows: {row_count}")
```

📢 **섹션 요약 비유**: Airflow vs Prefect vs Dagster는 프로젝트 관리 도구 비교다. Airflow는 Microsoft [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/)(성숙·복잡), Prefect는 Notion(현대적·유연), Dagster는 Jira Software(에셋 추적 특화)다. 팀 상황에 맞는 도구를 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Airflow 운영 [Best Practice](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)

```
[DAG 설계 원칙]
□ 원자성(Atomicity): 각 Task는 독립 실행 및 재실행 가능
□ 멱등성(Idempotency): 같은 실행 날짜로 재실행 시 동일 결과
□ 재시도 설정: retries=3, retry_delay=5분 기본 설정
□ 타임아웃: execution_timeout 설정으로 무한 대기 방지
□ catchup=False: 과거 실행 일정 소급 방지
□ depends_on_past=False: 이전 실행 실패 무관 실행

[모니터링 체크리스트]
□ SLA Miss 알림: 정해진 시간 내 완료 여부 모니터링
□ 실패 알림: Email/Slack 연동
□ DAG Lag 모니터링: 예상보다 오래 걸리는 Task 추적
```

### Airflow + dbt 통합 패턴

```python
# dbt DAG 예시 (DbtTaskGroup 또는 DbtOperator)
with DAG('dbt_daily_transform', schedule='0 3 * * *', ...):
    
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='dbt seed --profiles-dir /dbt --project-dir /dbt'
    )
    
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --profiles-dir /dbt --project-dir /dbt'
    )
    
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --profiles-dir /dbt --project-dir /dbt'
    )
    
    dbt_seed >> dbt_run >> dbt_test
```

📢 **섹션 요약 비유**: Airflow의 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 원칙은 은행 ATM과 같다. "1만원 출금"을 두 번 누르면 2만원이 나오면 안 된다. 재실행해도 항상 같은 결과(1만원 출금)를 보장해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **파이프라인 가시성** | UI에서 모든 [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 실행 상태 실시간 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| **자동 재시도** | [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 실패 시 정책에 따라 자동 재시도 |
| **의존성 관리** | 선행 [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 성공 후 후행 [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 자동 실행 |
| **이력 관리** | 모든 실행 이력 및 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장 |
| <strong>코드 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리</strong> | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) Python 파일을 Git으로 관리 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong>동적 <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a> 제한</strong> | 실행 중 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 구조 변경 어려움 |
| **학습 곡선** | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 개념, Scheduler 이해 필요 |
| <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 복잡</strong> | Celery/[Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) Executor, DB [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| **XCom 크기 제한** | [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 간 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 불가 (DB 저장) |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/">스케줄</a> <a href="/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a></strong> | 초 단위 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링 불가 (최소 분 단위) |

📢 **섹션 요약 비유**: Airflow는 유능한 프로젝트 관리자다. 모든 작업의 순서와 의존성을 파악하고, 누가 실패하면 재시도시키며, 전체 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 상황을 한눈에 보여준다. 단, 직접 일([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리)을 하지 않고 조율만 한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) (방향성 비순환 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)) | Airflow 파이프라인 구조의 핵심 개념 |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) | Airflow가 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)하는 주요 워크로드 |
| dbt | Airflow에서 실행하는 대표 Transform 도구 |
| [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) | KubernetesPodOperator, KEDA 기반 워커 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | SparkSubmitOperator로 Airflow에서 Spark 잡 제출 |
| AWS MWAA | Airflow 관리형 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) | Airflow [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 설계의 핵심 원칙 |

### 👶 어린이를 위한 3줄 비유 설명
1. Airflow는 학교 시간표와 같다. 1교시 수학, 2교시 과학처럼 각 수업([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/))이 언제 어떤 순서로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)되는지 정해두면, 선생님(Scheduler)이 자동으로 수업을 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)한다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">cron + 쉘 스크립트 (의존관계 관리 불가)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Airflow: DAG 기반 워크플로 오케스트레이션</div>
<div class="kb-diagram-tree-item" style="--depth:2">Scheduler · Worker · Metadata DB</div>
<div class="kb-diagram-tree-item" style="--depth:2">Operator: Python · Bash · K8s · Spark</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">차세대: Dagster · Prefect · Mage (데이터 자산 중심)</div>
</div>
</div>


2. DAG는 집 짓기 공정표다. 기초 공사를 해야 벽을 세울 수 있고, 벽이 있어야 지붕을 올릴 수 있는 것처럼, 각 단계([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/))가 순서대로 이루어진다.
3. 만약 어느 공정이 실패하면(벽 공사 실패), Airflow는 자동으로 다시 시도하고, 실패 원인을 기록해 나중에 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있게 해준다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 232 / 371

← **이전**: [232. CDC (Change Data Capture / 변경 데이터 캡처)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/232_cdc_change_data_capture_debezium/)
**다음**: [234. 컬럼 지향 스토리지 (Columnar Storage) - Parquet / ORC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/) →

---
