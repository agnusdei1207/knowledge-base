---
title: 120. 이벤트 주도 아키텍처 (EDA, Event-Driven Architecture)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[064_eda|EDA]] ([[140_event_driven_architecture_eda|Event-Driven Architecture]], [[367_architecture|이벤트 주도 아키텍처]])는 시스템 상태 변화를 이벤트(event)로 표현하고, 생산자(Producer)가 이벤트를 발행(Publish)하면 관심 있는 소비자(Consumer)가 비동기적으로 구독(Subscribe)하여 처리하는 방식으로 [[603_component_independent_deployment_unit|컴포넌트]] 간 [[195_coupling_levels|결합도]]를 최소화하는 [[114_architecture_style|아키텍처 스타일]]이다.
> 2. **가치**: 이벤트 생산자가 소비자를 알 필요가 없으므로 새로운 기능(소비자)을 추가해도 기존 코드를 전혀 수정하지 않아도 되며, 각 [[603_component_independent_deployment_unit|컴포넌트]]가 독립적으로 확장([[202_scale_out_distributed_horizontal_expansion|scale-out]])되는 [[571_resiliency_fault_tolerance_patterns|탄력성]](resilience)이 확보된다.
> 3. **판단 포인트**: EDA의 핵심 트레이드오프는 최종 [[194_consistency_database_integrity|일관성]]([[650_eventual_consistency|eventual consistency]])과 디버깅 복잡성이다. [[136_variance|분산]] 이벤트 흐름에서 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 보장이 어려우므로, 즉각적 [[194_consistency_database_integrity|일관성]]이 필수인 금융 결제 같은 도메인에서는 동기 호출과 적절히 혼합해야 한다.

---

## Ⅰ. 개요 및 필요성

EDA의 등장 배경은 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])의 확산이다. [[090_service_kubernetes_network_load_balancing|서비스]] 간 동기 [[156_rest_representational_state_transfer|REST]] 호출로만 통신하면 호출 체인이 길어질수록 단일 실패 지점([[454_spof|SPOF]], Single Point of Failure)이 늘어나고 [[452_availability|가용성]]이 낮아진다. [[090_service_kubernetes_network_load_balancing|서비스]] A가 B를 호출하고, B가 C를 호출하는 구조에서 C가 다운되면 A와 B까지 응답 불가 상태가 된다.

EDA는 이 동기 의존 체인을 끊는다. 주문 [[090_service_kubernetes_network_load_balancing|서비스]](Producer)가 "주문 완료" 이벤트를 발행하면, 재고 [[090_service_kubernetes_network_load_balancing|서비스]]·알림 [[090_service_kubernetes_network_load_balancing|서비스]]·포인트 [[090_service_kubernetes_network_load_balancing|서비스]](Consumer)가 각자 독립적으로 구독하여 처리한다. 주문 [[090_service_kubernetes_network_load_balancing|서비스]]는 다른 [[090_service_kubernetes_network_load_balancing|서비스]]의 상태나 처리 결과를 기다리지 않는다.

```text
┌─────────────────────────────────────────────────────────────┐
│         EDA의 이벤트 흐름: 발행-구독 구조                    │
├─────────────────────────────────────────────────────────────┤
│  [동기 호출 방식 - 강결합]                                   │
│  주문서비스 ──▶ 재고서비스 ──▶ 알림서비스 ──▶ 포인트서비스  │
│  (한 곳 장애 시 전체 실패)                                   │
│                                                             │
│  [EDA 방식 - 약결합]                                        │
│                                                             │
│  주문서비스                                                 │
│      │ OrderCompleted 이벤트 발행                           │
│      ▼                                                      │
│  [Message Broker (Kafka/RabbitMQ)]                          │
│      │          │               │                           │
│      ▼          ▼               ▼                           │
│  재고서비스   알림서비스      포인트서비스                   │
│  (독립 구독)  (독립 구독)     (독립 구독)                    │
└─────────────────────────────────────────────────────────────┘
```

이벤트가 [[145_message_broker_sync_async|메시지 브로커]]([[145_message_broker_sync_async|Message Broker]])에 저장되므로 소비자가 일시적으로 다운되어도 브로커가 이벤트를 보존하며, [[658_ir_recovery|복구]] 후 처리를 재개할 수 있다. 이 특성이 EDA의 [[571_resiliency_fault_tolerance_patterns|탄력성]](resilience)을 만든다.

- **📢 섹션 요약 비유**: 방송국(Producer)이 라디오 [[130_signal|신호]](이벤트)를 보내면 청취자(Consumer)들이 각자 수신한다. 방송국은 누가 듣는지 알 필요가 없고, 청취자도 방송국과 직접 연결될 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EDA는 이벤트의 처리 방식에 따라 세 가지 토폴로지(topology)로 구분된다. ① [[273_mediator_pattern|중재자]] 토폴로지([[273_mediator_pattern|Mediator]] Topology): 중앙 오케스트레이터가 이벤트 처리 흐름을 제어, ② 브로커 토폴로지(Broker Topology): 이벤트가 [[389_mesh_topology|메시]]지 채널을 따라 자율적으로 흐름, ③ 하이브리드: 둘의 혼합.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [[273_mediator_pattern|중재자]] ([[273_mediator_pattern|Mediator]]) | 중앙 오케스트레이터 존재 / 흐름 가시성 높음, 모니터링 용이 | 중앙 [[454_spof|SPOF]] 위험 |
| 브로커 (Broker) | 이벤트가 자율적으로 흐름 / 극단적 [[195_coupling_levels|결합도]] 감소 | 전체 흐름 파악 어려움 |
| 하이브리드 | 상황에 따라 혼합 / 균형 있는 트레이드오프 | 복잡한 설계 필요 |

