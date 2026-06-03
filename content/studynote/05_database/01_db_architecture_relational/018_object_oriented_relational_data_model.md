---
title: 18. 객체지향 데이터 모델 (OODBMS) / 객체 관계형 데이터 모델 (ORDBMS)
date: '2026-03-04'
description: RDBMS의 한계를 극복하고 복잡한 사용자 정의 데이터 타입과 상속을 지원하는 차세대 데이터 모델
tags:
- database
---

# 18. 객체지향 및 객체 [[017_relational_data_model|관계형 데이터 모델]] (OODBMS / ORDBMS)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[083_relationship_in_er_model|관계]]형 모델의 평면적 구조 한계를 극복하기 위해, [[322_oop_4_characteristics|객체지향 프로그래밍]]의 캡슐화, [[234_uml_class_relationships_generalization_dependency|상속]], 다형성 개념을 [[002_database_definition|데이터베이스]] [[005_schema|스키마]]와 질의어에 직접 통합한 아키텍처이다.
> 2. **가치**: 복잡한 멀티미디어, GIS 공간 [[001_dikw_pyramid|데이터]], 계층형 [[001_dikw_pyramid|데이터]]를 애플리케이션 코드 변환 없이 [[002_database_definition|데이터베이스]] 자체에서 네이티브하게 저장하고 메서드를 통해 조작할 수 있다.
> 3. **융합**: 객체와 [[083_relationship_in_er_model|관계]]형 테이블 사이의 구조적 불일치([[004_impedance|Impedance]] Mismatch)를 해결하며, ORDBMS는 기존 SQL 기반 RDBMS 위에 객체 특성을 융합한 실무적 타협안의 표준으로 자리잡았다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)
전통적인 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]](RDBMS)는 단순한 숫자와 문자 [[001_dikw_pyramid|데이터]]를 다루는 비즈니스 [[191_transaction_concept_states|트랜잭션]] 시스템([[327_hint_handoff|OLTP]])에서 엄청난 성공을 거두었다. 하지만 1990년대 이후 멀티미디어(이미지, 동영상), CAD/GIS(공간 좌표), 의료 [[001_dikw_pyramid|데이터]] 등 구조가 복잡하고 크기가 방대한 비정형/[[003_semi_structured_data|반정형 데이터]] 처리에 대한 수요가 폭발적으로 증가했다. RDBMS는 [[001_dikw_pyramid|데이터]]를 무조건 1차원적인 원자값(Atomic Value)으로만 쪼개어 저장해야 하는 [[103_first_normal_form_1nf_atomic_value|제1정규형]]([[103_first_normal_form_1nf_atomic_value|1NF]])의 제약을 가지고 있어, 이처럼 복잡한 계층형 [[001_dikw_pyramid|데이터]]를 모델링하려면 수많은 테이블을 억지로 쪼개고 무수한 조인([[521_join|Join]])을 유발해야 하는 치명적 한계에 부딪혔다.

또한, [[322_oop_4_characteristics|객체지향 프로그래밍]]([[322_oop_4_characteristics|OOP]]) 언어(Java, C++)가 대세가 되면서 애플리케이션은 [[001_dikw_pyramid|데이터]]를 '객체(Object)' 형태로 다루는데, DB는 '[[061_relation_schema_instance|릴레이션]](Table)' 형태를 고집하면서 심각한 [[004_impedance|임피던스]] 불일치([[004_impedance|Impedance]] Mismatch)가 발생했다. 이를 근본적으로 해결하기 위해 [[002_database_definition|데이터베이스]] 자체가 객체를 직접 저장하고 메서드(Method)를 실행할 수 있도록 설계된 객체지향 [[014_data_model_components|데이터 모델]](OODBMS)이 등장했다. 그러나 OODBMS는 수학적 기반과 질의어 표준의 부재로 인해 시장에서 도태되었고, 결국 기존 RDBMS의 장점(SQL, [[003_integrity|무결성]])을 유지하면서 객체의 개념(사용자 정의 타입, [[234_uml_class_relationships_generalization_dependency|상속]])을 수용한 객체 [[017_relational_data_model|관계형 데이터 모델]](ORDBMS)이 현대 엔터프라이즈의 표준 [[014_data_model_components|데이터 모델]]로 안착하게 되었다.

