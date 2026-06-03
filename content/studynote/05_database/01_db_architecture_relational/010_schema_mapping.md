+++
title = "10. 스키마 매핑 (Mapping) - 외부/개념 사상, 개념/내부 사상"
description = "데이터 독립성을 보장하는 3단계 스키마 간의 사상(Mapping) 메커니즘"
date = 2024-05-20

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑 ([Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) Mapping)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ANSI/SPARC [3단계 스키마 아키텍처](/knowledge-base/studynote/05_database/01_db_architecture_relational/006_three_level_schema_architecture/)에서 외부-개념, 개념-[내부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/009_internal_schema/) 계층을 서로 연결하여 상호 변환해 주는 '규칙(Rule)'이자 '인터페이스'입니다.
> 2. **가치**: 한 계층의 구조가 변경되더라도 [매핑 규칙](/knowledge-base/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/)만 수정함으로써 다른 계층에 영향을 주지 않도록 격리하는 **[데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)([Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/))**의 실질적인 구현체입니다.
> 3. **융합**: [소프트웨어 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/)의 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)([Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)) 패턴, ORM(Object-Relational Mapping)의 [임피던스](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) 불일치 해결 원리와 기술적 철학을 완벽히 공유합니다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 3단계 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)(외부, 개념, 내부)를 독립적으로 정의해 두더라도, 이들 간에 원활한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 일어나지 않는다면 아키텍처는 동작할 수 없습니다. [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑([Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) Mapping), 우리말로는 '사상(寫像)'이라 불리는 이 기술은 서로 다른 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 수준을 가진 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 간의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 변환하고 대응시키는 규칙의 집합입니다. 
만약 매핑 계층이 없다면, 테이블에 컬럼이 하나 추가되거나 디스크의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로가 바뀌었을 때 응용 프로그램의 소스코드를 모두 뒤져서 수정해야 합니다. 매핑은 계층 간의 완충 지대(Buffer Zone)를 형성하여 하위 계층의 변경이 상위 계층으로 전파되는 것을 차단합니다. 현대 시스템에서 비즈니스 로직(응용 프로그램)과 스토리지(물리 DB)가 수명 주기를 달리하며 발전할 수 있는 이유는 전적으로 이 매핑 매커니즘 덕분입니다.

다음 그림은 3단계 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 구조 사이에서 두 가지 매핑이 어떻게 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)을 형성하는지 보여줍니다.
```text
[ 외부 스키마 ] (User View 1)      [ 외부 스키마 ] (User View 2)
       │                                 │
       └──> 외부/개념 매핑 (논리적 데이터 독립성 보장) <──┘
                       │
[ 개념 스키마 ] (Global Logical Structure)
                       │
           개념/내부 매핑 (물리적 데이터 독립성 보장)
                       │
[ 내부 스키마 ] (Physical Storage & Index)
```
이 도식에서 핵심은 매핑이 단순한 선이 아니라, 변화를 흡수하는 '변환기(Translator)'라는 점입니다. [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)은 위쪽 매핑을 통해 보장되고, 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)은 아래쪽 매핑을 통해 보장됩니다. 실무에서 시스템 유지보수 비용을 낮추는 핵심 비결은 바로 이 [매핑 규칙](/knowledge-base/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/)을 [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) 내부에 안전하게 캡슐화해 두는 것입니다.

📢 **섹션 요약 비유**: 서로 다른 언어를 쓰는 세 나라의 대통령(외부, 개념, 내부)이 회담할 때, 중간에서 완벽하게 뜻을 통역해 주어 오해를 막고 대화를 이어주는 두 명의 동시통역사(매핑)와 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑은 위치에 따라 두 가지로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)되며, 각기 다른 수준의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 재작성과 [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) 조회를 수행합니다.

