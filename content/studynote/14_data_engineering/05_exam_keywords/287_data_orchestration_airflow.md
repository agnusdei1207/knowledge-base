---
title: "287. 데이터 오케스트레이션 Airflow DAG 워크플로 (Data Orchestration Airflow DAG Workflow)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Airflow는 **Python 코드로 작성된 DAG(Directed Acyclic Graph)**를 기반으로 **Scheduler -> Executor -> Worker** 3계층 구조에서 **Task 단위의 의존성·재시도·스케줄·백필**을 선언적으로 오케스트레이션하는 배치 워크플로 엔진이며, 2.x 이후의 **TaskFlow API(@task), Datasets 기반 Data-Aware Scheduling, DAG Serialization, HA Scheduler**가 핵심 차별점이다.
> 2. **가치**: 수천 개 태스크의 **SLA 준수율 95% 이상, 장애 격리로 인한 MTTR 60% 단축, 백필/리트라이 자동화로 운영 개입 70% 감소, Lineage 추적과 DAG Versioning**을 통해 데이터 거버넌스·컴플라이언스(개인정보 파기 SLA, 재무 결산 마감) 요구를 코드화할 수 있다.
> 3. **판단 포인트**: 워크로드 특성에 따른 **Executor 선택(CeleryExecutor vs KubernetesExecutor vs CeleryKubernetesExecutor)**, 외부 시스템 트리거 기반의 **Sensor 남용 vs Datasets/TriggerDagRunOperator**, **단일 Scheduler의 Bottleneck vs Airflow 2.7+ HA Scheduler(Active-Active)**, 그리고 **DAG 파일 I/O 부하와 Scheduler Parsing 한계(파일 수·복잡도)**가 아키텍처 결정의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

현대 데이터 플랫폼은 단순한 ETL을 넘어 **실시간 스트리밍, ML 파이프라인, 인프라 프로비저닝, API 의존 작업**이 혼재하는 복잡한 워크플로를 요구한다. 전통적인 **cron + shell 스크립트** 방식은 의존성 표현·재시도·로깅·알람·모니터링이 모두 수작업이라 장애 시 **평균 복구 시간(MTTR)이 길고, 운영자가 crontab을 직접 수정**해야 하는 "Configuration Drift" 문제가 발생한다. 또한 데이터 팀이 늘어나면서 **DAG 간 의존성 폭발(Dependency Hell)**로 신규 파이프라인 추가가 수일~수주 단위로 지연된다.

Apache Airflow(2014년 Airbnb에서 시작, 2019년 TLP, 2020년 2.0 출시)는 이를 **"Workflow as Code"** 패러다임으로 해결한다. Python의 표현력을 활용해 DAG을 코드로 정의하고, **메타데이터 DB(Metastore, 기본 SQLite -> 운영 시 PostgreSQL/MySQL)**를 단일 진실 공급원(Source of Truth)으로 사용해 **상태(State), 실행 이력(History), Lineage**를 통합 관리한다.

**기존 방식 vs Airflow 기반 오케스트레이션**

| 항목 | Cron + Shell Script | Apache Airflow |
|---|---|---|
| 의존성 표현 | `sleep &&` 체이닝 (수동) | `>>` / `set_downstream()` (DAG 선언) |
| 재시도/백오프 | 스크립트 내부 루프 작성 | `retries`, `retry_delay`, `retry_exponential_backoff` |
| 실패 알림 | cron mail / 별도 스크립트 | `on_failure_callback` + Email/Slack/Pagerduty Operator |
| 실행 이력 | 로그 파일 (`/var/log/cron.log`) | Metastore + Web UI (Run ID, Duration, Logs) |
| 파라미터화 | 환경변수 / 파일 치환 | `dag_run.conf`, Variables, `params` |
| SLA 관리 | 없음 | `sla_miss_callback` + Web UI SLA Miss 표시 |
| 동시성 제어 | 없음 (서버 과부하 위험) | `pool`, `priority_weight`, `concurrency` |

