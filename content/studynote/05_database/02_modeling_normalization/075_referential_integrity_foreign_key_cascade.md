+++
title = "75. 참조 무결성 (Referential Integrity) - 외래 키 값은 참조하는 릴레이션의 기본키 값이거나 NULL이어야 함"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Referential](/knowledge-base/studynote/05_database/07_exam_summary/406_referential_integrity_foreign_key/) [Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))은 자식 행의 [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) (Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))가 존재하지 않는 부모를 가리키지 못하게 막는 규칙이다.
> 2. **가치**: ON DELETE CASCADE 같은 동작 규칙은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제가 전파될지, 차단될지, 빈값으로 바뀔지를 명시해 애플리케이션의 숨은 버그를 줄인다.
> 3. **판단 포인트**: CASCADE는 편하지만 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·정산·이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 과삭제 위험이 있으므로, 의도된 소유 관계일 때만 써야 한다.

---

## Ⅰ. 개요 및 필요성

관계형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스는 테이블 간 연결이 많기 때문에, 한쪽이 지워졌는데 다른 쪽이 그대로 남는다면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 금방 꼬인다. [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 이런 "고아 행"을 막기 위한 안전장치다.

`SQL (Structured Query Language)`에서 [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) 제약은 단순한 문법이 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생명주기 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 부모 행이 사라질 때 자식도 같이 사라질지, 막을지, 빈값으로 남길지를 미리 정해야 운영 중 예외를 줄일 수 있다.

```text
Parent PK ---► Child FK
   |             |
   +- RESTRICT   +- no delete
   +- CASCADE    -+- delete child
   +- SET NULL   -+- keep row
```

이 규칙이 없으면 조인은 되지만 의미는 무너진다.

- **📢 섹션 요약 비유**: 연결선이 끊기면 장부가 아니라 조각이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)는 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이 아니라, 갱신과 삭제에 대한 동작도 함께 정의한다. 즉 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "존재 여부"와 "변경 전파"를 같이 다루는 제약이다.

| 동작 | 의미 | 주의점 |
| :--- | :--- | :--- |
| RESTRICT / NO ACTION | 부모 삭제 차단 | 가장 보수적 |
| CASCADE | 자식도 함께 변경/삭제 | 과삭제 위험 |
| SET NULL | [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 비움 | NULL 허용 필요 |
| SET DEFAULT | 기본값으로 교체 | 기본값의 의미 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

인덱스가 없으면 제약 검사 비용이 커진다. 그래서 FK는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 규칙이면서 동시에 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 설계와도 연결된다.

- **📢 섹션 요약 비유**: 문은 잠그고, 열쇠는 정해진 사람에게만 준다.

---

## Ⅲ. 비교 및 연결

[참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "존재하는 부모를 가리키는가"를 묻고, entity integrity는 "기본키가 비어 있지 않은가"를 묻는다. 둘은 비슷해 보이지만 대상이 다르다.

| 비교 축 | [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) | CASCADE |
| :--- | :--- | :--- |
| 목적 | 잘못된 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 차단 | 전파 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 지정 |
| 성격 | 규칙 | 행동 |
| 위험 | 고아 행 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 삭제 폭발 |

또 하나의 경계는 cascade와 soft delete다. 이력과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 중요한 시스템은 물리 삭제보다 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 삭제가 더 안전한 경우가 많다.

- **📢 섹션 요약 비유**: 열쇠가 맞는지 보는 일과 문을 같이 여는 일은 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 자식의 생명주기가 부모에 완전히 종속될 때만 CASCADE를 쓴다. 주문과 주문상세처럼 부모 없이는 자식이 의미 없는 경우가 대표적이다.

체크 포인트는 다음과 같다.
- FK 컬럼에 인덱스가 있는가.
- 대량 삭제 시 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 범위를 감당할 수 있는가.
- [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·정산·법적 보존 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 물리 삭제를 쓰지 않는가.

안티패턴은 "편하니까 CASCADE"다. 특히 다단계 cascade는 작은 실수 하나로 많은 행을 날릴 수 있으므로, 운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 더 조심해야 한다.

- **📢 섹션 요약 비유**: 편리한 자동문도 방향을 잘못 잡으면 위험하다.

---

## Ⅴ. 기대효과 및 결론

FK 제약은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 마지막 선이다. 사람이 깜빡해도 DB가 막아 주므로, 결함이 코드 레벨로 번지기 전에 멈출 수 있다.

결국 기억할 것은, [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)는 단지 연결선이 아니라 관계의 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이라는 점이다. 어떤 연결은 끊으면 안 되고, 어떤 연결은 같이 움직여야 하며, 그 기준을 DB가 대신 보증한다.

- **📢 섹션 요약 비유**: 가족사진의 이름표가 맞아야 누구인지 알 수 있다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 부모의 고유 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 부모를 가리키는 연결 |
| Cascade | 변경/삭제 전파 |
| Restrict | 삭제 차단 |
| Soft Delete | 이력 보존을 위한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 삭제 |

### 관련 키워드 및 발전 흐름도

```text
parent insert/update
    |
    v
FK constraint check
    |
    +-- reject
    |
    +-- propagate / set null / set default
    |
    v
commit
```

### 어린이를 위한 3줄 비유 설명

1. 엄마 이름표가 있어야 아이 이름표도 맞아요.
2. 엄마가 사라지면 아이도 같이 없어질 수 있어요.
3. 하지만 기록이 중요하면 이름표만 바꾸고 남겨 두기도 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 75 / 600

<- **이전**: [74. 개체 무결성 (Entity Integrity) / 기본 키 (Primary Key)](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/)
**다음**: [76. 도메인 무결성 (Domain Integrity) - 속성 값은 정의된 도메인에 속해야 함](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/) ->

---
