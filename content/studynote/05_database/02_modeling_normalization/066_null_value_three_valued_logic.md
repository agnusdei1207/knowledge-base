+++
title = "66. NULL 값 - 아직 알려지지 않거나 해당 없는 값 (0이나 공백과 다름)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NULL은 값이 없다는 뜻이 아니라, 아직 모름(Unknown) 또는 해당 없음(Inapplicable)을 뜻하는 특수 마커다.
> 2. **가치**: SQL은 NULL을 위해 3값 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)(TRUE/FALSE/UNKNOWN)를 사용하므로 일반적인 비교와 다르게 동작한다.
> 3. **판단**: NULL은 =로 비교하지 말고 IS NULL로 검사해야 하며, 집계/조인에서도 주의를 기울여야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스에서 NULL은 0이나 빈 문자열과 다르다. 값이 없다는 의미가 아니라, 아직 알 수 없거나 넣을 수 없음을 표현한다.

이 차이를 모르고 SQL을 쓰면 비교, 집계, 조건문에서 예상과 다른 결과가 나온다.

- **📢 섹션 요약 비유**: 상자 안에 "모름" 메모가 들어 있는 것이지, 상자가 비어 있다는 뜻은 아니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Value
  ├─ Known
  ├─ Unknown
  └─ Inapplicable
```

| 개념 | 의미 |
| :-- | :-- |
| NULL | 특수 마커 |
| 3-valued logic | TRUE / FALSE / UNKNOWN |
| IS NULL | NULL 여부 검사 |

SQL에서는 `NULL = NULL`도 TRUE가 아니라 UNKNOWN이 된다. 그래서 일반적인 2값 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)와 다르게 해석해야 한다.

- **📢 섹션 요약 비유**: 모른다고 적힌 칸은 예/아니오로 바로 답할 수 없다.

---

## Ⅲ. 비교 및 연결

| 값 | 의미 | NULL과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :-- | :-- | :-- |
| 0 | 숫자 값 | NULL 아님 |
| "" | 빈 문자열 | NULL 아님 |
| NULL | 미상/해당 없음 | 특수 마커 |

| 연산 | 결과 |
| :-- | :-- |
| = | UNKNOWN 가능 |
| IS NULL | 정확한 검사 |
| COALESCE | 대체값 지정 |

NULL은 [집계 함수](/knowledge-base/studynote/05_database/03_relational_model/147_aggregate_function_group_by/), 조인, 조건 필터에서 결과를 바꾸므로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델과 SQL 설계에서 반드시 고려해야 한다.

- **📢 섹션 요약 비유**: 빈 접시와 "아직 안 받음" 표시를 같은 것으로 보면 안 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. NULL과 0/빈 문자열을 구분하는가?
2. IS NULL / IS NOT NULL을 사용했는가?
3. [집계 함수](/knowledge-base/studynote/05_database/03_relational_model/147_aggregate_function_group_by/)의 NULL 처리 방식을 아는가?
4. 조인과 필터에서 UNKNOWN 결과를 고려했는가?
5. NULL 허용 여부를 모델링 단계에서 결정했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- NULL을 일반 값처럼 비교하는 설계
- 의미 없는 빈 문자열과 NULL을 혼동하는 설계
- 3값 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)를 무시하는 설계
- NULL 허용 규칙 없이 테이블만 만드는 설계

기술사 관점에서는 NULL을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 결측만이 아니라 도메인과 업무 의미를 함께 담는 개념으로 봐야 한다.

- **📢 섹션 요약 비유**: "없음"과 "아직 모름"은 서로 다르다.

---

## Ⅴ. 기대효과 및 결론

NULL을 정확히 이해하면 SQL 조건과 집계 결과를 더 안전하게 예측할 수 있다. 결국 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 해석이 안정된다.

결론적으로 NULL은 0이나 공백이 아니라, 알려지지 않음과 해당 없음의 표시다.

- **📢 섹션 요약 비유**: 비어 있는 칸과 표시만 남은 칸은 다르다.

---

## 관련 개념 맵

```text
NULL
  ↓
3-valued Logic
  ↓
SQL Comparison
  ↓
Data Quality
```

---

## 관련 키워드 및 발전 흐름도

```text
Unknown Value
  ↓
NULL
  ↓
Three-valued Logic
  ↓
Query Semantics
```

---

## 어린이를 위한 3줄 비유 설명

아직 모르는 답이 있을 수 있어요.  
그건 0이 아니라 모른다는 표시예요.  
NULL은 그런 특별한 표시예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 600

← **이전**: [65. 릴레이션의 특징 - 튜플의 무순서, 속성의 무순서, 튜플의 유일성, 속성의 원자성](/knowledge-base/studynote/05_database/02_modeling_normalization/065_relation_characteristics/)
**다음**: [67. 키 (Key)의 개념 - 유일성(Uniqueness), 최소성(Minimality)](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) →

---