아래 다이어그램은 객체지향 언어와 RDBMS 간의 [[004_impedance|임피던스]] 불일치 문제를 [[003_bigdata_7v|시각화]]한 것이다.

```text
┌─────── [App: 객체지향 세계] ───────┐
│ class Car {                        │
│   Engine eng; // 중첩 객체         │
│   Wheel[] wh; // 배열/컬렉션       │
│   void start() { ... } // 행위     │
│ }                                  │
└───────────────┬────────────────────┘
                │ 💥 Impedance Mismatch (구조적 충돌)
                │ (ORM 계층이 변환/분해 매핑 수행)
┌───────────────▼────────────────────┐
│ [DB: 관계형 세계 (1NF 제약)]       │
│ TABLE Car (id, name, eng_id)       │
│ TABLE Engine (eng_id, power)       │
│ TABLE Wheel (id, car_id, size)     │ ← 배열 불가, 행 단위 분할 필수
└────────────────────────────────────┘
```

이 그림의 핵심은 애플리케이션 계층과 스토리지 계층 간의 [[001_dikw_pyramid|데이터]] 패러다임이 완전히 어긋나 있다는 점이다. 객체지향 모델은 [[001_dikw_pyramid|데이터]]([[082_attribute_types_er_model|속성]])와 행위(메서드)를 하나로 캡슐화하고, 리스트나 중첩 객체 등 풍부한 자료구조를 허용한다. 반면 [[083_relationship_in_er_model|관계]]형 모델은 행위의 개념이 없고, 모든 [[001_dikw_pyramid|데이터]]를 단순 스칼라 값으로 평탄화(Flattening)해야 한다. 이러한 불일치로 인해 개발자는 비즈니스 로직보다 객체를 테이블 구조로 분해(Insert)하고 조립([[520_select|Select]])하는 매핑 코드(Boilerplate) 작성에 막대한 시간을 낭비하게 된다. 실무에서는 이를 완화하기 위해 Hibernate/JPA와 같은 ORM 프레임워크를 도입하지만, 결국 ORM의 [[198_abstraction_control_data_process|추상화]] 누수(N+1 [[298_qkv_attention|쿼리]] 문제 등)로 인한 심각한 [[282_performance_tactics|성능]] [[015_지연_데이터_관점|지연]]을 겪는 원인이 된다. 

📢 **섹션 요약 비유**: 마치 입체적인 레고 완성품(객체)을 보관함(RDB)에 넣을 때마다 전부 분해해서 부품별로 따로 보관해야 하고, 꺼낼 때마다 다시 조립해야 하는 번거로운 상황과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
객체 [[014_data_model_components|데이터 모델]]은 [[002_database_definition|데이터베이스]] 내부에 OID(Object [[088_identifier_in_er_model|Identifier]]), 캡슐화(Encapsulation), [[234_uml_class_relationships_generalization_dependency|상속]](Inheritance), 다형성(Polymorphism)이라는 OOP의 핵심 기둥을 그대로 내재화한다. 

