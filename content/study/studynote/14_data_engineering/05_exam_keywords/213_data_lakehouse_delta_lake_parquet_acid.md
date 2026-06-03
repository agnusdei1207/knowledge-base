+++
weight = 213
title = "213. 데이터 레이크하우스 (Data Lakehouse) Delta Lake 파케이 ACID"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]([[210_data_lakehouse_delta_lake|Data Lakehouse]])는 [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])의 저비용·유연성과 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]])의 ACID([[193_atomicity_all_or_nothing|Atomicity]]·[[194_consistency_database_integrity|Consistency]]·[[195_isolation_concurrency_control|Isolation]]·[[196_durability_permanent_storage|Durability]]) [[191_transaction_concept_states|트랜잭션]]·[[005_schema|스키마]] 관리를 통합한 차세대 [[001_dikw_pyramid|데이터]] 플랫폼 아키텍처다.
> 2. **가치**: Delta Lake는 [[494_object_storage|오브젝트 스토리지]](S3, ADLS) 위에 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[191_transaction_concept_states|Transaction]] Log)를 추가해 ACID를 보장하고, [[178_parquet_rle_encoding_columnar_compression|Parquet]] 컬럼 형식의 [[347_compaction|압축]] 효율과 함께 타임 트래블(Time Travel)로 임의 시점 [[001_dikw_pyramid|데이터]] 복원을 가능하게 한다.
> 3. **판단 포인트**: 기존 DW는 관리 비용이 높고 비정형 [[001_dikw_pyramid|데이터]]를 처리 못하며, 순수 레이크는 ACID가 없어 [[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]이 낮다 — [[146_lakehouse|레이크하우스]]는 이 두 단점을 모두 해소하는 아키텍처적 수렴점이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[001_dikw_pyramid|데이터]] 저장 아키텍처의 진화

```
1세대: 데이터 웨어하우스 (DW)
  장점: ACID, 스키마 관리, BI 연동
  단점: 고비용, 정형 데이터만, 확장성 한계

      ↓ (비정형/반정형 데이터 폭증)

2세대: 데이터 레이크 (Data Lake)
  장점: 저비용(S3), 정형+비정형, 무한 확장
  단점: ACID 없음, 스키마 관리 어려움, 데이터 늪(Data Swamp)

      ↓ (ML 워크로드 + 실시간 분석 요구)

3세대: 데이터 레이크하우스 (Data Lakehouse)
  장점: DW + 레이크 장점 통합
  핵심: Delta Lake / Apache Iceberg / Apache Hudi
```

### 1.2 세 아키텍처 비교

| 항목 | [[209_data_warehouse_schema_on_write|DW]] | [[208_data_lake_schema_on_read|Data Lake]] | [[146_lakehouse|Lakehouse]] |
|:---|:---|:---|:---|
| **ACID 지원** | ✅ | ❌ | ✅ |
| **[[005_schema|스키마]]** | 엄격([[010_schema_on_write|Schema-on-Write]]) | 유연([[009_schema_on_read|Schema-on-Read]]) | 진화형([[505_schema|Schema]] Evolution) |
| **[[001_dikw_pyramid|데이터]] 유형** | 정형 | 정형·반정형·비정형 | 정형·반정형·비정형 |
| **ML 지원** | 제한적 | ✅ | ✅ |
| **비용** | 높음 | 낮음 | 낮음 |
| **대표 기술** | Teradata, Redshift | S3+[[544_hive|Hive]] | [[147_delta_lake|Delta Lake]], Iceberg |

📢 **섹션 요약 비유**: [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 창고([[209_data_warehouse_schema_on_write|DW]])의 꼼꼼함과 광활한 공터(Lake)의 자유로움을 합친 '스마트 창고'다 — 어떤 물건이든 넣을 수 있으면서도 재고가 정확히 관리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[147_delta_lake|Delta Lake]] 아키텍처

Delta Lake는 [[191_oss_license_compliance|오픈소스]] 스토리지 레이어로, [[494_object_storage|오브젝트 스토리지]]([[494_object_storage|Object Storage]]) 위에 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]](`_delta_log/`)를 추가해 ACID를 구현한다.

