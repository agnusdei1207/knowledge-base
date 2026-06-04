+++
title = "665. 시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Windows [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)([Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))는 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), 디바이스 드라이버, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 그리고 사용자 애플리케이션의 모든 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 정보(Configuration)를 수만 개의 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(INI) 대신 <strong>단일화된 계층형(Tree) <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong>로 관리하는 중앙 집중형 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 저장소다.
> 2. <strong>구조 (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/">Hive</a>)</strong>: [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 물리적으로 디스크에 흩어져 있는 여러 개의 이진 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/): SAM, [SECURITY](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), SOFTWARE, SYSTEM 등)들로 구성되며, 부팅 시 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 `Configuration Manager`가 이를 RAM으로 올려 하나의 거대한 가상 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 트리(HKEY_*)로 조립해 낸다.
> 3. **가치**: 이 아키텍처는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 파싱(Parsing)에 소모되는 CPU와 I/O 오버헤드를 극단적으로 줄이고, 다중 사용자 환경(Multi-user)에서 사용자별 프로필(NTUSER.DAT)을 동적으로 로드 및 언로드할 수 있게 하여 Windows가 거대한 엔터프라이즈 OS로 기능할 수 있는 근간이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>Windows <a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a></strong>: 윈도우 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 애플리케이션의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 하드웨어 정보, 사용자 프로필 등을 저장하는 중앙 집중식 계층형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/).
  - <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/">Hive</a> (하이브)</strong>: [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 트리의 특정 가지(Branch)를 물리적으로 저장하고 있는 디스크 상의 바이너리 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/).

- <strong>필요성 (INI <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 지옥의 종식)</strong>:
  - 과거 Windows 3.1 시절까지는 모든 프로그램이 각자의 폴더에 `win.ini`, `system.ini` 같은 텍스트 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 만들었다.
  - 프로그램이 수천 개로 늘어나자, OS가 부팅될 때 수천 개의 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 열고 파싱(Parsing)하느라 부팅이 엄청나게 느려졌다. (I/O 병목 및 캐시 부재)
  - 더 심각한 것은 보안이었다. 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 '누가 읽고 쓸 수 있는지' 권한을 섬세하게 통제하기 어려웠고, 여러 프로세스가 동시에 한 INI [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쓰려다 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 깨지는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 문제가 빈발했다.
  - **해결책**: 모든 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 관리하는 '하나의 고속 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)'로 몰아넣고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(`RegOpenKey`, `RegSetValue`)를 통해서만 접근하게 만들자!

  - <strong>과거 (INI <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>)</strong>: 회사 직원 1,000명이 각자의 책상 서랍에 중요한 서류를 보관한다. 사장님이 특정 정보를 찾으려면 1,000개의 서랍을 일일이 열어봐야 하고, 도둑이 들면 서랍을 통째로 털린다.
  - <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a></strong>: 거대한 중앙 도서관([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)). 모든 직원은 서류를 도서관 사서(Configuration Manager)에게 맡긴다. 사서는 서류를 체계적인 트리(Tree) 구조로 정리하고, 찰나의 속도로 검색해 주며, 사원증(권한)이 없는 자에게는 서류를 절대 보여주지 않는다.

- **발전 과정**:
  1. <strong>Windows 3.x (INI <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>)</strong>: 텍스트 기반, 파편화, [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)/보안 취약.
  2. <strong>Windows NT/95 (<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a> 도입)</strong>: COM([Component](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) Object Model) 클래스 정보를 저장하기 위해 도입 후 시스템 전체 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 확장.
  3. **Windows 2000 이후**: 사용자별 동적 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)(HKEY_CURRENT_USER) 지원 및 Transactional [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)(TxR) 도입으로 크래시 안정성 극대화.

- **📢 섹션 요약 비유**: 수만 개의 종이 쪼가리(INI)를 방구석에 어질러 놓고 찾던 구시대에서 벗어나, 철저하게 인덱싱된 하나의 거대한 엑셀 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))로 국가 통계(OS [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))를 일원화한 행정 혁명입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조 (5대 Root Keys)

우리가 `regedit.exe`를 열면 보이는 5개의 큰 폴더(`HKEY`)는 사실 디스크에 있는 모양이 아니라 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 조립해 낸 '가상 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))'다.

