---
title: "Byzantine Fault Tolerance Majority Defense"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)(Byzantine [Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/), [비잔틴 장애 허용](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/))는 최대 <strong>f개의 악의적 노드</strong>가 존재해도 정상 합의를 보장하기 위해 <strong>3f+1개 이상의 노드</strong>가 필요하다는 수학적 원리다.
> 2. **가치**: [PBFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)([Practical BFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/))의 3단계(Pre-prepare -> Prepare -> Commit)와 현대적 최적화 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(Tendermint, HotStuff)은 허가형 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 <strong>결정적 최종성(Deterministic <a href="/studynote/06_ict_convergence/01_blockchain/065_consensus_finality_probabilistic_deterministic/">Finality</a>)</strong>을 가능하게 한다.
> 3. **판단 포인트**: [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 기반 합의는 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리에서 <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a> 모델</strong>([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)+[파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용)에 해당하며, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 발생 시 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 희생해 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 지킨다.

---

## Ⅰ. 개요 및 필요성

### 비잔틴 장군 문제(Byzantine Generals Problem)

1982년 Lamport·Shostak·Pease 논문에서 제시된 문제: 여러 장군이 메신저를 통해 공격 계획을 조율하는데, 일부 장군이나 메신저가 거짓 메시지를 전달할 때 어떻게 올바른 합의에 도달하는가?

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에서 이는 일부 노드가 악의적으로 다른 노드에 서로 다른 값을 전송하는 **이중 메시지(Equivocation)** 문제로 구체화된다.

### 3f+1 원리의 수학적 근거

```
총 노드 수: n, 악의 노드 수: f

조건: n ≥ 3f + 1

예시: f=1(악의 1개)이면 n≥4 필요
     f=10(악의 10개)이면 n≥31 필요

이유: 정상 2f+1 ≥ f+1 (과반 이상 보장)
     모든 노드 쌍의 교집합에 정직 노드 포함
```

- **📢 섹션 요약 비유**: — "장군 4명 중 1명이 거짓말쟁이여도, 나머지 3명이 다수결로 올바른 공격 시간을 결정할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [PBFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) 3단계 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)

```
+----------------------------------------------------------+
|                PBFT 합의 3단계 (뷰 v)                     |
|                                                          |
|  클라이언트  리더(Primary)    복제 노드 R1  복제 노드 R2  |
|      |           |                |              |       |
|      |--Request--►               |              |       |
|      |           |                |              |       |
|      |    [1] Pre-prepare         |              |       |
|      |           |--Pre-prepare--►|--Pre-prepare-►       |
|      |           |                |              |       |
|      |    [2] Prepare             |              |       |
|      |           |◄--Prepare-----►|◄-Prepare-----►       |
|      |           |    (2f+1개 수신 후 진행)       |       |
|      |    [3] Commit              |              |       |
|      |           |◄--Commit------►|◄-Commit------►       |
|      |           |    (2f+1개 수신 후 실행)       |       |
|      |           |                |              |       |
|      |◄----------Reply----------------------------       |
+----------------------------------------------------------+
```

### 현대 [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 메시지 복잡도 | 특징 | 사용처 |
|:---|:---:|:---|:---|
| <strong><a href="/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/">PBFT</a></strong> | O(n^) | 최초 실용 [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/), 소규모 최적 | Hyperledger |
| **Tendermint** | O(n^) | 라운드 기반, [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 특화 | Cosmos, [BSC](/studynote/12_it_management/01_governance_strategy/019_bsc/) |
| **HotStuff** | O(n) | 선형 복잡도, 파이프라인 | LibraBFT/Diem |
| **SBFT** | O(n) | 리더 집합, 실용 최적화 | 엔터프라이즈 |

- **📢 섹션 요약 비유**: — "PBFT는 모든 장군이 서로 편지를 써야 하는 시스템, HotStuff는 한 줄로 줄 세워 릴레이 전달로 최적화한 것이다.

---

## Ⅲ. 비교 및 연결

### [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) vs CFT 비교

| 항목 | CFT(Crash [Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) | [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)(Byzantine [Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) |
|:---|:---|:---|
| **가정** | 노드가 멈추거나 응답 없음 | 노드가 거짓 응답 가능 |
| **허용 장애** | f < n/2 | f < n/3 |
| **복잡도** | 낮음 | 높음 |
| **사용처** | [Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/), Paxos | [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/), 허가형 [DLT](/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) |

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

[BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a>(<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a> + <a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> Tolerance)</strong> 모델이다:
- [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(네트워크 분리) 발생 시 -> 2f+1 정족수 미달 -> <strong>블록 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 중단</strong> ([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 희생)
- 대신 <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 보장</strong>: 두 서로 다른 블록이 동시에 최종화되는 상황(Fork) 방지

- **📢 섹션 요약 비유**: — "BFT는 '틀린 답보다 답 없음이 낫다'는 원칙 — 거짓 합의보다 합의 중단을 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 구현별 특성과 판단 기준

1. <strong><a href="/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/">Hyperledger Fabric</a></strong>: 채널(Channel)별 [PBFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) -> 기업 내부망, 소수 노드 환경 적합
2. **Tendermint(Cosmos)**: 라운드-로빈 리더 선출, 2/3 투표 -> 빠른 최종성, 퍼블릭 체인 적합
3. **HotStuff(Diem/Aptos)**: O(n) 선형 메시지 -> 대규모 검증자 집합도 효율적

### 뷰 체인지([View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) Change)
PBFT는 리더(Primary)가 비잔틴 행동 시 <strong>뷰 체인지 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>로 새 리더를 선출한다. 이 때도 2f+1 노드의 동의가 필요하다.

### 기술사 판단: 언제 BFT인가?
- 노드 수가 수십~수백 수준 (대규모 퍼블릭 체인 부적합)
- 결정적 최종성 필요 (금융 결제, 의료 기록)
- 허가형 환경에서 신뢰 최소화 필요

- **📢 섹션 요약 비유**: — "BFT는 소규모 이사회에서 만장일치에 가까운 의결 구조 — 구성원이 많아질수록 진행이 느려진다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **결정적 최종성** | 한 번 확정된 블록은 절대 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 불가 |
| **포크 방지** | 네트워크 분리 시에도 이중 블록 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 차단 |
| <strong>허가형 <a href="/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a> 핵심</strong> | 금융·의료·[공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 엔터프라이즈 활용 기반 |
| **보안 경계 명확** | f < n/3 범위 내에서 수학적 안전 보장 |

BFT는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 악의적 행위자까지 허용하는 가장 강한 수준의 내결함성이다. 3f+1 원리와 [PBFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) 3단계 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 이해하면 현대 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 합의 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 설계 철학을 꿰뚫을 수 있다.

- **📢 섹션 요약 비유**: — "3명이 1명의 거짓말쟁이를 이기려면 적어도 4명이 필요하다 — 이것이 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 안전성의 수학적 바닥이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| 비잔틴 장군 문제 | BFT의 이론적 원천 문제 |
| [PBFT](/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) | BFT의 최초 실용 구현, O(n^) |
| Tendermint | [BFT](/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 기반 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 최적화 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | BFT는 [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] -> [BFT 비잔틴 장애 허용과 다수결 방어] -> [BFT는 CP 모델]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 5명이 투표하는데 1명이 거짓말쟁이여도, 나머지 4명이 다수결로 올바른 결정을 내릴 수 있어요.
2. 이 원리를 수학으로 정리하면 "거짓말쟁이가 n/3보다 적으면 안전"이에요.
3. [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)이 해커 공격을 받아도 버티는 이유가 바로 이 수학 덕분입니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 476 / 552

<- **이전**: [475. PoW와 PoS 합의 메커니즘 비교 (PoW vs PoS Consensus Mechanism)](/studynote/06_ict_convergence/01_blockchain/475_pow_pos_proof_mechanisms_comparison/)
**다음**: [477. 스마트 컨트랙트 EVM과 가스 실행 구조 (Smart Contract EVM and Gas Execution)](/studynote/06_ict_convergence/01_blockchain/477_smart_contract_evm_gas_execution/) ->

---
