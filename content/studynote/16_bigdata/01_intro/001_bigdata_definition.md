---
title: '1. 빅데이터 정의 — 3V: Volume(양) / Velocity(속도) / Variety(다양성) (Laney, 2001)'
date: '2026-03-26'
tags:
- studynote-bigdata
---

> **핵심 인사이트**
> 1. **본질**: 단일 컴퓨터의 물리적 한계를 초월하는 막대한 규모, 속도, 다양성을 지닌 [[001_dikw_pyramid|데이터]]를 수천 대의 범용 서버 클러스터에서 [[136_variance|분산]] [[430_index_fast_full_scan|병렬]] 처리하는 패러다임.
> 2. **가치**: 기존 RDBMS로는 불가능했던 전수 [[001_dikw_pyramid|데이터]] 분석을 가능케 하여 [[001_dikw_pyramid|데이터]] 기반 의사결정과 [[241_machine_learning_basics|머신러닝]] 예측 모델의 기반이 됨.
> 3. **융합**: [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 디스크 기반 [[228_batch_processing_hadoop_spark|배치 처리]]에서 스파크의 인메모리 연산, 실시간 스트리밍 [[031_에코_반향|에코]]시스템으로 진화 중.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 개념 정의

빅데이터 (Big [[001_dikw_pyramid|Data]])란 기존 [[003_dbms_database_management_system|데이터베이스 관리 시스템]]이 단일 장비 내에서 처리하기 어려운 규모의 [[001_dikw_pyramid|데이터]]를 지칭하는 용어다. 단순히 "큰 [[001_dikw_pyramid|데이터]]"를 넘어서, [[001_dikw_pyramid|데이터]]의 수집, 저장, 분석, 활용 방법 자체에 대한 근본적 패러다임 전환을 의미한다. 2001년 더글라스 래니 (Douglas Laney)가 제시한 3V 모델이 빅데이터의 공식적 정의로 널리 통용되고 있으며, 이후 기업들은 이를 확장하여 5V, 7V 모델을 제시하며 개념을 재정립했다.

빅데이터가 필요하게 된 근본적 이유는 두 가지로 귀결된다. 첫째, 인터넷 보급과 모바일 기기 폭발적 증가로 인해 매일 수십 페타바이트 (PB)规模的 [[001_dikw_pyramid|데이터]]가 [[087_process_state_transition|생성]]되고 있다. 인간이 수동으로 처리할 수 없는 양을 기계가 자동화해야 하는 상황이 됐다. 둘째, 기업 경쟁력의 핵심이 직관에서 [[001_dikw_pyramid|데이터]]로 이동하면서, 과거에는 버려졌던 [[004_unstructured_data|비정형 데이터]] (웹 [[568_logs_distributed_logging_elk_fluentd|로그]], SNS 텍스트, 센서 [[001_dikw_pyramid|데이터]] 등)조차 분석 대상으로 부상했다.

### 등장 배경 및 발전 과정

[[459_quic_fec_forward_error_correction|초기]] 기업들은 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]] (RDBMS)의 엄격한 [[005_schema|스키마]] ([[010_schema_on_write|Schema-on-Write]])에 맞지 않는 [[001_dikw_pyramid|데이터]]를 모두 폐기해야 했다. 그러나 2000년대 중반, 구글 (Google)이 발표한 GFS (Google [[501_file_definition_logical_record|File]] System)와 [[018_mapreduce|MapReduce]] 논문이 이 한계를 극적으로 바꿨다. 비싸고 고장 안 나는 슈퍼컴퓨터 대신, 싸고 흔한 범용 서버 (Commodity Hardware) 수천 대를 네트워크로 묶어 [[001_dikw_pyramid|데이터]]를 [[136_variance|분산]] 저장하고 연산하는 방식이 탄생했다.

이 아키텍처의 핵심 발상은 [[001_dikw_pyramid|데이터]]가 있는 곳으로 [[159_opcode|연산 코드]]를 보내라는 것이다. 네트워크를 통해 거대한 [[001_dikw_pyramid|데이터]]를 이동시키는 것은 너무 느리기 때문에, 연산을 [[001_dikw_pyramid|데이터]] 존재 위치로 [[136_variance|분산]]시키는 것이 핵심 설계 원칙이다. 이것을 [[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]]) 원칙이라고 하며, 빅데이터 [[136_variance|분산]] 처리 시스템의 근간이 된다.

빅데이터의 역사는 세대로 구분할 수 있다. 1세대 (2000년대 중반)는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]])의 등장으로 특징지어지며, [[228_batch_processing_hadoop_spark|배치 처리]]와 스토리지 중심이었다. 2세대 (2010년대 초중반)는 스파크 ([[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]])의 등장으로 인메모리 연산이 가능해져 반복적 기계학습 [[001_algorithm_definition|알고리즘]]의 속도가 급격히 향상됐다. 3세대 (2010년대 후반~현재)는 [[179_kafka_flink_watermark_time_window|카프카]] ([[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]])와 플링크 ([[215_flink_native_stream_watermark_window_time|Apache Flink]]) 기반 실시간 스트리밍이 보편화되면서 초단위 분석이 가능해졌고, 현재는 [[190_ai_llm_requirements_specification|AI]] [[582_llm_based_code_generation_tools|대규모 언어 모델]] ([[263_llm_large_language_model|LLM]])의 학습 [[001_dikw_pyramid|데이터]] 소스로 그 활용 범위가 더욱 확대되고 있다.

