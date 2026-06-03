+++
weight = 14
title = "14. 데이터 모델 (Data Model) 구성 요소 - 구조(Structure), 연산(Operation), 제약조건(Constraint)"
description = "현실 세계를 데이터베이스로 추상화하기 위한 필수 3요소인 정적 구조, 동적 연산, 무결성 제약조건"
date = "2024-05-18"
[taxonomies]
tags = ["Database", "Data Model", "Structure", "Operation", "Constraint"]
categories = ["studynote", "5_database"]
+++

# 14. [[001_dikw_pyramid|데이터]] 모델 ([[001_dikw_pyramid|Data]] Model) 구성 요소 - 구조, 연산, 제약조건

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 복잡한 현실 세계의 비즈니스 요건을 컴퓨터가 이해할 수 있는 [[002_database_definition|데이터베이스]] [[369_logic_bomb|논리]] 구조로 변환하는 [[198_abstraction_control_data_process|추상화]]([[198_abstraction_control_data_process|Abstraction]]) 프레임워크이자 도구 모음이다.
> 2. **가치**: 구조(정적 특성), 연산(동적 특성), 제약조건([[003_integrity|무결성]] 규칙)이라는 3요소를 완벽히 정의함으로써 시스템의 확장성과 [[001_dikw_pyramid|데이터]] 정합성을 동시에 확보한다.
> 3. **융합**: [[322_oop_4_characteristics|객체지향 프로그래밍]]([[322_oop_4_characteristics|OOP]])의 클래스-메서드-접근제어자 개념과 매핑되며, [[001_software_engineering_definition|소프트웨어 공학]]의 [[310_architecture|도메인 주도 설계]]([[310_architecture|DDD]])를 뒷받침하는 핵심 [[001_dikw_pyramid|데이터]] 기둥이다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[001_dikw_pyramid|데이터]] 모델([[001_dikw_pyramid|Data]] Model)은 현실 세계의 방대하고 무질서한 [[001_dikw_pyramid|데이터]]들을 어떻게 체계화하여 [[002_database_definition|데이터베이스]]에 저장하고 사용할 것인가를 결정하는 개념적 설계 도구이다. 건축물을 짓기 전 설계도가 필요하듯, 고품질의 정보 시스템을 구축하기 위해서는 "어떤 [[001_dikw_pyramid|데이터]]가 존재하는가", "그 [[001_dikw_pyramid|데이터]]들을 어떻게 조작할 것인가", "오류 [[001_dikw_pyramid|데이터]]의 입력을 어떻게 막을 것인가"에 대한 명확한 규칙이 필요하다.

이러한 요구에 따라 [[001_dikw_pyramid|데이터]] 모델은 **구조(Structure), 연산([[329_delta_encoding|Operation]]), 제약조건(Constraint)** 이라는 3가지 필수 구성 요소를 갖추게 되었다. 이 중 하나라도 누락되면 [[002_database_definition|데이터베이스]]는 형체를 잃거나(구조 부재), [[001_dikw_pyramid|데이터]]를 가공할 수 없거나(연산 부재), 쓰레기 [[001_dikw_pyramid|데이터]]가 쌓이는(제약조건 부재, GIGO) 심각한 [[352_defect_definition|결함]] 상태에 빠지게 된다.

[[001_dikw_pyramid|데이터]] 모델은 크게 요구사항을 [[003_bigdata_7v|시각화]]하는 '개념적 [[001_dikw_pyramid|데이터]] 모델(예: ER 모델)'과 DBMS에 종속적인 '[[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 모델(예: [[083_relationship_in_er_model|관계]]형 모델)'로 나뉘며, 이 두 단계 모두에서 3가지 구성 요소는 반드시 구체화되어야 한다.

```text
[그림 1: 데이터 모델의 필수 3요소와 역할 다이어그램]

                       [현실 세계의 비즈니스 요구사항]
                                     │ (추상화 / 모델링)
                                     ▼
                  ┌─────────────────────────────────────┐
                  │          데이터 모델 (Data Model)   │
                  │                                     │
                  │  (1) 구조 (Structure) - [정적]      │ ──> "무엇(What)을 저장할 것인가?"
                  │      : 개체, 속성, 관계의 형태      │     (예: 테이블, 컬럼, 트리 노드)
                  │                                     │
                  │  (2) 연산 (Operation) - [동적]      │ ──> "어떻게(How) 처리할 것인가?"
                  │      : 상태 변경, 검색, 조작 방법   │     (예: 관계 대수, SELECT/JOIN)
                  │                                     │
                  │  (3) 제약조건 (Constraint) - [규칙] │ ──> "무엇을 금지(Limit)할 것인가?"
                  │      : 무결성을 위한 논리적 규칙    │     (예: 기본키 제약, Not Null)
                  └─────────────────────────────────────┘
                                     │ (물리적 구현)
                                     ▼
                             [DBMS 데이터베이스]
```

