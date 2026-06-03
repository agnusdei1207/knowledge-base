---
title: 545. 모듈러 블록체인과 데이터 가용성 계층 (Modular Blockchain and Data Availability Layer)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]([[095_modular_blockchain_execution_da_consensus|Modular Blockchain]])은 실행(Execution)·합의(Consensus)·정산(Settlement)·[[094_data_availability_da_layer_celestia|데이터 가용성]]([[104_da_as_is_analysis|DA]], [[001_dikw_pyramid|Data]] [[452_availability|Availability]]) 계층을 분리하여 각 계층이 전문화로 트릴레마를 **계층별 최적화**로 우회하는 아키텍처다.
> 2. **가치**: Celestia([[104_da_as_is_analysis|DA]] 전문), EigenLayer(재스테이킹, 보안 임대), Danksharding(이더리움 [[104_da_as_is_analysis|DA]] 확장)이 모듈러 생태계의 핵심 인프라로, [[042_rollup_l2_solution|롤업]]과 결합하여 이더리움 확장성 로드맵을 실현한다.
> 3. **판단 포인트**: 모놀리식(Monolithic) [[004_blockchain|블록체인]]은 모든 계층을 하나의 체인이 처리하여 트릴레마에 구속되지만, [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]은 **계층 분리로 트릴레마를 계층별 [[136_variance|분산]]**하여 전체 시스템 성능을 극대화한다.

---

## Ⅰ. 개요 및 필요성

### 모놀리식 [[004_blockchain|블록체인]]의 한계

비트코인·[[459_quic_fec_forward_error_correction|초기]] 이더리움은 단일 체인이 모든 역할(실행+합의+정산+[[104_da_as_is_analysis|DA]])을 담당하는 모놀리식 구조다. 이는 트릴레마(확장성·[[010_decentralization|탈중앙화]]·보안 동시 불가)에 구속된다.

[[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]은 이를 **소프트웨어 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]**처럼 계층 분리하여 각 계층이 하나의 역할만 전문화한다.

- **📢 섹션 요약 비유**: — "모놀리식 [[004_blockchain|블록체인]]은 요리·서빙·계산을 한 사람이 하는 레스토랑, 모듈러는 주방장·웨이터·계산원이 전문 분업하는 레스토랑이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]] 4계층 구조

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
| **Celestia** | [[104_da_as_is_analysis|DA]] 전문 | [[339_das|DAS]]([[094_data_availability_da_layer_celestia|데이터 가용성]] 샘플링) | 실행·합의 없음, [[104_da_as_is_analysis|DA]] 전용 |
| **EigenLayer** | 보안 임대 | 재스테이킹(Restaking) | [[118_eth|ETH]] 보안을 다른 [[295_protocol_field_tcp_udp_icmp|프로토콜]]에 임대 |
| **Avail** | [[104_da_as_is_analysis|DA]] | KZG [[195_polynomial_generator_crc|다항식]] 커밋 | [[045_sidechain_bridge_polygon|Polygon]] 분사 [[104_da_as_is_analysis|DA]] 레이어 |
| **Ethereum** | 합의+정산+[[104_da_as_is_analysis|DA]] | Danksharding | L2 생태계 기반 정산 레이어 |

- **📢 섹션 요약 비유**: — "Celestia는 [[004_blockchain|블록체인]]의 클라우드 스토리지 — '실행은 니들이 해, [[001_dikw_pyramid|데이터]] 보관은 내가 전담할게'라고 역할을 나눈 것이다.

---

## Ⅲ. 비교 및 연결

### 모놀리식 vs 모듈러 비교

| 항목 | 모놀리식 | 모듈러 |
|:---|:---|:---|
| **단일 체인 역할** | 실행+합의+정산+[[104_da_as_is_analysis|DA]] 모두 | 한 역할만 전담 |
| **TPS** | 낮음 (단일 병목) | 높음 (계층 [[430_index_fast_full_scan|병렬]]) |
| **[[010_decentralization|탈중앙화]]** | 전체 트레이드오프 | 계층별 최적화 |
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

- **📢 섹션 요약 비유**: — "재스테이킹은 은행 직원이 은행 업무(이더리움 [[395_verification_process_review|검증]]) 외에 보험사 파트타임(다른 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 보안)도 하는 것 — 수익 두 배지만 책임도 두 배.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[094_data_availability_da_layer_celestia|데이터 가용성]]([[104_da_as_is_analysis|DA]]) 문제 이해

[[104_da_as_is_analysis|DA]] 문제: 블록 생산자가 [[191_transaction_concept_states|트랜잭션]] [[001_dikw_pyramid|데이터]]를 공개하지 않아도 블록 헤더만 공개 시 다른 노드가 내용 [[396_validation|확인]] 불가 → 사기 증명(Fraud Proof) 불가 → 보안 붕괴

