---
title: 13. 데이터 디렉터리 (Data Directory) - 시스템만 접근 가능한 카탈로그 부분
date: '2024-05-18'
description: DBMS 시스템 내부에서만 접근 가능한 카탈로그의 은닉 영역이자 핵심 제어 구조
tags:
- database
---

# 13. [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] ([[001_dikw_pyramid|Data]] [[506_directory_structure_symbol_table|Directory]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[011_system_catalog|시스템 카탈로그]] 중 [[003_dbms_database_management_system|데이터베이스 관리 시스템]]([[502_dbms|DBMS]]) 소프트웨어 자신만이 접근하고 갱신할 수 있는 고도의 보안/은닉 영역이다.
> 2. **가치**: 일반 사용자의 임의 접근을 차단하여 [[002_database_definition|데이터베이스]] 엔진의 [[369_logic_bomb|논리]]적, 물리적 [[012_metadata|메타데이터]] 매핑 [[003_integrity|무결성]]을 완벽히 보장한다.
> 3. **융합**: [[001_operating_system_purpose|운영체제]](OS)의 [[022_kernel_role|커널]] 모드([[022_kernel_role|Kernel]] Mode) 메모리 영역과 유사하게 [[004_data_independence|데이터 독립성]]과 안정성을 수호하는 기반 아키텍처 기술이다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[002_database_definition|데이터베이스]] 시스템에는 모든 [[005_schema|스키마]], 사용자, 권한, 통계 등의 [[012_metadata|메타데이터]]가 저장되는 '[[011_system_catalog|시스템 카탈로그]]([[011_system_catalog|System Catalog]])'가 존재한다. 그러나 [[394_catalog_metadata|카탈로그]] 내의 모든 정보가 사용자에게 공개되어야 하는 것은 아니다. [[394_catalog_metadata|카탈로그]] 내부에는 [[502_dbms|DBMS]] 자체가 [[001_dikw_pyramid|데이터]]를 디스크의 어느 물리적 블록(Block)에 읽고 쓸지, 내부 포인터 구조는 어떻게 되어 있는지를 나타내는 극도로 민감한 기계적 매핑 정보가 포함되어 있다.

[[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]([[001_dikw_pyramid|Data]] [[506_directory_structure_symbol_table|Directory]])는 [[011_system_catalog|시스템 카탈로그]] 내에서 **오직 [[002_database_definition|데이터베이스]] 시스템([[502_dbms|DBMS]] 엔진)만이 접근할 수 있도록 격리된 특수 구역**이다. 만약 사용자가 이 물리적 포인터나 내부 매핑 정보에 접근하여 수정할 수 있다면, [[369_logic_bomb|논리]]적 테이블 구조와 물리적 [[501_file_definition_logical_record|파일]] 시스템 간의 연결 고리가 끊어져 [[002_database_definition|데이터베이스]] 전체가 붕괴(Corruption)될 수 있다.

이처럼 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 "[[004_data_independence|데이터 독립성]]([[504_data_independence|Data Independence]])" 중에서도 특히 [[369_logic_bomb|논리]]적 구조와 물리적 저장 구조 간의 은닉([[199_information_hiding_encapsulation|Information Hiding]])을 완벽히 구현하기 위해 필수적인 아키텍처 요소이다.

```text
[그림 1: 메타데이터 저장소의 권한별 격리 구조]

[일반 사용자 / DBA] (질의, 권한 요청)
        │
        ▼ (SELECT 허용)
┌──────────────────────────────────────┐  <─ 시스템 카탈로그 (System Catalog)
│      데이터 사전 (Data Dictionary)   │     : 논리적 스키마, 뷰, 사용자 통계 등
│      (사용자 접근 가능 영역)         │
├──────────────────────────────────────┤  <─ [엄격한 접근 통제벽]
│    데이터 디렉터리 (Data Directory)  │     : 물리적 블록 주소, 시스템 내부 포인터,
│      (DBMS 시스템 전용 영역)         │       B-Tree 노드 물리적 연결 정보 등
└──────────────────────────────────────┘
        ▲ (내부 제어, DDL에 의한 자동 변경)
        │
[DBMS 내부 엔진 (Storage/Execution Engine)]
```

이 그림은 전체 [[012_metadata|메타데이터]] 저장소([[011_system_catalog|시스템 카탈로그]])가 권한과 접근 주체에 따라 어떻게 두 영역으로 쪼개지는지를 명확히 보여준다. 상단의 [[393_data_dictionary|데이터 사전]]은 사용자를 위한 읽기 전용 [[090_service_kubernetes_network_load_balancing|서비스]] 영역인 반면, 하단의 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 오직 [[502_dbms|DBMS]] 엔진만이 배타적으로 읽고 쓰는 시스템 격리 구역이다. 이 구조를 통해 악의적이거나 실수로 인한 물리적 [[012_metadata|메타데이터]] 훼손 원천을 차단한다.

📢 **섹션 요약 비유**: 스마트폰에서 사용자가 볼 수 있는 '[[009_config|설정]] 앱([[393_data_dictionary|데이터 사전]])'과, 스마트폰 [[001_operating_system_purpose|운영체제]]만이 조작할 수 있는 '[[029_bootloader|부트로더]]/[[022_kernel_role|커널]] 숨김 [[501_file_definition_logical_record|파일]]([[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]])'을 분리해 기기가 벽돌이 되는 것을 막는 원리와 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 [[502_dbms|DBMS]] 내부의 스토리지 엔진(Storage Engine) 및 [[501_file_definition_logical_record|파일]] 시스템 매니저([[501_file_definition_logical_record|File]] System Manager)와 직접적으로 상호작용한다. 사용자가 [[020_ddl|DDL]]([[020_ddl|Data Definition Language]]) 연산을 수행하면 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]가 백그라운드에서 조작된다.

