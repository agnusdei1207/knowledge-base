---
title: 72. 외래 키 (Foreign Key, FK) - 다른 릴레이션의 기본 키를 참조하는 속성
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 외래 키는 다른 테이블의 기본 키를 [[316_reference_pattern_nosql|참조]]하는 [[082_attribute_types_er_model|속성]]이다.
> 2. **가치**: 테이블 간 [[083_relationship_in_er_model|관계]]를 만들고 [[075_referential_integrity_foreign_key_cascade|참조 무결성]]을 지킨다.
> 3. **판단**: 단순한 컬럼이 아니라 [[083_relationship_in_er_model|관계]]의 계약이다.

---

## Ⅰ. 개요 및 필요성

[[083_relationship_in_er_model|관계]]형 [[001_dikw_pyramid|데이터]]베이스는 테이블이 서로 연결되어야 의미가 있다.

외래 키가 그 연결을 만든다.

- **📢 섹션 요약 비유**: 친구의 주소록에 적힌 다른 친구의 전화번호다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Parent Table (PK)
  ↑ referenced by
Child Table (FK)
```

| 요소 | 의미 |
| :-- | :-- |
| Referenced PK | 부모 키 |
| FK | [[316_reference_pattern_nosql|참조]] 키 |
| [[003_integrity|Integrity]] | [[003_integrity|무결성]] |

외래 키는 부모 테이블의 존재를 전제로 한다. 그래서 잘못된 [[316_reference_pattern_nosql|참조]]를 막아 준다.

- **📢 섹션 요약 비유**: 부모 없는 번호를 적지 못하게 하는 약속이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Primary [[067_db_key_uniqueness_minimality|Key]] | Foreign [[067_db_key_uniqueness_minimality|Key]] |
| :-- | :-- | :-- |
| 역할 | 대표 [[655_ir_detection_analysis|식별]] | [[316_reference_pattern_nosql|참조]] |
| 위치 | 원본 테이블 | 자식 테이블 |

| 효과 | 의미 |
| :-- | :-- |
| [[521_join|Join]] | 테이블 연결 |
| [[075_referential_integrity_foreign_key_cascade|Referential Integrity]] | [[075_referential_integrity_foreign_key_cascade|참조 무결성]] |

외래 키는 [[083_relationship_in_er_model|관계]]형 모델의 핵심이며, 조인과 [[001_dikw_pyramid|데이터]] 정합성의 기반이다.

- **📢 섹션 요약 비유**: 문을 연결하는 열쇠고리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 부모 키를 [[316_reference_pattern_nosql|참조]]하는가?
2. [[075_referential_integrity_foreign_key_cascade|참조 무결성]]을 지키는가?
3. 조인 [[083_relationship_in_er_model|관계]]를 이해하는가?
4. 삭제/갱신 정책을 정했는가?
5. NULL 허용 여부를 고려했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[316_reference_pattern_nosql|참조]] 대상 없는 외래 키
- [[003_integrity|무결성]] 없이 연결하는 설계
- 삭제/갱신 정책을 무시하는 설계
- 외래 키를 단순 숫자 컬럼으로 보는 설계

기술사 관점에서는 외래 키를 "테이블 [[083_relationship_in_er_model|관계]]와 [[003_integrity|무결성]]을 보장하는 [[316_reference_pattern_nosql|참조]] [[082_attribute_types_er_model|속성]]"으로 설명해야 한다.

- **📢 섹션 요약 비유**: [[083_relationship_in_er_model|관계]]를 묶어 주는 연결고리다.

---

## Ⅴ. 기대효과 및 결론

외래 키는 [[001_dikw_pyramid|데이터]] 정합성과 [[083_relationship_in_er_model|관계]] 표현을 가능하게 한다.

결론적으로 외래 키는 다른 릴레이션의 기본 키를 [[316_reference_pattern_nosql|참조]]하는 [[082_attribute_types_er_model|속성]]이다.

- **📢 섹션 요약 비유**: 서로를 잇는 전화번호다.

---

## 관련 개념 맵

```text
Primary Key
  ↓ referenced by
Foreign Key
  ↓
Join / Integrity
```

---

## 관련 키워드 및 발전 흐름도

```text
Referential Integrity
  ↓
Foreign Key
  ↓
Relational Model
```

---

## 어린이를 위한 3줄 비유 설명

다른 친구 번호를 적어요.  
그래야 서로 연결돼요.  
외래 키는 그런 약속이에요.
