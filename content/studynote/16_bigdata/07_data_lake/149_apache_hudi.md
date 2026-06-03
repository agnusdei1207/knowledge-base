---
title: 149. Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. Apache Hudi는 Uber가 MySQL → [[208_data_lake_schema_on_read|데이터 레이크]] [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) [[212_synchronization_mechanisms|동기화]] 문제를 해결하기 위해 만든 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]으로, **Upsert(Update + Insert)와 Delete를 레이크에서 직접 수행**할 수 있게 한다.
2. **[[542_cow_file_system|COW]] ([[542_cow_file_system|Copy-on-Write]], 읽기 최적화)**와 **MOR (Merge-on-Read, [[289_cqrs_db|쓰기]] 최적화)** 두 가지 테이블 유형을 제공하여 워크로드 특성에 맞는 [[282_performance_tactics|성능]] 트레이드오프를 선택할 수 있다.
3. **Timeline (커밋 이력 [[568_logs_distributed_logging_elk_fluentd|로그]])**과 **Incremental Query**를 통해 마지막 체크포인트 이후 변경분만 처리하는 효율적인 증분 [[123_pipe|파이프]]라인 구현이 가능하다.

---

## Ⅰ. 개요 및 필요성

Uber는 수천 개의 MySQL 테이블을 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[208_data_lake_schema_on_read|데이터 레이크]]에 [[212_synchronization_mechanisms|동기화]]해야 했다. 전통적인 배치 ETL은 전체 테이블을 매일 덮어쓰는 방식으로, 테이블 크기가 증가할수록 비용이 급증하는 문제가 있었다. 또한 라이더/드라이버 [[001_dikw_pyramid|데이터]] 삭제([[781_personal_information|개인정보]] [[571_protection_vs_security|보호]]법) 요청에 대응하기 위한 레코드 단위 삭제 기능도 필요했다.

Uber는 2016년 Hudi를 개발하여 레이크에서 [[217_cdc_binlog_change_capture_debezium|CDC]] 기반 실시간 upsert를 가능하게 했고, 2019년 Apache 재단에 기증했다.

| 문제 (기존 레이크) | Hudi 해결책 |
|:---|:---|
| [[217_cdc_binlog_change_capture_debezium|CDC]] 반영 = 전체 재작성 | Upsert API로 변경 레코드만 처리 |
| 레코드 삭제 불가 | Hard Delete (물리) / Soft Delete ([[369_logic_bomb|논리]]) |
| 변경분 재처리 | Incremental Query로 타임라인 구간 조회 |
| 읽기/[[289_cqrs_db|쓰기]] [[282_performance_tactics|성능]] 선택 | [[542_cow_file_system|COW]](읽기 최적) vs MOR([[289_cqrs_db|쓰기]] 최적) |

