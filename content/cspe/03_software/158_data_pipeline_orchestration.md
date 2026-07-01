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
- **개요**: 데이터 작업의 순서, 의존성, 일정, 재시도, 알림을 관리하는 실행 제어 체계
- **왜 필요한가**: 추출, 변환, 품질 검사, 적재, 리포트 갱신 작업은 순서가 틀리면 데이터가 깨진다. 오케스트레이션은 작업 그래프를 기준으로 실행과 실패 복구를 통제한다.
- **핵심 직관**: 공항 관제처럼 비행기 출발 순서, 활주로, 지연, 재출발을 조정하는 역할이다.

## 깊이 이해
- **배경·문제의식**: 크론으로 배치를 돌리면 의존성, 재시도, backfill, 알림, SLA 추적이 흩어진다. Airflow는 DAG로 작업 관계를 코드화하고 scheduler, executor, metadata DB로 실행 상태를 관리한다.
- **작동 원리**: DAG에 task와 dependency를 정의하면 scheduler가 실행 시점을 계산한다. executor는 worker에 작업을 분배하고, 실패 시 retry와 alert를 수행하며, metadata DB는 task 상태와 로그를 보관한다.
- **비유**: 요리 코스 진행표와 같다. 육수 끓이기 후 소스 만들기, 재료 손질 후 조리처럼 순서를 지키고 실패하면 다시 처리한다.
- **구체 예시**: `extract_orders -> dq_check -> transform_sales -> publish_mart` DAG에서 DQ 실패 시 mart 적재를 중단하고 Slack 알림, retry 2회, SLA 06:00 기준을 적용한다.
- **흔한 오해·주의점**: Airflow는 데이터 처리 엔진이 아니다. Spark, SQL, Python 작업을 호출하고 조정하는 도구이며 대용량 변환 자체는 외부 엔진이 수행한다.

## 연결 개념
- ETL/ELT 파이프라인 - 오케스트레이션 대상 작업
- 데이터 품질 관리 - DAG 중간 검증 단계
- 데이터 계보 - DAG 실행과 변환 의존성 기록

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

오케스트레이션은 데이터 작업 실행 제어 체계임. 데이터 파이프라인은 다수 작업의 순서와 성공 조건에 의존한다. Airflow는 DAG 기반으로 일정, 의존성, 재시도, 알림, backfill을 관리한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
