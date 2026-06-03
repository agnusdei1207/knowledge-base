+++
title = "01. 아파치 하둡 (Apache Hadoop) - 분산 스토리지 및 처리"
date = "2026-03-04"
weight = 23
[extra]
categories = ["studynote-bigdata", "hadoop"]
+++

## 핵심 인사이트 (3줄 요약)
- **빅데이터의 시초**: [[012_apache_hadoop|아파치 하둡]]([[012_apache_hadoop|Apache Hadoop]])은 방대한 [[004_unstructured_data|비정형 데이터]]를 저가형 상용 서버(Commodity Hardware) 수백 대에 [[136_variance|분산]] 저장하고 [[430_index_fast_full_scan|병렬]] 처리하는 [[191_oss_license_compliance|오픈소스]] 자바 프레임워크입니다.
- **스토리지와 연산의 결합**: [[001_dikw_pyramid|데이터]] 저장을 담당하는 [[553_distributed_file_system|분산 파일 시스템]]([[013_hdfs|HDFS]])과 [[001_dikw_pyramid|데이터]]를 처리하는 [[430_index_fast_full_scan|병렬]] 연산 엔진([[018_mapreduce|MapReduce]])으로 구성되어 단일 거대 머신의 한계를 극복했습니다.
- **[[031_에코_반향|에코]]시스템의 중심**: [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 자체만으로는 속도의 한계(디스크 I/O 병목)가 있으나, 자원 관리자([[020_yarn|YARN]]) 위에서 스파크(Spark), 하이브([[544_hive|Hive]]) 등 다양한 [[385_third_party_cookie_deprecation_cdw|서드파티]] 엔진들을 돌리는 거대한 생태계의 [[001_operating_system_purpose|운영체제]] 역할을 수행합니다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
2000년대 초반 구글은 전 세계 웹페이지를 긁어모아 검색 엔진을 구축해야 했으나 기존 RDBMS와 고가의 스토리지로는 비용과 용량의 한계에 부딪혔습니다. 구글이 발표한 GFS([[553_distributed_file_system|분산 파일 시스템]])와 [[018_mapreduce|MapReduce]] 논문을 바탕으로, 더그 커팅(Doug Cutting)이 야후에서 개발을 주도해 [[191_oss_license_compliance|오픈소스]]화한 것이 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]입니다. 
빅데이터라는 단어를 세상에 각인시킨 일등 공신이며, 비싼 슈퍼컴퓨터 한 대를 사는 대신 싼 100대의 깡통 컴퓨터를 묶어 '[[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]([[202_scale_out_distributed_horizontal_expansion|Scale-out]])' 수평 확장의 표준 패러다임을 정립했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[843_hadoop_rack_awareness_data_replication_topology|하둡]] 2.0 이후 아키텍처는 스토리지, 연산, 자원 [[208_schedule_history_transaction_execution_order|스케줄]]링의 철저한 계층 분리를 달성했습니다.

```text
+-----------------------------------------------------------------+
|                      Apache Hadoop Ecosystem                    |
|                                                                 |
|  +--------------------+  +--------------------+  +-----------+  |
|  |   MapReduce (MR)   |  |   Apache Spark     |  |   Hive    |  |
|  | (Data Processing)  |  | (In-Memory Engine) |  | (SQL DW)  |  |
|  +---------+----------+  +---------+----------+  +-----+-----+  |
|            |                       |                   |        |
|  +---------v-----------------------v-------------------v-----+  |
|  |           YARN (Yet Another Resource Negotiator)          |  |
|  |                   (Resource Management)                   |  |
|  +---------------------------------+-------------------------+  |
|                                    |                            |
|  +---------------------------------v-------------------------+  |
|  |           HDFS (Hadoop Distributed File System)           |  |
|  |                   (Distributed Storage)                   |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
```

