---
sidebar:
  order: 127
  label: "127. Delta Lake (Delta Lake)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Delta Lake (Delta Lake)"
date: "2026-08-18T00:25:00+09:00"
tags:
  - "notes-software"
weight: 127
extra:
  question_no: "127"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, Delta Lake 구현 사례 성격"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Delta Lake**: Databricks가 개발한 오픈 테이블 포맷(Open Table Format)으로, S3 등의 불변 Parquet 파일 상에 JSON 트랜잭션 로그(`_delta_log/`)를 결합하여 ACID 트랜잭션과 타임 트래블을 보장하는 스토리지 계층.
- **부분 실패 및 스키마 변조(Dirty Write & Schema Corruption)**: 전통적 데이터 레이크에서 파일 직접 수정 중 네트워크 단절로 일부 파일만 써지거나 부적절한 컬럼이 유입되어 테이블 전체가 손상되는 위험.

</details>

- 정의/개념: 객체 스토리지의 Parquet 파일 상에 **JSON 트랜잭션 로그(_delta_log)를 추가하여 ACID 트랜잭션, 타임트래블, MERGE를 보장**하는 오픈 테이블 포맷
- 배경/필요성: 기존 데이터 레이크의 파일 직접 갱신 시 발생하는 **부분 쓰기 실패(Dirty Write), 동시 쓰기 충돌 및 스키마 변조 위험** 직면

#### 한줄 요약

- 불변 Parquet 파일과 JSON 트랜잭션 로그를 결합하여 데이터 레이크 상에서 100% ACID 트랜잭션과 고성능 UPSERT를 실현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Delta 트랜잭션 로그(`_delta_log`)**: 모든 파일의 추가(Add)와 삭제(Remove) 액션을 순차적 JSON 커밋(`0000.json`)과 체크포인트 Parquet로 기록하는 메타데이터.
- **Z-Ordering**: 다차원 공간 채움 곡선을 적용하여 관련 컬럼의 데이터를 동일 파일에 물리적으로 군집화함으로써 파일 건너뛰기(Data Skipping)를 극대화하는 기법.

</details>

- 객체 스토리지 파일 쓰기에 대한 **완벽한 ACID 트랜잭션 및 스냅샷 격리**
- RDBMS와 동일한 멱등성 병합 처리를 지원하는 **`MERGE INTO` (UPSERT) 지원**
- Spark Structured Streaming과 완벽히 통합된 **배치 및 스트리밍 통합 처리** #### 한줄 요약

- JSON 커밋 로그와 OCC 동시성 제어를 통해 객체 스토리지의 신뢰성과 데이터 정합성을 보장

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Add & Remove File Actions**: `_delta_log` 내부에서 파일이 추가될 때 `AddFile`, 이전 버전 파일이 갱신되어 삭제될 때 `RemoveFile`을 기록하여 유효 파일 목록을 관리.

</details>

```text
[ Delta Lake 스토리지 아키텍처 구조도 ]

 MyTable/ (S3 디렉터리)
 ├── _delta_log/ (트랜잭션 로그 디렉터리)
 │   ├── 00000000000000000000.json  (Add: part-00001.parquet)
 │   ├── 00000000000000000001.json  (Remove: part-00001, Add: part-00002)
 │   └── 00000000000000000010.checkpoint.parquet (10개 로그 압축)
 ├── part-00001-c000.snappy.parquet (이전 버전 데이터 파일)
 └── part-00002-c000.snappy.parquet (최신 유효 데이터 파일)
```

선의 의미: Parquet 실체 데이터 파일과 `_delta_log/` 트랜잭션 로그 파일이 결합하여 ACID 버전을 완성하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| `_delta_log` (커밋 로그) | 파일 추가/삭제(Add/Remove), **스키마 메타데이터 이력을 JSON 커밋으로 순차 기록** |
| 체크포인트 (Checkpoint) | 10개 커밋마다 누적 상태를 **단일 Parquet 파일로 압축하여 쿼리 시작 시간 단축** |
| Parquet 데이터 파일 | 테이블 레코드를 저장하는 **불변(Immutable) 열 지향 압축 파일** |
| OPTIMIZE & Z-Order | 자잘한 파일을 1GB로 병합하고 **Z-Order 컬럼 기준으로 물리 데이터를 재정렬** |
| VACUUM 엔진 | 타임 트래블 보존 기간(예: 7일)이 경과한 **미참조 물리 Parquet 파일을 영구 삭제** |

#### 한줄 요약

