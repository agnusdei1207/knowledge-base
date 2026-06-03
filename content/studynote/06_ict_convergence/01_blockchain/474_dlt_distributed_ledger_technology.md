---
title: 474. 분산 원장 기술 (DLT, Distributed Ledger Technology)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]](Distributed Ledger Technology, [[136_variance|분산]] 원장 기술)는 중앙 서버 없이 다수 노드가 **동일한 원장 복사본을 공유·합의**하는 기술의 총칭으로, [[004_blockchain|블록체인]]은 DLT의 한 구현 형태다.
> 2. **가치**: [[341_process|CAP]] 정리([[194_consistency_database_integrity|Consistency]]·[[452_availability|Availability]]·[[514_partition_slice_volume|Partition]] Tolerance 동시 불가)에서 DLT는 상황에 따라 [[086_CP_순환_전치_GI|CP]](강한 [[194_consistency_database_integrity|일관성]]) 또는 [[572_ap_access_point_ds_distribution_system|AP]]([[452_availability|가용성]] 우선)를 선택하는 **설계 트레이드오프**를 명시화한다.
> 3. **판단 포인트**: [[004_blockchain|블록체인]](선형 체인)·[[401_bayesian_network_dag_causality|DAG]]([[255_apache_airflow_dag|Directed Acyclic Graph]])·HashGraph 등 구조 차이가 [[139_throughput|처리량]](TPS)·최종성([[065_consensus_finality_probabilistic_deterministic|Finality]]) 성능을 결정하므로, 활용 목적에 맞는 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 선택이 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 중앙화 원장의 한계

기존 금융 시스템의 중앙화 원장(Centralized Ledger)은 단일 기관이 [[001_dikw_pyramid|데이터]]를 독점 관리한다. 이 구조는 [[454_spof|단일 장애점]], 내부자 조작, 오프라인 시 [[090_service_kubernetes_network_load_balancing|서비스]] 중단 문제를 내포한다.

DLT는 원장을 **여러 노드에 [[136_variance|분산]]·[[016_replication_factor|복제]]**하여 한 노드가 실패해도 [[090_service_kubernetes_network_load_balancing|서비스]]가 지속되고, 다수 노드가 합의해야만 원장을 수정할 수 있어 내부자 조작이 어렵다.

### [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] [[104_classification_analysis|분류]] 체계

