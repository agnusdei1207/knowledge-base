---
title: "데이터 파이프라인 오케스트레이션 - Airflow (Data Pipeline Orchestration)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 158
---

# 📖 【암기용】 개념 완전 이해

> 목적: 데이터 파이프라인 오케스트레이션을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: **워크플로우 오케스트레이션**(Workflow Orchestration) — 여러 데이터 작업(Task)의 실행 순서·의존성·일정을 **DAG**(방향성 비순환 그래프)로 정의하고, 실행 상태와 실패 복구를 통제하는 체계
- **왜 필요한가**: 추출→검증→변환→적재처럼 순서가 틀리면 결과가 깨지는 작업을 Cron만으로 돌리면 의존성을 "시간 간격 추정"으로만 관리하게 되어, 앞 작업이 늦어지면 뒤 작업이 미완성 데이터를 참조하는 사고가 난다. 오케스트레이션은 이 의존성을 코드로 명시하고 실패 시 자동으로 재시도·알림한다.
- **핵심 직관**: 공항 관제탑처럼, 비행기(작업) 하나하나의 이착륙 순서·활주로 배정·지연 시 재조정을 중앙에서 관제한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 워크플로우 오케스트레이션 | 작업 순서·의존성·일정·실패복구를 코드로 관리하는 상위 개념 | 관제탑의 항공 스케줄 총괄 |
| DAG (방향성 비순환 그래프) | Task 간 의존관계를 순환 없이 방향으로 표현한 그래프 | "A 끝나야 B 시작"을 그린 순서도 |
| Task / Operator | DAG를 구성하는 개별 작업 단위 / 그 작업의 실행 로직을 담은 템플릿(PythonOperator 등) | 순서도의 한 칸 / 그 칸의 작업 매뉴얼 |
| Scheduler | DAG를 주기적으로 읽어 실행 시점이 된 Task를 큐에 올리는 프로세스 | 스케줄표를 보고 이륙 시간을 알리는 관제사 |
| Executor / Worker | 큐에 올라온 Task를 실제로 실행하는 주체(단일 프로세스 또는 분산 노드) | 관제 지시를 받아 실제 유도하는 지상 요원 |
| Metadata DB | DAG 실행 이력, Task 상태, 로그를 저장하는 저장소 | 관제 기록 로그북 |
| Retry / Backoff | 실패한 Task를 정해진 횟수·간격으로 재시도 | 이륙 실패 시 재점검 후 재시도 |
| Backfill | 과거 특정 기간에 대해 DAG를 소급 실행 | 결항된 과거 편을 뒤늦게 재운항 |
| SLA | Task/DAG가 완료돼야 하는 기한 | "이 시간까지는 끝나야 한다"는 약속 |
| 멱등성 (Idempotency) | 같은 Task를 여러 번 실행해도 결과가 같도록 보장하는 성질 | 몇 번 눌러도 결과가 같은 리모컨 버튼 |

## 깊이 이해

### 왜 Cron이 아니라 오케스트레이션이 필요했나 (배경)
- Cron은 "몇 시 몇 분에 실행"만 알 뿐 앞 작업의 성공 여부를 모른다. 예: `extract_orders`가 보통 5분 만에 끝난다고 가정해 `transform_sales`를 5분 뒤로 걸어둬도, 그날따라 extract가 20분 걸리면 transform은 미완성 데이터를 읽는다.
- Airflow는 이 관계를 "시간"이 아니라 "완료 이벤트"로 정의한다 — extract의 Task 상태가 success가 되어야 transform이 트리거된다. 2014년 Airbnb가 사내 배치 난립 문제를 해결하려 만들었고, 이후 Apache 프로젝트로 표준화됐다.