| 구성 요소 | 역할 | 내부 동작/특성 | RDBMS와의 차이 | 비유 |
|:---|:---|:---|:---|:---|
| **OID (객체 [[289_identification_flags_fragmentation_offset|식별자]])** | 객체의 절대적 고유성 보장 | [[001_dikw_pyramid|데이터]] 값 변경과 무관하게 시스템이 자동 할당 | PK(기본키)는 [[001_dikw_pyramid|데이터]] 값에 의존함 | 사람의 지문(변하지 않음) |
| **UDT (사용자 정의 타입)** | 복잡한 [[001_dikw_pyramid|데이터]] 구조 정의 | 단순 스칼라뿐 아니라 Record, [[055_array|Array]] 형태 지원 | 내장 [[001_dikw_pyramid|데이터]] 타입만 허용 | 맞춤형 공구 세트 |
| **메서드 (Method)** | [[001_dikw_pyramid|데이터]]와 결합된 동작 절차 | [[005_schema|스키마]] 내에 절차적 로직을 C, Java 등으로 저장 | Stored Procedure보다 강한 결합 | 스마트폰의 버튼 기능 |
| **[[234_uml_class_relationships_generalization_dependency|상속]] (Inheritance)** | 객체 구조의 재사용 및 확장 | 슈퍼타입의 [[082_attribute_types_er_model|속성]]과 메서드를 서브타입이 물려받음 | 테이블 조인이나 슈퍼/서브 패턴 필요 | 부모의 유전자 물려받기 |
| **집합 (Collection)** | 다치 [[082_attribute_types_er_model|속성]] 지원 | 하나의 [[082_attribute_types_er_model|속성]]이 List, Set, Bag, Array를 가짐 | [[103_first_normal_form_1nf_atomic_value|1NF]]([[193_atomicity_all_or_nothing|원자성]]) 위배로 불허 | 한 칸에 여러 물건 담기 |

ORDBMS는 RDBMS의 엔진 코어 위에 이 UDT와 컬렉션 엔진을 래핑(Wrapping)하는 방식으로 구현된다. 즉, 내부 스토리지는 [[286_page_frame|페이지]]와 블록 기반으로 동작하되, 파서(Parser)와 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[088_optimizer|Optimizer]])가 객체 [[316_reference_pattern_nosql|참조]](Ref)와 [[055_array|배열]]([[055_array|Array]]) 처리를 이해할 수 있도록 확장된 것이다.

다음 다이어그램은 ORDBMS 환경에서 테이블이 어떻게 계층적 [[234_uml_class_relationships_generalization_dependency|상속]] 구조와 중첩 객체를 저장하는지를 보여주는 [[001_dikw_pyramid|데이터]] 레이아웃이다.

```text
[ORDBMS 논리적 구조: Type 상속과 컬렉션]

(Super Type) 
┌─ Person_Type ─────────────────────────┐
│ OID | Name(String) | Address(Object)  │  ← Address 자체도 또 다른 객체
└─▲─────────────────────────────────────┘
  │ (Inheritance / IS-A)
  │
(Sub Type) 
┌─ Employee_Type ────────────────────────────────────────┐
│ OID | Person_Type_속성_상속 | Salary | Skills(Array)   │ ← 다치 속성(Array) 지원
├────────────────────────────────────────────────────────┤
│ id1 | "Alice" | {City: "Seoul"} | 5000 | ["C", "SQL"]  │
└────────────────────────────────────────────────────────┘
```

이 도식의 핵심은 [[017_relational_data_model|관계형 데이터 모델]]의 철칙이었던 '[[082_attribute_types_er_model|속성]]의 [[193_atomicity_all_or_nothing|원자성]]([[103_first_normal_form_1nf_atomic_value|1NF]])'을 의도적으로 파괴하고, '다치 [[082_attribute_types_er_model|속성]](Skills [[055_array|Array]])'과 '중첩 객체(Address Object)'를 단일 [[063_relation_tuple_cardinality|튜플]] 내에 수용했다는 점이다. 이로 인해 [[063_relation_tuple_cardinality|튜플]]의 물리적 크기가 가변적으로 변하며 저장 엔진의 블록 분할(Block Splitting) 오버헤드가 증가할 수 있다. 하지만 [[369_logic_bomb|논리]]적 관점에서는 '사원'을 조회하기 위해 '주소' 테이블과 '스킬' 테이블을 따로 조인할 필요가 없으므로, 관련된 [[001_dikw_pyramid|데이터]]가 물리적으로 클러스터링되어 디스크 I/O가 획기적으로 줄어드는 [[282_performance_tactics|성능]]적 이점을 제공한다. 실무에서는 PostgreSQL과 같은 현대적 RDBMS가 이러한 JSONB [[001_dikw_pyramid|데이터]] 타입과 [[055_array|배열]] 컬럼을 지원하는 것이 대표적인 ORDBMS적 특징의 발현이며, 이를 통해 NoSQL의 유연성과 RDB의 [[003_integrity|무결성]]을 동시에 달성한다.

