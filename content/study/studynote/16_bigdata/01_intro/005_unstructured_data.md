+++
weight = 5
title = "5. 비정형 데이터 유형 — 텍스트/이미지/동영상/음성/로그/SNS/IoT 센서"
description = "텍스트, 이미지, 로그 등 비정형 데이터의 본질적 한계를 극복하고 벡터 임베딩과 NoSQL로 가공하는 전주기 파이프라인 분석"
date = "2024-05-24"
[taxonomies]
tags = ["빅데이터", "비정형데이터", "텍스트마이닝", "오브젝트스토리지", "벡터DB", "NoSQL"]
categories = ["studynote-bigdata"]
+++

# [[004_unstructured_data|비정형 데이터]] 유형 및 처리 아키텍처

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[004_unstructured_data|비정형 데이터]]([[004_unstructured_data|Unstructured Data]])는 고정된 테이블 [[005_schema|스키마]]에 담을 수 없는 텍스트, 미디어, 센서 [[568_logs_distributed_logging_elk_fluentd|로그]] 등으로, 전체 [[087_process_state_transition|생성]] [[001_dikw_pyramid|데이터]]의 80% 이상을 차지하는 핵심 정보의 보고다.
> 2. **가치**: 형태가 불규칙하여 전통적인 SQL로는 [[298_qkv_attention|쿼리]]가 불가능하지만, NLP, 컴퓨터 비전 모델을 통해 수학적 벡터(Vector) 공간으로 [[278_instruction_tuning|임베딩]]([[278_instruction_tuning|Embedding]])함으로써 컴퓨터가 이해할 수 있는 연산 가능한 자산으로 탈바꿈한다.
> 3. **융합**: 원본 보존을 위한 [[494_object_storage|오브젝트 스토리지]](S3), 유연한 구조를 담는 [[035_nosql|NoSQL]]([[540_mongodb|MongoDB]]), 그리고 시맨틱 검색을 위한 [[151_vector_database_embedding_ann_search|Vector DB]]([[320_gnn_vector_db_recommendation|Milvus]], Pinecone)가 결합하여 엔드투엔드([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) 처리 생태계를 이룬다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

현대 비즈니스 환경에서 발생하는 [[001_dikw_pyramid|데이터]]는 크게 정형(Structured), 반정형(Semi-structured), 비정형(Unstructured) [[001_dikw_pyramid|데이터]]로 [[104_classification_analysis|분류]]된다. RDBMS의 테이블 구조에 정확히 들어맞는 [[002_structured_data|정형 데이터]]는 기업 [[001_dikw_pyramid|데이터]]의 빙산의 일각(약 20% 미만)에 불과하다. 나머지 수면 아래의 거대한 영역은 소셜 미디어 텍스트, 고객 센터 통화 녹음(음성), [[933_cctv|CCTV]] 영상(비디오), 그리고 초당 수만 건씩 쏟아지는 [[101_iot_concept|IoT]] 센서 [[568_logs_distributed_logging_elk_fluentd|로그]] 같은 [[004_unstructured_data|비정형 데이터]]로 구성되어 있다.

이러한 [[004_unstructured_data|비정형 데이터]]는 일정한 규칙이나 [[005_schema|스키마]]([[505_schema|Schema]])가 없어 기존의 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]로는 저장과 검색이 근본적으로 불가능하다는 문제의식을 낳았다.

```text
이 도식은 데이터의 구조화 정도에 따른 유형 분류와, 현재 발생 빈도의 압도적 불균형을 보여준다.

[데이터 유형 스펙트럼과 비중]

   정형 데이터 (20% 미만)      반정형 데이터 (브릿지 역할)      비정형 데이터 (80% 이상 집중)
  ┌──────────────────┐    ┌─────────────────────┐    ┌──────────────────────────┐
  │ - RDBMS Tables   │    │ - JSON, XML, HTML   │    │ - SNS 텍스트, 고객 리뷰  │
  │ - Excel CSV      │    │ - NoSQL Documents   │    │ - 이미지(JPG), 영상(MP4) │
  │ - 정산/회계 장부 │ => │ - 센서 발생 로그    │ => │ - 콜센터 음성, 위성 사진 │
  └────────┬─────────┘    └──────────┬──────────┘    └─────────────┬────────────┘
           │                         │                             │
    [ SQL 직접 쿼리 ]         [ Key-Value 탐색 ]           [ 메타데이터 / AI 파싱 필수 ]
```

