+++
weight = 8
title = "8. 개념 스키마 (Conceptual Schema) - 조직 전체 관점, 논리적 구조"
description = "조직 전체 관점의 논리적 데이터베이스 구조와 전사 데이터 모델링 원리"
date = "2024-05-20"
[taxonomies]
tags = ["Database", "Schema", "Conceptual Schema", "ANSI-SPARC", "Data Modeling"]
categories = ["studynote-database"]
+++

# 개념 [[005_schema|스키마]] (Conceptual [[505_schema|Schema]])
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 조직 전체의 관점에서 [[002_database_definition|데이터베이스]]에 어떤 [[001_dikw_pyramid|데이터]]가 저장되어 있고, 이들 간의 [[083_relationship_in_er_model|관계]]와 [[003_integrity|무결성]] 규칙이 무엇인지 정의하는 전사적 [[369_logic_bomb|논리]] 구조입니다.
> 2. **가치**: [[007_external_schema|외부 스키마]]와 [[009_internal_schema|내부 스키마]] 사이의 '단단한 중심축' 역할을 수행하여 [[001_dikw_pyramid|데이터]]의 [[194_consistency_database_integrity|일관성]]을 강제하고, 물리적 환경 변화로부터 애플리케이션을 [[571_protection_vs_security|보호]]합니다.
> 3. **융합**: ER(Entity-[[083_relationship_in_er_model|Relationship]]) 모델링, [[310_architecture|도메인 주도 설계]]([[310_architecture|DDD]])의 애그리거트([[222_aggregate_ddd_transaction_consistency|Aggregate]]) 정의 등과 맥락을 같이하는 [[291_information_architecture|정보 아키텍처]]의 심장입니다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)
개념 [[005_schema|스키마]] (Conceptual [[505_schema|Schema]])는 전체 사용자나 응용 프로그램이 요구하는 모든 [[001_dikw_pyramid|데이터]]를 통합한 조직 전체의 [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 구조를 의미합니다. 단순히 '[[002_database_definition|데이터베이스]]'라고 일컬을 때 대부분 이 개념 [[005_schema|스키마]]를 지칭합니다. [[459_quic_fec_forward_error_correction|초기]] 정보 시스템은 각 부서가 독립적인 [[501_file_definition_logical_record|파일]] 구조를 유지함에 따라 [[001_dikw_pyramid|데이터]] 중복과 불일치 현상([[530_anomaly|Anomaly]])이 극심했습니다. 
이러한 혼란을 해결하기 위해 ANSI/SPARC 구조는 조직 내 모든 [[001_dikw_pyramid|데이터]] 개체, [[082_attribute_types_er_model|속성]], [[083_relationship_in_er_model|관계]], [[073_integrity_constraints_overview|무결성 제약조건]]을 단 하나의 중앙 집중적 구조로 통합하는 개념 [[005_schema|스키마]]를 제안했습니다. 이를 통해 모든 외부 시스템은 오직 일관된 단일 진실 공급원([[119_gitops_single_source_of_truth|Single Source of Truth]])을 바라보게 되며, 관리자([[025_dba_database_administrator|DBA]])는 [[001_dikw_pyramid|데이터]]의 [[369_logic_bomb|논리]]적 구조를 전사 차원에서 통제할 수 있게 되었습니다.

아래 그림은 다수의 [[007_external_schema|외부 스키마]]와 물리적 [[009_internal_schema|내부 스키마]] 사이에서 중심을 잡아주는 개념 [[005_schema|스키마]]의 위치를 보여줍니다.
```text
[External Level]  View A    View B    View C  (사용자 맞춤형 논리 구조)
                     \        |        /
                      \       |       /  <-- (외부/개념 사상)
[Conceptual Level] ┌─────────────────────┐
                   │ 개념 스키마 (통합)  │ (전사적 논리 구조, ERD, 제약조건)
                   └─────────────────────┘
                              |          <-- (개념/내부 사상)
[Internal Level]   [ 내부 스키마 (인덱스, 스토리지) ]
```
이 도식의 핵심은 개념 [[005_schema|스키마]]가 병목([[617_io_bottleneck|Bottleneck]])이자 동시에 든든한 뼈대(Spine)로 작용한다는 점입니다. 위에 위치한 뷰([[151_sql_view_virtual_table|View]])가 수십 개 추가되거나 아래의 디스크 볼륨이 수차례 교체되더라도, 가운데 위치한 개념 [[005_schema|스키마]]의 [[003_integrity|무결성]] 규칙은 흔들림 없이 유지됩니다. 실무에서는 이 영역의 설계가 한 번 잘못되면 파급 효과가 시스템 전체로 퍼지기 때문에, [[001_dikw_pyramid|데이터]] 아키텍트([[104_da_as_is_analysis|DA]])가 가장 신중하게 설계하는 영역입니다.

📢 **섹션 요약 비유**: 수많은 부서([[007_external_schema|외부 스키마]])의 요청을 종합하여 만든 회사의 통합 조직도 및 업무 규정집(개념 [[005_schema|스키마]])과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
개념 [[005_schema|스키마]]는 [[002_database_definition|데이터베이스]] 내부에 저장된 단순한 테이블 목록을 넘어, [[001_dikw_pyramid|데이터]]의 본질적 의미와 규칙을 코드로 강제합니다.

| 구성 요소 | 역할 | 내부 동작 | 구현 요소 | 비유 |
|:---|:---|:---|:---|:---|
| **Entities (개체)** | 관리 대상 정의 | 독립적인 [[082_attribute_types_er_model|속성]]을 가진 [[655_ir_detection_analysis|식별]] 가능한 실체 구축 | Base Tables | 명사 (사물) |
| **[[502_file_attributes_metadata|Attributes]] ([[082_attribute_types_er_model|속성]])** | 개체의 성질 정의 | [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]], [[001_dikw_pyramid|데이터]] 타입, 크기 결정 | Columns, [[001_dikw_pyramid|Data]] Types | 형용사 (특성) |
| **Relationships ([[083_relationship_in_er_model|관계]])** | 개체 간의 연관성 | 1:1, 1:N, M:N의 [[316_reference_pattern_nosql|참조]] [[083_relationship_in_er_model|관계]] [[009_config|설정]] | Primary/Foreign Keys | 동사 (행위) |
| **Constraints (제약조건)** | [[001_dikw_pyramid|데이터]] [[442_consistency_integrity|무결성 보장]] | [[076_domain_integrity|도메인 무결성]], [[075_referential_integrity_foreign_key_cascade|참조 무결성]], [[074_entity_integrity_primary_key|개체 무결성]] 강제 | CHECK, UNIQUE, NOT NULL | 교통 법규 |
| **[[283_security_tactics|Security]]/Auth** | 전사적 접근 [[164_policy|정책]] | 개념 레벨의 롤(Role) 및 [[509_authorization_models_rbac_abac|인가]]([[509_authorization_models_rbac_abac|Authorization]]) 기준 | [[022_dcl|DCL]] (GRANT) | 사규 |

