+++
title = "7. 다익스트라 (Dijkstra) — 단일 출발 최단 경로, 비음수 가중치"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다익스트라 (Dijkstra) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 단일 출발점 (Single Source)으로부터 모든 정점까지의 최단 거리를 탐욕적 (Greedy) 방법으로 계산한다.
> 2. **가치**: [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) ([Priority Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)) 기반으로 O((V+E)log V) 시간에 GPS 내비게이션, 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 등 실세계 최단 경로 문제를 해결하는 핵심 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 3. **판단 포인트**: 음수 간선이 존재하면 다익스트라는 오동작 — [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/) ([Bellman-Ford](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/)) 또는 존슨 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 전환해야 한다.

## Ⅰ. 개요 및 필요성

다익스트라 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 1956년 에츠허르 다익스트라가 설계한 최단 경로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 시작 정점 s에서 출발하여 현재 알려진 최단 거리가 가장 짧은 미방문 정점을 우선 처리하는 탐욕 전략으로, 각 정점을 한 번씩만 처리한다.

| 특성 | 내용 |
|:---|:---|
| [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | O((V+E)log V) — 이진 힙 |
| [공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) | O(V) |
| 전제 조건 | 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) (Non-negative weights) |
| 핵심 자료구조 | [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) (Min-Heap) |
| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 유형 | 탐욕 (Greedy) |

다익스트라가 필요한 상황:

- GPS 경로 안내 (도로 거리/시간 기반 최단 경로)
- 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) ([OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/), [IS-IS](/knowledge-base/studynote/03_network/07_network_layer_routing/363_is_is_intermediate_system_clnp_telecom/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))
- 게임 경로 탐색 (이동 비용이 다른 지형)

📢 **섹션 요약 비유**: 다익스트라는 가장 가까운 정류장에서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 타는 방식으로 목적지까지 가는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 항상 "지금까지 알려진 가장 가까운 곳"을 먼저 방문한다.

## Ⅱ. 아키텍처 및 핵심 원리

### 기본 동작 순서 (이완, Relaxation)

```
그래프: A─(4)─B, A─(2)─C, C─(1)─B, B─(5)─D, C─(8)─D
시작: A

초기: dist = {A:0, B:∞, C:∞, D:∞}

1단계: A 처리 (dist=0)
  → B: 0+4=4 < ∞ → dist[B]=4
  → C: 0+2=2 < ∞ → dist[C]=2
  dist = {A:0, B:4, C:2, D:∞}

2단계: C 처리 (dist=2, 최솟값)
  → B: 2+1=3 < 4 → dist[B]=3 (이완!)
  → D: 2+8=10 < ∞ → dist[D]=10
  dist = {A:0, B:3, C:2, D:10}

3단계: B 처리 (dist=3)
  → D: 3+5=8 < 10 → dist[D]=8 (이완!)
  dist = {A:0, B:3, C:2, D:8}

4단계: D 처리 (dist=8) → 완료
최종: A→0, B→3, C→2, D→8
```

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 — 이완 과정과 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)

```
┌──────────────────────────────────────────────────────────┐
│                     (4)                                  │
│            A ──────────── B                              │
│            │              │                              │
│           (2)            (5)                             │
│            │              │                              │
│            C ──(1)──────► B    ← 이완: 2+1=3 < 4        │
│            │                                             │
│           (8)                                            │
│            │                                             │
│            D                                             │
│                                                          │
│  우선순위 큐 (Min-Heap):                                   │
│  [(0,A)] → [(2,C),(4,B)] → [(3,B),(4,B),(10,D)]          │
│          → [(4,B),(8,D),(10,D)] → [(8,D),(10,D)]         │
│  ※ 중복 항목(4,B)은 꺼낼 때 dist 불일치로 무시             │
└──────────────────────────────────────────────────────────┘
```

### 이완 (Relaxation) 연산

다익스트라의 핵심 연산:

```
if dist[u] + weight(u,v) < dist[v]:
    dist[v] = dist[u] + weight(u,v)
    parent[v] = u
    우선순위 큐에 (dist[v], v) 삽입
```

| 단계 | 설명 |
|:---|:---|
| 초기화 | dist[s]=0, 나머지 ∞, 큐에 (0,s) 삽입 |
| 반복 | 큐에서 최솟값 꺼냄 → 이미 처리된 정점이면 스킵 |
| 이완 | 인접 간선 전체에 대해 거리 갱신 시 큐에 삽입 |
| 종료 | 큐가 빌 때까지 반복 |

📢 **섹션 요약 비유**: 이완은 "더 짧은 길을 발견했을 때 지도를 업데이트"하는 과정이다. 처음에는 모든 길이 무한히 멀어 보이다가, 탐색할수록 더 좋은 경로가 발견된다.

## Ⅲ. 비교 및 연결

### 최단 경로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 음수 간선 | 음수 사이클 | 출발점 |
|:---|:---:|:---:|:---:|:---:|
| 다익스트라 | O((V+E)log V) | 불가 | 불가 | 단일 |
| [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/) | O(VE) | 가능 | 검출 가능 | 단일 |
| [플로이드-워샬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) | O(V³) | 가능 | 검출 가능 | 전체 쌍 |
| [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) | O(V+E) | 불가 (비가중치) | 해당 없음 | 단일 |