| 구성 요소 | 역할 | 내부 동작 | [[295_protocol_field_tcp_udp_icmp|프로토콜]]/제어 | 비유 |
|:---|:---|:---|:---|:---|
| **물리적 [[501_file_definition_logical_record|파일]] 매핑 테이블** | 테이블/[[154_database_index_b_tree_search_optimization|인덱스]]가 저장된 실제 디스크 경로 및 [[531_extent_allocation|Extent]] 관리 | 테이블스페이스에 새 [[501_file_definition_logical_record|파일]]이 할당되면 [[506_directory_structure_symbol_table|디렉터리]]에 물리 경로(Inode 등) 기록 | 스토리지 엔진 I/O 호출 | 건물의 비밀 설계도 및 배관도 |
| **[[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]] 루트 포인터** | 각 테이블의 기본키/보조 [[154_database_index_b_tree_search_optimization|인덱스]]의 최상위 노드 디스크 주소 저장 | [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 [[154_database_index_b_tree_search_optimization|인덱스]] 스캔을 결정하면 [[506_directory_structure_symbol_table|디렉터리]]에서 Root 주소를 페치함 | 메모리 버퍼 풀 매핑 | 도서관 서고의 비밀 열쇠 보관함 |
| **블록 체인/프리리스트(Free List)** | 빈 블록(사용 가능한 공간)의 [[056_linked_list|연결 리스트]] 유지 | INSERT 발생 시 [[506_directory_structure_symbol_table|디렉터리]]의 프리리스트를 [[316_reference_pattern_nosql|참조]]하여 빈 블록에 [[001_dikw_pyramid|데이터]] 할당 | [[191_transaction_concept_states|트랜잭션]] 커밋/[[098_rollback_strategy_pipeline_error_threshold|롤백]] 시 갱신 | 빈 좌석 현황판 |
| **[[288_version_ihl_tos_total_length|버전]] 제어 [[012_metadata|메타데이터]]** (MVCC용) | [[191_transaction_concept_states|트랜잭션]] [[195_isolation_concurrency_control|격리성]]을 위한 [[393_undo|Undo]] 세그먼트 포인터 유지 | [[014_concurrency|동시성]] 제어 시 구버전([[637_zfs_snapshot_cow_architecture|Snapshot]]) [[001_dikw_pyramid|데이터]]가 위치한 블록 주소 추적 | [[454_undo_segment_rollback|언두]] 매니저([[393_undo|Undo]] Manager) | 과거 기록 보관소의 타임머신 좌표 |
| **접근 제어 [[192_module_independence|모듈]]** ([[547_access_control_rwx|Access Control]]) | [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]에 대한 어떠한 외부 [[298_qkv_attention|쿼리]](User SQL)도 원천 차단 | SQL 파서 단계에서 시스템 내부 객체로 [[655_ir_detection_analysis|식별]]되면 Exception 발생 (`ORA-00942` 등) | 시스템 레벨 락(System [[510_lock|Lock]]) | 출입 금지 구역 경보 장치 |

[[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 시스템이 구동([[516_mount_mechanism|Mount]] / Open)될 때 가장 먼저 메모리에 로드되는 영역 중 하나이다. DBMS는 제어 [[501_file_definition_logical_record|파일]](Control [[501_file_definition_logical_record|File]])을 읽어 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]의 위치를 파악하고, 이를 통해 전체 [[002_database_definition|데이터베이스]]의 [[003_integrity|무결성]]을 1차적으로 [[395_verification_process_review|검증]]한다.

```text
[그림 2: DDL 실행 시 데이터 사전과 데이터 디렉터리의 동작 흐름도]

[사용자] "CREATE TABLE EMP (ID INT);"
   │
   ▼
[DBMS 파서 & 실행기]
   │
   ├─ 1. [데이터 사전 (Data Dictionary)] 접근
   │     : 'EMP' 테이블명 중복 여부 확인, 논리적 스키마(ID INT) 메타데이터 INSERT
   │
   └─ 2. [스토리지 엔진 (Storage Engine)] 호출
         │
         ▼
      [데이터 디렉터리 (Data Directory)] 내부 동작
         : 빈 공간(Free Extent) 탐색 → 논리 테이블 'EMP'와 할당된 물리적 디스크 블록 주소 매핑
         : 내부 포인터 연결 정보 시스템만 은밀하게 갱신 (사용자 접근 불가)
```

이 흐름도는 단순한 `CREATE TABLE` [[158_instruction|명령어]] 하나가 [[369_logic_bomb|논리]]적 [[393_data_dictionary|데이터 사전]]과 물리적 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] 양쪽에 어떻게 다르게 작용하는지를 보여준다. 핵심은 1번 작업([[369_logic_bomb|논리]] [[005_schema|스키마]] 등록)은 뷰를 통해 사용자가 조회할 수 있지만, 2번 작업(블록 할당 및 [[323_physical_address|물리 주소]] 매핑)은 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] 내에서 완전히 캡슐화되어 은닉된다는 점이다. 이로 인해 물리적 디스크 구조가 변경되어도 [[369_logic_bomb|논리]]적 [[298_qkv_attention|쿼리]]는 영향을 받지 않는 '물리적 [[004_data_independence|데이터 독립성]]'이 달성된다.

