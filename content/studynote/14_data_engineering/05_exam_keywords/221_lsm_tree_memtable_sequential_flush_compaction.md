---
title: 221. LSM 트리 (Log-Structured Merge-Tree) 멤테이블 순차 플러시 콤팩션
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSM 트리(Log-Structured Merge-Tree)는 랜덤 [[289_cqrs_db|쓰기]]를 순차 [[289_cqrs_db|쓰기]]로 변환해 [[327_ssd|SSD]]/[[465_hdd_structure|HDD]] [[289_cqrs_db|쓰기]] [[282_performance_tactics|성능]]을 극대화하는 저장 엔진 핵심 자료구조이다.
> 2. **가치**: [[494_memtable_sstable_flush|Memtable]](인메모리 버퍼)→SSTable(Sorted String Table) 순차 플러시 구조 덕분에 [[541_cassandra|Cassandra]]·[[543_hbase|HBase]]·RocksDB가 초당 수십만 건의 [[289_cqrs_db|쓰기]]를 달성한다.
> 3. **판단 포인트**: [[289_cqrs_db|쓰기]] 집약 워크로드에는 LSM, 읽기 집약 워크로드에는 B-Tree가 유리하며, [[347_compaction|Compaction]] [[268_strategy_pattern|전략]] 선택이 읽기 증폭(Read Amplification)과 [[480_write_amplification|쓰기 증폭]]([[480_write_amplification|Write Amplification]]) 균형을 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적인 [[064_b_tree|B-Tree]] 기반 스토리지 엔진은 랜덤 I/O(Input/Output)로 인한 높은 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]을 피할 수 없다. 디스크 헤드가 임의의 위치로 이동하면서 [[001_dikw_pyramid|데이터]]를 갱신해야 하기 때문이다. LSM 트리(Log-Structured Merge-Tree)는 1996년 Patrick O'Neil이 제안한 구조로, **"[[289_cqrs_db|쓰기]]는 항상 순차적으로, 병합은 나중에"** 라는 철학으로 이 문제를 해결한다.

### 등장 배경

| 구분 | [[064_b_tree|B-Tree]] | LSM 트리 |
|:---|:---|:---|
| [[289_cqrs_db|쓰기]] 방식 | 랜덤 I/O (in-place update) | 순차 I/O (append-only) |
| [[289_cqrs_db|쓰기]] [[282_performance_tactics|성능]] | IOPS 제약으로 병목 | 메모리 버퍼→디스크 순차 플러시 |
| 읽기 [[282_performance_tactics|성능]] | 트리 탐색 O(log n) | 다수 레벨 탐색, [[061_bloomfilter|Bloom Filter]] 보조 |
| 공간 사용 | 낮음 | [[347_compaction|Compaction]] 전 임시 공간 필요 |
| 대표 시스템 | MySQL InnoDB, PostgreSQL | [[543_hbase|HBase]], [[541_cassandra|Cassandra]], RocksDB, LevelDB |

📢 **섹션 요약 비유**: LSM 트리는 "지금 당장 정리하지 말고 일단 메모장에 받아 적은 뒤, 여유 있을 때 한꺼번에 서류철로 이전하는" 사무 방식과 같다. 매번 [[501_file_definition_logical_record|파일]] 캐비닛을 열어 정확한 위치에 끼워 넣는 [[064_b_tree|B-Tree]] 방식보다 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 전체 [[289_cqrs_db|쓰기]] 경로

```
클라이언트 쓰기 요청
        │
        ▼
┌──────────────────────┐
│   WAL (Write-Ahead   │  ← 내구성 보장 (crash recovery)
│   Log, 선행 기록 로그) │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│     Memtable         │  ← 인메모리 정렬 구조 (Red-Black Tree 또는 SkipList)
│  (메모리 쓰기 버퍼)   │
└──────────────────────┘
   임계 크기 초과 시
        │ flush
        ▼
┌──────────────────────┐
│   Level 0 SSTable    │  ← 불변(Immutable), 순차 정렬 파일
│ (Sorted String Table)│
└──────────────────────┘
        │ Compaction
        ▼
┌──────────────────────┐
│   Level 1 ~ Level N  │  ← 레벨 올라갈수록 파일 크기 10× 증가
│     SSTables         │
└──────────────────────┘
```