개념적 [[014_data_model_components|데이터 모델]](ERD)이 [[391_relation_schema_intension|릴레이션 스키마]]로 변환되어 적용되는 흐름은 다음과 같습니다.
```text
[요구사항 분석] 전사 업무 프로세스 도출
   ↓
[개념적 모델링] ER 다이어그램 (개체, 관계 식별)
   ↓
[논리적 모델링] 릴레이션 변환 및 정규화 (1NF -> 2NF -> 3NF)
   => EMPLOYEE(emp_id PK, dept_id FK, name)
   ↓
[DDL 생성] CREATE TABLE 문 작성 (개념 스키마 구체화)
   ↓
[무결성 검사] 데이터 딕셔너리 등록 및 Constraints 활성화
```
이 흐름의 핵심은 물리적 스토리지 [[282_performance_tactics|성능]]이나 화면 UI를 전혀 고려하지 않고, 오직 '[[001_dikw_pyramid|데이터]] [[008_dependencies|종속성]] 제거'와 '비즈니스 규칙 반영'에만 집중한다는 점입니다. 이 단계에서 수행되는 [[093_normalization|정규화]]([[093_normalization|Normalization]])는 중복 [[001_dikw_pyramid|데이터]]를 제거하여 [[090_anomaly_insertion_deletion_update|이상 현상]]([[530_anomaly|Anomaly]])을 방지하는 핵심 엔진입니다. 실무에서 [[061_relation_schema_instance|릴레이션]] 간의 M:N([[100_many_to_many_model|다대다]]) [[083_relationship_in_er_model|관계]]를 해소하지 않고 개념 [[005_schema|스키마]]를 구성하면, 추후 조인([[521_join|Join]]) 연산에서 치명적인 [[412_cartesian_product|카티션 프로덕트]]([[412_cartesian_product|Cartesian Product]])가 발생합니다.