```text
┌─────────────────────────────────────────────────────────────┐
│         이벤트 처리 보장 수준 스펙트럼                        │
├─────────────────────────────────────────────────────────────┤
│  At-most-once  │ At-least-once  │ Exactly-once             │
│  (최대 한 번)  │ (최소 한 번)   │ (정확히 한 번)            │
│  손실 가능     │ 중복 처리 가능 │ 가장 강력, 비용 높음       │
│                │                │                          │
│  로그 수집     │ 알림·이메일    │ 금융 거래                 │
└─────────────────────────────────────────────────────────────┘
```

[[179_kafka_flink_watermark_time_window|Kafka]] ([[214_kafka_pubsub_topic_partition_offset_broker|아파치 카프카]])는 EDA에서 가장 널리 사용되는 [[136_variance|분산]] [[389_mesh_topology|메시]]지 스트리밍 플랫폼이다. 파티셔닝을 통한 [[430_index_fast_full_scan|병렬]] 처리, 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]] 영속화, 컨슈머 그룹을 통한 부하 [[136_variance|분산]]이 대규모 EDA를 지원한다.

- **📢 섹션 요약 비유**: 우편함([[145_message_broker_sync_async|메시지 브로커]])에 편지(이벤트)를 넣으면 수신자(Consumer)가 자기 페이스에 맞게 꺼내 읽는다. 발송자(Producer)는 수신자가 자리에 있는지 확인하지 않는다.

---
## Ⅲ. 비교 및 연결

EDA와 동기 [[156_rest_representational_state_transfer|REST]] 호출의 핵심 차이는 시간적 결합(temporal [[195_coupling_levels|coupling]])의 제거다. 동기 호출에서는 호출자와 수신자가 같은 시간에 활성화되어야 한다. EDA는 이 시간적 결합을 끊어 독립적 생명주기를 부여한다.

| 비교 축 | A | B |
|:---|:---|:---|
| **[[195_coupling_levels|결합도]]** | 높음 (직접 의존) | 낮음 (브로커 경유) |
| **[[194_consistency_database_integrity|일관성]]** | 즉각적 [[194_consistency_database_integrity|일관성]] | 최종 [[194_consistency_database_integrity|일관성]] |
| **[[452_availability|가용성]]** | 호출 대상 의존 | 브로커 내구성에 의존 |
| **디버깅** | [[057_stack|스택]] 트레이스 추적 용이 | 이벤트 흐름 추적 복잡 |
| **적합 케이스** | 즉각 응답 필요 | 비동기 처리, 독립 확장 |

EDA는 [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation, [[271_command_pattern|커맨드]] [[298_qkv_attention|쿼리]] 책임 분리)·[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]])과 자주 결합된다. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]에서 상태 변화를 이벤트 스트림으로 저장하고, CQRS에서 이 이벤트를 읽기 모델에 반영하는 패턴이 대표적 조합이다.

- **📢 섹션 요약 비유**: 회의(동기 호출)는 참석자 모두가 같은 시간에 모여야 한다. 게시판([[064_eda|EDA]])은 메모를 붙여두면 각자 시간이 날 때 읽어가면 된다. 긴급 상황은 회의로, 일상 공지는 게시판으로 처리한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[064_eda|EDA]] 적용의 가장 까다로운 실무 과제는 이벤트 [[005_schema|스키마]] 진화([[505_schema|schema]] evolution)와 [[171_idempotency_iac_terraform|멱등성]]([[194_idempotency|idempotency]]) 보장이다. 이벤트 [[005_schema|스키마]]가 변경될 때 기존 소비자와의 하위 호환성을 유지해야 하며, 네트워크 재시도로 같은 이벤트가 중복 전달될 때 소비자가 동일 처리를 중복 실행하지 않도록 [[171_idempotency_iac_terraform|멱등성]] 처리가 필요하다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 이벤트 소비자가 동일 이벤트를 중복 수신해도 안전하게 처리하는가([[171_idempotency_iac_terraform|멱등성]])?
2. 이벤트 [[005_schema|스키마]] 변경 시 기존 소비자가 영향받지 않도록 하위 호환성을 보장하는가?
3. 이벤트 흐름 전체를 추적할 수 있는 [[112_distributed_tracing_microservices|분산 트레이싱]]([[569_distributed_tracing_opentelemetry_jaeger|distributed tracing]])이 적용되어 있는가?
4. 이벤트 처리 실패 시 DLQ (Dead Letter [[058_queue|Queue]], 데드 레터 큐)를 통한 재처리 전략이 있는가?
5. [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]이 최종 [[194_consistency_database_integrity|일관성]]으로 충분한가, 즉각적 [[194_consistency_database_integrity|일관성]]이 필요한 트랜잭션이 혼재하는가?

