+++
title = "268. 벡터 데이터베이스 임베딩 유사도 검색 (Vector Database Embedding Similarity Search)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 고차원 임베딩 벡터(보통 384~4096차원) 상에서 **HNSW, IVF-PQ, ScaNN** 등 ANN(Approximate Nearest Neighbor) 인덱스 구조와 **코사인 유사도 / 내적 / L2 거리** 같은 메트릭을 결합해, k-NN의 정확도를 95~99% 수준으로 유지하면서 **O(log N) ~ O(√N)** 복잡도로 Top-K 유사 벡트를 검색하는 기법이다.
> 2. **가치**: RAG(Retrieval-Augmented Generation)·시맨틱 검색·추천·이상탐지·이미지·오디오·코드 검색 등에서 BM25/TF-IDF 대비 **재현율(Recall@10)을 30~60% 향상**시키고, LLM의 환각(Hallucination)을 컨텍스트 주입으로 억제하며, p99 latency 20~100ms 내 수십억 벡터 검색을 가능케 한다.
> 3. **판단 포인트**: 인덱스 알고리즘(HNSW vs IVF-PQ vs ScaNN), 양자화(SQ/PQ/BQ/RQ), 하이브리드 검색(BM25 + Dense), 메타데이터 필터 전략(pre-filter vs post-filter), 임베딩 모델 선택(다국어·도메인 특화), GPU 가속 여부, 샤딩·복제 정책이 **정확도-지연시간-메모리-CAPEX** 트레이드오프를 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적인 RDBMS의 B-Tree 인덱스나 Elasticsearch의 **BM25 역문서빈도(Inverted Index)** 기반 검색은 **정확한 토큰 일치(Exact Match)** 나 통계적 어휘 유사성에 의존한다. 그러나 `"노트북 과열"` 이라는 쿼리에 `"발열이 심한 랩탑"` 같은 표현이 등장하면 BM25는 recall이 0에 수렴한다. 또한 LLM·비전 모델이 산출하는 **의미론적 임베딩(Semantic Embedding)** 은 "king" − "man" + "woman" ≈ "queen" 같은 **선형 관계성(Linear Relationality)** 을 내포하므로, 키워드 매칭만으로는 활용이 불가능하다.

벡터 데이터베이스는 **고정 차원의 실수 벡터(Floating-Point Vector)** 를 1차 ID로 인덱싱하고, **HNSW(Hierarchical Navigable Small World)** 그래프나 **IVF(Inverted File) + PQ(Product Quantization)** 같은 근사 인덱스로 ANN 검색을 수행한다. 이로써 (1) 의미 기반 검색, (2) 멀티모달 통합 검색(텍스트↔이미지↔오디오), (3) Few-Shot / Zero-Shot LLM의 외부 지식 주입이 가능해졌다.

```text
[ BM25 시대 ]                            [ Vector Search 시대 ]
                                       +--------------+
쿼리: "노트북 과열" -+                  | Embedding    |
키워드 매칭: ❌ 실패 |                  | Model(BGE-M3)|
                      v                 +------+-------+
                  Recall 0%                     | 1024-dim float32
                                                v
                                       +----------------------+
                                       |  Vector Database    |
                                       |  +------+ +------+  |
                                       |  | HNSW | | IVF  |  |
                                       |  |Layer0| | Coarse|  |
                                       |  |Layer1| |Cluster|  |
                                       |  |Layer2| |  PQ  |  |
                                       |  +------+ +------+  |
                                       +----------+-----------+
                                                  v
                                       Top-K: ["발열 랩탑", "쿨링 패드", ...]
                                                  |
                                                  v
                                       Recall@10 ≈ 87%
```

| 비교 차원 | BM25 / RDBMS | 벡터 유사도 검색 |
| :--- | :--- | :--- |
| 검색 패러다임 | Lexical (어휘 일치) | Semantic (의미 공간) |
| 유사어·동의어 | 처리 불가 | 임베딩 공간에서 자연 처리 |
| 다국어·교차모달 | 불가 | Cross-lingual / Cross-modal 가능 |
| 인덱스 비용 | 낮음, 디스크 친화 | RAM 의존 (HNSW), 디스크 가능 (DiskANN) |
| Latency | 5~30ms | 10~100ms (ANN) |
| Recall@10 | 0.4~0.6 (긴 쿼리) | 0.85~0.97 |

- **📢 섹션 요약 비유**: BM25는 **백과사전 색인**으로 "Apple"이라는 단어가 정확히 적힌 페이지만 찾지만, 벡터 검색은 **천체 지도** 위에서 "Apple"이라는 별과 가장 가까운 별자리(🍎 회사, 🍎 과일, Newton 사과)를 모두 안내한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 임베딩 생성 파이프라인

