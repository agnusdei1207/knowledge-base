+++
title = "542. 멀티시그와 계정 추상화 (Multi-Sig and Account Abstraction ERC-4337)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티시그(Multi-Sig, Multi-Signature)는 M-of-N 서명 구조로 단일 키 분실 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 제거하고, ERC-4337 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)(Account [Abstraction](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/))는 [EOA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/088_eoa_vs_89_ca_ethereum_accounts/)([Externally Owned Account](/knowledge-base/studynote/06_ict_convergence/01_blockchain/088_eoa_vs_89_ca_ethereum_accounts/))를 [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 계정으로 업그레이드하여 <strong>지갑 로직을 프로그래머블</strong>하게 만든다.
> 2. **가치**: 소셜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Social [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))·가스비 대납(Paymaster)·[세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)([Session Key](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)) 기능이 Web3 UX의 가장 큰 진입 장벽(개인키 관리·가스비)을 제거하여 <strong>대중화 핵심 기술</strong>이 된다.
> 3. **판단 포인트**: UserOperation -> Bundler -> EntryPoint 아키텍처는 기존 이더리움 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변경 없이 EIP-4337로 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)를 실현하는 영리한 설계로, 기술사 시험에서 구조 이해가 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 단일 키의 위험성

이더리움 [EOA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/088_eoa_vs_89_ca_ethereum_accounts/)([Externally Owned Account](/knowledge-base/studynote/06_ict_convergence/01_blockchain/088_eoa_vs_89_ca_ethereum_accounts/))는 개인키(Private [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 하나로만 접근한다. 분실하면 영구 잠금, 해킹되면 전액 탈취 가능. 2022년 기준 추정 약 4백만 BTC (전체 공급의 20%)가 분실 키로 영구 잠금 상태.

- **멀티시그**: M-of-N -> 예: 3-of-5 = 5개 키 중 3개로 승인
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/">계정 추상화</a></strong>: 지갑 자체가 [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) -> [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·권한 로직 [커스터마이즈](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/)

- **📢 섹션 요약 비유**: — "집 열쇠 하나를 잃어버리면 못 들어가는 대신, 여러 열쇠 중 과반수만 있으면 문이 열리는 시스템을 만드는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ERC-4337 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/) 구조

```
+---------------------------------------------------------+
|            ERC-4337 Account Abstraction 흐름             |
|                                                         |
|  사용자                                                  |
|    | UserOperation (서명된 의도)                         |
|    v                                                    |
|  Bundler (번들러)                                        |
|    | 여러 UserOp 묶어 트랜잭션으로 L1 제출               |
|    v                                                    |
|  EntryPoint Contract (단일 전역 컨트랙트)                |
|    | ① validateUserOp 검증                              |
|    | ② Paymaster 가스비 대납 확인                        |
|    v                                                    |
|  스마트 컨트랙트 계정 (Smart Account)                    |
|    + 소셜 복구 (Social Recovery)                         |
|    + 세션 키 (Session Key)                               |
|    + 다중 서명 지원                                      |
|    + 가스비 ERC-20으로 지불                              |
+---------------------------------------------------------+
```

### 멀티시그 vs ERC-4337 비교

| 항목 | 멀티시그 (Gnosis [Safe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)) | ERC-4337 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/) |
|:---|:---|:---|
| **서명 구조** | M-of-N 온체인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | UserOperation [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직 [커스터마이즈](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) |
| **가스비** | 서명자 중 한 명이 지불 | Paymaster가 대납 가능 |
| <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 추가 키 보관 필요 | 소셜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) |
| **UX** | 복잡(다수 서명 수집) | 단순(앱 레벨 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)) |
| **적용처** | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 트레저리, 기업 지갑 | 소비자 지갑, [DApp](/knowledge-base/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/) |

- **📢 섹션 요약 비유**: — "멀티시그는 금고를 열려면 이사 3명의 도장이 필요한 방식, [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)는 스마트폰 Face ID로 결제하는 것처럼 지갑 자체가 스마트해지는 것이다.

---

## Ⅲ. 비교 및 연결

### 주요 기능 상세

