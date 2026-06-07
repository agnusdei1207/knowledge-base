---
title: "CAP Theorem"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
weight: 125
---
## 핵심 인사이트 (3줄 요약)
- <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>의 불가능성:</strong> [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(C), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A), [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 감내(P) 세 가지를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 동시에 완벽하게 만족할 수 없다는 에릭 브루어의 이론임.
- **P는 필수:** 네트워크 단절(P)은 제어 불가능한 실재이므로, 실제 설계 시에는 [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 중심)와 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 중심) 중 하나를 선택하는 트레이드오프가 핵심임.
- **아키텍처 가이드:** 시스템의 목적(금융 vs SNS)에 따라 어떤 특성을 우선시할지 결정하는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계의 가장 중요한 나침반 역할을 수행함.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
1. <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 환경의 숙명:</strong> 노드가 여러 개로 나뉘어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하는 환경에서는 네트워크 장애가 필연적으로 발생하며, 이때 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 처리할지가 시스템의 성격을 결정함.
2. <strong>트레이드오프 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>:</strong> 모든 것을 가질 수는 없으므로, 비즈니스 요건에 맞춰 "무엇을 버릴지"를 결정하는 엔지니어링적 통찰을 제공함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/">CAP Theorem</a> Triangle &amp; Node Interaction</strong>
```text
          [ Consistency ] (C)
              /   \
             /     \
      (CP)  /       \  (CA)
           /         \
          /           \
[ Partition ]-------[ Availability ]
 Tolerance (P)  (AP)      (A)

1. C: 모든 노드가 같은 시점에 같은 데이터를 보아야 함.
2. A: 일부 노드 장애 시에도 모든 요청에 응답해야 함.
3. P: 노드 간 네트워크 단절 시에도 시스템이 작동해야 함.
```

1. <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a> (<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a> + <a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> Tolerance):</strong>
   - 네트워크 단절 시, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치를 막기 위해 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 응답을 거부(에러 반환)함. <strong>완벽한 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong>이 중요한 금융권, [HBase](/studynote/05_database/04_transactions_concurrency/543_hbase/), [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/)(기본)가 대표적임.
2. <strong><a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> (<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a> + <a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> Tolerance):</strong>
   - 네트워크 단절 시, 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 아닐지라도 일단 응답을 제공함. <strong>중단 없는 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>가 중요한 SNS, [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/), DynamoDB가 대표적임.
3. <strong><a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a> (<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a> + <a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>):</strong>
   - 네트워크 장애가 없음을 가정하므로 단일 노드 시스템(RDBMS)에 해당함. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서는 P를 포기할 수 없으므로 사실상 성립하기 어려움.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 ([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) focus) | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 ([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) focus) |
| :--- | :--- | :--- |
| **장애 대응** | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 위해 "느린 응답" 또는 "거절" | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 위해 "부정확한 응답" 허용 |
| **주요 기술** | Quorum, Paxos, [Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) | Gossip [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [Vector Clock](/studynote/05_database/04_transactions_concurrency/258_vector_clock/) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 정합성</strong> | 강한 정합성 (Strong [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 결과적 정합성 ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) |
| **사용 사례** | 결제, 인벤토리 관리, 사용자 프로필 | 뉴스 피드, 댓글, 장바구니 |
| **철학적 기반** | ACID (안정성) | BASE (속도) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. <strong>네트워크 장애(P)는 상수다 (Strategic <a href="/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a>):</strong>
   - [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 P를 선택하지 않는 것은 장애 시 시스템 전체 침묵을 의미함. 따라서 현대 클라우드 설계는 CP와 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 사이의 균형점을 찾는 과정임.
2. **기술사적 판단:** [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 고정된 불변의 진리라기보다 '극한 상황에서의 기준'임. 최근에는 [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리를 통해 네트워크가 정상인 시점의 Latency와 [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 사이의 트레이드오프까지 고려하는 고도화된 설계가 필요함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 시스템 요구사항에 최적화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소를 선택하고, 장애 상황에서도 비즈니스 연속성을 보장하는 구조적 설계를 가능하게 함.
2. **결론:** [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍트의 기초 문법임. 이를 통해 우리는 기술의 한계를 명확히 인식하고, 최선의 차선책을 선택할 수 있는 전문적 역량을 갖추게 됨.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템, [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/)
- **하위 개념:** [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(C), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A), [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 감내(P)
- **연관 개념:** [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리, BASE 원칙, [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) ([Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/))

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 분산 시스템, NoSQL]
    |
    v
[하위 개념: 일관성(C), 가용성(A), 파티션 감내(P)]
    |
    v
[연관 개념: PACELC 정리, BASE 원칙, 합의 알고리즘 (Raft)]
```

이 흐름도는 상위 개념: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템, NoSQL에서 출발해 연관 개념: [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리, BASE 원칙, [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) ([Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- **통신 끊김(P):** 친구와 전화가 끊겼을 때 어떻게 할까요?
- <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a> 친구:</strong> "중요한 얘기니까 나중에 전화 연결되면 다시 할게!" 하고 전화를 아예 안 받아요.
- <strong><a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> 친구:</strong> "아마도 어제 말한 그거일 거야!" 하고 일단 대답부터 해주고 끊어요.
- **결론:** 정답이 중요한지, 대답이 빠른 게 중요한지 고르는 시합이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 262

<- **이전**: [BASE 원칙 (Basically Available, Soft State, Eventual Consistency)](/studynote/16_bigdata/06_nosql/124_base_principles_nosql/)
**다음**: [PACELC 정리 (PACELC Theorem)](/studynote/16_bigdata/06_nosql/126_pacelc_theorem_extended_cap/) ->

---
