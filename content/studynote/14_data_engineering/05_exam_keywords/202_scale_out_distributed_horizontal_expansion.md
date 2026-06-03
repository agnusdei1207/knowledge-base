---
title: 202. 스케일 아웃 (Scale-Out) 분산 수평 확장
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스케일 아웃(Scale-Out)은 고성능 단일 서버를 키우는 대신, 저렴한 범용 서버를 수평으로 늘려 용량과 [[139_throughput|처리량]]을 선형적으로 확장하는 [[136_variance|분산]] 컴퓨팅 패러다임이다.
> 2. **가치**: 빅데이터 환경에서 스케일 아웃은 수직 확장의 물리적 한계와 비용 폭증을 극복하고, 장애 허용([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])과 탄력적 용량 조절(Elasticity)을 동시에 실현한다.
> 3. **판단 포인트**: 기술사 논술에서는 스케일 아웃 채택 시 [[341_process|CAP]] 정리([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]])의 [[194_consistency_database_integrity|일관성]]-[[452_availability|가용성]] 트레이드오프, [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]], 부하 [[136_variance|분산]]기([[031_load_balancer|Load Balancer]]) 설계를 반드시 논해야 한다.

---

## Ⅰ. 개요 및 필요성

### [[621_scale_up_system_bus|스케일 업]] ([[621_scale_up_system_bus|Scale-Up]]) vs 스케일 아웃 (Scale-Out) 등장 배경

전통적인 IT 시스템은 하드웨어 [[282_performance_tactics|성능]] 향상(무어의 법칙)에 의존해 단일 서버를 업그레이드하는 [[621_scale_up_system_bus|스케일 업]]([[621_scale_up_system_bus|Scale-Up]]) 방식을 사용했다. 그러나 CPU 클럭 속도 정체(2000년대 중반 이후), 빅데이터의 페타바이트급 규모, 클라우드 컴퓨팅의 부상으로 범용 서버를 무한히 추가하는 스케일 아웃(Scale-Out)이 주류가 되었다.

| 배경 요인 | 내용 | 스케일 아웃 필요성 |
|:---|:---|:---|
| 무어의 법칙 정체 | CPU 단일 코어 [[282_performance_tactics|성능]] 향상 둔화 | 다수 코어·노드로 [[282_performance_tactics|성능]] 확보 |
| [[001_dikw_pyramid|데이터]] 폭증 | 페타바이트급 빅데이터 | 단일 서버 저장 용량 한계 초과 |
| 고가용성 요구 | 24/7 무중단 [[090_service_kubernetes_network_load_balancing|서비스]] | 단일 서버 [[454_spof|SPOF]] (Single Point of Failure) 제거 |
| 비용 효율성 | 클라우드 종량제 과금 | 필요한 만큼만 노드 추가 |

### 스케일 아웃의 핵심 원리

스케일 아웃은 공유 아무것도 없는(Shared-Nothing) 아키텍처를 기반으로 한다. 각 노드는 독립적인 CPU, 메모리, 스토리지를 가지며, 노드 간 통신은 네트워크를 통해서만 이루어진다.

```
스케일 아웃 구조
┌─────────────────────────────────────────────────────┐
│                   부하 분산기 (Load Balancer)         │
└─────────┬──────────┬──────────┬──────────┬──────────┘
          │          │          │          │
      ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐
      │ Node1 │  │ Node2 │  │ Node3 │  │ Node4 │
      │ CPU   │  │ CPU   │  │ CPU   │  │ CPU   │
      │ MEM   │  │ MEM   │  │ MEM   │  │ MEM   │
      │ DISK  │  │ DISK  │  │ DISK  │  │ DISK  │
      └───────┘  └───────┘  └───────┘  └───────┘
         ↑ 노드 추가 시 선형 성능 향상 (이상적)
```

📢 **섹션 요약 비유**: [[621_scale_up_system_bus|스케일 업]]은 "혼자 더 많이 먹을 수 있게 위를 크게 하는 수술"이고, 스케일 아웃은 "친구를 더 불러서 나눠 먹는 것"이다. 수술은 한계가 있지만 친구는 계속 부를 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[621_scale_up_system_bus|스케일 업]] vs 스케일 아웃 상세 비교

