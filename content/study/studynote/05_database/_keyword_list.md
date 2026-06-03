---
title: 05. 데이터베이스 키워드 목록
date: '2026-03-04'
tags:
- studynote-database
---
[[267_weight_bias_activation|weight]] = 9999

# [[002_database_definition|데이터베이스]] ([[501_database|Database]]) 키워드 목록 (심화 확장판)

정보관리기술사·컴퓨터응용시스템기술사 및 전문 DB/[[001_dikw_pyramid|데이터]] 엔지니어를 위한 [[002_database_definition|데이터베이스]] 전 영역 핵심 및 심화 키워드 800선입니다.

[[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]](RDB) 기초부터 [[093_normalization|정규화]], [[014_concurrency|동시성]] 제어, [[191_transaction_concept_states|트랜잭션]] 관리, [[136_variance|분산]] DB, [[035_nosql|NoSQL]], [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]], [[209_data_warehouse_schema_on_write|데이터 웨어하우스]], 그리고 최근의 [[223_vector_database_embedding|벡터 데이터베이스]]([[151_vector_database_embedding_ann_search|Vector DB]])와 [[531_cloud_native_architecture|클라우드 네이티브]] [[002_database_definition|데이터베이스]] 기술까지 완벽하게 포괄합니다.

---

## 1. [[002_database_definition|데이터베이스]] 기초 및 아키텍처 (60개)
1. [[001_dikw_pyramid|데이터]] ([[001_dikw_pyramid|Data]]) / 정보 (Information) / 지식 (Knowledge) / 지혜 (Wisdom) - DIKW 피라미드
2. [[002_database_definition|데이터베이스]] ([[501_database|Database]])의 정의 - 통합(Integrated), 저장(Stored), 운영(Operational), 공용(Shared) [[001_dikw_pyramid|데이터]]
3. [[003_dbms_database_management_system|데이터베이스 관리 시스템]] ([[502_dbms|DBMS]]) - 사용자와 DB 사이의 인터페이스 ([[004_data_independence|데이터 독립성]] 제공)
4. [[004_data_independence|데이터 독립성]] ([[504_data_independence|Data Independence]]) - [[369_logic_bomb|논리]]적 독립성 vs 물리적 독립성
5. [[005_schema|스키마]] ([[505_schema|Schema]]) - [[002_database_definition|데이터베이스]]의 [[369_logic_bomb|논리]]적 구조와 제약 조건에 대한 명세
6. [[006_three_level_schema_architecture|3단계 스키마 아키텍처]] (ANSI/SPARC)
7. [[007_external_schema|외부 스키마]] ([[007_external_schema|External Schema]]) - 사용자 관점, 서브 [[005_schema|스키마]]
8. [[008_conceptual_schema|개념 스키마]] ([[008_conceptual_schema|Conceptual Schema]]) - 조직 전체 관점, [[369_logic_bomb|논리]]적 구조
9. [[009_internal_schema|내부 스키마]] ([[009_internal_schema|Internal Schema]]) - 물리적 저장 장치 관점
[[489_raid_10_hybrid|10]]. [[010_schema_mapping|스키마 매핑]] ([[010_schema_mapping|Mapping]]) - 외부/개념 사상, 개념/내부 사상
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_system_catalog|시스템 카탈로그]] ([[011_system_catalog|System Catalog]]) / [[393_data_dictionary|데이터 사전]] ([[509_data_dictionary|Data Dictionary]]) - [[012_metadata|메타데이터]]([[012_metadata|Metadata]]) 저장소
12. [[012_metadata|메타데이터]] ([[012_metadata|Metadata]]) - [[001_dikw_pyramid|데이터]]에 대한 [[001_dikw_pyramid|데이터]]
13. [[013_data_directory|데이터 디렉터리]] ([[013_data_directory|Data Directory]]) - 시스템만 접근 가능한 [[394_catalog_metadata|카탈로그]] 부분
14. [[014_data_model_components|데이터 모델]] ([[014_data_model_components|Data Model]]) 구성 요소 - 구조(Structure), 연산([[329_delta_encoding|Operation]]), 제약조건(Constraint)
15. [[015_hierarchical_data_model|계층형 데이터 모델]] ([[015_hierarchical_data_model|Hierarchical Model]]) - 트리 구조 (1:N)
16. [[016_network_data_model|망형 데이터 모델]] ([[016_network_data_model|Network Model]]) - [[070_graph_datastructure|그래프]] 구조 (N:M 허용)
17. [[017_relational_data_model|관계형 데이터 모델]] ([[017_relational_data_model|Relational Model]]) - 테이블 구조, E.F. Codd 제안
18. [[018_object_oriented_relational_data_model|객체지향 데이터 모델]] ([[018_object_oriented_relational_data_model|OODBMS]]) / 객체 [[017_relational_data_model|관계형 데이터 모델]] (ORDBMS)
19. [[502_dbms|DBMS]] 언어
20. [[020_ddl|DDL]] ([[020_ddl|Data Definition Language]]) - [[001_dikw_pyramid|데이터]] 정의 언어 (CREATE, ALTER, DROP, TRUNCATE)
21. [[083_dml|DML]] ([[021_dml|Data Manipulation Language]]) - [[001_dikw_pyramid|데이터]] 조작 언어 ([[520_select|SELECT]], INSERT, UPDATE, DELETE)
22. [[022_dcl|DCL]] ([[022_dcl|Data Control Language]]) - [[001_dikw_pyramid|데이터]] 제어 언어 (GRANT, REVOKE)
23. [[023_tcl|TCL]] ([[023_tcl|Transaction Control Language]]) - [[191_transaction_concept_states|트랜잭션]] 제어 (COMMIT, [[313_rollback|ROLLBACK]], [[200_savepoint_partial_rollback|SAVEPOINT]])
24. 절차적 [[083_dml|DML]] (네비게이션) vs 비절차적 [[083_dml|DML]] (선언적, SQL)
25. [[002_database_definition|데이터베이스]] 관리자 ([[025_dba_database_administrator|DBA]], [[025_dba_database_administrator|Database Administrator]])
26. [[001_dikw_pyramid|데이터]] 관리자 ([[104_da_as_is_analysis|DA]], [[026_da_data_administrator|Data Administrator]]) - [[001_dikw_pyramid|데이터]] 표준, [[203_metadata_management|메타데이터 관리]]
27. [[027_database_designer|데이터베이스 설계자]] ([[027_database_designer|Database Designer]])
28. [[002_database_definition|데이터베이스]] 사용자 - 일반 사용자, 응용 프로그래머
29. [[002_database_definition|데이터베이스]] [[501_file_definition_logical_record|파일]] 시스템 ([[501_file_definition_logical_record|File]] System) 문제점 - [[001_dikw_pyramid|데이터]] [[008_dependencies|종속성]], [[001_dikw_pyramid|데이터]] 중복성
30. [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] ([[003_integrity|Integrity]]) / [[283_security_tactics|보안성]] ([[283_security_tactics|Security]])
31. 클라이언트-서버 [[502_dbms|DBMS]] 아키텍처 (2-Tier, 3-Tier)
32. TP [[229_monitor|모니터]] ([[032_tp_monitor|Transaction Processing Monitor]]) / 미들웨어
33. [[033_file_storage_structure|파일 저장 구조]] - 히프([[078_heap_datastructure|Heap]]), 순차(Sequential), 해시(Hash), [[154_database_index_b_tree_search_optimization|인덱스]]([[181_indexed_addressing|Indexed]]) [[501_file_definition_logical_record|파일]]
34. 고정 길이 레코드 vs 가변 길이 레코드
35. [[035_blocking_factor|블로킹 팩터]] ([[035_blocking_factor|Blocking Factor]]) - 하나의 블록에 저장되는 레코드 수
36. [[064_b_tree|B-Tree]] (다진 탐색 트리) 원리 및 구조
37. B+Tree - 리프 노드에만 [[001_dikw_pyramid|데이터]] 저장, 리프 노드 간 [[056_linked_list|연결 리스트]] (RDB [[154_database_index_b_tree_search_optimization|인덱스]] 기본)
38. [[038_relational_algebra|관계 대수]] ([[038_relational_algebra|Relational Algebra]]) - 절차적 언어, "어떻게" 구할 것인가 명시
39. [[039_general_set_operators|일반 집합 연산]]자 - 합집합(Union), 교집합(Intersection), 차집합(Difference), [[412_cartesian_product|카티션 프로덕트]]([[412_cartesian_product|Cartesian Product]])
40. [[040_pure_relational_operators|순수 관계 연산자]] - 셀렉트([[520_select|Select]], σ), 프로젝트([[042_relational_algebra_project|Project]], π), 조인([[521_join|Join]], ⋈), [[411_division_operation|디비전]]([[411_division_operation|Division]], ÷)
41. 셀렉트([[520_select|Select]]) - 수평적 부분집합 (행 추출)
42. 프로젝트([[042_relational_algebra_project|Project]]) - 수직적 부분집합 (열 추출)
43. 조인([[521_join|Join]]) - 공통 [[082_attribute_types_er_model|속성]] 기준으로 두 [[061_relation_schema_instance|릴레이션]] 결합
44. [[411_division_operation|디비전]]([[411_division_operation|Division]]) - [[082_attribute_types_er_model|속성]] 값을 모두 가진 [[063_relation_tuple_cardinality|튜플]] 추출
45. [[410_relational_calculus|관계 해석]] ([[045_relational_calculus|Relational Calculus]]) - 비절차적 언어, "무엇을" 구할 것인가 명시 ([[063_relation_tuple_cardinality|튜플]] [[410_relational_calculus|관계 해석]], [[064_relation_domain|도메인]] [[410_relational_calculus|관계 해석]])
46. 인-메모리 [[002_database_definition|데이터베이스]] (IMDB, [[139_inmemory_db|In-Memory DB]]) - [[542_redis|Redis]], Memcached, SAP HANA (디스크 I/O 병목 제거)
47. 컬럼 기반 저장소 (Columnar Store) - 분석([[316_olap|OLAP]]) 최적화, 높은 [[347_compaction|압축]]률
48. 로우 기반 저장소 (Row Store) - [[191_transaction_concept_states|트랜잭션]]([[327_hint_handoff|OLTP]]) 최적화
49. 스토리지 엔진 (Storage Engine) 구조 (InnoDB, MyISAM 등)
50. 버퍼 풀 (Buffer Pool) / 버퍼 관리자 - 디스크 접근 최소화 
51. [[051_logging_engine_wal_redo_undo|로깅 엔진]] ([[051_logging_engine_wal_redo_undo|Logging Engine]]) - [[658_ir_recovery|복구]]([[658_ir_recovery|Recovery]])를 위한 [[568_logs_distributed_logging_elk_fluentd|로그]](WAL) 작성
52. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]]) - 최적의 SQL [[166_execution_plan_optimizer_navigation_tree|실행 계획]] [[087_process_state_transition|생성]]
53. 파서 (Parser) - SQL 구문 분석 및 파스 트리 [[087_process_state_transition|생성]]
54. [[394_catalog_metadata|카탈로그]] 매니저 - [[012_metadata|메타데이터]] 접근
55. 커넥션 풀 (Connection Pool) - [[002_database_definition|데이터베이스]] 연결 오버헤드 감소
56. [[001_dikw_pyramid|데이터]] 딕셔너리 캐시 ([[056_data_dictionary_cache|Data Dictionary Cache]])
57. [[057_shared_pool_oracle_sga|공유 풀]] ([[057_shared_pool_oracle_sga|Shared Pool]]) - [[188_pl_sql_t_sql_procedural|Oracle]] 인스턴스 구조
58. [[058_database_instance_architecture|데이터베이스 인스턴스]] ([[058_database_instance_architecture|Database Instance]]) - 메모리 구조 + 백그라운드 프로세스
59. [[059_persistent_storage_data_log_control_file|영구 저장소]] ([[059_persistent_storage_data_log_control_file|Persistent Storage]]) - [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]], [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]], 제어 [[501_file_definition_logical_record|파일]]
60. [[060_serverless_database_aurora|서버리스 데이터베이스]] ([[060_serverless_database_aurora|Serverless DB]]) - Amazon [[390_aurora_serverless_quorum_write|Aurora]] [[206_serverless_cold_start|Serverless]] 등 자동 확장 아키텍처

