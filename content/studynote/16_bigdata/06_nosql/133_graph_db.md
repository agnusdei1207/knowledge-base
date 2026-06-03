+++
title = "133. 그래프 데이터베이스 (Graph DB) — Neo4j/Amazon Neptune/Memgraph"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 엔티티(노드)와 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)(엣지)를 1등급 시민으로 저장하여, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색이 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 없이 포인터 추적 방식으로 O(1) per hop [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 중심 NoSQL이다.
- **가치**: 소셜 네트워크 친구의 친구, 사기 탐지 링, 추천 엔진처럼 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만큼 중요한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 RDBMS JOIN이 수 분 걸릴 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 밀리초 만에 처리한다.
- **판단 포인트**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)보다 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 중요하고 탐색 깊이가 3홉 이상이며 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 구조가 예측 불가능하게 변한다면, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 RDBMS보다 압도적으로 유리한 선택이다.

---

## Ⅰ. 개요 및 필요성

### [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 문제
RDBMS에서 "내 친구의 친구의 친구(3홉)"를 구하려면 동일 테이블에 3회 자기 조인(Self-[Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))이 필요하다. 네트워크가 클수록 지수적으로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비용이 증가하여 수억 명 규모의 소셜 네트워크에서는 실질적으로 불가능하다.

### [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)의 기본 구성 요소



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Property Graph 모델</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Node (노드)</div><div class="kb-diagram-cell">Node (노드)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Label: Person</div><div class="kb-diagram-cell">엣지</div><div class="kb-diagram-cell">Label: Product</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Properties:</div><div class="kb-diagram-cell">Properties:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- name: "홍길동"</div><div class="kb-diagram-cell">BOUGHT</div><div class="kb-diagram-cell">- name: "키보드"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- age: 30</div><div class="kb-diagram-cell">since:</div><div class="kb-diagram-cell">- price: 89000</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- city: "서울"</div><div class="kb-diagram-cell">"2026"</div><div class="kb-diagram-cell">- stock: 15</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드(Node): 엔티티</div><div class="kb-diagram-cell">엣지(Edge/Relationship): 관계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">라벨(Label): 타입</div><div class="kb-diagram-cell">속성(Property): 메타데이터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">방향(Direction): 단방향 또는 양방향</div></div>
</div>
</div>



### 대표 솔루션 비교

| 솔루션 | 특징 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | 적합 사용처 |
|:---:|:---|:---:|:---:|
| **Neo4j** | 가장 성숙, ACID, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없는 인접성 | Cypher | 엔터프라이즈 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **Amazon Neptune** | AWS 관리형, 멀티 모델 | Gremlin/SPARQL | 클라우드 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **Memgraph** | 인메모리, 스트리밍, OpenCypher | Cypher | 실시간 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **ArangoDB** | 문서+[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)+KV 멀티모델 | AQL | 유연한 멀티모델 |
| **TigerGraph** | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리, 딥 링크 분석 | GSQL | 엔터프라이즈 분석 |

