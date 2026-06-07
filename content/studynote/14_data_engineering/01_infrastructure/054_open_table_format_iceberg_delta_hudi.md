---
title: "Open Table Format: Iceberg/Delta/Hudi"
date: "2026-05-01"
tags:
  - "studynote-data-engineering"
weight: 54
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈 테이블 포맷은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크에 ACID ([Atomicity](/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/))와 테이블 관리 기능을 더한 표준 계층이다.
> 2. **가치**: Iceberg, [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/), Hudi는 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, 타임 트래블, 업데이트/삭제를 지원한다.
> 3. **판단 포인트**: 엔진 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 스트리밍/배치, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 규모를 함께 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크는 원시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 싸게 저장할 수 있지만, 테이블처럼 다루기 어렵다. 오픈 테이블 포맷은 그 위에 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)와 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 계층을 얹는다.

이 덕분에 분석, 스트리밍, 배치를 하나의 테이블 관점으로 운영할 수 있다.

- **📢 섹션 요약 비유**: 오픈 테이블 포맷은 큰 창고 안에 서랍장과 목록표를 함께 놓는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이 포맷들은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 분리하고, [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)/커밋 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 일관성을 유지한다. 그래서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위 저장소를 테이블처럼 다룰 수 있다.

```text
Data Files + Metadata Log -> Table Snapshot -> Query Engine
```

| 포맷 | 특징 | 강점 |
| :--- | :--- | :--- |
| Iceberg | 강한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)/[파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 관리 | 대규모 테이블 |
| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | 커밋 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 | 생태계 친화 |
| Hudi | upsert/[CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 강점 | 증분 처리 |

핵심은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 직접 다루지 않고, 테이블 상태와 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)을 기준으로 읽고 쓰는 것이다.

- **📢 섹션 요약 비유**: 오픈 테이블 포맷은 쌓아 둔 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/)에 카탈로그와 버전표를 붙이는 일이다.

---

## Ⅲ. 비교 및 연결

원시 파켓/CSV [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 두면 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화나 삭제가 어렵다. 오픈 테이블 포맷은 이를 해결하지만, 각 포맷의 엔진 지원과 운영 성숙도는 다르다.

| 항목 | Iceberg | Delta | Hudi |
| :--- | :--- | :--- | :--- |
| 강점 | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)/[파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 커밋 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | upsert |
| 활용 | 대형 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) | 분석/스트리밍 | [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)/증분 |

이 포맷들은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 웨어하우스와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크의 경계를 줄이는 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 구조와도 연결된다.

- **📢 섹션 요약 비유**: 원시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 상자 [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/), 오픈 테이블 포맷은 상자에 칸막이와 재고표를 붙인 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 엔진 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)(Spark, Flink, Trino 등), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 설계, [compaction](/studynote/02_operating_system/06_memory_management/347_compaction/), GC, [snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) 관리가 중요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 필요한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진과 호환되는가?
2. [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화와 타임 트래블이 필요한가?
3. upsert/delete 요구가 있는가?
4. [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 규모와 컴팩션을 운영할 수 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장을 테이블처럼 착각하는 경우
- 포맷 기능을 과하게 도입해 운영을 복잡하게 만드는 경우
- 엔진별 지원 차이를 무시하는 경우

기술사 관점에서는 오픈 테이블 포맷이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크를 운영 가능한 테이블로 바꾸는 계층이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 오픈 테이블 포맷은 창고에 붙이는 번호표와 출입기록이다.

---

## Ⅴ. 기대효과 및 결론

오픈 테이블 포맷은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크의 유연성과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 웨어하우스의 관리성을 함께 가져온다. 그래서 현대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼의 핵심 기반이 된다.

정리하면, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장을 테이블 운영으로 바꾸는 것이 핵심이다.

- **📢 섹션 요약 비유**: 오픈 테이블 포맷은 흐트러진 서류를 번호순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)철로 바꾸는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Iceberg | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 중심 |
| Delta | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 |
| Hudi | 증분/업서트 |
| [Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) | 시점 읽기 |
| [Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 정리 |

### 📈 관련 키워드 및 발전 흐름도

```text
파일 기반 레이크
    |
    v
메타데이터/커밋 로그
    |
    v
오픈 테이블 포맷
    |
    v
레이크하우스 / ACID / 타임 트래블
```

이 흐름은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크를 테이블형 운영 체계로 진화시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 오픈 테이블 포맷은 상자 [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/)에 번호표를 붙이는 거예요.
2. 그래서 언제 넣고 뺐는지 알 수 있어요.
3. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 많아도 테이블처럼 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 258

<- **이전**: [53. DataOps CI/CD 데이터 파이프라인 (DataOps CI/CD Data Pipeline)](/studynote/14_data_engineering/01_infrastructure/053_dataops_ci_cd_data_pipeline/)
**다음**: [55. 컴퓨트와 스토리지 분리 (Separation of Compute and Storage / Cloud DW)](/studynote/14_data_engineering/01_infrastructure/055_separation_of_compute_and_storage_cloud_dw/) ->

---
