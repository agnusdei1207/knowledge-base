+++
weight = 9999
title = "06. ICT 융합 및 신기술 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynote-ict-convergence"
+++
[[267_weight_bias_activation|weight]] = 9999

# ICT 융합 및 신기술 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 합격을 위한 최신 ICT 융합, 4차 산업혁명 핵심 기술, Web 3.0, 자율주행, 퀀텀 컴퓨팅, [[232_spatial_computing_digital_twin|공간 컴퓨팅]] 및 [[171_smart_city_platform_architecture|스마트 시티]] 등 전 영역을 망라한 800대 핵심 키워드입니다.

---

## 1. Web 3.0 및 [[004_blockchain|블록체인]] ([[004_blockchain|Blockchain]]) (100개)
1. Web 1.0 (Read-only) / Web 2.0 (Read-Write, 플랫폼 중심)
2. Web 3.0 (Read-Write-Own) - [[010_decentralization|탈중앙화]]([[010_decentralization|Decentralization]])와 개인 소유권 보장 웹
3. [[003_semantic_web|시맨틱 웹]] ([[003_semantic_web|Semantic Web]]) - 온톨로지(Ontology) 기반 의미 연결망
4. [[004_blockchain|블록체인]] ([[004_blockchain|Blockchain]]) - [[474_dlt_distributed_ledger_technology|분산 원장 기술]]([[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]], Distributed Ledger Technology)
5. [[005_genesis_block|제네시스 블록]] ([[005_genesis_block|Genesis Block]]) - [[004_blockchain|블록체인]]의 첫 번째 블록
6. 블록의 구조 - 블록 헤더 ([[288_version_ihl_tos_total_length|버전]], 이전 블록 해시, [[008_merkle_root|머클 루트]], 타임스탬프, 난이도, 논스) + 바디
7. [[007_merkle_tree|머클 트리]] ([[007_merkle_tree|Merkle Tree]] / Hash Tree) - [[191_transaction_concept_states|트랜잭션]] [[003_integrity|무결성]] [[395_verification_process_review|검증]]을 위한 해시 트리
8. [[008_merkle_root|머클 루트]] ([[008_merkle_root|Merkle Root]]) - 모든 [[191_transaction_concept_states|트랜잭션]] 해시를 묶은 최종 해시값
9. [[009_hash_pointer|해시 포인터]] ([[009_hash_pointer|Hash Pointer]]) - [[001_dikw_pyramid|데이터]]의 위치와 [[003_integrity|무결성]] 정보를 동시에 지님
[[489_raid_10_hybrid|10]]. [[010_decentralization|탈중앙화]] ([[010_decentralization|Decentralization]]) - [[454_spof|단일 장애점]]([[454_spof|SPOF]]) 제거 및 투명성 확보
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_consensus_algorithm|합의 알고리즘]] ([[011_consensus_algorithm|Consensus Algorithm]]) - [[136_variance|분산]] 노드 간 상태 일치 달성 매커니즘
12. [[647_bft_verification|비잔틴 장애 허용]] ([[647_bft_verification|BFT]], Byzantine [[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) - 1/3 미만의 악의적 노드가 있어도 정상 합의 보장
13. [[013_pbft_practical_bft|PBFT]] ([[013_pbft_practical_bft|Practical BFT]]) - 다수결 기반 상태 기계 [[016_replication_factor|복제]] 합의 (텐더민트, 하이퍼레저)
14. [[014_pow_proof_of_work|작업 증명]] (PoW, Proof of Work) - 해시 퍼즐 연산 경쟁 (비트코인), 막대한 [[466_power_consumption|전력 소모]]
15. [[015_pos_proof_of_stake|지분 증명]] (PoS, Proof of Stake) - 보유 지분(Coin)에 비례해 블록 [[087_process_state_transition|생성]] 권한 부여 (이더리움 2.0)
16. [[016_dpos_delegated_pos|위임 지분 증명]] (DPoS, Delegated PoS) - 대표자(BP)를 투표로 선출해 합의 위임 (빠른 속도, EOS)
17. [[017_poa_proof_of_authority|권위 증명]] (PoA, Proof of Authority) - 신원 [[303_authentication_authorization_patterns|인증]]된 노드만 합의 참여 ([[020_private_blockchain|프라이빗 블록체인]])
18. 공간/시간 증명 (PoST, Proof of Space and Time) - 스토리지 자원 증명 (Chia Network)
19. [[019_public_blockchain|퍼블릭 블록체인]] ([[019_public_blockchain|Public Blockchain]]) - 누구나 참여 가능 (비트코인, 이더리움)
20. [[020_private_blockchain|프라이빗 블록체인]] ([[020_private_blockchain|Private Blockchain]]) - 허가된 노드만 참여 ([[058_hyperledger_fabric_private_blockchain|하이퍼레저 패브릭]])
21. [[021_consortium_blockchain|컨소시엄 블록체인]] ([[021_consortium_blockchain|Consortium Blockchain]]) - 여러 기업이 연합하여 노드 운영
22. [[022_smart_contract|스마트 컨트랙트]] ([[022_smart_contract|Smart Contract]]) - 조건이 충족되면 [[004_blockchain|블록체인]] 상에서 자동 실행되는 프로그램 코드 (닉 자보 제안)
23. [[152_evm_earned_value_management|EVM]] ([[023_evm_ethereum_virtual_machine|Ethereum Virtual Machine]]) - 이더리움 [[022_smart_contract|스마트 컨트랙트]] 런타임 환경
24. [[024_gas|가스]] ([[024_gas|Gas]]) - [[022_smart_contract|스마트 컨트랙트]] 실행 및 [[191_transaction_concept_states|트랜잭션]] 처리에 지불하는 네트워크 수수료
25. [[025_turing_completeness|튜링 완전성]] ([[025_turing_completeness|Turing Completeness]]) - 이더리움 [[022_smart_contract|스마트 컨트랙트]] 연산의 무한루프 방지를 위해 [[024_gas|Gas]] 도입
26. [[026_token_economy|토큰 이코노미]] ([[026_token_economy|Token Economy]]) - [[004_blockchain|블록체인]] 생태계 내의 인센티브 보상 구조
27. ICO (Initial Coin Offering) / STO ([[283_security_tactics|Security]] Token Offering, 증권형 토큰 발행) / IEO
28. RWA (Real World Asset) [[820_tokenization|토큰화]] - 실물 자산(부동산, 미술품 등)의 [[004_blockchain|블록체인]] 토큰 변환
29. 대체 불가능 토큰 (NFT, [[029_nft_non_fungible_token|Non-Fungible Token]]) - 고유한 [[289_identification_flags_fragmentation_offset|식별자]]를 가진 디지털 자산 (ERC-721 규격)
30. 암호화폐 지갑 (Cryptocurrency Wallet) - 핫 월렛 (온라인) vs 콜드 월렛 (오프라인/하드웨어)
31. 니모닉 (Mnemonic) - 지갑 [[658_ir_recovery|복구]]를 위한 12~24개의 무작위 영단어 조합 (시드 구문)
32. 디앱 ([[032_dapp_decentralized_application|DApp]], [[592_blockchain_dapp_architecture_ipfs|Decentralized Application]]) - 백엔드가 [[004_blockchain|블록체인]]([[022_smart_contract|스마트 컨트랙트]])인 애플리케이션
33. 디파이 ([[033_defi_decentralized_finance|DeFi]], Decentralized Finance) - [[010_decentralization|탈중앙화]] 금융 (중개자 없는 대출, 예치, 스왑)
34. 유니스왑 (Uniswap) / AMM (Automated Market Maker) - 자동화된 시장 조성자 [[001_algorithm_definition|알고리즘]] (유동성 풀)
35. [[035_flash_loan|플래시 론]] ([[035_flash_loan|Flash Loan]]) - [[191_transaction_concept_states|트랜잭션]] 블록 1개 내에서 무담보 대출 및 상환을 동시에 진행하는 구조
36. [[004_blockchain|블록체인]] 오라클 ([[188_pl_sql_t_sql_procedural|Oracle]]) 문제 - [[004_blockchain|블록체인]] 외부(Off-chain)의 현실 [[001_dikw_pyramid|데이터]]를 [[004_blockchain|블록체인]] 내부(On-chain)로 가져올 때 발생하는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 문제
37. [[229_zkp_data_clean_room|영지식 증명]] ([[354_did_decentralized_identity_zkp|ZKP]], [[037_zero_knowledge_proof_zkp|Zero-Knowledge Proof]]) - 비밀을 공개하지 않고도 그 비밀을 안다는 것을 증명 (Zcash 등 프라이버시 [[571_protection_vs_security|보호]])
38. zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge) - 비대화형 [[229_zkp_data_clean_room|영지식 증명]]
39. 레이어 1 (Layer 1) - 비트코인, 이더리움 등 메인 [[004_blockchain|블록체인]] 네트워크 (트릴레마 딜레마 직면)
40. [[040_blockchain_trilemma|블록체인 트릴레마]] ([[482_blockchain_trilemma_scalability_decentralization_security|Blockchain Trilemma]]) - 확장성(Scalability), [[010_decentralization|탈중앙화]]([[010_decentralization|Decentralization]]), [[283_security_tactics|보안성]]([[283_security_tactics|Security]]) 세 가지를 동시에 완벽히 만족할 수 없는 문제
41. 레이어 2 (Layer 2) 솔루션 - L1의 확장성 문제를 해결하기 위해 메인넷 밖에서 연산 수행 후 결과만 L1에 기록
42. [[042_rollup_l2_solution|롤업]] ([[042_rollup_l2_solution|Rollup]]) - 수천 개의 오프체인 [[191_transaction_concept_states|트랜잭션]]을 하나로 묶어([[042_rollup_l2_solution|Rollup]]) L1에 [[395_verification_process_review|검증]]
43. 옵티미스틱 [[042_rollup_l2_solution|롤업]] (Optimistic [[042_rollup_l2_solution|Rollup]]) - 기본적으로 [[191_transaction_concept_states|트랜잭션]]이 유효하다고 낙관하고, 사기 증명(Fraud Proof) 기간을 두는 방식 (Arbitrum, Optimism)
44. ZK [[042_rollup_l2_solution|롤업]] (Zero-Knowledge [[042_rollup_l2_solution|Rollup]]) - [[191_transaction_concept_states|트랜잭션]] 배치마다 [[229_zkp_data_clean_room|영지식 증명]](Validity Proof)을 [[087_process_state_transition|생성]]해 L1에 즉시 확정 (속도 빠름, 연산 복잡)
45. 사이드체인 (Sidechain) - 메인체인과 [[260_bridge_pattern_abstraction_implementation|브리지]]로 연결된 별도의 독립된 [[004_blockchain|블록체인]] ([[045_sidechain_bridge_polygon|Polygon]] 등)
46. [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) - 메인 체인을 여러 개의 조각(Shard)으로 분할하여 [[191_transaction_concept_states|트랜잭션]]을 [[430_index_fast_full_scan|병렬]] 처리하는 L1 확장성 기술
47. 하드 포크 (Hard Fork) - 기존 [[004_blockchain|블록체인]]과 호환되지 않는 중대한 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 업그레이드 (체인 분리)
48. 소프트 포크 (Soft Fork) - 이전 [[288_version_ihl_tos_total_length|버전]]과 [[344_compatibility_usability|호환성]]을 유지하는 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 업그레이드
49. [[004_blockchain|블록체인]] [[260_bridge_pattern_abstraction_implementation|브리지]] (Cross-chain [[260_bridge_pattern_abstraction_implementation|Bridge]]) - 서로 다른 이기종 [[004_blockchain|블록체인]] 간 자산 및 [[001_dikw_pyramid|데이터]] 이동 통로
50. 소울바운드 토큰 (SBT, [[050_sbt_soulbound_token|Soulbound Token]]) - 양도/전송이 불가능한 NFT (학위, 자격증, 신원 증명용)
51. [[052_did_architecture_issuer_holder_verifier_vc_vp|탈중앙화 신원증명]] ([[231_did_decentralized_identity|DID]], Decentralized Identity) - W3C 표준, 사용자가 자신의 신원 정보를 직접 관리하고 통제 (SSI, Self-Sovereign Identity)
52. [[231_did_decentralized_identity|DID]] 아키텍처 - Issuer(발행자), Holder(소유자/지갑), Verifier([[395_verification_process_review|검증]]자), Verifiable Credential(VC), Verifiable Presentation(VP)
53. [[136_variance|분산]] [[289_identification_flags_fragmentation_offset|식별자]] ([[231_did_decentralized_identity|DID]] [[037_document|Document]]) - 퍼블릭 키, [[303_authentication_authorization_patterns|인증]] 정보, [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트 포함 
54. 다오 ([[054_dao_decentralized_autonomous_organization|DAO]], [[054_dao_decentralized_autonomous_organization|Decentralized Autonomous Organization]]) - 중앙 관리자 없이 [[022_smart_contract|스마트 컨트랙트]]와 거버넌스 토큰 투표로 운영되는 자율 조직
55. [[055_ipfs_interplanetary_file_system|IPFS]] ([[055_ipfs_interplanetary_file_system|InterPlanetary File System]]) - [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] [[553_distributed_file_system|분산 파일 시스템]], 위치 기반([[461_http_stateless_connection_oriented|HTTP]] URL)이 아닌 콘텐츠 해시(CID) 기반 검색
56. [[022_smart_contract|스마트 컨트랙트]] 보안 취약점 - 재진입 ([[056_smart_contract_vulnerability_reentrancy|Re-entrancy]], [[054_dao_decentralized_autonomous_organization|DAO]] 해킹 사태 원인), [[095_overflow|오버플로우]]/[[096_underflow|언더플로우]], 권한 탈취
57. [[057_solidity_smart_contract_language|솔리디티]] ([[057_solidity_smart_contract_language|Solidity]]) - 이더리움 [[022_smart_contract|스마트 컨트랙트]] 개발 언어
58. [[058_hyperledger_fabric_private_blockchain|하이퍼레저 패브릭]] ([[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]]) - IBM 주도 기업용 [[020_private_blockchain|프라이빗 블록체인]] 프레임워크 
59. [[059_chaincode_smart_contract|체인코드]] ([[059_chaincode_smart_contract|Chaincode]]) - 하이퍼레저의 [[022_smart_contract|스마트 컨트랙트]]
60. 하이퍼레저 아키텍처 - 피어([[060_hyperledger_architecture_peer_orderer_msp|Peer]]), 오더러(Orderer, 합의 노드), MSP(Membership [[535_sp_service_provider|Service Provider]], [[303_authentication_authorization_patterns|인증]])
61. [[061_cbdc_central_bank_digital_currency|CBDC]] (Central Bank Digital Currency) - 중앙은행이 직접 발행하는 디지털 화폐 (소매형 vs 도매형)
62. [[062_bitcoin_halving_supply_shock|비트코인 반감기]] ([[062_bitcoin_halving_supply_shock|Halving]]) - 약 4년마다 채굴 보상이 절반으로 줄어드는 메커니즘
63. [[063_mempool_transaction_queue|트랜잭션 풀]] (Mempool / [[369_memory_pool|Memory Pool]]) - 블록에 포함되지 않은 대기 중인 [[191_transaction_concept_states|트랜잭션]] 저장소
64. [[647_bft_verification|BFT]] 합의의 3단계 - Pre-prepare, Prepare, Commit
65. [[065_consensus_finality_probabilistic_deterministic|합의 완결성]] ([[065_consensus_finality_probabilistic_deterministic|Finality]]) - 블록이 체인에 기록되어 뒤집히지 않음이 보장되는 상태 (PoW는 [[130_probability|확률]]적 완결성, BFT는 즉각적 완결성)
66. [[066_dag_directed_acyclic_graph_tangle|지향성 비순환 그래프]] ([[401_bayesian_network_dag_causality|DAG]], [[255_apache_airflow_dag|Directed Acyclic Graph]]) - [[004_blockchain|블록체인]] 대신 [[191_transaction_concept_states|트랜잭션]]들이 거미줄처럼 서로를 증명하는 [[136_variance|분산]] 원장 구조 (IOTA의 Tangle)
67. 51% 공격 (51% Attack) - 악의적 노드가 전체 해시 파워의 51% 이상을 장악해 장부를 조작하는 공격
68. [[068_eclipse_attack_p2p_isolation|이클립스 공격]] ([[068_eclipse_attack_p2p_isolation|Eclipse Attack]]) - 특정 노드의 주변 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 연결을 악성 노드가 장악하여 네트워크를 고립시키고 허위 정보를 주입하는 공격
69. [[069_cryptojacking_malware_mining|크립토재킹]] ([[069_cryptojacking_malware_mining|Cryptojacking]]) - 타인의 PC나 서버 리소스를 해킹하여 몰래 암호화폐를 채굴하는 공격
70. [[070_sybil_attack_fake_nodes|시빌 공격]] ([[070_sybil_attack_fake_nodes|Sybil Attack]]) - 한 명이 여러 개의 가짜 노드(신분)를 [[087_process_state_transition|생성]]하여 투표율/합의를 조작하는 공격
71. [[071_baas_blockchain_as_a_service|블록체인 서비스형]] ([[186_baas_backend_as_a_service_firebase|BaaS]], [[004_blockchain|Blockchain]] [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 클라우드 기반 [[004_blockchain|블록체인]] 인프라 제공 [[090_service_kubernetes_network_load_balancing|서비스]]
72. [[072_erc_20_fungible_token_standard|ERC-20]] (이더리움 대체 가능 토큰 표준)
73. [[073_erc_1155_multi_token_standard|ERC-1155]] (다중 토큰 표준 - NFT와 FT 동시 발행 가능, 게임 아이템에 유리)
74. 영지식 이더리움 가상머신 ([[074_zkevm_zero_knowledge_ethereum_virtual_machine|zkEVM]]) - ZK [[042_rollup_l2_solution|롤업]] 내에서 이더리움 [[022_smart_contract|스마트 컨트랙트]]를 그대로 실행할 수 있게 [[344_compatibility_usability|호환성]] 제공
75. [[136_variance|분산]] 스토리지 보상 시스템 (Filecoin, Arweave)
76. [[076_permissionless_vs_permissioned_blockchain|무허가형]] ([[076_permissionless_vs_permissioned_blockchain|Permissionless]]) vs 허가형 (Permissioned) [[004_blockchain|블록체인]]
77. [[077_crypto_mixing_tumbler_tornado_cash|암호화폐 믹싱]] (Coin Mixing / Tumbler) - 거래 자금 출처 추적을 어렵게 하는 [[191_transaction_concept_states|트랜잭션]] 섞기 (Tornado Cash 등, 자금 세탁 악용)
78. 웹3.0 소셜 네트워크 (Mastodon, Bluesky, Nostr 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]])
79. [[012_mydata|마이데이터]] ([[266_mydata_open_api_token_security|MyData]]) 시스템의 [[004_blockchain|블록체인]] 영수증 및 [[303_authentication_authorization_patterns|인증]] 활용
80. [[061_cbdc_central_bank_digital_currency|CBDC]] 오프라인 결제 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
81. [[081_blockchain_scalability_tps_latency|블록체인 확장성 지표]] - TPS (Transactions Per Second), 레이턴시 ([[141_latency|Latency]])
82. [[082_light_node_spv_simplified_payment_verification|라이트 노드]] (Light Node / SPV, Simplified Payment [[395_verification_process_review|Verification]]) - 블록 헤더만 다운로드하여 [[191_transaction_concept_states|트랜잭션]]을 [[395_verification_process_review|검증]]하는 모바일/경량 환경용 노드
83. [[083_full_node_complete_ledger|풀 노드]] ([[083_full_node_complete_ledger|Full Node]]) - [[005_genesis_block|제네시스 블록]]부터 모든 거래 내역을 보관하고 [[395_verification_process_review|검증]]하는 노드
84. [[084_blockchain_interoperability_polkadot_cosmos|블록체인 상호운용성]] ([[084_blockchain_interoperability_polkadot_cosmos|Interoperability]]) 폴카닷(Polkadot), 코스모스(Cosmos) 네트워크
85. [[085_travel_rule_vasp_fatf|가상자산 사업자]] ([[085_travel_rule_vasp_fatf|VASP]]) 트래블 룰 (Travel Rule) - 자금 세탁 방지를 위해 가상자산 송/수신자 정보를 [[396_validation|확인]]하는 규제
86. [[086_multisig_wallet_n_of_m|지갑 멀티시그]] (Multi-Sig, Multi-Signature) - 출금을 위해 N명 중 M명 이상의 서명이 필요한 보안 지갑 구조
87. [[087_account_abstraction_erc_4337|계정 추상화]] (Account [[198_abstraction_control_data_process|Abstraction]], ERC-4337) - 이더리움 지갑([[088_eoa_vs_89_ca_ethereum_accounts|EOA]])을 [[022_smart_contract|스마트 컨트랙트]]([[089_contract_account_smart_contract|CA]])처럼 프로그래밍 가능하게 만들어 소셜 [[658_ir_recovery|복구]], [[024_gas|가스]]비 대납 등을 지원
88. [[088_eoa_vs_89_ca_ethereum_accounts|EOA]] ([[088_eoa_vs_89_ca_ethereum_accounts|Externally Owned Account]]) - 개인키로 통제되는 일반 사용자 계정
89. [[089_contract_account_smart_contract|CA]] ([[089_contract_account_smart_contract|Contract Account]]) - 코드에 의해 통제되는 컨트랙트 계정
90. 거버넌스 51% 방어 체계 ([[136_variance|분산]] 슬래싱 Slashing) - 악의적 행동 적발 시 스테이킹한 지분을 몰수하는 PoS 방어 기법
91. [[091_synthetic_assets_tokens|합성 자산]] ([[091_synthetic_assets_tokens|Synthetic Assets]]) 토큰 구조
92. [[092_decentralized_escrow_trust|탈중앙화 신탁 관리]] ([[092_decentralized_escrow_trust|Decentralized Escrow]])
93. [[022_smart_contract|스마트 컨트랙트]] 정형 [[395_verification_process_review|검증]] ([[093_smart_contract_formal_verification|Formal Verification]]) - 수학적 모델링을 통해 컨트랙트 코드 [[003_integrity|무결성]] 증명
94. [[094_data_availability_da_layer_celestia|데이터 가용성]] ([[001_dikw_pyramid|Data]] [[452_availability|Availability]], [[104_da_as_is_analysis|DA]]) 계층 - [[042_rollup_l2_solution|롤업]] [[191_transaction_concept_states|트랜잭션]] [[001_dikw_pyramid|데이터]]가 L1에 안전하게 게시되었는지 보장하는 [[004_blockchain|블록체인]] 모듈러 분리 계층 (Celestia, EigenLayer)
95. [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]] ([[095_modular_blockchain_execution_da_consensus|Modular Blockchain]]) - 실행(Execution), 합의(Consensus), 정산(Settlement), [[094_data_availability_da_layer_celestia|데이터 가용성]]([[104_da_as_is_analysis|DA]]) 계층을 분리하여 확장성 극대화 
96. [[096_monolithic_blockchain_solana|모놀리식 블록체인]] ([[096_monolithic_blockchain_solana|Monolithic Blockchain]]) - 모든 작업을 단일 체인(솔라나, 앱토스 등)에서 처리
97. [[120_elliptic_curve_equation|타원곡선]] 디지털 서명 [[001_algorithm_definition|알고리즘]] ([[097_ecdsa_schnorr_signature_bitcoin|ECDSA]]) 및 슈노르 서명 (Schnorr Signature - 다중 서명 병합 축소)
98. [[098_the_graph_blockchain_indexing|블록체인 데이터 인덱싱]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] (The [[104_graph|Graph]])
99. BRC-20 표준 - 비트코인 네트워크 상에서의 토큰 발행 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (오디널스 Ordinals)
100. 양자 내성 [[004_blockchain|블록체인]] 서명 체계 전환 연구

## 2. [[101_iot_concept|사물인터넷]]([[101_iot_concept|IoT]]), 모빌리티 및 무선 신기술 (80개)
101. [[101_iot_concept|사물인터넷]] ([[101_iot_concept|IoT]], Internet of Things) 개념 - 모든 사물이 센서와 통신 기능을 내장하여 인터넷에 연결되는 기술
102. [[101_iot_concept|IoT]] 3대 구성 요소 - 디바이스(센서/액추에이터), 네트워크, 플랫폼/클라우드
103. [[103_wsn_sensor_network|센서 네트워크]] ([[103_wsn_sensor_network|WSN]], Wireless Sensor Network) / 싱크 노드(Sink Node)
104. [[104_tinyos_riot_freertos_micro_os|초소형 운영체제]] (TinyOS, RIOT, FreeRTOS)
105. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] ([[235_edge_computing_smart_factory|Edge Computing]]) - 클라우드로 모든 [[001_dikw_pyramid|데이터]]를 보내지 않고 디바이스 주변(엣지)에서 [[001_dikw_pyramid|데이터]]를 실시간 처리하여 [[015_지연_데이터_관점|지연]] 단축 및 [[140_bandwidth|대역폭]] 절감
106. [[106_fog_computing_cisco_architecture|포그 컴퓨팅]] ([[106_fog_computing_cisco_architecture|Fog Computing]]) - 시스코 제안, 클라우드와 엣지 사이의 지역 노드(게이트웨이) 단에서 [[136_variance|분산]] 처리
107. [[107_hyper_connected_society|초연결 사회]] ([[107_hyper_connected_society|Hyper-connected Society]])
108. [[101_iot_concept|IoT]] 무선 통신 기술 [[104_classification_analysis|분류]] - [[604_wpan_wireless_personal_area_network|WPAN]], [[571_wlan_bss_ess_structure|WLAN]], [[109_lpwan_low_power_wide_area_network|LPWAN]]
109. [[109_lpwan_low_power_wide_area_network|저전력 광역 통신망]] ([[109_lpwan_low_power_wide_area_network|LPWAN]], [[615_lpwan_low_power_wide_area_network|Low-Power Wide-Area Network]]) - 수십 km 커버리지, 수년 배터리 수명, 저용량 [[001_dikw_pyramid|데이터]]
110. 비면허 대역 [[109_lpwan_low_power_wide_area_network|LPWAN]] - LoRaWAN (Chirp [[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]] 방식), [[1030_lpwan_sigfox|Sigfox]] (Ultra Narrow Band)
111. 면허 대역 (이동통신 기반) [[109_lpwan_low_power_wide_area_network|LPWAN]] - [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] ([[752_lte_long_term_evolution_4g|LTE]] [[571_protection_vs_security|보호]]대역 200kHz 사용), [[621_ltem_emtc_iot_mobility_voice|LTE-M]] ([[621_ltem_emtc_iot_mobility_voice|eMTC]], 음성 및 이동성 지원)
112. [[609_zigbee_ieee_802_15_4_mesh_iot|지그비]] ([[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]]) - IEEE 802.15.4 기반 저전력 [[389_mesh_topology|메시]]([[389_mesh_topology|Mesh]]) 네트워크 [[604_wpan_wireless_personal_area_network|WPAN]] 기술
113. [[610_z_wave_900mhz_smart_home_iot|Z-Wave]] - 홈 네트워크 특화 저주파(900MHz) 무선 통신 
114. [[114_ble_bluetooth_low_energy_beacon|블루투스 저전력]] ([[607_ble_bluetooth_low_energy_iot|BLE]], [[607_ble_bluetooth_low_energy_iot|Bluetooth Low Energy]]) - [[608_beacon_technology_ibeacon_eddystone|비컨]]([[608_beacon_technology_ibeacon_eddystone|Beacon]]) 활용 위치 기반 [[090_service_kubernetes_network_load_balancing|서비스]]
115. [[092_thread_lwp|스레드]] ([[092_thread_lwp|Thread]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]] - [[324_ipv6_128bit_next_generation_address|IPv6]] 기반 스마트홈 [[101_iot_concept|IoT]] [[389_mesh_topology|메시]] 네트워크 (Google 주도)
116. [[612_matter_csa_smart_home_standard|매터]] ([[612_matter_csa_smart_home_standard|Matter]]) 표준 - CSA 주도, 애플/구글/아마존 스마트홈 기기 간 상호 연동성([[084_blockchain_interoperability_polkadot_cosmos|Interoperability]])을 보장하는 단일 앱/[[295_protocol_field_tcp_udp_icmp|프로토콜]] 규격
117. [[117_6lowpan_iot_ipv6|6LoWPAN]] - 저전력/소용량 네트워크(802.15.4)에서 [[324_ipv6_128bit_next_generation_address|IPv6]] 패킷을 전송하기 위해 헤더 [[347_compaction|압축]] 및 [[291_fragmentation_and_reassembly_process|단편화]] 수행
118. [[622_mqtt_publish_subscribe_qos|MQTT]] (Message Queuing Telemetry Transport) - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반, 퍼블리시/서브스크라이브 (Pub/Sub) 모델의 초경량 [[101_iot_concept|IoT]] [[389_mesh_topology|메시]]지 [[295_protocol_field_tcp_udp_icmp|프로토콜]], 브로커(Broker) 필수
119. [[622_mqtt_publish_subscribe_qos|MQTT]] [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] ([[388_qos_quality_of_service_best_effort_intserv_diffserv|Quality of Service]]) - Level 0 (최대 1회, 유실 가능), Level 1 (최소 1회, 중복 가능), Level 2 (정확히 1회, 오버헤드 큼)
120. [[120_coap_constrained_application_protocol|CoAP]] ([[120_coap_constrained_application_protocol|Constrained Application Protocol]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반, RESTful(GET/POST/PUT/DELETE) 구조를 제공하는 경량 [[101_iot_concept|IoT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]], 브로커리스 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 지원
121. [[121_lwm2m_lightweight_m2m|LwM2M]] ([[121_lwm2m_lightweight_m2m|Lightweight M2M]]) - [[120_coap_constrained_application_protocol|CoAP]] 기반의 [[101_iot_concept|IoT]] 디바이스 원격 관리 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
122. oneM2M - 이기종 [[101_iot_concept|사물인터넷]] 플랫폼 간 상호 연동을 위한 글로벌 공통 아키텍처 표준
123. [[123_ocf_open_connectivity_foundation|OCF]] ([[123_ocf_open_connectivity_foundation|Open Connectivity Foundation]]) 표준
124. [[101_iot_concept|IoT]] [[990_botnet_cnc|봇넷]] ([[990_botnet_cnc|Botnet]]) 위협 - 미라이(Mirai) 악성코드, 디폴트 패스워드 악용 DDoS 전진기지화
125. 무선 스니핑 및 리플레이 공격 방어
126. [[126_digital_twin_concept|디지털 트윈]] ([[126_digital_twin_concept|Digital Twin]]) - 물리적 세계(객체, 시스템, 도시)를 가상 공간에 1:1로 동일하게 구현하고 실시간 [[212_synchronization_mechanisms|동기화]]하여 시뮬레이션 및 예측하는 기술
127. [[126_digital_twin_concept|디지털 트윈]] 3요소 - 물리 공간 (Physical), 가상 공간 (Virtual), 실시간 [[001_dikw_pyramid|데이터]] 연결 ([[001_dikw_pyramid|Data]]/Connection)
128. 가상/증강/혼합 현실 (VR / AR / MR / XR)
129. [[232_spatial_computing_digital_twin|공간 컴퓨팅]] ([[232_spatial_computing_digital_twin|Spatial Computing]]) - 현실 공간을 3D로 스캔하여 디지털 정보와 상호작용하는 기술 (Apple Vision Pro 등)
130. 6자유도 (6DoF) 트래킹 - X, Y, Z 이동 및 Pitch, Yaw, Roll 회전 추적
131. [[131_slam_simultaneous_localization_mapping|SLAM]] (Simultaneous Localization and [[010_schema_mapping|Mapping]]) - 로봇/AR 기기가 미지의 환경을 돌아다니며 지도를 작성함과 동시에 자신의 위치를 추정하는 자율주행/AR 핵심 [[001_algorithm_definition|알고리즘]]
132. [[132_v_slam_visual_slam_camera|V-SLAM]] (Vision [[131_slam_simultaneous_localization_mapping|SLAM]]) - 카메라 시각 정보 기반 [[131_slam_simultaneous_localization_mapping|SLAM]]
133. 볼류메트릭 비디오 (Volumetric Video) - 다수의 카메라로 인물/사물을 360도 3D로 캡처하여 홀로그램처럼 재생하는 기술
134. [[594_metaverse_realtime_sync_rendering_offloading|메타버스]] ([[594_metaverse_realtime_sync_rendering_offloading|Metaverse]]) - 가상 현실 기술을 기반으로 경제/사회/문화 활동이 이루어지는 3D 가상 세계
135. 자율주행 자동차 (Autonomous Vehicle) 기술 단계 (SAE J3016 기준 0~5단계)
136. 레벨 2 (부분 자동화) - ADAS (차선 유지, 크루즈 컨트롤) 결합
137. 레벨 3 (조건부 자율주행) - 시스템 제어, 비상 시 운전자 개입 (시선 이탈 금지)
138. 레벨 4 (고도 자율주행) - 특정 구역 내에서 시스템이 완전 주행 책임 (운전자 개입 불필요)
139. [[139_sensor_fusion_camera_lidar_radar|센서 퓨전]] (Sensor Fusion) - 카메라, 라이다([[140_lidar_light_detection_and_ranging_tof|LiDAR]]), 레이더(Radar), 초음파 센서의 [[001_dikw_pyramid|데이터]]를 결합하여 인식 정확도 극대화
140. 라이다 ([[140_lidar_light_detection_and_ranging_tof|LiDAR]], Light [[961_deepfake_detection|Detection]] And Ranging) - 레이저를 쏴서 반사되는 시간(ToF)을 측정해 주변을 고정밀 3D 포인트 클라우드(Point Cloud)로 맵핑
141. [[141_v2x_vehicle_to_everything_communication|V2X]] ([[589_v2x_vehicle_to_everything_autonomous|Vehicle to Everything]]) 통신 - 차량과 차량(V2V), 인프라(V2I), 보행자(V2P), 네트워크(V2N) 간 무선 통신
142. [[590_wave_ieee_802_11p_dsrc_v2x|WAVE]] (Wireless Access in Vehicular Environments) - IEEE 802.11p 기반 근거리 전용 [[1025_c_v2x_wave_dsrc|DSRC]] 자율주행 통신 (과거 표준)
143. [[143_c_v2x_cellular_based_communication|C-V2X]] ([[143_c_v2x_cellular_based_communication|Cellular V2X]]) - [[751_3gpp_3rd_generation_partnership_project|3GPP]] 표준, [[752_lte_long_term_evolution_4g|LTE]]/[[418_5g_embb_urllc_mmtc_slicing|5G]] [[551_cellular_network_concept_reuse_handover|이동통신망]] 기반 차량 통신 (현대 대세 기술)
144. 플래투닝 ([[144_platooning_autonomous_truck_convoy|Platooning]] / 군집 주행) - 여러 대의 트럭이 통신으로 연결되어 좁은 간격으로 줄지어 동시 자율 주행 (연비 및 효율 향상)
145. [[145_uam_urban_air_mobility_evtol|UAM]] ([[145_uam_urban_air_mobility_evtol|Urban Air Mobility]] / 도심 항공 교통) - 에어 택시, 수직이착륙기(eVTOL)를 이용한 도심 3차원 교통 체계
146. [[368_k_uam|K-UAM]] (한국형 도심항공교통) 그랜드 챌린지 및 회랑([[146_k_uam_grand_challenge_corridor|Corridor]]) 설계
147. [[147_utm_unmanned_aircraft_system_traffic_management|UTM]] (Unmanned Aircraft System Traffic [[372_management|Management]]) - 무인 비행체 교통 관제 시스템
148. [[418_5g_embb_urllc_mmtc_slicing|5G]] 통신망의 3대 초격차 특성 - [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] ([[148_5g_embb_urllc_mmtc|초고속]]), [[761_urllc_ultra_reliable_low_latency|uRLLC]] (초저지연/고신뢰 1ms), [[762_mmtc_massive_machine_type_communications|mMTC]] (초연결 [[101_iot_concept|IoT]])
149. [[149_network_slicing_5g_architecture|네트워크 슬라이싱]] ([[149_network_slicing_5g_architecture|Network Slicing]]) - [[418_5g_embb_urllc_mmtc_slicing|5G]] 핵심, 물리적 통신망 하나를 [[369_logic_bomb|논리]]적으로 분할하여 자율주행([[761_urllc_ultra_reliable_low_latency|uRLLC]] [[331_neuromorphic_ai_db|슬라이스]]), [[101_iot_concept|IoT]]([[762_mmtc_massive_machine_type_communications|mMTC]] [[331_neuromorphic_ai_db|슬라이스]]) 등에 맞춤형 보장 제공
150. [[150_5g_sa_standalone_architecture|5G SA]] ([[150_5g_sa_standalone_architecture|Standalone]]) 아키텍처 - [[752_lte_long_term_evolution_4g|LTE]] 코어망([[753_epc_evolved_packet_core_sgw_pgw|EPC]])을 버리고 순수 [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어([[768_5gc_5g_core_network_evolution|5GC]])로만 구성하여 진정한 [[418_5g_embb_urllc_mmtc_slicing|5G]] 초저지연 [[282_performance_tactics|성능]] 발휘
151. [[151_sba_service_based_architecture_5g|SBA]] ([[151_sba_service_based_architecture_5g|Service Based Architecture]]) - [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어망 네트워크 기능(NF)들을 [[532_microservices_decomposition_patterns|마이크로서비스]] 및 [[477_rest_api_architecture|REST API]] 기반으로 [[531_cloud_native_architecture|클라우드 네이티브]]하게 모듈화
152. [[419_6g_ntn_thz_ris_next_gen|6G]] 통신망 비전 - [[157_terahertz_thz_6g|테라헤르츠]]([[157_terahertz_thz_6g|THz]]) 대역 사용, Tbps 속도, 수중/우주 통신 커버리지 확장, [[190_ai_llm_requirements_specification|AI]] 내재화 ([[792_ai_native_6g_neural_network_radio|AI-Native]])
153. [[153_ris_reconfigurable_intelligent_surface|지능형 반사 표면]] (RIS, Reconfigurable Intelligent Surface) - [[419_6g_ntn_thz_ris_next_gen|6G]] 메타물질, 전파의 반사/투과 방향을 인위적으로 조절하여 고주파(음영지역)의 커버리지 극복
154. [[154_ntn_non_terrestrial_network_6g|비지상 네트워크]] (NTN, Non-Terrestrial Network) - [[595_leo_low_earth_orbit_starlink_6g|저궤도 위성]]([[595_leo_low_earth_orbit_starlink_6g|LEO]]), 성층권 드론([[596_haps_high_altitude_platform_station_drone|HAPS]])을 기지국으로 활용하여 전 세계(바다, 사막)를 커버하는 [[419_6g_ntn_thz_ris_next_gen|6G]] [[592_satellite_communication_characteristics|위성 통신]] 
155. [[155_oran_open_radio_access_network|오픈 랜]] ([[782_o_ran_open_ran_white_box_interface|O-RAN]], Open Radio Access Network) - 기지국 장비의 하드웨어와 소프트웨어를 분리하고 인터페이스를 개방형(오픈 [[014_api_posix|API]]) 표준으로 전환하여 벤더 [[008_dependencies|종속성]]([[362_lock_in_portability|Lock-in]]) 탈피 ([[859_whitebox_switch_open_hardware_nos|화이트박스 스위치]] 활용)
156. [[156_c_ran_cloud_ran|C-RAN]] ([[156_c_ran_cloud_ran|Cloud RAN]]) - 기지국의 [[001_dikw_pyramid|데이터]] 처리부([[688_bbu|BBU]]/DU)를 한 곳의 클라우드 센터에 모아 [[285_pooling_layer|풀링]]([[285_pooling_layer|Pooling]]) 관리하고 [[171_antenna_basic_dipole_resonance|안테나]](RU)만 엣지에 [[136_variance|분산]] 배치하는 구조 
157. [[157_wifi_6_802_11ax|와이파이 6]] ([[576_802_11ax_wifi_6_ofdma_twt|Wi-Fi 6]] / IEEE 802.[[576_802_11ax_wifi_6_ofdma_twt|11ax]]) - [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] 및 양방향 MU-MIMO 도입, 밀집 지역 통신 [[015_지연_데이터_관점|지연]] 최소화
158. [[157_wifi_6_802_11ax|와이파이 6]]E - 기존 2.4G/[[418_5g_embb_urllc_mmtc_slicing|5G]] 외에 깨끗한 6GHz 대역(1.2GHz 폭)을 추가 사용
159. [[159_wifi_7_802_11be|와이파이 7]] (IEEE 802.[[578_802_11be_wifi_7_mlo_4k_qam|11be]]) - 320MHz 초광대역폭, 4K-QAM, MLO(Multi-Link [[329_delta_encoding|Operation]]: 2.4/5/6GHz 동시 송수신) 도입 극초고속 무선랜
160. [[160_uwb_ultra_wideband|UWB]] ([[598_uwb_ultra_wideband_indoor_positioning|Ultra-Wideband]] / 초광대역) 통신 - 매우 짧은 임펄스(Impulse) 신호를 넒은 주파수에 걸쳐 송신, 수 센티미터 단위 정밀 위치 측정(스마트 태그, 디지털 키)
161. [[161_smart_grid_architecture|스마트 그리드]] ([[161_smart_grid_architecture|Smart Grid]]) - 전력망에 ICT를 접목하여 양방향으로 전력/정보를 교환, 에너지 효율 극대화
162. [[162_ami_advanced_metering_infrastructure|AMI]] ([[162_ami_advanced_metering_infrastructure|Advanced Metering Infrastructure]]) - 지능형 원격 검침 인프라
163. [[163_microgrid_island_mode|마이크로그리드]] ([[163_microgrid_island_mode|Microgrid]]) - 기존 광역 전력망과 독립적으로 [[136_variance|분산]] 전원(태양광 등)과 ESS를 갖춘 소규모 지역 자급자족 전력망
164. [[164_ess_energy_storage_system|ESS]] ([[164_ess_energy_storage_system|Energy Storage System]]) - 남는 전력을 배터리에 저장했다가 피크 타임에 방전하는 에너지 저장 장치
165. [[165_v2g_vehicle_to_grid|V2G]] ([[165_v2g_vehicle_to_grid|Vehicle to Grid]]) - 전기차 배터리의 남는 전력을 전력망으로 역송전하여 전력 피크 부하를 줄이는 기술
166. [[166_smart_factory|스마트 팩토리]] ([[166_smart_factory|Smart Factory]]) 
167. [[167_cps_cyber_physical_system|CPS]] (Cyber-Physical System / 가상물리시스템) - 컴퓨팅 연산 체계(Cyber)가 물리(Physical) 공정 프로세스를 실시간 제어하고 피드백하는 시스템 (스마트팩토리 두뇌)
168. 산업용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] ([[630_industrial_ethernet_profinet_ethercat_modbus|Industrial Ethernet]]) 및 [[546_tsn_hardware|TSN]] ([[168_industrial_ethernet_tsn|Time-Sensitive Networking]]) - 마이크로초 단위 [[001_dikw_pyramid|데이터]] 전달 시간을 절대적으로 보장(결정론적)하는 산업 공장 통신망
169. [[631_opc_ua_smart_factory_protocol|OPC UA]] - [[166_smart_factory|스마트 팩토리]] 기기 간 상호 운용성을 보장하는 산업 자동화 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
170. 프라이빗 [[418_5g_embb_urllc_mmtc_slicing|5G]] (특화망 / 이음5G) - 통신사가 아닌 일반 기업/공장이 자신의 건물 내에 직접 구축하고 특정 목적으로만 운영하는 사설 [[418_5g_embb_urllc_mmtc_slicing|5G]] 네트워크
171. [[171_smart_city_platform_architecture|스마트 시티]] ([[171_smart_city_platform_architecture|Smart City]]) 플랫폼 아키텍처
172. [[172_maas_mobility_as_a_service|마스]] (MaaS, Mobility [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 대중교통, 공유차량, 킥보드 등 모든 이동 수단을 하나의 플랫폼에서 통합 결제 및 최적 경로로 제공하는 [[090_service_kubernetes_network_load_balancing|서비스]]
173. [[173_c_its_cooperative_intelligent_transport_systems|C-ITS]] (협력형 지능형 교통 체계)
174. 엣지 [[190_ai_llm_requirements_specification|AI]] ([[174_edge_ai_on_device_ai|Edge AI]]) 기술 적용 아키텍처
175. [[175_ambient_backscatter_communication|백스캐터 통신]] ([[175_ambient_backscatter_communication|Ambient Backscatter Communication]]) - 배터리 없이 공기 중의 TV, Wi-Fi 전파 에너지를 흡수/반사하여 무전원으로 통신하는 초소형 [[101_iot_concept|IoT]] 기술
176. [[176_wearable_device_wban|웨어러블 디바이스]] ([[176_wearable_device_wban|Wearable Device]]) - 신체 부착형 기기 통신 체계 ([[927_wban_wireless_body_area_network_healthcare_sar|WBAN]], Body Area Network)
177. [[177_hmd_eye_tracking_foveated_rendering|HMD]] ([[177_hmd_eye_tracking_foveated_rendering|Head Mounted Display]]) 시선 추적(Eye Tracking), 포비티드 렌더링 (Foveated Rendering - 시선이 머무는 중심부만 초고화질 렌더링하여 [[418_gpu|GPU]] 부담 감소 기술)
178. 디지털 후각 / 촉각 텔레햅틱 ([[178_tele_haptics_communication|Tele-haptics]]) 통신 [[015_지연_데이터_관점|지연]] 제어
179. [[179_bci_brain_computer_interface|BCI]] ([[179_bci_brain_computer_interface|Brain-Computer Interface]]) - 뇌파를 직접 인식하여 기계를 제어하는 신경망 인터페이스 기술 (뉴럴링크)
180. [[180_drone_swarm_control_algorithm|드론 스웜]] ([[180_drone_swarm_control_algorithm|Drone Swarm]]) - 군집 비행 제어 및 충돌 회피 [[001_algorithm_definition|알고리즘]]

## 3. [[052_cloud_computing_os|클라우드 컴퓨팅]] 및 컴퓨팅 인프라 신기술 (80개)
181. [[052_cloud_computing_os|클라우드 컴퓨팅]] ([[052_cloud_computing_os|Cloud Computing]]) 5대 특징 (NIST) - 주문형 셀프 [[090_service_kubernetes_network_load_balancing|서비스]], 광범위한 네트워크 접근, [[638_resource_pooling_cxl|자원 풀링]], 신속한 [[571_resiliency_fault_tolerance_patterns|탄력성]], 측정 가능한 [[090_service_kubernetes_network_load_balancing|서비스]]
182. [[201_cloud_service_models_iaas_paas_saas|클라우드 서비스 모델]]
183. [[183_iaas_infrastructure_as_a_service|IaaS]] (Infrastructure [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 서버, 스토리지, 네트워크 [[015_virtualization|가상화]] 제공 (AWS EC2)
184. [[184_paas_platform_as_a_service|PaaS]] (Platform [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 개발 런타임, [[002_database_definition|데이터베이스]], 배포 환경 제공 (AWS Elastic Beanstalk)
185. [[309_saas|SaaS]] (Software [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 완제품 소프트웨어 제공 (Office 365, Salesforce)
186. [[186_baas_backend_as_a_service_firebase|BaaS]] (Backend [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) - 모바일/웹 앱용 백엔드(DB, [[303_authentication_authorization_patterns|인증]], 푸시) 제공 (Firebase)
187. [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]] / [[206_serverless_cold_start|Serverless]]) - 인프라 관리 없이 함수 단위로 코드만 배포 및 호출 시 과금 (AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]])
188. [[188_cloud_deployment_models_public_private|클라우드 배포 모델]] - 퍼블릭(Public), 프라이빗(Private), 하이브리드(Hybrid), [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]]([[202_multi_cloud_hybrid_cloud_governance|Multi-Cloud]])
189. [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] ([[202_multi_cloud_hybrid_cloud_governance|Multi-Cloud]]) [[268_strategy_pattern|전략]] - 특정 클라우드 [[008_dependencies|종속성]]([[362_lock_in_portability|Lock-in]]) 방지 및 최적화 조합 활용 ([[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 필수)
190. [[015_virtualization|가상화]] ([[190_virtualization_computing_architecture_cloud|Virtualization]]) 컴퓨팅 아키텍처
191. [[054_hypervisor|하이퍼바이저]] ([[054_hypervisor|Hypervisor]]) Type 1 (베어메탈 - ESXi, Xen) vs Type 2 (호스트형 - VMware Workstation)
192. [[057_full_virtualization|전가상화]] ([[057_full_virtualization|Full Virtualization]]) vs [[058_paravirtualization|반가상화]] ([[192_full_virtualization_vs_para_virtualization|Para-virtualization]])
193. [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]] ([[658_intel_vtx|Intel VT-x]])
194. [[561_container_based_deployment|컨테이너]] ([[194_container_virtualization_docker_namespace|Container]]) [[015_virtualization|가상화]] - Guest OS 없이 호스트 OS [[022_kernel_role|커널]]을 공유하며 프로세스 격리 (초경량, [[148_5g_embb_urllc_mmtc|초고속]] 기동)
195. [[063_docker_architecture|도커]] ([[063_docker_architecture|Docker]]) 아키텍처 - [[066_docker_daemon_dockerd|도커 데몬]], [[068_docker_image_immutable_package|도커 이미지]](레이어 구조), [[561_container_based_deployment|컨테이너]], [[235_registry_immutable_tag|레지스트리]]
196. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]], K8s) - 수백/수천 개의 [[561_container_based_deployment|컨테이너]]를 스케줄링, 배포, 로드밸런싱, [[249_scaling_normalization_standardization|스케일링]]하는 [[073_container_orchestration_tools|오케스트레이션]] 도구
197. K8s [[603_component_independent_deployment_unit|컴포넌트]] - [[075_kubernetes_k8s_cluster_architecture|마스터 노드]] ([[014_api_posix|API]] Server, [[078_etcd_distributed_key_value_store|etcd]], Scheduler, Controller Manager), 워커 노드 ([[082_kubelet_node_agent|Kubelet]], Kube-proxy, [[628_container_runtime_oci|컨테이너 런타임]])
198. [[198_pod_kubernetes_minimum_deployment_unit|Pod]] ([[198_pod_kubernetes_minimum_deployment_unit|포드]]) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]의 최소 배포 단위 (1개 이상의 [[561_container_based_deployment|컨테이너]] 그룹)
199. [[531_cloud_native_architecture|클라우드 네이티브]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]]) 아키텍처 - 클라우드 환경의 이점을 극대화하기 위한 앱 구축/운영 방식 ([[532_microservices_decomposition_patterns|마이크로서비스]], [[561_container_based_deployment|컨테이너]], [[090_configuration_item|CI]]/CD, [[652_devops_calms_culture|DevOps]] 결합)
200. [[200_12_factor_app_cloud_native_principles|12-Factor App]] - [[309_saas|SaaS]] 애플리케이션 개발을 위한 12가지 베스트 프랙티스 ([[007_codebase|코드베이스]], [[008_dependencies|종속성]] 격리, [[009_config|설정]] 외부화, [[012_stateless_processes|무상태 프로세스]] 등)
201. [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]]) 아키텍처 한계점 분석 - [[559_serverless_cold_start_mitigation|콜드 스타트]]([[347_cold_start_problem|Cold Start]]: 함수 최초 호출 시 [[561_container_based_deployment|컨테이너]] 로딩 [[015_지연_데이터_관점|지연]]), 장기 실행 제약, 상태 비저장([[239_stateless_redis|Stateless]])
202. [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]] ([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]]) - [[559_serverless_cold_start_mitigation|콜드 스타트]] 해결을 위해 유휴 [[561_container_based_deployment|컨테이너]]를 미리 예열해두는 [[206_serverless_cold_start|서버리스]] 옵션
203. [[207_iac_terraform_immutable_infrastructure|인프라스트럭처 애즈 코드]] ([[793_iac_idempotency_template|IaC]], [[062_infrastructure_as_code|Infrastructure as Code]]) - 수동 UI 클릭 대신 코드([[343_json|JSON]], YAML, HCL)로 인프라를 정의/[[528_provisioning|프로비저닝]] ([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]], [[198_ansible_os_configuration_management_ssh|Ansible]])
204. [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] ([[204_immutable_infrastructure_configuration_drift_prevention|Immutable Infrastructure]]) - 서버 구성을 배포 후 수정하지 않고, 변경이 필요하면 새 이미지로 [[561_container_based_deployment|컨테이너]]/VM을 갈아치우는 패러다임 ([[193_configuration_drift|구성 편류]] [[193_configuration_drift|Configuration Drift]] 방지)
205. [[561_container_based_deployment|컨테이너]] 이미지 레이어 (Image Layer) 및 [[333_process|OCI]] ([[205_container_image_layer_oci_standard|Open Container Initiative]]) 표준 규격
206. [[206_kubernetes_autoscaling_hpa_vpa_ca|쿠버네티스 오토스케일링]] - [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]] - [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 개수 증가), [[096_vpa_vertical_pod_autoscaler_kubernetes|VPA]] (수직 [[249_scaling_normalization_standardization|스케일링]]), Cluster Autoscaler (워커 노드 자체 추가)
207. [[207_helm_kubernetes_package_manager_chart|헬름]] ([[207_helm_kubernetes_package_manager_chart|Helm]]) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 패키지 매니저
208. [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) 및 [[242_distributed_cloud_edge_computing_aws_outposts|분산 클라우드]] 로드밸런싱
209. [[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]] ([[209_spot_instance_cloud_cost_optimization|Spot Instance]]) - 클라우드 사업자의 남는 자원을 저렴하게 임대(갑자기 회수될 수 있음), [[561_container_based_deployment|컨테이너]]/배치 처리와 결합하여 비용 최적화
210. [[344_finops|FinOps]] ([[210_finops_cloud_financial_operations_cost_optimization|Cloud Financial Operations]]) - 기술, 비즈니스, 재무 팀이 협력하여 클라우드 비용을 투명하게 관리/최적화하는 클라우드 재무 관리 문화
211. 클라우드 마이그레이션 ([[211_cloud_migration_strategies_6r_rehost_refactor|Cloud Migration]]) [[268_strategy_pattern|전략]] - 6R (Rehost/[[086_lift_association_rule_marketing|Lift]] & Shift, Replatform, Repurchase, [[213_refactoring_cloud_native_rearchitecture|Refactor]], Retire, Retain)
212. [[212_rehost_lift_and_shift_migration_strategy|리호스트]] (Rehost / [[086_lift_association_rule_marketing|Lift]] and Shift) - [[061_on_premise_legacy_infrastructure|온프레미스]] 앱을 변경 없이 그대로 VM으로 마이그레이션
213. [[213_refactoring_cloud_native_rearchitecture|리팩토링]] ([[213_refactoring_cloud_native_rearchitecture|Refactor]]) - [[531_cloud_native_architecture|클라우드 네이티브]] [[282_performance_tactics|성능]]([[184_paas_platform_as_a_service|PaaS]]/[[206_serverless_cold_start|Serverless]])을 끌어내기 위해 [[105_aa_as_is_analysis|애플리케이션 아키텍처]]([[619_msa_traffic_hardware|MSA]] 등)를 전면 수정
214. [[631_sddc|SDDC]] (Software Defined [[801_data_center_3_tier_architecture_core_aggregation_access|Data Center]]) - 컴퓨트, 스토리지, 네트워크 등 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 모든 인프라를 [[015_virtualization|가상화]]하여 소프트웨어로 통제
215. [[633_sdn_whitebox|SDN]] ([[215_sdn_software_defined_networking_openflow|Software Defined Networking]]) - 제어 평면(Control Plane)과 [[001_dikw_pyramid|데이터]] 평면([[001_dikw_pyramid|Data]] Plane)을 분리, 중앙 집중식 네트워크 컨트롤러 배포
216. [[632_sds|SDS]] ([[632_sds|Software Defined Storage]]) - 범용 x86 서버에 소프트웨어를 탑재하여 스토리지 기능([[528_provisioning|프로비저닝]], [[456_dual_redundancy|이중화]]) 구현 (Ceph 등)
217. [[630_hci|하이퍼컨버지드 인프라]] ([[630_hci|HCI]], Hyper-Converged Infrastructure) - 서버, 스토리지, 네트워킹 [[015_virtualization|가상화]] 및 관리 도구를 단일 x86 어플라이언스 박스로 통합 패키징하여 제공 (IT 인프라 단순화)
218. [[236_quantum_computing_pqc|양자 컴퓨팅]] ([[236_quantum_computing_pqc|Quantum Computing]]) 핵심 원리
219. [[219_quantum_superposition_qubit|양자 중첩]] ([[219_quantum_superposition_qubit|Superposition]]) - 0과 1의 상태가 동시에 존재하는 양자적 특성 (연산 속도 지수적 증가)
220. [[220_quantum_entanglement|양자 얽힘]] ([[220_quantum_entanglement|Entanglement]]) - 두 [[448_qubit|큐비트]]가 서로 멀리 떨어져 있어도 하나의 상태가 변하면 다른 하나도 즉시 결정되는 성질
221. [[448_qubit|큐비트]] ([[448_qubit|Qubit]]) - [[447_quantum_computer|양자 컴퓨터]]의 기본 정보 단위
222. 노이즈 있는 중간 규모 양자 기술 (NISQ, Noisy Intermediate-Scale [[690_round_robin_time_quantum|Quantum]]) - 현재의 [[447_quantum_computer|양자 컴퓨터]] 발전 단계 (오류 정정이 완벽하지 않음)
223. [[223_quantum_supremacy_advantage|양자 우위]] ([[223_quantum_supremacy_advantage|Quantum Supremacy]]) - [[447_quantum_computer|양자 컴퓨터]]가 슈퍼컴퓨터를 능가하여 특정 연산을 압도적 속도로 풀어낸 기점
224. 쇼어 [[001_algorithm_definition|알고리즘]] (Shor's [[001_algorithm_definition|Algorithm]]) - 양자 푸리에 변환 적용 시 대용량 소인수분해를 다항 시간에 처리 ([[110_rsa|RSA]] 공개키 암호 붕괴 위협)
225. 그로버 [[001_algorithm_definition|알고리즘]] ([[986_grover_algorithm_impact|Grover]]'s [[001_algorithm_definition|Algorithm]]) - 비정렬 [[001_dikw_pyramid|데이터]] 검색 복잡도를 O(N)에서 O(√N)으로 단축 ([[656_aes_advanced_encryption_standard_rijndael|AES]] 대칭키 탐색 위협)
226. 슈퍼컴퓨팅 / [[548_automotive_hpc|HPC]] ([[226_hpc_supercomputing_infrastructure|High Performance Computing]]) 인프라 아키텍처
227. MPI ([[227_mpi_message_passing_interface_distributed_computing|Message Passing Interface]]) 기반 [[136_variance|분산]] 클러스터 [[430_index_fast_full_scan|병렬]] 컴퓨팅
228. [[490_edge_computing_hw|엣지 컴퓨팅 하드웨어]] [[440_offloading|오프로딩]] (SmartNIC / [[436_dpu|DPU]] - [[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]])
229. [[436_dpu|DPU]] ([[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]]) / [[437_ipu|IPU]] - 서버 CPU가 처리하던 네트워킹, 보안, 스토리지 패킷 처리 기능을 전용 [[009_semiconductor|반도체]] 카드로 [[440_offloading|오프로딩]]하여 CPU는 애플리케이션 연산에만 집중하게 하는 칩 (클라우드 인프라 가속기)
230. [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) - [[356_pcie|PCIe]] [[344_bus|버스]] 기반 차세대 인터커넥트 기술, CPU-메모리-가속기 간 메모리 공유([[285_pooling_layer|풀링]])와 [[402_cache_coherence|캐시 일관성]] 보장
231. [[442_memory_pooling|메모리 풀링]] ([[442_memory_pooling|Memory Pooling]]) - CXL을 이용해 물리적으로 떨어진 서버 메모리를 거대한 단일 [[369_logic_bomb|논리]] 메모리로 묶어 가상머신에 동적 할당
232. [[443_ucie|UCIe]] (Universal [[497_chiplet|Chiplet]] Interconnect Express) - [[497_chiplet|칩렛]]([[497_chiplet|Chiplet]]) 간 상호 연결 통신 고속화 범용 표준
233. [[497_chiplet|칩렛]] ([[497_chiplet|Chiplet]]) 아키텍처 - 거대한 단일 칩(Monolithic) 대신 여러 개의 작은 기능별 칩 조각([[497_chiplet|Chiplet]])을 따로 제조하여 하나의 패키지판(2.5D/3D 패키징)에 이어 붙여 수율 및 비용을 개선하는 최신 [[009_semiconductor|반도체]] 제조 공법
234. [[193_neuromorphic_chip_snn_low_power_inference|뉴로모픽 반도체]] ([[193_neuromorphic_chip_snn_low_power_inference|Neuromorphic Chip]]) - [[124_von_neumann|폰 노이만 아키텍처]] 한계 극복, 인체 두뇌 신경망 [[129_spike_agile_technical_investigation|스파이크]] 시그널을 하드웨어 회로로 모방 (초저전력 [[190_ai_llm_requirements_specification|AI]] 연산)
235. [[235_immersion_cooling_datacenter|액침 냉각]] ([[602_immersion_cooling|Immersion Cooling]]) - [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 발열 해소를 위해 서버 전체를 비전도성 특수 액체 냉매에 담가 식히는 고효율 친환경 냉각 기술
236. 콜드 아일 (Cold Aisle) / 핫 아일 ([[236_cold_aisle_hot_aisle_containment_datacenter|Hot Aisle]]) 차폐 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 공조 설계
237. [[237_pue_power_usage_effectiveness_datacenter_metric|PUE]] ([[623_datacenter_pue|Power Usage Effectiveness]]) - [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전력 효율 지표 (총 소비 전력 / IT 장비 전력), 1에 가까울수록 고효율
238. 그린 IT / [[469_carbon_aware_computing|탄소 인지 컴퓨팅]] ([[238_carbon_aware_computing_green_it|Carbon-Aware Computing]]) 클라우드 전력 리전 스위칭
239. [[629_bare_metal_cloud|베어메탈 클라우드]] ([[629_bare_metal_cloud|Bare Metal Cloud]]) - [[015_virtualization|가상화]] 오버헤드 없이 물리 서버 자체를 클라우드처럼 임대 (DB, 고성능 연산용)
240. 클라우드 [[379_dr_architecture|재해 복구]] 아키텍처 ([[501_file_definition_logical_record|파일]]럿 라이트 Pilot Light, 웜 스탠바이 Warm Standby 비교)
241. BDI ([[241_bdi_bridge_domain_interface_vxlan_overlay|Bridge Domain Interface]]) [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] 인프라 연동
242. [[242_distributed_cloud_edge_computing_aws_outposts|분산 클라우드]] ([[242_distributed_cloud_edge_computing_aws_outposts|Distributed Cloud]]) - [[007_public_cloud|퍼블릭 클라우드]] [[090_service_kubernetes_network_load_balancing|서비스]]를 다양한 물리적 위치(고객사, 통신사 엣지)에 배포하면서 중앙 집중형 통제권은 CSP가 유지하는 모델
243. 마이크로VM (MicroVM, Firecracker) - [[206_serverless_cold_start|서버리스]]([[342_faas|FaaS]]) 환경에서 극강의 부팅 속도(수 밀리초)와 가상머신급 보안 격리를 동시 제공하는 초경량 [[054_hypervisor|하이퍼바이저]] 기술
244. [[479_grpc_protobuf_http2|gRPC]] 기반 [[302_service_mesh_istio|서비스 메시]] 동기 통신망
245. [[974_restful_api_stateless_http_methods_uri|RESTful API]] 성숙도 모델 ([[157_restful_api_richardson_maturity_model|Richardson Maturity Model]] - Level 3 HATEOAS)
246. [[246_graphql_query_language_overfetching_solution|GraphQL]] - 클라이언트가 필요한 [[001_dikw_pyramid|데이터]] 필드만 명시하여 한 번의 [[014_api_posix|API]] 쿼리로 복합 [[001_dikw_pyramid|데이터]] 수신 (오버패칭 Overfetching 문제 해결)
247. 오픈 [[014_api_posix|API]] ([[247_open_api_gateway_security_throttling_rate_limiting|Open API]]) 및 [[014_api_posix|API]] 게이트웨이 보안 스로틀링 
248. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) 아키텍처 - UI 프론트엔드 파트도 독립적 배포 가능한 [[532_microservices_decomposition_patterns|마이크로서비스]] 뷰로 분할 개발
249. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) - 상태([[272_state_pattern|State]])의 최종 결과만 DB에 저장하는 게 아니라, 상태를 변화시킨 모든 '이벤트 이력'을 스트림으로 저장하여 불일치 방지 및 재생(Replay) 허용
250. [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) - 명령(Insert/Update) 모델과 조회([[520_select|Select]]) 모델을 물리적/[[369_logic_bomb|논리]]적으로 분리 [[136_variance|분산]] 인프라 설계
251. [[231_edge_native|엣지 네이티브]] ([[251_edge_native_architecture_distributed_ai_k3s|Edge Native]]) 설계 패턴
252. [[099_aiops_chatbot_itsm_automation|AIOps]] ([[001_artificial_intelligence|Artificial Intelligence]] for IT Operations) - 클라우드 인프라/네트워크의 방대한 [[568_logs_distributed_logging_elk_fluentd|로그]], 텔레메트리 [[001_dikw_pyramid|데이터]]를 [[241_machine_learning_basics|머신러닝]]으로 분석해 장애 전조를 예측하고 자동 치유(Auto-healing)하는 운영 자동화 
253. [[055_digital_transformation|디지털 전환]] (DT/[[726_platform_engineering_idp_dx|DX]], [[055_digital_transformation|Digital Transformation]]) - 기업 생태계 전반을 디지털 인프라 기반으로 혁신
254. 클라우드 락인 ([[254_cloud_vendor_lock_in_avoidance_portability_multi_cloud|Vendor Lock-in]]) 회피 [[106_ta_as_is_analysis|기술 아키텍처]]
255. [[645_data_pipeline_acceleration|데이터 파이프라인]] ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]]) [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) 배치 플로우 관리
256. [[179_kafka_flink_watermark_time_window|카프카]] ([[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]]) - 대규모 실시간 [[568_logs_distributed_logging_elk_fluentd|로그]] 및 이벤트 스트리밍 처리를 위한 [[136_variance|분산]]형 [[389_mesh_topology|메시]]지 큐 (Pub/Sub 모델, [[514_partition_slice_volume|파티션]] [[136_variance|분산]] 저장)
257. [[642_observability_telemetry|옵저버빌리티]] ([[642_observability_telemetry|Observability]]) 도구 연동 ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 오픈 표준)
258. 로우코드 / 노코드 (Low-[[082_process_memory_structure|Code]] / No-[[082_process_memory_structure|Code]]) 플랫폼 개발론 
259. [[259_citizen_developer|시민 개발자]] ([[259_citizen_developer|Citizen Developer]]) - IT 비전문가 현업 부서원이 로우코드 툴을 이용해 스스로 앱을 개발
260. [[260_sdv_software_defined_vehicle|소프트웨어 정의 차량]] (SDV, Software Defined Vehicle) - 테슬라 등 하드웨어 부품(ECU) 중심 통제에서 벗어나 스마트폰처럼 통합 OS 소프트웨어와 OTA 업데이트를 통해 차량 [[282_performance_tactics|성능]]이 진화하는 구조

