---
title: 3. 데이터베이스 관리 시스템 (DBMS) - 사용자와 DB 사이의 인터페이스 (데이터 독립성 제공)
date: '2024-05-20'
description: 사용자와 데이터베이스 간의 인터페이스 역할을 수행하며 데이터 독립성을 제공하는 DBMS의 아키텍처 및 내부 원리
tags:
- database
---

# 03. [[002_database_definition|데이터베이스]] 관리 시스템 ([[502_dbms|DBMS]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[502_dbms|DBMS]]([[501_database|Database]] [[372_management|Management]] System)는 응용 프로그램과 물리적 [[002_database_definition|데이터베이스]] 사이의 [[273_mediator_pattern|중재자]]로서, [[001_dikw_pyramid|데이터]]의 [[087_process_state_transition|생성]], 조회, 수정, 제어를 관리하는 복합 시스템 소프트웨어입니다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]의 [[008_dependencies|종속성]]과 중복성을 획기적으로 해결하고, 다중 사용자의 동시 접근([[266_other_transparency|Concurrency]])과 장애 발생 시의 [[658_ir_recovery|복구]]([[658_ir_recovery|Recovery]])를 보장하여 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 지킵니다.
> 3. **융합**: [[001_operating_system_purpose|운영체제]](OS)의 [[022_kernel_role|커널]]과 유사한 [[208_schedule_history_transaction_execution_order|스케줄]]링 및 버퍼 관리 기능을 내재화하고 있으며, 최근에는 [[136_variance|분산]] 컴퓨팅 엔진과 결합하여 대규모 수평 확장성을 지원합니다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[002_database_definition|데이터베이스]] 관리 시스템 ([[502_dbms|DBMS]])은 사용자와 [[002_database_definition|데이터베이스]]를 연결해주는 핵심 시스템 소프트웨어입니다. [[002_database_definition|데이터베이스]]가 단순한 [[001_dikw_pyramid|데이터]]의 집합이라면, DBMS는 그 [[001_dikw_pyramid|데이터]]를 살아 숨 쉬게 하고 통제하는 "엔진" 역할을 합니다.

과거 종속적인 [[501_file_definition_logical_record|파일]] 처리([[501_file_definition_logical_record|File]] Processing) 시스템에서는 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]의 물리적 구조가 바뀌면, 이를 [[316_reference_pattern_nosql|참조]]하는 모든 애플리케이션의 코드를 전면 수정해야 하는 심각한 **[[001_dikw_pyramid|데이터]] [[008_dependencies|종속성]]([[001_dikw_pyramid|Data]] Dependency)** 문제가 있었습니다. 또한 여러 애플리케이션이 동일한 [[001_dikw_pyramid|데이터]]를 각자 보관함에 따라 생기는 **[[001_dikw_pyramid|데이터]] 중복성([[001_dikw_pyramid|Data]] Redundancy)** 은 저장 공간의 낭비를 넘어 [[194_consistency_database_integrity|일관성]]을 훼손하는 치명적 약점이었습니다.

이러한 문제를 극복하기 위해 [[001_dikw_pyramid|데이터]]를 애플리케이션 로직에서 완전히 분리해내는 "[[198_abstraction_control_data_process|추상화]] 레이어"가 절실히 요구되었고, 이를 실현한 것이 바로 DBMS입니다.