📢 **섹션 요약 비유**: 건물을 올리기 전, 하중과 구조적 안정성, 각 방의 연결 동선을 완벽하게 계산해 놓은 [[172_maas_mobility_as_a_service|마스]]터 건축 설계도와 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
개념 [[005_schema|스키마]]의 역할은 [[369_logic_bomb|논리]]적/물리적 관점 모델링 방식과 대조할 때 명확해집니다.

| 비교 항목 | [[369_logic_bomb|논리]] 모델링 (개념 [[005_schema|스키마]] 관점) | 물리 모델링 ([[009_internal_schema|내부 스키마]] 관점) | 판단 기준 |
|:---|:---|:---|:---|
| **주요 목표** | [[546_data_deduplication|데이터 중복 제거]], [[442_consistency_integrity|무결성 보장]] | [[138_response_time|응답 시간]] 단축, 스토리지 효율화 | **최우선 가치** |
| **주요 기법** | [[093_normalization|정규화]]([[093_normalization|Normalization]]) | 반정규화(De-[[093_normalization|normalization]]), 인덱싱 | **설계 방향** |
| **DB [[008_dependencies|종속성]]** | 특정 [[502_dbms|DBMS]] 제품에 독립적 (RDB 공통) | [[188_pl_sql_t_sql_procedural|Oracle]], MySQL 등 엔진 구조에 강하게 종속 | **이식성** |
| **결과물** | ERD, [[391_relation_schema_intension|릴레이션 스키마]], [[020_ddl|DDL]] 구조 | 테이블스페이스, [[179_table_partitioning_concept|파티셔닝]], [[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]] | **산출물 형태** |

이 매트릭스는 "어떤 [[001_dikw_pyramid|데이터]]가 필요한가([[369_logic_bomb|논리]])"와 "어떻게 빠르게 가져올 것인가(물리)"의 트레이드오프를 보여줍니다. 실무에서는 개념 [[005_schema|스키마]] 단계에서 철저히 3정규형([[105_third_normal_form_3nf_transitive|3NF]]) 이상을 준수하여 [[001_dikw_pyramid|데이터]]의 순수성을 유지하고, 이후 시스템 [[282_performance_tactics|성능]] 한계가 발생할 때 물리적 단계([[009_internal_schema|내부 스키마]])에서만 반정규화를 조심스럽게 허용하는 접근법이 권장됩니다.

📢 **섹션 요약 비유**: 자동차 설계 시, 엔진과 바퀴의 완벽한 물리적 비율을 그리는 것(개념)과, 실제 도로 주행을 위해 서스펜션을 조율하는 것(물리)의 차이입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
[[104_da_as_is_analysis|데이터 아키텍처]]([[104_da_as_is_analysis|DA]]) 실무에서 개념 [[005_schema|스키마]]의 품질은 기업의 장기적 [[001_dikw_pyramid|데이터]] 활용 가치를 결정합니다.

