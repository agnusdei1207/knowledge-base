---
title: 23. EVM (Ethereum Virtual Machine) — 이더리움 가상 머신
date: '2026-04-29'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[152_evm_earned_value_management|EVM]] (Ethereum [[598_vm_migration_nic|Virtual Machine]], 이더리움 가상 머신)은 이더리움 [[004_blockchain|블록체인]] 위에서 [[022_smart_contract|스마트 컨트랙트]]([[022_smart_contract|Smart Contract]])를 결정론적(Deterministic)으로 실행하는 [[010_decentralization|탈중앙화]] 세계 컴퓨터의 실행 환경으로, 전 세계 수천 개의 노드가 동일한 코드를 완전히 동일한 결과로 실행하는 것을 보장한다.
> 2. **가치**: EVM은 [[057_stack|스택]] 기반([[057_stack|Stack]]-Based) 256비트 아키텍처로 설계되어 암호학적 연산(해시, 서명 [[395_verification_process_review|검증]])을 네이티브로 지원하며, [[024_gas|가스]]([[024_gas|Gas]]) 메커니즘으로 무한 루프(Halting Problem)를 차단하여 [[004_blockchain|블록체인]] 전체의 안전성과 일관성을 지킨다.
> 3. **판단 포인트**: Solidity로 작성된 [[022_smart_contract|스마트 컨트랙트]]는 [[152_evm_earned_value_management|EVM]] [[074_byte|바이트]]코드로 컴파일되어 배포되며, [[024_gas|가스]] 최적화([[024_gas|Gas]] Optimization)는 [[033_defi_decentralized_finance|DeFi]], NFT, [[054_dao_decentralized_autonomous_organization|DAO]] 등 모든 Web3 애플리케이션의 운영 비용과 직결되므로 설계 초기부터 [[024_gas|가스]] 효율을 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

[[152_evm_earned_value_management|EVM]] (Ethereum [[598_vm_migration_nic|Virtual Machine]], 이더리움 가상 머신)은 이더리움 네트워크의 모든 노드에서 동일하게 실행되는 [[057_stack|스택]] 기반 가상 실행 환경이다.

[[073_bit|비트]]코인의 스크립트 언어가 단순한 전송 조건만 처리하는 한계를 극복하기 위해 비탈릭 부테린(Vitalik Buterin)이 2015년 설계한 EVM은 튜링 완전(Turing-Complete)한 연산을 [[004_blockchain|블록체인]] 위에서 처리할 수 있게 했다. EVM이 없다면 [[033_defi_decentralized_finance|DeFi]]([[010_decentralization|탈중앙화]] 금융), NFT, [[054_dao_decentralized_autonomous_organization|DAO]] 같은 복잡한 [[004_blockchain|블록체인]] 애플리케이션은 존재할 수 없다.

```text
┌─────────────────────────────────────────────────────────────┐
│                EVM 실행 계층 전체 구조                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Solidity / Vyper 소스 코드                                  │
│          │ (컴파일)                                          │
│          ▼                                                  │
│  EVM 바이트코드 (Bytecode)                                   │
│          │ (트랜잭션으로 블록체인에 배포)                      │
│          ▼                                                  │
│  ┌───────────────────────────────────┐                      │
│  │  EVM 실행 환경                    │                      │
│  │  ├─ 스택 (Stack, 1024 슬롯 최대) │                      │
│  │  ├─ 메모리 (Memory, 휘발성)      │                      │
│  │  ├─ 스토리지 (Storage, 영구)     │                      │
│  │  └─ 프로그램 카운터 (PC)         │                      │
│  └───────────────────────────────────┘                      │
│          │ (가스 소비하며 실행)                               │
│          ▼                                                  │
│  상태 전이 (State Transition) — 블록체인 상태 업데이트         │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: EVM은 전 세계가 공동 소유한 슈퍼컴퓨터다. 아무도 혼자 멈추거나 조작할 수 없고, 모든 참가자가 동시에 같은 프로그램을 돌려 결과를 [[395_verification_process_review|검증]]한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [[057_stack|스택]] 기반 256비트 아키텍처

EVM은 256비트(32바이트) 단위의 [[057_stack|스택]]을 사용한다. 이는 [[101_sha_3|SHA-3]](Keccak-256) 해시 값과 이더리움 주소(160비트)를 네이티브로 처리하기 위함이다.

| 구성 요소 | 크기/특성 | 용도 |
|:---|:---|:---|
| **[[057_stack|스택]] ([[057_stack|Stack]])** | 256bit × 최대 1024 슬롯 | 연산 중간 값 임시 저장 |
| **메모리 (Memory)** | [[074_byte|바이트]] [[055_array|배열]], 휘발성 | 함수 실행 중 임시 [[001_dikw_pyramid|데이터]] |
| **스토리지 (Storage)** | 256bit→256bit 맵, 영구 | 컨트랙트 상태 변수 |
| **콜데이터 (Calldata)** | 읽기 전용 | 외부 [[294_function_calling_tool_use|함수 호출]] 인자 |

### 2. [[024_gas|가스]]([[024_gas|Gas]]) 메커니즘

[[024_gas|가스]]는 EVM의 각 연산코드([[159_opcode|Opcode]]) 실행 비용을 ETH로 환산한 단위다.

```text
┌─────────────────────────────────────────────────────┐
│              가스 동작 흐름                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  사용자 → 트랜잭션 전송 (Gas Limit + Gas Price 설정) │
│              │                                      │
│              ▼                                      │
│  EVM 실행 → 각 Opcode마다 가스 차감                  │
│    ├─ ADD: 3 gas                                    │
│    ├─ SSTORE (새 값): 20,000 gas (비쌈!)             │
│    ├─ SSTORE (업데이트): 2,900 gas                   │
│    └─ KECCAK256: 30 + 6×데이터크기 gas               │
│              │                                      │
│  가스 소진 전 완료 → 남은 가스 환불                   │
│  가스 소진(Out of Gas) → 트랜잭션 전체 롤백           │
└─────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[024_gas|가스]]는 자동차 연료다. 출발 전 연료([[024_gas|Gas]] Limit)를 넣고, 복잡한 길(복잡한 연산)을 갈수록 기름을 더 소비하며, 연료가 바닥나면 목적지 못 가고 출발 지점으로 되돌아온다([[098_rollback_strategy_pipeline_error_threshold|롤백]]).

