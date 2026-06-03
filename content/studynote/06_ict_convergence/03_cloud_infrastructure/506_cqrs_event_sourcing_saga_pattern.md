+++
title = "506. CQRS, 이벤트 소싱, 사가 패턴 (CQRS Event Sourcing Saga Pattern)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)([Command](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Query Responsibility Segregation)는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 읽기 모델을 분리하고, [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/))은 상태 대신 이벤트 이력을 저장하며, [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)([Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/))는 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)을 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)으로 관리한다.
> 2. **가치**: 이 세 패턴의 조합으로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적을 동시에 확보할 수 있다.
> 3. **판단 포인트**: [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 희생시키므로([CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리), MSA에서는 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 기반의 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 패턴이 현실적인 대안이다.

---

## Ⅰ. 개요 및 필요성

모놀리식(Monolithic) 시스템에서는 단일 DB에 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 걸면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장할 수 있다. 그러나 MSA에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 독립 DB를 가지면([Database per Service](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) 패턴) 다음 문제가 생긴다:
- 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(DB-A), 재고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(DB-B), 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(DB-C) 간 [원자적 트랜잭션](/knowledge-base/studynote/02_operating_system/04_synchronization/267_atomic_transaction/) 불가
- 읽기(조회)와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(변경)의 확장성 요구가 다름: 조회는 수백 TPS, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 수십 TPS
- 상태 변경 이력 추적 어려움

[CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/), [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/), [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 패턴이 이 문제들을 각각 해결한다.

- **📢 섹션 요약 비유**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB는 여러 나라에 분점이 있는 기업의 회계다. 각 지점이 독립 장부를 쓰는 만큼, 전체 결산을 맞추는 방법이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/">CQRS</a> + <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a> 구조</strong>:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">명령(Command) 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클라이언트 → Command Handler → 이벤트 발행 → Event Store</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이벤트 브로커(Kafka)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조회(Query) 흐름 Read Model 업데이트</div></div>
<div class="kb-diagram-note">클라이언트 → Query Handler → Read DB(최적화 뷰) ←</div>
</div>
</div>



| 패턴 | 핵심 개념 | 주요 이점 | 트레이드오프 |
|:---|:---|:---|:---|
| [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) | Write/Read 모델 분리 | 각 모델 독립 최적화 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 복잡성 |
| [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) | 상태 대신 이벤트 저장 | 완전한 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 이력, 리플레이 | 이벤트 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 어려움 |
| [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) ([Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)) | [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)으로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) TX | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지, 느슨한 결합 | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(Eventual) |

<strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/">Event Sourcing</a>) 핵심</strong>:
- [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 대신 이벤트 이력(History) 저장: `OrderCreated`, `PaymentConfirmed`, `OrderShipped`
- [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) = [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태 + 모든 이벤트 순차 적용(리플레이)
- 장점: 완전한 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적, 특정 시점으로 상태 복원, 이벤트 기반 통합 용이

<strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/">사가</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a>) 패턴 두 가지 방식</strong>:
- **코레오그래피(Choreography)**: 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이벤트를 발행하고 구독하여 자율적으로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/). 중앙 조율 없음.
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a>(<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a>)</strong>: [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 오케스트레이터가 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 순서대로 호출하고 실패 시 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) 실행.

- **📢 섹션 요약 비유**: 코레오그래피는 재즈 밴드처럼 각자 박자에 맞춰 연주하는 것, [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)은 지휘자(오케스트레이터)가 각 악기를 순서대로 지시하는 것이다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/">2PC</a>(<a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/">Two-Phase Commit</a>) vs <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/">사가</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a>)</strong>:

| 구분 | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) | [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)([Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)) |
|:---|:---|:---|
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (ACID) | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | 낮음 (코디네이터 장애 시 블록) | 높음 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 낮음 (글로벌 잠금) | 높음 |
| [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 적합성 | 낮음 | 높음 |

2PC는 모든 참여자가 Prepare 단계에서 잠금([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 유지하므로, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) MSA에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 모두 희생된다. [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 각 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 독립 커밋하고 실패 시 보상([Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))으로 되돌린다.

- **📢 섹션 요약 비유**: 2PC는 모두가 동시에 계약서에 서명해야 하는 방식, [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 순서대로 서명하고 한 명이 취소하면 이미 서명한 사람들이 계약을 무효화(보상)하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. CQRS의 Read/Write 모델 분리로 각 모델을 독립 최적화(Write는 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), Read는 비정규화 뷰)할 수 있음을 설명한다.
2. [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)에서 "리플레이(Replay)" 기능이 디버깅, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션에 활용됨을 언급한다.
3. [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 코레오그래피 vs [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)의 장단점을 명확히 대비한다.

**실무 시나리오**: 전자상거래 주문 처리 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)([오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 방식):
1. 주문 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 2. 결제 요청 → 3. 재고 차감 → 4. 배송 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
실패 시 보상: 배송 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 실패 → 재고 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) → 결제 취소 → 주문 실패 처리
→ 각 단계가 독립 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 전체 실패 없이 보상으로 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지

- **📢 섹션 요약 비유**: [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 릴레이 경주다 — 한 주자가 넘어지면, 앞서 뛴 주자들이 되돌아와 경기를 취소(보상)한다. 전체 레이스는 멈추지 않는다.

---

## Ⅴ. 기대효과 및 결론

[CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/), [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/), [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 패턴을 적절히 조합하면:
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 향상</strong>: 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 독립 확장으로 조회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 10배 이상 개선 가능
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 완전성</strong>: [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)으로 모든 상태 변경 이력 영구 보존
- <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/">분산 트랜잭션</a> 해결</strong>: [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)로 MSA에서도 비즈니스 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지
- **유연성**: 이벤트 스트림 재처리로 새로운 Read Model 추가 용이

이 패턴들은 복잡도가 높으므로, 단순한 CRUD 시스템에 무조건 적용하는 것은 과잉 설계(Over-engineering)다. 복잡한 비즈니스 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 있는 MSA에서만 선택적으로 적용한다.

- **📢 섹션 요약 비유**: [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)/[이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)/[사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 큰 도시의 교통 시스템이다 — [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(읽기), 지하철([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)), 환승([사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/))을 분리하면 효율적이지만, 작은 마을에선 그냥 자전거(단순 CRUD)가 더 낫다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservice Architecture](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/365_msa_microservice_architecture/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리, [Database per Service](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) · 505 |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) (이벤트 브로커) | 이벤트 스트리밍, 메시지 큐 · 505 |
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 허용 · 507 |
| [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) | [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/), XA [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) · 505 |
| 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | BASE [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/), 비동기 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) · 507 |

### 📈 관련 키워드 및 발전 흐름도

```text
[서비스 분리 · Database per Service] → [CQRS · 이벤트 소싱] → [BASE 속성 · 비동기 동기화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. CQRS는 글쓰기 연필([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))과 읽기 안경(읽기)을 따로 가지는 것처럼, 저장과 조회를 다른 방법으로 해요.
2. [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 일기장에 매일 있었던 일을 기록하는 것 — 오늘 상태를 지우지 않고, 어제부터 오늘까지 일어난 일을 모두 쌓아가요.
3. [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 패턴은 릴레이 경주처럼, 한 팀원이 실수하면 앞서 달린 팀원들이 함께 되돌아와 처음부터 다시 시작해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 506 / 552

← **이전**: [505. 마이크로서비스, API 게이트웨이, 서비스 메시 (MSA API Gateway Service Mesh)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/505_microservices_api_gateway_service_mesh/)
**다음**: [507. 카오스 엔지니어링, 섀도 배포, 서킷 브레이커 (Chaos Engineering Shadow Deployment Circuit](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/507_chaos_engineering_shadow_circuit_breaker/) →

---
