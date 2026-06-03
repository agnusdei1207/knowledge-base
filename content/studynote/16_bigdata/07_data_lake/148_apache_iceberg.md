---
title: 148. Apache Iceberg — 오픈 테이블 포맷 히든 파티셔닝
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
1. Apache Iceberg는 Netflix가 고안한 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]]으로, **히든 [[179_table_partitioning_concept|파티셔닝]](Hidden [[179_table_partitioning_concept|Partitioning]])**을 통해 [[298_qkv_attention|쿼리]] 작성자가 [[514_partition_slice_volume|파티션]] 컬럼을 알지 못해도 [[184_partition_pruning|파티션 프루닝]]([[184_partition_pruning|Partition Pruning]])이 자동 적용된다.
2. **[[514_partition_slice_volume|파티션]] 진화([[514_partition_slice_volume|Partition]] Evolution)**와 **[[005_schema|스키마]] 진화**, **[[022_snapshot_backup_architecture|스냅샷]] 격리**, **행 수준 삭제(Row-Level Delete)**를 지원하여 멀티 페타바이트 분석 테이블을 안전하게 운영할 수 있다.
3. Spark, Flink, Trino, [[544_hive|Hive]], Dremio 등 다수 엔진이 네이티브 지원하여 [[051_vendor_lock_in_cloud_computing|벤더 종속]] 없는 **멀티엔진 오픈 [[146_lakehouse|레이크하우스]]**의 사실상 표준으로 자리 잡고 있다.

---

## Ⅰ. 개요 및 필요성

[[459_quic_fec_forward_error_correction|초기]] [[544_hive|Hive]] 기반 [[208_data_lake_schema_on_read|데이터 레이크]]는 [[514_partition_slice_volume|파티션]] [[506_directory_structure_symbol_table|디렉터리]] 구조를 그대로 노출했다(`/year=2026/month=04/day=21`). 이 방식은 사용자가 [[298_qkv_attention|쿼리]]에 [[514_partition_slice_volume|파티션]] 조건을 명시해야만 [[184_partition_pruning|파티션 프루닝]]이 작동하여 실수 시 풀 스캔(Full Table Scan)이 발생했다. 또한 [[514_partition_slice_volume|파티션]] [[268_strategy_pattern|전략]] 변경 시 기존 [[001_dikw_pyramid|데이터]]를 전부 재작성해야 하는 운영 부담이 있었다.

Netflix는 수백 PB 규모의 테이블 운영 경험에서 이 한계를 극복하기 위해 Iceberg를 설계했다. Iceberg는 테이블 [[012_metadata|메타데이터]]를 트리 구조([[394_catalog_metadata|Catalog]] → [[637_zfs_snapshot_cow_architecture|Snapshot]] → Manifest List → Manifest [[501_file_definition_logical_record|File]] → [[001_dikw_pyramid|Data]] [[501_file_definition_logical_record|File]])로 관리하여 물리적 [[514_partition_slice_volume|파티션]] 구조를 숨기고, 엔진이 [[012_metadata|메타데이터]]만 읽어 최적 접근 경로를 선택하게 한다.

| 항목 | [[544_hive|Hive]] [[179_table_partitioning_concept|파티셔닝]] | Iceberg 히든 [[179_table_partitioning_concept|파티셔닝]] |
|:---|:---|:---|
| [[514_partition_slice_volume|파티션]] 조건 명시 | [[298_qkv_attention|쿼리]]에 직접 기재 필수 | 엔진이 자동 추론 |
| [[514_partition_slice_volume|파티션]] 변경 | 전체 [[001_dikw_pyramid|데이터]] 재작성 | [[012_metadata|메타데이터]]만 변경 |
| 스캔 최적화 | 컬럼 기반 필터 없음 | Min/Max 기반 [[501_file_definition_logical_record|파일]] 스킵 |
| [[014_concurrency|동시성]] 제어 | 없음 | 낙관적 [[014_concurrency|동시성]] (OCC) |

