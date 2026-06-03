+++
weight = 225
title = "225. 델타 레이크 / Apache Iceberg / Apache Hudi"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[147_delta_lake|Delta Lake]]·Iceberg·Hudi는 [[494_object_storage|오브젝트 스토리지]](S3) 위의 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]들에 **ACID [[191_transaction_concept_states|트랜잭션]]·타임트래블·[[005_schema|스키마]] 진화**라는 DB 수준 [[012_metadata|메타데이터]] 레이어를 추가하는 오픈 소스 테이블 포맷이다.
> 2. **가치**: 기존에는 S3에 쌓인 [[501_file_definition_logical_record|파일]]이 "그냥 [[501_file_definition_logical_record|파일]] [[459_dummy_test_double|더미]]"였다면, 이제는 **[[288_version_ihl_tos_total_length|버전]] 관리 가능한 [[191_transaction_concept_states|트랜잭션]] 테이블**로 동작하여 [[276_write_through|동시 쓰기]] 충돌과 부분 실패로 인한 [[001_dikw_pyramid|데이터]] 오염 문제를 해소한다.
> 3. **판단 포인트**: Delta Lake는 [[074_photon_engine|Databricks]] 통합 최적화, Iceberg는 멀티 엔진 범용성, Hudi는 [[217_cdc_binlog_change_capture_debezium|CDC]]·Upsert 특화라는 각자의 강점이 있으므로 **워크로드 특성**에 따라 선택한다.

---

## Ⅰ. 개요 및 필요성

S3 같은 [[494_object_storage|오브젝트 스토리지]]는 저렴하고 확장성이 뛰어나지만, 기본적으로는 "[[501_file_definition_logical_record|파일]]을 저장하는 버킷"일 뿐이다. 여러 Spark 잡이 동시에 같은 디렉토리에 쓰면 [[501_file_definition_logical_record|파일]] 충돌이 발생하고, 파이프라인이 중간에 실패하면 불완전한 [[501_file_definition_logical_record|파일]]이 남아 [[001_dikw_pyramid|데이터]]가 오염된다.

**오픈 테이블 포맷이 해결하는 문제:**

```
[오브젝트 스토리지 기본 문제]
Writer-1 ──▶ S3/data/ ◀── Writer-2  (동시 쓰기 충돌)
파이프라인 실패 후 S3에 불완전 Parquet 파일 잔류
스키마 변경 시 이전 파일과 호환성 깨짐
어제 실행 결과 재현 불가 (타임트래블 없음)

[오픈 테이블 포맷 도입 후]
┌──────────────────────────────────┐
│   S3 Parquet 파일들              │
│     + 트랜잭션 로그(_delta_log/) │  ← Delta Lake
│     + 메타데이터 파일(metadata/) │  ← Iceberg
│     + 타임라인 로그(.hoodie/)    │  ← Hudi
└──────────────────────────────────┘
       ↑ "이 레이어가 있으면 DB처럼 동작"
```

📢 **섹션 요약 비유**: S3는 창고이고, 오픈 테이블 포맷은 창고에 설치한 재고 관리 시스템([[081_erp_enterprise_resource_planning|ERP]])이다. 창고 자체는 변하지 않지만, ERP가 있으면 어떤 물건이 언제 들어오고 나갔는지 추적하고, 실수로 잘못 입고된 물건을 되돌릴 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[147_delta_lake|Delta Lake]] 아키텍처

```
┌────────────────────────────────────────────────────┐
│               Delta Lake 구조                       │
│                                                    │
│  S3 버킷: s3://bucket/tables/orders/               │
│  ├── _delta_log/                                   │
│  │   ├── 00000000000000000000.json  ← 버전 0 (CREATE)│
│  │   ├── 00000000000000000001.json  ← 버전 1 (INSERT)│
│  │   ├── 00000000000000000002.json  ← 버전 2 (UPDATE)│
│  │   └── 00000000000000000010.checkpoint.parquet  │
│  ├── part-00000-xxx.snappy.parquet  ← 실제 데이터  │
│  ├── part-00001-xxx.snappy.parquet                 │
│  └── part-00002-xxx.snappy.parquet                 │
└────────────────────────────────────────────────────┘
         ↑ Delta Log가 ACID 트랜잭션 구현의 핵심
```

