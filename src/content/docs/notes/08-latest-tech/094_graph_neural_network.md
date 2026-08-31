---
sidebar:
  order: 94
  label: "094. 그래프 신경망 (Graph Neural Network)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "그래프 신경망 (Graph Neural Network)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest_tech"
weight: 94
extra:
  question_no: "094"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "그래프 관계 학습이 최신 AI 구조 쟁점"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **그래프 신경망(Graph Neural Network, GNN)**: 그래프 위상과 특징을 메시지 전달로 학습한다.
- **간선 관계(Edge Relation)**: 두 노드 관계의 유형•강도•방향 정보이다.

</details>

- 정의/개념: 이웃 특징을 집계해 관계를 표현하는 **GNN**
- 배경/필요성: 전통적인 심층 신경망(CNN, RNN, Transformer)은 유클리드 공간의 격자형(Grid) 이미지나 1차원 순차(Sequential) 텍스트 데이터 처리에 최적화되어 있어, 금융 이상 거래 탐지, 소셜 네트워크, 분자 구조(단백질/화합물), 지식 그래프 등 현실 세계의 비유클리드 공간(Non-Euclidean Space)에 존재하는 복잡한 위상 구조(Topology)와 불규칙한 다대다 관계를 효과적으로 학습할 수 없는 근본적 한계가 존재함에 따라, 그래프의 노드(Node)와 간선(Edge)의 구조적 정보를 메시지 전달(Message Passing / Neighborhood Aggregation) 메커니즘을 통해 이웃 노드 간에 전파·집계하여 저차원 노드/그래프 임베딩을 생성하는 그래프 신경망(Graph Neural Network: GNN / GCN, GraphSAGE, GAT / Message Passing Neural Network: MPNN) 아키텍처를 도입하여 **그래프 위상 구조와 노드 속성 정보를 동시에 반영하는 강력한 관계 중심 표현 학습(Representation Learning) 달성, 노드 분류(Node Classification), 링크 예측(Link Prediction), 그래프 수준 분류/생성 과업의 획기적 정확도 제고, 대규모 동적 이기종 그래프에 대한 귀납적(Inductive) 학습 능력 확보**를 달성할 필요

#### 한줄 요약

- **그래프 위상•이웃 특징** 기반 구조적 관계 학습

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **메시지 전달(Message Passing)**: 이웃 특징을 계산•전달해 노드 상태를 갱신한다.
- **과평활(Over-smoothing)**: 깊은 층에서 노드 표현이 유사해지는 현상이다.
- **과압축(Over-squashing)**: 많은 관계 정보가 고정 벡터에 압축돼 손실되는 현상이다.

</details>

- 이웃 특징을 계산•전달하는 **메시지 전달**
- 이웃 순서와 무관한 **순서 불변 집계**
- 깊은 전파의 **과평활•과압축** 위험

#### 한줄 요약

- **메시지 전달•순서 불변 집계•전파 깊이** 표현 결정

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **집계 함수(Aggregation Function)**: 이웃 메시지를 순서와 무관하게 결합한다.
- **갱신 함수(Update Function)**: 현재 상태와 집계값으로 표현을 갱신한다.
- **읽기 함수(Readout Function)**: 노드 표현을 과업별 결과로 변환한다.

</details>

```text
[특징 저장소]──[메시지 함수]──[집계 함수]
                                  │
                            [갱신 함수]──[읽기 함수]
```

선의 의미: 특징•메시지•집계•갱신•읽기 책임의 정적 연결

| 구성요소 | 책임 |
|:---|:---|
| 특징 저장소 | **노드•간선 특징** 보관 |
| 메시지 함수 | 이웃 특징 기반 **전달 메시지** 계산 |
| 집계 함수 | 이웃 메시지의 **순서 불변 결합** |
| 갱신 함수 | 현재 상태와 **집계값 결합•갱신** |
| 읽기 함수 | 노드 표현을 **과업 결과**로 변환 |

#### 한줄 요약
- **특징•메시지•집계•갱신•읽기** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **순서 불변성(Permutation Invariance)**: 이웃 입력 순서와 무관한 결과 성질이다.
- **전파 깊이(Propagation Depth)**: 관계를 반영하는 이웃 홉 범위이다.

