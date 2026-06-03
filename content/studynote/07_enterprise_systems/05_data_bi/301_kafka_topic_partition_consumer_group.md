---
title: 301. 카프카 토픽 파티셔닝 기반 컨슈머 그룹 부하 분산 (Kafka Topic Partition Consumer Group)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kafka의 [[514_partition_slice_volume|파티션]]은 [[430_index_fast_full_scan|병렬]]성의 최소 단위이며, [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] 내 컨슈머 수와 [[514_partition_slice_volume|파티션]] 수의 비율이 [[139_throughput|처리량]]과 직결된다.
> 2. **가치**: 전체 [[139_throughput|처리량]](MB/s) = [[514_partition_slice_volume|파티션]] 수 × 컨슈머당 [[139_throughput|처리량]](MB/s) 공식으로 수평 확장 상한을 사전에 설계할 수 있다.
> 3. **판단 포인트**: [[514_partition_slice_volume|파티션]] 수는 한번 늘리면 줄일 수 없으므로, 최소 예상 피크 [[139_throughput|처리량]] ÷ 컨슈머 단위 [[139_throughput|처리량]] × 2배 여유로 [[459_quic_fec_forward_error_correction|초기]] 설계한다.

## Ⅰ. 개요 및 필요성

[[179_kafka_flink_watermark_time_window|Kafka]] ([[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]])는 LinkedIn이 설계한 [[136_variance|분산]] 스트리밍 플랫폼으로, 초당 수백만 건의 이벤트를 처리한다.
토픽(Topic)은 [[389_mesh_topology|메시]]지의 [[369_logic_bomb|논리]]적 채널이며, 이를 물리적으로 분할한 단위가 [[514_partition_slice_volume|파티션]]([[514_partition_slice_volume|Partition]])이다.
하나의 [[514_partition_slice_volume|파티션]]은 오직 하나의 컨슈머에게만 할당되므로([[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] 내), [[514_partition_slice_volume|파티션]] 수가 [[430_index_fast_full_scan|병렬]] 처리 상한을 결정한다.

[[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]]([[191_consumer_group_kafka_partition_load_balancing|Consumer Group]])은 같은 `group.id`를 공유하는 컨슈머들의 [[369_logic_bomb|논리]]적 집합이다.
그룹 내 컨슈머들은 [[514_partition_slice_volume|파티션]]을 나눠 소비하므로 [[139_throughput|처리량]] [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]이 가능하다.
반면 서로 다른 그룹은 동일 토픽 [[389_mesh_topology|메시]]지를 독립적으로 소비하므로, 하나의 토픽을 여러 하위 시스템이 동시에 구독하는 브로드캐스트 패턴을 구현할 수 있다.

[[139_throughput|처리량]] 설계 공식:
```
전체 처리량(MB/s) = 파티션 수 × 컨슈머당 처리량(MB/s)
예) 파티션 12개 × 컨슈머당 50 MB/s = 600 MB/s 피크 처리 가능
```

[[514_partition_slice_volume|파티션]] 수 설계 원칙:
- 너무 적으면: [[139_throughput|처리량]] 병목, 컨슈머 추가해도 효과 없음
- 너무 많으면: 브로커 메모리 압박, [[798_distributed_lock_zookeeper_consensus|ZooKeeper]]/KRaft [[012_metadata|메타데이터]] 과부하
- 권장: 브로커당 2,000~4,000 [[514_partition_slice_volume|파티션]] 이내 유지 ([[094_reinforcement_learning|Confluent]] 권장)

📢 **섹션 요약 비유**: [[514_partition_slice_volume|파티션]]은 고속도로 차선, 컨슈머는 차량이다. 차선 수보다 차가 많아봐야 차선 수만큼밖에 통행하지 못한다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[514_partition_slice_volume|파티션]] 할당 [[268_strategy_pattern|전략]] ([[514_partition_slice_volume|Partition]] Assignment [[268_strategy_pattern|Strategy]])

| [[268_strategy_pattern|전략]] | 동작 방식 | 특징 | 적합 상황 |
|:---|:---|:---|:---|
| RangeAssignor | [[514_partition_slice_volume|파티션]] 범위를 컨슈머에 균등 분할 | 구현 단순, 불균형 발생 가능 | 소수 [[514_partition_slice_volume|파티션]] |
| RoundRobinAssignor | [[178_round_robin_scheduling|라운드 로빈]] 방식으로 순환 배분 | 균형 우수 | 토픽 다수 구독 |
| StickyAssignor | 리밸런싱 시 기존 할당 최대 유지 | 리밸런싱 비용 최소화 | [[272_state_pattern|스테이트]]풀 컨슈머 |
| CooperativeStickyAssignor | 점진적 리밸런싱 (Incremental) | 중단 없는 리밸런싱 | 프로덕션 권장 |

