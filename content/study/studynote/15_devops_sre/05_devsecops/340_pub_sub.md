+++
weight = 340
title = "340. 카프카 분산 메시지 스트리밍 (Apache Kafka Topic Partition Offset Consumer Group ISR vs RabbitMQ)"
date = "2026-05-09"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Kafka는 [[136_variance|분산]] 이벤트 스트리밍 플랫폼으로 Topic-[[514_partition_slice_volume|Partition]]-Offset 구조로 대용량 [[389_mesh_topology|메시]]지를 내구성 있게 저장하고 전달한다. [[389_mesh_topology|메시]]지를 소비(Consume)해도 삭제하지 않고 보존 기간 동안 유지하므로, 여러 Consumer Group이 독립적으로 같은 [[001_dikw_pyramid|데이터]]를 읽을 수 있다.
> 2. **Partition과 [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]]**: Partition은 [[179_kafka_flink_watermark_time_window|Kafka]] 확장성의 핵심이다. 하나의 Topic이 여러 Partition으로 나뉘고, [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] 내의 Consumer들이 각 Partition을 분담해 [[430_index_fast_full_scan|병렬]] 처리한다. Consumer 수가 [[514_partition_slice_volume|Partition]] 수보다 많으면 일부 Consumer는 유휴 상태가 된다.
> 3. **판단 포인트**: [[020_isr|ISR]] (In-Sync Replica, [[212_synchronization_mechanisms|동기화]]된 [[016_replication_factor|복제]]본) 수가 최소 [[016_replication_factor|복제]] 기준(min.insync.replicas)을 만족해야 Producer가 [[389_mesh_topology|메시]]지를 기록할 수 있다. [[020_isr|ISR]] 부족 시 [[289_cqrs_db|쓰기]] 거부로 내구성을 보장한다. [[179_kafka_flink_watermark_time_window|Kafka]] vs RabbitMQ: 대용량 스트리밍은 [[179_kafka_flink_watermark_time_window|Kafka]], 복잡한 [[339_routing_overview_best_path_selection|라우팅]]은 RabbitMQ다.

---

## Ⅰ. 개요 및 필요성

LinkedIn이 2011년 내부 [[645_data_pipeline_acceleration|데이터 파이프라인]] 병목을 해결하기 위해 개발한 Kafka는 초당 수백만 건의 이벤트를 처리하는 고처리량(High-[[139_throughput|Throughput]]) [[145_message_broker_sync_async|메시지 브로커]]로 발전했다.

기존 [[389_mesh_topology|메시]]지 큐(RabbitMQ 등)는 [[389_mesh_topology|메시]]지를 소비하면 즉시 삭제해 재처리가 어렵다. Kafka는 [[389_mesh_topology|메시]]지를 [[568_logs_distributed_logging_elk_fluentd|로그]](Log)로 영속 저장해 Consumer가 과거 어느 시점으로도 되돌아가 재처리할 수 있다. 이는 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]])과 [[306_cqrs|CQRS]] 패턴의 핵심 인프라가 된다.

