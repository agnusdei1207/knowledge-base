+++
title = "107. 소셜 네트워크 분석 (SNA, Social Network Analysis) — 중심성/커뮤니티 탐지"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SNA](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) (Social Network Analysis)는 개인·조직·시스템을 노드 (Node)로, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 엣지 (Edge)로 모델링하여 네트워크 구조와 정보 흐름을 분석하는 수학적·통계적 기법이다.
> 2. **가치**: 중심성 지표 (연결·매개·근접·고유벡터)로 핵심 인플루언서와 정보 병목을 발견하고, 커뮤니티 탐지 (Community [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))로 숨겨진 집단 구조를 드러내어 마케팅·보안·역학 조사에 활용한다.
> 3. **판단 포인트**: 수억 노드의 소셜 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 단일 머신에서 처리 불가능하므로, [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) GraphX·Amazon Neptune·TigerGraph 등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 플랫폼 선택이 핵심이다.

---

## Ⅰ. 개요 및 필요성

"당신이 누구를 아느냐가 당신이 무엇을 아는가보다 중요하다"는 말처럼, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 구조 자체가 정보와 영향력의 흐름을 결정한다. 코로나 [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 전파 경로 추적, SNS 허위정보 확산 패턴, 기업 내 비공식 협업 네트워크—이 모든 문제는 SNA로 접근할 때 새로운 인사이트를 얻을 수 있다.

수십억 명의 페이스북·링크드인·카카오 사용자 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망은 기존의 행렬 기반 분석으로는 처리할 수 없는 초대형 스파스 (Sparse) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)다. 빅데이터 기술과 SNA의 결합이 필요한 이유다.

- **📢 섹션 요약 비유**: SNA는 인간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망의 X-레이다. 겉으로 드러나지 않는 연결 구조와 영향력의 흐름을 투명하게 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SNA 분석 구조 및 주요 개념</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드 A 노드 B 노드 D</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\</div><div class="kb-diagram-cell">중심성 지표:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\</div><div class="kb-diagram-cell">A: Degree=3 (연결 많음)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드 C \ 노드 E B: Betweenness 높음 (다리 역할)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\ E: Eigenvector 높음 (영향력)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드 F</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">커뮤니티 탐지: {A,B,C} ←→ {D,E,F} (모듈러리티 최적화)</div></div>
</div>
</div>



### 핵심 중심성 지표

