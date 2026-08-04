---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Apache Spark"
date: "2026-08-04T13:17:00+09:00"
tags:
  - "notes-software"
weight: 117
extra:
  question_no: "117"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "120회 기출 후 저빈도, 인메모리 처리 정본"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **Apache Spark 분산 처리 엔진**: 방향성 비순환 그래프(Directed Acyclic Graph, DAG)로 작업 의존성을 구성하고 파티션별 태스크를 메모리 중심으로 병렬 실행하는 엔진이다.

</details>

- 정의/개념: 연산을 **DAG** 로 계획하는 **Apache Spark 분산 처리 엔진**
- 배경/필요성: MapReduce의 단계별 디스크 기록은 반복 분석마다 **입출력 지연** 유발

#### 한줄 요약
- 계산을 작업 그래프로 묶고 자주 쓰는 중간 자료를 재사용하는 엔진이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **DAG 스케줄링**: 셔플 경계를 기준으로 작업을 Stage와 Task로 나누어 실행하는 특성이다.
- **지연 실행(Lazy Evaluation)**: 변환을 즉시 수행하지 않고 Action이 호출될 때 전체 실행 계획을 구성하는 방식이다.
- **Catalyst**: 논리•물리 실행 계획을 규칙과 비용으로 최적화하는 기능이다.
- **적응형 질의 실행(Adaptive Query Execution, AQE)**: 실행 통계로 조인•파티션 계획을 보정하는 기능이다.

</details>

- **지연 실행**: Action에서 계산 시작
- **DAG 스케줄링**: 셔플 경계로 Stage 분할
- **계획 보정**: Catalyst•AQE 기반 실행 최적화

#### 한줄 요약
- 반복 분석은 빠르지만 파티션 쏠림과 메모리 상태 등을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **Driver**: 응용의 실행 계획과 Job을 구성하는 구성요소이다.
- **SparkSession**: 데이터프레임과 SQL 처리 기능의 진입점이다.
- **Scheduler**: Job을 Stage와 Task로 나누는 구성요소이다.
- **Cluster Manager**: 실행 자원을 Executor에 할당하는 구성요소이다.
- **Executor**: 태스크와 캐시 및 셔플 연산을 실행하는 프로세스이다.
- **Partition**: 하나의 Task가 처리하는 분산 데이터 조각이다.
- **Checkpoint**: 스트림 진행 위치와 상태를 영속화한 복구 지점이다.
- **State Store**: 스트림의 키별 상태를 저장하는 구성요소이다.

</details>

```mermaid
block-beta
  columns 3
  A["Spark 실행 경계"]:3
  D["Driver•SparkSession"]
  C["Catalyst•AQE"]
  S["Scheduler•Cluster Manager"]
  E["Executor•Partition"]
  P["Checkpoint•State Store"]
  D --- C
  D --- S
  S --- E
  E --- P
```

| 구성요소 | 책임 |
|:---|:---|
| Driver•SparkSession | **계획•Job** 조정 |
| Catalyst•AQE | **계획 최적화•보정** |
| Scheduler•Cluster Manager | **Stage•Task•자원** 할당 |
| Executor•Partition | **태스크•캐시•셔플** 실행 |
| Checkpoint•State Store | **진행 위치•상태** 복구 |

#### 한줄 요약

- 계획자, 최적화 담당자, 작업 배정자, 실행자, 복구 저장소로 구성된다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **5. 실행 통계**: 실제 행 수와 셔플량을 AQE에 전달해 실행 계획을 조정하는 정보이다.
- **1. Catalyst 논리 계획**: Driver가 지연 연산을 최적화 가능한 논리 그래프로 구성한 계획이다.
- **2. AQE 최적 계획**: 실행 중 통계로 조인 방식과 파티션 수를 다시 선택한 계획이다.
- **3. DAG•Stage 구성**: 셔플 경계를 기준으로 실행 단계를 나누는 단계이다.
- **4. 파티션 Task**: Driver가 Executor에 배치하는 파티션 단위 작업이다.

</details>

```mermaid
sequenceDiagram
    participant U as 응용 프로그램
    participant D as Driver
    participant E as Executor
    U->>D: 변환•액션 제출
    D->>D: 1. Catalyst 논리 계획
    D->>D: 2. AQE 최적 실행 계획
    D->>D: 3. DAG•Stage 구성
    D->>E: 4. 파티션 Task
    E-->>D: 5. 실행 통계
```

**동작 원리**

