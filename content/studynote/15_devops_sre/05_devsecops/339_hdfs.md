+++
title = "339. Hadoop HDFS MapReduce Spark 빅데이터 분산 처리 (Hadoop HDFS MapReduce vs Spark RDD In-Memory Processing)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Hadoop은 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop Distributed File System](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/))와 MapReduce를 결합한 [빅데이터 분산 처리 프레임워크](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/298_distributed_processing_framework_mapreduce_spark/)다. 수십~수천 노드에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 곳에서 연산을 수행하는 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)) 원칙으로 네트워크 부하를 최소화한다.
> 2. **Spark의 등장**: [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) MapReduce는 모든 중간 결과를 디스크에 기록해 반복 처리가 느리다. Spark는 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/), 탄력적 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋)를 메모리에 유지해 반복 처리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 MapReduce보다 100배 빠르다.
> 3. **판단 포인트**: HDFS는 대용량 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)에 적합하고, 실시간 스트리밍에는 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 또는 Flink가 더 적합하다. 분석 워크로드는 Spark, SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 중심은 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)/Presto/Trino를 선택한다.

---

## Ⅰ. 개요 및 필요성

2000년대 초 구글이 PageRank 계산을 위해 수천 대 서버로 웹 전체를 처리하는 기술이 필요했다. 구글의 GFS (Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System)와 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 논문이 그 해법이었고, 이를 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)로 구현한 것이 Hadoop이다.

Hadoop은 값싼 상용 서버(commodity hardware) + 소프트웨어 중복으로 고가 슈퍼컴퓨터 없이 페타바이트 규모의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리한다. 장애는 예외가 아니라 정상 상태로 가정하고 소프트웨어 수준에서 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)한다.

