---
sidebar:
  order: 126
  label: "126. 데이터 레이크하우스 (Data Lakehouse)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터 레이크하우스 (Data Lakehouse)"
date: "2026-08-13T23:20:00+09:00"
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

- **Data Lakehouse (데이터 레이크하우스)**: 데이터 레이크(Data Lake)의 저비용 객체 스토리지 수평 확장성과, 데이터 웨어하우스(DW)의 100% ACID 트랜잭션 및 고성능 SQL 쿼리 관리 기능을 결합한 차세대 모던 데이터 아키텍처.
- **Open Table Format**: 객체 스토리지 파일 위에서 ACID 트랜잭션, 타임 트래블(Time Travel), 스키마 진화(Schema Evolution)를 가능케 해주는 오픈소스 메타데이터 표기 표준 (Delta Lake, Apache Iceberg, Apache Hudi).
- **Time Travel (타임 트래블)**: 테이블 메타데이터의 버전 스냅샷 이력을 추적하여, 과거 특정 시점의 데이터로 쿼리를 조율하거나 원복(Rollback)하는 기능.

</details>

- 정의/개념: 객체 스토리지와 관리형 테이블을 결합한 **레이크하우스**
- 배경/필요성: Lake•DW 이중 적재는 **복제 비용•버전 불일치** 유발

#### 한줄 요약

- 객체 스토리지에 ACID 테이블 메타데이터를 결합하여 여러 분석 엔진이 동일 테이블을 안전하게 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ACID Transactions on Object Storage**: 스냅숏 메타데이터로 원자적 테이블 변경 제공.
- **Decoupled Storage and Compute**: S3 스토리지 용량과 Spark/Presto 쿼리 엔진의 수평 분리.

</details>

- **Data Lake (S3/GCS 가성비) + Data Warehouse (ACID/SQL 성능) 융합**
- **Open Table Format (Delta Lake, Apache Iceberg, Apache Hudi) 수용**
- **Direct Access for Diversity Engines (Spark, Presto, FDS, Machine Learning 동시 접근)**

#### 한줄 요약

- 파일은 불변으로 저장하되 스냅숏 메타데이터가 현재 버전을 결정하므로 읽기 도중 테이블이 불완전하게 변경되지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ACID Transaction Log**: Parquet 데이터 파일들의 변경 이력을 JSON/AVRO 트랜잭션 로그로 기록하여 동시성 및 타임 트래블 제어.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     Data Lakehouse Unified Architecture                │
├────────────────────────────────────────────────────────────────────────┤
│ Diverse Engines: [Spark SQL]  [Presto/Trino]  [Databricks]  [ML Engine]│
├────────────────────────────────────────────────────────────────────────┤
│ Open Table Format Layer: [Delta Lake / Apache Iceberg / Hudi]          │
│  • ACID Transaction Log (JSON/AVRO Metadata) & Time Travel             │
│  • Schema Evolution & Enforcement                                      │
├────────────────────────────────────────────────────────────────────────┤
│ Storage Layer: Cloud Object Storage [AWS S3 / GCS / Azure ADLS]        │
│  • Parquet / ORC Columnar Data Files                                   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 다종의 쿼리 엔진이 Open Table Format 메타데이터 레이어를 경유하여 S3의 Parquet 파일에 ACID 및 고성능 SQL 연산을 수행하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 연산 엔진 | 공통 테이블 메타데이터로 읽기•쓰기 수행 |
| Open Table Format | 스냅숏•스키마•파티션•삭제 규칙 정의 |
| Metadata File | 데이터 파일 목록과 버전 이력 보관 |
| Catalog | 테이블 이름과 현재 메타데이터 위치 관리 |
| Object Storage | 불변 데이터•메타데이터 파일 저장 |

#### 한줄 요약