이 구조 스펙트럼에서 주목해야 할 점은 오른쪽으로 갈수록 기계가 직접 해석하기는 기하급수적으로 어려워지지만, 비즈니스의 잠재적 폭발력(고객의 진짜 의도, 공정 불량의 원인 등)은 더욱 높다는 것이다. 따라서 [[004_unstructured_data|비정형 데이터]]를 폐기하지 않고 담아둘 수 있는 [[494_object_storage|오브젝트 스토리지]] 기반의 '[[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])'와, 비정형 패턴을 수학적 벡터로 변환하는 '[[278_instruction_tuning|임베딩]] [[241_machine_learning_basics|머신러닝]] 모델'의 도입이 기업 생존을 위한 필수 아키텍처로 자리매김했다.

> 📢 **섹션 요약 비유**: [[002_structured_data|정형 데이터]]가 규격이 딱 맞는 '퍼즐 블록'이라면, [[004_unstructured_data|비정형 데이터]]는 크기와 모양이 제각각인 '자연석 바위'와 같다. 규격화된 수납장(RDBMS)에는 바위가 들어가지 않으므로, 넓은 마당([[208_data_lake_schema_on_read|Data Lake]])에 쌓아두고 필요할 때 돌의 특징을 분석([[190_ai_llm_requirements_specification|AI]] [[278_instruction_tuning|임베딩]])하여 활용하는 것이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[004_unstructured_data|비정형 데이터]] 처리는 수집된 원본 [[001_dikw_pyramid|데이터]]를 보존하는 '스토리지 계층'과, 의미를 추출하는 '딥러닝/[[278_instruction_tuning|임베딩]] 계층', 그리고 이를 색인하여 검색하는 '특수 [[002_database_definition|데이터베이스]] 계층'으로 구분된다.

| [[004_unstructured_data|비정형 데이터]] 유형 | 형태적 한계 | 파싱 및 추출 [[001_algorithm_definition|알고리즘]] | 저장 아키텍처 | 실무 활용 |
|:---|:---|:---|:---|:---|
| **텍스트 (SNS/리뷰)** | 문법 불규칙, 동음이의어 | NLP ([[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]]), 형태소 분석, [[117_ner|NER]] | 문서형 [[035_nosql|NoSQL]] ([[540_mongodb|MongoDB]]), [[151_vector_database_embedding_ann_search|Vector DB]] | [[105_exploratory_data_analysis|감성 분석]], 챗봇 |
| **이미지/비디오** | 픽셀 단위 2D/3D [[055_array|배열]] | [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 기반 객체 인식(YOLO), 얼굴 인식 | [[494_object_storage|Object Storage]] (AWS S3) + [[012_metadata|메타데이터]] DB | 불량 탐지, 무인 매장 |
| **[[568_logs_distributed_logging_elk_fluentd|로그]]/이벤트** | 길이 가변적 텍스트 라인 | 정규표현식 파싱(Grok), Logstash 필터 | 검색 엔진 DB ([[302_cdc|Elasticsearch]]) | 보안 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] |
| **음성 (콜센터)** | 주파수 아날로그 파형 | [[819_stt_stateless_transport_tunneling_offload|STT]](Speech-to-Text), 화자 분리 분석 | [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[013_hdfs|HDFS]] (원시) + 텍스트 변환 마트 | 불만 고객 사전 [[655_ir_detection_analysis|식별]] |

