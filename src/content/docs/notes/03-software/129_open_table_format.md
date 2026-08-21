---
sidebar:
  order: 129
  label: "129. 오픈 테이블 포맷 비교 (Open Table Format)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "오픈 테이블 포맷 비교 (Open Table Format)"
date: "2026-08-18T00:35:00+09:00"
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

<details><summary>용어 설명</summary>

- **오픈 테이블 포맷 3대 기술**: S3/GCS 등 클라우드 객체 스토리지의 불변 Parquet 파일 상에서 ACID 트랜잭션, 타임 트래블, 스키마 진화를 가능케 하는 메타데이터 표준인 Delta Lake, Apache Iceberg, Apache Hudi.
- **물리 디렉터리 스캔 및 동시성 한계(Directory Scanning & Concurrency Bottleneck)**: 전통적 하둡/하이브의 디렉터리 파티션 탐색 방식으로 인해 발생하는 파일 리스팅 지연과 동시 쓰기 시 정합성 파괴 위험.

</details>

- 정의/개념: 객체 스토리지 파일 상에서 **ACID 트랜잭션, 타임트래블, 스키마 진화를 제공하는 Delta, Iceberg, Hudi** 등 오픈소스 메타데이터 계층 표준
- 배경/필요성: 전통적 데이터 레이크의 물리 디렉터리 스캔 방식으로 인한 **동시 쓰기 충돌, 원자적 롤백 불가 및 메타데이터 탐색 지연 위험** 직면

#### 한줄 요약

- 객체 스토리지 상에 표준화된 메타데이터 계층을 두어 다양한 분산 엔진이 공유 가능한 ACID 테이블을 구현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **낙관적 동시성 제어(OCC: Optimistic Concurrency Control)**: 동시 쓰기 트랜잭션 충돌 시 락 없이 커밋 시점에 충돌 여부를 검증하고 자동 재시도하는 분산 트랜잭션 메커니즘.
- **Copy-on-Write (CoW) vs Merge-on-Read (MoR)**: 수정 시 파일 전체를 새로 쓰는 읽기 최적화 CoW와 변경분만 별도 파일에 기록하고 조회 시 조인하는 쓰기 최적화 MoR.

</details>

- 객체 스토리지 기반의 **100% ACID 트랜잭션 및 스냅샷 격리 보장**
- 과거 특정 시점의 데이터 상태를 쿼리하고 원복하는 **타임 트래블(Time Travel) 지원**
- Spark, Trino, Presto, Flink 등 **다양한 연산 엔진이 단일 테이블을 직접 공유(Engine-Agnostic)**

#### 한줄 요약

- 오픈 메타데이터 표준을 통해 레이크의 경제성과 DW의 정합성을 동시에 달성

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **3대 포맷 메타데이터 구조**: Delta Lake(JSON Commit Log), Apache Iceberg(3-Tier AVRO Manifest Tree), Apache Hudi(Timeline Log + Index).

</details>

