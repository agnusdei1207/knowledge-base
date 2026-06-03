---
title: 159. 결과적 일관성 (Eventual Consistency)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[650_eventual_consistency|결과적 일관성]] ([[650_eventual_consistency|Eventual Consistency]])이란 [[136_variance|분산]] 시스템에서 즉각적인 강일관성(Strong [[194_consistency_database_integrity|Consistency]]) 대신 "충분한 시간이 흐르면 모든 노드의 [[001_dikw_pyramid|데이터]]가 일치하게 된다"는 사상으로, [[341_process|CAP]] 이론의 A([[452_availability|가용성]])와 P([[136_variance|분산]] 내성) 선택 시 C([[194_consistency_database_integrity|일관성]])를 완화한 결과다.
> 2. **가치**: [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 없이도 높은 [[452_availability|가용성]]과 [[282_performance_tactics|성능]]을 유지하면서 최종적으로 [[001_dikw_pyramid|데이터]] 정합성을 보장하므로, [[619_msa_traffic_hardware|MSA]] 환경의 비동기 이벤트 기반 아키텍처와 완벽하게 부합한다.
> 3. **판단 포인트**: 잠시 오래된 [[001_dikw_pyramid|데이터]]를 보여줘도 비즈니스 영향이 없는(SNS 좋아요 수 등) 시스템은 Eventual Consistency가 최선이나, 금융 이체처럼 순간적으로도 [[001_dikw_pyramid|데이터]]가 틀려서는 안 되는 경우에는 여전히 강일관성 또는 [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])가 필요하다.

---

## Ⅰ. 개요 및 필요성

단일 RDBMS (Relational [[501_database|Database]] [[372_management|Management]] System)에서는 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) [[191_transaction_concept_states|트랜잭션]]이 즉각적인 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]을 보장한다. 그러나 [[532_microservices_decomposition_patterns|마이크로서비스]] 환경에서 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 독립된 DB를 소유하면, 여러 [[090_service_kubernetes_network_load_balancing|서비스]]에 걸친 [[191_transaction_concept_states|트랜잭션]]을 원자적으로 처리하기 위한 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] ([[549_2pc_two_phase_commit_limitations_msa|2PC]])은 [[282_performance_tactics|성능]] 병목과 [[452_availability|가용성]] 저하를 초래한다.

[[341_process|CAP]] ([[194_consistency_database_integrity|Consistency]], [[452_availability|Availability]], [[514_partition_slice_volume|Partition]] Tolerance) 이론은 [[136_variance|분산]] 시스템이 네트워크 [[514_partition_slice_volume|파티션]](P) 상황에서 [[194_consistency_database_integrity|일관성]](C)과 [[452_availability|가용성]](A)을 동시에 완벽하게 만족할 수 없다고 말한다. 대부분의 인터넷 규모 [[136_variance|분산]] 시스템은 A와 P를 선택하고 C를 완화—즉 "결국에는 일치한다"는 [[650_eventual_consistency|결과적 일관성]]을 채택한다.

BASE (Basically Available, Soft [[272_state_pattern|State]], [[650_eventual_consistency|Eventual Consistency]]) 모델은 이 철학을 정식화한 것으로, ACID의 대안으로 [[035_nosql|NoSQL]]·[[136_variance|분산]] 시스템 설계의 근간이 된다.

📢 **섹션 요약 비유**: [[650_eventual_consistency|결과적 일관성]]은 소문 전파 — 어제 일어난 일이 모든 마을 사람에게 퍼지려면 시간이 필요하지만, 결국에는 모두가 같은 이야기를 알게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | ACID (강일관성) | BASE ([[650_eventual_consistency|결과적 일관성]]) |
|:---|:---|:---|
| [[193_atomicity_all_or_nothing|Atomicity]] / Basically Available | 모두 성공 또는 전체 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 기본 [[452_availability|가용성]] 유지, 부분 실패 허용 |
| [[194_consistency_database_integrity|Consistency]] / Soft [[272_state_pattern|State]] | [[191_transaction_concept_states|트랜잭션]] 후 즉시 일관 | 일시적으로 불일치 상태 허용 |
| [[195_isolation_concurrency_control|Isolation]] / Eventual | 다른 [[191_transaction_concept_states|트랜잭션]] 간섭 없음 | 결국 일관 상태에 도달 |
| [[196_durability_permanent_storage|Durability]] | 커밋 후 영구 저장 | 비동기 [[016_replication_factor|복제]] 허용 |
| 적합 DB | RDBMS (MySQL, PostgreSQL) | [[545_dynamodb|DynamoDB]], [[541_cassandra|Cassandra]], [[540_mongodb|MongoDB]] |
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

| 구분 | [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) | [[305_saga|SAGA]] 패턴 | [[650_eventual_consistency|Eventual Consistency]] |
|:---|:---|:---|:---|
| [[191_transaction_concept_states|트랜잭션]] 방식 | [[136_variance|분산]] 원자 [[191_transaction_concept_states|트랜잭션]] | [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] 체인 | 비동기 이벤트 전파 |
| [[194_consistency_database_integrity|일관성]] 수준 | 강일관성 | 최종 [[194_consistency_database_integrity|일관성]] | 최종 [[194_consistency_database_integrity|일관성]] |
| [[282_performance_tactics|성능]] | 낮음 (잠금 발생) | 중간 | 높음 |
| 복잡도 | 중간 | 높음 | 중간 |
| 부분 실패 처리 | 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 보상 이벤트 | 재처리 + DLQ |
| 적합 환경 | 단일/소규모 [[136_variance|분산]] | [[619_msa_traffic_hardware|MSA]] 비즈니스 프로세스 | 고가용성 [[619_msa_traffic_hardware|MSA]] |

