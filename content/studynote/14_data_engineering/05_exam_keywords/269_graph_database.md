+++
title = "269. 그래프 데이터베이스 관계 모델링 지식 그래프 (Graph Database Knowledge Graph Neo4j)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 그래프 데이터베이스는 노드(Node)-관계(Relationship)-속성(Property)으로 구성된 Property Graph Model을 채택하며, Neo4j는 이를 Disk-native(연결 리스트 + Fixed-size Pointer) 저장 구조로 구현하여 Multi-hop(3~6 hop) 트래버설에서 RDBMS 대비 100~1,000배의 성능 우위를 확보한다. 지식 그래프(Knowledge Graph)는 엔터티·관계·속성에 정규화된 온톨로지(SHACL/OWL)를 부여해 추론과 시맨틱 검색을 가능하게 하는 그래프 모델의 상위 개념이다.
> 2. **가치**: Gartner(2024) 기준 전 세계 기업 데이터의 약 75%가 관계형이며, 이를 그래프로 재해석하면欺诈 탐지 정확도 30%↑, 추천 시스템 CTR 15~25%↑, 신약 개발 후보 물질 도출 시간 60% 단축 등 정량적 임팩트를 검증할 수 있다. 또한 LLM의 Hallucination을 RAG + GraphRAG로 보완해 답변 신뢰도(Faithfulness)를 40~70%까지 끌어올린다.
> 3. **판단 포인트**: 트래픽이 OLTP성 단순 Key-Value 조회(hop ≤ 2) 위주라면 RDBMS + 인덱스가 더 비용 효율적이고, 관계의 카디널리티가 높고 탐색 깊이가 3 hop 이상이며 스키마가 자주 변하는 도메인(소셜, 사기 탐지, 지식 베이스)에서 그래프 DB가 정당화된다. 저장 방식(Native vs Non-native), 일관성 모델(CA→CP), Cypher/RDF/SPARQL 중 어떤 질의 언어를 표준화할지, 그리고 온톨로지 거버넌스 팀의 운영 역량이 도입 성패의 분기점이다.

---

## Ⅰ. 개요 및 필요성

기존 RDBMS는 데이터를 2차원 테이블에 정규화(3NF/BCNF)하고 JOIN으로 관계를 계산한다. 그러나 현실 세계의 데이터는 "고객이 거주하는 도시 → 도시에 본사를 둔 회사 → 회사가 발행한 상품 → 상품을 구매한 다른 고객"처럼 **5~6 hop을 횡단해야 인사이트가 도출**되는 사례가 압도적으로 많다. SNS 친구 추천(친구의 친구의 친구), 자금 세탁 추적(다층 Shell Company 네트워크), 신약 후보 탐색(유전자-단백질-경로-질환)이 대표적이다. RDBMS에서 6 hop을 Self-JOIN하면 6개의 Intermediate Result Set이 폭발적으로 증가해(Self-JOIN 폭발, Optimizer의 한계) 사실상 분석이 불가능해진다. 또한 테이블 스키마를 변경하면 모든 자식 테이블·인덱스·뷰·저장 프로시저를 재작성해야 하므로, **스키마 진화 비용(Schema Evolution Cost)**이 매우 크다.

그래프 데이터베이스는 관계를 1급 시민(First-class Citizen)으로 만들어, JOIN을 **물리적 포인터(Disk-resident Pointer)로 미리 매핑**해두고 트래버설 시점에만 비용을 지불한다(Index-Free Adjacency). Neo4j v5(2023~)는 Record Size를 15 bytes로 줄이고 Bolt 5.0(Bolt v5, 2024) 프로토콜로 Pipe-lining을 강화했으며, 다수의 도입 기업이 평균 **Time-to-Insight를 70% 단축**했다고 보고했다. 지식 그래프는 여기에 한 걸음 더 나아가, **온톨로지(RDF Schema/OWEL/SHACL)**를 얹어 "A는 B의 부분집합이다(SubClassOf)", "A는 B와 상호 배타적(DisjointWith)" 같은 **의미론적 제약과 추론(Reasoning)**을 가능케 한다. 이 두 축이 만나면서 그래프는 단순 저장소를 넘어 **"연결된 지능(Connected Intelligence)"**의 코어 엔진으로 격상되었다.

