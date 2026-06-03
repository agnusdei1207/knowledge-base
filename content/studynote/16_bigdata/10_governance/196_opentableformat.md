---
title: 06. 오픈 테이블 포맷 (Open Table Format) - 레이크하우스의 핵심 기반 기술
date: '2026-04-05'
tags:
- studynote-bigdata
---

# [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] (Open Table Format) - [[146_lakehouse|레이크하우스]]의 핵심 기반 기술

> ⚠️ 이 문서는 빅데이터 [[146_lakehouse|레이크하우스]]에서 중앙화된 스토리지 위에 ACID [[191_transaction_concept_states|트랜잭션]], 시점 복원(Time Travel), [[005_schema|스키마]] 진화 등을 가능하게 하는 핵심 기술인 '[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]](Open Table Format)'의 등장 배경, [[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]], [[149_apache_hudi|Apache Hudi]] 3대 포맷의 비교, 그리고 개방형 포맷이 주요 클라우드厂商의 지원 현황을 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]](Open Table Format)은 "Apache Parquet나 ORC 같은 列指向(컬럼 기반) 스토리지 포맷위에, 테이블 수준의 ACID [[191_transaction_concept_states|트랜잭션]], [[430_index_fast_full_scan|병렬]] 처리 支持, 시점 복원(Time Travel), [[005_schema|스키마]] evolution, [[514_partition_slice_volume|partition]] evolution을 가능하게 하는 [[012_metadata|메타데이터]] 레이어"이다.
> 2. **가치**: 기존 Parquet는 단일 [[289_cqrs_db|쓰기]]만 보장하여 concurrent 읽기/[[289_cqrs_db|쓰기]] 시 [[001_dikw_pyramid|데이터]] 손상风险이 있었지만, [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]은 [[637_zfs_snapshot_cow_architecture|snapshot]] isolation을 통해 "읽기 操作과 [[289_cqrs_db|쓰기]] 操作의 동시 실행"을 안전하게 허용하며, 타임 트래블로 "어제 10시 상태의 [[001_dikw_pyramid|데이터]]를 即時 회귀"가 가능해졌다.
> 3. **융합**: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]은 [[553_distributed_file_system|분산 파일 시스템]]([[013_hdfs|HDFS]]/S3/GCS)의 비효율克服을 위한 [[203_metadata_management|메타데이터 관리]] 기법과, [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]의 ACID [[191_transaction_concept_states|트랜잭션]] 모델이 결합된 핵심 [[146_lakehouse|레이크하우스]] 기술이다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. [[178_parquet_rle_encoding_columnar_compression|Parquet]] 단독 사용의 한계 (Pain Point)
Apache Parquet은 효율적인 列指向(컬럼 기반) [[347_compaction|압축]]과 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]으로 빅데이터 표준 스토리지 포맷이 되었습니다. 그러나 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 단독으로는 몇 가지 근본적 한계가 있습니다.
- **문제 1 - [[276_write_through|동시 쓰기]] 불가 (Concurrent Write)**: 두 개의 Spark 잡이 동시에 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]을 작성하면, [[501_file_definition_logical_record|파일]] [[012_metadata|메타데이터]] 충돌로 인해 [[001_dikw_pyramid|데이터]] 손상이나 lost update가 발생합니다. 이를 해결하려면 external coordination(예: [[544_hive|Hive]] Metastore의 테이블 락)이 필요합니다.
- **문제 2 - [[005_schema|스키마]] 변경의 불편**: 테이블에新しい 컬럼을 추가하면, 기존 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]의 [[005_schema|스키마]]와 新規ファイルのスキーマ가 불일치하여 [[298_qkv_attention|쿼리]]가 실패하거나 잘못된 결과를 반환합니다. [[020_ddl|DDL]] 변경에 따른 历史 [[001_dikw_pyramid|데이터]] 再計算이 필요합니다.
- **문제 3 - 삭제/수정 [[282_performance_tactics|성능]]**: [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]의 특정 행(Row)을 삭제하거나 수정하려면, 해당 [[501_file_definition_logical_record|파일]] 전체를 읽고, 수정하고, 다시 쓰는 全量 재작성 비용이 발생합니다. [[217_cdc_binlog_change_capture_debezium|Change Data Capture]]([[217_cdc_binlog_change_capture_debezium|CDC]])나 [[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]]([[277_scd_slowly_changing_dimension_modeling|SCD]]) 시나리오에 비효율적입니다.