📢 **섹션 요약 비유**: 과거에는 가방, 렌즈, 삼각대를 따로 들고 다녀야(조인) 했다면, 이제는 모든 기능이 하나로 합쳐진 만능 스마트폰(중첩 객체) 하나만 주머니에 넣고 다니는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[[014_data_model_components|데이터 모델]] 패러다임은 순수 RDBMS에서 OODBMS로의 급진적 전환을 시도했다가 실패하고, 결국 중도적 타협안인 ORDBMS로 안착했다.

| 분석 항목 | RDBMS | OODBMS | ORDBMS | 판단 포인트 |
|:---|:---|:---|:---|:---|
| **이론적 기반** | 수학적 집합론, [[038_relational_algebra|관계 대수]] | [[322_oop_4_characteristics|객체지향 프로그래밍]] (수학적 모델 부재) | [[038_relational_algebra|관계 대수]] + 객체지향 확장 | [[298_qkv_attention|쿼리]] 최적화의 가능성 |
| **[[001_dikw_pyramid|데이터]] 언어** | SQL (선언적, 강력한 최적화) | OQL, 포인터 네비게이션 (절차적 성격) | SQL3 / SQL:1999 (SQL 기반 객체 확장) | 기존 인력과 생태계 [[344_compatibility_usability|호환성]] |
| **복잡 [[001_dikw_pyramid|데이터]] 처리** | 조인 오버헤드 큼 | 포인터 기반으로 복잡한 구조 [[148_5g_embb_urllc_mmtc|초고속]] 처리 | 복잡 구조 지원, 조인 최소화 | 멀티미디어/공간 [[001_dikw_pyramid|데이터]] 적합성 |
| **[[003_integrity|무결성]] 및 보안** | 최고 수준 (ACID 완벽) | 상대적으로 약함 (애플리케이션 의존) | 최고 수준 (RDB 엔진 그대로 사용) | 금융 등 엔터프라이즈 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] |

순수 OODBMS는 객체 간의 [[083_relationship_in_er_model|관계]]를 물리적인 메모리 포인터 형태로 디스크에 저장했기에, 한 객체에서 다른 객체로 탐색하는 속도는 극단적으로 빨랐다. 그러나 선언적 질의(SQL)와 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 없어 복잡한 집계 분석이 불가능했고, 시스템 간 [[344_compatibility_usability|호환성]]이 결여되어 몰락했다.

다음은 시스템 선택 시 고려해야 할 [[001_dikw_pyramid|데이터]] 복잡도와 [[191_transaction_concept_states|트랜잭션]] 빈도에 따른 아키텍처 포지셔닝 맵이다.

```text
복잡도/계층성 (High)
  ▲
  │                 [ OODBMS ] (CAD, 원격탐사)
  │
  │                           [ ORDBMS ] (PostgreSQL, Oracle)
  │                           멀티미디어, GIS, 복합 트랜잭션
  │
  │       [ NoSQL / Document ] 
  │       (빠른 쓰기, 스키마리스)
  │
  │ [ RDBMS ] (금융, 회계)
  └─────────────────────────────────────────▶ 데이터 무결성/정합성 요구 (High)
```

