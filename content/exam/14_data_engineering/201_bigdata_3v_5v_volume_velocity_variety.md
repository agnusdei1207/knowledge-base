---
title: "Big Data 3V·5V Characteristics"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 빅데이터는 단순한 '크기'가 아니라, 규모([Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/))·속도(Velocity)·다양성(Variety)이라는 세 축이 동시에 폭발적으로 증가하면서 기존 RDBMS 패러다임을 붕괴시킨 현상이다.
> 2. **가치**: 3V에 진실성(Veracity)과 가치(Value)가 추가된 5V는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 많이 수집하는 것"에서 "신뢰할 수 있는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 비즈니스 가치를 창출하는 것"으로 패러다임을 전환시킨다.
> 3. **판단 포인트**: 기술사 논술에서는 각 V의 기술적 대응 방법([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장, 스트리밍, [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리, 비용 최적화)을 5V와 1:1로 매핑하여 논지를 전개할 것.

---

## Ⅰ. 개요 및 필요성

### 빅데이터 등장 배경

2000년대 후반 소셜 미디어, [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) (Internet of Things), 모바일 기기의 폭증과 함께 기존 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스 관리 시스템](/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/)(RDBMS: Relational [Database](/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) System)으로는 처리 불가능한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쏟아지기 시작했다. 2001년 가트너(Gartner)의 더그 레이니(Doug Laney)가 처음 제시한 3V 개념은, 이 혼돈을 구조적으로 설명하는 언어가 되었다.

| 연도 | 사건 | 의의 |
|:---|:---|:---|
| 2001 | 가트너, 3V 정의 | [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/)·Velocity·Variety 개념 정립 |
| 2010 | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 성숙 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 실용화 |
| 2012 | IBM, 4V(Veracity 추가) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 문제 부각 |
| 2014 | IDC, 5V(Value 추가) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 자산으로 보는 관점 확립 |

### 왜 기존 방식으로는 한계인가?

RDBMS는 [스키마 온 라이트](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)([Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)), 수직 확장([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)), [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)([Structured Data](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)) 위주로 설계되었다. 빅데이터는 이 세 가지 가정을 모두 깨뜨린다.

```
기존 RDBMS 한계
+-----------------------------------------+
| 정형 데이터(행·열) <------ Variety 충돌  |
| 수직 확장(고가 서버) <---- Volume 충돌   |
| 배치 처리(야간 ETL) <----- Velocity 충돌 |
+-----------------------------------------+
```

📢 **섹션 요약 비유**: 빅데이터는 "소방호스로 물을 받아야 하는데 컵 밖에 없는 상황"이다. 컵(RDBMS)을 아무리 크게 만들어도 소방호스(3V)를 감당할 수 없어서, 아예 저수지(빅데이터 플랫폼)를 파야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3V 심화 정의

#### [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) (규모)

단위가 테라바이트(TB)·페타바이트(PB)·엑사바이트(EB)로 이동하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양. 핵심 대응 기술은 [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)([HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/): [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/studynote/02_operating_system/09_file_system/553_distributed_file_system/))과 [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3, GCS).

| 규모 단위 | 크기 | 대표 사례 |
|:---|:---|:---|
| Terabyte (TB) | 10¹^ Bytes | 중소기업 연간 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| Petabyte (PB) | 10¹⁵ Bytes | 페이스북 일일 업로드 이미지 |
| Exabyte (EB) | 10¹⁸ Bytes | 글로벌 인터넷 트래픽/월 |
| Zettabyte (ZB) | 10^¹ Bytes | 전 세계 연간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)량 |

#### Velocity (속도)

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·수집·처리 속도. 실시간 스트리밍 처리([Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/), [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/))와 마이크로배치(Apache [Spark Streaming](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/))로 대응.

```
속도 스펙트럼
+------------------------------------------------------+
|  배치(Batch)  ->  마이크로배치  ->  스트리밍  ->  실시간 |
|  (1일 주기)       (수 초)        (수 밀리초)  (< 1ms) |
|  Hive           Spark           Kafka        Flink   |
+------------------------------------------------------+
```

#### Variety (다양성)

정형(Structured), 반정형(Semi-Structured), 비정형(Unstructured) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 혼재.

| 유형 | 예시 | 저장 기술 |
|:---|:---|:---|
| 정형 | RDB 테이블, CSV | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/), Redshift |
| 반정형 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), XML, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Elasticsearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) |
| 비정형 | 이미지, 동영상, SNS 텍스트 | S3, [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) + [Spark MLlib](/studynote/16_bigdata/03_spark/062_spark_mllib/) |

### 5V: Veracity와 Value의 추가