```
┌─────────────────────────────────────────────┐
│             DLT 분류                         │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  블록체인(Blockchain)               │   │
│  │  : 순차적 블록 연결, 해시 포인터     │   │
│  │  예) Bitcoin, Ethereum              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  DAG(Directed Acyclic Graph)        │   │
│  │  : 트랜잭션이 직접 서로 검증        │   │
│  │  예) IOTA Tangle, Nano              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  HashGraph                          │   │
│  │  : 가십 프로토콜 + 가상 투표        │   │
│  │  예) Hedera Hashgraph               │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: — "중앙 은행 금고 하나에 모든 돈 장부가 있는 것 vs 전국 지점 모두가 동일한 장부 사본을 갖는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 주요 구현 비교

| 항목 | [[004_blockchain|블록체인]] | [[401_bayesian_network_dag_causality|DAG]] | HashGraph |
|:---|:---:|:---:|:---:|
| **구조** | 선형 블록 체인 | 비순환 방향 [[070_graph_datastructure|그래프]] | 가십 이벤트 [[070_graph_datastructure|그래프]] |
| **TPS** | 7~30 (BTC/[[118_eth|ETH]]) | 수천 | [[489_raid_10_hybrid|10]],000+ |
| **최종성** | 확률적 | 확률적 | 결정적 |
| **에너지** | 높음(PoW) | 낮음 | 낮음 |
| **허가 여부** | 공개/비허가 | 공개/비허가 | 허가형 |

### [[341_process|CAP]] 정리와 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 설계

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

- **[[086_CP_순환_전치_GI|CP]] 모델**: [[013_pbft_practical_bft|PBFT]]([[013_pbft_practical_bft|Practical BFT]]) 기반 [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]] → [[514_partition_slice_volume|파티션]] 시 [[452_availability|가용성]] 희생, [[194_consistency_database_integrity|일관성]] 보장
- **[[572_ap_access_point_ds_distribution_system|AP]] 모델**: 비트코인 → [[194_consistency_database_integrity|일관성]] 최종성을 확률적으로 처리, [[452_availability|가용성]] 유지
- **실질적 [[136_variance|분산]] 시스템**: P([[514_partition_slice_volume|Partition]] Tolerance)는 필수 → CA는 단일 노드에만 해당

- **📢 섹션 요약 비유**: — "음식점 주방 메모판(중앙)을 없애고 모든 직원이 메모를 복사해 갖는 것. 한 명이 실수해도 나머지가 수정해 준다.

---

## Ⅲ. 비교 및 연결

### 주요 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 플랫폼

| 플랫폼 | 유형 | 특징 |
|:---|:---|:---|
| **R3 Corda** | 허가형(Permissioned) | 금융 기관 전용, [[191_transaction_concept_states|트랜잭션]] 당사자만 공유 |
| **[[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]]** | 허가형 | 채널(Channel) 격리, [[059_chaincode_smart_contract|체인코드]]([[059_chaincode_smart_contract|Chaincode]]) |
| **IOTA** | 비허가형 [[401_bayesian_network_dag_causality|DAG]] | [[101_iot_concept|IoT]] 마이크로 [[191_transaction_concept_states|트랜잭션]], 수수료 없음 |
| **Hedera Hashgraph** | 허가형 HashGraph | 고TPS, 가십 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **Ethereum** | 비허가형 [[004_blockchain|블록체인]] | [[022_smart_contract|스마트 컨트랙트]] 범용 플랫폼 |

**비블록체인 DLT의 차이점**: DAG는 블록 단위가 없으며 새 [[191_transaction_concept_states|트랜잭션]]이 이전 [[191_transaction_concept_states|트랜잭션]] 2개를 직접 [[395_verification_process_review|검증]]하는 방식으로 합의한다. [[191_transaction_concept_states|트랜잭션]] 수가 많을수록 [[395_verification_process_review|검증]] 속도가 빨라지는 **자기 확장성(Self-Scaling)**이 특징이다.

- **📢 섹션 요약 비유**: — "[[004_blockchain|블록체인]]은 기차처럼 한 줄로 가고, DAG는 고속도로처럼 여러 차선이 동시에 달린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 도메인별 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 선택 기준

1. **금융 결제·무역 금융**: R3 Corda, [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]] (허가형, 프라이버시 [[571_protection_vs_security|보호]])
2. **[[101_iot_concept|IoT]] 마이크로 결제**: IOTA [[401_bayesian_network_dag_causality|DAG]] (수수료 없음, 높은 TPS)
3. **공개 [[033_defi_decentralized_finance|DeFi]]([[010_decentralization|탈중앙화]] 금융)**: Ethereum, Solana (비허가형, [[022_smart_contract|스마트 컨트랙트]])
4. **공공 행정**: 허가형 [[004_blockchain|블록체인]] ([[001_dikw_pyramid|데이터]] 접근 제어, [[606_auditing_linux_auditd|감사]] Trail)

### 기술사 핵심 판단
- **"왜 [[004_blockchain|블록체인]]만이 DLT가 아닌가?"**: [[401_bayesian_network_dag_causality|DAG]], HashGraph의 구조적 차이와 장단점 명시
- **[[341_process|CAP]] 트레이드오프**: 금융은 [[086_CP_순환_전치_GI|CP]], IoT는 [[572_ap_access_point_ds_distribution_system|AP]] 선택이 합리적
- **[[065_consensus_finality_probabilistic_deterministic|Finality]] 종류**: 확률적 최종성(비트코인, k번 [[396_validation|확인]]) vs 결정적 최종성([[013_pbft_practical_bft|PBFT]], Tendermint)

- **📢 섹션 요약 비유**: — "은행 장부(R3 Corda)와 공개 게시판(Bitcoin)은 모두 [[136_variance|분산]] 원장이지만, 쓰임새와 보안 모델이 완전히 다르다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **신뢰 비용 절감** | 중개기관(Escrow, Clearing) 없는 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 거래 |
| **[[606_auditing_linux_auditd|감사]] 가능성** | 변경 불가한 기록으로 규제 보고 자동화 |
| **글로벌 금융 포용** | 은행 계좌 없이도 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 지갑으로 금융 [[090_service_kubernetes_network_load_balancing|서비스]] 이용 |
| **[[809_data_sovereignty|데이터 주권]]** | 개인이 자신의 [[001_dikw_pyramid|데이터]]를 직접 관리(SSI와 연계) |

DLT는 [[004_blockchain|블록체인]]보다 넓은 개념이며, 사용 목적·허가 수준·[[011_consensus_algorithm|합의 알고리즘]]에 따라 다양한 형태가 존재한다. 기술사는 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 종류를 용도에 맞게 선택하고 [[341_process|CAP]] 트레이드오프를 명확히 설명할 수 있어야 한다.

- **📢 섹션 요약 비유**: — "'자동차'가 승용차·트럭·버스를 포괄하듯, DLT는 [[004_blockchain|블록체인]]·[[401_bayesian_network_dag_causality|DAG]]·HashGraph를 포괄하는 큰 범주다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [[083_relationship_in_er_model|관계]] 설명 |
| [[341_process|CAP]] 정리 | [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 설계 트레이드오프의 이론적 근거 |
| [[401_bayesian_network_dag_causality|DAG]] | 비블록체인 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 구조, IOTA 사용 |
| [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]] | 허가형 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]], 엔터프라이즈 활용 |
| [[013_pbft_practical_bft|PBFT]] | 허가형 DLT의 주요 [[011_consensus_algorithm|합의 알고리즘]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [분산 원장 기술] → [허가형 DLT의 주요 합의 알고리즘]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 반 친구 모두가 같은 공유 노트를 가지고 있어서, 선생님 없이도 내용을 수정하려면 반 전체 동의가 필요합니다.
2. [[004_blockchain|블록체인]]은 노트가 한 줄씩 이어지는 형태고, DAG는 여러 줄을 동시에 쓸 수 있는 형태예요.
3. 중앙에서 혼자 관리하면 그 사람이 거짓말해도 모르지만, [[136_variance|분산]]하면 다 같이 [[396_validation|확인]]하니까 속이기 어렵습니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 474 / 552

← **이전**: [[473_blockchain_merkle_tree_hash_integrity|473. 블록체인 머클 트리와 해시 무결성 (Blockchain Merkle Tree and Hash Integrity)]]
**다음**: [[475_pow_pos_proof_mechanisms_comparison|475. PoW와 PoS 합의 메커니즘 비교 (PoW vs PoS Consensus Mechanism)]] →

---