- 객체 스토리지, 테이블 메타데이터, 메타데이터 포인터, 연산 엔진, 거버넌스•유지관리로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Optimistic Concurrency Control (OCC)**: 동시 쓰기 시 락(Lock)을 걸지 않고, Commit 시점에 타 트랜잭션의 파일 변경 유무를 검사하여 충돌 시 자동 재시도하는 기법.

</details>

```text
[테이블 쓰기]
      │
      ▼
1. 기준 스냅숏 조회
      │
      ▼
2. 신규 데이터 파일 기록
      │
      ▼
3. 충돌 범위 검증
      │
      ▼
4. 새 메타데이터 생성
      │
      ▼
5. 현재 포인터 전환
```

### 동작 원리

1. **기준 스냅숏 조회**: 현재 버전과 대상 파일 범위 확인
2. **신규 데이터 파일 기록**: 변경 결과를 불변 파일로 생성
3. **충돌 범위 검증**: 기준 이후 동시 커밋과 겹침 검사
4. **새 메타데이터 생성**: 새 파일 목록•통계•스키마 기록
5. **현재 포인터 전환**: 원자 커밋 후 새 스냅숏 공개

#### 한줄 요약

- 새 데이터 파일과 스냅숏 메타데이터를 먼저 생성하고 마지막에 메타데이터 포인터만 원자적으로 전환하여 확정된 새 버전을 공개한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Architecture Evolution**: DW (정형 전용) $\rightarrow$ Data Lake (비정형 전용, 무질서) $\rightarrow$ Lakehouse (정형/비정형 통합 + ACID).

</details>

| 비교 항목 | Data Warehouse (DW) | Data Lake | Data Lakehouse |
|:---|:---|:---|:---|
| 데이터 형태 | **정형 분석 모델 중심** | **다양한 원천 파일** | 다양한 파일의 관리형 테이블 |
| 트랜잭션 | 엔진 관리 테이블 ACID | 파일 API 수준 | **테이블 포맷별 ACID 제공** |
| 스토리지/컴퓨팅 | 결합형 (고비용) | 완전 분리형 (가성비) | **완전 분리형 (가성비 + 고성능)** |
| 대표 기술 | Snowflake, Redshift | AWS S3, Hadoop HDFS | **Databricks, Iceberg, Delta Lake** |

#### 한줄 요약

- 레이크하우스는 객체 스토리지 위에 다중 엔진이 공유하는 ACID 테이블 메타데이터를 결합한 구조이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Vacuum Operation**: 타임 트래블 이력 기간이 지난 구버전 S3 쓰레기 Parquet 파일들을 주기적으로 삭제하여 디스크 비용을 정제하는 작업.

</details>

| 튜닝 영역 | 문제 및 위험 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. File Compaction | 자잘한 파티션 파일 누적 속도 폭락 | **`OPTIMIZE` (Bin-packing) 파일 병합 주기적 실행** |
| 2. Storage Cost | 타임 트래블 구버전 파일 무한 누적 | **`VACUUM` 명령으로 7일 이전 구버전 물리 파일 삭제** |
| 3. Schema Drift | 소스 데이터 컬럼 타입 예가없이 변경 | **`mergeSchema` 옵션으로 안전한 스키마 진화 허용** |

> 사례: **카카오 / 당근마켓 / Databricks Delta Lake 기반 전사 데이터 레이크하우스 구축**

#### 한줄 요약

- 새 데이터 파일을 모두 기록한 뒤 스냅숏으로 한 번에 공개하고 오래된 파일은 보존 기간 후 정리한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Lakehouse 수립 기준(Data Lakehouse Standards)**: S3 객체 스토리지, Delta Lake / Apache Iceberg Open Table Format, OCC 동시성 제어 및 Databricks/Trino 통합성에 의거한 체계.

</details>

- 다중 엔진 테이블 공유는 **Lakehouse**, 단순 원천 보관은 Lake 선택

#### 한줄 요약

- 하나의 객체 스토리지를 다중 엔진이 공유하려면 메타데이터 포인터와 충돌 규칙, 스냅숏 만료•파일 정리를 함께 관리해야 한다.