비정형 텍스트와 이미지 [[001_dikw_pyramid|데이터]]가 어떻게 기계가 이해할 수 있는 형태로 처리되는지 핵심 벡터 변환([[278_instruction_tuning|Embedding]]) [[123_pipe|파이프]]라인을 살펴보자.

```text
이 흐름도는 비정형 데이터(텍스트/이미지)가 AI 임베딩 모델을 거쳐 수치화된 고차원 벡터로 변환되고 Vector DB에 저장되는 내부 동작을 보여준다.

[비정형 원시 데이터]
 1. 텍스트: "제품 품질이 훌륭합니다"  ────┐
 2. 이미지: [강아지 사진.jpg]         ────┼──>  [ Embedding Model (BERT, ResNet) ]
                                          │     (수백 차원의 실수 배열 공간으로 매핑)
[데이터 변환 및 저장]                       ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Vector DB (Milvus, Pinecone 등)                             │
 │  - ID: doc_001                                              │
 │  - Vector: [0.12, -0.44, 0.89, ... , 0.31] (768차원)        │
 │  - Metadata: { "type": "review", "date": "2024-05" }        │
 └──────────────────────────┬──────────────────────────────────┘
                            │ (시맨틱 유사도 검색: 코사인 유사도, L2 거리 연산)
                            ▼
 [Application] "비슷한 긍정 리뷰를 찾아줘" => (벡터 공간 내 최단 거리 탐색 반환)
```

이 메커니즘의 가장 큰 혁신은 단순한 '단어 일치' 검사에서 벗어나 [[001_dikw_pyramid|데이터]]의 '의미적 유사성(Semantic Similarity)'을 계산할 수 있게 되었다는 점이다. 텍스트의 문맥이나 이미지의 형상을 딥러닝 모델이 수백 차원의 실수 벡터로 치환하면, Vector DB는 벡터 간의 거리를 연산(예: [[359_cosine_similarity|코사인 유사도]])하여 의미가 가장 가까운 [[001_dikw_pyramid|데이터]]를 마이크로초 단위로 찾아낸다. 이 과정에서 병목은 딥러닝 모델의 [[278_instruction_tuning|임베딩]] 추론 시간이며, 실무에서는 이를 해소하기 위해 [[418_gpu|GPU]] 기반의 추론 서버(Triton 등)를 별도로 운영한다.

```python
# 비정형 텍스트를 파싱하여 Vector DB에 저장하는 파이썬 의사 코드
from sentence_transformers import SentenceTransformer
import pinecone

model = SentenceTransformer('paraphrase-multilingual')
raw_text = "배송은 느렸지만 포장이 깔끔해요." # 비정형 텍스트

# 1. 자연어를 고차원 벡터로 변환 (Embedding)
vector_representation = model.encode(raw_text).tolist() 

# 2. Vector DB에 메타데이터와 함께 업로드 (시맨틱 검색 준비)
index.upsert(vectors=[("review_123", vector_representation, {"category": "delivery"})])
```

> 📢 **섹션 요약 비유**: 외국인(컴퓨터)에게 한국어([[004_unstructured_data|비정형 데이터]])를 그대로 들려주면 알아듣지 못한다. 중간에 훌륭한 통역사([[278_instruction_tuning|임베딩]] 모델)가 한국어의 뜻을 외국인의 모국어(수학적 벡터 [[055_array|배열]])로 실시간 번역해 주어야만 비로소 원활한 대화와 지시([[348_similarity_search|유사도 검색]])가 가능해진다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[004_unstructured_data|비정형 데이터]]를 저장하기 위해서는 [[001_dikw_pyramid|데이터]]의 특성에 맞는 적절한 스토리지 솔루션의 조합이 필수적이다. 비정형/[[003_semi_structured_data|반정형 데이터]]를 다루는 3대 스토리지 시스템을 융합 관점에서 비교해 보자.