> 📢 **섹션 요약 비유**: Hadoop은 고성능 단일 컴퓨터(슈퍼컴퓨터) 대신, 수백 명의 사람(노드)이 분업해 큰 일을 처리하는 협업 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+---------------------------------------------------------+
|              HDFS + MapReduce vs Spark 흐름              |
+---------------------------------------------------------+
|                                                         |
|  [HDFS 저장 구조]                                        |
|  NameNode (메타데이터)                                   |
|       |  파일 위치, 블록 정보                            |
|       v                                                 |
|  DataNode1  DataNode2  DataNode3  (각 64/128MB 블록)    |
|  (복제본 3개로 내결함성 보장)                             |
|                                                         |
|  [MapReduce vs Spark]                                   |
|                                                         |
|  MapReduce: Map -> Disk Write -> Shuffle -> Reduce      |
|  (중간 결과 항상 HDFS에 기록, 느리지만 안정)              |
|                                                         |
|  Spark: Map -> RDD (메모리) -> Reduce                   |
|  (중간 결과 메모리 유지, 반복 처리 100x 빠름)             |
|                                                         |
+---------------------------------------------------------+
```

| 항목 | [Hadoop MapReduce](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/395_hadoop_mapreduce_disk_bottleneck/) | [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) |
|:---|:---|:---|
| 중간 결과 저장 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) (디스크) | 메모리 ([RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/)) |
| 반복 처리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 느림 | 100x 빠름 |
| 스트리밍 지원 | 미흡 | [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 지원 |
| ML 통합 | 제한적 | [Spark MLlib](/knowledge-base/studynote/16_bigdata/03_spark/062_spark_mllib/) |
| 오류 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 체크포인트 (디스크) | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 리니지 재계산 |

[RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)): Spark의 핵심 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)로 탄력적(Resilient) + [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)(Distributed) + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이다. 불변([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/))하고, 노드 장애 시 리니지(Lineage, 변환 이력)를 통해 재계산으로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)된다.

> 📢 **섹션 요약 비유**: MapReduce는 중간 계산 결과를 항상 칠판(디스크)에 적는 것이고, Spark는 머릿속(메모리)에서 계산하다가 최종 결과만 기록한다. 머릿속 계산이 훨씬 빠르다.

---

## Ⅲ. 비교 및 연결

| 기술 | 주 용도 | 특징 |
|:---|:---|:---|
| [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장 | 대용량, 순차 읽기 최적화 |
| [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) | 디스크 기반, 안정적 |
| Spark | 배치+스트리밍+ML | 메모리 기반, 빠름 |
| [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) | SQL on [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), HQL |
| Presto/Trino | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 멀티 소스 통합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | 스트림 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 소스 |

[YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) ([Yet Another Resource Negotiator](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/)): Hadoop의 클러스터 자원 관리자로 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), Spark 등 다양한 처리 엔진이 [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) 위에서 자원을 할당받아 실행된다.

> 📢 **섹션 요약 비유**: YARN은 건물 관리자다. 각 입주 회사([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), Spark)가 사무실(자원)을 요청하면 공평하게 배분한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 아키텍처 선택 기준

- **배치 대용량 처리**: Spark on [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) 또는 Spark on [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)
- **실시간 스트리밍**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 또는 [Apache Flink](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/)
- **대화형 SQL 분석**: Presto/Trino (다중 소스), [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) ([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 전용)
- **ML/[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인**: [Spark MLlib](/knowledge-base/studynote/16_bigdata/03_spark/062_spark_mllib/) + [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/)

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수가 3으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 내결함성이 보장되는가?
2. Spark 작업의 메모리 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 최적화되어 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 없이 실행되는가?
3. 오래된 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 작업이 Spark으로 마이그레이션되어 처리 속도가 개선되었는가?

> 📢 **섹션 요약 비유**: 배치는 트럭 운송(대용량, 계획적), 스트리밍은 택배(실시간, 소규모). 화물 종류에 맞는 운송 방법을 선택해야 효율적이다.

---

## Ⅴ. 기대효과 및 결론

[Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark 기반 빅데이터 플랫폼은 페타바이트 규모의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 상용 서버로 처리하는 비용 효율성을 제공한다. Spark의 인메모리 처리로 기계학습 훈련, 반복 분석의 처리 시간이 대폭 단축된다.

현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼의 트렌드는 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lakehouse다. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/), S3)의 유연성과 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 결합한 [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/), [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) 등이 그 구현체다.

> 📢 **섹션 요약 비유**: Hadoop은 큰 도서관([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장)과 도서관 사서 시스템([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리)이다. Spark은 사서가 책을 찾을 때 매번 서가로 가는 대신 이미 외운 내용(메모리)으로 바로 답하는 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop Distributed File System](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장, 블록 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/), 디스크 기반 |
| [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)) | Spark 핵심 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/), 메모리 기반 |
| [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) ([Yet Another Resource Negotiator](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/)) | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 자원 관리 |
| [Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) + 웨어하우스 통합 |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | 인메모리 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 프레임워크 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 서버 시대             Hadoop 시대               Spark + Cloud 시대
------------------   --------------------------   ------------------------
RDBMS 한계           ->  Hadoop HDFS + MapReduce  ->  Spark (메모리 처리)
단일 서버 스케일업         Google GFS/MapReduce 논문   Kafka + 스트리밍
페타바이트 불가            YARN 자원 관리               Delta Lake, Iceberg
                           Hive SQL on Hadoop           서버리스 Spark
```

### 👶 어린이를 위한 3줄 비유 설명

1. HDFS는 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 여러 컴퓨터에 나눠서 보관하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 도서관이에요. 책 하나가 망가져도 다른 복사본이 있어서 괜찮아요.
2. MapReduce는 도서관의 모든 책을 수백 명이 동시에 읽고 결과를 모으는 방법이에요. 단, 메모를 매번 저장해서 느려요.
3. Spark는 메모를 머릿속에 기억하면서 작업해서 MapReduce보다 훨씬 빠르게 결과를 낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 339 / 373

← **이전**: [338. Platform Engineering IDP Golden Path 개발자 경험 (Platform Engineering Internal](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/338_process/)
**다음**: [340. 카프카 분산 메시지 스트리밍 (Apache Kafka Topic Partition Offset Consumer Group ISR](/knowledge-base/studynote/15_devops_sre/05_devsecops/340_pub_sub/) →

---