| 항목 | [[621_scale_up_system_bus|스케일 업]] ([[621_scale_up_system_bus|Scale-Up]]) | 스케일 아웃 (Scale-Out) |
|:---|:---|:---|
| 방향 | 수직 확장 (Vertical Scaling) | 수평 확장 (Horizontal Scaling) |
| 방법 | CPU·메모리·스토리지 업그레이드 | 동일 사양 서버 추가 |
| 비용 | 지수적 증가 (2배 [[282_performance_tactics|성능]] = 4배 비용) | 선형 증가 (2배 [[282_performance_tactics|성능]] = 2배 비용) |
| 한계 | 물리적 상한(최대 RAM, [[125_socket|소켓]] 수) | 이론상 무한 확장 가능 |
| 장애 내구성 | 단일 서버 [[454_spof|SPOF]] | 노드 장애 시 나머지 노드로 대체 |
| 운영 복잡성 | 단순 | [[136_variance|분산]] 조정(Coordination) 필요 |
| 적합 워크로드 | [[327_hint_handoff|OLTP]] (Online [[191_transaction_concept_states|Transaction]] Processing) | 빅데이터, [[136_variance|분산]] 처리, 웹 [[090_service_kubernetes_network_load_balancing|서비스]] |

### 수평 확장의 핵심 기술

#### 1. [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]] ([[001_dikw_pyramid|Data]] [[179_table_partitioning_concept|Partitioning]] / [[243_sharding_horizontal_scaling_database|Sharding]])

전체 [[001_dikw_pyramid|데이터]]를 여러 노드에 [[136_variance|분산]] 저장하는 [[268_strategy_pattern|전략]].

```
파티셔닝 전략
┌─────────────────────────────────────────────────────┐
│  전체 데이터셋 (100TB)                               │
│                                                     │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐    │
│  │ 샤드 1  │  │ 샤드 2  │  │ 샤드 3  │  │ 샤드 4  │    │
│  │ 25TB   │  │ 25TB   │  │ 25TB   │  │ 25TB   │    │
│  │ 해시 0  │  │ 해시 1  │  │ 해시 2  │  │ 해시 3  │    │
│  └────────┘  └────────┘  └────────┘  └────────┘    │
└─────────────────────────────────────────────────────┘
```

| [[179_table_partitioning_concept|파티셔닝]] 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| 범위 (Range) | 키 범위로 분할 (A-G, H-N...) | 범위 [[298_qkv_attention|쿼리]] 효율적 | 핫스팟(Hot Spot) 위험 |
| 해시 (Hash) | 해시 함수로 균등 [[136_variance|분산]] | 균등한 부하 [[136_variance|분산]] | 범위 [[298_qkv_attention|쿼리]] 비효율 |
| 지리 (Geographic) | 지역별 [[136_variance|분산]] | 레이턴시 최소화 | 재조합 [[298_qkv_attention|쿼리]] 복잡 |

#### 2. [[016_replication_factor|복제]] ([[016_replication_factor|Replication]])

[[001_dikw_pyramid|데이터]]를 여러 노드에 [[016_replication_factor|복제]]하여 [[452_availability|가용성]]과 읽기 [[282_performance_tactics|성능]]을 향상.

```
복제 아키텍처 (복제 계수 = 3)
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ┌──────────┐    복제    ┌──────────┐               │
│  │ Primary  │──────────▶│ Replica1 │               │
│  │  Node    │           └──────────┘               │
│  └──────────┘                                       │
│       │         복제    ┌──────────┐               │
│       └───────────────▶│ Replica2 │               │
│                         └──────────┘               │
└─────────────────────────────────────────────────────┘
   쓰기: Primary만, 읽기: 세 노드 모두 처리 가능
```

#### 3. 부하 [[136_variance|분산]] ([[196_hard_soft_real_time|Load Balancing]])