### 3V 모델의 이해

빅데이터의 핵심 특성을 설명하는 3V 모델은 다음과 같이 구성된다.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    빅데이터 3V 모델 구조                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Volume: 규모]              [Velocity: 속도]                  │
│   ┌─────────────────┐          ┌─────────────────┐               │
│   │ 수십 페타바이트 │          │ 초당 수백만 건  │               │
│   │ ~ 제타바이트   │          │ 이벤트 생성     │               │
│   │ 단위 데이터    │          │ 처리           │               │
│   └─────────────────┘          └─────────────────┘               │
│                                                                 │
│                    [Variety: 다양성]                             │
│          ┌─────────────────────────────────────┐                │
│          │  비정형 데이터     반정형 데이터       │                │
│          │  ┌─────────┐    ┌─────────┐         │                │
│          │  │ SNS тек스트 │  │  JSON   │         │                │
│          │  │ 이미지    │    │  XML    │         │                │
│          │  │ 동영상    │    │  로그   │         │                │
│          │  │ 음성     │    │         │         │                │
│          │  └─────────┘    └─────────┘         │                │
│          │  + 정형 데이터 (RDBMS)               │                │
│          └─────────────────────────────────────┘                │
│                                                                 │
│   추가 V 확장:                                                   │
│   [Veracity: 진실성] → 데이터 품질, 신뢰성                         │
│   [Value: 가치]      → 분석을 통해 도출되는 비즈니스 가치           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 3V 모델에서 [[001_bigdata_3v_5v|Volume]] (규모)은 [[001_dikw_pyramid|데이터]] 양의 절대적 크기를 의미한다. 2010년대에 형성된 [[001_dikw_pyramid|데이터]]总量的 팽창 속도는 기하급수적이며, 매일 전 세계에서 [[087_process_state_transition|생성]]되는 [[001_dikw_pyramid|데이터]]양은 약 3.3자이트 (3.3ZB)에 달한다. Velocity (속도)는 [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]] 주기와 [[019_처리_지연|처리 지연]] 시간을 의미한다. 실시간 금융 거래, [[101_iot_concept|사물인터넷]] ([[101_iot_concept|IoT]]) 센서, 소셜 미디어 스트림은 초당 수백만 건의 이벤트를 쏟아내며, 전통적인 [[228_batch_processing_hadoop_spark|배치 처리]] 방식으로는 감당할 수 없는 흐름을 형성한다. Variety (다양성)는 [[001_dikw_pyramid|데이터]] 형태의 이질성을 의미한다. 구조화된 [[083_relationship_in_er_model|관계]]형 [[001_dikw_pyramid|데이터]]와 반정형 [[343_json|JSON]], 비정형 이미지·동영상·텍스트가 혼재하며, 이를 통합적으로 처리할 수 있는 유연한 [[005_schema|스키마]]-[[094_less_large_scale_scrum|less]] 접근이 필수적이다.