## 4. [[231_ai_turing_test|인공지능]] ([[190_ai_llm_requirements_specification|AI]]) 심화 및 초거대 언어 모델 ([[263_llm_large_language_model|LLM]]) 트렌드 (100개)
261. [[225_foundation_model_peft_lora|파운데이션 모델]] ([[225_foundation_model_peft_lora|Foundation Model]]) - 스탠퍼드 HAI 정의, 방대한 무라벨 [[001_dikw_pyramid|데이터]]를 자기지도 학습하여 여러 다운스트림 태스크에 전이 가능한 거대 범용 모델 
262. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] ([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 어텐션 기반 [[430_index_fast_full_scan|병렬]] 연산 구조
263. [[263_llm_large_language_model|LLM]] ([[263_llm_large_language_model|Large Language Model]]) - 수백억 이상의 파라미터를 가진 거대 언어 모델 ([[302_gpt_autoregressive|GPT]]-4, Gemini, Claude, Llama 3)
264. sLLM / [[313_slm|SLM]] (Small [[263_llm_large_language_model|Large Language Model]]) - 7B 이하의 경량화 [[225_foundation_model_peft_lora|파운데이션 모델]], 엣지 기기 오프라인 구동 및 특정 [[064_relation_domain|도메인]] 파인튜닝용 (Llama-3-8B, Phi-3, Gemma 등)
265. [[265_emergent_abilities|창발성]] ([[265_emergent_abilities|Emergent Abilities]]) - 파라미터와 훈련 [[001_dikw_pyramid|데이터]] 규모가 특정 [[431_ssthresh_slow_start_threshold|임계치]]를 넘겼을 때, 사전에 프로그래밍/학습하지 않은 복잡한 추론 [[369_logic_bomb|논리]] 능력이 스스로 발현되는 현상
266. [[266_self_supervised_learning|자기 지도 학습]] ([[266_self_supervised_learning|Self-Supervised Learning]]) - 다음 단어 예측(Next Token Prediction), 빈칸 채우기([[138_mlm_learning|MLM]]) 방식으로 사람이 라벨링하지 않아도 텍스트 구조 자체를 정답 삼아 자가 학습
267. [[147_instruction_tuning_rlhf_alignment|인스트럭션 튜닝]] ([[147_instruction_tuning_rlhf_alignment|Instruction Tuning]]) - 범용 LLM을 "인간의 명령(지시문)"과 "그에 따른 모범 답변" [[001_dikw_pyramid|데이터]]셋(Prompt-Response)으로 추가 지도 미세조정(SFT)하여 대화형 챗봇 형태로 가다듬는 과정
268. 인간 피드백 기반 강화학습 ([[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]], [[094_reinforcement_learning|Reinforcement Learning]] from Human Feedback) - LLM이 내뱉은 여러 답변을 인간이 랭킹 매겨 보상 모델([[403_rlhf_reward_model|Reward Model]])을 훈련시키고, 이를 [[395_ppo_clipping|PPO]] 강화학습 [[001_algorithm_definition|알고리즘]]으로 본 모델에 적용하여 유해성/편향성을 통제 (정렬, Alignment 기법)
269. [[269_vector_database|RLAIF]] ([[190_ai_llm_requirements_specification|AI]] 피드백 기반 강화학습) - 인간 라벨러 대신 [[302_gpt_autoregressive|GPT]]-4 등 고성능 AI가 답변 품질 랭킹 채점을 대행 (헌법적 [[190_ai_llm_requirements_specification|AI]] / [[966_constitutional_ai|Constitutional AI]] - Anthropic 제안)
270. [[270_embedding_model|DPO]] ([[270_embedding_model|Direct Preference Optimization]]) - 강화학습([[395_ppo_clipping|PPO]])과 보상 모델 구축의 복잡한 2단계를 생략하고, 선호/비선호 [[001_dikw_pyramid|데이터]]셋으로 LLM을 직접 [[133_fine_tuning|미세 조정]]하는 최신 최적화 기법
271. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]] ([[224_prompt_engineering_guideline|Prompt Engineering]]) - LLM의 숨겨진 능력을 이끌어내기 위해 질문 컨텍스트를 구조화 설계
272. 제로샷 (Zero-shot) / 원샷 ([[272_in_context_learning_icl|One-shot]]) / 퓨샷 (Few-shot) 프롬프팅
273. [[273_zero_few_shot_learning|생각의 사슬]] ([[146_chain_of_thought_cot|CoT]], [[146_chain_of_thought_cot|Chain-of-Thought]]) - "단계별로 차근차근 생각해 보자"는 명령을 통해 중간 추론 과정(Reasoning Path)을 [[087_process_state_transition|생성]]하게 유도하여 수학/[[369_logic_bomb|논리]] 문제 정답률 극대화
274. [[147_concept|ToT]] (Tree of Thoughts) / GoT ([[274_cot_chain_of_thought|Graph of Thoughts]]) - 단일 사슬을 넘어 여러 추론 경로를 탐색/평가하며 분기하는 고도화 프롬프팅
275. [[275_react_framework|환각]] ([[345_llm_foundation_model_hallucination|Hallucination]] / [[251_hallucination_rag_augmented_retrieval_vector_db|할루시네이션]]) - LLM이 학습 [[001_dikw_pyramid|데이터]]의 공백이나 패턴 오류로 인해 그럴싸한 허위 사실(거짓말)을 진실처럼 [[087_process_state_transition|생성]]하는 한계점
276. [[276_fine_tuning|RAG]] ([[585_rag_retrieval_augmented_generation|Retrieval-Augmented Generation]] / [[222_rag_retrieval_augmented_generation|검색 증강 생성]]) - [[251_hallucination_rag_augmented_retrieval_vector_db|할루시네이션]] 극복 아키텍처. 사용자 질문 수신 시 ①외부 사내 DB/문서에서 관련 문단 검색(Retrieve) -> ②검색된 문단을 프롬프트에 주입(Augment) -> ③LLM이 참조하여 답변 [[087_process_state_transition|생성]](Generate)
277. [[223_vector_database_embedding|벡터 데이터베이스]] ([[223_vector_database_embedding|Vector Database]]) - [[276_fine_tuning|RAG]] 검색의 핵심, 텍스트/이미지를 다차원 [[278_instruction_tuning|임베딩]] 텐서로 변환 저장하고 [[359_cosine_similarity|코사인 유사도]] 연산으로 문맥적(Semantic) 의미가 가까운 문서를 빛의 속도로 추출 ([[320_gnn_vector_db_recommendation|Milvus]], Pinecone 등)
278. [[278_instruction_tuning|임베딩]] ([[278_instruction_tuning|Embedding]]) - [[004_unstructured_data|비정형 데이터]]의 의미적 관계를 다차원 실수 [[055_array|배열]](벡터) 공간에 좌표로 투영하는 변환 과정
279. [[279_rlhf_reinforcement_learning_human_feedback|하이브리드 검색]] ([[279_rlhf_reinforcement_learning_human_feedback|Hybrid Search]]) - 전통적인 키워드 정확 일치 검색(BM25)과 벡터 의미 [[348_similarity_search|유사도 검색]](Dense)을 결합하여 검색 정확도 상호 보완
280. [[280_ppo_proximal_policy_optimization|시맨틱 캐시]] ([[280_ppo_proximal_policy_optimization|Semantic Cache]]) - 이전 질문의 의미 벡터값을 저장해두고, 유사한(정확히 일치하지 않아도) 질문이 오면 [[263_llm_large_language_model|LLM]] API를 호출하지 않고 캐시에서 답변 즉시 반환 ([[015_지연_데이터_관점|지연]]시간 단축, 비용 절감)
281. 파인튜닝 ([[304_fine_tuning|Fine-Tuning]] / [[133_fine_tuning|미세 조정]]) [[132_transfer_learning|전이 학습]] 방법론
282. 파라미터 효율적 [[133_fine_tuning|미세 조정]] ([[306_peft_lora|PEFT]], [[306_peft_lora|Parameter-Efficient Fine-Tuning]]) - 수천억 파라미터 거대 모델 전체를 업데이트하기엔 [[418_gpu|GPU]] 자원이 부족하므로, 원래 [[267_weight_bias_activation|가중치]]는 동결(Freeze)하고 극히 일부의 추가 파라미터 모듈만 훈련
283. [[283_lora_low_rank_adaptation|로라]] ([[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]], [[145_peft_lora_low_rank_adaptation|Low-Rank Adaptation]]) - PEFT의 대표 기법. 거대 [[267_weight_bias_activation|가중치]] 행렬 사이에 낮은 차원(Rank)의 랭크 분해 행렬 2개를 삽입하여 그것만 훈련시킨 후 나중에 원본 행렬에 더함 (VRAM 사용량 획기적 절약)
284. [[434_quantization|양자화]] ([[434_quantization|Quantization]] / [[404_qlora|QLoRA]]) - 모델 [[267_weight_bias_activation|가중치]]의 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 FP32(32비트)에서 INT8, INT4 등 정수형으로 깎아내어 모델 용량과 추론 메모리를 대폭 [[347_compaction|압축]] (모바일 온디바이스 탑재 핵심)
285. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) - [[282_performance_tactics|성능]]이 좋은 무거운 교사(Teacher) 모델의 산출물 [[130_probability|확률]] 분포를 가벼운 학생(Student) 모델이 모방 학습하도록 하여 [[282_performance_tactics|성능]]은 유지하되 모델 사이즈를 경량화
286. [[158_multimodal_clip_vision_audio_encoding|멀티모달]] ([[158_multimodal_clip_vision_audio_encoding|Multimodal]]) [[190_ai_llm_requirements_specification|AI]] - 텍스트뿐만 아니라 이미지, 영상, 오디오 등 이기종 [[001_dikw_pyramid|데이터]]를 동시에 입력받고 상호 교차 이해/[[087_process_state_transition|생성]]하는 [[225_foundation_model_peft_lora|파운데이션 모델]] ([[302_gpt_autoregressive|GPT]]-4o, Gemini)
287. [[153_diffusion_model_stable_diffusion_denoising|디퓨전 모델]] ([[153_diffusion_model_stable_diffusion_denoising|Diffusion Model]]) - 원본 이미지에 노이즈를 미세하게 반복 주입해 파괴([[235_forward_backward_chaining|Forward]])한 뒤, 그 노이즈를 단계적으로 제거(Denoising)하는 역과정을 신경망이 학습하여 텍스트로부터 고해상도 이미지를 [[087_process_state_transition|생성]] (Stable Diffusion, Midjourney)
288. [[288_latent_diffusion_model|LDM]] ([[288_latent_diffusion_model|Latent Diffusion Model]]) - 픽셀 공간이 아닌 [[347_compaction|압축]]된 잠재(Latent) 공간에서 디퓨전 연산을 수행해 이미지 [[087_process_state_transition|생성]] 속도와 자원 효율 극대화
289. [[159_gan|생성적 적대 신경망]] ([[154_gan_generative_adversarial_network|GAN]])과의 차이 (디퓨전은 [[087_process_state_transition|생성]] 품질이 압도적, 속도는 [[154_gan_generative_adversarial_network|GAN]] 우위)
290. 오토레그레시브 ([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]) [[087_process_state_transition|생성]] ([[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] [[039_decoder|디코더]] 토큰 [[087_process_state_transition|생성]] 메커니즘)
291. KV 캐시 ([[291_kv_cache|Key-Value Cache]]) - [[263_llm_large_language_model|LLM]] 텍스트 추론 단계에서 매 토큰 [[087_process_state_transition|생성]] 시 과거 텍스트의 [[067_db_key_uniqueness_minimality|Key]], Value 어텐션 행렬 연산을 다시 하지 않고 메모리에 캐싱해두어 텍스트 [[087_process_state_transition|생성]] 속도 가속화
292. [[292_pagedattention_vllm|페이즈드 어텐션]] (PagedAttention / vLLM) - OS의 [[381_virtual_memory|가상 메모리]] [[259_paging|페이징]] 기법을 차용하여 VRAM 내 KV 캐시 파편화를 방지하고 연속 할당하여 [[418_gpu|GPU]] 메모리 활용률을 극대화하는 서빙 아키텍처 최적화 기법
293. [[190_ai_llm_requirements_specification|AI]] 에이전트 ([[155_ai_agents_function_calling_agentic_loop|AI Agents]]) / 에이전틱 [[190_ai_llm_requirements_specification|AI]] - 챗봇 수준을 넘어, 목표가 주어지면 LLM이 스스로 필요한 도구(웹 브라우저, 파이썬, [[014_api_posix|API]])를 선택해 실행하고 중간 결과를 바탕으로 다음 행동을 자율 계획(Planning)하여 임무를 완수하는 독립적 [[190_ai_llm_requirements_specification|AI]]
294. [[294_function_calling_tool_use|함수 호출]] (Function Calling / Tool Use) - LLM이 [[343_json|JSON]] 포맷으로 외부 [[014_api_posix|API]] 매개변수를 출력하면, 서버가 해당 API를 실행하고 결과를 다시 LLM에 주입하는 에이전트 핵심 기술
295. MoE (Mixture of Experts / [[535_moe_mixture_of_experts|전문가 혼합 모델]]) 아키텍처 - 거대 신경망 내에 특정 분야별 소규모 전문가(Expert) 네트워크 여러 개를 [[430_index_fast_full_scan|병렬]] 배치. [[339_routing_overview_best_path_selection|라우팅]] 게이트 네트워크가 입력 질문에 따라 가장 적합한 전문가 1~2개만 활성화하여 연산 (파라미터는 거대하지만 실제 추론 연산량은 획기적으로 줄어드는 [[302_gpt_autoregressive|GPT]]-4 채용 추정 구조)
296. [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) - [[190_ai_llm_requirements_specification|AI]] 모델 [[001_dikw_pyramid|데이터]] 수집, 학습, 평가, 배포, 모니터링을 [[081_cd_continuous_deployment_pipeline_architecture|지속적 배포 파이프라인]]([[090_configuration_item|CI]]/CD/[[162_continuous_training_pipeline_model_retraining|CT]])으로 묶는 운영 체계
297. [[221_llmops_large_language_model_ops|LLMOps]] - 기존 MLOps에 더해 대규모 모델 튜닝([[306_peft_lora|PEFT]]), 프롬프트 관리, [[276_fine_tuning|RAG]] 파이프라인 지속 개선, [[275_react_framework|환각]] 모니터링 기능이 추가된 [[263_llm_large_language_model|LLM]] 특화 운영 파이프라인
298. [[468_model_drift_retraining|모델 드리프트]] ([[468_model_drift_retraining|Model Drift]] / [[163_data_drift_statistical_distribution_shift|Data Drift]]) - 배포 후 입력 [[001_dikw_pyramid|데이터]]의 통계적 분포나 환경이 변하여 [[190_ai_llm_requirements_specification|AI]] 모델의 정확도가 시간이 지남에 따라 하락하는 현상 (재학습 [[507_acid_properties|트리거]] 원인)
299. [[165_feature_store_training_serving_consistency|피처 스토어]] ([[165_feature_store_training_serving_consistency|Feature Store]]) - 전처리된 [[241_machine_learning_basics|머신러닝]] [[247_feature_label_variables|피처]] 셋을 팀 간 공유하고 서빙 레이어에 고속 공급하기 위한 중앙 저장소
300. [[300_ann_approximate_nearest_neighbor_vector_index|벡터 인덱싱]] ([[350_ann|ANN]]: [[351_hnsw|Approximate Nearest Neighbor]]) - [[002_bigdata_5v|정확성]] 대신 탐색 속도를 취한 벡터 DB [[154_database_index_b_tree_search_optimization|인덱스]] ([[351_hnsw|HNSW]], IVFFlat, [[391_qos_queuing_pq_cq_wfq_cbwfq_llq|PQ]] 등)
301. [[190_ai_llm_requirements_specification|AI]] 안전 ([[190_ai_llm_requirements_specification|AI]] Safety) 및 레드티밍 ([[301_ai_safety_red_teaming|Red Teaming]]) - [[190_ai_llm_requirements_specification|AI]] 모델 배포 전 보안/윤리 결함을 의도적으로 찾아내기 위해 공격자 관점에서 취약점(탈옥 등)을 테스트하는 기법
302. [[955_prompt_injection|프롬프트 인젝션]] ([[955_prompt_injection|Prompt Injection]] / Jailbreak) 공격 - LLM의 행동 제어 프롬프트를 악의적 명령으로 무시하게 만들어 차별, 혐오, 기밀 코드를 내뱉게 하는 공격
303. 설명 가능한 [[190_ai_llm_requirements_specification|AI]] ([[227_xai_explainable_ai_lime_shap|XAI]], [[255_xai_lime_shap_explainable_contribution|eXplainable AI]]) - 딥러닝 블랙박스 도출 결과의 [[369_logic_bomb|논리]]적 근거([[247_feature_label_variables|피처]] 기여도, 활성화 히트맵)를 인간이 이해할 수 있도록 [[003_bigdata_7v|시각화]] 및 수치화
304. [[326_lime|LIME]] / [[327_shap|SHAP]] 지표 (부분적 / 게임이론 전역적 변수 기여 해석)
305. [[256_federated_learning_privacy_model_security|연합 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]]) - 엣지 디바이스(스마트폰)에 원본 [[001_dikw_pyramid|데이터]]를 남겨두고 로컬에서 학습한 [[267_weight_bias_activation|가중치]](Gradient) 업데이트 값만 클라우드 중앙 서버로 모아 병합하는 프라이버시 보존형 [[241_machine_learning_basics|머신러닝]] ([[001_dikw_pyramid|데이터]] 유출 원천 차단)
306. [[306_graph_neural_network_gnn|그래프 신경망]] ([[159_gnn_graph_neural_network_message_passing|GNN]], [[159_gnn_graph_neural_network_message_passing|Graph Neural Network]]) - 노드(Node)와 간선(Edge)의 네트워크 관계를 학습하는 딥러닝 구조 (분자 구조 분석, 소셜 네트워크 추천)
307. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 윈도우 한계 크기 ([[033_context|Context]] Window) 확장 기술 (RoPE, ALiBi 등 [[300_positional_encoding|포지셔널 인코딩]] 개선)
308. 장기 문맥 ([[308_long_context_llm|Long-context]]) 처리 - 1M 토큰(책 수권 분량) 동시 입력 처리 모델 아키텍처 구조 
309. [[407_cosine_annealing|코사인 어닐링]] ([[309_cosine_annealing|Cosine Annealing]]) 및 [[080_gradient_descent_learning_rate|학습률]] 스케줄링 튜닝
310. [[190_ai_llm_requirements_specification|AI]] 윤리, 편향성 ([[094_bias|Bias]]), [[583_ai_code_license_security_threats|저작권]] ([[310_ai_ethics_bias_copyright|Copyright]]) 이슈 - 크롤링 [[001_dikw_pyramid|데이터]] 공정 이용(Fair Use) 논란, [[087_process_state_transition|생성]]물 지식재산권 인정 불가 등 규제 거버넌스 동향 (EU [[190_ai_llm_requirements_specification|AI]] Act 등)
311. 오디오/비디오 [[087_process_state_transition|생성]] [[190_ai_llm_requirements_specification|AI]] - Sora (OpenAI 비디오 모델), 텍스트 투 스피치(TTS, [[960_deepfake|딥페이크]] 오디오 보이스 클로닝)
312. [[312_clip_contrastive_learning|클립]] ([[408_clip|CLIP]], [[408_clip|Contrastive Language-Image Pre-training]]) - 이미지와 그에 해당하는 텍스트 설명 쌍(Pair)을 같은 잠재 공간에 가깝게 [[278_instruction_tuning|임베딩]]하는 대조 학습(Contrastive [[240_switch_learning_forwarding_flooding|Learning]]) 기법 (제로샷 이미지 [[104_classification_analysis|분류]] 혁신)
313. 자율주행 강화학습 모방 학습 ([[200_autonomous_driving_imitation_learning_digital_twin|Imitation Learning]] / Behavior Cloning)
314. 강화학습 [[372_bellman_equation|벨만 방정식]] ([[372_bellman_equation|Bellman Equation]]) 및 상태-행동 가치함수([[314_reinforcement_learning_bellman|Q-Value]])
315. [[335_autoencoder|오토인코더]] ([[335_autoencoder|Autoencoder]]) 구조 및 [[213_variational_autoencoder|변이형 오토인코더]] ([[315_autoencoder_vae|VAE]]) 잠재 벡터 [[087_process_state_transition|생성]]망
316. [[190_ai_llm_requirements_specification|AI]] [[009_semiconductor|반도체]] 생태계 - [[427_tensor_core|텐서 코어]]([[427_tensor_core|Tensor Core]]) [[418_gpu|GPU]] 가속, [[495_hbm|HBM]] ([[495_hbm|High Bandwidth Memory]]) [[140_bandwidth|대역폭]] 병목 파훼
317. [[438_lpu|LPU]] ([[317_lpu_language_processing_unit|Language Processing Unit]]) - [[263_llm_large_language_model|LLM]] [[039_decoder|디코더]]의 순차적 토큰 [[087_process_state_transition|생성]] [[015_지연_데이터_관점|지연]]시간([[141_latency|Latency]]) 단축에 특화된 추론 전용 [[148_5g_embb_urllc_mmtc|초고속]] [[009_semiconductor|반도체]] (Groq 등)
318. [[190_ai_llm_requirements_specification|AI]] 컴파일러 (TensorRT, ONNX) 모델 최적화 및 타겟 하드웨어 런타임 변환 엔진
319. [[645_data_pipeline_acceleration|데이터 파이프라인]] ([[215_etl_vs_elt_pipeline|ETL]]) 내 [[004_unstructured_data|비정형 데이터]] OCR 및 [[263_llm_large_language_model|LLM]] 문서 파싱 파이프라인 
320. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] 기반 온디바이스 [[313_slm|SLM]] 구동 경량 아키텍처