```text
원본 데이터 (텍스트/이미지/오디오/코드)
    |
    | 1) Chunking (512~1024 tokens, overlap 10~20%)
    v
Tokenization (BPE, WordPiece, SentencePiece)
    |
    | 2) Transformer Encoder
    v
Hidden States (B × L × D) --[Mean/Max/CLS Pooling]---> 임베딩 벡터 (D,)
    |
    | 3) L2 Normalize (cosine 사용 시)
    v
Vector Index에 저장 (id -> vector, metadata, payload)
```

| 단계 | 핵심 파라미터 | 대표 구현 |
| :--- | :--- | :--- |
| Chunking | chunk_size, overlap, splitter | LangChain RecursiveCharacterTextSplitter, LlamaIndex SentenceSplitter |
| Tokenization | vocab_size, max_len | BERT WordPiece, GPT BPE, LLaMA SentencePiece |
| Encoder | dim (384/768/1024/1536/3072), layers | BGE-M3 (1024), OpenAI text-embedding-3 (1536/3072), Cohere embed-v3, E5-mistral-7b |
| Pooling | mean, cls, last-token | Sentence-Transformers의 `mean_pooling` |
| Normalization | L2 norm = 1 | Cosine similarity = Dot product |

### 2. ANN 인덱스 알고리즘

```text
              +----------------------------------------------------------+
              |              Query Vector  q ∈ ℝᵈ                       |
              +--------------------+-------------------------------------+
                                   v
        +----------------------------------------------------------+
        |  [ Coarse Quantizer / Entry Point ]                     |
        |   - IVF: k-means centroid (nlist=4√N)                   |
        |   - HNSW: 최상위 Layer (M=16, efConstruction=200)        |
        +--------------+-------------------------------------------+
                       v
        +----------------------------------------------------------+
        |  [ Fine Search within Partition / Neighbors ]            |
        |   - IVF: probe nprobe=8~64 buckets                       |
        |   - HNSW: efSearch=100, greedy walk in graph             |
        +--------------+-------------------------------------------+
                       v
        +----------------------------------------------------------+
        |  [ Re-rank with Exact Distance (optional) ]              |
        |   - PQ 코드북 복원 후 FP32 거리 재계산                   |
        |   - Top-K selection                                      |
        +----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **HNSW (Hierarchical Navigable Small World)** | 그래프 기반 ANN | 각 노드가 `M0~2M0`개의 이웃을 가지는 다층 네비게이션 그래프. **O(log N)** 탐색, **Recall@10 ≥ 0.95** 가능. RAM 상주(50GB/100M 벡터/d=768), 갱신 친화적. |
| **IVF (Inverted File Index)** | 클러스터 기반 ANN | k-means로 nlist centroid 학습. `nprobe` 개 버킷만 훑어 검색. 메모리 효율적이나 nprobe^ 시 latency^. **Faiss IVF-Flat, IVF-PQ**가 표준. |
| **PQ (Product Quantization)** | 벡터 압축 | d차원 벡터를 m개 서브벡터로 분할 -> 각 서브벡터를 K=256 centroid로 **k-means 양자화**. 768d×4byte=3KB -> **48byte**로 64× 압축. |
| **OPQ (Optimized PQ)** | PQ 왜곡 보정 | 회전 행렬 R을 학습해 PQ 재현 오차 최소화. Recall 5~15% 향상. |
| **ScaNN (Google)** | 비대칭 거리 + 정수 양자화 | Anisotropic Vector Quantization으로 **Recall@1을 20~40%** 개선. TPU 최적화. |
| **DiskANN** | SSD 기반 ANN | Vamana 그래프 + PQ + SSD 캐싱. **RAM 1/100 수준** 으로 10억+ 벡터 운영. Azure Cognitive Search, Milvus 2.4+ 채택. |
| **LSH / Annoy** | 단순 해시/트리 | Random Projection 또는 Random Forest. 정확도 낮지만 학습 0초. Spotify Annoy가 대표. |

### 3. 유사도 메트릭

| 메트릭 | 수식 | 사용 시나리오 | 비고 |
| :--- | :--- | :--- | :--- |
| **Cosine Similarity** | $\frac{A \cdot B}{\|A\| \|B\|}$ | 텍스트 임베딩, 정규화된 벡터 | L2 normalize 후엔 dot product와 동치, **HNSW 라이브러리에서 기본 채택** |
| **Dot Product (IP)** | $A \cdot B$ | 길이 정보 보존, 추천시스템 | Faiss `IndexFlatIP`, Pinecone default |
| **Euclidean (L2)** | $\sqrt{\sum (a_i - b_i)^2}$ | 이미지, 좌표 데이터 | HNSW `space=l2` |
| **Hamming** | $\sum [a_i \neq b_i]$ | BQ(Binary Quantization) 벡터 | 64~256bit binary code, **메모리 32×v** |
| **Jaccard** | $\|A \cap B\| / \|A \cup B\|$ | Sparse 벡터(SPLADE, BM25) | Qdrant, Milvus sparse vector 지원 |

### 4. 하이브리드 검색과 필터링

```text
   Query
     |
     +---> Sparse Encoder (BM25 / SPLADE) ---> Sparse Vector -+
     |                                                       +---> Fusion ---> Reranker (Cross-Encoder) ---> Final Top-K
     +---> Dense Encoder (BGE-M3) -----------> Dense Vector  -+
                |
                +---> Metadata Filter (tenant_id, date_range, tag)
                       +- Pre-filter: 후보 축소 후 ANN (Recall 손실 가능)
                       +- Post-filter: ANN 후 조건부 제거 (Recall 보존)
