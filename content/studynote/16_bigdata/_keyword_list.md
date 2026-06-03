---
title: 16. 빅데이터 키워드 목록
date: '2026-03-04'
tags:
- studynote-bigdata
---
[[267_weight_bias_activation|weight]] = 9999

# 빅데이터 (Big [[001_dikw_pyramid|Data]]) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 빅데이터 전 영역 기술사 수준 핵심 키워드
> ⚡ 빅데이터 기술사 문제: 단순 플랫폼 나열이 아닌 **아키텍처 선택 근거 + 법·제도 + 비즈니스 가치 + 미래 전망** 통합 서술 요구

---

## 1. 빅데이터 개론 / 특성 — 22개

1. 빅데이터 정의 — 3V: [[001_bigdata_3v_5v|Volume]](양) / Velocity(속도) / Variety(다양성) (Laney, 2001)
2. 5V — 3V + Veracity([[002_bigdata_5v|정확성]]) + Value(가치)
3. 7V — 5V + Visualization([[003_bigdata_7v|시각화]]) + Variability(가변성)
4. 빅데이터 도입 필요성 — [[001_dikw_pyramid|데이터]] 폭증([[004_bigdata_necessity|제타바이트 시대]]), [[004_unstructured_data|비정형 데이터]] 급증
5. [[004_unstructured_data|비정형 데이터]] 유형 — 텍스트/이미지/동영상/음성/[[568_logs_distributed_logging_elk_fluentd|로그]]/SNS/[[101_iot_concept|IoT]] 센서
6. [[003_semi_structured_data|반정형 데이터]] — [[343_json|JSON]]/XML/HTML/CSV — [[005_schema|스키마]] 부분 보유
7. 빅데이터 생태계 — 수집→저장→처리→분석→[[003_bigdata_7v|시각화]]→활용
8. 빅데이터 vs 전통적 [[001_dikw_pyramid|데이터]] — RDBMS 한계(수평 확장 불가, 고정 [[005_schema|스키마]])
9. [[001_dikw_pyramid|데이터]] 폭증 요인 — [[101_iot_concept|IoT]]/SNS/모바일/센서/영상 [[933_cctv|CCTV]]
[[489_raid_10_hybrid|10]]. [[010_data_democratization|데이터 민주화]] ([[010_data_democratization|Data Democratization]]) — 셀프서비스 분석, 시민 [[001_dikw_pyramid|데이터]] 과학자
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_data_economy|데이터 경제]] ([[011_data_economy|Data Economy]]) — [[001_dikw_pyramid|데이터]] 자산화, [[001_dikw_pyramid|데이터]] 거래소
12. [[012_mydata|마이데이터]] ([[266_mydata_open_api_token_security|MyData]]) — [[781_personal_information|개인정보]] 자기결정권, 금융 [[012_mydata|마이데이터]]
13. [[245_public_bigdata|공공 빅데이터]] — 공공데이터포털, 행정안전부, [[001_dikw_pyramid|데이터]] 개방 [[164_policy|정책]]
14. [[246_data_voucher|데이터바우처 사업]] — 중소기업 [[001_dikw_pyramid|데이터]] 구매·가공 지원
15. 오픈데이터 원칙 — FAIR (Findable/Accessible/Interoperable/Reusable)
16. 유럽 [[001_dikw_pyramid|데이터]] [[268_strategy_pattern|전략]] — [[001_dikw_pyramid|Data]] Spaces, Gaia-X
17. 국가 [[001_dikw_pyramid|데이터]] [[164_policy|정책]] — [[001_dikw_pyramid|데이터]]기본법, [[001_dikw_pyramid|데이터]] 산업 진흥법
18. [[809_data_sovereignty|데이터 주권]] ([[410_ai_intellectual_property_data_sovereignty_data_act|Data Sovereignty]]) — 국가별 [[001_dikw_pyramid|데이터]] 현지화 규제
19. [[251_data_anonymization|개인정보 비식별화]] — [[185_k_anonymity_masking_data_pipeline|k-익명성]] / [[815_l_diversity|l-다양성]] / [[816_t_closeness|t-근접성]]
20. [[252_data_structured_ratio|데이터 정형화 비율]] — 전체 [[001_dikw_pyramid|데이터]] 중 정형 < 20%, 비정형 > 80%
21. [[004_bigdata_necessity|제타바이트 시대]] — 2025년 전 세계 [[087_process_state_transition|생성]] [[001_dikw_pyramid|데이터]] ~175 ZB
22. [[254_data_asset_valuation|데이터 자산 평가]] — 재무적 가치화, ISO/IEC 22123

---

## 2. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[031_에코_반향|에코]]시스템 심화 — 28개

