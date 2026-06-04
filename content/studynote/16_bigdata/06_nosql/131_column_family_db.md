+++
title = "131. 컬럼 패밀리 데이터베이스 (Column Family DB) — Cassandra/HBase/ScyllaDB"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: 컬럼 패밀리(Wide-Column) DB는 행마다 다른 컬럼을 가질 수 있는 스파스(Sparse) 2차원 맵 구조로, 수십억 개의 컬럼과 행을 효율적으로 저장하는 대규모 시계열·이벤트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 최적화된 모델이다.
- **가치**: 시간 기반(Time-series) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 피드처럼 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 압도적으로 많고 특정 컬럼 범위를 자주 스캔하는 워크로드에서 RDBMS 대비 수십 배 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 제공한다.
- **판단 포인트**: HBase는 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 필요할 때([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 기반), Cassandra는 다중 리전 고가용성이 우선일 때([마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스), ScyllaDB는 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지하면서 하드웨어 비용을 줄일 때 선택한다.

---

## Ⅰ. 개요 및 필요성

### 등장 배경: Big Table에서 시작
2006년 Google이 발표한 BigTable 논문이 기반. 행·컬럼·타임스탬프의 3차원 맵 구조로 페타바이트급 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 아이디어를 제시했다. [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 기반 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/))와 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)(Facebook 개발, [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 기반)가 이를 계승했다.

### RDBMS vs 컬럼 패밀리 DB 저장 구조 차이

```text
+-----------------------------------------------------+
|     RDBMS (행 기반 저장): 모든 컬럼 고정              |
+--------+------+------+------+------+------+--------+
| Row ID | col1 | col2 | col3 | col4 | col5 | col6   |
+--------+------+------+------+------+------+--------+
| user:1 | 홍길동| 20   | NULL | NULL | NULL | NULL   |
| user:2 | 이몽룡| 22   | 서울 | NULL | NULL | NULL   |
+--------+------+------+------+------+------+--------+

+-----------------------------------------------------+
|  Wide-Column DB (스파스 저장): 있는 컬럼만 저장       |
|                                                     |
|  Row Key: "user:1"                                  |
|  +-- CF: profile -> { name:"홍길동", age:20 }         |
|  +-- CF: activity -> { login:"2026-04", views:42 }   |
|                                                     |
|  Row Key: "user:2"                                  |
|  +-- CF: profile -> { name:"이몽룡", age:22, city:"서울" }
|  +-- CF: activity -> { login:"2026-04" }             |
|  +-- CF: purchase -> { item1:"A",item2:"B" }         |
|                                                     |
|  * NULL 컬럼 저장 불필요 -> 스토리지 효율 극대화        |
+-----------------------------------------------------+
```

### 대표 솔루션 비교

| 항목 | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | ScyllaDB |
|:---:|:---:|:---:|:---:|
| 기반 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) + [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 링 | C++ 재구현 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 조정 가능 | 조정 가능 |
| [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 | Master 존재 | [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스 | [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스 |
| 확장성 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 의존 | 독립 확장 | 독립 확장 |
| GC 영향 | Java GC 문제 | Java GC 문제 | 없음(C++) |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | CQL | CQL 호환 |

📢 **섹션 요약 비유**
> 컬럼 패밀리 DB는 체크인 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)와 같다. 항공사마다(컬럼 패밀리) 필요한 서류(컬럼)가 다르고, 출국 승객(행)마다 제출하는 서류도 다르다. 없는 서류를 비워놓지 않고 제출한 것만 기록하니 공간이 훨씬 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) 아키텍처

```text
+----------------------------------------------------------+
|                   HBase 아키텍처                          |
|                                                          |
|  +----------------------------------------------------+  |
|  |              HMaster                              |  |
|  |  - Region 할당 관리         - DDL 처리             |  |
|  |  - Region Server 모니터링   - 부하 분산             |  |
|  +----------------------------------------------------+  |
|                        | ZooKeeper 코디네이션             |
|  +--------------+  +--------------+  +--------------+   |
|  |RegionServer 1|  |RegionServer 2|  |RegionServer 3|   |
|  | Region A     |  | Region B     |  | Region C     |   |
|  | Region D     |  | Region E     |  | Region F     |   |
|  +--------------+  +--------------+  +--------------+   |
|                        |                                 |
|  +-----------------------------------------------------+ |
|  |           HDFS (Hadoop Distributed File System)     | |
|  |  HFile(SSTable) 영구 저장, 3중 복제                  | |
|  +-----------------------------------------------------+ |
+----------------------------------------------------------+
```

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 링 구조

```text
+------------------------------------------------------+
|           Cassandra 마스터리스 링 토폴로지               |
|                                                      |
|              Node 1 (token: 0)                       |
|             ╱         ╲                              |
|  Node 5   ●             ●   Node 2                   |
| (token:   |   동등한     |   (token:                  |
|  2^126)   |   피어들     |    2^30)                   |
|            ●             ●                           |
|  Node 4 (token:2^94)  Node 3(token:2^62)             |
|                                                      |
|  * 모든 노드가 동등(피어) -> 단일 장애점(SPOF) 없음       |
|  * RF=3: 데이터는 일관된 해싱으로 결정된 3개 노드에 저장  |
|  * Gossip Protocol: 노드 상태 P2P 전파               |
+------------------------------------------------------+
```

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로 (Write Path)

```text
클라이언트 Write 요청
        |
        v
+--------------+
|  Commit Log  | <- 내구성 보장 (Sequential Write)
+--------------+
        |
        v
+--------------+
|  MemTable    | <- 인메모리 정렬 구조
+--------------+
        | (임계값 도달 시 Flush)
        v
+--------------+
|   SSTable    | <- 불변(Immutable) 디스크 파일
+--------------+
        |
        v (주기적 Compaction)
+--------------+
| 병합된 SSTable| <- 공간 회수 + 성능 최적화
+--------------+
```

### [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | 적합 워크로드 |
|:---:|:---|:---:|
| **STCS** (SizeTiered [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | 비슷한 크기 SSTable 병합 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/">LCS</a></strong> (Leveled [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | 레벨별 정렬 유지 | 읽기 집중 |
| **TWCS** (TimeWindow [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | 시간 윈도우별 병합 | 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

📢 **섹션 요약 비유**
> Cassandra의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로는 편의점 재고 관리와 같다. 판매 즉시 영수증(Commit Log)을 끊고, 진열대([MemTable](/knowledge-base/studynote/05_database/07_exam_summary/494_memtable_sstable_flush/))에 임시 표시한 뒤, 밤마다 창고(SSTable)로 정리한다. 창고가 복잡해지면 주기적으로 재정리([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))하여 공간을 확보한다.

---

## Ⅲ. 비교 및 연결

### 튜너블 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Tunable [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))

| [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) Level | 읽기 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 보장 수준 |
|:---:|:---:|:---:|:---:|
| ONE | 1 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 응답 | 1 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 최저 (빠름) |
| QUORUM | 과반수 응답 | 과반수 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 중간 (권장) |
| LOCAL_QUORUM | 로컬 DC 과반수 | 로컬 DC 과반수 | [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 최적 |
| ALL | 전체 응답 | 전체 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 최고 (느림) |

> QUORUM + QUORUM = 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (W + R > N: 2Q > RF)

### ScyllaDB의 차별화

```text
Java Cassandra -> GC 일시 정지(Stop-the-World)
                 100ms~수초 스파이크

C++ ScyllaDB  -> GC 없음, 코어별 CPU 친화성
                p99 지연 10배 이상 개선
                같은 워크로드를 1/5~1/10 노드로 처리
```

📢 **섹션 요약 비유**
> QUORUM [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 과반수 투표와 같다. 5개 노드 중 3개가 "OK"하면 정상으로 인정한다. 한두 노드가 느리거나 다운되어도 과반수가 살아있으면 계속 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)할 수 있어, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 사이의 균형점이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링: [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 우선 설계

```text
❌ 잘못된 접근: 엔티티 관계 우선 설계
   (후에 필요한 쿼리에 맞게 복잡한 JOIN -> CQL에서 불가)

✅ 올바른 접근: 쿼리 패턴 우선 설계
   1. "어떤 쿼리로 데이터를 읽을 것인가?" 정의
   2. 그 쿼리를 위한 파티션 키 + 클러스터링 키 결정
   3. 쿼리당 1개 테이블 원칙 (Query-per-table)

예: "사용자별 최근 100개 주문 시간 역순 조회"
   -> PRIMARY KEY ((user_id), order_time)
      WITH CLUSTERING ORDER BY (order_time DESC)
```

### [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 설계 주의사항

| 문제 | 증상 | 해결책 |
|:---:|:---:|:---|
| 핫 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 특정 노드 CPU/IO 급증 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키에 버킷(bucket) 추가 |
| 대형 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 읽기 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), GC 압박 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 크기 < 100MB 유지 |
| 하나의 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키만 | 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 한 노드 | 복합 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 설계 |

📢 **섹션 요약 비유**
> [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링은 슈퍼마켓 진열 계획과 같다. 손님이 "우유"를 찾을 것인지 "아침 식재료"를 한번에 찾을 것인지 먼저 알아야 어느 통로([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키)에 무엇을 진열할지 결정할 수 있다. 모든 상품을 한 통로에 몰아넣으면(핫 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 그 통로만 항상 막히게 된다.

---

## Ⅴ. 기대효과 및 결론

### 적합 사용 사례 요약

| 사용 사례 | 추천 솔루션 | 이유 |
|:---:|:---:|:---|
| [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 시계열 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) + TWCS | 시간 기반 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중, 자동 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) |
| 실시간 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 저장 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) |
| [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 기반 분석 | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 통합, [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 연계 |
| 비용 효율 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | ScyllaDB | 노드 수 1/5, 동일 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| 사용자 활동 피드 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화, 시간 역순 조회 |

### 결론
컬럼 패밀리 DB는 시계열·이벤트 중심의 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 타 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델보다 압도적인 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공한다. 기술사 시험에서는 <strong>Cassandra의 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/">마스</a>터리스 링 구조와 튜너블 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong>, <strong>HBase의 <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">ZooKeeper</a> 기반 강한 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 메커니즘</strong>, <strong>TWCS <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>의 시계열 최적화 원리</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> 컬럼 패밀리 DB는 거대한 실시간 기록 시스템이다. 초당 수백만 개의 센서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 끊임없이 기록하면서도, "지난 1시간 온도 변화"를 즉시 조회할 수 있다. 마치 CCTV가 24시간 녹화하면서도 특정 시간대 영상을 바로 재생할 수 있는 것처럼.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| BigTable | 이론적 기원 | Google의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컬럼 저장소 논문 |
| SSTable | 저장 구조 | Sorted String Table, 불변 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 유지 관리 | SSTable 병합, 삭제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제거 |
| Gossip [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 클러스터 관리 | 노드 간 상태 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 전파 |
| [Tombstone](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/) | 삭제 마커 | 삭제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표시, [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 시 제거 |

### 📈 관련 키워드 및 발전 흐름도

```text
[RDBMS 행 기반 저장]
    |
    v
[와이드 컬럼 필요성]
    |
    v
[컬럼 패밀리 DB(HBase/Cassandra)]
    |
    v
[SSTable/LSM 트리]
    |
    v
[시계열/IoT 응용]
```

컬럼 패밀리 DB는 행 기반 RDBMS의 한계를 넘어 LSM 트리와 wide-column 저장으로 확장된다.

### 👶 어린이를 위한 3줄 비유 설명
1. 컬럼 패밀리 DB는 학생마다 필요한 칸이 다른 성적표 — 미술반 학생에게는 실기 칸이 있고, 수학반 학생에게는 없어도 괜찮아요.
2. Cassandra는 원형으로 앉은 친구들이 서로 소식을 전달하는 릴레이 게임 — 선생님([마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터) 없이도 모두가 같은 정보를 갖게 돼요.
3. Compaction은 방 정리와 같아요. 쓰다 버린 메모(삭제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 주기적으로 청소해서 서랍(디스크)을 깨끗하게 유지해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 262

<- **이전**: [130. MongoDB 아키텍처 — ReplicaSet/Sharding/Mongos](/knowledge-base/studynote/16_bigdata/06_nosql/130_mongodb_architecture/)
**다음**: [132. Apache Cassandra — 마스터 없는 링 구조 분산 데이터베이스](/knowledge-base/studynote/16_bigdata/06_nosql/132_cassandra/) ->

---
