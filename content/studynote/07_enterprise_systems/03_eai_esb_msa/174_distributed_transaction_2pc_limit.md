+++
title = "174. 분산 트랜잭션 한계 및 2PC (Two-Phase Commit) 배제 이유 - 블로킹 오버헤드"
date = 2026-05-06

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))는 여러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소에 걸친 변경을 하나의 원자적 커밋처럼 보이게 만들기 위해, 참여자 전원에게 **준비(Prepare)와 최종 결정(Commit/[Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))** 을 강제하는 동기식 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 커밋 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.
> 2. **가치**: 참여 자원이 동일하고 네트워크가 안정적이며 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 짧다면, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계를 넘는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업에도 강한 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/))을 부여할 수 있다.
> 3. **판단 포인트**: [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 와 클라우드 환경에서는 락 점유, 블로킹, 조정자 의존성, 이기종 자원 비호환 때문에 비용이 너무 커서, [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/))·아웃박스·[보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)이 더 현실적인 대안이 된다.

---

## Ⅰ. 개요 및 필요성

[분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)은 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)나 여러 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 걸친 변경을 하나의 업무 단위로 묶고 싶을 때 등장한다. 예를 들어 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 주문을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 승인 상태를 기록하며, 재고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 수량을 차감해야 한다. 이 세 단계 중 하나만 성공하고 나머지가 실패하면 업무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 바로 불일치 상태가 된다.

단일 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 안에서는 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)으로 이 문제를 다룰 수 있다. 하지만 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 자기 저장소를 가지는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 에서는 "모두 성공하거나 모두 취소"를 자연스럽게 보장해 주는 전역 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계가 사라진다. 여기서 등장한 고전적 해법이 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 다.

[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 출발점은 명확하다. **참여자 전원이 확실히 준비되었는지 먼저 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤, 그 다음에만 최종 커밋을 허용하자**는 것이다. 이 사고는 이론적으로 깔끔하지만, 준비 후 최종 결정 전까지 모두가 기다려야 한다는 대가를 함께 안고 들어온다.

- **📢 섹션 요약 비유**: 친구 셋이 카드로 공동 결제할 때 "모두 결제 준비됐지? 한 명이라도 안 되면 전부 취소!"라고 외치는 방식과 같다. 깔끔해 보이지만, 한 명이 휴대폰을 떨어뜨리는 순간 나머지 둘도 계산대 앞에서 꼼짝없이 기다려야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 보통 **조정자 ([Coordinator](/knowledge-base/studynote/05_database/04_transactions_concurrency/250_coordinator_participant_2pc_roles/)) + 참여자 (Participant)** 구조로 동작한다. 조정자는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 참여자들에게 먼저 준비 여부를 묻고, 전원이 준비 완료라고 응답해야만 최종 커밋을 명령한다. 참여자는 Prepare 단계에서 로컬 변경을 디스크 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 남기고, 관련 자원을 잠근 채 최종 명령을 기다린다.

| 단계 | 조정자 동작 | 참여자 동작 | 시스템 대가 |
| :--- | :--- | :--- | :--- |
| Prepare | "커밋 가능?" 투표 요청 전송 | 로컬 작업 수행 후 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기록, 락 유지, Yes/No 응답 | 응답 대기 동안 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 |
| Decision | 전원 Yes 면 Commit, 하나라도 No 면 [Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) 결정 | 결정 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 수신 대기 | 조정자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 전체 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 전파 |
| Completion | 최종 결과 통보 및 종료 | Commit/[Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) 후 락 해제 | 네트워크 실패 시 재전송·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 필요 |

아래 그림은 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 핵심 문제를 보여 준다. Prepare 이후에는 참여자가 스스로 결정을 내릴 수 없기 때문에, 조정자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이나 장애가 곧 **블로킹 구간**이 된다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                 Two-Phase Commit blocking window                   │
├────────────────────────────────────────────────────────────────────┤
│ Coordinator : prepare? ---> wait votes ---> COMMIT / ABORT        │
│                     │                    ▲                         │
│ Order DB    : lock row + YES ============┘                         │
│ Payment DB  : lock row + YES ============┘                         │
│ Inventory DB: lock row + YES ============┘                         │
│                                                                    │
│ If coordinator fails after all YES:                                │
│ participants stay in uncertain state and keep waiting              │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 Prepare 단계가 "검사"가 아니라 거의 커밋 직전 상태라는 점이다. 참여자는 이미 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능한 최소 단위를 넘어 로컬 자원을 잡아 두고, 최종 명령을 기다린다. 따라서 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 길어질수록 락 경쟁, [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 저하, 사용자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 함께 커진다.

이 때문에 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 짧고 통제된 내부 시스템에서는 성립할 수 있지만, [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)과 자원 다양성이 큰 환경에서는 급격히 부담스러워진다. 다시 말해 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 본질은 "전역 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)"이 아니라, **전역 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)을 위해 모두를 잠시 세워 두는 메커니즘**이다.

- **📢 섹션 요약 비유**: 출발선에서 심판 총소리를 기다리는 육상 경기와 같다. 모두가 자세를 잡고 멈춰 서 있는 동안에는 질서가 유지되지만, 총이 늦게 울리면 선수들은 그만큼 오래 긴장한 채 서 있어야 한다.

---

## Ⅲ. 비교 및 연결

[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 한계를 제대로 이해하려면 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/), [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/), TCC (Try-Confirm-Cancel) 와 비교해야 한다. 이들은 모두 "여러 단계를 어떻게 일관되게 관리할 것인가"에 답하지만, 락을 다루는 방식과 실패 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 철학이 다르다.

| 비교 축 | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) | [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) | TCC |
| :--- | :--- | :--- | :--- | :--- |
| 적용 범위 | 단일 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·단일 저장소 | 다중 저장소·다중 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 비즈니스 흐름 | 예약 가능한 자원 흐름 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 최종적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 단계적 강한 제어 |
| 락 유지 | 짧음 | 준비 후 최종 결정까지 길어질 수 있음 | 보통 없음 | Try 단계에서 자원 예약 |
| 실패 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 조정자·참여자 재조정 필요 | [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) | Confirm/Cancel 호출 |
| 잘 맞는 환경 | 모놀리식 업무 | 통제된 내부 시스템 | 클라우드 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), 비동기 이벤트 | 좌석·재고 예약형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 에서 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 가 기피되는 이유는 단순히 느려서가 아니다. 첫째, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 네트워크 홉이 늘수록 Prepare/Commit 왕복 비용이 누적된다. 둘째, [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), 캐시, [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 저장소처럼 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 친화적이지 않은 자원이 섞이면 전체 설계가 제한된다. 셋째, 조정자가 병목이 되거나 장애 지점이 되면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립성 자체가 흔들린다.

반면 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)을 먼저 확정하고, 실패 시 보상 작업으로 되돌리는 방식을 택한다. 이 구조는 중간에 잠깐 불일치 상태가 생길 수 있지만, 블로킹 없이 더 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 확장성을 얻는다. 따라서 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 에서는 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 를 "정합성의 정답"이 아니라, **강한 정합성을 얻는 대신 독립성과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 희생하는 선택지**로 봐야 한다.

