+++
title = "16. 최대 유량 (Max Flow) — Ford-Fulkerson / Edmonds-Karp"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 최대 유량 (Max Flow) 문제는 소스 (Source)에서 싱크 (Sink)까지 흘릴 수 있는 최대 흐름량을 구하는 문제로, 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Residual [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))와 증가 경로 (Augmenting Path)를 이용해 해결한다.
> 2. **가치**: Ford-Fulkerson, Edmonds-Karp [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) ([Bipartite Matching](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/)), 프로젝트 선택 등 다양한 문제를 최대 유량 문제로 환원하여 해결한다.
> 3. **판단 포인트**: Edmonds-Karp ([BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) 기반 Ford-Fulkerson)는 O(VE²)으로 정수 용량에서 항상 종료하며, 최대 유량 = [최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/) (Max-Flow Min-Cut 정리)은 핵심 정리다.

## Ⅰ. 개요 및 필요성

최대 유량 문제는 방향 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 각 간선에 용량 제한이 있을 때, 소스 s에서 싱크 t까지 보낼 수 있는 최대 흐름을 구하는 문제다.

| 특성 | 내용 |
|:---|:---|
| Ford-Fulkerson 시간 | O(E × max_flow) |
| Edmonds-Karp 시간 | O(VE²) |
| Dinic's [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | O(V²E) |
| 핵심 개념 | 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), 증가 경로, 역방향 간선 |
| 핵심 정리 | Max-Flow = Min-Cut |

최대 유량이 필요한 상황:

- 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 최대화 (인터넷 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))
- [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) (구직자-회사, 학생-기숙사 배정)
- 프로젝트 선택 문제 (손익 최대화)
- 이미지 세분화 ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) Cut)

📢 **섹션 요약 비유**: 최대 유량은 수도관 네트워크에서 수원지(소스)에서 도시(싱크)까지 흘릴 수 있는 최대 물의 양을 구하는 것이다. 각 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)의 지름(용량)이 흐름을 제한한다.

## Ⅱ. 아키텍처 및 핵심 원리

### 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Residual [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))

```
원본 간선 (u→v, 용량 c, 현재 흐름 f):
  잔여 정방향 용량: c - f  (더 보낼 수 있는 양)
  잔여 역방향 용량: f      (취소할 수 있는 양)

핵심: 역방향 간선이 있기 때문에 "이미 보낸 흐름을 우회"하는 경로도 활용 가능
```

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 — 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)와 증가 경로

```
┌──────────────────────────────────────────────────────────┐
│  원본 그래프 (용량):         잔여 그래프 (흐름 2 후):     │
│  S──(10)→A──(8)→T           S──(8)→A──(6)→T             │
│  S──(5)→B──(6)→T            S──(3)→B──(4)→T             │
│  A──(4)→B                   A──(2)→B, B──(2)→A(역방향)  │
│                                                          │
│  증가 경로 탐색 (BFS):                                   │
│  Path1: S→A→T  (용량=8) → 흐름 8 추가                   │
│  Path2: S→B→T  (용량=5) → 흐름 5 추가                   │
│  Path3: S→A→B→T (역방향 활용) → 추가 가능               │
│                                                          │
│  최대 유량 = 경로 탐색 불가 시점의 총 흐름               │
└──────────────────────────────────────────────────────────┘
```

### Ford-Fulkerson vs Edmonds-Karp

```
Ford-Fulkerson:
  증가 경로를 DFS로 탐색
  정수 용량이면 종료, 비정수면 무한루프 가능
  시간: O(E × max_flow)

Edmonds-Karp:
  증가 경로를 BFS로 탐색 (최단 증가 경로)
  항상 O(VE²)에 종료
  시간: O(VE²)
```

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 경로 탐색 | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 종료 보장 |
|:---|:---:|:---:|:---:|
| Ford-Fulkerson | [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) | O(E × max_flow) | 정수 용량만 |
| Edmonds-Karp | [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) | O(VE²) | 항상 |
| Dinic's | [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) + [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) | O(V²E) | 항상 |

📢 **섹션 요약 비유**: Ford-Fulkerson은 물길을 아무 방향으로나 찾고, Edmonds-Karp는 항상 가장 짧은 물길을 먼저 찾는다. 짧은 길을 우선하면 전체 탐색 횟수가 줄어든다.

## Ⅲ. 비교 및 연결

### Max-Flow Min-Cut 정리

최대 유량 = [최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/) (Min-Cut)의 용량

```
최소 컷: 소스와 싱크를 분리하는 간선 집합 중 총 용량이 최소인 것
Max-Flow = Min-Cut 용량
→ 최대 유량 해로부터 최소 컷 도출 가능
```

### [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) ([Bipartite Matching](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/))으로 환원

```
이분 그래프: 좌측 집합 L, 우측 집합 R
→ 소스 s에서 L의 모든 정점에 용량 1 간선
→ R의 모든 정점에서 싱크 t로 용량 1 간선
→ L-R 간 원래 간선은 용량 1
→ 최대 유량 = 최대 매칭 수
```