| 비교 매트릭스 | [[494_object_storage|Object Storage]] (AWS S3) | [[035_nosql|NoSQL]] [[037_document|Document]] ([[540_mongodb|MongoDB]]) | Search Engine ([[302_cdc|Elasticsearch]]) |
|:---|:---|:---|:---|
| **주 목적** | 대용량 원본([[225_raw|Raw]]) 미디어/[[501_file_definition_logical_record|파일]] 보관 | 반정형([[343_json|JSON]]) 기반 애플리케이션 상태 저장 | 대규모 [[568_logs_distributed_logging_elk_fluentd|로그]]/텍스트 전문 검색 (Full-text) |
| **저장 방식** | [[501_file_definition_logical_record|파일]] 자체 + 고유 ID([[067_db_key_uniqueness_minimality|Key]]) 맵핑 매칭 | 계층형 [[037_document|Document]](BSON) 단위 저장 | [[500_inverted_index_elasticsearch|역색인]]([[500_inverted_index_elasticsearch|Inverted Index]]) 기반 단어-문서 매핑 |
| **[[001_dikw_pyramid|데이터]] 수정** | 덮어쓰기만 가능 (In-place 수정 불가) | 필드 단위 부분 업데이트 지원 (Update) | 색인 재구성 과정 비용이 높음 |
| **장단점 트레이드오프**| 비용이 가장 저렴하나, 내부 검색 불가 | [[005_schema|스키마]] 유연성이 높으나 조인([[521_join|Join]]) 연산 취약| 검색 속도 최상, 메모리 자원 소모 극심 |

실제 [[090_service_kubernetes_network_load_balancing|서비스]] 환경에서는 단일 스토리지가 [[004_unstructured_data|비정형 데이터]]를 전담할 수 없다. 다음과 같은 아키텍처적 결합 구조가 요구된다.

```text
이 아키텍처는 비정형 이미지 파일을 저장할 때, 각 스토리지의 한계를 상호 보완하기 위해 시스템을 융합하는 분산 저장 패턴을 보여준다.

[User Upload: 제품 사진.jpg + "강력 추천합니다" 텍스트]
        │
        ├─> (1) 대용량 원본 파일 저장 (비용 절감)
        │      => [ Object Storage (S3) ] -> 반환된 URL: https://s3.../img.jpg
        │
        ├─> (2) 구조화된 메타데이터 및 URL 맵핑 저장 (유연성 확보)
        │      => [ NoSQL (MongoDB) ] -> { id: 1, url: "...", tags: ["electronics"] }
        │
        └─> (3) 텍스트 형태소 파싱 및 역색인 (초고속 전문 검색 지원)
               => [ Elasticsearch ] -> "강력", "추천" 키워드에 id 1 매핑
```

이 패턴의 핵심은 대용량 바이너리(Blob) [[001_dikw_pyramid|데이터]] 자체를 DB에 우겨넣지 않는다는 점이다. [[501_file_definition_logical_record|파일]] 본체는 무한히 저렴한 S3([[494_object_storage|오브젝트 스토리지]])로 빼고, 애플리케이션 로직을 제어하는 [[343_json|JSON]] 껍데기만 NoSQL에 유지하며, 텍스트 검색을 위한 특수 계층을 Elasticsearch로 분리한다. 이는 [[001_dikw_pyramid|데이터]] 정합성을 관리하는 복잡도가 증가하지만 시스템 전체 [[282_performance_tactics|성능]]과 [[452_availability|가용성]]을 극대화하는 표준 실무 아키텍처다.

> 📢 **섹션 요약 비유**: 도서관([[004_unstructured_data|비정형 데이터]] 처리 시스템)에서 무거운 책 원본(미디어 [[501_file_definition_logical_record|파일]])은 지하 서고(S3)에 보관하고, 책의 제목과 위치가 적힌 대출 카드([[035_nosql|NoSQL]])는 안내 데스크에 두며, 책 속 단어까지 빠르게 찾을 수 있는 컴퓨터 검색대([[302_cdc|Elasticsearch]])를 따로 운영하여 효율성을 극대화하는 방식이다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

