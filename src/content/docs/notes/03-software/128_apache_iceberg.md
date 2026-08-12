---
sidebar:
  order: 128
  label: "128. Apache Iceberg"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Apache Iceberg"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 128
extra:
  question_no: "128"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, Iceberg 메타데이터 구조 사례"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Apache Iceberg**: Netflix가 창시하여 Apache 재단 top-level 프로젝트로 공개된 대규모 오픈형 Open Table Format 기술로, 거대한 파일 파티션을 3계층 메타데이터 트리(Metadata File $\rightarrow$ Manifest List $\rightarrow$ Manifest File)로 추적하여 초고속 데이터 Pruning 및 ACID 트랜잭션을 보장.
- **Hidden Partitioning (숨겨진 파티셔닝)**: 사용자가 SQL 쿼리 작성 시 `WHERE date = '2026-08-12'`와 같이 파티션 변환 함수를 명시하지 않아도, Iceberg가 알아서 `days(timestamp)` 파티션을 자동 추적하여 쿼리를 가속해 주는 기능.
- **Field ID Schema Evolution**: 컬럼명을 바꾸거나 이동해도 컬럼 이름이 아닌 고유 필드 ID(Field ID)를 통해 데이터를 매핑함으로써 스키마 변경 시 데이터 유실을 0% 방지하는 기술.

</details>

- 정의/개념: S3 객체 스토리지 파일들을 3계층 트리 메타데이터로 관리하여, 엔진 독립적 ACID 트랜잭션, Hidden Partitioning, Field ID 기반 스키마 진화를 제공하는 표준 Open Table Format인 **Apache Iceberg**
- 배경/필요성: 기존 Hive 파티션 방식의 수백만 파일 S3 `ListBucket` 쿼리 지연 극복, 엔진 중립적(Spark, Trino, Flink, Snowflake) 멀티 레이크하우스 접근 요구성

#### 한줄 요약

- 폴더를 모두 뒤지지 않고 단계별 목록표로 현재 표에 속한 파일을 찾는다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Engine-Agnostic Format**: 특정 엔진(Spark/Databricks)에 종속되지 않고 Trino, Presto, Flink, Snowflake, BigQuery에서 100% 동일 테이블 접근.
- **Manifest-Level Data Pruning**: 각 Manifest File에 기록된 컬럼별 Min/Max 통계값을 읽어 무의미한 Parquet 파일 조회를 99% Skip.

</details>

- **3-Tier Tree Metadata Architecture (Metadata File $\rightarrow$ Manifest List $\rightarrow$ Manifest File)**
- **Hidden Partitioning & Field ID Based Schema Evolution**
- **Row-Level Deletes (Position Delete & Equality Delete)** 및 **Engine-Agnostic Open Standard**

#### 한줄 요약

- 열 이름이나 파티션이 바뀌어도 필드 ID와 매니페스트가 같은 데이터를 추적하지만 만료된 스냅숏과 고아 파일은 정리해야 한다.

## Ⅲ. 구조 및 구성요소 (Iceberg 3계층 메타데이터 트레이스 아키텍처)

<details><summary>핵심 용어</summary>

- **Manifest File**: 실제 Parquet 데이터 파일들의 경로, 용량, Row Count, 컬럼별 Min/Max 값 등의 통계가 세밀하게 기록된 AVRO 파일.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     Apache Iceberg 3-Tier Metadata Tree                │
├────────────────────────────────────────────────────────────────────────┤
│ Catalog (Iceberg Catalog: REST, Hive Metastore, AWS Glue)              │
│    │ (Pointer to Current Metadata File)                                │
│    ▼                                                                   │
│ [v1.metadata.json] (Schema, Partition Spec, Snapshots)                 │
│    │                                                                   │
│    ▼                                                                   │
│ [snap-1.avro (Manifest List)] (Contains array of Manifest Files)       │
│    │                                                                   │
│    ▼                                                                   │
│ [manifest-1.avro (Manifest File)] (File Paths, Min/Max Stats per Col) │
│    │                                                                   │
│    ▼                                                                   │
│ [part-0001.parquet] [part-0002.parquet] (Data Files)                   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Catalog가 메타데이터 파일을 가리키고, Manifest List와 Manifest File 트리를 타고 내려가 최종 데이터 파일로 좁혀나가는 아키텍처.

| 메타데이터 계층 | 주요 파일 및 역할 | 포함 정보 및 주요 이점 |
|:---|:---|:---|
| **Catalog (카탈로그)** | **테이블 이름과 최신 `vN.metadata.json` 주소 맵핑** | Atomic Commit 지원 (REST, Glue) |
| **Metadata File** | **테이블 스키마(Field ID), 파티션 규격, 스냅샷 목록**| `v1.metadata.json` 타임트래블 지점 |
| **Manifest List** | **해당 스냅샷에 속한 Manifest File들의 묶음 목록** | 파티션 범위 정보로 Manifest 가지치기 |
| **Manifest File** | **실제 Parquet 데이터 파일들의 경로 및 컬럼 Min/Max**| **Sub-second File Pruning 가속화** |

