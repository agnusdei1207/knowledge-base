+++
title = "73. 무결성 제약조건 (Integrity Constraints)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약조건은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 강제하는 규칙이다.
> 2. **가치**: 잘못된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력과 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 막아 준다.
> 3. **판단**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/), 키, 개체, [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 엉키면 시스템 전체가 흔들린다. 제약조건은 이를 막는 방어막이다.

그래서 DB 설계의 핵심이다.

- **📢 섹션 요약 비유**: 울타리가 있어야 정원이 망가지지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data
  ↓ constraints
Integrity
```

| 종류 | 의미 |
| :-- | :-- |
| [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 값의 범위 |
| [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 유일성 |
| Entity | NULL 불가 |
| [Referential](/knowledge-base/studynote/05_database/07_exam_summary/406_referential_integrity_foreign_key/) | [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) |

제약조건은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 현실과 맞도록 강제한다.

- **📢 섹션 요약 비유**: 규칙이 있어야 장난감이 안 망가진다.

---

## Ⅲ. 비교 및 연결

| 유형 | 의미 |
| :-- | :-- |
| [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 허용 값 |
| [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) |
| Entity | 행 존재 |
| [Referential](/knowledge-base/studynote/05_database/07_exam_summary/406_referential_integrity_foreign_key/) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |

| 효과 | 설명 |
| :-- | :-- |
| [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| Correctness | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) |

[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약은 DB의 신뢰성을 지키는 기본 도구다.

- **📢 섹션 요약 비유**: 잘못된 값은 문 앞에서 막는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 각 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)의 의미를 아는가?
2. 제약을 DB 수준에서 강제하는가?
3. [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 지키는가?
4. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 연결하는가?
5. 설계 단계에서 반영하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 애플리케이션만 믿는 설계
- 제약을 너무 늦게 거는 설계
- [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 종류를 혼동하는 설계
- 규칙 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 쌓는 설계

기술사 관점에서는 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약조건을 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) 강제 규칙"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 잘못된 값은 처음부터 못 들어오게 한다.

---

## Ⅴ. 기대효과 및 결론

[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약조건은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 신뢰성을 높인다.

결론적으로 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약조건은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 강제하는 규칙이다.

- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정원을 지키는 울타리다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Constraints</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Integrity</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Quality</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Domain / Key / Entity / Referential</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Integrity Constraints</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Quality</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

규칙을 정해요.  
틀린 값은 막아요.  
제약조건은 그런 약속이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 600

← **이전**: [72. 외래 키 (Foreign Key, FK) - 다른 릴레이션의 기본 키를 참조하는 속성](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)
**다음**: [74. 개체 무결성 (Entity Integrity) / 기본 키 (Primary Key)](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/) →

---
