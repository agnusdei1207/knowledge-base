+++
title = "100. 정규화 (Normalization) - 이상 현상 방지를 위해 릴레이션을 분해(Decomposition)하는 과정"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))는 하나의 거대한 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)([Relation](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/))을 의미 있는 [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (Functional Dependency)에 따라 여러 개의 작은 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 [무손실 분해](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) ([Lossless-Join Decomposition](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/))하는 과정이다.
> 2. **가치**: 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제거하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 삽입, 삭제, 갱신 시 발생하는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 오류인 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 원천적으로 차단한다.
> 3. **판단 포인트**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 수준이 높아지면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 보장되지만 조인 ([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산이 증가하여 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하될 수 있으므로, 실무에서는 [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) ([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/))이나 [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) 수준을 기준으로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 저울질해야 한다.

---

## Ⅰ. 개요 및 필요성

[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계에서 중복을 최소화하기 위해 테이블을 쪼개는 구조화 기법이다. 설계 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 단계에서 여러 엔티티(Entity)의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)들이 하나의 테이블에 무분별하게 혼재되어 있으면, 특정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 반복해서 저장되는 낭비가 발생한다.

이러한 구조적 문제는 단순한 용량 낭비를 넘어, [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))이라는 치명적인 오류를 낳는다. 수강 취소를 했더니 학생 정보까지 날아가는 [삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/) ([Deletion Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/)), 학생의 학과가 바뀌었는데 일부 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 수정되어 정보가 불일치하는 [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/) ([Update Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 넣으려 해도 불필요한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)값이 없어 넣지 못하는 [삽입 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/) ([Insertion Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/))이 발생한다. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 이 질병들을 치료하는 필수적인 수술이다.

- **📢 섹션 요약 비유**: 비정규화된 테이블은 학생과 수강 과목이 심장을 공유하는 샴쌍둥이와 같습니다. 한쪽만 치료하려 해도 둘 다 위험해지는 병([이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/))이 생기므로, 의사(설계자)가 둘을 독립적인 몸으로 떼어놓는 수술이 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 핵심 원리는 두 가지 제약 조건을 반드시 지키며 테이블을 분해하는 것이다. 첫째는 조인했을 때 원래의 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 100% 복원되어야 하는 무손실 조인 분해 ([Lossless-Join Decomposition](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)), 둘째는 기존의 [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (FD, Functional Dependency)이 분해된 테이블 중 최소 한 곳에는 유지되어야 하는 [종속성 보존](/knowledge-base/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/) ([Dependency Preservation](/knowledge-base/studynote/05_database/02_modeling_normalization/102_dependency_preservation_decomposition/))이다.

정규형 (Normal Form, NF)은 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 제거하는 강도에 따라 단계적으로 진행된다.

| 정규형 | 분해 기준 (제거 대상) | 핵심 요건 |
|:---|:---|:---|
| [제1정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/103_first_normal_form_1nf_atomic_value/) ([1NF](/knowledge-base/studynote/05_database/02_modeling_normalization/103_first_normal_form_1nf_atomic_value/)) | 반복 집단 제거 | 모든 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 <strong>원자값</strong>만 가짐 |
| [제2정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/) ([2NF](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/)) | 부분 함수 종속 제거 | 복합 기본키의 일부에만 종속된 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 분리 |
| [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) ([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)) | 이행적 함수 종속 제거 | 일반 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 간의 꼬리 무는 종속 (A→B, B→C) 분리 |
| [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) | 모든 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) 제약 | 모든 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 후보키 ([Candidate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/))가 아닌 종속 분리 |
| [제4정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/) ([4NF](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/)) | [다치 종속](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/) ([MVD](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/)) 제거 | 하나의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 여러 독립적 값을 가질 때 분리 |
| [제5정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/110_fifth_normal_form_5nf_pjnf/) (5NF) | 조인 종속 (JD) 제거 | 3개 이상의 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 [무손실 분해](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) 가능 시 분리 |

```text
┌──────────────────────────────────────────────────────────────┐
│                  정규화 과정의 무손실 분해 원리               │
├──────────────────────────────────────────────────────────────┤
│ [원래 테이블: 수강] (학번, 과목코드, 성적, 과목명)                 │
│         │ (부분 함수 종속 발생: 과목코드 ─▶ 과목명)             │
│         ▼                                                    │
│ ┌──────────────────────┐  ┌────────────────────────┐         │
│ │ [테이블 A: 성적]      │  │ [테이블 B: 과목]        │         │
│ │ 학번, 과목코드, 성적    │  │ 과목코드(PK), 과목명      │         │
│ └──────────────────────┘  └────────────────────────┘         │
│         │                             │                      │
│         └──────▶ 조인 (JOIN) ◀──────┘                      │
│                (과목코드 기준)                                  │
│         ▼                                                    │
│ [완벽히 복원된 원래 테이블] (가짜 데이터 없음 = 무손실)               │
└──────────────────────────────────────────────────────────────┘
```

이 그림은 분해 후 외래키를 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다시 연결할 때, 어떤 정보의 손실이나 잉여 없이 완벽히 복원되어야 한다는 [무손실 분해](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)의 핵심을 보여준다.

- **📢 섹션 요약 비유**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 거대한 레고 성을 부품 단위로 분해하는 것과 같습니다. 다시 설명서(외래키)대로 조립하면 원래 성과 똑같이 만들어져야 하며, 엉뚱한 블록이 튀어나오면 잘못 분해한 것입니다.

---

## Ⅲ. 비교 및 연결

[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 반정규화 (De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))와 항상 트레이드오프(Trade-off) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에 놓인다.

| 비교 항목 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 반정규화 (De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) |
|:---|:---|:---|
| **목적** | [데이터 중복 제거](/knowledge-base/studynote/02_operating_system/09_file_system/546_data_deduplication/) 및 [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) | 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) (조인 최소화) 향상 |
| **적용 시점** | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델링 단계 | 물리적 설계 후반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 단계 |
| **장점** | [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/) 방지, 저장 공간 절약 | 복잡한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 단순화, 조회 속도 극대화 |
| **단점** | 다수의 조인으로 인한 CPU 연산 부하 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 위험, 업데이트 비용 증가 |

[OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) 시스템에서는 잦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경으로 인한 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)을 막기 위해 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)가 필수적이다. 반면, [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))와 같은 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) 환경에서는 조인 비용을 줄이기 위해 의도적으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 포기하는 반정규화를 적용한다.