1. [[012_apache_hadoop|Apache Hadoop]] — [[136_variance|분산]] 스토리지([[013_hdfs|HDFS]]) + [[136_variance|분산]] 처리([[018_mapreduce|MapReduce]]) + 자원 관리([[020_yarn|YARN]])
2. [[013_hdfs|HDFS]] ([[203_hadoop_hdfs_block_replication_fault_tolerance|Hadoop Distributed File System]]) — 블록 128MB, 3중 [[016_replication_factor|복제]], [[014_namenode|NameNode]]/[[015_datanode|DataNode]]
3. [[014_namenode|NameNode]] — [[203_metadata_management|메타데이터 관리]], [[454_spof|SPOF]] 우려 → Secondary [[014_namenode|NameNode]] / HA [[014_namenode|NameNode]]
4. [[015_datanode|DataNode]] — 실제 [[001_dikw_pyramid|데이터]] 블록 저장, 주기적 Heartbeat
5. [[017_rack_awareness|Rack Awareness]] — 같은 랙 두 [[016_replication_factor|복제]]본 방지, 장애 [[658_ir_recovery|복구]] 최적화
6. [[018_mapreduce|MapReduce]] — Map([[136_variance|분산]] 처리)/Shuffle&Sort/Reduce(집계) 3단계
7. Map 함수 — 입력 → ([[067_db_key_uniqueness_minimality|Key]], Value) 쌍 출력
8. Reduce 함수 — 동일 Key의 Value 집계, 최종 결과 출력
9. [[205_shuffle_sort_yarn_resource_manager|Shuffle & Sort]] — Map 출력을 Reduce로 분배 (네트워크 병목)
[[489_raid_10_hybrid|10]]. [[020_yarn|YARN]] ([[020_yarn|Yet Another Resource Negotiator]]) — 자원 관리, Application Master / [[194_container_virtualization_docker_namespace|Container]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[028_apache_hive|Apache Hive]] — SQL on [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]], HQL, 메타스토어(MySQL/PostgreSQL), 배치형
12. Apache [[543_hbase|HBase]] — [[035_nosql|NoSQL]] on [[013_hdfs|HDFS]], 열 지향, 실시간 랜덤 R/W, [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 의존
13. [[038_apache_pig|Apache Pig]] — [[001_dikw_pyramid|데이터]] 흐름 스크립트 언어 (Pig Latin), 복잡한 [[215_etl_vs_elt_pipeline|ETL]]
14. [[039_apache_sqoop|Apache Sqoop]] — RDBMS ↔ [[013_hdfs|HDFS]] [[001_dikw_pyramid|데이터]] 임포트/익스포트
15. [[040_apache_flume|Apache Flume]] — [[626_log_collection|로그 수집]] 에이전트, Source/Channel/Sink 구조
16. [[051_apache_oozie|Apache Oozie]] — [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 워크플로우/코디네이터 [[079_kube_scheduler_pod_placement|스케줄러]]
17. [[029_apache_zookeeper|Apache Zookeeper]] — [[136_variance|분산]] 코디네이션 [[090_service_kubernetes_network_load_balancing|서비스]], 리더 선출, 잠금
18. [[041_apache_ambari_management|Apache Ambari]] — [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터 관리 GUI
19. Cloudera CDH / HDP (Hortonworks) → [[193_crl_distribution_point_cdp|CDP]] ([[042_cloudera_cdp_platform|Cloudera Data Platform]])
20. [[028_apache_tez|Apache Tez]] — [[401_bayesian_network_dag_causality|DAG]] 기반 실행 엔진, [[544_hive|Hive]]/Pig 속도 개선
21. [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 연동) — Flume 대체, 내구성/[[139_throughput|처리량]]↑
22. [[044_apache_storm|Apache Storm]] — [[459_quic_fec_forward_error_correction|초기]] 실시간 처리, Spout/Bolt 토폴로지
23. Apache Samza — LinkedIn, [[179_kafka_flink_watermark_time_window|Kafka]] 네이티브 스트리밍
24. [[013_hdfs|HDFS]] 페더레이션 ([[543_federation|Federation]]) — 다중 [[014_namenode|NameNode]], [[061_namespace|네임스페이스]] [[136_variance|분산]]
25. [[048_hdfs_viewfs|HDFS ViewFS]] — [[501_file_definition_logical_record|파일]] 시스템 투명 접근
26. [[269_small_file_problem_data_lakehouse|Small File Problem]] — [[013_hdfs|HDFS]] 비효율, HAR/Sequence [[501_file_definition_logical_record|File]]/ORC로 해결
27. [[001_dikw_pyramid|데이터]] [[149_serial_communication_rs232_rs485|직렬]]화 — Avro / [[535_sync_communication_rest_grpc|Protocol Buffers]] / Thrift / Kryo
28. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 보안 — [[545_kerberos_kdc_ticket_based_auth|Kerberos]] [[303_authentication_authorization_patterns|인증]], Ranger(권한)/Atlas([[394_catalog_metadata|카탈로그]])

---

## 3. [[136_variance|분산]] 처리 / 스파크 심화 — 24개

1. [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] — 인메모리 [[136_variance|분산]] 처리, [[018_mapreduce|MapReduce]] 대비 최대 100배 빠름
2. [[310_audit|RDD]] ([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]]) — 불변, [[136_variance|분산]], [[296_fault_tolerance_architecture|결함 허용]], Lineage 기반 [[658_ir_recovery|복구]]
3. Transformation vs Action — [[023_lazy_evaluation|Lazy Evaluation]] (변환은 [[015_지연_데이터_관점|지연]], 액션은 즉시)
4. DataFrame / Dataset — [[005_schema|스키마]] 기반, Catalyst 최적화, Type-[[093_safe_scaled_agile_framework_art_pi|safe]]
5. [[056_spark_sql|Spark SQL]] — SQL [[298_qkv_attention|쿼리]]로 DataFrame 처리, [[544_hive|Hive]] 메타스토어 연동
6. [[057_catalyst_optimizer|Catalyst Optimizer]] — [[369_logic_bomb|논리]] → 물리 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 최적화
7. [[058_tungsten_engine|Tungsten Engine]] — CPU/메모리 최적화, Codegen, Off-[[078_heap_datastructure|heap]] 메모리
8. AQE (Adaptive Query Execution) — 런타임 통계 기반 자동 최적화 (Spark 3.0+)
9. [[060_spark_streaming_dstream|Spark Streaming]] ([[060_spark_streaming_dstream|DStream]]) — 마이크로배치 스트리밍 (구세대)
[[489_raid_10_hybrid|10]]. [[061_structured_streaming|Structured Streaming]] — DataFrame [[014_api_posix|API]] 스트리밍, 연속 처리, [[085_watermark|Watermark]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. MLlib — [[136_variance|분산]] ML [[336_library_vs_framework|라이브러리]] ([[104_classification_analysis|분류]]/회귀/군집/추천/[[163_pca|PCA]])
12. GraphX — [[136_variance|분산]] [[070_graph_datastructure|그래프]] 처리, PageRank
13. Spark 배포 모드 — Local / [[150_5g_sa_standalone_architecture|Standalone]] / [[020_yarn|YARN]] / [[205_kubernetes_container_orchestration|Kubernetes]] / Mesos
14. Executor / Driver / Cluster Manager — Spark 실행 구조
15. Shuffle 최적화 — spark.sql.shuffle.partitions, AQE 코어리스
16. Spark [[149_serial_communication_rs232_rs485|직렬]]화 최적화 (Kryo) — Kryo > Java, [[282_performance_tactics|성능]] 차이
17. Broadcast [[521_join|Join]] — 소규모 테이블을 모든 Executor에 복사
18. [[069_skew_join|Skew Join]] — [[001_dikw_pyramid|데이터]] 쏠림 해결 (AQE 자동 분할)
19. [[070_partition_optimization|파티션 최적화]] — repartition / coalesce, 코어 수 × 2~4
20. [[071_checkpointing|체크포인팅]] ([[071_checkpointing|Checkpointing]]) — Lineage 단절, 장애 [[658_ir_recovery|복구]] 가속
21. [[072_spark_history_server|Spark History Server]] — 완료 작업 [[568_logs_distributed_logging_elk_fluentd|로그]] 조회, UI
22. [[073_delta_lake_on_spark|Delta Lake on Spark]] — ACID [[191_transaction_concept_states|트랜잭션]], MERGE INTO, 타임 트래블
23. [[074_photon_engine|Photon Engine]] ([[074_photon_engine|Databricks]]) — 네이티브 벡터화 Spark 실행 엔진
24. [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] 3.5+ 개선 — ANSI SQL 확대, Python [[014_api_posix|API]] 강화

---

## 4. 스트리밍 / 실시간 처리 — 22개

1. 스트리밍 처리 필요성 — 실시간 이상 감지, 즉각 대응 의사결정
2. [[215_flink_native_stream_watermark_window_time|Apache Flink]] — 상태 기반 스트리밍, 이벤트 시간 처리, Exactly-Once
3. Flink 아키텍처 — JobManager / TaskManager / JobGraph
4. DataStream [[014_api_posix|API]] / Table [[014_api_posix|API]] & SQL — Flink 두 계층
5. Flink [[200_savepoint_partial_rollback|Savepoint]] / Checkpoint — 상태 저장, 재시작 지점
6. 이벤트 시간 (Event Time) vs 처리 시간 (Processing Time)
7. [[085_watermark|Watermark]] — [[015_지연_데이터_관점|지연]] 이벤트 허용 임계, 늦은 [[001_dikw_pyramid|데이터]] [[507_acid_properties|트리거]]
8. [[086_window_operations|윈도우 연산]] — 텀블링 / 슬라이딩 / [[160_session_controlling_terminal|세션]] / 글로벌 윈도우
9. [[083_cross_validation|정확히 한 번]] ([[083_cross_validation|Exactly-Once Semantics]]) — [[549_2pc_two_phase_commit_limitations_msa|2PC]] + Idempotent Sink
[[489_raid_10_hybrid|10]]. [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] — 내구성 있는 [[389_mesh_topology|메시]]지 큐, 스트리밍 기반
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[179_kafka_flink_watermark_time_window|Kafka]] [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]] — 키 기반 / 라운드로빈 / 커스텀
12. [[089_consumer_lag|Consumer Lag]] — [[179_kafka_flink_watermark_time_window|Kafka]] 소비 [[015_지연_데이터_관점|지연]] [[229_monitor|모니터]]링, Burrow / JMX
13. [[179_kafka_flink_watermark_time_window|Kafka]] MirrorMaker 2 — 클러스터 간 [[016_replication_factor|복제]], [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]
14. [[091_amazon_kinesis|Amazon Kinesis]] [[001_dikw_pyramid|Data]] Streams — 샤드 기반, AWS 관리형
15. Google Pub/Sub — [[179_kafka_flink_watermark_time_window|Kafka]] 대안, GCP, 글로벌 [[136_variance|분산]]
16. [[093_azure_event_hubs|Azure Event Hubs]] — [[179_kafka_flink_watermark_time_window|Kafka]] 호환 [[014_api_posix|API]], AMQP 지원
17. [[094_apache_pulsar|Apache Pulsar]] — [[179_kafka_flink_watermark_time_window|Kafka]] 대안, 컴퓨팅/스토리지 분리, [[014_multi_tenancy|멀티 테넌시]]
18. [[095_lambda_architecture|람다 아키텍처]] — 배치([[092_GPT_NLP|Speed Layer]]) + 실시간(Batch Layer) + Serving Layer
19. [[096_kappa_architecture|카파 아키텍처]] — 스트리밍만으로 단순화, [[179_kafka_flink_watermark_time_window|Kafka]] + Flink
20. 스트리밍 SQL — ksqlDB ([[094_reinforcement_learning|Confluent]]) / Flink SQL / [[061_structured_streaming|Spark Structured Streaming]]
21. [[098_cep|CEP]] ([[098_cep|Complex Event Processing]]) — 패턴 이벤트 감지, Flink [[098_cep|CEP]]
22. 실시간 [[316_olap|OLAP]] — Apache Druid / Apache Pinot / ClickHouse — ms [[015_지연_데이터_관점|지연]] [[298_qkv_attention|쿼리]]

---

## 5. 빅데이터 분석 기법 — 26개

1. [[100_descriptive_statistics|기술 통계]] ([[100_descriptive_statistics|Descriptive Statistics]]) — 평균/중앙값/[[136_variance|분산]]/분포 요약
2. [[101_inferential_statistics|추론 통계]] ([[101_inferential_statistics|Inferential Statistics]]) — 표본 → 모집단 추론, [[145_hypothesis_testing|가설 검정]]
3. [[062_eda_exploratory_data_analysis|탐색적 데이터 분석]] ([[064_eda|EDA]]) — 패턴 발견, [[397_outlier_mahalanobis|이상치 탐지]], [[003_bigdata_7v|시각화]]
4. [[149_regression_analysis|회귀 분석]] (Regression) — 단순/다중/다항/릿지/라쏘/엘라스틱넷
5. [[104_classification_analysis|분류]] ([[107_classification|Classification]]) — [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] / 트리 / [[238_svm_margin_kernel_trick_naive_bayes|SVM]] / [[257_ensemble_learning|앙상블]]
6. [[105_clustering_analysis|군집화]] ([[105_clustering_analysis|Clustering]]) — K-Means / [[351_dbscan_density_based_clustering|DBSCAN]] / 계층적 / Gaussian Mixture
7. [[106_association_rules|연관 규칙]] ([[106_association_rules|Association Rules]]) — Apriori / [[293_fp_function_point|FP]]-Growth, [[084_support_association_rule_transaction|지지도]]/[[085_confidence_association_rule_conditional_probability|신뢰도]]/[[086_lift_association_rule_marketing|향상도]]
8. [[107_market_basket_analysis|장바구니 분석]] ([[107_market_basket_analysis|Market Basket Analysis]]) — 구매 패턴, 교차 판매
9. [[105_exploratory_data_analysis|감성 분석]] ([[105_exploratory_data_analysis|Sentiment Analysis]]) — 긍/부정/중립, [[301_bert_mlm|BERT]] 기반 심화
[[489_raid_10_hybrid|10]]. [[109_text_mining|텍스트 마이닝]] ([[109_text_mining|Text Mining]]) — [[232_tfidf_cosine_similarity_text_embedding_confusion_matrix|TF-IDF]] / [[339_word2vec|Word2Vec]] / [[301_bert_mlm|BERT]] / [[263_llm_large_language_model|LLM]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[107_classification|소셜 네트워크 분석]] ([[107_classification|SNA]]) — 중심성 / 커뮤니티 탐지 / 영향력
12. [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] ([[111_anomaly_detection|Anomaly Detection]]) — 통계 기반 / ML 기반 / 딥러닝 기반
13. [[341_time_series_ar_ma_arma|시계열 분석]] (Time Series) — [[342_arima_auto_regressive_integrated_moving_average|ARIMA]] / SARIMA / Prophet / [[292_lstm|LSTM]] / [[246_transformer_self_attention_parallel_positional_encoding|Transformer]]
14. [[113_spatial_analysis|공간 분석]] ([[113_spatial_analysis|Spatial Analysis]]) — 지리정보시스템(GIS), PostGIS
15. [[114_graph_analytics|그래프 분석]] ([[114_graph_analytics|Graph Analytics]]) — PageRank / 커뮤니티 탐지 / 최단 경로
16. [[115_text_summarization|텍스트 요약]] — 추출적(Extractive) / 추상적(Abstractive) 요약
17. [[116_topic_modeling|토픽 모델링]] — LDA / BERTopic / NMF
18. [[117_ner|개체명 인식]] ([[117_ner|NER]]) — 인물/장소/조직/날짜 추출
19. [[118_image_analysis|이미지 분석]] — [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 기반 [[104_classification_analysis|분류]]/탐지/분할 대용량 배치
20. [[119_log_analysis|로그 분석]] — 이상 감지, 보안 이벤트, 패턴 발견
21. [[120_clickstream_analysis|클릭스트림 분석]] — 사용자 행동 패턴, 전환율 최적화
22. A/B 테스트 — 실험적 방법론, 통계적 유의성
23. [[211_recommendation_system|추천 시스템]] — [[345_collaborative_filtering|협업 필터링]] / 콘텐츠 기반 / 하이브리드
24. [[046_predictive_analytics|예측 분석]] ([[046_predictive_analytics|Predictive Analytics]]) — 이탈 예측, 대출 부도, 장비 고장
25. 처방적 분석 ([[047_prescriptive_analytics|Prescriptive Analytics]]) — 최적 의사결정 제안
26. [[122_causal_inference|인과 추론]] ([[122_causal_inference|Causal Inference]]) — 상관≠인과, DoWhy, 반사실 분석

---

## 6. [[035_nosql|NoSQL]] [[002_database_definition|데이터베이스]] — 20개

1. [[035_nosql|NoSQL]] 등장 배경 — RDBMS 수평 확장 한계, BASE 원칙
2. BASE 원칙 — Basically Available / Soft [[272_state_pattern|State]] / Eventually Consistent
3. [[341_process|CAP]] 정리 — [[194_consistency_database_integrity|Consistency]] / [[452_availability|Availability]] / [[514_partition_slice_volume|Partition]] Tolerance (2개만 선택)
4. [[342_pacelc|PACELC]] 이론 — [[341_process|CAP]] 확장, [[015_지연_데이터_관점|지연]] vs [[194_consistency_database_integrity|일관성]] 트레이드오프
5. 키-값 ([[067_db_key_uniqueness_minimality|Key]]-Value) DB — [[542_redis|Redis]] / [[545_dynamodb|DynamoDB]] / Riak — 빠른 조회, 단순 구조
6. [[542_redis|Redis]] — 인메모리, Pub/Sub, 자료구조(String/List/Set/Hash/ZSet), 클러스터
7. 문서형 ([[037_document|Document]]) DB — [[540_mongodb|MongoDB]] / CouchDB / Firestore
8. [[540_mongodb|MongoDB]] 아키텍처 — [[086_replicaset_kubernetes_controller_self_healing|ReplicaSet]] / [[243_sharding_horizontal_scaling_database|Sharding]] / Mongos / [[009_config|Config]] Server
9. 컬럼 패밀리 (Column Family) DB — [[541_cassandra|Cassandra]] / [[543_hbase|HBase]] / ScyllaDB
[[489_raid_10_hybrid|10]]. [[541_cassandra|Cassandra]] — [[172_maas_mobility_as_a_service|마스]]터 없는 링 구조, 토큰 기반 [[194_consistency_database_integrity|일관성]] 해시, 튜닝 가능한 [[194_consistency_database_integrity|일관성]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[070_graph_datastructure|그래프]] DB — Neo4j / Amazon Neptune / Memgraph — [[083_relationship_in_er_model|관계]] [[298_qkv_attention|쿼리]] 최적화
12. Cypher [[298_qkv_attention|쿼리]] 언어 (Neo4j) — MATCH / WHERE / RETURN
13. 시계열 DB — [[255_time_series_rollup_retention_compression|InfluxDB]] / TimescaleDB / QuestDB — 시간 기반 인덱싱
14. 검색 엔진 DB — [[302_cdc|Elasticsearch]] / OpenSearch — [[500_inverted_index_elasticsearch|역색인]], 전문 검색
15. 다중 모델 DB — ArangoDB / SurrealDB — 여러 [[035_nosql|NoSQL]] 모델 지원
16. [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] — [[292_etl_process|CockroachDB]] / [[293_elt_process|TiDB]] / YugabyteDB — SQL + 수평 확장 + ACID
17. 인메모리 DB — [[542_redis|Redis]] / Memcached / SAP HANA — 마이크로초 응답
18. [[140_consistency_levels|일관성 수준 선택]] — Strong / Bounded Staleness / [[160_session_controlling_terminal|Session]] / Consistent Prefix / Eventual
19. [[272_multi_master_replication|멀티 마스터 복제]] — CouchDB / [[545_dynamodb|DynamoDB]] Global Tables
20. [[142_schemaless_design_patterns|스키마리스 설계 패턴]] — [[278_instruction_tuning|임베딩]] vs [[316_reference_pattern_nosql|참조]], [[001_dikw_pyramid|데이터]] 중복 허용 설계

---

## 7. [[208_data_lake_schema_on_read|데이터 레이크]] / [[146_lakehouse|레이크하우스]] — 18개

1. [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) — 원시 [[001_dikw_pyramid|데이터]] 저장, [[009_schema_on_read|Schema-on-Read]], 저비용
2. [[001_dikw_pyramid|데이터]] 스왐프 ([[288_data_swamp_metadata_management_absence|Data Swamp]]) — 거버넌스 부재, 레이크 변질 위험
3. [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]]) — 구조화, [[010_schema_on_write|Schema-on-Write]], 높은 [[282_performance_tactics|성능]]
4. [[146_lakehouse|레이크하우스]] ([[146_lakehouse|Lakehouse]]) — 레이크(유연성) + [[209_data_warehouse_schema_on_write|DW]](ACID/[[282_performance_tactics|성능]]), [[177_delta_lakehouse_time_travel_transaction|Delta Lakehouse]]
5. [[147_delta_lake|Delta Lake]] — ACID on [[178_parquet_rle_encoding_columnar_compression|Parquet]], 타임 트래블, MERGE, [[005_schema|스키마]] 강제
6. [[148_apache_iceberg|Apache Iceberg]] — [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]], 히든 [[179_table_partitioning_concept|파티셔닝]], [[022_snapshot_backup_architecture|스냅샷]]
7. [[149_apache_hudi|Apache Hudi]] ([[149_apache_hudi|Hadoop Upserts Deletes Incrementals]]) — Uber, [[217_cdc_binlog_change_capture_debezium|CDC]] 지원
8. [[150_unity_catalog|Unity Catalog]] ([[074_photon_engine|Databricks]]) — [[146_lakehouse|레이크하우스]] 통합 거버넌스
9. [[151_multi_tier_architecture|다중 계층 아키텍처]] — Bronze(원시) / Silver(정제) / Gold(집계) — Medallion
[[489_raid_10_hybrid|10]]. [[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]] — [[147_delta_lake|Delta Lake]] 기반 3계층, [[074_photon_engine|Databricks]] 표준
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) — [[064_relation_domain|도메인]] 분권, [[154_data_product|데이터 제품]]화, 연합 거버넌스
12. [[154_data_product|데이터 제품]] ([[154_data_product|Data Product]]) — [[014_api_posix|API]] 인터페이스, [[085_sla|SLA]], 품질 지표 보유
13. [[155_elt_vs_etl|ELT vs ETL]] — 클라우드에서 ELT가 주류 (먼저 적재 후 변환)
14. [[212_data_fabric_virtualization|데이터 패브릭]] ([[212_data_fabric_virtualization|Data Fabric]]) — 위치 무관 지능형 [[001_dikw_pyramid|데이터]] 연결, Gartner
15. [[001_dikw_pyramid|데이터]] 분석 [[090_service_kubernetes_network_load_balancing|서비스]] — Amazon EMR / Azure HDInsight / GCP Dataproc
16. [[074_photon_engine|Databricks]] — Spark 기반 [[146_lakehouse|레이크하우스]] 플랫폼, [[150_unity_catalog|Unity Catalog]]
17. [[541_cassandra|Snowflake]] on [[208_data_lake_schema_on_read|Data Lake]] — External Table, Iceberg 지원
18. [[160_microsoft_fabric|Microsoft Fabric]] — One Lake, [[165_power_bi|Power BI]] + Synapse + [[001_dikw_pyramid|Data]] Factory 통합