### 2-2. 구성 요소 상세

**WAL (Write-Ahead Log, 선행 기록 [[568_logs_distributed_logging_elk_fluentd|로그]])**
모든 [[289_cqrs_db|쓰기]] 요청을 디스크 순차 [[568_logs_distributed_logging_elk_fluentd|로그]]에 먼저 기록한다. 시스템 장애 시 [[494_memtable_sstable_flush|Memtable]] 복구에 사용된다.

**[[494_memtable_sstable_flush|Memtable]] (메모리 [[289_cqrs_db|쓰기]] 버퍼)**
정렬 상태를 유지하는 인메모리 자료구조([[063_red_black_tree|레드-블랙 트리]] 또는 [[067_skip_list|스킵 리스트]]). 임계 크기(보통 64~256 MB) 초과 시 [[298_immutable|Immutable]] Memtable로 전환되고, 백그라운드 스레드가 SSTable로 플러시한다.

**SSTable (Sorted String Table, 정렬 문자열 테이블)**
디스크에 저장된 불변([[298_immutable|Immutable]]) 정렬 [[501_file_definition_logical_record|파일]]. [[501_file_definition_logical_record|파일]] 내부는 키 순으로 정렬되어 있어 [[031_binary_search_algorithm|이진 탐색]] 또는 [[061_bloomfilter|블룸 필터]]([[061_bloomfilter|Bloom Filter]])로 빠르게 조회할 수 있다.

### 2-3. [[347_compaction|Compaction]] (병합·정렬) [[268_strategy_pattern|전략]]

```
Leveled Compaction                  Size-Tiered Compaction
────────────────────               ──────────────────────
L0: [f1][f2][f3][f4]               Tier1: [s1][s2][s3][s4]
       │ overlap 검사                        │ 유사 크기끼리 병합
L1: [   merged_file   ]            Tier2: [   larger_file   ]
       │ 크기 10× 증가              Tier3: [      huge_file     ]
L2: [ ─────────────── ]
(각 레벨 총 크기 제한 있음)          쓰기 증폭 낮음 / 읽기 증폭 높음
읽기 증폭 낮음 / 쓰기 증폭 높음
```

| [[268_strategy_pattern|전략]] | [[480_write_amplification|쓰기 증폭]] (WA) | 읽기 증폭 ([[161_ra_registration_authority|RA]]) | 공간 증폭 ([[767_sa_standalone_5g_core_network|SA]]) | 적합 워크로드 |
|:---|:---:|:---:|:---:|:---|
| Leveled [[347_compaction|Compaction]] | 높음 ([[489_raid_10_hybrid|10]]~30×) | 낮음 | 낮음 | 읽기 빈번, [[327_ssd|SSD]] 환경 |
| Size-Tiered [[347_compaction|Compaction]] | 낮음 (5~[[489_raid_10_hybrid|10]]×) | 높음 | 높음 | [[289_cqrs_db|쓰기]] 집약, [[465_hdd_structure|HDD]] 환경 |
| TWCS (Time Window CS) | 중간 | 중간 | 중간 | 시계열 [[001_dikw_pyramid|데이터]], [[294_ttl_time_to_live_looping_prevention|TTL]] 있는 [[001_dikw_pyramid|데이터]] |

📢 **섹션 요약 비유**: Leveled Compaction은 "도서관 사서가 책을 매일 정리하여 책장을 깔끔하게 유지하지만 정리에 힘이 많이 들고", Size-Tiered는 "쌓이면 쌓이는 대로 두다가 한꺼번에 대형 박스로 옮겨 담는" 방식이다.

---

## Ⅲ. 비교 및 연결

### 3-1. 읽기 최적화 보조 구조

읽기 요청이 오면 최신 Memtable부터 L0 → L1 → ... → Ln 순으로 조회해야 한다. 이 비용을 줄이기 위해 다음 구조를 사용한다.

- **[[061_bloomfilter|Bloom Filter]] ([[061_bloomfilter|블룸 필터]])**: 특정 키가 SSTable에 없음을 확률적으로 빠르게 판별. False Negative 없음, False Positive 가능.
- **Block [[154_database_index_b_tree_search_optimization|Index]] (블록 [[154_database_index_b_tree_search_optimization|인덱스]])**: SSTable 내 [[001_dikw_pyramid|데이터]] 블록의 시작 키와 오프셋을 기록하여 탐색 범위를 좁힘.
- **Block Cache (블록 캐시)**: 자주 읽히는 블록을 메모리에 [[456_caching|캐싱]].

