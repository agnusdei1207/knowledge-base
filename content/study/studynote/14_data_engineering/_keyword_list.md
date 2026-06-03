---
title: 16. 빅데이터 및 데이터 과학 키워드 목록
date: '2026-03-04'
tags:
- studynote-bigdata
---
[[267_weight_bias_activation|weight]] = 9999

# 빅데이터 (Big [[001_dikw_pyramid|Data]]) 및 [[001_dikw_pyramid|데이터]] 과학 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 [[001_dikw_pyramid|데이터]] 사이언티스트(DS), [[001_dikw_pyramid|데이터]] 엔지니어(DE)를 위한 빅데이터 처리 플랫폼, [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]], [[001_dikw_pyramid|데이터]] 분석 수학/통계, 최신 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 아키텍처 및 기계학습(ML) 전 영역 800대 핵심 키워드입니다.

---

## 1. 빅데이터 인프라 및 [[136_variance|분산]] 처리 시스템 (80개)
1. 빅데이터 3V / 5V - 볼륨([[001_bigdata_3v_5v|Volume]]), 속도(Velocity), 다양성(Variety), + 진실성(Veracity), 가치(Value)
2. [[002_structured_data|정형 데이터]] ([[002_structured_data|Structured Data]]) - RDBMS 테이블 같이 엄격한 [[005_schema|스키마]] 구조 보유
3. [[003_semi_structured_data|반정형 데이터]] ([[003_semi_structured_data|Semi-structured Data]]) - [[001_dikw_pyramid|데이터]] 내부(태그)에 구조([[012_metadata|메타데이터]])를 포함 (XML, [[343_json|JSON]], [[568_logs_distributed_logging_elk_fluentd|로그]])
4. [[004_unstructured_data|비정형 데이터]] ([[004_unstructured_data|Unstructured Data]]) - [[005_schema|스키마]]가 없는 텍스트, 음성, 비디오, 이미지 [[001_dikw_pyramid|데이터]]
5. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]], [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]]) - 전사적 관점의 [[282_business_intelligence_bi_technology_framework|비즈니스 인텔리전스]](BI)를 위한 통합/주제별/시계열 [[001_dikw_pyramid|데이터]] 저장소 ([[311_inmon|Inmon]] 모델)
6. [[209_data_mart_kimball_star_schema|데이터 마트]] ([[209_data_mart_kimball_star_schema|Data Mart]]) - 부서별(영업, 재무 등) 필요에 맞춘 소규모 분석 DB ([[312_kimball|Kimball]] 모델)
7. [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) - [[843_hadoop_rack_awareness_data_replication_topology|하둡]]/S3 등 저렴한 스토리지에 원시([[225_raw|Raw]]) 형태의 모든 비정형/[[002_structured_data|정형 데이터]]를 구조화 없이 무한 저장
8. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] ([[210_data_lakehouse_delta_lake|Data Lakehouse]]) - [[208_data_lake_schema_on_read|데이터 레이크]]의 유연성/저비용과 DW의 ACID [[191_transaction_concept_states|트랜잭션]], SQL [[282_performance_tactics|성능]]을 단일 계층에 결합한 현대 아키텍처 ([[074_photon_engine|Databricks]], [[541_cassandra|Snowflake]])
9. [[009_schema_on_read|스키마 온 리드]] ([[009_schema_on_read|Schema-on-Read]]) - 저장 시엔 원시 그대로 두고, [[298_qkv_attention|쿼리]](읽기)할 때 [[005_schema|스키마]]를 동적으로 부여 ([[208_data_lake_schema_on_read|데이터 레이크]])
[[489_raid_10_hybrid|10]]. [[010_schema_on_write|스키마 온 라이트]] ([[010_schema_on_write|Schema-on-Write]]) - 저장 전 [[093_normalization|정규화]]/ETL을 통해 [[005_schema|스키마]]에 맞게 정제 ([[209_data_warehouse_schema_on_write|DW]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[136_variance|분산]] 컴퓨팅 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] ([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) - 저가형 범용 x86 서버(Commodity Hardware) 대수를 늘려 [[282_performance_tactics|성능]] 무한 확장
12. [[012_apache_hadoop|아파치 하둡]] ([[012_apache_hadoop|Apache Hadoop]]) - 대용량 [[001_dikw_pyramid|데이터]] [[136_variance|분산]] 저장 및 [[430_index_fast_full_scan|병렬]] 처리 자바 [[191_oss_license_compliance|오픈소스]] 프레임워크 
13. [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]]) - 거대 [[501_file_definition_logical_record|파일]]을 기본 128MB 블록 단위로 쪼개 수많은 [[015_datanode|데이터노드]]에 [[136_variance|분산]] 저장
14. [[014_namenode|네임노드]] ([[014_namenode|NameNode]]) - [[501_file_definition_logical_record|파일]] [[506_directory_structure_symbol_table|디렉터리]], 블록 맵핑 [[203_metadata_management|메타데이터 관리]] [[075_kubernetes_k8s_cluster_architecture|마스터 노드]] ([[454_spof|SPOF]] 존재)
15. [[015_datanode|데이터노드]] ([[015_datanode|DataNode]]) - 실제 [[001_dikw_pyramid|데이터]]를 보관하는 수많은 워커 노드
16. [[016_replication_factor|복제]] ([[016_replication_factor|Replication]]) 계수 3 - 하드웨어 장애(고장)에 대비해 동일 블록을 서로 다른 랙(Rack) 서버에 3벌 복사하여 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) 달성
17. [[017_rack_awareness|랙 인지]] ([[017_rack_awareness|Rack Awareness]]) [[001_algorithm_definition|알고리즘]] - [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]] 시 물리적으로 동일한 [[238_switch_operation_principles|스위치]] 전원을 공유하는 랙에 전부 넣지 않고 [[136_variance|분산]] 배치
18. [[018_mapreduce|맵리듀스]] ([[018_mapreduce|MapReduce]]) - 디스크 I/O 기반 [[136_variance|분산]] [[430_index_fast_full_scan|병렬]] 연산 프레임워크 (Map: 매핑/필터링 -> Shuffle: [[001_dikw_pyramid|데이터]] 섞기 -> Reduce: 집계합산)
19. [[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]]) - 연산 코드를 [[001_dikw_pyramid|데이터]]가 이미 존재하는 노드로 전송하여 네트워크 전송 오버헤드 최소화 (연산 이동이 [[001_dikw_pyramid|데이터]] 이동보다 싸다)
20. [[020_yarn|YARN]] (Yet Another Resource Negotiator) - [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 2.0 클러스터 자원(CPU/Mem) 스케줄링 통합 관리자
21. [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]] ([[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]]) - [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[018_mapreduce|맵리듀스]]의 느린 디스크 반복 접근 단점을 극복한 인메모리(In-Memory) 기반 [[148_5g_embb_urllc_mmtc|초고속]] 범용 [[136_variance|분산]] 처리 엔진
22. [[310_audit|RDD]] ([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]]) - 스파크 핵심. 탄력적이고 불변하는 메모리 [[001_dikw_pyramid|데이터]] 구조. 장애 시 리니지(계보) 연산 기록을 바탕으로 즉시 자가 [[658_ir_recovery|복구]]
23. [[023_lazy_evaluation|지연 평가]] ([[023_lazy_evaluation|Lazy Evaluation]]) - 트랜스포메이션 연산(map, filter)은 즉시 실행 안하고 [[401_bayesian_network_dag_causality|DAG]] 궤적만 그리다가, 액션(count, save) 명령 시 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 묶어서 한 번에 최적 처리
24. [[215_flink_native_stream_watermark_window_time|아파치 플링크]] ([[215_flink_native_stream_watermark_window_time|Apache Flink]]) - 배치 모사가 아닌 네이티브 이벤트 기반 진정한 실시간 [[229_stream_processing_kafka_flink|스트림 처리]] 엔진 (상태 관리, [[085_watermark|워터마크]] 지원 우수)
25. [[214_kafka_pubsub_topic_partition_offset_broker|아파치 카프카]] ([[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]]) - [[136_variance|분산]] 이벤트 스트리밍 플랫폼 (Pub/Sub [[389_mesh_topology|메시]]지 큐), 고성능 [[568_logs_distributed_logging_elk_fluentd|로그]] [[123_pipe|파이프]]라인
26. 토픽(Topic)과 [[514_partition_slice_volume|파티션]]([[514_partition_slice_volume|Partition]]) - [[389_mesh_topology|메시]]지 저장 경로 / [[514_partition_slice_volume|파티션]] 분할을 통한 컨슈머 [[430_index_fast_full_scan|병렬]] [[136_variance|분산]] 처리 달성
27. 오프셋 (Offset) 보존 및 [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]] ([[191_consumer_group_kafka_partition_load_balancing|Consumer Group]]) 부하 분배 원리
28. 아파치 하이브 ([[028_apache_hive|Apache Hive]]) - [[018_mapreduce|맵리듀스]] 자바 코드 대신 HiveQL(SQL) [[298_qkv_attention|쿼리]]를 날려주는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] [[198_abstraction_control_data_process|추상화]]
29. 아파치 즈쿠퍼 ([[029_apache_zookeeper|Apache ZooKeeper]]) - [[136_variance|분산]] 클러스터 노드 상태 [[212_synchronization_mechanisms|동기화]], [[136_variance|분산]] 락, [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] 방지(리더 선출) 코디네이션
30. [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] ([[190_split_brain_zookeeper_fencing_quorum|Split Brain]]) 장애와 Quorum(정족수 과반 투표) 방어망 체계
31. 아파치 우지 ([[051_apache_oozie|Apache Oozie]]) / [[233_apache_airflow_dag_orchestration|아파치 에어플로우]] ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]]) - 복잡한 [[136_variance|분산]] [[123_pipe|파이프]]라인 작업 간 [[401_bayesian_network_dag_causality|DAG]] 의존성 스케줄링 관리
32. [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) - 기존 RDBMS(운영 DB)의 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[234_redo_roll_forward_durability_recovery|Redo]], Binlog)를 긁어내 DB [[282_performance_tactics|성능]] 부하 없이 실시간으로 [[179_kafka_flink_watermark_time_window|카프카]]나 DW에 변경/[[212_synchronization_mechanisms|동기화]] 시키는 [[001_dikw_pyramid|데이터]] 이관 핵심 기술 (Debezium)
33. [[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load) - 운영계에서 [[001_dikw_pyramid|데이터]] 추출 후 별도 서버에서 정제(T)하여 [[209_data_warehouse_schema_on_write|DW]] 적재(L) (병목 발생)
34. [[034_elt|ELT]] (Extract, Load, Transform) - 추출 [[001_dikw_pyramid|데이터]]를 바로 클라우드 [[209_data_warehouse_schema_on_write|DW]]([[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]])로 쏟아넣고, 클라우드 DB 연산력 자체를 이용해 그 안에서 SQL로 정제 변환 (현대 대세)
35. [[035_nosql|NoSQL]] ([[274_nosql|Not Only SQL]]) [[002_database_definition|데이터베이스]] 구조 유형 4가지
36. [[036_key_value|키-값 저장소]] (Key-Value) - [[542_redis|Redis]], Memcached (인메모리 [[148_5g_embb_urllc_mmtc|초고속]] [[160_session_controlling_terminal|세션]]/캐시)
37. [[237_document_store_mongodb_elasticsearch|도큐먼트 저장소]] ([[037_document|Document]]) - [[540_mongodb|MongoDB]] ([[343_json|JSON]] 형태 유연한 계층 저장, 부분 필드 검색 용이)
38. [[278_column_family_store|컬럼 패밀리 저장소]] (Wide-Column) - [[543_hbase|HBase]], [[541_cassandra|Cassandra]] (수십억 행의 시계열 로깅 [[001_dikw_pyramid|데이터]] [[289_cqrs_db|쓰기]] 최적화)
39. [[279_graph_store|그래프 저장소]] ([[039_graph_db|Graph DB]]) - Neo4j (노드와 엣지 [[083_relationship_in_er_model|관계]] 맵핑, 조인 오버헤드 없는 최단경로/추천 탐색)
40. [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) - [[136_variance|분산]] [[002_database_definition|데이터베이스]]는 [[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]]), [[452_availability|가용성]]([[452_availability|Availability]]), [[514_partition_slice_volume|파티션]] 감내([[514_partition_slice_volume|Partition]] Tolerance) 세 가지를 동시에 완벽히 만족할 수 없음 (P는 필수이므로 [[086_CP_순환_전치_GI|CP]] 또는 [[572_ap_access_point_ds_distribution_system|AP]] 모델 선택)
41. [[342_pacelc|PACELC]] 정리 - 장애(P) 시 A와 C의 상충, 정상(E) 시 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])과 [[194_consistency_database_integrity|일관성]](C)의 상충 [[083_relationship_in_er_model|관계]] 확장 정리
42. BASE 특성 - ACID의 반대 개념. [[035_nosql|NoSQL]] 특성으로 Basically Available, Soft-state, Eventually Consistent(일정 시간 지나면 결국 [[212_synchronization_mechanisms|동기화]]됨)
43. [[095_lambda_architecture|람다 아키텍처]] ([[095_lambda_architecture|Lambda Architecture]]) - 빅데이터 처리 시 과거 배치는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]](Batch Layer)으로, 실시간 처리는 스트리밍([[092_GPT_NLP|Speed Layer]])으로 듀얼 구축하여 뷰에서 합치는 모델 (복잡성 증가 단점)
44. [[096_kappa_architecture|카파 아키텍처]] ([[096_kappa_architecture|Kappa Architecture]]) - [[216_lambda_kappa_architecture_batch_realtime|람다]] 단점 극복, 배치 레이어를 버리고 과거/실시간 모든 [[001_dikw_pyramid|데이터]]를 [[179_kafka_flink_watermark_time_window|카프카]] 기반 단일 스트림 계층으로 통일 처리
45. 컬럼 지향 저장소 ([[234_columnar_storage_parquet_orc|Columnar Storage]]) 포맷 - RDB처럼 로우(행) 단위 저장이 아니라, 컬럼(열) 단위로 [[347_compaction|압축]] 보관 (Apache [[178_parquet_rle_encoding_columnar_compression|Parquet]], ORC). [[316_olap|OLAP]] [[298_qkv_attention|쿼리]] 시 불필요한 필드는 디스크에서 읽지 않아 [[282_performance_tactics|성능]] 극대화
46. LSM 트리 ([[221_lsm_tree_memtable_sequential_flush_compaction|Log-Structured Merge-Tree]]) - [[299_data_lake|카산드라]], RocksDB 스토리지 코어 엔진. 디스크 랜덤 [[289_cqrs_db|쓰기]] 병목을 막기 위해 [[494_memtable_sstable_flush|멤테이블]](Memory)에 순차 기록 후 꽉 차면 SS테이블로 디스크 순차 플러시(Flush) ([[289_cqrs_db|쓰기]] 속도 극대화)
47. [[378_lsm_compaction_tombstone|콤팩션]] ([[347_compaction|Compaction]])과 [[300_schema_on_write_vs_read|툼스톤]] ([[300_schema_on_write_vs_read|Tombstone]]) - 디스크 파편화 병합 및 삭제 [[186_character_stuffing_dle_stx_etx|플래그]](비석) 처리 기법
48. [[244_consistent_hashing_ring_distribution|컨시스턴트 해싱]] ([[244_consistent_hashing_ring_distribution|Consistent Hashing]]) - DB 노드 증설/삭제 시 전체 [[001_dikw_pyramid|데이터]] 리밸런싱 해시 이동을 최소화하는 원형 링(Ring) 분할 구조
49. [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) - [[001_dikw_pyramid|데이터]] 인프라 조직론 혁신. 사일로화된 중앙 집중식 [[001_dikw_pyramid|데이터]]팀 구조를 타파하고, 각 현업 [[064_relation_domain|도메인]] 부서가 [[136_variance|분산]] 오너십을 갖고 '[[001_dikw_pyramid|데이터]]를 하나의 독립 프로덕트'로 직접 제공
50. [[212_data_fabric_virtualization|데이터 패브릭]] ([[212_data_fabric_virtualization|Data Fabric]]) - 물리적으로 흩어진 [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] DB 사일로들을 [[016_replication_factor|복제]]/이동([[215_etl_vs_elt_pipeline|ETL]]) 없이, 지능화된 [[190_ai_llm_requirements_specification|AI]] [[012_metadata|메타데이터]] [[015_virtualization|가상화]] 계층([[247_data_virtualization_federated_query|Data Virtualization]])으로 연결해 실시간 단일 뷰로 활용하는 아키텍처
51. [[213_data_catalog_metadata|데이터 카탈로그]] ([[213_data_catalog_metadata|Data Catalog]]) - [[012_metadata|메타데이터]]를 통합 수집/태깅하여 분석가들이 [[001_dikw_pyramid|데이터]]를 구글처럼 쉽게 검색([[001_dikw_pyramid|Data]] Discovery)하고 권한을 통제하는 시스템 (AWS Glue, Amundsen)
52. [[214_data_lineage_tracking|데이터 리니지]] ([[214_data_lineage_tracking|Data Lineage]]) - [[001_dikw_pyramid|데이터]]의 출처 소스부터 전처리 단계, 최종 타겟 대시보드까지의 [[001_dikw_pyramid|데이터]] 흐름과 변환 이력을 족보처럼 시각적으로 추적하는 체계 (규제 [[606_auditing_linux_auditd|감사]], 영향도 분석 핵심)
53. [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]] ([[324_dataops|DataOps]]) - [[645_data_pipeline_acceleration|데이터 파이프라인]] 개발에 [[652_devops_calms_culture|DevOps]] 사상 적용. 품질 테스트 자동화([[090_configuration_item|CI]]/CD), 코드로서의 [[123_pipe|파이프]]라인 [[317_versioning_data_model_design|버저닝]] 관리 (dbt 툴 등 활용)
54. [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] ([[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]], [[149_apache_hudi|Apache Hudi]]) - [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]를 완성하는 핵심 계층. [[178_parquet_rle_encoding_columnar_compression|파케이]] [[501_file_definition_logical_record|파일]] 덩어리 위에 RDB 수준의 [[191_transaction_concept_states|트랜잭션]](ACID) 제어, 타임트래블([[022_snapshot_backup_architecture|스냅샷]] [[098_rollback_strategy_pipeline_error_threshold|롤백]]), [[005_schema|스키마]] 에볼루션 기능 부여
55. [[293_storage_compute_separation|스토리지와 컴퓨팅의 분리]] (Separation of Compute and Storage) 클라우드 [[209_data_warehouse_schema_on_write|DW]] [[249_scaling_normalization_standardization|스케일링]] 특성
56. [[360_data_virtualization|데이터 가상화]] [[195_federated_query_data_fabric_distributed_join|연방 쿼리]] ([[195_federated_query_data_fabric_distributed_join|Federated Query]]) 엔진 (Trino, Presto)
57. [[057_tsdb_downsampling_retention_policy|시계열 데이터베이스]] 다운샘플링 (Downsampling) 보존 [[164_policy|정책]] ([[515_mvcc|Retention]])
58. [[058_newsql_google_spanner_truetime_distributed_transaction|뉴에스큐엘]] ([[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]]) 글로벌 스패너 (Spanner) 트루타임 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 융합
59. [[061_bloomfilter|블룸 필터]] ([[061_bloomfilter|Bloom Filter]]) 디스크 랜덤 I/O 긍정 오류 배제 [[130_probability|확률]]망 검색 
60. [[062_darkdata|다크 데이터]] ([[062_darkdata|Dark Data]]) 발굴 자산화 및 프라이버시 클린 룸 [[602_sandboxing_kernel_wrapper|샌드박싱]] 결합망

