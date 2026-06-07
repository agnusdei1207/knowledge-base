---
title: "Apache Hadoop Distributed Storage Processing"
date: "2026-03-04"
tags:
  - "hadoop"
  - "studynote-bigdata"
weight: 23
---
## 핵심 인사이트 (3줄 요약)
- **빅데이터의 시초**: [아파치 하둡](/studynote/14_data_engineering/01_infrastructure/012_apache_hadoop/)([Apache Hadoop](/studynote/14_data_engineering/01_infrastructure/012_apache_hadoop/))은 방대한 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 저가형 상용 서버(Commodity Hardware) 수백 대에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하고 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리하는 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 자바 프레임워크입니다.
- **스토리지와 연산의 결합**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장을 담당하는 [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)([HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/))과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 엔진([MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))으로 구성되어 단일 거대 머신의 한계를 극복했습니다.
- <strong><a href="/studynote/03_network/01_data_communication/031_에코_반향/">에코</a>시스템의 중심</strong>: [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 자체만으로는 속도의 한계(디스크 I/O 병목)가 있으나, 자원 관리자([YARN](/studynote/14_data_engineering/01_infrastructure/020_yarn/)) 위에서 스파크(Spark), 하이브([Hive](/studynote/05_database/04_transactions_concurrency/544_hive/)) 등 다양한 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 엔진들을 돌리는 거대한 생태계의 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역할을 수행합니다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
2000년대 초반 구글은 전 세계 웹페이지를 긁어모아 검색 엔진을 구축해야 했으나 기존 RDBMS와 고가의 스토리지로는 비용과 용량의 한계에 부딪혔습니다. 구글이 발표한 GFS([분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/))와 [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 논문을 바탕으로, 더그 커팅(Doug Cutting)이 야후에서 개발을 주도해 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)화한 것이 [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)입니다.
빅데이터라는 단어를 세상에 각인시킨 일등 공신이며, 비싼 슈퍼컴퓨터 한 대를 사는 대신 싼 100대의 깡통 컴퓨터를 묶어 '[스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))' 수평 확장의 표준 패러다임을 정립했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.0 이후 아키텍처는 스토리지, 연산, 자원 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링의 철저한 계층 분리를 달성했습니다.

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

1. <strong><a href="/studynote/14_data_engineering/01_infrastructure/013_hdfs/">HDFS</a> (<a href="/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/">Hadoop Distributed File System</a>)</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 128MB 블록 단위로 쪼개어 수많은 워커 노드에 3벌씩 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 저장하여 디스크 고장에 대비한 [결함 허용](/studynote/04_software_engineering/05_devops_ci_cd/296_fault_tolerance_architecture/)([Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))을 달성합니다.
2. <strong><a href="/studynote/14_data_engineering/01_infrastructure/020_yarn/">YARN</a> (자원 협상가)</strong>: [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 내 CPU와 메모리 자원을 누가 얼마나 쓸지 할당하고 통제하는 클러스터 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역할을 합니다.
3. <strong><a href="/studynote/14_data_engineering/01_infrastructure/019_data_locality/">데이터 지역성</a> (<a href="/studynote/14_data_engineering/01_infrastructure/019_data_locality/">Data Locality</a>)</strong>: 방대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 서버로 가져와서 연산하면 네트워크가 마비되므로, 반대로 '[연산 코드](/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/)'를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 저장된 워커 노드로 전송하여 각자 자리에서 연산하는 혁신적 구조를 채택했습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 RDBMS ([Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), MySQL) | [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) ([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) + [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) |
| :--- | :--- | :--- |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 구조</strong> | [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/) (Strict [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 요구, [Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) | 정형, 반정형, [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 무관 ([Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) |
| **하드웨어 아키텍처** | 고가의 [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)([Scale-up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 서버 (CPU/RAM 집중 증설) | 저가형 x86 서버 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) (무한 수평 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) |
| **처리 특성** | 실시간 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) (ACID 보장), [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 고속 I/O | 방대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 배치(Batch) 처리 중심 로딩 시간 긺 |
| <strong>장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 별도 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 솔루션 필요 ([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 의존도 높음) | 소프트웨어 단에서 3중 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 노드 고장 시 자동 우회 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **레거시화에 대한 판단**: 디스크 기반 반복 연산을 수행하는 [맵리듀스](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)([MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))는 속도가 너무 느려 현재 실무에서 메모리 기반의 '스파크(Spark)'로 99% 대체되었습니다. 그러나 밑바탕을 지탱하는 스토리지 HDFS와 자원 관리자 YARN은 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 빅데이터 클러스터의 중추로 여전히 굳건합니다.
- **아키텍처 진화 방향**: 기업들이 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 장비 관리에 지치며 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)의 관리형 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(AWS EMR, GCP Dataproc)로 이전하거나, [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 스토리지를 무한한 S3 객체 스토리지로 교체하여 '컴퓨팅과 스토리지의 분리'를 구현하는 모던 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)로 전환하는 추세입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 비용을 극적으로 낮춰 기업이 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 텍스트를 버리지 않고 모두 저장([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))하게 만들었으며, 이는 훗날 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 딥러닝 부흥을 위한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자양분 축적으로 직결되었습니다. [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 빅데이터 플랫폼을 구축하고 이해하는 근본적인 핵심 뼈대로서 기술사와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어에게 최우선 필수 지식입니다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **선행 개념**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅, 빅데이터 3V, [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)
- **핵심 기술**: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), [YARN](/studynote/14_data_engineering/01_infrastructure/020_yarn/)
- **확장 및 응용**: [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/), [Apache Hive](/studynote/14_data_engineering/01_infrastructure/028_apache_hive/), [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/), AWS EMR

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS]
    |
    v
[MapReduce]
    |
    v
[YARN]
    |
    v
[Hive/Spark]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 세상의 모든 책을 도서관 사서 한 명이 전부 읽고 요약하려면 평생이 걸려도 모자랄 거예요. (기존 방식)
2. [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 만 명의 친구들을 한꺼번에 불러서 책을 몇 장씩 나눠주고, 각자 읽고 요약해오라고 시키는 방법이랍니다.
3. 중간에 한 친구가 아파서 집에 가더라도, 다른 친구에게 복사본을 줘서 대신 읽게 하니까 절대 실패하지 않아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 23 / 262

<- **이전**: [22. 데이터 자산 평가 — 재무적 가치화, ISO/IEC 22123](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/)
**다음**: [02. HDFS (Hadoop Distributed File System) - 하둡 분산 파일 시스템](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) ->

---
