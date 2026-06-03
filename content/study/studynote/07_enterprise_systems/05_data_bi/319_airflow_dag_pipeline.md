---
title: 319. Apache Airflow DAG 파이프라인 오케스트레이션
date: '2026-05-09'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] (에어플로우)는 [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]], 방향성 비순환 [[070_graph_datastructure|그래프]])로 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 코드로 정의하고 [[208_schedule_history_transaction_execution_order|스케줄]]·의존성 관리·[[229_monitor|모니터]]링을 제공하는 [[191_oss_license_compliance|오픈소스]] 워크플로우 오케스트레이터다.
> 2. **가치**: [[123_pipe|파이프]]라인을 코드 (Python [[401_bayesian_network_dag_causality|DAG]])로 관리하면 [[288_version_ihl_tos_total_length|버전]] 관리 (Git), 테스트, 재사용이 가능해지며, [[150_task|태스크]] 간 의존성과 실패 재시도 (Retry)를 선언적으로 정의하여 복잡한 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있게 운영할 수 있다.
> 3. **판단 포인트**: Airflow는 배치 [[073_container_orchestration_tools|오케스트레이션]]에 강점이 있지만 실시간 스트리밍 처리에는 적합하지 않으며, 수백 개 이상의 DAG를 운영할 때는 [[079_kube_scheduler_pod_placement|스케줄러]] [[282_performance_tactics|성능]]과 메타DB 부하를 고려한 아키텍처 설계가 필요하다.

---

## Ⅰ. 개요 및 필요성

[[645_data_pipeline_acceleration|데이터 파이프라인]]은 일반적으로 [[001_dikw_pyramid|데이터]] 수집 → 변환 → [[395_verification_process_review|검증]] → 적재 → 리포팅의 여러 단계로 구성된다. 각 단계는 이전 단계 완료 후 실행되어야 하는 의존성이 있고, 실패 시 재시도·알림이 필요하다. 이를 [[107_nightly_build_scheduled_cron_pipeline|cron]] 스크립트로 관리하면 의존성 처리, 실패 감지, 재실행이 수작업이 된다.

Airflow는 Airbnb가 2014년 개발하고 2016년 Apache 인큐베이터에 기증했다. [[123_pipe|파이프]]라인을 Python DAG로 정의하면 의존성·[[208_schedule_history_transaction_execution_order|스케줄]]·재시도를 선언적으로 관리하고, 웹 UI로 실행 상태를 실시간 [[229_monitor|모니터]]링할 수 있다.