이 매트릭스의 핵심은 ORDBMS가 가장 넓은 커버리지를 가진 범용 솔루션의 위치를 차지하고 있다는 점이다. 순수 RDBMS는 [[001_dikw_pyramid|데이터]] 정합성은 높지만 구조가 복잡해지면 [[282_performance_tactics|성능]]이 무너진다. OODBMS는 복잡한 구조를 다루지만 엔터프라이즈가 요구하는 정합성과 분석 질의 능력을 상실했다. ORDBMS는 RDB의 강력한 [[191_transaction_concept_states|트랜잭션]] 엔진(ACID)과 SQL 최적화기를 기반으로 객체 타입을 얹었기 때문에, 두 마리 토끼를 잡을 수 있었다. 따라서 실무에서 공간 정보(PostGIS)나 복잡한 [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]] 분석이 필요할 때 새로운 이기종 DB를 구축하는 대신, Oracle이나 PostgreSQL의 확장 [[192_module_independence|모듈]]을 활용하는 것이 인프라 복잡도를 낮추는 결정적 요인이 된다.

📢 **섹션 요약 비유**: 순수 전기차(OODBMS)로 바로 넘어가기에는 충전 인프라(SQL 표준)가 부족해서, 기존 내연기관의 장점과 배터리를 섞은 하이브리드 자동차(ORDBMS)가 현실적인 대세가 된 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
실무 환경에서 객체 [[083_relationship_in_er_model|관계]]형 기능을 남용하면 [[002_database_definition|데이터베이스]] [[005_schema|스키마]]가 스파게티처럼 엉키고 [[555_backup_and_restore_strategy|백업]]/[[658_ir_recovery|복구]]가 극도로 복잡해지는 [[128_water_scrum_fall_anti_pattern|안티패턴]]이 발생할 수 있다.

1. **실무 시나리오: [[288_data_warehouse_definition|공간 데이터베이스]](Spatial DB) 구축**
   - **상황**: 배달 앱에서 라이더의 실시간 위치와 식당 간의 거리를 반경 탐색([[541_radius_remote_authentication_aaa|Radius]] Search)해야 함. 순수 RDBMS의 위도/경도 숫자 컬럼으로는 지구의 곡률을 반영한 삼각함수 조인 계산 시 극심한 CPU 과부하 발생.
   - **판단**: ORDBMS 특성을 활용하여 PostgreSQL에 PostGIS 확장을 적용. `GEOMETRY`라는 사용자 정의 타입(UDT)과 [[289_dw_4characteristics|R-Tree]] 공간 [[154_database_index_b_tree_search_optimization|인덱스]]를 활용하여, 복잡한 기하학적 다형성 연산(`ST_Distance`)을 DB 엔진 레벨에서 C언어 속도로 고속 처리.
2. **도입 [[435_checklist_based_testing|체크리스트]]: [[343_json|JSON]] / [[055_array|배열]] 타입 활용의 경계**
   - 객체 [[083_relationship_in_er_model|관계]]형 기능으로 테이블 안에 [[343_json|JSON]] [[055_array|배열]]을 통째로 넣으면 1:N 조인을 피할 수 있어 읽기 [[282_performance_tactics|성능]]이 올라간다.
   - **단점/[[096_risk_non_risk_architecture_evaluation_flaws|리스크]]**: [[055_array|배열]] 내 특정 원소만 수정하는 부분 업데이트(Partial Update)가 비효율적이며, [[001_dikw_pyramid|데이터]] 양이 커질 경우 TOAST(초대형 [[082_attribute_types_er_model|속성]] 저장) 영역으로 [[001_dikw_pyramid|데이터]]가 빠지면서 오히려 I/O 증폭을 유발할 수 있다.
   - **판단 기준**: 해당 [[001_dikw_pyramid|데이터]]가 **'조회' 시 항상 전체 세트로 소비되는가?** (예: 사용자의 프로필 [[009_config|설정]]값) 그렇다면 ORDBMS 컬렉션/JSON을 쓰고, 개별 조작이 빈번하다면 [[093_normalization|정규화]] 테이블로 분리하라.

아래 [[124_decision_tree|의사결정 트리]]는 애플리케이션의 복잡한 객체 [[001_dikw_pyramid|데이터]]를 DB에 어떻게 매핑할지 결정하는 실무 플로우다.

