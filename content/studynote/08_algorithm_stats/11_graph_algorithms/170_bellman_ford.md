+++
title = "08. 벨만-포드 (Bellman-Ford)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 벨만-포드 (Bellman-Ford) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 모든 간선을 반복적으로 완화 (Relaxation) 하여 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 있어도 단일 시작점 최단 경로를 구하는 동적 계획법 ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) 기반 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 단순히 최단 경로만 찾는 것이 아니라, V번째 반복에서도 거리가 더 줄어들면 음수 사이클 (Negative Cycle) 이 존재한다고 판정해 "유한한 최단 경로가 없음"까지 감지할 수 있다.
> 3. **판단 포인트**: [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)는 O(VE)로 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))보다 느리지만, 음수 간선 가능성이나 음수 사이클 검출이 요구되면 가장 신뢰할 수 있는 기본 해법이다.

---

## Ⅰ. 개요 및 필요성

벨만-포드는 가중 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 한 시작점으로부터 다른 모든 정점까지의 최단 거리를 구하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 가장 큰 특징은 <strong>음수 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 간선</strong>을 허용한다는 점이다. 그래서 비용이 감소하는 쿠폰, 환율 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 변환, [거리 벡터](/knowledge-base/studynote/03_network/07_network_layer_routing/347_distance_vector_routing_bellman_ford/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)처럼 "한 번 지나갈수록 더 유리해질 수 있는" 모델에서도 사용할 수 있다.

이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 필요한 이유는 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)가 탐욕적 확정 전략을 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문이다. [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)는 한 번 확정한 거리가 다시 줄어들지 않는다는 전제가 있어야 안전한데, 음수 간선이 들어오면 이 전제가 무너진다. 반면 벨만-포드는 성급하게 확정하지 않고 모든 간선을 여러 번 훑으며 거리를 점진적으로 개선한다.

수학적 근거는 단순하다. 음수 사이클이 없다면 최단 경로는 같은 정점을 반복하지 않는 단순 경로가 되고, 단순 경로는 최대 V-1개의 간선만 포함한다. 따라서 모든 간선을 V-1번 완화하면 길이 1, 2, 3, ... , V-1인 최단 경로 정보가 차례로 전파되어 결국 정답에 도달한다.

아래 그림은 왜 반복이 필요한지를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         One more pass means shortest paths with one more edge        │
├──────────────────────────────────────────────────────────────────────┤
│ Pass 0 : only source is known                                        │
│ Pass 1 : shortest paths using <= 1 edge become correct               │
│ Pass 2 : shortest paths using <= 2 edges become correct               │
│ ...                                                                  │
│ Pass V-1 : all simple shortest paths are covered                     │
└──────────────────────────────────────────────────────────────────────┘
```

즉 벨만-포드는 "지금 가장 짧아 보이는 길"을 믿기보다, <strong>경로 길이가 늘어날수록 더 좋은 해가 뒤늦게 나타날 수 있다</strong>는 가능성을 끝까지 열어 둔다. 느리지만 음수 세계에서 안전한 이유가 여기에 있다.

- **📢 섹션 요약 비유**: [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)가 눈앞의 지름길을 먼저 확정하는 빠른 길잡이라면, 벨만-포드는 지도를 여러 번 다시 보며 숨은 할인길이 있는지 끝까지 확인하는 신중한 안내원과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

벨만-포드의 구현은 간단하다. 시작 정점 거리는 0, 나머지는 무한대 (INF, Infinity) 로 두고, 모든 간선 `(u, v, w)`에 대해 `dist[u] + w < dist[v]` 이면 `dist[v]`를 갱신한다. 이 연산을 완화 (Relaxation) 라고 하며, 전체 간선 집합에 대해 V-1번 반복한다.

| 단계 | 수행 내용 | 의미 |
| :--- | :--- | :--- |
| 초기화 | `dist[source] = 0`, 나머지 INF | 아직 모르는 정점은 미도달 상태 |
| 반복 완화 | 모든 간선 순회 | 한 번의 반복마다 경로 길이 1 증가분 반영 |
| [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) | 한 바퀴 동안 갱신이 없으면 중단 | 실무 최적화 포인트 |
| 음수 사이클 검사 | 한 번 더 완화 시도 | 값이 줄면 유한 최단 경로 없음 |

아래 상태도는 벨만-포드의 계산 흐름을 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  Bellman-Ford relaxation workflow                    │
├──────────────────────────────────────────────────────────────────────┤
│ Init dist[source]=0, others=INF                                     │
│        │                                                             │
│        ▼                                                             │
│ Repeat V-1 times: for every edge (u,v,w)                            │
│        │                                                             │
│        ├─ if dist[u] + w < dist[v] -> update dist[v]                │
│        └─ if no update in a full pass -> early stop                 │
│        │                                                             │
│        ▼                                                             │
│ One extra pass                                                       │
│        ├─ update exists -> negative cycle reachable                  │
│        └─ no update     -> distances finalized                       │
└──────────────────────────────────────────────────────────────────────┘
```