이 도식은 [[001_dikw_pyramid|데이터]] 모델이 현실 세계를 DB로 번역하는 중간 번역기 역할을 수행하며, 세 가지 요소가 각각 정적 상태, 동적 행위, 통제 규칙이라는 시스템의 기본 요건을 만족시킴을 보여준다. 실무에서는 흔히 '구조(테이블)' 설계에만 집중하다가 '제약조건' 설계를 누락하여 [[001_dikw_pyramid|데이터]] 품질이 훼손되는 경우가 많은데, 이 모델링 3요소 프레임워크는 설계의 사각지대를 방지하는 [[435_checklist_based_testing|체크리스트]] 역할을 한다.

📢 **섹션 요약 비유**: 보드게임(현실 세계)을 컴퓨터 게임으로 만들려면, 게임판의 모양(구조), 말을 움직이는 방법(연산), 그리고 반칙을 막는 룰(제약조건)을 컴퓨터에게 알려줘야 하는 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[001_dikw_pyramid|데이터]] 모델을 [[017_relational_data_model|관계형 데이터 모델]]([[017_relational_data_model|Relational Data Model]])의 관점에서 구체적으로 해부해 보면, 각 구성 요소가 시스템 내부에서 어떻게 구동되는지 명확히 알 수 있다.

| 구성 요소 | 역할 (기능) | RDB에서의 구현 (예시) | 내부 동작 [[295_protocol_field_tcp_udp_icmp|프로토콜]] | 비유 |
|:---|:---|:---|:---|:---|
| **1. 구조** (Structure) | 개체와 개체 간의 연관성 등 [[001_dikw_pyramid|데이터]]의 '정적(Static)'인 형태 정의 | [[061_relation_schema_instance|릴레이션]]([[061_relation_schema_instance|Relation]]/Table), [[082_attribute_types_er_model|속성]]([[082_attribute_types_er_model|Attribute]]), [[063_relation_tuple_cardinality|튜플]](Tuple) | [[020_ddl|DDL]](Create/Alter)을 통해 [[011_system_catalog|시스템 카탈로그]]의 [[012_metadata|메타데이터]]로 영구 등록 | 건물의 뼈대와 방의 배치 |
| **2. 연산** ([[329_delta_encoding|Operation]]) | [[001_dikw_pyramid|데이터]]를 검색하고 조작하는 '동적(Dynamic)'인 상태 변화 메커니즘 | [[038_relational_algebra|관계 대수]] ([[520_select|Select]], [[042_relational_algebra_project|Project]], [[521_join|Join]] 등) 및 SQL [[083_dml|DML]] (Insert, Update) | [[502_dbms|DBMS]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 파싱 → [[166_execution_plan_optimizer_navigation_tree|실행 계획]] [[087_process_state_transition|생성]] → 스토리지 엔진 I/O 호출 | 건물 내 엘리베이터 이동과 리모델링 작업 |
| **3. 제약조건** (Constraint) | [[001_dikw_pyramid|데이터]]의 [[369_logic_bomb|논리]]적 모순을 막는 '[[003_integrity|무결성]]([[003_integrity|Integrity]])' 통제 규칙 | [[074_entity_integrity_primary_key|개체 무결성]](PK), [[075_referential_integrity_foreign_key_cascade|참조 무결성]](FK), [[076_domain_integrity|도메인 무결성]](Check) | [[083_dml|DML]] 실행 전 [[191_transaction_concept_states|트랜잭션]] 매니저가 제약조건 위반 검사, 위반 시 예외([[313_rollback|Rollback]]) 발생 | 건물 입구의 보안 게이트 및 출입증 검사 |

**핵심 원리: 연산과 제약조건의 상호 작용**
연산(조작)이 일어날 때 시스템은 반드시 제약조건을 평가해야 한다. 예를 들어 `INSERT`(연산)를 수행할 때 입력되는 값이 Primary [[067_db_key_uniqueness_minimality|Key]] 제약(제약조건)을 위반하면 시스템은 상태 변화를 거부한다. 이는 연산의 자율성을 제약조건이라는 엄격한 바운더리가 통제하는 구조다.

```text
[그림 2: 데이터 조작 연산(Operation) 시 제약조건(Constraint) 검증 흐름도]

[Client] ── (연산 발생: UPDATE 부서코드=99 WHERE 사원=홍길동) ──┐
                                                               │
┌────────────────────── DBMS 트랜잭션 제어기 ──────────────────▼──┐
│                                                                 │
│  [1. 구조 확인]                                                 │
│   → '사원' 테이블과 '부서코드' 컬럼이 존재하는가? (Pass)        │
│                                                                 │
│  [2. 제약조건(참조 무결성) 검사]                                │
│   → '부서코드 99'가 부서(Parent) 테이블의 기본키에 존재하는가?  │
│      ├─ 존재함 (Pass) ────────┐                                 │
│      │                        ▼                                 │
│      │               [3. 연산 확정 적용] (데이터 갱신 반영)     │
│      │                                                          │
│      └─ 존재 안 함 (Fail) ────┐                                 │
│                               ▼                                 │
│               [연산 거부 및 Exception 발생 (ORA-02291 등)]      │
└─────────────────────────────────────────────────────────────────┘
```

이 흐름도의 핵심은 [[001_dikw_pyramid|데이터]] 모델에서 '연산'이 단독으로 [[001_dikw_pyramid|데이터]]를 갱신할 수 없고, 반드시 사전에 정의된 '제약조건' 필터를 통과해야만 '구조' 내에 정착할 수 있다는 인과 [[083_relationship_in_er_model|관계]]를 보여준다는 점이다. 제약조건이 DB 엔진 레벨(제약조건 검사)에서 수행될지, 아니면 애플리케이션 백엔드 코드 레벨에서 수행될지에 따라 시스템의 [[195_coupling_levels|결합도]]와 [[282_performance_tactics|성능]] 오버헤드가 크게 달라진다.

📢 **섹션 요약 비유**: 물([[001_dikw_pyramid|데이터]])이 [[123_pipe|파이프]](구조)를 타고 흐를 때(연산), 중간에 설치된 정수 필터(제약조건)가 불순물을 걸러내어 깨끗한 상태만을 목적지에 도달하게 하는 원리입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[001_dikw_pyramid|데이터]] 모델의 3요소는 개념적(Conceptual) 설계 단계와 [[369_logic_bomb|논리]]적(Logical) 설계 단계에서 각각 다른 모습으로 구체화된다. 대표적인 ER(Entity-[[083_relationship_in_er_model|Relationship]]) 모델과 RDB([[083_relationship_in_er_model|관계]]형) 모델 간의 구성 요소를 비교해 보면 이 [[198_abstraction_control_data_process|추상화]] 레벨의 차이를 알 수 있다.

