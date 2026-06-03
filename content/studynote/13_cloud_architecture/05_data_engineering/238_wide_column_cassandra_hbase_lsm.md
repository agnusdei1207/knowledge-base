+++
title = "238. 와이드 컬럼 저장소 (Wide-Column Store) - Cassandra / HBase"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [와이드 컬럼 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/038_wide_column/)(Wide-Column Store)는 행 키(Row [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 기반으로 컬럼 패밀리를 구성하며, **페타바이트 규모의 시계열·이벤트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 초당 수십만 건 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)**에 최적화된 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB다.
> 2. **가치**: [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/)([Log-Structured Merge-Tree](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/)) 기반 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 엔진으로 **디스크 랜덤 I/O 없이 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)**만 수행하여 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 극대화하고, [컨시스턴트 해싱](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)으로 노드 장애에도 무중단 운영이 가능하다.
> 3. **판단 포인트**: Cassandra는 마스터리스(Masterless) 완전 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)으로 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)이 없고, HBase는 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위에서 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 에코시스템과 통합되므로, **24/7 무중단 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) vs [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 배치 통합** 요건이 선택 기준이다.

---

## Ⅰ. 개요 및 필요성

[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서가 초당 100만 건의 온도·습도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송한다. 페이스북은 사용자 타임라인에 초당 수십만 건의 메시지를 저장한다. RDBMS로는 이 규모의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 감당할 수 없다.

[와이드 컬럼 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/038_wide_column/)는 **"[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 무조건 빠르게, 읽기는 행 키 기준으로"** 라는 단순하지만 강력한 원칙으로 이 문제를 해결한다.

```
[와이드 컬럼 저장소 개념]
Row Key: "sensor:IoT-001:2024-01-15:09:00:00"
┌──────────────────────────────────────────────────────────┐
│  Column Family "cf_data"                                 │
│  ├── temperature: 23.5                                   │
│  ├── humidity: 60.2                                      │
│  └── pressure: 1013.25                                   │
│  Column Family "cf_meta"                                 │
│  ├── firmware: "v2.1"                                    │
│  └── location: "서울 강남"                                │
└──────────────────────────────────────────────────────────┘

특징:
- 행마다 컬럼 수와 종류가 다를 수 있음
- 행 키로 데이터 정렬·분산
- 컬럼 패밀리 단위 압축·저장 최적화
```

📢 **섹션 요약 비유**: [와이드 컬럼 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/038_wide_column/)는 무한히 확장 가능한 엑셀 시트다. 각 행(Row [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))이 서로 다른 수의 열을 가질 수 있고, 시트가 너무 커지면 자동으로 여러 컴퓨터에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) ([Log-Structured Merge-Tree](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/)) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 엔진

```
[LSM-Tree 쓰기 흐름]
쓰기 요청 → WAL(Write-Ahead Log) → MemTable(메모리 버퍼)
                                        │ MemTable 가득 찰 때
                                        ▼
                              SSTable (Sorted String Table)
                              → 디스크에 순차 쓰기 (랜덤 I/O 없음!)
                                        │ 백그라운드 Compaction
                                        ▼
                              더 큰 SSTable로 병합 (Leveled Compaction)

핵심 원리:
1. 모든 쓰기는 순차 (Random I/O → Sequential I/O)
2. 인메모리 버퍼 → 디스크 플러시
3. Compaction으로 읽기 성능 주기적 최적화
```

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처 (Masterless Ring)

```
┌─────────────────────────────────────────────────────────┐
│               Cassandra 링 토폴로지                       │
│                                                         │
│            Node A (token 0~249)                         │
│           /                      \                      │
│  Node D  (token 750~999)    Node B (token 250~499)      │
│           \                      /                      │
│            Node C (token 500~749)                       │
│                                                         │
│  특징:                                                   │
│  - 마스터 없음 (모든 노드 동등)                           │
│  - 컨시스턴트 해싱으로 데이터 분산                         │
│  - Replication Factor: 3 (각 데이터 3개 노드 복제)        │
│  - Gossip Protocol: 노드 상태 전파                       │
└─────────────────────────────────────────────────────────┘
```

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 ([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) Level)

| 수준 | 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
|:---|:---|:---|:---|
| **ONE** | 1개 노드 응답 | 최고 | 낮음 |
| **QUORUM** | 과반수(RF/2+1) 응답 | 중간 | 중간 |
| **ALL** | 모든 노드 응답 | 낮음 | 최고 |
| **LOCAL_QUORUM** | 로컬 DC 과반수 | 높음 | 중간 |

```
WRITE QUORUM + READ QUORUM = 강한 일관성 보장
(쓰기 2/3 노드 + 읽기 2/3 노드 → 최소 1개 노드 겹침)
```

📢 **섹션 요약 비유**: [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 링과 Quorum은 다수결 투표다. 3명 중 2명(Quorum)이 "이 값이 맞아요"라고 하면 신뢰한다. 1명만 물어보면(ONE) 빠르지만 잘못된 답을 줄 수 있고, 3명 모두(ALL) 물어보면 정확하지만 느리다.

---

## Ⅲ. 비교 및 연결

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) vs [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) 비교

| 비교 항목 | Apache [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | Apache [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) |
|:---|:---|:---|
| **아키텍처** | Masterless Ring | Master-Slave (HMaster + RegionServer) |
| **저장 기반** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템 ([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 자체) | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [분산 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/)) |
| **[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | Tunable (ONE/QUORUM/ALL) | Strong [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| **[단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)** | 없음 (완전 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) | HMaster 장애 시 HA 필요 |
| **[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)** | 매우 높음 | 높음 |
| **[Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 통합** | 제한적 | 완전 통합 ([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), Spark) |
| **SQL 지원** | CQL ([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) Query Language) | Phoenix (SQL on [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)) |
| **운영 복잡성** | 중간 | 높음 ([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)+[HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)+[ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)) |
| **적합 사례** | 24/7 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집약, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 타임라인 | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 에코시스템, 배치+실시간 혼합 |

### [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 설계 원칙

```
[좋은 파티션 키 설계]
사례: IoT 센서 시계열 데이터

❌ 나쁜 설계:
   파티션 키: sensor_id
   클러스터링 키: timestamp
   문제: 한 센서 데이터가 영원히 같은 파티션에 쌓임 → 파티션 크기 무한 증가

✅ 좋은 설계 (Bucket 전략):
   파티션 키: sensor_id + year_month (예: "IoT-001:2024-01")
   클러스터링 키: timestamp
   효과: 월별로 파티션 분리 → 파티션 크기 제어 + 시간 범위 쿼리 최적화
```

```cql
-- Cassandra CQL 예시
CREATE TABLE sensor_data (
    sensor_id TEXT,
    year_month TEXT,        -- 버킷 파티션
    event_time TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    PRIMARY KEY ((sensor_id, year_month), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- 최근 1시간 데이터 조회
SELECT * FROM sensor_data
WHERE sensor_id = 'IoT-001'
  AND year_month = '2024-01'
  AND event_time > '2024-01-15 09:00:00'
LIMIT 100;
```

📢 **섹션 요약 비유**: [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 버킷은 월별 서랍 정리다. 모든 이벤트를 하나의 서랍([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))에 넣으면 서랍이 꽉 차지만, 월별로 서랍을 나누면 각 서랍 크기가 적당하고 특정 월 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바로 꺼낼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 와이드 컬럼 적용 시나리오

```
[IoT 스마트 팩토리 아키텍처]
센서 1,000개 × 초당 100건 = 100,000 이벤트/초

Kafka 버퍼 → Flink 스트림 처리 → Cassandra (실시간 저장)
                                  → 파티션: sensor_id + date
                                  → 클러스터링: timestamp

Cassandra 적합 이유:
- 초당 10만+ 쓰기 처리 가능
- 24/7 무중단 (Masterless)
- 파티션 키 기반 초고속 범위 쿼리
- TTL로 오래된 데이터 자동 삭제
```

### [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | 적합 사례 |
|:---|:---|:---|
| **STCS (Size-Tiered)** | 비슷한 크기 SSTable 병합 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 중심, 시계열 |
| **[LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) (Leveled)** | 레벨별 고정 크기 SSTable | 읽기 중심, 디스크 사용 많음 |
| **TWCS (Time-Window)** | 시간 윈도우별 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 시계열 + [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 조합 최적 |

**기술사 핵심 판단**: [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 선택 이유를 "CAP에서 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택, Tunable [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)으로 유연한 트레이드오프, LSM-Tree로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화"로 논리화한다.

📢 **섹션 요약 비유**: LSM-Tree의 Compaction은 주기적인 책상 정리다. 바쁠 때는 일단 메모([MemTable](/knowledge-base/studynote/05_database/07_exam_summary/494_memtable_sstable_flush/))를 써놓고 나중에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(SSTable)로 정리한다. 백그라운드에서 여러 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 하나로 합치는([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 작업으로 책상이 깔끔하게 유지된다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **초당 수십만 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)** | [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)로 극한 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 달성 |
| **99.99% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)** | Masterless 아키텍처로 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 제거 |
| **선형 확장** | 노드 추가로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)·읽기 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 선형 증가 |
| **지리 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)** | Multi-DC 복제로 글로벌 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지원 |
| **자동 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 만료** | TTL로 시계열 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자동 삭제 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **[JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 불가** | 관계형 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴 지원 없음 |
| **전체 테이블 스캔 금지** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 없는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 AllowFiltering 필요 ([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극악) |
| **설계 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)** | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴에 맞게 테이블 설계 → [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 변경 시 테이블 재설계 |
| **[Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 부하** | 배경 Compaction이 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 간섭 |

📢 **섹션 요약 비유**: Cassandra는 "[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 천재, 읽기는 규칙 준수자"다. [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 무조건 빠르지만, 읽기는 반드시 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키(주소)를 알아야 한다. 주소를 모르면 전체 동(AllowFiltering)을 뒤지는 극악의 비효율이 발생한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)/[HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 자료구조 |
| [컨시스턴트 해싱](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) Ring에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 메커니즘 |
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택, Tunable [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| 시계열 DB | InfluxDB와 비교되는 시계열 저장 대안 |
| [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | Cassandra로의 대용량 이벤트 스트리밍 소스 |
| [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 에코시스템 통합형 와이드 컬럼 DB |
| [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | SSTable 병합을 통한 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |

### 👶 어린이를 위한 3줄 비유 설명
1. [와이드 컬럼 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/038_wide_column/)는 학교 출석부다. 날짜(행 키)마다 학생들의 출석 여부(컬럼)를 기록하는데, 학생 수가 아무리 많아도 여러 반(노드)으로 나눠 기록하면 빠르다.

### 📈 관련 키워드 및 발전 흐름도

```text
Wide-Column: 행 키 + 컬럼 패밀리 구조
    ├─► Cassandra: 고가용성 · 멀티 DC · 최종 일관성
    ├─► HBase: HDFS 기반 · 강한 일관성
    └─► Bigtable: Google 관리형 서비스
    │
    ▼
활용: IoT 시계열 · 로그 · 대규모 쓰기 워크로드
```
2. [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 칠판에 먼저 적고 나중에 공책에 옮기는 방식이다. 칠판 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(메모리)는 빠르고, 나중에 공책 정리(SSTable [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))는 순서대로 하니 효율적이다.
3. Cassandra의 Tunable Consistency는 투표 규칙이다. "1명만 찬성해도 통과"(빠름), "과반수 찬성해야 통과"(믿음직), "만장일치"(정확) 중 상황에 따라 고를 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 237 / 371

← **이전**: [237. 도큐먼트 저장소 (Document Store) - MongoDB / Elasticsearch](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/237_document_store_mongodb_elasticsearch/)
**다음**: [239. 그래프 데이터베이스 (Neo4j, AWS Neptune)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/239_graph_database_neo4j_neptune/) →

---
