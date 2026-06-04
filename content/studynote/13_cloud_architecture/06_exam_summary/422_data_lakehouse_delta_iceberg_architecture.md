---
title: "422. 데이터 레이크하우스 델타 아이스버그 (Data Lakehouse Delta Iceberg Architecture)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 레이크하우스는 객체 스토리지(S3/ADLS/GCS) 기반의 오픈 트랜잭션 레이어(Delta Lake, Apache Iceberg, Apache Hudi)를 통해 Parquet/ORC 파일에 ACID 트랜잭션, 스키마 진화, 타임 트래블, 히든 파티셔닝을 제공하여 데이터 레이크의 유연성과 데이터 웨어하우스의 신뢰성·성능을 동시에 확보하는 하이브리드 아키텍처이다.
> 2. **가치**: 동일 데이터에 대해 BI(Snowflake, BigQuery), ML(Spark, Ray), Streaming(Kafka + Flink)이 동시 접근 가능하며, TPC-DS 벤치마크에서 2~10배의 쿼리 성능 향상, 스토리지 비용 60~80% 절감, ETL 단계 축소로 데이터 파이프라인 복잡도 50% 감소 효과를 제공한다.
> 3. **판단 포인트**: 메타데이터 카탈로그 선택(Unity Catalog vs Glue Data Catalog vs Nessie/JDBC), 컴팩션 전략(Optimize, Auto Compaction, Sort/Z-Order vs Bucket/Bin-Packing), 동시성 제어 모델(Optimistic Concurrency vs Serializable Isolation), 그리고 멀티 엔진 환경에서의 Iceberg REST Catalog 표준화 여부가 핵심 의사결정 요소이다.

---

## Ⅰ. 개요 및 필요성

기존 데이터 분석 환경은 두 가지 극단으로 분화되어 있었다. **데이터 웨어하우스**(Oracle Exadata, Teradata, Snowflake)는 고가의 MPP 엔진 위에서 컬럼형 압축, 머터리얼라이즈드 뷰, ACID 트랜잭션을 제공하지만 페타바이트급 비정형·반정형 데이터 처리에 비용·확장성 한계를 보였다. 반면 **데이터 레이크**(HDFS, AWS S3)는 HDFS에 Parquet/Avro/ORC 파일을 적재해 저비용·대용량 처리가 가능했으나, "**데이터 스왐프(Data Swamp)**" 문제, 즉 메타데이터 부재로 인한 무결성 훼손, 동시 쓰기 충돌, 스키마 드리프트, 거대한 소형 파일(Small File) 누적, 그리고 파티션 프루닝의 비효율성 등으로 실무 활용도가 급격히 저하되었다.

데이터 레이크하우스(Data Lakehouse)는 이러한 이분법을 극복하기 위해, 객체 스토리지의 파일 위에 **트랜잭션 메타데이터 레이어**를 얹는 방식(Databricks Delta Lake, 2019년 오픈소스 공개, Apache Iceberg 2018년 Netflix 개발, Apache Hudi 2017년 Uber 개발)으로 등장했다. 핵심 통찰은 *"파일은 데이터에, 메타데이터는 트랜잭션에"* 라는 분리 원칙이다. Parquet 같은 컬럼형 파일은 그대로 유지하되, `_delta_log/`, `metadata/` 같은 별도 메타데이터 디렉터리에 JSON/Avro 기반의 트랜잭션 로그와 매니페스트 리스트를 저장함으로써, 오픈 파일 포맷의 이식성과 데이터베이스의 격리성을 동시에 달성한다.