| Root [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) (HKEY) | 역할 및 내용 | 실제 매핑 (물리적 출처) |
|:---|:---|:---|
| **HKEY_LOCAL_MACHINE (HKLM)** | 컴퓨터 자체에 대한 글로벌 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (하드웨어, 드라이버, 시스템 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | \System32\[config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 하단의 SOFTWARE, SYSTEM 등 여러 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들의 합체 |
| **HKEY_USERS (HKU)** | 이 PC에 계정이 있는 모든 사용자의 프로필 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 모음 | 각 사용자의 `NTUSER.DAT` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들이 동적으로 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)됨 |
| **HKEY_CURRENT_USER (HKCU)**| 현재 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인한 사용자의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (바탕화면, [테마](/knowledge-base/studynote/04_software_engineering/03_design_architecture/184_theme_agile_requirements/) 등) | HKU 아래의 현재 사용자 SID(보안 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)) 폴더에 대한 바로가기(Symlink) |
| **HKEY_CLASSES_ROOT (HKCR)**| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 확장자 연결 프로그램, COM 객체 등록 정보 | HKLM\Software\Classes 와 HKCU\Software\Classes 의 융합(Merge) |
| **HKEY_CURRENT_CONFIG** | 현재 부팅 시 사용된 하드웨어 프로필 | HKLM\SYSTEM\CurrentControlSet\Hardware Profiles 에 대한 바로가기 |

---

### 하이브 ([Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 Configuration Manager

디스크의 물리적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/))이 어떻게 램(RAM)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 트리로 올라오는지에 대한 아키텍처다.

