---
title: Spark Streaming (DStream) 아키텍처
date: '2024-03-24'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **마이크로 배치(Micro-batch):** 실시간 스트림 [[001_dikw_pyramid|데이터]]를 아주 짧은 간격(예: 1초)의 작은 배치로 쪼개어 기존 스파크 배치 엔진으로 처리하는 방식.
- **DStream (Discretized [[467_http2_stream_multiplexing_tcp_hol|Stream]]):** 연속적인 [[001_dikw_pyramid|데이터]] 흐름을 시간 단위의 [[310_audit|RDD]] 시퀀스로 [[198_abstraction_control_data_process|추상화]]하여, 기존 [[310_audit|RDD]] 연산을 스트리밍 환경에서 그대로 활용 가능.
- **신구 조화:** 초저지연(Native Streaming)보다는 [[139_throughput|처리량]]([[139_throughput|Throughput]])과 기존 코드 재사용성에 강점이 있으며, 현재는 Structured Streaming으로 진화하는 과도기적 핵심 기술.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
[[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]]의 첫 번째 스트리밍 [[336_library_vs_framework|라이브러리]]인 Spark Streaming은 "모든 [[229_stream_processing_kafka_flink|스트림 처리]]는 아주 작은 배치의 연속"이라는 철학에서 시작되었습니다. 이는 플링크(Flink) 같은 '이벤트 단위' 처리 모델과 대비되는 특징으로, [[211_hadoop_ecosystem_mapreduce|하둡 에코시스템]]과의 강력한 통합과 고도의 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) 기능을 제공하며 실시간 분석 시장을 선도했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Spark Streaming은 입력을 짧은 주기의 RDD로 변환하여 스파크 코어 엔진으로 전달합니다.

```text
[ Spark Streaming Micro-batch Architecture ]

   (Input Stream)        (Spark Streaming)        (Spark Core)
   Kafka/Flume/S3           Receiver               Engine
   ~~~~~~~~~~~~~~       +---------------+       +-----------+
   Data Flow (t)  --->  | Micro-batch 1 | ----> | RDD (t)   |
   ~~~~~~~~~~~~~~       | (1 second)    |       +-----------+
                        +---------------+       +-----------+
                        | Micro-batch 2 | ----> | RDD (t+1) |
                        | (1 second)    |       +-----------+
                        +---------------+

[ DStream Definition ]
DStream = Sequence of RDDs (t, t+1, t+2, ...)
* Operation: DStream.map() internally calls RDD.map() for each batch.
```

**핵심 원리:**
1. **Receiver:** 워커 노드에서 실행되며 외부 소스로부터 [[001_dikw_pyramid|데이터]]를 수집해 메모리에 저장하고 [[016_replication_factor|복제]]하여 안정성 확보.
2. **배치 간격 (Batch Interval):** 스트림을 쪼개는 최소 시간 단위. 시스템의 [[141_latency|지연 시간]]([[141_latency|Latency]])을 결정함.
3. **[[086_window_operations|윈도우 연산]] ([[086_window_operations|Window Operations]]):** 현재 배치뿐 아니라 과거 여러 배치를 묶어서 집계(예: 최근 10분간의 평균) 수행.
4. **[[071_checkpointing|체크포인팅]] ([[071_checkpointing|Checkpointing]]):** 장애 시 상태 [[658_ir_recovery|복구]]를 위해 [[012_metadata|메타데이터]]와 [[310_audit|RDD]] [[001_dikw_pyramid|데이터]]를 안정적인 스토리지([[013_hdfs|HDFS]])에 저장.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Spark Streaming (DStream) | [[061_structured_streaming|Structured Streaming]] |
| :--- | :--- | :--- |
| **[[014_api_posix|API]] 모델** | [[310_audit|RDD]] 기반 (Low-level) | DataFrame/Dataset 기반 (High-level) |
| **처리 방식** | 시간 기반 마이크로 배치 | 무한히 성장하는 테이블 (Append-only) |
| **최적화** | 수동 [[310_audit|RDD]] 튜닝 필요 | Catalyst/Tungsten 자동 최적화 |
| **이벤트 시간** | 처리 시간 기준 중심 (복잡) | 원어민 수준의 Event Time/[[085_watermark|Watermark]] 지원 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **실무 적용:** 기존에 작성된 대규모 스파크 배치 코드를 실시간으로 전환해야 할 때, DStream 모델을 사용하면 비즈니스 로직 수정 없이 배포할 수 있어 마이그레이션 비용이 저렴합니다.
- **기술사적 판단:** DStream은 '초당 수십만 건'의 대량 처리에 유리하지만, '밀리초' 단위의 반응 속도가 중요한 증권 거래 등에는 부적합할 수 있습니다. 기술사는 비즈니스 요구사항([[141_latency|지연 시간]] vs [[139_throughput|처리량]])을 분석하여 Spark Streaming과 Flink 중 적합한 엔진을 권고해야 합니다. 또한 최신 프로젝트라면 [[282_performance_tactics|성능]]과 편의성이 개선된 '[[061_structured_streaming|Structured Streaming]]'으로의 전환을 우선 고려해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Spark Streaming은 빅데이터 [[228_batch_processing_hadoop_spark|배치 처리]]와 실시간 처리를 단일 코드 베이스로 통합한 혁신적인 사례입니다. 비록 현재는 구조화된 스트리밍([[061_structured_streaming|Structured Streaming]])에 주류 자리를 내주고 있으나, 마이크로 배치 사상은 [[227_cloud_cost_optimization|클라우드 비용 최적화]]([[206_serverless_cold_start|서버리스]] 가동 시간 제어) 관점에서 여전히 유효한 아키텍처 표준입니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념:** Real-time [[001_dikw_pyramid|Data]] Processing, [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]]
- **하위 개념:** Micro-batch, DStream, Receiver, Batch Interval
- **연관 기술:** [[215_flink_native_stream_watermark_window_time|Apache Flink]] (Native [[467_http2_stream_multiplexing_tcp_hol|Stream]]), [[179_kafka_flink_watermark_time_window|Kafka]], [[061_structured_streaming|Structured Streaming]]

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리(Spark Core)]
    │
    ▼
[마이크로 배치]
    │
    ▼
[Spark Streaming(DStream)]
    │
    ▼
[Structured Streaming]
    │
    ▼
[실시간 분석 파이프라인]
```

Spark Streaming은 배치 중심 Spark에서 마이크로 배치와 DStream, Structured Streaming으로 진화했다.

### 👶 어린이를 위한 3줄 비유 설명
1. 수도꼭지에서 계속 나오는 물(스트림)을 아주 작은 컵(마이크로 배치)에 1초마다 받아내는 거예요.
2. 그 컵이 찰 때마다 정수기(스파크 엔진)로 가져가서 깨끗하게 걸러내는 방식이죠.
3. 컵이 작을수록 물을 빨리 처리할 수 있고, 컵을 한 줄로 줄 세워 놓으면 물의 흐름을 놓치지 않는답니다.