## 2. [[001_dikw_pyramid|데이터]] 분석 수학, 통계 및 [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] (60개)
61. [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] ([[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]]) 프레임워크 - [[225_kdd_t_test_anova_statistical_analysis|KDD]] (지식 탐색 프로세스: 선택->전처리->변환->마이닝->해석), CRISP-DM 모델
62. [[062_eda_exploratory_data_analysis|탐색적 데이터 분석]] ([[064_eda|EDA]], [[105_exploratory_data_analysis|Exploratory Data Analysis]]) - 가설 수립 전 [[001_dikw_pyramid|데이터]]의 패턴, [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]], 통계적 특성을 [[003_bigdata_7v|시각화]]/요약하여 통찰 도출
63. [[063_central_tendency_dispersion_variance_iqr|중심 경향도]] (평균, 중앙값, 최빈값) / 산포도 ([[136_variance|분산]], 표준편차, 사분위수 범위 IQR)
64. [[064_skewness_kurtosis_log_transformation|왜도]] ([[064_skewness_kurtosis_log_transformation|Skewness]] / 비대칭 쏠림) / 첨도 (Kurtosis / 꼬리 두께 뾰족함)
65. [[065_pearson_correlation_coefficient_multicollinearity|피어슨 상관 계수]] ([[226_pearson_correlation_regression_r2_vif_multicollinearity|Pearson Correlation]] Coefficient) - 두 연속형 변수 간의 선형적 비례 [[083_relationship_in_er_model|관계]] 측정 (-1.0 ~ 1.0)
66. 스피어만 순위 상관 계수 ([[066_spearman_rank_correlation_nonparametric_robustness|Spearman Rank Correlation]]) - 서열/비선형적 비모수 [[325_correlation_analysis_pearson_spearman|상관 분석]]
67. [[145_hypothesis_testing|가설 검정]] 프로세스 - 귀무 가설([[067_hypothesis_testing_null_alternative_p_value|H0]], 차이/효과 없음) vs 대립 가설(H1, 차이 입증)
68. [[068_significance_level_alpha_p_value_hypothesis|유의 수준]] ([[068_significance_level_alpha_p_value_hypothesis|Alpha]]) 과 [[337_p_value_significance|유의 확률]] ([[337_p_value_significance|p-value]]) - [[337_p_value_significance|p-value]] < 0.05 이면 우연히 일어날 [[130_probability|확률]]이 극히 적으므로 귀무 가설 기각(유의미함)
69. 1종 오류 (참인 [[067_hypothesis_testing_null_alternative_p_value|H0]] 기각) / 2종 오류 (거짓인 [[067_hypothesis_testing_null_alternative_p_value|H0]] 기각 실패) / 검정력 ([[069_type_1_2_error_statistical_power|Power]])
70. T-검정 ([[070_t_test_independent_paired_mean_difference|t-Test]]) - 두 집단 간 평균 차이 통계적 [[395_verification_process_review|검증]] (독립 표본, 대응 표본)
71. [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] ([[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]]) - 3개 이상 다수 집단 간 평균 차이 [[395_verification_process_review|검증]] (F-분포 활용)
72. [[147_chi_square_test|카이제곱 검정]] ([[147_chi_square_test|Chi-square Test]]) - 범주형 명목 [[001_dikw_pyramid|데이터]]의 독립성/적합성 [[395_verification_process_review|검증]] (교차 분석)
73. [[139_clt|중심 극한 정리]] ([[139_clt|CLT]], Central Limit Theorem) - 모집단 분포와 상관없이 표본의 크기(n)가 30 이상 크면 표본 평균의 분포는 [[138_normal_distribution|정규 분포]](종 모양)를 따른다는 통계학 대원칙
74. [[074_law_of_large_numbers_lln_convergence_probability|대수의 법칙]] (Law of Large Numbers) - 시행을 무한히 반복하면 표본 평균이 모평균에 수렴
75. [[132_conditional_probability|조건부 확률]] ([[132_conditional_probability|Conditional Probability]]) 및 베이즈 정리 (Bayes' Theorem) 사후 [[130_probability|확률]] 계산
76. [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] ([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]]) 탐지 기법 - IQR 1.5배 벗어남, Z-Score 3 이상, [[351_dbscan_density_based_clustering|DBSCAN]], [[195_isolation_concurrency_control|Isolation]] Forest [[001_algorithm_definition|알고리즘]]
77. 결측치 (Missing Value) 처리 기법 - 단순 삭제, 평균/중앙값 대치, 다중 대치법(MICE), [[352_knn_distance_metrics|K-NN]] 대치 보간
78. [[001_dikw_pyramid|데이터]] [[249_scaling_normalization_standardization|스케일링]] - [[093_normalization|정규화]] ([[093_normalization|Normalization]] / [[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]] 0~1 매핑), 표준화 (Standardization / 평균 0 [[136_variance|분산]] 1 Z-Score 치환) (거리 기반 [[001_algorithm_definition|알고리즘]] [[352_knn_distance_metrics|K-NN]], [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 필수 전처리)
79. [[079_one_hot_encoding_categorical_dummy_variable|원-핫 인코딩]] ([[079_one_hot_encoding_categorical_dummy_variable|One-hot Encoding]]) - 범주형 문자를 기계가 인식하도록 0과 1 희소 벡터 [[055_array|배열]]로 [[330_dummy_variable|더미 변수]]([[330_dummy_variable|Dummy Variable]])화
80. [[080_multicollinearity_vif_variance_inflation_factor_regression|다중 공선성]] ([[080_multicollinearity_vif_variance_inflation_factor_regression|Multicollinearity]]) 문제 - [[149_regression_analysis|회귀 분석]] 시 독립변수들끼리 너무 강한 상관관계를 가져 회귀 계수(기여도)가 왜곡되는 현상 (VIF [[136_variance|분산]] 팽창 지수 [[489_raid_10_hybrid|10]] 이상 시 변수 축소)
81. [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] ([[079_dimensionality_reduction|Dimensionality Reduction]]) - [[338_pca_principal_component_analysis|주성분 분석]] ([[163_pca|PCA]], [[163_pca|Principal Component Analysis]]), 변수의 [[136_variance|분산]](정보량)을 최대로 보존하는 직교 축 도출 변환 ([[341_eigenvalue_decomposition|고유값 분해]] 활용)
82. [[082_lda_linear_discriminant_analysis_classification|선형 판별 분석]] (LDA) - 클래스 간 [[136_variance|분산]] 최대화, 내 [[136_variance|분산]] 최소화 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] ([[121_supervised_learning|지도 학습]])
83. [[083_association_rule_apriori_market_basket|연관 규칙 탐색]] ([[083_association_rule_apriori_market_basket|Association Rule]]) - [[107_market_basket_analysis|장바구니 분석]] (기저귀와 맥주), Apriori [[001_algorithm_definition|알고리즘]]
84. [[084_support_association_rule_transaction|지지도]] ([[084_support_association_rule_transaction|Support]]) - 전체 거래 중 A와 B가 동시에 포함된 거래 비율
85. [[085_confidence_association_rule_conditional_probability|신뢰도]] ([[085_confidence_association_rule_conditional_probability|Confidence]]) - A를 구매한 거래 중 B도 함께 구매한 [[132_conditional_probability|조건부 확률]] 비율
86. [[086_lift_association_rule_marketing|향상도]] ([[086_lift_association_rule_marketing|Lift]]) - 우연적 구매를 배제한, A 구매가 B 구매를 얼마나 끌어올리는지 실제 효과 ([[086_lift_association_rule_marketing|Lift]] > 1 이면 유의미)
87. [[293_fp_function_point|FP]]-Growth [[001_algorithm_definition|알고리즘]] - Apriori의 반복 DB 스캔 속도 한계를 타파한 트리(Tree) 구조 빈발 항목 탐색법
88. [[088_k_fold_cross_validation_overfitting_generalization|머신러닝 교차 검증]] ([[088_k_fold_cross_validation_overfitting_generalization|K-Fold Cross Validation]]) - 훈련 [[001_dikw_pyramid|데이터]]를 K개 조각으로 나누어 학습/[[395_verification_process_review|검증]]을 교대로 반복 평가하여 과적합([[245_overfitting_variance|Overfitting]]) 방지 및 일반화 [[395_verification_process_review|검증]]
89. [[241_machine_learning_basics|머신러닝]] 평가 지표 [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] ([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]]) - TP, [[293_fp_function_point|FP]], FN, TN 분할 통계표
90. 정확도 (Accuracy) - 전체 모수 중 1과 0을 모두 맞춘 정답 비율 (암 환자 [[001_dikw_pyramid|데이터]] 등 심한 불균형 Data에서는 왜곡 함정 발생)
91. [[233_precision_recall_f1_roc_auc_threshold|정밀도]] ([[233_precision_recall_f1_roc_auc_threshold|Precision]]) - 모델이 "양성(Positive)"으로 예측한 것 중에 실제 양성의 비율 ([[293_fp_function_point|FP]] 억제가 중요할 때, 스팸 필터링)
92. [[092_recall_sensitivity_hit_rate|재현율]] ([[254_recall_sensitivity|Recall]] / 민감도) - 실제 "양성"인 [[001_dikw_pyramid|데이터]] 전체 중에서 모델이 놓치지 않고 찾아낸 양성의 비율 (FN 억제가 중요할 때, 암 진단/불량 탐지)
93. [[255_f1_score|F1-Score]] - [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]의 조화 평균 (불균형 [[001_dikw_pyramid|데이터]] 평가 제1지표)
94. ROC 곡선 (Receiver Operating Characteristic) - [[104_classification_analysis|분류]] 모델 [[431_ssthresh_slow_start_threshold|임계치]] 변화에 따른 FPR(위양성률) 대비 TPR([[092_recall_sensitivity_hit_rate|재현율]]) [[070_graph_datastructure|그래프]] 모형
95. AUC (Area Under Curve) - ROC 곡선 아래 넓이 척도 (1.0에 가까울수록 완벽한 모델)
96. [[096_oversampling_smote|불균형 데이터 증강]] ([[096_oversampling_smote|Oversampling]]) - [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] (Synthetic Minority Over-sampling Technique) [[001_algorithm_definition|알고리즘]] ([[352_knn_distance_metrics|K-NN]] 이웃 선형 보간 기반 가상 [[818_synthetic_data|합성 데이터]] [[087_process_state_transition|생성]]망)
97. [[097_regression_metrics_mse_rmse_mae|회귀 분석 지표]] - [[076_mse_mean_squared_error_regression|MSE]] (평균 제곱 오차), RMSE (루트 보정), MAE (절대값 오차) 
98. [[098_coefficient_of_determination_r_squared|결정 계수]] (R-Squared, R^2) - 0~1 사이값, 독립변수가 종속변수의 변동([[136_variance|Variance]])을 얼마나 완벽히 설명하는가 ([[316_ssr_vs_csr|SSR]]/SST) 모델 설명력
99. A/B 테스트 검정력 ([[069_type_1_2_error_statistical_power|Power]]) 설계 및 [[337_p_value_significance|p-value]] 해킹 통계 조작 한계 
100. K-Means [[105_clustering_analysis|군집화]] ([[105_clustering_analysis|Clustering]]) 엘보우 (Elbow) 기법 및 실루엣 (Silhouette) 스코어 클러스터 [[193_cohesion_levels|응집도]] 밀도 측정 함수
101. [[264_naive_bayes|나이브 베이즈]] [[104_classification_analysis|분류]] ([[078_Naive_Bayes|Naive Bayes]]) 조건부 독립 [[350_laplace_smoothing|라플라스 스무딩]] 결합
102. [[102_lasso_ridge_regression_regularization|회귀 라쏘]] ([[102_lasso_ridge_regression_regularization|Lasso]] / L1) 및 릿지 (Ridge / L2) 패널티 [[093_normalization|정규화]] 식 파싱
103. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] [[268_sigmoid_vanishing_gradient|시그모이드]] [[104_classification_analysis|분류]] 로짓 곡선 함수
104. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] 선형 [[104_classification_analysis|분류]] [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 마진 튜브 서포트 벡터 내적 
105. [[232_tfidf_cosine_similarity_text_embedding_confusion_matrix|TF-IDF]] 및 [[109_text_mining|텍스트 마이닝]] [[359_cosine_similarity|코사인 유사도]] 벡터 탐색
106. [[106_mahalanobis_distance|마할라노비스 거리]] 통계 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 파악
107. [[107_tensorflow_array_tensor|텐서플로우 배열]] 스칼라 벡터 차원 수학
108. [[108_gini_impurity|지니 불순도]] 정보 이득 트리 분할 [[136_variance|분산]] 
109. 유클리드 거리 L2, 맨해튼 거리 L1 측정 
110. 편향 [[136_variance|분산]] 트레이드 오프 오버피팅 언더피팅 
111. [[140_markov_chain|마르코프 체인]] 시간 전이 행렬 시계열 
112. 로버스트 (Robust) 중앙값 절사 평균 
113. 다차원 표면 매니폴드 가정 매핑 
114. [[114_gaussian_mixture_model|가우시안 혼합 모델]] [[360_gmm_em_algorithm|GMM]] EM 
115. 밀도 군집 [[351_dbscan_density_based_clustering|DBSCAN]] 노이즈 [[655_ir_detection_analysis|식별]] 
116. [[116_kernel_density_estimation|커널 밀도 추정]] KDE 스무딩 
117. 베이즈 오류 최저 한계 
118. 정보 이론 교차 [[151_entropy|엔트로피]] KLD 발산 
119. [[257_ensemble_learning|앙상블]] 조합 [[258_voting_ensemble|보팅]] 통계망 
120. [[127_boosting|부스팅]] 경사 하강 수치 오차 보완

## 3. [[241_machine_learning_basics|머신러닝]]/딥러닝 [[001_algorithm_definition|알고리즘]] 및 초거대 [[190_ai_llm_requirements_specification|AI]] ([[263_llm_large_language_model|LLM]]) 트렌드 (60개)
121. [[121_supervised_learning|지도 학습]] ([[121_supervised_learning|Supervised Learning]]) - 정답(Label)이 달린 [[001_dikw_pyramid|데이터]]를 입력하여 회귀/[[104_classification_analysis|분류]] 모델 훈련
122. [[122_unsupervised_learning|비지도 학습]] ([[122_unsupervised_learning|Unsupervised Learning]]) - 정답 없이 [[001_dikw_pyramid|데이터]] 자체의 숨겨진 패턴, 군집, [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 연산
123. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] ([[094_reinforcement_learning|Reinforcement Learning]]) - 시뮬레이션 환경([[463_markov_decision_process_mdp|MDP]])에서 에이전트가 행동을 취하고 보상(Reward)을 최대화하는 방향으로 시행착오 학습 ([[316_q_learning|Q-Learning]])
124. 결정 트리 ([[124_decision_tree|Decision Tree]]) - 스무고개 하듯 조건 분기 트리 [[087_process_state_transition|생성]] (정보 이득 극대화, 과적합 위험 높음)
125. [[125_ensemble_learning|앙상블 학습]] ([[125_ensemble_learning|Ensemble Learning]]) - 여러 약한 [[104_classification_analysis|분류]]기를 묶어 [[282_performance_tactics|성능]]과 일반화 극대화
126. [[259_bagging_random_forest|배깅]] ([[259_bagging_random_forest|Bagging]], Bootstrap Aggregating) - 훈련 [[001_dikw_pyramid|데이터]]를 랜덤 복원 추출(Bootstrap)해 여러 모델을 [[430_index_fast_full_scan|병렬]] [[430_index_fast_full_scan|병렬]] 학습 후 다수결 ([[353_random_forest|Random Forest]], [[136_variance|분산]] 감소 효과)
127. [[127_boosting|부스팅]] ([[127_boosting|Boosting]]) - 순차적 [[149_serial_communication_rs232_rs485|직렬]] 학습, 이전 트리가 틀린 [[001_dikw_pyramid|데이터]]에 [[267_weight_bias_activation|가중치]] 페널티를 주어 다음 트리가 보완 학습 ([[034_gradient_boosting|Gradient Boosting]], XGBoost, LightGBM, 편향 감소 효과 극대화)
128. [[061_artificial_neural_network_ann_neuron_model|인공 신경망]] ([[350_ann|ANN]]) [[266_mlp_hidden_layers|다층 퍼셉트론]] (MLP) 비선형 은닉층 아키텍처
129. [[129_activation_function|활성화 함수]] ([[129_activation_function|Activation Function]]) - 선형 덧셈 값을 비선형으로 구부려 복잡한 차원을 해석하게 만듦 ([[268_sigmoid_vanishing_gradient|Sigmoid]], [[070_hyperbolic_tangent_tanh_activation|Tanh]], [[269_relu_activation|ReLU]])
130. [[269_relu_activation|ReLU]] ([[269_relu_activation|Rectified Linear Unit]]) 함수 - 양수면 자기 자신, 음수면 0. 기존 Sigmoid가 [[272_backpropagation|역전파]] 시 발생시키던 '[[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]])' 문제를 해결한 딥러닝 부흥의 1등 공신
131. [[075_loss_function_cost_function|손실 함수]] ([[087_loss_function|Loss Function]]) 및 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]]) [[275_gradient_descent_sgd|경사 하강법]] ([[165_gradient_descent|Gradient Descent]])
132. [[277_adam_optimizer|Adam]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] - [[276_momentum_optimizer|모멘텀]](관성) 방향 가속과 RMSProp(적응형 스텝폭 축소)을 융합한 최신 수리 최적화 표준
133. [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) 연쇄 미분 오차 전달 
134. 규제([[134_regularization_dropout_batch_norm|Regularization]]) [[278_regularization_overview|과적합 방지 기법]] - [[267_weight_bias_activation|가중치]] 감쇠(L1/L2), [[280_dropout|드롭아웃]]([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]], 임의 뉴런 제거), [[281_early_stopping|조기 종료]]([[281_early_stopping|Early Stopping]]), [[282_batch_normalization|배치 정규화]]([[282_batch_normalization|Batch Normalization]])
135. [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] ([[089_CNN_Convolutional|합성곱 신경망]]) - 이미지 인식 특화. [[096_convolution_layer_filter_stride_padding|합성곱 층]]([[022_kernel_role|커널]] 필터 이동, 특성맵 추출) + [[100_pooling_layer_max_pooling_downsampling_cnn|풀링 층]](해상도 [[347_compaction|압축]], 공간 불변성 확보)으로 구성
136. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] ([[111_rnn_recurrent_neural_network_sequential_data|순환 신경망]]) - 텍스트/음성 등 순서(시퀀스)가 있는 시계열 [[001_dikw_pyramid|데이터]]. 이전 은닉 상태(과거 정보)가 다음 텐서 입력으로 순환
137. [[292_lstm|LSTM]] (장단기 메모리) / [[294_gru|GRU]] - [[111_rnn_recurrent_neural_network_sequential_data|순환 신경망]]이 길어질수록 과거 정보를 까먹는([[291_long_term_dependency|장기 의존성]]) 문제를 해결하기 위해 '셀 상태 컨베이어 벨트'와 게이트(망각, 입력, 출력) 구조 부착
138. [[296_attention_mechanism|어텐션 메커니즘]] (Attention) - 고정된 길이 [[347_compaction|압축]] 병목([[120_context_vector|Context Vector]])의 한계를 깨고, [[039_decoder|디코더]]가 매 단어 출력 시마다 [[040_encoder|인코더]] 입력 문장 전체 중 '가장 연관도([[267_weight_bias_activation|가중치]])가 높은 단어'를 동적으로 다시 들여다보게 하는 혁신적 수리 텐서 매핑 
139. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] ([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 아키텍처 (2017) - RNN과 CNN을 아예 버리고 오직 '어텐션 [[430_index_fast_full_scan|병렬]] 연산'만으로 모델을 구성하여 훈련 속도를 지수적으로 폭발시킴 (초거대 [[190_ai_llm_requirements_specification|AI]] 탄생의 시발점)
140. 셀프 어텐션 ([[124_self_attention|Self-Attention]]) / [[299_multi_head_attention|멀티 헤드 어텐션]] / [[300_positional_encoding|포지셔널 인코딩]](위치 정보 주입) 구조체
141. [[301_bert_mlm|BERT]] - [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]의 '[[040_encoder|인코더]]'만 채용, 텍스트 양방향 문맥을 완벽히 이해해 빈칸 채우기([[138_mlm_learning|MLM]]) 등 언어 이해 [[104_classification_analysis|분류]]에 최적 (구글)
142. [[302_gpt_autoregressive|GPT]] - [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]의 '[[039_decoder|디코더]]'만 채용, 과거 단어 [[033_context|컨텍스트]]를 보고 그 다음 올 단어 [[130_probability|확률]]을 자동 회귀([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]) [[087_process_state_transition|생성]] 예측에 최적 (OpenAI)
143. [[225_foundation_model_peft_lora|파운데이션 모델]] ([[225_foundation_model_peft_lora|Foundation Model]]) - 초거대 파라미터(수백억~수천억) 모델을 테라바이트급 무라벨 원시 텍스트로 사전 자기지도 학습(Pre-[[588_mlops_pipeline_automation|training]])시켜, 세상 지식의 범용 베이스를 구축한 기본 엔진 (Llama, Claude 등)
144. [[133_fine_tuning|미세 조정]] ([[304_fine_tuning|Fine-Tuning]] / [[304_fine_tuning|파인 튜닝]]) 및 [[132_transfer_learning|전이 학습]] - 범용 사전 학습 모델 [[267_weight_bias_activation|가중치]]를 기반으로 특정 [[064_relation_domain|도메인]](법률, 의학) [[001_dikw_pyramid|데이터]]셋을 소량 추가 훈련시켜 목적에 맞게 전이
145. 파라미터 효율적 [[133_fine_tuning|미세 조정]] ([[306_peft_lora|PEFT]]) 및 [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] ([[145_peft_lora_low_rank_adaptation|Low-Rank Adaptation]]) 기법 - 초거대 모델 전체 [[267_weight_bias_activation|가중치]]를 훈련하려면 막대한 VRAM 메모리가 필요하므로, 기존 뼈대는 얼리고(Freeze) 저차원 분해 행렬 [[259_adapter_pattern_interface_wrapper|어댑터]]만 삽입해 훈련 후 병합하는 최적 파인튜닝 가속 기술
146. [[434_quantization|양자화]] ([[434_quantization|Quantization]] / [[404_qlora|QLoRA]]) 모델 경량화 - [[087_floating_point|부동소수점]] FP32 파라미터를 INT8, INT4 등 정수로 [[347_compaction|압축]]하여 모바일/온디바이스(엣지)에 배포 구동 가능화
147. [[147_instruction_tuning_rlhf_alignment|인스트럭션 튜닝]] ([[147_instruction_tuning_rlhf_alignment|Instruction Tuning]]) - 기본 모델을 "질문-답변" 지시어 포맷에 찰떡같이 응답하도록 대화형 특화 추가 훈련 
148. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] (인간 피드백 기반 강화학습) - LLM이 내뱉는 윤리 위반 텍스트를 막기 위해, 인간이 "더 유용한 답변"에 랭킹을 매긴 리워드 모델([[403_rlhf_reward_model|Reward Model]])을 통과시켜 [[395_ppo_clipping|PPO]] 강화학습으로 모델 행동을 통제 정렬(Alignment) 
149. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]] ([[224_prompt_engineering_guideline|Prompt Engineering]]) - 제로샷, 퓨샷(Few-shot), Chain of Thought (사고 사슬, 단계별 [[369_logic_bomb|논리]] 추론 유도) 
150. [[251_hallucination_rag_augmented_retrieval_vector_db|할루시네이션]] ([[345_llm_foundation_model_hallucination|Hallucination]] / [[275_react_framework|환각]]) 및 [[276_fine_tuning|RAG]] ([[222_rag_retrieval_augmented_generation|검색 증강 생성]]) 아키텍처 - LLM의 가장 큰 취약점인 '거짓말'을 막기 위해, 기업 프라이빗 DB를 벡터 DB로 구축해놓고 유저 질문 시 검색된 실제 팩트 문서 문단을 프롬프트에 주입(Augment)하여 정답 [[087_process_state_transition|생성]]망 유도
151. [[223_vector_database_embedding|벡터 데이터베이스]] ([[151_vector_database_embedding_ann_search|Vector DB]], Pinecone/[[320_gnn_vector_db_recommendation|Milvus]]) - 비정형 문자열을 [[278_instruction_tuning|임베딩]] 텐서 좌표로 변환 저장하고 [[359_cosine_similarity|코사인 유사도]]([[350_ann|ANN]]: [[351_hnsw|HNSW]], IVFFlat)로 근접 문서 고속 검색 프레임워크 
152. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) 교사 학생 모델 [[347_compaction|압축]] 경량 전이 
153. [[153_diffusion_model_stable_diffusion_denoising|디퓨전 모델]] (Diffusion) 이미지 [[087_process_state_transition|생성]] [[190_ai_llm_requirements_specification|AI]] 역노이즈 파괴 복원망 (Stable Diffusion, Midjourney)
154. [[159_gan|생성적 적대 신경망]] ([[154_gan_generative_adversarial_network|GAN]]) 위조 경찰 적대 통계 보정 
155. [[190_ai_llm_requirements_specification|AI]] 에이전트 ([[155_ai_agents_function_calling_agentic_loop|AI Agents]]) 도구 [[294_function_calling_tool_use|함수 호출]] (Function Calling) 자동 과업 루프 목표 달성망 
156. [[211_recommendation_system|추천 시스템]] 딥러닝 팩토라이제이션 머신 (DeepFM) 
157. 시계열 예측 딥러닝 TCN [[430_index_fast_full_scan|병렬]] [[228_cnn_1d_2d_3d_video_medical|합성곱]] 필터 변환망 
158. [[158_multimodal_clip_vision_audio_encoding|멀티모달]] ([[158_multimodal_clip_vision_audio_encoding|Multimodal]]) 비전 오디오 동시 인코딩 [[278_instruction_tuning|임베딩]] [[312_clip_contrastive_learning|클립]] ([[408_clip|CLIP]]) 대조 학습 모델망 
159. [[159_gnn_graph_neural_network_message_passing|GNN]] [[070_graph_datastructure|그래프]] 노드 구조 [[389_mesh_topology|메시]]지 패싱 네트워크 
160. [[160_knowledge_graph_graphrag_integration|지식 그래프]] 연계 [[530_graph_rag|GraphRAG]] 연동망 체제 설계

