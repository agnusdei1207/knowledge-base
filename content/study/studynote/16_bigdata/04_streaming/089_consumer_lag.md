+++
weight = 89
title = "14. Consumer Lag — Kafka 소비 지연 모니터링"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: Consumer Lag (소비자 [[015_지연_데이터_관점|지연]])은 [[179_kafka_flink_watermark_time_window|Kafka]] 토픽의 최신 오프셋(Latest Offset)과 Consumer 그룹이 커밋한 오프셋(Committed Offset)의 차이로, "Consumer가 Producer보다 얼마나 뒤처져 있는가"를 나타내는 스트리밍 [[123_pipe|파이프]]라인의 핵심 건강 지표다.
- **가치**: Consumer Lag 급증은 [[123_pipe|파이프]]라인 병목(처리 속도 < 수신 속도)의 조기 경보이며, Lag=0이 목표이나 일시적 급증은 정상이므로 **트렌드와 임계값**을 기반으로 오토스케일링과 알림 [[507_acid_properties|트리거]]를 [[009_config|설정]]해야 한다.
- **판단 포인트**: Consumer Lag이 계속 증가하면 Consumer를 수평 확장하거나([[514_partition_slice_volume|파티션]] 수만큼), 소비 처리 로직을 최적화하거나, [[389_mesh_topology|메시]]지 생산 속도를 낮추는 세 가지 대응 중 병목 위치에 따라 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. Consumer Lag의 정의

```
Kafka Topic "orders":
  파티션 0: 최신 오프셋 = 10,000 (Producer가 여기까지 씀)
  파티션 0: Consumer 커밋 오프셋 = 9,500 (Consumer가 여기까지 읽음)
  → Lag = 10,000 - 9,500 = 500 (메시지 500개 미처리)

파티션 1: 최신 = 8,000, 커밋 = 8,000 → Lag = 0
파티션 2: 최신 = 12,000, 커밋 = 11,000 → Lag = 1,000

총 Consumer Lag = 500 + 0 + 1,000 = 1,500
```

### 2. Consumer Lag이 중요한 이유

- **실시간 처리 [[085_sla|SLA]]**: Lag이 크면 [[001_dikw_pyramid|데이터]] 신선도([[001_dikw_pyramid|Data]] Freshness)가 낮아짐
- **장애 예측**: Lag 급증 → 처리 병목 → 잠재적 [[157_oom_killer|OOM]]/장애 전조
- **[[249_scaling_normalization_standardization|스케일링]] [[130_signal|신호]]**: 지속적인 Lag 증가 = Consumer 추가 또는 [[123_pipe|파이프]]라인 최적화 필요

**📢 섹션 요약 비유**
> Consumer Lag는 "편의점 계산대 앞 대기 줄 길이"다. 줄이 0이면 실시간 처리, 줄이 100명이면 주문이 100개 밀려 있다는 의미다. 줄이 계속 길어지면 계산원(Consumer)을 더 배치해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Lag 계산 및 [[229_monitor|모니터]]링 방법

```bash
# Kafka CLI로 Consumer Lag 조회
kafka-consumer-groups.sh \
    --bootstrap-server kafka:9092 \
    --group my-consumer-group \
    --describe

# 출력 예시:
# TOPIC          PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# orders         0          9500            10000           500
# orders         1          8000            8000            0
# orders         2          11000           12000           1000
```

### 2. 주요 [[229_monitor|모니터]]링 도구

| 도구 | 특징 | 권장 사용 환경 |
|:---|:---|:---|
| [[179_kafka_flink_watermark_time_window|Kafka]] CLI (`kafka-consumer-groups.sh`) | 기본 제공, 실시간 조회 | 개발/디버깅 |
| Burrow (LinkedIn [[191_oss_license_compliance|오픈소스]]) | 트렌드 분석, 알림, 슬라이딩 윈도우 판단 | 프로덕션 [[229_monitor|모니터]]링 |
| JMX [[567_metrics_time_series_prometheus_grafana|Metrics]] | `kafka.consumer.fetch-manager-metrics` | [[136_prometheus|Prometheus]]/[[168_grafana|Grafana]] 통합 |
| [[179_kafka_flink_watermark_time_window|Kafka]] UI / [[094_reinforcement_learning|Confluent]] Control Center | [[003_bigdata_7v|시각화]] 대시보드 | 운영 가시성 |
| AWS MSK Console (MSK 사용 시) | 관리형 클러스터 내장 | AWS 환경 |

### 3. Burrow의 Lag 판단 로직