### 3-2. 주요 시스템별 LSM 구현 특징

| 시스템 | [[347_compaction|Compaction]] 기본 [[268_strategy_pattern|전략]] | 특이사항 |
|:---|:---|:---|
| RocksDB | Leveled | Facebook 최적화, Column Family 지원 |
| LevelDB | Leveled | Google 개발, RocksDB의 원형 |
| Apache [[541_cassandra|Cassandra]] | STCS / TWCS | [[136_variance|분산]] 환경, Wide-Column 모델 |
| Apache [[543_hbase|HBase]] | Minor/Major [[347_compaction|Compaction]] | [[013_hdfs|HDFS]] 기반, Region Server별 관리 |
| ScyllaDB | Incremental [[347_compaction|Compaction]] | C++ 구현, [[541_cassandra|Cassandra]] 호환 |

📢 **섹션 요약 비유**: LSM 트리 위에 올라간 각 시스템은 같은 기초 공사(LSM) 위에 각자의 설계로 건물을 올린 것과 같다. 기초는 같지만 내부 구조와 엘리베이터([[347_compaction|Compaction]]) 방식은 제각각이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 설계 트레이드오프 시나리오

**시나리오 A – 이커머스 [[626_log_collection|로그 수집]] (초당 100만 건 [[289_cqrs_db|쓰기]])**
- RocksDB + Size-Tiered [[347_compaction|Compaction]] 선택
- 이유: [[480_write_amplification|쓰기 증폭]]을 최소화해야 하며, [[568_logs_distributed_logging_elk_fluentd|로그]]는 최신 [[001_dikw_pyramid|데이터]] 위주로 읽히므로 L0 히트율 높음

**시나리오 B – [[101_iot_concept|IoT]] 센서 시계열 [[001_dikw_pyramid|데이터]] ([[294_ttl_time_to_live_looping_prevention|TTL]] 30일)**
- [[541_cassandra|Cassandra]] + TWCS (Time Window [[347_compaction|Compaction]] [[268_strategy_pattern|Strategy]], 시간 창 컴팩션 [[268_strategy_pattern|전략]])
- 이유: 같은 시간 창 [[001_dikw_pyramid|데이터]]끼리 병합되므로 [[294_ttl_time_to_live_looping_prevention|TTL]] 만료 시 SSTable 통째로 삭제 가능 → 공간 증폭 최소화

**시나리오 C – 사용자 프로파일 빈번 조회**
- RocksDB + Leveled [[347_compaction|Compaction]] + [[061_bloomfilter|Bloom Filter]]
- 이유: 읽기 증폭을 최소화하고 [[061_bloomfilter|블룸 필터]]로 불필요한 I/O 차단

### 4-2. [[347_compaction|Compaction]] 튜닝 핵심 파라미터

```
RocksDB Leveled Compaction 주요 설정
────────────────────────────────────
max_bytes_for_level_base = 256MB   (L1 최대 크기)
max_bytes_for_level_multiplier = 10 (레벨별 10× 증가)
level0_file_num_compaction_trigger = 4 (L0 파일 4개 쌓이면 compaction)
write_buffer_size = 64MB           (Memtable 크기)
max_write_buffer_number = 3        (동시 Memtable 수)
```

📢 **섹션 요약 비유**: 파라미터 튜닝은 "쓰레기통 크기([[494_memtable_sstable_flush|Memtable]])와 청소 주기([[347_compaction|Compaction]] trigger)를 조절하는 것"이다. 통이 작으면 자주 비워야 하고, 너무 크면 넘친다.

---

## Ⅴ. 기대효과 및 결론

LSM 트리가 현대 [[136_variance|분산]] [[002_database_definition|데이터베이스]]의 표준 저장 엔진이 된 이유는 명확하다. [[289_cqrs_db|쓰기]] 경로를 순차적으로 제한함으로써 디스크 I/O 특성을 최대한 활용하고, Compaction을 통해 점진적으로 [[001_dikw_pyramid|데이터]]를 정리하면서도 서비스를 중단하지 않는다.

