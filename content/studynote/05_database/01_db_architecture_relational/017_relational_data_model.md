+++
title = "17. 관계형 데이터 모델 (Relational Model) - 테이블 구조, E.F. Codd 제안"
description = "E.F. Codd가 제안한 테이블 구조 기반의 수학적 논리 데이터 모델"
date = 2026-03-04

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# 17. [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) (Relational [Data Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 1970년 E.F. Codd가 제안한 수학적 집합론과 술어 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)(Predicate Logic)에 기반하여 2차원 테이블([Relation](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)) 형태로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 표현하는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)이다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조와 물리적 저장 구조를 완전히 분리([데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/))하여, 애플리케이션 코드를 수정하지 않고도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 변경할 수 있는 획기적인 유연성을 제공한다.
> 3. **융합**: 집합 연산을 수행하는 [관계 대수](/knowledge-base/studynote/05_database/01_db_architecture_relational/038_relational_algebra/)([Relational Algebra](/knowledge-base/studynote/05_database/01_db_architecture_relational/038_relational_algebra/))와 [관계 해석](/knowledge-base/studynote/05_database/07_exam_summary/410_relational_calculus/)([Relational Calculus](/knowledge-base/studynote/05_database/01_db_architecture_relational/045_relational_calculus/))을 바탕으로 SQL 엔진의 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 최적화하는 이론적 토대가 된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) (Relational [Data Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/))은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 역사상 가장 성공적이고 지배적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표현 방식이다. 1960년대까지 주류를 이루던 계층형(Hierarchical) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 망형(Network) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 애플리케이션이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 저장 경로를 정확히 알아야만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 탐색(Navigation)할 수 있는 치명적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Dependency) 문제를 안고 있었다. 이러한 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 시스템 확장을 어렵게 만들고 유지보수 비용을 기하급수적으로 증가시켰다.

이를 해결하기 위해 E.F. Codd 박사는 수학의 '집합론(Set Theory)'을 도입하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 뷰와 물리적 저장을 완벽히 분리하는 혁신적인 패러다임을 제안했다. [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델에서는 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)(Tuple, 행)과 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/), 열)으로 이루어진 '[릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)([Relation](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/))'이라는 단순하고 직관적인 2차원 표 형태로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)한다. 사용자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 '어디에' '어떻게' 저장되어 있는지 알 필요 없이, '무엇을' 원하는지만 선언적으로 요구(SQL)하면 된다. 현재 비즈니스 환경에서 요구하는 엄격한 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) 유지와 복잡한 다차원 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 분석은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델의 수학적 엄밀성이 없었다면 불가능했을 것이다.

다음 다이어그램은 과거 네비게이션 방식의 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 선언적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)의 근본적인 접근 방식 차이를 보여준다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색의 주체가 누구인지 비교해보자.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">계층/망형 모델 (Navigation)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">App → "A 찾고, 그 포인터 따라가서 B 찾고..." → Data</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 물리적 링크(Pointer) 변경 시 App 코드 전면 수정 필수</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">관계형 모델 (Declarative)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">App → "A와 B가 조건에 맞는 것 줘 (SQL)" → DBMS가 찾음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 논리적 구조만 참조하므로 물리적 저장 구조 변경 자유</div></div>
</div>
</div>



이 도식의 핵심은 애플리케이션과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 강한 결합([Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))을 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델의 DBMS가 어떻게 끊어내었는가이다. 과거 모델은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인터를 애플리케이션이 직접 추적해야 했기에 물리적 구조 변경이 곧 시스템 장애로 직결되었다. 반면, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델은 집합 연산에 기반한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진을 중간에 두어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 선언적으로 요구할 수 있게 하였다. 따라서 스토리지 최적화나 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 추가와 같은 물리적 변경이 애플리케이션 수명주기에 영향을 주지 않으며, 이는 엔터프라이즈 시스템의 장기적인 안정성과 확장성을 담보하는 결정적 요인이 된다. 실무에서는 이러한 특징 덕분에 백엔드 개발자가 스토리지 블록의 배치 상태를 몰라도 복잡한 비즈니스 로직을 구현할 수 있다.