---

## 8. 빅데이터 [[003_bigdata_7v|시각화]] — 14개

1. [[161_visualization_principles|데이터 시각화 원칙]] — 목적 명확성 / 간결성 / [[001_dikw_pyramid|데이터]] 잉크 비율 (Tufte)
2. [[162_chart_type_selection|차트 유형 선택]] — 비교(막대)/추세(선)/비율(파이/도넛)/분포(히스토그램/박스)
3. [[163_dashboard_design|대시보드 설계]] — [[018_kpi|KPI]] 중심, 5초 규칙, 인터랙티브
4. [[164_tableau|Tableau]] — 드래그앤드롭, VizQL, Extract/Live 연결
5. [[165_power_bi|Power BI]] — Microsoft 생태계 통합, DAX, Dataflow
6. [[166_looker|Looker]] / [[166_looker|Looker]] Studio — Google, LookML 시맨틱 레이어
7. [[167_apache_superset|Apache Superset]] — [[191_oss_license_compliance|오픈소스]], SQL Lab, 다양한 차트
8. [[168_grafana|Grafana]] — [[342_routing_metric_hop_bandwidth_delay|메트릭]]/[[568_logs_distributed_logging_elk_fluentd|로그]]/추적 통합 [[003_bigdata_7v|시각화]], 알람
9. [[169_kibana|Kibana]] — ELK [[057_stack|Stack]] [[003_bigdata_7v|시각화]], [[119_log_analysis|로그 분석]]
[[489_raid_10_hybrid|10]]. D3.js — JavaScript 기반 커스텀 인터랙티브 [[003_bigdata_7v|시각화]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. Plotly / [[510_dash_dynamic_adaptive_streaming_over_http|Dash]] — Python 기반 인터랙티브 [[003_bigdata_7v|시각화]]
12. [[172_network_visualization|네트워크 시각화]] — Gephi / Cytoscape — [[070_graph_datastructure|그래프]] [[003_bigdata_7v|시각화]]
13. [[173_geospatial_visualization|지리공간 시각화]] — Kepler.gl / Folium / Deck.gl — 지도 기반
14. [[174_bigdata_visualization_challenges|빅데이터 시각화 도전]] — 수십억 개 포인트, 집계/샘플링/렌더링 최적화

---

## 9. 빅데이터 플랫폼 / 아키텍처 — 16개

1. [[175_platform_selection_criteria|빅데이터 플랫폼 선택 기준]] — [[001_dikw_pyramid|데이터]] 규모 / 실시간 여부 / 비용 / 기술 역량
2. [[061_on_premise_legacy_infrastructure|On-Premise]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] vs Cloud 비교 — [[459_quic_fec_forward_error_correction|초기]] 비용 vs OPEX, 유연성
3. [[177_bigdata_reference_architecture|빅데이터 참조 아키텍처]] — 수집→저장→처리→분석→[[090_service_kubernetes_network_load_balancing|서비스]]→관리
4. [[178_modern_data_stack|모던 데이터 스택]] ([[764_mds|MDS]]) — Fivetran + [[541_cassandra|Snowflake]] + dbt + [[164_tableau|Tableau]]
5. 실시간 + 배치 통합 플랫폼 — Unified Batch/Streaming (Spark/Flink)
6. [[180_data_hub|데이터 허브]] ([[180_data_hub|Data Hub]]) — 중앙 [[001_dikw_pyramid|데이터]] 집계 및 배포 계층
7. [[181_multicloud_data_platform|멀티클라우드 데이터 플랫폼]] — [[541_cassandra|Snowflake]] / [[074_photon_engine|Databricks]] 멀티클라우드 지원
8. [[182_serverless_bigdata|서버리스 빅데이터]] — AWS Athena / [[263_storage_compute_separation_bigquery|BigQuery]] / Redshift [[206_serverless_cold_start|Serverless]]
9. [[183_data_orchestration|데이터 오케스트레이션]] — [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] / Dagster / Prefect
[[489_raid_10_hybrid|10]]. [[184_data_catalog_integration|데이터 카탈로그 통합]] — Glue [[394_catalog_metadata|Catalog]] / DataHub / OpenMetadata / Alation
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[185_scalability_design|확장성 설계]] — 수평 확장 / [[280_sharding|샤딩]] / [[179_table_partitioning_concept|파티셔닝]] / 클러스터 자동 확장
12. [[186_data_compression|데이터 컴프레션 전략]] — Snappy(속도) / Zstd([[347_compaction|압축]]률) / Gzip([[344_compatibility_usability|호환성]])
13. [[187_parquet_orc_iceberg_arrow|컬럼 기반 파일 포맷]] — [[178_parquet_rle_encoding_columnar_compression|Parquet]] / ORC / Iceberg / Arrow — 조회 최적화
14. [[188_spot_instance_ri|빅데이터 비용 최적화]] — [[209_spot_instance_cloud_cost_optimization|Spot Instance]] / 컴퓨팅-스토리지 분리 / RI
15. [[189_egress|데이터 이동 비용]] — [[189_egress|Egress]] 비용, 리전 내 [[001_dikw_pyramid|데이터]] 로컬화
16. [[190_management|하이브리드 분석]] — [[061_on_premise_legacy_infrastructure|온프레미스]] + 클라우드 [[344_bus|버스]]팅

