+++
title = "296. RAG 아키텍처 검색 증강 생성 파이프라인 (RAG Architecture Retrieval Augmented Generation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RAG(Retrieval-Augmented Generation)는 LLM의 추론 능력과 외부 Knowledge Base의 사실성을 결합한 2-Stage 아키텍처로, Query Embedding -> Vector/Sparse Retrieval -> Re-ranking -> Prompt Augmentation -> LLM Generation 파이프라인을 통해 Hallucination을 구조적으로 억제한다.
> 2. **가치**: 동일 도메인 Fine-tuning 대비 학습 비용 1/10 이하, 최신 정보 반영(Real-time Updates), 출처 추적(Provenance) 가능, 도메인 적응(Domain Adaptation) 속도 10x 향상, 정확도 30~70% 개선(HotpotQA·Natural Questions 기준 RAGAS 평가).
> 3. **판단 포인트**: Chunk Size(128~1024 token)·Overlap 비율(10~20%)·Embedding 모델 선택(BGE-M3 vs OpenAI text-embedding-3-large)·Vector Index 알고리즘(HNSW vs IVF)·Hybrid Search 가중치(α·β)·Re-ranker 도입 여부·Cache 전략·Multi-modal 확장성 사이의 트레이드오프가 성능과 비용을 결정한다.

---

## Ⅰ. 개요 및 필요성

LLM(대규모 언어 모델)은 2020년 GPT-3 이후 1조 토큰 규모의 파라미터 학습으로 일반 상식·추론 능력을 획득했으나, **Knowledge Cutoff 문제**(2023년 10월 이전 데이터만 학습), **환각(Hallucination)**, **사적/기업 내부 문서 미학습**, **사실 검증 불가**라는 4대 구조적 한계를 갖는다. 기존에는 이를 해결하기 위해 Fine-tuning(PEFT, LoRA, QLoRA)이나 Prompt Engineering(Chain-of-Thought, ReAct)만 사용했으나, Fine-tuning은 ① 수억 원의 GPU 비용, ② 수 주간의 학습 시간, ③ 업데이트 시 재학습 필요라는 비효율을, Prompt Engineering은 ① Context Window 한계(8K~200K token), ② 비사실성 통제 불가라는 한계를 내포했다.

**RAG(Retrieval-Augmented Generation)**는 2020년 Meta AI의 Patrick Lewis 등이 발표한 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" 논문에서 처음 체계화되었으며, **"외부 검색(Non-parametric memory)으로 LLM의 parametric memory를 보강한다"**는 핵심 아이디어로 출발했다. 현재는 Naive RAG -> Advanced RAG -> Modular RAG -> Agentic RAG -> GraphRAG로 진화하며, NVIDIA, Microsoft, AWS, Naver, LG AI Research 등이 모두 표준 아키텍처로 채택하고 있다.

```text
+--------------------------------------------------------------------+
|            LLM의 4대 한계와 RAG가 해결하는 영역                       |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------------------+         +----------------------+         |
|  |  LLM Only (Parametric)|        |  RAG (Hybrid Memory) |         |
|  |  +----------------+   |         |  +----------------+  |         |
|  |  |  Pre-trained   |   |         |  |  Pre-trained   |  |         |
|  |  |  Knowledge     |   |  ---►   |  |  Knowledge     |  |         |
|  |  |  (Static)      |   |  보강   |  |  (Dynamic)     |  |         |
|  |  +----------------+   |         |  +----------------+  |         |
|  |  + 추론 능력          |         |  + 추론 능력          |         |
|  +----------------------+         |  + 외부 검색 결과      |         |
|                                   |  + 출처 인용           |         |
|  ✗ Knowledge Cutoff              |  + 실시간 업데이트      |         |
|  ✗ Hallucination 30%+           +----------------------+         |
|  ✗ 비공개 문서 미학습             ✓ Real-time Knowledge             |
|  ✗ 출처 추적 불가                ✓ Provenance & Citation            |
|                                   ✓ Hallucination 70%v             |
+--------------------------------------------------------------------+
```

기존 Fine-tuning 방식과 대비되는 RAG의 패러다임 전환은 **"학습(Learning)이 아니라 조회(Lookup)"**라는 점에 있다. 즉, 모델 파라미터를 변경하지 않고도(Read-only Weight) Context Window에 사실 정보를 주입함으로써, **데이터 업데이트가 분 단위로 가능**하며 **데이터 양에 비례한 선형 비용**만 발생한다. 2023년 Gartner 보고서에 따르면, 2026년 기업용 Generative AI 솔루션의 60% 이상이 RAG 아키텍처를 채택할 것으로 예측되며, 이미 PwC, 마이크로소프트 365 Copilot, Samsung Gauss Portal 등이 RAG-first 전략을 채택했다.