- `_delta_log`, 체크포인트, Parquet 데이터 파일, 유지보수 엔진(OPTIMIZE/VACUUM)으로 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **타임 트래블(Time Travel) 쿼리 5단계**: 대상 버전/시간 해석 $\to$ 최근 Checkpoint 로드 $\to$ 잔여 JSON 로그 재생 $\to$ 유효 파일 추출 $\to$ Parquet 스캔.

</details>

```text
[ Delta Lake 타임 트래블 쿼리 처리 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 타임 트래블 쿼리 (VERSION AS OF N)  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 대상 버전 이전 최근 Checkpoint 로드 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Checkpoint 이후 잔여 JSON 로그 재생 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Add/Remove 파일 계산 ➔ 유효 파일 확정│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 해당 버전 Parquet 파일 병렬 스캔    │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 쿼리 접수: `SELECT * FROM table VERSION AS OF 5` 쿼리에서 대상 버전 번호를 확인.
2. 체크포인트 로드: 버전 5 이전의 가장 최근 체크포인트 Parquet 파일을 메모리에 로드.
3. 로그 재생: 체크포인트 이후부터 버전 5까지의 JSON 로그를 순서대로 파싱하여 Add/Remove 액션을 반영.
4. 파일 확정: 버전 5 시점에 유효했던 Parquet 파일 경로 목록을 정확히 도출.
5. 병렬 스캔: 계산된 파일 목록에 대해서만 Spark 엔진이 병렬 디스크 읽기를 수행하여 결과를 반환.

#### 한줄 요약

- 버전 확인 $\to$ 체크포인트 로드 $\to$ JSON 로그 재생 $\to$ 유효 파일 확정 $\to$ Parquet 스캔의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Open Table Format 3대 기술**: Databricks 중심의 Delta Lake, Netflix 주도의 Apache Iceberg, Uber 중심의 Apache Hudi.

</details>

| 구분 | Delta Lake (Databricks) | Apache Iceberg (Apache 재단) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| **적용 기준** | Spark 및 Databricks 중심 생태계 환경 | Trino, Flink, Spark 등 다중 엔진 중립 환경 | 대규모 CDC 스트리밍 및 빠른 증분 적재 환경 |
| **핵심 특징** | **JSON Log + Checkpoint, 완벽한 Spark 통합** | **AVRO Manifest List/File 계층 메타데이터** | **Timeline Log, Merge-on-Read (MOR) 최적화** |
| **한계** | Databricks 외 타 엔진 지원 시 드라이버 의존성 | 메타데이터 파일 트리 깊이에 따른 관리 복잡도 | 설정 복잡도 및 상대적으로 무거운 인프라 |

#### 한줄 요약

- Spark/Databricks 환경은 Delta Lake, 다중 엔진 중립성은 Iceberg, 스트리밍 증분 적재는 Hudi를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스키마 강제 및 진화(Schema Enforcement & Evolution)**: 실수로 잘못된 컬럼이 유입되면 쓰기를 차단(Enforcement)하고, 의도된 스키마 변경은 `mergeSchema` 옵션으로 수용(Evolution)하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스트리밍 인서트로 수만 개의 자잘한 Small File 누적 | **주기적 `OPTIMIZE my_table ZORDER BY (user_id)` 실행** | 파일 병합 및 데이터 건너뛰기 극대화 |
| 타임 트래블 이력 누적으로 S3 스토리지 비용 폭증 | **`VACUUM my_table RETAIN 168 HOURS` (7일 보존) 정기 스케줄링** | 구버전 미사용 파일 정리 및 비용 절감 |
| 다중 파이프라인 동시 쓰기 시 Concurrent Append 충돌 | **OCC 자동 재시도 활성화 및 쓰기 파티션 키 격리 분할** | 쓰기 충돌 에러 0건 달성 |

#### 한줄 요약

- Z-Order 최적화, Vacuum 정기 실행, OCC 자동 재시도를 통해 Delta Lake의 성능과 비용을 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **유니버설 포맷(UniForm: Universal Format)**: Delta Lake 메타데이터를 Iceberg 및 Hudi 메타데이터로 자동 동기화하여 엔진 종속성을 제거한 최신 기술.

</details>

- **Delta Lake** 기반 데이터 레이크에 엔터프라이즈급 신뢰성을 부여한 혁신적인 오픈 테이블 포맷이며, Z-Order 인덱싱과 배치·스트리밍 통합 파이프라인을 구축하여 레이크하우스의 핵심 엔진으로 운용해야 함

#### 한줄 요약

- Parquet 파일과 JSON 트랜잭션 로그를 통해 객체 스토리지 상에서 무결점 ACID 트랜잭션을 완성