📢 **섹션 요약 비유**: 식당에서 손님이 볼 수 있는 '메뉴판([[393_data_dictionary|데이터 사전]])'에 신메뉴를 추가하는 동시에, 주방 안에서는 손님은 절대 들어갈 수 없는 '재료 보관 냉장고([[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]])'에 공간을 몰래 마련하는 것과 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[011_system_catalog|시스템 카탈로그]]를 이루는 두 축인 [[393_data_dictionary|데이터 사전]]과 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]를 비교 분석하면 [[502_dbms|DBMS]] [[012_metadata|메타데이터]] 아키텍처의 설계 철학을 이해할 수 있다.

| 비교 항목 | [[393_data_dictionary|데이터 사전]] ([[509_data_dictionary|Data Dictionary]]) | [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] ([[001_dikw_pyramid|Data]] [[506_directory_structure_symbol_table|Directory]]) | 판단 포인트 |
|:---|:---|:---|:---|
| **대상 독자 / 접근자** | 일반 사용자, [[025_dba_database_administrator|DBA]], 응용 프로그램 | 오직 [[502_dbms|DBMS]] 시스템 엔진 자신 | 사용자 인터페이스 vs 시스템 인터페이스 |
| **제공 정보의 [[198_abstraction_control_data_process|추상화]]** | 고수준 ([[369_logic_bomb|논리]]적 [[198_abstraction_control_data_process|추상화]]: 테이블명, 뷰, 제약조건, 권한) | 저수준 (물리적 실체: [[501_file_definition_logical_record|파일]] 경로, 블록 헤더, 포인터) | [[004_data_independence|데이터 독립성]]을 위한 [[198_abstraction_control_data_process|추상화]] 계층 분리 |
| **접근 방식 (Access)** | 시스템 제공 뷰(Views)를 통한 간접 `SELECT` | [[502_dbms|DBMS]] 내부 C/C++ 소스코드를 통한 메모리 및 포인터 직접 연산 | [[298_qkv_attention|쿼리]] 언어(SQL) 호환 여부 |
| **[[003_integrity|무결성]] 훼손 시 파급** | 특정 [[298_qkv_attention|쿼리]] 파싱 실패, 권한 오류 ([[369_logic_bomb|논리]]적 에러) | [[502_dbms|DBMS]] 인스턴스 크래시, [[001_dikw_pyramid|데이터]] 완전 소실 (물리적 에러) | [[658_ir_recovery|복구]] 복잡도 ([[506_directory_structure_symbol_table|디렉터리]] 손상 시 블록 [[658_ir_recovery|복구]] 필요) |