### 핵심 기능 상세

| 기능 | 구현 원리 |
|:---|:---|
| **ACID [[191_transaction_concept_states|트랜잭션]]** | Delta Log에 원자적 [[343_json|JSON]] 커밋. Optimistic [[266_other_transparency|Concurrency]] Control로 [[276_write_through|동시 쓰기]] 충돌 감지 |
| **타임트래블** | `VERSION AS OF N` 또는 `TIMESTAMP AS OF` → Delta Log의 특정 [[288_version_ihl_tos_total_length|버전]] [[501_file_definition_logical_record|파일]] 목록 재구성 |
| **[[005_schema|스키마]] 진화** | 새 컬럼 추가(ADD COLUMN) 시 기존 [[501_file_definition_logical_record|파일]]은 NULL로 읽기, 상위 [[344_compatibility_usability|호환성]] 유지 |
| **Upsert (MERGE)** | `MERGE INTO` SQL 구문으로 INSERT+UPDATE+DELETE 원자 처리 |
| **Z-Ordering** | 다차원 클러스터링으로 자주 쿼리되는 컬럼 기준 [[501_file_definition_logical_record|파일]] 정렬 → Skip 효율 ↑ |
| **OPTIMIZE + VACUUM** | 소형 [[501_file_definition_logical_record|파일]] 병합(OPTIMIZE), 오래된 [[288_version_ihl_tos_total_length|버전]] 삭제(VACUUM) |

### Delta vs Iceberg vs Hudi 아키텍처 비교

```
[Delta Lake]          [Apache Iceberg]       [Apache Hudi]
_delta_log/           metadata/              .hoodie/
├─ 버전별 JSON        ├─ v1.metadata.json    ├─ 타임라인 파일
│  커밋 로그          ├─ snap-xxx.avro       ├─ .commit
│  (추가/삭제 파일)   │  (스냅샷)             ├─ .deltacommit
└─ checkpoint        └─ manifest-xxx.avro   └─ .replacecommit

특화: Databricks 통합  특화: 멀티엔진 범용    특화: Upsert/CDC
```

📢 **섹션 요약 비유**: Delta Log는 은행 거래 내역서와 같다. 계좌 잔액(현재 [[001_dikw_pyramid|데이터]])만 보는 게 아니라, 모든 거래 이력(Delta Log)이 있으니 언제든 특정 시점 잔액(타임트래블)을 재현할 수 있다.

---

## Ⅲ. 비교 및 연결

### 세 포맷 심층 비교

| 비교 항목 | [[147_delta_lake|Delta Lake]] | [[148_apache_iceberg|Apache Iceberg]] | [[149_apache_hudi|Apache Hudi]] |
|:---|:---|:---|:---|
| **개발 기원** | [[074_photon_engine|Databricks]] (2019) | Netflix (2018) | Uber (2019) |
| **[[012_metadata|메타데이터]] 형식** | [[343_json|JSON]] [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] | Avro/[[178_parquet_rle_encoding_columnar_compression|Parquet]] [[022_snapshot_backup_architecture|스냅샷]] | Avro 타임라인 |
| **ACID** | OCC 기반 | OCC 기반 | OCC/[[449_mvcc|MVCC]] |
| **타임트래블** | VERSION/TIMESTAMP | [[637_zfs_snapshot_cow_architecture|SNAPSHOT]]/TAG | [[200_savepoint_partial_rollback|SAVEPOINT]] |
| **[[005_schema|스키마]] 진화** | 추가·변경 지원 | 추가·변경·삭제 지원 | 추가 지원 |
| **[[217_cdc_binlog_change_capture_debezium|CDC]]/Upsert** | MERGE INTO | MERGE INTO | 네이티브 Upsert |
| **컴퓨팅 엔진** | Spark (주), Trino | Spark, Flink, Trino | Spark, Flink |
| **소형 [[501_file_definition_logical_record|파일]] 관리** | OPTIMIZE | REWRITE | 자동 [[347_compaction|압축]] |
| **삭제 방식** | [[542_cow_file_system|Copy-on-Write]] | [[542_cow_file_system|Copy-on-Write]]/MOR | [[542_cow_file_system|Copy-on-Write]]/MOR |
| **적합 사례** | [[074_photon_engine|Databricks]] ML+BI | 멀티클라우드, [[541_cassandra|Snowflake]] | [[217_cdc_binlog_change_capture_debezium|CDC]] 실시간 [[212_synchronization_mechanisms|동기화]] |