---

## Ⅲ. 비교 및 연결

| 항목 | [[152_evm_earned_value_management|EVM]] | [[701_webassembly_wasm_frontend_performance|WASM]] ([[319_webassembly_architecture|WebAssembly]]) | JVM (Java [[598_vm_migration_nic|VM]]) |
|:---|:---|:---|:---|
| **설계 목적** | [[004_blockchain|블록체인]] [[022_smart_contract|스마트 컨트랙트]] | 웹 브라우저 고성능 실행 | 범용 애플리케이션 |
| **[[073_bit|비트]] 단위** | 256bit 네이티브 | 32/64bit | 32/64bit |
| **실행 비용 제어** | [[024_gas|가스]]([[024_gas|Gas]]) 메커니즘 | 없음 | 없음 |
| **결정론적 실행** | 완전 보장 | 보장 가능 | 부분적 |
| **[[152_evm_earned_value_management|EVM]] 호환 체인** | Ethereum, [[019_bsc|BSC]], [[045_sidechain_bridge_polygon|Polygon]] 등 | — | — |

[[152_evm_earned_value_management|EVM]] [[344_compatibility_usability|호환성]]([[152_evm_earned_value_management|EVM]] [[344_compatibility_usability|Compatibility]])은 이더리움 생태계의 핵심 경쟁 우위로, [[019_bsc|BSC]](Binance Smart Chain), [[045_sidechain_bridge_polygon|Polygon]], Avalanche C-Chain 등이 EVM을 채택하여 이더리움 DApp을 그대로 이식 가능하게 했다.

- **📢 섹션 요약 비유**: [[152_evm_earned_value_management|EVM]] [[344_compatibility_usability|호환성]]은 안드로이드 앱 생태계와 같다. 한 번 개발하면 안드로이드 폰(이더리움 호환 체인) 어디서든 그대로 작동한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [[033_defi_decentralized_finance|DeFi]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[024_gas|가스]] 최적화
AMM(Automated Market Maker) 스왑 컨트랙트의 [[191_transaction_concept_states|트랜잭션]] [[024_gas|가스]] 비용이 경쟁 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 대비 40% 높다.

1. **문제 [[655_ir_detection_analysis|식별]]**: `SSTORE` 호출 횟수 과다 — 루프마다 스토리지 [[289_cqrs_db|쓰기]] 발생.
2. **최적화**: 중간 계산 값을 메모리(Memory)에 임시 저장 후 최종 값만 스토리지에 씀.
3. **결과**: [[024_gas|가스]] 소비 35% 절감, 사용자 [[191_transaction_concept_states|트랜잭션]] 비용 대폭 감소.

