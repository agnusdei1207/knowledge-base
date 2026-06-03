---
title: 115. 논리 설계와 정규화 (Logical Design & Normalization) - ERD→릴레이션 변환·FD 분석
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[369_logic_bomb|논리]] 설계는 개념 설계(ERD)를 **[[083_relationship_in_er_model|관계]]형 [[391_relation_schema_intension|릴레이션 스키마]](테이블·PK·FK)**로 변환한 후, **함수 [[008_dependencies|종속성]](FD) 분석을 통해 [[093_normalization|정규화]]([[105_third_normal_form_3nf_transitive|3NF]]/[[529_bcnf|BCNF]])**를 수행하여 [[093_update_anomaly|갱신 이상]]을 제거하는 단계다.
> 2. **가치**: ERD의 엔터티·[[083_relationship_in_er_model|관계]]·[[082_attribute_types_er_model|속성]]을 체계적 규칙(1:N→FK, M:N→교차 테이블)에 따라 [[061_relation_schema_instance|릴레이션]]으로 변환하고, FD 분석으로 부분·이행·[[095_determinant_dependent|결정자]] 이상 [[008_dependencies|종속성]]을 식별하여 분해한다.
> 3. **판단 포인트**: [[093_normalization|정규화]]의 각 단계([[103_first_normal_form_1nf_atomic_value|1NF]]→[[104_second_normal_form_2nf_full_fd|2NF]]→[[105_third_normal_form_3nf_transitive|3NF]]→[[529_bcnf|BCNF]])에서 **제거되는 [[008_dependencies|종속성]] 유형**을 정확히 구분하고, [[093_normalization|정규화]] 완료 후 **[[101_lossless_join_decomposition|무손실 분해]]·[[102_dependency_preservation_decomposition|종속성 보존]]** 조건을 [[395_verification_process_review|검증]]해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    논리 설계 흐름                                      │
├───────────────────────────────────────────────────────┤
│  [ERD]                                                │
│   엔터티(고객, 주문, 상품) + 관계(구매, 포함)         │
│      │                                                │
│      ▼ 변환 규칙 적용                                 │
│  [릴레이션 스키마]                                    │
│   고객(고객ID PK, 이름, 주소)                         │
│   주문(주문ID PK, 고객ID FK, 날짜)                    │
│   주문상세(주문ID PK, 상품ID PK FK, 수량)             │
│      │                                                │
│      ▼ FD 분석 + 정규화                               │
│  [정규화된 스키마]                                    │
│   부분FD 제거(2NF), 이행FD 제거(3NF),                │
│   결정자 조건(BCNF) → 갱신 이상 없음                 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ERD→[[061_relation_schema_instance|릴레이션]] 변환은 한국어→영어 번역이고, [[093_normalization|정규화]]는 번역된 영어 문장의 문법 검사([[093_update_anomaly|갱신 이상]] 제거)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[093_normalization|정규화]] 단계별 제거 대상

| 정규형 | 제거 대상 | 조건 |
|:---|:---|:---|
| **[[103_first_normal_form_1nf_atomic_value|1NF]]** | 반복 그룹, 비원자값 | 모든 [[082_attribute_types_er_model|속성]]이 원자값 |
| **[[104_second_normal_form_2nf_full_fd|2NF]]** | 부분 함수 종속 | 기본키 일부 → 일반 [[082_attribute_types_er_model|속성]] |
| **[[105_third_normal_form_3nf_transitive|3NF]]** | 이행 함수 종속 | A→B→C에서 A→C 제거 |
| **[[529_bcnf|BCNF]]** | [[095_determinant_dependent|결정자]] 조건 위반 | 모든 [[095_determinant_dependent|결정자]]가 후보키 |

### ERD→[[061_relation_schema_instance|릴레이션]] 변환 규칙

| ERD 요소 | [[061_relation_schema_instance|릴레이션]] 변환 |
|:---|:---|
| 강한 엔터티 | 독립 테이블 + PK |
| 약한 엔터티 | 테이블 + 소유자 FK (PK에 포함) |
| 1:N [[083_relationship_in_er_model|관계]] | N쪽 테이블에 FK 추가 |
| M:N [[083_relationship_in_er_model|관계]] | **교차 테이블** (양쪽 PK가 복합키) |
| 다치 [[082_attribute_types_er_model|속성]] | 별도 테이블로 분리 |