> 📢 **섹션 요약 비유**: Kafka는 방송국 라디오다. 한 번 방송된 프로그램([[389_mesh_topology|메시]]지)을 여러 청취자([[191_consumer_group_kafka_partition_load_balancing|Consumer Group]])가 각자의 시간에 들을 수 있다. Offset으로 이어 들을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+----------------------------------------------------------------+
|                    Kafka 토픽 구조                              |
+----------------------------------------------------------------+
|                                                                |
|  Topic: "order-events"                                         |
|  +-----------------------------------------------------------+ |
|  |  Partition 0: [Offset 0][Offset 1][Offset 2]...           | |
|  |  Partition 1: [Offset 0][Offset 1][Offset 2]...           | |
|  |  Partition 2: [Offset 0][Offset 1][Offset 2]...           | |
|  +-----------------------------------------------------------+ |
|                                                                |
|  Consumer Group A:                                             |
|  Consumer 1 -> Partition 0                                     |
|  Consumer 2 -> Partition 1                                     |
|  Consumer 3 -> Partition 2                                     |
|  (각 Consumer가 독립적 Offset 추적)                             |
|                                                                |
|  ISR (In-Sync Replica):                                        |
|  Leader: Broker 1 <- Producer 기록                             |
|  Follower: Broker 2, 3 (Leader 복제)                           |
|  ISR = {Broker 1, 2, 3} -> min.insync.replicas=2 -> 기록 OK   |
+----------------------------------------------------------------+
```

| 개념 | 설명 |
|:---|:---|
| Topic | [[389_mesh_topology|메시]]지 카테고리 |
| [[514_partition_slice_volume|Partition]] | Topic의 [[430_index_fast_full_scan|병렬]] 처리 단위 |
| Offset | [[514_partition_slice_volume|Partition]] 내 [[389_mesh_topology|메시]]지 순서 번호 |
| [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] | 같은 Topic을 분담 처리하는 Consumer 집합 |
| [[020_isr|ISR]] | Leader와 [[212_synchronization_mechanisms|동기화]]된 Replica 집합 |

> 📢 **섹션 요약 비유**: Partition은 슈퍼마켓의 계산대 줄이다. 줄이 많을수록([[514_partition_slice_volume|Partition]] 수 증가) 더 많은 손님([[389_mesh_topology|메시]]지)을 동시에 처리할 수 있다. Consumer는 각 계산대를 담당하는 직원이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[179_kafka_flink_watermark_time_window|Kafka]] | RabbitMQ |
|:---|:---|:---|
| [[389_mesh_topology|메시]]지 보존 | 기간 기반 영속 저장 | 소비 후 즉시 삭제 |
| [[139_throughput|처리량]] | 매우 높음 (초당 수백만) | 중간 |
| 순서 보장 | [[514_partition_slice_volume|Partition]] 내 보장 | [[058_queue|Queue]] 내 보장 |
| 재처리 | Offset 재설정으로 가능 | 어려움 |
| 사용 사례 | 이벤트 스트리밍, [[626_log_collection|로그 수집]] | 작업 큐, [[126_rpc|RPC]] |
| [[339_routing_overview_best_path_selection|라우팅]] | 단순 (Topic 기반) | 복잡 (Exchange/Binding) |

> 📢 **섹션 요약 비유**: Kafka는 유튜브(영상 영속 저장, 여러 사람이 다른 시간에 시청)이고, RabbitMQ는 택배 [[090_service_kubernetes_network_load_balancing|서비스]](배달 완료 후 패키지 폐기, 복잡한 배송 경로)다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[179_kafka_flink_watermark_time_window|Kafka]] 설계 원칙

- **[[514_partition_slice_volume|Partition]] 수**: Consumer 수와 일치시키거나, 미래 확장을 고려해 더 크게 [[009_config|설정]]
- **[[016_replication_factor|복제]] 팩터**: 최소 3 (Leader 1 + Follower 2), min.insync.replicas=2
- **보존 기간**: 비즈니스 요구에 따라 [[009_config|설정]] (7일~수 주, 또는 무한)
- **[[191_consumer_group_kafka_partition_load_balancing|Consumer Group]]**: 각 소비 용도마다 별도 Group (분석, 알림, 저장 등)

### [[435_checklist_based_testing|체크리스트]]

1. [[514_partition_slice_volume|Partition]] 수가 Consumer 수와 균형을 이루는가?
2. min.insync.replicas [[009_config|설정]]이 [[001_dikw_pyramid|데이터]] 내구성 요구사항을 충족하는가?
3. [[089_consumer_lag|Consumer Lag]] (Consumer가 따라가지 못하는 [[389_mesh_topology|메시]]지 수)를 [[229_monitor|모니터]]링하는가?
4. [[505_schema|Schema]] Registry로 [[389_mesh_topology|메시]]지 형식(Avro/[[343_json|JSON]] [[505_schema|Schema]])이 관리되는가?

> 📢 **섹션 요약 비유**: Consumer Lag는 받은 편지함에 읽지 않은 메일 수다. 너무 많이 쌓이면 처리가 늦어지고 있다는 [[130_signal|신호]]다.

---

## Ⅴ. 기대효과 및 결론

[[179_kafka_flink_watermark_time_window|Kafka]] 도입으로 [[532_microservices_decomposition_patterns|마이크로서비스]] 간 느슨한 결합(Loose [[195_coupling_levels|Coupling]])이 달성된다. [[090_service_kubernetes_network_load_balancing|서비스]] A가 이벤트를 발행하면 [[090_service_kubernetes_network_load_balancing|서비스]] B, C, D가 독립적으로 소비해, 직접 의존 없이 [[001_dikw_pyramid|데이터]]가 흐른다.

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 패턴에서 Kafka는 모든 상태 변경을 이벤트로 저장해 시스템 상태를 임의 시점으로 재현할 수 있다. 이는 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]]), 디버깅, 재처리에 강력한 능력을 제공한다.

> 📢 **섹션 요약 비유**: Kafka는 회사의 공식 회의록이다. 모든 의사결정(이벤트)이 기록되고, 나중에 그때 무슨 결정이 났지를 [[396_validation|확인]]하거나 잘못된 결정을 되돌릴 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Topic | [[179_kafka_flink_watermark_time_window|Kafka]] [[389_mesh_topology|메시]]지 카테고리 |
| [[514_partition_slice_volume|Partition]] | [[430_index_fast_full_scan|병렬]] 처리 단위, Offset 순서 보장 |
| [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] | 독립적 [[389_mesh_topology|메시]]지 소비 단위 |
| [[020_isr|ISR]] (In-Sync Replica) | Leader [[016_replication_factor|복제]] [[212_synchronization_mechanisms|동기화]] 집합 |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] | [[179_kafka_flink_watermark_time_window|Kafka]] 기반 상태 이력 관리 |
| [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] | [[389_mesh_topology|메시]]지 형식 [[288_version_ihl_tos_total_length|버전]] 관리 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통 메시지 큐            Kafka 등장                   현대 이벤트 스트리밍
------------------   --------------------------   ------------------------
RabbitMQ/ActiveMQ  ->  LinkedIn Kafka 오픈소스    ->  Kafka Streams API
소비 후 삭제             Topic-Partition-Offset        Schema Registry
단순 작업 큐              ISR 내구성 보장               Kafka Connect
                          Consumer Group 병렬화          서버리스 Kafka (Confluent)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[179_kafka_flink_watermark_time_window|Kafka]] Topic은 TV 채널이에요. Partition은 같은 채널의 여러 화면이고, 각 Consumer가 한 화면씩 맡아서 봐요.
2. Offset은 드라마를 어디까지 봤는지 기록하는 책갈피예요. 나중에 다시 봐도 이어서 볼 수 있어요.
3. ISR은 중요한 방송을 녹화해두는 [[555_backup_and_restore_strategy|백업]] 장치예요. 녹화기가 최소 2대 있어야 방송이 안전하게 기록돼요.