---

## [[489_raid_10_hybrid|10]]. 빅데이터 거버넌스 / 품질 / 법규 — 18개

1. [[197_data_governance_definition|데이터 거버넌스 정의]] — [[001_dikw_pyramid|데이터]] 소유·관리·사용 원칙 체계
2. [[198_data_governance_components|데이터 거버넌스 구성 요소]] — [[164_policy|정책]]/표준/역할/프로세스/도구
3. [[067_data_steward_data_quality|데이터 스튜어드]] ([[067_data_steward_data_quality|Data Steward]]) — [[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]] 책임자
4. [[200_data_owner|데이터 소유자]] ([[200_data_owner|Data Owner]]) — 비즈니스 책임, 접근 승인
5. [[201_data_quality_dimensions|데이터 품질 차원]] — 완전성/[[002_bigdata_5v|정확성]]/[[194_consistency_database_integrity|일관성]]/적시성/유일성/유효성
6. [[202_data_quality_tools|데이터 품질 관리 도구]] — Great Expectations / Deequ / Soda Core
7. [[001_dikw_pyramid|데이터]] 계보 ([[214_data_lineage_tracking|Data Lineage]]) — 열 수준 계보, 영향 분석, Apache Atlas
8. [[203_metadata_management|메타데이터 관리]] — 비즈니스/기술/운영 [[012_metadata|메타데이터]] 3유형
9. [[051_mdm_master_data_management|마스터 데이터 관리]] ([[539_mdm_master_data_management|MDM]]) — 황금 레코드, 중복 제거
[[489_raid_10_hybrid|10]]. [[001_dikw_pyramid|데이터]] 보안 — 암호화(전송/저장) / 접근 제어 / [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] / [[386_dlp|DLP]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[206_pipa_bigdata_exception|개인정보보호법 빅데이터 특례]] — 가명처리 허용 (2020년 [[001_dikw_pyramid|데이터]] 3법)
12. [[207_gdpr_article_89|GDPR Article 89]] — 과학적 연구 목적 빅데이터 처리 특례
13. [[208_data_deidentification_techniques|데이터 비식별화 기법]] — [[819_data_masking|데이터 마스킹]] / 가명화 / 집계화 / 노이즈 추가
14. [[209_differential_privacy|차등 프라이버시]] ([[817_differential_privacy|Differential Privacy]]) — 통계 [[298_qkv_attention|쿼리]] + 노이즈, Apple/Google
15. [[818_synthetic_data|합성 데이터]] ([[818_synthetic_data|Synthetic Data]]) — 원본과 유사 통계적 특성, [[781_personal_information|개인정보]] 대체
16. [[211_data_ethics|데이터 윤리]] ([[211_data_ethics|Data Ethics]]) — [[001_algorithm_definition|알고리즘]] 편향, 공정성, 투명성
17. [[212_bigdata_disputes|빅데이터 분쟁]] — [[001_dikw_pyramid|데이터]] 소유권, 수집 동의, 목적 외 사용
18. [[213_data_audit|데이터 감사]] ([[213_data_audit|Data Audit]]) — 접근 이력, 변경 이력, 보관 기간

