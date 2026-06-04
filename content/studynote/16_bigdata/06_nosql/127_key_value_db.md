+++
title = "127. 키-값 데이터베이스 (Key-Value DB) — Redis/DynamoDB/Riak"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: 키-값 DB는 [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) 구조를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경으로 확장한 가장 단순하면서 가장 빠른 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델로, O(1) 조회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 본질적 강점이다.
- **가치**: [세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/)·[캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)·장바구니처럼 단순 키로 즉시 조회해야 하는 워크로드에서 RDBMS 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 빠른 응답속도를 제공한다.
- **판단 포인트**: 복잡한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), 범위 검색) 없이 키로만 접근하는 워크로드라면 키-값 DB가 최적 선택이며, 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현이 필요하면 다른 모델로 전환해야 한다.

---

## Ⅰ. 개요 및 필요성

### 등장 배경
대규모 인터넷 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Amazon, LinkedIn 등)에서 수억 건의 사용자 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·장바구니를 실시간으로 처리하기 위한 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 저장소가 필요해졌다. RDBMS는 행 잠금(Row [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))과 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 오버헤드로 인해 이 요구를 충족시키지 못했다.

### 핵심 개념
[키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)([Key-Value Store](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/))는 고유한 키([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))와 임의의 값(Value)을 쌍으로 저장한다. 내부 구조는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)(DHT, Distributed [Hash Table](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/))로, `해시(key) -> 노드 위치`를 결정하여 O(1) 접근을 보장한다.

```text
+-------------------------------------------------+
|       키-값 데이터베이스 기본 구조                  |
+--------------------+----------------------------+
|        KEY         |          VALUE             |
+--------------------+----------------------------+
| session:user_1234  | {"name":"홍길동","cart":[]} |
| product:SKU-9900   | {"price":29900,"stock":50} |
| rate_limit:ip_x    | 142                        |
| leaderboard:score  | [sorted member list]       |
+--------------------+----------------------------+
  핵심: Key = 유일 식별자, Value = 임의 형식(바이너리 가능)
```

### 대표 솔루션 비교

| 솔루션 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 | 특징 |
|:---:|:---:|:---:|:---|
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a></strong> | 인메모리 + 지속성 | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(단일 노드) | 다양한 자료구조, Pub/Sub, 클러스터 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a></strong> | 완전 관리형 | 조정 가능(Eventual/Strong) | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), 무제한 확장, AWS 통합 |
| **Riak** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) | CRDT 지원, 고가용성 우선 |
| **Memcached** | 순수 캐시 | 없음(휘발성) | 단순·고성능 캐시, 멀티스레드 |

📢 **섹션 요약 비유**
> 키-값 DB는 거대한 물품 보관소와 같다. 보관증([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))을 내밀면 즉시 해당 물건(Value)을 꺼내준다. 어떤 물건인지 내용을 검사하거나 다른 물건과 비교하는 일은 하지 않는다 — 그것이 속도의 비결이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) (DHT, Distributed [Hash Table](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/))

```text
+----------------------------------------------------+
|           일관된 해싱 (Consistent Hashing) 링        |
|                                                    |
|              Node A (0+)                           |
|             ╱                                      |
|    Node D --●----------------●-- Node B            |
|   (270+)    |                |    (90+)            |
|             |   Hash Ring    |                     |
|             |   (0~2^32)     |                     |
|    Node C --●----------------                      |
|   (180+)                                           |
|                                                    |
|  Key "user:123" -> hash(key) -> 위치 -> Node B 담당    |
|  노드 추가/제거 시 일부 키만 재배치 (최소 이동)          |
+----------------------------------------------------+
```

### 핵심 연산

