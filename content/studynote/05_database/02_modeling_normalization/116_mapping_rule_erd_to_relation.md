+++
title = "116. 매핑 규칙 (ERD→릴레이션 매핑) - 엔터티·관계·속성의 체계적 변환"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 매핑 규칙은 개념 설계의 ERD(엔터티·[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))를 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계의 **[릴레이션 스키마](/knowledge-base/studynote/05_database/07_exam_summary/391_relation_schema_intension/)(테이블·PK·FK·컬럼)**로 변환하는 **체계적 규칙 집합**이다.
> 2. **가치**: 규칙 없이 직감으로 변환하면 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 누락·PK 오류·중복 테이블이 발생하므로, **7대 매핑 규칙**을 순서대로 적용하여 정확한 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)을 도출한다.
> 3. **판단 포인트**: 1:1, 1:N, M:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 변환 방식이 각각 다르며, **M:N → 교차 테이블 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)**, **다치 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) → 별도 테이블 분리**, **약한 엔터티 → 소유자 FK 포함 복합 PK**를 정확히 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    7대 매핑 규칙 순서                                  │
├───────────────────────────────────────────────────────┤
│  1. 강한 엔터티 → 테이블 (PK = 식별자)               │
│  2. 약한 엔터티 → 테이블 (PK = 소유자FK + 부분키)    │
│  3. 1:1 관계 → 한쪽 테이블에 FK 추가                 │
│  4. 1:N 관계 → N쪽 테이블에 FK 추가                  │
│  5. M:N 관계 → 교차 테이블 생성 (양쪽 PK가 복합키)   │
│  6. 다치 속성 → 별도 테이블 분리                      │
│  7. N-ary 관계 → 관계 테이블 생성                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 매핑 규칙은 외국어 번역 문법이다. "주어+동사+목적어" 순서를 지키지 않으면 엉뚱한 문장(잘못된 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 유형별 매핑

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 매핑 방식 | 예시 |
|:---|:---|:---|
| **1:1** | 한쪽에 FK (가능하면 전참여 쪽) | 사원←→여권 |
| **1:N** | N쪽에 FK | 부서←→사원 |
| **M:N** | **교차 테이블** | 학생←→과목 → 수강(학생ID, 과목ID) |
| **약한 엔터티** | 소유자 FK + 부분키 = 복합 PK | 주문←→주문상세 |
| **다치 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)** | 별도 테이블 + FK | 사원(취미) → 취미(사원ID, 취미명) |

- **📢 섹션 요약 비유**: M:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 학생과 과목이 서로 "누가 누구를 듣는지" 모르므로, **수강 기록부(교차 테이블)**를 만들어 연결하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 1:1 | 1:N | M:N |
|:---|:---|:---|:---|
| **FK 위치** | 한쪽 | N쪽 | **교차 테이블** |
| **테이블 수** | 동일 | 동일 | **+1 (교차)** |
| **복잡도** | 낮음 | 낮음 | **높음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 답안 작성
1. ERD에서 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 유형(1:1/1:N/M:N) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/).
2. 매핑 규칙 번호를 명시하며 변환 과정 서술.
3. 결과 [릴레이션 스키마](/knowledge-base/studynote/05_database/07_exam_summary/391_relation_schema_intension/)에 PK·FK·NULL 여부 명시.

---

## Ⅴ. 기대효과 및 결론

매핑 규칙은 DB 설계의 "번역 문법"이며, 이를 체계적으로 적용하면 ERD의 비즈니스 의미를 **손실 없이 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 변환**할 수 있다. CASE 도구(ERwin, [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)#)가 이 규칙을 자동으로 적용하여 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ERD** | 매핑 규칙의 입력 |
| **[릴레이션 스키마](/knowledge-base/studynote/05_database/07_exam_summary/391_relation_schema_intension/)** | 매핑 규칙의 출력 |
| **교차 테이블** | M:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 매핑의 핵심 산출물 |
| **[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)** | 매핑 후 적용하는 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계 |
| **약한 엔터티** | 소유자 FK + 부분키 복합 PK 매핑 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ER 모델 (Chen, 1976) — 개념적 데이터 모델]
    │
    ▼
[매핑 규칙 체계화 (1980s) — ERD→릴레이션 7대 규칙]
    │
    ▼
[CASE 도구 (ERwin, 1990s) — 자동 매핑 구현]
    │
    ▼
[Schema-as-Code (2020s) — 코드 기반 스키마 생성]
    │
    ▼
[현재: AI 기반 ERD→스키마 자동 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ERD는 "학생이 과목을 듣는다"라는 **[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 그림**으로 표현한 거예요.
2. 매핑 규칙은 이 그림을 **컴퓨터가 이해하는 표(테이블)**로 바꾸는 번역 문법이에요.
3. "학생↔과목" 같은 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 **수강 기록부(교차 테이블)**를 만들어서 연결한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 116 / 600

← **이전**: [115. 논리 설계와 정규화 (Logical Design & Normalization) - ERD→릴레이션 변환·FD 분석](/knowledge-base/studynote/05_database/02_modeling_normalization/115_logical_design_normalization/)
**다음**: [117. 물리 데이터베이스 설계 (Physical DB Design) - 인덱스·파티셔닝·스토리지 최적화](/knowledge-base/studynote/05_database/02_modeling_normalization/117_physical_database_design_indexing/) →

---
