+++
weight = 147
title = "147. Delta Lake — ACID 트랜잭션 지원 오픈 테이블 포맷"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. Delta Lake는 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]] 위에 **`_delta_log` [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]**를 추가하여 객체 스토리지에서 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) [[191_transaction_concept_states|트랜잭션]]을 실현한 [[191_oss_license_compliance|오픈소스]] 스토리지 레이어다.
2. `MERGE INTO`, `UPDATE`, `DELETE`, 타임 트래블(Time Travel), [[005_schema|스키마]] 진화([[505_schema|Schema]] Evolution)를 지원하여 [[146_lakehouse|레이크하우스]]의 핵심 구현 기술로 자리 잡았다.
3. Spark 네이티브로 설계되었고 현재는 Linux Foundation에 기증되어 Spark·Flink·Trino 등 멀티엔진으로 확산되고 있다.

---

## Ⅰ. 개요 및 필요성

객체 스토리지(S3, ADLS, GCS)는 저렴하고 확장성이 뛰어나지만, [[501_file_definition_logical_record|파일]] 기반이라 부분 수정이 불가능하고 [[014_concurrency|동시성]] 제어가 없다. 결과적으로 기존 [[208_data_lake_schema_on_read|데이터 레이크]]에서는 읽기/[[289_cqrs_db|쓰기]] 충돌, 중간 실패 시 [[001_dikw_pyramid|데이터]] 손상, 이력 추적 불가 등의 문제가 발생했다.

Databricks는 2019년 Delta Lake를 공개하여 이 문제를 해결했다. [[343_json|JSON]] 형식의 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 `_delta_log/` [[506_directory_structure_symbol_table|디렉터리]]에 순차적으로 기록함으로써, [[501_file_definition_logical_record|파일]] 수정 없이도 원자적 연산과 [[022_snapshot_backup_architecture|스냅샷]] 격리를 달성한다.

| 문제 (기존 레이크) | Delta Lake 해결책 |
|:---|:---|
| 부분 [[289_cqrs_db|쓰기]] 실패 시 오염 | 원자적 커밋 ([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]) |
| 동시 읽기/[[289_cqrs_db|쓰기]] 충돌 | [[223_optimistic_concurrency_control_validation|낙관적 동시성 제어]] (OCC) |
| 이전 [[001_dikw_pyramid|데이터]] [[658_ir_recovery|복구]] 불가 | 타임 트래블 (VERSION [[344_as_autonomous_system_asn|AS]] OF) |
| [[005_schema|스키마]] 불일치 오류 | [[005_schema|스키마]] 적용/진화 자동 관리 |