```
L4/L7 부하 분산기 구조
                   ┌──────────────────┐
  클라이언트 ──────▶│  Load Balancer   │
                   │  (라운드로빈/최소  │
                   │   연결/IP해시)    │
                   └──┬───┬───┬───┬──┘
                      │   │   │   │
                   ┌──▼─┐ ┌▼──┐ ┌▼──┐ ┌▼──┐
                   │WS1 │ │WS2│ │WS3│ │WS4│
                   └────┘ └───┘ └───┘ └───┘
```

📢 **섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]]은 "도서관 책을 A~Z 선반에 나눠 꽂기", [[016_replication_factor|복제]]는 "같은 책을 3층 각 열람실에 비치하기", 부하 [[136_variance|분산]]은 "어느 열람실에 안내할지 결정하는 안내 데스크"다.

---

## Ⅲ. 비교 및 연결

### [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) 트레이드오프

브루어(Brewer)의 [[341_process|CAP]] 정리: [[136_variance|분산]] 시스템은 **[[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]])**, **[[452_availability|가용성]]([[452_availability|Availability]])**, **[[514_partition_slice_volume|파티션]] 허용성([[514_partition_slice_volume|Partition]] Tolerance)** 중 동시에 2가지만 보장 가능.

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
| [[089_contract_account_smart_contract|CA]] | [[194_consistency_database_integrity|일관성]] + [[452_availability|가용성]] | RDBMS ([[514_partition_slice_volume|파티션]] 없을 때) | 소규모 단일 서버 |
| [[086_CP_순환_전치_GI|CP]] | [[194_consistency_database_integrity|일관성]] + [[514_partition_slice_volume|파티션]] 허용 | [[543_hbase|HBase]], [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] | 강한 [[194_consistency_database_integrity|일관성]] 필요 시 |
| [[572_ap_access_point_ds_distribution_system|AP]] | [[452_availability|가용성]] + [[514_partition_slice_volume|파티션]] 허용 | [[541_cassandra|Cassandra]], [[545_dynamodb|DynamoDB]] | 대규모 빅데이터 ✅ |

### 스케일 아웃과 빅데이터 기술 [[057_stack|스택]] 연결

