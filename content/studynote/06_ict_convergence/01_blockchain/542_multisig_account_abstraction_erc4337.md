---
title: 542. 멀티시그와 계정 추상화 (Multi-Sig and Account Abstraction ERC-4337)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티시그(Multi-Sig, Multi-Signature)는 M-of-N 서명 구조로 단일 키 분실 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 제거하고, ERC-4337 [[087_account_abstraction_erc_4337|계정 추상화]](Account [[198_abstraction_control_data_process|Abstraction]])는 [[088_eoa_vs_89_ca_ethereum_accounts|EOA]]([[088_eoa_vs_89_ca_ethereum_accounts|Externally Owned Account]])를 [[022_smart_contract|스마트 컨트랙트]] 계정으로 업그레이드하여 **지갑 로직을 프로그래머블**하게 만든다.
> 2. **가치**: 소셜 [[658_ir_recovery|복구]](Social [[658_ir_recovery|Recovery]])·가스비 대납(Paymaster)·[[140_session_key|세션 키]]([[140_session_key|Session Key]]) 기능이 Web3 UX의 가장 큰 진입 장벽(개인키 관리·가스비)을 제거하여 **대중화 핵심 기술**이 된다.
> 3. **판단 포인트**: UserOperation → Bundler → EntryPoint 아키텍처는 기존 이더리움 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변경 없이 EIP-4337로 [[087_account_abstraction_erc_4337|계정 추상화]]를 실현하는 영리한 설계로, 기술사 시험에서 구조 이해가 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 단일 키의 위험성

이더리움 [[088_eoa_vs_89_ca_ethereum_accounts|EOA]]([[088_eoa_vs_89_ca_ethereum_accounts|Externally Owned Account]])는 개인키(Private [[067_db_key_uniqueness_minimality|Key]]) 하나로만 접근한다. 분실하면 영구 잠금, 해킹되면 전액 탈취 가능. 2022년 기준 추정 약 4백만 BTC (전체 공급의 20%)가 분실 키로 영구 잠금 상태.

- **멀티시그**: M-of-N → 예: 3-of-5 = 5개 키 중 3개로 승인
- **[[087_account_abstraction_erc_4337|계정 추상화]]**: 지갑 자체가 [[022_smart_contract|스마트 컨트랙트]] → [[658_ir_recovery|복구]]·권한 로직 [[091_kustomize_kubernetes_declarative_overlay_manifest|커스터마이즈]]

- **📢 섹션 요약 비유**: — "집 열쇠 하나를 잃어버리면 못 들어가는 대신, 여러 열쇠 중 과반수만 있으면 문이 열리는 시스템을 만드는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ERC-4337 [[087_account_abstraction_erc_4337|계정 추상화]] 구조

```
┌─────────────────────────────────────────────────────────┐
│            ERC-4337 Account Abstraction 흐름             │
│                                                         │
│  사용자                                                  │
│    │ UserOperation (서명된 의도)                         │
│    ▼                                                    │
│  Bundler (번들러)                                        │
│    │ 여러 UserOp 묶어 트랜잭션으로 L1 제출               │
│    ▼                                                    │
│  EntryPoint Contract (단일 전역 컨트랙트)                │
│    │ ① validateUserOp 검증                              │
│    │ ② Paymaster 가스비 대납 확인                        │
│    ▼                                                    │
│  스마트 컨트랙트 계정 (Smart Account)                    │
│    ├ 소셜 복구 (Social Recovery)                         │
│    ├ 세션 키 (Session Key)                               │
│    ├ 다중 서명 지원                                      │
│    └ 가스비 ERC-20으로 지불                              │
└─────────────────────────────────────────────────────────┘
```

### 멀티시그 vs ERC-4337 비교

| 항목 | 멀티시그 (Gnosis [[093_safe_scaled_agile_framework_art_pi|Safe]]) | ERC-4337 [[087_account_abstraction_erc_4337|계정 추상화]] |
|:---|:---|:---|
| **서명 구조** | M-of-N 온체인 [[395_verification_process_review|검증]] | UserOperation [[395_verification_process_review|검증]] 로직 [[091_kustomize_kubernetes_declarative_overlay_manifest|커스터마이즈]] |
| **가스비** | 서명자 중 한 명이 지불 | Paymaster가 대납 가능 |
| **[[658_ir_recovery|복구]]** | 추가 키 보관 필요 | 소셜 [[658_ir_recovery|복구]] [[022_smart_contract|스마트 컨트랙트]] |
| **UX** | 복잡(다수 서명 수집) | 단순(앱 레벨 [[198_abstraction_control_data_process|추상화]]) |
| **적용처** | [[054_dao_decentralized_autonomous_organization|DAO]] 트레저리, 기업 지갑 | 소비자 지갑, [[032_dapp_decentralized_application|DApp]] |

- **📢 섹션 요약 비유**: — "멀티시그는 금고를 열려면 이사 3명의 도장이 필요한 방식, [[087_account_abstraction_erc_4337|계정 추상화]]는 스마트폰 Face ID로 결제하는 것처럼 지갑 자체가 스마트해지는 것이다.

---

## Ⅲ. 비교 및 연결

### 주요 기능 상세

**소셜 [[658_ir_recovery|복구]](Social [[658_ir_recovery|Recovery]])**:
개인키 분실 시 사전 지정한 Guardian(친구·가족) 과반수 동의로 새 키로 계정 [[658_ir_recovery|복구]]
→ Web2의 "비밀번호 찾기" 개념을 [[010_decentralization|탈중앙화]] 방식으로 구현

