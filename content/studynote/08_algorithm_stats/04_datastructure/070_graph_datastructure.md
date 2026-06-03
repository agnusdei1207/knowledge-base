---
title: 18. 그래프 (Graph) — 방향/무방향, 가중/비가중
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 그래프 ([[104_graph|Graph]])는 G = (V, E)로 정의되며, 정점(Vertex)과 간선(Edge)의 집합으로 복잡한 [[083_relationship_in_er_model|관계]]와 연결성을 표현하는 비선형 자료구조다.
> 2. **가치**: 소셜 네트워크의 친구 [[083_relationship_in_er_model|관계]], 지도의 도로, 소프트웨어 의존성 등 현실의 모든 [[083_relationship_in_er_model|관계]]망이 그래프로 모델링되므로, [[035_bfs|BFS]]·[[034_dfs|DFS]]·최단 경로·[[039_topological_sort|위상 정렬]] 등 그래프 [[001_algorithm_definition|알고리즘]]은 실무 핵심이다.
> 3. **판단 포인트**: 정점 수 V와 간선 수 E의 비율로 희소 그래프(E ≪ V²)는 인접 리스트, 밀집 그래프(E ≈ V²)는 인접 행렬로 표현하는 것이 공간·시간 효율에 유리하다.

---

## Ⅰ. 개요 및 필요성

트리는 계층적 부모-자식 [[083_relationship_in_er_model|관계]]만 표현하지만, 현실의 [[083_relationship_in_er_model|관계]]는 훨씬 복잡하다. 친구는 서로 친구일 수 있고(무방향), 도로는 일방통행일 수 있다(방향). 그래프는 이런 **임의의 [[100_many_to_many_model|다대다]] [[083_relationship_in_er_model|관계]]**를 표현하는 가장 범용적인 자료구조다.

### 그래프 [[104_classification_analysis|분류]] 체계

| [[104_classification_analysis|분류]] 기준 | 종류 | 설명 |
|:---|:---|:---|
| 방향성 | 무방향 (Undirected) | 간선이 양방향 (A-B = B-A) |
| | 방향 (Directed, Digraph) | 간선이 [[008_단방향_반이중_전이중|단방향]] (A→B ≠ B→A) |
| [[267_weight_bias_activation|가중치]] | 비가중 (Unweighted) | 간선에 비용 없음 |
| | 가중 (Weighted) | 간선에 거리·비용·용량 부여 |
| 연결성 | 연결 (Connected) | 모든 정점 쌍 경로 존재 |
| | 비연결 (Disconnected) | 고립된 [[603_component_independent_deployment_unit|컴포넌트]] 존재 |
| 순환 | 순환 (Cyclic) | 사이클 존재 |
| | 비순환 (Acyclic) | 사이클 없음 (트리, [[401_bayesian_network_dag_causality|DAG]]) |

📢 **섹션 요약 비유**: 그래프는 도시 지도다—교차로가 정점, 도로가 간선, 일방통행은 방향 간선, 통행 시간은 [[267_weight_bias_activation|가중치]]다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[033_graph_representation|그래프 표현]] 방법

#### 인접 행렬 ([[358_ospf_adjacency_hello_lsa_lsdb|Adjacency]] Matrix)

```
정점: {0, 1, 2, 3}
간선: 0→1, 0→2, 1→3, 2→3

     0  1  2  3
  ┌──────────────┐
0 │  0  1  1  0  │
1 │  0  0  0  1  │
2 │  0  0  0  1  │
3 │  0  0  0  0  │
  └──────────────┘

공간: O(V²)
간선 존재 여부: O(1)
인접 정점 나열: O(V)
```

#### 인접 리스트 ([[358_ospf_adjacency_hello_lsa_lsdb|Adjacency]] List)

```
0: [1, 2]
1: [3]
2: [3]
3: []

공간: O(V + E)
간선 존재 여부: O(degree)
인접 정점 나열: O(degree)
```

### 인접 행렬 vs 인접 리스트 비교

