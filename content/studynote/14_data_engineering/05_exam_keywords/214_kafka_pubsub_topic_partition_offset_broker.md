---
title: 214. 아파치 카프카 (Apache Kafka) Pub-Sub 토픽 파티션 오프셋 브로커
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Kafka는 Pub-Sub(Publish-Subscribe) 메시징 패턴 기반의 [[136_variance|분산]] 이벤트 스트리밍 플랫폼으로, 토픽(Topic)을 [[514_partition_slice_volume|파티션]]([[514_partition_slice_volume|Partition]])으로 분할해 수평 확장하며, 오프셋(Offset)으로 각 컨슈머의 읽기 위치를 독립적으로 추적한다.
> 2. **가치**: [[514_partition_slice_volume|파티션]] 단위 [[430_index_fast_full_scan|병렬]] 처리와 리플리케이션([[016_replication_factor|Replication]])으로 초당 수백만 건 메시지를 내결함성([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])을 유지하며 처리하고, [[179_kafka_flink_watermark_time_window|Kafka]] Connect·[[179_kafka_flink_watermark_time_window|Kafka]] Streams 에코시스템이 [[645_data_pipeline_acceleration|데이터 파이프라인]] 전반을 담당한다.
> 3. **판단 포인트**: Kafka는 "메시지를 소비해도 삭제하지 않는다" — 이 원칙이 멀티 컨슈머 독립 처리, 재처리, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]])을 가능하게 하는 핵심 설계 철학이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 전통적 메시지 큐 vs [[179_kafka_flink_watermark_time_window|Kafka]]

| 항목 | 전통 MQ (RabbitMQ 등) | Apache [[179_kafka_flink_watermark_time_window|Kafka]] |
|:---|:---|:---|
| **소비 후 삭제** | 소비 시 즉시 삭제 | 보존 기간([[515_mvcc|retention]]) 동안 유지 |
| **순서 보장** | 큐 수준 | [[514_partition_slice_volume|파티션]] 수준 |
| **[[249_scaling_normalization_standardization|스케일링]]** | 수직 확장 위주 | 수평 확장 ([[514_partition_slice_volume|파티션]] 추가) |
| **재처리** | 불가 | 오프셋 리셋으로 가능 |
| **[[139_throughput|처리량]]** | 중간 (수만 TPS) | 초고성능 (수백만 TPS) |
| **주요 용도** | 작업 큐, [[126_rpc|RPC]] | 이벤트 스트리밍, [[217_cdc_binlog_change_capture_debezium|CDC]], [[626_log_collection|로그 수집]] |

### 1.2 Kafka의 핵심 설계 원칙

Kafka는 [[568_logs_distributed_logging_elk_fluentd|로그]](Log) 자료구조를 기반으로 설계되었다. 메시지는 순서대로 [[568_logs_distributed_logging_elk_fluentd|로그]]에 추가(Append-Only)되며, 컨슈머는 [[568_logs_distributed_logging_elk_fluentd|로그]]를 읽을 뿐 지우지 않는다.

```
Kafka 토픽 = 무한히 이어지는 기록지(Append-Only Log)

오프셋:  0     1     2     3     4     5   ...
        ┌───┬─────┬─────┬─────┬─────┬─────┐
메시지:  │ A │  B  │  C  │  D  │  E  │  F  │ ──► 계속 추가
        └───┴─────┴─────┴─────┴─────┴─────┘
컨슈머1:                    ↑ (오프셋 3 읽는 중)
컨슈머2:              ↑ (오프셋 2 읽는 중 — 독립적!)
```

