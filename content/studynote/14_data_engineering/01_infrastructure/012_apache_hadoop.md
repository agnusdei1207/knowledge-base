+++
title = "12. 아파치 하둡 (Apache Hadoop) - 대용량 데이터 분산 저장 및 병렬 처리 자바 오픈소스 프레임워크"
description = "대용량 비정형 데이터를 저비용으로 분산 저장하고 병렬 처리하는 자바 기반 오픈소스 프레임워크의 코어 아키텍처"
date = 2023-10-24

[taxonomies]
tags = ["data_engineering"]

[extra]
tags = ["data_engineering"]
+++

# 아파치 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) (Apache [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 방대한 양의 정형·비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 거대한 클러스터에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/))하고, 이를 디스크 기반으로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))하는 자바 기반의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프레임워크이다.
> 2. **가치**: 값비싼 스토리지 대신 저가형 x86 서버 여러 대를 활용하여 페타바이트급 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)를 구축할 수 있게 함으로써, 빅데이터 생태계라는 거대한 산업을 탄생시켰다.
> 3. **융합**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)의 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 한계를 극복하기 위해 YARN과 같은 자원 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 도입했으며, 이후 스파크(Spark)나 하이브([Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)) 등 수많은 에코시스템이 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위에서 동작하게 되었다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

아파치 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) (Apache [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/))은 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 너무 커서 한 대의 컴퓨터에 담을 수도, 처리할 수도 없다'는 근본적인 물리적 한계를 타파하기 위해 등장한 혁명적인 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 플랫폼이다. 2000년대 초반 구글(Google)이 폭발하는 웹 문서 검색 인덱싱을 위해 발표한 'GFS(Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System)'와 '[MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)' 논문을 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 진영인 더그 커팅(Doug Cutting)이 자바로 구현하여 아파치 재단에 기증하면서 그 역사가 시작되었다.

기존의 전통적인 관계형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(RDBMS)나 고가의 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 어플라이언스는 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르게 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)하는 데는 탁월했으나, 기하급수적으로 늘어나는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 이미지, 텍스트 같은 비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하기에는 도입 비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/))이 천문학적으로 높았다. [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 저렴한 일반 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(Commodity Hardware)들을 네트워크로 묶어 거대한 가상 스토리지 풀(Pool)을 만들고, '장애는 필연적으로 발생한다'는 전제하에 스스로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))하는 획기적인 패러다임을 제시했다.

다음 도식은 단일 RDBMS의 한계에 부딪힌 기존 시스템이 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)이라는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 플랫폼으로 어떻게 아키텍처 패러다임을 전환했는지 그 배경을 시각화한다.

```text
[전통적 데이터 처리 시스템과 하둡 분산 시스템의 패러다임 변화]

[기존 방식 (Scale-up)]                [하둡 패러다임 (Scale-out)]
   고가 스토리지 + 고성능 CPU              저가형 x86 서버 수천 대 묶음
   ┌─────────┐                       ┌───┐ ┌───┐ ┌───┐ ┌───┐
   │ RDBMS   │   (데이터 병목 발생) => │ N1│ │ N2│ │ N3│ │ N4│ ...
   │ (단일)  │   ────────────────>   └───┘ └───┘ └───┘ └───┘
   └─────────┘                       (HDFS 기반 무한 분산 저장)
    - 엄격한 스키마 필요                - 스키마 온 리드 (Schema-on-Read)
    - 데이터 이동 비용 높음             - 데이터가 있는 곳으로 연산을 이동
```

