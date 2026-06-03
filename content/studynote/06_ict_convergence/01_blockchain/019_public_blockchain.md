---
title: 19. 퍼블릭 블록체인 (Public Blockchain) - 누구나 참여 가능 (비트코인, 이더리움)
date: '2026-03-04'
description: 중앙 통제 기관 없이 누구나 자유롭게 네트워크에 참여하고 트랜잭션을 검증할 수 있는 무허가형(Permissionless) 개방형
  분산 원장 기술
tags:
- ict_convergence
---

# 19. 퍼블릭 [[004_blockchain|블록체인]] (Public [[004_blockchain|Blockchain]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사전에 허가를 받지 않아도([[076_permissionless_vs_permissioned_blockchain|Permissionless]]) 누구나 노드를 구성하여 읽기, [[289_cqrs_db|쓰기]], [[395_verification_process_review|검증]] 등 네트워크의 모든 권한을 행사할 수 있는 극단적 개방형 [[136_variance|분산]] 원장 기술이다.
> 2. **가치**: 검열 저항성(Censorship [[003_resistance|Resistance]])과 [[454_spof|단일 장애점]]([[454_spof|SPOF]]) 부재를 통해 특정 정부나 기업의 통제를 받지 않는 글로벌 신뢰 자산 및 [[022_smart_contract|스마트 컨트랙트]] 실행 플랫폼을 제공한다.
> 3. **융합**: Web 3.0의 근간 인프라로서, 디파이([[033_defi_decentralized_finance|DeFi]]), NFT, [[054_dao_decentralized_autonomous_organization|DAO]] 등의 [[010_decentralization|탈중앙화]] 애플리케이션([[032_dapp_decentralized_application|DApp]]) 생태계가 구동되는 베이스 레이어(Layer 1) 역할을 수행한다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

퍼블릭 [[004_blockchain|블록체인]] (Public [[004_blockchain|Blockchain]])은 네트워크 참여에 어떠한 신원 [[396_validation|확인]]이나 승인 절차도 요구하지 않는([[076_permissionless_vs_permissioned_blockchain|Permissionless]]), 전 세계 누구에게나 100% 개방된 [[004_blockchain|블록체인]] 시스템이다. 인터넷에 연결된 컴퓨터만 있으면 누구나 전체 장부를 다운로드([[083_full_node_complete_ledger|Full Node]])하여 거래를 [[395_verification_process_review|검증]]하고 새로운 블록을 [[087_process_state_transition|생성]]하는 합의 과정에 직접 참여할 수 있다. 비트코인(Bitcoin)과 이더리움(Ethereum)이 가장 대표적인 퍼블릭 [[004_blockchain|블록체인]]이다.

이러한 개방형 아키텍처가 필요해진 궁극적인 배경은 '신뢰의 주체'를 중앙 집중형 기관(은행, 정부)에서 '수학적 [[001_algorithm_definition|알고리즘]]과 대중의 합의'로 옮기기 위함이다. 기존의 금융 시스템이나 서버-클라이언트 모델 구조는 해킹, 내부자 조작, 혹은 국가의 강제 검열에 의해 [[001_dikw_pyramid|데이터]]가 위변조되거나 시스템이 셧다운될 수 있는 치명적인 [[454_spof|단일 장애점]]([[454_spof|SPOF]])을 가지고 있었다. 퍼블릭 [[004_blockchain|블록체인]]은 수만 대의 익명 노드에 동일한 원장을 [[136_variance|분산]] 저장하여, 누군가가 강제로 시스템을 끄거나 특정인의 자산을 검열(동결)하는 것을 원천적으로 불가능하게 만드는 무신뢰성(Trustless) 환경을 제공하기 위해 탄생했다.