## 2. [[017_relational_data_model|관계형 데이터 모델]] 및 [[093_normalization|정규화]] (70개)
61. [[061_relation_schema_instance|릴레이션]] ([[061_relation_schema_instance|Relation]]) - [[001_dikw_pyramid|데이터]]를 2차원 표로 표현한 구조
62. [[082_attribute_types_er_model|속성]] ([[082_attribute_types_er_model|Attribute]] / Column / Degree) - [[061_relation_schema_instance|릴레이션]]의 열 (차수)
63. [[063_relation_tuple_cardinality|튜플]] (Tuple / Row / Cardinality) - [[061_relation_schema_instance|릴레이션]]의 행 (카디널리티)
64. [[064_relation_domain|도메인]] ([[064_relation_domain|Domain]]) - [[082_attribute_types_er_model|속성]]이 가질 수 있는 원자값(Atomic Value)들의 집합
65. [[061_relation_schema_instance|릴레이션]]의 특징 - [[063_relation_tuple_cardinality|튜플]]의 무순서, [[082_attribute_types_er_model|속성]]의 무순서, [[063_relation_tuple_cardinality|튜플]]의 유일성, [[082_attribute_types_er_model|속성]]의 [[193_atomicity_all_or_nothing|원자성]]
66. NULL 값 - 아직 알려지지 않거나 해당 없는 값 ([[066_null_value_three_valued_logic|0이나 공백과 다름]])
67. 키 ([[067_db_key_uniqueness_minimality|Key]])의 개념 - 유일성(Uniqueness), 최소성(Minimality)
68. [[068_super_key_uniqueness|슈퍼 키]] ([[068_super_key_uniqueness|Super Key]]) - 유일성은 만족하나 최소성은 만족하지 않는 [[082_attribute_types_er_model|속성]] 집합
69. [[069_candidate_key_uniqueness_minimality|후보 키]] ([[069_candidate_key_uniqueness_minimality|Candidate Key]]) - 유일성과 최소성을 모두 만족하는 키
70. [[070_primary_key_alternate_key|기본 키]] (Primary [[067_db_key_uniqueness_minimality|Key]], PK) - [[069_candidate_key_uniqueness_minimality|후보 키]] 중 설계자가 선택한 메인 [[289_identification_flags_fragmentation_offset|식별자]] (NULL 불가)
71. [[071_alternate_key|대체 키]] ([[071_alternate_key|Alternate Key]]) - [[069_candidate_key_uniqueness_minimality|후보 키]] 중 [[070_primary_key_alternate_key|기본 키]]로 선택되지 않은 나머지 키
72. [[072_foreign_key_fk|외래 키]] (Foreign [[067_db_key_uniqueness_minimality|Key]], FK) - 다른 [[061_relation_schema_instance|릴레이션]]의 [[070_primary_key_alternate_key|기본 키]]를 [[316_reference_pattern_nosql|참조]]하는 [[082_attribute_types_er_model|속성]]
73. [[073_integrity_constraints_overview|무결성 제약조건]] ([[073_integrity_constraints_overview|Integrity Constraints]])
74. [[074_entity_integrity_primary_key|개체 무결성]] ([[074_entity_integrity_primary_key|Entity Integrity]]) - [[070_primary_key_alternate_key|기본 키]]는 NULL이나 중복값을 가질 수 없음
75. [[075_referential_integrity_foreign_key_cascade|참조 무결성]] ([[075_referential_integrity_foreign_key_cascade|Referential Integrity]]) - [[072_foreign_key_fk|외래 키]] 값은 [[316_reference_pattern_nosql|참조]]하는 [[061_relation_schema_instance|릴레이션]]의 기본키 값이거나 NULL이어야 함
76. [[076_domain_integrity|도메인 무결성]] ([[076_domain_integrity|Domain Integrity]]) - [[082_attribute_types_er_model|속성]] 값은 정의된 [[064_relation_domain|도메인]]에 속해야 함
77. [[077_user_defined_integrity_check_trigger|사용자 정의 무결성]] ([[077_user_defined_integrity_check_trigger|User-defined Integrity]]) - 업무 규칙에 따른 제약 (CHECK 제약조건 등)
78. [[078_key_integrity|키 무결성]] ([[078_key_integrity|Key Integrity]])
79. NULL [[003_integrity|무결성]] (Null [[003_integrity|Integrity]])
80. ER 모델 (Entity-[[083_relationship_in_er_model|Relationship]] Model) - 피터 첸(Peter Chen) 제안, 개념적 모델링
81. 개체 (Entity) - 사각형, 관리 대상
82. [[082_attribute_types_er_model|속성]] ([[082_attribute_types_er_model|Attribute]]) - 타원, 개체의 특성
83. [[083_relationship_in_er_model|관계]] ([[083_relationship_in_er_model|Relationship]]) - 마름모, 개체 간 연관성
84. [[084_cardinality_ratio_1_to_n|카디널리티 비율]] ([[084_cardinality_ratio_1_to_n|Cardinality Ratio]]) - 1:1, 1:N, M:N
85. [[085_participation_constraint_total_partial|참여 제약조건]] ([[085_participation_constraint_total_partial|Participation Constraint]]) - 필수 참여(전체), 선택 참여(부분)
86. [[086_weak_entity_identifying_relationship|약한 개체]] ([[086_weak_entity_identifying_relationship|Weak Entity]]) - 이중 사각형, 부모 개체에 종속 ([[087_identifying_vs_non_identifying_relationship|식별 관계]])
87. [[087_identifying_vs_non_identifying_relationship|식별 관계]] ([[087_identifying_vs_non_identifying_relationship|Identifying]]) vs 비식별 [[083_relationship_in_er_model|관계]] (Non-[[087_identifying_vs_non_identifying_relationship|identifying]])
88. [[289_identification_flags_fragmentation_offset|식별자]] ([[088_identifier_in_er_model|Identifier]]) - ER 모델에서의 키
89. 확장 ER 모델 ([[089_eer_enhanced_er_model_specialization|EER]]) - 서브클래스, 슈퍼클래스, [[234_uml_class_relationships_generalization_dependency|상속]](일반화/특수화) 개념 추가
90. [[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]]) - [[093_normalization|정규화]]를 거치지 않아 발생하는 [[001_dikw_pyramid|데이터]] 중복에 따른 부작용
91. [[091_functional_dependency_fd|삽입 이상]] ([[091_functional_dependency_fd|Insertion Anomaly]]) - 불필요한 [[001_dikw_pyramid|데이터]]까지 함께 삽입해야 하는 현상
92. [[092_deletion_anomaly|삭제 이상]] ([[092_deletion_anomaly|Deletion Anomaly]]) - 연쇄 삭제로 인해 필요한 [[001_dikw_pyramid|데이터]]까지 소실되는 현상
93. [[093_update_anomaly|갱신 이상]] ([[093_update_anomaly|Update Anomaly]]) - 중복 [[001_dikw_pyramid|데이터]] 중 일부만 갱신되어 [[001_dikw_pyramid|데이터]] 불일치 발생
94. [[094_functional_dependency_fd|함수적 종속성]] (Functional Dependency, FD) - X의 값이 Y의 값을 유일하게 결정할 때 (X -> Y)
95. [[095_determinant_dependent|결정자]] ([[095_determinant_dependent|Determinant]]) X / 종속자 (Dependent) Y
96. [[096_full_functional_dependency|완전 함수적 종속]] ([[096_full_functional_dependency|Full Functional Dependency]])
97. [[097_partial_functional_dependency|부분 함수적 종속]] ([[097_partial_functional_dependency|Partial Functional Dependency]]) - 복합키의 일부 [[082_attribute_types_er_model|속성]]에만 종속
98. [[098_transitive_functional_dependency|이행적 함수적 종속]] ([[098_transitive_functional_dependency|Transitive Functional Dependency]]) - X->Y, Y->Z 일 때 X->Z 종속 발생
99. 암스트롱의 공리 (Armstrong's Axioms) - 반사의 공리, 첨가의 공리, 이행의 공리
100. [[093_normalization|정규화]] ([[093_normalization|Normalization]]) - [[090_anomaly_insertion_deletion_update|이상 현상]] 방지를 위해 [[061_relation_schema_instance|릴레이션]]을 분해(Decomposition)하는 과정
101. [[101_lossless_join_decomposition|무손실 분해]] ([[101_lossless_join_decomposition|Lossless-Join Decomposition]]) - 조인 시 원래 [[061_relation_schema_instance|릴레이션]]이 복원됨 보장
102. [[102_dependency_preservation_decomposition|종속성 보존]] ([[102_dependency_preservation_decomposition|Dependency Preservation]]) - 분해 후에도 FD가 유지됨
103. [[103_first_normal_form_1nf_atomic_value|제1정규형]] ([[103_first_normal_form_1nf_atomic_value|1NF]]) - [[064_relation_domain|도메인]]이 원자값만으로 구성
104. [[104_second_normal_form_2nf_full_fd|제2정규형]] ([[104_second_normal_form_2nf_full_fd|2NF]]) - [[103_first_normal_form_1nf_atomic_value|1NF]] 만족 및 부분 함수 종속 제거 (완전 함수 종속화)
105. [[105_third_normal_form_3nf_transitive|제3정규형]] ([[105_third_normal_form_3nf_transitive|3NF]]) - [[104_second_normal_form_2nf_full_fd|2NF]] 만족 및 이행적 함수 종속 제거
106. [[529_bcnf|BCNF]] ([[106_bcnf_boyce_codd_normal_form|Boyce-Codd Normal Form]]) - [[105_third_normal_form_3nf_transitive|3NF]] 만족 및 모든 [[095_determinant_dependent|결정자]]가 후보키 (강한 [[105_third_normal_form_3nf_transitive|3NF]])
107. [[107_multi_valued_dependency_mvd_4nf|다치 종속성]] ([[400_mvd_4nf|MVD]], Multi-Valued Dependency) - X->>Y
108. [[108_fourth_normal_form_4nf|제4정규형]] ([[108_fourth_normal_form_4nf|4NF]]) - [[529_bcnf|BCNF]] 만족 및 [[400_mvd_4nf|다치 종속]] 제거
109. [[109_join_dependency_jd|조인 종속성]] ([[521_join|Join]] Dependency)
110. [[110_fifth_normal_form_5nf_pjnf|제5정규형]] (5NF / PJNF) - [[108_fourth_normal_form_4nf|4NF]] 만족 및 조인 종속 제거
111. [[093_normalization|정규화]]의 역설 / [[282_performance_tactics|성능]] 저하 - 과도한 분해 시 조인([[521_join|Join]]) 오버헤드 증가
112. 반정규화 (De-[[093_normalization|normalization]] / 비정규화) - [[282_performance_tactics|성능]] 향상을 위해 [[093_normalization|정규화]] 원칙을 의도적으로 위배, 중복 허용
113. 반정규화 기법 - 테이블 병합(1:1, 1:M, 슈퍼/서브), 테이블 분할(수직, [[268_horizontal_fragmentation|수평 분할]]), 중복 칼럼 추가, 파생 컬럼/테이블 추가
114. [[114_database_design_phases|데이터베이스 설계 단계]] - 요구사항 분석 -> 개념적 설계 -> [[369_logic_bomb|논리]]적 설계 -> 물리적 설계
115. [[369_logic_bomb|논리]]적 설계 (Logical Design) - ERD를 [[391_relation_schema_intension|릴레이션 스키마]]로 변환, [[093_normalization|정규화]] 수행
116. 매핑 룰 ([[010_schema_mapping|Mapping]] Rule) - 개념적 모델(ERD)을 [[369_logic_bomb|논리]] 모델([[061_relation_schema_instance|릴레이션]])로 변환하는 규칙
117. 물리적 설계 (Physical Design) - [[154_database_index_b_tree_search_optimization|인덱스]], [[179_table_partitioning_concept|파티셔닝]], 클러스터링, 저장 구조 설계
118. [[118_dimensional_modeling_star_schema|차원 모델링]] ([[118_dimensional_modeling_star_schema|Dimensional Modeling]]) - [[316_olap|OLAP]], [[334_star_schema|스타 스키마]] ([[296_star_schema|Star Schema]]), [[335_snowflake_schema|스노우플레이크 스키마]] ([[313_snowflake_schema|Snowflake Schema]])
119. [[210_fact_dimension_table_snowflake_schema|팩트 테이블]] ([[210_fact_dimension_table_snowflake_schema|Fact Table]]) / [[273_dimension_table_analysis_perspective|차원 테이블]] ([[273_dimension_table_analysis_perspective|Dimension Table]])
120. [[001_dikw_pyramid|데이터]] 역엔지니어링 ([[120_data_reverse_engineering|Data Reverse Engineering]])
121. [[104_da_as_is_analysis|데이터 아키텍처]] ([[104_da_as_is_analysis|DA]], [[001_dikw_pyramid|Data]] [[319_architecture|Architecture]]) 프레임워크 ([[243_zachman_framework_matrix|Zachman]] 등)
122. [[051_mdm_master_data_management|마스터 데이터 관리]] ([[539_mdm_master_data_management|MDM]], Master [[001_dikw_pyramid|Data]] [[372_management|Management]])
123. 기준 정보 ([[316_reference_pattern_nosql|Reference]] [[001_dikw_pyramid|Data]])
124. [[052_data_governance_framework|데이터 거버넌스]] ([[052_data_governance_framework|Data Governance]])
125. [[125_metadata_management_system_mms|메타데이터 관리 시스템]] ([[125_metadata_management_system_mms|MMS]])
126. [[126_data_standardization_word_domain_term|데이터 표준화]] ([[001_dikw_pyramid|Data]] Standardization) - 단어 사전, [[064_relation_domain|도메인]], 표준 용어 정의
127. 정보 공학 방법론 (Information Engineering) - [[383_data_centric_architecture|데이터 중심]] 개발 (James Martin)
128. [[369_logic_bomb|논리]]적 [[004_data_independence|데이터 독립성]]과 뷰([[151_sql_view_virtual_table|View]])의 [[083_relationship_in_er_model|관계]]
129. ORM (Object-Relational [[010_schema_mapping|Mapping]]) 개념과 [[004_impedance|임피던스]] 불일치 ([[004_impedance|Impedance]] Mismatch)
130. ERD 표기법 - IE(Information Engineering, 까마귀발 표기법), Barker, IDEF1X

## 3. SQL 및 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (60개)
131. SQL (Structured Query Language) 국제 표준 (ANSI/ISO SQL)
132. 조인 연산의 종류 (SQL 기준)
133. 내부 조인 (Inner [[521_join|Join]]) - 교집합, 양쪽에 모두 존재하는 행만 추출
134. 동등 조인 (Equi [[521_join|Join]]) / [[413_natural_join|자연 조인]] ([[413_natural_join|Natural Join]]) - 중복 컬럼 제거
135. 비동등 조인 (Non-Equi [[521_join|Join]]) - BETWEEN, >, < 등 등호 이외 연산자 사용 조인
136. [[414_outer_join|외부 조인]] ([[414_outer_join|Outer Join]]) - 합집합 개념, 기준 테이블의 모든 행 추출 + 조인 실패 시 NULL 반환
137. Left [[414_outer_join|Outer Join]] / Right [[414_outer_join|Outer Join]] / Full [[414_outer_join|Outer Join]]
138. 교차 조인 (Cross [[521_join|Join]] / [[412_cartesian_product|Cartesian Product]]) - M x N 건 [[087_process_state_transition|생성]]
139. 셀프 조인 (Self [[521_join|Join]]) - 동일 테이블 간의 조인, 계층형 [[298_qkv_attention|쿼리]] 등에 활용
140. 서브쿼리 ([[523_subquery|Subquery]]) - [[298_qkv_attention|쿼리]] 내부에 포함된 또 다른 [[298_qkv_attention|쿼리]]
141. [[141_inline_view_subquery|인라인 뷰]] ([[141_inline_view_subquery|Inline View]]) - FROM 절에 사용된 서브쿼리, 동적으로 [[087_process_state_transition|생성]]되는 뷰
142. [[142_scalar_subquery|스칼라 서브쿼리]] ([[142_scalar_subquery|Scalar Subquery]]) - [[520_select|SELECT]] 절에 사용, 단일 행/단일 열 반환
143. 중첩 서브쿼리 (Nested [[523_subquery|Subquery]]) - WHERE 절에 사용 (IN, [[435_exists_boolean_fast_search|EXISTS]], ANY, ALL)
144. 연관 서브쿼리 ([[144_correlated_subquery_nested_loop|Correlated Subquery]]) - 메인 [[298_qkv_attention|쿼리]]의 컬럼을 포함하는 서브쿼리
145. 윈도우 함수 ([[139_window_function_analytics|Window Function]] / [[139_window_function_analytics|분석 함수]]) - 행 간의 [[083_relationship_in_er_model|관계]]를 분석 (RANK, DENSE_RANK, ROW_NUMBER, LEAD, LAG)
146. [[514_partition_slice_volume|파티션]] 바이 ([[436_window_function_over|PARTITION BY]]) / 오더 바이 (ORDER BY) - 윈도우 함수의 범위와 정렬
147. [[147_aggregate_function_group_by|집계 함수]] ([[147_aggregate_function_group_by|Aggregate Function]]) - SUM, AVG, MAX, MIN, COUNT
148. [[148_sql_group_by_having_clause|그룹 바이]] ([[522_group_by|GROUP BY]]) / 해빙 (HAVING) - HAVING은 [[535_grouping_counting_free_space|그룹화]] 결과에 대한 조건
149. [[042_rollup_l2_solution|ROLLUP]], CUBE, [[535_grouping_counting_free_space|GROUPING]] SETS - 다차원 소계 및 총계 [[087_process_state_transition|생성]] ([[316_olap|OLAP]])
150. 집합 연산자 - UNION (중복 제거 합집합), UNION ALL (중복 포함 합집합), INTERSECT, MINUS/EXCEPT
151. 뷰 ([[151_sql_view_virtual_table|View]]) - 가상 테이블, [[369_logic_bomb|논리]]적 [[004_data_independence|데이터 독립성]] 및 보안 제공
152. [[152_simple_view_vs_complex_view|단순 뷰]] ([[152_simple_view_vs_complex_view|Simple View]]) vs 복합 뷰 (Complex [[151_sql_view_virtual_table|View]])
153. [[153_materialized_view_mview_data_warehouse|구체화된 뷰]] (MVIEW, Materialized [[151_sql_view_virtual_table|View]]) - 물리적 공간에 실제 [[001_dikw_pyramid|데이터]] 저장, [[282_performance_tactics|성능]] 향상, [[212_synchronization_mechanisms|동기화]](Refresh) 필요
154. [[154_database_index_b_tree_search_optimization|인덱스]] ([[154_database_index_b_tree_search_optimization|Index]]) - 검색 속도 향상을 위한 자료구조, 별도의 저장 공간 차지
155. [[155_database_index_overhead_dml_performance_degradation|인덱스의 단점]] - [[083_dml|DML]](Insert, Update, Delete) 시 [[154_database_index_b_tree_search_optimization|인덱스]] 수정 오버헤드 발생
156. [[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]] / B+Tree [[154_database_index_b_tree_search_optimization|인덱스]]
157. [[157_hash_index_equal_search|해시 인덱스]] ([[157_hash_index_equal_search|Hash Index]]) - 동등(=) 검색에 빠름, 범위(Range) 검색 불가
158. [[158_bitmap_index_cardinality_dml|비트맵 인덱스]] ([[158_bitmap_index_cardinality_dml|Bitmap Index]]) - 분포도(Cardinality)가 나쁜(성별 등) 컬럼에 적합, [[083_dml|DML]] [[282_performance_tactics|성능]] 저하 큼
159. [[159_clustered_index_physical_sort|클러스터드 인덱스]] ([[159_clustered_index_physical_sort|Clustered Index]]) - 물리적 [[001_dikw_pyramid|데이터]] 정렬 기준, 테이블당 1개 (보통 PK)
160. [[160_non_clustered_index_secondary|넌클러스터드 인덱스]] (Non-[[159_clustered_index_physical_sort|Clustered Index]] / 보조 [[154_database_index_b_tree_search_optimization|인덱스]]) - 리프 노드가 실제 [[001_dikw_pyramid|데이터]] 포인터 보유, 여러 개 가능
161. [[161_composite_index_leading_column|결합 인덱스]] ([[161_composite_index_leading_column|Composite Index]]) - 2개 이상 컬럼으로 구성 (선행 컬럼 순서 중요)
162. [[162_fbi_function_based_index|함수 기반 인덱스]] (FBI, Function Based [[154_database_index_b_tree_search_optimization|Index]]) - 산술식이나 함수가 적용된 결과 기준 인덱싱
163. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]]) - SQL 실행 최적 경로([[166_execution_plan_optimizer_navigation_tree|Execution Plan]]) [[087_process_state_transition|생성]]기
164. [[164_rbo_rule_based_optimizer|규칙 기반 옵티마이저]] (RBO, Rule Based [[088_optimizer|Optimizer]]) - 정해진 우선순위 규칙에 따라 계획 수립 (구형)
165. [[165_cbo_cost_based_optimizer|비용 기반 옵티마이저]] (CBO, Cost Based [[088_optimizer|Optimizer]]) - 시스템 통계 정보 기반, 디스크 I/O 등 최소 비용 계산 (현대 RDBMS)
166. [[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]]) - [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 [[087_process_state_transition|생성]]한 네비게이션 트리
167. [[167_sql_hint_optimizer_override|힌트]] ([[167_sql_hint_optimizer_override|Hint]]) - 개발자가 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]에게 접근 경로를 명시적으로 지시 (/*+ [[154_database_index_b_tree_search_optimization|INDEX]]([[931_emp_shielding|EMP]] IDX_01) */ 등)
168. [[168_clustering_factor_index_physical_alignment|데이터 딕셔너리 통계 정보]] ([[168_clustering_factor_index_physical_alignment|Statistics]]) - 테이블 건수, 블록 수, [[154_database_index_b_tree_search_optimization|인덱스]] 높이, [[169_clustering_factor_index_physical_sort|클러스터링 팩터]] 등
169. [[169_clustering_factor_index_physical_sort|클러스터링 팩터]] ([[169_clustering_factor_index_physical_sort|Clustering Factor]]) - [[154_database_index_b_tree_search_optimization|인덱스]] 정렬 순서와 실제 물리적 [[001_dikw_pyramid|데이터]] 정렬 순서의 일치 정도
170. [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]]) / [[077_radix|기수]]성 (Cardinality) / 분포도 (Distribution)
171. [[171_optimizer_join_methods|옵티마이저 조인 기법 3가지]]
172. [[172_nl_join_nested_loop|중첩 루프 조인]] (NL [[521_join|Join]], [[431_nested_loop_join|Nested Loop Join]]) - 선행(Driving) 테이블 행마다 후행(Driven) 테이블 [[154_database_index_b_tree_search_optimization|인덱스]] 탐색, 소량 [[001_dikw_pyramid|데이터]]/온라인([[327_hint_handoff|OLTP]]) 적합
173. [[173_sort_merge_join|소트 머지 조인]] ([[173_sort_merge_join|Sort Merge Join]]) - 양쪽 테이블 [[432_sort_merge_join|정렬 후 병합]], [[154_database_index_b_tree_search_optimization|인덱스]] 없을 때나 대량 [[001_dikw_pyramid|데이터]] 조인 시 (동등/비동등 모두 가능)
174. [[174_hash_join|해시 조인]] ([[174_hash_join|Hash Join]]) - 작은 테이블로 해시 맵 [[087_process_state_transition|생성]] 후 큰 테이블 탐색, 대량 [[001_dikw_pyramid|데이터]]/동등(=) 조인 전용, [[484_elt_extract_load_transform|성능 우수]]
175. [[175_driving_vs_driven_table|드라이빙 테이블]] (Driving Table / Outer Table) vs 드리븐 테이블 (Driven Table / Inner Table)
176. [[176_join_order_optimization|조인 순서]] ([[176_join_order_optimization|Join Order]]) 최적화 - 동적 계획법([[007_dynamic_programming|Dynamic Programming]]), [[006_greedy_algorithm|탐욕 알고리즘]]
177. [[177_view_merging_query_transformation|뷰 머징]] ([[177_view_merging_query_transformation|View Merging]]) - [[163_optimizer_sql_execution_plan_generator|옵티마이저]]의 [[298_qkv_attention|쿼리]] 변환 ([[141_inline_view_subquery|인라인 뷰]]를 메인 [[298_qkv_attention|쿼리]]에 병합)
178. [[178_condition_pushdown|조건 푸시 다운]] ([[178_condition_pushdown|Condition Pushdown]]) - WHERE 조건을 뷰 내부로 밀어 넣어 [[001_dikw_pyramid|데이터]] 필터링 조기화
179. [[179_table_partitioning_concept|파티셔닝]] ([[179_table_partitioning_concept|Partitioning]]) - 대용량 테이블 물리적 분할 관리 기법
180. [[180_range_partitioning|레인지 파티셔닝]] ([[180_range_partitioning|Range Partitioning]]) - 범위(날짜 등) 기준
181. [[181_hash_partitioning|해시 파티셔닝]] ([[181_hash_partitioning|Hash Partitioning]]) - [[667_hash_function_integrity_one_way|해시 함수]] 결과, 균등 [[136_variance|분산]]용
182. [[182_list_partitioning|리스트 파티셔닝]] ([[182_list_partitioning|List Partitioning]]) - 명시적 특정 값(지역명 등) 기준
183. [[183_composite_partitioning|컴포지트 파티셔닝]] ([[183_composite_partitioning|Composite Partitioning]]) - 복합 (Range + Hash 등)
184. [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]]) - SQL 조건에 맞는 [[514_partition_slice_volume|파티션]]만 스캔 ([[163_optimizer_sql_execution_plan_generator|옵티마이저]] 최적화)
185. [[185_global_vs_local_index|전역 인덱스]] ([[185_global_vs_local_index|Global Index]]) vs 지역 [[154_database_index_b_tree_search_optimization|인덱스]] (Local [[154_database_index_b_tree_search_optimization|Index]], [[514_partition_slice_volume|파티션]]별 독립 [[154_database_index_b_tree_search_optimization|인덱스]])
186. [[186_stored_procedure_trigger|스토어드 프로시저]] ([[186_stored_procedure_trigger|Stored Procedure]]) / [[507_acid_properties|트리거]] (Trigger) - DB 서버 내에 컴파일되어 저장된 [[192_module_independence|모듈]]
187. [[187_user_defined_function_udf|사용자 정의 함수]] (UDF, User Defined Function)
188. PL/SQL ([[188_pl_sql_t_sql_procedural|Oracle]]), T-SQL (SQL Server) - 절차적 SQL 언어
189. 동적 SQL ([[189_dynamic_sql|Dynamic SQL]]) - 실행 시점에 문자열 형태로 조립되어 실행
190. [[190_bind_variable_soft_parsing|바인드 변수]] ([[190_bind_variable_soft_parsing|Bind Variable]]) - 파싱 결과 재사용, SQL [[480_injection|인젝션]] 방지, 하드 파싱 (Hard Parsing) 방지 [[282_performance_tactics|성능]] 이점

