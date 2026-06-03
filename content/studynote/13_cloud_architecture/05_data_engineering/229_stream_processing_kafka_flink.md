---
title: 229. 스트림 처리 (Stream Processing)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스트림 처리([[467_http2_stream_multiplexing_tcp_hol|Stream]] Processing)는 [[001_dikw_pyramid|데이터]]가 발생하는 즉시 밀리초~초 단위로 실시간 처리하는 방식으로, **[[141_latency|지연 시간]]([[141_latency|Latency]])을 최소화**하여 실시간 의사결정을 가능하게 한다.
> 2. **가치**: [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[267_gnn_fraud_detection_knowledge_graph|FDS]]), 실시간 추천, [[101_iot_concept|IoT]] 모니터링처럼 **[[001_dikw_pyramid|데이터]]의 가치가 시간이 지남에 따라 급격히 감소**하는 워크로드에서 [[228_batch_processing_hadoop_spark|배치 처리]] 대비 압도적 우위를 갖는다.
> 3. **판단 포인트**: 윈도우 처리(Tumbling·Sliding·[[160_session_controlling_terminal|Session]]), 이벤트 시간 vs 처리 시간, [[085_watermark|워터마크]]([[085_watermark|Watermark]])를 통한 늦게 도착하는 [[001_dikw_pyramid|데이터]] 처리가 스트림 처리의 핵심 복잡성이다.

---

## Ⅰ. 개요 및 필요성

은행 사기 탐지 시스템이 10분 후에 이상 거래를 탐지한다면 이미 피해가 발생했다. 실시간 주식 가격 알림이 1시간 [[015_지연_데이터_관점|지연]]된다면 투자 판단이 무의미하다. 이처럼 **[[001_dikw_pyramid|데이터]]의 가치가 시간에 반비례**하는 워크로드에서 [[228_batch_processing_hadoop_spark|배치 처리]]는 한계가 있다.

```
[데이터 가치 vs 시간 그래프]
가치
│▓▓▓▓▓
│    ▓▓▓▓
│        ▓▓▓▓
│            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
└─────────────────────────────── 시간
이벤트 발생시  초    분    시간
↑ 스트리밍 처리 구간  ↑ 배치 처리 수용 구간

실시간성 필요 사례:
- 신용카드 이상 거래 탐지 (FDS)
- IoT 센서 이상 알림
- 실시간 광고 입찰 (RTB)
- 게임 이벤트 처리
- 실시간 대시보드
```

📢 **섹션 요약 비유**: 스트림 처리는 119 구급대가 신고 즉시 출동하는 것이다. 하루치 신고를 모아서 아침에 한꺼번에 출동(배치)하면 이미 늦다. 신고가 오는 즉시 실시간으로 대응해야 생명을 구할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스트림 처리 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                  스트림 처리 파이프라인                        │
│                                                             │
│  이벤트 소스          메시지 브로커          스트림 프로세서    │
│  ┌──────────┐        ┌──────────┐          ┌────────────┐  │
│  │ 웹 클릭   │ ─────▶ │  Kafka   │ ───────▶ │   Flink    │  │
│  │ IoT 센서  │        │  Topic   │          │  (실시간    │  │
│  │ 결제 이벤트│        │ 파티션   │          │   변환·집계) │  │
│  └──────────┘        └──────────┘          └─────┬──────┘  │
│                                                   │         │
│              ┌────────────────────────────────────┘         │
│              ▼                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │ 출력 싱크 (Output Sink)                           │      │
│  │  - Redis (실시간 집계 결과 캐시)                   │      │
│  │  - Elasticsearch (검색·대시보드)                  │      │
│  │  - S3/Delta Lake (스트리밍 적재)                  │      │
│  │  - 알림 시스템 (이상 탐지 경보)                    │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 윈도우 처리 유형

```
[Tumbling Window - 겹치지 않는 고정 윈도우]
│ W1  │ W2  │ W3  │ W4  │
──────────────────────────▶ 시간
0초  10초  20초  30초  40초

[Sliding Window - 슬라이딩 윈도우]
│  W1   │
   │  W2   │
      │  W3   │
──────────────────────────▶ 시간
매 5초마다 10초 윈도우 집계

[Session Window - 활동 기반 세션 윈도우]
│─── 세션 1 ───│  │── 세션 2 ──│
활동  ...  활동  gap  활동  활동
```

### 이벤트 시간 vs 처리 시간

