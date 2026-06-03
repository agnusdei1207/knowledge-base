---
title: 70. 기본 키 (Primary Key, PK) - 후보 키 중 설계자가 선택한 메인 식별자 (NULL 불가)
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기본 키는 [[069_candidate_key_uniqueness_minimality|후보 키]] 중에서 테이블을 대표하도록 선택된 [[289_identification_flags_fragmentation_offset|식별자]]다.
> 2. **가치**: NULL 불가와 유일성으로 행을 안정적으로 식별하게 해 준다.
> 3. **판단**: 대체 키와 외래 키와의 관계까지 이해해야 모델링이 정확해진다.

---

## Ⅰ. 개요 및 필요성

테이블에는 여러 [[069_candidate_key_uniqueness_minimality|후보 키]]가 있을 수 있지만, 대표로 쓸 하나가 필요하다.

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
| Representative | 대표 [[289_identification_flags_fragmentation_offset|식별자]] |

기본 키는 [[069_candidate_key_uniqueness_minimality|후보 키]] 중 하나를 선택한 것이며, 테이블의 주인공 역할을 한다.

- **📢 섹션 요약 비유**: 이름표가 가장 크고 눈에 잘 띄는 한 명이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[069_candidate_key_uniqueness_minimality|Candidate Key]] | Primary [[067_db_key_uniqueness_minimality|Key]] | [[071_alternate_key|Alternate Key]] |
| :-- | :-- | :-- | :-- |
| 유일성 | O | O | O |
| 최소성 | O | O | O |
| 선택 | 후보 | 대표 | 나머지 후보 |

| 관련 키 | 의미 |
| :-- | :-- |
| Foreign [[067_db_key_uniqueness_minimality|Key]] | [[316_reference_pattern_nosql|참조]] |
| [[068_super_key_uniqueness|Super Key]] | 더 넓은 집합 |

기본 키는 단순한 [[289_identification_flags_fragmentation_offset|식별자]]를 넘어 관계형 모델의 중심이다.

- **📢 섹션 요약 비유**: 여러 후보 중 가장 중요한 대표를 정하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[069_candidate_key_uniqueness_minimality|후보 키]] 중 하나를 선택했는가?
2. NULL을 허용하지 않는가?
3. 변경 가능성이 낮은가?
4. 외래 키와 관계를 고려했는가?
5. 대체 키를 보존하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 의미 없는 컬럼을 기본 키로 정하는 설계
- NULL 가능한 키를 쓰는 설계
- [[069_candidate_key_uniqueness_minimality|후보 키]]를 여러 개 기본 키로 착각하는 설계
- [[316_reference_pattern_nosql|참조]] 무결성을 무시하는 설계

기술사 관점에서는 기본 키를 "테이블 대표 [[289_identification_flags_fragmentation_offset|식별자]]"로 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: 한 반의 대표 이름표다.

---

## Ⅴ. 기대효과 및 결론

기본 키를 잘 정하면 [[001_dikw_pyramid|데이터]] 식별과 [[316_reference_pattern_nosql|참조]]가 안정된다.

결론적으로 기본 키는 [[069_candidate_key_uniqueness_minimality|후보 키]] 중 선택된 대표 [[289_identification_flags_fragmentation_offset|식별자]]다.

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