> 📢 **섹션 요약 비유**: 공유 메모장에 여러 사람이 동시에 글을 쓰면 엉망이 되는 문제를, Delta Lake는 각자 초안을 작성하고 순번 도장을 찍어 순서대로 반영하는 방식으로 해결한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────┐
│               Delta Lake 내부 구조                            │
├──────────────────────────────────────────────────────────────┤
│  객체 스토리지 버킷 (S3 / ADLS / GCS)                         │
│                                                              │
│  ┌─────────────────────────────┐  ┌──────────────────────┐  │
│  │  _delta_log/                │  │  데이터 파일 (Parquet) │  │
│  │  ├── 00000.json  (커밋 0)   │  │  ├── part-0001.parquet│  │
│  │  ├── 00001.json  (커밋 1)   │  │  ├── part-0002.parquet│  │
│  │  ├── 00002.json  (커밋 2)   │  │  └── ...             │  │
│  │  └── 00010.checkpoint.parquet│  └──────────────────────┘  │
│  └─────────────────────────────┘                            │
│                                                              │
│  커밋 로그 내용: {add/remove 파일 목록, 스키마, 통계, 타임스탬프} │
└──────────────────────────────────────────────────────────────┘
```

**주요 기능 상세**

| 기능 | SQL 문법 | 설명 |
|:---|:---|:---|
| Upsert | `MERGE INTO target USING source` | INSERT + UPDATE 원자적 처리 |
| 타임 트래블 | `SELECT * FROM t VERSION AS OF 5` | 과거 [[022_snapshot_backup_architecture|스냅샷]] 조회 |
| 타임 트래블 (시간) | `SELECT * FROM t TIMESTAMP AS OF '2026-01-01'` | 날짜 기준 과거 조회 |
| [[005_schema|스키마]] 진화 | `ALTER TABLE ... ADD COLUMN` | 기존 [[501_file_definition_logical_record|파일]] 재작성 없이 컬럼 추가 |
| Z-오더링 | `OPTIMIZE table ZORDER BY (col)` | 연관 컬럼 [[001_dikw_pyramid|데이터]] co-locating |
| 히스토리 조회 | `DESCRIBE HISTORY table` | 커밋 이력 전체 출력 |
| 진공 청소 | `VACUUM table RETAIN 168 HOURS` | 오래된 [[501_file_definition_logical_record|파일]] 물리적 삭제 |

> 📢 **섹션 요약 비유**: Delta Lake는 공증 사무소와 같다. 모든 변경 사항을 번호 순서로 공증 도장을 찍어 기록하므로, 언제든 과거의 특정 순간으로 돌아가거나 여러 명이 동시에 작업해도 기록이 꼬이지 않는다.

---

## Ⅲ. 비교 및 연결

**Delta Lake vs [[148_apache_iceberg|Apache Iceberg]] vs [[149_apache_hudi|Apache Hudi]]**

| 항목 | Delta Lake | [[148_apache_iceberg|Apache Iceberg]] | [[149_apache_hudi|Apache Hudi]] |
|:---|:---|:---|:---|
| 탄생 배경 | [[074_photon_engine|Databricks]] (2019) | Netflix (2018) | Uber (2019) |
| [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] | `_delta_log` ([[343_json|JSON]]) | Manifest + [[637_zfs_snapshot_cow_architecture|Snapshot]] | Timeline |
| [[514_partition_slice_volume|파티션]] 방식 | 명시적 [[514_partition_slice_volume|파티션]] | 히든 [[179_table_partitioning_concept|파티셔닝]] | [[514_partition_slice_volume|파티션]] [[154_database_index_b_tree_search_optimization|인덱스]] |
| 주요 강점 | Spark 생태계 성숙도 | 멀티엔진 표준화 | [[217_cdc_binlog_change_capture_debezium|CDC]]/upsert 특화 |
| 기본 [[501_file_definition_logical_record|파일]] 포맷 | [[178_parquet_rle_encoding_columnar_compression|Parquet]] | [[178_parquet_rle_encoding_columnar_compression|Parquet]] / ORC / Avro | [[178_parquet_rle_encoding_columnar_compression|Parquet]] / ORC |
| [[791_gdpr_eu|GDPR]] 지원 | VACUUM + DELETE | Row-level delete | 레코드 수준 삭제 |

**연관 기술 연결**

- **[[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]]**: Delta Lake의 Bronze/Silver/Gold 계층 구현 기반
- **AutoLoader**: 신규 [[501_file_definition_logical_record|파일]]을 자동 감지하여 Delta 테이블로 적재
- **[[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] (Delta Live Tables)**: 선언적 [[123_pipe|파이프]]라인 프레임워크
- **[[150_unity_catalog|Unity Catalog]]**: Delta Lake 테이블의 거버넌스 관리

> 📢 **섹션 요약 비유**: Delta Lake(Spark 전문가), Iceberg(전 회사 어디서나 쓰이는 범용 도구), Hudi([[217_cdc_binlog_change_capture_debezium|CDC]] 특화 전문가)는 같은 문제를 다른 관점에서 해결한다. 선택은 기존 엔진 생태계에 따라 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도입 시나리오**

- **[[217_cdc_binlog_change_capture_debezium|CDC]] [[212_synchronization_mechanisms|동기화]]**: MySQL/Postgres 변경 [[001_dikw_pyramid|데이터]]를 MERGE INTO로 레이크에 실시간 반영
- **[[791_gdpr_eu|GDPR]] 준수**: 사용자 삭제 요청을 DELETE로 처리, VACUUM으로 물리 삭제
- **스트리밍 + 배치 통합**: Spark Structured Streaming이 Delta 테이블에 [[289_cqrs_db|쓰기]], 배치 [[298_qkv_attention|쿼리]]가 읽기
- **소급 재처리**: 잘못된 변환 발견 시 VERSION [[344_as_autonomous_system_asn|AS]] OF로 과거 상태 [[658_ir_recovery|복구]] 후 재처리

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Delta Log 동작 원리 | 각 [[191_transaction_concept_states|트랜잭션]]을 [[343_json|JSON]] [[501_file_definition_logical_record|파일]]로 기록, 체크포인트(10개마다)로 [[347_compaction|압축]] |
| [[223_optimistic_concurrency_control_validation|낙관적 동시성 제어]] | 충돌 감지 시 재시도, [[289_cqrs_db|쓰기]] 충돌 없으면 원자적 커밋 |
| Small [[501_file_definition_logical_record|File]] 문제 해결 | `OPTIMIZE` 명령으로 소규모 [[501_file_definition_logical_record|파일]]을 128MB 단위로 병합 |
| 타임 트래블 한계 | VACUUM 실행 시 보존 기간(기본 7일) 이전 [[501_file_definition_logical_record|파일]] 삭제됨 |

> 📢 **섹션 요약 비유**: Delta Lake 운영은 은행 계좌 관리와 같다. 입출금(변경)마다 명세서([[568_logs_distributed_logging_elk_fluentd|로그]])를 남기고, 오래된 명세서는 주기적으로 정리(VACUUM)하되, 최신 잔액은 항상 정확하게 유지된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 향상 | ACID 보장으로 [[123_pipe|파이프]]라인 실패 시 부분 [[001_dikw_pyramid|데이터]] 오염 방지 |
| 운영 효율화 | MERGE INTO로 [[217_cdc_binlog_change_capture_debezium|CDC]] 구현 단순화, OPTIMIZE로 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] 향상 |
| 규정 준수 | [[791_gdpr_eu|GDPR]]/[[783_pipa_korea|개인정보보호법]] 대응을 위한 물리적 삭제 경로 확보 |
| 실험 재현성 | 타임 트래블로 ML 모델 학습 [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 고정 가능 |

Delta Lake는 [[191_oss_license_compliance|오픈소스]] [[146_lakehouse|레이크하우스]] 생태계의 선두 구현체로, [[074_photon_engine|Databricks]] 플랫폼 밖에서도 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], Trino, Flink 등 다양한 엔진에서 사용 가능하다. 기술사 시험에서는 **[[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] 구조**, **MERGE INTO 동작**, **타임 트래블 메커니즘**이 주요 출제 포인트다.

> 📢 **섹션 요약 비유**: Delta Lake는 [[208_data_lake_schema_on_read|데이터 레이크]]에 교통 [[130_signal|신호]]등을 설치한 것이다. [[130_signal|신호]]등이 없으면 차들이 충돌하지만, [[130_signal|신호]]등([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]])이 있으면 수천 대가 동시에 달려도 질서 있게 통행한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| `_delta_log` | 핵심 구성요소 | [[343_json|JSON]] [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] [[506_directory_structure_symbol_table|디렉터리]] |
| MERGE INTO | [[083_dml|DML]] 확장 | upsert 원자적 처리 |
| OPTIMIZE + Z-ORDER | [[282_performance_tactics|성능]] 최적화 | 소규모 [[501_file_definition_logical_record|파일]] 병합 + [[001_dikw_pyramid|데이터]] 클러스터링 |
| VACUUM | 유지 관리 | 만료 [[501_file_definition_logical_record|파일]] 물리 삭제 |
| AutoLoader | 수집 도구 | 신규 [[501_file_definition_logical_record|파일]] 자동 감지·적재 |
| [[150_unity_catalog|Unity Catalog]] | 거버넌스 | 테이블 수준 접근 제어·리니지 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[_delta_log (트랜잭션 로그)]
    │
    ▼
[MERGE INTO (Upsert)]
    │
    ▼
[OPTIMIZE + Z-ORDER]
    │
    ▼
[VACUUM (파일 정리)]
    │
    ▼
[AutoLoader]
```

이 흐름도는 _delta_log ([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]])에서 출발해 AutoLoader까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Delta Lake는 그림 일기장처럼 매일 무슨 일이 있었는지 날짜별로 기록해두는 특별한 저장소예요.
2. 일기를 잘못 쓴 날로 돌아가서 다시 읽을 수 있고, 여러 친구가 동시에 써도 겹치지 않아요.
3. 오래된 일기는 주기적으로 정리(VACUUM)해서 공간이 가득 차지 않게 깔끔히 유지한답니다.
