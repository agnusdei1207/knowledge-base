+++
title = "130. MongoDB 아키텍처 — ReplicaSet/Sharding/Mongos"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: MongoDB의 ReplicaSet은 자동 장애 조치(Automatic [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/))를 제공하는 고가용성 단위이며, Sharding은 이 ReplicaSet을 기반으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수평 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)하여 무제한 확장을 실현한다.
- **가치**: Mongos 라우터가 클라이언트에게 단일 엔드포인트를 제공하여 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 복잡성을 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하며, WiredTiger 스토리지 엔진의 문서 수준 잠금으로 높은 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 보장한다.
- **판단 포인트**: [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/) 선택이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 90%를 결정하며, 카디널리티(Cardinality)가 낮거나 단조 증가하는 키는 핫스팟(Hot Spot)을 유발하므로 복합 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)를 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

### [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 아키텍처 3대 구성 요소

| 구성 요소 | 역할 | 특징 |
|:---:|:---|:---:|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/">ReplicaSet</a></strong> | 고가용성 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 자동 프라이머리 선출 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/">Sharding</a></strong> | 수평 확장 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 청크(Chunk) 기반 분배 |
| **Mongos** | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 라우터 | 클라이언트 단일 접점 |

### WiredTiger 스토리지 엔진 특징

```text
+----------------------------------------------------+
|          WiredTiger 스토리지 엔진 (기본값)            |
+----------------------------------------------------+
|  ■ 잠금 수준: 문서(Document) 수준 — 행 잠금보다 세밀   |
|  ■ 압축: Snappy/zlib/zstd 지원 (스토리지 50~80% 절감)|
|  ■ MVCC: 읽기/쓰기 충돌 없음                        |
|  ■ 캐시: 기본 50% RAM 할당 (wiredTigerCacheSizeGB)  |
|  ■ 저널: 100ms 간격 Journaling (내구성 보장)         |
+----------------------------------------------------+
```

📢 **섹션 요약 비유**
> [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 아키텍처는 대형 물류 센터와 같다. ReplicaSet은 각 창고의 자동 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시스템이고, Sharding은 물건을 여러 창고에 나눠 보관하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장이며, Mongos는 어느 창고에 뭐가 있는지 알고 배송 경로를 안내하는 물류 AI다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) 구조 및 장애 조치

```text
+----------------------------------------------------------+
|                 MongoDB ReplicaSet 구조                   |
|                                                          |
|  +-------------+    복제     +-------------+             |
|  |  Primary    | -----------> | Secondary 1 |             |
|  |  (읽기/쓰기) |             |  (읽기 가능) |             |
|  +-------------+             +-------------+             |
|         |                          |                     |
|         |  복제                    |                     |
|         v                          v                     |
|  +-------------+          +--------------+               |
|  | Secondary 2 |          |   Arbiter    |               |
|  | (읽기 가능) |          | (투표만, 데이터 |              |
|  +-------------+          |  저장 안 함)  |               |
|                            +--------------+               |
|                                                          |
|  ■ 장애 조치(Failover) 과정:                              |
|    1. Primary 다운 감지 (heartbeat 실패)                  |
|    2. Secondaries + Arbiter 투표 (과반수 득표)             |
|    3. 새 Primary 선출 (보통 10~30초)                      |
|    4. 클라이언트 자동 재연결                               |
+----------------------------------------------------------+
```

### [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) 전체 구조

