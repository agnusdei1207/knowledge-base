---
title: "176. Choreography Saga Pub Sub"
date: "2026-05-06"
tags:
  - "studynote-enterprise-systems"
weight: 176
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/) ([Choreography Saga](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/))는 중앙 오케스트레이터 없이, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)을 커밋한 뒤 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트를 발행하고 다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이를 구독해 흐름을 이어 가는 [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 조정 방식이다.
> 2. **가치**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성과 확장성을 높이고 중앙 제어기의 병목이나 [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure)를 줄이면서도, 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 기반의 업무 흐름을 만들 수 있다.
> 3. **판단 포인트**: 이 방식은 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)), [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)), 상관관계 ID, 관측성 없이는 곧 이벤트 스파게티가 되므로, 짧고 안정적인 흐름에 우선 적용하는 편이 안전하다.

---

## Ⅰ. 개요 및 필요성

[코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))에서 하나의 비즈니스 요청이 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 건너갈 때, 이를 중앙 지휘 서버 없이 어떻게 일관되게 끝낼지 다루는 패턴이다. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 저장소 안에서는 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)을 짧게 커밋하고, 그 결과를 이벤트로 외부에 알린다. 다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 그 이벤트를 구독해 자기 업무를 수행하고 다시 새로운 이벤트를 낸다.

이 방식이 필요한 이유는 전통적인 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 MSA와 잘 맞지 않기 때문이다. 주문, 결제, 재고, 배송이 서로 다른 저장소를 쓰는 상황에서 [2PC](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) 같은 강한 동기식 조정은 락 지속시간, 장애 전파, 운영 복잡도를 키운다. 그렇다고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들을 동기 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)) 체인으로 엮으면 앞단 장애가 뒷단까지 연쇄 전파되고, 호출 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도 빠르게 복잡해진다.

[코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 여기서 한 걸음 비틀어 생각한다. <strong>다음 단계를 직접 호출하지 말고, "무슨 일이 일어났는지"를 이벤트로 알리자</strong>는 것이다. 그러면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들은 서로의 위치나 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 내부를 몰라도 같은 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)를 통해 느슨하게 협력할 수 있다.

아래 그림은 중앙 조정자 없이 이벤트만으로 주문 흐름이 이어지는 모습을 보여 준다.

```text
+--------------------------------------------------------------------+
| Choreography Saga by domain events                                |
+--------------------------------------------------------------------+
| Order Service  -- OrderCreated ---> Event Bus                     |
|                                  |                                |
|                                  +-> Payment Service              |
|                                  |      +- PaymentApproved ------>|
|                                  |                                |
|                                  +-> Inventory Service            |
|                                         +- StockReserved -------->|
|                                                                    |
| No central conductor; each service reacts to business events      |
+--------------------------------------------------------------------+
```

따라서 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)의 필요성은 "비동기라서 멋있다"가 아니다. <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간 직접 의존을 줄이면서도, <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>된 업무를 끝까지 이어 갈 수 있는 자율 협업 규칙</strong>이 필요하기 때문에 등장한다.

- **📢 섹션 요약 비유**: 무대 뒤에서 감독이 한 명씩 지시하는 대신, 배우들이 음악 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 듣고 자기 차례에 맞춰 스스로 등장하는 공연과 같다. 중앙 지시는 줄지만, 각 배우가 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 정확히 이해해야 공연이 끊기지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)의 구조는 단순히 "이벤트를 쓴다"로 끝나지 않는다. 핵심 구성은 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/), 이벤트 브로커, 이벤트 핸들러, 보상 이벤트, 그리고 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행 누락을 막는 아웃박스 패턴이다. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 반영과 이벤트 발행을 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 이어 붙여야 하고, 구독자는 중복 수신과 순서 뒤바뀜까지 견딜 수 있어야 한다.