- **📢 섹션 요약 비유**: Airflow는 공장 조립 라인 관제탑이다. 부품 A가 완성되면 부품 B 조립을 시작하고, 문제가 생기면 자동으로 재작업하며, 전체 라인 상태를 대시보드로 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│                Airflow 아키텍처와 DAG 구성                          │
├──────────────────────────────────────────────────────────────────┤
│  Airflow 컴포넌트:                                                 │
│  웹 서버 (Web Server) → UI · REST API 제공                         │
│  스케줄러 (Scheduler) → DAG 파싱 · 태스크 스케줄링                  │
│  실행자 (Executor) → 태스크 실행 방식 결정                           │
│    SequentialExecutor: 순차 실행 (개발용)                           │
│    CeleryExecutor: 분산 실행 (Worker 노드 추가 가능)                │
│    KubernetesExecutor: K8s Pod로 격리 실행                         │
│  워커 (Worker) → 실제 태스크 실행 프로세스                          │
│  메타 DB (Metadata DB) → DAG·실행 기록·상태 저장 (PostgreSQL 권장) │
│                                                                  │
│  DAG 예시 (Python):                                               │
│  extract → transform → validate → load                           │
│  (t1)  →    (t2)    →   (t3)   → (t4)                           │
│                                                                  │
│  t1 >> t2 >> t3 >> t4  ← 의존성 선언 (Python 코드)                │
└──────────────────────────────────────────────────────────────────┘
```

| 개념               | 설명                              | 역할                      |
|:----------------|:---------------------------------|:------------------------|
| [[401_bayesian_network_dag_causality|DAG]]              | [[150_task|태스크]] 의존성 [[070_graph_datastructure|그래프]]                | [[123_pipe|파이프]]라인 전체 정의        |
| [[565_operator_pattern_kubernetes_automation|Operator]]         | [[150_task|태스크]] 실행 단위 (PythonOperator 등)| 각 단계 작업 실행          |
| [[150_task|Task]] Instance    | 특정 날짜의 [[150_task|태스크]] 실행 인스턴스    | 실행 상태·[[568_logs_distributed_logging_elk_fluentd|로그]] 추적         |
| [[401_bayesian_network_dag_causality|DAG]] Run          | 특정 날짜의 전체 [[401_bayesian_network_dag_causality|DAG]] 실행 인스턴스 | [[123_pipe|파이프]]라인 실행 단위        |
| XCom             | [[150_task|태스크]] 간 소규모 [[001_dikw_pyramid|데이터]] 전달 메커니즘| [[150_task|태스크]] 결과 공유           |

- **📢 섹션 요약 비유**: DAG는 요리 레시피다. 재료 손질(t1) → 볶기(t2) → 간 맞추기(t3) 순서가 정해져 있고, 이전 단계가 완료되어야 다음 단계가 시작된다.

---

## Ⅲ. 비교 및 연결

Airflow vs 대안 오케스트레이터 비교:

| 도구            | 특성                         | 강점                          | 약점                    |
|:-------------|:----------------------------|:-----------------------------|:-----------------------|
| Airflow       | Python [[401_bayesian_network_dag_causality|DAG]], 풍부한 생태계    | 유연성, 커뮤니티 생태계          | [[079_kube_scheduler_pod_placement|스케줄러]] 복잡도, 학습 곡선|
| Prefect       | 파이썬 함수 기반, 현대적 UI  | 코드 친화적, 동적 [[401_bayesian_network_dag_causality|DAG]]           | 상대적으로 작은 생태계   |
| Dagster       | [[001_dikw_pyramid|데이터]] 자산 중심, 타입 시스템 | [[001_dikw_pyramid|데이터]] 품질 통합, 테스트 용이     | 더 가파른 학습 곡선      |
| dbt (+ 오케스트레이터) | SQL 변환 특화          | 분석 엔지니어 친화적             | [[073_container_orchestration_tools|오케스트레이션]]만으로 불완전|

- **📢 섹션 요약 비유**: Airflow는 범용 공장 자동화 시스템, Dagster는 품질 관리 특화 시스템, dbt는 완제품 포장 전용 기계다. 목적에 맞는 도구 선택이 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[401_bayesian_network_dag_causality|DAG]] 설계 모범 사례**:
1. [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]): 같은 [[401_bayesian_network_dag_causality|DAG]] Run을 여러 번 실행해도 결과가 동일해야 함 → 덮어쓰기(UPSERT) 기반 설계
2. [[150_task|태스크]] [[193_atomicity_all_or_nothing|원자성]]: 각 [[150_task|태스크]]는 독립적으로 성공/실패 판단 가능해야 함
3. 적절한 [[150_task|태스크]] 크기: 너무 세분화 (오버헤드) vs 너무 큰 단위 (재시도 시 전체 재실행)
4. [[156_environment_variables|환경 변수]] 관리: Airflow Variables, Connections로 환경별 [[009_config|설정]] 분리

**[[282_performance_tactics|성능]] 튜닝**:
- [[079_kube_scheduler_pod_placement|스케줄러]] 파싱 부하: [[401_bayesian_network_dag_causality|DAG]] [[501_file_definition_logical_record|파일]] 수 최소화, `min_file_process_interval` 조정
- 동시 실행 제한: `max_active_runs_per_dag`, `concurrency` [[009_config|설정]]
- CeleryExecutor 워커 스케일: 작업량에 따른 워커 수 동적 조정

- **📢 섹션 요약 비유**: [[171_idempotency_iac_terraform|멱등성]]은 같은 주문서를 두 번 넣어도 같은 물건이 한 번만 배송되게 하는 것이다. 재처리 시 중복 문제가 없어야 한다.

---

## Ⅴ. 기대효과 및 결론

Airflow 도입으로 [[645_data_pipeline_acceleration|데이터 파이프라인]]이 코드로 관리되어 변경 이력 추적, [[330_code_review|코드 리뷰]], 자동화 테스트가 가능해진다. 실패 [[150_task|태스크]]의 자동 재시도와 알림으로 [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]이 높아지고, 시각적 [[401_bayesian_network_dag_causality|DAG]] [[229_monitor|모니터]]링으로 운영 효율성이 향상된다.

한계는 실시간 스트리밍 처리에 부적합하다는 점이다. Airflow는 배치 [[208_schedule_history_transaction_execution_order|스케줄]] 기반이므로, 이벤트 드리븐 실시간 처리는 [[179_kafka_flink_watermark_time_window|Kafka]]+Flink 같은 스트리밍 프레임워크가 필요하다. 배치(Airflow)와 스트리밍(Flink)을 병행하는 [[095_lambda_architecture|Lambda Architecture]] 또는 [[235_kappa|Kappa]] Architecture가 실무에서 많이 사용된다.

- **📢 섹션 요약 비유**: Airflow는 정기 배송 [[090_service_kubernetes_network_load_balancing|서비스]]다. 매일 정해진 시간에 물건을 배달하는 데는 최적이지만, 즉시 배달(실시간 스트리밍)은 다른 [[090_service_kubernetes_network_load_balancing|서비스]](Flink)가 필요하다.

---

### 📌 관련 개념 맵

| 개념                          | 연결 포인트                              |
|:-----------------------------|:----------------------------------------|
| [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]])  | Airflow [[123_pipe|파이프]]라인 정의 핵심 구조        |
| KubernetesExecutor            | [[150_task|태스크]]별 K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 격리 실행               |
| [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]])          | [[123_pipe|파이프]]라인 재실행 안전성 핵심 원칙       |
| dbt + Airflow                 | SQL 변환 + [[073_container_orchestration_tools|오케스트레이션]] 결합 패턴      |
| [[216_lambda_kappa_architecture_batch_realtime|Lambda]] / [[096_kappa_architecture|Kappa Architecture]]   | 배치+스트리밍 [[123_pipe|파이프]]라인 아키텍처 패턴   |

### 📈 관련 키워드 및 발전 흐름도

```
cron 기반 스크립트 (의존성·재시도 관리 어려움)
    │
    ▼
Airflow DAG (Python으로 파이프라인 코드화)
    │
    ▼
CeleryExecutor → KubernetesExecutor (분산·격리 실행)
    │
    ▼
DataOps: dbt + Airflow + 데이터 품질 테스트 통합
    │
    ▼
Prefect · Dagster (현대적 데이터 자산 중심 오케스트레이터)
```

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow는 레시피 관리 앱이에요. 요리 순서([[401_bayesian_network_dag_causality|DAG]])를 정해두면 각 단계를 정시에 자동으로 실행해줘요.
2. 한 단계가 실패하면 자동으로 다시 시도하고, 계속 실패하면 요리사(운영자)에게 알림을 보내요.
3. 모든 요리 기록(실행 [[568_logs_distributed_logging_elk_fluentd|로그]])이 남아서 "어제 몇 시에 어떤 요리가 실패했는지" 바로 [[396_validation|확인]]할 수 있어요!