### [[435_checklist_based_testing|체크리스트]]
- `SSTORE` > `MSTORE` 순으로 비용 크므로, 루프 내 스토리지 직접 접근 최소화.
- 변수 타입 `uint256` 패킹(Packing)으로 슬롯 절약.
- `view`/`pure` 함수는 [[024_gas|가스]] 소모 없음 — 읽기 전용 설계 활용.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[024_gas|Gas]] Limit을 과도하게 높게 설정하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]. EVM은 실제 소비된 [[024_gas|가스]]만 차감하지만, [[024_gas|Gas]] Limit 초과 시 [[191_transaction_concept_states|트랜잭션]] 자체가 거부되므로 적절한 추정(Estimation)이 필수다. 무작정 높이면 사용자 경험(UX)이 저하된다.

- **📢 섹션 요약 비유**: [[024_gas|가스]] 최적화는 연비 좋은 자동차를 설계하는 것과 같다. 엔진([[152_evm_earned_value_management|EVM]])은 정해져 있지만, 설계자가 부품 배치(코드 구조)를 잘 하면 같은 거리를 절반의 연료로 갈 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **[[010_decentralization|탈중앙화]] 실행 보장** | 단일 실패 지점 없는 코드 실행 | 99.99% [[452_availability|가용성]] |
| **투명성** | 모든 실행 결과 [[004_blockchain|블록체인]]에 영구 기록 | [[606_auditing_linux_auditd|감사]] 가능성 100% |
| **확장성 진화** | [[152_evm_earned_value_management|EVM]] 2.0(EOF 포맷) + L2 [[042_rollup_l2_solution|롤업]] 결합 | TPS 수천~수만 달성 |

EVM은 이더리움 생태계의 근간이며, [[152_evm_earned_value_management|EVM]] Object Format (EOF), EIP-4844 (Proto-Danksharding) 등의 업그레이드로 성능과 보안이 지속 강화되고 있다. ZK-[[152_evm_earned_value_management|EVM]]([[229_zkp_data_clean_room|영지식 증명]] 기반 [[152_evm_earned_value_management|EVM]])은 프라이버시와 확장성을 동시에 달성하는 차세대 실행 환경으로 주목받고 있다.

- **📢 섹션 요약 비유**: EVM은 세계 모든 은행이 합의한 단 하나의 계산기다. 어느 나라에서 계산하든 항상 같은 답이 나오며, 계산 결과를 누구도 지울 수 없는 영구 영수증으로 남긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[022_smart_contract|스마트 컨트랙트]]** | [[152_evm_earned_value_management|EVM]] 위에서 실행되는 자동 계약 코드 |
| **[[057_solidity_smart_contract_language|Solidity]]** | [[152_evm_earned_value_management|EVM]] [[074_byte|바이트]]코드로 컴파일되는 [[022_smart_contract|스마트 컨트랙트]] 언어 |
| **[[024_gas|가스]]([[024_gas|Gas]])** | [[152_evm_earned_value_management|EVM]] 연산 비용 단위; 무한 루프 차단 메커니즘 |
| **EIP (이더리움 개선 제안)** | [[152_evm_earned_value_management|EVM]] 스펙을 발전시키는 공식 제안 프로세스 |
| **ZK-[[152_evm_earned_value_management|EVM]]** | [[229_zkp_data_clean_room|영지식 증명]]으로 [[152_evm_earned_value_management|EVM]] 실행을 [[395_verification_process_review|검증]]하는 차세대 확장 솔루션 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비트코인 스크립트 — 제한된 조건부 실행]
    │
    ▼
[EVM v1 (2015) — 튜링 완전 스마트 컨트랙트 실행]
    │
    ▼
[EVM 호환 L1 체인 — BSC, Polygon, Avalanche]
    │
    ▼
[EVM on L2 — Optimism, Arbitrum (롤업 기반 확장)]
    │
    ▼
[ZK-EVM — 영지식 증명 기반 EVM 검증 (Scroll, zkSync)]
```
[[073_bit|비트]]코인의 단순 스크립트에서 출발해 튜링 완전 EVM을 거쳐, L2 [[042_rollup_l2_solution|롤업]]과 ZK 증명 기반 EVM으로 확장성과 보안을 동시에 달성하는 방향으로 진화 중이다.

### 👶 어린이를 위한 3줄 비유 설명

1. EVM은 전 세계 모든 친구들이 함께 쓰는 거대한 **공용 로봇 두뇌**예요!
2. 이 두뇌에 규칙([[022_smart_contract|스마트 컨트랙트]])을 프로그래밍하면, 누가 시키지 않아도 스스로 약속을 지켜 돈을 보내거나 거래를 완료해 줘요.
3. 연료([[024_gas|가스]])를 넣어줘야 일하고, 연료가 다 떨어지면 작동을 멈추고 원래대로 되돌아가는 아주 신중한 로봇이에요!
