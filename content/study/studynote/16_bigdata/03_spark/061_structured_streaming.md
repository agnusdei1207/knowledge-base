+++
weight = 61
title = "스파크 구조적 스트리밍 (Spark Structured Streaming)"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **구조적 스트리밍 (Structured Streaming)**은 [[056_spark_sql|Spark SQL]] 엔진 위에서 동작하는 확장 가능하고 [[296_fault_tolerance_architecture|결함 허용]](Fault-tolerant)이 가능한 [[229_stream_processing_kafka_flink|스트림 처리]] 엔진이다.
2. 실시간 [[001_dikw_pyramid|데이터]]를 지속적으로 추가되는 **'무한 테이블(Unbounded Table)'**로 간주하여, [[228_batch_processing_hadoop_spark|배치 처리]]와 동일한 DataFrame/Dataset API로 스트리밍 로직을 작성할 수 있다.
3. **체크포인트와 Write-ahead Log**를 통해 '[[083_cross_validation|정확히 한 번]](Exactly-once)' 처리 보증을 제공하며, 이벤트 시간(Event-time) 처리 및 [[085_watermark|워터마크]] 기능을 완벽히 지원한다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **정의**: 정적 [[001_dikw_pyramid|데이터]]에 대한 배치 [[298_qkv_attention|쿼리]]를 실행하듯이 스트리밍 [[001_dikw_pyramid|데이터]]를 처리할 수 있게 해주는 고수준 [[014_api_posix|API]] 기반의 실시간 처리 프레임워크이다.
- **배경**: 기존 [[060_spark_streaming_dstream|DStream]](마이크로 배치)의 복잡한 [[310_audit|RDD]] 조작과 이벤트 시간 처리의 한계를 극복하고, 배치와 스트리밍 코드의 통합(Unified)을 실현하기 위해 등장했다.
- **주요 활용**: 실시간 [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인, 실시간 대시보드 업데이트, [[101_iot_concept|IoT]] 센서 [[001_dikw_pyramid|데이터]]의 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]], 실시간 개인화 [[211_recommendation_system|추천 시스템]] 등에서 표준으로 사용된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 무한 테이블 (Unbounded Table) 모델
```text
[ Data Stream ] (Incoming events)
      |
      V
[ Input Table ] (Unbounded / Append-only)
+-------+-------+-------+
| Col 1 | Col 2 | Col 3 |  <-- New data appended every trigger
+-------+-------+-------+
      |
      V [ Incremental Query ] (Spark SQL Engine)
      |
[ Result Table ] (Updated state)
      |
      V [ Output Sink ] (External Storage)
```

