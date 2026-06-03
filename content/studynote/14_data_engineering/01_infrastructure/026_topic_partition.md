---
title: 26. Kafka 토픽 파티션 (Topic Partition) — 분산 스트림 병렬 처리
date: '2026-04-29'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kafka의 토픽 [[514_partition_slice_volume|파티션]](Topic [[514_partition_slice_volume|Partition]])은 하나의 [[001_dikw_pyramid|데이터]] 스트림(Topic)을 순서 보장이 가능한 독립적인 [[568_logs_distributed_logging_elk_fluentd|로그]] 단위로 분할한 것으로, [[514_partition_slice_volume|파티션]] 수를 늘릴수록 [[430_index_fast_full_scan|병렬]] 처리 [[139_throughput|처리량]]([[139_throughput|throughput]])이 선형적으로 증가한다.
> 2. **가치**: [[514_partition_slice_volume|파티션]]의 핵심 트레이드오프는 "[[430_index_fast_full_scan|병렬]]성(Parallelism) vs. 순서 보장([[277_semaphore_ordering|Ordering]])"이다. 전체 토픽 레벨에서는 순서가 보장되지 않지만, 같은 [[514_partition_slice_volume|파티션]] 내 메시지는 프로듀서 삽입 순서가 보장된다. 동일 키를 가진 메시지는 항상 같은 [[514_partition_slice_volume|파티션]]에 [[339_routing_overview_best_path_selection|라우팅]]되므로 키 기반 순서 보장이 가능하다.
> 3. **판단 포인트**: [[514_partition_slice_volume|파티션]] 수 설계 공식 = `max(프로듀서 처리량 / 파티션당 프로듀서 처리량, 컨슈머 처리량 / 파티션당 컨슈머 처리량)`. [[514_partition_slice_volume|파티션]] 수는 늘릴 수 있지만 줄이기는 어렵고, [[514_partition_slice_volume|파티션]] 수가 많아질수록 브로커 메모리 사용량·리더 선출 시간이 증가하므로 과도한 [[514_partition_slice_volume|파티션]]은 역효과다.

---

## Ⅰ. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────┐
│             Kafka Topic Partition 구조                  │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Topic: user-events                                     │
│  ┌─────────────────────────────────────────┐            │
│  │ Partition 0: [msg0] → [msg3] → [msg6]  │            │
│  │ Partition 1: [msg1] → [msg4] → [msg7]  │            │
│  │ Partition 2: [msg2] → [msg5] → [msg8]  │            │
│  └─────────────────────────────────────────┘            │
│                                                         │
│  Producer → 파티션별 분배 (라운드로빈 or 키 해시)          │
│  Consumer Group → 파티션당 1 컨슈머 할당                  │
└────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]]은 고속도로 다차선이다. 1차선이면 차가 한 줄로 줄 서야 하지만, 3차선이면 3배 많은 차량이 동시에 달릴 수 있다. 단, 같은 목적지(키)의 차량은 항상 같은 차선([[514_partition_slice_volume|파티션]])을 이용한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[514_partition_slice_volume|파티션]] 내부 구조

```text
파티션 0 (Offset 기반 순서 로그):
  Offset: 0        1        2        3
          [msg_A] → [msg_B] → [msg_C] → [msg_D]
                                              ↑ LEO (Log End Offset)

Leader Partition: 읽기/쓰기 처리
Follower Partition: ISR (In-Sync Replicas) — 복제본
```

### [[514_partition_slice_volume|파티션]] [[339_routing_overview_best_path_selection|라우팅]] [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 동작 | 사용 케이스 |
|:---|:---|:---|
| **Round-Robin** | [[514_partition_slice_volume|파티션]]에 순서대로 분배 | [[139_throughput|처리량]] 극대화 |
| **[[067_db_key_uniqueness_minimality|Key]] Hash** | hash([[067_db_key_uniqueness_minimality|key]]) % partitions | 동일 키 순서 보장 |
| **Custom Partitioner** | 커스텀 로직 | 특정 [[514_partition_slice_volume|파티션]] 집중 |

- **📢 섹션 요약 비유**: 라운드로빈은 은행 대기 번호표 시스템이다. 번호 순서대로 창구에 배정한다. 키 해시는 "홍길동은 항상 3번 창구"처럼 특정 고객이 항상 같은 창구로 가도록 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]] | RabbitMQ 큐 | Kinesis 샤드 |
|:---|:---|:---|:---|
| 순서 보장 | [[514_partition_slice_volume|파티션]] 내 보장 | 단일 큐 내 보장 | 샤드 내 보장 |
| 확장 | [[514_partition_slice_volume|파티션]] 추가 | 큐 추가 | 샤드 증가 |
| 메시지 재처리 | Offset 리셋 가능 | ACK 전 재전송 | [[270_iterator_pattern|Iterator]] 리셋 |

