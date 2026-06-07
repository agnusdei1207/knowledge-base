---
title: "004. Unstructured Data"
date: "2024-05-24"
tags:
  - "data_engineering"
  - "studynote-data-engineering"
weight: 4
---
# 04. 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Unstructured [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Unstructured [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 사전 정의된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델이나 규칙([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/))이 전혀 없이 텍스트, 비디오, 오디오, 이미지 형태로 존재하는 거대하고 불규칙한 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리다.
> 2. **가치**: 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 80% 이상을 차지하며, 기존에는 버려지던 '[다크 데이터](/studynote/12_it_management/02_itsm_itil/062_darkdata/)'였으나 최근 딥러닝과 대형 언어 모델([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))의 발전으로 인간의 지식과 맥락을 추출할 수 있는 핵심 자산으로 격상되었다.
> 3. **융합**: 이 방대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저비용으로 보관하기 위해 객체 스토리지([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))가 활용되며, 의미 기반 검색을 위해 벡터 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)(Vector [Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) 기술과 [벡터 데이터베이스](/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/) 아키텍처가 필연적으로 결합된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (Unstructured [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 관계형 DB 테이블이나 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 태그처럼 기계가 즉시 파싱할 수 있는 형태적 단서가 없는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다. 소셜 미디어의 긴 글, 유튜브 비디오 스트림, 콜센터의 음성 녹음 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 위성 이미지 등이 이에 해당한다.
과거 기업의 IT 시스템은 결제 금액, 날짜, 고객 ID 등 정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에만 집중했다. 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 용량만 막대하게 차지하고 "컴퓨터가 읽어서 뜻을 알 수 없는" 블랙박스였기 때문이다. 하지만 스마트폰 보급으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발생량의 80% 이상이 비정형 포맷으로 전환되었고, 기업은 고객의 진정한 의도(감정, 리뷰 맥락, 행동 패턴)가 정형화된 숫자 너머 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 속에 숨어 있음을 깨달았다.
결국 이 방대한 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 버리지 않고 저비용으로 적재([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))한 뒤, [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))을 통해 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)(Feature)와 문맥을 추출하여 비즈니스 가치로 변환해야 하는 근본적인 필요성이 현대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍처를 추동했다.

[데이터 종류별 의미 추출 난이도와 잠재 가치 (문제 배경도)]
```text
[정형 데이터]              [비정형 데이터] (텍스트, 이미지, 음성)
(RDB 테이블)               (자연어 리뷰 "배송은 느렸지만 제품은 예뻐요")
     |                          | (기계가 뜻을 알 수 없음)
 [SQL 쿼리]                     v
     |                  [AI / 딥러닝 모델 개입 필수] => (NLP, Computer Vision)
     v                          | (문맥, 감정, 객체 추출 연산)
[명시적 수치/통계]         [암묵적 인사이트 / 추론 모델링] => (추천, 예측 등 고부가가치 창출)
 (가치 한계치 존재)          (무한한 잠재적 비즈니스 가치 보유)
```
이 도식은 기존 시스템이 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루지 못한 이유와, 현재 왜 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 중요한지 대조하여 보여준다. 정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 쿼리만 던지면 바로 답이 나오지만 창출할 수 있는 통찰의 깊이가 제한적이다. 반면 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 중간에 무거운 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산 모델이 개입해야만 비로소 의미를 추출할 수 있는 병목이 존재하지만, 성공 시 '고객 감정 분석' 등 차원이 다른 고부가가치를 낳는다.

📢 **섹션 요약 비유**: 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 해독법을 모를 때는 자리만 차지하는 수천 권의 '외계어 마법서([다크 데이터](/studynote/12_it_management/02_itsm_itil/062_darkdata/))' 같았지만, 딥러닝이라는 '번역 안경'이 발명되면서 세상의 모든 지식을 담은 보물창고로 돌변했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체는 단순한 바이너리(BLOB) 덩어리이므로, 이를 저장하고 활용하기 위한 두 가지 핵심 인프라가 필요하다. 바로 객체 스토리지([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/))와 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) 변환 파이프라인이다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 실무 의미 |
|:---|:---|:---|:---|
| <strong>객체 스토리지 (<a href="/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">Data Lake</a>)</strong> | 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 원본([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) [영구 저장소](/studynote/05_database/01_db_architecture_relational/059_persistent_storage_data_log_control_file/) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 계층 없이 고유 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)(URI)로 BLOB 형태 플랫 보관 (AWS S3) | 무한한 Scale-out과 초저비용 확보 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> (<a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a>)</strong> | 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찾기 위한 유일한 단서 | 객체 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)일, 크기, 소스 시스템, 해시값 등을 Key-Value로 객체 옆에 첨부 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 검색([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Discovery)의 기반 |
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> 모델 (<a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">Embedding</a>)</strong> | 비정형 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기계가 이해할 수 있는 좌표로 변환 | [CNN](/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)(비전) 또는 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)(텍스트)를 거쳐 수백 차원의 실수 밀집 벡터(Vector)로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 의미적 유사성 수치화 |
| <strong>벡터 DB (<a href="/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/">Vector DB</a>)</strong> | 변환된 벡터 좌표를 저장하고 고속 검색 | [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) ([Approximate Nearest Neighbor](/studynote/05_database/06_dw_olap_trends/351_hnsw/)), [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 기반 거리 계산([코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)) 검색 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 검색 및 [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) ([검색 증강 생성](/studynote/12_it_management/05_security_compliance/222_rag_retrieval_augmented_generation/))의 핵심 |

[비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 수집부터 벡터 변환, 검색까지의 전체 파이프라인 흐름도]
```text
[1. 원시 비정형 데이터 유입] : 기업 PDF 매뉴얼, 고객 음성 파일
        v (무제한 적재: ELT 사상)
[2. Data Lake (AWS S3)] : URI 기반 단순 객체(Object) 저장 (메타데이터 부착)
        v (배치/스트리밍 AI 파이프라인 트리거)
[3. Deep Learning Embedding 변환 연산] (텍스트 -> LLM, 음성 -> STT 후 LLM)
        v
  [ 0.12, -0.45, 0.88, ... 768차원 벡터 데이터 도출 ]
        v
[4. Vector Database 저장 및 검색 인덱싱] (Milvus, Pinecone)
        v (사용자 "에러 해결법 찾아줘" 자연어 질의 발생)
[5. 코사인 유사도 연산을 통한 가장 의미가 비슷한 비정형 원본 매칭 및 반환]
```
이 흐름의 핵심은 "비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 검색할 것인가"라는 난제를 푸는 과정이다. 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 `WHERE name = 'Kim'` 같은 일치 검색이 불가능하다. 따라서 중간의 신경망(Deep [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 파이프라인이 텍스트나 이미지를 수학적 좌표(벡터)로 변환해 벡터 DB에 넣는다. 이후 사용자가 질문을 하면, 그 질의 역시 벡터로 변환되어 '좌표 공간 상에서 가장 거리가 가까운(의미가 유사한) 문서'를 수학적으로 찾아내어 원본 S3 링크를 반환하는 구조다. 이 과정에서 엄청난 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 연산 부하가 발생한다.

📢 **섹션 요약 비유**: 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 검색은 도서관에 무작위로 쌓인 수만 권의 책([데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))을 사서([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))가 미리 전부 읽고 내용의 분위기와 주제에 따라 거대한 우주 지도의 좌표(벡터 변환)를 찍어두어, 비슷한 내용의 책끼리 모여있게 만드는 마법과 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소인 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 전통적인 정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)웨어하우스([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))와 목적과 사상이 대척점에 있다.

| 비교 항목 | RDBMS / [Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/) (정형) | [Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) / 객체 스토리지 (비정형) | 판단 포인트 |
|:---|:---|:---|:---|
| **저장 전제 조건** | 명확한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)와 정제([ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)) 필수 | 아무 조건 없이 원시 형태 그대로 적재 | 수집 속도 및 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 인프라 오버헤드 |
| <strong>주요 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 형식</strong> | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 결제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 동영상, 이미지, SNS 텍스트 덤프 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스의 다양성 (Variety) |
| **사용자** | 비즈니스 분석가 (SQL 사용) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트 (Python, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사용) | 통찰의 목적 (통계 리포트 vs 예측 모델) |
| **비용 구조** | 스토리지 비용 매우 높음 ([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), 연산결합) | 스토리지 비용 극도로 낮음 (저가 디스크 분리) | 장기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Retention](/studynote/05_database/04_transactions_concurrency/515_mvcc/)) 능력 |

[정형/비정형 아키텍처의 연산 부하 위치 (병목) 비교도]
```text
< 전통적 정형 데이터 (Schema-on-Write) >
(유입) => [ 🚨병목: ETL 텍스트 파싱/정규화 연산 ] => [ RDBMS 저장 ] => (조회) 즉시 응답

< 비정형 데이터 (Schema-on-Read / Data Lake) >
(유입) => [ S3 단순 덤프 저장 (병목 0, 초고속) ] => [ 🚨병목: 스파크/AI 읽을 때 연산 부하 ] => 인사이트 도출
```
이 비교도는 두 진영 아키텍처의 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 철학을 명확히 대조한다. 정형 DB는 넣을 때 뼈를 깎는 정제 작업([ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/))을 거치지만 읽을 때는 쾌적하다. 반면 비정형 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 유입 속도(Velocity)를 늦추지 않기 위해 일단 무지성으로 다 저장해놓고, 나중에 분석가가 필요할 때 거대한 컴퓨팅 클러스터(Spark, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))를 띄워 무거운 연산을 돌린다. 클라우드 시대에 컴퓨팅 자원을 필요할 때만 빌려 쓸 수 있게 되면서, 이 [Schema-on-Read](/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) 방식이 대세로 자리 잡았다.

