+++
title = "236. 키-값 저장소 (Key-Value Store) - Redis / DynamoDB"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)([Key-Value Store](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/))는 고유한 키([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))로 값(Value)을 O(1) 시간에 조회하는 가장 단순한 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 구조로, <strong>밀리초 이하 응답 속도</strong>가 핵심 가치다.
> 2. **가치**: Redis는 인메모리 기반으로 문자열·해시·리스트·셋·정렬셋 등 <strong>풍부한 자료구조</strong>를 제공해 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·캐시·리더보드에, DynamoDB는 완전관리형 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)로 <strong>무한 확장</strong>에 적합하다.
> 3. **판단 포인트**: Redis는 단일 서버 메모리 용량이 한계이므로 대용량 영구 저장은 DynamoDB가 적합하고, 두 시스템을 <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a> DAX(캐시) + <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a>(영구)</strong>처럼 조합하는 패턴이 일반적이다.

---

## Ⅰ. 개요 및 필요성

웹 서비스에서 DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 병목은 만성적 문제다. 매 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 요청마다 복잡한 SQL을 실행하면 응답이 수백ms~수초로 늘어난다. [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)는 이 병목을 해결하는 첫 번째 방어선이다.

```
[캐시 패턴 - Cache Aside]
1. 앱 → Redis 조회 (Cache Hit: 1ms 응답)
        ↓ Cache Miss
2. 앱 → DB 조회 (100ms 응답)
3. 앱 → Redis 저장 (TTL 설정)
4. 다음 요청 → Redis 캐시 Hit (1ms 응답)

효과: DB 부하 90%+ 감소, 응답 속도 100배 향상
```

<strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/">키-값 저장소</a> 주요 사용 사례:</strong>
- <strong><a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/">세션 관리</a></strong>: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 사용자 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 토큰 저장 ([TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 자동 만료)
- **캐시**: DB/[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) (Cache Aside, [Write-Through](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/))
- **실시간 리더보드**: 게임 점수 랭킹 ([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) ZSet)
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 락</strong>: [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 (Redlock [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))
- <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a></strong>: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청 속도 제한 (Sliding Window)
- **Pub/Sub**: 경량 실시간 메시지 발행/구독

📢 **섹션 요약 비유**: [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)는 열쇠고리다. 각 열쇠(키)에 방(값)이 매핑되어 있어, 열쇠만 있으면 즉시 방을 열 수 있다. 열쇠가 없으면 방 목록 전체를 뒤져야(DB 풀스캔) 하지만, 열쇠고리는 O(1)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 자료구조 및 활용 패턴

```
[Redis 5가지 핵심 자료구조]
┌────────────┬───────────────────────────────────────────────┐
│ String     │ SET/GET, INCR/DECR, EXPIRE (TTL)              │
│            │ 사례: 세션 토큰, 카운터, 분산 락               │
├────────────┼───────────────────────────────────────────────┤
│ Hash       │ HSET/HGET, HMGET, HGETALL                     │
│            │ 사례: 사용자 프로필, 상품 정보                  │
├────────────┼───────────────────────────────────────────────┤
│ List       │ LPUSH/RPUSH, LPOP/RPOP, LRANGE                │
│            │ 사례: 메시지 큐, 최근 방문 기록                 │
├────────────┼───────────────────────────────────────────────┤
│ Set        │ SADD/SMEMBERS, SUNION, SINTER                 │
│            │ 사례: 유니크 방문자, 태그 교집합                │
├────────────┼───────────────────────────────────────────────┤
│ Sorted Set │ ZADD/ZRANGE, ZREVRANGEBYSCORE                 │
│  (ZSet)    │ 사례: 실시간 점수 랭킹, 시간 순 이벤트          │
└────────────┴───────────────────────────────────────────────┘
```

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 옵션

| 옵션 | 설명 | 특성 |
|:---|:---|:---|
| <strong>RDB (<a href="/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/">Snapshot</a>)</strong> | 주기적 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장 | 빠른 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 마지막 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 이후 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 |
| <strong>AOF (Append Only <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a>)</strong> | 모든 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 명령 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기록 | 높은 내구성, 디스크 비용 ↑ |
| **RDB + AOF 혼합** | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) + 이후 AOF | 균형 잡힌 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **No Persistence** | 메모리만 (순수 캐시) | 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 재시작 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제 |

