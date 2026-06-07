---
title: "073. Delta Lake On Spark"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 73
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Delta Lake는 [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 기반 저장소 위에 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(`_delta_log`)를 추가하여 ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 강제([Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Enforcement), 타임 트래블(Time Travel), MERGE/UPDATE/DELETE 연산을 Spark에서 사용할 수 있게 하는 오픈 소스 스토리지 레이어다.
- **가치**: 기존 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 "쓰고 잊어버리는(Write-once)" 구조라 잘못 쓴 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수정하거나 두 스트림이 동시에 같은 테이블에 쓸 때 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장할 수 없었는데, Delta Lake는 이 문제를 [Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/) 수준의 ACID 보장으로 해결한다.
- **판단 포인트**: Delta Lake의 타임 트래블([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)별 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/))은 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)), 재처리(Reprocessing), 실수 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)에 매우 유용하지만, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 다중 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 축적되어 스토리지를 소모하므로 주기적 `VACUUM` 명령으로 오래된 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 정리해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 전통적 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 한계

```
문제 1: 데이터 수정 어려움
  Parquet 파일은 불변(Immutable) -> UPDATE/DELETE가 사실상 불가
  -> 파티션 전체를 재작성하는 우회 방법만 존재

문제 2: 동시성 문제
  두 Spark 잡이 같은 테이블에 동시 쓰기 -> 데이터 부분 손상 가능
  -> 중복 데이터 또는 누락 데이터 발생

문제 3: 스키마 불일치
  스트림이 새 컬럼을 추가하거나 타입이 바뀌면 하위 쿼리가 이상 동작

문제 4: 읽기/쓰기 일관성 없음
  쓰기 도중 읽기가 이루어지면 "반쯤 쓰여진" 상태 읽기 가능
```

### 2. Delta Lake의 해결책

이 모든 문제는 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(`_delta_log/`) 하나로 해결된다. 모든 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업이 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 기록되고, 원자적으로 커밋되므로 ACID 보장이 가능해진다.

**📢 섹션 요약 비유**
> 기존 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 "책상 위 메모지 [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/)"다 — 누가 언제 추가했는지 기억이 없다. Delta Lake는 "공증 사무실의 거래 장부" — 모든 변경이 날짜·서명과 함께 순서대로 기록된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 디렉토리 구조

```
/delta/table/
+-- _delta_log/
|   +-- 00000000000000000000.json   <- 초기 커밋 (테이블 스키마)
|   +-- 00000000000000000001.json   <- 첫 번째 쓰기 트랜잭션
|   +-- 00000000000000000002.json   <- UPDATE/DELETE 트랜잭션
|   +-- 00000000000000000010.checkpoint.parquet  <- 로그 체크포인트
|   +-- _last_checkpoint
+-- part-00000-xxx.parquet          <- 실제 데이터 파일 (활성)
+-- part-00001-xxx.parquet          <- (이전 버전 파일, VACUUM 전)
+-- part-00002-xxx.parquet
```

### 2. Delta Lake의 4가지 핵심 기능

| 기능 | 설명 | Spark [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
|:---|:---|:---|
| ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | 원자적 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [동시 쓰기](/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/) 충돌 방지 | `df.write.format("delta")` |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 강제 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 불일치 시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 실패 (실수 방지) | 기본 활성화 |
| 타임 트래블 | 과거 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조회 및 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | `VERSION AS OF N`, `TIMESTAMP AS OF` |
| MERGE INTO | Upsert(Insert+Update+Delete) 단일 연산 | `DeltaTable.merge()` |

### 3. 타임 트래블 활용

```python
# Python API
from delta.tables import DeltaTable

# 버전 N으로 조회
df_v1 = spark.read.format("delta") \
    .option("versionAsOf", 1) \
    .load("/delta/orders")

# 특정 타임스탬프로 조회
df_yesterday = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-01") \
    .load("/delta/orders")

# SQL 방식
spark.sql("SELECT * FROM orders VERSION AS OF 3")
spark.sql("SELECT * FROM orders TIMESTAMP AS OF '2024-01-01'")

# 롤백
spark.sql("RESTORE TABLE orders TO VERSION AS OF 2")
```

### 4. MERGE INTO (Upsert)

```sql
-- CDC(Change Data Capture) 패턴: 변경분 적용
MERGE INTO target_orders t
USING source_updates s
ON t.order_id = s.order_id
WHEN MATCHED AND s.status = 'DELETED' THEN DELETE
WHEN MATCHED THEN UPDATE SET t.status = s.status, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT *;
```

**📢 섹션 요약 비유**
> Delta Lake의 MERGE INTO는 "엑셀 시트 vs [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)"의 차이다. 엑셀(기존 레이크)은 복사·붙여넣기로 수정하지만, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)([Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/))는 UPDATE/INSERT/DELETE를 원자적으로 처리한다.

---

## Ⅲ. 비교 및 연결

### 1. [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) vs [Apache Iceberg](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) vs [Apache Hudi](/studynote/16_bigdata/07_data_lake/149_apache_hudi/)

