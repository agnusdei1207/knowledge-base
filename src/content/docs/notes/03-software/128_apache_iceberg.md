---
sidebar:
  order: 128
  label: "128. Apache Iceberg"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Apache Iceberg"
date: "2026-08-25T11:00:00+09:00"
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

- **Apache Iceberg**: Netflix가 개발하고 아파치 오픈소스로 기증한 3계층 메타데이터 트리 기반의 대규모 오픈 테이블 포맷.
- **3계층 메타데이터 트리**: Metadata File(JSON), Manifest List(AVRO), Manifest File(AVRO)로 이어지는 계층형 메타데이터 구조.

</details>

- 정의/개념: 대규모 객체 스토리지 환경에서 **3계층 메타데이터 트리(Manifest)를 통해 ACID 트랜잭션, 숨김 파티셔닝, 스키마 진화를 제공**하는 오픈 테이블 포맷
- 배경/필요성: Hive 디렉터리 구조 기반의 파일 리스팅(ListBucket) 병목으로 인한 **초대규모 파일 스캔 지연 및 파티션 변경 시 테이블 재작성 해결 불가**

#### 한줄 요약
- 3계층 메타데이터 트리와 숨겨진 파티셔닝으로 디렉터리 탐색 없이 파일 수준의 고속 프루닝과 ACID를 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Hidden Partitioning**: 쿼리 작성자가 물리 파티션 컬럼을 명시하지 않고 원본 날짜 컬럼만 조건으로 주어도 엔진이 내부 변환 함수(`days()`)를 통해 자동 프루닝.
- **Partition Evolution**: 기존 데이터를 재작성하거나 마이그레이션하지 않고도 파티션 단위(예: 일 단위 $\to$ 월 단위)를 무중단으로 동적 변경.

</details>

- Metadata File $\to$ Manifest List $\to$ Manifest File의 **3계층 메타데이터 트리 아키텍처**
- 사용자가 파티션 구조를 몰라도 최적 프루닝을 수행하는 **숨겨진 파티셔닝(Hidden Partitioning)**
- Spark, Trino, Flink, Snowflake, BigQuery 등 **다양한 연산 엔진에 대한 완전한 중립성**

#### 한줄 요약
- 메타데이터 수준의 세밀한 통계와 엔진 중립성을 바탕으로 페타바이트급 테이블을 고속으로 관리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Iceberg Catalog**: 테이블 이름과 최신 Metadata File 경로를 원자적으로 매핑 관리하는 카탈로그(REST, Hive, Glue).

</details>

```text
[Apache Iceberg 3계층 메타데이터 트리 구조]
|-- Iceberg Catalog (REST Catalog / AWS Glue: 최신 Metadata File 포인터 관리)
|   `-- [v1.metadata.json] -> 테이블 스키마, 파티션 스펙(Spec), 전체 스냅샷 이력
|       `-- [snap-1.avro (Manifest List)] -> 현재 스냅샷의 Manifest File 배열 및 파티션 범위
|           |-- [manifest-1.avro (Manifest File)] -> Parquet 파일 경로, 컬럼별 Min/Max 통계
|           `-- [manifest-2.avro (Manifest File)] -> Parquet 파일 경로, 컬럼별 Min/Max 통계
`-- Data Layer (Amazon S3 / GCS)
    |-- part-00001.parquet (실제 데이터 레코드 파일)
    `-- part-00002.parquet (실제 데이터 레코드 파일)