```text
[과거: 종속성과 중복성의 늪]
App A (C언어) ───[종속]──> Employee.dat (고정길이 텍스트) ──┐
App B (Java)  ───[종속]──> Employee.bin (바이너리 포맷)   ──┴── 데이터 중복 & 불일치!

[현재: DBMS를 통한 추상화와 독립성]
App A (C언어) ───[SQL]──┐
                        ▼
               ┌─────────────────┐
App B (Java)  ─┼─> DBMS Engine   ├─> DB (통합된 Employee 테이블)
               └─────────────────┘
                        ▲
App C (Python) ─[SQL]───┘
```
이 도식의 핵심은 DBMS가 도입되면서 애플리케이션이 [[501_file_definition_logical_record|파일]]의 물리적 포맷이나 경로를 알 필요가 완전히 사라졌다는 점입니다. 오직 표준화된 질의어(SQL)를 DBMS에 던지기만 하면, DBMS가 내부적으로 최적의 경로를 찾아 I/O를 수행합니다. 이로 인해 개발 생산성은 극적으로 향상되고, [[001_dikw_pyramid|데이터]] 구조가 확장되거나 변경되어도 애플리케이션은 영향을 받지 않습니다. 실무에서는 이 구조 덕분에 무중단 [[005_schema|스키마]] 마이그레이션이 가능해지며, DB 스토리지 계층을 클라우드로 변경해도 애플리케이션은 동일하게 작동합니다.

📢 **섹션 요약 비유**: 각자 요리사가 식재료 산지에 가서 직접 재료를 캐고 손질하던 방식에서, 주방 중앙에 거대한 식자재 창고(DB)와 이를 전담하는 창고장([[502_dbms|DBMS]])을 두어 요리사들은 "양파 2개"라고 주문만 하면 되도록 자동화한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

DBMS는 단일 프로그램이 아니라 수많은 [[192_module_independence|모듈]]이 유기적으로 결합된 방대한 아키텍처를 가집니다. 일반적으로 질의 처리기(Query Processor), [[191_transaction_concept_states|트랜잭션]] 관리자([[191_transaction_concept_states|Transaction]] Manager), 저장소 관리자(Storage Manager) 등으로 구분됩니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|
| **파서 / 컴파일러** | SQL 문법 [[395_verification_process_review|검증]] 및 변환 | SQL 구문을 파싱 트리(Parse Tree)로 변환하고 [[394_catalog_metadata|카탈로그]] [[316_reference_pattern_nosql|참조]] | 통역사 및 문법 교정기 |
| **[[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]])** | 최적의 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 수립 | [[154_database_index_b_tree_search_optimization|인덱스]]와 통계 정보를 바탕으로 최소 비용(Cost) 경로 계산 (CBO) | 차량 내비게이션 (최단 경로) |
| **[[191_transaction_concept_states|트랜잭션]] 매니저** | ACID 특성 보장 | [[014_concurrency|동시성]] 제어([[213_locking_mechanism_concurrency_control|Locking]]), 교착상태 탐지 및 [[568_logs_distributed_logging_elk_fluentd|로그]] 기록 지시 | 은행의 깐깐한 [[606_auditing_linux_auditd|감사]]관 |
| **버퍼 관리자** | 메모리 버퍼 최적화 | 디스크 접근을 최소화하기 위해 [[262_lru_page_replacement|LRU]]/[[045_clock|Clock]] 등의 [[260_page_replacement|페이지 교체]] 수행 | 도서관의 자주 찾는 책꽂이 |
| **저장소 엔진** | 물리적 I/O 처리 | 디스크 상의 [[286_page_frame|페이지]]나 블록 단위로 [[001_dikw_pyramid|데이터]]를 읽고 [[289_cqrs_db|쓰기]] 수행 | 창고의 화물 지게차 |

DBMS가 사용자의 질의를 받아 [[001_dikw_pyramid|데이터]]를 반환하기까지의 내부 흐름 [[123_pipe|파이프]]라인은 아래와 같이 동작합니다.