이 그림은 기존 중앙 통제형 네트워크와 퍼블릭 [[004_blockchain|블록체인]]의 위상 구조 차이를 명확히 보여준다.
```text
┌────────────────────────────────────────────────────────┐
│ [기존 구조 한계: 중앙 서버 의존형 (Client-Server)]     │
│       Client A ──┐             ┌── Client C            │
│                  ↓             ↓                       │
│              [ 중앙 데이터베이스 (은행) ]              │
│  ※ 중앙 DB 장애, 해킹, 관리자 조작 시 전체 시스템 마비│
├────────────────────────────────────────────────────────┤
│ [퍼블릭 블록체인: P2P 무허가형 분산 원장]              │
│       Node A ←───────→ Node B ←───────→ Node C        │
│         ↕      (누구나 접속/탈퇴 자유)      ↕          │
│       Node D ←───────→ Node E ←───────→ Node F        │
│  ※ 특정 노드가 파괴되어도 전체 네트워크는 100% 정상 가동│
└────────────────────────────────────────────────────────┘
```
이 도식의 핵심은 시스템의 생존성이 특정 서버나 기업에 의존하지 않는다는 점이다. 이런 배치는 권력이 단일 노드에 집중되지 않게 [[136_variance|분산]]시키기 때문이며, 따라서 외부의 물리적 공격이나 법적 규제로 네트워크 전체를 정지시키는 검열(Censorship)이 불가능하다. 실무에서는 이처럼 완벽한 [[010_decentralization|탈중앙화]] 시스템을 유지하기 위해, 익명의 노드들이 자신의 자원(전기, 지분)을 소모하여 합의에 참여하도록 유도하는 강력한 코인 보상 메커니즘([[026_token_economy|Token Economy]])이 필수적으로 결합되어야만 한다.

📢 **섹션 요약 비유**: 입장을 위해 까다로운 심사와 회원증이 필요한 고급 프라이빗 클럽이 아니라, 전 세계 누구나 신분 [[396_validation|확인]] 없이 자유롭게 들어가서 발언하고 기록을 [[396_validation|확인]]할 수 있는 열린 광장(Public [[341_iso_iec_25010|Square]])과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

퍼블릭 [[004_blockchain|블록체인]]의 아키텍처는 악의적인 해커를 포함한 익명의 대중이 참여함을 전제로 하므로, 시스템 내부에서 스스로 [[003_integrity|무결성]]을 지키고 정직한 행동을 강제하는 암호학적 및 경제학적 설계가 정교하게 맞물려 돌아간다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | [[295_protocol_field_tcp_udp_icmp|프로토콜]] 연계 | 비유 |
|:---|:---|:---|:---|:---|
| **[[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] Network** | 글로벌 통신망 유지 | 중앙 서버 없이 가십 [[295_protocol_field_tcp_udp_icmp|프로토콜]](Gossip)로 [[191_transaction_concept_states|트랜잭션]]과 블록 [[001_dikw_pyramid|데이터]]를 노드 간 전파 | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 기반 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] | 소문 퍼뜨리기 |
| **[[083_full_node_complete_ledger|Full Node]] ([[083_full_node_complete_ledger|풀 노드]])** | 장부의 독립적 [[395_verification_process_review|검증]] | 제네시스 블록부터 모든 거래 내역을 저장하고 규칙 위반 [[191_transaction_concept_states|트랜잭션]]을 거부 | [[395_verification_process_review|검증]] 엔진 | 스스로 회계장부 [[289_cqrs_db|쓰기]] |
| **Consensus ([[011_consensus_algorithm|합의 알고리즘]])** | 익명 노드 간의 상태 일치 | PoW, PoS 등을 통해 누구나 합의에 참여하되, 악의적 조작 비용을 천문학적으로 높임 | PoW, PoS | 광장 다수결 투표 |
| **[[026_token_economy|Token Economy]]** | 네트워크 유지 동기 부여 | 올바른 블록 [[087_process_state_transition|생성]] 노드에게 블록 보상(Coin) 및 [[191_transaction_concept_states|트랜잭션]] 수수료([[024_gas|Gas]]) 지급 | 보상 컨트랙트 | 수고비(인센티브) 지급 |
| **Cryptographic Primitives** | 소유권 및 [[442_consistency_integrity|무결성 보장]] | 타원 곡선 암호([[097_ecdsa_schnorr_signature_bitcoin|ECDSA]]) 비대칭 키 지갑, SHA-256 [[667_hash_function_integrity_one_way|해시 함수]], [[007_merkle_tree|머클 트리]] | 암호화 체계 | 변조 방지 지문 |

