---
sidebar:
  order: 139
  label: "139. 데이터 파이프라인 오케스트레이션: Airflow"
  badge:
    text: "미출 · 50%"
    variant: note
title: "데이터 파이프라인 오케스트레이션: Airflow (Data Pipeline Orchestration)"
date: "2026-08-31T10:48:00+09:00"
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

- **데이터 파이프라인 오케스트레이션**: 분산된 데이터 처리 작업 간의 실행 선후 관계, 스케줄링, 실패 복구, 모니터링을 중앙에서 통제하는 프레임워크.
- **Apache Airflow & DAG**: Python 코드로 방향성 비순환 그래프(DAG)를 정의하여 작업 간의 의존성(`Task_A >> Task_B`)을 관리하는 오케스트레이션 플랫폼.

</details>

- 정의/개념: 복잡한 데이터 파이프라인 간의 실행 순서(DAG), 의존성, 실패 재시도, 스케줄링 및 백필(Backfill)을 코드로 제어하는 오케스트레이션 체계
- 배경/필요성: 시간 기반 스케줄러(Crontab)의 선행 작업 완료 미검증으로 인한 불량 데이터 하류 전파, 장애 시 수동 재시도 및 과거 이력 소급 처리(Backfill) 불가 한계

#### 한줄 요약
- 오케스트레이터는 작업 자체를 빠르게 하지 않고 실패와 재실행을 다루는 비용을 낮추므로, 도입 효과는 작업 수보다 실패 빈도와 소급 처리 필요성에 비례한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Workflow-as-Code**: 파이썬 코드로 파이프라인을 작성하므로 Git 버전 관리, CI/CD 테스트, 동적 DAG 생성이 가능.
- **Backfill**: 과거 특정 기간(예: 최근 1년) 동안 누락되거나 오류가 발생한 파티션 데이터를 CLI 명령으로 자동 순차 재실행하는 기능.

</details>

- 파이썬 코드로 파이프라인을 선언하고 Git 버전 관리하는 **Workflow-as-Code**
- 실패 시 조건부 재시도 및 과거 파티션을 일괄 소급 재처리하는 자동화된 백필(Backfill)
- Operator, Sensor, Hook을 통해 클라우드와 DB를 연결하는 확장성 높은 플러그인 아키텍처

#### 한줄 요약
- 코드 기반 워크플로, 강력한 장애 복구 및 백필, 유연한 확장성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Airflow 4대 핵심 컴포넌트**: Webserver(GUI UI), Scheduler(DAG 파싱/스케줄링), Metadata DB(상태 저장소), Executor/Worker(태스크 실행기).

</details>

```text
[Apache Airflow 구성]
|-- 스케줄러
|-- 메타데이터 DB
|-- 실행기
|-- 워커
`-- 웹서버
```

선의 의미: 계층 및 Scheduler가 DAG를 해석하여 DB에 상태를 기록하고 Executor를 통해 Worker 노드로 작업을 분산 실행하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 스케줄러 (Scheduler) | DAG 코드를 파싱하고 의존성을 평가하여 실행 가능한 Task를 Executor 큐로 전달 | 2초 주기 루프 스캔 |
| 메타데이터 DB | DAG 실행(DagRun), Task 상태, 연결 정보, 변수(Variables)를 영구 보관 | PostgreSQL, MySQL |
| 실행기 (Executor) | 스케줄러로부터 받은 Task를 Celery 워커나 Kubernetes Pod로 분산 할당 | K8s/Celery Executor |
| 워커 (Worker) | 할당받은 Operator의 비즈니스 로직을 실제 프로세스/컨테이너에서 실행 후 결과 보고| 분산 병렬 연산 |
| 웹서버 (Webserver) | 파이프라인 실행 상태 그래프, 로그 뷰어, 수동 재실행 인터페이스 제공 | Flask 기반 GUI |

#### 한줄 요약
- 스케줄러와 메타데이터 DB는 개별 배치 스크립트에 흩어져 있던 의존성 판단과 실행 상태 보관을 중앙 계층으로 흡수하고, 실행기는 그 판단을 Celery 워커나 Kubernetes Pod로 교체 가능한 실행 계층과 분리해 둔다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trigger Rule**: `all_success`(전원 성공), `one_failed`(하나라도 실패 시), `all_done`(성패 무관 완료 시) 등 후속 작업 실행 조건을 지정하는 규칙.

</details>

```text
정해진 스케줄 시각 도달 또는 수동 트리거 발생
        │
   [DagRun 인스턴스 생성] 스케줄러가 메타데이터 DB에 신규 실행 인스턴스 생성 및 상태(Running) 기록
        │
   [선행 의존성 및 Trigger Rule 검증] 선행 Task의 성공 완료 및 리소스 풀 가용 여부 확인
        │
   [Task 큐잉] 준비 완료된 Task를 Celery 브로커(Redis) 또는 K8s API 큐로 전송
        │
   [Worker 실행 및 상태 보고] 워커가 로직 실행 후 성공(Success)/실패(Failed) 상태를 메타 DB에 기록
        │
   실패 시 정의된 `retries` 횟수에 따라 지수 백오프 재시도, 성공 시 후속 Task 즉시 트리거