- **📢 섹션 요약 비유**: LLM이 "암기만 한 박사"라면, RAG는 "인터넷 검색 + 암기를 병행하는 사서 박사"이다. 박사의 두뇌(LLM)는 그대로지만, 매 질문마다 도서관(Vector DB)에서 최신 도서를 빌려 책상(Context Window)에 올려놓고 답변을 쓰는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RAG 파이프라인은 크게 **Ingestion(색인) 단계**와 **Inference(추론) 단계**로 나뉘며, 각 단계는 다시 5~7개의 세부 모듈로 구성된다. Naive RAG가 가장 단순한 형태이고, Advanced RAG는 여기에 Query Optimization, Re-ranking, Re-ranking 후 Prompt Engineering이 추가된다. Modular RAG(2024~)는 각 모듈을 독립적으로 조합 가능하도록 분리한 아키텍처다.

```text
-----------------------------------------------------------------------
  ① Ingestion Pipeline (Offline Indexing)
-----------------------------------------------------------------------

  [Source Docs]   [Load]    [Transform]   [Split]      [Embed]      [Store]
  +---------+    +------+  +----------+  +--------+  +--------+  +--------+
  | PDF     |---►|PyPDF |-►|Clean/Nor |-►|Chunker |-►|BGE-M3  |-►|Pinecone|
  | DOCX    |    |Unstru|  |malize    |  |512 tok |  |1024-d  |  |  Index |
  | HWP     |    |LlamaP|  |LangDetect|  |overlap |  |float32 |  |        |
  | HTML    |    |arse  |  |Dedup     |  |50 tok  |  |        |  |        |
  | DB/SQL  |    +------+  +----------+  +--------+  +--------+  +--------+
  | Confluence|
  | Slack    |              Metadata: source, page, timestamp, author
  +---------+
       |
       v
  +------------------------------------------------------+
  |  Vector Store Index (HNSW / IVF / ScaNN / PQ)        |
  |  + BM25 Sparse Index (Elasticsearch / OpenSearch)    |
  |  + Metadata Filter Index (Author, Date, ACL)         |
  +------------------------------------------------------+

-----------------------------------------------------------------------
  ② Inference Pipeline (Online Retrieval + Generation)
-----------------------------------------------------------------------

   User Query
       |
       v
  +----------+  +----------+  +------------------+
  |Query     |-►|Query     |-►|Hybrid Retrieval  |
  |Rewrite   |  |Embedding |  |(Dense + Sparse)  |
  |(HyDE/    |  |(BGE-M3)  |  |Top-K = 50        |
  |Multi-Q)  |  +----------+  +--------+---------+
  +----------+                        |
                                      v
                            +------------------+
                            | Re-ranker        |
                            |(Cross-Encoder /  |
                            | Cohere Rerank-3  |
                            | Top-N = 5)       |
                            +--------+---------+
                                     |
                                     v
                            +------------------+
                            |Context           |
                            |Compression       |
                            |(Lost-in-Middle   |
                            | mitigation)      |
                            +--------+---------+
                                     |
                                     v
                            +------------------+
                            |Prompt Assembly   |
                            |{System, Context, |
                            | History, Query}  |
                            +--------+---------+
                                     |
                                     v
                            +------------------+
                            | LLM Generation   |
                            | (GPT-4o, Claude  |
                            |  3.5, Llama-3.1) |
                            +--------+---------+
                                     |
                                     v
                              [Final Answer +
                               Citation Sources]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Document Loader** | 비정형·정형 데이터 수집 | PyPDF, pdfplumber, Unstructured.io, LlamaParse(테이블 인식), Apache Tika, Confluence REST API, SQLAlchemy. HWP/PPTX는 `olefile`, `python-pptx`로 파싱. |
| **Chunker (Splitter)** | 토큰 단위 분할 | RecursiveCharacterTextSplitter(권장), SemanticChunker(임베딩 유사도 기반), Sliding Window(512 token + 50 overlap). 한국어는 Kiwi, Mecab 형태소 분석기 활용 시 경계 정확도 15%^. |
| **Embedding Model** | 텍스트 -> 고차원 벡터 | BGE-M3(다국어, 1024-d), OpenAI text-embedding-3-large(3072-d, Matryoshka 지원), E5-Large, KoSimCSE-roberta(한국어 특화), Cohere embed-v3. MTEB Benchmark score 60+ 권장. |
| **Vector Database** | ANN(Approximate Nearest Neighbor) 검색 | Pinecone(Managed), Weaviate(Open-source), Milvus(10억+ 벡터), Qdrant(Rust 기반, 1ms 미만), Chroma(프로토타입용), PGVector(PostgreSQL 통합). 인덱스: HNSW(M=16, efConstruction=200), IVF-PQ(메모리 95%v), ScaNN(Google). |
| **Retriever** | Top-K 후보 추출 | Dense Retrieval(cosine similarity), Sparse Retrieval(BM25, SPLADE), Hybrid Search(Reciprocal Rank Fusion, α=0.7~0.8 가중치). Multi-Query Retriever(LLM으로 5개 변형 생성), HyDE(Hypothetical Document Embedding). |
| **Re-ranker** | 정밀 재순위 | Cross-Encoder(ms-marco-MiniLM, BGE-reranker-v2-m3, 100~500ms), Cohere Rerank-3, ColBERT(토큰 단위 Late Interaction), LLM-based Reranker(GPT-4 점수화, 비용^). |
| **LLM Generator** | 최종 답변 생성 | GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama-3.1-405B, HyperCLOVA X. Context Window 128K+ 필수. Temperature 0.0~0.3 권장(factuality 위해). |

### 핵심 알고리즘 및 파라미터

**1. Chunk Size와 Overlap**
$$C_{opt} = \arg\min_{c} \left( \alpha \cdot \text{Lost}_{ctx}(c) + \beta \cdot \text{Noise}_{ctx}(c) + \gamma \cdot \text{IndexSize}(c) \right)$$
- 너무 작으면(Sentence-level) 문맥 손실, 너무 크면(>1024) LLM이 핵심을 놓치고 Index 비대화. **256~512 token, overlap 10~20%**가 일반적 sweet spot.
- 최신 기법: **Parent Document Retriever**(작은 chunk로 검색 후 상위 Parent Window 반환), **Auto-Merging Retriever**(Hierarchical).

**2. Hybrid Search 가중치 (RRF)**
$$RRF_{score}(d) = \sum_{r \in R} \frac{1}{k + r(d)}$$ where $k = 60$ (default).
Dense α와 Sparse β의 가중 평균: $final\_score = \alpha \cdot sim_{dense} + \beta \cdot sim_{sparse}$, 일반적으로 **α=0.7, β=0.3**.

**3. Similarity 메트릭**
- **Cosine Similarity**: $\frac{A \cdot B}{||A|| \cdot ||B||}$ (정규화 후, OpenAI·BGE 기본)
- **Dot Product**: $A \cdot B$ (정규화 안 된 벡터, Faiss 기본)
- **Euclidean (L2)**: $\sqrt{\sum(A_i - B_i)^2}$ (Scale-sensitive)

**4. HNSW (Hierarchical Navigable Small World)**
- Multi-layer Graph 구조, Search Complexity $O(\log N)$. Parameter: `M=16~64`, `efConstruction=128~512`, `efSearch=50~200`. Recall@10 95%+ @ 1ms.

- **📢 섹션 요약 비유**: RAG 파이프라인은 "도서관의 사서 시스템"이다. 책(Document)이 들어오면 ① 색인 카드(Chunk)로 자르고, ② 주제별 번호(Embedding)를 붙여, ③ 서가(Vector DB)에 정리한다. 손님이 질문하면 사서가 ④ 관련 카드 50장(Retriever)을 뽑고, ⑤ 전문가가 다시 5장(Re-ranker)을 추리고, ⑥ 박사(LLM)가 책을 읽고 답한다.

---

## Ⅲ. 비교 및 연결

RAG는 단독 기술이 아니라, LLM의 한계를 보완하는 **인접 기술군**과 명확히 구분·결합된다. 특히 **Fine-tuning**, **Long Context LLM**, **Tool-use Agent**와의 관계는 기술사 시험에서 빈번히 비교된다.

| 구분 | **Naive RAG** | **Fine-tuning (LoRA)** | **Long Context LLM** | **Agentic RAG** |
| :--- | :--- | :--- | :--- | :--- |
| **지식 업데이트 방식** | 외부 DB 재색인 (분 단위) | 가중치 재학습 (수 일) | Context 주입 (실시간) | Tool 호출 (실시간) |
| **비용 (100GB 데이터)** | $500~$2K (임베딩) | $50K~$500K (GPU) | $0 (Token 비용만) | $1K~$10K (Tool) |
| **할루시네이션 감소율** | 30~50% | 20~40% | 10~30% | 50~70% |
| **출처 추적 (Provenance)** | ✅ 가능 (인용) | ❌ 불가 (암기) | ⚠️ 부분 가능 | ✅ 가능 |
| **추론 능력 향상** | △ 보통 | ✅ 강함 (스타일 학습) | △ 보통 | ✅ 강함 (Multi-step) |
| **적합 시나리오** | 팩트 조회, Q&A, 검색 | 톤·스타일·포맷 학습 | 단일 문서 분석 | 복합 추론, Workflow |
| **한
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 296 / 300

<- **이전**: [295. LLMOps 대규모 언어 모델 운영 관리 (LLMOps Large Language Model Operations)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/295_llmops/)
**다음**: [297. 프롬프트 엔지니어링 인컨텍스트 학습 전략 (Prompt Engineering In-Context Learning)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/297_prompt_engineering/) ->

---
