+++
title = "Spark Shuffle 최적화 (Shuffle Optimization)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- 셔플(Shuffle)은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 재분배하는 과정으로, 네트워크 I/O와 디스크 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 유발하는 스파크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 최대 병목 구간이다.
- 적절한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쏠림(Skew) 해결, 그리고 AQE(Adaptive Query Execution) 활용이 셔플 최적화의 3대 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
- 셔플을 최소화하는 조인 방식(Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 등)을 선택하고 불필요한 `repartition`을 줄이는 것이 고성능 스파크 애플리케이션 설계의 관건이다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
스파크 연산은 셔플이 발생하지 않는 **Narrow Dependency**(map, filter)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 필수적인 **Wide Dependency**(groupBy, [join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))로 나뉜다. Wide Dependency 발생 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 로컬 디스크에 쓰여지고 네트워크를 통해 다른 노드로 전송되는데, 이 과정이 전체 실행 시간의 80% 이상을 차지할 수 있어 최적화가 필수적이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
스파크 셔플은 **Sort-based Shuffle** 방식을 기본으로 하며, 효율적인 리소스 활용을 위해 다양한 최적화 기술이 적용된다.

```text
[ Spark Shuffle Process / 스파크 셔플 프로세스 ]

  [ Stage 1: Map ]           [ Network / Disk ]          [ Stage 2: Reduce ]
  Partition A --(Shuffle Write)--> [ Local Disk ] --(Fetch)--> [ Partition X ]
  Partition B --(Shuffle Write)--> [ Local Disk ] --(Fetch)--> [ Partition Y ]
  Partition C --(Shuffle Write)--> [ Local Disk ] --(Fetch)--> [ Partition Z ]

1. Shuffle Write: Map tasks sort and write output to local disk files.
2. Shuffle Fetch: Reduce tasks read data from multiple remote nodes via HTTP.
3. Bottleneck: Heavy Disk I/O, Network Congestion, Memory Pressure.
```

- **AQE (Adaptive Query Execution):** 실행 중 수집된 통계를 바탕으로 셔플 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수를 자동으로 조절하거나, 셔플 조인을 브로드캐스트 조인으로 런타임에 변경한다.
- **Shuffle Partitions 관리:** `spark.sql.shuffle.partitions`의 기본값(200)을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모에 맞게 조정해야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 작으면 오버헤드가 크고, 너무 크면 [가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)(GC) 문제가 발생한다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Skew 해결:</strong> 특정 키에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 몰려 하나의 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)만 늦게 끝나는 현상을 방지하기 위해 [Salting](/knowledge-base/studynote/02_operating_system/10_security/605_password_salting_hash/)(키에 랜덤값 추가)이나 AQE [Skew Join](/knowledge-base/studynote/16_bigdata/03_spark/069_skew_join/) 최적화를 사용한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 최적화 기법 | 주요 내용 | 적용 효과 |
| :--- | :--- | :--- |
| <strong>Broadcast <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | 소규모 테이블을 모든 노드에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | **셔플 완전 제거**, 속도 대폭 향상 |
| **AQE (Coalescing)** | 너무 많은 작은 셔플 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 자동 병합 | 리소스 낭비 방지, [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링 효율화 |
| **Filter Pushdown** | 조인/셔플 전 미리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필터링 | 셔플 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송량 감소 |
| **Columnar Format** | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC 등 컬럼 기반 저장 | 필요한 컬럼만 셔플하여 I/O 감소 |
| **Serialization** | Kryo 등 고성능 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 도구 사용 | 네트워크 전송 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기 축소 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **기술사적 통찰:** 셔플 최적화는 단순히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 바꾸는 것이 아니라, [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링 단계부터 고려해야 한다. 자주 조인되는 테이블은 동일한 키로 미리 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)(Bucketing)해두면 셔플 자체를 회피(Shuffle Exchange Elimination)할 수 있다.
- **메모리 관리:** 셔플 과정에서 대량의 메모리가 소모되므로 `spark.memory.fraction` 조절을 통해 실행 메모리와 스토리지 메모리의 균형을 맞춰야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
스파크 3.0 이후 AQE의 등장으로 셔플 최적화의 많은 부분이 자동화되었지만, 여전히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성을 파악한 수동 튜닝은 고득점 분석의 핵심이다. 향후에는 외부 셔플 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(External Shuffle [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 넘어 스토리지와 컴퓨팅이 완전히 분리된 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 셔플 엔진으로 발전할 전망이다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝
- **핵심 기술:** AQE, Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Skew, Shuffle Partitions
- **연관 기술:** Wide Dependency, Narrow Dependency, Kryo Serialization


### 📈 관련 키워드 및 발전 흐름도

```text
[스파크 RDD 와이드 의존성 (Wide Dependency) — 셔플 발생 원인, 파티션 간 데이터 이동]
    │
    ▼
[셔플 (Shuffle) — groupBy·join 시 네트워크를 통한 데이터 재분배, 성능 병목의 핵심]
    │
    ▼
[AQE (Adaptive Query Execution) — 런타임 통계 기반 셔플 파티션 수 동적 최적화]
    │
    ▼
[브로드캐스트 조인 (Broadcast Join) — 작은 테이블을 모든 노드에 복제하여 셔플 전체 제거]
    │
    ▼
[데이터 스큐 처리 (Skew Handling) — 편향 파티션 분할·솔팅으로 불균형 셔플 해소]
```

이 흐름은 스파크에서 셔플이 와이드 의존성으로 발생하는 원리를 이해하고, AQE의 동적 최적화→브로드캐스트 조인으로 셔플 자체를 제거하거나 최소화하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐 처리로 불균형 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)까지 해소하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 여러 명의 요리사가 각자 재료를 썰다가, 요리를 완성하기 위해 재료를 서로 바꾸는 시간이에요.
- 재료를 옮기는 데 시간이 너무 오래 걸리면 요리가 늦어지니까, 최대한 재료 이동을 줄여야 해요.
- 처음부터 비슷한 재료끼리 모여서 요리를 시작하면 훨씬 빨리 끝낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 262

← **이전**: [스파크 런타임 아키텍처 (Executor / Driver / Cluster Manager)](/knowledge-base/studynote/16_bigdata/03_spark/065_spark_runtime_architecture/)
**다음**: [Spark 데이터 직렬화 (Data Serialization)](/knowledge-base/studynote/16_bigdata/03_spark/067_spark_data_serialization/) →

---