| 구분 | 이벤트 시간 (Event Time) | 처리 시간 (Processing Time) |
|:---|:---|:---|
| **정의** | 이벤트가 실제 발생한 시간 | 시스템이 처리하는 시간 |
| **예시** | 사용자가 클릭한 시각 | Kafka에 도달한 시각 |
| **[[015_지연_데이터_관점|지연]] 원인** | 네트워크·배터리 [[015_지연_데이터_관점|지연]] | 없음 |
| **정확도** | 높음 (실제 시간 반영) | 낮음 ([[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] 미반영) |
| **복잡도** | 높음 ([[085_watermark|워터마크]] 필요) | 낮음 |

### [[085_watermark|워터마크]]([[085_watermark|Watermark]])

```
[워터마크 개념]
이벤트 시간: 09:00 09:01 09:02 ... (지연 이벤트: 09:00 이벤트가 09:05에 도달)

워터마크 = 현재 최대 이벤트 시간 - 허용 지연 시간
예: 최대 이벤트 시간 09:05, 허용 지연 2분 → 워터마크 = 09:03

09:03 이전 이벤트는 "완전하다" 판단 → 윈도우 닫기 가능
09:03 이후 도착한 09:00 이벤트는 "늦음" → 무시 또는 별도 처리
```

📢 **섹션 요약 비유**: [[085_watermark|워터마크]]는 우체국의 "마감 시간"이다. "오후 5시 이전 소인이 찍힌 편지는 오늘 처리한다"는 규칙처럼, [[085_watermark|워터마크]] 이전 시간의 이벤트만 현재 윈도우에서 처리하고, 너무 늦게 도착한 편지([[015_지연_데이터_관점|지연]] 이벤트)는 별도로 처리한다.

---

## Ⅲ. 비교 및 연결

### 스트림 처리 프레임워크 비교

| 비교 항목 | [[215_flink_native_stream_watermark_window_time|Apache Flink]] | [[061_structured_streaming|Spark Structured Streaming]] | [[179_kafka_flink_watermark_time_window|Kafka]] Streams |
|:---|:---|:---|:---|
| **처리 모델** | 네이티브 스트리밍 | 마이크로배치 | 네이티브 스트리밍 |
| **[[141_latency|지연 시간]]** | 밀리초 | 수백ms~수초 | 밀리초 |
| **상태 관리** | 강력 (RocksDB) | 보통 | 가능 |
| **이벤트 시간** | 완전 지원 | 지원 | 지원 |
| **복잡 이벤트 처리** | 우수 | 보통 | 제한적 |
| **배치 통합** | Flink Batch | Spark Batch | ❌ |
| **운영 복잡성** | 높음 | 중간 | 낮음 ([[179_kafka_flink_watermark_time_window|Kafka]] 내장) |
| **적합 사례** | 복잡한 이벤트 처리, 금융 | 기존 Spark 팀, 배치+스트리밍 | [[179_kafka_flink_watermark_time_window|Kafka]] 기반 간단 변환 |

### Exactly-Once vs At-Least-Once

| 보장 수준 | 설명 | 비용 | 사용 사례 |
|:---|:---|:---|:---|
| **At-Most-Once** | 손실 가능, 중복 없음 | 낮음 | [[626_log_collection|로그 수집]] (손실 허용) |
| **At-Least-Once** | 중복 가능, 손실 없음 | 중간 | 이벤트 집계 ([[171_idempotency_iac_terraform|멱등성]] 보장 시) |
| **Exactly-Once** | [[083_cross_validation|정확히 한 번]] 처리 | 높음 | 금융 거래, 정산 |

📢 **섹션 요약 비유**: Exactly-Once는 계좌 이체와 같다. "한 번만" 처리되어야 하며, 두 번 이체(중복)되거나 미이체(손실)되면 안 된다. 반면 웹 [[626_log_collection|로그 수집]]은 한두 개 누락되어도 통계에 큰 영향이 없으므로 At-Least-Once로 충분하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Flink 스트림 처리 예시

```java
// Apache Flink: 실시간 이상 거래 탐지
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Kafka 소스
FlinkKafkaConsumer<Transaction> source = new FlinkKafkaConsumer<>(
    "transactions", new TransactionSchema(), properties);
source.assignTimestampsAndWatermarks(
    WatermarkStrategy.<Transaction>forBoundedOutOfOrderness(Duration.ofSeconds(5))
        .withTimestampAssigner((t, ts) -> t.getEventTime())
);

// 5분 윈도우 내 동일 카드 10만원 초과 거래 탐지
DataStream<Alert> alerts = env
    .addSource(source)
    .keyBy(Transaction::getCardId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .process(new FraudDetectionProcess());  // 합산 금액 > 100,000원
    
alerts.addSink(new FlinkKafkaProducer<>("fraud-alerts", ...));
env.execute("Fraud Detection Pipeline");
```

### 실무 스트리밍 선택 기준

| 요건 | 권장 기술 |
|:---|:---|
| 밀리초 단위 [[015_지연_데이터_관점|지연]] 필요 | [[215_flink_native_stream_watermark_window_time|Apache Flink]] |
| 기존 Spark 팀 있음 | [[061_structured_streaming|Spark Structured Streaming]] |
| [[179_kafka_flink_watermark_time_window|Kafka]] 중심 단순 변환 | [[179_kafka_flink_watermark_time_window|Kafka]] Streams |
| AWS 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] | [[091_amazon_kinesis|Amazon Kinesis]] [[001_dikw_pyramid|Data]] Analytics (Flink) |
| GCP | Google Dataflow (Apache Beam) |

