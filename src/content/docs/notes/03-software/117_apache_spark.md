---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Apache Spark"
date: "2026-08-25T11:00:00+09:00"
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

- **Apache Spark**: 인메모리 분산 데이터셋(RDD)과 DAG 엔진을 바탕으로 배치, 스트리밍, 머신러닝을 고속 처리하는 분산 컴퓨팅 프레임워크.
- **RDD(Resilient Distributed Dataset)**: 노드 장애 시 계보(Lineage)를 추적하여 메모리 상에서 유실된 파티션만 재계산·복구하는 불변 분산 자료구조.

</details>

- 정의/개념: 대규모 분산 처리를 위해 **인메모리 RDD와 DAG 실행 엔진 및 Catalyst 최적화기를 기반으로 고속 병렬 연산을 수행**하는 분산 컴퓨팅 프레임워크
- 배경/필요성: 하둡 MapReduce의 단계별 디스크 I/O 물질화로 인한 **반복 머신러닝, 실시간 스트리밍 및 대화형 분석 쿼리의 심각한 지연 해결 불가**

#### 한줄 요약
- 인메모리 RDD와 DAG 지연 연산으로 디스크 기반 분산 처리 대비 최대 100배 빠른 연산을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lazy Evaluation(지연 평가)**: Transformation(`map`, `filter`) 연산 시 즉시 계산하지 않고 DAG만 구성한 뒤, Action(`count`, `save`) 호출 시 일괄 최적화 실행.
- **Catalyst Optimizer**: 논리적 실행 계획을 규칙(Rule) 및 비용(Cost) 기반으로 분석하여 최적의 물리적 실행 계획을 생성하는 엔진.

</details>

- 메모리 상에서 중간 데이터를 유지하는 **인메모리 컴퓨팅(In-Memory Computing)**
- 연산 파이프라인을 최적화하여 한 번에 실행하는 **지연 평가(Lazy Evaluation)**
- SQL, Streaming, 머신러닝(MLlib), 그래프(GraphX)를 아우르는 **통합 분산 데이터 플랫폼**

#### 한줄 요약
- 인메모리 RDD 계보 복원과 Catalyst 최적화를 통해 고속 반복 연산을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Driver vs Executor**: main()을 실행하고 DAG를 스케줄링하는 Driver와 워커 노드에서 실제 태스크를 메모리 병렬 실행하는 Executor.

</details>

```text
[Apache Spark 클러스터 아키텍처]
|-- Driver Program (애플리케이션 진입점: SparkSession)
|   |-- Catalyst Optimizer (논리/물리 쿼리 최적화 및 코드 생성)
|   `-- DAG Scheduler (Stage 분할 및 TaskSet 생성)
`-- Cluster Manager (YARN / Kubernetes / Standalone: 자원 할당)
    |-- Worker Node 1 -> Executor 1 (RAM RDD Cache + Task 1, 2 병렬 실행)
    `-- Worker Node 2 -> Executor 2 (RAM RDD Cache + Task 3, 4 병렬 실행)
```

선의 의미: 계층 및 Driver가 DAG를 수립하고 Cluster Manager를 통해 Executor들로 분산 실행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **드라이버 (Driver)** | 애플리케이션 진입점을 실행하고 **DAG 생성 및 태스크 스케줄링 총괄** | 단일 코디네이터 역할 |
| **Catalyst 최적화기** | SQL/DataFrame 논리 계획을 분석하여 **Filter Pushdown 등 최적 물리 계획 생성** | 규칙/비용 기반 CBO |
| **DAG 스케줄러** | 전체 연산 그래프를 셔플(Shuffle) 경계 기준으로 **Stage와 Task 단위로 분할** | 지연 평가 파이프라인화 |
| **실행기 (Executor)** | 워커 노드에서 메모리 상에 RDD를 캐시하고 **할당된 태스크를 병렬 실행** | JVM 컨테이너 기반 |

#### 한줄 요약
- 드라이버(총괄), Catalyst(최적화), DAG 스케줄러(분할), 실행기(연산)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AQE(Adaptive Query Execution)**: 런타임에 셔플 단계의 실제 데이터 크기를 측정하여 파티션 수를 자동 병합하고 조인 전략을 동적으로 변경하는 기술.

</details>

```text
DataFrame / Spark SQL 쿼리 선언
        │
   1. [논리 계획 수립] 파서와 카탈로그를 통해 Unresolved Plan을 Analyzed Logical Plan으로 변환
        │
   2. [Catalyst 최적화] Filter Pushdown 및 Column Pruning을 적용하여 최적화된 논리 계획 도출
        │
   3. [물리 계획 생성] 브로드캐스트 해시 조인 등 최소 비용 물리 전략 선택 및 Stage 분할
        │
   4. [Tungsten 코드 생성] JVM 바이트코드를 런타임 동적 컴파일(Whole-Stage CodeGen)
        │
   5. Executor 메모리 상에서 Task 병렬 실행 및 AQE 기반 런타임 파티션 동적 보정