📢 **섹션 요약 비유**: 마치 과거에는 목적지까지 골목길을 일일이 외워서 운전해야 했다면(네비게이션), [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델은 목적지만 입력하면 내비게이션 시스템이 최적의 경로를 알아서 찾아주는(선언적) 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)([Relation](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)), [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)), [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)(Tuple), [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))이라는 핵심 구성 요소로 이루어지며, 이를 바탕으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 보장하기 위한 제약조건(Constraints)과 연산(Operations) 규칙을 갖는다.

| 구성 요소 | 역할 | 내부 동작/특성 | 대응되는 SQL 개념 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/">Relation</a></strong> ([릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)) | 엔티티 집합 표현 | [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)의 무순서성 보장, 중복 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/) 불허 | Table (테이블) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 한 시트 |
| **Tuple** ([튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)) | 개별 엔티티 인스턴스 | 각 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)값의 모음, 유일성 가짐 | Row (행, 레코드) | 시트의 한 줄 |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">Attribute</a></strong> ([속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) | 엔티티의 특성 정의 | [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)(Atomic) 보장, [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 간 무순서 | Column (열, 필드) | 시트의 항목(헤더) |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a></strong> ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)) | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 값의 허용 범위 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 및 유효 범위 제약 | Type & Check 제약 | 셀의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규칙 |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a></strong> (키) | [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)의 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 및 연관성 | 유일성과 최소성을 통한 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 역할 | PK, FK, UK | 주민등록번호 |

[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델은 단순히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 표에 담는 것이 아니라, 이 표가 수학적 '집합'으로서의 성질을 만족하도록 강제한다. 이는 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)의 무순서성(집합의 원소는 순서가 없다)과 중복 불허(집합에는 동일 원소가 존재하지 않는다)로 나타난다.

아래 다이어그램은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)의 구조적 레이아웃과 제약조건이 어떻게 상호작용하는지를 시각적으로 보여준다. 기본키(PK)와 외래키(FK)의 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하자.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Relation: EMP (사원)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Attribute(도메인)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">EMP_ID(Int)</div><div class="kb-diagram-cell">ENAME(VarChar)</div><div class="kb-diagram-cell">DEPT_ID(Int)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">100</div><div class="kb-diagram-cell">Alice</div><div class="kb-diagram-cell">10 (FK) ──</div><div class="kb-diagram-cell">← Tuple 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">101</div><div class="kb-diagram-cell">Bob</div><div class="kb-diagram-cell">20 (FK) ── ─</div><div class="kb-diagram-cell">← Tuple 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">102</div><div class="kb-diagram-cell">Charlie</div><div class="kb-diagram-cell">10 (FK) ──</div><div class="kb-diagram-cell">← Tuple 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(기본키 무결성)</div><div class="kb-diagram-cell">(참조 무결성)</div></div>
<div class="kb-diagram-note">Relation: DEPT (부서)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DEPT_ID(Int)</div><div class="kb-diagram-cell">DNAME(VarChar)</div><div class="kb-diagram-cell">LOCATION(VarChar)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">10 (PK)</div><div class="kb-diagram-cell">Sales</div><div class="kb-diagram-cell">Seoul</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">20 (PK)</div><div class="kb-diagram-cell">R&amp;D</div><div class="kb-diagram-cell">Busan</div></div>
</div>
</div>



이 구조도의 핵심은 두 개의 독립된 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)이 <strong>값(Value)</strong>을 통해서만 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 연결된다는 점이다. 물리적인 포인터나 주소값이 아니라, `DEPT_ID`라는 외래키(Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 값을 통해 개체 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 맺는다. 이는 [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)([Referential Integrity](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)) 제약을 발생시키며, 자식 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)([EMP](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/931_emp_shielding/))에 있는 `DEPT_ID` 값은 반드시 부모 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)(DEPT)에 존재해야 한다는 강력한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 규칙을 엔진 차원에서 강제한다. 따라서 개발자가 애플리케이션 단에서 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 로직의 오류를 범하더라도, [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 엔진이 잘못된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 삽입이나 삭제를 원천적으로 차단하여 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 지켜낸다. 실무에서는 이 FK 제약조건이 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)에는 좋지만, 대량 [DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_dml/) 작업 시 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하의 주범이 되기도 하므로 트레이드오프를 고려해야 한다.