```text
[ 오픈 테이블 포맷 3대 기술 아키텍처 비교도 ]

 ┌────────────────────────────────────────────────────────────────────────┐
 │ 1. 다중 분석 엔진 계층: [ Apache Spark ]  [ Trino / Presto ]  [ Flink ] │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 2. 오픈 테이블 포맷 메타데이터 계층                                    │
 │   • Delta Lake:  JSON Commit Log (`_delta_log/`) + Parquet Checkpoint  │
 │   • Iceberg:     Metadata File ➔ Manifest List ➔ Manifest File (AVRO) │
 │   • Hudi:        Timeline Metadata + Key Index                         │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 3. 스토리지 계층: Cloud Object Storage [ AWS S3 / GCS / Azure ADLS ]   │
 │   • 불변(Immutable) Parquet / ORC 데이터 파일 및 삭제 파일             │
 └────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 처리 엔진들이 오픈 테이블 포맷 메타데이터를 거쳐 S3 파일에 저장/조회 연산을 수행하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 카탈로그 (Catalog) | 테이블 식별자와 **현재 유효한 최신 메타데이터 파일 위치를 원자적 관리** |
| 메타데이터 계층 | 스냅샷 버전, 스키마, 파티션 스펙, **파일별 Min/Max 통계 정보를 구조화 관리** |
| 데이터 파일 (Data File) | 실제 비즈니스 레코드를 저장하는 **불변(Immutable) Parquet/ORC 압축 파일** |
| 삭제 파일 (Delete File) | MoR 모드에서 **수정/삭제된 레코드의 위치 및 동등 조건을 별도 저장** |

#### 한줄 요약

- 카탈로그, 메타데이터 계층, 데이터 파일, 삭제 파일이 결합하여 객체 스토리지 테이블을 완성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **오픈 테이블 트랜잭션 5단계 파이프라인**: 스냅샷 조회 $\to$ 불변 파일 쓰기 $\to$ 메타데이터 작성 $\to$ OCC 충돌 검증 $\to$ 카탈로그 포인터 갱신.

</details>

```text
[ 오픈 테이블 포맷 원자적 커밋 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 현재 테이블 기준 스냅샷 메타데이터 조회│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 신규 불변 Parquet 데이터 파일 기록  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 신규 메타데이터(Log/Manifest) 생성  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. OCC 동시성 충돌 검증 (충돌 시 재시도)│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Catalog 최신 스냅샷 포인터 원자 갱신│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 스냅샷 조회: 쓰기 엔진이 카탈로그를 참조하여 현재 유효한 최신 테이블 스냅샷 버전을 확인.
2. 데이터 쓰기: 변경된 레코드를 새로운 불변 Parquet 파일로 객체 스토리지에 기록.
3. 메타데이터 생성: 신규 파일 경로 및 통계 정보를 담은 메타데이터(JSON 로그 또는 AVRO 매니페스트)를 작성.
4. 충돌 검증: 쓰기 도중 타 트랜잭션이 동일 파티션을 변경했는지 낙관적 동시성 제어(OCC)로 검사.
5. 포인터 갱신: 카탈로그의 현재 테이블 포인터를 신규 메타데이터로 원자적 교체하여 새 버전을 즉시 공개.

#### 한줄 요약

- 스냅샷 조회 $\to$ 불변 파일 기록 $\to$ 메타데이터 생성 $\to$ OCC 충돌 검증 $\to$ 포인터 갱신의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Delta vs Iceberg vs Hudi**: Spark 중심(Delta), 다중 엔진 표준(Iceberg), 초저지연 CDC 스트리밍(Hudi).

</details>

| 구분 | Delta Lake (Databricks) | Apache Iceberg (Apache 재단) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| **적용 기준** | Spark 및 Databricks 플랫폼 중심 환경 | Trino, Snowflake, Spark 등 다중 엔진 환경 | 초저지연 CDC 스트리밍 UPSERT 환경 |
| **핵심 특징** | **JSON Log + Checkpoint, 완벽한 Spark 통합** | **3계층 AVRO 트리, 숨겨진 파티셔닝(Hidden)** | **Timeline Log + Key Index, 초고속 증분 적재** |
| **한계** | Databricks 외 타 엔진 지원 시 드라이버 의존성 | Manifest 파일 누적 시 정기적인 트리 관리 필요 | 아키텍처 및 설정 복잡도 상대적 높음 |

#### 한줄 요약

- Spark/Databricks 환경은 Delta Lake, 다중 엔진 중립성은 Iceberg, 실시간 CDC는 Hudi를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **컴팩션 및 스냅샷 만료(Compaction & Expire Snapshots)**: 작은 파일을 병합하고 만료된 스냅샷과 고아 파일을 제거하는 오픈 테이블 공통 유지보수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스트리밍 인서트로 인한 Small Files 누적으로 쿼리 지연 | **정기적인 백그라운드 `Compaction` (Bin-packing) 배치 실행** | 파일 크기 512MB 표준화 및 스캔 속도 5배 향상 |
| 타임 트래블 구버전 파일 누적으로 인한 S3 비용 폭증 | **보존 기간(7일) 기준 `VACUUM` / `Expire Snapshots` 자동화** | 미사용 불변 파일 삭제 및 스토리지 비용 절감 |
| MoR 삭제 파일 누적으로 읽기 시점 조인 오버헤드 증가 | **주기적인 CoW 변환 및 데이터 파일 Rewrite 작업 수행** | 읽기 성능 저하 해소 |

#### 한줄 요약

- 정기 컴팩션, 스냅샷 만료 자동화, 파일 재작성을 통해 오픈 테이블 포맷의 성능을 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **오픈 테이블 통합 거버넌스(Open Table Governance)**: REST Catalog 및 Apache Polaris 등을 통해 오픈 테이블 포맷의 메타데이터와 접근 제어를 중앙 집중 관리하는 체계.

</details>

- **오픈 테이블 포맷** 데이터 레이크하우스의 핵심 메타데이터 표준이며, 비즈니스 워크로드에 맞추어 Delta Lake, Apache Iceberg, Apache Hudi 중 최적의 포맷을 선정하고 정기적인 컴팩션 및 거버넌스를 결합해야 함

#### 한줄 요약

- 메타데이터 기반 ACID 트랜잭션과 다중 엔진 지원을 통해 개방형 데이터 레이크하우스를 완성