```text
+------------------------------------------------------------+
|                  MongoDB Sharding 아키텍처                  |
|                                                            |
|  [Application]                                             |
|       |                                                    |
|       v                                                    |
|  +----------------------------------+                      |
|  |     Mongos (Query Router)        |  <- 여러 개 배치 가능  |
|  +----------------------------------+                      |
|       | 샤드 키 기반 라우팅                                   |
|       +----------------+---------------+                   |
|       v                v               v                   |
|  +---------+     +---------+    +---------+               |
|  | Shard 1 |     | Shard 2 |    | Shard 3 |               |
|  |(RSset1) |     |(RSset2) |    |(RSset3) |               |
|  | Chunk   |     | Chunk   |    | Chunk   |               |
|  | 0~33%  |     | 34~66%  |    | 67~100% |               |
|  +---------+     +---------+    +---------+               |
|       ^                ^               ^                   |
|  +-----------------------------------------------------+   |
|  |         Config Servers (ReplicaSet)                 |   |
|  |   샤드 메타데이터: 청크 범위, 샤드 위치 정보 저장        |   |
|  +-----------------------------------------------------+   |
+------------------------------------------------------------+
```

### [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 예시 | 장점 | 단점 |
|:---:|:---:|:---:|:---:|
| **범위 기반(Range)** | 날짜, 숫자 ID | 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 효율 | 단조 증가 시 핫스팟 |
| **해시 기반(Hash)** | hash(userId) | 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 불가 |
| **복합(Compound)** | {region, userId} | 핫스팟 방지 + 범위 | 설계 복잡 |
| **영역 기반(Zone)** | {country: "KR"} | 지역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 격리 | 수동 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 |

### [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유형

| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유형 | 용도 | 예시 |
|:---:|:---|:---:|
| **단일 필드** | 기본 조회 최적화 | `{name: 1}` |
| **복합(Compound)** | 다중 필드 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | `{category:1, price:-1}` |
| **텍스트(Text)** | 전문 검색 | `{description: "text"}` |
| **지리공간(Geospatial)** | 위치 기반 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | `{location: "2dsphere"}` |
| **와일드카드(Wildcard)** | 동적 필드 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | `{"$**": 1}` |
| <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">TTL</a></strong> | 문서 자동 만료 | `{createdAt:1}, {expireAfterSeconds:3600}` |

📢 **섹션 요약 비유**
> [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/) 선택은 도서관 도서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 방법을 정하는 것과 같다. '가나다순 첫 글자'로만 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면 'ㄱ'으로 시작하는 책이 너무 많아 한 선반이 터진다(핫스팟). '주제+저자'의 복합 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 균형 잡힌 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 만든다.

---

## Ⅲ. 비교 및 연결

### [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) vs [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) 목적 차이

| 관점 | [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) | [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) |
|:---:|:---:|:---:|
| **목적** | 고가용성(HA) + 읽기 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 수평 확장 + [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 모든 노드에 전체 복사본 | 노드별 부분 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **노드 실패 시** | 자동 페일오버 | 해당 샤드만 영향 |
| **언제 도입** | 항상 (최소 구성) | 단일 ReplicaSet이 한계 도달 시 |

### 읽기 선호도(Read Preference) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)

```text
primaryPreferred   : 주로 Primary, 없으면 Secondary
secondary          : Secondary 전용 (분석 쿼리)
secondaryPreferred : 주로 Secondary
nearest            : 네트워크 지연 최소 노드
```

📢 **섹션 요약 비유**
> ReplicaSet은 똑같은 복사본을 3개 만드는 복사기이고, Sharding은 큰 문서를 3등분해서 각각 다른 서랍에 넣는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)링 시스템이다. 복사기는 하나를 잃어도 괜찮게 하고, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)링 시스템은 서랍 하나가 꽉 차지 않게 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 배포 아키텍처 결정 트리

```text
데이터 볼륨 < 1TB / 쓰기 TPS < 10K?
        |
   YES -+- NO ---> Sharding 도입 필요
        |         (최소 3 Shard × ReplicaSet)
        v
단순 ReplicaSet (1 Primary + 2 Secondary)
        |
읽기 부하 높음? --YES---> Secondary 읽기 분산 + ReadPreference
        |
       NO
        v
기본 구성 유지, 모니터링 기반 단계적 확장
```

