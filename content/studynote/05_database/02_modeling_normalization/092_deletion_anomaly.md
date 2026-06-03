---
title: 92. 삭제 이상 (Deletion Anomaly) - 연쇄 삭제로 인해 필요한 데이터까지 소실되는 현상
tags:
- database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 삭제 이상 (Deletion [[530_anomaly|Anomaly]])은 [[093_normalization|정규화]]되지 않은 [[061_relation_schema_instance|릴레이션]](테이블)에서 특정 [[001_dikw_pyramid|데이터]]를 삭제할 때, 의도하지 않은 다른 필수 [[001_dikw_pyramid|데이터]]까지 연쇄적으로 소멸하는 부작용이다.
> 2. **가치**: 이 문제를 이해하고 해결([[093_normalization|정규화]])하면, [[002_database_definition|데이터베이스]]의 [[001_dikw_pyramid|데이터]] 정합성을 유지하고 [[003_integrity|무결성]] 훼손을 방지할 수 있다.
> 3. **판단 포인트**: 하나의 [[061_relation_schema_instance|릴레이션]]에 두 개 이상의 이질적인 독립 개체(Entity) 테마가 혼재되어 있다면, 삭제 이상 발생 위험이 높으므로 [[101_lossless_join_decomposition|무손실 분해]]([[093_normalization|정규화]])를 수행해야 한다.

---

## Ⅰ. 개요 및 필요성
삭제 이상 (Deletion [[530_anomaly|Anomaly]])은 관계형 [[002_database_definition|데이터베이스]]에서 잘못된 테이블 설계로 인해 발생하는 [[001_dikw_pyramid|데이터]] [[093_update_anomaly|갱신 이상]]([[530_anomaly|Anomaly]])의 한 종류이다. 학생 정보와 수강 정보처럼 성격이 다른 [[001_dikw_pyramid|데이터]]를 하나의 테이블에 뭉쳐 놓았을 때, 수강 취소라는 행위를 처리하기 위해 행(Row) 전체를 지우면 그 학생의 기본 신상 정보까지 통째로 날아가는 문제가 생긴다.

이러한 현상은 [[002_database_definition|데이터베이스]]의 가장 중요한 목적인 '[[001_dikw_pyramid|데이터]]의 [[196_durability_permanent_storage|영속성]] 보장'을 심각하게 위협한다. 정상적인 트랜잭션이라 할지라도 시스템 설계의 [[352_defect_definition|결함]] 때문에 핵심 비즈니스 [[001_dikw_pyramid|데이터]]가 증발하므로, 이를 방지하기 위한 [[093_normalization|정규화]]([[093_normalization|Normalization]]) 이론이 필수적으로 등장하게 되었다.

- **📢 섹션 요약 비유**: 삭제 이상은 병원의 '진료 기록부'에 '환자 연락처'를 같이 적어두는 것과 같다. 환자가 진료 예약을 취소해서 기록부 한 줄을 지웠더니, 병원 시스템에서 환자 자체의 연락처까지 영영 사라져 버리는 치명적인 실수다.

---

## Ⅱ. 아키텍처 및 핵심 원리
삭제 이상은 [[094_functional_dependency_fd|함수적 종속성]](Functional Dependency)이 얽혀있는 비정규화 [[061_relation_schema_instance|릴레이션]]에서 발생한다. [[063_relation_tuple_cardinality|튜플]](Tuple) 단위로 삭제가 이루어지는 RDBMS(Relational [[501_database|Database]] [[372_management|Management]] System)의 특성 때문이다.

### 비정규화 테이블 구조와 삭제 연산의 병목
| 학번(PK) | 과목코드(PK) | 학생이름 | 학과 | 과목명 |
| :--- | :--- | :--- | :--- | :--- |
| 101 | DB | 김철수 | 컴퓨터 | [[002_database_definition|데이터베이스]] |
| 102 | ACC | 이영희 | 경영 | 회계학 |

