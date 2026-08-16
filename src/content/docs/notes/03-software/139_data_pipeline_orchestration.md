---
sidebar:
  order: 139
  label: "139. 데이터 파이프라인 오케스트레이션: Airflow (Data Pipeline Orchestration)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "데이터 파이프라인 오케스트레이션: Airflow (Data Pipeline Orchestration)"
date: "2026-08-14T00:51:00+09:00"
tags:
  - "notes-software"
weight: 139
extra:
  question_no: "139"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Airflow 의존성•재시도•스케줄 운영 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Data Pipeline Orchestration**: 이종의 수십~수백 개 데이터 연산 파이프라인(Task) 간의 실행 순서, 의존성(Dependency), 실패 재시도(Retry), 과거 데이터 재처리(Backfill)를 제어하고 모니터링하는 오케스트레이터 관리 체계.
- **Apache Airflow**: Airbnb가 제안한 파이썬(Python) 기반 오픈소스 표준 워크플로 오케스트레이션 플랫폼.
- **DAG (Directed Acyclic Graph)**: 순과정(Acyclic)이 없는 방향성 그래프 구조로, 작업(Task) 간의 `Task_A >> Task_B` 선후 의존 관계를 정의하는 워크플로 표현 단위.

</details>

- 정의/개념: 작업 의존성•실행 상태•복구를 제어하는 **오케스트레이션**
- 배경/필요성: 시간 기반 Cron만으로는 **선후 조건•재시도•백필** 제어 불가

#### 한줄 요약

- 지휘자는 작업 순서와 재실행을 정하고 실제 데이터 가공은 각 작업자가 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Workflow-as-Code**: 파이썬 코드로 DAG 워크플로를 작성하므로 Git 버전 관리, CI/CD 테스트, 동적 DAG 생성 가능.
- **Backfill & Re-execution**: 과거 실패했던 3년 치 파티션 구간을 단 한 줄의 CLI 명령으로 자동 순차 재계산(Backfill).

</details>

- **Workflow-as-Code (Python 코드 기반의 DAG 선언 및 Git 버전 통제)**
- **Robust Failure Recovery & Backfill (실패 시 조건부 Retry, SLA 모니터링, 과거 파티션 백필)**
- **Extensible Architecture (Operator, Sensor, Hook을 활용한 모든 클라우드/DB 연동)**

#### 한줄 요약

- 순서표가 있어도 작업을 한꺼번에 너무 많이 보내면 공용 창구가 막히므로 동시 실행 수를 제한해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Scheduler, Webserver, Celery Executor, Metadata DB**: Airflow 분산 가동을 지탱하는 4대 코어 물리 컴포넌트.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Apache Airflow Architecture                     │
├────────────────────────────────────────────────────────────────────────┤
│ [User Browser] ──► [Airflow Webserver (UI)]                            │
│                         │ (Read / Write Metadata)                      │
│                         ▼                                              │
│ [Airflow Scheduler] ──► [Metadata DB (PostgreSQL)]                     │
│   (DAG Parsing)         ▲ (Task State Update)                          │
│                         │                                              │
│ [Celery / Kubernetes Executor] ──► [Worker Node 1] [Worker Node 2]     │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Scheduler가 DAG를 파싱해 Metadata DB 및 Executor를 거쳐 Worker 노드로 Task를 분산 할당하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **Scheduler** | DAG 해석과 실행 가능 Task 판정 |
| **Metadata DB** | Run•Task 상태•재시도•이력 보관 |
| **Executor** | Task를 실행 큐•Pod•프로세스에 전달 |
| **Worker** | Operator 코드 실행과 상태 보고 |
| **Webserver** | 실행 상태•로그•수동 조작 UI 제공 |

#### 한줄 요약

- 상태 장부를 보고 준비된 작업만 작업자에게 보낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trigger Rule**: `all_success`, `one_failed`, `all_done` 등 선행 Task의 성공/실패 여부에 따라 후속 Task의 실행 진입 여부를 정하는 로직.

</details>

```text
[DAG 실행 시각]
      │
      ▼
1. DagRun 생성
      │
      ▼
2. 의존성•Trigger 판정
      │
      ▼
3. Task 큐잉
      │
      ▼
4. Worker 실행•상태 기록
      │
      ▼
5. 후속 Task•재시도 결정
```

### 동작 원리

1. **DagRun 생성**: 스케줄•데이터 구간별 실행 인스턴스 등록
2. **의존성•Trigger 판정**: 선행 상태•풀•동시성 검사
3. **Task 큐잉**: Executor에 실행 대상과 우선순위 전달
4. **Worker 실행•상태 기록**: 작업 수행 후 결과•로그 저장
5. **후속 Task•재시도 결정**: 성공•실패 정책으로 다음 상태 전이

#### 한줄 요약

- 설계도와 상태 장부를 보고 준비된 작업만 보내고 결과가 적힐 때마다 다음 작업을 다시 고른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Crontab vs Airflow**: Crontab은 단순 1회성 시간 기반 실행, Airflow는 DAG 기반 복합 의존성 및 UI 모니터링 보장.

</details>

| 비교 항목 | Linux Crontab | Apache Airflow | Prefect / Dagster (3세대) |
|:---|:---|:---|:---|
| **의존성 제어** | 쉘•외부 상태로 직접 구현 | **DAG 기반 Task 의존성** | Asset•Flow 기반 의존성 |
| **모니터링 UI** | 없음 (로그 파일 파싱 필요) | **우수 (웹 UI에서 Task 상태 시각화)**| **최상 (모던 데이터 아키텍처 UI)** |
| **과거 백필 **| 불가능 (수동 스크립트 개별 가동)| **CLI 한 줄로 파티션 백필 완전 자동화**| 완전 자동화 |
| **설정 방식** | 텍스트 Cron 표현식 | **Python DAG 코드** | Python Code & Asset 중심 |

#### 한줄 요약

- Airflow는 앞 작업의 결과를 보고 다음 일을 정하고 크론은 정해진 시각에 알람만 울린다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Top-Level Code Heavy Operations**: DAG 파이썬 파일의 Top-Level 위치에 DB 연결이나 API 호출 코드를 넣으면, Scheduler가 매초 파싱할 때마다 시스템 전체가 다운되는 안티패턴.

</details>

| 3대 Airflow 장애 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Scheduler Lag / Stalls**| Top-Level 파이썬 코드에 DB Heavy 쿼리 작성 | **Heavy 연산은 무조건 Operator 함수 내부 배치** |
| **2. Database Bottleneck** | Task 수가 수만 개로 늘어나 DB Connection 차올라감| **PGBouncer 연동 및 Task Concurrency 제한** |
| **3. OOM on Worker** | Worker 노드 메모리를 초과하는 대용량 DataFrame 연산 | **KubernetesPodOperator로 작업 노드 물리 분리** |

> 사례: **쿠팡 / 카카오 / 네이버 MWAA (Amazon Managed Workflows for Apache Airflow) 운용**

#### 한줄 요약

- 적재와 검사가 끝나야 게시하고 과거 재작업은 별도 줄에서 천천히 보낸다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Orchestration 수립 기준(Orchestration Standards)**: Airflow 2.x, Python DAG, Celery/K8s Executor, Top-Level Code 분리 및 Backfill 튜닝성에 의거한 체계.

</details>

- 단순 시간 실행은 **Cron**, 복합 의존•백필은 Airflow 선택

#### 한줄 요약

- 지휘자는 순서와 재시도를 맡고 각 작업은 다시 실행해도 결과가 겹치지 않게 만들어야 한다.