## 4. [[191_transaction_concept_states|트랜잭션]], [[014_concurrency|동시성]] 제어 및 [[658_ir_recovery|복구]] (70개)
191. [[191_transaction_concept_states|트랜잭션]] ([[191_transaction_concept_states|Transaction]]) - [[369_logic_bomb|논리]]적 작업의 기본 단위, 분할할 수 없는 일련의 연산
192. [[191_transaction_concept_states|트랜잭션]]의 ACID 특성
193. [[193_atomicity_all_or_nothing|원자성]] ([[193_atomicity_all_or_nothing|Atomicity]]) - All or Nothing (모두 반영되거나 모두 취소) - [[233_recovery_database_restoration_overview|회복]]([[658_ir_recovery|Recovery]]) 관리자가 보장
194. [[194_consistency_database_integrity|일관성]] ([[194_consistency_database_integrity|Consistency]]) - [[191_transaction_concept_states|트랜잭션]] 전후에 [[002_database_definition|데이터베이스]] 제약조건([[003_integrity|무결성]]) 유지 - 병행제어/[[073_integrity_constraints_overview|무결성 제약조건]] 보장
195. [[195_isolation_concurrency_control|격리성]] ([[195_isolation_concurrency_control|Isolation]]) - 실행 중인 [[191_transaction_concept_states|트랜잭션]] 연산에 다른 [[191_transaction_concept_states|트랜잭션]] 간섭 불가 - 병행 제어([[508_concurrency_control|Concurrency Control]]) 보장
196. [[196_durability_permanent_storage|영속성]] ([[196_durability_permanent_storage|Durability]]) - 성공 완료된 [[191_transaction_concept_states|트랜잭션]] 결과는 영구 반영 - [[233_recovery_database_restoration_overview|회복]]([[658_ir_recovery|Recovery]]) 관리자가 보장
197. [[197_transaction_state_transition|트랜잭션 상태 전이]] - 활동([[483_active_vs_passive_ftp|Active]]) -> 부분 완료(Partially Committed) -> 완료(Committed) / 실패(Failed) -> 철회(Aborted)
198. COMMIT [[158_instruction|명령어]] - [[191_transaction_concept_states|트랜잭션]] 성공적 완료, 디스크 반영 확정
199. [[313_rollback|ROLLBACK]] [[158_instruction|명령어]] - [[191_transaction_concept_states|트랜잭션]] 취소, 이전 상태로 [[658_ir_recovery|복구]]
200. [[200_savepoint_partial_rollback|SAVEPOINT]] - [[191_transaction_concept_states|트랜잭션]] 내 중간 [[658_ir_recovery|복구]] 지점 [[009_config|설정]]
201. [[014_concurrency|동시성]] 제어 ([[508_concurrency_control|Concurrency Control]] / 병행 제어)의 목적 - [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 유지, 다중 사용자 [[139_throughput|처리량]] 극대화
202. [[202_concurrent_execution_problems_overview|병행 수행 시 문제점]] ([[195_isolation_concurrency_control|격리성]] 위배 시)
203. [[203_lost_update_concurrency_problem|갱신 손실]] ([[203_lost_update_concurrency_problem|Lost Update]]) - 둘 이상의 [[191_transaction_concept_states|트랜잭션]]이 동시 갱신 시, 이전 값이 덮어써져 손실
204. [[204_inconsistency_unrepeatable_read_concurrency|모순성]] (Inconsistency / Unrepeatable Read) - 동일 [[001_dikw_pyramid|데이터]] 반복 읽기 시 값이 달라지는 현상
205. [[205_dirty_read_uncommitted_dependency|오손 읽기]] ([[528_third_normal_form|Dirty Read]]) - 다른 [[191_transaction_concept_states|트랜잭션]]이 아직 커밋하지 않은 미확정 [[001_dikw_pyramid|데이터]]를 읽음
206. [[206_cascading_rollback_unrecoverable_schedule|연쇄 복귀]] ([[206_cascading_rollback_unrecoverable_schedule|Cascading Rollback]]) - 한 [[191_transaction_concept_states|트랜잭션]] 취소 시, 의존하던 다른 [[191_transaction_concept_states|트랜잭션]]도 연쇄 취소
207. [[207_phantom_read_insert_range_query|유령 읽기]] ([[207_phantom_read_insert_range_query|Phantom Read]]) - 이전 읽기에 없던 새로운 행(INSERT)이 반복 읽기 시 나타남
208. [[208_schedule_history_transaction_execution_order|스케줄]] (Schedule / History) - [[191_transaction_concept_states|트랜잭션]] 연산의 실행 순서
209. [[209_serial_schedule_sequential_execution|직렬 스케줄]] ([[209_serial_schedule_sequential_execution|Serial Schedule]]) - [[191_transaction_concept_states|트랜잭션]]을 순차적으로 실행 ([[014_concurrency|동시성]] 0)
210. [[210_non_serial_schedule_interleaved_execution|비직렬 스케줄]] ([[210_non_serial_schedule_interleaved_execution|Non-serial Schedule]]) - 인터리빙 방식 병행 실행
211. [[211_serializable_schedule_concurrency_control_goal|직렬 가능 스케줄]] ([[211_serializable_schedule_concurrency_control_goal|Serializable Schedule]]) - 비직렬이지만 결과가 [[209_serial_schedule_sequential_execution|직렬 스케줄]]과 동일한 [[208_schedule_history_transaction_execution_order|스케줄]] 보장
212. [[212_conflict_serializable_schedule_operation_swap|충돌 직렬 가능성]] ([[212_conflict_serializable_schedule_operation_swap|Conflict Serializable]])
213. 락킹 ([[213_locking_mechanism_concurrency_control|Locking]]) 기법 - [[283_mutual_exclusion|상호 배제]]를 위한 잠금
214. [[214_shared_lock_read_concurrency|공유 락]] (Shared [[510_lock|Lock]] / Read [[510_lock|Lock]], S-[[510_lock|Lock]]) - 읽기 허용, [[289_cqrs_db|쓰기]] 불가
215. [[215_exclusive_lock_write_concurrency|배타 락]] (Exclusive [[510_lock|Lock]] / Write [[510_lock|Lock]], X-[[510_lock|Lock]]) - 읽기/[[289_cqrs_db|쓰기]] 모두 불가 독점
216. [[216_two_phase_locking_protocol_2pl|2단계 락킹 프로토콜]] ([[320_two_phase_locking_deadlock|2PL]], [[511_two_phase_locking|Two-Phase Locking]]) - [[149_serial_communication_rs232_rs485|직렬]] 가능성 보장을 위한 락 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
217. [[217_growing_phase_2pl|확장 단계]] ([[217_growing_phase_2pl|Growing Phase]]) - 락 획득만 가능, 반납 불가
218. [[218_shrinking_phase_2pl_cascading_rollback|축소 단계]] ([[218_shrinking_phase_2pl_cascading_rollback|Shrinking Phase]]) - 락 반납만 가능, 획득 불가
219. 2PL의 한계 - [[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]]) 발생 가능성, [[206_cascading_rollback_unrecoverable_schedule|연쇄 복귀]] 위험
220. 엄격한 [[320_two_phase_locking_deadlock|2PL]] ([[220_strict_2pl_cascading_rollback_prevention|Strict 2PL]]) - X-Lock을 커밋 전까지 보유 ([[206_cascading_rollback_unrecoverable_schedule|연쇄 복귀]] 방지)
221. 강건한 [[320_two_phase_locking_deadlock|2PL]] ([[221_rigorous_2pl_strict_locking_protocol|Rigorous 2PL]]) - S-[[510_lock|Lock]], X-[[510_lock|Lock]] 모두 커밋 전까지 보유
222. [[452_timestamp_ordering|타임스탬프 순서]] ([[222_timestamp_ordering_concurrency_control|Timestamp Ordering]]) 기법 - [[191_transaction_concept_states|트랜잭션]] 진입 시간에 맞춰 [[149_serial_communication_rs232_rs485|직렬]]화 (비관적 제어 아님, 락 없음)
223. [[223_optimistic_concurrency_control_validation|낙관적 동시성 제어]] ([[223_optimistic_concurrency_control_validation|Optimistic Concurrency Control]]) - 작업 먼저 수행 후 종료([[396_validation|Validation]]) 시점에 충돌 검사
224. [[224_mvcc_multi_version_concurrency_control|다중 버전 동시성 제어]] ([[449_mvcc|MVCC]], Multi-Version [[508_concurrency_control|Concurrency Control]]) - 읽기와 [[289_cqrs_db|쓰기]] 락 충돌 배제, [[022_snapshot_backup_architecture|스냅샷]] 활용 ([[188_pl_sql_t_sql_procedural|Oracle]], PostgreSQL 기본)
225. [[393_undo|Undo]] 세그먼트 ([[098_rollback_strategy_pipeline_error_threshold|롤백]] 세그먼트) - [[449_mvcc|MVCC]] 구버전 [[001_dikw_pyramid|데이터]] 저장 영역
226. 블로킹 ([[122_sync_async_communication|Blocking]]) 현상 완화 (MVCC의 가장 큰 장점 - 읽기가 [[289_cqrs_db|쓰기]]를 막지 않고, [[289_cqrs_db|쓰기]]가 읽기를 막지 않음)
227. [[227_transaction_isolation_levels_ansi_sql_standard|트랜잭션 고립화 수준]] ([[227_transaction_isolation_levels_ansi_sql_standard|Isolation Level]]) - ANSI/ISO SQL 표준 4단계
228. [[228_read_uncommitted_isolation_level|Read Uncommitted]] (레벨 0) - 커밋 안된 [[001_dikw_pyramid|데이터]] 읽기 허용 ([[528_third_normal_form|Dirty Read]] 발생)
229. [[229_read_committed_isolation_level|Read Committed]] (레벨 1) - 커밋된 [[001_dikw_pyramid|데이터]]만 읽음 ([[188_pl_sql_t_sql_procedural|Oracle]] 기본, Non-[[230_repeatable_read_isolation_level|Repeatable Read]] 발생)
230. [[230_repeatable_read_isolation_level|Repeatable Read]] (레벨 2) - [[191_transaction_concept_states|트랜잭션]] 내에서 읽은 [[001_dikw_pyramid|데이터]] 락 유지 (MySQL 기본, [[207_phantom_read_insert_range_query|Phantom Read]] 발생 가능성)
231. [[231_serializable_isolation_level|Serializable]] (레벨 3) - 완벽한 [[149_serial_communication_rs232_rs485|직렬]]화, 가장 엄격 (모든 이상현상 방지, [[014_concurrency|동시성]] 최저)
232. [[232_database_failure_types_transaction_system_media|데이터베이스 장애 유형]] - [[191_transaction_concept_states|트랜잭션]] 장애, 시스템 장애, 미디어 장애
233. [[233_recovery_database_restoration_overview|회복]] ([[658_ir_recovery|Recovery]]) - 장애 발생 전 일관된 상태로 DB 복원 ([[193_atomicity_all_or_nothing|원자성]], [[196_durability_permanent_storage|영속성]] 보장 기법)
234. [[234_redo_roll_forward_durability_recovery|Redo]] (재실행) - 장애 발생 후 커밋된 [[191_transaction_concept_states|트랜잭션]]을 [[568_logs_distributed_logging_elk_fluentd|로그]] [[316_reference_pattern_nosql|참조]]하여 재반영 ([[196_durability_permanent_storage|영속성]] 보장)
235. [[393_undo|Undo]] (취소) - 장애 발생 후 커밋 안된 [[191_transaction_concept_states|트랜잭션]]을 이전 상태로 원복 ([[193_atomicity_all_or_nothing|원자성]] 보장)
236. WAL ([[236_wal_write_ahead_logging_protocol|Write-Ahead Logging]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]] - [[001_dikw_pyramid|데이터]] 갱신 전 반드시 [[568_logs_distributed_logging_elk_fluentd|로그]]부터 디스크에 안전하게 기록
237. [[237_log_based_recovery_redo_undo_records|로그 기반 회복 기법]] ([[237_log_based_recovery_redo_undo_records|Log-based Recovery]])
238. [[238_deferred_update_recovery_no_undo|지연 갱신]] ([[238_deferred_update_recovery_no_undo|Deferred Update]]) - [[191_transaction_concept_states|트랜잭션]] 완료 전까지 DB 기록 [[015_지연_데이터_관점|지연]], [[393_undo|Undo]] 불필요, Redo만 수행
239. [[239_immediate_update_recovery_redo_undo|즉시 갱신]] ([[239_immediate_update_recovery_redo_undo|Immediate Update]]) - [[191_transaction_concept_states|트랜잭션]] 도중에도 DB 기록, [[233_recovery_database_restoration_overview|회복]] 시 Redo와 [[393_undo|Undo]] 모두 필요
240. 그림자 [[259_paging|페이징]] ([[240_shadow_paging_recovery_no_log|Shadow Paging]]) 기법 - [[568_logs_distributed_logging_elk_fluentd|로그]] 없이 구버전(그림자) 디렉토리와 현재 디렉토리 유지 교체 ([[542_cow_file_system|COW]] 유사)
241. 검사점 (Checkpoint / [[071_checkpointing|Checkpointing]]) [[233_recovery_database_restoration_overview|회복]] 기법 - 주기적으로 메모리 버퍼를 디스크에 [[212_synchronization_mechanisms|동기화]](Flush)하여 [[658_ir_recovery|복구]] 시간([[234_redo_roll_forward_durability_recovery|Redo]] 대상) 단축
242. [[242_media_recovery_dump_archive_rollforward|미디어 회복]] ([[242_media_recovery_dump_archive_rollforward|Media Recovery]]) - 디스크 손상 시 [[555_backup_and_restore_strategy|백업]](덤프) 아카이브와 [[568_logs_distributed_logging_elk_fluentd|로그]]를 이용해 롤포워드(Roll-[[235_forward_backward_chaining|forward]]) [[658_ir_recovery|복구]]
243. ARIES [[001_algorithm_definition|알고리즘]] - 현대 [[502_dbms|DBMS]] [[658_ir_recovery|복구]] 표준 [[001_algorithm_definition|알고리즘]] (Analysis, [[234_redo_roll_forward_durability_recovery|Redo]], [[393_undo|Undo]] 3단계 페이즈)
244. [[244_lsn_log_sequence_number_recovery_tracking|LSN]] ([[244_lsn_log_sequence_number_recovery_tracking|Log Sequence Number]]) - [[568_logs_distributed_logging_elk_fluentd|로그]] 레코드 고유 [[655_ir_detection_analysis|식별]] 번호
245. [[245_clr_compensation_log_record_undo_recovery|Compensation Log Record]] ([[245_clr_compensation_log_record_undo_recovery|CLR]]) - [[393_undo|Undo]] 수행 시 남기는 보상 [[568_logs_distributed_logging_elk_fluentd|로그]] (중복 [[393_undo|Undo]] 방지)
246. [[002_database_definition|데이터베이스]] [[281_deadlock_definition|교착 상태]] ([[281_deadlock_definition|Deadlock]]) 처리 기법 - Wait-Die, Wound-Wait (타임스탬프 선점/[[285_no_preemption|비선점]] 기반 예방)
247. [[247_wait_for_graph_deadlock_detection_victim|교착 상태 탐지 대기 그래프]] ([[305_wait_for_graph|Wait-for Graph]]) - 사이클 발생 시 희생자(주로 후발 [[191_transaction_concept_states|트랜잭션]]) [[098_rollback_strategy_pipeline_error_threshold|롤백]]
248. [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] ([[248_distributed_transaction_multiple_nodes|Distributed Transaction]]) - 둘 이상의 노드/DB에 걸친 [[191_transaction_concept_states|트랜잭션]]
249. [[249_two_phase_commit_2pc_distributed|2단계 커밋]] ([[549_2pc_two_phase_commit_limitations_msa|2PC]], [[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) - [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]의 [[193_atomicity_all_or_nothing|원자성]] 보장 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
250. 코디네이터 ([[250_coordinator_participant_2pc_roles|Coordinator]])와 참여자 (Participant) - 1단계(Prepare), 2단계(Commit/[[313_rollback|Rollback]])
251. [[251_three_phase_commit_3pc_blocking_solution|3단계 커밋]] (3PC, Three-Phase Commit) - 2PC의 블로킹 한계 보완 (Pre-Commit 추가)
252. [[305_saga|Saga]] 패턴 - [[619_msa_traffic_hardware|MSA]] 환경의 긴 [[191_transaction_concept_states|트랜잭션]](Long Lived [[191_transaction_concept_states|Transaction]]) 처리, 이벤트 기반 [[548_local_vs_distributed_transactions|로컬 트랜잭션]] 분할 및 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]([[551_compensating_transaction_logical_rollback|Compensating Transaction]]) 수행
253. [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) - [[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]]), [[452_availability|가용성]]([[452_availability|Availability]]), 분단 허용성([[514_partition_slice_volume|Partition]] Tolerance) 3가지를 동시 만족 불가 ([[136_variance|분산]] DB 이론)
254. [[086_CP_순환_전치_GI|CP]] 시스템 ([[543_hbase|HBase]], [[540_mongodb|MongoDB]] 기본) / [[572_ap_access_point_ds_distribution_system|AP]] 시스템 ([[541_cassandra|Cassandra]], [[545_dynamodb|DynamoDB]]) / [[089_contract_account_smart_contract|CA]] 시스템 (RDBMS, 네트워크 분할 없는 단일망)
255. [[342_pacelc|PACELC]] 정리 - [[341_process|CAP]] 확장판 (분할 P 시 A/C 대안, 정상 작동 E 시 L([[015_지연_데이터_관점|지연]])/C([[194_consistency_database_integrity|일관성]]) 상충 [[083_relationship_in_er_model|관계]])
256. [[650_eventual_consistency|결과적 일관성]] ([[650_eventual_consistency|Eventual Consistency]]) - 일정 시간이 지나면 결국 [[212_synchronization_mechanisms|동기화]]됨 ([[572_ap_access_point_ds_distribution_system|AP]] 시스템 특징, BASE 특성)
257. BASE [[082_attribute_types_er_model|속성]] - Basically Available, Soft-[[272_state_pattern|state]], Eventually consistent (NoSQL의 특성, ACID의 반대)
258. [[258_vector_clock|벡터 시계]] ([[258_vector_clock|Vector Clock]]) / 타임스탬프 - [[136_variance|분산]] 시스템 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]] 충돌 해결
259. [[259_raft_paxos|래프트]] ([[259_raft_paxos|Raft]]) / 팍소스 (Paxos) [[001_algorithm_definition|알고리즘]] - [[136_variance|분산]] DB 리더 선출 및 [[568_logs_distributed_logging_elk_fluentd|로그]] [[016_replication_factor|복제]] 합의 (Consensus)
260. [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] ([[190_split_brain_zookeeper_fencing_quorum|Split Brain]]) 현상 - 네트워크 단절로 두 개의 [[172_maas_mobility_as_a_service|마스]]터가 독립적 작동 (Quorum/과반수 투표로 방지)