음수 사이클 판정이 중요한 이유는, 그런 사이클이 시작점에서 도달 가능하면 최단 거리 개념 자체가 무너진다는 데 있다. 예를 들어 한 바퀴 돌 때마다 비용이 -3씩 줄어드는 사이클이 있으면, 그 경로를 더 많이 돌수록 비용이 계속 낮아져 최적해가 정해지지 않는다. 벨만-포드는 V번째 검사에서 이 현상을 포착한다.

실무 코드에서는 두 가지를 특히 주의한다. 첫째, 도달하지 못한 정점의 `INF + w` 연산에서 오버플로를 피해야 한다. 둘째, 간선 리스트 기반 구현이 자연스럽기 때문에 인접 리스트보다 "edge list" 순회가 더 직접적일 때가 많다.

- **📢 섹션 요약 비유**: 벨만-포드는 한 번 산책하며 길을 정하는 방식이 아니라, 모든 골목을 여러 차례 돌면서 더 싼 길이 나타날 때마다 지도를 새로 그리는 방식이다.

---

## Ⅲ. 비교 및 연결

벨만-포드의 위치를 이해하려면 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/), 플로이드-워셜 ([Floyd-Warshall](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)), 그리고 개선형으로 자주 언급되는 SPFA ([Shortest Path](/knowledge-base/studynote/05_database/07_exam_summary/547_graph_shortest_path_db_mapping/) Faster [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) 와 비교해야 한다.

| 항목 | [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) | 벨만-포드 (Bellman-Ford) | 플로이드-워셜 ([Floyd-Warshall](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)) |
| :--- | :--- | :--- | :--- |
| 목표 | 단일 시작점 최단 경로 | 단일 시작점 최단 경로 | 모든 쌍 최단 경로 |
| 음수 간선 | 불가 | 가능 | 가능 |
| 음수 사이클 검출 | 직접적으론 어려움 | 가능 | 가능 |
| [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | O(E log V) | O(VE) | O(V³) |
| 대표 장점 | 빠름 | 안전함, 검출 가능 | 전체 관계를 한 번에 계산 |

[다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)는 빠르지만 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)라는 계약이 깨지면 신뢰할 수 없다. 플로이드-워셜은 모든 정점 쌍을 한꺼번에 다루기 때문에 작은 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 분석에는 좋지만, 단일 시작점 문제에 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)에는 비용이 크다. 벨만-포드는 그 중간이 아니라, <strong>음수 간선과 음수 사이클 검출이 필요할 때 선택하는 별도 해법</strong>이다.

이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 금융 모델에도 연결된다. [거리 벡터](/knowledge-base/studynote/03_network/07_network_layer_routing/347_distance_vector_routing_bellman_ford/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 본질적으로 분산형 벨만-포드이고, 환율 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에 `-log(rate)`를 적용하면 차익 거래는 음수 사이클 탐지 문제로 바뀐다. 즉 벨만-포드는 교과서 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 머물지 않고 실제 인프라 논리를 뒷받침한다.

SPFA는 "갱신 가능성이 있는 정점 주변만 다시 보자"는 아이디어로 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 개선할 수 있지만, 최악의 경우는 여전히 O(VE)다. 따라서 SPFA는 실전 최적화 선택지이지, 벨만-포드의 이론적 대체재라고 보긴 어렵다.

- **📢 섹션 요약 비유**: [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)가 양수 도로만 있는 도시에서 빠른 스포츠카라면, 벨만-포드는 뒤늦은 할인길과 함정까지 체크하는 안전한 탐사차이고, 플로이드-워셜은 도시 전체 지도를 통째로 다시 계산하는 관제 시스템에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

벨만-포드는 보통 두 가지 상황에서 선택된다. 첫째, 입력 데이터에 음수 간선이 섞일 수 있을 때다. 둘째, 단순 경로 계산보다 "모델 자체가 모순되지 않는가"를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 할 때다. 그래서 외환 차익 거래 탐지, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 비용 모델, 일부 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 분석에 적합하다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에 음수 간선이 존재하거나 존재 가능성이 있는가?
2. 시작점 기준 최단 경로만 필요한가, 아니면 모든 쌍 최단 경로가 필요한가?
3. 음수 사이클 존재 여부를 판정해야 하는가?
4. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 규모가 커서 O(VE) 비용이 감당 가능한가?
5. [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)나 SPFA 같은 실무 최적화를 적용할 가치가 있는가?

### 채택 / 회피 판단

- **채택**: 음수 간선 허용, 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 필요, 차익 거래 탐지, [거리 벡터](/knowledge-base/studynote/03_network/07_network_layer_routing/347_distance_vector_routing_bellman_ford/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 해석
- **회피 또는 대안 검토**: [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 모두 비음수이고 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)가 큰 경우에는 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/), 모든 쌍이 필요하면 플로이드-워셜 또는 존슨 (Johnson) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 검토

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 음수 간선 가능성을 무시하고 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)를 사용하는 경우
- `INF` 처리 없이 오버플로를 일으키는 경우
- 음수 사이클이 있는 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 거리값만 출력하고 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 생략하는 경우
- SPFA가 평균적으로 빠르다는 이유만으로 항상 우월하다고 오해하는 경우

