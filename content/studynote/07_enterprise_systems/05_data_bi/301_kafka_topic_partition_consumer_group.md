---
title: "301. 카프카 토픽 파티셔닝 기반 컨슈머 그룹 부하 분산 (Kafka Topic Partition Consumer Group)"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kafka의 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 최소 단위이며, [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 내 컨슈머 수와 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수의 비율이 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 직결된다.
> 2. **가치**: 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(MB/s) = [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 × 컨슈머당 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(MB/s) 공식으로 수평 확장 상한을 사전에 설계할 수 있다.
> 3. **판단 포인트**: [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수는 한번 늘리면 줄일 수 없으므로, 최소 예상 피크 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ÷ 컨슈머 단위 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) × 2배 여유로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 설계한다.

## Ⅰ. 개요 및 필요성

[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) ([Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/))는 LinkedIn이 설계한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 스트리밍 플랫폼으로, 초당 수백만 건의 이벤트를 처리한다.
토픽(Topic)은 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 채널이며, 이를 물리적으로 분할한 단위가 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))이다.
하나의 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 오직 하나의 컨슈머에게만 할당되므로([컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 내), [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 상한을 결정한다.

[컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/)([Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/))은 같은 `group.id`를 공유하는 컨슈머들의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 집합이다.
그룹 내 컨슈머들은 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 나눠 소비하므로 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)이 가능하다.
반면 서로 다른 그룹은 동일 토픽 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 독립적으로 소비하므로, 하나의 토픽을 여러 하위 시스템이 동시에 구독하는 브로드캐스트 패턴을 구현할 수 있다.

[처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 설계 공식:
```
전체 처리량(MB/s) = 파티션 수 × 컨슈머당 처리량(MB/s)
예) 파티션 12개 × 컨슈머당 50 MB/s = 600 MB/s 피크 처리 가능
```

[파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 설계 원칙:
- 너무 적으면: [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 병목, 컨슈머 추가해도 효과 없음
- 너무 많으면: 브로커 메모리 압박, [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)/KRaft [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 과부하
- 권장: 브로커당 2,000~4,000 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 이내 유지 ([Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) 권장)

📢 **섹션 요약 비유**: [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 고속도로 차선, 컨슈머는 차량이다. 차선 수보다 차가 많아봐야 차선 수만큼밖에 통행하지 못한다.

## Ⅱ. 아키텍처 및 핵심 원리

### [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 할당 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) ([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Assignment [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 동작 방식 | 특징 | 적합 상황 |
|:---|:---|:---|:---|
| RangeAssignor | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 범위를 컨슈머에 균등 분할 | 구현 단순, 불균형 발생 가능 | 소수 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) |
| RoundRobinAssignor | [라운드 로빈](/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) 방식으로 순환 배분 | 균형 우수 | 토픽 다수 구독 |
| StickyAssignor | 리밸런싱 시 기존 할당 최대 유지 | 리밸런싱 비용 최소화 | [스테이트](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)풀 컨슈머 |
| CooperativeStickyAssignor | 점진적 리밸런싱 (Incremental) | 중단 없는 리밸런싱 | 프로덕션 권장 |

### 오프셋 커밋 (Offset Commit) 방식

| 방식 | 설명 | 위험성 |
|:---|:---|:---|
| Auto commit | 5초 주기 자동 커밋 (기본) | 중복 또는 유실 가능 |
| Manual sync commit | commitSync() 직접 호출 | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 저하 |
| Manual async commit | commitAsync() + 콜백 | 재시도 순서 역전 주의 |

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: 토픽 4파티션 -> [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 2대

```
  Topic: user-events (파티션 4개)
  +--------------------------------------------------------------+
  |  Partition-0   |  Partition-1   |  Partition-2   |  Partition-3   |
  +-------+--------+-------+--------+-------+--------+-------+--------+
          |                |                |                |
          v                v                v                v
  +-------------------------------------------------------------------+
  |                Consumer Group: analytics-group                    |
  |   +-----------------------------+   +--------------------------+  |
  |   |         Consumer-A          |   |         Consumer-B       |  |
  |   |   (Partition-0, P-1 담당)   |   |   (Partition-2, P-3 담당)|  |
  |   +-----------------------------+   +--------------------------+  |
  +-------------------------------------------------------------------+
                | 오프셋 커밋
  +---------------------+
  |  Kafka Broker       |  __consumer_offsets 토픽
  |  P-0: 48200         |  P-1: 50100
  |  P-2: 47900         |  P-3: 51200
  +---------------------+
```

### [Consumer Lag](/studynote/16_bigdata/04_streaming/089_consumer_lag/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링

```
Consumer Lag = Log End Offset - Consumer Commit Offset
Lag > 10,000건 -> 알람 -> 컨슈머 추가 or 처리 로직 최적화
```

📢 **섹션 요약 비유**: 오프셋은 책갈피다. 책갈피를 자주 꽂을수록 재시작 시 읽을 분량이 줄어들지만, 너무 자주 꽂으면 손이 바빠진다.

## Ⅲ. 비교 및 연결

### [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) vs 브로드캐스트 (다수 그룹)

| 항목 | [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) (1그룹 N컨슈머) | 브로드캐스트 (N그룹 각 1컨슈머) |
|:---|:---|:---|
| [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 처리 | 각 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 1컨슈머만 처리 | 모든 그룹이 동일 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 수신 |
| 활용 패턴 | 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 수평 확장 | 이벤트 팬아웃 (결제+알림+분석) |
| 오프셋 관리 | 그룹 단위 공유 | 그룹별 독립 관리 |

### Push vs Pull 모델

| 항목 | Push (RabbitMQ 방식) | Pull ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 방식) |
|:---|:---|:---|
| 처리 속도 제어 | 브로커가 전송 속도 결정 | 컨슈머가 자신의 속도로 인출 |
| 백프레셔 | 어렵다 | 자연스럽게 지원 |
| [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 재처리 | 복잡 (ACK 메커니즘) | 오프셋 리셋으로 간단히 재처리 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 낮음 (즉시 전달) | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 주기만큼 추가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |

📢 **섹션 요약 비유**: Push는 식당 서버가 음식을 가져다주는 것, Pull은 뷔페에서 내가 원할 때 가져오는 것이다. 뷔페(Pull)에서는 내 속도에 맞춰 먹을 수 있다.

## Ⅳ. 실무 적용 및 기술사 판단

### [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 설계 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 예상 피크 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 수(건/초) × 평균 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 크기(KB) = 목표 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(MB/s) 계산
- [ ] 컨슈머 단위 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 벤치마크 (일반적으로 50~100 MB/s/컨슈머)
- [ ] [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 = 목표 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ÷ 컨슈머 단위 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) × 1.5배(여유)
- [ ] [replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/).factor=3 (최소), min.insync.replicas=2 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- [ ] CooperativeStickyAssignor 적용으로 무중단 리밸런싱 확보

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| enable.auto.commit=true + 무거운 처리 | 처리 전 커밋 -> 유실 | 수동 커밋 + [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 처리 |
| 단일 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 쏠림 | 핫 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(Hotspot) | 복합 키 or 랜덤 솔팅 |
| [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 = 컨슈머 수 고정 | 탄력적 확장 불가 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 여유분 확보 |
| 리밸런싱 무시 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 수초 | CooperativeStickyAssignor 적용 |

📢 **섹션 요약 비유**: [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 설계는 고속도로 건설과 같다. 준공 후 차선을 줄이기는 매우 어려우므로, 처음부터 충분한 여유 차선을 확보해야 한다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | Before (단일 큐) | After ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)) |
|:---|:---|:---|
| [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | 수천 건/초 | 수백만 건/초 (수평 확장) |
| 장애 내성 | [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | 레플리카로 고가용성 |
| 재처리 | 불가 (삭제됨) | 오프셋 리셋으로 가능 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 수ms (단순) | 수ms~수십ms ([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) + [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) |

### 한계 및 선결 과제

- [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수는 증가만 가능, 감소 불가 -> [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 설계가 중요
- Kafka는 at-least-once 기본 -> [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)(Idempotent) 처리를 컨슈머가 보장
- [exactly-once semantics](/studynote/12_it_management/02_itsm_itil/083_cross_validation/) (EOS) 사용 시 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~30% 저하

📢 **섹션 요약 비유**: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 여러 계산대를 열어 계산대마다 전담 직원을 배치한 대형마트다. 계산대([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))가 많을수록 손님([메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지)을 빠르게 처리하지만, 너무 많으면 직원 관리 비용도 늘어난다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Topic | 포함 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 묶음 |
| [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 단위 | 물리적 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위 |
| [Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) | 소비자 단위 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 나눠 소비하는 그룹 |
| Offset | 위치 추적 | 컨슈머가 읽은 마지막 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 위치 |
| Rebalancing | 재배분 이벤트 | 컨슈머 수 변경 시 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 재할당 |
| [Consumer Lag](/studynote/16_bigdata/04_streaming/089_consumer_lag/) | [처리 지연](/studynote/03_network/01_data_communication/019_처리_지연/) 지표 | Log End Offset - 커밋 Offset |

### 📈 관련 키워드 및 발전 흐름도

```
단일 큐 메시지 브로커 - 처리량 병목
    |
    v
Kafka Topic - 논리적 데이터 채널 추상화
    |
    v
Partition - 물리적 분산·병렬 처리 단위
    |
    v
Consumer Group - 파티션별 독립 소비자 배정
    |
    v
Replication Factor + ISR = 고가용성 보장
```

> **키워드**: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Topic, [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), [Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/), Offset, [Replication Factor](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/), Producer, Broker

### 👶 어린이를 위한 3줄 비유 설명

1. 토픽은 학교 알림판이고, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 알림판을 반별로 나눈 구역이에요.
2. [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/)은 각 구역 담당 학생 모둠이고, 한 구역은 한 학생만 담당해요.
3. 오프셋은 어디까지 읽었는지 표시하는 책갈피예요. 덕분에 다음 날에도 이어서 읽을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 301 / 482

<- **이전**: [300. 실시간 데이터 스트리밍 (Kafka + CDC)](/studynote/07_enterprise_systems/05_data_bi/300_realtime_data_streaming_kafka_cdc/)
**다음**: [302. 데이터옵스 CI/CD 파이프라인 자동 테스팅 (DataOps CI/CD dbt)](/studynote/07_enterprise_systems/05_data_bi/302_dataops_cicd_dbt/) ->

---
