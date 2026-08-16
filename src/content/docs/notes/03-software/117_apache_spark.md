---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Apache Spark"
date: "2026-08-13T22:17:00+09:00"
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

<details><summary>용어 설명</summary>

- **Apache Spark**: 기존 MapReduce의 디스크 I/O 병목을 극복하기 위해 인메모리(In-Memory) 기반 RDD(Resilient Distributed Dataset) 및 DAG(Directed Acyclic Graph) 실행 엔진을 활용하여, 배치 및 스트리밍 연산을 최대 100배 빠르게 연산하는 2세대 분산 데이터 처리 엔진.
- **RDD (Resilient Distributed Dataset)**: 장애 발생 시 계보(Lineage) 추적을 통해 메모리상에서 즉시 복원 가능한, 불변(Immutable) 분산 데이터 집합.
- **DAG Engine (방향성 비순환 그래프)**: 연산 과정(Transformation)을 순과정이 없는 방향 그래프로 묶어 두었다가, 최적의 실행 경로(Stage)로 나누어 연산하는 최적화 엔진.

</details>

- 정의/개념: DAG 실행과 중간 결과 재사용을 제공하는 **Apache Spark**
- 배경/필요성: 단계별 디스크 물질화는 **반복 연산•대화형 분석 지연** 유발

#### 한줄 요약

- 계산을 작업 그래프로 묶고 자주 쓰는 중간 자료를 재사용하는 엔진이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lazy Evaluation (지연 연산)**: Action(예: `count()`, `collect()`) 구문이 호출되기 전까지는 실제 연산을 수행하지 않고 DAG 최적화 그래프만 축적하는 특성.
- **Catalyst Optimizer**: SQL 및 DataFrame 연산을 논리적/물리적 계획(Logical/Physical Plan)으로 자동 튜닝해 주는 내부 쿼리 최적화 엔진.

</details>

- **In-Memory Computing (RAM 중심의 RDD / DataFrame 연산)**
- **Lazy Evaluation (Transformation 지연 연산 & Action 시점 최적화 실행)**
- **Catalyst Optimizer & AQE (Adaptive Query Execution 동적 쿼리 최적화)**

#### 한줄 요약

- 반복 분석은 빠르지만 파티션 쏠림과 메모리 상태 등을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Driver vs Executor**: Driver는 main() 함수를 실행하며 DAG 맵을 짜고 Task를 배정하는 마스터, Executor는 각 노드 메모리상에서 Task를 실행하고 결과를 리턴하는 일꾼.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Apache Spark Architecture                       │
├────────────────────────────────────────────────────────────────────────┤
│ [Driver Program (SparkSession / Catalyst Optimizer / DAG Scheduler)]   │
│                                │ (Task Dispatch)                       │
│        ┌───────────────────────┼───────────────────────┐               │
│        ▼                       ▼                       ▼               │
│  [Executor Node 1]      [Executor Node 2]      [Executor Node 3]       │
│  (RAM RDD Task 1, 2)    (RAM RDD Task 3, 4)    (RAM RDD Task 5, 6)     │
├────────────────────────────────────────────────────────────────────────┤
│ Spark Ecosystem: Spark SQL | Spark Streaming | MLlib | GraphX          │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Driver가 Catalyst 및 DAG 스케줄러를 통해 연산을 최적화하고, Cluster Manager를 거쳐 각 Executor 노드의 RAM 파티션으로 Task를 분산 전파하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Driver | 앱 제어•DAG 생성•태스크 결과 관리 |
| Catalyst•AQE | 논리•물리 계획과 실행 중 재최적화 |
| DAG Scheduler | 셔플 경계로 Stage•Task 분할 |
| Cluster Manager | Executor 자원 요청•할당 |
| Executor | 파티션 연산•캐시•셔플 데이터 처리 |

#### 한줄 요약

- 계획자, 최적화 담당자, 작업 배정자, 실행자, 복구 저장소로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BroadCast Hash Join**: 대용량 테이블과 소용량 테이블 조인 시, 소용량 테이블을 모든 Executor 메모리에 복제(Broadcast)하여 Shuffle I/O 0회로 조인하는 기법.

</details>

```text
[DataFrame•SQL]
      │
      ▼
1. 논리 계획 분석
      │
      ▼
2. 논리 계획 최적화
      │
      ▼
3. 물리 계획 선택
      │
      ▼
4. Stage•Task 실행
      │
      ▼
5. 실행 계획 보정
```

### 동작 원리

1. 논리 계획 분석: 카탈로그로 열•타입•함수 해석
2. 논리 계획 최적화: 필터 푸시다운•열 가지치기 적용
3. 물리 계획 선택: 비용으로 조인•셔플 전략 결정
4. Stage•Task 실행: 셔플 경계별 파티션 작업 수행
5. 실행 계획 보정: 실제 통계로 파티션•조인 방식 조정

#### 한줄 요약

- 계산표를 먼저 최적화하고 셔플 경계로 나눠 여러 실행자에게 맡긴 뒤 실제 크기로 계획을 보정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Transformation vs Action**: Transformation(`map`, `filter`, `groupBy`)은 지연 연산으로 DAG 구성, Action(`select`, `collect`, `save`)은 연산 즉시 실행.

</details>

| 연산 분류 (Operation) | 주요 메소드 종류 | 실행 특성 및 메커니즘 |
|:---|:---|:---|
| Narrow Transformation | **`map()`, `filter()`, `flatMap()`** | **1:1 파티션 맵핑 (Shuffle 없음, 초고속)** |
| Wide Transformation | **`groupBy()`, `join()`, `distinct()`** | **N:M 파티션 맵핑 (Shuffle 디스크/네트워크 I/O 발생)** |
| Action | **`collect()`, `count()`, `saveAsTextFile()`** | **DAG 지연 연산을 확정 짓고 실제 Executor 가동** |

#### 한줄 요약

- Spark는 계산 그래프를 이어 실행하고 필요한 중간 자료만 캐시해 반복 작업을 줄인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Data Skew Salting**: 특정 Key에 파티션 데이터가 몰려 Executor OOM 발생 시, Key 뒤에 임의 숫자(Salting)를 붙여 균등 수평 분산시키는 튜닝 기법.

</details>

| 실무 장애 및 병목 | 발생 원인 | 해결 대책 및 튜닝 파라미터 |
|:---|:---|:---|
| Driver OOM (Out Of Memory) | `collect()` 호출로 거대 데이터가 Driver 몰림 | **`collect()` 사용 금지, `take()` 또는 파일 저장** |
| Executor Data Skew OOM | 특정 Key 파티션 데이터 폭발 | **Salting 적용 및 Broadcast Hash Join 전환** |
| Garbage Collection (GC) 지연 | RDD 객체 생성 과다로 Java GC 병목 | **Kryo Serializer 적용 및 DataFrame API 전환** |

> 사례: **카카오 / 당근마켓 EMR Spark Cluster & Databricks Lakehouse 빅데이터 분석**

#### 한줄 요약

- 평균 작업시간보다 가장 늦은 파티션과 셔플•상태 크기를 보고 병목을 고친다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Spark 아키텍처 수립 기준(Apache Spark Standards)**: In-Memory RDD 튜닝, Catalyst/AQE 최적화, Data Skew Salting 및 Structured Streaming 수용성에 의거한 체계.

</details>

- 반복•복합 분석은 **Spark**, 단순 대형 배치는 MapReduce 선택

#### 한줄 요약

- Spark 처리 방식 선택 기준은 파티션•셔플•상태의 실제 실행량을 함께 확인한다.
