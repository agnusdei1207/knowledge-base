---
title: "011. System Catalog"
date: "2024-05-20"
tags:
  - "database"
  - "studynote-database"
weight: 11
---
# 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) (System [Catalog](/studynote/05_database/07_exam_summary/394_catalog_metadata/))와 [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 저장된 모든 객체(테이블, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 뷰, 권한 등)에 대한 정의와 명세, 즉 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/), [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/))'를 저장하는 시스템 전용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)입니다.
> 2. **가치**: [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 파서(Parser)와 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))가 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)의 문법을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고 최적의 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)([Execution Plan](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/))을 수립하는 데 필요한 모든 통계적, 구조적 정보를 제공하는 뇌(Brain) 역할을 합니다.
> 3. **융합**: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 할당 테이블([FAT](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)/i-node), [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 하이브 메타스토어([Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) Metastore) 및 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 플랫폼과 철학적으로 동일한 메타 관리 체계입니다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) (System [Catalog](/studynote/05_database/07_exam_summary/394_catalog_metadata/))는 흔히 [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/) ([Data Dictionary](/studynote/05_database/04_transactions_concurrency/509_data_dictionary/))이라고도 불리며, [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 스스로가 시스템을 운영하고 통제하기 위해 구축해 놓은 특별한 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)입니다. 일반 사용자가 급여나 재고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장한다면, 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 "이 시스템에 어떤 테이블이 있고, 컬럼의 길이는 얼마이며, 누가 접근 권한을 가졌는가?"라는 구조적 정보([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/))를 저장합니다.
만약 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)가 없다면, 사용자가 `SELECT * FROM EMP`를 요청했을 때 DBMS는 `EMP`라는 테이블이 존재하는지, 사용자가 읽기 권한이 있는지 판단할 기준점이 없습니다. 나아가, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 건수나 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 상태 같은 통계 정보가 없으므로 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 풀 스캔을 할지 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 탈지 비용을 계산(Cost-Based Optimization)할 수도 없습니다. 즉, 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 DBMS가 단순한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 보관함을 넘어 스스로 생각하고 최적화하는 '지능형 시스템'이 되게 하는 핵심 중추입니다.

이 그림은 일반 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 분리를 보여줍니다.
```text
+----------------- DBMS Engine ------------------+
|                                                |
|  [사용자 질의] SELECT * FROM Employee;         |
|           v                                    |
|  [ 질의 파서 / 옵티마이저 ] --(메타데이터 참조)--+ |
|           v                                  v |
|  [ 사용자 데이터베이스 ]              [ 시스템 카탈로그 ]|
|  - Employee Table                   - SYSTABLES  |
|  - Order Table                      - SYSCOLUMNS |
|  - Product Table                    - SYSINDEXES |
|  (실제 비즈니스 데이터)               (메타 & 통계 정보)|
+------------------------------------------------+
```
이 도식의 핵심은 모든 사용자 질의 처리가 반드시 우측의 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 조회를 거쳐야만 좌측의 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 접근할 수 있다는 점입니다. 따라서 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 영역에 I/O 병목이 생기면 시스템 전체의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 마비됩니다. 실무에서는 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 접근 속도를 극대화하기 위해 이를 메모리에 상주시키는 '딕셔너리 캐시(Dictionary Cache)' 계층을 반드시 운영합니다.

