---
title: "114. 데이터베이스 설계 단계 (Database Design Phases) - 개념·논리·물리 3단계 체계"
date: "2026-04-19"
tags:
  - "studynote-database"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DB 설계는 <strong>개념 설계(ERD, <a href="/studynote/05_database/04_transactions_concurrency/502_dbms/">DBMS</a> 독립) -> <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 설계(<a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>, <a href="/studynote/05_database/07_exam_summary/391_relation_schema_intension/">릴레이션 스키마</a>) -> 물리 설계(<a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>·<a href="/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/">역정규화</a>·<a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a>)</strong>의 3단계로 진행되며, 각 단계는 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 수준이 다르고 산출물이 명확히 구분된다.
> 2. **가치**: 개념 설계를 건너뛰고 바로 테이블을 만드는 것은 "설계도 없이 건물을 짓는 것"과 같으며, 요구 변경 시 전체 DB를 재구축해야 하는 재앙을 초래한다.
> 3. **판단 포인트**: 기술사 시험에서는 3단계 각각의 <strong>산출물·핵심 활동·변환 규칙</strong>을 정확히 구분하여 서술해야 하며, [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)->물리 전환 시 <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화(<a href="/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/">역정규화</a>·<a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>)</strong> 판단 근거를 제시하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    DB 설계 3단계 흐름도                                |
+-------------------------------------------------------+
|  [요구 분석]                                          |
|      |  "고객이 주문하고, 상품을 배송한다"             |
|      v                                                |
|  [1단계: 개념 설계]                                   |
|      산출물: ERD (엔터티·속성·관계)                    |
|      DBMS 독립, 비즈니스 관점                          |
|      |                                                |
|      v                                                |
|  [2단계: 논리 설계]                                   |
|      산출물: 릴레이션 스키마 (테이블·PK·FK)            |
|      정규화 (3NF/BCNF), DBMS 유형 결정                |
|      |                                                |
|      v                                                |
|  [3단계: 물리 설계]                                   |
|      산출물: 물리 테이블·인덱스·역정규화·파티셔닝      |
|      성능 최적화, 특정 DBMS 종속                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 개념 설계는 건물의 조감도(어떤 방이 있는지), [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계는 평면도(방 크기·문 위치), 물리 설계는 시공 도면(콘크리트 두께·배관 위치)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3단계 비교표

| 단계 | 관점 | 산출물 | 핵심 활동 | [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 종속 |
|:---|:---|:---|:---|:---|
| **개념** | 비즈니스 | ERD | 엔터티·[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | **독립** |
| <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a></strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 | [릴레이션 스키마](/studynote/05_database/07_exam_summary/391_relation_schema_intension/) | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), PK/FK 정의 | 유형 결정 |
| **물리** | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/), [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/), [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | **종속** |

### 개념->[논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 변환 규칙

| ERD 요소 | [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 변환 |
|:---|:---|
| 엔터티 | 테이블 |
| [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 컬럼 |
| 1:N [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | FK (N쪽에 추가) |
| M:N [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 교차 테이블 (연결 엔터티) |
| [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | PK |

- **📢 섹션 요약 비유**: ERD->[릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 변환은 한국어->영어 번역이다. 같은 의미(비즈니스 규칙)를 다른 형식(테이블 구조)으로 옮기는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 개념 설계 | [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계 | 물리 설계 |
|:---|:---|:---|:---|
| **질문** | "무엇을 저장?" | "어떤 구조로?" | "어떻게 빠르게?" |
| **도구** | ERD 도구 | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 전용 [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/) |
| **변경 비용** | 낮음 | 중간 | **높음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 답안 구성 포인트
1. **개념 설계**: 비즈니스 규칙에서 엔터티·[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 도출하는 과정.
2. <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 설계</strong>: ERD->[릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 변환 + [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(FD 분석 -> [3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)/[BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/)).
3. **물리 설계**: [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 측정 -> 병목 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) -> [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)/[인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 판단.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **개념 설계 생략**: 바로 CREATE TABLE -> 요구 변경 시 전체 재구축.

---

## Ⅴ. 기대효과 및 결론

3단계 설계를 충실히 따르면 <strong>요구 변경에 유연하고, <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화가 체계적이며, 유지보수가 용이한</strong> DB를 구축할 수 있다. 최근에는 ERD를 코드로 관리하는 Schema-as-Code(Prisma, DBdiagram.io)가 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 파이프라인에 통합되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ERD** | 개념 설계의 핵심 산출물 |
| <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a></strong> | [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계의 핵심 활동 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/">역정규화</a></strong> | 물리 설계의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 기법 |
| <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a></strong> | 물리 설계의 조회 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 도구 |
| <strong><a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a></strong> | 물리 설계의 대용량 테이블 관리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ER 모델 (Chen, 1976) — 개념 설계 체계 확립]
    |
    v
[정규화 이론 (Codd, 1970s) — 논리 설계 수학적 기반]
    |
    v
[물리 설계 패턴 (1990s) — 인덱스·역정규화·파티셔닝]
    |
    v
[Schema-as-Code (2020s) — Prisma·DBdiagram.io]
    |
    v
[현재: AI 기반 스키마 추천 — 요구사항에서 ERD 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>개념 설계</strong>는 "이 집에는 거실·부엌·침실이 필요해!"라고 <strong>큰 그림</strong>을 그리는 거예요.
2. <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 설계</strong>는 "거실은 5×5m, 부엌은 3×3m"처럼 <strong>정확한 크기</strong>를 정하는 거예요.
3. <strong>물리 설계</strong>는 "벽 두께 20cm, 수도관 위치는 여기"처럼 <strong>실제로 짓는 방법</strong>을 정하는 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 114 / 600

<- **이전**: [113. 역정규화 기법 (Denormalization Techniques) - 테이블 병합·분할·중복 컬럼](/studynote/05_database/02_modeling_normalization/113_denormalization_techniques_merge_split/)
**다음**: [115. 논리 설계와 정규화 (Logical Design & Normalization) - ERD->릴레이션 변환·FD 분석](/studynote/05_database/02_modeling_normalization/115_logical_design_normalization/) ->

---
