---
title: 91. 삽입 이상 (Insertion Anomaly) - 불필요한 데이터까지 함께 삽입해야 하는 현상
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[094_functional_dependency_fd|함수적 종속성]] (Functional Dependency, FD)은 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]에서 어떤 [[082_attribute_types_er_model|속성]](X)의 값이 다른 [[082_attribute_types_er_model|속성]](Y)의 값을 유일하게 결정하는 제약 조건이다.
> 2. **가치**: [[002_database_definition|데이터베이스]] [[093_normalization|정규화]] ([[093_normalization|Normalization]])를 수행할 때, 테이블을 분해하는 기준이 되어 [[001_dikw_pyramid|데이터]] 중복과 [[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]])을 예방하는 척도가 된다.
> 3. **판단 포인트**: 부분 함수 종속과 이행적 함수 종속을 식별하여 제거하는 것이 [[104_second_normal_form_2nf_full_fd|제2정규형]]([[104_second_normal_form_2nf_full_fd|2NF]]) 및 [[105_third_normal_form_3nf_transitive|제3정규형]]([[105_third_normal_form_3nf_transitive|3NF]]) 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[094_functional_dependency_fd|함수적 종속성]] (Functional Dependency)은 [[061_relation_schema_instance|릴레이션]] 내에서 [[082_attribute_types_er_model|속성]]들 간의 의미적 연관성을 나타내는 수학적 개념이다. 특정 [[082_attribute_types_er_model|속성]] 집합 X의 값을 알면, 다른 [[082_attribute_types_er_model|속성]] 집합 Y의 값이 반드시 하나로 결정될 때, "Y는 X에 함수적으로 종속된다"고 하며 $X \rightarrow Y$로 표기한다. 이때 X를 [[095_determinant_dependent|결정자]] ([[095_determinant_dependent|Determinant]]), Y를 종속자 (Dependent)라고 부른다.

[[002_database_definition|데이터베이스]] 설계 시, [[061_relation_schema_instance|릴레이션]] 내에 여러 [[082_attribute_types_er_model|속성]]을 무분별하게 모아두면 정보의 중복이 발생하고 갱신 시 모순이 생기는 [[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]])이 일어난다. 이를 방지하기 위해서는 어떤 [[082_attribute_types_er_model|속성]]이 다른 [[082_attribute_types_er_model|속성]]을 의미적으로 규정하는지 정확히 파악하여, [[008_dependencies|종속성]] 규칙에 따라 테이블을 분리해야 한다. [[094_functional_dependency_fd|함수적 종속성]]은 이러한 분리의 수학적 근거를 제공한다.

- **📢 섹션 요약 비유**: [[094_functional_dependency_fd|함수적 종속성]]은 학교의 학번과 학생 이름의 [[083_relationship_in_er_model|관계]]와 같다. 학번을 알면 그 학생이 누구인지 한 명으로 특정되듯, 한 [[001_dikw_pyramid|데이터]]가 다른 [[001_dikw_pyramid|데이터]]를 유일하게 가리키는 나침반 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[094_functional_dependency_fd|함수적 종속성]]은 크게 세 가지 형태로 나뉘며, 각 형태는 [[093_normalization|정규화]]의 특정 단계와 직결된다. 가장 이상적인 상태는 [[061_relation_schema_instance|릴레이션]]의 모든 일반 [[082_attribute_types_er_model|속성]]이 기본키(PK) 전체에만 종속되는 완전 함수 종속이다.

| [[008_dependencies|종속성]] 유형 | 설명 | 수식 예시 | [[093_normalization|정규화]] [[083_relationship_in_er_model|관계]] |
| :--- | :--- | :--- | :--- |
| **완전 함수 종속 (Full FD)** | 종속자 Y가 기본키 X 전체에 대해서만 종속되고, X의 일부분에는 종속되지 않는 상태. | `{학번, 과목} → 성적` | 정상 (이상적 상태) |
| **부분 함수 종속 (Partial FD)** | 종속자 Y가 기본키 X의 전체가 아닌 일부에만 종속되는 상태. | `{학번, 과목} → 학생이름`<br>(학생이름은 학번에만 종속됨) | [[104_second_normal_form_2nf_full_fd|제2정규형]]([[104_second_normal_form_2nf_full_fd|2NF]])의 제거 대상 |
| **이행적 함수 종속 (Transitive FD)** | $X \rightarrow Y$ 이고 $Y \rightarrow Z$ 일 때, $X \rightarrow Z$가 성립하는 연쇄적 종속 상태. | `학번 → 학과`, `학과 → 학과장`<br>(학번 → 학과장) | [[105_third_normal_form_3nf_transitive|제3정규형]]([[105_third_normal_form_3nf_transitive|3NF]])의 제거 대상 |