[[001_operating_system_purpose|운영체제]](OS)의 아키텍처와 융합해 보면, [[393_data_dictionary|데이터 사전]]은 OS의 `/proc` [[501_file_definition_logical_record|파일]] 시스템이나 '작업 관리자([[150_task|Task]] Manager)'처럼 상태를 보여주는 사용자 모드(User Mode) 영역에 해당한다. 반면, [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 OS의 [[022_kernel_role|커널]]([[022_kernel_role|Kernel]]) 내 [[353_page_table|페이지 테이블]]([[353_page_table|Page Table]])이나 [[501_file_definition_logical_record|파일]] 시스템 Inode 구조체처럼 [[022_kernel_role|커널]] 모드([[022_kernel_role|Kernel]] Mode)에서만 제어되는 코어 영역과 완벽히 대응된다.

```text
[그림 3: DBMS와 OS 메모리 보호 아키텍처의 유사성 비교]

   [DBMS 아키텍처]                           [OS 아키텍처]
┌──────────────────┐ User/DBA 쿼리 허용  ┌──────────────────┐ User Application 허용
│  Data Dictionary │ <-----------------> │  /proc, sysfs    │ (상태 모니터링)
├──────────────────┤                     ├──────────────────┤
│ - - (격리벽) - - │                     │ - (System Call)- │ (Mode Switch)
├──────────────────┤                     ├──────────────────┤
│  Data Directory  │ <-----------------> │  Kernel Memory   │ (OS만 조작 가능)
│ (물리적 포인터)  │ System Engine 독점  │ (페이지 테이블 등)│
└──────────────────┘                     └──────────────────┘
```

이 도식은 [[002_database_definition|데이터베이스]]의 [[506_directory_structure_symbol_table|디렉터리]] [[571_protection_vs_security|보호]] 매커니즘이 [[001_operating_system_purpose|운영체제]]의 [[022_kernel_role|커널]] [[571_protection_vs_security|보호]] 메커니즘과 설계적으로 동일한 궤를 가지고 있음을 보여준다. 두 구조 모두 하위 레벨의 복잡한 물리적 제어를 은닉함으로써, 사용자 레벨의 응용 프로그램이 안전하고 일관된 인터페이스만을 사용하도록 강제한다. 따라서 시스템 엔지니어는 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] 손상을 OS [[036_kernel_panic|커널 패닉]]([[036_kernel_panic|Kernel Panic]])과 동급의 치명적 장애로 간주해야 한다.

📢 **섹션 요약 비유**: [[393_data_dictionary|데이터 사전]]이 '관제탑 [[229_monitor|모니터]]'라면, [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 관제탑 아래에 묻혀 있어 시스템 관리자만 만질 수 있는 '복잡한 배선망'과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 개발자나 분석가는 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]의 존재를 직접 인지할 일이 거의 없다. 하지만 시스템의 [[003_integrity|무결성]]을 책임지는 DBA나 아키텍트에게는 [[506_directory_structure_symbol_table|디렉터리]] 아키텍처에 대한 이해가 장애 [[658_ir_recovery|복구]]([[658_ir_recovery|Recovery]])와 [[282_performance_tactics|성능]] 튜닝의 핵심 판단 기준이 된다.

