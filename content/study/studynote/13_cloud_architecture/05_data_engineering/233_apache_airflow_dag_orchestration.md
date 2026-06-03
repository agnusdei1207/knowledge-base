+++
weight = 233
title = "233. 아파치 에어플로우 (Apache Airflow)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Airflow는 복잡한 [[645_data_pipeline_acceleration|데이터 파이프라인]]의 선후행 의존성을 **[[401_bayesian_network_dag_causality|DAG]]([[255_apache_airflow_dag|Directed Acyclic Graph]], 방향성 비순환 [[070_graph_datastructure|그래프]])**로 Python 코드로 정의하고 [[208_schedule_history_transaction_execution_order|스케줄]]링·모니터링하는 워크플로우 [[073_container_orchestration_tools|오케스트레이션]] 도구다.
> 2. **가치**: 수십 개의 [[215_etl_vs_elt_pipeline|ETL]] 작업이 서로 복잡하게 의존할 때, 실패한 작업만 재실행하고 의존성 순서를 자동 관리하여 **[[645_data_pipeline_acceleration|데이터 파이프라인]] 운영의 신뢰성과 가시성**을 극대화한다.
> 3. **판단 포인트**: Airflow는 **"코드로 파이프라인 정의([[072_declarative_pipeline_jenkinsfile_as_code|Pipeline as Code]])"** 철학이므로 Git [[288_version_ihl_tos_total_length|버전]] 관리가 가능하지만, [[001_dikw_pyramid|데이터]]를 직접 처리하지 않고 작업 [[208_schedule_history_transaction_execution_order|스케줄]]링·실행만 담당한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 엔지니어링 파이프라인은 단순히 한 두 개의 작업이 아니다. 실무에서는 "[[001_dikw_pyramid|데이터]] 추출 → 품질 [[395_verification_process_review|검증]] → 변환 → 테이블 A 적재 → 테이블 B 적재 → BI 갱신 → 슬랙 알림" 같은 복잡한 의존성 체인이 형성된다.

2014년 Airbnb에서 개발, 현재 Apache 최상위 프로젝트. **"워크플로우를 코드로"** 라는 철학이 핵심이다.

```
[복잡한 파이프라인 의존성 예시]
                   extract_crm
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
    validate_crm   extract_erp   extract_ga
          │             │             │
          └──────┬───────┘             │
                 ▼                    │
          transform_orders            │
                 │                    │
                 └──────────┬─────────┘
                            ▼
                     load_fact_sales
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
           update_bi   train_ml   send_alert
```

이런 복잡한 의존성을 [[107_nightly_build_scheduled_cron_pipeline|cron]] 스크립트로 관리하면 실패 추적, 재실행, 모니터링이 불가능하다. Airflow가 이 문제를 해결한다.

