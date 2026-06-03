---
title: 506. CQRS, 이벤트 소싱, 사가 패턴 (CQRS Event Sourcing Saga Pattern)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[306_cqrs|CQRS]]([[271_command_pattern|Command]] Query Responsibility Segregation)는 [[289_cqrs_db|쓰기]]와 읽기 모델을 분리하고, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]])은 상태 대신 이벤트 이력을 저장하며, [[312_saga_pattern_choreography_orchestration|사가]]([[305_saga|Saga]])는 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]을 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]으로 관리한다.
> 2. **가치**: 이 세 패턴의 조합으로 [[136_variance|분산]] [[619_msa_traffic_hardware|MSA]] 환경에서도 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], [[282_performance_tactics|성능]], [[606_auditing_linux_auditd|감사]] 추적을 동시에 확보할 수 있다.
> 3. **판단 포인트**: [[549_2pc_two_phase_commit_limitations_msa|2PC]]([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])는 [[136_variance|분산]] 시스템에서 [[452_availability|가용성]]을 희생시키므로([[341_process|CAP]] 정리), MSA에서는 최종 [[194_consistency_database_integrity|일관성]]([[650_eventual_consistency|Eventual Consistency]]) 기반의 [[312_saga_pattern_choreography_orchestration|사가]] 패턴이 현실적인 대안이다.

---

## Ⅰ. 개요 및 필요성

모놀리식(Monolithic) 시스템에서는 단일 DB에 [[191_transaction_concept_states|트랜잭션]]을 걸면 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]을 보장할 수 있다. 그러나 MSA에서 [[090_service_kubernetes_network_load_balancing|서비스]]마다 독립 DB를 가지면([[311_database_per_service_pattern|Database per Service]] 패턴) 다음 문제가 생긴다:
- 주문 [[090_service_kubernetes_network_load_balancing|서비스]](DB-A), 재고 [[090_service_kubernetes_network_load_balancing|서비스]](DB-B), 결제 [[090_service_kubernetes_network_load_balancing|서비스]](DB-C) 간 [[267_atomic_transaction|원자적 트랜잭션]] 불가
- 읽기(조회)와 [[289_cqrs_db|쓰기]](변경)의 확장성 요구가 다름: 조회는 수백 TPS, [[289_cqrs_db|쓰기]]는 수십 TPS
- 상태 변경 이력 추적 어려움

[[306_cqrs|CQRS]], [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]], [[312_saga_pattern_choreography_orchestration|사가]] 패턴이 이 문제들을 각각 해결한다.

- **📢 섹션 요약 비유**: [[136_variance|분산]] DB는 여러 나라에 분점이 있는 기업의 회계다. 각 지점이 독립 장부를 쓰는 만큼, 전체 결산을 맞추는 방법이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**[[306_cqrs|CQRS]] + [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 구조**:

```
┌─────────────────────────────────────────────────────────────┐
│  명령(Command) 흐름                                          │
│  클라이언트 → Command Handler → 이벤트 발행 → Event Store    │
│                                             ↓               │
│                                     이벤트 브로커(Kafka)     │
│                                             ↓               │
│  조회(Query) 흐름                   Read Model 업데이트       │
│  클라이언트 → Query Handler → Read DB(최적화 뷰) ←───────────┘
└─────────────────────────────────────────────────────────────┘
```

| 패턴 | 핵심 개념 | 주요 이점 | 트레이드오프 |
|:---|:---|:---|:---|
| [[306_cqrs|CQRS]] | Write/Read 모델 분리 | 각 모델 독립 최적화 | [[212_synchronization_mechanisms|동기화]] 복잡성 |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) | 상태 대신 이벤트 저장 | 완전한 [[606_auditing_linux_auditd|감사]] 이력, 리플레이 | 이벤트 [[005_schema|스키마]] 진화 어려움 |
| [[312_saga_pattern_choreography_orchestration|사가]] ([[305_saga|Saga]]) | [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]으로 [[136_variance|분산]] TX | [[452_availability|가용성]] 유지, 느슨한 결합 | 최종 [[194_consistency_database_integrity|일관성]](Eventual) |