📢 **섹션 요약 비유**: [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/)의 최대 유량 변환은 구직자와 회사 사이에 지원 가능한 경로만 있고, 각 사람은 한 회사에만 매칭될 수 있는 채용 네트워크를 만드는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

**시나리오 1**: [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) — 과목-교실 배정
- 과목 집합과 교실 집합이 있을 때, 최대 몇 과목을 배정할 수 있는가?
- 최대 유량으로 O(VE²) 해결

**시나리오 2**: 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 분석
- 서버 네트워크에서 소스([데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/))→싱크([CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)) 최대 전송 가능 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)
- Max-Flow = Min-Cut → 병목 링크([최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/)) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)

**시나리오 3**: 프로젝트 선택 문제
- 각 프로젝트는 이익/비용이 있고 의존 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 존재
- 최대 이익 = 최대 유량 모델링으로 O(VE²) 해결

### 기술사 판단 포인트

| 상황 | 판단 |
|:---|:---|
| 정수 용량, 소규모 | Ford-Fulkerson |
| 일반적인 경우 | Edmonds-Karp (O(VE²)) |
| 대규모 고성능 | Dinic's [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (O(V²E)) |
| [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) | 최대 유량으로 환원 |
| 병목 링크 찾기 | Max-Flow 후 Min-Cut 계산 |

📢 **섹션 요약 비유**: 최대 유량은 도시의 하수도 설계 문제와 같다. 어떤 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)가 막히면([최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/)) 전체 흐름이 제한된다는 것을 알아내는 것이 핵심이다.

## Ⅴ. 기대효과 및 결론

최대 유량 (Max Flow) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 네트워크 최적화의 핵심 도구로, Ford-Fulkerson의 기본 아이디어를 Edmonds-Karp가 BFS로 개선하여 항상 O(VE²)에 종료를 보장한다. Max-Flow Min-Cut 정리는 네트워크 분석과 [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) 등 다양한 문제의 이론적 기반이다.

**핵심 결론**: 유량, 매칭, 분리 문제는 모두 최대 유량으로 통합된다. 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)와 역방향 간선이 이 통합의 핵심 메커니즘이다.

📢 **섹션 요약 비유**: 최대 유량 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 가장 막힌 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)([최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/))를 찾아내는 과정이기도 하다. 물이 최대로 흐르면, 그 흐름을 막는 최소한의 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 집합이 자동으로 드러난다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 잔여 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Residual [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) | 핵심 개념 | 남은 용량 + 역방향 간선 |
| 증가 경로 (Augmenting Path) | 핵심 개념 | s→t 경로 탐색 |
| Max-Flow Min-Cut 정리 | 핵심 정리 | 최대 유량 = [최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/) |
| [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) | 응용 | 최대 유량으로 환원 |
| Dinic's [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 확장 | O(V²E) 고성능 |
| [최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/) (Min-Cut) | 연계 | 병목 간선 집합 |


### 📈 관련 키워드 및 발전 흐름도

```text
[DFS 기반 Ford-Fulkerson — 증가 경로 탐색, 무한 루프 위험(비정수 용량)]
    │
    ▼
[BFS 기반 Edmonds-Karp — O(VE²) 다항 시간 보장, 최단 증가 경로 선택]
    │
    ▼
[Dinic's Algorithm — 계층 그래프 + 차단 흐름, O(V²E) 고성능]
    │
    ▼
[Max-Flow Min-Cut 정리 — 최대 유량 = 최소 컷, 네트워크 병목 분석 기반]
    │
    ▼
[이분 매칭 (Bipartite Matching) / 프로젝트 선택 — 최대 유량으로 환원하는 응용]
```
이 흐름은 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 유량 문제의 기초 아이디어(Ford-Fulkerson)가 수렴 보장의 결함을 극복하며 효율적인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 정제되고, 그 결과물인 Max-Flow Min-Cut 정리가 매칭·분리·스케줄링 등 다양한 문제를 통합하는 이론적 기반으로 자리잡는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 🚿 최대 유량은 수원지에서 도시까지 여러 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)로 연결된 수도관에서 물을 최대로 보내는 방법을 찾는 문제다.
2. 🔄 역방향 간선은 "이미 보낸 물을 다른 방향으로 돌릴 수 있다"는 것을 의미하여, 더 좋은 경로를 발견하면 이전 선택을 취소할 수 있다.
3. 🔎 최대한 물을 보내고 나면, 전체 흐름을 막는 가장 작은 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 집합([최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/))이 자동으로 드러난다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 43 / 175

← **이전**: [14. 크루스칼 (Kruskal) — 간선 정렬 + Union-Find](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/)
**다음**: [19. 합병 정렬 (Merge Sort) — O(n log n), 안정, O(n) 공간](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/) →

---