다음은 퍼블릭 [[004_blockchain|블록체인]]에서 사용자의 [[191_transaction_concept_states|트랜잭션]]이 익명의 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 네트워크를 거쳐 최종적으로 블록에 기록되는 과정을 나타낸 순차 흐름도이다.

```text
[퍼블릭 블록체인 트랜잭션 전파 및 검증 흐름도]

[사용자 A 지갑] --(1. 송금 서명 후 전파)--> [인접 노드들]
                                             │
   ┌─────────────────────────────────────────┘
   │ (2. Gossip 알고리즘을 통해 전 세계 수만 개 노드로 브로드캐스트)
   ↓
[각 노드의 Mempool (대기열)] --(3. 트랜잭션 유효성 1차 검증)--> [유효한 Tx만 적재]
   │
   └─ (4. 채굴자/검증자 노드가 Mempool에서 수수료가 높은 Tx들을 모아 블록 생성 시도)
   │
[새 블록 생성 (PoW 해시 도출 완료)] --(5. 블록 전파)--> [전체 네트워크]
   │
   └─ (6. 모든 Full Node들이 새 블록을 검증하고, 이상 없으면 원장에 추가 확정)
```
이 흐름의 핵심은 거래를 [[087_process_state_transition|생성]]한 자, 전파하는 자, [[395_verification_process_review|검증]]하는 자, 블록을 만드는 자 모두가 서로 누군지 모르는 익명의 상태에서 각자의 경제적 이익(수수료/보상)을 위해 기계적으로 움직인다는 점이다. 이런 배치는 중앙의 관리자 개입 없이도 시스템이 자체적으로 굴러가게 만들기 때문이며, 따라서 네트워크는 365일 24시간 중단 없이 완전 자율적으로 동작한다. 실무에서는 수많은 노드에 [[001_dikw_pyramid|데이터]]가 브로드캐스트되는 데 물리적 시간이 소요되므로, 초당 [[191_transaction_concept_states|트랜잭션]] [[139_throughput|처리량]](TPS)이 [[020_private_blockchain|프라이빗 블록체인]] 대비 구조적으로 매우 낮게 제한되는 병목을 감수해야 한다.

이러한 [[010_decentralization|탈중앙화]]와 [[282_performance_tactics|성능]] 간의 상충 관계를 설명하는 것이 바로 [[040_blockchain_trilemma|블록체인 트릴레마]](Trilemma)이다.

```text
[퍼블릭 블록체인의 트릴레마 구조도]

          [Decentralization (탈중앙화)]
                  ▲
                 / \
   퍼블릭 포지션 /   \
 (비트코인,이더)/_____\
               /       \
[Security] ───/─────────\─── [Scalability (확장성/성능)]
(보안성)                     (프라이빗 블록체인 포지션)

※ 퍼블릭 체인은 누구나 참여하는 '탈중앙화'와 공격을 막는 '보안성'을
   극대화하기 위해 필연적으로 '성능(TPS)'을 희생하게 설계된다.
```
이 그림은 왜 퍼블릭 [[004_blockchain|블록체인]]이 기업용 중앙 시스템보다 느린지를 수학적, 구조적 한계로 설명한다. 이 도식에서 핵심은 수만 개의 노드가 상태를 완벽히 합의([[212_synchronization_mechanisms|동기화]])해야만 보안과 [[010_decentralization|탈중앙화]]가 달성된다는 점이다. 따라서 [[191_transaction_concept_states|트랜잭션]] 처리 속도를 무리하게 높이려면 노드의 사양(하드웨어) 진입 장벽이 높아져 결국 소수의 노드만 남는 중앙화로 회귀하게 된다. 실무에서는 이러한 한계를 극복하기 위해 퍼블릭 체인(L1) 위에서 연산을 묶어 처리하는 [[042_rollup_l2_solution|롤업]]([[042_rollup_l2_solution|Rollup]]) 등의 레이어 2(Layer 2) 확장성 솔루션을 덧붙이는 아키텍처가 필수적으로 요구된다.