**가스비 대납([[024_gas|Gas]] Sponsorship, Paymaster)**:
DApp이 사용자 가스비를 대납하거나 [[072_erc_20_fungible_token_standard|ERC-20]] 토큰으로 가스비 지불
→ "ETH가 없어도 게임 아이템 무료로 민팅" 시나리오 가능

**[[140_session_key|세션 키]]([[140_session_key|Session Key]])**:
게임·DApp에서 매 트랜잭션마다 지갑 팝업 없이 사전 승인된 범위 내 자동 서명
→ Web2 "로그인 상태 유지"와 동일한 UX

### 멀티시그 실제 활용
- **Gnosis [[093_safe_scaled_agile_framework_art_pi|Safe]]**: 최대 [[033_defi_decentralized_finance|DeFi]] [[054_dao_decentralized_autonomous_organization|DAO]] 트레저리 관리 도구, 수백억 달러 보관
- **거래소 콜드 월렛**: 3-of-5 멀티시그로 출금 보안 강화
- **기업 자산 관리**: CFO·CEO·[[606_auditing_linux_auditd|감사]] 3인 승인 구조

- **📢 섹션 요약 비유**: — "[[140_session_key|세션 키]]는 편의점 자동 결제처럼 소액 거래를 매번 서명 없이 통과시키되, 일정 금액 이상만 확인하는 스마트 지갑이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 보안 고려 사항

1. **Guardian [[009_config|설정]]**: 신뢰할 수 있는 Guardian 선정 + 시간락(Timelock) [[658_ir_recovery|복구]] 대기
2. **Bundler 신뢰**: Bundler가 UserOp 검열 가능 → [[136_variance|분산]] Bundler 필요
3. **EntryPoint [[606_auditing_linux_auditd|감사]]**: 전역 단일 컨트랙트이므로 취약점 시 전체 생태계 위협
4. **[[140_session_key|세션 키]] 범위 제한**: 너무 넓은 [[140_session_key|세션 키]] 권한은 [[032_dapp_decentralized_application|DApp]] 해킹 시 피해 최대화

### 기술사 핵심 판단
- ERC-4337은 이더리움 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변경(하드포크) 없이 [[022_smart_contract|스마트 컨트랙트]]만으로 [[087_account_abstraction_erc_4337|계정 추상화]] 달성 → 배포 즉시 모든 [[152_evm_earned_value_management|EVM]] 체인 적용 가능
- [[105_aa_as_is_analysis|AA]](Account [[198_abstraction_control_data_process|Abstraction]])와 스마트 지갑이 Web3 Mass Adoption의 UX 핵심 과제
- **[[562_passkey|Passkey]] 연동**: iOS/Android FIDO2 패스키를 스마트 계정 서명에 연동 → 지문/Face ID로 [[004_blockchain|블록체인]] 거래

- **📢 섹션 요약 비유**: — "ERC-4337은 이더리움 지갑을 '스마트폰 앱 수준의 UX'로 만드는 업그레이드 — 개인키를 직접 관리하지 않아도 되는 시대를 여는 기술이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **보안 강화** | 멀티시그로 단일 키 분실·해킹 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 제거 |
| **UX 혁신** | 가스비 대납·소셜 [[658_ir_recovery|복구]]·[[140_session_key|세션 키]]로 진입 장벽 제거 |
| **[[054_dao_decentralized_autonomous_organization|DAO]] 트레저리** | Gnosis [[093_safe_scaled_agile_framework_art_pi|Safe]] 멀티시그로 수십억 달러 안전 관리 |
| **대중화 가속** | 스마트폰 수준의 지갑 UX → Web3 신규 사용자 유입 |

멀티시그와 ERC-4337 [[087_account_abstraction_erc_4337|계정 추상화]]는 [[004_blockchain|블록체인]] 지갑 보안과 사용성을 동시에 높이는 핵심 기술이다. Web3 대중화를 위해서는 "개인키 없는 지갑" 경험이 필수이며, [[087_account_abstraction_erc_4337|계정 추상화]]가 그 핵심 솔루션이다.

- **📢 섹션 요약 비유**: — "Web2에서 '비밀번호 없는 로그인([[562_passkey|Passkey]])'이 UX 혁신이었다면, Web3에서는 '개인키 없는 지갑([[087_account_abstraction_erc_4337|계정 추상화]])'이 같은 혁신이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [[083_relationship_in_er_model|관계]] 설명 |
| [[088_eoa_vs_89_ca_ethereum_accounts|EOA]] | [[087_account_abstraction_erc_4337|계정 추상화]]의 출발점, 개인키 기반 계정 |
| Gnosis [[093_safe_scaled_agile_framework_art_pi|Safe]] | 대표적 멀티시그 스마트 지갑 |
| Paymaster | ERC-4337 가스비 대납 [[603_component_independent_deployment_unit|컴포넌트]] |
| 소셜 [[658_ir_recovery|복구]] | 키 분실 방어를 위한 [[087_account_abstraction_erc_4337|계정 추상화]] 기능 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [멀티시그 · 계정 추상화] → [키 분실 방어를 위한 계정 추상화 기능]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 멀티시그는 금고 열쇠를 여러 명이 나눠 가져서 과반수가 동의해야 열리는 안전한 방식이에요.
2. [[087_account_abstraction_erc_4337|계정 추상화]]는 [[004_blockchain|블록체인]] 지갑을 스마트폰 앱처럼 만드는 것 — 지문으로 로그인하고, 친구가 비밀번호를 대신 찾아줄 수 있어요.
3. 덕분에 더 많은 사람이 어렵지 않게 [[004_blockchain|블록체인]]을 사용할 수 있게 돼요.
