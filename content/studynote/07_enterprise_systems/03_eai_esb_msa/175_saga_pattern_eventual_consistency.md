+++
title = "175. 사가 패턴 (Saga Pattern) - 로컬 트랜잭션 연쇄와 보상 트랜잭션으로 최종적 일관성 보장"
date = 2026-05-06

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/))은 하나의 긴 비즈니스 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 여러 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)으로 쪼개고, 각 단계가 성공할 때 다음 단계를 이어 가며 실패 시 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))으로 되돌리는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방식이다.
> 2. **가치**: [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))처럼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체를 오래 묶어 두지 않고도 [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))에서 업무 흐름 수준의 정합성을 맞출 수 있다.
> 3. **판단 포인트**: 보상 가능성, [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)), 상태 추적, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), 사용자 노출 상태를 함께 설계하지 않으면 최종적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))은 곧 운영 혼란으로 바뀐다.

---

## Ⅰ. 개요 및 필요성

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 각자 자기 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 가진 환경에서, 하나의 업무를 어떻게 일관되게 끝낼지 다루는 아키텍처 패턴이다. 주문, 결제, 재고, 배송처럼 한 번의 사용자 요청이 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 걸쳐 퍼지는 순간, 단일 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 쓰던 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계는 더 이상 그대로 적용되지 않는다.

문제는 비즈니스 관점에서는 "한 건의 주문"인데, 시스템 관점에서는 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 독립 커밋으로 쪼개진다는 점이다. 주문은 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)됐지만 결제가 실패하거나, 결제는 승인됐는데 재고 확보가 실패하면 사용자는 성공과 실패가 섞인 상태를 보게 된다. 그렇다고 2PC처럼 전역 락과 중앙 조정자를 두면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립성과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 크게 떨어진다.

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 여기서 출발한다. <strong>강한 전역 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 대신, 로컬 성공을 차례로 쌓고 실패하면 비즈니스적으로 상쇄하는 행동을 역순으로 실행하자</strong>는 것이다. 즉 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 레벨의 하나의 거대한 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 아니라, 비즈니스 흐름 수준의 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 문제를 푼다.

아래 그림은 MSA에서 왜 별도의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 패턴이 필요한지를 보여 준다. 업무는 하나처럼 보이지만, 실제 저장소 경계는 여러 개로 나뉘어 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">One business action, many local databases</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Order Service DB Payment Service DB Inventory Service DB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">business success must span all</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">In typical MSA, no single ACID transaction covers all three</div></div>
</div>
</div>



따라서 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)의 필요성은 단순히 "비동기라서 멋있다"가 아니다. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 분리로 잃어버린 전역 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>을, 이벤트와 보상이라는 다른 철학으로 다시 조립하는 방식</strong>이기 때문에 중요하다.

- **📢 섹션 요약 비유**: 여러 가게가 한 세트 상품을 함께 파는 상황과 같다. 한 가게에서 환불이 필요해도 모든 계산을 한 번에 취소할 수 없으니, 이미 끝난 계산은 각 가게가 자기 방식으로 다시 정정해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)의 기본 구성은 <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/">로컬 트랜잭션</a>, 다음 단계를 촉발하는 이벤트 또는 명령, 실패 시 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a>, 그리고 전체 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/">진행</a> 상태를 추적하는 메커니즘</strong>이다. 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 안에서는 짧고 강한 로컬 커밋을 수행하고, 그 결과를 바탕으로 다음 단계를 이어 준다.

| 구성 요소 | 역할 | 왜 필요한가 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부에서 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 커밋 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립성 유지 | 짧고 명확해야 함 |
| 이벤트 / 명령 | 다음 단계를 시작시키는 연결 고리 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 흐름 전달 | 중복 수신 대비 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 필요 |
| [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) | 실패 시 이전 성공을 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 상쇄 | 전역 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 부재 보완 | 업무적으로 되돌릴 수 있어야 함 |
| 상태 추적 | 현재 단계, 실패 위치, 재시도 여부 관리 | 운영 가시성 확보 | 상관관계 ID, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 필요 |
| 아웃박스 패턴 | DB 반영과 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행의 간극 축소 | 유실 없는 연계 | 로컬 커밋과 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |

[사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)의 핵심은 "이전 단계를 지운다"가 아니라 <strong>이전 단계를 상쇄하는 새 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>을 실행한다</strong>는 점이다. 예를 들어 `주문 생성`을 물리적으로 [ROLLBACK](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) 하는 것이 아니라, `주문 취소` 상태를 새로 기록한다. 이미 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 로컬 커밋은 끝났기 때문이다.

아래 그림은 성공 경로와 실패 시 보상 경로를 함께 보여 준다. 포인트는 실패가 난 지점보다 앞서 성공한 단계들이 <strong>역순 보상</strong>으로 정리된다는 것이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Saga forward flow and compensation</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">commit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">commit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">FAIL</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">compensation path:</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2c</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">commit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1c</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">commit</div></div>
</div>
</div>



