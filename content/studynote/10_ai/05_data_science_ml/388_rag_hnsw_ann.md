---
title: "RAG HNSW ANN"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 388
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) ([Retrieval-Augmented Generation](/studynote/04_software_engineering/09_cloud_native_ai_architecture/585_rag_retrieval_augmented_generation/), [검색 증강 생성](/studynote/12_it_management/05_security_compliance/222_rag_retrieval_augmented_generation/))는 LLM의 파라미터 지식을 외부 벡터 DB에서 검색한 관련 문서로 보완하며, [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) ([Hierarchical Navigable Small World](/studynote/05_database/06_dw_olap_trends/352_rag/)) [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)가 대규모 벡터 [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) ([Approximate Nearest Neighbor](/studynote/05_database/06_dw_olap_trends/351_hnsw/)) 검색의 사실상 표준이다.
> 2. **가치**: HNSW는 계층적 소규모 세계 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 O(log n) 검색 복잡도를 달성하며, 정확도·속도·메모리 트레이드오프에서 우수한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보인다.
> 3. **판단 포인트**: [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) 품질은 청킹 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 모델 선택, [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) 파라미터(M, ef_construction, ef_search)의 조합으로 결정되며, Reranker 추가로 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 높인다.

---

## Ⅰ. 개요 및 필요성

LLM은 사전학습 컷오프 이후 지식이 없고, 길고 구체적인 내부 문서에 대한 질문에 취약하다. RAG는 질문과 관련된 외부 문서를 실시간 검색해 LLM의 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)에 주입함으로써 이 문제를 해결한다.

