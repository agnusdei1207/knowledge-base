---
sidebar:
  order: 127
  label: "127. Delta Lake"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Delta Lake (Delta Lake)"
date: "2026-08-27T02:25:00+09:00"
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

- **Delta Lake**: Databricks가 주도한 오픈 테이블 포맷으로, S3/ADLS 객체 스토리지의 Parquet 파일 위에 JSON 커밋 로그(`_delta_log/`)를 추가하여 ACID를 보장하는 스토리지 계층.
- **_delta_log**: 모든 트랜잭션의 파일 변경 이력(Add/Remove)을 순차적 JSON 파일과 10회 주기 Checkpoint Parquet로 기록하는 핵심 디렉터리.

</details>

- 정의/개념: 객체 스토리지의 Parquet 파일 상에 **JSON 트랜잭션 로그(`_delta_log`)를 결합하여 ACID 트랜잭션, 타임트래블, MERGE INTO를 지원**하는 오픈 테이블 포맷
- 배경/필요성: 객체 스토리지의 파일을 직접 고치면 부분 쓰기 실패를 되돌릴 방법이 없고 동시 쓰기의 순서를 정할 지점도 없어 정합성을 파일 시스템에 기댈 수 없으므로, 어떤 파일이 유효한지를 별도 JSON 커밋 로그에 기록하고 그 로그를 테이블 상태의 유일한 정본으로 삼을 필요

#### 한줄 요약
- 데이터 파일을 불변으로 두고 유효성을 로그로만 판정하기에 갱신·삭제·타임트래블이 모두 같은 메커니즘 하나로 해결되지만, 그 대가로 읽기마다 로그를 재생하는 비용이 붙는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Z-Ordering**: 다차원 공간 채움 곡선(Space-Filling Curve)을 적용하여 여러 컬럼의 데이터를 동일 파일에 물리적으로 군집화함으로써 Data Skipping을 극대화.
- **ACID & OCC**: 낙관적 동시성 제어(OCC)를 통해 여러 작업자가 동시에 쓰기를 시도해도 충돌 없이 순차적 스냅샷을 생성.

</details>

- 객체 스토리지 파일 쓰기에 대한 **완벽한 ACID 트랜잭션 및 스냅샷 격리**
- RDBMS와 동일한 멱등성 병합 처리를 지원하는 **`MERGE INTO` (UPSERT) 지원**
- Spark Structured Streaming과 완벽히 통합된 **배치 및 스트리밍 통합 처리**

#### 한줄 요약
- JSON 커밋 로그와 OCC 동시성 제어를 통해 객체 스토리지의 데이터 정합성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Add & Remove File Actions**: `_delta_log` 내부에서 파일이 추가될 때 `AddFile`, 이전 파일이 갱신되어 삭제될 때 `RemoveFile`을 기록하여 최신 상태 유지.

</details>

```text
[Delta Lake 구성]
|-- _delta_log
|-- 체크포인트
|-- Parquet 데이터 파일
|-- OPTIMIZE & Z-Order
`-- VACUUM 엔진
```

선의 의미: 계층 및 Parquet 데이터 파일과 `_delta_log/` 트랜잭션 로그 파일이 결합하여 버전을 관리하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| `_delta_log` (커밋 로그) | 파일 추가/삭제(Add/Remove), **스키마 메타데이터 이력을 JSON 커밋으로 순차 기록** | 원자적 단일 진실 공급원 |
| 체크포인트 (Checkpoint) | 10개 커밋마다 누적 상태를 **단일 Parquet 파일로 압축하여 쿼리 시작 시간 단축** | 로그 재생 부하 제거 |
| Parquet 데이터 파일 | 테이블 레코드를 저장하는 **불변(Immutable) 열 지향 압축 파일** | Snappy 압축 지원 |
| OPTIMIZE & Z-Order | 자잘한 파일을 512MB~1GB로 병합하고 **Z-Order 컬럼 기준으로 물리 데이터를 재정렬** | Data Skipping 극대화 |
| VACUUM 엔진 | 타임 트래블 보존 기간(예: 7일)이 경과한 **미참조 물리 Parquet 파일을 영구 삭제** | 스토리지 비용 절감 |

#### 한줄 요약
- 로그가 길어질수록 재생 비용이 늘기에 체크포인트가 그 비용을 상수로 묶고, 무효화된 파일은 즉시 지워지지 않으므로 별도의 정리 작업이 저장 비용을 회수하는 역할을 맡는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Time Travel 5단계**: 대상 버전/시간 해석 $\to$ 최근 Checkpoint 로드 $\to$ 잔여 JSON 로그 재생 $\to$ 유효 파일 목록 확정 $\to$ Parquet 병렬 스캔.

</details>

```text
클라이언트가 타임 트래블 쿼리 실행 (`SELECT * FROM table VERSION AS OF 5`)
        │
   [버전 해석] 쿼리에서 요청한 과거 버전(Version 5) 또는 타임스탬프 시점 확인
        │
   [체크포인트 로드] 버전 5 이전의 가장 최근 Checkpoint Parquet 파일을 메모리에 로드
        │
   [로그 재생] Checkpoint 이후부터 버전 5까지의 JSON 로그를 순차 파싱하여 Add/Remove 계산
        │
   [유효 파일 목록 확정] 버전 5 시점에 유효했던 물리 Parquet 파일 경로 목록 정확히 도출
        │
   계산된 유효 Parquet 파일에 대해서만 Spark 엔진이 병렬 스캔하여 과거 결과 즉시 반환