📢 **섹션 요약 비유**: 정형 시스템은 재료를 씻고 썰어 완벽하게 준비한 뒤에만 냉장고([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))에 넣는 것이고, 비정형 시스템은 마트에서 사 온 봉지째로 거대한 냉동고([데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))에 쑤셔 넣고 나중에 요리할 때 해동하며 다듬는 방식입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룰 때는 비용 통제와 보안, 그리고 '[데이터 늪](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)' 화를 방지하는 거버넌스가 핵심이다.

1. <strong><a href="/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">데이터 늪</a> (<a href="/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">Data Swamp</a>) <a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: S3 같은 객체 스토리지 비용이 싸다고 비정형 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)나 이미지를 아무런 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 없이 [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 때려 넣으면, 1년 뒤 아무도 그 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 무엇인지 알 수 없어 검색 자체가 불가능해진다.
   - **판단**: 적재 시점(Ingestion)에 내용 자체를 정제하진 않더라도, 반드시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)명, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 일자, 소스 시스템, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(Year/Month/Day) 등의 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 강제로 태깅하고 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/))에 등록시키는 파이프라인 자동화가 필수적이다.
2. <strong>비정형 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 내 <a href="/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a>(PII) 노출 위험</strong>: 콜센터 음성을 텍스트로 변환한 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 주민등록증 이미지에는 치명적인 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)가 섞여 있으며, 정형 테이블처럼 컬럼 단위 암호화나 마스킹이 불가능하다.
   - **판단**: 비정형 원본이 레이크에 안착하기 직전이나 직후에, 정규표현식 기반의 필터나 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반의 PII(Personally Identifiable Information) 탐지(Named Entity Recognition) 모델을 통과시켜 민감 정보를 실시간으로 비식별화(마스킹)하는 보안 구역(Clean Room)을 거쳐야 한다.
