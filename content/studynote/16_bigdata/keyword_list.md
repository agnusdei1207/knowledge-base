+++
title = "16. 빅데이터 키워드 목록"
date = 2026-03-04

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++
[weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) = 9999

# 빅데이터 (Big [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 빅데이터 전 영역 기술사 수준 핵심 키워드
> ⚡ 빅데이터 기술사 문제: 단순 플랫폼 나열이 아닌 **아키텍처 선택 근거 + 법·제도 + 비즈니스 가치 + 미래 전망** 통합 서술 요구

---

## 1. 빅데이터 개론 / 특성 — 22개

1. 빅데이터 정의 — 3V: [Volume](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/)(양) / Velocity(속도) / Variety(다양성) (Laney, 2001)
2. 5V — 3V + Veracity([정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)) + Value(가치)
3. 7V — 5V + Visualization([시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)) + Variability(가변성)
4. 빅데이터 도입 필요성 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭증([제타바이트 시대](/knowledge-base/studynote/16_bigdata/01_intro/004_bigdata_necessity/)), [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 급증
5. [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 유형 — 텍스트/이미지/동영상/음성/[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/SNS/[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서
6. [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/) — [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/)/XML/HTML/CSV — [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 부분 보유
7. 빅데이터 생태계 — 수집→저장→처리→분석→[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)→활용
8. 빅데이터 vs 전통적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) — RDBMS 한계(수평 확장 불가, 고정 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))
9. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭증 요인 — [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)/SNS/모바일/센서/영상 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터 민주화](/knowledge-base/studynote/16_bigdata/01_intro/010_data_democratization/) ([Data Democratization](/knowledge-base/studynote/16_bigdata/01_intro/010_data_democratization/)) — 셀프서비스 분석, 시민 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [데이터 경제](/knowledge-base/studynote/16_bigdata/01_intro/011_data_economy/) ([Data Economy](/knowledge-base/studynote/16_bigdata/01_intro/011_data_economy/)) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산화, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거래소
12. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) ([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/)) — [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 자기결정권, 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)
13. [공공 빅데이터](/knowledge-base/studynote/16_bigdata/13_intro_trends/245_public_bigdata/) — 공공데이터포털, 행정안전부, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개방 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)
14. [데이터바우처 사업](/knowledge-base/studynote/16_bigdata/13_intro_trends/246_data_voucher/) — 중소기업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구매·가공 지원
15. 오픈데이터 원칙 — FAIR (Findable/Accessible/Interoperable/Reusable)
16. 유럽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Spaces, Gaia-X
17. 국가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)기본법, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 산업 진흥법
18. [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) ([Data Sovereignty](/knowledge-base/studynote/06_ict_convergence/05_data_science/410_ai_intellectual_property_data_sovereignty_data_act/)) — 국가별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 현지화 규제
19. [개인정보 비식별화](/knowledge-base/studynote/16_bigdata/13_intro_trends/251_data_anonymization/) — [k-익명성](/knowledge-base/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/) / [l-다양성](/knowledge-base/studynote/09_security/16_data_privacy/815_l_diversity/) / [t-근접성](/knowledge-base/studynote/09_security/16_data_privacy/816_t_closeness/)
20. [데이터 정형화 비율](/knowledge-base/studynote/16_bigdata/13_intro_trends/252_data_structured_ratio/) — 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중 정형 < 20%, 비정형 > 80%
21. [제타바이트 시대](/knowledge-base/studynote/16_bigdata/01_intro/004_bigdata_necessity/) — 2025년 전 세계 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ~175 ZB
22. [데이터 자산 평가](/knowledge-base/studynote/16_bigdata/13_intro_trends/254_data_asset_valuation/) — 재무적 가치화, ISO/IEC 22123

---

## 2. [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [에코](/knowledge-base/studynote/03_network/01_data_communication/031_에코_반향/)시스템 심화 — 28개

