+++
title = "190. 이벤트 기반 아키텍처 (Event-Driven Architecture, EDA) - 비동기 Publish/Subscribe"
date = 2026-05-08

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [이벤트 기반 아키텍처](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/) ([Event-Driven Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/), [EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/))는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 상대방을 직접 호출해 명령하는 대신, 자신에게 일어난 상태 변화를 이벤트로 발행하고 관심 있는 소비자가 이를 비동기로 처리하게 만드는 느슨한 결합 구조다.
> 2. **가치**: 생산자와 소비자의 생명주기와 처리 속도를 분리하므로, 장애 격리·탄력 확장·다중 후속 처리에 강하고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 연쇄 대기를 크게 줄인다.
> 3. **판단 포인트**: EDA는 결국 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 중복 처리, 추적 복잡성을 받아들이는 선택이므로, 이벤트 계약·재처리·[멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 없이는 오히려 운영 난도가 더 높아질 수 있다.

---

## Ⅰ. 개요 및 필요성

EDA는 시스템 내부의 중요한 상태 변화를 이벤트라는 사실 형태로 외부에 알리고, 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이를 독립적으로 구독해 처리하는 아키텍처다. 이 방식이 필요한 이유는 전통적인 동기 호출 체인이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 늘수록 장애 전파와 응답 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 확대하기 때문이다. 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 결제, 재고, 알림, 분석 시스템을 순서대로 직접 호출하면, 가장 느린 하위 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 전체 사용자 경험을 결정하게 된다.

특히 [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)에서는 서로 다른 팀이 각자 배포 일정을 가지므로, 강한 시간 결합이 운영 병목으로 이어진다. EDA는 "상대가 지금 살아 있는가"보다 "이 사실을 브로커에 안전하게 기록했는가"에 초점을 맞춘다. 즉 생산자는 이벤트를 남기고 빠르게 자신의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 끝내며, 후속 처리는 각 소비자의 속도와 장애 상황에 맞춰 흘러간다.

- **📢 섹션 요약 비유**: 누군가에게 직접 전화를 돌리는 대신, 공용 게시판에 중요한 공지를 붙여 두고 필요한 사람이 각자 와서 읽게 하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EDA의 핵심 구성은 생산자, 이벤트 브로커, 토픽 또는 큐, 소비자, 재처리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 생산자는 보통 업무 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 끝나는 시점에 이벤트를 발행하고, 브로커는 이를 내구성 있게 저장해 소비자가 가져가도록 만든다. 소비자는 이벤트를 읽어 자신의 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 갱신하거나 외부 알림, 분석 적재, 후속 워크플로를 수행한다.

아래 그림은 전형적인 퍼블리시/서브스크라이브 흐름을 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Event propagation through broker</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Order Service -- publish OrderPlaced --&gt; Broker Topic</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Inventory Consumer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Payment Consumer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Notification Consumer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trace ID / key / schema version travel with the event</div></div>
</div>
</div>



| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 생산자 (Producer) | 상태 변화 이벤트 발행 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 이벤트 발행의 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 보장 필요 |
| 브로커 (Broker) | 이벤트 저장과 전달 | 보존 기간, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), 순서 보장 범위 설계 |
| 이벤트 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | 소비자 간 계약 | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리와 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 중요 |
| 소비자 (Consumer) | 이벤트 기반 후속 처리 | [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/), 재시도, 장애 격리 필요 |
| 재처리 경로 | 실패 이벤트 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | Dead Letter [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/), 재시도, 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 |

EDA에서 중요한 원리는 이벤트를 "사실"로 다루는 것이다. `OrderPlaced`는 이미 발생한 상태 변화이므로 보통 불변이며, 나중에 수정이 필요하면 `OrderCancelled`처럼 새로운 이벤트를 발행한다. 또한 실무에서는 아웃박스 패턴 (Outbox Pattern)을 사용해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장과 이벤트 발행 사이의 유실 위험을 줄이는 경우가 많다.

- **📢 섹션 요약 비유**: 한 부서가 일을 끝냈다는 사실을 방송실에 남기면, 필요한 부서들이 자기 차례에 맞춰 방송을 듣고 각각 행동하는 것과 같다.

---

## Ⅲ. 비교 및 연결

EDA는 동기 요청-응답과 다르며, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐와도 목적이 조금 다르다. 동기 응용 프로그램 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))는 즉시 결과가 필요할 때 강력하지만, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 장애가 직접 연결된다. 반면 EDA는 후속 처리의 분기와 확장에 유리하지만, 모든 시스템이 같은 시점에 같은 상태를 보는 것은 포기해야 한다. [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐가 "한 작업자를 위한 일감 전달"에 가깝다면, 퍼블리시/서브스크라이브는 "여러 소비자를 위한 사실 전파"에 가깝다.

| 비교 대상 | 강점 | 한계 | 잘 맞는 상황 |
| :--- | :--- | :--- | :--- |
| 동기 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 즉시 응답과 단순한 흐름 | 연쇄 장애와 대기 증가 | 조회, 즉시 승인, 사용자 상호작용 |
| 작업 큐 | 비동기 처리와 백프레셔 | 다중 소비자 확장성은 제한적 | 배치 작업, 단일 후속 처리 |
| [EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/) Pub/Sub | 다중 소비자, 확장성, 느슨한 결합 | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 운영 복잡성 | 주문 후속 처리, 알림, 분석, 통합 이벤트 |

EDA는 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/)), [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/)), 명령 질의 책임 분리 ([Command Query Responsibility Segregation](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/), [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)), [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)과 자주 연결된다. 예를 들어 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)는 이벤트를 통해 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)을 이어 가고, CQRS는 읽기 모델을 비동기 이벤트로 갱신한다. 따라서 EDA는 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 기술이 아니라, <strong>시스템을 상태 변화 중심으로 조직하는 사고방식</strong>에 가깝다.