```
3V -> 5V 진화
         +------------------------------------+
         |           5V 프레임워크             |
         |                                    |
         |  Volume  ----------------------+   |
         |  Velocity ---------------------+   |
         |  Variety  ---------------------+--->| Value (궁극 목적)
         |  Veracity ---------------------+   | 비즈니스 인사이트
         |  (신뢰성 검증)                 |   |
         +--------------------------------+---+
```

| V 특성 | 영문 | 정의 | 핵심 기술 |
|:---|:---|:---|:---|
| V1 | [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) (규모) | 저장·처리해야 할 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기 | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), S3, [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) |
| V2 | Velocity (속도) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·처리 속도 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), Flink, Spark |
| V3 | Variety (다양성) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식·출처의 다양성 | [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), Avro |
| V4 | Veracity (진실성) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)·[신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | DQ ([Data Quality](/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/)) 도구 |
| V5 | Value (가치) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 추출한 비즈니스 가치 | ML (Machine [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)), BI |

📢 **섹션 요약 비유**: 3V는 "많고, 빠르고, 다양한 재료가 들어온다"는 상황이고, Veracity는 "상한 재료를 걸러내는 품질 검사", Value는 "결국 맛있는 요리를 만들어야 한다"는 목적이다. 5V는 식재료 창고 운영의 전체 사이클이다.

---

## Ⅲ. 비교 및 연결

### 3V vs 5V: 적용 관점 차이

| 구분 | 3V | 5V |
|:---|:---|:---|
| 초점 | 기술적 도전(저장·처리 능력) | 비즈니스 가치 창출 능력 |
| 등장 배경 | 인프라 한계 극복 | [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 및 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 요구 |
| 기술사 논술 포인트 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 아키텍처 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)·비용 최적화 |

### 각 V의 기술적 대응 매핑

```
V-기술 매핑 아키텍처
+---------+---------------------------------------------+
|   V     |  핵심 기술 스택                               |
+---------+---------------------------------------------+
| Volume  |  HDFS -> S3/GCS -> Delta Lake (콜드/핫 계층화) |
| Velocity|  Kafka -> Spark Streaming -> Flink (지연 최소) |
| Variety |  Schema Registry -> Avro/Parquet -> Catalog    |
| Veracity|  Great Expectations -> dbt test -> Data Lineage|
| Value   |  Spark MLlib -> BI 대시보드 -> A/B 테스트       |
+---------+---------------------------------------------+
```

### 빅데이터 vs 전통 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/)) 비교

| 항목 | 전통 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 빅데이터 플랫폼 |
|:---|:---|:---|
| 확장 방식 | 수직 확장([Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) | 수평 확장([Scale-Out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) | 사전 정의([Schema-on-Write](/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) | 읽기 시점 정의([Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/)) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형 | 정형 위주 | 정형·반정형·비정형 |
| 처리 방식 | 배치 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 스트리밍 + 배치 |
| 비용 | 고가 전용 하드웨어 | 범용 하드웨어 |

📢 **섹션 요약 비유**: 3V는 "어떤 재료 문제인지 진단"이고, 5V는 "그 재료로 어떤 가치를 만들지까지 포함한 완전한 레시피"다. 기존 DW는 깔끔한 레스토랑, 빅데이터 플랫폼은 어떤 식재료든 받는 대형 푸드홀이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 이커머스 빅데이터 적용

**문제 상황**: 쇼핑몰에서 일 5TB의 클릭 스트림, 10억 건의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), 이미지·리뷰 텍스트를 처리해야 함.

| V 특성 | 이커머스 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 적용 기술 | 효과 |
|:---|:---|:---|:---|
| [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) | 클릭스트림 5TB/일 | S3 + [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 계층화 | 저장 비용 70% 절감 |
| Velocity | 실시간 재고·가격 변동 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Flink | 200ms 이내 재고 반영 |
| Variety | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 이미지, CSV | [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) Metastore | 통합 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리 |
| Veracity | 중복 주문, 봇 트래픽 | Great Expectations | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 95% -> 99% |
| Value | 개인화 추천 [CTR](/studynote/09_security/02_crypto/090_ctr_mode/) 향상 | [Spark MLlib](/studynote/16_bigdata/03_spark/062_spark_mllib/) | [CTR](/studynote/09_security/02_crypto/090_ctr_mode/) (Click-Through Rate) 23% 향상 |

### 기술사 논술 핵심 포인트

1. <strong><a href="/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/">Volume</a> 대응</strong>: 단순히 "HDFS를 쓴다"가 아니라, 핫(Hot)·웜(Warm)·콜드(Cold) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층화([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Tiering)로 [TCO](/studynote/12_it_management/01_governance_strategy/016_tco/) (Total Cost of Ownership) 최적화를 논해야 한다.
2. **Velocity 대응**: 배치와 스트리밍을 결합한 [람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/)([Lambda Architecture](/studynote/16_bigdata/04_streaming/095_lambda_architecture/)) 또는 [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)([Kappa Architecture](/studynote/16_bigdata/04_streaming/096_kappa_architecture/))를 언급하되, 복잡성 트레이드오프를 균형 있게 서술할 것.
3. **Veracity 대응**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질(DQ: [Data Quality](/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/))과 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)([Data Governance](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/))를 단순 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 수준이 아니라 조직·프로세스·기술의 3축으로 논할 것.
4. **Value 실현**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정(DDDM: [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)-Driven Decision Making)의 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) ([Return on Investment](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/))를 구체적 수치로 제시할 것.

📢 **섹션 요약 비유**: 빅데이터 프로젝트에서 5V는 건물 설계의 체크리스트다. "[Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) 기초공사, Velocity 배관, Variety 전기, Veracity 내진 설계, Value 완공 인테리어"—어느 하나라도 빠지면 건물이 흔들린다.

---

## Ⅴ. 기대효과 및 결론

### 5V 프레임워크 도입 효과

| 효과 영역 | 구체적 내용 |
|:---|:---|
| 비용 절감 | 범용 하드웨어([Scale-Out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))로 스토리지 비용 60~80% 절감 |
| 의사결정 속도 | [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)(T+1 보고) -> 실시간 대시보드(실시간 분석) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 범위 | [정형 데이터](/studynote/14_data_engineering/01_infrastructure/002_structured_data/)만 -> 비정형 포함 전사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 |
| 비즈니스 가치 | ML 기반 예측 모델로 수익 예측 정확도 향상 |
| [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 관리 | Veracity 기반 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리로 잘못된 의사결정 방지 |

### 미래 방향: 6V, 7V 논의

| 추가 V | 개념 | 의의 |
|:---|:---|:---|
| Variability (가변성) | 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 의미 맥락 변화 | NLP (Natural Language Processing) 필요성 |
| Visualization ([시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)) | 복잡한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 직관적 표현 | BI (Business Intelligence) 도구 발전 |

### 결론

빅데이터의 3V·5V 프레임워크는 단순한 학술 개념이 아니라, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 아키텍처 설계의 요구사항 도출 도구다. 기술사 관점에서는 각 V에 대응하는 기술 선택의 근거와 트레이드오프를 명확히 설명할 수 있어야 한다. 특히 Veracity와 Value는 기술 문제가 아니라 조직 문화와 거버넌스의 문제임을 이해해야 한다.

📢 **섹션 요약 비유**: 5V는 "빅데이터 사업의 사업계획서"다. Volume은 규모, Velocity는 성장 속도, Variety는 사업 다각화, Veracity는 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/), Value는 수익성이다. 다섯 항목 모두 우수해야 투자자(경영진)가 OK를 낸다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 기술 | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)) | [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) 대응 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장 |
| 기반 기술 | [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | Velocity 대응 스트리밍 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 |
| 기반 기술 | [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | Variety 대응 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리 |
| 연관 개념 | [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) | Veracity 실현 조직 프레임워크 |
| 연관 개념 | [Lambda Architecture](/studynote/16_bigdata/04_streaming/095_lambda_architecture/) | Velocity 대응 배치+스트리밍 아키텍처 |
| 상위 개념 | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | 3V 전체를 수용하는 저장소 패러다임 |
| 발전 방향 | [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)) | Value 실현을 위한 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 주도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 |

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/">Volume</a>(볼륨)</strong>은 도서관에 책이 엄청 많아지는 것, <strong>Velocity(속도)</strong>는 새 책이 매초 배달되는 것, <strong>Variety(다양성)</strong>은 책·만화·영상·음악이 한꺼번에 오는 것이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
빅데이터 3V: Volume · Velocity · Variety
    |
    v
확장 5V: + Veracity (정확성) + Value (가치)
    |
    v
처리 기술: Hadoop -> Spark -> Flink (실시간)
    |
    v
저장 아키텍처: Data Lake -> Lakehouse -> Data Mesh
```
2. <strong>Veracity(진실성)</strong>는 잘못 인쇄된 책을 걸러내는 품질 검사관이고, <strong>Value(가치)</strong>는 그 많은 책들로 결국 유용한 지식을 얻는 것이에요.
3. 빅데이터 시스템은 이 다섯 가지 문제를 모두 해결하는 "슈퍼 도서관 관리 시스템"이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 201 / 258

<- **이전**: [200. 자율주행 모방 학습 (Imitation Learning) 시뮬레이터 디지털 트윈 합성 데이터 생성](/studynote/14_data_engineering/04_mlops/200_autonomous_driving_imitation_learning_digital_twin/)
**다음**: [202. 스케일 아웃 (Scale-Out) 분산 수평 확장](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) ->

---