### DAG 실행 흐름을 수치로 추적하기
- DAG: `extract_orders(5분) → dq_check(2분) → transform_sales(10분) → publish_mart(3분)`, `schedule_interval="0 6 * * *"`(매일 06:00 실행)라고 하자.
- 06:00 extract 시작 → 06:05 완료 → dq_check 시작 → 06:07 완료(정상 시) → transform 시작 → 06:17 완료 → publish 시작 → 06:20 완료. 전체 20분 소요.
- dq_check가 실패하면 이후 transform·publish는 실행되지 않고 파이프라인이 멈춘다 — 나쁜 데이터가 마트까지 전파되는 것을 막는 핵심 지점이다.

### Retry와 Backfill을 수치로 이해하기
- `retries=2, retry_delay=5분`이면 최초 실패 → 5분 뒤 1차 재시도 → 또 실패 → 5분 뒤(또는 exponential backoff면 10분 뒤) 2차 재시도 → 그래도 실패하면 최종 실패로 기록하고 Slack 알림.
- Backfill: DAG를 3월 1일에 새로 배포했는데 `start_date`를 2월 1일로 설정하면, `catchup=True`일 때 스케줄러가 2/1~2/28까지 28회분을 소급 실행한다. 과거 데이터 보정이나 로직 변경 후 재계산에 쓴다.

### Executor 종류에 따른 처리량 차이
- LocalExecutor는 한 서버 안에서 코어 수만큼 병렬 실행하고, CeleryExecutor·KubernetesExecutor는 여러 워커 노드로 분산해 수백~수천 Task를 동시에 처리한다. 하루 Task 수가 30개 수준이면 LocalExecutor로 충분하지만, 수백 개 이상이면 분산 Executor가 필요하다.

### 흔한 오해
- Airflow 자체는 데이터를 변환하지 않는다. `transform_sales` Task는 내부적으로 Spark job이나 SQL을 호출만 할 뿐, 대용량 연산은 외부 엔진이 수행한다. Airflow는 제어(control plane), Spark/SQL은 처리(data plane)로 역할이 분리된다.

## 연결 개념
- ETL/ELT 파이프라인 — 오케스트레이션이 순서를 통제하는 대상 작업
- 데이터 품질 관리 — DAG 중간의 dq_check 같은 검증 단계
- 데이터 계보(Lineage) — DAG 실행과 변환 의존성의 기록

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 오케스트레이션 답안은 DAG, scheduler, executor, retry, SLA, backfill, 관측 지표를 작업 제어 관점으로 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 파이프라인 오케스트레이션은 작업 의존성, 일정, 실행 상태, 재시도, 알림을 DAG 기반으로 관리하는 체계임.
> 2. **가치**: 크론 배치의 의존성 누락과 장애 복구 공백을 줄이고 task 성공률, SLA miss, retry count를 지표화함.
> 3. **판단 포인트**: Airflow는 제어 plane이고 Spark/DBT/SQL 엔진은 처리 plane이므로 역할 분리를 명확히 해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 배치 운영 구조 이해 확인 | DAG, scheduler, executor, metadata DB | Airflow를 변환 엔진으로 설명 |
| 장애 복구 판단 확인 | retry, backfill, alert, SLA | 실행 순서만 서술 |
| 운영 지표 확인 | task success rate, SLA miss, duration | 관측 지표 누락 |

> 요약: 오케스트레이션 문제는 작업 순서와 장애 복구를 코드와 지표로 관리하는 구조가 핵심임.

---

## Ⅰ. 개요 및 필요성

- 개요: 오케스트레이션은 데이터 작업 실행 제어 체계임.
- 배경: 데이터 파이프라인은 다수 작업의 순서와 성공 조건에 의존한다.
- 필요성: Airflow의 DAG 기반 일정, 의존성, 재시도, 알림, backfill로 배치 실행 기준을 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
DAG Code -> Scheduler -> Executor/Worker -> Task Operator -> Metadata DB/UI
                     +-> Alert/SLA
                     +-> External Engine
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DAG | 작업과 의존성 정의 | Python code, schedule |
| Scheduler | 실행 시점과 task 상태 계산 | catchup, SLA |
| Executor/Worker | task 실행 분산 | Celery, Kubernetes |
| Metadata DB/UI | 상태, 로그, 이력 조회 | retry, duration 추적 |

