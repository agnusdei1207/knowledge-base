---
title: 96. 완전 함수적 종속 (Full Functional Dependency)
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 완전 함수적 종속 (Full Functional Dependency)은 복합 기본키(PK)를 가진 테이블에서 일반 [[082_attribute_types_er_model|속성]]이 복합키 '전체'에 온전히 의존하는 이상적인 상태다.
> 2. **가치**: 복합키 중 하나라도 누락되면 값을 결정할 수 없게 만들어, 테이블 내 [[001_dikw_pyramid|데이터]]의 논리적 일관성과 응집도를 극대화한다.
> 3. **판단 포인트**: 복합키의 일부 [[082_attribute_types_er_model|속성]]만으로 결정되는 [[097_partial_functional_dependency|부분 함수적 종속]]이 발견된다면, 이는 [[090_anomaly_insertion_deletion_update|이상 현상]]의 원인이 되므로 즉시 테이블을 분리(제2정규화)해야 한다.

---

## Ⅰ. 개요 및 필요성

완전 함수적 종속 (Full Functional Dependency)은 테이블의 [[070_primary_key_alternate_key|기본 키]](PK)가 두 개 이상의 [[082_attribute_types_er_model|속성]]으로 결합된 복합키([[261_composite_pattern_tree_structure|Composite]] [[067_db_key_uniqueness_minimality|Key]])일 때, 종속자(일반 컬럼)가 복합키 전체 집합에 100% 종속되어 있는 관계를 말한다. 즉, $X \rightarrow Y$ 관계에서 $X$의 진부분집합(Proper Subset)으로는 $Y$를 결정할 수 없는 상태다.

관계형 [[002_database_definition|데이터베이스]]에서 여러 [[082_attribute_types_er_model|속성]]이 모여 하나의 [[289_identification_flags_fragmentation_offset|식별자]]를 이룰 때, 각 일반 컬럼은 반드시 그 [[289_identification_flags_fragmentation_offset|식별자]] 전체의 맥락 아래에서만 의미를 가져야 한다. 만약 복합키의 일부에만 의존하는 [[001_dikw_pyramid|데이터]]가 섞여 있다면, 삽입/삭제/갱신 시 원치 않는 정보까지 강제로 조작해야 하는 [[090_anomaly_insertion_deletion_update|이상 현상]]([[530_anomaly|Anomaly]])이 발생한다. 따라서 완전 함수적 종속은 테이블을 안전하고 깨끗하게 유지하기 위한 필수적인 설계 기준이 된다.

- **📢 섹션 요약 비유**: 완전 함수적 종속은 은행의 '공동 명의 금고'와 같다. 남편의 열쇠 1개와 아내의 열쇠 1개가 동시에 꽂혀야만 금고([[001_dikw_pyramid|데이터]])가 열리도록 설계되어, 한 사람만의 권한으로는 절대 접근할 수 없는 완벽한 보안 상태다.

---

## Ⅱ. 아키텍처 및 핵심 원리

완전 함수적 종속을 이해하려면 $X$ ([[095_determinant_dependent|결정자]], 복합키)와 $Y$ (종속자, 일반 [[082_attribute_types_er_model|속성]]) 간의 매핑 구조를 파악해야 한다. 기본키가 `{학번, 과목코드}`인 수강 테이블을 가정해 보자.

| 요소 | 역할 및 메커니즘 |
| :--- | :--- |
| **[[095_determinant_dependent|결정자]] ([[095_determinant_dependent|Determinant]])** | 튜플을 유일하게 식별하는 복합 [[082_attribute_types_er_model|속성]] 집합 (예: `{학번, 과목코드}`) |
| **종속자 (Dependent)** | [[095_determinant_dependent|결정자]]의 값에 의해 유일한 값이 정해지는 일반 [[082_attribute_types_er_model|속성]] (예: `성적`) |
| **완전 종속 조건** | `{학번, 과목코드} \rightarrow 성적` 성립, 단 `{학번} \rightarrow 성적`이나 `{과목코드} \rightarrow 성적`은 불성립 |

```text
┌──────────────────────────────────────────────────────────────┐
│           완전 함수적 종속 vs 부분 함수적 종속 비교          │
├──────────────────────────────────────────────────────────────┤
│ [복합키]                [일반 속성]                          │
│ ┌─────────┐                                                  │
│ │   학번  │──────────┐                                       │
│ └─────────┘          │   완전 함수적 종속                    │
│      +               ├──────────▶ 성적 (O)                 │
│ ┌─────────┐          │   두 조건이 모두 필요함               │
│ │과목코드 │──────────┘                                       │
│ └─────────┘                                                  │
│                                                              │
│ [복합키의 일부]                                              │
│ ┌─────────┐              부분 함수적 종속                    │
│ │   학번  │─────────────────────────▶ 학생이름 (X)         │
│ └─────────┘              (제2정규화로 분리 대상)             │
└──────────────────────────────────────────────────────────────┘
```

