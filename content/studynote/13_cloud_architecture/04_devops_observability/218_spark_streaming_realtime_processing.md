---
title: "Spark Streaming Realtime Processing"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 218
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Spark Structured Streaming은 실시간 스트림 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 "무한히 쌓이는 테이블(Unbounded Table)"로 추상화하여 배치와 동일한 DataFrame API로 처리하는 실시간 처리 엔진이며, 마이크로 배치와 연속 처리 두 모드를 지원한다.
> 2. **가치**: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 소스와의 완전한 통합, 이벤트 시간(Event-time) 기반 [윈도우 연산](/studynote/16_bigdata/04_streaming/086_window_operations/), [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/))를 통한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리로 [정확히 한 번](/studynote/12_it_management/02_itsm_itil/083_cross_validation/)(Exactly-once) 처리 의미론을 보장한다.
> 3. **판단 포인트**: 마이크로 배치는 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 수백ms~수 초([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))지만 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))이 높고, 연속 처리는 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) ~1ms이지만 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 낮다. 대부분의 실무는 수 초 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 허용되므로 마이크로 배치가 표준이다.

---

## Ⅰ. 개요 및 필요성

기업의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 요구가 "어젯밤 [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/)(배치)" 수준을 넘어 "지금 이 순간 이상 감지·추천·알림"으로 진화하면서 실시간 [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/)가 필수가 됐다. 넷플릭스가 사용자가 영상을 보는 동안 실시간으로 스트리밍 품질을 조정하고, 우버가 실시간으로 근방 드라이버를 매칭하는 것이 대표적 사례다.

[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [Spark Streaming](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/)(Spark 1.x)은 [DStream](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/)(Discretized [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)) API를 사용했다. 스트림 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 고정 시간 간격(예: 1초)으로 RDD로 쪼개어 배치처럼 처리하는 방식이었다. 동작은 했지만 이벤트 시간 처리, 상태 관리, exactly-once 보장이 복잡했다.

Spark 2.0에서 등장한 <strong><a href="/studynote/16_bigdata/03_spark/061_structured_streaming/">Structured Streaming</a></strong>은 완전히 재설계됐다. 핵심 아이디어: <strong>스트림을 끝없이 행이 추가되는 테이블</strong>로 본다. 개발자는 이 테이블에 배치와 동일한 DataFrame/SQL [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 작성하고, Spark이 내부적으로 마이크로 배치로 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 반복 실행하여 결과를 점진적으로 업데이트한다.

📢 **섹션 요약 비유**: Structured Streaming은 뉴스 자막 기계와 같다. 자막 기계는 기자가 전송하는 뉴스(스트림)를 화면 아래에 계속 추가하는 테이블처럼 처리하여, 매초 새로운 자막을 자동으로 표시한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) 실행 모델

```
  +------------------------------------------------------------+
  |               Structured Streaming 처리 모델                |
  +------------------------------------------------------------+
  |                                                             |
  |  소스 (Kafka/File/Socket)                                   |
  |       | 새 데이터 계속 유입                                  |
  |       v                                                     |
  |  Input Table (무한히 쌓이는 테이블 추상화)                   |
  |  +------------------------------------------------------+  |
  |  | T=0 | event_1, event_2                               |  |
  |  | T=1 | event_3, event_4, event_5                      |  |
  |  | T=2 | event_6                                        |  |
  |  | ... | (계속 쌓임)                                     |  |
  |  +------------------------------------------------------+  |
  |       | 동일한 DataFrame 쿼리 적용                           |
  |       v                                                     |
  |  Result Table (쿼리 결과 테이블)                             |
  |       |                                                     |
  |       v 마이크로 배치마다 업데이트                            |
  |  Output (Console/File/Kafka/DB 등)                          |
  +------------------------------------------------------------+
```

### [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 소스 연동 코드

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StringType, LongType

spark = SparkSession.builder \
    .appName("RealtimeOrderAnalysis") \
    .getOrCreate()

# Kafka 소스 읽기 (실시간 스트림)
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# JSON 파싱
schema = StructType() \
    .add("order_id", LongType()) \
    .add("user_id", LongType()) \
    .add("amount", LongType()) \
    .add("timestamp", LongType())

orders = kafka_df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# 이벤트 시간 기반 윈도우 집계 (5분 윈도우, 1분 슬라이딩)
windowed_counts = orders \
    .withWatermark("timestamp", "10 minutes") \  # 지연 데이터 10분까지 허용
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("user_id")
    ) \
    .agg(count("order_id").alias("order_count"),
         sum("amount").alias("total_amount"))

