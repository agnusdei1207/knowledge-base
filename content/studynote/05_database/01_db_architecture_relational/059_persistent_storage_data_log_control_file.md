+++
title = "59. 영구 저장소 (Persistent Storage) - 데이터 파일, 로그 파일, 제어 파일"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 영구 저장소는 DB 인스턴스가 메모리 밖에 남기는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 집합이다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 변경 이력을, 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 구조와 위치 정보를 보존한다.
> 3. **판단 포인트**: [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 있어야 시작되므로, 세 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 역할과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 분리해서 봐야 한다.

---

## Ⅰ. 개요 및 필요성

메모리의 인스턴스는 전원이 꺼지면 사라진다. 그래서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 디스크에 자신의 상태를 기록할 영구 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 필요하다.

이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들은 단순 저장소가 아니라 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치다. 장애 후 재기동할 때 무엇이 있었고, 무엇이 바뀌었고, 어디에 저장됐는지를 알려 주기 때문이다.

- **📢 섹션 요약 비유**: 교실 칠판, 출석부, 교실 배치도처럼 각각 기록하는 내용이 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

영구 저장소는 보통 세 축으로 본다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 변경 이력, 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 전체 구조의 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 담는다.

```text
Nomount
   ↓
제어 파일(Control File) 읽기
   ↓
Mount
   ↓
데이터 파일(Data File) + 로그 파일(Redo Log) 확인
   ↓
Open
```

| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 역할 | 장애 시 의미 |
| :-- | :-- | :-- |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 테이블, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 가장 큰 본체 |
| [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) Log, Write-Ahead Log) | 변경 순서와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 흔적 저장 | 되돌리기/재생의 근거 |
| 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(Control [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치, DB 이름, 상태 기록 | DB가 어디를 열지 알려 주는 지도 |

DBWR([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) Writer)는 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 쓰고, LGWR(Log Writer)는 변경 기록을 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 남긴다. 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 부팅 시 가장 먼저 읽혀 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 위치를 찾아 준다.

- **📢 섹션 요약 비유**: 창고에 물건을 넣는 장부, 출입 기록, 창고 위치도가 각각 따로 있는 구조다.

---

## Ⅲ. 비교 및 연결

세 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 모두 중요하지만 중요성이 다르다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 본체라면, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)의 시간축이고, 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 시작 주소다.

| 항목 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| :-- | :-- | :-- | :-- |
| 담는 것 | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 변경 이력 | 메타정보 |
| 용도 | 조회/저장 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)/재생 | 기동/관리 |
| 손상 영향 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 | 최근 변경 손실 | DB 기동 실패 가능 |
| [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 순환/[미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) | [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) |

제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 없으면 DB는 어디에 무엇이 있는지 몰라 열린다 해도 운영할 수 없다. 반대로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 있어도 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 없으면 장애 후 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)이 어렵다.

- **📢 섹션 요약 비유**: 본체, 블랙박스, 네비게이션이 각각 다른 역할을 맡는 자동차와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 세 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기준으로 나눠야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 아카이빙과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시점, 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 다중 보관이 핵심이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 2개 이상 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)했는가?
2. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 아카이브와 순환 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 갖추는가?
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보관 주기가 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표([RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)/[RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))에 맞는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 단일 위치에만 두는 설계
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 충분히 보관하지 않는 설계
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 같은 수준으로 취급하는 설계

### 실무 시나리오

- 장애 후 시점 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Point-in-Time [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))
- 정기 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 아카이브 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 결합
- [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 환경에서 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)

- **📢 섹션 요약 비유**: 교무실 열쇠, 수업 기록, 배치도가 모두 있어야 학교를 다시 열 수 있는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

영구 저장소의 핵심은 "남긴다"가 아니라 "다시 살릴 수 있게 남긴다"이다. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 따로 보고 따로 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)해야 한다.

좋은 설계는 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 줄이고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 범위를 줄이며, 운영자가 시스템 상태를 빠르게 이해하게 만든다.

- **📢 섹션 요약 비유**: 일기, 영수증, 지도 세 장이 있어야 여행을 처음부터 다시 복기할 수 있다.

---

## 관련 개념 맵

```text
인스턴스(메모리)
   ↓
데이터 파일 / 로그 파일 / 제어 파일
   ↓
복구 / 기동 / 운영
```

---

## 관련 키워드 및 발전 흐름도

```text
휘발성 메모리
   ↓
영구 저장소
   ↓
Redo Log / Control File
   ↓
백업 · 복구 · 재생
```

---

## 어린이를 위한 3줄 비유 설명

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 진짜 물건이 들어 있는 창고예요.  
[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 무엇이 언제 바뀌었는지 적는 일기예요.  
제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 그 창고가 어디 있는지 알려 주는 지도예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 600

← **이전**: [58. 데이터베이스 인스턴스 (Database Instance) - 메모리와 백그라운드 프로세스](/knowledge-base/studynote/05_database/01_db_architecture_relational/058_database_instance_architecture/)
**다음**: [60. 서버리스 데이터베이스 (Serverless DB) - Amazon Aurora Serverless 등 자동 확장 아키텍처](/knowledge-base/studynote/05_database/01_db_architecture_relational/060_serverless_database_aurora/) →

---