3. **비용 한계 및 수명주기 관리 부재**: 아무리 저렴한 객체 스토리지라도 수백 페타바이트의 비정형 영상이 쌓이면 비용이 감당 안 된다.
   - **판단**: S3 Intelligent-Tiering과 같은 정책을 활성화하여 90일 이상 접근하지 않은 비정형 객체는 딥 아카이브(Glacier) 계층으로 자동 이관시키는 ILM(Information [Lifecycle Management](/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/)) 룰을 설계 단계에서 확정해야 한다.

[비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 안전한 활용을 위한 거버넌스 운영 플로우]
```text
[비정형 원본 (이미지/텍스트)]
       v
[PII 비식별화 파이프라인 (AI 검출기)] --(실패/예외)--> [격리 큐 (보안팀 수동 검토)]
       v (마스킹 완료)
[메타데이터 태깅 (날짜/분류 키)] => (동시에 Data Catalog DB에 인덱스 등록)
       v
[Data Lake (Gold Zone) 적재] => (이후 100일 경과 시 Cold Storage로 자동 하강)
```
이 의사결정 트리는 방치되기 쉬운 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기업의 통제 하에 두기 위한 실무적 가이드라인이다. 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 유연성을 핑계로 보안과 메타 관리를 방치하면 대형 컴플라이언스 위반이나 인프라 비용 폭탄을 맞게 된다. 따라서 저장소 앞단에 필수적인 가드레일(마스킹, 태깅)을 두어 품질을 담보해야 한다.