#### 한줄 요약

- 단계별 목록표가 현재 테이블에 속한 파일을 찾아 준다.

## Ⅳ. 흐름도 (Iceberg Position Delete 대 Equality Delete)

<details><summary>핵심 용어</summary>

- **Position Delete vs Equality Delete**: Position Delete는 지워질 행의 파일 경로와 Offset 위치를 직접 찍어 지우는 방식, Equality Delete는 `id=101`처럼 삭제 조건값을 기록해 두었다가 읽기 시점에 조인해 지우는 방식.

</details>

```text
[1. Position Delete (Merge-on-Read)]
 Data File: part-001.parquet ──► Delete File: (part-001.parquet, Row #40) ──► Read Time Skip!

[2. Copy-on-Write]
 Data File ──► [Rewrite Whole Parquet File without Row #40] ──► New Data File
```

### 동작 원리

1. **Merge-on-Read (Position Delete)**: 삭제 시 원본 파일을 안 건드리고 삭제 위치(`part-001, Row 40`)만 기록해 두었다가 Read 시점에 걸러냄 (**초고속 쓰기**).
2. **Copy-on-Write**: 삭제 시 원본 Parquet 전체를 다시 덮어써서 새 파일로 보관 (**읽기 성능 최적화**).

#### 한줄 요약

- 새 자료와 목록표를 모두 만든 뒤 카탈로그의 현재 위치표 한 칸만 원자적으로 바꾼다.

## Ⅴ. 종류 및 비교 (Apache Iceberg 대 Delta Lake)

<details><summary>핵심 용어</summary>

- **Open Standard Maturity**: Iceberg는 Snowflake, AWS Athena, BigQuery, StarRocks 등 모든 상용/오픈소스 DW 엔진에서 퍼스트 클래스로 동등 지원.

</details>

| 비교 항목 | Apache Iceberg | Delta Lake |
|:---|:---|:---|
| **오픈소스 주도** | **Apache Foundation (Netflix, Apple 개방 생태계)** | Databricks 주도 오픈소스 |
| **메타데이터 구조** | **3-Tier AVRO Tree (Manifest List/File)** | JSON Transaction Log (`_delta_log`) |
| **파티셔닝 기술** | **Hidden Partitioning (쿼리 자동 추적 파티셔닝)** | Explicit Partitioning (명시적 컬럼 파티션) |
| **엔진 중립성** | **극상 (Trino, Athena, Snowflake, Flink, Spark 등등)**| 상 (Spark / Databricks 최적화) |

#### 한줄 요약

- Hive식 표는 서랍 이름으로 자료를 찾고 Iceberg는 버전 있는 목록표로 자료를 찾는다.

## Ⅵ. 실무 고려사항 및 대책 (Iceberg 메타데이터 유지관리)

<details><summary>핵심 용어</summary>

- **Expire Snapshots**: 수개월 지난 구버전 스냅샷 메타데이터와 고아(Orphan) Parquet 파일들을 정리해 스토리지 비용을 감축시키는 작업.

</details>

| 튜닝 영역 | 발생 원인 및 위협 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **Manifest File 누적** | 빈번한 스트리밍 커밋으로 Manifest 수천 개 | **`rewrite_manifests()` 연산으로 Manifest 병합** |
| **Small Data Files** | 초 단위 쓰기로 1MB 이하 파일 폭발 | **`rewrite_data_files()` 병합 (Bin-packing)** |
| **Orphan Data Files** | 실패한 트랜잭션의 더미 파일 찌꺼기 | **`remove_orphan_files()` 정기 스케줄 실행** |

> 사례: **Snowflake / AWS Athena / Trino 모던 데이터 레이크하우스 아키텍처로 Apache Iceberg 채택**

#### 한줄 요약

- 사용자는 시각만 검색해도 Iceberg가 맞는 날짜 서랍과 값 범위의 파일만 골라낸다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Iceberg 수립 기준(Apache Iceberg Standards)**: 3계층 트래버스 메타데이터, Hidden Partitioning, Engine-Agnostic 중립성 및 Manifest Compaction에 의거한 체계.

</details>

- **Iceberg 수립 기준**에 따라 멀티 엔진(Trino+Spark+Snowflake) 레이크하우스 구축 시 **Apache Iceberg Open Table Format** 필수 수용

#### 한줄 요약

- 목록표 덕분에 구조를 안전하게 바꿀 수 있지만 오래된 목록과 쓰지 않는 파일은 계속 정리해야 한다.
