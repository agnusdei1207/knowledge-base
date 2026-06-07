---
title: "Dependency Preservation Decomposition"
date: "2026-06-07"
tags:
  - "database"
  - "studynote-database"
weight: 102
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존 (Dependency Preservation)은 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 분해할 때 원본 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)에 존재하던 [함수적 종속성](/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/) (FD; Functional Dependency)이 분해된 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)들 중 적어도 하나에 온전히 남아 유지되어야 한다는 설계 원칙이다.
> 2. **가치**: 이 원칙을 지켜야만 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 새로운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 삽입하거나 수정할 때, 테이블들을 조인하지 않고도 단일 테이블 내에서 업무적 규칙(제약조건) 위반 여부를 빠르게 검사할 수 있다.
> 3. **판단 포인트**: [무손실 분해](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) (Lossless Decomposition)는 절대 타협할 수 없는 0순위 법칙인 반면, [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 [BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) 이상의 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 과정에서 구조적 모순이 생길 경우 어쩔 수 없이 포기(소실)하고 애플리케이션 레벨에서 통제해야 할 수도 있는 선택적 1순위 법칙이다.

---

## Ⅰ. 개요 및 필요성

[종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 과정에서 비대해진 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 여러 개로 쪼갤 때, 기존의 비즈니스 룰을 의미하는 [함수적 종속성](/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/)이 허공으로 사라지지 않게 방지하는 안전장치다. [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계에서 "학번이 학과를 결정한다"와 같은 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 지키는 핵심 규칙이다.

이 개념이 중요한 이유는 성능과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 때문이다. 만약 $A \rightarrow B$라는 규칙이 분해된 어떤 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 안에도 포함되지 못하고 두 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)에 찢어져 버린다면, DBMS는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 입력될 때마다 이 규칙이 지켜졌는지 확인하기 위해 무거운 조인([Join](/studynote/05_database/04_transactions_concurrency/521_join/)) 연산을 수행해야 한다. 최악의 경우 시스템이 룰 검사를 포기해버리면 쓰레기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(가짜 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))가 DB에 그대로 쌓이게 된다.

- **📢 섹션 요약 비유**: [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 헌법이 쓰인 거대한 석판을 옮기기 위해 반으로 자르는 일과 같다. 자를 때 "살인 금지"라는 조항 한가운데를 잘라버려서 글씨를 못 읽게 만들면 처벌을 할 수 없게 되므로, 조항이 훼손되지 않게 여백을 따라 잘라야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존의 핵심 원리는 분해된 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 집합 $D = \{R_1, R_2, ..., R_n\}$ 에 대해, 각 $R_i$에서 유지되는 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)들의 합집합 연산(Closure)이 원래 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) $R$의 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 집합 $F$와 수학적으로 완전히 동일해야 한다는 것이다.

```text
+--------------------------------------------------------------+
|           종속성 보존의 분해 원리: 룰의 소실 여부 비교       |
+--------------------------------------------------------------+
| [원본 테이블 R(A, B, C)]                                     |
|  - 보유 규칙: A -> B, B -> C                                 |
|                                                              |
| [나쁜 분해 (소실 발생)]            [좋은 분해 (보존 성공)]   |
| R1(A, B) : A -> B 감시 가능         R1(A, B) : A -> B 감시 가능|
| R2(A, C) : 룰 감시 불가!           R2(B, C) : B -> C 감시 가능|
| +--> B -> C 규칙이 공중 분해됨        +--> 모든 규칙이 각 테이블에|
|                                           안전하게 보존됨    |
+--------------------------------------------------------------+
```

위 그림처럼 분해 후에도 각 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 그룹이 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 온전히 담고 있어야 한다. $R_1$과 $R_2$ 각각에 제약조건(Constraint)을 걸어 조인 없이 즉시 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 수행하는 것이 이 아키텍처의 목적이다.

- **📢 섹션 요약 비유**: 두 명의 경비원에게 넓은 구역을 나눠줄 때, "출입증 검사"라는 한 가지 임무를 둘로 쪼개어 한 명은 "출", 다른 한 명은 "입증"을 검사하게 하면 아무것도 막지 못한다. 각 경비원이 온전한 하나의 검사 매뉴얼을 가지도록 구역을 나누는 것이다.

---

## Ⅲ. 비교 및 연결

[데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)에서 테이블을 분해할 때 지켜야 할 두 가지 기둥은 <strong><a href="/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/">무손실 분해</a></strong>와 <strong><a href="/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a> 보존</strong>이다. 이 둘은 종종 서로 충돌하는 트레이드오프 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 가진다.

