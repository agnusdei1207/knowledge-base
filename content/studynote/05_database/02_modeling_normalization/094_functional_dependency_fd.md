+++
title = "94. 함수적 종속성 (Functional Dependency, FD)"
date = 2024-05-15

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) (Functional Dependency)은 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 내에서 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) X의 값이 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) Y의 값을 유일하게 결정하는 수학적 종속 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)($X \rightarrow Y$)다.
> 2. **가치**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) 과정에서 테이블을 분해(Decomposition)하는 명확한 기준점과 논리적 근거를 제공한다.
> 3. **판단 포인트**: 모든 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)가 좋은 것은 아니며, [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 분리할수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성은 올라가지만 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산으로 인한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하가 발생하므로 트레이드오프를 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) (Functional Dependency, FD)은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 어떤 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) 무리가 다른 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 무리의 값을 유일하게 결정짓는 제약 조건을 의미한다. 기호로는 $X \rightarrow Y$ 로 표기하며, 이때 $X$를 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) ([Determinant](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)), $Y$를 종속자 (Dependent)라고 부른다. 

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계에서는 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 하나의 거대한 테이블에 몰아넣는 비정규화 상태가 흔했다. 그러나 이렇게 되면 학번을 알 때 이름이 결정되는 규칙과, 부서 코드를 알 때 부서 이름이 결정되는 서로 다른 규칙들이 한 공간에 뒤섞이게 된다. 이로 인해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복이 발생하고 갱신, 삽입, [삭제 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/)([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/)) 현상이 필연적으로 일어난다. 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 이러한 얽힌 규칙들을 수학적으로 찾아내어 분리할 수 있는 칼날 같은 기준이 된다.

- **📢 섹션 요약 비유**: 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 자물쇠와 열쇠의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. 특정 열쇠([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) X)를 넣고 돌리면 언제나 정해진 서랍(종속자 Y) 하나만 열린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)의 조합 형태와 종속의 성격에 따라 세 가지로 나뉜다. 이들은 각각 제2, 제3 정규형 등 특정 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 단계의 타겟이 된다.

| [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 유형 | 조건 | 타겟 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) |
| :--- | :--- | :--- |
| **완전 함수 종속 (Full FD)** | 종속자 Y가 복합키 X 전체에 대해서만 종속될 때 | 이상적인 상태 |
| **부분 함수 종속 (Partial FD)** | 종속자 Y가 복합키 X의 일부에만 종속될 때 | [제2정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/) ([2NF](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/)) 대상 |
| **이행적 함수 종속 (Transitive FD)** | $X \rightarrow Y$ 이고 $Y \rightarrow Z$ 일 때 ($X \rightarrow Z$) | [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) ([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)) 대상 |

```text
┌──────────────────────────────────────────────────────────────┐
│                  함수적 종속성 분석 다이어그램               │
├──────────────────────────────────────────────────────────────┤
│ [복합 기본키]                                                │
│ ┌───────┐   ┌─────────┐                                      │
│ │ 학번  │   │ 과목코드│                                      │
│ └───┬───┘   └───┬─────┘                                      │
│     │           │                                            │
│     └─────┬─────┘                                            │
│           │ (1) 완전 함수 종속: 복합키 전체에 종속           │
│           ▼                                                  │
│      ┌────┴────┐                                             │
│      │  성적   │                                             │
│      └─────────┘                                             │
│                                                              │
│ (2) 부분 함수 종속: 키의 일부에 종속                         │
│ ┌───────┐        ┌─────────┐                                 │
│ │ 학번  │───────▶│ 학생이름│                                 │
│ └───────┘        └─────────┘                                 │
│                                                              │
│ (3) 이행적 함수 종속: 다른 속성을 거쳐 종속                  │
│ ┌───────┐        ┌─────────┐        ┌─────────┐            │
│ │ 학번  │───────▶│ 지도교수│───────▶│ 교수방 번호 │         │
│ └───────┘        └─────────┘        └─────────┘            │
└──────────────────────────────────────────────────────────────┘
```

