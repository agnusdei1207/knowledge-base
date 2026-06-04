+++
title = "20. 데이터 정형화 비율 — 전체 데이터 중 정형 < 20%, 비정형 > 80%"
description = "빅데이터 시대의 다크 데이터 문제와 정형/비정형 데이터의 구조적 역전 현상 및 처리 아키텍처"
date = 2024-05-24

[taxonomies]
tags = ["bigdata"]

[extra]
tags = ["bigdata"]
+++

# 20. [데이터 정형화 비율](/knowledge-base/studynote/16_bigdata/13_intro_trends/252_data_structured_ratio/) (정형 < 20% vs 비정형 > 80%)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기업과 사회에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중 RDBMS에 예쁘게 담기는 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)는 20% 미만에 불과하며, 텍스트, 이미지, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 영상 등 구조가 없는 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)가 80% 이상을 차지하는 구조적 대역전 현상이다.
> 2. **가치**: 이 80%의 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 그동안 처리와 분석이 어려워 방치된 '[다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)([Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))'였으나, 최근 AI와 빅데이터 플랫폼의 발전으로 가장 거대한 비즈니스 인사이트의 원천으로 변모했다.
> 3. **융합**: 이를 처리하기 위해 고전적인 [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) 방식의 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) 아키텍처는 붕괴되고, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)/[Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) 기반에 [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) 방식을 결합한 '[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))'와 '[레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)([Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/))' 아키텍처가 필수적으로 융합된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

과거 IT 시스템의 중심은 명확한 행(Row)과 열(Column)을 가진 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(RDBMS)였다. 은행의 거래 내역, 쇼핑몰의 주문 정보 등 구조화된 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/">정형 데이터</a>(<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/">Structured Data</a>)</strong>가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 전부라고 여겨졌다. 그러나 스마트폰의 보급, SNS의 폭발적 성장, 그리고 모든 기기가 인터넷에 연결되는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)([사물인터넷](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 시대가 도래하면서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 지형이 완전히 뒤집혔다.

현재 전 세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발생량의 80% 이상은 이메일 텍스트, [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 영상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 음성 통화 녹음, 서버의 클릭스트림 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 센서의 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등 정해진 형태가 없는 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">비정형 데이터</a>(<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">Unstructured Data</a>)</strong>가 차지하고 있다. 문제는 이 방대한 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)들이 기존의 DB 시스템에는 저장조차 할 수 없어, 어두운 곳에 쌓인 채 버려지는 <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/">다크 데이터</a>(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/">Dark Data</a>)</strong>로 전락한다는 점이다. 빅데이터 기술의 본질적 필요성은 바로 이 80%의 어둠 속에 잠든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 AI와 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)을 활용해 혁신적인 가치를 발굴해 내는 데 있다.

다음은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생태계의 거대한 빙산 구조를 보여주는 도식이다.

```text
[데이터 빙산 (Data Iceberg) 모델 현상]

      /\         [정형 데이터 (Structured Data) - < 20%]
     /  \        - RDBMS 저장, 관리 용이, 명확한 스키마
    /____\       - 재무, ERP, CRM 거래 데이터
 ￣￣￣￣￣￣￣￣  <==== (수면: 기존 IT 기술의 한계선)
  /        \
 /          \    [반정형/비정형 데이터 (Unstructured Data) - > 80%]
/            \   - 텍스트, 이미지, 로그, SNS, IoT, 영상
--------------   - 다크 데이터(Dark Data): 수집은 되나 방치됨
                 - NoSQL, Data Lake, 딥러닝 파이프라인 필수 구간
```

이 도식의 핵심은 기업이 수면 위 20%의 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)만 분석해서는 결코 시장의 전체 그림(예: 고객이 우리 브랜드를 어떻게 느끼는지, 기계가 언제 고장 날지)을 파악할 수 없다는 것이다. 80%의 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 건져 올리기 위해서는 저장소, 처리 엔진, 분석 기법 모두가 근본적으로 달라져야 한다.

> 📢 **섹션 요약 비유**: 예전에는 깨끗하게 포장된 마트의 채소(정형 20%)만으로 요리를 했다면, 이제는 거대한 바다와 정글에서 형태도 모를 야생의 식재료(비정형 80%)가 쏟아져 들어오고 있어, 이것들을 썩히지 않고 요리할 수 있는 완전히 새로운 거대한 만능 주방 기계가 필요해진 상황입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

80%의 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 수용하고 분석하기 위해 빅데이터 아키텍처는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 구조를 강제하는 방식에서 벗어나, 유연성을 극대화하는 방향으로 진화했다.

#### 1. 정형 vs [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리 아키텍처 구성

