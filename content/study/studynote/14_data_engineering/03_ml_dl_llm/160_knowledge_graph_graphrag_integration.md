+++
weight = 160
title = "160. 지식 그래프 (Knowledge Graph) + GraphRAG 연동망"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지식 [[070_graph_datastructure|그래프]](Knowledge [[104_graph|Graph]])는 엔티티(Entity)와 [[083_relationship_in_er_model|관계]]([[061_relation_schema_instance|Relation]])를 삼중쌍(Triple: 주어-술어-목적어)으로 구조화한 지식 저장 체계이며, GraphRAG는 이를 LLM과 결합해 구조적 추론을 수행한다.
> 2. **가치**: 단순 벡터 검색([[276_fine_tuning|RAG]])이 "관련 문서 검색"에 그치는 반면, GraphRAG는 지식 [[070_graph_datastructure|그래프]]의 다단계 추론(Multi-hop Reasoning)으로 "A의 상사의 동료의 연락처"같은 복잡한 [[083_relationship_in_er_model|관계]]형 질의를 처리한다.
> 3. **판단 포인트**: 구조화된 [[064_relation_domain|도메인]] 지식(의료, 법률, 기업 조직)에는 GraphRAG가 강하고, 비정형 최신 정보에는 표준 RAG가 효율적이다 — 두 가지를 하이브리드로 결합하는 것이 최선이다.

## Ⅰ. 개요 및 필요성

"삼성전자 CEO의 전 직장 동료의 현재 직책은?" 같은 다단계 [[083_relationship_in_er_model|관계]]형 질의는 벡터 검색 RAG로는 처리가 어렵다. 지식 [[070_graph_datastructure|그래프]]는 이런 복잡한 [[083_relationship_in_er_model|관계]]를 구조적으로 탐색한다.

대표적 지식 [[070_graph_datastructure|그래프]]: Google Knowledge [[104_graph|Graph]], Wikidata, DBpedia, 기업 내부 [[064_relation_domain|도메인]] KG

**지식 [[070_graph_datastructure|그래프]] 기본 구성**
- 엔티티 (Entity): 노드 — 사람, 조직, 제품, 개념
- [[083_relationship_in_er_model|관계]] ([[061_relation_schema_instance|Relation]]): 엣지 — 소속, 제조, 의존, 포함
- 삼중쌍 (Triple): (삼성전자, CEO, 이재용) — 주어-술어-목적어

📢 **섹션 요약 비유**: 지식 [[070_graph_datastructure|그래프]]는 AI를 위한 구조화된 백과사전이다. 단순히 텍스트를 저장하는 게 아니라, 모든 지식 간의 [[083_relationship_in_er_model|관계]]를 명시한다.

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | 설명 |
|:---|:---|
| 삼중쌍 (Triple) | (Subject, Predicate, Object) |
| 온톨로지 (Ontology) | 엔티티 유형, [[083_relationship_in_er_model|관계]] 유형의 [[005_schema|스키마]] 정의 |
| SPARQL | 지식 [[070_graph_datastructure|그래프]] 질의 언어 |
| [[278_instruction_tuning|임베딩]] | TransE, RotatE — 엔티티/[[083_relationship_in_er_model|관계]]를 벡터로 표현 |
| 링크 예측 | 누락된 삼중쌍 예측 (지식 [[070_graph_datastructure|그래프]] 완성) |
| Neo4j, GraphDB | 지식 [[070_graph_datastructure|그래프]] 저장 시스템 |

