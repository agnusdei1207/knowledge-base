---
title: 20. 데이터 정형화 비율 — 전체 데이터 중 정형 < 20%, 비정형 > 80%
date: '2024-05-24'
description: 빅데이터 시대의 다크 데이터 문제와 정형/비정형 데이터의 구조적 역전 현상 및 처리 아키텍처
tags:
- bigdata
---

# 20. [[252_data_structured_ratio|데이터 정형화 비율]] (정형 < 20% vs 비정형 > 80%)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기업과 사회에서 [[087_process_state_transition|생성]]되는 전체 [[001_dikw_pyramid|데이터]] 중 RDBMS에 예쁘게 담기는 [[002_structured_data|정형 데이터]]는 20% 미만에 불과하며, 텍스트, 이미지, [[568_logs_distributed_logging_elk_fluentd|로그]], 영상 등 구조가 없는 [[004_unstructured_data|비정형 데이터]]가 80% 이상을 차지하는 구조적 대역전 현상이다.
> 2. **가치**: 이 80%의 [[004_unstructured_data|비정형 데이터]]는 그동안 처리와 분석이 어려워 방치된 '[[062_darkdata|다크 데이터]]([[062_darkdata|Dark Data]])'였으나, 최근 AI와 빅데이터 플랫폼의 발전으로 가장 거대한 비즈니스 인사이트의 원천으로 변모했다.
> 3. **융합**: 이를 처리하기 위해 고전적인 [[010_schema_on_write|Schema-on-Write]] 방식의 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]]) 아키텍처는 붕괴되고, [[136_variance|분산]] 스토리지([[013_hdfs|HDFS]]/[[494_object_storage|Object Storage]]) 기반에 [[009_schema_on_read|Schema-on-Read]] 방식을 결합한 '[[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])'와 '[[146_lakehouse|레이크하우스]]([[146_lakehouse|Lakehouse]])' 아키텍처가 필수적으로 융합된다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

과거 IT 시스템의 중심은 명확한 행(Row)과 열(Column)을 가진 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]](RDBMS)였다. 은행의 거래 내역, 쇼핑몰의 주문 정보 등 구조화된 **[[002_structured_data|정형 데이터]]([[002_structured_data|Structured Data]])**가 [[001_dikw_pyramid|데이터]]의 전부라고 여겨졌다. 그러나 스마트폰의 보급, SNS의 폭발적 성장, 그리고 모든 기기가 인터넷에 연결되는 [[101_iot_concept|IoT]]([[101_iot_concept|사물인터넷]]) 시대가 도래하면서 [[001_dikw_pyramid|데이터]]의 지형이 완전히 뒤집혔다.

현재 전 세계 [[001_dikw_pyramid|데이터]] 발생량의 80% 이상은 이메일 텍스트, [[933_cctv|CCTV]] 영상 [[501_file_definition_logical_record|파일]], 음성 통화 녹음, 서버의 클릭스트림 [[568_logs_distributed_logging_elk_fluentd|로그]], 센서의 시계열 [[001_dikw_pyramid|데이터]] 등 정해진 형태가 없는 **[[004_unstructured_data|비정형 데이터]]([[004_unstructured_data|Unstructured Data]])**가 차지하고 있다. 문제는 이 방대한 [[004_unstructured_data|비정형 데이터]]들이 기존의 DB 시스템에는 저장조차 할 수 없어, 어두운 곳에 쌓인 채 버려지는 **[[062_darkdata|다크 데이터]]([[062_darkdata|Dark Data]])**로 전락한다는 점이다. 빅데이터 기술의 본질적 필요성은 바로 이 80%의 어둠 속에 잠든 [[001_dikw_pyramid|데이터]]에서 AI와 [[241_machine_learning_basics|머신러닝]]을 활용해 혁신적인 가치를 발굴해 내는 데 있다.

다음은 [[001_dikw_pyramid|데이터]] 생태계의 거대한 빙산 구조를 보여주는 도식이다.

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

이 도식의 핵심은 기업이 수면 위 20%의 [[002_structured_data|정형 데이터]]만 분석해서는 결코 시장의 전체 그림(예: 고객이 우리 브랜드를 어떻게 느끼는지, 기계가 언제 고장 날지)을 파악할 수 없다는 것이다. 80%의 [[004_unstructured_data|비정형 데이터]]를 건져 올리기 위해서는 저장소, 처리 엔진, 분석 기법 모두가 근본적으로 달라져야 한다.