이 그림의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하기 위해 거대한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 메모리나 연산 서버로 끌어오는([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Movement) 전통적 방식의 비효율을 꼬집는 데 있다. [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기가 수 테라바이트에 달할 때 네트워크를 통해 이를 전송하는 것은 불가능하다는 점을 인지하고, 대신 용량이 매우 작은 '[연산 코드](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/)([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))'를 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 이미 저장되어 있는 노드로 전송하여 실행시키는 이른바 '[데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))'이라는 핵심 철학을 바탕으로 설계되었다.

> 📢 **섹션 요약 비유**: 커다란 도서관에서 책을 사서 읽으려면 집으로 무겁게 들고 와야 하지만(기존 방식), [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 아예 독서실 책상을 도서관 각 책장 바로 옆에 두고 그 자리에서 읽고 요약하게 만드는([데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)) 천재적인 시스템입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.0 시절에는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/))과 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))만 존재했으나, 다양한 처리 엔진을 수용하기 위해 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.0부터는 클러스터의 자원을 총괄 관리하는 [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) (Yet Another Resource Negotiator)이 핵심 레이어로 편입되었다.

| 구성 요소 | 역할 | 내부 동작 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/">HDFS</a> (저장)</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 거대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 128MB 블록으로 쪼개 3벌씩 여러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)노드에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 보관 | [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/), [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) | 거대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 창고 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/">MapReduce</a> (연산)</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치(Batch) 처리 | Map(필터링/매핑) → Shuffle(정렬/[그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)) → Reduce(집계) 과정을 디스크 기반으로 수행 | Java [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 수만 명의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/">YARN</a> (자원 관리)</strong> | 클러스터 자원 스케줄링 | 전체 노드의 CPU/Memory 현황을 파악하여 각 애플리케이션(Spark, [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))에 자원 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 할당 | [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) | 인력 사무소 소장 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/">NameNode</a> (마스터)</strong> | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 중앙 관리 | 블록이 어느 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)노드에 있는지 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 구조와 매핑 테이블을 RAM에서 관리 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 창고 장부(목록) 관리자 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/">DataNode</a> (워커)</strong> | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 입출력 | 클라이언트의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/읽기 요청을 처리하고, 주기적으로 NameNode에 Heartbeat 보고 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP | 실제 물건을 쌓는 창고지기 |

아래의 구조도는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.0 이상의 에코시스템에서 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위에 YARN이 올라가고, 그 위에서 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)를 비롯한 다양한 엔진이 동작하는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 코어 아키텍처를 보여준다.