```
[지식 그래프 + GraphRAG 구조]

지식 그래프 예시:
  삼성전자 ──[CEO]──▶ 이재용
  삼성전자 ──[소재지]──▶ 서울
  삼성전자 ──[제품]──▶ 갤럭시 시리즈
  이재용 ──[학력]──▶ 하버드 대학원
  이재용 ──[국적]──▶ 대한민국

GraphRAG 질의: "삼성전자 CEO가 다닌 학교는?"
                    │
        ①삼성전자 노드 검색
                    │
        ②CEO 관계 따라 이재용
                    │
        ③이재용의 학력 관계 탐색
                    │
        ④하버드 대학원 반환
                    │
        LLM이 자연어로 응답 생성

[GraphRAG vs 표준 RAG 비교]

표준 RAG:
"삼성전자 CEO 학력" ─▶ 벡터 검색 ─▶ 관련 문서 반환
→ 문서에 명시된 경우만 답변 가능

GraphRAG (Microsoft):
"삼성전자 CEO 학력" ─▶ 엔티티 추출 ─▶ 그래프 탐색
─▶ 다단계 관계 추론 ─▶ 정확한 구조적 답변

[GraphRAG 파이프라인 (Microsoft)]
문서
  │ 정보 추출 (LLM 활용)
  ▼
엔티티 & 관계 추출
  │
그래프 구축 (Neo4j 등)
  │ 커뮤니티 탐지 (Leiden 알고리즘)
  ▼
글로벌/로컬 요약 생성
  │
질의 처리:
  ├── 글로벌 질의: 커뮤니티 요약 활용
  └── 로컬 질의: 관련 서브그래프 탐색
          │
    LLM 최종 응답 생성
```

**지식 [[070_graph_datastructure|그래프]] [[278_instruction_tuning|임베딩]] 기법**

| 방법 | 수식 | 특징 |
|:---|:---|:---|
| TransE | h + r ≈ t | 단순, 1:1 [[083_relationship_in_er_model|관계]] |
| TransR | h + Mr ≈ t | [[083_relationship_in_er_model|관계]]별 공간 |
| RotatE | h ∘ r = t | 회전 연산, 역관계 |
| Knowledge [[104_graph|Graph]] [[301_bert_mlm|BERT]] | [[301_bert_mlm|BERT]] 기반 | 풍부한 표현 |

📢 **섹션 요약 비유**: GraphRAG는 "이 사람은 누구야?"라는 질문에 단순히 이름을 말하는 게 아니라, [[083_relationship_in_er_model|관계]]망 전체를 탐색해서 "이 사람은 A의 동료이고, B의 상사이며, C의 동창"이라고 설명한다.

## Ⅲ. 비교 및 연결

| 항목 | 표준 [[276_fine_tuning|RAG]] | [[530_graph_rag|GraphRAG]] | KG 직접 [[298_qkv_attention|쿼리]] |
|:---|:---|:---|:---|
| 다단계 추론 | ❌ | ✅ | ✅ |
| 최신 정보 | ✅ (인덱싱 후) | 보통 | ❌ |
| 구현 복잡도 | 낮음 | 높음 | 중간 |
| 비정형 텍스트 | ✅ | 보통 | ❌ |
| [[083_relationship_in_er_model|관계]] 정확도 | 보통 | ✅ | ✅ |
| 비용 | 낮음 | 높음 (KG 구축) | 중간 |

**[[530_graph_rag|GraphRAG]] 활용 사례**
- 의료: 약물-질병-유전자 [[083_relationship_in_er_model|관계]] 추론 (생물의학 KG)
- 법률: 판례-법령-당사자 [[083_relationship_in_er_model|관계]] 검색
- 기업: 조직도·인사·프로젝트 [[083_relationship_in_er_model|관계]] 질의
- 금융: 기업-주주-자회사 [[083_relationship_in_er_model|관계]] 분석 (사기 탐지)

📢 **섹션 요약 비유**: 표준 RAG가 구글 검색이라면, GraphRAG는 구글 지식 [[070_graph_datastructure|그래프]] — 단순 검색이 아니라 연결된 사실들을 탐색한다.

## Ⅳ. 실무 적용 및 기술사 판단

**지식 [[070_graph_datastructure|그래프]] 구축 파이프라인**
1. 소스 [[001_dikw_pyramid|데이터]]: 문서, DB, [[014_api_posix|API]]
2. 정보 추출: [[117_ner|NER]] ([[117_ner|개체명 인식]]), RE ([[083_relationship_in_er_model|관계]] 추출) — [[263_llm_large_language_model|LLM]] 활용 가능
3. 온톨로지 설계: 엔티티 유형, [[083_relationship_in_er_model|관계]] 유형 정의
4. [[070_graph_datastructure|그래프]] DB 저장: Neo4j, Amazon Neptune
5. 지식 [[070_graph_datastructure|그래프]] [[395_verification_process_review|검증]]: [[194_consistency_database_integrity|일관성]], 완전성 [[396_validation|확인]]