## 5. [[136_variance|분산]] DB, [[035_nosql|NoSQL]] 및 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] (60개)
261. [[136_variance|분산]] [[002_database_definition|데이터베이스]] ([[261_distributed_database|Distributed Database]]) 목표 - 단일 시스템처럼 보이게 하는 투명성(Transparency) 제공
262. [[262_distributed_transparency|분산 데이터베이스 투명성 6가지 규칙]]
263. [[263_location_transparency|위치 투명성]] ([[263_location_transparency|Location Transparency]]) - [[001_dikw_pyramid|데이터]] 물리적 위치 몰라도 접근
264. [[264_fragmentation_transparency|분할 투명성]] ([[291_fragmentation_and_reassembly_process|Fragmentation]]/[[514_partition_slice_volume|Partition]] Transparency) - [[001_dikw_pyramid|데이터]] 분할 여부 은닉
265. [[265_replication_transparency|복제 투명성]] ([[265_replication_transparency|Replication Transparency]]) - [[001_dikw_pyramid|데이터]] 중복 유지 및 갱신 투명
266. 병행 투명성 ([[266_other_transparency|Concurrency]]) / 장애 투명성 (Failure) / 지역 사상 투명성 (Local [[010_schema_mapping|Mapping]])
267. [[267_data_fragmentation|데이터 분할 기법]] ([[291_fragmentation_and_reassembly_process|Fragmentation]])
268. [[268_horizontal_fragmentation|수평 분할]] ([[268_horizontal_fragmentation|Horizontal Fragmentation]]) - [[063_relation_tuple_cardinality|튜플]](행) 단위 분할, 셀렉트 연산
269. [[269_vertical_fragmentation|수직 분할]] ([[269_vertical_fragmentation|Vertical Fragmentation]]) - [[082_attribute_types_er_model|속성]](열) 단위 분할, [[042_relational_algebra_project|프로젝트 연산]] (PK 반드시 포함)
270. [[016_replication_factor|복제]] ([[016_replication_factor|Replication]]) - 동기식 [[016_replication_factor|복제]] ([[010_동기식_비동기식_전송|Synchronous]]) vs 비동기식 [[016_replication_factor|복제]] (Asynchronous)
271. [[172_maas_mobility_as_a_service|마스]]터-슬레이브 (Master-Slave / Primary-Replica) [[016_replication_factor|복제]] - 읽기/[[289_cqrs_db|쓰기]] [[136_variance|분산]] 아키텍처
272. 멀티 [[172_maas_mobility_as_a_service|마스]]터 (Multi-Master / [[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) [[016_replication_factor|복제]] - 양방향 [[289_cqrs_db|쓰기]] 가능, 충돌 해결 매커니즘 필수
273. 동종 [[136_variance|분산]] DB vs 이종 ([[273_heterogeneous_db|Heterogeneous]]) [[136_variance|분산]] DB 통합
274. [[035_nosql|NoSQL]] ([[274_nosql|Not Only SQL]]) [[002_database_definition|데이터베이스]] - [[005_schema|스키마]]리스(Schemaless), 수평적 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]]), [[136_variance|분산]] 아키텍처
275. [[035_nosql|NoSQL]] [[014_data_model_components|데이터 모델]] 4가지
276. [[036_key_value|키-값 저장소]] ([[036_key_value|Key-Value Store]]) - 속도 최적화, [[542_redis|Redis]], Memcached, Amazon [[545_dynamodb|DynamoDB]]
277. [[037_document|문서 저장소]] ([[037_document|Document Store]]) - [[343_json|JSON]]/XML 형태, BSON 포맷, 유연성, [[540_mongodb|MongoDB]], CouchDB
278. [[278_column_family_store|컬럼 패밀리 저장소]] (Column Family / [[238_wide_column_cassandra_hbase_lsm|Wide-Column Store]]) - 대량 [[289_cqrs_db|쓰기]]/읽기 특화, [[347_compaction|압축]] 우수, [[543_hbase|HBase]], [[541_cassandra|Cassandra]]
279. [[279_graph_store|그래프 저장소]] ([[279_graph_store|Graph Store]]) - 노드(Node), 엣지(Edge), [[082_attribute_types_er_model|속성]](Property) 구조, [[083_relationship_in_er_model|관계]] 탐색 최적화, Neo4j, Amazon Neptune
280. [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) - NoSQL의 수평적 [[179_table_partitioning_concept|파티셔닝]] 기술 ([[002_database_definition|데이터베이스]] 분할)
281. [[281_nosql_modeling_strategy|샤드 키]] (Shard [[067_db_key_uniqueness_minimality|Key]] / [[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) - [[136_variance|분산]] 배치 기준이 되는 키 설계 중요성
282. [[282_embedded_document_pattern|해시 샤딩]] ([[282_embedded_document_pattern|Hash Sharding]]) - 균등 분배 / 레인지 [[280_sharding|샤딩]] (Range [[243_sharding_horizontal_scaling_database|Sharding]]) - 범위 검색 유리 (핫스팟 문제 유의)
283. [[283_reference_pattern|일관된 해싱]] ([[244_consistent_hashing_ring_distribution|Consistent Hashing]]) - 노드 추가/삭제 시 재배치 최소화 (링 구조 [[055_array|배열]])
284. [[018_mapreduce|맵리듀스]] ([[018_mapreduce|MapReduce]]) - [[035_nosql|NoSQL]]/Hadoop의 [[136_variance|분산]] [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]] 처리 프로그래밍 모델 (Map: 매핑/필터링, Reduce: 집계)
285. [[285_tree_structure_storage|그래프 쿼리 언어]] - Cypher (Neo4j), Gremlin, SPARQL
286. [[057_tsdb_downsampling_retention_policy|시계열 데이터베이스]] (Time Series [[501_database|Database]], TSDB) - 시간순 로깅 특화, [[255_time_series_rollup_retention_compression|InfluxDB]], [[136_prometheus|Prometheus]]
287. [[287_multi_model_db_arangodb|시계열 데이터 특성]] - 높은 [[289_cqrs_db|쓰기]] [[139_throughput|처리량]], 다운샘플링 (Downsampling), 보존 [[164_policy|정책]] ([[515_mvcc|Retention]] [[164_policy|Policy]])
288. [[288_data_warehouse_definition|공간 데이터베이스]] ([[288_data_warehouse_definition|Spatial Database]]) - 좌표, 기하학적 객체 [[298_qkv_attention|쿼리]], PostGIS 확장
289. R 트리 ([[289_dw_4characteristics|R-Tree]]) / [[515_mbr_vs_gpt|MBR]] (Minimum Bounding Rectangle) - 공간 검색 [[154_database_index_b_tree_search_optimization|인덱스]] 구조
290. [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] [[002_database_definition|데이터베이스]] - RDB의 ACID [[191_transaction_concept_states|트랜잭션]]과 NoSQL의 수평적 확장성([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) 결합 패러다임
291. [[291_ods|구글 스패너]] ([[291_ods|Google Cloud Spanner]]) - 글로벌 [[136_variance|분산]], 트루타임(TrueTime/원자시계+GPS) 기반 글로벌 [[194_consistency_database_integrity|일관성]] 보장 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]]
292. 칵로치DB ([[292_etl_process|CockroachDB]]) - 생존성 극대화 [[136_variance|분산]] SQL [[002_database_definition|데이터베이스]]
293. [[293_elt_process|티아이디비]] ([[293_elt_process|TiDB]]) - [[294_oltp_vs_olap|HTAP]] (Hybrid Transactional/Analytical Processing) 지원 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]]
294. [[294_oltp_vs_olap|HTAP]] - [[327_hint_handoff|OLTP]]([[191_transaction_concept_states|트랜잭션]])와 [[316_olap|OLAP]](분석) 워크로드를 단일 [[002_database_definition|데이터베이스]] 플랫폼에서 분리/동시 처리하는 기술 (Row+Column 하이브리드 엔진)
295. [[295_olap_operations|메모리 캐싱]] ([[456_caching|Caching]]) 기술 적용 - Look-aside ([[182_lazy_loading|Lazy Loading]]) 패턴, [[276_write_through|Write-through]] 패턴
296. [[296_star_schema|캐시 스탬피드]] ([[296_star_schema|Cache Stampede]]) / Thundering Herd 문제 - 대규모 동시 캐시 미스 발생 부하
297. [[297_snowflake_schema|레디스]] ([[542_redis|Redis]]) 자료구조 - String, List, Set, Sorted Set, Hash
298. 몽고DB ([[540_mongodb|MongoDB]]) 아키텍처 - 레플리카 셋 (Replica Set), 샤드 클러스터 (mongos, [[009_config|config]] server, shard)
299. [[299_data_lake|카산드라]] ([[541_cassandra|Cassandra]]) 특징 - 링 기반 피어투피어, 가십 [[295_protocol_field_tcp_udp_icmp|프로토콜]](Gossip [[295_protocol_field_tcp_udp_icmp|Protocol]]), 튜너블 컨시스턴시 (Tunable [[194_consistency_database_integrity|Consistency]] - Quorum Read/Write)
300. [[300_schema_on_write_vs_read|툼스톤]] ([[300_schema_on_write_vs_read|Tombstone]]) 메커니즘 - [[136_variance|분산]] DB에서 삭제된 레코드 마킹 (삭제 [[212_synchronization_mechanisms|동기화]] [[015_지연_데이터_관점|지연]] 해결)
301. [[001_dikw_pyramid|데이터]] 마이그레이션 도구 및 [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) - Debezium 등 실시간 변경 로깅/전송
302. [[302_cdc|엘라스틱서치]] ([[302_cdc|Elasticsearch]]) - 루씬(Lucene) 기반 텍스트 검색 및 분석 [[500_inverted_index_elasticsearch|역색인]]([[500_inverted_index_elasticsearch|Inverted Index]]) DB
303. [[500_inverted_index_elasticsearch|역색인]] ([[500_inverted_index_elasticsearch|Inverted Index]]) 구조 - 단어(Term)가 포함된 문서 ID 리스트 매핑 (검색 엔진 핵심)
304. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] ([[210_data_lakehouse_delta_lake|Data Lakehouse]]) - [[208_data_lake_schema_on_read|데이터 레이크]](비정형)와 웨어하우스(정형)의 융합 구조 ([[074_photon_engine|Databricks]], [[147_delta_lake|Delta Lake]])
305. 오라클 RAC ([[305_vector_db|Real Application Clusters]]) - 공유 디스크(Shared Disk) 기반 다중 인스턴스 클러스터링 RDB (수직적 한계 완화)
306. [[306_embedding_model|셰어드 낫띵]] ([[306_embedding_model|Shared Nothing]]) 아키텍처 - [[001_dikw_pyramid|데이터]] 분할 공유 (수평 확장, [[035_nosql|NoSQL]] 기본 구조)
307. [[307_gsi_global_secondary_index_overhead|글로벌 보조 인덱스]] (GSI, Global Secondary [[154_database_index_b_tree_search_optimization|Index]]) [[136_variance|분산]] 환경 오버헤드
308. [[308_pgvector|폴리글랏 퍼시스턴스]] ([[132_polyglot_persistence|Polyglot Persistence]]) - [[532_microservices_decomposition_patterns|마이크로서비스]]마다 목적에 맞는 최적의 이기종 DB 선택/혼용
309. [[306_cqrs|CQRS]] 아키텍처와 DB [[212_synchronization_mechanisms|동기화]] ([[307_event_sourcing|Event Sourcing]] 연동)
310. [[310_multi_tenant_database_architecture|멀티테넌트]] ([[888_multi_tenant_cloud_resource_isolation_noisy_neighbor|Multi-tenant]]) [[002_database_definition|데이터베이스]] 구조 - [[369_logic_bomb|논리]]적 [[005_schema|스키마]] 분리, 물리적 인스턴스 분리 격리
311. [[311_database_fuzzing_vulnerability_test|데이터베이스 퍼징]] ([[311_database_fuzzing_vulnerability_test|Database Fuzzing]]) 및 테스트 취약점
312. 클라우드 관리형 DB (DBaaS, [[501_database|Database]] [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - AWS RDS, Azure SQL 등
313. [[306_graph_neural_network_gnn|그래프 신경망]] ([[159_gnn_graph_neural_network_message_passing|GNN]]) 연계를 위한 [[039_graph_db|그래프 데이터베이스]] 활용
314. [[035_nosql|NoSQL]] 모델링 [[268_strategy_pattern|전략]] - [[093_normalization|정규화]]가 아닌 [[298_qkv_attention|쿼리]] 패턴 주도 설계 (Query-driven Modeling), [[111_denormalization_performance_tradeoff|역정규화]] 내재화
315. [[315_embedded_document_pattern_nosql|임베디드 도큐먼트]] ([[315_embedded_document_pattern_nosql|Embedded Document]]) 패턴 - 연관 [[001_dikw_pyramid|데이터]]를 한 문서에 중첩 저장 (조인 배제)
316. [[316_reference_pattern_nosql|참조]] ([[316_reference_pattern_nosql|Reference]]) 패턴 - 문서 크기 한계 시 외부 링크 저장
317. [[317_versioning_data_model_design|버저닝]] ([[317_versioning_data_model_design|Versioning]]) [[014_data_model_components|데이터 모델]] 설계
318. 트리 구조 저장을 위한 [[035_nosql|NoSQL]] 모델 (Materialized Path, Nested Sets)
319. [[319_blockchain_tamper_evident_ledger_amazon_qldb|블록체인 기반 변조 방지 원장 데이터베이스]] ([[319_blockchain_tamper_evident_ledger_amazon_qldb|Amazon QLDB]])
320. [[320_multi_model_database_arangodb|다중 모델 데이터베이스]] ([[320_multi_model_database_arangodb|Multi-model Database]]) - 단일 엔진 내 [[037_document|Document]], [[104_graph|Graph]], KV, Relational 지원 (ArangoDB 등)

## 6. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]], [[316_olap|OLAP]] 및 최신 DB 트렌드 (70개)
321. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]], [[209_data_warehouse_schema_on_write|DW]]) - 의사결정 지원을 위한 통합, 주젯 중심, 시계열, 비휘발성 저장소 ([[311_inmon|Inmon]] 모델)
322. [[209_data_warehouse_schema_on_write|DW]] 4대 특징 - 주젯 지향성(Subject-oriented), 통합성(Integrated), 시계열성(Time-variant), 비휘발성(Non-volatile)
323. [[209_data_mart_kimball_star_schema|데이터 마트]] ([[209_data_mart_kimball_star_schema|Data Mart]]) - 특정 부서/조직 중심의 소규모 [[209_data_warehouse_schema_on_write|DW]] ([[312_kimball|Kimball]] 모델 - 상향식)
324. [[291_ods|ODS]] ([[264_ods_operational_data_store_realtime|Operational Data Store]]) - DW로 가기 전의 임시/운영 [[001_dikw_pyramid|데이터]] 통합 영역
325. [[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load) 프로세스 - 소스 추출 -> 정제/변환 -> 타겟 적재
326. [[034_elt|ELT]] (Extract, Load, Transform) 프로세스 - 클라우드 기반 현대 아키텍처, 먼저 적재 후 웨어하우스 내에서 변환 처리
327. [[327_hint_handoff|OLTP]] ([[327_hint_handoff|On-Line Transaction Processing]]) - 실시간 [[191_transaction_concept_states|트랜잭션]], [[093_normalization|정규화]]된 RDB, 빠른 응답 속도
328. [[316_olap|OLAP]] ([[328_lsm_tree_compaction|On-Line Analytical Processing]]) - 대용량 다차원 분석, 비정규화([[334_star_schema|스타 스키마]]), 읽기 위주
329. [[316_olap|OLAP]] 연산 ([[329_delta_encoding|Operation]]) - [[042_rollup_l2_solution|롤업]], 드릴다운, [[331_neuromorphic_ai_db|슬라이스]], 다이스, [[037_pivot|피벗]]
330. [[042_rollup_l2_solution|롤업]] ([[330_olap_rollup_drilldown|Roll-up]]) - 요약 / 드릴다운 (Drill-down) - 구체화 (계층 구조 상하 이동)
331. [[331_neuromorphic_ai_db|슬라이스]] ([[331_neuromorphic_ai_db|Slice]]) - 특정 차원의 단일 평면 절단 / 다이스 (Dice) - 여러 차원의 작은 주사위 모양 추출
332. [[037_pivot|피벗]] ([[037_pivot|Pivot]]) - 보고서 축 전환 (행렬 변환)
333. [[333_multidimensional_modeling|다차원 모델링]] - 팩트 (Fact / 측정값)와 차원 (Dimension / 분석 기준) 구성
334. [[334_star_schema|스타 스키마]] ([[296_star_schema|Star Schema]]) - 사실 테이블 1개, [[093_normalization|정규화]] 안된 다수 [[273_dimension_table_analysis_perspective|차원 테이블]] 방사형 배치 (빠른 조인, 중복 존재)
335. [[335_snowflake_schema|스노우플레이크 스키마]] ([[313_snowflake_schema|Snowflake Schema]]) - [[273_dimension_table_analysis_perspective|차원 테이블]]을 [[105_third_normal_form_3nf_transitive|3NF]] [[093_normalization|정규화]]하여 중복 제거, 조인 복잡성 증가 눈송이 형태
336. [[336_molap|MOLAP]] ([[336_molap|Multidimensional OLAP]]) - 다차원 큐브(Cube) 사전 [[087_process_state_transition|생성]] 구조, [[148_5g_embb_urllc_mmtc|초고속]] 검색, 큐브 갱신 비용 큼
337. [[337_rolap|ROLAP]] ([[337_rolap|Relational OLAP]]) - [[083_relationship_in_er_model|관계]]형 DB 기반 SQL 실시간 분석, 대용량 처리에 적합
338. [[338_holap|HOLAP]] ([[338_holap|Hybrid OLAP]]) - MOLAP의 속도 + ROLAP의 대용량 처리 결합
339. [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) - 원시 [[001_dikw_pyramid|데이터]]([[225_raw|Raw]] [[001_dikw_pyramid|data]]), 정형/반정형/비정형 모두 저장하는 [[009_schema_on_read|스키마 온 리드]]([[009_schema_on_read|Schema-on-read]]) 중앙 저장소
340. [[010_schema_on_write|스키마 온 라이트]] ([[010_schema_on_write|Schema-on-write]]) - RDBMS의 입력 시점 [[005_schema|스키마]] [[395_verification_process_review|검증]]
341. [[009_schema_on_read|스키마 온 리드]] ([[009_schema_on_read|Schema-on-read]]) - [[208_data_lake_schema_on_read|데이터 레이크]]/NoSQL의 조회 시점 [[005_schema|스키마]] 적용
342. [[342_metadata_catalog|메타데이터 카탈로그]] ([[544_hive|Hive]] Metastore, AWS Glue) - [[208_data_lake_schema_on_read|데이터 레이크]] 자산 검색 지원
343. [[218_cdc_change_data_capture|변경 데이터 캡처]] ([[217_cdc_binlog_change_capture_debezium|CDC]], [[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) [[645_data_pipeline_acceleration|데이터 파이프라인]]
344. [[229_stream_processing_kafka_flink|스트림 처리]] ([[229_stream_processing_kafka_flink|Stream Processing]]) DB 기술 ([[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]], Flink) - 실시간 이벤트 [[002_database_definition|데이터베이스]]화
345. [[228_batch_processing_hadoop_spark|배치 처리]] ([[228_batch_processing_hadoop_spark|Batch Processing]]) [[123_pipe|파이프]]라인
346. [[223_vector_database_embedding|벡터 데이터베이스]] ([[223_vector_database_embedding|Vector Database]]) - [[190_ai_llm_requirements_specification|AI]], [[263_llm_large_language_model|LLM]], 딥러닝 [[278_instruction_tuning|임베딩]]([[278_instruction_tuning|Embedding]]) 벡터 고속 검색에 특화 ([[320_gnn_vector_db_recommendation|Milvus]], Pinecone, Qdrant 등)
347. [[278_instruction_tuning|임베딩]] ([[278_instruction_tuning|Embedding]]) 모델 - [[004_unstructured_data|비정형 데이터]](텍스트, 이미지)를 고차원 숫자 [[055_array|배열]]로 변환
348. [[348_similarity_search|유사도 검색]] ([[348_similarity_search|Similarity Search]]) - 벡터 간 거리/각도 기반 의미적 탐색 연산 (키워드 일치 검색의 대안)
349. [[359_cosine_similarity|코사인 유사도]] ([[359_cosine_similarity|Cosine Similarity]]) - 벡터 간 각도 측정
350. [[350_ann|유클리디안 거리]] (Euclidean Distance / L2) / 내적 ([[519_dot_dns_over_tls|Dot]] Product)
351. [[350_ann|ANN]] ([[351_hnsw|Approximate Nearest Neighbor]]) [[001_algorithm_definition|알고리즘]] - 벡터 DB의 고속 근사치 검색 (정확도 일부 희생, 속도 극대화)
352. [[351_hnsw|HNSW]] ([[352_rag|Hierarchical Navigable Small World]]) - 대표적인 [[300_ann_approximate_nearest_neighbor_vector_index|벡터 인덱싱]] [[070_graph_datastructure|그래프]] 기반 [[350_ann|ANN]] [[001_algorithm_definition|알고리즘]]
353. [[276_fine_tuning|RAG]] ([[585_rag_retrieval_augmented_generation|Retrieval-Augmented Generation]]) 패턴 - 벡터 DB를 연동하여 [[263_llm_large_language_model|LLM]] [[087_process_state_transition|생성]]의 [[275_react_framework|환각]]([[345_llm_foundation_model_hallucination|Hallucination]]) 방지 프레임워크
354. 벡터 [[154_database_index_b_tree_search_optimization|인덱스]] IVFFlat ([[354_vector_index_ivfflat|Inverted File Flat]])
355. [[308_pgvector|PGVector]] - PostgreSQL RDBMS의 벡터 검색 확장 플러그인 [[192_module_independence|모듈]]
356. [[356_cloud_data_warehouse_redshift_bigquery_snowflake|클라우드 데이터 웨어하우스 솔루션]] - Amazon Redshift, Google [[263_storage_compute_separation_bigquery|BigQuery]], [[541_cassandra|Snowflake]] 아키텍처 특성
357. [[357_separation_of_storage_and_compute|스토리지와 컴퓨팅 분리 아키텍처]] ([[357_separation_of_storage_and_compute|Separation of Storage and Compute]]) - [[531_cloud_native_architecture|클라우드 네이티브]] [[209_data_warehouse_schema_on_write|DW]] 핵심, 독립적 탄력적 확장
358. [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) - 중앙 집중형 [[208_data_lake_schema_on_read|데이터 레이크]] 한계 극복, [[064_relation_domain|도메인]] 주도의 [[136_variance|분산]] [[104_da_as_is_analysis|데이터 아키텍처]] 조직론
359. [[212_data_fabric_virtualization|데이터 패브릭]] ([[212_data_fabric_virtualization|Data Fabric]]) 플랫폼 ([[015_virtualization|가상화]] 연계망)
360. [[360_data_virtualization|데이터 가상화]] ([[247_data_virtualization_federated_query|Data Virtualization]]) - 물리적 이동/[[016_replication_factor|복제]] 없이 다양한 소스 [[369_logic_bomb|논리]]적 통합 조회 뷰
361. [[062_darkdata|다크 데이터]] ([[062_darkdata|Dark Data]]) 관리 및 발견
362. [[362_privacy_preserving_db|프라이버시 보존형 데이터베이스]] ([[362_privacy_preserving_db|동형 암호 검색 데이터베이스 적용 기초]])
363. [[306_graph_neural_network_gnn|그래프 신경망]] ([[159_gnn_graph_neural_network_message_passing|GNN]])과 [[160_knowledge_graph_graphrag_integration|지식 그래프]] ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]]) 연계 DB 시스템
364. [[214_data_lineage_tracking|데이터 리니지]] ([[214_data_lineage_tracking|Data Lineage]]) - [[001_dikw_pyramid|데이터]] 기원, 이동 경로, 변환 이력 추적(규제 대응, [[003_integrity|무결성]])
365. [[365_tde|데이터베이스 암호화]] ([[403_tde_transparent_data_encryption|TDE]], [[403_tde_transparent_data_encryption|Transparent Data Encryption]]) - 애플리케이션 수정 없이 디스크 저장 [[501_file_definition_logical_record|파일]] 레벨 암호화 (휴지 상태 암호화)
366. 컬럼 레벨 암호화 / 블록 레벨 암호화
367. [[528_obfuscation_anti_debugging_mobile|난독화]] ([[528_obfuscation_anti_debugging_mobile|Obfuscation]]) 및 [[819_data_masking|데이터 마스킹]] ([[819_data_masking|Data Masking]]) - 개발/운영계 테스트 DB 민감 [[199_information_hiding_encapsulation|정보 은닉]]
368. [[822_fpe|FPE]] ([[822_fpe|Format Preserving Encryption]]) - 암호화 전후 [[001_dikw_pyramid|데이터]] 포맷(길이, 형식) 유지 (카드번호, 주민번호 등)
369. [[369_db_auditing|데이터베이스 감사]] ([[369_db_auditing|DB Auditing]]) 추적 [[568_logs_distributed_logging_elk_fluentd|로그]]
370. [[370_db_firewall_access_control|접근 통제 정책 기반 방화벽]] (DB [[690_firewall_generation_evolution|방화벽]]) - SQL [[480_injection|인젝션]] 차단 및 IP/[[446_port_and_bus|포트]]/접근시간 제어
371. SQL [[480_injection|인젝션]] ([[604_sql_injection|SQL Injection]]) 공격 및 방어 수단 (Prepared Statement / 바인드 파라미터)
372. [[498_dataops_automation_pipeline|데이터 옵스]] ([[324_dataops|DataOps]]) - [[645_data_pipeline_acceleration|데이터 파이프라인]] [[076_ci_continuous_integration|지속적 통합]]/배포/[[229_monitor|모니터]]링 개발 문화
373. [[676_cold_data_archiving|콜드 데이터]] ([[676_cold_data_archiving|Cold Data]]) vs [[675_hot_data_caching|핫 데이터]] ([[675_hot_data_caching|Hot Data]]) 계층화(Tiering) 스토리지 아키텍처
374. 공간 [[154_database_index_b_tree_search_optimization|인덱스]] Quad-tree [[001_algorithm_definition|알고리즘]]
375. 시계열 DB 보간 ([[187_time_series_interpolation_rollup_dashboard|Interpolation]]) [[298_qkv_attention|쿼리]] 기능
376. [[035_nosql|NoSQL]] [[514_partition_slice_volume|파티션]] 톨러런스 [[658_ir_recovery|복구]] (Hinted Handoff, Anti-[[151_entropy|entropy]] 매커니즘 / [[007_merkle_tree|머클 트리]]([[007_merkle_tree|Merkle Tree]]) 비교)
377. [[377_lsm_tree_storage_engine|LSM-Tree]] ([[221_lsm_tree_memtable_sequential_flush_compaction|Log-Structured Merge-Tree]]) - 빅데이터/[[035_nosql|NoSQL]]([[541_cassandra|Cassandra]], RocksDB) [[289_cqrs_db|쓰기]] 최적화 저장 엔진 ([[494_memtable_sstable_flush|MemTable]] -> SSTable 구조)
378. [[378_lsm_compaction_tombstone|콤팩션]] ([[347_compaction|Compaction]]) - LSM 트리 구조 병합 및 [[300_schema_on_write_vs_read|툼스톤]] 정리
379. [[379_delta_encoding_gorilla_compression|델타 인코딩]] ([[329_delta_encoding|Delta Encoding]]) 및 시계열 [[159_compression|데이터 압축]] (Gorilla алгоритм)
380. [[380_sequence_vs_auto_increment|시퀀스 데이터베이스 객체 특징]] ([[380_sequence_vs_auto_increment|Auto Increment vs Sequence]])
381. 메인 메모리 DB의 [[022_snapshot_backup_architecture|스냅샷]] 로깅 ([[381_imdb_snapshot_logging_checkpointing|Checkpointing in IMDB]])
382. [[382_neuromorphic_ai_database_trends|뉴모픽]]([[382_neuromorphic_ai_database_trends|Neuromorphic]]) 인프라 연동형 [[190_ai_llm_requirements_specification|AI]] [[002_database_definition|데이터베이스]] 기술 동향
383. [[383_graph_data_analysis_pagerank_bfs|그래프 데이터 분석 알고리즘]] (PageRank, [[035_bfs|BFS]] 최단경로 매핑 DB 엔진 연산)
384. [[384_realtime_cdp_database_model|실시간 커스터머 데이터 플랫폼]] ([[193_crl_distribution_point_cdp|CDP]]) 구성을 위한 DB 연계 모델
385. [[385_third_party_cookie_deprecation_cdw|서드파티]] ([[385_third_party_cookie_deprecation_cdw|3rd Party]]) [[475_cookie_local_state|쿠키]] 소멸에 대비한 퍼스트파티 고객 [[001_dikw_pyramid|데이터]] 저장소(CDW) 아키텍처
386. [[386_data_clean_room_sharing|데이터 공유]] ([[001_dikw_pyramid|Data]] Sharing / Clean Room) 보안 [[514_partition_slice_volume|파티션]] 교환 모델 ([[541_cassandra|Snowflake]] [[305_data_clean_room|Data Clean Room]] 등)
387. [[387_zkp_blockchain_data_query|블록체인 기반의 영지식 증명]]([[354_did_decentralized_identity_zkp|ZKP]]) [[001_dikw_pyramid|데이터]] 질의 프레임워크 연구 모델
388. [[388_spanner_truetime_clock_skew|분산 노드 간 클럭 스큐]]([[388_spanner_truetime_clock_skew|Clock Skew]]) 해결용 스패너(Spanner) 트루타임 원리
389. [[389_bulk_insert_batching_optimization|대용량 트랜잭션의 배칭]]([[389_bulk_insert_batching_optimization|Batching]]) 삽입 최적화 (Bulk Insert / COPY [[158_instruction|명령어]])
390. [[206_serverless_cold_start|서버리스]] DB 오로라 ([[390_aurora_serverless_quorum_write|Aurora]]) 스토리지 로깅 [[136_variance|분산]] 쿼럼 [[289_cqrs_db|쓰기]] (6개 [[016_replication_factor|복제]]본 중 4개 이상 [[396_validation|확인]] 시 완료) 아키텍처 특장점

