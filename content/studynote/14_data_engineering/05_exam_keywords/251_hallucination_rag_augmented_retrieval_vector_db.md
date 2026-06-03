+++
title = "251. 할루시네이션 (Hallucination) RAG (Retrieval Augmented Generation) 벡터 DB"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))은 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 범위 밖이나 최신 정보에 대해 그럴듯하지만 틀린 답변([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/))을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.
> 2. **가치**: [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)(Retrieval Augmented Generation)는 외부 지식 베이스에서 관련 문서를 실시간 검색하여 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)로 주입함으로써 할루시네이션을 근본적으로 억제한다.
> 3. **판단 포인트**: 벡터 DB([Vector Database](/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/)) 선택(Pinecone·Weaviate·[Milvus](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/320_gnn_vector_db_recommendation/))과 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) 품질이 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 시스템의 전체 정확도를 결정짓는 핵심 변수이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 할루시네이션([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) 이란?

LLM은 다음 토큰(Token)을 예측하는 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델이다. 따라서 사실 여부와 무관하게 통계적으로 그럴듯한 텍스트를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. 이 현상을 **할루시네이션([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/))**이라 한다.

| 원인 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 상세 설명 |
|:---|:---|
| **훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 컷오프(Cutoff)** | 특정 날짜 이후 정보는 모델 가중치에 없음 |
| **[확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)** | 토큰 예측이 사실 DB 조회가 아니라 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 샘플링 |
| **편향된 학습 코퍼스(Corpus)** | 인터넷 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 오류·편향 그대로 학습 |
| **긴 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 소실** | 긴 문서 처리 시 초반 정보 주의가 약해짐 |
| **지식 공백** | 희귀하거나 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 지식 부재 |

### 1.2 할루시네이션이 문제인 이유

의료 진단, 법률 자문, 금융 분석 등 정확성이 요구되는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 LLM이 오답을 자신 있게 제시하면 치명적 결과로 이어진다. 예를 들어 존재하지 않는 판례를 인용하거나, 신약 부작용을 잘못 설명할 수 있다.

📢 **섹션 요약 비유**: LLM은 기억력 좋은 대학생과 같다. 배운 범위 내에서는 정확하지만, 모르는 문제를 만나면 외운 패턴으로 그럴듯한 오답을 써낸다. 답안지에 "모름"이라고 쓰지 않고 자신감 넘치게 오답을 제출하는 것이 할루시네이션이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)(Retrieval Augmented Generation) 구조

RAG는 세 단계로 구성된다: **검색(Retrieval) → 증강(Augmentation) → [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)(Generation)**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAG 파이프라인 (RAG Pipeline)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  사용자 질의(Query)                                               │
│        │                                                         │
│        ▼                                                         │
│  ┌───────────────┐    임베딩(Embedding)     ┌──────────────────┐ │
│  │  쿼리 인코더   │ ─────────────────────► │  벡터 DB         │ │
│  │(Query Encoder)│                         │ (Vector DB)      │ │
│  └───────────────┘                         │  Pinecone/       │ │
│                                            │  Weaviate/Milvus │ │
│                                            └────────┬─────────┘ │
│                                                     │           │
│                                          유사도 검색(Top-K)      │
│                                                     │           │
│                                                     ▼           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             컨텍스트 주입(Context Injection)               │   │
│  │  프롬프트 = "다음 문서를 참고하여 답하라: [검색문서1,2,3]  │   │
│  │             + 사용자 질의"                                 │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│                   ┌───────────────┐                              │
│                   │    LLM 생성   │                              │
│                   │ (Generation)  │                              │
│                   └───────────────┘                              │
│                           │                                      │
│                           ▼                                      │
│                   사실 기반 응답(Grounded Response)               │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 벡터 DB([Vector Database](/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/)) 핵심 개념

**[임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))**: 텍스트를 고차원 벡터로 변환하는 과정. 의미적으로 유사한 텍스트는 벡터 공간에서 가까운 거리에 위치한다.

