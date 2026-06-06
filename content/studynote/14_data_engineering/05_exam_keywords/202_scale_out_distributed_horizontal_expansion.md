---
title: "202. Scale Out Distributed Horizontal Expansion"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스케일 아웃(Scale-Out)은 고성능 단일 서버를 키우는 대신, 저렴한 범용 서버를 수평으로 늘려 용량과 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 선형적으로 확장하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 패러다임이다.
> 2. **가치**: 빅데이터 환경에서 스케일 아웃은 수직 확장의 물리적 한계와 비용 폭증을 극복하고, 장애 허용([Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))과 탄력적 용량 조절(Elasticity)을 동시에 실현한다.
> 3. **판단 포인트**: 기술사 논술에서는 스케일 아웃 채택 시 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))의 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)-[가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 트레이드오프, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)기([Load Balancer](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/)) 설계를 반드시 논해야 한다.

---

## Ⅰ. 개요 및 필요성

### [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) ([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) vs 스케일 아웃 (Scale-Out) 등장 배경

전통적인 IT 시스템은 하드웨어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상(무어의 법칙)에 의존해 단일 서버를 업그레이드하는 [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 방식을 사용했다. 그러나 CPU 클럭 속도 정체(2000년대 중반 이후), 빅데이터의 페타바이트급 규모, 클라우드 컴퓨팅의 부상으로 범용 서버를 무한히 추가하는 스케일 아웃(Scale-Out)이 주류가 되었다.

| 배경 요인 | 내용 | 스케일 아웃 필요성 |
|:---|:---|:---|
| 무어의 법칙 정체 | CPU 단일 코어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 둔화 | 다수 코어·노드로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확보 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭증 | 페타바이트급 빅데이터 | 단일 서버 저장 용량 한계 초과 |
| 고가용성 요구 | 24/7 무중단 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 단일 서버 [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure) 제거 |
| 비용 효율성 | 클라우드 종량제 과금 | 필요한 만큼만 노드 추가 |

### 스케일 아웃의 핵심 원리

스케일 아웃은 공유 아무것도 없는(Shared-Nothing) 아키텍처를 기반으로 한다. 각 노드는 독립적인 CPU, 메모리, 스토리지를 가지며, 노드 간 통신은 네트워크를 통해서만 이루어진다.

```
스케일 아웃 구조
+-----------------------------------------------------+
|                   부하 분산기 (Load Balancer)         |
+---------+----------+----------+----------+----------+
          |          |          |          |
      +---v---+  +---v---+  +---v---+  +---v---+
      | Node1 |  | Node2 |  | Node3 |  | Node4 |
      | CPU   |  | CPU   |  | CPU   |  | CPU   |
      | MEM   |  | MEM   |  | MEM   |  | MEM   |
      | DISK  |  | DISK  |  | DISK  |  | DISK  |
      +-------+  +-------+  +-------+  +-------+
         ^ 노드 추가 시 선형 성능 향상 (이상적)
```

📢 **섹션 요약 비유**: [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)은 "혼자 더 많이 먹을 수 있게 위를 크게 하는 수술"이고, 스케일 아웃은 "친구를 더 불러서 나눠 먹는 것"이다. 수술은 한계가 있지만 친구는 계속 부를 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) vs 스케일 아웃 상세 비교

| 항목 | [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) ([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) | 스케일 아웃 (Scale-Out) |
|:---|:---|:---|
| 방향 | 수직 확장 (Vertical Scaling) | 수평 확장 (Horizontal Scaling) |
| 방법 | CPU·메모리·스토리지 업그레이드 | 동일 사양 서버 추가 |
| 비용 | 지수적 증가 (2배 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) = 4배 비용) | 선형 증가 (2배 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) = 2배 비용) |
| 한계 | 물리적 상한(최대 RAM, [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 수) | 이론상 무한 확장 가능 |
| 장애 내구성 | 단일 서버 [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | 노드 장애 시 나머지 노드로 대체 |
| 운영 복잡성 | 단순 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 조정(Coordination) 필요 |
| 적합 워크로드 | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) | 빅데이터, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리, 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

### 수평 확장의 핵심 기술

#### 1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Partitioning](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) / [Sharding](/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))

전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 노드에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/).

```
파티셔닝 전략
+-----------------------------------------------------+
|  전체 데이터셋 (100TB)                               |
|                                                     |
|  +--------+  +--------+  +--------+  +--------+    |
|  | 샤드 1  |  | 샤드 2  |  | 샤드 3  |  | 샤드 4  |    |
|  | 25TB   |  | 25TB   |  | 25TB   |  | 25TB   |    |
|  | 해시 0  |  | 해시 1  |  | 해시 2  |  | 해시 3  |    |
|  +--------+  +--------+  +--------+  +--------+    |
+-----------------------------------------------------+
```

