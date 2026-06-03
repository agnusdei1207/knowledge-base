+++
title = "26. Kafka 토픽 파티션 (Topic Partition) — 분산 스트림 병렬 처리"
date = 2026-04-29

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kafka의 토픽 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(Topic [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))은 하나의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스트림(Topic)을 순서 보장이 가능한 독립적인 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 단위로 분할한 것으로, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수를 늘릴수록 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))이 선형적으로 증가한다.
> 2. **가치**: [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)의 핵심 트레이드오프는 "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성(Parallelism) vs. 순서 보장([Ordering](/knowledge-base/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/))"이다. 전체 토픽 레벨에서는 순서가 보장되지 않지만, 같은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내 메시지는 프로듀서 삽입 순서가 보장된다. 동일 키를 가진 메시지는 항상 같은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)되므로 키 기반 순서 보장이 가능하다.
> 3. **판단 포인트**: [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 설계 공식 = `max(프로듀서 처리량 / 파티션당 프로듀서 처리량, 컨슈머 처리량 / 파티션당 컨슈머 처리량)`. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수는 늘릴 수 있지만 줄이기는 어렵고, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 많아질수록 브로커 메모리 사용량·리더 선출 시간이 증가하므로 과도한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 역효과다.

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

- **📢 섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 고속도로 다차선이다. 1차선이면 차가 한 줄로 줄 서야 하지만, 3차선이면 3배 많은 차량이 동시에 달릴 수 있다. 단, 같은 목적지(키)의 차량은 항상 같은 차선([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 이용한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내부 구조

```text
파티션 0 (Offset 기반 순서 로그):
  Offset: 0        1        2        3
          [msg_A] → [msg_B] → [msg_C] → [msg_D]
                                              ↑ LEO (Log End Offset)

Leader Partition: 읽기/쓰기 처리
Follower Partition: ISR (In-Sync Replicas) — 복제본
```

### [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 동작 | 사용 케이스 |
|:---|:---|:---|
| **Round-Robin** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에 순서대로 분배 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 극대화 |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> Hash</strong> | hash([key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) % partitions | 동일 키 순서 보장 |
| **Custom Partitioner** | 커스텀 로직 | 특정 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 집중 |

- **📢 섹션 요약 비유**: 라운드로빈은 은행 대기 번호표 시스템이다. 번호 순서대로 창구에 배정한다. 키 해시는 "홍길동은 항상 3번 창구"처럼 특정 고객이 항상 같은 창구로 가도록 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | RabbitMQ 큐 | Kinesis 샤드 |
|:---|:---|:---|:---|
| 순서 보장 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내 보장 | 단일 큐 내 보장 | 샤드 내 보장 |
| 확장 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 추가 | 큐 추가 | 샤드 증가 |
| 메시지 재처리 | Offset 리셋 가능 | ACK 전 재전송 | [Iterator](/knowledge-base/studynote/04_software_engineering/04_testing_quality/270_iterator_pattern/) 리셋 |

- **📢 섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 양방향 2차선 도로다. 지나간 차(메시지)의 블랙박스(Offset) 덕분에 과거로 돌아가서 다시 재생할 수 있다. RabbitMQ는 일방통행 도로로 한 번 지나가면 사라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 설계 기준
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

### [ISR](/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/) (In-Sync Replicas) 관리
- [ISR](/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/): 리더 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)과 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 상태를 유지하는 팔로워 집합.
- min.insync.replicas=2: 최소 2개 [ISR](/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(Ack). 내구성 보장.

- **📢 섹션 요약 비유**: ISR은 비행기 블랙박스 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 시스템이다. 리더 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(메인 블랙박스)과 팔로워([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본)가 항상 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)되어 있어, 리더가 고장 나도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 사라지지 않는다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **수평 확장** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 추가로 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 선형 증가 |
| **순서 보장** | 키 기반 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)으로 이벤트 순서 유지 |
| **내구성** | [ISR](/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 브로커 장애 시 무손실 |

[Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 [이벤트 드리븐 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/214_eda_event_driven_architecture_async/)([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/)), 실시간 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)), [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 비동기 통신의 핵심 인프라로, 스트리밍 ML 파이프라인과 결합하여 실시간 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론 플랫폼의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 백본으로 발전 중이다.

- **📢 섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 현대 디지털 도시의 고속 지하철 다노선 시스템이다. 노선([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 늘릴수록 더 많은 승객([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 동시에 이동시킬 수 있고, 같은 노선(키)은 항상 같은 방향으로 간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Offset** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내 메시지 순서의 논리적 주소 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/">Consumer Group</a></strong> | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 분담하는 컨슈머 집합 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/">ISR</a></strong> | 리더와 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)된 팔로워 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 집합 |
| **Broker** | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)의 물리적 저장 노드 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">CDC</a></strong> | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 기반 DB 변경 스트림 |

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

1. [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 고속도로 여러 차선이에요! 차선이 많을수록 더 많은 차(메시지)가 동시에 달릴 수 있어요.
2. 같은 차 번호판(키)을 가진 차는 항상 같은 차선([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))으로 가서, 순서가 뒤섞이지 않아요!
3. 블랙박스(Offset) 덕분에 과거 어느 시점으로도 돌아가서 메시지를 다시 읽을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 258

← **이전**: [25. Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)
**다음**: [27. Kafka 오프셋 & 컨슈머 그룹 (Offset & Consumer Group)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/027_offset_consumer_group/) →

---
