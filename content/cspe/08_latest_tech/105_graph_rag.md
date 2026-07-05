---
title: "그래프 RAG (Graph Retrieval-Augmented Generation)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 105
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 방대한 문서에서 개체(Entity)와 그들 간의 관계(Relationship)를 추출해 거대한 '지식 그래프(Knowledge Graph)'를 구축한 뒤, 이를 바탕으로 문맥과 관계망을 탐색해 LLM에 주입하는 RAG 아키텍처.
- **필요성**: 기존 벡터(Vector) 기반 RAG는 단순히 '단어 의미가 비슷한 조각(Chunk)'들만 가져올 뿐, 문서 전반에 걸쳐 흩어진 정보들을 연결(Connecting the dots)하거나 거시적인 구조를 요약하는 데는 완전한 맹점(Blind spot)을 가짐.
- **핵심 직관**: 백과사전에서 "스티브 잡스"가 포함된 페이지 조각들을 무작위로 찢어 오는 것(Vector RAG)이 아니라, 스티브 잡스를 중심으로 "애플 창업 $\rightarrow$ 워즈니악과 친구 $\rightarrow$ 아이폰 발표"라는 '인물 관계도와 마인드맵'을 그려서 통째로 건네주는 것(Graph RAG).

## 깊이 이해
- **배경**: 2024년 마이크로소프트(MS) 연구소가 논문으로 구체화하며 폭발적 관심. 문서의 숲(전체 맥락)은 보지 못하고 나무(문서 조각)만 보는 기존 RAG의 치명적 한계를 지식 그래프의 구조적 특성으로 해결.
- **작동 원리**:
  1. (사전 작업): LLM을 돌려 문서 전체를 읽고, 모든 인물, 장소, 개념(Node)과 그 사이의 관계(Edge)를 뽑아내어 지식 그래프(Neo4j 등)를 생성.
  2. 그래프의 군집(Community) 단위로 미리 요약본(Summary)을 만들어 둠.
  3. (검색 시): "이 회사의 핵심 사업 변화 추이는?"처럼 포괄적인 질문이 들어오면, 노드 간 연결선(Multi-hop)을 따라가거나 커뮤니티 요약본을 조합하여 전체적인 그림(Global Context)을 응답.
- **구체 예시**: 수사 기관의 범죄 기록 분석. 벡터 검색으로 "김철수"를 치면 김철수 이름이 들어간 조서 파편만 나옴. Graph RAG를 쓰면 "김철수가 A에게 송금함 $\rightarrow$ A는 B와 통화함 $\rightarrow$ B는 횡령 사건 주범임"과 같이 흩어진 문서 속 숨겨진 돈세탁 네트워크 경로(Multi-hop)를 단숨에 찾아냄.
- **흔한 오해/주의점**: Graph RAG가 무조건 더 좋은 것은 아님. 지식 그래프를 구축(Index)할 때 문서를 전부 LLM으로 분석해야 하므로 기존 임베딩 방식보다 시간과 토큰 비용이 수십 배에서 수백 배 더 듦. 가성비(Trade-off) 철저히 따져야 함.

## 연결 개념
- **Knowledge Graph (지식 그래프)**: 노드(개체)와 엣지(관계)로 세상의 지식을 표현하는 그래프 데이터베이스 (예: Neo4j).
- **Multi-hop QA (다중 홉 추론)**: 한 번의 검색으로 알 수 없고, A를 찾아 B를 알고, B를 찾아 C를 알아야 하는 연쇄적 질문. Graph RAG가 가장 강력하게 해결하는 문제 유형.
- **Vector DB (벡터 데이터베이스)**: 의미 기반 1차원 검색을 담당하며, Graph RAG 내에서 노드의 속성을 검색할 때 융합(Hybrid)하여 사용되기도 함.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 비정형 텍스트 코퍼스를 LLM을 통해 노드(Entity)와 엣지(Relationship) 구조의 지식 그래프로 변환(Indexing)하고, 이를 순회(Traversal)하며 글로벌 문맥과 논리적 관계를 추출해 내는 고차원 RAG 프레임워크.
- **가치**: 기존 Vector RAG의 근본적 한계인 파편화된 컨텍스트(Fragmented Context) 문제를 극복하고, 코퍼스 전체를 조망하는 글로벌 질문(Global Query)과 복잡한 연결(Multi-hop) 추론에서 압도적인 성능 우위를 제공함.
- **판단 포인트**: 지식 그래프 자동 추출 과정에서의 막대한 LLM 토큰 비용 및 오추출(Noise) 관리, Graph DB 운영 복잡도, Vector 검색과의 하이브리드 결합 설계 시 손익분기점 산정.

## Ⅰ. 개요 및 필요성
- **정의**: 사내 문서 등의 비정형 데이터에서 명시적 개체와 관계를 추출해 지식 그래프(Knowledge Graph)를 구축하고, 이를 기반으로 검색과 추론을 수행하여 LLM의 생성 능력을 증강하는 아키텍처.
- **배경**: 기존 Dense Vector 기반 검색은 국소적 문장 유사도(Local Similarity)에만 의존하여, "이 책의 전체 주제는 무엇인가?"나 "A와 B의 숨겨진 연관성은?"과 같은 구조적, 포괄적 질의에 대답하지 못함.
- **필요성**: 파편화된 데이터 조각들을 유의미한 시맨틱 네트워크(Semantic Network)로 연결하여, 모델의 정보 통합력과 설명 가능성(Explainability)을 극대화하기 위해 필수적임.

