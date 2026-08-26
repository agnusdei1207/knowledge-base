---
sidebar:
  order: 126
  label: "126. 데이터 레이크하우스"
  badge:
    text: "기출 · 50%"
    variant: note
title: "데이터 레이크하우스 (Data Lakehouse)"
date: "2026-08-26T09:54:00+09:00"
tags:
  - "notes-software"
weight: 126
extra:
  question_no: "126"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 레이크•웨어하우스 통합 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **데이터 레이크하우스(Data Lakehouse)**: 저비용 객체 스토리지의 확장성과 데이터 웨어하우스(DW)의 ACID 트랜잭션 및 고성능 SQL을 융합한 차세대 데이터 아키텍처.
- **Open Table Format**: 객체 스토리지의 Parquet 파일 위에서 ACID 트랜잭션과 메타데이터 관리를 수행하는 계층(Delta Lake, Apache Iceberg).

</details>

- 정의/개념: 데이터 레이크의 유연한 저비용 스토리지와 **데이터 웨어하우스의 ACID 트랜잭션 및 고성능 SQL 관리를 단일 계층으로 융합**한 차세대 데이터 아키텍처
- 배경/필요성: Lake와 DW 이중 인프라 운영 시 발생하는 **데이터 중복 복제 비용, 파이프라인 지연 및 엔진 간 지표 불일치 해결 불가**

#### 한줄 요약
- 저비용 객체 스토리지 위에 오픈 테이블 포맷을 얹어 ACID 트랜잭션과 다중 엔진 SQL 분석을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Time Travel(타임 트래블)**: 테이블의 과거 스냅샷 버전으로 시점을 되돌려 쿼리하거나 롤백할 수 있는 기능.
- **Schema Evolution**: 기존 데이터를 재작성하지 않고도 안전하게 컬럼을 추가, 변경, 삭제할 수 있는 스키마 진화 기능.

</details>

- 객체 스토리지 파일 기반의 **100% ACID 트랜잭션 및 스냅샷 격리 보장**
- 단일 데이터 원천을 Spark, Trino, MLlib 등이 **직접 동시 쿼리(Direct Access)**
- 스냅샷 메타데이터 이력을 추적하여 과거 시점으로 롤백하는 **타임 트래블(Time Travel) 지원**

#### 한줄 요약
- 오픈 테이블 포맷을 통해 레이크의 경제성과 DW의 정합성을 동시에 달성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **레이크하우스 3대 계층**: Compute Layer(다중 쿼리 엔진), Open Table Format(메타데이터/ACID), Storage Layer(클라우드 객체 스토리지).

</details>

```text
[데이터 레이크하우스 3계층 아키텍처]
|-- 1. Compute Layer (다중 분산 쿼리 및 AI 연산 엔진)
|   |-- Spark SQL, Databricks, Trino / Presto, DuckDB, MLlib (직접 쿼리)
|-- 2. Open Table Format Layer (메타데이터 및 ACID 트랜잭션)
|   |-- Delta Lake / Apache Iceberg / Apache Hudi
|   |-- ACID 커밋 로그 (JSON / Avro 스냅샷 메타데이터 트리)
|   `-- Time Travel, Schema Evolution, Partition Evolution
`-- 3. Storage Layer (Cloud Object Storage)
    `-- Amazon S3 / GCS / ADLS (불변 Parquet / ORC 열 지향 데이터 파일)
