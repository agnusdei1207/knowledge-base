+++
title = "518. TF-IDF, 코사인 유사도, 텍스트 마이닝 (TF-IDF Cosine Similarity Text Mining Word2Vec)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/)(Term Frequency-Inverse [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) Frequency)는 문서 내 단어 빈도를 전체 문서에서의 희귀도로 보정해 단어 중요도를 정량화 — BoW(Bag of Words)의 한계를 극복한 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 방식이다.
> 2. **가치**: Word2Vec은 단어를 조밀한 벡터(Dense Vector)로 표현해 의미적 유사성을 거리로 표현 — "왕 − 남자 + 여자 = 여왕" 같은 벡터 산술이 가능하다.
> 3. **판단 포인트**: 키워드 매칭은 [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/)(BM25), 의미 검색은 Dense Vector([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) — [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)([Retrieval-Augmented Generation](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/585_rag_retrieval_augmented_generation/)) 파이프라인에서는 [하이브리드 검색](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/)이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적.

---

## Ⅰ. 개요 및 필요성

텍스트를 컴퓨터가 처리하려면 수치화(Vectorization)가 필수다. BoW부터 BERT까지의 진화는 "단어 빈도 → 의미 → 문맥 이해"로의 발전 과정이다.

### 텍스트 표현 방법의 진화

| 세대 | 방법 | 장점 | 한계 |
|:---|:---|:---|:---|
| 1세대 | BoW (Bag of Words) | 단순, 빠름 | 순서 무시, 의미 없음 |
| 2세대 | [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) | 중요 단어 강조 | 의미적 유사성 없음 |
| 3세대 | [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/), [GloVe](/knowledge-base/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/) | 의미적 유사성 포착 | 문맥 독립(단일 벡터) |
| 4세대 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) | 문맥 의존적 표현 | 고비용, 느림 |

- **📢 섹션 요약 비유**: 텍스트 표현의 발전은 단어 사전에서 단어 지도로의 진화야. 처음엔 단어가 있는지 없는지만 봤지만(BoW), 이제는 단어들이 얼마나 가까운지([Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/))를 지도처럼 그릴 수 있어.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 계산 구조

```
문서 컬렉션 (D개 문서)
        │
        ▼
TF(t,d) = 단어 t가 문서 d에 나타난 횟수 / 문서 d의 전체 단어 수
        │
IDF(t) = log(D / df(t))     df(t) = 단어 t를 포함한 문서 수
        │
        ▼
TF-IDF(t,d) = TF(t,d) × IDF(t)
        │
높은 TF-IDF ──→ 이 문서에 자주 나타나면서
                전체 문서에서는 희귀한 단어
```

### [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) ([Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))

$$\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{|\vec{A}||\vec{B}|}$$

- 두 벡터의 내적을 각 벡터의 크기로 나눔 → 범위 [-1, 1].
- 문서 길이에 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)없이 방향(의미)만 비교 — 유클리드 거리보다 텍스트에 적합.

| 유사도 값 | 의미 |
|:---|:---|
| 1.0 | 완전히 같은 방향 (동일 의미) |
| 0.0 | 직교 (의미 무관) |
| -1.0 | 반대 방향 (반의어적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)) |