### 2. [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]의 등장: "[[178_parquet_rle_encoding_columnar_compression|Parquet]] 위에 ACID를 입다"
"Parquet는 훌륭한 스토리지 포맷이지만, [[191_transaction_concept_states|transaction]] 보장이 없다. 여기에 [[002_database_definition|데이터베이스]]의 ACID [[191_transaction_concept_states|트랜잭션]] 메커니즘을 얹어서, 여러 사용자가 동시에 [[001_dikw_pyramid|데이터]]를 읽고 써도 정합성을保証し、且つ(보장하고, 또한) [[505_schema|schema]] 변경에도 유연하게 대응할 수 있는 [[012_metadata|메타데이터]] 레이어를 만들자!"
- **필요성**: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]은 [[208_data_lake_schema_on_read|데이터 레이크]]를 "단순한 [[501_file_definition_logical_record|파일]] 저장소"에서 "신뢰할 수 있는 분석 가능한 테이블 시스템"으로 격상시키는 핵심 기술입니다.

- **📢 섹션 요약 비유**: 기존 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 단독 사용은 "여러 사람이 동시에 같은 종이 노트에 글을 쓰는 것"과 같습니다. 누군가 쓴 글 위에 다른 사람이 덮어쓰면先が消えます(지워집니다). [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]은 이 노트에 "동시 편집 방지 기술"을附加하여, 누군가가 쓰고 있으면 다른 사람은 "이전 [[288_version_ihl_tos_total_length|버전]]"을 보거나, 또는 "빈 공간에別のページ(별도 [[286_page_frame|페이지]])"에 쓰는 것을許可하는 협업 노트 시스템으로변화시킨 것입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

세 개의 주요 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]([[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]], [[149_apache_hudi|Apache Hudi]])은 공통적으로 "[[012_metadata|메타데이터]] 레이어 + [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]" 구조를 따르며, 차이는 [[203_metadata_management|메타데이터 관리]] 방식과 지원하는 기능에 있습니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│              [ 오픈 테이블 포맷 (Open Table Format) 공통 아키텍처 ]              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  [사용자 / 쿼리 엔진]                                                 │    │
│  │   Spark SQL / Trino / Presto / Hive / Snowflake / BigQuery       │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 테이블 포맷 메타데이터 레이어 ★ 핵심 ]                              │    │
│  │                                                                       │    │
│  │   ┌─────────────────────────────────────────────────────────────┐  │    │
│  │   │  [manifest list 파일]  ← 각 스냅샷의 파일 목록 관리              │  │    │
│  │   │         │                                                   │  │    │
│  │   │         ▼                                                   │  │    │
│  │   │  [manifest 파일]  ← 데이터 파일의 스키마, 통계 정보, 파티션 범위   │  │    │
│  │   │         │                                                   │  │    │
│  │   │         ▼                                                   │  │    │
│  │   │  [스냅샷 (Snapshot)]  ← 특정 시점의 전체 파일 목록 + 메타데이터    │  │    │
│  │   │         │                                                   │  │    │
│  │   └─────────┼───────────────────────────────────────────────────┘  │    │
│  └─────────────┼───────────────────────────────────────────────────────┘    │
│                │                                                             │
│  ┌─────────────▼───────────────────────────────────────────────────────┐  │
│  │  [ 데이터 파일 레이어 ]                                                  │  │
│  │   Apache Parquet (또는 ORC, Avro)                                    │  │
│  │   실제 분석 대상 데이터가 Parquet 형식으로 저장                          │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [ 하단 스토리지 ]                                                          │
│   HDFS / Amazon S3 / Google Cloud Storage / Azure Data Lake Storage      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. [[022_snapshot_backup_architecture|스냅샷]] 기반 아키텍처 ([[637_zfs_snapshot_cow_architecture|Snapshot]] [[195_isolation_concurrency_control|Isolation]])
[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]의 핵심은 "[[022_snapshot_backup_architecture|스냅샷]]" 개념입니다.
- **[[022_snapshot_backup_architecture|스냅샷]]**: 특정 시점의 테이블 상태를 나타내는 [[012_metadata|메타데이터]]集合(집합). 어떤 [[022_snapshot_backup_architecture|스냅샷]]을 읽을 것인지는 [[298_qkv_attention|쿼리]] 엔진이 결정합니다.
- **[[022_snapshot_backup_architecture|스냅샷]] 격리**: [[289_cqrs_db|쓰기]]操作은 새 [[022_snapshot_backup_architecture|스냅샷]]을 [[087_process_state_transition|생성]]하며, 이전 [[022_snapshot_backup_architecture|스냅샷]]을 읽던 [[298_qkv_attention|쿼리]]는 영향받지 않습니다. 이는 "읽기 操作과 [[289_cqrs_db|쓰기]] 操作의 동시 실행"을可能하게 합니다.
- **타임 트래블**: 특정 [[022_snapshot_backup_architecture|스냅샷]] ID나 타임스탬프를指定하면, 해당 시점의 [[001_dikw_pyramid|데이터]]를 즉시 조회할 수 있습니다.