### 운영 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 항목 | 권장 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 이유 |
|:---:|:---:|:---|
| [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) 최소 멤버 | 3개 이상(홀수) | 과반수 투표 보장 |
| 청크 크기 | 기본 128MB | 과도한 마이그레이션 방지 |
| 샤드 밸런서 시간 | 피크 외 시간 | 밸런싱 중 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향 최소화 |
| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 빌드 | Rolling Build | Primary 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| Mongos 수 | 앱 서버당 1개 이상 | [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 방지 |

📢 **섹션 요약 비유**
> [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 운영은 교통 관제와 같다. 평소에는 Mongos(교통 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))가 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 최적 경로로 안내하고, 사고(노드 장애) 시에는 자동으로 우회로(페일오버)를 찾는다. 청크 밸런서는 야간에 조용히 도로 공사를 해서 낮에는 항상 원활한 소통을 유지한다.

---

## Ⅴ. 기대효과 및 결론

### 대규모 배포 사례 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표

| 규모 | 구성 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
|:---:|:---:|:---:|
| 소규모 | 1 [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) (3노드) | ~50K TPS |
| 중규모 | 3 Shard × [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) | ~150K TPS |
| 대규모 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)+ Shard × [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) | ~500K+ TPS |

### 결론
MongoDB의 [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/)-[Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) 이중 구조는 고가용성과 무제한 확장을 동시에 달성하는 현존 최선의 문서형 DB 아키텍처다. 그러나 <strong><a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/">샤드 키</a> 선택 실수는 수정 비용이 극히 높으므로</strong> [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 패턴 분석에 충분한 시간을 투자해야 한다. 기술사 시험에서는 [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) 선출 메커니즘, [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/) 핫스팟 문제, Mongos 역할이 단골 출제 포인트다.

📢 **섹션 요약 비유**
> [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 아키텍처 설계는 도시 건설 계획과 같다. 처음에 도로([샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/))를 잘못 놓으면 나중에 뜯어고치는 비용이 엄청나다. 처음부터 교통 흐름([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴)을 고려해 넓은 도로(높은 카디널리티 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/))를 설계하면, 도시가 아무리 커져도 원활하게 확장된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| WiredTiger | 스토리지 엔진 | [MVCC](/knowledge-base/studynote/11_design_supervision/06_exam_summary/449_mvcc/), 문서 수준 잠금 |
| Oplog ([Operation](/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/) Log) | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 메커니즘 | Primary -> Secondary 변경 전파 |
| 청크(Chunk) | [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 단위 | 기본 128MB, 분할/마이그레이션 |
| [Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) Server | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 청크 위치 정보 관리 |
| ReadPreference | 읽기 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | Secondary 읽기 활용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서 지향 DB (Document-Oriented DB)]
    |
    v
[WiredTiger 스토리지 엔진 — MVCC]
    |
    v
[레플리카 셋 (Replica Set) — 자동 장애 조치]
    |
    v
[샤딩 (Sharding) — 수평 확장]
    |
    v
[Atlas (클라우드 MongoDB) — 서버리스 Document DB]
```

[MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 아키텍처가 단일 노드에서 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)을 거쳐 완전 관리형 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. ReplicaSet은 같은 책을 3권 인쇄해두는 것 — 한 권이 찢어져도 나머지 두 권으로 계속 읽을 수 있어요.
2. Sharding은 두꺼운 백과사전을 ㄱ~ㅇ, ㅈ~ㅎ으로 나눠 다른 선반에 두는 것 — 선반 하나가 무거워지지 않아요.
3. Mongos는 "내가 찾는 글자가 어느 선반에 있는지" 알려주는 안내원 — 덕분에 우리는 어느 선반에 뭐가 있는지 몰라도 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 262

<- **이전**: [129. 문서형 데이터베이스 (Document DB) — MongoDB/CouchDB/Firestore](/knowledge-base/studynote/16_bigdata/06_nosql/129_document_db/)
**다음**: [131. 컬럼 패밀리 데이터베이스 (Column Family DB) — Cassandra/HBase/ScyllaDB](/knowledge-base/studynote/16_bigdata/06_nosql/131_column_family_db/) ->

---
