+++
title = "159. GNN (Graph Neural Network) 그래프 노드 메시지 패싱 네트워크"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GNN ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) Neural Network, [그래프 신경망](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/306_graph_neural_network_gnn/))은 메시지 패싱([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 메커니즘으로 이웃 노드의 정보를 반복적으로 집계해 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 노드·엣지·[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 수준 표현을 학습한다.
> 2. **가치**: SNS [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망, 분자 구조, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/), [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)처럼 "[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)"가 핵심인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)/RNN이 처리할 수 없는 비유클리드 구조를 처리한다.
> 3. **판단 포인트**: GCN ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) Convolutional Network)은 정적 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에, GraphSAGE는 동적·대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에, [GAT](/knowledge-base/studynote/10_ai/05_data_science_ml/398_gat/) ([Graph Attention Network](/knowledge-base/studynote/10_ai/05_data_science_ml/398_gat/))은 엣지 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 학습이 필요할 때 선택한다.

## Ⅰ. 개요 및 필요성

일반 딥러닝은 격자(이미지) 또는 시퀀스(텍스트) 구조를 처리한다. 하지만 소셜 네트워크, 단백질 상호작용, 도로 네트워크, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)는 불규칙한 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조다.

[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) G = (V, E) — V는 노드(Node), E는 엣지(Edge)
- 노드: 사람, 원자, 도시, 개체
- 엣지: 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 화학 결합, 도로, 의미 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

📢 **섹션 요약 비유**: GNN은 친구 네트워크에서 "내 친구들의 특성을 종합해서 나를 이해"하는 방식이다. 혼자보다 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망 전체로 나를 설명한다.

## Ⅱ. 아키텍처 및 핵심 원리

| 개념 | 수식/설명 |
|:---|:---|
| 메시지 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | mᵤᵥ = M(hᵤ, hᵥ, eᵤᵥ) |
| 집계 (Aggregation) | aᵥ = [Aggregate](/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)({mᵤᵥ | u ∈ N(v)}) |
| 업데이트 (Update) | h'ᵥ = Update(hᵥ, aᵥ) |
| 반복 (K 회) | K 레이어 = K-hop 이웃 정보 통합 |
| 읽기 (Readout) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 수준: hG = Readout({h'ᵥ}) |

```
[GNN 메시지 패싱 과정]

초기 그래프:
    A───B
    │   │
    C───D

Layer 1 (1-hop 이웃 집계):
  h'A = Update(hA, Agg({hB, hC}))
  h'B = Update(hB, Agg({hA, hD}))
  h'C = Update(hC, Agg({hA, hD}))
  h'D = Update(hD, Agg({hB, hC}))

Layer 2 (2-hop 이웃 정보까지):
  h''A는 이제 B,C를 통해 D의 정보까지 반영

[GCN - Graph Convolutional Network]
h'ᵥ = σ(Σᵤ∈N(v)∪{v} (1/√(dᵤdᵥ)) · Wh_u)
dᵥ: 노드 v의 차수 (연결 수)
→ 정규화된 스펙트럼 합성곱

[GAT - Graph Attention Network]
이웃 중요도에 어텐션 가중치 α_uv 부여:
h'ᵥ = σ(Σᵤ∈N(v) α_uv · Wh_u)
α_uv = softmax(LeakyReLU(a^T[Wh_v || Wh_u]))
```

**주요 GNN 아키텍처**

| 모델 | 핵심 차이 | 적합 사용 |
|:---|:---|:---|
| GCN (2017) | 스펙트럼 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 정적 소규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| GraphSAGE (2017) | 미니배치 이웃 샘플링 | 대규모 동적 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| [GAT](/knowledge-base/studynote/10_ai/05_data_science_ml/398_gat/) (2018) | 어텐션 기반 이웃 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 이웃 중요도 다를 때 |
| GIN (2019) | 단사(Injective) 집계 | 구조 이소모피즘 |
| PNA (2020) | 다중 [집계 함수](/knowledge-base/studynote/05_database/03_relational_model/147_aggregate_function_group_by/) 결합 | 범용 고성능 |

📢 **섹션 요약 비유**: GCN은 모든 친구의 의견을 동등하게 듣는 것, GAT는 더 가까운 친구의 의견에 더 많은 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 주는 것이다.

## Ⅲ. 비교 및 연결

| 항목 | [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/) | [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) | GNN |
|:---|:---|:---|:---|
| 처리 구조 | 격자 (이미지) | 시퀀스 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망) |
| 이웃 정의 | 픽셀 인근 | 시간 인접 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 엣지 |
| 크기 가변 | ❌ 고정 | ✅ 가변 시퀀스 | ✅ 가변 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| 위치 불변 | ✅ (같은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) | ❌ | ✅ (순열 불변) |

**GNN 활용 분야**
- [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/): Pinterest PinSage (사용자-핀 이분 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/))
- 약물 발견: 분자 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 특성 예측
- 사기 탐지: 금융 거래 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)망 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)
- [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/): [GraphRAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/530_graph_rag/) 지식 추론
- 교통 예측: 도로 네트워크 혼잡 예측