```text
┌─────────────────────────────────────────────────────────────┐
│                 삭제 이상 발생 메커니즘                     │
├─────────────────────────────────────────────────────────────┤
│ 1. 삭제 의도: 학번 102의 'ACC' 과목 수강 내역 삭제          │
│                                                             │
│ 2. DB 시스템의 처리: 행(Row) 단위 삭제 연산 수행            │
│    DELETE FROM Table WHERE 학번=102 AND 과목코드='ACC';     │
│                                                             │
│ 3. 결과: 의도하지 않은 '이영희, 경영' 정보까지 동반 소멸    │
└─────────────────────────────────────────────────────────────┘
```
[[063_relation_tuple_cardinality|튜플]]을 삭제할 때 부분적인 [[082_attribute_types_er_model|속성]]([[082_attribute_types_er_model|Attribute]])만 남길 수 없으므로, 해당 [[063_relation_tuple_cardinality|튜플]]에 유일하게 존재했던 종속 [[001_dikw_pyramid|데이터]](이름, 학과)가 함께 파괴된다.

- **📢 섹션 요약 비유**: 이것은 폭탄 해체를 잘못한 것과 같다. 파란 선(수강 정보)만 잘라야 하는데, 빨간 선(학생 정보)이 한 묶음으로 꼬여 있어서 같이 잘라버려 폭탄이 터지는 원리다.

---

## Ⅲ. 비교 및 연결
[[002_database_definition|데이터베이스]]의 [[093_update_anomaly|갱신 이상]]([[530_anomaly|Anomaly]])에는 삭제 이상 외에도 [[091_functional_dependency_fd|삽입 이상]], [[093_update_anomaly|갱신 이상]]이 있다. 이들은 모두 **'하나의 [[061_relation_schema_instance|릴레이션]]에 여러 테마가 섞여 있어서'** 발생하는 형제 문제들이다.

| 이상([[530_anomaly|Anomaly]]) 유형 | 핵심 문제 | 실무 발생 상황 |
| :--- | :--- | :--- |
| **삭제 이상 (Deletion)** | 원치 않는 연쇄 정보 소멸 | 수강 취소 시 학생 신상 정보 증발 |
| **[[091_functional_dependency_fd|삽입 이상]] (Insertion)** | 불필요한 [[459_dummy_test_double|더미]] [[001_dikw_pyramid|데이터]] 강제 요구 | 미수강 신입생 등록 시 가짜 과목코드 필요 |
| **[[093_update_anomaly|갱신 이상]] (Update)** | 중복 [[001_dikw_pyramid|데이터]]의 부분 수정으로 불일치 | 학과명 변경 시 일부 행만 수정되어 모순 발생 |

삭제 이상은 [[091_functional_dependency_fd|삽입 이상]]과 동전의 양면이다. 합쳐진 [[001_dikw_pyramid|데이터]]를 억지로 넣으려다 실패하는 것이 [[091_functional_dependency_fd|삽입 이상]]이라면, 억지로 빼내려다 다른 것까지 부수는 것이 삭제 이상이다. 결국 이들의 공통 해결책은 [[093_normalization|정규화]]를 통한 '[[101_lossless_join_decomposition|무손실 분해]]'다.

- **📢 섹션 요약 비유**: [[091_functional_dependency_fd|삽입 이상]]은 옷장에 옷과 신발을 같이 묶어서만 넣을 수 있는 규정이고, 삭제 이상은 낡은 신발을 버릴 때 멀쩡한 옷까지 무조건 같이 버려야 하는 억지 규정이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무 설계 시나리오에서 [[282_performance_tactics|성능]] 향상을 위해 의도적으로 '반정규화(De-[[093_normalization|normalization]])'를 수행할 때, 삭제 이상은 가장 꼼꼼하게 따져봐야 할 위험 요소다. 조회 [[282_performance_tactics|성능]]을 높이려고 테이블을 합쳐두면, 훗날 [[001_dikw_pyramid|데이터]]를 삭제할 때 반드시 이 문제에 부딪히게 된다.