| 구성 요소 | 역할 | 왜 중요한가 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부 상태 변경 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립성 유지 | 짧고 명확한 커밋 경계 |
| [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 | 다음 단계의 촉발 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 직접 호출 없이 흐름 연결 | 과거형 이름, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| [Event Bus](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/) | 발행/구독 전달 통로 | 느슨한 결합 유지 | 재시도, 순서, DLQ (Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) |
| 보상 이벤트 | 실패를 외부에 알리고 상쇄 동작 유도 | 전역 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 부재 보완 | 역순 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 멱등 처리 |
| Outbox | [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 반영과 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행 사이의 틈 보완 | 유실 방지 | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)/[CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) 연계 |

실행 흐름은 보통 다음과 같다. 주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 `OrderCreated`를 저장하고 아웃박스에 함께 기록한다. 릴레이 프로세스가 이를 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)로 발행하면, 결제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이벤트를 읽고 결제를 승인한 뒤 `PaymentApproved`를 다시 발행한다. 재고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 이 이벤트를 구독해 재고를 예약하고, 이어 배송 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 출고를 준비한다. 어느 단계에서 실패하면 `PaymentFailed`, `StockRejected` 같은 실패 이벤트가 발행되고, 앞선 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들은 이를 보고 취소나 해제를 수행한다.

```text
+--------------------------------------------------------------------+
| Forward flow and compensation                                      |
+--------------------------------------------------------------------+
| Order database commit + Outbox(OrderCreated)                       |
|                  |                                                 |
|                  v                                                 |
|               Event Bus                                            |
|                  |                                                 |
|                  +-> Payment Service -> PaymentApproved            |
|                  |                                                 |
|                  +-> Payment Service -> PaymentFailed              |
|                                         |                          |
|                                         +-> OrderCancelled         |
|                                             InventoryReleased      |
+--------------------------------------------------------------------+
```

중요한 점은 보상이 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) ROLLBACK이 아니라는 사실이다. 이미 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 로컬 커밋은 끝났으므로, 실패가 나면 반대 의미의 새 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 실행해 상태를 상쇄해야 한다. 따라서 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)의 설계 핵심은 "성공 이벤트 설계"만이 아니라 <strong>실패 이벤트와 보상 경로를 업무적으로 모델링하는 것</strong>이다.

또한 관측성이 매우 중요하다. 중앙 오케스트레이터가 없기 때문에 전체 흐름은 상관관계 ID와 [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 사실상 유일한 실마리가 된다. 이 장치가 약하면 장애가 났을 때 "누가 어떤 이벤트를 언제 소비했는가"를 찾기 어렵다.

- **📢 섹션 요약 비유**: 각 상점이 영수증과 메모를 함께 남기고 다음 가게에 전달하는 릴레이 장사와 같다. 메모가 빠지면 다음 가게는 움직이지 못하고, 취소 메모가 늦으면 이미 끝난 계산을 뒤늦게 다시 정리해야 한다.

---

## Ⅲ. 비교 및 연결

[코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)를 제대로 이해하려면 [오케스트레이션 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/552_orchestration_saga_centralized_control/), 단순 이벤트 알림, 동기 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 체인과 구분해야 한다. 모두 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 연결하지만, <strong>누가 흐름을 알고 있는가</strong>가 다르다.

| 방식 | 제어 주체 | 장점 | 약점 | 잘 맞는 상황 |
| :--- | :--- | :--- | :--- | :--- |
| [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/) | 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이벤트를 보고 자율 반응 | [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 낮음, 중앙 병목 감소 | 흐름 가시성 낮음, 이벤트 확산 | 3~5단계 내외의 안정적 비즈니스 흐름 |
| [오케스트레이션 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/552_orchestration_saga_centralized_control/) | 중앙 오케스트레이터 | 추적과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 통제 용이 | 중앙 로직 비대화 가능 | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·승인·장기 흐름 |
| 동기 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 체인 | 앞단 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 직접 호출 | 이해가 직관적 | 장애 전파, 강한 결합 | 짧고 단순한 내부 호출 |

코레오그래피는 느슨한 결합 면에서 강하지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 늘고 분기 조건이 많아질수록 "누가 어떤 이벤트를 듣는가"가 코드 밖에서 잘 보이지 않게 된다. 이때부터는 이벤트 스파게티, 숨은 의존성, 예측 어려운 재시도 폭주가 생기기 쉽다. 반대로 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)은 흐름을 한곳에서 볼 수 있지만, 중앙 조정 로직이 너무 많은 업무 규칙을 품으면 새로운 병목이 될 수 있다.

또한 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) ([Domain-Driven Design](/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/))의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트, [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command Query Responsibility Segregation](/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/)), [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)와 자주 함께 등장한다. 이유는 단순하다. 이벤트 중심 흐름은 결국 "상태 변화의 의미"를 명확히 정의해야 하고, 중복·재시도·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 견디려면 읽기 모델과 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/) 모델을 분리해 설계하는 편이 유리하기 때문이다.