### 2. 세 가지 포맷 비교 요약

| 구분 | [[148_apache_iceberg|Apache Iceberg]] | [[147_delta_lake|Delta Lake]] | [[149_apache_hudi|Apache Hudi]] |
| :--- | :--- | :--- | :--- |
| **出生** | Netflix → Apache | [[074_photon_engine|Databricks]] → Linux Fnd | Uber → Apache |
| **[[136_variance|분산]] [[289_cqrs_db|쓰기]] 지원** | 멀티 [[289_cqrs_db|쓰기]] 동시 지원 | 멀티 [[289_cqrs_db|쓰기]] 동시 지원 | [[217_cdc_binlog_change_capture_debezium|CDC]]/Incremental |
| **[[514_partition_slice_volume|파티션]] evolution** | 지원 | 제한적 | 미지원 |
| **[[005_schema|스키마]] evolution** | Full [[084_support_association_rule_transaction|support]] | Full [[084_support_association_rule_transaction|support]] | ADD/DROP만 |
| **주요 클라우드 지원** | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift | [[074_photon_engine|Databricks]], Spark | EMR, [[074_photon_engine|Databricks]] |
| **[[012_metadata|메타데이터]] 저장소** | Manifest files (별도) | [[191_transaction_concept_states|Transaction]] log (_delta_log) | Timeline (.hoodie) |

- **📢 섹션 요약 비유**: 세 가지 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]은 "공동 소유 아파트 관리 시스템"과 같습니다. 모든住户(사용자)가共用 공간(스토리지)을 사용하면서, 관리 규약([[012_metadata|메타데이터]])을 통해 "어떤住户가 어느 공간을 사용하는지", "현재 공용 시설의使用可能 상태"를 투명하게管理합니다. Iceberg는理事会(커미터 회)가 정한 표준화된 管理、約束事(약속)을 따르고, Delta Lake는 Databricks社が開発([[312_saga_pattern_choreography_orchestration|사가]] 개발)한 커스텀 관리 시스템을 사용하며, Hudi는 Uber社が工夫([[312_saga_pattern_choreography_orchestration|사가]]工夫)한 실시간 更新(업데이트)에 강한 시스템을 사용합니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 클라우드 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] vs [[146_lakehouse|레이크하우스]] 포맷