Burrow (LinkedIn, [[191_oss_license_compliance|오픈소스]])는 단순 Lag 숫자가 아닌 **Consumer의 처리 [[216_progress_in_synchronization|진행]] 여부**로 판단한다.

```
판단 기준:
  OK:       Consumer가 계속 진행 중 (Lag이 있어도 줄어들고 있으면 OK)
  WARNING:  Consumer가 느려지고 있음 (Lag이 천천히 증가)
  ERROR:    Consumer가 멈춤 (커밋 오프셋이 변하지 않음)
  STALLED:  Consumer가 커밋을 못함 (처리 중이지만 커밋 미완료)
  STOPPED:  Consumer 그룹 전체 정지
```

**📢 섹션 요약 비유**
> Burrow는 "대기 줄 분석가"다. 단순히 "줄이 500명이다"가 아니라 "줄이 줄어드는 중인가, 늘어나는 중인가, 멈췄는가"를 판단한다. 줄이 500명이어도 줄어드는 중이면 문제없고, 줄이 10명이어도 계속 늘어나면 위험 [[130_signal|신호]]다.

---

## Ⅲ. 비교 및 연결

### 1. Consumer Lag 급증 원인별 해결책

| 원인 | 증상 | 해결책 |
|:---|:---|:---|
| Consumer 처리 속도 부족 | Lag 지속 증가, Consumer CPU 높음 | Consumer 수 증가 ([[514_partition_slice_volume|파티션]] 수 이내) |
| Consumer 로직 병목 | 특정 처리 단계에서 느림 | 처리 로직 최적화, I/O 비동기화 |
| 프로듀서 [[344_bus|버스]]트 트래픽 | 일시적 Lag 급등 후 [[233_recovery_database_restoration_overview|회복]] | 버퍼 크기 조정, 처리 용량 예비 확보 |
| Consumer 장애 | Lag 무한 증가, Consumer 0개 | 장애 [[658_ir_recovery|복구]], 자동 재시작 [[009_config|설정]] |
| [[514_partition_slice_volume|파티션]] 수 < Consumer 수 | 일부 Consumer 유휴 | [[514_partition_slice_volume|파티션]] 수 증가 |

### 2. [[179_kafka_flink_watermark_time_window|Kafka]] Lag 기반 오토스케일링

```yaml
# KEDA (Kubernetes Event-Driven Autoscaling) 예시
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
spec:
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      consumerGroup: my-consumer-group
      topic: orders
      lagThreshold: "100"   # Lag 100 초과 시 스케일아웃
      offsetResetPolicy: latest
```

**📢 섹션 요약 비유**
> [[179_kafka_flink_watermark_time_window|Kafka]] Lag 기반 오토스케일링은 "주문 대기열에 따라 배달원을 자동으로 더 투입하는 시스템"이다. 주문이 100개 밀리면(Lag > 100) 배달원(Consumer [[198_pod_kubernetes_minimum_deployment_unit|Pod]])을 자동으로 추가하고, 다 처리되면 줄인다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. Consumer Lag [[229_monitor|모니터]]링 아키텍처

```
Kafka Cluster
    ↓ JMX Metrics 수집
JMX Exporter (Prometheus)
    ↓
Prometheus → Grafana 대시보드
    ↓ Lag > 임계값
AlertManager → PagerDuty / Slack 알림
    ↓ Lag 지속 증가
KEDA / Custom HPA → Consumer Pod 스케일아웃
```

### 2. 알림 임계값 [[009_config|설정]] 가이드

| Lag 수준 | 의미 | 권장 대응 |
|:---|:---|:---|
| Lag < 허용_지연 × EPS | 정상 | [[229_monitor|모니터]]링 유지 |
| Lag 증가 추세 지속 5분+ | 경고 | 원인 분석 시작 |
| Lag > 최대_허용_지연 × EPS | 알림 | 즉시 대응 |
| Consumer [[216_progress_in_synchronization|진행]] 멈춤 | 긴급 | PagerDuty 알림 |

(EPS = Events Per Second = 초당 이벤트 수)

### 3. [[435_checklist_based_testing|체크리스트]]