```
S3 또는 ADLS 버킷
├── _delta_log/                ← 트랜잭션 로그 (JSON 파일들)
│   ├── 00000000000000000000.json   (커밋 0: 초기 생성)
│   ├── 00000000000000000001.json   (커밋 1: 데이터 추가)
│   ├── 00000000000000000002.json   (커밋 2: 업데이트)
│   └── 00000000000000000010.checkpoint.parquet (체크포인트)
├── part-00000-abc.parquet     ← 실제 데이터 파일
├── part-00001-def.parquet
└── part-00002-ghi.parquet
```

**[[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] 동작 원리**:
- 모든 [[289_cqrs_db|쓰기]] 작업(INSERT, UPDATE, DELETE, MERGE)은 먼저 [[568_logs_distributed_logging_elk_fluentd|로그]]에 기록
- [[568_logs_distributed_logging_elk_fluentd|로그]]가 원자적(Atomic)으로 커밋되어야 실제 [[001_dikw_pyramid|데이터]]로 반영
- 충돌 시 [[223_optimistic_concurrency_control_validation|낙관적 동시성 제어]]([[223_optimistic_concurrency_control_validation|Optimistic Concurrency Control]])로 재시도

### 2.2 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 컬럼 형식 (Apache [[178_parquet_rle_encoding_columnar_compression|Parquet]])

[[178_parquet_rle_encoding_columnar_compression|Parquet]]([[178_parquet_rle_encoding_columnar_compression|파케이]])는 Apache에서 개발한 컬럼 지향(Columnar) 바이너리 [[501_file_definition_logical_record|파일]] 형식으로, 분석 [[298_qkv_attention|쿼리]]에 최적화되어 있다.

```
행 지향 저장 (Row-oriented, CSV/JSON):
┌────┬──────────┬────────┬────────┐
│ ID │   이름   │  나이  │  매출  │
├────┼──────────┼────────┼────────┤
│  1 │  홍길동  │   30   │  1000  │
│  2 │  김철수  │   25   │  2000  │
│  3 │  이영희  │   35   │  1500  │
└────┴──────────┴────────┴────────┘
→ "매출 합계"를 구하려면 모든 행을 읽어야 함

컬럼 지향 저장 (Columnar, Parquet):
┌──────────────────────────────────┐
│ 매출 컬럼만 읽기: [1000,2000,1500]│
│ → SUM = 4500  ← 다른 컬럼 스킵  │
└──────────────────────────────────┘
```

**[[178_parquet_rle_encoding_columnar_compression|Parquet]] [[347_compaction|압축]] 효율**: 동일 타입의 값이 연속 저장되어 [[347_compaction|압축]]률이 매우 높다.

| 형식 | 평균 [[347_compaction|압축]]률 | 분석 [[298_qkv_attention|쿼리]] 속도 |
|:---|:---|:---|
| CSV | [[584_802_1x_pnac_eap_radius|1x]] | 느림 (전체 파싱 필요) |
| [[343_json|JSON]] | 1.5~2x | 느림 |
| **[[178_parquet_rle_encoding_columnar_compression|Parquet]]** | **5~10x** | **빠름 (컬럼 프루닝)** |
| ORC | 4~8x | 빠름 |

### 2.3 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) 보장

| [[082_attribute_types_er_model|속성]] | 전체 명칭 | [[147_delta_lake|Delta Lake]] 구현 방법 |
|:---|:---|:---|
| **A** | [[193_atomicity_all_or_nothing|Atomicity]] ([[193_atomicity_all_or_nothing|원자성]]) | 모든 변경이 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]에 원자적 커밋 |
| **C** | [[194_consistency_database_integrity|Consistency]] ([[194_consistency_database_integrity|일관성]]) | [[005_schema|스키마]] 검증으로 잘못된 타입 차단 |
| **I** | [[195_isolation_concurrency_control|Isolation]] ([[195_isolation_concurrency_control|격리성]]) | [[223_optimistic_concurrency_control_validation|낙관적 동시성 제어]], [[637_zfs_snapshot_cow_architecture|Snapshot]] [[195_isolation_concurrency_control|Isolation]] |
| **D** | [[196_durability_permanent_storage|Durability]] (내구성) | S3/ADLS의 [[308_static_dynamic_nat_pat_port_address_translation|11]] 9's 내구성 [[234_uml_class_relationships_generalization_dependency|상속]] |

### 2.4 타임 트래블 (Time Travel)

Delta Lake의 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 이용해 과거 [[288_version_ihl_tos_total_length|버전]]의 [[001_dikw_pyramid|데이터]]를 조회·복원할 수 있다.