---

## [[308_static_dynamic_nat_pat_port_address_translation|11]]. 빅데이터 산업 응용 — 16개

1. [[214_finance_bigdata|금융 빅데이터]] — 신용평가 / 이상거래탐지([[267_gnn_fraud_detection_knowledge_graph|FDS]]) / [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 관리 / 알고트레이딩
2. [[215_healthcare_bigdata|의료 빅데이터]] — 전자의무기록(EMR) / 유전체 분석 / 임상 예측 / 신약 개발
3. 공공 [[001_dikw_pyramid|데이터]] 활용 — 교통 예측 / 범죄 예방 / 도시 계획 / 행정 [[090_service_kubernetes_network_load_balancing|서비스]] 개선
4. [[217_manufacturing_bigdata|제조 빅데이터]] — 예지 정비([[123_pdm_product_data_management|PdM]]) / 불량 감지 / 에너지 최적화
5. 유통·물류 빅데이터 — 수요 예측 / 재고 최적화 / 배송 경로 최적화
6. [[219_media_bigdata|미디어 빅데이터]] — 시청 분석 / 콘텐츠 추천 / 광고 타겟팅
7. SNS 빅데이터 — 여론 분석 / 트렌드 감지 / 인플루언서 분석
8. [[221_smart_city_bigdata|스마트시티 빅데이터]] — [[933_cctv|CCTV]] 분석 / 교통 [[130_signal|신호]] 최적화 / 에너지 그리드
9. [[222_agriculture_bigdata|농업 빅데이터]] — 정밀 농업 / 날씨 연계 수확량 예측 / 토양 분석
[[489_raid_10_hybrid|10]]. [[223_education_bigdata|교육 빅데이터]] — 학습 분석([[240_switch_learning_forwarding_flooding|Learning]] Analytics) / 맞춤형 교육
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[224_tourism_bigdata|관광 빅데이터]] — 관광 수요 예측 / 혼잡도 분석 / 관광 코스 추천
12. [[225_telecom_bigdata|통신 빅데이터]] — 네트워크 장애 예측 / 고객 이탈 분석 / QoE 최적화
13. [[226_energy_bigdata|에너지 빅데이터]] — 전력 수요 예측 / 신재생에너지 출력 예측 / 스마트미터
14. [[227_management|보험 빅데이터]] — 보험료 산정 / 사기 탐지 / 언더라이팅 자동화
15. [[228_management|부동산 빅데이터]] — 시세 예측 / 상권 분석 / 인구 이동 분석
16. [[229_audit|국방 빅데이터]] — 정보 분석 / 적 행동 예측 / 보안 위협 탐지

