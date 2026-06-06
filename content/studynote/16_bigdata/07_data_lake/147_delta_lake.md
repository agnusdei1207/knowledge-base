---
title: "147. Delta Lake"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)
1. Delta Lake는 [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위에 <strong><code>_delta_log</code> <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong>를 추가하여 객체 스토리지에서 ACID ([Atomicity](/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 실현한 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 스토리지 레이어다.
2. `MERGE INTO`, `UPDATE`, `DELETE`, 타임 트래블(Time Travel), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화([Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution)를 지원하여 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/)의 핵심 구현 기술로 자리 잡았다.
3. Spark 네이티브로 설계되었고 현재는 Linux Foundation에 기증되어 Spark·Flink·Trino 등 멀티엔진으로 확산되고 있다.

---

## Ⅰ. 개요 및 필요성

객체 스토리지(S3, ADLS, GCS)는 저렴하고 확장성이 뛰어나지만, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기반이라 부분 수정이 불가능하고 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어가 없다. 결과적으로 기존 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에서는 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 충돌, 중간 실패 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상, 이력 추적 불가 등의 문제가 발생했다.

Databricks는 2019년 Delta Lake를 공개하여 이 문제를 해결했다. [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 형식의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 `_delta_log/` [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 순차적으로 기록함으로써, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 없이도 원자적 연산과 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 격리를 달성한다.

| 문제 (기존 레이크) | Delta Lake 해결책 |
|:---|:---|
| 부분 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 실패 시 오염 | 원자적 커밋 ([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) |
| 동시 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 충돌 | [낙관적 동시성 제어](/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/) (OCC) |
| 이전 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 불가 | 타임 트래블 (VERSION [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) OF) |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 불일치 오류 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 적용/진화 자동 관리 |

> 📢 **섹션 요약 비유**: 공유 메모장에 여러 사람이 동시에 글을 쓰면 엉망이 되는 문제를, Delta Lake는 각자 초안을 작성하고 순번 도장을 찍어 순서대로 반영하는 방식으로 해결한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+--------------------------------------------------------------+
|               Delta Lake 내부 구조                            |
+--------------------------------------------------------------+
|  객체 스토리지 버킷 (S3 / ADLS / GCS)                         |
|                                                              |
|  +-----------------------------+  +----------------------+  |
|  |  _delta_log/                |  |  데이터 파일 (Parquet) |  |
|  |  +-- 00000.json  (커밋 0)   |  |  +-- part-0001.parquet|  |
|  |  +-- 00001.json  (커밋 1)   |  |  +-- part-0002.parquet|  |
|  |  +-- 00002.json  (커밋 2)   |  |  +-- ...             |  |
|  |  +-- 00010.checkpoint.parquet|  +----------------------+  |
|  +-----------------------------+                            |
|                                                              |
|  커밋 로그 내용: {add/remove 파일 목록, 스키마, 통계, 타임스탬프} |
+--------------------------------------------------------------+
```

**주요 기능 상세**

| 기능 | SQL 문법 | 설명 |
|:---|:---|:---|
| Upsert | `MERGE INTO target USING source` | INSERT + UPDATE 원자적 처리 |
| 타임 트래블 | `SELECT * FROM t VERSION AS OF 5` | 과거 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 조회 |
| 타임 트래블 (시간) | `SELECT * FROM t TIMESTAMP AS OF '2026-01-01'` | 날짜 기준 과거 조회 |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 | `ALTER TABLE ... ADD COLUMN` | 기존 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 재작성 없이 컬럼 추가 |
| Z-오더링 | `OPTIMIZE table ZORDER BY (col)` | 연관 컬럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) co-locating |
| 히스토리 조회 | `DESCRIBE HISTORY table` | 커밋 이력 전체 출력 |
| 진공 청소 | `VACUUM table RETAIN 168 HOURS` | 오래된 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 물리적 삭제 |

> 📢 **섹션 요약 비유**: Delta Lake는 공증 사무소와 같다. 모든 변경 사항을 번호 순서로 공증 도장을 찍어 기록하므로, 언제든 과거의 특정 순간으로 돌아가거나 여러 명이 동시에 작업해도 기록이 꼬이지 않는다.

---

## Ⅲ. 비교 및 연결

<strong>Delta Lake vs <a href="/studynote/16_bigdata/07_data_lake/148_apache_iceberg/">Apache Iceberg</a> vs <a href="/studynote/16_bigdata/07_data_lake/149_apache_hudi/">Apache Hudi</a></strong>

| 항목 | Delta Lake | [Apache Iceberg](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) | [Apache Hudi](/studynote/16_bigdata/07_data_lake/149_apache_hudi/) |
|:---|:---|:---|:---|
| 탄생 배경 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) (2019) | Netflix (2018) | Uber (2019) |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | `_delta_log` ([JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)) | Manifest + [Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) | Timeline |
| [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 방식 | 명시적 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 히든 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
| 주요 강점 | Spark 생태계 성숙도 | 멀티엔진 표준화 | [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)/upsert 특화 |
| 기본 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) / ORC / Avro | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) / ORC |
| [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 지원 | VACUUM + DELETE | Row-level delete | 레코드 수준 삭제 |

**연관 기술 연결**

- <strong><a href="/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/">Medallion Architecture</a></strong>: Delta Lake의 Bronze/Silver/Gold 계층 구현 기반
- **AutoLoader**: 신규 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 자동 감지하여 Delta 테이블로 적재
- <strong><a href="/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/">DLT</a> (Delta Live Tables)</strong>: 선언적 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 프레임워크
- <strong><a href="/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a></strong>: Delta Lake 테이블의 거버넌스 관리

> 📢 **섹션 요약 비유**: Delta Lake(Spark 전문가), Iceberg(전 회사 어디서나 쓰이는 범용 도구), Hudi([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 특화 전문가)는 같은 문제를 다른 관점에서 해결한다. 선택은 기존 엔진 생태계에 따라 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도입 시나리오**

- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">CDC</a> <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: MySQL/Postgres 변경 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 MERGE INTO로 레이크에 실시간 반영
- <strong><a href="/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a> 준수</strong>: 사용자 삭제 요청을 DELETE로 처리, VACUUM으로 물리 삭제
- **스트리밍 + 배치 통합**: Spark Structured Streaming이 Delta 테이블에 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 배치 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 읽기
- **소급 재처리**: 잘못된 변환 발견 시 VERSION [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) OF로 과거 상태 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 재처리

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Delta Log 동작 원리 | 각 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 기록, 체크포인트(10개마다)로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) |
| [낙관적 동시성 제어](/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/) | 충돌 감지 시 재시도, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 충돌 없으면 원자적 커밋 |
| Small [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제 해결 | `OPTIMIZE` 명령으로 소규모 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 128MB 단위로 병합 |
| 타임 트래블 한계 | VACUUM 실행 시 보존 기간(기본 7일) 이전 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 삭제됨 |

> 📢 **섹션 요약 비유**: Delta Lake 운영은 은행 계좌 관리와 같다. 입출금(변경)마다 명세서([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))를 남기고, 오래된 명세서는 주기적으로 정리(VACUUM)하되, 최신 잔액은 항상 정확하게 유지된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상 | ACID 보장으로 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 실패 시 부분 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오염 방지 |
| 운영 효율화 | MERGE INTO로 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 구현 단순화, OPTIMIZE로 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |
| 규정 준수 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) 대응을 위한 물리적 삭제 경로 확보 |
| 실험 재현성 | 타임 트래블로 ML 모델 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 고정 가능 |

Delta Lake는 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 생태계의 선두 구현체로, [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 플랫폼 밖에서도 [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/), Trino, Flink 등 다양한 엔진에서 사용 가능하다. 기술사 시험에서는 <strong><a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 구조</strong>, **MERGE INTO 동작**, <strong>타임 트래블 메커니즘</strong>이 주요 출제 포인트다.

> 📢 **섹션 요약 비유**: Delta Lake는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에 교통 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등을 설치한 것이다. [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등이 없으면 차들이 충돌하지만, [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))이 있으면 수천 대가 동시에 달려도 질서 있게 통행한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| `_delta_log` | 핵심 구성요소 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) |
| MERGE INTO | [DML](/studynote/12_it_management/02_itsm_itil/867_dml/) 확장 | upsert 원자적 처리 |
| OPTIMIZE + Z-ORDER | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 | 소규모 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 병합 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클러스터링 |
| VACUUM | 유지 관리 | 만료 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 물리 삭제 |
| AutoLoader | 수집 도구 | 신규 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자동 감지·적재 |
| [Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 거버넌스 | 테이블 수준 접근 제어·리니지 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[_delta_log (트랜잭션 로그)]
    |
    v
[MERGE INTO (Upsert)]
    |
    v
[OPTIMIZE + Z-ORDER]
    |
    v
[VACUUM (파일 정리)]
    |
    v
[AutoLoader]
```

이 흐름도는 _delta_log ([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))에서 출발해 AutoLoader까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Delta Lake는 그림 일기장처럼 매일 무슨 일이 있었는지 날짜별로 기록해두는 특별한 저장소예요.
2. 일기를 잘못 쓴 날로 돌아가서 다시 읽을 수 있고, 여러 친구가 동시에 써도 겹치지 않아요.
3. 오래된 일기는 주기적으로 정리(VACUUM)해서 공간이 가득 차지 않게 깔끔히 유지한답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 262

<- **이전**: [146. 레이크하우스 (Lakehouse) — 데이터 레이크 + 웨어하우스 융합](/studynote/16_bigdata/07_data_lake/146_lakehouse/)
**다음**: [148. Apache Iceberg — 오픈 테이블 포맷 히든 파티셔닝](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) ->

---