1. [Apache Hadoop](/knowledge-base/studynote/14_data_engineering/01_infrastructure/012_apache_hadoop/) — [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)) + [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) + 자원 관리([YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/))
2. [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop Distributed File System](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/)) — 블록 128MB, 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/)/[DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/)
3. [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) — [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/), [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 우려 → Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) / HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/)
4. [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) — 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 저장, 주기적 Heartbeat
5. [Rack Awareness](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/) — 같은 랙 두 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 방지, 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 최적화
6. [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) — Map([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리)/Shuffle&Sort/Reduce(집계) 3단계
7. Map 함수 — 입력 → ([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), Value) 쌍 출력
8. Reduce 함수 — 동일 Key의 Value 집계, 최종 결과 출력
9. [Shuffle & Sort](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/205_shuffle_sort_yarn_resource_manager/) — Map 출력을 Reduce로 분배 (네트워크 병목)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) ([Yet Another Resource Negotiator](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/)) — 자원 관리, Application Master / [Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Apache Hive](/knowledge-base/studynote/14_data_engineering/01_infrastructure/028_apache_hive/) — SQL on [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/), HQL, 메타스토어(MySQL/PostgreSQL), 배치형
12. Apache [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) — [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) on [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/), 열 지향, 실시간 랜덤 R/W, [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존
13. [Apache Pig](/knowledge-base/studynote/16_bigdata/02_hadoop/038_apache_pig/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 스크립트 언어 (Pig Latin), 복잡한 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)
14. [Apache Sqoop](/knowledge-base/studynote/16_bigdata/02_hadoop/039_apache_sqoop/) — RDBMS ↔ [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 임포트/익스포트
15. [Apache Flume](/knowledge-base/studynote/16_bigdata/02_hadoop/040_apache_flume/) — [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) 에이전트, Source/Channel/Sink 구조
16. [Apache Oozie](/knowledge-base/studynote/16_bigdata/02_hadoop/051_apache_oozie/) — [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 워크플로우/코디네이터 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)
17. [Apache Zookeeper](/knowledge-base/studynote/14_data_engineering/01_infrastructure/029_apache_zookeeper/) — [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이션 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 리더 선출, 잠금
18. [Apache Ambari](/knowledge-base/studynote/16_bigdata/02_hadoop/041_apache_ambari_management/) — [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 관리 GUI
19. Cloudera CDH / HDP (Hortonworks) → [CDP](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) ([Cloudera Data Platform](/knowledge-base/studynote/16_bigdata/02_hadoop/042_cloudera_cdp_platform/))
20. [Apache Tez](/knowledge-base/studynote/16_bigdata/02_hadoop/028_apache_tez/) — [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 실행 엔진, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)/Pig 속도 개선
21. [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 연동) — Flume 대체, 내구성/[처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)↑
22. [Apache Storm](/knowledge-base/studynote/16_bigdata/02_hadoop/044_apache_storm/) — [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 실시간 처리, Spout/Bolt 토폴로지
23. Apache Samza — LinkedIn, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 네이티브 스트리밍
24. [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 페더레이션 ([Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/)) — 다중 [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/), [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)
25. [HDFS ViewFS](/knowledge-base/studynote/16_bigdata/02_hadoop/048_hdfs_viewfs/) — [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 투명 접근
26. [Small File Problem](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/) — [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 비효율, HAR/Sequence [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/ORC로 해결
27. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 — Avro / [Protocol Buffers](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) / Thrift / Kryo
28. [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 보안 — [Kerberos](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), Ranger(권한)/Atlas([카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/))

---

## 3. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 / 스파크 심화 — 24개

1. [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) — 인메모리 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리, [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 대비 최대 100배 빠름
2. [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) ([Resilient Distributed Dataset](/knowledge-base/studynote/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset/)) — 불변, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [결함 허용](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/296_fault_tolerance_architecture/), Lineage 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)
3. Transformation vs Action — [Lazy Evaluation](/knowledge-base/studynote/14_data_engineering/01_infrastructure/023_lazy_evaluation/) (변환은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 액션은 즉시)
4. DataFrame / Dataset — [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 기반, Catalyst 최적화, Type-[safe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)
5. [Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/) — SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 DataFrame 처리, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 메타스토어 연동
6. [Catalyst Optimizer](/knowledge-base/studynote/16_bigdata/03_spark/057_catalyst_optimizer/) — [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) → 물리 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 최적화
7. [Tungsten Engine](/knowledge-base/studynote/16_bigdata/03_spark/058_tungsten_engine/) — CPU/메모리 최적화, Codegen, Off-[heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 메모리
8. AQE (Adaptive Query Execution) — 런타임 통계 기반 자동 최적화 (Spark 3.0+)
9. [Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) ([DStream](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/)) — 마이크로배치 스트리밍 (구세대)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/) — DataFrame [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스트리밍, 연속 처리, [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). MLlib — [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) ML [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) ([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)/회귀/군집/추천/[PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))
12. GraphX — [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리, PageRank
13. Spark 배포 모드 — Local / [Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) / [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) / [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) / Mesos
14. Executor / Driver / Cluster Manager — Spark 실행 구조
15. Shuffle 최적화 — spark.sql.shuffle.partitions, AQE 코어리스
16. Spark [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 최적화 (Kryo) — Kryo > Java, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이
17. Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) — 소규모 테이블을 모든 Executor에 복사
18. [Skew Join](/knowledge-base/studynote/16_bigdata/03_spark/069_skew_join/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쏠림 해결 (AQE 자동 분할)
19. [파티션 최적화](/knowledge-base/studynote/16_bigdata/03_spark/070_partition_optimization/) — repartition / coalesce, 코어 수 × 2~4
20. [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) ([Checkpointing](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/)) — Lineage 단절, 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가속
21. [Spark History Server](/knowledge-base/studynote/16_bigdata/03_spark/072_spark_history_server/) — 완료 작업 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 조회, UI
22. [Delta Lake on Spark](/knowledge-base/studynote/16_bigdata/03_spark/073_delta_lake_on_spark/) — ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), MERGE INTO, 타임 트래블
23. [Photon Engine](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) ([Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)) — 네이티브 벡터화 Spark 실행 엔진
24. [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) 3.5+ 개선 — ANSI SQL 확대, Python [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 강화

---

## 4. 스트리밍 / 실시간 처리 — 22개

1. 스트리밍 처리 필요성 — 실시간 이상 감지, 즉각 대응 의사결정
2. [Apache Flink](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) — 상태 기반 스트리밍, 이벤트 시간 처리, Exactly-Once
3. Flink 아키텍처 — JobManager / TaskManager / JobGraph
4. DataStream [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) / Table [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) & SQL — Flink 두 계층
5. Flink [Savepoint](/knowledge-base/studynote/05_database/04_transactions_concurrency/200_savepoint_partial_rollback/) / Checkpoint — 상태 저장, 재시작 지점
6. 이벤트 시간 (Event Time) vs 처리 시간 (Processing Time)
7. [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) — [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 허용 임계, 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)
8. [윈도우 연산](/knowledge-base/studynote/16_bigdata/04_streaming/086_window_operations/) — 텀블링 / 슬라이딩 / [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) / 글로벌 윈도우
9. [정확히 한 번](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_cross_validation/) ([Exactly-Once Semantics](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_cross_validation/)) — [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) + Idempotent Sink
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) — 내구성 있는 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, 스트리밍 기반
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 키 기반 / 라운드로빈 / 커스텀
12. [Consumer Lag](/knowledge-base/studynote/16_bigdata/04_streaming/089_consumer_lag/) — [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 소비 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링, Burrow / JMX
13. [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) MirrorMaker 2 — 클러스터 간 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)
14. [Amazon Kinesis](/knowledge-base/studynote/16_bigdata/04_streaming/091_amazon_kinesis/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams — 샤드 기반, AWS 관리형
15. Google Pub/Sub — [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 대안, GCP, 글로벌 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)
16. [Azure Event Hubs](/knowledge-base/studynote/16_bigdata/04_streaming/093_azure_event_hubs/) — [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 호환 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), AMQP 지원
17. [Apache Pulsar](/knowledge-base/studynote/16_bigdata/04_streaming/094_apache_pulsar/) — [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 대안, 컴퓨팅/스토리지 분리, [멀티 테넌시](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)
18. [람다 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/095_lambda_architecture/) — 배치([Speed Layer](/knowledge-base/studynote/12_it_management/02_itsm_itil/092_GPT_NLP/)) + 실시간(Batch Layer) + Serving Layer
19. [카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/) — 스트리밍만으로 단순화, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Flink
20. 스트리밍 SQL — ksqlDB ([Confluent](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/)) / Flink SQL / [Spark Structured Streaming](/knowledge-base/studynote/16_bigdata/03_spark/061_structured_streaming/)
21. [CEP](/knowledge-base/studynote/16_bigdata/04_streaming/098_cep/) ([Complex Event Processing](/knowledge-base/studynote/16_bigdata/04_streaming/098_cep/)) — 패턴 이벤트 감지, Flink [CEP](/knowledge-base/studynote/16_bigdata/04_streaming/098_cep/)
22. 실시간 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) — Apache Druid / Apache Pinot / ClickHouse — ms [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)

---

## 5. 빅데이터 분석 기법 — 26개

1. [기술 통계](/knowledge-base/studynote/16_bigdata/05_analysis/100_descriptive_statistics/) ([Descriptive Statistics](/knowledge-base/studynote/16_bigdata/05_analysis/100_descriptive_statistics/)) — 평균/중앙값/[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)/분포 요약
2. [추론 통계](/knowledge-base/studynote/16_bigdata/05_analysis/101_inferential_statistics/) ([Inferential Statistics](/knowledge-base/studynote/16_bigdata/05_analysis/101_inferential_statistics/)) — 표본 → 모집단 추론, [가설 검정](/knowledge-base/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/)
3. [탐색적 데이터 분석](/knowledge-base/studynote/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis/) ([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/)) — 패턴 발견, [이상치 탐지](/knowledge-base/studynote/10_ai/05_data_science_ml/397_outlier_mahalanobis/), [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
4. [회귀 분석](/knowledge-base/studynote/08_algorithm_stats/08_stats/149_regression_analysis/) (Regression) — 단순/다중/다항/릿지/라쏘/엘라스틱넷
5. [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) ([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) — [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) / 트리 / [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) / [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)
6. [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) ([Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)) — K-Means / [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) / 계층적 / Gaussian Mixture
7. [연관 규칙](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/) ([Association Rules](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/)) — Apriori / [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth, [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)/[신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)/[향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)
8. [장바구니 분석](/knowledge-base/studynote/16_bigdata/05_analysis/107_market_basket_analysis/) ([Market Basket Analysis](/knowledge-base/studynote/16_bigdata/05_analysis/107_market_basket_analysis/)) — 구매 패턴, 교차 판매
9. [감성 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/105_exploratory_data_analysis/) ([Sentiment Analysis](/knowledge-base/studynote/12_it_management/03_ea_isp/105_exploratory_data_analysis/)) — 긍/부정/중립, [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 기반 심화
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [텍스트 마이닝](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/) ([Text Mining](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/)) — [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) / [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) / [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) / [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [소셜 네트워크 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) ([SNA](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) — 중심성 / 커뮤니티 탐지 / 영향력
12. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) — 통계 기반 / ML 기반 / 딥러닝 기반
13. [시계열 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/341_time_series_ar_ma_arma/) (Time Series) — [ARIMA](/knowledge-base/studynote/06_ict_convergence/05_data_science/342_arima_auto_regressive_integrated_moving_average/) / SARIMA / Prophet / [LSTM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/292_lstm/) / [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)
14. [공간 분석](/knowledge-base/studynote/16_bigdata/05_analysis/113_spatial_analysis/) ([Spatial Analysis](/knowledge-base/studynote/16_bigdata/05_analysis/113_spatial_analysis/)) — 지리정보시스템(GIS), PostGIS
15. [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) ([Graph Analytics](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/)) — PageRank / 커뮤니티 탐지 / 최단 경로
16. [텍스트 요약](/knowledge-base/studynote/16_bigdata/05_analysis/115_text_summarization/) — 추출적(Extractive) / 추상적(Abstractive) 요약
17. [토픽 모델링](/knowledge-base/studynote/16_bigdata/05_analysis/116_topic_modeling/) — LDA / BERTopic / NMF
18. [개체명 인식](/knowledge-base/studynote/16_bigdata/05_analysis/117_ner/) ([NER](/knowledge-base/studynote/16_bigdata/05_analysis/117_ner/)) — 인물/장소/조직/날짜 추출
19. [이미지 분석](/knowledge-base/studynote/16_bigdata/05_analysis/118_image_analysis/) — [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) 기반 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)/탐지/분할 대용량 배치
20. [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/) — 이상 감지, 보안 이벤트, 패턴 발견
21. [클릭스트림 분석](/knowledge-base/studynote/16_bigdata/05_analysis/120_clickstream_analysis/) — 사용자 행동 패턴, 전환율 최적화
22. A/B 테스트 — 실험적 방법론, 통계적 유의성
23. [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) — [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) / 콘텐츠 기반 / 하이브리드
24. [예측 분석](/knowledge-base/studynote/16_bigdata/02_hadoop/046_predictive_analytics/) ([Predictive Analytics](/knowledge-base/studynote/16_bigdata/02_hadoop/046_predictive_analytics/)) — 이탈 예측, 대출 부도, 장비 고장
25. 처방적 분석 ([Prescriptive Analytics](/knowledge-base/studynote/16_bigdata/02_hadoop/047_prescriptive_analytics/)) — 최적 의사결정 제안
26. [인과 추론](/knowledge-base/studynote/16_bigdata/05_analysis/122_causal_inference/) ([Causal Inference](/knowledge-base/studynote/16_bigdata/05_analysis/122_causal_inference/)) — 상관≠인과, DoWhy, 반사실 분석

---

## 6. [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) — 20개

1. [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 등장 배경 — RDBMS 수평 확장 한계, BASE 원칙
2. BASE 원칙 — Basically Available / Soft [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) / Eventually Consistent
3. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 — [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) / [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) / [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance (2개만 선택)
4. [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 이론 — [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 확장, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) vs [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 트레이드오프
5. 키-값 ([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value) DB — [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) / [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) / Riak — 빠른 조회, 단순 구조
6. [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) — 인메모리, Pub/Sub, 자료구조(String/List/Set/Hash/ZSet), 클러스터
7. 문서형 ([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/)) DB — [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) / CouchDB / Firestore
8. [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 아키텍처 — [ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) / [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) / Mongos / [Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) Server
9. 컬럼 패밀리 (Column Family) DB — [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) / [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) / ScyllaDB
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) — [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 없는 링 구조, 토큰 기반 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해시, 튜닝 가능한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB — Neo4j / Amazon Neptune / Memgraph — [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화
12. Cypher [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 (Neo4j) — MATCH / WHERE / RETURN
13. 시계열 DB — [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) / TimescaleDB / QuestDB — 시간 기반 인덱싱
14. 검색 엔진 DB — [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) / OpenSearch — [역색인](/knowledge-base/studynote/05_database/07_exam_summary/500_inverted_index_elasticsearch/), 전문 검색
15. 다중 모델 DB — ArangoDB / SurrealDB — 여러 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델 지원
16. [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/) — [CockroachDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/292_etl_process/) / [TiDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/) / YugabyteDB — SQL + 수평 확장 + ACID
17. 인메모리 DB — [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) / Memcached / SAP HANA — 마이크로초 응답
18. [일관성 수준 선택](/knowledge-base/studynote/16_bigdata/06_nosql/140_consistency_levels/) — Strong / Bounded Staleness / [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) / Consistent Prefix / Eventual
19. [멀티 마스터 복제](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/272_multi_master_replication/) — CouchDB / [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Global Tables
20. [스키마리스 설계 패턴](/knowledge-base/studynote/16_bigdata/06_nosql/142_schemaless_design_patterns/) — [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) vs [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 허용 설계

---

## 7. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) / [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) — 18개

1. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) — 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장, [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/), 저비용
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스왐프 ([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) — 거버넌스 부재, 레이크 변질 위험
3. [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) — 구조화, [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/), 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)
4. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) ([Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)) — 레이크(유연성) + [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)(ACID/[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)), [Delta Lakehouse](/knowledge-base/studynote/14_data_engineering/04_mlops/177_delta_lakehouse_time_travel_transaction/)
5. [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) — ACID on [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), 타임 트래블, MERGE, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 강제
6. [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) — [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/), 히든 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)
7. [Apache Hudi](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/) ([Hadoop Upserts Deletes Incrementals](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/)) — Uber, [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 지원
8. [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) ([Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)) — [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 통합 거버넌스
9. [다중 계층 아키텍처](/knowledge-base/studynote/16_bigdata/07_data_lake/151_multi_tier_architecture/) — Bronze(원시) / Silver(정제) / Gold(집계) — Medallion
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Medallion Architecture](/knowledge-base/studynote/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold/) — [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) 기반 3계층, [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 표준
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) ([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/)) — [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 분권, [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)화, 연합 거버넌스
12. [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) ([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)) — [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 인터페이스, [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), 품질 지표 보유
13. [ELT vs ETL](/knowledge-base/studynote/16_bigdata/07_data_lake/155_elt_vs_etl/) — 클라우드에서 ELT가 주류 (먼저 적재 후 변환)
14. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) ([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)) — 위치 무관 지능형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연결, Gartner
15. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) — Amazon EMR / Azure HDInsight / GCP Dataproc
16. [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) — Spark 기반 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 플랫폼, [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)
17. [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) on [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) — External Table, Iceberg 지원
18. [Microsoft Fabric](/knowledge-base/studynote/16_bigdata/07_data_lake/160_microsoft_fabric/) — One Lake, [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) + Synapse + [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Factory 통합

---

## 8. 빅데이터 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) — 14개

1. [데이터 시각화 원칙](/knowledge-base/studynote/16_bigdata/08_visualization/161_visualization_principles/) — 목적 명확성 / 간결성 / [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 잉크 비율 (Tufte)
2. [차트 유형 선택](/knowledge-base/studynote/16_bigdata/08_visualization/162_chart_type_selection/) — 비교(막대)/추세(선)/비율(파이/도넛)/분포(히스토그램/박스)
3. [대시보드 설계](/knowledge-base/studynote/16_bigdata/08_visualization/163_dashboard_design/) — [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 중심, 5초 규칙, 인터랙티브
4. [Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/) — 드래그앤드롭, VizQL, Extract/Live 연결
5. [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) — Microsoft 생태계 통합, DAX, Dataflow
6. [Looker](/knowledge-base/studynote/16_bigdata/08_visualization/166_looker/) / [Looker](/knowledge-base/studynote/16_bigdata/08_visualization/166_looker/) Studio — Google, LookML 시맨틱 레이어
7. [Apache Superset](/knowledge-base/studynote/16_bigdata/08_visualization/167_apache_superset/) — [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), SQL Lab, 다양한 차트
8. [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) — [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)/[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/추적 통합 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/), 알람
9. [Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/) — ELK [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/), [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). D3.js — JavaScript 기반 커스텀 인터랙티브 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). Plotly / [Dash](/knowledge-base/studynote/03_network/09_application_layer_web_email/510_dash_dynamic_adaptive_streaming_over_http/) — Python 기반 인터랙티브 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
12. [네트워크 시각화](/knowledge-base/studynote/16_bigdata/08_visualization/172_network_visualization/) — Gephi / Cytoscape — [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
13. [지리공간 시각화](/knowledge-base/studynote/16_bigdata/08_visualization/173_geospatial_visualization/) — Kepler.gl / Folium / Deck.gl — 지도 기반
14. [빅데이터 시각화 도전](/knowledge-base/studynote/16_bigdata/08_visualization/174_bigdata_visualization_challenges/) — 수십억 개 포인트, 집계/샘플링/렌더링 최적화

---

## 9. 빅데이터 플랫폼 / 아키텍처 — 16개

1. [빅데이터 플랫폼 선택 기준](/knowledge-base/studynote/16_bigdata/09_platform/175_platform_selection_criteria/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모 / 실시간 여부 / 비용 / 기술 역량
2. [On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) vs Cloud 비교 — [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용 vs OPEX, 유연성
3. [빅데이터 참조 아키텍처](/knowledge-base/studynote/16_bigdata/09_platform/177_bigdata_reference_architecture/) — 수집→저장→처리→분석→[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)→관리
4. [모던 데이터 스택](/knowledge-base/studynote/16_bigdata/09_platform/178_modern_data_stack/) ([MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/)) — Fivetran + [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) + dbt + [Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/)
5. 실시간 + 배치 통합 플랫폼 — Unified Batch/Streaming (Spark/Flink)
6. [데이터 허브](/knowledge-base/studynote/16_bigdata/09_platform/180_data_hub/) ([Data Hub](/knowledge-base/studynote/16_bigdata/09_platform/180_data_hub/)) — 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집계 및 배포 계층
7. [멀티클라우드 데이터 플랫폼](/knowledge-base/studynote/16_bigdata/09_platform/181_multicloud_data_platform/) — [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) / [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 멀티클라우드 지원
8. [서버리스 빅데이터](/knowledge-base/studynote/16_bigdata/09_platform/182_serverless_bigdata/) — AWS Athena / [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) / Redshift [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)
9. [데이터 오케스트레이션](/knowledge-base/studynote/16_bigdata/09_platform/183_data_orchestration/) — [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) / Dagster / Prefect
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터 카탈로그 통합](/knowledge-base/studynote/16_bigdata/09_platform/184_data_catalog_integration/) — Glue [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) / DataHub / OpenMetadata / Alation
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [확장성 설계](/knowledge-base/studynote/16_bigdata/09_platform/185_scalability_design/) — 수평 확장 / [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) / [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) / 클러스터 자동 확장
12. [데이터 컴프레션 전략](/knowledge-base/studynote/16_bigdata/09_platform/186_data_compression/) — Snappy(속도) / Zstd([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률) / Gzip([호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/))
13. [컬럼 기반 파일 포맷](/knowledge-base/studynote/16_bigdata/09_platform/187_parquet_orc_iceberg_arrow/) — [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) / ORC / Iceberg / Arrow — 조회 최적화
14. [빅데이터 비용 최적화](/knowledge-base/studynote/16_bigdata/09_platform/188_spot_instance_ri/) — [Spot Instance](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/209_spot_instance_cloud_cost_optimization/) / 컴퓨팅-스토리지 분리 / RI
15. [데이터 이동 비용](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/) — [Egress](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/) 비용, 리전 내 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로컬화
16. [하이브리드 분석](/knowledge-base/studynote/16_bigdata/09_platform/190_management/) — [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) + 클라우드 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)팅

---

## [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 빅데이터 거버넌스 / 품질 / 법규 — 18개

1. [데이터 거버넌스 정의](/knowledge-base/studynote/16_bigdata/10_governance/197_data_governance_definition/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유·관리·사용 원칙 체계
2. [데이터 거버넌스 구성 요소](/knowledge-base/studynote/16_bigdata/10_governance/198_data_governance_components/) — [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)/표준/역할/프로세스/도구
3. [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) ([Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)) — [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책임자
4. [데이터 소유자](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) ([Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)) — 비즈니스 책임, 접근 승인
5. [데이터 품질 차원](/knowledge-base/studynote/16_bigdata/10_governance/201_data_quality_dimensions/) — 완전성/[정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)/[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)/적시성/유일성/유효성
6. [데이터 품질 관리 도구](/knowledge-base/studynote/16_bigdata/10_governance/202_data_quality_tools/) — Great Expectations / Deequ / Soda Core
7. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 ([Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)) — 열 수준 계보, 영향 분석, Apache Atlas
8. [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) — 비즈니스/기술/운영 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 3유형
9. [마스터 데이터 관리](/knowledge-base/studynote/12_it_management/01_governance_strategy/051_mdm_master_data_management/) ([MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) — 황금 레코드, 중복 제거
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안 — 암호화(전송/저장) / 접근 제어 / [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) / [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [개인정보보호법 빅데이터 특례](/knowledge-base/studynote/16_bigdata/10_governance/206_pipa_bigdata_exception/) — 가명처리 허용 (2020년 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 3법)
12. [GDPR Article 89](/knowledge-base/studynote/16_bigdata/10_governance/207_gdpr_article_89/) — 과학적 연구 목적 빅데이터 처리 특례
13. [데이터 비식별화 기법](/knowledge-base/studynote/16_bigdata/10_governance/208_data_deidentification_techniques/) — [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/) / 가명화 / 집계화 / 노이즈 추가
14. [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/) ([Differential Privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/)) — 통계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) + 노이즈, Apple/Google
15. [합성 데이터](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/) ([Synthetic Data](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/)) — 원본과 유사 통계적 특성, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 대체
16. [데이터 윤리](/knowledge-base/studynote/16_bigdata/10_governance/211_data_ethics/) ([Data Ethics](/knowledge-base/studynote/16_bigdata/10_governance/211_data_ethics/)) — [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 편향, 공정성, 투명성
17. [빅데이터 분쟁](/knowledge-base/studynote/16_bigdata/10_governance/212_bigdata_disputes/) — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권, 수집 동의, 목적 외 사용
18. [데이터 감사](/knowledge-base/studynote/16_bigdata/10_governance/213_data_audit/) ([Data Audit](/knowledge-base/studynote/16_bigdata/10_governance/213_data_audit/)) — 접근 이력, 변경 이력, 보관 기간

---

## [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 빅데이터 산업 응용 — 16개

1. [금융 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/214_finance_bigdata/) — 신용평가 / 이상거래탐지([FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/)) / [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 관리 / 알고트레이딩
2. [의료 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/215_healthcare_bigdata/) — 전자의무기록(EMR) / 유전체 분석 / 임상 예측 / 신약 개발
3. 공공 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 — 교통 예측 / 범죄 예방 / 도시 계획 / 행정 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 개선
4. [제조 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/217_manufacturing_bigdata/) — 예지 정비([PdM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/123_pdm_product_data_management/)) / 불량 감지 / 에너지 최적화
5. 유통·물류 빅데이터 — 수요 예측 / 재고 최적화 / 배송 경로 최적화
6. [미디어 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/219_media_bigdata/) — 시청 분석 / 콘텐츠 추천 / 광고 타겟팅
7. SNS 빅데이터 — 여론 분석 / 트렌드 감지 / 인플루언서 분석
8. [스마트시티 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/221_smart_city_bigdata/) — [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 분석 / 교통 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 최적화 / 에너지 그리드
9. [농업 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/222_agriculture_bigdata/) — 정밀 농업 / 날씨 연계 수확량 예측 / 토양 분석
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [교육 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/223_education_bigdata/) — 학습 분석([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Analytics) / 맞춤형 교육
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [관광 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/224_tourism_bigdata/) — 관광 수요 예측 / 혼잡도 분석 / 관광 코스 추천
12. [통신 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/225_telecom_bigdata/) — 네트워크 장애 예측 / 고객 이탈 분석 / QoE 최적화
13. [에너지 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/226_energy_bigdata/) — 전력 수요 예측 / 신재생에너지 출력 예측 / 스마트미터
14. [보험 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/227_management/) — 보험료 산정 / 사기 탐지 / 언더라이팅 자동화
15. [부동산 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/228_management/) — 시세 예측 / 상권 분석 / 인구 이동 분석
16. [국방 빅데이터](/knowledge-base/studynote/16_bigdata/11_industry/229_audit/) — 정보 분석 / 적 행동 예측 / 보안 위협 탐지

---

## 12. 최신 빅데이터 동향 — 12개

1. [레이크하우스 주류화](/knowledge-base/studynote/16_bigdata/12_trends/230_delta_iceberg_hudi/) — Delta/Iceberg/Hudi 3강 경쟁, 개방형 포맷
2. [데이터 메시 확산](/knowledge-base/studynote/16_bigdata/12_trends/231_management/) — [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권, 자율 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)
3. 실시간 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 성장 — Druid / Pinot / ClickHouse / StarRocks
4. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) + 빅데이터 융합 — 대규모 ML 학습, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석
5. [Text-to-SQL on BigData](/knowledge-base/studynote/16_bigdata/12_trends/234_text_to_sql_on_bigdata/) — LLM으로 자연어 → [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
6. [스트리밍 우선 아키텍처](/knowledge-base/studynote/16_bigdata/12_trends/235_kappa/) — 배치 → 스트리밍 전환, [Kappa](/knowledge-base/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처 강화
7. [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/) ([Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) — [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 안정성 보장 생산자-소비자 합의
8. [오픈소스 포맷 경쟁](/knowledge-base/studynote/16_bigdata/12_trends/237_apache_iceberg/) — [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) 사실상 표준화 움직임
9. [양자 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/236_quantum_computing_pqc/) + 빅데이터 — 최적화 문제, 양자 ML [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 연구
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [엣지 빅데이터](/knowledge-base/studynote/16_bigdata/12_trends/239_architecture/) — 엣지에서 집계 후 클라우드 전송, [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 절감
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Databricks vs Snowflake](/knowledge-base/studynote/16_bigdata/12_trends/240_databricks_vs_snowflake_dw/) — [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) vs [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 진영 경쟁
12. [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/) — Monte Carlo / Bigeye — [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)

---

**총 키워드 수: 216개**
