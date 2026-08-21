---
sidebar:
  order: 128
  label: "128. Apache Iceberg"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Apache Iceberg"
date: "2026-08-18T00:30:00+09:00"
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

<details><summary>용어 설명</summary>

- **Apache Iceberg 3계층 메타데이터 트리**: Metadata File(스냅샷 목록), Manifest List(스냅샷별 매니페스트 배열), Manifest File(개별 Parquet 파일의 경로 및 Min/Max 통계)로 구성된 오픈 테이블 포맷.
- **Hive 디렉터리 탐색 병목 및 파티션 한계(Directory Listing Bottleneck)**: 기존 하둡/하이브의 물리 디렉터리 스캔 방식으로 인해 파일 수가 수백만 개로 늘어날 때 쿼리 지연이 발생하고 파티션 변경이 불가능한 한계.

</details>

- 정의/개념: 대규모 객체 스토리지 환경에서 **3계층 메타데이터 트리(Manifest)를 통해 ACID 트랜잭션, 숨김 파티셔닝, 스키마 진화를 제공**하는 오픈 테이블 포맷
- 배경/필요성: Hive 디렉터리 구조 기반의 파일 리스팅(ListBucket) 병목으로 인한 **초대규모 파일 스캔 지연 및 파티션 변경 시 테이블 재작성 위험** 직면

#### 한줄 요약

- 3계층 메타데이터 트리와 숨겨진 파티셔닝을 통해 디렉터리 탐색 없이 파일 수준의 초고속 데이터 건너뛰기와 ACID를 보장

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **숨겨진 파티셔닝(Hidden Partitioning)**: 쿼리에 파티션 컬럼을 명시하지 않고 원본 날짜 컬럼만 조건으로 주어도 엔진이 알아서 `days(timestamp)` 파티션을 찾아 프루닝하는 기술.
- **필드 ID 기반 스키마 진화(Field ID Evolution)**: 컬럼명이 변경되거나 위치가 바뀌어도 고유 필드 ID를 기준으로 데이터를 추적하여 데이터 유실 없이 스키마를 유연하게 변경하는 기법.

</details>

- Metadata File $\to$ Manifest List $\to$ Manifest File의 **3계층 메타데이터 트리 아키텍처**
- 사용자가 파티션 구조를 몰라도 최적 프루닝을 수행하는 **숨겨진 파티셔닝(Hidden Partitioning)**
- Spark, Trino, Flink, Snowflake, BigQuery 등 **다양한 연산 엔진에 대한 완전한 중립성** #### 한줄 요약

- 메타데이터 수준의 세밀한 통계와 엔진 중립성을 바탕으로 페타바이트급 테이블을 고속으로 관리

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Manifest File**: 실제 Parquet 데이터 파일의 경로, 파티션 소속, 레코드 수, 컬럼별 Min/Max 통계가 AVRO 포맷으로 기록된 파일.

</details>

```text
[ Apache Iceberg 3계층 메타데이터 트리 구조도 ]

 [ Iceberg Catalog (REST / Hive / Glue) ]
                     │ (Current Metadata Pointer)
                     ▼
 1. [ v1.metadata.json (Metadata File) ]
    - 테이블 스키마, 파티션 스펙, 스냅샷 이력
                     │
                     ▼
 2. [ snap-1.avro (Manifest List) ]
    - 현재 스냅샷에 속한 Manifest File들의 배열 및 파티션 범위
                     │
                     ▼
 3. [ manifest-1.avro (Manifest File) ]
    - 실제 Parquet 파일 경로, 레코드 수, 컬럼별 Min/Max 통계
                     │
                     ▼
 4. [ part-0001.parquet ]  [ part-0002.parquet ] (Data Files)
```

선의 의미: Catalog가 메타데이터 파일을 가리키고, Manifest List와 Manifest File 트리를 타고 내려가 최종 데이터 파일로 좁혀나가는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 카탈로그 (Catalog) | 테이블 이름과 **현재 최신 Metadata File(JSON)의 S3 위치 포인터 원자적 관리** |
| 메타데이터 파일 (Metadata) | 테이블 스키마, 파티션 규격(Spec), **전체 스냅샷 이력 및 현재 스냅샷 ID 보관** |
| 매니페스트 리스트 (List) | 특정 스냅샷을 구성하는 **Manifest File 목록과 파티션 범위 요약 통계 관리** |
| 매니페스트 파일 (Manifest) | 실제 Parquet 파일의 경로, 상태(Add/Delete), **컬럼별 Min/Max 통계 정보 보관** |
| 데이터 파일 (Data File) | 실제 비즈니스 레코드가 저장된 **불변(Immutable) Parquet/ORC 압축 파일** |

