---
title: "088. Eoa Vs 89 Ca Ethereum Accounts"
date: "2026-06-07"
tags:
  - "ict_convergence"
  - "studynote-ict-convergence"
weight: 88
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이더리움의 계정 모델은 개인키(Private [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))로 통제되는 사람의 계정인 `EOA (Externally Owned Account)`와, 배포된 코드([Smart Contract](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))로 동작하는 프로그램 계정인 `CA (Contract Account)`로 이원화되어 있다.
> 2. **가치**: [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 네트워크에서 모든 상태 변화([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))는 오직 스스로 의사결정을 내리고 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비를 지불할 수 있는 EOA로부터만 시작될 수 있도록 강제하여, 시스템의 무한 루프를 막고 책임을 명확히 한다.
> 3. **판단 포인트**: 사용자의 자산 보관과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 서명은 EOA가 전담하고, 복잡한 비즈니스 로직과 다중 서명 등의 제어는 CA에 위임하는 것이 이더리움 설계의 기본 원칙이다.

---

## Ⅰ. 개요 및 필요성

비트코인이 `UTXO (Unspent Transaction Output)` 모델을 사용하여 단순한 '돈의 이동'만을 추적했다면, 이더리움은 '상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))'를 저장하고 실행할 수 있는 <strong>계정(Account) 모델</strong>을 도입했다. 이 계정 모델은 크게 `EOA (Externally Owned Account)`와 `CA (Contract Account)` 두 가지로 나뉜다.

EOA는 우리가 흔히 메타마스크(MetaMask) 같은 지갑을 통해 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 일반적인 계정이다. 오직 개인키를 가진 주체만이 이 계정을 통제할 수 있다. 반면 CA는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에 배포된 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 그 자체로, 개인키가 없으며 오직 내장된 '코드'에 의해서만 통제된다. 만약 이 두 가지가 분리되지 않았다면, 기계(코드)가 스스로 끝없이 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 발생시켜 네트워크 자원을 고갈시키거나 누가 수수료를 내야 할지 모호해지는 문제가 생겼을 것이다.

- **📢 섹션 요약 비유**: EOA는 지갑을 들고 다니며 식당 문을 열고 들어가는 '손님'이고, CA는 돈([가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비)을 받고 정해진 레시피(코드)대로 요리를 내어주는 '자동 판매기'다. 자동 판매기는 혼자서 요리를 시작하지 못한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이더리움의 모든 계정은 20바이트의 주소(Address)를 가지며, 내부적으로 4가지 필드(`Nonce`, `Balance`, `Storage Root`, `Code Hash`)를 갖는다. EOA와 CA는 이 필드들이 어떻게 채워져 있는지에 따라 구분된다.

| 계정 내부 필드 | EOA (외부 소유 계정) | [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (컨트랙트 계정) |
| :--- | :--- | :--- |
| <strong><a href="/studynote/09_security/05_web_app_security/519_oidc_nonce/">Nonce</a> (논스)</strong> | 계정에서 보낸 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)의 총 개수 | 계정이 배포한 컨트랙트의 총 개수 |
| **Balance (잔고)** | 보유한 이더([ETH](/studynote/08_algorithm_stats/06_np_theory/118_eth/))의 양 | 보유한 이더([ETH](/studynote/08_algorithm_stats/06_np_theory/118_eth/))의 양 |
| **Storage Root** | 비어 있음 (상태 저장 불가) | 컨트랙트 상태 변수가 저장된 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/) 루트 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/082_process_memory_structure/">Code</a> Hash</strong> | 비어 있음 (코드 없음) | 배포된 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)의 바이트코드 해시 |

```text
+--------------------------------------------------------------+
|            트랜잭션(Transaction) 발생과 전파 흐름          |
+--------------------------------------------------------------+
| [인간/외부 시스템]                                           |
|       | 1. 트랜잭션 생성 및 개인키 서명 (가스비 지불 약속)     |
|       v                                                      |
| +-----------+         2. 트랜잭션 전송          +-----------+|
| |    EOA    |---------------------------------->|    CA     ||
| |(코드 없음)|                                  |(코드 있음)||
| +-----------+                                  +-----------+|
|                                                      |       |
|               3. 내부 메시지(Internal Call) 발생       |       |
|               (CA는 스스로 트랜잭션을 시작할 수 없음)   v       |
|                                                +-----------+|
|                                                | 다른 CA   ||
|                                                +-----------+|
+--------------------------------------------------------------+
```
가장 중요한 원리는 <strong>"<a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>의 시작점은 항상 EOA여야 한다"</strong>는 것이다. CA는 EOA나 다른 CA로부터 메시지(호출)를 받았을 때만 깨어나서 코드를 실행하고, 다시 잠든다.

- **📢 섹션 요약 비유**: 도미노 쓰러뜨리기와 같다. EOA는 첫 번째 도미노를 손가락으로 밀어 쓰러뜨리는 유일한 존재([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 시작)이고, CA는 그 힘을 받아 다음 도미노를 차례로 쓰러뜨리는 중간 블록(내부 호출)이다.

---

## Ⅲ. 비교 및 연결

EOA와 CA는 이더리움 생태계를 굴러가게 하는 두 개의 바퀴로, 서로 명확한 트레이드오프(Trade-off)와 한계를 가진다.

| 비교 축 | EOA (외부 소유 계정) | [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (컨트랙트 계정) |
| :--- | :--- | :--- |
| **제어 권한** | 개인키 (Private [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 소유자 | 컨트랙트에 작성된 로직 ([Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) |
| <strong><a href="/studynote/06_ict_convergence/01_blockchain/024_gas/">가스</a>(<a href="/studynote/06_ict_convergence/01_blockchain/024_gas/">Gas</a>) 지불</strong> | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 발생 시 직접 지불해야 함 | 스스로 지불 불가 (EOA가 낸 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)를 소모) |
| <strong>다중 서명/<a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 불가능 (개인키 분실 시 자산 영구 상실) | 로직으로 구현 가능 (Multisig Wallet 등) |
| <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 비용</strong> | 무료 (오프라인에서 키 쌍 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) | [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비 발생 ([블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에 코드 배포 비용) |

EOA의 가장 큰 치명적 약점은 <strong>"개인키를 잃어버리면 모든 것을 잃는다"</strong>는 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))이다. 또한 복잡한 실행 조건(예: 하루 이체 한도 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), 3명 중 2명 서명 시 송금)을 스스로 부여할 수 없다. 반대로 CA는 유연한 로직 구현이 가능하지만 스스로 움직일 수 없고 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비를 낼 수 없다는 단점이 있다.

이 둘의 장점을 합치기 위해 등장한 개념이 바로 <strong><code>AA (Account Abstraction, 계정 추상화 - ERC-4337)</code></strong>이다. 사용자의 지갑 자체를 하나의 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))로 만들어, [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비 대납(Paymaster)이나 소셜 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 기능을 제공하려는 핵심 확장 흐름이다.

- **📢 섹션 요약 비유**: EOA는 열쇠를 잃어버리면 영영 열 수 없는 철제 금고이고, CA는 지문, 홍채, 비밀번호 등 다양한 조건으로 열리게 세팅할 수 있는 디지털 도어락이다. [계정 추상화](/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)([AA](/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))는 철제 금고 대신 모두에게 디지털 도어락을 달아주자는 움직임이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[DApp](/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/)([탈중앙화](/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 애플리케이션)이나 기업용 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 서비스를 설계할 때, EOA와 CA의 특성을 잘못 활용하면 심각한 보안 사고나 UX(사용자 경험) 저하로 이어진다.

### 실무 설계 판단 포인트
1. **자금 보관 및 다중 관리자 승인 (Multisig)**
   - **판단**: 기업의 운영 자금이나 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 관리자 권한을 단일 EOA에 부여하면, 해당 담당자 퇴사나 키 유출 시 치명적이다. 반드시 `Gnosis Safe` 같은 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 기반의 다중 서명 지갑을 사용하여 로직으로 자금을 통제해야 한다.
2. <strong>사용자 온보딩 및 <a href="/studynote/06_ict_convergence/01_blockchain/024_gas/">가스</a>비 장벽 (UX)</strong>
   - **판단**: 일반 사용자가 서비스에 진입하려면 EOA를 만들고 거래소에서 이더([ETH](/studynote/08_algorithm_stats/06_np_theory/118_eth/))를 사서 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비로 써야 하는 허들이 있다. 이를 극복하기 위해 메타 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(Meta-transaction)이나 `ERC-4337 (AA)` 구조를 도입해 기업(Paymaster)이 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비를 대납하도록 설계해야 한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)) 내부에 이더를 보관하면서, 인출(Withdraw) 로직을 단일 EOA 관리자만 호출할 수 있게 하드코딩하는 것. 이는 [탈중앙화](/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 철학을 위배하며 단일 키 유출이 전체 자산 탈취로 이어진다.

- **📢 섹션 요약 비유**: 회사 금고([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))를 만들었는데 열쇠(EOA)를 직원 한 명의 호주머니에만 넣어두는 것은 최악의 설계다. 반드시 사장, 재무팀장, 감사가 동시에 열쇠를 돌려야(다중 서명 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)) 열리도록 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론

이더리움이 EOA와 CA를 분리한 것은 인간의 책임([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 시작과 비용 지불)과 기계의 신뢰(결정론적 코드 실행)를 완벽히 분리하기 위한 천재적인 설계였다. 이 구조 덕분에 이더리움은 단순한 화폐 시스템을 넘어 글로벌 컴퓨터로 동작할 수 있게 되었다.

그러나 대중화(Mass Adoption)를 가로막는 가장 큰 장벽 역시 EOA의 불편한 키 관리와 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)비 구조에 있다. 결론적으로 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 미래는 EOA의 의존도를 점차 줄이고, [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 기반의 지갑([Smart Contract](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) Wallet)과 `AA (Account Abstraction)`를 통해 사용자는 웹2(Web2)처럼 쉽게 접근하면서도 웹3(Web3)의 보안을 누리는 방향으로 진화하고 있다.

- **📢 섹션 요약 비유**: 수동 변속기(EOA)는 운전의 책임을 온전히 운전자에게 묻지만 조작이 어렵다. 앞으로의 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 복잡한 조작을 자동차 시스템([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), [AA](/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))이 알아서 해주는 자동 변속기를 향해 발전하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/06_ict_convergence/01_blockchain/024_gas/">가스</a> (<a href="/studynote/06_ict_convergence/01_blockchain/024_gas/">Gas</a>)</strong> | EOA가 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 발생시킬 때 네트워크 자원 사용료로 지불하는 비용 |
| <strong><a href="/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">스마트 컨트랙트</a> (<a href="/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">Smart Contract</a>)</strong> | CA에 배포되어 [EVM](/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/)([Ethereum Virtual Machine](/studynote/06_ict_convergence/01_blockchain/023_evm_ethereum_virtual_machine/)) 위에서 실행되는 바이트코드 |
| <strong>ERC-4337 (Account <a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">Abstraction</a>)</strong> | EOA와 경계를 허물어, [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 자체가 지갑 역할을 하도록 돕는 이더리움 표준 |
| **지갑 (Wallet)** | 사용자가 EOA의 개인키를 안전하게 보관하고 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 서명하게 해주는 소프트웨어 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
UTXO (비트코인의 단순 잔고 증명)
    |
    v
Account Model 도입 (이더리움의 상태 저장)
    |
    +--> EOA (Externally Owned Account) : 키 관리, 트랜잭션 시작, 가스 지불
    +--> CA (Contract Account) : 코드 실행, 상태 저장, 내부 메시지 호출
             |
             v
Smart Contract Wallet (다중 서명, 소셜 복구 기능 등 제한적 적용)
             |
             v
Account Abstraction (ERC-4337) : 프로토콜 수준에서 EOA와 CA의 통합 및 UX 혁신
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>EOA</strong>는 네가 게임기에 동전을 넣고 '시작 버튼'을 누르는 손가락이에요.
2. <strong><a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a></strong>는 동전이 들어오면 정해진 규칙대로 캐릭터를 움직이게 해주는 게임기 안의 '프로그램'이에요.
3. 게임기([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))는 혼자서 동전을 넣거나 게임을 시작할 수 없고, 반드시 너(EOA)의 손가락이 필요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 88 / 552

<- **이전**: [87. 계정 추상화 (Account Abstraction, ERC-4337) - 이더리움 지갑(EOA)을 스마트 컨트랙트(CA)처럼 프로그래밍](/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/)
**다음**: [89. CA (Contract Account) - 코드에 의해 통제되는 컨트랙트 계정](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) ->

---