```text
┌──────────────────────────────────────────────────────────────┐
│                  함수적 종속성의 3가지 구조                  │
├──────────────────────────────────────────────────────────────┤
│ [1] 완전 함수 종속         [2] 부분 함수 종속         [3] 이행적 함수 종속         │
│   ┌──────┴──────┐          ┌──────┴──────┐          ┌─────────────┐        │
│   │             │          │             │          │             │        │
│   X1            X2         X1            X2         X             │        │
│   └──────┬──────┘          │             │          │             │        │
│          │                 │             │          ▼             │        │
│          ▼                 ▼             │          Y ────────────┘        │
│          Y                 Y (X1에만 종속)│          │                      │
│                            └─────────────┘          ▼                      │
│                                                     Z                      │
└──────────────────────────────────────────────────────────────┘
```

다이어그램에서 보듯, 부분 함수 종속과 이행적 함수 종속은 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 훼손하는 우회 경로를 만든다. 이 우회 경로를 끊고 독립된 테이블로 분리하는 과정이 [[093_normalization|정규화]]다.

- **📢 섹션 요약 비유**: 완전 종속은 부대원 모두가 중대장 한 명의 명령을 직접 듣는 정상적인 지휘 체계다. 반면 부분 종속은 부대원이 다른 소대장의 명령도 듣는 것이고, 이행적 종속은 중대장 명령을 소대장을 거쳐 건너 듣는 것이다. 이중 지휘를 막으려면 소대를 분리해야 한다.

---

## Ⅲ. 비교 및 연결

[[094_functional_dependency_fd|함수적 종속성]]은 단순히 의존성을 넘어 다중값 종속 (Multivalued Dependency)이나 조인 종속 ([[521_join|Join]] Dependency)으로 개념이 확장된다. [[094_functional_dependency_fd|함수적 종속성]]이 주로 1:1 결정 [[083_relationship_in_er_model|관계]]를 다룬다면, 다중값 종속은 1:N 결정 [[083_relationship_in_er_model|관계]]를 다룬다.

| 기준 | [[094_functional_dependency_fd|함수적 종속성]] (FD) | 다중값 [[008_dependencies|종속성]] ([[400_mvd_4nf|MVD]]) |
| :--- | :--- | :--- |
| **결정 값의 수** | X값 1개에 Y값 **1개**가 결정됨 | X값 1개에 Y값 **여러 개**가 독립적으로 결정됨 |
| **제거 대상 정규형** | 제1~3정규형, [[529_bcnf|BCNF]] | [[108_fourth_normal_form_4nf|제4정규형]] ([[108_fourth_normal_form_4nf|4NF]]) |
| **표기법** | $X \rightarrow Y$ | $X \twoheadrightarrow Y$ |

[[094_functional_dependency_fd|함수적 종속성]]을 완벽히 해소하여 모든 [[095_determinant_dependent|결정자]]가 후보키가 되도록 만든 상태가 [[529_bcnf|BCNF]] ([[106_bcnf_boyce_codd_normal_form|Boyce-Codd Normal Form]])이다. 즉, [[094_functional_dependency_fd|함수적 종속성]]은 RDBMS (Relational [[501_database|Database]] [[372_management|Management]] System)에서 테이블이 원자성을 유지하고 모순 없이 작동하기 위한 가장 기본적이고 강력한 설계 [[395_verification_process_review|검증]] 도구다.

- **📢 섹션 요약 비유**: [[094_functional_dependency_fd|함수적 종속성]]이 '주민번호를 주면 사람 한 명이 나온다'는 1:1 자판기라면, 다중값 [[008_dependencies|종속성]]은 '과목 번호를 주면 수강생 명단 전체가 나온다'는 1:N 복권 추첨기와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실제 DB 설계에서는 모든 [[094_functional_dependency_fd|함수적 종속성]]을 완벽하게 분리하는 것만이 정답은 아니다. [[008_dependencies|종속성]] 제거([[093_normalization|정규화]])는 [[001_dikw_pyramid|데이터]] 정합성을 높이지만, 반대로 [[001_dikw_pyramid|데이터]]를 조회할 때 무수한 조인([[521_join|Join]]) 연산을 유발하여 [[282_performance_tactics|성능]] 저하를 가져올 수 있다.

### [[435_checklist_based_testing|체크리스트]]

1. 복합 기본키를 사용하는 테이블에 부분 함수 종속이 남아있어 수정 이상(Modification [[530_anomaly|Anomaly]])이 발생하지 않는가?
2. 특정 [[082_attribute_types_er_model|속성]] 값이 변경될 때 여러 행을 동시에 업데이트해야 하는 이행적 종속이 숨어있지 않는가?
3. 모든 [[095_determinant_dependent|결정자]]가 후보키인가? ([[529_bcnf|BCNF]] 위배 [[396_validation|확인]])

### 실무 판단 포인트 (반정규화와의 트레이드오프)

