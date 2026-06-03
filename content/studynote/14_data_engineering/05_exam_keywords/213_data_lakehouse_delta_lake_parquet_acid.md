+++
title = "213. 데이터 레이크하우스 (Data Lakehouse) Delta Lake 파케이 ACID"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)([Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/))는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))의 저비용·유연성과 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))의 ACID([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)·[Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)·[Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관리를 통합한 차세대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 아키텍처다.
> 2. **가치**: Delta Lake는 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3, ADLS) 위에 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Log)를 추가해 ACID를 보장하고, [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 컬럼 형식의 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 효율과 함께 타임 트래블(Time Travel)로 임의 시점 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원을 가능하게 한다.
> 3. **판단 포인트**: 기존 DW는 관리 비용이 높고 비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리 못하며, 순수 레이크는 ACID가 없어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 낮다 — [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 이 두 단점을 모두 해소하는 아키텍처적 수렴점이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 아키텍처의 진화

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

| 항목 | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
|:---|:---|:---|:---|
| **ACID 지원** | ✅ | ❌ | ✅ |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)** | 엄격([Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) | 유연([Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) | 진화형([Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution) |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형** | 정형 | 정형·반정형·비정형 | 정형·반정형·비정형 |
| **ML 지원** | 제한적 | ✅ | ✅ |
| **비용** | 높음 | 낮음 | 낮음 |
| **대표 기술** | Teradata, Redshift | S3+[Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) | [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/), Iceberg |

📢 **섹션 요약 비유**: [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)는 창고([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))의 꼼꼼함과 광활한 공터(Lake)의 자유로움을 합친 '스마트 창고'다 — 어떤 물건이든 넣을 수 있으면서도 재고가 정확히 관리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) 아키텍처

Delta Lake는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 스토리지 레이어로, [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)([Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) 위에 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(`_delta_log/`)를 추가해 ACID를 구현한다.

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

**[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 동작 원리**:
- 모든 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업(INSERT, UPDATE, DELETE, MERGE)은 먼저 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 기록
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 원자적(Atomic)으로 커밋되어야 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 반영
- 충돌 시 [낙관적 동시성 제어](/knowledge-base/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/)([Optimistic Concurrency Control](/knowledge-base/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/))로 재시도

### 2.2 [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 컬럼 형식 (Apache [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/))

[Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)([파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/))는 Apache에서 개발한 컬럼 지향(Columnar) 바이너리 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형식으로, 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 최적화되어 있다.

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

**[Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 효율**: 동일 타입의 값이 연속 저장되어 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률이 매우 높다.

| 형식 | 평균 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 | 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 |
|:---|:---|:---|
| CSV | [1x](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/584_802_1x_pnac_eap_radius/) | 느림 (전체 파싱 필요) |
| [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) | 1.5~2x | 느림 |
| **[Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)** | **5~10x** | **빠름 (컬럼 프루닝)** |
| ORC | 4~8x | 빠름 |

### 2.3 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) 보장

| [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 전체 명칭 | [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) 구현 방법 |
|:---|:---|:---|
| **A** | [Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) ([원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)) | 모든 변경이 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 원자적 커밋 |
| **C** | [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 검증으로 잘못된 타입 차단 |
| **I** | [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) ([격리성](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)) | [낙관적 동시성 제어](/knowledge-base/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/), [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) |
| **D** | [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) (내구성) | S3/ADLS의 [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 9's 내구성 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) |

### 2.4 타임 트래블 (Time Travel)

Delta Lake의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 이용해 과거 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조회·복원할 수 있다.

```sql
-- 버전 5 시점 데이터 조회
SELECT * FROM delta.`/data/orders` VERSION AS OF 5;

-- 어제 데이터 조회
SELECT * FROM delta.`/data/orders`
TIMESTAMP AS OF '2026-04-20 00:00:00';

-- 실수로 삭제한 데이터 복원
RESTORE TABLE orders TO VERSION AS OF 3;
```

📢 **섹션 요약 비유**: Delta Lake의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 '블랙박스'다 — 비행기가 추락해도 블랙박스로 사고 직전 상태를 복원하듯, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잘못 지워도 과거 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 되돌릴 수 있다.

---

## Ⅲ. 비교 및 연결

### 3.1 [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) 3종 비교

| 항목 | [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) | [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) | [Apache Hudi](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/) |
|:---|:---|:---|:---|
| **주도** | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) | Netflix | Uber |
| **ACID** | ✅ | ✅ | ✅ |
| **타임 트래블** | ✅ | ✅ | ✅ |
| **스트리밍** | ✅ [Spark Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) | 제한적 | ✅ ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)/MOR) |
| **강점** | Spark 통합 | 대규모 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 증분 처리(Upsert) |

### 3.2 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 전체 아키텍처

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

📢 **섹션 요약 비유**: [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 '스마트 물류창고'다 — 물건([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 거대한 야외 창고(S3)에 [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 박스로 쌓이고, [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 모든 입출고 기록을 ACID로 보장하며, ML·BI 팀이 같은 창고를 공유한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) 운영 최적화

```
문제: 소규모 Parquet 파일 다수 생성 → "작은 파일 문제"
해결: OPTIMIZE 명령으로 파일 병합

OPTIMIZE delta.`/data/orders`
ZORDER BY (customer_id, order_date);  -- Z-ORDER 클러스터링

문제: 오래된 버전 데이터가 스토리지 누적
해결: VACUUM으로 오래된 파일 정리

VACUUM delta.`/data/orders` RETAIN 168 HOURS;  -- 7일 이내 보존
```

### 4.2 [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 단계 | [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 항목 |
|:---|:---|
| **레이어 설계** | Bronze([RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) → Silver(정제) → Gold(집계) 3계층 |
| **[파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)** | 날짜·지역 등 자주 필터링하는 컬럼으로 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) |
| **[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 형식** | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) + Snappy [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 기본 적용 |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화** | `mergeSchema=true`로 컬럼 추가 허용 |
| **접근 제어** | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)([Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)) 또는 AWS Lake Formation |

📢 **섹션 요약 비유**: [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 운영은 도서관 관리와 같다 — OPTIMIZE는 흩어진 책을 두꺼운 전집으로 묶기, VACUUM은 낡은 책 폐기, Z-ORDER는 자주 찾는 책을 앞으로 배치하는 것이다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 도입 효과

| 효과 | 내용 |
|:---|:---|
| **비용 절감** | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 대비 스토리지 비용 70~90% 절감 (S3 기반) |
| **ML 통합** | 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 BI와 ML 동시 서빙 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이중 관리 제거 |
| **[신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)** | ACID + 타임 트래블로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 보장 |
| **개방성** | 벤더 락인([Lock-in](/knowledge-base/studynote/12_it_management/05_security_compliance/362_lock_in_portability/)) 없이 표준 포맷([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) 사용 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"Delta Lake가 왜 ACID를 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 구현하는가"**를 [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 불변성(Immutability)과 연결해 논술해야 한다. [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 한번 쓰이면 수정되지 않고 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 생성되며, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 어떤 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 유효한지 관리하는 방식으로 ACID가 달성됨을 설명하면 고득점이다.

📢 **섹션 요약 비유**: Lakehouse는 '모든 것을 담는 현명한 창고'다 — 저렴한 공간(S3), 정확한 재고 관리([Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/)), 어제 상태 복원(타임 트래블), [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 포장([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) — 이 네 가지가 한 지붕 아래 합쳐진 것이다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 구현체 | [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) / Iceberg / Hudi | [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) 3종 |
| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형식 | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) ([파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) | 컬럼 지향 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 바이너리 포맷 |
| [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 보장 | ACID (A·C·I·D) | [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)·[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[격리성](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)·내구성 |
| 이력 관리 | 타임 트래블 (Time Travel) | 과거 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 조회·복원 기능 |
| 레이어 패턴 | Bronze → Silver → Gold | [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층 |
| 기반 스토리지 | S3 / ADLS / GCS | [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) |

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)는 레고 블록 창고야 — 어떤 모양의 블록([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이든 넣을 수 있고, 재고 목록([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))도 정확히 관리되지!

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
2. [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 블록을 종류별로 꽉꽉 눌러서 지퍼백에 담아 놓은 것 — 같은 종류끼리 있으니 공간도 적게 차지하고, 필요한 것만 꺼내기도 쉬워.
3. 타임 트래블은 '되감기 버튼'이야 — 실수로 블록을 버렸어도 어제 창고 상태로 되돌릴 수 있으니 걱정 없어!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 213 / 258

← **이전**: [212. ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/212_etl_elt_cloud_transformation_bottleneck/)
**다음**: [214. 아파치 카프카 (Apache Kafka) Pub-Sub 토픽 파티션 오프셋 브로커](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) →

---
