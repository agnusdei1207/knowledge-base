+++
title = "189. 카프카 컨슈머 랙 (Kafka Consumer Lag) 지연 모니터링 경보 파이프"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 컨슈머 랙([Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/))은 **프로듀서(Producer)의 최신 오프셋(Log End Offset)과 컨슈머(Consumer)의 현재 오프셋([Current](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) Offset) 차이**로, 메시지 처리 지연의 핵심 지표이자 스트리밍 파이프라인 건전성의 척도다.
> 2. **가치**: Consumer Lag를 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) + [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) + AlertManager로 실시간 모니터링하고, 임계값 초과 시 자동으로 컨슈머 그룹을 스케일아웃하면 **[SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약) 위반을 선제적으로 방지**할 수 있다.
> 3. **판단 포인트**: Lag 증가 원인 분석—처리 로직 병목 vs [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 불균형 vs 외부 의존성 장애—을 구분하는 것이 핵심이며, 무조건 컨슈머 수 증가가 해결책이 아니라 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 상한선임을 기억해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 아키텍처 기본 개념

```
Kafka 아키텍처:
┌──────────────────────────────────────────────────────────┐
│                  Kafka 클러스터                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │         Topic: orders (Partition 0~3)               │  │
│  │  P0: [msg_1, msg_2, ..., msg_1000] ← LEO=1000      │  │
│  │  P1: [msg_1, msg_2, ..., msg_800]  ← LEO=800       │  │
│  │  P2: [msg_1, msg_2, ..., msg_900]  ← LEO=900       │  │
│  │  P3: [msg_1, msg_2, ..., msg_950]  ← LEO=950       │  │
│  └────────────────────────────────────────────────────┘  │
│           ↑ Producer 삽입            ↓ Consumer 읽기       │
└──────────────────────────────────────────────────────────┘

Consumer Group: order-processor
  Consumer 0: P0 처리 중 (Offset=990) → Lag = 1000-990 = 10
  Consumer 1: P1 처리 중 (Offset=750) → Lag = 800-750 = 50
  Consumer 2: P2 처리 중 (Offset=890) → Lag = 900-890 = 10
  Consumer 3: P3 처리 중 (Offset=900) → Lag = 950-900 = 50

Total Group Lag = 10 + 50 + 10 + 50 = 120
```

### 1.2 [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) 증가 원인 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

| 원인 | 증상 | 대응 |
|:---|:---|:---|
| 처리 속도 < 생산 속도 | Lag 지속 증가, 직선적 상승 | 컨슈머 스케일아웃 |
| 처리 로직 병목 | 특정 시간대 급상승 | UDF 최적화, 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 비동기화 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐 | 특정 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 Lag 높음 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 재분배, 키 해시 재설계 |
| 컨슈머 장애 | 갑작스러운 Lag 급등 | 리밸런싱, 장애 컨슈머 재시작 |
| GC 정지 | 주기적 Lag 상승 | JVM GC 튜닝 |
| 외부 DB 장애 | 특정 시간 Lag 폭증 | [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/), 비동기 처리 |

📢 **섹션 요약 비유**: Consumer Lag는 마치 음식점의 주문 대기열이다. 주방(Consumer)이 요리를 만드는 속도보다 손님 주문(Producer)이 빠르면 대기 번호판(Lag)이 계속 올라간다. 주방장을 더 투입하거나(스케일아웃) 요리법을 단순화(최적화)해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) 모니터링 도구 비교

```
┌──────────────────────────────────────────────────────────┐
│            Consumer Lag 모니터링 도구 생태계               │
│                                                           │
│  1. Kafka CLI (카프카 내장)                                │
│     kafka-consumer-groups.sh                             │
│     --describe --group order-processor                   │
│     → 순간 Lag 값 확인, 트렌드 추적 불가                  │
│                                                           │
│  2. JMX (Java Management Extensions) 메트릭               │
│     kafka.consumer:type=consumer-fetch-manager-metrics   │
│     records-lag-max → 컨슈머별 최대 Lag                   │
│     → Telegraf/JMX Exporter로 Prometheus 수집             │
│                                                           │
│  3. Burrow (LinkedIn 오픈소스)                            │
│     → 컨슈머 그룹 상태: OK / WARNING / ERROR             │
│     → Lag 증가 추세 기반 상태 판단 (단순 수치 아님)         │
│     → REST API + 알림 지원                                │
│                                                           │
│  4. Kafka Cruise Control                                  │
│     → 파티션 균형 자동 조정                                │
│     → 리소스 활용률 기반 Lag 원인 분석                     │
│                                                           │
│  5. Confluent Control Center (유료)                        │
│     → 완전한 Kafka 관리 UI + SLA 모니터링                  │
└──────────────────────────────────────────────────────────┘
```