### 오프셋 커밋 (Offset Commit) 방식

| 방식 | 설명 | 위험성 |
|:---|:---|:---|
| Auto commit | 5초 주기 자동 커밋 (기본) | 중복 또는 유실 가능 |
| Manual sync commit | commitSync() 직접 호출 | [[139_throughput|처리량]] 저하 |
| Manual async commit | commitAsync() + 콜백 | 재시도 순서 역전 주의 |

### [[103_ascii|ASCII]] 다이어그램: 토픽 4파티션 → [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] 2대

```
  Topic: user-events (파티션 4개)
  ┌──────────────────────────────────────────────────────────────┐
  │  Partition-0   │  Partition-1   │  Partition-2   │  Partition-3   │
  └───────┬────────┴───────┬────────┴───────┬────────┴───────┬────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │                Consumer Group: analytics-group                    │
  │   ┌─────────────────────────────┐   ┌──────────────────────────┐  │
  │   │         Consumer-A          │   │         Consumer-B       │  │
  │   │   (Partition-0, P-1 담당)   │   │   (Partition-2, P-3 담당)│  │
  │   └─────────────────────────────┘   └──────────────────────────┘  │
  └───────────────────────────────────────────────────────────────────┘
                │ 오프셋 커밋
  ┌─────────────────────┐
  │  Kafka Broker       │  __consumer_offsets 토픽
  │  P-0: 48200         │  P-1: 50100
  │  P-2: 47900         │  P-3: 51200
  └─────────────────────┘
```

### [[089_consumer_lag|Consumer Lag]] [[229_monitor|모니터]]링

```
Consumer Lag = Log End Offset - Consumer Commit Offset
Lag > 10,000건 → 알람 → 컨슈머 추가 or 처리 로직 최적화
```

📢 **섹션 요약 비유**: 오프셋은 책갈피다. 책갈피를 자주 꽂을수록 재시작 시 읽을 분량이 줄어들지만, 너무 자주 꽂으면 손이 바빠진다.

## Ⅲ. 비교 및 연결

### [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] vs 브로드캐스트 (다수 그룹)

| 항목 | [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] (1그룹 N컨슈머) | 브로드캐스트 (N그룹 각 1컨슈머) |
|:---|:---|:---|
| [[389_mesh_topology|메시]]지 처리 | 각 [[514_partition_slice_volume|파티션]]은 1컨슈머만 처리 | 모든 그룹이 동일 [[389_mesh_topology|메시]]지 수신 |
| 활용 패턴 | 부하 [[136_variance|분산]], 수평 확장 | 이벤트 팬아웃 (결제+알림+분석) |
| 오프셋 관리 | 그룹 단위 공유 | 그룹별 독립 관리 |

### Push vs Pull 모델

| 항목 | Push (RabbitMQ 방식) | Pull ([[179_kafka_flink_watermark_time_window|Kafka]] 방식) |
|:---|:---|:---|
| 처리 속도 제어 | 브로커가 전송 속도 결정 | 컨슈머가 자신의 속도로 인출 |
| 백프레셔 | 어렵다 | 자연스럽게 지원 |
| [[389_mesh_topology|메시]]지 재처리 | 복잡 (ACK 메커니즘) | 오프셋 리셋으로 간단히 재처리 |
| [[015_지연_데이터_관점|지연]] | 낮음 (즉시 전달) | [[448_polling_programmed_io|폴링]] 주기만큼 추가 [[015_지연_데이터_관점|지연]] |

📢 **섹션 요약 비유**: Push는 식당 서버가 음식을 가져다주는 것, Pull은 뷔페에서 내가 원할 때 가져오는 것이다. 뷔페(Pull)에서는 내 속도에 맞춰 먹을 수 있다.

## Ⅳ. 실무 적용 및 기술사 판단

### [[514_partition_slice_volume|파티션]] 수 설계 [[435_checklist_based_testing|체크리스트]]

- [ ] 예상 피크 [[389_mesh_topology|메시]]지 수(건/초) × 평균 [[389_mesh_topology|메시]]지 크기(KB) = 목표 [[139_throughput|처리량]](MB/s) 계산
- [ ] 컨슈머 단위 [[139_throughput|처리량]] 벤치마크 (일반적으로 50~100 MB/s/컨슈머)
- [ ] [[514_partition_slice_volume|파티션]] 수 = 목표 [[139_throughput|처리량]] ÷ 컨슈머 단위 [[139_throughput|처리량]] × 1.5배(여유)
- [ ] [[016_replication_factor|replication]].factor=3 (최소), min.insync.replicas=2 [[009_config|설정]] [[396_validation|확인]]
- [ ] CooperativeStickyAssignor 적용으로 무중단 리밸런싱 확보

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| enable.auto.commit=true + 무거운 처리 | 처리 전 커밋 → 유실 | 수동 커밋 + [[171_idempotency_iac_terraform|멱등성]] 처리 |
| 단일 [[514_partition_slice_volume|파티션]] 키 쏠림 | 핫 [[514_partition_slice_volume|파티션]](Hotspot) | 복합 키 or 랜덤 솔팅 |
| [[514_partition_slice_volume|파티션]] 수 = 컨슈머 수 고정 | 탄력적 확장 불가 | [[514_partition_slice_volume|파티션]] 여유분 확보 |
| 리밸런싱 무시 | [[090_service_kubernetes_network_load_balancing|서비스]] 중단 수초 | CooperativeStickyAssignor 적용 |