### [[542_cow_file_system|Copy-on-Write]] vs Merge-on-Read

| 방식 | [[289_cqrs_db|쓰기]] 시점 | 읽기 [[282_performance_tactics|성능]] | [[289_cqrs_db|쓰기]] [[282_performance_tactics|성능]] |
|:---|:---|:---|:---|
| **[[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|CoW]])** | 변경 [[501_file_definition_logical_record|파일]] 전체 재작성 | 빠름 (최적화 [[501_file_definition_logical_record|파일]]) | 느림 ([[501_file_definition_logical_record|파일]] 재작성) |
| **Merge-on-Read (MoR)** | 변경 내역만 별도 [[568_logs_distributed_logging_elk_fluentd|로그]] 저장 | 보통 (읽기 시 병합) | 빠름 |

📢 **섹션 요약 비유**: Copy-on-Write는 노트를 수정할 때마다 새 노트에 전체를 다시 쓰는 것(읽기 빠름), Merge-on-Read는 포스트잇(변경 내역)만 덧붙이고 나중에 정리하는 것([[289_cqrs_db|쓰기]] 빠름)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선택 가이드라인

| 상황 | 권장 포맷 | 이유 |
|:---|:---|:---|
| [[074_photon_engine|Databricks]] 플랫폼 사용 | [[147_delta_lake|Delta Lake]] | 네이티브 통합, [[180_mlflow|MLflow]] 연동 |
| 멀티 엔진 (Spark+Flink+Trino) | [[148_apache_iceberg|Apache Iceberg]] | 엔진 독립적 설계 |
| MySQL/PostgreSQL [[217_cdc_binlog_change_capture_debezium|CDC]] 실시간 [[212_synchronization_mechanisms|동기화]] | [[149_apache_hudi|Apache Hudi]] | Upsert [[282_performance_tactics|성능]] 최적화 |
| [[541_cassandra|Snowflake]] 외부 테이블 연동 | [[148_apache_iceberg|Apache Iceberg]] | [[541_cassandra|Snowflake]] 네이티브 지원 |
| AWS EMR 기반 | Delta 또는 Iceberg | AWS EMR 두 포맷 모두 지원 |

### 실무 주요 운영 명령 ([[147_delta_lake|Delta Lake]] 기준)