- <strong><a href="/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/">Hallucination</a> 감소</strong>: 실제 문서 근거 제공
- **지식 최신화**: DB 업데이트만으로 지식 갱신
- **비용 효율**: 재학습 없이 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 가능

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: RAG는 "오픈북 시험"이다. [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(학생)이 모든 걸 외우는 대신, 시험 중에 책(벡터 DB)을 찾아보고 답을 작성한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

```
+----------------------------------------------------------+
|  [Indexing 단계]                                         |
|  문서 -> 청킹(Chunking) -> 임베딩 모델 -> 벡터 DB (HNSW)   |
|                                                          |
|  [Retrieval + Generation 단계]                           |
|  사용자 질문 -> 임베딩 -> ANN 검색(HNSW) -> Top-K 문서     |
|             v                                            |
|  프롬프트 = [시스템] + [검색 문서] + [사용자 질문]        |
|             v                                            |
|  LLM -> 생성 답변                                         |
+----------------------------------------------------------+
```

### [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) ([Hierarchical Navigable Small World](/studynote/05_database/06_dw_olap_trends/352_rag/))

NSW (Navigable Small World): 소수의 장거리 연결 + 다수의 단거리 연결로 좁은 세상 현상 구현
[HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/): 계층적 구조로 탐색 시작점 최적화

```
레이어 3 (희소): ● ------------------ ●
레이어 2 (중간): ● --- ● ------- ● --- ●
레이어 1 (밀집): ● - ● - ● - ● - ● - ●
레이어 0 (전체): ● ● ● ● ● ● ● ● ● ● ●
                ^ 상위 레이어에서 시작해 하위로 내려가며 탐색
```

<strong><a href="/studynote/05_database/06_dw_olap_trends/351_hnsw/">HNSW</a> 주요 파라미터</strong>:

| 파라미터 | 의미 | 기본값 | 영향 |
|:---|:---|:---|:---|
| M | 각 노드의 최대 연결 수 | 16 | ^: 정확도^, 메모리^ |
| ef_construction | 인덱싱 시 탐색 후보 수 | 200 | ^: [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 품질^, 빌드 느림 |
| ef_search | 검색 시 탐색 후보 수 | 50 | ^: 정확도^, 검색 느림 |

<strong><a href="/studynote/05_database/06_dw_olap_trends/351_hnsw/">HNSW</a> 복잡도</strong>:
- 삽입: O(log n)
- 검색: O(log n) 평균

### 청킹 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (Chunking [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))

```
고정 크기: 512 토큰씩 분할 (단순, 컨텍스트 파괴 가능)
문장 기반: 문장 경계 존중 (의미 보존, 크기 가변)
재귀적 분할: 단락 -> 문장 -> 단어 순서로 분할
시맨틱 청킹: 임베딩 유사도 기반 의미 단위 분할
```

- **📢 섹션 요약 비유**: HNSW는 "지도의 축척"처럼 계층을 나눠 큰 그림에서 시작해 점점 세밀한 위치로 찾아가는 지능적 내비게이션이다.

---

## Ⅲ. 비교 및 연결

| [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 복잡도 | 메모리 | 정확도 | 업데이트 |
|:---|:---|:---|:---|:---|
| 완전 탐색 | O(nd) | 낮음 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0% | 쉬움 |
| IVF (Inverted [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | O(√n·d) | 중간 | 높음 | 어려움 |
| [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) | O(log n) | 높음 | 매우 높음 | 어려움 |
| FAISS (Flat) | O(nd) | 낮음 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0% | 쉬움 |
| ScaNN | O(log n) | 중간 | 높음 | 중간 |

**주요 벡터 DB**: Chroma, Pinecone, Weaviate, [Milvus](/studynote/07_enterprise_systems/05_data_bi/320_gnn_vector_db_recommendation/), Qdrant (대부분 [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) 지원)

- **📢 섹션 요약 비유**: [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택은 "지도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)"와 같다. 완전 탐색은 전국 도보 여행, HNSW는 고속도로 내비게이션이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Reranker 추가**: BM25 + 벡터 검색 하이브리드 -> Cross-[Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) Reranker로 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 향상
**청크 크기**: 128~512 토큰 ([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 창 크기 고려)
<strong><a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> 모델</strong>: text-[embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)-ada-002, BGE, E5 등 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)별 선택

기술사 포인트: [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) [파이프라인 단계](/studynote/01_computer_architecture/05_control_unit_pipelining/219_pipeline_stages/)(인덱싱->검색->[생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)), [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) 계층 구조, [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) vs 완전 탐색 트레이드오프를 도식으로 설명.

- **📢 섹션 요약 비유**: Reranker는 "Google 검색 결과 1위가 항상 최선이 아니라 1위~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)위를 모두 읽고 가장 적합한 것을 다시 고르는" 정밀 필터링이다.

---

## Ⅴ. 기대효과 및 결론

[RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) + [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) 조합은 LLM의 [환각](/studynote/06_ict_convergence/04_ai_llm/275_react_framework/) 문제를 실용적으로 해결하는 현재 표준 아키텍처다. 기업 내 문서 Q&A, 법률·의료 전문 AI에서 재학습 없이 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식을 제공한다. HNSW의 O(log n) 검색 효율은 수억 개의 벡터에서도 밀리초 단위 검색을 가능하게 한다.

- **📢 섹션 요약 비유**: RAG는 AI에게 "기억력을 인터넷으로 확장"하는 것이다. 외울 수 없는 것은 빠르게 검색해서 답하면 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) | 검색 증강, 벡터 DB / [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 지식 확장 방법 |
| [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) | 계층 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), O(log n) / 벡터 [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) 검색 표준 |
| [ANN](/studynote/05_database/06_dw_olap_trends/350_ann/) | 근사 최근접 이웃 / 벡터 [유사도 검색](/studynote/05_database/06_dw_olap_trends/348_similarity_search/) |
| 청킹 | 문서 분할, [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) / 인덱싱 전처리 |
| Reranker | Cross-[Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/), [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) / 검색 결과 재정렬 |
| 벡터 DB | Pinecone, Chroma / [HNSW](/studynote/05_database/06_dw_olap_trends/351_hnsw/) 구현체 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [RAG 파이프라인 (RAG HNSW ANN)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. RAG는 "시험 중 책을 찾아보는 오픈북 시험"이야. AI가 모든 걸 외우는 대신 필요할 때 빠르게 검색해.
2. HNSW는 지도처럼 큰 그림(상위 레이어)에서 점점 자세한 곳(하위 레이어)으로 좁혀가며 가장 비슷한 답을 찾아.
3. Reranker는 검색 결과 1~10위를 다시 꼼꼼히 읽어서 "진짜 제일 좋은 답"을 다시 고르는 2차 심사야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 388 / 420

<- **이전**: [387. Top-K / Top-P (Nucleus Sampling)](/studynote/10_ai/05_data_science_ml/387_topk_topp_sampling/)
**다음**: [389. 지식 증류 소프트 타겟 (Soft Target)](/studynote/10_ai/05_data_science_ml/389_knowledge_distillation_soft_target/) ->

---