[[104_da_as_is_analysis|DA]] 해결책:
1. **[[339_das|DAS]]([[001_dikw_pyramid|Data]] [[452_availability|Availability]] [[056_표본화_Sampling|Sampling]])**: 무작위 샘플 조회로 전체 [[452_availability|가용성]] [[395_verification_process_review|검증]]
2. **KZG [[195_polynomial_generator_crc|다항식]] 커밋**: [[001_dikw_pyramid|데이터]] 일부 없어도 나머지로 [[658_ir_recovery|복구]] 가능 증명
3. **이레이저 코딩([[681_erasure_coding|Erasure Coding]])**: 원본 2배 확장 저장 → 50%만 있어도 복원

### 기술사 핵심 판단
1. **[[042_rollup_l2_solution|롤업]] + [[104_da_as_is_analysis|DA]] 레이어 선택**: zkSync → 이더리움 [[104_da_as_is_analysis|DA]] / Celestia [[104_da_as_is_analysis|DA]] 선택 가능
2. **EigenLayer [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]**: 재스테이킹 집중화 → 단일 슬래싱 이벤트가 다수 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 동시 위협
3. **Danksharding 완성 시**: 이더리움이 [[104_da_as_is_analysis|DA]] 레이어 전문화 → Celestia와 경쟁 구도
4. **계층 간 통신**: 크로스 레이어 메시지 패싱([[119_message_passing|Message Passing]]) 보안 취약점 주의

- **📢 섹션 요약 비유**: — "[[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]은 [[532_microservices_decomposition_patterns|마이크로서비스]] 전환 — 빠르고 유연해지지만, [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신([[014_api_posix|API]]) 실패 가능성도 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **확장성 극복** | 각 계층 독립 최적화로 TPS 수십 배 향상 |
| **보안 재활용** | 이더리움 보안(EigenLayer)을 신규 [[295_protocol_field_tcp_udp_icmp|프로토콜]]에 임대 |
| **개발 유연성** | 앱체인(App-chain)이 [[104_da_as_is_analysis|DA]]·정산 레이어 선택 가능 |
| **트릴레마 우회** | 계층 분리로 [[040_blockchain_trilemma|블록체인 트릴레마]] 실질적 해소 |

[[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]은 [[040_blockchain_trilemma|블록체인 트릴레마]] 해결의 가장 유망한 설계 패러다임이다. 이더리움 L2 생태계([[042_rollup_l2_solution|롤업]]+Danksharding+EigenLayer)는 모듈러 아키텍처의 가장 성숙한 구현체이며, 향후 Web3 인프라의 표준 아키텍처로 자리잡을 가능성이 높다.

- **📢 섹션 요약 비유**: — "인터넷이 [[461_http_stateless_connection_oriented|HTTP]](응용)·[[405_tcp_transmission_control_protocol_connection_oriented|TCP]](전송)·IP(네트워크) 계층으로 분리되어 발전했듯, [[004_blockchain|블록체인]]도 계층 분리로 새로운 발전 단계에 진입하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [[083_relationship_in_er_model|관계]] 설명 |
| [[042_rollup_l2_solution|롤업]] | [[095_modular_blockchain_execution_da_consensus|모듈러 블록체인]]의 실행 계층 |
| Celestia | [[104_da_as_is_analysis|DA]] 전문 모듈러 레이어 |
| EigenLayer | 보안 임대 모듈러 레이어 |
| [[339_das|DAS]] | [[104_da_as_is_analysis|DA]] 계층의 핵심 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [모듈러 블록체인과 데이터 가용성 계층] → [DA 계층의 핵심 기술]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 모놀리식 [[004_blockchain|블록체인]]은 한 명이 요리·서빙·계산을 다 하는 것, 모듈러는 전문가가 각자 역할을 나누는 것이에요.
2. Celestia는 [[001_dikw_pyramid|데이터]] 보관만 잘하는 전문 창고, 이더리움은 최종 결정만 내리는 판사, [[042_rollup_l2_solution|롤업]]은 실제로 계산하는 계산원이에요.
3. 이렇게 역할을 나누면 각자가 더 빠르고 싸게 일할 수 있어서 전체 [[004_blockchain|블록체인]]이 훨씬 강해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 545 / 552

← **이전**: [[544_web3_decentralized_platform_economy|544. Web 3.0 탈중앙화 플랫폼 경제 (Web 3.0 Decentralized Platform Economy)]]
**다음**: [[546_data_fabric_distributed_data_mesh|546. 데이터 패브릭과 분산 데이터 메시 (Data Fabric and Distributed Data Mesh)]] →

---