📢 **섹션 요약 비유**: 도서관에 있는 수만 권의 진짜 책(사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 찾기 위해, 책의 위치와 대출 가능 여부를 꼼꼼하게 기록해 둔 '도서 검색용 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 카드함(시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/))'과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 자체도 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)(테이블) 형태로 구성되며, [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 내부 메커니즘에 의해 자동으로 갱신됩니다.

| 구성 요소 | 역할 | 내부 동작/특징 | 대표적 저장 정보 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/509_data_dictionary/">Data Dictionary</a></strong> | 핵심 구조 정의 | 객체의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), 타입, 제약조건 저장 (읽기 전용 뷰 제공) | 테이블명, 컬럼, 뷰 정의 | 설계 도면 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/013_data_directory/">Data Directory</a></strong> | 물리 위치 매핑 | [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/)의 정보를 물리적 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조와 연결 | OS [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포인터 | 창고 약도 |
| <strong>통계 정보 (<a href="/studynote/05_database/03_relational_model/168_clustering_factor_index_physical_alignment/">Statistics</a>)</strong> | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 지원 | [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 비용 기반(CBO) 계산을 위한 수치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 행 건수, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 깊이, 분포도 | 상품 재고표 |
| **Dictionary Cache** | [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 가속 | 디스크 기반의 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 메모리(SGA)에 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)하여 병목 해소 | 파싱 단계의 [LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 캐시 | 안내 데스크 메모 |

[DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/)([Data Definition Language](/studynote/05_database/01_db_architecture_relational/020_ddl/))이 실행될 때 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)가 갱신되는 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 흐름은 다음과 같습니다.
```text
1. [DBA의 명령] CREATE TABLE New_Emp (id INT, name VARCHAR);
        v
2. [DBMS 엔진 수신] 문법 검증 및 물리적 스토리지 블록 할당 수행
        v
3. [카탈로그 업데이트 (자동)]
   - SYSTABLES 에 'New_Emp' 레코드 1행 삽입
   - SYSCOLUMNS 에 'id', 'name' 레코드 2행 삽입
   - SYSAUTH 에 소유자 권한 부여 이력 삽입
        v
4. [캐시 동기화] 메모리의 Dictionary Cache 무효화(Invalidation) 및 최신화
        v
5. [완료] 이후부터 일반 사용자가 New_Emp 테이블 SELECT 가능
```
이 흐름의 핵심은 사용자가 직접 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 갱신(INSERT/UPDATE)할 수 없다는 점입니다. 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 DBMS만이 [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/) 명령문을 해석하여 스스로 갱신합니다. 만약 일반 사용자가 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직접 수정할 수 있다면, 테이블의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 정의와 디스크의 물리적 형태가 어긋나 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 전체가 붕괴(Corruption)됩니다. 따라서 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 오직 `SELECT`만을 허용하는 [동적 성능 뷰](/studynote/05_database/04_transactions_concurrency/582_dynamic_performance_views_v_dollar_dmv_monitoring/)(예: Oracle의 `USER_`, `ALL_`, `DBA_` 뷰) 형태로만 접근이 개방됩니다.

📢 **섹션 요약 비유**: 뇌([DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/))가 자신의 몸([데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/))의 상태를 기억하는 '자아 인식 스토리지'입니다. 몸무게가 늘면 뇌의 인식이 자동으로 갱신될 뿐, 손으로 뇌세포를 직접 찔러 정보를 조작할 수는 없습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 관리하는 두 축인 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)와 일반 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 그리고 [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/)과 [데이터 디렉터리](/studynote/05_database/01_db_architecture_relational/013_data_directory/)를 비교합니다.

| 항목 | 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) ([데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/)) | [데이터 디렉터리](/studynote/05_database/01_db_architecture_relational/013_data_directory/) ([Data Directory](/studynote/05_database/01_db_architecture_relational/013_data_directory/)) | 판단 및 접근 권한 |
|:---|:---|:---|:---|
| **저장 내용** | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 명세, 제약조건, 통계, 권한 등 <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 저장된 물리적 블록과 실린더 포인터 등 **물리적 제어 정보** | <strong><a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a> 수준 차이</strong> |
| **접근 주체** | [DBA](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) 및 일반 사용자 (시스템 제공 뷰를 통해 [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 가능) | 오직 시스템([DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 내부 엔진)만이 접근 가능 | <strong><a href="/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/">접근 통제</a> 경계</strong> |
| **목적** | 파싱, 구문 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 최적화 계획 수립 보조 | 실행 엔진이 실제 디스크 I/O를 수행하기 위한 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | **사용되는 실행 단계** |
| **변경 시점** | [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/) (CREATE, ALTER) 실행 시 및 통계 수집(Analyze) 시 | 디스크 할당 갱신 및 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 조각화 변경 시 | <strong><a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a> 시점</strong> |

이 매트릭스는 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)조차 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 영역(사전)과 물리적 영역([디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))으로 나뉜다는 것을 보여줍니다. DBA는 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 뷰를 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)하여 테이블 통계가 낡았는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있지만, [데이터 디렉터리](/studynote/05_database/01_db_architecture_relational/013_data_directory/)에 직접 접근해 포인터를 조작할 수는 없습니다. 이 철저한 캡슐화가 DBMS의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 지키는 방어 기제입니다.

📢 **섹션 요약 비유**: 도서 검색용 컴퓨터([데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/))는 누구나 검색할 수 있지만, 사서만 볼 수 있는 도서관 지하 서고의 비밀 열쇠 보관함([데이터 디렉터리](/studynote/05_database/01_db_architecture_relational/013_data_directory/))은 철저히 접근이 차단된 것과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 관리 상태는 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(옵티마이징)과 직결되는 가장 중요한 DBA의 관리 대상입니다.

1. **통계 정보 갱신(Analyze/Gather Stats) 시나리오**: 대량의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 작업(Bulk Insert)이 일어난 후, [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 통계 정보(행 건수, 분포도 등)가 갱신되지 않으면 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 과거의 작은 테이블로 착각하여 풀 스캔 계획을 세웁니다. 실무에서는 야간에 주기적으로 [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 통계 수집 잡(Job)을 돌려 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 최신화해야 악성 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(Bad Plan)를 막을 수 있습니다.
2. <strong>딕셔너리 캐시 경합 (Row Cache <a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)</strong>: 트래픽이 폭주하는 피크 시간에 [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/)(테이블 변경 등)을 수행하면 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)가 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))에 걸립니다. 이 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 읽어야만 일반 [DML](/studynote/12_it_management/02_itsm_itil/867_dml/)([SELECT](/studynote/05_database/04_transactions_concurrency/520_select/))도 파싱할 수 있으므로, [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 락은 순식간에 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체의 행(Hang) 장애로 전파됩니다.
3. <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (의미 없는 동의어 반복)</strong>: [데이터 표준화](/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/) 없이 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)에 무의미한 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(수천 개의 테스트 뷰, [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))를 방치하면, 딕셔너리 캐시를 소진시켜 시스템 파싱 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 심각하게 저하됩니다.

