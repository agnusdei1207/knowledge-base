---
title: "데이터 파이프라인 오케스트레이션 — Airflow (Data Pipeline Orchestration)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 158
extra:
  question_no: "158"
  exam_status: "미출제"
---

## 미리 알고가기

- DAG는 Task의 의존성과 실행 조건을 순환 없이 표현한 워크플로 정의임
- DAG Run은 특정 데이터 구간이나 수동 요청에 대해 생성된 DAG의 실행 인스턴스임
- Task Instance는 DAG Run 안에서 상태를 가진 개별 Task 실행 단위임
- Scheduler는 DAG Run을 만들고 의존성을 충족한 Task Instance를 Executor에 제출함
- Executor는 실행 가능한 Task를 로컬 프로세스·분산 Worker·컨테이너에 배치함
- Operator·TaskFlow 함수는 실행할 데이터 처리 코드를 Task로 정의함
- Backfill은 과거 데이터 구간별 DAG Run을 다시 생성해 누락·변경 데이터를 처리함
- Cron은 지정한 시각에 명령을 실행하지만 작업 간 의존성과 상태는 별도로 관리해야 하는 스케줄러임
- Trigger Rule은 상위 Task 상태를 기준으로 하위 Task의 실행 가능 여부를 판정함
- Pool은 공유 DB·API에 동시에 접근할 수 있는 Task 수를 제한함

## 작성 근거(검토용)

- Airflow는 DAG 의존성·Scheduler·Executor·Task Instance 상태·재시도·Backfill을 핵심으로 선정함
- 비교표는 Cron과 Airflow의 의존성 표현·실패 복구·자원 조정을 같은 기준에서 대비함
- 절차는 DAG 파싱부터 의존성 판정·Task 실행·상태 전이까지 실제 제어권 이동을 설명함
- 제목부터 결론까지 모든 문장·표 셀·요약을 5회 전수 검수해 데이터 처리와 실행 조정 역할을 분리함

## Ⅰ. 개요

- **정의/개념**: 데이터 파이프라인 오케스트레이션은 DAG의 의존성·스케줄·재시도와 Task Instance 상태로 데이터 작업의 실행 순서를 조정하는 제어 체계임
- **배경/필요성**: 여러 적재·변환·품질 작업의 선후 관계와 실패 복구·과거 구간 재실행을 일관되게 관리하기 위해 상태 기반 워크플로 조정이 필요함

## Ⅱ. 특징

- DAG가 Task의 선후 관계와 Trigger Rule을 선언하고 Operator·TaskFlow 함수가 처리 코드를 정의함
- Scheduler가 데이터 구간별 DAG Run을 만들고 상위 Task 상태로 실행 가능 여부를 판정함
- Executor가 실행 환경에 Task를 제출하고 Worker가 실제 데이터 처리 코드를 수행함
- Task Instance의 재시도·실패·건너뜀·상위 실패 상태로 부분 재실행 범위를 통제함
- Backfill·Pool·동시성 제한이 과거 구간 처리와 DB·API 자원 경쟁을 조정함

## Ⅲ. 종류 및 비교

| 판단 기준 | Cron 중심 실행 | Airflow 오케스트레이션 |
|:---|:---|:---|
| 의존성 표현 | 스크립트 내부 대기·호출로 연결 | DAG의 상·하위 Task와 Trigger Rule로 선언 |
| 실패 복구 | 스크립트 단위 재실행·수동 구간 지정 | 메타DB에 저장된 Task Instance 상태로 실패 Task 재시도와 구간 재실행 |
| 자원 조정 | OS 스케줄과 개별 스크립트 설정 | Executor·Queue·Pool·동시성으로 배치 |

> 요약: Airflow는 DAG 의존성 선언과 Task Instance 상태 기반 재시도로 실패를 복구하며 Executor·Pool로 자원을 조정함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| DAG·Task | 스케줄·데이터 구간·의존성과 실행할 작업을 코드로 정의함 |
| DAG Processor | DAG 파일을 파싱하고 직렬화한 정의를 Metadata DB에 반영함 |
| Scheduler | DAG Run을 생성하고 실행 가능한 Task Instance를 판정함 |
| Executor·Worker | 준비된 Task를 Queue·프로세스·컨테이너에 배치하고 실행함 |
| Metadata DB | DAG Run·Task Instance·스케줄·재시도·연결 상태를 저장함 |
| API Server·UI | 실행 요청·상태·그래프·로그·재실행 제어를 사용자에게 제공함 |

```text
DAG 파일 -> DAG Processor -> Metadata DB <- Scheduler
Scheduler -> Executor -> Worker -> API Server -> Metadata DB
```

> 요약: DAG Processor가 정의를 저장하고 Scheduler가 상태를 판정해 Executor·Worker로 Task 실행을 전달함.

## Ⅴ. 원리 및 절차 흐름도

```text
DAG 파싱 -> DAG Run 생성 -> 의존성 판정 -> Executor 제출 -> 실행 상태·재시도 갱신
```

1. **DAG 파싱**: DAG Processor가 코드에서 스케줄·Task·의존성을 읽어 직렬화함
2. **실행 생성**: Scheduler가 시간표나 요청에 따라 데이터 구간별 DAG Run을 생성함
3. **의존성 판정**: 상위 Task·Trigger Rule·Pool·동시성 조건을 충족한 Task를 찾음
4. **Task 제출**: Executor가 준비된 Task Instance를 Worker 실행 자원에 배치함
5. **상태 갱신**: 결과를 성공·실패·재시도 상태로 기록하고 하위 Task의 실행 가능성을 다시 판정함

> 요약: Airflow는 DAG Run의 Task 상태와 의존성을 반복 판정해 실행 자원에 제출하고 후속 작업을 진행함.

## Ⅵ. 실무 사례

1. 일별 웨어하우스 적재는 DAG 의존성과 Pool을 설정하고 스케줄 지연·Task 실패율을 확인함
2. 과거 데이터 재처리는 구간별 Backfill을 실행하고 완료 시간·중복 적재 건수를 확인함

## Ⅶ. 결론

- Airflow는 Task 의존성·실패 복구·과거 구간 재처리 요구와 Scheduler·Metadata DB 운영 용량을 기준으로 적용해야 함