이 그림은 완전 함수적 종속이 복합키 전체 집합에 의해 온전히 결정되는 반면, [[097_partial_functional_dependency|부분 함수적 종속]]은 복합키의 일부에 의해 독립적으로 결정되는 치명적인 구조적 결함임을 보여준다.

- **📢 섹션 요약 비유**: 로켓 발사 시스템의 '이중 암호'와 같다. 사령관의 코드와 부사령관의 코드가 합쳐져야만 미사일(성적) 궤도가 결정된다. 사령관 코드만으로 무언가 결정된다면 그것은 설계 오류다.

---

## Ⅲ. 비교 및 연결

완전 함수적 종속은 이와 대립되는 [[097_partial_functional_dependency|부분 함수적 종속]] ([[097_partial_functional_dependency|Partial Functional Dependency]]), 그리고 확장된 개념인 이행적 함수 종속 ([[098_transitive_functional_dependency|Transitive Functional Dependency]])과 비교해야 그 위치가 명확해진다.

| 특성 | 완전 함수적 종속 | [[097_partial_functional_dependency|부분 함수적 종속]] | 이행적 함수 종속 |
| :--- | :--- | :--- | :--- |
| **발생 조건** | 복합키 기반 테이블 | 복합키 기반 테이블 | 단일키/복합키 무관 |
| **의존 대상** | 기본키(PK) 전체 [[082_attribute_types_er_model|속성]] | 기본키(PK)의 일부 [[082_attribute_types_er_model|속성]] | 일반 [[082_attribute_types_er_model|속성]] 간 의존 |
| **[[093_normalization|정규화]] 단계** | [[104_second_normal_form_2nf_full_fd|2NF]] ([[104_second_normal_form_2nf_full_fd|제2정규형]]) 달성 | 분리하여 [[104_second_normal_form_2nf_full_fd|2NF]] 만족 | 분리하여 [[105_third_normal_form_3nf_transitive|3NF]] 만족 |
| **[[090_anomaly_insertion_deletion_update|이상 현상]]** | 발생 안 함 | 갱신, 삽입, [[092_deletion_anomaly|삭제 이상]] 발생 | 갱신, 삽입, [[092_deletion_anomaly|삭제 이상]] 발생 |

이러한 차이 때문에 [[093_normalization|정규화]] 과정은 '[[097_partial_functional_dependency|부분 함수적 종속]] 제거([[103_first_normal_form_1nf_atomic_value|1NF]] $\rightarrow$ [[104_second_normal_form_2nf_full_fd|2NF]])' 이후에 '이행적 함수 종속 제거([[104_second_normal_form_2nf_full_fd|2NF]] $\rightarrow$ [[105_third_normal_form_3nf_transitive|3NF]])' 순서로 단계적으로 쪼개진다. 완전 함수적 종속은 2NF의 완성 기준점이 된다.

- **📢 섹션 요약 비유**: 완전 종속은 '전체 팀'이 협력해야 나오는 결과물이고, 부분 종속은 팀 과제에서 '특정 개인'의 역량만으로 나와버리는 편법이다. 이행적 종속은 '팀장 $\rightarrow$ 대리 $\rightarrow$ 사원'으로 이어지는 불필요한 사내 하청 구조다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 [[002_database_definition|데이터베이스]] 설계에서 복합키를 사용할 때는 [[097_partial_functional_dependency|부분 함수적 종속]]을 반드시 색출해 내야 한다. 특히 이력 관리 테이블이나 주문 상세 테이블을 설계할 때 잦은 실수가 발생한다.

### [[435_checklist_based_testing|체크리스트]]
1. **복합키 [[396_validation|확인]]**: 현재 테이블의 기본키(PK)가 2개 이상의 컬럼으로 구성되어 있는가?
2. **부분 [[008_dependencies|종속성]] [[395_verification_process_review|검증]]**: 일반 컬럼 중 일부 PK 컬럼만으로 결정되는 값이 존재하는가? (예: `주문번호+상품코드`가 PK인데 일반 컬럼으로 `상품명`이 있는 경우)
3. **분리 및 외래키(FK) [[009_config|설정]]**: 발견된 부분 [[008_dependencies|종속성]]을 새로운 마스터 테이블로 떼어내고, 기존 테이블에서 외래키로 참조하게 만들었는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 설계 귀찮음을 이유로 복합키 테이블에 모든 마스터 정보를 다 때려 넣는 '슈퍼 테이블' 설계 ([[001_dikw_pyramid|데이터]] 중복으로 인한 스토리지 낭비 및 [[001_dikw_pyramid|데이터]] 불일치 위험 증가)
- 복합키 대신 인공키(Auto Increment)를 무분별하게 추가하여 본질적인 함수 [[008_dependencies|종속성]]을 감추고 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 훼손