1. **전사 [[126_data_standardization_word_domain_term|데이터 표준화]]**: 개념 [[005_schema|스키마]] 설계 시 전사 공통 '단어 사전'과 '[[064_relation_domain|도메인]] 사전'을 적용하여, A부서의 '고객명'과 B부서의 '성명'을 물리적으로 동일한 구조(VARCHAR(50))로 통일합니다. 이는 훗날 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]]) 구축 비용을 획기적으로 줄입니다.
2. **[[072_foreign_key_fk|외래 키]](Foreign [[067_db_key_uniqueness_minimality|Key]]) 딜레마**: 이론적으로 개념 [[005_schema|스키마]]는 완벽한 [[075_referential_integrity_foreign_key_cascade|참조 무결성]](FK) [[009_config|설정]]을 요구합니다. 하지만 극단적인 [[191_transaction_concept_states|트랜잭션]]이 발생하는 [[619_msa_traffic_hardware|MSA]]([[532_microservices_decomposition_patterns|마이크로서비스]]) 환경에서는, 락([[510_lock|Lock]]) 경합과 데드락([[281_deadlock_definition|Deadlock]])을 피하기 위해 물리적 FK 제약을 제거하고 애플리케이션 레벨에서 [[369_logic_bomb|논리]]적으로 [[083_relationship_in_er_model|관계]]를 보장하는 방식을 택하기도 합니다.
3. **[[128_water_scrum_fall_anti_pattern|안티패턴]] (만능 테이블 [[087_process_state_transition|생성]])**: 하나의 테이블에 수십 개의 [[186_character_stuffing_dle_stx_etx|플래그]]([[186_character_stuffing_dle_stx_etx|Flag]])와 여분 컬럼(VAR1, VAR2...)을 두고 여러 업무를 때워넣는 구조는 최악의 개념 [[005_schema|스키마]] [[128_water_scrum_fall_anti_pattern|안티패턴]]입니다. 이는 [[093_normalization|정규화]]를 파괴하여 [[001_dikw_pyramid|데이터]] 정합성을 무너뜨립니다.

아래 [[124_decision_tree|의사결정 트리]]는 개념 [[005_schema|스키마]] 변경 시의 충격 파급 경로를 나타냅니다.
```text
[개념 스키마의 변경 (예: 단일 '주소' 컬럼을 '시/구/동'으로 분리)]
   ↓
[파급 1: 외부/개념 사상(Mapping) 확인]
   ├─> 뷰 갱신으로 커버 가능? ──> (O) 애플리케이션 영향 없음 (논리적 독립성)
   └─> 뷰로 대체 불가능? ──> (X) 애플리케이션 DTO 등 연쇄 수정 발생
   ↓
[파급 2: 개념/내부 사상(Mapping) 확인]
   └─> 새로운 컬럼들에 대한 스토리지 블록, 인덱스 물리 재구성 비용 발생
```
이 흐름은 개념 [[005_schema|스키마]]의 변경이 상/하위 계층 모두에 거대한 파도를 일으킴을 시사합니다. 따라서 실무에서 [[005_schema|스키마]] 변경(Alter Table)은 개발 단계에서 철저히 격리 통제되어야 하며, 운영 중의 개념 [[005_schema|스키마]] 변경은 반드시 다운타임과 애플리케이션 파급도 평가(Impact Analysis)를 선행해야 합니다.

📢 **섹션 요약 비유**: 집의 기초 철골(개념 [[005_schema|스키마]])을 들어내고 재시공하려면, 그 위에 덮인 인테리어(외부)는 물론 바닥 기초(내부)까지 모두 뜯어고쳐야 하는 막대한 비용이 발생합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
견고한 개념 [[005_schema|스키마]] 설계는 [[001_dikw_pyramid|데이터]]의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 담보하는 가장 확실한 방어막입니다.

