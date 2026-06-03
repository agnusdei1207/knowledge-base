---
title: 107. 소셜 네트워크 분석 (SNA, Social Network Analysis) — 중심성/커뮤니티 탐지
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[107_classification|SNA]] (Social Network Analysis)는 개인·조직·시스템을 노드 (Node)로, [[083_relationship_in_er_model|관계]]를 엣지 (Edge)로 모델링하여 네트워크 구조와 정보 흐름을 분석하는 수학적·통계적 기법이다.
> 2. **가치**: 중심성 지표 (연결·매개·근접·고유벡터)로 핵심 인플루언서와 정보 병목을 발견하고, 커뮤니티 탐지 (Community [[961_deepfake_detection|Detection]])로 숨겨진 집단 구조를 드러내어 마케팅·보안·역학 조사에 활용한다.
> 3. **판단 포인트**: 수억 노드의 소셜 [[070_graph_datastructure|그래프]]는 단일 머신에서 처리 불가능하므로, [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX·Amazon Neptune·TigerGraph 등 [[136_variance|분산]] [[070_graph_datastructure|그래프]] 처리 플랫폼 선택이 핵심이다.

---

## Ⅰ. 개요 및 필요성

"당신이 누구를 아느냐가 당신이 무엇을 아는가보다 중요하다"는 말처럼, [[083_relationship_in_er_model|관계]] 구조 자체가 정보와 영향력의 흐름을 결정한다. 코로나 [[589_virus|바이러스]] 전파 경로 추적, SNS 허위정보 확산 패턴, 기업 내 비공식 협업 네트워크—이 모든 문제는 SNA로 접근할 때 새로운 인사이트를 얻을 수 있다.

수십억 명의 페이스북·링크드인·카카오 사용자 [[083_relationship_in_er_model|관계]]망은 기존의 행렬 기반 분석으로는 처리할 수 없는 초대형 스파스 (Sparse) [[070_graph_datastructure|그래프]]다. 빅데이터 기술과 SNA의 결합이 필요한 이유다.

- **📢 섹션 요약 비유**: SNA는 인간 [[083_relationship_in_er_model|관계]]망의 X-레이다. 겉으로 드러나지 않는 연결 구조와 영향력의 흐름을 투명하게 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│                SNA 분석 구조 및 주요 개념                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   노드 A ──────── 노드 B ──────── 노드 D                         │
│      │ \              │                                          │
│      │  \             │          중심성 지표:                    │
│      │   \            │          A: Degree=3 (연결 많음)         │
│   노드 C   \──── 노드 E          B: Betweenness 높음 (다리 역할) │
│               \                  E: Eigenvector 높음 (영향력)    │
│                노드 F                                            │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  커뮤니티 탐지:  {A,B,C} ←→ {D,E,F} (모듈러리티 최적화)         │
└──────────────────────────────────────────────────────────────────┘
```

### 핵심 중심성 지표

| 지표 | 수식/원리 | 의미 | 활용 |
|:---|:---|:---|:---|
| **연결 중심성 (Degree [[383_graph_mining_centrality_metrics|Centrality]])** | 노드의 직접 연결 수 / (N-1) | 가장 많이 연결된 [[152_hub_dummy_switching_intelligent|허브]] | 슈퍼 커넥터 발굴 |
| **매개 중심성 (Betweenness [[383_graph_mining_centrality_metrics|Centrality]])** | 노드를 통과하는 최단 경로 비율 | 정보 흐름의 병목/다리 | 핵심 브로커 [[655_ir_detection_analysis|식별]] |
| **근접 중심성 (Closeness [[383_graph_mining_centrality_metrics|Centrality]])** | 다른 모든 노드까지의 평균 거리 역수 | 정보 빠르게 전파 가능 | 전파 효율 분석 |
| **고유벡터 중심성 (Eigenvector [[383_graph_mining_centrality_metrics|Centrality]])** | 연결된 이웃의 중심성 가중 합 | 영향력 있는 노드와 연결 | PageRank의 기반 |

### 커뮤니티 탐지 [[001_algorithm_definition|알고리즘]]

| [[001_algorithm_definition|알고리즘]] | 원리 | 복잡도 | 특징 |
|:---|:---|:---|:---|
| **Louvain** | [[192_module_independence|모듈]]러리티 (Modularity) 최적화 | O(n log n) | 대규모 [[070_graph_datastructure|그래프]]에 실용적, 계층적 |
| **Girvan-Newman** | 매개 중심성 높은 엣지 순차 제거 | O(m²n) | 계층적 분해, 대규모에 느림 |
| **Label Propagation** | 이웃 레이블 다수결 전파 | O(n+m) | 가장 빠름, 비결정적 |
| **Spectral [[105_clustering_analysis|Clustering]]** | [[070_graph_datastructure|그래프]] 라플라시안 고유벡터 | O(n³) | 수학적으로 정교, 소규모 |

- **📢 섹션 요약 비유**: 중심성은 도시에서 교통의 [[152_hub_dummy_switching_intelligent|허브]]를 찾는 것과 같다. 연결 중심성은 가장 많은 도로가 만나는 교차로, 매개 중심성은 다른 도시로 가려면 반드시 거쳐야 하는 분기점이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[107_classification|SNA]] | [[211_recommendation_system|추천 시스템]] | [[070_graph_datastructure|그래프]] DB |
|:---|:---|:---|:---|
| **목적** | 구조·영향력 분석 | 개인화 추천 | [[083_relationship_in_er_model|관계]] [[001_dikw_pyramid|데이터]] 저장·[[298_qkv_attention|쿼리]] |
| **출력** | 중심성 지표, 커뮤니티 | 추천 아이템 목록 | Cypher/Gremlin [[298_qkv_attention|쿼리]] 결과 |
| **처리 방식** | [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]] | [[161_matrix_decomposition|행렬 분해]]·[[159_gnn_graph_neural_network_message_passing|GNN]] | [[070_graph_datastructure|그래프]] 순회 [[298_qkv_attention|쿼리]] |
| **대표 도구** | NetworkX, Gephi | Spark ALS | Neo4j, Amazon Neptune |

SNA와 [[114_graph_analytics|그래프 분석]] ([[114_graph_analytics|Graph Analytics]])은 개념적으로 겹치지만, SNA는 사회 과학적 맥락에서 행위자 간 [[083_relationship_in_er_model|관계]]를 중심으로 보고, [[114_graph_analytics|그래프 분석]]은 더 일반적인 구조 (도로망·물류·전력망)에 적용된다.

- **📢 섹션 요약 비유**: SNA는 "사람들의 [[083_relationship_in_er_model|관계]]"를 보는 사회학자의 렌즈이고, [[114_graph_analytics|그래프 분석]]은 "어떤 연결이든" 다루는 수학자의 렌즈다. 같은 도구를 다른 목적으로 사용하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. **인플루언서 마케팅**: 고유벡터 중심성·매개 중심성이 높은 노드 = 최적 바이럴 시드 (Seed) 선정
2. **사기 네트워크 탐지**: 금융 거래 [[070_graph_datastructure|그래프]]에서 밀집 커뮤니티 = 공모 거래 그룹 [[655_ir_detection_analysis|식별]]
3. **역학 조사**: 감염병 전파 경로 추적, 슈퍼스프레더 (Super-Spreader) [[655_ir_detection_analysis|식별]]
4. **조직 분석**: 이메일·슬랙 커뮤니케이션 [[070_graph_datastructure|그래프]]로 비공식 협업 네트워크 파악

### 빅데이터 처리 도구

| 도구 | 특징 | 처리 규모 |
|:---|:---|:---|
| **NetworkX (Python)** | 프로토타이핑·연구, 단일 머신 | 수백만 노드 |
| **Gephi** | [[003_bigdata_7v|시각화]] 특화, 인터랙티브 | 수십만 노드 |
| **[[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX** | [[136_variance|분산]] 처리, Pregel [[014_api_posix|API]] | 수십억 노드 |
| **TigerGraph** | 실시간 [[070_graph_datastructure|그래프]] [[298_qkv_attention|쿼리]] DB | 수십억 노드, 실시간 |
| **Amazon Neptune** | 관리형 [[070_graph_datastructure|그래프]] DB (RDF+Property [[104_graph|Graph]]) | 클라우드 스케일 |

- **📢 섹션 요약 비유**: 수억 명의 소셜 [[070_graph_datastructure|그래프]]는 노트북으로 분석하려는 것은 자동차로 태평양을 건너려는 것과 같다. 규모에 맞는 [[136_variance|분산]] 처리 플랫폼 선택이 [[107_classification|SNA]] 프로젝트의 성패를 가른다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 핵심 인물 [[655_ir_detection_analysis|식별]] | 마케팅·보안·조직 관리에서 핵심 노드 자동 발굴 |
| 허위정보 추적 | 가짜뉴스 확산 경로와 최초 전파자 역추적 |
| 사기·범죄 탐지 | 공모 집단의 네트워크 패턴 자동 탐지 |
| 조직 효율화 | 정보 병목 및 [[002_silo_hyeonhyung|사일로]] ([[002_silo_hyeonhyung|Silo]]) 구조 [[003_bigdata_7v|시각화]]로 협업 개선 |
| 역학·방역 | 감염병 전파 시뮬레이션 및 고위험 [[152_hub_dummy_switching_intelligent|허브]] 우선 관리 |

SNA는 개인이 아닌 [[083_relationship_in_er_model|관계]]가 가치를 만든다는 통찰에서 출발한다. 빅데이터 시대에 소셜 플랫폼의 폭발적 성장은 수십억 노드의 초거대 네트워크를 분석 대상으로 만들었고, [[136_variance|분산]] [[070_graph_datastructure|그래프]] 처리 기술의 발전이 이를 가능하게 했다. 앞으로 SNA는 [[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]])과 결합하여 링크 예측·노드 [[104_classification_analysis|분류]] 등 더 정교한 예측 모델로 진화할 것이다.

- **📢 섹션 요약 비유**: SNA는 사람들이 어떻게 연결돼 있는지 지도를 그리는 것이다. 지도가 있어야 가장 빠른 길도, 막힌 길도, 가장 중요한 교차로도 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| [[070_graph_datastructure|그래프]] 이론 ([[104_graph|Graph]] Theory) | SNA의 수학적 기반 |
| 중심성 지표 ([[383_graph_mining_centrality_metrics|Centrality]] Measures) | 노드 중요도 측정 핵심 도구 |
| 커뮤니티 탐지 (Community [[961_deepfake_detection|Detection]]) | 숨겨진 집단 구조 발굴 |
| PageRank | 고유벡터 중심성의 실용적 응용 (구글 검색) |
| [[159_gnn_graph_neural_network_message_passing|GNN]] ([[159_gnn_graph_neural_network_message_passing|Graph Neural Network]]) | [[107_classification|SNA]] + 딥러닝 결합의 최신 트렌드 |
| [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] GraphX | [[136_variance|분산]] 환경 대규모 [[070_graph_datastructure|그래프]] 처리 |
| Louvain [[001_algorithm_definition|알고리즘]] | 대규모 커뮤니티 탐지 표준 [[001_algorithm_definition|알고리즘]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[네트워크 그래프 구성 (Network Graph) — 노드(행위자)와 엣지(관계) 모델링]
    │
    ▼
[중심성 분석 (Centrality Analysis) — 연결·매개·근접 중심성으로 핵심 노드 탐지]
    │
    ▼
[커뮤니티 탐지 (Community Detection) — Louvain·Girvan-Newman으로 그룹 식별]
    │
    ▼
[영향력 확산 모델 (Diffusion Model) — SIR·IC 모델로 정보·전파 시뮬레이션]
    │
    ▼
[그래프 머신러닝 (GNN — Graph Neural Network) — 관계 구조 학습으로 추천·예측]
```

이 흐름은 [[083_relationship_in_er_model|관계]] [[070_graph_datastructure|그래프]] 구축에서 중심성 분석·커뮤니티 탐지·GNN까지 [[107_classification|소셜 네트워크 분석]] 기술이 진화하는 경로를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
- SNA는 반 친구들의 사이좋은 [[083_relationship_in_er_model|관계]]를 선으로 그려서 누가 제일 인기 많고, 어떤 무리가 있는지 알아내는 거예요.
- 매개 중심성이 높은 친구는 여러 무리 사이를 연결해주는 다리 역할을 하는 중요한 친구예요.
- 페이스북 같은 SNS에서 수억 명의 친구 [[083_relationship_in_er_model|관계]]를 이런 방식으로 분석해서 바이럴이나 사기를 탐지해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 110 / 262

← **이전**: [[109_text_mining|106. 텍스트 마이닝 (Text Mining) — TF-IDF/Word2Vec/BERT 기반 텍스트 분석]]
**다음**: [[111_anomaly_detection|108. 이상 탐지 (Anomaly Detection) — 통계/ML/딥러닝 기반 이상치 감지]] →

---
