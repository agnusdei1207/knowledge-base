+++
title = "106. 텍스트 마이닝 (Text Mining) — TF-IDF/Word2Vec/BERT 기반 텍스트 분석"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 텍스트 마이닝 (Text Mining)은 비정형 텍스트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정형 특성 벡터로 변환한 뒤, 통계·ML·딥러닝 모델을 적용하여 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·군집·요약·[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 추출 등의 지식을 발굴하는 종합 분석 기법이다.
> 2. **가치**: [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) ([Term Frequency-Inverse Document Frequency](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/))가 단어 중요도를 측정하고, Word2Vec이 의미적 유사성을 포착하며, [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) ([Bidirectional Encoder Representations from Transformers](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))가 문맥을 통합적으로 이해함으로써, 단계별로 정교해지는 언어 표현이 가능해진다.
> 3. **판단 포인트**: 한국어 텍스트 마이닝에서 형태소 분석 품질이 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 변수이며, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 어휘(의료·법률·금융)는 일반 사전 기반 모델만으로는 한계가 있어 파인튜닝이 필수다.

---

## Ⅰ. 개요 및 필요성

전 세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 약 80%는 비정형 텍스트다. 이메일, 계약서, SNS 포스트, 고객 상담 기록, 뉴스 기사 등 인간의 언어는 컴퓨터가 바로 처리할 수 있는 구조화된 형태가 아니다. 텍스트 마이닝은 이 방대한 비정형 정보를 기계가 처리할 수 있는 수치 벡터로 변환하고, 의미 있는 패턴과 지식을 추출하는 기술이다.

빅데이터 분석에서 텍스트 마이닝의 중요성은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체의 성격에서 비롯된다. 수치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 "얼마나"를 말해준다면, 텍스트는 "왜, 어떻게, 어떤 맥락에서"를 말해준다. 두 가지를 결합해야 완전한 비즈니스 인사이트가 나온다.

- **📢 섹션 요약 비유**: 텍스트 마이닝은 수백만 권의 책을 읽고 핵심만 뽑아내는 초속독 전문가다. 사람이 한 평생 읽을 분량을 컴퓨터는 몇 분 안에 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+--------------------------------------------------------------------+
|                텍스트 마이닝 전체 파이프라인                        |
+--------------------------------------------------------------------+
|  [원시 텍스트] "오늘 배송은 늦었지만, 제품 품질은 기대 이상이에요"  |
|          |                                                          |
|          v                                                          |
|  [1단계: 전처리 (Preprocessing)]                                    |
|   형태소 분석 -> 품사 태깅 -> 불용어 제거 -> 정규화/소문자화           |
|   KoNLPy(Okt/Mecab) / NLTK / spaCy                                 |
|          |                                                          |
|          v                                                          |
|  [2단계: 특성 추출 (Feature Extraction)]                            |
|   +--------------+----------------+--------------------------+     |
|   |  Bag-of-Words|   TF-IDF       |  Word2Vec / BERT          |     |
|   |  단어 빈도   |  중요도 가중치 |  의미적 임베딩 벡터       |     |
|   +--------------+----------------+--------------------------+     |
|          |                                                          |
|          v                                                          |
|  [3단계: 분석 태스크]                                               |
|   +----------+----------+----------+----------+--------------+     |
|   |  분류    |  군집화  |  요약    |  NER     |  감성 분석   |     |
|   +----------+----------+----------+----------+--------------+     |
+--------------------------------------------------------------------+
```

### 텍스트 표현 방법 진화

| 방법 | 원리 | 특징 | 단점 |
|:---|:---|:---|:---|
| **Bag-of-Words** | 단어 출현 빈도 벡터 | 단순, 빠름 | 순서·의미 무시 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/">TF-IDF</a></strong> | 단어 빈도 × 역문서 빈도 | 희귀 단어 중요도 강조 | 의미적 유사성 미반영 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/">Word2Vec</a></strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 표현, 의미적 유사 단어가 가까운 벡터 | 유추 가능 (왕-남성+여성=여왕) | 동음이의어 구분 불가 |
| **FastText** | 서브워드 단위 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) | 신조어·오타에 강함 | Word2Vec보다 느림 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | 양방향 [트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/), [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) | 동음이의어·맥락 완벽 처리 | 추론 비용 높음 |

### [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 공식

```text
TF(t,d)  = 문서 d에서 단어 t의 출현 횟수 / 문서 d의 총 단어 수
IDF(t)   = log(전체 문서 수 / 단어 t를 포함하는 문서 수)
TF-IDF   = TF(t,d) × IDF(t)
```

- **📢 섹션 요약 비유**: TF-IDF는 "자주 나오지만 흔한 단어는 중요하지 않고, 드물지만 이 문서에서만 자주 나오는 단어가 핵심"이라는 원리다. "의" "는"은 모든 문서에 있으니 중요하지 않고, "항생제 내성"은 의학 문서에서만 자주 나오니 중요하다.

---

## Ⅲ. 비교 및 연결

| 항목 | 전통 NLP ([TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) + ML) | 딥러닝 NLP ([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)) |
|:---|:---|:---|
| <strong>학습 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 소규모 가능 | 대규모 레이블 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 또는 파인튜닝 |
| **계산 비용** | 낮음 | 높음 ([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 필요) |
| **해석 가능성** | 높음 (특성 중요도 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 가능) | 낮음 (블랙박스) |
| **맥락 이해** | 제한적 | 우수 (양방향 어텐션) |
| **최적 사용처** | 빠른 프로토타이핑, 소규모 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 고정밀 요구, 대규모 텍스트 |

한국어 텍스트 마이닝 도구 생태계:
- **KoNLPy**: Okt (Open Korean Text), Komoran, Mecab 등 래핑
- <strong>KoBERT / klue-<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">bert</a></strong>: 한국어 사전학습 [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 모델
- **kiwipiepy**: 경량화 한국어 형태소 분석기

- **📢 섹션 요약 비유**: 전통 NLP는 잘 훈련된 사전 편찬자가 단어를 세는 방식이고, BERT는 책을 전부 읽고 문맥으로 의미를 이해하는 방식이다. 사전 편찬자가 빠르지만 "배가 아프다"와 "배를 먹는다"의 '배'를 구분하지 못한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. <strong>법률 문서 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>: 수십만 건의 판결문을 [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) + SVM으로 판례 유형 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)
2. **고객 상담 자동화**: [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 기반 의도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)로 챗봇 정확도 향상
3. **특허 분석**: [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) 기반 유사 특허 클러스터링으로 기술 트렌드 파악
4. **뉴스 분석**: 기사 [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 벡터로 주제 클러스터링 후 실시간 이슈 트래킹

### 기술사 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 전처리 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 불용어 목록이 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 맞게 [커스터마이즈](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/)됐는가?
2. 형태소 분석 도구 선택 시 처리 속도와 정확도 트레이드오프를 고려했는가?
   - Mecab: 빠름, 사전 의존 / Okt: 느리지만 사전 없이도 처리 가능
3. [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 사용 시 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 파인튜닝 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 충분한가? (최소 수천~수만 건)
4. 대용량 텍스트의 경우 Spark NLP를 활용한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리를 고려했는가?

- **📢 섹션 요약 비유**: 텍스트 마이닝 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 요리 레시피와 같다. 재료(전처리) -> 조리법(특성 추출) -> 요리(모델 적용)의 순서가 중요하고, 어떤 단계도 건너뛸 수 없다. 재료가 나쁘면 아무리 좋은 요리사도 맛있는 음식을 만들 수 없다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 활용 | 기존 수치 분석이 놓친 80% 텍스트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 인사이트 추출 |
| 업무 자동화 | 문서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 요약, 정보 추출 자동화로 인력 비용 절감 |
| 의사결정 지원 | VoC (Voice of [C고객](/knowledge-base/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/)), 뉴스, SNS 종합 인사이트 대시보드 |
| 지식 발굴 | 수백만 건 문서에서 사람이 발견하지 못한 패턴과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 자동 추출 |
| 실시간 처리 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Spark Streaming으로 실시간 텍스트 스트림 분석 |

텍스트 마이닝은 단순 키워드 추출에서 시작하여 의미 이해, 맥락 추론으로 진화해왔다. BERT와 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 같은 대형 언어 모델이 등장하면서 텍스트의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·요약·번역·질의응답이 실용 수준에 도달했다. 이제 텍스트 마이닝의 핵심 과제는 모델 자체가 아니라, 정확하고 편향 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구축과 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식을 모델에 효과적으로 주입하는 것으로 이동하고 있다.

- **📢 섹션 요약 비유**: 텍스트 마이닝은 언어의 산을 오르는 것이다. Bag-of-Words는 산 입구, TF-IDF는 중턱, Word2Vec은 7부 능선, BERT는 정상 부근이다. 어디까지 오를지는 해결하려는 문제의 난이도와 가용 자원에 달려 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| NLP (Natural Language Processing) | 텍스트 마이닝의 기반 기술 |
| [TF-IDF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) ([Term Frequency-Inverse Document Frequency](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/)) | 단어 중요도 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 계산 |
| [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) | 의미적 단어 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) ([Bidirectional Encoder Representations from Transformers](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)) | [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 최신 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| KoNLPy / Mecab | 한국어 형태소 분석 도구 |
| [감성 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/889_exploratory_data_analysis/) ([Sentiment Analysis](/knowledge-base/studynote/12_it_management/03_ea_isp/889_exploratory_data_analysis/)) | 텍스트 마이닝의 대표 응용 |
| [토픽 모델링](/knowledge-base/studynote/16_bigdata/05_analysis/116_topic_modeling/) ([Topic Modeling](/knowledge-base/studynote/16_bigdata/05_analysis/116_topic_modeling/)) | 문서 집합의 주제 발굴 응용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비정형 텍스트 (Unstructured Text) — 원시 자연어 데이터]
    |
    v
[전처리 (Preprocessing) — 토큰화·불용어 제거·정규화]
    |
    v
[TF-IDF / BoW — 텍스트 수치 벡터화]
    |
    v
[NLP (자연어 처리) — 형태소 분석·개체명 인식·감성 분석]
    |
    v
[워드 임베딩 (Word Embedding) — Word2Vec·GloVe 의미 벡터화]
    |
    v
[LLM 기반 텍스트 분석 — BERT·GPT 사전학습 모델 응용]
```
텍스트 마이닝은 규칙 기반 전처리에서 출발해 통계적 벡터화 -> 딥러닝 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) -> [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 분석으로 발전하며 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) 가치화의 핵심 기술이 되었다.

### 👶 어린이를 위한 3줄 비유 설명
- 텍스트 마이닝은 컴퓨터가 글을 읽고 "여기서 중요한 게 뭔지" 스스로 알아내는 거예요.
- TF-IDF는 "모든 글에 나오는 '은/이/가'보다, 이 글에서만 많이 나오는 특별한 단어가 중요하다"고 판단하는 방법이에요.
- BERT는 단어의 앞뒤 문맥까지 다 읽고 이해하는 아주 똑똑한 독서 로봇이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 109 / 262

<- **이전**: [105. 감성 분석 (Sentiment Analysis) — 긍부정 감정 자동 분류](/knowledge-base/studynote/16_bigdata/05_analysis/108_sentiment_analysis/)
**다음**: [107. 소셜 네트워크 분석 (SNA, Social Network Analysis) — 중심성/커뮤니티 탐지](/knowledge-base/studynote/16_bigdata/05_analysis/110_social_network_analysis/) ->

---