```text
[객체/계층형 데이터 저장 요구]
   ↓
(Q1. 데이터가 독립적인 쿼리나 업데이트의 대상인가?) ── 예 ──> [정규화된 RDB 테이블 생성 (ORM 활용)]
   ↓ 아니오 (항상 전체 문서로만 다뤄짐)
(Q2. 강력한 ACID 트랜잭션 보장이 필요한가?) 
   ├─ 아니오 ──> [MongoDB 등 Document NoSQL 도입]
   └─ 예 ─────> [PostgreSQL/Oracle JSONB, Array 컬럼 적용 (ORDBMS 기능)]
```

이 [[124_decision_tree|의사결정 트리]]의 핵심은 객체 단위 기능(컬렉션, [[234_uml_class_relationships_generalization_dependency|상속]] 등)의 사용 여부를 '[[191_transaction_concept_states|트랜잭션]] 격리'와 '[[001_dikw_pyramid|데이터]] 조작 단위'를 기준으로 판별하는 것이다. 만약 객체 내부의 [[055_array|배열]] 원소 하나가 독립적인 [[191_transaction_concept_states|트랜잭션]] 락([[510_lock|Lock]])의 대상이 되어야 한다면, ORDBMS의 [[055_array|배열]] 타입에 집어넣는 것은 [[063_relation_tuple_cardinality|튜플]] 전체에 락을 걸게 되어 심각한 [[014_concurrency|동시성]] 저하([[266_other_transparency|Concurrency]] 병목)를 유발한다. 이 경우는 전통적인 RDBMS 자식 테이블로 쪼개어 행 단위(Row-level) 락을 [[136_variance|분산]]시켜야 한다. 반면, 단순히 이력 보관용 복합 페이로드를 저장한다면 ORDBMS의 확장 타입을 쓰는 것이 조인 비용을 완벽히 제거하는 최선의 설계다.

📢 **섹션 요약 비유**: 맥가이버 칼(ORDBMS)이 톱, 가위, 드라이버를 다 가졌다고 해서 통나무를 자를 때 쓰면 안 됩니다. 용도에 맞게 가벼운 작업에만 다기능을 쓰고, 큰 작업에는 전용 도구([[093_normalization|정규화]] 테이블)를 꺼내야 하는 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
객체 [[017_relational_data_model|관계형 데이터 모델]](ORDBMS)의 등장은 [[002_database_definition|데이터베이스]]가 단순한 '수동적인 [[001_dikw_pyramid|데이터]] 저장고'에서 '능동적인 비즈니스 로직 처리 엔진'으로 진화했음을 의미한다. 

| 기대효과 구분 | 세부 내용 및 지표 |
|:---|:---|
| **생산성 향상** | ORM 매핑 복잡성 완화, 객체-테이블 매핑 코드(Boilerplate) 30% 이상 감소 |
| **[[064_relation_domain|도메인]] 확장** | 비정형 특수 [[001_dikw_pyramid|데이터]](GIS, XML, 시계열, 유전체)를 네이티브 수준의 [[154_database_index_b_tree_search_optimization|인덱스]]로 처리 |
| **[[282_performance_tactics|성능]] 튜닝** | 다치 [[082_attribute_types_er_model|속성]]([[055_array|Array]]) 활용으로 무거운 다중 테이블 조인 비용(CPU, Memory) 극단적 감소 |

결론적으로, 현대의 상용 RDBMS([[188_pl_sql_t_sql_procedural|Oracle]], SQL Server, PostgreSQL)는 이미 완벽한 ORDBMS의 형태를 띠고 있다. SQL:1999 표준에서 객체지향 개념이 정식 수용된 이후, 순수한 RDBMS와 ORDBMS의 경계는 무의미해졌다. 최근에는 벡터 [[278_instruction_tuning|임베딩]](Vector [[278_instruction_tuning|Embedding]]) [[001_dikw_pyramid|데이터]]나 [[070_graph_datastructure|그래프]] 노드를 사용자 정의 타입으로 수용하여 AI와 [[241_machine_learning_basics|머신러닝]] 워크로드까지 단일 [[002_database_definition|데이터베이스]] 내에서 소화하는 멀티-모델(Multi-model) [[002_database_definition|데이터베이스]] 시대로 그 아키텍처 사상이 계승되고 발전하고 있다.