### [[435_checklist_based_testing|체크리스트]] (설계 [[395_verification_process_review|검증]])
1. 특정 [[001_dikw_pyramid|데이터]]를 지웠을 때, 테이블에서 영구적으로 사라져서는 안 되는 부모 격의 마스터 [[001_dikw_pyramid|데이터]]가 포함되어 있는가?
2. 기본키(PK)가 복합키([[261_composite_pattern_tree_structure|Composite]] [[067_db_key_uniqueness_minimality|Key]])인 경우, [[082_attribute_types_er_model|속성]] 중 일부가 기본키의 일부에만 종속(부분 함수 종속)되어 있지 않은가?
3. 반정규화를 적용한 테이블에 `DELETE` 트랜잭션이 얼마나 자주 발생하는가? (자주 발생한다면 반정규화 철회 고려)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 삭제 이상을 피하려고 [[001_dikw_pyramid|데이터]] 삭제 대신 `IS_DELETED = 'Y'` 같은 [[186_character_stuffing_dle_stx_etx|플래그]]([[186_character_stuffing_dle_stx_etx|Flag]])만 업데이트하는 꼼수를 남발하는 설계. (이는 근본적 구조 [[352_defect_definition|결함]]을 회피할 뿐 [[002_database_definition|데이터베이스]] 비대화를 초래한다.)

- **📢 섹션 요약 비유**: 실무의 테이블 설계는 레고 조립과 같다. 나중에 분리해야 할 부품은 본드(반정규화)로 붙이지 말고, 홈(외래키)으로 끼워둬야 나중에 부수지 않고 뺄 수 있다.

---

## Ⅴ. 기대효과 및 결론
삭제 이상을 인지하고 테이블을 [[101_lossless_join_decomposition|무손실 분해]](예: 학생 테이블과 수강 테이블로 분리)하면, [[001_dikw_pyramid|데이터]] 정합성이 완벽하게 보장된다. 특정 과목의 수강 기록을 지우더라도 학생의 신상 [[001_dikw_pyramid|데이터]]는 독립된 테이블에 안전하게 남아있게 된다.

그러나 과도한 [[093_normalization|정규화]]는 조인([[521_join|Join]]) 연산을 증가시켜 시스템 [[282_performance_tactics|성능]] 저하를 부를 수 있으므로, 삭제 연산의 빈도와 조회 연산의 빈도를 균형 있게 평가해야 한다. 결론적으로 삭제 이상은 "[[001_dikw_pyramid|데이터]] 구조의 [[352_defect_definition|결함]]이 어떻게 비즈니스 논리를 파괴하는가"를 보여주는 가장 강력한 경고등이다.

- **📢 섹션 요약 비유**: 독립된 수납장을 마련하는 것과 같다. 책장과 옷장을 따로 분리해 두면, 안 읽는 책을 버린다고 내 옷까지 같이 내다 버리는 어처구니없는 실수를 완벽히 예방할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[093_normalization|정규화]] ([[093_normalization|Normalization]])** | 삭제 이상을 포함한 [[093_update_anomaly|갱신 이상]]을 해결하는 [[002_database_definition|데이터베이스]] 설계 기법 |
| **[[091_functional_dependency_fd|삽입 이상]] / [[093_update_anomaly|갱신 이상]]** | 삭제 이상과 함께 발생하는 3대 [[093_update_anomaly|갱신 이상]]([[530_anomaly|Anomaly]]) |
| **함수적 종속 (Functional Dependency)** | [[061_relation_schema_instance|릴레이션]] 내 [[082_attribute_types_er_model|속성]] 간의 종속 관계로, 삭제 이상의 근본 원인 파악 도구 |
| **[[101_lossless_join_decomposition|무손실 분해]] (Lossless Decomposition)** | 정보 손실(삭제 이상) 없이 [[061_relation_schema_instance|릴레이션]]을 쪼개는 [[093_normalization|정규화]] 원칙 |

### 📈 관련 키워드 및 발전 흐름도
```text
비정규화 릴레이션 (하나의 거대한 테이블)
    │
    ▼
갱신 이상 발생 (삽입 / 갱신 / 삭제 이상)
    │
    ▼
함수적 종속성 (FD) 분석
    │
    ▼
정규화 및 무손실 분해 (1NF, 2NF, 3NF...)
    │
    ▼
독립된 엔티티 보장 및 데이터 무결성 확보
```

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감 상자에 '레고'와 '점토'를 본드로 딱 붙여서 보관한다고 상상해 보세요.
2. 어느 날 점토가 굳어서 쓰레기통에 버리려는데, 레고까지 본드로 붙어 있어서 소중한 레고도 같이 버려야만 해요.
3. [[002_database_definition|데이터베이스]]에서도 성격이 다른 정보를 한곳에 억지로 붙여두면, 하나를 지울 때 소중한 다른 정보까지 사라지는데 이걸 '삭제 이상'이라고 부른답니다.
