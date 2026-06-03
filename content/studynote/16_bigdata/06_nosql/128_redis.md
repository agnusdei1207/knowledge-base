+++
title = "128. Redis (Remote Dictionary Server) — 인메모리 데이터 구조 서버"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: Redis는 단순한 캐시를 넘어 String·List·Hash·Set·Sorted Set 등 풍부한 자료구조를 인메모리로 제공하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 서버로, 초당 수십만 연산의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 핵심 강점이다.
- **가치**: RDB([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)과 AOF(Append-Only [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) 결합으로 인메모리의 속도와 디스크의 내구성을 동시에 달성하며, [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster로 수평 확장까지 지원한다.
- **판단 포인트**: Pub/Sub [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금·실시간 순위표·[세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/) 등 패턴별로 Redis의 특정 자료구조를 매핑하여 설계해야 최적 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다.

---

## Ⅰ. 개요 및 필요성

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 탄생 배경
2009년 살바토레 산필리포(Salvatore Sanfilippo)가 실시간 [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 해결하기 위해 개발. "단순히 키-값을 넘어 값 자체를 조작할 수 있는 서버 측 자료구조"라는 개념이 혁신이었다.

### 핵심 자료구조 총람

| 자료구조 | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(예) | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 주요 용도 |
|:---:|:---:|:---:|:---|
| **String** | SET/GET/INCR | O(1) | 캐시, [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 토큰 |
| **List** | LPUSH/RPOP/LRANGE | O(1)/O(N) | 작업 큐, 활동 피드 |
| **Hash** | HSET/HGET/HMGET | O(1) | 객체 저장(사용자 프로필) |
| **Set** | SADD/SISMEMBER | O(1) | 고유 [방문자](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/), 태그 |
| **Sorted Set (ZSet)** | ZADD/ZRANGE/ZRANK | O(log N) | 실시간 리더보드, 순위 |
| **Bitmap** | SETBIT/BITCOUNT | O(1)/O(N) | 일별 출석 체크 |
| **HyperLogLog** | PFADD/PFCOUNT | O(1) | 근사 카디널리티(UV 측정) |
| <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/">Stream</a></strong> | XADD/XREAD | O(1) | 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 대체 |

📢 **섹션 요약 비유**
> Redis는 스위스 아미 나이프와 같다. 단순한 캐시(칼날)를 기본으로, 상황에 따라 큐(가위)·순위표(톱)·Pub/Sub(코르크 오프너) 등 다양한 도구를 꺼내 쓸 수 있다. 하지만 모든 도구를 동시에 쓰려 하면 오히려 복잡해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)

```text
┌─────────────────────────────────────────────────────────┐
│              Redis 처리 모델 (단일 스레드 이벤트 루프)       │
│                                                         │
│  Client 1 ──┐                                           │
│  Client 2 ──┤──→ [소켓 큐] ──→ [이벤트 루프] ──→ 응답    │
│  Client 3 ──┘       (epoll)    (단일 스레드)             │
│                                                         │
│  * 컨텍스트 스위칭 없음 → 초저지연                          │
│  * 명령은 원자적으로 순차 처리 → 레이스 컨디션 없음             │
│  * I/O 스레드(Redis 6.0+): 네트워크 I/O 병렬화             │
└─────────────────────────────────────────────────────────┘
```

### [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)(Persistence) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```text
┌───────────────────────────────────────────────────────────┐
│                 Redis 영속성 메커니즘                        │
│                                                           │
│  ┌─────────────────┐      ┌─────────────────────────────┐ │
│  │  RDB (Snapshot) │      │  AOF (Append-Only File)     │ │
│  │                 │      │                             │ │
│  │  주기적 fork()  │      │  모든 쓰기 명령을 로그 파일에  │ │
│  │  → 전체 메모리  │      │  순차 추가 (fsync 정책 선택)  │ │
│  │    직렬화       │      │                             │ │
│  │                 │      │  always: 매 명령 fsync      │ │
│  │  장점: 빠른 복구│      │  everysec: 1초마다 (기본)    │ │
│  │  단점: 데이터   │      │  no: OS에 위임              │ │
│  │    손실 가능    │      │                             │ │
│  │  (마지막 스냅샷 │      │  장점: 데이터 손실 최소화     │ │
│  │   이후 소실)   │      │  단점: 파일 크기 증가, 재시작  │ │
│  │                 │      │        시간 증가             │ │
│  └─────────────────┘      └─────────────────────────────┘ │
│                                                           │
│  권장: RDB + AOF 혼합 (Hybrid Persistence)                │
│  → 빠른 복구 + 최소 데이터 손실                             │
└───────────────────────────────────────────────────────────┘
```

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster 구조

```text
┌──────────────────────────────────────────────────────────┐
│           Redis Cluster (수평 확장)                       │
│                                                          │
│  Hash Slots: 0 ~ 16383 (총 16384개)                      │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Master 1    │  │  Master 2    │  │  Master 3    │   │
│  │  Slot 0~5460 │  │ Slot 5461~   │  │ Slot 10923~  │   │
│  │              │  │   10922      │  │   16383      │   │
│  │  Replica 1   │  │  Replica 2   │  │  Replica 3   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│  CRC16(key) % 16384 → 슬롯 번호 → 담당 마스터 노드         │
│  클라이언트: MOVED 리다이렉션으로 올바른 노드로 라우팅         │
└──────────────────────────────────────────────────────────┘
```

### [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/): MULTI/EXEC

| 명령 | 동작 |
|:---:|:---|
| `MULTI` | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 시작, 이후 명령은 큐에 저장 |
| `EXEC` | 큐의 모든 명령을 원자적으로 실행 |
| `DISCARD` | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 취소, 큐 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 |
| `WATCH key` | 낙관적 잠금(Optimistic [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), 변경 시 EXEC 실패 |

📢 **섹션 요약 비유**
> [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster의 해시 슬롯은 선거구 분할과 같다. 총 16384개 선거구를 여러 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터가 나눠 담당하고, 투표([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 CRC16 계산으로 자동으로 올바른 선거구로 배정된다. 노드가 추가되면 선거구 일부를 재배분하면 끝이다.

---

## Ⅲ. 비교 및 연결

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) vs Memcached

| 항목 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) | Memcached |
|:---:|:---:|:---:|
| 자료구조 | 다양(8가지+) | String만 |
| [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) | RDB + AOF | 없음(순수 캐시) |
| 클러스터 | 내장 지원 | 클라이언트 사이드 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) |
| [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터-레플리카 | 없음 |
| Pub/Sub | 지원 | 미지원 |
| 멀티스레드 | I/O [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(v6+) | 완전 멀티스레드 |
| 적합 | 복잡 워크로드 | 단순 캐시 |

### Pub/Sub [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 패턴

```text
Publisher ──→ Channel "news:sports" ──→ Subscriber A
                                   ──→ Subscriber B
                                   ──→ Subscriber C

* 메시지 보장 없음(Fire-and-forget)
* 영속성 필요 시 Redis Stream 사용 권장
```

📢 **섹션 요약 비유**
> Redis와 Memcached의 차이는 만능 슈퍼마켓([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/))과 편의점(Memcached)의 차이와 같다. 편의점은 빠르고 단순하지만 취급 품목이 한정적이다. 슈퍼마켓은 거의 모든 것을 구할 수 있지만, 단순한 우유 한 팩만 사러 가기에는 약간 과한 느낌이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 패턴별 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 자료구조 매핑

| 실무 패턴 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 자료구조 | 핵심 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) |
|:---:|:---:|:---:|
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 저장 | String + EXPIRE | SET/GET/[TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) |
| 실시간 리더보드 | Sorted Set | ZADD/ZREVRANGE |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금 | String + NX + PX | SET [lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) NX PX 30000 |
| 중복 요청 방지 | Set/Bitmap | SADD/SETBIT |
| 작업 큐 | List | LPUSH/BRPOP |
| 이벤트 스트림 | [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) | XADD/XREADGROUP |

### [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 포인트

```text
⚠️ Redis 운영 시 주의 사항:

1. KEYS * 명령 금지 → SCAN 0 COUNT 100 MATCH "prefix:*" 사용
   (KEYS는 단일 스레드를 블로킹하여 전체 서비스 지연)

2. Big Key 방지 → Hash/Set 아이템 수 10,000개 이하 권장
   (1개의 큰 키 삭제 시 UNLINK로 비동기 삭제)

3. 메모리 정책 설정 → maxmemory-policy
   allkeys-lru: 캐시 용도
   noeviction: 데이터 손실 불허 시
```

📢 **섹션 요약 비유**
> Redis의 `KEYS *` 명령은 도서관 사서가 모든 책을 하나하나 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하느라 다른 손님을 못 받는 것과 같다. `SCAN`은 조금씩 나눠서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하니 다른 손님도 동시에 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)할 수 있다. 실무에서 `KEYS *`는 절대 금지어다.

---

## Ⅴ. 기대효과 및 결론

### 도입 전/후 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 (e-커머스 실사례 기준)

| 항목 | DB Only | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 추가 |
|:---:|:---:|:---:|
| 상품 상세 응답시간 | 120ms | 2ms |
| DB CPU | 85% | 15% |
| [캐시 히트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/)율 | — | 94% |
| TPS | 3,000 | 180,000 |

### 결론
Redis는 현대 고성능 아키텍처에서 사실상 필수 구성 요소로 자리잡았다. 단순 캐시 레이어를 넘어 실시간 분석·[메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징·[세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/)·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금·이벤트 스트리밍까지 단일 인프라로 처리할 수 있다. 기술사 시험에서는 **자료구조 선택 근거**, <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a> <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 결정 기준</strong>, <strong>클러스터 슬롯 분배 원리</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> Redis를 도입한 아키텍처는 도서관 앞에 짧은 대출 기간의 회전서가를 설치한 것과 같다. 자주 빌리는 책(인기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 회전서가([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/))에서 즉시 집어가고, 오래된 자료(원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 깊숙한 창고(RDBMS)에서 꺼낸다. 덕분에 대부분의 방문객(요청)이 창고까지 가지 않아도 된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| [일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) | 클러스터 기반 | 해시 슬롯 0~16383 분배 |
| AOF (Append-Only [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 메커니즘 | 명령 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| RDB ([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) | [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 메커니즘 | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| Pub/Sub | [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 패턴 | 채널 기반 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 브로드캐스트 |
| CRDT | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) CRDT (엔터프라이즈) |

### 📈 관련 키워드 및 발전 흐름도

```text
[인메모리 (In-Memory)]
    │
    ▼
[Redis (Redis)]
    │
    ▼
[키-값 저장소 (Key-Value Store)]
    │
    ▼
[캐싱 (Caching)]
```

이 흐름도는 인메모리 특성이 Redis의 [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)와 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 구조로 이어지는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. Redis는 책상 위의 메모장 같아요. 필요한 내용을 적어두면 책장(DB)을 뒤지지 않고 바로 꺼낼 수 있어요.
2. 중요한 메모는 사진도 찍어두고(RDB [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)) 언제 썼는지 일기도 쓰는(AOF [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) 이중 보관이 안전해요.
3. [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 클러스터는 메모장을 여러 명이 나눠 가지는 것처럼, 한 명이 감당 못할 양의 메모를 팀원끼리 16384개 섹션으로 분담해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 128 / 262

← **이전**: [127. 키-값 데이터베이스 (Key-Value DB) — Redis/DynamoDB/Riak](/knowledge-base/studynote/16_bigdata/06_nosql/127_key_value_db/)
**다음**: [129. 문서형 데이터베이스 (Document DB) — MongoDB/CouchDB/Firestore](/knowledge-base/studynote/16_bigdata/06_nosql/129_document_db/) →

---