- **📢 섹션 요약 비유**: [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 모두 손을 꼭 잡고 함께 다니는 행진이고, [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 각자 먼저 움직이되 문제가 생기면 다시 제자리로 돌아오는 약속이다. 전자는 질서가 강하지만 느리고, 후자는 유연하지만 사후 정리가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 를 검토해도 되는 경우는 의외로 좁다. 같은 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 안의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) (RDBMS, Relational [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System) 들이 짧은 업무 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 처리하고, 참여자 수가 적으며, 운영팀이 중앙 조정자와 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차를 강하게 통제할 수 있을 때 정도다. 배치성 재무 정산처럼 "무조건 같이 반영되어야 한다"는 요구가 매우 강한 경우가 대표적이다.

반대로 전자상거래 주문·결제·배송처럼 외부 응용 프로그래밍 인터페이스 ([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), 재시도, 사용자 대기 시간이 얽힌 흐름에는 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 가 잘 맞지 않는다. 사용자가 모바일 앱에서 결제 버튼을 누르고 몇 초 동안 전체 참여자가 락을 잡은 채 기다리는 구조는 확장성과 장애 격리 모두에 불리하다. 이 경우에는 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) + [트랜잭셔널 아웃박스](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) + [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 보상 흐름이 일반적으로 더 현실적이다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 참여 자원이 모두 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 또는 X/Open XA 를 안정적으로 지원하는가?
2. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 사람 개입 없이 수백 밀리초~수초 안에 끝나는 짧은 흐름인가?
3. [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)과 장애가 작고, 중앙 조정자를 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있게 운영할 수 있는가?
4. 실패 시 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)보다 즉시 원자 커밋이 정말 더 중요한가?
5. [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), 캐시, 외부 결제사처럼 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 밖의 자원이 업무 핵심에 포함되어 있지 않은가?
6. 교차 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 락 점유로 인한 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 저하를 수용할 수 있는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 까지 한 번에 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 로 묶으려는 경우
- 사용자 승인 대기처럼 긴 업무를 Prepare 상태로 오래 끌고 가는 경우
- 교차 리전, 교차 클라우드 환경에서 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 로 저지연을 기대하는 경우
- 보상 설계를 회피하려고 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 를 "만능 해결책"처럼 도입하는 경우

기술사 관점에서 중요한 판단은 이것이다. **[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 불가능해서 버리는 기술이 아니라, 클라우드형 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 요구하는 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·독립성·[처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 너무 자주 충돌하기 때문에 의식적으로 배제되는 기술**이다.

- **📢 섹션 요약 비유**: 중요한 서류에 모두가 동시에 도장을 찍는 절차는 엄격하고 안전하지만, 사람 수가 많아질수록 회의실 예약과 대기 시간이 더 큰 문제가 된다. 그래서 현대 조직은 꼭 필요한 문서에만 전원 서명을 요구하고, 나머지는 책임자별 승인으로 나눠 처리한다.

---

## Ⅴ. 기대효과 및 결론

[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 가장 큰 장점은 분명하다. 여러 저장소에 걸친 변경을 하나의 원자적 결정처럼 보이게 만들어, 회계나 재무처럼 강한 정합성이 핵심인 업무에서 설계 설명이 단순해진다. 이 점에서 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 여전히 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 이론의 기준점이다.

하지만 현대 엔터프라이즈 시스템에서는 그 대가가 너무 자주 크게 나타난다. 락 유지 시간 증가, 조정자 병목, 장애 시 불확실 상태, 이기종 자원 비지원이 대표적이다. 그래서 실제 아키텍처는 전역 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)보다 **[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 로컬 정합성과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능한 업무 흐름** 쪽으로 이동해 왔다.

결론적으로 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 를 기억하는 가장 정확한 관점은 "완벽한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)"이 아니라, **강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 얻기 위해 시스템 전체를 동기식으로 묶는 비용 구조**다. [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 시대의 핵심 질문은 "[2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 를 쓸 수 있는가?"보다 "정말 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 가 필요한가?"다.

- **📢 섹션 요약 비유**: [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 는 모두가 동시에 문을 잠그고 열쇠를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 출발할 수 있는 규율 강한 여행이다. 절대 흩어지지 않는 대신, 한 명만 늦어도 모두가 그 자리에서 멈춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 조정자 ([Coordinator](/knowledge-base/studynote/05_database/04_transactions_concurrency/250_coordinator_participant_2pc_roles/)) | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 의 Prepare·Commit 결정을 중앙에서 관리하는 주체 |
| 참여자 (Participant) | 로컬 자원을 잠그고 Yes/No 투표를 수행하는 자원 관리자 |
| ACID | 단일 저장소의 강한 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 개념으로, [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 확장하려는 대상 |
| [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/)) | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 대신 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)과 보상 흐름으로 정합성을 맞추는 대안 |
| [트랜잭셔널 아웃박스](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경과 이벤트 발행 사이의 정합성을 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)으로 보장하는 기법 |
| [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 재시도와 보상 처리를 안전하게 만들기 위한 핵심 성질 |
| TCC (Try-Confirm-Cancel) | 예약 가능한 자원을 명시적으로 다루는 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
Single database local transaction
              │
              ▼
Database per service and distributed write problem
              │
              ▼
2PC for atomic commit across participants
              │
              ▼
Blocking, coordinator dependency, heterogeneous limits
              │
              ▼
Saga / outbox / idempotent recovery patterns
```

이 흐름은 "단일 저장소 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) → [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리 → 전역 커밋 필요 → [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 도입 → 블로킹 한계 → 비동기 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 패턴"으로 이어지는 아키텍처 진화를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구들이 같이 보물상자를 열 때, 모두가 "준비됐어!"라고 말해야만 뚜껑을 여는 규칙이 2PC예요.
2. 그런데 한 친구가 대답을 늦게 하면 다른 친구들은 손을 잡은 채 계속 기다려야 해요.
3. 그래서 요즘은 각자 먼저 움직이고, 문제가 생기면 다시 정리하는 다른 방법도 많이 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 174 / 482

← **이전**: [173. 데이터베이스 퍼 서비스 (Database per Service)](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/173_database_per_service/)
**다음**: [175. 사가 패턴 (Saga Pattern) - 로컬 트랜잭션 연쇄와 보상 트랜잭션으로 최종적 일관성 보장](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/175_saga_pattern_eventual_consistency/) →

---