📢 **섹션 요약 비유**: 수만 명의 낯선 사람들이 각자 장부 사본을 들고 일일이 내용을 대조하고 만장일치를 봐야 하므로, 결재 속도는 엄청나게 느리지만 그 누구도 장부를 몰래 조작할 수 없는 세상에서 가장 튼튼한 금고와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

퍼블릭 [[004_blockchain|블록체인]]은 네트워크의 참여를 철저히 통제하는 프라이빗(Private) [[004_blockchain|블록체인]]과 철학과 구조 양면에서 대척점에 서 있다.

| 비교 항목 | 퍼블릭 [[004_blockchain|블록체인]] (Public) | [[020_private_blockchain|프라이빗 블록체인]] (Private) | 기술 및 실무적 판단 포인트 |
|:---|:---|:---|:---|
| **네트워크 접근 권한** | **[[076_permissionless_vs_permissioned_blockchain|무허가형]] ([[076_permissionless_vs_permissioned_blockchain|Permissionless]])** 누구나 자유롭게 | **허가형 (Permissioned)** 신원 [[303_authentication_authorization_patterns|인증]]된 노드만 | 참여의 투명성 및 통제성 |
| **[[001_dikw_pyramid|데이터]] 프라이버시** | 모든 거래 내역 전 세계 투명 공개 | 허가된 기관/채널 내에서만 기밀 유지 | 기업 기밀(B2B) [[001_dikw_pyramid|데이터]] 수용 가능성 |
| **[[282_performance_tactics|성능]] (TPS)** | 낮음 (초당 15 ~ 수십 건 병목) | 높음 (수천 TPS 이상) | 대용량 [[191_transaction_concept_states|트랜잭션]] 실시간 처리 |
| **보상 시스템** | 필수 (코인 채굴, [[024_gas|가스]]비 수수료) | 불필요 (비즈니스적 협약으로 유지) | [[026_token_economy|토큰 이코노미]] 설계 필요성 |
| **[[454_spof|단일 장애점]] ([[454_spof|SPOF]])**| 완전히 제거됨 (절대 안 죽음) | 중앙 [[303_authentication_authorization_patterns|인증]] 기관(Admin) 해킹 시 취약 | 인프라의 [[003_integrity|무결성]] 및 항구성 |

퍼블릭 [[004_blockchain|블록체인]]은 익명 노드 간의 합의를 이끌어내기 위해 엄청난 시간과 자원(합의 오버헤드)을 쏟아붓는다. 이는 비효율적으로 보이지만, 그 대가로 '국경 없는 가치 이전'과 '중앙 검열 회피'라는 전에 없던 혁신 가치를 창출한다. 반면 프라이빗 체인은 이를 포기하고 B2B [[001_dikw_pyramid|데이터]]베이스의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확장에 집중한다.

```text
┌─────────── [블록체인 네트워크 개방성 매트릭스] ───────────┐
│                                                           │
│  [Read 권한 누구나]            [Read 권한 통제]           │
│         ▲                            ▲                    │
│   Public Blockchain           Consortium Blockchain       │
│  (Bitcoin, Ethereum)         (Klaytn 기업노드, R3 Corda)  │
│ ────────┼────────────────────────────┼─────────────────── │
│         │                            │                    │
│   (존재하기 어려움)            Private Blockchain         │
│                              (Hyperledger, CBDC 내부망)   │
│         └────────────────────────────┴                    │
│  [Write 권한 누구나]           [Write 권한 통제 (인가 노드만)]│
└───────────────────────────────────────────────────────────┘
```
이 비교 매트릭스의 핵심은 [[001_dikw_pyramid|데이터]]를 쓰고 읽는 권한을 대중에게 주느냐 특정 집단에게 주느냐에 따라 [[004_blockchain|블록체인]]의 형태가 3단계로 분화된다는 점이다. 퍼블릭 [[004_blockchain|블록체인]]은 좌측 상단에 위치하며, 국가의 통제력이 미치지 않는 독자적 경제 생태계([[033_defi_decentralized_finance|DeFi]])를 구성하는 핵심 엔진이다. 이 공간에서는 코드([[022_smart_contract|Smart Contract]])가 곧 법(Law)으로 작용한다.