**1. 실무 시나리오: 시스템 크래시 후 부팅([[516_mount_mechanism|Mount]]) 실패 판단**
- **현상**: 정전 후 DB 인스턴스를 시작하려 했으나, "[[011_system_catalog|System Catalog]] Inconsistent" 또는 "Corrupt Block in [[001_dikw_pyramid|Data]] [[506_directory_structure_symbol_table|Directory]]" 에러를 내며 오픈되지 않음.
- **의사결정**: 이는 [[393_data_dictionary|데이터 사전]]의 단순한 [[369_logic_bomb|논리]]적 오류가 아니라, 시스템이 [[501_file_definition_logical_record|파일]]을 찾아가는 길목([[506_directory_structure_symbol_table|디렉터리]] 포인터)이 깨진 상태이다. 일반적인 [[098_rollback_strategy_pipeline_error_threshold|롤백]]으로 불가능하며, 오프라인 미디어 [[658_ir_recovery|복구]]([[242_media_recovery_dump_archive_rollforward|Media Recovery]])를 수행하거나 [[555_backup_and_restore_strategy|백업]]된 컨트롤 [[501_file_definition_logical_record|파일]]/시스템 테이블스페이스를 복원(Restore)해야 한다.

**2. [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 마이그레이션 vs 물리적 [[016_replication_factor|복제]] 의사결정**
- **상황**: 대규모 [[002_database_definition|데이터베이스]]를 다른 스토리지 서버로 이관.
- **판단**: `Export/Import` 도구([[001_dikw_pyramid|Data]] Pump 등)는 [[393_data_dictionary|데이터 사전]]을 [[316_reference_pattern_nosql|참조]]하여 [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]]를 뽑아내는 반면, 스토리지 레벨의 [[022_snapshot_backup_architecture|스냅샷]]이나 RMAN 같은 툴은 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]의 물리적 블록 구조까지 통째로 [[016_replication_factor|복제]]한다. 따라서 [[001_dikw_pyramid|데이터]] 조각화([[291_fragmentation_and_reassembly_process|Fragmentation]])를 제거하고 싶다면 [[369_logic_bomb|논리]]적 이관을, 다운타임을 최소화하고 시스템 상태를 그대로 덤프하고 싶다면 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]가 포괄되는 물리적 이관을 선택해야 한다.

```text
[그림 4: 데이터베이스 장애 복구 판단 트리]

[장애 발생: 데이터 쿼리 실패]
          │
          ▼
[장애 원인이 메타데이터와 관련이 있는가?]
   ├─ 아니오 ──> (일반적인 트랜잭션 롤백, 데이터 Redo 적용)
   │
   └─ 예
      ▼
   [접근 불가 영역 판단]
      ├─ 데이터 사전(딕셔너리) 뷰 훼손 ──> [논리적 손상] 딕셔너리 뷰 재컴파일 스크립트 실행 (복구 용이)
      │
      └─ 데이터 디렉터리 블록 손상/Lost ──> [물리적 치명상] 
            │                                  ▼
            │                         (시스템 인스턴스 Down 발생)
            │                         (Full System Recovery 또는 Block Media Recovery 요망)
```

이 [[124_decision_tree|의사결정 트리]]는 장애의 양상에 따라 [[012_metadata|메타데이터]] 손상 부위를 진단하는 과정을 보여준다. [[393_data_dictionary|데이터 사전]]의 뷰([[151_sql_view_virtual_table|View]])가 깨진 것은 껍데기가 벗겨진 것에 불과하여 스크립트로 재생성이 가능하지만, [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]](물리적 포인터 블록)의 손상은 뼈대가 부러진 것이라 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 동원한 복잡한 미디어 [[658_ir_recovery|복구]]가 필수적임을 시사한다. 

📢 **섹션 요약 비유**: 내비게이션 앱의 화면([[393_data_dictionary|데이터 사전]])이 깨지면 앱을 다시 깔면 되지만, 내비게이션 안의 GPS 센서 자체([[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]])가 고장나면 기기를 뜯어서 수리해야 하는 치명적인 상태인 것과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]는 사용자와 물리적 [[001_dikw_pyramid|데이터]] 사이의 가장 강력한 [[690_firewall_generation_evolution|방화벽]]이자, 투명성(Transparency)을 제공하는 핵심 계층이다. 이 은닉 구조 덕분에 DBA는 사용자의 [[298_qkv_attention|쿼리]]를 단 한 줄도 수정하지 않고도, 디스크의 테이블을 [[179_table_partitioning_concept|파티셔닝]]하거나 스토리지를 [[482_nvme|NVMe]] 플래시로 통째로 마이그레이션할 수 있는 완벽한 물리적 [[004_data_independence|데이터 독립성]](Physical [[504_data_independence|Data Independence]])을 달성한다.