- **📢 섹션 요약 비유**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 물건을 완벽히 카테고리별로 서랍장에 정리하는 것이고, 반정규화는 자주 꺼내 쓰는 물건을 묶어서 책상 위에 어질러 두어 빨리 찾게 하는 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 모든 테이블을 [제5정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/110_fifth_normal_form_5nf_pjnf/)(5NF)까지 쪼개는 것은 심각한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 장애를 유발한다. 테이블이 과도하게 잘게 쪼개지면, 단순한 회원 정보 하나를 조회할 때도 4~5번의 조인이 걸려 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 인덱스가 무용지물이 될 수 있다.

### 실무 판단 포인트 및 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong>어디까지 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>할 것인가?</strong>
   - 일반적인 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB에서는 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/">제3정규형</a>(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/">3NF</a>) 또는 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/">BCNF</a></strong>까지만 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)해도 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)의 99%를 방지할 수 있다. 4NF와 5NF는 학술적 성격이 강해 특수한 케이스가 아니면 지양한다.
2. **언제 멈출 것인가?**
   - 갱신보다 조회가 압도적으로 많은 테이블 (예: 통계성 게시판, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 테이블)이라면 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 기준을 완화하고 읽기 최적화 설계를 채택한다.
3. <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/">무손실 분해</a>가 제대로 되었는가?</strong>
   - 분해된 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)들의 공통 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 적어도 한 쪽 테이블에서는 기본키 (Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))나 유일키 (Unique [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 역할을 해야 무손실 조인이 성립한다.

- **📢 섹션 요약 비유**: 외과 수술([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))을 너무 깊게 하면 종양(중복)은 완벽히 제거되지만, 환자(DB)가 회복하지 못해 걷지도(조회) 못하게 됩니다. 살 수 있는 선까지만 자르는 것이 명의입니다.

---

## Ⅴ. 기대효과 및 결론

[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 완벽히 수행하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 정합성과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 영구적으로 유지되는 튼튼한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 얻는다. 요구사항이 변경되어 새로운 엔티티가 추가되더라도 기존 구조를 갈아엎지 않고 유연하게 확장할 수 있는 토대가 마련된다.

결론적으로, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 "단일 진실(Single Source of Truth)"을 만들기 위한 핵심 규칙이다. 설계 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 철저하게 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 수행하여 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 완결성을 확보하고, 시스템 오픈 전후 [성능 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/445_performance_test_types/) 결과에 따라 필요한 부분만 예외적으로 반정규화를 허용하는 방어적 접근이 가장 훌륭한 DB 아키텍처 전략이다.

- **📢 섹션 요약 비유**: 건물을 지을 때 설계도대로 철골을 하나씩 정교하게 맞추는([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) 과정이 힘들어도, 이렇게 지어둔 건물이어야 지진([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 갱신 폭탄)이 와도 무너지지 않고 버틸 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (Functional Dependency) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 수행하기 위한 직접적인 기준점 ([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)와 종속자의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)) |
| [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/)) | 비정규화된 테이블에서 발생하는 삽입/삭제/갱신 시의 치명적 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 오류 |
| [무손실 분해](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) ([Lossless-Join Decomposition](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 분해 후 조인 시 정보 손실이나 가짜 투플이 발생하지 않아야 한다는 절대 제약 |
| 반정규화 (De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 조회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상을 위해 의도적으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 원칙을 깨고 중복을 허용하는 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 종속성 파악 (Functional Dependency)
    │
    ▼
정규화 적용 (1NF ~ BCNF)
    │
    ▼
무손실 분해 및 종속성 보존 검증
    │
    ▼
논리적 무결성 확보 (Anomaly 제거)
    │
    ▼
성능 튜닝 및 반정규화 (De-normalization) 결합
```

이 흐름도는 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 분석을 시작으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 거쳐 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 확보한 뒤, 현실적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 타협점인 반정규화로 이어지는 실무적 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자에 자동차, 인형, 블록을 마구 섞어 놓으면 나중에 찾기도 힘들고 망가지기 쉬워요.
2. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 이 장난감들을 자동차 상자, 인형 상자, 블록 상자로 종류별로 깔끔하게 나누어 담는 정리 정돈이에요.
3. 이렇게 잘 나누어두면 새로 장난감이 생겨도 어디에 넣을지 헷갈리지 않고, 필요한 것만 쏙쏙 꺼내 놀 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 600

← **이전**: [99. 암스트롱의 공리 (Armstrong's Axioms) - 반사의 공리, 첨가의 공리, 이행의 공리](/knowledge-base/studynote/05_database/02_modeling_normalization/099_armstrongs_axioms_reflexivity/)
**다음**: [101. 무손실 분해 (Lossless-Join Decomposition) - 조인 시 원래 릴레이션이 복원됨 보장](/knowledge-base/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) →

---
