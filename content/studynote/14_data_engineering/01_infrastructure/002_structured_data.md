+++
title = "2. 정형 데이터 (Structured Data) - RDBMS 테이블 같이 엄격한 스키마 구조 보유"
description = "관계형 데이터베이스 테이블처럼 엄격한 스키마 구조를 보유하는 데이터 유형의 정의, RDBMS 기반 저장 구조, OLTP와 OLAP 환경에서의 활용"
date = 2024-05-24

[taxonomies]
tags = ["data_engineering"]

[extra]
tags = ["data_engineering"]
+++

# 02. 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Structured [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 행( Row )과 열( Column )로 구성된 사전에 정의된 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 따르며, 각 필드의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입이 고정되어 있어 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 검색과 분석이 매우 효율적이다.
> 2. **구조**: 관계형 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/)( RDBMS )인 오라클, MySQL, PostgreSQL 등의 테이블 구조를 기반으로 하며, [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)( Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) )와 조인( [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) ) 연산을 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 유지한다.
> 3. **한계**: [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 고정되어 있어 새로운 필드 추가 시 마이그레이션이 필요하며, [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)( 텍스트, 이미지, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) )를 직접 저장하다에는이다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)( Structured [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) )란정의에 따라 구성되며, 행( Row )과 열( Column )의 2차원 테이블 형태로 저장되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 의미한다. 이는 마치 엑셀 스프레드시트의 셀(cell)처럼 각 열( Column )이 주민등록번호, 이름, 주소처럼 정해진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입( 문자열, 정수, 날짜 등 )을 갖고, 각 행( Row )이 하나의 레코드( Record )를 대표한다.
전통적인 기업 정보 시스템은 1970년대 관계형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)( Relational [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) )의 등장 이래로 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기반으로 구축되었다. 이러한 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는은행업의 계좌 거래, 제조업의 재고 관리, 소매업의 매출 기록 등 핵심 자산으로 활용되어 왔다. [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 미리 정의되어 있기 때문에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)( [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) )을 걸 수 있고, 급en's 행( ACID ) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 안전하게 처리할 수 있다.
그러나, 인터넷과 SNS, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기에서 발생하는 비정형 및 [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)( [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), XML, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 등 )는 기존의 RDBMS 방식으로는 저장소 구조가 맞지 않아 별도의 처리 파이프라인이 필요하게 되었다.

[전통적 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 환경과 RDBMS 한계 도식도]
```text
[기업 업무 시스템] [정형 데이터의 흐름]
ERP / SAP ──> [OLTP DB] ──> [정기 배치 ETL] ──> [Data Warehouse]
(정형 거래) (실시간 갱신) (야간DW이전) (경영분석Reporting)
│ │ │ │
└───── 트랜잭션 ACID 보존 ─┴────── 매일 수십GB ──────────┴───── BI 대시보드
```
이 도식은 전통적인 기업의 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 보여준다. ERP나업paeos에서 발생한 정형 거래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)( Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing ) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 실시간으로 저장되고, 야간에 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)( Extract, Transform, Load ) 작업을 통해 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Warehouse로 이전되어 경영진용 BI 리포팅에 활용된다. 이러한 배치 처리는 하룻밤 사이에 모든 거래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 DW에 반영되어야 하므로 일() 단위 분석만 가능하다는 속도(Velocity) 한계가 존재한다.

📢 **섹션 요약 비유**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 도서관의 정화된 분류표에 맞게 정리된 도서 목록 카드( [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) )와 같다. 카드는 미리 정해진 항목( 청구기호, 저자, 제목 )으로 구성되어 있어 빠르게 검색( SQL )할 수 있지만, 그림이나 표지 색깔 같은 비정형 속성은 표현할 수 없다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 그 구조적 특성 인해 OLTP와 OLAP라는 두 가지 다른 환경으로 나뉘며, 각각 최적화된 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 아키텍처가 존재한다.

