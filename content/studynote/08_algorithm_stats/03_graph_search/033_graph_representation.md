---
title: "033. Graph Representation"
date: "2026-04-21"
tags:
  - "studynote-algorithm-stats"
weight: 33
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Graph](/studynote/12_it_management/03_ea_isp/888_graph/))는 정점 (Vertex)과 간선 (Edge)으로 이루어진 자료구조이며, 인접 행렬 ([Adjacency](/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/) Matrix)과 인접 리스트 ([Adjacency](/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/) List) 두 가지 방식으로 컴퓨터에 표현한다.
> 2. **가치**: 인접 행렬은 O(1) 간선 조회, 인접 리스트는 O(V+E) 공간 효율 — [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 밀도에 따라 올바른 표현을 선택해야 성능을 끌어낼 수 있다.
> 3. **판단 포인트**: 밀집 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Dense [Graph](/studynote/12_it_management/03_ea_isp/888_graph/), E ≈ V^)에는 인접 행렬, 희소 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Sparse [Graph](/studynote/12_it_management/03_ea_isp/888_graph/), E ≪ V^)에는 인접 리스트가 기본 선택 기준이다.

## Ⅰ. 개요 및 필요성

[그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Graph](/studynote/12_it_management/03_ea_isp/888_graph/))는 G = (V, E)로 정의되며, V는 정점 집합, E는 간선 집합이다. 실세계의 네트워크, 지도, 소셜 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 의존성 등 수많은 문제가 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 모델링된다.

[그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)의 주요 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/):

| [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 설명 |
|:---|:---|
| 방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Directed [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)) | 간선에 방향 존재 (->) |
| 무방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Undirected [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)) | 간선에 방향 없음 (—) |
| [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Weighted [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)) | 간선에 비용/거리 부여 |
| 밀집 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Dense [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)) | E ≈ V^, 간선이 많음 |
| 희소 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Sparse [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)) | E ≪ V^, 간선이 적음 |

📢 **섹션 요약 비유**: [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 도시들(정점)과 도로들(간선)로 구성된 지도다. 표현 방식은 이 지도를 어떤 형식의 종이에 기록하느냐의 차이다.

## Ⅱ. 아키텍처 및 핵심 원리

### 예시 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)

```
정점: {A, B, C, D, E}
간선: {A-B, A-C, B-D, C-D, D-E}

     A
    / \
   B   C
    \ /
     D
     |
     E
```

### 인접 행렬 ([Adjacency](/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/) Matrix)

V×V 크기의 2차원 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/). `adj[i][j] = 1`이면 i->j 간선 존재.

```
     A  B  C  D  E
  A [0, 1, 1, 0, 0]
  B [1, 0, 0, 1, 0]
  C [1, 0, 0, 1, 0]
  D [0, 1, 1, 0, 1]
  E [0, 0, 0, 1, 0]
```

[가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 `adj[i][j] = 가중치` (없는 경우 ∞ 또는 0).

### 인접 리스트 ([Adjacency](/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/) List)

각 정점마다 연결된 정점 목록을 저장.

```
A: [B, C]
B: [A, D]
C: [A, D]
D: [B, C, E]
E: [D]
```

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 — 두 표현 방식 비교

```
+----------------------------------------------------------+
|  [인접 행렬]              [인접 리스트]                    |
|                                                          |
|    A B C D E             A ---> [B] ---> [C]              |
|  A[0 1 1 0 0]            B ---> [A] ---> [D]              |
|  B[1 0 0 1 0]            C ---> [A] ---> [D]              |
|  C[1 0 0 1 0]            D ---> [B] ---> [C] ---> [E]      |
|  D[0 1 1 0 1]            E ---> [D]                      |
|  E[0 0 0 1 0]                                            |
|                                                          |
|  공간: O(V^)             공간: O(V+E)                     |
|  간선 조회: O(1)          간선 조회: O(degree)             |
+----------------------------------------------------------+
```

### 간선 리스트 (Edge List)

모든 간선을 `(u, v, weight)` 튜플로 저장.

```
[(A,B,1), (A,C,1), (B,D,1), (C,D,1), (D,E,1)]
```

[크루스칼](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) ([Kruskal](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/)) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)처럼 간선 정렬이 필요한 경우에 적합.

### 표현 방식별 복잡도 비교

| 연산 | 인접 행렬 | 인접 리스트 | 간선 리스트 |
|:---|:---:|:---:|:---:|
| [공간 복잡도](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) | O(V^) | O(V+E) | O(E) |
| 간선 (u,v) 존재 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | O(1) | O(degree(u)) | O(E) |
| 정점 u의 이웃 순회 | O(V) | O(degree(u)) | O(E) |
| 간선 추가 | O(1) | O(1) | O(1) |
| 간선 삭제 | O(1) | O(degree) | O(E) |
| 적합 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [플로이드-워샬](/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) | [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/), [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/), [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) | [크루스칼](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) |

📢 **섹션 요약 비유**: 인접 행렬은 전국 도로 연결표 (모든 도시 쌍에 대해 O/X 표시), 인접 리스트는 각 도시의 관광 안내서 (이 도시에서 갈 수 있는 곳 목록)다.

## Ⅲ. 비교 및 연결

### 밀집 vs 희소 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서의 선택