### 음수 간선에서 다익스트라가 실패하는 이유

```
A ─(3)→ B ─(-5)→ C
A ─(2)→ C

다익스트라: A→C = 2 (잘못됨)
실제 최단:  A→B→C = 3-5 = -2 (더 짧음)

이유: B를 처리하기 전에 C가 이미 처리됨 → 이완 기회 상실
```

📢 **섹션 요약 비유**: 음수 간선에서 다익스트라가 실패하는 것은 "지금까지 가장 싼 표"를 먼저 결제했는데, 나중에 더 싼 환불 가능 표가 발견된 상황과 같다. 이미 결제한 것은 취소가 안 된다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

**시나리오 1**: GPS 내비게이션 (T-Map, 카카오맵)
- 도로 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 출발지→목적지 최단 경로
- 실시간 교통 정보 반영: 간선 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 동적 업데이트
- 실제 구현: 다익스트라 + 이분할(양방향) + A* 혼합

**시나리오 2**: [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) (Open [Shortest Path](/knowledge-base/studynote/05_database/07_exam_summary/547_graph_shortest_path_db_mapping/) First) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)
- 라우터 간 [링크 상태](/knowledge-base/studynote/03_network/07_network_layer_routing/348_link_state_routing_dijkstra_spf/) 정보로 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구성
- 다익스트라로 최단 경로 트리 ([SPF](/knowledge-base/studynote/03_network/09_application_layer_web_email/495_spf_sender_policy_framework/) Tree) 계산
- 링크 변화 발생 시 다익스트라 재실행

**시나리오 3**: 게임 경로 탐색 (지형 비용 차등)
- 늪지(비용 5), 평지(비용 1), 도로(비용 0.5)
- 다익스트라로 최소 이동 비용 경로 탐색

### 기술사 판단 포인트

| 상황 | 선택 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 이유 |
|:---|:---|:---|
| 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), 단일 출발 | 다익스트라 | O((V+E)log V) 최적 |
| 음수 간선, 단일 출발 | [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/) | 음수 간선 처리 가능 |
| 전체 쌍 최단 경로 | [플로이드-워샬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) | O(V³), 밀집 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| 비가중치 최단 경로 | [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) | O(V+E) 가장 빠름 |
| 실시간 동적 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | D* Lite / A* | 동적 경로 재계산 |

📢 **섹션 요약 비유**: 다익스트라는 "지금 할인 중인 가장 싼 항공권"을 예약하고 목적지를 향해 나아가는 전략이다. 할인율이 음수(추가 비용 발생)가 없는 한 항상 최저가 경로를 찾는다.

## Ⅴ. 기대효과 및 결론

다익스트라 (Dijkstra) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 단일 출발 최단 경로를 O((V+E)log V)에 보장하는 실무 표준 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. GPS, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), 게임 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 등 방대한 분야에서 직접 활용되며, 음수 간선 처리는 [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/)로 위임하는 명확한 역할 분리가 설계 포인트다.

**핵심 결론**: 간선 비용이 모두 양수인 환경에서는 다익스트라가 최단 경로의 표준이다. 음수 비용이 나타나는 순간 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 교체하라.

📢 **섹션 요약 비유**: 다익스트라는 항상 남은 구간 중 "이미 확정된 가장 싼 경로"에 올라타는 전략이다. 확정된 경로는 뒤집히지 않기 때문에 각 정점을 딱 한 번만 처리하면 된다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/) ([Bellman-Ford](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/)) | 대안 | 음수 간선 처리 가능 |
| [플로이드-워샬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) ([Floyd-Warshall](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)) | 대안 | 전체 쌍 최단 경로 |
| A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 확장 | [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)으로 가속 |
| [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 활용 | 라우터 최단 경로 트리 |
| 이완 (Relaxation) | 핵심 연산 | 더 짧은 경로 발견 시 갱신 |
| [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) (Min-Heap) | 자료구조 | O((V+E)log V) 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
[그래프 이론 (Graph Theory)]
    │
    ▼
[BFS 너비 우선 탐색 (Breadth-First Search)]
    │
    ▼
[다익스트라 알고리즘 (Dijkstra Algorithm)]
    │
    ▼
[우선순위 큐 (Priority Queue)]
    │
    ▼
[A* 알고리즘 (A* Algorithm)]
    │
    ▼
[벨만-포드 알고리즘 (Bellman-Ford Algorithm)]
```

[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 탐색에서 최단 경로 문제로 발전하며 다익스트라가 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)를 활용해 효율성을 높이고 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 탐색으로 이어지는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 🗺️ 다익스트라는 목적지까지 가는 여러 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 노선 중, 항상 "지금 당장 가장 빠른 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)"를 타는 방법으로 최단 경로를 찾는다.
2. ✅ 한 번 목적지가 확정되면 다시 확인하지 않아도 된다 — 더 좋은 경로는 이미 다 시도해 본 후이기 때문이다.
3. ❌ 하지만 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 요금이 마이너스(돈을 돌려주는)인 노선이 있으면 이 방법은 틀릴 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 36 / 175

← **이전**: [6. 너비 우선 탐색 (BFS, Breadth-First Search) — 큐, 최단 경로](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/)
**다음**: [9. 플로이드-워샬 (Floyd-Warshall) — 전체 쌍 최단 경로, O(V³)](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) →

---
