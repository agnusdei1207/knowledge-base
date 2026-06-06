---
title: "Primary Key"
tags:
  - "database"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 NULL이 아니고 각 행을 유일하게 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)해야 한다는 규칙이다.
> 2. **가치**: 테이블의 행 존재를 명확히 한다.
> 3. **판단**: [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)는 개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)의 중심이다.

---

## Ⅰ. 개요 및 필요성

테이블의 한 행은 반드시 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)되어야 한다.

그래서 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 중요하다.

- **📢 섹션 요약 비유**: 학생 명찰에 번호가 반드시 있어야 하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Row
  v primary key
Unique & Not Null
```

| 요소 | 의미 |
| :-- | :-- |
| Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) |
| NOT NULL | 비어 있지 않음 |
| Uniqueness | 유일성 |

개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 NULL일 수 없고 중복될 수 없다는 규칙이다.

- **📢 섹션 요약 비유**: 학생 한 명당 하나의 번호가 꼭 있어야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | 의미 |
| :-- | :-- |
| Entity [Integrity](/studynote/09_security/01_intro_principles/003_integrity/) | 개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) |
| Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 대표 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |

| 관련 | 의미 |
| :-- | :-- |
| Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| [Alternate Key](/studynote/05_database/02_modeling_normalization/071_alternate_key/) | [대체 키](/studynote/05_database/02_modeling_normalization/071_alternate_key/) |

개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 릴레이션에서 행을 확실하게 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하게 한다.

- **📢 섹션 요약 비유**: 명찰 번호가 없으면 누군지 모른다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 NULL이 아닌가?
2. 유일성이 보장되는가?
3. 행 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 확실한가?
4. 외래 키와 연결되는가?
5. [대체 키](/studynote/05_database/02_modeling_normalization/071_alternate_key/)와 구분되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- NULL 허용 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)
- 중복 가능한 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)
- PK와 FK를 혼동하는 설계
- [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 규칙을 애매하게 두는 설계

기술사 관점에서는 개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 "[기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)의 유일성과 비널성"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 번호가 없거나 같은 사람은 안 된다.

---

## Ⅴ. 기대효과 및 결론

개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 테이블의 신뢰성을 지킨다.

결론적으로 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)는 NULL이 아니고 유일해야 한다.

- **📢 섹션 요약 비유**: 한 사람 한 명찰의 원칙이다.

---

## 관련 개념 맵

```text
Row
  v
Primary Key
  v
Entity Integrity
```

---

## 관련 키워드 및 발전 흐름도

```text
Primary Key
  v
Entity Integrity
  v
Relational Model
```

---

## 어린이를 위한 3줄 비유 설명

번호표가 꼭 있어야 해요.
같은 번호면 안 돼요.
개체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 그런 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 600

<- **이전**: [73. 무결성 제약조건 (Integrity Constraints)](/studynote/05_database/02_modeling_normalization/073_integrity_constraints_overview/)
**다음**: [75. 참조 무결성 (Referential Integrity) - 외래 키 값은 참조하는 릴레이션의 기본키 값이거나 NULL이어야 함](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) ->

---