### [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 아키텍처

```
[DynamoDB 핵심 개념]
테이블: users
┌────────────────────────────────────────────────────────┐
│ Partition Key (PK): user_id  (해시 키)                  │
│ Sort Key (SK): created_at    (선택적 범위 키)            │
├────────────────────────────────────────────────────────┤
│ {PK:"U001", SK:"2024-01-01", name:"김철수", tier:"VIP"} │
│ {PK:"U001", SK:"2024-01-15", name:"김철수", tier:"VIP"} │
│ {PK:"U002", SK:"2024-01-10", name:"이영희", tier:"일반"} │
└────────────────────────────────────────────────────────┘

PK 기반 조회: O(1) 해시 조회
SK 기반 범위: PK 고정 + SK 범위 쿼리
GSI (Global Secondary Index): 다른 속성으로 추가 인덱스
```

### [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) DAX (가속 캐시)

```
앱 → DAX (인메모리, 마이크로초 응답)
       ↓ Cache Miss
     DynamoDB (밀리초 응답)

DAX: DynamoDB용 인메모리 캐시 클러스터
     Redis와 유사하지만 DynamoDB API와 완전 호환
     코드 변경 없이 URL만 DAX로 변경
```

📢 **섹션 요약 비유**: DynamoDB의 PK와 SK는 주민등록 시스템이다. 주민번호(PK)로 사람을 찾고, 사건 날짜(SK)로 특정 기간 기록만 조회한다. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없이 다른 속성으로 찾으면 전수조사(Full Scan) 해야 한다.

---

## Ⅲ. 비교 및 연결

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) vs [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 비교

| 비교 항목 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) | Amazon [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) |
|:---|:---|:---|
| **스토리지 유형** | 인메모리 (+ 디스크 영속) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) |
| **응답 속도** | 마이크로초~밀리초 | 밀리초 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기</strong> | 수십GB ~ 수TB | 무제한 |
| **비용** | 메모리 비용 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)/스토리지 과금 |
| **자료구조** | 풍부 (Hash, ZSet, List…) | 단순 (Item 기반) |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a></strong> | 제한적 (MULTI/EXEC) | ACID (같은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) |
| **관리** | 직접 관리 or [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cloud | 완전 관리형 ([서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) |
| **적합 사례** | 캐시, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 리더보드 | 대규모 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 앱, 완전 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) |

### 캐시 패턴 비교

| 패턴 | 설명 | 특성 |
|:---|:---|:---|
| <strong>Cache Aside (<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a>)</strong> | 캐시 미스 시 앱이 DB 조회 후 캐시 저장 | 가장 일반적 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/">Write-Through</a></strong> | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시 캐시+DB 동시 저장 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ↑, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ↑ |
| **Write-Behind** | 캐시 먼저 쓰고 비동기로 DB 저장 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) ↑, 손실 위험 |
| **Read-Through** | 캐시가 DB 조회를 대행 | 캐시 계층 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |

📢 **섹션 요약 비유**: Cache Aside는 편의점이 없으면 대형마트에서 가져오는 것, Write-Through는 편의점 납품할 때 창고에도 동시에 넣는 것, Write-Behind는 편의점에만 먼저 넣고 나중에 창고 정리하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 실무 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)

```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# String: 세션 저장 (TTL 1시간)
r.setex('session:tok123', 3600, '{"user_id": "U001", "role": "admin"}')

# Hash: 사용자 프로필 (부분 업데이트)
r.hset('user:U001', mapping={'name': '김철수', 'tier': 'VIP', 'points': 5000})
r.hincrby('user:U001', 'points', 500)  # 포인트 증가

# Sorted Set: 실시간 리더보드
r.zadd('leaderboard:2024-01', {'player1': 1500, 'player2': 2300})
top10 = r.zrevrange('leaderboard:2024-01', 0, 9, withscores=True)

# 분산 락 (Redlock)
lock = r.set('lock:order_123', 'worker_1', nx=True, ex=30)
if lock:
    # 독점 작업 수행
    r.delete('lock:order_123')
```