```
V=1,000, E=200 (희소, E ≪ V^=1,000,000)
  -> 인접 행렬: 1,000,000 셀 메모리 낭비
  -> 인접 리스트: 1,200개 항목으로 충분

V=1,000, E=900,000 (밀집, E ≈ V^)
  -> 인접 리스트: 900,000개 포인터 오버헤드
  -> 인접 행렬: 1,000,000 셀로 O(1) 접근 효율적
```

### 방향/무방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 처리 차이

| 항목 | 무방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | 방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
|:---|:---|:---|
| 인접 행렬 대칭 | adj[i][j] == adj[j][i] | adj[i][j] ≠ adj[j][i] 가능 |
| 인접 리스트 | 양방향 삽입 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 삽입 |
| 간선 수 E | 리스트 항목 수 = 2E | 리스트 항목 수 = E |

📢 **섹션 요약 비유**: 방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 일방통행 도로, 무방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 양방향 도로다. 인접 행렬에서 방향 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 비대칭 행렬, 무방향은 대칭 행렬로 표현된다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

**시나리오 1**: 소셜 네트워크 팔로워 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) (V=억, E=수십억)
- 희소 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) -> 인접 리스트 필수
- 인접 행렬 시 V^=[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^16 셀 -> 물리적 불가

**시나리오 2**: [플로이드-워샬](/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) ([Floyd-Warshall](/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)) 전체 쌍 최단 경로
- O(V³) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) -> 인접 행렬로 O(1) 간선 비용 조회 최적화
- 인접 리스트라면 간선 조회마다 O(degree) 추가 비용

**시나리오 3**: [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) (Depth-First Search) / [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) (Breadth-First Search)
- 정점의 이웃 순회가 핵심 -> 인접 리스트가 O(V+E)로 효율적
- 인접 행렬 사용 시 이웃 순회에 O(V) -> 전체 [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) O(V^) 비효율

### 기술사 판단 기준

| 상황 | 권장 표현 | 이유 |
|:---|:---|:---|
| E ≈ V^ (밀집) | 인접 행렬 | 공간 효율 비슷, O(1) 접근 |
| E ≪ V^ (희소) | 인접 리스트 | O(V+E) 공간 절약 |
| 간선 정렬 필요 | 간선 리스트 | [크루스칼](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) 등 |
| 간선 존재 빈번 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 인접 행렬 | O(1) 직접 조회 |
| [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)/[BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) | 인접 리스트 | 이웃 순회 효율 |

📢 **섹션 요약 비유**: [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 표현 선택은 수납 방식 선택과 같다. 물건이 가득 찬 서랍(밀집)은 표 형식이 낫고, 듬성듬성한 물건(희소)은 품목 목록이 공간 낭비가 없다.

## Ⅴ. 기대효과 및 결론

[그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 표현 방식의 선택은 이후 모든 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 시간·[공간 복잡도](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)에 직접적인 영향을 미친다. 희소 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 인접 행렬을 사용하면 O(V^) 공간 낭비와 O(V) 이웃 순회 비효율이 동시에 발생하여 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 성능을 수십 배 떨어뜨린다.

**핵심 결론**: [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 설계의 첫 단계는 항상 "이 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 희소한가, 밀집한가?"를 묻는 것이다.

📢 **섹션 요약 비유**: [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 표현 방식은 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 설계와 같다. 잘못된 선택은 코드 한 줄 수정 없이 성능을 몇 십 배 떨어뜨린다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) (Depth-First Search) | 활용 | 인접 리스트로 O(V+E) 탐색 |
| [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) (Breadth-First Search) | 활용 | 인접 리스트로 O(V+E) 탐색 |
| [플로이드-워샬](/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) | 활용 | 인접 행렬로 O(V³) 최단 경로 |
| [크루스칼](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) ([Kruskal](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/)) | 활용 | 간선 리스트로 정렬 후 [MST](/studynote/08_algorithm_stats/03_graph_search/041_mst/) |
| [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) | 활용 | 인접 리스트로 O((V+E)log V) |
| 희소 행렬 (Sparse Matrix) | 연관 | 메모리 최적화된 행렬 표현 |

### 📈 관련 키워드 및 발전 흐름도

```text
[:---]
    |
    v
[DFS (Depth-First Search)]
    |
    v
[BFS (Breadth-First Search)]
    |
    v
[플로이드-워샬]
    |
    v
[크루스칼 (Kruskal)]
    |
    v
[다익스트라 (Dijkstra)]
    |
    v
[희소 행렬 (Sparse Matrix)]
```

이 흐름도는 :---에서 출발해 [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 🗺️ [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 도시들(정점)과 도로들(간선)로 이루어진 지도인데, 이 지도를 컴퓨터에 기록하는 방법이 두 가지다.
2. 📊 인접 행렬은 모든 도시 쌍에 대해 "도로 있음/없음"을 큰 표에 적는 방식이고, 인접 리스트는 각 도시의 메모장에 연결된 도시만 적는 방식이다.
3. 🏙️ 도시가 많고 도로가 적으면 메모장 방식이 훨씬 효율적이고, 도로가 거의 모두 연결되어 있으면 표 방식이 더 빠르다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 175

<- **이전**: [3. 해시 탐색 (Hash Search) — O(1) 평균](/studynote/08_algorithm_stats/03_graph_search/032_hash_search/)
**다음**: [5. 깊이 우선 탐색 (DFS, Depth-First Search) — 스택/재귀](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) ->

---