📢 **섹션 요약 비유**: 스트림 처리 프레임워크 선택은 소방차 선택과 같다. 대형 화재(복잡한 이벤트)에는 Flink 사다리차가, 일반 화재에는 [[060_spark_streaming_dstream|Spark Streaming]] 펌프차가, 좁은 골목은 [[179_kafka_flink_watermark_time_window|Kafka]] Streams 소형 차가 적합하다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **실시간 의사결정** | [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]], 긴급 알림을 초 단위로 실행 |
| **[[001_dikw_pyramid|데이터]] 신선도** | 항상 최신 상태의 집계/분석 결과 |
| **경쟁 우위** | 실시간 개인화 추천으로 고객 경험 극대화 |
| **운영 효율** | [[101_iot_concept|IoT]] 센서 이상 즉시 감지로 장비 사고 예방 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **아키텍처 복잡성** | 상태 관리, 윈도우 설계, [[085_watermark|워터마크]] 튜닝 필요 |
| **운영 비용** | 클러스터 상시 가동으로 배치 대비 높은 비용 |
| **[[002_bigdata_5v|정확성]] vs [[015_지연_데이터_관점|지연]]** | [[085_watermark|워터마크]] 길게 설정할수록 [[015_지연_데이터_관점|지연]]↑·[[002_bigdata_5v|정확성]]↑ |
| **재처리 어려움** | 실패 시 이벤트 재처리 복잡 ([[179_kafka_flink_watermark_time_window|Kafka]] 오프셋 관리) |

📢 **섹션 요약 비유**: 스트림 처리는 24시간 편의점 운영과 같다. 항상 열려있어(상시 클러스터) 언제든 [[090_service_kubernetes_network_load_balancing|서비스]] 가능하지만, 야간 인건비(고비용)와 야간 운영의 복잡성(아키텍처 복잡도)이 있다. 대부분의 업무는 낮에만 영업하는 [[228_batch_processing_hadoop_spark|배치 처리]]로 충분하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] | 스트림 처리의 [[145_message_broker_sync_async|메시지 브로커]], 이벤트 소스 |
| [[215_flink_native_stream_watermark_window_time|Apache Flink]] | 스트림 처리의 표준 프레임워크 |
| [[228_batch_processing_hadoop_spark|배치 처리]] | 스트리밍의 대조 개념, [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 아키텍처에서 결합 |
| 윈도우 처리 | 스트림 [[001_dikw_pyramid|데이터]]를 구간 단위로 집계하는 핵심 기법 |
| [[085_watermark|워터마크]] | [[015_지연_데이터_관점|지연]] 이벤트 처리를 위한 시간 허용 한계 정의 |
| Exactly-Once | 금융 스트리밍에서 요구되는 처리 보장 수준 |
| [[216_lambda_kappa_architecture_batch_realtime|Lambda]]/[[235_kappa|Kappa]] | 배치와 스트리밍을 결합·단일화하는 아키텍처 패턴 |

### 👶 어린이를 위한 3줄 비유 설명
1. 스트림 처리는 물이 흐르는 강에서 물고기를 바로바로 잡는 것이다. 강([[179_kafka_flink_watermark_time_window|Kafka]])에 물고기([[001_dikw_pyramid|데이터]])가 흘러오면, 낚시꾼(Flink)이 즉시 잡아 요리한다.

### 📈 관련 키워드 및 발전 흐름도

```text
Batch (지연 처리) → Micro-batch (Spark Streaming)
    │
    ▼
True Stream: Apache Flink · Kafka Streams
    ├─► Exactly-Once 보장 · Event-Time 처리
    └─► Watermark: 늦은 이벤트 처리
    │
    ▼
Unified: Batch + Stream 통합 (Flink · Beam)
```
2. 윈도우는 강의 그물을 일정 구간에 치는 것이다. 10분마다 그물을 걷어서 그 사이 잡힌 물고기를 세면, 10분 단위 어획량(집계)을 알 수 있다.
3. [[085_watermark|워터마크]]는 "이 물고기는 너무 오래전에 잡힌 것이라 포함하지 않겠다"는 규칙이다. 너무 늦게 도착한 [[001_dikw_pyramid|데이터]]는 결과에 포함하지 않아야 처리가 멈추지 않는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 228 / 371

← **이전**: [[228_batch_processing_hadoop_spark|228. 배치 처리 (Batch Processing)]]
**다음**: [[230_apache_kafka_distributed_messaging|230. 아파치 카프카 (Apache Kafka)]] →

---
