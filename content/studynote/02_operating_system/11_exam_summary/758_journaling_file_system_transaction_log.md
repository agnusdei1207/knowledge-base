+++
title = "758. 저널링 파일 시스템 트랜잭션 로그 (Journaling File System Transaction Log)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [저널링 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/539_journaling_file_system/) ([Journaling File System](/knowledge-base/studynote/02_operating_system/09_file_system/539_journaling_file_system/))은 디스크에 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기록하기 전에, <strong>어떤 변경 작업을 할 것인지 그 계획을 미리 별도의 안전한 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 영역(저널, Journal)에 순차적으로 기록해 두는 아키텍처</strong>다.
> 2. **가치**: [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 도중 갑작스러운 정전이나 [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/)이 발생했을 때, 전통적인 `fsck` ([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 검사)로 디스크 전체를 스캔하느라 서버가 몇 시간씩 멈춰있는 악몽을 끝내고, <strong>단 몇 초 만에 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>(저널)를 다시 재생(Replay)하여 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템의 <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>을 즉각 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong>해 낸다.
> 3. **융합**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(DB) 시스템의 핵심인 '[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))'과 WAL ([Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/)) 철학을 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레이어로 그대로 이식하여 융합시킨, 현대 OS (ext4, XFS, NTFS)의 절대적 생존 표준 기술이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - 저널링은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 변경 사항([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 원본 디스크 위치에 반영하기 직전에, 원형 큐 구조로 된 전용 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 영역(Journal Area)에 일기장 쓰듯 순서대로 먼저 밀어 넣는(Commit) 기법이다.

- <strong>필요성 (디스크 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 붕괴의 공포)</strong>:
  - "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개를 만든다"는 행위는 내부적으로 매우 복잡한 다단계 톱니바퀴다.
  - ① i-node 1개 할당 $\rightarrow$ ② 빈 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 할당 $\rightarrow$ ③ [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 항목에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)명 추가 $\rightarrow$ ④ [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/).
  - 만약 ②번까지만 하고 갑자기 <strong>정전(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/">Power</a> Loss)</strong>이 되면 어떻게 될까? OS가 재부팅되면 그 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록은 "할당은 됐는데 가리키는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 없는" 영원한 쓰레기 고아 블록이 되어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 서서히 붕괴(Corruption)된다.
  - 구형 OS는 이걸 고치려고 부팅 시 `fsck` 프로그램을 돌려 테라바이트급 디스크의 수억 개 블록을 처음부터 끝까지 다 뒤져서 짝을 맞췄다 (부팅에만 5시간 소요).
  - **해결책**: "디스크를 다 뒤지지 말고, 정전 나기 1초 전에 <strong>'내가 지금부터 무슨 작업을 할 거다'</strong>라고 적어둔 일기장(저널)만 읽어보고 그것만 다시 덮어쓰거나 취소하자!"

  - **비저널링 (구형)**: 책상 위에 레고 조각 수만 개를 쏟아놓고 성을 조립하다가, 지진이 나서 흩어지면 처음부터 도면을 다 뒤져가며 잃어버린 조각이 뭔지 찾아내야 한다 (fsck 수시간 소요).
  - **저널링**: 조립하기 전에 꼭 작업 노트(저널)에 "지금 지붕 블록 3개를 끼울 거임"이라고 적고 조립한다. 지진이 나도 노트 맨 마지막 줄만 딱 읽어보면, 지붕 블록을 다시 껴야 하는지 아니면 아예 취소할 건지 1초 만에 알 수 있다.

- **등장 배경**:
  - 엔터프라이즈 서버 디스크 용량이 10GB를 넘어가면서 디스크 전체 검사(fsck) 시간이 인내의 한계를 돌파하자, IBM의 JFS나 SGI의 XFS 등 고성능 UNIX 진영에서 DB의 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 기법을 차용해 개발했고 리눅스의 ext3/ext4로 대중화되었다.

```text
  +-------------------------------------------------------------+
  |                 파일 시스템 충돌(Crash) 시의 복구 메커니즘 차이       |
  +-------------------------------------------------------------+
  |                                                             |
  |  [ 전통적 파일 시스템 (ext2, FAT32) ]                         |
  |                                                             |
  |   정전 발생! ⚡                                               |
  |   재부팅 -> OS: "아 찝찝해. 디스크 어딘가 꼬였을지 몰라."            |
  |   [fsck 실행]                                                |
  |   블록 1 검사.. 블록 2 검사.. ...... 블록 10,000,000 검사 완료!     |
  |   -> 결과: 수백 GB 탐색으로 수십 분 ~ 몇 시간 부팅 지연 ☠️            |
  |                                                             |
  |  [ 저널링 파일 시스템 (ext4, NTFS, XFS) ]                     |
  |                                                             |
  |   정전 발생! ⚡                                               |
  |   재부팅 -> OS: "일기장(Journal)의 최근 5줄만 확인하자."            |
  |   [로그 리플레이 (Log Replay)]                                 |
  |   - 로그: "파일 A 만들려다 말았음" -> 롤백 (작업 취소, 블록 해제)      |
  |   - 로그: "파일 B 다 쓰고 기록만 안했음" -> 리두 (저널에서 원본 덮어씀) |
  |   -> 결과: 디스크 용량과 무관하게 단 2~3초 만에 100% 복구 완료! 🚀     |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 저널링의 본질은 "[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 디스크 크기 비례(O(N))에서, 저널 크기 비례(O(1))로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)"한 위대한 알고리즘적 승리다. 과거에는 디스크가 10TB면 검사 시간도 10배 늘어났지만, 저널링 시스템에서는 디스크가 100PB(페타바이트)라 하더라도 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시 확인해야 할 영역은 수십 MB 크기의 작고 고정된 '저널([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))' 구역뿐이다. 부팅 시 이 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 구역만 재빨리 훑어보면 정전 직전에 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이던 미완성 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 무엇인지 정확히 짚어내고 외과 수술처럼 그 부위만 치료([Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)/[Undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/))할 수 있다.

- **📢 섹션 요약 비유**: 대형 마트에 도둑이 들었을 때, 저널링이 없는 마트는 물건이 10만 개면 10만 개를 다 세어봐야 뭐가 없어졌는지 압니다. 저널링이 있는 마트는 계산대 출입 명부(저널) 딱 1장만 확인하면 방금 뭐가 도둑맞았는지 1분 만에 파악하는 최첨단 재고 관리 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 저널링의 내부 파이프라인 (WAL 철학)

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 WAL ([Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/), [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전 로깅) 원리가 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 완벽히 이식된 구조다.

1. <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">Transaction</a> Start</strong>: 여러 개의 연산(i-node 갱신, 블록 할당)을 하나의 논리적 묶음([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))으로 선언한다.
2. <strong>Journal Write (일기 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>)</strong>: 변경될 내용을 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치가 아니라, 디스크 내의 안전한 '저널 영역(원형 큐)'에 순차적으로(Sequential) 빠르게 쭉 쓴다.
3. **Commit Record**: 저널 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 완벽히 끝나면, "이 작업 일기 다 썼음" 이라는 마침표(Commit Block)를 찍는다. ★정전 시 이 마침표가 없으면 해당 일기는 무효 처리([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))된다.★
4. <strong>Checkpoint (실제 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>)</strong>: 마침표까지 찍혔으면, 비로소 진짜 디스크 위치(원본)에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)([Delayed Write](/knowledge-base/studynote/02_operating_system/11_exam_summary/757_delayed_write_write_behind/)) 방식으로 반영한다.
5. **Free Journal**: 원본 반영까지 끝난 저널은 다 쓴 휴지가 되므로 삭제(원형 큐 포인터 이동)하여 공간을 확보한다.

### 리눅스 ext4의 3가지 저널링 모드 (핵심 트레이드오프)

저널 영역에 "[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이름, 크기 등)"만 적을 것인지, 아니면 "실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용물([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))"까지 전부 다 적을 것인지에 따라 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안전성의 시소가 크게 널뛰기한다.

```text
  +-------------------------------------------------------------------+
  |                 ext4 저널링 모드 비교 (성능 vs 무결성 트레이드오프)         |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 1. Data=Journal 모드 ] - 최강의 안전 (파라노이아 모드)             |
  |   동작: 메타데이터 + 실제 파일 데이터를 통째로 저널에 먼저 씀.                  |
  |   효과: 전원 차단 시 파일 내용까지 100% 완벽 복구.                         |
  |   부작용: 1GB 파일을 저장하면 저널에 1GB 쓰고, 원본에 1GB 쓰는 [2배 쓰기 페널티] |
  |        -> 속도가 반토막 나므로 실무에서는 거의 안 씀.                       |
  |                                                                   |
  |   [ 2. Data=Ordered 모드 (★ 디폴트 및 권장) ]                        |
  |   동작: 저널에는 "메타데이터(파일이름/크기)"만 씀.                          |
  |        단, 원본 위치에 "실제 데이터"를 쓴 것이 확실해진 후에야 저널을 커밋함!     |
  |   효과: 메타데이터와 파일 내용이 꼬일 일 없음. 쓰기 페널티 방어. 완벽한 타협점.   |
  |                                                                   |
  |   [ 3. Data=Writeback 모드 ] - 최강의 속도 (위험 모드)                |
  |   동작: 저널에 메타데이터만 씀. 실제 데이터는 언제 쓰이든 순서 상관없이 내팽개침.    |
  |   효과: 가장 빠름. (파일 시스템 뼈대는 안 깨짐 보장)                       |
  |   부작용: 정전 후 복구 시 파일 이름은 멀쩡한데 열어보면 안의 내용은 텅 비어있거나 |
  |         쓰레기 값이 들어있는 '파일 내용물 부패(Stale Data)' 위험 존재.        |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 설계자들의 깊은 고뇌가 담긴 설정이다. OS는 기본적으로 속도와 안전의 균형점인 `Ordered` 모드를 선택한다. 왜 `Writeback` 모드가 위험할까? 저널에 "A [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 10KB [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)"이라고만 적어두고 커밋을 쳤는데 정전이 났다 치자. 재부팅하면 OS는 저널을 보고 "아, A [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 10KB 할당!" 하고 빈 공간을 연결해 준다. 그런데 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 10KB는 아직 기록되기 전이었다. 그 결과, 할당된 10KB 블록에 이전에 쓰다 버린 '다른 사람의 은밀한 사진이나 비밀번호' 쓰레기 찌꺼기가 그대로 유저에게 노출되는 치명적 보안 사고가 터진다. `Ordered` 모드는 "반드시 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 먼저 원본에 바른 뒤에야 저널을 커밋한다"는 순서(Order)를 강제하여 이 재앙을 원천 봉쇄한다.

- **📢 섹션 요약 비유**: 이삿짐을 나를 때 박스 안의 물건([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))까지 전부 사진(저널)을 찍어두면 완벽하지만 시간([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 2배로 걸립니다(`Journal`). 그래서 내용물은 박스에 먼저 잘 집어넣은 걸 눈으로 확인한 뒤, 박스 겉면에 매직으로 이름표([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 저널)만 후다닥 적고 끝내는 것이 실무에서 쓰는 가장 현명한 `Ordered` 방식입니다.

---

## Ⅲ. 비교 및 연결

### [저널링 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/539_journaling_file_system/) (Journaling) vs [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 (ZFS, Btrfs)

저널링은 혁명적이었지만 '이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Double Write)'라는 근본적 한계를 피할 수 없다. 이를 타파하기 위해 등장한 넥스트 제네레이션이 [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)([Copy-On-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)) 기반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이다.

| 비교 항목 | [Journaling File System](/knowledge-base/studynote/02_operating_system/09_file_system/539_journaling_file_system/) (ext4, XFS) | [COW File System](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) (ZFS, Btrfs) |
|:---|:---|:---|
| **설계 철학** | 제자리에 덮어쓰기 (Overwrite-in-place) 전 일기장에 메모 | 절대로 원본을 덮어쓰지 않고 항상 새 빈 공간에 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) ([Copy-on-write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)) |
| <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 원리</strong> | 꼬였을 때 저널(일기장)을 보고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)/리플레이 | 원본을 안 건드렸으니 새 포인터만 옛날 걸로 돌리면 끝 (저널 필요 없음) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/">스냅샷</a> 기능</strong> | 무겁고 제약이 많음 (LVM 의존) | 빛의 속도로 테라바이트급 무한 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 1초 만에 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/">쓰기 증폭</a>(WA)</strong>| 저널 영역에 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 중복으로 써야 해서 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 수명 갉아먹음 | 덮어쓰기가 없어 분산되지만, 파편화([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))가 심하게 발생함 |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/">Redo</a>/<a href="/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/">Undo</a> Log)</strong>: 저널링은 DBMS의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(Oracle의 [Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) Log, InnoDB의 ib_logfile)에서 아이디어를 훔쳐 온 것이다. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 저널은 오직 '[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)의 구조적 붕괴'를 막기 위한 인프라 수준의 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수단이며, 응용 프로그램이 쓰던 '문서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)'까지 보장해 주는 것은 아니다. 따라서 DB 엔지니어는 OS 저널링을 맹신하지 않고 자기만의 WAL([Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/))과 fsync()를 독자적으로 반드시 쳐야 한다. (이중 로깅의 발생 원인).
- <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/">솔리드 스테이트 드라이브</a> (<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/">SSD FTL</a>)</strong>: [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러 내부의 [FTL](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)([Flash Translation Layer](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) 역시 덮어쓰기가 불가능한 플래시 특성상 내부적으로 저널링이나 COW와 유사한 포인터 매핑 방식을 사용한다. OS가 저널링을 위해 동일한 저널 블록을 너무 자주 쓰면 해당 블록의 플래시 셀만 집중적으로 타버리므로(Wear out), SSD는 [마모 평준화](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)([Wear Leveling](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/))를 통해 OS 몰래 내부적으로 쓰는 위치를 계속 섞어준다.

- **📢 섹션 요약 비유**: 저널링(ext4)이 기존의 오답 노트(원본)를 지우개로 빡빡 지우고 고쳐 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전에 만약을 위해 메모지(저널)에 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)해 두는 방식이라면, [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)(ZFS)는 아예 새 연습장을 한 장 꺼내서 정답을 새로 적은 다음 옛날 오답 노트를 쿨하게 찢어버리는 방식이라 애초에 꼬일 일이 없습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 운영 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

1. <strong>시나리오 — <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 수명 단축과 MySQL 이중 저널링 오버헤드</strong>: MySQL DB 서버를 AWS EBS([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에 세팅했는데, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 부하가 커지자 디스크 IOPS가 폭발하면서 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 심해졌다.
   - **원인 분석**: InnoDB 스토리지 엔진은 자체적으로 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) log)를 맹렬하게 기록한다. 그런데 밑바닥에 깔린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(ext4) 역시 저널링(`data=ordered`)을 돌리며 자기 나름대로 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 저널을 계속 쓰고 있다. 앱 단의 안전장치와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단의 안전장치가 겹치면서 디스크 입장에서는 1건의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)당 엄청난 이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)([Write Amplification](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)) 폭탄을 맞고 있는 것이다.
   - **아키텍트 판단 (저널링 비활성화 튜닝)**: DB 엔진이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 100% 책임지는 전용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 디스크 블록이라면, 과감하게 ext4의 저널링 기능을 끄는(disable) 극단적 최적화(`tune2fs -O ^has_journal`)를 단행하거나, 애초에 저널 오버헤드가 적은 XFS [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템으로 교체 포맷하여 스토리지 IOPS를 극한으로 아껴 내야 한다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">하이퍼바이저</a>/가상 머신(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>) 환경의 I/O 장벽(Barrier) 붕괴</strong>: [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) 호스트 위의 Linux VM이 정전으로 비정상 종료되었다. 재부팅 시 저널 리플레이(fsck)가 돌았는데도 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 수퍼블록이 아작나서 부팅이 불가([Mount](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) failed)한 참사가 일어났다. 저널링이 방어하지 못한 것이다.
   - **원인 분석**: 스토리지 컨트롤러나 하드웨어 [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 카드에는 속도를 높이기 위한 자체 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 캐시(Write Cache)가 있다. OS가 "저널 커밋 마침표 찍고 -> 그 다음에 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 써!"라고 아무리 순서를 지시(Barrier)해도, 밑단의 멍청한 레이드 카드가 캐시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이려고 자기 마음대로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 순서를 재배치(Reordering) 해버려, 저널 커밋보다 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 먼저 물리 디스크에 부어버렸다. 이때 전원이 나가니 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 현실의 인과율이 완전히 붕괴된 것이다.
   - <strong>아키텍트 판단 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/688_bbu/">BBU</a> 장착 및 배리어 점검)</strong>: 이 현상을 막으려면 OS가 내리는 `flush` / `fua` (Force Unit Access) 장벽 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 스토리지 하드웨어가 절대 씹지 않도록 설정해야 한다. 특히 하드웨어 레이드 컨트롤러를 쓴다면 정전 시 캐시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 며칠간 살려두는 <strong>배터리 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> 유닛(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/688_bbu/">BBU</a>, Battery <a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">Backup</a> Unit)이나 플래시 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/005_capacitor/">커패시터</a>(FBWC)</strong>가 반드시 정상 동작하는지 모니터링해야 한다. BBU가 고장 나면 컨트롤러는 살기 위해 즉시 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 캐시([Write-back](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/))를 끄고 느린 [Write-through](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/) 모드로 강등되어 전체 서버 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 반토막 난다.

```text
  +-------------------------------------------------------------------+
  |                 파일 시스템 계층의 이중 쓰기(Double Write) 병목 현상        |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 1건의 DB 트랜잭션이 디스크에 박히기까지의 숨겨진 비효율 ]                  |
  |                                                                   |
  |   DBMS (MySQL)     : 1. Redo Log 씀 ---> 2. Data 씀                 |
  |   (사용자 공간)                |                  |                     |
  |   --------------------------+------------------+------------------ |
  |   File System (ext4) :      v (파일 용량/수정시간 변경됨)             |
  |   (OS 커널 공간)          3. Journal 씀 ---> 4. 메타데이터 씀           |
  |                                                                   |
  |   결과: 1건의 데이터 저장을 위해 총 4번의 자잘한 랜덤 쓰기가 발생함!         |
  |        (DB 로그 1번 + DB 데이터 1번 + OS 저널 1번 + OS 메타 1번)       |
  |                                                                   |
  |   [ 아키텍트의 해결 솔루션 (Tuning) ]                                   |
  |   1. DB 데이터 파티션은 ext4 대신 **XFS** 사용 (메타데이터 로깅 최적화 우수)|
  |   2. DB 파일 크기를 미리 크게 할당(Pre-allocate)하여 OS의 저널링 개입 억제  |
  |   3. NVMe 기반 O_DIRECT를 사용하여 OS 페이지 캐시 및 저널 간섭 우회       |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 클라우드나 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 인프라를 지탱하는 아키텍트는 층층이 쌓인 소프트웨어 스택의 '안전망'들이 서로 충돌하여 만들어내는 중복 비용을 발라내야 한다. DB 엔진이 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 책임지고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) ext4가 저널링을 책임지고, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 내부의 FTL이 또 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 쓴다. "책임의 중첩"은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 암살자다. 고성능 인프라 엔지니어링의 정수는 이 중첩된 안전망 중 어느 층(Layer) 하나에만 책임을 몰아주고 나머지는 빗장을 풀어버리는 날카로운 결단에 있다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **ext2나 FAT32를 서버에 사용**: 저널링 기능이 없는 원시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(ext2)을 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 조금 빠르다는 이유로 프로덕션 서버의 루트 파티션에 사용하는 행위. 한 번이라도 비정상 종료([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/) 등)가 발생하면, 수 테라바이트 디스크를 `fsck`로 스캔하는 수 시간 동안 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 완벽한 오프라인(Downtime) 상태가 되는 최악의 참사를 맞이한다. 무조건 저널링(ext4/XFS)이 디폴트다.

- **📢 섹션 요약 비유**: 이중 삼중으로 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 일기를 쓰는 것은 좋지만, 100원짜리 사탕을 하나 팔 때마다 매장 장부에 적고, 본사 장부에 적고, 국세청 장부에 적느라 손님을 5분씩 세워둔다면(이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 병목) 그 가게는 망합니다. 신뢰할 수 있는 단 하나의 장부(최적화)에만 의존하는 과감함이 필요합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 비저널링 (ext2) | 저널링 기반 (ext4, XFS) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 시간, <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a>)</strong>| 용량에 비례해 수십 분 ~ 수 시간 소요 | 용량에 무관하게 **수 초 이내 (O(1))** 완료 | 비정상 종료 시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 복원 시간(Downtime) 극단적 단축 |
| <strong>정성 (<a href="/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/">무결성 보장</a>)</strong> | 고아 블록(Orphan block) 파편화 및 오작동 | 원자적(Atomic) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 갱신 보장 | OS 크래시나 하드웨어 리셋에 대한 강력한 내성(Robustness) |
| **정성 (운영 자동화)** | 관리자가 `fsck` 선택지(Y/N) 수동 입력 | OS 부트 로더가 저널 리플레이 자동 수행 | 사람 개입 없는 무인 서버/클라우드 환경의 자동 [재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) |

### 미래 전망
- <strong>DAX (<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/">Direct</a> Access)와 PMEM 최적화</strong>: 디스크 대신 램처럼 동작하는 비휘발성 영구 메모리(NVDIMM)가 등장하면서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 구조가 뿌리째 흔들리고 있다. 블록 단위 I/O로 동작하던 무거운 저널링 메커니즘 자체가 필요 없어지고, CPU의 캐시 플러시(CLFLUSH) [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 한 번으로 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 1바이트 단위로 실시간 보장하는 <strong>PMEM 전용 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템(NOVA, ext4-DAX)</strong>으로 패러다임이 이동 중이다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-On-Write</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템의 정복</strong>: 저널링을 쓰더라도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 덮어쓰기 도중 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체가 깨지는 현상([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Rot)은 막을 수 없다. 따라서 ZFS, Btrfs, APFS(애플)처럼 디스크 블록의 해시 [체크섬](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)([Checksum](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/))을 유지하고 언제나 새로운 빈 곳에만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰는 [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 아키텍처가 차세대 엔터프라이즈 및 개인용 데스크톱 OS의 절대 표준으로 자리 잡고 있다.

### 참고 표준
- <strong>POSIX <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> I/O 시스템 콜</strong>: UNIX 환경에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 오퍼레이션의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 정의하는 기반 규격. 저널링은 이 시스템 콜 아래의 블랙박스로서 OS 벤더 재량으로 구현됨.
- <strong>T10 SCSI / <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a> Flush Commands</strong>: 소프트웨어의 저널 커밋 명령이 물리적 디스크 플래터나 낸드 셀에 즉각 내려꽂히도록 보장하는 스토리지 하드웨어 하위 표준 규격 (FUA: Force Unit Access).

[저널링 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/539_journaling_file_system/)은 1990년대 중반, 덩치가 통제 불능으로 커져버린 디스크 스토리지의 붕괴(fsck의 저주)로부터 인류의 서버 인프라를 구원해 낸 은인이다. "무언가를 부수기(수정하기) 전에, 반드시 내가 무슨 짓을 할 건지 벽에 새겨두어라(Write-Ahead Log)." 이 단순하고도 아름다운 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 철학을 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 맨 밑바닥 심연에 이식함으로써, 오늘날 전 세계 수억 대의 클라우드 서버 인스턴스가 맘 편히 플러그를 뽑았다 켜면서도 부팅 10초 컷을 달성하는 기적을 누리고 있는 것이다.

- **📢 섹션 요약 비유**: 비행기가 추락(정전)하여 완전히 산산조각이 났을 때, 비행기 전체 파편을 이어 붙여(fsck) 사고 원인을 추리하는 불가능한 미션 대신, 튼튼한 '블랙박스(저널)' 하나만 열어보고 10분 만에 마지막 순간을 완벽히 재현해 내는(리플레이) 안전 공학의 위대한 승리입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 시스템 콜 오버헤드 이유 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [파일 지연 쓰기](/knowledge-base/studynote/02_operating_system/11_exam_summary/757_delayed_write_write_behind/) ([Delayed Write](/knowledge-base/studynote/02_operating_system/11_exam_summary/757_delayed_write_write_behind/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 블로킹 / 논블로킹 / 비동기 I/O | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [슬랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) ([Slab](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/)) 할당기 객체 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 지연 쓰기 (Delayed Write)]
    |
    v
[저널링 파일 시스템 트랜잭션 로그 (Journaling File System Transaction Log)]
    |
    +---> [블로킹 / 논블로킹 / 비동기 I/O]
    +---> [슬랩 (Slab) 할당기 객체 캐싱]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 레고로 커다란 성을 조립할 때, 실수로 발로 차서 성이 무너지면 수만 개의 조각을 설명서랑 하나하나 비교하며 고쳐야 해서 며칠이 걸렸어요. (옛날 컴퓨터)
2. 그래서 이제는 조립하기 전에 꼭 '작업 노트(저널)'에 "지금 지붕 빨간 블록 2개 끼울 차례임"이라고 순서대로 먼저 적어놓고 조립을 시작해요. (저널링)
3. 만약 도중에 쿵 하고 성이 무너져도(정전), 작업 노트 맨 끝줄만 딱 읽어보면 "아, 빨간 블록 끼우다 말았구나" 하고 1초 만에 원래대로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 수 있게 된 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 758 / 800

<- **이전**: [757. 파일 지연 쓰기 (Delayed Write)](/knowledge-base/studynote/02_operating_system/11_exam_summary/757_delayed_write_write_behind/)
**다음**: [759. 블로킹 / 논블로킹 / 비동기 I/O (Blocking Nonblocking Async I/O)](/knowledge-base/studynote/02_operating_system/11_exam_summary/759_blocking_nonblocking_async_io/) ->

---