📢 **섹션 요약 비유**
> RDBMS가 정류장 목록표([데이터 중심](/knowledge-base/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/))라면, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 지하철 노선도([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 중심)다. 노선도에서는 "강남에서 3번 환승하면 어디까지 갈 수 있나?"를 지도를 눈으로 따라가듯 즉시 파악할 수 있지만, 목록표에서는 수십 번의 검색과 비교가 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없는 인접성 ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)-Free [Adjacency](/knowledge-base/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RDBMS의 관계 탐색 (JOIN 기반):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SELECT u2.name FROM users u1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">JOIN follows f ON u1.id = f.follower_id</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">JOIN users u2 ON f.following_id = u2.id</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">WHERE u1.name = '홍길동'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 전체 follows 테이블 스캔 → O(N) 비용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 깊이 3홉: 3중 JOIN → O(N³) 최악의 경우</div></div>
<div class="kb-diagram-note">그래프 DB의 관계 탐색 (포인터 추적):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Node</div><div class="kb-diagram-node">홍길동</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FOLLOWS</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">이몽룡</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 포인터</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Node</div><div class="kb-diagram-node">이몽룡</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FOLLOWS</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 각 노드가 인접 노드의 직접 포인터 보유</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 홉당 O(1) 탐색 → 깊이와 무관하게 빠름</div></div>
</div>
</div>



### Neo4j 내부 저장 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Neo4j 저장 파일 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">neostore.nodestore.db ← 노드 레코드 (고정 15바이트)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">neostore.relationshipstore ← 관계 레코드 (34바이트)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">neostore.propertystore.db ← 속성 레코드 (가변 길이)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">neostore.labeltokenstore ← 라벨 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드 레코드 구조:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ID</div><div class="kb-diagram-cell">첫 관계</div><div class="kb-diagram-cell">첫 속성</div><div class="kb-diagram-cell">라벨</div><div class="kb-diagram-cell">플래그</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 노드에서 관계 체인을 직접 포인터로 탐색</div></div>
</div>
</div>



### [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 모델 유형 비교

| 모델 | 표현 방식 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | 특징 |
|:---:|:---:|:---:|:---|
| <strong>Property <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/">Graph</a></strong> | 노드/엣지 + [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | Cypher, Gremlin | 가장 직관적, 엔터프라이즈 표준 |
| **RDF (Resource Description Framework)** | 주어-술어-목적어 트리플 | SPARQL | [시맨틱 웹](/knowledge-base/studynote/06_ict_convergence/01_blockchain/003_semantic_web/), [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) |
| **Hypergraph** | N개 노드를 잇는 하이퍼엣지 | 전용 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 모델링 |

📢 **섹션 요약 비유**
> [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없는 인접성은 전화번호부에서 이름을 찾는 것(O(N))이 아니라, 각 사람이 명함에 다음 연락처를 직접 적어두는 것(O(1))과 같다. 아무리 긴 연락 체인이어도 명함을 따라가면 되니, 전체 전화번호부를 뒤지는 비용이 없다.

---

## Ⅲ. 비교 및 연결

### [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 유리한 워크로드

| 사용 사례 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | RDBMS 대비 |
|:---:|:---|:---:|
| 소셜 네트워크 탐색 | 친구의 친구(N홉) | 수초 → 수ms |
| 추천 엔진 | "이 상품 산 사람들이 같이 산 것" | 복잡한 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) → 단순 패턴 |
| 사기 탐지 | 계좌 거래 링 탐지 | 불가능 → 실시간 |
| [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) | 개념 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 추론 | 비정형 → 자연 표현 |
| 네트워크 IT | 의존성 분석, 영향 범위 계산 | 복잡 → 직관적 |

### ACID vs BASE [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB

```text
Neo4j (ACID):
  - 관계 일관성 보장 (고아 노드 방지)
  - 트랜잭션 내 복수 노드/관계 변경
  - 적합: 금융 사기 탐지, 규정 준수

Amazon Neptune (조정 가능):
  - Multi-AZ 복제
  - SPARQL로 연합 쿼리
  - 적합: 지식 그래프, 소셜 그래프
```

📢 **섹션 요약 비유**
> [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB와 RDBMS의 선택은 도시 내비게이션과 같다. RDBMS는 "도로 목록"을 가지고 경로를 계산하고, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 이미 도로가 연결된 지도를 가지고 있다. 출발지와 목적지 사이 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 복잡할수록 지도([그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB)가 월등히 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 사기 탐지 시나리오 (금융권 활용 사례)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">시나리오: 여러 계좌가 동일 휴대폰 번호를 공유하고</div>
<div class="kb-diagram-note">짧은 시간에 순환 송금하는 패턴 탐지</div>
<div class="kb-diagram-note">그래프 표현:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Account A ─</div><div class="kb-diagram-node">SENT_TO</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Account B</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Account B ─</div><div class="kb-diagram-node">SENT_TO</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Account C</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Account C ─</div><div class="kb-diagram-node">SENT_TO</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Account A ← 순환 고리(Ring) 탐지!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">REGISTERED</div><div class="kb-diagram-note">── Account A</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">REGISTERED</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">동일 번호 공유!</div></div>
<div class="kb-diagram-note">Cypher 쿼리:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">MATCH path=(a:Account)-</div><div class="kb-diagram-node">:SENT_TO*2..5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(a)</div></div>
<div class="kb-diagram-note">WHERE ALL(r IN relationships(path)</div>
<div class="kb-diagram-note">WHERE r.amount &gt; 1000000</div>
<div class="kb-diagram-note">AND r.time &gt; timestamp() - 3600000)</div>
<div class="kb-diagram-note">RETURN path</div>
</div>
</div>



### 기술사 판단: [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB 도입 기준

```text
그래프 DB 도입 검토 기준:
  ① 관계 탐색 깊이 ≥ 3홉
  ② 관계 유형이 동적으로 추가됨
  ③ 관계 자체에 속성(가중치, 날짜 등) 필요
  ④ 실시간 경로 탐색, 클러스터링 필요

RDBMS 유지 기준:
  ① 단순 1~2홉 관계
  ② 배치 집계 쿼리 중심
  ③ ACID 강한 일관성 필수
  ④ 기존 SQL 인프라 활용
```

📢 **섹션 요약 비유**
> 금융 사기 탐지에서 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 거미줄 속 파리를 찾는 것과 같다. RDBMS로는 각 실을 하나하나 비교해야 하지만, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 거미줄 전체 패턴을 한눈에 보고 이상한 진동(순환 패턴)을 즉시 감지할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 산업별 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB 활용 효과

| 산업 | 활용 | 효과 |
|:---:|:---:|:---:|
| 금융 | 사기 탐지 링 분석 | 탐지율 30% 향상, 오탐 50% 감소 |
| 이커머스 | 추천 엔진 | [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 15~20% 향상 |
| 통신 | 네트워크 의존성 분석 | 장애 영향 분석 90% 단축 |
| 의료 | [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) | 약물 상호작용 발견 |
| 미디어 | 콘텐츠 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | Netflix 유사 추천 |

### 결론
[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 "[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"인 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 RDBMS가 해결할 수 없는 문제를 해결하는 특화 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)다. 기술사 시험에서는 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 없는 인접성 원리</strong>, <strong>Property <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/">Graph</a> vs RDF 모델 차이</strong>, **사기 탐지·추천 엔진 적용 시나리오**, <strong>Cypher 패턴 매칭 문법</strong>이 핵심 논점이다.

📢 **섹션 요약 비유**
> [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB 도입은 지도 앱이 없던 시대에 지도 앱을 도입하는 것과 같다. "서울에서 부산까지 최단 경로"를 묻는 질문에 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 노선 전체 목록을 뒤지는 것(RDBMS)과 지도를 보는 것([그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB)은 차원이 다른 접근이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| Cypher | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | 패턴 매칭 기반 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| SPARQL | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | RDF 트리플스토어 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없는 인접성 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 원리 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 포인터로 직접 저장 |
| PageRank | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 노드 중요도 계산 |
| 커뮤니티 탐지 | [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) | 클러스터(사기 그룹) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">관계형 DB (RDBMS) — 조인(Join)으로 관계 탐색, 깊은 연결에서 성능 저하</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프 DB (Graph DB) — 노드·엣지·속성으로 관계를 네이티브 저장·탐색</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프 쿼리 언어 (Cypher / Gremlin / SPARQL) — 경로 탐색·패턴 매칭 전용 쿼리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">지식 그래프 (Knowledge Graph) — 개체 간 시맨틱 관계로 AI 추론 강화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프 머신러닝 (Graph ML) — GNN으로 구조적 패턴 학습, 사기 탐지·추천에 적용</div></div>
</div>
</div>



이 흐름은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 조인 한계를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 극복하고 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)·GNN으로 AI와 융합하는 발전 경로를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 선으로 이어놓은 그림 — "내 친구의 친구는 누구?"를 선을 따라가면 바로 알 수 있어요.
2. 일반 DB가 "학생 명단"이라면 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 "친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도" — [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 복잡할수록 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 훨씬 유용해요.
3. 사기꾼들이 돈을 돌리는 고리 패턴을 찾는 것도 선으로 이어진 그림에서 동그라미를 찾는 것과 같아서, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 딱 맞는 도구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 262

← **이전**: [132. Apache Cassandra — 마스터 없는 링 구조 분산 데이터베이스](/knowledge-base/studynote/16_bigdata/06_nosql/132_cassandra/)
**다음**: [134. Cypher 쿼리 언어 (Cypher Query Language) — 그래프 패턴 매칭](/knowledge-base/studynote/16_bigdata/06_nosql/134_cypher_query/) →

---
