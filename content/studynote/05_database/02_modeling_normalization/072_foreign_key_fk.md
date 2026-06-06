---
title: "072. Foreign Key Fk"
tags:
  - "database"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 외래 키는 다른 테이블의 기본 키를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이다.
> 2. **가치**: 테이블 간 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 만들고 [참조 무결성](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 지킨다.
> 3. **판단**: 단순한 컬럼이 아니라 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 계약이다.

---

## Ⅰ. 개요 및 필요성

[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스는 테이블이 서로 연결되어야 의미가 있다.

외래 키가 그 연결을 만든다.

- **📢 섹션 요약 비유**: 친구의 주소록에 적힌 다른 친구의 전화번호다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Parent Table (PK)
  ^ referenced by
Child Table (FK)
```

| 요소 | 의미 |
| :-- | :-- |
| Referenced PK | 부모 키 |
| FK | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 키 |
| [Integrity](/studynote/09_security/01_intro_principles/003_integrity/) | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) |

외래 키는 부모 테이블의 존재를 전제로 한다. 그래서 잘못된 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 막아 준다.

- **📢 섹션 요약 비유**: 부모 없는 번호를 적지 못하게 하는 약속이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) |
| :-- | :-- | :-- |
| 역할 | 대표 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| 위치 | 원본 테이블 | 자식 테이블 |

| 효과 | 의미 |
| :-- | :-- |
| [Join](/studynote/05_database/04_transactions_concurrency/521_join/) | 테이블 연결 |
| [Referential Integrity](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) | [참조 무결성](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) |

외래 키는 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델의 핵심이며, 조인과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성의 기반이다.

- **📢 섹션 요약 비유**: 문을 연결하는 열쇠고리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 부모 키를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는가?
2. [참조 무결성](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 지키는가?
3. 조인 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이해하는가?
4. 삭제/갱신 정책을 정했는가?
5. NULL 허용 여부를 고려했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 대상 없는 외래 키
- [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 없이 연결하는 설계
- 삭제/갱신 정책을 무시하는 설계
- 외래 키를 단순 숫자 컬럼으로 보는 설계

기술사 관점에서는 외래 키를 "테이블 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)와 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장하는 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)"으로 설명해야 한다.

- **📢 섹션 요약 비유**: [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 묶어 주는 연결고리다.

---

## Ⅴ. 기대효과 및 결론

외래 키는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성과 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현을 가능하게 한다.

결론적으로 외래 키는 다른 릴레이션의 기본 키를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이다.

- **📢 섹션 요약 비유**: 서로를 잇는 전화번호다.

---

## 관련 개념 맵

```text
Primary Key
  v referenced by
Foreign Key
  v
Join / Integrity
```

---

## 관련 키워드 및 발전 흐름도

```text
Referential Integrity
  v
Foreign Key
  v
Relational Model
```

---

## 어린이를 위한 3줄 비유 설명

다른 친구 번호를 적어요.
그래야 서로 연결돼요.
외래 키는 그런 약속이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 600

<- **이전**: [71. 대체 키 (Alternate Key) - 후보 키 중 기본 키로 선택되지 않은 나머지 키](/studynote/05_database/02_modeling_normalization/071_alternate_key/)
**다음**: [73. 무결성 제약조건 (Integrity Constraints)](/studynote/05_database/02_modeling_normalization/073_integrity_constraints_overview/) ->

---