# 싱크: 콘솔 출력 (처음 N개만, 개발용)
query = windowed_counts.writeStream \
    .outputMode("update") \      # 변경된 행만 출력
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \  # 10초마다 마이크로 배치
    .start()

query.awaitTermination()
```

### [윈도우 연산](/studynote/16_bigdata/04_streaming/086_window_operations/) 유형

| 윈도우 유형 | 설명 | 예시 |
|:---|:---|:---|
| **Tumbling Window** | 겹치지 않는 고정 크기 윈도우 | 1분마다 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 |
| **Sliding Window** | 슬라이딩 간격으로 이동하는 윈도우 | 5분 윈도우, 1분마다 이동 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">Session</a> Window</strong> | 비활성 기간으로 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 구분 | 30초 이상 이벤트 없으면 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 종료 |

📢 **섹션 요약 비유**: [윈도우 연산](/studynote/16_bigdata/04_streaming/086_window_operations/)은 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 창문으로 바깥을 보는 것과 같다. Tumbling은 매 정류장마다 새 창문, Sliding은 창문이 조금씩 이동하면서 앞 풍경과 현재 풍경이 겹치는 것이다.

---

## Ⅲ. 비교 및 연결

### 처리 모드 비교

| 모드 | 최소 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | 정확도 | 사용 시나리오 |
|:---|:---:|:---:|:---:|:---|
| 마이크로 배치 (기본) | ~100ms | 높음 | Exactly-once | 대부분의 실시간 처리 |
| 연속 처리 (Spark 2.3+) | ~1ms | 낮음 | At-least-once | 초저지연 필요 시 |
| [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) (비교용) | 분~시간 | 최고 | Exactly-once | 대규모 비실시간 |

### 출력 모드 (OutputMode)

| 모드 | 설명 | 적합 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
|:---|:---|:---|
| **Append** | 새로 추가된 행만 출력 | 집계 없는 변환, [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) 적용 시 |
| **Complete** | 결과 테이블 전체를 매번 출력 | 소규모 집계 결과 |
| **Update** | 변경된 행만 출력 | 집계 + 실시간 대시보드 |

### [Spark Streaming](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) vs [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/)

| 항목 | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) | [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) |
|:---|:---|:---|
| 처리 방식 | 마이크로 배치 (기본) | 진정한 [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) |
| [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | 수백ms~수 초 | ~수ms |
| [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | 높음 | 중간 |
| 배치 통합 | ✅ (배치와 동일 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) | 별도 DataSet [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| 상태 관리 | 좋음 | 매우 강함 |
| 적합 시나리오 | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 우선 | 초저지연 필요 |

📢 **섹션 요약 비유**: Spark Streaming과 Flink의 차이는 편의점 계산대(Spark, 10초마다 일괄 처리)와 고속 체크아웃(Flink, 아이템마다 즉시 처리)의 차이다. 빠른 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 편의점이, 즉각 반응은 고속 체크아웃이 강하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/16_bigdata/04_streaming/085_watermark/">워터마크</a>(<a href="/studynote/16_bigdata/04_streaming/085_watermark/">Watermark</a>) <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>:
```python
# 이벤트 시간 vs 처리 시간
# 이벤트: 15:00:00에 발생 -> 네트워크 지연으로 15:00:30에 도착
# 워터마크 10분 설정: 15:10:00 이후에는 15:00:00 이벤트를 늦은 데이터로 처리

windowed = df \
    .withWatermark("event_time", "10 minutes") \  # 10분 지연 허용
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    ) \
    .count()