| 지표 | 수식/원리 | 의미 | 활용 |
|:---|:---|:---|:---|
| <strong>연결 중심성 (Degree <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/383_graph_mining_centrality_metrics/">Centrality</a>)</strong> | 노드의 직접 연결 수 / (N-1) | 가장 많이 연결된 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) | 슈퍼 커넥터 발굴 |
| <strong>매개 중심성 (Betweenness <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/383_graph_mining_centrality_metrics/">Centrality</a>)</strong> | 노드를 통과하는 최단 경로 비율 | 정보 흐름의 병목/다리 | 핵심 브로커 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) |
| <strong>근접 중심성 (Closeness <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/383_graph_mining_centrality_metrics/">Centrality</a>)</strong> | 다른 모든 노드까지의 평균 거리 역수 | 정보 빠르게 전파 가능 | 전파 효율 분석 |
| <strong>고유벡터 중심성 (Eigenvector <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/383_graph_mining_centrality_metrics/">Centrality</a>)</strong> | 연결된 이웃의 중심성 가중 합 | 영향력 있는 노드와 연결 | PageRank의 기반 |

### 커뮤니티 탐지 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 원리 | 복잡도 | 특징 |
|:---|:---|:---|:---|
| **Louvain** | [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러리티 (Modularity) 최적화 | O(n log n) | 대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에 실용적, 계층적 |
| **Girvan-Newman** | 매개 중심성 높은 엣지 순차 제거 | O(m²n) | 계층적 분해, 대규모에 느림 |
| **Label Propagation** | 이웃 레이블 다수결 전파 | O(n+m) | 가장 빠름, 비결정적 |
| <strong>Spectral <a href="/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/">Clustering</a></strong> | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 라플라시안 고유벡터 | O(n³) | 수학적으로 정교, 소규모 |

- **📢 섹션 요약 비유**: 중심성은 도시에서 교통의 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)를 찾는 것과 같다. 연결 중심성은 가장 많은 도로가 만나는 교차로, 매개 중심성은 다른 도시로 가려면 반드시 거쳐야 하는 분기점이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [SNA](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) | [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB |
|:---|:---|:---|:---|
| **목적** | 구조·영향력 분석 | 개인화 추천 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **출력** | 중심성 지표, 커뮤니티 | 추천 아이템 목록 | Cypher/Gremlin [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 결과 |
| **처리 방식** | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [행렬 분해](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/)·[GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 순회 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **대표 도구** | NetworkX, Gephi | Spark ALS | Neo4j, Amazon Neptune |

SNA와 [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) ([Graph Analytics](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/))은 개념적으로 겹치지만, SNA는 사회 과학적 맥락에서 행위자 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 중심으로 보고, [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/)은 더 일반적인 구조 (도로망·물류·전력망)에 적용된다.

- **📢 섹션 요약 비유**: SNA는 "사람들의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)"를 보는 사회학자의 렌즈이고, [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/)은 "어떤 연결이든" 다루는 수학자의 렌즈다. 같은 도구를 다른 목적으로 사용하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. **인플루언서 마케팅**: 고유벡터 중심성·매개 중심성이 높은 노드 = 최적 바이럴 시드 (Seed) 선정
2. **사기 네트워크 탐지**: 금융 거래 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 밀집 커뮤니티 = 공모 거래 그룹 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)
3. **역학 조사**: 감염병 전파 경로 추적, 슈퍼스프레더 (Super-Spreader) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)
4. **조직 분석**: 이메일·슬랙 커뮤니케이션 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 비공식 협업 네트워크 파악

### 빅데이터 처리 도구

| 도구 | 특징 | 처리 규모 |
|:---|:---|:---|
| **NetworkX (Python)** | 프로토타이핑·연구, 단일 머신 | 수백만 노드 |
| **Gephi** | [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 특화, 인터랙티브 | 수십만 노드 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">Apache Spark</a> GraphX</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리, Pregel [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 수십억 노드 |
| **TigerGraph** | 실시간 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) DB | 수십억 노드, 실시간 |
| **Amazon Neptune** | 관리형 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB (RDF+Property [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) | 클라우드 스케일 |

- **📢 섹션 요약 비유**: 수억 명의 소셜 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 노트북으로 분석하려는 것은 자동차로 태평양을 건너려는 것과 같다. 규모에 맞는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 플랫폼 선택이 [SNA](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) 프로젝트의 성패를 가른다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 핵심 인물 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 마케팅·보안·조직 관리에서 핵심 노드 자동 발굴 |
| 허위정보 추적 | 가짜뉴스 확산 경로와 최초 전파자 역추적 |
| 사기·범죄 탐지 | 공모 집단의 네트워크 패턴 자동 탐지 |
| 조직 효율화 | 정보 병목 및 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) ([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 구조 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)로 협업 개선 |
| 역학·방역 | 감염병 전파 시뮬레이션 및 고위험 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 우선 관리 |

SNA는 개인이 아닌 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 가치를 만든다는 통찰에서 출발한다. 빅데이터 시대에 소셜 플랫폼의 폭발적 성장은 수십억 노드의 초거대 네트워크를 분석 대상으로 만들었고, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 기술의 발전이 이를 가능하게 했다. 앞으로 SNA는 [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) ([Graph Neural Network](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/))과 결합하여 링크 예측·노드 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 등 더 정교한 예측 모델로 진화할 것이다.

- **📢 섹션 요약 비유**: SNA는 사람들이 어떻게 연결돼 있는지 지도를 그리는 것이다. 지도가 있어야 가장 빠른 길도, 막힌 길도, 가장 중요한 교차로도 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 이론 ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) Theory) | SNA의 수학적 기반 |
| 중심성 지표 ([Centrality](/knowledge-base/studynote/06_ict_convergence/05_data_science/383_graph_mining_centrality_metrics/) Measures) | 노드 중요도 측정 핵심 도구 |
| 커뮤니티 탐지 (Community [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) | 숨겨진 집단 구조 발굴 |
| PageRank | 고유벡터 중심성의 실용적 응용 (구글 검색) |
| [GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) ([Graph Neural Network](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/)) | [SNA](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) + 딥러닝 결합의 최신 트렌드 |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) GraphX | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 |
| Louvain [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 대규모 커뮤니티 탐지 표준 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">네트워크 그래프 구성 (Network Graph) — 노드(행위자)와 엣지(관계) 모델링</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">중심성 분석 (Centrality Analysis) — 연결·매개·근접 중심성으로 핵심 노드 탐지</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">커뮤니티 탐지 (Community Detection) — Louvain·Girvan-Newman으로 그룹 식별</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">영향력 확산 모델 (Diffusion Model) — SIR·IC 모델로 정보·전파 시뮬레이션</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프 머신러닝 (GNN — Graph Neural Network) — 관계 구조 학습으로 추천·예측</div></div>
</div>
</div>



이 흐름은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구축에서 중심성 분석·커뮤니티 탐지·GNN까지 [소셜 네트워크 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) 기술이 진화하는 경로를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
- SNA는 반 친구들의 사이좋은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 선으로 그려서 누가 제일 인기 많고, 어떤 무리가 있는지 알아내는 거예요.
- 매개 중심성이 높은 친구는 여러 무리 사이를 연결해주는 다리 역할을 하는 중요한 친구예요.
- 페이스북 같은 SNS에서 수억 명의 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이런 방식으로 분석해서 바이럴이나 사기를 탐지해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 110 / 262

← **이전**: [106. 텍스트 마이닝 (Text Mining) — TF-IDF/Word2Vec/BERT 기반 텍스트 분석](/knowledge-base/studynote/16_bigdata/05_analysis/109_text_mining/)
**다음**: [108. 이상 탐지 (Anomaly Detection) — 통계/ML/딥러닝 기반 이상치 감지](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/) →

---