## 4. [[348_mlops|MLOps]] [[123_pipe|파이프]]라인 및 [[001_dikw_pyramid|데이터]] 분석 엔지니어링 (60개)
161. [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) - [[190_ai_llm_requirements_specification|AI]] 모델 개발(Jupyter 노트북 랩)과 실제 프로덕션 서버 운영(서빙) 간의 단절을 타파하고, [[090_configuration_item|CI]]/CD 배포 자동화를 [[001_dikw_pyramid|데이터]]/[[190_ai_llm_requirements_specification|AI]] [[123_pipe|파이프]]라인 전 주기에 접목한 공학 체계
162. [[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]], 지속적 훈련) [[123_pipe|파이프]]라인 - 모델 [[282_performance_tactics|성능]] 저하가 감지되면 자동으로 재학습 사이클을 [[507_acid_properties|트리거]] 
163. [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] ([[163_data_drift_statistical_distribution_shift|Data Drift]]) - [[067_service_operation|서비스 운영]] 중 유입되는 새로운 사용자 입력 [[001_dikw_pyramid|데이터]]의 통계적 분포(평균, 편차)가 훈련 [[001_dikw_pyramid|데이터]] 분포와 심하게 이격되는 현상 (정확도 하락 원인)
164. [[164_concept_drift_target_mapping_change|컨셉 드리프트]] ([[164_concept_drift_target_mapping_change|Concept Drift]]) - [[001_dikw_pyramid|데이터]] 자체는 같으나, "개=1, 고양이=0" 식의 타겟 정답 맵핑 규칙(세상의 트렌드) 자체가 뒤바뀌어버리는 현상
165. [[165_feature_store_training_serving_consistency|피처 스토어]] ([[165_feature_store_training_serving_consistency|Feature Store]]) - 전처리([[093_normalization|정규화]]/결측치 처리)가 끝난 [[241_machine_learning_basics|머신러닝]] 변수 셋을 중앙 집중 관리하여, 오프라인 훈련 팀과 온라인 서빙 [[014_api_posix|API]] 간의 [[247_feature_label_variables|피처]] 불일치([[588_mlops_pipeline_automation|Training]]-Serving Skew)를 방지하는 실시간 캐시 DB 인프라
166. [[166_model_registry_versioning_mlflow|모델 레지스트리]] ([[166_model_registry_versioning_mlflow|Model Registry]]) - 학습 완료 모델 바이너리 [[267_weight_bias_activation|가중치]] 덤프, 하이퍼파라미터 이력, [[012_metadata|메타데이터]] [[288_version_ihl_tos_total_length|버전]] 관리 창고 ([[180_mlflow|MLflow]], W&B)
167. [[167_kubeflow_kubernetes_ml_pipeline|쿠브플로우]] ([[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]]) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[561_container_based_deployment|컨테이너]] 기반 딥러닝 [[136_variance|분산]] 학습, [[123_pipe|파이프]]라인 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼
168. [[645_data_pipeline_acceleration|데이터 파이프라인]] 워크플로우 [[401_bayesian_network_dag_causality|DAG]] 제어 ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]]) 자동화
169. [[169_model_serving_engine_triton_tensorflow_serving|모델 서빙 엔진]] - [[156_rest_representational_state_transfer|REST]]/[[479_grpc_protobuf_http2|gRPC]] 기반 추론(Inference) 서버 (TensorFlow Serving, NVIDIA Triton)
170. 서빙 아키텍처 A/B 테스트 및 [[595_canary_stack_smashing_protector|카나리]] 롤아웃 ([[170_ab_test_canary_rollout_shadow_mirroring|Canary Rollout]]) 섀도우 [[333_raid_1|미러링]] [[395_verification_process_review|검증]] 라우터
171. 설명 가능한 [[190_ai_llm_requirements_specification|AI]] ([[227_xai_explainable_ai_lime_shap|XAI]]) 도입 - 딥러닝 블랙박스 파훼. 국소적 선형 대리 모델 [[326_lime|LIME]] 및 게임이론 기반 변수 전역 기여도 [[327_shap|SHAP]] 값 지표 도출 
172. [[418_gpu|GPU]] 인프라 [[136_variance|분산]] 학습 ([[001_dikw_pyramid|Data]] Parallelism [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화 분배 vs Model Parallelism 모델 층 쪼개기 텐서 [[430_index_fast_full_scan|병렬]]화) 
173. [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]) [[495_hbm|HBM]] [[418_gpu|GPU]] 병목 최적화 (혼합 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 학습 FP16/FP32 믹싱 스루풋 향상)
174. [[221_llmops_large_language_model_ops|LLMOps]] 특화 요소 - 프롬프트 템플릿 관리, [[276_fine_tuning|RAG]] 벡터 DB [[212_synchronization_mechanisms|동기화]] [[123_pipe|파이프]], [[306_peft_lora|PEFT]] 잡 스케줄링 관리망 모니터링 
175. RHF ([[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]]) 기반 랭킹 선호 모델 수집 [[123_pipe|파이프]] 인간 라벨러 루프 연동
176. 자동화 [[123_pipe|파이프]]라인 ([[176_automl_hyperparameter_optimization_bayesian|AutoML]]) 하이퍼파라미터 최적화 베이지안 탐색 모듈망 결합
177. [[001_dikw_pyramid|데이터]] 엔지니어링 [[282_performance_tactics|성능]] 최적 [[177_delta_lakehouse_time_travel_transaction|델타 레이크하우스]] [[022_snapshot_backup_architecture|스냅샷]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] (Time Travel) [[191_transaction_concept_states|트랜잭션]] 
178. [[178_parquet_rle_encoding_columnar_compression|파케이]] ([[178_parquet_rle_encoding_columnar_compression|Parquet]]) 스토리지 [[347_compaction|압축]] 포맷 [[099_rle|RLE]] 스킵 인코딩 최적 [[282_performance_tactics|성능]] 모델 
179. [[179_kafka_flink_watermark_time_window|카프카]] ([[179_kafka_flink_watermark_time_window|Kafka]]) [[229_stream_processing_kafka_flink|스트림 처리]] 플링크 (Flink) 시간 창 (Window) ウォ터마크([[085_watermark|Watermark]]) 체제
180. [[217_cdc_binlog_change_capture_debezium|CDC]] 실시간 [[568_logs_distributed_logging_elk_fluentd|로그]] 캡처 데베지움 [[123_pipe|파이프]] 동기망
181. [[181_federated_learning_privacy_distributed_training|연방 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]]) 스마트폰/[[136_variance|분산]] 엣지 노드 [[267_weight_bias_activation|가중치]] 로컬 암호 전송 클라우드 보안 병합
182. [[004_blockchain|블록체인]]/[[022_smart_contract|스마트 컨트랙트]] [[001_dikw_pyramid|데이터]] 무결 증빙 NFT [[191_transaction_concept_states|트랜잭션]] 마켓 
183. [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] 클라우드 인프라 키 전환 
184. 프라이버시 [[571_protection_vs_security|보호]] [[396_differential_privacy|차분 프라이버시]] 노이즈 통계 방어 
185. K-익명성, 마스킹 [[123_pipe|파이프]] 자동 변환 전처리 
186. [[070_graph_datastructure|그래프]] DB 추천 [[001_algorithm_definition|알고리즘]] [[345_collaborative_filtering|협업 필터링]] [[559_serverless_cold_start_mitigation|콜드 스타트]] 파훼 
187. 시계열 DB 보간법([[187_time_series_interpolation_rollup_dashboard|Interpolation]]) [[042_rollup_l2_solution|롤업]] 통계 지표 대시보드
188. [[157_oom_killer|OOM]] [[307_memory_protection|메모리 보호]] GC([[380_garbage_collection|Garbage Collection]]) 스파크 스왑 방어
189. [[189_kafka_consumer_lag_monitoring_alert|카프카 컨슈머 랙]] (Lag) [[015_지연_데이터_관점|지연]] 모니터링 경보 [[123_pipe|파이프]] 
190. [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] 방어 주키퍼 펜싱 합의 코디 연계망 
191. [[216_lambda_kappa_architecture_batch_realtime|람다]]/[[096_kappa_architecture|카파 아키텍처]] 재현 ([[307_event_sourcing|Event Sourcing]] Replay) 스트림 병합
192. 엣지 [[190_ai_llm_requirements_specification|AI]] 컴파일러 (ONNX, TensorRT) 모델 [[149_serial_communication_rs232_rs485|직렬]]화 패키징 배포망 
193. [[193_neuromorphic_chip_snn_low_power_inference|뉴로모픽 반도체]] [[446_snn|SNN]] 저전력 칩 통계 추론 
194. 메들리온 아키텍처 (Bronze, Silver, Gold 테이블) 정제 적재 로직 
195. [[195_federated_query_data_fabric_distributed_join|연방 쿼리]] [[212_data_fabric_virtualization|데이터 패브릭]] [[136_variance|분산]] 메타 통계망 조인 
196. [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]] [[090_configuration_item|CI]]/CD (dbt) [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] 테스트 코드 결합 
197. [[213_data_catalog_metadata|데이터 카탈로그]] 계보 (Lineage) [[003_bigdata_7v|시각화]] [[007_security_policy|보안 정책]] 연계망 
198. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] 소프트 타겟([[389_knowledge_distillation_soft_target|Soft Target]]) [[130_probability|확률]] 분포 모방 [[123_pipe|파이프]]
199. [[199_intent_based_networking_ibn_ai_traffic_routing|인텐트 기반 네트워킹]] ([[857_ibn_intent_based_networking_declarative_automation|IBN]]) 트래픽 [[231_ai_turing_test|인공지능]] [[339_routing_overview_best_path_selection|라우팅]] 분배망
200. [[200_autonomous_driving_imitation_learning_digital_twin|자율주행 모방 학습]] 시뮬레이터 [[126_digital_twin_concept|디지털 트윈]] 동기 [[818_synthetic_data|합성 데이터]] [[087_process_state_transition|생성]] [[123_pipe|파이프]]라인