[[341_process|CAP]] 정리 정리:
- **[[089_contract_account_smart_contract|CA]]**: [[136_variance|분산]] 없음 (단일 RDBMS) — ACID 가능
- **[[086_CP_순환_전치_GI|CP]]**: [[194_consistency_database_integrity|일관성]] + [[136_variance|분산]] 내성 ([[798_distributed_lock_zookeeper_consensus|ZooKeeper]], [[078_etcd_distributed_key_value_store|etcd]]) — [[194_consistency_database_integrity|일관성]] 우선
- **[[572_ap_access_point_ds_distribution_system|AP]]**: [[452_availability|가용성]] + [[136_variance|분산]] 내성 ([[545_dynamodb|DynamoDB]], [[541_cassandra|Cassandra]]) — [[650_eventual_consistency|Eventual Consistency]]

📢 **섹션 요약 비유**: [[341_process|CAP]] 선택은 "빠른 배달 vs 정확한 배달" — 두 개를 동시에 완벽하게 할 수는 없어서 하나를 조금 양보해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도메인별 [[140_consistency_levels|일관성 수준 선택]]**
- 금융 이체·재고 감소 → ACID 또는 [[305_saga|SAGA]] 패턴 (보상 필수)
- 장바구니·좋아요 수 → [[650_eventual_consistency|Eventual Consistency]] (잠시 불일치 허용)
- 사용자 [[160_session_controlling_terminal|세션]]·캐시 → [[294_ttl_time_to_live_looping_prevention|TTL]] 기반 [[650_eventual_consistency|Eventual Consistency]]

**Outbox 패턴 (이중 커밋 방지)**
1. 주문 [[090_service_kubernetes_network_load_balancing|서비스]]: 주문 레코드 + 이벤트 레코드를 동일 DB [[191_transaction_concept_states|트랜잭션]]으로 저장
2. [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) 또는 Relay 프로세스가 이벤트 레코드를 읽어 메시지 큐 발행
3. 이벤트 발행 성공 시 이벤트 레코드 상태 업데이트 → 이중 커밋 없이 [[193_atomicity_all_or_nothing|원자성]] 보장

📢 **섹션 요약 비유**: Outbox 패턴은 복사 카본지 — 원본 주문서(DB [[191_transaction_concept_states|트랜잭션]])를 쓸 때 동시에 이벤트 복사본(Outbox)이 생겨, 나중에 배달(메시지 큐)에 사용한다.

---

## Ⅴ. 기대효과 및 결론

[[650_eventual_consistency|결과적 일관성]]은 인터넷 규모의 [[136_variance|분산]] 시스템이 높은 [[452_availability|가용성]]과 [[282_performance_tactics|성능]]을 유지하면서도 [[001_dikw_pyramid|데이터]] 정합성을 달성하는 실용적 타협점이다. MSA에서 [[305_saga|SAGA]] 패턴, Outbox 패턴, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]])과 결합하면 비즈니스 요구를 충족하면서도 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]의 [[282_performance_tactics|성능]] 병목을 피할 수 있다.

한계는 개발자가 "언제 [[194_consistency_database_integrity|일관성]]이 맞춰지는가"를 항상 인식해야 하고, 오래된 [[001_dikw_pyramid|데이터]] 읽기 문제(Stale Read)에 대한 UX 설계가 필요하다는 점이다. 도메인별 [[194_consistency_database_integrity|일관성]] 요구 수준을 명확히 분류해 선택적으로 강일관성과 [[650_eventual_consistency|결과적 일관성]]을 혼용하는 설계가 현실적이다.

📢 **섹션 요약 비유**: [[650_eventual_consistency|결과적 일관성]] 설계는 적정 기술 선택 — 모든 곳에 원자력 발전소(ACID)를 세울 필요 없이, 용도에 맞게 태양광(Eventual)과 원자력을 섞어 쓰는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[341_process|CAP]] 이론 | [[194_consistency_database_integrity|일관성]]·[[452_availability|가용성]]·[[136_variance|분산]] 내성 중 2개 선택 |
| BASE 모델 | ACID 대안, [[650_eventual_consistency|Eventual Consistency]] 공식화 |
| [[305_saga|SAGA]] 패턴 | [[619_msa_traffic_hardware|MSA]] [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]을 보상 이벤트로 처리 |
| Outbox 패턴 | 이중 커밋 없이 DB 변경 + 이벤트 발행 [[193_atomicity_all_or_nothing|원자성]] |
| [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | DB 변경을 스트림으로 캡처, Outbox 구현에 활용 |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) | 상태 변경을 이벤트로 저장, [[650_eventual_consistency|Eventual Consistency]] 기반 |

### 👶 어린이를 위한 3줄 비유 설명
1. [[650_eventual_consistency|결과적 일관성]]은 업데이트되는 인터넷 지도 — 새 건물이 생기면 바로 모든 지도에 반영되지 않고, 시간이 지나면 서서히 업데이트돼요.

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
2. 지도 회사(클라우드)는 일단 [[090_service_kubernetes_network_load_balancing|서비스]]는 끊기지 않게 하고, 나중에 업데이트를 맞춰요.
3. 긴급 상황(금융 거래)은 실시간 반영이 필요하지만, 맛집 후기(SNS 좋아요)는 잠깐 오래된 숫자를 보여줘도 괜찮아요.