> 📢 **섹션 요약 비유**: Hive는 서랍마다 이름표를 붙이고 사람이 직접 열어야 하는 서랍장이고, Iceberg는 [[190_ai_llm_requirements_specification|AI]] 비서가 내용물을 다 파악해서 어느 서랍인지 알아서 꺼내주는 스마트 서랍장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│                 Apache Iceberg 메타데이터 트리                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Catalog]  (Hive / REST / AWS Glue / Nessie)                   │
│       │                                                          │
│       └─▶  [Table Metadata]  (metadata.json)                    │
│                  │   스키마 / 파티션 스펙 / 스냅샷 목록          │
│                  │                                               │
│                  └─▶  [Snapshot]  (커밋 시점 스냅샷)             │
│                            │                                     │
│                            └─▶  [Manifest List]  (*.avro)       │
│                                       │  파티션 범위 요약        │
│                                       │                          │
│                            ┌──────────┴──────────┐              │
│                            ▼                     ▼              │
│                    [Manifest File]        [Manifest File]        │
│                    (데이터 파일 목록,      (추가/삭제 델타)        │
│                     컬럼 통계 포함)                              │
│                            │                                     │
│                    ┌───────┴────────┐                            │
│                    ▼               ▼                             │
│              part-001.parquet  part-002.parquet                  │
└──────────────────────────────────────────────────────────────────┘
```

**핵심 기능 요약**

| 기능 | 설명 | 이점 |
|:---|:---|:---|
| 히든 [[179_table_partitioning_concept|파티셔닝]] | [[514_partition_slice_volume|파티션]] 변환 함수(years/months/bucket 등) [[012_metadata|메타데이터]] 저장 | [[298_qkv_attention|쿼리]] 단순화, 실수 방지 |
| [[514_partition_slice_volume|파티션]] 진화 | 기존 [[001_dikw_pyramid|데이터]] 재작성 없이 [[514_partition_slice_volume|파티션]] [[268_strategy_pattern|전략]] 변경 | 운영 유연성 |
| [[022_snapshot_backup_architecture|스냅샷]] 격리 | 각 [[191_transaction_concept_states|트랜잭션]]이 독립적 [[022_snapshot_backup_architecture|스냅샷]] [[087_process_state_transition|생성]] | 타임 트래블 가능 |
| 행 수준 삭제 | Equality Delete / Position Delete [[501_file_definition_logical_record|파일]] | [[791_gdpr_eu|GDPR]] 삭제 지원 |
| 증분 읽기 | `incrementalScan` API로 [[022_snapshot_backup_architecture|스냅샷]] 간 변경분만 읽기 | 스트리밍 처리 효율화 |

> 📢 **섹션 요약 비유**: Iceberg [[012_metadata|메타데이터]] 트리는 도서관 색인 시스템과 같다. 책 제목([[394_catalog_metadata|Catalog]])으로 서가 위치(Manifest)를 찾고, 서가에서 원하는 [[286_page_frame|페이지]]([[001_dikw_pyramid|Data]] [[501_file_definition_logical_record|File]])만 꺼낸다. 모든 색인이 최신으로 유지되어 새 책이 추가돼도 [[154_database_index_b_tree_search_optimization|인덱스]]만 갱신하면 된다.

---

## Ⅲ. 비교 및 연결

**Iceberg vs [[147_delta_lake|Delta Lake]] vs Hudi (세부 비교)**

| 항목 | Iceberg | [[147_delta_lake|Delta Lake]] | Hudi |
|:---|:---|:---|:---|
| [[179_table_partitioning_concept|파티셔닝]] | 히든 (자동 추론) | 명시적 | 명시적 |
| [[514_partition_slice_volume|파티션]] 진화 | [[001_dikw_pyramid|데이터]] 재작성 없음 | [[514_partition_slice_volume|파티션]] 재작성 필요 | 제한적 지원 |
| 엔진 지원 | Spark/Flink/Trino/[[544_hive|Hive]]/Dremio | Spark 중심, Trino 지원 | Spark 중심 |
| 삭제 [[501_file_definition_logical_record|파일]] 방식 | Equality/Position Delete [[501_file_definition_logical_record|파일]] | 새 [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]로 대체 | MOR [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] |
| [[394_catalog_metadata|카탈로그]] 표준 | [[156_rest_representational_state_transfer|REST]] [[394_catalog_metadata|Catalog]] ([[635_ietf_core_working_group_coap|IETF]] 표준화 중) | [[150_unity_catalog|Unity Catalog]] | [[544_hive|Hive]] Metastore |
| 클라우드 채택 | AWS Athena/Glue 기본 지원 | [[074_photon_engine|Databricks]] 기본 | Cloudera 기본 |

**주목할 트렌드**: AWS, Google Cloud, Snowflake가 Iceberg를 기본 테이블 포맷으로 채택하면서 **멀티엔진 오픈 [[146_lakehouse|레이크하우스]]의 사실상 표준**으로 부상하고 있다.

> 📢 **섹션 요약 비유**: Delta Lake가 애플 생태계처럼 Spark에 최적화되어 편하다면, Iceberg는 안드로이드처럼 다양한 기기(엔진)에서 동작하는 개방형 표준이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**주요 활용 시나리오**

- **대규모 히스토리 테이블**: 수십억 행 이벤트 테이블의 날짜별 [[514_partition_slice_volume|파티션]] 자동 프루닝
- **멀티엔진 환경**: Spark로 쓰고 Trino로 [[298_qkv_attention|쿼리]]하는 혼합 환경
- **[[791_gdpr_eu|GDPR]] 삭제**: Equality Delete [[501_file_definition_logical_record|파일]]로 특정 사용자 [[001_dikw_pyramid|데이터]] [[369_logic_bomb|논리]] 삭제 후 [[347_compaction|compaction]]
- **[[217_cdc_binlog_change_capture_debezium|CDC]] [[123_pipe|파이프]]라인**: Flink가 [[179_kafka_flink_watermark_time_window|Kafka]] 변경 [[001_dikw_pyramid|데이터]]를 Iceberg 테이블에 실시간 upsert

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 히든 [[179_table_partitioning_concept|파티셔닝]] 원리 | [[514_partition_slice_volume|파티션]] 변환 함수를 [[012_metadata|메타데이터]]에 저장, 엔진이 [[298_qkv_attention|쿼리]] 필터에서 자동 추론 |
| [[022_snapshot_backup_architecture|스냅샷]] 격리 메커니즘 | 각 커밋이 새 [[022_snapshot_backup_architecture|스냅샷]]을 [[087_process_state_transition|생성]], 구 [[022_snapshot_backup_architecture|스냅샷]]은 expire snapshots로 GC |
| Manifest 역할 | [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]] 목록 + 컬럼별 min/max 통계 → [[501_file_definition_logical_record|파일]] 스킵 최적화 |
| [[514_partition_slice_volume|파티션]] 진화 장점 | ALTER TABLE 후 새 [[501_file_definition_logical_record|파일]]만 새 [[514_partition_slice_volume|파티션]] [[268_strategy_pattern|전략]] 적용, 기존 [[501_file_definition_logical_record|파일]] 불변 |

> 📢 **섹션 요약 비유**: Iceberg 운영은 스마트 빌딩 관리와 같다. 새 층을 추가해도 기존 층 구조를 바꾸지 않고, 모든 층의 현황은 통제 센터([[012_metadata|메타데이터]])에서 실시간으로 파악된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] | Min/Max 통계 기반 [[501_file_definition_logical_record|파일]] 스킵으로 풀 스캔 최소화 |
| 운영 비용 절감 | [[514_partition_slice_volume|파티션]] 변경 시 [[001_dikw_pyramid|데이터]] 재작성 불필요 → 컴퓨팅 비용 절감 |
| 벤더 독립성 | 오픈 포맷으로 클라우드·엔진 변경 자유로움 |
| 규정 준수 | 행 수준 삭제로 [[791_gdpr_eu|GDPR]] 우측 삭제 요건 충족 |

Apache Iceberg는 2024년 이후 AWS Athena, [[541_cassandra|Snowflake]], Spark 3.x, Flink, Trino의 기본 테이블 포맷으로 채택되며 오픈 [[146_lakehouse|레이크하우스]] 생태계의 중심축이 됐다. 기술사 시험에서는 **히든 [[179_table_partitioning_concept|파티셔닝]] 원리**, **[[012_metadata|메타데이터]] 트리 구조(Manifest List → Manifest → [[001_dikw_pyramid|Data]] [[501_file_definition_logical_record|File]])**, **[[514_partition_slice_volume|파티션]] 진화**가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Iceberg는 도시 지도 앱과 같다. 길이 바뀌어도([[514_partition_slice_volume|파티션]] 진화) 앱 지도만 업데이트하면 되고, 어느 네비게이션 앱(엔진)을 써도 같은 지도 [[001_dikw_pyramid|데이터]]를 활용할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Manifest List | 핵심 [[012_metadata|메타데이터]] | [[022_snapshot_backup_architecture|스냅샷]] 내 Manifest [[501_file_definition_logical_record|파일]] 목록 |
| Hidden [[179_table_partitioning_concept|Partitioning]] | 핵심 기능 | [[514_partition_slice_volume|파티션]] 변환 함수 자동 추론 |
| [[637_zfs_snapshot_cow_architecture|Snapshot]] | [[191_transaction_concept_states|트랜잭션]] 단위 | 각 커밋의 테이블 상태 |
| [[156_rest_representational_state_transfer|REST]] [[394_catalog_metadata|Catalog]] | [[394_catalog_metadata|카탈로그]] 표준 | 멀티엔진 테이블 등록·조회 |
| Equality Delete | 행 삭제 방식 | 특정 컬럼 값 기준 [[369_logic_bomb|논리]] 삭제 |
| Apache Nessie | [[288_version_ihl_tos_total_length|버전]] 관리 [[394_catalog_metadata|카탈로그]] | Git과 유사한 브랜치 기반 [[394_catalog_metadata|카탈로그]] |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 레이크 (Data Lake)]
    │
    ▼
[테이블 포맷 (Table Format)]
    │
    ▼
[Apache Iceberg (Apache Iceberg)]
    │
    ▼
[타임 트래블 (Time Travel)]
```

이 흐름도는 [[208_data_lake_schema_on_read|데이터 레이크]]를 테이블 포맷으로 다듬고 Apache Iceberg의 타임 트래블로 확장되는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. Iceberg는 스마트 도서관이에요. 책([[001_dikw_pyramid|데이터]])이 어느 방([[514_partition_slice_volume|파티션]])에 있는지 알아서 찾아줘서 직접 돌아다닐 필요가 없어요.
2. 도서관 구조([[514_partition_slice_volume|파티션]])를 바꿔도 이미 있는 책들을 다시 옮길 필요가 없고, 새 책만 새 구조에 따라 놓으면 돼요.
3. 어떤 도서관 로봇(엔진)을 써도 같은 방식으로 책을 찾을 수 있어서 누구나 편리하게 이용할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 148 / 262

← **이전**: [[147_delta_lake|147. Delta Lake — ACID 트랜잭션 지원 오픈 테이블 포맷]]
**다음**: [[149_apache_hudi|149. Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크]] →

---