1. **Catalyst 논리 계획**: Driver가 지연 연산을 논리 그래프로 구성
2. **AQE 최적 실행 계획**: 실행 통계에 맞춰 조인•스캔 방식 선택
3. **DAG•Stage 구성**: Driver가 셔플 경계별 실행 단계 생성
4. **파티션 Task**: Driver가 Executor에 파티션 작업 배치
5. **실행 통계**: Executor가 Driver에 행 수•셔플량 전달

#### 한줄 요약

- 계산표를 먼저 최적화하고 셔플 경계로 나눠 여러 실행자에게 맡긴 뒤 실제 크기로 계획을 보정한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **데이터프레임 응용 프로그램 인터페이스(DataFrame Application Programming Interface, DataFrame API)**: 스키마가 있는 분산 데이터를 표 형태 연산으로 다루는 접점이다.
- **Structured Streaming**: DataFrame API로 연속 입력을 증분 처리하고 상태를 관리하는 방식이다.
- **Spark Batch**: DAG와 캐시로 반복•복합 일괄 분석을 처리하는 방식이다.
- **SQL 처리**: SQL로 구조화된 분산 데이터를 분석하는 방식이다.
- **Hadoop MapReduce**: 파일 기반 Map•Shuffle•Reduce 단계를 디스크에 기록하며 대형 단순 배치를 처리하는 엔진이다.
- **입출력(Input/Output, I/O)**: 디스크나 네트워크에서 데이터를 읽고 쓰는 연산이다.

</details>

| Spark 처리 방식 | Spark Batch•SQL | Structured Streaming | Hadoop MapReduce |
|:---|:---|:---|:---|
| 적용 기준 | **반복•복합 배치** | **연속 증분 처리** | **대형 단순 배치** |
| 핵심 특징 | **DAG•SQL•캐시** | **Micro-batch•상태** | **파일 기반 단계 실행** |
| 한계 | **메모리•셔플•편향** | **상태•늦은 이벤트** | **디스크 I/O•시작 지연** |

#### 한줄 요약

- Spark는 계산 그래프를 이어 실행하고 필요한 중간 자료만 캐시해 반복 작업을 줄인다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **입력량 기반 파티션 조정**: 파티션 크기를 데이터 양에 맞추는 활동이다.
- **코어 기반 파티션 조정**: 병렬 자원 수에 맞춰 파티션 수를 정하는 활동이다.
- **셔플량 기반 파티션 조정**: 네트워크 이동량에 맞춰 파티션 수를 정하는 활동이다.
- **키 분할**: 편향 키를 보조 키로 나눠 여러 파티션에 배치하는 통제이다.
- **사전 집계**: 셔플 전에 같은 키의 값을 부분 집계하는 통제이다.
- **재사용 비용**: 캐시 데이터가 반복 연산을 줄이는 이익이다.
- **재계산 비용**: 캐시 없이 계보를 따라 결과를 다시 만드는 비용이다.
- **필터 설계**: 조인 전에 불필요한 행과 열을 제거하는 방식이다.
- **브로드캐스트 설계**: 작은 입력을 실행 노드마다 복제하는 조인 방식이다.
- **분할 설계**: 큰 입력의 키 배치를 맞춰 셔플을 줄이는 방식이다.
- **워터마크(Watermark)**: 늦은 이벤트를 허용할 시간 경계이다.
- **키 유효 시간(Time To Live, TTL)**: 키별 상태를 유지한 뒤 만료할 기간이다.
- **상태 지표**: State Store의 크기와 처리량을 나타내는 관측값이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파티션 수가 코어•입력량과 불균형 | **입력•코어•셔플량 기반 파티션 조정** | **유휴•스케줄 비용** 감소 |
| 일부 키에 조인•집계 레코드 집중 | **AQE•키 분할•사전 집계** | **느린 Task** 완화 |
| 재사용 없는 데이터가 메모리 점유 | **재사용•재계산 비용 기반 캐시 결정** | **메모리 압박** 방지 |
| 대형 조인으로 네트워크•디스크 포화 | **필터•브로드캐스트•분할 설계** | **셔플 부하** 감소 |
| 워터마크 없이 키별 상태 누적 | **워터마크•TTL•상태 지표** | **상태 무한 증가** 방지 |

#### 한줄 요약

- 평균 작업시간보다 가장 늦은 파티션과 셔플•상태 크기를 보고 병목을 고친다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **Spark Batch**: 반복 계산과 복합 배치 분석에 DAG•SQL•캐시를 활용하는 처리 방식이다.

</details>

- 반복 배치는 **Spark Batch**, 연속 증분 처리는 **Structured Streaming** 선택

#### 한줄 요약

- 작업 그래프가 좋아도 한 파티션이나 상태가 커지면 느려지므로 실제 실행량을 보고 조정한다.