```

#### 한줄 요약
- 논리 계획 → Catalyst 최적화 → 물리 계획 수립 → 코드 생성 → 메모리 병렬 실행 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Narrow vs Wide Transformation**: 셔플 없이 1:1 파티션으로 연산되는 Narrow(`map`, `filter`)와 네트워크 셔플이 발생하는 Wide(`groupByKey`, `join`).

</details>

| 비교 항목 | Narrow Transformation (협소 변환) | Wide Transformation (광역 변환) |
|:---|:---|:---|
| 데이터 의존성 | **부모 파티션과 자식 파티션이 1:1 대응** | **부모 파티션이 다수의 자식 파티션에 전파 (N:M)**|
| 네트워크 셔플 | **Shuffle 없음 (로컬 메모리 즉시 파이프라이닝)**| **네트워크를 통해 데이터를 재분배하는 Shuffle 필수** |
| 대표 연산자 | `map()`, `flatMap()`, `filter()` | `groupByKey()`, `reduceByKey()`, `join()` |
| 장애 복구 비용 | 유실된 단일 로컬 파티션만 즉시 재계산 | 이전 Stage 전체 재실행 또는 셔플 파일 재인출 |

#### 한줄 요약
- 파티션 내 초고속 처리는 Narrow 변환, 키 재분배 집계는 Wide 변환을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Salting**: 조인/집계 키에 임의의 난수 접두사를 붙여 특정 파티션에 데이터가 몰리는 Data Skew를 해소하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `collect()` 호출로 거대 데이터가 Driver로 몰려 Driver OOM | **`collect()` 금지 및 `take(N)` 또는 스토리지 파일 저장** | Driver 메모리 고갈 원천 차단 |
| 특정 조인 키 편향으로 인한 Executor Data Skew OOM | **조인 키에 Salting 난수 부여 및 Broadcast Hash Join 전환** | 파티션 메모리 부하 균등 분산 |
| 수많은 RDD 객체 생성으로 인한 Java GC 지연 발생 | **Kryo Serializer 적용 및 Tungsten 오프힙 메모리 관리 활용** | 메모리 효율 극대화 및 GC 오버헤드 제거 |
| 소규모 파일 수천 개로 인한 셔플 I/O 병목 | **`coalesce()` 및 AQE의 Coalescing Shuffle Partitions 활성화** | 셔플 파티션 수 자동 최적화 |

#### 한줄 요약
- collect 지양, Salting 및 Broadcast 조인, Kryo 직렬화, 파티션 자동 병합으로 운영한다.

## Ⅶ. 결론

- 대규모 데이터 처리와 인공지능 엔지니어링을 위해 **Apache Spark의 인메모리 DAG 엔진과 Catalyst 최적화기를 분산 파이프라인의 핵심 표준으로 도입**하고, **AQE 동적 튜닝 및 Broadcast 조인을 적용**하여 초고속 레이크하우스 컴퓨팅 완성

#### 한줄 요약
- Apache Spark는 인메모리 RDD와 DAG 실행 엔진을 통해 배치와 스트리밍 연산을 초고속으로 완수하는 현대 분산 데이터 엔지니어링의 표준 프레임워크다.