- **📢 섹션 요약 비유**: 택배 시스템처럼 보내는 사람(Producer)과 받는 사람(Consumer)이 같은 시간에 만나지 않아도 된다. 택배사(브로커)가 중간에서 보관하고 배달한다. 배달 실패 시 재시도(DLQ)한다.

---

## Ⅴ. 기대효과 및 결론

EDA를 적용하면 시스템의 [[571_resiliency_fault_tolerance_patterns|탄력성]]과 확장성이 동시에 향상된다. 트래픽 급증 시 소비자를 수평 확장하여 이벤트 처리량을 늘릴 수 있고, 특정 [[090_service_kubernetes_network_load_balancing|서비스]]의 장애가 다른 [[090_service_kubernetes_network_load_balancing|서비스]]로 전파되지 않는 격리([[195_isolation_concurrency_control|isolation]])가 달성된다. 새로운 기능을 추가할 때 기존 이벤트를 구독하는 새 소비자를 추가하는 것만으로 확장이 완료되어 기존 코드 변경 없이 기능 확장([[746_ocp|OCP]] 실현)이 가능하다.

한계는 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], 이벤트 순서 보장, 디버깅 복잡성이다. [[136_variance|분산]] 이벤트 시스템에서 이벤트 순서가 뒤바뀌거나 중복 처리되는 상황을 모두 처리해야 하며, 전통적인 [[057_stack|스택]] 트레이스 기반 디버깅 대신 [[112_distributed_tracing_microservices|분산 트레이싱]] 도구(Jaeger, Zipkin)가 필수가 된다.

미래 방향으로는 ① 이벤트 [[389_mesh_topology|메시]] (Event [[389_mesh_topology|Mesh]])를 통한 [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] 이벤트 [[339_routing_overview_best_path_selection|라우팅]], ② CloudEvents 표준으로 이벤트 형식 표준화, ③ [[190_ai_llm_requirements_specification|AI]] 기반 이벤트 스트림 이상 탐지가 발전하고 있다.

EDA는 "[[090_service_kubernetes_network_load_balancing|서비스]]가 서로를 모르는 상태에서 협력하는 방법"을 구현하는 아키텍처로, [[532_microservices_decomposition_patterns|마이크로서비스]]의 진정한 독립성을 달성하는 핵심 메커니즘으로 기억해야 한다.

- **📢 섹션 요약 비유**: 오케스트라(동기)는 지휘자 타이밍에 모두가 맞춰야 하지만, 재즈 즉흥 연주([[064_eda|EDA]])는 각 연주자가 다른 사람의 연주를 듣고 자신의 타이밍에 맞춰 독립적으로 반응한다.

---

### 📌 관련 개념 맵

[동기 [[156_rest_representational_state_transfer|REST]] 강결합 문제] → [[[064_eda|EDA]]] → [메시지 브로커([[179_kafka_flink_watermark_time_window|Kafka]])] → [[[306_cqrs|CQRS]]·이벤트 소싱] → [[[619_msa_traffic_hardware|MSA]] 탄력성]

| 개념 | 연결 포인트 |
|:---|:---|
| [[179_kafka_flink_watermark_time_window|Kafka]] | EDA의 대표 [[136_variance|분산]] [[389_mesh_topology|메시]]지 스트리밍 플랫폼 |
| [[306_cqrs|CQRS]] | EDA와 결합하여 [[289_cqrs_db|쓰기]]·읽기 모델을 이벤트로 분리 |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] | 상태를 이벤트 스트림으로 저장, EDA와 자연스럽게 결합 |
| [[112_distributed_tracing_microservices|분산 트레이싱]] | [[064_eda|EDA]] 이벤트 흐름 추적을 위한 Jaeger, Zipkin 등 |

### 📈 관련 키워드 및 발전 흐름도

[동기 [[156_rest_representational_state_transfer|REST]] 강결합] → [비동기 [[389_mesh_topology|메시]]징(MQ)] → [[[064_eda|EDA]] 아키텍처 스타일] → [[[179_kafka_flink_watermark_time_window|Kafka]] [[136_variance|분산]] 스트리밍] → [[[306_cqrs|CQRS]]+이벤트 소싱] → [이벤트 [[389_mesh_topology|메시]]·CloudEvents 표준화]

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 안내 방송(이벤트)이 나오면 각 교실(Consumer)에서 각자 알아서 준비해요.
2. 방송국(Producer)은 어느 교실이 듣는지 일일이 확인하지 않아요.
3. 새 교실([[090_service_kubernetes_network_load_balancing|서비스]])이 추가되어도 방송 시스템을 바꿀 필요 없이 스피커(구독)만 달면 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 176 / 530

← **이전**: [[119_mvc_architecture|119. 모델-뷰-컨트롤러 아키텍처 (MVC, Model-View-Controller)]]
**다음**: [[121_cqrs_pattern|121. CQRS 패턴 (Command Query Responsibility Segregation)]] →

---