> 요약: Airflow는 DAG 정의, 스케줄링, 실행 분배, 상태 저장의 구성요소로 파이프라인을 제어함.

---

## Ⅲ. 동작원리 및 흐름도

```text
DAG 파싱 -> 실행 일정 계산 -> task 큐잉 -> worker 실행 -> 상태 기록 -> 알림/backfill
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DAG 파일 파싱과 dependency 확인 | parse error 0건 |
| 2 | schedule interval과 catchup 계산 | 예정 실행 누락 0건 |
| 3 | task 큐잉과 worker 할당 | queue delay 1분 이하 |
| 4 | 성공/실패 상태와 로그 기록 | task success rate 99% |
| 5 | 실패 retry, alert, backfill 수행 | SLA miss 1% 이하 |

> 요약: 오케스트레이션은 DAG 파싱부터 실패 복구까지 상태 기반으로 제어됨.

---

## Ⅳ. 특징

| 구분 | Cron 배치 | Airflow 오케스트레이션 | 판단 포인트 |
|:---|:---|:---|:---|
| 의존성 | 시간 기반 추정 | DAG 기반 명시 | dependency 누락 |
| 복구 | 수동 재실행 | retry/backfill | 재처리 시간 |
| 관측 | 로그 파일 분산 | UI/metadata DB | duration, SLA |
| 한계 | 구조 단순 | DAG 복잡도 관리 필요 | task 수, parse time |

> 요약: Airflow는 작업 의존성과 복구를 명시하지만 DAG 설계와 메타DB 운영이 필요함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Cron, shell script | DAG 기반 Airflow | task 30개 이상 |
| 비용/처리 | 단일 서버 | worker 분산 실행 | 동시 실행 수 |
| 운영/위험 | 실패 추적 어려움 | retry, alert, SLA | SLA miss 관리 필요 |

> 요약: 작업 수와 의존성이 증가하면 Cron보다 Airflow 기반 DAG 관리가 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| DAG 폭증 | 과도한 세분화 | domain별 DAG, naming rule | DAG parse time |
| 재처리 오류 | 멱등성 미확보 | idempotent task, partition overwrite | duplicate 0건 |
| 메타DB 병목 | task instance 증가 | DB 튜닝, log retention | scheduler lag |

> 요약: 오케스트레이션 리스크는 DAG 복잡도와 멱등성 부족이며 설계 규칙과 상태 지표로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 실행 | task success rate 99% 이상 | Airflow metadata |
| 일정 | SLA miss 1% 이하 | SLA callback log |
| 복구 | retry 후 성공률 95% 이상 | retry history |

> 요약: Airflow 운영은 성공률, SLA miss, retry 후 성공률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. DAG 표준화: extract, validate, transform, publish task naming과 owner, retry, SLA 필수값을 코드 리뷰 기준으로 지정
2. 멱등 처리: partition 단위 overwrite, merge key, checkpoint를 적용해 backfill 시 duplicate 0건 보장
3. 관측 운영: task success 99%, SLA miss 1%, queue delay 1분 이하를 Airflow UI와 Prometheus로 점검

**결론 (2줄):**
- 기술사 판단: 단순 1~2개 배치는 Cron, 의존성 30개 이상과 재처리 요구가 있으면 Airflow를 선택함
- 향후 방향: 오케스트레이션은 데이터 품질, 계보, 데이터 계약 검증과 결합되어 파이프라인 신뢰 제어점이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Airflow를 설명하시오" | DAG 파싱부터 알림까지 흐름 | Cron과 Airflow 비교 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "설계하시오" | retry, backfill, SLA, 멱등 흐름 | task 지표와 장애 대응 기준 |

> 요약: 설명형은 구성 원리, 운영형은 재처리와 SLA 지표를 중심으로 전환함.
