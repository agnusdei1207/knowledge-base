---
title: "Iceberg Hudi Delta Lake Table Format"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 레이크의 "파일 형식(File Format)"과 "테이블 형식(Table Format)"을 분리하여, **Parquet/ORC 같은 컬럼형 파일 위에 메타데이터 계층과 트랜잭션 로그**를 얹음으로써 HDFS/S3 오브젝트 스토리지에서 **ACID 트랜잭션, 스키마 진화, 타임트래블, 히든 파티셔닝**을 가능케 한 것이다.
> 2. **가치**: 기존 데이터 레이크 대비 **소단위 파일 문제(Small File)·갱신/삭제 불가·동시성 충돌·쿼리 엔진 종속**이라는 4대 고질적 한계를 해소하여, **단일 데이터 소스로 BI·ML·스트리밍**을 통합하는 **레이크하우스(Lakehouse)** 아키텍처의 토대가 된다.
> 3. **판단 포인트**: Iceberg(엔진 중립·파티션 진화 강점), Hudi(레코드 단위 upsert·CDC·Incremental 강점), Delta Lake(Databricks 생태계·성능 최적화 성숙) 세 포맷은 **메타데이터 구조·머지 전략·트랜잭션 모델**이 근본적으로 다르므로, **워크로드 패턴(Batch/Streaming/CDC), 기존 엔진(Spark/Trino/Flink), 운영 거버넌스**에 따라 신중히 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 데이터 레이크의 한계와 테이블 형식의 등장

기존 데이터 레이크는 **HDFS, S3, ADLS, GCS 같은 오브젝트 스토리지**에 Parquet/ORC/Avro 같은 컬럼형 파일을 직접 dump하는 구조였다. 이 구조는 **저비용·무제한 확장**이라는 장점이 있었지만, 다음의 치명적 한계를 지녔다.

- **트랜잭션 부재**: 여러 작업이 동일 파일을 동시에 쓰면 데이터 손상·중복 발생. 디렉터리 단위의 원자성 보장 불가
- **스키마 강제력 부재**: Producer가 임의로 스키마를 변경하면 Consumer 전체 파이프라인이 깨짐
- **갱신/삭제 불가**: 데이터웨어하우스(StarRocks, Snowflake)와 달리 UPSERT/DELETE 미지원
- **작은 파일(Small File) 폭증**: 스트리밍/마이크로 배치로 인한 메타데이터 압박, NameNode/OBC 부하
- **쿼리 엔진 종속**: Hive Metastore + HiveQL에 종속, Presto/Trino/Flink 호환성 약화
- **시간 기반 조회(Time Travel) 불가**: 실수로 덮어쓴 데이터 복구 불가

2016~2019년 사이 Uber(Hudi), Netflix(Iceberg), Databricks(Delta Lake)가 거의 동시에 이 문제를 해결하기 위한 **테이블 형식(Table Format)** 표준을 제안했고, 이는 **Apache TLP(Top-Level Project)**로 성장해 데이터 엔지니어링 분야의 핵심 인프라로 자리잡았다.

```text
[기존 데이터 레이크: 파일 덤프 구조]

  Producer (Spark/Flink)              Consumer (Presto/Hive)
       |                                       |
       v                                       v
  +-----------------------------------------------------+
  |           S3 / HDFS 오브젝트 스토리지                  |
  |   /year=2024/month=01/day=01/part-0000.parquet      |
  |   /year=2024/month=01/day=01/part-0001.parquet      |
  |   /year=2024/month=01/day=02/part-0000.parquet      |
  |        ^                                            |
  |        |  "이 디렉터리가 곧 테이블이다" (no metadata)  |
  +-----------------------------------------------------+
   문제) ACID X, 스키마 강제 X, UPSERT X, 시간여행 X


[테이블 형식 적용 후: 메타데이터 계층 추가]

       +----------------------+
       |   Catalog (HMS/REST) | <---- 스키마, 현재 스냅샷 ID
       +----------+-----------+
                  v
       +----------------------+
       |  Metadata File       | <---- 파티션 스펙, 컬럼 통계
       |  (JSON / Avro)       |
       +----------+-----------+
                  v
       +----------------------+
       |  Manifest List       | <---- 데이터 파일 목록 + 통계
       |  (Avro)              |
       +----------+-----------+
                  v
  +--------------------------------------+
  |  Data Files (Parquet)                |
  |   - col stats (min/max/null count)   |
  |   - bloom filter, sort order         |
  +--------------------------------------+
   효과) ACID O, 스키마 강제 O, UPSERT O, 시간여행 O
```

### 1.2 패러다임 비교