> 📢 **섹션 요약 비유**: 예전에는 깨끗하게 포장된 마트의 채소(정형 20%)만으로 요리를 했다면, 이제는 거대한 바다와 정글에서 형태도 모를 야생의 식재료(비정형 80%)가 쏟아져 들어오고 있어, 이것들을 썩히지 않고 요리할 수 있는 완전히 새로운 거대한 만능 주방 기계가 필요해진 상황입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

80%의 [[004_unstructured_data|비정형 데이터]]를 수용하고 분석하기 위해 빅데이터 아키텍처는 [[001_dikw_pyramid|데이터]]의 구조를 강제하는 방식에서 벗어나, 유연성을 극대화하는 방향으로 진화했다. 

#### 1. 정형 vs [[004_unstructured_data|비정형 데이터]] 처리 아키텍처 구성

| 요소명 | [[002_structured_data|정형 데이터]] (20%) 아키텍처 | [[004_unstructured_data|비정형 데이터]] (80%) 아키텍처 | 아키텍처 전환 이유 |
|:---|:---|:---|:---|
| **저장소 (Storage)** | RDBMS ([[188_pl_sql_t_sql_procedural|Oracle]], MySQL), [[493_san_storage_area_network|SAN]]/[[492_nas_network_attached_storage|NAS]] | [[208_data_lake_schema_on_read|Data Lake]], [[494_object_storage|Object Storage]] (AWS S3), [[013_hdfs|HDFS]] | [[004_unstructured_data|비정형 데이터]]의 무한한 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) 및 저비용 저장 |
| **[[005_schema|스키마]] [[268_strategy_pattern|전략]]** | [[010_schema_on_write|Schema-on-Write]] (저장 시 테이블 구조 강제 [[395_verification_process_review|검증]]) | [[009_schema_on_read|Schema-on-Read]] (일단 원시 [[001_dikw_pyramid|데이터]]로 저장, 읽을 때 구조 부여) | 형태가 시시각각 변하는 [[568_logs_distributed_logging_elk_fluentd|로그]]/텍스트 [[001_dikw_pyramid|데이터]]를 [[005_schema|스키마]] 설계 없이 즉시 수용 |
| **처리 엔진** | SQL, [[186_stored_procedure_trigger|Stored Procedure]] | Spark, Flink, NLP [[123_pipe|파이프]]라인, [[018_mapreduce|MapReduce]] | 이미지/텍스트 내의 특징 추출을 위한 [[136_variance|분산]] [[430_index_fast_full_scan|병렬]] 연산 필요 |
| **[[002_database_definition|데이터베이스]]** | RDBMS | [[035_nosql|NoSQL]] ([[037_document|Document]], [[067_db_key_uniqueness_minimality|Key]]-Value, [[104_graph|Graph]], [[151_vector_database_embedding_ann_search|Vector DB]]) | 비정형 [[082_attribute_types_er_model|속성]]([[343_json|JSON]] 등)이나 복잡한 [[083_relationship_in_er_model|관계]]망 저장 최적화 |

#### 2. [[004_unstructured_data|비정형 데이터]]([[062_darkdata|Dark Data]])의 가치화 [[123_pipe|파이프]]라인 흐름

아래 도식은 저장조차 어려웠던 [[004_unstructured_data|비정형 데이터]](예: 고객의 콜센터 음성 녹음과 리뷰 텍스트)가 어떻게 정형화되어 분석 가치를 가지게 되는지 보여준다.

```text
[비정형 데이터의 정형화 파이프라인 (Dark Data to Insight)]

[입력: 비정형 데이터] (음성 녹음 파일, SNS 이미지)
        │
        ▼ (원시 저장)
[Data Lake / Object Storage] --- (무한 용량, 저비용 보관)
        │
        ▼ (특징 추출 및 벡터화 / AI 모델 적용)
[AI / ML Pipeline 계층]
 ├─ STT (Speech-to-Text)  : 음성 -> 텍스트 
 ├─ NLP (감성 분석)       : 텍스트 -> "불만(Negative)", "긍정(Positive)" 분류
 └─ CNN (이미지 인식)     : 이미지 -> "파손된 상품" 객체 검출
        │
        ▼ (추출된 메타데이터의 반정형/정형화)
[NoSQL / Data Warehouse] --- (예: 고객ID | 불만여부 | 상품파손 | 발생시간)
        │
        ▼ (통합 분석)
[BI Dashboard / LLM Prompt Context]
```

