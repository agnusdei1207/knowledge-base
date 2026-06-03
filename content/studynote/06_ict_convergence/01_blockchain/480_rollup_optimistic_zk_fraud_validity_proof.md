+++
title = "480. 롤업: 옵티미스틱과 ZK 사기/타당성 증명 (Rollup: Optimistic vs ZK Fraud/Validity Proof)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)([Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/))은 수백 개 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 L2에서 처리 후 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·증명하여 L1에 제출하는 확장성 기술로, 옵티미스틱(낙관적 가정+사기 증명)과 ZK(즉시 타당성 증명) 두 패러다임이 대립한다.
> 2. **가치**: 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)(Optimistic [Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/))은 범용 [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 호환이 쉬워 Arbitrum·Optimism이 TVL(Total Value Locked) 기준 L2 1~2위를 차지하고, ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 더 빠른 최종성과 높은 보안이 장점이다.
> 3. **판단 포인트**: 출금 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(7일 챌린지 vs 즉시), 연산 오버헤드(낮음 vs 높음), [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)(완전 vs 부분)이 두 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 선택의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

### L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이 필요한 이유

이더리움 L1은 TPS(Transactions Per Second) 약 15~30 수준으로 글로벌 결제·[DeFi](/knowledge-base/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/) 트래픽을 감당하기 어렵다. [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 연산을 L2로 오프로드하되 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 보안은 L1에 위탁</strong>하는 방식으로 확장성을 달성한다.

```
기존: L1에서 모든 트랜잭션 개별 실행 → TPS ≈ 15
롤업: L2에서 배치 실행 → 압축 데이터만 L1에 → TPS ≈ 2,000+
```

- **📢 섹션 요약 비유**: — "지점 창구(L2)에서 모든 거래를 처리하고, 일일 결산서([롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 배치)만 본점(L1)에 보고하는 은행 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 두 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 구조 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">옵티미스틱 롤업(Optimistic Rollup)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L2: 트랜잭션 실행 (EVM 호환)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시퀀서(Sequencer): 배치 구성 및 L1 제출</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">가정: "모든 거래는 유효하다" (낙관적)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L1 제출: 압축 calldata + 상태 루트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">챌린지 기간: 7일 (Fraud Proof 제출 가능)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출금: 7일 대기 (또는 유동성 브릿지 사용)</div></div>
<div class="kb-diagram-note">ZK 롤업(ZK Rollup)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L2: 트랜잭션 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ZK Prover: 유효성 증명(Validity Proof) 생성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L1 제출: 압축 데이터 + ZK 증명(π)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L1 Verifier: π 검증 → 즉시 최종화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출금: 즉시 (증명 검증 완료 후)</div></div>
</div>
</div>



### 핵심 비교표

| 항목 | 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) | ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) |
|:---|:---|:---|
| **증명 방식** | 사기 증명(Fraud Proof) | 타당성 증명(Validity Proof) |
| **출금 대기** | 7일 챌린지 기간 | 즉시 (수 분~수 시간) |
| **L1 연산 비용** | 낮음 (calldata만) | 높음 (ZK 증명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) |
| **Prover 비용** | 없음 | 높음 (ZK 증명 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) |
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/">EVM</a> 호환</strong> | 완전 호환 용이 | ZK-[EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 개발 필요 |
| **보안 가정** | 최소 1명의 정직한 챌린저 | 수학적 완전성 |
| **대표 사례** | Arbitrum, Optimism | zkSync Era, StarkNet |

- **📢 섹션 요약 비유**: — "옵티미스틱은 '일단 믿고 7일 안에 이의제기 없으면 OK', ZK는 '수학 증명서 첨부해서 즉시 승인'이다.

---

## Ⅲ. 비교 및 연결

### 사기 증명(Fraud Proof) 동작



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">시퀀서가 잘못된 상태 루트 제출</div>
<div class="kb-diagram-note">→ 챌린저: L1에 챌린지 트랜잭션 전송</div>
<div class="kb-diagram-note">→ L1: 문제 구간 단일 연산 재실행(Interactive Fraud Proof)</div>
<div class="kb-diagram-note">→ 위반 확인 → 시퀀서 본드 슬래싱 + 롤백</div>
</div>
</div>