즉 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 단순 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 패턴이 아니라, <strong>업무 의미를 이벤트로 표현하고 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 경계를 느슨하게 유지하려는 아키텍처 선택</strong>이다. 그래서 기술 선택보다 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계와 운영 성숙도가 먼저 중요하다.

- **📢 섹션 요약 비유**: 자유로운 재즈 합주는 연주자 개개인의 자율성을 살리지만, 곡이 길고 변주가 많아질수록 누가 언제 들어와야 하는지 놓치기 쉽다. 반면 지휘자가 있는 오케스트라는 통제가 쉬운 대신 중앙 악보에 더 크게 의존한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 주문 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 포인트 적립, 쿠폰 차감, 결제 승인, 재고 예약처럼 <strong>여러 팀이 소유한 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>를 느슨하게 이어야 하는 짧은 흐름</strong>에서 특히 유효하다. 각 팀이 자기 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 이벤트 핸들러만 관리하면 되므로 배포 독립성이 높고, 새로운 후속 기능도 구독자로 붙이기 쉽다. 예를 들어 주문 완료 후 [추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)이 `OrderCompleted`를 구독해 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 적재하는 식의 확장이 자연스럽다.

하지만 모든 [사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)를 코레오그래피로 밀어 넣으면 곧 한계가 온다. 분기 규칙이 많고, 사람이 개입하는 승인 절차가 있고, 규제 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)로 전체 타임라인을 한눈에 보여 줘야 한다면 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)이 더 낫다. 실패 보상이 복잡한 금융 업무나 장시간 지속되는 배송·정산 흐름도 마찬가지다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 전체 흐름이 짧고 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 의미가 안정적으로 정의돼 있는가?
2. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 멱등 소비와 중복 이벤트 재처리를 안전하게 지원하는가?
3. [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 반영과 이벤트 발행을 아웃박스 등으로 확실히 연결했는가?
4. 상관관계 ID, [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리가 준비돼 있는가?
5. 실패 시 보상 이벤트와 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 처리 절차가 명확한가?
6. 흐름이 길거나 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 요구가 강하다면 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)이 더 적합하지 않은가?

### 자주 나오는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 상대 API를 직접 호출하면서 동시에 이벤트도 발행해 흐름 책임이 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)되는 경우
- `OrderCreated` 같은 이벤트 이름은 있으나 보상 이벤트와 상태 모델은 없는 경우
- 같은 이벤트를 두 번 처리했을 때 중복 결제·중복 적립이 발생하는 경우
- 중앙 추적 장치 없이 "이벤트가 잘 가겠지"라고 낙관하는 경우
- 소비자가 너무 많아졌는데도 이벤트 계약 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리를 하지 않는 경우

기술사 답안에서는 장점만 강조하면 부족하다. [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 분명 자율성과 확장성에 강하지만, 그 대가로 추적성과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 통제를 잃기 쉽다. 따라서 채택 기준을 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 자율성 우선인가, 전체 흐름 통제가 우선인가</strong>로 분명히 나눠 설명해야 한다.

- **📢 섹션 요약 비유**: 작은 동네 축제는 서로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보며 유연하게 움직여도 되지만, 수만 명이 모이는 국제 행사는 중앙 관제실이 필요하다. 코레오그래피는 규모와 규칙이 맞을 때 가장 아름답다.

---

## Ⅴ. 기대효과 및 결론

[코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)가 잘 작동하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들은 서로를 직접 붙잡지 않고도 하나의 비즈니스 흐름을 완성할 수 있다. 그 결과 팀 자율성, 배포 독립성, 확장성이 높아지고 중앙 조정자의 장애가 전체 업무를 멈추는 위험도 줄어든다. 새로운 후행 기능을 추가할 때도 기존 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 크게 바꾸지 않고 구독자만 늘려 확장하기 쉽다.

그러나 한계 또한 구조적이다. 이벤트 흐름이 눈에 잘 보이지 않고, 실패 원인을 추적하기 어렵고, 계약 변경이 숨은 연쇄 영향을 만들 수 있다. 따라서 이벤트 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 추적 도구, 재처리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 수동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 함께 갖춰져야 한다.

앞으로는 많은 조직이 순수 코레오그래피나 순수 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 중 하나만 고집하기보다, 짧은 흐름은 코레오그래피로 두고 장기·고위험 흐름은 워크플로 엔진으로 분리하는 하이브리드 구조를 택할 가능성이 크다. 결론적으로 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)는 <strong>이벤트로 스스로 이어지는 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 업무 안무</strong>로 기억하면 된다. 다만 안무가 아름다우려면 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자기 박자와 실패 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 규칙을 정확히 알고 있어야 한다.

- **📢 섹션 요약 비유**: 감독 없는 춤이 잘 맞으면 아주 유연하고 자연스럽지만, 박자를 잃으면 누가 먼저 틀렸는지 찾기 어려워진다. 자유를 얻는 대신 합을 맞추는 규칙을 더 엄격히 지켜야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 ([Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Event) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 상태 변화를 외부에 알리는 코레오그래피의 기본 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)) | [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 커밋과 이벤트 발행 간 정합성 문제를 줄이는 실무 기법 |
| [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 재시도와 중복 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 상황에서도 결과를 안정적으로 유지하는 조건 |
| 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | 즉시 일치 대신 시간이 지나 수렴하는 정합성 모델 |
| [보상 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Compensating Transaction](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)) | 실패 이후 이전 성공 단계를 업무적으로 상쇄하는 동작 |
| 상관관계 ID (Correlation ID) | 중앙 제어기 없이도 전체 이벤트 흐름을 추적하게 해 주는 열쇠 |
| [오케스트레이션 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/552_orchestration_saga_centralized_control/) | 코레오그래피와 대비되는 중앙 통제형 [사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
Business command accepted
        |
        v
Local transaction + outbox write
        |
        v
Publish to event bus
        |
        v
Subscriber local transaction
        |
        +--------------► failure event -> compensation chain
        v
Next domain event
        |
        v
Eventual consistency reached
```

이 흐름도는 "업무 요청 수락 -> 로컬 커밋 -> 이벤트 발행 -> 다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 반응 -> 실패 시 보상 -> 최종 상태 수렴"이라는 [코레오그래피 사가](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)의 전형적 리듬을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 한 명이 "주문했어!"라고 말하면, 다른 친구들이 그 소리를 듣고 각자 자기 일을 시작해요.
2. 중간에 누가 "못 하겠어!"라고 말하면, 앞에서 했던 친구들이 그 말을 듣고 다시 정리해요.
3. 그래서 선생님이 한 명씩 시키지 않아도, 약속된 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)만 잘 들으면 함께 큰 일을 끝낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 176 / 482

<- **이전**: [175. 사가 패턴 (Saga Pattern) - 로컬 트랜잭션 연쇄와 보상 트랜잭션으로 최종적 일관성 보장](/studynote/07_enterprise_systems/03_eai_esb_msa/175_saga_pattern_eventual_consistency/)
**다음**: [177. 오케스트레이션 사가 (Orchestration Saga) - 중앙 오케스트레이터(컨트롤러)가 전체 트랜잭션 흐름을 룰 엔진처럼](/studynote/07_enterprise_systems/03_eai_esb_msa/177_orchestration_saga_controller/) ->

---
