---
title: 477. 스마트 컨트랙트 EVM과 가스 실행 구조 (Smart Contract EVM and Gas Execution)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[022_smart_contract|스마트 컨트랙트]]([[022_smart_contract|Smart Contract]])는 [[152_evm_earned_value_management|EVM]]([[023_evm_ethereum_virtual_machine|Ethereum Virtual Machine]], 이더리움 가상 머신)에서 실행되는 자율 프로그램으로, 코드가 곧 계약서이자 집행자다.
> 2. **가치**: [[024_gas|가스]]([[024_gas|Gas]]) 시스템은 튜링 완전(Turing Complete) 언어의 무한루프 문제를 경제적으로 해결하며, EIP-1559의 기본 수수료(Base Fee) 소각 메커니즘은 [[118_eth|ETH]] 디플레이션 효과를 만든다.
> 3. **판단 포인트**: [[057_solidity_smart_contract_language|Solidity]] → Bytecode → [[152_evm_earned_value_management|EVM]] [[159_opcode|Opcode]] 변환 흐름을 이해하면 재진입 공격(Reentrancy)·[[333_integer_overflow|정수 오버플로우]] 등 [[022_smart_contract|스마트 컨트랙트]] 취약점의 발생 원인을 논리적으로 추론할 수 있다.

---

## Ⅰ. 개요 및 필요성

### [[022_smart_contract|스마트 컨트랙트]]의 등장

Nick Szabo가 1994년 제안한 [[022_smart_contract|스마트 컨트랙트]] 개념은 "조건 충족 시 자동 실행되는 계약 코드"다. 이더리움은 이를 **[[010_decentralization|탈중앙화]] 월드 컴퓨터**로 구현했다.

전통 계약의 문제: 중개자 필요, 이행 강제 비용, 불투명성 → [[022_smart_contract|스마트 컨트랙트]]는 코드가 자동 집행되므로 신뢰 비용을 제거한다.

- **📢 섹션 요약 비유**: — "자판기가 가장 단순한 [[022_smart_contract|스마트 컨트랙트]]다 — 동전 넣으면(조건 충족), 음료 나온다(자동 실행), 중간에 사람 필요 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 컴파일·실행 흐름

```
┌─────────────────────────────────────────────────────────┐
│         스마트 컨트랙트 실행 파이프라인                  │
│                                                         │
│  Solidity (.sol)                                        │
│       │  solc 컴파일러                                   │
│       ▼                                                 │
│  Bytecode (0x606060...)      ABI (인터페이스 정의)       │
│       │                           │                     │
│       ▼                           ▼                     │
│  EVM(Ethereum Virtual Machine)                          │
│  ┌───────────────────────────────────────────┐          │
│  │ Stack (256bit × 1024) │ Memory (바이트배열) │          │
│  │ Storage (영구 키-값)   │ Opcode 실행 엔진   │          │
│  └───────────────────────────────────────────┘          │
│       │ 가스(Gas) 차감                                    │
│       ▼                                                 │
│  상태 변경(State Change) → 블록체인 기록                 │
└─────────────────────────────────────────────────────────┘
```

### [[024_gas|가스]]([[024_gas|Gas]]) 구조

| 구성 요소 | 설명 | EIP-1559 이후 |
|:---|:---|:---|
| **[[024_gas|Gas]] Limit** | [[191_transaction_concept_states|트랜잭션]] 최대 허용 연산량 | 동일 |
| **[[024_gas|Gas]] Price** | 단위 [[024_gas|가스]]당 지불 [[118_eth|ETH]](Gwei) | 폐지 |
| **Base Fee** | 네트워크 혼잡도 기반 소각 수수료 | ✅ 도입 |
| **Priority Fee(Tip)** | 채굴자/[[395_verification_process_review|검증]]자 팁 | ✅ 도입 |
| **실제 비용** | [[024_gas|Gas]] Used × (Base Fee + Tip) | 예측 가능 |

### 주요 [[159_opcode|Opcode]] [[024_gas|가스]] 비용 예시

```
SSTORE (스토리지 쓰기): 20,000 gas
SLOAD  (스토리지 읽기): 2,100 gas
ADD    (덧셈 연산):        3 gas
CALL   (외부 호출):    2,600 gas
```

- **📢 섹션 요약 비유**: — "EVM은 미터기 달린 택시다 — 이동 거리(연산량)마다 요금([[024_gas|Gas]])이 나오고, 잔액 떨어지면 멈춘다.

---

## Ⅲ. 비교 및 연결

### [[152_evm_earned_value_management|EVM]] 호환 체인 비교

| 체인 | [[152_evm_earned_value_management|EVM]] 호환 | 특징 |
|:---|:---:|:---|
| **Ethereum** | 기준 | 원조 [[152_evm_earned_value_management|EVM]], 최고 보안 |
| **[[045_sidechain_bridge_polygon|Polygon]]** | ✅ | 낮은 [[024_gas|가스]]비, 이더리움 L2 |
| **BNB Chain** | ✅ | 빠른 블록, 중앙화 우려 |
| **Arbitrum** | ✅ | 옵티미스틱 [[042_rollup_l2_solution|롤업]] L2 |
| **Solana** | ❌ | [[238_svm_margin_kernel_trick_naive_bayes|SVM]], [[782_memory_safety_rust_compiler_verification|Rust]] 기반 |

