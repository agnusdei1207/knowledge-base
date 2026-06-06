---
title: "086. Weak Entity Identifying Relationship"
tags:
  - "database"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Weak Entity(약한 개체)는 ER (Entity-[Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)) 모델에서 독립 PK를 갖지 못하고 부모 개체에 종속되는 개체다.
> 2. **가치**: 부분 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)와 [식별 관계](/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/)를 함께 써야 전역적으로 유일하게 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 있다.
> 3. **판단 포인트**: 전체 참여와 삭제 정책을 이해해야 정규화와 물리 설계가 흔들리지 않는다.

---

## Ⅰ. 개요 및 필요성
약한 개체는 부모가 있어야 이름이 완성된다. 예를 들어 주문(Order) 없이는 주문항목(Line Item)이 어떤 항목인지 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 없다.

그래서 약한 개체는 부모 키와 부분 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 함께 써서 구분한다.
- **📢 섹션 요약 비유**: 부모 이름이 있어야 자식 이름이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 요소 | 의미 | 설계 포인트 |
|:---|:---|:---|
| Strong Entity | 독립 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 가능 | 자체 PK 보유 |
| Weak Entity | 부모에 종속 | 독립 PK 없음 |
| Partial [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 부모 안에서만 유일 | line_no, 순번 |
| [Identifying](/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 종속 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 부모 키 포함 |
| Total Participation | 반드시 부모와 연결 | 존재 의존성 |

+--------------+      +----------------+
|  주문(Order) |--◇--->| 주문항목(Line) |
+--------------+      +----------------+
       PK: order_id           partial [key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/): line_no
- **📢 섹션 요약 비유**: 부분 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)와 부모 키를 같이 본다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | Strong Entity | Weak Entity | Associative Entity |
|:---|:---|:---|:---|
| 독립 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 가능 | 불가 | 가능 |
| PK 구성 | 자체 PK | 부모 PK + partial [key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 중심 |
| 존재 의존성 | 낮음 | 높음 | 중간 |

약한 개체는 “부모 키에 매달린 존재”라는 점이 핵심이다.
- **📢 섹션 요약 비유**: 강한 개체와 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- [ ] 부모 개체가 명확히 정의되어 있는지 확인한다.
- [ ] 부분 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)가 부모 범위 내에서만 유일한지 검토한다.
- [ ] [식별 관계](/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/)와 전체 참여를 ER 다이어그램에 표시한다.
- [ ] 부모 삭제 시 자식 처리 규칙을 정한다.
- [ ] [외래 키](/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)(FK, Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))와 복합 키 구성을 점검한다.

- ❌ 약한 개체를 강한 개체처럼 독립 PK로만 취급하는 것
- ❌ 부모가 없어도 존재 가능한 것처럼 모델링하는 것
- **📢 섹션 요약 비유**: 삭제와 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 규칙을 같이 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론
약한 개체는 혼자서는 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 완성되지 않는다. 부모와 함께 있을 때만 존재와 이름이 완성되는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조다.
- **📢 섹션 요약 비유**: 종속성을 이해하면 키 설계가 쉬워진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 약한 개체 | 부모 없이는 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 완성되지 않는다. |
| [식별 관계](/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/) | 부모 키를 함께 전달한다. |
| 부분 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 부모 안에서만 유일하다. |
| 전체 참여 | 자식이 부모에 반드시 연결된다. |
| PK (Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) | 복합 키로 완성되는 경우가 많다. |

### 📈 관련 키워드 및 발전 흐름도

```text
부모 개체 선택 -> 부분 식별자 정의 -> 식별 관계 연결 -> 복합 키 생성 -> 약한 개체 완성
```

### 👶 어린이를 위한 3줄 비유 설명

1. 가족 성이 먼저 있어야 이름이 완성되는 아이와 비슷하다.
2. 혼자서는 누구인지 못 알아보지만, 가족 이름이 붙으면 바로 알 수 있다.
3. 부모를 잃으면 아이의 이름도 같이 사라진다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 86 / 600

<- **이전**: [85. 참여 제약조건 (Participation Constraint) - 필수 참여(전체), 선택 참여(부분)](/studynote/05_database/02_modeling_normalization/085_participation_constraint_total_partial/)
**다음**: [87. 식별 관계 (Identifying) vs 비식별 관계 (Non-identifying)](/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/) ->

---