```text
  +-------------------------------------------------------------------+
  |                 Windows Registry Hive 마운트 메커니즘              |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [물리적 디스크 (Physical Storage)]                                   |
  |   - C:\Windows\System32\config\SYSTEM   (부팅/드라이버 설정)          |
  |   - C:\Windows\System32\config\SOFTWARE (프로그램 설치 정보)          |
  |   - C:\Users\Admin\NTUSER.DAT           (Admin 유저 개인 설정)        |
  |                                                                   |
  |  ==========v (부팅 및 로그인 시 커널에 로드됨) =========================|
  |                                                                   |
  |  [Windows Kernel (Configuration Manager)]                         |
  |                                                                   |
  |   (가상 트리 조립 - Virtual Registry Tree)                          |
  |   [\REGISTRY] (루트)                                              |
  |      +-- \MACHINE                                                 |
  |      |     +-- \SYSTEM   <--- (디스크의 SYSTEM 파일 전체가 여기 마운트됨) |
  |      |     +-- \SOFTWARE <--- (디스크의 SOFTWARE 파일 전체가 마운트됨) |
  |      |                                                            |
  |      +-- \USER                                                    |
  |            +-- \S-1-5-21... (Admin SID) <--- (NTUSER.DAT 가 마운트됨)|
  |                                                                   |
  |  ==========v (API를 통해 유저 스페이스에 노출) =========================|
  |                                                                   |
  |  [User Space (애플리케이션 및 regedit)]                               |
  |   - HKEY_LOCAL_MACHINE\SYSTEM  (가상화된 뷰를 통해 접근)               |
  |   - HKEY_CURRENT_USER          (현재 로그인 유저의 SID로 자동 점프)       |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 리눅스의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)(`mount /dev/sda1 /mnt`)와 완전히 똑같은 개념이다. 윈도우 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 Configuration Manager(CM)는 부팅 시 디스크에 흩어진 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 `Paged Pool`(메모리)로 읽어 들인다. 그리고 `\REGISTRY\MACHINE\SYSTEM` 이라는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 경로에 그 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 찰칵 끼워 넣는다. 사용자가 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인하면 그 사람 폴더의 `NTUSER.DAT`를 찾아 `\REGISTRY\USER\<SID>`에 동적으로 추가 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)한다. 이 구조 덕분에 "내가 바탕화면을 빨간색으로 바꿨다고 해서, 다른 계정으로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인한 동생의 바탕화면이 빨개지는 일"이 완벽하게 방지된다.

---

### 트랜잭셔널 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) (TxR - Transactional [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))

[레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 OS의 심장이므로, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Write) 도중 정전이 나면 윈도우는 영원히 부팅되지 않는다(Blue Screen).
이를 막기 위해 Windows Vista부터 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a>의 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>(ACID)</strong> 개념을 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)에 도입했다.

- 애플리케이션이나 윈도우 업데이트가 수백 개의 키를 수정할 때, 이를 하나의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(`RegCreateTransaction`)으로 묶는다.
- 수정 사항은 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 본체에 바로 쓰이지 않고, 숨겨진 `.LOG` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 먼저 순차적으로 기록된다 (WAL: [Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/)).
- 모든 수정이 완벽히 끝나면 커밋(Commit)하여 본체에 반영한다. 도중에 전원이 나가면 부팅 시 CM이 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 보고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))을 수행하여 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)가 깨지는 것을 100% 방어한다.

- **📢 섹션 요약 비유**: 수술([레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 수정)을 할 때 환자 몸에 바로 메스를 대지 않고, 옆에 있는 연습용 인형(.LOG)에 먼저 수술을 다 해본 뒤, 완벽하게 성공했을 때만 환자에게 1초 만에 덮어씌우는 극강의 안전판입니다.

---

## Ⅲ. 비교 및 연결

### [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 관리 패러다임 비교 (Windows vs Linux)

| 비교 항목 | Windows ([Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)) | Linux / Unix (/etc 밑의 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들) |
|:---|:---|:---|
| **저장 형태** | 중앙 집중형 이진(Binary) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) | 분산형 평문 텍스트(Plain Text) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| **파싱 오버헤드**| **거의 없음** ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)하고 바이너리로 직독) | **높음** (앱 구동 시 텍스트 파싱) |
| **보안 제어** | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 단위로 정밀한 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) (접근 제어) 부여 가능 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위의 소유권(rwx)으로만 제어 |
| **트러블슈팅** | 전용 툴(`regedit`) 필수. 깨지면 OS 부팅 불가 | `vi`, `cat`으로 언제든 수정/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능 |
| <strong>이식성/<a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a></strong> | 타 PC로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 옮기기 매우 까다로움 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 복사만 하면 끝 (GitOps에 유리함) |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB)</strong>: [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 자체가 거대한 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)(또는 유사 계층 구조) 기반의 인메모리(캐시) + 디스크 [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)다. 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(TxR), 캐시 무효화 등 RDBMS의 모든 핵심 요소가 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준에 미니멀하게 내장되어 있다.
- <strong>보안 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>: 악성코드나 루트킷이 윈도우 부팅 시 자기를 자동으로 실행시키기 위해 가장 먼저 노리는 곳이 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)의 `Run` 키(`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`)다. 이 때문에 현대 윈도우 디펜더는 이 특정 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 경로에 대한 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시도를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨([Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) Callback)에서 후킹하여 실시간 감시한다.

- **📢 섹션 요약 비유**: 윈도우 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 모든 정보가 일목요연하게 정리된 대형 마트이고, 리눅스의 /etc는 작은 동네 구멍가게들이 모여있는 골목길입니다. 마트는 계산([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 빠르지만 불이 나면 전체가 마비되고, 골목길은 일일이 찾아다니기 귀찮지만 가게 하나가 망해도 다른 가게는 멀쩡합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a> 팽창 (<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a> Bloat)으로 인한 시스템 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하</strong>: 5년간 포맷 없이 사용한 윈도우 서버에 수많은 프로그램을 지웠다 깔기를 반복했더니 부팅 속도가 10분 이상 걸리고 시스템이 버벅거림.
   - **원인 분석**: 프로그램들이 삭제(Uninstall)될 때 자신이 남긴 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 찌꺼기(Orphaned Keys)를 지우지 않았다. [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`SOFTWARE`)의 크기가 수백 MB로 비대해졌고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 부팅 시 이 거대한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 통째로 Paged Pool(메모리)에 올리느라 RAM과 I/O를 다 소모해버린 것이다.
   - **대응 (기술사적 가이드)**: 과거에는 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 클리너(CCleaner 등)를 썼지만, 잘못된 키 삭제로 OS가 박살나는 위험이 크다. 현대의 서버 운영(특히 클라우드)에서는 OS를 수년간 재사용하는 것(Pet)을 금지하고, 템플릿 이미지를 통해 서버를 주기적으로 완전히 새로 굽는(Cattle, [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) 방식으로 아키텍처를 전환해야 한다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/">멀티 테넌트</a>(<a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/">VDI</a>) 환경에서의 프로필 로드 실패</strong>: 데스크톱 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)([VDI](/knowledge-base/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/)) 환경에서 A 사용자가 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인했는데 "임시 프로필로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인되었습니다"라는 에러가 뜨며 바탕화면 아이콘이 다 날아감.
   - **원인 분석**: 사용자의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)인 `NTUSER.DAT` (HKCU의 원본)가 다른 프로세스(예: 백그라운드 [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 백신 스캔이나 윈도우 업데이트)에 의해 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))이 걸려 있어서, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Configuration Manager가 이 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 트리에 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)(Load)하는 데 실패한 것이다.
   - **대응**: UPHClean (User Profile [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) Cleanup) 같은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모듈을 적용하여, 유저 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)오프 시 `NTUSER.DAT`를 강제로 물고 있는 빗나간 프로세스의 핸들(Handle)을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단에서 강제로 끊어주어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 락을 해제해야 한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 Windows 애플리케이션 설정 저장소 아키텍처 플로우           |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [새로운 Windows 데스크톱/서버용 애플리케이션 개발 시 설정값 저장 방식 선택] |
  |                |                                                  |
  |                v                                                  |
  |      애플리케이션이 OS의 부팅이나 하드웨어, 타 프로세스(COM)와 깊게 엮이는가? |
  |          +- 예 ------> [Registry 사용 강제 (HKLM / HKCU)]             |
  |          |            - 드라이버 설정, 시스템 서비스 등록 등은 레지스트리가 필수 |
  |          +- 아니오 (단순한 독립형(Standalone) 유저 애플리케이션이다)      |
  |                |                                                  |
  |                v                                                  |
  |      사용자가 설정 파일을 직접 에디터로 고치거나, 클라우드(Git)로 백업해야 하는가?|
  |          +- 예 ------> [JSON / YAML / XML 형태의 로컬 파일 사용 권장]   |
  |          |            (예: `%APPDATA%\MyApp\config.json`)           |
  |          |                                                        |
  |          +- 아니오 ---> 레지스트리 사용 가능 (단, 성능 이슈로 남용 금지)      |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 마이크로소프트조차도 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)의 남용을 후회하고 있다. [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 윈도우 앱이 '포터블(Portable)' 해지는 것을 막는 최대 족쇄다. 요즘 개발되는 윈도우 애플리케이션이나 게임들은 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 전혀 건드리지 않고 자신의 설치 폴더나 `%APPDATA%` 폴더에 `json`이나 `ini` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 저장하는 과거 리눅스식 방식으로 회귀(리눅스화)하고 있다. 아키텍트는 글로벌 OS 세팅은 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)에, 앱 종속적 세팅은 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 분리 저장하는 투 트랙(Two-track) 설계를 지향해야 한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **WOW64 (32/64비트 리다이렉션)**: 64비트 윈도우에서 32비트 앱이 `HKLM\Software`에 글을 쓰려 할 때, 64비트 앱과 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 충돌하지 않도록 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 몰래 `HKLM\Software\WOW6432Node` 라는 격리된 공간으로 주소를 강제 변환(Redirection) 시켜주는 원리를 이해하고 코딩했는가?
- <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a> <a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (UAC)</strong>: 일반 권한(Non-admin) 앱이 관리자만 쓸 수 있는 `HKLM`에 억지로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 시도하면, 윈도우는 에러를 뱉는 대신 그 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 행위를 `HKCU\Software\Classes\VirtualStore`로 몰래 튕겨내어([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)) 앱이 죽는 것을 막아준다. 이 매직 때문에 "저장했다고 뜨는데 재부팅하면 날아가요"라는 버그가 발생하지 않는지 검증해야 한다.

- **📢 섹션 요약 비유**: [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 윈도우의 뇌(Brain)입니다. 너무 많은 기억(찌꺼기)을 집어넣으면 치매([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하)가 오고, 서로 다른 성격(32비트/64비트)이 한 공간에 섞이면 분열이 옵니다. 이를 막기 위해 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 뇌의 방을 쪼개고 거짓 기억(리다이렉션)을 심어주는 고도의 심리 치료를 병행하고 있습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 개별 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (구형) | Windows [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 아키텍처 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (파싱 속도)**| 부팅 시 수천 개 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 및 파싱 | [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/) [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)으로 `O(log N)` 탐색 | OS 부팅 및 앱 구동 속도 비약적 향상 |
| **정성 (보안 통제)**| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위의 거친 접근 제어 | 노드([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 단위의 정교한 보안 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 권한 탈취 및 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 무단 변조 원천 차단 |
| **정성 (다중 사용자)**| 유저별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 격리 복잡 (하드코딩) | 부팅 시 동적 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)(HKCU)를 통한 자동 뷰 | 완벽한 엔터프라이즈 멀티 유저 OS 달성 |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/070_container_registry_docker_hub_ecr/">컨테이너 레지스트리</a> 격리</strong>: Windows [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) on Windows) 기술의 핵심은 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)의 격리다. 호스트 OS의 거대한 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안으로 통째로 복사하는 것은 불가능하므로, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 전용의 'Diff(차분) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 하이브'를 메모리 상에서 호스트의 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)와 겹쳐 보여주는(Overlay) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술이 Windows 클라우드 네이티브의 핵심으로 동작하고 있다.
- <strong>탈 <a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a> (MSIX)</strong>: 마이크로소프트의 최신 앱 패키징 포맷인 `MSIX`는 설치 시 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 1바이트도 더럽히지 않는다. 앱 전용의 아주 작은 가상 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 공간을 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)처럼 만들어 앱이 켜질 때만 메모리에 붙였다가 끄면 떼어내는 방식으로, "윈도우는 쓰다 보면 느려진다"는 오랜 오명을 지워나가고 있다.

### 결론
Windows [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 1990년대 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 혁명기, 수만 개의 [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 소프트웨어가 뿜어내는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)의 혼돈(Chaos)을 잠재우기 위해 마이크로소프트가 내놓은 훌륭한 독재적 해결책이었다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨의 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), 동적 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)를 통해 OS의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안을 비약적으로 끌어올렸으나, 반대급부로 OS와 앱의 결합도를 너무 높여 현대의 유연한 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 생태계와는 다소 거리가 생겼다. 그럼에도 불구하고, 수억 줄의 윈도우 OS 코드가 한 치의 오차 없이 동작하게 만드는 이 거대한 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 정교함은 시스템 소프트웨어 역사에 남을 위대한 성취임이 분명하다.

- **📢 섹션 요약 비유**: 수만 개의 섬(프로그램)들이 각자의 법(INI)을 쓰던 난장판을 평정하고, 모든 권력과 법률([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))을 하나의 거대한 제국 수도([레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))로 중앙집권화하여 팍스 윈도우(Pax Windows)를 이룩한 통치 시스템입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| macOS/iOS Grand Central Dispatch ([GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/)) 블록 및 디스패치 큐 기반 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 구조 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| Windows [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 비동기 프로시저 호출 ([APC](/knowledge-base/studynote/02_operating_system/10_security/664_windows_kernel_apc_dpc_irql/)) 및 지연된 프로시저 호출 (DPC) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [보안 엔클레이브](/knowledge-base/studynote/02_operating_system/10_security/666_secure_enclave_trustzone_sgx_tee/) (TrustZone, [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/))와 OS [TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)) 연동 구조 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 철학 하의 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 레벨 런타임 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 검증망 설계 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)]
    |
    v
[시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조]
    |
    +---> [보안 엔클레이브 (TrustZone, SGX)와 OS TEE (Trusted Execution Environment) 연동 구조]
    +---> [제로 트러스트(Zero Trust) 철학 하의 운영체제 레벨 런타임 무결성 검증망 설계]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 수천 개의 프로그램이 살아요. 옛날에는 프로그램들이 각자 자기 방(폴더)에 비밀 노트를 숨겨둬서, 뭐가 어딨는지 찾으려면 하루 종일 걸렸어요.
2. 그래서 윈도우 대장님이 아주 크고 튼튼한 '중앙 대형 도서관([레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))'을 지었어요. 모든 프로그램은 자기 비밀 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 무조건 이 도서관에만 맡겨야 해요.
3. 도서관 사서([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 컴퓨터처럼 빠르게 책을 찾아주고, 남의 책은 절대 못 보게 철통 보안을 지켜줘서 컴퓨터가 빠르고 안전하게 돌아간답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 665 / 800

<- **이전**: [664. Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)](/knowledge-base/studynote/02_operating_system/10_security/664_windows_kernel_apc_dpc_irql/)
**다음**: [666. 보안 엔클레이브 (TrustZone, SGX)와 OS TEE (Trusted Execution Environment) 연동 구조](/knowledge-base/studynote/02_operating_system/10_security/666_secure_enclave_trustzone_sgx_tee/) ->

---
