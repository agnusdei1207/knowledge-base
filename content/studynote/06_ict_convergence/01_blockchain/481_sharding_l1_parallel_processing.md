+++
title = "481. 샤딩과 L1 병렬 처리 (Sharding and L1 Parallel Transaction Processing)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)([Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))은 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) L1 네트워크를 여러 샤드(Shard, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))로 분할하여 각 샤드가 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 처리함으로써 <strong>TPS를 선형 확장</strong>하는 기술이다.
> 2. **가치**: 이더리움 2.0의 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 계획은 실행 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 대신 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a>(Danksharding)</strong>으로 방향을 전환하여, [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)을 위한 저렴한 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 계층([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) Layer) 역할을 담당한다.
> 3. **판단 포인트**: 크로스-샤드 통신(Cross-Shard Communication)과 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 샘플링([DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))이 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)의 핵심 기술 과제이며, 이를 해결해야 진정한 L1 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 확장성이 달성된다.

---

## Ⅰ. 개요 및 필요성

### 단일 체인의 확장성 한계

이더리움 모든 노드가 모든 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 처리하면 → 네트워크 최대 TPS = 개별 노드 TPS. 노드 수를 늘려도 TPS는 증가하지 않는다. [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 이 병목을 깨는 <strong><a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/">수평 분할</a>(Horizontal <a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">Partitioning</a>)</strong> [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

<strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a> vs <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a></strong>: DB [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 중앙화 조율자가 있지만, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 상태에서 크로스-샤드 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/))을 보장해야 하는 더 어려운 문제다.

- **📢 섹션 요약 비유**: — "모든 손님을 한 계산대에서 처리하는 대신, 계산대를 10개로 늘려 줄을 10배 빠르게 처리하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 이더리움 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 아키텍처

```
┌─────────────────────────────────────────────────────┐
│          이더리움 2.0 샤딩 구조                      │
│                                                     │
│          비콘 체인(Beacon Chain)                     │
│          ├ 검증자 등록·관리                          │
│          ├ 샤드 위원회(Shard Committee) 무작위 배정  │
│          └ 크로스링크(Crosslink) 조율                │
│                 │                                   │
│    ┌────────────┼────────────┐                      │
│    ▼            ▼            ▼                      │
│  샤드 0       샤드 1       샤드 N                    │
│  (Shard)      (Shard)      (Shard)                  │
│  병렬 처리    병렬 처리    병렬 처리                  │
└─────────────────────────────────────────────────────┘
```

### Danksharding / Proto-Danksharding 로드맵

| 단계 | 이름 | 내용 | 상태 |
|:---|:---|:---|:---:|
| **EIP-4844** | Proto-Danksharding | Blob [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 도입, [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비용 90% 절감 | ✅ 완료(2024) |
| **Full Danksharding** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) | 64개 Blob/블록, [DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/) 활성화 | 🔄 개발 중 |
| <strong>실행 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a></strong> | 폐기 | [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)으로 대체됨 | ❌ 폐기 |

### [DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)) 원리

```
완전 다운로드 없이 데이터 가용성 검증:
1. 데이터를 이레이저 코딩(Erasure Coding)으로 2배 확장
2. 경량 노드: 무작위 위치의 샘플 K개만 다운로드
3. K개 정상 수신 → 97%+ 확률로 전체 데이터 가용 판단
4. K ≈ 30 수준에서 충분한 신뢰도 달성
```

- **📢 섹션 요약 비유**: — "1만 쪽 책 전체를 읽지 않고 무작위 30쪽만 읽어도 '책이 멀쩡하다'를 통계적으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 방법이다.

---

## Ⅲ. 비교 및 연결

### L1 확장 방식 비교

| 방식 | 메커니즘 | TPS 향상 | [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) | 구현 난이도 |
|:---|:---|:---:|:---:|:---:|
| **블록 크기 증가** | 단순 파라미터 변경 | 낮음 | 하락 | 낮음 |
| **블록 시간 감소** | 합의 속도 향상 | 중간 | 보통 | 중간 |
| <strong>실행 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a></strong> | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 | 높음 | 유지 | 매우 높음 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a></strong> | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 계층 확장 | 간접 | 유지 | 높음 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/">롤업</a> + <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/">DAS</a></strong> | L2 실행 + L1 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) | 매우 높음 | 유지 | 중간 |