| [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| 범위 (Range) | 키 범위로 분할 (A-G, H-N...) | 범위 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 효율적 | 핫스팟(Hot Spot) 위험 |
| 해시 (Hash) | 해시 함수로 균등 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 균등한 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 범위 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비효율 |
| 지리 (Geographic) | 지역별 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 레이턴시 최소화 | 재조합 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡 |

#### 2. [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 노드에 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하여 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 향상.

```
복제 아키텍처 (복제 계수 = 3)
+-----------------------------------------------------+
|                                                     |
|  +----------+    복제    +----------+               |
|  | Primary  |----------->| Replica1 |               |
|  |  Node    |           +----------+               |
|  +----------+                                       |
|       |         복제    +----------+               |
|       +---------------->| Replica2 |               |
|                         +----------+               |
+-----------------------------------------------------+
   쓰기: Primary만, 읽기: 세 노드 모두 처리 가능
```

#### 3. 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) ([Load Balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/))

```
L4/L7 부하 분산기 구조
                   +------------------+
  클라이언트 ------->|  Load Balancer   |
                   |  (라운드로빈/최소  |
                   |   연결/IP해시)    |
                   +--+---+---+---+--+
                      |   |   |   |
                   +--v-+ +v--+ +v--+ +v--+
                   |WS1 | |WS2| |WS3| |WS4|
                   +----+ +---+ +---+ +---+
```

📢 **섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 "도서관 책을 A~Z 선반에 나눠 꽂기", [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 "같은 책을 3층 각 열람실에 비치하기", 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 "어느 열람실에 안내할지 결정하는 안내 데스크"다.

---

## Ⅲ. 비교 및 연결

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)) 트레이드오프

