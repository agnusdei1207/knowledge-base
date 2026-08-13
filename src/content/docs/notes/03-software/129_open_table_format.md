---
sidebar:
  order: 129
  label: "129. 오픈 테이블 포맷 비교 (Open Table Format)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "오픈 테이블 포맷 비교 (Open Table Format)"
date: "2026-08-13T23:41:00+09:00"
tags:
  - "notes-software"
weight: 129
extra:
  question_no: "129"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 세 오픈 포맷 선택 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Open Table Format (오픈 테이블 포맷)**: S3/GCS 등 클라우드 객체 스토리지 파일들 위에서 ACID 트랜잭션, 타임 트래블, 스키마/파티션 진화 기능을 가능하게 해주는 오픈소스 메타데이터 레이어 표준 (Delta Lake, Apache Iceberg, Apache Hudi).
- **Metadata Management Layer**: 디렉터리 경로 스캔 방식(Hive Metastore)을 지양하고, 파일 단위 메타데이터(AVRO/JSON)를 관리하여 초고속 데이터 Pruning 및 동시성 제어를 렌더링하는 기술.

</details>

- 정의/개념: 객체 파일을 테이블로 관리하는 **Open Table Format**
- 배경/필요성: 디렉터리 기반 파일 관리는 **동시 커밋•진화•탐색** 제약

#### 한줄 요약

- 같은 객체 스토리지 파일을 여러 엔진이 동일한 테이블로 읽도록 공개된 메타데이터 명세를 둔다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Acid Compliance & Time Travel**: 객체 스토리지 상에서 100% 원자성 및 과거 시점 복구 보장.
- **Hidden Partitioning & Schema Evolution**: SQL 쿼리 파괴 없는 자동 파티션 갱신 및 스키마 변경.

</details>

- **ACID Transactions & Time Travel (과거 스냅샷 복원)**
- **Schema & Partition Evolution (컬럼 추가/삭제 및 파티션 변경 수용)**
- **Engine Agnostic (Spark, Trino, Flink, Snowflake, Presto 등 다양한 엔진 지원)**

#### 한줄 요약

- 세 포맷 모두 안전한 장부를 제공하지만 현재 파일과 바뀐 행을 찾고 정리하는 방법이 다르다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Delta vs Iceberg vs Hudi**: Databricks 주도의 Delta Lake, Netflix/Apache 주도의 Iceberg, Uber 주도의 Hudi.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                    Open Table Format Layer Architecture                │
├────────────────────────────────────────────────────────────────────────┤
│ Engines: [Apache Spark]    [Trino / Presto]    [Apache Flink]          │
├────────────────────────────────────────────────────────────────────────┤
│ Open Table Format Metadata Layer:                                      │
│  • Delta Lake:  JSON Commit Log + Parquet Checkpoint                   │
│  • Iceberg:     3-Tier Metadata (Metadata File -> Manifest List/File) │
│  • Hudi:        Timeline Metadata + Key Index                          │
├────────────────────────────────────────────────────────────────────────┤
│ Storage Layer: Cloud Object Storage [AWS S3 / GCS / Azure ADLS]        │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 처리 엔진들이 오픈 테이블 포맷 메타데이터를 거쳐 S3 파일에 저장/조회 연산을 수행하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **Catalog** | 테이블명과 현재 메타데이터 위치 관리 |
| **Metadata File** | 스냅숏•스키마•파티션•통계 보관 |
| **Data File** | 실제 행 데이터를 열 지향 파일로 저장 |
| **Delete File** | 위치•동등 조건 기반 행 삭제 정보 저장 |

#### 한줄 요약

- 엔진과 파일 사이의 공개 장부가 현재 테이블 상태를 정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Copy-on-Write (CoW) vs Merge-on-Read (MoR)**: CoW는 수정/삭제 시 파일 전체를 새로 덮어쓰는 방식(읽기 최적화), MoR은 변경분만 별도 Delta/Delete 파일에 쓰고 읽을 때 조인하는 방식(쓰기 최적화).

</details>

| 비교 항목 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| **최초 개발사** | **Databricks** | **Netflix** | **Uber** |
| **주요 강점 도메인**| **Spark / Databricks 파이프라인**| **멀티 엔진(Trino/Snowflake) BI**| **초저지연 스트리밍 CDC UPSERT**|
| **메타데이터 구조** | **JSON Commit Log (`_delta_log`)** | **3-Tier AVRO Metadata Tree** | Timeline Log + Key Index |
| **파티셔닝** | 명시 파티션 중심 | **Hidden Partitioning** | 명시•필드 파티션 |
| **쓰기 패턴 지원** | CoW•MoR | CoW•MoR | **CoW•MoR•레코드 인덱스** |

#### 한줄 요약

- 새 파일과 목록을 준비하고 현재 장부 위치를 한 번에 바꾼 뒤 독자는 확정된 파일만 읽는다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Decision Tree for Open Table Format**: Databricks 환경은 Delta Lake, 다양한 DW/BI 쿼리 엔진 조합은 Iceberg, 초저지연 CDC 스트리밍은 Hudi 선택.

</details>

```text
[요구사항 분석]
  ├── Databricks / Spark 위주 환경? ───────────────► [Delta Lake 선택]
  ├── 다양한 멀티 엔진 (Trino + Snowflake + Athena)? ──► [Apache Iceberg 선택]
  └── 초저지연 CDC 스트리밍 및 UPSERT 중심? ───────► [Apache Hudi 선택]
```

#### 한줄 요약

- 델타는 거래 로그, 아이스버그는 단계별 파일 목록, 후디는 작업 시간선과 레코드 위치표가 중심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Compaction & Vacuum**: 3대 포맷 공통으로 발생하는 자잘한 Small Files 및 구버전 메타데이터 파일 쓰레기를 정기 청소하는 배치 작업.

</details>

| 3대 유지보수 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Small File Problem** | 빈번한 스트리밍 삽입으로 Small File 누적 | **정기적인 `Compaction` 배치 작업 자동화** |
| **2. Storage Cost Risk** | 타임 트래블 구버전 파일 물리 누적 | **7일/30일 기준 `VACUUM` / `Expire Snapshots` 수행**|
| **3. Read Performance Drop**| MoR 삭제 파일 과다로 읽기 조인 지연 | **CoW 전환 또는 정기적 데이터 파일 Rewrite** |

> 사례: **카카오 / 네이버 / 쿠팡 Databricks Delta Lake & Apache Iceberg 혼용 레이크하우스 운용**

#### 한줄 요약

- 이름표만 비교하지 말고 실제 주문 변경을 넣어 쓰기•읽기•정리 비용까지 재 본다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Open Table Format 수립 기준(Open Table Standards)**: S3 스토리지, Iceberg/Delta 메타데이터, Compaction/Vacuum 자동화 및 Multi-Engine 수용성에 의거한 체계.

</details>

- Spark 중심은 **Delta**, 다중 엔진은 Iceberg, CDC 중심은 Hudi 선택

#### 한줄 요약

- 같은 안전 장부라도 도구와 변경 방식에 따라 유지비가 달라 실제 작업으로 골라야 한다.