**[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]]) 핵심**:
- [[178_as_is_to_be_analysis|현재 상태]]([[272_state_pattern|State]]) 대신 이벤트 이력(History) 저장: `OrderCreated`, `PaymentConfirmed`, `OrderShipped`
- [[178_as_is_to_be_analysis|현재 상태]] = [[459_quic_fec_forward_error_correction|초기]] 상태 + 모든 이벤트 순차 적용(리플레이)
- 장점: 완전한 [[606_auditing_linux_auditd|감사]] 추적, 특정 시점으로 상태 복원, 이벤트 기반 통합 용이

**[[312_saga_pattern_choreography_orchestration|사가]]([[305_saga|Saga]]) 패턴 두 가지 방식**:
- **코레오그래피(Choreography)**: 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 이벤트를 발행하고 구독하여 자율적으로 [[216_progress_in_synchronization|진행]]. 중앙 조율 없음.
- **[[073_container_orchestration_tools|오케스트레이션]]([[073_container_orchestration_tools|Orchestration]])**: [[312_saga_pattern_choreography_orchestration|사가]] 오케스트레이터가 각 [[090_service_kubernetes_network_load_balancing|서비스]]를 순서대로 호출하고 실패 시 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] 실행.

- **📢 섹션 요약 비유**: 코레오그래피는 재즈 밴드처럼 각자 박자에 맞춰 연주하는 것, [[073_container_orchestration_tools|오케스트레이션]]은 지휘자(오케스트레이터)가 각 악기를 순서대로 지시하는 것이다.

---

## Ⅲ. 비교 및 연결

**[[549_2pc_two_phase_commit_limitations_msa|2PC]]([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) vs [[312_saga_pattern_choreography_orchestration|사가]]([[305_saga|Saga]])**:

| 구분 | [[549_2pc_two_phase_commit_limitations_msa|2PC]] | [[312_saga_pattern_choreography_orchestration|사가]]([[305_saga|Saga]]) |
|:---|:---|:---|
| [[194_consistency_database_integrity|일관성]] | 강한 [[194_consistency_database_integrity|일관성]] (ACID) | 최종 [[194_consistency_database_integrity|일관성]] |
| [[452_availability|가용성]] | 낮음 (코디네이터 장애 시 블록) | 높음 |
| [[282_performance_tactics|성능]] | 낮음 (글로벌 잠금) | 높음 |
| [[619_msa_traffic_hardware|MSA]] 적합성 | 낮음 | 높음 |

2PC는 모든 참여자가 Prepare 단계에서 잠금([[510_lock|Lock]])을 유지하므로, [[136_variance|분산]] MSA에서는 [[282_performance_tactics|성능]]과 [[452_availability|가용성]] 모두 희생된다. [[312_saga_pattern_choreography_orchestration|사가]]는 각 로컬 [[191_transaction_concept_states|트랜잭션]]이 독립 커밋하고 실패 시 보상([[551_compensating_transaction_logical_rollback|Compensating Transaction]])으로 되돌린다.

- **📢 섹션 요약 비유**: 2PC는 모두가 동시에 계약서에 서명해야 하는 방식, [[312_saga_pattern_choreography_orchestration|사가]]는 순서대로 서명하고 한 명이 취소하면 이미 서명한 사람들이 계약을 무효화(보상)하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. CQRS의 Read/Write 모델 분리로 각 모델을 독립 최적화(Write는 [[093_normalization|정규화]], Read는 비정규화 뷰)할 수 있음을 설명한다.
2. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]에서 "리플레이(Replay)" 기능이 디버깅, [[606_auditing_linux_auditd|감사]], [[001_dikw_pyramid|데이터]] 마이그레이션에 활용됨을 언급한다.
3. [[312_saga_pattern_choreography_orchestration|사가]] 코레오그래피 vs [[073_container_orchestration_tools|오케스트레이션]]의 장단점을 명확히 대비한다.