📢 **섹션 요약 비유**: Airflow는 공장의 생산 관리 시스템([[119_mes_manufacturing_execution_system|MES]])이다. 각 공정([[150_task|Task]])이 어떤 순서로 [[216_progress_in_synchronization|진행]]되어야 하는지 공정도([[401_bayesian_network_dag_causality|DAG]])를 정의하면, 자동으로 순서를 조율하고 어떤 공정이 지연되거나 실패했는지 실시간으로 모니터링한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Airflow 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                  Airflow 아키텍처                              │
│                                                              │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │  Webserver  │   │  Scheduler   │   │   Executor        │  │
│  │  (UI/API)   │   │  (DAG 파싱   │   │   (Task 실행)     │  │
│  │  DAG 모니터 │   │   일정 관리)  │   │  ┌────────────┐  │  │
│  │  실행 로그  │   │              │   │  │Worker 1    │  │  │
│  └─────────────┘   └──────┬───────┘   │  │Worker 2    │  │  │
│                            │           │  │Worker 3    │  │  │
│                            │ Task 큐   │  └────────────┘  │  │
│  ┌─────────────┐           └──────────▶│                  │  │
│  │  Metadata   │                       └──────────────────┘  │
│  │  Database   │◀──────────────────────── 상태 업데이트       │
│  │ (PostgreSQL)│                                             │
│  └─────────────┘                                            │
│                                                              │
│  DAG 파일 저장소: Git Repo / S3 / Local filesystem           │
└──────────────────────────────────────────────────────────────┘
```

### [[401_bayesian_network_dag_causality|DAG]] 정의 예시

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

### 주요 [[565_operator_pattern_kubernetes_automation|Operator]] 유형

| [[565_operator_pattern_kubernetes_automation|Operator]] | 역할 | 예시 |
|:---|:---|:---|
| **PythonOperator** | Python 함수 실행 | [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]], 알림 |
| **BashOperator** | 쉘 명령 실행 | dbt 실행, 스크립트 |
| **SQLOperator** | SQL 실행 | [[209_data_warehouse_schema_on_write|DW]] [[298_qkv_attention|쿼리]] |
| **EmailOperator** | 이메일 발송 | 실패 알림 |
| **HttpOperator** | [[014_api_posix|API]] 호출 | [[477_rest_api_architecture|REST API]] [[507_acid_properties|트리거]] |
| **GlueJobOperator** | AWS Glue 잡 | S3 [[215_etl_vs_elt_pipeline|ETL]] |
| **SparkSubmitOperator** | Spark 잡 제출 | 대용량 배치 |
| **DbtOperator** | dbt 모델 실행 | [[034_elt|ELT]] Transform |
| **KubernetesPodOperator** | K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 실행 | 컨테이너화 작업 |

📢 **섹션 요약 비유**: Operator는 도구 상자 속 각종 공구다. 나사(Python), 망치(Bash), 전동 드릴(Spark) 등 각 작업에 맞는 도구를 골라 DAG에 조립하면 완성된 파이프라인이 된다.

---

## Ⅲ. 비교 및 연결

### 워크플로우 [[073_container_orchestration_tools|오케스트레이션]] 도구 비교

| 비교 항목 | [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | Prefect | Dagster | Luigi |
|:---|:---|:---|:---|:---|
| **코드 방식** | Python [[401_bayesian_network_dag_causality|DAG]] | Python Flow | Python Asset | Python [[150_task|Task]] |
| **UI** | 강력 | 좋음 | 좋음 | 기본 |
| **동적 [[401_bayesian_network_dag_causality|DAG]]** | 제한적 | 우수 | 우수 | 기본 |
| **관리형 [[090_service_kubernetes_network_load_balancing|서비스]]** | AWS MWAA, Astronomer | Prefect Cloud | Dagster Cloud | - |
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

📢 **섹션 요약 비유**: Airflow vs Prefect vs Dagster는 프로젝트 관리 도구 비교다. Airflow는 Microsoft [[042_relational_algebra_project|Project]](성숙·복잡), Prefect는 Notion(현대적·유연), Dagster는 Jira Software(에셋 추적 특화)다. 팀 상황에 맞는 도구를 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Airflow 운영 [[087_erp_package_advantages_best_practice|Best Practice]]

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

📢 **섹션 요약 비유**: Airflow의 [[171_idempotency_iac_terraform|멱등성]] 원칙은 은행 ATM과 같다. "1만원 출금"을 두 번 누르면 2만원이 나오면 안 된다. 재실행해도 항상 같은 결과(1만원 출금)를 보장해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **파이프라인 가시성** | UI에서 모든 [[150_task|Task]] 실행 상태 실시간 [[396_validation|확인]] |
| **자동 재시도** | [[150_task|Task]] 실패 시 정책에 따라 자동 재시도 |
| **의존성 관리** | 선행 [[150_task|Task]] 성공 후 후행 [[150_task|Task]] 자동 실행 |
| **이력 관리** | 모든 실행 이력 및 [[568_logs_distributed_logging_elk_fluentd|로그]] 저장 |
| **코드 [[288_version_ihl_tos_total_length|버전]] 관리** | [[401_bayesian_network_dag_causality|DAG]] Python 파일을 Git으로 관리 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **동적 [[401_bayesian_network_dag_causality|DAG]] 제한** | 실행 중 [[401_bayesian_network_dag_causality|DAG]] 구조 변경 어려움 |
| **학습 곡선** | [[401_bayesian_network_dag_causality|DAG]] 개념, Scheduler 이해 필요 |
| **[[459_quic_fec_forward_error_correction|초기]] [[009_config|설정]] 복잡** | Celery/[[205_kubernetes_container_orchestration|Kubernetes]] Executor, DB [[009_config|설정]] |
| **XCom 크기 제한** | [[150_task|Task]] 간 대용량 [[001_dikw_pyramid|데이터]] 전달 불가 (DB 저장) |
| **[[208_schedule_history_transaction_execution_order|스케줄]] [[002_bigdata_5v|정확성]]** | 초 단위 [[208_schedule_history_transaction_execution_order|스케줄]]링 불가 (최소 분 단위) |

📢 **섹션 요약 비유**: Airflow는 유능한 프로젝트 관리자다. 모든 작업의 순서와 의존성을 파악하고, 누가 실패하면 재시도시키며, 전체 [[216_progress_in_synchronization|진행]] 상황을 한눈에 보여준다. 단, 직접 일([[001_dikw_pyramid|데이터]] 처리)을 하지 않고 조율만 한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[401_bayesian_network_dag_causality|DAG]] (방향성 비순환 [[070_graph_datastructure|그래프]]) | Airflow 파이프라인 구조의 핵심 개념 |
| [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] | Airflow가 [[073_container_orchestration_tools|오케스트레이션]]하는 주요 워크로드 |
| dbt | Airflow에서 실행하는 대표 Transform 도구 |
| [[205_kubernetes_container_orchestration|Kubernetes]] | KubernetesPodOperator, KEDA 기반 워커 [[249_scaling_normalization_standardization|스케일링]] |
| [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | SparkSubmitOperator로 Airflow에서 Spark 잡 제출 |
| AWS MWAA | Airflow 관리형 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]] |
| [[171_idempotency_iac_terraform|멱등성]] | Airflow [[150_task|Task]] 설계의 핵심 원칙 |

### 👶 어린이를 위한 3줄 비유 설명
1. Airflow는 학교 시간표와 같다. 1교시 수학, 2교시 과학처럼 각 수업([[150_task|Task]])이 언제 어떤 순서로 [[216_progress_in_synchronization|진행]]되는지 정해두면, 선생님(Scheduler)이 자동으로 수업을 [[216_progress_in_synchronization|진행]]한다.

### 📈 관련 키워드 및 발전 흐름도

```text
cron + 쉘 스크립트 (의존관계 관리 불가)
    │
    ▼
Airflow: DAG 기반 워크플로 오케스트레이션
    ├─► Scheduler · Worker · Metadata DB
    └─► Operator: Python · Bash · K8s · Spark
    │
    ▼
차세대: Dagster · Prefect · Mage (데이터 자산 중심)
```
2. DAG는 집 짓기 공정표다. 기초 공사를 해야 벽을 세울 수 있고, 벽이 있어야 지붕을 올릴 수 있는 것처럼, 각 단계([[150_task|Task]])가 순서대로 이루어진다.
3. 만약 어느 공정이 실패하면(벽 공사 실패), Airflow는 자동으로 다시 시도하고, 실패 원인을 기록해 나중에 [[396_validation|확인]]할 수 있게 해준다.