```text
[Client Request: SELECT * FROM Users WHERE id = 1]
        │
        ▼
┌────── Query Processor Layer ──────┐
│  1. Parser (구문 분석 및 파스 트리)│
│               ↓                   │
│  2. Optimizer (실행 계획 Cost계산) │ ◁── 통계 정보 (Statistics) 참조
│               ↓                   │
│  3. Execution Engine (플랜 실행)   │
└───────────────┬───────────────────┘
                │ Page Request (id=1 데이터가 있는 블록 요청)
                ▼
┌────── Storage Manager Layer ──────┐
│  4. Transaction/Lock Manager      │ ◁── 락 충돌 검사 (S-Lock 획득)
│               ↓                   │
│  5. Buffer Manager (Memory Pool)  │ ◁── 캐시 히트 검사 (있으면 즉시 반환)
│               ↓                   │ (Miss 시 디스크 I/O)
│  6. Disk I/O & Recovery Manager   │
└───────────────┬───────────────────┘
                ▼
      [ Physical Data Files ]
```
이 흐름도의 핵심은 [[298_qkv_attention|쿼리]] 처리가 '비용 계산([[088_optimizer|Optimizer]])'과 '상태 제어([[510_lock|Lock]]/Buffer)'라는 두 가지 주요 관문을 거친다는 것입니다. [[298_qkv_attention|쿼리]]가 아무리 단순해도, [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 통계 정보를 바탕으로 잘못된 플랜(예: Full Table Scan)을 짜면 시스템은 순식간에 병목에 빠집니다. 또한 버퍼 매니저에서 캐시 미스가 다수 발생하면 느린 물리적 디스크 I/O가 큐에 쌓이면서 전체 응답 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])이 기하급수적으로 증가합니다. 실무에서는 이 [[123_pipe|파이프]]라인 상의 어느 지점에서 [[015_지연_데이터_관점|지연]]이 발생하는지([[510_lock|Lock]] 대기인지, Disk I/O 대기인지)를 정확히 추적하는 것이 [[282_performance_tactics|성능]] 튜닝의 출발점입니다.

이러한 복잡한 처리를 위해 DBMS는 백그라운드 프로세스(예: Oracle의 DBWn, LGWR, PMON 등)를 상시 구동하여 시스템 상태를 지속적으로 [[229_monitor|모니터]]링하고 조정합니다.

📢 **섹션 요약 비유**: 식당에서 손님이 주문(SQL)을 하면, 매니저([[163_optimizer_sql_execution_plan_generator|옵티마이저]])가 가장 빠른 조리 순서를 정하고, 주방장(실행 엔진)이 냉장고 관리자(버퍼 매니저)에게 재료를 요청하여 요리를 완성하는 체계적인 주방 시스템과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

현대의 DBMS는 크게 [[083_relationship_in_er_model|관계]]형(RDBMS)과 NoSQL로 나뉘며, 최근에는 이 둘의 장점을 융합한 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 모델이 대두되고 있습니다. DBMS의 내부 엔진 관점에서 이들을 비교하면 아키텍처적 차이가 극명하게 드러납니다.

| 분석 항목 | [[083_relationship_in_er_model|관계]]형 [[502_dbms|DBMS]] ([[188_pl_sql_t_sql_procedural|Oracle]], MySQL) | [[035_nosql|NoSQL]] [[502_dbms|DBMS]] ([[540_mongodb|MongoDB]], [[541_cassandra|Cassandra]]) | [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] (Spanner, [[292_etl_process|CockroachDB]]) |
|:---|:---|:---|:---|
| **스토리지 포맷** | 행 기반 (Row-based), [[064_b_tree|B-Tree]] 위주 | 문서([[343_json|JSON]]) 또는 컬럼 패밀리([[377_lsm_tree_storage_engine|LSM-Tree]]) | 혼합 또는 스토리지 [[136_variance|분산]] [[016_replication_factor|복제]] |
| **확장성 구조** | 수직적 확장 ([[621_scale_up_system_bus|Scale-Up]] 중심) | 수평적 확장 ([[202_scale_out_distributed_horizontal_expansion|Scale-Out]] 최적화) | 수평적 확장 + ACID 완벽 보장 |
| **[[191_transaction_concept_states|트랜잭션]] (ACID)** | 완벽 보장 (단일 노드 강점) | 부분 보장 (BASE 특성, [[194_consistency_database_integrity|일관성]] 양보) | 글로벌 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 보장 |
| **[[005_schema|스키마]] 유연성** | 엄격함 ([[010_schema_on_write|Schema-on-Write]]) | 유연함 ([[009_schema_on_read|Schema-on-Read]], Schemaless) | 엄격한 릴레이셔널 뷰 제공 |

