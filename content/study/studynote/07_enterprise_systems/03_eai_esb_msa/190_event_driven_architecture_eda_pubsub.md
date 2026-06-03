+++
weight = 190
title = "190. 이벤트 기반 아키텍처 (Event-Driven Architecture, EDA) - 비동기 Publish/Subscribe"
date = "2026-05-08"
[extra]
categories = "studynote-enterprise"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]] ([[140_event_driven_architecture_eda|Event-Driven Architecture]], [[064_eda|EDA]])는 [[090_service_kubernetes_network_load_balancing|서비스]]가 상대방을 직접 호출해 명령하는 대신, 자신에게 일어난 상태 변화를 이벤트로 발행하고 관심 있는 소비자가 이를 비동기로 처리하게 만드는 느슨한 결합 구조다.
> 2. **가치**: 생산자와 소비자의 생명주기와 처리 속도를 분리하므로, 장애 격리·탄력 확장·다중 후속 처리에 강하고 [[090_service_kubernetes_network_load_balancing|서비스]] 간 연쇄 대기를 크게 줄인다.
> 3. **판단 포인트**: EDA는 결국 최종 [[194_consistency_database_integrity|일관성]], 중복 처리, 추적 복잡성을 받아들이는 선택이므로, 이벤트 계약·재처리·[[171_idempotency_iac_terraform|멱등성]] 없이는 오히려 운영 난도가 더 높아질 수 있다.

---

## Ⅰ. 개요 및 필요성

EDA는 시스템 내부의 중요한 상태 변화를 이벤트라는 사실 형태로 외부에 알리고, 다른 [[090_service_kubernetes_network_load_balancing|서비스]]가 이를 독립적으로 구독해 처리하는 아키텍처다. 이 방식이 필요한 이유는 전통적인 동기 호출 체인이 [[090_service_kubernetes_network_load_balancing|서비스]] 수가 늘수록 장애 전파와 응답 [[015_지연_데이터_관점|지연]]을 확대하기 때문이다. 주문 [[090_service_kubernetes_network_load_balancing|서비스]]가 결제, 재고, 알림, 분석 시스템을 순서대로 직접 호출하면, 가장 느린 하위 [[090_service_kubernetes_network_load_balancing|서비스]]가 전체 사용자 경험을 결정하게 된다.

특히 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]에서는 서로 다른 팀이 각자 배포 일정을 가지므로, 강한 시간 결합이 운영 병목으로 이어진다. EDA는 "상대가 지금 살아 있는가"보다 "이 사실을 브로커에 안전하게 기록했는가"에 초점을 맞춘다. 즉 생산자는 이벤트를 남기고 빠르게 자신의 [[191_transaction_concept_states|트랜잭션]]을 끝내며, 후속 처리는 각 소비자의 속도와 장애 상황에 맞춰 흘러간다.

- **📢 섹션 요약 비유**: 누군가에게 직접 전화를 돌리는 대신, 공용 게시판에 중요한 공지를 붙여 두고 필요한 사람이 각자 와서 읽게 하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EDA의 핵심 구성은 생산자, 이벤트 브로커, 토픽 또는 큐, 소비자, 재처리 [[164_policy|정책]]이다. 생산자는 보통 업무 [[191_transaction_concept_states|트랜잭션]]이 끝나는 시점에 이벤트를 발행하고, 브로커는 이를 내구성 있게 저장해 소비자가 가져가도록 만든다. 소비자는 이벤트를 읽어 자신의 [[002_database_definition|데이터베이스]]를 갱신하거나 외부 알림, 분석 적재, 후속 워크플로를 수행한다.

