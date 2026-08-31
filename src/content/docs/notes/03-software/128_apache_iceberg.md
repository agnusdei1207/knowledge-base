---
sidebar:
  order: 128
  label: "128. Apache Iceberg"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Apache Iceberg"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 기존 Hive 메타스토어 방식이 디렉터리 기반 파일 목록 조회(`LIST`)에 의존하여 파일 수 증가 시 극심한 O(N) 파일 시스템 I/O 병목을 유발하고 파티션 변경 시 테이블 전체를 재작성해야 했던 한계를 극복하고, Metadata JSON $\to$ Manifest List $\to$ Manifest File로 이어지는 3계층 메타데이터 트리를 구축하여 **디렉터리 리스팅 없는 O(1) 파일 프루닝, 숨겨진 파티셔닝(Hidden Partitioning), 무중단 파티션 진화(Partition Evolution) 및 완벽한 엔진 중립성(Spark/Trino/Flink/Snowflake)을 실현**할 필요

#### 한줄 요약
- Iceberg는 파일 목록을 메타데이터로 관리해 프루닝 비용을 전체 데이터량에서 떼어내는 대신, 커밋마다 메타데이터 파일이 쌓여 그 정리를 상시 운영 작업으로 떠안는다.

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
[Apache Iceberg 메타데이터 트리]
|-- 카탈로그
`-- 메타데이터 계층
    |-- 메타데이터 파일
    |-- 매니페스트 리스트
    `-- 매니페스트 파일
        `-- 데이터 파일
```

선의 의미: 계층 및 Catalog가 메타데이터 파일을 가리키고 Manifest List와 Manifest File을 거쳐 실제 데이터 파일로 접근하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 카탈로그 (Catalog) | 테이블 이름과 **현재 최신 Metadata File(JSON)의 S3 위치 포인터 원자적 관리** | REST, AWS Glue 등 |
| 메타데이터 파일 (Metadata) | 테이블 스키마, 파티션 규격(Spec), **전체 스냅샷 이력 및 현재 스냅샷 ID 보관** | JSON 포맷 |
| 매니페스트 리스트 (List) | 특정 스냅샷을 구성하는 **Manifest File 목록과 파티션 범위 요약 통계 관리** | AVRO 포맷 |
| 매니페스트 파일 (Manifest) | 실제 Parquet 파일의 경로, 상태(Add/Delete), **컬럼별 Min/Max 통계 정보 보관** | 파일 수준 Data Skipping |
| 데이터 파일 (Data File) | 실제 비즈니스 레코드가 저장된 **불변(Immutable) Parquet/ORC 압축 파일** | 열 지향 포맷 |

#### 한줄 요약
- 3계층 트리는 스캔 범위를 위에서부터 단계적으로 잘라내는 구조라 상위 한 계층만으로도 대부분의 파일이 걸러지고, 그 덕분에 파일 수가 늘어도 질의 계획 비용이 선형으로 커지지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Atomic Commit 5단계**: 기준 스냅샷 확인 $\to$ 데이터 파일 쓰기 $\to$ Manifest 생성 $\to$ Metadata JSON 갱신 $\to$ Catalog 포인터 원자 교체.

</details>

```text
클라이언트가 Iceberg 테이블에 트랜잭션 쓰기 커밋
        │
   [기준 스냅샷 확인] 트랜잭션 시작 시점의 테이블 스냅샷 ID 및 최신 파티션 규격 획득
        │
   [데이터 파일 기록] 변경/추가된 데이터를 새로운 불변 Parquet 파일로 S3에 기록
        │
   [Manifest 생성] 기록된 데이터 파일 경로와 컬럼별 Min/Max 통계를 담은 AVRO 파일 작성
        │
   [Metadata JSON 생성] 신규 스냅샷 ID를 부여하고 새 Manifest List와 연결된 메타데이터 생성
        │
   [Catalog 원자 교체] 카탈로그의 현재 테이블 포인터를 신규 Metadata 파일 경로로 원자적 갱신
```

#### 한줄 요약
- 새 스냅샷을 만든 뒤 카탈로그 포인터만 교체하기에 커밋이 원자적으로 성립하지만, 동시 커밋이 몰리면 바로 그 한 지점에서 충돌해 재시도 비용이 발생한다.

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

- 엔터프라이즈 멀티 엔진 레이크하우스 및 클라우드 분석 플랫폼의 **글로벌 표준 오픈 테이블 포맷(Open Table Format)**으로 확립되었으며, 실무 운영 시에는 **매니페스트 탐색 지연을 제거하는 `rewrite_manifests()`, 소형 파일 I/O를 최적화하는 `rewrite_data_files()`, 스토리지 비용을 절감하는 `expire_snapshots()` 및 `remove_orphan_files()` 정기 유지보수 자동화**를 결합하여 페타바이트급 데이터에 대한 초고속 쿼리 성능과 비용 통제를 동시 달성

#### 한줄 요약
- Apache Iceberg는 3계층 Manifest 트리와 숨겨진 파티셔닝을 기반으로 엔진 중립적인 고성능 레이크하우스를 완성하는 차세대 표준 오픈 테이블 포맷이다.
