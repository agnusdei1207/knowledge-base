+++
title = "13. 데이터 디렉터리 (Data Directory) - 시스템만 접근 가능한 카탈로그 부분"
description = "DBMS 시스템 내부에서만 접근 가능한 카탈로그의 은닉 영역이자 핵심 제어 구조"
date = 2024-05-18

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# 13. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) 중 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/)([DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/)) 소프트웨어 자신만이 접근하고 갱신할 수 있는 고도의 보안/은닉 영역이다.
> 2. **가치**: 일반 사용자의 임의 접근을 차단하여 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 엔진의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적, 물리적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 매핑 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 완벽히 보장한다.
> 3. **융합**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Mode) 메모리 영역과 유사하게 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)과 안정성을 수호하는 기반 아키텍처 기술이다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 시스템에는 모든 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 사용자, 권한, 통계 등의 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 저장되는 '[시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/)([System Catalog](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/))'가 존재한다. 그러나 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 내의 모든 정보가 사용자에게 공개되어야 하는 것은 아니다. [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 내부에는 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 자체가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 디스크의 어느 물리적 블록(Block)에 읽고 쓸지, 내부 포인터 구조는 어떻게 되어 있는지를 나타내는 극도로 민감한 기계적 매핑 정보가 포함되어 있다.

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))는 [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) 내에서 <strong>오직 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 시스템(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/">DBMS</a> 엔진)만이 접근할 수 있도록 격리된 특수 구역</strong>이다. 만약 사용자가 이 물리적 포인터나 내부 매핑 정보에 접근하여 수정할 수 있다면, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 테이블 구조와 물리적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 간의 연결 고리가 끊어져 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 전체가 붕괴(Corruption)될 수 있다.

이처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 "[데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)([Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/))" 중에서도 특히 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조와 물리적 저장 구조 간의 은닉([Information Hiding](/knowledge-base/studynote/04_software_engineering/04_testing_quality/199_information_hiding_encapsulation/))을 완벽히 구현하기 위해 필수적인 아키텍처 요소이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">그림 1: 메타데이터 저장소의 권한별 격리 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">일반 사용자 / DBA</div><div class="kb-diagram-note">(질의, 권한 요청)</div></div>
<div class="kb-diagram-note">▼ (SELECT 허용)</div>
<div class="kb-diagram-note">&lt;─ 시스템 카탈로그 (System Catalog)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 사전 (Data Dictionary)</div><div class="kb-diagram-cell">: 논리적 스키마, 뷰, 사용자 통계 등</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(사용자 접근 가능 영역)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">&lt;─</div><div class="kb-diagram-node">엄격한 접근 통제벽</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 디렉터리 (Data Directory)</div><div class="kb-diagram-cell">: 물리적 블록 주소, 시스템 내부 포인터,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(DBMS 시스템 전용 영역)</div><div class="kb-diagram-cell">B-Tree 노드 물리적 연결 정보 등</div></div>
<div class="kb-diagram-note">▲ (내부 제어, DDL에 의한 자동 변경)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DBMS 내부 엔진 (Storage/Execution Engine)</div></div>
</div>
</div>



이 그림은 전체 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 저장소([시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/))가 권한과 접근 주체에 따라 어떻게 두 영역으로 쪼개지는지를 명확히 보여준다. 상단의 [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)은 사용자를 위한 읽기 전용 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 영역인 반면, 하단의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 오직 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 엔진만이 배타적으로 읽고 쓰는 시스템 격리 구역이다. 이 구조를 통해 악의적이거나 실수로 인한 물리적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 훼손 원천을 차단한다.

📢 **섹션 요약 비유**: 스마트폰에서 사용자가 볼 수 있는 '[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 앱([데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/))'과, 스마트폰 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)만이 조작할 수 있는 '[부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/)/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 숨김 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))'을 분리해 기기가 벽돌이 되는 것을 막는 원리와 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 내부의 스토리지 엔진(Storage Engine) 및 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 매니저([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System Manager)와 직접적으로 상호작용한다. 사용자가 [DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/)([Data Definition Language](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/)) 연산을 수행하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)가 백그라운드에서 조작된다.

