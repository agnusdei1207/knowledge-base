+++
title = "474. 분산 원장 기술 (DLT, Distributed Ledger Technology)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/)(Distributed Ledger Technology, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 원장 기술)는 중앙 서버 없이 다수 노드가 <strong>동일한 원장 복사본을 공유·합의</strong>하는 기술의 총칭으로, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 DLT의 한 구현 형태다.
> 2. **가치**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·[Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance 동시 불가)에서 DLT는 상황에 따라 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)(강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 또는 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선)를 선택하는 <strong>설계 트레이드오프</strong>를 명시화한다.
> 3. **판단 포인트**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)(선형 체인)·[DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/)([Directed Acyclic Graph](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/))·HashGraph 등 구조 차이가 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(TPS)·최종성([Finality](/knowledge-base/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/)) 성능을 결정하므로, 활용 목적에 맞는 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 선택이 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 중앙화 원장의 한계

기존 금융 시스템의 중앙화 원장(Centralized Ledger)은 단일 기관이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 독점 관리한다. 이 구조는 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), 내부자 조작, 오프라인 시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 문제를 내포한다.

DLT는 원장을 <strong>여러 노드에 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>·<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a></strong>하여 한 노드가 실패해도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 지속되고, 다수 노드가 합의해야만 원장을 수정할 수 있어 내부자 조작이 어렵다.

### [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계

```
+---------------------------------------------+
|             DLT 분류                         |
|                                             |
|  +-------------------------------------+   |
|  |  블록체인(Blockchain)               |   |
|  |  : 순차적 블록 연결, 해시 포인터     |   |
|  |  예) Bitcoin, Ethereum              |   |
|  +-------------------------------------+   |
|                                             |
|  +-------------------------------------+   |
|  |  DAG(Directed Acyclic Graph)        |   |
|  |  : 트랜잭션이 직접 서로 검증        |   |
|  |  예) IOTA Tangle, Nano              |   |
|  +-------------------------------------+   |
|                                             |
|  +-------------------------------------+   |
|  |  HashGraph                          |   |
|  |  : 가십 프로토콜 + 가상 투표        |   |
|  |  예) Hedera Hashgraph               |   |
|  +-------------------------------------+   |
+---------------------------------------------+
```

- **📢 섹션 요약 비유**: — "중앙 은행 금고 하나에 모든 돈 장부가 있는 것 vs 전국 지점 모두가 동일한 장부 사본을 갖는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 주요 구현 비교

| 항목 | [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | HashGraph |
|:---|:---:|:---:|:---:|
| **구조** | 선형 블록 체인 | 비순환 방향 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | 가십 이벤트 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **TPS** | 7~30 (BTC/[ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/)) | 수천 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000+ |
| **최종성** | 확률적 | 확률적 | 결정적 |
| **에너지** | 높음(PoW) | 낮음 | 낮음 |
| **허가 여부** | 공개/비허가 | 공개/비허가 | 허가형 |

### [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리와 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 설계

```
         C (Consistency, 일관성)
              /\
             /  \
            /    \
           /  CA  \
          /--------\
         / CP   AP  \
        /______________\
   A (Availability)    P (Partition Tolerance)
```

- <strong><a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a> 모델</strong>: [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)([Practical BFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)) 기반 [Hyperledger Fabric](/knowledge-base/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/) -> [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 시 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 희생, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장
- <strong><a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> 모델</strong>: 비트코인 -> [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 최종성을 확률적으로 처리, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지
- <strong>실질적 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템</strong>: P([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance)는 필수 -> CA는 단일 노드에만 해당

- **📢 섹션 요약 비유**: — "음식점 주방 메모판(중앙)을 없애고 모든 직원이 메모를 복사해 갖는 것. 한 명이 실수해도 나머지가 수정해 준다.

---

## Ⅲ. 비교 및 연결

### 주요 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 플랫폼

| 플랫폼 | 유형 | 특징 |
|:---|:---|:---|
| **R3 Corda** | 허가형(Permissioned) | 금융 기관 전용, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 당사자만 공유 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/">Hyperledger Fabric</a></strong> | 허가형 | 채널(Channel) 격리, [체인코드](/knowledge-base/studynote/06_ict_convergence/01_blockchain/059_chaincode_smart_contract/)([Chaincode](/knowledge-base/studynote/06_ict_convergence/01_blockchain/059_chaincode_smart_contract/)) |
| **IOTA** | 비허가형 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 마이크로 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), 수수료 없음 |
| **Hedera Hashgraph** | 허가형 HashGraph | 고TPS, 가십 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| **Ethereum** | 비허가형 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) | [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 범용 플랫폼 |

**비블록체인 DLT의 차이점**: DAG는 블록 단위가 없으며 새 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 이전 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 2개를 직접 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방식으로 합의한다. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 수가 많을수록 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 속도가 빨라지는 <strong>자기 확장성(Self-Scaling)</strong>이 특징이다.

- **📢 섹션 요약 비유**: — "[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 기차처럼 한 줄로 가고, DAG는 고속도로처럼 여러 차선이 동시에 달린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 도메인별 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 선택 기준

1. **금융 결제·무역 금융**: R3 Corda, [Hyperledger Fabric](/knowledge-base/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/) (허가형, 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/))
2. <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 마이크로 결제</strong>: IOTA [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) (수수료 없음, 높은 TPS)
3. <strong>공개 <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/">DeFi</a>(<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/">탈중앙화</a> 금융)</strong>: Ethereum, Solana (비허가형, [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))
4. **공공 행정**: 허가형 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 제어, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) Trail)