### 재진입 공격(Reentrancy) 원리

```solidity
// 취약한 패턴
function withdraw() {
    uint amount = balances[msg.sender];
    (bool sent,) = msg.sender.call{value: amount}(""); // ← 외부 호출
    balances[msg.sender] = 0; // ← 업데이트가 호출 이후 → 위험!
}
```
EVM의 [[189_subroutine_call_return|CALL]] Opcode가 외부 컨트랙트 실행을 허용하기 때문에, 상태 업데이트 전 외부 호출은 재진입 취약점을 만든다.

- **📢 섹션 요약 비유**: — "ATM에서 '잔액 차감' 전에 '현금 지급'을 먼저 하면, 현금 받는 즉시 다시 출금 요청할 수 있다 — 이것이 재진입 공격이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[024_gas|가스]] 최적화 실무 기법

1. **스토리지 읽기 최소화**: SLOAD는 비싸므로 로컬 변수에 [[456_caching|캐싱]]
2. **이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]] 활용**: 히스토리 데이터는 Storage 대신 Event([[568_logs_distributed_logging_elk_fluentd|로그]]) 사용
3. **[[228_batch_processing_hadoop_spark|배치 처리]]**: 여러 작업을 단일 [[191_transaction_concept_states|트랜잭션]]에 묶어 기본 비용 절감
4. **[[057_solidity_smart_contract_language|Solidity]] [[288_version_ihl_tos_total_length|버전]] 최신화**: 컴파일러 최적화 개선

### EIP-1559 의미
- Base Fee 소각 → [[118_eth|ETH]] 공급량 감소 → 인플레이션 방어
- [[024_gas|가스]]비 예측 가능 → UX 개선
- [[395_verification_process_review|검증]]자 팁(Priority Fee)만 수령 → 기존 수익 감소, 장기 보안 모델 변화

### 기술사 핵심 판단
- 튜링 완전성과 무한루프 방지: [[024_gas|가스]] 한도가 Halting Problem의 실용적 해결책
- 형식 [[395_verification_process_review|검증]]([[093_smart_contract_formal_verification|Formal Verification]]) 도구(Certora, Mythril) 필요성
- 업그레이드 패턴: 불변 컨트랙트의 한계 → [[158_proxy_pattern|프록시 패턴]]([[158_proxy_pattern|Proxy Pattern]])으로 우회

- **📢 섹션 요약 비유**: — "[[022_smart_contract|스마트 컨트랙트]] 버그는 '배포 후 수정 불가'가 원칙 — 은행 [[272_atm_asynchronous_transfer_mode_53byte_cell|ATM]] 코드를 배포 전에 완벽히 [[395_verification_process_review|검증]]해야 하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **중개 비용 제거** | 계약 집행 자동화로 법적 비용 절감 |
| **투명성** | 모든 실행 결과가 온체인 공개 |
| **프로그래머블 화폐** | 조건부 지불, 탈중앙 금융([[033_defi_decentralized_finance|DeFi]]) 기반 |
| **새 취약점 등장** | 재진입·오라클 조작·플래시론 공격 등 |

EVM과 [[024_gas|가스]] 시스템은 이더리움 생태계의 실행 엔진이다. 튜링 완전성을 경제적 [[024_gas|가스]] 메커니즘으로 안전하게 제공함으로써 [[033_defi_decentralized_finance|DeFi]], NFT, [[054_dao_decentralized_autonomous_organization|DAO]] 등 모든 Web3 서비스의 근간을 형성한다.

- **📢 섹션 요약 비유**: — "EVM은 전 세계가 공유하는 단 하나의 컴퓨터 — 연산 자원을 [[024_gas|가스]]로 경매하여 공정 배분한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [[083_relationship_in_er_model|관계]] 설명 |
| [[057_solidity_smart_contract_language|Solidity]] | [[152_evm_earned_value_management|EVM]] [[022_smart_contract|스마트 컨트랙트]] 주요 언어 |
| EIP-1559 | [[024_gas|가스]] 수수료 개혁 제안 |
| 재진입 공격 | [[152_evm_earned_value_management|EVM]] [[189_subroutine_call_return|CALL]] 순서 오류 취약점 |
| [[015_abi|ABI]] | [[022_smart_contract|스마트 컨트랙트]] 외부 인터페이스 정의 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [스마트 컨트랙트 EVM과 가스 실행 구조] → [스마트 컨트랙트 외부 인터페이스 정의]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[022_smart_contract|스마트 컨트랙트]]는 조건을 만족하면 자동으로 실행되는 로봇 계약서예요.
2. [[024_gas|가스]]([[024_gas|Gas]])는 이 로봇이 작동하는 데 필요한 연료인데, 연료가 떨어지면 작동을 멈춰 무한 루프를 막아요.
3. 자판기처럼 동전 넣으면 음료가 나오듯, [[022_smart_contract|스마트 컨트랙트]]는 조건이 맞으면 자동으로 돈이나 토큰을 보냅니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 477 / 552

← **이전**: [[476_bft_byzantine_fault_tolerance_majority_defense|476. BFT 비잔틴 장애 허용과 다수결 방어 (Byzantine Fault Tolerance Majority Defense)]]
**다음**: [[478_token_economy_ico_nft_rwa|478. 토큰 이코노미: ICO, NFT, RWA (Token Economy: ICO, NFT, RWA)]] →

---