📢 **섹션 요약 비유**: 퍼블릭 체인이 누구나 자유롭게 이용하지만 비밀은 없는 투명한 '공용 [[344_bus|버스]]'라면, 프라이빗 체인은 사원증을 찍어야만 탈 수 있고 내부 기밀을 지켜주는 회사 전용 '통근 [[344_bus|버스]]'와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 퍼블릭 [[004_blockchain|블록체인]] 도입을 검토할 때는, 퍼블릭 체인이 만능 [[001_dikw_pyramid|데이터]]베이스가 아니라 극도로 느리고 비싼 '신뢰 증명 기계'임을 정확히 이해하고 아키텍처를 설계해야 한다.

**1. 실무 시나리오 기반 의사결정 플로우**
- **시나리오 A: 전 세계 누구나 접근 가능한 [[010_decentralization|탈중앙화]] 금융([[033_defi_decentralized_finance|DeFi]]) 대출 [[090_service_kubernetes_network_load_balancing|서비스]] 출시**
  - **판단**: [[090_service_kubernetes_network_load_balancing|서비스]]의 핵심 가치가 '은행 없는 투명한 자산 운용'이므로 이더리움 같은 퍼블릭 [[004_blockchain|블록체인]]의 [[022_smart_contract|스마트 컨트랙트]]를 기반으로 구축해야 한다. 단, [[024_gas|가스]]비(수수료) 폭등에 대비하여 로직을 최적화하고 L2 레이어 활용을 병행해야 한다.
- **시나리오 B: A 기업과 B 기업 간의 민감한 영업 비밀([[167_scm_software_configuration_management|SCM]] 물류 [[001_dikw_pyramid|데이터]]) 원장 공유**
  - **판단**: 퍼블릭 [[004_blockchain|블록체인]]을 사용하면 영업 비밀이 전 세계에 평문으로 공개되어 치명적이다. 또한 [[191_transaction_concept_states|트랜잭션]]마다 [[024_gas|가스]]비를 지불해야 하므로 막대한 비용이 든다. 따라서 퍼블릭 체인을 배제하고, 프라이빗(컨소시엄) [[004_blockchain|블록체인]]을 도입해야 한다.

**2. 도입 전 필수 [[435_checklist_based_testing|체크리스트]]**
- [ ] **기술적/비용적**: [[191_transaction_concept_states|트랜잭션]] 1건당 발생하는 [[024_gas|가스]]비([[024_gas|Gas]] Fee)가 비즈니스 모델상 감당 가능한가? (이더리움 메인넷은 복잡한 로직 구동 시 수만 원의 수수료가 들 수 있음)
- [ ] **보안/법률적**: [[022_smart_contract|스마트 컨트랙트]]는 한 번 퍼블릭 체인에 배포되면 수정이 극도로 어렵다. 배포 전 보안 오딧([[363_audit|Audit]]) 및 정형 [[395_verification_process_review|검증]]을 100% 완수했는가? [[001_dikw_pyramid|데이터]] 삭제가 불가능하여 GDPR의 '잊힐 권리'와 충돌하는 부분은 오프체인에 분리 저장했는가?

**3. [[128_water_scrum_fall_anti_pattern|안티패턴]] (치명적 [[352_defect_definition|결함]] 사례)**
- **모든 대용량 [[001_dikw_pyramid|데이터]]를 온체인(On-chain)에 저장**: 이미지, 영상, 대용량 텍스트 로그를 퍼블릭 [[004_blockchain|블록체인]]에 직접 저장(Insert)하도록 앱을 설계하는 경우. 이더리움 등은 1MB 저장에 수억 원의 수수료가 들 수 있다. 퍼블릭 체인은 [[001_dikw_pyramid|데이터]]베이스가 아님을 망각한 최악의 [[128_water_scrum_fall_anti_pattern|안티패턴]]이다.