```

#### 한줄 요약
- 스케줄러가 메타데이터 DB를 거쳐 모든 상태를 판단하므로 DAG 수가 늘면 연산이 아니라 그 DB 접근이 먼저 병목이 되며, 파싱 주기 설정이 반응 속도와 부하를 동시에 좌우한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Crontab vs Airflow vs Dagster**: 단순 시간 실행(Crontab), DAG 기반 워크플로(Airflow), 데이터 자산 중심 오케스트레이터(Dagster).

</details>

| 비교 항목 | Linux Crontab | Apache Airflow (2세대) | Dagster / Prefect (3세대) |
|:---|:---|:---|:---|
| 의존성 제어 | 시간차 간접 의존 (선후 보장 불가) | DAG 기반 선후 의존성 완벽 보장 | 데이터 자산(Asset) 중심 의존성|
| 모니터링 및 UI | 없음 (서버 로그 수동 확인) | 웹 UI 기반 실시간 그래프 및 로그 뷰어 | 모던 웹 UI 및 데이터 카탈로그 결합|
| 과거 백필(Backfill) | 불가 (수동 쉘 스크립트 작성) | CLI 한 줄로 다중 파티션 자동 백필 | 파티션 기반 자동 백필 완전 지원 |
| 설정 방식 | 텍스트 Cron 표현식 | Python 코드 기반 DAG 선언 | Python 코드 & 데코레이터 중심 |

#### 한줄 요약
- 단순 스케줄링은 Cron, 엔터프라이즈 복합 파이프라인은 Airflow, 자산 중심 관리는 Dagster를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Top-Level Code**: DAG 파이썬 파일의 최상단(함수 밖)에 작성된 코드로, 스케줄러가 매초 파싱할 때마다 실행되어 DB 부하를 유발하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Top-Level에 무거운 쿼리/API 호출 작성으로 스케줄러 다운 | 무거운 로직은 반드시 Operator `execute()` 함수 내부로 격리 | 스케줄러 파싱 지연 0화 |
| 수만 개 Task 동시 실행 시 메타데이터 DB 커넥션 고갈 | PgBouncer 커넥션 풀러 연동 및 Task 동시성(Concurrency) 제한 | DB 병목 및 락업 해소 |
| 대용량 데이터 로드로 인한 Worker 메모리 OOM 크래시 | `KubernetesPodOperator` 활용하여 작업을 격리된 독립 Pod로 분리 | 워커 클러스터 안정성 확보 |
| DAG 파일 수 급증으로 인한 스케줄러 CPU 과부하 | `min_file_process_interval` 튜닝 및 DAG 디렉터리 샤딩 | 스케줄러 리소스 50% 절감 |

#### 한줄 요약
- Top-Level 코드 격리, PgBouncer 연동, K8s Pod 격리 실행, 파싱 주기 최적화로 안정성을 확보한다.

## Ⅶ. 결론

- 엔터프라이즈 배치 및 모던 데이터 플랫폼 워크플로 스케줄링의 가장 지배적인 표준 오케스트레이션 플랫폼으로 확립되었으며, 실무 운영 시에는 스케줄러 락업을 방지하는 Top-Level 무거운 연산 배제, 메타데이터 DB 커넥션 풀링(PgBouncer), 대규모 연산의 리소스 고립을 위한 `KubernetesPodOperator` 격리 실행, 지연 센서로 인한 슬롯 낭비를 제거하는 `deferrable=True` 비동기 트리거 최적화를 결합하여 수천 개 DAG 환경에서도 중단 없는 고가용성 파이프라인 지휘를 완성

#### 한줄 요약
- 데이터 파이프라인 오케스트레이션은 DAG 기반의 선후 의존성 제어와 자동 재시도, 백필을 통해 복잡한 데이터 흐름을 무결점으로 지휘하는 핵심 플랫폼이다.
