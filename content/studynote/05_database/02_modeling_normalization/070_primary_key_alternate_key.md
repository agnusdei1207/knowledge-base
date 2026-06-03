+++
title = "70. 기본 키 (Primary Key, PK) - 후보 키 중 설계자가 선택한 메인 식별자 (NULL 불가)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기본 키는 [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 중에서 테이블을 대표하도록 선택된 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)다.
> 2. **가치**: NULL 불가와 유일성으로 행을 안정적으로 식별하게 해 준다.
> 3. **판단**: 대체 키와 외래 키와의 관계까지 이해해야 모델링이 정확해진다.

---

## Ⅰ. 개요 및 필요성

테이블에는 여러 [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)가 있을 수 있지만, 대표로 쓸 하나가 필요하다.

그 대표가 기본 키다.

- **📢 섹션 요약 비유**: 반장 후보 중 실제 반장을 뽑는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Candidate Keys
  ↓ choose one
Primary Key
```

| 조건 | 의미 |
| :-- | :-- |
| Uniqueness | 유일성 |
| NOT NULL | NULL 불가 |
| Representative | 대표 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |

기본 키는 [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 중 하나를 선택한 것이며, 테이블의 주인공 역할을 한다.

- **📢 섹션 요약 비유**: 이름표가 가장 크고 눈에 잘 띄는 한 명이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Candidate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [Alternate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/071_alternate_key/) |
| :-- | :-- | :-- | :-- |
| 유일성 | O | O | O |
| 최소성 | O | O | O |
| 선택 | 후보 | 대표 | 나머지 후보 |

| 관련 키 | 의미 |
| :-- | :-- |
| Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| [Super Key](/knowledge-base/studynote/05_database/02_modeling_normalization/068_super_key_uniqueness/) | 더 넓은 집합 |

기본 키는 단순한 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 넘어 관계형 모델의 중심이다.

- **📢 섹션 요약 비유**: 여러 후보 중 가장 중요한 대표를 정하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 중 하나를 선택했는가?
2. NULL을 허용하지 않는가?
3. 변경 가능성이 낮은가?
4. 외래 키와 관계를 고려했는가?
5. 대체 키를 보존하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 의미 없는 컬럼을 기본 키로 정하는 설계
- NULL 가능한 키를 쓰는 설계
- [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)를 여러 개 기본 키로 착각하는 설계
- [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 무결성을 무시하는 설계

기술사 관점에서는 기본 키를 "테이블 대표 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)"로 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: 한 반의 대표 이름표다.

---

## Ⅴ. 기대효과 및 결론

기본 키를 잘 정하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 식별과 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)가 안정된다.

결론적으로 기본 키는 [후보 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) 중 선택된 대표 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)다.

- **📢 섹션 요약 비유**: 대표가 있어야 모두를 부를 수 있다.

---

## 관련 개념 맵

```text
Candidate Key
  ↓ choose
Primary Key
  ↓
Foreign Key
```

---

## 관련 키워드 및 발전 흐름도

```text
Candidate Key
  ↓
Primary Key
  ↓
Referential Integrity
```

---

## 어린이를 위한 3줄 비유 설명

여러 후보 중 한 명을 뽑아요.  
그 사람은 대표가 돼요.  
기본 키는 그런 대표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 600

← **이전**: [69. 후보 키 (Candidate Key) - 유일성과 최소성을 모두 만족하는 키](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)
**다음**: [71. 대체 키 (Alternate Key) - 후보 키 중 기본 키로 선택되지 않은 나머지 키](/knowledge-base/studynote/05_database/02_modeling_normalization/071_alternate_key/) →

---