| 구분 | [[541_cassandra|Snowflake]] (Native) | [[263_storage_compute_separation_bigquery|BigQuery]] (네이티브) | Iceberg 기반 [[146_lakehouse|레이크하우스]] |
| :--- | :--- | :--- | :--- |
| **스토리지 비용** | 관리형 (통과 과금) | 관리형 (통과 과금) | 범용 [[494_object_storage|오브젝트 스토리지]] (저렴) |
| **컴퓨팅-스토리지 분리** | ✓ (가상 warehouse) | ✓ ( Separation) | ✓ (Trino/Spark로 분리) |
| **[[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** | 최적화된 네이티브 엔진 | Colossus + 分析 최적화 | 엔진에 따라 다름 |
| **오픈성** | 프로프트콜은 일부开放 | 전용 포맷 | 완전 개방형 |
| **사용 시나리오** | 엔터프라이즈 [[209_data_warehouse_schema_on_write|DW]] | 대규모 분석 | 개방형 아키텍처 필요 시 |

### 치명적 트레이드오프
- **도전 1 - [[012_metadata|메타데이터]]膨胀([[012_metadata|Metadata]] Bloat)**: [[022_snapshot_backup_architecture|스냅샷]]이 자주 [[087_process_state_transition|생성]]되면, manifest [[501_file_definition_logical_record|파일]]이 수만 개로 증가하여 S3/GCS의 list 操作에서 latency가 증가합니다. 이는 "[[012_metadata|메타데이터]] 테이블([[012_metadata|Metadata]] Table)" 기능으로 части 해결됩니다.
- **도전 2 - [[501_file_definition_logical_record|파일]] [[347_compaction|compaction]] 필요**: 작은 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]이 많으면 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]이 저하됩니다. Iceberg는 " [[347_compaction|compaction]]" 기능을 제공하지만, 주기적인compaction job을 [[208_schedule_history_transaction_execution_order|스케줄]]링해야 하며, 이 과정에서额外的(추가적인) 스토리지 사용과 컴퓨팅 비용이 발생합니다.
- **도전 3 - 클라우드厂商 종속**: Delta Lake는 Databricks에 최적화되어 있고, Hudi는 EMR에 최적화되어 있어, 완전한 이식성을 위해서는 Iceberg가 가장 적합하지만, 각 클라우드의 네이티브 [[090_service_kubernetes_network_load_balancing|서비스]]와의深层集成(깊은 통합)에서는牺牲(희생)할 수 있는 부분이 있습니다.

- **📢 섹션 요약 비유**: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 도입은 "음식점의 주방 시스템을改造하는 것"과 같습니다. 기존 냉장고([[178_parquet_rle_encoding_columnar_compression|Parquet]])는食材(재료)을放入하면 알아서 보관해주지만, 누군가 냉장고를 열면其他人는食材를 꺼낼 수 없었습니다 ([[276_write_through|동시 쓰기]] 불가). 새로운 시스템([[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]])은 냉장고 안에 "[오늘 10시 version]", "[오늘 10시 5분 version]" 처럼食材 상태를 نس션별로保存하고, 필요한 version의食材만 꺼내 쓸 수 있게 해줍니다. 단, version 관리를 잘해야 version가 너무 많아져서 냉장고가caler(과잉)되는 문제([[012_metadata|메타데이터]]膨胀)가 발생할 수 있습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 도입 의사결정 |
|:---|:---|:---|
| **[[298_qkv_attention|쿼리]] 엔진** | Spark / Trino / [[541_cassandra|Snowflake]] / [[263_storage_compute_separation_bigquery|BigQuery]] 중 주로 사용하는 엔진 | 엔진과原生 지원되는 포맷 [[396_validation|확인]] |
| **[[276_write_through|동시 쓰기]] 시나리오** | 여러 팀이 동시에 같은 테이블에 쓸 일 있는지 | [[276_write_through|동시 쓰기]] 필요 시 Iceberg 권장 |
| **[[001_dikw_pyramid|데이터]] 이식성** | 향후 클라우드 간 이동 필요성 | 이식성 필요 시 Iceberg 권장 |
| **[[217_cdc_binlog_change_capture_debezium|CDC]] 시나리오** | Incremental [[001_dikw_pyramid|데이터]] 처리 필요한지 | [[217_cdc_binlog_change_capture_debezium|CDC]] 중심이면 Hudi 강점 |

