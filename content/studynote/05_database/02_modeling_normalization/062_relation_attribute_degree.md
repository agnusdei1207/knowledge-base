+++
title = "62. 속성 (Attribute / Column / Degree) - 릴레이션의 열 (차수)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))은 릴레이션의 열(Column)이며, 개체의 특징을 나타내는 가장 작은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 단위다.
> 2. **구조**: 릴레이션의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 개수를 차수(Degree)라고 하며, 스키마를 볼 때 가장 먼저 확인해야 할 정보다.
> 3. **판단**: [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 이름, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/), [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/))이 흔들리면 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 무결성도 함께 무너진다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스에서 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 "무엇을 저장하는가"를 나타낸다. 이름, 나이, 전공 같은 항목이 바로 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이다.

[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 잘 정의해야 테이블이 읽히고, 검색되고, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)도 가능하다. 결국 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 설계가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질을 좌우한다.

- **📢 섹션 요약 비유**: 표의 제목 칸 하나하나가 무엇을 적는지 알려 주는 이름표다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">릴레이션</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">학번</div><div class="kb-diagram-cell">이름</div><div class="kb-diagram-cell">전공</div></div>
<div class="kb-diagram-note">속성 속성 속성</div>
</div>
</div>



| 용어 | 의미 |
| :-- | :-- |
| [Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 열, [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
| [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 가질 수 있는 값의 범위 |
| Degree | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 개수 |
| [Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) | 한 셀에는 하나의 값만 있어야 함 |

[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 릴레이션의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조를 만든다. 이름이 중복되면 해석이 꼬이고, 값이 여러 개 섞이면 정규형이 무너진다.

- **📢 섹션 요약 비유**: 책장마다 라벨이 있어야 무엇이 어디 있는지 바로 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목 | 의미 |
| :-- | :-- |
| [Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 어떤 정보를 담는 열 |
| Tuple | 한 행의 실제 값 묶음 |
| [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 값이 허용되는 범위 |
| [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 행을 구분하는 특별한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 묶음 |

| 설계 포인트 | 설명 |
| :-- | :-- |
| 이름 유일성 | 같은 테이블 안에서 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 이름이 중복되면 안 됨 |
| [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) | 하나의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)에 여러 값을 넣지 않음 |
| 순서 무의미성 | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 순서는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 의미가 없음 |

[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 직접 연결된다. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 원자적이지 않으면 1NF부터 흔들리고, 잘못된 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 분해는 전체 스키마를 복잡하게 만든다.

- **📢 섹션 요약 비유**: 한 칸에 여러 물건을 섞어 넣으면, 꺼낼 때마다 뭐가 뭔지 헷갈리는 서랍이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 이름이 업무 의미를 잘 드러내는가?
2. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입이 명확한가?
3. 한 칸에 여러 값이 들어가지 않는가?
4. 키와 일반 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 구분했는가?
5. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 수준이 업무 요구와 맞는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 연락처, 취미처럼 다중 값을 한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)에 넣는 설계
- 의미가 비슷한 중복 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 여러 개 두는 설계
- [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 이름을 모호하게 짓는 설계
- 비즈니스 규칙보다 구현 편의만 보는 설계

기술사 관점에서는 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 단순한 컬럼이 아니라 "의미와 제약의 단위"로 봐야 한다. 잘 정의된 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 있어야 모델이 유지된다.

- **📢 섹션 요약 비유**: 서랍 이름이 정확해야 물건이 섞이지 않는다.

---

## Ⅴ. 기대효과 및 결론

[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 릴레이션을 이해하는 가장 기본적인 열쇠다. [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 제대로 정의하면 키, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 무결성도 자연스럽게 따라온다.

결국 좋은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스는 좋은 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 정의에서 시작한다.

- **📢 섹션 요약 비유**: 집안 정리의 출발점은 각 물건에 이름표를 제대로 붙이는 것이다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Attribute</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Domain / Degree</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Tuple / Key</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Normalization</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Relational Design</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">열(Column)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">속성(Attribute)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">차수(Degree)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">정규화(Normalization)</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 표의 열 이름이에요.  
열 이름이 정확해야 무엇을 적는지 알 수 있어요.  
그래야 표가 깔끔해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 600

← **이전**: [61. 릴레이션 (Relation) - 데이터를 2차원 표로 표현한 구조](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)
**다음**: [63. 튜플 (Tuple / Row / Cardinality) - 릴레이션의 행 (카디널리티)](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/) →

---