```

- **Reciprocal Rank Fusion (RRF)**: $\text{score}(d) = \sum_{r \in R} \frac{1}{k + r(d)}$, k=60 기본.
- **Cross-Encoder Reranking**: Bi-Encoder로 100~1000개 1차 후보 -> MonoT5/ColBERT/Cross-Encoder로 정밀 재정렬, NDCG@10 10~25%^.

- **📢 섹션 요약 비유**: ANN은 **대형 서점의 "관련 서가" 안내**이고(빠르지만 근사), Cross-Encoder Rerank는 **사서가 직접 책을 펼쳐 비교**하는 단계(느리지만 정확). 두 단계가 합쳐져야 1초 안에 "진짜" 답을 찾는다.

---

## Ⅲ. 비교 및 연결

### 1. 벡터 데이터베이스 vs 전통 저장소

| 구분 | RDBMS (PostgreSQL+pgvector) | 전용 Vector DB (Milvus/Qdrant/Weaviate) | 검색엔진 (Elasticsearch kNN) |
| :--- | :--- | :--- | :--- |
| ANN 알고리즘 | HNSW, IVF-Flat | HNSW, IVF-PQ, DiskANN, ScaNN | HNSW |
| 최대 스케일 | 수백만 벡터 | 10억+ 벡터 | 수천만~1억 |
| 멀티 인덱스 | 단일 | **다중 (Dense + Sparse + BM25)** | BM25 + Dense |
| 메타데이터 | SQL 필터 (강함) | Payload 인덱스 / SQL-like | Nested aggregation |
| 트랜잭션/ACID | ✅ (Postgres) | △ (최종 일관성) | ❌ |
| 운영 복잡도 | 낮음 (기존 DB 활용) | 중~상 (별도 클러스터) | 중 (ES 스택) |
| 비용 | Open-source | Managed 시 비용^ | Managed 가능 |

### 2. 주요 벡터 DB 비교

| 제품 | 인덱스 | 특화점 | 라이선스 | RAG 통합 |
| :--- | :--- | :--- | :--- | :--- |
| **Milvus 2.4+** | HNSW, IVF-PQ, DiskANN, GPU CAGRA | 10억+ 스케일, 멀티테넌시, 스트리밍 | Apache 2.0 | Attu UI, SDK |
| **Qdrant 1.10+** | HNSW + Scalar Quantization | Rust 기반 고성능, payload 필터 강함 | Apache 2.0 | REST/gRPC |
| **Weaviate 1.24+** | HNSW + PQ | 모듈식 (vectorizer 모듈 내장) | BSD-3 | GraphQL |
| **Pinecone** | Proprietary (POD 아키텍처) | Serverless, 메타데이터 필터, namespace | SaaS | SDK 다국어 |
| **Chroma** | HNSW (DuckDB+Parquet) | 임베딩된 메타데이터, 로컬 친화 | Apache 2.0 | Pythonic |
| **pgvector** | HNSW, IVF-Flat | Postgres 확장, 운영 단순 | PostgreSQL | SQL 통합 |
| **Vespa** | HNSW + Streaming | 대용량 + Boolean 필터 + Ranking | Apache 2.0 | Query Profile |
| **LanceDB** | IVF-PQ (Lance 컬럼) | Embedded, Disk-based, OLAP-친화 | Apache 2.0 | DataFrame API |
| **Redis Vector** | HNSW (FLAT+HNSW) | In-memory, 초저지연 | SSPL/AGPL | Lua, Spring |

### 3. RAG·LLM·Knowledge Graph와의 연결

| 연계 시스템 | 연결 방식 | 실무 효과 |
| :--- | :--- | :--- |
| **LLM (GPT-4o, Claude, Llama 3.1)** | Retriever -> Prompt Context | 환각률 30~70%v |
| **Knowledge Graph (Neo4j, GraphRAG)** | Entity Embedding + Edge Weight | Multi-hop 추론 정확도^ |
| **BM25 (Elasticsearch, OpenSearch)** | RRF Hybrid Search | Lexical 정확도 + Semantic 재현율 동시 확보 |
| **Reranker (Cohere Rerank 3, BGE-reranker)** | Cross-Encoder 후처리 | NDCG@10 10~25%^ |
| **Streaming
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 268 / 300

<- **이전**: [267. 스트리밍 ETL 실시간 파이프라인 설계 (Streaming ETL Real-time Pipeline Design)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/267_streaming_etl/)
**다음**: [269. 그래프 데이터베이스 관계 모델링 지식 그래프 (Graph Database Knowledge Graph Neo4j)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/269_graph_database/) ->

---