- **📢 섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]]은 양방향 2차선 도로다. 지나간 차(메시지)의 블랙박스(Offset) 덕분에 과거로 돌아가서 다시 재생할 수 있다. RabbitMQ는 일방통행 도로로 한 번 지나가면 사라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[514_partition_slice_volume|파티션]] 수 설계 기준
```text
요구사항:
  - 초당 100만 메시지 처리 (Producer)
  - 파티션당 최대 3만 TPS (브로커 디스크 순차 쓰기 한계)
  - 컨슈머 처리량: 파티션당 5만 TPS

설계:
  min partitions = ceil(1,000,000 / 30,000) = 34 파티션
  → 여유 포함 40 파티션으로 설정
  → replication-factor = 3 (내구성)
```

### [[020_isr|ISR]] (In-Sync Replicas) 관리
- [[020_isr|ISR]]: 리더 [[514_partition_slice_volume|파티션]]과 [[212_synchronization_mechanisms|동기화]] 상태를 유지하는 팔로워 집합.
- min.insync.replicas=2: 최소 2개 [[020_isr|ISR]] [[396_validation|확인]] 후 [[289_cqrs_db|쓰기]] [[396_validation|확인]](Ack). 내구성 보장.

- **📢 섹션 요약 비유**: ISR은 비행기 블랙박스 [[016_replication_factor|복제]] 시스템이다. 리더 [[514_partition_slice_volume|파티션]](메인 블랙박스)과 팔로워([[016_replication_factor|복제]]본)가 항상 [[212_synchronization_mechanisms|동기화]]되어 있어, 리더가 고장 나도 [[001_dikw_pyramid|데이터]]가 사라지지 않는다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **수평 확장** | [[514_partition_slice_volume|파티션]] 추가로 [[139_throughput|처리량]] 선형 증가 |
| **순서 보장** | 키 기반 [[514_partition_slice_volume|파티션]] [[339_routing_overview_best_path_selection|라우팅]]으로 이벤트 순서 유지 |
| **내구성** | [[020_isr|ISR]] [[016_replication_factor|복제]]로 브로커 장애 시 무손실 |

[[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]]은 [[214_eda_event_driven_architecture_async|이벤트 드리븐 아키텍처]]([[064_eda|EDA]]), 실시간 [[217_cdc_binlog_change_capture_debezium|CDC]]([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]), [[532_microservices_decomposition_patterns|마이크로서비스]] 비동기 통신의 핵심 인프라로, 스트리밍 ML 파이프라인과 결합하여 실시간 [[190_ai_llm_requirements_specification|AI]] 추론 플랫폼의 [[001_dikw_pyramid|데이터]] 백본으로 발전 중이다.

- **📢 섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]]은 현대 디지털 도시의 고속 지하철 다노선 시스템이다. 노선([[514_partition_slice_volume|파티션]])을 늘릴수록 더 많은 승객([[001_dikw_pyramid|데이터]])을 동시에 이동시킬 수 있고, 같은 노선(키)은 항상 같은 방향으로 간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Offset** | [[514_partition_slice_volume|파티션]] 내 메시지 순서의 논리적 주소 |
| **[[191_consumer_group_kafka_partition_load_balancing|Consumer Group]]** | [[514_partition_slice_volume|파티션]]을 분담하는 컨슈머 집합 |
| **[[020_isr|ISR]]** | 리더와 [[212_synchronization_mechanisms|동기화]]된 팔로워 [[016_replication_factor|복제]]본 집합 |
| **Broker** | [[514_partition_slice_volume|파티션]]의 물리적 저장 노드 |
| **[[217_cdc_binlog_change_capture_debezium|CDC]]** | [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]] 기반 DB 변경 스트림 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 큐 메시징 — 순서 보장, 확장 한계]
    │
    ▼
[Kafka 토픽 파티션 — 병렬 분산 로그 스트림]
    │
    ▼
[Consumer Group — 파티션별 병렬 소비]
    │
    ▼
[Kafka Streams / Flink — 파티션 기반 상태 연산]
    │
    ▼
[실시간 AI 파이프라인 — 스트리밍 ML 추론 백본]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[179_kafka_flink_watermark_time_window|Kafka]] [[514_partition_slice_volume|파티션]]은 고속도로 여러 차선이에요! 차선이 많을수록 더 많은 차(메시지)가 동시에 달릴 수 있어요.
2. 같은 차 번호판(키)을 가진 차는 항상 같은 차선([[514_partition_slice_volume|파티션]])으로 가서, 순서가 뒤섞이지 않아요!
3. 블랙박스(Offset) 덕분에 과거 어느 시점으로도 돌아가서 메시지를 다시 읽을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 258

← **이전**: [[025_spark_rdd_resilient_distributed_dataset|25. Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋]]
**다음**: [[027_offset_consumer_group|27. Kafka 오프셋 & 컨슈머 그룹 (Offset & Consumer Group)]] →

---