📢 **섹션 요약 비유**: Kafka는 거대한 공용 게시판이다 — 글을 올리면 모두가 볼 수 있고, 내가 어디까지 읽었는지(오프셋)는 각자 책갈피로 관리한다. 다른 사람이 읽어도 게시물은 지워지지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[179_kafka_flink_watermark_time_window|Kafka]] 핵심 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **브로커 (Broker)** | [[179_kafka_flink_watermark_time_window|Kafka]] 서버 노드 — 메시지 저장·전달 담당 |
| **토픽 (Topic)** | 메시지 [[104_classification_analysis|분류]] 채널 (예: orders, payments, [[568_logs_distributed_logging_elk_fluentd|logs]]) |
| **[[514_partition_slice_volume|파티션]] ([[514_partition_slice_volume|Partition]])** | 토픽을 분할한 단위 — [[430_index_fast_full_scan|병렬]] 처리의 기본 |
| **오프셋 (Offset)** | [[514_partition_slice_volume|파티션]] 내 메시지 순서 번호 (0부터 시작) |
| **프로듀서 (Producer)** | 메시지를 토픽에 발행(Publish)하는 주체 |
| **컨슈머 (Consumer)** | 토픽에서 메시지를 구독(Subscribe)하는 주체 |
| **[[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] ([[191_consumer_group_kafka_partition_load_balancing|Consumer Group]])** | 동일 토픽을 [[430_index_fast_full_scan|병렬]]로 처리하는 컨슈머 묶음 |
| **주키퍼 ([[798_distributed_lock_zookeeper_consensus|ZooKeeper]]) / KRaft** | 클러스터 [[203_metadata_management|메타데이터 관리]] ([[179_kafka_flink_watermark_time_window|Kafka]] 3.x에서 KRaft로 전환) |

### 2.2 [[514_partition_slice_volume|파티션]]과 [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] [[083_relationship_in_er_model|관계]]

```
토픽: "orders" (파티션 3개)

파티션 0: [msg0, msg3, msg6, ...]
파티션 1: [msg1, msg4, msg7, ...]
파티션 2: [msg2, msg5, msg8, ...]

컨슈머 그룹 A (컨슈머 3개 — 1:1 매핑):
┌────────────┬────────────┬────────────┐
│ Consumer-0 │ Consumer-1 │ Consumer-2 │
│  파티션 0  │  파티션 1  │  파티션 2  │
└────────────┴────────────┴────────────┘
→ 최대 처리량 (각 컨슈머가 독립 파티션 담당)

컨슈머 그룹 B (컨슈머 1개 — 전체 소비):
┌──────────────────────────────────────┐
│           Consumer-0                  │
│  파티션 0 + 파티션 1 + 파티션 2      │
└──────────────────────────────────────┘
→ 단일 컨슈머가 전체 순서 처리 가능
```

**중요 규칙**: 하나의 [[514_partition_slice_volume|파티션]]은 동일 [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] 내에서 **하나의 컨슈머에게만** 할당된다 → [[514_partition_slice_volume|파티션]] 수가 [[430_index_fast_full_scan|병렬]]처리의 한계를 결정한다.

### 2.3 리플리케이션 ([[016_replication_factor|Replication]]) 내결함성

```
토픽: "payments", 파티션 0, 복제 인수(Replication Factor) = 3

브로커 1 (Leader): ┌─────────────────┐
                   │  파티션 0 리더  │ ◄── 프로듀서/컨슈머 연결
                   └─────────────────┘
                         │  복제
브로커 2 (Follower): ┌───▼─────────────┐
                   │  파티션 0 팔로워 │
                   └─────────────────┘
                         │  복제
브로커 3 (Follower): ┌───▼─────────────┐
                   │  파티션 0 팔로워 │
                   └─────────────────┘

브로커 1 장애 시 → 브로커 2 또는 3이 자동으로 리더 선출
```

**[[020_isr|ISR]](In-Sync Replicas)**: 리더와 동기화된 팔로워 집합. `acks=all`(또는 `-1`) [[009_config|설정]] 시 모든 ISR에 [[016_replication_factor|복제]] 완료 후 응답 → 최강 내구성.

### 2.4 [[179_kafka_flink_watermark_time_window|Kafka]] 에코시스템

```
┌─────────────────────────────────────────────────────────┐
│                    Kafka 에코시스템                       │
│                                                         │
│  ┌──────────────────┐   ┌──────────────────────────┐   │
│  │  Kafka Connect   │   │     Kafka Streams         │   │
│  │ (커넥터 기반     │   │ (스트림 처리 라이브러리)  │   │
│  │  데이터 이동)    │   │  조인·집계·윈도우 연산   │   │
│  └──────────────────┘   └──────────────────────────┘   │
│                                                         │
│  ┌──────────────────┐   ┌──────────────────────────┐   │
│  │  Schema Registry │   │       ksqlDB              │   │
│  │ (Avro/Protobuf   │   │ (SQL로 스트림 처리)       │   │
│  │  스키마 관리)    │   │                           │   │
│  └──────────────────┘   └──────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Kafka의 [[514_partition_slice_volume|파티션]]·[[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] [[083_relationship_in_er_model|관계]]는 '고속도로 요금소'다 — [[514_partition_slice_volume|파티션]]은 차선, 컨슈머는 요금소 직원이다. 차선([[514_partition_slice_volume|파티션]])을 늘리면 [[139_throughput|처리량]]이 증가하고, 각 직원은 자기 차선만 담당한다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[179_kafka_flink_watermark_time_window|Kafka]] vs 경쟁 기술

| 항목 | Apache [[179_kafka_flink_watermark_time_window|Kafka]] | AWS Kinesis | RabbitMQ | Pulsar |
|:---|:---|:---|:---|:---|
| **관리 방식** | 자체 운영 | 완전 관리형 | 자체 운영 | 자체/관리형 |
| **보존 기간** | [[009_config|설정]] 가능 (무제한) | 24시간~7일 | 소비 즉시 삭제 | 무제한 |
| **[[015_지연_데이터_관점|지연]]** | ms 단위 | ms 단위 | ms 단위 | ms 단위 |
| **[[888_multi_tenant_cloud_resource_isolation_noisy_neighbor|멀티 테넌트]]** | 제한적 | AWS 계정 단위 | 제한적 | 기본 지원 |

### 3.2 오프셋 관리 [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 설명 | [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] |
|:---|:---|:---|
| **자동 커밋** | `enable.auto.commit=true` | 처리 전 커밋 시 [[001_dikw_pyramid|데이터]] 손실 |
| **수동 커밋** | 처리 완료 후 명시적 커밋 | 중복 처리 가능성 (At-Least-Once) |
| **정확히 한번** | [[083_cross_validation|Exactly-Once Semantics]] (EOS) | [[191_transaction_concept_states|트랜잭션]] [[014_api_posix|API]] 필요, 오버헤드 |

📢 **섹션 요약 비유**: 오프셋은 소설책의 책갈피다 — 어디까지 읽었는지 기록해두면 나중에 이어서 읽을 수 있고, 한 권의 책을 여러 사람이 동시에 다른 진도로 읽을 수도 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]] 수 설계 가이드

```
파티션 수 = max(컨슈머 수, 목표 처리량 / 단일 파티션 처리량)

예시:
- 목표 처리량: 100만 TPS
- 단일 파티션 처리량: 10만 TPS
- 최소 파티션 수 = 100만 / 10만 = 10개
- 컨슈머 수 = 10개 (1:1 매핑)

주의: 파티션 수는 나중에 늘릴 수 있지만 줄이기는 불가
     → 처음에 여유있게 설계 권장
```

### 4.2 [[179_kafka_flink_watermark_time_window|Kafka]] Connect를 이용한 [[217_cdc_binlog_change_capture_debezium|CDC]] 파이프라인

```
MySQL DB ──► Debezium Connector ──► Kafka 토픽 ──► Sink Connector ──► DW
           (Source Connector)      "db.orders"   (JDBC/S3 Sink)
```

[[179_kafka_flink_watermark_time_window|Kafka]] Connect는 소스(Source)와 싱크(Sink) 커넥터로 외부 시스템과 Kafka를 연결하며, Debezium은 대표적인 [[217_cdc_binlog_change_capture_debezium|CDC]] Source 커넥터다.

📢 **섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] Connect는 Kafka라는 [[152_hub_dummy_switching_intelligent|허브]] 공항의 '수하물 컨베이어'다 — 각 항공사(소스 시스템)에서 짐([[001_dikw_pyramid|데이터]])을 받아 Kafka를 거쳐 목적지 컨베이어(싱크)로 자동 배달한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[179_kafka_flink_watermark_time_window|Kafka]] 도입 효과

| 효과 | 내용 |
|:---|:---|
| **디커플링** | 프로듀서·컨슈머 독립 — [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[195_coupling_levels|결합도]] 감소 |
| **내결함성** | 리플리케이션으로 브로커 장애 시에도 무중단 |
| **재처리** | 오프셋 리셋으로 과거 [[001_dikw_pyramid|데이터]] 재처리 가능 |
| **확장성** | [[514_partition_slice_volume|파티션]] 추가만으로 [[139_throughput|처리량]] 선형 증가 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"[[514_partition_slice_volume|파티션]]이 [[179_kafka_flink_watermark_time_window|Kafka]] 성능과 [[430_index_fast_full_scan|병렬]]성의 근간"**임을 강조하고, [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]]의 [[514_partition_slice_volume|파티션]] 할당 메커니즘, [[020_isr|ISR]] 기반 내결함성, 오프셋 커밋 [[268_strategy_pattern|전략]](At-Most-Once / At-Least-Once / Exactly-Once)을 함께 논술하면 고득점이다.

📢 **섹션 요약 비유**: Kafka는 현대 [[001_dikw_pyramid|데이터]] 인프라의 '중앙 혈관'이다 — 모든 [[090_service_kubernetes_network_load_balancing|서비스]]가 이 혈관을 통해 [[001_dikw_pyramid|데이터]]를 주고받으며, 혈관이 막히지 않도록 [[514_partition_slice_volume|파티션]](굵기)을 늘리고 리플리케이션([[555_backup_and_restore_strategy|백업]] 혈관)을 유지한다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 메시지 [[104_classification_analysis|분류]] | 토픽 (Topic) | 메시지 채널 단위 |
| [[430_index_fast_full_scan|병렬]] 처리 단위 | [[514_partition_slice_volume|파티션]] ([[514_partition_slice_volume|Partition]]) | 토픽 분할, [[139_throughput|처리량]] 확장 |
| 읽기 위치 추적 | 오프셋 (Offset) | [[514_partition_slice_volume|파티션]] 내 메시지 순서 번호 |
| [[430_index_fast_full_scan|병렬]] 컨슈머 관리 | [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] ([[191_consumer_group_kafka_partition_load_balancing|Consumer Group]]) | [[514_partition_slice_volume|파티션]]을 컨슈머에 할당 |
| 내결함성 | [[020_isr|ISR]] (In-Sync Replicas) | 동기화된 [[016_replication_factor|복제]]본 집합 |
| 외부 연동 | [[179_kafka_flink_watermark_time_window|Kafka]] Connect | 소스/싱크 커넥터 프레임워크 |
| [[229_stream_processing_kafka_flink|스트림 처리]] | [[179_kafka_flink_watermark_time_window|Kafka]] Streams / ksqlDB | 토픽 내 실시간 [[001_dikw_pyramid|데이터]] 처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. Kafka는 여러 방송국(프로듀서)이 보내는 채널(토픽)을 여러 시청자(컨슈머)가 각자 원하는 속도로 보는 케이블 TV야.

### 📈 관련 키워드 및 발전 흐름도

```text
포인트-투-포인트 메시징 (단일 소비자)
    │
    ▼
Pub/Sub 패턴: 다중 소비자 독립 구독
    │
    ▼
Kafka: Topic · Partition · Offset · Broker 클러스터
    ├─► Producer: 키 기반 파티셔닝
    └─► Consumer Group: 파티션별 분산 소비
    │
    ▼
Kafka Connect + Schema Registry → 데이터 통합 허브
```
2. [[514_partition_slice_volume|파티션]]은 채널을 여러 조각으로 나눠서 여러 TV(컨슈머)가 동시에 시청하게 하는 것 — 채널 조각이 많을수록 더 많은 TV가 동시에 볼 수 있어!
3. 오프셋은 '어디까지 봤어요' 표시야 — TV를 껐다 켜도 이어보기가 되고, 다른 사람이 봐도 내 진도는 그대로야.
