---
title: "Apache Spark"
date: "2026-07-13T23:00:00+09:00"
tags:
  - "cspe-software"
weight: 134
extra:
  question_no: "134"
  exam_status: "기출"
  exam_history: "120회"
---

## 미리 알고가기

- Spark는 변환 연산의 의존성을 DAG로 구성하고 파티션별 Task를 Executor에서 병렬 실행하는 분산 처리 엔진임
- Transformation은 지연 평가되며 Action이 호출될 때 Driver가 Job·Stage·Task 실행 계획을 생성함
- DataFrame·SQL 질의는 Catalyst가 논리 계획을 최적화하고 AQE가 실행 중 통계로 물리 계획을 조정함
- Cache·Persist는 반복 사용 데이터를 재활용하지만 메모리가 부족하면 축출·디스크 저장·재계산이 발생함
- Structured Streaming은 DataFrame API로 연속 입력을 증분 처리하며 체크포인트와 상태 저장소로 복구를 지원함

## 작성 근거(검토용)

- Spark는 DAG 실행, Catalyst·AQE 최적화, 메모리·Shuffle 관리와 스트림 상태 복구를 핵심 축으로 설명함
- 비교표는 MapReduce와 Spark의 실행 그래프·반복 처리·적합 작업을 대비함
- 실무 사례는 편향 조인과 상태 기반 스트림 집계를 Shuffle 전송량·최장 Task 시간·복구 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: Apache Spark는 변환 연산을 DAG로 구성하고 파티션별 Task를 Executor에서 실행하며 구조화 질의와 스트림을 같은 실행 엔진으로 처리하는 분산 컴퓨팅 플랫폼임
- **배경/필요성**: 여러 MapReduce Job 사이의 디스크 기록과 반복 입력 읽기를 줄이고 SQL·반복 분석·스트림 처리를 하나의 분산 실행 모델로 운영하기 위해 필요함

### 쉽게 이해하기 (학습용)
- 여러 계산을 하나의 작업 그래프로 묶고 자주 쓰는 중간 자료를 재사용하는 분산 처리 엔진임

## Ⅱ. 특징

- Transformation을 지연 평가하고 Action 호출 시 의존성을 Job·Stage·Task로 변환함
- Shuffle이 필요한 넓은 의존성에서 Stage를 나누고 파티션별 Task를 Executor에 배치함
- Catalyst가 DataFrame·SQL의 논리 계획을 최적화하고 AQE가 실행 통계로 조인·파티션 계획을 조정함
- Cache·Persist와 계보(Lineage) 재계산으로 반복 처리와 장애 복구를 지원하지만 Shuffle·데이터 편향·메모리 압박은 성능 저하 요인임
- Structured Streaming이 체크포인트·상태 저장소·워터마크로 상태 기반 증분 처리를 관리함

### 쉽게 이해하기 (학습용)
- 반복 분석은 빠르지만 파티션 쏠림·Shuffle·메모리와 큰 상태를 관리해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Hadoop MapReduce | Apache Spark |
|:---|:---|:---|
| 실행 그래프 | Map·Shuffle·Reduce 단계의 Job을 연결 | 연산 의존성을 DAG의 Job·Stage·Task로 구성 |
| 반복 처리 | 이전 Job 출력을 다시 읽어 다음 Job 실행 | Cache·Persist한 파티션을 반복 연산에 재사용 |
| 적합 작업 | 파일 기반 대용량 일괄 정렬·집계 | SQL·반복 분석·상태 기반 스트림 처리 |

> 요약: MapReduce는 Job 사이 결과를 파일로 연결하고, Spark는 DAG·Cache·Catalyst로 반복 분석과 구조화 처리를 통합함.

### 쉽게 이해하기 (학습용)
- MapReduce는 단계마다 파일을 넘기고 Spark는 작업 그래프와 재사용 자료로 이어 계산함

## Ⅳ. 설계 요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Driver·SparkSession | 응용 진입점에서 Job을 생성하고 전체 실행을 조정함 |
| Catalyst·AQE | 논리 계획을 최적화하고 실행 통계로 물리 계획을 조정함 |
| DAG Scheduler·Task Scheduler | Shuffle 경계로 Stage를 나누고 파티션별 Task를 Executor에 배치함 |
| Cluster Manager | Standalone·YARN·Kubernetes 환경에서 Executor 자원을 할당함 |
| Executor·Partition | Task를 실행하고 파티션 데이터·Cache·Shuffle 블록을 관리함 |
| Checkpoint·State Store | 스트림 진행 위치와 상태를 저장해 재시작 시 처리를 복구함 |

```text
Action -> Driver 실행 계획 -> Stage·Task -> Executor 파티션 처리 -> 결과
                              └-> Shuffle·Cache·State Store
```

> 요약: Driver가 최적화된 DAG를 Stage·Task로 나누고 Executor가 파티션·Shuffle·상태를 처리함.

### 쉽게 이해하기 (학습용)
- 지휘자, 질의 최적화기, 작업 그래프 스케줄러와 여러 실행 작업자로 구성됨

## Ⅴ. 원리 및 절차 흐름도

```text
Transformation 정의 -> Action 호출 -> 논리·물리 계획 최적화 -> Stage·Task 실행 -> 결과 반환
```

1. **Transformation 정의**: DataFrame·RDD에 필터·조인·집계 등 지연 연산을 구성함
2. **Action 호출**: 결과 조회·저장 요청이 들어오면 Driver가 Job 생성을 시작함
3. **계획 최적화**: Catalyst가 질의 계획을 변환하고 AQE가 실행 통계로 물리 계획을 보정함
4. **Stage·Task 실행**: Shuffle 경계별 Stage와 파티션별 Task를 Executor에 분배함
5. **결과 반환**: Executor가 Shuffle·Cache·상태 저장을 거쳐 결과를 Driver나 저장소에 전달함

> 요약: Action이 지연 연산을 실행 계획으로 확정하면 Driver가 Stage·Task를 배치하고 Executor가 파티션을 처리함.

### 쉽게 이해하기 (학습용)
- Action이 그래프를 확정하면 Shuffle 경계로 Stage를 나눠 파티션별 Task를 실행함

## Ⅵ. 실무 사례

1. 편향 조인은 AQE와 파티션 재분배를 적용하고 Shuffle 전송량·최장 Task 시간을 확인함
2. 상태 기반 스트림 집계는 워터마크·체크포인트를 적용하고 상태 저장소 크기·재시작 시간을 확인함

### 쉽게 이해하기 (학습용)
- 편향 조인과 상태 스트림에서 가장 느린 Task·Shuffle 양·복구 시간을 확인함

## Ⅶ. 결론

- Spark는 반복 처리·구조화 질의·상태 기반 스트림 요구에 맞춰 DAG·파티션·Shuffle·상태 복구 방식을 설계해야 함
- 메모리 내 처리만 강조하지 말고 데이터 편향·Shuffle·상태 증가와 재계산 비용을 실측해 조정해야 함

### 쉽게 이해하기 (학습용)
- 작업대 확장보다 한 작업자에게 일이 몰리는 데이터 편향과 과도한 Shuffle을 먼저 확인함