| 구분 | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) | 판단 기준 |
|:---|:---|:---|:---|
| **목적** | 일상적 거래( 등록, 수정, 삭제 )의 실시간 처리 | 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 분석, 집계, 통계 처리 | 처리 유형 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기** | 수천~수백만 건 (단위: 레코드) | 수십억~수천억 건 (단위: 기가~테라바이트) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 볼륨 |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)** | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)( 3차 정규형~[BCNF](/knowledge-base/studynote/05_database/04_transactions_concurrency/529_bcnf/) ) | 다차원 모델( [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/), 눈송이 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) ) | 설계 방법론 |
| **[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴** | 단일 레코드 CRUD (수십 건/초) | 복잡한 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), 그룹핑, 윈도우 함수 (수백 건/일) | 액세스 패턴 |
| **[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)** | [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/), [해시 인덱스](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/) | 클러스터드, [비트맵 인덱스](/knowledge-base/studynote/05_database/03_relational_model/158_bitmap_index_cardinality_dml/) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |
| **[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)** | ACID 완전 준수 | 읽기 전용쿼리 위주 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 요구 |
| **대표 제품** | [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), MySQL, PostgreSQL | [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), Redshift, Teradata | 솔루션 |

[정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 OLTP에서 OLAP로의 이동 아키텍처]
```text
[OLTP 계층 - 실시간 정형 거래 처리]
┌─────────────────────────────────────────────────────┐
│ 웹/App ──> [Load Balancer] ──> [MySQL Primary] │
│ │ │ │
│ 읽기 전용 │ RAID 1 복제 │
│ ↓ ↓ │
│ [MySQL Replica 1] [MySQL Replica 2] │
│ (샤딩/Sharding 수평 확장) │
└─────────────────────────────────────────────────────┘
│ 야간 ETL / CDC
↓ (아마존 DMS, Debezium)
┌─────────────────────────────────────────────────────┐
│ [OLAP 계층 - 분석용 데이터 웨어하우스] │
│ │
│ Snowflake / Redshift / BigQuery │
│ ┌─────────┬─────────┬─────────┬─────────┐ │
│ │ Fact │ Fact │ Dim │ Dim │ │
│ │ Sales │ Inventory│ Customer│ Product │ │
│ └─────────┴─────────┴─────────┴─────────┘ │
│ (스타 스키마 / 눈송이 스키마 구성) │
└─────────────────────────────────────────────────────┘
│
↓ (BI 도구: Tableau, Looker)
[경영진 대시보드 / 자가 보고서]
```
이 구조는 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실시간 거래 환경( [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) )에서 분석 환경( [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) )으로 어떻게 흐르는지를 보여준다. [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 매일 밤 또는 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)( [Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) )를 통해 실시간으로 DW로 이전되며, DW에서는 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 테이블이 분석에 유리한 다차원 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)로 재구성된다. [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 환경에서는 단일 레코드 접근에 최적화된 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 필수적이고, [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 환경에서는 대규모 스캔과 집계에 적합한 컬럼 스토어 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 핵심이다.

📢 **섹션 요약 비유**: OLTP는 놀이공원의 입장권 발권 시스템( 빠른 처리 )이고, OLAP는 하루 종일 모인 활용자 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를하여 어떤 놀이기구가 가장 인기가 있는지 분석하다시스템입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 반정형( Semi-structured ), 비정형( Unstructured ) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 각각 다른 저장소와 처리 패러다임을 요구하며, 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼에서는 이가 공존한다.

| 비교 항목 | 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Structured) | [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/) (Semi-structured) | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) (Unstructured) |
|:---|:---|:---|:---|
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)** | 사전 정의된 고정 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 포함 | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 없음 |
| **보관 형태** | RDBMS 테이블 (행/열) | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), XML, CSV, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 텍스트, 이미지, 영상, 음성 |
| **검색 방식** | SQL (정형 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)) | JSONPath, XPath, 정규식 | 풀 텍스트 검색, [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터 |
| **확장성** | 수직 확장 ([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 한계 | 수평 확장 ([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 가능 | 대규모 [분산 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/) |
| **ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)** | 완전 지원 | 부분 지원 ([MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 등) | 미지원 |
| **대표 저장소** | [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), MySQL, PostgreSQL | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), S3 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/), S3, [Vector DB](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/) |
| **분석 용도** | 집계, 리포팅, BI | [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/), 실시간 모니터링 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 훈련, NLP, 이미지 인식 |
| **비용** | 라이선스 비용 높음 | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 중심 (저렴) | 클라우드 [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) (저렴) |

[현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼에서 정형-반정형-[비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)의 공존 구조]
```text
┌─────────────────────────────────────────────────────────────────────┐
│ 통합 데이터 플랫폼 (Modern Data Stack) │
├──────────────────┬──────────────────┬────────────────────────────────┤
│ [정형 데이터] │ [반정형 데이터] │ [비정형 데이터] │
│ Oracle / MySQL │ Kafka / MongoDB │ S3 / HDFS │
│ Snowflake │ Elasticsearch │ Vector DB (Pinecone) │
│ (OLAP DW) │ (로그/스트림) │ (AI Training Data) │
├──────────────────┴──────────────────┴────────────────────────────────┤
│ 공통 메타데이터 계층 (Data Catalog / Lineage) │
│ AWS Glue / Amundsen / DataHub │
├─────────────────────────────────────────────────────────────────────┤
│ 통합 쿼리 엔진 (Federated Query) │
│ Trino / Presto / Apache Drill │
└─────────────────────────────────────────────────────────────────────┘
```
이 다이어그램은 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼에서 세 가지수가 공존하면서 통합되는 구조를 보여준다. 각기 다른 저장소에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되어 있지만, [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)( [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) )와 [Federated Query](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)( [연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) ) 기술을 통해 논리적으로 단일 뷰( Single [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) )를 제공한다. 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 전통적인 RDBMS와 DW에서 가장 효율적으로 처리되고, [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)는 Kafka나 [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) 같은 스트림/[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 특화 시스템에서, [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 S3와 Vector DB에서 각각 관리된다.

📢 **섹션 요약 비유**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는에된 도시락( 규격화된 밥과 반찬 )이고, [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)는 덮밥( 위에 뭐가 올지 모르는 )이며, [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 재료시장( 어떤 것도 다 들어올 수 있는 )과 같다. 도시락은 세상 어디든 표준화되어 있지만 변화가 어렵고, 재료시장은 뭐든 넣을 수 있지만 관리가 어렵다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루면서 마주치는 기술적 판단 상황과 그에 따른 의사결정 기준을 정리한다.

1. **[정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)( [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ) vs [역정규화](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)( [Denormalization](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) )**: [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 환경에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 제거하고 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 보장하기 위해 3차 정규형( [3NF](/knowledge-base/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) )까지 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하는 것이 원칙이다.
- **판단**: 그러나 분석가을 위한 DW에서는 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 비용을 줄이기 위해 [역정규화](/knowledge-base/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)된 [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/)가 더 효율적이며, 이 두 목적은 물리적으로 분리된 OLTP와 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 시스템으로 구현된다.
2. **[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계의 중요성**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 쿼리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 전략에 의해 결정된다.
- **판단**: [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 등치 검색( = )과 범위 검색( BETWEEN )에 강하지만, 너무 많은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)( INSERT/UPDATE ) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 저하시킨다. 반면 [비트맵 인덱스](/knowledge-base/studynote/05_database/03_relational_model/158_bitmap_index_cardinality_dml/)는 카디널리티( 종류 )가 낮은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)( 성별, 지역코드 )에 극도로 효율적이다.
3. **[파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)과 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)**: 단일 테이블이 수십억 행에 도달하면 테이블 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)( [수평 분할](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/) )이 필수적이다.
- **판단**:_RANGE [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)( 날짜별 ), _HASH [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)( 키) 등을 통해 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 프루닝( 불필요한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 읽기 건너뛰기 )으로 쿼리 범위를 좁혀 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 향상시킨다.

[정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 쿼리 최적화를 위한 실무 의사결정 트리]
```text
[SQL 쿼리 실행 계획 분석]
│
├── [Full Table Scan 발생?]
│ └── Yes ──> [적합한 인덱스 추가 검토]
│ ├─ B-Tree (등치/범위 검색)
│ └─ 복합 인덱스 (선행 열 우선)
│
├── [JOIN 비용 과다?]
│ └── Yes ──> [조인 순서 최적화 / 힌트 사용]
│ ├─ 드라이빙 테이블 선정
│ └─ 중첩 루프 vs 해시 조인 vs 정렬 병합
│
└── [정규화 vs 역정규화 판단]
├── OLTP (거래 처리) ──> 3NF 정규화
└── OLAP (분석 처리) ──> 역정규화 (합성키, 누적으로드)
```
이 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)는 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 SQL 쿼리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 진단하고 해결하는프로세스을/를 보여준다. 먼저 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)( EXPLAIN )을 분석하여 Full Table Scan이 발생하면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 검토하고, [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 비용이 높으면 조인 순서와 알고리즘을 변경하며, 시스템 목적에 따라 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 전략을 선택한다. 이러한 튜닝은 수십억 행의 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어의 핵심 역량이다.

📢 **섹션 요약 비유**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 쿼리 최적화는 교통 정체( Full Table Scan )가 발생한 고속도로에 입체 교차로( [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) )를하거나, 골목 길( [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) )을 광장로우는 것과 같다. 목적지( [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) )에 빨리 도착하려면 경로( [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) )를에분석하여하다와/과이/가입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 인공지능과 빅데이터 시대에도 여전히 기업 정보 시스템의 중추( ) 역할을 하며, 클라우드 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 발전으로 그 활용 범위가 확대되고 있다.

| 관점 | 기대 효과 (Before & After) | 정량 지표 |
|:---|:---|:---|
| 인프라 비용 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) RDBMS 라이선스 → 클라우드 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/)) | DB 유지보수 비용 50% 절감 |
| 분석 속도 | 일 배칭 → 실시간 스트리밍 SQL 쿼리 | 쿼리 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 90% 단축 |
| 확장성 | 수직 확장 ([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 한계 → (Auto-scaling) | 피크 타임 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 10배 향상 |

미래에는 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 관리에서도 머신러닝이 활용되어, 쿼리 패턴을 학습하여 자동으로 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 추천하고 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 전략을 최적화하는 **자율 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)( Autonomous [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) )**가 표준이 될 것이다. 또한, 정형정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통합적으로 쿼리하는 [Federated Query](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) 기술이 성숙하면서, 사용자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 위치를에 SQL 하나로 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분석할 수 있는 세상이 올 것이다.

📢 **섹션 요약 비유**: 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기술은/는:classical 오케스트라의 기본 악기( 비올라, 첼로 )처럼 오랜 역사와 안정감을 갖추면서도, 클라우드 오케스트라( [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) )의 시대에는 더 이상 개별 악기의( 인프라 )을 관리하지 않고 지휘자( ML 기반 오토 튜닝 )에게 전체 작품( [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 )을관리수이/가하여있다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* 관계형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) (RDBMS) | 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하는 2차원 테이블 기반 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 시스템
* [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) | 일상적 거래의 실시간 처리 환경
* [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) | 대규모 분석을 위한 다차원 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)
* [스키마 온 라이트](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) ([Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/)) | 저장 시 사전에 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 정의하고 정제하는 방식
* [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/)) | 전사적 관점의 분석을 위한 통합 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소
* [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 제거와 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 보장을 위한 테이블 설계 기법

### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 데이터베이스 (RDBMS)]
│
▼
[OLTP (Online Transaction Processing)]
│
▼
[OLAP (Online Analytical Processing)]
│
▼
[스키마 온 라이트 (Schema-on-Write)]
│
▼
[데이터 웨어하우스 (Data Warehouse)]
```

이 흐름도는 관계형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) (RDBMS)에서 출발해 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 정형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 칸막이가 나누어진 필통과 같아서, 연필( [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) )마다 정해진 칸이 있어 바로 찾을 수 있어요.
2. 하지만 칸에 맞는 연필만 넣을 수 있어서 크레파스( [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) )는 넣을 수 없어요.
3. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세계에서는 연필도 크레파스도 모두 넣을 수 있는 서랍장( [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) )도 함께 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 2 / 258

← **이전**: [1. 빅데이터 3V / 5V - 볼륨(Volume), 속도(Velocity), 다양성(Variety), + 진실성(Veracity),](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/)
**다음**: [3. 반정형 데이터 (Semi-structured Data) - 데이터 내부(태그)에 구조(메타데이터)를 포함 (XML, JSON, 로그)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/) →

---
