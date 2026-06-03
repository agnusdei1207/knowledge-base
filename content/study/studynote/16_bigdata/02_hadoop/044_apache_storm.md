+++
weight = 44
title = "아파치 스톰 (Apache Storm) 및 실시간 분산 처리"
date = "2024-03-24"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- **네이티브 스트리밍:** 마이크로배치 방식이 아닌, [[001_dikw_pyramid|데이터]] 하나하나를 즉시 처리하는 이벤트 기반 [[136_variance|분산]] 실시간 연산 프레임워크.
- **토폴로지 구조:** Spout([[001_dikw_pyramid|데이터]] 수집)와 Bolt([[001_dikw_pyramid|데이터]] 변환/집계)를 [[401_bayesian_network_dag_causality|DAG]](비순환 방향 [[070_graph_datastructure|그래프]])로 묶어 중단 없는 [[229_stream_processing_kafka_flink|스트림 처리]] 흐름 구현.
- **[[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]):** [[063_relation_tuple_cardinality|튜플]](Tuple) 단위의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 보장 메커니즘을 통해 [[001_dikw_pyramid|데이터]] 유실 없는 안정적인 스트리밍 [[090_service_kubernetes_network_load_balancing|서비스]] 제공.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
빅데이터 [[459_quic_fec_forward_error_correction|초기]], [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[018_mapreduce|맵리듀스]]는 디스크 기반 [[228_batch_processing_hadoop_spark|배치 처리]]에는 강력했으나 실시간 응답이 필요한 시스템에는 부적합했습니다. Apache Storm은 "실시간 [[843_hadoop_rack_awareness_data_replication_topology|하둡]](Real-time [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]])"이라 불리며 등장하여, [[001_dikw_pyramid|데이터]]가 유입되는 즉시 수 밀리초(ms) 내에 연산을 수행할 수 있는 환경을 제공했습니다. 이는 금융 거래 사기 탐지, 실시간 대시보드 업데이트, [[101_iot_concept|IoT]] 센서 [[001_dikw_pyramid|데이터]] [[229_monitor|모니터]]링 분야의 혁신을 이끌었습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Storm은 영구적으로 실행되는 토폴로지(Topology) 아키텍처를 기반으로 합니다.

```text
[ Apache Storm Topology: Spout & Bolt ]

   (Data Source)         (Processing Unit)        (Storage/Output)
   -------------        -------------------      ------------------
   [   Spout   ] ---->  [     Bolt 1      ] ----> [   Final DB     ]
   (Data Ingest)        (Filtering/Logic)        [ (Result Store) ]
       |                       |
       |                [     Bolt 2      ]
       +--------------> (Aggregation/Joins)

[ Core Components ]
1. Spout: 외부 소스(Kafka, Twitter 등)에서 데이터를 읽어 튜플 스트림 생성.
2. Bolt: 실제 비즈니스 로직(필터링, 조인, DB 저장 등)을 수행하는 연산 노드.
3. Tuple: 스톰에서 처리되는 데이터의 기본 단위 (List of Values).
4. Nimbus: 마스터 노드로 코드 배포 및 작업 할당 관리.
5. Supervisor: 실제 작업을 수행하는 워커 프로세스 관리 노드.
```

