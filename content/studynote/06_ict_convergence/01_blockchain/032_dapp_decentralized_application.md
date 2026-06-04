---
title: "DApp (Decentralized Application, 분산 애플리케이션)"
date: "2026-03-03"
tags:
  - "studynote-ict-convergence"
---


> **핵심 인사이트 3줄**
> 1. DApp([Decentralized Application](/studynote/04_software_engineering/09_cloud_native_ai_architecture/592_blockchain_dapp_architecture_ipfs/))은 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)를 백엔드로 사용해 중앙 서버 없이 동작하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 애플리케이션이다.
> 2. [탈중앙화](/studynote/06_ict_convergence/01_blockchain/010_decentralization/)·검열 [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)·투명성이 강점이지만, 느린 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 속도·높은 가스비·UX 복잡성이 대중화의 장벽이다.
> 3. [DeFi](/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/)·NFT 마켓·[DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 거버넌스·게임파이(GameFi) 등 Web3 생태계의 핵심 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레이어로 진화하고 있다.

---

## Ⅰ. DApp의 정의와 특성

DApp([Decentralized Application](/studynote/04_software_engineering/09_cloud_native_ai_architecture/592_blockchain_dapp_architecture_ipfs/))은 <strong>백엔드 로직을 <a href="/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a> <a href="/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">스마트 컨트랙트</a>로 구현한 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 애플리케이션</strong>이다.

| 특성              | 중앙화 앱           | DApp                       |
|-----------------|-------------------|---------------------------|
| 백엔드            | 중앙 서버           | [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) ([블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/))  |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장       | 중앙 DB            | [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)·[IPFS](/studynote/06_ict_convergence/01_blockchain/055_ipfs_interplanetary_file_system/)              |
| 운영자 통제       | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 가능    | 자율 실행, 중단 불가         |
| 투명성           | 블랙박스            | 코드 공개·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능          |
| [사용자 인증](/studynote/02_operating_system/10_security/604_authentication_factors/)       | ID/PW              | 지갑(개인키) 기반            |

### DApp 아키텍처

```
사용자 브라우저
   | Web3.js / Ethers.js
   v
프론트엔드 (IPFS/Vercel)
   |
MetaMask (지갑 연결)
   |
이더리움 노드 (Infura/Alchemy)
   |
스마트 컨트랙트 (Solidity)
   |
EVM (Ethereum Virtual Machine)
```

📢 **섹션 요약 비유**: DApp은 자판기다 — 주인 없이 동전([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))을 넣으면 규칙(컨트랙트)에 따라 자동으로 결과가 나온다.

---

## Ⅱ. [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)와 상호작용

### [Solidity](/studynote/06_ict_convergence/01_blockchain/057_solidity_smart_contract_language/) [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 예시

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedData;

    function set(uint256 x) public {
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
```

### [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 흐름

```
사용자 서명 -> MetaMask -> 이더리움 노드 -> 컨트랙트 실행
     v                                          v
  개인키 사용                            상태 변경 + 가스비 소모
```

📢 **섹션 요약 비유**: [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)는 자동 계약서다 — 조건이 충족되면 변호사 없이 자동으로 실행되고, 한번 배포되면 변경할 수 없다.

---

## Ⅲ. DApp 주요 카테고리

| 카테고리    | 예시                    | 핵심 기능                     |
|------------|------------------------|------------------------------|
| [DeFi](/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/)       | Uniswap, Aave, Compound | 탈중앙 거래소·대출·이자       |
| NFT 마켓   | OpenSea, Blur           | 디지털 자산 소유권 거래        |
| GameFi     | Axie Infinity, StepN    | P2E (Play-to-Earn)            |
| [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)        | MakerDAO, Uniswap [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)   | 토큰 기반 거버넌스             |
| 소셜       | Lens [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), Farcaster | 탈중앙 SNS                   |
| 스토리지   | Filecoin, Arweave       | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장                 |

📢 **섹션 요약 비유**: DApp 카테고리는 현실 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 탈중앙 버전이다 — DeFi는 은행, NFT는 경매장, DAO는 주주총회, GameFi는 게임 회사가 없는 게임이다.

---

## Ⅳ. DApp 기술 스택과 개발 도구

```
+----------------------------------------------+
|  프론트엔드: React/Vue + Web3.js/Ethers.js   |
+----------------------------------------------+
|  지갑 연결: MetaMask / WalletConnect         |
+----------------------------------------------+
|  스마트 컨트랙트: Solidity / Vyper           |
+----------------------------------------------+
|  개발 프레임워크: Hardhat / Foundry / Truffle|
+----------------------------------------------+
|  블록체인 노드: Infura / Alchemy / 자체 노드 |
+----------------------------------------------+
|  분산 스토리지: IPFS / Arweave               |
+----------------------------------------------+
```

**L2 확장 솔루션**: [Polygon](/studynote/06_ict_convergence/01_blockchain/045_sidechain_bridge_polygon/)·Arbitrum·Optimism으로 가스비 절감 + 속도 개선

📢 **섹션 요약 비유**: DApp 스택은 현대 웹사이트 구조와 같지만, 서버 대신 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)이 있고 DB 대신 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지가 있다.

---

## Ⅴ. DApp의 한계와 Web3 미래

### 현재 한계

| 한계           | 원인                       | 해결 방향               |
|--------------|---------------------------|------------------------|
| 느린 속도     | 블록 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시간 (12초/이더리움) | L2·[샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)               |
| 높은 가스비   | 네트워크 혼잡도              | EIP-1559, L2           |
| UX 복잡성    | 지갑·개인키 관리              | [AA](/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)([계정 추상화](/studynote/06_ict_convergence/01_blockchain/087_account_abstraction_erc_4337/))         |
| 확장성        | 트릴레마 (속도/탈중앙/보안)   | [롤업](/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)·[샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)              |
| [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 버그 | 배포 후 수정 불가        | 업그레이더블 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)     |

### Web3 발전 방향

```
Web1 (읽기) -> Web2 (읽기+쓰기) -> Web3 (읽기+쓰기+소유)
                                     v
                               DApp + DID + 토큰 이코노미
```

📢 **섹션 요약 비유**: DApp의 현재 한계는 초창기 인터넷과 같다 — 느리고 불편하지만, 인프라가 성숙해지면 지금의 앱스토어처럼 당연한 것이 될 것이다.

---

## 📌 관련 개념 맵

```
DApp (Decentralized Application)
+-- 기반 기술
|   +-- 스마트 컨트랙트 (Smart Contract)
|   +-- EVM (Ethereum Virtual Machine)
|   +-- IPFS (분산 스토리지)
+-- 지갑 연결
|   +-- MetaMask
|   +-- WalletConnect
|   +-- AA (Account Abstraction)
+-- 카테고리
|   +-- DeFi (탈중앙 금융)
|   +-- NFT 마켓플레이스
|   +-- DAO (탈중앙 자율 조직)
|   +-- GameFi / SocialFi
+-- 확장 솔루션 (L2)
    +-- Polygon
    +-- Arbitrum / Optimism (롤업)
    +-- zkSync (ZK-롤업)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|                   DApp 발전 흐름                                 |
+--------------+--------------------+-----------------------------+
| 2015년       | 이더리움 출시       | 스마트 컨트랙트·EVM 등장     |
| 2017년       | CryptoKitties      | NFT·GameFi 원형              |
| 2018~19년    | DeFi 초기 (MakerDAO) | 탈중앙 금융 개념 확립      |
| 2020년       | DeFi Summer        | Uniswap·Compound 급성장      |
| 2021년       | NFT 붐·GameFi 등장 | OpenSea·Axie Infinity        |
| 2022~현재    | L2 성장·AA         | 확장성 개선·UX 단순화        |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
블록체인 -> 스마트 컨트랙트 -> DApp -> DeFi/NFT/DAO
    v             v            v
  EVM          Solidity     Web3.js
    v
  L2 롤업 -> zkEVM -> 모바일 DApp 대중화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. DApp은 주인 없는 자판기다 — 규칙([스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))에 따라 자동으로 작동하고, 아무도 임의로 규칙을 바꿀 수 없다.
2. 지갑(MetaMask)은 비밀번호 대신 열쇠다 — 열쇠를 가진 사람만 자기 돈을 쓸 수 있고, 열쇠를 잃으면 돈도 잃는다.
3. DeFi는 은행 없는 은행이다 — 직원도 본사도 없지만 이자를 주고받고 대출도 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 32 / 552

<- **이전**: [31. 니모닉 시드 구문 심화 — BIP-39 보안과 파생](/studynote/06_ict_convergence/01_blockchain/031_mnemonic_seed_phrase/)
**다음**: [DeFi (Decentralized Finance, 탈중앙화 금융)](/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/) ->

---