#### 한줄 요약

- 카탈로그, 메타데이터 파일, 매니페스트 리스트, 매니페스트 파일의 3계층 트리가 데이터 파일을 정밀 추적

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Iceberg 원자적 커밋 5단계**: 기준 스냅샷 확인 $\to$ 데이터/삭제 파일 기록 $\to$ Manifest 생성 $\to$ Metadata 갱신 $\to$ Catalog 포인터 교체.

</details>

```text
[ Apache Iceberg 원자적 트랜잭션 커밋 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 기준 스냅샷(Base Snapshot) 확인     │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 신규 Parquet 데이터/삭제 파일 S3 기록│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 신규 AVRO Manifest File 생성        │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 신규 Snapshot 및 Metadata JSON 생성 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Catalog 최신 메타데이터 포인터 원자 교체
 └────────────────────────────────────────┘
```

### 동작 원리

1. 기준 스냅샷 확인: 트랜잭션 시작 시점의 테이블 스냅샷 ID와 유효 파티션 규격을 획득.
2. 데이터 파일 기록: 변경된 데이터를 새로운 Parquet 파일로 S3에 기록.
3. Manifest 생성: 기록된 데이터 파일의 경로와 컬럼별 Min/Max 통계를 담은 AVRO Manifest File을 작성.
4. Metadata 생성: 신규 스냅샷 ID를 부여하고 새로운 Manifest List와 연결된 Metadata JSON을 생성.
5. Catalog 포인터 교체: 카탈로그의 현재 테이블 포인터를 신규 Metadata 파일 경로로 원자적(Atomic Swap) 갱신.

#### 한줄 요약

- 스냅샷 확인 $\to$ 데이터 파일 기록 $\to$ Manifest 작성 $\to$ Metadata 생성 $\to$ 카탈로그 교체의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Iceberg vs Delta Lake**: 독립적인 Apache 오픈 생태계 중심의 Iceberg와 Spark/Databricks 생태계 중심의 Delta Lake.

</details>

| 구분 | Apache Iceberg (오픈 표준) | Delta Lake (Databricks) |
|:---|:---|:---|
| **적용 기준** | Trino, Flink, Spark, Snowflake 등 다중 엔진 중립 환경 | Spark 및 Databricks 플랫폼 중심의 통합 분석 환경 |
| **핵심 특징** | **3계층 AVRO Manifest 트리, 숨겨진 파티셔닝 지원** | **JSON 커밋 로그(`_delta_log`) + Checkpoint Parquet** |
| **한계** | Manifest 파일 누적 시 정기적인 트리 컴팩션 관리 필요 | 타 엔진(Trino 등) 지원 시 추가적인 커넥터 호환성 확인 필요 |

#### 한줄 요약

- 다중 엔진 중립성과 숨겨진 파티셔닝은 Iceberg, 강력한 Spark 네이티브 통합은 Delta Lake를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **매니페스트 및 데이터 재작성(Rewrite Operations)**: 자잘한 Manifest와 데이터 파일을 병합하여 메타데이터 트리 탐색을 최적화하는 유지보수 연산.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빈번한 커밋으로 인한 수천 개의 Manifest File 누적 | **`rewrite_manifests()` 연산으로 Manifest 파일 정기 병합** | 메타데이터 조회 속도 극대화 |
| 초 단위 스트리밍 쓰기로 인한 Small Data Files 폭발 | **`rewrite_data_files()` (Bin-packing) 작업 주기적 실행** | Parquet 파일 크기 512MB 표준화 |
| 실패한 트랜잭션의 더미 파일 찌꺼기 누적 | **`remove_orphan_files()` 정기 스케줄링으로 고아 파일 삭제** | 미사용 S3 스토리지 비용 회수 |

#### 한줄 요약

- 매니페스트 병합, 데이터 파일 컴팩션, 고아 파일 삭제를 통해 Iceberg 클러스터를 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **글로벌 오픈 표준 테이블(Global Standard Table Format)**: Snowflake, AWS, GCP 등 주요 클라우드 벤더들이 기본 지원하는 차세대 표준 오픈 테이블 포맷.

</details>

- **Apache Iceberg** 기반 객체 스토리지의 디렉터리 한계를 완전히 극복한 가장 진보된 오픈 테이블 포맷이며, 3계층 메타데이터 트리와 숨겨진 파티셔닝을 통해 멀티 엔진 기반의 개방형 데이터 레이크하우스를 실현함

#### 한줄 요약

- 3계층 Manifest 트리와 숨겨진 파티셔닝을 기반으로 엔진 중립적인 고성능 레이크하우스를 완성