| 요소명 | [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) (20%) 아키텍처 | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) (80%) 아키텍처 | 아키텍처 전환 이유 |
|:---|:---|:---|:---|
| **저장소 (Storage)** | RDBMS ([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), MySQL), [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)/[NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/), [Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) (AWS S3), [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)의 무한한 수평 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 및 저비용 저장 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | [Schema-on-Write](/knowledge-base/studynote/14_data_engineering/01_infrastructure/010_schema_on_write/) (저장 시 테이블 구조 강제 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) | [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) (일단 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 저장, 읽을 때 구조 부여) | 형태가 시시각각 변하는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/텍스트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 설계 없이 즉시 수용 |
| **처리 엔진** | SQL, [Stored Procedure](/knowledge-base/studynote/05_database/03_relational_model/186_stored_procedure_trigger/) | Spark, Flink, NLP [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | 이미지/텍스트 내의 특징 추출을 위한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 필요 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong> | RDBMS | [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) ([Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/), [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value, [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/), [Vector DB](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/)) | 비정형 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 등)이나 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망 저장 최적화 |

#### 2. [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)([Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))의 가치화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 흐름

아래 도식은 저장조차 어려웠던 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(예: 고객의 콜센터 음성 녹음과 리뷰 텍스트)가 어떻게 정형화되어 분석 가치를 가지게 되는지 보여준다.

```text
[비정형 데이터의 정형화 파이프라인 (Dark Data to Insight)]

[입력: 비정형 데이터] (음성 녹음 파일, SNS 이미지)
        |
        v (원시 저장)
[Data Lake / Object Storage] --- (무한 용량, 저비용 보관)
        |
        v (특징 추출 및 벡터화 / AI 모델 적용)
[AI / ML Pipeline 계층]
 +- STT (Speech-to-Text)  : 음성 -> 텍스트
 +- NLP (감성 분석)       : 텍스트 -> "불만(Negative)", "긍정(Positive)" 분류
 +- CNN (이미지 인식)     : 이미지 -> "파손된 상품" 객체 검출
        |
        v (추출된 메타데이터의 반정형/정형화)
[NoSQL / Data Warehouse] --- (예: 고객ID | 불만여부 | 상품파손 | 발생시간)
        |
        v (통합 분석)
[BI Dashboard / LLM Prompt Context]
```

이 메커니즘의 핵심은 <strong>"<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">비정형 데이터</a> 그 자체를 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>하는 것이 아니라, <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 모델을 통과시켜 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>나 벡터 값(반정형/정형)으로 변환한 뒤에 융합 분석한다"</strong>는 점이다. 과거에는 사람이 일일이 듣고 태그를 달아야 했던 작업이 딥러닝과 Spark 같은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 엔진을 만나면서 자동화되었고, 비로소 80%의 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)에 불을 밝힐 수 있게 되었다.

> 📢 **섹션 요약 비유**: 형태가 제각각인 폐플라스틱 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/)([비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/))를 그냥 창고([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))에 쌓아두면 쓰레기([다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))에 불과하지만, AI라는 거대한 분쇄기와 용광로(ML [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인)를 통과시키면 규격화된 플라스틱 블록([정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/))으로 재탄생하여 새로운 장난감을 조립할 수 있게 되는 과정입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

이러한 비율 역전 현상에 대응하기 위해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 세 가지 스펙트럼과 그에 맞는 저장 기술의 트레이드오프를 명확히 비교해야 한다.

#### 1. 정형 vs 반정형 vs [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 특성 비교

| 구분 | [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) (Structured) | [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/) (Semi-structured) | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) (Unstructured) |
|:---|:---|:---|:---|
| **비율 추정** | ~ 20% | 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중간 연결 고리 | ~ 80% |
| **특징** | 엄격한 고정 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 테이블 형태 | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에 존재 (자기 기술적), 유연한 구조 | 일정한 규칙이나 구조가 전혀 없음 |
| **대표 포맷** | RDB의 Table, Excel | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/), XML, HTML, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 텍스트, 오디오, 비디오, 이미지 |
| **저장 및 처리** | RDBMS (강력한 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)) | [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) ([MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)) | [Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/), [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [Vector DB](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/) |
| **검색 및 분석** | SQL 기반 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 연산 | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value 조회, 트리 파싱 | [역색인](/knowledge-base/studynote/05_database/07_exam_summary/500_inverted_index_elasticsearch/)(Full-text), 벡터 [유사도 검색](/knowledge-base/studynote/05_database/06_dw_olap_trends/348_similarity_search/) |

이 비교에서 가장 눈여겨볼 부분은 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/">반정형 데이터</a></strong>의 역할이다. [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(예: 기사 원문)가 AI를 거치면 태그가 달린 [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 형태의 [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)로 1차 가공되며, 이는 NoSQL을 거쳐 궁극적으로 DW에 적재될 수 있는 징검다리 역할을 한다.

#### 2. 기술 융합: [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(거대 언어 모델)과 Vector DB의 부상
최근 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 생태계의 가장 큰 혁신은 LLM의 등장이다. 과거 [텍스트 마이닝](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/)은 키워드 빈도수 분석에 그쳤으나, 이제는 수백만 건의 비정형 PDF 문서를 [Vector DB](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/)([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공간)에 저장하고, [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)([검색 증강 생성](/knowledge-base/studynote/12_it_management/05_security_compliance/222_rag_retrieval_augmented_generation/)) 아키텍처를 통해 LLM이 직접 비정형 문서를 읽고 요약해 주는 수준에 이르렀다. 이는 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 처리의 패러다임을 "[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 추출"에서 "시맨틱(의미) 이해"로 완전히 진화시켰다.

> 📢 **섹션 요약 비유**: [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)가 서랍장 칸마다 딱 맞게 정리된 옷이라면, [반정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)는 옷에 사이즈 태그가 붙어 행거에 걸려있는 상태고, [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 바닥에 산더미처럼 쌓인 빨랫감입니다. 최근 등장한 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))는 이 산더미 속에서 "파란색 줄무늬 티셔츠 찾아줘"라는 말 한마디에 정확히 옷을 끄집어내는 로봇 팔과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 기업이 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)를 자산화하려 할 때, 무작정 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 모으는 것은 인프라 재앙을 초래한다.