| 구성 요소 | 역할 | 내부 동작 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)/제어 | 비유 |
|:---|:---|:---|:---|:---|
| <strong>물리적 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 매핑 테이블</strong> | 테이블/[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 저장된 실제 디스크 경로 및 [Extent](/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/) 관리 | 테이블스페이스에 새 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 할당되면 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 물리 경로(Inode 등) 기록 | 스토리지 엔진 I/O 호출 | 건물의 비밀 설계도 및 배관도 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/">B-Tree</a> <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 루트 포인터</strong> | 각 테이블의 기본키/보조 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 최상위 노드 디스크 주소 저장 | [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 스캔을 결정하면 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에서 Root 주소를 페치함 | 메모리 버퍼 풀 매핑 | 도서관 서고의 비밀 열쇠 보관함 |
| **블록 체인/프리리스트(Free List)** | 빈 블록(사용 가능한 공간)의 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 유지 | INSERT 발생 시 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 프리리스트를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하여 빈 블록에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 할당 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 커밋/[롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 시 갱신 | 빈 좌석 현황판 |
| <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 제어 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> (MVCC용) | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [격리성](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)을 위한 [Undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/) 세그먼트 포인터 유지 | [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 시 구버전([Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 위치한 블록 주소 추적 | [언두](/knowledge-base/studynote/05_database/07_exam_summary/454_undo_segment_rollback/) 매니저([Undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/) Manager) | 과거 기록 보관소의 타임머신 좌표 |
| <strong>접근 제어 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a></strong> ([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 대한 어떠한 외부 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(User SQL)도 원천 차단 | SQL 파서 단계에서 시스템 내부 객체로 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)되면 Exception 발생 (`ORA-00942` 등) | 시스템 레벨 락(System [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) | 출입 금지 구역 경보 장치 |

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 시스템이 구동([Mount](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) / Open)될 때 가장 먼저 메모리에 로드되는 영역 중 하나이다. DBMS는 제어 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(Control [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))을 읽어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 위치를 파악하고, 이를 통해 전체 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 1차적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">그림 2: DDL 실행 시 데이터 사전과 데이터 디렉터리의 동작 흐름도</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">사용자</div><div class="kb-diagram-note">"CREATE TABLE EMP (ID INT);"</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DBMS 파서 &amp; 실행기</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 1.</div><div class="kb-diagram-node">데이터 사전 (Data Dictionary)</div><div class="kb-diagram-note">접근</div></div>
<div class="kb-diagram-note">: 'EMP' 테이블명 중복 여부 확인, 논리적 스키마(ID INT) 메타데이터 INSERT</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 2.</div><div class="kb-diagram-node">스토리지 엔진 (Storage Engine)</div><div class="kb-diagram-note">호출</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 디렉터리 (Data Directory)</div><div class="kb-diagram-note">내부 동작</div></div>
<div class="kb-diagram-note">: 빈 공간(Free Extent) 탐색 → 논리 테이블 'EMP'와 할당된 물리적 디스크 블록 주소 매핑</div>
<div class="kb-diagram-note">: 내부 포인터 연결 정보 시스템만 은밀하게 갱신 (사용자 접근 불가)</div>
</div>
</div>



이 흐름도는 단순한 `CREATE TABLE` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 하나가 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)과 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 양쪽에 어떻게 다르게 작용하는지를 보여준다. 핵심은 1번 작업([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 등록)은 뷰를 통해 사용자가 조회할 수 있지만, 2번 작업(블록 할당 및 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) 매핑)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 내에서 완전히 캡슐화되어 은닉된다는 점이다. 이로 인해 물리적 디스크 구조가 변경되어도 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 영향을 받지 않는 '물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)'이 달성된다.

📢 **섹션 요약 비유**: 식당에서 손님이 볼 수 있는 '메뉴판([데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/))'에 신메뉴를 추가하는 동시에, 주방 안에서는 손님은 절대 들어갈 수 없는 '재료 보관 냉장고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))'에 공간을 몰래 마련하는 것과 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/)를 이루는 두 축인 [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)를 비교 분석하면 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 아키텍처의 설계 철학을 이해할 수 있다.

| 비교 항목 | [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) ([Data Dictionary](/knowledge-base/studynote/05_database/04_transactions_concurrency/509_data_dictionary/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)) | 판단 포인트 |
|:---|:---|:---|:---|
| **대상 독자 / 접근자** | 일반 사용자, [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/), 응용 프로그램 | 오직 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 시스템 엔진 자신 | 사용자 인터페이스 vs 시스템 인터페이스 |
| <strong>제공 정보의 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a></strong> | 고수준 ([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/): 테이블명, 뷰, 제약조건, 권한) | 저수준 (물리적 실체: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로, 블록 헤더, 포인터) | [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)을 위한 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층 분리 |
| **접근 방식 (Access)** | 시스템 제공 뷰(Views)를 통한 간접 `SELECT` | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 내부 C/C++ 소스코드를 통한 메모리 및 포인터 직접 연산 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어(SQL) 호환 여부 |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 훼손 시 파급</strong> | 특정 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 파싱 실패, 권한 오류 ([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 에러) | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 인스턴스 크래시, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 완전 소실 (물리적 에러) | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 복잡도 ([디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 손상 시 블록 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 필요) |

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)의 아키텍처와 융합해 보면, [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)은 OS의 `/proc` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이나 '작업 관리자([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Manager)'처럼 상태를 보여주는 사용자 모드(User Mode) 영역에 해당한다. 반면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 OS의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) 내 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))이나 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 Inode 구조체처럼 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Mode)에서만 제어되는 코어 영역과 완벽히 대응된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">그림 3: DBMS와 OS 메모리 보호 아키텍처의 유사성 비교</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DBMS 아키텍처</div><div class="kb-diagram-node">OS 아키텍처</div></div>
<div class="kb-diagram-note">User/DBA 쿼리 허용 User Application 허용</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Dictionary</div><div class="kb-diagram-cell">&lt;-----------------&gt;</div><div class="kb-diagram-cell">/proc, sysfs</div><div class="kb-diagram-cell">(상태 모니터링)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- - (격리벽) - -</div><div class="kb-diagram-cell">- (System Call)-</div><div class="kb-diagram-cell">(Mode Switch)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Directory</div><div class="kb-diagram-cell">&lt;-----------------&gt;</div><div class="kb-diagram-cell">Kernel Memory</div><div class="kb-diagram-cell">(OS만 조작 가능)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(물리적 포인터)</div><div class="kb-diagram-cell">System Engine 독점</div><div class="kb-diagram-cell">(페이지 테이블 등)</div></div>
</div>
</div>



이 도식은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 매커니즘이 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘과 설계적으로 동일한 궤를 가지고 있음을 보여준다. 두 구조 모두 하위 레벨의 복잡한 물리적 제어를 은닉함으로써, 사용자 레벨의 응용 프로그램이 안전하고 일관된 인터페이스만을 사용하도록 강제한다. 따라서 시스템 엔지니어는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 손상을 OS [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/)([Kernel Panic](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/))과 동급의 치명적 장애로 간주해야 한다.

📢 **섹션 요약 비유**: [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)이 '관제탑 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)'라면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 관제탑 아래에 묻혀 있어 시스템 관리자만 만질 수 있는 '복잡한 배선망'과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 개발자나 분석가는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 존재를 직접 인지할 일이 거의 없다. 하지만 시스템의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 책임지는 DBA나 아키텍트에게는 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 아키텍처에 대한 이해가 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝의 핵심 판단 기준이 된다.

<strong>1. 실무 시나리오: 시스템 크래시 후 부팅(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/">Mount</a>) 실패 판단</strong>
- **현상**: 정전 후 DB 인스턴스를 시작하려 했으나, "[System Catalog](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) Inconsistent" 또는 "Corrupt Block in [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)" 에러를 내며 오픈되지 않음.
- **의사결정**: 이는 [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)의 단순한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 오류가 아니라, 시스템이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 찾아가는 길목([디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 포인터)이 깨진 상태이다. 일반적인 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)으로 불가능하며, 오프라인 미디어 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([Media Recovery](/knowledge-base/studynote/05_database/04_transactions_concurrency/242_media_recovery_dump_archive_rollforward/))를 수행하거나 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)된 컨트롤 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/시스템 테이블스페이스를 복원(Restore)해야 한다.

<strong>2. <a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 마이그레이션 vs 물리적 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a> 의사결정</strong>
- **상황**: 대규모 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 다른 스토리지 서버로 이관.
- **판단**: `Export/Import` 도구([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Pump 등)는 [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)을 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하여 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 뽑아내는 반면, 스토리지 레벨의 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)이나 RMAN 같은 툴은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 물리적 블록 구조까지 통째로 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)한다. 따라서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각화([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))를 제거하고 싶다면 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 이관을, 다운타임을 최소화하고 시스템 상태를 그대로 덤프하고 싶다면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)가 포괄되는 물리적 이관을 선택해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">그림 4: 데이터베이스 장애 복구 판단 트리</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">장애 발생: 데이터 쿼리 실패</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">장애 원인이 메타데이터와 관련이 있는가?</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">아니오 ──&gt; (일반적인 트랜잭션 롤백, 데이터 Redo 적용)</div>
<div class="kb-diagram-tree-item" style="--depth:1">예</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">접근 불가 영역 판단</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 데이터 사전(딕셔너리) 뷰 훼손 ──&gt;</div><div class="kb-diagram-node">논리적 손상</div><div class="kb-diagram-note">딕셔너리 뷰 재컴파일 스크립트 실행 (복구 용이)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 데이터 디렉터리 블록 손상/Lost ──&gt;</div><div class="kb-diagram-node">물리적 치명상</div></div>
<div class="kb-diagram-note">(시스템 인스턴스 Down 발생)</div>
<div class="kb-diagram-note">(Full System Recovery 또는 Block Media Recovery 요망)</div>
</div>
</div>