```text
[퍼블릭 블록체인 데이터 저장 안티패턴 및 권장 아키텍처]

[안티패턴: 파산으로 가는 길]
[사용자 사진 업로드(5MB)] => [Public Blockchain 직접 저장 시도]
                            🚨 가스비 수천만 원 청구 & 네트워크 거부

[권장 아키텍처: 하이브리드 체인 분리]
[사용자 사진 업로드(5MB)] => [IPFS / AWS S3 등 외부 스토리지 저장]
                            ↓ (해시값 SHA-256 추출: 32Bytes)
                      [Public Blockchain] (해시값만 기록하여 무결성만 증명)
```
이 그림은 퍼블릭 [[004_blockchain|블록체인]]의 높은 저장 비용([[024_gas|가스]] 병목)을 회피하기 위한 오프체인(Off-chain) 연동 구조를 보여준다. 이 도식에서 핵심은 무겁고 부피가 큰 '실제 [[001_dikw_pyramid|데이터]]'는 바깥에 두고, 그 [[001_dikw_pyramid|데이터]]가 변조되지 않았음을 증명하는 가벼운 '해시 지문'만을 퍼블릭 체인에 올린다는 점이다. 실무에서는 이처럼 무거운 [[001_dikw_pyramid|데이터]] 저장과 복잡한 연산은 모두 오프체인(L2 또는 클라우드)으로 빼고, 퍼블릭 체인은 오직 최종적인 상태 [[395_verification_process_review|검증]]과 자산 이동의 신뢰 앵커(Trust Anchor) 역할로만 사용해야 시스템 파산을 막을 수 있다.

📢 **섹션 요약 비유**: 세계에서 가장 비싸고 좁은 최고급 금고(퍼블릭 체인) 안에 두꺼운 전화번호부 뭉치(대용량 [[001_dikw_pyramid|데이터]])를 통째로 쑤셔 넣으려는 멍청한 짓 대신, 전화번호부는 일반 책장에 두고 그 요약본 메모 한 장만 금고에 보관하는 지혜가 필요합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

퍼블릭 [[004_blockchain|블록체인]]은 중앙 기구의 승인이나 개입 없이도 글로벌 인터넷 상에서 익명의 개인들이 서로 가치를 주고받으며 신뢰할 수 있게 만든 인류 역사상 최초의 시스템이다.

| 구분 | 중앙화 플랫폼 중심 (Web 2.0) | 퍼블릭 [[004_blockchain|블록체인]] 중심 (Web 3.0) | 기대 [[012_roi_return_on_investment|ROI]] 및 파급 효과 |
|:---|:---|:---|:---|
| **소유권 및 자산** | 플랫폼 기업이 DB를 소유 및 통제 | 사용자가 개인 키로 자산을 직접 통제 | 진정한 디지털 자산 소유권(NFT) 보장 |
| **상호 운용성** | 폐쇄적 [[014_api_posix|API]], 기업 간 연동 어려움 | 오픈 소스 및 공개 원장, 블록 장난감처럼 결합 | 디앱 간 강력한 시너지 (머니 레고) |
| **운영 연속성** | 기업 파산 시 [[090_service_kubernetes_network_load_balancing|서비스]] 및 [[001_dikw_pyramid|데이터]] 증발 | 코드가 영구 존속하며 누구나 실행 가능 | [[454_spof|단일 장애점]] 부재로 영구적인 시스템 |

