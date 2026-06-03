+++
title = "78. 키 무결성 (Key Integrity)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 PK (Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))가 각 행을 유일하게 식별하고 FK (Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))가 부모 행을 실제로 가리키게 하는 규칙이다.
> 2. **가치**: 이 규칙이 있어야 중복과 고아 레코드를 막고 조인 결과를 믿을 수 있다.
> 3. **판단 포인트**: 기술사는 의미보다 안정성이 높은 키를 선택하고 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System) 제약조건으로 강제해야 한다.

---

## Ⅰ. 개요 및 필요성

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 릴레이션의 각 행이 하나의 키로 식별되고, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 관계가 실제 존재하는 값만 가리키도록 보장하는 규칙이다.
이 규칙이 무너지면 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 번 들어가거나, 부모가 사라졌는데 자식만 남는 문제가 생긴다. 그래서 정규화된 모델도 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 없으면 신뢰를 잃는다.
```text
┌───────────────┐      FK      ┌───────────────┐
│ Customer      │────────────▶│ Order         │
│ PK customer_id│             │ PK order_id   │
└───────────────┘             └───────────────┘
```

- **📢 섹션 요약 비유**: 식별이 흐리면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관계도 같이 흐려진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

후보키([candidate key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)) 중 하나가 PK가 되고, 나머지는 UK (Unique [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))로 남을 수 있다. FK는 부모 테이블의 키를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하면서 [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 유지한다.
PK는 보통 NOT NULL과 UNIQUE를 동시에 만족해야 하고, FK는 삽입·갱신·삭제 규칙까지 함께 설계해야 한다.
| 구성 요소 | 역할 | 설계 포인트 |
| --- | --- | --- |
| [Candidate key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | 후보 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 집합 | 업무 의미와 안정성을 본다 |
| PK | 대표 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 짧고 변하지 않아야 한다 |
| UK | 대체 유일성 보장 | 중복만 막고 NULL 정책을 확인한다 |
| FK | 부모 행 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | 고아 레코드 방지와 조인 기준이 된다 |
| [Surrogate key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/) | 대리 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경과 변경 안정성을 고려한다 |

- **📢 섹션 요약 비유**: 후보키, 대표키, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)키가 역할을 나눠 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 만든다.

---

## Ⅲ. 비교 및 연결

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 엔터티 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([entity integrity](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/))과 [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)([referential integrity](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/))을 실제로 구현하는 바닥 규칙이다. 둘을 함께 봐야 "행은 자기 자신을 잃지 않고, 관계도 끊기지 않는다"는 뜻이 완성된다.
자연키는 업무 의미가 분명하지만 변경 가능성이 있고, 대리키는 의미는 약하지만 안정성과 조인 성능이 좋다. 그래서 키 선택은 의미와 운영을 동시에 봐야 한다.
| 비교축 | 자연키 | 대리키 |
| --- | --- | --- |
| 의미 | 업무상 읽기 쉽다 | 의미는 약하다 |
| 변경성 | 업무 변경에 흔들릴 수 있다 | 대체로 안정적이다 |
| 운영성 | 사람이 이해하기 좋다 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)·샤딩에 유리하다 |

- **📢 섹션 요약 비유**: 자연키와 대리키는 의미와 안정성 사이의 선택이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 안정성, 길이, 의미, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)성, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 비용을 함께 본다. 특히 키가 바뀌면 연쇄 갱신이 발생하므로, 바뀔 가능성이 낮은 값을 우선한다.
[DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System) 제약조건으로 강제하고 애플리케이션은 보조 역할만 맡겨야 한다. 앱 코드만 믿으면 배치 작업이나 수동 수정에서 쉽게 깨진다.
### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. PK가 짧고 변하지 않는가?
2. FK가 실제 부모 행을 강제하는가?
3. 키 변경 시 연쇄 영향이 통제되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 이메일, 전화번호처럼 바뀌기 쉬운 값을 PK로 쓰는 것
- 편하다는 이유로 FK 제약을 꺼버리는 것

- **📢 섹션 요약 비유**: 제약조건을 DBMS에 걸어야 키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 실제로 살아난다.

---

## Ⅴ. 기대효과 및 결론

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 좋으면 중복 제거, 조인 안정성, 장애 복구가 함께 쉬워진다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질은 결국 키 설계에서 출발한다.
[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 UUID (Universally Unique [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))처럼 전역 유일성과 운영 편의성을 함께 보는 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 전략이 중요해진다.
기술사는 이 주제를 "행을 찾는 표지판과 관계를 지키는 울타리"로 기억하면 된다.

- **📢 섹션 요약 비유**: 좋은 키는 품질과 운영의 첫 번째 안전장치다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| PK | 행을 유일하게 식별한다 |
| FK | 부모 행과 자식 행을 연결한다 |
| UK | 대체 유일성을 보장한다 |
| [Candidate key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | 후보 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 집합이다 |
| [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 중복과 이상 현상을 줄인다 |
| UUID | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경의 전역 식별에 쓰인다 |

### 📈 관련 키워드 및 발전 흐름도

```text
도메인 속성
  │
  ▼
후보키 선택
  │
  ▼
PK/UK 확정
  │
  ▼
FK 연결
  │
  ▼
정규화와 무결성 검증
```

### 👶 어린이를 위한 3줄 비유 설명

1. 도서관 책마다 바코드가 있어야 책을 헷갈리지 않는 것과 같다.
2. 다른 책을 빌릴 때도 번호표를 보고 연결해야 반납이 틀리지 않는다.
3. 번호표가 자꾸 바뀌면 혼란이 생기니, 잘 안 바뀌는 표식을 쓰는 게 좋다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 78 / 600

← **이전**: [77. 사용자 정의 무결성 (User-defined Integrity) - 업무 규칙에 따른 제약 (CHECK 제약조건 등)](/knowledge-base/studynote/05_database/02_modeling_normalization/077_user_defined_integrity_check_trigger/)
**다음**: [079. NULL 무결성과 NOT NULL 제약조건](/knowledge-base/studynote/05_database/02_modeling_normalization/079_null_integrity_not_null/) →

---