[[004_unstructured_data|비정형 데이터]]를 다룰 때 맞닥뜨리는 가장 큰 실무적 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]는 [[005_schema|스키마]] 부재로 인한 [[123_pipe|파이프]]라인의 조용한 붕괴(Silent Failure) 현상이다.

```text
이 의사결정 트리는 다양한 포맷이 섞여 들어오는 로그(비정형/반정형) 파이프라인에서 장애를 격리하고 처리하기 위한 운영 플로우를 보여준다.

[웹/앱 로그 스트림 유입 (JSON, Plain Text 혼재)]
        ↓
[로그 수집 에이전트 (Fluentd / Logstash)]
        ↓
[정규식 파싱 시도 (Grok Pattern)] ──(패턴 매칭 실패?)──> [Yes] ─> 폐기 금지! -> Dead Letter Queue (S3 원시 보관)
        ↓ [No]                                                      (추후 수동 분석 또는 패턴 업데이트 후 재처리)
[Elasticsearch 역색인 적재] ──(Dynamic Mapping 충돌?)──> [Yes] ─> Type 에러 경고 발생 (숫자에 문자가 들어옴 등)
        ↓ [No]
[Kibana 대시보드 시각화 및 로그 모니터링]
```

**실무 [[128_water_scrum_fall_anti_pattern|안티패턴]] ([[161_anti_pattern|Anti-pattern]])**
- **[[004_unstructured_data|비정형 데이터]]의 RDBMS 강제 주입**: 애플리케이션 [[568_logs_distributed_logging_elk_fluentd|로그]] 텍스트를 파싱하지 않고 RDBMS의 VARCHAR/CLOB 컬럼에 무작정 때려 넣는 경우. 이후 특정 에러 [[568_logs_distributed_logging_elk_fluentd|로그]]를 찾기 위해 `LIKE '%error%'` [[298_qkv_attention|쿼리]]를 실행하면 [[002_database_definition|데이터베이스]] 전체의 [[428_table_full_scan|테이블 풀 스캔]](Full Scan)이 발생하여 [[090_service_kubernetes_network_load_balancing|서비스]]가 마비된다.
- **Dynamic [[010_schema_mapping|Mapping]] 맹신**: Elasticsearch를 사용할 때 [[154_database_index_b_tree_search_optimization|인덱스]] 매핑을 자동으로 맡겨두면, 센서 [[001_dikw_pyramid|데이터]]의 '100'(숫자)을 정수로 인식하다가 어느 순간 '"100"'(문자열)이 들어올 때 인덱싱 충돌이 발생해 그 이후의 모든 [[001_dikw_pyramid|데이터]]가 적재되지 않는 조용한 장애가 발생한다.

> 📢 **섹션 요약 비유**: 모양이 제각각인 폐기물(비정형 [[568_logs_distributed_logging_elk_fluentd|로그]])을 소각장(분석 DB)에 넣기 전, [[104_classification_analysis|분류]]기(파서)가 인식하지 못하는 낯선 쓰레기가 나타났다고 태워 없애버리면 나중에 중요한 증거를 영영 잃게 된다. 모르는 것은 일단 예비 창고(DLQ)에 보관하는 것이 방어적 운영의 핵심이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[004_unstructured_data|비정형 데이터]] 처리 아키텍처의 내재화는 기업이 '세상의 모든 소리'를 들을 수 있게 됨을 의미한다. 과거에는 매출 장표(정형)를 통해 '무엇이 얼마나 팔렸는가'라는 결과만 알 수 있었다면, 이제는 유튜브 댓글(텍스트)과 매장 [[933_cctv|CCTV]](영상) 분석을 통해 '고객이 이 제품을 왜 싫어하는지', '어떤 동선으로 매장을 이탈하는지'와 같은 인과관계(Why)를 정량적으로 파악할 수 있다.