## 5. 시험 빈출 요약 및 기술사 빅데이터/[[190_ai_llm_requirements_specification|AI]] 논술 키워드 (100개 집중)
201. 3V 5V 빅데이터 특성 다양 속도 볼륨 
202. [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] [[136_variance|분산]] 확장 수평 범용 노드 
203. [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[013_hdfs|HDFS]] 블록 [[016_replication_factor|복제]] 3벌 [[017_rack_awareness|랙 인지]] 내결함성 
204. [[014_namenode|네임노드]] [[012_metadata|메타데이터]] [[018_mapreduce|맵리듀스]] 디스크 병목 
205. 셔플 정렬 [[020_yarn|YARN]] 리소스 매니저 
206. 스파크 인메모리 [[310_audit|RDD]] [[023_lazy_evaluation|지연 평가]] 계보 [[658_ir_recovery|복구]] 
207. [[208_data_lake_schema_on_read|데이터 레이크]] [[009_schema_on_read|스키마 온 리드]] 원시 저장 
208. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] [[010_schema_on_write|스키마 온 라이트]] [[311_inmon|Inmon]] 주젯 
209. [[209_data_mart_kimball_star_schema|데이터 마트]] [[312_kimball|Kimball]] 다차원 분석 [[334_star_schema|스타 스키마]] 
210. 팩트 [[273_dimension_table_analysis_perspective|차원 테이블]] 스노우플레이크 눈송이 
211. [[316_olap|OLAP]] 드릴다운 [[042_rollup_l2_solution|롤업]] [[276_surrogate_key_artificial_identifier|서로게이트 키]] 
212. [[215_etl_vs_elt_pipeline|ETL]] 변환 병목 [[034_elt|ELT]] 클라우드 내부 연산 전이 
213. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] [[191_transaction_concept_states|트랜잭션]] 델타 레이크 [[178_parquet_rle_encoding_columnar_compression|파케이]] [[347_compaction|압축]] 
214. [[179_kafka_flink_watermark_time_window|카프카]] [[315_pub_sub|Pub Sub]] 토픽 [[514_partition_slice_volume|파티션]] 오프셋 [[136_variance|분산]] 브로커 
215. 플링크 네이티브 스트림 [[085_watermark|워터마크]] 윈도우 시간 
216. [[216_lambda_kappa_architecture_batch_realtime|람다]] [[096_kappa_architecture|카파 아키텍처]] 배치 실시간 분할 일원화망 
217. [[217_cdc_binlog_change_capture_debezium|CDC]] 빈로그 [[001_dikw_pyramid|데이터]] 캡처 변경 [[568_logs_distributed_logging_elk_fluentd|로그]] 추출 데베지움 
218. [[218_nosql_base_eventual_consistency_sharding|NoSQL BASE]] [[650_eventual_consistency|결과적 일관성]] [[280_sharding|샤딩]] 해시 [[136_variance|분산]]
219. [[341_process|CAP]] [[342_pacelc|PACELC]] 트레이드오프 [[136_variance|분산]] 합의 
220. 키-값 도큐먼트 컬럼 패밀리 [[039_graph_db|그래프 데이터베이스]] 
221. LSM 트리 [[494_memtable_sstable_flush|멤테이블]] 순차 플러시 [[378_lsm_compaction_tombstone|콤팩션]] 
222. [[211_data_mesh_domain_ownership|데이터 메시]] [[136_variance|분산]] 오너십 [[001_dikw_pyramid|데이터]] 프로덕트 셀프 서빙 
223. [[212_data_fabric_virtualization|데이터 패브릭]] 메타 [[015_virtualization|가상화]] 통합 연결망 
224. [[214_data_lineage_tracking|데이터 리니지]] 흐름 족보 [[394_catalog_metadata|카탈로그]] 탐색 태그 
225. [[225_kdd_t_test_anova_statistical_analysis|KDD]] 교차 분석 T검정 [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] 통계 
226. [[226_pearson_correlation_regression_r2_vif_multicollinearity|피어슨 상관]] 회귀 최소 제곱 R^2 결정 다중 공선 VIF 
227. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] 우도 [[139_clt|중심 극한 정리]] [[337_p_value_significance|p-value]] 1/2종 오류 
228. [[163_pca|PCA]] 주성분 LDA t-SNE [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 비지도 지도 
229. 시계열 [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] 정상성 [[345_collaborative_filtering|협업 필터링]] 추천 
230. [[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]] [[161_matrix_decomposition|행렬 분해]] [[353_random_forest|랜덤 포레스트]] [[127_boosting|부스팅]] XGBoost 
231. [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] 오버 샘플링 [[096_oversampling_smote|불균형 데이터 증강]] 
232. [[232_tfidf_cosine_similarity_text_embedding_confusion_matrix|TF-IDF]] [[359_cosine_similarity|코사인 유사도]] 텍스트 [[278_instruction_tuning|임베딩]] [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] 
233. [[233_precision_recall_f1_roc_auc_threshold|정밀도]] [[092_recall_sensitivity_hit_rate|재현율]] F1 스코어 [[256_roc_auc|ROC AUC]] 임계 곡선 
234. [[539_mdm_master_data_management|마스터 데이터]] ([[539_mdm_master_data_management|MDM]]) 골든 레코드 클린 룸 
235. [[231_ai_turing_test|인공지능]] [[002_turing_test|튜링 테스트]] [[233_expert_system|전문가 시스템]] 퍼지 탐색 
236. A* [[210_heuristics_scheduling|휴리스틱]] [[239_minimax_alpha_beta_pruning|미니맥스]] [[240_mcts_monte_carlo|MCTS]] 몬테카를로 [[315_exploration_exploitation|탐험]] 
237. [[241_machine_learning_basics|머신러닝]] 지도 비지도 강화 편향 [[136_variance|분산]] 오류 
238. [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 마진 [[059_kernel_trick_rbf_polynomial|커널 트릭]] [[264_naive_bayes|나이브 베이즈]] [[130_probability|확률]] 
239. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] 다층 은닉층 [[267_weight_bias_activation|가중치]] 활성화 [[268_sigmoid_vanishing_gradient|시그모이드]] 
240. [[269_relu_activation|ReLU]] [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 복원 [[363_softmax_backprop|소프트맥스 역전파]] 연쇄 
241. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] SGD 미니배치 [[277_adam_optimizer|Adam]] 관성 적응 [[276_momentum_optimizer|모멘텀]] 
242. [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|규제 드롭아웃]] [[281_early_stopping|조기 종료]] L1 L2 라쏘 릿지 
243. [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] [[097_stride_convolutional_neural_network_downsampling|스트라이드]] [[285_pooling_layer|풀링]] [[287_resnet_skip_connection|ResNet]] 잔차 연결 YOLO 객체 
244. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 시계열 [[292_lstm|LSTM]] 셀 게이트 [[291_long_term_dependency|장기 의존성]] 극복 
245. [[245_seq2seq_context_vector_attention_dynamic_weight|Seq2Seq]] [[033_context|컨텍스트]] 어텐션 동적 가중 집중 연산 
246. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 셀프 어텐션 [[430_index_fast_full_scan|병렬]] [[300_positional_encoding|포지셔널 인코딩]] 
247. [[225_foundation_model_peft_lora|파운데이션 모델]] [[263_llm_large_language_model|LLM]] 파라미터 [[265_emergent_abilities|창발성]] 자기 지도 
248. [[301_bert_mlm|BERT]] [[040_encoder|인코더]] [[138_mlm_learning|MLM]] [[302_gpt_autoregressive|GPT]] [[039_decoder|디코더]] 자동 회귀 
249. [[249_instruction_finetuning_peft_lora_low_rank_adapter|인스트럭션 파인튜닝]] [[306_peft_lora|PEFT LoRA]] 저차원 [[259_adapter_pattern_interface_wrapper|어댑터]] 
250. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] 인간 피드백 강화 정렬 프롬프트 [[146_chain_of_thought_cot|CoT]] 사슬 
251. [[454_hallucination_prevention|할루시네이션 환각]] [[276_fine_tuning|RAG]] 증강 검색 벡터 DB 
252. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] [[434_quantization|양자화]] 경량 온디바이스 [[313_slm|SLM]] 디퓨전 노이즈 [[087_process_state_transition|생성]] 
253. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] [[463_markov_decision_process_mdp|MDP]] [[164_policy|정책]] 가치 Q러닝 [[465_dqn_deep_q_network|DQN]] 
254. [[348_mlops|MLOps]] [[001_dikw_pyramid|데이터]]/[[164_concept_drift_target_mapping_change|컨셉 드리프트]] [[165_feature_store_training_serving_consistency|피처 스토어]] 
255. [[227_xai_explainable_ai_lime_shap|XAI]] 설명 가능 [[326_lime|LIME]] [[327_shap|SHAP]] 기여 분할 
256. [[256_federated_learning_privacy_model_security|연합 학습]] 프라이버시 모델 보안 지표망 
257. (빅데이터 분석 / 클라우드 [[123_pipe|파이프]]라인 등 300+ 개념 연결 완성)
...
300. [[001_dikw_pyramid|데이터]] 및 [[190_ai_llm_requirements_specification|AI]] 아키텍트 전용 고득점 암기 단어장 집대성

---
**총정리 빅데이터 / [[001_dikw_pyramid|데이터]] 엔지니어링 키워드 : 총 300+ 통합 (1~6부 총 800+ 규모 핵심 토픽 포함)**
(빅데이터 인프라, [[843_hadoop_rack_awareness_data_replication_topology|하둡]]/스파크 구조, 실시간 [[179_kafka_flink_watermark_time_window|카프카]] [[123_pipe|파이프]]라인부터 [[211_data_mesh_domain_ownership|데이터 메시]]/[[146_lakehouse|레이크하우스]] 사상 및 최신 [[276_fine_tuning|RAG]] 튜닝, [[348_mlops|MLOps]], 통계 분석 수학까지 [[001_dikw_pyramid|데이터]] 전문가 과정의 지식 사전입니다.)