### 기술사 핵심 판단
- <strong>"왜 <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a>만이 DLT가 아닌가?"</strong>: [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/), HashGraph의 구조적 차이와 장단점 명시
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 트레이드오프</strong>: 금융은 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/), IoT는 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택이 합리적
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/">Finality</a> 종류</strong>: 확률적 최종성(비트코인, k번 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)) vs 결정적 최종성([PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/), Tendermint)

- **📢 섹션 요약 비유**: — "은행 장부(R3 Corda)와 공개 게시판(Bitcoin)은 모두 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 원장이지만, 쓰임새와 보안 모델이 완전히 다르다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **신뢰 비용 절감** | 중개기관(Escrow, Clearing) 없는 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 거래 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 가능성</strong> | 변경 불가한 기록으로 규제 보고 자동화 |
| **글로벌 금융 포용** | 은행 계좌 없이도 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 지갑으로 금융 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이용 |
| <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/">데이터 주권</a></strong> | 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직접 관리(SSI와 연계) |

DLT는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)보다 넓은 개념이며, 사용 목적·허가 수준·[합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)에 따라 다양한 형태가 존재한다. 기술사는 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 종류를 용도에 맞게 선택하고 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 트레이드오프를 명확히 설명할 수 있어야 한다.

- **📢 섹션 요약 비유**: — "'자동차'가 승용차·트럭·버스를 포괄하듯, DLT는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)·[DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/)·HashGraph를 포괄하는 큰 범주다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 설계 트레이드오프의 이론적 근거 |
| [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | 비블록체인 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) 구조, IOTA 사용 |
| [Hyperledger Fabric](/knowledge-base/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/) | 허가형 [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/), 엔터프라이즈 활용 |
| [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) | 허가형 DLT의 주요 [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] -> [분산 원장 기술] -> [허가형 DLT의 주요 합의 알고리즘]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 반 친구 모두가 같은 공유 노트를 가지고 있어서, 선생님 없이도 내용을 수정하려면 반 전체 동의가 필요합니다.
2. [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 노트가 한 줄씩 이어지는 형태고, DAG는 여러 줄을 동시에 쓸 수 있는 형태예요.
3. 중앙에서 혼자 관리하면 그 사람이 거짓말해도 모르지만, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)하면 다 같이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하니까 속이기 어렵습니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 474 / 552

<- **이전**: [473. 블록체인 머클 트리와 해시 무결성 (Blockchain Merkle Tree and Hash Integrity)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/473_blockchain_merkle_tree_hash_integrity/)
**다음**: [475. PoW와 PoS 합의 메커니즘 비교 (PoW vs PoS Consensus Mechanism)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/475_pow_pos_proof_mechanisms_comparison/) ->

---
