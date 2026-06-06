---
title: "063. Mempool Transaction Queue"
tags:
  - "ict_convergence"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멤풀(Mempool)은 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에 아직 포함되지 않은 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 네트워크 노드에 임시로 대기하는 공간이다.
> 2. **가치**: 멤풀은 수수료 시장과 블록 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 우선순위를 형성해, 거래 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 비용을 사실상 결정한다.
> 3. **판단**: 확인되지 않은 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 최종 합의가 아니므로, 지갑과 노드 운영은 멤풀 특성을 반영해야 한다.

---

## Ⅰ. 개요 및 필요성

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 거래를 즉시 확정하지 않는다. 먼저 네트워크에 퍼뜨리고, 채굴자나 검증자가 선택한 뒤 블록에 넣어야 한다.

그 사이의 대기 공간이 멤풀이다. 멤풀을 이해해야 왜 수수료가 오르면 거래가 빨라지고, 네트워크가 막히면 확인이 늦어지는지 설명할 수 있다.

- **📢 섹션 요약 비유**: 식당 번호표를 뽑고 기다리는 대기실과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Wallet
  v
P2P Network
  v
Mempool
  v
Miner / Validator Selection
  v
Block
  v
Blockchain
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Wallet | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| Node | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 수신 및 보관 |
| Mempool | 미확정 거래 임시 저장 |
| Block Producer | 거래 선택 및 블록 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

[트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 수수료, 입력/출력, [nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/) 같은 조건을 기준으로 멤풀에서 경쟁한다. 결국 멤풀은 단순한 큐가 아니라 수수료 시장의 전장이다.

- **📢 섹션 요약 비유**: 줄서기 대기표에 팁을 많이 내는 손님이 먼저 들어가는 구조다.

---

## Ⅲ. 비교 및 연결

| 구분 | Mempool | [Blockchain](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) | Wallet [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) |
| :-- | :-- | :-- | :-- |
| 상태 | 미확정 | 확정 | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 대기 |
| 지속성 | 짧음 | 길음 | 사용자 측 임시 |
| 의미 | 우선순위 대기 | 최종 기록 | 전송 준비 |

| 네트워크 | 특징 |
| :-- | :-- |
| Bitcoin | 수수료 기반 우선순위가 강함 |
| Ethereum | [Gas](/studynote/06_ict_convergence/01_blockchain/024_gas/) 가격과 nonce가 중요함 |

멤풀은 합의 그 자체가 아니라 합의 이전의 예비 공간이다. 따라서 멤풀 상태만 보고 거래가 끝났다고 말하면 안 된다.

- **📢 섹션 요약 비유**: 대기실에서 이름이 불려도 진료가 끝난 것은 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 수수료 추정 로직이 있는가?
2. [nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/) 충돌과 거래 재전송을 관리하는가?
3. 네트워크 혼잡 시 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 설명할 수 있는가?
4. Replace-By-Fee(RBF) 같은 정책을 이해하는가?
5. 미확정 거래를 확정으로 오해하지 않는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 낮은 수수료로만 보내고 왜 안 들어가냐고 묻는 설계
- [nonce](/studynote/09_security/05_web_app_security/519_oidc_nonce/) 관리 없이 여러 거래를 동시에 보내는 설계
- 멤풀과 블록 확정을 같은 의미로 쓰는 설계
- 네트워크 혼잡을 고려하지 않는 지갑 설계

기술사 관점에서는 멤풀을 "대기열"로만 보지 말고, 수수료 시장과 확정 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 연결고리로 봐야 한다. 이 관점이 있어야 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) UX를 제대로 설명할 수 있다.

- **📢 섹션 요약 비유**: 입장권을 먼저 사면 빨리 들어가고, 늦게 사면 오래 기다리는 놀이공원 줄과 같다.

---

## Ⅴ. 기대효과 및 결론

멤풀을 이해하면 거래 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 수수료 상승, 재전송 문제를 설명할 수 있다. 결국 사용자는 "보냈다"와 "확정됐다"의 차이를 알아야 한다.

결론적으로 멤풀은 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 거래의 대기실이자 가격 결정장치다.

- **📢 섹션 요약 비유**: 줄을 서서 기다리는 동안에도 순서와 비용이 정해진다.

---

## 관련 개념 맵

```text
Transaction
  v
Mempool
  v
Block Inclusion
  v
Confirmation
```

---

## 관련 키워드 및 발전 흐름도

```text
거래 생성
  v
네트워크 전파
  v
멤풀 대기
  v
블록 포함
```

---

## 어린이를 위한 3줄 비유 설명

놀이공원에 들어가려면 먼저 줄을 서야 해요.
앞줄에 서는 사람은 더 빨리 들어가요.
멤풀은 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 거래가 기다리는 줄이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 63 / 552

<- **이전**: [62. 비트코인 반감기 (Halving) - 약 4년마다 채굴 보상이 절반으로 줄어드는 메커니즘](/studynote/06_ict_convergence/01_blockchain/062_bitcoin_halving_supply_shock/)
**다음**: [64. BFT 합의의 3단계 - Pre-prepare, Prepare, Commit](/studynote/06_ict_convergence/01_blockchain/064_bft_pbft_consensus_3_phases/) ->

---
