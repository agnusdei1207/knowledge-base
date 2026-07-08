---
title: "Graph Transformer (Graph Transformer)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 156
extra:
  question_no: "156"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Graph Transformer는 그래프에 transformer attention을 적용한 전역 관계 학습 모델임
- 구조적 positional encoding이 없으면 단순 self-attention만으로 그래프 위상을 이해하기 어려움
- 장거리 상호작용이 중요한 분자와 코드 그래프에서 특히 유리함

## Ⅰ. 개요

- **정의/개념**: Graph Transformer는 그래프 노드와 간선 표현에 구조적 위치 인코딩을 결합하고, 전역 self-attention으로 노드 간 장거리 상호작용을 학습해 예측을 수행하는 그래프 신경망 계열임
- **배경/필요성**: message passing 기반 GNN은 멀리 떨어진 노드 관계를 포착하려면 레이어를 깊게 쌓아야 하므로 정보 병목과 평활화 한계가 생겨, 전역 관계를 직접 보는 구조가 필요했음

## Ⅱ. 특징

- 전역 attention으로 장거리 의존성과 비국소 관계를 직접 모델링함
- shortest path나 centrality 같은 구조 인코딩이 모델 품질을 크게 좌우함
- 분자와 코드처럼 구조 전체 맥락이 중요한 그래프에 강함
- 노드 수가 커질수록 $O(N^2)$ attention 비용이 크게 증가함

## Ⅲ. 종류 및 비교

| 판단 기준 | Message Passing GNN | GAT | Graph Transformer |
|:---|:---|:---|:---|
| 정보 범위 | 로컬 중심 | 로컬 중심 | 전역 중심 |
| 장거리 관계 포착 | 낮음 | 중간 | 높음 |
| 연산 비용 | 낮음 | 중간 | 높음 |
| 대규모 그래프 적합성 | 높음 | 중간 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Node, Edge Embedding | 노드와 간선의 속성을 초기 임베딩으로 변환해 attention 입력을 구성함 |
| Structural Encoding | 최단 경로와 중심성 같은 위상 정보를 주입해 그래프 내 위치 감각을 부여함 |
| Global Self-Attention | 모든 노드 간 상호작용을 계산해 장거리 관계를 직접 반영함 |
| Readout, Prediction Head | 전역 표현을 모아 그래프나 노드 수준 예측 결과를 생성함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Node/Edge Embed   | ---> | Structural Enc.   | ---> | Global Attention  |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Readout / Predict |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 그래프 임베딩화   | --> | 구조 정보 주입  | --> | 전역 attention   | --> | 예측/평가 수행  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **그래프 임베딩화**: 노드와 간선을 임베딩 표현으로 변환함
2. **구조 정보 주입**: 위상 정보를 positional bias로 추가함
3. **전역 attention 수행**: 모든 노드 간 중요도를 계산함
4. **예측 및 평가 수행**: 전역 표현으로 최종 예측을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 노드 수가 조금만 커져도 전역 attention 비용이 급증해 메모리와 학습 시간이 병목이 될 수 있음
   - 해결방안: sparse attention과 subgraph batching을 적용하고 memory footprint와 throughput으로 검증함
2. 문제: 구조 인코딩이 부정확하거나 단순하면 그래프 위상을 충분히 반영하지 못해 attention의 장점이 사라질 수 있음
   - 해결방안: shortest-path bias와 Laplacian encoding을 비교 적용하고 validation MAE와 structural probe score로 검증함
3. 문제: 전역 관계에 치우치면 가까운 이웃의 강한 로컬 패턴을 오히려 약하게 반영할 수 있음
   - 해결방안: local-global hybrid layer를 적용하고 local task accuracy와 long-range accuracy를 함께 검증함

## Ⅶ. 적용 사례

- 분자 물성 예측이 장거리 원자 상호작용을 학습하도록 Graph Transformer를 적용하며 확인 지표는 MAE와 hit rate임
- 프로그램 분석이 제어 흐름 그래프의 전역 의존성을 파악하도록 Graph Transformer를 운영하며 확인 지표는 bug detection precision과 recall임
- 지식 그래프 추론이 멀리 떨어진 개체 관계를 반영하도록 Graph Transformer를 활용하며 확인 지표는 link prediction MRR과 accuracy임

## Ⅷ. 결론

Graph Transformer는 그래프의 전역 상호작용을 직접 다루는 강력한 구조이므로, 구조 인코딩 설계와 attention 비용 제어가 실무 도입의 핵심 판단 기준임.
