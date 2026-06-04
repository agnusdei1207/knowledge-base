---
title: "3. 반정형 데이터 (Semi-structured Data) - 데이터 내부(태그)에 구조(메타데이터)를 포함 (XML, JSON, 로그)"
date: "2024-05-24"
description: "데이터 내부에 메타데이터(태그,スキーマ)를 포함하는 XML, JSON, 로그 등의 반정형 데이터 유형, NoSQL과 메시지 큐에서의 활용"
tags:
  - "data_engineering"
---


# 03. 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Semi-structured [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 고정된 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)( [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) )가 없지만, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에 태그( Tag )나 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)( [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) )를 내장하여 자체적으로 구조를 기술한다.
> 2. **유연성**: XML( Extensible Markup Language ), [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)( JavaScript Object Notation ), CSV, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 등이 대표적이며, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화( [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution )에 유리하여 [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 환경에서 자주 사용된다.
> 3. **한계**: 관계형 연산( [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/), 집계 )의 효율이 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)보다 낮아, 대규모 분석에는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 엔진( Spark, Flink )와의 연동이 필수적이다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)( Semi-structured [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) )와은/는사전정의된고정スキーマ 없이도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)( 태그, 요소, [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) )를 포함하여 스스로의 구조를 표현하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형을 말한다. 이는 기존의 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)( RDBMS 테이블 )처럼 엄격한 열( Column ) 정의가 필요하지 않으면서도, 완전한 무정형( Unstructured ) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)( 이미지, 영상, 음성 )보다는 내재된 구조를 갖고 있다.
대표적인 예로서, 웹 문서의 HTML, 이메일의 [MIME](/studynote/03_network/09_application_layer_web_email/492_mime_multipurpose_internet_mail_extensions/), [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 XML,[REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API의 요청/응답 몸체인 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), 서버/애플리케이션 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 등이 있다. 이러한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들은 개발자가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 동적으로 정의할 수 있어,업무의변화에 빠르게 대응해야 하는현대적연건개발 환경에서 선호된다.
특히, [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)( [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) )에서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신은 대부분 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 기반의 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API로 이루어지며, [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기에서 발생하는 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 또는 CSV 형태로 전달된다. 이러한 맥락에서 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 처리는 현대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼에서 필수적인 기술 역량으로 부상하였다.

[반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 대표 유형과 구조적 특성 도식도]
```text
[반정형 데이터 유형 매트릭스]

+-----------------------------------------------------------------+
|  데이터 유형          구조 표현 방식          활용 분야          |
+-----------------------------------------------------------------+
|  JSON                키-값 쌍의 계층 구조      REST API, 설정 파일  |
|  {                   (네스티드/중첩 구조)                       |
|    "name": "홍길동",                                           |
|    "age": 30,                                                  |
|    "address": {                                                |
|      "city": "서울",                                           |
|      "district": "강남구"                                      |
|    }                                                           |
|  }                                                              |
+-----------------------------------------------------------------+
|  XML                태그( <tag> ) 기반 계층      웹 문서, 설정 파일  |
|  <person>                                                        |
|    <name>홍길동</name>                                         |
|    <address>                                                   |
|      <city>서울</city>                                         |
|    </address>                                                  |
|  </person>                                                     |
+-----------------------------------------------------------------+
|  CSV                컴마/탭 분리된 평면 테이블    로그, 내보내기 파일  |
|  name,age,city                                                     |
|  홍길동,30,서울                                                   |
|  김철수,25,부산                                                   |
+-----------------------------------------------------------------+
|  로그 파일          타임스탬프 + 레벨 + 메시지     서버/앱 로그 분석   |
|  2024-01-01 10:00:00 ERROR [Auth] Login failed for user: admin   |
+-----------------------------------------------------------------+
```
이 도식은 대표적인 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형들의 구조적 특성을 비교한다. JSON은 키-값 쌍의 중첩( Nested ) 구조로 복잡한 계층을 표현할 수 있어 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와([NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/)) [Document](/studynote/14_data_engineering/01_infrastructure/037_document/) DB에최적. XML은 시작/종료 태그로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 감싸는Markup 언어로, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에력사적으로 많이 사용되었다. CSV는최간단적한 평면 구조로 스프레드시트 내보내기나 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 활용된다. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 반정형이라기보다는 비정형에 가깝지만, 정규식( Regular Expression )을리용하여 구조화할 수 있는 특성이 있다.

📢 **섹션 요약 비유**: 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는수사록기처럼 그날그날의상황을 자유로운 문장으로 적어두지만, 그래도"날짜,날씨,하루 목표" 같은 항목은 항상 포함하는 다이어리와 같다. 항목 이름( 태그/키 )은 있지만 혈마다 실제 내용이 다르므로 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)나양적엄격적표결구는 아니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 그 내재적 유연성으로 인해 다양한 저장소와 처리 엔진에서 활용되며, 각각 특화된 기술 스택이 존재한다.

| 반정형 유형 | 핵심 저장소 | 처리 엔진 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/11_design_supervision/06_exam_summary/343_json/">JSON</a></strong> | [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Elasticsearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), Couchbase | Spark, Flink, Trino | 유연한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 친화 | 중첩흔심시 조회 복잡 |
| **XML** | MarkLogic, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) XML DB | Spark, DataStage | 구조적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(XSD) 가능 | 파싱 오버헤드 큼 |
| <strong>CSV/<a href="/studynote/01_computer_architecture/14_hardware_security_trends/496_tsv/">TSV</a></strong> | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), S3, MySQL | Spark, Pandas, Airflow |シンプル에서보편성 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 추론 필요 |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong> | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [Elasticsearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), S3 | Flink, Logstash, [Splunk](/studynote/09_security/13_secops_ir_forensics/630_splunk/) | 실시간 분석 가능 | 검색성능 제한 |
| **Avro** | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) ([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)) | Spark, Flink | 바이너리고효, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)진화지지 | 바이너리 직접 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 어려움 |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/">Protocol Buffers</a></strong> | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 통신, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | Spark (SparkSQL) | 강력한 타입,スキーマ검정 | 이기종 언어한정 |