| 벡터 DB | 특징 | 적합 사용 사례 |
|:---|:---|:---|
| **Pinecone** | 완전 관리형 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/), 빠른 시작 | [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/), 중소규모 |
| **Weaviate** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) | [하이브리드 검색](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/) |
| **[Milvus](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/320_gnn_vector_db_recommendation/)** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 대규모 확장성, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 지원 | 기업 대규모 배포 |
| **Chroma** | 로컬 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/), Python 친화적 | 개발/테스트 환경 |
| **Qdrant** | 러스트([Rust](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/)) 기반 고성능 | [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 민감 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

### 2.3 [유사도 검색](/knowledge-base/studynote/05_database/06_dw_olap_trends/348_similarity_search/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([Similarity Search](/knowledge-base/studynote/05_database/06_dw_olap_trends/348_similarity_search/))

- **[코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)([Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))**: 두 벡터 간 각도 측정, 방향성 중심
- **[HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)(Hierarchical Navigable Small World)**: 근사 최근접 이웃([ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/), [Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), O(log N) 검색 복잡도
- **IVF(Inverted [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))**: 클러스터 기반 색인, 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 효율적 검색

📢 **섹션 요약 비유**: 벡터 DB는 도서관의 의미 지도(Semantic Map)다. 책 제목이 아니라 "내용의 의미"로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해두기 때문에 "당뇨 치료"를 검색하면 "인슐린 분비 조절"이라는 제목의 책도 찾아준다. 전통 도서관(키워드 검색)과 달리 의미 기반으로 동의어와 유의어까지 포괄한다.

---

## Ⅲ. 비교 및 연결

### 3.1 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) vs [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) vs [Prompt Engineering](/knowledge-base/studynote/12_it_management/05_security_compliance/224_prompt_engineering_guideline/) 비교

| 기법 | 지식 갱신 | 비용 | 정확도 | 적합 시나리오 |
|:---|:---|:---|:---|:---|
| **[프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)([Prompt Engineering](/knowledge-base/studynote/12_it_management/05_security_compliance/224_prompt_engineering_guideline/))** | 불가 | 최저 | 낮음 | 단순 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) |
| **[RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)** | 실시간 | 중간 | 높음 | 최신 정보 필요 |
| **파인튜닝([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))** | 배치성 | 고비용 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 | 특정 스타일/언어 |
| **[RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) + [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)** | 실시간 + 배치 | 최고 | 최고 | 엔터프라이즈 |

### 3.2 [Advanced RAG](/knowledge-base/studynote/10_ai/03_llm_nlp/218_rag_advanced_techniques/) 기법

기본 RAG의 한계(청크 경계 손실, 다중 홉 추론 어려움 등)를 극복하는 고도화 기법:

| 기법 | 설명 | 효과 |
|:---|:---|:---|
| **HyDE(Hypothetical [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) Embeddings)** | 질의로 가상 답변 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 후 이를 검색 쿼리로 사용 | 검색 정확도 향상 |
| **Multi-query Retrieval** | 동일 질의를 여러 방식으로 변형하여 다중 검색 | [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)) 향상 |
| **Re-ranking** | 검색된 문서를 크로스 [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)(Cross-Encoder)로 재정렬 | 관련성 개선 |
| **Self-[RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)** | LLM이 검색 필요 여부 스스로 판단 | 불필요 검색 감소 |
| **[Corrective](/knowledge-base/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)(CRAG)** | 검색 결과 품질 평가 후 웹 검색 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) | [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 향상 |

📢 **섹션 요약 비유**: 기본 RAG가 도서관 사서에게 한 번 질문하는 것이라면, Advanced RAG는 사서에게 여러 방식으로 질문하고, 찾아온 책을 다시 품질 검사하고, 필요하면 인터넷까지 뒤지는 베테랑 연구원의 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 기업 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 시스템 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 및 전처리**: PDF·HTML·DB 문서를 청크(Chunk)로 분할 (512~1024 토큰 권장)
2. **[임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 모델 선택**: OpenAI `text-embedding-3-large`, `bge-m3`(한국어 강점) 등
3. **벡터 DB 운영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**: [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 필터(날짜·출처·카테고리)로 검색 범위 한정
4. **[컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 창([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Window) 관리**: 검색 결과가 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 한도 초과 방지
5. **평가 지표**: [RAGAS](/knowledge-base/studynote/10_ai/03_llm_nlp/225_rag_evaluation_ragas/)([RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) Assessment) 프레임워크 — Faithfulness, Answer Relevancy, [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)

### 4.2 할루시네이션 감지 및 방어 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
┌────────────────────────────────────────────────────────┐
│              할루시네이션 방어 계층                      │
├────────────┬──────────────────────────────────────────┤
│ 입력 계층  │ 질의 분류 → 검색 필요성 판단              │
│ 검색 계층  │ 하이브리드 검색(벡터 + BM25 키워드)       │
│ 생성 계층  │ 소스 인용 강제(Citation Grounding)        │
│ 검증 계층  │ NLI(자연어 추론) 기반 사실 검증            │
│ 출력 계층  │ 신뢰도 점수(Confidence Score) 사용자 노출 │
└────────────┴──────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: RAG는 오픈북 시험(Open Book Exam)으로 바꾸는 것이다. 모든 것을 외워야 했던 기존 방식 대신, 시험장에 자료집(외부 DB)을 들고 들어가 참조하며 답변한다. 자료집의 품질(벡터 DB)과 빠르게 찾는 능력([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 검색)이 좋아야 좋은 점수를 받는다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 도입 효과 요약

| 기대효과 | 정량적 지표 |
|:---|:---|
| 할루시네이션 감소 | 사실 기반 응답률 60~80% 향상 |
| 최신성(Freshness) | 실시간 지식 반영 (파인튜닝 없이) |
| 비용 효율 | 대규모 재훈련 불필요 |
| 투명성 | 출처 문서 인용 가능 |
| 컴플라이언스 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 등 규제 준수 (특정 문서 제거 가능) |

### 5.2 기술 발전 방향

RAG는 단순 문서 검색에서 **에이전틱 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)(Agentic [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/))**로 진화 중이다. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 에이전트(Agent)가 멀티스텝 추론을 수행하며 도구(Tool) 호출과 반복 검색을 자율적으로 조합한다. 나아가 **[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)([Graph RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/530_graph_rag/))**는 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))와 결합하여 개념 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 추론 능력을 대폭 향상시킨다.

📢 **섹션 요약 비유**: RAG는 인터넷이 등장했을 때와 같은 혁명이다. 기존 LLM이 "내 머릿속에 있는 것만 말할 수 있는 백과사전"이었다면, RAG는 "구글 검색을 한 후 답하는 전문가"다. 검색 기술이 발전할수록 전문가의 답변 품질도 함께 올라간다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 문제 | 할루시네이션([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) | LLM이 사실과 다른 그럴듯한 답변 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 해결책 | [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)(Retrieval Augmented Generation) | 외부 문서 검색 후 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 주입 |
| 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 벡터 DB([Vector Database](/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/)) | [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터 저장·검색 특화 DB |
| 핵심 기술 | [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) | 텍스트→고차원 벡터 변환 |
| 유사도 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/) | 근사 최근접 이웃 검색, O(log N) |
| 고도화 기법 | [Advanced RAG](/knowledge-base/studynote/10_ai/03_llm_nlp/218_rag_advanced_techniques/) | HyDE, Multi-query, Re-ranking |
| 평가 프레임워크 | [RAGAS](/knowledge-base/studynote/10_ai/03_llm_nlp/225_rag_evaluation_ragas/) | Faithfulness·Relevancy·[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 측정 |
| 미래 방향 | Agentic [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) | 멀티스텝 자율 검색 및 추론 |

### 👶 어린이를 위한 3줄 비유 설명
1. LLM은 아주 많이 공부한 학생인데, 가끔 잘 모르는 문제를 마치 아는 것처럼 틀린 답을 자신 있게 써버려요. 이게 할루시네이션이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
LLM 할루시네이션 (사실과 다른 생성)
    │
    ▼
RAG: 외부 문서 검색 → 컨텍스트로 생성
    ├─► Vector DB: FAISS · Pinecone · Weaviate
    └─► Chunking · Embedding · Re-ranking
    │
    ▼
Advanced RAG: Self-RAG · Corrective RAG · Graph RAG
```
2. RAG는 그 학생에게 시험 중에 도서관을 이용할 수 있게 해주는 거예요. 책에서 관련 내용을 찾아서 그걸 보고 답을 쓰니까 훨씬 정확해지죠.
3. 벡터 DB는 그 도서관에서 "의미가 비슷한 책들"을 빠르게 찾아주는 똑똑한 사서예요. 제목이 달라도 내용이 비슷하면 딱 골라줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 251 / 258

← **이전**: [250. RLHF (Reinforcement Learning from Human Feedback) 정렬 CoT 프롬프트 심화](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/)
**다음**: [252. 지식 증류 (Knowledge Distillation) 양자화 (Quantization) 경량 SLM 디퓨전 생성](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) →

---