📢 **섹션 요약 비유**: 진정한 융합 기술은 기존 것을 버리고 완전히 새로 짓는 것이 아니라, 튼튼한 한옥 뼈대(RDB)를 유지한 채 현대적인 스마트 홈 시스템(객체 기능)을 유연하게 이식하는 것과 같습니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
* **[[004_impedance|임피던스]] 불일치 ([[004_impedance|Impedance]] Mismatch)** | [[322_oop_4_characteristics|객체지향 프로그래밍]] 패러다임과 [[017_relational_data_model|관계형 데이터 모델]]의 수학적 구조 차이에서 오는 아키텍처적 충돌 현상
* **ORM (Object-Relational [[010_schema_mapping|Mapping]])** | 객체와 테이블 간의 불일치를 미들웨어 계층에서 자동으로 변환하여 매핑해주는 프레임워크 (JPA, Hibernate)
* **사용자 정의 타입 (UDT)** | ORDBMS에서 사용자가 비즈니스 [[064_relation_domain|도메인]]에 맞춰 기본 [[001_dikw_pyramid|데이터]] 타입을 결합해 새롭게 정의한 복합 [[001_dikw_pyramid|데이터]] 구조
* **PostGIS** | PostgreSQL의 객체 [[083_relationship_in_er_model|관계]]형 기능을 확장하여 공간 정보(도형, 위경도) [[001_dikw_pyramid|데이터]]를 저장하고 기하 연산을 수행하는 플러그인
* **N+1 [[298_qkv_attention|쿼리]] 문제** | 객체의 [[182_lazy_loading|지연 로딩]]([[182_lazy_loading|Lazy Loading]]) 과정에서 부모 객체를 읽은 후 자식 컬렉션을 탐색할 때 불필요한 [[298_qkv_attention|쿼리]]가 N번 추가 실행되는 [[282_performance_tactics|성능]] 병목 현상


### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 모델 (RDBMS) — 테이블·SQL, 복잡한 타입 표현 한계]
    │
    ▼
[객체지향 모델 (OODBMS) — 객체·상속·메서드, 임피던스 불일치 해결]
    │
    ▼
[객체-관계형 모델 (ORDBMS) — RDBMS + 사용자 정의 타입(UDT), SQL 확장]
    │
    ▼
[NoSQL (Document·Graph DB) — 스키마리스, 수평 확장]
    │
    ▼
[NewSQL / 멀티모델 DB — ACID + 수평 확장 통합]
```
OODBMS와 ORDBMS는 [[083_relationship_in_er_model|관계]]형 모델의 타입 표현 한계를 극복하는 두 가지 접근법으로, 현대 다중 모델 DB의 전신이다.
### 👶 어린이를 위한 3줄 비유 설명
1. 옛날 서랍(RDB)은 칸막이가 작아서 장난감 로봇을 꼭 팔, 다리, 머리로 분해해서 넣어야만 했어요. 너무 귀찮았죠!
2. 그래서 아예 커다란 마법의 상자(OODBMS)를 만들었지만, 이건 정리가 하나도 안 돼서 물건을 찾기가 어려웠어요.
3. 지금 쓰는 서랍(ORDBMS)은 칸막이를 내 마음대로 넓힐 수도 있고 조립된 로봇을 통째로 넣을 수 있으면서도 이름표가 잘 붙어 있는 최고의 하이브리드 서랍장이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 18 / 600

← **이전**: [[017_relational_data_model|17. 관계형 데이터 모델 (Relational Model) - 테이블 구조, E.F. Codd 제안]]
**다음**: [[019_dbms_language|19. DBMS 언어]] →

---
