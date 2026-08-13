---
sidebar:
  order: 109
  label: "109. Neo4j 그래프 데이터베이스 (Neo4j Graph Database)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "Neo4j 그래프 데이터베이스 (Neo4j Graph Database)"
date: "2026-08-13T21:21:00+09:00"
tags:
  - "notes-software"
weight: 109
extra:
  question_no: "109"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 70
  priority_note: "137•138회 연속, 그래프 탐색 적용성 높음"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Neo4j**: 엔티티를 노드(Node), 관계를 간선(Edge), 속성을 Property로 표현하는 대표적 Property Graph 기반 그래프 데이터베이스(Graph Database).
- **Index-Free Adjacency (무색인 인접성)**: RDBMS의 조인 테이블(Join Table)이나 인덱스 B+Tree 탐색 없이, 각 노드가 자신의 물리적 이웃 노드 메모리 포인터(Direct Pointer)를 직접 가리켜 $O(1)$의 조인 성능을 달성하는 그래프 핵심 메커니즘.
- **Cypher Query Language**: Neo4j 전용의 서술적 그래프 질의 언어로, `MATCH (u:User)-[:FRIEND]->(f:User) RETURN f` 형태의 직관적 노드-관계 아스키 아트 표기법 사용.

</details>

- 정의/개념: 노드•관계•속성으로 연결 데이터를 저장하는 **Neo4j**
- 배경/필요성: 관계 깊이가 늘면 반복 조인의 **중간 결과•탐색 비용** 증가

#### 한줄 요약

- 연결선을 저장해 친구의 친구를 선 따라 찾는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Property Graph Model**: 노드(Node)와 관계(Relationship) 모두에 키-값(Key-Value) 속성(Property) 및 레이블(Label)을 자유롭게 부착할 수 있는 가변 모델.
- **ACID Transaction Support**: NoSQL 계열임에도 불구하고 100% Strict ACID 트랜잭션을 완전 보장.

</details>

- **Index-Free Adjacency**: 인접 관계를 직접 연결해 단계별 탐색
- **Property Graph (Node, Edge, Label, Property)** 모델 지원
- **Cypher Declarative Query Language** 및 **Strict ACID** 지원

#### 한줄 요약

- 탐색은 자연스럽지만 시작점과 깊이를 제한해야 후보 경로가 폭발하지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Node, Relationship, Property, Label**: Property Graph의 4대 기본 구성 성분.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Neo4j Property Graph Model                      │
├────────────────────────────────────────────────────────────────────────┤
│ (User:Alice {age:30}) ───[:KNOWS {since:2026}]───► (User:Bob {age:28})│
│   ▲                      ▲                          ▲                  │
│   [Node A & Label]       [Relationship & Property]  [Node B & Label]   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 노드(Node)와 노드 사이를 방향성 및 속성을 지닌 관계(Relationship)로 직접 포인터 연결하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **Node** | 사람•상품 등 실체와 식별자 표현 |
| **Relationship** | 노드 간 유형•방향을 가진 연결 표현 |
| **Property** | 노드•관계의 키-값 부가 정보 저장 |
| **Label** | 노드 분류와 시작점 탐색 범위 지정 |

#### 한줄 요약

- 개체, 연결선, 부가값, 출발점 색인, 탐색 담당자로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Traversing vs Index Lookup**: RDBMS는 조인 때마다 인덱스 B+Tree 탐색($O(\log N)$)을 반복하지만, Neo4j는 메모리 포인터를 쫓아 바로 다음 노드로 이동($O(1)$).

</details>

```text
[그래프 질의]
     │
     ▼
1. 시작 노드 탐색
     │
     ▼
2. 관계 유형 필터
     │
     ▼
3. 인접 관계 순회
     │
     ▼
4. 깊이•조건 판정
     │
     ▼
5. 경로•노드 반환
```

### 동작 원리

1. **시작 노드 탐색**: 레이블•속성 인덱스로 출발점 식별
2. **관계 유형 필터**: 방향•유형•속성 조건 적용
3. **인접 관계 순회**: 연결된 관계와 이웃 노드 방문
4. **깊이•조건 판정**: 최대 Hop과 경로 조건 검사
5. **경로•노드 반환**: 일치 결과를 투영•집계

#### 한줄 요약

- 먼저 출발점을 좁힌 뒤 정해진 종류와 방향의 연결선만 따라간다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Graph Model Tradeoff**: 관계 탐색 및 지식 그래프에는 압도적이나, 전체 집계(`SUM`, `AVG`)나 정형 스키마 변경 시에는 고비용화.

</details>

| 비교 항목 | RDBMS (Relational DB) | Neo4j (Graph DB) |
|:---|:---|:---|
| 데이터 모델 | **2차원 테이블 (Row x Column)** | **Property Graph (Node - Edge - Property)** |
| 관계 표현 방식 | **Foreign Key & Join Table** | **Direct Memory Pointer (Index-Free Adjacency)**|
| 다단계 관계 탐색 | 조인 선택도•중간 결과에 좌우 | 단계별 인접 관계 수에 좌우 |
| 쿼리 언어 | SQL | **Cypher (아스키 아트 표기법)** |

#### 한줄 요약

- 그래프•관계형 모델 선택 기준에서 표는 조건으로 다시 결합하고 그래프는 저장된 연결선을 따라간다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Super Node Problem**: 연예인/인플루언서처럼 1개 노드에 수백만 개의 Relationship 엣지가 몰려 있어, 탐색 시 메모리 폭증과 락 병목을 유발하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수백만 엣지가 몰린 **Super Node** 탐색 시 메모리 폭사 | **Super Node 분할(Sub-node) 및 Relationship Property 필터링**| Traversal 속도 보장 |
| 시작 노드 인덱스 미지정 시 전체 탐색 | **선택도 높은 레이블•속성 인덱스** | 시작 후보 축소 |
| N-Hop 범위 미지정 시 무한 그래프 순회 폭주 | **Cypher 쿼리에 최대 Hop 수 지정 (`-[:KNOWS*1..3]->`)** | Infinite Loop 차단 |

> 사례: **카카오뱅크 FDS (이상금융거래 탐색) & LLM RAG용 Knowledge Graph 구축**

#### 한줄 요약

- 출발 사용자와 권한 관계 종류, 최대 단계를 정해야 빠르고 설명 가능한 결과를 얻는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Neo4j 수립 기준(Neo4j Architecture Standards)**: Property Graph 수용성, N-Hop Traversal 성능, Cypher 쿼리 튜닝 및 Super Node 해결성에 의거한 체계.

</details>

- 연결 경로가 핵심이면 **Neo4j**, 정형 집계•원장은 RDBMS 선택

#### 한줄 요약

- Neo4j 적용 판단 기준은 연결선이 답일 때 시작점과 탐색 깊이를 제한한다.
