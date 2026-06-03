---
title: 09. 맵리듀스 (MapReduce) - 대규모 데이터 병렬 처리를 위한 분산 프로그래밍 모델
date: '2026-03-04'
tags:
- hadoop
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **[[005_divide_and_conquer|분할 정복]]의 표준**: 방대한 [[001_dikw_pyramid|데이터]]를 작은 단위로 나누어 [[430_index_fast_full_scan|병렬]]로 처리(Map)하고, 그 결과를 하나로 합쳐(Reduce) 최종 통찰을 도출하는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 핵심 연산 프레임워크입니다.
- **[[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]])**: [[001_dikw_pyramid|데이터]]가 있는 곳으로 [[159_opcode|연산 코드]]를 보내어(Function to [[001_dikw_pyramid|Data]]) 대규모 [[001_dikw_pyramid|데이터]] 이동에 따른 네트워크 병목을 획기적으로 줄입니다.
- **[[233_recovery_database_restoration_overview|회복]] [[571_resiliency_fault_tolerance_patterns|탄력성]]**: 작업 도중 특정 서버가 고장 나도 다른 서버가 해당 작업을 자동으로 재수행하여 결코 멈추지 않는 [[136_variance|분산]] 연산을 보장합니다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
수 테라바이트의 [[001_dikw_pyramid|데이터]]를 단일 서버에서 처리하는 것은 불가능에 가깝습니다. 구글이 2004년 발표한 논문을 바탕으로 구현된 [[018_mapreduce|맵리듀스]]는 "[[001_dikw_pyramid|데이터]]를 쪼개서 수만 대의 서버에 나눠주고(Map), 다 끝난 결과를 묶어서 가져온다(Reduce)"는 단순하지만 강력한 철학을 통해 빅데이터 분석의 시대를 열었습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[[018_mapreduce|맵리듀스]]는 Map - [[205_shuffle_sort_yarn_resource_manager|Shuffle & Sort]] - Reduce의 단계를 거치며 모든 [[001_dikw_pyramid|데이터]]는 ([[067_db_key_uniqueness_minimality|Key]], Value) 쌍으로 처리됩니다.

```text
[ MapReduce Processing Flow Architecture ]

1. Input Split: Split large file into blocks (HDFS).
2. Map: Filter and sort data (e.g., Word counting).
3. Shuffle & Sort: Group values by key across nodes (Heavy Network I/O).
4. Reduce: Aggregate values for each key.

[ Diagram: Word Count Example ]
(Input: "Apple Banana Apple") 
      |
[ Map ] --> (Apple, 1), (Banana, 1), (Apple, 1)
      |
[ Shuffle ] --> (Apple: [1, 1]), (Banana: [1])
      |
[ Reduce ] --> (Apple: 2), (Banana: 1)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[[018_mapreduce|맵리듀스]]와 차세대 엔진인 스파크를 비교합니다.

| 비교 항목 | [[018_mapreduce|맵리듀스]] ([[018_mapreduce|MapReduce]]) | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]] (Spark) |
| :--- | :--- | :--- |
| **저장 [[121_transmission_media_guided_unguided|매체]]** | **디스크 ([[013_hdfs|HDFS]]) 기반** | **메모리 (In-Memory) 기반** |
| **속도** | 느림 (단계별 디스크 I/O 발생) | **매우 빠름 (최대 100배)** |
| **복잡도** | Java 코딩 필요 (낮은 [[198_abstraction_control_data_process|추상화]]) | 다양한 [[014_api_posix|API]] (Python/SQL, 높은 [[198_abstraction_control_data_process|추상화]]) |
| **적합성** | 배치성 대용량 정산/통계 | 실시간, 반복 연산, [[241_machine_learning_basics|머신러닝]] |
| **안정성** | 매우 높음 (중간 결과 디스크 보존) | 높음 (리니지 기반 [[658_ir_recovery|복구]]) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **셔플 최적화**: [[018_mapreduce|맵리듀스]]의 가장 큰 병목은 셔플(Shuffle) 단계의 네트워크 전송입니다. `Combiner`를 사용하여 맵 단계에서 1차 집계를 수행함으로써 전송량을 줄여야 합니다.
2. **[[228_batch_processing_hadoop_spark|배치 처리]]의 제왕**: 실시간성보다는 며칠 치의 거대 [[568_logs_distributed_logging_elk_fluentd|로그]]를 정산하거나 과거 [[001_dikw_pyramid|데이터]]를 전수 조사하는 'Heavy Batch' 작업에 여전히 비용 효율적인 선택지가 됩니다.
3. **기술사적 판단**: [[018_mapreduce|맵리듀스]]는 '느리다'는 평가를 받지만, 극단적인 저사양 서버 클러스터에서도 디스크를 믿고 끝까지 작업을 완수해내는 끈기(Robustness)가 장점입니다. 최근에는 Hive의 엔진을 Tez나 Spark로 바꾸는 추세지만, 원리적 이해는 필수입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[018_mapreduce|맵리듀스]]는 단순한 소프트웨어를 넘어 '[[136_variance|분산]] 사고방식'의 표준을 제시했습니다. 비록 현재는 메모리 기반의 스파크나 실시간 플링크에 자리를 내주고 있지만, "[[001_dikw_pyramid|데이터]]가 있는 곳에서 연산한다"는 지역성 원리와 "장애를 당연시하는 [[136_variance|분산]] 처리" 사상은 현대 클라우드 아키텍처의 유전자로 깊이 각인되어 있습니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: [[136_variance|분산]] 컴퓨팅, [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]])
- **핵심 단계**: 맵(Map), 셔플(Shuffle), 리듀스(Reduce)
- **대안 기술**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], [[028_apache_tez|Apache Tez]], [[215_flink_native_stream_watermark_window_time|Apache Flink]]

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 서버 한계]
    │
    ▼
[분산 처리 필요]
    │
    ▼
[MapReduce(Map 단계)]
    │
    ▼
[Shuffle/Sort]
    │
    ▼
[Reduce 단계 → Hadoop 에코시스템]
```

MapReduce는 단일 서버 한계를 넘어 Map, Shuffle/Sort, Reduce로 [[136_variance|분산]] 처리를 수행한다.

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 운동장에 흩어진 1만 개의 공을 색깔별로 세어야 한다고 해봐요.
2. [[018_mapreduce|맵리듀스]]는 전교생에게 운동장에 나가서 "각자 앞에 있는 공들만 세어와!(Map)"라고 시키는 거예요.
3. 그런 다음 반장들이 각 색깔별 숫자를 다 더해서(Reduce) 최종 숫자를 알아내는 아주 빠른 방법이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 262

← **이전**: [[030_rack_awareness_fault_tolerance_topology|08. 랙 인지 (Rack Awareness) - 물리적 장애 격리를 위한 데이터 복제 전략]]
**다음**: [[032_map_function_key_value_output|Map 함수: MapReduce 분산 처리의 시작]] →

---