## 7. 시험 빈출 핵심 요약 및 실무 용어 확장 (210개)
391. [[391_relation_schema_intension|릴레이션 스키마]] (내포 / Intension) 구조
392. [[392_relation_instance_extension|릴레이션 인스턴스]] (외연 / Extension) 값
393. [[393_data_dictionary|데이터 사전]] ([[509_data_dictionary|Data Dictionary]]) 질의
394. [[394_catalog_metadata|카탈로그]] ([[394_catalog_metadata|Catalog]]) [[012_metadata|메타데이터]]
395. [[395_data_independence_logical_physical|데이터 독립성 2단계]] ([[369_logic_bomb|논리]], 물리)
396. [[010_schema_mapping|Mapping]] 규칙 개체->테이블
397. [[397_partial_functional_dependency_2nf|부분 함수 종속 제2정규형]]
398. [[398_transitive_functional_dependency_3nf|이행 함수 종속 제3정규형]]
399. [[529_bcnf|BCNF]] 모든 [[095_determinant_dependent|결정자]] 후보키
400. [[400_mvd_4nf|MVD]] ([[400_mvd_4nf|다치 종속]]) [[108_fourth_normal_form_4nf|제4정규형]]
401. [[401_join_dependency_5nf|조인 종속 제5정규형]]
402. [[091_functional_dependency_fd|삽입 이상]] ([[091_functional_dependency_fd|Insertion Anomaly]])
403. [[092_deletion_anomaly|삭제 이상]] ([[092_deletion_anomaly|Deletion Anomaly]])
404. [[093_update_anomaly|갱신 이상]] ([[093_update_anomaly|Update Anomaly]])
405. [[074_entity_integrity_primary_key|개체 무결성]] ([[074_entity_integrity_primary_key|Entity Integrity]]) 기본키 NULL 불가
406. [[075_referential_integrity_foreign_key_cascade|참조 무결성]] ([[406_referential_integrity_foreign_key|Referential]]) 외래키
407. [[407_super_key_minimality|슈퍼 키 최소성 부재]]
408. [[408_alternate_key|대체 키 후보키 중 탈락키]]
409. [[038_relational_algebra|관계 대수]] ([[409_relational_algebra|절차적 연산]])
410. [[410_relational_calculus|관계 해석]] (비절차적 연산, 술어)
411. [[411_division_operation|디비전]] ([[411_division_operation|Division]]) 연산 
412. [[412_cartesian_product|카티션 프로덕트]] ([[412_cartesian_product|조인 조건 누락]]) 
413. [[413_natural_join|자연 조인]] (동등 [[082_attribute_types_er_model|속성]] 자동 조인/중복 제거)
414. [[414_outer_join|외부 조인]] ([[414_outer_join|Outer Join]] + 표시 / 기준 [[061_relation_schema_instance|릴레이션]] 보존)
415. [[020_ddl|DDL]] (CREATE, ALTER, DROP, TRUNCATE [[098_rollback_strategy_pipeline_error_threshold|롤백]] 불가)
416. [[083_dml|DML]] (INSERT, UPDATE, DELETE [[098_rollback_strategy_pipeline_error_threshold|롤백]] 가능)
417. [[022_dcl|DCL]] (GRANT, REVOKE 권한 통제)
418. [[023_tcl|TCL]] (COMMIT, [[313_rollback|ROLLBACK]], [[200_savepoint_partial_rollback|SAVEPOINT]])
419. 뷰 ([[151_sql_view_virtual_table|VIEW]]) [[087_process_state_transition|생성]] 가상 테이블
420. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] CBO 시스템 통계 
421. [[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]] 풀 스캔 vs [[154_database_index_b_tree_search_optimization|인덱스]] 스캔)
422. [[154_database_index_b_tree_search_optimization|인덱스]] B+Tree 리프 노드 순차 연결
423. [[160_non_clustered_index_secondary|넌클러스터드 인덱스]] ([[423_non_clustered_index|포인터 배열]])
424. [[159_clustered_index_physical_sort|클러스터드 인덱스]] ([[424_clustered_index|물리적 레코드 정렬]])
425. [[157_hash_index_equal_search|해시 인덱스]] ([[425_hash_index_bucket_chaining|버킷 충돌 체이닝]]) 
426. [[426_bitmap_index_low_cardinality|비트맵 인덱스 분포도 낮음 특화]] 
427. [[161_composite_index_leading_column|결합 인덱스]] ([[261_composite_pattern_tree_structure|Composite]]) 순서 중요 
428. [[428_table_full_scan|테이블 풀 스캔]] ([[428_table_full_scan|Table Full Scan]] / FTS) 
429. [[429_index_range_scan|인덱스 레인지 스캔]] ([[429_index_range_scan|Index Range Scan]])
430. [[430_index_fast_full_scan|인덱스 패스트 풀 스캔]] ([[430_index_fast_full_scan|병렬]])
431. [[172_nl_join_nested_loop|중첩 루프 조인]] ([[431_nested_loop_join|Nested Loop]])
432. [[173_sort_merge_join|소트 머지 조인]] ([[432_sort_merge_join|정렬 후 병합]])
433. [[174_hash_join|해시 조인]] ([[433_hash_join_build_probe|메모리 해시 영역 빌드 프로브]])
434. 서브쿼리 IN 연산자 
435. [[435_exists_boolean_fast_search|EXISTS]] ([[435_exists_boolean_fast_search|존재 여부 불린 반환 고속 탐색]])
436. 윈도우 함수 OVER ([[436_window_function_over|PARTITION BY]])
437. RANK() 동점 점프 / DENSE_RANK() 비점프
438. [[522_group_by|GROUP BY]] 다차원 [[042_rollup_l2_solution|ROLLUP]], CUBE
439. [[439_optimizer_hint_index|힌트 구문 적용]] (/*+ [[154_database_index_b_tree_search_optimization|INDEX]]() */)
440. [[191_transaction_concept_states|트랜잭션]] ACID 특성 
441. [[193_atomicity_all_or_nothing|원자성]] ([[441_atomicity_recovery|회복 보장]]) 
442. [[194_consistency_database_integrity|일관성]] ([[442_consistency_integrity|무결성 보장]])
443. [[443_isolation_concurrency_control|고립성]] ([[443_isolation_concurrency_control|병행제어 보장]]) 
444. [[196_durability_permanent_storage|영속성]] ([[568_logs_distributed_logging_elk_fluentd|로그]]/[[441_atomicity_recovery|회복 보장]]) 
445. [[203_lost_update_concurrency_problem|갱신 손실]] ([[203_lost_update_concurrency_problem|Lost Update]])
446. [[205_dirty_read_uncommitted_dependency|오손 읽기]] ([[528_third_normal_form|Dirty Read]] 미커밋 읽기) 
447. [[447_non_repeatable_read|반복 불가능 읽기]] (Non-Repeatable Update 변경) 
448. [[207_phantom_read_insert_range_query|유령 읽기]] ([[207_phantom_read_insert_range_query|Phantom Read]] Insert 추가) 
449. [[449_locking_s_x_lock|동시성 제어 잠금]] ([[213_locking_mechanism_concurrency_control|Locking]]) S-락 / X-락
450. [[450_two_phase_locking_2pl|2단계 잠금]] ([[320_two_phase_locking_deadlock|2PL]]) 확장/축소 
451. [[281_deadlock_definition|교착 상태]] ([[451_deadlock_wait_die|Deadlock Wait-Die]])
452. [[452_timestamp_ordering|타임스탬프 순서]] ([[222_timestamp_ordering_concurrency_control|Timestamp Ordering]])
453. [[449_mvcc|MVCC]] 다중 [[288_version_ihl_tos_total_length|버전]] 읽기 [[194_consistency_database_integrity|일관성]]
454. [[454_undo_segment_rollback|언두]] ([[393_undo|Undo]] [[098_rollback_strategy_pipeline_error_threshold|롤백]]/읽기 [[194_consistency_database_integrity|일관성]] 세그먼트) 
455. [[455_redo_log_archive|리두]] ([[234_redo_roll_forward_durability_recovery|Redo]] [[658_ir_recovery|복구]] [[568_logs_distributed_logging_elk_fluentd|로그]] 아카이브)
456. WAL [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[456_wal_protocol_write_ahead|먼저 로그 기록]])
457. [[457_checkpoint_recovery_optimization|체크포인트 회복 범위 단축]] 
458. [[458_isolation_levels_read_uncommitted_to_serializable|고립화 수준]] ([[228_read_uncommitted_isolation_level|Read Uncommitted]]~[[231_serializable_isolation_level|Serializable]])
459. [[136_variance|분산]] DB [[263_location_transparency|위치 투명성]] 
460. [[460_data_fragmentation_horizontal_vertical|단편화 수평 분할]] (행) / [[269_vertical_fragmentation|수직 분할]] (열 PK포함)
461. [[461_replication_master_slave|복제 마스터-슬레이브]] 
462. [[249_two_phase_commit_2pc_distributed|2단계 커밋]] ([[549_2pc_two_phase_commit_limitations_msa|2PC]] Prepare -> Commit)
463. [[341_process|CAP]] 이론 정합성 [[452_availability|가용성]] [[514_partition_slice_volume|파티션]] [[136_variance|분산]] 특성
464. BASE [[082_attribute_types_er_model|속성]] [[035_nosql|NoSQL]] [[650_eventual_consistency|결과적 일관성]] 
465. 키-값 DB [[297_snowflake_schema|레디스]] 인메모리 
466. 도큐먼트 DB 몽고DB [[343_json|JSON]] BSON 
467. 컬럼 패밀리 [[543_hbase|HBASE]] [[299_data_lake|카산드라]] 와이드 컬럼
468. [[070_graph_datastructure|그래프]] DB 노드 엣지 프로퍼티 [[083_relationship_in_er_model|관계]] 탐색 Neo4j
469. [[469_sharding_horizontal_partitioning|샤딩 파티셔닝 수평 스케일 아웃]] 
470. [[470_hash_sharding_distribution|해시 샤딩 분산 해시 함수]]
471. [[471_consistent_hashing_ring|컨시스턴트 해싱 링 토폴로지]]
472. [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] [[291_ods|구글 스패너]] 글로벌 [[194_consistency_database_integrity|일관성]] 
473. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] [[311_inmon|Inmon]] 전사 통합
474. [[209_data_mart_kimball_star_schema|데이터 마트]] 부서용 [[312_kimball|Kimball]] 상향식
475. [[327_hint_handoff|OLTP]] [[093_normalization|정규화]] [[289_cqrs_db|쓰기]] 위주
476. [[316_olap|OLAP]] 비정규화 읽기 다차원 
477. [[477_star_schema_fact_dimension|스타 스키마 중심 팩트 방사 차원 단일 계층]]
478. [[478_snowflake_schema_normalization|스노우플레이크 차원 정규화 계층 트리]]
479. 드릴 다운 / 롤 업 계층 분석 
480. [[480_slicing_dicing_olap|슬라이스 다이스 차원 절단]]
481. [[481_pivoting_crosstab_report|피벗 크로스탭 보고서]] 
482. [[482_data_lake_schema_on_read|데이터 레이크 스키마 온 리드 원시 형태 저장]] 
483. [[215_etl_vs_elt_pipeline|ETL]] 병목 적재 전 변환 
484. [[034_elt|ELT]] 클라우드 [[209_data_warehouse_schema_on_write|DW]] 적재 후 변환 ([[484_elt_extract_load_transform|성능 우수]]) 
485. [[485_vector_database_embedding|벡터 데이터베이스 임베딩 검색 구조]]
486. [[486_cosine_similarity_search|코사인 유사도 각도 유사 탐색 엔진망 연계]] 
487. [[350_ann|ANN]] [[351_hnsw|HNSW]] [[154_database_index_b_tree_search_optimization|인덱스]] 근사 탐색 구조망 적용 
488. [[276_fine_tuning|RAG]] ([[222_rag_retrieval_augmented_generation|검색 증강 생성]]) 프레임워크 DB 매핑
489. [[489_data_mesh_domain_ownership|데이터 메시 도메인 기반 오너십 분산]] 
490. [[217_cdc_binlog_change_capture_debezium|CDC]] 캡처 변경 [[568_logs_distributed_logging_elk_fluentd|로그]] 추출 스트림 
491. [[001_dikw_pyramid|데이터]] 암호화 [[403_tde_transparent_data_encryption|TDE]] 디스크 [[501_file_definition_logical_record|파일]] 암호망 설계 
492. [[004_blockchain|블록체인]] [[022_smart_contract|스마트 컨트랙트]] 원장 DB 융합 
493. [[035_nosql|NoSQL]] LSM 트리 [[289_cqrs_db|쓰기]] 병합 엔진 구조 분석 
494. [[494_memtable_sstable_flush|멤테이블]] ([[494_memtable_sstable_flush|MemTable]]) 디스크 SStable 플러시
495. [[495_cassandra_gossip_protocol|카산드라 가십 프로토콜 노드 상태 전파]]
496. Quorum 읽기 [[289_cqrs_db|쓰기]] [[194_consistency_database_integrity|일관성]] 보정 정족수 합의 구조 
497. [[300_schema_on_write_vs_read|툼스톤]] 마킹 [[015_지연_데이터_관점|지연]] 삭제 [[035_nosql|NoSQL]] 설계 
498. [[498_dataops_automation_pipeline|데이터 옵스]] ([[324_dataops|DataOps]]) 자동화 [[123_pipe|파이프]]라인
499. ORM 객체 매핑 JPA N+1 질의 문제
500. [[500_inverted_index_elasticsearch|역색인]] ([[500_inverted_index_elasticsearch|Inverted Index]]) 엘라스틱 서치 단어 포인터
501. 스토리지 컴퓨팅 분리 [[531_cloud_native_architecture|클라우드 네이티브]] [[209_data_warehouse_schema_on_write|DW]] 특장점 
502. [[502_dbms|데이터 리니지 흐름 추적 무결성 감사 구조]] 
503. [[503_database_vs_dbms|데이터 거버넌스 품질 메타 카탈로그 통제 관리]] 
504. [[504_data_independence|데이터베이스 백업 핫 덤프 콜드 덤프]] 
505. [[505_schema|트랜잭션 장애 미디어 장애 복구 범위]]
506. [[506_transaction|데이터 디렉터리 시스템 카탈로그 차이]]
507. [[507_acid_properties|트리거]] (Trigger 이벤트 연동 프로시저 콜) 
508. [[508_concurrency_control|프로시저 vs 함수 컴파일 재사용 구조]] 
509. [[509_data_dictionary|클러스터링 팩터 인덱스 효율 평가 지표]]
510. [[510_lock|바인드 변수 적용 하드 파싱 회피]] 
511. [[511_two_phase_locking|옵티마이저 힌트 사용 인덱스 강제 접근]] 
512. [[512_deadlock|반정규화 성능 트레이드오프 파생 컬럼 설계]] 
513. 트리 구조 CTE ([[513_cte_with_recursive_tree|Common Table Expression]]) WITH 절 [[014_recursion|재귀]] 
514. [[514_optimistic_cc|팩트 테이블 차원 모델 비즈니스 수치 저장]] 
515. 시계열 DB 보존 [[164_policy|정책]] ([[515_mvcc|Retention]]) [[001_dikw_pyramid|데이터]] 라이프사이클 
516. [[159_gnn_graph_neural_network_message_passing|GNN]] [[070_graph_datastructure|그래프]] 모델 연계 [[211_recommendation_system|추천 시스템]] 설계망 적용
517. [[517_dark_data_security_control|데이터베이스 보안 다크 데이터 노출 방지 통제]]
518. [[518_data_clean_room_sandboxing|클린 룸 데이터 공유 샌드박싱 연동]] 
519. [[519_aurora_serverless_quorum_replication|서버리스 오로라 스토리지 분산 복제 쿼럼]] 
520. [[342_pacelc|PACELC]] [[136_variance|분산]] DB 장애 평시 트레이드 오프 이론 
521. 동적 SQL 조립 런타임 질의 파서
522. [[522_group_by|데이터 거버넌스 3요소]] (원칙, 조직, 프로세스) 
523. [[523_subquery|정보 공학 방법론 데이터 주도적 생명 주기]]
524. [[089_eer_enhanced_er_model_specialization|EER]] 모델 서브타입 [[234_uml_class_relationships_generalization_dependency|상속]] 특수화 
525. B+Tree [[154_database_index_b_tree_search_optimization|인덱스]] 스플릿 병합 오버헤드 
526. [[174_hash_join|해시 조인]] 탐색 비용 및 메모리([[526_first_normal_form|PGA]]) 스왑 오버헤드 
527. [[527_second_normal_form|정규화의 역설 조인 비용 및 응답 지연 해결망 설계]]
528. [[014_concurrency|동시성]] [[205_dirty_read_uncommitted_dependency|오손 읽기]] ([[528_third_normal_form|Dirty Read]]) 고립 수준 회피 
529. [[230_repeatable_read_isolation_level|Repeatable Read]] 의 팬텀 현상 [[449_mvcc|MVCC]] 해결 유무 
530. [[231_serializable_isolation_level|Serializable]] [[282_performance_tactics|성능]] 저하 임계 영역 데드락 방어 
531. [[136_variance|분산]] 환경 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 블로킹 한계 코디네이터 다운 
532. 3PC [[573_timeout_retry_backoff_strategy|타임아웃]] 우회 비블로킹 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 통신 구조 
533. [[533_event_sourcing_state_stream|이벤트 소싱 상태 변경 스트림 영속 저장망 구성]] 
534. [[305_saga|Saga]] 패턴 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] 비즈니스 실패 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 모사 
535. [[218_nosql_base_eventual_consistency_sharding|NoSQL BASE]] 특성 소프트 [[272_state_pattern|스테이트]] 결국 일관 [[632_state_transition_diagram_testing|상태 전이]] 
536. [[536_shard_key_hotspot_imbalance|샤드 키 불균형 데이터 핫스팟 현상 대처]] 
537. 시계열 DB [[042_rollup_l2_solution|롤업]] 다운샘플링 [[298_qkv_attention|쿼리]] 효율화 
538. [[538_multi_model_database|다중 모델 데이터베이스 융합 조회 연동성]] 
539. [[539_mdm_master_data_management|마스터 데이터]]([[539_mdm_master_data_management|MDM]]) 중복 배제 통합 기준 관리 체계 
540. [[540_mongodb|데이터 가상화 연방 쿼리]] ([[195_federated_query_data_fabric_distributed_join|Federated Query]]) 실행 엔진 
541. 클라우드 [[209_data_warehouse_schema_on_write|DW]] 스노우플레이크([[541_cassandra|Snowflake]]) 구조적 특징 
542. [[542_redis|데이터 마스킹 부분 비식별화 암호화 비교 체계]] 
543. DB [[690_firewall_generation_evolution|방화벽]] [[264_proxy_pattern_surrogate_access_control|프록시]] 스니핑 방식 [[229_monitor|모니터]]링 [[606_auditing_linux_auditd|감사]] 통제 
544. SQL [[480_injection|인젝션]] [[369_logic_bomb|논리]] 에러/타임베이스 블라인드 주입 체계망
545. [[190_secure_coding_guideline|시큐어 코딩]] 파라 파라미터 매핑 ORM 보안 내재화 방식 
546. 공간 [[001_dikw_pyramid|데이터]] [[298_qkv_attention|쿼리]] 기하 연산 [[515_mbr_vs_gpt|MBR]] 근접 분석 기술 구조 
547. [[547_graph_shortest_path_db_mapping|그래프 데이터 최단 경로]]([[547_graph_shortest_path_db_mapping|Shortest Path]]) [[001_algorithm_definition|알고리즘]] DB 매핑 
548. [[548_data_lakehouse_schema_on_read_fusion|데이터 레이크하우스 스키마 온 리드 융합 엔진 구성 기초 분석]] 
549. [[190_ai_llm_requirements_specification|AI]] [[225_foundation_model_peft_lora|파운데이션 모델]] [[276_fine_tuning|RAG]] 패턴 융합 벡터 DB 핵심 아키텍처 
550. [[294_oltp_vs_olap|HTAP]] 기술 [[327_hint_handoff|OLTP]], [[316_olap|OLAP]] 메모리 [[016_replication_factor|복제]]/공유 실시간 아키텍처
551. [[018_mapreduce|맵리듀스]] [[136_variance|분산]] 처리 노드 작업 셔플/소트 단계
552. [[552_consistent_hashing_rebalancing|일관된 해싱 노드 이탈 데이터 리밸런싱 극소화 원리]]
553. [[1019_homomorphic_encryption|동형 암호]] DB 질의 [[282_performance_tactics|성능]] 한계 극복 가속화 연구망 설계 
554. 트리 구조 매핑 Nested Set [[282_performance_tactics|성능]] 검색 비교 Nested Path 모델 
555. 다차원 [[154_database_index_b_tree_search_optimization|인덱스]] K-d 트리 공간/다변량 질의 처리망 [[001_dikw_pyramid|데이터]] 구조 분석 
556. [[556_master_slave_replication_lag_inconsistency|마스터 슬레이브 지연]]([[556_master_slave_replication_lag_inconsistency|Replication Lag]]) 읽기 불일치 이슈 극복망 
557. [[557_multi_master_conflict_last_writer_wins|멀티 마스터 충돌 해결 라스트 라이트 윈]]([[557_multi_master_conflict_last_writer_wins|Last Writer Wins]]) 메커니즘 
558. 벡터 [[001_dikw_pyramid|데이터]] [[350_ann|ANN]] 인덱싱 파라미터(M, efConstruction) [[282_performance_tactics|성능]]/리콜 튜닝 
559. [[559_cosine_similarity_text_embedding_normalization|코사인 유사도 텍스트 임베딩 매칭 정규화 거리 계측 연산 방식]] 
560. [[560_data_fabric_knowledge_graph_intelligent_exploration|데이터 패브릭 지식 그래프 연동 지능형 데이터 탐색 메타 계층]] 
561. 클라우드 DB 고가용성 멀티 AZ 자동 페일오버 ([[300_failover_architecture|Failover]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]] 
562. [[064_b_tree|B-Tree]] 디스크 I/O 최적화 팬아웃 차수 및 노드 크기 블록 매핑 
563. [[563_hash_collision_chaining_linear_probing|해시 충돌]]([[563_hash_collision_chaining_linear_probing|Collision]]) 체이닝 방식 및 선형 탐사 [[282_performance_tactics|성능]] 오버헤드 DB 매핑 
564. [[564_column_storage_run_length_encoding_rle|컬럼 기반 스토리지 런 렝스 인코딩]]([[099_rle|RLE]]) [[347_compaction|압축]] 효율화 탐색 
565. 인 메모리 DB 디스크 [[555_backup_and_restore_strategy|백업]] 체크포인트 방식 [[015_지연_데이터_관점|지연]] [[282_performance_tactics|성능]] 최소화 아키텍처
566. [[566_cache_stampede_mutex_probabilistic_early_expiration|캐시 스탬피드 뮤텍스 락 및 확률적 갱신]]([[566_cache_stampede_mutex_probabilistic_early_expiration|Probabilistic Early Expiration]]) 회피기법 
567. [[567_redis_cache_eviction_policy_lru_lfu|레디스 만료 데이터 키 삭제 정책]]([[262_lru_page_replacement|LRU]], [[263_lfu_page_replacement|LFU]], Random) 캐시 스토리지 운영 
568. 몽고DB [[280_sharding|샤딩]] 청크 마이그레이션 백그라운드 밸런싱 모형 분석망 
569. [[569_cassandra_write_path_commitlog_memtable_sstable|카산드라 쓰기 경로]](Commit Log -> [[494_memtable_sstable_flush|Memtable]] -> SSTable) 병목 배제 모델 
570. [[211_hadoop_ecosystem_mapreduce|하둡 에코시스템]] [[544_hive|Hive]], Pig [[136_variance|분산]] DB 질의 [[298_qkv_attention|쿼리]] 엔진 [[018_mapreduce|맵리듀스]] [[198_abstraction_control_data_process|추상화]] 
571. Spark 스트리밍 마이크로 배치 vs Flink 네이티브 스트림 인 메모리 DB 
572. [[572_dataops_automated_testing_canary_deployment|데이터 옵스 자동화 테스트 카나리 배포 데이터 파이프라인 검증망 설계]] 
573. [[291_ods|ODS]] 준실시간 [[022_snapshot_backup_architecture|스냅샷]] 레코드 마이그레이션 [[209_data_warehouse_schema_on_write|DW]] 배치 레이어 차이점 
574. [[574_conformed_dimension|데이터 마트 콘포밍 차원]] ([[574_conformed_dimension|Conformed Dimension]]) 킴볼 [[344_bus|버스]] 구조 
575. [[575_scd_slowly_changing_dimension_type_history_management|Slowly Changing Dimension]] ([[277_scd_slowly_changing_dimension_modeling|SCD]] Type 1, 2, 3) 시계열 이력 차원 이력 관리 모델 
576. [[576_factless_fact_table_event_tracking_coverage|팩트리스 팩트 테이블]] ([[576_factless_fact_table_event_tracking_coverage|Factless Fact Table]]) 이벤트 추적 차원 교차망 모델 
577. [[577_many_to_many_resolution_intersection_entity|다대다 관계 해소 교차 릴레이션]] (Intersection Entity / [[010_schema_mapping|Mapping]] Table) 분해 
578. 수퍼타입/서브타입 [[001_dikw_pyramid|데이터]] 물리 변환 1:1 병합 테이블 최적 접근 모델 
579. [[003_integrity|무결성]] 제약 조건 CASCADE, RESTRICT, SET NULL 연쇄 업데이트 삭제 [[009_config|설정]]
580. [[076_domain_integrity|도메인 무결성]] CHECK 구문 [[104_regex|정규 표현식]] 입력 통제 규칙 
581. [[581_tablespace_system_capacity_management_datafiles|테이블 스페이스 시스템 용량 분산 관리 물리 파일 그룹핑 구성 정책]] 
582. [[582_dynamic_performance_views_v_dollar_dmv_monitoring|동적 성능 뷰]] (V$, DMV) [[025_dba_database_administrator|DBA]] [[229_monitor|모니터]]링 병목 락 트레이싱 [[282_performance_tactics|성능]] 지표 [[396_validation|확인]]망 
583. [[583_parameter_sniffing_execution_plan_cache_pollution|프로시저 플랜 캐시 스니핑]] ([[583_parameter_sniffing_execution_plan_cache_pollution|Parameter Sniffing]]) 캐시 오염 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 악화 
584. 윈도우 함수 ROWS BETWEEN 누적 합계 구간 이동 평균 연산 [[514_partition_slice_volume|파티션]] 
585. [[585_subquery_unnesting_optimizer_query_transformation|서브쿼리 언네스팅]] ([[585_subquery_unnesting_optimizer_query_transformation|Subquery Unnesting]]) 메인 [[298_qkv_attention|쿼리]] 조인 변환 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 룰 
586. [[586_join_predicate_pushdown_view_query_transformation|푸시 다운 조인 프레디케이트]] ([[586_join_predicate_pushdown_view_query_transformation|Join Predicate Pushdown]]) 뷰 연산 [[298_qkv_attention|쿼리]] 변환 
587. [[587_star_transformation_fact_dimension_bitmap_index|스타 변환]] ([[587_star_transformation_fact_dimension_bitmap_index|Star Transformation]]) 팩트/차원 조인 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 스캔 효율화 기법 
588. [[588_distributed_transaction_coordinator_dtc_2pc|분산 트랜잭션 코디네이터]] ([[588_distributed_transaction_coordinator_dtc_2pc|DTC]]) 미들웨어 애플리케이션 [[191_transaction_concept_states|트랜잭션]] 연합 
589. [[589_lamport_clock_vector_timestamp|람포트 시계 논리적 이벤트 순서 선후 관계 인과 보장 분산 벡터 타임스탬프]] 
590. [[590_google_truetime_clock_skew|클럭 스큐 구글 트루타임 원자 시계 오차 범위 대기 분산 노드 일관성 통제]] 
591. [[591_mvcc_garbage_collection_vacuum|가비지 컬렉터]] ([[449_mvcc|MVCC]] [[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]] 블록 회수 진공 프로세스 Vacuum) [[001_dikw_pyramid|데이터]] 정리 
592. ACID [[191_transaction_concept_states|트랜잭션]] 섀도우 [[259_paging|페이징]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] 속도 최적 디스크 I/O 절감 [[002_database_definition|데이터베이스]] 구조 
593. ARIES [[658_ir_recovery|복구]] [[001_algorithm_definition|알고리즘]] 생존자 Analysis [[234_redo_roll_forward_durability_recovery|Redo]] [[393_undo|Undo]] 3페이즈 시스템 [[658_ir_recovery|복구]] 표준 원리 
594. WAL [[568_logs_distributed_logging_elk_fluentd|로그]] 플러시 [[244_lsn_log_sequence_number_recovery_tracking|LSN]] 기반 체크포인트 미디어 장애 [[001_dikw_pyramid|데이터]] 롤 포워드 [[003_integrity|무결성]] 체재 
595. [[058_data_literacy|데이터 리터러시]] ([[058_data_literacy|Data Literacy]]) 기업 내 [[001_dikw_pyramid|데이터]] 분석 역량 도구 지식 기반 문화 확산 
596. [[596_data_discovery_catalog|데이터 디스커버리 카탈로그 플랫폼 검색 큐레이션 거버넌스 워크플로우 지식 저장]] 
597. [[781_personal_information|개인정보]] 비식별 조치 K-익명성 [[815_l_diversity|l-다양성]] [[816_t_closeness|t-근접성]] 프라이버시 [[001_dikw_pyramid|데이터]] 보존 평가 기준 
598. 정보보안 암호화 DB [[192_module_independence|모듈]] ([[014_api_posix|API]]/Plug-in/[[403_tde_transparent_data_encryption|TDE]]) 혼합 구성 인프라망 구조 체계 검토 
599. [[599_graph_mining|그래프 마이닝 네트워크 라우팅 추천 엔진 사기 탐지 소셜 연결 데이터 연산]] 
600. [[236_quantum_computing_pqc|양자 컴퓨팅]] 대응 포스트 퀀텀 암호화 DB [[191_transaction_concept_states|트랜잭션]] 서명 보안 체계 적용 방안 연구 동향

---
**총정리 [[002_database_definition|데이터베이스]] 키워드 : 총 800개 수록** (+파생/분석 확장 시 1,000여 개 커버)
(RDBMS 기초([[093_normalization|정규화]], SQL, [[154_database_index_b_tree_search_optimization|인덱스]], [[191_transaction_concept_states|트랜잭션]], [[658_ir_recovery|복구]])부터 [[035_nosql|NoSQL]], [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]], [[136_variance|분산]] DB 아키텍처, [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]]), 그리고 최신 벡터 DB, [[294_oltp_vs_olap|HTAP]], [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]에 이르는 전 영역을 깊이 있게 총망라하였습니다.)