```

선의 의미: 계층 및 Catalog가 메타데이터 파일을 가리키고 Manifest List와 Manifest File을 거쳐 실제 데이터 파일로 접근하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **카탈로그 (Catalog)** | 테이블 이름과 **현재 최신 Metadata File(JSON)의 S3 위치 포인터 원자적 관리** | REST, AWS Glue 등 |
| **메타데이터 파일 (Metadata)**| 테이블 스키마, 파티션 규격(Spec), **전체 스냅샷 이력 및 현재 스냅샷 ID 보관** | JSON 포맷 |
| **매니페스트 리스트 (List)** | 특정 스냅샷을 구성하는 **Manifest File 목록과 파티션 범위 요약 통계 관리** | AVRO 포맷 |
| **매니페스트 파일 (Manifest)**| 실제 Parquet 파일의 경로, 상태(Add/Delete), **컬럼별 Min/Max 통계 정보 보관** | 파일 수준 Data Skipping |
| **데이터 파일 (Data File)** | 실제 비즈니스 레코드가 저장된 **불변(Immutable) Parquet/ORC 압축 파일** | 열 지향 포맷 |

#### 한줄 요약
- 카탈로그, 메타데이터 파일, 매니페스트 리스트, 매니페스트 파일의 3계층 트리가 데이터 파일을 정밀 추적한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Atomic Commit 5단계**: 기준 스냅샷 확인 $\to$ 데이터 파일 쓰기 $\to$ Manifest 생성 $\to$ Metadata JSON 갱신 $\to$ Catalog 포인터 원자 교체.

</details>

```text
클라이언트가 Iceberg 테이블에 트랜잭션 쓰기 커밋
        │
   1. [기준 스냅샷 확인] 트랜잭션 시작 시점의 테이블 스냅샷 ID 및 최신 파티션 규격 획득
        │
   2. [데이터 파일 기록] 변경/추가된 데이터를 새로운 불변 Parquet 파일로 S3에 기록
        │
   3. [Manifest 생성] 기록된 데이터 파일 경로와 컬럼별 Min/Max 통계를 담은 AVRO 파일 작성
        │
   4. [Metadata JSON 생성] 신규 스냅샷 ID를 부여하고 새 Manifest List와 연결된 메타데이터 생성
        │
   5. [Catalog 원자 교체] 카탈로그의 현재 테이블 포인터를 신규 Metadata 파일 경로로 원자적 갱신
```

#### 한줄 요약
- 스냅샷 확인 → 데이터 파일 기록 → Manifest 작성 → Metadata 생성 → 카탈로그 교체 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Iceberg vs Delta Lake**: 독립적인 오픈 생태계 중심의 Iceberg와 Spark/Databricks 생태계 중심의 Delta Lake.

</details>

| 비교 항목 | Apache Iceberg (오픈 표준) | Delta Lake (Databricks) |
|:---|:---|:---|
| 메타데이터 계층 | **3계층 AVRO Manifest 트리 구조** | **단일 디렉터리 JSON 커밋 로그 + 체크포인트** |
| 파티셔닝 유연성 | **Hidden Partitioning 및 Partition Evolution 지원**| 파티션 컬럼 물리 경로 종속, 변경 시 재작성 필요 |
| 엔진 생태계 중립성| **Trino, Flink, Spark, Snowflake 등 완전 중립** | Spark / Databricks 중심 (UniForm 확장 중) |
| 컬럼 진화 방식 | **고유 Field ID 기반 추적 (이름/순서 변경 무관)** | 컬럼명 매핑 기반 추적 |

#### 한줄 요약
- 다중 엔진 중립성과 숨겨진 파티셔닝은 Iceberg, 강력한 Spark 네이티브 통합은 Delta Lake를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Rewrite Operations**: 자잘한 Manifest와 데이터 파일을 병합하여 메타데이터 트리 탐색을 최적화하는 Iceberg 유지보수 프로시저.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빈번한 커밋으로 인한 수천 개의 Manifest File 누적 | **`rewrite_manifests()` 연산으로 Manifest 파일 정기 병합** | 메타데이터 조회 속도 극대화 |
| 초 단위 스트리밍 쓰기로 인한 Small Data Files 폭발 | **`rewrite_data_files()` (Bin-packing) 작업 주기적 실행** | Parquet 파일 크기 512MB 표준화 |
| 실패한 트랜잭션의 더미 파일 찌꺼기 누적 | **`remove_orphan_files()` 정기 스케줄링으로 고아 파일 삭제** | 미사용 S3 스토리지 비용 회수 |
| 과거 스냅샷 누적으로 인한 메타데이터 크기 비대화 | **`expire_snapshots()` 프로시저로 7일 이전 구버전 스냅샷 정리** | 카탈로그 파싱 속도 개선 |

#### 한줄 요약
- 매니페스트 병합, 데이터 파일 컴팩션, 고아 파일 삭제, 스냅샷 만료로 클러스터를 최적화한다.

## Ⅶ. 결론

- 멀티 클라우드 및 이종 연산 엔진(Spark, Trino, Flink) 환경에서 **벤더 종속 없는 데이터 레이크하우스를 구축하기 위해 Apache Iceberg를 오픈 테이블 포맷 표준으로 채택**하고, **3계층 Manifest 트리와 숨겨진 파티셔닝**을 통해 페타바이트급 데이터 플랫폼 완성

#### 한줄 요약
- Apache Iceberg는 3계층 Manifest 트리와 숨겨진 파티셔닝을 기반으로 엔진 중립적인 고성능 레이크하우스를 완성하는 차세대 표준 오픈 테이블 포맷이다.