이 메커니즘의 핵심은 **"[[004_unstructured_data|비정형 데이터]] 그 자체를 [[298_qkv_attention|쿼리]]하는 것이 아니라, [[190_ai_llm_requirements_specification|AI]] 모델을 통과시켜 [[012_metadata|메타데이터]]나 벡터 값(반정형/정형)으로 변환한 뒤에 융합 분석한다"**는 점이다. 과거에는 사람이 일일이 듣고 태그를 달아야 했던 작업이 딥러닝과 Spark 같은 [[136_variance|분산]] 처리 엔진을 만나면서 자동화되었고, 비로소 80%의 [[062_darkdata|다크 데이터]]에 불을 밝힐 수 있게 되었다.

> 📢 **섹션 요약 비유**: 형태가 제각각인 폐플라스틱 [[459_dummy_test_double|더미]]([[004_unstructured_data|비정형 데이터]])를 그냥 창고([[208_data_lake_schema_on_read|데이터 레이크]])에 쌓아두면 쓰레기([[062_darkdata|다크 데이터]])에 불과하지만, AI라는 거대한 분쇄기와 용광로(ML [[123_pipe|파이프]]라인)를 통과시키면 규격화된 플라스틱 블록([[002_structured_data|정형 데이터]])으로 재탄생하여 새로운 장난감을 조립할 수 있게 되는 과정입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

이러한 비율 역전 현상에 대응하기 위해 [[001_dikw_pyramid|데이터]]를 [[104_classification_analysis|분류]]하는 세 가지 스펙트럼과 그에 맞는 저장 기술의 트레이드오프를 명확히 비교해야 한다.

#### 1. 정형 vs 반정형 vs [[004_unstructured_data|비정형 데이터]] 특성 비교

| 구분 | [[002_structured_data|정형 데이터]] (Structured) | [[003_semi_structured_data|반정형 데이터]] (Semi-structured) | [[004_unstructured_data|비정형 데이터]] (Unstructured) |
|:---|:---|:---|:---|
| **비율 추정** | ~ 20% | 전체 [[001_dikw_pyramid|데이터]]의 중간 연결 고리 | ~ 80% |
| **특징** | 엄격한 고정 [[005_schema|스키마]], 테이블 형태 | [[005_schema|스키마]]가 [[001_dikw_pyramid|데이터]] 내부에 존재 (자기 기술적), 유연한 구조 | 일정한 규칙이나 구조가 전혀 없음 |
| **대표 포맷** | RDB의 Table, Excel | [[343_json|JSON]], XML, HTML, [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] | 텍스트, 오디오, 비디오, 이미지 |
| **저장 및 처리** | RDBMS (강력한 ACID [[191_transaction_concept_states|트랜잭션]]) | [[035_nosql|NoSQL]] ([[540_mongodb|MongoDB]], [[302_cdc|Elasticsearch]]) | [[494_object_storage|Object Storage]], [[013_hdfs|HDFS]], [[151_vector_database_embedding_ann_search|Vector DB]] |
| **검색 및 분석** | SQL 기반 [[083_relationship_in_er_model|관계]] 연산 | [[067_db_key_uniqueness_minimality|Key]]-Value 조회, 트리 파싱 | [[500_inverted_index_elasticsearch|역색인]](Full-text), 벡터 [[348_similarity_search|유사도 검색]] |

이 비교에서 가장 눈여겨볼 부분은 **[[003_semi_structured_data|반정형 데이터]]**의 역할이다. [[004_unstructured_data|비정형 데이터]](예: 기사 원문)가 AI를 거치면 태그가 달린 [[343_json|JSON]] 형태의 [[003_semi_structured_data|반정형 데이터]]로 1차 가공되며, 이는 NoSQL을 거쳐 궁극적으로 DW에 적재될 수 있는 징검다리 역할을 한다.