| 구분 | 개념적 [[001_dikw_pyramid|데이터]] 모델 (ER 모델) | [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 모델 ([[083_relationship_in_er_model|관계]]형 모델) | [[001_software_engineering_definition|소프트웨어 공학]] 매핑 ([[322_oop_4_characteristics|OOP]]) |
|:---|:---|:---|:---|
| **구조 (Structure)** | 개체(Entity), [[082_attribute_types_er_model|속성]]([[082_attribute_types_er_model|Attribute]]), [[083_relationship_in_er_model|관계]]([[083_relationship_in_er_model|Relationship]]) | [[061_relation_schema_instance|릴레이션]]([[061_relation_schema_instance|Relation]]), 컬럼(Column), 외래키 매핑 | 클래스(Class), 인스턴스 변수(Field), 연관 [[083_relationship_in_er_model|관계]] |
| **연산 ([[329_delta_encoding|Operation]])** | 개념적 모델 단계에서는 연산을 명시적으로 표현하지 않음 | [[038_relational_algebra|관계 대수]] ([[038_relational_algebra|Relational Algebra]]), [[410_relational_calculus|관계 해석]], SQL [[083_dml|DML]] | 메서드(Method), 함수(Function) |
| **제약조건 (Constraint)** | 카디널리티 (1:1, 1:N), 필수/선택 참여 조건 | [[074_entity_integrity_primary_key|개체 무결성]](PK), [[075_referential_integrity_foreign_key_cascade|참조 무결성]](FK), [[064_relation_domain|도메인]]/NULL 규칙 | 유효성 검사 로직([[396_validation|Validation]]), 접근 제어자(Private) |

[[322_oop_4_characteristics|객체지향 프로그래밍]]([[322_oop_4_characteristics|OOP]]) 패러다임과 비교하면, DB의 '구조'는 OOP의 Class이고, '연산'은 Method이며, '제약조건'은 상태 불변성을 유지하기 위한 [[396_validation|Validation]] 로직에 해당한다. 즉, 객체지향 설계(OOD)와 [[002_database_definition|데이터베이스]] 모델링은 표현 방식만 다를 뿐, 대상을 [[198_abstraction_control_data_process|추상화]]하는 근본적인 패러다임을 공유(Synergy)하고 있다. 이것이 ORM(Object-Relational [[010_schema_mapping|Mapping]]) 기술이 탄생하게 된 구조적 기반이다.

```text
[그림 3: 데이터 모델별 구조적 차이 비교 매트릭스 (계층/망/관계형)]

┌────────────┬─────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│ 모델 유형  │ 계층형 (Hierarchical)       │ 망형 (Network)               │ 관계형 (Relational)          │
├────────────┼─────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ 1. 구조    │ 트리 (Tree) / 부모-자식     │ 그래프 (Graph) / 오너-멤버   │ 2차원 표 (Table) / 수학적 집합│
│ 2. 연산    │ 포인터 네비게이션 (순차적)  │ 링크 리스트 순회 탐색        │ 관계 대수 (조인 등 집합 연산)│
│ 3. 제약조건│ 자식은 부모 하나만 가짐(1:N)│ 여러 오너 소유 허용 (N:M)    │ 키 기반 참조 무결성 통제     │
│ 실무 활용  │ LDAP, XML 문서 구조         │ 초기 메인프레임 시스템       │ 현대 RDBMS의 절대적 표준     │
└────────────┴─────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

이 매트릭스는 과거부터 현대까지 [[001_dikw_pyramid|데이터]] 모델이 진화해 온 과정을 3요소 관점에서 명확히 대조한다. [[459_quic_fec_forward_error_correction|초기]] 계층/망형 모델은 '구조'가 복잡한 포인터로 얽혀 있어 '연산'이 매우 종속적이고 절차적이었다. 반면, [[083_relationship_in_er_model|관계]]형 모델은 표라는 단순한 '구조'와 수학적 집합 '연산([[038_relational_algebra|관계 대수]])'을 도입하여 [[001_dikw_pyramid|데이터]]를 직관적이고 비절차적으로 다룰 수 있게 함으로써 [[002_database_definition|데이터베이스]]의 대중화를 이끌어냈다.

📢 **섹션 요약 비유**: 자전거(개념적 모델)의 부품, 페달 밟기, 브레이크 규칙을 오토바이([[369_logic_bomb|논리]]적 모델)의 엔진, 가속 레버, 속도 제한 규칙으로 구체화하고 진화시키는 과정과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무 프로젝트에서 [[001_dikw_pyramid|데이터]] 아키텍트([[104_da_as_is_analysis|DA]])가 모델링을 수행할 때, 이 3요소 중 하나라도 소홀히 하면 심각한 [[100_technical_debt_monitoring_release_policy|기술 부채]]([[100_technical_debt_monitoring_release_policy|Technical Debt]])가 발생한다. 가장 빈번한 [[128_water_scrum_fall_anti_pattern|안티패턴]]은 '제약조건의 어플리케이션 전가'이다.

**1. 실무 시나리오: 제약조건(Constraint) 설계 누락 [[128_water_scrum_fall_anti_pattern|안티패턴]]**
- **문제**: 개발 편의성과 [[459_quic_fec_forward_error_correction|초기]] Insert [[282_performance_tactics|성능]]을 높이기 위해 RDBMS 설계 시 Foreign [[067_db_key_uniqueness_minimality|Key]](FK)와 NOT NULL 제약조건을 물리 모델에 걸지 않고, 자바(Java) 백엔드 코드 단에서만 [[395_verification_process_review|검증]] 로직을 구현함.
- **결과**: 시간이 지나면서 다수의 이기종 애플리케이션(배치 스크립트, 관리자 직접 조작 등)이 DB에 붙기 시작했고, [[395_verification_process_review|검증]] 코드를 타지 않은 우회 [[191_transaction_concept_states|트랜잭션]]이 발생하여 "고아 레코드(부모 없는 자식 [[001_dikw_pyramid|데이터]])"가 양산되는 치명적 [[001_dikw_pyramid|데이터]] 오염 발생.
- **의사결정 판단**: 아무리 [[619_msa_traffic_hardware|MSA]]([[532_microservices_decomposition_patterns|마이크로서비스]]) 기반이라 하더라도, 핵심 비즈니스 정합성을 지키는 최소한의 [[075_referential_integrity_foreign_key_cascade|참조 무결성]]과 [[064_relation_domain|도메인]] 제약조건은 DB 계층에(물리 모델에) 강력하게 강제화(Enforce)해야 한다. DB의 제약조건이야말로 [[288_data_swamp_metadata_management_absence|데이터 늪]]을 막는 최후의 보루이다.

**2. 실무 시나리오: 연산([[329_delta_encoding|Operation]]) 효율성을 위한 구조(Structure) 반정규화**
- **상황**: [[093_normalization|정규화]] 원칙에 따라 설계된 [[105_third_normal_form_3nf_transitive|3NF]] 구조에서, 조인([[521_join|Join]]) 연산이 너무 많아 대시보드 조회 화면에서 [[573_timeout_retry_backoff_strategy|타임아웃]]([[015_지연_데이터_관점|지연]]) 발생.
- **판단**: 읽기 연산(Read [[329_delta_encoding|Operation]])의 [[282_performance_tactics|성능]]을 위해 일부 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 제약(중복 제거)을 의도적으로 위배하고 파생 컬럼을 추가하는 반정규화(De-[[093_normalization|normalization]]) 구조로 모델을 타협함. 이때 중복된 구조의 정합성을 맞추기 위해 주기적인 배치(Batch) 연산을 보완책으로 추가 설계해야 한다.

```text
[그림 4: 데이터 품질 확보를 위한 모델링 3요소 설계 체크리스트 흐름도]

[요구사항 분석] ──> [논리적 데이터 모델링]
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   [구조 설계]      [연산(트랜잭션) 분석] [제약조건 설계]
 - 정규화 준수?     - CRUD 빈도는?     - PK/FK 식별 관계 명확?
 - 슈퍼/서브타입?   - 복잡한 조인 유무? - 도메인(Check/Null) 유효?
        │                │                │
        └───────┬────────┴────────┬───────┘
                ▼                 ▼
          (구조가 연산을     (제약이 연산을
           감당 가능한가?)    안전하게 막는가?)
                │                 │
                ▼                 ▼
          [병목 예상 시]     [오류 예상 시]
          (반정규화 적용)    (DB/App 검증 분리)
                         │
                         ▼
                [물리적 데이터베이스 생성]
```

이 [[124_decision_tree|의사결정 트리]]는 실무 설계 시 세 가지 요소가 독립적으로 끝나는 것이 아니라 지속적으로 [[250_cross_validation_kfold|교차 검증]]되어야 함을 보여준다. '구조'만 예쁘게 짠다고 끝이 아니라, 그 구조 위에서 일어날 '연산'의 부하를 버틸 수 있는지, 파괴적인 연산을 '제약조건'이 빈틈없이 차단할 수 있는지 [[395_verification_process_review|검증]]하는 루프가 모델링 품질의 핵심이다.

📢 **섹션 요약 비유**: 멋진 자동차(구조)를 설계했다고 끝이 아니라, 시속 200km로 달리는 상황(연산)에서 브레이크 시스템(제약조건)이 완벽히 동작하는지 시뮬레이션해야 실제 도로에 나갈 수 있는 것과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

| 지표 | 정량적/정성적 기대효과 | 모델링 관점의 가치 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 정합성 | [[352_defect_definition|결함]] [[001_dikw_pyramid|데이터]](GIGO) 발생률 99% 차단 | 견고한 '제약조건' 설계에 의한 예외 원천 봉쇄 |
| [[346_maintainability_portability|유지보수성]] | 구조 파악 시간 단축 및 스파게티 [[298_qkv_attention|쿼리]] 감소 | [[093_normalization|정규화]]된 '구조'와 최적화된 '연산' 매핑의 효과 |
| 확장성 | 신규 비즈니스 로직 추가 시 DB 재설계 비용 최소화 | [[198_abstraction_control_data_process|추상화]] 원칙이 잘 지켜진 유연한 모델의 이점 |

[[001_dikw_pyramid|데이터]] 모델의 3요소(구조, 연산, 제약조건)는 과거 E.F. Codd 박사가 [[083_relationship_in_er_model|관계]]형 모델을 제창한 이래 50년 넘게 정보 시스템 설계의 불변하는 진리로 자리 잡고 있다.

최근의 [[035_nosql|NoSQL]]([[037_document|Document]], [[104_graph|Graph]])이나 [[208_data_lake_schema_on_read|데이터 레이크]] 환경에서는 [[459_quic_fec_forward_error_correction|초기]]에 '제약조건'을 풀고 '구조'를 유연하게 가져가는 "[[009_schema_on_read|스키마 온 리드]]([[009_schema_on_read|Schema-on-read]])" 방식이 대두되고 있으나, 이 역시 연산 단계(Read)에서 구조와 제약조건을 동적으로 적용할 뿐 3요소의 본질 자체가 사라진 것은 아니다. 시스템이 진화할수록 [[001_dikw_pyramid|데이터]]를 안전하게 담고(구조), 빠르고 정확하게 꺼내며(연산), 썩지 않게 보존하는(제약조건) [[001_dikw_pyramid|데이터]] 모델링의 근본 원칙은 그 중요성을 더욱 더해가고 있다.

📢 **섹션 요약 비유**: 집을 짓는 기술([[035_nosql|NoSQL]], 클라우드)이 아무리 발전하더라도, 기둥(구조)을 세우고, 문을 열며(연산), 비바람을 막는 지붕(제약조건)이 있어야 집이라는 본질은 절대 변하지 않습니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- 개체 [[083_relationship_in_er_model|관계]] 모델 (ER Model) | 구조(개체/[[082_attribute_types_er_model|속성]])와 제약조건(카디널리티)을 시각적으로 도식화하는 개념적 모델링 표준 도구
- [[038_relational_algebra|관계 대수]] ([[038_relational_algebra|Relational Algebra]]) | [[017_relational_data_model|관계형 데이터 모델]]의 '연산'을 수학적 집합론에 근거하여 절차적으로 표현한 언어
- [[073_integrity_constraints_overview|무결성 제약조건]] ([[073_integrity_constraints_overview|Integrity Constraints]]) | [[001_dikw_pyramid|데이터]]의 [[002_bigdata_5v|정확성]]과 [[194_consistency_database_integrity|일관성]]을 유지하기 위해 DB에 선언하는 '제약조건'의 집합 (개체/[[316_reference_pattern_nosql|참조]]/[[064_relation_domain|도메인]])
- [[093_normalization|정규화]] ([[093_normalization|Normalization]]) | [[090_anomaly_insertion_deletion_update|이상 현상]]을 제거하기 위해 [[061_relation_schema_instance|릴레이션]]의 '구조'를 [[094_functional_dependency_fd|함수적 종속성]]에 따라 작게 분해하는 과정
- 객체 [[083_relationship_in_er_model|관계]] 매핑 (ORM) | 객체 지향의 클래스(구조/연산)와 [[083_relationship_in_er_model|관계]]형 DB의 테이블(구조) 간의 [[004_impedance|임피던스]] 불일치를 해결하는 미들웨어 기술


### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 모델 3요소 — 구조(Structure), 연산(Operation), 제약(Constraint)]
    │
    ▼
[개념적 데이터 모델 (E-R 다이어그램) — 엔티티·속성·관계 개념적 표현]
    │
    ▼
[논리적 데이터 모델 (관계형 모델) — 테이블·키·정규화·SQL 규칙 정의]
    │
    ▼
[물리적 데이터 모델 — 인덱스·파티션·스토리지 엔진 매핑]
    │
    ▼
[NoSQL / 다중 모델 DB — 유연한 구조로 비정형 데이터 제약 완화]
```

이 흐름은 [[001_dikw_pyramid|데이터]] 모델의 추상 3요소에서 출발해 개념·[[369_logic_bomb|논리]]·물리 설계 단계로 구체화되고, [[004_unstructured_data|비정형 데이터]] 요구에 따라 NoSQL로 모델 제약이 완화되는 [[001_dikw_pyramid|데이터]] 설계 발전 과정을 보여준다.


### 👶 어린이를 위한 3줄 비유 설명
1. 게임을 만들기 위해서는 3가지가 꼭 필요해요. 첫째는 캐릭터와 맵의 생김새(구조)입니다.
2. 둘째는 캐릭터가 달리고 점프하고 공격하는 방법(연산)입니다.
3. 셋째는 캐릭터가 벽을 뚫고 지나가거나 체력이 0인데도 살아있지 못하게 막는 규칙(제약조건)입니다. 이 3가지가 [[001_dikw_pyramid|데이터]] 모델이에요.