```

선의 의미: 계층 및 다중 연산 엔진이 오픈 테이블 포맷 메타데이터를 통해 S3의 Parquet 파일에 직접 접근하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 다중 연산 엔진 (Compute) | Spark, Trino, Python 등이 **공통 테이블 포맷을 통해 데이터를 직접 병렬 처리** | 벤더 종속 탈피 |
| 오픈 테이블 포맷 (Format) | Delta Lake, Iceberg 등이 **ACID 트랜잭션, 타임 트래블, 스키마 진화 통제** | 메타데이터 기반 ACID |
| 메타데이터 카탈로그 | 현재 유효한 최신 테이블 스냅샷 포인터 및 **파티션/파일 통계 정보 보관** | Glue, Unity Catalog |
| 객체 스토리지 (Storage) | AWS S3 등에 **불변(Immutable) Parquet 데이터 파일과 변경 로그 영구 저장** | 저비용 무제한 확장 |

#### 한줄 요약
- 다중 연산 엔진, 오픈 테이블 포맷, 메타데이터 카탈로그, 객체 스토리지가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OCC(Optimistic Concurrency Control) 쓰기**: 스냅샷 확인 $\to$ 불변 파일 생성 $\to$ 충돌 검증 $\to$ 메타데이터 원자적 전환.

</details>

```text
클라이언트가 레이크하우스 테이블에 쓰기 트랜잭션 요청 (`MERGE INTO`)
        │
   [스냅샷 조회] 쓰기 트랜잭션이 현재 테이블의 최신 스냅샷 버전(Version N) 확인
        │
   [불변 파일 기록] 변경/추가된 데이터를 새로운 불변 Parquet 파일로 S3에 기록
        │
   [동시 커밋 충돌 검증] 작업 도중 타 트랜잭션의 동일 파티션 변경 여부 OCC 검사
        │
   [신규 메타데이터 생성] 추가/삭제된 파일 목록을 담은 신규 스냅샷 메타데이터(N+1) 작성
        │
   카탈로그의 최신 포인터를 N+1로 원자적(Atomic) 전환하여 즉시 공개
```

#### 한줄 요약
- 스냅샷 조회 → 불변 파일 기록 → OCC 충돌 검증 → 메타데이터 작성 → 원자적 포인터 전환 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DW vs Lake vs Lakehouse**: 정형 SQL 전용 DW, 무질서 원본 보관 Lake, 둘의 장점을 융합한 Lakehouse.

</details>

| 비교 항목 | 데이터 웨어하우스 (DW) | 데이터 레이크 (Data Lake) | 데이터 레이크하우스 (Data Lakehouse) |
|:---|:---|:---|:---|
| 데이터 모델 | **정형 2차원 테이블 중심** | **정형, 반정형, 비정형 다형성** | **정형·반정형 테이블화 + 비정형 파일 직접 연동**|
| 트랜잭션 및 ACID| **엔진 내부 완전한 ACID 지원** | 트랜잭션 미지원 (일관성 없음) | **객체 스토리지 위에서 100% ACID 트랜잭션 보장**|
| 스토리지 및 포맷| 전용 독점 포맷 (고비용) | **오픈 포맷 Parquet/JSON (저비용)**| **오픈 테이블 포맷 (Delta/Iceberg/Parquet)** |
| 쿼리 엔진 호환성| 단일 벤더 전용 엔진 종속 | 다양한 오픈소스 엔진 연동 | **Spark, Trino, Python 등 모든 엔진 직접 쿼리** |

#### 한줄 요약
- DW의 정합성과 Lake의 유연성을 융합하여 단일 스토리지에서 모든 분석을 처리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Compaction & Vacuum**: 자잘한 파일을 512MB 표준 크기로 병합하는 `OPTIMIZE`와 보존 주기가 지난 과거 스냅샷 파일을 영구 삭제하는 `VACUUM`.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자잘한 파티션 파일 누적으로 인한 쿼리 성능 급락 | **`OPTIMIZE` (Bin-packing 컴팩션) 작업으로 512MB 파일 병합** | 메타데이터 조회 및 스캔 속도 5배 가속 |
| 타임 트래블 이력 누적으로 S3 스토리지 비용 폭증 | **`VACUUM` 명령을 주기적으로 실행하여 7일 이전 구버전 파일 삭제** | 미사용 스토리지 비용 50% 이상 절감 |
| 원천 데이터 구조 변경으로 인한 스키마 충돌 오류 | **`mergeSchema` 옵션 활성화를 통한 안전한 스키마 진화 허용** | 파이프라인 중단 없는 유연한 스키마 적응 |
| 다중 엔진 동시 쓰기 시 커밋 충돌(Conflict) 발생 | **파티션 세분화 및 멱등 MERGE 연산으로 충돌 범위 격리** | 동시 쓰기 성공률 극대화 |

#### 한줄 요약
- 파일 컴팩션, 진공 청소(Vacuum), 스키마 진화 옵션, 파티션 격리로 운영한다.

## Ⅶ. 결론

- 통합 분석은 **레이크하우스**, 트랜잭션은 **오픈 포맷** 선택

#### 한줄 요약
- 데이터 레이크하우스는 객체 스토리지의 경제성과 오픈 테이블 포맷의 ACID 정합성을 결합하여 현대 데이터 플랫폼의 표준으로 자리잡은 통합 아키텍처다.