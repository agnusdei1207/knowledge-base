+++
title = "159. 결과적 일관성 (Eventual Consistency)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))이란 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 즉각적인 강일관성(Strong [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 대신 "충분한 시간이 흐르면 모든 노드의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 일치하게 된다"는 사상으로, [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 이론의 A([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))와 P([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 내성) 선택 시 C([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))를 완화한 결과다.
> 2. **가치**: [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 없이도 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하면서 최종적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성을 보장하므로, [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경의 비동기 이벤트 기반 아키텍처와 완벽하게 부합한다.
> 3. **판단 포인트**: 잠시 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보여줘도 비즈니스 영향이 없는(SNS 좋아요 수 등) 시스템은 Eventual Consistency가 최선이나, 금융 이체처럼 순간적으로도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 틀려서는 안 되는 경우에는 여전히 강일관성 또는 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))가 필요하다.

---

## Ⅰ. 개요 및 필요성

단일 RDBMS (Relational [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System)에서는 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 즉각적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장한다. 그러나 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 독립된 DB를 소유하면, 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 걸친 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 원자적으로 처리하기 위한 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 저하를 초래한다.

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) ([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 이론은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(P) 상황에서 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(C)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A)을 동시에 완벽하게 만족할 수 없다고 말한다. 대부분의 인터넷 규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 A와 P를 선택하고 C를 완화—즉 "결국에는 일치한다"는 [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)을 채택한다.

BASE (Basically Available, Soft [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/), [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 모델은 이 철학을 정식화한 것으로, ACID의 대안으로 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계의 근간이 된다.

📢 **섹션 요약 비유**: [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)은 소문 전파 — 어제 일어난 일이 모든 마을 사람에게 퍼지려면 시간이 필요하지만, 결국에는 모두가 같은 이야기를 알게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | ACID (강일관성) | BASE ([결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) |
|:---|:---|:---|
| [Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) / Basically Available | 모두 성공 또는 전체 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 기본 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지, 부분 실패 허용 |
| [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) / Soft [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 후 즉시 일관 | 일시적으로 불일치 상태 허용 |
| [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) / Eventual | 다른 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 간섭 없음 | 결국 일관 상태에 도달 |
| [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) | 커밋 후 영구 저장 | 비동기 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 허용 |
| 적합 DB | RDBMS (MySQL, PostgreSQL) | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) |
| 적합 사용 사례 | 금융 거래, 재고 감소 | SNS 좋아요, 추천 피드, 장바구니 |

```text
┌──────────────────────────────────────────────────────────────────────┐
│              결과적 일관성: MSA 이벤트 기반 구현                     │
│                                                                      │
│  주문 서비스                이벤트 버스              재고 서비스      │
│  ┌────────────────┐                               ┌──────────────┐  │
│  │ 1. 주문 DB     │                               │ 3. 재고 DB   │  │
│  │    저장        │  2. OrderPlaced  이벤트 발행   │    감소       │  │
│  │    (커밋)      │──────────────────────────────►│    (비동기)  │  │
│  └────────────────┘                               └──────────────┘  │
│                                                                      │
│  T=0:  주문 DB = "주문완료", 재고 DB = "아직 반영 안됨" [불일치]     │
│  T=1s: 이벤트 전달 완료 → 재고 DB = "감소" [일치]                  │
│                                                                      │
│  SAGA 패턴 보상 트랜잭션:                                            │
│  재고 부족 시 OrderFailed 이벤트 발행 → 주문 서비스가 주문 취소      │
│                                                                      │
│  Outbox 패턴:                                                        │
│  DB 변경 + 이벤트 발행을 로컬 트랜잭션으로 묶어 이중 커밋 방지       │
└──────────────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Eventual Consistency는 은행 이체 후 잔액 반영 — 이체 직후 ATM과 앱이 잠깐 다른 잔액을 보일 수 있지만, 몇 초 후엔 동기화된다.

---

## Ⅲ. 비교 및 연결

| 구분 | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) | [SAGA](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 | [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) |
|:---|:---|:---|:---|
| [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 방식 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 원자 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) 체인 | 비동기 이벤트 전파 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 | 강일관성 | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 낮음 (잠금 발생) | 중간 | 높음 |
| 복잡도 | 중간 | 높음 | 중간 |
| 부분 실패 처리 | 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 보상 이벤트 | 재처리 + DLQ |
| 적합 환경 | 단일/소규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 비즈니스 프로세스 | 고가용성 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 정리:
- **[CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 없음 (단일 RDBMS) — ACID 가능
- **[CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)**: [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) + [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 내성 ([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/), [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/)) — [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선
- **[AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)**: [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) + [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 내성 ([DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)) — [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)

📢 **섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 선택은 "빠른 배달 vs 정확한 배달" — 두 개를 동시에 완벽하게 할 수는 없어서 하나를 조금 양보해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도메인별 [일관성 수준 선택](/knowledge-base/studynote/16_bigdata/06_nosql/140_consistency_levels/)**
- 금융 이체·재고 감소 → ACID 또는 [SAGA](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 (보상 필수)
- 장바구니·좋아요 수 → [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) (잠시 불일치 허용)
- 사용자 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·캐시 → [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 기반 [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)

**Outbox 패턴 (이중 커밋 방지)**
1. 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/): 주문 레코드 + 이벤트 레코드를 동일 DB [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)으로 저장
2. [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) 또는 Relay 프로세스가 이벤트 레코드를 읽어 메시지 큐 발행
3. 이벤트 발행 성공 시 이벤트 레코드 상태 업데이트 → 이중 커밋 없이 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 보장

📢 **섹션 요약 비유**: Outbox 패턴은 복사 카본지 — 원본 주문서(DB [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))를 쓸 때 동시에 이벤트 복사본(Outbox)이 생겨, 나중에 배달(메시지 큐)에 사용한다.

---

## Ⅴ. 기대효과 및 결론

[결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)은 인터넷 규모의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하면서도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성을 달성하는 실용적 타협점이다. MSA에서 [SAGA](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴, Outbox 패턴, [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/))과 결합하면 비즈니스 요구를 충족하면서도 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 피할 수 있다.

한계는 개발자가 "언제 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 맞춰지는가"를 항상 인식해야 하고, 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기 문제(Stale Read)에 대한 UX 설계가 필요하다는 점이다. 도메인별 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 요구 수준을 명확히 분류해 선택적으로 강일관성과 [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)을 혼용하는 설계가 현실적이다.

📢 **섹션 요약 비유**: [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) 설계는 적정 기술 선택 — 모든 곳에 원자력 발전소(ACID)를 세울 필요 없이, 용도에 맞게 태양광(Eventual)과 원자력을 섞어 쓰는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 이론 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 내성 중 2개 선택 |
| BASE 모델 | ACID 대안, [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) 공식화 |
| [SAGA](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)을 보상 이벤트로 처리 |
| Outbox 패턴 | 이중 커밋 없이 DB 변경 + 이벤트 발행 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) |
| [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | DB 변경을 스트림으로 캡처, Outbox 구현에 활용 |
| [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) | 상태 변경을 이벤트로 저장, [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) 기반 |

### 👶 어린이를 위한 3줄 비유 설명
1. [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)은 업데이트되는 인터넷 지도 — 새 건물이 생기면 바로 모든 지도에 반영되지 않고, 시간이 지나면 서서히 업데이트돼요.

### 📈 관련 키워드 및 발전 흐름도

```text
강한 일관성 (2PC · Paxos: 높은 지연)
    │
    ▼
Eventual Consistency: 최종적 일관성 보장
    ├─► SAGA 패턴: 보상 트랜잭션
    └─► Outbox + CDC: 이벤트 안정 발행
    │
    ▼
Tunable Consistency · CRDTs (충돌 해소 자료구조)
```
2. 지도 회사(클라우드)는 일단 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 끊기지 않게 하고, 나중에 업데이트를 맞춰요.
3. 긴급 상황(금융 거래)은 실시간 반영이 필요하지만, 맛집 후기(SNS 좋아요)는 잠깐 오래된 숫자를 보여줘도 괜찮아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 371

← **이전**: [158. gRPC와 프로토콜 버퍼 (gRPC / Protocol Buffers / HTTP2)](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/158_grpc_protocol_buffers_http2/)
**다음**: [160. 이스티오 / 링커디 서비스 메시 (Istio / Linkerd Service Mesh)](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/160_service_mesh_istio_linkerd/) →

---