빅데이터의 3V 특성이 전통적 [[002_database_definition|데이터베이스]]의 용량 한계를 초월하게 되면서, 수십 대의 범용 서버를 클러스터로 구성하여 [[001_dikw_pyramid|데이터]]를 [[136_variance|분산]] 저장하고 [[430_index_fast_full_scan|병렬]]로 처리하는 [[136_variance|분산]] 컴퓨팅 아키텍처가 필수적으로 요구되었다. 마치 수영장에서 물 한 그릇을 퍼내는 것은 쉽지만, 바다의 물을 퍼내는 것은 배수구 시스템을 대규모로 배치해야 하는 것과 같은 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 표

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **[[136_variance|분산]] 스토리지** | 무한 [[001_dikw_pyramid|데이터]] [[196_durability_permanent_storage|영속성]] 보장 | [[001_dikw_pyramid|데이터]] 블록 분할 및 3중 [[016_replication_factor|복제]], [[014_namenode|네임노드]] 관리 | [[013_hdfs|HDFS]], Amazon S3, MinIO | 끝없이 확장되는 대형 창고 |
| **[[136_variance|분산]] 연산 엔진** | 페타바이트급 [[430_index_fast_full_scan|병렬]] 연산 | Map([[104_classification_analysis|분류]])과 Reduce(집계), [[310_audit|RDD]] 기반 인메모리 연산 | [[012_apache_hadoop|Apache Hadoop]], [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | 수만 명의 엑셀 계산 직원 |
| **리소스 매니저** | 클러스터 전체 [[041_resource_allocation|자원 할당]]调度 | 노드 상태 [[229_monitor|모니터]]링, 작업 [[208_schedule_history_transaction_execution_order|스케줄]]링, 장애 [[658_ir_recovery|복구]] | [[020_yarn|YARN]], Mesos, [[205_kubernetes_container_orchestration|Kubernetes]] | 공사现场的 물량 배분 감독관 |
| **[[001_dikw_pyramid|데이터]] 수집 계층** | 다양한 소스로부터 [[001_dikw_pyramid|데이터]] 수집 | 에이전트 기반 수집, [[389_mesh_topology|메시]]지 큐 [[454_buffering|버퍼링]] | Flume, Sqoop, [[179_kafka_flink_watermark_time_window|Kafka]] Connect | 공장 입구의 컨베이어 벨트 |
| **[[203_metadata_management|메타데이터 관리]]** | [[001_dikw_pyramid|데이터]] 위치 및 [[005_schema|스키마]] 관리 | [[061_namespace|네임스페이스]], 접근 권한, [[001_dikw_pyramid|데이터]] 계보 추적 | [[544_hive|Hive]] Metastore, Glue [[394_catalog_metadata|Catalog]] | 창고의 사서 시스템 |

### [[136_variance|분산]] 처리 아키텍처의 핵심 원리

빅데이터 시스템의 동작 원리를 이해하려면, 단일 컴퓨터에서 [[376_multicomputer|다중 컴퓨터]]로 [[001_dikw_pyramid|데이터]] 처리가 확장되는 과정에서 발생하는 근본적 변화를 이해해야 한다. Fred Brooks가 제시한 "달 월嘴上 달을 올리는 일은 [[136_variance|분산]] 시스템에서도 마찬가지로 어렵다"는 유명한 격언처럼, 단순히 장비 수를 늘리는 것만으로는 [[282_performance_tactics|성능]]이线性적으로 증가하지 않는다.

[[136_variance|분산]] 환경에서는 네트워크를 통한 통신, 노드 간 [[212_synchronization_mechanisms|동기화]], 부분적 장애 감내, [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 유지 등 단일 시스템에서는 존재하지 않는 복잡성이 추가된다. 따라서 빅데이터 아키텍처는 이러한 [[136_variance|분산]] 환경의 복잡성을 [[198_abstraction_control_data_process|추상화]]하여 개발자에게 단일 시스템과 유사한 프로그래밍 모델을 제공하는 것이 핵심 목표다.

```text
┌─────────────────────────────────────────────────────────────────┐
│              빅데이터 분산 처리 아키텍처 전체 흐름                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [데이터 소스 계층]                                              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ RDBMS  │ │  로그   │ │  SNS   │ │ 센서   │               │
│  │  기존   │ │  파일   │ │ 스트림  │ │ IoT    │               │
│  │ 데이터  │ │         │ │         │ │        │               │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘               │
│       │           │           │           │                      │
│       ▼           ▼           ▼           ▼                      │
│  [데이터 수집: Flume / Sqoop / Kafka Connect]                    │
│                         │                                         │
│                         ▼                                         │
│  [분산 스토리지: HDFS / S3 / MinIO]                              │
│       │                     │                    │                 │
│       ▼                     ▼                    ▼                │
│  ┌─────────┐          ┌─────────┐          ┌─────────┐            │
│  │ Datanode│          │ Datanode│          │ Datanode│            │
│  │ Block 1 │          │ Block 2 │          │ Block 3 │            │
│  │ 복제 3개│          │ 복제 3개│          │ 복제 3개│            │
│  └─────────┘          └─────────┘          └─────────┘            │
│       │                     │                    │                 │
│       └─────────────────────┼────────────────────┘                │
│                             ▼                                     │
│  [리소스 매니저: YARN / Mesos]                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────┐            │
│  │         분산 연산 엔진 (MapReduce / Spark)        │            │
│  │                                                 │            │
│  │   [Map Task 1] [Map Task 2] [Map Task 3] ...   │            │
│  │        │           │           │                │            │
│  │        └───────────┼───────────┘                │            │
│  │                    ▼                            │            │
│  │              [Shuffle & Sort]                  │            │
│  │                    │                            │            │
│  │        ┌───────────┼───────────┐                │            │
│  │        ▼           ▼           ▼                │            │
│  │   [Reduce 1] [Reduce 2] [Reduce 3] ...          │            │
│  └─────────────────────────────────────────────────┘            │
│                             │                                     │
│                             ▼                                     │
│                    [결과: HDFS / DB / BI]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 아키텍처에서 핵심은 [[001_dikw_pyramid|데이터]] 흐름이 [[008_단방향_반이중_전이중|단방향]]이 아니라 [[005_feedback_loop|피드백 루프]]를 형성한다는 점이다. [[001_dikw_pyramid|데이터]] 수집 계층에서 들어오는 [[001_dikw_pyramid|데이터]]는 [[136_variance|분산]] 스토리지에 먼저 저장되며, 연산 엔진은 이 스토리지에서 [[001_dikw_pyramid|데이터]]를 읽어 처리한다. 3중 [[016_replication_factor|복제]] (Triple [[016_replication_factor|Replication]]) 구조는 특정 노드 장애 시에도 [[001_dikw_pyramid|데이터]] 손실을 방지하며, 리소스 매니저가 클러스터 전체의 CPU와 메모리를 [[369_logic_bomb|논리]]적으로 분할하여 여러 작업에 동시에 할당한다. 특히 Shuffle 단계가 네트워크를 통해 [[001_dikw_pyramid|데이터]]를 재분배하므로, 이 구간이 가장 [[282_performance_tactics|성능]] 병목 구간이 되며 최적화의 핵심 초점이 된다. 실무에서는 이 흐름을 파악한 뒤 [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]]과 네트워크 [[140_bandwidth|대역폭]]을 먼저 튜닝하는 것이 일반적이다.

### [[019_data_locality|데이터 지역성]] 원리의 동작 과정

MapReduce의 가장 중요한 설계 원칙은 "[[001_dikw_pyramid|데이터]]를 연산 중심으로 이동시키지 말고, 연산을 [[383_data_centric_architecture|데이터 중심]]으로 이동시켜라"다. 수십 테라바이트의 [[001_dikw_pyramid|데이터]]를 네트워크로 전송하면 엄청난 [[140_bandwidth|대역폭]]이 필요하고 [[015_지연_데이터_관점|지연]]이 발생한다. 따라서 거대한 [[001_dikw_pyramid|데이터]]를 여러 블록으로 쪼개 각 [[001_dikw_pyramid|데이터]] 노드에 저장하고, 각 노드에서 로컬로 연산을 수행한 뒤 결과만 취합하는 방식이 핵심이다.

```text
┌─────────────────────────────────────────────────────────────────┐
│              데이터 지역성 (Data Locality) 동작 원리              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [네임노드 (NameNode) - 메타데이터 관리자]                         │
│       │                                                          │
│       │  ① job.submit() → 작업 요청                               │
│       │  ② 데이터 블록 위치 정보 반환 (Block Map)                  │
│       ▼                                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    연산 코어 로직                          │   │
│  │                                                          │   │
│  │   TaskTracker A          TaskTracker B        TaskTracker C│   │
│  │   ┌─────────────┐       ┌─────────────┐      ┌─────────────┐│   │
│  │   │ 로컬 블록 1 │       │ 로컬 블록 2 │      │ 로컬 블록 3 ││   │
│  │   │ apple:1     │       │ banana:1    │      │ cherry:1    ││   │
│  │   │ banana:1    │       │ apple:1     │      │ apple:1     ││   │
│  │   └─────────────┘       └─────────────┘      └─────────────┘│   │
│  │         │                    │                     │        │   │
│  │         └────────────────────┼─────────────────────┘        │   │
│  │                              ▼                               │   │
│  │                    [Shuffle: 네트워크 전송]                  │   │
│  │                              │                               │   │
│  │              ┌───────────────┼───────────────┐               │   │
│  │              ▼               ▼               ▼               │   │
│  │        ┌──────────┐    ┌──────────┐    ┌──────────┐           │   │
│  │        │ Reduce A │    │ Reduce B │    │ Reduce C │           │   │
│  │        │ apple:3  │    │banana:2  │    │ cherry:1 │           │   │
│  │        └──────────┘    └──────────┘    └──────────┘           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  핵심 이점: 3TB 데이터 처리 시 네트워크 전송량 3TB → 0 (로컬 연산) │
│  대역폭 절약: 전체 클러스터 병목 구간인 Shuffle 구간만 최적화     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[019_data_locality|데이터 지역성]]의 진가는 물리적 [[140_bandwidth|대역폭]] 비용 절약에서 드러난다. 3TB의 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]에서 단어 개수를 세는 Job을 생각해보면, [[001_dikw_pyramid|데이터]]를 전부 네트워크로 이동시키면 3TB의 WAN/LAN 트래픽이 발생한다. 그러나 블록 단위 [[136_variance|분산]] 저장 후 각 노드에서 Map 연산을 수행하면, 거대한 [[001_dikw_pyramid|데이터]]는 움직이지 않고 [[159_opcode|연산 코드]]만 각 노드에 배포된다. 오직 Map의 결과 (최종 결과보다 훨씬 작은 용량)만이 네트워크를 통해 Reduce 노드로 이동한다. 이것이 바로 구글과 야후가 수천 대의 싸구려 서버로 수 페타바이트를 처리할 수 있었던 핵심 설계 비결이다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 전통적 RDBMS vs 빅데이터 [[136_variance|분산]] 처리 비교