| 매핑 종류 | 연결 대상 | 보장하는 독립성 | 실무적 구현 사례 | 비유 |
|:---|:---|:---|:---|:---|
| **외부/개념 사상** ([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 매핑) | [외부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/007_external_schema/) ↔ [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/) | **[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)** | [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) (CREATE [VIEW](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)), INSTEAD OF [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | 외화 번역기 |
| **개념/내부 사상** (물리적 매핑) | [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/) ↔ [내부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/009_internal_schema/) | **물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)** | [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), Tablespace 변경, [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | 물류 라우터 |

사용자의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 두 단계의 매핑을 거쳐 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 도달하는 심층 동작 흐름은 다음과 같습니다.
```text
1. [User Query] SELECT name FROM Employee_View;
        ↓
2. [외부/개념 매핑 동작] 
   - 딕셔너리 조회: Employee_View는 'EMP' 테이블의 'emp_name' 컬럼과 매핑됨.
   - 쿼리 변환: SELECT emp_name FROM EMP;
        ↓
3. [개념/내부 매핑 동작] 
   - 딕셔너리 조회: 'EMP' 테이블은 'DATA_TBS_01' 파일의 14번 블록에 있음.
   - 접근 경로 산출: 'EMP_NAME_IDX' B-Tree 인덱스를 거쳐 Heap 데이터로 접근.
        ↓
4. [Storage Engine] 디스크 I/O 실행 및 역방향 매핑을 거쳐 결과 반환
```
이 흐름의 핵심은 매핑이 런타임에 동적으로 일어난다는 점입니다. [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)([Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/))와 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 파서가 [시스템 카탈로그](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/)([데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/))에 저장된 [매핑 규칙](/knowledge-base/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/)을 읽어와서 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 계속해서 재작성(Rewriting)합니다. 하지만 이 동적 변환 과정에는 CPU 연산 비용이 듭니다. 따라서 매핑이 너무 복잡해지면(예: 수십 개의 뷰 중첩), 매핑 해석에만 수 초가 걸리는 오버헤드가 발생할 수 있으므로 딕셔너리 캐시(Dictionary Cache)를 통해 [매핑 규칙](/knowledge-base/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/)을 메모리에 올려두는 최적화가 필수적입니다.

📢 **섹션 요약 비유**: 웹사이트 주소창에 `www.google.com`을 치면 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버(외부/개념 매핑)가 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 IP를 찾아주고, 공유기의 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블(개념/내부 매핑)이 실제 랜선 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 찾아주는 완벽한 중계 시스템입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
두 매핑 계층이 제공하는 '독립성'의 성격과 관리 포인트를 비교해 봅니다.

| 비교 항목 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) (외부/개념 매핑) | 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) (개념/내부 매핑) |
|:---|:---|:---|
| **발생 원인** | [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조 변경 (테이블 분할, 병합, 컬럼 추가) | [내부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/009_internal_schema/)의 물리적 변경 (디스크 교체, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 추가, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치 이동) |
| **[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상** | 사용자 뷰, 응용 프로그램(코드) | [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/)의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 규칙 및 전체 아키텍처 |
| **대처 방법** | 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 수정하여 이전 구조 모사 | 시스템 내부 테이블스페이스 포인터 갱신 |
| **달성 난이도**| **어려움** (비즈니스 로직과 강하게 결합됨) | **쉬움** ([DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 엔진이 자동 처리하는 부분 많음) |

이 매트릭스는 물리적 독립성에 비해 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 독립성을 달성하는 것이 훨씬 어렵다는 점을 시사합니다. 하드웨어 드라이브를 SSD로 교체하는 물리적 변경은 DBMS가 알아서 매핑을 조정해 주지만, 테이블이 분리되는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 변경은 DBA가 직접 뷰를 재작성하여 외부/개념 매핑을 수동으로 이어주지 않으면 응용 프로그램에 즉각적인 장애가 발생합니다.

📢 **섹션 요약 비유**: 물리적 독립성(개념/내부 매핑)은 자동차 바퀴를 바꿔도 운전대는 그대로 쓸 수 있는 것이고, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 독립성(외부/개념 매핑)은 자동차가 비행기로 바뀌어도 기존의 운전대로 조종하게끔 고도의 시뮬레이터를 달아주는 것입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무 환경에서 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑 원리를 활용하여 대규모 마이그레이션이나 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 위험을 회피할 수 있습니다.

1. **테이블 분할 시나리오 (무중단 마이그레이션)**:
   - 상황: 비대해진 `Order` 테이블을 `Order_Master`와 `Order_Detail`로 분할([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))해야 함.
   - [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): 물리적 테이블은 2개로 분할하되, [외부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/007_external_schema/)에 `Order`라는 이름의 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 두 테이블을 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))하여 매핑해 둠.
   - 결과: 기존 레거시 앱은 여전히 `Order`라는 1개의 뷰를 찌르므로 앱 소스 코드는 한 줄도 수정할 필요가 없음. (외부/개념 매핑 활용)

2. **물리 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 적용 시나리오**:
   - 상황: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 테이블 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 너무 커져서 I/O 병목 발생.
   - [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 테이블 구조는 그대로 둔 채, [내부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/009_internal_schema/) 매핑만 변경하여 월별 [Range Partitioning](/knowledge-base/studynote/05_database/03_relational_model/180_range_partitioning/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 디스크를 분리.
   - 결과: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 응답 속도는 개선되지만, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조([개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/))는 동일하므로 상위의 모든 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)문은 유지됨. (개념/내부 매핑 활용)

다음은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 구조 변경 시 매핑을 통해 장애를 격리하는 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)입니다.
```text
[개념 스키마 변경 필요성 발생: 컬럼명 변경]
   ↓
[응용 프로그램 영향도 평가]
   ├─> (직접 참조 중) ──> 매핑(View) 부재로 즉각 장애 발생 (안티패턴)
   └─> (View를 통한 간접 참조 중)
          ↓
[외부/개념 매핑 규칙 수정]
   => ALTER VIEW User_View AS SELECT new_col_name AS old_col_name FROM Table;
          ↓
[격리 성공] 응용 프로그램은 과거 컬럼명으로 지속 접근 가능 (장애 제로)
```
이 흐름의 핵심은 "인터페이스와 구현의 분리"라는 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 대원칙이 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 매핑 계층에도 정확히 적용된다는 점입니다. 실무에서는 이러한 매핑 기술 덕분에 24시간 365일 무중단 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 가능합니다.

📢 **섹션 요약 비유**: 충격이 발생했을 때 자동차 본체와 탑승자 사이에서 진동을 완벽하게 흡수하여 승차감을 유지해 주는 자동차의 서스펜션(쇼크 업소버) 시스템과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑의 완벽한 구현은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 유연성을 극대화하고 개발과 운영 조직 간의 책임을 분리합니다.

| 정량적 효과 | 정성적 효과 |
|:---|:---|
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 애플리케이션 코드 수정 비용(MM) 80% 절감 | 인프라 교체 및 스토리지 마이그레이션의 위험 부담 최소화 |
| [DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/) 작업에 따른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 다운타임(Downtime) [제로화](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 모델러([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))와 물리 엔지니어([DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)) 간의 명확한 역할 분리 |

미래의 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)에서는 ORM(Object-Relational Mapping) 프레임워크가 외부/개념 매핑의 상당 부분을 애플리케이션 계층으로 가져가고 있습니다. JPA나 Hibernate 같은 도구들은 DB 내부의 매핑뿐만 아니라, 객체 지향 언어와 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 간의 '[임피던스](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) 불일치([Impedance](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) Mismatch)'를 해결하는 또 다른 차원의 강력한 [외부 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/007_external_schema/) 매핑 도구로 진화하고 있습니다.

📢 **섹션 요약 비유**: 과거, 현재, 미래의 어떤 규격의 플러그라도 꽂기만 하면 적절한 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)으로 변환해 주는 완벽한 만능 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)(Universal [Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))입니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* ANSI/SPARC 3단계 아키텍처 (매핑이 활동하는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 무대)
* [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) (매핑 계층이 존재하는 궁극적인 목적, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적/물리적 독립성)
* 뷰 ([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) (외부/개념 매핑을 실제로 구현하는 가장 강력한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 객체)
* ORM (Object-Relational Mapping) (DB를 넘어 애플리케이션 단에서 수행되는 확장된 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑)
* [임피던스](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) 불일치 ([Impedance](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) Mismatch) (객체 모델과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 모델 간의 차이를 매핑으로 극복해야 하는 과제)

### 📈 관련 키워드 및 발전 흐름도

```text
[개념적 스키마 (Conceptual Schema) — 비즈니스 엔티티·관계 모델링]
    │
    ▼
[논리적 스키마 (Logical Schema) — 관계형 테이블·키 정규화]
    │
    ▼
[물리적 스키마 (Physical Schema) — 저장 구조·인덱스·파티셔닝]
    │
    ▼
[스키마 매핑 (Schema Mapping) — 계층 간 변환 규칙 정의]
    │
    ▼
[ETL / 데이터 통합 — 이기종 스키마 간 데이터 이동]
    │
    ▼
[스키마 레지스트리 (Schema Registry) — 이벤트 기반 스키마 버전 관리]
```
[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑은 추상적 개념 모델을 물리 저장소로 변환하는 다리 역할을 하며, ETL과 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)로 이어지는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합의 핵심 기반이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 미국 친구(앱)와 한국 친구([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))가 전화를 하면 서로 말이 안 통해서 답답해요.
2. [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 매핑은 중간에서 영어와 한국어를 아주 빠르게 통역해 주는 '똑똑한 통역사 선생님'이에요.
3. 한국 친구가 갑자기 사투리를 쓰게(내부 구조 변경) 되어도, 통역사 선생님이 알아서 표준 영어로 바꿔주니까 미국 친구는 아무 문제 없이 계속 대화할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 10 / 600

← **이전**: [9. 내부 스키마 (Internal Schema) - 물리적 저장 장치 관점](/knowledge-base/studynote/05_database/01_db_architecture_relational/009_internal_schema/)
**다음**: [11. 시스템 카탈로그 (System Catalog) / 데이터 사전 (Data Dictionary) - 메타데이터(Metadata)](/knowledge-base/studynote/05_database/01_db_architecture_relational/011_system_catalog/) →

---