```text
   +---------------------------------------------------------------------+
   |           기존 패러다임 비교: 진화 과정 (Evolution)                  |
   +---------------------------------------------------------------------+

  [1세대: 데이터 웨어하우스]    [2세대: 데이터 레이크]      [3세대: 데이터 레이크하우스]
  (1990s~2010s)               (2010s)                    (2019~현재)
  +------------------+        +------------------+        +------------------+
  | Proprietary HW   |        | Object Storage   |        | Object Storage   |
  | +--------------+ |        |  +------------+  |        |  +------------+  |
  | |  Vertica    | |        |  | Parquet    |  |        |  | Parquet    |  |
  | |  Exadata    | |        |  | ORC/Avro   |  |        |  | (Raw)      |  |
  | |  Teradata   | |        |  | (Raw)      |  |        |  +-----+------+  |
  | |  Netezza    | |        |  +-----+------+  |        |        |         |
  | +--------------+ |        |        |         |        |  +-----v------+  |
  |  ACID, MV, Index |        |  No    |  No     |        |  | Tx-Log     |  |
  |  Cost: $$, Petab.|        |  Schema|  ACID   |        |  | (Delta/    |  |
  |  ^ Petabyte 시   |        |  Enforc|  Enforc |        |  |  Iceberg)  |  |
  |    비용 급증     |        |  ^ 파일|  ^ Data |        |  +-----+------+  |
  |                  |        |    단편|    Swamp|        |        |         |
  |                  |        |    화  |    화   |        |  +-----v------+  |
  |                  |        |        |         |        |  | Catalog    |  |
  |                  |        |        |         |        |  | (Unity/    |  |
  |                  |        |        |         |        |  |  Nessie)   |  |
  |                  |        |        |         |        |  +------------+  |
  +------------------+        +------------------+        +------------------+
        v                            v                              ^
      폐쇄적                    개방·저비용                       통합(개방+신뢰)
```

**왜 지금 필요한가?** GDPR/CCPA 등 데이터 거버넌스 규제 강화, ML 워크로드의 폭증, 실시간 스트리밍+배치의 통합 요구, 그리고 멀티 클라우드 전략(데이터 중립성) 채택이 맞물리면서, 단일 벤더 종속(Hive, Snowflake-only 등)에서 벗어나 **오픈 테이블 포맷 기반의 레이크하우스**가 사실상 표준으로 자리 잡고 있다. Databricks·Snowflake·AWS·Google·Confluent·Starburst 모두 Iceberg를, Databricks·Microsoft Fabric은 Delta를, Netflix·Apple·LinkedIn·Adobe는 Iceberg를, Uber·Amazon은 Hudi를 채택하여 양대 표준으로 수렴 중이다.

- **📢 섹션 요약 비유**: 데이터 레이크가 "공터에 책을 아무렇게나 쌓아둔 도서관"이었다면, 데이터 레이크하우스는 같은 책 더미 위에 "도서관 색인 시스템과 대출 대장, 그리고 분실 방지 시스템"을 얹은 것이다. 책 자체(Pa­rquet)는 그대로 두면서 카드(메타데이터)만 똑똑하게 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 메타데이터 레이어 아키텍처

Delta Lake와 Apache Iceberg는 모두 **"파일 위에 파일(메타데이터)을 얹는"** 구조를 채택하지만, 내부 메타데이터 모델은 상이하다.