```text
[관계형 vs 그래프: 4-hop 탐색 비용 비교]

  RDBMS (6 Tables JOIN)                       Graph DB (Native Index-Free Adjacency)
  ────────────────────────                    ─────────────────────────────────────
  Customer ─┐                                (Customer:Person {id:1})
            │  JOIN(4회)                        │─[:LIVES_IN]──────────► (City {name:"Seoul"})
  Address ──┤  ↘ 폭발적 중간집합                  │                       │
            │   100만 × 1만 = 100억 Rows          │─[:WORKS_AT]─────────► (Company {name:"Neo Corp"})
  City ─────┤                                   │                       │
            │  Optimizer 한계                      │─[:PURCHASED]────────► (Product {sku:"P-001"})
  Order ────┤  Hash-Join 비용 ↑↑                 │                       │
            │   I/O Random Read ↑↑                │─[:BOUGHT_WITH ◄─────┐│
  Product ──┘                                   ▼                       ▼│
                                                (Customer:Person {id:2}) (Customer {id:3})
  ⏱ 4 hop 평균 12.3초 (TPC-H SF=10)             ⏱ 4 hop 평균 0.04초 ──────┘
                                                (캐시 적중 시 < 1 ms)
```

관계형 패러다임은 "데이터를 분해하고 다시 조립한다(Decompose & Reassemble)"이고, 그래프 패러다임은 "**처음부터 연결된 채로 저장한다(Store-as-connected)**". 노드가 생성될 때 관계(Edge)가 디스크에 포인터로 기록되고, 그 포인터는 양방향 ID-Pair(Outgoing/Incoming) 모두로 인덱싱된다. 이 점이 RDBMS와의 결정적 차이이며, 데이터가 기하급수적으로 연결될수록(Social Network 평균 Degree 200+) 비용 곡선이 반대 방향으로 움직인다.

- **📢 섹션 요약 비유**: RDBMS는 친구 주소를 적힌 전화번호부를 6권으로 나눠 보관하고 매번 6권을 뒤지는 서점 직원과 같고, 그래프 DB는 친구마다 "다음 친구를 직접 가리키는 손가락"이 그려진 분홍색 실타래 지도(Reddit Maps) — 손가락을 따라가기만 하면 곧장 도착한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Neo4j 5.x의 아키텍처는 **Layered Storage** 위에서 **Causal Cluster**가 Bolt 5.0으로 클라이언트에 서비스를 제공한다. 내부적으로는 페이지 캐시(Page Cache, 기본 Heap의 50% 할당), 라벨/관계 타입별 커서, 트랜잭션 상태 머신(OPTIMISTIC Concurrency + Deadlock Detection by wait-for graph), APOC/AuraDS 같은 Procedure Library로 구성된다.

