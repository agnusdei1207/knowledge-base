+++
weight = 4
title = "4. 데이터 독립성 (Data Independence) - 논리적 독립성 vs 물리적 독립성"
description = "논리적 독립성과 물리적 독립성의 개념, 사상(Mapping) 원리 및 데이터베이스 스키마 보호 아키텍처"
date = "2024-05-20"
[taxonomies]
tags = ["Data Independence", "Database", "논리적 독립성", "물리적 독립성"]
categories = ["Database", "Studynote"]
+++

# 04. [[001_dikw_pyramid|데이터]] 독립성 ([[504_data_independence|Data Independence]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[001_dikw_pyramid|데이터]] 독립성은 하위 단계의 [[001_dikw_pyramid|데이터]] 구조(물리적 저장 방식이나 전체 [[369_logic_bomb|논리]] 구조)가 변경되더라도 상위 단계의 응용 프로그램이나 사용자에게 영향을 주지 않는 [[002_database_definition|데이터베이스]] 시스템의 핵심 방어 기제입니다.
> 2. **가치**: 응용 프로그램 유지보수 비용을 기하급수적으로 낮추고, 무중단으로 스토리지 [[282_performance_tactics|성능]] 튜닝이나 [[005_schema|스키마]] 확장을 가능하게 하여 비즈니스 민첩성을 극대화합니다.
> 3. **융합**: [[322_oop_4_characteristics|객체지향 프로그래밍]]([[322_oop_4_characteristics|OOP]])의 캡슐화(Encapsulation) 원칙 및 [[201_software_architecture_definition|소프트웨어 아키텍처]]의 인터페이스 기반 다형성과 근본 궤를 같이하는 시스템 설계 사상입니다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[002_database_definition|데이터베이스]] 시스템이 발명되기 이전의 전통적인 [[501_file_definition_logical_record|파일]] 시스템([[501_file_definition_logical_record|File]] System) 환경에서는 애플리케이션 프로그램과 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]이 강하게 결합되어 있었습니다. 개발자는 [[501_file_definition_logical_record|파일]]의 물리적 경로, [[001_dikw_pyramid|데이터]] 레코드의 크기, 인코딩 방식까지 모든 물리적 세부 사항을 프로그램 코드 내에 하드코딩해야만 했습니다.

이러한 **[[001_dikw_pyramid|데이터]] [[008_dependencies|종속성]]([[001_dikw_pyramid|Data]] Dependency)** 은 재앙에 가까운 결과를 낳았습니다. 만약 [[282_performance_tactics|성능]]을 위해 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]의 정렬 방식을 바꾸거나 새로운 필드를 하나 추가하기만 해도, 이 [[501_file_definition_logical_record|파일]]을 읽는 수십 개의 프로그램 소스 코드를 모두 찾아 수정하고 다시 컴파일해야 했습니다. 시스템이 커질수록 [[001_dikw_pyramid|데이터]] 구조 변경은 사실상 불가능해졌고, 이는 IT 인프라 발전의 거대한 병목으로 작용했습니다.

이러한 [[008_dependencies|종속성]]의 늪을 끊어내기 위해 고안된 개념이 바로 **[[001_dikw_pyramid|데이터]] 독립성 ([[504_data_independence|Data Independence]])** 입니다. 

```text
[종속성의 늪: 파일 시스템의 연쇄 붕괴]
변경 발생: "고객 파일에 '이메일' 칼럼 추가"
   │
   ├─> (Crash) 영업 App: 바이트 오프셋 밀림 현상 발생 -> 코드 수정
   ├─> (Crash) 배송 App: 파일 읽기 에러 발생 -> 코드 수정
   └─> (Crash) 정산 App: 배열 파싱 오류 -> 코드 수정
   => 작은 데이터 변경이 전사 시스템 마비 유발!

[데이터 독립성: DBMS의 방어막 구조]
변경 발생: "고객 테이블에 '이메일' 칼럼 추가"
   │
   ├─> DBMS Engine: 내부 매핑(Mapping) 정보만 업데이트
   │
   ├─> 영업 App: (기존 SELECT 이름, 전화번호 FROM 고객) -> 정상 작동!
   ├─> 배송 App: (기존 SELECT 주소 FROM 고객) -> 정상 작동!
   └─> 정산 App: 새로운 '이메일' 칼럼 무시 -> 정상 작동!
```
이 도식은 [[001_dikw_pyramid|데이터]] 독립성이 왜 필수적인지 극명하게 보여줍니다. [[501_file_definition_logical_record|파일]] 시스템은 작은 변화가 모든 상위 시스템에 장애를 전파(Crash)하지만, [[002_database_definition|데이터베이스]] 환경에서는 DBMS가 '방어막(매핑 레이어)' 역할을 수행하여 기존 애플리케이션의 [[298_qkv_attention|쿼리]]에 영향을 주지 않습니다. 실무에서는 이 방어막 덕분에 무중단 [[090_service_kubernetes_network_load_balancing|서비스]] 중에도 칼럼을 추가하거나 디스크를 SSD로 교체하는 등의 마이그레이션 작업이 가능해집니다.

