---
title: "214. 아파치 카프카 (Apache Kafka) Pub-Sub 토픽 파티션 오프셋 브로커"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Kafka는 Pub-Sub(Publish-Subscribe) 메시징 패턴 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 스트리밍 플랫폼으로, 토픽(Topic)을 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))으로 분할해 수평 확장하며, 오프셋(Offset)으로 각 컨슈머의 읽기 위치를 독립적으로 추적한다.
> 2. **가치**: [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 단위 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리와 리플리케이션([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))으로 초당 수백만 건 메시지를 내결함성([Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))을 유지하며 처리하고, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect·[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams 에코시스템이 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 전반을 담당한다.
> 3. **판단 포인트**: Kafka는 "메시지를 소비해도 삭제하지 않는다" — 이 원칙이 멀티 컨슈머 독립 처리, 재처리, [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/))을 가능하게 하는 핵심 설계 철학이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 전통적 메시지 큐 vs [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)

| 항목 | 전통 MQ (RabbitMQ 등) | Apache [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) |
|:---|:---|:---|
| **소비 후 삭제** | 소비 시 즉시 삭제 | 보존 기간([retention](/studynote/05_database/04_transactions_concurrency/515_mvcc/)) 동안 유지 |
| **순서 보장** | 큐 수준 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수준 |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | 수직 확장 위주 | 수평 확장 ([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 추가) |
| **재처리** | 불가 | 오프셋 리셋으로 가능 |
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a></strong> | 중간 (수만 TPS) | 초고성능 (수백만 TPS) |
| **주요 용도** | 작업 큐, [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) | 이벤트 스트리밍, [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/) |

### 1.2 Kafka의 핵심 설계 원칙

Kafka는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(Log) 자료구조를 기반으로 설계되었다. 메시지는 순서대로 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 추가(Append-Only)되며, 컨슈머는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 읽을 뿐 지우지 않는다.

```
Kafka 토픽 = 무한히 이어지는 기록지(Append-Only Log)

오프셋:  0     1     2     3     4     5   ...
        +---+-----+-----+-----+-----+-----+
메시지:  | A |  B  |  C  |  D  |  E  |  F  | --► 계속 추가
        +---+-----+-----+-----+-----+-----+
컨슈머1:                    ^ (오프셋 3 읽는 중)
컨슈머2:              ^ (오프셋 2 읽는 중 — 독립적!)
```

📢 **섹션 요약 비유**: Kafka는 거대한 공용 게시판이다 — 글을 올리면 모두가 볼 수 있고, 내가 어디까지 읽었는지(오프셋)는 각자 책갈피로 관리한다. 다른 사람이 읽어도 게시물은 지워지지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 핵심 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **브로커 (Broker)** | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 서버 노드 — 메시지 저장·전달 담당 |
| **토픽 (Topic)** | 메시지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 채널 (예: orders, payments, [logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) |
| <strong><a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> (<a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a>)</strong> | 토픽을 분할한 단위 — [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리의 기본 |
| **오프셋 (Offset)** | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내 메시지 순서 번호 (0부터 시작) |
| **프로듀서 (Producer)** | 메시지를 토픽에 발행(Publish)하는 주체 |
| **컨슈머 (Consumer)** | 토픽에서 메시지를 구독(Subscribe)하는 주체 |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/">컨슈머 그룹</a> (<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/">Consumer Group</a>)</strong> | 동일 토픽을 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 처리하는 컨슈머 묶음 |
| <strong>주키퍼 (<a href="/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">ZooKeeper</a>) / KRaft</strong> | 클러스터 [메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/) ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 3.x에서 KRaft로 전환) |

### 2.2 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)과 [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

```
토픽: "orders" (파티션 3개)

파티션 0: [msg0, msg3, msg6, ...]
파티션 1: [msg1, msg4, msg7, ...]
파티션 2: [msg2, msg5, msg8, ...]

컨슈머 그룹 A (컨슈머 3개 — 1:1 매핑):
+------------+------------+------------+
| Consumer-0 | Consumer-1 | Consumer-2 |
|  파티션 0  |  파티션 1  |  파티션 2  |
+------------+------------+------------+
-> 최대 처리량 (각 컨슈머가 독립 파티션 담당)

컨슈머 그룹 B (컨슈머 1개 — 전체 소비):
+--------------------------------------+
|           Consumer-0                  |
|  파티션 0 + 파티션 1 + 파티션 2      |
+--------------------------------------+
-> 단일 컨슈머가 전체 순서 처리 가능
```

**중요 규칙**: 하나의 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 동일 [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 내에서 **하나의 컨슈머에게만** 할당된다 -> [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)처리의 한계를 결정한다.

### 2.3 리플리케이션 ([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) 내결함성

```
토픽: "payments", 파티션 0, 복제 인수(Replication Factor) = 3

브로커 1 (Leader): +-----------------+
                   |  파티션 0 리더  | ◄-- 프로듀서/컨슈머 연결
                   +-----------------+
                         |  복제
브로커 2 (Follower): +---v-------------+
                   |  파티션 0 팔로워 |
                   +-----------------+
                         |  복제
브로커 3 (Follower): +---v-------------+
                   |  파티션 0 팔로워 |
                   +-----------------+

브로커 1 장애 시 -> 브로커 2 또는 3이 자동으로 리더 선출
```

<strong><a href="/studynote/02_operating_system/01_overview_architecture/020_isr/">ISR</a>(In-Sync Replicas)</strong>: 리더와 동기화된 팔로워 집합. `acks=all`(또는 `-1`) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 시 모든 ISR에 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 완료 후 응답 -> 최강 내구성.

### 2.4 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 에코시스템

```
+---------------------------------------------------------+
|                    Kafka 에코시스템                       |
|                                                         |
|  +------------------+   +--------------------------+   |
|  |  Kafka Connect   |   |     Kafka Streams         |   |
|  | (커넥터 기반     |   | (스트림 처리 라이브러리)  |   |
|  |  데이터 이동)    |   |  조인·집계·윈도우 연산   |   |
|  +------------------+   +--------------------------+   |
|                                                         |
|  +------------------+   +--------------------------+   |
|  |  Schema Registry |   |       ksqlDB              |   |
|  | (Avro/Protobuf   |   | (SQL로 스트림 처리)       |   |
|  |  스키마 관리)    |   |                           |   |
|  +------------------+   +--------------------------+   |
+---------------------------------------------------------+
```

📢 **섹션 요약 비유**: Kafka의 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)·[컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 '고속도로 요금소'다 — [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 차선, 컨슈머는 요금소 직원이다. 차선([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 늘리면 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 증가하고, 각 직원은 자기 차선만 담당한다.

---

## Ⅲ. 비교 및 연결

### 3.1 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) vs 경쟁 기술

| 항목 | Apache [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | AWS Kinesis | RabbitMQ | Pulsar |
|:---|:---|:---|:---|:---|
| **관리 방식** | 자체 운영 | 완전 관리형 | 자체 운영 | 자체/관리형 |
| **보존 기간** | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 가능 (무제한) | 24시간~7일 | 소비 즉시 삭제 | 무제한 |
| <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong> | ms 단위 | ms 단위 | ms 단위 | ms 단위 |
| <strong><a href="/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/">멀티 테넌트</a></strong> | 제한적 | AWS 계정 단위 | 제한적 | 기본 지원 |

### 3.2 오프셋 관리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) |
|:---|:---|:---|
| **자동 커밋** | `enable.auto.commit=true` | 처리 전 커밋 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 |
| **수동 커밋** | 처리 완료 후 명시적 커밋 | 중복 처리 가능성 (At-Least-Once) |
| **정확히 한번** | [Exactly-Once Semantics](/studynote/12_it_management/02_itsm_itil/083_cross_validation/) (EOS) | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 필요, 오버헤드 |

📢 **섹션 요약 비유**: 오프셋은 소설책의 책갈피다 — 어디까지 읽었는지 기록해두면 나중에 이어서 읽을 수 있고, 한 권의 책을 여러 사람이 동시에 다른 진도로 읽을 수도 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 설계 가이드

```
파티션 수 = max(컨슈머 수, 목표 처리량 / 단일 파티션 처리량)

예시:
- 목표 처리량: 100만 TPS
- 단일 파티션 처리량: 10만 TPS
- 최소 파티션 수 = 100만 / 10만 = 10개
- 컨슈머 수 = 10개 (1:1 매핑)

주의: 파티션 수는 나중에 늘릴 수 있지만 줄이기는 불가
     -> 처음에 여유있게 설계 권장
```

### 4.2 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect를 이용한 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 파이프라인

```
MySQL DB --► Debezium Connector --► Kafka 토픽 --► Sink Connector --► DW
           (Source Connector)      "db.orders"   (JDBC/S3 Sink)
```

[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect는 소스(Source)와 싱크(Sink) 커넥터로 외부 시스템과 Kafka를 연결하며, Debezium은 대표적인 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) Source 커넥터다.

📢 **섹션 요약 비유**: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect는 Kafka라는 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 공항의 '수하물 컨베이어'다 — 각 항공사(소스 시스템)에서 짐([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 받아 Kafka를 거쳐 목적지 컨베이어(싱크)로 자동 배달한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 도입 효과

| 효과 | 내용 |
|:---|:---|
| **디커플링** | 프로듀서·컨슈머 독립 — [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 감소 |
| **내결함성** | 리플리케이션으로 브로커 장애 시에도 무중단 |
| **재처리** | 오프셋 리셋으로 과거 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재처리 가능 |
| **확장성** | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 추가만으로 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 선형 증가 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 <strong>"<a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a>이 <a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a> 성능과 <a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성의 근간"</strong>임을 강조하고, [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/)의 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 할당 메커니즘, [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 기반 내결함성, 오프셋 커밋 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(At-Most-Once / At-Least-Once / Exactly-Once)을 함께 논술하면 고득점이다.

📢 **섹션 요약 비유**: Kafka는 현대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 인프라의 '중앙 혈관'이다 — 모든 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이 혈관을 통해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받으며, 혈관이 막히지 않도록 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(굵기)을 늘리고 리플리케이션([백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 혈관)을 유지한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 메시지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 토픽 (Topic) | 메시지 채널 단위 |
| [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 단위 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) ([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) | 토픽 분할, [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 확장 |
| 읽기 위치 추적 | 오프셋 (Offset) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내 메시지 순서 번호 |
| [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 컨슈머 관리 | [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) ([Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/)) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 컨슈머에 할당 |
| 내결함성 | [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) (In-Sync Replicas) | 동기화된 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 집합 |
| 외부 연동 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect | 소스/싱크 커넥터 프레임워크 |
| [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams / ksqlDB | 토픽 내 실시간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. Kafka는 여러 방송국(프로듀서)이 보내는 채널(토픽)을 여러 시청자(컨슈머)가 각자 원하는 속도로 보는 케이블 TV야.

### 📈 관련 키워드 및 발전 흐름도

```text
포인트-투-포인트 메시징 (단일 소비자)
    |
    v
Pub/Sub 패턴: 다중 소비자 독립 구독
    |
    v
Kafka: Topic · Partition · Offset · Broker 클러스터
    +-► Producer: 키 기반 파티셔닝
    +-► Consumer Group: 파티션별 분산 소비
    |
    v
Kafka Connect + Schema Registry -> 데이터 통합 허브
```
2. [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 채널을 여러 조각으로 나눠서 여러 TV(컨슈머)가 동시에 시청하게 하는 것 — 채널 조각이 많을수록 더 많은 TV가 동시에 볼 수 있어!
3. 오프셋은 '어디까지 봤어요' 표시야 — TV를 껐다 켜도 이어보기가 되고, 다른 사람이 봐도 내 진도는 그대로야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 214 / 258

<- **이전**: [213. 데이터 레이크하우스 (Data Lakehouse) Delta Lake 파케이 ACID](/studynote/14_data_engineering/05_exam_keywords/213_data_lakehouse_delta_lake_parquet_acid/)
**다음**: [215. 아파치 플링크 (Apache Flink) 네이티브 스트림 워터마크 윈도우](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) ->

---