## Ⅱ. MS Graph RAG 아키텍처 (Indexing & Querying)
```text
[ 1. Indexing Phase (그래프 자동 구축) ]
비정형 문서 -> LLM 기반 추출 (NER & Relation) -> Node & Edge 생성
          -> 커뮤니티 탐지 알고리즘 (Hierarchical Clustering) 적용
          -> 커뮤니티별 글로벌 요약(Summary) 미리 생성 -> [ Graph DB 저장 ]

[ 2. Query Phase (글로벌/로컬 질의 응답) ]
사용자 질의 -> 질의 내 Entity 추출
          |
          +-> (Local Search) 특정 Entity 중심의 K-hop 이웃 정보 추출
          +-> (Global Search) 관련된 계층적 커뮤니티 요약본(Summary) 병렬 취합
          |
[ 3. Generation ] -> 취합된 서브 그래프(Sub-graph)와 요약본을 프롬프트로 주입 -> LLM 최종 답변
```

## Ⅲ. Vector RAG vs Graph RAG 핵심 비교
| 비교 항목 | Vector RAG | Graph RAG |
|:---:|:---|:---|
| **검색 메커니즘** | 임베딩 벡터 간 코사인 유사도 연산 | 그래프 순회(Traversal), K-Hop 관계 매칭 |
| **강점 (Sweet Spot)**| "특정 사실이나 문장을 찾아줘" (Local Query) | "전체 맥락을 요약해 줘", "연결고리를 찾아줘" (Global & Multi-hop) |
| **추론 연결성** | 파편화된 조각(Chunks) -> 연결성 부재 | 노드와 엣지로 이어진 명시적 추론 경로 제공 |
| **구축(Index) 비용** | 낮음 (임베딩 모델만 통과하면 됨) | **매우 높음** (전체 문서를 LLM으로 돌려 추출해야 함) |
| **설명 가능성** | 검색된 청크를 보여줌 (간접적) | **그래프 시각화**를 통한 명확한 연관 관계 제시 |

## Ⅳ. 주요 도입 패턴 (Hybrid Graph-Vector RAG)
- 실제 실무에서는 둘 중 하나만 쓰지 않고 결합하여 시너지를 극대화함.
- 노드의 메타데이터(속성)는 벡터로 임베딩하여 Vector DB에 넣고, 관계 구조는 Graph DB(Neo4j)에 넣음.
- 질의 시 $\rightarrow$ 1. 벡터 검색으로 질의와 연관된 '시작 노드(Start Node)'들을 빠르게 탐색 $\rightarrow$ 2. 시작 노드에서부터 Graph DB의 관계 선을 타고 2-hop, 3-hop 확장하며 관련 문맥을 쓸어 담음.

## Ⅴ. 한계점 및 운영 리스크 (Trade-off 분석)
- **리스크 1: 폭발적인 인덱싱 비용 (Indexing Cost)**:
  - 수십만 장의 문서를 지식 그래프로 자동 변환하려면, 수많은 LLM 프롬프팅 연산이 발생함. (MS 연구소 논문 기준, 인덱싱 비용이 기존 대비 수십~수백 배 상승)
  - **대응 방안**: 데이터의 갱신 주기가 짧은 동적 데이터(예: 데일리 뉴스)는 Vector RAG로 처리하고, 핵심 정적 자산(예: 사내 표준 매뉴얼, 계약서 규정)에만 선별적으로 Graph RAG를 파이프라이닝.
- **리스크 2: 온톨로지(Ontology)와 정규화(Resolution) 문제**:
  - LLM이 'Apple', '애플', '사과'를 각각 다른 노드로 추출하면 그래프가 지저분해지고 연결이 끊어짐(Entity Disambiguation 문제).
  - **대응 방안**: LLM 추출 프롬프트에 도메인 특화 사전(Dictionary)을 제공하고, 사후 처리로 유사 노드 간 병합(Node Merging) 자동화 프로세스 도입.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Global Query 처리 시 환각(Hallucination) 감소율, 다단계 추론(Multi-hop QA) 벤치마크 점수, 인덱싱 토큰 소모량 대비 성능 향상분.
- **실무 설계**: 제약/바이오 기업의 신약 개발 AI 구축 시. 수십만 건의 의학 논문과 임상 데이터를 Graph RAG 기반으로 구축. '단백질 구조(Node)' - '상호작용(Edge)' - '부작용(Node)' 간의 관계망을 Neo4j로 시각화하여, 연구원이 "A 화합물이 B 단백질을 거쳐 C 질병에 미치는 기전을 분석해"라고 질문할 때, 벡터 RAG가 놓치는 숨겨진 부작용 연관성(Hidden Link)을 정확히 도출.
- **결론**: Graph RAG는 단순 정보 검색(Information Retrieval)을 지식 탐구(Knowledge Discovery)의 영역으로 끌어올린 혁신이며, 생성형 AI가 인간 수준의 통찰력(Insights)을 모방하기 위해 나아갈 궁극적 진화 방향임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Entity/Relationship 추출 파이프라인, 하위 노드들을 계층적으로 묶는 커뮤니티 탐지 알고리즘(Leiden Algorithm 등)의 수학적 원리 상세 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: Vector 검색과의 Hybrid RAG 아키텍처 결합, 인덱싱 런타임 비용 최적화(FinOps 관점), 금융(FDS) 및 사이버 보안(Threat Hunting) 분야 등 실사용 Use-case 중심 도출.