이 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)는 장애의 양상에 따라 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 손상 부위를 진단하는 과정을 보여준다. [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)의 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))가 깨진 것은 껍데기가 벗겨진 것에 불과하여 스크립트로 재생성이 가능하지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)(물리적 포인터 블록)의 손상은 뼈대가 부러진 것이라 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 동원한 복잡한 미디어 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 필수적임을 시사한다. 

📢 **섹션 요약 비유**: 내비게이션 앱의 화면([데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/))이 깨지면 앱을 다시 깔면 되지만, 내비게이션 안의 GPS 센서 자체([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))가 고장나면 기기를 뜯어서 수리해야 하는 치명적인 상태인 것과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)는 사용자와 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이의 가장 강력한 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이자, 투명성(Transparency)을 제공하는 핵심 계층이다. 이 은닉 구조 덕분에 DBA는 사용자의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 단 한 줄도 수정하지 않고도, 디스크의 테이블을 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)하거나 스토리지를 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 플래시로 통째로 마이그레이션할 수 있는 완벽한 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)(Physical [Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/))을 달성한다.

[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) 및 스토리지-컴퓨팅 분리 아키텍처(예: Amazon [Aurora](/knowledge-base/studynote/05_database/06_dw_olap_trends/390_aurora_serverless_quorum_write/), [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)) 시대로 넘어오면서, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 역할은 더욱 중요해지고 있다. 컴퓨팅 노드와 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지 노드 간에 수많은 물리적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 청크(Chunk)가 쪼개져 저장되는데, 이 복잡한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 물리적 매핑 정보를 클러스터 차원에서 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 있게 관리하고 은닉하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 제어 기술이 현대 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 엔진의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성을 판가름하는 핵심 척도가 되고 있다.