```text
┌────────────────────────────────────────────────────────┐
│           [Hadoop Ecosystem (Hive, Pig, Spark)]        │
├────────────────────────────────────────────────────────┤
│           [Data Processing Layer - 맵리듀스 외]        │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│    │ MapReduce V2 │ │ Apache Spark │ │ Apache Flink │  │
│    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘  │
├───────────┼────────────────┼────────────────┼──────────┤
│    ┌──────▼────────────────▼────────────────▼──────┐   │
│    │    YARN (Cluster Resource Management)         │   │
│    │  [ResourceManager] <--> [NodeManager]         │   │
│    └───────────────────────┬───────────────────────┘   │
├────────────────────────────┼───────────────────────────┤
│    ┌───────────────────────▼───────────────────────┐   │
│    │     HDFS (Hadoop Distributed File System)     │   │
│    │   [NameNode]       <-->      [DataNode(s)]    │   │
│    └───────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

이 아키텍처의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 저장 레이어([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/))와 자원 스케줄링 레이어([YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/)), 그리고 실제 연산 레이어([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)/Spark)가 완벽하게 분리(Decoupling)되어 있다는 점이다. 과거에는 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)만 사용할 수 있어 실시간 처리가 불가능했지만, YARN의 도입으로 인해 메모리 기반의 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 엔진인 스파크(Spark)나 스트리밍 엔진들이 동일한 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 클러스터 자원을 공유하며 동시에 구동될 수 있게 되었다. 실무에서는 이 구조를 통해 하나의 클러스터로 배치, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/), 실시간 분석을 모두 소화하는 [멀티 테넌트](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/)([Multi-tenant](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/)) [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)를 구성한다.

[맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)의 내부 동작 원리 (Map → Shuffle → Reduce)는 다음과 같은 텍스트 처리 예제([Word](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) Count)로 설명된다.
```java
// Map 과정: 한 줄을 읽어 단어별로 <단어, 1> 이라는 Key-Value 쌍 방출
public void map(LongWritable key, Text value, Context context) {
    String[] words = value.toString().split(" ");
    for (String word : words) {
        context.write(new Text(word), new IntWritable(1));
    }
}
// Reduce 과정: Shuffle된 후 같은 키(단어)를 가진 값들을 모두 더함
public void reduce(Text key, Iterable<IntWritable> values, Context context) {
    int sum = 0;
    for (IntWritable val : values) {
        sum += val.get(); // 1 + 1 + 1 ...
    }
    context.write(key, new IntWritable(sum)); // 최종 <단어, 총 빈도수> 출력
}
```

> 📢 **섹션 요약 비유**: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 일종의 거대한 '신도시 건설 프로젝트'입니다. HDFS라는 튼튼한 지반(저장)을 다지고, YARN이라는 통합 관리실(자원 분배)을 세우면, 그 위에 아파트([맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)), 빌딩(스파크), 공원(하이브) 등 어떤 건물이든 목적에 맞게 자유롭게 올릴 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)는 빅데이터의 시작을 열었지만, 극심한 디스크 I/O 의존성으로 인해 점차 한계를 드러냈다. 이에 따라 인메모리(In-Memory) 기반의 [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)(Spark)와의 비교 분석은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 실무에서 가장 중요한 의사결정 기준이다.

| 항목 | 아파치 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) ([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) | [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) (Spark) | 실무 판단 포인트 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 처리 모델</strong> | 디스크(Disk) 기반, 단계마다 HDFS에 임시 결과 저장 | 인메모리(In-Memory) 기반, RDD를 통해 메모리에서 파이프라인 처리 | 처리 속도 요구치 |
| **적합한 워크로드** | 대규모 야간 배치(Batch) 처리, [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 정제 | [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)(ML) 반복 훈련, 실시간 스트리밍, 대화형 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 반응성([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) |
| <strong>장애 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 방식</strong> | 디스크에 기록된 체크포인트에서 재시작 | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 리니지(Lineage, 연산 계보)를 통해 메모리 유실 시 즉시 재연산 | 장애 시 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 허용 범위 |
| **학습 곡선** | Map, Reduce로만 로직을 구현해야 해 복잡함 | SQL, Dataframe, 풍부한 고급 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 지원으로 직관적임 | 개발 생산성 |

아래의 동작 타이밍 매트릭스는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)가 왜 디스크 I/O 병목을 유발하는지 시각적으로 보여준다.

```text
[하둡 MapReduce와 Spark의 동작 타이밍 및 디스크 의존도 비교]

하둡 MapReduce :
[HDFS Read] ─> [Map 연산] ─> [Disk Write] ─> (Shuffle) ─> [Disk Read] ─> [Reduce 연산] ─> [HDFS Write]
                            ▲ 병목! 임시 결과를 모두 디스크에 씀

스파크 Spark :
[HDFS Read] ─> [Map/Filter/Join 등의 복합 연산이 메모리 위에서 연속 실행] ─> [최종 액션 시 HDFS Write]
                            ▲ 성능! 메모리에서 파이프라이닝 되어 중간 I/O 제거
