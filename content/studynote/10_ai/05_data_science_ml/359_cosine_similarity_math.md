---
title: "Cosine Similarity"
date: "2026-05-09"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)([Cosine Similarity](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))는 두 벡터 사이의 각도(θ)의 코사인 값으로 방향적 유사성을 측정하며, 벡터의 크기(magnitude)를 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)하므로 문서 길이에 무관한 텍스트 유사도 측정에 최적화된 거리 척도다.
> 2. **가치**: "[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"와 "[인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)"처럼 의미는 같지만 하나는 2자, 다른 하나는 4자인 경우 [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 벡터의 L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 후 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)를 계산하면 크기 차이를 무시하고 의미적 방향만 비교해 높은 유사도를 얻는다.
> 3. **판단 포인트**: cos(θ) = (A·B)/(|A||B|) = ΣAᵢBᵢ/√(ΣAᵢ^·ΣBᵢ^) 범위는 [-1, 1]이며, L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 벡터 간의 내적([Dot](/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/) Product)이 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)와 동치다.

---

## Ⅰ. 개요 및 필요성

검색 엔진에서 "기계 학습"이라는 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 가장 유사한 문서를 찾을 때, 짧은 문서([10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0단어)와 긴 문서(1,000단어)를 유클리드 거리로 비교하면 긴 문서의 단어 빈도가 절대적으로 크므로 불공평하다. [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 두 벡터의 방향만 비교하므로 문서 길이(크기)에 무관하게 의미적 유사도를 측정한다. [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 모델의 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공간에서 의미론적 [유사도 검색](/studynote/05_database/06_dw_olap_trends/348_similarity_search/)(Semantic [Similarity Search](/studynote/05_database/06_dw_olap_trends/348_similarity_search/))의 핵심 지표다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 "나침반 방향 비교"다. 두 사람이 걷는 거리(벡터 크기)는 달라도, 같은 방향(북쪽)을 향하면 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) = 1(동일 방향)이다. AI는 문서의 "방향성(주제)"만 보고 유사도를 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+---------------------------------------------------------+
|           코사인 유사도 수식 및 기하학적 의미            |
+---------------------------------------------------------+
|                                                         |
|  cos(θ) = (A·B) / (|A|·|B|)                           |
|         = ΣᵢAᵢBᵢ / √(ΣᵢAᵢ^) · √(ΣᵢBᵢ^)             |
|                                                         |
|  θ=0+  -> cos=1.0  -> 완전 동일 방향 (최고 유사)        |
|  θ=90+ -> cos=0.0  -> 직교 (무관)                       |
|  θ=180+-> cos=-1.0 -> 반대 방향 (최저 유사)             |
|                                                         |
|  L2 정규화 후 내적:                                    |
|  + = A/|A|,  b̂ = B/|B|   (단위 벡터)                  |
|  cos(θ) = + · b̂          (정규화된 내적)              |
|                                                         |
|  ANN 검색: FAISS/Milvus에서 코사인 거리 =1-cos(θ)     |
+---------------------------------------------------------+
```

| 유사도/거리 | 수식 | 크기 영향 | 주요 용도 |
|:---|:---|:---|:---|
| [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) | A·B/\|A\|\|B\| | ❌ 무관 | 텍스트, [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 유클리드 거리 | √Σ(Aᵢ-Bᵢ)^ | ✅ 영향 있음 | K-Means, [KNN](/studynote/10_ai/03_llm_nlp/262_knn/) |
| 내적 ([Dot](/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/) Product) | Σ AᵢBᵢ | ✅ 영향 있음 | Attention Score |
| 맨해튼 거리 (L1) | Σ\|Aᵢ-Bᵢ\| | ✅ 영향 있음 | 희소 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

- **📢 섹션 요약 비유**: L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 후 내적 = [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 "모든 선수를 같은 체급(단위 벡터)으로 맞춘 뒤 방향 비교"다. 체급(크기)을 통일하면 내적만으로 방향 유사도를 공정하게 측정할 수 있다.

---

## Ⅲ. 비교 및 연결

PPMI(Positive Pointwise [Mutual Information](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/), 양의 점별 상호정보)와 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)의 결합: [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 벡터에 PPMI [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 적용하면 희귀 단어의 공동 등장 패턴을 더 잘 포착한다. [벡터 데이터베이스](/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/)([Vector Database](/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/), [Milvus](/studynote/07_enterprise_systems/05_data_bi/320_gnn_vector_db_recommendation/), Pinecone, Weaviate)에서 [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/)([Approximate Nearest Neighbor](/studynote/05_database/06_dw_olap_trends/351_hnsw/), 근사 최근접 이웃) 검색은 FAISS의 [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/)([Hierarchical Navigable Small World](/studynote/05_database/06_dw_olap_trends/352_rag/)) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 수십억 벡터에서 밀리초 내 코사인 [유사도 검색](/studynote/05_database/06_dw_olap_trends/348_similarity_search/)을 지원한다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) ([Cosine Similarity](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: 벡터 DB에서 코사인 [유사도 검색](/studynote/05_database/06_dw_olap_trends/348_similarity_search/)은 "도서관 사서 없는 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 도서 추천"이다. 수십억 권의 책(벡터) 중에서 "이 책과 방향이 비슷한 책 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)권"을 밀리초 만에 찾아주는 FAISS가 ChatGPT의 [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)([Retrieval-Augmented Generation](/studynote/04_software_engineering/09_cloud_native_ai_architecture/585_rag_retrieval_augmented_generation/)) 시스템 뒤에서 돌아간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[추천 시스템](/studynote/10_ai/03_llm_nlp/211_recommendation_system/)에서 사용자 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터와 아이템 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터의 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) 상위 K개를 추천한다(Item-based CF). Sentence-[BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(SBERT) 같은 문장 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 모델은 [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)로 의미론적 문장 검색(Semantic Search)을 구현한다. 주의: 이진 특성 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(0/1 벡터)에서는 자카드 유사도(Jaccard Similarity)가 더 적합하고, 고차원 희소 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/))에서는 코사인이 적합하며 밀집 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 출력)도 코사인이 적합하다.

- **📢 섹션 요약 비유**: [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 "유튜브 추천 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 심장"이다. 내가 본 영상의 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터와 방향이 가장 비슷한 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)을 가진 영상 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)개를 추천한다. 영상 길이(크기)가 달라도 주제 방향이 비슷하면 추천된다.

---

## Ⅴ. 기대효과 및 결론

[코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 자연어 처리(NLP)와 정보 검색([IR](/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/)) 분야의 표준 유사도 척도로, [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공간에서 의미론적 검색의 핵심 수식이다. L2 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 벡터에서 내적이 코사인과 동치라는 사실은 GPU에서 행렬 곱으로 수십억 쌍의 유사도를 효율적으로 계산할 수 있게 해준다.

- **📢 섹션 요약 비유**: [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 "나침반 거리"다. 얼마나 멀리 걸어왔는지(벡터 크기)가 아니라, 같은 방향(주제/의미)을 향하고 있는지만 측정한다. ChatGPT의 RAG부터 유튜브 추천까지, 이 단순한 삼각함수 공식이 현대 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 검색의 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) | 텍스트 벡터화 / [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) 입력 |
| 벡터 DB ([Milvus](/studynote/07_enterprise_systems/05_data_bi/320_gnn_vector_db_recommendation/), FAISS) | [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) 검색 / [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) 대규모 검색 |
| SBERT | 문장 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) / 코사인 기반 의미 검색 |
| [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) ([Retrieval-Augmented Generation](/studynote/04_software_engineering/09_cloud_native_ai_architecture/585_rag_retrieval_augmented_generation/)) | [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 지식 검색 / [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)로 관련 문서 검색 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [코사인 유사도 (Cosine Similarity)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [코사인 유사도](/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 "두 사람이 같은 방향을 바라보고 있는가"를 측정하는 거예요.
2. 얼마나 멀리 있는지(거리)가 아니라, 같은 곳을 향하고 있는지(방향)만 보는 게 핵심이에요.
3. 검색 AI가 "이 질문과 가장 관련 있는 문서"를 찾을 때 이 방법으로 수십억 개 중 1초 만에 찾아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 359 / 420

<- **이전**: [358. 계층적 군집화 (Hierarchical Clustering)](/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/)
**다음**: [360. GMM (Gaussian Mixture Model) 과 EM 알고리즘](/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) ->

---