### 2.2 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) + [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) + AlertManager 모니터링 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)

```
┌──────────────────────────────────────────────────────────┐
│          Consumer Lag 모니터링 파이프라인                   │
│                                                           │
│  Kafka 브로커                                             │
│  JMX 메트릭 노출 (포트 9999)                              │
│       ↓                                                  │
│  Kafka JMX Exporter (kafka-exporter)                     │
│  → kafka_consumergroup_lag{group, topic, partition}       │
│       ↓ Prometheus 수집 (15초 간격 스크레이핑)             │
│  Prometheus 저장소                                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │ 집계 쿼리:                                        │   │
│  │ sum(kafka_consumergroup_lag{group="order-proc"})  │   │
│  │   by (topic) > 1000  → 경보 트리거!               │   │
│  └──────────────────────────────────────────────────┘   │
│       ↓                                                  │
│  AlertManager → Slack / PagerDuty / Email                │
│       ↓ (선택적)                                         │
│  Auto Scaling Hook → Kubernetes HPA 또는 AWS ASG         │
│  → 컨슈머 파드 자동 스케일아웃                             │
└──────────────────────────────────────────────────────────┘
```

### 2.3 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 경보 규칙 설계

```yaml
# alertmanager_kafka_lag.yaml

groups:
- name: kafka_consumer_lag
  rules:

  # 경보 1: Consumer Lag 임계값 초과
  - alert: KafkaConsumerLagHigh
    expr: |
      sum(kafka_consumergroup_lag{
        consumergroup="order-processor"
      }) by (topic) > 10000
    for: 5m  # 5분 이상 지속 시 발동
    labels:
      severity: warning
    annotations:
      summary: "Kafka Consumer Lag 높음"
      description: |
        토픽 {{ $labels.topic }}의 컨슈머 그룹 Lag가
        {{ $value }}개 메시지 초과 (5분 이상 지속)

  # 경보 2: Lag 증가율 급등 (급격한 상승 패턴)
  - alert: KafkaConsumerLagRisingFast
    expr: |
      rate(kafka_consumergroup_lag{
        consumergroup="order-processor"
      }[5m]) > 100
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Kafka Consumer Lag 급증"

  # 경보 3: 컨슈머 그룹 오프셋 정지 (처리 중단 의심)
  - alert: KafkaConsumerGroupStopped
    expr: |
      changes(kafka_consumergroup_current_offset{
        consumergroup="order-processor"
      }[10m]) == 0
    for: 10m
    labels:
      severity: critical
```

📢 **섹션 요약 비유**: [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) + AlertManager는 마치 주방에 CCTV를 달고, 주문 대기열이 100개를 넘으면 주방장 핸드폰으로 자동 문자를 보내는 스마트 레스토랑 관리 시스템이다.

---

## Ⅲ. 비교 및 연결

### 3.1 Lag 증가 패턴별 원인 진단

```
Lag 패턴 분석:

패턴 1: 선형 증가 (지속적 상승)
  ↑ Lag
  │       /
  │      /
  │     /
  └──────── 시간
  원인: 처리 속도 < 생산 속도 (구조적 문제)
  대응: 컨슈머 스케일아웃 or 파티션 증가

패턴 2: 계단식 증가 (주기적 상승 후 정체)
  ↑ Lag
  │  ┌──┐  ┌──┐
  │──┘  └──┘  └──
  └──────────── 시간
  원인: 주기적 배치 부하 (예: 매 시 정각)
  대응: 부하 분산 일정 조정

패턴 3: 급등 후 정체 (장애)
  ↑ Lag
  │         ┌─────
  │         │
  │─────────┘
  └──────────── 시간
  원인: 특정 시점 컨슈머 장애 or 외부 의존성 장애
  대응: 장애 컨슈머 재시작, 서킷 브레이커

패턴 4: 특정 파티션만 높음
  P0 Lag: 5    (정상)
  P1 Lag: 5    (정상)
  P2 Lag: 50,000 (이상)
  원인: 데이터 스큐 or 특정 파티션 할당 불균형
  대응: 파티션 키 재설계, Cruise Control 균형 조정
```