- **📢 섹션 요약 비유**: [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 두 사람이 같은 방향을 바라보는지 확인하는 것과 같아. 키가 달라도(문서 길이 다름) 같은 방향을 보면 유사한 내용의 문서야.

---

## Ⅲ. 비교 및 연결

### 희소 벡터 vs 조밀 벡터

| 구분 | [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) (희소, Sparse) | [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) (조밀, Dense) |
|:---|:---|:---|
| 벡터 차원 | 어휘 크기 (수만~수십만) | 고정 (100~1000) |
| 대부분 값 | 0 | 실수 값 |
| 의미 포착 | 불가 | 가능 |
| 계산 속도 | 빠름 | 상대적으로 느림 |
| 활용 | 키워드 검색, BM25 | 의미 검색, 추천 |

### [하이브리드 검색](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/) ([Hybrid Search](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/)) — [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 활용

```
쿼리 입력
    │
    ├─ BM25 검색 (키워드 매칭) ──┐
    │                            ├─ RRF 융합 → 최종 문서 순위
    └─ Dense Vector 검색         │
       (의미 유사도)  ────────────┘
```

**RRF(Reciprocal Rank Fusion)**: 두 검색 결과의 순위를 결합하는 [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 방법.

### [토큰화](/knowledge-base/studynote/09_security/16_data_privacy/820_tokenization/) ([Tokenization](/knowledge-base/studynote/09_security/16_data_privacy/820_tokenization/)) 방법

- <strong>BPE (<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/378_bpe_byte_pair_encoding/">Byte Pair Encoding</a>)</strong>: 빈번한 문자 쌍을 반복 합병 → [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 계열 사용.
- **WordPiece**: BPE 변형, 하위 단어(Subword) 어휘 학습 → [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 사용.
- **Unigram LM**: [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 기반 최적 분할 → SentencePiece.

- **📢 섹션 요약 비유**: BM25는 "이 책에 '파이썬'이라는 단어가 많이 나와"라고 검색하는 도서관 사서이고, Dense Vector는 "파이썬이라는 단어는 없지만 내용이 프로그래밍에 관한 책이야"라는 것을 이해하는 스마트 사서야.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시나리오 1 - 고객 리뷰 분석**:
- 10만 건 리뷰 [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 벡터화 → [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)로 유사 리뷰 클러스터링.
- 상위 키워드: "배송 빠름"([TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 0.82), "포장 불량"(0.71) → 운영 개선 우선순위 결정.

<strong>시나리오 2 - 사내 문서 검색 시스템 (<a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/">RAG</a>)</strong>:
- BM25: 정확한 제품명 검색에 강점.
- Dense Vector ([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)): "비용 절감 방법"처럼 의미 기반 질의에 강점.
- 하이브리드: NDCG@[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 기준 BM25=0.62, Dense=0.71, 하이브리드=0.79.

**기술사 판단 포인트**:
- [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/): 일반 BERT보다 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 파인튜닝([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) 모델이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 20~30% 향상.
- [벡터 데이터베이스](/knowledge-base/studynote/12_it_management/05_security_compliance/223_vector_database_embedding/): Faiss, Pinecone, Weaviate — [HNSW](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)(Hierarchical Navigable Small World) 인덱스로 [ANN](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/)([Approximate Nearest Neighbor](/knowledge-base/studynote/05_database/06_dw_olap_trends/351_hnsw/)) 검색.
- 한국어 처리: 형태소 분석(Mecab, Kiwi) 후 [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 적용 필수.

- **📢 섹션 요약 비유**: TF-IDF는 레시피에서 자주 나오는 특별한 재료를 찾아주는 것이고, Word2Vec은 "닭고기"와 "쇠고기"가 비슷한 카테고리라는 것을 스스로 배우는 것처럼, 단어 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이해해.

---

## Ⅴ. 기대효과 및 결론

[텍스트 마이닝](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/) 기술의 계층적 이해는 키워드 기반 검색부터 의미 기반 [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 시스템 설계까지 실무 전 과정에 활용된다.

- **검색 품질 향상**: [하이브리드 검색](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/)으로 키워드 검색과 의미 검색의 상호 보완.
- <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/">비정형 데이터</a> 활용</strong>: 리뷰·CS [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·계약서를 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·요약·검색.
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> 파이프라인 최적화</strong>: RAG에서 고품질 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 검색이 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 응답 품질 결정.

- **📢 섹션 요약 비유**: [텍스트 마이닝](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/)은 도서관을 AI에게 주는 것과 같아. TF-IDF는 책에 어떤 단어가 많은지 세고, Word2Vec은 책 내용의 의미를 이해하고, BERT는 문장 전체 문맥을 파악해서 진짜 도서관 사서처럼 도움을 줘.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) | BoW, BM25, 키워드 검색 · 문서 검색, 요약 |
| [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) | 벡터 공간 모델, 추천 · 문서 유사도 |
| [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) | [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/), [GloVe](/knowledge-base/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/) · 의미 분석 |
| [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 문맥 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/), [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) · NLU, [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) |
| [하이브리드 검색](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/279_rlhf_reinforcement_learning_human_feedback/) | BM25+Dense, RRF · [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 파이프라인 |

### 📈 관련 키워드 및 발전 흐름도

```text
[BoW · BM25] → [TF-IDF · 코사인 유사도] → [BM25+Dense · RRF]
```

### 👶 어린이를 위한 3줄 비유 설명

1. TF-IDF는 책에서 자주 나오는 특별한 단어가 무엇인지 찾아주는 거야 — "바나나"가 과일 책에만 자주 나오면 그게 그 책의 핵심 단어야.
2. [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 두 문서가 같은 방향을 바라보는지 확인하는 거야 — 방향이 같으면 비슷한 내용이야.
3. Word2Vec은 단어들을 지도 위에 올려놓는 거야 — 비슷한 뜻의 단어들은 지도에서 가까이 모여 있어!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 518 / 552

← **이전**: [517. 시계열 ARIMA 정상성과 평활법 (Time Series ARIMA Stationarity Smoothing)](/knowledge-base/studynote/06_ict_convergence/05_data_science/517_time_series_arima_stationarity_smoothing/)
**다음**: [519. 협업 필터링, 콜드 스타트, 추천 시스템 (Collaborative Filtering Cold Start Recommendation)](/knowledge-base/studynote/06_ict_convergence/05_data_science/519_collaborative_filtering_cold_start_recommendation/) →

---