| 빅데이터 기술 | 스케일 아웃 방식 | 핵심 원리 |
|:---|:---|:---|
| [[013_hdfs|HDFS]] | 블록 [[136_variance|분산]] + 3중 [[016_replication_factor|복제]] | 블록(128MB) 단위 수평 [[136_variance|분산]] |
| [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | [[514_partition_slice_volume|파티션]] 기반 [[310_audit|RDD]] [[136_variance|분산]] | 익스큐터(Executor) 수평 추가 |
| [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] | [[514_partition_slice_volume|파티션]] + 리더/팔로워 | 토픽 [[514_partition_slice_volume|파티션]] 수평 [[136_variance|분산]] |
| [[541_cassandra|Cassandra]] | 일관된 해시링([[244_consistent_hashing_ring_distribution|Consistent Hashing]]) | 노드 추가 시 자동 리밸런싱 |
| [[302_cdc|Elasticsearch]] | 샤드 + 레플리카 | [[154_database_index_b_tree_search_optimization|인덱스]] 샤드 수평 [[136_variance|분산]] |

📢 **섹션 요약 비유**: [[341_process|CAP]] 트레이드오프는 "탈것 선택"이다. [[194_consistency_database_integrity|일관성]]은 정확도(오차 없는 GPS), [[452_availability|가용성]]은 연중무휴 운행, [[514_partition_slice_volume|파티션]] 허용은 네트워크 단절 시 계속 운행. 비행기([[086_CP_순환_전치_GI|CP]])는 정확하지만 멈추고, 자동차([[572_ap_access_point_ds_distribution_system|AP]])는 연중무휴지만 GPS가 가끔 틀린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 스케일 아웃 설계 시 핵심 고려사항

#### 1. 스테이트리스([[239_stateless_redis|Stateless]]) 설계 원칙

스케일 아웃이 효과적이려면 각 노드가 독립적으로 요청을 처리할 수 있는 무상태([[239_stateless_redis|Stateless]]) 설계가 필수다.

```
Stateful vs Stateless
┌─────────────────────────────────────────────────────┐
│  Stateful (문제):                                    │
│  Client ──▶ Server1 (세션 A 보유)                    │
│  Client ──▶ Server2 (세션 A 없음!) → 오류 발생        │
│                                                     │
│  Stateless (해결):                                   │
│  Client ──▶ (JWT 토큰 포함) ──▶ Server1 또는 Server2  │
│  모든 서버가 토큰으로 자체 검증 → 어디든 OK            │
└─────────────────────────────────────────────────────┘
```

#### 2. 실무 적용 사례: 전자상거래 플랫폼

| 레이어 | 스케일 아웃 방법 | 효과 |
|:---|:---|:---|
| 웹 서버 | Nginx 로드밸런서 + 10대 [[014_api_posix|API]] 서버 | 동시 접속 10만 → 100만 처리 |
| 캐시 레이어 | [[542_redis|Redis]] Cluster ([[280_sharding|샤딩]] 16384 슬롯) | 읽기 응답시간 50ms → 2ms |
| [[002_database_definition|데이터베이스]] | MySQL 읽기 레플리카 5대 | 읽기 부하 80% [[136_variance|분산]] |
| 빅데이터 처리 | Spark 클러스터 50 Executor | 일 1TB 집계 처리 2시간 → 10분 |

#### 3. 기술사 판단 포인트

- **[[179_table_partitioning_concept|파티셔닝]] 키 선택**: 핫스팟 방지를 위해 카디널리티(Cardinality)가 높은 컬럼 선택 필수
- **재조정(Resharding) 비용**: 노드 추가 시 [[001_dikw_pyramid|데이터]] 재분배 다운타임 최소화 [[268_strategy_pattern|전략]] 필요 ([[283_reference_pattern|일관된 해싱]] 사용)
- **네트워크 병목**: 스케일 아웃 시 노드 간 통신(셔플, [[016_replication_factor|복제]])이 병목이 될 수 있음. 10GbE 또는 [[361_infiniband|InfiniBand]] 활용

📢 **섹션 요약 비유**: 스케일 아웃은 배달 앱 운영과 같다. 주문이 늘어나면 배달 기사를 더 고용(수평 확장)하면 되지만, 모든 기사가 공통 창고(공유 상태)를 사용하면 창고에서 병목이 생긴다. 각 기사가 독립적으로 출발할 수 있어야([[239_stateless_redis|Stateless]]) 진정한 스케일 아웃이 된다.

---

## Ⅴ. 기대효과 및 결론

### 스케일 아웃 도입 효과

| 효과 영역 | 수치 사례 | 설명 |
|:---|:---|:---|
| 비용 절감 | 70% 비용 절감 | 고가 서버 1대 → 범용 서버 10대 |
| [[452_availability|가용성]] 향상 | 99.99% [[452_availability|가용성]] | N+1 리던던시로 노드 장애 무영향 |
| 확장 유연성 | 분 단위 노드 추가 | 클라우드 [[030_auto_scaling|Auto Scaling]] 연동 |
| [[139_throughput|처리량]] 향상 | 선형적 TPS 증가 | 노드 2배 = [[139_throughput|처리량]] 약 2배 |

### 한계 및 극복 방안

| 한계 | 원인 | 극복 방안 |
|:---|:---|:---|
| 운영 복잡성 | [[136_variance|분산]] 시스템 디버깅 어려움 | [[112_distributed_tracing_microservices|분산 트레이싱]](Jaeger, Zipkin) |
| [[194_consistency_database_integrity|일관성]] 약화 | [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]]([[556_master_slave_replication_lag_inconsistency|Replication Lag]]) | 강한 [[194_consistency_database_integrity|일관성]] 모드(Quorum 읽기) |
| 핫스팟 문제 | 불균등 [[179_table_partitioning_concept|파티셔닝]] | [[283_reference_pattern|일관된 해싱]], 가상 노드(Vnode) |
| 네트워크 비용 | 노드 간 [[001_dikw_pyramid|데이터]] 전송 | [[019_data_locality|데이터 지역성]]([[019_data_locality|Data Locality]]) 최적화 |

