+++
title = "90. 이상 현상 (Anomaly) - 정규화를 거치지 않아 발생하는 데이터 중복에 따른 부작용"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이상 현상 ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 테이블 설계([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))가 잘못되어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 불필요하게 중복 저장될 때 발생하는 삽입, 삭제, 갱신 시의 논리적 모순과 오류다.
> 2. **가치**: 이상 현상을 이해하는 것은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))을 지키기 위한 필수 과정이며, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))의 필요성을 증명하는 직접적인 근거가 된다.
> 3. **판단 포인트**: 모든 테이블을 잘게 쪼개는 것만이 능사가 아니며, 이상 현상의 발생 가능성과 조인 ([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))으로 인한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 저울질하여 적절한 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)/반정규화 수준을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

이상 현상 ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 내에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 중복해서 저장됨으로써 발생하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 상태를 의미한다. [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 두 개 이상의 독립적인 엔티티 (Entity) 정보가 하나의 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) ([Relation](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/))에 혼재되어 있을 때 필연적으로 나타난다. 

시스템 규모가 커지고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경이 빈번해질수록, 중복된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중 일부만 수정되거나 필요 없는 정보까지 강제로 다뤄야 하는 문제가 시스템 전체의 신뢰성을 무너뜨린다. 따라서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계자는 "어떤 조작을 할 때 모순이 생기는가"를 사전에 파악하고 이를 방지할 수 있는 테이블 구조를 만들어야 한다.

- **📢 섹션 요약 비유**: 이상 현상은 두 명의 환자가 한 침대에 본드로 붙어있는 샴쌍둥이 상태와 같다. 한 명에게 주사를 놓거나 퇴원시킬 때마다 멀쩡한 다른 한 명에게 치명적인 부작용이 터지는 현상이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이상 현상은 발생하는 작업의 종류에 따라 [삽입 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/) ([Insertion Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/)), [삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/) ([Deletion Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/)), [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/) ([Update Anomaly](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/))의 3가지로 나뉜다. 이들은 모두 **'[종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) (Dependency)이 얽혀 있는 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'**라는 동일한 원인에서 출발한다.

| 이상 현상 종류 | 메커니즘 (발생 원리) | 결과 |
| :--- | :--- | :--- |
| **[삽입 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/)** | 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 넣으려 할 때, 아직 불필요한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)값이 없어 Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 제약(NULL 불가)에 걸려 삽입 실패 | 정상적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등록 거부 |
| **[삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/)** | 특정 정보를 지울 때, 같은 행에 묶여 있던 유지해야 할 핵심 정보까지 연쇄적으로 날아감 | 의도치 않은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 |
| **[갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/)** | 중복 저장된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중 일부만 수정되어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간에 모순 발생 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 및 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 하락 |