향후 [[004_unstructured_data|비정형 데이터]] 처리의 패러다임은 대형 언어 모델([[263_llm_large_language_model|LLM]]) 및 [[158_multimodal_clip_vision_audio_encoding|멀티모달]](Multi-modal) [[190_ai_llm_requirements_specification|AI]] 시스템과 완벽히 융합되는 방향으로 진화하고 있다. 텍스트, 이미지, 음성을 개별 [[123_pipe|파이프]]라인이 아닌 하나의 딥러닝 모델이 동시에 벡터화하여 통합된 문맥(Variability)을 이해하는 시대가 도래했으며, 이를 지탱하기 위한 고성능 [[151_vector_database_embedding_ann_search|Vector DB]] ([[320_gnn_vector_db_recommendation|Milvus]], Qdrant 등)의 확산이 빅데이터 표준 인프라의 핵심으로 확고히 자리 잡을 것이다.

> 📢 **섹션 요약 비유**: [[004_unstructured_data|비정형 데이터]] 분석의 완성은 눈 감고 귀 막은 채 장부만 보며 장사하던 사장님(기존 RDBMS)이 비로소 눈을 뜨고 손님들의 표정, 말투, 행동 하나하나([[004_unstructured_data|비정형 데이터]])를 깊이 있게 관찰하며 소통하는 진정한 [[090_service_kubernetes_network_load_balancing|서비스]] 장인으로 거듭나는 과정이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[494_object_storage|Object Storage]]** | 폴더 계층 대신 [[501_file_definition_logical_record|파일]](Object) 단위로 고유 [[289_identification_flags_fragmentation_offset|식별자]]([[067_db_key_uniqueness_minimality|Key]])를 부여하여 무한정 수평 확장되는 비용 효율적 스토리지
- **[[223_vector_database_embedding|Vector Database]]** | 단어 매칭이 아닌 [[001_dikw_pyramid|데이터]]의 의미적 유사도(거리)를 연산하기 위해 고차원 실수 [[055_array|배열]]([[278_instruction_tuning|Embedding]])을 저장하는 특수 DB
- **[[500_inverted_index_elasticsearch|Inverted Index]] ([[500_inverted_index_elasticsearch|역색인]])** | 문서의 위치를 단어 기준으로 정리하여, 비정형 텍스트 내의 키워드를 빛의 속도로 검색하게 해주는 검색 엔진의 핵심 구조
- **[[009_schema_on_read|Schema-on-Read]]** | 정해진 표 구조([[005_schema|스키마]]) 없이 일단 비정형 상태로 원본 저장 후, 필요할 때 로직을 통해 구조를 씌워 읽어내는 개념
- **Dead Letter [[058_queue|Queue]] (DLQ)** | 파싱에 실패하거나 알 수 없는 형태의 [[004_unstructured_data|비정형 데이터]]가 유입됐을 때 유실을 막기 위해 임시로 격리하는 대기열 공간

### 📈 관련 키워드 및 발전 흐름도

```text
[Object Storage]
    │
    ▼
[Vector Database]
    │
    ▼
[Inverted Index (역색인)]
    │
    ▼
[Schema-on-Read]
    │
    ▼
[Dead Letter Queue (DLQ)]
```

이 흐름도는 Object Storage에서 출발해 Dead Letter [[058_queue|Queue]] (DLQ)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 엑셀처럼 칸이 딱딱 나뉘어 있는 공책([[002_structured_data|정형 데이터]])도 있지만, 우리가 찍은 사진, 녹음한 목소리, 낙서장([[004_unstructured_data|비정형 데이터]])은 그런 칸에 절대 들어가지 않아요.
2. 그래서 컴퓨터는 사진이나 목소리를 자기들만 아는 아주 길고 복잡한 숫자 암호(벡터 [[278_instruction_tuning|임베딩]])로 바꾼 다음 넓은 마당([[208_data_lake_schema_on_read|데이터 레이크]])에 던져놓아요.
3. 나중에 우리가 "귀여운 강아지 사진 찾아줘!"라고 말하면, 컴퓨터는 그 숫자 암호들의 거리를 계산해서 뜻이 가장 비슷한 진짜 강아지 사진을 1초 만에 눈앞에 마법처럼 대령한답니다!