[[531_cloud_native_architecture|클라우드 네이티브]]([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]]) 및 스토리지-컴퓨팅 분리 아키텍처(예: Amazon [[390_aurora_serverless_quorum_write|Aurora]], [[541_cassandra|Snowflake]]) 시대로 넘어오면서, [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]의 역할은 더욱 중요해지고 있다. 컴퓨팅 노드와 [[136_variance|분산]] 스토리지 노드 간에 수많은 물리적 [[501_file_definition_logical_record|파일]]과 청크(Chunk)가 쪼개져 저장되는데, 이 복잡한 [[136_variance|분산]] 물리적 매핑 정보를 클러스터 차원에서 [[194_consistency_database_integrity|일관성]] 있게 관리하고 은닉하는 [[136_variance|분산]] [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] 제어 기술이 현대 [[502_dbms|DBMS]] 엔진의 [[282_performance_tactics|성능]]과 안정성을 판가름하는 핵심 척도가 되고 있다.

📢 **섹션 요약 비유**: 완벽히 격리된 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]] 덕분에, 승객들(사용자)은 열차가 디젤 엔진에서 전기 모터(저장 장치 변경)로 바뀐 것을 전혀 눈치채지 못하고 평화롭게 목적지에 도착할 수 있습니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- [[011_system_catalog|시스템 카탈로그]] ([[011_system_catalog|System Catalog]]) | [[393_data_dictionary|데이터 사전]]과 [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]를 모두 포함하는 [[502_dbms|DBMS]] 최상위 [[012_metadata|메타데이터]] 집합체
- [[004_data_independence|데이터 독립성]] ([[504_data_independence|Data Independence]]) | [[005_schema|스키마]] 구조나 물리적 저장소가 바뀌어도 응용 프로그램이 영향받지 않는 성질
- [[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]] 구조 ([[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|Index]]) | [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]가 물리적 디스크 주소(포인터)를 탐색할 때 활용하는 핵심 자료구조
- 스토리지 엔진 (Storage Engine) | [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]의 명령을 받아 실제 디스크의 블록 I/O를 수행하는 [[502_dbms|DBMS]] 하위 [[192_module_independence|모듈]] (예: InnoDB)
- 블록 손상 (Block Corruption) | [[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]]나 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]의 물리적 정보가 깨져 DBMS가 해당 영역을 읽지 못하는 치명적 장애 상태

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 딕셔너리 (Data Dictionary) — DB 메타데이터의 중앙 저장소]
    │
    ▼
[시스템 카탈로그 (System Catalog) — DBMS 내부 데이터 딕셔너리 구현체]
    │
    ▼
[메타데이터 관리 (Metadata Management) — 스키마·통계·권한 정보 통합 관리]
    │
    ▼
[데이터 거버넌스 (Data Governance) — 정책 기반의 메타데이터 품질 관리]
    │
    ▼
[데이터 카탈로그 (Data Catalog) — 비즈니스 맥락 추가, 데이터 검색·계보 제공]
```

이 흐름은 [[502_dbms|DBMS]] 내부의 [[011_system_catalog|시스템 카탈로그]]([[001_dikw_pyramid|데이터]] 딕셔너리)가 기업 수준의 [[052_data_governance_framework|데이터 거버넌스]] 도구와 현대적 [[213_data_catalog_metadata|데이터 카탈로그]]로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 은행의 금고 시스템을 상상해 보세요. 일반 고객은 "내 통장에 100만 원이 있다"는 장부([[393_data_dictionary|데이터 사전]])만 볼 수 있어요.
2. 하지만 그 100만 원짜리 지폐가 실제로 지하 금고의 몇 번 캐비닛 몇 번째 선반에 물리적으로 들어 있는지는 은행 시스템([[001_dikw_pyramid|데이터]] [[506_directory_structure_symbol_table|디렉터리]])만 알고 있어요.
3. 고객이 진짜 돈의 위치를 마음대로 알거나 옮길 수 없게 엄격히 숨겨놓았기 때문에, 금고 전체가 털리지 않고 안전하게 유지되는 원리랍니다.