```text
[Warehouse vs Lakehouse 진화]

  1세대 (1990s~)  ---  DW (Oracle/Teradata)
       |              장점: ACID, 고성능
       |              단점: 비쌈, 반정형 데이터 약함
       v
  2세대 (2010s~)  ---  Data Lake (S3 + Parquet)
       |              장점: 저비용, 무제한 확장
       |              단점: 품질·거버넌스 부재
       v
  3세대 (2019~)   ---  Lakehouse (Lake + Table Format)
       |              장점: 저비용 + 트랜잭션 + 오픈 포맷
       |              단점: 성숙도·툴링 격차, 작은 파일 문제 잔존
       v
  4세대 (2023~)   ---  Lakehouse + Iceberg REST / UniForm
                      엔진·벤더 종속 탈피, 멀티 클라우드 통합
```

- **📢 섹션 요약 비유**: 데이터 레이크는 **"대형 창고에 짐을 아무렇게나 쌓아두는 것"** 이고, 테이블 형식은 **"창고 안에 사물함(파티션)·재고대장(메타데이터)·CCTV(타임트래블)을 설치하는 것"** 이다. 짐(파일)은 그대로지만 관리 체계가 추가된 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Apache Iceberg

**역사**: Netflix 2017년 개발, 2018년 Apache Incubator, 2020년 TLP. **설계 철학**: "엔진에 종속되지 않는 테이블 표준".

```text
[Iceberg 아키텍처 상세]

  +------------------------------------------------------------+
  |                     Catalog Layer                          |
  |  (Hive Metastore / Glue / Nessie / REST / JDBC)            |
  |   - table identifier -> current metadata location            |
  +--------------------------+---------------------------------+
                             | (atomic swap)
                             v
  +------------------------------------------------------------+
  |                Metadata File (v2.metadata.json)            |
  |   format-version: 2                                        |
  |   table-uuid, location, last-column-id                     |
  |   schemas: [ v1, v2, ... ]    <--- 모든 스키마 이력         |
  |   partition-spec: [ day(ts), bucket(16, id) ]              |
  |   snapshots: [                                            |
  |     { snapshot-id: 9182, parent-id: 8147,                  |
  |       manifest-list: s3://.../snap-9182.avro },            |
  |     ...                                                    |
  |   ]                                                        |
  |   snapshot-log: [{ ts, snapshot-id }, ...]                |
  |   properties: { write.format.default, ... }                |
  +--------------------------+---------------------------------+
                             |
                             v
  +------------------------------------------------------------+
  |           Manifest List (snap-XXXX.avro)                   |
  |   +-- manifest-1.avro  (DataFile entries, partition spec)  |
  |   +-- manifest-2.avro  (DeleteFile entries - v2)           |
  |   +-- ...                                                  |
  |   각 manifest에 added_data_files_count,                   |
  |   existing_data_files_count, deleted_data_files_count      |
  +--------------------------+---------------------------------+
                             |
                             v
  +------------------------------------------------------------+
  |              Manifest File (manifest-N.avro)               |
  |   fields: status(0/1/2), snapshot_id, data_file{          |
  |      file_path, file_format, partition{...},               |
  |      record_count, file_size_in_bytes,                     |
  |      value_counts, null_value_counts,                      |
  |      lower_bounds, upper_bounds, key_metadata              |
  |   }                                                        |
  +--------------------------+---------------------------------+
                             |
                             v
  +------------------------------------------------------------+
  |           Data Files (Parquet/ORC/Avro)                   |
  |   - 컬럼 단위 min/max 통계 (Data Skipping)                  |
  |   - 삭제 파일(POSITION/Equality Deletes, v2)               |
  +------------------------------------------------------------+
```

**핵심 기능**

- **히든 파티셔닝(Hidden Partitioning)**: 사용자가 `WHERE event_date >= '2024-01-01'` 라고 쓰면 Iceberg는 `partition.transform = day(ts)` 자동 매핑. 사용자·쿼리 엔진이 파티션 컬럼을 몰라도 됨
- **파티션 진화(Partition Evolution)**: `month(ts)` -> `day(ts)`로 사양 변경 시 **데이터 재작성 없이** 스키마만 갱신 (spec_id만 증가)
- **스키마 진화**: 컬럼 추가·삭제·이름변경·순서변경·nullable 변경 모두 메타데이터 단위에서 처리
- **타임 트래블**: `AS OF TIMESTAMP` 또는 `VERSION AS OF <snapshot-id>` 로 과거 상태 조회
- **카탈로그 트랜잭션**: HMSTracker / REST 카탈로그 등에서 `compare-and-swap` 으로 원자적 메타데이터 스왑

### 2.2 Apache Hudi

**역사**: Uber 2016년 개발, 2020년 Apache TLP. **설계 철학**: "레코드 단위 변경을 효율적으로 처리하는 증분 처리 프레임워크".