구현 방식은 크게 두 갈래다. **코레오그래피 (Choreography)** 는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들이 이벤트를 보고 스스로 다음 행동을 결정하는 방식이고, <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a>)</strong> 은 중앙 오케스트레이터가 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 명령을 보내며 상태를 관리하는 방식이다. 전자는 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추기 쉽지만 흐름 가시성이 떨어질 수 있고, 후자는 통제가 쉽지만 중앙 조정 로직이 두꺼워질 수 있다.

결국 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)의 핵심 원리는 "전역 커밋"이 아니라 <strong>전진 경로와 <a href="/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/">후퇴</a> 경로를 모두 비즈니스적으로 모델링하는 것</strong>이다. 이 설계가 있어야 최종적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 단순 희망사항이 아니라 실제 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 된다.

- **📢 섹션 요약 비유**: 릴레이 경기처럼 한 주자가 바통을 넘기며 앞으로 나아가되, 중간에 문제가 생기면 이미 지나간 주자들이 반대로 뛰어와 자기 구간을 다시 정리하는 방식과 같다.

---

## Ⅲ. 비교 및 연결

[사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)를 정확히 이해하려면 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/), [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/), TCC (Try-Confirm-Cancel) 와 비교해야 한다. 모두 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무를 일관되게 끝내려는 시도지만, <strong>락을 거는 방식과 실패 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 철학</strong>이 다르다.

| 비교 축 | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) | [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) | TCC |
| :--- | :--- | :--- | :--- | :--- |
| 적용 범위 | 단일 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부 | 여러 자원의 전역 커밋 | 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 업무 흐름 | 예약 가능한 자원 흐름 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 최종적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 단계적 강한 제어 |
| 실패 처리 | 즉시 [ROLLBACK](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) | 조정자 결정 대기 | [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) 실행 | Cancel 호출 |
| 블로킹 | 짧음 | Prepare 이후 길어질 수 있음 | 낮음 | 중간 예약 비용 존재 |
| 잘 맞는 환경 | 단일 DB 업무 | 통제된 내부 시스템 | 클라우드형 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) | 좌석·재고·한도 예약 |

[사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)와 2PC의 가장 큰 차이는 "언제 확정하느냐"다. 2PC는 마지막까지 모두를 묶어 두었다가 한 번에 확정하려 하고, [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 각 단계가 먼저 확정된 뒤 나중에 문제가 생기면 보상으로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)한다. 그래서 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 독립성에 강하지만, 중간 순간에는 잠시 불일치가 존재할 수 있다.

또 하나 중요한 연결은 <strong>코레오그래피 vs <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a></strong> 선택이다. 이벤트가 몇 단계 안 되고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 결합을 낮추는 것이 최우선이라면 코레오그래피가 자연스럽다. 반대로 승인 이력, 단계 추적, 규제 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 관리가 중요하면 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)이 더 적합하다. 즉 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 하나의 구현이 아니라, 공통 철학 위에 여러 조정 방식을 얹는 프레임이다.

또한 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 [트랜잭셔널 아웃박스](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)), 멱등 소비자, 데드 레터 큐와 함께 설계될 때 안정성이 높아진다. [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지는 보통 적어도 한 번(at-least-once) 전달되므로, 같은 보상 이벤트가 두 번 와도 결과가 망가지지 않아야 한다. 이 연결 고리가 약하면 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 아니라 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 혼란이 된다.

- **📢 섹션 요약 비유**: 2PC가 모두가 손을 잡고 동시에 움직이는 행진이라면, [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 각자 먼저 움직이고 문제가 생기면 뒤돌아와 자기 자리를 정리하는 팀플레이다. 어느 쪽이 맞는지는 규율보다 현장의 속도와 복잡도에 달려 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 주문-결제-재고-배송 같은 <strong>긴 업무 흐름</strong>에 자주 쓰인다. 예를 들어 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 주문을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 재고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 수량을 예약하고, 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 승인한 뒤, 배송 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 출고를 잡는 흐름을 생각할 수 있다. 여기서 결제가 실패하면 재고 예약을 해제하고 주문 상태를 취소로 바꾸는 식으로 비즈니스적으로 정리한다.

다만 모든 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)에 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)가 맞는 것은 아니다. 보상 자체가 불가능하거나, 한 번 외부에 노출된 결과를 되돌려도 법적·금전적 문제가 남는 경우는 더 강한 제어가 필요하다. 예를 들어 좌석 선점, 잔액 차감, 중복 없는 번호 발급처럼 희소 자원을 다루는 흐름은 TCC나 예약 모델이 더 적절할 수 있다. 즉 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)의 전제는 "되돌릴 수 있음"이 아니라, <strong>업무적으로 상쇄 가능한 반대 동작을 설계할 수 있음</strong>이다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 각 단계에 대해 현실적인 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)을 정의할 수 있는가?
2. 이벤트 중복 수신과 재시도를 견딜 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)이 보장되는가?
3. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 반영과 이벤트 발행 사이를 아웃박스 패턴 등으로 안전하게 연결했는가?
4. 사용자 화면에 `PENDING`, `FAILED`, `CANCELLED` 같은 중간 상태를 자연스럽게 표현할 수 있는가?
5. [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), 재시도, 데드 레터 큐, 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 준비되어 있는가?
6. 규제 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)와 운영 추적이 중요하다면 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)이 더 적합하지 않은가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 보상 로직 없이 "일단 이벤트로 묶으면 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)"라고 부르는 경우
- 동일 이벤트가 두 번 들어왔을 때 중복 취소·중복 결제가 발생하는 경우
- 사용자에게는 즉시 완료처럼 보이게 하면서 내부 상태 모델은 중간 단계를 전혀 표현하지 않는 경우
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경과 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행을 따로 처리해, DB는 커밋됐는데 이벤트는 유실되는 경우