📢 **섹션 요약 비유**: [[514_partition_slice_volume|파티션]] 설계는 고속도로 건설과 같다. 준공 후 차선을 줄이기는 매우 어려우므로, 처음부터 충분한 여유 차선을 확보해야 한다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | Before (단일 큐) | After ([[179_kafka_flink_watermark_time_window|Kafka]] [[179_table_partitioning_concept|파티셔닝]]) |
|:---|:---|:---|
| [[139_throughput|처리량]] | 수천 건/초 | 수백만 건/초 (수평 확장) |
| 장애 내성 | [[454_spof|단일 장애점]] | 레플리카로 고가용성 |
| 재처리 | 불가 (삭제됨) | 오프셋 리셋으로 가능 |
| [[015_지연_데이터_관점|지연]] | 수ms (단순) | 수ms~수십ms ([[514_partition_slice_volume|파티션]] [[136_variance|분산]] + [[016_replication_factor|복제]]) |

### 한계 및 선결 과제

- [[514_partition_slice_volume|파티션]] 수는 증가만 가능, 감소 불가 → [[459_quic_fec_forward_error_correction|초기]] 설계가 중요
- Kafka는 at-least-once 기본 → [[171_idempotency_iac_terraform|멱등성]](Idempotent) 처리를 컨슈머가 보장
- [[083_cross_validation|exactly-once semantics]] (EOS) 사용 시 [[139_throughput|처리량]] [[489_raid_10_hybrid|10]]~30% 저하

📢 **섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] [[179_table_partitioning_concept|파티셔닝]]은 여러 계산대를 열어 계산대마다 전담 직원을 배치한 대형마트다. 계산대([[514_partition_slice_volume|파티션]])가 많을수록 손님([[389_mesh_topology|메시]]지)을 빠르게 처리하지만, 너무 많으면 직원 관리 비용도 늘어난다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Topic | 포함 | [[514_partition_slice_volume|파티션]]의 [[369_logic_bomb|논리]]적 묶음 |
| [[514_partition_slice_volume|Partition]] | [[430_index_fast_full_scan|병렬]] 단위 | 물리적 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] 단위 |
| [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] | 소비자 단위 | [[514_partition_slice_volume|파티션]]을 나눠 소비하는 그룹 |
| Offset | 위치 추적 | 컨슈머가 읽은 마지막 [[389_mesh_topology|메시]]지 위치 |
| Rebalancing | 재배분 이벤트 | 컨슈머 수 변경 시 [[514_partition_slice_volume|파티션]] 재할당 |
| [[089_consumer_lag|Consumer Lag]] | [[019_처리_지연|처리 지연]] 지표 | Log End Offset - 커밋 Offset |

### 📈 관련 키워드 및 발전 흐름도

```
단일 큐 메시지 브로커 - 처리량 병목
    │
    ▼
Kafka Topic - 논리적 데이터 채널 추상화
    │
    ▼
Partition - 물리적 분산·병렬 처리 단위
    │
    ▼
Consumer Group - 파티션별 독립 소비자 배정
    │
    ▼
Replication Factor + ISR = 고가용성 보장
```

> **키워드**: [[179_kafka_flink_watermark_time_window|Kafka]] Topic, [[514_partition_slice_volume|Partition]], [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]], Offset, [[016_replication_factor|Replication Factor]], [[020_isr|ISR]], Producer, Broker

### 👶 어린이를 위한 3줄 비유 설명

1. 토픽은 학교 알림판이고, [[514_partition_slice_volume|파티션]]은 알림판을 반별로 나눈 구역이에요.
2. [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]]은 각 구역 담당 학생 모둠이고, 한 구역은 한 학생만 담당해요.
3. 오프셋은 어디까지 읽었는지 표시하는 책갈피예요. 덕분에 다음 날에도 이어서 읽을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 301 / 482

← **이전**: [[300_realtime_data_streaming_kafka_cdc|300. 실시간 데이터 스트리밍 (Kafka + CDC)]]
**다음**: [[302_dataops_cicd_dbt|302. 데이터옵스 CI/CD 파이프라인 자동 테스팅 (DataOps CI/CD dbt)]] →

---