| 항목 | 인접 행렬 | 인접 리스트 |
|:---|:---:|:---:|
| 공간 | O(V²) | O(V + E) |
| 간선 존재 [[396_validation|확인]] | O(1) | O(degree) |
| 인접 정점 나열 | O(V) | O(degree) |
| 적합한 그래프 | 밀집(Dense) | 희소(Sparse) |
| [[267_weight_bias_activation|가중치]] 저장 | 행렬 값 | 노드에 [[267_weight_bias_activation|weight]] 필드 |

### 핵심 그래프 용어

- **차수 (Degree)**: 정점에 연결된 간선 수 (방향 그래프: 진입차수 in-degree, 진출차수 out-degree)
- **핸드셰이킹 보조정리 (Handshaking Lemma)**: 무방향 그래프에서 모든 정점 차수의 합 = 2|E|
- **[[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]])**: 방향 그래프 + 사이클 없음 → [[039_topological_sort|위상 정렬]]([[039_topological_sort|Topological Sort]]) 가능
- **이분 그래프 (Bipartite [[104_graph|Graph]])**: 정점을 두 집합으로 나눠 모든 간선이 집합 간에만 존재 → 2-채색 가능
- **연결 [[603_component_independent_deployment_unit|컴포넌트]] (Connected [[603_component_independent_deployment_unit|Component]])**: 서로 도달 가능한 정점들의 최대 부분 그래프

📢 **섹션 요약 비유**: 핸드셰이킹 보조정리는 파티에서 모든 악수 횟수를 세는 원리—각 사람이 한 악수 수를 합하면 실제 악수 횟수의 두 배가 된다.

---

## Ⅲ. 비교 및 연결

### 그래프 vs 트리 vs [[056_linked_list|연결 리스트]]

| 항목 | 그래프 | 트리 | [[056_linked_list|연결 리스트]] |
|:---|:---:|:---:|:---:|
| [[083_relationship_in_er_model|관계]] | 임의 N:M | 부모-자식 1:N | 선형 1:1 |
| 사이클 | 가능 | 없음 | 없음([[008_단방향_반이중_전이중|단방향]]) |
| 루트 | 없음 | 1개 | 없음 |
| 순회 | [[035_bfs|BFS]]/[[034_dfs|DFS]] | 전위/중위/후위 | [[030_linear_search|선형 탐색]] |

### 주요 그래프 [[001_algorithm_definition|알고리즘]] 지도

```
그래프
├── 탐색
│   ├── BFS (Breadth-First Search)  → 최단 경로(비가중)
│   └── DFS (Depth-First Search)    → 사이클 감지, 위상 정렬
├── 최단 경로
│   ├── Dijkstra            → 단일 출발, 비음수 가중치
│   ├── Bellman-Ford        → 단일 출발, 음수 가중치 허용
│   └── Floyd-Warshall      → 전체 쌍 최단 경로
├── MST (최소 신장 트리)
│   ├── Kruskal             → 간선 정렬 + 유니온-파인드
│   └── Prim                → 정점 기반 탐욕
└── 위상 정렬 (DAG)         → 의존성 처리, 빌드 시스템
```

📢 **섹션 요약 비유**: 그래프 [[001_algorithm_definition|알고리즘]]은 지도 앱의 기능 목록이다—최단 거리 안내([[036_dijkstra|Dijkstra]]), 전체 도로 연결([[041_mst|MST]]), 공사 구간 우회(음수 [[267_weight_bias_activation|가중치]]/[[170_bellman_ford|Bellman-Ford]]).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **소셜 네트워크**: 친구 [[083_relationship_in_er_model|관계]](무방향), 팔로우(방향), 최단 인맥 경로([[035_bfs|BFS]])
- **지도/내비게이션**: 도로 그래프, 가중 최단 경로([[036_dijkstra|Dijkstra]]/A*)
- **의존성 그래프 ([[401_bayesian_network_dag_causality|DAG]])**: Maven/npm 빌드, Airflow [[401_bayesian_network_dag_causality|DAG]], [[205_kubernetes_container_orchestration|Kubernetes]] 오브젝트 의존성
- **웹 크롤러**: [[286_page_frame|페이지]](정점) + 하이퍼링크(방향 간선), [[035_bfs|BFS]] 탐색
- **네트워크 플로우**: [[043_max_flow|최대 유량]]([[043_max_flow|Max Flow]]), Ford-Fulkerson [[001_algorithm_definition|알고리즘]]

