---
title: "87. 식별 관계 (Identifying) vs 비식별 관계 (Non-identifying)"
tags:
  - "database"
---


## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) (Identifying [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))는 자식 엔터티의 키가 부모 키를 포함해 구성되는 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)로, 자식의 존재와 정체성이 부모에 종속된다.
    > 2. **가치**: 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) (Non-identifying [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))는 자식이 독립된 키를 가지며 부모 키는 [외래 키](/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) (Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), FK)로만 연결된다.
    > 3. **판단 포인트**: 키 구조만 바꿔도 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)성, 존재 의존성, 삭제 전파가 달라지므로 ERD (Entity-[Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) Diagram) 설계에서 의도를 정확히 표현해야 한다.

    ---

    ## Ⅰ. 개요 및 필요성

    ERD (Entity-[Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) Diagram)에서 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 그리는 목적은 단순 연결이 아니라 키와 존재 의존성을 표현하는 데 있다. [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 자식이 부모 없이는 의미가 없고, 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 자식이 독립적으로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)될 수 있다는 차이를 드러낸다.

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델링에서 이 구분이 중요한 이유는 삭제, 갱신, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 결과가 달라지기 때문이다. 같은 1:N [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)라도 키를 어떻게 구성하느냐에 따라 업무 의미와 물리 설계가 달라진다.

    - **📢 섹션 요약 비유**: 부모 이름이 적힌 명찰이 필요한지, 자식만의 명찰이 필요한지 정하는 일이다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 보통 약한 엔터티 ([Weak Entity](/studynote/05_database/02_modeling_normalization/086_weak_entity_identifying_relationship/))와 연결된다. 자식의 Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) (PK)에 부모의 PK가 포함되며, [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)선은 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)로 작동한다.

| 구분 | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :-- | :-- | :-- |
| 자식 키 | 부모 키 포함한 복합 PK | 독립 PK + FK |
| 존재 의존성 | 강함 | 약함 |
| 삭제 전파 | 부모 삭제 시 자식 의미 상실 가능 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 따라 선택 |
| 표기 감각 | 강한 소속감 | 느슨한 연결 |

```text
식별 관계:   Parent --< Child(PK = ParentPK + ChildSeq)
비식별 관계: Parent --.. Child(PK = ChildID, FK = ParentPK)
```

[식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 "자식의 이름표에 부모 이름이 같이 적히는가"로 이해하면 쉽다. 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 자식이 자기 이름표를 따로 갖고 부모는 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)만 하는 방식이다.

    - **📢 섹션 요약 비유**: 가족 명단에 함께 적히는지, 따로 주소록에 적히는지의 차이로 보면 쉽다.

    ---

    ## Ⅲ. 비교 및 연결

    [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)보다 결합이 강하지만, 항상 좋은 것은 아니다. 강한 결합은 의미를 명확히 해 주지만, 자식의 독립적 변경과 재사용은 어렵게 만든다.

| 비교 포인트 | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :-- | :-- | :-- |
| 대표 예 | 주문-주문항목 | 고객-주소록 |
| 키 설계 | 복합 PK | 대리키([surrogate key](/studynote/12_it_management/05_security_compliance/956_surrogate_key/)) 가능 |
| [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 관점 | 부모 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 핵심 | 자식 독립성이 중요 |
| 변경 유연성 | 낮음 | 높음 |

연결 관점에서는 카디널리티만 보는 것이 아니라, 부모 없이는 자식이 성립하는지까지 봐야 한다. 즉 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)선의 모양보다 "업무 의미의 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)"이 더 본질적이다.

    - **📢 섹션 요약 비유**: 같은 친구라도 이름표가 하나인지 둘인지에 따라 관리 방식이 달라진다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 자식 레코드가 부모 없이 존재할 수 없는지 먼저 물어보면 된다. 주문항목, 송장라인처럼 부모 스코프 안에서만 의미가 있는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 어울리고, 회원-주소처럼 자식이 독립 생명주기를 가지면 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 더 자연스럽다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 자식의 정체성이 부모 없이는 정의되지 않는가?
2. 자식 키를 부모 키에 종속시키는 것이 업무 의미를 더 잘 드러내는가?
3. FK만으로도 충분한데 복합 PK를 억지로 쓰고 있지는 않은가?
4. 삭제/갱신 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 의미와 일치하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 의미 없이 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 남발하는 것
- surrogate key가 있는데도 복합 PK를 억지로 추가하는 것
- 모델 의도와 물리 제약을 분리하지 않는 것

    - **📢 섹션 요약 비유**: 자식이 혼자 살 수 없는데도 독립해 보이게 적으면, 나중에 정리가 어렵다.

    ---

    ## Ⅴ. 기대효과 및 결론

    [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)와 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 차이는 키 설계 그 자체보다, 업무 의미를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델에 얼마나 정확히 담았는지에서 드러난다. 올바르게 선택하면 제약 조건과 조인 조건이 자연스럽게 정렬된다.

따라서 ERD에서 이 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 단순 선 하나가 아니라, 존재 의존성과 정체성의 강도를 표현하는 장치로 기억해야 한다.

    - **📢 섹션 요약 비유**: 가방 안에만 존재하는 물건인지, 따로 꺼내도 되는 물건인지 구분하는 것과 같다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| ERD (Entity-[Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) Diagram) | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 의미를 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| Identifying [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 자식 PK에 부모 PK 포함 |
| Non-identifying [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 자식 PK와 부모 FK 분리 |
| PK (Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) | 자식 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| FK (Foreign [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) | 부모 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |

    ### 📈 관련 키워드 및 발전 흐름도

    엔터티 의미 파악
    |
    v
존재 의존성 판단
    |
    v
[식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) / 비식별 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 선택
    |
    v
PK / FK / 삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 정렬

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 어떤 물건은 엄마 이름이 같이 적혀 있어야 누군지 알아요.
    2. 어떤 물건은 자기 이름만 있어도 혼자 구별돼요.
    3. 그래서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 같이 사는지, 따로 사는지 나눠 적어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 87 / 600

<- **이전**: [86. 약한 개체 (Weak Entity) - 이중 사각형, 부모 개체에 종속 (식별 관계)](/studynote/05_database/02_modeling_normalization/086_weak_entity_identifying_relationship/)
**다음**: [88. 식별자 (Identifier) - ER 모델에서의 키](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/) ->

---