📢 **섹션 요약 비유**: 건물 전체의 배관(물리적 [[001_dikw_pyramid|데이터]])을 수리해도, 각 사무실의 수도꼭지(응용 프로그램) 모양이나 사용법은 전혀 바꾸지 않고 그대로 물을 쓸 수 있게 해주는 마법의 배관 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[001_dikw_pyramid|데이터]] 독립성을 시스템적으로 구현하기 위해 ANSI/SPARC 위원회는 [[002_database_definition|데이터베이스]] [[005_schema|스키마]]를 3단계(외부, 개념, 내부)로 나누고, 각 계층 사이에 **사상([[010_schema_mapping|Mapping]], 매핑)** 이라는 개념을 도입했습니다. 독립성은 이 매핑 계층이 변경 사항을 흡수(Translation)함으로써 달성됩니다.

[[001_dikw_pyramid|데이터]] 독립성은 크게 두 가지 수준으로 나뉩니다.

| 독립성 유형 | 정의 및 역할 | 내부 메커니즘 (방어 원리) | 비유 |
|:---|:---|:---|:---|
| **[[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 독립성**<br>(Logical [[133_independence|Independence]]) | [[008_conceptual_schema|개념 스키마]]가 변경되어도 [[007_external_schema|외부 스키마]]나 응용 프로그램에 영향을 주지 않는 성질 | 외부/개념 매핑([[010_schema_mapping|Mapping]]) 변경.<br>테이블이 분할되거나 합쳐져도 **뷰([[151_sql_view_virtual_table|View]])** 를 통해 기존 형태 유지 | 회사 조직도가 바뀌어도, 고객이 거는 대표 번호는 바뀌지 않음 |
| **물리적 [[001_dikw_pyramid|데이터]] 독립성**<br>(Physical [[133_independence|Independence]]) | [[009_internal_schema|내부 스키마]](물리적 저장 구조)가 변경되어도 개념/[[007_external_schema|외부 스키마]]에 영향을 주지 않는 성질 | 개념/내부 매핑([[010_schema_mapping|Mapping]]) 변경.<br>디스크 [[179_table_partitioning_concept|파티셔닝]], [[154_database_index_b_tree_search_optimization|인덱스]] 추가 시 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 경로만 재계산 | 창고 위치가 서울에서 부산으로 바뀌어도 주문 시스템은 똑같이 동작 |

이 두 독립성이 매핑([[010_schema_mapping|Mapping]]) 계층을 통해 어떻게 [[571_protection_vs_security|보호]]막을 형성하는지 아래 다이어그램으로 [[396_validation|확인]]할 수 있습니다.

```text
┌────────────────────────────────────────────────────────┐
│ [ Application A ]         [ Application B ]            │
│  (외부 스키마: View A)       (외부 스키마: View B)      │
└─────────┬───────────────────────┬──────────────────────┘
          │ (1) 논리적 독립성 보장 구역 (External/Conceptual Mapping)
          │     - 테이블 통합/분리 시 여기서 뷰 정의만 변경하여 대응
┌─────────▼───────────────────────▼──────────────────────┐
│                  [ 개념 스키마 ]                       │
│        (전체 조직의 통합된 논리적 데이터 구조)         │
│          Entity: Employee (Name, Dept, Salary)         │
└─────────────────────────┬──────────────────────────────┘
                          │ (2) 물리적 독립성 보장 구역 (Conceptual/Internal Mapping)
                          │     - 스토리지 위치, 인덱싱 변경 시 여기서 경로만 재설정
┌─────────────────────────▼──────────────────────────────┐
│                  [ 내부 스키마 ]                       │
│         (디스크 파일, B-Tree 인덱스, 클러스터링)       │
│      File Path: /dev/sdb1, Block Size: 8KB             │
└────────────────────────────────────────────────────────┘
```
이 구조도의 핵심은 매핑([[010_schema_mapping|Mapping]]) 계층의 존재입니다. 만약 전체 조직의 테이블([[008_conceptual_schema|개념 스키마]]) 구조가 완전히 뜯어고쳐져도, (1)번 구역에서 SQL [[151_sql_view_virtual_table|View]] 매핑만 다시 맞춰주면 애플리케이션 코드는 단 한 줄도 수정할 필요가 없습니다. 마찬가지로, HDD에서 [[482_nvme|NVMe]] SSD로 하드웨어를 교체하여 저장 방식이 바뀌어도, (2)번 구역이 변경된 물리적 주소를 [[198_abstraction_control_data_process|추상화]]하여 [[008_conceptual_schema|개념 스키마]]에 전달하므로 위쪽 레이어는 알 필요가 없습니다. 실무에서는 물리적 독립성([[154_database_index_b_tree_search_optimization|인덱스]], [[179_table_partitioning_concept|파티셔닝]] 변경)은 쉽게 달성되지만, [[369_logic_bomb|논리]]적 독립성은 [[020_ddl|DDL]] 변경의 파급력이 커서 완벽한 달성이 상대적으로 더 어렵습니다.

📢 **섹션 요약 비유**: 전원 플러그([[007_external_schema|외부 스키마]])의 모양만 맞으면, 벽 너머의 전선([[008_conceptual_schema|개념 스키마]])이 구리선이든 알루미늄이든, 심지어 발전소가 원자력에서 태양광([[009_internal_schema|내부 스키마]])으로 바뀌어도 TV를 보는 데는 아무 문제가 없는 원리와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[369_logic_bomb|논리]]적 독립성과 물리적 독립성은 달성 난이도와 운영에 미치는 영향이 매우 다릅니다. 이 둘의 트레이드오프와 아키텍처적 차이를 비교 분석해야 합니다.

| 분석 항목 | [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 독립성 | 물리적 [[001_dikw_pyramid|데이터]] 독립성 |
|:---|:---|:---|
| **발생 [[507_acid_properties|트리거]]** | 비즈니스 로직 변경, 새로운 [[001_dikw_pyramid|데이터]] 엔티티 추가, 테이블 [[093_normalization|정규화]]/반정규화 | 스토리지 용량 부족, 검색 [[282_performance_tactics|성능]] 저하에 따른 [[154_database_index_b_tree_search_optimization|인덱스]] 튜닝, [[179_table_partitioning_concept|파티셔닝]] |
| **방어 수단** | **뷰([[151_sql_view_virtual_table|View]])**, 서브쿼리, [[186_stored_procedure_trigger|스토어드 프로시저]], 외부/개념 사상 수정 | **[[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[088_optimizer|Optimizer]])**, [[514_partition_slice_volume|파티션]] 매핑, 개념/내부 사상 수정 |
| **구현 난이도** | 어려움 ([[064_relation_domain|도메인]] 지식 필요, 복잡한 View는 조인 [[282_performance_tactics|성능]] 저하 유발) | 쉬움 ([[502_dbms|DBMS]] 엔진이 대부분 자동 처리) |
| **애플리케이션 영향** | [[298_qkv_attention|쿼리]] 프로젝션([[520_select|SELECT]] 칼럼)과 관련된 컴파일 의존성 방어 | [[501_file_definition_logical_record|파일]] 경로, I/O 블록 사이즈 등에 대한 물리적 의존성 방어 |
| **연관 IT 기술** | [[542_api_gateway|API Gateway]] 패턴, 백엔드 [[198_abstraction_control_data_process|추상화]] 인터페이스 | [[015_virtualization|가상화]]([[190_virtualization_computing_architecture_cloud|Virtualization]]), LVM(Logical [[001_bigdata_3v_5v|Volume]] Manager) |

이를 타 시스템의 [[198_abstraction_control_data_process|추상화]] 계층과 융합하여 바라보면 흥미로운 유사성을 발견할 수 있습니다.

```text
[데이터베이스의 독립성] vs [운영체제의 가상 메모리] vs [네트워크의 OSI 7계층]

1. DB 물리적 독립성   ≒  OS 가상 메모리(Virtual Memory)
   DB가 물리 디스크 위치를 숨김  == OS가 RAM의 실제 물리 주소를 숨기고 가상 주소 제공.
   (디스크가 교체되어도 무관)       (RAM 조각나도 프로세스는 연속된 메모리로 인식)

2. DB 논리적 독립성   ≒  OSI 네트워크 전송 계층(Transport Layer)
   DB 스키마 변경이 App을 안 건드림 == 하위망(Wi-Fi/LTE)이 바뀌어도 TCP 세션은 안 끊어짐.
```
이 비교의 핵심은 컴퓨터 공학을 관통하는 "[[198_abstraction_control_data_process|추상화]]를 통한 디커플링(Decoupling)" 사상입니다. [[001_dikw_pyramid|데이터]] 독립성은 [[002_database_definition|데이터베이스]]에만 국한된 개념이 아니라, 시스템의 복잡도를 제어하기 위해 인터페이스를 분리하는 보편적 엔지니어링 원칙의 DB적 구현체입니다. 실무에서는 이러한 레이어 분리 때문에 매핑 연산([[010_schema_mapping|Mapping]] Overhead)이라는 필연적인 CPU/메모리 비용을 지불해야 하며, 이는 때때로 [[177_view_merging_query_transformation|뷰 머징]]([[177_view_merging_query_transformation|View Merging]]) 등 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]의 고도화된 최적화를 필요로 합니다.

📢 **섹션 요약 비유**: 물리적 독립성이 자동차의 타이어를 윈터 타이어로 바꿔도 운전법이 똑같은 것이라면, [[369_logic_bomb|논리]]적 독립성은 가솔린차를 전기차로 바꿔도 액셀러레이터를 밟는 느낌과 조작법을 똑같이 유지해주는 더 고차원적인 마법입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 [[002_database_definition|데이터베이스]] 구조는 비즈니스 성장에 따라 끊임없이 변화합니다. [[001_dikw_pyramid|데이터]] 독립성이 없다면 이 변화를 감당할 수 없지만, 무조건적인 독립성 추구 또한 [[282_performance_tactics|성능]] 병목을 가져옵니다.

**실무 의사결정 시나리오 1: 대규모 테이블 분할 시 뷰([[151_sql_view_virtual_table|View]])의 활용**
운영 중인 '주문(Order)' 테이블의 [[001_dikw_pyramid|데이터]]가 수억 건을 넘어가면서, 조회 [[282_performance_tactics|성능]]이 급격히 저하되었습니다. DBA는 이를 해결하기 위해 최근 1년 치 '최신주문'과 이전의 '과거주문' 테이블로 [[268_horizontal_fragmentation|수평 분할]]([[179_table_partitioning_concept|Partitioning]] 또는 [[243_sharding_horizontal_scaling_database|Sharding]])하기로 결정했습니다.
이때 [[369_logic_bomb|논리]]적 독립성이 없다면 이 테이블을 읽는 수천 개의 [[014_api_posix|API]] [[298_qkv_attention|쿼리]]들을 모두 수정해야 합니다. 하지만 DBA는 기존 이름과 동일한 `Order`라는 이름의 **통합 뷰([[151_sql_view_virtual_table|View]])** (예: `SELECT * FROM 최신주문 UNION ALL SELECT * FROM 과거주문`)를 [[087_process_state_transition|생성]]하여 외부/개념 사상을 갱신합니다. 결과적으로 애플리케이션 코드는 단 한 줄도 수정하지 않고 [[001_dikw_pyramid|데이터]] 파편화를 방어했습니다.

**실무 의사결정 시나리오 2: [[154_database_index_b_tree_search_optimization|인덱스]] 추가와 물리적 독립성의 함정**
검색 속도를 높이기 위해 테이블에 복합 [[154_database_index_b_tree_search_optimization|인덱스]]([[161_composite_index_leading_column|Composite Index]])를 추가했습니다. 이것은 [[009_internal_schema|내부 스키마]]의 변경이므로 응용 프로그램은 영향을 받지 않습니다(물리적 독립성 증명). 그러나 실무에서는 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 새로 생긴 [[154_database_index_b_tree_search_optimization|인덱스]]를 잘못 판단하여, 기존에 잘 타던 [[298_qkv_attention|쿼리]] [[166_execution_plan_optimizer_navigation_tree|실행 계획]]([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])이 뒤틀리면서 풀 스캔으로 돌변하는 장애가 종종 발생합니다.

```text
[물리적 독립성의 사이드 이펙트와 의사결정]
변경: DBA가 [성별] 칼럼에 비트맵 인덱스 추가
   │
   ├─> (독립성 보장) 애플리케이션 코드는 수정 필요 없음. SQL은 그대로 동작.
   │
   └─> (성능 부작용) 옵티마이저가 엉뚱한 인덱스를 타게 되어 CPU 100% 치솟음.
       => DBA 판단: 물리적 독립성은 "코드 오류를 막을 뿐, 성능 무결성을 보장하지 않는다."
       => 조치 방안: 힌트(Hint)를 통한 실행 계획 고정, 통계 정보 재수집
```
이 흐름도의 핵심은 물리적 독립성이 '문법적 에러(Syntax Error)'를 막아주지만, '[[282_performance_tactics|성능]] 회귀([[282_performance_tactics|Performance]] Regression)'까지 막아주지는 않는다는 점입니다. [[001_dikw_pyramid|데이터]] 구조가 물리적으로 변경되면 [[502_dbms|DBMS]] 엔진의 내부 계산식도 바뀌기 때문에, 실무자는 독립성이라는 우산 뒤에 숨지 말고 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 변화를 반드시 트레이싱해야 합니다.

**도입 [[435_checklist_based_testing|체크리스트]] 및 [[128_water_scrum_fall_anti_pattern|안티패턴]]**
- ✅ ([[369_logic_bomb|논리]]적 보어) 외부 시스템이나 타 부서에 [[001_dikw_pyramid|데이터]]를 제공할 때, 테이블(Table) 권한을 직접 주지 않고 반드시 뷰([[151_sql_view_virtual_table|View]])를 [[087_process_state_transition|생성]]하여 제공했는가? (향후 [[005_schema|스키마]] 변경 대비)
- ✅ (물리적 대응) 테이블 스페이스를 분리하거나 [[154_database_index_b_tree_search_optimization|인덱스]]를 재빌드한 후, [[011_system_catalog|시스템 카탈로그]]의 통계 정보를 최신화(Analyze) 하였는가?
- ❌ **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: ORM(Object-Relational [[010_schema_mapping|Mapping]]) 도구에서 `SELECT *` 형태의 암묵적 풀 스캔을 남발하는 것. 테이블 칼럼이 추가되면 불필요한 [[001_dikw_pyramid|데이터]]까지 메모리에 로드되어 네트워크 병목을 초래합니다.

📢 **섹션 요약 비유**: 뷰([[151_sql_view_virtual_table|View]])라는 방패를 세워 적의 화살([[005_schema|스키마]] 변경)은 완벽히 막아냈지만, 방패가 너무 무거워져서 병사([[282_performance_tactics|성능]])가 지쳐 쓰러지지 않도록 방패의 무게(매핑 오버헤드)를 늘 감시해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[001_dikw_pyramid|데이터]] 독립성을 원칙으로 설계된 [[002_database_definition|데이터베이스]] 시스템은 유지보수 비용을 획기적으로 낮추고 시스템의 수명을 연장합니다. 