#### 1. 실무 시나리오: 제조 공장의 예지 정비(Predictive Maintenance) 도입
- **상황**: 기존 ERP에 기록되는 설비 구매 내역/고장 일자(정형 20%)만으로는 공장 가동 중단을 예측하지 못함. 이에 설비의 소음(오디오), 진동 센서(시계열 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)), 외관 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)(영상) 등 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 80%를 수집하기 시작.
- **의사결정 및 난관**: [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 용량이 기하급수적으로 커 네트워크 병목과 클라우드 스토리지 비용 폭탄을 유발함.
- <strong>기술적 해결책 (아키텍처 분리 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>)</strong>:
  1. **Edge Tier**: 공장 내 [엣지 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/) 노드에서 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 영상을 실시간 분석([CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)). 정상 영상은 버리고, '불꽃'이나 '연기'가 감지된 영상 프레임과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(발생 시간, 위치)만 클라우드로 전송 ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경량화).
  2. <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/">Lakehouse</a> Tier</strong>: 원시 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(반정형)은 저렴한 클라우드 Object Storage에 저장하되, Apache [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 같은 컬럼 기반 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 포맷으로 변환하여 저장 공간 1/10로 축소.
  3. **Analytics Tier**: Delta Lake나 Iceberg 포맷을 입혀 비정형 저장소 위에서 직접 빠르고 안전한 SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 수행.

```text
[비정형 데이터 비용/네트워크 최적화 의사결정 트리]

[대용량 비정형 데이터 발생 (CCTV, 센서)]
       |
       +- (모두 중앙 클라우드로 전송?) --> [네트워크 마비, Storage 비용 폭발] (안티패턴)
       |
       v (엣지 필터링 도입)
[Edge Node에서 1차 가공 / 필터링]
       |
       +- 정상 패턴 --> [폐기 또는 24시간 후 자동 덮어쓰기]
       |
       v 이상 패턴 / 요약 메타데이터
[저비용 Object Storage 적재 (Data Lake)]
       |
       v (포맷 변환: CSV -> Parquet 압축)
[Data Lakehouse 기반 AI 통합 예측 모델 학습]
```

#### 2. 실무 도입 시 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) ([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/) 현상)
비정형 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 가장 치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)은 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)가 거대한 쓰레기장인 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 스왐프(<a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>)</strong>로 변질되는 것이다. 구조가 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 넣을 때 '[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(누가, 언제, 왜 만들었는지)'를 태깅하지 않고 마구 던져 넣으면, 나중에 검색 자체가 불가능해져 영원히 꺼내 쓸 수 없는 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)로 회귀한다. 이를 막기 위해 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) 솔루션 도입이 필수적이다.

> 📢 **섹션 요약 비유**: 물건을 버리긴 아깝다며 끝없이 사서 창고에 대충 쑤셔 박아두면 나중엔 문조차 열 수 없는 '호더([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))'의 방이 됩니다. [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 저장할 때는 반드시 박스 겉면에 "2023년 겨울 옷"이라는 라벨([메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/))을 붙여 둬야 거대한 창고([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))가 제 기능을 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 80%를 차지하는 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)를 처리할 수 있는 역량 확보는 기업 생존의 필수 조건이다.