#### 2. 기술 융합: [[263_llm_large_language_model|LLM]](거대 언어 모델)과 Vector DB의 부상
최근 [[004_unstructured_data|비정형 데이터]] 생태계의 가장 큰 혁신은 LLM의 등장이다. 과거 [[109_text_mining|텍스트 마이닝]]은 키워드 빈도수 분석에 그쳤으나, 이제는 수백만 건의 비정형 PDF 문서를 [[151_vector_database_embedding_ann_search|Vector DB]]([[278_instruction_tuning|임베딩]] 공간)에 저장하고, [[276_fine_tuning|RAG]]([[222_rag_retrieval_augmented_generation|검색 증강 생성]]) 아키텍처를 통해 LLM이 직접 비정형 문서를 읽고 요약해 주는 수준에 이르렀다. 이는 [[004_unstructured_data|비정형 데이터]] 처리의 패러다임을 "[[012_metadata|메타데이터]] 추출"에서 "시맨틱(의미) 이해"로 완전히 진화시켰다.

> 📢 **섹션 요약 비유**: [[002_structured_data|정형 데이터]]가 서랍장 칸마다 딱 맞게 정리된 옷이라면, [[003_semi_structured_data|반정형 데이터]]는 옷에 사이즈 태그가 붙어 행거에 걸려있는 상태고, [[004_unstructured_data|비정형 데이터]]는 바닥에 산더미처럼 쌓인 빨랫감입니다. 최근 등장한 [[190_ai_llm_requirements_specification|AI]]([[263_llm_large_language_model|LLM]])는 이 산더미 속에서 "파란색 줄무늬 티셔츠 찾아줘"라는 말 한마디에 정확히 옷을 끄집어내는 로봇 팔과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 기업이 [[062_darkdata|다크 데이터]]를 자산화하려 할 때, 무작정 [[004_unstructured_data|비정형 데이터]]를 모으는 것은 인프라 재앙을 초래한다.

#### 1. 실무 시나리오: 제조 공장의 예지 정비(Predictive Maintenance) 도입
- **상황**: 기존 ERP에 기록되는 설비 구매 내역/고장 일자(정형 20%)만으로는 공장 가동 중단을 예측하지 못함. 이에 설비의 소음(오디오), 진동 센서(시계열 [[568_logs_distributed_logging_elk_fluentd|로그]]), 외관 [[933_cctv|CCTV]](영상) 등 [[004_unstructured_data|비정형 데이터]] 80%를 수집하기 시작.
- **의사결정 및 난관**: [[004_unstructured_data|비정형 데이터]]는 용량이 기하급수적으로 커 네트워크 병목과 클라우드 스토리지 비용 폭탄을 유발함.
- **기술적 해결책 (아키텍처 분리 [[268_strategy_pattern|전략]])**:
  1. **Edge Tier**: 공장 내 [[235_edge_computing_smart_factory|엣지 컴퓨팅]] 노드에서 [[933_cctv|CCTV]] 영상을 실시간 분석([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]). 정상 영상은 버리고, '불꽃'이나 '연기'가 감지된 영상 프레임과 [[012_metadata|메타데이터]](발생 시간, 위치)만 클라우드로 전송 ([[001_dikw_pyramid|데이터]] 경량화).
  2. **[[146_lakehouse|Lakehouse]] Tier**: 원시 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]](반정형)은 저렴한 클라우드 Object Storage에 저장하되, Apache [[178_parquet_rle_encoding_columnar_compression|Parquet]] 같은 컬럼 기반 [[347_compaction|압축]] 포맷으로 변환하여 저장 공간 1/10로 축소.
  3. **Analytics Tier**: Delta Lake나 Iceberg 포맷을 입혀 비정형 저장소 위에서 직접 빠르고 안전한 SQL [[298_qkv_attention|쿼리]] 수행.

```text
[비정형 데이터 비용/네트워크 최적화 의사결정 트리]

[대용량 비정형 데이터 발생 (CCTV, 센서)]
       │
       ├─ (모두 중앙 클라우드로 전송?) ──> [네트워크 마비, Storage 비용 폭발] (안티패턴)
       │
       ▼ (엣지 필터링 도입)
[Edge Node에서 1차 가공 / 필터링]
       │
       ├─ 정상 패턴 ──> [폐기 또는 24시간 후 자동 덮어쓰기]
       │
       ▼ 이상 패턴 / 요약 메타데이터
[저비용 Object Storage 적재 (Data Lake)]
       │
       ▼ (포맷 변환: CSV -> Parquet 압축)
[Data Lakehouse 기반 AI 통합 예측 모델 학습]
```