아래 그림은 전형적인 퍼블리시/서브스크라이브 흐름을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Event propagation through broker                                     │
├──────────────────────────────────────────────────────────────────────┤
│ Order Service -- publish OrderPlaced --> Broker Topic               │
│                                         ├─ Inventory Consumer       │
│                                         ├─ Payment Consumer         │
│                                         └─ Notification Consumer    │
│                                                                      │
│ Trace ID / key / schema version travel with the event               │
└──────────────────────────────────────────────────────────────────────┘
```

| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 생산자 (Producer) | 상태 변화 이벤트 발행 | [[191_transaction_concept_states|트랜잭션]]과 이벤트 발행의 [[193_atomicity_all_or_nothing|원자성]] 보장 필요 |
| 브로커 (Broker) | 이벤트 저장과 전달 | 보존 기간, [[514_partition_slice_volume|파티션]], 순서 보장 범위 설계 |
| 이벤트 [[005_schema|스키마]] | 소비자 간 계약 | [[288_version_ihl_tos_total_length|버전]] 관리와 하위 [[344_compatibility_usability|호환성]] 중요 |
| 소비자 (Consumer) | 이벤트 기반 후속 처리 | [[171_idempotency_iac_terraform|멱등성]], 재시도, 장애 격리 필요 |
| 재처리 경로 | 실패 이벤트 [[658_ir_recovery|복구]] | Dead Letter [[058_queue|Queue]], 재시도, 수동 [[658_ir_recovery|복구]] 절차 |

EDA에서 중요한 원리는 이벤트를 "사실"로 다루는 것이다. `OrderPlaced`는 이미 발생한 상태 변화이므로 보통 불변이며, 나중에 수정이 필요하면 `OrderCancelled`처럼 새로운 이벤트를 발행한다. 또한 실무에서는 아웃박스 패턴 (Outbox Pattern)을 사용해 [[001_dikw_pyramid|데이터]] 저장과 이벤트 발행 사이의 유실 위험을 줄이는 경우가 많다.

- **📢 섹션 요약 비유**: 한 부서가 일을 끝냈다는 사실을 방송실에 남기면, 필요한 부서들이 자기 차례에 맞춰 방송을 듣고 각각 행동하는 것과 같다.

---

## Ⅲ. 비교 및 연결

EDA는 동기 요청-응답과 다르며, [[389_mesh_topology|메시]]지 큐와도 목적이 조금 다르다. 동기 응용 프로그램 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]])는 즉시 결과가 필요할 때 강력하지만, [[138_response_time|응답 시간]]과 장애가 직접 연결된다. 반면 EDA는 후속 처리의 분기와 확장에 유리하지만, 모든 시스템이 같은 시점에 같은 상태를 보는 것은 포기해야 한다. [[389_mesh_topology|메시]]지 큐가 "한 작업자를 위한 일감 전달"에 가깝다면, 퍼블리시/서브스크라이브는 "여러 소비자를 위한 사실 전파"에 가깝다.

| 비교 대상 | 강점 | 한계 | 잘 맞는 상황 |
| :--- | :--- | :--- | :--- |
| 동기 [[014_api_posix|API]] | 즉시 응답과 단순한 흐름 | 연쇄 장애와 대기 증가 | 조회, 즉시 승인, 사용자 상호작용 |
| 작업 큐 | 비동기 처리와 백프레셔 | 다중 소비자 확장성은 제한적 | 배치 작업, 단일 후속 처리 |
| [[064_eda|EDA]] Pub/Sub | 다중 소비자, 확장성, 느슨한 결합 | 최종 [[194_consistency_database_integrity|일관성]]과 운영 복잡성 | 주문 후속 처리, 알림, 분석, 통합 이벤트 |

EDA는 [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]), [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]), 명령 질의 책임 분리 ([[250_cqrs_command_query_responsibility_segregation_pattern|Command Query Responsibility Segregation]], [[306_cqrs|CQRS]]), [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]과 자주 연결된다. 예를 들어 [[312_saga_pattern_choreography_orchestration|사가]]는 이벤트를 통해 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]을 이어 가고, CQRS는 읽기 모델을 비동기 이벤트로 갱신한다. 따라서 EDA는 [[389_mesh_topology|메시]]징 기술이 아니라, **시스템을 상태 변화 중심으로 조직하는 사고방식**에 가깝다.

- **📢 섹션 요약 비유**: 직접 손을 잡고 줄지어 움직이는 행진보다, 무전 방송을 듣고 각 팀이 자기 자리에서 동시에 움직이는 운영 방식에 더 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 이벤트 이름, [[005_schema|스키마]] [[288_version_ihl_tos_total_length|버전]], [[514_partition_slice_volume|파티션]] 키, 재시도 [[164_policy|정책]]을 먼저 정해야 한다. 이벤트는 `SendNotification` 같은 명령형보다 `OrderPlaced`, `PaymentFailed` 같은 사실형 이름이 적합하며, 소비자는 같은 이벤트를 두 번 받아도 결과가 망가지지 않도록 멱등하게 구현해야 한다. 또한 장애 시 재시도만 반복하면 독성 [[389_mesh_topology|메시]]지가 전체 [[123_pipe|파이프]]라인을 막을 수 있으므로 데드 레터 큐 (Dead Letter [[058_queue|Queue]], DLQ)와 수동 [[658_ir_recovery|복구]] 절차가 필요하다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 이벤트 발행이 [[001_dikw_pyramid|데이터]] 저장과 분리되어 유실될 가능성이 있다면 아웃박스 패턴 등 보완책이 있는가?
2. 소비자가 중복 이벤트를 받아도 안전하도록 멱등 키, 상태 체크, 업서트 [[164_policy|정책]]이 준비되어 있는가?
3. 이벤트 [[005_schema|스키마]] 변경 시 하위 [[344_compatibility_usability|호환성]]과 [[288_version_ihl_tos_total_length|버전]] 관리 [[164_policy|정책]]이 있는가?
4. 최종 [[194_consistency_database_integrity|일관성]]을 사용자 경험과 업무 규칙 측면에서 수용할 수 있는가?
5. 브로커, 소비자, DLQ, 추적 시스템까지 포함한 운영 관측성이 갖춰져 있는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 이벤트라는 이름으로 사실상 원격 프로시저 호출을 흉내 내는 구조
- 재처리 [[268_strategy_pattern|전략]] 없이 소비자 로직만 구현해 장애 시 [[389_mesh_topology|메시]]지가 누적되는 구조
- 이벤트에 [[178_as_is_to_be_analysis|현재 상태]] 전체를 마구 담아 [[005_schema|스키마]] 진화를 어렵게 만드는 구조
- 추적 ID 없이 비동기 흐름을 흩어 놓아 장애 분석이 어려운 구조

기술사 관점에서는 EDA를 만능 해법처럼 [[289_cqrs_db|쓰기]]보다, 비동기 후속 처리와 느슨한 결합이 실제로 필요한지 먼저 판단해야 한다. 사용자에게 즉시 확정 결과를 보여 줘야 하는 단계와, 뒤에서 비동기로 확장해도 되는 단계를 구분하는 설계가 핵심이다.

- **📢 섹션 요약 비유**: 방송 체계는 빠르고 유연하지만, 누가 어떤 공지를 듣지 못했는지 추적하고 다시 알리는 규칙이 없으면 금방 혼란이 생기는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

EDA는 [[090_service_kubernetes_network_load_balancing|서비스]] 간 결합을 줄이고, 다수의 후속 처리를 독립적으로 확장하게 해 준다. 생산자는 빠르게 업무를 마감하고, 소비자는 자신만의 속도로 [[139_throughput|처리량]]을 조절할 수 있으므로 대규모 트래픽과 부분 장애 상황에 특히 강하다. 또한 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]는 [[606_auditing_linux_auditd|감사]] 추적과 재처리의 근거가 되어, 운영 복원력 향상에도 기여한다.

하지만 [[001_dikw_pyramid|데이터]]가 즉시 맞지 않을 수 있고, [[389_mesh_topology|메시]]지 중복·순서·장애 재처리를 체계적으로 관리해야 한다는 부담이 따른다. 결국 EDA는 "[[090_service_kubernetes_network_load_balancing|서비스]]를 직접 호출하지 않는다"가 핵심이 아니라, **상태 변화의 사실을 안정적으로 기록하고 해석하는 운영 체계**로 이해해야 한다. 그래서 이벤트 설계와 운영 규율이 빈약하면, EDA는 단순 결합 해소가 아니라 새로운 복잡성의 원인이 될 수 있다.

- **📢 섹션 요약 비유**: 잘 운영되는 방송국은 많은 사람에게 동시에 소식을 전하지만, 녹음 보관함과 재방송 규칙이 있어야 놓친 사람도 다시 들을 수 있는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 브로커 (Broker) | 생산자와 소비자 사이의 비동기 전달과 저장을 담당한다. |
| 아웃박스 패턴 (Outbox Pattern) | [[191_transaction_concept_states|트랜잭션]]과 이벤트 발행 간 유실 문제를 완화한다. |
| [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) | 중복 이벤트 처리 시 결과를 안정적으로 유지한다. |
| [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]) | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]을 이벤트 기반 보상 흐름으로 풀어낸다. |
| [[306_cqrs|CQRS]] ([[250_cqrs_command_query_responsibility_segregation_pattern|Command Query Responsibility Segregation]]) | 이벤트를 이용해 읽기 모델을 비동기로 갱신한다. |
| [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]]) | 비동기 경로를 따라 이벤트 흐름과 병목을 분석하게 해 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
동기 호출 체인의 결합 증가
        │
        ▼
브로커 기반 비동기 메시징 도입
        │
        ▼
Publish / Subscribe 이벤트 전파
        │
        ▼
멱등성 · DLQ · 추적 체계 강화
        │
        ▼
Saga · CQRS · Event Sourcing 확장
```

이 흐름은 단순 [[119_message_passing|메시지 전달]]에서 출발해, 점차 이벤트 중심 운영과 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] [[268_strategy_pattern|전략]]으로 확장되는 구조를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 한 친구가 소식을 모두에게 직접 전화하지 않고 방송으로 알려줘요.
2. 필요한 친구들은 방송을 듣고 자기 일을 알아서 해요.
3. 그래서 한 친구가 잠깐 바빠도 다른 친구들까지 모두 멈추지 않아요.