| 정량적 효과 | 정성적 효과 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] 중복률(Redundancy) 90% 이상 제거 | 단일 진실 공급원(SSOT) 확보로 의사결정 [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상 |
| [[090_anomaly_insertion_deletion_update|이상 현상]]([[530_anomaly|Anomaly]]) 버그 디버깅 비용 감소 | 비즈니스 로직과 [[001_dikw_pyramid|데이터]] 구조 간의 직관적 매핑 (ORM 용이성) |

미래의 [[531_cloud_native_architecture|클라우드 네이티브]] 및 [[308_pgvector|폴리글랏 퍼시스턴스]]([[132_polyglot_persistence|Polyglot Persistence]]) 환경에서도 개념 [[005_schema|스키마]]의 중요성은 줄지 않습니다. RDBMS를 넘어 NoSQL이나 [[104_graph|Graph]] DB를 도입하더라도, 전사 [[064_relation_domain|도메인]]의 개념적 [[014_data_model_components|데이터 모델]]을 먼저 설계한 뒤, 각 스토리지의 특성에 맞게 [[136_variance|분산]] 배치하는 '[[369_logic_bomb|논리]] 주도적 [[136_variance|분산]] 설계'가 업계의 표준으로 자리 잡고 있습니다.

📢 **섹션 요약 비유**: 수많은 악기([[001_dikw_pyramid|데이터]])들이 어우러져 교향곡을 연주할 수 있도록 규칙을 정해 놓은 오케스트라의 완벽한 총보(악보)입니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
* ER 다이어그램 (Entity-[[083_relationship_in_er_model|Relationship]], 개념 [[005_schema|스키마]]를 [[003_bigdata_7v|시각화]]하는 핵심 도구)
* [[093_normalization|정규화]] ([[093_normalization|Normalization]]) (개념 [[005_schema|스키마]] 내 [[001_dikw_pyramid|데이터]] 중복을 제거하는 수학적 과정)
* [[073_integrity_constraints_overview|무결성 제약조건]] (개체, [[316_reference_pattern_nosql|참조]], [[076_domain_integrity|도메인 무결성]] 등 [[001_dikw_pyramid|데이터]] 정합성 방어막)
* [[369_logic_bomb|논리]]적 [[014_data_model_components|데이터 모델]]링 (비즈니스 요구사항을 [[005_schema|스키마]] [[061_relation_schema_instance|릴레이션]]으로 변환하는 과정)
* 단일 진실 공급원 (SSOT, 전사 [[001_dikw_pyramid|데이터]]가 모순 없이 한 곳을 가리키는 원칙)

### 📈 관련 키워드 및 발전 흐름도

```text
[요구사항 분석 (Requirements Analysis)]
    │
    ▼
[개념 스키마 (Conceptual Schema) — ER 다이어그램]
    │
    ▼
[논리 스키마 (Logical Schema) — 릴레이션 모델]
    │
    ▼
[물리 스키마 (Physical Schema) — 인덱스, 스토리지]
    │
    ▼
[데이터 독립성 (Data Independence) — ANSI/SPARC 3-Layer]
```

[[002_database_definition|데이터베이스]] 설계가 요구사항 수집에서 개념-[[369_logic_bomb|논리]]-물리 3단계 [[005_schema|스키마]]로 분리하여 [[004_data_independence|데이터 독립성]]을 보장하는 방향으로 정립된 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 전체 학생들의 반, 번호, 이름 규칙을 정해둔 '학교 전체 명부 규칙'이 바로 개념 [[005_schema|스키마]]예요.
2. 이 규칙이 없다면 반장, 선생님, 양호실에서 각자 마음대로 학생 이름을 적어서 나중에 누군지 찾을 수 없게 돼요.
3. 딱 하나의 튼튼한 규칙을 만들어 두면, 누구나 헷갈리지 않고 똑같이 정확한 정보를 얻을 수 있답니다!