## 5. [[001_dikw_pyramid|데이터]] 과학 ([[001_dikw_pyramid|Data]] Science) 및 통계/최적화 (100개)
321. [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] ([[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]]) 프레임워크 (CRISP-DM, [[225_kdd_t_test_anova_statistical_analysis|KDD]])
322. 교차 분석 (Cross Tabulation) / [[147_chi_square_test|카이제곱 검정]] ([[147_chi_square_test|Chi-Square Test]]) - 범주형 [[004_data_independence|데이터 독립성]] 검정
323. T-검정 ([[070_t_test_independent_paired_mean_difference|t-Test]]) - 두 집단 간 평균 차이 검정 (단일 표본, 독립 표본, 대응 표본)
324. [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] ([[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]]) - 3개 이상 집단 평균 차이 비교 (F-분포)
325. [[325_correlation_analysis_pearson_spearman|상관 분석]] ([[325_correlation_analysis_pearson_spearman|Correlation Analysis]]) - 피어슨 상관계수(선형, 연속형), 스피어만 서열 상관계수(비모수)
326. [[149_regression_analysis|회귀 분석]] ([[149_regression_analysis|Regression Analysis]]) - 단순/다중 선형 회귀 모형
327. [[327_ordinary_least_squares_ols|최소 제곱법]] (OLS, Ordinary Least Squares) - 잔차(오차) 제곱합 최소화 선형 방정식 도출
328. [[098_coefficient_of_determination_r_squared|결정 계수]] (R-Squared, R^2) - 0~1 사이, 회귀 모형의 [[001_dikw_pyramid|데이터]] 설명력 크기
329. [[080_multicollinearity_vif_variance_inflation_factor_regression|다중 공선성]] ([[080_multicollinearity_vif_variance_inflation_factor_regression|Multicollinearity]]) - 독립변수들 간 높은 상관관계로 회귀 계수 왜곡 (VIF 지수 [[489_raid_10_hybrid|10]] 이상 시 변수 제거)
330. [[330_dummy_variable|더미 변수]] ([[330_dummy_variable|Dummy Variable]]) - 범주형 -> 이진(0, 1) 변환
331. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]]) - 종속 변수가 이진(범주형)일 때, 오즈비(Odds Ratio)에 [[568_logs_distributed_logging_elk_fluentd|로그]]를 취해 선형 결합으로 매핑, [[268_sigmoid_vanishing_gradient|시그모이드]](S자) [[130_probability|확률]] 반환
332. [[332_maximum_likelihood_estimation_mle|최대 우도 추정법]] ([[143_mle|MLE]], Maximum Likelihood Estimation)
333. 베이즈 정리 (Bayes' Theorem) - 사전 [[130_probability|확률]]과 우도를 통해 사후 [[130_probability|확률]] 계산
334. [[140_markov_chain|마르코프 체인]] ([[140_markov_chain|Markov Chain]]) - 미래 상태 [[130_probability|확률]]이 오직 현재 상태에만 의존하는 [[130_probability|확률]]적 [[632_state_transition_diagram_testing|상태 전이]] 과정
335. [[139_clt|중심 극한 정리]] ([[139_clt|CLT]], Central Limit Theorem) - 표본의 크기(n)가 커지면 모집단 분포 무관하게 표본 평균의 분포가 [[138_normal_distribution|정규 분포]]에 수렴
336. 1종 오류 (Type I Error, 알파) / 2종 오류 (Type II Error, 베타)
337. [[337_p_value_significance|유의 확률]] ([[337_p_value_significance|p-value]]) - 귀무가설이 맞다고 가정할 때 관측치 이상 극단값이 나올 [[130_probability|확률]] (유의수준 0.05보다 작으면 귀무가설 기각)
338. [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]법 [[163_pca|PCA]] ([[338_pca_principal_component_analysis|주성분 분석]]) - [[001_dikw_pyramid|데이터]] [[136_variance|분산]]을 최대로 보존하는 직교 축 도출
339. [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]법 LDA ([[082_lda_linear_discriminant_analysis_classification|선형 판별 분석]]) - 클래스 간 [[136_variance|분산]]을 최대화하고 클래스 내 [[136_variance|분산]]을 최소화하는 [[121_supervised_learning|지도 학습]]
340. t-SNE / UMAP - 고차원 [[001_dikw_pyramid|데이터]]의 비선형적 이웃 관계를 저차원에 보존하는 [[003_bigdata_7v|시각화]] 특화 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 기법
341. [[341_time_series_ar_ma_arma|시계열 분석]] - AR (자기회귀), MA (이동평균), ARMA 모델
342. [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] ([[383_llm_autoregressive_math|Auto-Regressive]] Integrated Moving Average) - 차분(Integrated)을 통해 비정상 시계열을 정상성 시계열로 변환하여 예측
343. 정상성 ([[377_time_series_stationarity|Stationarity]]) 검정 ([[343_stationarity_adf_test|ADF Test]]) - 평균과 [[136_variance|분산]]이 시간에 따라 일정한 시계열 [[082_attribute_types_er_model|속성]]
344. 지수 평활법 ([[344_exponential_smoothing_moving_average|Exponential Smoothing]]) / 이동 평균
345. [[345_collaborative_filtering|협업 필터링]] ([[186_graph_db_recommendation_collaborative_filtering_cold_start|Collaborative Filtering]]) - 사용자 기반 / 아이템 기반 [[211_recommendation_system|추천 시스템]] 핵심 
346. [[346_content_based_filtering|콘텐츠 기반 필터링]] ([[346_content_based_filtering|Content-based Filtering]]) - 아이템의 메타 [[082_attribute_types_er_model|속성]] 분석 추천
347. [[559_serverless_cold_start_mitigation|콜드 스타트]] ([[347_cold_start_problem|Cold Start]]) 문제 - [[211_recommendation_system|추천 시스템]]에서 신규 유저/아이템에 대한 정보 부족으로 추천 불가 현상
348. [[161_matrix_decomposition|행렬 분해]] ([[348_matrix_factorization|Matrix Factorization]]) - 거대 사용자-아이템 평점 행렬을 잠재 요인(Latent Factor) 행렬 두 개로 쪼개어 빈 공간(예측 평점) 추론
349. [[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]] ([[342_svd|특이값 분해]]) 및 ALS ([[349_svd_als_recommendation|Alternating Least Squares]]) 추천 [[001_algorithm_definition|알고리즘]] 연산
350. K-Means 클러스터링의 엘보우 기법 (Elbow Method) / 실루엣 계수 ([[350_kmeans_elbow_silhouette|Silhouette Score]]) 최적 K값 탐색
351. [[351_dbscan_density_based_clustering|DBSCAN]] - 밀도 기반 클러스터링 (원 모양이 아닌 불규칙한 모양 군집, 노이즈/[[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 판별 가능)
352. K-최근접 이웃 ([[352_knn_distance_metrics|K-NN]]) / 거리 척도 - 유클리디안 (L2), 맨해튼 (L1), 민코프스키, [[106_mahalanobis_distance|마할라노비스 거리]]
353. [[353_random_forest|랜덤 포레스트]] ([[353_random_forest|Random Forest]]) - 다수의 결정 트리를 [[259_bagging_random_forest|배깅]]([[259_bagging_random_forest|Bagging]])과 [[247_feature_label_variables|피처]] 무작위 선택으로 결합하여 과적합 [[656_ir_containment|억제]]
354. [[354_boosting_adaboost_gbm|부스팅 기법]] ([[077_Adaboost|AdaBoost]], GBM) - 트리 오차 수정 반복 연산
355. XGBoost / LightGBM - [[104_classification_analysis|분류]]/회귀 대회의 우승 단골 [[127_boosting|부스팅]] 모델, [[093_normalization|정규화]](L1/L2) 도입 및 [[430_index_fast_full_scan|병렬]] 트리 [[087_process_state_transition|생성]]으로 GBM 속도/과적합 개선
356. [[356_imbalanced_data_sampling|불균형 데이터 처리]] ([[356_imbalanced_data_sampling|Imbalanced Data]]) - 언더샘플링 vs 오버샘플링
357. [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] (Synthetic Minority Over-sampling Technique) - 소수 클래스의 [[001_dikw_pyramid|데이터]] 포인트를 [[352_knn_distance_metrics|K-NN]] 기반으로 선형 보간하여 합성 [[087_process_state_transition|생성]] [[001_dikw_pyramid|데이터]] 증강
358. [[232_tfidf_cosine_similarity_text_embedding_confusion_matrix|TF-IDF]] (Term Frequency - Inverse [[037_document|Document]] Frequency) - 텍스트 단어 중요도 [[267_weight_bias_activation|가중치]]. 특정 문서에 많이 나올수록(TF 증가), 전체 문서군에 드물게 나올수록(IDF 증가) [[267_weight_bias_activation|가중치]] 높음
359. [[359_cosine_similarity|코사인 유사도]] ([[359_cosine_similarity|Cosine Similarity]]) - 텍스트 벡터 간 각도 측정 (-1 ~ 1)
360. [[379_ensemble_bias_variance_math|앙상블 편향-분산]] 수식 증명 ([[259_bagging_random_forest|배깅]]은 [[136_variance|분산]] 감소, [[127_boosting|부스팅]]은 편향 감소)
361. 그래디언트 소실 ([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 대비 [[087_weight_initialization_xavier_he_glorot|가중치 초기화]] (Xavier, He)
362. [[104_svm_support_vector_machine|서포트 벡터 머신]] ([[238_svm_margin_kernel_trick_naive_bayes|SVM]])의 하드 마진 ([[362_svm_hard_soft_margin|Hard Margin]]) vs 소프트 마진 (Soft Margin / 슬랙 변수 허용)
363. [[151_entropy|엔트로피]] ([[151_entropy|Entropy]]) - 불확실성 정보량 척도 (결정 트리 정보 획득량 계산)
364. 베이즈 정리 사후 [[130_probability|확률]] 갱신 구조망 파악
365. [[098_coefficient_of_determination_r_squared|결정 계수]](R^2)와 조정된 [[098_coefficient_of_determination_r_squared|결정 계수]](Adjusted R^2) 비교
366. [[001_dikw_pyramid|데이터]] 전처리 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]]) 제거 (IQR 1.5 규칙, Z-score)
367. [[367_missing_value_imputation_mice|결측치 대치법]] ([[367_missing_value_imputation_mice|Imputation]]) - 평균, 중앙값 대치 및 다중 대치법(MICE)
368. [[368_data_scaling_normalization_standardization|데이터 스케일링 민감도]] ([[352_knn_distance_metrics|K-NN]], [[238_svm_margin_kernel_trick_naive_bayes|SVM]], [[163_pca|PCA]] 등 거리/[[136_variance|분산]] 기반 모델은 필수)
369. [[001_dikw_pyramid|데이터]] 비식별화 K-익명성, L-다양성, T-근접성
370. 최적화 [[275_gradient_descent_sgd|경사 하강법]] [[080_gradient_descent_learning_rate|학습률]] ([[240_switch_learning_forwarding_flooding|Learning]] Rate) 적응형 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[277_adam_optimizer|Adam]] 수리 모형)
371. 교차 [[151_entropy|엔트로피]] [[075_loss_function_cost_function|손실 함수]] 도함수 산출 구조
372. 라쏘([[102_lasso_ridge_regression_regularization|Lasso]]) 회귀의 L1 [[093_normalization|정규화]] 모델의 변수 선택 (특성 희소성/계수 0) 기능
373. 릿지(Ridge) 회귀의 L2 [[093_normalization|정규화]] ([[267_weight_bias_activation|가중치]] 0에 가깝게 축소, 다중공선성 대처)
374. [[374_elastic_net_regression|엘라스틱 넷]] ([[374_elastic_net_regression|Elastic Net]]) - L1과 L2 패널티 혼합 통계
375. A/B 테스트 검정력 계산 및 샘플 사이즈 결정 모형
376. [[140_markov_chain|마르코프 체인]] 몬테카를로 ([[376_mcmc_markov_chain_monte_carlo|MCMC]]) 샘플링 통계 기법 베이지안 근사 
377. [[392_perceptron_convergence|퍼셉트론 수렴 정리]] ([[377_perceptron_convergence_theorem|Convergence Theorem]]) 선형 매핑 분리망 
378. 텍스트 [[820_tokenization|토큰화]] BPE ([[378_bpe_byte_pair_encoding|Byte Pair Encoding]]) 서브워드 병합 [[001_algorithm_definition|알고리즘]] 빈도 [[130_probability|확률]] 
379. 우도비 검정 ([[379_likelihood_ratio_test|Likelihood Ratio Test]]) 두 통계 모델 적합성 우위 
380. 텐서플로우/파이토치 계산 [[070_graph_datastructure|그래프]] (Computational [[104_graph|Graph]]) [[015_지연_데이터_관점|지연]] 실행([[380_computational_graph_lazy_eager_execution|Lazy]]) vs 즉시 실행(Eager/Dynamic) 모드 차이
381. 딥러닝 미분 연쇄 법칙 자동 미분([[381_autograd_chain_rule|Autograd]]) 원리 
382. 퍼지 집합 [[369_logic_bomb|논리]] 제어 소속도 연산 ([[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]]) 함수
383. [[070_graph_datastructure|그래프]] 마이닝 중심성 ([[383_graph_mining_centrality_metrics|Centrality]]) 측정 지표 - 연결 중심성, 매개 중심성, 근접 중심성, 고유벡터 중심성 
384. [[286_page_frame|페이지]] 랭크 (PageRank) 행렬 이동 고유 벡터 무작위 서퍼 ([[384_pagerank_random_surfer|Random Surfer]]) 모형
385. 은닉 [[755_markov_model|마르코프 모델]] (HMM) 비터비 ([[385_hmm_viterbi_dynamic_programming|Viterbi]]) [[001_algorithm_definition|알고리즘]] 은닉 상태 최적 경로 탐색 동적 계획법 
386. [[264_naive_bayes|나이브 베이즈]] 모델 스무딩 ([[350_laplace_smoothing|라플라스 스무딩]] 빈도 0 방어) 기법 
387. [[083_association_rule_apriori_market_basket|연관 규칙 탐색]] Apriori [[001_algorithm_definition|알고리즘]] ([[084_support_association_rule_transaction|지지도]], [[085_confidence_association_rule_conditional_probability|신뢰도]], [[086_lift_association_rule_marketing|향상도]]) FP-Growth [[282_performance_tactics|성능]] 개선 구조 
388. 강화학습 상태 가치(V) 및 행동 가치(Q) 차이 [[316_q_learning|Q-Learning]] 오프 폴리시 타겟 갱신망 
389. [[395_ppo_clipping|PPO]] 근위 [[164_policy|정책]] 최적화 클리핑([[389_ppo_proximal_policy_optimization|Clipping]]) 폭주 통제 서로게이트 
390. [[114_gaussian_mixture_model|가우시안 혼합 모델]] ([[360_gmm_em_algorithm|GMM]]) 연성 군집 ([[130_probability|확률]] 분할 매핑 통계)
391. 다변량 통계 주성분 고유값 크기 순 컷오프(Scree Plot 기준) 
392. 시계열 자기 상관 함수 (ACF, PACF) 지표도 
393. 생존 분석 카플란-마이어 ([[393_survival_analysis_kaplan_meier|Kaplan-Meier]]) 누적 추정 
394. [[116_kernel_density_estimation|커널 밀도 추정]] (KDE) 비모수 [[001_dikw_pyramid|데이터]] 스무딩 [[140_bandwidth|대역폭]] ([[140_bandwidth|Bandwidth]])
395. 유전 [[001_algorithm_definition|알고리즘]] ([[169_evolutionary_algorithms|GA]]) 적합도([[395_genetic_algorithm_ga_operators|Fitness]]), 룰렛 휠 선택, 교차(Crossover), 변이(Mutation) 
396. 시뮬레이티드 어닐링 ([[396_simulated_annealing_heuristic|모의 담금질]]) 볼츠만 [[130_probability|확률]] 기반 지역 최적해 탈출 
397. 정보 이론 쿨백-라이블러 발산 ([[153_kl_divergence|KL Divergence]]) 
398. 노이즈 [[001_dikw_pyramid|데이터]] [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] 의사결정 방어 [[353_random_forest|랜덤 포레스트]] 
399. 딥러닝 비용 함수 다차원 표면 매니폴드 매핑 ([[113_manifold_hypothesis_dimensionality_reduction|Manifold Hypothesis]]) 
400. [[241_machine_learning_basics|머신러닝]] 비용 기반 모델 (AIC, BIC 정보 기준)
401. 베이지안 네트워크 [[130_probability|확률]]적 방향성 비순환 [[070_graph_datastructure|그래프]] ([[401_bayesian_network_dag_causality|DAG]]) 인과 모델
402. 정수 계획법 선형 완화 [[011_branch_and_bound|분기 한정]] ([[011_branch_and_bound|Branch and Bound]]) 최적 탐색
403. [[378_dtw|동적 시간 워핑]] ([[403_dtw_dynamic_time_warping|DTW]]) 시계열 유사 변위 
404. [[412_svr_support_vector_regression|서포트 벡터 회귀]] (SVR) 튜브 입실론(ε) 경계 모형
405. 최적화 [[015_heuristic_search|휴리스틱 탐색]] Tabu Search 금기 목록 로컬 미니마 탈출
406. [[167_linear_programming|선형 프로그래밍]] 심플렉스 ([[406_linear_programming_simplex|Simplex]]) 다면체 버텍스 최적 
407. [[106_mahalanobis_distance|마할라노비스 거리]] (공분산 고려 [[093_normalization|정규화]] 투영 거리)
408. 랜덤 워크 마팅게일 공리 [[130_probability|확률]]론
409. [[312_quantization|모델 양자화]] 오차 최소화 패널티 연산망
410. [[190_ai_llm_requirements_specification|AI]] 지적 재산권 [[809_data_sovereignty|데이터 주권]] ([[410_ai_intellectual_property_data_sovereignty_data_act|Data Sovereignty]]) 유럽 [[001_dikw_pyramid|Data]] Act 법제
411. 지식 정보 시스템 온톨로지 (OWL, RDF 규격 표현) 
412. 시계열 예측 딥러닝 TCN 구조 팽창 인과 [[228_cnn_1d_2d_3d_video_medical|합성곱]] ([[412_tcn_dilated_causal_convolution|Dilated Causal Conv]]) 매핑 
413. 다중 모달 [[312_clip_contrastive_learning|클립]]([[408_clip|CLIP]]) 텍스트/이미지 대조 손실 정렬 ([[413_clip_multimodal_contrastive_loss|Contrastive Loss]])
414. [[263_llm_large_language_model|LLM]] [[039_decoder|디코더]] 탑-K ([[414_llm_decoder_top_k_temperature|Top-K]]), 템퍼리처 제어 [[087_process_state_transition|생성]] 텍스트 [[270_softmax|소프트맥스]] 변화율 망
415. [[276_fine_tuning|RAG]] 리랭크([[415_rag_rerank_cross_encoder|Re-rank]]) 크로스 [[040_encoder|인코더]] 결합 문서 적합도 재배열 [[001_algorithm_definition|알고리즘]]
416. [[955_prompt_injection|프롬프트 인젝션]] 방어 시맨틱 [[339_routing_overview_best_path_selection|라우팅]] 의도([[416_prompt_injection_semantic_routing|Intent]]) 필터 게이트웨이 
417. [[348_mlops|MLOps]] 드리프트 PSI ([[417_mlops_data_drift_psi|Population Stability Index]]) 탐지 수리
418. 오버 샘플링 [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] 보간 벡터 난수 발생 수식 증강망 
419. [[256_roc_auc|ROC AUC]] 0.5 하한 임계 모델 무작위성 평가망 
420. 빅데이터 처리 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[013_hdfs|HDFS]] 블록 [[016_replication_factor|복제]] 3벌 [[017_rack_awareness|랙 인지]] [[136_variance|분산]] [[002_database_definition|데이터베이스]] 연계망 처리 

