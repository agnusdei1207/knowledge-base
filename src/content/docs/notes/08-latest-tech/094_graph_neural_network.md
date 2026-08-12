---
sidebar:
  order: 94
  label: "094. 그래프 신경망 (Graph Neural Network)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "그래프 신경망 (Graph Neural Network)"
date: "2026-08-06T23:27:50+09:00"
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

<details>
<summary>핵심 용어</summary>

- **GNN(Graph Neural Network)**: 노드(Node)•엣지(Edge)로 구성된 그래프의 위상 정보(Topological Info)와 구조를 메시지 패싱(Message Passing)으로 학습하는 신경망 모델
- **간선 관계(Edge Relation)**: 두 노드를 연결하는 관계의 유형•강도•방향성 정보

</details>

- 정의: 이웃 노드 특징을 순차 집계하여 노드•링크•전체 그래프 표현(Representation)을 학습하는 모델
- 배경: 독립 표본(i.i.d) 모델의 위상 정보 활용 한계 및 간선 관계 유실 극복 필요
- 한줄 요약: 그래프 위상 정보 기반의 구조적 관계 학습 체계 구현

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **메시지 전달(Message Passing)**: 이웃 노드 특징 계산•전달을 통해 상태를 최신화하는 학습 과정
- **과평활(Over-smoothing)**: 층(Layer) 깊어짐에 따라 노드 벡터가 수렴하여 구별력이 저하되는 현상
- **과압축(Over-squashing)**: 그래프 내 방대한 정보가 고정 벡터 압축 시 주요 관계가 손실되는 현상
- 한줄 요약: 이웃 정보의 순서 불변 집계를 통한 그래프 구조적 표현 학습

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **집계 함수 (Aggregation Function)**: 이웃 메시지를 순서 무관하게 결합하는 함수
- **갱신 함수 (Update Function)**: 현재 상태와 집계값을 결합하여 표현 갱신
- **읽기 함수 (Readout Function)**: 노드 표현을 과업별 결과로 변환하는 함수

</details>

| 구성요소 | 책임 |
|:---|:---|
| 특징 저장소 | 노드, 간선 정보 보관 |
| 메시지 함수 | 이웃 특징 기반 전달 메시지 계산 |
| 집계 함수 | 이웃 메시지의 순서 불변 결합 |
| 갱신 함수 | 현재 노드 정보와 집계값 결합 및 갱신 |
| 읽기 함수 | 학습된 노드 표현을 과업별 결과로 변환 |

#### 한줄 요약
- 메시지 집계•갱신•출력을 통한 그래프 표현 학습 체계 구현

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **순서 불변성 (Permutation Invariance)**: 입력 순서와 무관한 동일 결과 도출
- **전파 깊이 (Propagation Depth)**: 관계 반영 범위(홉수) 결정

</details>

```text
┌─────────── 메시지 전달 층 ───────────┐
│ 1. 특징 공유     2. 메시지 계산      │
│ 3. 순서 불변 집계 4. 상태 표현 갱신  │
└─────────────┬──────────────┘
              │
          과업별 출력(노드/링크/그래프)
```

**동작 원리**
1. **전달**: 인접 노드 간 특징 공유
2. **계산**: 메시지 함수 기반 특징 변환
3. **집계**: 순서 불변 결합 수행
4. **갱신**: 현재 노드 상태 업데이트
5. **출력**: 노드•링크•그래프 결과 생성

#### 한줄 요약
- 그래프 위상 정보 기반의 단계별 메시지 전달 및 표현 갱신

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **GCN (Graph Convolutional Network)**: 정규화 이웃 정보를 합성곱 방식으로 집계
- **GraphSAGE (Sample and Aggregate)**: 대규모 그래프 이웃 표본화 및 귀납 학습
- **GAT (Graph Attention Network)**: 어텐션 기반 이웃별 중요도 가중 학습

</details>

| 방식 | GCN | GraphSAGE | GAT |
|:---|:---|:---|:---|
| 주요 적용 | 반지도 학습 | 대규모/변화 그래프 | 중요도 학습 필수 |
| 핵심 특징 | 정규화 이웃 집계 | 이웃 표본화/귀납 학습 | 어텐션 가중치 적용 |
| 한계점 | 과평활 발생 | 표본 편향/정보 누락 | 연산량 증가 |

#### 한줄 요약
- 그래프 규모와 이웃 정보의 특성에 따른 집계 방식 최적화

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **이웃 표본화 (Neighbor Sampling)**: 대규모 그래프에서 연산량 제어를 위한 노드 일부 선택
- **평가 누출 (Evaluation Leakage)**: 미래 정보가 학습에 반영되어 측정값이 왜곡되는 현상

</details>

| 문제 | 대책 | 기대 효과 |
|:---|:---|:---|
| 과평활 | 잔차 연결(Residual Connection) 및 층수 제한 | 노드 구별력 보존 |
| 연산량 폭증 | 이웃 표본화(Neighbor Sampling) 및 미니배치 학습 | 효율적인 대규모 그래프 처리 |
| 평가 누출 | 시간 순서 기반 그래프 분할(Temporal Split) | 모델 일반화 성능 검증 |

#### 한줄 요약
- 이웃 샘플링 및 계층 전파 제어를 통한 효율적 학습 체계 운영

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **집계 방식 (Aggregation Method)**: 이웃 특징 결합 규칙 (합, 평균, 어텐션 등)
- **노드 구별력 (Node Discriminability)**: 관계 기반 노드 표현 유지 정도

</details>

- 이웃 범위와 그래프 동적 변화를 고려한 집계 방식 최적화
- 과평활 통제 및 노드 구별력 중심의 모델 설계

#### 한줄 요약
- 이웃 기반의 구조적 표현 학습 체계 적용
