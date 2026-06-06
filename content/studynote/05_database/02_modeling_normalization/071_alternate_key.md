---
title: "071. Alternate Key"
tags:
  - "database"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 대체 키는 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 중에서 기본 키로 선택되지 않은 나머지 유일 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)다.
> 2. **가치**: 여전히 유일성을 보장하므로 중요한 예비 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 역할을 한다.
> 3. **판단**: 기본 키와 대체 키를 구분해야 설계와 제약 조건이 명확해진다.

---

## Ⅰ. 개요 및 필요성

[후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)가 여러 개일 때 하나만 기본 키가 된다. 나머지는 대체 키다.

그래서 대체 키도 충분히 중요하다.

- **📢 섹션 요약 비유**: 반장 말고도 후보였던 다른 친구들이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Candidate Keys
  +- Primary Key
  +- Alternate Keys
```

| 개념 | 의미 |
| :-- | :-- |
| Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 선택된 대표 |
| Alternate [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 나머지 후보 |

대체 키는 기본 키가 아니지만, 여전히 유일성을 만족한다. 그래서 보조 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)로 활용될 수 있다.

- **📢 섹션 요약 비유**: 1등은 아니어도 충분히 잘하는 후보들이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | Alternate [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) |
| :-- | :-- | :-- |
| 선택 | 대표 | 나머지 후보 |
| 유일성 | O | O |
| NULL | 불가 | 보통 불가 |

| 관련 키 | 의미 |
| :-- | :-- |
| [Candidate Key](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | 상위 개념 |
| Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |

대체 키는 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)의 일부로서 설계의 유연성을 제공한다.

- **📢 섹션 요약 비유**: 대표는 하나지만, 다른 후보도 능력이 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 기본 키와 구분되는가?
2. 유일성을 유지하는가?
3. 보조 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)로 사용할 수 있는가?
4. 제약 조건이 명확한가?
5. [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 목록을 보존하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 대체 키를 그냥 버리는 설계
- 기본 키와 같은 의미로 쓰는 설계
- 유일성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 보조 키로 쓰는 설계
- [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 후보를 정리하지 않는 설계

기술사 관점에서는 대체 키를 "기본 키로 선택되지 않은 유일 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)"로 설명해야 한다.

- **📢 섹션 요약 비유**: 1등이 아니어도 중요한 예비 선수다.

---

## Ⅴ. 기대효과 및 결론

대체 키를 이해하면 모델링에서 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 전체를 더 잘 활용할 수 있다.

결론적으로 대체 키는 기본 키로 선택되지 않은 [후보 키](/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)다.

- **📢 섹션 요약 비유**: 반장 후보였던 다른 친구들도 쓸모가 있다.

---

## 관련 개념 맵

```text
Candidate Key
  v
Primary Key
  v
Alternate Key
```

---

## 관련 키워드 및 발전 흐름도

```text
Candidate Key
  v
Alternate Key
  v
Key Constraint
```

---

## 어린이를 위한 3줄 비유 설명

반장 말고도 잘하는 친구가 있어요.
그 친구들도 중요해요.
대체 키는 그런 친구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 600

<- **이전**: [70. 기본 키 (Primary Key, PK) - 후보 키 중 설계자가 선택한 메인 식별자 (NULL 불가)](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)
**다음**: [72. 외래 키 (Foreign Key, FK) - 다른 릴레이션의 기본 키를 참조하는 속성](/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) ->

---