📢 **섹션 요약 비유**: 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모으는 것은 블랙박스를 창고에 쌓는 것과 같습니다. 상자 겉면에 최소한 '언제 어디서 온 상자'인지 견출지([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/))를 붙이고, 안에 폭발물([개인정보](/studynote/09_security/16_data_privacy/781_personal_information/))이 없는지 엑스레이(PII 검사)를 통과시킨 후에만 입고시켜야 창고가 마비되지 않습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 기술의 성숙은 기업이 가진 암묵지(Tacit Knowledge)를 명시적 자산으로 전환하는 기술적 특이점을 가져왔다.

| 관점 | 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 기대효과 | 정량/정성적 지표 |
|:---|:---|:---|
| 비즈니스 인사이트 | 콜센터 음성 및 리뷰 텍스트 감성 분석을 통한 고객 이탈 방어 | 고객 만족도(CSAT) 향상 및 이탈률 감소 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기술 확보 | [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([대규모 언어 모델](/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/))의 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)([Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 확보 | 기업 맞춤형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 비서([RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)) 구축 성공률 획득 |

미래에는 정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 경계가 무너지는 <strong><a href="/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/">데이터 레이크하우스</a> (<a href="/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/">Data Lakehouse</a>)</strong> 아키텍처가 완전히 자리 잡을 것이다. Iceberg나 [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 같은 오픈 테이블 포맷이 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 위의 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리에 ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 기능을 부여함으로써, 비정형 저장소에서도 마치 정형 DB처럼 빠르고 안전하게 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조작할 수 있는 하이브리드 표준으로 진화하고 있다. 결국 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대의 가장 중요한 원유로서 인프라 설계의 영원한 핵심 축이 될 것이다.

📢 **섹션 요약 비유**: 과거 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 묻혀있던 쓸모없는 흙더미였다면, 이제는 고성능 정유 기계(AI와 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/))를 만나 비즈니스의 엔진을 폭발적으로 돌리는 시커먼 원유(석유)가 되었습니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비롯한 모든 종류의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 없이 무제한으로 저장하는 객체 스토리지
* 객체 스토리지 ([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) | [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 계층 없이 고유 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)(URI)와 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)로 비정형 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 보관하는 클라우드 인프라
* [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) ([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) | 비정형 텍스트/이미지를 인공신경망을 통해 기계가 연산할 수 있는 실수 벡터 좌표로 변환하는 기술
* [벡터 데이터베이스](/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/) ([Vector DB](/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/)) | 벡터화된 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 유사도(거리)를 고속으로 연산하여 맥락 검색을 제공하는 시스템
* [다크 데이터](/studynote/12_it_management/02_itsm_itil/062_darkdata/) ([Dark Data](/studynote/12_it_management/02_itsm_itil/062_darkdata/)) | 기업에 저장되어 있으나 구조화되지 않아 분석이나 비즈니스에 활용되지 못하고 방치된 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 레이크 (Data Lake)]
    |
    v
[객체 스토리지 (Object Storage)]
    |
    v
[임베딩 (Embedding)]
    |
    v
[벡터 데이터베이스 (Vector DB)]
    |
    v
[다크 데이터 (Dark Data)]
```

이 흐름도는 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))에서 출발해 [다크 데이터](/studynote/12_it_management/02_itsm_itil/062_darkdata/) ([Dark Data](/studynote/12_it_management/02_itsm_itil/062_darkdata/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 글, 사진, 녹음된 목소리처럼 규칙 없이 자유롭게 만들어진 거대한 일기장 같아요.
2. 옛날 컴퓨터는 이 일기장의 뜻을 몰라서 그냥 창고에 쌓아두기만 했어요.
3. 하지만 지금은 똑똑한 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 안경이 생겨서, 일기장의 내용을 읽고 숨겨진 보물 같은 힌트를 찾아낼 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 4 / 258

<- **이전**: [3. 반정형 데이터 (Semi-structured Data) - 데이터 내부(태그)에 구조(메타데이터)를 포함 (XML, JSON, 로그)](/studynote/14_data_engineering/01_infrastructure/003_semi_structured_data/)
**다음**: [5. 데이터 웨어하우스 (DW, Data Warehouse) - 전사적 관점의 비즈니스 인텔리전스(BI)를 위한 통합/주제별/시계열 데이터](/studynote/14_data_engineering/01_infrastructure/005_data_warehouse/) ->

---