- **📢 섹션 요약 비유**: [[093_normalization|정규화]]는 "한 서랍에 양말과 속옷을 섞어 넣지 않는 것"이다. 섞으면 양말을 꺼낼 때 속옷이 따라 나오는 [[090_anomaly_insertion_deletion_update|이상 현상]]([[093_update_anomaly|갱신 이상]])이 발생한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 비정규형 | [[105_third_normal_form_3nf_transitive|3NF]] | [[529_bcnf|BCNF]] |
|:---|:---|:---|:---|
| **중복** | 많음 | 최소 | **최소** |
| **[[093_update_anomaly|갱신 이상]]** | 빈번 | 대부분 제거 | **완전 제거** |
| **[[102_dependency_preservation_decomposition|종속성 보존]]** | - | **보장** | 보장 안 될 수 있음 |
| **실무** | 안 됨 | 대부분 채택 | 이상적 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 답안 핵심
1. FD 분석: "주문ID → 고객ID, 날짜" (완전 FD [[396_validation|확인]]).
2. [[093_normalization|정규화]]: "고객ID → 이름, 주소"가 이행 FD인 경우 분해.
3. [[101_lossless_join_decomposition|무손실 분해]] [[395_verification_process_review|검증]]: 분해 후 자연 조인으로 원본 복원 가능 [[396_validation|확인]].

---

## Ⅴ. 기대효과 및 결론

[[369_logic_bomb|논리]] 설계와 [[093_normalization|정규화]]는 DB 설계의 **수학적 토대**이며, 올바른 [[093_normalization|정규화]] 없이 물리 설계([[111_denormalization_performance_tradeoff|역정규화]])를 논의하는 것은 무의미하다. Schema-as-Code와 [[190_ai_llm_requirements_specification|AI]] 기반 FD 자동 탐지가 결합하여 [[093_normalization|정규화]] 프로세스가 자동화되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ERD** | [[369_logic_bomb|논리]] 설계의 입력 (개념 설계 산출물) |
| **함수 [[008_dependencies|종속성]] (FD)** | [[093_normalization|정규화]]의 분석 대상 |
| **[[101_lossless_join_decomposition|무손실 분해]]** | [[093_normalization|정규화]] 분해의 [[002_bigdata_5v|정확성]] [[395_verification_process_review|검증]] 조건 |
| **[[111_denormalization_performance_tradeoff|역정규화]]** | [[093_normalization|정규화]] 완료 후 물리 설계에서 적용 |
| **[[529_bcnf|BCNF]]** | 모든 [[095_determinant_dependent|결정자]]가 후보키인 이상적 정규형 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ER 모델 (Chen, 1976) — 개념 설계→논리 설계 변환 기초]
    │
    ▼
[정규화 이론 (Codd, 1970s) — 1NF~3NF 체계 확립]
    │
    ▼
[BCNF (1974) — 결정자 조건 강화]
    │
    ▼
[자동 정규화 도구 (2000s) — CASE 도구 내장]
    │
    ▼
[현재: AI FD 자동 탐지 — 데이터에서 종속성 자동 추출]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ERD는 "이 방에는 침대, 저 방에는 책상"이라고 **집 구조를 정하는 것**이에요.
2. [[093_normalization|정규화]]는 "양말 서랍에 속옷을 섞지 않기"처럼 **물건을 깔끔하게 정리하는 규칙**이에요.
3. 잘 정리하면 나중에 양말을 찾을 때 **속옷이 따라 나오는 이상한 일([[093_update_anomaly|갱신 이상]])**이 안 생긴답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 600

← **이전**: [[114_database_design_phases|114. 데이터베이스 설계 단계 (Database Design Phases) - 개념·논리·물리 3단계 체계]]
**다음**: [[116_mapping_rule_erd_to_relation|116. 매핑 규칙 (ERD→릴레이션 매핑) - 엔터티·관계·속성의 체계적 변환]] →

---