```text
+--------------------------------------------------------------------------+
|            데이터 오케스트레이션 패러다임의 진화                          |
+--------------------------------------------------------------------------+
|                                                                          |
|   1세대: cron + bash        2세대: Oozie/Azkanban    3세대: Airflow       |
|   +----------+              +----------+              +----------+        |
|   | Server A |              | Oozie    |              | Scheduler|        |
|   | Server B |  --->        | Coordi-  |   --->       | --------->|        |
|   | Server C |              | nator    |              | Executor |        |
|   +----------+              | (XML)    |              |  |       |        |
|   - 설정 분산                +----------+              |  v       |        |
|   - 장애 전파                - 하둡 종속                | Workers  |        |
|   - 수동 재실행              - 정적 워크플로            | (K8s Pod)|        |
|                                                    +----------+        |
|   (2010~)                    (2010~)                    (2014~)         |
|   도메인: 단일 서버          도메인: Hadoop 클러스터    도메인: 하이브리드 |
|                                                                          |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 기존 cron 방식이 **"각 가족에게 수기로 일정을 알려 알람기를 맞추게 하는 것"**이라면, Airflow는 **"Google Calendar처럼 모든 집안일(태스크)을 중앙 서버가 추적하고, 부엌(Worker)에 자동 배차하며, 완료 시 가족 단톡방(Web UI)에 자동 보고하는 시스템"**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Airflow는 **논리적 컴포넌트(Scheduler, Webserver, Metastore DB, Executor, Worker)**와 **DAG 파일(DAG Definition)**로 구성된다. 사용자가 정의한 DAG 파일을 Scheduler가 주기적으로 Parsing하여 DagRun/TaskInstance 객체를 생성하고, Executor가 이를 Worker에 분배·실행한다.

```text
+----------------------------------------------------------------------------+
|                    Apache Airflow 2.x 핵심 아키텍처                        |
|                                                                            |
|  +----------------+    1. Parsing (5s 주기)     +---------------------+   |
|  |  DAG Files     | ---------------------------> |   Scheduler         |   |
|  | (Python 코드)  |                              |  (DagFileProcessor  |   |
|  | - my_dag.py    |                              |   Manager)          |   |
|  +----------------+                              |  - Serialization    |   |
|        |                                          |  - Trigger Logic    |   |
|        | 2. @task / Operator 정의                 +----------+----------+   |
|        v                                                     |              |
|  +----------------+                                          |              |
|  | Metadata DB    | <------- 3. DagRun / TaskInstance CRUD ---+              |
|  | (PostgreSQL)   |                                          |              |
|  |  - dag_run     |                                          |              |
|  |  - task_instance|                                         |              |
|  |  - log         |                                          |              |
|  |  - serialized_dag|                                        |              |
|  +-------^--------+                                          |              |
|          | 4. 상태 변경                                       |              |
|          |                                                   v              |
|  +--------------+                                   +------------------+   |
|  |  Webserver    |  5. UI 조회 <----- DAG/Task 상태 - | Executor          |   |
|  |  (Flask +    |                                   | (CeleryExecutor/  |   |
|  |   Gunicorn)  |                                   |  K8sExecutor)     |   |
|  |  - REST API   |                                   +---------+--------+   |
|  +--------------+                                             |              |
|                                                              | 6. Task 할당  |
|                                                              v              |
|                                                      +------------------+  |
|                                                      |  Worker Nodes     |  |
|                                                      |  (Celery Worker/  |  |
|                                                      |   K8s Pod per TI) |  |
|                                                      |  - Operator 실행  |  |
|                                                      |  - Hook으로 외부  |  |
|                                                      |    시스템 연결    |  |
|                                                      +---------+--------+  |
|                                                                |            |
|                                                                v            |
|                                                      +------------------+  |
|                                                      |  External Systems |  |
|                                                      |  S3, GCS, BQ,    |  |
|                                                      |  SFTP, MySQL,    |  |
|                                                      |  Slack, Email    |  |
|                                                      +------------------+  |
|                                                                            |
|  [보조 컴포넌트]                                                            |
|   - Flower: Celery Worker 모니터링                                          |
|   - StatsD/Prometheus Exporter: 메트릭 수집                                 |
|   - Triggerer: Deferrable Operator/Trigger의 비동기 이벤트 루프 (Airflow 2.2+)|
|   - DAG File Processor: Scheduler 내부에서 DAG Parsing 전담 (2.0+)         |
+----------------------------------------------------------------------------+
```

### 1) DAG(Directed Acyclic Graph)와 TaskInstance의 상태 머신

DAG는 **순환이 없는 방향성 그래프**로, 노드가 Task, 엣지가 의존성이다. **Cycle이 있으면 무한 루프**가 되어 시스템이 중단되므로, Airflow는 명시적으로 검출하여 DAG Parsing 자체를 거부한다. Task는 다음 상태 머신을 거친다:

```
none -> scheduled -> queued -> running -> success / failed / up_for_retry / skipped / up_for_reschedule / deferred
```

| 상태 | 의미 | 트리거 조건 |
|---|---|---|
| `scheduled` | 실행 시각이 도래하여 대기열에 등록 | Scheduler가 `next_execution_date` 도달 시 |
| `queued` | Executor가 Worker에 할당 대기 | `queued_by_job_id` 기록 |
| `running` | Worker가 실제 수행 중 | `hostname`, `pid` 기록 |
| `success` | 정상 완료 | `_execute_task` 콜백 성공 |
| `up_for_retry` | 실패 후 재시도 대기 | `retries < max_retries` |
| `failed` | 재시도 소진 후 최종 실패 | `on_failure_callback` 발화 |
| `skipped` | BranchPythonOperator 분기에서 제외 | `none_failed_or_skipped` 트리거 |
| `up_for_reschedule` | Sensor가 `mode='reschedule'`로 다음 점검까지 해제 | `poke_interval` 적용 |
| `deferred` | 외부 이벤트/I/O 대기 (Trigger 사용) | `triggerer`가 비동기 모니터링 |

### 2) Scheduler의 핵심 메커니즘

Scheduler는 **DAG Parsing -> DagRun 생성 -> TaskInstance 스케줄 -> Executor 큐잉**의 4단계를 수행한다. Airflow 2.0 이전에는 단일 프로세스에서 모든 것을 처리해 병목이었으나, **2.0+부터 DAG File Processor Manager(서브 프로세스 풀)**가 도입되어 Parsing이 분리되었다.

```text
+------------------------------------------------------------------+
|         Scheduler 내부 루프 (1초 주기, scheduler_heartbeat)       |
+------------------------------------------------------------------+
|  1. DagFileProcessorManagerProcess                                |
|     +- DagFileProcessorProcess (N개, multiprocessing)             |
|         +- DAG 파일 1개 Parsing -> SerializedDAGModel 저장         |
|         +- DAG 파일 2개 Parsing -> ...                              |
|         +- 신규 DagRun 생성 (start_date, schedule_interval)        |
|  2. SchedulerJob                                                   |
|     +- DagRun의 scheduled TaskInstance 조회                        |
|     +- Pool 가용 슬롯 확인                                         |
|     +- Upstream 완료 여부 확인 (Trigger Rule 평가)                 |
|     +- Executor.queue_command(task_instance) 호출                  |
|  3. Executor (Celery/K8s)                                          |
|     +- TaskInstance를 큐(Redis)/Pod 스펙으로 변환하여 Worker 할당   |
+------------------------------------------------------------------+
```

### 3) Executor 선택 — 아키텍처의 분기점

| Executor | 동작 원리 | 적합 시나리오 | 제약/주의점 |
|---|---|---|---|
| **SequentialExecutor** | 단일 프로세스 순차 실행 | 개발/디버깅 전용 | 프로덕션 부적합 |
| **LocalExecutor** | 로컬 멀티프로세스 | 소규모 단일 노드 (<50 tasks) | DB 락 경합, 단일 장애점 |
| **CeleryExecutor** | Celery + Redis/RabbitMQ로 태스크 분배 | 중규모 (50~500 tasks/day), 상시 Worker Pool 유지 | Worker 상시 가동으로 비용, Celery Broker 장애 시 큐 적체 |
| **CeleryKubernetesExecutor** | Celery + K8s 하이브리드 | **일부는 상시 Worker, 일부는 K8s Pod 격리** | 양쪽 운영 복잡도 |
| **KubernetesExecutor** | **TaskInstance 1개당 K8s Pod 1개 동적 생성** | 간헐적·격리·리소스 변동 큰 워크로드, ML training | K8s API 호출 오버헤드, Image Pull 시간, K8s 클러스터 필수 |
| **CeleryExecutor + DockerOperator** | Celery Worker 안에서 docker run | 패키지 의존성 격리 (Python 2/3 공존) | Airflow 2.0에서 KubernetesExecutor로 흡수 권장 |

### 4) Operator / Sensor / Hook의 분담

* **Operator**: Task의 **"무엇을 할 것인가"**를 정의 (단일 작업 단위, BashOperator, PythonOperator, BigQueryInsertJobOperator 등 50+ 내장)
* **Sensor**: Operator의 특수 형태로 **외부 상태를 폴링** (S3KeySensor, ExternalTaskSensor, HttpSensor)
* **Hook**: Operator 내부에서 **외부 시스템 연결 추상화** (S3Hook -> boto3 래퍼, BigQueryHook -> google-cloud-bigquery 래퍼). Connection 오브젝트(Airflow Metastore에 저장된 `conn_id`)로 인증 정보 통합 관리
* **TaskFlow API (`@task`)**: Airflow 2.0에서 도입된 **XCom 자동 처리** 래퍼. 함수 인자/리턴이 자동 직렬화되어 의존성 그래프의 노드 역할을 동시에 수행

### 5) Deferrable Operator와 Triggerer

전통적인 Sensor는 **Worker 슬롯을 점유한 채 `time.sleep()`**로 폴링하여 자원 낭비가 심했다(예: 1시간 대기 Sensor가 1시간 Worker CPU 점유). Airflow 2.2+의 **Deferrable Operator + Triggerer**는 Sensor의 폴링을 **Triggerer 프로세스의 비동기 이벤트 루프(asyncio)**로 옮기고, 대기 중에는 Worker 슬롯을 반납한다. 이로써 **동시 Sensor 1000건을 Triggerer 단일 프로세스 1개**로 처리할 수 있다.

### 6) Datasets (Data-Aware Scheduling, Airflow 2.4+)

기존의 **시간 기반 스케줄**(`schedule="0 2 * * *"`)은 **데이터 도착 시점과 무관**하게 실행되어 **데이터 미준비로 인한 No-op 실행**이 빈번했다. Datasets은 **"이 태스크가 이 Dataset을 produce"** -> **"다른 DAG가 그 Dataset을 consume"**을 선언하면, **자동으로 의존 DAG를 트리거**한다. 구현은 Metastore의 `dataset_event` 테이블 + `dataset_dag_run_queued_ref`로, **DAG 간 명확한 데이터 Lineage + 의존성 표현**이 가능하다.

### 7) 핵심 구성 요소 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Scheduler** | DAG Parsing, DagRun/TaskInstance 생성, Executor 큐잉 | DagFileProcessorManager(멀티프로세스), SerializedDAGModel 캐
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 287 / 300

<- **이전**: [286. 엣지 데이터 처리 분산 파이프라인 설계 (Edge Data Processing Distributed Pipeline)](/studynote/14_data_engineering/05_exam_keywords/286_edge_data_processing/)
**다음**: [288. dbt 데이터 변환 모델링 테스트 문서화 (dbt Data Transformation Modeling Testing)](/studynote/14_data_engineering/05_exam_keywords/288_dbt_transformation/) ->

---