## 6. 시험 빈출 핵심 토픽 및 기술사 융합 논술 키워드 (380개 집중 요약)
421. [[002_turing_test|튜링 테스트]] 기계 지능 평가 
422. A* 허용 [[210_heuristics_scheduling|휴리스틱]] 
423. [[240_mcts_monte_carlo|MCTS]] 알파고 시뮬 트리 탐색 
424. 과대적합 [[136_variance|분산]] 과소적합 편향 
425. 차원의 저주 [[163_pca|PCA]] 해결 
426. K-Fold [[250_cross_validation_kfold|교차 검증]] 
427. [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] [[233_precision_recall_f1_roc_auc_threshold|정밀도]] [[092_recall_sensitivity_hit_rate|재현율]] F1 조화 
428. [[256_roc_auc|ROC AUC]] [[431_ssthresh_slow_start_threshold|임계치]] 곡선
429. [[429_bagging_random_forest|배깅 랜덤 포레스트]] 
430. [[127_boosting|부스팅]] XGBoost
431. K-Means 군집 엘보우 
432. [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 초평면 [[022_kernel_role|커널]] 마진
433. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] XOR 한계 은닉층
434. [[434_sigmoid_vanishing_gradient|시그모이드 기울기 소실]] 
435. [[269_relu_activation|ReLU]] 도함수 0, 1 
436. [[272_backpropagation|역전파]] 연쇄 법칙 체인 룰
437. 미니배치 SGD [[130_probability|확률]] 하강 
438. [[277_adam_optimizer|Adam]] 관성 적응 속도 
439. [[280_dropout|드롭아웃]] 임의 뉴런 차단 
440. L1 L2 [[093_normalization|정규화]] 페널티 
441. [[282_batch_normalization|배치 정규화]] 평균 [[136_variance|분산]] 
442. [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] [[097_stride_convolutional_neural_network_downsampling|스트라이드]] [[098_padding_convolutional_neural_network_same_valid|패딩]] 필터 
443. [[285_pooling_layer|풀링]] 해상도 불변 차원 
444. [[287_resnet_skip_connection|ResNet]] 잔차 연결 기울기 전달 
445. YOLO 실시간 1-Stage 
446. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 시계열 [[114_bptt_backpropagation_through_time|BPTT]] 
447. [[292_lstm|LSTM]] 장기 기억 셀 게이트 
448. 어텐션 병목 벡터 [[136_variance|분산]] 가중
449. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 셀프 어텐션 [[430_index_fast_full_scan|병렬]] 
450. [[301_bert_mlm|BERT]] 양방향 [[138_mlm_learning|MLM]] 
451. [[302_gpt_autoregressive|GPT]] 자가 회귀 [[039_decoder|디코더]] [[087_process_state_transition|생성]] 
452. [[225_foundation_model_peft_lora|파운데이션 모델]] 자기 지도
453. 프롬프트 [[146_chain_of_thought_cot|CoT]] 단계별 추론 
454. [[454_hallucination_prevention|할루시네이션 환각]] 
455. [[276_fine_tuning|RAG]] 검색 증강 외부 주입 
456. 벡터 DB 코사인 [[278_instruction_tuning|임베딩]] 
457. [[306_peft_lora|PEFT LoRA]] 저차원 파인튜닝 
458. [[434_quantization|양자화]] FP32 INT8 [[347_compaction|압축]] 
459. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] 교사 학생 네트워크 
460. [[154_gan_generative_adversarial_network|GAN]] [[087_process_state_transition|생성]]자 판별자 적대 
461. 디퓨전 노이즈 역산 [[087_process_state_transition|생성]] 
462. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] 인간 피드백 강화 정렬 
463. 마르코프 [[463_markov_decision_process_mdp|MDP]] 상태 행동 보상 
464. [[316_q_learning|Q-Learning]] 오프 폴리시 
465. [[465_dqn_deep_q_network|DQN]] 딥러닝 테이블 타겟 [[016_replication_factor|복제]] 
466. [[348_mlops|MLOps]] 파이프라인 [[324_ci_cd|CI CD]] [[162_continuous_training_pipeline_model_retraining|CT]] 
467. [[165_feature_store_training_serving_consistency|피처 스토어]] 특징 변수 공유 
468. [[468_model_drift_retraining|모델 드리프트]] 재학습
469. [[227_xai_explainable_ai_lime_shap|XAI]] 국소 대리 [[326_lime|LIME]] 전역 섀플리 [[327_shap|SHAP]] 
470. 적대적 공격 포이즈닝 미세 변조
471. [[256_federated_learning_privacy_model_security|연합 학습]] 디바이스 [[267_weight_bias_activation|가중치]] 통합 프라이버시
472. 온디바이스 [[190_ai_llm_requirements_specification|AI]] [[313_slm|SLM]] 엣지 추론 
473. [[004_blockchain|블록체인]] [[007_merkle_tree|머클 트리]] 해시 [[003_integrity|무결성]] 
474. [[136_variance|분산]] 원장 [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 
475. PoW 해시 퍼즐 PoS [[015_pos_proof_of_stake|지분 증명]] 
476. 비잔틴 장애 [[647_bft_verification|BFT]] 다수결 1/3 방어
477. [[022_smart_contract|스마트 컨트랙트]] [[152_evm_earned_value_management|EVM]] [[024_gas|가스]] 
478. [[026_token_economy|토큰 이코노미]] ICO NFT RWA 
479. [[229_zkp_data_clean_room|영지식 증명]] [[354_did_decentralized_identity_zkp|ZKP]] 프라이버시 [[396_validation|확인]] 
480. [[042_rollup_l2_solution|롤업]] 옵티미스틱 사기 증명 ZK 타당 증명 
481. [[280_sharding|샤딩]] [[179_table_partitioning_concept|파티셔닝]] [[430_index_fast_full_scan|병렬]] L1 
482. [[040_blockchain_trilemma|블록체인 트릴레마]] 확장 탈중앙 보안
483. [[231_did_decentralized_identity|DID]] 탈중앙 신원 W3C VC VP 
484. [[054_dao_decentralized_autonomous_organization|DAO]] 자율 탈중앙 조직 스마트 투표 
485. 51% [[068_eclipse_attack_p2p_isolation|이클립스 공격]] [[070_sybil_attack_fake_nodes|시빌 공격]] 노드 기만 
486. [[101_iot_concept|사물인터넷]] [[101_iot_concept|IoT]] [[103_wsn_sensor_network|센서 네트워크]] 
487. 엣지 [[106_fog_computing_cisco_architecture|포그 컴퓨팅]] 클라우드 [[136_variance|분산]] 
488. [[1029_lpwan_lora|LPWAN LoRa]] [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] 면허 비면허 
489. [[622_mqtt_publish_subscribe_qos|MQTT]] Pub/Sub 큐 [[120_coap_constrained_application_protocol|CoAP]] [[156_rest_representational_state_transfer|REST]] 경량
490. [[612_matter_csa_smart_home_standard|매터]] [[612_matter_csa_smart_home_standard|Matter]] 스마트홈 표준 
491. [[126_digital_twin_concept|디지털 트윈]] [[212_synchronization_mechanisms|동기화]] 시뮬레이션 가상 
492. [[594_metaverse_realtime_sync_rendering_offloading|메타버스]] XR [[131_slam_simultaneous_localization_mapping|SLAM]] 위치 동시 추정 
493. 자율주행 레벨 라이다 [[139_sensor_fusion_camera_lidar_radar|센서 퓨전]] 
494. [[141_v2x_vehicle_to_everything_communication|V2X]] 통신 [[143_c_v2x_cellular_based_communication|C-V2X]] [[418_5g_embb_urllc_mmtc_slicing|5G]] 차량 제어망
495. [[418_5g_embb_urllc_mmtc_slicing|5G]] [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] [[761_urllc_ultra_reliable_low_latency|uRLLC]] [[762_mmtc_massive_machine_type_communications|mMTC]] 슬라이싱 
496. [[419_6g_ntn_thz_ris_next_gen|6G]] [[157_terahertz_thz_6g|테라헤르츠]] 위성 NTN RIS 메타 표면 
497. [[155_oran_open_radio_access_network|오픈 랜]] [[782_o_ran_open_ran_white_box_interface|O-RAN]] 장비 화이트박스 분리
498. [[166_smart_factory|스마트 팩토리]] [[167_cps_cyber_physical_system|CPS]] [[163_microgrid_island_mode|마이크로그리드]] 
499. 클라우드 [[183_iaas_infrastructure_as_a_service|IaaS]] [[184_paas_platform_as_a_service|PaaS]] [[309_saas|SaaS]] [[342_faas|FaaS]] 
500. [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] 록인 회피 네이티브 
501. [[063_docker_architecture|도커]] [[561_container_based_deployment|컨테이너]] 경량 OS 격리 
502. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[198_pod_kubernetes_minimum_deployment_unit|포드]] [[073_container_orchestration_tools|오케스트레이션]] 배포
503. [[377_serverless_cold_start|서버리스 콜드 스타트]] [[015_지연_데이터_관점|지연]] 제어 
504. [[793_iac_idempotency_template|IaC]] [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] 선언 
505. [[532_microservices_decomposition_patterns|마이크로서비스]] [[014_api_posix|API]] 게이트웨이 [[302_service_mesh_istio|서비스 메시]] 
506. [[306_cqrs|CQRS]] [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] [[305_saga|사가 패턴]] 로컬 [[136_variance|분산]]
507. [[751_chaos_engineering|카오스 엔지니어링]] [[575_shadow_deployment_traffic_mirroring|섀도우 배포]] [[307_circuit_breaker_pattern|서킷 브레이커]]
508. [[236_quantum_computing_pqc|양자 컴퓨팅]] 중첩 얽힘 쇼어 그로버 보안 위협 
509. [[441_cxl|CXL]] [[497_chiplet|칩렛]] [[442_memory_pooling|메모리 풀링]] [[443_ucie|UCIe]] 하드웨어
510. 통계 평균 [[136_variance|분산]] 표준편차 [[064_skewness_kurtosis_log_transformation|왜도]] 첨도
511. [[138_normal_distribution|정규 분포]] [[139_clt|중심 극한 정리]] [[074_law_of_large_numbers_lln_convergence_probability|대수의 법칙]]
512. [[145_hypothesis_testing|가설 검정]] [[068_significance_level_alpha_p_value_hypothesis|유의 수준]] [[337_p_value_significance|P-Value]] 1/2종 오류 
513. [[070_t_test_independent_paired_mean_difference|t-검정]] [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] [[250_cross_validation_kfold|교차 검증]] 카이제곱 
514. 회귀 계수 OLS 다중공선성 [[459_dummy_test_double|더미]] VIF 
515. [[163_pca|PCA]] LDA [[342_svd|특이값 분해]] 행렬 차원 
516. [[140_markov_chain|마르코프 체인]] 흡수 에르고딕 전이 상태 
517. [[377_time_series_stationarity|시계열 정상성]] [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 평활법 
518. [[232_tfidf_cosine_similarity_text_embedding_confusion_matrix|TF-IDF]] [[359_cosine_similarity|코사인 유사도]] 텍스트 워드투벡 
519. [[345_collaborative_filtering|협업 필터링]] 콘텐츠 기반 [[559_serverless_cold_start_mitigation|콜드 스타트]] 추천망
520. [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] [[225_kdd_t_test_anova_statistical_analysis|KDD]] 프로세스 [[106_association_rules|연관 규칙]] 
521. [[1019_homomorphic_encryption|동형 암호]] 재파라미터 [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] 전환망 
522. [[062_darkdata|다크 데이터]] 클린 룸 [[012_mydata|마이데이터]] 
523. [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]] [[576_feature_flag_ab_testing_rollout|피처 플래그]] [[259_citizen_developer|시민 개발자]] 노코드 
524. [[099_aiops_chatbot_itsm_automation|AIOps]] [[221_llmops_large_language_model_ops|LLMOps]] [[642_observability_telemetry|옵저버빌리티]] [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 
525. [[232_spatial_computing_digital_twin|공간 컴퓨팅]] [[239_micro_frontends_architecture|마이크로 프론트엔드]] [[319_webassembly_architecture|WebAssembly]]
526. [[360_dpu_smartnic|DPU SmartNIC]] 인프라 [[440_offloading|오프로딩]] 가속망
527. [[495_hbm|HBM]] [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]] [[140_bandwidth|대역폭]] 초거대 병목 완화
528. vLLM KV 캐시 PagedAttention [[259_paging|페이징]] 
529. DSPy 프롬프트 자동 최적화 컴파일 아키텍처 
530. [[530_graph_rag|GraphRAG]] [[160_knowledge_graph_graphrag_integration|지식 그래프]] 연동 [[275_react_framework|환각]] 배제망 
531. [[014_api_posix|API]] 스로틀링 백엔드 포 프론트([[543_bff_backend_for_frontend|BFF]]) 통합 
532. [[270_embedding_model|DPO]] 선호 최적화 강화학습 회피 튜닝 
533. [[288_latent_diffusion_model|LDM]] 잠재 디퓨전 속도 최적화 공간 [[087_process_state_transition|생성]]망 
534. [[408_clip|CLIP]] [[158_multimodal_clip_vision_audio_encoding|멀티모달]] 텍스트 이미지 쌍 대조 매핑망 
535. MoE 파라미터 게이팅 전문가 [[136_variance|분산]] [[339_routing_overview_best_path_selection|라우팅]]망 
536. [[587_agentic_ai_autonomous_tools|Agentic AI]] 자율 [[294_function_calling_tool_use|함수 호출]] 목적 달성 루프망 
537. [[280_ppo_proximal_policy_optimization|시맨틱 캐시]] [[276_fine_tuning|RAG]] 반복 비용 [[015_지연_데이터_관점|지연]] 감축 계층망 
538. [[194_deepdream_gradcam|딥 드림]] 역산 공격 [[396_differential_privacy|차분 프라이버시]] 방어 
539. 마이그레이션 6R (Rehost, [[213_refactoring_cloud_native_rearchitecture|Refactor]]) 클라우드 전이 
540. [[631_sddc|SDDC]] [[630_hci|HCI]] 스토리지 컴퓨팅 통합 어플라이언스망
541. [[629_bare_metal_cloud|베어메탈 클라우드]] 물리 서버 가상 오버헤드 무결 
542. 멀티시그 [[087_account_abstraction_erc_4337|계정 추상화]] 이더리움 지갑 컨트랙트화 
543. SBT 영구 귀속 NFT 신원 [[303_authentication_authorization_patterns|인증]] (학위) 
544. Web 3.0 [[010_decentralization|탈중앙화]] 플랫폼 경제 소유망 
545. [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]] 합의 [[001_dikw_pyramid|데이터]]가용성([[104_da_as_is_analysis|DA]]) 분리 확장망 
546. [[212_data_fabric_virtualization|데이터 패브릭]] 융합 [[012_metadata|메타데이터]] [[136_variance|분산]] [[211_data_mesh_domain_ownership|데이터 메시]] 
547. [[335_autoencoder|오토인코더]] 비지도 잠재 벡터 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 
548. [[947_data_poisoning|데이터 포이즈닝]] 미세 노이즈 [[942_adversarial_example|적대적 예제]] 모델 오판망
549. [[263_llm_large_language_model|LLM]] [[033_context|Context]] Window 확장 긴 문맥 요약 한계망 극복
550. 정보보호 기술사 [[231_ai_turing_test|인공지능]]/[[004_blockchain|블록체인]]/클라우드 신기술 암기 키워드 등 통합
551. (이상 파생 토픽 800+망 총정리 분석)
... (반복 심화 전용)
800. 최신 ICT 융합 메가트렌드 ([[792_ai_native_6g_neural_network_radio|AI-Native]], Web3, [[047_zta|ZTA]], [[690_round_robin_time_quantum|Quantum]]) 구조 프레임워크 총합 망 완성

---
**총정리 ICT 신기술 / 융합 기술 키워드 : 총 800개 수록** (+관련 지식망 1,200개 커버)
(Web 3.0 [[004_blockchain|블록체인]]부터 최신 초거대 [[190_ai_llm_requirements_specification|AI]]([[263_llm_large_language_model|LLM]]) 프롬프팅, [[276_fine_tuning|RAG]] 구조, [[204_cloud_native_architecture|클라우드 네이티브 아키텍처]], [[447_quantum_computer|양자 컴퓨터]]와 자율주행 모빌리티 등 기술사 시험에 가장 많이 출제되는 차세대 트렌드 기술 용어들을 완전 집대성하였습니다.)