### 기술사 판단 기준

```
간선 확인이 빈번 + 작은 밀집 그래프   →  인접 행렬
대규모 희소 그래프 (소셜/웹)           →  인접 리스트
최단 경로 (비음수)                     →  Dijkstra O((V+E)logV)
사이클 없음 + 순서 처리                →  위상 정렬 (DAG)
무방향 연결 요소 파악                  →  유니온-파인드 O(α)
```

📢 **섹션 요약 비유**: [[033_graph_representation|그래프 표현]] 선택은 도시 지도 종류 선택이다—격자 도시(밀집)면 2차원 지도(행렬), 듬성듬성 도로(희소)면 도로 목록(리스트)이 효율적이다.

---

## Ⅴ. 기대효과 및 결론

그래프는 선형·계층 구조로 표현 불가능한 임의의 [[083_relationship_in_er_model|관계]]를 모델링하는 유일한 범용 자료구조다. 표현 방식(인접 행렬 vs 인접 리스트)의 공간·시간 트레이드오프를 이해하고, 문제 유형에 따라 [[035_bfs|BFS]]/[[034_dfs|DFS]]·최단 경로·[[039_topological_sort|위상 정렬]]·[[041_mst|최소 신장 트리]] [[001_algorithm_definition|알고리즘]]을 적재적소에 적용하는 것이 그래프 역량의 핵심이다.

**결론**: 복잡한 [[083_relationship_in_er_model|관계]] 표현과 경로 탐색이 필요한 모든 시나리오에서 그래프가 1순위 모델이며, E/V² 비율로 표현 방식을 결정한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| [[035_bfs|BFS]] / [[034_dfs|DFS]] | [[613_graph_bfs_memory|그래프 탐색]] [[001_algorithm_definition|알고리즘]] |
| [[036_dijkstra|Dijkstra]] | 가중 그래프 최단 경로 |
| [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) | [[039_topological_sort|위상 정렬]]의 전제 조건 |
| [[041_mst|MST]] (Minimum Spanning Tree) | 그래프의 최소 비용 연결 구조 |
| 유니온-파인드 ([[070_union_find|Union-Find]]) | 연결 [[603_component_independent_deployment_unit|컴포넌트]] 판단 |
| 이분 그래프 (Bipartite) | 2-채색 가능한 특수 그래프 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[선형 자료구조 (Array / Linked List) — 1차원 순서 관계]
    │
    ▼
[트리 (Tree) — 계층 관계, 사이클 없는 연결 그래프]
    │
    ▼
[그래프 (Graph) — 정점(V) + 간선(E), 방향/무방향·가중/비가중]
    │
    ▼
[BFS (Breadth-First Search) / DFS (Depth-First Search) — 그래프 탐색]
    │
    ▼
[최단 경로 (Dijkstra·Bellman-Ford·Floyd-Warshall) → 네트워크 플로우]
```
그래프는 트리보다 일반적인 [[083_relationship_in_er_model|관계]]를 표현하며, [[035_bfs|BFS]]/[[034_dfs|DFS]] 탐색을 기반으로 최단 경로·[[039_topological_sort|위상 정렬]]·네트워크 플로우 [[001_algorithm_definition|알고리즘]]으로 확장된다.
### 👶 어린이를 위한 3줄 비유 설명

1. 그래프는 도시 지도야—도시(정점)들을 도로(간선)로 연결하고, 일방통행 도로는 방향 간선이야.
2. 친구 지도는 무방향 그래프—내가 너 친구면 너도 내 친구니까 화살표가 양방향이야.
3. 거미줄처럼 얽힌 [[083_relationship_in_er_model|관계]]는 배열이나 트리로 못 표현하지만, 그래프로는 다 그릴 수 있어!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 175

← **이전**: [[069_chaining|17. 체인법 (Chaining) — 연결 리스트 충돌 처리]]
**다음**: [[071_segment_tree|세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트]] →

---