| 항목 | [무손실 분해](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) (Lossless Decomposition) | [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존 (Dependency Preservation) |
| :--- | :--- | :--- |
| **목적** | 조인 시 원래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 100% 복원 보장 | 분해 후에도 조인 없이 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 제약 검사 보장 |
| **필수 여부** | **절대적 필수 (0순위)** | **권장 사항 (1순위, 타협 가능)** |
| **실패 시 문제** | 가짜 정보(Spurious Tuple) 발생, DB 망가짐 | 룰 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 위해 무거운 조인 필요, 코드 복잡도 증가 |
| **달성 한계** | [BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) 이상에서도 무조건 달성 가능 | [BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) 이상에서는 수학적으로 달성 불가능할 수 있음 |

[제3정규형](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)([3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/))까지는 이 두 가지를 모두 만족하도록 분해하는 것이 가능하지만, 더 엄격한 BCNF부터는 [무손실 분해](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)를 지키려다 보면 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 소실되는 딜레마에 빠지는 경우가 발생한다.

- **📢 섹션 요약 비유**: [무손실 분해](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)는 레고 자동차를 분해했다가 다시 조립했을 때 원래 모양이 나오는(필수 생존) 것이고, [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 분해된 레고 블록들이 여전히 자동차의 부품이라는 설명서(유지보수 편리함)를 달고 있는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 아키텍트는 3NF와 [BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) 사이에서 딜레마를 마주한다. BCNF로 쪼개야 [이상 현상](/studynote/05_database/02_modeling_normalization/090_anomaly_insertion_deletion_update/)([Anomaly](/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 완벽히 제거할 수 있는데, 그 과정에서 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 깨진다면 어떻게 할 것인가?

기술사적 판단 포인트는 다음과 같다. <strong>"<a href="/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/">무손실 분해</a>는 하늘이 두 쪽 나도 지킨다. <a href="/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a> 보존은 포기할 수 있다."</strong>
BCNF로 분해하면서 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 보존되지 않는다면, 분해된 테이블 단에서는 잃어버린 비즈니스 룰을 DB 제약조건(Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 등)으로 막을 수 없다. 이럴 때는 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 소실을 감수하고 [BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) 분해를 강행한 뒤, 잃어버린 제약 조건 검사를 <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a> (Trigger)</strong>나 <strong>애플리케이션(Java/Spring) 레벨의 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 로직</strong>으로 보완(땜질)하는 전략을 채택해야 한다.

- **📢 섹션 요약 비유**: 수술(분해)을 하다가 환자의 체력([종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존)이 버티지 못할 것 같아도, 암세포([무손실 분해](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/) 위반)는 무조건 도려내야 한다. 체력이 떨어진 부분은 수술 후 영양제([트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)/애플리케이션 코드)로 보충하면 된다.

---

## Ⅴ. 기대효과 및 결론

[종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존 원칙을 완벽히 지키면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삽입/수정 시 발생하는 오버헤드가 최소화되고 시스템의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)이 강력하게 유지된다. 개발자는 DB 제약조건만 믿고 코딩을 할 수 있어 소프트웨어 아키텍처가 단순해진다.

결론적으로, [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 이상적인 목표점이다. 그러나 완벽한 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/))와 완벽한 룰 보존([종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존)이 충돌하는 현실 세계에서는 유연한 설계가 필요하다. [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 "가능한 지키되, 정합성(무손실)을 위해선 애플리케이션에 책임을 넘길 줄도 알아야 하는 유연한 방어선"으로 이해해야 한다.

- **📢 섹션 요약 비유**: 튼튼한 성벽([종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존)을 세울 수 있다면 최고겠지만, 지형이 험해 성벽을 세울 수 없다면 그 구간에는 정예 순찰대(애플리케이션 로직)를 배치해 방어력을 유지하는 것이 현명한 지휘관이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/05_database/02_modeling_normalization/094_functional_dependency_fd/">함수적 종속성</a> (FD)</strong> | [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존 원칙이 지켜내고자 하는 비즈니스 규칙의 실체 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/">무손실 분해</a></strong> | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 시 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존과 함께 달성해야 하지만 우선순위가 더 높은 원칙 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/529_bcnf/">BCNF</a> (보이스-코드 정규형)</strong> | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 엄격하게 적용하다 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존이 깨질 수 있는 경계점 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a> (Trigger)</strong> | [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)이 소실되었을 때 이를 보완하기 위해 사용하는 DB 내부 장치 |

### 📈 관련 키워드 및 발전 흐름도

```text
비정규화 테이블 (이상 현상 발생)
    |
    v
정규화 및 함수적 종속성 (FD) 정의
    |
    v
무손실 분해 (Lossless Decomposition) 최우선 적용
    |
    v
종속성 보존 (Dependency Preservation) 검증
    |
    v
BCNF 딜레마 (종속성 소실 발생 시 트리거/앱 레벨 보완)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 피자를 친구와 나눠 먹으려고 칼로 자르는데, 피자 토핑이 떨어지지 않게 자르는 규칙이 있어요.
2. [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 보존은 "피자를 자른 후에도 페퍼로니와 치즈가 같은 조각에 잘 붙어 있게 자르자"는 규칙이에요.
3. 이렇게 자르면 나중에 피자를 먹을 때 "어? 내 치즈 어디 갔어?" 하고 찾을 필요가 없어서 아주 편하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 102 / 600

<- **이전**: [101. 무손실 분해 (Lossless-Join Decomposition) - 조인 시 원래 릴레이션이 복원됨 보장](/studynote/05_database/02_modeling_normalization/101_lossless_join_decomposition/)
**다음**: [103. 제1정규형 (1NF) - 도메인이 원자값만으로 구성](/studynote/05_database/02_modeling_normalization/103_first_normal_form_1nf_atomic_value/) ->

---
