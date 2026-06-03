+++
title = "139. 인메모리 데이터베이스 (In-Memory DB) — Redis/Memcached/SAP HANA"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: 인메모리 DB는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주 스토리지로 RAM에 저장하여 디스크 I/O 병목을 완전히 제거함으로써 마이크로초(μs) 단위의 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 초당 수백만 연산을 실현한다.
- **가치**: 순수 캐시(Memcached)·캐시+[영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/))·풀스택 분석(SAP HANA)·[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)(VoltDB)로 특화되어, 서로 다른 인메모리 요구 사항에 맞는 솔루션 생태계가 성숙되어 있다.
- **판단 포인트**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내구성 필요 여부와 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡도가 솔루션 선택의 핵심 기준으로, 단순 캐시는 Memcached, 복합 워크로드는 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), 엔터프라이즈 HTAP은 SAP HANA가 적합하다.

---

## Ⅰ. 개요 및 필요성

### 메모리 vs 디스크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이

```text
┌──────────────────────────────────────────────────────────┐
│         스토리지 계층별 접근 지연 (Latency Hierarchy)       │
│                                                          │
│  CPU 레지스터     ~0.3ns   ████                          │
│  L1 캐시         ~1ns     ████                           │
│  L2 캐시         ~4ns     ████                           │
│  RAM (DRAM)      ~100ns   ████                           │
│  NVMe SSD        ~100μs   ████████████████               │
│  SATA SSD        ~500μs   ████████████████████           │
│  HDD             ~10ms    ██████████████████████████████ │
│                                                          │
│  RAM vs HDD 차이: 약 100,000배                            │
│  → 인메모리 DB의 성능 우위 근거                            │
└──────────────────────────────────────────────────────────┘
```

### 인메모리 DB [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 솔루션 | 내구성 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡도 |
|:---:|:---:|:---:|:---:|
| **순수 캐시** | Memcached | 없음 | 키-값 only |
| <strong>캐시+<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a></strong> | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) | RDB+AOF | 자료구조 |
| <strong>엔터프라이즈 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/">HTAP</a></strong> | SAP HANA | 완전한 ACID | 복잡한 SQL |
| <strong>인메모리 <a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/">OLTP</a></strong> | VoltDB | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 기반 | SQL + 절차 |
| **분석 가속** | Apache Ignite | 선택적 | SQL + KV |

