---
title: 159. GNN (Graph Neural Network) 그래프 노드 메시지 패싱 네트워크
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GNN ([[104_graph|Graph]] Neural Network, [[306_graph_neural_network_gnn|그래프 신경망]])은 메시지 패싱([[119_message_passing|Message Passing]]) 메커니즘으로 이웃 노드의 정보를 반복적으로 집계해 [[070_graph_datastructure|그래프]] 구조 [[001_dikw_pyramid|데이터]]의 노드·엣지·[[070_graph_datastructure|그래프]] 수준 표현을 학습한다.
> 2. **가치**: SNS [[083_relationship_in_er_model|관계]]망, 분자 구조, [[160_knowledge_graph_graphrag_integration|지식 그래프]], [[211_recommendation_system|추천 시스템]]처럼 "[[083_relationship_in_er_model|관계]]"가 핵심인 [[001_dikw_pyramid|데이터]]에서 [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]/RNN이 처리할 수 없는 비유클리드 구조를 처리한다.
> 3. **판단 포인트**: GCN ([[104_graph|Graph]] Convolutional Network)은 정적 [[070_graph_datastructure|그래프]]에, GraphSAGE는 동적·대규모 [[070_graph_datastructure|그래프]]에, [[398_gat|GAT]] ([[398_gat|Graph Attention Network]])은 엣지 [[267_weight_bias_activation|가중치]] 학습이 필요할 때 선택한다.

## Ⅰ. 개요 및 필요성

일반 딥러닝은 격자(이미지) 또는 시퀀스(텍스트) 구조를 처리한다. 하지만 소셜 네트워크, 단백질 상호작용, 도로 네트워크, [[160_knowledge_graph_graphrag_integration|지식 그래프]]는 불규칙한 [[070_graph_datastructure|그래프]] 구조다.

[[070_graph_datastructure|그래프]] G = (V, E) — V는 노드(Node), E는 엣지(Edge)
- 노드: 사람, 원자, 도시, 개체
- 엣지: 친구 [[083_relationship_in_er_model|관계]], 화학 결합, 도로, 의미 [[083_relationship_in_er_model|관계]]

📢 **섹션 요약 비유**: GNN은 친구 네트워크에서 "내 친구들의 특성을 종합해서 나를 이해"하는 방식이다. 혼자보다 [[083_relationship_in_er_model|관계]]망 전체로 나를 설명한다.

## Ⅱ. 아키텍처 및 핵심 원리