미래의 퍼블릭 [[004_blockchain|블록체인]]은 고질적인 한계였던 확장성(TPS)을 해결하기 위해 [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]([[095_modular_blockchain_execution_da_consensus|Modular Blockchain]]) 아키텍처로 진화하고 있다. 즉 합의, 실행, [[094_data_availability_da_layer_celestia|데이터 가용성]]([[104_da_as_is_analysis|DA]]) 레이어를 각각 분리하여 처리함으로써 퍼블릭 특유의 막강한 보안성과 [[010_decentralization|탈중앙화]]를 유지한 채 수십만 TPS를 달성하는 Web 3.0 글로벌 인프라 표준으로 우뚝 설 것이다.

📢 **섹션 요약 비유**: 퍼블릭 [[004_blockchain|블록체인]]은 특정 회사가 전원을 끌 수 없는 영원히 살아 숨 쉬는 '전 지구적 글로벌 컴퓨터'이자, 앞으로 모든 디지털 가치가 거래되는 국경 없는 고속도로의 기초 포장 공사입니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[076_permissionless_vs_permissioned_blockchain|무허가형]] ([[076_permissionless_vs_permissioned_blockchain|Permissionless]])** | 네트워크에 노드로 참여하거나 [[191_transaction_concept_states|트랜잭션]]을 전송할 때 관리자의 사전 허가를 받을 필요가 없는 개방성 철학
- **[[011_consensus_algorithm|합의 알고리즘]] (PoW, PoS)** | 익명 노드들로 구성된 퍼블릭 환경에서, 악의적 조작을 막고 장부의 상태를 일치시키기 위한 수학적 합의 규칙
- **[[024_gas|가스]] ([[024_gas|Gas]])** | 무한 루프를 방지하고 스팸 [[191_transaction_concept_states|트랜잭션]] 공격을 막기 위해 퍼블릭 체인에서 연산 및 저장 시 사용자에게 부과하는 네트워크 수수료
- **[[454_spof|단일 장애점]] ([[454_spof|SPOF]])** | 중앙 서버 한 곳이 파괴되면 시스템 전체가 멈추는 취약점 (퍼블릭 체인은 이 SPOF를 100% 제거함)
- **레이어 2 (Layer 2) [[042_rollup_l2_solution|롤업]]** | 퍼블릭 체인(L1)의 느린 속도와 비싼 수수료 문제를 해결하기 위해 거래를 밖에서 묶어 처리한 뒤 결과만 L1에 기록하는 확장성 기술

### 📈 관련 키워드 및 발전 흐름도

```text
[비트코인 (Bitcoin) — PoW 합의, 최초 퍼블릭 블록체인]
    │
    ▼
[이더리움 (Ethereum) — 스마트 컨트랙트·PoS 전환]
    │
    ▼
[Layer 2 (Rollup·Plasma) — 처리량 확장, 수수료 절감]
    │
    ▼
[크로스체인 (Cross-Chain) — 서로 다른 퍼블릭 체인 간 자산 이동]
```
퍼블릭 [[004_blockchain|블록체인]]은 [[076_permissionless_vs_permissioned_blockchain|무허가형]]·[[010_decentralization|탈중앙화]] 원칙 위에서 합의 메커니즘을 PoW에서 PoS로, 확장성을 Layer 2로 진화시켜왔다.

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 퍼블릭 [[004_blockchain|블록체인]]은 동네 사람 누구나 와서 마음대로 글을 쓰고 읽을 수 있는 커다란 투명 마을 게시판이에요.
2. **원리**: 나쁜 사람이 게시판에 거짓말을 쓰려고 하면, 동네 사람들이 다 같이 지켜보고 있다가 "저거 틀렸어!" 하고 막아주는 똑똑한 규칙이 있어요.
3. **효과**: 경찰이나 은행장님이 없어도 우리끼리 스스로 돈이나 중요한 약속을 안전하게 지킬 수 있어서, 전 세계 친구들과 마음 놓고 거래할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 19 / 552

← **이전**: [[018_post_proof_of_space_and_time|18. 공간/시간 증명 (PoST, Proof of Space and Time) - 스토리지 자원 증명 (Chia Network)]]
**다음**: [[020_private_blockchain|20. 프라이빗 블록체인 (Private Blockchain) - 허가된 노드만 참여 (하이퍼레저 패브릭)]] →

---