기존 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]와 현대 빅데이터 아키텍처는 근본적으로 다른 설계 철학을 따른다. RDBMS는 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) [[191_transaction_concept_states|트랜잭션]]을 엄격히 준수하는 대신 수평 확장에 어려움을 겪는다. 빅데이터는 이를 희생하고 대규모 [[430_index_fast_full_scan|병렬]] 처리와 고가용성을 우선시한다.

| 비교 항목 | 전통적 RDBMS | 빅데이터 [[136_variance|분산]] 시스템 | 실무 판단 포인트 |
|:---|:---|:---|:---|
| **확장 방식** | 스케일업 ([[621_scale_up_system_bus|Scale-up]]) - 단일 장비 강화 | 스케일아웃 ([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) - 장비 수 증가 | PB 단위 이상에서는 [[136_variance|분산]]이 필수 |
| **[[014_data_model_components|데이터 모델]]** | 고정 [[005_schema|스키마]] ([[010_schema_on_write|Schema-on-Write]]) | 유연한 [[005_schema|스키마]] ([[009_schema_on_read|Schema-on-Read]]) | 다양한 [[001_dikw_pyramid|데이터]] 소스 활용 시 빅데이터 우위 |
| **[[194_consistency_database_integrity|일관성]]** | 강일관성 (Strong [[194_consistency_database_integrity|Consistency]]) | 최종 [[194_consistency_database_integrity|일관성]] ([[650_eventual_consistency|Eventual Consistency]]) | 금융 거래 등 정밀성 필요 시 RDBMS |
| **[[191_transaction_concept_states|트랜잭션]]** | ACID 완전 지원 | 제한적 지원 또는 미지원 | 복잡한 조인 [[191_transaction_concept_states|트랜잭션]]은 RDBMS |
| **[[298_qkv_attention|쿼리]] 언어** | SQL (표준화) | SQL 호환 또는 전용 언어 | BI 도구 연동 시 SQL 지원 여부 [[396_validation|확인]] |
| **[[352_defect_definition|결함]] 감내** | [[454_spof|단일 장애점]] ([[454_spof|SPOF]]) 위험 | 노드 장애 시 자동 [[658_ir_recovery|복구]] | 24/7 [[090_service_kubernetes_network_load_balancing|서비스]]에는 [[136_variance|분산]] 시스템 필수 |
| **활용 비용** | 전용 고가 하드웨어 | 범용 서버 클러스터 | [[459_quic_fec_forward_error_correction|초기]] 구축 비용은 낮지만 운영 복잡도 높음 |

RDBMS와 빅데이터는 상호 배타적이지 않다. 실제로 대부분의 기업 환경에서는 두 시스템을 함께 사용한다. 핵심 비즈니스 [[191_transaction_concept_states|트랜잭션]]은 RDBMS에서 처리하고, 분석을 위한 대규모 [[001_dikw_pyramid|데이터]] 처리는 빅데이터 시스템에서 수행하는 하이브리드 접근이 일반적이다.

### 대용량 [[001_dikw_pyramid|데이터]] 처리 엔진 발전 비교

```text
┌─────────────────────────────────────────────────────────────────┐
│         데이터 처리 엔진 발전 과정: Hadoop MR → Spark → Flink      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1세대: Hadoop MapReduce]                                       │
│  ┌─────────────────────────────────────────────────┐           │
│  │  디스크 I/O 바쁜 배치 처리                        │           │
│  │                                                 │           │
│  │  Map → [Disk Write] → Shuffle → [Disk Read] → Reduce     │   │
│  │                     │                              │           │
│  │              네트워크 + 디스크 병목                   │           │
│  └─────────────────────────────────────────────────┘           │
│  특징: 내구성 높음, 확장성优异, 반복処理에 비효율                   │
│                                                                 │
│  [2세대: Apache Spark]                                          │
│  ┌─────────────────────────────────────────────────┐           │
│  │  인메모리 기반의 고속 반복 처리                    │           │
│  │                                                 │           │
│  │  Map → [Memory] → Shuffle → [Memory] → Reduce            │   │
│  │            │                    │                         │   │
│  │       RDD 캐싱           캐시된 데이터 재사용              │           │
│  └─────────────────────────────────────────────────┘           │
│  특징: MapReduce 대비 10~100배高速, ML/반복 알고리즘 최적화       │
│                                                                 │
│  [3세대: Apache Flink]                                          │
│  ┌─────────────────────────────────────────────────┐           │
│  │ ネイティブ 스트리밍 + 배치 통합                      │           │
│  │                                                 │           │
│  │  [Event Stream] → Process → [State] → Output              │   │
│  │       │                                         │           │
│  │  Event-Time 윈도우       정확히 한 번 (Exactly-once) 처리  │   │
│  └─────────────────────────────────────────────────┘           │
│  특징: 진정한 실시간 처리, 지연 시간 밀리초 단위                    │
│                                                                 │
│  선택 기준:                                                      │
│  - 일별 배치 처리: Hadoop MR (安定的, 보간)                       │
│  - 대화형 분석: Spark (高速, SQL 지원)                           │
│  - 순수 실시간: Flink (낮은 지연, 정확한 결과)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 각 세대의 처리 엔진은 이전 세대의 한계를 극복하는 방향으로 진화했다. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] MapReduce는 디스크 기반 처리로 내구성은 높지만, 동일한 [[001_dikw_pyramid|데이터]]를 반복 연산하는 기계학습 (Machine [[240_switch_learning_forwarding_flooding|Learning]]) 워크로드에서는 디스크 읽기/[[289_cqrs_db|쓰기]] 오버헤드가 심각한 병목이 됐다. Spark는 [[310_audit|RDD]] ([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]])를 통해 메모리에 중간 결과를 [[456_caching|캐싱]]하여 이 문제를 해결했지만, 여전히 Micro-batch 기반이라 진정한 의미의 실시간에는 한계가 있다. Flink는 스트림 우선 ([[467_http2_stream_multiplexing_tcp_hol|Stream]]-first) 아키텍처로 이 문제를 근본적으로 해결하며, Event-Time 윈도우와 상태 관리 기능을 내장하여 스트리밍 처리에서 가장 진보한 엔진으로 평가받는다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

### 실무 시나리오

**시나리오 1: 이커머스平台的 일별 매출 분석 배치 잡 (Batch Job) 설계**

대규모 이커머스 플랫폼에서 매일 새벽에 실행되는 일별 매출 집계 잡은 수백만 건의 주문 [[001_dikw_pyramid|데이터]]를 처리해야 한다. 이때 고려해야 할 기술적 판단은 다음과 같다.

첫째, [[001_dikw_pyramid|데이터]] [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]]이다. 주문 [[001_dikw_pyramid|데이터]]를 날짜별로 [[179_table_partitioning_concept|파티셔닝]]하면 특정 날짜 범위 [[298_qkv_attention|쿼리]] 시 스캔 범위를 극적으로 줄일 수 있다. 그러나 시간대별 분석이 필요한 경우 시간 단위 [[179_table_partitioning_concept|파티셔닝]]이 유리하다. 둘째, 셔플 비용 최적화다. 집계 과정에서 발생하는 네트워크 [[001_dikw_pyramid|데이터]] 전송량을 줄이기 위해, 가능한 한 Map 쪽에서 부분 집계를 수행하는 Combiner 함수를 활용해야 한다. 셋째, 장애 [[658_ir_recovery|복구]] 메커니즘이다. 8시간 걸리는 잡이 7시간 50분에서 실패할 경우, 전체를 다시 시작하면 엄청난 비용이 발생한다. 따라서 Checkpoint를 [[009_config|설정]]하여 실패 지점부터 재시작할 수 있는 설계가 필수적이다.

**시나리오 2: 금융권 실시간 사기 거래 탐지 (Fraud [[961_deepfake_detection|Detection]]) 시스템**

신용카드 도용 거래를传统的 배치 분석으로 탐지하면 다음 날 아침에나 결과를 받을 수 있다. 수백억 원의 잠재적 피해를 막기 위해서는 초단위 실시간 분석이 필수적이다. 이 경우 Apache Kafka로 결제 이벤트를 실시간 수집하고, Apache Flink로 최근 5분 윈도우 내 의심 패턴을 탐지하며, 결과를 [[542_redis|Redis]] [[139_inmemory_db|인메모리 데이터베이스]]에 저장하여 승인 서버가 실시간 차단 판단을 내릴 수 있도록 설계해야 한다.

[[009_real_time_system|실시간 시스템]] 설계 시 가장 중요한 판단은 [[019_처리_지연|처리 지연]] ([[141_latency|Latency]]), [[139_throughput|처리량]] ([[139_throughput|Throughput]]), 결과 [[002_bigdata_5v|정확성]] (Accuracy) 사이의 트레이드오프다. 마이크로 배치 (Micro-batch) 방식은 [[139_throughput|처리량]]이 높지만 [[015_지연_데이터_관점|지연]]이 상대적으로 크고, 네이티브 스트리밍 방식은 [[015_지연_데이터_관점|지연]]이 낮지만 [[139_throughput|처리량]]이 낮을 수 있다.

```text
┌─────────────────────────────────────────────────────────────────┐
│           실시간 사기 거래 탐지 아키텍처 의사결정 트리              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [결제 이벤트 발생]                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐   카드사 API        ┌─────────────┐           │
│  │  Kafka Topic │ ───────────────▶ │  승인 서버   │           │
│  │  (결제 이벤트) │                    │             │           │
│  └──────┬──────┘                    └──────▲──────┘           │
│         │                                  │                   │
│         ▼                                  │                   │
│  ┌─────────────┐                    ┌─────┴─────┐            │
│  │ Flink 스트리밍│ ──── Redis ────▶ │ 실시간 차단 │            │
│  │  5분 윈도우   │   (의심 점수)      │  판단       │            │
│  └─────────────┘                    └────────────┘            │
│                                                                 │
│  의사결정 체크리스트:                                             │
│  ├─ 지연 요구사항: < 100ms → Native Streaming (Flink)           │
│  ├─ 처리량 요구사항: > 10만 TPS → Kafka + Micro-batch (Spark)   │
│  ├─ 정확성 요구사항: 재현 가능성 필요 → Checkpoint 필수          │
│  └─ 운영 복잡도: 팀 역량 + 유지보수 편의성 고려                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 아키텍처에서 핵심은 승인 서버와 분석 시스템이 완전히 분리되어 있다는 점이다. 승인 서버는 금융 [[191_transaction_concept_states|트랜잭션]]의 본務 책임이 있으므로, 분석 시스템의 부하가 직접적으로 승인レイテン시에 영향을 주면 안 된다. 따라서 Kafka를 통한 비동기 [[389_mesh_topology|메시]]지 큐 구조가 필수적이다. Flink는 [[272_state_pattern|State]] backend로 RocksDB를 사용하여 상태를 디스크에 영속화하므로, Flink 장애 시에도 상태 [[658_ir_recovery|복구]]가 가능하다. Redis는 순수 인메모리 KV 스토어로 읽기 [[282_performance_tactics|성능]]이 우수하여 승인 서버의 블로킹 없는高速 조회에 적합하다.

### 도입 [[435_checklist_based_testing|체크리스트]]

기술 도입 전 반드시 [[396_validation|확인]]해야 할 항목은 다음과 같다.

기술적 항목으로는 클러스터 규모 산정이 선행되어야 한다. 예상 [[001_dikw_pyramid|데이터]] 성장률을 고려하여 [[459_quic_fec_forward_error_correction|초기]] 노드 수와 [[249_scaling_normalization_standardization|스케일링]] [[164_policy|정책]]을 수립해야 하며, 네트워크 [[140_bandwidth|대역폭]]이 [[136_variance|분산]] 처리 병목 구간이 되므로 10Gbps 이상 [[238_switch_operation_principles|스위치]]를 배치하는 것이 일반적이다. [[019_data_locality|데이터 지역성]]을 극대화하기 위해 [[001_dikw_pyramid|데이터]] 노드와 연산 노드를 공존 ([[062_colocation_data_center_leasing|Colocation]])시키는 것이 효과적이다.

운영 및 보안 항목으로는 [[052_data_governance_framework|데이터 거버넌스]] [[164_policy|정책]]이 수립되어야 한다. PII (Personal Identifiable Information) [[001_dikw_pyramid|데이터]]의 수집, 저장, 처리, 폐기에 대한 Lifecycle 관리와 [[387_access_control_pattern|접근 통제]]가 필수적이다. 또한 [[791_gdpr_eu|GDPR]], [[783_pipa_korea|개인정보보호법]] 등 규제 요건에 대한 [[819_data_masking|데이터 마스킹]] 및 익명화 [[164_policy|정책]]이 동반되어야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**작은 [[501_file_definition_logical_record|파일]]의 저주 (Small Files Problem)** 는 [[211_hadoop_ecosystem_mapreduce|하둡 에코시스템]]에서 가장 흔한 [[282_performance_tactics|성능]] 저하 원인이다. 수 KB 크기의 [[501_file_definition_logical_record|파일]] 수백만 개가 HDFS에 저장되면, 각 [[501_file_definition_logical_record|파일]]이 하나의 블록으로 취급되어 [[014_namenode|네임노드]]의 메모리가 고갈된다. 또한 스파크가 수백만 개의 [[150_task|태스크]]를 [[087_process_state_transition|생성]]하여 [[150_task|태스크]] [[208_schedule_history_transaction_execution_order|스케줄]]링 오버헤드가 실제 연산 시간보다 커지는 역설적 상황이 발생한다. 해결책은 [[001_dikw_pyramid|데이터]] 수집 단계에서 마이크로 배치를 적절한 크기 (128MB 이상)로 병합하는 것이다.

**정 반대 극단: 과도한 테스크 [[430_index_fast_full_scan|병렬]]화** 도 [[128_water_scrum_fall_anti_pattern|안티패턴]]이다. 수백만 개의 [[514_partition_slice_volume|파티션]]을 [[087_process_state_transition|생성]]하면 셔플 오버헤드가 급증하고, JVM 스타트업 오버헤드와 [[149_serial_communication_rs232_rs485|직렬]]화 비용이 전체 처리 시간을 증가시킨다. 일반적으로 [[514_partition_slice_volume|파티션]]당 100MB~1GB 정도가 적정 규모다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적 효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 처리 규모** | 단일 DB 10TB 한계 | 클러스터 스케일아웃 수 PB 처리 | **100배+ 확장** |
| **[[228_batch_processing_hadoop_spark|배치 처리]] 시간** | 야간 배치 8시간 | Spark 인메모리 10분 | **48배 단축** |
| **분석 대시보드 [[015_지연_데이터_관점|지연]]** | D+1 (24시간 후) | 실시간 (1초 이내) | **[[015_지연_데이터_관점|지연]] 99% 감소** |
| **스토리지 비용** | 전량 [[493_san_storage_area_network|SAN]] 스토리지 | 对象 스토리지 + [[208_data_lake_schema_on_read|데이터 레이크]] | **70% 비용 절감** |

### 미래 전망

빅데이터의 미래는 세 가지 방향으로 진화하고 있다.

첫째, [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]]) 아키텍처의 보편화다. [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Databricks와 같은 [[531_cloud_native_architecture|클라우드 네이티브]] 빅데이터 플랫폼은 인프라 관리 부담을 크게 줄이고, 사용량은 실제 컴퓨팅 자원에 기반한 과금으로 비용 효율성을 높인다. 개발자는 [[645_data_pipeline_acceleration|데이터 파이프라인]] 작성에 집중하고, 클러스터 [[528_provisioning|provisioning]], 노드 관리, 소프트웨어 패치는 플랫폼이 자동 처리한다.

둘째, [[190_ai_llm_requirements_specification|AI]] [[582_llm_based_code_generation_tools|대규모 언어 모델]] ([[263_llm_large_language_model|LLM]])과의 융합加速다. LLM의 학습과 추론에는 정제된 대규모 텍스트 [[001_dikw_pyramid|데이터]]가 필수적이며, 이는 빅데이터 인프라와 직접 연결된다. [[276_fine_tuning|RAG]] ([[585_rag_retrieval_augmented_generation|Retrieval-Augmented Generation]]) 아키텍처에서는 [[223_vector_database_embedding|벡터 데이터베이스]] ([[223_vector_database_embedding|Vector Database]])가 핵심 역할을 하며, 이는 전통적 빅데이터 기술과 차별화된 새로운 기술 영역이다.

셋째, 실시간性与 정밀性の 동시 달성이 핵심 과제로 부상하고 있다. [[235_kappa|Kappa]] 아키텍처가 대세로 자리 잡으며 배치와 스트리밍의 경계가模糊되고, 모든 [[001_dikw_pyramid|데이터]] 처리가 스트림으로 통합되는 방향으로 진화하고 있다.

### 참고 표준

- ISO/IEC 20546: [[177_bigdata_reference_architecture|빅데이터 참조 아키텍처]] ([[177_bigdata_reference_architecture|Big Data Reference Architecture]], BDRA) 및 프레임워크 국제 표준
- Apache Software Foundation: 실질적인 빅데이터 [[191_oss_license_compliance|오픈소스]] 생태계의 표준화 기구
- NIST [[166_sp|SP]] 1500: 미국国家标准기술연구소 (NIST)의 빅데이터 프레임워크

---

## 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

- `[분산 시스템]`: 빅데이터의根基로, 수천 대의 서버를单一 클러스터로 묶는 네트워크 및 [[212_synchronization_mechanisms|동기화]] 기술
- `[병렬 처리 알고리즘]`: [[018_mapreduce|MapReduce]], [[401_bayesian_network_dag_causality|DAG]] 실행 모델 등 [[136_variance|분산]] 환경에서의 연산 최적화 기법
- `[데이터 엔지니어링 파이프라인]`: [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] [[073_container_orchestration_tools|오케스트레이션]], [[001_dikw_pyramid|데이터]] 품질 관리, [[012_metadata|메타데이터]] 체계
- `[클라우드 네이티브 아키텍처]`: [[561_container_based_deployment|컨테이너]], [[073_container_orchestration_tools|오케스트레이션]], [[206_serverless_cold_start|서버리스]]를 활용한 탄력적 빅데이터 인프라
- `[머신러닝 시스템]`: 정제된 빅데이터를 입력으로 받아 예측 모델을 학습하고 배포하는 종단간 [[123_pipe|파이프]]라인

---

### 📈 관련 키워드 및 발전 흐름도

```text
[3V]
    │
    ▼
[5V/7V]
    │
    ▼
[Hadoop/MapReduce]
    │
    ▼
[Spark/Flink]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 빅데이터는 **엄청나게 큰 모래사장** 같은 거예요. 금(金)을 찾으려면 모래 한 알 한 알 살펴봐야 하는데, 혼자 하면 1년이고 걸리잖아요. 그래서 수천 명의 친구들을 모래사장에 동시에 보내서 각자 구역을 나눠 빠르게 찾는 것과 같아요.

2. 3V는 모래사장에서 금을 찾는游戏的 규칙이에요. **규모 ([[001_bigdata_3v_5v|Volume]])** 는 모래가 엄청 많은 것, **속도 (Velocity)** 는 금을 빨리 찾아야 하는 것, **다양성 (Variety)** 은 모래뿐 아니라 조약돌, 진주, 보석도 같이 섞여 있는 것이에요.

3. 빅데이터 시스템은 **자동화 물류 창고**와 같아요. 물건 ([[001_dikw_pyramid|데이터]])이 들어오면 로봇 (연산 엔진)이 알아서 [[104_classification_analysis|분류]]하고, 고객이 필요할 때 가장 빠른 경로로 배달해 주는 거예요. 창고 관리자는 로봇들이 잘하고 있는지 감시만 하면 됩니다!