**[[530_graph_rag|GraphRAG]] 구현 (Microsoft [[530_graph_rag|GraphRAG]])**
```bash
# 설치
pip install graphrag
# 인덱싱 (문서 → KG 구축)
python -m graphrag.index --root ./data
# 질의
python -m graphrag.query --root ./data \
  --method global "삼성전자 주요 제품군은?"
```

**기술사 출제 포인트**
- "지식 [[070_graph_datastructure|그래프]]의 삼중쌍 구조를 설명하고, 일반 벡터 [[001_dikw_pyramid|데이터]]베이스와의 차이를 설명하시오"
- "GraphRAG가 표준 [[276_fine_tuning|RAG]] 대비 갖는 장점과 한계를 비교하시오"

📢 **섹션 요약 비유**: 지식 [[070_graph_datastructure|그래프]]는 AI의 두뇌에 체계적인 지식 지도를 심어주는 것이다. 단편적인 사실이 아닌 구조화된 지식 네트워크를 갖게 된다.

## Ⅴ. 기대효과 및 결론

지식 [[070_graph_datastructure|그래프]]와 LLM의 결합은 AI의 추론 능력을 크게 향상시킨다. LLM의 언어 이해력과 지식 [[070_graph_datastructure|그래프]]의 구조적 추론이 결합되면, 단순 텍스트 검색을 넘어 복잡한 전문 지식 [[064_relation_domain|도메인]]에서도 신뢰할 수 있는 [[190_ai_llm_requirements_specification|AI]] 어시스턴트가 가능하다.

Microsoft GraphRAG는 2024년 오픈소스로 공개되어 기업 내 문서를 지식 [[070_graph_datastructure|그래프]]로 변환하고 고급 질의 응답을 구현하는 실용적 도구가 됐다.

📢 **섹션 요약 비유**: GraphRAG는 AI에게 단순히 기억하는 능력이 아닌, 기억들 사이의 [[083_relationship_in_er_model|관계]]를 이해하는 '지능적 추론 능력'을 부여한다.

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 기반 | 지식 [[070_graph_datastructure|그래프]] (Knowledge [[104_graph|Graph]]) | 삼중쌍 구조 지식 |
| 구성 | 엔티티 (Entity) | [[070_graph_datastructure|그래프]] 노드 |
| 구성 | [[083_relationship_in_er_model|관계]] ([[061_relation_schema_instance|Relation]]) | [[070_graph_datastructure|그래프]] 엣지 |
| [[298_qkv_attention|쿼리]] | SPARQL | KG 질의 언어 |
| 결합 | [[530_graph_rag|GraphRAG]] | KG + [[263_llm_large_language_model|LLM]] 검색 증강 |
| 기술 | [[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]]) | [[070_graph_datastructure|그래프]] 학습 |
| 구현 | Neo4j, Amazon Neptune | [[070_graph_datastructure|그래프]] DB |

### 👶 어린이를 위한 3줄 비유 설명
1. 지식 [[070_graph_datastructure|그래프]]는 세상의 모든 사실을 "누가-무엇을-어떻게" 형태로 연결한 거대한 [[083_relationship_in_er_model|관계]] 지도예요.
2. GraphRAG는 그 지도를 사용해서 "A의 친구의 직장"처럼 여러 단계를 거치는 복잡한 질문도 찾아낼 수 있어요.
3. AI가 단순히 글을 검색하는 것에서, [[083_relationship_in_er_model|관계]]를 이해하고 추론하는 단계로 발전한 것이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
구조화 지식: 트리플 (주어, 술어, 목적어)
    │
    ▼
지식 그래프 (KG) 구축
    ├─► 수동: Wikidata · DBpedia
    └─► 자동: LLM 기반 엔티티/관계 추출
    │
    ▼
지식 그래프 임베딩 (TransE · RotatE · ComplEx)
    │
    ▼
GraphRAG (Microsoft, 2024)
    ├─► 문서 → KG 구성 → 커뮤니티 요약
    └─► 글로벌 검색 + 로컬 검색 결합
    │
    ▼
LLM + KG → 환각 감소 · 사실 기반 추론 강화
```
