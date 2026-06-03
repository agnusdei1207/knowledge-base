+++
title = "229. 스트림 처리 (Stream Processing)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스트림 처리([Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) Processing)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 발생하는 즉시 밀리초~초 단위로 실시간 처리하는 방식으로, <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a>(<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>)을 최소화</strong>하여 실시간 의사결정을 가능하게 한다.
> 2. **가치**: [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)([FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/)), 실시간 추천, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 모니터링처럼 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 가치가 시간이 지남에 따라 급격히 감소</strong>하는 워크로드에서 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 대비 압도적 우위를 갖는다.
> 3. **판단 포인트**: 윈도우 처리(Tumbling·Sliding·[Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)), 이벤트 시간 vs 처리 시간, [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/))를 통한 늦게 도착하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리가 스트림 처리의 핵심 복잡성이다.

---

## Ⅰ. 개요 및 필요성

은행 사기 탐지 시스템이 10분 후에 이상 거래를 탐지한다면 이미 피해가 발생했다. 실시간 주식 가격 알림이 1시간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된다면 투자 판단이 무의미하다. 이처럼 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 가치가 시간에 반비례</strong>하는 워크로드에서 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)는 한계가 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 가치 vs 시간 그래프</div></div>
<div class="kb-diagram-note">가치</div>
<div class="kb-diagram-note">▓▓▓▓▓</div>
<div class="kb-diagram-note">▓▓▓▓</div>
<div class="kb-diagram-note">▓▓▓▓</div>
<div class="kb-diagram-note">▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓</div>
<div class="kb-diagram-tree-item" style="--depth:0">시간</div>
<div class="kb-diagram-note">이벤트 발생시 초 분 시간</div>
<div class="kb-diagram-note">↑ 스트리밍 처리 구간 ↑ 배치 처리 수용 구간</div>
<div class="kb-diagram-note">실시간성 필요 사례:</div>
<div class="kb-diagram-tree-item" style="--depth:0">신용카드 이상 거래 탐지 (FDS)</div>
<div class="kb-diagram-tree-item" style="--depth:0">IoT 센서 이상 알림</div>
<div class="kb-diagram-tree-item" style="--depth:0">실시간 광고 입찰 (RTB)</div>
<div class="kb-diagram-tree-item" style="--depth:0">게임 이벤트 처리</div>
<div class="kb-diagram-tree-item" style="--depth:0">실시간 대시보드</div>
</div>
</div>



📢 **섹션 요약 비유**: 스트림 처리는 119 구급대가 신고 즉시 출동하는 것이다. 하루치 신고를 모아서 아침에 한꺼번에 출동(배치)하면 이미 늦다. 신고가 오는 즉시 실시간으로 대응해야 생명을 구할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스트림 처리 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스트림 처리 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이벤트 소스 메시지 브로커 스트림 프로세서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">웹 클릭</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Kafka</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Flink</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IoT 센서</div><div class="kb-diagram-cell">Topic</div><div class="kb-diagram-cell">(실시간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결제 이벤트</div><div class="kb-diagram-cell">파티션</div><div class="kb-diagram-cell">변환·집계)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출력 싱크 (Output Sink)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Redis (실시간 집계 결과 캐시)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Elasticsearch (검색·대시보드)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- S3/Delta Lake (스트리밍 적재)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 알림 시스템 (이상 탐지 경보)</div></div>
</div>
</div>



### 윈도우 처리 유형



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Tumbling Window - 겹치지 않는 고정 윈도우</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">W1</div><div class="kb-diagram-cell">W2</div><div class="kb-diagram-cell">W3</div><div class="kb-diagram-cell">W4</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">▶ 시간</div>
<div class="kb-diagram-note">0초 10초 20초 30초 40초</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Sliding Window - 슬라이딩 윈도우</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">W1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">W2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">W3</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">▶ 시간</div>
<div class="kb-diagram-note">매 5초마다 10초 윈도우 집계</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Session Window - 활동 기반 세션 윈도우</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">세션 1</div><div class="kb-diagram-cell">── 세션 2 ──</div></div>
<div class="kb-diagram-note">활동 ... 활동 gap 활동 활동</div>
</div>
</div>



### 이벤트 시간 vs 처리 시간