1. **[[013_hdfs|HDFS]] ([[203_hadoop_hdfs_block_replication_fault_tolerance|Hadoop Distributed File System]])**: [[001_dikw_pyramid|데이터]]를 128MB 블록 단위로 쪼개어 수많은 워커 노드에 3벌씩 [[016_replication_factor|복제]] 저장하여 디스크 고장에 대비한 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])을 달성합니다.
2. **[[020_yarn|YARN]] (자원 협상가)**: [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 클러스터 내 CPU와 메모리 자원을 누가 얼마나 쓸지 할당하고 통제하는 클러스터 [[001_operating_system_purpose|운영체제]] 역할을 합니다.
3. **[[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]])**: 방대한 [[001_dikw_pyramid|데이터]]를 [[172_maas_mobility_as_a_service|마스]]터 서버로 가져와서 연산하면 네트워크가 마비되므로, 반대로 '[[159_opcode|연산 코드]]'를 [[001_dikw_pyramid|데이터]]가 저장된 워커 노드로 전송하여 각자 자리에서 연산하는 혁신적 구조를 채택했습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 RDBMS ([[188_pl_sql_t_sql_procedural|Oracle]], MySQL) | [[843_hadoop_rack_awareness_data_replication_topology|하둡]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[013_hdfs|HDFS]] + [[018_mapreduce|MapReduce]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 구조** | [[002_structured_data|정형 데이터]] (Strict [[005_schema|스키마]] 요구, [[010_schema_on_write|Schema-on-Write]]) | 정형, 반정형, [[004_unstructured_data|비정형 데이터]] 무관 ([[009_schema_on_read|Schema-on-Read]]) |
| **하드웨어 아키텍처** | 고가의 [[621_scale_up_system_bus|스케일 업]]([[621_scale_up_system_bus|Scale-up]]) 서버 (CPU/RAM 집중 증설) | 저가형 x86 서버 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) (무한 수평 [[430_index_fast_full_scan|병렬]]) |
| **처리 특성** | 실시간 [[191_transaction_concept_states|트랜잭션]] (ACID 보장), [[327_hint_handoff|OLTP]] 고속 I/O | 방대한 [[001_dikw_pyramid|데이터]]의 배치(Batch) 처리 중심 로딩 시간 긺 |
| **장애 [[658_ir_recovery|복구]]** | 별도 [[555_backup_and_restore_strategy|백업]], [[016_replication_factor|복제]] 솔루션 필요 ([[483_raid_overview|RAID]] 의존도 높음) | 소프트웨어 단에서 3중 [[016_replication_factor|복제]]로 노드 고장 시 자동 우회 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **레거시화에 대한 판단**: 디스크 기반 반복 연산을 수행하는 [[018_mapreduce|맵리듀스]]([[018_mapreduce|MapReduce]])는 속도가 너무 느려 현재 실무에서 메모리 기반의 '스파크(Spark)'로 99% 대체되었습니다. 그러나 밑바탕을 지탱하는 스토리지 HDFS와 자원 관리자 YARN은 [[061_on_premise_legacy_infrastructure|온프레미스]] 빅데이터 클러스터의 중추로 여전히 굳건합니다.
- **아키텍처 진화 방향**: 기업들이 [[061_on_premise_legacy_infrastructure|온프레미스]] 장비 관리에 지치며 [[007_public_cloud|퍼블릭 클라우드]]의 관리형 [[090_service_kubernetes_network_load_balancing|서비스]](AWS EMR, GCP Dataproc)로 이전하거나, [[013_hdfs|HDFS]] 스토리지를 무한한 S3 객체 스토리지로 교체하여 '컴퓨팅과 스토리지의 분리'를 구현하는 모던 [[208_data_lake_schema_on_read|데이터 레이크]]로 전환하는 추세입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[843_hadoop_rack_awareness_data_replication_topology|하둡]]은 [[001_dikw_pyramid|데이터]] 처리 비용을 극적으로 낮춰 기업이 [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]]나 텍스트를 버리지 않고 모두 저장([[208_data_lake_schema_on_read|Data Lake]])하게 만들었으며, 이는 훗날 [[190_ai_llm_requirements_specification|AI]] 딥러닝 부흥을 위한 [[001_dikw_pyramid|데이터]] 자양분 축적으로 직결되었습니다. [[061_on_premise_legacy_infrastructure|온프레미스]] 빅데이터 플랫폼을 구축하고 이해하는 근본적인 핵심 뼈대로서 기술사와 [[001_dikw_pyramid|데이터]] 엔지니어에게 최우선 필수 지식입니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **선행 개념**: [[136_variance|분산]] 컴퓨팅, 빅데이터 3V, [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]
- **핵심 기술**: [[013_hdfs|HDFS]], [[018_mapreduce|MapReduce]], [[020_yarn|YARN]]
- **확장 및 응용**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], [[028_apache_hive|Apache Hive]], [[208_data_lake_schema_on_read|데이터 레이크]], AWS EMR

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS]
    │
    ▼
[MapReduce]
    │
    ▼
[YARN]
    │
    ▼
[Hive/Spark]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 세상의 모든 책을 도서관 사서 한 명이 전부 읽고 요약하려면 평생이 걸려도 모자랄 거예요. (기존 방식)
2. [[843_hadoop_rack_awareness_data_replication_topology|하둡]]은 만 명의 친구들을 한꺼번에 불러서 책을 몇 장씩 나눠주고, 각자 읽고 요약해오라고 시키는 방법이랍니다.
3. 중간에 한 친구가 아파서 집에 가더라도, 다른 친구에게 복사본을 줘서 대신 읽게 하니까 절대 실패하지 않아요!