```text
   +----------------------------------------------------------------------+
   |          Delta Lake vs Apache Iceberg 내부 구조 비교                  |
   +----------------------------------------------------------------------+

   [ Delta Lake Table ]                     [ Apache Iceberg Table ]
   +------------------------------+         +------------------------------+
   | s3://bucket/delta/tbl/       |         | s3://bucket/iceberg/tbl/     |
   |   +-- _delta_log/            |         |   +-- metadata/              |
   |   |    +-- 000000.json       |         |   |    +-- v1.metadata.json   |
   |   |    +-- 000001.json       |         |   |    +-- v2.metadata.json   |
   |   |    +-- 000001.checkpoint |         |   |    +-- v3.metadata.json   |
   |   |    +-- 000002.json       |         |   |    +-- snap-*.avro        |
   |   |    +-- 000010.checkpoint |         |   |    +-- ...                |
   |   +-- part-00000-...parquet  |         |   +-- data/                  |
   |   +-- part-00001-...parquet  |         |   |    +-- bucket=2024/       |
   |   +-- part-00099-...parquet  |         |   |    |    +-- 00xxx.parq    |
   |                              |         |   |    |    +-- 00yyy.parq    |
   | • 단일 JSON 체크포인트 +     |         |   |    +-- bucket=2025/...    |
   |   Parquet 체크포인트(10개)   |         |   +-- metadata/version-hint |
   | • 단일 manifest: 병목 가능   |         |                              |
   +------------------------------+         | • 계층형: manifest list --+  |
                                            |              manifest    |  |
                                            |              data file   |  |
                                            | • 다중 manifest로 확장성^ |  |
                                            +------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Storage Layer (Parquet/ORC)** | 실제 데이터 저장 | 컬럼형 압축(Snappy/Zstd), Predicate Pushdown, 벡터화 읽기. 대부분 Apache Parquet v2 포맷 사용. Iceberg는 ORC·Avro도 지원 |
| **Transaction Log (`_delta_log/`)** | Delta Lake의 변경 이력 | **JSON 체크포인트**(10개 커밋마다) -> **Parquet 체크포인트**(100개 커밋마다, 기본 10개=10 commit). 단조 증가하는 20자리 zero-padded 숫자. 모든 Reader/Writer가 이 로그를 폴링하여 스냅샷 격리 확보 |
| **Metadata Hierarchy** | Iceberg의 다층 메타데이터 | `metadata.json`(스키마·파티션 명세) -> `*-manifest.avro`(파일 목록과 파티션 튜플, 컬럼 통계) -> `*-manifest-list.avro`(스냅샷별 매니페스트 참조). **Cat-and-Mouse 구조**로 Reader/Writer 효율 동시 확보 |
| **Catalog (메타스토어)** | 테이블 위치·현재 스냅샷 추적 | Delta: Hive Metastore / Unity Catalog / Glue / PostgreSQL JDBC. Iceberg: **REST Catalog(Iceberg v2 표준, 2024 확립)**, Hive Metastore, AWS Glue, Nessie(Git-like 분기), Polaris(Snowflake), Unity Catalog. 카탈로그가 가장 중요한 SPOF |
| **Query Engine** | SQL/분석 실행 | Spark, Trino, Flink, Snowflake, BigQuery (Iceberg), Dremio, Starburst, Databricks SQL, Athena v3 (Iceberg). 동일 테이블을 다중 엔진이 동시 조회 |
| **Optimize/Compaction Service** | 소형 파일 병합·정렬 | Delta `OPTIMIZE`/`VACUUM`, Iceberg `rewrite_data_files`(Bin-Pack, Sort, Z-Order, Shuffle), Auto-Compaction(Photon/Databricks), Dremio Reflections |

### 2. 핵심 동작 메커니즘

**ACID 트랜잭션의 원리**: Writer는 트랜잭션 시작 시 카탈로그에서 현재 테이블 버전(`version=42`)을 읽고, 신규 데이터 파일을 S3에 쓴 뒤, 새 `_delta_log/00000000000000000043.json` 파일(예: `{"add":{"path":"part-000.parquet","size":..,"stats":"..","tags":{}}}`)을 원자적 put으로 기록한다. S3의 **최종적 일관성(Eventual Consistency)** 문제 해결을 위해 Delta는 Checkpoint(병합된 Parquet 스냅샷)와 CAS(Compare-And-Set) 시맨틱을, Iceberg는 **Optimistic Concurrency + Retry** 또는 Hadoop Lock Manager(파티션 레벨 Zookeeper lock) 옵션을 사용한다.

**Time Travel / Snapshot Isolation**:
- Delta: `SELECT * FROM tbl VERSION AS OF 42` 또는 `TIMESTAMP AS OF '2024-01-01'`
- Iceberg: `SELECT * FROM tbl FOR SYSTEM_TIME AS OF '2024-01-01'`, `FOR SYSTEM_VERSION AS OF 8123456789012345678`
내부적으로 `version=42` 시점의 메타데이터/매니페스트 파일을 재생(replay)하여 당시 상태를 재구성한다. 데이터 파일은 변경되지 않으므로 **MVCC(Multi-Version Concurrency Control)** 의 write-once-read-many 특성을 가진다.

**히든 파티셔닝(Hidden Partitioning) & 파티션 진화(Partition Evolution)**: Iceberg의 가장 혁신적 기능. 기존 Hive 스타일은 `PARTITIONED BY (dt string)` 시 파티션 컬럼을 SELECT에 명시해야 했다(`WHERE dt='2024-01-01'`). Iceberg는 메타데이터에 `transform=identity(year(ts))` 같은 변환 명세를 저장하여, 사용자가 `WHERE ts BETWEEN '2024-01-01' AND '2024-12-31'`를 작성하면 엔진이 **자동으로 year() 변환**을 적용하여 파티션 프루닝을 수행한다. 더 나아가 `month(ts)` -> `day(ts)`로 파티션 전략을 바꿔도 **데이터 재작성 없이** 메타데이터만 갱신한다(Partition Evolution).

**스키마 진화(Schema Evolution)**: Delta는 `overwriteSchema` 모드에서 컬럼 추가/삭제/순서변경/리네임(2023+), 타입 승격(`int -> bigint`, `float -> double`)을 지원. Iceberg는 `ALTER TABLE ... ADD/RENAME/REPLACE COLUMNS` 시 메타데이터에 `_id=N` 필드 ID를 부여하여 **컬럼 ID 기반 추적**을 수행하므로, 컬럼 이름이 바뀌어도 ID가 같으면 통계·파티션이 유지된다. 이는 Parquet 파일 내부의 필드 ID와도 일치하여 **컬럼 프로젝션과 통계 활용**을 일관되게 보장한다.

**데이터 스키핑(Data Skipping)**: 두 포맷 모두 파일 단위 컬럼 통계(하한값/상한값/Null 수)를 Parquet footer 또는 `stats` 필드에 저장한다. Iceberg는 추가로 **Puffin 파일**(v2 spec)에 NDV, Top-N, Bloom Filter, Theta Sketch 같은 풍부한 통계를 저장하여 고카디널리티 컬럼의 스킵 효율을 5~20배 향상시킨다.

### 3. 성능 튜닝 핵심 파라미터

| 파라미터 | Delta | Iceberg | 권장값/효과 |
| :--- | :--- | :--- | :--- |
| 타겟 파일 크기 | `optimize.targetFileSize` (기본 1GB) | `write.target-file-size-bytes` (기본 512MB) | 128MB~1GB. 1GB 초과 시 S3 GET 요청 병렬성 저하, 미만 시 메타데이터 비대화 |
| 컴팩션 빈도 | Auto Optimize (Spark Structured Streaming commit 시) | `commit.manifest-merge.enabled`, `commit.manifest.min-count-to-merge` | 스트리밍: 매 마이크로배치 / 배치: 시간/크기 트리거 |
| 정렬 키 | Z-Order(다차원 클러스터링) | Z-Order / Hilbert Curve / Sort / Bucket | Z-Order는 4~5개 컬럼까지 효과, 그 이상은 차원의 저주 발생 -> Hilbert 권장 |
| Vacuum 보존 | `vacuumRetentionHours` (기본 168h) | `history.expire.min-snapshots-to-keep`, `history.expire.max-ref-age-ms` | 7일(Time Travel) ~ 30일(감사) |
| 체크포인트 간격 | `checkpointInterval` (기본 10) | N/A (자동
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 422 / 800

<- **이전**: [421. 클라우드 데이터 레이크 S3 ADLS GCS](/studynote/13_cloud_architecture/06_exam_summary/421_cloud_data_lake_s3_adls_gcs/)
**다음**: [423. 클라우드 DW 빅쿼리 레드시프트 스노우플레이크](/studynote/13_cloud_architecture/06_exam_summary/423_cloud_dw_bigquery_redshift_snowflake/) ->

---