[반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 아키텍처]
```text
[반정형 JSON 데이터의 수집에서 분석까지의 파이프라인]
+---------------------------------------------------------------------+
|  [데이터 소스 계층]                                                   |
|  +-----------+  +-----------+  +-----------+  +-----------+        |
|  |REST API   |  |IoT Sensors|  |Mobile App |  |Web Log    |        |
|  |(JSON)     |  |(JSON)     |  |(JSON)     |  |(Log/CSV)  |        |
|  +-----+-----+  +-----+-----+  +-----+-----+  +-----+-----+        |
|        |              |              |              |               |
|        +--------------+--------------+--------------+               |
|                              | (HTTP POST / MQTT / SDK)            |
|                              v                                      |
|  [수집 계층]  ---------------------------------------------          |
|  +---------------------------------------------------------+        |
|  |              Apache Kafka (토픽: user-events)            |        |
|  |  +---------+---------+---------+---------+---------+  |        |
|  |  |Partition|Partition|Partition|Partition|Partition|  |        |
|  |  |   0     |   1     |   2     |   3     |   4     |  |        |
|  |  +---------+---------+---------+---------+---------+  |        |
|  +---------------------------------------------------------+        |
|                              |                                     |
|                              v (Consumer Group 병렬 처리)            |
|  [처리 계층]  ---------------------------------------------          |
|  +---------------------------------------------------------+        |
|  |           Apache Flink (반정형 JSON 파싱/변환)           |        |
|  |                                                         |        |
|  |  fromKafka("user-events")                               |        |
|  |    .filter(x => x.eventType == "purchase")             |        |
|  |    .keyBy(x => x.userId)                               |        |
|  |    .window(TumblingEventTimeWindows.of(Time.minutes(5)))|        |
|  |    .sum("amount")                                       |        |
|  +---------------------------------------------------------+        |
|                              |                                     |
|                              v (Parquet / ORC 압축 적재)             |
|  [저장 계층]  ---------------------------------------------          |
|  +---------------------------------------------------------+        |
|  |              Data Lake (S3 / HDFS)                     |        |
|  |  +-------------------------------------------------+    |        |
|  |  |  user-events/year=2024/month=01/day=15/        |    |        |
|  |  |    part-00000.snappy.parquet (압축: 10:1)       |    |        |
|  |  +-------------------------------------------------+    |        |
|  +---------------------------------------------------------+        |
|                              |                                     |
|                              v (Trino Federated Query)              |
|  [분석 계층]  ---------------------------------------------          |
|  +---------------------------------------------------------+        |
|  |              BI / ML Tools (Tableau, Jupyter)           |        |
|  +---------------------------------------------------------+        |
+---------------------------------------------------------------------+
```
이 구조는 반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서에서 발생하여 Kafka에 수집되고, Flink에서 실시간으로 파싱 및 윈도우 집계된 후, 최종적으로 Parquet형식에서Data Lake에 저장되어 분석되는전과정을 보여준다. 핵심적인리점은 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의령활성과[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리의スケーラビリティ을 결합하여, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변화( [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution )에도 유연하게 대응할 수 있다는 것이다. Kafka에서Schema [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)( Avro/Protobuf )를 함께 활용하면, 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의スキーマ정합성も학보에서きる.

📢 **섹션 요약 비유**: 반정형 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)은대소양々な대きさ의수과( 다양한 구조의 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/XML )를 컨베이어 벨트( [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) )에 그대로 올려놓고, 거대한선별 시스템( Flink )에서자동적에등급( 파싱/[파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) )을분け종 료한ら, 등급별로상에힐める( [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) )자동화창고와 같다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)와 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 사이의 중간 위치에 있으며, 각각의 장점을 취합하는장면에서활용된다.