📢 **섹션 요약 비유**: 마치 레고 블록 자체에 돌기와 홈(키와 제약조건)이 정확한 규격으로 정해져 있어서, 설명서 없이 조립해도 구조물이 무너지지 않고 견고하게 맞물리는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 이후 등장한 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/), [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 명확한 철학적 차이를 갖는다. 이들의 차이는 단순히 저장 방식이 아니라 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 확장성에 대한 아키텍처적 선택에 기인한다.

| 비교 항목 | RDBMS ([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)) | [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) (문서형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)) | 판단 포인트 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 구조</strong> | 엄격한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 테이블 구조 ([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 유연한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON 형태 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포맷의 가변성 유무 |
| <strong>조인 (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a>)</strong> | 탁월함, 복잡한 다차원 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색 유리 | 조인 회피, [역정규화](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) 선호 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색의 복잡도 수준 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 보장</strong> | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 완벽 지원) | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) (BASE, [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 이론) | 결제의 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) vs 트래픽 수용 |
| **확장성** | 수직적 확장([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 중심 | 수평적 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 용이 | 시스템의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장 요구사항 |

[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 최소화하지만, 이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조회 시 여러 테이블을 조인해야 하는 연산 오버헤드를 발생시킨다. 반면 NoSQL은 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 의도적으로 중복([Denormalization](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/))을 허용한다.

아래 다이어그램은 RDBMS와 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 환경에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽어오는 과정의 아키텍처적 트레이드오프를 비교한 것이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">RDBMS: 정규화 구조의 읽기 병목</div></div>
<div class="kb-diagram-note">Order_Tb ──(Join)── User_Tb ──(Join)── Product_Tb</div>
<div class="kb-diagram-tree-item" style="--depth:1">복수의 디스크 블록 접근 + 조인 버퍼/해시 연산 발생 =&gt; CPU/Mem 부하</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">NoSQL (Document): 비정규화 구조의 쓰기 병목</div></div>
<div class="kb-diagram-note">Order_Doc { UserInfo: {}, ProductInfo: [] }</div>
<div class="kb-diagram-tree-item" style="--depth:1">단일 디스크 블록 조회 완료 =&gt; 초고속 읽기</div>
<div class="kb-diagram-tree-item" style="--depth:1">단, UserInfo 변경 시 모든 관련 주문 문서 업데이트 필요 =&gt; 쓰기/일관성 지연</div>
</div>
</div>



이 비교 매트릭스와 구조도의 핵심은 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)에 따른 워크로드(Workload)의 최적화 방향성이 완전히 다르다는 것이다. RDBMS는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중복을 없애 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 극한으로 올렸지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조립하는 과정([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))에서 막대한 CPU와 메모리([PGA](/knowledge-base/studynote/05_database/04_transactions_concurrency/526_first_normal_form/)) 자원을 소모한다. 반면 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 문서 모델은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 이미 조립된 채로 저장하여 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 최소화하지만, 상태 변경 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 실패 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 감수해야 한다. 실무에서는 금융, 회계 등 강한 정합성이 필요한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)(ACID)은 RDBMS를, 게임 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)나 쇼핑몰 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)처럼 읽기 중심의 대규모 트래픽 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)(BASE)은 NoSQL을 채택하는 [폴리글랏 퍼시스턴스](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/)) 아키텍처가 표준으로 자리잡았다.