- [ ] [[136_prometheus|Prometheus]] + JMX Exporter로 Consumer Lag 지표 수집
- [ ] [[168_grafana|Grafana]] 대시보드에 [[514_partition_slice_volume|파티션]]별 Lag [[003_bigdata_7v|시각화]]
- [ ] Lag 증가 추세에 대한 알림 규칙 [[009_config|설정]] (단순 임계값이 아닌 트렌드)
- [ ] Burrow 또는 유사 도구로 Consumer 상태 [[104_classification_analysis|분류]] [[229_monitor|모니터]]링
- [ ] KEDA/[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 기반 오토스케일링 [[009_config|설정]]

**📢 섹션 요약 비유**
> Consumer Lag [[229_monitor|모니터]]링은 "혈압 측정"과 같다. 단일 측정값보다 시간 추이가 중요하다. 혈압이 높아도 안정적이면 문제없지만, 계속 오르는 추세면 의사에게 가야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 장애 조기 예방 | Lag 증가 추세로 병목 사전 감지 |
| [[085_sla|SLA]] 보장 | [[001_dikw_pyramid|데이터]] 신선도([[001_dikw_pyramid|Data]] Freshness) [[229_monitor|모니터]]링 |
| 비용 최적화 | Lag 기반 오토스케일링으로 불필요한 과잉 Consumer 방지 |

### 2. 결론

Consumer Lag는 [[179_kafka_flink_watermark_time_window|Kafka]] 기반 스트리밍 [[123_pipe|파이프]]라인의 **가장 중요한 단일 건강 지표**다. 기술사 답안에서는 Lag의 수식 정의(Latest - Committed Offset), [[229_monitor|모니터]]링 도구(Burrow, JMX), 원인별 해결 [[268_strategy_pattern|전략]], 오토스케일링과의 연계를 체계적으로 서술하면 된다.

**📢 섹션 요약 비유**
> Consumer Lag는 공장 생산라인의 "미완성 재공품(WIP) 수량"이다. WIP가 0이면 완벽한 흐름, WIP가 늘어나면 어딘가 병목이 있다는 [[130_signal|신호]]다. 공장 관리자([[229_monitor|모니터]]링 시스템)는 WIP 추이를 실시간으로 보고 라인을 조정한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[179_kafka_flink_watermark_time_window|Kafka]] [[179_table_partitioning_concept|파티셔닝]] | 전제 구조 | [[514_partition_slice_volume|파티션]]별 Lag을 개별 추적 |
| [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] | 측정 단위 | Lag는 [[191_consumer_group_kafka_partition_load_balancing|Consumer Group]] 기준 측정 |
| Burrow | [[229_monitor|모니터]]링 도구 | LinkedIn의 Lag 상태 [[104_classification_analysis|분류]] 도구 |
| KEDA | 오토스케일링 | Lag 기반 K8s Consumer 자동 확장 |
| [[179_kafka_flink_watermark_time_window|Kafka]] MirrorMaker 2 | 연관 운영 | [[016_replication_factor|복제]] 클러스터 간 Lag 차이 [[229_monitor|모니터]]링 |


### 📈 관련 키워드 및 발전 흐름도

```text
[Kafka 프로듀서 (Producer) — 토픽 파티션에 메시지 비동기 발행]
    │
    ▼
[오프셋 (Offset) — 파티션 내 메시지 위치, LEO vs 커밋 오프셋 구분]
    │
    ▼
[Consumer Lag — LEO - Current Offset, 소비 지연 누적량 정량 측정]
    │
    ▼
[컨슈머 그룹 모니터링 — Burrow·kafka-consumer-groups로 실시간 Lag 추적]
    │
    ▼
[자동 스케일링 (KEDA) — Lag 임계값 기반 컨슈머 인스턴스 수평 확장·축소]
```

이 흐름은 [[179_kafka_flink_watermark_time_window|Kafka]] [[389_mesh_topology|메시]]지 발행에서 오프셋 개념으로 Consumer Lag이 정의되고, [[229_monitor|모니터]]링 도구로 가시화된 뒤 KEDA 기반 자동 [[249_scaling_normalization_standardization|스케일링]]으로 Lag을 능동적으로 제어하는 스트리밍 [[123_pipe|파이프]]라인 운영의 핵심 계보를 보여준다.


### 👶 어린이를 위한 3줄 비유 설명

카카오톡 [[389_mesh_topology|메시]]지를 받았지만 아직 읽지 않은 것처럼, Consumer Lag는 "Kafka에 [[389_mesh_topology|메시]]지가 왔는데 아직 처리 못한 개수"예요. 읽지 않은 [[389_mesh_topology|메시]]지가 0개면 실시간 처리, 1000개면 1000개 뒤처진 것이에요. [[389_mesh_topology|메시]]지가 계속 쌓이면(Lag 증가) 더 많은 처리자(Consumer)를 투입하거나 읽는 속도를 높여야 해요!
