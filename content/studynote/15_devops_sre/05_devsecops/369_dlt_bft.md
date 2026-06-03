---
title: 369. 블록체인 분산원장 스마트계약 BFT 합의 (Blockchain DLT Smart Contract BFT PBFT Consensus)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] (Distributed Ledger Technology)는 중앙 관리자 없이 [[136_variance|분산]]된 노드들이 [[011_consensus_algorithm|합의 알고리즘]]([[647_bft_verification|BFT]], PoW, PoS)으로 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 보장하는 기술이며, [[004_blockchain|블록체인]]은 DLT의 한 구현체로 블록이 체인으로 연결된 해시 기반 불변 원장이다.
> 2. **가치**: [[022_smart_contract|스마트 컨트랙트]]([[022_smart_contract|Smart Contract]])는 조건 충족 시 자동 실행되는 코드로 중개자 없는 신뢰 거래를 가능하게 하며, [[013_pbft_practical_bft|PBFT]] (Practical Byzantine [[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])는 허가형 [[004_blockchain|블록체인]]([[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]])에서 f개 악의적 노드가 있어도 3f+1 이상 노드로 합의를 보장한다.
> 3. **판단 포인트**: 공개형([[076_permissionless_vs_permissioned_blockchain|Permissionless]]) [[004_blockchain|블록체인]](Bitcoin PoW, Ethereum PoS)은 [[010_decentralization|탈중앙화]]가 강하지만 [[139_throughput|처리량]](TPS)이 낮고, 허가형(Permissioned) [[004_blockchain|블록체인]]([[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]], R3 Corda)은 엔터프라이즈 요건에 적합하다.

---

## Ⅰ. 개요 및 필요성

기존 거래 시스템은 중앙 신뢰 기관(은행, 정부)이 원장을 관리한다. 이 구조는 [[454_spof|단일 장애점]]([[454_spof|SPoF]]), [[001_dikw_pyramid|데이터]] 변조 위험, 중간자 비용의 문제를 가진다. DLT는 신뢰 기관 없이 참여 노드들이 합의로 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 [[395_verification_process_review|검증]]해 이 문제를 해결한다.

Ethereum의 [[022_smart_contract|스마트 컨트랙트]]는 Solidity로 작성된 코드가 [[152_evm_earned_value_management|EVM]] ([[023_evm_ethereum_virtual_machine|Ethereum Virtual Machine]])에서 실행되어 [[010_decentralization|탈중앙화]] 애플리케이션([[032_dapp_decentralized_application|DApp]])을 가능하게 한다.

- 📢 섹션 요약 비유: [[004_blockchain|블록체인]]은 수백 명이 동시에 복사본을 가진 공책이다. 한 사람이 내용을 바꾸면 나머지와 달라져서 바로 들키고, 과반수 동의 없이는 변경이 불가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│              블록체인 블록 구조 및 BFT 합의                      │
├──────────────────────────────────────────────────────────────────┤
│  [블록 N-1]          [블록 N]            [블록 N+1]             │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐           │
│  │ 헤더      │        │ 헤더      │        │ 헤더      │          │
│  │ PrevHash │◀───────│ PrevHash │◀───────│ PrevHash │           │
│  │ Merkle   │        │ Merkle   │        │ Merkle   │           │
│  ├──────────┤        ├──────────┤        ├──────────┤           │
│  │ 트랜잭션  │        │ 트랜잭션  │        │ 트랜잭션  │          │
│  └──────────┘        └──────────┘        └──────────┘           │
│                                                                  │
│  PBFT: Pre-prepare → Prepare → Commit → Reply (3f+1 노드 필요)  │
└──────────────────────────────────────────────────────────────────┘
```

| [[011_consensus_algorithm|합의 알고리즘]]   | 내결함성          | TPS       | 주요 사용처          |
| :-------------- | :---------------- | :-------- | :------------------- |
| PoW             | 51% 공격 [[003_resistance|저항]]     | ~7        | Bitcoin              |
| PoS             | 33% 지분 공격     | ~수천     | Ethereum 2.0         |
| [[013_pbft_practical_bft|PBFT]]            | (n-1)/3 악의 노드 | ~수천     | [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]]   |
| [[259_raft_paxos|Raft]]            | (n-1)/2 장애 노드 | 수만      | [[078_etcd_distributed_key_value_store|etcd]], [[292_etl_process|CockroachDB]]    |

**Merkle 트리**: 블록 내 모든 [[191_transaction_concept_states|트랜잭션]]의 해시를 트리 구조로 집계해 Merkle Root를 [[087_process_state_transition|생성]]. 하나의 [[191_transaction_concept_states|트랜잭션]] 변조 시 Merkle Root가 바뀌어 즉시 탐지된다.

- 📢 섹션 요약 비유: [[022_smart_contract|스마트 컨트랙트]]는 자동 판매기다. 돈을 넣으면(조건 충족) 자동으로 음료가 나온다(코드 실행). 중간에 사람(중개자)이 개입할 필요 없이 프로그램이 처리한다.

---

## Ⅲ. 비교 및 연결

| 항목            | 공개형 [[004_blockchain|블록체인]]               | 허가형 [[004_blockchain|블록체인]]               |
| :-------------- | :---------------------------- | :---------------------------- |
| 접근 제어       | 누구나 참여 가능              | 허가된 노드만 참여            |
| 합의            | PoW, PoS (에너지 소모)        | [[013_pbft_practical_bft|PBFT]], [[259_raft_paxos|Raft]] (에너지 효율적)    |
| TPS             | 낮음 (~수십~수천)             | 높음 (~수천~수만)             |
| 주요 사례       | Bitcoin, Ethereum             | [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]], R3 Corda  |

- 📢 섹션 요약 비유: 허가형 [[004_blockchain|블록체인]]은 회사 내부 전자 결재 시스템이다. 공개형이 누구나 볼 수 있는 공개 게시판이라면, 허가형은 임직원만 접근 가능한 사내 인트라넷이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[004_blockchain|블록체인]] 도입 [[435_checklist_based_testing|체크리스트]]**
1. 필요성 [[395_verification_process_review|검증]]: 중앙 신뢰 기관 없이도 거래가 성립해야 하는가? (아니면 DB로 충분)
2. 공개형 vs 허가형: TPS, 프라이버시, 규제 요건 기반 결정
3. [[022_smart_contract|스마트 컨트랙트]] [[527_security_audit_trail|보안 감사]]: Reentrancy, [[333_integer_overflow|Integer Overflow]] 등 취약점 전문 [[606_auditing_linux_auditd|감사]]
4. [[011_consensus_algorithm|합의 알고리즘]] 선택: [[013_pbft_practical_bft|PBFT]] (소규모, 고성능), PoS (대규모 탈중앙)
5. 오라클([[188_pl_sql_t_sql_procedural|Oracle]]) 연동: 외부 [[001_dikw_pyramid|데이터]] → [[004_blockchain|블록체인]] 입력 신뢰 경로 설계

**[[128_water_scrum_fall_anti_pattern|안티패턴]]**
- 불필요한 [[004_blockchain|블록체인]] 도입 → "[[004_blockchain|블록체인]] 씻기([[004_blockchain|Blockchain]] Washing)"
- [[022_smart_contract|스마트 컨트랙트]] 배포 후 버그 발견 → 수정 불가로 [[090_service_kubernetes_network_load_balancing|서비스]] 완전 중단
- [[013_pbft_practical_bft|PBFT]] 노드 수를 너무 늘림 → O(n^2) [[389_mesh_topology|메시]]지 복잡도로 [[282_performance_tactics|성능]] 급락

- 📢 섹션 요약 비유: [[022_smart_contract|스마트 컨트랙트]] 버그는 자판기 프로그램 오류와 같다. 자판기가 설치된 후에는 프로그램을 바꾸기가 매우 어렵다.

---

## Ⅴ. 기대효과 및 결론

글로벌 [[520_supply_chain_attack_and_ci_cd_security|공급망]]에 허가형 [[004_blockchain|블록체인]]([[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]])을 적용한 Walmart Food Trust는 식품 추적 시간을 6.5일에서 2.2초로 단축했다.

미래는 Layer 2 [[249_scaling_normalization_standardization|스케일링]](Optimistic [[042_rollup_l2_solution|Rollup]], ZK-[[042_rollup_l2_solution|Rollup]])으로 TPS를 수십만까지 확장하고, [[190_ai_llm_requirements_specification|AI]] + [[004_blockchain|블록체인]]의 [[010_decentralization|탈중앙화]] [[190_ai_llm_requirements_specification|AI]] 추론 [[395_verification_process_review|검증]]이 새로운 응용 영역으로 부상한다.

- 📢 섹션 요약 비유: [[004_blockchain|블록체인]]은 공증 시스템이다. 중요한 계약서에는 공증이 필요하지만, 매일 쓰는 메모장에 공증을 받을 필요는 없다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] (Distributed Ledger Technology)     | [[004_blockchain|블록체인]]을 포함하는 상위 개념, 합의 기반 [[136_variance|분산]] 원장       |
| [[647_bft_verification|BFT]] (Byzantine [[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])         | 악의적 노드 포함 환경에서 합의 보장하는 이론             |
| [[013_pbft_practical_bft|PBFT]] ([[013_pbft_practical_bft|Practical BFT]])                    | 3f+1 노드로 f개 악의 노드 허용, 허가형 [[004_blockchain|블록체인]] 합의     |
| [[022_smart_contract|스마트 컨트랙트]]                          | 조건 자동 실행 코드, [[057_solidity_smart_contract_language|Solidity]]/Chaincode로 구현           |
| Merkle 트리                              | 블록 내 [[191_transaction_concept_states|트랜잭션]] [[003_integrity|무결성]] 증명 구조                        |

### 📈 관련 키워드 및 발전 흐름도

```text
Bitcoin PoW (에너지 집약 탈중앙 합의)
    │
    ▼
Ethereum 스마트 컨트랙트 + EVM (DApp 플랫폼)
    │
    ▼
허가형 블록체인 (Hyperledger Fabric + PBFT)
    │
    ▼
DeFi (탈중앙화 금융) / NFT / DAO
    │
    ▼
Layer 2 스케일링 (ZK-Rollup, Optimistic Rollup)
    │
    ▼
멀티체인 + 크로스체인 + AI 추론 검증
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[004_blockchain|블록체인]]은 수천 명이 같은 공책을 동시에 들고 있어서, 한 명이 내용을 바꾸면 나머지가 다 알아채는 마법 공책이에요.
2. [[022_smart_contract|스마트 컨트랙트]]는 "조건을 달성하면 자동으로 보상을 준다"는 약속이 컴퓨터 코드로 이루어진 거예요.
3. PBFT는 100명 중 33명이 거짓말을 해도 나머지 67명의 투표로 올바른 결정을 내릴 수 있는 투표 방식이에요.