Optimism Cannon, Arbitrum BOLD: [이분 탐색](/knowledge-base/studynote/08_algorithm_stats/02_sorting/028_binary_search/)(Bisection) 방식으로 문제 구간을 좁혀가는 대화형 사기 증명

### ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 호환 도전

ZK-EVM은 이더리움 Opcode를 ZK 회로(Circuit)로 변환해야 한다. 일부 [Opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/)(SHA-256, [KECCAK](/knowledge-base/studynote/09_security/02_crypto/101_sha_3/))는 ZK 증명 비용이 매우 높아 완전 [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 호환이 어렵다.

<strong>ZK-<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/">EVM</a> 호환 레벨</strong> (Vitalik Buterin [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)):
- Type 1: 완전 호환, 가장 무거운 증명
- Type 2: [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 동등, 약간 최적화
- Type 3/4: 고수준 언어([Solidity](/knowledge-base/studynote/06_ict_convergence/01_blockchain/057_solidity_smart_contract_language/)) 호환, 경량

- **📢 섹션 요약 비유**: — "옵티미스틱은 '출입증 검사 없이 들어가되 나중에 단속', ZK는 '입구에서 신분증 검사 완료 후 즉시 입장'이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 선택 기준

1. **빠른 출금이 중요한 경우**: ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) ([DeFi](/knowledge-base/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/), CEX 연동)
2. <strong>기존 <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/057_solidity_smart_contract_language/">Solidity</a> 코드 재사용</strong>: 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) (Arbitrum, [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 완전 호환)
3. **최고 보안이 필요한 경우**: ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) (수학적 완전성)
4. <strong>저비용 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a></strong>: EIP-4844(Blob) 도입 후 양쪽 모두 비용 대폭 감소

### Sequencer 중앙화 문제

현재 대부분 L2의 시퀀서(Sequencer)는 단일 주체가 운영 → [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)·검열 위험. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시퀀서(Decentralized Sequencer)</strong> 가 L2 로드맵의 핵심 과제.

### 기술사 핵심 판단
- "L2 보안은 어디서 오는가?": L1에 제출된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + L1 Fraud/Validity Proof
- "출금 7일이 왜 필요한가?": 챌린저가 사기를 감지·증명할 시간 보장
- "ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이 더 좋으면 왜 옵티미스틱이 더 많이 쓰이나?": [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 개발 성숙도

- **📢 섹션 요약 비유**: — "옵티미스틱은 법원 재판(느리지만 쉬운 진입), ZK는 현장 공증(빠르지만 공증인 비용 높음)이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **TPS 확장** | L1 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상 |
| **가스비 절감** | L1 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50배 저렴 |
| <strong>L1 보안 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/">상속</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·증명은 L1에 → 이더리움 보안 활용 |
| **EIP-4844 효과** | Blob [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 L2 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비용 추가 90% 절감 |

[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 현재 이더리움 확장성 로드맵의 핵심 전략이다. 옵티미스틱과 ZK 두 접근은 서로 다른 트레이드오프를 제공하며, 중장기적으로는 ZK-[EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 성숙에 따라 ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 우세가 예상된다.

- **📢 섹션 요약 비유**: — "[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 고속도로를 넓히는 대신, 고속도로 옆에 지름길을 만들어 결과만 보고하는 방식이 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) | ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)의 타당성 증명 기반 |
| EIP-4844 | Blob [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 비용 절감 |
| 시퀀서 | [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 순서 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) |
| 사기 증명 | 옵티미스틱 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 보안 메커니즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [롤업: 옵티미스틱과 ZK 사기 · 타당성 증명] → [옵티미스틱 롤업 보안 메커니즘]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 반 아이들의 숙제를 반장이 모아서 선생님께 한꺼번에 제출하는 것이에요.
2. 옵티미스틱은 "일단 믿고 일주일 안에 이상하면 신고해요", ZK는 "숙제마다 정답 증명서를 붙여서 바로 검사해요".
3. 덕분에 이더리움이 훨씬 빠르고 저렴하게 많은 거래를 처리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 480 / 552

← **이전**: [479. 영지식 증명 ZKP와 프라이버시 보호 (ZKP Zero-Knowledge Proof Privacy)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/479_zero_knowledge_proof_zkp_privacy/)
**다음**: [481. 샤딩과 L1 병렬 처리 (Sharding and L1 Parallel Transaction Processing)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/481_sharding_l1_parallel_processing/) →

---