**실무 시나리오**: 전자상거래 주문 처리 [[312_saga_pattern_choreography_orchestration|사가]]([[073_container_orchestration_tools|오케스트레이션]] 방식):
1. 주문 [[087_process_state_transition|생성]] → 2. 결제 요청 → 3. 재고 차감 → 4. 배송 [[087_process_state_transition|생성]]
실패 시 보상: 배송 [[087_process_state_transition|생성]] 실패 → 재고 [[658_ir_recovery|복구]] → 결제 취소 → 주문 실패 처리
→ 각 단계가 독립 [[090_service_kubernetes_network_load_balancing|서비스]], 전체 실패 없이 보상으로 [[194_consistency_database_integrity|일관성]] 유지

- **📢 섹션 요약 비유**: [[312_saga_pattern_choreography_orchestration|사가]]는 릴레이 경주다 — 한 주자가 넘어지면, 앞서 뛴 주자들이 되돌아와 경기를 취소(보상)한다. 전체 레이스는 멈추지 않는다.

---

## Ⅴ. 기대효과 및 결론

[[306_cqrs|CQRS]], [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]], [[312_saga_pattern_choreography_orchestration|사가]] 패턴을 적절히 조합하면:
- **[[282_performance_tactics|성능]] 향상**: 읽기/[[289_cqrs_db|쓰기]] 독립 확장으로 조회 [[282_performance_tactics|성능]] 10배 이상 개선 가능
- **[[606_auditing_linux_auditd|감사]] 완전성**: [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]으로 모든 상태 변경 이력 영구 보존
- **[[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 해결**: [[312_saga_pattern_choreography_orchestration|사가]]로 MSA에서도 비즈니스 [[191_transaction_concept_states|트랜잭션]] [[194_consistency_database_integrity|일관성]] 유지
- **유연성**: 이벤트 스트림 재처리로 새로운 Read Model 추가 용이

이 패턴들은 복잡도가 높으므로, 단순한 CRUD 시스템에 무조건 적용하는 것은 과잉 설계(Over-engineering)다. 복잡한 비즈니스 [[191_transaction_concept_states|트랜잭션]]이 있는 MSA에서만 선택적으로 적용한다.

- **📢 섹션 요약 비유**: [[306_cqrs|CQRS]]/[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]/[[312_saga_pattern_choreography_orchestration|사가]]는 큰 도시의 교통 시스템이다 — [[344_bus|버스]](읽기), 지하철([[289_cqrs_db|쓰기]]), 환승([[312_saga_pattern_choreography_orchestration|사가]])을 분리하면 효율적이지만, 작은 마을에선 그냥 자전거(단순 CRUD)가 더 낫다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[619_msa_traffic_hardware|MSA]] ([[365_msa_microservice_architecture|Microservice Architecture]]) | [[090_service_kubernetes_network_load_balancing|서비스]] 분리, [[311_database_per_service_pattern|Database per Service]] · 505 |
| [[179_kafka_flink_watermark_time_window|Kafka]] (이벤트 브로커) | 이벤트 스트리밍, 메시지 큐 · 505 |
| [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) | [[194_consistency_database_integrity|일관성]], [[452_availability|가용성]], [[514_partition_slice_volume|파티션]] 허용 · 507 |
| [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]], XA [[295_protocol_field_tcp_udp_icmp|프로토콜]] · 505 |
| 최종 [[194_consistency_database_integrity|일관성]] ([[650_eventual_consistency|Eventual Consistency]]) | BASE [[082_attribute_types_er_model|속성]], 비동기 [[212_synchronization_mechanisms|동기화]] · 507 |

### 📈 관련 키워드 및 발전 흐름도

```text
[서비스 분리 · Database per Service] → [CQRS · 이벤트 소싱] → [BASE 속성 · 비동기 동기화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. CQRS는 글쓰기 연필([[289_cqrs_db|쓰기]])과 읽기 안경(읽기)을 따로 가지는 것처럼, 저장과 조회를 다른 방법으로 해요.
2. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 일기장에 매일 있었던 일을 기록하는 것 — 오늘 상태를 지우지 않고, 어제부터 오늘까지 일어난 일을 모두 쌓아가요.
3. [[312_saga_pattern_choreography_orchestration|사가]] 패턴은 릴레이 경주처럼, 한 팀원이 실수하면 앞서 달린 팀원들이 함께 되돌아와 처음부터 다시 시작해요.