- **📢 섹션 요약 비유**: 직접 손을 잡고 줄지어 움직이는 행진보다, 무전 방송을 듣고 각 팀이 자기 자리에서 동시에 움직이는 운영 방식에 더 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 이벤트 이름, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키, 재시도 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 먼저 정해야 한다. 이벤트는 `SendNotification` 같은 명령형보다 `OrderPlaced`, `PaymentFailed` 같은 사실형 이름이 적합하며, 소비자는 같은 이벤트를 두 번 받아도 결과가 망가지지 않도록 멱등하게 구현해야 한다. 또한 장애 시 재시도만 반복하면 독성 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지가 전체 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 막을 수 있으므로 데드 레터 큐 (Dead Letter [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/), DLQ)와 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 필요하다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이벤트 발행이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장과 분리되어 유실될 가능성이 있다면 아웃박스 패턴 등 보완책이 있는가?
2. 소비자가 중복 이벤트를 받아도 안전하도록 멱등 키, 상태 체크, 업서트 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 준비되어 있는가?
3. 이벤트 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
4. 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 사용자 경험과 업무 규칙 측면에서 수용할 수 있는가?
5. 브로커, 소비자, DLQ, 추적 시스템까지 포함한 운영 관측성이 갖춰져 있는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 이벤트라는 이름으로 사실상 원격 프로시저 호출을 흉내 내는 구조
- 재처리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 없이 소비자 로직만 구현해 장애 시 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지가 누적되는 구조
- 이벤트에 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 전체를 마구 담아 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화를 어렵게 만드는 구조
- 추적 ID 없이 비동기 흐름을 흩어 놓아 장애 분석이 어려운 구조

기술사 관점에서는 EDA를 만능 해법처럼 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다, 비동기 후속 처리와 느슨한 결합이 실제로 필요한지 먼저 판단해야 한다. 사용자에게 즉시 확정 결과를 보여 줘야 하는 단계와, 뒤에서 비동기로 확장해도 되는 단계를 구분하는 설계가 핵심이다.

- **📢 섹션 요약 비유**: 방송 체계는 빠르고 유연하지만, 누가 어떤 공지를 듣지 못했는지 추적하고 다시 알리는 규칙이 없으면 금방 혼란이 생기는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

EDA는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 결합을 줄이고, 다수의 후속 처리를 독립적으로 확장하게 해 준다. 생산자는 빠르게 업무를 마감하고, 소비자는 자신만의 속도로 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 조절할 수 있으므로 대규모 트래픽과 부분 장애 상황에 특히 강하다. 또한 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적과 재처리의 근거가 되어, 운영 복원력 향상에도 기여한다.

하지만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 즉시 맞지 않을 수 있고, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 중복·순서·장애 재처리를 체계적으로 관리해야 한다는 부담이 따른다. 결국 EDA는 "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 직접 호출하지 않는다"가 핵심이 아니라, <strong>상태 변화의 사실을 안정적으로 기록하고 해석하는 운영 체계</strong>로 이해해야 한다. 그래서 이벤트 설계와 운영 규율이 빈약하면, EDA는 단순 결합 해소가 아니라 새로운 복잡성의 원인이 될 수 있다.

- **📢 섹션 요약 비유**: 잘 운영되는 방송국은 많은 사람에게 동시에 소식을 전하지만, 녹음 보관함과 재방송 규칙이 있어야 놓친 사람도 다시 들을 수 있는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 브로커 (Broker) | 생산자와 소비자 사이의 비동기 전달과 저장을 담당한다. |
| 아웃박스 패턴 (Outbox Pattern) | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 이벤트 발행 간 유실 문제를 완화한다. |
| [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 중복 이벤트 처리 시 결과를 안정적으로 유지한다. |
| [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/)) | [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)을 이벤트 기반 보상 흐름으로 풀어낸다. |
| [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command Query Responsibility Segregation](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/)) | 이벤트를 이용해 읽기 모델을 비동기로 갱신한다. |
| [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([Distributed Tracing](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)) | 비동기 경로를 따라 이벤트 흐름과 병목을 분석하게 해 준다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">동기 호출 체인의 결합 증가</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">브로커 기반 비동기 메시징 도입</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Publish / Subscribe 이벤트 전파</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">멱등성 · DLQ · 추적 체계 강화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Saga · CQRS · Event Sourcing 확장</div>
</div>
</div>



이 흐름은 단순 [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)에서 출발해, 점차 이벤트 중심 운영과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 확장되는 구조를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 한 친구가 소식을 모두에게 직접 전화하지 않고 방송으로 알려줘요.
2. 필요한 친구들은 방송을 듣고 자기 일을 알아서 해요.
3. 그래서 한 친구가 잠깐 바빠도 다른 친구들까지 모두 멈추지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 190 / 482

← **이전**: [189. 멀티 테넌트 데이터베이스 아키텍처 (Multi-Tenant Database Architecture) - SaaS 격리 설계](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/189_multi_tenant_database_architecture_saas/)
**다음**: [191. 컨슈머 그룹 (Consumer Group) - Kafka 파티션 병렬 처리와 부하 분산](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) →

---