위 다이어그램은 한 테이블 내에 혼재된 여러 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 형태를 보여준다. (1) 완전 함수 종속은 올바른 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)지만, (2) 부분 함수 종속과 (3) 이행적 함수 종속은 중복을 유발하므로 테이블을 찢어서([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) 분리해야 한다.

- **📢 섹션 요약 비유**: 회사 조직도에서 말단 직원은 직속 팀장([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/))에게만 보고해야 한다(완전 종속). 다른 부서 팀장에게 부분적으로 보고하거나(부분 종속), 본부장에게 직보하는 구조(이행적 종속)는 조직을 꼬이게 만든다.

---

## Ⅲ. 비교 및 연결

함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 [다치 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/107_multi_valued_dependency_mvd_4nf/) (Multi-Valued Dependency, [MVD](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/))과 자주 비교된다. 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 $1:1$ [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 제약이라면, [다치 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/107_multi_valued_dependency_mvd_4nf/)은 $1:N$ [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 제약이다.

| 항목 | 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) (FD) | [다치 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/107_multi_valued_dependency_mvd_4nf/) ([MVD](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/)) |
| :--- | :--- | :--- |
| **결정 규칙** | X 값 하나에 Y 값 **하나**가 결정됨 | X 값 하나에 Y 값 **여러 개**가 결정됨 |
| **기호 표기** | $X \rightarrow Y$ | $X \twoheadrightarrow Y$ |
| **관련 정규형** | 제1 ~ [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) 정규형 | [제4정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/) ([4NF](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/)) |
| **해결 방법** | 부분/이행 종속을 분리 | 독립적인 다치 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 별도 테이블로 분리 |

함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 이론의 뼈대이며, 이를 바탕으로 Boyce-Codd 정규형([BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/))까지 도달한다. 즉, "모든 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 후보키([Candidate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/))[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)?"라는 질문은 결국 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 얼마나 깔끔하게 정리되었는지를 묻는 것이다.

- **📢 섹션 요약 비유**: 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 한 명의 주민등록번호로 한 명의 사람을 찾는 단칸방이라면, [다치 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/107_multi_valued_dependency_mvd_4nf/)은 한 부모의 이름으로 여러 자녀 목록을 찾는 기숙사와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 스키마를 설계할 때, 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 완벽히 제거하는 것만이 능사는 아니다. 

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) ([종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 분리 판단)
1. **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 갱신 빈도가 높은가?** 
   - 잦은 Update/Delete가 발생한다면, [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)을 막기 위해 부분/이행 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 반드시 분리([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))해야 한다.
2. **조회(Read) 연산이 복잡한가?** 
   - 테이블을 너무 쪼개면 여러 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 묶기 위해 잦은 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))이 발생한다. 조회 중심의 시스템(예: [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))에서는 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 묵인하고 비정규화([Denormalization](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)) 상태를 유지하기도 한다.
3. **[결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 정말 유일한가?** 
   - 이름이나 이메일처럼 중복 가능성이 0.01%라도 있는 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)로 쓰면 안 되며, 인조 키([Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/))를 도입해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 실무 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 핑계로 아무런 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 분석 없이 초거대 테이블(One Big Table)을 방치하는 설계.

- **📢 섹션 요약 비유**: 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 분석하는 것은 요리 전 식재료를 종류별로 소분하는 작업이다. 다 나눠두면 관리는 편하지만([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)), 볶음밥을 만들 때는 다시 꺼내는 데 시간이 걸리듯(조인) 상황에 맞게 쪼개야 한다.

---

## Ⅴ. 기대효과 및 결론

함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 정확히 식별하고 관리하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))이 극대화된다. 한 곳을 수정했는데 다른 곳이 꼬이는 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)이 원천 차단되며, 스키마의 논리적 구조가 명확해져 유지보수가 쉬워진다.

다만 한계점도 명확하다. 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 기반의 분해는 필연적으로 물리적 테이블 수를 증가시킨다. 따라서 시스템 설계자는 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 수학적 도구로 철저히 분석하되, 물리 모델링 단계에서는 디스크 I/O와 애플리케이션의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴을 감안하여 타협선(반정규화)을 찾아야 한다. 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 그 타협을 위한 가장 단단한 기준선이다.

- **📢 섹션 요약 비유**: 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 분석은 건물의 하중을 분산하는 설계도와 같다. 기둥이 어떻게 힘을 받는지 정확히 알아야 나중에 필요할 때 안전하게 벽을 허물거나(비정규화) 합칠 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))** | 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 제거하여 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)을 막는 일련의 과정 |
| **기본키 (Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))** | 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)에서 다른 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)들을 완벽히 결정짓는 으뜸 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) |
| **[이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))** | [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 잘못 엮여 있을 때 발생하는 삽입/수정/삭제 오류 |
| **[다치 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/107_multi_valued_dependency_mvd_4nf/) ([MVD](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/))** | 함수적 종속의 개념을 1:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)로 확장한 특수 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) |

### 📈 관련 키워드 및 발전 흐름도

```text
정규화의 기초
    │
    ▼
함수적 종속성 (Functional Dependency)
    │
    ▼
부분 함수 종속 (Partial FD) · 이행적 함수 종속 (Transitive FD)
    │
    ▼
다치 종속성 (Multi-Valued Dependency) · 조인 종속성 (Join Dependency)
    │
    ▼
데이터 무결성 확보 및 반정규화 (Denormalization) 타협
```

### 👶 어린이를 위한 3줄 비유 설명

1. 함수적 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 자판기 버튼과 나오는 음료수와의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)예요.
2. 1번 버튼([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/))을 누르면 무조건 콜라(종속자) 하나만 나와야 정상적인 자판기랍니다.
3. 1번을 눌렀는데 사이다도 나오고 환타도 나오면 고장난 거라서, 자판기 안의 통을 분리해서 고쳐야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 94 / 600

← **이전**: [93. 갱신 이상 (Update Anomaly) - 중복 데이터 중 일부만 갱신되어 데이터 불일치 발생](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/)
**다음**: [95. 결정자 (Determinant) X / 종속자 (Dependent) Y](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) →

---