> 📢 **섹션 요약 비유**: 기존 레이크는 메모장을 수정할 때마다 전체를 복사하던 방식이었고, Hudi는 수정 내용만 포스트잇으로 붙여두었다가 주기적으로 정리하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────────────────┐
│                  Apache Hudi 내부 구조                           │
├─────────────────────────────────────────────────────────────────┤
│  .hoodie/  (Timeline)                                           │
│  ├── 20260421120000.commit    (완료된 커밋)                      │
│  ├── 20260421120000.clean     (클리너 실행 이력)                 │
│  └── 20260421120000.compaction (컴팩션 이력)                     │
│                                                                 │
│  COW (Copy-on-Write) 테이블:                                    │
│  ┌───────────┐  Write    ┌─────────────────┐                   │
│  │ 변경 레코드│ ────────▶ │ 파일 전체 재작성 │ (base Parquet)    │
│  └───────────┘           └─────────────────┘                   │
│                                                                 │
│  MOR (Merge-on-Read) 테이블:                                    │
│  ┌───────────┐  Write    ┌────────────────┐                    │
│  │ 변경 레코드│ ────────▶ │ Delta Log 파일  │ (.log, Avro)      │
│  └───────────┘           └───────┬────────┘                    │
│                                  │ 읽기 시 병합                  │
│                         ┌────────▼────────┐                    │
│                         │ Base Parquet +  │                     │
│                         │ Delta Log 병합  │                     │
│                         └─────────────────┘                    │
│                          (주기적 Compaction으로 병합 고정)        │
└─────────────────────────────────────────────────────────────────┘
```

**[[542_cow_file_system|COW]] vs MOR 비교**

| 항목 | [[542_cow_file_system|COW]] ([[542_cow_file_system|Copy-on-Write]]) | MOR (Merge-on-Read) |
|:---|:---|:---|
| [[289_cqrs_db|쓰기]] 방식 | 변경 행 포함 [[501_file_definition_logical_record|파일]] 전체 재작성 | Delta Log [[501_file_definition_logical_record|파일]]에 추가만 |
| 읽기 방식 | [[178_parquet_rle_encoding_columnar_compression|Parquet]] 직접 읽기 (빠름) | Base + Delta 병합 (느림) |
| [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]] | 높음 ([[501_file_definition_logical_record|파일]] 재작성 비용) | 낮음 ([[568_logs_distributed_logging_elk_fluentd|로그]] 추가만) |
| 읽기 [[015_지연_데이터_관점|지연]] | 낮음 | [[347_compaction|Compaction]] 전까지 높음 |
| 적합 워크로드 | 읽기 집중, 배치 [[217_cdc_binlog_change_capture_debezium|CDC]] | [[289_cqrs_db|쓰기]] 집중, 실시간 [[217_cdc_binlog_change_capture_debezium|CDC]] |
| [[347_compaction|Compaction]] 필요 | 없음 | 필요 (주기적 [[568_logs_distributed_logging_elk_fluentd|로그]] 정리) |

> 📢 **섹션 요약 비유**: COW는 수정 때마다 새 책을 통째로 인쇄하는 방식(읽기 빠름)이고, MOR은 수정 내용을 포스트잇으로 붙여두는 방식([[289_cqrs_db|쓰기]] 빠름)이다. 독자가 많으면 [[542_cow_file_system|COW]], 편집이 잦으면 MOR을 선택한다.

---

## Ⅲ. 비교 및 연결

**Hudi [[298_qkv_attention|쿼리]] 타입 (3가지)**

| [[298_qkv_attention|쿼리]] 타입 | 설명 | 사용 목적 |
|:---|:---|:---|
| [[637_zfs_snapshot_cow_architecture|Snapshot]] Query | 최신 [[022_snapshot_backup_architecture|스냅샷]] 전체 조회 | 일반 조회, BI |
| Incremental Query | 특정 시간 구간의 변경분만 조회 | [[217_cdc_binlog_change_capture_debezium|CDC]] [[123_pipe|파이프]]라인, 증분 처리 |
| Read-Optimized Query | Base [[501_file_definition_logical_record|파일]]만 읽기 (MOR에서 Delta 무시) | 높은 읽기 [[282_performance_tactics|성능]] 필요 시 |

**Hudi vs [[147_delta_lake|Delta Lake]] vs Iceberg**

| 항목 | Hudi | [[147_delta_lake|Delta Lake]] | Iceberg |
|:---|:---|:---|:---|
| 주요 강점 | [[217_cdc_binlog_change_capture_debezium|CDC]]/upsert 특화, 증분 처리 | Spark 생태계 성숙도 | 멀티엔진 표준, 히든 [[179_table_partitioning_concept|파티셔닝]] |
| [[289_cqrs_db|쓰기]] 방식 선택 | [[542_cow_file_system|COW]] / MOR 선택 가능 | [[542_cow_file_system|COW]] 방식 | [[542_cow_file_system|COW]] 방식 (행 삭제 [[501_file_definition_logical_record|파일]] 별도) |
| 증분 처리 [[014_api_posix|API]] | Incremental Query 공식 지원 | 체인지 [[001_dikw_pyramid|데이터]] 피드(CDF) | 증분 스캔 [[014_api_posix|API]] |
| 주요 채택 | Cloudera, AWS EMR | [[074_photon_engine|Databricks]] | AWS Athena, [[541_cassandra|Snowflake]] |

> 📢 **섹션 요약 비유**: Hudi는 택배 기사처럼 변경된 물건만 빠르게 교체 배달하는 방식이고, Delta Lake는 수정 내용을 일기장에 기록해두는 방식이며, Iceberg는 거대한 창고를 어떤 운송 업체든 동일하게 이용할 수 있게 하는 표준 물류 규격이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**주요 활용 시나리오**

- **[[791_gdpr_eu|GDPR]] 삭제**: Hard Delete API로 특정 사용자의 모든 레코드를 레이크에서 물리 삭제
- **실시간 [[217_cdc_binlog_change_capture_debezium|CDC]]**: Debezium → [[179_kafka_flink_watermark_time_window|Kafka]] → [[061_structured_streaming|Spark Structured Streaming]] → Hudi MOR 테이블 upsert
- **증분 배치**: 매시간 Incremental Query로 변경분만 읽어 하위 집계 테이블 갱신
- **대용량 upsert**: 수억 건의 MySQL 테이블을 Hudi로 매일 delta [[212_synchronization_mechanisms|동기화]]

**핵심 운영 [[150_task|태스크]]**

| [[150_task|태스크]] | 설명 | Hudi [[014_api_posix|API]] |
|:---|:---|:---|
| [[347_compaction|Compaction]] | MOR [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]을 Parquet로 병합 | `HoodieCompactionJob` |
| Cleaning | 만료 [[501_file_definition_logical_record|파일]] [[288_version_ihl_tos_total_length|버전]] 정리 | `HoodieCleanJob` |
| [[105_clustering_analysis|Clustering]] | [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]] 정렬·통합 | `HoodieClusteringJob` |
| [[154_database_index_b_tree_search_optimization|Index]] 관리 | 레코드 키 → [[501_file_definition_logical_record|파일]] 위치 매핑 | Bloom/Bucket/Record Level |

> 📢 **섹션 요약 비유**: Hudi 운영은 슈퍼마켓 재고 관리와 같다. 팔린 상품만 재입고(upsert)하고, 유통기한 만료 상품은 폐기(cleaning)하며, 주기적으로 진열대를 정리([[347_compaction|compaction]])하여 쇼핑([[298_qkv_attention|쿼리]])이 빠르게 되도록 유지한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [[217_cdc_binlog_change_capture_debezium|CDC]] 실시간화 | 배치 전체 재작성 → 변경분만 upsert로 [[015_지연_데이터_관점|지연]] 수 시간 → 수 분 단축 |
| 스토리지 효율 | 전체 테이블 복사 제거로 스토리지 사용량 30~60% 절감 |
| 규정 준수 | [[791_gdpr_eu|GDPR]]·[[800_ccpa|CCPA]] 삭제 요구를 레이크 단계에서 직접 처리 |
| 증분 [[123_pipe|파이프]]라인 | Incremental Query로 하위 [[123_pipe|파이프]]라인 컴퓨팅 비용 대폭 감소 |

Apache Hudi는 CDC와 upsert가 핵심 요건인 [[208_data_lake_schema_on_read|데이터 레이크]] 환경에서 독보적인 강점을 가진다. [[042_cloudera_cdp_platform|Cloudera CDP]], AWS EMR, Google Dataproc에서 기본 지원하며, [[791_gdpr_eu|GDPR]] 대응과 실시간 CDC가 요건인 프로젝트에서 [[147_delta_lake|Delta Lake]], Iceberg와 함께 1순위 후보다. 기술사 시험에서는 **[[542_cow_file_system|COW]] vs MOR 트레이드오프**, **Timeline 구조**, **Incremental Query 활용**이 핵심 논점이다.

> 📢 **섹션 요약 비유**: Hudi는 [[208_data_lake_schema_on_read|데이터 레이크]]에 외과 수술 능력을 부여한 것이다. 기존에는 환자 전체를 교체(전체 재작성)해야 했다면, Hudi는 아픈 세포(변경 레코드)만 정밀하게 교체할 수 있게 된다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[542_cow_file_system|COW]] 테이블 | 핵심 설계 | [[289_cqrs_db|쓰기]] 시 전체 [[501_file_definition_logical_record|파일]] 재작성, 읽기 최적 |
| MOR 테이블 | 핵심 설계 | 델타 [[568_logs_distributed_logging_elk_fluentd|로그]] 추가 방식, [[289_cqrs_db|쓰기]] 최적 |
| Timeline | [[012_metadata|메타데이터]] 구조 | `.hoodie/` 내 커밋·클린·컴팩션 이력 |
| Incremental Query | [[298_qkv_attention|쿼리]] 타입 | 특정 구간 변경분만 조회 |
| [[347_compaction|Compaction]] | 운영 [[150_task|태스크]] | MOR [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] → [[178_parquet_rle_encoding_columnar_compression|Parquet]] 병합 |
| [[791_gdpr_eu|GDPR]] 삭제 | 활용 사례 | Hard Delete API로 레코드 물리 삭제 |

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS]
    │
    ▼
[Delta Lake]
    │
    ▼
[Apache Hudi]
    │
    ▼
[Copy-on-Write]
    │
    ▼
[Merge-on-Read]
    │
    ▼
[Data Lakehouse]
```

[[013_hdfs|HDFS]] 기반 [[208_data_lake_schema_on_read|데이터 레이크]]에서 ACID와 증분 처리 요구가 더해지며 Hudi와 [[146_lakehouse|레이크하우스]] 아키텍처로 발전하는 흐름이다.

---

### 👶 어린이를 위한 3줄 비유 설명
1. Hudi는 일기장에서 틀린 글자만 수정 테이프로 고치는 방식이에요. 전체 일기를 다시 쓸 필요가 없답니다.
2. 수정 내용을 빠르게 적고 싶으면 MOR(포스트잇 방식), 나중에 읽기 편하게 하고 싶으면 [[542_cow_file_system|COW]](완성본 인쇄 방식)을 골라요.
3. 주기적으로 포스트잇을 정리해서 일기장에 깔끔하게 붙이는 작업([[347_compaction|Compaction]])도 해줘야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 149 / 262

← **이전**: [[148_apache_iceberg|148. Apache Iceberg — 오픈 테이블 포맷 히든 파티셔닝]]
**다음**: [[150_unity_catalog|150. Unity Catalog (Databricks) — 레이크하우스 통합 거버넌스]] →

---