| 비교 지표 | [[008_dependencies|종속성]] 환경 (독립성 결여) | 독립성 확보 환경 | 비즈니스 [[012_roi_return_on_investment|ROI]] |
|:---|:---|:---|:---|
| **[[005_schema|스키마]] 변경 비용** | 수십만 줄의 [[330_code_review|코드 리뷰]] 및 수정 | [[151_sql_view_virtual_table|View]] 변경 또는 [[394_catalog_metadata|카탈로그]] 갱신 | 유지보수 인건비 90% 이상 절감 |
| **운영 중단 시간** | 소스 재배포로 인한 [[090_service_kubernetes_network_load_balancing|서비스]] 다운타임 | 무중단(Online) [[020_ddl|DDL]] 작업 가능 | 24/365 [[452_availability|가용성]] 확보 및 무정지 [[090_service_kubernetes_network_load_balancing|서비스]] |
| **개발팀/[[025_dba_database_administrator|DBA]] 협업** | [[001_dikw_pyramid|데이터]]와 로직 강결합으로 갈등 심화 | 인터페이스(SQL/[[151_sql_view_virtual_table|View]]) 기반 역할 분리 | 개발 민첩성 증가 및 보안 통제력 강화 |

**미래 전망**: [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]]) 시대로 접어들면서, 단일 [[502_dbms|DBMS]] 내부의 [[001_dikw_pyramid|데이터]] 독립성을 넘어 [[090_service_kubernetes_network_load_balancing|서비스]] 간의 [[001_dikw_pyramid|데이터]] 독립성이 중요해지고 있습니다. 앞으로는 [[246_graphql_query_language_overfetching_solution|GraphQL]] 기반의 연방(Federated) [[298_qkv_attention|쿼리]] 엔진이나 [[360_data_virtualization|데이터 가상화]]([[247_data_virtualization_federated_query|Data Virtualization]]) 기술이 여러 이기종 DB들을 하나로 묶어, 전사 차원의 거대한 [[369_logic_bomb|논리]]적 독립성을 제공하는 [[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]]) 형태로 진화하고 있습니다. 

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 독립성은 스마트폰의 '[[001_operating_system_purpose|운영체제]] 업데이트'와 같습니다. 안드로이드나 iOS의 내부 심장부가 완전히 교체되어도, 우리가 즐겨 쓰던 카카오톡이나 유튜브 앱은 삭제되지 않고 여전히 잘 돌아가는 경이로운 [[344_compatibility_usability|호환성]]의 기적입니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **3단계 [[005_schema|스키마]] (3-Level [[505_schema|Schema]])** | [[001_dikw_pyramid|데이터]] 독립성을 구현하기 위해 ANSI/SPARC가 정의한 외부/개념/[[009_internal_schema|내부 스키마]] 계층 모델
- **뷰 ([[151_sql_view_virtual_table|View]])** | [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 독립성을 제공하는 가장 핵심적인 [[002_database_definition|데이터베이스]] 객체이자 가상 테이블
- **사상 ([[010_schema_mapping|Mapping]])** | [[005_schema|스키마]] 계층 간의 구조적 차이를 번역하고 매워주어 독립성을 유지하는 연결 메커니즘
- **객체 [[083_relationship_in_er_model|관계]] 매핑 (ORM)** | 응용 프로그램 단에서 [[369_logic_bomb|논리]]적 [[005_schema|스키마]]와 객체 모델 간의 차이를 극복하게 해주는 개발 프레임워크
- **[[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])** | 물리적 독립성이 유지되더라도 디스크 구조 변경 시 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 재계산해야 하는 내부 내비게이션

### 📈 관련 키워드 및 발전 흐름도

```text
[3단계 스키마 (3-Level Schema)]
    │
    ▼
[뷰 (View)]
    │
    ▼
[사상 (Mapping)]
    │
    ▼
[객체 관계 매핑 (ORM)]
    │
    ▼
[실행 계획 (Execution Plan)]
```

이 흐름도는 3단계 [[005_schema|스키마]] (3-Level [[505_schema|Schema]])에서 출발해 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[001_dikw_pyramid|데이터]] 독립성은 게임기가 아무리 새로운 모델로 바뀌어도 옛날 게임팩이 여전히 쏙 들어가서 작동하게 해주는 마법 같은 규칙이에요.
2. 겉모양 규칙([[369_logic_bomb|논리]]적 독립성)과 속부품 규칙(물리적 독립성) 두 가지가 시스템을 든든하게 지켜주죠.
3. 이 규칙 덕분에 엔지니어 아저씨들은 우리가 게임을 하는 도중에도 게임기를 더 빠르고 튼튼하게 고칠 수 있답니다!
