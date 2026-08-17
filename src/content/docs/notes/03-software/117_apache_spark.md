---
sidebar:
  order: 117
  label: "117. Apache Spark"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Apache Spark"
date: "2026-08-18T00:00:00+09:00"
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

- **Apache Spark 핵심 기술**: 메모리 계보(Lineage) 복원이 가능한 불변 분산 데이터 집합(RDD), 방향성 비순환 그래프(DAG) 실행 엔진, SQL 질의를 최적화하는 Catalyst Optimizer.
- **반복 연산 및 스트리밍 지연(Iterative & Streaming Bottleneck)**: 하둡 MapReduce처럼 매 단계마다 디스크에 중간 결과를 쓰는 방식으로 인해 머신러닝 반복 연산과 대화형 쿼리가 극도로 느려지는 한계.

</details>

- 정의/개념: 대규모 분산 데이터 처리를 위해 **인메모리 RDD와 DAG 실행 엔진 및 Catalyst 최적화기를 기반으로 고속 병렬 연산을 수행**하는 분산 컴퓨팅 프레임워크
- 배경/필요성: 기존 하둡 MapReduce의 단계별 디스크 I/O 물질화로 인한 **반복 머신러닝, 실시간 스트리밍 및 대화형 분석 쿼리의 심각한 지연 위험** 직면

#### 한줄 요약

- 인메모리 RDD와 DAG 지연 연산을 통해 기존 디스크 기반 분산 처리 대비 최대 100배 빠른 대용량 데이터 연산을 실현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **지연 평가(Lazy Evaluation)**: `map`, `filter` 등 Transformation 연산 시 실제 계산을 미루고 DAG 그래프만 구축하다가 `collect`, `count` 등 Action 호출 시 한 번에 최적화 실행하는 기법.
- **Catalyst Optimizer 및 AQE(Adaptive Query Execution)**: 쿼리 계획을 규칙/비용 기반으로 최적화하고 런타임 통계를 바탕으로 파티션 수와 조인 방식을 동적으로 자동 보정하는 엔진.

</details>

- 메모리 상에서 중간 데이터를 유지하는 **인메모리 컴퓨팅(In-Memory Computing)**
- 연산 파이프라인을 최적화하여 한 번에 실행하는 **지연 평가(Lazy Evaluation)**
- SQL, Streaming, 머신러닝(MLlib), 그래프(GraphX)를 아우르는 **통합 분산 데이터 플랫폼**

#### 한줄 요약

- 인메모리 RDD 계보 복원과 Catalyst 최적화를 통해 고속 반복 연산과 대규모 스트리밍을 지원

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Driver vs Executor**: main() 프로그램을 실행하며 DAG를 생성하고 태스크를 분배하는 Driver와 실제 메모리 파티션을 보유하고 태스크를 수행하는 Executor.

</details>