```sql
-- 타임트래블 조회
SELECT * FROM orders VERSION AS OF 5;
SELECT * FROM orders TIMESTAMP AS OF '2024-01-01';

-- 소형 파일 병합 (OPTIMIZE)
OPTIMIZE orders ZORDER BY (customer_id, order_date);

-- 오래된 버전 파일 삭제 (VACUUM)
VACUUM orders RETAIN 168 HOURS;  -- 7일 보관

-- 스키마 진화 (컬럼 추가)
ALTER TABLE orders ADD COLUMNS (discount_rate DOUBLE);

-- 증분 데이터 UPSERT (MERGE)
MERGE INTO orders AS target
USING new_orders AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

📢 **섹션 요약 비유**: OPTIMIZE는 서랍 정리, VACUUM은 오래된 영수증 버리기다. 서랍이 지저분하면(소형 [[501_file_definition_logical_record|파일]] 난립) 물건 찾기 느리고, 영수증이 넘치면(오래된 [[288_version_ihl_tos_total_length|버전]]) 서랍이 꽉 차니 주기적으로 관리가 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **[[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]** | [[276_write_through|동시 쓰기]] 충돌·부분 실패 오염 제거, ACID 보장 |
| **규정 [[606_auditing_linux_auditd|감사]] 대응** | 타임트래블로 특정 시점 [[001_dikw_pyramid|데이터]] 재현 ([[791_gdpr_eu|GDPR]] Right to Erasure 포함) |
| **운영 비용 절감** | [[209_data_warehouse_schema_on_write|DW]]+레이크 이중 구조 → 단일 [[146_lakehouse|레이크하우스]]로 통합 |
| **ML 파이프라인 안정성** | [[165_feature_store_training_serving_consistency|피처 스토어]] [[001_dikw_pyramid|데이터]]의 [[288_version_ihl_tos_total_length|버전]] 관리로 모델 재현성 확보 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **Small Files 문제** | 스트리밍/빈번 [[289_cqrs_db|쓰기]] 시 소형 [[501_file_definition_logical_record|파일]] 폭발 → OPTIMIZE 필수 |
| **[[012_metadata|메타데이터]] 오버헤드** | Delta Log [[501_file_definition_logical_record|파일]]이 수천만 [[501_file_definition_logical_record|파일]] 시 조회 [[015_지연_데이터_관점|지연]] |
| **벤더 의존** | Delta Lake는 [[074_photon_engine|Databricks]] 라이선스 주도 (Iceberg로 중립화 가능) |
| **학습 곡선** | [[025_dba_database_administrator|DBA]]→[[001_dikw_pyramid|데이터]] 엔지니어 전환 시 [[542_cow_file_system|CoW]]/MoR, Z-Ordering 개념 학습 필요 |

📢 **섹션 요약 비유**: 오픈 테이블 포맷은 스마트폰 OS와 같다. 하드웨어(S3 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]])는 그대로지만, OS(Delta/Iceberg/Hudi)가 있으면 앱(BI·ML·SQL)이 안정적으로 동작한다. OS 선택(포맷 선택)은 나중에 바꾸기 어려우니 신중하게 결정해야 한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] | 오픈 테이블 포맷이 구현하는 상위 아키텍처 |
| Apache [[178_parquet_rle_encoding_columnar_compression|Parquet]] | 오픈 테이블 포맷의 기반 [[501_file_definition_logical_record|파일]] 포맷 |
| ACID [[191_transaction_concept_states|트랜잭션]] | 오픈 테이블 포맷의 핵심 부가 기능 |
| [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | Hudi의 주요 적용 패턴 |
| [[074_photon_engine|Databricks]] | Delta Lake의 상용 플랫폼 |
| [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | 모든 오픈 테이블 포맷의 주요 컴퓨팅 엔진 |
| 타임트래블 | [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 이력 관리의 핵심 기능 |

### 👶 어린이를 위한 3줄 비유 설명
1. 오픈 테이블 포맷은 그림 [[501_file_definition_logical_record|파일]]([[001_dikw_pyramid|데이터]])에 저장 기록([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]])을 붙여서, 언제 어떤 그림을 그렸는지 추적하고 이전 [[288_version_ihl_tos_total_length|버전]]으로 되돌릴 수 있게 해준다.

### 📈 관련 키워드 및 발전 흐름도

```text
Parquet/ORC 파일 (메타데이터 부재)
    │
    ▼
오픈 테이블 포맷: 메타데이터 레이어 추가
    ├─► Delta Lake: Databricks 주도 · Unity Catalog
    ├─► Apache Iceberg: Netflix 주도 · 벤더 중립
    └─► Apache Hudi: Uber 주도 · CDC 최적화
```
2. Delta Lake는 다이어리(일기장), Iceberg는 여러 도서관에서 읽을 수 있는 표준 교과서, Hudi는 실시간으로 내용이 바뀌는 뉴스 게시판과 같다.
3. ACID는 은행 통장 잔액처럼 믿을 수 있어야 하는 규칙이다. 내가 1만원을 출금할 때 다른 사람도 동시에 1만원을 출금해서 잔액이 마이너스가 되는 일이 없도록 보호한다.