# 워터마크 없으면: 지연 데이터 기다리느라 메모리 무한 증가
# 워터마크 있으면: 허용 시간 초과한 지연 데이터는 버리고 상태 메모리 정리
```

<strong><a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a> -> Spark -> S3 파이프라인</strong>:
```python
# Delta Lake로 실시간 데이터 저장 (ACID 트랜잭션 지원)
orders.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://checkpoints/orders/") \
    .option("path", "s3://data/orders/") \
    .trigger(processingTime="30 seconds") \
    .start()
```

**기술사 판단 포인트**:
- Checkpoint Location은 장애 복구의 핵심이다. Spark가 재시작될 때 checkpoint에서 마지막 처리 오프셋을 읽어 중복 처리 없이 이어서 실행한다.
- 상태 있는 집계(Stateful Aggregation)는 상태가 메모리에 축적되므로, [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)로 오래된 상태를 주기적으로 정리해야 메모리 문제를 방지한다.
- Structured Streaming과 Delta Lake의 조합이 현대 실시간 [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) 아키텍처의 표준이 되고 있다.

📢 **섹션 요약 비유**: Checkpoint는 게임 세이브처럼, 서버가 재시작되어도 마지막으로 처리한 위치에서 이어서 처리한다. Checkpoint 없으면 재시작 시 처음부터 또는 중복 처리가 발생한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 배치·스트리밍 통합 | 동일한 DataFrame API로 배치와 스트리밍 처리 |
| Exactly-once 보장 | [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/)과 멱등 싱크로 [정확히 한 번](/studynote/12_it_management/02_itsm_itil/083_cross_validation/) 처리 |
| 이벤트 시간 처리 | [네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)로 처리 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 완전 통합 | 오프셋 관리·[체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/) 자동화 |

Spark Structured Streaming은 "빅데이터 [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)의 강점을 실시간 처리로 확장"한 결과물이다. 카프카와의 통합, Delta Lake와의 조합으로 현대 [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 아키텍처와 [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처를 모두 Spark 단일 플랫폼으로 구현할 수 있게 됐다. 정보통신기술사 시험에서 스트리밍 처리 아키텍처와 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)·Spark의 연계는 빈출 주제다.

📢 **섹션 요약 비유**: Structured Streaming은 강의 물흐름(스트림)을 배와 양동이(배치) 없이 수력 발전기로 직접 처리하는 것과 같다. 물이 흐르는 그 자리에서 즉시 에너지(인사이트)를 추출하여 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 활용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | Structured Streaming의 가장 일반적인 소스 |
| [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) ([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/)) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리와 상태 메모리 관리의 핵심 |
| 마이크로 배치 | Structured Streaming의 기본 실행 모드 |
| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | [Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) 결과 저장의 현대 표준 |
| [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) | 초저지연 스트리밍에서 Spark의 대안 도구 |
| Exactly-once | [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/)으로 보장하는 스트리밍 처리 의미론 |

### 👶 어린이를 위한 3줄 비유 설명

1. Structured Streaming은 쇼핑몰 CCTV처럼, 카메라([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))에서 계속 들어오는 영상(이벤트)을 실시간으로 분석해서 도둑이 있는지(이상 감지) 알려줘.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 처리 (지연 ^, 실시간성 v)
    |
    v
Spark Streaming: 마이크로배치 (준실시간)
    |
    v
Structured Streaming: DataFrame API + Event-Time + Watermark
    |
    v
Flink: True Streaming (이벤트별 처리) · 정확히 한 번 보장
```
2. 마이크로 배치는 10초마다 영상을 묶어서 분석하는 것, 연속 처리는 프레임마다 즉시 분석하는 거야.
3. [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)는 "이미 10분 지난 영상은 그냥 넘어가자"라는 규칙이야. 너무 늦게 온 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 기다리지 않고 무시해서 메모리가 꽉 차지 않게 해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 217 / 371

<- **이전**: [217. 지연 평가 / DAG 최적화 (Lazy Evaluation)](/studynote/13_cloud_architecture/04_devops_observability/217_lazy_evaluation_spark_optimization/)
**다음**: [219. 데이터 레이크 (Data Lake) - 원시 데이터 중심의 전사적 통합 저장소](/studynote/13_cloud_architecture/05_data_engineering/219_data_lake/) ->

---
