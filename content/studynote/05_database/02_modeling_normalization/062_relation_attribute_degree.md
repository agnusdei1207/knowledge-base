---
title: 62. 속성 (Attribute / Column / Degree) - 릴레이션의 열 (차수)
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[082_attribute_types_er_model|속성]]([[082_attribute_types_er_model|Attribute]])은 릴레이션의 열(Column)이며, 개체의 특징을 나타내는 가장 작은 [[369_logic_bomb|논리]] 단위다.
> 2. **구조**: 릴레이션의 [[082_attribute_types_er_model|속성]] 개수를 차수(Degree)라고 하며, 스키마를 볼 때 가장 먼저 확인해야 할 정보다.
> 3. **판단**: [[082_attribute_types_er_model|속성]] 이름, [[064_relation_domain|도메인]], [[193_atomicity_all_or_nothing|원자성]]([[193_atomicity_all_or_nothing|Atomicity]])이 흔들리면 [[093_normalization|정규화]]와 무결성도 함께 무너진다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]베이스에서 [[082_attribute_types_er_model|속성]]은 "무엇을 저장하는가"를 나타낸다. 이름, 나이, 전공 같은 항목이 바로 [[082_attribute_types_er_model|속성]]이다.

[[082_attribute_types_er_model|속성]]을 잘 정의해야 테이블이 읽히고, 검색되고, [[093_normalization|정규화]]도 가능하다. 결국 [[082_attribute_types_er_model|속성]] 설계가 [[001_dikw_pyramid|데이터]] 품질을 좌우한다.

- **📢 섹션 요약 비유**: 표의 제목 칸 하나하나가 무엇을 적는지 알려 주는 이름표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
릴레이션
┌──────┬──────┬──────┐
│ 학번 │ 이름 │ 전공 │
└──────┴──────┴──────┘
   ↑      ↑      ↑
  속성   속성   속성
```

| 용어 | 의미 |
| :-- | :-- |
| [[082_attribute_types_er_model|Attribute]] | 열, [[082_attribute_types_er_model|속성]] |
| [[064_relation_domain|Domain]] | [[082_attribute_types_er_model|속성]]이 가질 수 있는 값의 범위 |
| Degree | [[082_attribute_types_er_model|속성]]의 개수 |
| [[193_atomicity_all_or_nothing|Atomicity]] | 한 셀에는 하나의 값만 있어야 함 |

[[082_attribute_types_er_model|속성]]은 릴레이션의 [[369_logic_bomb|논리]] 구조를 만든다. 이름이 중복되면 해석이 꼬이고, 값이 여러 개 섞이면 정규형이 무너진다.

- **📢 섹션 요약 비유**: 책장마다 라벨이 있어야 무엇이 어디 있는지 바로 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목 | 의미 |
| :-- | :-- |
| [[082_attribute_types_er_model|Attribute]] | 어떤 정보를 담는 열 |
| Tuple | 한 행의 실제 값 묶음 |
| [[064_relation_domain|Domain]] | 값이 허용되는 범위 |
| [[067_db_key_uniqueness_minimality|Key]] | 행을 구분하는 특별한 [[082_attribute_types_er_model|속성]] 묶음 |

| 설계 포인트 | 설명 |
| :-- | :-- |
| 이름 유일성 | 같은 테이블 안에서 [[082_attribute_types_er_model|속성]] 이름이 중복되면 안 됨 |
| [[193_atomicity_all_or_nothing|원자성]] | 하나의 [[082_attribute_types_er_model|속성]]에 여러 값을 넣지 않음 |
| 순서 무의미성 | [[082_attribute_types_er_model|속성]] 순서는 [[369_logic_bomb|논리]]적 의미가 없음 |

[[082_attribute_types_er_model|속성]]은 [[093_normalization|정규화]]와 직접 연결된다. [[082_attribute_types_er_model|속성]]이 원자적이지 않으면 1NF부터 흔들리고, 잘못된 [[082_attribute_types_er_model|속성]] 분해는 전체 스키마를 복잡하게 만든다.

- **📢 섹션 요약 비유**: 한 칸에 여러 물건을 섞어 넣으면, 꺼낼 때마다 뭐가 뭔지 헷갈리는 서랍이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[082_attribute_types_er_model|속성]] 이름이 업무 의미를 잘 드러내는가?
2. [[064_relation_domain|도메인]]과 [[001_dikw_pyramid|데이터]] 타입이 명확한가?
3. 한 칸에 여러 값이 들어가지 않는가?
4. 키와 일반 [[082_attribute_types_er_model|속성]]을 구분했는가?
5. [[093_normalization|정규화]] 수준이 업무 요구와 맞는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 연락처, 취미처럼 다중 값을 한 [[082_attribute_types_er_model|속성]]에 넣는 설계
- 의미가 비슷한 중복 [[082_attribute_types_er_model|속성]]을 여러 개 두는 설계
- [[082_attribute_types_er_model|속성]] 이름을 모호하게 짓는 설계
- 비즈니스 규칙보다 구현 편의만 보는 설계

기술사 관점에서는 [[082_attribute_types_er_model|속성]]을 단순한 컬럼이 아니라 "의미와 제약의 단위"로 봐야 한다. 잘 정의된 [[082_attribute_types_er_model|속성]]이 있어야 모델이 유지된다.

- **📢 섹션 요약 비유**: 서랍 이름이 정확해야 물건이 섞이지 않는다.

---

## Ⅴ. 기대효과 및 결론

[[082_attribute_types_er_model|속성]]은 릴레이션을 이해하는 가장 기본적인 열쇠다. [[082_attribute_types_er_model|속성]]을 제대로 정의하면 키, [[093_normalization|정규화]], 무결성도 자연스럽게 따라온다.

결국 좋은 [[001_dikw_pyramid|데이터]]베이스는 좋은 [[082_attribute_types_er_model|속성]] 정의에서 시작한다.

- **📢 섹션 요약 비유**: 집안 정리의 출발점은 각 물건에 이름표를 제대로 붙이는 것이다.

---

## 관련 개념 맵

```text
Attribute
   ↓
Domain / Degree
   ↓
Tuple / Key
   ↓
Normalization
   ↓
Relational Design
```

---

## 관련 키워드 및 발전 흐름도

```text
열(Column)
   ↓
속성(Attribute)
   ↓
차수(Degree)
   ↓
정규화(Normalization)
```

---

## 어린이를 위한 3줄 비유 설명

[[082_attribute_types_er_model|속성]]은 표의 열 이름이에요.  
열 이름이 정확해야 무엇을 적는지 알 수 있어요.  
그래야 표가 깔끔해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 600

← **이전**: [[061_relation_schema_instance|61. 릴레이션 (Relation) - 데이터를 2차원 표로 표현한 구조]]
**다음**: [[063_relation_tuple_cardinality|63. 튜플 (Tuple / Row / Cardinality) - 릴레이션의 행 (카디널리티)]] →

---
