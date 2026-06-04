+++
title = "91. 삽입 이상 (Insertion Anomaly) - 불필요한 데이터까지 함께 삽입해야 하는 현상"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (Functional Dependency, FD)은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 어떤 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(X)의 값이 다른 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(Y)의 값을 유일하게 결정하는 제약 조건이다.
> 2. **가치**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 수행할 때, 테이블을 분해하는 기준이 되어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복과 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 예방하는 척도가 된다.
> 3. **판단 포인트**: 부분 함수 종속과 이행적 함수 종속을 식별하여 제거하는 것이 [제2정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/)([2NF](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/)) 및 [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)) 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (Functional Dependency)은 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 내에서 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)들 간의 의미적 연관성을 나타내는 수학적 개념이다. 특정 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 집합 X의 값을 알면, 다른 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 집합 Y의 값이 반드시 하나로 결정될 때, "Y는 X에 함수적으로 종속된다"고 하며 $X \rightarrow Y$로 표기한다. 이때 X를 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) ([Determinant](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)), Y를 종속자 (Dependent)라고 부른다.

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계 시, [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 내에 여러 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 무분별하게 모아두면 정보의 중복이 발생하고 갱신 시 모순이 생기는 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))이 일어난다. 이를 방지하기 위해서는 어떤 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 다른 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 의미적으로 규정하는지 정확히 파악하여, [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 규칙에 따라 테이블을 분리해야 한다. [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 이러한 분리의 수학적 근거를 제공한다.

- **📢 섹션 요약 비유**: [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 학교의 학번과 학생 이름의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)와 같다. 학번을 알면 그 학생이 누구인지 한 명으로 특정되듯, 한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 유일하게 가리키는 나침반 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 크게 세 가지 형태로 나뉘며, 각 형태는 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 특정 단계와 직결된다. 가장 이상적인 상태는 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)의 모든 일반 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 기본키(PK) 전체에만 종속되는 완전 함수 종속이다.

| [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 유형 | 설명 | 수식 예시 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :--- | :--- | :--- | :--- |
| **완전 함수 종속 (Full FD)** | 종속자 Y가 기본키 X 전체에 대해서만 종속되고, X의 일부분에는 종속되지 않는 상태. | `{학번, 과목} -> 성적` | 정상 (이상적 상태) |
| **부분 함수 종속 (Partial FD)** | 종속자 Y가 기본키 X의 전체가 아닌 일부에만 종속되는 상태. | `{학번, 과목} -> 학생이름`<br>(학생이름은 학번에만 종속됨) | [제2정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/)([2NF](/knowledge-base/studynote/05_database/02_modeling_normalization/104_second_normal_form_2nf_full_fd/))의 제거 대상 |
| **이행적 함수 종속 (Transitive FD)** | $X \rightarrow Y$ 이고 $Y \rightarrow Z$ 일 때, $X \rightarrow Z$가 성립하는 연쇄적 종속 상태. | `학번 -> 학과`, `학과 -> 학과장`<br>(학번 -> 학과장) | [제3정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)([3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/))의 제거 대상 |

```text
+--------------------------------------------------------------+
|                  함수적 종속성의 3가지 구조                  |
+--------------------------------------------------------------+
| [1] 완전 함수 종속         [2] 부분 함수 종속         [3] 이행적 함수 종속         |
|   +------+------+          +------+------+          +-------------+        |
|   |             |          |             |          |             |        |
|   X1            X2         X1            X2         X             |        |
|   +------+------+          |             |          |             |        |
|          |                 |             |          v             |        |
|          v                 v             |          Y ------------+        |
|          Y                 Y (X1에만 종속)|          |                      |
|                            +-------------+          v                      |
|                                                     Z                      |
+--------------------------------------------------------------+
```

다이어그램에서 보듯, 부분 함수 종속과 이행적 함수 종속은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 훼손하는 우회 경로를 만든다. 이 우회 경로를 끊고 독립된 테이블로 분리하는 과정이 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)다.

- **📢 섹션 요약 비유**: 완전 종속은 부대원 모두가 중대장 한 명의 명령을 직접 듣는 정상적인 지휘 체계다. 반면 부분 종속은 부대원이 다른 소대장의 명령도 듣는 것이고, 이행적 종속은 중대장 명령을 소대장을 거쳐 건너 듣는 것이다. 이중 지휘를 막으려면 소대를 분리해야 한다.

---

## Ⅲ. 비교 및 연결

[함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 단순히 의존성을 넘어 다중값 종속 (Multivalued Dependency)이나 조인 종속 ([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) Dependency)으로 개념이 확장된다. [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)이 주로 1:1 결정 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 다룬다면, 다중값 종속은 1:N 결정 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 다룬다.

| 기준 | [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (FD) | 다중값 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) ([MVD](/knowledge-base/studynote/05_database/07_exam_summary/400_mvd_4nf/)) |
| :--- | :--- | :--- |
| **결정 값의 수** | X값 1개에 Y값 <strong>1개</strong>가 결정됨 | X값 1개에 Y값 <strong>여러 개</strong>가 독립적으로 결정됨 |
| **제거 대상 정규형** | 제1~3정규형, [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) | [제4정규형](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/) ([4NF](/knowledge-base/studynote/05_database/02_modeling_normalization/108_fourth_normal_form_4nf/)) |
| **표기법** | $X \rightarrow Y$ | $X \twoheadrightarrow Y$ |

[함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)을 완벽히 해소하여 모든 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 후보키가 되도록 만든 상태가 [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) ([Boyce-Codd Normal Form](/knowledge-base/studynote/05_database/02_modeling_normalization/106_bcnf_boyce_codd_normal_form/))이다. 즉, [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 RDBMS (Relational [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/) System)에서 테이블이 원자성을 유지하고 모순 없이 작동하기 위한 가장 기본적이고 강력한 설계 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 도구다.

- **📢 섹션 요약 비유**: [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)이 '주민번호를 주면 사람 한 명이 나온다'는 1:1 자판기라면, 다중값 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)은 '과목 번호를 주면 수강생 명단 전체가 나온다'는 1:N 복권 추첨기와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실제 DB 설계에서는 모든 [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)을 완벽하게 분리하는 것만이 정답은 아니다. [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 제거([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성을 높이지만, 반대로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조회할 때 무수한 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산을 유발하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 가져올 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 복합 기본키를 사용하는 테이블에 부분 함수 종속이 남아있어 수정 이상(Modification [Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))이 발생하지 않는가?
2. 특정 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 값이 변경될 때 여러 행을 동시에 업데이트해야 하는 이행적 종속이 숨어있지 않는가?
3. 모든 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)가 후보키인가? ([BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) 위배 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))

### 실무 판단 포인트 (반정규화와의 트레이드오프)

- <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a> 채택</strong>: 핵심 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)(회원 정보, 상품 정보 등)는 완전 함수 종속을 엄격히 지켜 일관성을 보호해야 한다.
- **의도적 위반 (반정규화)**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 극도로 중요한 통계 테이블이나, 읽기 전용의 대규모 이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 경우, 이행적 종속을 알면서도 조인 비용을 줄이기 위해 한 테이블에 합쳐놓는 반정규화(De-[normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적으로 선택할 수 있다.

- **📢 섹션 요약 비유**: [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 제거해 테이블을 쪼개는 것은 물건을 분류별로 완벽히 서랍에 넣는 것과 같다. 정리는 깔끔하지만 물건을 꺼낼 때 서랍을 여러 번 열어야 하는 불편함(조인 비용)이 생긴다. 때로는 자주 쓰는 물건을 한 바구니에 담는 타협도 필요하다.

---

## Ⅴ. 기대효과 및 결론

[함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)을 기반으로 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 수행하면, 삽입, 갱신, 삭제 시 발생하는 [이상 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/) ([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 원천 차단할 수 있다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중복이 최소화되어 스토리지 공간이 절약되고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성이 보장되어 시스템의 신뢰도가 크게 상승한다.

결론적으로, [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 본질적 의미와 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 수학적으로 모델링하는 수단이다. "어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 결정하는가"라는 비즈니스 로직의 본질을 파악하고, 이를 테이블 구조로 매핑하는 능력이 바로 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계자의 핵심 역량이다.

- **📢 섹션 요약 비유**: [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 얽힌 실타래를 푸는 정확한 공식이다. 공식을 모르면 억지로 당겨 끊어지지만, 공식을 알면 아무리 꼬인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라도 깔끔하고 독립된 한 가닥의 실로 깔끔하게 감아낼 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/">이상 현상</a> (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/">Anomaly</a>)</strong> | [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)을 위배한 잘못된 설계로 인해 발생하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 갱신 오류 현상 |
| <strong>기본키 (Primary <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a>)</strong> | [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 내에서 가장 강력한 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) ([Determinant](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)) 역할을 하는 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a> (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">Normalization</a>)</strong> | [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)에 따라 테이블을 무손실 분해하는 과정 ([1NF](/knowledge-base/studynote/05_database/02_modeling_normalization/103_first_normal_form_1nf_atomic_value/) ~ [BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/)) |
| <strong>반정규화 (De-<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">normalization</a>)</strong> | 조인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상을 위해 의도적으로 [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) 원칙을 일부 위배하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

### 📈 관련 키워드 및 발전 흐름도

```text
비정규 릴레이션 (데이터 중복 및 이상 현상)
    |
    v
부분 함수 종속 (Partial FD) 식별 및 제거
    |
    v
제2정규형 (2NF) 달성
    |
    v
이행적 함수 종속 (Transitive FD) 식별 및 제거
    |
    v
제3정규형 (3NF) 및 BCNF 달성 (모든 결정자가 후보키)
```

이 흐름도는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리 속에서 나쁜 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 차례대로 솎아내어 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 높은 구조로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [함수적 종속성](/knowledge-base/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)은 "왕과 신하" 규칙이에요. 왕([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/))이 명령하면 신하(종속자)는 무조건 그대로 따라야 해요.
2. 만약 한 명의 신하가 두 명의 왕에게 명령을 받거나, 신하가 다른 신하에게 몰래 명령을 내리면 나라([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))가 혼란스러워져요.
3. 그래서 이런 복잡한 명령 체계를 발견하면, 왕과 신하를 짝지어 새로운 성(테이블)으로 나눠주는 게 아주 중요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 91 / 600

<- **이전**: [90. 이상 현상 (Anomaly) - 정규화를 거치지 않아 발생하는 데이터 중복에 따른 부작용](/knowledge-base/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)
**다음**: [92. 삭제 이상 (Deletion Anomaly) - 연쇄 삭제로 인해 필요한 데이터까지 소실되는 현상](/knowledge-base/studynote/05_database/02_modeling_normalization/092_deletion_anomaly/) ->

---