#### 2. 실무 도입 시 [[128_water_scrum_fall_anti_pattern|안티패턴]] ([[288_data_swamp_metadata_management_absence|Data Swamp]] 현상)
비정형 [[104_da_as_is_analysis|데이터 아키텍처]]의 가장 치명적 [[352_defect_definition|결함]]은 [[208_data_lake_schema_on_read|데이터 레이크]]가 거대한 쓰레기장인 **[[001_dikw_pyramid|데이터]] 스왐프([[288_data_swamp_metadata_management_absence|Data Swamp]])**로 변질되는 것이다. 구조가 없는 [[001_dikw_pyramid|데이터]]를 넣을 때 '[[012_metadata|메타데이터]](누가, 언제, 왜 만들었는지)'를 태깅하지 않고 마구 던져 넣으면, 나중에 검색 자체가 불가능해져 영원히 꺼내 쓸 수 없는 [[062_darkdata|다크 데이터]]로 회귀한다. 이를 막기 위해 [[213_data_catalog_metadata|데이터 카탈로그]]([[213_data_catalog_metadata|Data Catalog]]) 솔루션 도입이 필수적이다.

> 📢 **섹션 요약 비유**: 물건을 버리긴 아깝다며 끝없이 사서 창고에 대충 쑤셔 박아두면 나중엔 문조차 열 수 없는 '호더([[288_data_swamp_metadata_management_absence|Data Swamp]])'의 방이 됩니다. [[004_unstructured_data|비정형 데이터]]를 저장할 때는 반드시 박스 겉면에 "2023년 겨울 옷"이라는 라벨([[203_metadata_management|메타데이터 관리]])을 붙여 둬야 거대한 창고([[208_data_lake_schema_on_read|Data Lake]])가 제 기능을 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[001_dikw_pyramid|데이터]]의 80%를 차지하는 [[004_unstructured_data|비정형 데이터]]를 처리할 수 있는 역량 확보는 기업 생존의 필수 조건이다.

| 구분 | 정량/정성적 기대효과 및 변화 |
|:---|:---|
| **비즈니스 통찰력** | 고객의 숨겨진 감정, 리뷰, 음성 등 [[062_darkdata|다크 데이터]]에서 행동 패턴을 발굴하여 이탈률 예측 및 개인화 마케팅 달성 |
| **운영 비용 최적화** | 비싼 RDBMS 스토리지에 모든 [[001_dikw_pyramid|데이터]]를 욱여넣던 과거와 달리, 저렴한 [[136_variance|분산]] 스토리지 중심의 저장소 혁신([[208_data_lake_schema_on_read|Data Lake]])으로 [[016_tco|TCO]] 절감 |
| **아키텍처 진화** | [[001_dikw_pyramid|데이터]]를 복사하여 이동시키는 복잡한 [[215_etl_vs_elt_pipeline|ETL]] 방식에서 벗어나, 레이크에 두고 즉시 분석하는 [[585_zero_skipping|Zero]]-[[215_etl_vs_elt_pipeline|ETL]] 및 [[146_lakehouse|레이크하우스]]로 진화 |

결론적으로, **"[[002_structured_data|정형 데이터]]가 기업의 과거(What happened)를 기록한다면, [[004_unstructured_data|비정형 데이터]]는 기업의 미래(What will happen)를 예측하는 맥락([[033_context|Context]])을 제공한다."** 앞으로의 빅데이터 아키텍처는 이 이질적인 두 세계를 어떻게 끊김 없이 하나로 결합(Unified [[319_architecture|Architecture]])할 것인가에 성패가 달려 있으며, [[158_multimodal_clip_vision_audio_encoding|멀티모달]](Multi-modal) [[190_ai_llm_requirements_specification|AI]] 기술이 이 거대한 융합의 핵심 엔진으로 작용할 것이다.