```text
┌──────────────────────────────────────────────────────────────┐
│        정규화되지 않은 뚱뚱한 테이블에서의 3대 이상 현상     │
├──────────────────────────────────────────────────────────────┤
│ [ 학번(PK) │ 과목명(PK) │   이름   │  학과  │  성적 ]      │
│ ──────────────────────────────────────────────────────────── │
│   101      │    DB      │  김철수  │ 컴퓨터 │   A          │
│   101      │    OS      │  김철수  │ 컴퓨터 │   B          │ ◀ 갱신 이상
│   102      │   회계     │  이영희  │  경영  │   A          │ ◀ 삭제 이상
│                                                              │
│ [삽입 이상]: 신입생 '박민수(컴퓨터)' 입학 (아직 수강과목 없음) │
│             => 과목명(PK)이 NULL이라 삽입 불가!              │
│ [삭제 이상]: '이영희'가 회계 수강 취소 (행 삭제)             │
│             => 이영희가 경영학과라는 학생 정보까지 영구 삭제!│
│ [갱신 이상]: '김철수'가 수학과로 전과                        │
│             => DB 행만 '수학과'로 바꾸면 OS 행과 데이터 불일치!│
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 학생 엔티티와 수강 엔티티가 합쳐졌을 때 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 간의 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 꼬이면서 발생하는 구체적인 에러 상황을 보여준다.

- **📢 섹션 요약 비유**: 뚱뚱한 테이블은 학생증과 수강증을 한 장의 종이에 인쇄한 것과 같다. 과목을 취소하려고 종이를 찢으면 학생증도 찢어지고([삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/)), 수강 안 한 신입생은 종이 자체를 발급받을 수 없다([삽입 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/)).

---

## Ⅲ. 비교 및 연결

이상 현상을 해결하기 위한 접근은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))와 어플리케이션 단의 방어 로직으로 나눌 수 있다. 

| 항목 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 애플리케이션 레벨 방어 |
| :--- | :--- | :--- |
| 목적 | DB 구조적 차원에서의 근본적 해결 | 반정규화 상태에서 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 제어로 모순 방지 |
| 장점 | 원천적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) | 조인 연산 감소로 인한 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |
| 약점 | 테이블 쪼개기로 인한 조인 비용 발생 | 개발 복잡도 증가, 휴먼 에러 위험 잔존 |

[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 이상 현상을 없애는 대신 조인 ([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산이라는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용을 지불한다. 반면 읽기 중심의 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/)) 환경에서는 이상 현상(특히 [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/))의 발생 빈도가 극히 낮으므로, 의도적으로 반정규화 (De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 통해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화하는 전략을 취한다. 

- **📢 섹션 요약 비유**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 약 상자를 종류별로 나누어 섞이지 않게 하는 원초적 해결책이고, 애플리케이션 방어는 약을 한 통에 섞어두고 간호사가 실수 없이 골라내게 훈련시키는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 이상 현상은 개발 단계보다 운영 중반 이후 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 누적되었을 때 치명적인 버그로 발현된다. "A 화면과 B 화면의 통계 숫자가 다르다"는 장애 보고의 80%는 [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/)에서 비롯된다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 특정 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 변경될 때, 테이블 내 여러 행을 스캔하여 동시 업데이트(UPDATE)해야 하는 구조인가? ([갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/) 징후)
2. 엔티티를 삭제할 때 남겨둬야 할 이력(History)이 연쇄 삭제(Cascade) 처리되는가? ([삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/) 징후)
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삽입 시 불필요한 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)([Dummy](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 강제로 넣고 있지 않은가? ([삽입 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/) 징후)

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 핑계로 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 설계부터 하나의 거대한 단일 테이블을 고집하는 행위
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 방치한 채, 애플리케이션의 복잡한 비즈니스 로직으로 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 억지로 땜질하려는 설계

- **📢 섹션 요약 비유**: 이상 현상이 있는 DB는 시한폭탄과 같다. 처음 빈 테이블일 때는 잘 돌아가지만, 트래픽이 몰리고 갱신이 잦아지면 예외 처리 코드가 기하급수적으로 늘어나 결국 폭발한다.

---

## Ⅴ. 기대효과 및 결론

이상 현상을 완벽히 파악하고 제거하면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))이 보장되어 한 번 입력된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 어디서 조회하든 항상 참(Truth)을 유지하게 된다. 또한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조가 업무의 본질적 의미(Entity)를 정확히 반영하게 되어 시스템의 유지보수성과 확장성이 비약적으로 상승한다.

결국 이상 현상은 "테이블을 어떻게 분리할 것인가"를 알려주는 경고등이다. 설계자는 이상 현상의 징후를 조기에 발견하고, [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)) 또는 [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) ([Boyce-Codd Normal Form](/knowledge-base/studynote/05_database/02_modeling_normalization/106_bcnf_boyce_codd_normal_form/))까지의 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 통해 건강한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 뼈대를 구축해야 한다.

- **📢 섹션 요약 비유**: 이상 현상은 암세포의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 증상이다. 통증(이상 현상)을 정확히 인지해야 수술([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))을 통해 건강한 몸([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))을 되찾을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) | 이상 현상을 막아서 최종적으로 달성하고자 하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) |
| 함수적 종속 (Functional Dependency) | 이상 현상을 유발하는 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 간의 불필요한 결합 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 이상 현상을 치료하기 위해 테이블을 분해하는 수술 과정 |
| 반정규화 (De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | 이상 현상 위험을 감수하고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 다시 테이블을 합치는 행위 |

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 중복 방치 (비정규화 테이블)
    │
    ▼
3대 이상 현상 발생 (삽입 / 삭제 / 갱신 이상)
    │
    ▼
함수적 종속성 분석 (결정자와 종속자 파악)
    │
    ▼
정규화 (Normalization: 1NF → 2NF → 3NF → BCNF)
    │
    ▼
성능/무결성 트레이드오프 및 반정규화 (De-normalization) 판단
```

이 흐름도는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복이 유발한 문제가 어떻게 구조적 분석을 거쳐 해결되고, 최종 실무적 타협점까지 이어지는지 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자에 로봇과 인형을 막 섞어 놓으면 찾을 때 헷갈리고 고장 나기 쉬워요. 이것이 이상 현상이에요!
2. 로봇 부품을 버리려다가 엉뚱하게 인형 팔까지 같이 버려지는 슬픈 일이 생길 수도 있죠.
3. 그래서 상자를 두 개로 나눠서([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) 로봇은 로봇 상자에, 인형은 인형 상자에 깔끔하게 따로 보관해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 600

← **이전**: [89. 확장 ER 모델 (EER) - 서브클래스, 슈퍼클래스, 상속(일반화/특수화) 개념 추가](/knowledge-base/studynote/05_database/02_modeling_normalization/089_eer_enhanced_er_model_specialization/)
**다음**: [91. 삽입 이상 (Insertion Anomaly) - 불필요한 데이터까지 함께 삽입해야 하는 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/091_functional_dependency_fd/) →

---