```sql
-- 버전 5 시점 데이터 조회
SELECT * FROM delta.`/data/orders` VERSION AS OF 5;

-- 어제 데이터 조회
SELECT * FROM delta.`/data/orders`
TIMESTAMP AS OF '2026-04-20 00:00:00';

-- 실수로 삭제한 데이터 복원
RESTORE TABLE orders TO VERSION AS OF 3;
```

📢 **섹션 요약 비유**: Delta Lake의 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]는 [[001_dikw_pyramid|데이터]]의 '블랙박스'다 — 비행기가 추락해도 블랙박스로 사고 직전 상태를 복원하듯, [[001_dikw_pyramid|데이터]]를 잘못 지워도 과거 [[288_version_ihl_tos_total_length|버전]]으로 되돌릴 수 있다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 3종 비교

| 항목 | [[147_delta_lake|Delta Lake]] | [[148_apache_iceberg|Apache Iceberg]] | [[149_apache_hudi|Apache Hudi]] |
|:---|:---|:---|:---|
| **주도** | [[074_photon_engine|Databricks]] | Netflix | Uber |
| **ACID** | ✅ | ✅ | ✅ |
| **타임 트래블** | ✅ | ✅ | ✅ |
| **스트리밍** | ✅ [[061_structured_streaming|Spark Structured Streaming]] | 제한적 | ✅ ([[542_cow_file_system|COW]]/MOR) |
| **강점** | Spark 통합 | 대규모 [[012_metadata|메타데이터]] | 증분 처리(Upsert) |

### 3.2 [[146_lakehouse|레이크하우스]] 전체 아키텍처

```
┌────────────────────────────────────────────────────────┐
│                   데이터 레이크하우스                    │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ BI 도구  │  │ ML 플랫폼│  │ SQL 엔진 │             │
│  │ Tableau  │  │ MLflow   │  │ Spark SQL│             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       └─────────────┴─────────────┘                   │
│                      │ 통합 쿼리                        │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │         Delta Lake / Iceberg / Hudi               │  │
│  │    (ACID + 스키마 관리 + 타임 트래블)             │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │                                 │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │     오브젝트 스토리지 (S3 / Azure ADLS / GCS)    │  │
│  │     Parquet 파일 + _delta_log/ 트랜잭션 로그     │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [[146_lakehouse|레이크하우스]]는 '스마트 물류창고'다 — 물건([[001_dikw_pyramid|데이터]])은 거대한 야외 창고(S3)에 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 박스로 쌓이고, [[147_delta_lake|Delta Lake]] [[568_logs_distributed_logging_elk_fluentd|로그]]가 모든 입출고 기록을 ACID로 보장하며, ML·BI 팀이 같은 창고를 공유한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[147_delta_lake|Delta Lake]] 운영 최적화

```
문제: 소규모 Parquet 파일 다수 생성 → "작은 파일 문제"
해결: OPTIMIZE 명령으로 파일 병합

OPTIMIZE delta.`/data/orders`
ZORDER BY (customer_id, order_date);  -- Z-ORDER 클러스터링

문제: 오래된 버전 데이터가 스토리지 누적
해결: VACUUM으로 오래된 파일 정리