### 3.2 컨슈머 수 확장의 한계

```
핵심 원칙: 컨슈머 수 ≤ 파티션 수

파티션 4개, 컨슈머 4개 (최적):
  C0 → P0
  C1 → P1
  C2 → P2
  C3 → P3
  → 모든 컨슈머가 활성화, 최대 병렬처리

파티션 4개, 컨슈머 6개 (낭비):
  C0 → P0
  C1 → P1
  C2 → P2
  C3 → P3
  C4 → 유휴 (파티션 없음)
  C5 → 유휴 (파티션 없음)
  → C4, C5는 낭비! 컨슈머만 추가해도 Lag 해소 안 됨

파티션 4개, 컨슈머 2개:
  C0 → P0 + P2
  C1 → P1 + P3
  → 처리 가능하나 최대 처리량이 반으로 제한
```

### 3.3 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) 연계 ([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) KEDA)

```yaml
# KEDA ScaledObject - Kafka Lag 기반 자동 스케일링

apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-consumer-scaledobject
spec:
  scaleTargetRef:
    name: order-processor-deployment
  minReplicaCount: 2    # 최소 컨슈머 수
  maxReplicaCount: 8    # 최대 컨슈머 수 (파티션 수 이하)
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      consumerGroup: order-processor
      topic: orders
      lagThreshold: "1000"  # 파티션당 Lag 1000 초과 시 스케일아웃
```

📢 **섹션 요약 비유**: 컨슈머 수 ≤ [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 원칙은 마치 계산대([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 4개인 마트에 계산원을 10명 고용해도 4명만 일할 수 있는 것과 같다. 계산대 수([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))를 먼저 늘려야 인력(컨슈머)을 효과적으로 활용할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 설계 가이드

```
SLA 기반 Lag 임계값 설계:

  서비스 유형별 Lag SLA:
  ┌──────────────────────────────────────────────────┐
  │ 서비스 유형 │ Lag 임계값 │ 알림 지연 │ 자동 대응  │
  ├──────────────────────────────────────────────────┤
  │ 실시간 결제  │ 100개      │ 1분       │ 즉시 HPA  │
  │ 주문 처리    │ 1,000개    │ 3분       │ 5분 내 HPA│
  │ 로그 분석    │ 100,000개  │ 15분      │ 수동 확인 │
  │ 배치 ETL    │ 제한 없음   │ 없음      │ 없음      │
  └──────────────────────────────────────────────────┘

  Lag 계산:
  처리 지연 시간 = Lag / 초당 소비 속도
  예: Lag=10,000, 초당 1,000 메시지 처리
  → 처리 지연 = 10초

  실시간 시스템 허용 지연 = 수 초
  배치 시스템 허용 지연 = 수 분~수 시간
```

### 4.2 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 계산

```
파티션 수 설계:
  목표 처리량 (메시지/초): 50,000 msg/s
  파티션당 처리량: 10,000 msg/s (컨슈머 처리 속도 기준)
  필요 파티션 수: 50,000 / 10,000 = 5개

  안전 여유: × 1.5 ~ 2배 = 8~10개 파티션 권장

  주의: 파티션 수 늘리기는 쉽지만 줄이기는 어려움
  → 처음부터 충분히 많게 설계 (나중에 추가 가능)
```

### 4.3 기술사 답안 핵심 포인트

```
Kafka Consumer Lag 모니터링 설계 시 필수 언급:
  ✓ Consumer Lag = LEO(Log End Offset) - Current Offset
  ✓ 모니터링 스택: kafka-exporter → Prometheus → Grafana
  ✓ Burrow: Lag 수치 + 증가 추세 함께 분석
  ✓ AlertManager: 단계별 경보 (Warning/Critical)
  ✓ Auto Scaling: KEDA + Kubernetes HPA 연계
  ✓ 컨슈머 수 ≤ 파티션 수 (근본 한계)
  ✓ Lag 패턴 분석: 선형 vs 급등 vs 파티션 스큐
  ✓ SLA 기반 임계값 설계 (서비스 유형별 차별화)
  ✓ 파티션 수 계산 방법 (목표 처리량 / 파티션당 처리량)
```

📢 **섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) SLA는 마치 택배 회사의 배송 약속이다. 당일 배송(실시간 결제)은 Lag 100개도 위험하고, 일반 택배(배치 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/))는 Lag 10만 개도 허용된다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 성격에 따라 다른 기준을 적용해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) 모니터링 도입 효과