RDBMS와 NoSQL의 I/O 특성 및 트레이드오프를 결정하는 자료구조적 차이는 다음과 같습니다.

```text
[RDBMS: B+Tree 구조의 업데이트 병목]
        [ Root ]
       /        \
   [ Node ]   [ Node ]   => (단점) 잦은 쓰기 작업(Insert/Update) 시 트리 스플릿(Split) 발생.
     / \        / \           오버헤드가 커 쓰기(Write) 위주의 대용량 트래픽에 불리.
 [Data] [Data] [Data] ...

[NoSQL: LSM-Tree 구조의 쓰기 최적화]
   (Memory) [ MemTable ] ── 가득 차면 ──> 디스크로 순차 기록 (Flush)
                                             │
   (Disk)   [ SSTable 1 ] [ SSTable 2 ] <────┘
            => (장점) 쓰기 요청을 메모리에만 남기고 순차 파일 기록하므로 초고속 쓰기 가능.
               (단점) 읽기 시 여러 SSTable을 뒤져야 해서 읽기(Read) 성능 페널티 존재.
```
이 구조도의 핵심은 저장소 엔진이 채택한 인덱싱 [[001_algorithm_definition|알고리즘]]이 해당 DBMS의 성격을 근본적으로 결정한다는 점입니다. RDBMS는 B+Tree를 통해 '빠르고 안정적인 임의 읽기/[[289_cqrs_db|쓰기]]'를 보장하지만 [[275_lock_contention_monitoring|락 경합]]과 트리 재구성 비용이 높습니다. 반면 NoSQL의 상당수가 채택하는 [[377_lsm_tree_storage_engine|LSM-Tree]]([[221_lsm_tree_memtable_sequential_flush_compaction|Log-Structured Merge-Tree]])는 '압도적인 [[289_cqrs_db|쓰기]] [[139_throughput|처리량]]'을 보장하지만 [[347_compaction|압축]]([[347_compaction|Compaction]]) 작업 시 CPU [[129_spike_agile_technical_investigation|스파이크]]가 발생할 수 있습니다. 실무에서는 트래픽의 Read/Write 비율에 따라 엔진을 선택해야 합니다.

📢 **섹션 요약 비유**: RDBMS가 모든 책이 십진분류법에 따라 빽빽하게 꽂힌 도서관(찾기 쉬우나 책 꽂기 힘듦)이라면, NoSQL은 새로 들어오는 책을 빈 바구니에 무조건 던져놓고 나중에 한 번에 정리하는 방식(꽂기 편하나 찾을 때 오래 걸림)입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 DBMS를 도입하고 운영할 때 가장 중요한 것은 시스템의 한계를 이해하고 장애를 선제적으로 방어하는 의사결정입니다. 아무리 뛰어난 DBMS도 잘못된 설계와 [[298_qkv_attention|쿼리]] 앞에서는 무력해집니다.

