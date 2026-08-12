---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Apache Spark"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Apache Spark**: 기존 MapReduce의 디스크 I/O 병목을 극복하기 위해 인메모리(In-Memory) 기반 RDD(Resilient Distributed Dataset) 및 DAG(Directed Acyclic Graph) 실행 엔진을 활용하여, 배치 및 스트리밍 연산을 최대 100배 빠르게 연산하는 2세대 분산 데이터 처리 엔진.
- **RDD (Resilient Distributed Dataset)**: 장애 발생 시 계보(Lineage) 추적을 통해 메모리상에서 즉시 복원 가능한, 불변(Immutable) 분산 데이터 집합.
- **DAG Engine (방향성 비순환 그래프)**: 연산 과정(Transformation)을 순과정이 없는 방향 그래프로 묶어 두었다가, 최적의 실행 경로(Stage)로 나누어 연산하는 최적화 엔진.

</details>

- 정의/개념: 인메모리 RDD 및 DAG 연산 그래프 최적화를 통해 기존 MapReduce 대비 100배 빠른 초고속 분산 처리를 수행하는 2세대 빅데이터 컴퓨팅 엔진인 **Apache Spark**
- 배경/필요성: 1세대 MapReduce의 단계별 디스크 Spill 및 네트워크 Shuffle I/O 병목 극복, 머신러닝 Iterative(반복) 연산 및 실시간 Stream 데이터 통합 연산 요구성

#### 한줄 요약

- 계산을 작업 그래프로 묶고 자주 쓰는 중간 자료를 재사용하는 엔진이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Lazy Evaluation (지연 연산)**: Action(예: `count()`, `collect()`) 구문이 호출되기 전까지는 실제 연산을 수행하지 않고 DAG 최적화 그래프만 축적하는 특성.
- **Catalyst Optimizer**: SQL 및 DataFrame 연산을 논리적/물리적 계획(Logical/Physical Plan)으로 자동 튜닝해 주는 내부 쿼리 최적화 엔진.

</details>

- **In-Memory Computing (RAM 중심의 RDD / DataFrame 연산)**
- **Lazy Evaluation (Transformation 지연 연산 & Action 시점 최적화 실행)**
- **Catalyst Optimizer & AQE (Adaptive Query Execution 동적 쿼리 최적화)**

#### 한줄 요약

- 반복 분석은 빠르지만 파티션 쏠림과 메모리 상태 등을 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (Spark 4대 핵심 컴포넌트 & 아키텍처)

<details><summary>핵심 용어</summary>

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

| 구성요소 (Component) | 역할 및 주요 메커니즘 | 실무 튜닝 포인트 |
|:---|:---|:---|
| **Driver Program** | **main() 실행, SparkSession 생성, DAG 그래프 최적화** | Driver Memory 부족 시 OOM 장애 발생 |
| **Executor** | **분산 노드 RAM 상에서 Task 실행 및 RDD 블록 저장** | Executor Cores & Memory 사양 배정 |
| **RDD / DataFrame** | **불변 분산 데이터 구조 (Lineage 계보 정보 보존)** | `.cache()` / `.persist()` 인메모리 튜닝 |
| **AQE Engine** | **실행 중 동적으로 Join 방식(Broadcast) 변경 및 파티션 병합** | `spark.sql.adaptive.enabled=true` |

#### 한줄 요약

- 계획자, 최적화 담당자, 작업 배정자, 실행자, 복구 저장소로 구성된다.

## Ⅳ. 흐름도 (Catalyst Optimizer 4단계 연산 흐름)

<details><summary>핵심 용어</summary>

- **BroadCast Hash Join**: 대용량 테이블과 소용량 테이블 조인 시, 소용량 테이블을 모든 Executor 메모리에 복제(Broadcast)하여 Shuffle I/O 0회로 조인하는 기법.

</details>

```text
[Unresolved Logical Plan] ──► [Analysis (Catalog)] ──► [Logical Optimization (Rule-based)]
                                                                │
                                                                ▼
[Physical Plan (Cost-based)] ◄── [Code Generation] ◄── [Physical Planning]
```

### 동작 원리

1. **Analysis**: SQL/DataFrame 구문을 내장 카탈로그와 대조하여 컬럼 및 타입 검증.
2. **Logical Optimization**: 조건절 푸시다운(Filter Pushdown), 불필요 컬럼 제거(Pruning) 수행.
3. **Physical Planning**: CBO 기반으로 Broadcast Hash Join 대 Sort Merge Join 등 최적 물리 연산 선택 후 코드로 컴파일 실행.

#### 한줄 요약

- 계산표를 먼저 최적화하고 셔플 경계로 나눠 여러 실행자에게 맡긴 뒤 실제 크기로 계획을 보정한다.

## Ⅴ. 종류 및 비교 (Transformation 대 Action)

<details><summary>핵심 용어</summary>

- **Transformation vs Action**: Transformation(`map`, `filter`, `groupBy`)은 지연 연산으로 DAG 구성, Action(`select`, `collect`, `save`)은 연산 즉시 실행.

</details>

| 연산 분류 (Operation) | 주요 메소드 종류 | 실행 특성 및 메커니즘 |
|:---|:---|:---|
| **Narrow Transformation** | **`map()`, `filter()`, `flatMap()`** | **1:1 파티션 맵핑 (Shuffle 없음, 초고속)** |
| **Wide Transformation** | **`groupBy()`, `join()`, `distinct()`** | **N:M 파티션 맵핑 (Shuffle 디스크/네트워크 I/O 발생)** |
| **Action** | **`collect()`, `count()`, `saveAsTextFile()`** | **DAG 지연 연산을 확정 짓고 실제 Executor 가동** |

#### 한줄 요약

- Spark는 계산 그래프를 이어 실행하고 필요한 중간 자료만 캐시해 반복 작업을 줄인다.

## Ⅵ. 실무 고려사항 및 대책 (Spark OOM & Shuffle 병목 해결)

<details><summary>핵심 용어</summary>

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

<details><summary>핵심 용어</summary>

- **Spark 아키텍처 수립 기준(Apache Spark Standards)**: In-Memory RDD 튜닝, Catalyst/AQE 최적화, Data Skew Salting 및 Structured Streaming 수용성에 의거한 체계.

</details>

- **Spark 아키텍처 수립 기준**에 따라 빅데이터 2세대 분석/ML 시스템 구축 시 **Apache Spark & AQE & Delta Lake** 필수 수용

#### 한줄 요약

- Spark 처리 방식 선택 기준은 파티션•셔플•상태의 실제 실행량을 함께 확인한다.
