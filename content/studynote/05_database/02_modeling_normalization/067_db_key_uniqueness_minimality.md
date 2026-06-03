---
title: 67. 키 (Key)의 개념 - 유일성(Uniqueness), 최소성(Minimality)
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 키(Key)는 릴레이션에서 각 튜플을 유일하게 [[655_ir_detection_analysis|식별]]하는 [[082_attribute_types_er_model|속성]] 또는 [[082_attribute_types_er_model|속성]] 집합이다.
> 2. **가치**: 유일성(Uniqueness)과 최소성(Minimality)을 만족해야 진짜 키로 인정된다.
> 3. **판단**: 후보키, 기본키, 대체키, 외래키를 구분해야 [[001_dikw_pyramid|데이터]] 모델링이 정확해진다.

---

## Ⅰ. 개요 및 필요성

같은 이름이 여러 번 있을 수 있으므로, [[001_dikw_pyramid|데이터]]는 꼭 한 행을 정확히 가리킬 [[289_identification_flags_fragmentation_offset|식별자]]가 필요하다.

키는 [[001_dikw_pyramid|데이터]] 중복을 관리하고, [[316_reference_pattern_nosql|참조]] 관계를 안정적으로 만드는 데 핵심이다.

- **📢 섹션 요약 비유**: 같은 반에 이름이 같아도 학번이 다르면 구분되는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Tuple
  ↓
Uniqueness
  ↓
Minimality
  ↓
Key
```

| 개념 | 의미 |
| :-- | :-- |
| Uniqueness | 각 튜플을 유일하게 [[655_ir_detection_analysis|식별]] |
| Minimality | 불필요한 [[082_attribute_types_er_model|속성]] 제거 |
| [[069_candidate_key_uniqueness_minimality|Candidate Key]] | 후보키 |
| Primary Key | 대표키 |

키는 하나의 [[082_attribute_types_er_model|속성]]일 수도 있고 여러 [[082_attribute_types_er_model|속성]]의 조합일 수도 있다. 중요한 것은 유일하고 더 줄일 수 없어야 한다는 점이다.

- **📢 섹션 요약 비유**: 집 열쇠는 문을 여는 데 꼭 필요한 것만 있어야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | 후보키 | 기본키 | 외래키 |
| :-- | :-- | :-- | :-- |
| 역할 | 후보 [[289_identification_flags_fragmentation_offset|식별자]] | 대표 [[289_identification_flags_fragmentation_offset|식별자]] | [[316_reference_pattern_nosql|참조]] 연결 |
| 조건 | 유일성+최소성 | 후보키 중 선택 | [[075_referential_integrity_foreign_key_cascade|참조 무결성]] |

| 용어 | 의미 |
| :-- | :-- |
| [[068_super_key_uniqueness|Super Key]] | 유일하지만 최소성 없음 |
| [[071_alternate_key|Alternate Key]] | 기본키가 아닌 후보키 |

키를 정확히 이해해야 [[093_normalization|정규화]], [[075_referential_integrity_foreign_key_cascade|참조 무결성]], [[154_database_index_b_tree_search_optimization|인덱스]] 설계를 제대로 할 수 있다.

- **📢 섹션 요약 비유**: 방 열쇠, 출입증, 예비 열쇠가 각각 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 각 테이블의 후보키를 [[655_ir_detection_analysis|식별]]했는가?
2. 최소성을 검증했는가?
3. 기본키와 외래키를 분리했는가?
4. 복합키가 정말 필요한가?
5. [[075_referential_integrity_foreign_key_cascade|참조 무결성]]을 설계에 반영했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[289_identification_flags_fragmentation_offset|식별자]]를 제대로 정하지 않는 설계
- 불필요하게 긴 복합키를 만드는 설계
- 후보키와 기본키를 혼동하는 설계
- 키 없이 [[316_reference_pattern_nosql|참조]]만 쌓는 설계

기술사 관점에서는 키를 "행 번호"로만 보지 말고, [[001_dikw_pyramid|데이터]] 모델의 [[655_ir_detection_analysis|식별]] 규칙으로 이해해야 한다.

- **📢 섹션 요약 비유**: 이름표를 제대로 달아야 누가 누구인지 헷갈리지 않는다.

---

## Ⅴ. 기대효과 및 결론

키를 제대로 잡으면 [[001_dikw_pyramid|데이터]] 중복과 [[316_reference_pattern_nosql|참조]] 오류를 줄일 수 있다. 그래서 관계형 모델의 안정성이 높아진다.

결론적으로 키는 유일성과 최소성을 만족하는 [[289_identification_flags_fragmentation_offset|식별자]]다.

- **📢 섹션 요약 비유**: 딱 맞는 열쇠만 있어야 문이 열린다.

---

## 관련 개념 맵

```text
Relation
  ↓
Key
  ↓
Candidate / Primary / Foreign Key
  ↓
Referential Integrity
```

---

## 관련 키워드 및 발전 흐름도

```text
Uniqueness
  ↓
Minimality
  ↓
Key
  ↓
Normalization
```

---

## 어린이를 위한 3줄 비유 설명

사람을 구분하는 번호가 필요해요.  
딱 필요한 것만 있어야 해요.  
키는 그런 [[289_identification_flags_fragmentation_offset|식별자]]예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 600

← **이전**: [[066_null_value_three_valued_logic|66. NULL 값 - 아직 알려지지 않거나 해당 없는 값 (0이나 공백과 다름)]]
**다음**: [[068_super_key_uniqueness|68. 슈퍼 키 (Super Key) - 유일성은 만족하나 최소성은 만족하지 않는 속성 집합]] →

---