브루어(Brewer)의 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>(<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a>)</strong>, <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>(<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong>, <strong><a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> 허용성(<a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> Tolerance)</strong> 중 동시에 2가지만 보장 가능.

```
CAP 트리앙글
              일관성 (Consistency)
                    △
                   /|\
                  / | \
                 /  |  \
                /   |   \
               / CA | CP  \
              /     |     \
             /______|______\
    가용성                   파티션
  (Availability)    AP    허용성
                         (Partition Tolerance)
```

| 유형 | 보장 특성 | 대표 시스템 | 빅데이터 적합성 |
|:---|:---|:---|:---|
| [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) + [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | RDBMS ([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 없을 때) | 소규모 단일 서버 |
| [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) + [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용 | [HBase](/studynote/05_database/04_transactions_concurrency/543_hbase/), [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 필요 시 |
| [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) + [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용 | [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | 대규모 빅데이터 ✅ |

### 스케일 아웃과 빅데이터 기술 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 연결

| 빅데이터 기술 | 스케일 아웃 방식 | 핵심 원리 |
|:---|:---|:---|
| [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | 블록 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) + 3중 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 블록(128MB) 단위 수평 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 기반 [RDD](/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 익스큐터(Executor) 수평 추가 |
| [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) + 리더/팔로워 | 토픽 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수평 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) | 일관된 해시링([Consistent Hashing](/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)) | 노드 추가 시 자동 리밸런싱 |
| [Elasticsearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) | 샤드 + 레플리카 | [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 샤드 수평 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |

📢 **섹션 요약 비유**: [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 트레이드오프는 "탈것 선택"이다. [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 정확도(오차 없는 GPS), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 연중무휴 운행, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용은 네트워크 단절 시 계속 운행. 비행기([CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))는 정확하지만 멈추고, 자동차([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))는 연중무휴지만 GPS가 가끔 틀린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 스케일 아웃 설계 시 핵심 고려사항

#### 1. 스테이트리스([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 설계 원칙

스케일 아웃이 효과적이려면 각 노드가 독립적으로 요청을 처리할 수 있는 무상태([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 설계가 필수다.

```
Stateful vs Stateless
+-----------------------------------------------------+
|  Stateful (문제):                                    |
|  Client ---> Server1 (세션 A 보유)                    |
|  Client ---> Server2 (세션 A 없음!) -> 오류 발생        |
|                                                     |
|  Stateless (해결):                                   |
|  Client ---> (JWT 토큰 포함) ---> Server1 또는 Server2  |
|  모든 서버가 토큰으로 자체 검증 -> 어디든 OK            |
+-----------------------------------------------------+
```

#### 2. 실무 적용 사례: 전자상거래 플랫폼

| 레이어 | 스케일 아웃 방법 | 효과 |
|:---|:---|:---|
| 웹 서버 | Nginx 로드밸런서 + 10대 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버 | 동시 접속 10만 -> 100만 처리 |
| 캐시 레이어 | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster ([샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 16384 슬롯) | 읽기 응답시간 50ms -> 2ms |
| [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) | MySQL 읽기 레플리카 5대 | 읽기 부하 80% [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| 빅데이터 처리 | Spark 클러스터 50 Executor | 일 1TB 집계 처리 2시간 -> 10분 |

#### 3. 기술사 판단 포인트

- <strong><a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a> 키 선택</strong>: 핫스팟 방지를 위해 카디널리티(Cardinality)가 높은 컬럼 선택 필수
- **재조정(Resharding) 비용**: 노드 추가 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재분배 다운타임 최소화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필요 ([일관된 해싱](/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) 사용)
- **네트워크 병목**: 스케일 아웃 시 노드 간 통신(셔플, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))이 병목이 될 수 있음. 10GbE 또는 [InfiniBand](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 활용

📢 **섹션 요약 비유**: 스케일 아웃은 배달 앱 운영과 같다. 주문이 늘어나면 배달 기사를 더 고용(수평 확장)하면 되지만, 모든 기사가 공통 창고(공유 상태)를 사용하면 창고에서 병목이 생긴다. 각 기사가 독립적으로 출발할 수 있어야([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 진정한 스케일 아웃이 된다.

---

## Ⅴ. 기대효과 및 결론

### 스케일 아웃 도입 효과

| 효과 영역 | 수치 사례 | 설명 |
|:---|:---|:---|
| 비용 절감 | 70% 비용 절감 | 고가 서버 1대 -> 범용 서버 10대 |
| [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상 | 99.99% [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | N+1 리던던시로 노드 장애 무영향 |
| 확장 유연성 | 분 단위 노드 추가 | 클라우드 [Auto Scaling](/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) 연동 |
| [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상 | 선형적 TPS 증가 | 노드 2배 = [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 약 2배 |

### 한계 및 극복 방안

| 한계 | 원인 | 극복 방안 |
|:---|:---|:---|
| 운영 복잡성 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 디버깅 어려움 | [분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/)(Jaeger, Zipkin) |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 약화 | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Replication Lag](/studynote/05_database/04_transactions_concurrency/556_master_slave_replication_lag_inconsistency/)) | 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모드(Quorum 읽기) |
| 핫스팟 문제 | 불균등 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | [일관된 해싱](/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/), 가상 노드(Vnode) |
| 네트워크 비용 | 노드 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 | [데이터 지역성](/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/studynote/14_data_engineering/01_infrastructure/019_data_locality/)) 최적화 |

### 결론

스케일 아웃은 빅데이터 시대의 핵심 인프라 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 무한 확장성과 비용 효율성이라는 장점은 있지만, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 복잡성과 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 트레이드오프라는 대가를 치러야 한다. 기술사 관점에서는 "왜 스케일 아웃인가"뿐만 아니라 "어떤 조건에서 [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)이 더 적합한가"도 균형 있게 서술해야 한다.

📢 **섹션 요약 비유**: 스케일 아웃은 "체인 레스토랑 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)"이다. 한 매장을 고급화하기보다 동네마다 표준화된 지점을 내는 것. 관리는 더 복잡해지지만, 한 지점이 문 닫아도 전체 영업은 계속되고 수요에 따라 지점을 빠르게 늘리거나 줄일 수 있다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 대비 개념 | [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) ([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) | 수직 확장, 단일 서버 고사양화 |
| 기반 개념 | Shared-Nothing 아키텍처 | 노드 간 자원 비공유 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 설계 |
| 이론적 근거 | [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)-[가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 트레이드오프 |
| 핵심 기술 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) / [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 노드에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장 |
| 핵심 기술 | 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) ([Load Balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/)) | 요청을 여러 노드에 균등 분배 |
| 응용 기술 | [Auto Scaling](/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) | 부하에 따른 자동 노드 추가/제거 |
| 연관 기술 | [일관된 해싱](/studynote/05_database/05_distributed_nosql_newsql/283_reference_pattern/) ([Consistent Hashing](/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/)) | 노드 추가/제거 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재배치 최소화 |

### 👶 어린이를 위한 3줄 비유 설명
1. [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)은 "한 명의 요리사를 슈퍼 셰프로 만들기"고, 스케일 아웃은 "평범한 요리사를 100명 고용하기"예요.

### 📈 관련 키워드 및 발전 흐름도

```text
단일 서버 (Scale-Up: CPU·RAM 증설)
    | 물리적 한계
    v
Scale-Out: 수평 분산 (노드 추가)
    +-► 데이터 샤딩 · 파티셔닝
    +-► 로드 밸런싱 · 장애 격리
    +-► Shared-Nothing 아키텍처
    |
    v
클라우드 오토스케일링: K8s · Auto Scaling Group
```
2. 슈퍼 셰프는 한 명이라 몸이 아프면 레스토랑 전체가 멈추지만, 100명 중 한 명이 아파도 나머지 99명이 계속 요리해요.
3. 그래서 빅데이터처럼 엄청난 주문이 오는 곳에서는 "평범한 요리사 100명 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)"인 스케일 아웃을 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 202 / 258

<- **이전**: [201. 빅데이터 3V·5V 특성 (Big Data 3V·5V Characteristics)](/studynote/14_data_engineering/05_exam_keywords/201_bigdata_3v_5v_volume_velocity_variety/)
**다음**: [203. 하둡 HDFS (Hadoop Distributed File System) 블록 복제 내결함성](/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/) ->

---