| 비교 항목 | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | [Apache Iceberg](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) | [Apache Hudi](/studynote/16_bigdata/07_data_lake/149_apache_hudi/) |
|:---|:---|:---|:---|
| 개발사 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) ([오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)) | Netflix/Apple | Uber |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | ACID | ACID | ACID |
| 타임 트래블 | ✅ ([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)/타임스탬프) | ✅ ([스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)) | ✅ (커밋 시간) |
| [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 진화 | ✅ | ✅ (히든 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)) | ✅ |
| Spark 통합 | 최고 | 우수 | 우수 |
| 스트리밍 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) | ✅ | ✅ | ✅ (DeltaStreamer) |
| 커뮤니티 생태계 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 중심 | 멀티 엔진 강점 | [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/)/Flink 강점 |

**📢 섹션 요약 비유**
> [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/), Iceberg, Hudi는 "같은 문제를 푸는 다른 브랜드의 [볼트](/studynote/15_devops_sre/05_devsecops/236_vault_dynamic_secrets_ttl/)-너트 조합"이다. 기능은 비슷하지만 생태계([Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) vs 멀티 엔진)와 성숙도가 다르다. 환경에 맞는 선택이 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 운영 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)

```sql
-- 테이블 히스토리 조회
DESCRIBE HISTORY orders;

-- 오래된 버전 파일 정리 (VACUUM)
VACUUM orders RETAIN 168 HOURS;  -- 7일 이전 파일 삭제

-- 테이블 통계 및 최적화
OPTIMIZE orders ZORDER BY (user_id, order_date);  -- 데이터 레이아웃 최적화

-- 스키마 조회
DESCRIBE TABLE EXTENDED orders;
```

### 2. 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] Spark에 [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 추가 (`delta-core`)
- [ ] 기존 [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 테이블을 Delta로 변환: `CONVERT TO DELTA parquet.'/path'`
- [ ] VACUUM 주기 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (7일 이상 유지 권장 — [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능 기간)
- [ ] [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 (`mergeSchema` 옵션 사용 여부)
- [ ] MERGE INTO [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝: OPTIMIZE + Z-[Ordering](/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/) 적용

**📢 섹션 요약 비유**
> VACUUM 없이 Delta Lake를 운영하는 것은 "폐기 서류를 절대 버리지 않는 사무실"과 같다. 모든 과거 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 쌓이면 스토리지 비용이 폭발한다. 정기 VACUUM은 필수 정리 루틴이다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상 | ACID로 중복·손상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 방지 |
| 개발 생산성 | MERGE/UPDATE/DELETE로 복잡한 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 단순화 |
| 운영 안전성 | 타임 트래블로 실수 즉시 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |
| [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) ([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)) | 테이블 히스토리로 누가 무엇을 언제 변경했는지 추적 |

### 2. 결론

Delta Lake는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 유연성과 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 안정성을 결합한 <strong><a href="/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a> 아키텍처의 핵심 스토리지 레이어</strong>다. [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 환경에서는 기본이며, [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 Spark 클러스터에도 적용 가능하다. 기술사 답안에서는 기존 레이크의 한계 -> Delta Lake의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 해결책 -> ACID + 타임 트래블의 가치를 순서대로 서술하는 것이 핵심이다.

**📢 섹션 요약 비유**
> Delta Lake는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에 "법적 효력을 가진 계약 시스템"을 도입한 것이다. 어떤 변경도 장부에 기록되고, 잘못된 거래는 취소([롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/))할 수 있으며, 언제나 특정 시점의 장부(타임 트래블)를 열람할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Apache Iceberg](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) | 경쟁 기술 | 멀티 엔진 지원이 강한 유사 [오픈 테이블 포맷](/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) |
| [Apache Hudi](/studynote/16_bigdata/07_data_lake/149_apache_hudi/) | 경쟁 기술 | [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 처리에 강한 유사 [오픈 테이블 포맷](/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) |
| [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) | 실행 엔진 | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 연산의 실행 환경 |
| [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) ([Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/)) | 상위 아키텍처 | Delta Lake가 구현하는 아키텍처 패턴 |
| VACUUM | 운영 도구 | 오래된 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 정리 |
| Z-[Ordering](/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/) | 최적화 기술 | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 자주 쓰는 컬럼 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클러스터링 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Data Lake — 스키마 없는 원시 파일 저장]
    |
    v
[Delta Log (트랜잭션 로그) — 모든 변경 이력 기록]
    |
    v
[ACID 보장 (원자성·일관성·격리·지속성) — 동시성 제어]
    |
    v
[타임 트래블 (Time Travel) — 특정 시점 버전 조회]
    |
    v
[Lakehouse 아키텍처 — DW 신뢰성 + Data Lake 유연성 통합]
```
단순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장소인 [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lake에 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 더해 ACID 정합성과 타임 트래블을 제공하는 Delta Lake가 [Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처의 표준으로 자리잡는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 물건을 그냥 던져 넣는 창고인데, Delta Lake는 물건을 넣을 때마다 "언제, 무엇을, 왜 넣었는지" 일지에 적는 창고예요. 나중에 실수로 물건을 망가뜨려도 일지(타임 트래블)를 보고 예전 상태로 되돌릴 수 있고, 두 사람이 동시에 물건을 정리해도 서로 충돌(ACID)하지 않아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 262

<- **이전**: [21. Spark History Server — 완료 작업 이력 조회](/studynote/16_bigdata/03_spark/072_spark_history_server/)
**다음**: [23. Photon 엔진 (Databricks) — 네이티브 벡터화 실행 엔진](/studynote/16_bigdata/03_spark/074_photon_engine/) ->

---