```

A 방식([하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))은 한 단계가 끝날 때마다 안전을 위해 다음 단계를 위한 임시 결과를 디스크에 저장한다. 이는 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 허용에는 극도로 안정적이지만, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수천 번 반복해서 읽고 써야 하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서는 끔찍한 속도 저하를 부른다. 반면 B 방식(스파크)은 메모리에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 올려두고([캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)) 연산을 이어가므로 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 대비 10배~100배 빠른 성능을 낸다. 실무에서는 보통 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 HDFS를 무한 저장소([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))로 유지하면서, 연산 엔진만 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)에서 스파크로 교체하여 상호 보완적인 융합 아키텍처를 구축한다.

> 📢 **섹션 요약 비유**: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)가 중간 결과를 매번 수첩(디스크)에 꼼꼼히 적어가며 일하는 느긋한 서기라면, 스파크는 머릿속(메모리)에 다 외워두고 순식간에 답을 내는 천재 암산가입니다. 결국 서기의 창고([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)) 위에 천재 암산가(Spark)를 고용하는 것이 최고 효율을 냅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

현대의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어는 "아직도 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)을 직접 구축해야 하는가?"라는 근본적인 질문에 직면한다. [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계는 거대하지만, [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)([On-premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/))에서 직접 운영할 경우 클러스터 유지보수 복잡도가 매우 높다.

1. <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/045_msp_managed_service_provider/">클라우드 매니지드 서비스</a>(Managed <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a>) 전환</strong>: 기업들은 HDFS와 YARN을 직접 구성하는 대신, AWS EMR(Elastic [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))이나 GCP Dataproc을 사용하여 필요할 때만 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터를 띄우고 연산이 끝나면 종료하는 과금 최적화 아키텍처를 선택한다.
2. <strong>소규모 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> (Small Files) 문제의 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) HDFS는 수 GB, 수 TB의 거대한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 소수를 저장하는 데 최적화되어 있다. 만약 10KB짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수백만 개를 그대로 HDFS에 넣으면, [마스터 노드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/075_kubernetes_k8s_cluster_architecture/)([NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/))의 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 메모리가 고갈되어 전체 클러스터가 뻗어버리는 치명적 장애가 발생한다. 실무에서는 반드시 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)에 적재 전, 작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들을 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC 등)로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 및 병합([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))하는 전처리 파이프라인이 필수적이다.
3. <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a> (<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a>)의 양면성</strong>: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원시 형태 그대로 욱여넣을 수 있어 적재(Ingestion)는 매우 빠르다. 그러나 읽을 때 구조를 해석해야 하므로 파싱 오버헤드가 크고 [데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/), 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)장)으로 전락할 위험이 있다. 이를 방어하기 위해 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 메타스토어 기반의 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 관리가 병행되어야 한다.

```text
[하둡 도입 및 운영 시 안티패턴 대응 의사결정 트리]

[하둡 클러스터 내 성능/안정성 이슈 감지]
       ↓
[NameNode 메모리가 지속적으로 부족한가?]
  ├─ (Yes) ─> HDFS 내 파일 크기 점검 ─> (수많은 작은 파일 발견) ─> [해결: 하이브 병합 배치 잡 또는 SequenceFile 압축 적용]
  └─ (No) ──> [Task가 한 노드에서만 느리게 도는가?]
                     ↓
             (Data Skew / 데이터 쏠림 현상)
                     ↓
             [해결: MapReduce 파티션 키(해시 키) 재설계 및 Salt 값 추가]
