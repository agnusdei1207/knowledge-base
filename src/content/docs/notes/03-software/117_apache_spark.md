---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Apache Spark"
date: "2026-09-07T10:05:00+09:00"
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

- 정의/개념: 대규모 분산 처리를 위해 인메모리 RDD와 DAG 실행 엔진 및 **Catalyst** 최적화기를 기반으로 고속 병렬 연산을 수행하는 분산 컴퓨팅 프레임워크
- 배경/필요성: 1세대 Hadoop MapReduce의 매 단계 디스크 I/O 플러시로 인한 **심각한 지연 및 머신러닝/그래프 반복 연산 처리 한계**

#### 한줄 요약
- Spark는 중간 결과를 메모리에 두어 반복 연산 비용을 낮추는 대신 그 메모리를 잃으면 계보를 따라 다시 계산해야 하므로, 무엇을 캐시할지가 곧 재계산 비용과 메모리 점유의 균형 결정이 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lazy Evaluation(지연 평가)**: Transformation(`map`, `filter`) 연산 시 즉시 계산하지 않고 DAG만 구성한 뒤, Action(`count`, `save`) 호출 시 일괄 최적화 실행.
- **Catalyst Optimizer**: 논리적 실행 계획을 규칙(Rule) 및 비용(Cost) 기반으로 분석하여 최적의 물리적 실행 계획을 생성하는 엔진.

</details>

- 메모리 상에서 중간 데이터를 유지하는 인메모리 컴퓨팅(In-Memory Computing)
- 연산 파이프라인을 최적화하여 한 번에 실행하는 **지연 평가(Lazy Evaluation)**
- SQL, Streaming, 머신러닝(MLlib), 그래프(GraphX)를 아우르는 통합 분산 데이터 플랫폼

#### 한줄 요약
- 인메모리 RDD 계보 복원과 Catalyst 최적화를 통해 고속 반복 연산을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Driver vs Executor**: main()을 실행하고 DAG를 스케줄링하는 Driver와 워커 노드에서 실제 태스크를 메모리 병렬 실행하는 Executor.

</details>

```text
[Apache Spark 클러스터 아키텍처]
├─ [드라이버 프로그램 (Driver)]
│  ├─ SparkSession (진입점)
│  ├─ Catalyst Optimizer (쿼리 최적화)
│  └─ DAG Scheduler (Stage/Task 분할)
├─ [클러스터 관리자 (Cluster Manager)]
│  └─ YARN / Kubernetes (자원 할당)
└─ [워커 노드 (Worker Nodes)]
   ├─ Executor (태스크 병렬 실행)
   └─ RDD BlockManager (인메모리 캐시)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 드라이버 | DAG 생성과 태스크 스케줄링 조정 |
| Catalyst 최적화기 | SQL·DataFrame의 논리·물리 계획 최적화 |
| DAG 스케줄러 | 셔플 경계로 Stage·Task 분할 |
| 실행기 | RDD 캐시와 할당 태스크 실행 |

#### 한줄 요약
- Catalyst가 논리 계획을 다시 쓰고 DAG 스케줄러가 셔플 경계로 단계를 자르므로 작성한 코드 순서와 실제 실행 단위는 일치하지 않으며, 성능 판단의 기준도 코드 줄이 아니라 셔플 경계가 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AQE(Adaptive Query Execution)**: 런타임에 셔플 단계의 실제 데이터 크기를 측정하여 파티션 수를 자동 병합하고 조인 전략을 동적으로 변경하는 기술.

</details>

```text
DataFrame / Spark SQL 쿼리 선언
        │
   [논리 계획 수립] 파서와 카탈로그를 통해 Unresolved Plan을 Analyzed Logical Plan으로 변환
        │
   [Catalyst 최적화] Filter Pushdown 및 Column Pruning을 적용하여 최적화된 논리 계획 도출
        │
   [물리 계획 생성] 브로드캐스트 해시 조인 등 최소 비용 물리 전략 선택 및 Stage 분할
        │
   [Tungsten 코드 생성] JVM 바이트코드를 런타임 동적 컴파일(Whole-Stage CodeGen)
        │
   Executor 메모리 상에서 Task 병렬 실행 및 AQE 기반 런타임 파티션 동적 보정
```

#### 한줄 요약
- 지연 실행 덕분에 최적화기가 전체 계획을 한꺼번에 보고 연산을 재배치할 수 있지만, 결과를 드라이버로 끌어오는 액션이 끼어드는 순간 그 최적화 범위는 거기서 잘린다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Narrow vs Wide Transformation**: 셔플 없이 1:1 파티션으로 연산되는 Narrow(`map`, `filter`)와 네트워크 셔플이 발생하는 Wide(`groupByKey`, `join`).

</details>

| 비교 항목 | Narrow Transformation (협소 변환) | Wide Transformation (광역 변환) |
|:---|:---|:---|
| 데이터 의존성 | 부모 파티션과 자식 파티션이 1:1 대응 | 부모 파티션이 다수의 자식 파티션에 전파 (N:M)|
| 네트워크 셔플 | Shuffle 없음 (로컬 메모리 즉시 파이프라이닝)| 네트워크를 통해 데이터를 재분배하는 Shuffle 필수 |
| 대표 연산자 | `map()`, `flatMap()`, `filter()` | `groupByKey()`, `reduceByKey()`, `join()` |
| 장애 복구 비용 | 유실된 단일 로컬 파티션만 즉시 재계산 | 이전 Stage 전체 재실행 또는 셔플 파일 재인출 |

#### 한줄 요약
- 두 변환은 같은 데이터를 다루면서도 네트워크를 건너느냐로 갈리므로, 성능 개선은 연산량을 줄이는 일이 아니라 Wide 변환의 수와 그 발생 시점을 옮기는 일이 된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Salting**: 조인/집계 키에 임의의 난수 접두사를 붙여 특정 파티션에 데이터가 몰리는 Data Skew를 해소하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `collect()`에 따른 Driver OOM | 크기 확인 후 `take`·분산 저장 사용 | Driver 메모리 유입량 제한 |
| 특정 조인 키 편향으로 인한 Executor Data Skew OOM | 조인 키에 **Salting** 난수 부여 및 Broadcast Hash Join 전환 | 파티션 메모리 부하 균등 분산 |
| 다수 객체 생성에 따른 Java GC 지연 | Kryo·Tungsten 메모리 관리 적용 | 직렬화 크기와 GC 부담 감소 |
| 소규모 파일에 따른 셔플 I/O 병목 | `coalesce`·AQE 파티션 병합 적용 | 셔플 파티션 수 조정 |

#### 한줄 요약
- collect 지양, Salting 및 Broadcast 조인, Kryo 직렬화, 파티션 자동 병합으로 운영한다.

## Ⅶ. 결론

- 현대 빅데이터 엔지니어링, 대규모 분산 데이터 파이프라인 및 AI/ML 데이터 전처리의 **사실상 표준(De-facto Standard) 인메모리 분산 컴퓨팅 엔진**으로 확립되었으며, 실무 운영 시에는 **Driver OOM을 유발하는 `collect()` 금지, 셔플 네트워크 병목을 완화하는 Broadcast Hash Join 및 Adaptive Query Execution(AQE) 런타임 최적화, GC 부하를 억제하는 Off-Heap 메모리 관리(Tungsten) 및 Kryo 직렬화**를 결합하여 대규모 클러스터 자원 효율성과 처리량을 극대화

#### 한줄 요약
- 재사용 데이터는 캐시하고 Wide 변환의 셔플 비용을 줄인다.