기술사 관점에서 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)의 핵심 판단은 이것이다. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/">사가</a>는 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/">ROLLBACK</a> 기술이 아니라, 실패를 전제로 한 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">RECOVERY</a> 설계</strong>라는 점이다. 이 관점이 없으면 구현은 이벤트 기반이어도 운영은 수작업 정정에 의존하게 된다.

- **📢 섹션 요약 비유**: 여행 예약을 여러 사이트에서 따로 했을 때, 한 곳이 실패하면 다른 예약도 취소 전화를 돌려 정리하는 것과 같다. 한 번에 되돌아가지는 않지만, 정리 순서를 잘 설계하면 결국 처음 의도한 상태로 수습할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)의 가장 큰 효과는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립성과 확장성을 유지하면서도, 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 걸친 업무 흐름을 통제 가능한 형태로 만들 수 있다는 점이다. 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 스스로 커밋하고, 전체 업무는 이벤트와 보상으로 엮인다. 그 결과 전역 락과 중앙 XA 자원 관리자에 대한 의존을 줄이면서도 대규모 MSA에 맞는 정합성 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 확보할 수 있다.

하지만 대가도 있다. 중간 상태를 수용해야 하고, 보상 로직을 별도로 설계해야 하며, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 유실·중복·순서 문제까지 운영 차원에서 다뤄야 한다. 따라서 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 단순히 "[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 대신 이벤트를 쓴다"는 선택이 아니라, <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>의 형태를 강한 동기식 정합성에서 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 가능한 비동기 정합성으로 바꾸는 아키텍처 전환</strong>이다.

결론적으로 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 "[분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)을 쉽게 만드는 방법"이 아니라, <strong>전역 커밋이 어려운 현실에서 비즈니스적으로 수습 가능한 흐름을 설계하는 방법</strong>으로 기억해야 한다. 핵심 질문은 "어떻게 한 번에 커밋할까"가 아니라, "어디서 실패해도 어떻게 끝까지 정리할까"다.

- **📢 섹션 요약 비유**: 좋은 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 넘어지지 않는 줄타기가 아니라, 넘어져도 안전망과 복귀 동선을 미리 짜 둔 공연과 같다. 완벽한 무실패보다, 실패했을 때 끝까지 수습할 수 있는 설계가 더 중요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자기 저장소 안에서 확실히 커밋하는 최소 단위 |
| [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)) | 실패 시 이전 성공 단계를 업무적으로 상쇄하는 반대 동작 |
| 최종적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | 잠시 불일치가 있어도 결국 수렴하도록 만드는 정합성 모델 |
| [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) | [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)와 대비되는 강한 전역 커밋 방식 |
| 코레오그래피 (Choreography) | 이벤트 중심으로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 제어 방식 |
| [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) ([Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)) | 중앙 조정자가 흐름을 통제하는 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 제어 방식 |
| [트랜잭셔널 아웃박스](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)) | 로컬 커밋과 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행 정합성을 잇는 실무 기법 |
| [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 재시도와 중복 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 처리의 안전장치 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비즈니스 요청 발생</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">로컬 트랜잭션 1 커밋</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">이벤트 / 명령으로 다음 단계 전달</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">로컬 트랜잭션 연쇄 실행</div>
<div class="kb-diagram-tree-item" style="--depth:4">실패 발생 -&gt; 보상 트랜잭션 역순 실행</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">최종적 일관성 수렴</div>
</div>
</div>



이 흐름은 "업무 요청 → 로컬 커밋 연쇄 → 실패 시 보상 → 최종 상태 수렴"이라는 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)의 운영 사고방식을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구들이 함께 큰 성을 짓는데, 각자 맡은 방을 먼저 만들고 다음 친구에게 넘겨줘요.
2. 중간에 누가 못 하게 되면, 앞에서 만든 친구들이 자기 방을 다시 치워서 전체 모양을 맞춰요.
3. 그래서 한 번에 모두 멈춰 서 있기보다, 움직이면서 문제가 생기면 뒤에서 정리하는 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 175 / 482

← **이전**: [174. 분산 트랜잭션 한계 및 2PC (Two-Phase Commit) 배제 이유 - 블로킹 오버헤드](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/174_distributed_transaction_2pc_limit/)
**다음**: [176. 코레오그래피 사가 (Choreography Saga) - 중앙 통제 없이 각 서비스가 비동기 이벤트를 발행/구독 (Pub/Sub,](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/176_choreography_saga_pub_sub/) →

---