VACUUM delta.`/data/orders` RETAIN 168 HOURS;  -- 7일 이내 보존
```

### 4.2 [[146_lakehouse|Lakehouse]] 도입 [[435_checklist_based_testing|체크리스트]]

| 단계 | [[396_validation|확인]] 항목 |
|:---|:---|
| **레이어 설계** | Bronze([[225_raw|RAW]]) → Silver(정제) → Gold(집계) 3계층 |
| **[[179_table_partitioning_concept|파티셔닝]]** | 날짜·지역 등 자주 필터링하는 컬럼으로 [[514_partition_slice_volume|파티션]] |
| **[[347_compaction|압축]] 형식** | [[178_parquet_rle_encoding_columnar_compression|Parquet]] + Snappy [[347_compaction|압축]] 기본 적용 |
| **[[005_schema|스키마]] 진화** | `mergeSchema=true`로 컬럼 추가 허용 |
| **접근 제어** | [[150_unity_catalog|Unity Catalog]]([[074_photon_engine|Databricks]]) 또는 AWS Lake Formation |

📢 **섹션 요약 비유**: [[146_lakehouse|Lakehouse]] 운영은 도서관 관리와 같다 — OPTIMIZE는 흩어진 책을 두꺼운 전집으로 묶기, VACUUM은 낡은 책 폐기, Z-ORDER는 자주 찾는 책을 앞으로 배치하는 것이다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[146_lakehouse|Lakehouse]] 도입 효과

| 효과 | 내용 |
|:---|:---|
| **비용 절감** | [[209_data_warehouse_schema_on_write|DW]] 대비 스토리지 비용 70~90% 절감 (S3 기반) |
| **ML 통합** | 동일 [[001_dikw_pyramid|데이터]]로 BI와 ML 동시 서빙 — [[001_dikw_pyramid|데이터]] 이중 관리 제거 |
| **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]** | ACID + 타임 트래블로 [[001_dikw_pyramid|데이터]] 품질·[[658_ir_recovery|복구]] 보장 |
| **개방성** | 벤더 락인([[362_lock_in_portability|Lock-in]]) 없이 표준 포맷([[178_parquet_rle_encoding_columnar_compression|Parquet]]) 사용 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"Delta Lake가 왜 ACID를 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]로 구현하는가"**를 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]의 불변성(Immutability)과 연결해 논술해야 한다. [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]은 한번 쓰이면 수정되지 않고 새 [[288_version_ihl_tos_total_length|버전]] [[501_file_definition_logical_record|파일]]이 생성되며, [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]가 어떤 [[501_file_definition_logical_record|파일]]이 유효한지 관리하는 방식으로 ACID가 달성됨을 설명하면 고득점이다.

📢 **섹션 요약 비유**: Lakehouse는 '모든 것을 담는 현명한 창고'다 — 저렴한 공간(S3), 정확한 재고 관리([[147_delta_lake|Delta Lake]]), 어제 상태 복원(타임 트래블), [[347_compaction|압축]] 포장([[178_parquet_rle_encoding_columnar_compression|Parquet]]) — 이 네 가지가 한 지붕 아래 합쳐진 것이다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| [[146_lakehouse|레이크하우스]] 구현체 | [[147_delta_lake|Delta Lake]] / Iceberg / Hudi | [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 3종 |
| [[501_file_definition_logical_record|파일]] 형식 | [[178_parquet_rle_encoding_columnar_compression|Parquet]] ([[178_parquet_rle_encoding_columnar_compression|파케이]]) | 컬럼 지향 [[347_compaction|압축]] 바이너리 포맷 |
| [[191_transaction_concept_states|트랜잭션]] 보장 | ACID (A·C·I·D) | [[193_atomicity_all_or_nothing|원자성]]·[[194_consistency_database_integrity|일관성]]·[[195_isolation_concurrency_control|격리성]]·내구성 |
| 이력 관리 | 타임 트래블 (Time Travel) | 과거 [[288_version_ihl_tos_total_length|버전]] 조회·복원 기능 |
| 레이어 패턴 | Bronze → Silver → Gold | [[146_lakehouse|레이크하우스]] [[001_dikw_pyramid|데이터]] 계층 |
| 기반 스토리지 | S3 / ADLS / GCS | [[494_object_storage|오브젝트 스토리지]] |

### 👶 어린이를 위한 3줄 비유 설명

1. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]는 레고 블록 창고야 — 어떤 모양의 블록([[001_dikw_pyramid|데이터]])이든 넣을 수 있고, 재고 목록([[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]])도 정확히 관리되지!

### 📈 관련 키워드 및 발전 흐름도

```text
Data Lake (유연 · 거버넌스 부족)
    │         ╳
    ▼     Data Warehouse (정확 · 유연성 부족)
Lakehouse 통합
    ├─► Delta Lake: ACID + Time Travel + Parquet
    ├─► Apache Iceberg: Hidden Partitioning
    └─► Apache Hudi: Upsert + CDC 특화
    │
    ▼
Unity Catalog · Open Table Format 표준화
```
2. [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]은 블록을 종류별로 꽉꽉 눌러서 지퍼백에 담아 놓은 것 — 같은 종류끼리 있으니 공간도 적게 차지하고, 필요한 것만 꺼내기도 쉬워.
3. 타임 트래블은 '되감기 버튼'이야 — 실수로 블록을 버렸어도 어제 창고 상태로 되돌릴 수 있으니 걱정 없어!