📢 **섹션 요약 비유**: GNN은 "혼자로는 이해할 수 없지만, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 속에서 이해되는" 개체들을 처리하는 AI다.

## Ⅳ. 실무 적용 및 기술사 판단

**대규모 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**
- Mini-batch 샘플링 (GraphSAGE): 전체 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 대신 이웃 샘플링
- 클러스터 GCN: [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 부분 클러스터로 나눠 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)
- GraphSAINT: 중요도 샘플링 기반

**이기종 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Heterogeneous](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/) [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))**
- 노드 타입, 엣지 타입이 다양한 현실 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)
- HGT ([Heterogeneous](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/) [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)): 타입별 독립 파라미터

**기술사 출제 포인트**
- "GNN의 메시지 패싱 메커니즘을 설명하고, GCN/GAT의 차이를 설명하시오"
- "GNN이 기존 딥러닝([CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/), [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/))으로 처리하지 못하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 설명하시오"

📢 **섹션 요약 비유**: GNN은 혼자서는 의미 없지만, [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 속에서 의미를 갖는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 "[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"다. 원자 하나가 아닌 분자 구조 전체를 이해한다.

## Ⅴ. 기대효과 및 결론

GNN은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 폭발적 증가(소셜 미디어, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/), 분자 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))와 함께 중요성이 커졌다. 알파폴드(AlphaFold)의 단백질 구조 예측, Google 지도의 교통 예측, 메타의 소셜 추천 모두 GNN 기반이다. [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)와 결합한 GraphRAG는 LLM의 추론 능력을 구조화된 지식으로 강화한다.

📢 **섹션 요약 비유**: GNN은 AI에게 "[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 읽기" 능력을 준 것이다. 점이 아닌 네트워크 전체로 세상을 이해하게 됐다.

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) G=(V,E) | 노드, 엣지 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| 핵심 | 메시지 패싱 | 이웃 정보 집계 |
| 아키텍처 | GCN | 스펙트럼 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) |
| 아키텍처 | [GAT](/knowledge-base/studynote/10_ai/05_data_science_ml/398_gat/) ([Graph Attention Network](/knowledge-base/studynote/10_ai/05_data_science_ml/398_gat/)) | 어텐션 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) |
| 확장 | GraphSAGE | 대규모 샘플링 |
| 응용 | [GraphRAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/530_graph_rag/) | [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) + [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) |

### 👶 어린이를 위한 3줄 비유 설명
1. GNN은 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이용해 "이 사람이 어떤 사람인지"를 알아내는 AI예요.
2. 나의 친구, 친구의 친구, 그 친구의 친구까지 정보를 모아서 판단해요.
3. 분자, 소셜 네트워크, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)처럼 연결이 중요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 이해하는 데 탁월해요.

### 📈 관련 키워드 및 발전 흐름도

```text
그래프 구조 데이터 (노드 + 엣지)
    │
    ▼
메시지 패싱 (Message Passing)
    노드가 이웃 노드의 특성을 집계 → 자기 표현 업데이트
    │
    ▼
GNN 변형
    ├─► GCN (Graph Convolutional Network)
    ├─► GAT (Graph Attention Network) — Attention 가중치
    └─► GraphSAGE — 이웃 샘플링, 인덕티브 학습
    │
    ▼
응용: 분자 속성 예측 · 소셜 커뮤니티 · 추천 시스템
    │
    ▼
GraphRAG — 지식 그래프 + LLM 결합
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 159 / 258

← **이전**: [158. 멀티모달 (Multimodal) 비전/오디오 동시 인코딩 CLIP](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/)
**다음**: [160. 지식 그래프 (Knowledge Graph) + GraphRAG 연동망](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) →

---