| 효과 | 정량 지표 |
|:---|:---|
| 장애 선제 감지 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 전 평균 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~30분 전 경보 |
| [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 위반 감소 | 프로액티브 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)으로 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 준수율 99.9% |
| 운영 비용 절감 | Auto Scaling으로 야간 수동 모니터링 제거 |
| RCA 시간 단축 | Lag 패턴 + [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 연계로 5분 내 원인 분석 |

### 5.2 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 운영 성숙도 모델

```
┌──────────────────────────────────────────────────────┐
│              Kafka 운영 성숙도 단계                    │
│                                                      │
│  Level 1: 기본 모니터링                               │
│  → CLI로 Lag 수동 확인, 장애 후 대응                  │
│                                                      │
│  Level 2: 메트릭 수집                                 │
│  → Prometheus + Grafana, 수동 경보 설정               │
│                                                      │
│  Level 3: 자동 경보                                   │
│  → AlertManager, PagerDuty 연동, SLA 기반 임계값      │
│                                                      │
│  Level 4: 자동 복구                                   │
│  → KEDA Auto Scaling, 장애 파티션 자동 재할당          │
│                                                      │
│  Level 5: 예측적 운영                                 │
│  → ML 기반 Lag 예측, 사전 스케일아웃 (프로액티브)       │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 운영 성숙도는 마치 공장 관리의 발전 단계와 같다. 처음엔 기계가 고장나야 알지만(Level 1), 나중엔 고장 예정을 미리 알고 부품을 교체하는(Level 5) 예측 정비 수준으로 발전한다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 지표 | [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) | [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) - [Current](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) Offset 차이 |
| 모니터링 표준 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) + [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) | [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) |
| 경보 시스템 | AlertManager | 조건 기반 알림 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| 심화 분석 | Burrow | Lag 추세 기반 상태 판단 |
| 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | KEDA | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Lag 기반 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 자동 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| 근본 한계 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 | 컨슈머 수의 상한선 |
| 균형 조정 | Cruise Control | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 자동 재분배 |
| 원인 분석 | Lag 패턴 | 선형/급등/[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 스큐 패턴별 대응 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. **[Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/)**는 마치 카카오톡에서 메시지를 보낸 시각과 읽은 시각의 차이처럼, [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)에서 메시지가 쓰여진 위치와 읽힌 위치의 차이를 숫자로 나타낸 것이에요—이 숫자가 클수록 처리가 많이 밀려있는 거예요.

### 📈 관련 키워드 및 발전 흐름도

```text
Kafka Producer → Broker (Topic/Partition)
    │
    ▼
Consumer Group → 파티션별 Offset 추적
    │
    ▼
Consumer Lag = Latest Offset - Consumer Offset
    │
    ▼
모니터링 도구
    ├─► Burrow (LinkedIn 오픈소스)
    ├─► Kafka Lag Exporter → Prometheus → Grafana
    └─► Confluent Control Center
    │
    ▼
자동 대응: Consumer 스케일아웃 · 파티션 추가 · 경보
```
2. **[Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) 모니터링**은 마치 음식점에서 주문 대기열 번호판을 관리자 핸드폰으로 실시간 전송하는 것처럼, [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)의 처리 지연을 자동으로 감지해서 경보를 보내는 시스템이에요.
3. **컨슈머 수 ≤ [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수** 원칙은 마치 계산대가 4개인 마트에 직원이 10명이어도 4명만 계산대에 설 수 있는 것처럼, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수보다 컨슈머를 더 많이 늘려도 추가 컨슈머는 아무 일도 못 하는 낭비가 된다는 뜻이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 189 / 258

← **이전**: [188. OOM (Out of Memory) 메모리 보호 GC (Garbage Collection) 스파크 스왑 방어](/knowledge-base/studynote/14_data_engineering/04_mlops/188_oom_memory_protection_gc_spark_spill/)
**다음**: [190. 스플릿 브레인 (Split Brain) 방어 주키퍼 (ZooKeeper) 펜싱 합의 코디 연계망](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) →

---