**실무 의사결정 시나리오 1: 데드락([[281_deadlock_definition|Deadlock]])과 [[154_database_index_b_tree_search_optimization|인덱스]] 부재 상황**
개발자가 테스트 환경에서는 문제없이 작동하던 애플리케이션을 운영에 배포하자마자 전체 시스템이 멈추는 장애가 발생했습니다. 원인은 특정 테이블에 [[154_database_index_b_tree_search_optimization|인덱스]]가 없어 DBMS가 Table Full Scan을 수행하면서 광범위한 행(Row)에 락([[510_lock|Lock]])을 걸어버렸기 때문입니다. 실무에서는 [[502_dbms|DBMS]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 효율적으로 일할 수 있도록 핵심 WHERE 절에 [[154_database_index_b_tree_search_optimization|인덱스]]를 부여하고, [[191_transaction_concept_states|트랜잭션]]을 최대한 짧게 유지하는 것이 생존의 기본 원칙입니다.

**실무 의사결정 시나리오 2: Connection Pool 고갈 (Thundering Herd)**
갑작스러운 트래픽 폭주 시 애플리케이션이 DBMS로 동시에 너무 많은 커넥션을 요청하여 [[502_dbms|DBMS]] 프로세스가 [[034_context_switch|컨텍스트 스위칭]] 오버헤드로 다운되는 상황입니다. DBMS는 CPU 코어 수와 메모리에 비례하여 처리할 수 있는 동시 [[160_session_controlling_terminal|세션]] 수가 정해져 있습니다. 따라서 애플리케이션 앞단에 커넥션 풀(HikariCP 등)을 반드시 [[009_config|설정]]하여 DBMS로 향하는 부하를 유량 제어하고 대기시켜야 합니다.

```text
[DBMS 장애 전파와 방어 아키텍처]
(위험) App A, B, C (각각 1000개 요청) ───> [ DBMS ] (Connection 3000개 폭주 -> 다운)

(안전) App A, B, C ──> [ Connection Pool (Max 100 제한) ] ──> [ DBMS ] (안정적 처리)
                             ↳ 101번째 요청은 대기(Wait) -> App 레벨에서 타임아웃 처리
```
이 도식은 부하가 발생했을 때 DBMS를 죽일 것인가, 애플리케이션에서 요청을 튕겨낼(Fail-fast) 것인가를 결정하는 장애 격리([[195_isolation_concurrency_control|Isolation]])의 핵심을 보여줍니다. 실무에서는 DBMS가 인프라의 가장 깊은 곳에 있는 최종 보루이므로 절대 죽어서는 안 됩니다. 따라서 커넥션 풀을 통한 유량 제어와 [[298_qkv_attention|쿼리]] [[573_timeout_retry_backoff_strategy|타임아웃]](Query [[319_timeout_prevention|Timeout]]) [[009_config|설정]]은 선택이 아닌 필수입니다.

**[[502_dbms|DBMS]] 운영 [[435_checklist_based_testing|체크리스트]]**
- ✅ Slow Query Log를 활성화하여 풀 스캔을 유발하는 악성 [[298_qkv_attention|쿼리]]를 주기적으로 색출하고 있는가?
- ✅ 버퍼 [[263_cache_hit_miss|캐시 히트]]율([[536_buffer_cache_page_cache|Buffer Cache]] [[359_effective_access_time|Hit Ratio]])이 90% 이상 유지되고 있으며, 부족 시 스케일업을 고려했는가?
- ❌ **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: "모든 비즈니스 로직을 [[186_stored_procedure_trigger|스토어드 프로시저]](Procedure)에 몰아넣기." 이는 애플리케이션 확장을 막고 DBMS의 CPU를 고갈시켜, 비싼 [[502_dbms|DBMS]] 라이선스 비용 증가와 시스템 경직성을 초래합니다.

📢 **섹션 요약 비유**: DBMS는 댐(Dam)의 수문장과 같아서, 물이 한꺼번에 쏟아질 때 적절히 수문을 조절(커넥션 풀)하지 않으면 댐 전체가 무너져 마을([[090_service_kubernetes_network_load_balancing|서비스]])이 물에 잠기게 됩니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

조직이 적절한 DBMS를 도입하고 고도화하면 비즈니스 [[196_durability_permanent_storage|영속성]]과 기민성이라는 두 마리 토끼를 잡을 수 있습니다.

| 정량적/정성적 지표 | [[502_dbms|DBMS]] 최적화 전 | [[502_dbms|DBMS]] 최적화 및 튜닝 후 | 효과 |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 비율** | 애플리케이션 버그 시 손상 | 100% (ACID 보장) | [[001_dikw_pyramid|데이터]] 정합성 보장을 통한 고객 [[085_confidence_association_rule_conditional_probability|신뢰도]] 확보 |
| **개발 및 배포 주기** | [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]] 포맷 의존 | [[005_schema|스키마]]-앱 분리로 짧아짐 | 비즈니스 요구사항에 대한 민첩한([[004_agile_relation|Agile]]) 대응 |
| **[[658_ir_recovery|복구]] 목표 시간([[176_rto_recovery_time_objective|RTO]])** | 수작업 [[501_file_definition_logical_record|파일]] 복원 (수 시간) | [[234_redo_roll_forward_durability_recovery|Redo]]/[[393_undo|Undo]] [[568_logs_distributed_logging_elk_fluentd|로그]] 복원 (수 분) | 치명적 장애 발생 시 신속한 [[090_service_kubernetes_network_load_balancing|서비스]] 정상화 |