---

## 12. 최신 빅데이터 동향 — 12개

1. [[230_delta_iceberg_hudi|레이크하우스 주류화]] — Delta/Iceberg/Hudi 3강 경쟁, 개방형 포맷
2. [[231_management|데이터 메시 확산]] — [[064_relation_domain|도메인]] 소유권, 자율 [[154_data_product|데이터 제품]]
3. 실시간 [[316_olap|OLAP]] 성장 — Druid / Pinot / ClickHouse / StarRocks
4. [[190_ai_llm_requirements_specification|AI]] + 빅데이터 융합 — 대규모 ML 학습, [[263_llm_large_language_model|LLM]] 기반 [[001_dikw_pyramid|데이터]] 분석
5. [[234_text_to_sql_on_bigdata|Text-to-SQL on BigData]] — LLM으로 자연어 → [[298_qkv_attention|쿼리]] 자동 [[087_process_state_transition|생성]]
6. [[235_kappa|스트리밍 우선 아키텍처]] — 배치 → 스트리밍 전환, [[235_kappa|Kappa]] 아키텍처 강화
7. [[236_data_contract|데이터 계약]] ([[236_data_contract|Data Contract]]) — [[005_schema|스키마]] 안정성 보장 생산자-소비자 합의
8. [[237_apache_iceberg|오픈소스 포맷 경쟁]] — [[148_apache_iceberg|Apache Iceberg]] 사실상 표준화 움직임
9. [[236_quantum_computing_pqc|양자 컴퓨팅]] + 빅데이터 — 최적화 문제, 양자 ML [[459_quic_fec_forward_error_correction|초기]] 연구
[[489_raid_10_hybrid|10]]. [[239_architecture|엣지 빅데이터]] — 엣지에서 집계 후 클라우드 전송, [[140_bandwidth|대역폭]] 절감
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[240_databricks_vs_snowflake_dw|Databricks vs Snowflake]] — [[146_lakehouse|레이크하우스]] vs [[209_data_warehouse_schema_on_write|DW]] 진영 경쟁
12. [[255_data_observability|데이터 옵저버빌리티]] — Monte Carlo / Bigeye — [[645_data_pipeline_acceleration|데이터 파이프라인]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]

---

**총 키워드 수: 216개**