- **[[093_normalization|정규화]] 채택**: 핵심 [[539_mdm_master_data_management|마스터 데이터]](회원 정보, 상품 정보 등)는 완전 함수 종속을 엄격히 지켜 일관성을 보호해야 한다.
- **의도적 위반 (반정규화)**: [[282_performance_tactics|성능]]이 극도로 중요한 통계 테이블이나, 읽기 전용의 대규모 이력 [[001_dikw_pyramid|데이터]]의 경우, 이행적 종속을 알면서도 조인 비용을 줄이기 위해 한 테이블에 합쳐놓는 반정규화(De-[[093_normalization|normalization]])를 [[268_strategy_pattern|전략]]적으로 선택할 수 있다.

- **📢 섹션 요약 비유**: [[008_dependencies|종속성]]을 제거해 테이블을 쪼개는 것은 물건을 분류별로 완벽히 서랍에 넣는 것과 같다. 정리는 깔끔하지만 물건을 꺼낼 때 서랍을 여러 번 열어야 하는 불편함(조인 비용)이 생긴다. 때로는 자주 쓰는 물건을 한 바구니에 담는 타협도 필요하다.

---

## Ⅴ. 기대효과 및 결론

[[094_functional_dependency_fd|함수적 종속성]]을 기반으로 [[093_normalization|정규화]]를 수행하면, 삽입, 갱신, 삭제 시 발생하는 [[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]])을 원천 차단할 수 있다. [[001_dikw_pyramid|데이터]]의 중복이 최소화되어 스토리지 공간이 절약되고, [[001_dikw_pyramid|데이터]] 정합성이 보장되어 시스템의 신뢰도가 크게 상승한다.

결론적으로, [[094_functional_dependency_fd|함수적 종속성]]은 [[001_dikw_pyramid|데이터]]의 본질적 의미와 [[083_relationship_in_er_model|관계]]를 수학적으로 모델링하는 수단이다. "어떤 [[001_dikw_pyramid|데이터]]가 어떤 [[001_dikw_pyramid|데이터]]를 결정하는가"라는 비즈니스 로직의 본질을 파악하고, 이를 테이블 구조로 매핑하는 능력이 바로 [[002_database_definition|데이터베이스]] 설계자의 핵심 역량이다.

- **📢 섹션 요약 비유**: [[094_functional_dependency_fd|함수적 종속성]]은 얽힌 실타래를 푸는 정확한 공식이다. 공식을 모르면 억지로 당겨 끊어지지만, 공식을 알면 아무리 꼬인 [[001_dikw_pyramid|데이터]]라도 깔끔하고 독립된 한 가닥의 실로 깔끔하게 감아낼 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[090_anomaly_insertion_deletion_update|이상 현상]] ([[530_anomaly|Anomaly]])** | [[094_functional_dependency_fd|함수적 종속성]]을 위배한 잘못된 설계로 인해 발생하는 [[001_dikw_pyramid|데이터]] 갱신 오류 현상 |
| **기본키 (Primary [[067_db_key_uniqueness_minimality|Key]])** | [[061_relation_schema_instance|릴레이션]] 내에서 가장 강력한 [[095_determinant_dependent|결정자]] ([[095_determinant_dependent|Determinant]]) 역할을 하는 [[082_attribute_types_er_model|속성]] |
| **[[093_normalization|정규화]] ([[093_normalization|Normalization]])** | [[094_functional_dependency_fd|함수적 종속성]]에 따라 테이블을 무손실 분해하는 과정 ([[103_first_normal_form_1nf_atomic_value|1NF]] ~ [[529_bcnf|BCNF]]) |
| **반정규화 (De-[[093_normalization|normalization]])** | 조인 [[282_performance_tactics|성능]] 향상을 위해 의도적으로 [[094_functional_dependency_fd|함수적 종속성]] 원칙을 일부 위배하는 [[268_strategy_pattern|전략]] |

### 📈 관련 키워드 및 발전 흐름도

```text
비정규 릴레이션 (데이터 중복 및 이상 현상)
    │
    ▼
부분 함수 종속 (Partial FD) 식별 및 제거
    │
    ▼
제2정규형 (2NF) 달성
    │
    ▼
이행적 함수 종속 (Transitive FD) 식별 및 제거
    │
    ▼
제3정규형 (3NF) 및 BCNF 달성 (모든 결정자가 후보키)
```

이 흐름도는 [[001_dikw_pyramid|데이터]] 덩어리 속에서 나쁜 [[008_dependencies|종속성]]을 차례대로 솎아내어 [[003_integrity|무결성]] 높은 구조로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[094_functional_dependency_fd|함수적 종속성]]은 "왕과 신하" 규칙이에요. 왕([[095_determinant_dependent|결정자]])이 명령하면 신하(종속자)는 무조건 그대로 따라야 해요.
2. 만약 한 명의 신하가 두 명의 왕에게 명령을 받거나, 신하가 다른 신하에게 몰래 명령을 내리면 나라([[002_database_definition|데이터베이스]])가 혼란스러워져요.
3. 그래서 이런 복잡한 명령 체계를 발견하면, 왕과 신하를 짝지어 새로운 성(테이블)으로 나눠주는 게 아주 중요하답니다!