📢 **섹션 요약 비유**
> 인메모리 DB와 디스크 기반 DB의 차이는 책상 서랍(RAM)과 창고 깊은 곳 박스([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))의 차이다. 서랍에서 꺼내는 건 0.1초, 창고 박스에서 꺼내는 건 10초가 걸린다면 10만 배 차이다. 하지만 서랍은 작고, 전기가 나가면 내용이 사라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Memcached vs [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 아키텍처 심층 비교

```text
┌─────────────────────────────────────────────────────────────┐
│  Memcached 아키텍처:                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Thread 1 │  │  Thread 2 │  │  Thread N │  (멀티스레드)  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│  단일 해시 테이블, String 타입만, 복제 없음                    │
│  슬랩 할당자(Slab Allocator): 메모리 단편화 방지              │
│  LRU 기반 자동 퇴출 (eviction)                              │
│                                                             │
│  Redis 아키텍처:                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  단일 메인 스레드 (이벤트 루프)                          │  │
│  │  + I/O 스레드 (Redis 6.0+)                             │  │
│  └───────────────────────────────────────────────────────┘  │
│  다양한 자료구조, RDB+AOF 영속성, 복제, 클러스터 지원          │
└─────────────────────────────────────────────────────────────┘
```

### SAP HANA 인메모리 컬럼 스토어

```text
┌──────────────────────────────────────────────────────────────┐
│              SAP HANA 아키텍처                                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Row Store (OLTP 최적화)                    │  │
│  │  빠른 INSERT/UPDATE, 개별 행 접근                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Column Store (OLAP 최적화)                 │  │
│  │  컬럼별 압축 (Dictionary + Run-Length Encoding)          │  │
│  │  SIMD 병렬 집계, 수십억 행 집계도 초고속                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           영속성: 비동기 로그 + 세이브포인트              │  │
│  │  (서버 재시작 시 약 수분 내 복구)                         │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### VoltDB 인메모리 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 특화

```text
VoltDB 설계 원칙:
  1. 단일 스레드 파티션: 잠금 없는(Lock-Free) 처리
  2. 저장 프로시저: Java로 작성, DB 내부 실행
  3. 동기 복제: 과반수 복제 후 응답 → 내구성 보장
  4. 파티셔닝: 파티션 키 기반, 크로스 파티션 최소화

성능: 단일 서버 수백만 TPS (단순 트랜잭션 기준)
적합: 광고 입찰(RTB), 금융 거래 엔진, 통신 과금
```

📢 **섹션 요약 비유**
> SAP HANA의 행 저장과 컬럼 저장 병존은 창고 구조와 같다. 새 상품 입고([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))는 상자째 쌓는 행 저장이 빠르고, "이번 달 사과 총 판매량"([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/))은 과일별로 분리된 칸(컬럼 저장)에서 사과 칸만 세면 된다. 두 작업이 동시에 최적화되는 이중 구조다.

---

## Ⅲ. 비교 및 연결

### 인메모리 DB 내구성([Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 위험 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 솔루션 |
|:---:|:---:|:---:|:---:|
| **없음** | 재시작 시 전부 손실 | 최고 | Memcached |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/">스냅샷</a>(RDB)</strong> | 마지막 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 이후 | 높음 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) RDB |
| <strong>AOF(명령 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>)</strong> | 최대 1초 | 중간 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) AOF |
| <strong>동기 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a></strong> | 매우 적음 | 중간 | VoltDB |
| **WAL + 세이브포인트** | 최소 | 중간~낮음 | SAP HANA |

### 메모리 관리: 캐시 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)

```text
LRU (Least Recently Used): 가장 오래된 접근 키 삭제
LFU (Least Frequently Used): 가장 적게 접근된 키 삭제
TTL: 설정된 만료 시간 초과 키 삭제
Random: 무작위 삭제 (오버헤드 최소)

Redis maxmemory-policy 옵션:
  noeviction      : 메모리 초과 시 에러 반환
  allkeys-lru     : 모든 키 대상 LRU
  volatile-lru    : TTL 키 대상 LRU
  allkeys-lfu     : 모든 키 대상 LFU (4.0+)
  allkeys-random  : 무작위 삭제
```

📢 **섹션 요약 비유**
> [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 캐시는 냉장고 정리와 같다. 오래 손대지 않은 식재료([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/): 오래된 접근)부터 버려서 새 식재료(신규 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 위한 공간을 만든다. LFU는 "적게 먹는" 식재료 기준으로 버린다 — 오래된 것도 자주 쓰면 살아남는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실시간 입찰 시스템 (RTB, Real-Time Bidding) 아키텍처

```text
광고 입찰 요청 (100ms 이내 응답 필수)
        │
        ↓
┌──────────────────────────────────────────────────────┐
│  입찰 엔진 (VoltDB / Redis 기반)                      │
│  1. 사용자 프로필 조회       (Redis Hash: <1ms)       │
│  2. 광고 예산 잔액 확인      (Redis 원자 연산: <1ms)   │
│  3. 예산 차감 + 입찰 기록    (원자 트랜잭션: <2ms)     │
│  4. 낙찰 결과 반환           (총 <10ms)               │
└──────────────────────────────────────────────────────┘
        │
        ↓
Kafka (배치 처리용 로그 → BigQuery/Redshift)
```

### 인메모리 DB 선택 가이드

| 요구 사항 | 추천 솔루션 |
|:---|:---:|
| 단순 웹 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 캐시 | Memcached |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) + 다양한 자료구조 + Pub/Sub | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) |
| 실시간 비딩·금융 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (수백만 TPS) | VoltDB |
| 엔터프라이즈 [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) (SAP 연동) | SAP HANA |
| [하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) 인메모리 그리드 | Apache Ignite |

📢 **섹션 요약 비유**
> RTB 광고 입찰에서 100ms 내에 응답하지 못하면 낙찰 기회가 사라진다. 인메모리 DB는 이 제약 조건을 물리적으로 충족시키는 유일한 방법이다. 마치 0.1초 만에 경매에서 손을 드는 것 — 디스크 DB로는 시간이 너무 오래 걸린다.

---

## Ⅴ. 기대효과 및 결론

### 인메모리 DB 도입 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 분석

| 구성 | 설명 | 비용 절감 |
|:---:|:---:|:---:|
| DB 앞단 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 | 히트율 90%+ → DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 90% 감소 | DB 서버 1/[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 전환 | 스티키 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 제거 → 웹 서버 수평 확장 | 인프라 비용 절감 |
| SAP [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) + HANA | 배치 리포트 24시간 → 실시간 | 비즈니스 민첩성 |

### 결론
인메모리 DB는 현대 고성능 아키텍처에서 "빠른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로"를 담당하는 필수 레이어다. 순수 캐시부터 엔터프라이즈 HTAP까지 스펙트럼이 넓어, 요구 사항의 정확한 분석이 솔루션 선택의 관건이다. 기술사 시험에서는 <strong>RAM vs 디스크 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 차이의 물리적 근거</strong>, <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> RDB+AOF <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a> 메커니즘</strong>, <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a>/<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/">LFU</a> 캐시 교체 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>, <strong>SAP HANA 행/컬럼 이중 스토어 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/">HTAP</a> 원리</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> 인메모리 DB 도입 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "자주 쓰는 물건을 책상 위에 두는" 집 정리와 같다. 가장 자주 꺼내는 것([핫 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/))을 책상 위(RAM)에, 가끔 필요한 것은 서랍([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에, 거의 안 쓰는 것은 창고([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))에 두면 일의 효율이 극적으로 올라간다. 전부를 책상 위에 놓으면 어수선해지듯, 인메모리와 디스크의 적절한 계층화가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| [슬랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) 할당자 | Memcached 메모리 | 고정 크기 슬롯으로 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 방지 |
| [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)/[LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/) | 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 메모리 초과 시 퇴출 대상 선택 |
| [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) | 처리 패러다임 | SAP HANA의 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)+[OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 통합 |
| WAL (Write-Ahead Log) | 내구성 메커니즘 | 장애 시 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 핫/웜/콜드 계층화 | 스토리지 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 빈도별 스토리지 분리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[디스크 기반 RDBMS — 영속 저장, I/O 병목, 밀리초~초 단위 응답]
    │
    ▼
[캐시 레이어 (Cache Layer) — Memcached 키-값 캐시, DB 부하 분산]
    │
    ▼
[인메모리 DB (In-Memory DB) — Redis / SAP HANA, 전체 데이터 RAM 상주, 마이크로초 응답]
    │
    ▼
[영속 인메모리 (Persistent In-Memory) — AOF / RDB 스냅샷, 재시작 후 데이터 복구]
    │
    ▼
[분산 인메모리 클러스터 (Redis Cluster) — 수평 샤딩·자동 장애 조치, 수백 GB 용량]
    │
    ▼
[인메모리 HTAP (SAP HANA / MemSQL) — 트랜잭션 + 분석 워크로드 통합 실시간 처리]
```
이 흐름은 디스크 기반 DB의 I/O [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 메모리 캐시로 완화하고, 완전한 인메모리 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)·[영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 확장으로 진화하여 실시간 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 분석을 동시에 처리하는 [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 아키텍처로 수렴하는 고속 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 기술의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 인메모리 DB는 책가방 대신 손에 들고 있는 것 — 바로 꺼낼 수 있어서 교과서(디스크 DB)를 책가방에서 찾는 것보다 10만 배 빨라요.
2. Memcached는 포스트잇(빠르지만 날리면 사라짐), Redis는 화이트보드(빠르고 사진으로 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 가능), SAP HANA는 대형 스마트 칠판(모든 기능 + 수식도 가능)이에요.
3. [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 냉장고 정리 — 오래된 음식부터 버려서 새로 산 음식을 넣을 공간을 만드는 것처럼, 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지워 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 위한 메모리를 확보해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 262

← **이전**: [138. NewSQL — CockroachDB/TiDB/YugabyteDB SQL+수평확장+ACID](/knowledge-base/studynote/16_bigdata/06_nosql/138_newsql/)
**다음**: [140. 일관성 수준 선택 (Consistency Levels) — Strong/Eventual/Bounded Staleness](/knowledge-base/studynote/16_bigdata/06_nosql/140_consistency_levels/) →

---