아래 트리는 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 파싱할 때 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 어떻게 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는지 보여주는 의사결정 흐름입니다.
```text
[쿼리 요청] SELECT * FROM Users WHERE age > 20;
   v
[1. 카탈로그 검증] (Dictionary Cache 스캔)
   +-> Users 테이블 존재? (O) / 권한 있음? (O)
   v
[2. 카탈로그 통계 확보]
   +-> age 인덱스 존재 여부 파악
   +-> 테이블 총 레코드 수 및 age > 20의 분포도(Selectivity) 추출
   v
[3. 실행 계획 산출]
   +-> 분포도가 10% 미만 --> 인덱스 스캔 플랜 채택
   +-> 분포도가 50% 이상 --> 테이블 풀 스캔 플랜 채택
```
이 흐름의 핵심은 [비용 기반 옵티마이저](/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/)(CBO)의 지능은 전적으로 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 통계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정확도에 의존한다는 점입니다. [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 통계가 거짓말을 하면 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 최악의 결정을 내립니다. "Garbage In, Garbage Out"의 원칙이 여기에도 적용됩니다.

📢 **섹션 요약 비유**: 내비게이션([옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/))이 아무리 똑똑해도 지도 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)(시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/))에 새로 생긴 고속도로가 업데이트되어 있지 않으면, 구불구불한 국도로만 길을 안내하는 것과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
안정적인 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 운영은 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화의 토대이자 전사 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)의 시작점입니다.

| 정량적 효과 | 정성적 효과 |
|:---|:---|
| 캐시 힛(Cache [Hit](/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/)) 최적화를 통한 하드 파싱 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 90% 이상 [억제](/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 객체와 구조에 대한 완벽한 자가 추적 및 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 확보 |
| 정확한 통계 기반 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)으로 CPU/디스크 자원 낭비 최소화 | [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)([Data Governance](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)) 구축을 위한 원천 정보 제공 |

미래의 아키텍처, 특히 [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)([Data Lakehouse](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/))와 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)) 환경에서는 단일 DBMS의 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 넘어, 전사적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산을 횡단으로 검색하고 관리하는 '글로벌 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)(예: AWS Glue, Allan, Amundsen)' 플랫폼으로 진화하고 있습니다. 이는 닫힌 시스템 안의 [데이터 사전](/studynote/05_database/07_exam_summary/393_data_dictionary/)을 열린 [지식 그래프](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)망으로 확장시키는 거대한 흐름입니다.

📢 **섹션 요약 비유**: 단일 부서의 연락망(시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/))을 넘어서, 글로벌 기업 전체의 모든 직원과 업무를 검색할 수 있는 거대한 전사 포털 인트라넷([데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 플랫폼)으로 진화하고 있습니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) ([Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/)) (시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)가 저장하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 본질)
* [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) ([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/)) ([카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 통계 정보를 먹고 자라며 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 세우는 핵심 엔진)
* [데이터 독립성](/studynote/05_database/01_db_architecture_relational/004_data_independence/) ([카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 통한 매핑 계층화로 보장되는 아키텍처 특성)
* 하드 파싱 (Hard Parsing) ([카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 조회하여 구문 분석과 계획을 새로 수립하는 고비용 작업)
* [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) (전사적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 통제를 위해 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 활용하는 관리 체계)

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 정의 (DDL 실행) — 테이블·인덱스·뷰 생성]
    |
    v
[시스템 카탈로그 갱신 (System Catalog Update) — 메타데이터 자동 등록]
    |
    v
[쿼리 파싱 (Hard Parsing) — 카탈로그 조회로 객체·권한 검증]
    |
    v
[옵티마이저 (Optimizer) — 통계 정보 기반 최적 실행 계획 수립]
    |
    v
[데이터 거버넌스 (Data Governance) — 카탈로그 메타데이터로 전사 자산 통제]
```

이 흐름은 [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/) 실행 시점부터 시작해 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)와 거버넌스까지 이어지는 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 역할 연쇄를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. 서점에 수많은 책이 있을 때, 책 제목과 작가, 꽂혀 있는 위치를 전부 적어둔 '도서 검색기'가 바로 시스템 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)예요.
2. 우리가 컴퓨터([데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/))에게 "사과에 대한 책 찾아줘"라고 하면, 컴퓨터는 제일 먼저 이 검색기를 보고 책이 1층에 있는지 2층에 있는지 찾아낸답니다.
3. 이 검색기가 없다면 컴퓨터는 서점의 모든 책을 1페이지부터 끝까지 전부 다 넘겨봐야 해서 시간이 엄청 오래 걸릴 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 11 / 600

<- **이전**: [10. 스키마 매핑 (Mapping) - 외부/개념 사상, 개념/내부 사상](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)
**다음**: [12. 메타데이터 (Metadata) - 데이터에 대한 데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) ->

---