📢 **섹션 요약 비유**: 완벽히 격리된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 덕분에, 승객들(사용자)은 열차가 디젤 엔진에서 전기 모터(저장 장치 변경)로 바뀐 것을 전혀 눈치채지 못하고 평화롭게 목적지에 도착할 수 있습니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) ([System Catalog](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/)) | [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)를 모두 포함하는 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 최상위 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 집합체
- [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) ([Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/)) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 구조나 물리적 저장소가 바뀌어도 응용 프로그램이 영향받지 않는 성질
- [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)가 물리적 디스크 주소(포인터)를 탐색할 때 활용하는 핵심 자료구조
- 스토리지 엔진 (Storage Engine) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)의 명령을 받아 실제 디스크의 블록 I/O를 수행하는 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 하위 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) (예: InnoDB)
- 블록 손상 (Block Corruption) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 물리적 정보가 깨져 DBMS가 해당 영역을 읽지 못하는 치명적 장애 상태

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 딕셔너리 (Data Dictionary) — DB 메타데이터의 중앙 저장소</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시스템 카탈로그 (System Catalog) — DBMS 내부 데이터 딕셔너리 구현체</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">메타데이터 관리 (Metadata Management) — 스키마·통계·권한 정보 통합 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 거버넌스 (Data Governance) — 정책 기반의 메타데이터 품질 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 카탈로그 (Data Catalog) — 비즈니스 맥락 추가, 데이터 검색·계보 제공</div></div>
</div>
</div>



이 흐름은 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 내부의 [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/)([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 딕셔너리)가 기업 수준의 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 도구와 현대적 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 은행의 금고 시스템을 상상해 보세요. 일반 고객은 "내 통장에 100만 원이 있다"는 장부([데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/))만 볼 수 있어요.
2. 하지만 그 100만 원짜리 지폐가 실제로 지하 금고의 몇 번 캐비닛 몇 번째 선반에 물리적으로 들어 있는지는 은행 시스템([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))만 알고 있어요.
3. 고객이 진짜 돈의 위치를 마음대로 알거나 옮길 수 없게 엄격히 숨겨놓았기 때문에, 금고 전체가 털리지 않고 안전하게 유지되는 원리랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 13 / 600

← **이전**: [12. 메타데이터 (Metadata) - 데이터에 대한 데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)
**다음**: [14. 데이터 모델 (Data Model) 구성 요소 - 구조(Structure), 연산(Operation), 제약조건(Constraint)](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) →

---