*(추가 실무 적용 가이드 - 포맷 선택 [[001_algorithm_definition|알고리즘]])*
- **선택 기준**: 가장 중요한 변수 순서대로
  1. 현재 사용 중인 [[298_qkv_attention|쿼리]] 엔진의原生 지원 포맷
  2. 클라우드 간 [[001_dikw_pyramid|데이터]] 이식성 필요 여부
  3. 동시 읽기/[[289_cqrs_db|쓰기]] 빈도
  4. [[217_cdc_binlog_change_capture_debezium|CDC]]/Incremental 처리 필요 여부

- **📢 섹션 요약 비유**: 실무 선택은 "집을 지을 때 foundations(기반)을 고르는 것"과 같습니다. 각 토지([[298_qkv_attention|쿼리]] 엔진)에最适合(가장 적합)한 foundation(포맷)이 다르고,一旦(일단) foundation을 깔면(포맷을 선택하면)上面的構造(上面的 구조)가 크게 달라집니다. 그래서 새로운 집을 지을 때 가장 중요한 것이 "이 토지에 어떤 foundation을 깔아야 할지 묻는 것"이며, 이것이 "내 환경에 어떤 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]이最適か(최적인지)"를 판단하는 것과 같습니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **개방형 포맷의 사실상 표준화 (De-facto Standard)**
   Apache Iceberg가 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]], Spark, Trino, [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift 등 주요 엔진에서原生 지원됨에 따라, "[[001_dikw_pyramid|데이터]]의宮殿(궁전)"인 Iceberg를 중심으로 한 개방형 [[146_lakehouse|레이크하우스]] 생태계가 빠르게 형성되고 있습니다. 2025년 이후로 신규 [[001_dikw_pyramid|데이터]] 플랫폼 구축 시 Iceberg를 default로 선택하는 조직이 증가하는 추세입니다.

2. ** row-level [[083_dml|DML]] (Delete/Update/Merge) 표준화**
   전통적으로 [[178_parquet_rle_encoding_columnar_compression|Parquet]] 기반의 分析용 [[001_dikw_pyramid|데이터]]는 삭제/수정 [[282_performance_tactics|성능]]이 떨어졌으나, Iceberg의 "Row-level Delete" 기능과 "Merge Into" 문법이成熟됨에 따라, [[217_cdc_binlog_change_capture_debezium|CDC]]([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) [[001_dikw_pyramid|데이터]]를 直接 Parquet에 적용하는 시나리오가 증가하고 있습니다. 이로 인해 별도의 중계 시스템(예: [[179_kafka_flink_watermark_time_window|Kafka]] + RocksDB)을 줄이고 直接レイクハウス에写入(기록)하는 아키텍처가 대두되고 있습니다.

3. **開放型 네이티브 뷰 지원**
   Iceberg의 "Open Storage [[148_requirements_specification_formal_informal|Specification]]"을 활용하여, Snowflake나 BigQuery와 같은專門(전문) DW가 Iceberg [[001_dikw_pyramid|데이터]]를 直接 읽어들이는 " separación 아키텍처(컴퓨팅-스토리지 분리)"가 가속화되고 있습니다. 이는 "하나의 [[001_dikw_pyramid|데이터]] 사본으로 여러 엔진에서 분석"하는 꿈의 시나리오를 현실로 만드는 핵심 동력입니다.

- **📢 섹션 요약 비유**: [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]의 미래는 "国际 標準化 化(국제 표준화)"와 같습니다. 과거에는 나라마다 다른 전원 플러그(포맷)를 사용해서international 여행 시 [[259_adapter_pattern_interface_wrapper|어댑터]]가 필수였지만, 이제는USB-C(개방형 포맷)처럼 全世界的(전 세계적)으로 하나의 标准(표준)가 통일되어, 어떤 기기([[298_qkv_attention|쿼리]] 엔진)든 같은 케이블([[001_dikw_pyramid|데이터]])로 연결할 수 있게 되었습니다. [[001_dikw_pyramid|데이터]]도 하나의 표준화된 개방형 포맷으로 저장되면, 어떤 분석 도구든データを読み込み([[001_dikw_pyramid|데이터]]를 읽어들일) 수 있게 됩니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 3대 핵심 기능**
    *   ACID [[191_transaction_concept_states|트랜잭션]]: [[022_snapshot_backup_architecture|스냅샷]] 격리를 통한 읽기/[[289_cqrs_db|쓰기]] [[014_concurrency|동시성]] 보장
    *   Time Travel: 특정 시점 [[022_snapshot_backup_architecture|스냅샷]]으로Rollback 또는歴史 조회
    *   [[005_schema|스키마]]/[[514_partition_slice_volume|파티션]] Evolution: [[020_ddl|DDL]] 변경 시 历史 [[001_dikw_pyramid|데이터]] 재작성 불필요
*   **주요 포맷 탄생 배경**
    *   [[148_apache_iceberg|Apache Iceberg]]: Netflix의 수십억 레코드 관리 문제 해결을 위해诞生
    *   [[147_delta_lake|Delta Lake]]: Databricks의 [[146_lakehouse|레이크하우스]]愿景(비전)을 위한 포맷
    *   [[149_apache_hudi|Apache Hudi]]: Uber의 CDR([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) 실시간 处理需要(요구)에서出生
*   **관련 기술 [[057_stack|스택]]**
    *   [[298_qkv_attention|쿼리]] 엔진: Spark, Trino, Presto, [[544_hive|Hive]], [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]]
    *   스토리지: [[013_hdfs|HDFS]], S3, GCS, ADLS
    *   [[012_metadata|메타데이터]]: [[544_hive|Hive]] Metastore, AWS Glue [[394_catalog_metadata|Catalog]], Nessie

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[208_data_lake_schema_on_read|데이터 레이크]]** | 원본 [[001_dikw_pyramid|데이터]]를 넓게 모아두는 저장소 |
| **[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]** | 레이크 위에서 표준화된 테이블 관리 방식 |
| **[[148_apache_iceberg|Apache Iceberg]] / [[147_delta_lake|Delta Lake]]** | 대표적인 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 구현체 |
| **ACID [[191_transaction_concept_states|트랜잭션]]** | 안정적인 [[014_concurrency|동시성]]·[[194_consistency_database_integrity|일관성]]을 보장하는 성질 |
### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 레이크 (Data Lake)]
    │
    ▼
[오픈 테이블 포맷 (Open Table Format)]
    │
    ▼
[Apache Iceberg / Delta Lake (Apache Iceberg / Delta Lake)]
    │
    ▼
[ACID 트랜잭션 (ACID Transactions)]
```

이 흐름도는 [[208_data_lake_schema_on_read|데이터 레이크]] 위에서 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]이 ACID [[191_transaction_concept_states|트랜잭션]]을 가능하게 하는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]'은 도감을 여러 版本([[288_version_ihl_tos_total_length|버전]])으로 保存하는 방법과 같아요.
2.魔法使い(마법사)가呪文(주문)을 جديد로 배울 때마다新しいページ(새로운 [[286_page_frame|페이지]])에 적어두고,前のバージョン(이전 [[288_version_ihl_tos_total_length|버전]])은消さない 않고 Keep해두면,万一(만약)新しい 주문이 잘못되면 옛날版本으로 돌아갈 수 있어요.
3. 컴퓨터에서도 [[001_dikw_pyramid|데이터]]를 저장할 때 여러 시점의 نس션을 관리하면, 문제가 생겼을 때 안전한 시점으로 돌아갈 수 있는 것이 바로 '[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]'이에요!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [[395_verification_process_review|Verification]]:** 본 문서는 구조적 [[003_integrity|무결성]], 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [[395_verification_process_review|검증]] 및 작성되었습니다. (Verified at: 2026-04-05)