#### 2. 핵심 처리 메커니즘
- **Trigger**: [[001_dikw_pyramid|데이터]]를 처리할 주기를 결정한다 (예: 1초마다, 혹은 [[001_dikw_pyramid|데이터]]가 들어오는 즉시 처리하는 연속 모드).
- **Watermarking**: 늦게 도착한 [[001_dikw_pyramid|데이터]](Late [[001_dikw_pyramid|Data]])를 얼마나 기다릴지 정의하여 상태 정보의 메모리 무한 증식을 방지한다.
- **[[272_state_pattern|State]] Store**: 윈도우 합계나 조인 처리를 위해 필요한 중간 상태값을 인메모리 혹은 [[013_hdfs|HDFS]]/S3에 안전하게 보관한다.
- **[[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]**: Checkpointing을 통해 장애 발생 시 마지막 처리 지점부터 중단 없이 재시작할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[060_spark_streaming_dstream|Spark Streaming]] ([[060_spark_streaming_dstream|DStream]]) | Structured Streaming |
| :--- | :--- | :--- |
| **기반 [[198_abstraction_control_data_process|추상화]]** | [[310_audit|RDD]] (Low-level) | DataFrame / Dataset (High-level) |
| **처리 모델** | 마이크로 배치 전용 | 마이크로 배치 + 연속 처리(Continuous) |
| **이벤트 시간 처리** | 지원 미흡 (Processing Time 위주) | [[085_watermark|워터마크]] 기반 완벽 지원 |
| **코드 통합** | 배치 코드와 별도 작성 필요 | 배치 [[298_qkv_attention|쿼리]]와 90% 이상 동일 코드 사용 |
| **보증 수준** | At-least-once (일부 상황) | Exactly-once (엔드 투 엔드 보장) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **배치-스트림 통합 아키텍처**: 동일한 로직을 배치 [[001_dikw_pyramid|데이터]]와 실시간 [[001_dikw_pyramid|데이터]]에 모두 적용할 수 있어 유지보수 비용을 획기적으로 낮춘다 ([[216_lambda_kappa_architecture_batch_realtime|Lambda]]/[[235_kappa|Kappa]] 아키텍처 구현 용이).
- **Sink 선택 [[268_strategy_pattern|전략]]**: [[179_kafka_flink_watermark_time_window|Kafka]], [[013_hdfs|HDFS]], Console 외에도 Delta Lake와 결합하여 실시간 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]를 구축하는 것이 최신 기술 트렌드이다.
- **[[282_performance_tactics|성능]] 최적화**: 셔플링을 유도하는 [[086_window_operations|윈도우 연산]] 시 [[514_partition_slice_volume|파티션]] 개수(`spark.sql.shuffle.partitions`)를 [[001_dikw_pyramid|데이터]] 규모에 맞게 조정하고, 로컬 상태 저장소의 [[282_performance_tactics|성능]](RocksDB 등)을 튜닝해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: [[001_dikw_pyramid|데이터]] 엔지니어가 실시간 처리를 위해 특별한 기술을 새로 배울 필요 없이 기존 SQL/DataFrame 지식만으로 고성능 [[009_real_time_system|실시간 시스템]]을 구축할 수 있게 한다.
- **결론**: 구조적 스트리밍은 '배치와 스트리밍의 경계'를 허문 혁신적인 도구이다. 향후 Apache Flink와의 경쟁 속에서도 Spark 생태계의 강력한 통합 이점을 바탕으로 실시간 [[001_dikw_pyramid|데이터]] 처리의 중추 역할을 지속할 것으로 전망된다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
1. **Micro-[[389_bulk_insert_batching_optimization|batching]]**: [[001_dikw_pyramid|데이터]]를 아주 작은 단위로 묶어 처리하는 방식
2. **[[083_cross_validation|Exactly-once Semantics]]**: [[001_dikw_pyramid|데이터]] 손실이나 중복 없이 [[083_cross_validation|정확히 한 번]] 처리됨을 보장
3. **Event Time**: [[001_dikw_pyramid|데이터]]가 시스템에 입력된 시간이 아닌, 실제 발생한 시간

---

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리 (Batch Processing) — 정해진 주기 대규모 데이터 처리]
    │
    ▼
[스트리밍 처리 (Streaming) — 실시간 연속 데이터 처리]
    │
    ▼
[Spark Streaming (DStream) — RDD 기반 마이크로 배치]
    │
    ▼
[Structured Streaming — DataFrame API 기반 연속 처리]
    │
    ▼
[워터마크 (Watermark) — 지연 데이터 처리 기준 시간 설정]
    │
    ▼
[Delta Live Tables — 선언형 스트리밍 파이프라인 자동화]
```
Structured Streaming은 DStream의 복잡성을 DataFrame API로 [[198_abstraction_control_data_process|추상화]]하여, 배치와 스트리밍을 통합하는 현대 실시간 [[123_pipe|파이프]]라인의 표준이 되었다.

### 👶 어린이를 위한 3줄 비유 설명
1. "수도꼭지에서 물이 계속 나오는 것처럼, 멈추지 않고 들어오는 [[001_dikw_pyramid|데이터]]를 바로바로 정리하는 기계예요."
2. "예전에는 바가지로 물을 퍼 날랐다면(배치), 이제는 호스를 연결해서 물이 흐르는 대로 [[104_classification_analysis|분류]]하는 것과 같아요."
3. "깜빡하고 늦게 들어온 [[001_dikw_pyramid|데이터]]도 제자리에 쏙쏙 끼워 넣어주는 아주 똑똑한 정리 대장이랍니다!"