**미래 전망**: DBMS는 단순히 [[001_dikw_pyramid|데이터]]를 저장하고 반환하는 소프트웨어를 넘어, AI를 통해 스스로 [[154_database_index_b_tree_search_optimization|인덱스]]를 [[087_process_state_transition|생성]]하고 튜닝하는 '자율 운영 [[002_database_definition|데이터베이스]](Autonomous [[501_database|Database]])'로 발전하고 있습니다. 또한 클라우드 환경에서는 사용량에 따라 스토리지가 무한대급으로 늘어나는 [[206_serverless_cold_start|Serverless]] DBMS와 컴퓨팅/스토리지 노드를 완벽히 분리한 아키텍처가 새로운 표준(Standard)으로 자리 잡고 있습니다.

📢 **섹션 요약 비유**: 엔진이 없는 마차에서 V8 엔진을 단 자동차로 넘어온 것이 과거의 발전이라면, 미래의 DBMS는 도로 상황을 스스로 파악해 기어를 변속하는 자율주행 자동차 엔진과 같이 진화하고 있습니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[004_data_independence|데이터 독립성]] ([[504_data_independence|Data Independence]])** | DBMS가 도입됨으로써 얻게 되는 가장 큰 이점으로, [[369_logic_bomb|논리]]적 구조와 물리적 구조를 분리
- **[[298_qkv_attention|쿼리]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (Query [[088_optimizer|Optimizer]])** | 입력된 SQL을 가장 빠르고 저렴하게 실행할 수 있는 플랜을 세우는 DBMS의 두뇌
- **[[191_transaction_concept_states|트랜잭션]] ([[191_transaction_concept_states|Transaction]])** | [[002_database_definition|데이터베이스]] 상태를 변화시키는 [[369_logic_bomb|논리]]적 작업의 최소 단위로 DBMS가 ACID를 통해 [[003_integrity|무결성]]을 제어
- **버퍼 풀 (Buffer Pool)** | I/O 병목을 제거하기 위해 디스크의 [[001_dikw_pyramid|데이터]]를 메모리에 [[456_caching|캐싱]]해두는 공간
- **[[186_stored_procedure_trigger|스토어드 프로시저]] ([[186_stored_procedure_trigger|Stored Procedure]])** | [[502_dbms|DBMS]] 서버 내에 컴파일되어 저장된 프로그래밍 블록으로, [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]을 줄이는 실행 방식

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 독립성 (Data Independence)]
    │
    ▼
[쿼리 옵티마이저 (Query Optimizer)]
    │
    ▼
[트랜잭션 (Transaction)]
    │
    ▼
[버퍼 풀 (Buffer Pool)]
    │
    ▼
[스토어드 프로시저 (Stored Procedure)]
```

이 흐름도는 [[004_data_independence|데이터 독립성]] ([[504_data_independence|Data Independence]])에서 출발해 [[186_stored_procedure_trigger|스토어드 프로시저]] ([[186_stored_procedure_trigger|Stored Procedure]])까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[002_database_definition|데이터베이스]]가 책들이 잔뜩 있는 도서관이라면, DBMS는 그 도서관에서 일하는 아주 똑똑한 '사서 선생님'이에요.
2. 우리가 "우주에 관한 책 찾아주세요"라고 말하면, 사서 선생님이 가장 빠른 길로 가서 책을 꺼내다 주죠.
3. 책이 찢어지지 않게 [[571_protection_vs_security|보호]]하고, 다른 사람이 볼 때는 순서를 정해주는 것도 모두 사서 선생님([[502_dbms|DBMS]])이 하는 아주 중요한 일이랍니다.