### [[018_kpi|핵심 성과 지표]]

| 지표 | [[064_b_tree|B-Tree]] 대비 LSM 개선 |
|:---|:---|
| [[289_cqrs_db|쓰기]] [[139_throughput|처리량]] (Write [[139_throughput|Throughput]]) | 5~[[489_raid_10_hybrid|10]]× 향상 |
| [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]] (Write [[141_latency|Latency]]) | [[489_raid_10_hybrid|10]]× 감소 (순차 I/O 덕분) |
| [[327_ssd|SSD]] 수명 | 랜덤 [[289_cqrs_db|쓰기]] 감소로 낸드 수명 연장 |
| 읽기 [[015_지연_데이터_관점|지연]] (Read [[141_latency|Latency]]) | [[061_bloomfilter|Bloom Filter]] 없이는 2~5× 증가 가능 |

기술사 시험에서 LSM 트리는 **"[[035_nosql|NoSQL]] 고성능 [[289_cqrs_db|쓰기]]의 근간"** 으로, [[347_compaction|Compaction]] [[268_strategy_pattern|전략]] 비교와 읽기/[[480_write_amplification|쓰기 증폭]] 트레이드오프를 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: LSM 트리는 "선불카드처럼 나중에 정산하는" 방식이다. 지금 당장 정확히 정리하지 않아도 되지만, Compaction이라는 정기 정산 작업이 반드시 필요하다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 구성 요소 | WAL (Write-Ahead Log) | 내구성 보장용 선행 기록 [[568_logs_distributed_logging_elk_fluentd|로그]] |
| 구성 요소 | [[494_memtable_sstable_flush|Memtable]] | 인메모리 정렬 [[289_cqrs_db|쓰기]] 버퍼 |
| 구성 요소 | SSTable (Sorted String Table) | 불변 정렬 디스크 [[501_file_definition_logical_record|파일]] |
| 최적화 | [[061_bloomfilter|Bloom Filter]] ([[061_bloomfilter|블룸 필터]]) | 키 존재 여부 빠른 판별 |
| [[268_strategy_pattern|전략]] | Leveled [[347_compaction|Compaction]] | 읽기 증폭 최소화, 레벨별 크기 제한 |
| [[268_strategy_pattern|전략]] | Size-Tiered [[347_compaction|Compaction]] | [[480_write_amplification|쓰기 증폭]] 최소화, 유사 크기 병합 |
| 적용 | RocksDB / LevelDB | Google·Facebook LSM 구현체 |
| 적용 | [[543_hbase|HBase]] / [[541_cassandra|Cassandra]] | [[136_variance|분산]] 환경 LSM [[002_database_definition|데이터베이스]] |
| 비교 | [[064_b_tree|B-Tree]] | 읽기 최적화, 랜덤 I/O |
| 지표 | [[480_write_amplification|Write Amplification]] ([[480_write_amplification|쓰기 증폭]]) | 실제 [[289_cqrs_db|쓰기]] / [[369_logic_bomb|논리]] [[289_cqrs_db|쓰기]] 비율 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 숙제를 바로 책상 서랍에 정리하지 않고 일단 메모장에 적어두는 것처럼, LSM 트리는 [[001_dikw_pyramid|데이터]]를 먼저 메모리에 빠르게 받아 적는다.

### 📈 관련 키워드 및 발전 흐름도

```text
B-Tree (읽기 최적화, 랜덤 I/O)
    │
    ▼
LSM-Tree (쓰기 최적화, 순차 I/O)
    ├─► MemTable (인메모리 정렬)
    ├─► Flush → SSTable (디스크 정렬 파일)
    └─► Compaction: Size-Tiered · Leveled
    │
    ▼
적용: Cassandra · HBase · RocksDB · LevelDB
```
2. 메모장이 꽉 차면 한꺼번에 깔끔하게 묶어서 [[501_file_definition_logical_record|파일]] 캐비닛에 넣는데, 이것이 SSTable 플러시이다.
3. [[501_file_definition_logical_record|파일]] 캐비닛에 쌓인 [[501_file_definition_logical_record|파일]]들을 주기적으로 합쳐서 큰 [[501_file_definition_logical_record|파일]]로 정리하는 작업이 Compaction이고, 이 덕분에 나중에 찾을 때도 빠르다.