```text
[Hudi 아키텍처: Timeline + File Slice]

  Timeline (불변 로그)
  +------------------------------------------------------------+
  |  20240101120000  commit  replacecommit  "ingest batch 1"  |
  |  20240101130000  deltacommit  "stream ingest"             |
  |  20240101140000  commit  replacecommit  "clustering"      |
  |  20240101150000  cleanup  "retain 10 commits"            |
  +------------------------------------------------------------+
           |
           v
  +------------------------------------------------------------+
  |  Hoodie Commit Metadata (.hoodie/ directory)              |
  |   +-- 20240101120000.commit                               |
  |   +-- 20240101120000.inflight                             |
  |   +-- 20240101130000.deltacommit                          |
  |   +-- .hoodie.properties (table config)                   |
  +--------------------------+---------------------------------+
                             |
                             v
  +------------------------------------------------------------+
  |             File Slice (record group)                      |
  |                                                             |
  |   +--------------+      +--------------+                  |
  |   | Base File    |      | Log File     |   (MoR 모드)      |
  |   | (Parquet)    | ----> | (.log, Avro) |                  |
  |   | part-0_1-... |      | .log.1_2-... |                  |
  |   +--------------+      +--------------+                  |
  |                                                             |
  |   File ID: part-0  Commit Time: 20240101_120000            |
  |   Write Token: 1-0-0                                       |
  +------------------------------------------------------------+
```

**핵심 기능**

- **테이블 타입**
  - **Copy-on-Write (CoW)**: 갱신 시 베이스 파일 전체 재기록. 읽기 빠름, 쓰기 비용 큼
  - **Merge-on-Read (MoR)**: 베이스 파일은 두고 **로그 파일**에 델타 기록. 읽기 시 머지 필요, 쓰기 빠름. Columnar 로그 가능(Hoodie Log File Format)
- **인덱스(Index)**: Bloom Filter, HBase, Simple, Global Bloom, Flink State 등. **레코드 키 -> 파일 ID** 매핑으로 UPSERT 시 모든 파일 스캔 방지
- **Incremental Query**: `incrementalQuery(startTime, endTime)` 로 두 커밋 사이의 변경분만 폴링
- **CDC**: `hoodie.datasource.query.type = incremental` + Debezium 통합으로 변경데이터 캡처
- **Clustering**: Z-order, linear, sort 등 **인라인/비동기 클러스터링**으로 작은 파일 정리
- **컨커런시 제어**: MultiWriter 시 `WRITE_CONFLICT` 정책 (block / fail / append)

### 2.3 Delta Lake

**역사**: Databricks 2019년 공개, 2020 Linux Foundation Delta Lake 프로젝트, 2024년 Delta Lake 3.x(UniForm) 발표. **설계 철학**: "Spark + 데이터 웨어하우스의 성능과 신뢰성을 오픈 포맷으로".

```text
[Delta Lake 아키텍처: _delta_log 트랜잭션 로그]

  +------------------------------------------------------------+
  |              _delta_log/  (트랜잭션 로그)                  |
  |                                                             |
  |   00000000000000000000.json   <--- 첫 커밋                   |
  |     { "metaData": { "schemaString": "...",                |
  |                     "partitionColumns": [...] },           |
  |       "add": { "path": "part-00000.parquet",              |
  |                 "size": 1024, "stats": "{...}" },          |
  |       "commitInfo": { "timestamp": ..., "operation": ... }|
  |     }                                                       |
  |                                                             |
  |   00000000000000000001.json   <--- 두 번째 커밋             |
  |     { "remove": { "path": "part-00000.parquet" },          |
  |       "add": { "path": "part-00001.parquet", ... },        |
  |       "txn": { "appId": "spark-app", "version": 1 }        |
  |     }                                                       |
  |                                                             |
  |   00000000000000000010.checkpoint.parquet   <--- 체크포인트  |
  |     (10개 커밋 단위 압축, 상태 스냅샷)                      |
  |                                                             |
  |   _last_checkpoint (메타 파일)                              |
  |     { "version": 10, "size": 1, "parts": 1 }               |
  +------------------------------------------------------------+
```

**핵심 기능**

- **DeltaLog**: 모든 변경을 **JSON 로그 + Parquet 체크포인트**로 저장. 단조 증가 version 번호
- **Optimistic Concurrency**: 읽기 시 snapshot
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 291 / 300

<- **이전**: [290. 파케이 ORC 열 지향 저장 포맷 최적화 (Parquet ORC Columnar Storage Format)](/studynote/14_data_engineering/05_exam_keywords/290_parquet_orc_columnar/)
**다음**: [292. 데이터 레이크하우스 메달리온 아키텍처 (Data Lakehouse Medallion Architecture)](/studynote/14_data_engineering/05_exam_keywords/292_lakehouse_medallion/) ->

---