### 결론

스케일 아웃은 빅데이터 시대의 핵심 인프라 [[268_strategy_pattern|전략]]이다. 무한 확장성과 비용 효율성이라는 장점은 있지만, [[136_variance|분산]] 시스템 복잡성과 [[341_process|CAP]] 트레이드오프라는 대가를 치러야 한다. 기술사 관점에서는 "왜 스케일 아웃인가"뿐만 아니라 "어떤 조건에서 [[621_scale_up_system_bus|스케일 업]]이 더 적합한가"도 균형 있게 서술해야 한다.

📢 **섹션 요약 비유**: 스케일 아웃은 "체인 레스토랑 [[268_strategy_pattern|전략]]"이다. 한 매장을 고급화하기보다 동네마다 표준화된 지점을 내는 것. 관리는 더 복잡해지지만, 한 지점이 문 닫아도 전체 영업은 계속되고 수요에 따라 지점을 빠르게 늘리거나 줄일 수 있다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 대비 개념 | [[621_scale_up_system_bus|스케일 업]] ([[621_scale_up_system_bus|Scale-Up]]) | 수직 확장, 단일 서버 고사양화 |
| 기반 개념 | Shared-Nothing 아키텍처 | 노드 간 자원 비공유 [[136_variance|분산]] 설계 |
| 이론적 근거 | [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) | [[136_variance|분산]] 시스템 [[194_consistency_database_integrity|일관성]]-[[452_availability|가용성]] 트레이드오프 |
| 핵심 기술 | [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]] / [[280_sharding|샤딩]] | [[001_dikw_pyramid|데이터]]를 여러 노드에 [[136_variance|분산]] 저장 |
| 핵심 기술 | 부하 [[136_variance|분산]] ([[196_hard_soft_real_time|Load Balancing]]) | 요청을 여러 노드에 균등 분배 |
| 응용 기술 | [[030_auto_scaling|Auto Scaling]] | 부하에 따른 자동 노드 추가/제거 |
| 연관 기술 | [[283_reference_pattern|일관된 해싱]] ([[244_consistent_hashing_ring_distribution|Consistent Hashing]]) | 노드 추가/제거 시 [[001_dikw_pyramid|데이터]] 재배치 최소화 |

### 👶 어린이를 위한 3줄 비유 설명
1. [[621_scale_up_system_bus|스케일 업]]은 "한 명의 요리사를 슈퍼 셰프로 만들기"고, 스케일 아웃은 "평범한 요리사를 100명 고용하기"예요.

### 📈 관련 키워드 및 발전 흐름도

```text
단일 서버 (Scale-Up: CPU·RAM 증설)
    │ 물리적 한계
    ▼
Scale-Out: 수평 분산 (노드 추가)
    ├─► 데이터 샤딩 · 파티셔닝
    ├─► 로드 밸런싱 · 장애 격리
    └─► Shared-Nothing 아키텍처
    │
    ▼
클라우드 오토스케일링: K8s · Auto Scaling Group
```
2. 슈퍼 셰프는 한 명이라 몸이 아프면 레스토랑 전체가 멈추지만, 100명 중 한 명이 아파도 나머지 99명이 계속 요리해요.
3. 그래서 빅데이터처럼 엄청난 주문이 오는 곳에서는 "평범한 요리사 100명 [[268_strategy_pattern|전략]]"인 스케일 아웃을 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 202 / 258

← **이전**: [[201_bigdata_3v_5v_volume_velocity_variety|201. 빅데이터 3V·5V 특성 (Big Data 3V·5V Characteristics)]]
**다음**: [[203_hadoop_hdfs_block_replication_fault_tolerance|203. 하둡 HDFS (Hadoop Distributed File System) 블록 복제 내결함성]] →

---