| 구분 | 정량/정성적 기대효과 및 변화 |
|:---|:---|
| **비즈니스 통찰력** | 고객의 숨겨진 감정, 리뷰, 음성 등 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)에서 행동 패턴을 발굴하여 이탈률 예측 및 개인화 마케팅 달성 |
| **운영 비용 최적화** | 비싼 RDBMS 스토리지에 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 욱여넣던 과거와 달리, 저렴한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지 중심의 저장소 혁신([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))으로 [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 절감 |
| **아키텍처 진화** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하여 이동시키는 복잡한 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 방식에서 벗어나, 레이크에 두고 즉시 분석하는 [Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-[ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 및 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)로 진화 |

결론적으로, <strong>"<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/">정형 데이터</a>가 기업의 과거(What happened)를 기록한다면, <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">비정형 데이터</a>는 기업의 미래(What will happen)를 예측하는 맥락(<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a>)을 제공한다."</strong> 앞으로의 빅데이터 아키텍처는 이 이질적인 두 세계를 어떻게 끊김 없이 하나로 결합(Unified [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))할 것인가에 성패가 달려 있으며, [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/)(Multi-modal) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기술이 이 거대한 융합의 핵심 엔진으로 작용할 것이다.

> 📢 **섹션 요약 비유**: [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)가 매달 찍히는 깔끔한 통장 잔고(결과)라면, [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)는 내가 매일 흘리는 땀방울과 영수증, 주고받은 수많은 카톡 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지(과정과 맥락)입니다. 이 80%의 일상을 이해하고 분석할 수 있어야만 진정으로 부자가 되는 미래의 길을 설계할 수 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">데이터 레이크</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">Data Lake</a>)</strong> | 비정형, 반정형, [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)를 원시 형태 그대로 규모의 제한 없이 저장하는 저비용 중앙 리포지토리
- <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/">다크 데이터</a> (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/">Dark Data</a>)</strong> | 수집하고 저장 및 처리하고는 있으나 분석이나 비즈니스 의사결정에는 전혀 활용되지 않고 방치되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/">Schema-on-Read</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장할 때는 형태를 따지지 않고 무조건 저장하고, 나중에 분석(Read)할 때 목적에 맞게 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 씌워 읽어내는 접근법
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/">벡터 데이터베이스</a> (<a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/">Vector DB</a>)</strong> | [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(텍스트, 이미지)를 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 통해 고차원의 숫자 벡터로 변환하여 저장하고, 의미적 유사성을 빠르게 검색하는 DB
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 스왐프 (<a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>)</strong> | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)에 거버넌스([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), 품질 관리 등)가 부재하여, 원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찾을 수도 쓸 수도 없게 된 [데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/) 상태

### 📈 관련 키워드 및 발전 흐름도

```text
[정형 데이터 (Structured) — RDBMS 행/열 구조, 전체의 약 20%]
    |
    v
[반정형 데이터 (Semi-structured) — JSON/XML/CSV, 스키마 유연]
    |
    v
[비정형 데이터 (Unstructured) — 텍스트·이미지·동영상, 전체의 약 80%]
    |
    v
[다크 데이터 (Dark Data) — 수집됐으나 활용되지 않는 방치 데이터]
    |
    v
[데이터 레이크 (Data Lake) — 모든 형태 원시 저장, Schema-on-Read 분석]
```
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 80%가 비정형임에도 불구하고 대부분이 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)로 방치되며, [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)와 [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) 방식이 이를 활용하는 현대 아키텍처 표준이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 공책에 줄을 쫙 그어놓고 숫자만 예쁘게 적는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/))만 중요하게 생각했어요.
2. 그런데 알고 보니 사람들이 주고받는 카톡 사진, 유튜브 영상, 목소리 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 같은 자유로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/))가 세상에 훨씬 더(80% 이상) 많았어요!
3. 예전에는 이 영상과 목소리들을 어떻게 계산할지 몰라 창고에 방치([다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))했지만, 이제 똑똑한 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))과 거대한 바다([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) 저장소가 생겨서 버려진 영상 속에서도 숨은 보물을 찾을 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 20 / 262

<- **이전**: [19. 개인정보 비식별화 — k-익명성 / l-다양성 / t-근접성](/knowledge-base/studynote/16_bigdata/01_intro/019_data_de_identification/)
**다음**: [21. 제타바이트 시대 — 2025년 전 세계 생성 데이터 ~175 ZB](/knowledge-base/studynote/16_bigdata/01_intro/021_zettabyte_era_data_explosion/) ->

---
