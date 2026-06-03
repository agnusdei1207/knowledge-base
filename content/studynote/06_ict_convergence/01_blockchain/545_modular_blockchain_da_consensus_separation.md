+++
title = "545. 모듈러 블록체인과 데이터 가용성 계층 (Modular Blockchain and Data Availability Layer)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)([Modular Blockchain](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/))은 실행(Execution)·합의(Consensus)·정산(Settlement)·[데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 계층을 분리하여 각 계층이 전문화로 트릴레마를 <strong>계층별 최적화</strong>로 우회하는 아키텍처다.
> 2. **가치**: Celestia([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 전문), EigenLayer(재스테이킹, 보안 임대), Danksharding(이더리움 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 확장)이 모듈러 생태계의 핵심 인프라로, [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)과 결합하여 이더리움 확장성 로드맵을 실현한다.
> 3. **판단 포인트**: 모놀리식(Monolithic) [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 모든 계층을 하나의 체인이 처리하여 트릴레마에 구속되지만, [모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)은 <strong>계층 분리로 트릴레마를 계층별 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong>하여 전체 시스템 성능을 극대화한다.

---

## Ⅰ. 개요 및 필요성

### 모놀리식 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 한계

비트코인·[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 이더리움은 단일 체인이 모든 역할(실행+합의+정산+[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))을 담당하는 모놀리식 구조다. 이는 트릴레마(확장성·[탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/)·보안 동시 불가)에 구속된다.

[모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)은 이를 <strong>소프트웨어 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/">마이크로서비스 아키텍처</a></strong>처럼 계층 분리하여 각 계층이 하나의 역할만 전문화한다.

- **📢 섹션 요약 비유**: — "모놀리식 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 요리·서빙·계산을 한 사람이 하는 레스토랑, 모듈러는 주방장·웨이터·계산원이 전문 분업하는 레스토랑이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/) 4계층 구조

```
┌────────────────────────────────────────────────────────┐
│              모듈러 블록체인 계층 구조                   │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │  실행 계층 (Execution Layer)                     │  │
│  │  스마트 컨트랙트 실행, 상태 전이                  │  │
│  │  예: Rollup (Arbitrum, zkSync), Sovereign Rollup│  │
│  └─────────────────────────────────────────────────┘  │
│                        │                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │  정산 계층 (Settlement Layer)                    │  │
│  │  실행 결과 최종 확정, Fraud/Validity Proof 검증  │  │
│  │  예: Ethereum L1                                │  │
│  └─────────────────────────────────────────────────┘  │
│                        │                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │  합의 계층 (Consensus Layer)                     │  │
│  │  트랜잭션 순서 합의, 체인 선택 규칙               │  │
│  │  예: Ethereum Beacon Chain, Tendermint           │  │
│  └─────────────────────────────────────────────────┘  │
│                        │                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │  데이터 가용성 계층 (DA Layer)                   │  │
│  │  트랜잭션 데이터 공개·가용성 보장                 │  │
│  │  예: Celestia, EIP-4844 Blob, Avail             │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### 핵심 모듈러 프로젝트 비교

| 프로젝트 | 전문 계층 | 핵심 기술 | 특징 |
|:---|:---|:---|:---|
| **Celestia** | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 전문 | [DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/)([데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 샘플링) | 실행·합의 없음, [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 전용 |
| **EigenLayer** | 보안 임대 | 재스테이킹(Restaking) | [ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/) 보안을 다른 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에 임대 |
| **Avail** | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) | KZG [다항식](/knowledge-base/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) 커밋 | [Polygon](/knowledge-base/studynote/06_ict_convergence/01_blockchain/045_sidechain_bridge_polygon/) 분사 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 레이어 |
| **Ethereum** | 합의+정산+[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) | Danksharding | L2 생태계 기반 정산 레이어 |

- **📢 섹션 요약 비유**: — "Celestia는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 클라우드 스토리지 — '실행은 니들이 해, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보관은 내가 전담할게'라고 역할을 나눈 것이다.

---

## Ⅲ. 비교 및 연결

### 모놀리식 vs 모듈러 비교

| 항목 | 모놀리식 | 모듈러 |
|:---|:---|:---|
| **단일 체인 역할** | 실행+합의+정산+[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 모두 | 한 역할만 전담 |
| **TPS** | 낮음 (단일 병목) | 높음 (계층 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/">탈중앙화</a></strong> | 전체 트레이드오프 | 계층별 최적화 |
| **유연성** | 낮음 | 높음 (조합 가능) |
| **복잡도** | 낮음 | 높음 (계층 간 통신) |
| **대표** | Bitcoin, Solana | 이더리움 L2 생태계 |

### EigenLayer 재스테이킹(Restaking) 메커니즘

```
ETH 스테이커 (32 ETH)
    │ 이더리움 보안 확보
    ▼
EigenLayer에 재스테이킹 등록
    │ 동일 ETH로 추가 보안 서비스 제공
    ▼
AVS (Actively Validated Service)
    ├ 오라클 네트워크 (Chainlink 대안)
    ├ 브릿지 보안
    └ DA 레이어 보안 (EigenDA)
    │ 추가 보상(수수료) 수령
    ▼
슬래싱 위험: 두 프로토콜 동시 위반 시
```

- **📢 섹션 요약 비유**: — "재스테이킹은 은행 직원이 은행 업무(이더리움 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) 외에 보험사 파트타임(다른 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 보안)도 하는 것 — 수익 두 배지만 책임도 두 배.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)) 문제 이해

[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 문제: 블록 생산자가 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 공개하지 않아도 블록 헤더만 공개 시 다른 노드가 내용 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 불가 → 사기 증명(Fraud Proof) 불가 → 보안 붕괴

[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 해결책:
1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/">DAS</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a> <a href="/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/">Sampling</a>)</strong>: 무작위 샘플 조회로 전체 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
2. <strong>KZG <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/">다항식</a> 커밋</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 일부 없어도 나머지로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능 증명
3. <strong>이레이저 코딩(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/">Erasure Coding</a>)</strong>: 원본 2배 확장 저장 → 50%만 있어도 복원

### 기술사 핵심 판단
1. <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/">롤업</a> + <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">DA</a> 레이어 선택</strong>: zkSync → 이더리움 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) / Celestia [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 선택 가능
2. <strong>EigenLayer <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong>: 재스테이킹 집중화 → 단일 슬래싱 이벤트가 다수 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 동시 위협
3. **Danksharding 완성 시**: 이더리움이 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 레이어 전문화 → Celestia와 경쟁 구도
4. **계층 간 통신**: 크로스 레이어 메시지 패싱([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 보안 취약점 주의

- **📢 섹션 요약 비유**: — "[모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)은 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 전환 — 빠르고 유연해지지만, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 실패 가능성도 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **확장성 극복** | 각 계층 독립 최적화로 TPS 수십 배 향상 |
| **보안 재활용** | 이더리움 보안(EigenLayer)을 신규 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에 임대 |
| **개발 유연성** | 앱체인(App-chain)이 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)·정산 레이어 선택 가능 |
| **트릴레마 우회** | 계층 분리로 [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/) 실질적 해소 |

[모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)은 [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/) 해결의 가장 유망한 설계 패러다임이다. 이더리움 L2 생태계([롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)+Danksharding+EigenLayer)는 모듈러 아키텍처의 가장 성숙한 구현체이며, 향후 Web3 인프라의 표준 아키텍처로 자리잡을 가능성이 높다.

- **📢 섹션 요약 비유**: — "인터넷이 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)(응용)·[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)(전송)·IP(네트워크) 계층으로 분리되어 발전했듯, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)도 계층 분리로 새로운 발전 단계에 진입하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) | [모듈러 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/095_modular_blockchain_execution_da_consensus/)의 실행 계층 |
| Celestia | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 전문 모듈러 레이어 |
| EigenLayer | 보안 임대 모듈러 레이어 |
| [DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/) | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 계층의 핵심 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [모듈러 블록체인과 데이터 가용성 계층] → [DA 계층의 핵심 기술]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 모놀리식 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 한 명이 요리·서빙·계산을 다 하는 것, 모듈러는 전문가가 각자 역할을 나누는 것이에요.
2. Celestia는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보관만 잘하는 전문 창고, 이더리움은 최종 결정만 내리는 판사, [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)은 실제로 계산하는 계산원이에요.
3. 이렇게 역할을 나누면 각자가 더 빠르고 싸게 일할 수 있어서 전체 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)이 훨씬 강해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 545 / 552

← **이전**: [544. Web 3.0 탈중앙화 플랫폼 경제 (Web 3.0 Decentralized Platform Economy)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/544_web3_decentralized_platform_economy/)
**다음**: [546. 데이터 패브릭과 분산 데이터 메시 (Data Fabric and Distributed Data Mesh)](/knowledge-base/studynote/06_ict_convergence/05_data_science/546_data_fabric_distributed_data_mesh/) →

---