실무 코드에서는 [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)가 매우 유용하다. 한 번의 전체 순회에서 아무 갱신도 일어나지 않았다면 이미 모든 최단 거리가 안정화된 것이므로 남은 반복을 생략할 수 있다. 그러나 이 최적화는 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선일 뿐, 최악의 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) 자체를 바꾸지는 않는다.

- **📢 섹션 요약 비유**: 건물 전체를 점검해야 할 때, 중간에 더 이상 고장 난 곳이 안 보이면 점검을 일찍 끝낼 수는 있지만, 원래 설계상 모든 층을 다 확인할 준비는 하고 있어야 하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

벨만-포드의 가장 큰 장점은 속도보다 신뢰성이다. 음수 간선이 있는 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서도 최단 경로를 일관되게 계산하고, 음수 사이클까지 검출해 모델이 논리적으로 성립하는지 알려 준다. 그래서 계산 결과를 "숫자"뿐 아니라 "유효성 판정"까지 포함한 답으로 확장해 준다.

대신 비용은 크다. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)가 커질수록 O(VE)는 빠르게 부담스러워지고, 모든 문제에 무심코 적용하기엔 무겁다. 따라서 벨만-포드는 범용 기본값이라기보다, <strong>음수 세계를 다뤄야 할 때 선택하는 안전한 표준 도구</strong>로 기억하는 편이 정확하다.

결론적으로 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 핵심은 완화 연산 자체가 아니라, "최단 경로가 아직 뒤집힐 수 있다"는 가능성을 끝까지 열어 두는 태도에 있다. 빠른 확정보다 늦은 교정을 택하기 때문에, 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 환경에서도 무너지지 않는다.

- **📢 섹션 요약 비유**: 벨만-포드는 빨리 도착했다고 길이 맞다고 우기지 않고, 마지막까지 할인길이나 함정길이 없는지 다시 확인한 뒤에야 진짜 지도를 완성하는 꼼꼼한 탐험가와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 완화 (Relaxation) | 벨만-포드의 핵심 갱신 연산 |
| 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) (Negative [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)) | [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) 대신 벨만-포드를 써야 하는 이유 |
| 음수 사이클 (Negative Cycle) | 유한 최단 경로가 존재하지 않음을 뜻하는 구조 |
| [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) | 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 조건에서 더 빠른 대안 |
| [거리 벡터](/knowledge-base/studynote/03_network/07_network_layer_routing/347_distance_vector_routing_bellman_ford/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (Distance-Vector [Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)) | 분산형 벨만-포드의 대표 응용 |
| 존슨 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Johnson's [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) | 벨만-포드를 재가중치 단계에 활용하는 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
Weighted graph shortest path
    │
    ├─ non-negative weights -> Dijkstra
    └─ possible negative weights
              │
              ▼
      Bellman-Ford relaxation
              │
              ├─ stable after V-1 passes -> shortest paths
              └─ still improves at Vth pass -> negative cycle
              │
              ▼
Distance-vector routing · arbitrage detection · Johnson reweighting
```

이 흐름은 최단 경로 문제에서 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 등장할 때 왜 벨만-포드가 별도의 해법으로 필요해지는지를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 벨만-포드는 미로의 모든 길을 여러 번 살펴보며 더 좋은 길이 숨어 있는지 확인하는 방법이에요.
2. 어떤 길은 지나가면 사탕을 하나 더 주는 특별한 길이라서, 그냥 빠른 길찾기보다 더 조심해야 해요.
3. 만약 빙글빙글 돌수록 사탕이 계속 늘어나는 길이 있으면, 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 "여긴 답이 없어"라고 알려줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 170 / 175

← **이전**: [10. 진화 알고리즘 — 유전 알고리즘 (GA), 입자 군집 최적화 (PSO)](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/169_evolutionary_algorithms/)
**다음**: [171. 프림 알고리즘 (Prim's Algorithm)](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/171_prim_algorithm/) →

---
