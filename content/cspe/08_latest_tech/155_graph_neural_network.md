---
title: "그래프 신경망 (Graph Neural Network)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 155
---

# 📖 【암기용】 개념 완전 이해

> 목적: Graph Neural Network를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 노드와 엣지로 구성된 그래프 구조에서 이웃 정보를 전파·집계해 예측을 수행하는 신경망
- **왜 필요한가**: 소셜 네트워크, 지식그래프, 분자 구조, 서비스 의존성처럼 관계 자체가 핵심인 데이터가 많음.
- **핵심 직관**: 한 사람의 특성만 보지 않고 친구와 친구의 친구 정보까지 모아 그 사람을 이해하는 모델임.

## 깊이 이해
- **배경·문제의식**: CNN은 격자 이미지, RNN은 순서 데이터에 적합하지만 그래프는 이웃 수와 연결 구조가 불규칙하다.
- **작동 원리**: 각 노드는 자신의 feature와 이웃 노드 feature를 메시지로 주고받고, aggregation과 update를 반복해 관계를 반영한 embedding을 만든다.
- **비유**: 팀원의 평판을 평가할 때 본인 정보뿐 아니라 함께 일한 동료들의 평가와 관계를 함께 반영하는 방식임.
- **구체 예시**: 이상 거래 탐지에서 계좌 노드와 송금 엣지를 GNN으로 학습해 2-hop 거래 패턴 기반 사기 후보를 탐지.
- **흔한 오해·주의점**: 깊은 GNN은 모든 노드 표현이 비슷해지는 over-smoothing 문제가 발생할 수 있어 2~3 layer와 residual을 사용함.

## 연결 개념
- Graph Transformer — attention으로 그래프 관계를 학습하는 모델
- Knowledge Graph — GNN의 입력 데이터가 될 수 있는 구조화 지식
- Message Passing — GNN의 핵심 이웃 정보 전파 원리

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GNN은 그래프의 노드·엣지 관계를 메시지 패싱으로 반영해 embedding과 예측을 수행함.
> 2. **가치**: 관계 패턴이 중요한 추천, 이상탐지, 지식그래프, 분자 예측에서 비정형 연결 정보를 활용함.
> 3. **판단 포인트**: over-smoothing, 대규모 그래프 샘플링, 동적 그래프 갱신을 설계해야 함.

## Ⅰ. 개요 및 필요성

GNN은 그래프 구조 데이터를 학습하는 신경망이다. 관계 데이터는 노드 특성보다 연결 패턴이 예측에 중요하다. GNN은 이웃 노드 정보를 반복 집계해 관계 기반 표현을 생성한다.

## Ⅱ. 구조 및 구성요소

```text
Graph(V,E,X) → Message Passing → Aggregation
  → Node Embedding → Task Head(Node/Edge/Graph)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Node/Edge Feature | 그래프 입력 특성 | 사용자, 상품, 계좌, 관계 |
| Message Function | 이웃 노드 정보 전달 | edge weight 반영 |
| Aggregation | 이웃 메시지 집계 | mean, sum, attention |
| Task Head | 예측 수행 | node classification, link prediction |

> 요약: GNN은 노드·엣지 특징을 메시지 패싱과 집계로 통합해 태스크별 예측을 수행함.

## Ⅲ. 동작원리 및 흐름도

```text
그래프 입력 → 이웃 샘플링 → 메시지 계산
  → aggregation/update 반복 → embedding 생성 → 예측
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 그래프와 노드·엣지 feature 구성 | 결측 feature <1% |
| 2 | 1~3 hop 이웃 샘플링 | fanout 10~25 |
| 3 | message passing과 aggregation | over-smoothing 지표 관리 |
| 4 | 노드·링크·그래프 예측 | AUC ≥0.85 또는 F1 목표 |

> 요약: GNN은 이웃 정보를 hop 단위로 집계해 관계가 반영된 embedding을 만들고 예측에 사용함.

## Ⅳ. 특징

| 구분 | MLP | GNN | 판단 포인트 |
|:---|:---|:---|:---|
| 입력 구조 | 독립 샘플 | 노드·엣지 그래프 | 관계 데이터는 GNN |
| 정보 활용 | 개별 feature | 이웃·경로·구조 | 2~3 hop 패턴 활용 |
| 확장성 | 단순 배치 | 샘플링·분산 필요 | 대규모 그래프 설계 |
| 한계 | 관계 미반영 | over-smoothing·cold start | residual·feature 보완 |

> 요약: GNN은 관계 패턴을 활용하지만 대규모 학습과 과도한 이웃 집계 문제를 통제해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 사기 탐지: 계좌-거래 그래프에서 2-hop 송금 패턴을 GNN으로 학습, AUC 0.85 이상 기준 운영
2. 추천 시스템: 사용자-아이템 bipartite graph에 GraphSAGE 적용, cold start는 콘텐츠 feature로 보완
3. 지식그래프 분석: KG link prediction으로 누락 관계 후보를 생성하고 신뢰도 0.8 이상만 검토 큐 반영

**결론 (2줄):**
- 기술사 판단: 관계 구조가 예측 핵심이면 GNN, 독립 표 데이터는 XGBoost/MLP 우선 적용
- 향후 방향: Graph Transformer와 Graph RAG 결합으로 관계 추론과 생성형 AI 연계가 강화됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GNN을 설명하시오" | 메시지 패싱→집계→embedding→예측 흐름 | MLP 대비 관계 활용 차이 |
| 요구사항 명시형 | "관계 데이터 분석 방안을 제시하시오" | 이웃 샘플링·over-smoothing 통제 | 사기탐지·추천·KG 적용 기준 |

> 요약: 설명형은 그래프 학습 원리, 방안형은 관계 데이터 적용과 확장성 통제를 중심으로 작성함.