| 개념 | 수식/설명 |
|:---|:---|
| 메시지 [[087_process_state_transition|생성]] | mᵤᵥ = M(hᵤ, hᵥ, eᵤᵥ) |
| 집계 (Aggregation) | aᵥ = [[222_aggregate_ddd_transaction_consistency|Aggregate]]({mᵤᵥ | u ∈ N(v)}) |
| 업데이트 (Update) | h'ᵥ = Update(hᵥ, aᵥ) |
| 반복 (K 회) | K 레이어 = K-hop 이웃 정보 통합 |
| 읽기 (Readout) | [[070_graph_datastructure|그래프]] 수준: hG = Readout({h'ᵥ}) |

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
| GCN (2017) | 스펙트럼 [[228_cnn_1d_2d_3d_video_medical|합성곱]], [[093_normalization|정규화]] | 정적 소규모 [[070_graph_datastructure|그래프]] |
| GraphSAGE (2017) | 미니배치 이웃 샘플링 | 대규모 동적 [[070_graph_datastructure|그래프]] |
| [[398_gat|GAT]] (2018) | 어텐션 기반 이웃 [[267_weight_bias_activation|가중치]] | 이웃 중요도 다를 때 |
| GIN (2019) | 단사(Injective) 집계 | 구조 이소모피즘 |
| PNA (2020) | 다중 [[147_aggregate_function_group_by|집계 함수]] 결합 | 범용 고성능 |

📢 **섹션 요약 비유**: GCN은 모든 친구의 의견을 동등하게 듣는 것, GAT는 더 가까운 친구의 의견에 더 많은 [[267_weight_bias_activation|가중치]]를 주는 것이다.

## Ⅲ. 비교 및 연결

| 항목 | [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] | GNN |
|:---|:---|:---|:---|
| 처리 구조 | 격자 (이미지) | 시퀀스 | [[070_graph_datastructure|그래프]] ([[083_relationship_in_er_model|관계]]망) |
| 이웃 정의 | 픽셀 인근 | 시간 인접 | [[070_graph_datastructure|그래프]] 엣지 |
| 크기 가변 | ❌ 고정 | ✅ 가변 시퀀스 | ✅ 가변 [[070_graph_datastructure|그래프]] |
| 위치 불변 | ✅ (같은 [[022_kernel_role|커널]]) | ❌ | ✅ (순열 불변) |

**GNN 활용 분야**
- [[211_recommendation_system|추천 시스템]]: Pinterest PinSage (사용자-핀 이분 [[070_graph_datastructure|그래프]])
- 약물 발견: 분자 [[070_graph_datastructure|그래프]] 특성 예측
- 사기 탐지: 금융 거래 [[083_relationship_in_er_model|관계]]망 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
- [[160_knowledge_graph_graphrag_integration|지식 그래프]]: [[530_graph_rag|GraphRAG]] 지식 추론
- 교통 예측: 도로 네트워크 혼잡 예측

📢 **섹션 요약 비유**: GNN은 "혼자로는 이해할 수 없지만, [[083_relationship_in_er_model|관계]] 속에서 이해되는" 개체들을 처리하는 AI다.

## Ⅳ. 실무 적용 및 기술사 판단

**대규모 [[070_graph_datastructure|그래프]] 처리 [[268_strategy_pattern|전략]]**
- Mini-batch 샘플링 (GraphSAGE): 전체 [[070_graph_datastructure|그래프]] 대신 이웃 샘플링
- 클러스터 GCN: [[070_graph_datastructure|그래프]]를 부분 클러스터로 나눠 [[228_batch_processing_hadoop_spark|배치 처리]]
- GraphSAINT: 중요도 샘플링 기반

**이기종 [[070_graph_datastructure|그래프]] ([[273_heterogeneous_db|Heterogeneous]] [[104_graph|Graph]])**
- 노드 타입, 엣지 타입이 다양한 현실 [[070_graph_datastructure|그래프]]
- HGT ([[273_heterogeneous_db|Heterogeneous]] [[104_graph|Graph]] [[246_transformer_self_attention_parallel_positional_encoding|Transformer]]): 타입별 독립 파라미터

**기술사 출제 포인트**
- "GNN의 메시지 패싱 메커니즘을 설명하고, GCN/GAT의 차이를 설명하시오"
- "GNN이 기존 딥러닝([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]], [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]])으로 처리하지 못하는 [[001_dikw_pyramid|데이터]] 구조를 설명하시오"

📢 **섹션 요약 비유**: GNN은 혼자서는 의미 없지만, [[083_relationship_in_er_model|관계]] 속에서 의미를 갖는 [[001_dikw_pyramid|데이터]]를 처리하는 "[[083_relationship_in_er_model|관계]] [[190_ai_llm_requirements_specification|AI]]"다. 원자 하나가 아닌 분자 구조 전체를 이해한다.

## Ⅴ. 기대효과 및 결론

GNN은 [[083_relationship_in_er_model|관계]] [[001_dikw_pyramid|데이터]]의 폭발적 증가(소셜 미디어, [[160_knowledge_graph_graphrag_integration|지식 그래프]], 분자 [[002_database_definition|데이터베이스]])와 함께 중요성이 커졌다. 알파폴드(AlphaFold)의 단백질 구조 예측, Google 지도의 교통 예측, 메타의 소셜 추천 모두 GNN 기반이다. [[160_knowledge_graph_graphrag_integration|지식 그래프]]와 결합한 GraphRAG는 LLM의 추론 능력을 구조화된 지식으로 강화한다.

📢 **섹션 요약 비유**: GNN은 AI에게 "[[083_relationship_in_er_model|관계]] 읽기" 능력을 준 것이다. 점이 아닌 네트워크 전체로 세상을 이해하게 됐다.

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 구조 | [[070_graph_datastructure|그래프]] G=(V,E) | 노드, 엣지 [[083_relationship_in_er_model|관계]] |
| 핵심 | 메시지 패싱 | 이웃 정보 집계 |
| 아키텍처 | GCN | 스펙트럼 [[228_cnn_1d_2d_3d_video_medical|합성곱]] |
| 아키텍처 | [[398_gat|GAT]] ([[398_gat|Graph Attention Network]]) | 어텐션 [[267_weight_bias_activation|가중치]] |
| 확장 | GraphSAGE | 대규모 샘플링 |
| 응용 | [[530_graph_rag|GraphRAG]] | [[160_knowledge_graph_graphrag_integration|지식 그래프]] + [[263_llm_large_language_model|LLM]] |

### 👶 어린이를 위한 3줄 비유 설명
1. GNN은 친구 [[083_relationship_in_er_model|관계]]를 이용해 "이 사람이 어떤 사람인지"를 알아내는 AI예요.
2. 나의 친구, 친구의 친구, 그 친구의 친구까지 정보를 모아서 판단해요.
3. 분자, 소셜 네트워크, [[160_knowledge_graph_graphrag_integration|지식 그래프]]처럼 연결이 중요한 [[001_dikw_pyramid|데이터]]를 이해하는 데 탁월해요.

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

← **이전**: [[158_multimodal_clip_vision_audio_encoding|158. 멀티모달 (Multimodal) 비전/오디오 동시 인코딩 CLIP]]
**다음**: [[160_knowledge_graph_graphrag_integration|160. 지식 그래프 (Knowledge Graph) + GraphRAG 연동망]] →

---