### [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 설계 주의사항

```
[핫 파티션 방지]
문제: user_type='VIP' 파티션에 80% 트래픽 집중
해결: PK에 랜덤 접미사 추가 (Write Sharding)
     user_id#1, user_id#2, ... user_id#N

[Single Table Design 패턴]
RDB 여러 테이블을 DynamoDB 단일 테이블로 모델링
PK="USER#U001", SK="PROFILE" → 사용자 정보
PK="USER#U001", SK="ORDER#20240115" → 사용자의 주문
PK="ORDER#O001", SK="ITEM#P001" → 주문의 상품
```

📢 **섹션 요약 비유**: [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Single Table Design은 다용도 가구와 같다. 여러 서랍(PK+SK 조합)이 있어 사람 정보, 주문 정보, 상품 정보를 하나의 가구(테이블)에 넣지만, 서랍 라벨(PK/SK 네이밍 규칙)을 잘 설계해야 원하는 걸 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **응답 속도 향상** | DB 대비 100~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000배 빠른 조회 |
| **DB 부하 감소** | 반복 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 캐시에서 처리해 DB 트래픽 90%+ 감소 |
| **무한 확장** | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/): 요청량에 따른 자동 확장 |
| <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">TTL</a> 자동 만료</strong> | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 만료, 임시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자동 삭제 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **Cache Invalidation** | 캐시 무효화 시점 관리가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 핵심 과제 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> 메모리 한계</strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 메모리를 초과하면 Eviction 발생 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a> 비용</strong> | 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 단위([RCU](/knowledge-base/studynote/02_operating_system/04_synchronization/254_rcu_read_copy_update/)/WCU)로 과금, 예측 어려움 |
| <strong>핫 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a></strong> | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) PK 설계 오류 시 특정 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 과부하 |

📢 **섹션 요약 비유**: [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시는 책상 위 자주 보는 책이다. 책장(DB)에 가지 않아도 즉시 꺼낼 수 있지만, 책상이 꽉 차면 덜 보는 책을 치워야 한다(Eviction). 캐시 무효화는 책 내용이 바뀌면 책상의 책도 교체하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/)/DynamoDB의 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 특성 ([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선) |
| 캐시 패턴 | Cache Aside, [Write-Through](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/) 등 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/) | Redis의 핵심 사용 사례 |
| [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) DAX | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 전용 인메모리 캐시 계층 |
| [컨시스턴트 해싱](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 메커니즘 |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sentinel | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 고가용성 구성 |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 수평 확장 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 구성 |

### 👶 어린이를 위한 3줄 비유 설명
1. [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)는 자동 판매기와 같다. 버튼(키)을 누르면 음료(값)가 즉시 나온다. 슈퍼마켓(DB)보다 훨씬 빠르지만, 넣을 수 있는 음료 종류([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조)가 정해져 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
Key-Value: O(1) 조회 · 초저지연
    ├─► In-Memory: Redis · Memcached (캐시)
    └─► Persistent: DynamoDB · etcd (영속)
    │
    ▼
활용: 세션 · 캐시 · 설정 · 분산 락
```
2. Redis는 교실 앞 칠판이다. 자주 필요한 내용을 칠판(메모리)에 적어두면 교과서(DB)를 매번 찾을 필요가 없다. 단, 칠판 크기(메모리)는 정해져 있다.
3. DynamoDB는 무제한 자동 창고다. 물건이 아무리 많아도 자동으로 공간이 늘어나고([서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 확장), 바코드(키)로 즉시 찾을 수 있지만, 바코드 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계(PK/SK 설계)를 잘 만들어야 한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 235 / 371

← **이전**: [235. 분산 NoSQL 데이터베이스 종류 개요](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/235_nosql_database_types_overview/)
**다음**: [237. 도큐먼트 저장소 (Document Store) - MongoDB / Elasticsearch](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/237_document_store_mongodb_elasticsearch/) →

---