| 비교 항목 | [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/) (Structured) | 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Semi-structured) | [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) (Unstructured) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a></strong> | 사전 정의 고정 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) | 동적 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내 포함) | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 없음 |
| **변화 대응** | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 마이그레이션 필요 | 동적 추가/삭제 가능 | 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)든 수용 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | SQL [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 통한 고효검색 | [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 제한적 ([MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | 풀 텍스트/벡터 검색 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a></strong> | ACID 완전 보장 | 제한적 ([MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 4.0+ ACID) | 미지원 |
| **적용 기술** | RDBMS, [Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/) | [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) [Document](/studynote/14_data_engineering/01_infrastructure/037_document/), [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), S3, [Vector DB](/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 예시</strong> | 고객 테이블, 거래 내역 | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 응답, [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 | 이미지, 음성, 영상 |
| **분석 용도** | 집계/BI/리포팅 | [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/)/실시간 모니터링 | 딥러닝/NLP/이미지 인식 |

[반정형 JSON과 정형 RDBMS 테이블의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)비교]
```text
[정형 RDBMS 테이블: 고객]
+---------------------------------------------------------+
|  고객ID (PK)  |  이름      |  나이  |  도시      | ...  |
+---------------+-------------+-------+-------------+      |
|  1001         |  홍길동     |  30    |  서울      |      |
|  1002         |  김철수     |  25    |  부산      |      |
|  1003         |  이영희     |  28    |  인천      |      |
+---------------------------------------------------------+
   (모든 행이 동일한 Column 구조, 타입 강제)

[반정형 JSON 문서: 고객 프로필]
{
  "customerId": "1001",
  "name": "홍길동",
  "age": 30,
  "city": "서울",
  "preferences": {
    "color": "파란색",
    "hobby": ["등산", "독서"],
    "notifications": {
      "email": true,
      "sms": false
    }
  },
  "tags": ["vip", "prime"],
  "metadata": {
    "registeredAt": "2023-01-01",
    "lastLogin": "2024-01-15T10:30:00Z"
  }
}
  (문서마다異なる 필드 추가/삭제 가능, 계층 구조 표현 가능)
```
이 비교는 정형 RDBMS 테이블의 rigid한 행/열 구조와 반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 문서의령활한 계층 구조의 차이를 보여준다. RDBMS 테이블에서는 회원의 선호색, 취미, 알림 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 같은 계층적/반복적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하여 별도 테이블로 분리해야 하지만, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 문서에서는 단일 문서 안에 중첩된 구조로 자연스럽게 표현된다. 다만, 이러한 flexibility는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)약속의관송과[쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)성능의 trade-off를 수반한다.

📢 **섹션 요약 비유**: [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)는 미리 정해진 칸의보선합( 각 칸에 정해진 음식만 )이고, 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는자유형식의보선대( 뭐든 넣을 수 있지만 모양이 제각각 )이며, [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는빙상 전체( 냉동실, 채소실,제품실 구분 없이 모두 휘저어넣은 )과 같다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룰 때 마주치는 핵심 판단 상황과 그 기준을 정리한다.

1. <strong><a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">스키마 온 리드</a>( <a href="/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a> ) vs <a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">스키마 온 라이트</a>( <a href="/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/">Schema-on-Write</a> )</strong>: 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 본질적으로 [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/)-on-Read에적한다.
   - **판단**: Kafka에 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 메시지를 저장할 때, 각 producers가 다른 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)( v1, v2 )을 보내면 [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)( [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) )를리용하여 하위 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을검정 하고 저장할 수 있다. 이후 소비자가 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 적용( 파싱 )할 때 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 신규 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 모두처리할 수 있다.
2. <strong>중첩 <a href="/studynote/11_design_supervision/06_exam_summary/343_json/">JSON</a> 구조의 조회 최적화</strong>: MongoDB에서 심중첩된 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)( [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) ) 필터를 queries 할 때성능문제가 발생한다.
   - **판단**: 먼저 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델링 시 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)( [Normalization](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) )를 고려하되, 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 중요하다면 반정규화( [Denormalization](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) )로배렬을평면화하여 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 적용한다. 또는 Elasticsearch의 중첩( Nested ) 타입과결합( [Join](/studynote/05_database/04_transactions_concurrency/521_join/) ) 타입을활용하여 조회한다.
3. <strong>반정형 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 실시간 분석</strong>: Application [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 형태로 Kafka에 유입될 때, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 레벨( DEBUG, INFO, ERROR )별 필터링이 필수적이다.
   - **판단**: Flink의 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 파싱과 [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)( [Watermark](/studynote/16_bigdata/04_streaming/085_watermark/) ) 처리를 통해 시간 기반 윈도우취합과 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)( [Anomaly](/studynote/05_database/04_transactions_concurrency/530_anomaly/) ) 탐지를 실시간으로 수행할 수 있다. 다만, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 파싱은 CPU 집약적이므로 고류량 환경에서는 라인 기반 파싱( [TSV](/studynote/01_computer_architecture/14_hardware_security_trends/496_tsv/)/공백 분리 )보다저속이다.

[반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화( [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Evolution ) 처리 전략]
```text
[Schema Registry를 활용한 스키마 진화 처리]
+-------------------------------------------------------------+
|  Schema Registry (Confluent)                                 |
|  +-------------------------------------------------------+  |
|  |  Topic: user-events                                    |  |
|  |  +-------------------------------------------------+   |  |
|  |  |  Schema v1 ( {"userId": "int", "name": "str"} )  |   |  |
|  |  |  Schema v2 ( {"userId": "int", "name": "str",   |   |  |
|  |  |              "email": "str"} ) <- 신규 필드 추가  |   |  |
|  |  |  Schema v3 ( {"userId": "int", "age": "int",    |   |  |
|  |  |              "name": "str"} ) <- 필드 순서 변경   |   |  |
|  |  +-------------------------------------------------+   |  |
|  +-------------------------------------------------------+  |
|         | Compatibility Mode: BACKWARD                      |
|         | (이전 버전 소비자가 신규 레코드 읽기 가능)          |
+-------------------------------------------------------------+
```
이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Registry를 활용하여 반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화를 안전하게관리하는 방법을 보여준다. BACKWARD [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)모식하에서 신규 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)( v3 )의 레코드도 이전 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)( v1 )의 consumers가 읽을 수 있어, producers와 consumers의-deploy를 독립적으로 진행할 수 있다. 이는 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 특히 중요한 패턴이다.

📢 **섹션 요약 비유**: 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화는수사록의 형식이 해마다 조금씩 변하는 것과 같다.，거년은"오늘의 목표"만 적었는데, 금년는"오늘의 목표"와"정서 상태"를 함께 적는 식이다. [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Registry는 이런 변화가 과거 기록을 감당할 수 있도록 해주는동시, 새 형식으로도 기록할 수 있게 해주는 문서 관리 정책과 같다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/), [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 그리고 실시간 분석 분야에서 그 활용이 계속 확대되고 있으며, 특히REST API와JSON 기반의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 표준이 된금, 그중요성은さら에고まっ있는.

| 관점 | 기대 효과 (Before & After) | 정량 지표 |
|:---|:---|:---|
| 개발 생산성 | 고정 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 마이그레이션 -> [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 없이고속개발 | 기능 출시 시간 40% 단축 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 | 이기종 시스템 간CSV/텍스트 변환 -> [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/REST로 직접연동 |.integration 시간 60% 절감 |
| 실시간 분석 | 배치 중심 -> 스트리밍 실시간 [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/) | 분석 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 95% 감소 |

미래에는 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)를 통합 조회하는 [Federated Query](/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) 기술이 더욱성숙하여, 사용자는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 저장 위치나 형식을의식하지 않고도단일의 SQL로 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분석할 수 있을 것이다. 또한, 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를AI가 자동으로 구조화하여정보를추출하는기술( Automated [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Inference )이 발전함에 따라, 현재의수동적な[스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)정의 부담도 크게 줄어들 것이다.

📢 **섹션 요약 비유**: 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기술은음식점에서 음식의 정확한 레시피( 정형 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) ) 없이도,（도성전）그일의식재상황（[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ）에 따라 메뉴를 즉석에서 구성하는령활영업과 같다. 레시피가 없으면주사의창새로운능력 발휘할 수 있지만, 때로는，창새로운과품질관리의간에trade-off가 존재한다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) (JavaScript Object Notation) | 키-값 쌍 기반의 경량 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 포맷
* XML (Extensible Markup Language) | 태그 기반의 계층적 구조를 표현하는Markup 언어
* [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) [Document](/studynote/14_data_engineering/01_infrastructure/037_document/) [Database](/studynote/05_database/04_transactions_concurrency/501_database/) | JSON과 같은 문서를 직접 저장하는 [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/), CouchBase 등
* [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | Kafka에서 메시지 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)의 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을관리하는 시스템
* [스키마 온 리드](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) ([Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) | 저장 시는 원시 그대로 두고, 읽을 때 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 적용하는 방식
* [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | 반정형 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/XML 메시지의 실시간 스트리밍을 처리하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 플랫폼

### 📈 관련 키워드 및 발전 흐름도

```text
[JSON (JavaScript Object Notation)]
    |
    v
[XML (Extensible Markup Language)]
    |
    v
[NoSQL Document Database]
    |
    v
[Schema Registry]
    |
    v
[스키마 온 리드 (Schema-on-Read)]
    |
    v
[Apache Kafka]
```

이 흐름도는 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) (JavaScript Object Notation)에서 출발해 [스키마 온 리드](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) ([Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 반정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는수진록기와 같아서, 날짜와 제목은 항상 쓰지만 그 옆에 그림을 그리거나 메모를 자유롭게 할 수 있어요.
2. 스마트폰의 사진 갤러리를 보면 사진마다 찍은 날짜( [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) )가 자동으로 붙지만, 사진 자체( 이미지 )는 규격이 없죠.
3. 그래서 반정형은 정형( 규격화된 필통 )과 비정형( 아무거나 넣는 서랍장 )의 중간쯤에 있는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 3 / 258

<- **이전**: [2. 정형 데이터 (Structured Data) - RDBMS 테이블 같이 엄격한 스키마 구조 보유](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)
**다음**: [4. 비정형 데이터 (Unstructured Data) - 스키마가 없는 텍스트, 음성, 비디오, 이미지 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) ->

---