**핵심 원리:**
1. **스트림 [[535_grouping_counting_free_space|그룹화]]([[467_http2_stream_multiplexing_tcp_hol|Stream]] Groupings):** [[001_dikw_pyramid|데이터]](Tuple)를 어떤 Bolt로 보낼지 결정하는 [[268_strategy_pattern|전략]](Shuffle, Fields, All [[535_grouping_counting_free_space|grouping]] 등).
2. **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 전파(Ack/Fail):** [[063_relation_tuple_cardinality|튜플]] 처리가 성공하면 Ack를 보내고, 실패 시 처음부터 재시도하여 최소 1회 처리(At-least-once) 보장.
3. **무한 루프 실행:** 배치와 달리 작업이 종료되지 않고 [[001_dikw_pyramid|데이터]]가 들어올 때까지 대기하며 지속 실행.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]] | Apache Storm | Apache [[060_spark_streaming_dstream|Spark Streaming]] |
| :--- | :--- | :--- | :--- |
| **처리 모델** | 배치 (Batch) | 네이티브 스트림 ([[467_http2_stream_multiplexing_tcp_hol|Stream]]) | 마이크로 배치 (Micro-batch) |
| **[[141_latency|지연 시간]] ([[141_latency|Latency]])** | 분~시간 (High) | 밀리초 (Very Low) | 초 단위 (Low) |
| **상태 관리** | [[501_file_definition_logical_record|파일]] 기반 ([[013_hdfs|HDFS]]) | 외부에 별도 관리 필요 | 인메모리 ([[071_checkpointing|Checkpointing]]) |
| **상태 보장** | Exactly-once | At-least-once (기본) | Exactly-once |
| **주요 용도** | 대규모 통계 분석 | 초저지연 알람, 실시간 처리 | 복잡한 분석 및 [[241_machine_learning_basics|머신러닝]] |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **실무 적용:** 웹 [[090_service_kubernetes_network_load_balancing|서비스]]의 실시간 [[119_log_analysis|로그 분석]] 시, Spout로 [[179_kafka_flink_watermark_time_window|카프카]] [[389_mesh_topology|메시]]지를 읽고 Bolt에서 특정 에러 키워드를 필터링하여 이상 징후 발생 시 0.1초 내에 관리자에게 푸시 알림을 보내는 시스템에 적합합니다.
- **기술사적 판단:** Storm은 상태 관리([[272_state_pattern|State]] [[372_management|Management]]) 기능이 약해 Flink나 Spark에 밀려나는 추세였으나, 단순하고 빠른 처리가 필요한 영역에서는 여전히 유효합니다. 기술사는 "복잡한 [[086_window_operations|윈도우 연산]]이나 정확한 상태 유지가 필요하다면 Storm 보다는 Trident(Storm의 고차원 [[198_abstraction_control_data_process|추상화]])나 Flink를 선택해야 한다"는 설계 가이드라인을 제시해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Apache Storm은 실시간 [[136_variance|분산]] 컴퓨팅의 원형을 정립한 도구입니다. 비록 최근에는 Apache Flink나 Spark Structured Streaming에 주류 자리를 넘겨주었지만, [[001_dikw_pyramid|데이터]] 흐름 지향(Dataflow) 프로그래밍 모델의 기초 지식으로서 가치가 높으며, 경량화된 실시간 [[123_pipe|파이프]]라인 구축 시 효율적인 대안으로 지속 활용될 것입니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념:** [[229_stream_processing_kafka_flink|Stream Processing]], Distributed Computing
- **하위 개념:** Spout, Bolt, Topology, [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[535_grouping_counting_free_space|Grouping]]
- **연관 기술:** [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]], [[215_flink_native_stream_watermark_window_time|Apache Flink]], [[060_spark_streaming_dstream|Spark Streaming]], Apache Samza

### 📈 관련 키워드 및 발전 흐름도

```text
[Spout (데이터 소스 — Kafka · 파일 · API)]
    │
    ▼
[스트림 (Stream) — 무한 데이터 튜플 흐름]
    │
    ▼
[Bolt (처리·변환·집계 — 필터·조인·집계)]
    │
    ▼
[토폴로지 (Topology) — Spout + Bolt 유향 그래프]
    │
    ▼
[Apache Flink / Spark Structured Streaming — 후계 진화]
```
Spout가 수집한 스트림이 Bolt 체인을 거쳐 처리되는 토폴로지 모델로 실시간 [[136_variance|분산]] 처리의 원형을 정립하고, Flink와 Spark Streaming으로 계승·발전된 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 폭포수([[001_dikw_pyramid|데이터]])가 끊임없이 쏟아지는 통로에 '물레방아(Spout)'를 설치해요.
2. 물레방아가 물을 퍼 올리면, 중간중간 '거름망(Bolt)'이 나뭇잎을 걸러내고 깨끗한 물만 통과시켜요.
3. 이 모든 과정이 쉬지 않고 아주 빠르게 돌아가는 거대한 정수기 시스템이 바로 Storm이에요.
