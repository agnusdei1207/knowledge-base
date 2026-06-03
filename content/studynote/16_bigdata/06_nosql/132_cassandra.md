+++
title = "132. Apache Cassandra — 마스터 없는 링 구조 분산 데이터베이스"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: Cassandra는 모든 노드가 동등한 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스(Masterless) 피어 링 토폴로지를 통해 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 없이 노드 추가만으로 선형적 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확장을 실현하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)다.
- **가치**: 튜너블 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(Tunable [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))으로 ONE~ALL까지 연산별로 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)-[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 트레이드오프를 조정할 수 있어, [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 글로벌 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 99.999% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 달성한다.
- **판단 포인트**: [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 항상 빠르지만(O(1) Commit Log), 읽기는 SSTable 수에 비례하므로 [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(STCS/[LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)/TWCS) 선택이 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 관건이다.

---

## Ⅰ. 개요 및 필요성

### Facebook의 받은 편지함 문제
2007년 Facebook은 수십억 개의 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 모든 사용자에게 실시간으로 제공해야 했다. RDBMS는 단일 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 구조로 수직 확장의 한계에 부딪혔고, Amazon의 Dynamo 논문([P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/), [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))과 Google의 Bigtable 논문(컬럼 구조)을 결합해 Cassandra를 개발했다.

### 핵심 설계 원칙

| 원칙 | 설명 |
|:---:|:---|
| **[마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스** | 모든 노드가 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 가능, [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 없음 |
| **[일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/)** | [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 노드에 균등 분배 |
| **튜너블 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | 연산별로 ONE~ALL [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 가능 |
| **[결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)** | 기본값 QUORUM, 최종적으로 모든 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| **[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화** | Sequential Append → 디스크 최적화 |

📢 **섹션 요약 비유**
> Cassandra는 선생님([마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터) 없이 모든 학생이 자료를 서로 공유하는 스터디 그룹과 같다. 한 명이 빠져도 나머지가 계속 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)할 수 있고, 인원이 늘어날수록 처리할 수 있는 자료량도 그만큼 늘어난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) ([Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)) [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)

```text
┌──────────────────────────────────────────────────────────────┐
│         Cassandra 토큰 링 (Token Ring)                        │
│                                                              │
│  토큰 범위: -2^63 ~ +2^63 (가상 노드 vnodes 사용 시 세분화)     │
│                                                              │
│               Node A (tokens: 0~25)                          │
│              ╱                    ╲                          │
│  Node E    ●    RF=3 예시:          ●   Node B               │
│ (76~100)   │    key "user:1"        │   (26~50)              │
│            │    → hash → 42        │                         │
│            │    → Node B, C, D     │                         │
│  Node D  ●                           ●  Node C               │
│  (51~75)    ╲                    ╱   (26~50 이후)             │
│              (시계 방향으로 RF개 노드)                          │
│                                                              │
│  Vnodes(가상 노드): 각 물리 노드가 여러 토큰 범위를 담당        │
│  → 노드 추가/제거 시 부하 분산 자동화                          │
└──────────────────────────────────────────────────────────────┘
```

### 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로 상세

```text
┌──────────────────────────────────────────────────────────┐
│                  Cassandra 쓰기 경로                       │
│                                                          │
│  Client → 코디네이터 노드 → 복제 노드들                     │
│                                                          │
│  각 복제 노드에서:                                         │
│  1. Commit Log 기록 (내구성, Sequential I/O)              │
│  2. MemTable 업데이트 (인메모리 정렬 구조)                  │
│  3. MemTable 임계값 도달 → SSTable Flush                  │
│  4. Bloom Filter, Index Summary 업데이트                  │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│                  Cassandra 읽기 경로                 │    │
│  └─────────────────────────────────────────────────┘    │
│  Client → 코디네이터 → 복제 노드 중 1개(or QUORUM)        │
│                                                          │
│  복제 노드에서:                                           │
│  1. MemTable 검색 (최신 데이터)                           │
│  2. Bloom Filter 확인 (SSTable에 키 존재 여부 빠른 확인)    │
│  3. Key Cache → Row Cache 확인                           │
│  4. SSTable 검색 (최신순, 병합 필요 시 Read Repair)        │
└──────────────────────────────────────────────────────────┘
```

### CQL ([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) Query Language) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)

```sql
-- 시계열 IoT 센서 테이블 예시
CREATE TABLE sensor_readings (
    sensor_id   UUID,
    reading_time TIMESTAMP,
    temperature  DOUBLE,
    humidity     DOUBLE,
    PRIMARY KEY ((sensor_id), reading_time)
) WITH CLUSTERING ORDER BY (reading_time DESC)
  AND default_time_to_live = 2592000;  -- 30일 자동 만료

-- 삽입 (자동으로 올바른 노드로 라우팅)
INSERT INTO sensor_readings (sensor_id, reading_time, temperature)
VALUES (uuid(), toTimestamp(now()), 23.5);

-- 최근 24시간 데이터 조회
SELECT * FROM sensor_readings
WHERE sensor_id = ? AND reading_time > ?
LIMIT 1000;
```

### RF ([Replication Factor](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))와 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수식

```text
N = 노드 수 (RF = 복제 수)
W = 쓰기 확인 노드 수
R = 읽기 확인 노드 수

강한 일관성 조건: W + R > N

예시 (RF=3):
  W=2, R=2 → 2+2=4 > 3 → 강한 일관성 ✓ (QUORUM+QUORUM)
  W=1, R=1 → 1+1=2 < 3 → 결과적 일관성 (ONE+ONE)
  W=3, R=1 → 3+1=4 > 3 → 강한 일관성 ✓ (ALL+ONE)
```

📢 **섹션 요약 비유**
> Cassandra의 QUORUM [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 "3명의 증인 중 2명이 서명하면 계약 성립"과 같다. 1명이 자리를 비워도 나머지 2명으로 계약을 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)할 수 있고, 읽을 때도 2명에게 물어 최신 서명을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 충분히 신뢰할 수 있다.

---

## Ⅲ. 비교 및 연결

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) vs [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) vs [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/)

| 비교 항목 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) |
|:---:|:---:|:---:|:---:|
| 배포 형태 | 자체 운영/클라우드 | AWS 완전 관리형 | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 튜너블 | 선택(Eventual/Strong) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 | 없음([P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/)) | 없음(관리형) | HMaster 있음 |
| [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) | 내장(다중 DC) | Global Tables | 복잡 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | CQL (SQL 유사) | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| 비용 모델 | 노드 기반 | 요청 단위 과금 | 클러스터 비용 |

### [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [Anti-Patterns](/knowledge-base/studynote/11_design_supervision/06_exam_summary/403_architecture/) (피해야 할 패턴)

```text
❌ 1. ALLOW FILTERING 사용
   → 파티션 키 없는 전체 스캔 → 클러스터 전체 부하

❌ 2. 매우 큰 파티션 (>100MB)
   → 읽기 타임아웃, GC 압박, 핫 노드

❌ 3. 무한 증가 컬렉션 (Set/List/Map)
   → 단일 파티션에 수백만 아이템 → 대형 파티션과 동일 문제

❌ 4. 높은 삭제 비율 + 낮은 TTL
   → Tombstone 폭발 → 읽기 성능 급락
```

📢 **섹션 요약 비유**
> Cassandra와 HBase의 차이는 자율 관리 아파트 단지([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/))와 관리사무소가 있는 아파트([HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/))의 차이다. 자율 관리는 관리사무소가 없어도 주민들이 자체적으로 운영하지만, 관리사무소가 있으면 더 강력한 규칙(강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 적용이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터 인식 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```text
NetworkTopologyStrategy 사용 (멀티 DC):

CREATE KEYSPACE myapp
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc_seoul': 3,    -- 서울 DC에 3개 복제본
  'dc_busan': 2     -- 부산 DR에 2개 복제본
};

LOCAL_QUORUM: 서울 DC 내에서만 QUORUM → 네트워크 지연 최소화
EACH_QUORUM: 모든 DC에서 QUORUM → 최고 일관성 (느림)
```

### 운영 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 항목 | 권장값 | 이유 |
|:---:|:---:|:---|
| 최소 노드 수 | RF × 2 이상 | 유지보수 중에도 QUORUM 보장 |
| 힙 메모리 | 최대 32GB | GC 압박 최소화 |
| [Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | TWCS(시계열), [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)(읽기 집중) | 워크로드 특성 매칭 |
| vnodes 수 | 8~16개 | 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) + 이동 비용 균형 |
| [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [Tombstone](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/) 경고 | 1만 이상 시 즉시 조사 |

📢 **섹션 요약 비유**
> [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 운영에서 Tombstone은 묘지 표시와 같다. 너무 많이 쌓이면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽으러 가는 길에 묘지 표시를 수십만 개 넘어가야 해서 속도가 급격히 떨어진다. 주기적인 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 Compaction으로 청소해야 한다.

---

## Ⅴ. 기대효과 및 결론

### Netflix의 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 도입 사례

```text
도입 전: Oracle RAC → 단일 마스터, 수직 확장 한계
도입 후: Cassandra 수백 노드
  - 쓰기: 초당 수백만 건(뷰 이력, 재생 상태)
  - 가용성: 99.999% (5-nines)
  - 리전: 멀티 AWS 리전 복제
  - 결과: RDBMS 대비 10배 이상 저렴한 비용으로 100배 처리량
```

### 결론
Cassandra는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중, 고가용성, [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/)이 필요한 대규모 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 표준 선택지가 되었다. 기술사 시험에서는 **[마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터리스 링 구조의 동작 원리**, **RF·W·R 조합과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 수식**, **[Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)별 적합 워크로드**, **CQL Primary [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 설계**가 핵심 논점이다.

📢 **섹션 요약 비유**
> Cassandra는 24시간 편의점 체인과 같다. 어느 지점(노드)에서든 물건을 사고 팔 수 있고, 한 지점이 문을 닫아도 다른 지점들이 운영을 이어간다. 인기 상품([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 여러 지점에 미리 재고를 쌓아두어 어느 지점에서든 즉시 구할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| [일관된 해싱](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)으로 노드 할당 |
| Gossip [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 클러스터 관리 | 노드 상태 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 전파 |
| [Bloom Filter](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) | 읽기 최적화 | SSTable 존재 여부 빠른 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| Read Repair | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 | 읽기 시 오래된 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 자동 갱신 |
| Anti-[Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) | 백그라운드 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 주기적 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 비교·수정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 DB (RDBMS) — 스키마 고정, 수직 확장 한계]
    │
    ▼
[NoSQL — 유연한 스키마, 수평 확장 지향]
    │
    ▼
[Cassandra — 분산 와이드 컬럼 스토어, 고가용성 설계]
    │
    ▼
[Consistent Hashing — 노드 추가 시 최소 리밸런싱 데이터 분산]
    │
    ▼
[쓰기 최적화 (Write-Optimized) — LSM 트리 기반 고처리량 쓰기]
    │
    ▼
[멀티 마스터 복제 (Multi-Master) — 전역 분산 액티브-액티브 구성]
```
Cassandra는 단일 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 RDBMS의 확장 한계를 극복하기 위해 설계된 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 와이드 컬럼 스토어로, [멀티 마스터 복제](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/272_multi_master_replication/)와 LSM 트리로 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 실현한다.

### 👶 어린이를 위한 3줄 비유 설명
1. Cassandra는 원형으로 앉은 친구들이 서로 노트를 돌려보는 스터디 모임 — 선생님 없이도 모두가 같은 내용을 갖게 돼요.
2. RF=3이면 노트를 3개 복사해서 서로 다른 친구에게 맡기는 것 — 한 친구가 결석해도 나머지에게 물어볼 수 있어요.
3. Compaction은 주기적인 방 정리 — 쓰레기(삭제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 쌓이면 필요한 물건(진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 찾는 데 시간이 오래 걸리니까요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 262

← **이전**: [131. 컬럼 패밀리 데이터베이스 (Column Family DB) — Cassandra/HBase/ScyllaDB](/knowledge-base/studynote/16_bigdata/06_nosql/131_column_family_db/)
**다음**: [133. 그래프 데이터베이스 (Graph DB) — Neo4j/Amazon Neptune/Memgraph](/knowledge-base/studynote/16_bigdata/06_nosql/133_graph_db/) →

---