```

이 운영 플로우의 핵심은 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 장애의 80%가 인프라 자체의 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 아니라 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형태와 분배 로직의 설계 미스'에서 비롯된다는 것이다. [네임노드](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리 붕괴([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))나 특정 워커 노드에만 일이 몰리는 스큐(Skew) 현상을 관제하고 선제 대응하는 것이 진정한 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 운영자의 핵심 역량이다.

> 📢 **섹션 요약 비유**: 거대한 화물 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)선([하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/))에 모래알(작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들)을 그냥 쏟아부으면 배의 시스템이 망가집니다. 모래를 거대한 포대자루([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)/병합 포맷)에 눌러 담아 실어야만 무사히 항해할 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 단순한 소프트웨어를 넘어 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루는 철학' 자체를 바꾸어 놓았으며, 그 사상은 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경으로 이어지고 있다.

| 기대 효과 | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 도입 이전의 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 중심 체계 | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 정착 이후 | 비즈니스/기술적 효과 |
|:---|:---|:---|:---|
| **저장 유연성** | 엄격한 RDB [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 버려지는 비정형 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 텍스트, 이미지 등 모든 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무한 보관 ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)([Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))의 자산화 |
| **연산의 확장** | SQL 기반의 한정된 분석 로직 | [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/), 자연어 처리 등 복잡한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 모델 훈련 파이프라인 구축 |
| **인프라 비용** | 스토리지 증설마다 수억 원의 라이선스/장비비 | 범용 하드웨어 및 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 결합으로 페타바이트당 단가 급감 | 저비용 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 대중화 |

현재 순수 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터의 수요는 AWS S3와 [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 등 클라우드 기반의 '스토리지-컴퓨팅 분리(Separation of Compute and Storage)' 아키텍처에 의해 대체되고 있다. 그러나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하고, 셔플하며, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 통해 장애를 감내하는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 핵심 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 원리는 [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)(Spark)와 [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)([Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)) 기술 깊숙한 곳에 여전히 살아 숨 쉬며 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 영원한 표준으로 남아 있다.

> 📢 **섹션 요약 비유**: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 빅데이터라는 대륙을 처음으로 개척한 '증기기관차'입니다. 지금은 고속철도(클라우드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 엔진)로 대체되고 있지만, 그 철로([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 철학)는 여전히 전 세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 산업을 달리고 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/">HDFS</a> (<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/">Hadoop</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/">Distributed File System</a>)</strong> | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 물리적 기반이 되는 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 허용형 대용량 [분산 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/) 구조
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/">맵리듀스</a> (<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/">MapReduce</a>)</strong> | 디스크 I/O를 활용하여 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쪼개고(Map) 합치는(Reduce) 고전적 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 프레임워크
- <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">Apache Spark</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">아파치 스파크</a>)</strong> | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 디스크 병목을 해결하기 위해 메모리 기반으로 작동하는 차세대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 연산 엔진
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/">YARN</a> (Yet Another Resource Negotiator)</strong> | 클러스터의 CPU와 메모리를 동적으로 쪼개어 여러 애플리케이션에 할당하는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.0의 자원 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">데이터 레이크</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">Data Lake</a>)</strong> | 원시 형태의 정형/비정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 무한히 저장하는 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 기반의 거대 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소 개념

### 📈 관련 키워드 및 발전 흐름도

```text
[GFS (Google File System) — 분산 파일 아이디어]
    │
    ▼
[HDFS (Hadoop Distributed File System) — 블록 복제]
    │
    ▼
[맵리듀스 (MapReduce) — 병렬 처리]
    │
    ▼
[YARN (Yet Another Resource Negotiator) — 자원 관리]
    │
    ▼
[아파치 스파크 (Apache Spark) — 인메모리 후계]
```

이 흐름은 GFS의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장 아이디어를 HDFS로 구현하고, [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)와 YARN을 거쳐 스파크 같은 인메모리 엔진으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 세상의 모든 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 다 모으고 싶은데 우리 집 책장(하나의 컴퓨터)에는 자리가 없어요.
2. 그래서 전 세계 친구들 수천 명의 방에 책을 조금씩 나누어 보관하고([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)), 특정 단어가 몇 개 있는지 찾고 싶을 땐 친구들이 각자 자기 방에서 찾은 다음 결과를 합쳐서 알려주게([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) 했어요.
3. 이렇게 여러 컴퓨터가 똘똘 뭉쳐서 어마어마하게 큰 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보관하고 똑똑하게 처리하는 마법 같은 시스템을 '아파치 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)'이라고 부른답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 12 / 258

← **이전**: [11. 분산 컴퓨팅 스케일 아웃 (Scale-out) - 저가형 범용 x86 서버(Commodity Hardware) 대수를 늘려 성능](/knowledge-base/studynote/14_data_engineering/01_infrastructure/011_distributed_computing_scale_out/)
**다음**: [13. HDFS (Hadoop Distributed File System) - 거대 파일을 기본 128MB 블록 단위로 쪼개 수많은 데이터노드에](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) →

---