📢 **섹션 요약 비유**: RDBMS가 부품을 체계적으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 둔 창고에서 주문이 올 때마다 로봇이 빠르게 조립(조인)하는 방식이라면, NoSQL은 이미 완성된 완제품을 진열대에 올려두고 주문 즉시 꺼내주는 방식과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)을 실무 시스템에 적용할 때 가장 중요한 것은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 모델링과 물리적 구현 사이의 간극을 조율하는 것이다. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 이론에만 집착하면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 무너지고, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만 좇으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쓰레기([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))가 양산된다.

1. <strong>실무 시나리오: <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>의 역설과 반정규화 결단</strong>
   - **상황**: 3NF까지 완벽하게 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 쇼핑몰 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/). 사용자의 주문 내역 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 띄우기 위해 7개의 테이블을 엮는 조인이 발생하여 평균 응답 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 3초를 초과함.
   - **판단**: 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확보를 위해 의도적으로 테이블을 합치거나 파생 컬럼을 추가하는 반정규화(De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 수행. 예컨대 '총 결제 금액'을 주문 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 테이블에 중복 저장. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 위험은 애플리케이션 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이나 DB [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)를 통해 강제로 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/).
2. <strong>도입 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a>: 외래키(FK) 제약조건 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 여부</strong>
   - [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) ERD에는 명확한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 존재하더라도, [물리 데이터베이스 설계](/knowledge-base/studynote/05_database/02_modeling_normalization/117_physical_database_design_indexing/) 시 초대용량 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 테이블 간에는 FK [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 생략하는 패턴이 많다.
   - FK를 활성화하면 INSERT/UPDATE 시 부모 테이블 락(Shared [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 유발하여 데드락([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))과 TPS 저하의 원인이 되기 때문. 정합성은 배치(Batch) 잡이나 애플리케이션 레벨의 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 우회한다.

아래 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)는 실무에서 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델을 언제 반정규화(De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))하거나 대안 모델로 넘어가야 할지 결정하는 플로우를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">요구사항 발생</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">(Q1. 트랜잭션 무결성이 절대적인가?) ── 아니오 ──&gt;</div><div class="kb-diagram-node">NoSQL 도입 고려</div></div>
<div class="kb-diagram-note">↓ 예</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">(Q2. 조인 시 조회 성능 지연이 심각한가?) ── 아니오 ──&gt;</div><div class="kb-diagram-node">정규화 RDB 유지</div></div>
<div class="kb-diagram-note">↓ 예</div>
<div class="kb-diagram-note">(Q3. 실시간 쓰기가 자주 발생하는가?)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 예 &gt;</div><div class="kb-diagram-node">데이터마트 분리(CQRS) / 읽기전용 DB 복제</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ 아니오 ──&gt;</div><div class="kb-diagram-node">뷰 머티리얼라이즈(MVIEW) 또는 과감한 반정규화 적용</div></div>
</div>
</div>



이 의사결정 흐름의 핵심은 '조인 비용'과 '[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 비용' 사이의 저울질이다. 조인 때문에 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 느리다고 무작정 반정규화를 하면, 후속 [DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_dml/)(업데이트) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모두 수정하느라 치명적인 DB 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합을 발생시킨다. 따라서 실시간 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 빈번한 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 환경이라면 테이블을 뭉개는 반정규화보다는 [Command Query Responsibility Segregation](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/) ([CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)) 아키텍처를 통해 조회 전용 DB를 분리하는 것이 구조적으로 안전하다. 기술사 및 아키텍트는 이론적 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 함정에 빠지지 않고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 생명 주기(읽기 vs [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비율)를 정량적으로 분석하여 물리 설계를 타협할 줄 알아야 한다.

📢 **섹션 요약 비유**: 영양학적으로 완벽한 식단([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))이라도 소화 불량([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하)을 일으킨다면, 때로는 소화가 빠른 다이어트 쉐이크(반정규화)를 섞어 먹는 유연한 처방이 필요한 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 지난 반세기 동안 엔터프라이즈 시스템의 심장 역할을 해왔으며, 그 수학적 견고함은 앞으로도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 요구되는 모든 비즈니스의 표준으로 남을 것이다. 최근에는 단순한 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 처리를 넘어, [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) (Hybrid Transactional/Analytical Processing) 아키텍처를 통해 하나의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델 내에서 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 실시간 다차원 분석을 동시에 처리하는 방향으로 진화하고 있다.

| 구분 | 도입 전 ([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템/네비게이션 모델) | 도입 후 ([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)) |
|:---|:---|:---|
| **개발 생산성** | 물리 경로 탐색 코드 작성 (고비용) | SQL 선언적 질의 (저비용, 고속) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong> | 애플리케이션 로직에 의존 | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 차원의 완벽한 제약조건 강제 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/">유지보수성</a></strong> | 스토리지 변경 시 앱 재배포 필수 | [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) 확보로 무중단 변경 가능 |

결론적으로 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 통한 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 순수성'을 확보하는 가장 강력한 프레임워크다. 클라우드 시대에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB의 부상으로 RDBMS의 한계가 지적되기도 했으나, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서도 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델을 보장하는 [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/)(Google Spanner, [CockroachDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/292_etl_process/) 등)의 등장으로 인해 그 위상은 오히려 더 굳건해지고 있다.

📢 **섹션 요약 비유**: 튼튼한 철근 콘크리트 골조([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델)로 지어진 빌딩은 그 위에 어떤 현대적인 인테리어(클라우드, [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))를 입히든 흔들리지 않는 굳건한 기반을 제공하는 것과 같습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* **SQL (Structured Query Language)** | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델의 집합 연산을 구현하여 사용자와 DBMS를 이어주는 선언적 질의 표준 언어
* <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a> (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">Normalization</a>)</strong> | [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 제거하고 삽입, 삭제, [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/) 현상을 방지하는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 설계 기법
* <strong>ACID <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a></strong> | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 물리적으로 보장하기 위해 지원하는 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [격리성](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 특성
* <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/038_relational_algebra/">관계 대수</a> (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/038_relational_algebra/">Relational Algebra</a>)</strong> | [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 조작하여 새로운 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 절차적 수학 연산 (선택, 투영, 조인 등)
* <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/">NewSQL</a></strong> | NoSQL의 수평적 확장성([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)의 ACID/SQL 특성을 결합한 차세대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">계층형 / 망형 모델 (Hierarchical / Network Model) — 포인터 기반, 물리적 구조 의존</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">관계형 데이터 모델 (Relational Model) — E.F. Codd 제안, 수학적 집합·릴레이션</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SQL (Structured Query Language) — 선언적 질의, 데이터 독립성 실현</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">정규화 (Normalization) — 함수 종속 제거, 이상 현상 방지, 설계 표준화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">ACID 트랜잭션 — 원자성·일관성·격리성·지속성으로 데이터 무결성 보장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">NewSQL / HTAP — 관계형 의미론 유지하며 수평 확장·실시간 분석 지원</div></div>
</div>
</div>


이 흐름은 물리적 포인터 구조에 얽매이던 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) DB 모델이 수학적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 이론으로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)되고, SQL 표준을 거쳐 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)·실시간 처리 요건을 수용하는 현대 DBMS로 진화하는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기술의 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 서랍장([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))에 물건을 마구 쑤셔 넣으면 나중에 찾기 너무 힘들죠?
2. [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 물건을 엑셀 표(테이블)처럼 '이름', '종류', '위치' 칸에 맞춰 아주 깔끔하게 정리하는 완벽한 규칙이에요.
3. 이렇게 표끼리 서로 연결(조인)해두면, 아무리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수백만 개로 많아져도 원하는 정보를 1초 만에 쏙 뽑아낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 17 / 600

← **이전**: [16. 망형 데이터 모델 (Network Model) - 그래프 구조 (N:M 허용)](/knowledge-base/studynote/05_database/01_db_architecture_relational/016_network_data_model/)
**다음**: [18. 객체지향 데이터 모델 (OODBMS) / 객체 관계형 데이터 모델 (ORDBMS)](/knowledge-base/studynote/05_database/01_db_architecture_relational/018_object_oriented_relational_data_model/) →

---