### Solana L1 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 방식 (Sealevel)

[샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)과 다른 접근: 단일 체인 내에서 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 의존성 [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) → 의존성 없는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 → 이론적 TPS 65,000+. 그러나 단일 체인이므로 [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 희생.

- **📢 섹션 요약 비유**: — "이더리움 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 도로를 여러 갈래로 나누는 것, Solana는 한 도로에서 차들이 서로 안 부딪히는 선에서 동시에 달리는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 크로스-샤드 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 문제

샤드 A → 샤드 B로 자산 이동 시 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 보장 필요:
- <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/249_two_phase_commit_2pc_distributed/">2단계 커밋</a>(<a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/">2PC</a>)</strong>: 잠금 → [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) → 커밋, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생
- **영수증 기반 비동기**: 샤드 A 소각 증명 → 샤드 B 민팅, 복잡도 증가

### 기술사 핵심 판단
1. <strong>왜 이더리움이 실행 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a>을 포기했나?</strong>: 크로스-샤드 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 해결 복잡도 + [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 생태계가 실행 계층을 대체
2. **Danksharding의 의의**: L1은 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 전문화, L2는 실행 전문화 → 모듈러 아키텍처 완성
3. **EIP-4844 효과**: [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비용 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 절감 실현 (2024년 실측)
4. **DAS와 경량 노드**: 스마트폰도 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 참여 가능 → [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 확장

- **📢 섹션 요약 비유**: — "실행 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 '모든 계산대에서 직접 계산', 현재 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 '계산은 지점에서, 본점은 영수증만 보관'으로 더 효율적이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **TPS 확장** | 샤드 N개 × 단일 샤드 TPS (이론적 선형 확장) |
| **비용 절감** | EIP-4844 Blob으로 L2 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비용 대폭 감소 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/">탈중앙화</a> 유지</strong> | DAS로 경량 노드도 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 참여 |
| **L2 시너지** | [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 계층 강화 → [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 동시 향상 |

[샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/) 중 확장성을 공략하는 L1 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 이더리움은 실행 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 대신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)(Danksharding)으로 방향을 전환해 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 중심 생태계를 지원하는 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 계층으로 진화하고 있다.

- **📢 섹션 요약 비유**: — "[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 고속도로를 실제로 넓히는 공사([샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/))와, 고속도로 옆 지름길([롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)) — 이더리움은 두 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 조합해 병목 없는 Web3를 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| 비콘 체인 | [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 조율 및 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자 관리 |
| EIP-4844 | Proto-Danksharding, Blob 도입 |
| [DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/) | [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 경량화 기법 |
| [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) | [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)과 결합한 이더리움 확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] → [샤딩과 L1 병렬 처리] → [샤딩과 결합한 이더리움 확장 전략]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 한 계산대에 줄이 너무 길면 계산대를 여러 개로 늘리는 것처럼, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)도 여러 조각으로 나눠서 동시에 처리해요.
2. 이더리움은 복잡한 계산은 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)에게 맡기고, 자기는 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보관'만 전문적으로 하기로 했어요.
3. 덕분에 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)이 완성되면 이더리움이 아주 빠르고 저렴한 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)이 될 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 481 / 552

← **이전**: [480. 롤업: 옵티미스틱과 ZK 사기/타당성 증명 (Rollup: Optimistic vs ZK Fraud/Validity Proof)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/480_rollup_optimistic_zk_fraud_validity_proof/)
**다음**: [482. 블록체인 트릴레마: 확장성-탈중앙화-보안 (Blockchain Trilemma)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/482_blockchain_trilemma_scalability_decentralization_security/) →

---