```text
                          Neo4j 5.x Causal Cluster Architecture
  ┌──────────────────────────────────────────────────────────────────────┐
  │                       Client Driver (Java/Python/JS/Go)              │
  │                              │ Bolt 5.0 Protocol (TCP/TLS 1.3)      │
  │                              │ Pipelining + Routing Context          │
  └──────────────────────────────┼───────────────────────────────────────┘
                                 ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐        │
  │   │  Core-1 (LE)  │◄──►│  Core-2       │◄──►│  Core-3 (Foll)│        │
  │   │ Raft Leader   │    │ Raft Follower │    │ Raft Follower │        │
  │   └───────┬───────┘    └───────┬───────┘    └───────┬───────┘        │
  │           │  Tx Replication (Raft, WAL Shipping)    │                │
  │           ▼                    ▼                    ▼                │
  │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐        │
  │   │  Read Replica │    │  Read Replica │    │  Read Replica │        │
  │   │   (off-load)  │    │   (off-load)  │    │   (off-load)  │        │
  │   └───────┬───────┘    └───────┬───────┘    └───────┬───────┘        │
  │           └────────────────────┼────────────────────┘                │
  │                                ▼                                     │
  │   ┌──────────────────────────────────────────────────────────┐       │
  │   │  Page Cache (Off-heap, Memory-mapped I/O, mmap)          │       │
  │   │  ─ Label/Type Index ─ Schema Cache ─ Statistics Store    │       │
  │   └──────────────────────────────────────────────────────────┘       │
  │                                ▼                                     │
  │   ┌──────────────────────────────────────────────────────────┐       │
  │   │  Store Files (per DB)                                    │       │
  │   │   neostore.nodestore.db      (Fixed 15B/node record)     │       │
  │   │   neostore.relationshipstore.db (Fixed 33B/rel record)   │       │
  │   │   neostore.propertystore.db  (Dynamic Property Blocks)   │       │
  │   │   neostore.labeltokenstore.db / relationship typestore   │       │
  │   │   neostore.transaction.db    (WAL, 1GB Rolling)          │       │
  │   │   neostore.counts.db         (Degree-aware Counts)       │       │
  │   └──────────────────────────────────────────────────────────┘       │
  └──────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ Graph Data Science (GDS) — In-memory Graph
                                 │ APOC 200+ Procedures — Data Integration
                                 │ Bloom / Browser — Visualization
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Node Store / Relationship Store** | 노드·관계의 Fixed-size Record 저장 | 노드 15B(Next Rel + Next Prop + Label + 1st Rel), 관계 33B(Start/End Node + Type + Prev/Next Rel×2 + 1st Prop). 인접 노드 간 **양방향 포인터**로 저장되어 Index-Free Adjacency 보장. |
| **Page Cache (Off-heap)** | Hot Page 핫 캐싱, mmap 기반 Zero-copy I/O | Heap 외 영역(Off-heap)에 매핑되어 GC Pause 최소화. 기본 `dbms.memory.pagecache.size=50%` of RAM. 캐시 미스 시 디스크 Random Read 발생. |
| **Causal Cluster + Raft** | Leader-Follower 합의, Multi-DC Replication | Raft로 Leader Election(1 Core Leader, 나머지 Follower). 모든 쓰기는 Leader 경유, Transaction은 전 Core에 동기 복제(SYNC) 또는 비동기 복제(ASYNC). Read Replica는 최종 일관성(Eventually Consistent). |
| **Bolt 5.0 Protocol** | 클라이언트-서버 고속 RPC | Binary Frame + Pipelining(다중 쿼리 묶음 전송) + Routing Context(`{address: "neo4j://..."}`). TLS 1.3, Kerberos, SCRAM-SHA-256 인증 지원. RTT < 1 ms LAN, 50+ k req/s 단일 노드 처리. |
| **Cypher Query Engine** | 패턴 매칭 선언형 질의 | ASCII Art 문법(`(a:PERSON)-[:KNOWS]->(b)`). Logical Plan → Physical Plan 변환 시 Rule-based + Cost-based Optimizer. Cartesian Product 경고 시 `USING INDEX` 힌트 사용. v5부터 `EXPLAIN` / `PROFILE`로 `db.hits` 분석 가능. |
| **Schema & Statistics** | 라벨/타입/인덱스 메타데이터 | 라벨 토큰(0~2³²) 단위로 분리 저장. Statistics Store는 `dbms.statistics.divergence` 주기(기본 1h)로 갱신되어 Cardinality 추정 정확도 유지. |

**핵심 동작 메커니즘 — Index-Free Adjacency & Multi-hop Traversal**:
노드 A의 Relationship Record 첫 8바이트에는 A와 연결된 첫 관계의 ID가 저장되어 있다. 쿼리 `MATCH (a)-[*1..6]->(b)` 실행 시 엔진은 (1) 라벨/타입 인덱스로 시작 노드 집합을 좁히고, (2) 시작 노드의 첫 관계 ID로 Hop을 시작, (3) 각 Hop에서 Relationship Record의 `Start Node ID ↔ End Node ID` 포인터로 인접 노드 Record를 O(1)로 Random Read한다. 디스크 Random Read가 발생하긴 하지만, 페이지 캐시 히트 시 Latency는 **마이크로초(μs) 단위**로 떨어진다. RDBMS는 매 Hop마다 Index Lookup + B-Tree Traversal + Hash Join + Materialize가 일어나므로 Latency가 누적된다. 6 hop 기준 RDBMS는 **O(N log N × k)** (k = 평균 Degree), 그래프는 **O(hop × Degree)** 이다.

**트랜잭션 모델 (OPTIMISTIC)**:
기본 Isolation Level은 `READ_COMMITTED`. 쓰기 트랜잭션 시작 시 시작 시점의 Snapshot을 잡고, 커밋 시점에 Lock 충돌을 감지하면 `TransientError`를 던지고 Driver가 자동 재시도(Retry, 기본 3회). `MATCH ... DETACH DELETE`나 깊은 트래버설은 메모리 폭주 위험이 있으므로 `dbms.transaction.concurrent.max_offheap_usage`로 Heap 보호.

- **📢 섹션 요약 비유**: Node Store는 서가의 "책 한 권", Relationship Store는 각 책에 붙은 "다음 책을 가리키는 색인 테이프", Page Cache는 "책상 위 항상 펼쳐두는 사본" — 테이프를 따라가기만 하면 책장 전체를 헤집지 않고도 6권짜리 시리즈를 끝까지 읽을 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | **RDBMS (PostgreSQL 16)** | **Document DB (MongoDB 7)** | **Triple Store (RDF/OWL, Stardog)** | **Neo4j 5 (LPG)** |
| :--- | :--- | :--- | :--- | :--- |
| **데이터 모델** | 고정 스키마, Table (행/열) | JSON Document, Schema-less | RDF Triple (S-P-O) + Ontology | Labeled Property Graph (노드/관계/속성) |
| **질의 언어** | SQL (ANSI/PG Dialect) | MQL (Aggregation Pipeline) | SPARQL 1.1 / SPARQL* | Cypher (OpenCypher 5, 2024) |
| **3 hop 이상 성능** | 매우 느림 (Self-JOIN 폭발) | N/A ($lookup 1~2 level 한계) | 중간 (RDF Index 효율 의존) | 매우 빠름 (Index-Free Adjacency) |
| **추론(Reasoning)** | 없음 (Trigger로 유사 구현) | 없음 | **내장**(OWL 2 RL/QL, SHACL 검증) | 제한적 (APOC/AuraDS 일부 Procedure) |
| **스키마 유연성** | 낮음 (Migration 비용 ↑) | 높음 | 중간 (Ontology 강제 가능) | 높음 (Schema Optional, Constraint 가능) |
| **정합성·트랜잭션** | ACID 완전 지원 | Multi-Document ACID (4.0+) | ACID (DBpedia 일부) | ACID + OPTIMISTIC + Raft |
| **확장성 모델** | 수직/Read Replica/Partitioning | Sharding (Hash-based) | Sharding (Predicate/Graph) | Causal Cluster (쓰기 Raft, 읽기 Replica) |
| **적합 워크로드** | OLTP, ERP, 회계 | Catalog, IoT, 사용자 프로파일 | 시맨틱 웹, 신약·온톨로지, Linked Data | 소셜, 사기 탐지, 추천, 지식 그래프, IDD |
| **Vector / AI 통합** | pgvector (외부) | Atlas Vector Search (내장) | Stardog Voicebox (내장) | **Vector Index (5.11+, 2024)**, GraphRAG, GDS Embeddings |
| **대표 도입 사례** | 금융 코어 뱅킹 | 전자상거래 카탈로그 | Google Knowledge Graph, BBC, NIH UniProt | Uber
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 269 / 300

<- **이전**: [268. 벡터 데이터베이스 임베딩 유사도 검색 (Vector Database Embedding Similarity Search)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/268_vector_database/)
**다음**: [270. 시계열 데이터베이스 IoT 모니터링 저장 (Time Series Database InfluxDB Prometheus)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/270_time_series_database/) ->

---