- **📢 섹션 요약 비유**: 자동차 설계에서 엔진(일부 키)에만 의존하는 온도계(부분 종속 [[082_attribute_types_er_model|속성]])를 주행 기록(복합키) 계기판에 억지로 달아두는 것과 같다. 엔진 온도는 별도의 엔진 제어반(새로운 테이블)으로 빼내야 관리가 된다.

---

## Ⅴ. 기대효과 및 결론

테이블 내 모든 [[082_attribute_types_er_model|속성]]을 완전 함수적 종속 상태로 만들면 [[104_second_normal_form_2nf_full_fd|제2정규형]]([[104_second_normal_form_2nf_full_fd|2NF]])을 달성하게 된다. 이는 부분 종속으로 인해 발생하는 중복 [[001_dikw_pyramid|데이터]]를 걷어내고, 부분 갱신 시 발생하는 [[001_dikw_pyramid|데이터]] 불일치를 원천 차단한다. 결과적으로 [[001_dikw_pyramid|데이터]] 삽입과 삭제 시 원치 않는 정보가 엮이는 [[090_anomaly_insertion_deletion_update|이상 현상]]([[530_anomaly|Anomaly]])을 막아 [[003_integrity|무결성]]을 높인다.

결론적으로 완전 함수적 종속은 복합키 설계가 가지는 위험성을 제어하는 '구조적 [[690_firewall_generation_evolution|방화벽]]'이다. [[001_dikw_pyramid|데이터]]의 응집도를 높이고 관리 단위를 명확하게 나누기 위해, [[001_dikw_pyramid|데이터]] 아키텍처를 그리는 엔지니어가 가장 먼저 확보해야 할 필수 기준선으로 기억해야 한다.

- **📢 섹션 요약 비유**: 완전 함수적 종속 달성은 건물의 '하중 [[136_variance|분산]]'과 같다. 건물의 모든 바닥재([[001_dikw_pyramid|데이터]])가 여러 기둥(복합키)에 골고루 완벽하게 지탱되어야 균열([[090_anomaly_insertion_deletion_update|이상 현상]]) 없이 무너지지 않고 버틸 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[103_first_normal_form_1nf_atomic_value|제1정규형]] ([[103_first_normal_form_1nf_atomic_value|1NF]])** | 모든 도메인이 원자값을 갖는 상태, 완전 종속을 논하기 위한 기본 전제 |
| **[[104_second_normal_form_2nf_full_fd|제2정규형]] ([[104_second_normal_form_2nf_full_fd|2NF]])** | [[103_first_normal_form_1nf_atomic_value|제1정규형]]을 만족하고, 모든 [[082_attribute_types_er_model|속성]]이 기본키에 '완전 함수적 종속'된 상태 |
| **[[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]])** | 부분 종속을 제거하지 않았을 때 발생하는 삽입, 삭제, 갱신 오류 |
| **[[095_determinant_dependent|결정자]] ([[095_determinant_dependent|Determinant]])** | 함수 종속 관계에서 종속자의 값을 결정하는 주체, 여기서는 복합 기본키 |

### 📈 관련 키워드 및 발전 흐름도

```text
제1정규형 (1NF) 달성 (원자값)
    │
    ▼
함수 종속성 분석 (부분 함수적 종속 식별)
    │
    ▼
테이블 분해 (제2정규형, 2NF 달성)
    │
    ▼
완전 함수적 종속 (Full Functional Dependency) 확보
    │
    ▼
제3정규형 (3NF) 및 이행적 함수 종속 제거로 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이기구를 타려면 '아빠 손'과 '엄마 손' 두 개를 모두 잡아야만 탈 수 있는 규칙이 있어요.
2. 만약 아빠 손 하나만 잡아도 탈 수 있는 기구가 있다면, 엄마가 없어져도 모르기 때문에 아주 위험한 상태예요.
3. 완전 함수적 종속은 항상 아빠와 엄마 양쪽 모두의 허락을 받아야만 안전하게 결론(값)을 내는 완벽한 규칙이랍니다!