```text
[ Apache Spark 클러스터 아키텍처 구조도 ]

 ┌────────────────────────────────────────────────────────────────────────┐
 │ [ Driver Program (SparkSession / DAG Scheduler / Catalyst Optimizer) ] │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ (Task 분배 및 스케줄링)
 ┌───────────────────────────────────┼────────────────────────────────────┐
 │                                   ▼                                    │
 │                       [ Cluster Manager (YARN / K8s) ]                 │
 │                                   │                                    │
 │                 ┌─────────────────┴─────────────────┐                  │
 │                 ▼                                   ▼                  │
 │      [ Executor 1 (Worker Node) ]        [ Executor 2 (Worker Node) ]  │
 │      - RAM RDD Cache                     - RAM RDD Cache               │
 │      - Task 1, Task 2 실행               - Task 3, Task 4 실행         │
 └────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Driver가 DAG 스케줄러를 통해 연산을 최적화하고 Cluster Manager를 거쳐 각 Executor 노드의 메모리 파티션으로 태스크를 전파하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 드라이버 프로그램 (Driver) | 애플리케이션 진입점(main)을 실행하고 **DAG 생성 및 태스크 스케줄링 총괄** |
| Catalyst 최적화기 | SQL/DataFrame의 논리적 계획을 최적화하고 **최적의 물리적 실행 계획 생성** |
| DAG 스케줄러 | 전체 연산 그래프를 셔플(Shuffle) 경계 기준으로 **Stage와 Task 단위로 분할** |
| 클러스터 매니저 (YARN/K8s) | 클러스터 노드의 CPU/Memory 자원을 중계하고 **Executor 프로세스 할당/회수** |
| 실행기 (Executor) | 워커 노드에서 메모리 상에 RDD를 캐시하고 **할당된 태스크를 병렬 실행** |

#### 한줄 요약

- 드라이버(총괄), Catalyst(최적화), DAG 스케줄러(분할), 실행기(연산)가 결합하여 고속 분산을 달성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Spark 쿼리 실행 5단계 파이프라인**: 논리 계획 분석 $\to$ 논리 최적화 $\to$ 물리 계획 생성 $\to$ Stage/Task 실행 $\to$ AQE 동적 보정.

</details>

```text
[ Spark Catalyst 및 DAG 연산 실행 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. DataFrame / Spark SQL 쿼리 접수     │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 논리 계획(Logical Plan) 분석 및 검증│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Catalyst 최적화: 필터 푸시다운 적용  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 물리 계획 선택 및 Stage/Task 분할   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Executor 메모리 병렬 연산 및 AQE 보정│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 쿼리 접수: 클라이언트가 DataFrame API나 Spark SQL을 통해 비즈니스 쿼리를 선언.
2. 논리 계획 분석: 카탈로그 메타데이터를 참조하여 컬럼명, 데이터 타입, 테이블 존재 여부를 검증.
3. Catalyst 최적화: Filter Pushdown(조건절 우선 처리), Column Pruning(불필요 컬럼 제거) 규칙을 적용하여 최적화.
4. 물리 계획 수립: Broadcast Hash Join 등 최소 비용 물리 전략을 선택하고 셔플 기준으로 Stage를 분할.
5. 병렬 연산 및 AQE 보정: Executor 메모리에서 태스크를 실행하며, 런타임 데이터 크기에 따라 파티션 수를 동적으로 재조정.

#### 한줄 요약

- 쿼리 접수 $\to$ 논리 분석 $\to$ 최적화 $\to$ 물리 계획 수립 $\to$ 병렬 실행 및 AQE 보정의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Narrow vs Wide Transformation**: 셔플 없이 1:1 파티션으로 연산되는 Narrow(`map`, `filter`)와 셔플 네트워크 I/O가 발생하는 Wide(`groupBy`, `join`).

</details>

| 구분 | Narrow Transformation (협소 변환) | Wide Transformation (광역 변환) |
|:---|:---|:---|
| **적용 기준** | 단일 레코드 단위 가공 및 단순 필터링 | 동일 키 기준 데이터 그룹화, 집계 및 다중 테이블 조인 |
| **핵심 특징** | **부모 파티션과 자식 파티션이 1:1 매핑 (Shuffle 없음)** | **네트워크를 통해 데이터를 재분배하는 Shuffle 발생 (N:M 매핑)** |
| **한계** | 복합 집계 및 정렬 연산 수행 불가 | 대량 네트워크 전송 및 디스크 Spill로 인한 병목 위험 |

#### 한줄 요약

- 단일 파티션 내 초고속 처리는 Narrow 변환, 키 재분배 집계는 Wide 변환을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **데이터 스큐 솔팅(Data Skew Salting)**: 특정 키(Key)에 데이터가 집중되어 단일 Executor의 메모리가 터지는(OOM) 현상을 막기 위해 키 뒤에 임의 난수를 붙여 분산시키는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `collect()` 호출로 거대 결과 데이터가 Driver로 집중되어 Driver OOM | **`collect()` 사용을 엄격히 금지하고 `take(N)` 또는 스토리지 파일 저장** | Driver 메모리 고갈 원천 차단 |
| 특정 조인 키 편향으로 인한 Executor Data Skew OOM | **조인 키에 Salting 접두사 부여 및 Broadcast Hash Join 전환** | 파티션 부하 완벽 분산 |
| 수많은 RDD 객체 생성으로 인한 Java GC(가비지 컬렉션) 오버헤드 | **Kryo Serializer 적용 및 Tungsten 엔진 기반 DataFrame API 사용** | 메모리 효율 극대화 및 GC 지연 제거 |

#### 한줄 요약

- collect 지양, Salting 및 Broadcast 조인 적용, Kryo 직렬화를 통해 안정적 Spark 클러스터를 운용

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **데이터 레이크하우스 통합 컴퓨팅(Unified Lakehouse Computing)**: Spark 엔진을 기반으로 배치, 스트리밍, 대화형 BI, 머신러닝을 단일 인프라에서 통합 수행하는 차세대 아키텍처.

</details>

- **Apache Spark**는 현대 빅데이터 및 AI 엔지니어링의 표준 분산 컴퓨팅 엔진이며, Catalyst 최적화와 메모리 튜닝 및 AQE를 결합하여 페타바이트급 데이터 파이프라인의 처리 속도를 극대화해야 함

#### 한줄 요약

- 인메모리 RDD와 DAG 엔진을 기반으로 대규모 배치 및 스트리밍 연산을 초고속으로 완성