| 연산 | 복잡도 | 설명 |
|:---:|:---:|:---|
| `GET key` | O(1) | 키로 값 조회 |
| `SET key value` | O(1) | 키-값 저장 또는 갱신 |
| `DEL key` | O(1) | 키 삭제 |
| `EXPIRE key ttl` | O(1) | [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)([Time To Live](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| `SCAN pattern` | O(N) | 패턴 기반 키 탐색 (비권장) |

### [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 구조

```text
+------------------------------------------------------+
|              DynamoDB 내부 구조                        |
|                                                      |
|  테이블 (Table)                                       |
|  +-----------------------------------------------+   |
|  |  PK(파티션 키) + SK(정렬 키, 선택)              |   |
|  |                                               |   |
|  |  hash(PK) -> Partition 1, 2, 3 ...             |   |
|  |                                               |   |
|  |  Partition 1   Partition 2   Partition 3      |   |
|  |  [item A]      [item D]      [item G]          |   |
|  |  [item B]      [item E]      [item H]          |   |
|  |  [item C]      [item F]      [item I]          |   |
|  +-----------------------------------------------+   |
|                                                      |
|  * 파티션 키 카디널리티(Cardinality)가 낮으면 핫 파티션 위험|
+------------------------------------------------------+
```

📢 **섹션 요약 비유**
> [일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) 링은 원형 시계판과 같다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 시침처럼 시계 방향으로 가장 가까운 노드에 저장된다. 노드가 추가되면 그 사이 구간의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 이사하면 되어, 전체 재배치라는 대혼란을 피할 수 있다.

---

## Ⅲ. 비교 및 연결

### 키-값 DB vs 다른 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델

| 관점 | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value DB | [Document DB](/knowledge-base/studynote/16_bigdata/06_nosql/129_document_db/) | Column-Family DB |
|:---:|:---:|:---:|:---:|
| **조회 방법** | 키만 가능 | 키 + 필드 필터 | 키 + 컬럼 범위 |
| **값 구조** | 불투명(Opaque) | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON 구조화 | 컬럼 그룹 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 표현력</strong> | 최소 | 중간 | 중간 |
| **조회 속도** | ★★★★★ | ★★★★ | ★★★★ |
| **적합 용도** | 캐시·[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | CMS·프로필 | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·시계열 |

### Riak의 CRDT (Conflict-free Replicated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Type)
멀티 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 환경에서 충돌 없는 병합을 보장하는 수학적 자료구조.

| CRDT 유형 | 설명 | 예시 |
|:---:|:---:|:---|
| G-[Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 증가만 가능한 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 뷰 집계 |
| PN-[Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 증가/감소 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 재고 수량 |
| OR-Set | 충돌 없는 집합 | 태그 목록 |
| LWW-[Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) | 최신 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 우선 | 사용자 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |

📢 **섹션 요약 비유**
> [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) DB가 내용을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있는 투명 상자라면, [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value DB는 겉에 번호만 붙은 불투명 금고다. 안을 열어보지 않아도 되기에 가장 빠르지만, "빨간 물건만 꺼내줘"라는 요청은 처리할 수 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적합한 워크로드 패턴

| 패턴 | 예시 | 추천 솔루션 |
|:---:|:---:|:---:|
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a> 저장</strong> | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), [JWT](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) 블랙리스트 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) ([TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 활용) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a> 레이어</strong> | DB 조회 결과 캐시 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) / Memcached |
| **실시간 리더보드** | 게임 점수 순위표 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sorted Set |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a> <a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/">OLTP</a></strong> | 전자상거래 주문 | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/">피처 플래그</a></strong> | A/B 테스트 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Hash |

### 기술사 시험 핵심 판단 포인트

```text
Q. 키-값 DB 선택 기준은?

       복잡한 쿼리 필요?
            |
      YES --+-- NO
      |          |
 Document/   단순 키 조회
 Column DB        |
            낮은 지연 필요?
                 |
           YES --+-- NO (지속성 중요)
           |              |
         Redis         DynamoDB
     (인메모리)        (영구 저장)
```

📢 **섹션 요약 비유**
> 기술사 판단은 요리사가 식재료를 고르는 것과 같다. 빨리 볶아야 하면 이미 손질된 재료([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/))를, 천천히 숙성이 필요하면 냉장 보관 가능한 재료([DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/))를 고른다. 용도에 맞지 않는 재료를 쓰면 맛있는 요리가 나오지 않는다.

---

## Ⅴ. 기대효과 및 결론

### 도입 효과 수치화

| 지표 | RDBMS | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value DB | 개선율 |
|:---:|:---:|:---:|:---:|
| 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(p99) | 50~200ms | 0.1~1ms | 50~200배 향상 |
| 초당 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(TPS) | 수천 | 수십만~수백만 | 100배+ |
| 수평 확장 | 어려움 | 용이([샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)) | — |
| 비용(대규모) | 높음 | 낮음 | 60~80% 절감 |

### 결론 및 아키텍처 권고
키-값 DB는 단독 사용보다 <strong>RDBMS + 키-값 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a> 레이어</strong>의 조합으로 가장 큰 효과를 발휘한다. [캐시 히트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/)율(Cache [Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) Rate) 90% 이상을 목표로 설계하면 DB 부하를 획기적으로 줄일 수 있다. DynamoDB를 중심으로 한 [서버리스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/215_serverless_architecture_faas_aws_lambda/)는 관리 오버헤드 없이 무제한 확장이 필요한 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에 최적이다.

📢 **섹션 요약 비유**
> 키-값 DB는 도로 위의 고속도로 휴게소 자판기와 같다. 버튼([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))만 누르면 음료(Value)가 나오는 단순함 덕분에 줄을 서지 않아도 된다. 하지만 "오늘의 특선 메뉴"처럼 복잡한 조합은 제공하지 못한다 — 그 역할은 레스토랑(RDBMS)의 몫이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | 이론적 기반 | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택(Riak), [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 클러스터) |
| [일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) | 구현 메커니즘 | 노드 추가 시 최소 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 |
| [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) ([Time To Live](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)) | 기능 | 만료 시간 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 캐시 갱신 |
| CRDT | 충돌 해결 | 자동 병합 가능한 자료구조 |
| [Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/) | 아키텍처 패턴 | DB 혼합 사용 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[CAP 정리 (CAP Theorem)]
    |
    v
[일관된 해싱 (Consistent Hashing)]
    |
    v
[TTL (Time To Live)]
    |
    v
[CRDT (Conflict-free Replicated Data Type)]
    |
    v
[Polyglot Persistence]
```

이 흐름도는 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))에서 출발해 Polyglot Persistence까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 키-값 DB는 학교 사물함과 같아요. 번호([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 알면 즉시 내 물건(Value)을 꺼낼 수 있어요.
2. 사물함 번호를 모르면 전체를 다 열어봐야 해서 시간이 오래 걸려요 — 그래서 "키"가 매우 중요해요.
3. Redis는 책상 위에 놓인 사물함(빠르지만 전기가 끊기면 잊어버림), DynamoDB는 학교 창고 사물함(느리지만 절대 잊어버리지 않음)이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 262

<- **이전**: [PACELC 정리 (PACELC Theorem)](/knowledge-base/studynote/16_bigdata/06_nosql/126_pacelc_theorem_extended_cap/)
**다음**: [128. Redis (Remote Dictionary Server) — 인메모리 데이터 구조 서버](/knowledge-base/studynote/16_bigdata/06_nosql/128_redis/) ->

---