```

#### 한줄 요약
- 읽기 시점의 유효 파일 목록이 로그 재생으로 결정되므로, 조회 성능은 데이터 크기보다 로그 길이와 체크포인트 간격에 먼저 좌우된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **3대 오픈 테이블 포맷**: Databricks 중심의 Delta Lake, Apache 재단 중립의 Apache Iceberg, Uber 중심의 Apache Hudi.

</details>

| 비교 항목 | Delta Lake (Databricks) | Apache Iceberg (Apache 재단) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| 메타데이터 아키텍처 | **JSON Log + Checkpoint Parquet** | **Avro Manifest List + Manifest File 트리** | **Timeline Commit Log (Avro 메타)** |
| 주 연동 생태계 | **Apache Spark 및 Databricks 최적화** | **Trino, Flink, Spark 등 다중 엔진 중립** | **Flink / Spark 기반 대규모 CDC 스트리밍**|
| 파티션 변경 지원 | 파티션 컬럼 변경 시 테이블 재생성 필요 | **Partition Evolution (무중단 파티션 변경)** | 파티션 변경 제한적 |
| 갱신/병합 메커니즘 | Copy-on-Write (COW) 중심 | Copy-on-Write / Merge-on-Read 지원 | **Merge-on-Read (MOR) 초고속 쓰기 최적화** |

#### 한줄 요약
- Spark/Databricks 환경은 Delta Lake, 다중 엔진 중립성은 Iceberg, 스트리밍 증분 적재는 Hudi를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Schema Enforcement vs Evolution**: 의도치 않은 잘못된 컬럼 유입 시 쓰기를 차단(Enforcement)하고, 의도된 스키마 변경은 `mergeSchema`로 수용(Evolution).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스트리밍 인서트로 수만 개의 자잘한 Small File 누적 | **주기적 `OPTIMIZE table ZORDER BY (user_id)` 실행** | 파일 병합 및 데이터 건너뛰기 극대화 |
| 타임 트래블 이력 누적으로 S3 스토리지 비용 폭증 | **`VACUUM table RETAIN 168 HOURS` (7일 보존) 정기 스케줄링** | 구버전 미사용 파일 정리 및 비용 절감 |
| 다중 파이프라인 동시 쓰기 시 Concurrent Append 충돌 | **OCC 자동 재시도 활성화 및 쓰기 파티션 키 격리 분할** | 쓰기 충돌 에러 0건 달성 |
| 잘못된 데이터 타입 유입으로 인한 테이블 오염 | **Schema Enforcement 기본 활성화 및 `mergeSchema` 선별 적용** | 데이터 무결성 100% 보존 |

#### 한줄 요약
- Z-Order 최적화, Vacuum 정기 실행, OCC 자동 재시도, 스키마 강제로 운영한다.

## Ⅶ. 결론

- Spark 기반 레이크는 **Delta Lake**, 정렬은 **Z-Order** 선택

#### 한줄 요약
- Delta Lake는 Parquet 파일과 JSON 트랜잭션 로그를 통해 객체 스토리지 상에서 무결점 ACID 트랜잭션과 고성능 UPSERT를 완성하는 대표 오픈 테이블 포맷이다.