> 📢 **섹션 요약 비유**: [[002_structured_data|정형 데이터]]가 매달 찍히는 깔끔한 통장 잔고(결과)라면, [[004_unstructured_data|비정형 데이터]]는 내가 매일 흘리는 땀방울과 영수증, 주고받은 수많은 카톡 [[389_mesh_topology|메시]]지(과정과 맥락)입니다. 이 80%의 일상을 이해하고 분석할 수 있어야만 진정으로 부자가 되는 미래의 길을 설계할 수 있습니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]])** | 비정형, 반정형, [[002_structured_data|정형 데이터]]를 원시 형태 그대로 규모의 제한 없이 저장하는 저비용 중앙 리포지토리
- **[[062_darkdata|다크 데이터]] ([[062_darkdata|Dark Data]])** | 수집하고 저장 및 처리하고는 있으나 분석이나 비즈니스 의사결정에는 전혀 활용되지 않고 방치되는 [[001_dikw_pyramid|데이터]]
- **[[009_schema_on_read|Schema-on-Read]]** | [[001_dikw_pyramid|데이터]]를 저장할 때는 형태를 따지지 않고 무조건 저장하고, 나중에 분석(Read)할 때 목적에 맞게 [[005_schema|스키마]]를 씌워 읽어내는 접근법
- **[[223_vector_database_embedding|벡터 데이터베이스]] ([[151_vector_database_embedding_ann_search|Vector DB]])** | [[004_unstructured_data|비정형 데이터]](텍스트, 이미지)를 [[190_ai_llm_requirements_specification|AI]] 모델을 통해 고차원의 숫자 벡터로 변환하여 저장하고, 의미적 유사성을 빠르게 검색하는 DB
- **[[001_dikw_pyramid|데이터]] 스왐프 ([[288_data_swamp_metadata_management_absence|Data Swamp]])** | [[208_data_lake_schema_on_read|데이터 레이크]]에 거버넌스([[012_metadata|메타데이터]], 품질 관리 등)가 부재하여, 원하는 [[001_dikw_pyramid|데이터]]를 찾을 수도 쓸 수도 없게 된 [[288_data_swamp_metadata_management_absence|데이터 늪]] 상태

### 📈 관련 키워드 및 발전 흐름도

```text
[정형 데이터 (Structured) — RDBMS 행/열 구조, 전체의 약 20%]
    │
    ▼
[반정형 데이터 (Semi-structured) — JSON/XML/CSV, 스키마 유연]
    │
    ▼
[비정형 데이터 (Unstructured) — 텍스트·이미지·동영상, 전체의 약 80%]
    │
    ▼
[다크 데이터 (Dark Data) — 수집됐으나 활용되지 않는 방치 데이터]
    │
    ▼
[데이터 레이크 (Data Lake) — 모든 형태 원시 저장, Schema-on-Read 분석]
```
[[001_dikw_pyramid|데이터]]의 80%가 비정형임에도 불구하고 대부분이 [[062_darkdata|다크 데이터]]로 방치되며, [[208_data_lake_schema_on_read|데이터 레이크]]와 [[009_schema_on_read|Schema-on-Read]] 방식이 이를 활용하는 현대 아키텍처 표준이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 공책에 줄을 쫙 그어놓고 숫자만 예쁘게 적는 [[001_dikw_pyramid|데이터]]([[002_structured_data|정형 데이터]])만 중요하게 생각했어요.
2. 그런데 알고 보니 사람들이 주고받는 카톡 사진, 유튜브 영상, 목소리 [[501_file_definition_logical_record|파일]] 같은 자유로운 [[001_dikw_pyramid|데이터]]([[004_unstructured_data|비정형 데이터]])가 세상에 훨씬 더(80% 이상) 많았어요!
3. 예전에는 이 영상과 목소리들을 어떻게 계산할지 몰라 창고에 방치([[062_darkdata|다크 데이터]])했지만, 이제 똑똑한 [[231_ai_turing_test|인공지능]]([[190_ai_llm_requirements_specification|AI]])과 거대한 바다([[208_data_lake_schema_on_read|데이터 레이크]]) 저장소가 생겨서 버려진 영상 속에서도 숨은 보물을 찾을 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 20 / 262

← **이전**: [[019_data_de_identification|19. 개인정보 비식별화 — k-익명성 / l-다양성 / t-근접성]]
**다음**: [[021_zettabyte_era_data_explosion|21. 제타바이트 시대 — 2025년 전 세계 생성 데이터 ~175 ZB]] →

---