<strong>소셜 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>(Social <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">Recovery</a>)</strong>:
개인키 분실 시 사전 지정한 Guardian(친구·가족) 과반수 동의로 새 키로 계정 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)
-> Web2의 "비밀번호 찾기" 개념을 [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 방식으로 구현

<strong>가스비 대납(<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/">Gas</a> Sponsorship, Paymaster)</strong>:
DApp이 사용자 가스비를 대납하거나 [ERC-20](/knowledge-base/studynote/06_ict_convergence/01_blockchain/072_erc_20_fungible_token_standard/) 토큰으로 가스비 지불
-> "ETH가 없어도 게임 아이템 무료로 민팅" 시나리오 가능

<strong><a href="/knowledge-base/studynote/09_security/03_network_security/140_session_key/">세션 키</a>(<a href="/knowledge-base/studynote/09_security/03_network_security/140_session_key/">Session Key</a>)</strong>:
게임·DApp에서 매 트랜잭션마다 지갑 팝업 없이 사전 승인된 범위 내 자동 서명
-> Web2 "로그인 상태 유지"와 동일한 UX

### 멀티시그 실제 활용
- <strong>Gnosis <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/">Safe</a></strong>: 최대 [DeFi](/knowledge-base/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/) [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 트레저리 관리 도구, 수백억 달러 보관
- **거래소 콜드 월렛**: 3-of-5 멀티시그로 출금 보안 강화
- **기업 자산 관리**: CFO·CEO·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 3인 승인 구조

- **📢 섹션 요약 비유**: — "[세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)는 편의점 자동 결제처럼 소액 거래를 매번 서명 없이 통과시키되, 일정 금액 이상만 확인하는 스마트 지갑이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 보안 고려 사항

1. <strong>Guardian <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: 신뢰할 수 있는 Guardian 선정 + 시간락(Timelock) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 대기
2. **Bundler 신뢰**: Bundler가 UserOp 검열 가능 -> [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) Bundler 필요
3. <strong>EntryPoint <a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: 전역 단일 컨트랙트이므로 취약점 시 전체 생태계 위협
4. <strong><a href="/knowledge-base/studynote/09_security/03_network_security/140_session_key/">세션 키</a> 범위 제한</strong>: 너무 넓은 [세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/) 권한은 [DApp](/knowledge-base/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/) 해킹 시 피해 최대화

### 기술사 핵심 판단
- ERC-4337은 이더리움 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변경(하드포크) 없이 [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)만으로 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/) 달성 -> 배포 즉시 모든 [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 체인 적용 가능
- [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)(Account [Abstraction](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/))와 스마트 지갑이 Web3 Mass Adoption의 UX 핵심 과제
- <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/562_passkey/">Passkey</a> 연동</strong>: iOS/Android FIDO2 패스키를 스마트 계정 서명에 연동 -> 지문/Face ID로 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 거래

- **📢 섹션 요약 비유**: — "ERC-4337은 이더리움 지갑을 '스마트폰 앱 수준의 UX'로 만드는 업그레이드 — 개인키를 직접 관리하지 않아도 되는 시대를 여는 기술이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **보안 강화** | 멀티시그로 단일 키 분실·해킹 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 제거 |
| **UX 혁신** | 가스비 대납·소셜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·[세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)로 진입 장벽 제거 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/">DAO</a> 트레저리</strong> | Gnosis [Safe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/) 멀티시그로 수십억 달러 안전 관리 |
| **대중화 가속** | 스마트폰 수준의 지갑 UX -> Web3 신규 사용자 유입 |

멀티시그와 ERC-4337 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 지갑 보안과 사용성을 동시에 높이는 핵심 기술이다. Web3 대중화를 위해서는 "개인키 없는 지갑" 경험이 필수이며, [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)가 그 핵심 솔루션이다.

- **📢 섹션 요약 비유**: — "Web2에서 '비밀번호 없는 로그인([Passkey](/knowledge-base/studynote/09_security/11_iam_access_control/562_passkey/))'이 UX 혁신이었다면, Web3에서는 '개인키 없는 지갑([계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/))'이 같은 혁신이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| [EOA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/088_eoa_vs_89_ca_ethereum_accounts/) | [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)의 출발점, 개인키 기반 계정 |
| Gnosis [Safe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/) | 대표적 멀티시그 스마트 지갑 |
| Paymaster | ERC-4337 가스비 대납 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) |
| 소셜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 키 분실 방어를 위한 [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/) 기능 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] -> [멀티시그 · 계정 추상화] -> [키 분실 방어를 위한 계정 추상화 기능]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 멀티시그는 금고 열쇠를 여러 명이 나눠 가져서 과반수가 동의해야 열리는 안전한 방식이에요.
2. [계정 추상화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 지갑을 스마트폰 앱처럼 만드는 것 — 지문으로 로그인하고, 친구가 비밀번호를 대신 찾아줄 수 있어요.
3. 덕분에 더 많은 사람이 어렵지 않게 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)을 사용할 수 있게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 542 / 552

<- **이전**: [541. 베어메탈 클라우드 가상화 오버헤드 없는 서비스 (Bare Metal Cloud No Hypervisor)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/541_bare_metal_cloud_no_hypervisor/)
**다음**: [543. SBT 소울바운드 토큰과 신원 인증 (SBT Soulbound Token Identity Credential)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/543_sbt_soulbound_token_identity/) ->

---