</details>

```text
┌─────────── 메시지 전달 층 ───────────┐
│ 1. 특징 공유     2. 메시지 계산      │
│ 3. 순서 불변 집계 4. 상태 표현 갱신  │
└─────────────┬──────────────┘
              │
          과업별 출력(노드/링크/그래프)
```

### 동작 원리

1. **특징 공유**: 인접 노드 간 특징 전달
2. **메시지 계산**: 메시지 함수로 특징 변환
3. **순서 불변 집계**: 이웃 메시지 결합
4. **상태 표현 갱신**: 현재 상태와 집계값 결합

#### 한줄 요약
- **특징 공유•메시지•집계•상태 갱신** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **그래프 합성곱 신경망(Graph Convolutional Network, GCN)**: 정규화 이웃을 합성곱으로 집계한다.
- **GraphSAGE(Sample and Aggregate)**: 이웃 표본화로 귀납 학습한다.
- **그래프 어텐션 네트워크(Graph Attention Network, GAT)**: 이웃 중요도를 가중 집계한다.

</details>

| 방식 | GCN | GraphSAGE | GAT |
|:---|:---|:---|:---|
| 적용 기준 | **반지도 학습** | **대규모•변화 그래프** | **이웃 중요도 학습** |
| 핵심 특징 | **정규화 이웃 집계** | **이웃 표본화•귀납 학습** | **어텐션 가중 집계** |
| 한계 | **과평활** | **표본 편향•정보 누락** | **연산량 증가** |

#### 한줄 요약
- **그래프 규모•귀납성•이웃 중요도** 대상 따라 방식 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **이웃 표본화(Neighbor Sampling)**: 연산량 제어를 위해 이웃 일부를 선택한다.
- **평가 누출(Evaluation Leakage)**: 미래 정보가 학습에 반영돼 성능이 왜곡된다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 깊은 전파의 **과평활** | 잔차 연결•층수 제한 | **노드 구별력** 보존 |
| 이웃 확장의 **연산량 폭증** | 이웃 표본화•미니배치 학습 | **대규모 처리 효율** 확보 |
| 미래 간선의 **평가 누출** | 시간 순서 기반 그래프 분할 | **일반화 성능** 검증 |

#### 한줄 요약
- **과평활•표본 편향•평가 누출•연산량** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **집계 방식(Aggregation Method)**: 합•평균•어텐션 등 이웃 결합 규칙이다.
- **노드 구별력(Node Discriminability)**: 관계 기반 노드 표현의 구분 정도이다.

</details>

- 비유클리드 기하학적 데이터의 위상 관계를 완벽히 모델링하여 분자 생물학, 금융 보안, 추천 시스템 및 지식 그래프 분석의 새로운 지평을 연 **기하학적 딥러닝(Geometric Deep Learning) 및 관계형 AI의 최고 핵심 원천 아키텍처(Graph Neural Network / Message Passing Framework / GCN Spectral & Spatial / Inductive GraphSAGE / Attention-based GAT / Graph Transformer & Over-smoothing Control)의 확고한 표준**으로 확고히 자리 잡았으며, 거대 그래프 트랜스포머 및 LLM-GNN 융합으로 진화하는 가운데, 실무 대규모 GNN 시스템 구축 시에는 **레이어가 깊어질 때 노드 임베딩이 균일화되는 과평활(Over-smoothing)을 방지하기 위해 잔차 연결(Residual Connection) 및 레이어 수($L=2\sim 4$) 최적화를 적용하고, 수십억 엣지 대규모 그래프 처리를 위한 이웃 샘플링(Neighbor Sampling) 기반의 분산 GraphSAGE/DGL 파이프라인 구축, 이종 그래프(Heterogeneous Graph)를 위한 메타패스(Meta-path) 어텐션 설계**를 결합하여 완벽한 관계 분석력과 대규모 프로덕션 확장성을 완성

#### 한줄 요약
- **그래프 규모•귀납성•이웃 중요도** 대상 따라 GNN 방식 결정
