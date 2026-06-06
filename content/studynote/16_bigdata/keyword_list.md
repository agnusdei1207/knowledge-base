---
title: "Keyword List"
date: "2026-03-04"
tags:
  - "studynote-bigdata"
weight: 50
---
# 빅데이터 (Big [Data](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 빅데이터 전 영역 기술사 수준 핵심 키워드
> ⚡ 빅데이터 기술사 문제: 단순 플랫폼 나열이 아닌 **아키텍처 선택 근거 + 법·제도 + 비즈니스 가치 + 미래 전망** 통합 서술 요구

---

## 1. 빅데이터 개론 / 특성 — 22개

1. 빅데이터 정의 — 3V: [Volume](/studynote/16_bigdata/01_intro/001_bigdata_definition/)(양) / Velocity(속도) / Variety(다양성) (Laney, 2001)
2. 5V — 3V + Veracity([정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)) + Value(가치)
3. 7V — 5V + Visualization([시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)) + Variability(가변성)
4. 빅데이터 도입 필요성 — [데이터](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 폭증([제타바이트 시대](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)), [비정형 데이터](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 급증
5. [비정형 데이터](/studynote/16_bigdata/01_intro/005_unstructured_data/) 유형 — 텍스트/이미지/동영상/음성/[로그](/studynote/16_bigdata/01_intro/005_unstructured_data/)/SNS/[IoT](/studynote/16_bigdata/01_intro/005_unstructured_data/) 센서
6. [반정형 데이터](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — [JSON](/studynote/16_bigdata/01_intro/006_semi_structured_data/)/XML/HTML/CSV — [스키마](/studynote/16_bigdata/01_intro/006_semi_structured_data/) 부분 보유
7. 빅데이터 생태계 — 수집->저장->처리->분석->[시각화](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)->활용
8. 빅데이터 vs 전통적 [데이터](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — RDBMS 한계(수평 확장 불가, 고정 [스키마](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/))
9. [데이터](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) 폭증 요인 — [IoT](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)/SNS/모바일/센서/영상 [CCTV](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터 민주화](/studynote/16_bigdata/01_intro/010_data_democratization/) ([Data Democratization](/studynote/16_bigdata/01_intro/010_data_democratization/)) — 셀프서비스 분석, 시민 [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 과학자
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [데이터 경제](/studynote/16_bigdata/01_intro/011_data_economy/) ([Data Economy](/studynote/16_bigdata/01_intro/011_data_economy/)) — [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 자산화, [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 거래소
12. [마이데이터](/studynote/16_bigdata/01_intro/012_mydata/) ([MyData](/studynote/16_bigdata/01_intro/012_mydata/)) — [개인정보](/studynote/16_bigdata/01_intro/012_mydata/) 자기결정권, 금융 [마이데이터](/studynote/16_bigdata/01_intro/012_mydata/)
13. [공공 빅데이터](/studynote/16_bigdata/01_intro/013_public_bigdata/) — 공공데이터포털, 행정안전부, [데이터](/studynote/16_bigdata/01_intro/013_public_bigdata/) 개방 [정책](/studynote/16_bigdata/01_intro/013_public_bigdata/)
14. [데이터바우처 사업](/studynote/16_bigdata/01_intro/014_data_voucher/) — 중소기업 [데이터](/studynote/16_bigdata/01_intro/014_data_voucher/) 구매·가공 지원
15. [오픈데이터 원칙 — FAIR (Findable/Accessible/Interoperable/Reusable)](/studynote/16_bigdata/01_intro/015_open_data_principles/)
16. 유럽 [데이터](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) [전략](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — [Data](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) Spaces, Gaia-X
17. 국가 [데이터](/studynote/16_bigdata/01_intro/017_national_data_policy/) [정책](/studynote/16_bigdata/01_intro/017_national_data_policy/) — [데이터](/studynote/16_bigdata/01_intro/017_national_data_policy/)기본법, [데이터](/studynote/16_bigdata/01_intro/017_national_data_policy/) 산업 진흥법
18. [데이터 주권](/studynote/16_bigdata/01_intro/018_data_sovereignty/) ([Data Sovereignty](/studynote/16_bigdata/01_intro/018_data_sovereignty/)) — 국가별 [데이터](/studynote/16_bigdata/01_intro/018_data_sovereignty/) 현지화 규제
19. [개인정보 비식별화](/studynote/16_bigdata/01_intro/019_data_de_identification/) — [k-익명성](/studynote/16_bigdata/01_intro/019_data_de_identification/) / [l-다양성](/studynote/16_bigdata/01_intro/019_data_de_identification/) / [t-근접성](/studynote/16_bigdata/01_intro/019_data_de_identification/)
20. [데이터 정형화 비율](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) — 전체 [데이터](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) 중 정형 < 20%, 비정형 > 80%
21. [제타바이트 시대](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) — 2025년 전 세계 [생성](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) [데이터](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) ~175 ZB
22. [데이터 자산 평가](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) — 재무적 가치화, ISO/IEC 22123

---

## 2. [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [에코](/studynote/16_bigdata/02_hadoop/031_mapreduce_programming_model_parallel_processing/)시스템 심화 — 28개

1. [Apache Hadoop](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — [분산](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 스토리지([HDFS](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) + [분산](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 처리([MapReduce](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) + 자원 관리([YARN](/studynote/16_bigdata/01_intro/001_bigdata_definition/))
2. [HDFS](/studynote/16_bigdata/01_intro/002_bigdata_5v/) ([Hadoop Distributed File System](/studynote/16_bigdata/01_intro/002_bigdata_5v/)) — 블록 128MB, 3중 [복제](/studynote/16_bigdata/01_intro/002_bigdata_5v/), [NameNode](/studynote/16_bigdata/01_intro/002_bigdata_5v/)/[DataNode](/studynote/16_bigdata/01_intro/002_bigdata_5v/)
3. [NameNode](/studynote/16_bigdata/01_intro/003_bigdata_7v/) — [메타데이터 관리](/studynote/16_bigdata/01_intro/003_bigdata_7v/), [SPOF](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 우려 -> Secondary [NameNode](/studynote/16_bigdata/01_intro/003_bigdata_7v/) / HA [NameNode](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
4. [DataNode](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) — 실제 [데이터](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 블록 저장, 주기적 Heartbeat
5. [Rack Awareness](/studynote/16_bigdata/01_intro/005_unstructured_data/) — 같은 랙 두 [복제](/studynote/16_bigdata/01_intro/005_unstructured_data/)본 방지, 장애 [복구](/studynote/16_bigdata/01_intro/005_unstructured_data/) 최적화
6. [MapReduce](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — Map([분산](/studynote/16_bigdata/01_intro/006_semi_structured_data/) 처리)/Shuffle&Sort/Reduce(집계) 3단계
7. Map 함수 — 입력 -> ([Key](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/), Value) 쌍 출력
8. [Reduce 함수 — 동일 Key의 Value 집계, 최종 결과 출력](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)
9. [Shuffle & Sort](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) — Map 출력을 Reduce로 분배 (네트워크 병목)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [YARN](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) ([Yet Another Resource Negotiator](/studynote/16_bigdata/01_intro/020_data_structure_ratio/)) — 자원 관리, Application Master / [Container](/studynote/16_bigdata/10_governance/194_datalineage/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Apache Hive](/studynote/16_bigdata/02_hadoop/028_apache_tez/) — SQL on [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/), HQL, 메타스토어(MySQL/PostgreSQL), 배치형
12. Apache [HBase](/studynote/16_bigdata/01_intro/012_mydata/) — [NoSQL](/studynote/16_bigdata/01_intro/012_mydata/) on [HDFS](/studynote/16_bigdata/01_intro/012_mydata/), 열 지향, 실시간 랜덤 R/W, [ZooKeeper](/studynote/16_bigdata/01_intro/012_mydata/) 의존
13. [Apache Pig](/studynote/16_bigdata/01_intro/013_public_bigdata/) — [데이터](/studynote/16_bigdata/01_intro/013_public_bigdata/) 흐름 스크립트 언어 (Pig Latin), 복잡한 [ETL](/studynote/16_bigdata/01_intro/013_public_bigdata/)
14. [Apache Sqoop](/studynote/16_bigdata/01_intro/014_data_voucher/) — RDBMS ↔ [HDFS](/studynote/16_bigdata/01_intro/014_data_voucher/) [데이터](/studynote/16_bigdata/01_intro/014_data_voucher/) 임포트/익스포트
15. [Apache Flume](/studynote/16_bigdata/01_intro/015_open_data_principles/) — [로그 수집](/studynote/16_bigdata/01_intro/015_open_data_principles/) 에이전트, Source/Channel/Sink 구조
16. [Apache Oozie](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — [Hadoop](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) 워크플로우/코디네이터 [스케줄러](/studynote/16_bigdata/01_intro/016_europe_data_strategy/)
17. [Apache Zookeeper](/studynote/16_bigdata/01_intro/017_national_data_policy/) — [분산](/studynote/16_bigdata/01_intro/017_national_data_policy/) 코디네이션 [서비스](/studynote/16_bigdata/01_intro/017_national_data_policy/), 리더 선출, 잠금
18. [Apache Ambari](/studynote/16_bigdata/01_intro/018_data_sovereignty/) — [Hadoop](/studynote/16_bigdata/01_intro/018_data_sovereignty/) 클러스터 관리 GUI
19. Cloudera CDH / HDP (Hortonworks) -> [CDP](/studynote/16_bigdata/01_intro/019_data_de_identification/) ([Cloudera Data Platform](/studynote/16_bigdata/01_intro/019_data_de_identification/))
20. [Apache Tez](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) — [DAG](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) 기반 실행 엔진, [Hive](/studynote/16_bigdata/01_intro/020_data_structure_ratio/)/Pig 속도 개선
21. [Apache Kafka](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) ([Hadoop](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) 연동) — Flume 대체, 내구성/[처리량](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/)^
22. [Apache Storm](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) — [초기](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) 실시간 처리, Spout/Bolt 토폴로지
23. Apache Samza — LinkedIn, [Kafka](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/) 네이티브 스트리밍
24. [HDFS](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) 페더레이션 ([Federation](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/)) — 다중 [NameNode](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/), [네임스페이스](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) [분산](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/)
25. [HDFS ViewFS](/studynote/16_bigdata/02_hadoop/025_namenode_metadata_spof_ha/) — [파일](/studynote/16_bigdata/02_hadoop/025_namenode_metadata_spof_ha/) 시스템 투명 접근
26. [Small File Problem](/studynote/16_bigdata/02_hadoop/026_apache_zookeeper/) — [HDFS](/studynote/16_bigdata/02_hadoop/026_apache_zookeeper/) 비효율, HAR/Sequence [File](/studynote/16_bigdata/02_hadoop/026_apache_zookeeper/)/ORC로 해결
27. [데이터](/studynote/16_bigdata/02_hadoop/027_oozie_airflow/) [직렬](/studynote/16_bigdata/02_hadoop/027_oozie_airflow/)화 — Avro / [Protocol Buffers](/studynote/16_bigdata/02_hadoop/027_oozie_airflow/) / Thrift / Kryo
28. [Hadoop](/studynote/16_bigdata/02_hadoop/028_apache_tez/) 보안 — [Kerberos](/studynote/16_bigdata/02_hadoop/028_apache_tez/) [인증](/studynote/16_bigdata/02_hadoop/028_apache_tez/), Ranger(권한)/Atlas([카탈로그](/studynote/16_bigdata/02_hadoop/028_apache_tez/))

---

## 3. [분산](/studynote/16_bigdata/06_nosql/136_search_engine_db/) 처리 / 스파크 심화 — 24개

1. [Apache Spark](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — 인메모리 [분산](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 처리, [MapReduce](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 대비 최대 100배 빠름
2. [RDD](/studynote/16_bigdata/01_intro/002_bigdata_5v/) ([Resilient Distributed Dataset](/studynote/16_bigdata/01_intro/002_bigdata_5v/)) — 불변, [분산](/studynote/16_bigdata/01_intro/002_bigdata_5v/), [결함 허용](/studynote/16_bigdata/01_intro/002_bigdata_5v/), Lineage 기반 [복구](/studynote/16_bigdata/01_intro/002_bigdata_5v/)
3. Transformation vs Action — [Lazy Evaluation](/studynote/16_bigdata/01_intro/003_bigdata_7v/) (변환은 [지연](/studynote/16_bigdata/01_intro/003_bigdata_7v/), 액션은 즉시)
4. DataFrame / Dataset — [스키마](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 기반, Catalyst 최적화, Type-[safe](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)
5. [Spark SQL](/studynote/16_bigdata/01_intro/005_unstructured_data/) — SQL [쿼리](/studynote/16_bigdata/01_intro/005_unstructured_data/)로 DataFrame 처리, [Hive](/studynote/16_bigdata/01_intro/005_unstructured_data/) 메타스토어 연동
6. [Catalyst Optimizer](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — [논리](/studynote/16_bigdata/01_intro/006_semi_structured_data/) -> 물리 [실행 계획](/studynote/16_bigdata/01_intro/006_semi_structured_data/) 최적화
7. [Tungsten 엔진](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) — CPU/메모리 최적화, Codegen, Off-[heap](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 메모리
8. [AQE (Adaptive Query Execution) — 런타임 통계 기반 자동 최적화 (Spark 3.0+)](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)
9. [Spark Streaming](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) ([DStream](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)) — 마이크로배치 스트리밍 (구세대)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) — DataFrame [API](/studynote/16_bigdata/01_intro/014_data_voucher/) 스트리밍, 연속 처리, [Watermark](/studynote/16_bigdata/04_streaming/085_watermark/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). MLlib — [분산](/studynote/16_bigdata/06_nosql/136_search_engine_db/) ML [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) ([분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)/회귀/군집/추천/[PCA](/studynote/16_bigdata/08_visualization/163_dashboard_design/))
12. GraphX — [분산](/studynote/16_bigdata/01_intro/012_mydata/) [그래프](/studynote/16_bigdata/01_intro/012_mydata/) 처리, PageRank
13. Spark 배포 모드 — Local / [Standalone](/studynote/16_bigdata/01_intro/013_public_bigdata/) / [YARN](/studynote/16_bigdata/01_intro/013_public_bigdata/) / [Kubernetes](/studynote/16_bigdata/01_intro/013_public_bigdata/) / Mesos
14. [Executor / Driver / Cluster Manager — Spark 실행 구조](/studynote/16_bigdata/01_intro/014_data_voucher/)
15. [Shuffle 최적화 — spark.sql.shuffle.partitions, AQE 코어리스](/studynote/16_bigdata/01_intro/015_open_data_principles/)
16. Spark [직렬](/studynote/16_bigdata/01_intro/016_europe_data_strategy/)화 최적화 (Kryo) — Kryo > Java, [성능](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) 차이
17. Broadcast [Join](/studynote/16_bigdata/01_intro/017_national_data_policy/) — 소규모 테이블을 모든 Executor에 복사
18. [Skew Join](/studynote/16_bigdata/01_intro/018_data_sovereignty/) — [데이터](/studynote/16_bigdata/01_intro/018_data_sovereignty/) 쏠림 해결 (AQE 자동 분할)
19. [파티션 최적화](/studynote/16_bigdata/01_intro/019_data_de_identification/) — repartition / coalesce, 코어 수 × 2~4
20. [체크포인팅](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) ([Checkpointing](/studynote/16_bigdata/01_intro/020_data_structure_ratio/)) — Lineage 단절, 장애 [복구](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) 가속
21. [Spark History Server](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) — 완료 작업 [로그](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) 조회, UI
22. [Delta Lake on Spark](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) — ACID [트랜잭션](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/), MERGE INTO, 타임 트래블
23. [Photon 엔진](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/) ([Databricks](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/)) — 네이티브 벡터화 Spark 실행 엔진
24. [Apache Spark](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) 3.5+ 개선 — ANSI SQL 확대, Python [API](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) 강화

---

## 4. 스트리밍 / 실시간 처리 — 22개

1. [스트리밍 처리 필요성 — 실시간 이상 감지, 즉각 대응 의사결정](/studynote/16_bigdata/01_intro/001_bigdata_definition/)
2. [Apache Flink](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — 상태 기반 스트리밍, 이벤트 시간 처리, Exactly-Once
3. [Flink 아키텍처 — JobManager / TaskManager / JobGraph](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
4. DataStream [API](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) / Table [API](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) & SQL — Flink 두 계층
5. Flink [Savepoint](/studynote/16_bigdata/01_intro/005_unstructured_data/) / Checkpoint — 상태 저장, 재시작 지점
6. [이벤트 시간 (Event Time) vs 처리 시간 (Processing Time)](/studynote/16_bigdata/01_intro/006_semi_structured_data/)
7. [Watermark](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) — [지연](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 이벤트 허용 임계, 늦은 [데이터](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) [트리거](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)
8. [윈도우 연산](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — 텀블링 / 슬라이딩 / [세션](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) / 글로벌 윈도우
9. [정확히 한 번](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) ([Exactly-Once Semantics](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)) — [2PC](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) + Idempotent Sink
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Apache Kafka](/studynote/16_bigdata/11_industry/214_finance_bigdata/) — 내구성 있는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, 스트리밍 기반
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Kafka](/studynote/16_bigdata/09_platform/179_unified_batch_streaming/) [파티셔닝](/studynote/16_bigdata/09_platform/179_unified_batch_streaming/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 키 기반 / 라운드로빈 / 커스텀
12. [Consumer Lag](/studynote/16_bigdata/01_intro/012_mydata/) — [Kafka](/studynote/16_bigdata/01_intro/012_mydata/) 소비 [지연](/studynote/16_bigdata/01_intro/012_mydata/) [모니터](/studynote/16_bigdata/01_intro/012_mydata/)링, Burrow / JMX
13. [Kafka](/studynote/16_bigdata/01_intro/013_public_bigdata/) MirrorMaker 2 — 클러스터 간 [복제](/studynote/16_bigdata/01_intro/013_public_bigdata/), [DR](/studynote/16_bigdata/01_intro/013_public_bigdata/)
14. [Amazon Kinesis](/studynote/16_bigdata/01_intro/014_data_voucher/) [Data](/studynote/16_bigdata/01_intro/014_data_voucher/) Streams — 샤드 기반, AWS 관리형
15. Google Pub/Sub — [Kafka](/studynote/16_bigdata/01_intro/015_open_data_principles/) 대안, GCP, 글로벌 [분산](/studynote/16_bigdata/01_intro/015_open_data_principles/)
16. [Azure Event Hubs](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — [Kafka](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) 호환 [API](/studynote/16_bigdata/01_intro/016_europe_data_strategy/), AMQP 지원
17. [Apache Pulsar](/studynote/16_bigdata/01_intro/017_national_data_policy/) — [Kafka](/studynote/16_bigdata/01_intro/017_national_data_policy/) 대안, 컴퓨팅/스토리지 분리, [멀티 테넌시](/studynote/16_bigdata/01_intro/017_national_data_policy/)
18. [람다 아키텍처](/studynote/16_bigdata/01_intro/018_data_sovereignty/) — 배치([Speed Layer](/studynote/16_bigdata/01_intro/018_data_sovereignty/)) + 실시간(Batch Layer) + Serving Layer
19. [카파 아키텍처](/studynote/16_bigdata/01_intro/019_data_de_identification/) — 스트리밍만으로 단순화, [Kafka](/studynote/16_bigdata/01_intro/019_data_de_identification/) + Flink
20. 스트리밍 SQL — ksqlDB ([Confluent](/studynote/16_bigdata/01_intro/020_data_structure_ratio/)) / Flink SQL / [Spark Structured Streaming](/studynote/16_bigdata/01_intro/020_data_structure_ratio/)
21. [CEP](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) ([Complex Event Processing](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/)) — 패턴 이벤트 감지, Flink [CEP](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/)
22. 실시간 [OLAP](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) — Apache Druid / Apache Pinot / ClickHouse — ms [지연](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/) [쿼리](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/)

---

## 5. 빅데이터 분석 기법 — 26개

1. [기술 통계](/studynote/16_bigdata/01_intro/001_bigdata_definition/) ([Descriptive Statistics](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) — 평균/중앙값/[분산](/studynote/16_bigdata/01_intro/001_bigdata_definition/)/분포 요약
2. [추론 통계](/studynote/16_bigdata/01_intro/002_bigdata_5v/) ([Inferential Statistics](/studynote/16_bigdata/01_intro/002_bigdata_5v/)) — 표본 -> 모집단 추론, [가설 검정](/studynote/16_bigdata/01_intro/002_bigdata_5v/)
3. [탐색적 데이터 분석](/studynote/16_bigdata/01_intro/003_bigdata_7v/) ([EDA](/studynote/16_bigdata/01_intro/003_bigdata_7v/)) — 패턴 발견, [이상치 탐지](/studynote/16_bigdata/01_intro/003_bigdata_7v/), [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
4. [회귀 분석](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) (Regression) — 단순/다중/다항/릿지/라쏘/엘라스틱넷
5. [분류](/studynote/16_bigdata/01_intro/005_unstructured_data/) ([Classification](/studynote/16_bigdata/01_intro/005_unstructured_data/)) — [로지스틱 회귀](/studynote/16_bigdata/01_intro/005_unstructured_data/) / 트리 / [SVM](/studynote/16_bigdata/01_intro/005_unstructured_data/) / [앙상블](/studynote/16_bigdata/01_intro/005_unstructured_data/)
6. [군집화](/studynote/16_bigdata/01_intro/006_semi_structured_data/) ([Clustering](/studynote/16_bigdata/01_intro/006_semi_structured_data/)) — K-Means / [DBSCAN](/studynote/16_bigdata/01_intro/006_semi_structured_data/) / 계층적 / Gaussian Mixture
7. [연관 규칙](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) ([Association Rules](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)) — Apriori / [FP](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)-Growth, [지지도](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)/[신뢰도](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)/[향상도](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)
8. [장바구니 분석](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) ([Market Basket Analysis](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)) — 구매 패턴, 교차 판매
9. [감성 분석](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) ([Sentiment Analysis](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)) — 긍/부정/중립, [BERT](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) 기반 심화
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [텍스트 마이닝](/studynote/16_bigdata/05_analysis/109_text_mining/) ([Text Mining](/studynote/16_bigdata/05_analysis/109_text_mining/)) — [TF-IDF](/studynote/16_bigdata/12_trends/232_olap_druid_pinot_clickhouse_starrocks/) / [Word2Vec](/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) / [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) / [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [소셜 네트워크 분석](/studynote/16_bigdata/05_analysis/107_market_basket_analysis/) ([SNA](/studynote/16_bigdata/05_analysis/107_market_basket_analysis/)) — 중심성 / 커뮤니티 탐지 / 영향력
12. [이상 탐지](/studynote/16_bigdata/01_intro/012_mydata/) ([Anomaly Detection](/studynote/16_bigdata/01_intro/012_mydata/)) — 통계 기반 / ML 기반 / 딥러닝 기반
13. [시계열 분석](/studynote/16_bigdata/01_intro/013_public_bigdata/) (Time Series) — [ARIMA](/studynote/16_bigdata/01_intro/013_public_bigdata/) / SARIMA / Prophet / [LSTM](/studynote/16_bigdata/01_intro/013_public_bigdata/) / [Transformer](/studynote/16_bigdata/01_intro/013_public_bigdata/)
14. [공간 분석](/studynote/16_bigdata/01_intro/014_data_voucher/) ([Spatial Analysis](/studynote/16_bigdata/01_intro/014_data_voucher/)) — 지리정보시스템(GIS), PostGIS
15. [그래프 분석](/studynote/16_bigdata/01_intro/015_open_data_principles/) ([Graph Analytics](/studynote/16_bigdata/01_intro/015_open_data_principles/)) — PageRank / 커뮤니티 탐지 / 최단 경로
16. [텍스트 요약](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — 추출적(Extractive) / 추상적(Abstractive) 요약
17. [토픽 모델링](/studynote/16_bigdata/01_intro/017_national_data_policy/) — LDA / BERTopic / NMF
18. [개체명 인식](/studynote/16_bigdata/01_intro/018_data_sovereignty/) ([NER](/studynote/16_bigdata/01_intro/018_data_sovereignty/)) — 인물/장소/조직/날짜 추출
19. [이미지 분석](/studynote/16_bigdata/01_intro/019_data_de_identification/) — [CNN](/studynote/16_bigdata/01_intro/019_data_de_identification/) 기반 [분류](/studynote/16_bigdata/01_intro/019_data_de_identification/)/탐지/분할 대용량 배치
20. [로그 분석](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) — 이상 감지, 보안 이벤트, 패턴 발견
21. [클릭스트림 분석](/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) — 사용자 행동 패턴, 전환율 최적화
22. [A/B 테스트 — 실험적 방법론, 통계적 유의성](/studynote/16_bigdata/01_intro/022_small_data_qualitative_analysis/)
23. [추천 시스템](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/) — [협업 필터링](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/) / 콘텐츠 기반 / 하이브리드
24. [예측 분석](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/) ([Predictive Analytics](/studynote/16_bigdata/02_hadoop/024_hdfs_hadoop_distributed_file_system_block/)) — 이탈 예측, 대출 부도, 장비 고장
25. 처방적 분석 ([Prescriptive Analytics](/studynote/16_bigdata/02_hadoop/025_namenode_metadata_spof_ha/)) — 최적 의사결정 제안
26. [인과 추론](/studynote/16_bigdata/02_hadoop/026_apache_zookeeper/) ([Causal Inference](/studynote/16_bigdata/02_hadoop/026_apache_zookeeper/)) — 상관≠인과, DoWhy, 반사실 분석

---

## 6. [NoSQL](/studynote/16_bigdata/02_hadoop/035_yarn_resource_negotiator/) [데이터베이스](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — 20개

1. [NoSQL](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 등장 배경 — RDBMS 수평 확장 한계, BASE 원칙
2. BASE 원칙 — Basically Available / Soft [State](/studynote/16_bigdata/01_intro/002_bigdata_5v/) / Eventually Consistent
3. [CAP](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 정리 — [Consistency](/studynote/16_bigdata/01_intro/003_bigdata_7v/) / [Availability](/studynote/16_bigdata/01_intro/003_bigdata_7v/) / [Partition](/studynote/16_bigdata/01_intro/003_bigdata_7v/) Tolerance (2개만 선택)
4. [PACELC](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 이론 — [CAP](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 확장, [지연](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) vs [일관성](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 트레이드오프
5. 키-값 ([Key](/studynote/16_bigdata/01_intro/005_unstructured_data/)-Value) DB — [Redis](/studynote/16_bigdata/01_intro/005_unstructured_data/) / [DynamoDB](/studynote/16_bigdata/01_intro/005_unstructured_data/) / Riak — 빠른 조회, 단순 구조
6. [Redis](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — 인메모리, Pub/Sub, 자료구조(String/List/Set/Hash/ZSet), 클러스터
7. 문서형 ([Document](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)) DB — [MongoDB](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) / CouchDB / Firestore
8. [MongoDB](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 아키텍처 — [ReplicaSet](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) / [Sharding](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) / Mongos / [Config](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) Server
9. 컬럼 패밀리 (Column Family) DB — [Cassandra](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) / [HBase](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) / ScyllaDB
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) — [마스](/studynote/16_bigdata/08_visualization/172_network_visualization/)터 없는 링 구조, 토큰 기반 [일관성](/studynote/16_bigdata/10_governance/194_datalineage/) 해시, 튜닝 가능한 [일관성](/studynote/16_bigdata/10_governance/194_datalineage/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [그래프](/studynote/16_bigdata/03_spark/070_partition_optimization/) DB — Neo4j / Amazon Neptune / Memgraph — [관계](/studynote/16_bigdata/04_streaming/083_flink_savepoint_checkpoint/) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화
12. Cypher [쿼리](/studynote/16_bigdata/01_intro/012_mydata/) 언어 (Neo4j) — MATCH / WHERE / RETURN
13. 시계열 DB — [InfluxDB](/studynote/16_bigdata/01_intro/013_public_bigdata/) / TimescaleDB / QuestDB — 시간 기반 인덱싱
14. 검색 엔진 DB — [Elasticsearch](/studynote/16_bigdata/01_intro/014_data_voucher/) / OpenSearch — [역색인](/studynote/16_bigdata/01_intro/014_data_voucher/), 전문 검색
15. 다중 모델 DB — ArangoDB / SurrealDB — 여러 [NoSQL](/studynote/16_bigdata/01_intro/015_open_data_principles/) 모델 지원
16. [NewSQL](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — [CockroachDB](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) / [TiDB](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) / YugabyteDB — SQL + 수평 확장 + ACID
17. 인메모리 DB — [Redis](/studynote/16_bigdata/01_intro/017_national_data_policy/) / Memcached / SAP HANA — 마이크로초 응답
18. [일관성 수준 선택](/studynote/16_bigdata/01_intro/018_data_sovereignty/) — Strong / Bounded Staleness / [Session](/studynote/16_bigdata/01_intro/018_data_sovereignty/) / Consistent Prefix / Eventual
19. [멀티 마스터 복제](/studynote/16_bigdata/01_intro/019_data_de_identification/) — CouchDB / [DynamoDB](/studynote/16_bigdata/01_intro/019_data_de_identification/) Global Tables
20. [스키마리스 설계 패턴](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) — [임베딩](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) vs [참조](/studynote/16_bigdata/01_intro/020_data_structure_ratio/), [데이터](/studynote/16_bigdata/01_intro/020_data_structure_ratio/) 중복 허용 설계

---

## 7. [데이터 레이크](/studynote/16_bigdata/10_governance/208_data_deidentification_techniques/) / [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) — 18개

1. [데이터 레이크](/studynote/16_bigdata/01_intro/001_bigdata_definition/) ([Data Lake](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) — 원시 [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 저장, [Schema-on-Read](/studynote/16_bigdata/01_intro/001_bigdata_definition/), 저비용
2. [데이터](/studynote/16_bigdata/01_intro/002_bigdata_5v/) 스왐프 ([Data Swamp](/studynote/16_bigdata/01_intro/002_bigdata_5v/)) — 거버넌스 부재, 레이크 변질 위험
3. [데이터 웨어하우스](/studynote/16_bigdata/01_intro/003_bigdata_7v/) ([DW](/studynote/16_bigdata/01_intro/003_bigdata_7v/)) — 구조화, [Schema-on-Write](/studynote/16_bigdata/01_intro/003_bigdata_7v/), 높은 [성능](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
4. [레이크하우스](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) ([Lakehouse](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)) — 레이크(유연성) + [DW](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)(ACID/[성능](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)), [Delta Lakehouse](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)
5. [Delta Lake](/studynote/16_bigdata/01_intro/005_unstructured_data/) — ACID on [Parquet](/studynote/16_bigdata/01_intro/005_unstructured_data/), 타임 트래블, MERGE, [스키마](/studynote/16_bigdata/01_intro/005_unstructured_data/) 강제
6. [Apache Iceberg](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — [오픈 테이블 포맷](/studynote/16_bigdata/01_intro/006_semi_structured_data/), 히든 [파티셔닝](/studynote/16_bigdata/01_intro/006_semi_structured_data/), [스냅샷](/studynote/16_bigdata/01_intro/006_semi_structured_data/)
7. [Apache Hudi](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) ([Hadoop Upserts Deletes Incrementals](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)) — Uber, [CDC](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 지원
8. [Unity Catalog](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) ([Databricks](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)) — [레이크하우스](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 통합 거버넌스
9. [다중 계층 아키텍처](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) — Bronze(원시) / Silver(정제) / Gold(집계) — Medallion
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [Medallion Architecture](/studynote/16_bigdata/10_governance/194_datalineage/) — [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 기반 3계층, [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 표준
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [데이터 메시](/studynote/16_bigdata/10_governance/211_data_ethics/) ([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)) — [도메인](/studynote/16_bigdata/03_spark/064_spark_deployment_modes/) 분권, [데이터 제품](/studynote/16_bigdata/07_data_lake/154_data_product/)화, 연합 거버넌스
12. [데이터 제품](/studynote/16_bigdata/01_intro/012_mydata/) ([Data Product](/studynote/16_bigdata/01_intro/012_mydata/)) — [API](/studynote/16_bigdata/01_intro/012_mydata/) 인터페이스, [SLA](/studynote/16_bigdata/01_intro/012_mydata/), 품질 지표 보유
13. [ELT vs ETL](/studynote/16_bigdata/01_intro/013_public_bigdata/) — 클라우드에서 ELT가 주류 (먼저 적재 후 변환)
14. [데이터 패브릭](/studynote/16_bigdata/01_intro/014_data_voucher/) ([Data Fabric](/studynote/16_bigdata/01_intro/014_data_voucher/)) — 위치 무관 지능형 [데이터](/studynote/16_bigdata/01_intro/014_data_voucher/) 연결, Gartner
15. [데이터](/studynote/16_bigdata/01_intro/015_open_data_principles/) 분석 [서비스](/studynote/16_bigdata/01_intro/015_open_data_principles/) — Amazon EMR / Azure HDInsight / GCP Dataproc
16. [Databricks](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — Spark 기반 [레이크하우스](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) 플랫폼, [Unity Catalog](/studynote/16_bigdata/01_intro/016_europe_data_strategy/)
17. [Snowflake](/studynote/16_bigdata/01_intro/017_national_data_policy/) on [Data Lake](/studynote/16_bigdata/01_intro/017_national_data_policy/) — External Table, Iceberg 지원
18. [Microsoft Fabric](/studynote/16_bigdata/01_intro/018_data_sovereignty/) — One Lake, [Power BI](/studynote/16_bigdata/01_intro/018_data_sovereignty/) + Synapse + [Data](/studynote/16_bigdata/01_intro/018_data_sovereignty/) Factory 통합

---

## 8. 빅데이터 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) — 14개

1. [데이터 시각화 원칙](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — 목적 명확성 / 간결성 / [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 잉크 비율 (Tufte)
2. [차트 유형 선택](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — 비교(막대)/추세(선)/비율(파이/도넛)/분포(히스토그램/박스)
3. [대시보드 설계](/studynote/16_bigdata/01_intro/003_bigdata_7v/) — [KPI](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 중심, 5초 규칙, 인터랙티브
4. [Tableau](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) — 드래그앤드롭, VizQL, Extract/Live 연결
5. [Power BI](/studynote/16_bigdata/01_intro/005_unstructured_data/) — Microsoft 생태계 통합, DAX, Dataflow
6. [Looker](/studynote/16_bigdata/01_intro/006_semi_structured_data/) / [Looker](/studynote/16_bigdata/01_intro/006_semi_structured_data/) Studio — Google, LookML 시맨틱 레이어
7. [Apache Superset](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) — [오픈소스](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/), SQL Lab, 다양한 차트
8. [Grafana](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — [메트릭](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)/[로그](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)/추적 통합 [시각화](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/), 알람
9. [Kibana](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) — ELK [Stack](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) [시각화](/studynote/16_bigdata/01_intro/009_data_explosion_factors/), [로그 분석](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). D3.js — JavaScript 기반 커스텀 인터랙티브 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). Plotly / [Dash](/studynote/03_network/09_application_layer_web_email/510_dash_dynamic_adaptive_streaming_over_http/) — Python 기반 인터랙티브 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
12. [네트워크 시각화](/studynote/16_bigdata/01_intro/012_mydata/) — Gephi / Cytoscape — [그래프](/studynote/16_bigdata/01_intro/012_mydata/) [시각화](/studynote/16_bigdata/01_intro/012_mydata/)
13. [지리공간 시각화](/studynote/16_bigdata/01_intro/013_public_bigdata/) — Kepler.gl / Folium / Deck.gl — 지도 기반
14. [빅데이터 시각화 도전](/studynote/16_bigdata/01_intro/014_data_voucher/) — 수십억 개 포인트, 집계/샘플링/렌더링 최적화

---

## 9. 빅데이터 플랫폼 / 아키텍처 — 16개

1. [빅데이터 플랫폼 선택 기준](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 규모 / 실시간 여부 / 비용 / 기술 역량
2. [On-Premise](/studynote/16_bigdata/01_intro/002_bigdata_5v/) [Hadoop](/studynote/16_bigdata/01_intro/002_bigdata_5v/) vs Cloud 비교 — [초기](/studynote/16_bigdata/01_intro/002_bigdata_5v/) 비용 vs OPEX, 유연성
3. [빅데이터 참조 아키텍처](/studynote/16_bigdata/01_intro/003_bigdata_7v/) — 수집->저장->처리->분석->[서비스](/studynote/16_bigdata/01_intro/003_bigdata_7v/)->관리
4. [모던 데이터 스택](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) ([MDS](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)) — Fivetran + [Snowflake](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) + dbt + [Tableau](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)
5. [실시간 + 배치 통합 플랫폼 — Unified Batch/Streaming (Spark/Flink)](/studynote/16_bigdata/01_intro/005_unstructured_data/)
6. [데이터 허브](/studynote/16_bigdata/01_intro/006_semi_structured_data/) ([Data Hub](/studynote/16_bigdata/01_intro/006_semi_structured_data/)) — 중앙 [데이터](/studynote/16_bigdata/01_intro/006_semi_structured_data/) 집계 및 배포 계층
7. [멀티클라우드 데이터 플랫폼](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) — [Snowflake](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) / [Databricks](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 멀티클라우드 지원
8. [서버리스 빅데이터](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — AWS Athena / [BigQuery](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) / Redshift [Serverless](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/)
9. [데이터 오케스트레이션](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) — [Apache Airflow](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) / Dagster / Prefect
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터 카탈로그 통합](/studynote/16_bigdata/09_platform/184_data_catalog_integration/) — Glue [Catalog](/studynote/05_database/07_exam_summary/394_catalog_metadata/) / DataHub / OpenMetadata / Alation
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [확장성 설계](/studynote/16_bigdata/09_platform/185_scalability_design/) — 수평 확장 / [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) / [파티셔닝](/studynote/16_bigdata/09_platform/179_unified_batch_streaming/) / 클러스터 자동 확장
12. [데이터 컴프레션 전략](/studynote/16_bigdata/01_intro/012_mydata/) — Snappy(속도) / Zstd([압축](/studynote/16_bigdata/01_intro/012_mydata/)률) / Gzip([호환성](/studynote/16_bigdata/01_intro/012_mydata/))
13. [컬럼 기반 파일 포맷](/studynote/16_bigdata/01_intro/013_public_bigdata/) — [Parquet](/studynote/16_bigdata/01_intro/013_public_bigdata/) / ORC / Iceberg / Arrow — 조회 최적화
14. [빅데이터 비용 최적화](/studynote/16_bigdata/01_intro/014_data_voucher/) — [Spot Instance](/studynote/16_bigdata/01_intro/014_data_voucher/) / 컴퓨팅-스토리지 분리 / RI
15. [데이터 이동 비용](/studynote/16_bigdata/01_intro/015_open_data_principles/) — [Egress](/studynote/16_bigdata/01_intro/015_open_data_principles/) 비용, 리전 내 [데이터](/studynote/16_bigdata/01_intro/015_open_data_principles/) 로컬화
16. [하이브리드 분석](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — [온프레미스](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) + 클라우드 [버스](/studynote/16_bigdata/01_intro/016_europe_data_strategy/)팅

---

## [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 빅데이터 거버넌스 / 품질 / 법규 — 18개

1. [데이터 거버넌스 정의](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 소유·관리·사용 원칙 체계
2. [데이터 거버넌스 구성 요소](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — [정책](/studynote/16_bigdata/01_intro/002_bigdata_5v/)/표준/역할/프로세스/도구
3. [데이터 스튜어드](/studynote/16_bigdata/01_intro/003_bigdata_7v/) ([Data Steward](/studynote/16_bigdata/01_intro/003_bigdata_7v/)) — [도메인](/studynote/16_bigdata/01_intro/003_bigdata_7v/) [데이터](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 책임자
4. [데이터 소유자](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) ([Data Owner](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)) — 비즈니스 책임, 접근 승인
5. [데이터 품질 차원](/studynote/16_bigdata/01_intro/005_unstructured_data/) — 완전성/[정확성](/studynote/16_bigdata/01_intro/005_unstructured_data/)/[일관성](/studynote/16_bigdata/01_intro/005_unstructured_data/)/적시성/유일성/유효성
6. [데이터 품질 관리 도구](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — Great Expectations / Deequ / Soda Core
7. [데이터](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 계보 ([Data Lineage](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)) — 열 수준 계보, 영향 분석, Apache Atlas
8. [메타데이터 관리](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — 비즈니스/기술/운영 [메타데이터](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 3유형
9. [마스터 데이터 관리](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) ([MDM](/studynote/16_bigdata/01_intro/009_data_explosion_factors/)) — 황금 레코드, 중복 제거
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 보안 — 암호화(전송/저장) / 접근 제어 / [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) / [DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [개인정보보호법 빅데이터 특례](/studynote/16_bigdata/10_governance/206_pipa_bigdata_exception/) — 가명처리 허용 (2020년 [데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 3법)
12. [GDPR Article 89](/studynote/16_bigdata/01_intro/012_mydata/) — 과학적 연구 목적 빅데이터 처리 특례
13. [데이터 비식별화 기법](/studynote/16_bigdata/01_intro/013_public_bigdata/) — [데이터 마스킹](/studynote/16_bigdata/01_intro/013_public_bigdata/) / 가명화 / 집계화 / 노이즈 추가
14. [차등 프라이버시](/studynote/16_bigdata/01_intro/014_data_voucher/) ([Differential Privacy](/studynote/16_bigdata/01_intro/014_data_voucher/)) — 통계 [쿼리](/studynote/16_bigdata/01_intro/014_data_voucher/) + 노이즈, Apple/Google
15. [합성 데이터](/studynote/16_bigdata/01_intro/015_open_data_principles/) ([Synthetic Data](/studynote/16_bigdata/01_intro/015_open_data_principles/)) — 원본과 유사 통계적 특성, [개인정보](/studynote/16_bigdata/01_intro/015_open_data_principles/) 대체
16. [데이터 윤리](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) ([Data Ethics](/studynote/16_bigdata/01_intro/016_europe_data_strategy/)) — [알고리즘](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) 편향, 공정성, 투명성
17. [빅데이터 분쟁](/studynote/16_bigdata/01_intro/017_national_data_policy/) — [데이터](/studynote/16_bigdata/01_intro/017_national_data_policy/) 소유권, 수집 동의, 목적 외 사용
18. [데이터 감사](/studynote/16_bigdata/01_intro/018_data_sovereignty/) ([Data Audit](/studynote/16_bigdata/01_intro/018_data_sovereignty/)) — 접근 이력, 변경 이력, 보관 기간

---

## [11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 빅데이터 산업 응용 — 16개

1. [금융 빅데이터](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — 신용평가 / 이상거래탐지([FDS](/studynote/16_bigdata/01_intro/001_bigdata_definition/)) / [리스크](/studynote/16_bigdata/01_intro/001_bigdata_definition/) 관리 / 알고트레이딩
2. [의료 빅데이터](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — 전자의무기록(EMR) / 유전체 분석 / 임상 예측 / 신약 개발
3. 공공 [데이터](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 활용 — 교통 예측 / 범죄 예방 / 도시 계획 / 행정 [서비스](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 개선
4. [제조 빅데이터](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) — 예지 정비([PdM](/studynote/16_bigdata/01_intro/004_bigdata_necessity/)) / 불량 감지 / 에너지 최적화
5. [유통·물류 빅데이터 — 수요 예측 / 재고 최적화 / 배송 경로 최적화](/studynote/16_bigdata/01_intro/005_unstructured_data/)
6. [미디어 빅데이터](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — 시청 분석 / 콘텐츠 추천 / 광고 타겟팅
7. [SNS 빅데이터 — 여론 분석 / 트렌드 감지 / 인플루언서 분석](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)
8. [스마트시티 빅데이터](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — [CCTV](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 분석 / 교통 [신호](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 최적화 / 에너지 그리드
9. [농업 빅데이터](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) — 정밀 농업 / 날씨 연계 수확량 예측 / 토양 분석
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [교육 빅데이터](/studynote/16_bigdata/11_industry/223_education_bigdata/) — 학습 분석([Learning](/studynote/16_bigdata/12_trends/240_databricks_vs_snowflake_dw/) Analytics) / 맞춤형 교육
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [관광 빅데이터](/studynote/16_bigdata/11_industry/224_tourism_bigdata/) — 관광 수요 예측 / 혼잡도 분석 / 관광 코스 추천
12. [통신 빅데이터](/studynote/16_bigdata/01_intro/012_mydata/) — 네트워크 장애 예측 / 고객 이탈 분석 / QoE 최적화
13. [에너지 빅데이터](/studynote/16_bigdata/01_intro/013_public_bigdata/) — 전력 수요 예측 / 신재생에너지 출력 예측 / 스마트미터
14. [보험 빅데이터](/studynote/16_bigdata/01_intro/014_data_voucher/) — 보험료 산정 / 사기 탐지 / 언더라이팅 자동화
15. [부동산 빅데이터](/studynote/16_bigdata/01_intro/015_open_data_principles/) — 시세 예측 / 상권 분석 / 인구 이동 분석
16. [국방 빅데이터](/studynote/16_bigdata/01_intro/016_europe_data_strategy/) — 정보 분석 / 적 행동 예측 / 보안 위협 탐지

---

## 12. 최신 빅데이터 동향 — 12개

1. [레이크하우스 주류화](/studynote/16_bigdata/01_intro/001_bigdata_definition/) — Delta/Iceberg/Hudi 3강 경쟁, 개방형 포맷
2. [데이터 메시 확산](/studynote/16_bigdata/01_intro/002_bigdata_5v/) — [도메인](/studynote/16_bigdata/01_intro/002_bigdata_5v/) 소유권, 자율 [데이터 제품](/studynote/16_bigdata/01_intro/002_bigdata_5v/)
3. 실시간 [OLAP](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 성장 — Druid / Pinot / ClickHouse / StarRocks
4. [AI](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) + 빅데이터 융합 — 대규모 ML 학습, [LLM](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 기반 [데이터](/studynote/16_bigdata/01_intro/004_bigdata_necessity/) 분석
5. [Text-to-SQL on BigData](/studynote/16_bigdata/01_intro/005_unstructured_data/) — LLM으로 자연어 -> [쿼리](/studynote/16_bigdata/01_intro/005_unstructured_data/) 자동 [생성](/studynote/16_bigdata/01_intro/005_unstructured_data/)
6. [스트리밍 우선 아키텍처](/studynote/16_bigdata/01_intro/006_semi_structured_data/) — 배치 -> 스트리밍 전환, [Kappa](/studynote/16_bigdata/01_intro/006_semi_structured_data/) 아키텍처 강화
7. [데이터 계약](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) ([Data Contract](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/)) — [스키마](/studynote/16_bigdata/01_intro/007_big_data_ecosystem/) 안정성 보장 생산자-소비자 합의
8. [오픈소스 포맷 경쟁](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) — [Apache Iceberg](/studynote/16_bigdata/01_intro/008_big_data_vs_traditional_data/) 사실상 표준화 움직임
9. [양자 컴퓨팅](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) + 빅데이터 — 최적화 문제, 양자 ML [초기](/studynote/16_bigdata/01_intro/009_data_explosion_factors/) 연구
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [엣지 빅데이터](/studynote/16_bigdata/12_trends/239_architecture/) — 엣지에서 집계 후 클라우드 전송, [대역폭](/studynote/16_bigdata/06_nosql/140_consistency_levels/) 절감
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [Databricks vs Snowflake](/studynote/16_bigdata/12_trends/240_databricks_vs_snowflake_dw/) — [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) vs [DW](/studynote/16_bigdata/10_governance/209_differential_privacy/) 진영 경쟁
12. [데이터 옵저버빌리티](/studynote/16_bigdata/01_intro/012_mydata/) — Monte Carlo / Bigeye — [데이터 파이프라인](/studynote/16_bigdata/01_intro/012_mydata/) [신뢰성](/studynote/16_bigdata/01_intro/012_mydata/)

---

**총 키워드 수: 216개**