| 구분 | 이벤트 시간 (Event Time) | 처리 시간 (Processing Time) |
|:---|:---|:---|
| **정의** | 이벤트가 실제 발생한 시간 | 시스템이 처리하는 시간 |
| **예시** | 사용자가 클릭한 시각 | Kafka에 도달한 시각 |
| <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 원인</strong> | 네트워크·배터리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 없음 |
| **정확도** | 높음 (실제 시간 반영) | 낮음 ([네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/) 미반영) |
| **복잡도** | 높음 ([워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 필요) | 낮음 |

### [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">워터마크 개념</div></div>
<div class="kb-diagram-note">이벤트 시간: 09:00 09:01 09:02 ... (지연 이벤트: 09:00 이벤트가 09:05에 도달)</div>
<div class="kb-diagram-note">워터마크 = 현재 최대 이벤트 시간 - 허용 지연 시간</div>
<div class="kb-diagram-note">예: 최대 이벤트 시간 09:05, 허용 지연 2분 → 워터마크 = 09:03</div>
<div class="kb-diagram-note">09:03 이전 이벤트는 "완전하다" 판단 → 윈도우 닫기 가능</div>
<div class="kb-diagram-note">09:03 이후 도착한 09:00 이벤트는 "늦음" → 무시 또는 별도 처리</div>
</div>
</div>



📢 **섹션 요약 비유**: [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)는 우체국의 "마감 시간"이다. "오후 5시 이전 소인이 찍힌 편지는 오늘 처리한다"는 규칙처럼, [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 이전 시간의 이벤트만 현재 윈도우에서 처리하고, 너무 늦게 도착한 편지([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트)는 별도로 처리한다.

---

## Ⅲ. 비교 및 연결

### 스트림 처리 프레임워크 비교

| 비교 항목 | [Apache Flink](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) | [Spark Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams |
|:---|:---|:---|:---|
| **처리 모델** | 네이티브 스트리밍 | 마이크로배치 | 네이티브 스트리밍 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | 밀리초 | 수백ms~수초 | 밀리초 |
| **상태 관리** | 강력 (RocksDB) | 보통 | 가능 |
| **이벤트 시간** | 완전 지원 | 지원 | 지원 |
| **복잡 이벤트 처리** | 우수 | 보통 | 제한적 |
| **배치 통합** | Flink Batch | Spark Batch | ❌ |
| **운영 복잡성** | 높음 | 중간 | 낮음 ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 내장) |
| **적합 사례** | 복잡한 이벤트 처리, 금융 | 기존 Spark 팀, 배치+스트리밍 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 간단 변환 |

### Exactly-Once vs At-Least-Once

| 보장 수준 | 설명 | 비용 | 사용 사례 |
|:---|:---|:---|:---|
| **At-Most-Once** | 손실 가능, 중복 없음 | 낮음 | [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) (손실 허용) |
| **At-Least-Once** | 중복 가능, 손실 없음 | 중간 | 이벤트 집계 ([멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 보장 시) |
| **Exactly-Once** | [정확히 한 번](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_cross_validation/) 처리 | 높음 | 금융 거래, 정산 |

📢 **섹션 요약 비유**: Exactly-Once는 계좌 이체와 같다. "한 번만" 처리되어야 하며, 두 번 이체(중복)되거나 미이체(손실)되면 안 된다. 반면 웹 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/)은 한두 개 누락되어도 통계에 큰 영향이 없으므로 At-Least-Once로 충분하다.

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
| 밀리초 단위 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 필요 | [Apache Flink](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) |
| 기존 Spark 팀 있음 | [Spark Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 중심 단순 변환 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams |
| AWS 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [Amazon Kinesis](/knowledge-base/studynote/16_bigdata/04_streaming/091_amazon_kinesis/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Analytics (Flink) |
| GCP | Google Dataflow (Apache Beam) |

📢 **섹션 요약 비유**: 스트림 처리 프레임워크 선택은 소방차 선택과 같다. 대형 화재(복잡한 이벤트)에는 Flink 사다리차가, 일반 화재에는 [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 펌프차가, 좁은 골목은 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams 소형 차가 적합하다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **실시간 의사결정** | [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), 긴급 알림을 초 단위로 실행 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 신선도</strong> | 항상 최신 상태의 집계/분석 결과 |
| **경쟁 우위** | 실시간 개인화 추천으로 고객 경험 극대화 |
| **운영 효율** | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 이상 즉시 감지로 장비 사고 예방 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **아키텍처 복잡성** | 상태 관리, 윈도우 설계, [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 튜닝 필요 |
| **운영 비용** | 클러스터 상시 가동으로 배치 대비 높은 비용 |
| <strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a> vs <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong> | [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 길게 설정할수록 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)↑·[정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)↑ |
| **재처리 어려움** | 실패 시 이벤트 재처리 복잡 ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 오프셋 관리) |

📢 **섹션 요약 비유**: 스트림 처리는 24시간 편의점 운영과 같다. 항상 열려있어(상시 클러스터) 언제든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 가능하지만, 야간 인건비(고비용)와 야간 운영의 복잡성(아키텍처 복잡도)이 있다. 대부분의 업무는 낮에만 영업하는 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)로 충분하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | 스트림 처리의 [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), 이벤트 소스 |
| [Apache Flink](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) | 스트림 처리의 표준 프레임워크 |
| [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) | 스트리밍의 대조 개념, [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 아키텍처에서 결합 |
| 윈도우 처리 | 스트림 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 구간 단위로 집계하는 핵심 기법 |
| [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 처리를 위한 시간 허용 한계 정의 |
| Exactly-Once | 금융 스트리밍에서 요구되는 처리 보장 수준 |
| [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)/[Kappa](/knowledge-base/studynote/16_bigdata/12_trends/235_kappa/) | 배치와 스트리밍을 결합·단일화하는 아키텍처 패턴 |

### 👶 어린이를 위한 3줄 비유 설명
1. 스트림 처리는 물이 흐르는 강에서 물고기를 바로바로 잡는 것이다. 강([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))에 물고기([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 흘러오면, 낚시꾼(Flink)이 즉시 잡아 요리한다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Batch (지연 처리) → Micro-batch (Spark Streaming)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">True Stream: Apache Flink · Kafka Streams</div>
<div class="kb-diagram-tree-item" style="--depth:2">Exactly-Once 보장 · Event-Time 처리</div>
<div class="kb-diagram-tree-item" style="--depth:2">Watermark: 늦은 이벤트 처리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Unified: Batch + Stream 통합 (Flink · Beam)</div>
</div>
</div>


2. 윈도우는 강의 그물을 일정 구간에 치는 것이다. 10분마다 그물을 걷어서 그 사이 잡힌 물고기를 세면, 10분 단위 어획량(집계)을 알 수 있다.
3. [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)는 "이 물고기는 너무 오래전에 잡힌 것이라 포함하지 않겠다"는 규칙이다. 너무 늦게 도착한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 결과에 포함하지 않아야 처리가 멈추지 않는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 228 / 371

← **이전**: [228. 배치 처리 (Batch Processing)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)
**다음**: [230. 아파치 카프카 (Apache Kafka)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/230_apache_kafka_distributed_messaging/) →

---
